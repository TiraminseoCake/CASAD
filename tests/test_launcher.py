"""Launcher tests: queue/dependency, GPU assignment with a mocked probe, cross-launcher lock,
external-process avoidance, failure propagation, resume, dry-run, child cleanup, prior-cache lock.
All jobs are CPU mock processes. Run: python -m unittest tests.test_launcher -v
"""
import fcntl
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

import numpy as np
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

import scripts.run_experiments as rx   # noqa: E402

PY = sys.executable
FAKE_GPUS = [
    {'index': 0, 'uuid': 'GPU-aaaa0000', 'mem_used_mb': 15, 'mem_total_mb': 49140, 'procs': []},
    {'index': 1, 'uuid': 'GPU-bbbb1111', 'mem_used_mb': 15, 'mem_total_mb': 49140, 'procs': []},
]


class FakeProbe(rx.GpuProbe):
    def __init__(self, gpus):
        self.gpus = gpus
    def query(self):
        return [dict(g, procs=list(g['procs'])) for g in self.gpus]


# ---- CPU mock jobs (stand-ins for main.py / eval_ckpt.py; they only create the files the launcher checks) ----
MOCK_TRAIN = r'''
import os, sys, time, json
run_dir, ent, seed, sleep_s, rc = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
t0 = time.time(); time.sleep(sleep_s)
os.makedirs(os.path.join(run_dir, 'ckpt'), exist_ok=True)
json.dump({'start': t0, 'end': time.time(), 'cvd': os.environ.get('CUDA_VISIBLE_DEVICES')}, open(os.path.join(run_dir, 'mock_train.json'), 'w'))
if rc != 0: sys.exit(rc)
for tag in ('best_val', 'last'):
    open(os.path.join(run_dir, 'ckpt', f'{ent}_seed{seed}_{tag}.pt'), 'wb').write(b'ckpt')
'''
MOCK_EVAL = r'''
import os, sys, time, json
ckpt_dir, out_dir, ent, seed, tag, sleep_s = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], float(sys.argv[6])
if os.path.exists(out_dir) and os.listdir(out_dir): sys.exit(3)      # eval_ckpt refuses a non-empty out_dir
ck = os.path.join(ckpt_dir, f'{ent}_seed{seed}_{tag}.pt')
if not os.path.exists(ck): sys.exit(4)
t0 = time.time(); time.sleep(sleep_s); os.makedirs(out_dir, exist_ok=True)
open(os.path.join(out_dir, 'metrics.csv'), 'w').write('variant,AUC-PR\nA_off,0.5\nA_on,0.6\n')
json.dump({'ckpt': ck, 'start': t0, 'end': time.time(), 'cvd': os.environ.get('CUDA_VISIBLE_DEVICES')}, open(os.path.join(out_dir, 'provenance.json'), 'w'))
'''


def make_hook(sleep_s=0.3, fail_train_seeds=()):
    def hook(job):
        if job.kind == 'prior':
            return [PY, '-c', 'print("prior ok")']
        if job.kind == 'train':
            rc = 1 if job.meta['seed'] in fail_train_seeds else 0
            return [PY, '-c', MOCK_TRAIN, job.job_dir, job.meta['entity'], str(job.meta['seed']), str(sleep_s), str(rc)]
        if job.kind == 'eval':
            return [PY, '-c', MOCK_EVAL, '<TRAIN_CKPT_DIR>', job.job_dir, job.meta['entity'], str(job.meta['seed']), job.meta['ckpt_tag'], str(sleep_s)]
        raise AssertionError(job.kind)
    return hook


class LauncherTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='launcher_')
        self.data_root = os.path.join(self.tmp, 'data'); os.makedirs(os.path.join(self.data_root, 'PSM'))
        np.savez(os.path.join(self.data_root, 'PSM', 'PSM.npz'), train=np.zeros((5, 2), np.float32), test=np.zeros((5, 2), np.float32), label=np.zeros(5, np.int32))
        self.out_root = os.path.join(self.tmp, 'out'); self.lock_dir = os.path.join(self.tmp, 'locks')
        self.manifest = os.path.join(self.tmp, 'm.yaml')
        yaml.safe_dump({'name': 'tpilot', 'defaults': {'threads_per_job': 1, 'prior_workers': 1, 'eval': {'ckpt_tags': ['last', 'best_val'], 'cf': 'both', 'calibrate': 'cfg'}},
                        'train': [{'dataset': 'PSM', 'config': 'scripts/configs/psm_cf_val.yaml', 'input_dir': 'PSM', 'entities': ['PSM'], 'seeds': [0, 1, 2]}]},
                       open(self.manifest, 'w'))
        self.base_argv = ['--manifest', self.manifest, '--out_root', self.out_root, '--data_root', self.data_root, '--lock_dir', self.lock_dir,
                          '--poll_seconds', '0.1', '--kill_grace', '2', '--install_signal_handlers', '0', '--no_collect']
        rx.JOB_CMD_HOOK = make_hook()
        self._env = mock.patch.dict(os.environ, {}, clear=False); self._env.start()
        os.environ.pop('CUDA_VISIBLE_DEVICES', None)

    def tearDown(self):
        rx.JOB_CMD_HOOK = None; self._env.stop(); shutil.rmtree(self.tmp, ignore_errors=True)

    def run_launcher(self, extra=(), gpus=FAKE_GPUS, argv_gpus='auto'):
        return rx.main(self.base_argv + ['--gpus', argv_gpus] + list(extra), probe=FakeProbe(gpus))

    def state(self, name='queue.json'):
        return json.load(open(os.path.join(self.out_root, '_launcher', 'tpilot', name)))


class TestPlan(LauncherTestBase):
    def test_expansion_order_and_paths(self):
        a = rx.build_parser().parse_args(self.base_argv + ['--gpus', 'auto'])
        plan = rx.Plan(rx.load_manifest(self.manifest), a)
        ids = [j.id for j in plan.jobs]
        self.assertEqual(ids[0], 'prior/PSM/PSM/psm_cf_val')
        self.assertEqual(ids[1:4], ['train/PSM/PSM/seed0/psm_cf_val', 'eval/PSM/PSM/seed0/psm_cf_val/eval/last', 'eval/PSM/PSM/seed0/psm_cf_val/eval/best_val'])
        self.assertEqual(len(ids), 1 + 3 * 3)
        tj = plan.jobs[1]; ej = plan.jobs[2]
        self.assertEqual(tj.deps, [ids[0]]); self.assertEqual(ej.deps, [tj.id])
        self.assertIn('RESULT_DIR_LITERAL', tj.cmd); self.assertIn('main.py', tj.cmd); self.assertNotIn('SOLVER.MAX_EPOCH', tj.cmd)   # epochs from config
        self.assertIn(os.path.join(self.data_root, 'PSM'), tj.cmd)
        self.assertTrue(tj.job_dir.endswith('PSM/PSM/seed0/psm_cf_val/attempt1'))
        self.assertTrue(ej.job_dir.endswith('eval/last/attempt1'))
        self.assertEqual(os.path.dirname(ej.log_path), os.path.dirname(ej.job_dir))        # log beside, not inside, --out_dir
        self.assertIn('scripts/eval_ckpt.py', ej.cmd); self.assertIn('--calibrate', ej.cmd); self.assertEqual(ej.cmd[ej.cmd.index('--calibrate') + 1], 'cfg')
        self.assertEqual(ej.cmd[ej.cmd.index('--cf') + 1], 'both')
        src = open(rx.__file__).read()
        self.assertNotIn("'scripts/aggregate_best_epoch.py'", src)      # never invoked (only mentioned in the docstring)
        self.assertNotIn('_final_eval(', src); self.assertNotIn('import main', src)


