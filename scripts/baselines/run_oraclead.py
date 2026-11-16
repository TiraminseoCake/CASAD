"""Run the OracleAD base runner (oraclead-repro/src/runners/oraclead_npz_runner.py) under the shared
benchmark protocol, without modifying the original file:

  - same npz data as PICAAD; standardization with training-split statistics (as PICAAD)
  - fixed seed (the original runner sets none)
  - training on the first (1 - val_ratio) of the train series (identical split to PICAAD / CAROTS)
  - native model, hyperparameters (defaults of the original runner), schedule (last epoch) and score A = P * D
  - raw per-timestamp scores A_t, P_t, D_t and labels are saved for evaluation with the shared script

Usage:
    python scripts/baselines/run_oraclead.py --input_dir data/PSM --seed 0 --out_dir results/bench/oraclead/PSM/seed0
"""
import argparse
import glob
import importlib.util
import os
import random

import numpy as np
import torch

RUNNER = '/home/mschae/oraclead_transfer/oraclead-repro/src/runners/oraclead_npz_runner.py'
_spec = importlib.util.spec_from_file_location('oraclead_npz_runner', RUNNER)
oad = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oad)


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input_dir', required=True)
    ap.add_argument('--entities', default='', help='comma list; empty = all npz files')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--val_ratio', type=float, default=0.2)
    ap.add_argument('--out_dir', required=True)
    # original runner defaults
    ap.add_argument('--L', type=int, default=60)
    ap.add_argument('--d', type=int, default=64)
    ap.add_argument('--heads', type=int, default=4)
    ap.add_argument('--dropout', type=float, default=0.0)
    ap.add_argument('--epochs', type=int, default=20)
    ap.add_argument('--batch', type=int, default=256)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--lam_recon', type=float, default=0.1)
    ap.add_argument('--lam_dev', type=float, default=3.0)
    ap.add_argument('--sls_ema', type=float, default=0.9)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if args.entities:
        files = [os.path.join(args.input_dir, f'{e.strip()}.npz') for e in args.entities.split(',') if e.strip()]
    else:
        files = sorted(glob.glob(os.path.join(args.input_dir, '*.npz')))

    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        out = os.path.join(args.out_dir, f'{name}.npz')
        if os.path.exists(out):
            print('[skip]', out)
            continue
        data = np.load(f)
        train = data['train'].astype(np.float32)
        test = data['test'].astype(np.float32)
        y = data['label'].astype(np.int32)
        train_z, test_z, mu, sd = oad.standardize_train_test(train, test)
        n_fit = int(train_z.shape[0] * (1.0 - args.val_ratio))
        train_fit = train_z[:n_fit]

        set_seed(args.seed)
        N = train_z.shape[1]
        print(f'\n=== {name} seed{args.seed} (Tfit={n_fit}, Tte={test_z.shape[0]}, N={N}) ===', flush=True)
        model = oad.OracleAD(N=N, L=args.L, d=args.d, heads=args.heads, dropout=args.dropout).to(device)
        oad.train_2d(model, train_fit, device, args.epochs, args.batch, args.lr,
                     args.lam_recon, args.lam_dev, args.sls_ema)
        P_w, D_w, A_w = oad.score_2d(model, test_z, device, batch=args.batch)

        Tt = test_z.shape[0]
        start = args.L - 1
        tl = {}
        for k, w in (('A_t', A_w), ('P_t', P_w), ('D_t', D_w)):
            arr = np.full((Tt,), np.nan, dtype=np.float32)
            arr[start:] = w.astype(np.float32)
            tl[k] = arr
        np.savez(out, y=y, start=start, **tl)
        print(f'  saved {out}  AUC-PR={oad.auc_pr(y, tl["A_t"]):.4f}', flush=True)


if __name__ == '__main__':
    main()
