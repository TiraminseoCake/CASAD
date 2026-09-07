#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-score trained models with different fusion strategies.
No re-training needed -- loads checkpoint, computes raw P/C/G scores,
applies different fusion formulas, evaluates each.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import argparse
import glob
import numpy as np
import torch

from config import get_cfg_defaults
from datasets.build import load_entity
from datasets.sliding_window import SlidingWindowDataset
from model.build import build_model
from model.scoring import score_windows_raw, fit_score_calibrator
from utils.evaluation import paper_eval_one
from utils.misc import robust_loc_scale, robust_zscore, pct, set_seed


FUSION_STRATEGIES = {
    "P*S (current)":    lambda P, C, G: P * (C + G),
    "P+C+G (additive)": lambda P, C, G: P + C + G,
    "P+C (no routing)": lambda P, C, G: P + C,
    "P+0.5C":           lambda P, C, G: P + 0.5 * C,
    "0.5P+C":           lambda P, C, G: 0.5 * P + C,
    "P+C+0.3G":         lambda P, C, G: P + C + 0.3 * G,
    "2P+C":             lambda P, C, G: 2.0 * P + C,
}


def calibrate_component(raw_train, raw_test):
    center, scale = robust_loc_scale(raw_train)
    train_z = robust_zscore(raw_train, center, scale, clip_min=0.0)
    test_z = robust_zscore(raw_test, center, scale, clip_min=0.0)
    return train_z, test_z


def run_one_entity(cfg, entity_name, seed, result_dir, device, fusions):
    set_seed(seed)

    entity = load_entity(cfg, entity_name)
    train_z = entity.train_z
    test_z = entity.test_z
    y = entity.y

    ckpt_dir = os.path.join(result_dir, entity_name, f"seed{seed}", "ckpt")
    ckpt_files = sorted(glob.glob(os.path.join(ckpt_dir, "*.pt")))
    if not ckpt_files:
        return None

    best_ep = None
    best_score = -1
    for cf in ckpt_files:
        ckpt = torch.load(cf, map_location="cpu")
        m = ckpt.get("metrics", {})
        sel = m.get("AUC_PR", 0) + m.get("AUC_ROC", 0) + m.get("F1", 0) + m.get("VUS_PR", 0)
        if sel > best_score:
            best_score = sel
            best_ep = cf
    if best_ep is None:
        return None

    ckpt = torch.load(best_ep, map_location=device)
    model = build_model(cfg, N=train_z.shape[1])
    model.load_state_dict(ckpt["state_dict"])
    model = model.to(device)
    model.eval()

    scoring_cfg = cfg.PICAAD.SCORING

    with torch.no_grad():
        train_raw = score_windows_raw(model, train_z, device,
                                       batch=cfg.TRAIN.BATCH_SIZE,
                                       scoring_cfg=scoring_cfg)
        test_raw = score_windows_raw(model, test_z, device,
                                      batch=cfg.TEST.BATCH_SIZE,
                                      scoring_cfg=scoring_cfg)

    P_train, P_test = calibrate_component(train_raw["P_raw"], test_raw["P_raw"])
    C_train, C_test = calibrate_component(train_raw["C_raw"], test_raw["C_raw"])
    G_train, G_test = calibrate_component(train_raw["G_raw"], test_raw["G_raw"])

    Tt = test_z.shape[0]
    start = cfg.PICAAD.L - 1

    results = {}
    for fname, ffunc in fusions.items():
        A_test = ffunc(P_test, C_test, G_test).astype(np.float32)

        A_t = np.full((Tt,), np.nan, dtype=np.float32)
        A_t[start:] = A_test

        mtr = paper_eval_one(A_t, y, start, cfg.EVAL)
        results[fname] = mtr

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["PSM", "SMD", "SWaT"])
    ap.add_argument("--result_dir", required=True)
    ap.add_argument("--cfg", required=True)
    ap.add_argument("--seeds", default="0,1,2,3")
    ap.add_argument("--gpu", default="0")
    a = ap.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = a.gpu

    cfg = get_cfg_defaults()
    cfg.merge_from_file(a.cfg)
    cfg.freeze()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    seeds = [int(s) for s in a.seeds.split(",")]

    SMD_ENTITIES = [
        f'machine-{g}-{i}'
        for g, n in [(1, 8), (2, 9), (3, 11)]
        for i in range(1, n + 1)
    ]

    entities = {
        "PSM": ["PSM"],
        "SMD": SMD_ENTITIES,
        "SWaT": ["swat"],
    }[a.dataset]

    fusions = FUSION_STRATEGIES

    all_results = {fname: {m: [] for m in [
        "AUC-PR", "AUC-ROC", "Standard-F1", "R-based-F1",
        "Affiliation-F", "VUS-ROC", "VUS-PR",
    ]} for fname in fusions}

    for ent in entities:
        for seed in seeds:
            res = run_one_entity(cfg, ent, seed, a.result_dir, device, fusions)
            if res is None:
                continue
            for fname, mtr in res.items():
                for mk in all_results[fname]:
                    v = mtr.get(mk, float("nan"))
                    if np.isfinite(v):
                        all_results[fname][mk].append(v)

    metric_labels = ["Standard-F1", "R-based-F1", "Affiliation-F",
                     "AUC-ROC", "AUC-PR", "VUS-ROC", "VUS-PR"]
    short_labels = ["F1", "R-F1", "Aff-F", "A-ROC", "A-PR", "V-ROC", "V-PR"]

    print(f"\n{'='*80}")
    print(f"  {a.dataset} — Fusion Strategy Comparison")
    print(f"{'='*80}")

    header = f"{'Strategy':<20}"
    for sl in short_labels:
        header += f" | {sl:>6}"
    print(header)
    print("-" * len(header))

    best_per_metric = {}
    for mi, ml in enumerate(metric_labels):
        best_val = -1
        for fname in fusions:
            vals = all_results[fname][ml]
            if vals:
                avg = np.mean(vals) * 100
                if avg > best_val:
                    best_val = avg
        best_per_metric[ml] = best_val

    for fname in fusions:
        row = f"{fname:<20}"
        for ml in metric_labels:
            vals = all_results[fname][ml]
            if vals:
                avg = np.mean(vals) * 100
                is_best = abs(avg - best_per_metric[ml]) < 0.005
                if is_best:
                    row += f" | {'**'+f'{avg:.2f}'+'**':>6}"
                else:
                    row += f" | {avg:>6.2f}"
            else:
                row += f" | {'N/A':>6}"
        print(row)

    print()


if __name__ == "__main__":
    main()