class TestRun(LauncherTestBase):
    def test_two_gpus_one_job_each_and_dependencies(self):
        rc = self.run_launcher()
        self.assertEqual(rc, 0)
        st = self.state(); statuses = {j['id']: j['status'] for j in st['jobs']}
        self.assertTrue(all(s == 'success' for s in statuses.values()), statuses)
        # per-GPU intervals must not overlap (1 job per GPU); each child saw a single logical device
        per_gpu = {}
        for j in st['jobs']:
            if j['kind'] == 'prior': continue
            f = os.path.join(j['job_dir'], 'mock_train.json' if j['kind'] == 'train' else 'provenance.json')
            r = json.load(open(f)); self.assertEqual(r['cvd'], j['gpu']['token']); per_gpu.setdefault(j['gpu']['uuid'], []).append((r['start'], r['end']))
            self.assertEqual(j['gpu']['child_logical_device'], 'cuda:0')
        self.assertEqual(set(per_gpu), {'GPU-aaaa0000', 'GPU-bbbb1111'})
        for iv in per_gpu.values():
            iv.sort()
            for (s1, e1), (s2, e2) in zip(iv, iv[1:]): self.assertLessEqual(e1, s2 + 1e-3)
        # eval ran only after its train success and used that attempt's ckpt dir
        for j in st['jobs']:
            if j['kind'] == 'eval':
                self.assertIn('/attempt1/ckpt', json.load(open(os.path.join(j['job_dir'], 'provenance.json')))['ckpt'])
                self.assertTrue(os.path.exists(os.path.join(j['job_dir'], 'SUCCESS.json')))
                self.assertTrue(os.path.exists(j['log_path'])); self.assertFalse(os.path.exists(os.path.join(j['job_dir'], os.path.basename(j['log_path']))))
        self.assertTrue(all(os.path.exists(os.path.join(j['job_dir'], 'SUCCESS.json')) for j in st['jobs'] if j['kind'] == 'train'))

    def test_external_process_and_other_launcher_lock_are_respected(self):
        gpus = [dict(FAKE_GPUS[0], procs=[{'pid': 999999, 'uid': 0}]), dict(FAKE_GPUS[1])]
        os.makedirs(self.lock_dir, exist_ok=True)
        held = open(os.path.join(self.lock_dir, 'gpu_GPU-bbbb1111.lock'), 'a+'); fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)   # "another launcher"
        a = rx.build_parser().parse_args(self.base_argv + ['--gpus', 'auto']); plan = rx.Plan(rx.load_manifest(self.manifest), a)
        L = rx.Launcher(plan, a, probe=FakeProbe(gpus))
        self.assertIsNone(L._pick_gpu())                       # gpu0 external process, gpu1 locked elsewhere
        fcntl.flock(held, fcntl.LOCK_UN); held.close()
        g = L._pick_gpu(); self.assertEqual(g['index'], 1); g['lock'].release()
        # full run: everything must go through gpu1 only, sequentially
        rc = self.run_launcher(gpus=gpus); self.assertEqual(rc, 0)
        st = self.state(); self.assertTrue(all(j['gpu']['index'] == 1 for j in st['jobs'] if j['gpu']))

    def test_gpus_explicit_and_env_restriction(self):
        with self.assertRaises(SystemExit):
            self.run_launcher(argv_gpus='5')
        os.environ['CUDA_VISIBLE_DEVICES'] = '1'
        rc = self.run_launcher(argv_gpus='auto'); self.assertEqual(rc, 0)
        st = self.state(); self.assertTrue(all(j['gpu']['index'] == 1 and j['gpu']['token'] == '1' for j in st['jobs'] if j['gpu']))
        with self.assertRaises(SystemExit):
            self.run_launcher(argv_gpus='0')                   # outside the launcher's own CUDA_VISIBLE_DEVICES

    def test_failure_blocks_dependents_and_keeps_partial_output(self):
        rx.JOB_CMD_HOOK = make_hook(fail_train_seeds=(1,))
        rc = self.run_launcher(); self.assertEqual(rc, 1)
        st = self.state(); statuses = {j['id']: j['status'] for j in st['jobs']}
        self.assertEqual(statuses['train/PSM/PSM/seed1/psm_cf_val'], 'failed')
        self.assertEqual(statuses['eval/PSM/PSM/seed1/psm_cf_val/eval/last'], 'blocked'); self.assertEqual(statuses['eval/PSM/PSM/seed1/psm_cf_val/eval/best_val'], 'blocked')
        self.assertEqual(statuses['train/PSM/PSM/seed0/psm_cf_val'], 'success'); self.assertEqual(statuses['eval/PSM/PSM/seed2/psm_cf_val/eval/last'], 'success')
        failed_dir = [j['job_dir'] for j in st['jobs'] if j['id'] == 'train/PSM/PSM/seed1/psm_cf_val'][0]
        self.assertTrue(os.path.exists(os.path.join(failed_dir, 'mock_train.json')))      # partial output preserved
        self.assertFalse(os.path.exists(os.path.join(failed_dir, 'SUCCESS.json')))

    def test_resume_skips_only_matching_completed_jobs_and_uses_new_attempts(self):
        self.assertEqual(self.run_launcher(), 0)
        rc = self.run_launcher(extra=['--resume']); self.assertEqual(rc, 0)
        st = self.state(); self.assertTrue(all(j['status'] == 'skipped_done' for j in st['jobs'] if j['kind'] != 'prior'))
        self.assertFalse(os.path.exists(os.path.join(self.out_root, 'PSM', 'PSM', 'seed0', 'psm_cf_val', 'attempt2')))
        # change the data identity -> not skipped, new attempt dirs, old attempt untouched
        np.savez(os.path.join(self.data_root, 'PSM', 'PSM.npz'), train=np.ones((5, 2), np.float32), test=np.zeros((5, 2), np.float32), label=np.zeros(5, np.int32))
        rc = self.run_launcher(extra=['--resume']); self.assertEqual(rc, 0)
        st = self.state(); self.assertTrue(all(j['status'] == 'success' for j in st['jobs'] if j['kind'] != 'prior'))
        self.assertTrue(all(j['job_dir'].endswith('attempt2') for j in st['jobs'] if j['kind'] != 'prior'))
        self.assertTrue(os.path.exists(os.path.join(self.out_root, 'PSM', 'PSM', 'seed0', 'psm_cf_val', 'attempt1', 'SUCCESS.json')))
        # a failed attempt leaves its dir; a fresh (non-resume) rerun uses attempt3 and never overwrites attempt2
        rx.JOB_CMD_HOOK = make_hook(fail_train_seeds=(0,))
        self.run_launcher()
        self.assertTrue(os.path.exists(os.path.join(self.out_root, 'PSM', 'PSM', 'seed0', 'psm_cf_val', 'attempt3')))
        self.assertTrue(os.path.exists(os.path.join(self.out_root, 'PSM', 'PSM', 'seed0', 'psm_cf_val', 'attempt2', 'SUCCESS.json')))

    def test_dry_run_writes_plan_json_only(self):
        """dry-run starts no job and creates no experiment/cache/checkpoint output; it only records
        the expanded plan in <out_root>/_launcher/<name>/queue_dryrun.json."""
        rc = self.run_launcher(extra=['--dry-run']); self.assertEqual(rc, 0)
        self.assertEqual(sorted(os.listdir(self.out_root)), ['_launcher'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.out_root, '_launcher', 'tpilot'))), ['queue_dryrun.json'])
        st = self.state('queue_dryrun.json'); self.assertTrue(st['dry_run']); self.assertEqual(len(st['jobs']), 10)
        self.assertTrue(all(j['status'] == 'pending' for j in st['jobs']))

    def test_shutdown_terminates_only_own_children_and_releases_locks(self):
        rx.JOB_CMD_HOOK = make_hook(sleep_s=30)
        a = rx.build_parser().parse_args(self.base_argv + ['--gpus', 'auto']); plan = rx.Plan(rx.load_manifest(self.manifest), a)
        for j in plan.jobs: j.cmd = rx.JOB_CMD_HOOK(j)
        L = rx.Launcher(plan, a, probe=FakeProbe(FAKE_GPUS))
        t = threading.Thread(target=L.run, daemon=True); t.start()
        deadline = time.time() + 10
        while time.time() < deadline and not any(self_j.kind == 'train' for self_j in [L.jobs[i] for i in L.running]): time.sleep(0.1)
        running = [L.running[i]['proc'] for i in list(L.running)]
        self.assertTrue(running)
        L.shutdown('test'); t.join(5)
        self.assertTrue(all(p.poll() is not None for p in running))
        self.assertTrue(any(j.status == 'killed' for j in L.jobs.values()))
        lock = rx.GpuLock(self.lock_dir, 'GPU-aaaa0000'); self.assertTrue(lock.acquire()); lock.release()


