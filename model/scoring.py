import numpy as np
import torch
from torch.utils.data import DataLoader

from datasets.sliding_window import SlidingWindowDataset
from layers.ops import normalize_causal_tensor_torch
from utils.misc import robust_loc_scale, robust_zscore


def fit_score_calibrator(train_scores: dict):
    out = {}
    for key in ["P_raw", "C_raw", "G_raw"]:
        center, scale = robust_loc_scale(train_scores[key])
        out[key] = {"center": center, "scale": scale}
    if "CF_raw" in train_scores:
        center, scale = robust_loc_scale(train_scores["CF_raw"])
        out["CF_raw"] = {"center": center, "scale": scale}
    return out


# --- original apply_score_calibrator (without CF) ---
# def apply_score_calibrator(raw_scores, calibrator, clip_min=0.0, alpha=1.0, beta=1.0):
#     Pn = robust_zscore(raw_scores["P_raw"], calibrator["P_raw"]["center"], calibrator["P_raw"]["scale"], clip_min)
#     Cn = robust_zscore(raw_scores["C_raw"], calibrator["C_raw"]["center"], calibrator["C_raw"]["scale"], clip_min)
#     Gn = robust_zscore(raw_scores["G_raw"], calibrator["G_raw"]["center"], calibrator["G_raw"]["scale"], clip_min)
#     S = (float(alpha) * Cn + float(beta) * Gn).astype(np.float32)
#     A = (Pn * S).astype(np.float32)
#     return {"P": Pn, "C": Cn, "G": Gn, "S": S, "A": A}


def apply_score_calibrator(raw_scores: dict, calibrator: dict, clip_min: float = 0.0,
                           alpha: float = 1.0, beta: float = 1.0, gamma: float = 0.0):
    Pn = robust_zscore(raw_scores["P_raw"], calibrator["P_raw"]["center"], calibrator["P_raw"]["scale"], clip_min)
    Cn = robust_zscore(raw_scores["C_raw"], calibrator["C_raw"]["center"], calibrator["C_raw"]["scale"], clip_min)
    Gn = robust_zscore(raw_scores["G_raw"], calibrator["G_raw"]["center"], calibrator["G_raw"]["scale"], clip_min)

    if "CF_raw" in raw_scores and "CF_raw" in calibrator and float(gamma) > 0:
        CFn = robust_zscore(raw_scores["CF_raw"], calibrator["CF_raw"]["center"], calibrator["CF_raw"]["scale"], clip_min)
    else:
        CFn = np.zeros_like(Pn)

    S = Cn.copy()
    A = (Pn + Cn).astype(np.float32)
    return {"P": Pn, "C": Cn, "G": Gn, "CF": CFn, "S": S, "A": A}


def score_components_to_timeline(comp_dict, Tt, start):
    out = {}
    for k, v in comp_dict.items():
        arr = np.full((Tt,), np.nan, dtype=np.float32)
        arr[start:] = np.asarray(v, dtype=np.float32)
        out[k + "_t"] = arr
    return out


def prediction_score(err: torch.Tensor, agg: str = "mean", topk: int = 3):
    if agg == "mean":
        return err.mean(dim=1)
    if agg == "max":
        return err.max(dim=1).values
    k = min(int(topk), err.shape[1])
    return err.topk(k, dim=1).values.mean(dim=1)


def matrix_deviation_per_tau(diff: torch.Tensor, agg: str = "fro", topk: int = 3):
    if agg == "fro":
        return torch.sqrt(diff.pow(2).mean(dim=(2, 3)) + 1e-12)
    row_dev = diff.abs().mean(dim=3)
    if agg == "maxrow":
        return row_dev.max(dim=2).values
    k = min(int(topk), row_dev.shape[2])
    return row_dev.topk(k, dim=2).values.mean(dim=2)


def lag_aggregate(per_tau: torch.Tensor, mode: str = "rms"):
    if mode == "max":
        return per_tau.max(dim=1).values
    if mode == "mean":
        return per_tau.mean(dim=1)
    return torch.sqrt(per_tau.pow(2).mean(dim=1) + 1e-12)


def _select_cf_sources(model, top_k):
    """Select source variables to intervene on, ranked by gate importance."""
    gate = model.edge_gate().detach()   # [tau_max, N, N]
    src_importance = gate.sum(dim=(0, 2))  # [N]
    if top_k > 0 and top_k < model.N:
        return src_importance.topk(top_k).indices.tolist()
    return list(range(model.N))


