"""Tests for the soft-prior 2x2 pilot (forward prior smoothing + effective-gate floor).

Synthetic fixture, CPU only. No real-data training and no test-set evaluation.
Covers the validation list in docs/soft_prior_2x2_protocol.md section 9:

  1 test_t0_*           T0 == native noalign: forward, loss, short-training regression
  2 test_formula_*      exact p_rho / G_floor formula, shape and range
  3 test_zero_options_* rho=0 / g_min=0 keep the original code path (bit-identical)
  4 test_init_state_*   four conditions share one initial state; buffers untouched
    test_buffers_*
  5 test_ckpt_*         options persisted in the checkpoint; strict restore + current_epoch
  6 test_cache_key_*    prior cache key and input data identical across conditions
  7 test_probe_*        probing does not mutate RNG / parameters / buffers
  8 test_eval_cf_off_*  pilot evaluation performs zero CF fitting/forward calls

Run:
  CUDA_VISIBLE_DEVICES= python -m unittest tests.test_soft_prior_2x2 -v
"""
import copy
import hashlib
import json
import os
import random
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import torch
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from config import get_cfg_defaults                                   # noqa: E402
from datasets.build import load_entity                                # noqa: E402
from model.build import _prior_cache_key, build_model                 # noqa: E402
from model.modeling_picaad import PICAAD                              # noqa: E402
from tests.test_phase1b_val_trainer import _base_cfg, _synth_npz      # noqa: E402

CONDITIONS = {"T0": (0.0, 0.0), "T1": (0.05, 0.0), "T2": (0.0, 0.05), "T3": (0.05, 0.05)}
GATE_FLOOR_STRUCT = 0.05          # the structural coefficient, which must NOT change
EPS_PRIOR = 1e-8


def _state_hash(model):
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode())
        h.update(np.ascontiguousarray(v.detach().cpu().numpy()).tobytes())
    return h.hexdigest()


def _pilot_cfg(tmp, rho=0.0, gmin=0.0, max_epoch=2):
    """Pilot fixed conditions on the synthetic fixture."""
    cfg = _base_cfg(tmp, max_epoch=max_epoch)
    cfg.PICAAD.ENABLE_PRIOR_LOSS = False
    cfg.PICAAD.START_CLS_EPOCH = max_epoch + 1       # cstruct never active
    cfg.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH = 0
    cfg.PICAAD.ENABLE_GATE_LOSS = False
    cfg.PICAAD.ENABLE_GRAPH_LOSS = False
    cfg.PICAAD.ENABLE_LAGMONO_LOSS = False
    cfg.PICAAD.ENABLE_INV_LOSS = False
    cfg.PICAAD.SCORING.CALIBRATE = False
    cfg.PICAAD.SCORING.USE_COUNTERFACTUAL = False
    cfg.PICAAD.SCORING.SCORE_GAMMA = 0.0
    cfg.PICAAD.PRIOR.SMOOTH_RHO = rho
    cfg.PICAAD.EFF_GATE_FLOOR = gmin
    cfg.TRAIN.EVAL_EVERY = 0
    return cfg


def _seeded_model(cfg, entity, seed=0, with_w_ref=False):
    """Build + prior-initialize deterministically, exactly as main.py would.

    with_w_ref=True additionally populates w_ref, mirroring the post-epoch state
    that a real best_val checkpoint carries (trainer._update_epoch_refs sets
    has_w_ref on the first epoch). scripts/eval_ckpt.restore_model requires all
    three reference flags, so checkpoint fixtures need it.
    """
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    model = build_model(cfg, entity.N)
    from model.build import build_causal_prior_cached
    from datasets.split import split_id_for
    te_w, te_g = build_causal_prior_cached(cfg, entity.train_z, entity.name,
                                           split_id=split_id_for(cfg, entity))
    model.set_te_prior(torch.from_numpy(te_w), torch.from_numpy(te_g),
                       init_scale=cfg.PICAAD.PRIOR.INIT_SCALE)
    model.reset_refs()
    if with_w_ref:
        with torch.no_grad():
            model.w_ref.copy_(model.get_pred_weights().detach())
            model.has_w_ref = True
    return model


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="sp2x2_")
        os.makedirs(os.path.join(cls.tmp, "npz"))
        _synth_npz(os.path.join(cls.tmp, "npz", "synth.npz"))
        cls.cfg0 = _pilot_cfg(cls.tmp)
        cls.entity = load_entity(cls.cfg0, "synth")
        cls.X = torch.from_numpy(
            np.stack([cls.entity.train_z[i:i + cls.cfg0.PICAAD.L] for i in range(0, 64)]).astype(np.float32))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def model_for(self, rho, gmin):
        return _seeded_model(_pilot_cfg(self.tmp, rho, gmin), self.entity)


