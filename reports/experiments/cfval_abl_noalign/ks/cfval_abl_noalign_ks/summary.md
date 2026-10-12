# cfval_abl_noalign / ks / cfval_abl_noalign_ks

- exported: 2026-10-12T17:54:37+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 117 — {'success': 117} — **COMPLETE**
- exported eval jobs: 72, train jobs: 36; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| PSM | PSM | 0 | last | 80 | A_off | 0.4430 | 0.4270 | 0.4371 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_on | 0.5330 | 0.4937 | 0.4810 | 1.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_off | 0.4430 | 0.4270 | 0.4371 | 1.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_on | 0.5330 | 0.4937 | 0.4810 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_off | 0.4437 | 0.4298 | 0.4378 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_on | 0.5352 | 0.4904 | 0.4788 | 1.0 | False |
| PSM | PSM | 1 | best_val | 80 | A_off | 0.4437 | 0.4298 | 0.4378 | 1.0 | False |
| PSM | PSM | 1 | best_val | 80 | A_on | 0.5352 | 0.4904 | 0.4788 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_off | 0.4225 | 0.4115 | 0.4432 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_on | 0.5387 | 0.4926 | 0.4803 | 1.0 | False |
| PSM | PSM | 2 | best_val | 74 | A_off | 0.4234 | 0.4120 | 0.4443 | 1.0 | False |
| PSM | PSM | 2 | best_val | 74 | A_on | 0.5396 | 0.4933 | 0.4817 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_off | 0.4410 | 0.4282 | 0.4482 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_on | 0.5415 | 0.4958 | 0.4828 | 1.0 | False |
| PSM | PSM | 3 | best_val | 79 | A_off | 0.4404 | 0.4276 | 0.4477 | 1.0 | False |
| PSM | PSM | 3 | best_val | 79 | A_on | 0.5408 | 0.4951 | 0.4816 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_off | 0.4908 | 0.5600 | 0.4767 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_on | 0.4840 | 0.5064 | 0.4693 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 78 | A_off | 0.4940 | 0.5602 | 0.4794 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 78 | A_on | 0.4820 | 0.5053 | 0.4668 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_off | 0.4954 | 0.5661 | 0.4801 | 1.0 | False |
| SMD | machine-1-1 | 1 | last | 80 | A_on | 0.4833 | 0.5026 | 0.4634 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 77 | A_off | 0.5011 | 0.5694 | 0.4841 | 1.0 | False |
| SMD | machine-1-1 | 1 | best_val | 77 | A_on | 0.4769 | 0.4944 | 0.4567 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_off | 0.5225 | 0.5818 | 0.5130 | 1.0 | False |
| SMD | machine-1-1 | 2 | last | 80 | A_on | 0.4734 | 0.5114 | 0.4435 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 78 | A_off | 0.5239 | 0.5838 | 0.5137 | 1.0 | False |
| SMD | machine-1-1 | 2 | best_val | 78 | A_on | 0.4732 | 0.5100 | 0.4427 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_off | 0.5207 | 0.5821 | 0.5044 | 1.0 | False |
| SMD | machine-1-1 | 3 | last | 80 | A_on | 0.4613 | 0.5017 | 0.4305 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 79 | A_off | 0.5236 | 0.5835 | 0.5091 | 1.0 | False |
| SMD | machine-1-1 | 3 | best_val | 79 | A_on | 0.4531 | 0.4940 | 0.4166 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_off | 0.1589 | 0.1699 | 0.2827 | 1.0 | False |
| SMD | machine-1-2 | 0 | last | 80 | A_on | 0.2988 | 0.3180 | 0.3936 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 78 | A_off | 0.1619 | 0.1724 | 0.2855 | 1.0 | False |
| SMD | machine-1-2 | 0 | best_val | 78 | A_on | 0.3026 | 0.3248 | 0.4017 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_off | 0.1440 | 0.1527 | 0.2441 | 1.0 | False |
| SMD | machine-1-2 | 1 | last | 80 | A_on | 0.3242 | 0.3363 | 0.3986 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 80 | A_off | 0.1440 | 0.1527 | 0.2441 | 1.0 | False |
| SMD | machine-1-2 | 1 | best_val | 80 | A_on | 0.3242 | 0.3363 | 0.3986 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_off | 0.1434 | 0.1523 | 0.2513 | 1.0 | False |
| SMD | machine-1-2 | 2 | last | 80 | A_on | 0.3571 | 0.3803 | 0.4204 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 80 | A_off | 0.1434 | 0.1523 | 0.2513 | 1.0 | False |
| SMD | machine-1-2 | 2 | best_val | 80 | A_on | 0.3571 | 0.3803 | 0.4204 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_off | 0.1236 | 0.1293 | 0.1811 | 1.0 | False |
| SMD | machine-1-2 | 3 | last | 80 | A_on | 0.3480 | 0.3639 | 0.4159 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 77 | A_off | 0.1276 | 0.1331 | 0.2001 | 1.0 | False |
| SMD | machine-1-2 | 3 | best_val | 77 | A_on | 0.3527 | 0.3678 | 0.4295 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_off | 0.2400 | 0.2314 | 0.3084 | 1.0 | False |
| SMD | machine-1-3 | 0 | last | 80 | A_on | 0.2806 | 0.2757 | 0.3626 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 69 | A_off | 0.2383 | 0.2294 | 0.3084 | 1.0 | False |
| SMD | machine-1-3 | 0 | best_val | 69 | A_on | 0.2844 | 0.2876 | 0.3582 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_off | 0.2347 | 0.2169 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 1 | last | 80 | A_on | 0.2203 | 0.2206 | 0.3128 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 80 | A_off | 0.2347 | 0.2169 | 0.3090 | 1.0 | False |
| SMD | machine-1-3 | 1 | best_val | 80 | A_on | 0.2203 | 0.2206 | 0.3128 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_off | 0.2339 | 0.2164 | 0.3081 | 1.0 | False |
| SMD | machine-1-3 | 2 | last | 80 | A_on | 0.3160 | 0.3372 | 0.3660 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 29 | A_off | 0.2362 | 0.2220 | 0.3087 | 1.0 | False |
| SMD | machine-1-3 | 2 | best_val | 29 | A_on | 0.2067 | 0.2003 | 0.2703 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_off | 0.2358 | 0.2265 | 0.3087 | 1.0 | False |
| SMD | machine-1-3 | 3 | last | 80 | A_on | 0.2589 | 0.2640 | 0.3216 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 80 | A_off | 0.2358 | 0.2265 | 0.3087 | 1.0 | False |
| SMD | machine-1-3 | 3 | best_val | 80 | A_on | 0.2589 | 0.2640 | 0.3216 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_off | 0.1291 | 0.1146 | 0.1778 | 1.0 | False |
| SMD | machine-1-4 | 0 | last | 80 | A_on | 0.1312 | 0.1179 | 0.1858 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 80 | A_off | 0.1291 | 0.1146 | 0.1778 | 1.0 | False |
| SMD | machine-1-4 | 0 | best_val | 80 | A_on | 0.1312 | 0.1179 | 0.1858 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_off | 0.1279 | 0.1127 | 0.1773 | 1.0 | False |
| SMD | machine-1-4 | 1 | last | 80 | A_on | 0.1382 | 0.1280 | 0.1988 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 79 | A_off | 0.1281 | 0.1130 | 0.1772 | 1.0 | False |
| SMD | machine-1-4 | 1 | best_val | 79 | A_on | 0.1391 | 0.1288 | 0.1965 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_off | 0.1297 | 0.1154 | 0.1774 | 1.0 | False |
| SMD | machine-1-4 | 2 | last | 80 | A_on | 0.1334 | 0.1267 | 0.2047 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 75 | A_off | 0.1301 | 0.1159 | 0.1774 | 1.0 | False |
| SMD | machine-1-4 | 2 | best_val | 75 | A_on | 0.1350 | 0.1287 | 0.2029 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_off | 0.1305 | 0.1161 | 0.1777 | 1.0 | False |
| SMD | machine-1-4 | 3 | last | 80 | A_on | 0.1354 | 0.1259 | 0.1915 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_off | 0.1305 | 0.1161 | 0.1777 | 1.0 | False |
| SMD | machine-1-4 | 3 | best_val | 80 | A_on | 0.1354 | 0.1259 | 0.1915 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_off | 0.5255 | 0.3898 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 0 | last | 80 | A_on | 0.5654 | 0.4363 | 0.5696 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 61 | A_off | 0.5237 | 0.3871 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 0 | best_val | 61 | A_on | 0.5669 | 0.4393 | 0.5783 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_off | 0.5136 | 0.3727 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 1 | last | 80 | A_on | 0.5268 | 0.3996 | 0.5465 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 73 | A_off | 0.5128 | 0.3724 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 1 | best_val | 73 | A_on | 0.5279 | 0.3995 | 0.5517 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_off | 0.5312 | 0.3851 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | last | 80 | A_on | 0.5880 | 0.4768 | 0.6029 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 69 | A_off | 0.5310 | 0.3903 | 0.5385 | 1.0 | False |
| SMD | machine-1-5 | 2 | best_val | 69 | A_on | 0.5912 | 0.5020 | 0.6124 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_off | 0.5131 | 0.3721 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 3 | last | 80 | A_on | 0.5287 | 0.4009 | 0.5568 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 80 | A_off | 0.5131 | 0.3721 | 0.5412 | 1.0 | False |
| SMD | machine-1-5 | 3 | best_val | 80 | A_on | 0.5287 | 0.4009 | 0.5568 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_off | 0.8695 | 0.8483 | 0.8505 | 1.0 | False |
| SMD | machine-1-6 | 0 | last | 80 | A_on | 0.6902 | 0.6437 | 0.6174 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 78 | A_off | 0.8649 | 0.8436 | 0.8450 | 1.0 | False |
| SMD | machine-1-6 | 0 | best_val | 78 | A_on | 0.6860 | 0.6386 | 0.6079 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_off | 0.8631 | 0.8411 | 0.8436 | 1.0 | False |
| SMD | machine-1-6 | 1 | last | 80 | A_on | 0.7824 | 0.7370 | 0.7296 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 80 | A_off | 0.8631 | 0.8411 | 0.8436 | 1.0 | False |
| SMD | machine-1-6 | 1 | best_val | 80 | A_on | 0.7824 | 0.7370 | 0.7296 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_off | 0.8600 | 0.8396 | 0.8348 | 1.0 | False |
| SMD | machine-1-6 | 2 | last | 80 | A_on | 0.7694 | 0.7346 | 0.6977 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 73 | A_off | 0.8634 | 0.8428 | 0.8388 | 1.0 | False |
| SMD | machine-1-6 | 2 | best_val | 73 | A_on | 0.7538 | 0.7159 | 0.6857 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_off | 0.8570 | 0.8365 | 0.8359 | 1.0 | False |
| SMD | machine-1-6 | 3 | last | 80 | A_on | 0.7796 | 0.7486 | 0.7106 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 79 | A_off | 0.8576 | 0.8371 | 0.8369 | 1.0 | False |
| SMD | machine-1-6 | 3 | best_val | 79 | A_on | 0.7706 | 0.7394 | 0.7011 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_off | 0.6441 | 0.6525 | 0.7139 | 1.0 | False |
| SMD | machine-1-7 | 0 | last | 80 | A_on | 0.5713 | 0.5780 | 0.6624 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 78 | A_off | 0.6447 | 0.6530 | 0.7132 | 1.0 | False |
| SMD | machine-1-7 | 0 | best_val | 78 | A_on | 0.5801 | 0.5869 | 0.6484 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_off | 0.6434 | 0.6507 | 0.7151 | 1.0 | False |
| SMD | machine-1-7 | 1 | last | 80 | A_on | 0.4680 | 0.4720 | 0.5453 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 70 | A_off | 0.6414 | 0.6489 | 0.7152 | 1.0 | False |
| SMD | machine-1-7 | 1 | best_val | 70 | A_on | 0.4997 | 0.5052 | 0.5763 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_off | 0.6419 | 0.6503 | 0.7154 | 1.0 | False |
| SMD | machine-1-7 | 2 | last | 80 | A_on | 0.4776 | 0.4822 | 0.5600 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 73 | A_off | 0.6394 | 0.6479 | 0.7153 | 1.0 | False |
| SMD | machine-1-7 | 2 | best_val | 73 | A_on | 0.4701 | 0.4733 | 0.5518 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_off | 0.6446 | 0.6521 | 0.7148 | 1.0 | False |
| SMD | machine-1-7 | 3 | last | 80 | A_on | 0.4697 | 0.4729 | 0.5477 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 73 | A_off | 0.6428 | 0.6507 | 0.7133 | 1.0 | False |
| SMD | machine-1-7 | 3 | best_val | 73 | A_on | 0.4557 | 0.4592 | 0.5410 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_off | 0.2641 | 0.2228 | 0.3232 | 1.0 | False |
| SMD | machine-1-8 | 0 | last | 80 | A_on | 0.1965 | 0.0934 | 0.2367 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 72 | A_off | 0.2655 | 0.2240 | 0.3269 | 1.0 | False |
| SMD | machine-1-8 | 0 | best_val | 72 | A_on | 0.2066 | 0.1006 | 0.2531 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_off | 0.2686 | 0.2297 | 0.3299 | 1.0 | False |
| SMD | machine-1-8 | 1 | last | 80 | A_on | 0.2084 | 0.1137 | 0.2516 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 78 | A_off | 0.2686 | 0.2292 | 0.3323 | 1.0 | False |
| SMD | machine-1-8 | 1 | best_val | 78 | A_on | 0.2097 | 0.1140 | 0.2522 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_off | 0.2662 | 0.2216 | 0.3248 | 1.0 | False |
| SMD | machine-1-8 | 2 | last | 80 | A_on | 0.2037 | 0.1012 | 0.2503 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 79 | A_off | 0.2646 | 0.2211 | 0.3246 | 1.0 | False |
| SMD | machine-1-8 | 2 | best_val | 79 | A_on | 0.2062 | 0.1038 | 0.2563 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_off | 0.2641 | 0.2230 | 0.3278 | 1.0 | False |
| SMD | machine-1-8 | 3 | last | 80 | A_on | 0.2067 | 0.1026 | 0.2564 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 77 | A_off | 0.2625 | 0.2194 | 0.3261 | 1.0 | False |
| SMD | machine-1-8 | 3 | best_val | 77 | A_on | 0.2069 | 0.1028 | 0.2589 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/PSM/PSM/seed0/psm_cf_val_noalign | 80 | 80 / 0.2255892531743166 | 80 / 0.2255892531743166 | 4499 |
| train/PSM/PSM/seed1/psm_cf_val_noalign | 80 | 80 / 0.2115292883212755 | 80 / 0.2115292883212755 | 4777 |
| train/PSM/PSM/seed2/psm_cf_val_noalign | 80 | 80 / 0.2142455615018688 | 74 / 0.2138522841098935 | 4701 |
| train/PSM/PSM/seed3/psm_cf_val_noalign | 80 | 80 / 0.2047470695013709 | 79 / 0.2036812553387039 | 4864 |
| train/SMD/machine-1-1/seed0/smd_cf_val_noalign | 80 | 80 / 0.1806970010815186 | 78 / 0.1798028193507504 | 1357 |
| train/SMD/machine-1-1/seed1/smd_cf_val_noalign | 80 | 80 / 0.1816132246190816 | 77 / 0.1810316019955918 | 1358 |
| train/SMD/machine-1-1/seed2/smd_cf_val_noalign | 80 | 80 / 0.1786094527771347 | 78 / 0.1785195567863325 | 1373 |
| train/SMD/machine-1-1/seed3/smd_cf_val_noalign | 80 | 80 / 0.1802113441856405 | 79 / 0.1800913453674697 | 1248 |
| train/SMD/machine-1-2/seed0/smd_cf_val_noalign | 80 | 80 / 0.2056985361233587 | 78 / 0.203680783266802 | 1179 |
| train/SMD/machine-1-2/seed1/smd_cf_val_noalign | 80 | 80 / 0.2016401743164605 | 80 / 0.2016401743164605 | 1170 |
| train/SMD/machine-1-2/seed2/smd_cf_val_noalign | 80 | 80 / 0.2014877691170232 | 80 / 0.2014877691170232 | 1162 |
| train/SMD/machine-1-2/seed3/smd_cf_val_noalign | 80 | 80 / 0.2037244940011005 | 77 / 0.2036989118016388 | 1182 |
| train/SMD/machine-1-3/seed0/smd_cf_val_noalign | 80 | 80 / 0.7971587314187063 | 69 / 0.7912683903572219 | 1174 |
| train/SMD/machine-1-3/seed1/smd_cf_val_noalign | 80 | 80 / 0.7892106237667081 | 80 / 0.7892106237667081 | 1183 |
| train/SMD/machine-1-3/seed2/smd_cf_val_noalign | 80 | 80 / 0.8274150416753144 | 29 / 0.7977419926850755 | 1166 |
| train/SMD/machine-1-3/seed3/smd_cf_val_noalign | 80 | 80 / 0.7912542412334588 | 80 / 0.7912542412334588 | 1160 |
| train/SMD/machine-1-4/seed0/smd_cf_val_noalign | 80 | 80 / 0.8814544494441541 | 80 / 0.8814544494441541 | 1183 |
| train/SMD/machine-1-4/seed1/smd_cf_val_noalign | 80 | 80 / 0.8799597126693919 | 79 / 0.8794324531797869 | 1161 |
| train/SMD/machine-1-4/seed2/smd_cf_val_noalign | 80 | 80 / 0.8911771180711724 | 75 / 0.8887240598277806 | 1175 |
| train/SMD/machine-1-4/seed3/smd_cf_val_noalign | 80 | 80 / 0.872183256865916 | 80 / 0.872183256865916 | 1176 |
| train/SMD/machine-1-5/seed0/smd_cf_val_noalign | 80 | 80 / 0.2128899882271148 | 61 / 0.2108660303899845 | 1166 |
| train/SMD/machine-1-5/seed1/smd_cf_val_noalign | 80 | 80 / 0.2157821631513255 | 73 / 0.214655222797084 | 1171 |
| train/SMD/machine-1-5/seed2/smd_cf_val_noalign | 80 | 80 / 0.2141995204907377 | 69 / 0.2059491495223329 | 1171 |
| train/SMD/machine-1-5/seed3/smd_cf_val_noalign | 80 | 80 / 0.2124419896507271 | 80 / 0.2124419896507271 | 1165 |
| train/SMD/machine-1-6/seed0/smd_cf_val_noalign | 80 | 80 / 0.1921977044754562 | 78 / 0.1906530193422217 | 1130 |
| train/SMD/machine-1-6/seed1/smd_cf_val_noalign | 80 | 80 / 0.1902860717114523 | 80 / 0.1902860717114523 | 1148 |
| train/SMD/machine-1-6/seed2/smd_cf_val_noalign | 80 | 80 / 0.1948971048521041 | 73 / 0.192177772659954 | 1141 |
| train/SMD/machine-1-6/seed3/smd_cf_val_noalign | 80 | 80 / 0.1923396909797192 | 79 / 0.1911361644577724 | 1135 |
| train/SMD/machine-1-7/seed0/smd_cf_val_noalign | 80 | 80 / 0.0868219661065332 | 78 / 0.0840074504590397 | 1160 |
| train/SMD/machine-1-7/seed1/smd_cf_val_noalign | 80 | 80 / 0.0878511324626022 | 70 / 0.0846878416800613 | 1101 |
| train/SMD/machine-1-7/seed2/smd_cf_val_noalign | 80 | 80 / 0.0838129651630045 | 73 / 0.083261462235273 | 1171 |
| train/SMD/machine-1-7/seed3/smd_cf_val_noalign | 80 | 80 / 0.0850334774470241 | 73 / 0.0834876288319238 | 1166 |
| train/SMD/machine-1-8/seed0/smd_cf_val_noalign | 80 | 80 / 0.1556031511944158 | 72 / 0.1521012831244037 | 1160 |
| train/SMD/machine-1-8/seed1/smd_cf_val_noalign | 80 | 80 / 0.15535482314038 | 78 / 0.1538529762879426 | 1170 |
| train/SMD/machine-1-8/seed2/smd_cf_val_noalign | 80 | 80 / 0.1583704649715769 | 79 / 0.1555927131770894 | 1170 |
| train/SMD/machine-1-8/seed3/smd_cf_val_noalign | 80 | 80 / 0.1631079179376569 | 77 / 0.1537317907200564 | 1202 |
