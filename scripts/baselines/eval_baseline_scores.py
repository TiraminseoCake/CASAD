"""Evaluate raw baseline anomaly scores with the same metric script as PICAAD.

Inputs per run:
  oraclead : <dir>/<entity>.npz with A_t (per-timestamp, NaN before start), y, start
  carots   : <result_dir>/test_scores.npy (one score per sliding window, window w covers [w, w+W)),
             labels taken from the shared npz (PSM/SMD) or the 5x-downsampled SWaT labels (CAROTS protocol)
Each window score is assigned to its last time step (t = w + W - 1), matching PICAAD.
Metrics: point-wise labels, threshold-dependent metrics with best threshold (current shared protocol).

Usage:
    python scripts/baselines/eval_baseline_scores.py --method oraclead --runs 'results/bench/oraclead/SMD/seed*' --out ...
    python scripts/baselines/eval_baseline_scores.py --method carots --runs '/home/mschae/external/CAROTS/bench/seed*' --out ...
"""
import argparse
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import get_cfg_defaults
from utils.evaluation import paper_eval_one

KEYS = ['Standard-F1', 'R-based-F1', 'Affiliation-F', 'AUC-ROC', 'AUC-PR', 'VUS-ROC', 'VUS-PR']
DATA = '/home/mschae/CASAD/data'
CAROTS_DATA = '/home/mschae/external/CAROTS/data'


def eval_cfg():
    cfg = get_cfg_defaults()
    cfg.EVAL.USE_MEDIAN_VUS_WINDOW = True  # same as PICAAD runs
    return cfg.EVAL


def carots_labels(dataset):
    if dataset == 'SWaT':
        return np.load(os.path.join(CAROTS_DATA, 'SWaT', 'downsampled_test_labels_rate5.npy')).astype(int)
    if dataset == 'PSM':
        return np.load(os.path.join(DATA, 'PSM', 'PSM.npz'))['label'].astype(int)
    m = re.match(r'SMD_(\d+-\d+)', dataset)
    return np.load(os.path.join(DATA, 'SMD', f'machine-{m.group(1)}.npz'))['label'].astype(int)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--method', choices=('oraclead', 'carots'), required=True)
    ap.add_argument('--runs', required=True, help='glob of seed directories')
    ap.add_argument('--win', type=int, default=10, help='CAROTS window size')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    ev = eval_cfg()

    rows = []
    for seed_dir in sorted(glob.glob(args.runs)):
        seed = int(re.search(r'seed(\d+)', seed_dir).group(1))
        if args.method == 'oraclead':
            for f in sorted(glob.glob(os.path.join(seed_dir, '*.npz'))):
                if 'A_t' not in np.load(f).files:
                    continue
                d = np.load(f)
                start = int(d['start']) if 'start' in d.files else args.win - 1
                m = paper_eval_one(d['A_t'], d['y'], start, ev)
                ent = re.sub(r'_seed\d+$', '', os.path.splitext(os.path.basename(f))[0])
                rows.append(dict(entity=ent, seed=seed,
                                 **{k: float(m[k]) for k in KEYS}))
        else:
            for f in sorted(glob.glob(os.path.join(seed_dir, '*', 'test_scores.npy'))):
                dataset = os.path.basename(os.path.dirname(f))
                y = carots_labels(dataset)
                s = np.load(f).astype(np.float64)
                start = args.win - 1
                assert len(s) == len(y) - start, (dataset, len(s), len(y))
                s_t = np.full(len(y), np.nan)
                s_t[start:] = s
                m = paper_eval_one(s_t, y, start, ev)
                ent = dataset if not dataset.startswith('SMD_') else 'machine-' + dataset[4:]
                rows.append(dict(entity=ent, seed=seed, **{k: float(m[k]) for k in KEYS}))
        print(f'{seed_dir}: {len(rows)} rows so far', flush=True)

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    pd.DataFrame(rows).to_csv(args.out, index=False)
    print(f'saved: {args.out}')


if __name__ == '__main__':
    main()
