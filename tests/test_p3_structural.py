"""Tests for the P3 structural ablation (no prior / matched random prior / delta removed).

Synthetic fixture, CPU only. No real-data training and no test-set evaluation of real data.
Covers docs/p3_structural_ablation_protocol.md section 3:

  T1 test_invariance_*        no-prior model ignores whatever sits in the te_prior_* buffers
                              (forward, losses, gradients, interventions, reference update, CF sources)
                              and a run is unaffected by a PCMCI+ prior present in the cache
  T2 test_init_*              same seed: parameters untouched by set_te_prior are identical across arms, and
                              A = N + the exact prior terms (paths 1-3)
  T3 test_forward_*           no-prior routing / gate / attention mask equations
  T4 test_objective_*         every arm trains on the prediction loss only (all other loss groups exactly 0)
  T5 test_ckpt_*              checkpoint payload: prior_info, prior_cache_key, prior buffers
  T6 test_eval_*              eval_ckpt.py restores every arm, CF off -> zero CF forwards, no-prior provenance
  T8 test_rewire_*            randomized prior invariants, determinism, RNG isolation
  T9 test_data_order_*        arms a/n/r see identical batches (d documented to differ)
     test_configs_*           generated configs/manifests: only the arm keys differ; prediction-only flags;
                              launcher plan expansion
     test_default_path_matches_base   optional cross-commit regression (set PICAAD_BASE_REPO to a 49f630a checkout)

Run:
  CUDA_VISIBLE_DEVICES= python -m unittest tests.test_p3_structural -v
"""
import copy
import glob
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import torch
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from config import get_cfg_defaults                                       # noqa: E402
from layers.ops import normalize_causal_tensor_torch                      # noqa: E402
import model.build as build_mod                                           # noqa: E402
from model.build import _prior_cache_key, apply_prior_to_model, build_model   # noqa: E402
from model.modeling_picaad import PICAAD                                  # noqa: E402
from model.prior_randomize import (degree_preserving_rewire, prepare_seed_prior,   # noqa: E402
                                   randomize_seed, rewire_checks)
from tests.test_phase1b_val_trainer import _base_cfg, _synth_npz          # noqa: E402

PRIOR_TOUCHED = {'pred_logits', 'edge_log_alpha', 'causal_mask_logits', 'te_prior_weight', 'te_prior_gate',
                 '_has_te_prior', 'cls_ref', '_has_cls_ref'}


