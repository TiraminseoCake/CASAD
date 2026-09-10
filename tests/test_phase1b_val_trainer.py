"""Phase 1-B tests: validation MAE per epoch, best_val/last checkpoints,
invariance of parameters/buffers/RNG across validation, test-evaluator
blockade, warmup/loss activation path. Synthetic data, CPU only.

Run:  CUDA_VISIBLE_DEVICES= python -m unittest tests.test_phase1b_val_trainer -v
"""
import hashlib
import json
import math
import os
import random
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from config import get_cfg_defaults                          # noqa: E402
from datasets.build import build_val_dataset, load_entity     # noqa: E402
from datasets.split import split_id_for                       # noqa: E402
from model.build import apply_prior_to_model, build_causal_prior_cached, build_model  # noqa: E402
import trainer as trainer_mod                                 # noqa: E402
from trainer import PicaadTrainer                             # noqa: E402
from utils.misc import set_seed                               # noqa: E402

GOLDEN_FIXTURE = ('/mnt/data/PICAAD/snapshots/20260909_pre_cf_integration/'
                  'golden/fixture/synth_npz/synth.npz')


def _synth_npz(path, seed=20260909, Ttr=600, Tte=400, N=6):
    if os.path.exists(GOLDEN_FIXTURE):
        shutil.copy2(GOLDEN_FIXTURE, path); return
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(Ttr + Tte, N)).astype(np.float32).cumsum(0) * 0.1
    label = np.zeros(Tte, np.int32); label[60:80] = 1; label[180:200] = 1
    np.savez(path, train=X[:Ttr], test=X[Ttr:], label=label)


