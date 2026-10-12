# cfval_abl_smdcrs / ks / cfval_abl_smdcrs_ks

- exported: 2026-10-12T17:53:14+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 416 — {'success': 416} — **COMPLETE**
- exported eval jobs: 256, train jobs: 128; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SMD | machine-1-1 | 0 | last | 80 | A_off | 0.5133 | 0.5806 | 0.4956 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_on | 0.4227 | 0.4635 | 0.4011 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.5169 | 0.5819 | 0.4953 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_on | 0.4182 | 0.4545 | 0.3948 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_off | 0.5019 | 0.5733 | 0.4814 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_on | 0.4162 | 0.4495 | 0.3896 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 77 | A_off | 0.5050 | 0.5739 | 0.4867 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 77 | A_on | 0.4112 | 0.4457 | 0.3911 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_off | 0.5166 | 0.5774 | 0.5012 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_on | 0.4772 | 0.5140 | 0.4392 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 78 | A_off | 0.5159 | 0.5773 | 0.5002 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 78 | A_on | 0.4785 | 0.5143 | 0.4439 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_off | 0.5248 | 0.5876 | 0.5061 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_on | 0.4327 | 0.4592 | 0.3948 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 74 | A_off | 0.5258 | 0.5866 | 0.5109 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 74 | A_on | 0.4274 | 0.4515 | 0.3942 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_off | 0.1548 | 0.1650 | 0.2777 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_on | 0.3834 | 0.3935 | 0.4235 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 80 | A_off | 0.1548 | 0.1650 | 0.2777 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 80 | A_on | 0.3834 | 0.3935 | 0.4235 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_off | 0.1357 | 0.1431 | 0.2275 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_on | 0.3348 | 0.3429 | 0.4099 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 80 | A_off | 0.1357 | 0.1431 | 0.2275 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 80 | A_on | 0.3348 | 0.3429 | 0.4099 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_off | 0.1439 | 0.1537 | 0.2491 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_on | 0.3428 | 0.3471 | 0.4199 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 80 | A_off | 0.1439 | 0.1537 | 0.2491 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 80 | A_on | 0.3428 | 0.3471 | 0.4199 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_off | 0.1278 | 0.1342 | 0.2006 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_on | 0.3358 | 0.3598 | 0.4356 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 74 | A_off | 0.1354 | 0.1428 | 0.2313 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 74 | A_on | 0.3457 | 0.3643 | 0.4318 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_off | 0.2316 | 0.2142 | 0.3099 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_on | 0.2047 | 0.1932 | 0.2659 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 78 | A_off | 0.2308 | 0.2129 | 0.3096 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 78 | A_on | 0.2182 | 0.2101 | 0.2841 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_off | 0.2364 | 0.2194 | 0.3099 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_on | 0.2329 | 0.2315 | 0.3078 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 76 | A_off | 0.2384 | 0.2224 | 0.3099 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 76 | A_on | 0.2348 | 0.2356 | 0.3102 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_off | 0.2386 | 0.2238 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_on | 0.2178 | 0.2101 | 0.2923 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 80 | A_off | 0.2386 | 0.2238 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 80 | A_on | 0.2178 | 0.2101 | 0.2923 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_off | 0.2375 | 0.2216 | 0.3096 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_on | 0.2208 | 0.2095 | 0.2940 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 76 | A_off | 0.2377 | 0.2227 | 0.3096 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 76 | A_on | 0.2156 | 0.2022 | 0.2868 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_off | 0.1299 | 0.1151 | 0.1780 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_on | 0.1521 | 0.1472 | 0.2171 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 58 | A_off | 0.1310 | 0.1168 | 0.1781 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 58 | A_on | 0.1524 | 0.1483 | 0.2177 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_off | 0.1284 | 0.1136 | 0.1779 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_on | 0.1535 | 0.1481 | 0.2131 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 79 | A_off | 0.1284 | 0.1137 | 0.1777 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 79 | A_on | 0.1546 | 0.1503 | 0.2114 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_off | 0.1284 | 0.1140 | 0.1777 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_on | 0.1451 | 0.1349 | 0.1912 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 80 | A_off | 0.1284 | 0.1140 | 0.1777 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 80 | A_on | 0.1451 | 0.1349 | 0.1912 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_off | 0.1289 | 0.1142 | 0.1778 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_on | 0.1531 | 0.1489 | 0.2205 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_off | 0.1289 | 0.1142 | 0.1778 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_on | 0.1531 | 0.1489 | 0.2205 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_off | 0.5189 | 0.3748 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_on | 0.5392 | 0.4293 | 0.5600 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 74 | A_off | 0.5206 | 0.3780 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 74 | A_on | 0.5429 | 0.4205 | 0.5556 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_off | 0.5142 | 0.3730 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_on | 0.5283 | 0.4032 | 0.5537 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 79 | A_off | 0.5140 | 0.3730 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 79 | A_on | 0.5288 | 0.4063 | 0.5537 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_off | 0.5183 | 0.3711 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_on | 0.5721 | 0.4750 | 0.5714 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 79 | A_off | 0.5183 | 0.3766 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 79 | A_on | 0.5716 | 0.4696 | 0.5714 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_off | 0.5200 | 0.3689 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_on | 0.5353 | 0.4117 | 0.5556 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 67 | A_off | 0.5200 | 0.3813 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 67 | A_on | 0.5324 | 0.4328 | 0.5618 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_off | 0.8669 | 0.8458 | 0.8484 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_on | 0.7585 | 0.7246 | 0.7054 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 78 | A_off | 0.8641 | 0.8430 | 0.8447 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 78 | A_on | 0.7568 | 0.7246 | 0.6984 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_off | 0.8669 | 0.8458 | 0.8431 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_on | 0.7348 | 0.7120 | 0.6741 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 80 | A_off | 0.8669 | 0.8458 | 0.8431 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 80 | A_on | 0.7348 | 0.7120 | 0.6741 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_off | 0.8657 | 0.8449 | 0.8407 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_on | 0.7561 | 0.7294 | 0.7117 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 77 | A_off | 0.8634 | 0.8427 | 0.8391 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 77 | A_on | 0.7607 | 0.7345 | 0.7197 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_off | 0.8641 | 0.8432 | 0.8431 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_on | 0.7725 | 0.7463 | 0.7391 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 79 | A_off | 0.8643 | 0.8435 | 0.8433 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 79 | A_on | 0.7711 | 0.7420 | 0.7357 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_off | 0.6442 | 0.6531 | 0.7145 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_on | 0.5738 | 0.5824 | 0.6640 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 78 | A_off | 0.6450 | 0.6535 | 0.7140 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 78 | A_on | 0.5658 | 0.5743 | 0.6648 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_off | 0.6426 | 0.6505 | 0.7141 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_on | 0.4999 | 0.5095 | 0.5834 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 62 | A_off | 0.6408 | 0.6488 | 0.7148 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 62 | A_on | 0.5171 | 0.5237 | 0.6011 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_off | 0.6442 | 0.6530 | 0.7143 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_on | 0.5109 | 0.5192 | 0.6174 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 73 | A_off | 0.6431 | 0.6521 | 0.7143 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 73 | A_on | 0.4923 | 0.4968 | 0.5791 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_off | 0.6443 | 0.6526 | 0.7152 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_on | 0.4764 | 0.4790 | 0.5585 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 73 | A_off | 0.6433 | 0.6513 | 0.7135 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 73 | A_on | 0.4854 | 0.4883 | 0.5613 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_off | 0.2575 | 0.2140 | 0.3198 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_on | 0.2042 | 0.1016 | 0.2586 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 77 | A_off | 0.2585 | 0.2134 | 0.3224 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 77 | A_on | 0.2059 | 0.0993 | 0.2651 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_off | 0.2648 | 0.2251 | 0.3281 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_on | 0.2156 | 0.1084 | 0.2638 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 78 | A_off | 0.2656 | 0.2257 | 0.3276 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 78 | A_on | 0.2154 | 0.1102 | 0.2640 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_off | 0.2581 | 0.2127 | 0.3200 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_on | 0.2004 | 0.0993 | 0.2462 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 79 | A_off | 0.2565 | 0.2096 | 0.3182 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 79 | A_on | 0.2004 | 0.1010 | 0.2473 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_off | 0.2625 | 0.2213 | 0.3254 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_on | 0.1894 | 0.0869 | 0.2359 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 75 | A_off | 0.2637 | 0.2209 | 0.3224 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 75 | A_on | 0.1955 | 0.0922 | 0.2423 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_off | 0.5263 | 0.5888 | 0.5120 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_on | 0.4620 | 0.4977 | 0.4189 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.5273 | 0.5878 | 0.5132 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_on | 0.4608 | 0.4968 | 0.4158 | 1.0 | False |
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
| SMD | machine-1-1 | 0 | last | 80 | A_off | 0.5190 | 0.5771 | 0.5023 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_on | 0.4299 | 0.4578 | 0.4154 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 74 | A_off | 0.5179 | 0.5757 | 0.5046 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 74 | A_on | 0.4280 | 0.4554 | 0.4102 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_off | 0.5160 | 0.5788 | 0.5059 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_on | 0.4412 | 0.4602 | 0.4010 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 79 | A_off | 0.5168 | 0.5792 | 0.5065 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 79 | A_on | 0.4405 | 0.4579 | 0.4008 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_off | 0.5467 | 0.5999 | 0.5354 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_on | 0.4575 | 0.4779 | 0.4187 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 74 | A_off | 0.5468 | 0.6007 | 0.5397 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 74 | A_on | 0.4523 | 0.4689 | 0.4181 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_off | 0.5145 | 0.5750 | 0.5001 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_on | 0.4448 | 0.4799 | 0.4141 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 79 | A_off | 0.5148 | 0.5758 | 0.5012 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 79 | A_on | 0.4419 | 0.4747 | 0.4072 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_off | 0.2151 | 0.2378 | 0.3613 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_on | 0.3794 | 0.3986 | 0.4387 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 74 | A_off | 0.2178 | 0.2395 | 0.3625 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 74 | A_on | 0.3607 | 0.3908 | 0.4368 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_off | 0.1799 | 0.1955 | 0.3221 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_on | 0.3347 | 0.3345 | 0.3900 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 72 | A_off | 0.1831 | 0.1998 | 0.3336 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 72 | A_on | 0.3682 | 0.3732 | 0.4084 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_off | 0.2065 | 0.2279 | 0.3580 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_on | 0.3191 | 0.3300 | 0.3673 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 76 | A_off | 0.2110 | 0.2347 | 0.3586 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 76 | A_on | 0.3229 | 0.3362 | 0.3899 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_off | 0.2186 | 0.2408 | 0.3620 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_on | 0.2705 | 0.2974 | 0.3453 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 56 | A_off | 0.2203 | 0.2427 | 0.3620 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 56 | A_on | 0.2915 | 0.3089 | 0.3737 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_off | 0.2351 | 0.2186 | 0.3087 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_on | 0.2398 | 0.2512 | 0.3088 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 79 | A_off | 0.2358 | 0.2193 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 79 | A_on | 0.2432 | 0.2457 | 0.3073 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_off | 0.2371 | 0.2238 | 0.3084 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_on | 0.2100 | 0.2071 | 0.2762 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 80 | A_off | 0.2371 | 0.2238 | 0.3084 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 80 | A_on | 0.2100 | 0.2071 | 0.2762 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_off | 0.2373 | 0.2205 | 0.3087 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_on | 0.2297 | 0.2294 | 0.3022 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 76 | A_off | 0.2370 | 0.2218 | 0.3084 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 76 | A_on | 0.2257 | 0.2239 | 0.2958 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_off | 0.2374 | 0.2236 | 0.3087 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_on | 0.2626 | 0.2699 | 0.3084 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 77 | A_off | 0.2373 | 0.2225 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 77 | A_on | 0.2289 | 0.2257 | 0.2865 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_off | 0.1304 | 0.1168 | 0.1782 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_on | 0.1672 | 0.1738 | 0.2558 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 79 | A_off | 0.1305 | 0.1170 | 0.1782 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 79 | A_on | 0.1551 | 0.1545 | 0.2260 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_off | 0.1306 | 0.1172 | 0.1782 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_on | 0.1582 | 0.1591 | 0.2310 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 75 | A_off | 0.1316 | 0.1185 | 0.1782 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 75 | A_on | 0.1608 | 0.1642 | 0.2288 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_off | 0.1307 | 0.1174 | 0.1782 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_on | 0.1721 | 0.1799 | 0.2493 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 47 | A_off | 0.1314 | 0.1186 | 0.1781 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 47 | A_on | 0.1731 | 0.1805 | 0.2675 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_off | 0.1302 | 0.1167 | 0.1781 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_on | 0.1589 | 0.1577 | 0.2286 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_off | 0.1302 | 0.1167 | 0.1781 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_on | 0.1589 | 0.1577 | 0.2286 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_off | 0.5141 | 0.3717 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_on | 0.5119 | 0.3692 | 0.5517 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 79 | A_off | 0.5131 | 0.3703 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 79 | A_on | 0.5121 | 0.3692 | 0.5506 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_off | 0.5136 | 0.3739 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_on | 0.5198 | 0.3842 | 0.5478 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 54 | A_off | 0.5112 | 0.3707 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 54 | A_on | 0.5200 | 0.3830 | 0.5682 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_off | 0.5174 | 0.3769 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_on | 0.5209 | 0.4125 | 0.5600 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 49 | A_off | 0.5137 | 0.3733 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 49 | A_on | 0.5173 | 0.3968 | 0.5587 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_off | 0.5203 | 0.3841 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_on | 0.5224 | 0.3899 | 0.5443 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 58 | A_off | 0.5158 | 0.3728 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 58 | A_on | 0.5190 | 0.3830 | 0.5556 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_off | 0.8669 | 0.8458 | 0.8478 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_on | 0.7422 | 0.6987 | 0.7051 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 79 | A_off | 0.8648 | 0.8436 | 0.8455 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 79 | A_on | 0.7473 | 0.7034 | 0.7047 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_off | 0.8685 | 0.8474 | 0.8494 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_on | 0.7518 | 0.7003 | 0.7116 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 77 | A_off | 0.8650 | 0.8440 | 0.8412 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 77 | A_on | 0.7704 | 0.7190 | 0.7223 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_off | 0.8702 | 0.8489 | 0.8540 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_on | 0.7150 | 0.6341 | 0.6590 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 50 | A_off | 0.8706 | 0.8492 | 0.8533 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 50 | A_on | 0.7688 | 0.6680 | 0.7308 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_off | 0.8681 | 0.8469 | 0.8527 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_on | 0.7971 | 0.7563 | 0.7443 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 71 | A_off | 0.8675 | 0.8464 | 0.8510 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 71 | A_on | 0.7815 | 0.7382 | 0.7204 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_off | 0.6407 | 0.6519 | 0.7158 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_on | 0.4798 | 0.4900 | 0.5377 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 14 | A_off | 0.6496 | 0.6604 | 0.7167 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 14 | A_on | 0.4479 | 0.4569 | 0.4826 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_off | 0.6442 | 0.6550 | 0.7155 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_on | 0.4172 | 0.4231 | 0.4769 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 37 | A_off | 0.6426 | 0.6531 | 0.7163 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 37 | A_on | 0.3954 | 0.4051 | 0.4194 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_off | 0.6507 | 0.6609 | 0.7165 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_on | 0.4854 | 0.4938 | 0.5456 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 35 | A_off | 0.6585 | 0.6699 | 0.7182 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 35 | A_on | 0.4838 | 0.4942 | 0.5420 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_off | 0.6434 | 0.6543 | 0.7161 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_on | 0.6539 | 0.6627 | 0.6896 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 72 | A_off | 0.6692 | 0.6793 | 0.7175 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 72 | A_on | 0.6695 | 0.6784 | 0.7037 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_off | 0.2572 | 0.2079 | 0.3178 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_on | 0.2089 | 0.1023 | 0.2678 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 77 | A_off | 0.2565 | 0.2048 | 0.3122 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 77 | A_on | 0.2054 | 0.1015 | 0.2630 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_off | 0.2553 | 0.2080 | 0.3174 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_on | 0.2160 | 0.1214 | 0.2619 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 80 | A_off | 0.2553 | 0.2080 | 0.3174 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 80 | A_on | 0.2160 | 0.1214 | 0.2619 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_off | 0.2532 | 0.2053 | 0.3179 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_on | 0.2077 | 0.1154 | 0.2592 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 75 | A_off | 0.2530 | 0.2018 | 0.3188 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 75 | A_on | 0.2093 | 0.1129 | 0.2654 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_off | 0.2530 | 0.2049 | 0.3172 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_on | 0.2101 | 0.1101 | 0.2646 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 77 | A_off | 0.2524 | 0.2038 | 0.3212 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 77 | A_on | 0.2028 | 0.1073 | 0.2482 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_off | 0.5650 | 0.6161 | 0.5608 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_on | 0.7184 | 0.8141 | 0.6674 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.5622 | 0.6134 | 0.5597 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_on | 0.7096 | 0.8027 | 0.6544 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_off | 0.6148 | 0.6669 | 0.5700 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_on | 0.6002 | 0.6855 | 0.5284 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 79 | A_off | 0.6057 | 0.6602 | 0.5660 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 79 | A_on | 0.5692 | 0.6589 | 0.4982 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_off | 0.5747 | 0.6140 | 0.5485 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_on | 0.5797 | 0.6625 | 0.5313 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 79 | A_off | 0.5741 | 0.6155 | 0.5465 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 79 | A_on | 0.5693 | 0.6315 | 0.5093 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_off | 0.6119 | 0.6540 | 0.5989 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_on | 0.7473 | 0.7963 | 0.7027 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 77 | A_off | 0.5998 | 0.6423 | 0.5928 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 77 | A_on | 0.7361 | 0.7864 | 0.6828 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_off | 0.2273 | 0.2473 | 0.3681 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_on | 0.2637 | 0.2818 | 0.3918 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 77 | A_off | 0.2270 | 0.2459 | 0.3667 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 77 | A_on | 0.2601 | 0.2771 | 0.3809 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_off | 0.2297 | 0.2475 | 0.3695 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_on | 0.2895 | 0.3051 | 0.3955 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 50 | A_off | 0.2268 | 0.2443 | 0.3593 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 50 | A_on | 0.2962 | 0.3010 | 0.3754 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_off | 0.2301 | 0.2525 | 0.3695 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_on | 0.2522 | 0.2552 | 0.3759 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 78 | A_off | 0.2337 | 0.2559 | 0.3713 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 78 | A_on | 0.2767 | 0.2779 | 0.3902 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_off | 0.2473 | 0.2678 | 0.3774 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_on | 0.3452 | 0.3365 | 0.3956 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 77 | A_off | 0.2490 | 0.2705 | 0.3770 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 77 | A_on | 0.3316 | 0.3217 | 0.3853 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_off | 0.2345 | 0.2195 | 0.3049 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_on | 0.1663 | 0.1639 | 0.1987 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 71 | A_off | 0.2375 | 0.2255 | 0.3081 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 71 | A_on | 0.2349 | 0.2489 | 0.2981 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_off | 0.2457 | 0.2434 | 0.3078 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_on | 0.2407 | 0.2555 | 0.2963 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 78 | A_off | 0.2468 | 0.2431 | 0.3078 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 78 | A_on | 0.2459 | 0.2731 | 0.2983 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_off | 0.2542 | 0.2497 | 0.3068 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_on | 0.1934 | 0.1988 | 0.2771 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 14 | A_off | 0.2345 | 0.2197 | 0.3081 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 14 | A_on | 0.3491 | 0.3857 | 0.3799 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_off | 0.2460 | 0.2427 | 0.3078 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_on | 0.1748 | 0.1504 | 0.2633 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 80 | A_off | 0.2460 | 0.2427 | 0.3078 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 80 | A_on | 0.1748 | 0.1504 | 0.2633 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_off | 0.1425 | 0.1320 | 0.1808 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_on | 0.1156 | 0.0961 | 0.1896 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 80 | A_off | 0.1425 | 0.1320 | 0.1808 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 80 | A_on | 0.1156 | 0.0961 | 0.1896 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_off | 0.1404 | 0.1299 | 0.1838 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_on | 0.1200 | 0.1024 | 0.1724 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 60 | A_off | 0.1405 | 0.1308 | 0.1895 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 60 | A_on | 0.1166 | 0.0973 | 0.1664 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_off | 0.1462 | 0.1382 | 0.1944 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_on | 0.1276 | 0.1156 | 0.1779 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 56 | A_off | 0.1449 | 0.1371 | 0.1940 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 56 | A_on | 0.1267 | 0.1140 | 0.1878 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_off | 0.1423 | 0.1327 | 0.1803 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_on | 0.1238 | 0.1051 | 0.1846 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 13 | A_off | 0.1338 | 0.1206 | 0.1782 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 13 | A_on | 0.1799 | 0.1860 | 0.2551 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_off | 0.5203 | 0.3817 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_on | 0.5395 | 0.4234 | 0.5486 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 66 | A_off | 0.5185 | 0.3813 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 66 | A_on | 0.5327 | 0.4166 | 0.5465 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_off | 0.5189 | 0.3777 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_on | 0.5282 | 0.3854 | 0.5393 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 71 | A_off | 0.5173 | 0.3745 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 71 | A_on | 0.5229 | 0.3845 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_off | 0.5240 | 0.3847 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_on | 0.5342 | 0.4010 | 0.5476 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 40 | A_off | 0.5133 | 0.3719 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 40 | A_on | 0.5219 | 0.3801 | 0.5581 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_off | 0.5247 | 0.3880 | 0.5393 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_on | 0.5395 | 0.4315 | 0.5465 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 62 | A_off | 0.5235 | 0.3817 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 62 | A_on | 0.5362 | 0.4261 | 0.5537 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_off | 0.8656 | 0.8439 | 0.8550 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_on | 0.8439 | 0.8023 | 0.7858 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 80 | A_off | 0.8656 | 0.8439 | 0.8550 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 80 | A_on | 0.8439 | 0.8023 | 0.7858 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_off | 0.8702 | 0.8483 | 0.8653 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_on | 0.8686 | 0.8355 | 0.8364 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 18 | A_off | 0.8643 | 0.8428 | 0.8480 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 18 | A_on | 0.7434 | 0.6589 | 0.6554 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_off | 0.8574 | 0.8345 | 0.8404 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_on | 0.7536 | 0.6138 | 0.6870 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 75 | A_off | 0.8584 | 0.8354 | 0.8417 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 75 | A_on | 0.7968 | 0.6814 | 0.7339 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_off | 0.8661 | 0.8435 | 0.8525 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_on | 0.8334 | 0.7730 | 0.7566 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 62 | A_off | 0.8650 | 0.8420 | 0.8534 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 62 | A_on | 0.8270 | 0.7731 | 0.7633 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_off | 0.6493 | 0.6614 | 0.7061 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_on | 0.2615 | 0.2637 | 0.3152 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 68 | A_off | 0.6456 | 0.6578 | 0.7036 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 68 | A_on | 0.2468 | 0.2457 | 0.3187 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_off | 0.6580 | 0.6720 | 0.7107 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_on | 0.2701 | 0.2694 | 0.3587 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 74 | A_off | 0.6498 | 0.6633 | 0.7132 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 74 | A_on | 0.2910 | 0.2937 | 0.3667 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_off | 0.6458 | 0.6590 | 0.7134 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_on | 0.3447 | 0.3578 | 0.3849 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 75 | A_off | 0.6456 | 0.6584 | 0.7143 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 75 | A_on | 0.3350 | 0.3482 | 0.3659 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_off | 0.5861 | 0.5933 | 0.6914 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_on | 0.2445 | 0.2482 | 0.3621 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 12 | A_off | 0.6365 | 0.6470 | 0.7157 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 12 | A_on | 0.4261 | 0.4344 | 0.4564 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_off | 0.2329 | 0.1583 | 0.2862 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_on | 0.1841 | 0.0976 | 0.2277 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 80 | A_off | 0.2329 | 0.1583 | 0.2862 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 80 | A_on | 0.1841 | 0.0976 | 0.2277 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_off | 0.2399 | 0.1648 | 0.2860 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_on | 0.1635 | 0.0892 | 0.2093 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 80 | A_off | 0.2399 | 0.1648 | 0.2860 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 80 | A_on | 0.1635 | 0.0892 | 0.2093 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_off | 0.2409 | 0.1621 | 0.2833 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_on | 0.1351 | 0.0853 | 0.2198 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 76 | A_off | 0.2423 | 0.1636 | 0.2852 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 76 | A_on | 0.1428 | 0.0930 | 0.2276 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_off | 0.2348 | 0.1620 | 0.2894 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_on | 0.1784 | 0.0998 | 0.1913 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 80 | A_off | 0.2348 | 0.1620 | 0.2894 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 80 | A_on | 0.1784 | 0.0998 | 0.1913 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SMD/machine-1-1/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1790444891808013 | 79 / 0.1787272637391705 | 1358 |
| train/SMD/machine-1-1/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1805390526397491 | 77 / 0.17844519029525 | 1358 |
| train/SMD/machine-1-1/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1793633020290552 | 78 / 0.1791173052637959 | 1335 |
| train/SMD/machine-1-1/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.180595420614352 | 74 / 0.1800676367907813 | 1335 |
| train/SMD/machine-1-2/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2036088402920972 | 80 / 0.2036088402920972 | 1121 |
| train/SMD/machine-1-2/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2045126315947036 | 80 / 0.2045126315947036 | 1099 |
| train/SMD/machine-1-2/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2034779423957435 | 80 / 0.2034779423957435 | 1140 |
| train/SMD/machine-1-2/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2065824120490665 | 74 / 0.2058792798500829 | 1139 |
| train/SMD/machine-1-3/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.7834812851757619 | 78 / 0.7821630869967491 | 1149 |
| train/SMD/machine-1-3/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.7796309234677196 | 76 / 0.7735972822970378 | 1128 |
| train/SMD/machine-1-3/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.7893697508231072 | 80 / 0.7893697508231072 | 1148 |
| train/SMD/machine-1-3/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.7824195454667527 | 76 / 0.7819332279016517 | 1106 |
| train/SMD/machine-1-4/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.906540254386776 | 58 / 0.9035320510249888 | 1194 |
| train/SMD/machine-1-4/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.8771606484686516 | 79 / 0.8756008719286312 | 1153 |
| train/SMD/machine-1-4/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.8939617679876147 | 80 / 0.8939617679876147 | 1172 |
| train/SMD/machine-1-4/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.8815870013913528 | 80 / 0.8815870013913528 | 1152 |
| train/SMD/machine-1-5/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2131211897357055 | 74 / 0.2110799029187735 | 1164 |
| train/SMD/machine-1-5/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2264937940386153 | 79 / 0.2237947517195094 | 1087 |
| train/SMD/machine-1-5/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2191958401335427 | 79 / 0.2124537010445747 | 1182 |
| train/SMD/machine-1-5/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2182929199425124 | 67 / 0.2169138905034347 | 1183 |
| train/SMD/machine-1-6/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1932325863182518 | 78 / 0.1920177543227381 | 1138 |
| train/SMD/machine-1-6/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1933022688745204 | 80 / 0.1933022688745204 | 1138 |
| train/SMD/machine-1-6/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1962149142714831 | 77 / 0.1948261217893677 | 1138 |
| train/SMD/machine-1-6/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.192989531203482 | 79 / 0.1920573000446138 | 1157 |
| train/SMD/machine-1-7/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.0875676521088186 | 78 / 0.0849168693633316 | 1196 |
| train/SMD/machine-1-7/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.088717833039651 | 62 / 0.0851933380089599 | 1160 |
| train/SMD/machine-1-7/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.0848525096009991 | 73 / 0.0836487291810827 | 1158 |
| train/SMD/machine-1-7/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.0855537133552718 | 73 / 0.0848160104145658 | 1176 |
| train/SMD/machine-1-8/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1574179650806524 | 77 / 0.1559832467829029 | 1178 |
| train/SMD/machine-1-8/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1563098204147963 | 78 / 0.1557981854378212 | 1177 |
| train/SMD/machine-1-8/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1669627111773357 | 79 / 0.1612100969450864 | 1177 |
| train/SMD/machine-1-8/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1672917981493581 | 75 / 0.1553594193309335 | 1071 |
| train/SMD/machine-1-1/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.179562969143687 | 79 / 0.1783938993104982 | 1402 |
| train/SMD/machine-1-1/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1808316963675016 | 77 / 0.1787375191118052 | 1403 |
| train/SMD/machine-1-1/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1800847916841698 | 80 / 0.1800847916841698 | 1403 |
| train/SMD/machine-1-1/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1794782367080112 | 80 / 0.1794782367080112 | 1384 |
| train/SMD/machine-1-2/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.2081978031853302 | 78 / 0.2071651626405241 | 1180 |
| train/SMD/machine-1-2/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.2062186616698295 | 68 / 0.2061335805500523 | 1178 |
| train/SMD/machine-1-2/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.2092028845267817 | 70 / 0.2072252232173904 | 1178 |
| train/SMD/machine-1-2/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.2080328051977857 | 77 / 0.2069088564123873 | 1211 |
| train/SMD/machine-1-3/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.790834231304981 | 78 / 0.7852600856105777 | 1172 |
| train/SMD/machine-1-3/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.7963746453471 | 80 / 0.7963746453471 | 1186 |
| train/SMD/machine-1-3/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.7809196622992142 | 76 / 0.7808048390160799 | 1169 |
| train/SMD/machine-1-3/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.7989303330335713 | 76 / 0.7983965923423612 | 1170 |
| train/SMD/machine-1-4/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.8931436573912274 | 75 / 0.8914337585886406 | 1180 |
| train/SMD/machine-1-4/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.892065682360067 | 68 / 0.8831833136242395 | 1179 |
| train/SMD/machine-1-4/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.8951284872996041 | 78 / 0.8942682403959551 | 1179 |
| train/SMD/machine-1-4/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.8923573032967554 | 80 / 0.8923573032967554 | 1178 |
| train/SMD/machine-1-5/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.2175348394466644 | 74 / 0.2162961688718215 | 1171 |
| train/SMD/machine-1-5/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.2200957936960994 | 79 / 0.2173074728314942 | 1184 |
| train/SMD/machine-1-5/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.2218274439272732 | 69 / 0.217389427131089 | 1199 |
| train/SMD/machine-1-5/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.2194472917666314 | 76 / 0.2184433076402579 | 1185 |
| train/SMD/machine-1-6/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1945659984187797 | 68 / 0.19398237771552 | 1147 |
| train/SMD/machine-1-6/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1957973498013595 | 80 / 0.1957973498013595 | 1146 |
| train/SMD/machine-1-6/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1965246188992314 | 77 / 0.1956309118055517 | 1160 |
| train/SMD/machine-1-6/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1932815073026063 | 79 / 0.1932473242593989 | 1145 |
| train/SMD/machine-1-7/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.0875899535073339 | 73 / 0.0856455676319788 | 1205 |
| train/SMD/machine-1-7/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.0898347607785899 | 70 / 0.0858530168712663 | 1176 |
| train/SMD/machine-1-7/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.0853851209695471 | 73 / 0.0851731757612558 | 1176 |
| train/SMD/machine-1-7/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.0858444264803392 | 77 / 0.0849561873593345 | 1175 |
| train/SMD/machine-1-8/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1644503063788438 | 72 / 0.1601497967284651 | 1173 |
| train/SMD/machine-1-8/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1589637344445736 | 78 / 0.1589290874924125 | 1188 |
| train/SMD/machine-1-8/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1715938314888492 | 78 / 0.160976558317324 | 1187 |
| train/SMD/machine-1-8/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1689681094421835 | 75 / 0.1620210264941996 | 1201 |
| train/SMD/machine-1-1/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1869175430736609 | 74 / 0.1849117445863878 | 2828 |
| train/SMD/machine-1-1/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1828569899761286 | 79 / 0.1826926124033804 | 2852 |
| train/SMD/machine-1-1/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1889559705974549 | 74 / 0.1863692623439676 | 2852 |
| train/SMD/machine-1-1/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1838418890086961 | 79 / 0.1827303634775874 | 2935 |
| train/SMD/machine-1-2/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.264797648999401 | 74 / 0.2583179328284301 | 2405 |
| train/SMD/machine-1-2/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2523466428368537 | 72 / 0.246351139471424 | 2455 |
| train/SMD/machine-1-2/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2452747066943919 | 76 / 0.2326882621822015 | 2416 |
| train/SMD/machine-1-2/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2565900392363622 | 56 / 0.2562252280257681 | 2455 |
| train/SMD/machine-1-3/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.816087327745452 | 79 / 0.8084603715241854 | 2392 |
| train/SMD/machine-1-3/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.8027526219240275 | 80 / 0.8027526219240275 | 2476 |
| train/SMD/machine-1-3/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.8205002030173151 | 76 / 0.810831253511275 | 2415 |
| train/SMD/machine-1-3/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.836238398723443 | 77 / 0.8255382837835066 | 2390 |
| train/SMD/machine-1-4/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.9328545802332314 | 79 / 0.9327288304867892 | 2426 |
| train/SMD/machine-1-4/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.930425688131809 | 75 / 0.926366053256784 | 2425 |
| train/SMD/machine-1-4/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.9863725931994372 | 47 / 0.984157068892646 | 2436 |
| train/SMD/machine-1-4/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.9733652226116732 | 80 / 0.9733652226116732 | 2461 |
| train/SMD/machine-1-5/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2315880188702444 | 79 / 0.2238203920110739 | 2437 |
| train/SMD/machine-1-5/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2308978062802088 | 54 / 0.2135895103960003 | 2448 |
| train/SMD/machine-1-5/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2274919949366209 | 49 / 0.2141085604031951 | 2436 |
| train/SMD/machine-1-5/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2438920351111518 | 58 / 0.2142261705900493 | 2425 |
| train/SMD/machine-1-6/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2010669921592414 | 79 / 0.2006710241121412 | 2372 |
| train/SMD/machine-1-6/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2044211515203381 | 77 / 0.1981035465138117 | 2360 |
| train/SMD/machine-1-6/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2067843130653239 | 50 / 0.2061165299959925 | 2392 |
| train/SMD/machine-1-6/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2059554876245638 | 71 / 0.1993506979121597 | 2402 |
| train/SMD/machine-1-7/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2203570243552753 | 14 / 0.1802851799930629 | 2354 |
| train/SMD/machine-1-7/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2248261948030836 | 37 / 0.1801132166493094 | 2383 |
| train/SMD/machine-1-7/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2959724810837877 | 35 / 0.1779127987523862 | 2413 |
| train/SMD/machine-1-7/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1734381139510543 | 72 / 0.1686211877714424 | 2363 |
| train/SMD/machine-1-8/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1656497223311528 | 77 / 0.1642432313248188 | 2446 |
| train/SMD/machine-1-8/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.166789376942174 | 80 / 0.166789376942174 | 2474 |
| train/SMD/machine-1-8/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1693704577496707 | 75 / 0.1672163830073584 | 2416 |
| train/SMD/machine-1-8/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1762857486255618 | 77 / 0.167257029655151 | 2415 |
| train/SMD/machine-1-1/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2510928633004463 | 79 / 0.2427272152863406 | 2869 |
| train/SMD/machine-1-1/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2253622453441088 | 79 / 0.2226599039583999 | 2832 |
| train/SMD/machine-1-1/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2316359247173732 | 79 / 0.225518545091605 | 2868 |
| train/SMD/machine-1-1/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.25070539966995 | 77 / 0.2477635589983998 | 2922 |
| train/SMD/machine-1-2/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2885943847330258 | 77 / 0.2873722947849584 | 2438 |
| train/SMD/machine-1-2/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2986216024600638 | 50 / 0.2827649646358759 | 2438 |
| train/SMD/machine-1-2/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.279774796505108 | 78 / 0.2730661798215912 | 2421 |
| train/SMD/machine-1-2/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2706956319447101 | 77 / 0.2697804625126919 | 2449 |
| train/SMD/machine-1-3/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.8695921543797246 | 71 / 0.8690130832584145 | 2424 |
| train/SMD/machine-1-3/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.9084004264439164 | 78 / 0.9061718328473172 | 2510 |
| train/SMD/machine-1-3/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.9255676429097623 | 14 / 0.903192530390346 | 2414 |
| train/SMD/machine-1-3/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.9030405159201556 | 80 / 0.9030405159201556 | 2439 |
| train/SMD/machine-1-4/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.9670572784514796 | 80 / 0.9670572784514796 | 2407 |
| train/SMD/machine-1-4/seed1/smd_cf_val_perm2_crson | 80 | 80 / 1.0099624326264418 | 60 / 0.990817630450624 | 2435 |
| train/SMD/machine-1-4/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.9932927109886808 | 56 / 0.9915677068199228 | 2406 |
| train/SMD/machine-1-4/seed3/smd_cf_val_perm2_crson | 80 | 80 / 1.044883927952306 | 13 / 1.0439795733251285 | 2458 |
| train/SMD/machine-1-5/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2369242279206157 | 66 / 0.235876775559048 | 2448 |
| train/SMD/machine-1-5/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2584512164681101 | 71 / 0.2499159018531009 | 2427 |
| train/SMD/machine-1-5/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2404285082482101 | 40 / 0.234606695380951 | 2448 |
| train/SMD/machine-1-5/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2471501372083998 | 62 / 0.2361554468569607 | 2413 |
| train/SMD/machine-1-6/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2273080111720115 | 80 / 0.2273080111720115 | 2423 |
| train/SMD/machine-1-6/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2575081475218782 | 18 / 0.2403234350686744 | 2410 |
| train/SMD/machine-1-6/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2335932974549966 | 75 / 0.2334413864798562 | 2384 |
| train/SMD/machine-1-6/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2350748891741605 | 62 / 0.2278102437418528 | 2371 |
| train/SMD/machine-1-7/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1782310715901701 | 68 / 0.1717419675370935 | 2356 |
| train/SMD/machine-1-7/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1813312235512059 | 74 / 0.1558781453310163 | 2408 |
| train/SMD/machine-1-7/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.147298963085568 | 75 / 0.1413798025642073 | 2414 |
| train/SMD/machine-1-7/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2486659400492551 | 12 / 0.2166702720444287 | 2395 |
| train/SMD/machine-1-8/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1920471792326421 | 80 / 0.1920471792326421 | 2400 |
| train/SMD/machine-1-8/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1976219883157543 | 80 / 0.1976219883157543 | 2430 |
| train/SMD/machine-1-8/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1952522952678963 | 76 / 0.1943485799097967 | 2441 |
| train/SMD/machine-1-8/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.193446247007594 | 80 / 0.193446247007594 | 2381 |
