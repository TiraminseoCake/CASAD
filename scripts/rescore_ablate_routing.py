#!/usr/bin/env python3
"""Post-hoc routing-input ablation (Approach A).

At each best-epoch checkpoint, compute 5 routing variants by zeroing out one
input at inference time:

  full        : score = φ + β·log(W̃+ε) + Δ(X)      gate = M_learn·(0.05+0.95·M)
  no_phi      : score = 0 + β·log(W̃+ε) + Δ(X)      gate = M_learn·(0.05+0.95·M)
  no_W        : score = φ + 0            + Δ(X)     gate = M_learn·(0.05+0.95·M)
  no_M        : score = φ + β·log(W̃+ε) + Δ(X)      gate = M_learn·1.0
  no_Mlearn   : score = φ + β·log(W̃+ε) + Δ(X)      gate = 1.0·(0.05+0.95·M)

For each variant, we recompute:
    pred      = Σ_{τ,i} Π_ablated * V + b_pred          (S_pred = mean |x - pred|)
    edge_str  = Π_ablated * |V|                          (S_str  = ||Norm(E) - CRS||_F)
    Π         = Π_ablated                                (S_route= ||Π - Π_ref||_F)

Then A = S_pred × (S_str + S_route)   [mult_raw fusion, dataset-invariant baseline].
Metrics computed with paper_eval_one.

Original results not modified. Output:
  results/rescored_ablate/{out_dir}/{entity}/seed{k}/{entity}_seed{k}_ablate_{variant}.csv
"""
import argparse
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import get_cfg_defaults
from datasets.build import load_entity
from datasets.sliding_window import SlidingWindowDataset
from layers.ops import normalize_causal_tensor_torch
from model.build import build_model
from model.scoring import lag_aggregate, matrix_deviation_per_tau, prediction_score
from utils.evaluation import paper_eval_one
from utils.misc import set_seed
from torch.utils.data import DataLoader


VARIANTS = ['full', 'no_phi', 'no_W', 'no_M', 'no_Mlearn']
METRIC_KEYS = [
    ('AUC-PR', 'AUC_PR'), ('AUC-ROC', 'AUC_ROC'),
    ('Standard-F1', 'F1'), ('PA-F1', 'PA_F1'),
    ('Event-based-F1', 'Event_F1'), ('R-based-F1', 'R_F1'),
    ('Affiliation-F', 'Aff_F'),
    ('VUS-ROC', 'VUS_ROC'), ('VUS-PR', 'VUS_PR'),
]


def _load_cfg(cfg_path: str):
    cfg = get_cfg_defaults()
    cfg.merge_from_file(cfg_path)
    return cfg


def _ablated_routing(model, local_delta, variant: str):
    """Recreate get_pred_weights logic, zeroing the specified input.
    Returns Π [B, τ, N, N] (same shape as model's pred_weights when dynamic_graph on)."""
    # Effective gate
    M_learn = torch.sigmoid(model.edge_log_alpha)      # [τ, N, N]
    if variant == 'no_M':
        gate = M_learn  # drop (0.05 + 0.95·M) factor
    elif variant == 'no_Mlearn':
        if model.has_te_prior:
            gate = 0.05 + 0.95 * model.te_prior_gate    # M_learn -> 1.0
        else:
            gate = torch.ones_like(M_learn)
    else:
        # full, no_phi, no_W keep gate unchanged
        gate = M_learn * (0.05 + 0.95 * model.te_prior_gate) if model.has_te_prior else M_learn

    # score
    if variant == 'no_W' or not model.has_te_prior or model.te_prior_blend <= 0.0:
        prior_bias = 0.0
    else:
        prior_bias = model.te_prior_blend * torch.log(model.te_prior_weight.clamp_min(1e-8))

    phi = torch.zeros_like(model.pred_logits) if variant == 'no_phi' else model.pred_logits

    if local_delta is None:
        if torch.is_tensor(prior_bias):
            score = phi + prior_bias
        else:
            score = phi
    else:
        if torch.is_tensor(prior_bias):
            score = phi.unsqueeze(0) + prior_bias.unsqueeze(0) + local_delta
        else:
            score = phi.unsqueeze(0) + local_delta

    return model._normalize_weight_tensor(score, gate)