# ---------------------------------------------------------------- 2. formulas
class TestFormulas(_Base):
    def test_formula_p_rho_exact_shape_range(self):
        for rho in (0.0, 0.05, 0.3, 1.0):
            m = self.model_for(rho, 0.0)
            w = m.te_prior_weight
            D = m.tau_max * m.N
            expect = (1.0 - rho) * w + rho * (1.0 / D)
            got = m._routing_prior_weight()
            self.assertEqual(tuple(got.shape), tuple(w.shape), f"shape mismatch at rho={rho}")
            self.assertEqual(got.dtype, w.dtype)
            self.assertTrue(torch.allclose(got, expect, atol=0, rtol=0),
                            f"p_rho not exact at rho={rho}")
            self.assertGreaterEqual(float(got.min()), 0.0)
            self.assertLessEqual(float(got.max()), 1.0)

    def test_formula_p_rho_columns_sum_to_one(self):
        """te_prior_weight columns sum to 1 over D entries, so p_rho does too:
        (1-rho)*1 + rho*D*(1/D) = 1. No renormalization is needed."""
        for rho in (0.0, 0.05, 0.5, 1.0):
            m = self.model_for(rho, 0.0)
            D = m.tau_max * m.N
            col = m._routing_prior_weight().reshape(D, m.N).double().sum(dim=0)
            self.assertTrue(torch.allclose(col, torch.ones_like(col), atol=1e-6),
                            f"column sums off at rho={rho}: {col}")

    def test_formula_p_rho_uniform_at_rho_one(self):
        m = self.model_for(1.0, 0.0)
        D = m.tau_max * m.N
        self.assertTrue(torch.allclose(m._routing_prior_weight(),
                                       torch.full_like(m.te_prior_weight, 1.0 / D), atol=0))

    def test_formula_p_rho_lifts_zero_entries_above_clamp(self):
        """The point of smoothing: entries that were exactly 0 (and therefore hit
        clamp_min(1e-8) in the prior bias) become rho/D > 1e-8."""
        m0, m1 = self.model_for(0.0, 0.0), self.model_for(0.05, 0.0)
        zero = (m0.te_prior_weight == 0)
        self.assertTrue(bool(zero.any()), "fixture has no zero prior entries")
        self.assertTrue(torch.all(m0._routing_prior_weight()[zero] <= EPS_PRIOR))
        lifted = m1._routing_prior_weight()[zero]
        self.assertTrue(torch.all(lifted > EPS_PRIOR))
        D = m1.tau_max * m1.N
        self.assertTrue(torch.allclose(lifted, torch.full_like(lifted, 0.05 / D), atol=0))

    def test_formula_G_floor_exact_shape_range(self):
        for gmin in (0.0, 0.05, 0.5):
            m = self.model_for(0.0, gmin)
            native = torch.sigmoid(m.edge_log_alpha) * (GATE_FLOOR_STRUCT
                                                        + (1.0 - GATE_FLOOR_STRUCT) * m.te_prior_gate)
            expect = native if gmin <= 0.0 else gmin + (1.0 - gmin) * native
            got = m._effective_gate()
            self.assertEqual(tuple(got.shape), tuple(m.edge_log_alpha.shape))
            self.assertTrue(torch.allclose(got, expect, atol=0, rtol=0),
                            f"G_floor not exact at g_min={gmin}")
            self.assertGreaterEqual(float(got.min()), gmin - 1e-12, f"below floor at g_min={gmin}")
            self.assertLessEqual(float(got.max()), 1.0 + 1e-12)

    def test_formula_G_floor_keeps_structural_coefficients(self):
        """g_min must not be implemented by changing the 0.05/0.95 structural
        coefficients: with g_min=0 the gate is exactly the native product, and
        the in/out ratio of the native part is unchanged for any g_min."""
        m0 = self.model_for(0.0, 0.0)
        native = torch.sigmoid(m0.edge_log_alpha) * (0.05 + 0.95 * m0.te_prior_gate)
        self.assertTrue(torch.allclose(m0._effective_gate(), native, atol=0))
        for gmin in (0.05, 0.5):
            m = self.model_for(0.0, gmin)
            recovered = (m._effective_gate() - gmin) / (1.0 - gmin)
            self.assertTrue(torch.allclose(recovered, native, atol=1e-6),
                            f"native gate not recoverable at g_min={gmin}")

    def test_formula_rejects_out_of_range(self):
        for bad in (-0.01, 1.01):
            with self.assertRaises(ValueError):
                PICAAD(N=4, L=6, tau_max=2, d=8, heads=2, enc_layers=1, dropout=0.0,
                       prior_smooth_rho=bad)
        for bad in (-0.01, 1.0, 1.5):
            with self.assertRaises(ValueError):
                PICAAD(N=4, L=6, tau_max=2, d=8, heads=2, enc_layers=1, dropout=0.0,
                       eff_gate_floor=bad)

    def test_formula_floor_applies_without_prior(self):
        """The floor is defined on the WHOLE effective gate, including the
        has_te_prior=False branch (unused by this pilot, but specified)."""
        m = PICAAD(N=4, L=6, tau_max=2, d=8, heads=2, enc_layers=1, dropout=0.0,
                   eff_gate_floor=0.2)
        self.assertFalse(m.has_te_prior)
        g = m._effective_gate()
        self.assertTrue(torch.allclose(g, 0.2 + 0.8 * torch.sigmoid(m.edge_log_alpha), atol=0))