# --- original counterfactual_score_windows (input ablation) ---
# @torch.no_grad()
# def counterfactual_score_windows(model, series_TN, device, batch,
#                                   top_k=15, fill_value=0.0):
#     """Input-ablation version: zeros out src in X."""
#     model.eval()
#     ds = SlidingWindowDataset(series_TN, model.L)
#     loader = DataLoader(ds, batch_size=batch, shuffle=False, drop_last=False, num_workers=0)
#     src_indices = _select_cf_sources(model, top_k)
#     k = len(src_indices)
#     W = len(ds)
#     effects = np.zeros((W, k), dtype=np.float32)
#     offset = 0
#     for X in loader:
#         X = X.to(device)
#         _, pred, *_ = model(X)
#         x_true = X[:, -1, :]
#         base_err = (x_true - pred).abs()
#         bsz = X.shape[0]
#         for j, src in enumerate(src_indices):
#             X_cf = X.clone()
#             X_cf[:, :, src] = fill_value
#             _, cf_pred, *_ = model(X_cf)
#             cf_err = (x_true - cf_pred).abs()
#             delta = (cf_err - base_err).mean(dim=1)
#             effects[offset:offset + bsz, j] = delta.cpu().numpy()
#         offset += bsz
#     return effects, src_indices


@torch.no_grad()
def counterfactual_score_windows(model, series_TN, device, batch,
                                  top_k=15, fill_value=0.0):
    """Graph-intervention version: cuts outgoing edges of src in the
    learned causal graph (gate_override) instead of modifying input X.

    For each window:
      base_err = |x_true - pred(X)|
      For each source src:
        gate_cf = gate with gate_cf[:, src, :] = 0  (structural intervention)
        cf_err = |x_true - pred(X, gate_override=gate_cf)|
        causal_effect[src] = mean(cf_err - base_err)

    Returns (effects, src_indices):
      effects: [W, k] — causal effect per window per source
      src_indices: list of k source variable indices
    """
    model.eval()
    ds = SlidingWindowDataset(series_TN, model.L)
    loader = DataLoader(ds, batch_size=batch, shuffle=False, drop_last=False, num_workers=0)

    src_indices = _select_cf_sources(model, top_k)
    k = len(src_indices)
    W = len(ds)
    effects = np.zeros((W, k), dtype=np.float32)
    offset = 0

    base_gate = model._effective_gate()  # [tau_max, N, N]

    for X in loader:
        X = X.to(device)
        _, pred, *_ = model(X)
        x_true = X[:, -1, :]
        base_err = (x_true - pred).abs()   # [B, N]

        bsz = X.shape[0]
        for j, src in enumerate(src_indices):
            gate_cf = base_gate.clone()
            gate_cf[:, src, :] = 0.0       # cut all outgoing edges from src
            _, cf_pred, *_ = model(X, gate_override=gate_cf)
            cf_err = (x_true - cf_pred).abs()
            delta = (cf_err - base_err).mean(dim=1)   # [B]
            effects[offset:offset + bsz, j] = delta.cpu().numpy()

        offset += bsz

    return effects, src_indices


def fit_cf_profile(effects):
    """Compute normal profile (mean, std) from training-set effects."""
    return {
        "mean": effects.mean(axis=0),        # [k]
        "std": effects.std(axis=0) + 1e-8,   # [k]
    }


def cf_anomaly_score(effects, profile):
    """Z-score of current effects vs normal profile, aggregated per window."""
    z = (effects - profile["mean"]) / profile["std"]   # [W, k]
    return np.abs(z).mean(axis=1).astype(np.float32)   # [W]


# --- original score_windows_raw (without CF) ---
# @torch.no_grad()
# def score_windows_raw(model, series_TN, device, batch, scoring_cfg):
#     ... (identical to current but without CF_raw) ...

