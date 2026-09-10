#!/usr/bin/env python3
"""Export completed launcher results into a small, publishable reproduction package,
and aggregate packages from several servers.

    python scripts/export_results.py export --out_root <launcher out_root> --campaign cfval --server server4 \
        [--run_id NAME] [--reports_root <dir>] [--data_root D] [--prior_cache_dir P]
    python scripts/export_results.py aggregate --reports_root <dir> --campaign cfval [--expected_seeds 0,1,2,3]

Export reads <out_root>/_launcher/<name>/queue.json (one per launcher manifest), keeps only jobs whose
SUCCESS.json and provenance.json exist, lists every other job with its status (the package is marked
complete only when all jobs succeeded), and writes to <reports_root>/<campaign>/<server>/<run_id>/:
    metrics.csv, run_manifest.json, config_resolved.yaml, provenance_summary.json, artifacts.json, summary.md
Checkpoints, scores.npz, data files, logs and symlinks are not copied; their sha256/size go to artifacts.json.
Absolute personal paths are replaced by placeholders; the original provenance stays on the server.
Several attempts of one logical job are never merged or ranked by metrics: only the attempt recorded in
queue.json is exported and the others are listed under `duplicates`.
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import yaml

REPO = Path(__file__).resolve().parents[1]
EXPORT_VERSION = 'export_results/1'
RESULT_KIND = 'val_ckpt_eval'          # eval_ckpt.py on last/best_val checkpoints of the validation protocol
SECRET_KEYS = re.compile(r'(token|secret|password|passwd|api_key|apikey|credential)', re.I)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def sha256_file(p: str | Path) -> str | None:
    p = Path(p)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


def git_info(repo: Path) -> dict:
    def _run(cmd):
        try:
            return subprocess.check_output(cmd, cwd=str(repo), stderr=subprocess.DEVNULL).decode().strip()
        except Exception:
            return None
    st = _run(['git', 'status', '--porcelain', '--untracked-files=no'])
    return {'commit': _run(['git', 'rev-parse', 'HEAD']), 'branch': _run(['git', 'rev-parse', '--abbrev-ref', 'HEAD']),
            'dirty_tracked': bool(st) if st is not None else None}


class Redactor:
    """Replace absolute personal paths with placeholders and drop secret-looking keys."""
    def __init__(self, prefixes: dict):
        # longest prefix first
        self.prefixes = sorted(((str(Path(v).resolve()), k) for k, v in prefixes.items() if v), key=lambda kv: -len(kv[0]))
        self.home_re = re.compile(r'/(?:home|Users)/[^/\s"\']+')
        self.user = getpass.getuser()

    def s(self, text: str) -> str:
        for real, tag in self.prefixes:
            text = text.replace(real, f'<{tag}>')
        text = self.home_re.sub('<HOME>', text)
        text = text.replace(self.user, '<USER>') if self.user and len(self.user) > 2 else text
        return text

    def obj(self, o):
        if isinstance(o, dict):
            return {k: self.obj(v) for k, v in o.items() if not SECRET_KEYS.search(str(k))}
        if isinstance(o, (list, tuple)):
            return [self.obj(v) for v in o]
        if isinstance(o, str):
            return self.s(o)
        return o


def _rel(path: str | None, out_root: Path) -> str | None:
    if not path:
        return None
    try:
        return str(Path(path).resolve().relative_to(out_root.resolve()))
    except ValueError:
        return None


# ----------------------------------------------------------------------------
# export
# ----------------------------------------------------------------------------
def _find_queues(out_root: Path):
    return sorted(out_root.glob('_launcher/*/queue.json'))


def _attempt_dirs(base: Path):
    return sorted((p for p in base.glob('attempt*') if p.is_dir()), key=lambda p: int(p.name[7:]) if p.name[7:].isdigit() else 0)


# an absolute machine path that survived redaction (a placeholder such as <HOME>/data/x is not a leak)
ABS_PATH_RE = re.compile(r'(?<![\w<>])/(?:mnt|srv|data|scratch|opt|home|Users|tmp|var|media)/[^\s"\'<>]+')


def export(out_root: str, campaign: str, server: str, run_id: str | None, reports_root: str,
           data_root: str | None = None, prior_cache_dir: str | None = None, queue_name: str | None = None,
           redact_prefixes: list | None = None) -> Path:
    out_root_p = Path(out_root).resolve()
    queues = _find_queues(out_root_p)
    if queue_name:
        queues = [q for q in queues if q.parent.name == queue_name]
    if not queues:
        raise SystemExit(f'no _launcher/*/queue.json under {out_root_p}')
    if len(queues) > 1:
        raise SystemExit(f'several launcher queues under {out_root_p}: {[q.parent.name for q in queues]}; pass --queue_name')
    q = json.loads(queues[0].read_text())
    run_id = run_id or q['name']
    dest = Path(reports_root).resolve() / campaign / server / run_id
    dest.mkdir(parents=True, exist_ok=True)
    prefixes = {'OUT_ROOT': str(out_root_p), 'OUT_ROOT_PARENT': str(out_root_p.parent), 'REPO': str(REPO), 'DATA_ROOT': data_root or '',
                'PRIOR_CACHE': prior_cache_dir or '', 'REPORTS_ROOT': str(Path(reports_root).resolve())}
    for i, extra in enumerate(redact_prefixes or []):
        prefixes[f'PATH{i + 1}'] = extra
    red = Redactor(prefixes)

    jobs = q['jobs']; by_id = {j['id']: j for j in jobs}
    status_rows, metrics_rows, prov_summary, artifacts, duplicates, configs = [], [], {'train': {}, 'eval': {}}, [], [], {}
    training_shas = set()

    for j in jobs:
        rec = {'job_id': j['id'], 'kind': j['kind'], 'status': j['status'], 'exit_code': j.get('exit_code'),
               'attempt_dir': _rel(j.get('job_dir'), out_root_p), 'gpu_index': (j.get('gpu') or {}).get('index'),
               'gpu_uuid': (j.get('gpu') or {}).get('uuid'), 'started_at': j.get('started_at'), 'finished_at': j.get('finished_at'),
               'blocked_reason': (j.get('meta') or {}).get('blocked_reason')}
        jd = Path(j['job_dir']) if j.get('job_dir') else None
        ok = j['status'] in ('success', 'skipped_done') and jd is not None and (jd / 'SUCCESS.json').exists()
        if j['kind'] == 'eval':
            ok = ok and (jd / 'provenance.json').exists() and (jd / 'metrics.csv').exists()
        rec['exported'] = (bool(ok) if j['kind'] != 'prior' else None)   # prior jobs have no artifacts to export
        # duplicate attempts of the same logical job (never ranked by metrics)
        if jd is not None:
            others = [p for p in _attempt_dirs(jd.parent) if p != jd and (p / 'SUCCESS.json').exists()]
            if others:
                duplicates.append({'job_id': j['id'], 'exported_attempt': _rel(str(jd), out_root_p),
                                   'other_successful_attempts': [_rel(str(p), out_root_p) for p in others],
                                   'policy': 'only the attempt recorded in queue.json is exported; no metric-based selection'})
        status_rows.append(rec)
        if not ok:
            continue
        succ = json.loads((jd / 'SUCCESS.json').read_text())
        if j['kind'] == 'train':
            ident = succ.get('identity', {})
            code = (ident.get('code') or {}).get('commit'); training_shas.add(code)
            vm = None
            vcs = list(jd.glob('*_val_metrics.csv'))
            if vcs:
                v = pd.read_csv(vcs[0])
                vm = {'epochs': int(len(v)), 'last_epoch': int(v['epoch'].iloc[-1]), 'last_val_pred_mae': float(v['val_pred_mae'].iloc[-1]),
                      'best_epoch': int(v['best_epoch_so_far'].iloc[-1]), 'best_val_pred_mae': float(v['best_val_mae_so_far'].iloc[-1]),
                      'all_finite': bool(v['val_pred_mae'].notna().all())}
            ck = {}
            for tag in ('best_val', 'last'):
                for p in jd.glob(f"ckpt/*_{tag}.pt"):
                    ck[tag] = {'file': _rel(str(p), out_root_p), 'sha256': sha256_file(p), 'size': p.stat().st_size}
                    artifacts.append({'job_id': j['id'], 'kind': 'checkpoint', 'tag': tag, 'path': _rel(str(p), out_root_p), 'sha256': ck[tag]['sha256'], 'size': ck[tag]['size']})
            for p in jd.glob('*.log'):
                artifacts.append({'job_id': j['id'], 'kind': 'log', 'path': _rel(str(p), out_root_p), 'sha256': sha256_file(p), 'size': p.stat().st_size})
            cfg_txt = (jd / 'config.yaml').read_text() if (jd / 'config.yaml').exists() else None
            if cfg_txt:
                configs[ident.get('config', j['meta'].get('config'))] = yaml.safe_load(cfg_txt)
            prov_summary['train'][j['id']] = red.obj({
                'dataset': j['meta'].get('dataset'), 'entity': j['meta'].get('entity'), 'seed': j['meta'].get('seed'), 'config': ident.get('config'),
                'config_sha256': ident.get('config_sha256'), 'data_sha256': ident.get('data_sha256'), 'training_code': ident.get('code'),
                'python': ident.get('python'), 'val_enabled': ident.get('val_enabled'), 'epochs_override': ident.get('epochs'), 'expected_n': ident.get('expected_n'),
                'gpu': j.get('gpu'), 'started_at': j.get('started_at'), 'finished_at': j.get('finished_at'),
                'duration_s': (j['finished_at'] - j['started_at']) if j.get('finished_at') and j.get('started_at') else None,
                'val_metrics': vm, 'checkpoints': ck, 'attempt_dir': _rel(str(jd), out_root_p)})
        else:  # eval
            prov = json.loads((jd / 'provenance.json').read_text())
            m = pd.read_csv(jd / 'metrics.csv')
            tj = by_id.get(j['deps'][0]) if j.get('deps') else None
            train_code = ((j.get('identity') or {}).get('train_identity') or {}).get('code', {}).get('commit')
            if train_code:
                training_shas.add(train_code)
            common = {'job_id': j['id'], 'result_kind': RESULT_KIND, 'protocol': prov['checkpoint'].get('protocol'),
                      'dataset': j['meta'].get('dataset'), 'entity': j['meta'].get('entity'), 'seed': j['meta'].get('seed'),
                      'config': j['meta'].get('config'), 'ckpt_tag': j['meta'].get('ckpt_tag'), 'ckpt_epoch': prov['restore']['restored_epoch'],
                      'ckpt_sha256': prov['checkpoint']['sha256'], 'ckpt_val_mae': prov['checkpoint'].get('val_mae'),
                      'split_id': prov['data'].get('split_id'), 'fit_protocol': prov['data'].get('fit_protocol'), 'data_sha256': prov['data'].get('npz_sha256'),
                      'prior_cache_key': prov['checkpoint'].get('prior_cache_key'), 'gamma': prov['scoring'].get('gamma'),
                      'calibrate': prov['calibration'].get('enabled'), 'cf_top_k': prov['cf'].get('top_k'), 'vus_window': prov['evaluator'].get('sliding_window_used'),
                      'training_code_sha': train_code, 'eval_code_sha': (prov.get('code_fingerprint') or {}).get('commit'),
                      'device': prov.get('device'), 'torch_version': prov.get('torch_version'), 'attempt_dir': _rel(str(jd), out_root_p),
                      'native_parity_ok': (all(prov['native_parity'].values()) if prov.get('native_parity') else None),
                      'state_unchanged': prov.get('state_unchanged')}
            for _, r in m.iterrows():
                row = dict(common); row.update({k: r[k] for k in m.columns if k not in ('entity', 'seed', 'epoch')})
                metrics_rows.append(row)
            prov_summary['eval'][j['id']] = red.obj({k: prov.get(k) for k in ('checkpoint', 'restore', 'data', 'scoring', 'cf', 'calibration', 'evaluator', 'forward_passes',
                                                                            'native_parity', 'state_unchanged', 'device', 'torch_version', 'elapsed_s', 'finished_at', 'code_fingerprint')} |
                                                  {'gpu': j.get('gpu'), 'attempt_dir': _rel(str(jd), out_root_p), 'train_job': tj['id'] if tj else None})
            for p in [jd / 'scores.npz'] + list(jd.parent.glob(f'{jd.name}.log')):
                if p.exists():
                    artifacts.append({'job_id': j['id'], 'kind': 'scores' if p.suffix == '.npz' else 'log', 'path': _rel(str(p), out_root_p), 'sha256': sha256_file(p), 'size': p.stat().st_size})
            if (jd / 'config_resolved.yaml').exists():
                configs.setdefault(j['meta'].get('config'), yaml.safe_load((jd / 'config_resolved.yaml').read_text()))
            # data files are outside out_root: identifiers only
            artifacts.append({'job_id': j['id'], 'kind': 'data_npz', 'path': red.s(prov['data'].get('npz_path', '')), 'sha256': prov['data'].get('npz_sha256'), 'shapes': prov['data'].get('shapes')})

    # ---- write package ----
    counts = {}
    for r in status_rows:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    complete = all(r['status'] in ('success', 'skipped_done') for r in status_rows) and bool(status_rows)
    df = pd.DataFrame(metrics_rows)
    df.to_csv(dest / 'metrics.csv', index=False)
    # content hash over everything that describes the results (no timestamps); an unchanged package keeps its
    # previous export stamp so repeated exports/publishes are idempotent
    content = json.dumps(red.obj({'metrics': metrics_rows, 'prov': prov_summary, 'artifacts': artifacts, 'configs': configs, 'jobs': status_rows,
                                  'duplicates': duplicates}), sort_keys=True, default=str)
    content_sha = hashlib.sha256(content.encode()).hexdigest()
    stamp = {'exported_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'exported_by_host': socket.gethostname(), 'export_code': git_info(REPO)}
    prev_p = dest / 'run_manifest.json'
    if prev_p.exists():
        try:
            prev = json.loads(prev_p.read_text())
            if prev.get('content_sha256') == content_sha:
                stamp = {k: prev[k] for k in ('exported_at', 'exported_by_host', 'export_code')}
        except Exception:
            pass
    manifest = red.obj({
        'export_version': EXPORT_VERSION, 'content_sha256': content_sha, **stamp,
        'campaign': campaign, 'server': server, 'run_id': run_id, 'launcher_queue': q['name'], 'launcher_manifest': q.get('manifest'),
        'launcher_updated_at': q.get('updated_at'), 'launcher_stopped': q.get('stopped'),
        'training_code_sha': sorted(s for s in training_shas if s), 'launcher_code': q.get('code'),
        'note_publishing_commit': 'the Git commit that publishes this package is NOT the training commit; see training_code_sha',
        'result_kind': RESULT_KIND, 'complete': complete, 'job_counts': counts, 'n_jobs': len(status_rows),
        'n_exported_eval_jobs': sum(1 for r in status_rows if r['kind'] == 'eval' and r['exported']),
        'n_exported_train_jobs': sum(1 for r in status_rows if r['kind'] == 'train' and r['exported']),
        'duplicates': duplicates, 'jobs': status_rows,
        'excluded_from_package': ['checkpoints (*.pt)', 'scores.npz', 'data NPZ', 'logs', 'symlinks'],
    })
    (dest / 'run_manifest.json').write_text(json.dumps(manifest, indent=1, default=str))
    (dest / 'provenance_summary.json').write_text(json.dumps(red.obj(prov_summary), indent=1, default=str))
    (dest / 'artifacts.json').write_text(json.dumps(red.obj({'out_root_placeholder': '<OUT_ROOT>', 'artifacts': artifacts}), indent=1, default=str))
    (dest / 'config_resolved.yaml').write_text(yaml.safe_dump(red.obj({k: v for k, v in configs.items()}), sort_keys=False))
    (dest / 'summary.md').write_text(_summary_md(manifest, df, prov_summary))
    # leak check: any absolute machine path left in the package is listed (never silently shipped)
    leaks = sorted({m for f in dest.iterdir() for m in ABS_PATH_RE.findall(f.read_text())})
    if leaks:
        manifest['redaction_warnings'] = leaks
        (dest / 'run_manifest.json').write_text(json.dumps(manifest, indent=1, default=str))
        print(f'[export] WARNING: absolute paths remain in the package (add --redact_prefix): {leaks[:5]}', file=sys.stderr)
    return dest


def _summary_md(man: dict, df: pd.DataFrame, prov: dict) -> str:
    L = [f"# {man['campaign']} / {man['server']} / {man['run_id']}", '',
         f"- exported: {man['exported_at']} (export tool commit {man['export_code'].get('commit')}); training code sha: {', '.join(man['training_code_sha']) or 'n/a'}",
         f"- result kind: `{man['result_kind']}` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)",
         f"- jobs: {man['n_jobs']} — {man['job_counts']} — **{'COMPLETE' if man['complete'] else 'INCOMPLETE'}**",
         f"- exported eval jobs: {man['n_exported_eval_jobs']}, train jobs: {man['n_exported_train_jobs']}; duplicates flagged: {len(man['duplicates'])}", '']
    if not df.empty:
        L.append('| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |'); L.append('|---|---|---|---|---|---|---|---|---|---|---|')
        for _, r in df[df['kind'] == 'fusion'].iterrows():
            L.append(f"| {r['dataset']} | {r['entity']} | {r['seed']} | {r['ckpt_tag']} | {r['ckpt_epoch']} | {r['variant']} | {r['AUC-PR']:.4f} | {r['VUS-PR']:.4f} | {r['Standard-F1']:.4f} | {r['gamma']} | {r['calibrate']} |")
        L.append('')
    bad = [j for j in man['jobs'] if j['exported'] is False]
    if bad:
        L.append('## Not exported'); L += [f"- {j['job_id']}: {j['status']} exit={j['exit_code']} {j.get('blocked_reason') or ''}" for j in bad]; L.append('')
    if prov['train']:
        L.append('## Training (validation MAE selection)'); L.append('| job | epochs | last ep / MAE | best ep / MAE | duration s |'); L.append('|---|---|---|---|---|')
        for jid, t in prov['train'].items():
            vm = t.get('val_metrics') or {}
            L.append(f"| {jid} | {vm.get('epochs')} | {vm.get('last_epoch')} / {vm.get('last_val_pred_mae')} | {vm.get('best_epoch')} / {vm.get('best_val_pred_mae')} | {t.get('duration_s') and round(t['duration_s'])} |")
    return '\n'.join(L) + '\n'


# ----------------------------------------------------------------------------
# aggregate
# ----------------------------------------------------------------------------
SMD_ALL = [f'machine-{g}-{i}' for g, n in [(1, 8), (2, 9), (3, 11)] for i in range(1, n + 1)]
PROTO_KEYS = ['protocol', 'result_kind', 'config', 'gamma', 'calibrate', 'cf_top_k', 'fit_protocol']


def aggregate(reports_root: str, campaign: str, expected_seeds=(0, 1, 2, 3), out_dir: str | None = None) -> Path:
    root = Path(reports_root).resolve() / campaign
    pkgs = sorted(p for p in root.glob('*/*/run_manifest.json') if p.parent.parent.name != '_aggregate')
    if not pkgs:
        raise SystemExit(f'no packages under {root}')
    frames, sources, cfg_sig = [], [], {}
    for mp in pkgs:
        man = json.loads(mp.read_text()); d = mp.parent
        df = pd.read_csv(d / 'metrics.csv') if (d / 'metrics.csv').stat().st_size > 0 else pd.DataFrame()
        if df.empty:
            sources.append({'package': str(d.relative_to(root)), 'server': man['server'], 'complete': man['complete'], 'rows': 0}); continue
        if (df['result_kind'] != RESULT_KIND).any():
            raise SystemExit(f'{d}: mixed result kinds {sorted(df["result_kind"].unique())}; only {RESULT_KIND} rows may be aggregated')
        df['package'] = str(d.relative_to(root)); df['server'] = man['server']; df['package_complete'] = man['complete']
        frames.append(df); sources.append({'package': str(d.relative_to(root)), 'server': man['server'], 'complete': man['complete'], 'rows': int(len(df))})
        cfgs = yaml.safe_load((d / 'config_resolved.yaml').read_text()) or {}
        for name, c in cfgs.items():
            sig = {'MAX_EPOCH': c['SOLVER']['MAX_EPOCH'], 'BASE_LR': c['SOLVER']['BASE_LR'], 'BATCH': c['TRAIN']['BATCH_SIZE'],
                   'PERM': c['PICAAD']['INTERVENTION']['PERM_PAIRS_PER_BATCH'], 'CALIBRATE': c['PICAAD']['SCORING']['CALIBRATE'],
                   'USE_CF': c['PICAAD']['SCORING']['USE_COUNTERFACTUAL'], 'GAMMA': c['PICAAD']['SCORING']['SCORE_GAMMA'], 'CF_TOP_K': c['PICAAD']['SCORING']['CF_TOP_K'],
                   'VAL': (c['VAL']['ENABLE'], c['VAL']['FRAC']), 'EVAL': (c['EVAL']['USE_MEDIAN_VUS_WINDOW'], c['EVAL']['VUS_VERSION'], c['EVAL']['VUS_THRE'])}
            if name in cfg_sig and cfg_sig[name] != sig:
                raise SystemExit(f'config/evaluator mismatch for {name} between packages: {cfg_sig[name]} vs {sig} ({d})')
            cfg_sig[name] = sig
    if not frames:
        raise SystemExit('no metric rows to aggregate')
    all_df = pd.concat(frames, ignore_index=True)
    # protocol consistency per dataset
    issues = []
    for ds, g in all_df.groupby('dataset'):
        for k in PROTO_KEYS:
            vals = sorted(map(str, g[k].dropna().unique()))
            if len(vals) > 1:
                issues.append(f'{ds}: {k} differs across rows: {vals}')
    if issues:
        raise SystemExit('protocol mismatch, refusing to aggregate: ' + '; '.join(issues))
    fus = all_df[all_df['kind'] == 'fusion']
    # duplicate logical results (same dataset/entity/seed/ckpt_tag/variant from different packages)
    key = ['dataset', 'entity', 'seed', 'ckpt_tag', 'variant']
    dup = fus[fus.duplicated(key, keep=False)]
    if not dup.empty:
        raise SystemExit('the same logical result appears in more than one package: ' + str(dup[key + ['package']].drop_duplicates().to_dict('records')[:5]))
    exp = set(int(s) for s in expected_seeds)
    coverage = {}
    for ds, g in fus.groupby('dataset'):
        ents = sorted(g['entity'].unique()); seeds_by_ent = {e: sorted(int(s) for s in g[g['entity'] == e]['seed'].unique()) for e in ents}
        if ds == 'SMD':
            full = (set(ents) == set(SMD_ALL)) and all(set(seeds_by_ent[e]) >= exp for e in ents)
            coverage[ds] = {'entities': len(ents), 'of': len(SMD_ALL), 'missing_entities': sorted(set(SMD_ALL) - set(ents)),
                            'entities_missing_seeds': {e: sorted(exp - set(s)) for e, s in seeds_by_ent.items() if exp - set(s)},
                            'label': 'full-SMD' if full else f'partial-SMD ({len(ents)}/{len(SMD_ALL)} entities; seeds incomplete for {sum(1 for e, s in seeds_by_ent.items() if exp - set(s))})'}
        else:
            coverage[ds] = {'entities': ents, 'seeds': seeds_by_ent, 'missing_seeds': {e: sorted(exp - set(s)) for e, s in seeds_by_ent.items() if exp - set(s)},
                            'label': 'all seeds' if all(set(s) >= exp for s in seeds_by_ent.values()) else 'partial seeds'}
    per_seed = fus[['dataset', 'entity', 'seed', 'ckpt_tag', 'ckpt_epoch', 'variant', 'AUC-PR', 'VUS-PR', 'Standard-F1', 'gamma', 'calibrate', 'server', 'package']].sort_values(key)
    agg = fus.groupby(['dataset', 'ckpt_tag', 'variant']).agg(n_rows=('AUC-PR', 'size'), n_entities=('entity', 'nunique'), n_seeds=('seed', 'nunique'),
                                                              AUC_PR_mean=('AUC-PR', 'mean'), AUC_PR_std=('AUC-PR', 'std'), VUS_PR_mean=('VUS-PR', 'mean'), VUS_PR_std=('VUS-PR', 'std'),
                                                              F1_mean=('Standard-F1', 'mean')).reset_index()
    agg['coverage'] = agg['dataset'].map(lambda d: coverage[d]['label'])
    inputs_hash = hashlib.sha256(''.join(sorted(sha256_file(mp) for mp in pkgs)).encode()).hexdigest()[:12]
    od = Path(out_dir) if out_dir else root / '_aggregate' / f'aggregate_{time.strftime("%Y%m%d-%H%M%S")}_{inputs_hash}'
    od.mkdir(parents=True, exist_ok=True)
    per_seed.to_csv(od / 'per_seed_results.csv', index=False); agg.to_csv(od / 'dataset_means.csv', index=False)
    (od / 'aggregate_manifest.json').write_text(json.dumps({'campaign': campaign, 'created_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'inputs_hash': inputs_hash,
                                                             'sources': sources, 'config_signatures': cfg_sig, 'coverage': coverage, 'expected_seeds': sorted(exp),
                                                             'result_kind': RESULT_KIND, 'rule': 'means over available seeds/entities only; SMD labelled full only with 28 entities x expected seeds; '
                                                                                                  'test-selected, gamma-sweep or native training-time results are never included'}, indent=1, default=str))
    md = [f'# Aggregate — {campaign}', '', f'inputs: {len(pkgs)} packages ({sum(s["rows"] for s in sources)} rows); incomplete packages: {[s["package"] for s in sources if not s["complete"]]}', '',
          '## Coverage'] + [f"- {ds}: {c['label']}" for ds, c in coverage.items()] + ['', '## Means over available seeds/entities (see per_seed_results.csv)', '',
          '| dataset | ckpt | variant | n | entities | seeds | AUC-PR mean±std | VUS-PR mean±std | coverage |', '|---|---|---|---|---|---|---|---|---|']
    for _, r in agg.iterrows():
        md.append(f"| {r['dataset']} | {r['ckpt_tag']} | {r['variant']} | {r['n_rows']} | {r['n_entities']} | {r['n_seeds']} | {r['AUC_PR_mean']:.4f}±{0 if pd.isna(r['AUC_PR_std']) else r['AUC_PR_std']:.4f} | {r['VUS_PR_mean']:.4f}±{0 if pd.isna(r['VUS_PR_std']) else r['VUS_PR_std']:.4f} | {r['coverage']} |")
    (od / 'aggregate.md').write_text('\n'.join(md) + '\n')
    return od


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('export'); e.add_argument('--out_root', required=True); e.add_argument('--campaign', required=True); e.add_argument('--server', required=True)
    e.add_argument('--run_id'); e.add_argument('--reports_root', default=str(REPO / 'reports' / 'experiments')); e.add_argument('--data_root'); e.add_argument('--prior_cache_dir'); e.add_argument('--queue_name')
    e.add_argument('--redact_prefix', action='append', default=[], help='extra absolute path prefix to replace by a placeholder (repeatable)')
    e.add_argument('--fail_on_leak', action='store_true', help='exit 3 if any absolute machine path remains in the package')
    a = sub.add_parser('aggregate'); a.add_argument('--reports_root', default=str(REPO / 'reports' / 'experiments')); a.add_argument('--campaign', required=True)
    a.add_argument('--expected_seeds', default='0,1,2,3'); a.add_argument('--out_dir')
    args = ap.parse_args(argv)
    if args.cmd == 'export':
        d = export(args.out_root, args.campaign, args.server, args.run_id, args.reports_root, args.data_root, args.prior_cache_dir, args.queue_name, args.redact_prefix)
        man = json.loads((d / 'run_manifest.json').read_text())
        print(f"exported -> {d}  complete={man['complete']} jobs={man['job_counts']} eval_jobs={man['n_exported_eval_jobs']} duplicates={len(man['duplicates'])}"
              f"{'  REDACTION WARNINGS: ' + str(len(man['redaction_warnings'])) if man.get('redaction_warnings') else ''}")
        return 3 if (args.fail_on_leak and man.get('redaction_warnings')) else 0
    d = aggregate(args.reports_root, args.campaign, [int(s) for s in args.expected_seeds.split(',') if s.strip()], args.out_dir)
    print(f'aggregate -> {d}'); return 0


if __name__ == '__main__':
    sys.exit(main())
