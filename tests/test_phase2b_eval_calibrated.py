"""Phase 2-B tests: corrected CALIBRATE=True path in scripts/eval_ckpt.py.
Order: restore -> CF profile (fit data) -> raw P/C/G/CF on fit data -> calibrator incl. CF -> apply.
Synthetic, CPU.  Run: CUDA_VISIBLE_DEVICES= python -m unittest tests.test_phase2b_eval_calibrated -v
"""
import json
import math
import os
import shutil
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
import torch

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from model.scoring import (counterfactual_score_windows, fit_cf_profile, fit_score_calibrator,  # noqa: E402
                           score_windows)
from utils.misc import robust_zscore                                   # noqa: E402
import scripts.eval_ckpt as ev                                         # noqa: E402
from tests.test_phase1b_val_trainer import _synth_npz                  # noqa: E402
from tests.test_phase2a_eval_ckpt import _train                        # noqa: E402


class TestCalibratedPath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='p2b_')
        os.makedirs(os.path.join(cls.tmp, 'npz')); _synth_npz(os.path.join(cls.tmp, 'npz', 'synth.npz'))
        # end-to-end: synthetic training under VAL (last.pt + best_val.pt only)
        import main as main_mod  # noqa
        from tests.test_phase1b_val_trainer import _base_cfg
        from unittest import mock
        cfg = _base_cfg(cls.tmp, max_epoch=3, save_every_epoch=False); cfg.VAL.ENABLE = True
        cfg.RESULT_DIR = os.path.join(cls.tmp, 'run_val'); cfg.TRAIN.CKPT_DIR = os.path.join(cfg.RESULT_DIR, 'ckpt'); cfg.freeze()
        os.makedirs(cfg.RESULT_DIR, exist_ok=True)
        with mock.patch.object(main_mod, 'load_config', lambda a: (cfg, None)), mock.patch.object(sys, 'argv', ['main.py']), \
             mock.patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES': ''}):
            main_mod.main()
        cls.ck_dir = cfg.TRAIN.CKPT_DIR
        cls.best = os.path.join(cls.ck_dir, 'synth_seed0_best_val.pt'); cls.last = os.path.join(cls.ck_dir, 'synth_seed0_last.pt')
        cls.n = 0
        cls.out_best = cls._out_static(cls)
        cls.df, cls.prov = ev.evaluate(cls.best, cls.out_best, cf='both', device='cpu', verify_native_parity=True, calibrate='on')
        cls.sc = np.load(os.path.join(cls.out_best, 'scores.npz'))

    @staticmethod
    def _out_static(cls):
        cls.n += 1; return os.path.join(cls.tmp, f'out_{cls.n}')

    def _out(self):
        return self._out_static(TestCalibratedPath)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_1_calibrator_entries_exist_and_finite(self):
        ent = self.prov['calibration']['entries']
        self.assertEqual(set(ent), {'P_raw', 'C_raw', 'G_raw', 'CF_raw'})
        self.assertTrue(self.prov['calibration']['has_CF_entry'])
        for k, v in ent.items():
            self.assertTrue(math.isfinite(v['center']) and math.isfinite(v['scale']) and v['scale'] > 0, (k, v))
        self.assertEqual(self.prov['calibration']['fit_windows'], 480 - 10 + 1)   # fit on train_sub windows
        self.assertIn('fit_score_calibrator(incl. CF_raw)', self.prov['calibration']['order'])

    def test_2_base_Pn_Cn_identical_off_on(self):
        sc, ent = self.sc, self.prov['calibration']['entries']; clip = self.prov['calibration']['clip_min']
        # stored once; recompute with the native z-score from the recorded calibrator entries
        self.assertTrue(np.array_equal(sc['Pn'], robust_zscore(sc['P_raw'], ent['P_raw']['center'], ent['P_raw']['scale'], clip)))
        self.assertTrue(np.array_equal(sc['Cn'], robust_zscore(sc['C_raw'], ent['C_raw']['center'], ent['C_raw']['scale'], clip)))
        self.assertTrue(np.array_equal(sc['A_off_cal'], (sc['Pn'] + sc['Cn']).astype(np.float32)))
        self.assertTrue(np.array_equal(sc['CFn'], robust_zscore(sc['CF_raw'], ent['CF_raw']['center'], ent['CF_raw']['scale'], clip)))

    def test_3_cf_term_added_when_positive(self):
        sc = self.sc; g = self.prov['scoring']['gamma']; self.assertGreater(g, 0)
        self.assertTrue(np.any(sc['CFn'] > 0))
        self.assertTrue(np.array_equal(sc['A_on_cal'], (sc['Pn'] + sc['Cn'] + g * sc['CFn']).astype(np.float32)))
        self.assertFalse(np.array_equal(sc['A_on_cal'], sc['A_off_cal']))
        d = sc['A_on_cal'] - sc['A_off_cal']
        self.assertGreater(float(d.max()), 0.0); self.assertGreaterEqual(float(d.min()), -1e-6)

    def test_4_native_scorer_parity_and_known_defect_difference(self):
        p = self.prov['native_parity']
        for k in ['A_off_cal_exact', 'A_on_cal_exact', 'Pn_exact', 'CFn_exact', 'A_on_exact', 'A_off_exact']:
            self.assertTrue(p[k], (k, p))
        # reproduce the native main._final_eval order (calibrator fit WITHOUT cf_profile) to document the difference
        ck = ev.load_payload(self.best); cfg = ev.cfg_from_payload(ck); cfg.freeze()
        e, _ = ev.load_data_with_saved_stats(cfg, ck); model, _ = ev.restore_model(cfg, ck, torch.device('cpu'))
        dev, S = torch.device('cpu'), cfg.PICAAD.SCORING
        train_scores_no_cf = score_windows(model, e.train_z, dev, cfg.TRAIN.BATCH_SIZE, S, calibrator=None)  # no cf_profile -> no CF_raw
        defect_cal = fit_score_calibrator(train_scores_no_cf); self.assertNotIn('CF_raw', defect_cal)
        eff, _ = counterfactual_score_windows(model, e.train_z, dev, cfg.TRAIN.BATCH_SIZE, top_k=S.CF_TOP_K, fill_value=S.CF_FILL_VALUE)
        prof = fit_cf_profile(eff)
        defect_out = score_windows(model, e.test_z, dev, cfg.TEST.BATCH_SIZE, S, calibrator=defect_cal, cf_profile=prof)
        self.assertTrue(np.array_equal(defect_out['A'], self.sc['A_off_cal']))      # native defect == Pn + Cn (CF dropped)
        self.assertFalse(np.array_equal(defect_out['A'], self.sc['A_on_cal']))      # corrected path differs
        self.assertTrue(np.array_equal(defect_out['P'], self.sc['Pn']))             # base identical
        # and the corrected calibrator handed to the native scorer reproduces A_on_cal
        good_cal = fit_score_calibrator({**{k: train_scores_no_cf[k] for k in ('P_raw', 'C_raw', 'G_raw')}, 'CF_raw': self.sc['cf_effects_fit'].__class__ and
                                         __import__('model.scoring', fromlist=['cf_anomaly_score']).cf_anomaly_score(eff, prof)})
        good_out = score_windows(model, e.test_z, dev, cfg.TEST.BATCH_SIZE, S, calibrator=good_cal, cf_profile=prof)
        self.assertTrue(np.array_equal(good_out['A'], self.sc['A_on_cal']))

    def test_5_end_to_end_last_and_best(self):
        for path, tag in [(self.last, 'last'), (self.best, 'best_val')]:
            out = self._out()
            df, prov = ev.evaluate(path, out, cf='both', device='cpu', calibrate='on')
            self.assertEqual(set(df['variant']), {'A_off', 'A_on', 'A_off_cal', 'A_on_cal', 'P_raw', 'C_raw', 'G_raw', 'CF_raw', 'Pn', 'Cn', 'Gn', 'CFn'})
            self.assertEqual(set(df['scoring_mode']), {'raw', 'calibrated'})
            self.assertEqual(prov['data']['fit_protocol'], 'train_sub_val'); self.assertTrue(prov['calibration']['enabled'])
            self.assertTrue(prov['state_unchanged'])
            fp = prov['forward_passes']; B = 64; W_fit = 480 - 10 + 1; W_test = 400 - 10 + 1; k = 3
            self.assertEqual(fp['fit_base_forward'], -(-W_fit // B)); self.assertEqual(fp['cf_profile_fit_forward'], -(-W_fit // B) * (1 + k))
            self.assertEqual(fp['test_base_forward'], -(-W_test // B)); self.assertEqual(fp['test_cf_forward'], -(-W_test // B) * (1 + k))
            self.assertNotIn('parity_native_score_windows', fp)
            ck = torch.load(path, map_location='cpu', weights_only=False)
            self.assertEqual(prov['restore']['restored_epoch'], ck['epoch']); self.assertEqual(ck['epoch'], 3 if tag == 'last' else ck['best_val_epoch_so_far'])
            for f in ['metrics.csv', 'scores.npz', 'provenance.json', 'config_resolved.yaml']:
                self.assertTrue(os.path.exists(os.path.join(out, f)))
            prov_disk = json.load(open(os.path.join(out, 'provenance.json')))
            self.assertEqual(prov_disk['calibration']['entries'], prov['calibration']['entries'])

    def test_6_default_follows_checkpoint_config(self):
        out = self._out()
        df, prov = ev.evaluate(self.best, out, cf='both', device='cpu')          # calibrate='cfg', ckpt cfg CALIBRATE=False
        self.assertFalse(prov['calibration']['enabled']); self.assertNotIn('A_on_cal', set(df['variant']))
        self.assertEqual(set(df['scoring_mode']), {'raw'})
        out2 = self._out()
        df2, prov2 = ev.evaluate(self.best, out2, cf='off', device='cpu', calibrate='on')
        self.assertEqual(set(df2['variant']), {'A_off', 'A_off_cal', 'P_raw', 'C_raw', 'G_raw', 'Pn', 'Cn', 'Gn'})
        self.assertFalse(prov2['calibration']['has_CF_entry'])


if __name__ == '__main__':
    unittest.main()