# ----------------------------------------------------------------------------- helpers
def _state_hashes(model):
    return {k: hashlib.sha256(v.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
            for k, v in model.state_dict().items()}


def _sd_hash(sd):
    h = hashlib.sha256()
    for k in sorted(sd):
        h.update(k.encode())
        h.update(sd[k].detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def _p3_cfg(tmp, arm, max_epoch=2, perm=0, start_cls=99999, run_name=None):
    cfg = _base_cfg(tmp, max_epoch=max_epoch)
    cfg.PICAAD.ENABLE_PRIOR_LOSS = False
    cfg.PICAAD.START_CLS_EPOCH = start_cls
    cfg.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH = perm
    cfg.PICAAD.SCORING.CALIBRATE = False
    cfg.PICAAD.SCORING.USE_COUNTERFACTUAL = False
    cfg.PICAAD.SCORING.SCORE_GAMMA = 0.0
    cfg.PICAAD.PRIOR.TYPE = 'none' if arm == 'n' else 'pcmci'
    cfg.PICAAD.PRIOR.RANDOMIZE = 'degree_preserving_v1' if arm == 'r' else 'none'
    cfg.PICAAD.DYNAMIC_GRAPH = True
    cfg.PICAAD.USE_DYNAMIC_DELTA = arm != 'd'
    cfg.RESULT_DIR = os.path.join(tmp, run_name or f'run_{arm}')
    cfg.TRAIN.CKPT_DIR = os.path.join(cfg.RESULT_DIR, 'ckpt')
    return cfg


def _run_main(cfg):
    """main.main() on the synthetic fixture with every test-evaluation entry point blocked (as in phase1b)."""
    import main as main_mod
    import trainer as trainer_mod

    def _raise(name):
        def f(*a, **k):
            raise AssertionError(f'{name} must not be called under VAL.ENABLE=True')
        return f
    cfg = cfg.clone()
    cfg.freeze()
    os.makedirs(cfg.RESULT_DIR, exist_ok=True)
    with mock.patch.object(main_mod, '_final_eval', _raise('main._final_eval')), \
         mock.patch.object(main_mod, 'score_windows', _raise('main.score_windows')), \
         mock.patch.object(main_mod, 'counterfactual_score_windows', _raise('main.counterfactual_score_windows')), \
         mock.patch.object(trainer_mod, 'run_epoch_eval', _raise('trainer.run_epoch_eval')), \
         mock.patch.object(main_mod, 'load_config', lambda args: (cfg, None)), \
         mock.patch.object(sys, 'argv', ['main.py']), \
         mock.patch.dict(os.environ, {'CUDA_VISIBLE_DEVICES': ''}):
        main_mod.main()
    ck = torch.load(os.path.join(cfg.TRAIN.CKPT_DIR, 'synth_seed0_best_val.pt'), map_location='cpu', weights_only=False)
    vm = pd.read_csv(os.path.join(cfg.RESULT_DIR, 'synth_seed0_val_metrics.csv'))
    return ck, vm


def _random_prior(rng, T=5, N=12, density=0.12, half_frac=0.2, self_lags=(0, 2)):
    """Synthetic prior shaped like priors.py output: normalized weights over (tau, src) per target, gates in
    {0, 0.5, 1}, lag-1 self loops with mass, some self edges at other lags."""
    raw = np.zeros((T, N, N))
    gate = np.zeros((T, N, N), np.float32)
    m = rng.random((T, N, N)) < density
    for tau in range(T):
        np.fill_diagonal(m[tau], False)
    raw[m] = rng.uniform(0.05, 0.6, size=int(m.sum()))
    gate[m] = np.where(rng.random(int(m.sum())) < half_frac, 0.5, 1.0)
    d = np.arange(N)
    for tau in self_lags:
        raw[tau, d, d] = rng.uniform(0.2, 0.5, size=N)
        gate[tau, d, d] = 1.0 if tau > 0 else 0.0           # lag-1 self loop: weight only (gate set by set_te_prior)
    flat = raw.reshape(T * N, N)
    flat = flat / flat.sum(axis=0, keepdims=True)
    return flat.reshape(T, N, N).astype(np.float32), gate


# ----------------------------------------------------------------------------- T8 randomized prior
class TestRewire(unittest.TestCase):
    def test_rewire_invariants_synthetic(self):
        rng = np.random.default_rng(0)
        moved_tot = edges_tot = 0
        for trial in range(12):
            w, g = _random_prior(rng, N=int(rng.integers(5, 25)), density=float(rng.uniform(0.03, 0.25)))
            w2, g2, st = degree_preserving_rewire(w, g, np.random.default_rng(trial), swaps_per_edge=10)
            c = st['checks']
            for k, v in c.items():
                if k == 'column_sums_max_abs_diff':
                    self.assertLess(v, 1e-6)
                else:
                    self.assertIs(v, True, f'trial {trial}: {k}')
            self.assertEqual(c, rewire_checks(w, g, w2, g2))
            for p in st['per_lag']:
                # rewiring is only possible with enough edges in a lag; every such lag must change
                if p['cross_edges'] >= 8:
                    self.assertGreater(p['slots_with_new_source'], 0, f'trial {trial}: {p}')
                    moved_tot += p['slots_with_new_source']; edges_tot += p['cross_edges']
        # small random graphs can wander back towards the input; in aggregate most slots must have moved
        self.assertGreater(moved_tot, 0.6 * edges_tot, (moved_tot, edges_tot))

    def test_rewire_invariants_shipped_priors(self):
        files = sorted(glob.glob(os.path.join(REPO, 'pretrained_priors', '*.npz')))
        if not files:
            self.skipTest('no pretrained_priors/*.npz in this checkout')
        for f in files[:6]:
            with np.load(f) as d:
                w, g = d['te_weight'], d['te_gate']
            w2, g2, st = degree_preserving_rewire(w, g, np.random.default_rng(1), 10)
            self.assertTrue(all(v is True for k, v in st['checks'].items() if k != 'column_sums_max_abs_diff'), f)
            self.assertLess(st['checks']['column_sums_max_abs_diff'], 1e-6, f)
            for p in st['per_lag']:
                if p['cross_edges'] >= 8:
                    self.assertGreater(p['slots_with_new_source'], 0.5 * p['cross_edges'], f'{f}: {p}')

    PRESERVED = ('out_degree_per_lag_source', 'out_degree_per_source_all_lags', 'in_degree_per_lag_target',
                 'edges_per_lag', 'cross_edges_per_lag', 'self_edges_every_lag', 'weight_multiset_per_lag_target',
                 'gate_multiset_per_lag_target', 'weight_multiset_per_lag', 'weight_multiset_global',
                 'in_strength_per_lag_target', 'column_sum_per_target', 'half_gate_count')
    NOT_PRESERVED = ('weight_multiset_per_lag_source', 'weight_multiset_per_source', 'out_strength_per_lag_source')

    def test_rewire_report_exact_and_changed(self):
        """Item 4: which statistics are kept exactly (always True) and which are not (False once edges move)."""
        from model.prior_randomize import rewire_report
        rng = np.random.default_rng(21)
        seen_false = {k: False for k in self.NOT_PRESERVED}
        for trial in range(8):
            w, g = _random_prior(rng, N=int(rng.integers(10, 30)), density=float(rng.uniform(0.05, 0.2)))
            w2, g2, _ = degree_preserving_rewire(w, g, np.random.default_rng(100 + trial), 10)
            r = rewire_report(w, g, w2, g2)
            for k in self.PRESERVED:
                self.assertIs(r['exact'][k], True, f'trial {trial}: {k}')
            for k in self.NOT_PRESERVED:
                seen_false[k] |= (r['exact'][k] is False)
            c = r['changed']
            self.assertLess(c['cross_support_jaccard'], 1.0)
            self.assertEqual(len(c['reciprocal_cross_pairs']), 2)
        self.assertTrue(all(seen_false.values()), seen_false)
        same = rewire_report(w, g, w, g)                               # identity: everything preserved
        self.assertTrue(all(same['exact'].values()))
        self.assertEqual(same['changed']['cross_support_jaccard'], 1.0)

    def test_rewire_deterministic_and_seed_specific(self):
        cfg = get_cfg_defaults(); cfg.DATA.NAME = 'SMD'; cfg.PICAAD.PRIOR.RANDOMIZE = 'degree_preserving_v1'
        w, g = _random_prior(np.random.default_rng(3), N=20, density=0.15)
        a1 = prepare_seed_prior(cfg, w, g, 'machine-1-1', 0)
        a2 = prepare_seed_prior(cfg, w, g, 'machine-1-1', 0)
        b = prepare_seed_prior(cfg, w, g, 'machine-1-1', 1)
        e = prepare_seed_prior(cfg, w, g, 'machine-1-2', 0)
        self.assertTrue(np.array_equal(a1[0], a2[0]) and np.array_equal(a1[1], a2[1]))
        self.assertEqual(a1[2]['weight_sha256'], a2[2]['weight_sha256'])
        self.assertNotEqual(a1[2]['weight_sha256'], b[2]['weight_sha256'])
        self.assertNotEqual(a1[2]['weight_sha256'], e[2]['weight_sha256'])
        self.assertEqual(a1[2]['rng_seed'], randomize_seed('p3-random-v1', 'SMD', 'machine-1-1', 0))

    def test_rewire_does_not_touch_global_rng(self):
        cfg = get_cfg_defaults(); cfg.PICAAD.PRIOR.RANDOMIZE = 'degree_preserving_v1'
        w, g = _random_prior(np.random.default_rng(4))
        torch.manual_seed(7); np.random.seed(7); random.seed(7)
        before = (torch.get_rng_state().clone(), np.random.get_state()[1].copy(), random.getstate())
        prepare_seed_prior(cfg, w, g, 'e', 0)
        self.assertTrue(torch.equal(before[0], torch.get_rng_state()))
        self.assertTrue(np.array_equal(before[1], np.random.get_state()[1]))
        self.assertEqual(before[2], random.getstate())

    def test_prepare_default_and_none_paths(self):
        cfg = get_cfg_defaults()
        w, g = _random_prior(np.random.default_rng(5))
        w1, g1, info = prepare_seed_prior(cfg, w, g, 'e', 0)
        self.assertIs(w1, w); self.assertIs(g1, g)
        self.assertEqual((info['type'], info['randomize']), ('pcmci', 'none'))
        cfg.PICAAD.PRIOR.TYPE = 'none'
        self.assertEqual(prepare_seed_prior(cfg, None, None, 'e', 0), (None, None, {'type': 'none', 'randomize': 'none'}))
        with self.assertRaises(ValueError):
            prepare_seed_prior(cfg, w, g, 'e', 0)                      # arrays must not reach a no-prior run
        cfg.PICAAD.PRIOR.RANDOMIZE = 'degree_preserving_v1'
        with self.assertRaises(ValueError):
            prepare_seed_prior(cfg, None, None, 'e', 0)                # randomize needs a prior
        cfg.PICAAD.PRIOR.TYPE = 'pcmci'; cfg.PICAAD.PRIOR.RANDOMIZE = 'shuffle'
        with self.assertRaises(ValueError):
            prepare_seed_prior(cfg, w, g, 'e', 0)


# ----------------------------------------------------------------------------- T1/T2/T3 model level
class TestNoPriorModel(unittest.TestCase):
    def setUp(self):
        self.cfg = get_cfg_defaults()
        self.N = 7
        self.w, self.g = _random_prior(np.random.default_rng(11), T=self.cfg.PICAAD.TAU_MAX, N=self.N, density=0.2)

    def _model(self, seed=0, prior=None, dynamic=True, delta=True):
        cfg = self.cfg.clone(); cfg.PICAAD.DYNAMIC_GRAPH = dynamic; cfg.PICAAD.USE_DYNAMIC_DELTA = delta
        torch.manual_seed(seed); np.random.seed(seed); random.seed(seed)
        m = build_model(cfg, N=self.N)
        if prior is not None:
            m.set_te_prior(torch.from_numpy(prior[0]), torch.from_numpy(prior[1]), init_scale=cfg.PICAAD.PRIOR.INIT_SCALE)
        return m

    def test_build_and_buffers_no_prior(self):
        cfg = self.cfg.clone(); cfg.PICAAD.PRIOR.TYPE = 'none'
        m = build_model(cfg, N=self.N)
        with mock.patch.object(PICAAD, 'set_te_prior', side_effect=AssertionError('set_te_prior called')):
            apply_prior_to_model(cfg, m, None, None)
        self.assertFalse(m.has_te_prior); self.assertFalse(m.has_cls_ref)
        for b in ('te_prior_weight', 'te_prior_gate', 'cls_ref'):
            self.assertEqual(float(getattr(m, b).abs().sum()), 0.0, b)
        cfg.PICAAD.PRIOR.TYPE = 'pcmci'
        with self.assertRaises(ValueError):
            apply_prior_to_model(cfg, m, None, None)

    def test_cached_builder_no_io_for_none(self):
        tmp = tempfile.mkdtemp(prefix='p3_cache_')
        try:
            cfg = self.cfg.clone(); cfg.PICAAD.PRIOR.TYPE = 'none'; cfg.PICAAD.PRIOR.CACHE_DIR = os.path.join(tmp, 'c')
            boom = mock.Mock(side_effect=AssertionError('prior machinery touched'))
            with mock.patch.object(build_mod, 'build_causal_prior', boom), \
                 mock.patch.object(build_mod, '_prior_cache_key', boom), \
                 mock.patch.object(build_mod.np, 'load', boom):
                self.assertEqual(build_mod.build_causal_prior_cached(cfg, np.zeros((50, 3), np.float32), 'x', 'val0.2_b40'),
                                 (None, None))
            self.assertFalse(os.path.exists(cfg.PICAAD.PRIOR.CACHE_DIR))
            self.assertEqual(build_mod.build_causal_prior(cfg, np.zeros((5, 3))), (None, None))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_invariance_buffers_do_not_leak(self):
        """T1 at model level: every read of te_prior_* must be gated by has_te_prior. A no-prior model whose
        buffers are overwritten with arbitrary priors (flag still False) must behave bit-identically."""
        from model.intervention import permutation_alignment_and_epoch_cls
        from model.scoring import _select_cf_sources
        X = torch.randn(16, self.cfg.PICAAD.L, self.N, generator=torch.Generator().manual_seed(3))
        outs = []
        for variant in ('zeros', 'real', 'noise'):
            m = self._model(seed=0)
            if variant == 'real':
                m.te_prior_weight.copy_(torch.from_numpy(self.w)); m.te_prior_gate.copy_(torch.from_numpy(self.g))
            elif variant == 'noise':
                m.te_prior_weight.copy_(torch.rand(m.te_prior_weight.shape)); m.te_prior_gate.copy_(torch.rand(m.te_prior_gate.shape))
            self.assertFalse(m.has_te_prior)
            m._current_epoch = 3                                   # causal attention mask ramp active
            m.train()
            torch.manual_seed(5)
            out = m(X)
            pred, pw, es = out[1], out[3], out[6]
            lw, lg = m.causal_prior_losses(pw)
            loss = (X[:, -1, :] - pred).abs().mean() + lw + lg
            m.zero_grad(); loss.backward()
            grads = {k: p.grad.detach().clone() for k, p in m.named_parameters() if p.grad is not None}
            rng = np.random.default_rng(9)
            torch.manual_seed(6)
            lp, cs, cc = permutation_alignment_and_epoch_cls(m, X, X[:, -1, :], (X[:, -1, :] - pred).abs().detach(),
                                                             es, rng, perm_pairs=3, perm_mode='permute')
            with torch.no_grad():
                eff = m._effective_gate().clone()
                srcs = _select_cf_sources(m, 3)
            outs.append((pred.detach(), pw.detach(), float(lw), float(lg), grads, float(lp), cs, cc, eff, srcs))
        ref = outs[0]
        for o in outs[1:]:
            self.assertTrue(torch.equal(ref[0], o[0]) and torch.equal(ref[1], o[1]))
            self.assertEqual(ref[2:4], o[2:4]); self.assertEqual(ref[2], 0.0)
            self.assertEqual(set(ref[4]), set(o[4]))
            for k in ref[4]:
                self.assertTrue(torch.equal(ref[4][k], o[4][k]), k)
            self.assertEqual(ref[5], o[5]); self.assertTrue(torch.equal(ref[6], o[6]) and torch.equal(ref[7], o[7]))
            self.assertTrue(torch.equal(ref[8], o[8])); self.assertEqual(ref[9], o[9])

    def test_invariance_reference_update(self):
        """trainer._update_epoch_refs must not fall back to te_prior_weight when has_te_prior is False."""
        import trainer as trainer_mod
        res = []
        for variant in ('zeros', 'real'):
            m = self._model(seed=0)
            if variant == 'real':
                m.te_prior_weight.copy_(torch.from_numpy(self.w))
            tr = trainer_mod.PicaadTrainer.__new__(trainer_mod.PicaadTrainer)
            tr.model, tr.cfg, tr.device = m, self.cfg, torch.device('cpu')
            T, N = m.tau_max, m.N
            tr._update_epoch_refs(torch.rand(T, N, N, generator=torch.Generator().manual_seed(1)), 1,
                                  torch.zeros(T, N, N), torch.zeros(T, N, 1))
            res.append((m.cls_ref.clone(), m.has_cls_ref))
        self.assertTrue(torch.equal(res[0][0], res[1][0]) and res[0][1] and res[1][1])

    def test_init_equivalence_across_arms(self):
        """T2: same seed -> identical parameters except those set_te_prior writes, and A = N + exact prior terms."""
        n = self._model(seed=0)
        a = self._model(seed=0, prior=(self.w, self.g))
        wr, gr, _ = degree_preserving_rewire(self.w, self.g, np.random.default_rng(2), 10)
        r = self._model(seed=0, prior=(wr, gr))
        hn, ha, hr = _state_hashes(n), _state_hashes(a), _state_hashes(r)
        for k in hn:
            if k not in PRIOR_TOUCHED:
                self.assertEqual(hn[k], ha[k], k); self.assertEqual(hn[k], hr[k], k)
        init_scale = self.cfg.PICAAD.PRIOR.INIT_SCALE
        w = normalize_causal_tensor_torch(torch.from_numpy(self.w).clamp_min(0.0))
        g = torch.from_numpy(self.g).clone()
        d = torch.arange(self.N); g[0, d, d] = 1.0
        gc = g.clamp(1e-4, 1.0 - 1e-4)
        exp_pl = n.pred_logits.detach().clone().add_(float(init_scale) * torch.log(w.clamp_min(1e-8)))
        exp_ea = n.edge_log_alpha.detach().clone().add_(0.5 * float(init_scale) * torch.log(gc / (1.0 - gc)))
        self.assertTrue(torch.equal(a.pred_logits.detach(), exp_pl))
        self.assertTrue(torch.equal(a.edge_log_alpha.detach(), exp_ea))
        self.assertTrue(torch.equal(a.causal_mask_logits.detach(), torch.log(gc / (1.0 - gc)) * 0.5))
        self.assertEqual(float(n.causal_mask_logits.detach().abs().sum()), 0.0)

    def test_forward_equations_no_prior(self):
        """T3: routing = softmax_(tau,src)(pred_logits + delta + log(sigmoid(edge_log_alpha) + 1e-12)); gate =
        sigmoid(edge_log_alpha); attention mask depends on causal_mask_logits only (constant at init)."""
        m = self._model(seed=0)
        m.eval(); m._current_epoch = 5
        X = torch.randn(4, self.cfg.PICAAD.L, self.N, generator=torch.Generator().manual_seed(4))
        with torch.no_grad():
            self.assertTrue(torch.equal(m._effective_gate(), torch.sigmoid(m.edge_log_alpha)))
            delta = torch.randn(4, m.tau_max, self.N, self.N, generator=torch.Generator().manual_seed(1))
            pw = m.get_pred_weights(local_delta=delta)
            T, N = m.tau_max, m.N
            s = (m.pred_logits.unsqueeze(0) + delta + torch.log(torch.sigmoid(m.edge_log_alpha) + 1e-12).unsqueeze(0))
            s = s.reshape(4, T * N, N) / max(m.pred_temp, 1e-6)
            exp = torch.softmax(s, dim=1).reshape(4, T, N, N)
            self.assertTrue(torch.allclose(pw, exp, atol=1e-6))
            mask = m._causal_attn_mask(1)
            self.assertTrue(torch.allclose(mask, torch.full_like(mask, float(mask.flatten()[0]))))
            out = m(X)
            self.assertTrue(all(torch.isfinite(t).all() for t in (out[1], out[3])))

    def test_delta_removed_model(self):
        """Arm D: dynamic_q/k are built (as in A) but delta is never added -> static routing weights."""
        m = self._model(seed=0, prior=(self.w, self.g), delta=False)
        self.assertTrue(hasattr(m, 'dynamic_q') and hasattr(m, 'dynamic_k'))
        X = torch.randn(4, self.cfg.PICAAD.L, self.N)
        with torch.no_grad():
            C = torch.randn(4, m.tau_max, self.N, m.d)
            self.assertIsNone(m._compute_dynamic_delta(C))
            self.assertEqual(m(X)[3].dim(), 3)                      # static routing weights [tau, src, tgt]

    def test_d_init_and_rng_identical_to_a(self):
        """Same seed: arm D (USE_DYNAMIC_DELTA=False) has exactly A's initial state and leaves the global RNG where A
        leaves it (so the DataLoader shuffles identically). Building without q/k (DYNAMIC_GRAPH=False, the first
        implementation) changes edge_value_head and the RNG state - the cause of the A/D mismatch."""
        def built(**kw):
            m = self._model(seed=0, **kw)
            return m.state_dict(), torch.get_rng_state().clone()
        sa, ra = built()
        sd, rd = built(delta=False)
        so, ro = built(dynamic=False)
        self.assertEqual(sorted(sa), sorted(sd))
        for k in sa:
            self.assertTrue(torch.equal(sa[k], sd[k]), k)
        self.assertTrue(torch.equal(ra, rd))
        self.assertFalse(torch.equal(ra, ro))
        self.assertEqual(sorted(k for k in so if not torch.equal(sa[k], so[k])), ['edge_value_head.bias', 'edge_value_head.weight'])
        self.assertEqual(sorted(set(sa) - set(so)), ['dynamic_k.weight', 'dynamic_q.weight'])

    def test_d_forward_equals_a_without_delta(self):
        """D's forward == A's forward with delta forced to None (same parameters)."""
        a = self._model(seed=0, prior=(self.w, self.g))
        d = self._model(seed=0, prior=(self.w, self.g), delta=False)
        X = torch.randn(4, self.cfg.PICAAD.L, self.N, generator=torch.Generator().manual_seed(8))
        a.eval(); d.eval(); a._current_epoch = d._current_epoch = 3
        with torch.no_grad(), mock.patch.object(PICAAD, '_compute_dynamic_delta', lambda self_, C: None):
            ya = a(X)
        with torch.no_grad():
            yd = d(X)
            self.assertFalse(torch.equal(a(X)[1], yd[1]))            # delta really matters for A
        for i in (1, 3, 6):
            self.assertTrue(torch.equal(ya[i], yd[i]), i)


# ----------------------------------------------------------------------------- end-to-end (synthetic)
class TestEndToEndArms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='p3_e2e_')
        os.makedirs(os.path.join(cls.tmp, 'npz'))
        _synth_npz(os.path.join(cls.tmp, 'npz', 'synth.npz'))
        cls.runs, cls.batches = {}, {}
        orig_forward = PICAAD.forward
        for arm in ('a', 'n', 'r', 'd'):
            seen = []

            def rec(self_, X, *a, _seen=seen, **k):
                if self_.training and len(_seen) < 12:
                    _seen.append(hashlib.sha256(X.detach().cpu().numpy().tobytes()).hexdigest())
                return orig_forward(self_, X, *a, **k)
            with mock.patch.object(PICAAD, 'forward', rec):
                cls.runs[arm] = _run_main(_p3_cfg(cls.tmp, arm))
            cls.batches[arm] = seen
        # T1 end-to-end: a PCMCI+ prior sitting in the cache must not change a no-prior run
        cfg = _p3_cfg(cls.tmp, 'n', run_name='run_n_poisoned')
        pc = cfg.clone(); pc.PICAAD.PRIOR.TYPE = 'pcmci'
        from datasets.build import load_entity
        from datasets.split import split_id_for
        e = load_entity(pc, 'synth')
        key = _prior_cache_key(pc, e.train_z, e.name, split_id=split_id_for(pc, e))
        cls.poison = os.path.join(cfg.PICAAD.PRIOR.CACHE_DIR, f'{key}.npz')
        assert os.path.exists(cls.poison), 'arm a/r runs should have cached the synthetic PCMCI+ prior'
        cls.poison_sha = hashlib.sha256(open(cls.poison, 'rb').read()).hexdigest()
        loads = []
        real_load = np.load

        def spy_load(p, *a, **k):
            loads.append(str(p)); return real_load(p, *a, **k)
        with mock.patch.object(build_mod.np, 'load', spy_load):
            cls.runs['n_poisoned'] = _run_main(cfg)
        cls.poison_loads = [p for p in loads if 'prior_cache' in p]
        # same with interventions + CRS on (stage-2 shape): no prior may enter sampling / reference / cstruct
        cls.runs['n_perm2'] = _run_main(_p3_cfg(cls.tmp, 'n', perm=2, start_cls=1, run_name='run_n_perm2'))
        cls.runs['n_perm2_b'] = _run_main(_p3_cfg(cls.tmp, 'n', perm=2, start_cls=1, run_name='run_n_perm2_b'))
        # arm D must be exactly "arm A with delta switched off"
        with mock.patch.object(PICAAD, '_compute_dynamic_delta', lambda self_, C: None):
            cls.runs['a_nodelta'] = _run_main(_p3_cfg(cls.tmp, 'a', run_name='run_a_nodelta'))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_invariance_cached_prior_never_read(self):
        ck0, vm0 = self.runs['n']; ck1, vm1 = self.runs['n_poisoned']
        self.assertEqual(self.poison_loads, [])
        self.assertEqual(hashlib.sha256(open(self.poison, 'rb').read()).hexdigest(), self.poison_sha)
        self.assertEqual(_sd_hash(ck0['state_dict']), _sd_hash(ck1['state_dict']))
        pd.testing.assert_frame_equal(vm0, vm1)

    def test_invariance_perm2_no_prior_reproducible(self):
        (c0, v0), (c1, v1) = self.runs['n_perm2'], self.runs['n_perm2_b']
        self.assertEqual(_sd_hash(c0['state_dict']), _sd_hash(c1['state_dict']))
        pd.testing.assert_frame_equal(v0, v1)
        self.assertGreater(v0['perm'].abs().sum(), 0.0)                 # interventions really ran (uniform sampling)
        self.assertEqual(float(c0['state_dict']['te_prior_weight'].abs().sum()), 0.0)

    def test_objective_prediction_only(self):
        """T4: total loss == prediction loss; prior/CRS/intervention/graph groups exactly 0 for every arm."""
        for arm in ('a', 'n', 'r', 'd'):
            _, vm = self.runs[arm]
            for col in ('group_causal', 'group_graphreg', 'group_robust', 'cstruct', 'perm'):
                self.assertEqual(float(vm[col].abs().max()), 0.0, f'{arm}:{col}')
            self.assertTrue(np.allclose(vm['loss_total'], vm['group_task'], rtol=0, atol=1e-12), arm)
            self.assertEqual(len(vm), 2)

    def test_ckpt_prior_info(self):
        """T5."""
        ck_a, ck_n, ck_r, ck_d = (self.runs[k][0] for k in 'anrd')
        self.assertEqual(ck_n['prior_info'], {'type': 'none', 'randomize': 'none'})
        self.assertIsNone(ck_n['prior_cache_key'])
        sd = ck_n['state_dict']
        self.assertFalse(bool(sd['_has_te_prior'].item()))
        self.assertEqual(float(sd['te_prior_weight'].abs().sum() + sd['te_prior_gate'].abs().sum()), 0.0)
        for ck in (ck_a, ck_d):
            pi = ck['prior_info']
            self.assertEqual((pi['type'], pi['randomize']), ('pcmci', 'none'))
            self.assertEqual(pi['weight_sha256'], pi['input_weight_sha256'])
            self.assertIsNotNone(ck['prior_cache_key'])
        self.assertEqual(ck_a['prior_cache_key'], ck_r['prior_cache_key'])      # R starts from the same cached prior
        pr = ck_r['prior_info']
        self.assertEqual(pr['randomize'], 'degree_preserving_v1')
        self.assertEqual(pr['input_weight_sha256'], ck_a['prior_info']['weight_sha256'])
        self.assertTrue(all(v is True for k, v in pr['checks'].items() if k != 'column_sums_max_abs_diff'))
        # the model buffers hold the randomized prior that prior_info describes
        cfg = get_cfg_defaults(); cfg.set_new_allowed(True); cfg.merge_from_other_cfg(cfg.load_cfg(ck_r['cfg']))
        with np.load(os.path.join(cfg.PICAAD.PRIOR.CACHE_DIR, ck_r['prior_cache_key'] + '.npz')) as cache:
            w0, g0 = cache['te_weight'], cache['te_gate']
        wr, gr, info = prepare_seed_prior(cfg, w0, g0, 'synth', 0)
        self.assertEqual(info['weight_sha256'], pr['weight_sha256'])
        exp = normalize_causal_tensor_torch(torch.from_numpy(wr).clamp_min(0.0))
        self.assertTrue(torch.equal(ck_r['state_dict']['te_prior_weight'], exp))
        # D keeps dynamic_q/k; they never receive gradients, so they stay at their (A-identical) initial values
        cfg_d = _p3_cfg(self.tmp, 'd')
        torch.manual_seed(0); np.random.seed(0); random.seed(0)
        fresh = build_model(cfg_d, N=6).state_dict()
        for k in ('dynamic_q.weight', 'dynamic_k.weight'):
            self.assertTrue(torch.equal(ck_d['state_dict'][k], fresh[k]), k)
        self.assertFalse(torch.equal(ck_a['state_dict']['dynamic_q.weight'], fresh['dynamic_q.weight']))
        rep_ = pr['report']['exact']
        for k in ('out_degree_per_lag_source', 'in_degree_per_lag_target', 'edges_per_lag', 'self_edges_every_lag',
                  'weight_multiset_per_lag_target', 'weight_multiset_per_lag', 'weight_multiset_global',
                  'column_sum_per_target'):
            self.assertTrue(rep_[k], k)

    def test_eval_all_arms_cf_off(self):
        """T6: eval_ckpt restores every arm; CF off -> no CF forward; no-prior provenance."""
        import scripts.eval_ckpt as ev
        for arm in ('a', 'n', 'r', 'd'):
            cfg = _p3_cfg(self.tmp, arm)
            out = os.path.join(self.tmp, f'eval_{arm}')
            df, prov = ev.evaluate(os.path.join(cfg.TRAIN.CKPT_DIR, 'synth_seed0_best_val.pt'), out,
                                   data_input_dir=os.path.join(self.tmp, 'npz'), cf='off', device='cpu', calibrate='off')
            self.assertIn('P_raw', set(df['variant']))
            self.assertFalse(any('cf' in k.lower() for k in prov['forward_passes']), prov['forward_passes'])
            self.assertEqual(prov['restore']['flags']['has_te_prior'], arm != 'n')
            self.assertEqual(prov['checkpoint']['prior_info']['type'], 'none' if arm == 'n' else 'pcmci')
            if arm == 'n':
                self.assertIsNone(prov['checkpoint']['prior_cache_key'])
        with self.assertRaises(ev.EvalError):
            ev.evaluate(os.path.join(_p3_cfg(self.tmp, 'n').TRAIN.CKPT_DIR, 'synth_seed0_best_val.pt'),
                        os.path.join(self.tmp, 'eval_n_cf'), data_input_dir=os.path.join(self.tmp, 'npz'),
                        cf='both', device='cpu', calibrate='off')

    def test_data_order_same_for_all_arms(self):
        """T9: arms a, n, r and d consume identical batches (prior handling uses no global RNG; d builds q/k)."""
        self.assertGreaterEqual(len(self.batches['a']), 6)
        for arm in 'nrd':
            self.assertEqual(self.batches['a'], self.batches[arm], arm)

    def test_d_equals_a_with_delta_switched_off(self):
        """Training arm D == training arm A with delta forced to None: identical checkpoint state and val curve."""
        (cd, vd), (cx, vx) = self.runs['d'], self.runs['a_nodelta']
        self.assertEqual(_sd_hash(cd['state_dict']), _sd_hash(cx['state_dict']))
        pd.testing.assert_frame_equal(vd, vx)
        self.assertNotEqual(_sd_hash(cd['state_dict']), _sd_hash(self.runs['a'][0]['state_dict']))

    def test_init_state_same_for_all_arms_outside_prior_params(self):
        """Initial non-prior parameters of a/n/r/d are identical (checked on the epoch-0 rebuild with the same seed)."""
        hs = {}
        for arm in 'anrd':
            cfg = _p3_cfg(self.tmp, arm)
            torch.manual_seed(0); np.random.seed(0); random.seed(0)
            m = build_model(cfg, N=6)
            hs[arm] = {k: v for k, v in _state_hashes(m).items() if k not in PRIOR_TOUCHED}
        for arm in 'nrd':
            self.assertEqual(hs['a'], hs[arm], arm)


# ----------------------------------------------------------------------------- configs / manifests
class TestConfigsAndManifests(unittest.TestCase):
    @staticmethod
    def _flat(d, p=''):
        out = {}
        for k, v in d.items():
            if isinstance(v, dict):
                out.update(TestConfigsAndManifests._flat(v, f'{p}{k}.'))
            else:
                out[f'{p}{k}'] = v
        return out

    def test_configs_generated_and_only_arm_keys_differ(self):
        import scripts.make_p3_configs as gen
        confs = gen.generated_configs()
        self.assertEqual(len(confs), 12)
        by_ds = {}
        for rel, (ds, arm, merged, base_rel) in confs.items():
            with open(os.path.join(REPO, rel)) as f:
                self.assertEqual(yaml.safe_load(f), merged, f'{rel} differs from the generator (hand edit?)')
            by_ds.setdefault(ds, {})[arm] = self._flat(merged)
        for ds, arms in by_ds.items():
            keys = set().union(*[set(v) for v in arms.values()])
            diff = sorted(k for k in keys if len({repr(a.get(k)) for a in arms.values()}) > 1)
            self.assertEqual(diff, sorted(gen.ARM_KEYS), ds)

    def test_configs_resolved_prediction_only(self):
        """Resolve every config through the real loader (utils/parser.load_config) as main.py does."""
        from utils.parser import load_config, parse_args
        lr = {'psm': 5e-05, 'smd': 5e-04, 'swat': 5e-04}
        tmp = tempfile.mkdtemp(prefix='p3_cfg_')
        self.addCleanup(shutil.rmtree, tmp, True)
        for path in sorted(glob.glob(os.path.join(REPO, 'scripts/configs/p3_structural/*.yaml'))):
            # the same CLI overrides the launcher passes to main.py
            argv = ['main.py', '--cfg', path, 'SEEDS', '[0]', 'RESULT_DIR', tmp, 'RESULT_DIR_LITERAL', 'True',
                    'DATA_LOADER.NUM_WORKERS', '0']
            with mock.patch.object(sys, 'argv', argv):
                cfg, _ = load_config(parse_args())
            P = cfg.PICAAD
            self.assertFalse(P.ENABLE_PRIOR_LOSS); self.assertEqual(P.START_CLS_EPOCH, 99999)
            self.assertEqual(P.INTERVENTION.PERM_PAIRS_PER_BATCH, 0)
            self.assertFalse(P.SCORING.CALIBRATE); self.assertFalse(P.SCORING.USE_COUNTERFACTUAL)
            self.assertFalse(P.ENABLE_GATE_LOSS or P.ENABLE_GRAPH_LOSS or P.ENABLE_LAGMONO_LOSS or P.ENABLE_INV_LOSS)
            self.assertEqual(cfg.SOLVER.MAX_EPOCH, 80); self.assertTrue(cfg.VAL.ENABLE); self.assertEqual(cfg.VAL.FRAC, 0.2)
            self.assertEqual(cfg.VAL.MIN_DELTA, 0.0); self.assertEqual(cfg.VAL.SELECTION_METRIC, 'pred_mae')
            ds = os.path.basename(path).split('_')[0]
            self.assertAlmostEqual(cfg.SOLVER.BASE_LR, lr[ds], msg=path)
            arm = os.path.basename(path).split('_p3_')[1][0]
            self.assertEqual(P.PRIOR.TYPE, 'none' if arm == 'n' else 'pcmci')
            self.assertEqual(P.PRIOR.RANDOMIZE, 'degree_preserving_v1' if arm == 'r' else 'none')
            self.assertTrue(P.DYNAMIC_GRAPH)
            self.assertEqual(P.USE_DYNAMIC_DELTA, arm != 'd')

    def test_manifests_plan(self):
        import scripts.run_experiments as rx
        SMD28 = [f'machine-{g}-{i}' for g, n in [(1, 8), (2, 9), (3, 11)] for i in range(1, n + 1)]
        want = {'p3_structural_psm_ks.yaml': (16, ['PSM'], [0, 1, 2, 3]),
                'p3_structural_smd_ks.yaml': (448, SMD28, [0, 1, 2, 3]),
                'p3_structural_swat_ks.yaml': (8, ['swat'], [0, 1])}
        tmp = tempfile.mkdtemp(prefix='p3_plan_')
        try:
            for name, (n_train, ents, seeds) in want.items():
                path = os.path.join(REPO, 'scripts/manifests/multiserver', name)
                man = rx.load_manifest(path)
                self.assertEqual(man['defaults']['eval'], {'ckpt_tags': ['best_val'], 'cf': 'off', 'calibrate': 'off',
                                                           'verify_native_parity': False})
                for spec in man['train']:
                    self.assertTrue(os.path.exists(os.path.join(REPO, spec['config'])), spec['config'])
                    self.assertEqual(spec['entities'], ents); self.assertEqual(spec['seeds'], seeds)
                a = rx.build_parser().parse_args(['--manifest', path, '--out_root', os.path.join(tmp, name),
                                                  '--data_root', os.path.join(tmp, 'data'), '--dry-run'])
                plan = rx.Plan(man, a)
                kinds = [j.kind for j in plan.jobs]
                self.assertEqual(kinds.count('train'), n_train, name)
                self.assertEqual(kinds.count('eval'), n_train, name)       # best_val only
                for j in plan.jobs:
                    if j.kind == 'eval':
                        self.assertIn('--cf', j.cmd); self.assertEqual(j.cmd[j.cmd.index('--cf') + 1], 'off')
                        self.assertEqual(j.cmd[j.cmd.index('--calibrate') + 1], 'off')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------------- cross-commit regression (optional)
@unittest.skipUnless(os.environ.get('PICAAD_BASE_REPO'), 'set PICAAD_BASE_REPO to a checkout of 49f630a')
class TestDefaultPathMatchesBase(unittest.TestCase):
    """With PRIOR.TYPE=pcmci and RANDOMIZE=none this branch must train bit-identically to the base commit."""

    SCRIPT = r'''
import os, sys, json, hashlib, torch, numpy as np, pandas as pd
repo, tmp, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, repo); os.chdir(repo)
from unittest import mock
from tests.test_phase1b_val_trainer import _base_cfg
import main as M, trainer as T
cfg = _base_cfg(tmp, max_epoch=3)
for k, v in [('PICAAD.ENABLE_PRIOR_LOSS', False), ('PICAAD.START_CLS_EPOCH', 99999)]:
    cfg.merge_from_list([k, v])
cfg.RESULT_DIR = out; cfg.TRAIN.CKPT_DIR = os.path.join(out, 'ckpt'); cfg.freeze(); os.makedirs(out, exist_ok=True)
with mock.patch.object(M, 'load_config', lambda a: (cfg, None)), mock.patch.object(sys, 'argv', ['main.py']):
    M.main()
ck = torch.load(os.path.join(out, 'ckpt', 'synth_seed0_best_val.pt'), map_location='cpu', weights_only=False)
h = hashlib.sha256()
for k in sorted(ck['state_dict']):
    h.update(k.encode()); h.update(ck['state_dict'][k].contiguous().numpy().tobytes())
vm = pd.read_csv(os.path.join(out, 'synth_seed0_val_metrics.csv'))
print(json.dumps({'state': h.hexdigest(), 'val': vm['val_pred_mae'].tolist(), 'epoch': ck['epoch']}))
'''

    def test_default_path_matches_base(self):
        tmp = tempfile.mkdtemp(prefix='p3_base_')
        try:
            os.makedirs(os.path.join(tmp, 'npz'))
            _synth_npz(os.path.join(tmp, 'npz', 'synth.npz'))
            res = {}
            for tag, repo in (('base', os.environ['PICAAD_BASE_REPO']), ('branch', REPO)):
                env = dict(os.environ, CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1')
                p = subprocess.run([sys.executable, '-c', self.SCRIPT, repo, tmp, os.path.join(tmp, tag)],
                                   capture_output=True, text=True, env=env, check=True)
                res[tag] = json.loads(p.stdout.strip().splitlines()[-1])
            self.assertEqual(res['base'], res['branch'])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