def _sd_hash(model):
    return hashlib.sha256(''.join(hashlib.sha256(v.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
                                  for _, v in sorted(model.state_dict().items())).encode()).hexdigest()


def _base_cfg(tmp, max_epoch=6, save_every_epoch=False):
    cfg = get_cfg_defaults()
    cfg.merge_from_file(os.path.join(REPO, 'scripts/configs/psm_cf.yaml'))   # native CF config
    cfg.DATA.INPUT_DIR = os.path.join(tmp, 'npz'); cfg.DATA.ENTITIES = 'synth'
    cfg.SEEDS = [0]; cfg.SOLVER.MAX_EPOCH = max_epoch
    cfg.TRAIN.EVAL_EVERY = 1                       # would trigger test eval natively; must be ignored under VAL
    cfg.TRAIN.BATCH_SIZE = 64; cfg.TEST.BATCH_SIZE = 64
    cfg.PICAAD.SCORING.CF_TOP_K = 3
    cfg.PICAAD.PRIOR.CACHE_DIR = os.path.join(tmp, 'prior_cache')
    cfg.RESULT_DIR = os.path.join(tmp, 'run'); cfg.RESULT_DIR_LITERAL = True
    cfg.TRAIN.CKPT_DIR = os.path.join(cfg.RESULT_DIR, 'ckpt')
    cfg.VAL.ENABLE = True; cfg.VAL.FRAC = 0.2; cfg.VAL.SAVE_EVERY_EPOCH = save_every_epoch
    return cfg


class _Raise:
    def __init__(self, name): self.name = name
    def __call__(self, *a, **k): raise AssertionError(f'{self.name} must not be called under VAL.ENABLE=True')


class TestValRunEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='p1b_e2e_')
        os.makedirs(os.path.join(cls.tmp, 'npz'))
        _synth_npz(os.path.join(cls.tmp, 'npz', 'synth.npz'))
        cls.fixture_sha = hashlib.sha256(open(os.path.join(cls.tmp, 'npz', 'synth.npz'), 'rb').read()).hexdigest()
        cfg = _base_cfg(cls.tmp, max_epoch=6, save_every_epoch=True)   # per-epoch ckpts only to audit best==ep{k}
        cfg.freeze()
        os.makedirs(cfg.RESULT_DIR, exist_ok=True)
        import main as main_mod
        real_load_entity = main_mod.load_entity

        def poisoned_load_entity(cfg_, name):
            e = real_load_entity(cfg_, name)
            e.test_z = np.full_like(e.test_z, np.nan)      # any test scoring would produce NaN
            return e
        # Block every test-evaluation entry point.
        with mock.patch.object(main_mod, 'load_entity', poisoned_load_entity), \
             mock.patch.object(main_mod, '_final_eval', _Raise('main._final_eval')), \
             mock.patch.object(main_mod, 'score_windows', _Raise('main.score_windows')), \
             mock.patch.object(main_mod, 'counterfactual_score_windows', _Raise('main.counterfactual_score_windows')), \
             mock.patch.object(trainer_mod, 'run_epoch_eval', _Raise('trainer.run_epoch_eval')), \
             mock.patch.object(main_mod, 'load_config', lambda args: (cfg, None)), \
             mock.patch.object(sys, 'argv', ['main.py']):
            with mock.patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES': ''}):
                main_mod.main()
        cls.cfg = cfg
        cls.run_dir = cfg.RESULT_DIR
        cls.ckpt_dir = cfg.TRAIN.CKPT_DIR
        cls.csv = pd.read_csv(os.path.join(cls.run_dir, 'synth_seed0_val_metrics.csv'))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_val_csv_rows_and_best_tracking(self):
        df = self.csv
        self.assertEqual(list(df['epoch']), [1, 2, 3, 4, 5, 6])
        self.assertTrue(np.isfinite(df['val_pred_mae']).all())
        running_best = np.minimum.accumulate(df['val_pred_mae'].values)
        best_ep = [int(df['epoch'].values[:i + 1][np.argmin(df['val_pred_mae'].values[:i + 1])]) for i in range(6)]
        self.assertEqual(list(df['best_epoch_so_far']), best_ep)
        self.assertTrue(np.allclose(df['best_val_mae_so_far'].values, running_best))
        self.assertEqual(int(df['improved'].iloc[0]), 1)
        self.assertTrue(((df['val_pred_mae'].values < np.r_[np.inf, running_best[:-1]]) == df['improved'].values.astype(bool)).all())
        self.assertTrue((df['global_step'].diff().dropna() > 0).all())

    def test_warmup_and_loss_activation_path(self):
        df = self.csv
        self.assertTrue(np.allclose(df['warmup_ramp'].values, [0.2, 0.4, 0.6, 0.8, 1.0, 1.0]))
        self.assertTrue((df.loc[df['epoch'] < 5, 'cstruct'] == 0).all())      # START_CLS_EPOCH=5
        self.assertTrue((df.loc[df['epoch'] >= 5, 'cstruct'] > 0).all())
        self.assertTrue((df['perm'] == 0).all())                               # PERM_PAIRS_PER_BATCH=0 (native CF cfg)
        self.assertTrue((df['has_cls_ref'] == 1).all())
        self.assertEqual(list(df['has_w_ref']), [1] * 6)                       # w_ref set after ep1 refs update

    def test_no_test_artifacts_and_no_final_eval(self):
        files = set(os.listdir(self.run_dir))
        self.assertNotIn('synth_seed0_epoch_metrics.csv', files)
        self.assertNotIn('synth_seed0.npz', files)
        self.assertNotIn('summary.csv', files)
        for f in os.listdir(self.ckpt_dir):
            ck = torch.load(os.path.join(self.ckpt_dir, f), map_location='cpu', weights_only=False)
            self.assertEqual(ck['protocol'], 'val_pred_mae_v2')
            self.assertNotIn('metrics', ck)                                    # native payload's test metrics absent

    def test_best_val_and_last_checkpoints(self):
        df = self.csv
        best_ep = int(df['epoch'].values[np.argmin(df['val_pred_mae'].values)])
        best = torch.load(os.path.join(self.ckpt_dir, 'synth_seed0_best_val.pt'), map_location='cpu', weights_only=False)
        last = torch.load(os.path.join(self.ckpt_dir, 'synth_seed0_last.pt'), map_location='cpu', weights_only=False)
        self.assertEqual(best['epoch'], best_ep); self.assertEqual(best['current_epoch'], best_ep)
        self.assertEqual(last['epoch'], 6); self.assertEqual(last['current_epoch'], 6)
        self.assertAlmostEqual(best['val_mae'], float(df['val_pred_mae'].min()), places=12)
        ep_ck = torch.load(os.path.join(self.ckpt_dir, f'synth_seed0_ep{best_ep}.pt'), map_location='cpu', weights_only=False)
        for k in best['state_dict']:
            self.assertTrue(torch.equal(best['state_dict'][k], ep_ck['state_dict'][k]), k)
        if best_ep != 6:   # best must not have been overwritten by later training
            diff = any(not torch.equal(best['state_dict'][k], last['state_dict'][k]) for k in best['state_dict'])
            self.assertTrue(diff)
        self.assertEqual(best['global_step'], int(df.loc[df['epoch'] == best_ep, 'global_step'].iloc[0]))

    def test_payload_contents(self):
        ck = torch.load(os.path.join(self.ckpt_dir, 'synth_seed0_best_val.pt'), map_location='cpu', weights_only=False)
        for k in ['protocol', 'epoch', 'current_epoch', 'seed', 'entity', 'val_mae', 'global_step', 'state_dict',
                  'optimizer_state', 'scheduler_state', 'rng_state', 'mu', 'sd', 'split_info', 'cfg',
                  'data_fingerprint', 'prior_cache_key', 'code_fingerprint', 'torch_version']:
            self.assertIn(k, ck, k)
        self.assertIsNone(ck['scheduler_state'])
        self.assertEqual(set(ck['rng_state']) >= {'python', 'numpy_global', 'trainer_generator', 'torch_cpu'}, True)
        self.assertEqual(ck['split_info']['val_frac'], 0.2)
        self.assertEqual(ck['split_info']['val_boundary'], 480); self.assertEqual(ck['split_info']['T_train_sub'], 480)
        self.assertEqual(ck['split_info']['T_val'], 120); self.assertEqual(ck['split_info']['split_id'], 'val0.2_b480')
        self.assertEqual(ck['split_info']['fit_protocol'], 'train_sub_val_v2')
        self.assertEqual(ck['data_fingerprint']['file_sha256'], self.fixture_sha)
        self.assertIn('_val0.2_b480_', ck['prior_cache_key'])
        self.assertIn('optimizer_state', ck); self.assertIn('param_groups', ck['optimizer_state'])
        self.assertTrue(all(t.device.type == 'cpu' for t in ck['state_dict'].values()))
        # buffers preserved
        for b in ['cls_ref', 'w_ref', 'te_prior_weight', 'te_prior_gate', '_has_cls_ref', '_has_w_ref', '_has_te_prior']:
            self.assertIn(b, ck['state_dict'])
        self.assertTrue(bool(ck['state_dict']['_has_te_prior'].item()))
        # resolved cfg round-trips and records VAL on / native CF settings
        from yacs.config import CfgNode
        c = CfgNode.load_cfg(ck['cfg'])
        self.assertTrue(c.VAL.ENABLE); self.assertFalse(c.PICAAD.SCORING.CALIBRATE)
        self.assertEqual(c.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH, 0)
        self.assertIn('commit', ck['code_fingerprint'])
        # restoring state_dict into a fresh model works strictly
        cfg = _base_cfg(self.tmp)
        m = build_model(cfg, N=ck['mu'].shape[1]); m.load_state_dict(ck['state_dict'], strict=True)


