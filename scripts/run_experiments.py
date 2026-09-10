#!/usr/bin/env python3
"""Multi-GPU experiment launcher (common entry point).

Expands a manifest (dataset x entity x seed x training config) into a queue of
independent jobs, assigns ONE job per GPU (no DDP/DataParallel), and chains
evaluation after successful training. It calls the existing CLIs only:

    training : python main.py --cfg <yaml> SEEDS [s] DATA.ENTITIES <e> RESULT_DIR <dir> RESULT_DIR_LITERAL True ...
    priors   : one CPU job per (config, entity) that calls model.build.build_causal_prior_cached
    eval     : python scripts/eval_ckpt.py --ckpt_dir <dir>/ckpt --entity <e> --seed <s> --ckpt_tag <last|best_val> ...

It never runs scripts/aggregate_best_epoch.py or main._final_eval, never picks
jobs/checkpoints by test metrics, and never changes batch size / precision /
model settings on OOM (the job simply fails and is reported).

Paths come from CLI or environment:
    --python / PICAAD_PYTHON, --data_root / PICAAD_DATA_ROOT (default <repo>/data_npz),
    --prior_cache_dir / PICAAD_PRIOR_CACHE (default: config value),
    --out_root / PICAAD_OUT_ROOT (default <repo>/results/experiments),
    --lock_dir / PICAAD_LOCK_DIR (default <tmp>/picaad_gpu_locks; shared between launchers)

Examples
    python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --gpus auto --dry-run
    python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --gpus 0,1,2
    python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --gpus auto --resume
    python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --status
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.run_parallel import SMD_ENTITIES, _cfg_val_enabled   # noqa: E402  (reused)

DEFAULT_PYTHON = os.environ.get('PICAAD_PYTHON', sys.executable)
DEFAULT_DATA_ROOT = os.environ.get('PICAAD_DATA_ROOT', str(REPO / 'data_npz'))
DEFAULT_PRIOR_CACHE = os.environ.get('PICAAD_PRIOR_CACHE', '')
DEFAULT_OUT_ROOT = os.environ.get('PICAAD_OUT_ROOT', str(REPO / 'results' / 'experiments'))
DEFAULT_LOCK_DIR = os.environ.get('PICAAD_LOCK_DIR', os.path.join(tempfile.gettempdir(), 'picaad_gpu_locks'))

# CPU-only snippet: fills the prior cache for one (config, entity) with the same
# split id main.py will use. Extra "KEY VALUE" opts (paths) are forwarded.
_PRIOR_SNIPPET = (
    'import sys; sys.path.insert(0, ".");'
    'from config import get_cfg_defaults;'
    'from datasets.build import load_entity;'
    'from datasets.split import split_id_for;'
    'from model.build import build_causal_prior_cached;'
    'cfg = get_cfg_defaults(); cfg.merge_from_file(sys.argv[1]);'
    'cfg.merge_from_list(["DATA.ENTITIES", sys.argv[2]] + sys.argv[3:]);'
    'e = load_entity(cfg, sys.argv[2]);'
    'build_causal_prior_cached(cfg, e.train_z, e.name, split_id=split_id_for(cfg, e));'
    'print("[prior-warmup] done", e.name)'
)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _sha256_file(path: str) -> Optional[str]:
    if not path or not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


def code_fingerprint() -> dict:
    def _run(cmd):
        try:
            return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, cwd=str(REPO)).decode()
        except Exception:
            return ''
    commit = _run(['git', 'rev-parse', 'HEAD']).strip() or None
    diff = _run(['git', 'diff', 'HEAD', '--', '.', ':!docs', ':!tests/golden'])
    return {'commit': commit, 'tracked_diff_sha256': hashlib.sha256(diff.encode()).hexdigest()}


def next_attempt_dir(base: Path) -> Path:
    """First attempt directory under base that does not exist yet (never reuse)."""
    n = 1
    while (base / f'attempt{n}').exists():
        n += 1
    return base / f'attempt{n}'


# ----------------------------------------------------------------------------
# GPU probe / lock
# ----------------------------------------------------------------------------
class GpuProbe:
    """Reads physical GPU state via nvidia-smi. Tests replace `query`."""
    def __init__(self, nvsmi: Optional[str] = None):
        self.nvsmi = nvsmi or ('/usr/bin/nvidia-smi' if os.path.exists('/usr/bin/nvidia-smi') else shutil.which('nvidia-smi'))

    def query(self) -> List[dict]:
        if not self.nvsmi:
            return []
        try:
            gpus = subprocess.check_output([self.nvsmi, '--query-gpu=index,uuid,memory.used,memory.total',
                                            '--format=csv,noheader,nounits'], stderr=subprocess.DEVNULL, timeout=20).decode()
            apps = subprocess.check_output([self.nvsmi, '--query-compute-apps=gpu_uuid,pid,used_memory',
                                            '--format=csv,noheader,nounits'], stderr=subprocess.DEVNULL, timeout=20).decode()
        except Exception:
            return []
        out = {}
        for line in gpus.splitlines():
            parts = [x.strip() for x in line.split(',')]
            if len(parts) < 4:
                continue
            out[parts[1]] = {'index': int(parts[0]), 'uuid': parts[1], 'mem_used_mb': int(float(parts[2])),
                             'mem_total_mb': int(float(parts[3])), 'procs': []}
        for line in apps.splitlines():
            parts = [x.strip() for x in line.split(',')]
            if len(parts) < 2 or parts[0] not in out:
                continue
            try:
                pid = int(parts[1])
            except ValueError:
                continue
            uid = None
            try:
                uid = os.stat(f'/proc/{pid}').st_uid
            except OSError:
                pass
            out[parts[0]]['procs'].append({'pid': pid, 'uid': uid})
        return sorted(out.values(), key=lambda g: g['index'])


class GpuLock:
    """Cross-launcher exclusive lock per physical GPU (flock on <lock_dir>/gpu_<uuid>.lock)."""
    def __init__(self, lock_dir: str, uuid: str):
        os.makedirs(lock_dir, exist_ok=True)
        self.path = os.path.join(lock_dir, f'gpu_{uuid}.lock')
        self.f = None

    def acquire(self) -> bool:
        f = open(self.path, 'a+')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            f.close()
            return False
        f.seek(0); f.truncate(); f.write(f'pid={os.getpid()} t={time.time()}\n'); f.flush()
        self.f = f
        return True

    def release(self):
        if self.f is not None:
            try:
                fcntl.flock(self.f, fcntl.LOCK_UN)
            finally:
                self.f.close(); self.f = None


def parse_visible_env() -> Optional[List[str]]:
    """Tokens of CUDA_VISIBLE_DEVICES in the launcher's own environment (None = unrestricted)."""
    v = os.environ.get('CUDA_VISIBLE_DEVICES')
    if v is None:
        return None
    return [t.strip() for t in v.split(',') if t.strip()]


