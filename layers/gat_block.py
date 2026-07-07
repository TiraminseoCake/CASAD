"""Cross-lag GAT block for PICAAD (Option C).

Replaces the per-lag MHSA over N variable nodes with a single GAT over
`tau_max * N` (lag * variable) nodes. Preserves the per-lag encoder pipeline
(LSTM + TemporalAttnPool → C_tau) so the `lag_win` local-window compression
that the original PICAAD relies on stays intact.

Key differences from the earlier CTSAD+PICAAD combined model:
    - Nodes are (lag, variable), NOT (time, variable). Half the nodes for the
      same tau_max/N, and PCMCI+ prior `[tau_max, N, N]` maps naturally via
      the lag_gap = τ_src - τ_tgt index.
    - `causal_mask_logits` is only detached inside intervention forward passes
      (where model() is called repeatedly for permutation alignment). Regular
      training forward keeps the gradient so the learnable mask actually
      updates -- fixing the "half-learnable" issue in the combined model.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


def build_cross_lag_causal_mask(N: int, tau_max: int, device=None) -> torch.Tensor:
    """Boolean edge mask [tau_max*N, tau_max*N].

    Node (τ, i) is flat-indexed as τ * N + i.
    Edge (τ_src, i) → (τ_tgt, j) is allowed iff τ_src >= τ_tgt (past→present,
    including same-lag cross-variable messages).
    """
    NT = tau_max * N
    tau_idx = torch.arange(NT, device=device) // N     # [NT], each node's τ
    tau_src = tau_idx.unsqueeze(1)                     # [NT, 1]
    tau_tgt = tau_idx.unsqueeze(0)                     # [1, NT]
    return tau_src >= tau_tgt                          # [NT, NT] bool


def build_cross_lag_prior_bias(
    te_prior_gate: torch.Tensor,
    causal_mask_logits: torch.Tensor,
    N: int,
    tau_max: int,
    scale: float,
    ramp: float,
    detach_for_intervention: bool = False,
    include_same_lag: bool = False,
) -> torch.Tensor:
    """Log-domain attention bias [tau_max*N, tau_max*N] from PCMCI+ prior gate.

    Cross-lag edges (τ_src > τ_tgt) with lag_gap = τ_src - τ_tgt use PCMCI+
    index `lag_gap - 1` on `causal_mask_logits` (index k = lag k+1).

    Same-lag edges (lag_gap == 0):
      - include_same_lag=False (default, matches original Option C):
          bias = 0, attention unconstrained apart from the causal mask.
      - include_same_lag=True (Option B / SLP variant):
          for each τ, the diagonal block (τ, τ) gets
          `scale * ramp * log(sigmoid(causal_mask_logits[τ]))`. This
          restores the per-τ within-lag prior that the original PICAAD
          per-lag MHSA applied via `causal_mask_logits[τ-1]`.

    Args:
        te_prior_gate:       [tau_max, N, N] (kept for API symmetry)
        causal_mask_logits:  [tau_max, N, N] learnable nn.Parameter
        scale:               PICAAD.CAUSAL_ATTN_MASK_SCALE
        ramp:                warmup ramp in [0, 1]
        detach_for_intervention: True inside intervention forward passes to
                                 avoid double-backward on the same graph.
        include_same_lag:    fill diagonal (τ, τ) blocks with
                             causal_mask_logits[τ]. See docstring above.

    Returns:
        bias:                [tau_max*N, tau_max*N] float
    """
    NT = tau_max * N
    device = causal_mask_logits.device
    dtype = causal_mask_logits.dtype

    logits = causal_mask_logits.detach() if detach_for_intervention else causal_mask_logits
    soft_gate = torch.sigmoid(logits)                   # [tau_max, N, N]
    log_gate = torch.log(soft_gate.clamp_min(1e-6))     # [tau_max, N, N]

    bias = torch.zeros(NT, NT, device=device, dtype=dtype)

    # Cross-lag: for lag_gap = τ_src - τ_tgt in [1, tau_max], fill tiles
    # where tau_src = tau_tgt + gap.
    for gap in range(1, tau_max + 1):
        block = scale * ramp * log_gate[gap - 1]        # [N, N]
        for tau_tgt in range(tau_max - gap):
            tau_src = tau_tgt + gap
            r_start = tau_src * N
            c_start = tau_tgt * N
            bias[r_start:r_start + N, c_start:c_start + N] = block

    # Same-lag (Option B / SLP): diagonal block (τ, τ) gets its own prior.
    if include_same_lag:
        for tau_diag in range(tau_max):
            block = scale * ramp * log_gate[tau_diag]   # [N, N]
            r_start = tau_diag * N
            c_start = tau_diag * N
            bias[r_start:r_start + N, c_start:c_start + N] = block

    return bias


class CrossLagGATLayer(nn.Module):
    """Single dense-masked multi-head attention layer over [B, NT, D] nodes."""

    def __init__(self, in_dim: int, out_dim: int, num_heads: int,
                 dropout: float = 0.1, residual: bool = True):
        super().__init__()
        assert out_dim % num_heads == 0
        self.num_heads = num_heads
        self.d_head = out_dim // num_heads
        self.W_q = nn.Linear(in_dim, out_dim)
        self.W_k = nn.Linear(in_dim, out_dim)
        self.W_v = nn.Linear(in_dim, out_dim)
        self.W_o = nn.Linear(out_dim, out_dim)
        self.attn_drop = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(out_dim)
        self.residual = residual
        if residual and in_dim != out_dim:
            self.res_proj = nn.Linear(in_dim, out_dim)
        else:
            self.res_proj = None

    def forward(self, x: torch.Tensor,
                causal_mask: torch.Tensor,
                prior_bias: torch.Tensor = None):
        """
        x:           [B, NT, D_in]
        causal_mask: [NT, NT] bool (True = allowed)
        prior_bias:  [NT, NT] float or None
        """
        B, NT, _ = x.shape
        H = self.num_heads
        dh = self.d_head

        Q = self.W_q(x).view(B, NT, H, dh).transpose(1, 2)   # [B, H, NT, dh]
        K = self.W_k(x).view(B, NT, H, dh).transpose(1, 2)
        V = self.W_v(x).view(B, NT, H, dh).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-1, -2)) / (dh ** 0.5)  # [B, H, NT, NT]

        neg_inf = torch.finfo(scores.dtype).min
        scores = scores.masked_fill(~causal_mask.unsqueeze(0).unsqueeze(0), neg_inf)

        if prior_bias is not None:
            scores = scores + prior_bias.unsqueeze(0).unsqueeze(0)

        attn = self.attn_drop(torch.softmax(scores, dim=-1))
        out = torch.matmul(attn, V)                          # [B, H, NT, dh]
        out = out.transpose(1, 2).reshape(B, NT, H * dh)     # [B, NT, D_out]
        out = self.W_o(out)

        if self.residual:
            res = self.res_proj(x) if self.res_proj is not None else x
            out = out + res
        return self.norm(out), attn


class CrossLagGATBlock(nn.Module):
    """Stack of CrossLagGATLayer with input/output projection to encoder dim."""

    def __init__(self, d: int, gat_dim: int, num_layers: int,
                 num_heads: int, dropout: float):
        super().__init__()
        self.in_proj = nn.Linear(d, gat_dim) if gat_dim != d else nn.Identity()
        self.layers = nn.ModuleList([
            CrossLagGATLayer(gat_dim, gat_dim, num_heads, dropout)
            for _ in range(num_layers)
        ])
        self.out_proj = nn.Linear(gat_dim, d) if gat_dim != d else nn.Identity()

    def forward(self, x: torch.Tensor,
                causal_mask: torch.Tensor,
                prior_bias: torch.Tensor = None):
        """x: [B, NT, d]  -> [B, NT, d]."""
        x = self.in_proj(x)
        for layer in self.layers:
            x, _ = layer(x, causal_mask, prior_bias)
        return self.out_proj(x)
