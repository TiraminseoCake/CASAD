"""Case study & scoring channel visualization.

Loads a trained model checkpoint, runs inference on test data,
and produces:
  1. Score timeline plot (S_pred, S_str, S_route, A vs ground truth labels)
  2. Case study: find segments where S_pred is low but S_str/S_route is high
     → anomalies that prediction-only methods would miss
  3. CRS vs current E heatmap at anomaly vs normal time points

Usage:
    python scripts/visualize_scores.py \
        --cfg scripts/configs/swat.yaml \
        --seed 0 \
        --entity swat \
        --out_dir figures/case_study
"""
import argparse
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.build import load_entity
from model.build import build_model, build_causal_prior_cached, apply_prior_to_model
from model.scoring import score_windows, score_components_to_timeline
from layers.ops import normalize_causal_tensor_torch
from utils.parser import load_config


def pct(x):
    return float(x) * 100.0 if np.isfinite(x) else float('nan')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', required=True)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--entity', type=str, default='')
    parser.add_argument('--out_dir', type=str, default='figures/case_study')
    parser.add_argument('--max_points', type=int, default=5000,
                        help='Max points for timeline plot (downsample if longer)')
    args = parser.parse_args()

    cfg = load_config(args.cfg, [])
    os.makedirs(args.out_dir, exist_ok=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load entity
    entity_name = args.entity or cfg.DATA.ENTITIES.split(',')[0].strip()
    entity = load_entity(cfg, entity_name)

    N = entity.N
    print(f'Entity: {entity.name}, N={N}, Ttr={entity.T_train}, Tte={entity.T_test}')

    # Build model + prior
    model = build_model(cfg, N).to(device)
    te_weight_np, te_gate_np = build_causal_prior_cached(cfg, entity.train_z, entity.name)
    apply_prior_to_model(cfg, model, te_weight_np, te_gate_np)

    # Find checkpoint
    result_dirs = sorted([
        d for d in os.listdir(cfg.RESULT_DIR)
        if os.path.isdir(os.path.join(cfg.RESULT_DIR, d))
    ])
    ckpt_path = None
    for rd in reversed(result_dirs):
        cp = os.path.join(cfg.RESULT_DIR, rd, 'ckpt', f'seed{args.seed}_best.pt')
        if os.path.exists(cp):
            ckpt_path = cp
            break
        cp2 = os.path.join(cfg.RESULT_DIR, rd, 'ckpt', f'seed{args.seed}_final.pt')
        if os.path.exists(cp2):
            ckpt_path = cp2
            break

    if ckpt_path is None:
        print(f'No checkpoint found for seed {args.seed}. Training from scratch for scoring...')
        # Train briefly just for demonstration
        from trainer import PicaadTrainer
        trainer = PicaadTrainer(cfg, model, entity.train_z, device, seed=args.seed)
        trainer.train()
    else:
        print(f'Loading checkpoint: {ckpt_path}')
        state = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(state['model'] if 'model' in state else state)

    # Score test data
    model.eval()

    class ScoringArgs:
        pass
    sargs = ScoringArgs()
    sargs.p_agg = cfg.PICAAD.SCORING.P_AGG
    sargs.p_topk = cfg.PICAAD.SCORING.P_TOPK
    sargs.c_agg = cfg.PICAAD.SCORING.C_AGG
    sargs.c_topk = cfg.PICAAD.SCORING.C_TOPK
    sargs.g_agg = cfg.PICAAD.SCORING.G_AGG
    sargs.g_topk = cfg.PICAAD.SCORING.G_TOPK
    sargs.causal_lag_agg = cfg.PICAAD.SCORING.CAUSAL_LAG_AGG
    sargs.graph_lag_agg = cfg.PICAAD.SCORING.GRAPH_LAG_AGG
    sargs.score_alpha = cfg.PICAAD.SCORING.SCORE_ALPHA
    sargs.score_beta = cfg.PICAAD.SCORING.SCORE_BETA
    sargs.calib_clip_min = cfg.PICAAD.SCORING.CALIB_CLIP_MIN

    test_scores = score_windows(model, entity.test_z, device,
                                batch=cfg.TEST.BATCH_SIZE, args=sargs)

    Tt = entity.T_test
    start = entity.T_test - len(test_scores['P'])
    y = entity.test_label

    score_t = score_components_to_timeline(
        {k: test_scores[k] for k in ['P', 'C', 'G', 'S', 'A']},
        Tt=Tt, start=start,
    )
    P_t = score_t['P_t']
    C_t = score_t['C_t']
    G_t = score_t['G_t']
    S_t = score_t['S_t']
    A_t = score_t['A_t']

    # ============================================================
    # Plot 1: Score Timeline
    # ============================================================
    max_pts = args.max_points
    if Tt > max_pts:
        sel = np.linspace(0, Tt - 1, max_pts).astype(int)
    else:
        sel = np.arange(Tt)

    fig, axes = plt.subplots(5, 1, figsize=(16, 12), sharex=True)

    axes[0].fill_between(sel, 0, y[sel], alpha=0.3, color='red', label='Anomaly')
    axes[0].set_ylabel('Label')
    axes[0].legend(loc='upper right')

    for ax, arr, label, color in [
        (axes[1], P_t, 'S_pred', '#3498db'),
        (axes[2], C_t, 'S_str (C)', '#e74c3c'),
        (axes[3], G_t, 'S_route (G)', '#2ecc71'),
        (axes[4], A_t, 'A (final)', '#8e44ad'),
    ]:
        valid = np.isfinite(arr[sel])
        ax.plot(sel[valid], arr[sel][valid], linewidth=0.8, color=color)
        # shade anomaly regions
        ax.fill_between(sel, 0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 1,
                         where=y[sel] == 1, alpha=0.1, color='red')
        ax.set_ylabel(label)

    axes[-1].set_xlabel('Time')
    plt.suptitle(f'{entity.name} — Scoring Channel Timeline (seed {args.seed})', fontsize=14)
    plt.tight_layout()
    path1 = os.path.join(args.out_dir, f'{entity.name}_score_timeline.png')
    plt.savefig(path1, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path1}')

    # ============================================================
    # Plot 2: Case Study — S_pred low but S_str/S_route high
    # ============================================================
    valid_mask = np.isfinite(P_t) & np.isfinite(S_t) & (y == 1)
    if valid_mask.sum() > 0:
        p_anom = P_t[valid_mask]
        s_anom = S_t[valid_mask]
        t_anom = np.where(valid_mask)[0]

        # Find anomaly points where P is below median but S is above median
        p_med = np.median(p_anom)
        s_med = np.median(s_anom)
        interesting = (p_anom < p_med) & (s_anom > s_med)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(p_anom[~interesting], s_anom[~interesting],
                   alpha=0.3, s=10, c='gray', label='Other anomaly points')
        ax.scatter(p_anom[interesting], s_anom[interesting],
                   alpha=0.6, s=20, c='red', label='Low P, High S (structure-detected)')
        ax.axvline(p_med, ls='--', color='blue', alpha=0.5, label=f'P median={p_med:.3f}')
        ax.axhline(s_med, ls='--', color='green', alpha=0.5, label=f'S median={s_med:.3f}')
        ax.set_xlabel('S_pred (prediction error)')
        ax.set_ylabel('S_str + S_route (structural deviation)')
        ax.set_title(f'{entity.name} — Anomaly Points: Prediction vs Structure')
        ax.legend(fontsize=9)
        path2 = os.path.join(args.out_dir, f'{entity.name}_case_study_scatter.png')
        plt.savefig(path2, dpi=150, bbox_inches='tight')
        plt.close()
        print(f'Saved: {path2}')
        print(f'  Anomaly points: {valid_mask.sum()}, '
              f'Low-P High-S: {interesting.sum()} ({interesting.sum()/max(valid_mask.sum(),1)*100:.1f}%)')
    else:
        print('No anomaly points found for case study scatter.')

    # ============================================================
    # Plot 3: Complementary detection — zoom into specific segment
    # ============================================================
    # Find a segment where S is high but P is relatively low
    window = 200
    if valid_mask.sum() > window:
        # Rolling average of P and S
        p_roll = np.convolve(np.nan_to_num(P_t), np.ones(window)/window, mode='same')
        s_roll = np.convolve(np.nan_to_num(S_t), np.ones(window)/window, mode='same')

        # Score: high S, low P, in anomaly region
        complementary_score = np.where(y == 1, s_roll / (p_roll + 1e-8), 0)
        best_t = int(np.argmax(complementary_score))
        zoom_start = max(0, best_t - 500)
        zoom_end = min(Tt, best_t + 500)
        zoom = slice(zoom_start, zoom_end)
        t_range = np.arange(zoom_start, zoom_end)

        fig, axes = plt.subplots(4, 1, figsize=(14, 8), sharex=True)
        axes[0].fill_between(t_range, 0, y[zoom], alpha=0.4, color='red')
        axes[0].set_ylabel('Label')
        axes[0].set_title(f'{entity.name} — Zoom [{zoom_start}:{zoom_end}] '
                          f'(structure catches what prediction misses)')

        axes[1].plot(t_range, P_t[zoom], color='#3498db', lw=1.2)
        axes[1].set_ylabel('S_pred')
        axes[1].fill_between(t_range, 0, axes[1].get_ylim()[1] if axes[1].get_ylim()[1] > 0 else 1,
                              where=y[zoom] == 1, alpha=0.1, color='red')

        axes[2].plot(t_range, S_t[zoom], color='#e74c3c', lw=1.2)
        axes[2].set_ylabel('S_str + S_route')
        axes[2].fill_between(t_range, 0, axes[2].get_ylim()[1] if axes[2].get_ylim()[1] > 0 else 1,
                              where=y[zoom] == 1, alpha=0.1, color='red')

        axes[3].plot(t_range, A_t[zoom], color='#8e44ad', lw=1.2)
        axes[3].set_ylabel('A (final)')
        axes[3].set_xlabel('Time')

        plt.tight_layout()
        path3 = os.path.join(args.out_dir, f'{entity.name}_case_study_zoom.png')
        plt.savefig(path3, dpi=150, bbox_inches='tight')
        plt.close()
        print(f'Saved: {path3}')

    print('Done.')


if __name__ == '__main__':
    main()