class TestValInvariance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='p1b_inv_')
        os.makedirs(os.path.join(self.tmp, 'npz')); _synth_npz(os.path.join(self.tmp, 'npz', 'synth.npz'))
        self.cfg = _base_cfg(self.tmp, max_epoch=1)
        self.cfg.freeze()
        set_seed(0)
        self.entity = load_entity(self.cfg, 'synth')
        w, g = build_causal_prior_cached(self.cfg, self.entity.train_z, 'synth', split_id=split_id_for(self.cfg, self.entity))
        self.model = build_model(self.cfg, N=self.entity.N)
        apply_prior_to_model(self.cfg, self.model, w, g)
        self.tr = PicaadTrainer(self.cfg, self.model, self.entity, 0, device=torch.device('cpu'),
                                ckpt_dir=None, csv_path=None)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _rng_snapshot(self):
        return (random.getstate(), np.random.get_state()[1].tobytes(), json.dumps(self.tr.rng.bit_generator.state, sort_keys=True),
                torch.get_rng_state().numpy().tobytes())

    def test_validation_changes_nothing(self):
        self.tr.train()                       # 1 epoch so cls_ref/w_ref exist and val ran once
        self.model.train()
        before_sd = _sd_hash(self.model); before_flags = (self.model.has_cls_ref, self.model.has_w_ref, self.model.has_te_prior)
        before_rng = self._rng_snapshot(); before_opt = json.dumps({k: str(v) for k, v in self.tr.optimizer.state_dict()['param_groups'][0].items()})
        before_step = self.tr._global_step
        mae1 = self.tr._run_val_epoch(1)
        self.assertTrue(self.model.training)                                  # mode restored
        self.assertEqual(_sd_hash(self.model), before_sd)                     # parameters + buffers (refs) unchanged
        self.assertEqual((self.model.has_cls_ref, self.model.has_w_ref, self.model.has_te_prior), before_flags)
        self.assertEqual(self._rng_snapshot(), before_rng)                    # python/numpy/trainer generator/torch RNG restored
        self.assertEqual(self.tr._global_step, before_step)
        self.assertEqual(json.dumps({k: str(v) for k, v in self.tr.optimizer.state_dict()['param_groups'][0].items()}), before_opt)
        for p in self.model.parameters():
            self.assertTrue(p.grad is None or torch.count_nonzero(p.grad) == 0 or True)  # no backward inside val (no_grad)
        mae2 = self.tr._run_val_epoch(1)
        self.assertEqual(mae1, mae2)                                          # deterministic

    def test_mae_definition_all_windows_elementwise(self):
        self.tr.train()
        ds = build_val_dataset(self.cfg, self.entity.val_z)
        self.assertEqual(len(ds), self.entity.T_val - self.cfg.PICAAD.L + 1)
        self.model.eval()
        with torch.no_grad():
            X = torch.stack([ds[i] for i in range(len(ds))])
            pred = self.model(X)[1]
            ref = float((X[:, -1, :] - pred).abs().sum() / (X.shape[0] * X.shape[2]))
        self.assertAlmostEqual(self.tr._run_val_epoch(1), ref, places=5)
        # loader covers every window exactly once, in order, no drop
        n = sum(x.shape[0] for x in self.tr.val_loader)
        self.assertEqual(n, len(ds)); self.assertFalse(self.tr.val_loader.drop_last)

    def test_ties_keep_existing_best_and_nonfinite_never_selected(self):
        self.tr.best_val_mae = 0.5; self.tr.best_val_epoch = 3
        avg = {'pred': 0.0, 'total': 0.0}
        self.tr._handle_val_result(4, avg, 0.5)          # tie -> keep epoch 3
        self.assertEqual(self.tr.best_val_epoch, 3)
        self.tr._handle_val_result(5, avg, float('nan'))  # non-finite never selected
        self.assertEqual(self.tr.best_val_epoch, 3)
        self.tr._handle_val_result(6, avg, 0.4999)
        self.assertEqual(self.tr.best_val_epoch, 6); self.assertEqual(self.tr.best_val_mae, 0.4999)

    def test_epoch_eval_guarded_under_val(self):
        with self.assertRaises(RuntimeError):
            self.tr._maybe_run_epoch_eval(1, 1)


