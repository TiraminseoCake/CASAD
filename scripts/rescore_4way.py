#!/usr/bin/env python3
"""Re-score saved PICAAD checkpoints with 4 fusion variants.

For each checkpoint {entity}_seed{seed}_ep{k}.pt found under --source_dir,
loads the model, runs a single forward pass on train + test windows to
obtain raw (P, C, G) scores, and computes four score fusion variants:

  mult_raw    : P * (C + G)                       # current code default
  add_calib   : P̃ + C̃ + G̃                        # paper's stated form
  add_raw     : P + C + G
  mult_calib  : P̃ * (C̃ + G̃)

where the tilde denotes robust z-score (median/MAD) normalization computed
on training-window scores, followed by ReLU (clip to ≥ 0).

Original training results are NOT modified. Output goes under --out_dir
with a mirrored (entity, seed) layout, one CSV per fusion variant, matching
the schema of the existing *_epoch_metrics.csv so that
aggregate_best_epoch.py can be reused unchanged.

Usage
-----
Single (config, source_dir, entity_subset, seeds) job pinned to one GPU:

    CUDA_VISIBLE_DEVICES=0 python scripts/rescore_4way.py \\
        --cfg scripts/configs/psm.yaml \\
        --source_dir results/parallel/psm_20260701-221416 \\
        --out_dir    results/rescored/psm_baseline \\
        --entities   PSM \\
        --seeds      0,1,2,3

Multiple jobs can run in parallel on different GPUs by launching this
script once per shard.
"""
import argparse
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import get_cfg_defaults
from datasets.build import load_entity
from model.build import build_model
from model.scoring import score_components_to_timeline, score_windows_raw
from utils.evaluation import paper_eval_one
from utils.misc import robust_loc_scale, set_seed


def _load_cfg(cfg_path: str):
    cfg = get_cfg_defaults()
    cfg.merge_from_file(cfg_path)
    return cfg


FUSIONS = ['mult_raw', 'add_calib', 'add_raw', 'mult_calib']

METRIC_KEYS = [
    ('AUC-PR', 'AUC_PR'),
    ('AUC-ROC', 'AUC_ROC'),
    ('Standard-F1', 'F1'),
    ('PA-F1', 'PA_F1'),
    ('Event-based-F1', 'Event_F1'),
    ('R-based-F1', 'R_F1'),
    ('Affiliation-F', 'Aff_F'),
    ('VUS-ROC', 'VUS_ROC'),
    ('VUS-PR', 'VUS_PR'),
]


def _ckpt_epoch(ckpt_path: Path) -> int:
    """Return the numeric epoch encoded in a ckpt filename like foo_seed0_ep35.pt."""
    m = re.search(r'ep(\d+)\.pt$', ckpt_path.name)
    return int(m.group(1)) if m else -1


def _robust_normalize(arr: np.ndarray, calib):
    """Robust z-score using median/MAD, then ReLU (clip to ≥ 0)."""
    center = float(calib['center'])
    scale = max(float(calib['scale']), 1e-6)
    z = (arr.astype(np.float64) - center) / scale
    return np.maximum(z, 0.0).astype(np.float32)


def _compute_all_fusions(train_raw: dict, test_raw: dict, wanted=None):
    """Given train/test raw score dicts, return dict[fusion_name] -> A_test 1D array.
    Only computes fusions listed in `wanted` (defaults to all four)."""
    if wanted is None:
        wanted = FUSIONS
    wanted = set(wanted)
    P_te, C_te, G_te = test_raw['P_raw'], test_raw['C_raw'], test_raw['G_raw']

    # Only fit/normalize when a calib-based fusion is requested (saves work).
    needs_calib = bool(wanted & {'add_calib', 'mult_calib'})
    if needs_calib:
        P_ctr, P_scl = robust_loc_scale(train_raw['P_raw'])
        C_ctr, C_scl = robust_loc_scale(train_raw['C_raw'])
        G_ctr, G_scl = robust_loc_scale(train_raw['G_raw'])
        Pn = _robust_normalize(P_te, {'center': P_ctr, 'scale': P_scl})
        Cn = _robust_normalize(C_te, {'center': C_ctr, 'scale': C_scl})
        Gn = _robust_normalize(G_te, {'center': G_ctr, 'scale': G_scl})

    all_fusions = {}
    if 'mult_raw' in wanted:
        all_fusions['mult_raw'] = P_te * (C_te + G_te)
    if 'add_calib' in wanted:
        all_fusions['add_calib'] = Pn + Cn + Gn
    if 'add_raw' in wanted:
        all_fusions['add_raw'] = P_te + C_te + G_te
    if 'mult_calib' in wanted:
        all_fusions['mult_calib'] = Pn * (Cn + Gn)
    return all_fusions


def _eval_all_fusions(A_map, entity_y, start, eval_cfg):
    """Convert each fusion's window-level A to a full-length timeline and
    compute paper metrics. Returns dict[fusion] -> {metric_short: value}."""
    Tt = entity_y.shape[0]
    out = {}
    for name, A_win in A_map.items():
        A_t = np.full((Tt,), np.nan, dtype=np.float32)
        A_t[start:] = np.asarray(A_win, dtype=np.float32)
        raw = paper_eval_one(A_t, entity_y, start, eval_cfg)
        out[name] = {short: float(raw.get(long_key, float('nan')))
                     for long_key, short in METRIC_KEYS}
    return out