@torch.no_grad()
def score_windows_raw(model, series_TN, device, batch, scoring_cfg):
    """scoring_cfg: cfg.PICAAD.SCORING subtree with attributes
        P_AGG, P_TOPK, C_AGG, C_TOPK, G_AGG, G_TOPK,
        CAUSAL_LAG_AGG, GRAPH_LAG_AGG.
    """
    model.eval()
    ds = SlidingWindowDataset(series_TN, model.L)
    loader = DataLoader(ds, batch_size=batch, shuffle=False, drop_last=False, num_workers=0)

    W = len(ds)
    P_w = np.zeros((W,), dtype=np.float32)
    C_w = np.zeros((W,), dtype=np.float32)
    G_w = np.zeros((W,), dtype=np.float32)

    cls_ref = model.cls_ref.detach()
    w_ref = model.w_ref.detach()
    offset = 0

    for X in loader:
        X = X.to(device)
        recon, pred, C_all, pred_weights, edge_value, edge_effect, edge_strength, gate, local_delta = model(X)

        x_true_next = X[:, -1, :]
        err = (x_true_next - pred).abs()
        P = prediction_score(err, agg=scoring_cfg.P_AGG, topk=scoring_cfg.P_TOPK)

        if model.has_cls_ref:
            cls_cur = normalize_causal_tensor_torch(edge_strength)
            cdiff = cls_cur - cls_ref.unsqueeze(0)
            C_per_tau = matrix_deviation_per_tau(cdiff, agg=scoring_cfg.C_AGG, topk=scoring_cfg.C_TOPK)
            Cscore = lag_aggregate(C_per_tau, mode=scoring_cfg.CAUSAL_LAG_AGG)
        else:
            Cscore = torch.zeros_like(P)

        if pred_weights.dim() == 3:
            pred_weights_b = pred_weights.unsqueeze(0).expand(X.shape[0], -1, -1, -1)
        else:
            pred_weights_b = pred_weights

        if model.has_w_ref:
            gdiff = pred_weights_b - w_ref.unsqueeze(0)
            G_per_tau = matrix_deviation_per_tau(gdiff, agg=scoring_cfg.G_AGG, topk=scoring_cfg.G_TOPK)
            Gscore = lag_aggregate(G_per_tau, mode=scoring_cfg.GRAPH_LAG_AGG)
        else:
            Gscore = torch.zeros_like(P)

        bsz = X.shape[0]
        P_w[offset:offset + bsz] = P.detach().cpu().numpy().astype(np.float32)
        C_w[offset:offset + bsz] = Cscore.detach().cpu().numpy().astype(np.float32)
        G_w[offset:offset + bsz] = Gscore.detach().cpu().numpy().astype(np.float32)
        offset += bsz

    return {"P_raw": P_w, "C_raw": C_w, "G_raw": G_w}


# --- original score_windows (without CF) ---
# def score_windows(model, series_TN, device, batch, scoring_cfg, calibrator=None):
#     raw = score_windows_raw(model, series_TN, device, batch, scoring_cfg)
#     if calibrator is not None:
#         cal = apply_score_calibrator(raw, calibrator,
#                                      clip_min=scoring_cfg.CALIB_CLIP_MIN,
#                                      alpha=scoring_cfg.SCORE_ALPHA,
#                                      beta=scoring_cfg.SCORE_BETA)
#     else:
#         cal = {"P": raw["P_raw"], "C": raw["C_raw"], "G": raw["G_raw"]}
#         cal["S"] = (scoring_cfg.SCORE_ALPHA * cal["C"] + scoring_cfg.SCORE_BETA * cal["G"])
#         cal["A"] = (cal["P"] * cal["S"])
#     out = {}; out.update(raw); out.update(cal)
#     return out


def score_windows(model, series_TN, device, batch, scoring_cfg,
                  calibrator=None, cf_profile=None):
    raw = score_windows_raw(model, series_TN, device, batch, scoring_cfg)

    use_cf = getattr(scoring_cfg, 'USE_COUNTERFACTUAL', False) and cf_profile is not None
    if use_cf:
        cf_effects, _ = counterfactual_score_windows(
            model, series_TN, device, batch,
            top_k=getattr(scoring_cfg, 'CF_TOP_K', 15),
            fill_value=getattr(scoring_cfg, 'CF_FILL_VALUE', 0.0),
        )
        raw["CF_raw"] = cf_anomaly_score(cf_effects, cf_profile)

    gamma = getattr(scoring_cfg, 'SCORE_GAMMA', 0.0) if use_cf else 0.0

    if calibrator is not None:
        cal = apply_score_calibrator(
            raw, calibrator,
            clip_min=scoring_cfg.CALIB_CLIP_MIN,
            alpha=scoring_cfg.SCORE_ALPHA,
            beta=scoring_cfg.SCORE_BETA,
            gamma=gamma,
        )
    else:
        cal = {
            "P": raw["P_raw"].astype(np.float32),
            "C": raw["C_raw"].astype(np.float32),
            "G": raw["G_raw"].astype(np.float32),
        }
        if use_cf:
            cal["CF"] = raw["CF_raw"].astype(np.float32)
        else:
            cal["CF"] = np.zeros_like(cal["P"])
        cal["S"] = cal["C"].copy()
        cal["A"] = (cal["P"] + cal["C"]).astype(np.float32)

    out = {}
    out.update(raw)
    out.update(cal)
    return out