@torch.no_grad()
def score_windows_ablate(model, series_TN, device, batch, scoring_cfg, variant: str,
                          Π_ref=None):
    """Like score_windows_raw but replaces routing with the ablated variant."""
    model.eval()
    ds = SlidingWindowDataset(series_TN, model.L)
    loader = DataLoader(ds, batch_size=batch, shuffle=False, drop_last=False, num_workers=0)

    W = len(ds)
    P_w = np.zeros((W,), dtype=np.float32)
    C_w = np.zeros((W,), dtype=np.float32)
    G_w = np.zeros((W,), dtype=np.float32)

    cls_ref = model.cls_ref.detach()
    w_ref = model.w_ref.detach() if Π_ref is None else Π_ref.to(device)
    offset = 0

    for X in loader:
        X = X.to(device)
        # Standard forward — we ignore pred/pred_weights below and rebuild them
        _, _, C_all, _, edge_value, _, _, _, local_delta = model(X)

        Π_ablated = _ablated_routing(model, local_delta, variant)  # [B, τ, N, N] or [τ, N, N]
        if Π_ablated.dim() == 3:
            Π_ablated = Π_ablated.unsqueeze(0).expand(X.shape[0], -1, -1, -1)

        # Recompute prediction and edge strength using ablated Π
        edge_effect = edge_value * Π_ablated
        pred_ab = edge_effect.sum(dim=(1, 2)) + model.pred_bias   # [B, N]
        edge_strength_ab = Π_ablated * edge_value.abs()

        # S_pred
        x_true_next = X[:, -1, :]
        err = (x_true_next - pred_ab).abs()
        P = prediction_score(err, agg=scoring_cfg.P_AGG, topk=scoring_cfg.P_TOPK)

        # S_str
        if model.has_cls_ref:
            cls_cur = normalize_causal_tensor_torch(edge_strength_ab)
            cdiff = cls_cur - cls_ref.unsqueeze(0)
            C_per_tau = matrix_deviation_per_tau(cdiff, agg=scoring_cfg.C_AGG, topk=scoring_cfg.C_TOPK)
            Cscore = lag_aggregate(C_per_tau, mode=scoring_cfg.CAUSAL_LAG_AGG)
        else:
            Cscore = torch.zeros_like(P)

        # S_route
        if model.has_w_ref:
            gdiff = Π_ablated - w_ref.unsqueeze(0)
            G_per_tau = matrix_deviation_per_tau(gdiff, agg=scoring_cfg.G_AGG, topk=scoring_cfg.G_TOPK)
            Gscore = lag_aggregate(G_per_tau, mode=scoring_cfg.GRAPH_LAG_AGG)
        else:
            Gscore = torch.zeros_like(P)

        bsz = X.shape[0]
        P_w[offset:offset+bsz] = P.detach().cpu().numpy().astype(np.float32)
        C_w[offset:offset+bsz] = Cscore.detach().cpu().numpy().astype(np.float32)
        G_w[offset:offset+bsz] = Gscore.detach().cpu().numpy().astype(np.float32)
        offset += bsz

    return {'P_raw': P_w, 'C_raw': C_w, 'G_raw': G_w}


def _find_best_epoch(source_dir: Path, entity: str, seed: int):
    csv_path = source_dir / entity / f'seed{seed}' / f'{entity}_seed{seed}_epoch_metrics.csv'
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path)
    df['_score'] = df[['AUC_PR','AUC_ROC','VUS_PR','VUS_ROC','F1','Aff_F']].sum(axis=1)
    return int(df.loc[df['_score'].idxmax(), 'epoch'])


def _rescore_one_seed(cfg, entity, seed_dir: Path, seed: int, device, variants):
    best_ep = _find_best_epoch(seed_dir.parent.parent, entity.name, seed)
    if best_ep is None:
        return None
    ckpt_path = seed_dir / 'ckpt' / f'{entity.name}_seed{seed}_ep{best_ep}.pt'
    if not ckpt_path.exists():
        return None

    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    model = build_model(cfg, N=entity.N).to(device)
    model.load_state_dict(ck['state_dict'], strict=True)
    model._current_epoch = int(ck.get('epoch', best_ep))
    model.eval()

    out = {}
    start = cfg.PICAAD.L - 1
    for variant in variants:
        raw = score_windows_ablate(model, entity.test_z, device,
                                   batch=cfg.TEST.BATCH_SIZE,
                                   scoring_cfg=cfg.PICAAD.SCORING,
                                   variant=variant)
        # mult_raw fusion for the final anomaly score
        A_win = raw['P_raw'] * (raw['C_raw'] + raw['G_raw'])
        A_t = np.full((entity.y.shape[0],), np.nan, dtype=np.float32)
        A_t[start:] = A_win
        mtr = paper_eval_one(A_t, entity.y, start, cfg.EVAL)
        out[variant] = {'epoch': best_ep, 'is_final': 1,
                        **{short: float(mtr.get(long, float('nan')))
                           for long, short in METRIC_KEYS}}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cfg', required=True)
    ap.add_argument('--source_dir', required=True)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--entities', default='')
    ap.add_argument('--seeds', default='0,1,2,3')
    ap.add_argument('--variants', default=','.join(VARIANTS))
    a = ap.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'[ablate] device={device}', flush=True)

    cfg = _load_cfg(a.cfg); cfg.freeze()

    source_dir = Path(a.source_dir).resolve()
    out_dir = Path(a.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if a.entities.strip():
        entities = [e.strip() for e in a.entities.split(',') if e.strip()]
    else:
        entities = sorted([p.name for p in source_dir.iterdir()
                           if p.is_dir() and (p / 'seed0').exists()])
    seeds = [int(s) for s in a.seeds.split(',') if s.strip()]
    variants = [v.strip() for v in a.variants.split(',') if v.strip() in VARIANTS]

    print(f'[ablate] entities={len(entities)} seeds={seeds} variants={variants}', flush=True)

    set_seed(0)
    n_total = len(entities) * len(seeds)
    n_done = 0
    for ent_name in entities:
        try:
            entity = load_entity(cfg, ent_name)
        except Exception as exc:
            print(f'  [skip] {ent_name}: {exc}', flush=True)
            continue
        for seed in seeds:
            seed_dir = source_dir / ent_name / f'seed{seed}'
            if not seed_dir.exists():
                n_done += 1; continue
            print(f'  [{n_done+1}/{n_total}] {ent_name} seed{seed}', flush=True)
            res = _rescore_one_seed(cfg, entity, seed_dir, seed, device, variants)
            if res is None:
                print(f'    [skip] no best-epoch or ckpt', flush=True)
                n_done += 1; continue
            out_seed_dir = out_dir / ent_name / f'seed{seed}'
            out_seed_dir.mkdir(parents=True, exist_ok=True)
            for variant, row in res.items():
                pd.DataFrame([row]).to_csv(
                    out_seed_dir / f'{ent_name}_seed{seed}_ablate_{variant}.csv',
                    index=False,
                )
            n_done += 1

    print(f'[ablate] done: {n_done}/{n_total}', flush=True)


if __name__ == '__main__':
    main()