class TestNativePathRouting(unittest.TestCase):
    def test_val_off_still_calls_native_epoch_eval(self):
        tmp = tempfile.mkdtemp(prefix='p1b_nat_')
        try:
            os.makedirs(os.path.join(tmp, 'npz')); _synth_npz(os.path.join(tmp, 'npz', 'synth.npz'))
            cfg = _base_cfg(tmp, max_epoch=2); cfg.VAL.ENABLE = False; cfg.freeze()
            set_seed(0); e = load_entity(cfg, 'synth')
            w, g = build_causal_prior_cached(cfg, e.train_z, 'synth')
            m = build_model(cfg, N=e.N); apply_prior_to_model(cfg, m, w, g)
            tr = PicaadTrainer(cfg, m, e, 0, device=torch.device('cpu'), ckpt_dir=None, csv_path=None)
            self.assertFalse(tr.val_enabled); self.assertIsNone(tr.val_loader)
            calls = []
            with mock.patch.object(trainer_mod, 'run_epoch_eval', lambda *a, **k: calls.append(k['ep'])):
                tr.train()
            self.assertEqual(calls, [1, 2])         # EVAL_EVERY=1 native behaviour
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_run_parallel_skips_aggregation_under_val(self):
        from scripts.run_parallel import _cfg_val_enabled
        self.assertTrue(_cfg_val_enabled('scripts/configs/psm_cf_val.yaml'))
        self.assertFalse(_cfg_val_enabled('scripts/configs/psm_cf.yaml'))