# ------------------------------------------------- 3. zero options == original
class TestZeroOptions(_Base):
    def test_zero_options_return_buffer_identity(self):
        """rho=0 returns the te_prior_weight buffer object itself, so the
        original expression is evaluated with no extra arithmetic."""
        m = self.model_for(0.0, 0.0)
        self.assertIs(m._routing_prior_weight(), m.te_prior_weight)

    def test_zero_options_gate_bit_identical_to_original(self):
        m = self.model_for(0.0, 0.0)
        original = m.edge_gate() * (0.05 + 0.95 * m.te_prior_gate)
        self.assertTrue(torch.equal(m._effective_gate(), original))

    def test_zero_options_weights_bit_identical_to_original(self):
        """Pi under rho=0,g_min=0 must equal the pre-change expression exactly."""
        m = self.model_for(0.0, 0.0)
        m.eval()
        with torch.no_grad():
            _, _, C_all, pw, *_ = m(self.X)
            delta = m._compute_dynamic_delta(C_all)
            gate = m.edge_gate() * (0.05 + 0.95 * m.te_prior_gate)
            prior_bias = m.te_prior_blend * torch.log(m.te_prior_weight.clamp_min(1e-8))
            score = m.pred_logits.unsqueeze(0) + prior_bias.unsqueeze(0) + delta
            ref = m._normalize_weight_tensor(score, gate)
        self.assertTrue(torch.equal(pw, ref), "rho=0/g_min=0 diverges from the original formula")

    def test_zero_options_nonzero_changes_weights(self):
        """Sanity: the options are actually wired into the forward pass."""
        base = None
        for name, (rho, gmin) in CONDITIONS.items():
            m = self.model_for(rho, gmin)
            m.eval()
            with torch.no_grad():
                pw = m(self.X)[3]
            if name == "T0":
                base = pw
            else:
                self.assertFalse(torch.equal(pw, base), f"{name} produced identical Pi to T0")


