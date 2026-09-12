# cfval / server8 / remaining_49f630a

- exported: 2026-09-13T01:00:37+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 10 — {'success': 10} — **COMPLETE**
- exported eval jobs: 6, train jobs: 3; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SWaT | swat | 1 | last | 80 | A_off | 0.7171 | 0.5809 | 0.7632 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_on | 0.7517 | 0.6180 | 0.7393 | 1.0 | False |
| SWaT | swat | 1 | best_val | 77 | A_off | 0.7169 | 0.5804 | 0.7629 | 1.0 | False |
| SWaT | swat | 1 | best_val | 77 | A_on | 0.7511 | 0.6135 | 0.7386 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_off | 0.6234 | 0.5298 | 0.6923 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7524 | 0.6652 | 0.7386 | 1.0 | False |
| SWaT | swat | 2 | best_val | 80 | A_off | 0.6234 | 0.5298 | 0.6923 | 1.0 | False |
| SWaT | swat | 2 | best_val | 80 | A_on | 0.7524 | 0.6652 | 0.7386 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.6325 | 0.5369 | 0.7155 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7312 | 0.6044 | 0.7377 | 1.0 | False |
| SWaT | swat | 3 | best_val | 76 | A_off | 0.6387 | 0.5402 | 0.7186 | 1.0 | False |
| SWaT | swat | 3 | best_val | 76 | A_on | 0.7344 | 0.6032 | 0.7376 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SWaT/swat/seed1/swat_cf_val | 80 | 80 / 0.0054798824060573 | 77 / 0.0051760359088776 | 111415 |
| train/SWaT/swat/seed2/swat_cf_val | 80 | 80 / 0.0049293918750308 | 80 / 0.0049293918750308 | 66409 |
| train/SWaT/swat/seed3/swat_cf_val | 80 | 80 / 0.0052403948032815 | 76 / 0.0049704159083291 | 107262 |
