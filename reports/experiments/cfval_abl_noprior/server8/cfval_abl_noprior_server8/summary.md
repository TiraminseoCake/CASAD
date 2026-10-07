# cfval_abl_noprior / server8 / cfval_abl_noprior_server8

- exported: 2026-10-07T11:33:02+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 273 — {'success': 273} — **COMPLETE**
- exported eval jobs: 168, train jobs: 84; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SWaT | swat | 0 | last | 80 | A_off | 0.6215 | 0.5227 | 0.7007 | 1.0 | False |
| SWaT | swat | 0 | last | 80 | A_on | 0.7200 | 0.5772 | 0.7545 | 1.0 | False |
| SWaT | swat | 0 | best_val | 76 | A_off | 0.6392 | 0.5350 | 0.7131 | 1.0 | False |
| SWaT | swat | 0 | best_val | 76 | A_on | 0.7188 | 0.5673 | 0.7537 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_off | 0.7163 | 0.5518 | 0.7700 | 1.0 | False |
| SWaT | swat | 1 | last | 80 | A_on | 0.7224 | 0.4553 | 0.7872 | 1.0 | False |
| SWaT | swat | 1 | best_val | 65 | A_off | 0.7162 | 0.5380 | 0.7700 | 1.0 | False |
| SWaT | swat | 1 | best_val | 65 | A_on | 0.7276 | 0.4663 | 0.7886 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_off | 0.6671 | 0.5568 | 0.7313 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7497 | 0.5825 | 0.8016 | 1.0 | False |
| SWaT | swat | 2 | best_val | 80 | A_off | 0.6671 | 0.5568 | 0.7313 | 1.0 | False |
| SWaT | swat | 2 | best_val | 80 | A_on | 0.7497 | 0.5825 | 0.8016 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.5855 | 0.5017 | 0.6477 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7675 | 0.6377 | 0.8110 | 1.0 | False |
| SWaT | swat | 3 | best_val | 77 | A_off | 0.5636 | 0.4784 | 0.6181 | 1.0 | False |
| SWaT | swat | 3 | best_val | 77 | A_on | 0.7670 | 0.6271 | 0.8110 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_off | 0.1559 | 0.1562 | 0.2034 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_on | 0.1797 | 0.1822 | 0.2426 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 76 | A_off | 0.1582 | 0.1589 | 0.2041 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 76 | A_on | 0.1754 | 0.1774 | 0.2352 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_off | 0.1519 | 0.1522 | 0.1982 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_on | 0.2152 | 0.2201 | 0.2780 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 60 | A_off | 0.1571 | 0.1587 | 0.2017 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 60 | A_on | 0.2387 | 0.2391 | 0.2778 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_off | 0.1581 | 0.1603 | 0.2037 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_on | 0.1874 | 0.1882 | 0.2612 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 72 | A_off | 0.1568 | 0.1583 | 0.2027 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 72 | A_on | 0.1954 | 0.1993 | 0.2668 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_off | 0.1571 | 0.1572 | 0.2027 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_on | 0.2031 | 0.2012 | 0.2789 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 66 | A_off | 0.1588 | 0.1601 | 0.2040 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 66 | A_on | 0.2054 | 0.2063 | 0.2732 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_off | 0.1491 | 0.1510 | 0.2319 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_on | 0.1587 | 0.1631 | 0.2362 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 58 | A_off | 0.1623 | 0.1645 | 0.2588 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 58 | A_on | 0.1811 | 0.1865 | 0.2680 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_off | 0.1552 | 0.1572 | 0.2473 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_on | 0.1672 | 0.1716 | 0.2386 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 80 | A_off | 0.1552 | 0.1572 | 0.2473 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 80 | A_on | 0.1672 | 0.1716 | 0.2386 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_off | 0.1505 | 0.1524 | 0.2309 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_on | 0.1661 | 0.1706 | 0.2305 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 41 | A_off | 0.1607 | 0.1630 | 0.2569 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 41 | A_on | 0.1848 | 0.1901 | 0.2660 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_off | 0.1495 | 0.1515 | 0.2314 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_on | 0.1610 | 0.1658 | 0.2346 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 51 | A_off | 0.1594 | 0.1618 | 0.2538 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 51 | A_on | 0.1559 | 0.1599 | 0.2351 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_off | 0.4077 | 0.3583 | 0.4444 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_on | 0.5323 | 0.4919 | 0.5526 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 80 | A_off | 0.4077 | 0.3583 | 0.4444 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 80 | A_on | 0.5323 | 0.4919 | 0.5526 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_off | 0.4174 | 0.3596 | 0.4428 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_on | 0.4967 | 0.4613 | 0.5244 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 79 | A_off | 0.4163 | 0.3561 | 0.4418 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 79 | A_on | 0.4995 | 0.4654 | 0.5236 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_off | 0.4085 | 0.3543 | 0.4506 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_on | 0.5353 | 0.5021 | 0.5176 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 80 | A_off | 0.4085 | 0.3543 | 0.4506 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 80 | A_on | 0.5353 | 0.5021 | 0.5176 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_off | 0.4177 | 0.3528 | 0.4355 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_on | 0.5125 | 0.4709 | 0.5197 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 80 | A_off | 0.4177 | 0.3528 | 0.4355 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 80 | A_on | 0.5125 | 0.4709 | 0.5197 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_off | 0.4002 | 0.3935 | 0.3927 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_on | 0.3730 | 0.3274 | 0.3470 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 73 | A_off | 0.3962 | 0.3897 | 0.3907 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 73 | A_on | 0.3754 | 0.3276 | 0.3469 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_off | 0.3923 | 0.3859 | 0.3876 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_on | 0.4264 | 0.4002 | 0.3879 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 74 | A_off | 0.3917 | 0.3850 | 0.3899 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 74 | A_on | 0.4294 | 0.4027 | 0.3905 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_off | 0.3911 | 0.3845 | 0.3863 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_on | 0.4444 | 0.4042 | 0.4076 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 77 | A_off | 0.3928 | 0.3868 | 0.3876 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 77 | A_on | 0.4435 | 0.4074 | 0.4088 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_off | 0.3966 | 0.3897 | 0.3933 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_on | 0.3979 | 0.3609 | 0.3528 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 77 | A_off | 0.3961 | 0.3889 | 0.3917 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 77 | A_on | 0.4303 | 0.4131 | 0.3764 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_off | 0.4327 | 0.4290 | 0.4955 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_on | 0.3106 | 0.2864 | 0.3373 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 80 | A_off | 0.4327 | 0.4290 | 0.4955 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 80 | A_on | 0.3106 | 0.2864 | 0.3373 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_off | 0.4216 | 0.4173 | 0.4819 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_on | 0.3060 | 0.2775 | 0.3163 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 80 | A_off | 0.4216 | 0.4173 | 0.4819 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 80 | A_on | 0.3060 | 0.2775 | 0.3163 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_off | 0.4338 | 0.4294 | 0.4929 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_on | 0.3169 | 0.2956 | 0.3251 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 75 | A_off | 0.4342 | 0.4297 | 0.4908 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 75 | A_on | 0.3192 | 0.2980 | 0.3231 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_off | 0.4300 | 0.4262 | 0.4889 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_on | 0.3023 | 0.2759 | 0.3185 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 79 | A_off | 0.4288 | 0.4252 | 0.4877 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 79 | A_on | 0.3031 | 0.2768 | 0.3173 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_off | 0.3698 | 0.3228 | 0.4765 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_on | 0.3823 | 0.3371 | 0.4562 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 76 | A_off | 0.3700 | 0.3232 | 0.4767 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 76 | A_on | 0.3840 | 0.3363 | 0.4516 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_off | 0.3671 | 0.3196 | 0.4776 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_on | 0.4046 | 0.3525 | 0.4657 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 79 | A_off | 0.3675 | 0.3199 | 0.4776 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 79 | A_on | 0.4058 | 0.3530 | 0.4655 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_off | 0.3702 | 0.3225 | 0.4747 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_on | 0.3855 | 0.3600 | 0.4740 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 77 | A_off | 0.3706 | 0.3228 | 0.4747 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 77 | A_on | 0.3864 | 0.3606 | 0.4684 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_off | 0.3697 | 0.3248 | 0.4763 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_on | 0.3957 | 0.3628 | 0.4813 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 72 | A_off | 0.3697 | 0.3262 | 0.4772 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 72 | A_on | 0.3953 | 0.3577 | 0.4884 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_off | 0.8137 | 0.7627 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_on | 0.7891 | 0.6572 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 80 | A_off | 0.8137 | 0.7627 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 80 | A_on | 0.7891 | 0.6572 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_off | 0.8082 | 0.7531 | 0.8188 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_on | 0.7914 | 0.6738 | 0.8169 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 73 | A_off | 0.8103 | 0.7556 | 0.8223 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 73 | A_on | 0.7965 | 0.6673 | 0.8216 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_off | 0.8058 | 0.7553 | 0.8168 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_on | 0.7895 | 0.6567 | 0.8169 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 76 | A_off | 0.8051 | 0.7535 | 0.8152 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 76 | A_on | 0.7912 | 0.6583 | 0.8118 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_off | 0.8057 | 0.7499 | 0.8202 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_on | 0.7842 | 0.6309 | 0.8062 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 80 | A_off | 0.8057 | 0.7499 | 0.8202 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 80 | A_on | 0.7842 | 0.6309 | 0.8062 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_off | 0.9674 | 0.9365 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_on | 0.9685 | 0.9308 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 66 | A_off | 0.9674 | 0.9342 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 66 | A_on | 0.9687 | 0.9341 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_off | 0.9675 | 0.9408 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_on | 0.9689 | 0.9402 | 0.9716 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 72 | A_off | 0.9676 | 0.9408 | 0.9655 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 72 | A_on | 0.9691 | 0.9423 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_off | 0.9673 | 0.9428 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_on | 0.9688 | 0.9318 | 0.9716 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 78 | A_off | 0.9674 | 0.9428 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 78 | A_on | 0.9689 | 0.9333 | 0.9716 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_off | 0.9675 | 0.9428 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_on | 0.9684 | 0.9268 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 76 | A_off | 0.9676 | 0.9406 | 0.9653 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 76 | A_on | 0.9686 | 0.9339 | 0.9687 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_off | 0.8321 | 0.8911 | 0.8161 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_on | 0.8264 | 0.8768 | 0.7918 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 78 | A_off | 0.8325 | 0.8914 | 0.8159 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 78 | A_on | 0.8282 | 0.8796 | 0.7949 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_off | 0.8295 | 0.8883 | 0.8145 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_on | 0.8345 | 0.8816 | 0.7880 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 78 | A_off | 0.8288 | 0.8876 | 0.8140 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 78 | A_on | 0.8349 | 0.8820 | 0.7886 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_off | 0.8332 | 0.8924 | 0.8168 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_on | 0.8502 | 0.9077 | 0.8000 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 77 | A_off | 0.8313 | 0.8908 | 0.8151 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 77 | A_on | 0.8506 | 0.8988 | 0.8126 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_off | 0.8361 | 0.8943 | 0.8176 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_on | 0.8152 | 0.8597 | 0.7637 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 77 | A_off | 0.8352 | 0.8937 | 0.8188 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 77 | A_on | 0.8105 | 0.8548 | 0.7598 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_off | 0.4855 | 0.4215 | 0.5286 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_on | 0.3741 | 0.2056 | 0.4680 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 78 | A_off | 0.4869 | 0.4214 | 0.5321 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 78 | A_on | 0.3749 | 0.2082 | 0.4680 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_off | 0.4786 | 0.4108 | 0.5166 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_on | 0.3724 | 0.2593 | 0.4692 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_off | 0.4786 | 0.4108 | 0.5166 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_on | 0.3724 | 0.2593 | 0.4692 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_off | 0.4716 | 0.4022 | 0.5086 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_on | 0.3800 | 0.2715 | 0.4683 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 79 | A_off | 0.4709 | 0.4000 | 0.5051 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 79 | A_on | 0.3821 | 0.2861 | 0.4683 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_off | 0.4773 | 0.4055 | 0.5130 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_on | 0.4078 | 0.3224 | 0.4671 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 78 | A_off | 0.4785 | 0.4098 | 0.5139 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 78 | A_on | 0.4075 | 0.3202 | 0.4683 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_off | 0.0726 | 0.0653 | 0.1053 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_on | 0.0656 | 0.0610 | 0.1081 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 78 | A_off | 0.0728 | 0.0656 | 0.1057 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 78 | A_on | 0.0622 | 0.0590 | 0.1021 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_off | 0.0723 | 0.0652 | 0.1061 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_on | 0.0783 | 0.0730 | 0.1318 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 72 | A_off | 0.0727 | 0.0662 | 0.1100 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 72 | A_on | 0.0731 | 0.0680 | 0.1147 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_off | 0.0734 | 0.0674 | 0.1137 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_on | 0.0582 | 0.0554 | 0.0944 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 79 | A_off | 0.0725 | 0.0669 | 0.1136 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 79 | A_on | 0.0597 | 0.0570 | 0.0961 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_off | 0.0720 | 0.0646 | 0.1068 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_on | 0.0690 | 0.0644 | 0.1163 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 77 | A_off | 0.0724 | 0.0651 | 0.1093 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 77 | A_on | 0.0707 | 0.0664 | 0.1253 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_off | 0.1211 | 0.1042 | 0.1793 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_on | 0.0832 | 0.0796 | 0.1286 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 76 | A_off | 0.1269 | 0.1099 | 0.1886 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 76 | A_on | 0.0864 | 0.0854 | 0.1383 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_off | 0.1285 | 0.1115 | 0.1881 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_on | 0.0780 | 0.0729 | 0.1315 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 79 | A_off | 0.1271 | 0.1093 | 0.1873 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 79 | A_on | 0.0761 | 0.0704 | 0.1243 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_off | 0.1241 | 0.1070 | 0.1840 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_on | 0.0920 | 0.0771 | 0.1325 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 79 | A_off | 0.1287 | 0.1114 | 0.1888 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 79 | A_on | 0.0924 | 0.0782 | 0.1418 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_off | 0.1270 | 0.1095 | 0.1893 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_on | 0.0967 | 0.0917 | 0.1477 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 58 | A_off | 0.1313 | 0.1134 | 0.1916 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 58 | A_on | 0.1056 | 0.1006 | 0.1561 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_off | 0.8829 | 0.8824 | 0.8864 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_on | 0.8839 | 0.8605 | 0.8663 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 77 | A_off | 0.8825 | 0.8819 | 0.8864 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 77 | A_on | 0.8847 | 0.8613 | 0.8674 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_off | 0.8817 | 0.8809 | 0.8870 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_on | 0.8916 | 0.8826 | 0.8679 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 79 | A_off | 0.8827 | 0.8829 | 0.8868 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 79 | A_on | 0.8922 | 0.8842 | 0.8696 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_off | 0.8836 | 0.8829 | 0.8867 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_on | 0.8955 | 0.8920 | 0.8693 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 79 | A_off | 0.8833 | 0.8832 | 0.8859 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 79 | A_on | 0.8966 | 0.8938 | 0.8704 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_off | 0.8837 | 0.8835 | 0.8857 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_on | 0.8882 | 0.8882 | 0.8683 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 71 | A_off | 0.8836 | 0.8829 | 0.8852 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 71 | A_on | 0.8900 | 0.8909 | 0.8712 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_off | 0.2548 | 0.1330 | 0.3487 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_on | 0.2462 | 0.1367 | 0.3759 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 79 | A_off | 0.2550 | 0.1333 | 0.3483 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 79 | A_on | 0.2492 | 0.1387 | 0.3839 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_off | 0.2537 | 0.1299 | 0.3465 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_on | 0.3056 | 0.1612 | 0.4070 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 76 | A_off | 0.2538 | 0.1299 | 0.3457 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 76 | A_on | 0.3057 | 0.1611 | 0.4073 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_off | 0.2525 | 0.1306 | 0.3454 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_on | 0.2840 | 0.1494 | 0.3959 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 80 | A_off | 0.2525 | 0.1306 | 0.3454 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 80 | A_on | 0.2840 | 0.1494 | 0.3959 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_off | 0.2535 | 0.1315 | 0.3475 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_on | 0.2596 | 0.1408 | 0.3710 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 77 | A_off | 0.2536 | 0.1325 | 0.3471 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 77 | A_on | 0.2557 | 0.1343 | 0.3610 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_off | 0.4746 | 0.5427 | 0.4789 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_on | 0.5557 | 0.6204 | 0.5284 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 74 | A_off | 0.4740 | 0.5414 | 0.4794 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 74 | A_on | 0.5542 | 0.6199 | 0.5251 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_off | 0.4952 | 0.5645 | 0.4896 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_on | 0.5423 | 0.6114 | 0.5302 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 79 | A_off | 0.4957 | 0.5654 | 0.4904 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 79 | A_on | 0.5446 | 0.6110 | 0.5289 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_off | 0.4839 | 0.5542 | 0.4824 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_on | 0.5273 | 0.5819 | 0.5218 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 78 | A_off | 0.4836 | 0.5534 | 0.4845 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 78 | A_on | 0.5216 | 0.5788 | 0.5201 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_off | 0.4832 | 0.5521 | 0.4854 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_on | 0.5837 | 0.6570 | 0.5454 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 77 | A_off | 0.4832 | 0.5518 | 0.4851 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 77 | A_on | 0.5889 | 0.6618 | 0.5514 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_off | 0.2316 | 0.2025 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_on | 0.3387 | 0.2812 | 0.4013 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 78 | A_off | 0.2310 | 0.2015 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 78 | A_on | 0.3381 | 0.2827 | 0.4135 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_off | 0.2338 | 0.2040 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_on | 0.3068 | 0.2372 | 0.3939 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 76 | A_off | 0.2342 | 0.2043 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 76 | A_on | 0.3073 | 0.2502 | 0.3973 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_off | 0.2328 | 0.2028 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_on | 0.3133 | 0.2441 | 0.4053 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 71 | A_off | 0.2333 | 0.2035 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 71 | A_on | 0.3191 | 0.2466 | 0.4044 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_off | 0.2299 | 0.2010 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_on | 0.3355 | 0.2129 | 0.4209 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 77 | A_off | 0.2304 | 0.2015 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 77 | A_on | 0.3302 | 0.2024 | 0.4186 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_off | 0.3260 | 0.3457 | 0.3206 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_on | 0.4915 | 0.5077 | 0.4650 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 78 | A_off | 0.3283 | 0.3480 | 0.3237 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 78 | A_on | 0.4910 | 0.5067 | 0.4663 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_off | 0.3234 | 0.3425 | 0.3230 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_on | 0.4925 | 0.5030 | 0.4704 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 79 | A_off | 0.3222 | 0.3415 | 0.3235 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 79 | A_on | 0.4901 | 0.5011 | 0.4675 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_off | 0.3272 | 0.3479 | 0.3219 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_on | 0.4952 | 0.5075 | 0.4756 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 73 | A_off | 0.3274 | 0.3480 | 0.3220 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 73 | A_on | 0.4943 | 0.5052 | 0.4735 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_off | 0.3256 | 0.3446 | 0.3248 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_on | 0.4934 | 0.4988 | 0.4653 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 75 | A_off | 0.3230 | 0.3425 | 0.3251 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 75 | A_on | 0.4934 | 0.4983 | 0.4670 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_off | 0.4562 | 0.3929 | 0.5052 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_on | 0.3516 | 0.2156 | 0.4750 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 77 | A_off | 0.4559 | 0.3926 | 0.5052 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 77 | A_on | 0.3534 | 0.2184 | 0.4750 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_off | 0.4526 | 0.3879 | 0.4932 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_on | 0.3507 | 0.2279 | 0.4746 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 78 | A_off | 0.4531 | 0.3878 | 0.4921 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 78 | A_on | 0.3502 | 0.2277 | 0.4746 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_off | 0.4535 | 0.3900 | 0.4958 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_on | 0.3473 | 0.2116 | 0.4755 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 80 | A_off | 0.4535 | 0.3900 | 0.4958 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 80 | A_on | 0.3473 | 0.2116 | 0.4755 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_off | 0.4419 | 0.3674 | 0.4740 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_on | 0.3489 | 0.2237 | 0.4724 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 79 | A_off | 0.4412 | 0.3654 | 0.4740 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 79 | A_on | 0.3484 | 0.2234 | 0.4724 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_off | 0.8013 | 0.8152 | 0.8373 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_on | 0.7835 | 0.7086 | 0.8519 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_off | 0.8053 | 0.8206 | 0.8460 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_on | 0.7816 | 0.7022 | 0.8524 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_off | 0.7905 | 0.8051 | 0.8122 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_on | 0.7756 | 0.4758 | 0.8339 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 76 | A_off | 0.7862 | 0.7996 | 0.8055 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 76 | A_on | 0.7858 | 0.5911 | 0.8559 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_off | 0.7717 | 0.7865 | 0.7807 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_on | 0.7892 | 0.7053 | 0.8556 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 73 | A_off | 0.7705 | 0.7853 | 0.7819 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 73 | A_on | 0.7891 | 0.7441 | 0.8590 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_off | 0.7814 | 0.7950 | 0.7984 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_on | 0.7819 | 0.6701 | 0.8511 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 68 | A_off | 0.7846 | 0.7998 | 0.8080 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 68 | A_on | 0.7823 | 0.6534 | 0.8521 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_off | 0.2247 | 0.2781 | 0.3779 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_on | 0.2111 | 0.1916 | 0.2825 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 80 | A_off | 0.2247 | 0.2781 | 0.3779 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 80 | A_on | 0.2111 | 0.1916 | 0.2825 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_off | 0.2277 | 0.2734 | 0.3816 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_on | 0.1771 | 0.1461 | 0.2636 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_off | 0.2277 | 0.2734 | 0.3816 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_on | 0.1771 | 0.1461 | 0.2636 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_off | 0.2218 | 0.2690 | 0.3628 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_on | 0.1675 | 0.1296 | 0.2571 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 77 | A_off | 0.2224 | 0.2720 | 0.3674 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 77 | A_on | 0.1681 | 0.1286 | 0.2571 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_off | 0.2291 | 0.2859 | 0.3868 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_on | 0.1820 | 0.1544 | 0.2895 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 78 | A_off | 0.2303 | 0.2888 | 0.3928 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 78 | A_on | 0.1828 | 0.1552 | 0.2951 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SWaT/swat/seed0/swat_cf_val_noprior | 80 | 80 / 0.0052489783226579 | 76 / 0.0051490361920487 | 106898 |
| train/SWaT/swat/seed1/swat_cf_val_noprior | 80 | 80 / 0.0052404627809974 | 65 / 0.0050791484942323 | 101579 |
| train/SWaT/swat/seed2/swat_cf_val_noprior | 80 | 80 / 0.0050473172543366 | 80 / 0.0050473172543366 | 107932 |
| train/SWaT/swat/seed3/swat_cf_val_noprior | 80 | 80 / 0.0052613505125237 | 77 / 0.0050629345283351 | 110746 |
| train/SMD/machine-2-1/seed0/smd_cf_val_noprior | 80 | 80 / 0.2677512646305079 | 76 / 0.2652475437067952 | 1171 |
| train/SMD/machine-2-1/seed1/smd_cf_val_noprior | 80 | 80 / 0.2733159899857519 | 60 / 0.2650976839592954 | 1156 |
| train/SMD/machine-2-1/seed2/smd_cf_val_noprior | 80 | 80 / 0.2631603831402303 | 72 / 0.2625569514309297 | 1250 |
| train/SMD/machine-2-1/seed3/smd_cf_val_noprior | 80 | 80 / 0.267333784025928 | 66 / 0.2620786889928247 | 1177 |
| train/SMD/machine-2-2/seed0/smd_cf_val_noprior | 80 | 80 / 0.2128747087635297 | 58 / 0.1978740756856416 | 1176 |
| train/SMD/machine-2-2/seed1/smd_cf_val_noprior | 80 | 80 / 0.2016555855221657 | 80 / 0.2016555855221657 | 1243 |
| train/SMD/machine-2-2/seed2/smd_cf_val_noprior | 80 | 80 / 0.2124291434316299 | 41 / 0.1988608548470631 | 1218 |
| train/SMD/machine-2-2/seed3/smd_cf_val_noprior | 80 | 80 / 0.2152667815044805 | 51 / 0.1999357197390236 | 1184 |
| train/SMD/machine-2-3/seed0/smd_cf_val_noprior | 80 | 80 / 0.1132665487406755 | 80 / 0.1132665487406755 | 1156 |
| train/SMD/machine-2-3/seed1/smd_cf_val_noprior | 80 | 80 / 0.1129704503519194 | 79 / 0.1126094781221132 | 1185 |
| train/SMD/machine-2-3/seed2/smd_cf_val_noprior | 80 | 80 / 0.1131016687033863 | 80 / 0.1131016687033863 | 1182 |
| train/SMD/machine-2-3/seed3/smd_cf_val_noprior | 80 | 80 / 0.1124991785988921 | 80 / 0.1124991785988921 | 1155 |
| train/SMD/machine-2-4/seed0/smd_cf_val_noprior | 80 | 80 / 0.1554433174734899 | 73 / 0.1544847137824443 | 1129 |
| train/SMD/machine-2-4/seed1/smd_cf_val_noprior | 80 | 80 / 0.1565842046887433 | 74 / 0.1551038102235098 | 1160 |
| train/SMD/machine-2-4/seed2/smd_cf_val_noprior | 80 | 80 / 0.1569711174203725 | 77 / 0.1557066600136528 | 1158 |
| train/SMD/machine-2-4/seed3/smd_cf_val_noprior | 80 | 80 / 0.1560131553215749 | 77 / 0.154754878801954 | 1154 |
| train/SMD/machine-2-5/seed0/smd_cf_val_noprior | 80 | 80 / 0.1209743139857931 | 80 / 0.1209743139857931 | 1195 |
| train/SMD/machine-2-5/seed1/smd_cf_val_noprior | 80 | 80 / 0.1162179247079018 | 80 / 0.1162179247079018 | 1196 |
| train/SMD/machine-2-5/seed2/smd_cf_val_noprior | 80 | 80 / 0.1213288220633152 | 75 / 0.1208335413781392 | 1148 |
| train/SMD/machine-2-5/seed3/smd_cf_val_noprior | 80 | 80 / 0.1163436210864897 | 79 / 0.1162440842817205 | 1187 |
| train/SMD/machine-2-6/seed0/smd_cf_val_noprior | 80 | 80 / 0.1172737797356386 | 76 / 0.1164736631789733 | 1385 |
| train/SMD/machine-2-6/seed1/smd_cf_val_noprior | 80 | 80 / 0.1199444695085686 | 79 / 0.1183922503730386 | 1417 |
| train/SMD/machine-2-6/seed2/smd_cf_val_noprior | 80 | 80 / 0.1184377516734803 | 77 / 0.1177942877272258 | 1404 |
| train/SMD/machine-2-6/seed3/smd_cf_val_noprior | 80 | 80 / 0.1189268314005496 | 72 / 0.1184424641852463 | 1320 |
| train/SMD/machine-2-7/seed0/smd_cf_val_noprior | 80 | 80 / 0.1141768853975056 | 80 / 0.1141768853975056 | 1217 |
| train/SMD/machine-2-7/seed1/smd_cf_val_noprior | 80 | 80 / 0.1114220416836363 | 73 / 0.1111401792335022 | 1227 |
| train/SMD/machine-2-7/seed2/smd_cf_val_noprior | 80 | 80 / 0.111073419357203 | 76 / 0.1098612553473506 | 1193 |
| train/SMD/machine-2-7/seed3/smd_cf_val_noprior | 80 | 80 / 0.110917667139753 | 80 / 0.110917667139753 | 1183 |
| train/SMD/machine-2-8/seed0/smd_cf_val_noprior | 80 | 80 / 0.1899361004983403 | 66 / 0.1881994045368628 | 1158 |
| train/SMD/machine-2-8/seed1/smd_cf_val_noprior | 80 | 80 / 0.1911054626335153 | 72 / 0.1839619707947962 | 1218 |
| train/SMD/machine-2-8/seed2/smd_cf_val_noprior | 80 | 80 / 0.1880090642608522 | 78 / 0.1852298756900003 | 1206 |
| train/SMD/machine-2-8/seed3/smd_cf_val_noprior | 80 | 80 / 0.1901813614829818 | 76 / 0.1873926668303233 | 1192 |
| train/SMD/machine-2-9/seed0/smd_cf_val_noprior | 80 | 80 / 0.1331278338371266 | 78 / 0.1319799127483774 | 1401 |
| train/SMD/machine-2-9/seed1/smd_cf_val_noprior | 80 | 80 / 0.131660906383357 | 78 / 0.1309958004630931 | 1420 |
| train/SMD/machine-2-9/seed2/smd_cf_val_noprior | 80 | 80 / 0.1324396091675258 | 77 / 0.1321394858077816 | 1421 |
| train/SMD/machine-2-9/seed3/smd_cf_val_noprior | 80 | 80 / 0.1315705879073842 | 77 / 0.1312004498604411 | 1436 |
| train/SMD/machine-3-1/seed0/smd_cf_val_noprior | 80 | 80 / 0.1293202968187141 | 78 / 0.1291395270633612 | 1373 |
| train/SMD/machine-3-1/seed1/smd_cf_val_noprior | 80 | 80 / 0.1279415137656847 | 80 / 0.1279415137656847 | 1397 |
| train/SMD/machine-3-1/seed2/smd_cf_val_noprior | 80 | 80 / 0.1336337271893568 | 79 / 0.1332567765665465 | 1402 |
| train/SMD/machine-3-1/seed3/smd_cf_val_noprior | 80 | 80 / 0.1295172108546676 | 78 / 0.1284125865757646 | 1438 |
| train/SMD/machine-3-2/seed0/smd_cf_val_noprior | 80 | 80 / 0.2309598640623783 | 78 / 0.2293385726130369 | 1176 |
| train/SMD/machine-3-2/seed1/smd_cf_val_noprior | 80 | 80 / 0.2417204566947673 | 72 / 0.2341794571812179 | 1176 |
| train/SMD/machine-3-2/seed2/smd_cf_val_noprior | 80 | 80 / 0.2337414529188864 | 79 / 0.2336164391160556 | 1201 |
| train/SMD/machine-3-2/seed3/smd_cf_val_noprior | 80 | 80 / 0.2313704439577041 | 77 / 0.2310234196883187 | 1164 |
| train/SMD/machine-3-3/seed0/smd_cf_val_noprior | 80 | 80 / 0.1266987274437393 | 76 / 0.1188758157318627 | 1229 |
| train/SMD/machine-3-3/seed1/smd_cf_val_noprior | 80 | 80 / 0.1202926282733765 | 79 / 0.1196693036513496 | 1229 |
| train/SMD/machine-3-3/seed2/smd_cf_val_noprior | 80 | 80 / 0.1230678650844604 | 79 / 0.1196093431342012 | 1208 |
| train/SMD/machine-3-3/seed3/smd_cf_val_noprior | 80 | 80 / 0.1210962271687186 | 58 / 0.1197535141499678 | 1245 |
| train/SMD/machine-3-4/seed0/smd_cf_val_noprior | 80 | 80 / 0.2768937876201374 | 77 / 0.2761364630317739 | 1187 |
| train/SMD/machine-3-4/seed1/smd_cf_val_noprior | 80 | 80 / 0.2787821854049434 | 79 / 0.2771272875872201 | 1090 |
| train/SMD/machine-3-4/seed2/smd_cf_val_noprior | 80 | 80 / 0.277838159768895 | 79 / 0.2753602113756877 | 1153 |
| train/SMD/machine-3-4/seed3/smd_cf_val_noprior | 80 | 80 / 0.2775573098592633 | 71 / 0.2768778276524165 | 1193 |
| train/SMD/machine-3-5/seed0/smd_cf_val_noprior | 80 | 80 / 0.122408125593213 | 79 / 0.1217384408430997 | 1253 |
| train/SMD/machine-3-5/seed1/smd_cf_val_noprior | 80 | 80 / 0.1217758012793619 | 76 / 0.1208404097097642 | 1183 |
| train/SMD/machine-3-5/seed2/smd_cf_val_noprior | 80 | 80 / 0.1208516182142541 | 80 / 0.1208516182142541 | 1143 |
| train/SMD/machine-3-5/seed3/smd_cf_val_noprior | 80 | 80 / 0.121202297626548 | 77 / 0.1207473727201622 | 1214 |
| train/SMD/machine-3-6/seed0/smd_cf_val_noprior | 80 | 80 / 0.1267546106520653 | 74 / 0.1257826214204895 | 1423 |
| train/SMD/machine-3-6/seed1/smd_cf_val_noprior | 80 | 80 / 0.12850140345689 | 79 / 0.1279900772127208 | 1390 |
| train/SMD/machine-3-6/seed2/smd_cf_val_noprior | 80 | 80 / 0.1272078660198974 | 78 / 0.1262959027565112 | 1374 |
| train/SMD/machine-3-6/seed3/smd_cf_val_noprior | 80 | 80 / 0.1281766087125246 | 77 / 0.1278887196170997 | 1454 |
| train/SMD/machine-3-7/seed0/smd_cf_val_noprior | 80 | 80 / 0.0673149266647365 | 78 / 0.0664043390786349 | 1183 |
| train/SMD/machine-3-7/seed1/smd_cf_val_noprior | 80 | 80 / 0.0650545017190451 | 76 / 0.0648927638510328 | 1386 |
| train/SMD/machine-3-7/seed2/smd_cf_val_noprior | 80 | 80 / 0.0667879363322103 | 71 / 0.066718352818658 | 1430 |
| train/SMD/machine-3-7/seed3/smd_cf_val_noprior | 80 | 80 / 0.066688501870334 | 77 / 0.066319193444049 | 1387 |
| train/SMD/machine-3-8/seed0/smd_cf_val_noprior | 80 | 80 / 0.104308922869532 | 78 / 0.1025004817556195 | 1388 |
| train/SMD/machine-3-8/seed1/smd_cf_val_noprior | 80 | 80 / 0.1057573855722296 | 79 / 0.1039622008360482 | 1384 |
| train/SMD/machine-3-8/seed2/smd_cf_val_noprior | 80 | 80 / 0.1070157918104472 | 73 / 0.1049652657235816 | 1347 |
| train/SMD/machine-3-8/seed3/smd_cf_val_noprior | 80 | 80 / 0.1040005492827805 | 75 / 0.1028525471954396 | 1416 |
| train/SMD/machine-3-9/seed0/smd_cf_val_noprior | 80 | 80 / 0.1191232482496704 | 77 / 0.1184668189145704 | 1391 |
| train/SMD/machine-3-9/seed1/smd_cf_val_noprior | 80 | 80 / 0.1183187518250153 | 78 / 0.1173974442761673 | 1228 |
| train/SMD/machine-3-9/seed2/smd_cf_val_noprior | 80 | 80 / 0.1187451889421565 | 80 / 0.1187451889421565 | 1432 |
| train/SMD/machine-3-9/seed3/smd_cf_val_noprior | 80 | 80 / 0.1195395104130931 | 79 / 0.1189633157029916 | 1447 |
| train/SMD/machine-3-10/seed0/smd_cf_val_noprior | 80 | 80 / 0.1033588665899395 | 75 / 0.0991854438561392 | 1163 |
| train/SMD/machine-3-10/seed1/smd_cf_val_noprior | 80 | 80 / 0.1020314567224488 | 76 / 0.1017707950121503 | 1188 |
| train/SMD/machine-3-10/seed2/smd_cf_val_noprior | 80 | 80 / 0.103334206895087 | 73 / 0.0998014532501203 | 1184 |
| train/SMD/machine-3-10/seed3/smd_cf_val_noprior | 80 | 80 / 0.1025989808985414 | 68 / 0.1005830158607635 | 1186 |
| train/SMD/machine-3-11/seed0/smd_cf_val_noprior | 80 | 80 / 0.1171976296382906 | 80 / 0.1171976296382906 | 1431 |
| train/SMD/machine-3-11/seed1/smd_cf_val_noprior | 80 | 80 / 0.115480997788629 | 80 / 0.115480997788629 | 1385 |
| train/SMD/machine-3-11/seed2/smd_cf_val_noprior | 80 | 80 / 0.1155039119010919 | 77 / 0.1152436499667034 | 1396 |
| train/SMD/machine-3-11/seed3/smd_cf_val_noprior | 80 | 80 / 0.1168401759310487 | 78 / 0.1159446583861127 | 1382 |
