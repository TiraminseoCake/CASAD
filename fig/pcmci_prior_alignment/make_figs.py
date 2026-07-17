"""
Visualization of PCMCI+ prior alignment analysis.

For each dataset (PSM, SMD, SWaT), we compare:
  - Φ_init  : causal attention bias initialized from PCMCI+ gate M
  - Φ_final : learned Φ after full training (ep80)

Figures saved to /home/sgshin/workspace/PICAAD/fig/pcmci_prior_alignment/
"""
import glob
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

EPS = 1e-4
BASE = Path("/home/sgshin/workspace/PICAAD/results/parallel")
OUT  = Path("/home/sgshin/workspace/PICAAD/fig/pcmci_prior_alignment")

DATASETS = {
    "PSM":  sorted(glob.glob(f"{BASE}/psm_20260701-221416/PSM/seed*/ckpt/*_ep80.pt")),
    "SMD":  sorted(glob.glob(f"{BASE}/smd_20260702-163856/machine-*/seed*/ckpt/*_ep80.pt")),
    "SWaT": sorted(glob.glob(f"{BASE}/swat_20260702-163856/swat/seed*/ckpt/*_ep80.pt")),
}
COLORS = {"M=0": "#4C72B0", "M=1": "#C44E52"}          # blue / red
DATASET_COLORS = {"PSM": "#4C72B0", "SMD": "#55A868", "SWaT": "#C44E52"}


def init_phi_from_M(M):
    Mc = M.clamp(EPS, 1 - EPS)
    return 0.5 * torch.log(Mc / (1 - Mc))


def load_pairs(ckpt_paths):
    """Return concatenated (phi_init, phi_final, M) across seeds/entities, excluding self-loops."""
    pi_list, pf_list, m_list = [], [], []
    for p in ckpt_paths:
        ck = torch.load(p, map_location="cpu", weights_only=False)
        sd = ck["state_dict"]
        M  = sd["te_prior_gate"]
        pf = sd["causal_mask_logits"]
        pi = init_phi_from_M(M)
        T, N, _ = M.shape
        nonself = torch.ones(T, N, N, dtype=torch.bool)
        for i in range(N):
            nonself[:, i, i] = False
        pi_list.append(pi[nonself])
        pf_list.append(pf[nonself])
        m_list.append(M[nonself])
    return (torch.cat(pi_list).numpy(),
            torch.cat(pf_list).numpy(),
            torch.cat(m_list).numpy())


plt.rcParams.update({
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "figure.dpi": 120,
})


