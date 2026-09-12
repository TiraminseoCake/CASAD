# cfval / server8 / pilot_49f630a

- exported: 2026-09-13T01:00:35+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 4 — {'success': 4} — **COMPLETE**
- exported eval jobs: 2, train jobs: 1; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SWaT | swat | 0 | last | 80 | A_off | 0.6765 | 0.5693 | 0.7346 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_on | 0.7532 | 0.6569 | 0.7434 | 1.0 | False |
| SWaT | swat | 0 | best_val | 62 | A_off | 0.6843 | 0.5712 | 0.7388 | 1.0 | False |
| SWaT | swat | 0 | best_val | 62 | A_on | 0.7549 | 0.6615 | 0.7470 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SWaT/swat/seed0/swat_cf_val | 80 | 80 / 0.0051344545319425 | 62 / 0.0051287867081799 | 83061 |
