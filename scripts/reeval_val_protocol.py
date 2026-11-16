"""Validation-only evaluation protocol on saved checkpoints (no retraining, no test labels for selection).

Per run:
  1. Checkpoint selection: for every saved epoch checkpoint, compute the validation prediction loss
     (mean |x_L - x_hat_L| over windows of the held-out validation split = last VAL_RATIO of train,
     which is never used for gradient updates). best_val = argmin; last = final epoch.
  2. Thresholding: threshold = q-th percentile of the validation anomaly scores A = P + C.
     F1 / R-F1 / Aff-F are computed from the resulting fixed predictions on the test set.
  3. Threshold-free metrics (AUC-ROC, AUC-PR, VUS-ROC, VUS-PR) are reported for the selected checkpoint.
Point-wise labels; first L-1 test points excluded (as in training-time evaluation).

Usage:
    python scripts/reeval_val_protocol.py --out results/reeval/valproto_psm.csv \
        --run results/parallel/psm_no_earlystop_ep100_20260918_seed0:PSM:0 [--run ...] \
        [--q 95 98 99 99.5 99.9]
"""
import argparse
import glob
import os
import re
import sys

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.build import load_entity, split_train_val
from datasets.util import get_median_anomaly_length
from metrics.paper_eval.basic_metrics import basic_metricor, generate_curve
from model.build import build_model
from model.scoring import score_windows_raw
from scripts.reeval_label_mode import load_run_cfg


def load_model(cfg, entity, ckpt_path, device):
    payload = torch.load(ckpt_path, map_location=device, weights_only=False)
    model = build_model(cfg, N=entity.N).to(device)
    model.load_state_dict(payload['state_dict'])
    model._current_epoch = int(payload['epoch'])  # causal-mask warmup ramp (not in state_dict)
    model.eval()
    return model


def a_score(model, series, cfg, device):
    with torch.no_grad():
        s = score_windows_raw(model, series, device, cfg.TEST.BATCH_SIZE, cfg.PICAAD.SCORING)
    return s['P_raw'] + s['C_raw'], s['P_raw']


def reeval(run_dir, entity_name, seed, qs, device):
    cfg = load_run_cfg(run_dir)
    entity = load_entity(cfg, entity_name)
    _, val = split_train_val(entity.train_z, getattr(cfg.PICAAD, 'VAL_RATIO', 0.0))

    ckpts = {}
    for p in glob.glob(os.path.join(cfg.TRAIN.CKPT_DIR, f'{entity_name}_seed{seed}_ep*.pt')):
        ckpts[int(re.search(r'_ep(\d+)\.pt$', p).group(1))] = p
    epochs = sorted(ckpts)

    # 1) validation prediction loss per checkpoint (P_raw = per-window mean abs error)
    val_loss = {}
    for ep in epochs:
        model = load_model(cfg, entity, ckpts[ep], device)
        _, p_val = a_score(model, val, cfg, device)
        val_loss[ep] = float(np.mean(p_val))
    best_ep = min(val_loss, key=val_loss.get)
    print(f'[{entity_name} seed{seed}] val loss by epoch: ' +
          ' '.join(f'{e}:{val_loss[e]:.4f}' for e in epochs) + f'  -> best {best_ep}', flush=True)

    start = cfg.PICAAD.L - 1
    y = entity.y[start:].astype(int)
    grader = basic_metricor()
    sw = get_median_anomaly_length(y) if cfg.EVAL.USE_MEDIAN_VUS_WINDOW else cfg.EVAL.SLIDING_WINDOW

    rows = []
    for sel, ep in (('best_val', best_ep), ('last', epochs[-1])):
        model = load_model(cfg, entity, ckpts[ep], device)
        a_val, _ = a_score(model, val, cfg, device)
        a_test, _ = a_score(model, entity.test_z, cfg, device)
        a_test = a_test.astype(np.float64)

        base = {'run': run_dir, 'entity': entity_name, 'seed': seed, 'selection': sel,
                'epoch': ep, 'val_loss': val_loss[ep]}
        _, _, _, _, _, _, vus_roc, vus_pr = generate_curve(y, a_test, sw, cfg.EVAL.VUS_VERSION, cfg.EVAL.VUS_THRE)
        base.update({'AUC-ROC': grader.metric_ROC(y, a_test), 'AUC-PR': grader.metric_PR(y, a_test),
                     'VUS-ROC': vus_roc, 'VUS-PR': vus_pr,
                     'oracle-F1': grader.metric_PointF1(y, a_test)})
        for q in qs:
            thr = float(np.percentile(a_val, q))
            pred = (a_test > thr).astype(int)
            row = dict(base, q=q, threshold=thr, pred_ratio=float(pred.mean()),
                       F1=grader.metric_PointF1(y, a_test, preds=pred),
                       **{'R-F1': grader.metric_RF1(y, a_test, preds=pred)})
            try:
                row['Aff-F'] = grader.metric_Affiliation(y, a_test, preds=pred)
            except Exception:
                row['Aff-F'] = float('nan')
            rows.append(row)
        print(f'[{entity_name} seed{seed} {sel} ep{ep}] A-PR={base["AUC-PR"] * 100:.2f} '
              f'V-PR={vus_pr * 100:.2f}  ' +
              '  '.join(f'q{r["q"]}:F1={r["F1"] * 100:.2f}' for r in rows[-len(qs):]), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='append', required=True, help='RUN_DIR:ENTITY:SEED')
    ap.add_argument('--q', type=float, nargs='+', default=[95, 98, 99, 99.5, 99.9])
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    rows = []
    for spec in args.run:
        run_dir, ent, seed = spec.rsplit(':', 2)
        rows += reeval(run_dir, ent, int(seed), args.q, device)
        pd.DataFrame(rows).to_csv(args.out, index=False)
    print(f'saved: {args.out}', flush=True)


if __name__ == '__main__':
    main()