def rescore_one_seed(cfg, entity, seed_dir: Path, seed: int, device, wanted_fusions=None):
    """Iterate over all checkpoints for one (entity, seed) and return a list
    of per-epoch records. Each record is one row per fusion variant."""
    if wanted_fusions is None:
        wanted_fusions = FUSIONS
    ckpts = sorted(seed_dir.glob('ckpt/*_ep*.pt'), key=_ckpt_epoch)
    if not ckpts:
        return {name: [] for name in wanted_fusions}

    # Build model once (architecture is checkpoint-invariant); reload weights per epoch.
    model = build_model(cfg, N=entity.N).to(device)
    model.eval()

    start = cfg.PICAAD.L - 1
    records = {name: [] for name in wanted_fusions}

    for ckpt_path in ckpts:
        epoch = _ckpt_epoch(ckpt_path)
        try:
            ck = torch.load(ckpt_path, map_location=device, weights_only=False)
        except Exception as exc:
            print(f'    [warn] failed to load {ckpt_path.name}: {exc}', flush=True)
            continue

        try:
            model.load_state_dict(ck['state_dict'], strict=True)
        except Exception as exc:
            print(f'    [warn] state_dict mismatch for {ckpt_path.name}: {exc}', flush=True)
            continue

        # `_current_epoch` is a plain Python attribute (not in state_dict) that
        # gates warmup_ramp for the causal attention bias. Restore it so the
        # model behaves identically to the original training-time eval.
        model._current_epoch = int(ck.get('epoch', epoch))

        with torch.no_grad():
            train_raw = score_windows_raw(model, entity.train_z, device,
                                          batch=cfg.TRAIN.BATCH_SIZE,
                                          scoring_cfg=cfg.PICAAD.SCORING)
            test_raw = score_windows_raw(model, entity.test_z, device,
                                         batch=cfg.TEST.BATCH_SIZE,
                                         scoring_cfg=cfg.PICAAD.SCORING)

        A_map = _compute_all_fusions(train_raw, test_raw, wanted=wanted_fusions)
        metric_map = _eval_all_fusions(A_map, entity.y, start, cfg.EVAL)

        for name in wanted_fusions:
            row = {'epoch': epoch, 'is_final': 0, **metric_map[name]}
            records[name].append(row)

    # Mark the largest epoch as final to match the schema of existing csv.
    for name in wanted_fusions:
        if records[name]:
            records[name][-1]['is_final'] = 1

    return records


def write_seed_csvs(records: dict, out_seed_dir: Path, entity_name: str, seed: int):
    out_seed_dir.mkdir(parents=True, exist_ok=True)
    schema_cols = ['epoch', 'is_final'] + [short for _, short in METRIC_KEYS]
    for name, rows in records.items():
        if not rows:
            continue
        df = pd.DataFrame(rows)[schema_cols]
        # Match the existing filename convention so aggregate_best_epoch.py picks it up.
        out_path = out_seed_dir / f'{entity_name}_seed{seed}_epoch_metrics_{name}.csv'
        df.to_csv(out_path, index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cfg', required=True, help='YAML config used for the original run')
    ap.add_argument('--source_dir', required=True,
                    help='Original run dir, e.g. results/parallel/psm_20260701-221416')
    ap.add_argument('--out_dir', required=True,
                    help='Where to write the four *_epoch_metrics_{fusion}.csv files')
    ap.add_argument('--entities', default='',
                    help='Comma-separated entity subset. Default: all subdirs under source_dir')
    ap.add_argument('--seeds', default='0,1,2,3', help='Comma-separated seeds to process')
    ap.add_argument('--limit_epochs', default='', help='(debug) comma-separated epoch subset')
    ap.add_argument('--fusions', default=','.join(FUSIONS),
                    help='Comma-separated fusion subset. Default: all four')
    a = ap.parse_args()

    wanted_fusions = [f.strip() for f in a.fusions.split(',') if f.strip() in FUSIONS]
    if not wanted_fusions:
        raise SystemExit(f'--fusions produced empty subset (valid: {FUSIONS})')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'[rescore] device={device}', flush=True)

    cfg = _load_cfg(a.cfg)
    cfg.freeze()

    source_dir = Path(a.source_dir).resolve()
    out_dir = Path(a.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if a.entities.strip():
        entities = [e.strip() for e in a.entities.split(',') if e.strip()]
    else:
        entities = sorted([p.name for p in source_dir.iterdir()
                           if p.is_dir() and (p / 'seed0').exists()])

    seeds = [int(s) for s in a.seeds.split(',') if s.strip()]

    print(f'[rescore] source={source_dir}', flush=True)
    print(f'[rescore] out={out_dir}', flush=True)
    print(f'[rescore] entities={entities}', flush=True)
    print(f'[rescore] seeds={seeds}', flush=True)
    print(f'[rescore] fusions={wanted_fusions}', flush=True)

    set_seed(0)  # deterministic scoring (forward passes are stochastic-free anyway)

    n_total = len(entities) * len(seeds)
    n_done = 0
    for ent_name in entities:
        try:
            entity = load_entity(cfg, ent_name)
        except Exception as exc:
            print(f'  [skip] entity {ent_name}: {exc}', flush=True)
            continue

        for seed in seeds:
            seed_dir = source_dir / ent_name / f'seed{seed}'
            if not seed_dir.exists():
                print(f'  [skip] missing {seed_dir}', flush=True)
                continue

            print(f'  [{n_done+1}/{n_total}] {ent_name} seed{seed} ...', flush=True)
            records = rescore_one_seed(cfg, entity, seed_dir, seed, device,
                                       wanted_fusions=wanted_fusions)
            out_seed_dir = out_dir / ent_name / f'seed{seed}'
            write_seed_csvs(records, out_seed_dir, ent_name, seed)
            n_done += 1

    print(f'[rescore] done: {n_done}/{n_total} seed-jobs', flush=True)


if __name__ == '__main__':
    main()