# ----------------------------------------------------------------------------
# jobs
# ----------------------------------------------------------------------------
@dataclass
class Job:
    id: str
    kind: str                      # prior | train | eval
    cmd: List[str]
    deps: List[str]
    job_dir: Optional[str]         # where outputs land (train: RESULT_DIR; eval: --out_dir; prior: None)
    log_path: str
    needs_gpu: bool
    meta: dict = field(default_factory=dict)
    identity: dict = field(default_factory=dict)   # config/data/code identifiers for resume
    success_files: List[str] = field(default_factory=list)
    status: str = 'pending'        # pending | running | success | failed | blocked | skipped_done | killed
    attempt_dir_base: Optional[str] = None
    exit_code: Optional[int] = None
    gpu: Optional[dict] = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    marker_path: Optional[str] = None

    def to_record(self):
        d = {k: getattr(self, k) for k in ('id', 'kind', 'cmd', 'deps', 'job_dir', 'log_path', 'needs_gpu', 'meta',
                                            'identity', 'success_files', 'status', 'exit_code', 'gpu', 'started_at',
                                            'finished_at', 'marker_path')}
        return d


class Plan:
    """Expands a manifest into ordered jobs. Attempt directories are chosen at
    plan time and never reused; --resume reads SUCCESS markers of older attempts."""

    def __init__(self, manifest: dict, args, resume_state: Optional[dict] = None):
        self.m = manifest
        self.a = args
        self.name = manifest.get('name') or Path(args.manifest).stem
        self.out_root = Path(args.out_root).resolve()
        self.data_root = Path(args.data_root).resolve()
        self.python = args.python
        d = manifest.get('defaults', {}) or {}
        self.threads = int(args.threads_per_job or d.get('threads_per_job', 4))
        self.workers = int(args.dataloader_workers if args.dataloader_workers is not None else d.get('dataloader_workers', 0))
        self.prior_workers = int(args.prior_workers or d.get('prior_workers', 1))
        self.eval_defaults = {'ckpt_tags': ['last', 'best_val'], 'cf': 'both', 'calibrate': 'cfg', 'verify_native_parity': False}
        self.eval_defaults.update(d.get('eval', {}) or {})
        self.code = code_fingerprint()
        self.jobs: List[Job] = []
        self._build()

    # ---- path helpers ----
    def _input_dir(self, spec) -> str:
        p = spec.get('input_dir', '')
        return str(p if os.path.isabs(p) else (self.data_root / p))

    def _common_path_opts(self, spec) -> List[str]:
        opts = []
        if self.a.prior_cache_dir:
            opts += ['PICAAD.PRIOR.CACHE_DIR', self.a.prior_cache_dir]
        if spec.get('expected_n'):
            opts += ['DATA.EXPECTED_N', str(int(spec['expected_n']))]
        return opts

    # ---- build ----
    def _build(self):
        prior_ids = {}
        for spec in self.m.get('train', []) or []:
            dataset = spec['dataset']
            cfg_rel = spec['config']; cfg_path = str(REPO / cfg_rel); cfg_stem = Path(cfg_rel).stem
            entities = spec['entities']
            if entities == 'all':
                if dataset != 'SMD':
                    raise ValueError("entities: all is only defined for SMD")
                entities = list(SMD_ENTITIES)
            seeds = [int(s) for s in spec['seeds']]
            input_dir = self._input_dir(spec)
            eval_cfg = dict(self.eval_defaults); eval_cfg.update(spec.get('eval', {}) or {})
            val_enabled = _cfg_val_enabled(cfg_rel)
            for ent in entities:
                npz = os.path.join(input_dir, f'{ent}.npz')
                data_sha = _sha256_file(npz)
                # --- prior warmup (CPU), shared by all seeds of (config, entity) ---
                pid_key = (cfg_rel, ent, input_dir)
                if pid_key not in prior_ids:
                    pj_id = f'prior/{dataset}/{ent}/{cfg_stem}'
                    pcmd = [self.python, '-c', _PRIOR_SNIPPET, cfg_path, ent, 'DATA.INPUT_DIR', input_dir] + self._common_path_opts(spec)
                    plog = self.out_root / '_launcher' / self.name / 'prior_logs' / f'{dataset}_{ent}_{cfg_stem}.log'
                    self.jobs.append(Job(id=pj_id, kind='prior', cmd=pcmd, deps=[], job_dir=None, log_path=str(plog), needs_gpu=False,
                                         meta={'dataset': dataset, 'entity': ent, 'config': cfg_rel},
                                         identity={'config_sha256': _sha256_file(cfg_path), 'data_sha256': data_sha, 'code': self.code,
                                                   'python': self.python, 'prior_cache_dir': self.a.prior_cache_dir or '<cfg>'}))
                    prior_ids[pid_key] = pj_id
                for seed in seeds:
                    base = self.out_root / dataset / ent / f'seed{seed}' / cfg_stem
                    tj_id = f'train/{dataset}/{ent}/seed{seed}/{cfg_stem}'
                    run_dir = next_attempt_dir(base)
                    tcmd = [self.python, '-u', 'main.py', '--cfg', cfg_path, 'SEEDS', f'[{seed}]', 'DATA.ENTITIES', ent,
                            'DATA.INPUT_DIR', input_dir, 'RESULT_DIR', str(run_dir), 'RESULT_DIR_LITERAL', 'True',
                            'DATA_LOADER.NUM_WORKERS', str(self.workers)] + self._common_path_opts(spec)
                    if spec.get('epochs') is not None:
                        tcmd += ['SOLVER.MAX_EPOCH', str(int(spec['epochs']))]
                    # identity must not depend on the attempt directory (RESULT_DIR), only on what defines the run
                    ident = {'config_sha256': _sha256_file(cfg_path), 'data_sha256': data_sha, 'code': self.code, 'python': self.python,
                             'config': cfg_rel, 'entity': ent, 'seed': seed, 'input_dir': input_dir, 'val_enabled': val_enabled,
                             'dataloader_workers': self.workers, 'epochs': spec.get('epochs'), 'expected_n': spec.get('expected_n'),
                             'prior_cache_dir': self.a.prior_cache_dir or '<cfg>'}
                    succ = ([f'ckpt/{ent}_seed{seed}_best_val.pt', f'ckpt/{ent}_seed{seed}_last.pt'] if val_enabled else [])
                    tj = Job(id=tj_id, kind='train', cmd=tcmd, deps=[prior_ids[pid_key]], job_dir=str(run_dir), log_path=str(run_dir / 'launcher_run.log'),
                             needs_gpu=True, meta={'dataset': dataset, 'entity': ent, 'seed': seed, 'config': cfg_rel, 'val_enabled': val_enabled},
                             identity=ident, success_files=succ, attempt_dir_base=str(base))
                    self.jobs.append(tj)
                    if val_enabled:
                        for tag in eval_cfg['ckpt_tags']:
                            self._add_eval_job(f'{tj_id}/eval/{tag}'.replace('train/', 'eval/', 1), tj, base / 'eval' / tag, tag, ent, seed,
                                               input_dir, eval_cfg, spec, dataset)
        for spec in self.m.get('eval_only', []) or []:
            name = spec['name']; base = self.out_root / 'eval_only' / name
            eval_cfg = dict(self.eval_defaults); eval_cfg.update(spec.get('eval', {}) or {})
            out_dir = next_attempt_dir(base)
            input_dir = self._input_dir(spec) if spec.get('input_dir') else None
            cmd = [self.python, 'scripts/eval_ckpt.py', '--out_dir', str(out_dir), '--cf', str(eval_cfg['cf']), '--calibrate', str(eval_cfg['calibrate'])]
            if spec.get('ckpt'):
                cmd += ['--ckpt', spec['ckpt']]; ck_sha = _sha256_file(spec['ckpt'])
            else:
                cmd += ['--ckpt_dir', spec['ckpt_dir'], '--entity', spec['entity'], '--seed', str(spec['seed']), '--ckpt_tag', spec['ckpt_tag']]
                ck_sha = _sha256_file(os.path.join(spec['ckpt_dir'], f"{spec['entity']}_seed{spec['seed']}_{spec['ckpt_tag']}.pt"))
            if input_dir:
                cmd += ['--data_input_dir', input_dir]
            if eval_cfg.get('verify_native_parity'):
                cmd += ['--verify_native_parity']
            self.jobs.append(Job(id=f'evalonly/{name}', kind='eval', cmd=cmd, deps=[], job_dir=str(out_dir), log_path=str(base / f'{out_dir.name}.log'),
                                 needs_gpu=True, meta={'name': name, **{k: spec.get(k) for k in ('ckpt', 'ckpt_dir', 'entity', 'seed', 'ckpt_tag')}},
                                 identity={'ckpt_sha256': ck_sha, 'code': self.code, 'python': self.python, 'input_dir': input_dir,
                                           'cf': str(eval_cfg['cf']), 'calibrate': str(eval_cfg['calibrate']),
                                           'verify_native_parity': bool(eval_cfg.get('verify_native_parity')),
                                           **{k: spec.get(k) for k in ('ckpt', 'ckpt_dir', 'entity', 'seed', 'ckpt_tag')}},
                                 success_files=['provenance.json', 'metrics.csv'], attempt_dir_base=str(base)))

    def _add_eval_job(self, ej_id, tj: Job, base: Path, tag, ent, seed, input_dir, eval_cfg, spec, dataset):
        out_dir = next_attempt_dir(base)
        # ckpt_dir is filled in at launch time from the *successful* train attempt (see Launcher._resolve_ckpt_dir)
        cmd = [self.python, 'scripts/eval_ckpt.py', '--ckpt_dir', '<TRAIN_CKPT_DIR>', '--entity', ent, '--seed', str(seed), '--ckpt_tag', tag,
               '--out_dir', str(out_dir), '--cf', str(eval_cfg['cf']), '--calibrate', str(eval_cfg['calibrate']), '--data_input_dir', input_dir]
        if eval_cfg.get('verify_native_parity'):
            cmd += ['--verify_native_parity']
        self.jobs.append(Job(id=ej_id, kind='eval', cmd=cmd, deps=[tj.id], job_dir=str(out_dir), log_path=str(base / f'{out_dir.name}.log'),
                             needs_gpu=True, meta={'dataset': dataset, 'entity': ent, 'seed': seed, 'config': tj.meta['config'], 'ckpt_tag': tag, 'train_job': tj.id},
                             identity={'train_identity': tj.identity, 'code': self.code, 'python': self.python, 'ckpt_tag': tag,
                                       'cf': str(eval_cfg['cf']), 'calibrate': str(eval_cfg['calibrate']),
                                       'verify_native_parity': bool(eval_cfg.get('verify_native_parity')), 'input_dir': input_dir},
                             success_files=['provenance.json', 'metrics.csv'], attempt_dir_base=str(base)))


