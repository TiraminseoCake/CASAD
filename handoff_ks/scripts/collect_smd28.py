#!/usr/bin/env python
"""Collect the SMD 28-entity CRS x PERM 2x2 results (trainer B) from the per-run launcher outputs.

Reads only per-run files: queue.json, train SUCCESS.json / config.yaml / <entity>_seed<k>_val_metrics.csv /
launcher_run.log / best_val checkpoint, and best_val eval SUCCESS.json / provenance.json / metrics.csv.
No aggregated CSV (eval_summary_*.csv, *_best_val_metrics.csv) is read.

Writes into --out_dir:
  smd28_runs.csv            one row per (entity, seed, arm): integrity fields + every metric of every variant
  smd28_checks.json         integrity check results (counts, failures, invariants)

Usage (paths are machine specific, pass them explicitly):
  python collect_smd28.py --runs_root <RUNS> --data_root <DATA_ROOT> --ref_hashes <data identity json> \
      --exec_repo <execution checkout at 49f630a> --out_dir <dir>
"""
import argparse
import hashlib
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

CODE_SHA = '49f630ac8d324ba01390c1a1dcaa4386cd94ae84'
EMPTY_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
CAMPAIGNS = [('cfval_abl_smdcrs', 'cfval_abl_smdcrs_ks'), ('cfval_abl_smdcrs20', 'cfval_abl_smdcrs20_ks')]
ARMS = {  # config stem -> (PERM_PAIRS_PER_BATCH, CRS loss on)
    'smd_cf_val_perm0_crsoff': (0, 0), 'smd_cf_val_perm0_crson': (0, 1),
    'smd_cf_val_perm2_crsoff': (2, 0), 'smd_cf_val_perm2_crson': (2, 1),
}
VARIANTS = ['P_raw', 'C_raw', 'G_raw', 'CF_raw', 'A_off', 'A_on']
METRICS = ['AUC-PR', 'AUC-ROC', 'VUS-PR', 'VUS-ROC', 'Standard-F1', 'PA-F1', 'Event-based-F1', 'R-based-F1',
           'Affiliation-F']
