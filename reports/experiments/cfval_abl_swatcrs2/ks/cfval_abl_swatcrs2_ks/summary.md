# cfval_abl_swatcrs2 / ks / cfval_abl_swatcrs2_ks

- exported: 2026-10-20T20:26:38+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 28 — {'success': 28} — **COMPLETE**
- exported eval jobs: 16, train jobs: 8; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SWaT | swat | 0 | last | 80 | A_off | 0.7023 | 0.5884 | 0.7442 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_on | 0.7467 | 0.6358 | 0.7386 | 1.0 | False |
| SWaT | swat | 0 | best_val | 73 | A_off | 0.6959 | 0.5847 | 0.7368 | 1.0 | False |
| SWaT | swat | 0 | best_val | 73 | A_on | 0.7472 | 0.6407 | 0.7386 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_off | 0.7217 | 0.5792 | 0.7672 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_on | 0.7476 | 0.5997 | 0.7394 | 1.0 | False |
| SWaT | swat | 1 | best_val | 74 | A_off | 0.7222 | 0.5797 | 0.7673 | 1.0 | False |
| SWaT | swat | 1 | best_val | 74 | A_on | 0.7484 | 0.6004 | 0.7393 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_off | 0.6765 | 0.5693 | 0.7346 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_on | 0.7532 | 0.6569 | 0.7434 | 1.0 | False |
| SWaT | swat | 0 | best_val | 62 | A_off | 0.6843 | 0.5712 | 0.7388 | 1.0 | False |
| SWaT | swat | 0 | best_val | 62 | A_on | 0.7549 | 0.6615 | 0.7470 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_off | 0.7171 | 0.5809 | 0.7632 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_on | 0.7517 | 0.6180 | 0.7393 | 1.0 | False |
| SWaT | swat | 1 | best_val | 77 | A_off | 0.7169 | 0.5804 | 0.7629 | 1.0 | False |
| SWaT | swat | 1 | best_val | 77 | A_on | 0.7511 | 0.6135 | 0.7386 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_off | 0.6592 | 0.5460 | 0.7301 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_on | 0.7537 | 0.6374 | 0.7419 | 1.0 | False |
| SWaT | swat | 0 | best_val | 74 | A_off | 0.6456 | 0.5360 | 0.7255 | 1.0 | False |
| SWaT | swat | 0 | best_val | 74 | A_on | 0.7595 | 0.6367 | 0.7421 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_off | 0.6785 | 0.5670 | 0.7625 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_on | 0.7595 | 0.6537 | 0.7521 | 1.0 | False |
| SWaT | swat | 1 | best_val | 76 | A_off | 0.6731 | 0.5628 | 0.7415 | 1.0 | False |
| SWaT | swat | 1 | best_val | 76 | A_on | 0.7559 | 0.6431 | 0.7414 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_off | 0.7260 | 0.5911 | 0.7775 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_on | 0.7091 | 0.6130 | 0.7424 | 1.0 | False |
| SWaT | swat | 0 | best_val | 4 | A_off | 0.6768 | 0.5676 | 0.7377 | 1.0 | False |
| SWaT | swat | 0 | best_val | 4 | A_on | 0.7493 | 0.5988 | 0.7444 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_off | 0.7251 | 0.5978 | 0.7730 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_on | 0.7359 | 0.6216 | 0.7528 | 1.0 | False |
| SWaT | swat | 1 | best_val | 12 | A_off | 0.7116 | 0.5909 | 0.7708 | 1.0 | False |
| SWaT | swat | 1 | best_val | 12 | A_on | 0.7591 | 0.6490 | 0.7450 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SWaT/swat/seed0/swat_cf_val_perm0_crsoff | 80 | 80 / 0.0051475986864211 | 73 / 0.0049514689892432 | 109387 |
| train/SWaT/swat/seed1/swat_cf_val_perm0_crsoff | 80 | 80 / 0.0055690734401855 | 74 / 0.0051509114316716 | 108563 |
| train/SWaT/swat/seed0/swat_cf_val_perm0_crson | 80 | 80 / 0.0051344545319425 | 62 / 0.0051287867081799 | 107840 |
| train/SWaT/swat/seed1/swat_cf_val_perm0_crson | 80 | 80 / 0.0054798824060573 | 77 / 0.0051760359088776 | 109735 |
| train/SWaT/swat/seed0/swat_cf_val_perm2_crsoff | 80 | 80 / 0.0058981184276732 | 74 / 0.0050690916309353 | 227465 |
| train/SWaT/swat/seed1/swat_cf_val_perm2_crsoff | 80 | 80 / 0.0051849658407176 | 76 / 0.0049236625621119 | 223502 |
| train/SWaT/swat/seed0/swat_cf_val_perm2_crson | 80 | 80 / 0.0124383116009064 | 4 / 0.010385293797442 | 226646 |
| train/SWaT/swat/seed1/swat_cf_val_perm2_crson | 80 | 80 / 0.0115918523495341 | 12 / 0.0099181441854514 | 224521 |
