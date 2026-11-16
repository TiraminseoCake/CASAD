"""Post-hoc score-composition evaluation (paper table): P only, C only, and A = P + C from the same checkpoint.

For every run directory (<entity>_seed<s>, holding config.yaml and ckpt/<entity>_seed<s>_<tag>.pt) the selected
checkpoint is loaded the way training left it (build -> cached prior -> load_state_dict -> epoch) and test scores
go through the same path as utils.evaluation.run_epoch_eval. The recomputed A metrics are checked against the
run's own select_<tag>.csv. No training, no prior refit (cache hit only).

Usage: python scripts/eval_score_components.py --runs <run_dir> [<run_dir> ...] --out <csv> [--tag best_smooth]
"""
import argparse
import os
import re
import sys

import numpy as np
import pandas as pd
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_cfg_defaults
from datasets.build import load_entity, split_train_val
from model.build import apply_prior_to_model, build_causal_prior_cached, build_model
from model.scoring import score_components_to_timeline, score_windows
from utils.evaluation import paper_eval_one

METRICS = [('F1', 'Standard-F1'), ('R_F1', 'R-based-F1'), ('Aff_F', 'Affiliation-F'),
           ('AUC_ROC', 'AUC-ROC'), ('AUC_PR', 'AUC-PR'), ('VUS_ROC', 'VUS-ROC'), ('VUS_PR', 'VUS-PR')]
SCORES = {'A': 'A', 'P': 'P_raw', 'C': 'C_raw'}


@torch.no_grad()
def score_run(run_dir, tag, device):
    m = re.fullmatch(r'(.+)_seed(\d+)', os.path.basename(os.path.normpath(run_dir)))
    entity_name, seed = m.group(1), int(m.group(2))
    cfg = get_cfg_defaults()
    cfg.merge_from_file(os.path.join(run_dir, 'config.yaml'))
    cfg.PICAAD.PRIOR.CACHE_REBUILD = False
    entity = load_entity(cfg, entity_name)
    prior_input, _ = split_train_val(entity.train_z, cfg.PICAAD.VAL_RATIO)
    te_w, te_g = build_causal_prior_cached(cfg, prior_input, entity.name)
    model = build_model(cfg, N=entity.N).to(device)
    apply_prior_to_model(cfg, model, te_w, te_g)
    payload = torch.load(os.path.join(run_dir, 'ckpt', f'{entity_name}_seed{seed}_{tag}.pt'),
                         map_location=device, weights_only=False)
    assert np.allclose(payload['mu'], entity.mu) and np.allclose(payload['sd'], entity.sd)
    model.load_state_dict(payload['state_dict'])
    model._current_epoch = int(payload['epoch'])
    model.eval()

    sc = score_windows(model, entity.test_z, device, batch=cfg.TEST.BATCH_SIZE,
                       scoring_cfg=cfg.PICAAD.SCORING, calibrator=None)
    start = cfg.PICAAD.L - 1
    tl = score_components_to_timeline({k: sc[k] for k in SCORES.values()}, Tt=entity.test_z.shape[0], start=start)
    run_csv = pd.read_csv(os.path.join(run_dir, f'{entity_name}_seed{seed}_select_{tag}.csv')).iloc[-1]
    assert int(run_csv['epoch']) == int(payload['epoch'])
    rows = []
    for name, key in SCORES.items():
        met = paper_eval_one(tl[f'{key}_t'], entity.y, start, cfg.EVAL)
        row = {'entity': entity_name, 'seed': seed, 'epoch': int(payload['epoch']), 'score': name,
               **{k: 100 * float(met[src]) for k, src in METRICS}}
        if name == 'A':
            row['max_abs_diff_vs_run_csv'] = max(abs(row[k] / 100 - float(run_csv[k])) for k, _ in METRICS)
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', nargs='+', required=True)
    ap.add_argument('--tag', default='best_smooth')
    ap.add_argument('--out', required=True)
    ap.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    args = ap.parse_args()
    rows = []
    for rd in args.runs:
        r = score_run(rd, args.tag, args.device)
        rows += r
        print(os.path.basename(rd), ' '.join(f"{x['score']}:A-PR={x['AUC_PR']:.2f}" for x in r),
              f"gap={r[0]['max_abs_diff_vs_run_csv']:.1e}", flush=True)
    pd.DataFrame(rows).to_csv(args.out, index=False)
    print('saved', args.out)


if __name__ == '__main__':
    main()