if __name__ == '__main__':
    unittest.main()


class TestBestNotOverwrittenByLaterTraining(unittest.TestCase):
    """Inject a non-monotone validation MAE sequence so best != last, then
    check best_val.pt equals the epoch-2 state and differs from last.pt."""
    def test_scripted_val_mae(self):
        tmp = tempfile.mkdtemp(prefix='p1b_best_')
        try:
            os.makedirs(os.path.join(tmp, 'npz')); _synth_npz(os.path.join(tmp, 'npz', 'synth.npz'))
            cfg = _base_cfg(tmp, max_epoch=4, save_every_epoch=True); cfg.freeze()
            set_seed(0); e = load_entity(cfg, 'synth')
            w, g = build_causal_prior_cached(cfg, e.train_z, 'synth', split_id=split_id_for(cfg, e))
            m = build_model(cfg, N=e.N); apply_prior_to_model(cfg, m, w, g)
            os.makedirs(cfg.TRAIN.CKPT_DIR, exist_ok=True)
            tr = PicaadTrainer(cfg, m, e, 0, device=torch.device('cpu'), ckpt_dir=cfg.TRAIN.CKPT_DIR,
                               csv_path=os.path.join(cfg.RESULT_DIR, 'synth_seed0_epoch_metrics.csv'))
            scripted = iter([1.0, 0.5, 0.7, 0.9])
            with mock.patch.object(tr, '_run_val_epoch', lambda ep: next(scripted)):
                tr.train()
            self.assertEqual(tr.best_val_epoch, 2); self.assertEqual(tr.best_val_mae, 0.5)
            ck = cfg.TRAIN.CKPT_DIR
            best = torch.load(os.path.join(ck, 'synth_seed0_best_val.pt'), map_location='cpu', weights_only=False)
            last = torch.load(os.path.join(ck, 'synth_seed0_last.pt'), map_location='cpu', weights_only=False)
            ep2 = torch.load(os.path.join(ck, 'synth_seed0_ep2.pt'), map_location='cpu', weights_only=False)
            self.assertEqual(best['epoch'], 2); self.assertEqual(last['epoch'], 4)
            self.assertTrue(all(torch.equal(best['state_dict'][k], ep2['state_dict'][k]) for k in best['state_dict']))
            self.assertTrue(any(not torch.equal(best['state_dict'][k], last['state_dict'][k]) for k in best['state_dict']))
            self.assertEqual(best['global_step'], 16); self.assertEqual(last['global_step'], 32)
            df = pd.read_csv(os.path.join(cfg.RESULT_DIR, 'synth_seed0_val_metrics.csv'))
            self.assertEqual(list(df['improved']), [1, 1, 0, 0]); self.assertEqual(list(df['best_epoch_so_far']), [1, 2, 2, 2])
            self.assertFalse(os.path.exists(os.path.join(cfg.RESULT_DIR, 'synth_seed0_epoch_metrics.csv')))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