class TestPriorCacheLock(unittest.TestCase):
    def test_concurrent_same_key_builds_once_atomically(self):
        from config import get_cfg_defaults
        import model.build as mb
        tmp = tempfile.mkdtemp(prefix='priorlock_')
        try:
            cfg = get_cfg_defaults(); cfg.PICAAD.PRIOR.CACHE_DIR = os.path.join(tmp, 'cache'); cfg.freeze()
            train = np.random.default_rng(0).normal(size=(50, 4)).astype(np.float32)
            calls = []
            def slow_build(cfg_, tn):
                calls.append(1); time.sleep(0.5)
                w = np.ones((cfg_.PICAAD.TAU_MAX, 4, 4), np.float32); return w, w
            results = []
            with mock.patch.object(mb, 'build_causal_prior', side_effect=slow_build):
                ths = [threading.Thread(target=lambda: results.append(mb.build_causal_prior_cached(cfg, train, 'ent')[0].sum())) for _ in range(4)]
                [t.start() for t in ths]; [t.join() for t in ths]
            self.assertEqual(len(calls), 1); self.assertEqual(len(results), 4); self.assertEqual(len(set(results)), 1)
            files = os.listdir(cfg.PICAAD.PRIOR.CACHE_DIR)
            self.assertEqual([f for f in files if f.endswith('.npz')].__len__(), 1); self.assertFalse(any('tmp' in f for f in files))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
