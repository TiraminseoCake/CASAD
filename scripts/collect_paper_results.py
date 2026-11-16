"""Collect every result reported in the paper's Experiments section into results/paper_final/.

Read-only on the source runs: each table is rebuilt from the per-run select_best_smooth.csv files (PICAAD), the
shared-evaluator CSVs (CAROTS, OracleAD), and the existing analysis CSVs (score components, folded routing), then
checked against the numbers written in docs/paper/full/experiments_revised.tex.

Usage: python scripts/collect_paper_results.py [--out results/paper_final]
"""
import argparse
import glob
import os
import re
import shutil

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS = ['F1', 'R_F1', 'Aff_F', 'AUC_ROC', 'AUC_PR', 'VUS_ROC', 'VUS_PR']
ORACLEAD = '/home/mschae/oraclead_faithful_v1/runs/floor_ep20/analysis'

PICAAD_FULL = {'PSM': 'results/ablation_hb/PSM/no_prioralign',
               'SMD': 'results/ablation_hb/SMD/no_prioralign',
               'SWaT_ds5': 'results/ablation_hb/SWaT_ds5/no_prioralign'}
PICAAD_ALIGN_ON = {'PSM': 'results/hb/PSM', 'SMD': 'results/hb/SMD', 'SWaT_ds5': 'results/hb/SWaT_ds5'}
ABLATION = [('PICAAD (Full)', PICAAD_FULL['PSM']),
            ('w/o Prior', 'results/ablation_hb/PSM_noalign/no_prior'),
            ('w/o Delta', 'results/ablation_hb/PSM_noalign/no_delta'),
            ('w/o CRS loss', 'results/ablation_hb/PSM_noalign/no_crsloss'),
            ('w/o Intervention', 'results/ablation_hb/PSM_noalign/no_interv'),
            ('w/o CRS update', 'results/ablation_hb/PSM_noalign/no_refupdate'),
            ('w/o L_int', 'results/ablation_hb/PSM_noalign/no_intloss'),
            ('+ prior-alignment loss', PICAAD_ALIGN_ON['PSM'])]


def read_runs(run_root):
    """Per-run best_smooth rows (metrics in %) from <run_root>/<entity>_seed<s>/."""
    rows = []
    for d in sorted(glob.glob(os.path.join(ROOT, run_root, '*_seed[0-9]*'))):
        if not os.path.isdir(d):
            continue
        m = re.fullmatch(r'(.+)_seed(\d+)', os.path.basename(d))
        f = os.path.join(d, f'{m.group(1)}_seed{m.group(2)}_select_best_smooth.csv')
        r = pd.read_csv(f).iloc[-1]
        rows.append({'entity': m.group(1), 'seed': int(m.group(2)), 'epoch': int(r['epoch']),
                     **{k: 100 * float(r[k]) for k in METRICS}, 'source': os.path.relpath(f, ROOT)})
    assert rows, run_root
    return pd.DataFrame(rows)


def per_seed(df):
    """Macro-average over entities per seed (identity for single-entity datasets)."""
    n = df.groupby('seed')['entity'].nunique()
    assert n.nunique() == 1, f'unequal entity count per seed: {n.to_dict()}'
    return df.groupby('seed')[METRICS].mean().reset_index()


def mean_sd(ps):
    return {**{k: ps[k].mean() for k in METRICS}, **{f'{k}_sd': ps[k].std(ddof=1) for k in METRICS}}


