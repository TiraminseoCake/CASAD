"""Tests for the per-server tmux wrappers and the multiserver manifests.
- manifests: disjoint train jobs, union == 120, prior/train/eval counts and dependencies
- wrappers: bash -n, dry-run argument passing, launcher exit-code preservation through tee,
  refusals (out_root inside checkout, CODE_SHA mismatch, GPU range, bad flags), mocked tmux session handling.
No training/eval is run.  Run: python -m unittest tests.test_server_wrappers -v
"""
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

import scripts.run_experiments as rx                    # noqa: E402
from scripts.run_parallel import SMD_ENTITIES            # noqa: E402

MS = os.path.join(REPO, 'scripts', 'manifests', 'multiserver')
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip()


def _plan(manifest, tmp):
    a = rx.build_parser().parse_args(['--manifest', manifest, '--out_root', os.path.join(tmp, 'out'), '--data_root', os.path.join(tmp, 'data'),
                                      '--lock_dir', os.path.join(tmp, 'locks'), '--gpus', 'auto'])
    return rx.Plan(rx.load_manifest(manifest), a)


class TestManifests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='ms_')
        os.makedirs(os.path.join(self.tmp, 'data'))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _check_deps(self, plan):
        ids = {j.id for j in plan.jobs}
        for j in plan.jobs:
            for d in j.deps:
                self.assertIn(d, ids, f'{j.id} depends on missing {d}')
            if j.kind == 'train':
                self.assertEqual(len(j.deps), 1); self.assertTrue(j.deps[0].startswith('prior/'))
            if j.kind == 'eval':
                self.assertEqual(len(j.deps), 1); self.assertTrue(j.deps[0].startswith('train/'))
        trains = [j for j in plan.jobs if j.kind == 'train']
        for t in trains:   # exactly two evals (last, best_val) per train
            ev = [j for j in plan.jobs if j.kind == 'eval' and j.deps == [t.id]]
            self.assertEqual(sorted(j.meta['ckpt_tag'] for j in ev), ['best_val', 'last'], t.id)

    def test_full_manifests_disjoint_union_120_and_counts(self):
        p4 = _plan(os.path.join(MS, 'full_server4.yaml'), self.tmp); p8 = _plan(os.path.join(MS, 'full_server8.yaml'), self.tmp)
        t4 = {j.id for j in p4.jobs if j.kind == 'train'}; t8 = {j.id for j in p8.jobs if j.kind == 'train'}
        self.assertEqual(t4 & t8, set())
        expected = {f'train/PSM/PSM/seed{s}/psm_cf_val' for s in range(4)} | {f'train/SWaT/swat/seed{s}/swat_cf_val' for s in range(4)} | \
                   {f'train/SMD/{e}/seed{s}/smd_cf_val' for e in SMD_ENTITIES for s in range(4)}
        self.assertEqual(t4 | t8, expected); self.assertEqual(len(t4 | t8), 120)
        self.assertEqual(len(t4), 4 + 8 * 4); self.assertEqual(len(t8), 4 + 20 * 4)
        kinds = lambda p: {k: sum(1 for j in p.jobs if j.kind == k) for k in ('prior', 'train', 'eval')}
        k4, k8 = kinds(p4), kinds(p8)
        self.assertEqual((k4['prior'] + k8['prior'], k4['train'] + k8['train'], k4['eval'] + k8['eval']), (30, 120, 240))
        self._check_deps(p4); self._check_deps(p8)
        # server8 queue order: all SWaT jobs before any SMD job; SMD entities explicit and fixed order
        ids8 = [j.id for j in p8.jobs if j.kind == 'train']
        self.assertTrue(all('SWaT' in i for i in ids8[:4])); self.assertTrue(all('SMD' in i for i in ids8[4:]))
        ents8 = [i.split('/')[2] for i in ids8 if '/SMD/' in i]
        self.assertEqual(list(dict.fromkeys(ents8)), SMD_ENTITIES[8:])
        ents4 = [i.split('/')[2] for i in [j.id for j in p4.jobs if j.kind == 'train'] if '/SMD/' in i]
        self.assertEqual(list(dict.fromkeys(ents4)), SMD_ENTITIES[:8])
        for m in ('full_server4.yaml', 'full_server8.yaml', 'pilot_server4.yaml', 'pilot_server8.yaml'):
            self.assertNotIn('entities: all', open(os.path.join(MS, m)).read())

    def test_pilot_manifests(self):
        p4 = _plan(os.path.join(MS, 'pilot_server4.yaml'), self.tmp); p8 = _plan(os.path.join(MS, 'pilot_server8.yaml'), self.tmp)
        t4 = {j.id for j in p4.jobs if j.kind == 'train'}; t8 = {j.id for j in p8.jobs if j.kind == 'train'}
        self.assertEqual(t4, {'train/PSM/PSM/seed0/psm_cf_val', 'train/SMD/machine-1-1/seed0/smd_cf_val'})
        self.assertEqual(t8, {'train/SWaT/swat/seed0/swat_cf_val'})
        self.assertEqual(t4 & t8, set()); self._check_deps(p4); self._check_deps(p8)
        for p in (p4, p8):
            for j in p.jobs:
                if j.kind == 'train':
                    self.assertNotIn('SOLVER.MAX_EPOCH', j.cmd)             # epochs from config (80), never overridden here
                if j.kind == 'eval':
                    self.assertEqual(j.cmd[j.cmd.index('--calibrate') + 1], 'cfg'); self.assertEqual(j.cmd[j.cmd.index('--cf') + 1], 'both')
        swat = [j for j in p8.jobs if j.kind == 'train'][0]; self.assertIn('DATA.EXPECTED_N', swat.cmd); self.assertEqual(swat.cmd[swat.cmd.index('DATA.EXPECTED_N') + 1], '51')


class WrapperBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='wrap_')
        self.out = os.path.join(self.tmp, 'runs', 'cfval', 'server4'); self.data = os.path.join(self.tmp, 'data'); os.makedirs(self.data)
        self.env = os.path.join(self.tmp, 'server4.env')
        self.write_env()
        self.bin = os.path.join(self.tmp, 'bin'); os.makedirs(self.bin)
        self.tmux_log = os.path.join(self.tmp, 'tmux_calls.txt'); self.sessions = os.path.join(self.tmp, 'sessions.txt'); open(self.sessions, 'w').close()
        fake_tmux = f'''#!/usr/bin/env bash
echo "$@" >> "{self.tmux_log}"
case "$1" in
  has-session) shift; [ "$1" = "-t" ] && grep -qx -- "$2" "{self.sessions}" && exit 0; exit 1 ;;
  new-session) while [ $# -gt 0 ]; do if [ "$1" = "-s" ]; then echo "$2" >> "{self.sessions}"; fi; shift; done; exit 0 ;;
  *) exit 0 ;;
esac
'''
        p = os.path.join(self.bin, 'tmux'); open(p, 'w').write(fake_tmux); os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_env(self, **over):
        vals = dict(PICAAD_PYTHON=sys.executable, PICAAD_DATA_ROOT=self.data, PICAAD_PRIOR_CACHE=os.path.join(self.tmp, 'cache'),
                    PICAAD_OUT_ROOT=self.out, PICAAD_LOCK_DIR=os.path.join(self.tmp, 'locks'), PICAAD_GPUS='0,1,2,3', PICAAD_CAMPAIGN='cfval',
                    PICAAD_CODE_SHA=HEAD, PICAAD_THREADS_PER_JOB='2', PICAAD_DATALOADER_WORKERS='0', PICAAD_PRIOR_WORKERS='1')
        vals.update(over)
        with open(self.env, 'w') as f:
            for k, v in vals.items():
                f.write(f'{k}={v}\n')

    def run_wrapper(self, *args, script='run_4gpu.sh', env_extra=None, fake_tmux=True):
        env = dict(os.environ); env.pop('CUDA_VISIBLE_DEVICES', None)
        if fake_tmux:
            env['PATH'] = self.bin + os.pathsep + env['PATH']
        env.update(env_extra or {})
        r = subprocess.run(['bash', os.path.join(REPO, 'scripts', 'servers', script), *args], cwd=REPO, env=env, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr


class TestWrappers(WrapperBase):
    def test_bash_syntax(self):
        for s in ('common.sh', 'run_4gpu.sh', 'run_8gpu.sh'):
            self.assertEqual(subprocess.run(['bash', '-n', os.path.join(REPO, 'scripts', 'servers', s)]).returncode, 0, s)

    def test_dry_run_default_passes_arguments_and_writes_plan_only(self):
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env)
        self.assertEqual(rc, 0, out)
        self.assertIn('gpus=0,1,2,3 (one job per GPU', out); self.assertIn('--gpus', out); self.assertIn('pilot_server4.yaml', out); self.assertIn('--dry-run', out)
        self.assertIn(f'--out_root {self.out}', out); self.assertIn('--prior_cache_dir', out); self.assertIn('tmux session=picaad_cfval_server4_pilot', out)
        self.assertTrue(os.path.exists(os.path.join(self.out, '_launcher', 'cfval_pilot_server4', 'queue_dryrun.json')))
        self.assertEqual(sorted(os.listdir(self.out)), ['_launcher'])                       # plan + wrapper log only
        self.assertFalse(os.path.exists(self.tmux_log))                                     # dry-run never touches tmux
        # run_8gpu.sh accepts indices 0..7; on this (possibly 4-GPU) machine the launcher validates the list against real GPUs,
        # so use a subset that exists everywhere for the dry-run and check the range validation separately.
        rc8, out8 = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--gpus', '0,1', '--out-root', self.out.replace('server4', 'server8'), script='run_8gpu.sh')
        self.assertEqual(rc8, 0, out8); self.assertIn('pilot_server8.yaml', out8); self.assertIn('gpus=0,1 (one job per GPU', out8)
        self.assertIn('picaad_cfval_server8_pilot', out8)
        rc9, out9 = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--gpus', '0,8', '--out-root', self.out.replace('server4', 'server8'), script='run_8gpu.sh')
        self.assertEqual(rc9, 2); self.assertIn('exceeds', out9)                                   # wrapper range check for the 8-GPU server

    def test_launcher_exit_code_preserved_through_tee(self):
        fake = os.path.join(self.tmp, 'fake_launcher.sh')
        open(fake, 'w').write('#!/usr/bin/env bash\necho "fake launcher args: $*"\nexit 3\n'); os.chmod(fake, 0o755)
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--execute', '--no-tmux', env_extra={'PICAAD_LAUNCHER_OVERRIDE': fake})
        self.assertEqual(rc, 3, out); self.assertIn('fake launcher args', out)
        log = os.path.join(self.out, '_launcher', 'picaad_cfval_server4_pilot.log')
        self.assertTrue(os.path.exists(log)); self.assertIn('fake launcher args', open(log).read())
        rc0, _ = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--execute', '--no-tmux', '--resume',
                                  env_extra={'PICAAD_LAUNCHER_OVERRIDE': fake.replace('fake_launcher.sh', 'fake_launcher.sh')})
        self.assertEqual(rc0, 3)
        rc_r, out_r = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--execute', '--no-tmux', '--resume', env_extra={'PICAAD_LAUNCHER_OVERRIDE': fake})
        self.assertIn('--resume', out_r)

    def test_refusals(self):
        self.write_env(PICAAD_OUT_ROOT=os.path.join(REPO, 'results', 'experiments', 'x'))   # inside checkout
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env); self.assertEqual(rc, 2, out[-800:]); self.assertIn('inside the Git checkout', out)
        self.write_env(PICAAD_CODE_SHA='0000000'); rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env); self.assertEqual(rc, 2); self.assertIn('does not match', out)
        self.write_env(PICAAD_CODE_SHA=''); rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env); self.assertEqual(rc, 2); self.assertIn('PICAAD_CODE_SHA', out)
        self.write_env()
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--gpus', '0,4'); self.assertEqual(rc, 2); self.assertIn('exceeds', out)
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--gpus', '0,1,2,3,4,5,6,7'); self.assertEqual(rc, 2)
        rc, out = self.run_wrapper('--phase', 'nightly', '--env', self.env); self.assertEqual(rc, 2)
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--resume'); self.assertEqual(rc, 2); self.assertIn('--resume only', out)
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--bogus'); self.assertEqual(rc, 2)
        self.assertFalse(os.path.exists(self.out))                                          # refused runs create nothing

    def test_tmux_session_named_and_duplicate_refused(self):
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--execute')
        self.assertEqual(rc, 0, out)
        calls = open(self.tmux_log).read()
        self.assertIn('has-session -t picaad_cfval_server4_pilot', calls); self.assertIn('new-session -d -s picaad_cfval_server4_pilot', calls)
        self.assertIn('--no-tmux', calls); self.assertIn('--execute', calls); self.assertIn('--code-sha', calls); self.assertIn(HEAD, calls)   # %q-escaped inner command
        rc2, out2 = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--execute')
        self.assertEqual(rc2, 2); self.assertIn('already exists', out2)
        rc3, out3 = self.run_wrapper('--phase', 'full', '--env', self.env, '--execute')     # different phase -> different session
        self.assertEqual(rc3, 0, out3); self.assertIn('picaad_cfval_server4_full', open(self.sessions).read())
        rc4, out4 = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--execute', '--campaign', 'cfval2')
        self.assertEqual(rc4, 0); self.assertIn('picaad_cfval2_server4_pilot', open(self.sessions).read())

    def test_status_mode_runs_launcher_status(self):
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env)          # creates plan
        rc, out = self.run_wrapper('--phase', 'pilot', '--env', self.env, '--status')
        self.assertIn('--status', out); self.assertIn('no state at', out)          # only a dry-run plan exists, no queue.json yet
        self.assertEqual(rc, 1)                                                    # launcher's own exit code preserved (1 = no state)


if __name__ == '__main__':
    unittest.main()