# ------------------------------- 4. shared initial state / untouched buffers
class TestInitStateAndBuffers(_Base):
    def test_init_state_identical_across_four_conditions(self):
        hashes = {}
        for name, (rho, gmin) in CONDITIONS.items():
            hashes[name] = _state_hash(self.model_for(rho, gmin))
        self.assertEqual(len(set(hashes.values())), 1,
                         f"initial state differs across conditions: {hashes}")

    def test_init_state_options_absent_from_state_dict(self):
        m = self.model_for(0.05, 0.05)
        keys = set(m.state_dict().keys())
        for forbidden in ("prior_smooth_rho", "eff_gate_floor"):
            self.assertNotIn(forbidden, keys)
            self.assertFalse(any(forbidden in k for k in keys))

    def test_buffers_prior_and_reference_untouched_by_options(self):
        ref = self.model_for(0.0, 0.0)
        for name, (rho, gmin) in CONDITIONS.items():
            m = self.model_for(rho, gmin)
            for buf in ("te_prior_weight", "te_prior_gate", "cls_ref", "w_ref"):
                self.assertTrue(torch.equal(getattr(m, buf), getattr(ref, buf)),
                                f"{name}: buffer {buf} differs")

    def test_buffers_not_written_by_forward(self):
        for name, (rho, gmin) in CONDITIONS.items():
            m = self.model_for(rho, gmin)
            before = {b: getattr(m, b).clone() for b in
                      ("te_prior_weight", "te_prior_gate", "cls_ref", "w_ref")}
            m.eval()
            with torch.no_grad():
                m(self.X)
                m._routing_prior_weight()
                m._effective_gate()
            for b, v in before.items():
                self.assertTrue(torch.equal(getattr(m, b), v), f"{name}: forward wrote {b}")

    def test_buffers_prior_losses_use_raw_prior(self):
        """causal_prior_losses must keep using the raw prior, not p_rho."""
        m0, m1 = self.model_for(0.0, 0.0), self.model_for(0.05, 0.0)
        pw = torch.rand(m0.tau_max, m0.N, m0.N)
        pw = pw / pw.reshape(m0.tau_max * m0.N, m0.N).sum(0).view(1, 1, m0.N)
        a_w, a_g = m0.causal_prior_losses(pw.clone())
        b_w, b_g = m1.causal_prior_losses(pw.clone())
        self.assertAlmostEqual(float(a_w), float(b_w), places=12)
        self.assertAlmostEqual(float(a_g), float(b_g), places=12)

    def test_init_state_set_te_prior_unchanged_by_rho(self):
        """psi / edge_log_alpha / causal_mask_logits initialization must not move."""
        ref = self.model_for(0.0, 0.0)
        for rho, gmin in CONDITIONS.values():
            m = self.model_for(rho, gmin)
            for p in ("pred_logits", "edge_log_alpha", "causal_mask_logits"):
                self.assertTrue(torch.equal(getattr(m, p), getattr(ref, p)),
                                f"{p} initialization changed at rho={rho}, g_min={gmin}")


# ------------------------------------------- 6. prior cache key / input data
class TestCacheKey(_Base):
    def test_cache_key_identical_across_conditions(self):
        keys = set()
        for rho, gmin in CONDITIONS.values():
            cfg = _pilot_cfg(self.tmp, rho, gmin)
            keys.add(_prior_cache_key(cfg, self.entity.train_z, self.entity.name, split_id="val0.2_b480"))
        self.assertEqual(len(keys), 1, f"prior cache key depends on the pilot options: {keys}")

    def test_cache_key_input_data_identical_across_conditions(self):
        hashes, mus, sds = set(), set(), set()
        for rho, gmin in CONDITIONS.values():
            e = load_entity(_pilot_cfg(self.tmp, rho, gmin), "synth")
            hashes.add(hashlib.sha256(np.ascontiguousarray(e.train_z).tobytes()).hexdigest())
            mus.add(hashlib.sha256(np.ascontiguousarray(e.mu).tobytes()).hexdigest())
            sds.add(hashlib.sha256(np.ascontiguousarray(e.sd).tobytes()).hexdigest())
            self.assertEqual(e.val_boundary, self.entity.val_boundary)
        self.assertEqual(len(hashes), 1)
        self.assertEqual(len(mus), 1)
        self.assertEqual(len(sds), 1)


