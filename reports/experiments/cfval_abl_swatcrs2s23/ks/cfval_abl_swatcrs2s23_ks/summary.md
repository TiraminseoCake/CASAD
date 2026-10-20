# cfval_abl_swatcrs2s23 / ks / cfval_abl_swatcrs2s23_ks

- exported: 2026-10-20T20:26:48+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 28 — {'success': 28} — **COMPLETE**
- exported eval jobs: 16, train jobs: 8; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SWaT | swat | 2 | last | 80 | A_off | 0.6313 | 0.5414 | 0.7028 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7531 | 0.6394 | 0.7387 | 1.0 | False |
| SWaT | swat | 2 | best_val | 59 | A_off | 0.6723 | 0.5680 | 0.7258 | 1.0 | False |
| SWaT | swat | 2 | best_val | 59 | A_on | 0.7474 | 0.6167 | 0.7386 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.6835 | 0.5532 | 0.7515 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7480 | 0.6076 | 0.7385 | 1.0 | False |
| SWaT | swat | 3 | best_val | 72 | A_off | 0.7002 | 0.5623 | 0.7520 | 1.0 | False |
| SWaT | swat | 3 | best_val | 72 | A_on | 0.7485 | 0.6099 | 0.7384 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_off | 0.6234 | 0.5298 | 0.6923 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7524 | 0.6652 | 0.7386 | 1.0 | False |
| SWaT | swat | 2 | best_val | 80 | A_off | 0.6234 | 0.5298 | 0.6923 | 1.0 | False |
| SWaT | swat | 2 | best_val | 80 | A_on | 0.7524 | 0.6652 | 0.7386 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.6325 | 0.5369 | 0.7155 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7312 | 0.6044 | 0.7377 | 1.0 | False |
| SWaT | swat | 3 | best_val | 76 | A_off | 0.6387 | 0.5402 | 0.7186 | 1.0 | False |
| SWaT | swat | 3 | best_val | 76 | A_on | 0.7344 | 0.6032 | 0.7376 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_off | 0.6264 | 0.5191 | 0.7078 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7487 | 0.6119 | 0.7385 | 1.0 | False |
| SWaT | swat | 2 | best_val | 67 | A_off | 0.6020 | 0.4911 | 0.6842 | 1.0 | False |
| SWaT | swat | 2 | best_val | 67 | A_on | 0.7479 | 0.6094 | 0.7385 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.6942 | 0.5691 | 0.7555 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7533 | 0.6375 | 0.7382 | 1.0 | False |
| SWaT | swat | 3 | best_val | 53 | A_off | 0.6878 | 0.5702 | 0.7536 | 1.0 | False |
| SWaT | swat | 3 | best_val | 53 | A_on | 0.7563 | 0.6249 | 0.7383 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_off | 0.7482 | 0.6086 | 0.7782 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7086 | 0.5908 | 0.7336 | 1.0 | False |
| SWaT | swat | 2 | best_val | 2 | A_off | 0.4147 | 0.3805 | 0.5667 | 1.0 | False |
| SWaT | swat | 2 | best_val | 2 | A_on | 0.7482 | 0.6527 | 0.7385 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.7335 | 0.6008 | 0.7911 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7482 | 0.6289 | 0.7420 | 1.0 | False |
| SWaT | swat | 3 | best_val | 79 | A_off | 0.7323 | 0.5985 | 0.7910 | 1.0 | False |
| SWaT | swat | 3 | best_val | 79 | A_on | 0.7484 | 0.6230 | 0.7397 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SWaT/swat/seed2/swat_cf_val_perm0_crsoff | 80 | 80 / 0.0051428281755355 | 59 / 0.0049107645926399 | 103304 |
| train/SWaT/swat/seed3/swat_cf_val_perm0_crsoff | 80 | 80 / 0.0051362669680361 | 72 / 0.0049462348384827 | 104503 |
| train/SWaT/swat/seed2/swat_cf_val_perm0_crson | 80 | 80 / 0.0049293918750308 | 80 / 0.0049293918750308 | 105104 |
| train/SWaT/swat/seed3/swat_cf_val_perm0_crson | 80 | 80 / 0.0052403948032815 | 76 / 0.0049704159083291 | 80479 |
| train/SWaT/swat/seed2/swat_cf_val_perm2_crsoff | 80 | 80 / 0.0048756304110764 | 67 / 0.0046879191827483 | 229223 |
| train/SWaT/swat/seed3/swat_cf_val_perm2_crsoff | 80 | 80 / 0.0062780537919 | 53 / 0.0055135827829411 | 228607 |
| train/SWaT/swat/seed2/swat_cf_val_perm2_crson | 80 | 80 / 0.0156226175922394 | 2 / 0.0111169817294397 | 225005 |
| train/SWaT/swat/seed3/swat_cf_val_perm2_crson | 80 | 80 / 0.011776569589028 | 79 / 0.0108407187543519 | 226205 |
