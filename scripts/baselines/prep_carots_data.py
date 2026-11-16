"""Convert the PICAAD npz datasets into the file layout the official CAROTS loaders expect,
so all methods train/test on identical arrays.

  PSM : <out>/PSM/{train,test,test_label}.csv            (first column = index, dropped by loader)
  SMD : <out>/ServerMachineDataset/preprocessed/machine-*_{train,test,test_label}.pkl
  SWaT: <out>/SWaT/downsampled_{train,val,test}[_labels]_rate5.npy
        CAROTS protocol: split train 80/20 first, then median-downsample each part by 5
        (cache files are read before the raw xlsx, so the raw loader is bypassed).
"""
import argparse, glob, os, pickle
import numpy as np
import pandas as pd


def downsample(a, r):  # identical to CAROTS datasets/util.py (median over blocks of r)
    n = a.shape[0] // r
    out = np.zeros((n,) + a.shape[1:], dtype=a.dtype)
    for i in range(n):
        out[i] = np.median(a[r * i:r * (i + 1)], axis=0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='/home/mschae/CASAD/data')
    ap.add_argument('--out', default='/home/mschae/external/CAROTS/data')
    ap.add_argument('--train_ratio', type=float, default=0.8)
    args = ap.parse_args()

    d = np.load(os.path.join(args.src, 'PSM', 'PSM.npz'))
    os.makedirs(os.path.join(args.out, 'PSM'), exist_ok=True)
    pd.DataFrame(d['train']).to_csv(os.path.join(args.out, 'PSM', 'train.csv'))
    pd.DataFrame(d['test']).to_csv(os.path.join(args.out, 'PSM', 'test.csv'))
    pd.DataFrame(d['label'].astype(int)).to_csv(os.path.join(args.out, 'PSM', 'test_label.csv'))
    print('PSM', d['train'].shape, d['test'].shape, d['label'].mean())

    smd_out = os.path.join(args.out, 'ServerMachineDataset', 'preprocessed')
    os.makedirs(smd_out, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(args.src, 'SMD', 'machine-*.npz'))):
        m = os.path.splitext(os.path.basename(f))[0]
        d = np.load(f)
        for k, arr in (('train', d['train']), ('test', d['test']), ('test_label', d['label'])):
            with open(os.path.join(smd_out, f'{m}_{k}.pkl'), 'wb') as fh:
                pickle.dump(np.asarray(arr), fh)
    print('SMD', len(glob.glob(os.path.join(smd_out, '*_train.pkl'))), 'entities')

    d = np.load(os.path.join(args.src, 'SWaT', 'swat.npz'))
    tr, te, y = d['train'], d['test'], d['label'].astype(int)
    n = int(len(tr) * args.train_ratio)
    parts = {'train': tr[:n], 'val': tr[n:], 'test': te,
             'train_labels': np.zeros(n, int), 'val_labels': np.zeros(len(tr) - n, int), 'test_labels': y}
    os.makedirs(os.path.join(args.out, 'SWaT'), exist_ok=True)
    for k, arr in parts.items():
        np.save(os.path.join(args.out, 'SWaT', f'downsampled_{k}_rate5.npy'), downsample(arr, 5))
    print('SWaT ds5', {k: downsample(v, 5).shape for k, v in parts.items() if 'labels' not in k},
          'anom', downsample(y, 5).mean())


if __name__ == '__main__':
    main()