# keys that legitimately differ per run (identity / output location), excluded from the config-diff check
RUN_KEYS = {'RESULT_DIR', 'RESULT_DIR_LITERAL', 'SEEDS', 'DATA.ENTITIES', 'TRAIN.CKPT_DIR'}
EP_RE = re.compile(r'^\s*\[ep (\d+)\] .*?\brobust=([-0-9.eE+]+).*?\bcstruct=([-0-9.eE+]+).*?\bperm=([-0-9.eE+]+)'
                   r'.*?\buse_cstruct=(True|False)')


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def flatten(d, prefix=''):
    out = {}
    for k, v in d.items():
        key = f'{prefix}{k}'
        if isinstance(v, dict):
            out.update(flatten(v, key + '.'))
        else:
            out[key] = json.dumps(v, sort_keys=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs_root', required=True)
    ap.add_argument('--data_root', required=True)
    ap.add_argument('--ref_hashes', required=True)
    ap.add_argument('--exec_repo', required=True)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--skip_ckpt', action='store_true', help='skip checkpoint hashing / cls_ref check (fast mode)')
    a = ap.parse_args()

    sys.dont_write_bytecode = True                    # never write __pycache__ into the execution checkout
    sys.path.insert(0, a.exec_repo)
    import torch
    torch.set_num_threads(4)
    from layers.ops import normalize_causal_tensor_torch

    runs_root, out_dir = Path(a.runs_root), Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ref = json.load(open(a.ref_hashes))['SMD']
    failures = []

    def fail(key, msg):
        failures.append({'key': key, 'check': msg})

    # ---- data identity: file on disk vs reference record ----
    data_sha = {}
    for ent, r in sorted(ref.items()):
        p = Path(a.data_root) / 'SMD' / f'{ent}.npz'
        data_sha[ent] = sha256_file(p)
        if data_sha[ent] != r['file_sha256']:
            fail(ent, 'data npz sha256 != reference')

    rows, queue_info, duplicates, orphan_dirs = [], {}, [], []
    cfg_flat = {}
    for camp, qname in CAMPAIGNS:
        out_root = runs_root / camp / 'ks'
        q = json.load(open(out_root / '_launcher' / qname / 'queue.json'))
        if q['code'] != {'commit': CODE_SHA, 'tracked_diff_sha256': EMPTY_SHA256}:
            fail(camp, f"queue code {q['code']}")
        jobs = q['jobs']
        queue_info[camp] = {'queue_name': q['name'], 'stopped': q.get('stopped'), 'updated_at': q.get('updated_at'),
                            'code': q['code'], 'job_counts': dict(Counter(f"{j['kind']}:{j['status']}" for j in jobs))}
        ids = [j['id'] for j in jobs]
        for k, n in Counter(ids).items():
            if n > 1:
                duplicates.append({'campaign': camp, 'job_id': k, 'count': n})
        evals = {(j['meta']['train_job'], j['meta']['ckpt_tag']): j for j in jobs if j['kind'] == 'eval'}
        seen_dirs = set()
        for j in (j for j in jobs if j['kind'] == 'train'):
            m = j['meta']
            arm = Path(m['config']).stem
            ent, seed = m['entity'], int(m['seed'])
            key = f'{camp}|{ent}|seed{seed}|{arm}'
            perm, crs = ARMS[arm]
            r = {'campaign': camp, 'entity': ent, 'seed': seed, 'arm': arm, 'perm_pairs': perm, 'crs_on': crs}
            # -- train job --
            r['train_status'] = j['status']
            r['train_exit'] = j['exit_code']
            jd = Path(j['job_dir'])
            seen_dirs.add(jd)
            logical = jd.parent
            att = sorted(p.name for p in logical.glob('attempt*') if p.is_dir())
            r['train_attempt'] = jd.name
            r['train_attempts_on_disk'] = len(att)
            if len(att) != 1:
                duplicates.append({'campaign': camp, 'logical_dir': str(logical.relative_to(runs_root)), 'attempts': att})
            succ = json.load(open(jd / 'SUCCESS.json'))
            ident = succ['identity']
            if succ['job_id'] != j['id'] or succ['exit_code'] != 0:
                fail(key, 'train SUCCESS.json job_id/exit mismatch')
            if ident['code'] != {'commit': CODE_SHA, 'tracked_diff_sha256': EMPTY_SHA256}:
                fail(key, 'train identity code')
            if ident['entity'] != ent or int(ident['seed']) != seed or not ident['val_enabled']:
                fail(key, 'train identity entity/seed/val_enabled')
            r['config_sha256'] = ident['config_sha256']
            if ident['config_sha256'] != sha256_file(Path(m['config'])):
                fail(key, 'config file changed since run (sha256)')
            r['data_sha256_identity'] = ident['data_sha256']
            if ident['data_sha256'] != ref[ent]['file_sha256']:
                fail(key, 'train identity data sha256 != reference')
            # resolved training config
            cfg = yaml.safe_load(open(jd / 'config.yaml'))
            fl = flatten(cfg)
            cfg_flat[key] = fl
            P = cfg['PICAAD']
            r['cfg_PERM_PAIRS'] = P['INTERVENTION']['PERM_PAIRS_PER_BATCH']
            r['cfg_START_CLS_EPOCH'] = P['START_CLS_EPOCH']
            r['cfg_MAX_EPOCH'] = cfg['SOLVER']['MAX_EPOCH']
            r['cfg_BASE_LR'] = cfg['SOLVER']['BASE_LR']
            r['cfg_VAL_FRAC'] = cfg['VAL']['FRAC']
            r['cfg_VAL_ENABLE'] = cfg['VAL']['ENABLE']
            r['cfg_PRIOR_TYPE'] = P['PRIOR']['TYPE']
            r['cfg_CALIBRATE'] = P['SCORING']['CALIBRATE']
            if (r['cfg_PERM_PAIRS'], int(r['cfg_START_CLS_EPOCH'] <= r['cfg_MAX_EPOCH'])) != (perm, crs):
                fail(key, 'resolved config PERM/START_CLS_EPOCH do not match arm name')
            # training log: active terms per epoch
            ep_rows = []
            with open(jd / 'launcher_run.log', errors='replace') as f:
                for line in f:
                    mm = EP_RE.match(line)
                    if mm:
                        ep_rows.append((int(mm.group(1)), float(mm.group(2)), float(mm.group(3)), float(mm.group(4)),
                                        mm.group(5) == 'True'))
            eps = [e[0] for e in ep_rows]
            r['log_epochs'] = len(ep_rows)
            r['log_use_cstruct_true'] = sum(e[4] for e in ep_rows)
            r['log_first_cstruct_epoch'] = min((e[0] for e in ep_rows if e[4]), default=-1)
            r['log_perm_nonzero_epochs'] = sum(e[3] != 0.0 for e in ep_rows)
            r['log_perm_min'] = min((e[3] for e in ep_rows), default=float('nan'))
            r['log_cstruct_nonzero_epochs'] = sum(e[2] != 0.0 for e in ep_rows)
            if eps != list(range(1, 81)):
                fail(key, f'log epochs not 1..80 ({len(eps)})')
            exp_cs = 76 if crs else 0
            if r['log_use_cstruct_true'] != exp_cs or (crs and r['log_first_cstruct_epoch'] != 5):
                fail(key, f"use_cstruct=True count {r['log_use_cstruct_true']} (expected {exp_cs})")
            if perm == 0 and r['log_perm_nonzero_epochs'] != 0:
                fail(key, 'PERM=0 but perm loss nonzero in log')
            if perm == 2 and r['log_perm_nonzero_epochs'] != 80:
                fail(key, f"PERM=2 but perm loss nonzero only {r['log_perm_nonzero_epochs']}/80 epochs")
            # validation curve and best_val selection
            vm = pd.read_csv(jd / f'{ent}_seed{seed}_val_metrics.csv')
            r['val_epochs'] = len(vm)
            r['val_all_finite'] = bool(np.isfinite(vm['val_pred_mae']).all() and (vm['val_is_finite'] == 1).all())
            i_min = int(vm['val_pred_mae'].values.argmin())          # first minimum, same tie rule as MIN_DELTA=0
            r['val_argmin_epoch'] = int(vm['epoch'].iloc[i_min])
            r['val_min_mae'] = float(vm['val_pred_mae'].iloc[i_min])
            r['val_final_best_epoch'] = int(vm['best_epoch_so_far'].iloc[-1])
            if r['val_epochs'] != 80 or not r['val_all_finite']:
                fail(key, 'val curve not 80 finite epochs')
            # -- best_val eval job --
            ej = evals.get((j['id'], 'best_val'))
            if ej is None:
                fail(key, 'no best_val eval job in queue')
                rows.append(r)
                continue
            r['eval_status'] = ej['status']
            ed = Path(ej['job_dir'])
            seen_dirs.add(ed)
            eatt = sorted(p.name for p in ed.parent.glob('attempt*') if p.is_dir())
            r['eval_attempts_on_disk'] = len(eatt)
            if len(eatt) != 1:
                duplicates.append({'campaign': camp, 'logical_dir': str(ed.parent.relative_to(runs_root)), 'attempts': eatt})
            es = json.load(open(ed / 'SUCCESS.json'))
            if es['job_id'] != ej['id'] or es['exit_code'] != 0 or es['identity']['ckpt_tag'] != 'best_val':
                fail(key, 'eval SUCCESS.json mismatch')
            if es['identity']['train_identity'] != ident:
                fail(key, 'eval train_identity != train SUCCESS identity')
            if es['identity']['code'] != {'commit': CODE_SHA, 'tracked_diff_sha256': EMPTY_SHA256}:
                fail(key, 'eval identity code')
            pv = json.load(open(ed / 'provenance.json'))
            ck = pv['checkpoint']
            r['ckpt_sha256'] = ck['sha256']
            r['ckpt_format'] = ck['format']
            r['ckpt_protocol'] = ck['protocol']
            r['ckpt_epoch'] = ck['payload_epoch']
            r['ckpt_val_mae'] = ck['val_mae']
            si = ck['split_info']
            r['split_id'] = si['split_id']
            r['fit_protocol'] = si['fit_protocol']
            r['val_frac'] = si['val_frac']
            r['val_boundary'] = si['val_boundary']
            r['T_train_sub'], r['T_val'], r['T_test'] = si['T_train_sub'], si['T_val'], si['T_test']
            r['prior_cache_key'] = ck['prior_cache_key']
            r['eval_npz_sha256'] = pv['data']['npz_sha256']
            r['eval_stats_maxdiff'] = max(pv['data']['stats_check']['max_abs_mu_diff'],
                                          pv['data']['stats_check']['max_abs_sd_diff'])
            r['state_unchanged'] = pv['state_unchanged']
            r['calibrate'] = pv['scoring']['calibrate']
            r['gamma'] = pv['scoring']['gamma']
            ev = pv['evaluator']
            r['vus_window'] = ev['sliding_window_used']
            r['evaluator_sig'] = json.dumps({k: ev[k] for k in ('USE_MEDIAN_VUS_WINDOW', 'VUS_VERSION', 'VUS_THRE',
                                                                 'start_idx')}, sort_keys=True)
            r['cf_top_k'] = pv['cf']['top_k']
            r['eval_elapsed_s'] = pv['elapsed_s']
            ckpt_path = Path(ck['path'])
            if ckpt_path != jd / 'ckpt' / f'{ent}_seed{seed}_best_val.pt':
                fail(key, 'eval checkpoint path is not this train job best_val.pt')
            if ck['format'] != 'val' or ck['protocol'] != 'val_pred_mae_v2' or ck['entity'] != ent or ck['seed'] != seed:
                fail(key, 'checkpoint format/protocol/entity/seed')
            if ck['code_fingerprint_in_ckpt']['commit'] != CODE_SHA or ck['code_fingerprint_in_ckpt']['dirty']:
                fail(key, 'checkpoint code fingerprint')
            if pv['code_fingerprint']['commit'] != CODE_SHA or pv['code_fingerprint']['modified_tracked']:
                fail(key, 'eval code fingerprint')
            if ck['data_fingerprint_in_ckpt']['file_sha256'] != ref[ent]['file_sha256'] or \
                    pv['data']['npz_sha256'] != ref[ent]['file_sha256']:
                fail(key, 'data sha256 in ckpt/eval != reference')
            T_tr = ref[ent]['train']['shape'][0]
            if not (si['val_enabled'] and si['val_frac'] == 0.2 and si['val_boundary'] == max(1, min(T_tr - 1, int(round(T_tr * (1.0 - 0.2)))))
                    and si['T_train_sub'] == si['val_boundary'] and si['T_train_sub'] + si['T_val'] == T_tr
                    and si['fit_protocol'] == 'train_sub_val_v2' and si['split_id'] == f"val0.2_b{si['val_boundary']}"
                    and pv['data']['fit_rows'] == si['T_train_sub'] and pv['data']['fit_protocol'] == 'train_sub_val'):
                fail(key, 'split is not the 80/20 chronological train_sub protocol')
            if f"val0.2_b{si['val_boundary']}" not in ck['prior_cache_key'] or '_pcmci_' not in ck['prior_cache_key']:
                fail(key, 'prior cache key is not the train_sub PCMCI+ key')
            if r['eval_stats_maxdiff'] != 0.0:
                fail(key, 'mu/sd in checkpoint differ from train_sub statistics')
            if not pv['state_unchanged'] or pv['restore']['strict_load'] is not True or \
                    pv['restore']['set_te_prior_called_after_load']:
                fail(key, 'eval restore/state check')
            if pv['scoring']['calibrate'] is not False or pv['scoring']['gamma'] != 1.0 or \
                    pv['scoring']['P_AGG'] != 'mean' or pv['scoring']['C_AGG'] != 'fro':
                fail(key, 'scoring settings')
            if ck['payload_epoch'] != r['val_argmin_epoch'] or ck['payload_epoch'] != r['val_final_best_epoch'] or \
                    abs(ck['val_mae'] - r['val_min_mae']) > 1e-9:
                fail(key, 'best_val checkpoint is not the validation-MAE argmin epoch')
            # metrics
            mt = pd.read_csv(ed / 'metrics.csv')
            if sorted(mt['variant']) != sorted(VARIANTS) or (mt['entity'] != ent).any() or (mt['seed'] != seed).any() \
                    or (mt['ckpt_format'] != 'val').any() or (mt['epoch'] != ck['payload_epoch']).any():
                fail(key, 'metrics.csv rows (variants/entity/seed/epoch)')
            vals = mt.set_index('variant')[METRICS]
            r['n_nonfinite_metrics'] = int((~np.isfinite(vals.values.astype(float))).sum())
            if r['n_nonfinite_metrics']:
                fail(key, f"{r['n_nonfinite_metrics']} non-finite metric values")
            for v in VARIANTS:
                for mname in METRICS:
                    r[f'{v}|{mname}'] = float(vals.loc[v, mname])
            r['P_formula'] = mt.set_index('variant').loc['P_raw', 'formula'] if 'formula' in mt else ''
            # checkpoint: sha256 and cls_ref vs normalize(te_prior_weight)
            if not a.skip_ckpt:
                raw = ckpt_path.read_bytes()
                r['ckpt_sha256_ondisk_match'] = hashlib.sha256(raw).hexdigest() == ck['sha256']
                if not r['ckpt_sha256_ondisk_match']:
                    fail(key, 'checkpoint file sha256 != provenance')
                pl = torch.load(io.BytesIO(raw), map_location='cpu', weights_only=False)
                sd = pl['state_dict']
                dev = (sd['cls_ref'] - normalize_causal_tensor_torch(sd['te_prior_weight'])).abs().max().item()
                r['cls_ref_dev_from_prior'] = dev
                pc = yaml.safe_load(pl['cfg'])
                if pc['PICAAD']['INTERVENTION']['PERM_PAIRS_PER_BATCH'] != perm or \
                        pc['PICAAD']['START_CLS_EPOCH'] != P['START_CLS_EPOCH'] or pl['epoch'] != ck['payload_epoch']:
                    fail(key, 'checkpoint cfg/epoch differ from resolved config / provenance')
                if (perm == 0 and dev > 1e-5) or (perm == 2 and dev < 0.1):
                    fail(key, f'cls_ref deviation {dev:.3g} inconsistent with PERM={perm}')
                del pl, sd, raw
            rows.append(r)
        # result dirs on disk that the queue does not reference
        for p in (out_root / 'SMD').glob('*/seed*/*/attempt*'):
            if p.is_dir() and p not in seen_dirs:
                orphan_dirs.append(str(p.relative_to(runs_root)))
        for p in (out_root / 'SMD').glob('*/seed*/*/eval/best_val/attempt*'):
            if p.is_dir() and p not in seen_dirs:
                orphan_dirs.append(str(p.relative_to(runs_root)))

    df = pd.DataFrame(rows).sort_values(['entity', 'seed', 'arm']).reset_index(drop=True)

    # ---- resolved-config diff: keys whose value varies across all runs, excluding per-run identity keys ----
    all_keys = set().union(*[set(f) for f in cfg_flat.values()])
    varying = sorted(k for k in all_keys - RUN_KEYS if len({f.get(k) for f in cfg_flat.values()}) > 1)
    if varying != ['PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH', 'PICAAD.START_CLS_EPOCH']:
        fail('config-diff', f'unexpected varying keys {varying}')
    within_entity_window = df.groupby('entity')['vus_window'].nunique()
    if (within_entity_window != 1).any():
        fail('evaluator', 'VUS window differs within an entity')
    if df['evaluator_sig'].nunique() != 1:
        fail('evaluator', 'evaluator settings differ across runs')
    keys = df[['entity', 'seed', 'arm']].apply(tuple, axis=1)
    if keys.duplicated().any():
        fail('coverage', 'duplicate logical keys')
    exp = {(e, s, arm) for e in ref for s in range(4) for arm in ARMS}
    missing = sorted(exp - set(keys))
    if missing:
        fail('coverage', f'{len(missing)} missing logical keys')

    df.to_csv(out_dir / 'smd28_runs.csv', index=False)
    checks = {
        'code_sha': CODE_SHA,
        'campaigns': queue_info,
        'n_rows': int(len(df)), 'n_expected': len(exp), 'missing': [list(m) for m in missing],
        'duplicates': duplicates, 'orphan_result_dirs': orphan_dirs,
        'entities': sorted(df['entity'].unique().tolist()), 'seeds': sorted(df['seed'].unique().tolist()),
        'arms': {k: list(v) for k, v in ARMS.items()},
        'config_sha256_by_arm': {arm: sorted(df.loc[df.arm == arm, 'config_sha256'].unique().tolist()) for arm in ARMS},
        'config_varying_keys': varying, 'config_run_identity_keys_excluded': sorted(RUN_KEYS),
        'resolved_config_values': {c: sorted(map(str, df[c].unique())) for c in
                                   ['cfg_MAX_EPOCH', 'cfg_BASE_LR', 'cfg_VAL_FRAC', 'cfg_VAL_ENABLE', 'cfg_PRIOR_TYPE',
                                    'cfg_CALIBRATE', 'fit_protocol', 'calibrate', 'gamma', 'cf_top_k', 'ckpt_format',
                                    'ckpt_protocol']},
        'log_use_cstruct_true_by_arm': {arm: sorted(df.loc[df.arm == arm, 'log_use_cstruct_true'].unique().tolist())
                                        for arm in ARMS},
        'log_perm_nonzero_epochs_by_arm': {arm: sorted(df.loc[df.arm == arm, 'log_perm_nonzero_epochs'].unique().tolist())
                                           for arm in ARMS},
        'cls_ref_dev_from_prior_by_arm': ({arm: [float(df.loc[df.arm == arm, 'cls_ref_dev_from_prior'].min()),
                                                 float(df.loc[df.arm == arm, 'cls_ref_dev_from_prior'].max())]
                                           for arm in ARMS} if 'cls_ref_dev_from_prior' in df else 'skipped'),
        'best_epoch_range_by_arm': {arm: [int(df.loc[df.arm == arm, 'ckpt_epoch'].min()),
                                          int(df.loc[df.arm == arm, 'ckpt_epoch'].max())] for arm in ARMS},
        'evaluator_signature': sorted(df['evaluator_sig'].unique().tolist()),
        'data_sha256_match_reference': {e: data_sha[e] == ref[e]['file_sha256'] for e in sorted(ref)},
        'n_nonfinite_metric_values': int(df['n_nonfinite_metrics'].sum()),
        'all_train_success': bool((df['train_status'] == 'success').all()),
        'all_eval_success': bool((df['eval_status'] == 'success').all()),
        'failures': failures,
    }
    json.dump(checks, open(out_dir / 'smd28_checks.json', 'w'), indent=1, default=str)
    print(f'rows={len(df)} expected={len(exp)} missing={len(missing)} duplicates={len(duplicates)} '
          f'orphans={len(orphan_dirs)} failures={len(failures)} varying={varying}')
    for f_ in failures[:20]:
        print('  FAIL', f_)


if __name__ == '__main__':
    main()
