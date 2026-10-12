#!/usr/bin/env python
"""Which statistics of the real PCMCI+ priors the P3 random prior (degree_preserving_v1) keeps exactly.

Reads the cached priors named in one or more verify_p3_plan.py reports (prior_cache_keys), randomizes each one
for every planned seed exactly as training would (model.prior_randomize.prepare_seed_prior), and writes
  <out>.csv   one row per (dataset, entity, seed): exact-preservation flags + change metrics
  <out>.json  summary: per flag, the number of (entity, seed) where it held; ranges of the change metrics
No training, no GPU.

  python scripts/p3_random_prior_report.py --cache_dir <prior cache> --verify <verify_p3_plan.json> [...] --out <prefix>
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
sys.dont_write_bytecode = True

from config import get_cfg_defaults                       # noqa: E402
from model.prior_randomize import prepare_seed_prior      # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache_dir', required=True)
    ap.add_argument('--verify', action='append', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    rows = []
    for vpath in a.verify:
        v = json.load(open(vpath))
        for ent, keys in sorted(v['prior_cache_keys'].items()):
            key = keys[0]
            ds = key.split('_', 1)[0]
            with np.load(os.path.join(a.cache_dir, f'{key}.npz')) as d:
                w, g = d['te_weight'], d['te_gate']
            cfg = get_cfg_defaults()
            cfg.DATA.NAME = ds
            cfg.PICAAD.PRIOR.RANDOMIZE = 'degree_preserving_v1'
            for seed in v['seeds']:
                _, _, info = prepare_seed_prior(cfg, w, g, ent, seed)
                r = info['report']
                row = {'dataset': ds, 'entity': ent, 'seed': seed, 'N': w.shape[1], 'prior_cache_key': key,
                       'cross_edges': sum(p['cross_edges'] for p in info['per_lag']),
                       'slots_with_new_source': sum(p['slots_with_new_source'] for p in info['per_lag']),
                       'random_weight_sha256': info['weight_sha256']}
                row.update({f'exact:{k}': v_ for k, v_ in r['exact'].items()})
                for k, v_ in r['changed'].items():
                    if isinstance(v_, list):
                        row[f'{k}:input'], row[f'{k}:random'] = v_
                    else:
                        row[k] = v_
                rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(a.out + '.csv', index=False)
    flags = [c for c in df.columns if c.startswith('exact:')]
    num = [c for c in df.columns if c not in flags and df[c].dtype.kind in 'fi' and c not in ('seed', 'N')]
    summ = {'n_priors': int(df.groupby(['dataset', 'entity']).ngroups), 'n_randomized': int(len(df)),
            'exact_flags_true_count': {c[6:]: int(df[c].sum()) for c in flags},
            'metrics_range': {c: [float(df[c].min()), float(df[c].median()), float(df[c].max())] for c in num}}
    with open(a.out + '.json', 'w') as f:
        json.dump(summ, f, indent=1)
    print(json.dumps(summ['exact_flags_true_count'], indent=0))
    print(f"{summ['n_randomized']} randomized priors from {summ['n_priors']} cached priors -> {a.out}.csv/.json")


if __name__ == '__main__':
    main()
