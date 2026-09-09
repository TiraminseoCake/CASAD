"""Eval-only script: load existing checkpoint, run counterfactual scoring.

Usage:
    python scripts/eval_cf.py \
        --cfg scripts/configs/psm.yaml \
        --ckpt-dir results/parallel/psm_paper_align_20260901/PSM/seed0/ckpt \
        --seed 0 \
        --gamma 1.0 \
        --cf-top-k 15
"""
import argparse
import os
import sys
import glob

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.build import list_entities, load_entity
from model.build import apply_prior_to_model, build_causal_prior_cached, build_model
from model.scoring import (
    counterfactual_score_windows,
    fit_cf_profile,
    fit_score_calibrator,
    score_components_to_timeline,
    score_windows,
)
from utils.evaluation import paper_eval_one
from utils.misc import pct, set_seed
from utils.parser import load_config


def find_best_ckpt(ckpt_dir):
    pts = sorted(glob.glob(os.path.join(ckpt_dir, '*.pt')))
    if not pts:
        raise FileNotFoundError(f'No checkpoints in {ckpt_dir}')
    return pts[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', required=True)
    parser.add_argument('--ckpt-dir', required=True)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--gamma', type=float, default=1.0)
    parser.add_argument('--cf-top-k', type=int, default=15)
    parser.add_argument('--cf-fill', type=float, default=0.0)
    parser.add_argument('--entity', type=str, default='')
    args = parser.parse_args()

    class FakeArgs:
        cfg_file = args.cfg
        opts = []
    cfg, _ = load_config(FakeArgs())

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    seed = args.seed
    set_seed(seed)

    entities = list_entities(cfg)
    if args.entity:
        entities = [args.entity]

    for name in entities:
        entity = load_entity(cfg, name)
        te_weight_np, te_gate_np = build_causal_prior_cached(cfg, entity.train_z, entity.name)

        model = build_model(cfg, N=entity.N).to(device)
        apply_prior_to_model(cfg, model, te_weight_np, te_gate_np)

        ckpt_path = find_best_ckpt(args.ckpt_dir)
        state = torch.load(ckpt_path, map_location=device, weights_only=False)
        model.load_state_dict(state['state_dict'])
        model.eval()
        print(f'Loaded {ckpt_path}', flush=True)

        scoring_cfg = cfg.PICAAD.SCORING

        # --- Baseline (P + C) ---
        raw_base = score_windows(model, entity.test_z, device,
                                 batch=cfg.TEST.BATCH_SIZE,
                                 scoring_cfg=scoring_cfg)
        Tt = entity.test_z.shape[0]
        start = cfg.PICAAD.L - 1
        tl_base = score_components_to_timeline(
            {k: raw_base[k] for k in ['P', 'C', 'G', 'S', 'A']}, Tt=Tt, start=start)
        mtr_base = paper_eval_one(tl_base['A_t'], entity.y, start, cfg.EVAL)

        # --- Counterfactual (P + C + gamma * CF) ---
        print(f'[seed {seed}] computing counterfactual profile (train) ...', flush=True)
        train_cf, _ = counterfactual_score_windows(
            model, entity.train_z, device, batch=cfg.TRAIN.BATCH_SIZE,
            top_k=args.cf_top_k, fill_value=args.cf_fill)
        cf_profile = fit_cf_profile(train_cf)

        print(f'[seed {seed}] computing counterfactual scores (test) ...', flush=True)
        test_cf, src_idx = counterfactual_score_windows(
            model, entity.test_z, device, batch=cfg.TEST.BATCH_SIZE,
            top_k=args.cf_top_k, fill_value=args.cf_fill)
        from model.scoring import cf_anomaly_score
        CF_raw = cf_anomaly_score(test_cf, cf_profile)

        P = raw_base['P'].astype(np.float32)
        C = raw_base['C'].astype(np.float32)
        CF = CF_raw.astype(np.float32)

        for gamma in [0.0, 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
            A_cf = P + C + gamma * CF
            tl_cf = score_components_to_timeline({'A': A_cf}, Tt=Tt, start=start)
            mtr_cf = paper_eval_one(tl_cf['A_t'], entity.y, start, cfg.EVAL)

            tag = 'baseline' if gamma == 0.0 else f'gamma={gamma}'
            print(
                f'[{name} seed {seed}] {tag:12s}  '
                f"F1={pct(mtr_cf['Standard-F1']):.2f}  "
                f"R-F1={pct(mtr_cf['R-based-F1']):.2f}  "
                f"Aff-F={pct(mtr_cf['Affiliation-F']):.2f}  "
                f"A-ROC={pct(mtr_cf['AUC-ROC']):.2f}  "
                f"A-PR={pct(mtr_cf['AUC-PR']):.2f}  "
                f"V-ROC={pct(mtr_cf['VUS-ROC']):.2f}  "
                f"V-PR={pct(mtr_cf['VUS-PR']):.2f}",
                flush=True,
            )


if __name__ == '__main__':
    main()
