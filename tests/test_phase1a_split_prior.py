"""Phase 1-A tests: VAL config, chronological split, train_sub-only fitting,
independent windowing, prior cache key separation. Synthetic data only.

Run:  python -m unittest tests.test_phase1a_split_prior -v
"""
import hashlib
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from config import get_cfg_defaults                      # noqa: E402
from datasets.build import (                              # noqa: E402
    build_train_dataset, build_val_dataset, load_entity,
)
from datasets.split import (                              # noqa: E402
    split_and_standardize, split_id_for, split_time_ordered,
)
from datasets.util import standardize_train_test          # noqa: E402
from model.build import _prior_cache_key, build_causal_prior_cached  # noqa: E402

GOLDEN_FIXTURE = ('/mnt/data/PICAAD/snapshots/20260909_pre_cf_integration/'
                  'golden/fixture/synth_npz/synth.npz')
GOLDEN_KEY = 'PSM_synth_pcmci_5fc402d470ab3c5c'   # from Phase-0 golden run.log (VAL off)


def _legacy_prior_cache_key(cfg, train_TN, entity_name):
    """Verbatim copy of model/build.py:_prior_cache_key at d9609c2 (pre Phase 1-A)."""
    h = hashlib.sha256()
    p = cfg.PICAAD.PRIOR
    parts = [cfg.DATA.NAME, entity_name, p.TYPE, f'tau{cfg.PICAAD.TAU_MAX}',
             f'self{p.SELF_MASS:g}', f'sd{p.SEED}']
    if p.TYPE == 'pcmci':
        parts += [p.PCMCI.CI_TEST, f'a{p.PCMCI.ALPHA:g}', f'sub{p.PCMCI.SUBSAMPLE}']
    else:
        parts += [f'b{p.TE.BINS}', f'nc{p.TE.NUM_CHUNKS}', f'cl{p.TE.CHUNK_LEN}', f'th{p.TE.THRESHOLD:g}']
    h.update('|'.join(parts).encode('utf-8'))
    h.update(np.ascontiguousarray(train_TN).tobytes())
    return f'{cfg.DATA.NAME}_{entity_name}_{p.TYPE}_{h.hexdigest()[:16]}'


def _make_npz(path, T_train=300, T_test=120, N=5, seed=1, with_nan=False):
    rng = np.random.default_rng(seed)
    train = rng.normal(size=(T_train, N)).astype(np.float32) * np.arange(1, N + 1) + 10 * np.arange(N)
    test = rng.normal(size=(T_test, N)).astype(np.float32) * 3.0
    if with_nan:
        train[T_train - 3, 0] = np.nan       # inside the val tail
        train[2, 1] = np.inf                 # inside train_sub
    label = np.zeros(T_test, np.int32); label[40:60] = 1
    np.savez(path, train=train, test=test, label=label)
    return train, test, label


def _cfg(input_dir, val=False, frac=0.2, scale='standard', L=10):
    cfg = get_cfg_defaults()
    cfg.DATA.INPUT_DIR = input_dir
    cfg.DATA.SCALE = scale
    cfg.PICAAD.L = L
    cfg.VAL.ENABLE = bool(val)
    cfg.VAL.FRAC = frac
    return cfg


class TestConfigDefaults(unittest.TestCase):
    def test_val_namespace_defaults_off(self):
        cfg = get_cfg_defaults()
        self.assertFalse(cfg.VAL.ENABLE)
        self.assertEqual(cfg.VAL.FRAC, 0.2)
        self.assertFalse(cfg.VAL.SAVE_EVERY_EPOCH)
        self.assertEqual(cfg.VAL.SAVE_EVERY_N, 0)
        self.assertEqual(cfg.DATA.EXPECTED_N, 0)
        # native settings untouched
        self.assertFalse(cfg.PICAAD.SCORING.CALIBRATE)
        self.assertEqual(cfg.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH, 2)


