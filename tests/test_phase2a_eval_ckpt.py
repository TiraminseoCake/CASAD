"""Phase 2-A tests for scripts/eval_ckpt.py (CALIBRATE=False path). Synthetic, CPU.

Run:  CUDA_VISIBLE_DEVICES= python -m unittest tests.test_phase2a_eval_ckpt -v
"""
import hashlib
import json
import os
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

from config import get_cfg_defaults                                  # noqa: E402
from datasets.build import load_entity                                # noqa: E402
from model.modeling_picaad import PICAAD                              # noqa: E402
from model.scoring import counterfactual_score_windows, fit_cf_profile, score_windows  # noqa: E402
import scripts.eval_ckpt as ev                                        # noqa: E402
from tests.test_phase1b_val_trainer import _base_cfg, _synth_npz      # noqa: E402


def _train(tmp, val: bool, epochs: int):
    """Train on the synthetic fixture via main.main(); returns (cfg, ckpt_dir)."""
    import main as main_mod
    cfg = _base_cfg(tmp, max_epoch=epochs, save_every_epoch=True)
    cfg.VAL.ENABLE = bool(val)
    cfg.TRAIN.EVAL_EVERY = 1
    cfg.RESULT_DIR = os.path.join(tmp, 'run_val' if val else 'run_native'); cfg.TRAIN.CKPT_DIR = os.path.join(cfg.RESULT_DIR, 'ckpt')
    cfg.freeze()
    os.makedirs(cfg.RESULT_DIR, exist_ok=True)
    with mock.patch.object(main_mod, 'load_config', lambda args: (cfg, None)), mock.patch.object(sys, 'argv', ['main.py']), \
         mock.patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES': ''}):
        main_mod.main()
    return cfg, cfg.TRAIN.CKPT_DIR


