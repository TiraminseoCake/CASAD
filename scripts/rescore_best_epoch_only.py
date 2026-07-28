#!/usr/bin/env python3
"""Minimal re-score: only the best-epoch checkpoint per (entity, seed).

Reads results/parallel/{run}/summary_best_epoch.csv to find each entity's
best epoch under the original multiplicative fusion, then re-evaluates that
single checkpoint with the four fusion variants. This avoids the 16× cost
of a full-sweep re-score and is sufficient for a "does additive fusion beat
multiplicative?" question at fixed model checkpoints.

Per-fusion output: results/rescored/{out_dir}/{entity}/seed{k}/
    best_epoch_metrics_{fusion}.csv  (one row = one seed's best epoch)

Aggregation script (aggregate_rescored_best_epoch.py) collects these into
the same MACRO_AVG format as the original summary_best_epoch.csv.

Usage:
    CUDA_VISIBLE_DEVICES=0 python scripts/rescore_best_epoch_only.py \\
        --cfg scripts/configs/psm.yaml \\
        --source_dir results/parallel/psm_20260701-221416 \\
        --out_dir    results/rescored_best/psm_baseline \\
        --entities   PSM --seeds 0,1,2,3 \\
        --fusions    add_calib
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
from model.build import build_model
from model.scoring import score_windows_raw
from utils.evaluation import paper_eval_one
from utils.misc import robust_loc_scale, set_seed


FUSIONS = ['mult_raw', 'add_calib', 'add_raw', 'mult_calib',
           'P_only', 'C_only', 'G_only',
           # Leave-one-out (calibrated addition, matching add_calib baseline):
           #   no_P_add = Cn + Gn, no_C_add = Pn + Gn, no_G_add = Pn + Cn
           'no_P_add', 'no_C_add', 'no_G_add']
METRIC_KEYS = [
    ('AUC-PR', 'AUC_PR'),
    ('AUC-ROC', 'AUC_ROC'),
    ('Standard-F1', 'F1'),
    ('PA-F1', 'PA_F1'),
    ('Event-based-F1', 'Event_F1'),
    ('R-based-F1', 'R_F1'),
    ('Affiliation-F', 'Aff_F'),
    ('VUS-ROC', 'VUS_ROC'),
    ('VUS-PR', 'VUS_PR'),
]


def _load_cfg(cfg_path: str):
    cfg = get_cfg_defaults()
    cfg.merge_from_file(cfg_path)
    return cfg


def _robust_normalize(arr, center, scale):
    z = (arr.astype(np.float64) - float(center)) / max(float(scale), 1e-6)
    return np.maximum(z, 0.0).astype(np.float32)


def _find_best_epoch_from_original(source_dir: Path, entity: str, seed: int):
    """Return the best epoch (per training-time eval) for one (entity, seed).
    Uses the entity's per-seed epoch_metrics.csv (not the aggregated
    summary_best_epoch.csv, because the latter aggregates across seeds)."""
    csv_path = source_dir / entity / f'seed{seed}' / f'{entity}_seed{seed}_epoch_metrics.csv'
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path)
    # match aggregator's selection metric set
    for c in ['AUC_PR', 'AUC_ROC', 'VUS_PR', 'VUS_ROC', 'F1', 'Aff_F']:
        if c not in df.columns:
            return None
    df['_score'] = df[['AUC_PR', 'AUC_ROC', 'VUS_PR', 'VUS_ROC', 'F1', 'Aff_F']].sum(axis=1)
    return int(df.loc[df['_score'].idxmax(), 'epoch'])


def _rescore_one_checkpoint(cfg, entity, ckpt_path, device, wanted, epoch):
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    model = build_model(cfg, N=entity.N).to(device)
    model.load_state_dict(ck['state_dict'], strict=True)
    model._current_epoch = int(ck.get('epoch', epoch))
    model.eval()

    with torch.no_grad():
        train_raw = score_windows_raw(model, entity.train_z, device,
                                      batch=cfg.TRAIN.BATCH_SIZE,
                                      scoring_cfg=cfg.PICAAD.SCORING)
        test_raw = score_windows_raw(model, entity.test_z, device,
                                     batch=cfg.TEST.BATCH_SIZE,
                                     scoring_cfg=cfg.PICAAD.SCORING)

    P_te, C_te, G_te = test_raw['P_raw'], test_raw['C_raw'], test_raw['G_raw']
    wanted_set = set(wanted)

    A_map = {}
    # Individual scores (normalization irrelevant for ranking-based metrics)
    if 'P_only' in wanted_set:
        A_map['P_only'] = P_te
    if 'C_only' in wanted_set:
        A_map['C_only'] = C_te
    if 'G_only' in wanted_set:
        A_map['G_only'] = G_te
    if 'mult_raw' in wanted_set:
        A_map['mult_raw'] = P_te * (C_te + G_te)
    if 'add_raw' in wanted_set:
        A_map['add_raw'] = P_te + C_te + G_te
    calib_variants = {'add_calib', 'mult_calib', 'no_P_add', 'no_C_add', 'no_G_add'}
    if wanted_set & calib_variants:
        P_ctr, P_scl = robust_loc_scale(train_raw['P_raw'])
        C_ctr, C_scl = robust_loc_scale(train_raw['C_raw'])
        G_ctr, G_scl = robust_loc_scale(train_raw['G_raw'])
        Pn = _robust_normalize(P_te, P_ctr, P_scl)
        Cn = _robust_normalize(C_te, C_ctr, C_scl)
        Gn = _robust_normalize(G_te, G_ctr, G_scl)
        if 'add_calib' in wanted_set:
            A_map['add_calib'] = Pn + Cn + Gn
        if 'mult_calib' in wanted_set:
            A_map['mult_calib'] = Pn * (Cn + Gn)
        if 'no_P_add' in wanted_set:
            A_map['no_P_add'] = Cn + Gn
        if 'no_C_add' in wanted_set:
            A_map['no_C_add'] = Pn + Gn
        if 'no_G_add' in wanted_set:
            A_map['no_G_add'] = Pn + Cn

    Tt = entity.y.shape[0]
    start = cfg.PICAAD.L - 1

    out = {}
    for name, A in A_map.items():
        A_t = np.full((Tt,), np.nan, dtype=np.float32)
        A_t[start:] = np.asarray(A, dtype=np.float32)
        raw = paper_eval_one(A_t, entity.y, start, cfg.EVAL)
        out[name] = {short: float(raw.get(long_key, float('nan')))
                     for long_key, short in METRIC_KEYS}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cfg', required=True)
    ap.add_argument('--source_dir', required=True)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--entities', default='')
    ap.add_argument('--seeds', default='0,1,2,3')
    ap.add_argument('--fusions', default='add_calib,add_raw,mult_calib')
    a = ap.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'[best_epoch_rescore] device={device}', flush=True)

    cfg = _load_cfg(a.cfg)
    cfg.freeze()

    source_dir = Path(a.source_dir).resolve()
    out_dir = Path(a.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if a.entities.strip():
        entities = [e.strip() for e in a.entities.split(',') if e.strip()]
    else:
        entities = sorted([p.name for p in source_dir.iterdir()
                           if p.is_dir() and (p / 'seed0').exists()])
    seeds = [int(s) for s in a.seeds.split(',') if s.strip()]
    wanted = [f.strip() for f in a.fusions.split(',') if f.strip() in FUSIONS]
    if not wanted:
        raise SystemExit(f'--fusions produced empty subset')

    print(f'[best_epoch_rescore] source={source_dir}', flush=True)
    print(f'[best_epoch_rescore] out={out_dir}', flush=True)
    print(f'[best_epoch_rescore] entities={len(entities)} seeds={seeds} fusions={wanted}', flush=True)

    set_seed(0)

    n_total = len(entities) * len(seeds)
    n_done = 0

    for ent_name in entities:
        try:
            entity = load_entity(cfg, ent_name)
        except Exception as exc:
            print(f'  [skip] entity {ent_name}: {exc}', flush=True)
            continue

        for seed in seeds:
            seed_dir = source_dir / ent_name / f'seed{seed}'
            if not seed_dir.exists():
                n_done += 1
                continue

            best_ep = _find_best_epoch_from_original(source_dir, ent_name, seed)
            if best_ep is None:
                print(f'  [skip] no best-epoch info for {ent_name} seed{seed}', flush=True)
                n_done += 1
                continue

            ckpt_path = seed_dir / 'ckpt' / f'{ent_name}_seed{seed}_ep{best_ep}.pt'
            if not ckpt_path.exists():
                print(f'  [skip] ckpt missing: {ckpt_path.name}', flush=True)
                n_done += 1
                continue

            print(f'  [{n_done+1}/{n_total}] {ent_name} seed{seed} best_ep={best_ep}', flush=True)
            metrics_by_fusion = _rescore_one_checkpoint(cfg, entity, ckpt_path, device,
                                                       wanted, best_ep)

            out_seed_dir = out_dir / ent_name / f'seed{seed}'
            out_seed_dir.mkdir(parents=True, exist_ok=True)
            for name, mtr in metrics_by_fusion.items():
                row = {'epoch': best_ep, 'is_final': 1, **mtr}
                pd.DataFrame([row]).to_csv(
                    out_seed_dir / f'{ent_name}_seed{seed}_best_metrics_{name}.csv',
                    index=False,
                )
            n_done += 1

    print(f'[best_epoch_rescore] done: {n_done}/{n_total}', flush=True)


if __name__ == '__main__':
    main()
