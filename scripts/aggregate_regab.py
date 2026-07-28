#!/usr/bin/env python3
"""Regularizer-ablation cross-config comparator.

Given a set of directories each holding a completed regularizer-ablation
run (baseline + no_gate + no_graph + no_lag + no_inv per dataset), this
script:

  1. Ensures each run has summary_best_epoch.csv, invoking
     aggregate_best_epoch.py on any that are missing.
  2. Reads the MACRO_AVG row from each summary_best_epoch.csv.
  3. Emits a wide comparison table (one row per config, one column per
     metric) plus per-metric deltas vs the 'baseline' row.

Usage:
    python scripts/aggregate_regab.py \
        --dataset PSM \
        --run_glob 'results/parallel/psm_regab_*_20260724-*' \
        --out_csv results/regab_summary/psm_regab_compare.csv

The --run_glob is expanded by the shell; quote it so the script sees the
pattern rather than pre-expanded names. Config tag is inferred from the
directory name segment between '<dataset_lower>_regab_' and '_<date>'.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd


METRICS = ['AUC_PR', 'AUC_ROC', 'F1', 'PA_F1', 'Event_F1',
           'R_F1', 'Aff_F', 'VUS_ROC', 'VUS_PR']

CANONICAL_ORDER = ['baseline', 'no_gate', 'no_graph', 'no_lag', 'no_inv']


def _tag_from_dirname(dirname: str, dataset_lower: str, baseline_dirname: str = None) -> str:
    if baseline_dirname and dirname == baseline_dirname:
        return 'baseline'
    m = re.match(rf'{re.escape(dataset_lower)}_regab_(.+?)_\d{{8}}-\d{{6}}$', dirname)
    if not m:
        return dirname
    return m.group(1)


def _ensure_summary(run_dir: Path) -> Path:
    summary = run_dir / 'summary_best_epoch.csv'
    if summary.exists():
        return summary
    repo_root = Path(__file__).resolve().parent.parent
    agg_script = repo_root / 'scripts' / 'aggregate_best_epoch.py'
    print(f'  [aggregate] {run_dir.name}', flush=True)
    subprocess.run(
        [sys.executable, str(agg_script), '--run_dir', str(run_dir)],
        check=True,
    )
    if not summary.exists():
        raise FileNotFoundError(f'Aggregation produced no summary at {summary}')
    return summary


def _read_macro_row(summary_csv: Path) -> dict:
    df = pd.read_csv(summary_csv)
    row = df[df['entity'] == 'MACRO_AVG']
    if row.empty:
        raise ValueError(f'No MACRO_AVG row in {summary_csv}')
    return row.iloc[0].to_dict()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True, help='PSM | SWaT | SMD')
    ap.add_argument('--run_glob', nargs='+', required=True,
                    help='Shell-expanded list of run directories.')
    ap.add_argument('--baseline_dir', default=None,
                    help='Directory to relabel as "baseline" so delta columns compute correctly. '
                         'Use for the pre-existing baseline that does not match the *_regab_* naming.')
    ap.add_argument('--out_csv', required=True)
    args = ap.parse_args()

    dataset_lower = args.dataset.lower()
    baseline_dirname = Path(args.baseline_dir).name if args.baseline_dir else None

    rows = []
    for run_str in args.run_glob:
        run_dir = Path(run_str)
        if not run_dir.is_dir():
            print(f'  [skip] not a directory: {run_dir}', file=sys.stderr)
            continue
        tag = _tag_from_dirname(run_dir.name, dataset_lower, baseline_dirname)
        summary = _ensure_summary(run_dir)
        macro = _read_macro_row(summary)
        row = {'config': tag, 'run_dir': run_dir.name}
        for m in METRICS:
            row[m + '_mean'] = macro.get(m + '_mean', float('nan'))
            row[m + '_std']  = macro.get(m + '_std', float('nan'))
        rows.append(row)

    if not rows:
        print('No valid runs found.', file=sys.stderr)
        sys.exit(1)

    df = pd.DataFrame(rows)
    df['_order'] = df['config'].apply(
        lambda t: CANONICAL_ORDER.index(t) if t in CANONICAL_ORDER else len(CANONICAL_ORDER)
    )
    df = df.sort_values(['_order', 'config']).drop(columns=['_order']).reset_index(drop=True)

    baseline_row = df[df['config'] == 'baseline']
    if not baseline_row.empty:
        base = baseline_row.iloc[0]
        for m in METRICS:
            df[m + '_delta'] = df[m + '_mean'] - base[m + '_mean']

    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f'Wrote {out_path}', flush=True)

    display_cols = ['config'] + [m + '_mean' for m in ['VUS_ROC', 'F1', 'AUC_ROC', 'Aff_F']]
    if 'VUS_ROC_delta' in df.columns:
        display_cols += ['VUS_ROC_delta']
    print()
    print(df[display_cols].to_string(index=False, float_format='%.4f'))


if __name__ == '__main__':
    main()
