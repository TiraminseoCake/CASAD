#!/usr/bin/env python
"""SMD 28-entity CRS x PERM 2x2 analysis on best_val checkpoints (trainer B, 49f630a).

Input : smd28_runs.csv written by collect_smd28.py (built from per-run files only), and optionally the js PSM 2x2
        package metrics.csv (results/cfval_abl_psmcrs/server8) as a separate reference.
Output: smd28_crs_perm_paired.csv, smd28_entity_effects.csv, smd28_uncertainty.csv, analysis_summary.json

Definitions (fixed before the 28-entity numbers were computed; same formulas as the handoff brief):
  a00 = PERM0/CRS off, a01 = PERM0/CRS on, a10 = PERM2/CRS off, a11 = PERM2/CRS on   (per entity, seed)
  crs_at_perm0 = a01 - a00          crs_at_perm2 = a11 - a10
  interaction  = crs_at_perm2 - crs_at_perm0
  crs_main     = (crs_at_perm0 + crs_at_perm2) / 2
  perm_main    = ((a10 - a00) + (a11 - a01)) / 2
Primary: variant P_raw, AUC-PR. Others are auxiliary and descriptive.

Uncertainty: entities are clusters. Each entity keeps its 4 seeds and its 4 arms together (paired cluster bootstrap):
B replicates draw n_entities entities with replacement and average every (seed, arm) row of the drawn entities.
With 4 seeds per entity this equals the mean of the drawn entity means. Percentile 95% CI.
Secondary: one-sample t on the entity means (df = n_entities - 1). Reference: one-sample t on the 4 seed-level
macro means (df = 3; treats the entity set as fixed). The 112 (entity, seed) pairs are never treated as independent.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ARM_CODE = {'smd_cf_val_perm0_crsoff': 'a00', 'smd_cf_val_perm0_crson': 'a01',
            'smd_cf_val_perm2_crsoff': 'a10', 'smd_cf_val_perm2_crson': 'a11'}
PSM_ARM_CODE = {'psm_cf_val_perm0_crsoff': 'a00', 'psm_cf_val_perm0_crson': 'a01',
                'psm_cf_val_perm2_crsoff': 'a10', 'psm_cf_val_perm2_crson': 'a11'}
METRICS = ['AUC-PR', 'AUC-ROC', 'VUS-PR', 'VUS-ROC', 'Standard-F1', 'Affiliation-F', 'R-based-F1', 'Event-based-F1',
           'PA-F1', 'best_val_MAE']
METRIC_NOTE = {'AUC-PR': 'primary', 'PA-F1': 'point-adjusted; not reliable, listed only for completeness',
               'best_val_MAE': 'validation prediction MAE of the selected checkpoint; lower is better',
               'VUS-PR': 'entity-specific median VUS window', 'VUS-ROC': 'entity-specific median VUS window'}
ARMS = ['a00', 'a01', 'a10', 'a11']
EFFECTS = ['crs_at_perm0', 'crs_at_perm2', 'interaction', 'crs_main', 'perm_main']
QUANTITIES = ARMS + EFFECTS


def add_effects(w: pd.DataFrame) -> pd.DataFrame:
    w = w.copy()
    w['crs_at_perm0'] = w['a01'] - w['a00']
    w['crs_at_perm2'] = w['a11'] - w['a10']
    w['interaction'] = w['crs_at_perm2'] - w['crs_at_perm0']
    w['crs_main'] = (w['crs_at_perm0'] + w['crs_at_perm2']) / 2.0
    w['perm_main'] = ((w['a10'] - w['a00']) + (w['a11'] - w['a01'])) / 2.0
    return w


def subset_of(entity: str) -> str:
    return 'ks8_machine-1' if entity.startswith('machine-1-') else 'js20_machine-2_3'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs_csv', required=True)
    ap.add_argument('--psm_metrics', default=None)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--boot', type=int, default=10000)
    ap.add_argument('--boot_seed', type=int, default=20261012)
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    runs = pd.read_csv(a.runs_csv)
    runs['arm_code'] = runs['arm'].map(ARM_CODE)
    assert runs['arm_code'].notna().all()
    assert len(runs) == 448 and not runs.duplicated(['entity', 'seed', 'arm']).any()

    # ---- paired (entity, seed) table, P_raw variant ----
    long = []
    for m in METRICS:
        col = 'ckpt_val_mae' if m == 'best_val_MAE' else f'P_raw|{m}'
        w = runs.pivot_table(index=['entity', 'seed'], columns='arm_code', values=col, aggfunc='first')[ARMS]
        w = add_effects(w).reset_index()
        w.insert(2, 'metric', m)
        w.insert(3, 'variant', 'P_raw' if m != 'best_val_MAE' else 'checkpoint')
        long.append(w)
    paired = pd.concat(long, ignore_index=True)
    ep = runs.pivot_table(index=['entity', 'seed'], columns='arm_code', values='ckpt_epoch', aggfunc='first')[ARMS]
    ep.columns = [f'best_epoch_{c}' for c in ep.columns]
    paired = paired.merge(ep.reset_index(), on=['entity', 'seed'])
    paired.insert(0, 'subset', paired['entity'].map(subset_of))
    camp = runs.groupby('entity')['campaign'].first()
    paired.insert(1, 'campaign', paired['entity'].map(camp))
    paired['metric_note'] = paired['metric'].map(METRIC_NOTE).fillna('auxiliary')
    ent_order = sorted(paired['entity'].unique(), key=lambda e: tuple(int(x) for x in e.split('-')[1:]))
    paired['_o'] = paired['entity'].map({e: i for i, e in enumerate(ent_order)})
    paired = paired.sort_values(['metric', '_o', 'seed'], key=lambda s: s.map({m: i for i, m in enumerate(METRICS)})
                                if s.name == 'metric' else s).drop(columns='_o').reset_index(drop=True)
    paired.to_csv(out / 'smd28_crs_perm_paired.csv', index=False, float_format='%.10g')

    # ---- entity-level 4-seed mean / sd ----
    g = paired.groupby(['metric', 'entity'], sort=False)
    ent = g[QUANTITIES].mean().add_suffix('_mean').join(g[QUANTITIES].std(ddof=1).add_suffix('_sd'))
    ent['n_seeds'] = g.size()
    for q in ['interaction', 'crs_at_perm2', 'crs_at_perm0']:
        ent[f'{q}_n_seed_pos'] = g[q].apply(lambda s: int((s > 0).sum()))
        ent[f'{q}_n_seed_neg'] = g[q].apply(lambda s: int((s < 0).sum()))
    ent = ent.reset_index()
    ent.insert(1, 'subset', ent['entity'].map(subset_of))
    ent.to_csv(out / 'smd28_entity_effects.csv', index=False, float_format='%.10g')

    # ---- uncertainty per scope ----
    scopes = {'SMD28': ent_order,
              'SMD8_ks_subset(reference)': [e for e in ent_order if e.startswith('machine-1-')],
              'SMD20_js_subset(reference)': [e for e in ent_order if not e.startswith('machine-1-')]}
    urows = []
    for si, (scope, ents) in enumerate(scopes.items()):
        rng = np.random.default_rng(a.boot_seed)             # same draws for every metric / quantity of a scope
        idx = rng.integers(0, len(ents), size=(a.boot, len(ents)))
        for m in METRICS:
            sub = paired[(paired['metric'] == m) & paired['entity'].isin(ents)]
            assert sub.groupby('entity').size().eq(4).all() and sub['entity'].nunique() == len(ents)
            emeans = sub.groupby('entity')[QUANTITIES].mean().loc[ents]
            smac = sub.groupby('seed')[QUANTITIES].mean()            # 4 seed-level macro means over the entities
            for q in QUANTITIES:
                e = emeans[q].to_numpy()
                boot = e[idx].mean(axis=1)
                sm = smac[q].to_numpy()
                r = {'scope': scope, 'metric': m, 'quantity': q, 'n_entities': len(ents), 'n_seeds_per_entity': 4,
                     'estimate': float(e.mean()),
                     **{f'seed{s}_macro': float(smac.loc[s, q]) for s in smac.index},
                     'seed_macro_mean': float(sm.mean()), 'seed_macro_sd_ddof1': float(sm.std(ddof=1)),
                     'entity_sd_ddof1': float(e.std(ddof=1)),
                     'entity_min': float(e.min()), 'entity_q25': float(np.quantile(e, 0.25)),
                     'entity_median': float(np.median(e)), 'entity_q75': float(np.quantile(e, 0.75)),
                     'entity_max': float(e.max()),
                     'n_entity_pos': int((e > 0).sum()), 'n_entity_neg': int((e < 0).sum()),
                     'n_entity_zero': int((e == 0).sum()),
                     'boot_B': a.boot, 'boot_seed': a.boot_seed, 'boot_unit': 'entity (4 seeds x 4 arms kept together)',
                     'boot_se': float(boot.std(ddof=1)),
                     'boot_ci95_lo': float(np.quantile(boot, 0.025)), 'boot_ci95_hi': float(np.quantile(boot, 0.975)),
                     'boot_frac_gt0': float((boot > 0).mean()),
                     't_entity_df': len(ents) - 1,
                     't_entity_p': float(stats.ttest_1samp(e, 0.0).pvalue) if q in EFFECTS else np.nan,
                     't_seedmacro_df': 3,
                     't_seedmacro_p': float(stats.ttest_1samp(sm, 0.0).pvalue) if q in EFFECTS else np.nan,
                     'metric_note': METRIC_NOTE.get(m, 'auxiliary')}
                urows.append(r)

    # ---- PSM reference (js server8 package; single entity -> seeds only, no entity bootstrap) ----
    psm_summary = None
    if a.psm_metrics:
        pm = pd.read_csv(a.psm_metrics)
        pm = pm[(pm['ckpt_tag'] == 'best_val') & (pm['variant'] == 'P_raw')].copy()
        pm['arm_code'] = pm['config'].map(lambda c: PSM_ARM_CODE[Path(c).stem])
        assert set(pm['training_code_sha']) == {'49f630ac8d324ba01390c1a1dcaa4386cd94ae84'}
        assert set(pm['result_kind']) == {'val_ckpt_eval'} and len(pm) == 16
        psm_summary = {}
        for m in METRICS:
            col = 'ckpt_val_mae' if m == 'best_val_MAE' else m
            w = add_effects(pm.pivot_table(index='seed', columns='arm_code', values=col, aggfunc='first')[ARMS])
            for q in QUANTITIES:
                s = w[q].to_numpy()
                urows.append({'scope': 'PSM_js_server8(reference)', 'metric': m, 'quantity': q, 'n_entities': 1,
                              'n_seeds_per_entity': 4, 'estimate': float(s.mean()),
                              **{f'seed{k}_macro': float(w.loc[k, q]) for k in w.index},
                              'seed_macro_mean': float(s.mean()), 'seed_macro_sd_ddof1': float(s.std(ddof=1)),
                              'n_entity_pos': int(s.mean() > 0), 'n_entity_neg': int(s.mean() < 0),
                              'boot_B': 0, 'boot_unit': 'n/a (single entity)',
                              't_seedmacro_df': 3,
                              't_seedmacro_p': float(stats.ttest_1samp(s, 0.0).pvalue) if q in EFFECTS else np.nan,
                              'seed_n_pos': int((s > 0).sum()), 'seed_n_neg': int((s < 0).sum()),
                              'metric_note': METRIC_NOTE.get(m, 'auxiliary')})
            if m == 'AUC-PR':
                psm_summary = {q: {'per_seed': [float(x) for x in w[q]], 'mean': float(w[q].mean()),
                                   'sd': float(w[q].std(ddof=1))} for q in QUANTITIES}
    unc = pd.DataFrame(urows)
    unc.to_csv(out / 'smd28_uncertainty.csv', index=False, float_format='%.10g')

    # ---- compact summary for the report ----
    def pick(scope, metric, q):
        r = unc[(unc.scope == scope) & (unc.metric == metric) & (unc.quantity == q)].iloc[0]
        return {k: (None if (isinstance(v, float) and np.isnan(v)) else v) for k, v in r.items()}
    summ = {'boot': {'B': a.boot, 'seed': a.boot_seed},
            'primary': {s: {q: pick(s, 'AUC-PR', q) for q in QUANTITIES} for s in scopes},
            'aux': {m: {q: pick('SMD28', m, q) for q in EFFECTS} for m in METRICS if m != 'AUC-PR'},
            'psm_auc_pr': psm_summary}
    ip = paired[paired['metric'] == 'AUC-PR']
    cons = ip.groupby('entity')['interaction'].agg(lambda s: 'all+' if (s > 0).all() else ('all-' if (s < 0).all()
                                                                                           else 'mixed'))
    summ['interaction_seed_consistency_entities'] = cons.value_counts().to_dict()
    c2 = ip.groupby('entity')['crs_at_perm2'].agg(lambda s: 'all+' if (s > 0).all() else ('all-' if (s < 0).all()
                                                                                          else 'mixed'))
    summ['crs_at_perm2_seed_consistency_entities'] = c2.value_counts().to_dict()
    summ['pairs_pos_interaction'] = int((ip['interaction'] > 0).sum())
    summ['pairs_pos_crs_at_perm2'] = int((ip['crs_at_perm2'] > 0).sum())
    json.dump(summ, open(out / 'analysis_summary.json', 'w'), indent=1, default=float)
    p = summ['primary']['SMD28']
    for q in QUANTITIES:
        r = p[q]
        print(f"SMD28 {q:13s} est={r['estimate']:+.4f} seedmacro={r['seed_macro_mean']:+.4f}+-{r['seed_macro_sd_ddof1']:.4f} "
              f"CI=[{r['boot_ci95_lo']:+.4f},{r['boot_ci95_hi']:+.4f}] pos/neg={r['n_entity_pos']}/{r['n_entity_neg']} "
              f"t_ent_p={r['t_entity_p']} t_seed_p={r['t_seedmacro_p']}")


if __name__ == '__main__':
    main()
