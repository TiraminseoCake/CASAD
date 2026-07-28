#!/usr/bin/env python3
"""Aggregate 4-way rescore outputs into per-fusion summary CSVs.

For a rescore run directory (produced by rescore_4way.py), this script:

  * Scans **/{entity}_seed{seed}_epoch_metrics_{fusion}.csv for every fusion
    in {mult_raw, add_calib, add_raw, mult_calib}.
  * For each fusion independently, applies the same best-epoch aggregation
    logic as aggregate_best_epoch.py:
        per entity: best epoch = argmax_e [AUC_PR + AUC_ROC + VUS_PR + VUS_ROC + F1 + Aff_F].mean_over_seeds(e)
        overall  : MACRO_AVG across entities at their respective best epochs.
  * Writes summary_best_epoch_{fusion}.csv and summary_all_epochs_{fusion}.csv
    into the rescore run directory.

Usage:
    python scripts/aggregate_rescored_4way.py --run_dir results/rescored/psm_baseline
"""
import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

FUSIONS = ['mult_raw', 'add_calib', 'add_raw', 'mult_calib']
BEST_METRICS = ['AUC_PR', 'AUC_ROC', 'VUS_PR', 'VUS_ROC', 'F1', 'Aff_F']
ALL_METRICS = ['AUC_PR', 'AUC_ROC', 'F1', 'PA_F1', 'Event_F1',
               'R_F1', 'Aff_F', 'VUS_ROC', 'VUS_PR']


def _parse_entity_seed(csv_stem: str, fusion: str):
    suffix = f'_epoch_metrics_{fusion}'
    if not csv_stem.endswith(suffix):
        return None
    base = csv_stem[: -len(suffix)]
    m = re.match(r'(.+)_seed(\d+)$', base)
    if not m:
        return None
    return m.group(1), int(m.group(2))


def collect(run_dir: Path, fusion: str) -> pd.DataFrame:
    rows = []
    for csv_path in sorted(run_dir.rglob(f'*_epoch_metrics_{fusion}.csv')):
        parsed = _parse_entity_seed(csv_path.stem, fusion)
        if parsed is None:
            continue
        ent, seed = parsed
        df = pd.read_csv(csv_path)
        df['entity'] = ent
        df['seed'] = seed
        rows.append(df)
    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)


def summarize(df: pd.DataFrame, run_dir: Path, fusion: str) -> None:
    missing = [m for m in ALL_METRICS if m not in df.columns]
    if missing:
        print(f'[error] fusion={fusion}: missing metric columns: {missing}', file=sys.stderr)
        return

    grp = df.groupby(['entity', 'epoch'])
    mean_df = grp[ALL_METRICS].mean().reset_index()
    std_df = grp[ALL_METRICS].std().reset_index()

    mean_ren = mean_df.rename(columns={m: f'{m}_mean' for m in ALL_METRICS})
    std_ren = std_df.rename(columns={m: f'{m}_std' for m in ALL_METRICS})
    all_epochs = mean_ren.merge(std_ren, on=['entity', 'epoch'])
    all_epochs = all_epochs.sort_values(['entity', 'epoch']).reset_index(drop=True)
    all_epochs.to_csv(run_dir / f'summary_all_epochs_{fusion}.csv', index=False)

    mean_df['_score'] = mean_df[BEST_METRICS].sum(axis=1)
    best_idx = mean_df.groupby('entity')['_score'].idxmax()
    best_rows = mean_df.loc[best_idx].copy().reset_index(drop=True)
    best_score = best_rows['_score'].copy()
    best_rows = best_rows.drop(columns=['_score'])

    best_rows_std = std_df.merge(best_rows[['entity', 'epoch']], on=['entity', 'epoch'])
    best_combined = best_rows.rename(columns={m: f'{m}_mean' for m in ALL_METRICS}).merge(
        best_rows_std.rename(columns={m: f'{m}_std' for m in ALL_METRICS}),
        on=['entity', 'epoch'],
    )
    best_combined.insert(2, 'selection_score', best_score.values)

    macro = {'entity': 'MACRO_AVG', 'epoch': np.nan, 'selection_score': np.nan}
    for m in ALL_METRICS:
        macro[f'{m}_mean'] = float(best_combined[f'{m}_mean'].mean())
        macro[f'{m}_std']  = float(best_combined[f'{m}_std'].mean())
    macro_row = pd.DataFrame([macro], columns=best_combined.columns)
    best_combined = pd.concat([best_combined, macro_row], ignore_index=True)

    best_combined.to_csv(run_dir / f'summary_best_epoch_{fusion}.csv', index=False)

    print(f'[{fusion}] {len(best_combined) - 1} entities -> summary_best_epoch_{fusion}.csv')
    macro_avg = best_combined.iloc[-1]
    for m in ALL_METRICS:
        print(f'    {m:9s} {macro_avg[f"{m}_mean"]:.4f} +/- {macro_avg[f"{m}_std"]:.4f}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run_dir', required=True)
    a = ap.parse_args()

    run_dir = Path(a.run_dir).resolve()
    if not run_dir.exists():
        print(f'[error] {run_dir} does not exist', file=sys.stderr)
        sys.exit(1)

    for fusion in FUSIONS:
        df = collect(run_dir, fusion)
        if df.empty:
            print(f'[{fusion}] no CSVs found under {run_dir}')
            continue
        summarize(df, run_dir, fusion)


if __name__ == '__main__':
    main()
