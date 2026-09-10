"""Explicit checkpoint evaluation (Phase 2-A): restore a checkpoint, fit the
counterfactual (CF) profile on that checkpoint's normal fitting data, and
score the test set with CF OFF / CF ON on the *same* base forward.

Raw (native uncalibrated) scoring, always computed:
    A_off = P_raw + C_raw
    A_on  = A_off + gamma_CF * CF_raw          (gamma_CF = cfg.PICAAD.SCORING.SCORE_GAMMA)

Calibrated scoring (--calibrate on, or cfg when the checkpoint config has CALIBRATE=True;
default stays CALIBRATE=False), corrected order so that CF is part of the calibrator:
    restore -> CF profile on the normal fitting data -> normal P/C/G/CF raw scores with that
    profile -> fit_score_calibrator (includes CF_raw) -> apply_score_calibrator on test:
    A_off_cal = Pn + Cn                      (gamma=0)
    A_on_cal  = Pn + Cn + gamma_CF * CFn     (native apply_score_calibrator, gamma=SCORE_GAMMA)
  Note: native main._final_eval fits the calibrator *without* the CF profile, so its
  CALIBRATE=True output has no CF term (known defect, left unchanged there).

Checkpoint formats
  * native  (utils/evaluation.run_epoch_eval): epoch, seed, entity, state_dict, metrics, cfg, mu, sd
  * val     (trainer, protocol 'val_pred_mae_v*'): + current_epoch, split_info, val_mae, ...

Selection is explicit: --ckpt <file>  or  --ckpt_dir + --entity + --seed + --ckpt_tag {last,best_val,epNN}.
No test-metric selection, no lexicographic glob pick.

Usage
  python scripts/eval_ckpt.py --ckpt results/parallel/<run>/PSM/seed0/ckpt/PSM_seed0_best_val.pt \
      --out_dir results/eval/<run>/PSM_seed0/best_val
  python scripts/eval_ckpt.py --ckpt_dir <run>/PSM/seed0/ckpt --entity PSM --seed 0 --ckpt_tag ep80 \
      --data_input_dir data_npz/PSM --out_dir results/eval/<run>/PSM_seed0/ep80      # colleague native ckpt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from yacs.config import CfgNode

REPO = str(Path(__file__).resolve().parent.parent)
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from config import get_cfg_defaults                                   # noqa: E402
from datasets.split import split_id_for, split_time_ordered           # noqa: E402
from datasets.util import get_median_anomaly_length, reduce_label     # noqa: E402
from model.build import build_model                                   # noqa: E402
from model.scoring import (                                           # noqa: E402
    apply_score_calibrator, cf_anomaly_score, counterfactual_score_windows,
    fit_cf_profile, fit_score_calibrator, score_components_to_timeline,
    score_windows, score_windows_raw,
)
from utils.evaluation import paper_eval_one                           # noqa: E402

METRIC_KEYS = ['AUC-PR', 'AUC-ROC', 'VUS-PR', 'VUS-ROC', 'Standard-F1', 'PA-F1',
               'Event-based-F1', 'R-based-F1', 'Affiliation-F']
CKPT_BUFFERS = ['cls_ref', 'w_ref', 'te_prior_weight', 'te_prior_gate',
                '_has_cls_ref', '_has_w_ref', '_has_te_prior']


class EvalError(RuntimeError):
    pass


# ----------------------------------------------------------------------------
# selection
# ----------------------------------------------------------------------------
def resolve_ckpt_path(ckpt_dir: str, entity: str, seed: int, tag: str) -> str:
    """Explicit checkpoint file from (dir, entity, seed, tag). tag ∈ {last, best_val, epNN}."""
    if tag in ('last', 'best_val'):
        name = f'{entity}_seed{seed}_{tag}.pt'
    elif re.fullmatch(r'ep\d+', tag):
        name = f'{entity}_seed{seed}_{tag}.pt'
    else:
        raise EvalError(f"unknown --ckpt_tag {tag!r}; use last, best_val or epNN")
    path = os.path.join(ckpt_dir, name)
    if not os.path.exists(path):
        raise EvalError(f'checkpoint not found: {path}')
    return path


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


def _tensor_hash(t: torch.Tensor) -> str:
    return hashlib.sha256(t.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def _git_fingerprint():
    def _run(cmd):
        try:
            return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, cwd=REPO).decode().strip()
        except Exception:
            return None
    st = _run(['git', 'status', '--porcelain', '--untracked-files=no'])
    return {'commit': _run(['git', 'rev-parse', 'HEAD']),
            'modified_tracked': [l.split(None, 1)[1] for l in st.splitlines() if l.strip()] if st else []}


# ----------------------------------------------------------------------------
# restore
# ----------------------------------------------------------------------------
def load_payload(path: str) -> dict:
    ck = torch.load(path, map_location='cpu', weights_only=False)
    for k in ('state_dict', 'cfg', 'mu', 'sd', 'entity'):
        if k not in ck:
            raise EvalError(f'{path}: payload lacks required key {k!r}')
    proto = str(ck.get('protocol', ''))
    ck['_format'] = 'val' if proto.startswith('val_pred_mae') else 'native'
    return ck


def cfg_from_payload(ck: dict, data_input_dir: str | None = None) -> CfgNode:
    """Defaults + the checkpoint's resolved config (unknown keys tolerated,
    missing keys keep defaults). Only the data path may be overridden."""
    cfg = get_cfg_defaults()
    cfg.set_new_allowed(True)
    cfg.merge_from_other_cfg(CfgNode.load_cfg(ck['cfg']))
    cfg.set_new_allowed(False)
    if data_input_dir:
        cfg.DATA.INPUT_DIR = data_input_dir
    if ck['_format'] == 'val':
        si = ck.get('split_info') or {}
        cfg.VAL.ENABLE = True
        cfg.VAL.FRAC = float(si.get('val_frac', cfg.VAL.FRAC))
    else:
        cfg.VAL.ENABLE = False
    return cfg


def resolved_epoch(ck: dict) -> tuple[int, str]:
    """(epoch to restore into model._current_epoch, source). current_epoch
    wins and must agree with epoch; else payload epoch; else error."""
    cur, ep = ck.get('current_epoch'), ck.get('epoch')
    if cur is not None:
        if ep is not None and int(cur) != int(ep):
            raise EvalError(f'current_epoch={cur} != epoch={ep} in payload; refusing to guess')
        return int(cur), 'payload.current_epoch'
    if ep is not None:
        return int(ep), 'payload.epoch'
    raise EvalError('payload has neither current_epoch nor epoch; cannot restore warmup state')


def ckpt_num_vars(ck: dict) -> int:
    sd = ck['state_dict']
    if 'te_prior_weight' in sd:
        return int(sd['te_prior_weight'].shape[-1])
    if 'pred_logits' in sd:
        return int(sd['pred_logits'].shape[-1])
    raise EvalError('cannot infer N from state_dict')


def load_data_with_saved_stats(cfg: CfgNode, ck: dict, tol: float = 1e-5):
    """Raw NPZ -> split per checkpoint split_info -> standardize with the
    *saved* mu/sd. Also recomputes the pipeline's own stats and reports the
    discrepancy; a mismatch beyond ``tol`` is a data-identity error."""
    entity = ck['entity']
    path = os.path.join(cfg.DATA.INPUT_DIR, f'{entity}.npz')
    if not os.path.exists(path):
        raise EvalError(f'entity NPZ not found: {path}')
    d = np.load(path)
    train = d['train'].astype(np.float32); test = d['test'].astype(np.float32)
    if train.ndim == 1: train = train[:, None]
    if test.ndim == 1: test = test[:, None]
    y = reduce_label(d['label'], test.shape[0])
    N_data = train.shape[1]
    mu = np.asarray(ck['mu'], dtype=np.float32).reshape(1, -1)
    sd = np.asarray(ck['sd'], dtype=np.float32).reshape(1, -1)
    N_ckpt = ckpt_num_vars(ck)
    expected_n = int(getattr(cfg.DATA, 'EXPECTED_N', 0) or 0)
    dims = {'N_data': N_data, 'N_ckpt_state': N_ckpt, 'N_mu_sd': int(mu.shape[1]), 'N_expected_cfg': expected_n}
    if not (N_data == N_ckpt == mu.shape[1]) or (expected_n > 0 and N_data != expected_n):
        raise EvalError(
            f'variable-count mismatch {dims} for {path}. No automatic channel selection/'
            f'padding is performed (SWaT must be the 51-channel export data_npz/SWaT51/swat.npz).'
        )
    if cfg.DATA.SCALE != 'standard':
        raise EvalError(f'eval_ckpt supports DATA.SCALE=standard only (got {cfg.DATA.SCALE})')

    # split exactly as recorded
    if ck['_format'] == 'val':
        si = ck['split_info']
        train_sub, val_sub, boundary = split_time_ordered(train, float(si['val_frac']))
        if boundary != int(si['val_boundary']) or train_sub.shape[0] != int(si['T_train_sub']) \
                or val_sub.shape[0] != int(si['T_val']) or test.shape[0] != int(si['T_test']):
            raise EvalError(f'split mismatch: data gives boundary={boundary} T_sub={train_sub.shape[0]} '
                            f'T_val={val_sub.shape[0]} T_test={test.shape[0]} vs split_info={si}')
        fit_raw, fit_protocol = train_sub, 'train_sub_val'
    else:
        train_sub, val_sub, boundary = train, train[0:0], train.shape[0]
        fit_raw, fit_protocol = train, 'full_train_native'

    def _z(x):
        x = np.where(np.isfinite(x), x, np.nan).astype(np.float32)
        x = np.where(np.isnan(x), mu, x).astype(np.float32)
        return ((x - mu) / sd).astype(np.float32)

    fit_z, test_z = _z(fit_raw), _z(test)
    val_z = _z(val_sub) if val_sub.shape[0] else np.empty((0, N_data), np.float32)

    # cross-check against the pipeline's own statistics on the same fitting block
    from datasets.util import standardize_train_test
    _, _, mu_re, sd_re = standardize_train_test(fit_raw, test)
    stats_check = {'max_abs_mu_diff': float(np.max(np.abs(mu_re - mu))), 'max_abs_sd_diff': float(np.max(np.abs(sd_re - sd)))}
    if stats_check['max_abs_mu_diff'] > tol or stats_check['max_abs_sd_diff'] > tol:
        raise EvalError(f'saved mu/sd disagree with statistics recomputed on the recorded fitting block '
                        f'{stats_check} (tol={tol}); data identity or split mismatch')

    class E: pass
    e = E()
    e.name, e.train_z, e.val_z, e.test_z, e.y, e.mu, e.sd = entity, fit_z, val_z, test_z, y, mu, sd
    e.N, e.T_train, e.T_val, e.T_test = N_data, fit_z.shape[0], val_z.shape[0], test_z.shape[0]
    e.val_boundary, e.val_frac = boundary, (float(ck['split_info']['val_frac']) if ck['_format'] == 'val' else 0.0)
    info = {'npz_path': os.path.abspath(path), 'npz_sha256': _sha256_file(path),
            'shapes': {k: list(d[k].shape) for k in d.files}, 'dims': dims, 'fit_protocol': fit_protocol,
            'fit_rows': int(fit_z.shape[0]), 'val_rows': int(val_z.shape[0]), 'test_rows': int(test_z.shape[0]),
            'boundary': int(boundary), 'stats_check': stats_check, 'split_id': split_id_for(cfg, e)}
    return e, info


def restore_model(cfg: CfgNode, ck: dict, device):
    """build_model from the saved config, strict load, restore _current_epoch.
    set_te_prior is NOT called (it would overwrite cls_ref)."""
    N = ckpt_num_vars(ck)
    model = build_model(cfg, N=N).to(device)
    model.load_state_dict(ck['state_dict'], strict=True)
    ep, src = resolved_epoch(ck)
    model._current_epoch = ep
    model.eval()
    flags = {'has_te_prior': model.has_te_prior, 'has_cls_ref': model.has_cls_ref, 'has_w_ref': model.has_w_ref}
    if not all(flags.values()):
        raise EvalError(f'restored model lacks reference buffers: {flags}')
    return model, {'restored_epoch': ep, 'epoch_source': src, 'warmup_ramp': float(model._warmup_ramp()), 'flags': flags}


def snapshot_state(model):
    return {k: _tensor_hash(v) for k, v in model.state_dict().items()}


class ForwardCounter:
    """Counts model forward passes per phase via a forward hook."""
    def __init__(self, model):
        self.counts, self.phase = {}, 'idle'
        self._h = model.register_forward_hook(lambda m, i, o: self.counts.__setitem__(self.phase, self.counts.get(self.phase, 0) + 1))
    def __call__(self, phase): self.phase = phase; return self
    def __enter__(self): return self
    def __exit__(self, *a): self.phase = 'idle'
    def close(self): self._h.remove()


# ----------------------------------------------------------------------------
# evaluation
# ----------------------------------------------------------------------------
def evaluate(ck_path: str, out_dir: str, data_input_dir: str | None = None, cf: str = 'both',
             device: str | None = None, verify_native_parity: bool = False, save_effects: bool = True,
             calibrate: str = 'cfg'):
    """calibrate: 'cfg' (follow checkpoint config, default False), 'off', 'on'."""
    out = Path(out_dir)
    if out.exists() and any(out.iterdir()):
        raise EvalError(f'refusing to write into non-empty out_dir {out} (never overwrite results)')
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    ck = load_payload(ck_path)
    cfg = cfg_from_payload(ck, data_input_dir)
    if calibrate not in ('cfg', 'off', 'on'):
        raise EvalError(f'calibrate must be cfg|off|on, got {calibrate!r}')
    do_calib = bool(cfg.PICAAD.SCORING.CALIBRATE) if calibrate == 'cfg' else (calibrate == 'on')
    use_cf_cfg = bool(cfg.PICAAD.SCORING.USE_COUNTERFACTUAL)
    if cf in ('on', 'both') and not use_cf_cfg:
        raise EvalError('checkpoint config has USE_COUNTERFACTUAL=False; only --cf off is meaningful')
    cfg.freeze()

    dev = torch.device(device or ('cuda' if torch.cuda.is_available() else 'cpu'))
    entity, data_info = load_data_with_saved_stats(cfg, ck)
    model, restore_info = restore_model(cfg, ck, dev)
    state_before = snapshot_state(model)
    counter = ForwardCounter(model)
    scoring = cfg.PICAAD.SCORING
    gamma = float(scoring.SCORE_GAMMA)

    # --- base forward on test (once) ---
    with counter('test_base_forward'):
        raw_test = score_windows_raw(model, entity.test_z, dev, cfg.TEST.BATCH_SIZE, scoring)
    P, C, G = raw_test['P_raw'], raw_test['C_raw'], raw_test['G_raw']
    A_off = (P + C).astype(np.float32)            # native uncalibrated branch: cal["A"] = P + C
    scores = {'P_raw': P, 'C_raw': C, 'G_raw': G, 'A_off': A_off}
    cf_info = {'requested': cf, 'cfg_use_counterfactual': use_cf_cfg}

    # --- CF profile on the checkpoint's normal fitting data, then test CF ---
    if cf in ('on', 'both'):
        with counter('cf_profile_fit_forward'):
            eff_fit, src = counterfactual_score_windows(model, entity.train_z, dev, cfg.TRAIN.BATCH_SIZE,
                                                        top_k=scoring.CF_TOP_K, fill_value=scoring.CF_FILL_VALUE)
        profile = fit_cf_profile(eff_fit)
        with counter('test_cf_forward'):
            eff_test, src_t = counterfactual_score_windows(model, entity.test_z, dev, cfg.TEST.BATCH_SIZE,
                                                           top_k=scoring.CF_TOP_K, fill_value=scoring.CF_FILL_VALUE)
        if list(src) != list(src_t):
            raise EvalError('CF source selection differs between fit and test passes')
        CF = cf_anomaly_score(eff_test, profile)
        A_on = (A_off + float(gamma) * CF).astype(np.float32)   # == native (P + C + gamma*CF) left-to-right
        scores.update({'CF_raw': CF, 'A_on': A_on, 'cf_profile_mean': profile['mean'], 'cf_profile_std': profile['std'],
                       'cf_sources': np.asarray(src, dtype=np.int64)})
        if save_effects:
            scores['cf_effects_fit'] = eff_fit; scores['cf_effects_test'] = eff_test
        cf_info.update({'top_k': int(scoring.CF_TOP_K), 'fill_value': float(scoring.CF_FILL_VALUE), 'gamma': gamma,
                        'sources': [int(s) for s in src], 'fit_windows': int(eff_fit.shape[0]),
                        'profile_mean': [float(x) for x in profile['mean']], 'profile_std': [float(x) for x in profile['std']]})

    # --- calibrated path (corrected order; native fit/apply functions) ---
    calib_info = {'enabled': do_calib, 'requested': calibrate, 'cfg_calibrate': bool(cfg.PICAAD.SCORING.CALIBRATE)}
    calibrator = None
    if do_calib:
        with counter('fit_base_forward'):
            raw_fit = score_windows_raw(model, entity.train_z, dev, cfg.TRAIN.BATCH_SIZE, scoring)
        if cf in ('on', 'both'):
            # same effects as score_windows(fit, cf_profile=profile) would recompute; reused, no extra forward
            raw_fit['CF_raw'] = cf_anomaly_score(eff_fit, profile)
        calibrator = fit_score_calibrator(raw_fit)
        for comp, ent in calibrator.items():
            if not (math.isfinite(ent['center']) and math.isfinite(ent['scale']) and ent['scale'] > 0):
                raise EvalError(f'calibrator entry {comp} not finite/positive: {ent}')
        clip_min = float(scoring.CALIB_CLIP_MIN)
        raw_test_c = {'P_raw': P, 'C_raw': C, 'G_raw': G}
        if 'CF_raw' in scores:
            raw_test_c['CF_raw'] = scores['CF_raw']
        cal_off = apply_score_calibrator(raw_test_c, calibrator, clip_min=clip_min, alpha=scoring.SCORE_ALPHA, beta=scoring.SCORE_BETA, gamma=0.0)
        scores.update({'Pn': cal_off['P'], 'Cn': cal_off['C'], 'Gn': cal_off['G'], 'A_off_cal': cal_off['A']})
        if 'CF_raw' in scores:
            cal_on = apply_score_calibrator(raw_test_c, calibrator, clip_min=clip_min, alpha=scoring.SCORE_ALPHA, beta=scoring.SCORE_BETA, gamma=gamma)
            if not (np.array_equal(cal_on['P'], cal_off['P']) and np.array_equal(cal_on['C'], cal_off['C'])):
                raise EvalError('calibrated base Pn/Cn differ between CF OFF and ON')
            scores.update({'CFn': cal_on['CF'], 'A_on_cal': cal_on['A']})
        calib_info.update({'order': 'restore -> cf_profile(fit) -> raw P/C/G/CF on fit with profile -> fit_score_calibrator(incl. CF_raw) -> apply on test',
                           'fit_windows': int(raw_fit['P_raw'].shape[0]), 'clip_min': clip_min,
                           'alpha': float(scoring.SCORE_ALPHA), 'beta': float(scoring.SCORE_BETA), 'gamma': gamma,
                           'entries': {k: {'center': float(v['center']), 'scale': float(v['scale'])} for k, v in calibrator.items()},
                           'has_CF_entry': 'CF_raw' in calibrator,
                           'native_final_eval_note': 'main._final_eval fits the calibrator without cf_profile (no CF_raw entry -> CFn=0); not reproduced here'})

    parity = None
    if verify_native_parity:
        # Independent native calls (extra forwards, recorded separately).
        with counter('parity_native_score_windows'):
            nat_off = score_windows(model, entity.test_z, dev, cfg.TEST.BATCH_SIZE, scoring, calibrator=None, cf_profile=None)
            parity = {'A_off_exact': bool(np.array_equal(nat_off['A'], A_off)),
                      'P_raw_exact': bool(np.array_equal(nat_off['P_raw'], P)), 'C_raw_exact': bool(np.array_equal(nat_off['C_raw'], C))}
            if 'A_on' in scores:
                nat_on = score_windows(model, entity.test_z, dev, cfg.TEST.BATCH_SIZE, scoring, calibrator=None, cf_profile=profile)
                parity.update({'A_on_exact': bool(np.array_equal(nat_on['A'], scores['A_on'])),
                               'CF_raw_exact': bool(np.array_equal(nat_on['CF_raw'], CF)),
                               'base_same_between_off_on': bool(np.array_equal(nat_on['P_raw'], nat_off['P_raw']) and np.array_equal(nat_on['C_raw'], nat_off['C_raw']))})
            if calibrator is not None:
                # native scorer given the *corrected* calibrator (includes CF_raw) and profile
                nat_c_off = score_windows(model, entity.test_z, dev, cfg.TEST.BATCH_SIZE, scoring, calibrator=calibrator, cf_profile=None)
                parity['A_off_cal_exact'] = bool(np.array_equal(nat_c_off['A'], scores['A_off_cal']))
                parity['Pn_exact'] = bool(np.array_equal(nat_c_off['P'], scores['Pn']))
                if 'A_on_cal' in scores:
                    nat_c_on = score_windows(model, entity.test_z, dev, cfg.TEST.BATCH_SIZE, scoring, calibrator=calibrator, cf_profile=profile)
                    parity['A_on_cal_exact'] = bool(np.array_equal(nat_c_on['A'], scores['A_on_cal']))
                    parity['CFn_exact'] = bool(np.array_equal(nat_c_on['CF'], scores['CFn']))
        if not all(parity.values()):
            raise EvalError(f'native parity failed: {parity}')
    counter.close()

    state_after = snapshot_state(model)
    changed = [k for k in state_before if state_before[k] != state_after[k]]
    if changed:
        raise EvalError(f'model parameters/buffers changed during evaluation: {changed[:10]}')

    # --- metrics ---
    Tt, start = entity.test_z.shape[0], cfg.PICAAD.L - 1
    variants = {'A_off': A_off}
    if 'A_on' in scores: variants['A_on'] = scores['A_on']
    diag = {'P_raw': P, 'C_raw': C, 'G_raw': G}
    if 'CF_raw' in scores: diag['CF_raw'] = scores['CF_raw']
    if do_calib:
        variants['A_off_cal'] = scores['A_off_cal']
        if 'A_on_cal' in scores: variants['A_on_cal'] = scores['A_on_cal']
        diag.update({'Pn': scores['Pn'], 'Cn': scores['Cn'], 'Gn': scores['Gn']})
        if 'CFn' in scores: diag['CFn'] = scores['CFn']
    if cf == 'on':
        variants.pop('A_off', None); variants.pop('A_off_cal', None)
    formulas = {'A_off': 'P_raw + C_raw', 'A_on': f'P_raw + C_raw + {gamma:g}*CF_raw',
                'A_off_cal': 'Pn + Cn', 'A_on_cal': f'Pn + Cn + {gamma:g}*CFn'}
    rows = []
    tl = score_components_to_timeline({**variants, **diag}, Tt=Tt, start=start)
    for name in list(variants) + list(diag):
        m = paper_eval_one(tl[name + '_t'], entity.y, start, cfg.EVAL)
        rows.append({'entity': entity.name, 'seed': ck.get('seed'), 'ckpt_format': ck['_format'], 'epoch': restore_info['restored_epoch'],
                     'variant': name, 'kind': 'fusion' if name in variants else 'diagnostic',
                     'scoring_mode': 'calibrated' if (name.endswith('_cal') or name in ('Pn', 'Cn', 'Gn', 'CFn')) else 'raw',
                     'formula': formulas.get(name, name),
                     **{k: float(m.get(k, float('nan'))) for k in METRIC_KEYS}})
    df = pd.DataFrame(rows)
    df.to_csv(out / 'metrics.csv', index=False)
    np.savez(out / 'scores.npz', y=entity.y, **scores)
    (out / 'config_resolved.yaml').write_text(cfg.dump())

    sliding_window = get_median_anomaly_length(entity.y[start:]) if cfg.EVAL.USE_MEDIAN_VUS_WINDOW else int(cfg.EVAL.SLIDING_WINDOW)
    prov = {
        'tool': 'scripts/eval_ckpt.py', 'phase': '2-B (raw + corrected calibrated path)', 'finished_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'elapsed_s': round(time.time() - t0, 2), 'device': str(dev), 'torch_version': torch.__version__,
        'checkpoint': {'path': os.path.abspath(ck_path), 'sha256': _sha256_file(ck_path), 'format': ck['_format'],
                       'protocol': ck.get('protocol'), 'payload_epoch': ck.get('epoch'), 'payload_current_epoch': ck.get('current_epoch'),
                       'seed': ck.get('seed'), 'entity': ck['entity'], 'val_mae': ck.get('val_mae'),
                       'split_info': ck.get('split_info'), 'prior_cache_key': ck.get('prior_cache_key'),
                       'data_fingerprint_in_ckpt': ck.get('data_fingerprint'), 'code_fingerprint_in_ckpt': ck.get('code_fingerprint'),
                       'native_test_metrics_in_payload': ck.get('metrics')},
        'restore': restore_info | {'set_te_prior_called_after_load': False, 'strict_load': True},
        'data': data_info,
        'scoring': {'calibrate': do_calib, 'A_off': 'P_raw + C_raw', 'A_on': 'A_off + gamma*CF_raw',
                    'A_off_cal': 'Pn + Cn' if do_calib else None, 'A_on_cal': 'Pn + Cn + gamma*CFn' if do_calib else None, 'gamma': gamma,
                    'P_AGG': scoring.P_AGG, 'C_AGG': scoring.C_AGG, 'CAUSAL_LAG_AGG': scoring.CAUSAL_LAG_AGG, 'GRAPH_LAG_AGG': scoring.GRAPH_LAG_AGG},
        'cf': cf_info,
        'calibration': calib_info,
        'evaluator': {'USE_MEDIAN_VUS_WINDOW': bool(cfg.EVAL.USE_MEDIAN_VUS_WINDOW), 'sliding_window_used': int(sliding_window),
                      'VUS_VERSION': cfg.EVAL.VUS_VERSION, 'VUS_THRE': int(cfg.EVAL.VUS_THRE), 'start_idx': int(start),
                      'note': 'threshold-based F1 metrics use the evaluator\'s label-based search; report as diagnostics'},
        'forward_passes': counter.counts, 'native_parity': parity, 'state_unchanged': True,
        'state_hash_before_after': hashlib.sha256(''.join(state_before[k] for k in sorted(state_before)).encode()).hexdigest(),
        'code_fingerprint': _git_fingerprint(),
    }
    (out / 'provenance.json').write_text(json.dumps(prov, indent=1, default=str))
    return df, prov


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ckpt', help='explicit checkpoint file')
    ap.add_argument('--ckpt_dir'); ap.add_argument('--entity'); ap.add_argument('--seed', type=int)
    ap.add_argument('--ckpt_tag', help='last | best_val | epNN')
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--data_input_dir', default=None, help='override cfg.DATA.INPUT_DIR (e.g. data_npz/PSM for a colleague ckpt)')
    ap.add_argument('--cf', choices=['off', 'on', 'both'], default='both')
    ap.add_argument('--device', default=None)
    ap.add_argument('--verify_native_parity', action='store_true', help='also run native score_windows and assert exact equality (extra forwards)')
    ap.add_argument('--no_save_effects', action='store_true')
    ap.add_argument('--calibrate', choices=['cfg', 'off', 'on'], default='cfg',
                    help="cfg: follow checkpoint config (default; colleague configs are CALIBRATE=False); on: corrected calibrated path (calibrator fit with CF)")
    a = ap.parse_args()
    if a.ckpt:
        ck_path = a.ckpt
    elif a.ckpt_dir and a.entity and a.seed is not None and a.ckpt_tag:
        ck_path = resolve_ckpt_path(a.ckpt_dir, a.entity, a.seed, a.ckpt_tag)
    else:
        ap.error('give --ckpt, or --ckpt_dir + --entity + --seed + --ckpt_tag')
    df, prov = evaluate(ck_path, a.out_dir, a.data_input_dir, a.cf, a.device, a.verify_native_parity, not a.no_save_effects,
                        calibrate=a.calibrate)
    print(f"ckpt={prov['checkpoint']['path']} format={prov['checkpoint']['format']} epoch={prov['restore']['restored_epoch']} "
          f"fit={prov['data']['fit_protocol']} gamma={prov['scoring']['gamma']} calibrate={prov['calibration']['enabled']} forwards={prov['forward_passes']}")
    print(df[['variant', 'kind', 'scoring_mode', 'AUC-PR', 'AUC-ROC', 'VUS-PR', 'VUS-ROC', 'Standard-F1', 'Affiliation-F']].to_string(index=False, float_format='%.4f'))
    print(f'wrote: {a.out_dir}/metrics.csv, scores.npz, provenance.json, config_resolved.yaml')


if __name__ == '__main__':
    main()
