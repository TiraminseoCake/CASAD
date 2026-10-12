#!/usr/bin/env python
"""Verify a P3 launcher plan (queue_dryrun.json) before any training is approved.

Checks, for every planned job of one P3 manifest (docs/p3_structural_ablation_protocol.md section 7):
  * launcher code fingerprint = this checkout's HEAD with no tracked changes
  * job counts: train = arms x entities x seeds, eval = train (best_val only), one prior warm-up per (entity, config)
  * every train job's config resolved exactly as main.py does (utils/parser.load_config with the job's CLI opts):
    prediction-only flags, dataset LR, epochs, VAL, and - within one (dataset, entity, seed) - the four arms differ
    only in PRIOR.TYPE / PRIOR.RANDOMIZE / DYNAMIC_GRAPH
  * config sha256 recorded in the plan identity == the file on disk
  * data NPZ sha256 == the reference (results/data-identity JSON, or --expect_sha for other entities)
  * prior: arms a/r/d resolve to the SAME PCMCI+ cache key and that cache file exists (cache hit, no recomputation);
    arm n has PRIOR.TYPE none (its warm-up job is a no-op)
  * eval jobs: --ckpt_tag best_val --cf off --calibrate off
Writes a JSON report; exit code 0 only if every check passes. No training, no GPU work.

  python scripts/verify_p3_plan.py --queue <out_root>/_launcher/<name>/queue_dryrun.json \
      --ref_hashes <data identity json> [--expect_sha PSM=<sha256>] --out <report.json>
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from unittest import mock

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
sys.dont_write_bytecode = True

ARM_KEYS = {'PICAAD.PRIOR.TYPE', 'PICAAD.PRIOR.RANDOMIZE', 'PICAAD.DYNAMIC_GRAPH'}
RUN_KEYS = {'RESULT_DIR', 'TRAIN.CKPT_DIR', 'SEEDS', 'DATA.ENTITIES'}
LR = {'PSM': 5e-05, 'SMD': 5e-04, 'SWaT': 5e-04}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def flatten(d, p=''):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(flatten(v, f'{p}{k}.'))
        else:
            out[f'{p}{k}'] = json.dumps(v, sort_keys=True, default=str)
    return out


def resolve(cmd):
    """cmd = [python, -u, main.py, --cfg, path, KEY, VAL, ...] -> resolved cfg (as main.py would build it)."""
    from utils.parser import load_config, parse_args
    i = cmd.index('main.py')
    args = list(cmd[i + 1:])
    k = args.index('--cfg')
    if not os.path.isabs(args[k + 1]):          # the launcher runs main.py with cwd=REPO
        args[k + 1] = os.path.join(REPO, args[k + 1])
    with mock.patch.object(sys, 'argv', ['main.py'] + args):
        cfg, _ = load_config(parse_args())
    return cfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--queue', required=True)
    ap.add_argument('--ref_hashes', required=True)
    ap.add_argument('--expect_sha', action='append', default=[], help='ENTITY=sha256 for entities not in --ref_hashes')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    q = json.load(open(a.queue))
    ref = json.load(open(a.ref_hashes))
    ref_sha = {e: v['file_sha256'] for e, v in ref.get('SMD', {}).items()}
    if 'SWaT51' in ref:
        ref_sha['swat'] = ref['SWaT51']['file_sha256']
    ref_sha.update(dict(x.split('=', 1) for x in a.expect_sha))
    fails, notes = [], []

    def fail(msg):
        fails.append(msg)

    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip()
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=REPO).decode().strip()
    if q['code'].get('commit') != head or dirty:
        fail(f"plan code {q['code']} vs checkout HEAD {head} (dirty={bool(dirty)})")
    jobs = q['jobs']
    kinds = Counter(j['kind'] for j in jobs)
    trains = [j for j in jobs if j['kind'] == 'train']
    evals = [j for j in jobs if j['kind'] == 'eval']
    ents = sorted({j['meta']['entity'] for j in trains})
    seeds = sorted({j['meta']['seed'] for j in trains})
    cfgs = sorted({j['meta']['config'] for j in trains})
    if len(trains) != len(ents) * len(seeds) * len(cfgs) or len(cfgs) != 4:
        fail(f'train count {len(trains)} != {len(ents)} entities x {len(seeds)} seeds x {len(cfgs)} configs (expect 4)')
    if len(evals) != len(trains):
        fail(f'eval count {len(evals)} != train count {len(trains)} (best_val only)')
    if kinds['prior'] != len(ents) * len(cfgs):
        fail(f"prior warm-up jobs {kinds['prior']} != entities x configs")
    for j in evals:
        c = j['cmd']
        if c[c.index('--ckpt_tag') + 1] != 'best_val' or c[c.index('--cf') + 1] != 'off' or c[c.index('--calibrate') + 1] != 'off':
            fail(f"{j['id']}: eval must be best_val / cf off / calibrate off")

    from datasets.build import load_entity
    from datasets.split import split_id_for
    from model.build import _prior_cache_key
    groups = defaultdict(dict)
    cache_keys = defaultdict(set)
    data_seen = {}
    for j in trains:
        m = j['meta']
        cfg_path = m['config'] if os.path.isabs(m['config']) else os.path.join(REPO, m['config'])
        if j['identity'].get('config_sha256') != sha256_file(cfg_path):
            fail(f"{j['id']}: config sha256 changed since the plan")
        cfg = resolve(j['cmd'])
        P = cfg.PICAAD
        arm = os.path.basename(m['config']).split('_p3_')[1][0]
        checks = {
            'ENABLE_PRIOR_LOSS': P.ENABLE_PRIOR_LOSS is False, 'START_CLS_EPOCH': P.START_CLS_EPOCH == 99999,
            'PERM_PAIRS': P.INTERVENTION.PERM_PAIRS_PER_BATCH == 0,
            'aux_losses_off': not (P.ENABLE_GATE_LOSS or P.ENABLE_GRAPH_LOSS or P.ENABLE_LAGMONO_LOSS or P.ENABLE_INV_LOSS),
            'CALIBRATE': P.SCORING.CALIBRATE is False, 'USE_COUNTERFACTUAL': P.SCORING.USE_COUNTERFACTUAL is False,
            'MAX_EPOCH': cfg.SOLVER.MAX_EPOCH == 80, 'VAL': cfg.VAL.ENABLE and cfg.VAL.FRAC == 0.2 and cfg.VAL.MIN_DELTA == 0.0,
            'LR': abs(cfg.SOLVER.BASE_LR - LR[cfg.DATA.NAME]) < 1e-12,
            'arm_type': P.PRIOR.TYPE == ('none' if arm == 'n' else 'pcmci'),
            'arm_randomize': P.PRIOR.RANDOMIZE == ('degree_preserving_v1' if arm == 'r' else 'none'),
            'arm_dynamic': P.DYNAMIC_GRAPH == (arm != 'd'),
        }
        for k, ok in checks.items():
            if not ok:
                fail(f"{j['id']}: {k}")
        groups[(cfg.DATA.NAME, m['entity'], m['seed'])][arm] = flatten(yaml_load(cfg.dump()))
        npz = os.path.join(cfg.DATA.INPUT_DIR, f"{m['entity']}.npz")
        if npz not in data_seen:
            data_seen[npz] = sha256_file(npz)
            exp = ref_sha.get(m['entity'])
            if exp is None:
                notes.append(f"{m['entity']}: no reference sha256 supplied (sha256 {data_seen[npz]})")
            elif exp != data_seen[npz]:
                fail(f"{m['entity']}: data sha256 {data_seen[npz]} != reference {exp}")
        if j['identity'].get('data_sha256') != data_seen[npz]:
            fail(f"{j['id']}: plan data sha256 differs from file")
        if arm != 'n' and m['seed'] == seeds[0]:
            e = load_entity(cfg, m['entity'])
            key = _prior_cache_key(cfg, e.train_z, e.name, split_id=split_id_for(cfg, e))
            cache_keys[m['entity']].add(key)
            if not os.path.exists(os.path.join(cfg.PICAAD.PRIOR.CACHE_DIR, f'{key}.npz')):
                fail(f"{m['entity']}: prior cache miss for arm {arm} ({key}) - PCMCI+ would be recomputed")
    for ent, keys in cache_keys.items():
        if len(keys) != 1:
            fail(f'{ent}: arms a/r/d resolve to different prior cache keys {sorted(keys)}')
    for g, arms in groups.items():
        if set(arms) != set('anrd'):
            fail(f'{g}: arms present {sorted(arms)}')
            continue
        keys = set().union(*[set(v) for v in arms.values()]) - RUN_KEYS
        varying = {k for k in keys if len({arms[x].get(k) for x in arms}) > 1}
        if varying != ARM_KEYS:
            fail(f'{g}: keys differing between arms {sorted(varying)} != {sorted(ARM_KEYS)}')
    rep = {'queue': os.path.basename(a.queue), 'plan_name': q['name'], 'code': q['code'], 'checkout_head': head,
           'job_counts': dict(kinds), 'entities': ents, 'seeds': seeds, 'configs': cfgs,
           'n_groups_checked': len(groups), 'data_sha256': {os.path.basename(k): v for k, v in data_seen.items()},
           'prior_cache_keys': {k: sorted(v) for k, v in cache_keys.items()},
           'arm_keys': sorted(ARM_KEYS), 'failures': fails, 'notes': notes, 'ok': not fails}
    with open(a.out, 'w') as f:
        json.dump(rep, f, indent=1)
    print(f"[verify] {q['name']}: jobs={dict(kinds)} entities={len(ents)} seeds={seeds} groups={len(groups)} "
          f"failures={len(fails)} notes={len(notes)} -> {a.out}")
    for x in fails[:20]:
        print('  FAIL', x)
    return 0 if not fails else 1


def yaml_load(s):
    import yaml
    return yaml.safe_load(s)


if __name__ == '__main__':
    sys.exit(main())
