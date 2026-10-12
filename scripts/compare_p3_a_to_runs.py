#!/usr/bin/env python
"""Does P3 arm A train under the same protocol as existing prediction-only runs (e.g. ks cfval_abl_noalign)?

For every P3 arm-A train job in a launcher plan (queue_dryrun.json) that has a finished reference run with the same
(dataset, entity, seed) under --ref_out_root, compare
  * the resolved training config (A resolved exactly as main.py would; reference = the run's own config.yaml),
    reporting every differing key and classifying it
      run-identity : output locations
      equivalent   : START_CLS_EPOCH values that both exceed MAX_EPOCH (CRS loss never active)
      eval-only    : PICAAD.SCORING.* (read only by scoring/evaluation, never by the trainer)
      new-default  : keys added by this branch, present only in A, at their default value
      OTHER        : anything else (must be empty)
  * data sha256, split id and PCMCI+ prior cache key (reference eval provenance vs A plan)
  * that the reference run was itself prediction-only (val_metrics: causal/graphreg/robust/cstruct/perm all 0)
No training. Writes a JSON report; exit 0 only if no OTHER difference and all identities match.

  python scripts/compare_p3_a_to_runs.py --queue <p3 queue_dryrun.json> --ref_out_root <noalign out_root> --out <json>
"""
import argparse
import glob
import json
import os
import sys
from unittest import mock

import pandas as pd
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
sys.dont_write_bytecode = True

from config import get_cfg_defaults        # noqa: E402

RUN_KEYS = {'RESULT_DIR', 'TRAIN.CKPT_DIR'}
NEW_KEYS = {'PICAAD.PRIOR.RANDOMIZE', 'PICAAD.PRIOR.RANDOMIZE_SALT', 'PICAAD.PRIOR.RANDOMIZE_SWAPS',
            'PICAAD.USE_DYNAMIC_DELTA'}


def flatten(d, p=''):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(flatten(v, f'{p}{k}.'))
        else:
            out[f'{p}{k}'] = v
    return out


def resolve(cmd):
    from utils.parser import load_config, parse_args
    args = list(cmd[cmd.index('main.py') + 1:])
    k = args.index('--cfg')
    if not os.path.isabs(args[k + 1]):
        args[k + 1] = os.path.join(REPO, args[k + 1])
    with mock.patch.object(sys, 'argv', ['main.py'] + args):
        cfg, _ = load_config(parse_args())
    return cfg


def classify(key, a, r, a_flat, val_both):
    if key in RUN_KEYS:
        return 'run-identity'
    if key == 'PICAAD.START_CLS_EPOCH' and a is not None and r is not None:
        me = a_flat['SOLVER.MAX_EPOCH']
        return 'equivalent' if (a > me and r > me) else 'OTHER'
    if key.startswith('PICAAD.SCORING.'):
        # under VAL.ENABLE the trainer never scores (test-set epoch eval raises), so SCORING is eval-only
        return 'eval-only' if val_both else 'OTHER'
    if key in NEW_KEYS and r is None:
        default = flatten(yaml.safe_load(get_cfg_defaults().dump()))[key]
        return 'new-default' if a == default else 'OTHER'
    return 'OTHER'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--queue', required=True)
    ap.add_argument('--ref_out_root', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    trainer_src = open(os.path.join(REPO, 'trainer.py')).read()
    if 'SCORING' in trainer_src:
        raise SystemExit('trainer.py reads PICAAD.SCORING; the eval-only classification would be wrong')
    q = json.load(open(a.queue))
    ref_jobs = {}
    for qp in glob.glob(os.path.join(a.ref_out_root, '_launcher', '*', 'queue.json')):
        for j in json.load(open(qp))['jobs']:
            if j['kind'] == 'train' and j['status'] == 'success':
                ref_jobs[(j['meta']['dataset'], j['meta']['entity'], int(j['meta']['seed']))] = j
    evals = {}
    for qp in glob.glob(os.path.join(a.ref_out_root, '_launcher', '*', 'queue.json')):
        for j in json.load(open(qp))['jobs']:
            if j['kind'] == 'eval' and j['status'] == 'success' and j['meta'].get('ckpt_tag') == 'best_val':
                evals[j['meta']['train_job']] = j
    rows, other, mism = [], [], []
    for j in q['jobs']:
        if j['kind'] != 'train' or '_p3_a.' not in j['meta']['config']:
            continue
        m = j['meta']
        key = (m['dataset'], m['entity'], int(m['seed']))
        rj = ref_jobs.get(key)
        if rj is None:
            continue
        cfg_a = resolve(j['cmd'])
        fa = flatten(yaml.safe_load(cfg_a.dump()))
        fr = flatten(yaml.safe_load(open(os.path.join(rj['job_dir'], 'config.yaml'))))
        diffs = {}
        for k in sorted(set(fa) | set(fr)):
            va, vr = fa.get(k), fr.get(k)
            if va != vr:
                c = classify(k, va, vr, fa, bool(fa.get('VAL.ENABLE')) and bool(fr.get('VAL.ENABLE')))
                diffs[k] = {'p3_a': va, 'reference': vr, 'class': c}
                if c == 'OTHER':
                    other.append(f'{key}: {k} {va!r} vs {vr!r}')
        ident = {'data_sha256_equal': j['identity']['data_sha256'] == rj['identity']['data_sha256']}
        ev = evals.get(rj['id'])
        prov = json.load(open(os.path.join(ev['job_dir'], 'provenance.json'))) if ev else None
        if prov:
            from datasets.build import load_entity
            from datasets.split import split_id_for
            from model.build import _prior_cache_key
            e = load_entity(cfg_a, m['entity'])
            sid = split_id_for(cfg_a, e)
            ident.update({'split_id_equal': sid == prov['data']['split_id'],
                          'prior_cache_key_equal': _prior_cache_key(cfg_a, e.train_z, e.name, split_id=sid)
                          == prov['checkpoint']['prior_cache_key']})
        vm = pd.read_csv(glob.glob(os.path.join(rj['job_dir'], '*_val_metrics.csv'))[0])
        ident['reference_prediction_only'] = bool(
            all(float(vm[c].abs().max()) == 0.0 for c in ('group_causal', 'group_graphreg', 'group_robust', 'cstruct', 'perm'))
            and (vm['loss_total'] - vm['group_task']).abs().max() < 1e-12)
        for k_, ok in ident.items():
            if not ok:
                mism.append(f'{key}: {k_}')
        rows.append({'key': list(key), 'reference_job': rj['id'], 'reference_code': rj['identity']['code']['commit'],
                     'diffs': diffs, **ident})
    classes = {}
    for r in rows:
        for k, d in r['diffs'].items():
            classes.setdefault(k, set()).add(d['class'])
    rep = {'p3_plan': q['name'], 'p3_code': q['code'], 'ref_out_root': os.path.basename(os.path.dirname(a.ref_out_root.rstrip('/'))),
           'n_compared': len(rows), 'differing_keys': {k: sorted(v) for k, v in sorted(classes.items())},
           'other_differences': other, 'identity_mismatches': mism, 'ok': bool(rows) and not other and not mism,
           'runs': rows}
    with open(a.out, 'w') as f:
        json.dump(rep, f, indent=1, default=str)
    print(f"[compare] {q['name']} vs {rep['ref_out_root']}: compared={len(rows)} other={len(other)} "
          f"identity_mismatch={len(mism)} keys={rep['differing_keys']}")
    return 0 if rep['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