# ----------------------------------------------------------------------------
# launcher
# ----------------------------------------------------------------------------
class Launcher:
    def __init__(self, plan: Plan, args, probe: Optional[GpuProbe] = None):
        self.plan, self.a = plan, args
        self.jobs = {j.id: j for j in plan.jobs}
        self.order = [j.id for j in plan.jobs]
        self.probe = probe or GpuProbe()
        self.state_dir = plan.out_root / '_launcher' / plan.name
        self.running: Dict[str, dict] = {}     # job_id -> {'proc', 'lock', 'log'}
        self.child_pids = set()
        self._stop = False
        self.visible_env = parse_visible_env()
        self.lock_dir = args.lock_dir

    # ---- resume ----
    def _find_done_marker(self, job: Job) -> Optional[dict]:
        """Look for a SUCCESS marker in earlier attempts whose identity matches."""
        if not job.attempt_dir_base:
            return None
        base = Path(job.attempt_dir_base)
        if not base.exists():
            return None
        for att in sorted(base.glob('attempt*'), key=lambda p: int(p.name[7:]) if p.name[7:].isdigit() else 0):
            mk = att / 'SUCCESS.json'
            if not mk.exists():
                continue
            try:
                rec = json.loads(mk.read_text())
            except Exception:
                continue
            if rec.get('identity') == job.identity and all((att / f).exists() for f in job.success_files):
                rec['_attempt_dir'] = str(att)
                return rec
        return None

    def apply_resume(self):
        for jid in self.order:
            j = self.jobs[jid]
            if j.kind == 'prior':
                continue  # cheap and idempotent (cache hit); always re-run
            rec = self._find_done_marker(j)
            if rec is not None:
                j.status = 'skipped_done'; j.job_dir = rec['_attempt_dir']; j.marker_path = str(Path(rec['_attempt_dir']) / 'SUCCESS.json')

    # ---- gpu ----
    def _allowed_tokens(self, gpus: List[dict]) -> List[dict]:
        """Filter probe result to GPUs this launcher may use; attach the token to pass as CUDA_VISIBLE_DEVICES."""
        env = self.visible_env
        out = []
        for g in gpus:
            tok = None
            if env is None:
                tok = str(g['index'])
            else:
                for t in env:
                    if t == str(g['index']) or t == g['uuid'] or (t.startswith('GPU-') and g['uuid'].startswith(t)):
                        tok = t; break
                if tok is None:
                    continue
            if self.a.gpus != 'auto':
                wanted = [x.strip() for x in self.a.gpus.split(',') if x.strip()]
                if str(g['index']) not in wanted and g['uuid'] not in wanted:
                    continue
            out.append({**g, 'token': tok})
        if self.a.gpus != 'auto':
            wanted = [x.strip() for x in self.a.gpus.split(',') if x.strip()]
            seen = {str(g['index']) for g in out} | {g['uuid'] for g in out}
            missing = [w for w in wanted if w not in seen]
            if missing:
                raise SystemExit(f'--gpus {self.a.gpus}: not visible/allowed in this environment: {missing} '
                                 f'(CUDA_VISIBLE_DEVICES={os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>")})')
        return out

    def _pick_gpu(self) -> Optional[dict]:
        """Re-probe right before assignment; skip GPUs used by external processes, by our own
        running jobs, or locked by another launcher. Returns dict with an acquired lock."""
        gpus = self._allowed_tokens(self.probe.query())
        in_use = {r['gpu']['uuid'] for r in self.running.values() if r.get('gpu')}
        for g in gpus:
            if g['uuid'] in in_use:
                continue
            external = [p for p in g['procs'] if p['pid'] not in self.child_pids]
            if external:
                continue
            if g['mem_used_mb'] > self.a.gpu_busy_mem_mb:
                continue
            lock = GpuLock(self.lock_dir, g['uuid'])
            if not lock.acquire():
                continue
            return {'index': g['index'], 'uuid': g['uuid'], 'token': g['token'], 'lock': lock,
                    'child_CUDA_VISIBLE_DEVICES': g['token'], 'child_logical_device': 'cuda:0'}
        return None

    # ---- launch ----
    def _resolve_cmd(self, job: Job) -> List[str]:
        cmd = list(job.cmd)
        if job.kind == 'eval' and '<TRAIN_CKPT_DIR>' in cmd:
            tj = self.jobs[job.deps[0]]
            cmd[cmd.index('<TRAIN_CKPT_DIR>')] = os.path.join(tj.job_dir, 'ckpt')
        return cmd

    def _deps_ok(self, job: Job) -> Optional[bool]:
        """True = all deps succeeded; False = some dep failed/blocked; None = still waiting."""
        st = [self.jobs[d].status for d in job.deps]
        if any(s in ('failed', 'blocked', 'killed') for s in st):
            return False
        if all(s in ('success', 'skipped_done') for s in st):
            # eval additionally requires the checkpoint file to exist
            if job.kind == 'eval' and job.deps:
                tj = self.jobs[job.deps[0]]
                ck = os.path.join(tj.job_dir, 'ckpt', f"{job.meta['entity']}_seed{job.meta['seed']}_{job.meta['ckpt_tag']}.pt")
                if not os.path.exists(ck):
                    job.meta['blocked_reason'] = f'checkpoint missing: {ck}'
                    return False
            return True
        return None

    def _launch(self, job: Job, gpu: Optional[dict]):
        cmd = self._resolve_cmd(job)
        env = dict(os.environ, PYTHONUNBUFFERED='1',
                   OMP_NUM_THREADS=str(self.plan.threads), MKL_NUM_THREADS=str(self.plan.threads),
                   OPENBLAS_NUM_THREADS=str(self.plan.threads), NUMEXPR_NUM_THREADS=str(self.plan.threads))
        env['CUDA_VISIBLE_DEVICES'] = gpu['child_CUDA_VISIBLE_DEVICES'] if gpu else ''
        if job.kind == 'train':
            os.makedirs(job.job_dir, exist_ok=True)          # main.py writes config.yaml here
        elif job.kind == 'eval':
            os.makedirs(os.path.dirname(job.job_dir), exist_ok=True)   # eval_ckpt requires --out_dir empty: do not create/write into it
        os.makedirs(os.path.dirname(job.log_path), exist_ok=True)
        log = open(job.log_path, 'a')
        log.write(f'# launcher: {time.strftime("%Y-%m-%dT%H:%M:%S")} job={job.id} gpu={None if gpu is None else {k: gpu[k] for k in ("index", "uuid", "token")}}\n# cmd: {" ".join(cmd)}\n')
        log.flush()
        proc = subprocess.Popen(cmd, cwd=str(REPO), env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        self.child_pids.add(proc.pid)
        job.status, job.started_at = 'running', time.time()
        job.gpu = None if gpu is None else {k: gpu[k] for k in ('index', 'uuid', 'token', 'child_CUDA_VISIBLE_DEVICES', 'child_logical_device')}
        job.cmd = cmd
        self.running[job.id] = {'proc': proc, 'lock': (gpu or {}).get('lock'), 'log': log, 'gpu': gpu}
        print(f'[launch] {job.id} pid={proc.pid} gpu={job.gpu["index"] if job.gpu else "cpu"} -> {job.log_path}', flush=True)

    def _finish(self, job: Job, rec: dict):
        proc = rec['proc']
        job.exit_code, job.finished_at = proc.returncode, time.time()
        rec['log'].close()
        if rec['lock'] is not None:
            rec['lock'].release()
        self.child_pids.discard(proc.pid)
        ok = (proc.returncode == 0) and all(os.path.exists(os.path.join(job.job_dir or '.', f)) for f in job.success_files)
        job.status = 'success' if ok else 'failed'
        if ok and job.job_dir:
            mk = Path(job.job_dir) / 'SUCCESS.json'
            mk.write_text(json.dumps({'job_id': job.id, 'identity': job.identity, 'cmd': job.cmd, 'exit_code': 0,
                                      'finished_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'gpu': job.gpu}, indent=1, default=str))
            job.marker_path = str(mk)
        print(f'[{job.status}] {job.id} exit={proc.returncode} ({job.finished_at - job.started_at:.0f}s)', flush=True)
        if not ok:
            for j in self.jobs.values():
                if job.id in j.deps and j.status == 'pending':
                    j.status = 'blocked'; j.meta['blocked_reason'] = f'dependency failed: {job.id}'

    def _persist(self, path_name='queue.json', extra=None):
        self.state_dir.mkdir(parents=True, exist_ok=True)
        rec = {'manifest': self.a.manifest, 'name': self.plan.name, 'out_root': str(self.plan.out_root), 'python': self.plan.python,
               'gpus_arg': self.a.gpus, 'launcher_CUDA_VISIBLE_DEVICES': os.environ.get('CUDA_VISIBLE_DEVICES'),
               'lock_dir': self.lock_dir, 'updated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'code': self.plan.code,
               'order': self.order, 'jobs': [self.jobs[i].to_record() for i in self.order]}
        if extra:
            rec.update(extra)
        tmp = self.state_dir / (path_name + '.tmp')
        tmp.write_text(json.dumps(rec, indent=1, default=str)); os.replace(tmp, self.state_dir / path_name)

    def shutdown(self, reason='signal'):
        """Terminate only the children this launcher started; release GPU locks."""
        self._stop = True
        for jid, rec in list(self.running.items()):
            p = rec['proc']
            if p.poll() is None:
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except Exception:
                    p.terminate()
        deadline = time.time() + self.a.kill_grace
        for jid, rec in list(self.running.items()):
            p = rec['proc']
            while p.poll() is None and time.time() < deadline:
                time.sleep(0.2)
            if p.poll() is None:
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except Exception:
                    p.kill()
                p.wait()
            self.jobs[jid].status, self.jobs[jid].exit_code, self.jobs[jid].finished_at = 'killed', p.returncode, time.time()
            rec['log'].close()
            if rec['lock'] is not None:
                rec['lock'].release()
            self.child_pids.discard(p.pid)
        self.running.clear()
        self._persist(extra={'stopped': reason})

    # ---- main loop ----
    def run(self):
        def _sig(signum, frame):
            print(f'[launcher] signal {signum}: stopping children', flush=True)
            self.shutdown(f'signal {signum}')
            raise SystemExit(130)
        old = {s: signal.signal(s, _sig) for s in (signal.SIGINT, signal.SIGTERM)} if self.a.install_signal_handlers else {}
        try:
            self._persist()
            while not self._stop:
                # reap
                for jid, rec in list(self.running.items()):
                    if rec['proc'].poll() is not None:
                        self._finish(self.jobs[jid], rec); del self.running[jid]
                # launch in manifest order
                n_prior = sum(1 for jid in self.running if self.jobs[jid].kind == 'prior')
                for jid in self.order:
                    j = self.jobs[jid]
                    if j.status != 'pending' or len(self.running) >= self.a.max_parallel:
                        continue
                    ok = self._deps_ok(j)
                    if ok is False:
                        j.status = 'blocked'; continue
                    if ok is None:
                        continue
                    if j.kind == 'prior':
                        if n_prior >= self.plan.prior_workers:
                            continue
                        self._launch(j, None); n_prior += 1
                    elif j.needs_gpu:
                        gpu = self._pick_gpu()
                        if gpu is None:
                            continue
                        self._launch(j, gpu)
                    else:
                        self._launch(j, None)
                self._persist()
                pend = [i for i in self.order if self.jobs[i].status == 'pending']
                if not self.running and not pend:
                    break
                if not self.running and pend:
                    # nothing running, nothing launchable: GPUs all busy/locked -> keep waiting
                    pass
                time.sleep(self.a.poll_seconds)
        finally:
            for s, h in old.items():
                signal.signal(s, h)
        self._persist(extra={'stopped': 'done'})
        return self.summary()

    def summary(self):
        from collections import Counter
        c = Counter(j.status for j in self.jobs.values())
        return dict(c)

    def collect_eval(self):
        """Concatenate eval metrics.csv files of successful/skipped eval jobs (no selection)."""
        import pandas as pd
        rows = []
        for jid in self.order:
            j = self.jobs[jid]
            if j.kind == 'eval' and j.status in ('success', 'skipped_done') and j.job_dir and os.path.exists(os.path.join(j.job_dir, 'metrics.csv')):
                df = pd.read_csv(os.path.join(j.job_dir, 'metrics.csv')); df.insert(0, 'job_id', jid); df.insert(1, 'out_dir', j.job_dir)
                rows.append(df)
        if not rows:
            return None
        out = pd.concat(rows, ignore_index=True)
        p = self.state_dir / f'eval_summary_{time.strftime("%Y%m%d-%H%M%S")}.csv'
        out.to_csv(p, index=False)
        return str(p)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def build_parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--gpus', default='auto', help="'auto' or comma-separated physical indices/UUIDs (must be within CUDA_VISIBLE_DEVICES if set)")
    ap.add_argument('--python', default=DEFAULT_PYTHON)
    ap.add_argument('--data_root', default=DEFAULT_DATA_ROOT)
    ap.add_argument('--prior_cache_dir', default=DEFAULT_PRIOR_CACHE or None)
    ap.add_argument('--out_root', default=DEFAULT_OUT_ROOT)
    ap.add_argument('--lock_dir', default=DEFAULT_LOCK_DIR)
    ap.add_argument('--threads_per_job', type=int, default=None)
    ap.add_argument('--dataloader_workers', type=int, default=None)
    ap.add_argument('--prior_workers', type=int, default=None)
    ap.add_argument('--max_parallel', type=int, default=64)
    ap.add_argument('--gpu_busy_mem_mb', type=int, default=1000, help='a GPU with more used memory than this is treated as busy')
    ap.add_argument('--poll_seconds', type=float, default=5.0)
    ap.add_argument('--kill_grace', type=float, default=15.0)
    ap.add_argument('--dry-run', dest='dry_run', action='store_true',
                    help='expand the queue and write <out_root>/_launcher/<name>/queue_dryrun.json only; no jobs, no experiment/cache/checkpoint output')
    ap.add_argument('--resume', action='store_true', help='skip jobs whose SUCCESS marker matches config/data/code identity')
    ap.add_argument('--status', action='store_true', help='print the last persisted queue state and exit')
    ap.add_argument('--no_collect', action='store_true')
    ap.add_argument('--install_signal_handlers', type=int, default=1)
    return ap


def load_manifest(path):
    with open(path) as f:
        return yaml.safe_load(f)


JOB_CMD_HOOK = None   # tests: callable(job) -> cmd, replaces the real CLI with CPU mock jobs


def main(argv=None, probe: Optional[GpuProbe] = None):
    a = build_parser().parse_args(argv)
    manifest = load_manifest(a.manifest)
    plan = Plan(manifest, a)
    if JOB_CMD_HOOK is not None:
        for j in plan.jobs:
            j.cmd = JOB_CMD_HOOK(j)
    launcher = Launcher(plan, a, probe=probe)
    if a.status:
        p = launcher.state_dir / 'queue.json'
        if not p.exists():
            print(f'no state at {p}'); return 1
        st = json.loads(p.read_text())
        for j in st['jobs']:
            print(f"{j['status']:13s} {j['id']}  gpu={j['gpu']['index'] if j.get('gpu') else '-'}  dir={j.get('job_dir')}")
        return 0
    if a.resume:
        launcher.apply_resume()
    if a.dry_run:
        gpus = launcher._allowed_tokens(launcher.probe.query()) if launcher.probe else []
        print(f'[dry-run] manifest={a.manifest} name={plan.name} jobs={len(plan.jobs)} out_root={plan.out_root} python={plan.python}')
        print(f'[dry-run] data_root={plan.data_root} prior_cache_dir={a.prior_cache_dir or "<config default>"} lock_dir={a.lock_dir}')
        print(f'[dry-run] launcher CUDA_VISIBLE_DEVICES={os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>")} --gpus={a.gpus} '
              f'candidates={[(g["index"], g["uuid"][:12], g["mem_used_mb"], len(g["procs"])) for g in gpus]} (1 job per GPU; child sees cuda:0)')
        print(f'[dry-run] threads_per_job={plan.threads} dataloader_workers={plan.workers} prior_workers={plan.prior_workers}')
        for j in plan.jobs:
            print(f'  {j.status:12s} {j.kind:5s} {j.id}\n      deps={j.deps}\n      dir={j.job_dir}\n      log={j.log_path}\n      cmd={" ".join(j.cmd)}')
        launcher._persist(path_name='queue_dryrun.json', extra={'dry_run': True})
        print(f'[dry-run] wrote plan {launcher.state_dir / "queue_dryrun.json"} (state dir only); no process started, '
              f'no experiment/cache/checkpoint output created')
        return 0
    summ = launcher.run()
    print(f'[launcher] done: {summ}')
    if not a.no_collect:
        p = launcher.collect_eval()
        if p:
            print(f'[launcher] eval summary (no selection): {p}')
    return 0 if all(j.status in ('success', 'skipped_done') for j in plan.jobs) else 1


if __name__ == '__main__':
    sys.exit(main())