# ------------------------------------------------------ 7. non-invasive probes
class TestProbeIsAnInspection(_Base):
    def test_probe_does_not_mutate_rng_params_or_buffers(self):
        m = self.model_for(0.05, 0.05)
        sh_before = _state_hash(m)
        torch.manual_seed(1234)
        rng_before = torch.get_rng_state().clone()
        py_before, np_before = random.getstate(), np.random.get_state()

        m.eval()
        with torch.no_grad():
            m(self.X)
            m._routing_prior_weight()
            m._effective_gate()
            m.get_pred_weights()

        self.assertEqual(sh_before, _state_hash(m))
        self.assertTrue(torch.equal(rng_before, torch.get_rng_state()))
        self.assertEqual(py_before, random.getstate())
        self.assertEqual(str(np_before), str(np.random.get_state()))

    def test_probe_grad_is_none_under_no_grad(self):
        m = self.model_for(0.05, 0.05)
        m.eval()
        with torch.no_grad():
            m(self.X)
        self.assertTrue(all(p.grad is None for p in m.parameters()))


# ---------------------------------- 1. T0 == native noalign (forward/loss/train)
class TestT0NativeParity(_Base):
    def test_t0_forward_matches_pre_change_model(self):
        """A model whose option attributes are stripped to the pre-change values
        must produce identical outputs to T0 (same seed, same prior)."""
        a = self.model_for(0.0, 0.0)
        b = self.model_for(0.0, 0.0)
        # emulate the pre-change class: no option attributes consulted at all
        b._routing_prior_weight = lambda: b.te_prior_weight
        b._effective_gate = lambda: b.edge_gate() * (0.05 + 0.95 * b.te_prior_gate)
        a.eval(); b.eval()
        with torch.no_grad():
            oa, ob = a(self.X), b(self.X)
        for i, nm in enumerate(["recon", "pred", "C_all", "pred_weights", "edge_value",
                                "edge_effect", "edge_strength", "edge_gate", "local_delta"]):
            if oa[i] is None:
                self.assertIsNone(ob[i]); continue
            self.assertTrue(torch.equal(oa[i], ob[i]), f"T0 differs from native in {nm}")

    def test_t0_prediction_loss_matches_native(self):
        from model.losses import prediction_train_loss
        a, b = self.model_for(0.0, 0.0), self.model_for(0.0, 0.0)
        b._routing_prior_weight = lambda: b.te_prior_weight
        b._effective_gate = lambda: b.edge_gate() * (0.05 + 0.95 * b.te_prior_gate)
        a.eval(); b.eval()
        with torch.no_grad():
            la = prediction_train_loss(self.X[:, -1, :], a(self.X)[1], "l1")
            lb = prediction_train_loss(self.X[:, -1, :], b(self.X)[1], "l1")
        self.assertEqual(float(la), float(lb))

    def test_t0_short_training_regression(self):
        """Two short training runs - one with the pilot options present and set to
        zero, one with them absent from the config entirely - must agree."""
        from model.losses import prediction_train_loss

        def short_train(rho, gmin, steps=6):
            m = self.model_for(rho, gmin)
            opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=0.01)
            m.train()
            losses = []
            for _ in range(steps):
                opt.zero_grad(set_to_none=True)
                loss = prediction_train_loss(self.X[:, -1, :], m(self.X)[1], "l1")
                loss.backward()
                opt.step()
                losses.append(float(loss.detach()))
            return losses, _state_hash(m)

        l0, h0 = short_train(0.0, 0.0)
        l0b, h0b = short_train(0.0, 0.0)
        self.assertEqual(l0, l0b, "T0 training is not deterministic")
        self.assertEqual(h0, h0b)
        l3, h3 = short_train(0.05, 0.05)
        self.assertNotEqual(h0, h3, "options had no effect on training")
        self.assertTrue(all(np.isfinite(l3)), "T3 training produced non-finite loss")
        self.assertLess(l3[-1], l3[0] * 1.5, "T3 training diverged")


