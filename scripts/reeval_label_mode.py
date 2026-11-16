"""Re-evaluate saved checkpoints under point-level and window-level labels.

No retraining: rebuilds the model from the run's config.yaml, loads the
checkpoint state_dict, re-scores the test set and evaluates the final score A
with EVAL.LABEL_MODE = 'point' (ours) and 'window' (CAROTS-style).
The point-level result is checked against the metrics stored in the checkpoint.

Usage:
    python scripts/reeval_label_mode.py --out results/reeval/swat.csv \
        --run results/swat_final/swat_bs512_seed0:swat:0 [--run ...] [--epoch 100]
    (each --run is RUN_DIR:ENTITY:SEED)
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_cfg_defaults
from datasets.build import load_entity
from model.build import build_model
from model.scoring import score_components_to_timeline, score_windows
from utils.evaluation import paper_eval_one

KEYS = ['Standard-F1', 'R-based-F1', 'Affiliation-F', 'AUC-ROC', 'AUC-PR', 'VUS-ROC', 'VUS-PR']
STORED = {'Standard-F1': 'F1', 'AUC-ROC': 'AUC_ROC', 'AUC-PR': 'AUC_PR'}


def load_run_cfg(run_dir):
    cfg = get_cfg_defaults()
    cfg.set_new_allowed(True)
    cfg.merge_from_file(os.path.join(run_dir, 'config.yaml'))
    return cfg


def reeval(run_dir, entity_name, seed, epoch, device):
    cfg = load_run_cfg(run_dir)
    ckpt = os.path.join(cfg.TRAIN.CKPT_DIR, f'{entity_name}_seed{seed}_ep{epoch}.pt')
    payload = torch.load(ckpt, map_location=device, weights_only=False)

    entity = load_entity(cfg, entity_name)
    model = build_model(cfg, N=entity.N).to(device)
    model.load_state_dict(payload['state_dict'])
    # causal-mask warmup ramp reads this plain attribute (not in state_dict); 0 would disable the mask
    model._current_epoch = int(payload['epoch'])
    model.eval()

    with torch.no_grad():
        sc = score_windows(model, entity.test_z, device, batch=cfg.TEST.BATCH_SIZE,
                           scoring_cfg=cfg.PICAAD.SCORING, calibrator=None)
    start = cfg.PICAAD.L - 1
    A_t = score_components_to_timeline({'A': sc['A']}, Tt=entity.test_z.shape[0], start=start)['A_t']

    rows = []
    for mode in ('point', 'window'):
        cfg.defrost()
        cfg.EVAL.LABEL_MODE = mode
        m = paper_eval_one(A_t, entity.y, start, cfg.EVAL)
        row = {'run': run_dir, 'entity': entity_name, 'seed': seed, 'epoch': epoch, 'label_mode': mode}
        row.update({k: float(m[k]) for k in KEYS})
        if mode == 'point':
            # reproduction check vs. metrics logged during training
            row['max_abs_diff_vs_ckpt'] = max(abs(float(m[k]) - float(payload['metrics'][v]))
                                              for k, v in STORED.items())
        rows.append(row)
        print(f'[{entity_name} seed{seed} {mode:6s}] ' +
              '  '.join(f'{k}={row[k] * 100:.2f}' for k in KEYS) +
              (f"  (diff vs ckpt {row['max_abs_diff_vs_ckpt']:.2e})" if mode == 'point' else ''),
              flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='append', required=True, help='RUN_DIR:ENTITY:SEED')
    ap.add_argument('--epoch', type=int, default=100)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    rows = []
    for spec in args.run:
        run_dir, ent, seed = spec.rsplit(':', 2)
        rows += reeval(run_dir, ent, int(seed), args.epoch, device)

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    pd.DataFrame(rows).to_csv(args.out, index=False)
    print(f'saved: {args.out}', flush=True)


if __name__ == '__main__':
    main()
