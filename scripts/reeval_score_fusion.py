"""Re-score saved checkpoints with different score fusions (no retraining).

Scores per window from the final checkpoint:
  P, C, G       raw components (prediction error, causal-structure deviation, graph deviation)
  A_raw = P + C current final score
  Z_PC  = z(P) + z(C)          CAROTS-style: z-normalized with train-score mean/std, then summed
  Z_PCG = z(P) + z(C) + z(G)
Each score gets AUROC, AUPRC (average precision, ours), AUPRC_trap (auc(recall, precision), CAROTS)
and best F1 (point labels). Z_PC additionally gets the full paper metric set.
Train scores use the training portion the model was fit on (first 1 - VAL_RATIO of train).

Usage:
    python scripts/reeval_score_fusion.py --out results/reeval/fusion_swat.csv \
        --run results/swat_final/swat_bs512_seed0:swat:0 [--run ...] [--epoch 100]
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import torch
from sklearn import metrics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.build import load_entity, split_train_val
from model.build import build_model
from model.scoring import score_windows_raw
from utils.evaluation import paper_eval_one
from utils.misc import robust_loc_scale
from scripts.reeval_label_mode import load_run_cfg

FULL_METRIC_SCORES = ('A_raw', 'M_PC', 'M_PCR')
PAPER_KEYS = ['Standard-F1', 'R-based-F1', 'Affiliation-F', 'AUC-ROC', 'AUC-PR', 'VUS-ROC', 'VUS-PR']


def quick_metrics(score, y):
    precision, recall, _ = metrics.precision_recall_curve(y, score)
    f1 = 2 * precision * recall / (precision + recall + 1e-12)
    return {
        'AUROC': metrics.roc_auc_score(y, score),
        'AUPRC': metrics.average_precision_score(y, score),
        'AUPRC_trap': metrics.auc(recall, precision),
        'F1': float(np.max(f1)),
    }


def reeval(run_dir, entity_name, seed, epoch, device):
    cfg = load_run_cfg(run_dir)
    payload = torch.load(os.path.join(cfg.TRAIN.CKPT_DIR, f'{entity_name}_seed{seed}_ep{epoch}.pt'),
                         map_location=device, weights_only=False)
    entity = load_entity(cfg, entity_name)
    model = build_model(cfg, N=entity.N).to(device)
    model.load_state_dict(payload['state_dict'])
    model._current_epoch = int(payload['epoch'])  # causal-mask warmup ramp (not in state_dict)
    model.eval()

    train_fit, _ = split_train_val(entity.train_z, getattr(cfg.PICAAD, 'VAL_RATIO', 0.0))
    with torch.no_grad():
        tr = score_windows_raw(model, train_fit, device, cfg.TEST.BATCH_SIZE, cfg.PICAAD.SCORING)
        te = score_windows_raw(model, entity.test_z, device, cfg.TEST.BATCH_SIZE, cfg.PICAAD.SCORING)

    def z(k):
        mu, sd = float(np.mean(tr[k])), float(np.std(tr[k])) + 1e-12
        return (te[k] - mu) / sd

    def mad(k):
        # paper Eq. 50: ReLU((S - median_train) / MAD_train)
        med, scale = robust_loc_scale(tr[k])
        return np.maximum((te[k] - med) / scale, 0.0)

    scores = {
        'P': te['P_raw'], 'C': te['C_raw'], 'G': te['G_raw'],
        'M_P': mad('P_raw'), 'M_C': mad('C_raw'), 'M_R': mad('G_raw'),
        'M_PC': mad('P_raw') + mad('C_raw'),
        'M_PCR': mad('P_raw') + mad('C_raw') + mad('G_raw'),
        'A_raw': te['P_raw'] + te['C_raw'],
        'Z_PC': z('P_raw') + z('C_raw'),
        'Z_PCG': z('P_raw') + z('C_raw') + z('G_raw'),
    }
    start = cfg.PICAAD.L - 1
    y = entity.y[start:].astype(int)

    rows = []
    for name, s in scores.items():
        row = {'run': run_dir, 'entity': entity_name, 'seed': seed, 'score': name}
        row.update(quick_metrics(s.astype(np.float64), y))
        if name in FULL_METRIC_SCORES:
            s_t = np.full(entity.test_z.shape[0], np.nan, dtype=np.float32)
            s_t[start:] = s
            m = paper_eval_one(s_t, entity.y, start, cfg.EVAL)
            row.update({k: float(m[k]) for k in PAPER_KEYS})
        rows.append(row)
        print(f'[{entity_name} seed{seed} {name:6s}] ' +
              '  '.join(f'{k}={row[k] * 100:.2f}' for k in ('AUROC', 'AUPRC', 'AUPRC_trap', 'F1')), flush=True)
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