def check(label, got, want, tol=0.006):
    assert abs(got - want) < tol, f'{label}: {got:.4f} != paper {want}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'results/paper_final'))
    out = ap.parse_args().out
    for sub in ['tables', 'per_run', 'sources']:
        os.makedirs(os.path.join(out, sub), exist_ok=True)

    # ---- Table 1: dataset statistics -------------------------------------------------------------------------
    stats = []
    for name, files in [('SWaT_ds5', ['data/SWaT_ds5/swat.npz']),
                        ('SMD', sorted(glob.glob(os.path.join(ROOT, 'data/SMD/*.npz')))),
                        ('PSM', ['data/PSM/PSM.npz'])]:
        zs = [np.load(os.path.join(ROOT, f)) for f in files]
        n_anom = sum(int((z['label'] > 0).sum()) for z in zs)
        n_test = sum(z['test'].shape[0] for z in zs)
        stats.append({'dataset': name, 'entities': len(zs), 'vars': zs[0]['train'].shape[1],
                      'train': sum(z['train'].shape[0] for z in zs), 'test': n_test,
                      'anomaly_pct': 100 * n_anom / n_test})
    stats = pd.DataFrame(stats)
    stats.to_csv(os.path.join(out, 'tables/T1_dataset_statistics.csv'), index=False)
    for ds, pct in [('SWaT_ds5', 12.14), ('SMD', 4.16), ('PSM', 27.76)]:
        check(f'T1 {ds} anomaly %', stats.set_index('dataset').loc[ds, 'anomaly_pct'], pct)

    # ---- Table 2: PICAAD / OracleAD / CAROTS -------------------------------------------------------------------
    main_rows, runs_all = [], []
    for ds, root in PICAAD_FULL.items():
        df = read_runs(root).assign(dataset=ds, method='PICAAD')
        runs_all.append(df)
        main_rows.append({'dataset': ds, 'method': 'PICAAD', 'n_seeds': df.seed.nunique(), **mean_sd(per_seed(df))})

    car = pd.read_csv(os.path.join(ROOT, 'results/bench/eval_carots.csv'))
    car.columns = ['entity', 'seed'] + METRICS
    car[METRICS] *= 100
    car['dataset'] = car['entity'].map(lambda e: 'SMD' if e.startswith('machine') else ('SWaT_ds5' if e == 'SWaT' else e))
    for ds, df in car.groupby('dataset'):
        runs_all.append(df.assign(method='CAROTS', source='results/bench/eval_carots.csv'))
        main_rows.append({'dataset': ds, 'method': 'CAROTS', 'n_seeds': df.seed.nunique(), **mean_sd(per_seed(df))})

    oad = pd.read_csv(os.path.join(ORACLEAD, 'per_run.csv')).rename(
        columns=dict(zip(['F1', 'R-F1', 'Aff-F', 'A-ROC', 'A-PR', 'V-ROC', 'V-PR'], METRICS)))
    for ds, df in oad.groupby('dataset'):
        runs_all.append(df[['dataset', 'entity', 'seed'] + METRICS].assign(method='OracleAD', source=f'{ORACLEAD}/per_run.csv'))
        main_rows.append({'dataset': ds, 'method': 'OracleAD', 'n_seeds': df.seed.nunique(), **mean_sd(per_seed(df))})

    t2 = pd.DataFrame(main_rows).sort_values(['dataset', 'method'])
    t2.to_csv(os.path.join(out, 'tables/T2_main_ours_vs_causal.csv'), index=False)
    pd.concat(runs_all, ignore_index=True).to_csv(os.path.join(out, 'per_run/T2_main_per_run.csv'), index=False)
    t2i = t2.set_index(['dataset', 'method'])
    for (ds, me, k, v) in [('PSM', 'PICAAD', 'AUC_PR', 58.22), ('PSM', 'PICAAD', 'VUS_PR', 54.69),
                           ('SMD', 'PICAAD', 'AUC_PR', 43.92), ('SWaT_ds5', 'PICAAD', 'AUC_PR', 74.02),
                           ('PSM', 'CAROTS', 'AUC_PR', 53.17), ('SWaT_ds5', 'CAROTS', 'AUC_PR', 75.90),
                           ('SMD', 'CAROTS', 'AUC_PR', 43.54), ('PSM', 'OracleAD', 'AUC_PR', 55.30),
                           ('SMD', 'OracleAD', 'AUC_PR', 46.49), ('SWaT_ds5', 'OracleAD', 'AUC_PR', 74.65)]:
        check(f'T2 {ds} {me} {k}', t2i.loc[(ds, me), k], v)

    # ---- Table 3: PSM ablation ---------------------------------------------------------------------------------
    full_ps = per_seed(read_runs(PICAAD_FULL['PSM'])).set_index('seed')
    abl_rows, abl_runs = [], []
    for name, root in ABLATION:
        df = read_runs(root)
        abl_runs.append(df.assign(variant=name))
        ps = per_seed(df).set_index('seed')
        d = ps.loc[full_ps.index] - full_ps
        abl_rows.append({'variant': name, **{k: ps[k].mean() for k in METRICS},
                         'dAUC_PR': d['AUC_PR'].mean(), 'dVUS_PR': d['VUS_PR'].mean(),
                         'n_below_full_AUC_PR': int((d['AUC_PR'] < 0).sum()),
                         'n_below_full_VUS_PR': int((d['VUS_PR'] < 0).sum()), 'source_dir': root})
    t3 = pd.DataFrame(abl_rows)
    t3.to_csv(os.path.join(out, 'tables/T3_ablation_psm.csv'), index=False)
    pd.concat(abl_runs, ignore_index=True).to_csv(os.path.join(out, 'per_run/T3_ablation_per_run.csv'), index=False)
    for name, v in [('w/o Prior', -10.79), ('w/o Delta', -12.09), ('w/o CRS loss', -14.11),
                    ('w/o Intervention', -14.08), ('w/o CRS update', -13.90), ('w/o L_int', -3.96),
                    ('+ prior-alignment loss', -4.28)]:
        check(f'T3 {name} dAUC_PR', t3.set_index('variant').loc[name, 'dAUC_PR'], v)

    # ---- Table 4a: prior-alignment loss on/off -----------------------------------------------------------------
    pa_rows, pa_runs = [], []
    for ds in PICAAD_FULL:
        off, on = read_runs(PICAAD_FULL[ds]), read_runs(PICAAD_ALIGN_ON[ds])
        pa_runs += [off.assign(dataset=ds, prior_align='OFF'), on.assign(dataset=ds, prior_align='ON')]
        d = per_seed(on).set_index('seed') - per_seed(off).set_index('seed')
        pa_rows.append({'dataset': ds, 'dAUC_PR_on_minus_off': d['AUC_PR'].mean(),
                        'dVUS_PR_on_minus_off': d['VUS_PR'].mean(), 'n_seeds': len(d),
                        'on_dir': PICAAD_ALIGN_ON[ds], 'off_dir': PICAAD_FULL[ds]})
    t4a = pd.DataFrame(pa_rows)
    t4a.to_csv(os.path.join(out, 'tables/T4a_prior_alignment_onoff.csv'), index=False)
    pd.concat(pa_runs, ignore_index=True).to_csv(os.path.join(out, 'per_run/T4a_prior_alignment_per_run.csv'), index=False)
    for ds, v in [('PSM', -4.28), ('SWaT_ds5', 0.64), ('SMD', 0.12)]:
        check(f'T4a {ds}', t4a.set_index('dataset').loc[ds, 'dAUC_PR_on_minus_off'], v)

    # ---- Table 4b: persistent bias vs folded (PSM, 8 seeds) ----------------------------------------------------
    fold = os.path.join(ROOT, 'results/orig_vs_folded/PSM/analysis_s0to7')
    pc = pd.read_csv(os.path.join(fold, 'paired_comparison.csv'))
    pc.to_csv(os.path.join(out, 'tables/T4b_persistent_vs_folded_psm.csv'), index=False)
    shutil.copy(os.path.join(fold, 'per_seed_metrics.csv'), os.path.join(out, 'per_run/T4b_folded_per_seed.csv'))
    r = pc[(pc.score == 'A') & (pc.metric == 'AUC_PR')].iloc[0]
    check('T4b orig', r.orig_mean, 58.07); check('T4b fold', r.fold_mean, 56.05)
    check('T4b ci_lo', r.ci95_lo, -5.17); check('T4b ci_hi', r.ci95_hi, 1.12)

    # ---- Table 5: score components ------------------------------------------------------------------------------
    sc = os.path.join(ROOT, 'results/score_components')
    t5 = pd.read_csv(os.path.join(sc, 'summary.csv'))
    t5.to_csv(os.path.join(out, 'tables/T5_score_components.csv'), index=False)
    shutil.copy(os.path.join(sc, 'all_runs.csv'), os.path.join(out, 'per_run/T5_score_components_per_run.csv'))
    t5i = t5.set_index(['dataset', 'score'])
    check('T5 PSM C', t5i.loc[('PSM', 'C'), 'AUC_PR'], 34.70)
    check('T5 SWaT C V-ROC', t5i.loc[(t5.dataset[t5.dataset.str.startswith('SWaT')].iloc[0], 'C'), 'VUS_ROC'], 83.51)

    # ---- the LaTeX section itself ------------------------------------------------------------------------------
    shutil.copy(os.path.join(ROOT, 'docs/paper/full/experiments_revised.tex'), os.path.join(out, 'sources/experiments_revised.tex'))
    print('all paper numbers reproduced from source runs; written to', out)


if __name__ == '__main__':
    main()