# ------------------------------------------------- 5. checkpoint round-trip
class TestCheckpointRoundTrip(_Base):
    def test_ckpt_options_persisted_and_strict_restore(self):
        for name, (rho, gmin) in CONDITIONS.items():
            cfg = _pilot_cfg(self.tmp, rho, gmin)
            m = _seeded_model(cfg, self.entity)
            m._current_epoch = 7
            payload = {
                "protocol": "val_pred_mae_v2", "epoch": 7, "current_epoch": 7,
                "seed": 0, "entity": self.entity.name, "val_mae": 0.5,
                "state_dict": {k: v.detach().cpu().clone() for k, v in m.state_dict().items()},
                "cfg": cfg.dump(),
            }
            path = os.path.join(self.tmp, f"ck_{name}.pt")
            torch.save(payload, path)

            ck = torch.load(path, map_location="cpu", weights_only=False)
            # the options travel inside the cfg dump
            dumped = yaml.safe_load(ck["cfg"])
            self.assertAlmostEqual(dumped["PICAAD"]["PRIOR"]["SMOOTH_RHO"], rho, places=12)
            self.assertAlmostEqual(dumped["PICAAD"]["EFF_GATE_FLOOR"], gmin, places=12)

            cfg2 = get_cfg_defaults()
            cfg2.merge_from_other_cfg(type(cfg2).load_cfg(ck["cfg"]))
            m2 = build_model(cfg2, self.entity.N)
            m2.load_state_dict(ck["state_dict"], strict=True)
            m2._current_epoch = int(ck["current_epoch"])

            self.assertEqual(m2.prior_smooth_rho, rho, f"{name}: rho not restored")
            self.assertEqual(m2.eff_gate_floor, gmin, f"{name}: g_min not restored")
            self.assertEqual(m2._current_epoch, 7)
            self.assertEqual(_state_hash(m2), _state_hash(m), f"{name}: state hash changed")
            m.eval(); m2.eval()
            with torch.no_grad():
                self.assertTrue(torch.equal(m(self.X)[3], m2(self.X)[3]),
                                f"{name}: restored model routes differently")

    def test_ckpt_strict_restore_rejects_extra_key(self):
        cfg = _pilot_cfg(self.tmp, 0.05, 0.05)
        m = _seeded_model(cfg, self.entity)
        sd = {k: v.clone() for k, v in m.state_dict().items()}
        sd["prior_smooth_rho"] = torch.tensor(0.05)      # must not be accepted
        m2 = build_model(cfg, self.entity.N)
        with self.assertRaises(RuntimeError):
            m2.load_state_dict(sd, strict=True)