class TestSplit(unittest.TestCase):
    def test_time_ordered_no_overlap_and_contiguous(self):
        x = np.arange(100 * 3, dtype=np.float32).reshape(100, 3)
        tr, va, b = split_time_ordered(x, 0.2)
        self.assertEqual(b, 80)
        self.assertEqual(tr.shape[0] + va.shape[0], 100)
        self.assertTrue(np.array_equal(np.concatenate([tr, va]), x))
        self.assertTrue(np.all(tr[:, 0] < va[:, 0].min()))       # strictly earlier rows
        self.assertEqual(len(set(tr[:, 0]) & set(va[:, 0])), 0)  # disjoint rows
        # val_frac=0 -> unchanged
        tr0, va0, b0 = split_time_ordered(x, 0.0)
        self.assertIs(tr0, x); self.assertEqual(va0.shape[0], 0); self.assertEqual(b0, 100)
        with self.assertRaises(ValueError):
            split_time_ordered(x, 1.0)

    def test_stats_fit_on_train_sub_only(self):
        rng = np.random.default_rng(0)
        train = rng.normal(size=(500, 4)).astype(np.float32)
        train[400:] += 50.0            # val tail has a very different mean
        test = rng.normal(size=(50, 4)).astype(np.float32)
        tr_z, va_z, te_z, mu, sd, b = split_and_standardize(train, test, 0.2)
        self.assertEqual(b, 400)
        ref_tr_z, ref_te_z, ref_mu, ref_sd = standardize_train_test(train[:400], test)
        self.assertTrue(np.array_equal(mu, ref_mu)); self.assertTrue(np.array_equal(sd, ref_sd))
        self.assertTrue(np.array_equal(tr_z, ref_tr_z)); self.assertTrue(np.array_equal(te_z, ref_te_z))
        # mu must NOT be the full-train mean (which would be pulled up by the +50 tail)
        full_mu = np.nanmean(train, axis=0, keepdims=True)
        self.assertGreater(np.abs(full_mu - mu).max(), 5.0)
        # val standardized with the same train_sub stats
        self.assertTrue(np.allclose(va_z, (train[400:] - mu) / sd, atol=1e-6))
        self.assertGreater(va_z.mean(), 10.0)  # shift preserved (not re-centered on val)


