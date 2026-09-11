# cfval / ks / remaining_49f630a

- exported: 2026-09-11T16:02:49+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 111 — {'success': 111} — **COMPLETE**
- exported eval jobs: 68, train jobs: 34; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| PSM | PSM | 1 | last | 80 | A_off | 0.4571 | 0.4410 | 0.4405 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_on | 0.5322 | 0.4893 | 0.4799 | 1.0 | False |
| PSM | PSM | 1 | best_val | 80 | A_off | 0.4571 | 0.4410 | 0.4405 | 1.0 | False |
| PSM | PSM | 1 | best_val | 80 | A_on | 0.5322 | 0.4893 | 0.4799 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_off | 0.4561 | 0.4387 | 0.4413 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_on | 0.4886 | 0.4550 | 0.4664 | 1.0 | False |
| PSM | PSM | 2 | best_val | 74 | A_off | 0.4575 | 0.4398 | 0.4441 | 1.0 | False |
| PSM | PSM | 2 | best_val | 74 | A_on | 0.4886 | 0.4549 | 0.4664 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_off | 0.4278 | 0.4162 | 0.4484 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_on | 0.5503 | 0.5029 | 0.4882 | 1.0 | False |
| PSM | PSM | 3 | best_val | 78 | A_off | 0.4260 | 0.4144 | 0.4462 | 1.0 | False |
| PSM | PSM | 3 | best_val | 78 | A_on | 0.5495 | 0.5019 | 0.4870 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_off | 0.4984 | 0.5726 | 0.4705 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_on | 0.4022 | 0.4566 | 0.3980 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 77 | A_off | 0.5028 | 0.5750 | 0.4777 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 77 | A_on | 0.4029 | 0.4534 | 0.3986 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_off | 0.5144 | 0.5759 | 0.5008 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_on | 0.3971 | 0.4413 | 0.3963 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 80 | A_off | 0.5144 | 0.5759 | 0.5008 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 80 | A_on | 0.3971 | 0.4413 | 0.3963 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_off | 0.5161 | 0.5782 | 0.5010 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_on | 0.4201 | 0.4720 | 0.4016 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 80 | A_off | 0.5161 | 0.5782 | 0.5010 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 80 | A_on | 0.4201 | 0.4720 | 0.4016 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_off | 0.1810 | 0.1971 | 0.3315 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_on | 0.3459 | 0.3692 | 0.4267 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 78 | A_off | 0.1841 | 0.2006 | 0.3346 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 78 | A_on | 0.3475 | 0.3669 | 0.4281 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_off | 0.1550 | 0.1662 | 0.2705 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_on | 0.3130 | 0.3230 | 0.3987 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 68 | A_off | 0.1624 | 0.1736 | 0.2905 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 68 | A_on | 0.3196 | 0.3362 | 0.4117 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_off | 0.1759 | 0.1913 | 0.3191 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_on | 0.3466 | 0.3550 | 0.4231 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 70 | A_off | 0.1816 | 0.1982 | 0.3305 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 70 | A_on | 0.3382 | 0.3521 | 0.4261 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_off | 0.1751 | 0.1881 | 0.3108 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_on | 0.3115 | 0.3240 | 0.4058 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 77 | A_off | 0.1771 | 0.1920 | 0.3160 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 77 | A_on | 0.3174 | 0.3270 | 0.4141 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_off | 0.2397 | 0.2253 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_on | 0.2306 | 0.2345 | 0.3042 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 78 | A_off | 0.2409 | 0.2300 | 0.3098 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 78 | A_on | 0.2367 | 0.2442 | 0.3034 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_off | 0.2397 | 0.2249 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_on | 0.2545 | 0.2590 | 0.3232 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 80 | A_off | 0.2397 | 0.2249 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 80 | A_on | 0.2545 | 0.2590 | 0.3232 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_off | 0.2358 | 0.2199 | 0.3093 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_on | 0.2046 | 0.1911 | 0.2925 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 76 | A_off | 0.2352 | 0.2189 | 0.3093 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 76 | A_on | 0.2017 | 0.1840 | 0.2822 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_off | 0.2390 | 0.2252 | 0.3099 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_on | 0.2221 | 0.2222 | 0.2881 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 76 | A_off | 0.2381 | 0.2232 | 0.3099 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 76 | A_on | 0.2182 | 0.2181 | 0.2882 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_off | 0.1314 | 0.1170 | 0.1774 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_on | 0.1472 | 0.1397 | 0.2232 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 75 | A_off | 0.1316 | 0.1173 | 0.1776 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 75 | A_on | 0.1484 | 0.1414 | 0.2159 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_off | 0.1294 | 0.1150 | 0.1775 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_on | 0.1637 | 0.1638 | 0.2424 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 68 | A_off | 0.1305 | 0.1164 | 0.1776 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 68 | A_on | 0.1505 | 0.1441 | 0.2103 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_off | 0.1295 | 0.1151 | 0.1780 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_on | 0.1492 | 0.1444 | 0.2030 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 78 | A_off | 0.1291 | 0.1147 | 0.1781 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 78 | A_on | 0.1511 | 0.1462 | 0.2081 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_off | 0.1297 | 0.1149 | 0.1774 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_on | 0.1569 | 0.1555 | 0.2246 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_off | 0.1297 | 0.1149 | 0.1774 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_on | 0.1569 | 0.1555 | 0.2246 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_off | 0.5167 | 0.3757 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_on | 0.5223 | 0.3998 | 0.5506 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 74 | A_off | 0.5175 | 0.3761 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 74 | A_on | 0.5248 | 0.4104 | 0.5537 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_off | 0.5207 | 0.3814 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_on | 0.5434 | 0.4281 | 0.5568 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 79 | A_off | 0.5207 | 0.3813 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 79 | A_on | 0.5425 | 0.4247 | 0.5537 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_off | 0.5244 | 0.3820 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_on | 0.5562 | 0.4604 | 0.5507 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 69 | A_off | 0.5242 | 0.3878 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 69 | A_on | 0.5565 | 0.4547 | 0.5478 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_off | 0.5185 | 0.3686 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_on | 0.5325 | 0.4200 | 0.5650 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 76 | A_off | 0.5190 | 0.3688 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 76 | A_on | 0.5337 | 0.4273 | 0.5618 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_off | 0.8604 | 0.8392 | 0.8423 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_on | 0.8469 | 0.8216 | 0.7817 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 68 | A_off | 0.8610 | 0.8400 | 0.8427 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 68 | A_on | 0.8255 | 0.7959 | 0.7588 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_off | 0.8664 | 0.8452 | 0.8473 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_on | 0.8153 | 0.7937 | 0.7573 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 80 | A_off | 0.8664 | 0.8452 | 0.8473 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 80 | A_on | 0.8153 | 0.7937 | 0.7573 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_off | 0.8655 | 0.8448 | 0.8436 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_on | 0.7902 | 0.7473 | 0.7458 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 77 | A_off | 0.8647 | 0.8441 | 0.8431 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 77 | A_on | 0.7863 | 0.7446 | 0.7438 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_off | 0.8674 | 0.8460 | 0.8506 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_on | 0.7786 | 0.7344 | 0.7560 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 79 | A_off | 0.8676 | 0.8462 | 0.8506 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 79 | A_on | 0.7829 | 0.7388 | 0.7591 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_off | 0.6388 | 0.6478 | 0.7144 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_on | 0.5382 | 0.5429 | 0.5980 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 73 | A_off | 0.6394 | 0.6478 | 0.7140 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 73 | A_on | 0.5371 | 0.5417 | 0.6036 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_off | 0.6488 | 0.6564 | 0.7145 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_on | 0.5379 | 0.5460 | 0.6206 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 70 | A_off | 0.6477 | 0.6560 | 0.7149 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 70 | A_on | 0.5279 | 0.5340 | 0.6020 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_off | 0.6443 | 0.6530 | 0.7151 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_on | 0.4992 | 0.5052 | 0.5643 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 73 | A_off | 0.6443 | 0.6530 | 0.7134 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 73 | A_on | 0.4991 | 0.5048 | 0.5709 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_off | 0.6472 | 0.6552 | 0.7131 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_on | 0.4725 | 0.4775 | 0.5570 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 77 | A_off | 0.6474 | 0.6553 | 0.7134 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 77 | A_on | 0.4703 | 0.4755 | 0.5538 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_off | 0.2575 | 0.2132 | 0.3216 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_on | 0.1905 | 0.0899 | 0.2405 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 72 | A_off | 0.2576 | 0.2133 | 0.3209 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 72 | A_on | 0.1907 | 0.0887 | 0.2409 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_off | 0.2657 | 0.2232 | 0.3250 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_on | 0.1983 | 0.0927 | 0.2588 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 78 | A_off | 0.2635 | 0.2205 | 0.3248 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 78 | A_on | 0.2031 | 0.0961 | 0.2632 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_off | 0.2560 | 0.2113 | 0.3188 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_on | 0.1992 | 0.1030 | 0.2419 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 78 | A_off | 0.2561 | 0.2086 | 0.3181 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 78 | A_on | 0.2033 | 0.1058 | 0.2473 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_off | 0.2549 | 0.2084 | 0.3215 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_on | 0.2069 | 0.1017 | 0.2630 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 75 | A_off | 0.2562 | 0.2090 | 0.3186 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 75 | A_on | 0.2056 | 0.1012 | 0.2599 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/PSM/PSM/seed1/psm_cf_val | 80 | 80 / 0.2111137406439951 | 80 / 0.2111137406439951 | 4650 |
| train/PSM/PSM/seed2/psm_cf_val | 80 | 80 / 0.2104035403865575 | 74 / 0.2093808583795234 | 4634 |
| train/PSM/PSM/seed3/psm_cf_val | 80 | 80 / 0.2093353842731222 | 78 / 0.2083046531007546 | 4617 |
| train/SMD/machine-1-1/seed1/smd_cf_val | 80 | 80 / 0.1808316963675016 | 77 / 0.1787375191118052 | 1343 |
| train/SMD/machine-1-1/seed2/smd_cf_val | 80 | 80 / 0.1800847916841698 | 80 / 0.1800847916841698 | 1347 |
| train/SMD/machine-1-1/seed3/smd_cf_val | 80 | 80 / 0.1794782367080112 | 80 / 0.1794782367080112 | 1340 |
| train/SMD/machine-1-2/seed0/smd_cf_val | 80 | 80 / 0.2081978031853302 | 78 / 0.2071651626405241 | 1132 |
| train/SMD/machine-1-2/seed1/smd_cf_val | 80 | 80 / 0.2062186616698295 | 68 / 0.2061335805500523 | 1121 |
| train/SMD/machine-1-2/seed2/smd_cf_val | 80 | 80 / 0.2092028845267817 | 70 / 0.2072252232173904 | 1137 |
| train/SMD/machine-1-2/seed3/smd_cf_val | 80 | 80 / 0.2080328051977857 | 77 / 0.2069088564123873 | 1134 |
| train/SMD/machine-1-3/seed0/smd_cf_val | 80 | 80 / 0.790834231304981 | 78 / 0.7852600856105777 | 1126 |
| train/SMD/machine-1-3/seed1/smd_cf_val | 80 | 80 / 0.7963746453471 | 80 / 0.7963746453471 | 1142 |
| train/SMD/machine-1-3/seed2/smd_cf_val | 80 | 80 / 0.7809196622992142 | 76 / 0.7808048390160799 | 1144 |
| train/SMD/machine-1-3/seed3/smd_cf_val | 80 | 80 / 0.7989303330335713 | 76 / 0.7983965923423612 | 1127 |
| train/SMD/machine-1-4/seed0/smd_cf_val | 80 | 80 / 0.8931436573912274 | 75 / 0.8914337585886406 | 1116 |
| train/SMD/machine-1-4/seed1/smd_cf_val | 80 | 80 / 0.892065682360067 | 68 / 0.8831833136242395 | 1116 |
| train/SMD/machine-1-4/seed2/smd_cf_val | 80 | 80 / 0.8951284872996041 | 78 / 0.8942682403959551 | 1117 |
| train/SMD/machine-1-4/seed3/smd_cf_val | 80 | 80 / 0.8923573032967554 | 80 / 0.8923573032967554 | 1138 |
| train/SMD/machine-1-5/seed0/smd_cf_val | 80 | 80 / 0.2175348394466644 | 74 / 0.2162961688718215 | 1160 |
| train/SMD/machine-1-5/seed1/smd_cf_val | 80 | 80 / 0.2200957936960994 | 79 / 0.2173074728314942 | 1157 |
| train/SMD/machine-1-5/seed2/smd_cf_val | 80 | 80 / 0.2218274439272732 | 69 / 0.217389427131089 | 1149 |
| train/SMD/machine-1-5/seed3/smd_cf_val | 80 | 80 / 0.2194472917666314 | 76 / 0.2184433076402579 | 1182 |
| train/SMD/machine-1-6/seed0/smd_cf_val | 80 | 80 / 0.1945659984187797 | 68 / 0.19398237771552 | 1143 |
| train/SMD/machine-1-6/seed1/smd_cf_val | 80 | 80 / 0.1957973498013595 | 80 / 0.1957973498013595 | 1149 |
| train/SMD/machine-1-6/seed2/smd_cf_val | 80 | 80 / 0.1965246188992314 | 77 / 0.1956309118055517 | 1150 |
| train/SMD/machine-1-6/seed3/smd_cf_val | 80 | 80 / 0.1932815073026063 | 79 / 0.1932473242593989 | 1151 |
| train/SMD/machine-1-7/seed0/smd_cf_val | 80 | 80 / 0.0875899535073339 | 73 / 0.0856455676319788 | 1186 |
| train/SMD/machine-1-7/seed1/smd_cf_val | 80 | 80 / 0.0898347607785899 | 70 / 0.0858530168712663 | 1174 |
| train/SMD/machine-1-7/seed2/smd_cf_val | 80 | 80 / 0.0853851209695471 | 73 / 0.0851731757612558 | 1187 |
| train/SMD/machine-1-7/seed3/smd_cf_val | 80 | 80 / 0.0858444264803392 | 77 / 0.0849561873593345 | 1177 |
| train/SMD/machine-1-8/seed0/smd_cf_val | 80 | 80 / 0.1644503063788438 | 72 / 0.1601497967284651 | 1176 |
| train/SMD/machine-1-8/seed1/smd_cf_val | 80 | 80 / 0.1589637344445736 | 78 / 0.1589290874924125 | 1171 |
| train/SMD/machine-1-8/seed2/smd_cf_val | 80 | 80 / 0.1715938314888492 | 78 / 0.160976558317324 | 1199 |
| train/SMD/machine-1-8/seed3/smd_cf_val | 80 | 80 / 0.1689681094421835 | 75 / 0.1620210264941996 | 1160 |
