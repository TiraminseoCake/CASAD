# sp2x2 / ks / soft_prior_2x2_ks

- exported: 2026-10-12T17:54:46+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: f50147db4d35297fa72dc2b7e15555c27a1d01bc
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 24 — {'success': 24} — **COMPLETE**
- exported eval jobs: 8, train jobs: 8; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| PSM | PSM | 0 | best_val | 80 | A_off | 0.4430 | 0.4270 | 0.4371 | 0.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_off | 0.4432 | 0.4272 | 0.4370 | 0.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_off | 0.4433 | 0.4273 | 0.4371 | 0.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_off | 0.4433 | 0.4272 | 0.4372 | 0.0 | False |
| SMD | machine-1-1 | 0 | best_val | 78 | A_off | 0.4940 | 0.5602 | 0.4794 | 0.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.4938 | 0.5607 | 0.4743 | 0.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.4851 | 0.5537 | 0.4679 | 0.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.4918 | 0.5598 | 0.4781 | 0.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/PSM/PSM/seed0/psm_sp2x2_t0 | 80 | 80 / 0.2255892531743166 | 80 / 0.2255892531743166 | 4800 |
| train/PSM/PSM/seed0/psm_sp2x2_t1 | 80 | 80 / 0.2256053734423372 | 80 / 0.2256053734423372 | 4734 |
| train/PSM/PSM/seed0/psm_sp2x2_t2 | 80 | 80 / 0.2258663359619813 | 80 / 0.2258663359619813 | 4886 |
| train/PSM/PSM/seed0/psm_sp2x2_t3 | 80 | 80 / 0.2267058183908615 | 80 / 0.2267058183908615 | 4791 |
| train/SMD/machine-1-1/seed0/smd_sp2x2_t0 | 80 | 80 / 0.1806970010815186 | 78 / 0.1798028193507504 | 1406 |
| train/SMD/machine-1-1/seed0/smd_sp2x2_t1 | 80 | 80 / 0.1820655681467514 | 79 / 0.1798230459698633 | 1391 |
| train/SMD/machine-1-1/seed0/smd_sp2x2_t2 | 80 | 80 / 0.1820707010580528 | 79 / 0.1796166839561481 | 1375 |
| train/SMD/machine-1-1/seed0/smd_sp2x2_t3 | 80 | 80 / 0.1823147981885914 | 79 / 0.1795781794957357 | 1372 |