data = {ds: load_pairs(paths) for ds, paths in DATASETS.items()}


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 — PCMCI+ prior sparsity across datasets
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 3.5))
datasets = list(data.keys())
m0_pct = [100 * (data[ds][2] == 0).mean() for ds in datasets]
m05_pct = [100 * ((data[ds][2] > 0.4) & (data[ds][2] < 0.6)).mean() for ds in datasets]
m1_pct = [100 * (data[ds][2] == 1.0).mean() for ds in datasets]
x = np.arange(len(datasets))
w = 0.25
ax.bar(x - w, m0_pct, w, label="M=0 (no causal)", color="#B0B0B0")
ax.bar(x,     m05_pct, w, label="M=0.5 (undetermined)", color="#F0AD4E")
ax.bar(x + w, m1_pct, w, label="M=1 (definitive)", color="#5CB85C")
for i, v in enumerate(m0_pct):
    ax.text(i - w, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
for i, v in enumerate(m1_pct):
    ax.text(i + w, v + 1, f"{v:.2f}%", ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(datasets)
ax.set_ylabel("Edge fraction (%)")
ax.set_title("PCMCI+ prior edge distribution per dataset\n(non-self edges only)")
ax.set_ylim(0, 105)
ax.legend(loc="center right", frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig(OUT / "fig1_pcmci_sparsity.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"saved: {OUT}/fig1_pcmci_sparsity.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 — Φ init→final scatter, one panel per dataset
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharex=True, sharey=True)
for ax, ds in zip(axes, datasets):
    pi, pf, M = data[ds]
    # Subsample for readability (M=0 dominates)
    idx0 = np.where(M == 0)[0]
    idx1 = np.where(M == 1.0)[0]
    if len(idx0) > 3000:
        idx0 = np.random.default_rng(0).choice(idx0, 3000, replace=False)
    ax.scatter(pi[idx0], pf[idx0], s=6, alpha=0.35, color=COLORS["M=0"],
               label=f"M=0 (n={len(np.where(M==0)[0])})", edgecolors="none")
    ax.scatter(pi[idx1], pf[idx1], s=16, alpha=0.9, color=COLORS["M=1"],
               label=f"M=1 (n={len(idx1)})", edgecolors="white", linewidths=0.4)
    lim = [-6, 6]
    ax.plot(lim, lim, "k--", lw=0.8, alpha=0.6, label="y = x")
    ax.axhline(0, color="gray", lw=0.4, alpha=0.5)
    ax.axvline(0, color="gray", lw=0.4, alpha=0.5)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(r"$\Phi_{init}$ (from PCMCI+ gate)")
    ax.set_title(ds)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
axes[0].set_ylabel(r"$\Phi_{final}$ (after training)")
fig.suptitle(r"Causal bias $\Phi$: PCMCI+ initialization vs. learned final value",
             y=1.02, fontsize=12)
plt.tight_layout()
plt.savefig(OUT / "fig2_phi_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"saved: {OUT}/fig2_phi_scatter.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 — Distribution shift: histograms of Φ_init and Φ_final per category
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 2, figsize=(10, 8), sharex=True)
bins = np.linspace(-6, 6, 50)
for row, ds in enumerate(datasets):
    pi, pf, M = data[ds]
    for col, (cat_name, cat_mask) in enumerate([
        ("M=0", M == 0),
        ("M=1", M == 1.0),
    ]):
        ax = axes[row, col]
        pi_c = pi[cat_mask]; pf_c = pf[cat_mask]
        ax.hist(pi_c, bins=bins, alpha=0.5, color="#888888", label=r"$\Phi_{init}$", edgecolor="white", linewidth=0.3)
        ax.hist(pf_c, bins=bins, alpha=0.7, color=COLORS[cat_name], label=r"$\Phi_{final}$", edgecolor="white", linewidth=0.3)
        ax.axvline(0, color="black", lw=0.4, alpha=0.5)
        if row == 0:
            ax.set_title(f"{cat_name} edges")
        if col == 0:
            ax.set_ylabel(f"{ds}\ncount")
        if row == 2:
            ax.set_xlabel(r"$\Phi$ value")
        # numeric annotations
        d = pf_c.mean() - pi_c.mean()
        ax.text(0.98, 0.95, f"Δ mean = {d:+.2f}\n|Δ| mean = {np.abs(pf_c-pi_c).mean():.2f}",
                transform=ax.transAxes, va="top", ha="right", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="lightgray", alpha=0.9))
        ax.legend(loc="upper left", fontsize=8, frameon=False)
fig.suptitle(r"Distribution of $\Phi$ before and after training, grouped by initial PCMCI+ gate",
             y=1.00, fontsize=12)
plt.tight_layout()
plt.savefig(OUT / "fig3_phi_distributions.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"saved: {OUT}/fig3_phi_distributions.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 4 — Summary metrics bar chart
# ─────────────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

# Panel A: |Δφ| mean per dataset per category
abs_delta_m0 = []
abs_delta_m1 = []
for ds in datasets:
    pi, pf, M = data[ds]
    d = pf - pi
    abs_delta_m0.append(np.abs(d[M == 0]).mean())
    abs_delta_m1.append(np.abs(d[M == 1.0]).mean())
x = np.arange(len(datasets)); w = 0.35
b1 = ax1.bar(x - w/2, abs_delta_m0, w, color=COLORS["M=0"], label="M=0 (no causal)")
b2 = ax1.bar(x + w/2, abs_delta_m1, w, color=COLORS["M=1"], label="M=1 (definitive)")
for b, v in zip(b1, abs_delta_m0):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.05, f"{v:.2f}", ha="center", fontsize=9)
for b, v in zip(b2, abs_delta_m1):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.05, f"{v:.2f}", ha="center", fontsize=9)
ax1.set_xticks(x); ax1.set_xticklabels(datasets)
ax1.set_ylabel(r"$|\Phi_{final} - \Phi_{init}|$ mean")
ax1.set_title(r"Magnitude of learned $\Phi$ shift" + "\n(higher = PCMCI+ prior overridden more)")
ax1.legend(loc="upper left", frameon=False, fontsize=9)
ax1.axhline(0.5, color="gray", ls=":", lw=0.7, alpha=0.7)
ax1.text(2.35, 0.55, "Δφ ≈ 0.5\n(prior mostly kept)", fontsize=8, color="gray", ha="right")

# Panel B: sign flip rate per dataset per category
flip_m0 = []; flip_m1 = []
for ds in datasets:
    pi, pf, M = data[ds]
    flip_m0.append(100 * ((pi[M == 0] * pf[M == 0]) < 0).mean())
    flip_m1.append(100 * ((pi[M == 1.0] * pf[M == 1.0]) < 0).mean())
b1 = ax2.bar(x - w/2, flip_m0, w, color=COLORS["M=0"], label="M=0")
b2 = ax2.bar(x + w/2, flip_m1, w, color=COLORS["M=1"], label="M=1")
for b, v in zip(b1, flip_m0):
    ax2.text(b.get_x() + b.get_width()/2, v + 0.15, f"{v:.1f}%", ha="center", fontsize=9)
for b, v in zip(b2, flip_m1):
    ax2.text(b.get_x() + b.get_width()/2, v + 0.15, f"{v:.1f}%", ha="center", fontsize=9)
ax2.set_xticks(x); ax2.set_xticklabels(datasets)
ax2.set_ylabel("Sign-flip rate (%)")
ax2.set_title(r"Fraction of edges with reversed sign" + "\n(higher = prior direction overridden)")
ax2.legend(loc="upper left", frameon=False, fontsize=9)
ax2.set_ylim(0, max(max(flip_m0), max(flip_m1)) * 1.4 + 0.5)

plt.tight_layout()
plt.savefig(OUT / "fig4_summary_metrics.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"saved: {OUT}/fig4_summary_metrics.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5 — Heatmap of |Δφ| for SWaT, τ=1 slice (single seed)
# ─────────────────────────────────────────────────────────────────────────────
# Take the first SWaT seed checkpoint for clarity
swat_ckpt = torch.load(DATASETS["SWaT"][0], map_location="cpu", weights_only=False)
sd = swat_ckpt["state_dict"]
M = sd["te_prior_gate"]              # [τ, N, N]
pf = sd["causal_mask_logits"]
pi = init_phi_from_M(M)
delta = (pf - pi).abs()              # [τ, N, N]

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for k, tau in enumerate([0, 2, 4]):   # τ=1, τ=3, τ=5 (indices 0, 2, 4)
    ax = axes[k]
    im = ax.imshow(delta[tau].numpy(), cmap="magma", aspect="auto",
                   vmin=0, vmax=delta.max().item())
    ax.set_title(fr"SWaT: $|\Delta\Phi|$ at $\tau$={tau+1}")
    ax.set_xlabel("target j")
    if k == 0:
        ax.set_ylabel("source i")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    # overlay M=1 edges with green outline
    M_slice = M[tau].numpy()
    ys, xs = np.where(M_slice == 1.0)
    if len(ys) > 0:
        ax.scatter(xs, ys, s=25, facecolors="none", edgecolors="lime", linewidths=0.9,
                   label="M=1 edges" if k == 0 else None)
    if k == 0 and len(ys) > 0:
        ax.legend(loc="upper right", fontsize=8, frameon=True, facecolor="white")

fig.suptitle(r"SWaT — spatial pattern of learned $\Phi$ shift by lag (single seed)",
             y=1.02, fontsize=12)
plt.tight_layout()
plt.savefig(OUT / "fig5_swat_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"saved: {OUT}/fig5_swat_heatmap.png")

print("\nAll figures saved to:", OUT)