class TestLoadEntity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.train, self.test, self.label = _make_npz(os.path.join(self.tmp.name, 'ent.npz'), with_nan=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_val_off_is_native(self):
        cfg = _cfg(self.tmp.name, val=False)
        e = load_entity(cfg, 'ent')
        tr_z, te_z, mu, sd = standardize_train_test(self.train, self.test)
        self.assertTrue(np.array_equal(e.train_z, tr_z)); self.assertTrue(np.array_equal(e.test_z, te_z))
        self.assertTrue(np.array_equal(e.mu, mu)); self.assertTrue(np.array_equal(e.sd, sd))
        self.assertEqual(e.T_val, 0); self.assertEqual(e.val_boundary, 300); self.assertEqual(e.val_frac, 0.0)
        self.assertEqual(split_id_for(cfg, e), 'full')

    def test_val_on_split_and_independent_windowing(self):
        cfg = _cfg(self.tmp.name, val=True, frac=0.2, L=10)
        e = load_entity(cfg, 'ent')
        self.assertEqual(e.val_boundary, 240); self.assertEqual(e.T_train, 240); self.assertEqual(e.T_val, 60)
        self.assertEqual(split_id_for(cfg, e), 'val0.2_b240')
        # stats from train_sub only
        tr_z, va_z, te_z, mu, sd, b = split_and_standardize(self.train, self.test, 0.2)
        self.assertTrue(np.array_equal(e.train_z, tr_z)); self.assertTrue(np.array_equal(e.val_z, va_z))
        self.assertTrue(np.array_equal(e.test_z, te_z)); self.assertTrue(np.array_equal(e.mu, mu))
        self.assertTrue(np.isfinite(e.val_z).all()); self.assertTrue(np.isfinite(e.train_z).all())
        # independent windowing: window counts and no straddling
        ds_tr = build_train_dataset(cfg, e.train_z); ds_va = build_val_dataset(cfg, e.val_z)
        self.assertEqual(len(ds_tr), 240 - 10 + 1); self.assertEqual(len(ds_va), 60 - 10 + 1)
        last_tr = ds_tr[len(ds_tr) - 1][0].numpy(); first_va = ds_va[0].numpy()
        self.assertTrue(np.array_equal(last_tr, e.train_z[230:240]))
        self.assertTrue(np.array_equal(first_va, e.val_z[0:10]))
        # every val window row index maps to raw rows >= boundary; every train window < boundary
        self.assertTrue(np.array_equal(first_va, e.val_z[:10]))
        self.assertFalse(np.array_equal(first_va[0], e.train_z[-1]))
        # val windows carry no env ids (plain tensor), train windows carry (x, env)
        self.assertIsInstance(ds_tr[0], tuple); self.assertFalse(isinstance(ds_va[0], tuple))

    def test_scale_none_split(self):
        cfg = _cfg(self.tmp.name, val=True, frac=0.25, scale='none')
        e = load_entity(cfg, 'ent')
        self.assertEqual(e.val_boundary, 225)
        self.assertTrue(np.array_equal(e.train_z, self.train[:225].astype(np.float32), equal_nan=True))
        self.assertTrue(np.array_equal(e.val_z, self.train[225:].astype(np.float32), equal_nan=True))

    def test_expected_n_guard(self):
        cfg = _cfg(self.tmp.name); cfg.DATA.EXPECTED_N = 51
        with self.assertRaises(ValueError):
            load_entity(cfg, 'ent')
        cfg.DATA.EXPECTED_N = 5
        load_entity(cfg, 'ent')  # ok


class TestPriorCacheKey(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.train, _, _ = _make_npz(os.path.join(self.tmp.name, 'ent.npz'))

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_key_unchanged_vs_legacy(self):
        cfg = _cfg(self.tmp.name)
        for name in ['PSM', 'SMD', 'SWaT']:
            cfg.DATA.NAME = name
            self.assertEqual(_prior_cache_key(cfg, self.train, 'ent'), _legacy_prior_cache_key(cfg, self.train, 'ent'))
            self.assertEqual(_prior_cache_key(cfg, self.train, 'ent', split_id='full'),
                             _legacy_prior_cache_key(cfg, self.train, 'ent'))
        cfg.PICAAD.PRIOR.TYPE = 'te'
        self.assertEqual(_prior_cache_key(cfg, self.train, 'ent'), _legacy_prior_cache_key(cfg, self.train, 'ent'))

    @unittest.skipUnless(os.path.exists(GOLDEN_FIXTURE), 'Phase-0 golden fixture not available')
    def test_full_key_matches_phase0_golden(self):
        cfg = get_cfg_defaults(); cfg.merge_from_file(os.path.join(REPO, 'scripts/configs/psm_cf.yaml'))
        cfg.DATA.INPUT_DIR = os.path.dirname(GOLDEN_FIXTURE); cfg.DATA.ENTITIES = 'synth'
        e = load_entity(cfg, 'synth')
        self.assertEqual(_prior_cache_key(cfg, e.train_z, 'synth', split_id=split_id_for(cfg, e)), GOLDEN_KEY)

    def test_val_key_separated_by_data_split_and_pcmci(self):
        cfg_off = _cfg(self.tmp.name, val=False); cfg_on = _cfg(self.tmp.name, val=True, frac=0.2)
        e_off = load_entity(cfg_off, 'ent'); e_on = load_entity(cfg_on, 'ent')
        k_full = _prior_cache_key(cfg_off, e_off.train_z, 'ent', split_id=split_id_for(cfg_off, e_off))
        k_val = _prior_cache_key(cfg_on, e_on.train_z, 'ent', split_id=split_id_for(cfg_on, e_on))
        self.assertNotEqual(k_full, k_val)
        self.assertIn('_val0.2_b240_', k_val); self.assertNotIn('val', k_full)
        # same train_sub bytes but 'full' tag -> different key (split identity matters, not just bytes)
        k_bytes_only = _prior_cache_key(cfg_on, e_on.train_z, 'ent', split_id='full')
        self.assertNotEqual(k_bytes_only, k_val)
        # deterministic
        self.assertEqual(k_val, _prior_cache_key(cfg_on, e_on.train_z, 'ent', split_id=split_id_for(cfg_on, e_on)))
        # different FRAC -> different data and id
        cfg_on2 = _cfg(self.tmp.name, val=True, frac=0.3); e_on2 = load_entity(cfg_on2, 'ent')
        self.assertNotEqual(k_val, _prior_cache_key(cfg_on2, e_on2.train_z, 'ent', split_id=split_id_for(cfg_on2, e_on2)))
        # different PCMCI alpha -> different key, same split id
        cfg_a = _cfg(self.tmp.name, val=True, frac=0.2); cfg_a.PICAAD.PRIOR.PCMCI.ALPHA = 0.01
        k_alpha = _prior_cache_key(cfg_a, e_on.train_z, 'ent', split_id=split_id_for(cfg_a, e_on))
        self.assertNotEqual(k_val, k_alpha); self.assertIn('_val0.2_b240_', k_alpha)

    def test_cached_builder_writes_separate_files(self):
        cache_dir = os.path.join(self.tmp.name, 'cache')
        cfg_off = _cfg(self.tmp.name, val=False); cfg_on = _cfg(self.tmp.name, val=True)
        for c in (cfg_off, cfg_on):
            c.PICAAD.PRIOR.CACHE_DIR = cache_dir
        e_off = load_entity(cfg_off, 'ent'); e_on = load_entity(cfg_on, 'ent')
        calls = []

        def fake_prior(cfg, train_TN):
            calls.append(train_TN.shape[0])
            N = train_TN.shape[1]; tau = cfg.PICAAD.TAU_MAX
            w = np.full((tau, N, N), float(train_TN.shape[0]), np.float32)
            return w, (w > 0).astype(np.float32)

        with mock.patch('model.build.build_causal_prior', side_effect=fake_prior):
            w_full, _ = build_causal_prior_cached(cfg_off, e_off.train_z, 'ent', split_id=split_id_for(cfg_off, e_off))
            w_val, _ = build_causal_prior_cached(cfg_on, e_on.train_z, 'ent', split_id=split_id_for(cfg_on, e_on))
            # second calls must be cache hits (no new build)
            build_causal_prior_cached(cfg_off, e_off.train_z, 'ent', split_id=split_id_for(cfg_off, e_off))
            w_val2, _ = build_causal_prior_cached(cfg_on, e_on.train_z, 'ent', split_id=split_id_for(cfg_on, e_on))
        self.assertEqual(calls, [300, 240])                      # prior fit on full (300) and train_sub (240) exactly once each
        files = sorted(f for f in os.listdir(cache_dir) if f.endswith('.npz'))   # .lock files live beside the caches
        self.assertEqual(len(files), 2)
        self.assertEqual(sum('val0.2_b240' in f for f in files), 1)
        self.assertEqual(float(w_full[0, 0, 0]), 300.0); self.assertEqual(float(w_val[0, 0, 0]), 240.0)
        self.assertTrue(np.array_equal(w_val, w_val2))


class TestCfValConfigs(unittest.TestCase):
    def test_cf_val_yaml_only_differs_in_allowed_keys(self):
        allowed = {'DATA.INPUT_DIR', 'DATA.EXPECTED_N', 'TRAIN.EVAL_EVERY',
                   'VAL.ENABLE', 'VAL.FRAC', 'VAL.SAVE_EVERY_EPOCH', 'VAL.SAVE_EVERY_N'}
        expect_dir = {'psm': 'data_npz/PSM', 'smd': 'data_npz/SMD', 'swat': 'data_npz/SWaT51'}

        def flat(node, prefix=''):
            out = {}
            for k, v in node.items():
                key = f'{prefix}{k}'
                if hasattr(v, 'items'): out.update(flat(v, key + '.'))
                else: out[key] = v
            return out

        for ds in ['psm', 'smd', 'swat']:
            base = get_cfg_defaults(); base.merge_from_file(os.path.join(REPO, f'scripts/configs/{ds}_cf.yaml'))
            val = get_cfg_defaults(); val.merge_from_file(os.path.join(REPO, f'scripts/configs/{ds}_cf_val.yaml'))
            fb, fv = flat(base), flat(val)
            diff = {k for k in fb if fb[k] != fv[k]}
            self.assertTrue(diff <= allowed, f'{ds}: unexpected diffs {diff - allowed}')
            self.assertTrue(val.VAL.ENABLE); self.assertEqual(val.VAL.FRAC, 0.2)
            self.assertFalse(val.VAL.SAVE_EVERY_EPOCH); self.assertEqual(val.VAL.SAVE_EVERY_N, 0)
            self.assertEqual(val.TRAIN.EVAL_EVERY, 0)
            self.assertEqual(val.DATA.INPUT_DIR, expect_dir[ds])
            # native CF settings preserved
            self.assertEqual(val.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH, 0)
            self.assertFalse(val.PICAAD.SCORING.CALIBRATE); self.assertTrue(val.PICAAD.SCORING.USE_COUNTERFACTUAL)
            self.assertEqual(val.SOLVER.MAX_EPOCH, base.SOLVER.MAX_EPOCH); self.assertEqual(val.SOLVER.BASE_LR, base.SOLVER.BASE_LR)
            self.assertEqual(val.PICAAD.CAUSAL_MASK_WARMUP, base.PICAAD.CAUSAL_MASK_WARMUP)
        swat = get_cfg_defaults(); swat.merge_from_file(os.path.join(REPO, 'scripts/configs/swat_cf_val.yaml'))
        self.assertEqual(swat.DATA.EXPECTED_N, 51)


if __name__ == '__main__':
    unittest.main()