def _sd_hash(model):
    return hashlib.sha256(''.join(hashlib.sha256(v.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
                                  for _, v in sorted(model.state_dict().items())).encode()).hexdigest()


class TestEvalCkpt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='p2a_')
        os.makedirs(os.path.join(cls.tmp, 'npz')); _synth_npz(os.path.join(cls.tmp, 'npz', 'synth.npz'))
        cls.cfg_val, cls.ck_val_dir = _train(cls.tmp, val=True, epochs=3)
        cls.cfg_nat, cls.ck_nat_dir = _train(cls.tmp, val=False, epochs=2)
        cls.val_best = os.path.join(cls.ck_val_dir, 'synth_seed0_best_val.pt')
        cls.nat_ep2 = os.path.join(cls.ck_nat_dir, 'synth_seed0_ep2.pt')
        cls.outs = 0

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _out(self):
        TestEvalCkpt.outs += 1
        return os.path.join(self.tmp, f'eval_out_{TestEvalCkpt.outs}')

    # ---------------- selection ----------------
    def test_explicit_selection_only(self):
        self.assertEqual(ev.resolve_ckpt_path(self.ck_val_dir, 'synth', 0, 'best_val'), self.val_best)
        self.assertTrue(ev.resolve_ckpt_path(self.ck_val_dir, 'synth', 0, 'last').endswith('_last.pt'))
        self.assertTrue(ev.resolve_ckpt_path(self.ck_val_dir, 'synth', 0, 'ep2').endswith('_ep2.pt'))
        with self.assertRaises(ev.EvalError): ev.resolve_ckpt_path(self.ck_val_dir, 'synth', 0, 'best')
        with self.assertRaises(ev.EvalError): ev.resolve_ckpt_path(self.ck_val_dir, 'synth', 0, 'ep99')
        src = open(ev.__file__).read()
        self.assertNotIn('sorted(glob', src); self.assertNotIn('idxmax', src)

    # ---------------- restore (both formats) ----------------
    def test_restore_both_formats_strict_no_set_te_prior(self):
        for path, fmt in [(self.val_best, 'val'), (self.nat_ep2, 'native')]:
            ck = ev.load_payload(path); self.assertEqual(ck['_format'], fmt)
            cfg = ev.cfg_from_payload(ck); cfg.freeze()
            with mock.patch.object(PICAAD, 'set_te_prior', side_effect=AssertionError('set_te_prior must not be called after load')):
                model, info = ev.restore_model(cfg, ck, torch.device('cpu'))
            for k, v in ck['state_dict'].items():
                self.assertTrue(torch.equal(model.state_dict()[k].cpu(), v), k)
            self.assertEqual(model._current_epoch, ck['epoch']); self.assertEqual(info['restored_epoch'], ck['epoch'])
            self.assertEqual(info['epoch_source'], 'payload.current_epoch' if fmt == 'val' else 'payload.epoch')
            self.assertTrue(all(info['flags'].values()))
            self.assertEqual(cfg.VAL.ENABLE, fmt == 'val')
        # epoch resolution rules
        with self.assertRaises(ev.EvalError): ev.resolved_epoch({'current_epoch': 3, 'epoch': 2})
        with self.assertRaises(ev.EvalError): ev.resolved_epoch({})
        self.assertEqual(ev.resolved_epoch({'epoch': 5}), (5, 'payload.epoch'))

    # ---------------- preprocessing from saved stats/split ----------------
    def test_saved_stats_and_split_applied(self):
        for path in [self.val_best, self.nat_ep2]:
            ck = ev.load_payload(path); cfg = ev.cfg_from_payload(ck); cfg.freeze()
            e, info = ev.load_data_with_saved_stats(cfg, ck)
            ref = load_entity(cfg, 'synth')
            self.assertTrue(np.array_equal(e.train_z, ref.train_z)); self.assertTrue(np.array_equal(e.test_z, ref.test_z))
            self.assertTrue(np.array_equal(e.mu, ck['mu'])); self.assertTrue(np.array_equal(e.sd, ck['sd']))
            if ck['_format'] == 'val':
                self.assertEqual(info['fit_protocol'], 'train_sub_val'); self.assertEqual(e.T_train, 480); self.assertEqual(e.T_val, 120)
                self.assertEqual(info['split_id'], 'val0.2_b480')
            else:
                self.assertEqual(info['fit_protocol'], 'full_train_native'); self.assertEqual(e.T_train, 600); self.assertEqual(e.T_val, 0)
                self.assertEqual(info['split_id'], 'full')
        # tampered mu -> data-identity error
        ck = ev.load_payload(self.val_best); ck['mu'] = ck['mu'] + 1.0; cfg = ev.cfg_from_payload(ck); cfg.freeze()
        with self.assertRaises(ev.EvalError): ev.load_data_with_saved_stats(cfg, ck)
        # tampered split_info -> split mismatch error
        ck = ev.load_payload(self.val_best); ck['split_info']['val_boundary'] = 400; cfg = ev.cfg_from_payload(ck); cfg.freeze()
        with self.assertRaises(ev.EvalError): ev.load_data_with_saved_stats(cfg, ck)

    # ---------------- dimension rejection (44 vs 51 proxy) ----------------
    def test_rejects_channel_mismatch_without_conversion(self):
        d5 = os.path.join(self.tmp, 'npz5'); os.makedirs(d5, exist_ok=True)
        src = np.load(os.path.join(self.tmp, 'npz', 'synth.npz'))
        np.savez(os.path.join(d5, 'synth.npz'), train=src['train'][:, :5], test=src['test'][:, :5], label=src['label'])
        with self.assertRaises(ev.EvalError) as c:
            ev.evaluate(self.val_best, self._out(), data_input_dir=d5, cf='both', device='cpu')
        msg = str(c.exception); self.assertIn("'N_data': 5", msg); self.assertIn('mismatch', msg); self.assertIn('51', msg)
        # EXPECTED_N in the checkpoint config (SWaT rule) vs 6-channel data
        ck = torch.load(self.val_best, map_location='cpu', weights_only=False)
        ck['cfg'] = ck['cfg'].replace('EXPECTED_N: 0', 'EXPECTED_N: 51')
        p = os.path.join(self.tmp, 'ckpt_expect51.pt'); torch.save(ck, p)
        with self.assertRaises(ev.EvalError) as c:
            ev.evaluate(p, self._out(), cf='both', device='cpu')
        msg = str(c.exception); self.assertIn("'N_expected_cfg': 51", msg); self.assertIn('mismatch', msg)

    # ---------------- CF OFF/ON on the same base, native parity, invariance ----------------
    def test_evaluate_val_ckpt_cf_off_on_parity_and_invariance(self):
        out = self._out()
        df, prov = ev.evaluate(self.val_best, out, cf='both', device='cpu', verify_native_parity=True)
        sc = np.load(os.path.join(out, 'scores.npz'))
        self.assertTrue(np.array_equal(sc['A_off'], (sc['P_raw'] + sc['C_raw']).astype(np.float32)))
        g = prov['scoring']['gamma']; self.assertEqual(g, 1.0)
        self.assertTrue(np.array_equal(sc['A_on'], (sc['A_off'] + g * sc['CF_raw']).astype(np.float32)))
        self.assertTrue(np.any(sc['CF_raw'] != 0))
        self.assertTrue(all(prov['native_parity'].values()), prov['native_parity'])
        self.assertTrue(prov['state_unchanged'])
        self.assertEqual(prov['data']['fit_protocol'], 'train_sub_val'); self.assertEqual(prov['cf']['fit_windows'], 480 - 10 + 1)
        # independent native recomputation on a freshly restored model equals the saved arrays
        ck = ev.load_payload(self.val_best); cfg = ev.cfg_from_payload(ck); cfg.freeze()
        e, _ = ev.load_data_with_saved_stats(cfg, ck); model, _ = ev.restore_model(cfg, ck, torch.device('cpu'))
        h0 = _sd_hash(model)
        eff, _ = counterfactual_score_windows(model, e.train_z, torch.device('cpu'), cfg.TRAIN.BATCH_SIZE, top_k=cfg.PICAAD.SCORING.CF_TOP_K, fill_value=cfg.PICAAD.SCORING.CF_FILL_VALUE)
        prof = fit_cf_profile(eff)
        nat = score_windows(model, e.test_z, torch.device('cpu'), cfg.TEST.BATCH_SIZE, cfg.PICAAD.SCORING, calibrator=None, cf_profile=prof)
        self.assertTrue(np.array_equal(nat['A'], sc['A_on'])); self.assertTrue(np.array_equal(nat['P_raw'], sc['P_raw']))
        self.assertEqual(_sd_hash(model), h0)                       # profile fit + scoring changed nothing
        # metrics rows and provenance essentials
        self.assertEqual(set(df['variant']), {'A_off', 'A_on', 'P_raw', 'C_raw', 'G_raw', 'CF_raw'})
        self.assertEqual(prov['checkpoint']['sha256'], hashlib.sha256(open(self.val_best, 'rb').read()).hexdigest())
        self.assertEqual(prov['restore']['restored_epoch'], ck['epoch']); self.assertFalse(prov['restore']['set_te_prior_called_after_load'])
        self.assertIn('sliding_window_used', prov['evaluator']); self.assertIn('npz_sha256', prov['data'])
        fp = prov['forward_passes']
        W_test, W_fit, B, k = 400 - 10 + 1, 480 - 10 + 1, 64, cfg.PICAAD.SCORING.CF_TOP_K
        self.assertEqual(fp['test_base_forward'], -(-W_test // B))
        self.assertEqual(fp['cf_profile_fit_forward'], -(-W_fit // B) * (1 + k))
        self.assertEqual(fp['test_cf_forward'], -(-W_test // B) * (1 + k))
        for f in ['metrics.csv', 'scores.npz', 'provenance.json', 'config_resolved.yaml']:
            self.assertTrue(os.path.exists(os.path.join(out, f)))
        # never overwrite
        with self.assertRaises(ev.EvalError): ev.evaluate(self.val_best, out, cf='off', device='cpu')

    def test_evaluate_native_ckpt_matches_saved_epoch_eval_off_path(self):
        out = self._out()
        df, prov = ev.evaluate(self.nat_ep2, out, cf='both', device='cpu', verify_native_parity=True)
        self.assertEqual(prov['checkpoint']['format'], 'native'); self.assertEqual(prov['data']['fit_protocol'], 'full_train_native')
        self.assertEqual(prov['cf']['fit_windows'], 600 - 10 + 1)
        # the native run_epoch_eval at ep2 used the live model with the same _current_epoch (=2): its A-PR must match ours
        # (native ep-eval used CF profile on full train with cf_profile passed -> A = P + C + gamma*CF)
        ep_csv = pd.read_csv(os.path.join(os.path.dirname(self.ck_nat_dir), 'synth_seed0_epoch_metrics.csv'))
        native_apr = float(ep_csv.loc[ep_csv['epoch'] == 2, 'AUC_PR'].iloc[0])
        ours = float(df.loc[df['variant'] == 'A_on', 'AUC-PR'].iloc[0])
        self.assertAlmostEqual(native_apr, ours, places=10)
        self.assertTrue(all(prov['native_parity'].values()))

    def test_cf_off_only_and_cfg_without_cf(self):
        out = self._out()
        df, prov = ev.evaluate(self.val_best, out, cf='off', device='cpu')
        self.assertEqual(set(df['variant']), {'A_off', 'P_raw', 'C_raw', 'G_raw'}); self.assertNotIn('test_cf_forward', prov['forward_passes'])
        ck = torch.load(self.val_best, map_location='cpu', weights_only=False)
        ck['cfg'] = ck['cfg'].replace('USE_COUNTERFACTUAL: true', 'USE_COUNTERFACTUAL: false')
        p = os.path.join(self.tmp, 'ckpt_nocf.pt'); torch.save(ck, p)
        with self.assertRaises(ev.EvalError): ev.evaluate(p, self._out(), cf='both', device='cpu')
        # CALIBRATE=True in the checkpoint config now routes to the corrected calibrated path (Phase 2-B)
        ck['cfg'] = ck['cfg'].replace('CALIBRATE: false', 'CALIBRATE: true').replace('USE_COUNTERFACTUAL: false', 'USE_COUNTERFACTUAL: true'); torch.save(ck, p)
        df2, prov2 = ev.evaluate(p, self._out(), cf='both', device='cpu')
        self.assertTrue(prov2['calibration']['enabled']); self.assertIn('A_on_cal', set(df2['variant']))


if __name__ == '__main__':
    unittest.main()
