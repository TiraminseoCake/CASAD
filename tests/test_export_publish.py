"""Tests for scripts/export_results.py and scripts/publish_results.sh using mock launcher results and a local
temporary Git origin. No real training/eval, no network.  Run: python -m unittest tests.test_export_publish -v"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

import numpy as np
import pandas as pd
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
import scripts.export_results as ex   # noqa: E402

PY = sys.executable


def _cfg(gamma=1.0):
    from config import get_cfg_defaults
    c = get_cfg_defaults(); c.merge_from_file(os.path.join(REPO, 'scripts/configs/psm_cf_val.yaml')); c.PICAAD.SCORING.SCORE_GAMMA = gamma
    c.DATA.INPUT_DIR = '/home/someone/data/PSM'; c.RESULT_DIR = '/home/tester/runs/server4/attempt1'; return c.dump()


def make_mock_out_root(root, server, jobs, code='abc1234def', failed=(), duplicate_for=None, gamma=1.0):
    """jobs: list of (dataset, entity, seed). Creates queue.json, train attempt dirs (SUCCESS, ckpt, val csv) and eval attempts."""
    home_path = f'/home/tester/runs/{server}'   # a personal absolute path that must be redacted
    qjobs = []
    for ds, ent, seed in jobs:
        cfg_stem = {'PSM': 'psm_cf_val', 'SMD': 'smd_cf_val', 'SWaT': 'swat_cf_val'}[ds]
        base = os.path.join(root, ds, ent, f'seed{seed}', cfg_stem); tdir = os.path.join(base, 'attempt1'); os.makedirs(os.path.join(tdir, 'ckpt'), exist_ok=True)
        tid = f'train/{ds}/{ent}/seed{seed}/{cfg_stem}'; pid = f'prior/{ds}/{ent}/{cfg_stem}'
        ident = {'config': f'scripts/configs/{cfg_stem}.yaml', 'config_sha256': 'c' * 64, 'data_sha256': 'd' * 64, 'code': {'commit': code, 'tracked_diff_sha256': 'e' * 64},
                 'python': PY, 'entity': ent, 'seed': seed, 'input_dir': f'/home/tester/data/{ds}', 'val_enabled': True, 'dataloader_workers': 0, 'epochs': None, 'expected_n': None, 'prior_cache_dir': '<cfg>'}
        fail = (ds, ent, seed) in failed
        qjobs.append({'id': pid, 'kind': 'prior', 'status': 'success', 'deps': [], 'job_dir': None, 'gpu': None, 'meta': {'dataset': ds, 'entity': ent}, 'identity': {}, 'exit_code': 0, 'started_at': 1.0, 'finished_at': 2.0, 'log_path': f'{home_path}/prior.log'})
        qjobs.append({'id': tid, 'kind': 'train', 'status': 'failed' if fail else 'success', 'deps': [pid], 'job_dir': tdir, 'gpu': {'index': 0, 'uuid': 'GPU-x', 'token': '0'},
                      'meta': {'dataset': ds, 'entity': ent, 'seed': seed, 'config': ident['config'], 'val_enabled': True}, 'identity': ident, 'exit_code': 1 if fail else 0,
                      'started_at': 10.0, 'finished_at': 20.0, 'log_path': os.path.join(tdir, 'launcher_run.log')})
        open(os.path.join(tdir, 'launcher_run.log'), 'w').write(f'# cmd: python main.py RESULT_DIR {home_path}\n')
        open(os.path.join(tdir, 'config.yaml'), 'w').write(_cfg(gamma))
        pd.DataFrame({'epoch': [1, 2, 3], 'val_pred_mae': [0.9, 0.8, 0.85], 'best_epoch_so_far': [1, 2, 2], 'best_val_mae_so_far': [0.9, 0.8, 0.8]}).to_csv(os.path.join(tdir, f'{ent}_seed{seed}_val_metrics.csv'), index=False)
        if not fail:
            for tag in ('best_val', 'last'):
                open(os.path.join(tdir, 'ckpt', f'{ent}_seed{seed}_{tag}.pt'), 'wb').write(os.urandom(64))
            json.dump({'job_id': tid, 'identity': ident, 'cmd': ['python', 'main.py', 'RESULT_DIR', tdir], 'exit_code': 0, 'gpu': {'index': 0}}, open(os.path.join(tdir, 'SUCCESS.json'), 'w'))
        for tag, epoch in (('last', 3), ('best_val', 2)):
            ebase = os.path.join(base, 'eval', tag); edir = os.path.join(ebase, 'attempt1'); os.makedirs(edir, exist_ok=True)
            eid = f'eval/{ds}/{ent}/seed{seed}/{cfg_stem}/eval/{tag}'
            st = 'blocked' if fail else 'success'
            qjobs.append({'id': eid, 'kind': 'eval', 'status': st, 'deps': [tid], 'job_dir': edir, 'gpu': {'index': 1, 'uuid': 'GPU-y', 'token': '1'},
                          'meta': {'dataset': ds, 'entity': ent, 'seed': seed, 'config': ident['config'], 'ckpt_tag': tag, 'train_job': tid, **({'blocked_reason': 'dependency failed'} if fail else {})},
                          'identity': {'train_identity': ident, 'ckpt_tag': tag, 'cf': 'both', 'calibrate': 'cfg'}, 'exit_code': None if fail else 0, 'started_at': 30.0, 'finished_at': 40.0, 'log_path': f'{ebase}/attempt1.log'})
            if fail:
                continue
            rows = []
            for variant, kind, mode in (('A_off', 'fusion', 'raw'), ('A_on', 'fusion', 'raw'), ('P_raw', 'diagnostic', 'raw'), ('CF_raw', 'diagnostic', 'raw')):
                rows.append({'entity': ent, 'seed': seed, 'ckpt_format': 'val', 'epoch': epoch, 'variant': variant, 'kind': kind, 'scoring_mode': mode, 'formula': variant,
                             'AUC-PR': 0.5 + 0.01 * seed + (0.02 if variant == 'A_on' else 0), 'AUC-ROC': 0.8, 'VUS-PR': 0.6, 'VUS-ROC': 0.85, 'Standard-F1': 0.55, 'PA-F1': 0.9, 'Event-based-F1': 0.7, 'R-based-F1': 0.4, 'Affiliation-F': 0.8})
            pd.DataFrame(rows).to_csv(os.path.join(edir, 'metrics.csv'), index=False)
            np.savez(os.path.join(edir, 'scores.npz'), A_off=np.zeros(5), A_on=np.ones(5))
            prov = {'checkpoint': {'path': os.path.join(tdir, 'ckpt', f'{ent}_seed{seed}_{tag}.pt'), 'sha256': 'f' * 64, 'protocol': 'val_pred_mae_v2', 'val_mae': 0.8, 'prior_cache_key': f'{ds}_{ent}_pcmci_val0.2_b100_abc',
                                   'split_info': {'split_id': 'val0.2_b100'}, 'entity': ent, 'seed': seed, 'format': 'val', 'payload_epoch': epoch, 'payload_current_epoch': epoch, 'code_fingerprint_in_ckpt': {'commit': code}, 'api_token': 'SECRET-VALUE'},
                    'restore': {'restored_epoch': epoch, 'epoch_source': 'payload.current_epoch', 'warmup_ramp': 1.0, 'flags': {'has_te_prior': True}},
                    'data': {'npz_path': f'/home/tester/data/{ds}/{ent}.npz', 'npz_sha256': 'd' * 64, 'shapes': {'train': [100, 6]}, 'split_id': 'val0.2_b100', 'fit_protocol': 'train_sub_val', 'dims': {'N_data': 6}},
                    'scoring': {'calibrate': False, 'gamma': gamma, 'A_off': 'P_raw + C_raw'}, 'cf': {'top_k': 15, 'gamma': gamma, 'sources': [0, 1]}, 'calibration': {'enabled': False},
                    'evaluator': {'USE_MEDIAN_VUS_WINDOW': True, 'sliding_window_used': 20, 'VUS_VERSION': 'opt', 'VUS_THRE': 250}, 'forward_passes': {'test_base_forward': 1},
                    'native_parity': None, 'state_unchanged': True, 'device': 'cuda', 'torch_version': '2.6.0', 'elapsed_s': 3.0, 'finished_at': 'now', 'code_fingerprint': {'commit': code}}
            json.dump(prov, open(os.path.join(edir, 'provenance.json'), 'w'))
            open(os.path.join(edir, 'config_resolved.yaml'), 'w').write(_cfg(gamma))
            open(f'{ebase}/attempt1.log', 'w').write(f'log {home_path}\n')
            json.dump({'job_id': eid, 'identity': qjobs[-1]['identity'], 'cmd': [], 'exit_code': 0}, open(os.path.join(edir, 'SUCCESS.json'), 'w'))
            if duplicate_for == (ds, ent, seed) and tag == 'last':
                d2 = os.path.join(ebase, 'attempt2'); shutil.copytree(edir, d2)   # a second successful attempt (not referenced by queue.json)
    qdir = os.path.join(root, '_launcher', f'cfval_pilot_{server}'); os.makedirs(qdir, exist_ok=True)
    json.dump({'name': f'cfval_pilot_{server}', 'manifest': f'{home_path}/manifest.yaml', 'out_root': root, 'python': PY, 'gpus_arg': 'auto', 'lock_dir': '/tmp/x',
               'launcher_CUDA_VISIBLE_DEVICES': None, 'updated_at': 'now', 'code': {'commit': code}, 'order': [j['id'] for j in qjobs], 'jobs': qjobs, 'stopped': 'done'}, open(os.path.join(qdir, 'queue.json'), 'w'))
    return root


class TestExport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='exp_'); self.root = os.path.join(self.tmp, 'out4'); os.makedirs(self.root)
        make_mock_out_root(self.root, 'server4', [('PSM', 'PSM', 0), ('PSM', 'PSM', 1), ('SMD', 'machine-1-1', 0)], failed=[('PSM', 'PSM', 1)], duplicate_for=('PSM', 'PSM', 0))
        self.reports = os.path.join(self.tmp, 'reports')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_export_package(self):
        d = ex.export(self.root, 'cfval', 'server4', None, self.reports, data_root='/home/tester/data')
        self.assertEqual(sorted(os.listdir(d)), ['artifacts.json', 'config_resolved.yaml', 'metrics.csv', 'provenance_summary.json', 'run_manifest.json', 'summary.md'])
        man = json.load(open(os.path.join(d, 'run_manifest.json')))
        self.assertFalse(man['complete']); self.assertEqual(man['job_counts'], {'success': 3 + 2 + 4, 'failed': 1, 'blocked': 2})
        self.assertEqual(man['n_exported_eval_jobs'], 4); self.assertEqual(man['n_exported_train_jobs'], 2)
        self.assertEqual(man['training_code_sha'], ['abc1234def']); self.assertNotEqual(man['export_code']['commit'], 'abc1234def')
        self.assertEqual(len(man['duplicates']), 1); self.assertIn('attempt2', man['duplicates'][0]['other_successful_attempts'][0]); self.assertIn('no metric-based selection', man['duplicates'][0]['policy'])
        self.assertEqual({j['job_id'] for j in man['jobs'] if j['exported'] is False}, {'train/PSM/PSM/seed1/psm_cf_val', 'eval/PSM/PSM/seed1/psm_cf_val/eval/last', 'eval/PSM/PSM/seed1/psm_cf_val/eval/best_val'})
        df = pd.read_csv(os.path.join(d, 'metrics.csv'))
        self.assertEqual(set(df['seed']), {0}); self.assertEqual(set(df['ckpt_tag']), {'last', 'best_val'}); self.assertEqual(set(df['result_kind']), {'val_ckpt_eval'})
        for col in ('ckpt_epoch', 'ckpt_sha256', 'gamma', 'calibrate', 'split_id', 'data_sha256', 'prior_cache_key', 'training_code_sha', 'fit_protocol', 'device', 'torch_version'):
            self.assertIn(col, df.columns)
        self.assertEqual(sorted(df.loc[df['ckpt_tag'] == 'last', 'ckpt_epoch'].unique()), [3])
        # redaction: no personal absolute paths, no secret keys; original provenance untouched
        blob = ''.join(open(os.path.join(d, f)).read() for f in os.listdir(d))
        self.assertNotIn('/home/tester', blob); self.assertNotIn(self.root, blob); self.assertNotIn('SECRET-VALUE', blob); self.assertNotIn('api_token', blob)
        self.assertIn('<OUT_ROOT>', blob); self.assertIn('<DATA_ROOT>', blob)
        self.assertIn('SECRET-VALUE', open(os.path.join(self.root, 'PSM/PSM/seed0/psm_cf_val/eval/last/attempt1/provenance.json')).read())
        # nothing heavy copied; hashes present
        for f in os.listdir(d):
            self.assertLess(os.path.getsize(os.path.join(d, f)), 200_000); self.assertFalse(f.endswith(('.pt', '.npz', '.log')))
        arts = json.load(open(os.path.join(d, 'artifacts.json')))['artifacts']
        kinds = {a['kind'] for a in arts}; self.assertEqual(kinds, {'checkpoint', 'scores', 'log', 'data_npz'})
        self.assertTrue(all(a.get('sha256') for a in arts if a['kind'] in ('checkpoint', 'scores')))
        self.assertTrue(all(a['path'].startswith(('PSM/', 'SMD/', '<')) for a in arts))
        md = open(os.path.join(d, 'summary.md')).read(); self.assertIn('INCOMPLETE', md); self.assertIn('Not exported', md)

    def test_export_idempotent_and_run_id(self):
        d1 = ex.export(self.root, 'cfval', 'server4', 'custom_run', self.reports)
        self.assertTrue(d1.as_posix().endswith('cfval/server4/custom_run'))
        m1 = pd.read_csv(d1 / 'metrics.csv'); d2 = ex.export(self.root, 'cfval', 'server4', 'custom_run', self.reports); m2 = pd.read_csv(d2 / 'metrics.csv')
        self.assertTrue(m1.equals(m2))


class TestAggregate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='agg_'); self.reports = os.path.join(self.tmp, 'reports')
        r4 = make_mock_out_root(os.path.join(self.tmp, 'out4'), 'server4', [('PSM', 'PSM', 0), ('PSM', 'PSM', 1), ('SMD', 'machine-1-1', 0), ('SMD', 'machine-1-2', 0)])
        r8 = make_mock_out_root(os.path.join(self.tmp, 'out8'), 'server8', [('SWaT', 'swat', 0), ('SMD', 'machine-2-1', 0), ('SMD', 'machine-2-1', 1)])
        ex.export(r4, 'cfval', 'server4', None, self.reports); ex.export(r8, 'cfval', 'server8', None, self.reports)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_aggregate_coverage_and_no_mixing(self):
        d = ex.aggregate(self.reports, 'cfval', (0, 1, 2, 3))
        man = json.load(open(d / 'aggregate_manifest.json'))
        self.assertTrue(man['coverage']['SMD']['label'].startswith('partial-SMD (3/28')); self.assertEqual(man['coverage']['SMD']['entities'], 3)
        self.assertEqual(man['coverage']['PSM']['label'], 'partial seeds'); self.assertEqual(man['coverage']['PSM']['missing_seeds'], {'PSM': [2, 3]})
        self.assertEqual(man['coverage']['SWaT']['missing_seeds'], {'swat': [1, 2, 3]})
        ps = pd.read_csv(d / 'per_seed_results.csv'); self.assertEqual(set(ps['server']), {'server4', 'server8'}); self.assertEqual(sorted(ps[ps['dataset'] == 'PSM']['seed'].unique()), [0, 1])
        dm = pd.read_csv(d / 'dataset_means.csv'); self.assertTrue((dm.loc[dm['dataset'] == 'SMD', 'coverage'].str.startswith('partial-SMD')).all())
        self.assertNotIn('full-SMD', open(d / 'aggregate.md').read())
        # a package with a different gamma must be refused
        r9 = make_mock_out_root(os.path.join(self.tmp, 'out9'), 'server8', [('SWaT', 'swat', 1)], gamma=0.5)
        ex.export(r9, 'cfval', 'server8', 'gamma05', self.reports)
        with self.assertRaises(SystemExit): ex.aggregate(self.reports, 'cfval')
        shutil.rmtree(os.path.join(self.reports, 'cfval', 'server8', 'gamma05'))
        # the same logical result in two packages must be refused
        ex.export(os.path.join(self.tmp, 'out8'), 'cfval', 'server8', 'dup', self.reports)
        with self.assertRaises(SystemExit): ex.aggregate(self.reports, 'cfval')

    def test_full_smd_label_only_when_complete(self):
        tmp = tempfile.mkdtemp(prefix='aggfull_'); rep = os.path.join(tmp, 'reports')
        try:
            jobs = [('SMD', e, s) for e in ex.SMD_ALL for s in (0, 1)]
            ex.export(make_mock_out_root(os.path.join(tmp, 'o'), 'server4', jobs), 'cfval', 'server4', None, rep)
            self.assertEqual(json.load(open(ex.aggregate(rep, 'cfval', (0, 1)) / 'aggregate_manifest.json'))['coverage']['SMD']['label'], 'full-SMD')
            self.assertTrue(json.load(open(ex.aggregate(rep, 'cfval', (0, 1, 2, 3)) / 'aggregate_manifest.json'))['coverage']['SMD']['label'].startswith('partial-SMD'))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestPublish(unittest.TestCase):
    """Local bare origin + execution clone; publish_results.sh must only touch the publishing worktree."""
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='pub_'); self.origin = os.path.join(self.tmp, 'origin.git'); subprocess.check_call(['git', 'init', '-q', '--bare', self.origin])
        self.clone = os.path.join(self.tmp, 'exec'); subprocess.check_call(['git', 'clone', '-q', self.origin, self.clone])
        g = lambda *a: subprocess.check_call(['git', '-C', self.clone, *a], stdout=subprocess.DEVNULL)
        g('config', 'user.email', 't@t'); g('config', 'user.name', 'T')
        os.makedirs(os.path.join(self.clone, 'scripts')); os.makedirs(os.path.join(self.clone, 'scripts', 'configs'))
        for f in ('scripts/export_results.py', 'scripts/publish_results.sh', 'config.py', 'scripts/configs/psm_cf_val.yaml'):
            shutil.copy2(os.path.join(REPO, f), os.path.join(self.clone, f))
        open(os.path.join(self.clone, 'README.md'), 'w').write('exec checkout\n')
        g('add', 'scripts', 'config.py', 'README.md'); g('commit', '-q', '-m', 'code'); g('push', '-q', 'origin', 'HEAD:main')
        self.head = subprocess.check_output(['git', '-C', self.clone, 'rev-parse', 'HEAD']).decode().strip()
        self.out = os.path.join(self.tmp, 'runs', 'cfval', 'server4'); os.makedirs(self.out)
        make_mock_out_root(self.out, 'server4', [('PSM', 'PSM', 0)], code=self.head)
        self.env = dict(os.environ, PICAAD_PYTHON=PY, GIT_AUTHOR_NAME='T', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='T', GIT_COMMITTER_EMAIL='t@t')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def pub(self, *args):
        r = subprocess.run(['bash', os.path.join(self.clone, 'scripts', 'publish_results.sh'), '--campaign', 'cfval', '--server', 'server4', '--out_root', self.out, *args],
                           cwd=self.clone, env=self.env, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def exec_state(self):
        return (subprocess.check_output(['git', '-C', self.clone, 'rev-parse', 'HEAD']).decode().strip(),
                subprocess.check_output(['git', '-C', self.clone, 'status', '--porcelain']).decode())

    def test_dry_run_then_commit_then_push(self):
        rc, out = self.pub(); self.assertEqual(rc, 0, out); self.assertIn('dry-run', out); self.assertIn('run_manifest.json', out)
        self.assertEqual(subprocess.run(['git', '-C', self.clone, 'branch', '--list', 'results/cfval/server4'], capture_output=True, text=True).stdout.strip(), '')
        rc, out = self.pub('--commit'); self.assertEqual(rc, 0, out)
        self.assertEqual(self.exec_state(), (self.head, ''))                                   # execution checkout untouched
        wt = os.path.join(self.out, '_publish', 'worktree_cfval_server4')
        self.assertEqual(subprocess.check_output(['git', '-C', wt, 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip(), 'results/cfval/server4')
        files = subprocess.check_output(['git', '-C', wt, 'show', '--name-only', '--format=', 'HEAD']).decode().split()
        self.assertTrue(files and all(f.startswith('reports/experiments/cfval/server4/cfval_pilot_server4/') for f in files), files)
        self.assertEqual(len(files), 6)
        msg = subprocess.check_output(['git', '-C', wt, 'log', '-1', '--format=%B']).decode(); self.assertIn(self.head, msg); self.assertIn('training code', msg)
        self.assertEqual(subprocess.run(['git', 'ls-remote', '--heads', self.origin, 'results/cfval/server4'], capture_output=True, text=True).stdout.strip(), '')   # not pushed yet
        rc, out = self.pub('--commit'); self.assertEqual(rc, 0, out); self.assertIn('nothing new to commit', out)
        rc, out = self.pub('--commit', '--push'); self.assertEqual(rc, 0, out)
        self.assertIn('results/cfval/server4', subprocess.check_output(['git', 'ls-remote', '--heads', self.origin]).decode())
        self.assertEqual(self.exec_state(), (self.head, ''))
        rc, out = self.pub('--push'); self.assertEqual(rc, 2)                                   # push without commit refused

    def test_remote_ahead_is_refused(self):
        rc, out = self.pub('--commit', '--push'); self.assertEqual(rc, 0, out)
        # someone else advances the results branch on the remote
        other = os.path.join(self.tmp, 'other'); subprocess.check_call(['git', 'clone', '-q', '-b', 'results/cfval/server4', self.origin, other])
        subprocess.check_call(['git', '-C', other, 'config', 'user.email', 'o@o']); subprocess.check_call(['git', '-C', other, 'config', 'user.name', 'O'])
        open(os.path.join(other, 'reports', 'x.txt'), 'w').write('x'); subprocess.check_call(['git', '-C', other, 'add', 'reports/x.txt']); subprocess.check_call(['git', '-C', other, 'commit', '-q', '-m', 'remote change'])
        subprocess.check_call(['git', '-C', other, 'push', '-q', 'origin', 'results/cfval/server4'])
        # new local result -> local branch would diverge -> must be refused, nothing forced
        make_mock_out_root(self.out, 'server4', [('PSM', 'PSM', 0), ('PSM', 'PSM', 1)], code=self.head)
        rc, out = self.pub('--commit', '--push'); self.assertEqual(rc, 2, out); self.assertIn('ahead of or diverged', out)
        self.assertEqual(self.exec_state(), (self.head, ''))

    def test_server_paths_are_disjoint(self):
        out8 = os.path.join(self.tmp, 'runs', 'cfval', 'server8'); os.makedirs(out8); make_mock_out_root(out8, 'server8', [('SWaT', 'swat', 0)], code=self.head)
        r = subprocess.run(['bash', os.path.join(self.clone, 'scripts', 'publish_results.sh'), '--campaign', 'cfval', '--server', 'server8', '--out_root', out8, '--commit'], cwd=self.clone, env=self.env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        rc, out = self.pub('--commit'); self.assertEqual(rc, 0, out)
        f4 = subprocess.check_output(['git', '-C', os.path.join(self.out, '_publish', 'worktree_cfval_server4'), 'show', '--name-only', '--format=', 'HEAD']).decode().split()
        f8 = subprocess.check_output(['git', '-C', os.path.join(out8, '_publish', 'worktree_cfval_server8'), 'show', '--name-only', '--format=', 'HEAD']).decode().split()
        self.assertEqual(set(f4) & set(f8), set()); self.assertTrue(all('/server8/' in f for f in f8) and all('/server4/' in f for f in f4))


if __name__ == '__main__':
    unittest.main()
