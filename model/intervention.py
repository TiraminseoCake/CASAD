import numpy as np
import torch
import torch.nn.functional as F

from layers.ops import normalize_vector_torch


def intervene_local_window(X: torch.Tensor, tau: int, src: int, lag_win: int,
                           mode: str = "permute", fill_value: float = 0.0):
    B, L, _ = X.shape
    tau = int(tau)
    src = int(src)
    end = L - tau
    start = max(0, end - int(lag_win))
    if start >= end:
        return X.clone()

    Xp = X.clone()
    if mode == "permute":
        if B <= 1:
            return Xp
        rng_idx = torch.randperm(B, device=X.device)
        Xp[:, start:end, src] = X[rng_idx, start:end, src]
    elif mode == "fill":
        Xp[:, start:end, src] = float(fill_value)
    else:
        raise ValueError(f"Unknown intervention mode: {mode}")
    return Xp


def sample_intervention_pairs(tau_max: int, N: int, num_pairs: int, rng: np.random.Generator,
                               te_prior_gate=None):
    """Sample (tau, src) pairs for intervention.

    If te_prior_gate is provided (PCMCI+ guided), sample edges proportional
    to their gate strength. Otherwise falls back to uniform random sampling.
    """
    pairs = []

    if te_prior_gate is not None:
        gate_np = te_prior_gate.detach().cpu().numpy() if hasattr(te_prior_gate, 'detach') else te_prior_gate
        source_importance = gate_np.sum(axis=2)  # [tau_max, N]
        flat = source_importance.ravel()
        flat_sum = flat.sum()

        if flat_sum > 1e-8:
            probs = flat / flat_sum
            indices = rng.choice(len(probs), size=max(int(num_pairs), 0), p=probs, replace=True)
            for idx in indices:
                tau = int(idx // N) + 1  # 1-indexed
                src = int(idx % N)
                pairs.append((tau, src))
            return pairs

    for _ in range(max(int(num_pairs), 0)):
        tau = int(rng.integers(1, tau_max + 1))
        src = int(rng.integers(0, N))
        pairs.append((tau, src))
    return pairs


def _intervention_loss_mse(cur, delta_pos):
    return F.mse_loss(normalize_vector_torch(cur), normalize_vector_torch(delta_pos))


def _intervention_loss_margin(cur, delta_pos, gate_row, margin_high=0.3, margin_low=0.1):
    delta_max = delta_pos.max().clamp(min=1e-8)
    delta_rel = delta_pos / delta_max
    loss_causal = gate_row * F.relu(margin_high - delta_rel)
    loss_spurious = (1.0 - gate_row) * F.relu(delta_rel - margin_low)
    return (loss_causal + loss_spurious).mean()


def _intervention_loss_contrastive(cur, delta_pos, gate_row, margin=0.1):
    gate_high = (gate_row > 0.5)
    gate_low = (gate_row <= 0.5)
    if gate_high.sum() == 0 or gate_low.sum() == 0:
        return F.mse_loss(normalize_vector_torch(cur), normalize_vector_torch(delta_pos))
    delta_high_mean = delta_pos[gate_high].mean()
    delta_low_mean = delta_pos[gate_low].mean()
    return F.relu(delta_low_mean - delta_high_mean + margin)


def gradient_sensitivity_and_epoch_cls(model, X, pred, x_true_next, edge_strength,
                                       loss_type='gradient', margin=0.1):
    """Gradient-based intervention: compute input sensitivity for all (τ, src)
    in a single backward pass — no extra forward passes needed.

    Returns (loss_perm, cls_sum, cls_cnt) with same interface as permutation variant.
    """
    _, L, N = X.shape
    tau_max = model.tau_max
    lag_win = model.lag_win
    device = X.device

    total_err = (x_true_next - pred).abs().sum()
    grad_X = torch.autograd.grad(total_err, X, retain_graph=True)[0]  # [B, L, N]

    sensitivity = torch.zeros(tau_max, N, device=device)
    for tau in range(1, tau_max + 1):
        end = L - tau
        start = max(0, end - lag_win)
        if start >= end:
            continue
        sensitivity[tau - 1, :] = grad_X[:, start:end, :].abs().mean(dim=(0, 1))

    sens_3d = sensitivity.unsqueeze(2).expand(tau_max, N, N)

    cls_sum = sens_3d.detach().clone()
    cls_cnt = torch.ones(tau_max, N, 1, device=device)

    sens_max = sensitivity.max().clamp(min=1e-8)
    sens_norm = sensitivity / sens_max  # [tau_max, N]

    gate = model.edge_gate().detach()  # [tau_max, N, N]
    gate_src = gate.mean(dim=2)  # [tau_max, N] — per-source average

    causal_mask = (gate_src > 0.5)
    spurious_mask = ~causal_mask
    if causal_mask.sum() > 0 and spurious_mask.sum() > 0:
        sens_causal = sens_norm[causal_mask].mean()
        sens_spurious = sens_norm[spurious_mask].mean()
        loss = F.relu(sens_spurious - sens_causal + margin)
    else:
        loss = F.mse_loss(gate_src, sens_norm)

    return loss, cls_sum, cls_cnt


def permutation_alignment_and_epoch_cls(model, X, x_true_next, base_abs_err_ref, edge_strength, rng,
                                         perm_pairs: int = 2, perm_mode: str = "permute",
                                         fill_value: float = 0.0, loss_type: str = "mse",
                                         margin_high: float = 0.3, margin_low: float = 0.1):
    zero = torch.tensor(0.0, device=X.device)
    cls_sum = torch.zeros(model.tau_max, model.N, model.N, device=X.device)
    cls_cnt = torch.zeros(model.tau_max, model.N, 1, device=X.device)

    if perm_pairs <= 0 or X.shape[0] <= 1:
        return zero, cls_sum, cls_cnt

    te_gate = model.te_prior_gate if model.has_te_prior else None
    pairs = sample_intervention_pairs(model.tau_max, model.N, perm_pairs, rng,
                                       te_prior_gate=te_gate)
    losses = []

    edge_strength_mean = edge_strength.mean(dim=0)
    gate_vals = model.edge_gate().detach() if loss_type in ('margin', 'contrastive') else None

    for tau, src in pairs:
        if perm_mode == "fill":
            _, pred_perm, _, _, _, _, _, _, _ = model(
                X, mask_tau=tau, mask_var=src, mask_fill_value=fill_value,
            )
        else:
            Xp = intervene_local_window(
                X, tau=tau, src=src, lag_win=model.lag_win,
                mode=perm_mode, fill_value=fill_value,
            )
            _, pred_perm, _, _, _, _, _, _, _ = model(Xp)

        delta_pos = torch.clamp((x_true_next - pred_perm).abs() - base_abs_err_ref, min=0.0).mean(dim=0)

        cls_sum[tau - 1, src, :] += delta_pos.detach()
        cls_cnt[tau - 1, src, 0] += 1.0

        delta_sum = float(delta_pos.sum().detach().cpu())
        if not np.isfinite(delta_sum) or delta_sum <= 1e-12:
            continue

        cur = edge_strength_mean[tau - 1, src, :]

        if loss_type == 'margin':
            gate_row = gate_vals[tau - 1, src, :]
            losses.append(_intervention_loss_margin(cur, delta_pos, gate_row, margin_high, margin_low))
        elif loss_type == 'contrastive':
            gate_row = gate_vals[tau - 1, src, :]
            losses.append(_intervention_loss_contrastive(cur, delta_pos, gate_row, margin_high))
        else:
            losses.append(_intervention_loss_mse(cur, delta_pos))

    if len(losses) == 0:
        return zero, cls_sum, cls_cnt
    return torch.stack(losses).mean(), cls_sum, cls_cnt
