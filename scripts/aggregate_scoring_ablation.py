#!/usr/bin/env python3
"""Score-component ablation aggregator.

Reads per-(entity, seed) best_metrics_<fusion>.csv from the scoring-ablation
rescore output and produces a comparison table:

  For each (dataset, fusion), MACRO_AVG(mean-across-seeds) across entities,
  with delta vs the add_calib row.

Usage:
    python scripts/aggregate_scoring_ablation.py \
        --root results/rescored_scoring_ablation \
        --out_csv results/regab_summary/scoring_ablation_table.csv
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DATASETS = ['psm_baseline', 'swat_baseline', 'smd_baseline']
FUSIONS = ['add_calib',                        # reference (baseline)
           'P_only', 'C_only', 'G_only',       # single-component isolation
           'no_P_add', 'no_C_add', 'no_G_add'] # leave-one-out
METRICS = ['AUC_PR', 'AUC_ROC', 'F1', 'PA_F1', 'Event_F1',
           'R_F1', 'Aff_F', 'VUS_ROC', 'VUS_PR']


def _read_entity_seed(dataset_root: Path, fusion: str):
    """Yield (entity, seed, metrics_dict) for every best_metrics_<fusion>.csv
    under dataset_root."""
    for ent_dir in sorted(dataset_root.iterdir()):
        if not ent_dir.is_dir():
            continue
        for seed_dir in sorted(ent_dir.iterdir()):
            if not seed_dir.is_dir() or not seed_dir.name.startswith('seed'):
                continue
            seed = int(seed_dir.name[len('seed'):])
            csv_path = seed_dir / f'{ent_dir.name}_seed{seed}_best_metrics_{fusion}.csv'
            if not csv_path.exists():
                continue
            df = pd.read_csv(csv_path)
            if df.empty:
                continue
            row = df.iloc[0].to_dict()
            yield ent_dir.name, seed, row


def _aggregate_one(dataset_root: Path, fusion: str):
    """Return dict of metric -> (macro_mean, macro_std). MACRO computed as
    mean-across-entities of per-entity seed-mean; std as mean across entities
    of per-entity seed-std."""
    per_ent = {}
    for ent, seed, row in _read_entity_seed(dataset_root, fusion):
        per_ent.setdefault(ent, []).append(row)

    if not per_ent:
        return None

    ent_means = {m: [] for m in METRICS}
    ent_stds  = {m: [] for m in METRICS}
    for ent, rows in per_ent.items():
        dfe = pd.DataFrame(rows)
        for m in METRICS:
            if m in dfe.columns:
                ent_means[m].append(float(dfe[m].mean()))
                ent_stds[m].append(float(dfe[m].std(ddof=0)) if len(dfe) > 1 else 0.0)

    return {m: (float(np.mean(ent_means[m])) if ent_means[m] else float('nan'),
                float(np.mean(ent_stds[m]))  if ent_stds[m]  else float('nan'))
            for m in METRICS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True,
                    help='Root dir containing {psm,swat,smd}_baseline/ subtrees.')
    ap.add_argument('--out_csv', required=True)
    args = ap.parse_args()

    root = Path(args.root)
    rows = []
    for ds in DATASETS:
        ds_root = root / ds
        if not ds_root.is_dir():
            print(f'  [skip] missing dataset dir: {ds_root}')
            continue
        print(f'[{ds}]')
        for fusion in FUSIONS:
            agg = _aggregate_one(ds_root, fusion)
            if agg is None:
                print(f'  [skip] no data for {fusion}')
                continue
            row = {'dataset': ds.replace('_baseline', '').upper(),
                   'fusion': fusion}
            for m in METRICS:
                mean, std = agg[m]
                row[m + '_mean'] = mean
                row[m + '_std']  = std
            rows.append(row)
            print(f'  {fusion:>12}  VUS_ROC={agg["VUS_ROC"][0]:.4f}  F1={agg["F1"][0]:.4f}')

    df = pd.DataFrame(rows)

    for ds in df['dataset'].unique():
        mask = df['dataset'] == ds
        base = df[mask & (df['fusion'] == 'add_calib')]
        if base.empty:
            continue
        base_row = base.iloc[0]
        for m in METRICS:
            df.loc[mask, m + '_delta'] = df.loc[mask, m + '_mean'] - base_row[m + '_mean']

    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f'\nWrote {out_path}')

    disp = df[['dataset', 'fusion',
               'VUS_ROC_mean', 'F1_mean', 'AUC_ROC_mean', 'Aff_F_mean',
               'VUS_ROC_delta']].copy()
    print()
    print(disp.to_string(index=False, float_format='%.4f'))


if __name__ == '__main__':
    main()
