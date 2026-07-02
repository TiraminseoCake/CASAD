#!/usr/bin/env python3
"""Best-epoch summary aggregator.

Walks {run_dir}/**/{entity}_seed{seed}_epoch_metrics.csv, computes:

  - Per (entity, epoch): mean and std of 9 metrics across seeds
  - Per entity: best epoch = argmax over epochs of the 4-seed-mean of
      (AUC_PR + AUC_ROC + VUS_PR + VUS_ROC + F1 + Aff_F)
  - Overall MACRO_AVG row (mean across entities at their respective best epochs)

Outputs (written into --run_dir):
  summary_all_epochs.csv   all (entity, epoch) rows with _mean and _std cols
  summary_best_epoch.csv   one row per entity at its best epoch + MACRO_AVG row

Usage:
    python scripts/aggregate_best_epoch.py --run_dir results/parallel/smd_20260701-1234
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


# Metrics used for best-epoch selection (per user spec).
# Sum of 4-seed means across these must be maximum.
BEST_METRICS = ['AUC_PR', 'AUC_ROC', 'VUS_PR', 'VUS_ROC', 'F1', 'Aff_F']

# All 9 metrics tracked in epoch_metrics.csv.
ALL_METRICS = ['AUC_PR', 'AUC_ROC', 'F1', 'PA_F1', 'Event_F1',
                'R_F1', 'Aff_F', 'VUS_ROC', 'VUS_PR']


def _parse_entity_seed(csv_stem: str):
    """From 'machine-1-1_seed0_epoch_metrics' return ('machine-1-1', 0)."""
    base = csv_stem.replace('_epoch_metrics', '')
    if '_seed' not in base:
        return None
    ent, seed_str = base.rsplit('_seed', 1)
    try:
        return ent, int(seed_str)
    except ValueError:
        return None


def collect(run_dir: Path) -> pd.DataFrame:
    rows = []
    for csv_path in sorted(run_dir.rglob('*_epoch_metrics.csv')):
        parsed = _parse_entity_seed(csv_path.stem)
        if parsed is None:
            print(f'[skip] cannot parse: {csv_path}', file=sys.stderr)
            continue
        ent, seed = parsed
        df = pd.read_csv(csv_path)
        df['entity'] = ent
        df['seed'] = seed
        rows.append(df)
    if not rows:
        print(f'[error] no *_epoch_metrics.csv found under {run_dir}', file=sys.stderr)
        sys.exit(1)
    return pd.concat(rows, ignore_index=True)


def summarize(df: pd.DataFrame, run_dir: Path) -> None:
    # Verify expected columns
    missing = [m for m in ALL_METRICS if m not in df.columns]
    if missing:
        print(f'[error] missing metric columns: {missing}', file=sys.stderr)
        sys.exit(1)

    grp = df.groupby(['entity', 'epoch'])
    mean_df = grp[ALL_METRICS].mean().reset_index()
    std_df = grp[ALL_METRICS].std().reset_index()

    # summary_all_epochs.csv: per (entity, epoch) mean and std
    mean_ren = mean_df.rename(columns={m: f'{m}_mean' for m in ALL_METRICS})
    std_ren = std_df.rename(columns={m: f'{m}_std' for m in ALL_METRICS})
    all_epochs = mean_ren.merge(std_ren, on=['entity', 'epoch'])
    all_epochs = all_epochs.sort_values(['entity', 'epoch']).reset_index(drop=True)
    all_epochs.to_csv(run_dir / 'summary_all_epochs.csv', index=False)

    # Best epoch selection: sum of BEST_METRICS on mean_df
    mean_df['_score'] = mean_df[BEST_METRICS].sum(axis=1)
    best_idx = mean_df.groupby('entity')['_score'].idxmax()
    best_rows = mean_df.loc[best_idx].copy().reset_index(drop=True)
    best_score = best_rows['_score'].copy()
    best_rows = best_rows.drop(columns=['_score'])

    # Attach std at the same best (entity, epoch)
    best_rows_std = std_df.merge(best_rows[['entity', 'epoch']], on=['entity', 'epoch'])
    best_combined = best_rows.rename(columns={m: f'{m}_mean' for m in ALL_METRICS}).merge(
        best_rows_std.rename(columns={m: f'{m}_std' for m in ALL_METRICS}),
        on=['entity', 'epoch'],
    )
    best_combined.insert(2, 'selection_score', best_score.values)

    # MACRO_AVG row: mean across entities of best-epoch mean-metrics
    macro = {'entity': 'MACRO_AVG', 'epoch': np.nan, 'selection_score': np.nan}
    for m in ALL_METRICS:
        macro[f'{m}_mean'] = best_combined[f'{m}_mean'].mean()
        macro[f'{m}_std'] = best_combined[f'{m}_std'].mean()
    best_combined = pd.concat([best_combined, pd.DataFrame([macro])], ignore_index=True)
    best_combined.to_csv(run_dir / 'summary_best_epoch.csv', index=False)

    # Console output
    print(f'Saved: {run_dir / "summary_all_epochs.csv"} '
          f'({len(all_epochs)} rows over {all_epochs["entity"].nunique()} entities)')
    print(f'Saved: {run_dir / "summary_best_epoch.csv"} '
          f'({len(best_combined) - 1} entities + 1 MACRO_AVG)')
    print()
    print(f'Best epoch per entity (score = sum of {BEST_METRICS}):')
    for _, r in best_combined.iloc[:-1].iterrows():
        parts = [f'{m}={r[f"{m}_mean"]:.4f}' for m in BEST_METRICS]
        print(f'  {r["entity"]:20s} ep={int(r["epoch"]):3d}  score={r["selection_score"]:.4f}  ' +
              '  '.join(parts))
    print()
    print(f'MACRO_AVG across {len(best_combined) - 1} entities (at their best epochs):')
    macro_row = best_combined.iloc[-1]
    for m in ALL_METRICS:
        print(f'  {m:10s} {macro_row[f"{m}_mean"]:.4f} +/- {macro_row[f"{m}_std"]:.4f}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run_dir', required=True)
    a = ap.parse_args()
    run_dir = Path(a.run_dir).resolve()
    if not run_dir.is_dir():
        print(f'[error] not a directory: {run_dir}', file=sys.stderr)
        sys.exit(1)
    df = collect(run_dir)
    summarize(df, run_dir)


if __name__ == '__main__':
    main()