# ----------------------------------------------- 8. pilot eval: zero CF calls
class TestEvalCfOff(_Base):
    def test_eval_cf_off_makes_zero_cf_calls(self):
        """scripts/eval_ckpt.py --cf off must not call CF fitting or CF forward.

        Both entry points are patched to raise; the run must still succeed and
        its fingerprint must carry no CF phase.
        """
        import scripts.eval_ckpt as ev

        cfg = _pilot_cfg(self.tmp, 0.05, 0.05, max_epoch=2)
        m = _seeded_model(cfg, self.entity, with_w_ref=True)
        payload = {
            "protocol": "val_pred_mae_v2", "epoch": 2, "current_epoch": 2,
            "seed": 0, "entity": self.entity.name, "val_mae": 0.5,
            "state_dict": {k: v.detach().cpu().clone() for k, v in m.state_dict().items()},
            "cfg": cfg.dump(),
            "mu": np.asarray(self.entity.mu, dtype=np.float32),
            "sd": np.asarray(self.entity.sd, dtype=np.float32),
            "split_info": {"val_enabled": True, "val_frac": 0.2,
                           "val_boundary": int(self.entity.val_boundary),
                           "T_train_sub": int(self.entity.T_train),
                           "T_val": int(self.entity.T_val),
                           "T_test": int(self.entity.T_test),
                           "split_id": "x", "fit_protocol": "train_sub_val_v2"},
        }
        ck_path = os.path.join(self.tmp, "ck_eval.pt")
        torch.save(payload, ck_path)
        out_dir = os.path.join(self.tmp, "eval_out_cf_off")

        boom_cf = mock.Mock(side_effect=AssertionError("counterfactual_score_windows called under --cf off"))
        boom_fit = mock.Mock(side_effect=AssertionError("fit_cf_profile called under --cf off"))
        with mock.patch.object(ev, "counterfactual_score_windows", boom_cf), \
             mock.patch.object(ev, "fit_cf_profile", boom_fit):
            ev.evaluate(ck_path, out_dir, data_input_dir=None, cf="off",
                        device="cpu", verify_native_parity=False, save_effects=False,
                        calibrate="off")
        boom_cf.assert_not_called()
        boom_fit.assert_not_called()

        prov = json.load(open(os.path.join(out_dir, "provenance.json")))
        fp = prov.get("forward_counts", prov)
        blob = json.dumps(prov)
        # the base test forward must be recorded, and no CF phase may appear
        self.assertIn("test_base_forward", blob)
        self.assertNotIn("cf_profile_fit_forward", blob)
        self.assertNotIn("test_cf_forward", blob)
        if isinstance(fp, dict):
            self.assertEqual(fp.get("cf_profile_fit_forward", 0), 0)
            self.assertEqual(fp.get("test_cf_forward", 0), 0)
        self.assertEqual(str(prov.get("cf", {}).get("requested", "off")), "off")

        npz = np.load(os.path.join(out_dir, "scores.npz"))
        self.assertIn("P_raw", npz.files)
        self.assertIn("A_off", npz.files)
        self.assertNotIn("CF_raw", npz.files)
        self.assertNotIn("A_on", npz.files)
        # secondary metric definition: A_off == P_raw + C_raw
        self.assertTrue(np.allclose(npz["A_off"], npz["P_raw"] + npz["C_raw"], atol=0))

    def test_eval_cf_on_is_refused_for_pilot_configs(self):
        """USE_COUNTERFACTUAL=False in the pilot configs makes --cf on|both an error,
        so a pilot run cannot silently compute CF."""
        import scripts.eval_ckpt as ev
        cfg = _pilot_cfg(self.tmp, 0.0, 0.0)
        m = _seeded_model(cfg, self.entity, with_w_ref=True)
        payload = {"protocol": "val_pred_mae_v2", "epoch": 1, "current_epoch": 1, "seed": 0,
                   "entity": self.entity.name, "val_mae": 0.5, "cfg": cfg.dump(),
                   "state_dict": {k: v.detach().cpu().clone() for k, v in m.state_dict().items()},
                   "mu": np.asarray(self.entity.mu, dtype=np.float32),
                   "sd": np.asarray(self.entity.sd, dtype=np.float32)}
        p = os.path.join(self.tmp, "ck_refuse.pt")
        torch.save(payload, p)
        for mode in ("on", "both"):
            with self.assertRaises(ev.EvalError):
                ev.evaluate(p, os.path.join(self.tmp, f"eval_refuse_{mode}"), cf=mode, device="cpu")


