"""Re-evaluate the counterfactual (CF) score on saved checkpoints (no retraining).

CF score (model/scoring.py): for the top-k sources by gate importance, do(X_src = fill),
cut incoming edges to src, and measure the change in prediction error per window.
A normal profile (mean/std per source) is fit on the training portion the model was
trained on; the test CF score is the mean |z| over sources.

Scores evaluated:
  A_raw            P + C (current final score)
  CF               CF alone
  A+CF(g)          P + C + g * CF for g in GAMMAS (what USE_COUNTERFACTUAL=True computes, uncalibrated)
  Z_PC_CF          z(P) + z(C) + z(CF) (train-statistics z-normalization)
All get AUROC / AUPRC / F1; CF and A+CF(1.0) also get the full paper metric set.

Usage:
    python scripts/reeval_cf.py --out results/reeval/cf_swat.csv \
        --run results/swat_final/swat_bs512_seed0:swat:0 [--run ...] [--epoch 100] [--top-k 15]
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.build import load_entity, split_train_val
from model.build import build_model
from model.scoring import (
    cf_anomaly_score,
    counterfactual_score_windows,
    fit_cf_profile,
    score_windows_raw,
)
from utils.evaluation import paper_eval_one
from scripts.reeval_label_mode import load_run_cfg
from scripts.reeval_score_fusion import PAPER_KEYS, quick_metrics

GAMMAS = (0.1, 0.3, 0.5, 1.0)
FULL_METRIC_SCORES = ('CF', 'A+CF(1.0)')


def reeval(run_dir, entity_name, seed, epoch, top_k, device, full_all=False, score_set='a'):
    cfg = load_run_cfg(run_dir)
    payload = torch.load(os.path.join(cfg.TRAIN.CKPT_DIR, f'{entity_name}_seed{seed}_ep{epoch}.pt'),
                         map_location=device, weights_only=False)
    entity = load_entity(cfg, entity_name)
    model = build_model(cfg, N=entity.N).to(device)
    model.load_state_dict(payload['state_dict'])
    model._current_epoch = int(payload['epoch'])  # causal-mask warmup ramp (not in state_dict)
    model.eval()

    train_fit, _ = split_train_val(entity.train_z, getattr(cfg.PICAAD, 'VAL_RATIO', 0.0))
    batch = cfg.TEST.BATCH_SIZE
    with torch.no_grad():
        tr = score_windows_raw(model, train_fit, device, batch, cfg.PICAAD.SCORING)
        te = score_windows_raw(model, entity.test_z, device, batch, cfg.PICAAD.SCORING)
    cf_tr_eff, _ = counterfactual_score_windows(model, train_fit, device, batch, top_k=top_k,
                                                fill_value=cfg.PICAAD.SCORING.CF_FILL_VALUE)
    cf_te_eff, _ = counterfactual_score_windows(model, entity.test_z, device, batch, top_k=top_k,
                                                fill_value=cfg.PICAAD.SCORING.CF_FILL_VALUE)
    profile = fit_cf_profile(cf_tr_eff)
    tr['CF_raw'] = cf_anomaly_score(cf_tr_eff, profile)
    te['CF_raw'] = cf_anomaly_score(cf_te_eff, profile)

    def z(k):
        mu, sd = float(np.mean(tr[k])), float(np.std(tr[k])) + 1e-12
        return (te[k] - mu) / sd

    if score_set == 'p':
        # without C: prediction error + counterfactual only
        P = te['P_raw']
        scores = {'P': P}
        for g in GAMMAS:
            scores[f'P+CF({g})'] = P + g * te['CF_raw']
        scores['Z_P_CF'] = z('P_raw') + z('CF_raw')
    else:
        A = te['P_raw'] + te['C_raw']
        scores = {'A_raw': A, 'CF': te['CF_raw']}
        for g in GAMMAS:
            scores[f'A+CF({g})'] = A + g * te['CF_raw']
        scores['Z_PC_CF'] = z('P_raw') + z('C_raw') + z('CF_raw')

    start = cfg.PICAAD.L - 1
    y = entity.y[start:].astype(int)
    rows = []
    for name, s in scores.items():
        row = {'run': run_dir, 'entity': entity_name, 'seed': seed, 'score': name, 'top_k': top_k}
        row.update(quick_metrics(s.astype(np.float64), y))
        if full_all or name in FULL_METRIC_SCORES:
            s_t = np.full(entity.test_z.shape[0], np.nan, dtype=np.float32)
            s_t[start:] = s
            m = paper_eval_one(s_t, entity.y, start, cfg.EVAL)
            row.update({k: float(m[k]) for k in PAPER_KEYS})
        rows.append(row)
        print(f'[{entity_name} seed{seed} {name:10s}] ' +
              '  '.join(f'{k}={row[k] * 100:.2f}' for k in ('AUROC', 'AUPRC', 'F1')), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='append', required=True, help='RUN_DIR:ENTITY:SEED')
    ap.add_argument('--epoch', type=int, default=100)
    ap.add_argument('--top-k', type=int, default=15)
    ap.add_argument('--full-all', action='store_true', help='full paper metrics (incl. VUS) for every score')
    ap.add_argument('--score-set', choices=('a', 'p'), default='a', help="'a': P+C based, 'p': P+CF without C")
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    rows = []
    for spec in args.run:
        run_dir, ent, seed = spec.rsplit(':', 2)
        rows += reeval(run_dir, ent, int(seed), args.epoch, args.top_k, device, args.full_all, args.score_set)
        pd.DataFrame(rows).to_csv(args.out, index=False)  # checkpoint progress after each run
    print(f'saved: {args.out}', flush=True)


if __name__ == '__main__':
    main()