# ----------------------------------------------------- generated config audit
class TestGeneratedConfigs(unittest.TestCase):
    def test_generated_configs_match_conditions(self):
        want = {"t0": (0.0, 0.0), "t1": (0.05, 0.0), "t2": (0.0, 0.05), "t3": (0.05, 0.05)}
        for ds, base_rel in (("psm", "psm_cf_val"), ("smd", "smd_cf_val"), ("swat", "swat_cf_val")):
            base = get_cfg_defaults()
            base.merge_from_file(os.path.join(REPO, f"scripts/configs/{base_rel}.yaml"))
            for cond, (rho, gmin) in want.items():
                path = os.path.join(REPO, f"scripts/configs/soft_prior_2x2/{ds}_sp2x2_{cond}.yaml")
                self.assertTrue(os.path.exists(path), path)
                c = get_cfg_defaults()
                c.merge_from_file(path)
                self.assertAlmostEqual(c.PICAAD.PRIOR.SMOOTH_RHO, rho, places=12)
                self.assertAlmostEqual(c.PICAAD.EFF_GATE_FLOOR, gmin, places=12)
                # fixed pilot conditions
                self.assertFalse(c.PICAAD.ENABLE_PRIOR_LOSS)
                self.assertEqual(c.PICAAD.START_CLS_EPOCH, 81)
                self.assertEqual(c.SOLVER.MAX_EPOCH, 80)
                self.assertEqual(c.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH, 0)
                self.assertFalse(c.PICAAD.SCORING.CALIBRATE)
                self.assertFalse(c.PICAAD.SCORING.USE_COUNTERFACTUAL)
                self.assertFalse(c.PICAAD.ENABLE_GATE_LOSS)
                self.assertFalse(c.PICAAD.ENABLE_GRAPH_LOSS)
                self.assertFalse(c.PICAAD.ENABLE_LAGMONO_LOSS)
                self.assertFalse(c.PICAAD.ENABLE_INV_LOSS)
                self.assertTrue(c.VAL.ENABLE)
                self.assertEqual(c.SEEDS, [0])
                # per-epoch checkpoints for the epoch 1/5/20/80 diagnostics;
                # output artifact only, so best_val saving must stay intact
                self.assertEqual(c.VAL.SAVE_EVERY_N, 1)
                self.assertFalse(c.VAL.SAVE_EVERY_EPOCH)
                self.assertEqual(c.VAL.SELECTION_METRIC, "pred_mae")
                # the deep merge must preserve every other base key
                self.assertEqual(c.DATA.NAME, base.DATA.NAME)
                self.assertEqual(c.DATA.EXPECTED_N, base.DATA.EXPECTED_N)
                self.assertEqual(c.SOLVER.BASE_LR, base.SOLVER.BASE_LR)
                self.assertEqual(c.TRAIN.BATCH_SIZE, base.TRAIN.BATCH_SIZE)
                self.assertEqual(c.PICAAD.L, base.PICAAD.L)
                self.assertEqual(c.PICAAD.TAU_MAX, base.PICAAD.TAU_MAX)
                self.assertEqual(c.PICAAD.D, base.PICAAD.D)
                self.assertEqual(c.PICAAD.CAUSAL_MASK_WARMUP, base.PICAAD.CAUSAL_MASK_WARMUP)
                self.assertEqual(c.PICAAD.PRIOR.BLEND, base.PICAAD.PRIOR.BLEND)
                self.assertEqual(c.PICAAD.PRIOR.INIT_SCALE, base.PICAAD.PRIOR.INIT_SCALE)
                self.assertEqual(c.PICAAD.PRIOR.PCMCI.SUBSAMPLE, base.PICAAD.PRIOR.PCMCI.SUBSAMPLE)
                self.assertEqual(c.VAL.FRAC, base.VAL.FRAC)

    def test_generated_configs_no_duplicate_top_level_keys(self):
        """A second `PICAAD:` block in the same document would make PyYAML drop
        the first one; the generator must emit one merged document."""
        d = os.path.join(REPO, "scripts/configs/soft_prior_2x2")
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".yaml"):
                continue
            text = open(os.path.join(d, fn)).read()
            keys = [ln.split(":")[0] for ln in text.splitlines()
                    if ln and not ln.startswith((" ", "\t", "#")) and ":" in ln]
            self.assertEqual(len(keys), len(set(keys)), f"{fn}: duplicate top-level keys {keys}")

    def test_manifests_pilot_eval_settings(self):
        for server, n_train in (("ks", 8), ("js", 4)):
            p = os.path.join(REPO, f"scripts/manifests/multiserver/soft_prior_2x2_{server}.yaml")
            m = yaml.safe_load(open(p))
            ev = m["defaults"]["eval"]
            self.assertEqual(ev["ckpt_tags"], ["best_val"], f"{server}: must evaluate best_val only")
            self.assertEqual(str(ev["cf"]), "off", f"{server}: CF must be off")
            self.assertEqual(str(ev["calibrate"]), "off", f"{server}: calibrate must be off")
            self.assertEqual(len(m["train"]), n_train)
            self.assertEqual(m["eval_only"], [])
            for spec in m["train"]:
                self.assertEqual(spec["seeds"], [0])
                self.assertIn("soft_prior_2x2/", spec["config"])
                self.assertTrue(os.path.exists(os.path.join(REPO, spec["config"])))


if __name__ == "__main__":
    unittest.main(verbosity=2)
