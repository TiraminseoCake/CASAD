# cfval_abl_smdcrs20 / ks / cfval_abl_smdcrs20_ks

- exported: 2026-10-12T17:54:23+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 1040 — {'success': 1040} — **COMPLETE**
- exported eval jobs: 640, train jobs: 320; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| SMD | machine-2-1 | 0 | last | 80 | A_off | 0.1580 | 0.1592 | 0.2037 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_on | 0.2108 | 0.2148 | 0.2781 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 79 | A_off | 0.1616 | 0.1629 | 0.2054 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 79 | A_on | 0.2086 | 0.2126 | 0.2793 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_off | 0.1541 | 0.1538 | 0.1998 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_on | 0.2224 | 0.2300 | 0.2773 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 49 | A_off | 0.1584 | 0.1606 | 0.2025 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 49 | A_on | 0.2399 | 0.2433 | 0.2865 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_off | 0.1583 | 0.1601 | 0.1998 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_on | 0.1915 | 0.1991 | 0.2648 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 76 | A_off | 0.1580 | 0.1601 | 0.1994 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 76 | A_on | 0.1861 | 0.1912 | 0.2583 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_off | 0.1607 | 0.1600 | 0.2054 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_on | 0.1968 | 0.1977 | 0.2677 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 74 | A_off | 0.1611 | 0.1614 | 0.2071 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 74 | A_on | 0.2014 | 0.2013 | 0.2654 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_off | 0.1540 | 0.1559 | 0.2355 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_on | 0.1796 | 0.1844 | 0.2628 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 45 | A_off | 0.1609 | 0.1631 | 0.2532 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 45 | A_on | 0.1805 | 0.1866 | 0.2561 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_off | 0.1570 | 0.1592 | 0.2454 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_on | 0.1606 | 0.1641 | 0.2400 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 80 | A_off | 0.1570 | 0.1592 | 0.2454 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 80 | A_on | 0.1606 | 0.1641 | 0.2400 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_off | 0.1468 | 0.1486 | 0.2272 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_on | 0.1590 | 0.1622 | 0.2345 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 31 | A_off | 0.1584 | 0.1607 | 0.2517 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 31 | A_on | 0.1915 | 0.1977 | 0.2705 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_off | 0.1507 | 0.1526 | 0.2331 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_on | 0.1632 | 0.1679 | 0.2437 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 35 | A_off | 0.1592 | 0.1616 | 0.2527 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 35 | A_on | 0.1839 | 0.1903 | 0.2585 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_off | 0.4120 | 0.3512 | 0.4462 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_on | 0.5446 | 0.5113 | 0.5348 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 71 | A_off | 0.4069 | 0.3479 | 0.4368 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 71 | A_on | 0.5615 | 0.5250 | 0.5403 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_off | 0.4005 | 0.3417 | 0.4472 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_on | 0.5436 | 0.5171 | 0.5708 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 79 | A_off | 0.4035 | 0.3475 | 0.4457 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 79 | A_on | 0.5415 | 0.5136 | 0.5670 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_off | 0.3973 | 0.3370 | 0.4208 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_on | 0.5315 | 0.4881 | 0.5562 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 75 | A_off | 0.3909 | 0.3345 | 0.4250 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 75 | A_on | 0.5467 | 0.4980 | 0.5522 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_off | 0.3981 | 0.3382 | 0.4246 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_on | 0.5694 | 0.5189 | 0.5451 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 80 | A_off | 0.3981 | 0.3382 | 0.4246 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 80 | A_on | 0.5694 | 0.5189 | 0.5451 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_off | 0.3982 | 0.3916 | 0.3916 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_on | 0.4243 | 0.4060 | 0.3820 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 76 | A_off | 0.4006 | 0.3935 | 0.3934 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 76 | A_on | 0.4214 | 0.4023 | 0.3817 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_off | 0.3938 | 0.3872 | 0.3889 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_on | 0.4285 | 0.3999 | 0.3851 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 78 | A_off | 0.3939 | 0.3874 | 0.3889 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 78 | A_on | 0.4291 | 0.4013 | 0.3939 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_off | 0.3915 | 0.3853 | 0.3895 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_on | 0.4036 | 0.3683 | 0.3665 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 79 | A_off | 0.3903 | 0.3842 | 0.3886 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 79 | A_on | 0.4069 | 0.3734 | 0.3711 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_off | 0.3932 | 0.3860 | 0.3923 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_on | 0.3997 | 0.3800 | 0.3730 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 76 | A_off | 0.3913 | 0.3841 | 0.3923 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 76 | A_on | 0.4003 | 0.3788 | 0.3727 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_off | 0.4338 | 0.4291 | 0.4936 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_on | 0.3063 | 0.2822 | 0.3215 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 74 | A_off | 0.4322 | 0.4273 | 0.4944 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 74 | A_on | 0.3089 | 0.2839 | 0.3211 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_off | 0.4323 | 0.4268 | 0.4906 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_on | 0.3222 | 0.2995 | 0.3319 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 80 | A_off | 0.4323 | 0.4268 | 0.4906 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 80 | A_on | 0.3222 | 0.2995 | 0.3319 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_off | 0.4393 | 0.4339 | 0.5012 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_on | 0.3267 | 0.3055 | 0.3338 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 79 | A_off | 0.4400 | 0.4344 | 0.5024 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 79 | A_on | 0.3248 | 0.3022 | 0.3269 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_off | 0.4335 | 0.4286 | 0.4949 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_on | 0.2978 | 0.2700 | 0.3173 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 80 | A_off | 0.4335 | 0.4286 | 0.4949 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 80 | A_on | 0.2978 | 0.2700 | 0.3173 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_off | 0.3715 | 0.3257 | 0.4759 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_on | 0.2982 | 0.2865 | 0.4124 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 70 | A_off | 0.3726 | 0.3250 | 0.4763 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 70 | A_on | 0.3241 | 0.3075 | 0.4279 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_off | 0.3673 | 0.3191 | 0.4763 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_on | 0.3634 | 0.3242 | 0.4256 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 74 | A_off | 0.3676 | 0.3197 | 0.4772 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 74 | A_on | 0.3623 | 0.3239 | 0.4256 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_off | 0.3682 | 0.3207 | 0.4767 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_on | 0.3837 | 0.3476 | 0.4556 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 78 | A_off | 0.3682 | 0.3205 | 0.4773 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 78 | A_on | 0.3851 | 0.3576 | 0.4585 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_off | 0.3667 | 0.3204 | 0.4772 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_on | 0.3106 | 0.2972 | 0.4041 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 73 | A_off | 0.3670 | 0.3216 | 0.4763 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 73 | A_on | 0.3043 | 0.2955 | 0.4100 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_off | 0.8136 | 0.7609 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_on | 0.7931 | 0.6763 | 0.8202 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 80 | A_off | 0.8136 | 0.7609 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 80 | A_on | 0.7931 | 0.6763 | 0.8202 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_off | 0.7981 | 0.7515 | 0.8116 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_on | 0.8100 | 0.7020 | 0.8117 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 80 | A_off | 0.7981 | 0.7515 | 0.8116 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 80 | A_on | 0.8100 | 0.7020 | 0.8117 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_off | 0.8108 | 0.7581 | 0.8163 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_on | 0.7933 | 0.6973 | 0.8132 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 77 | A_off | 0.8090 | 0.7587 | 0.8153 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 77 | A_on | 0.7954 | 0.7017 | 0.8142 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_off | 0.8092 | 0.7537 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_on | 0.7920 | 0.6715 | 0.8158 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 80 | A_off | 0.8092 | 0.7537 | 0.8183 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 80 | A_on | 0.7920 | 0.6715 | 0.8158 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_off | 0.9676 | 0.9406 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_on | 0.9687 | 0.9327 | 0.9716 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 78 | A_off | 0.9677 | 0.9406 | 0.9655 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 78 | A_on | 0.9688 | 0.9353 | 0.9716 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_off | 0.9674 | 0.9364 | 0.9625 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_on | 0.9687 | 0.9273 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 72 | A_off | 0.9675 | 0.9358 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 72 | A_on | 0.9688 | 0.9300 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_off | 0.9674 | 0.9491 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_on | 0.9690 | 0.9262 | 0.9748 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 78 | A_off | 0.9674 | 0.9491 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 78 | A_on | 0.9690 | 0.9262 | 0.9748 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_off | 0.9675 | 0.9445 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_on | 0.9682 | 0.9216 | 0.9685 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 76 | A_off | 0.9676 | 0.9443 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 76 | A_on | 0.9685 | 0.9255 | 0.9716 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_off | 0.8315 | 0.8901 | 0.8159 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_on | 0.8613 | 0.9224 | 0.8247 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 78 | A_off | 0.8323 | 0.8910 | 0.8160 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 78 | A_on | 0.8573 | 0.9191 | 0.8194 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_off | 0.8347 | 0.8933 | 0.8141 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_on | 0.8421 | 0.9012 | 0.8035 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 75 | A_off | 0.8325 | 0.8912 | 0.8139 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 75 | A_on | 0.8458 | 0.9085 | 0.8140 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_off | 0.8357 | 0.8942 | 0.8170 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_on | 0.8780 | 0.9331 | 0.8491 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 74 | A_off | 0.8350 | 0.8939 | 0.8164 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 74 | A_on | 0.8681 | 0.9250 | 0.8329 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_off | 0.8386 | 0.8956 | 0.8170 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_on | 0.8561 | 0.9177 | 0.8188 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 78 | A_off | 0.8366 | 0.8943 | 0.8174 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 78 | A_on | 0.8620 | 0.9193 | 0.8288 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_off | 0.4955 | 0.4285 | 0.5432 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_on | 0.3715 | 0.2591 | 0.4668 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 78 | A_off | 0.4967 | 0.4264 | 0.5429 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 78 | A_on | 0.3719 | 0.2559 | 0.4660 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_off | 0.4813 | 0.4147 | 0.5176 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_on | 0.3765 | 0.2705 | 0.4631 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_off | 0.4813 | 0.4147 | 0.5176 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_on | 0.3765 | 0.2705 | 0.4631 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_off | 0.4923 | 0.4290 | 0.5400 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_on | 0.4256 | 0.3680 | 0.4709 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 77 | A_off | 0.4922 | 0.4289 | 0.5400 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 77 | A_on | 0.4215 | 0.3649 | 0.4709 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_off | 0.4694 | 0.3995 | 0.5000 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_on | 0.4677 | 0.4431 | 0.4844 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 80 | A_off | 0.4694 | 0.3995 | 0.5000 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 80 | A_on | 0.4677 | 0.4431 | 0.4844 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_off | 0.0756 | 0.0679 | 0.1108 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_on | 0.0780 | 0.0734 | 0.1340 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 79 | A_off | 0.0757 | 0.0680 | 0.1122 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 79 | A_on | 0.0770 | 0.0730 | 0.1313 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_off | 0.0729 | 0.0650 | 0.1056 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_on | 0.0742 | 0.0717 | 0.1276 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 78 | A_off | 0.0742 | 0.0667 | 0.1090 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 78 | A_on | 0.0710 | 0.0682 | 0.1226 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_off | 0.0758 | 0.0688 | 0.1138 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_on | 0.0644 | 0.0605 | 0.1060 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 75 | A_off | 0.0751 | 0.0681 | 0.1113 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 75 | A_on | 0.0652 | 0.0611 | 0.1039 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_off | 0.0714 | 0.0641 | 0.1068 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_on | 0.0661 | 0.0638 | 0.1123 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 75 | A_off | 0.0722 | 0.0645 | 0.1078 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 75 | A_on | 0.0675 | 0.0645 | 0.1162 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_off | 0.1202 | 0.1023 | 0.1804 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_on | 0.0788 | 0.0769 | 0.1222 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 76 | A_off | 0.1254 | 0.1083 | 0.1867 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 76 | A_on | 0.0774 | 0.0696 | 0.1164 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_off | 0.1282 | 0.1114 | 0.1885 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_on | 0.0776 | 0.0724 | 0.1272 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 79 | A_off | 0.1261 | 0.1089 | 0.1860 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 79 | A_on | 0.0683 | 0.0627 | 0.1064 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_off | 0.1254 | 0.1078 | 0.1876 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_on | 0.0971 | 0.0815 | 0.1343 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 74 | A_off | 0.1295 | 0.1116 | 0.1896 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 74 | A_on | 0.0981 | 0.0863 | 0.1466 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_off | 0.1265 | 0.1102 | 0.1868 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_on | 0.0934 | 0.0879 | 0.1403 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 71 | A_off | 0.1304 | 0.1129 | 0.1907 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 71 | A_on | 0.0956 | 0.0892 | 0.1463 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_off | 0.8838 | 0.8831 | 0.8867 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_on | 0.8867 | 0.8632 | 0.8671 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 75 | A_off | 0.8828 | 0.8822 | 0.8862 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 75 | A_on | 0.8857 | 0.8615 | 0.8684 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_off | 0.8820 | 0.8811 | 0.8875 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_on | 0.8886 | 0.8689 | 0.8683 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 65 | A_off | 0.8826 | 0.8821 | 0.8870 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 65 | A_on | 0.8890 | 0.8679 | 0.8685 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_off | 0.8834 | 0.8825 | 0.8852 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_on | 0.8862 | 0.8865 | 0.8728 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 79 | A_off | 0.8838 | 0.8831 | 0.8849 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 79 | A_on | 0.8865 | 0.8878 | 0.8726 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_off | 0.8859 | 0.8907 | 0.8857 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_on | 0.8900 | 0.8821 | 0.8698 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 78 | A_off | 0.8856 | 0.8906 | 0.8856 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 78 | A_on | 0.8915 | 0.8871 | 0.8713 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_off | 0.2520 | 0.1321 | 0.3459 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_on | 0.2393 | 0.1271 | 0.3624 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 79 | A_off | 0.2523 | 0.1322 | 0.3484 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 79 | A_on | 0.2482 | 0.1320 | 0.3641 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_off | 0.2520 | 0.1318 | 0.3470 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_on | 0.2680 | 0.1404 | 0.3820 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 79 | A_off | 0.2524 | 0.1318 | 0.3469 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 79 | A_on | 0.2651 | 0.1413 | 0.3679 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_off | 0.2510 | 0.1282 | 0.3449 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_on | 0.2793 | 0.1495 | 0.3828 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 79 | A_off | 0.2511 | 0.1287 | 0.3449 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 79 | A_on | 0.2814 | 0.1520 | 0.3880 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_off | 0.2533 | 0.1312 | 0.3464 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_on | 0.2791 | 0.1464 | 0.3895 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 79 | A_off | 0.2534 | 0.1313 | 0.3473 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 79 | A_on | 0.2757 | 0.1431 | 0.3858 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_off | 0.4821 | 0.5503 | 0.4821 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_on | 0.5880 | 0.6575 | 0.5677 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 75 | A_off | 0.4805 | 0.5488 | 0.4816 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 75 | A_on | 0.6158 | 0.6855 | 0.5961 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_off | 0.4899 | 0.5598 | 0.4865 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_on | 0.4996 | 0.5636 | 0.4900 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 76 | A_off | 0.4901 | 0.5595 | 0.4860 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 76 | A_on | 0.5011 | 0.5647 | 0.4910 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_off | 0.4822 | 0.5516 | 0.4839 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_on | 0.5527 | 0.6234 | 0.5293 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 78 | A_off | 0.4814 | 0.5505 | 0.4847 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 78 | A_on | 0.5462 | 0.6124 | 0.5246 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_off | 0.4897 | 0.5591 | 0.4878 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_on | 0.5883 | 0.6602 | 0.5705 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 80 | A_off | 0.4897 | 0.5591 | 0.4878 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 80 | A_on | 0.5883 | 0.6602 | 0.5705 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_off | 0.2331 | 0.2033 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_on | 0.3390 | 0.2629 | 0.3961 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 79 | A_off | 0.2325 | 0.2029 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 79 | A_on | 0.3433 | 0.2676 | 0.3983 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_off | 0.2297 | 0.2009 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_on | 0.3616 | 0.2692 | 0.4183 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 80 | A_off | 0.2297 | 0.2009 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 80 | A_on | 0.3616 | 0.2692 | 0.4183 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_off | 0.2311 | 0.2014 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_on | 0.3276 | 0.2599 | 0.4000 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 74 | A_off | 0.2308 | 0.2014 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 74 | A_on | 0.3281 | 0.2574 | 0.4014 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_off | 0.2357 | 0.2071 | 0.3285 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_on | 0.3170 | 0.2388 | 0.3756 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 79 | A_off | 0.2357 | 0.2070 | 0.3285 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 79 | A_on | 0.3172 | 0.2387 | 0.3705 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_off | 0.3344 | 0.3545 | 0.3290 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_on | 0.4909 | 0.5063 | 0.4613 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 79 | A_off | 0.3337 | 0.3539 | 0.3291 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 79 | A_on | 0.4912 | 0.5070 | 0.4618 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_off | 0.3239 | 0.3452 | 0.3260 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_on | 0.5008 | 0.5171 | 0.4677 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 79 | A_off | 0.3250 | 0.3461 | 0.3275 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 79 | A_on | 0.4988 | 0.5155 | 0.4714 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_off | 0.3304 | 0.3501 | 0.3271 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_on | 0.4943 | 0.5033 | 0.4807 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 73 | A_off | 0.3299 | 0.3499 | 0.3277 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 73 | A_on | 0.4983 | 0.5082 | 0.4842 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_off | 0.3164 | 0.3354 | 0.3184 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_on | 0.4995 | 0.5117 | 0.4810 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 79 | A_off | 0.3174 | 0.3359 | 0.3196 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 79 | A_on | 0.4993 | 0.5123 | 0.4855 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_off | 0.4646 | 0.4073 | 0.5227 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_on | 0.3574 | 0.2361 | 0.4700 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 76 | A_off | 0.4652 | 0.4089 | 0.5235 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 76 | A_on | 0.3579 | 0.2371 | 0.4700 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_off | 0.4682 | 0.4107 | 0.5279 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_on | 0.3430 | 0.1972 | 0.4715 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 78 | A_off | 0.4694 | 0.4129 | 0.5286 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 78 | A_on | 0.3453 | 0.2027 | 0.4715 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_off | 0.4454 | 0.3754 | 0.4831 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_on | 0.3565 | 0.2455 | 0.4726 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 80 | A_off | 0.4454 | 0.3754 | 0.4831 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 80 | A_on | 0.3565 | 0.2455 | 0.4726 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_off | 0.4446 | 0.3751 | 0.4818 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_on | 0.3610 | 0.2482 | 0.4738 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 76 | A_off | 0.4456 | 0.3756 | 0.4818 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 76 | A_on | 0.3631 | 0.2501 | 0.4750 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_off | 0.7910 | 0.8050 | 0.8185 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_on | 0.7838 | 0.5992 | 0.8532 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_off | 0.7917 | 0.8066 | 0.8225 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_on | 0.7812 | 0.6122 | 0.8538 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_off | 0.8026 | 0.8177 | 0.8411 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_on | 0.7716 | 0.6313 | 0.8545 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 76 | A_off | 0.8078 | 0.8234 | 0.8405 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 76 | A_on | 0.7735 | 0.6278 | 0.8555 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_off | 0.6942 | 0.7059 | 0.7157 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_on | 0.7835 | 0.5671 | 0.8551 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 70 | A_off | 0.7337 | 0.7455 | 0.7463 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 70 | A_on | 0.7836 | 0.5703 | 0.8532 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_off | 0.7689 | 0.7807 | 0.7725 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_on | 0.7804 | 0.5863 | 0.8538 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 79 | A_off | 0.7688 | 0.7810 | 0.7741 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 79 | A_on | 0.7793 | 0.5664 | 0.8567 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_off | 0.2228 | 0.2765 | 0.3809 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_on | 0.2226 | 0.2023 | 0.3056 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 78 | A_off | 0.2236 | 0.2788 | 0.3862 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 78 | A_on | 0.2226 | 0.1998 | 0.3056 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_off | 0.2289 | 0.2862 | 0.3862 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_on | 0.2037 | 0.1801 | 0.2988 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_off | 0.2289 | 0.2862 | 0.3862 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_on | 0.2037 | 0.1801 | 0.2988 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_off | 0.2159 | 0.2584 | 0.3543 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_on | 0.1759 | 0.1415 | 0.2671 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 80 | A_off | 0.2159 | 0.2584 | 0.3543 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 80 | A_on | 0.1759 | 0.1415 | 0.2671 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_off | 0.2363 | 0.2954 | 0.4038 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_on | 0.2344 | 0.2287 | 0.3290 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 76 | A_off | 0.2369 | 0.2983 | 0.4056 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 76 | A_on | 0.2367 | 0.2322 | 0.3496 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_off | 0.1557 | 0.1568 | 0.2035 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_on | 0.2160 | 0.2213 | 0.2806 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 77 | A_off | 0.1568 | 0.1576 | 0.2032 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 77 | A_on | 0.2163 | 0.2224 | 0.2827 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_off | 0.1586 | 0.1583 | 0.2020 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_on | 0.2026 | 0.2029 | 0.2715 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 60 | A_off | 0.1575 | 0.1592 | 0.2041 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 60 | A_on | 0.2088 | 0.2093 | 0.2811 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_off | 0.1569 | 0.1587 | 0.2004 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_on | 0.2248 | 0.2302 | 0.2853 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 72 | A_off | 0.1563 | 0.1568 | 0.2008 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 72 | A_on | 0.2184 | 0.2235 | 0.2822 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_off | 0.1559 | 0.1570 | 0.2020 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_on | 0.2089 | 0.2093 | 0.2802 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 71 | A_off | 0.1586 | 0.1598 | 0.2032 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 71 | A_on | 0.2242 | 0.2260 | 0.2887 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_off | 0.1527 | 0.1547 | 0.2350 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_on | 0.1612 | 0.1649 | 0.2352 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 43 | A_off | 0.1610 | 0.1631 | 0.2568 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 43 | A_on | 0.1777 | 0.1828 | 0.2514 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_off | 0.1513 | 0.1532 | 0.2399 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_on | 0.1645 | 0.1692 | 0.2363 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 35 | A_off | 0.1584 | 0.1605 | 0.2517 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 35 | A_on | 0.1815 | 0.1864 | 0.2609 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_off | 0.1503 | 0.1524 | 0.2329 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_on | 0.1558 | 0.1602 | 0.2256 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 50 | A_off | 0.1570 | 0.1592 | 0.2516 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 50 | A_on | 0.1699 | 0.1737 | 0.2482 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_off | 0.1556 | 0.1578 | 0.2400 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_on | 0.1659 | 0.1692 | 0.2437 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 80 | A_off | 0.1556 | 0.1578 | 0.2400 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 80 | A_on | 0.1659 | 0.1692 | 0.2437 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_off | 0.4162 | 0.3650 | 0.4586 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_on | 0.5463 | 0.4860 | 0.5451 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 80 | A_off | 0.4162 | 0.3650 | 0.4586 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 80 | A_on | 0.5463 | 0.4860 | 0.5451 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_off | 0.4060 | 0.3507 | 0.4444 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_on | 0.6047 | 0.5513 | 0.5739 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 79 | A_off | 0.4059 | 0.3482 | 0.4340 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 79 | A_on | 0.6023 | 0.5544 | 0.5720 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_off | 0.4111 | 0.3541 | 0.4319 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_on | 0.5421 | 0.4960 | 0.5487 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 77 | A_off | 0.3869 | 0.3298 | 0.4213 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 77 | A_on | 0.5389 | 0.4933 | 0.5310 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_off | 0.4256 | 0.3684 | 0.4413 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_on | 0.6233 | 0.5655 | 0.5882 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 80 | A_off | 0.4256 | 0.3684 | 0.4413 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 80 | A_on | 0.6233 | 0.5655 | 0.5882 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_off | 0.4023 | 0.3953 | 0.3923 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_on | 0.4207 | 0.4006 | 0.3754 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 73 | A_off | 0.3979 | 0.3910 | 0.3916 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 73 | A_on | 0.4207 | 0.3982 | 0.3774 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_off | 0.3866 | 0.3798 | 0.3850 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_on | 0.4400 | 0.4222 | 0.3954 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 68 | A_off | 0.3874 | 0.3804 | 0.3873 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 68 | A_on | 0.4302 | 0.4084 | 0.3870 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_off | 0.3931 | 0.3864 | 0.3901 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_on | 0.3951 | 0.3531 | 0.3573 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 76 | A_off | 0.3945 | 0.3878 | 0.3907 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 76 | A_on | 0.3979 | 0.3579 | 0.3585 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_off | 0.3981 | 0.3910 | 0.3940 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_on | 0.4434 | 0.4289 | 0.3978 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 45 | A_off | 0.4059 | 0.3984 | 0.3938 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 45 | A_on | 0.4221 | 0.4043 | 0.3834 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_off | 0.4336 | 0.4294 | 0.4944 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_on | 0.3164 | 0.2944 | 0.3198 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 76 | A_off | 0.4322 | 0.4275 | 0.4913 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 76 | A_on | 0.3149 | 0.2932 | 0.3207 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_off | 0.4225 | 0.4173 | 0.4840 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_on | 0.3183 | 0.2982 | 0.3324 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 77 | A_off | 0.4246 | 0.4199 | 0.4863 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 77 | A_on | 0.3186 | 0.2969 | 0.3317 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_off | 0.4346 | 0.4309 | 0.4857 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_on | 0.3266 | 0.3031 | 0.3344 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 79 | A_off | 0.4352 | 0.4301 | 0.4884 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 79 | A_on | 0.3282 | 0.3050 | 0.3336 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_off | 0.4265 | 0.4217 | 0.4923 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_on | 0.3145 | 0.2909 | 0.3187 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 80 | A_off | 0.4265 | 0.4217 | 0.4923 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 80 | A_on | 0.3145 | 0.2909 | 0.3187 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_off | 0.3705 | 0.3225 | 0.4776 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_on | 0.3296 | 0.3114 | 0.4228 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 70 | A_off | 0.3707 | 0.3229 | 0.4776 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 70 | A_on | 0.3459 | 0.3149 | 0.4327 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_off | 0.3679 | 0.3219 | 0.4780 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_on | 0.3773 | 0.3568 | 0.4615 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 74 | A_off | 0.3680 | 0.3219 | 0.4780 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 74 | A_on | 0.3731 | 0.3465 | 0.4594 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_off | 0.3704 | 0.3236 | 0.4755 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_on | 0.3897 | 0.3490 | 0.4762 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 80 | A_off | 0.3704 | 0.3236 | 0.4755 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 80 | A_on | 0.3897 | 0.3490 | 0.4762 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_off | 0.3691 | 0.3223 | 0.4763 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_on | 0.3946 | 0.3589 | 0.4891 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 76 | A_off | 0.3693 | 0.3259 | 0.4772 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 76 | A_on | 0.3953 | 0.3620 | 0.4932 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_off | 0.8089 | 0.7578 | 0.8173 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_on | 0.7924 | 0.6821 | 0.8177 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 75 | A_off | 0.8082 | 0.7592 | 0.8158 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 75 | A_on | 0.7958 | 0.6856 | 0.8234 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_off | 0.8056 | 0.7553 | 0.8188 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_on | 0.7966 | 0.6928 | 0.8158 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 69 | A_off | 0.8075 | 0.7538 | 0.8223 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 69 | A_on | 0.7974 | 0.6945 | 0.8159 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_off | 0.8105 | 0.7590 | 0.8182 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_on | 0.7993 | 0.6881 | 0.8199 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 77 | A_off | 0.8071 | 0.7555 | 0.8157 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 77 | A_on | 0.8001 | 0.6957 | 0.8231 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_off | 0.8090 | 0.7560 | 0.8208 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_on | 0.8068 | 0.6875 | 0.8164 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 80 | A_off | 0.8090 | 0.7560 | 0.8208 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 80 | A_on | 0.8068 | 0.6875 | 0.8164 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_off | 0.9675 | 0.9358 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_on | 0.9686 | 0.9356 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 45 | A_off | 0.9676 | 0.9335 | 0.9655 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 45 | A_on | 0.9688 | 0.9308 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_off | 0.9674 | 0.9401 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_on | 0.9687 | 0.9295 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 72 | A_off | 0.9676 | 0.9381 | 0.9655 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 72 | A_on | 0.9689 | 0.9288 | 0.9748 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_off | 0.9673 | 0.9444 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_on | 0.9690 | 0.9267 | 0.9748 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 78 | A_off | 0.9673 | 0.9444 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 78 | A_on | 0.9691 | 0.9292 | 0.9779 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_off | 0.9675 | 0.9463 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_on | 0.9684 | 0.9301 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 76 | A_off | 0.9675 | 0.9463 | 0.9627 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 76 | A_on | 0.9685 | 0.9276 | 0.9687 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_off | 0.8287 | 0.8876 | 0.8147 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_on | 0.8742 | 0.9273 | 0.8330 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 79 | A_off | 0.8295 | 0.8881 | 0.8153 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 79 | A_on | 0.8734 | 0.9272 | 0.8288 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_off | 0.8348 | 0.8934 | 0.8164 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_on | 0.8755 | 0.9288 | 0.8413 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 78 | A_off | 0.8362 | 0.8947 | 0.8166 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 78 | A_on | 0.8622 | 0.9129 | 0.8224 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_off | 0.8341 | 0.8937 | 0.8179 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_on | 0.8800 | 0.9309 | 0.8255 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 78 | A_off | 0.8337 | 0.8930 | 0.8180 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 78 | A_on | 0.8785 | 0.9302 | 0.8257 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_off | 0.8364 | 0.8942 | 0.8182 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_on | 0.8559 | 0.9143 | 0.8206 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 80 | A_off | 0.8364 | 0.8942 | 0.8182 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 80 | A_on | 0.8559 | 0.9143 | 0.8206 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_off | 0.4903 | 0.4296 | 0.5382 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_on | 0.4254 | 0.3673 | 0.4638 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 80 | A_off | 0.4903 | 0.4296 | 0.5382 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 80 | A_on | 0.4254 | 0.3673 | 0.4638 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_off | 0.4768 | 0.3966 | 0.5119 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_on | 0.3822 | 0.3073 | 0.4748 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_off | 0.4768 | 0.3966 | 0.5119 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_on | 0.3822 | 0.3073 | 0.4748 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_off | 0.4734 | 0.3997 | 0.5077 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_on | 0.4040 | 0.3484 | 0.4657 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 76 | A_off | 0.4732 | 0.3991 | 0.5086 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 76 | A_on | 0.4061 | 0.3494 | 0.4667 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_off | 0.4763 | 0.4052 | 0.5118 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_on | 0.3837 | 0.2839 | 0.4649 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 80 | A_off | 0.4763 | 0.4052 | 0.5118 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 80 | A_on | 0.3837 | 0.2839 | 0.4649 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_off | 0.0736 | 0.0660 | 0.1071 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_on | 0.0839 | 0.0805 | 0.1472 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 78 | A_off | 0.0733 | 0.0656 | 0.1064 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 78 | A_on | 0.0819 | 0.0782 | 0.1437 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_off | 0.0725 | 0.0650 | 0.1039 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_on | 0.0773 | 0.0720 | 0.1231 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 78 | A_off | 0.0737 | 0.0667 | 0.1089 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 78 | A_on | 0.0758 | 0.0708 | 0.1247 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_off | 0.0767 | 0.0703 | 0.1195 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_on | 0.0571 | 0.0542 | 0.0956 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 79 | A_off | 0.0765 | 0.0700 | 0.1194 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 79 | A_on | 0.0577 | 0.0547 | 0.0968 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_off | 0.0759 | 0.0684 | 0.1131 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_on | 0.0667 | 0.0638 | 0.1116 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 75 | A_off | 0.0758 | 0.0683 | 0.1136 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 75 | A_on | 0.0666 | 0.0637 | 0.1139 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_off | 0.1209 | 0.1043 | 0.1796 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_on | 0.1033 | 0.0935 | 0.1348 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 79 | A_off | 0.1280 | 0.1100 | 0.1904 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 79 | A_on | 0.1042 | 0.0967 | 0.1478 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_off | 0.1297 | 0.1120 | 0.1899 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_on | 0.1027 | 0.0917 | 0.1419 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 54 | A_off | 0.1304 | 0.1136 | 0.1914 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 54 | A_on | 0.0981 | 0.0885 | 0.1358 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_off | 0.1242 | 0.1069 | 0.1869 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_on | 0.0827 | 0.0734 | 0.1241 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 79 | A_off | 0.1275 | 0.1100 | 0.1908 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 79 | A_on | 0.0881 | 0.0772 | 0.1287 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_off | 0.1271 | 0.1103 | 0.1885 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_on | 0.0947 | 0.0875 | 0.1330 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 76 | A_off | 0.1295 | 0.1122 | 0.1897 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 76 | A_on | 0.0989 | 0.0905 | 0.1369 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_off | 0.8844 | 0.8838 | 0.8863 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_on | 0.8824 | 0.8587 | 0.8661 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 78 | A_off | 0.8834 | 0.8826 | 0.8865 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 78 | A_on | 0.8824 | 0.8582 | 0.8683 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_off | 0.8825 | 0.8827 | 0.8857 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_on | 0.8878 | 0.8805 | 0.8731 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 74 | A_off | 0.8828 | 0.8828 | 0.8859 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 74 | A_on | 0.8880 | 0.8805 | 0.8738 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_off | 0.8826 | 0.8824 | 0.8863 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_on | 0.8906 | 0.8809 | 0.8720 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 79 | A_off | 0.8829 | 0.8827 | 0.8863 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 79 | A_on | 0.8917 | 0.8837 | 0.8715 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_off | 0.8842 | 0.8891 | 0.8857 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_on | 0.8881 | 0.8836 | 0.8681 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 67 | A_off | 0.8842 | 0.8892 | 0.8857 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 67 | A_on | 0.8892 | 0.8853 | 0.8715 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_off | 0.2503 | 0.1315 | 0.3402 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_on | 0.2437 | 0.1284 | 0.3546 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 79 | A_off | 0.2501 | 0.1314 | 0.3405 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 79 | A_on | 0.2486 | 0.1293 | 0.3565 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_off | 0.2509 | 0.1295 | 0.3450 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_on | 0.2814 | 0.1493 | 0.3909 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 79 | A_off | 0.2512 | 0.1305 | 0.3459 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 79 | A_on | 0.2763 | 0.1397 | 0.3887 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_off | 0.2515 | 0.1297 | 0.3461 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_on | 0.2838 | 0.1573 | 0.4060 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 77 | A_off | 0.2509 | 0.1294 | 0.3449 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 77 | A_on | 0.2846 | 0.1568 | 0.4030 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_off | 0.2536 | 0.1320 | 0.3459 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_on | 0.2685 | 0.1446 | 0.3932 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 77 | A_off | 0.2539 | 0.1312 | 0.3476 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 77 | A_on | 0.2694 | 0.1437 | 0.3848 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_off | 0.4690 | 0.5364 | 0.4733 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_on | 0.5027 | 0.5652 | 0.4766 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 74 | A_off | 0.4677 | 0.5353 | 0.4726 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 74 | A_on | 0.5015 | 0.5631 | 0.4788 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_off | 0.4873 | 0.5569 | 0.4848 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_on | 0.5300 | 0.5930 | 0.5147 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 79 | A_off | 0.4873 | 0.5564 | 0.4854 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 79 | A_on | 0.5377 | 0.6028 | 0.5186 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_off | 0.4790 | 0.5479 | 0.4747 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_on | 0.4633 | 0.5250 | 0.4566 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 78 | A_off | 0.4791 | 0.5481 | 0.4758 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 78 | A_on | 0.4563 | 0.5161 | 0.4544 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_off | 0.4778 | 0.5461 | 0.4828 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_on | 0.4753 | 0.5381 | 0.4512 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 80 | A_off | 0.4778 | 0.5461 | 0.4828 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 80 | A_on | 0.4753 | 0.5381 | 0.4512 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_off | 0.2335 | 0.2041 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_on | 0.3194 | 0.2526 | 0.3750 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 78 | A_off | 0.2334 | 0.2040 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 78 | A_on | 0.3174 | 0.2734 | 0.3616 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_off | 0.2329 | 0.2033 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_on | 0.3319 | 0.2464 | 0.4108 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 78 | A_off | 0.2327 | 0.2031 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 78 | A_on | 0.3372 | 0.2520 | 0.4152 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_off | 0.2324 | 0.2026 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_on | 0.3033 | 0.2482 | 0.3594 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 80 | A_off | 0.2324 | 0.2026 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 80 | A_on | 0.3033 | 0.2482 | 0.3594 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_off | 0.2316 | 0.2021 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_on | 0.3540 | 0.2831 | 0.4170 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 80 | A_off | 0.2316 | 0.2021 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 80 | A_on | 0.3540 | 0.2831 | 0.4170 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_off | 0.3324 | 0.3523 | 0.3221 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_on | 0.5009 | 0.5172 | 0.4682 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 76 | A_off | 0.3294 | 0.3492 | 0.3215 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 76 | A_on | 0.5006 | 0.5177 | 0.4717 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_off | 0.3226 | 0.3416 | 0.3219 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_on | 0.4932 | 0.5085 | 0.4698 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 79 | A_off | 0.3224 | 0.3416 | 0.3219 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 79 | A_on | 0.4889 | 0.5041 | 0.4705 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_off | 0.3273 | 0.3474 | 0.3201 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_on | 0.4691 | 0.4863 | 0.4402 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 75 | A_off | 0.3260 | 0.3464 | 0.3257 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 75 | A_on | 0.4694 | 0.4870 | 0.4413 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_off | 0.3166 | 0.3356 | 0.3215 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_on | 0.4854 | 0.5005 | 0.4577 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 79 | A_off | 0.3161 | 0.3356 | 0.3210 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 79 | A_on | 0.4835 | 0.4982 | 0.4585 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_off | 0.4510 | 0.3858 | 0.4916 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_on | 0.3371 | 0.1726 | 0.4703 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 77 | A_off | 0.4522 | 0.3889 | 0.4916 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 77 | A_on | 0.3376 | 0.1762 | 0.4726 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_off | 0.4411 | 0.3620 | 0.4829 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_on | 0.3519 | 0.2264 | 0.4712 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 78 | A_off | 0.4410 | 0.3625 | 0.4820 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 78 | A_on | 0.3517 | 0.2242 | 0.4712 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_off | 0.4542 | 0.3878 | 0.5009 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_on | 0.3521 | 0.2347 | 0.4724 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 78 | A_off | 0.4558 | 0.3920 | 0.5026 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 78 | A_on | 0.3562 | 0.2403 | 0.4724 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_off | 0.4338 | 0.3517 | 0.4697 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_on | 0.3507 | 0.2277 | 0.4715 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 79 | A_off | 0.4331 | 0.3512 | 0.4697 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 79 | A_on | 0.3509 | 0.2273 | 0.4724 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_off | 0.7997 | 0.8140 | 0.8294 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_on | 0.7880 | 0.6576 | 0.8506 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_off | 0.8004 | 0.8147 | 0.8358 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_on | 0.7884 | 0.6973 | 0.8545 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_off | 0.7827 | 0.7972 | 0.8093 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_on | 0.7902 | 0.6926 | 0.8533 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 80 | A_off | 0.7827 | 0.7972 | 0.8093 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 80 | A_on | 0.7902 | 0.6926 | 0.8533 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_off | 0.7610 | 0.7744 | 0.7656 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_on | 0.7838 | 0.5920 | 0.8526 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 79 | A_off | 0.7759 | 0.7888 | 0.7853 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 79 | A_on | 0.7801 | 0.5717 | 0.8512 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_off | 0.7907 | 0.8042 | 0.7986 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_on | 0.7871 | 0.6693 | 0.8556 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 79 | A_off | 0.7961 | 0.8103 | 0.8169 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 79 | A_on | 0.7867 | 0.6725 | 0.8552 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_off | 0.2297 | 0.2823 | 0.3871 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_on | 0.1047 | 0.0787 | 0.1544 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 78 | A_off | 0.2297 | 0.2813 | 0.3890 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 78 | A_on | 0.1073 | 0.0831 | 0.1602 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_off | 0.2346 | 0.2910 | 0.4067 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_on | 0.2243 | 0.2140 | 0.3316 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_off | 0.2346 | 0.2910 | 0.4067 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_on | 0.2243 | 0.2140 | 0.3316 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_off | 0.2196 | 0.2704 | 0.3592 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_on | 0.1742 | 0.1469 | 0.2534 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 79 | A_off | 0.2197 | 0.2703 | 0.3607 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 79 | A_on | 0.1727 | 0.1431 | 0.2569 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_off | 0.2278 | 0.2768 | 0.3851 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_on | 0.2520 | 0.2381 | 0.3685 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 79 | A_off | 0.2272 | 0.2764 | 0.3780 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 79 | A_on | 0.2515 | 0.2381 | 0.3740 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_off | 0.1578 | 0.1594 | 0.2022 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_on | 0.2222 | 0.2279 | 0.2768 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 52 | A_off | 0.1571 | 0.1584 | 0.2015 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 52 | A_on | 0.2263 | 0.2356 | 0.2755 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_off | 0.1599 | 0.1618 | 0.2031 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_on | 0.2200 | 0.2210 | 0.2879 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 62 | A_off | 0.1608 | 0.1632 | 0.2023 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 62 | A_on | 0.2374 | 0.2447 | 0.3068 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_off | 0.1593 | 0.1613 | 0.2018 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_on | 0.2159 | 0.2267 | 0.2802 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 74 | A_off | 0.1589 | 0.1600 | 0.2018 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 74 | A_on | 0.2205 | 0.2226 | 0.2869 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_off | 0.1605 | 0.1625 | 0.2036 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_on | 0.2487 | 0.2585 | 0.3141 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 45 | A_off | 0.1624 | 0.1635 | 0.2060 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 45 | A_on | 0.2334 | 0.2393 | 0.2768 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_off | 0.1552 | 0.1572 | 0.2428 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_on | 0.1921 | 0.1991 | 0.2623 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 78 | A_off | 0.1544 | 0.1564 | 0.2402 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 78 | A_on | 0.1845 | 0.1911 | 0.2518 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_off | 0.1587 | 0.1609 | 0.2519 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_on | 0.1854 | 0.1924 | 0.2546 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 58 | A_off | 0.1631 | 0.1653 | 0.2622 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 58 | A_on | 0.1882 | 0.1940 | 0.2596 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_off | 0.1549 | 0.1570 | 0.2458 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_on | 0.1847 | 0.1917 | 0.2512 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 80 | A_off | 0.1549 | 0.1570 | 0.2458 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 80 | A_on | 0.1847 | 0.1917 | 0.2512 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_off | 0.1509 | 0.1530 | 0.2315 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_on | 0.1775 | 0.1834 | 0.2382 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 40 | A_off | 0.1592 | 0.1615 | 0.2562 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 40 | A_on | 0.1924 | 0.2003 | 0.2647 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_off | 0.4641 | 0.4079 | 0.4727 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_on | 0.5950 | 0.5653 | 0.5688 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 55 | A_off | 0.4798 | 0.4224 | 0.4701 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 55 | A_on | 0.6256 | 0.5821 | 0.5852 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_off | 0.4493 | 0.3952 | 0.4687 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_on | 0.5657 | 0.5355 | 0.5622 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 49 | A_off | 0.4804 | 0.4286 | 0.4688 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 49 | A_on | 0.6450 | 0.5900 | 0.5806 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_off | 0.4480 | 0.4045 | 0.4693 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_on | 0.6197 | 0.5817 | 0.5808 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 73 | A_off | 0.4423 | 0.3913 | 0.4635 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 73 | A_on | 0.6194 | 0.5904 | 0.5803 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_off | 0.4779 | 0.4229 | 0.4871 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_on | 0.5458 | 0.5056 | 0.5564 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 68 | A_off | 0.4872 | 0.4295 | 0.4810 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 68 | A_on | 0.5313 | 0.4973 | 0.5349 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_off | 0.4025 | 0.3958 | 0.3931 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_on | 0.4728 | 0.4522 | 0.4164 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 66 | A_off | 0.4094 | 0.4018 | 0.3982 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 66 | A_on | 0.4946 | 0.4769 | 0.4415 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_off | 0.3978 | 0.3910 | 0.3867 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_on | 0.4066 | 0.3772 | 0.3571 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 73 | A_off | 0.3989 | 0.3919 | 0.3878 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 73 | A_on | 0.3997 | 0.3696 | 0.3536 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_off | 0.4153 | 0.4079 | 0.3998 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_on | 0.4196 | 0.3832 | 0.3768 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 74 | A_off | 0.4086 | 0.4015 | 0.3944 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 74 | A_on | 0.4070 | 0.3737 | 0.3680 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_off | 0.3892 | 0.3823 | 0.3828 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_on | 0.5010 | 0.4743 | 0.4479 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 54 | A_off | 0.3966 | 0.3898 | 0.3871 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 54 | A_on | 0.4694 | 0.4392 | 0.4298 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_off | 0.4300 | 0.4258 | 0.4889 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_on | 0.3282 | 0.3064 | 0.3467 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 79 | A_off | 0.4278 | 0.4234 | 0.4870 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 79 | A_on | 0.3291 | 0.3074 | 0.3453 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_off | 0.4291 | 0.4253 | 0.4950 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_on | 0.3322 | 0.3143 | 0.3415 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 73 | A_off | 0.4294 | 0.4257 | 0.4946 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 73 | A_on | 0.3308 | 0.3138 | 0.3388 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_off | 0.4233 | 0.4184 | 0.4805 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_on | 0.3226 | 0.3032 | 0.3312 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 78 | A_off | 0.4201 | 0.4156 | 0.4767 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 78 | A_on | 0.3259 | 0.3058 | 0.3340 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_off | 0.4327 | 0.4284 | 0.4962 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_on | 0.3209 | 0.2990 | 0.3289 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 75 | A_off | 0.4309 | 0.4257 | 0.4947 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 75 | A_on | 0.3100 | 0.2875 | 0.3154 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_off | 0.3691 | 0.3226 | 0.4788 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_on | 0.4193 | 0.3805 | 0.4916 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 66 | A_off | 0.3697 | 0.3258 | 0.4803 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 66 | A_on | 0.4242 | 0.3848 | 0.4952 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_off | 0.3684 | 0.3224 | 0.4841 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_on | 0.4159 | 0.3620 | 0.4931 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 76 | A_off | 0.3691 | 0.3233 | 0.4825 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 76 | A_on | 0.4170 | 0.3626 | 0.4949 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_off | 0.3705 | 0.3246 | 0.4850 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_on | 0.4022 | 0.3517 | 0.4785 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 71 | A_off | 0.3704 | 0.3258 | 0.4826 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 71 | A_on | 0.4080 | 0.3575 | 0.4851 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_off | 0.3679 | 0.3233 | 0.4803 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_on | 0.4141 | 0.3719 | 0.4975 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 76 | A_off | 0.3673 | 0.3223 | 0.4803 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 76 | A_on | 0.4156 | 0.3848 | 0.4966 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_off | 0.8236 | 0.7728 | 0.8226 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_on | 0.8103 | 0.6913 | 0.8306 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 80 | A_off | 0.8236 | 0.7728 | 0.8226 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 80 | A_on | 0.8103 | 0.6913 | 0.8306 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_off | 0.8193 | 0.7704 | 0.8287 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_on | 0.8218 | 0.7126 | 0.8287 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 79 | A_off | 0.8197 | 0.7718 | 0.8294 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 79 | A_on | 0.8218 | 0.7118 | 0.8291 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_off | 0.8214 | 0.7673 | 0.8238 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_on | 0.8127 | 0.7065 | 0.8243 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 77 | A_off | 0.8219 | 0.7681 | 0.8244 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 77 | A_on | 0.8097 | 0.7058 | 0.8240 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_off | 0.8195 | 0.7657 | 0.8243 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_on | 0.8218 | 0.6833 | 0.8181 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 79 | A_off | 0.8230 | 0.7710 | 0.8249 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 79 | A_on | 0.8236 | 0.6827 | 0.8193 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_off | 0.9677 | 0.9387 | 0.9685 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_on | 0.9694 | 0.9374 | 0.9781 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 80 | A_off | 0.9677 | 0.9387 | 0.9685 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 80 | A_on | 0.9694 | 0.9374 | 0.9781 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_off | 0.9677 | 0.9359 | 0.9653 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_on | 0.9688 | 0.9323 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 78 | A_off | 0.9677 | 0.9362 | 0.9653 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 78 | A_on | 0.9689 | 0.9313 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_off | 0.9676 | 0.9386 | 0.9653 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_on | 0.9692 | 0.9351 | 0.9748 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 75 | A_off | 0.9677 | 0.9406 | 0.9653 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 75 | A_on | 0.9693 | 0.9325 | 0.9779 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_off | 0.9677 | 0.9386 | 0.9685 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_on | 0.9693 | 0.9302 | 0.9779 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 71 | A_off | 0.9677 | 0.9408 | 0.9685 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 71 | A_on | 0.9693 | 0.9329 | 0.9779 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_off | 0.8308 | 0.8916 | 0.8172 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_on | 0.8546 | 0.8982 | 0.8017 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 80 | A_off | 0.8308 | 0.8916 | 0.8172 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 80 | A_on | 0.8546 | 0.8982 | 0.8017 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_off | 0.8284 | 0.8892 | 0.8147 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_on | 0.8745 | 0.9230 | 0.8429 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 79 | A_off | 0.8314 | 0.8919 | 0.8152 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 79 | A_on | 0.8688 | 0.9140 | 0.8251 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_off | 0.8350 | 0.8949 | 0.8166 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_on | 0.8754 | 0.9296 | 0.8388 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 76 | A_off | 0.8406 | 0.8988 | 0.8173 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 76 | A_on | 0.8727 | 0.9197 | 0.8276 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_off | 0.8197 | 0.8790 | 0.8097 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_on | 0.8808 | 0.9335 | 0.8407 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 78 | A_off | 0.8316 | 0.8902 | 0.8147 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 78 | A_on | 0.8736 | 0.9233 | 0.8289 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_off | 0.4731 | 0.4002 | 0.5059 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_on | 0.3858 | 0.3099 | 0.4668 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 78 | A_off | 0.4726 | 0.4002 | 0.5050 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 78 | A_on | 0.3854 | 0.3036 | 0.4668 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_off | 0.4833 | 0.4108 | 0.5213 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_on | 0.3971 | 0.3425 | 0.4694 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_off | 0.4833 | 0.4108 | 0.5213 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 80 | A_on | 0.3971 | 0.3425 | 0.4694 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_off | 0.4704 | 0.3976 | 0.5008 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_on | 0.4183 | 0.3368 | 0.4645 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 80 | A_off | 0.4704 | 0.3976 | 0.5008 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 80 | A_on | 0.4183 | 0.3368 | 0.4645 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_off | 0.4867 | 0.4171 | 0.5267 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_on | 0.3786 | 0.2622 | 0.4683 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 80 | A_off | 0.4867 | 0.4171 | 0.5267 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 80 | A_on | 0.3786 | 0.2622 | 0.4683 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_off | 0.0745 | 0.0686 | 0.1197 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_on | 0.0853 | 0.0793 | 0.1446 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 74 | A_off | 0.0737 | 0.0677 | 0.1199 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 74 | A_on | 0.0862 | 0.0791 | 0.1372 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_off | 0.0810 | 0.0738 | 0.1340 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_on | 0.0674 | 0.0636 | 0.1128 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 80 | A_off | 0.0810 | 0.0738 | 0.1340 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 80 | A_on | 0.0674 | 0.0636 | 0.1128 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_off | 0.0767 | 0.0705 | 0.1264 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_on | 0.0830 | 0.0765 | 0.1245 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 62 | A_off | 0.0771 | 0.0709 | 0.1289 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 62 | A_on | 0.0802 | 0.0735 | 0.1211 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_off | 0.0748 | 0.0689 | 0.1228 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_on | 0.0666 | 0.0619 | 0.1095 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 80 | A_off | 0.0748 | 0.0689 | 0.1228 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 80 | A_on | 0.0666 | 0.0619 | 0.1095 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_off | 0.1287 | 0.1118 | 0.1848 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_on | 0.0612 | 0.0564 | 0.0994 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 67 | A_off | 0.1297 | 0.1124 | 0.1852 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 67 | A_on | 0.0626 | 0.0568 | 0.1016 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_off | 0.1335 | 0.1175 | 0.1893 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_on | 0.0698 | 0.0625 | 0.1154 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 44 | A_off | 0.1336 | 0.1173 | 0.1924 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 44 | A_on | 0.0665 | 0.0594 | 0.1050 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_off | 0.1285 | 0.1108 | 0.1841 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_on | 0.0816 | 0.0748 | 0.1317 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 71 | A_off | 0.1306 | 0.1142 | 0.1848 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 71 | A_on | 0.0803 | 0.0764 | 0.1270 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_off | 0.1324 | 0.1160 | 0.1886 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_on | 0.0767 | 0.0701 | 0.1282 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 79 | A_off | 0.1325 | 0.1152 | 0.1878 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 79 | A_on | 0.0741 | 0.0688 | 0.1198 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_off | 0.8839 | 0.8833 | 0.8853 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_on | 0.8800 | 0.8455 | 0.8673 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 77 | A_off | 0.8840 | 0.8830 | 0.8849 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 77 | A_on | 0.8699 | 0.8064 | 0.8395 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_off | 0.8849 | 0.8841 | 0.8863 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_on | 0.8860 | 0.8715 | 0.8657 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 79 | A_off | 0.8853 | 0.8904 | 0.8856 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 79 | A_on | 0.8861 | 0.8679 | 0.8663 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_off | 0.8824 | 0.8819 | 0.8859 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_on | 0.8866 | 0.8674 | 0.8690 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 80 | A_off | 0.8824 | 0.8819 | 0.8859 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 80 | A_on | 0.8866 | 0.8674 | 0.8690 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_off | 0.8848 | 0.8840 | 0.8850 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_on | 0.8896 | 0.8785 | 0.8676 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 80 | A_off | 0.8848 | 0.8840 | 0.8850 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 80 | A_on | 0.8896 | 0.8785 | 0.8676 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_off | 0.2513 | 0.1301 | 0.3454 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_on | 0.2820 | 0.1557 | 0.3935 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 57 | A_off | 0.2520 | 0.1296 | 0.3445 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 57 | A_on | 0.2849 | 0.1567 | 0.3965 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_off | 0.2522 | 0.1300 | 0.3474 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_on | 0.3033 | 0.1620 | 0.4269 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 77 | A_off | 0.2522 | 0.1288 | 0.3466 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 77 | A_on | 0.2899 | 0.1572 | 0.4128 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_off | 0.2519 | 0.1301 | 0.3471 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_on | 0.2962 | 0.1569 | 0.4145 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 68 | A_off | 0.2520 | 0.1301 | 0.3476 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 68 | A_on | 0.2903 | 0.1548 | 0.4129 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_off | 0.2516 | 0.1311 | 0.3456 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_on | 0.2849 | 0.1520 | 0.3978 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 80 | A_off | 0.2516 | 0.1311 | 0.3456 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 80 | A_on | 0.2849 | 0.1520 | 0.3978 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_off | 0.4967 | 0.5667 | 0.4901 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_on | 0.5211 | 0.5925 | 0.5197 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 74 | A_off | 0.5001 | 0.5709 | 0.4906 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 74 | A_on | 0.5073 | 0.5759 | 0.4948 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_off | 0.4925 | 0.5637 | 0.4897 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_on | 0.5277 | 0.6018 | 0.5249 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 70 | A_off | 0.4863 | 0.5577 | 0.4876 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 70 | A_on | 0.5299 | 0.6042 | 0.5285 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_off | 0.4869 | 0.5585 | 0.4897 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_on | 0.5137 | 0.5830 | 0.5064 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 79 | A_off | 0.4907 | 0.5626 | 0.4900 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 79 | A_on | 0.5154 | 0.5888 | 0.5083 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_off | 0.4974 | 0.5681 | 0.4898 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_on | 0.5164 | 0.5871 | 0.5157 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 74 | A_off | 0.4968 | 0.5679 | 0.4904 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 74 | A_on | 0.5178 | 0.5909 | 0.5163 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_off | 0.2322 | 0.2034 | 0.3285 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_on | 0.3134 | 0.2411 | 0.3745 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 42 | A_off | 0.2296 | 0.2010 | 0.3285 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 42 | A_on | 0.3075 | 0.2234 | 0.3674 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_off | 0.2273 | 0.1989 | 0.3303 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_on | 0.3223 | 0.2773 | 0.4159 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 38 | A_off | 0.2286 | 0.2001 | 0.3285 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 38 | A_on | 0.3195 | 0.2164 | 0.3935 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_off | 0.2287 | 0.2002 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_on | 0.3419 | 0.2617 | 0.4346 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 78 | A_off | 0.2287 | 0.2000 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 78 | A_on | 0.3424 | 0.2655 | 0.4317 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_off | 0.2303 | 0.2016 | 0.3291 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_on | 0.2959 | 0.2354 | 0.3676 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 77 | A_off | 0.2302 | 0.2014 | 0.3297 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 77 | A_on | 0.3089 | 0.2536 | 0.3708 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_off | 0.3260 | 0.3460 | 0.3278 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_on | 0.5049 | 0.5201 | 0.4644 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 77 | A_off | 0.3284 | 0.3487 | 0.3328 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 77 | A_on | 0.5068 | 0.5219 | 0.4673 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_off | 0.3288 | 0.3474 | 0.3199 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_on | 0.4913 | 0.5040 | 0.4635 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 78 | A_off | 0.3308 | 0.3500 | 0.3240 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 78 | A_on | 0.4901 | 0.5032 | 0.4651 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_off | 0.3384 | 0.3554 | 0.3274 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_on | 0.5061 | 0.5171 | 0.4819 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 75 | A_off | 0.3321 | 0.3489 | 0.3257 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 75 | A_on | 0.5098 | 0.5204 | 0.4866 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_off | 0.3304 | 0.3493 | 0.3258 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_on | 0.4984 | 0.4954 | 0.4699 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 79 | A_off | 0.3316 | 0.3508 | 0.3306 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 79 | A_on | 0.4972 | 0.4993 | 0.4732 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_off | 0.4518 | 0.3849 | 0.4991 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_on | 0.3483 | 0.2123 | 0.4726 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 77 | A_off | 0.4518 | 0.3843 | 0.5000 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 77 | A_on | 0.3474 | 0.2115 | 0.4726 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_off | 0.4455 | 0.3676 | 0.4826 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_on | 0.3935 | 0.3298 | 0.4890 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 80 | A_off | 0.4455 | 0.3676 | 0.4826 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 80 | A_on | 0.3935 | 0.3298 | 0.4890 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_off | 0.4389 | 0.3657 | 0.4697 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_on | 0.3518 | 0.2276 | 0.4741 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 80 | A_off | 0.4389 | 0.3657 | 0.4697 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 80 | A_on | 0.3518 | 0.2276 | 0.4741 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_off | 0.4299 | 0.3483 | 0.4685 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_on | 0.3606 | 0.2539 | 0.4715 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 77 | A_off | 0.4313 | 0.3489 | 0.4685 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 77 | A_on | 0.3582 | 0.2468 | 0.4726 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_off | 0.7805 | 0.7964 | 0.8399 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_on | 0.7817 | 0.6180 | 0.8582 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 73 | A_off | 0.7994 | 0.8153 | 0.8467 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 73 | A_on | 0.7825 | 0.5900 | 0.8567 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_off | 0.8031 | 0.8218 | 0.8491 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_on | 0.7746 | 0.5744 | 0.8529 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 78 | A_off | 0.8068 | 0.8247 | 0.8439 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 78 | A_on | 0.7712 | 0.6164 | 0.8532 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_off | 0.7997 | 0.8149 | 0.8401 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_on | 0.7727 | 0.5638 | 0.8431 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 78 | A_off | 0.7913 | 0.8023 | 0.8170 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 78 | A_on | 0.7758 | 0.5975 | 0.8461 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_off | 0.8111 | 0.8283 | 0.8347 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_on | 0.7857 | 0.6453 | 0.8568 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 65 | A_off | 0.8094 | 0.8266 | 0.8400 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 65 | A_on | 0.7831 | 0.5854 | 0.8581 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_off | 0.2276 | 0.2840 | 0.3744 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_on | 0.1880 | 0.1722 | 0.2727 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 68 | A_off | 0.2278 | 0.2822 | 0.3777 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 68 | A_on | 0.2002 | 0.1794 | 0.2844 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_off | 0.2364 | 0.2985 | 0.3981 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_on | 0.1993 | 0.1739 | 0.2776 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_off | 0.2364 | 0.2985 | 0.3981 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_on | 0.1993 | 0.1739 | 0.2776 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_off | 0.2254 | 0.2713 | 0.3686 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_on | 0.2129 | 0.1909 | 0.3062 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 80 | A_off | 0.2254 | 0.2713 | 0.3686 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 80 | A_on | 0.2129 | 0.1909 | 0.3062 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_off | 0.2244 | 0.2774 | 0.3544 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_on | 0.2133 | 0.1934 | 0.3420 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 77 | A_off | 0.2275 | 0.2801 | 0.3676 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 77 | A_on | 0.2170 | 0.2019 | 0.3392 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_off | 0.1677 | 0.1693 | 0.2109 | 1.0 | False |
| SMD | machine-2-1 | 0 | last | 80 | A_on | 0.2238 | 0.2291 | 0.2798 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 76 | A_off | 0.1641 | 0.1660 | 0.2069 | 1.0 | False |
| SMD | machine-2-1 | 0 | best_val | 76 | A_on | 0.2149 | 0.2194 | 0.2738 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_off | 0.1646 | 0.1665 | 0.2119 | 1.0 | False |
| SMD | machine-2-1 | 1 | last | 80 | A_on | 0.1993 | 0.2040 | 0.2627 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 65 | A_off | 0.1662 | 0.1682 | 0.2105 | 1.0 | False |
| SMD | machine-2-1 | 1 | best_val | 65 | A_on | 0.2154 | 0.2221 | 0.2825 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_off | 0.1717 | 0.1742 | 0.2147 | 1.0 | False |
| SMD | machine-2-1 | 2 | last | 80 | A_on | 0.2008 | 0.2086 | 0.2820 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 80 | A_off | 0.1717 | 0.1742 | 0.2147 | 1.0 | False |
| SMD | machine-2-1 | 2 | best_val | 80 | A_on | 0.2008 | 0.2086 | 0.2820 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_off | 0.1744 | 0.1774 | 0.2151 | 1.0 | False |
| SMD | machine-2-1 | 3 | last | 80 | A_on | 0.1740 | 0.1764 | 0.2394 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 70 | A_off | 0.1757 | 0.1779 | 0.2193 | 1.0 | False |
| SMD | machine-2-1 | 3 | best_val | 70 | A_on | 0.1699 | 0.1721 | 0.2275 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_off | 0.1754 | 0.1783 | 0.2662 | 1.0 | False |
| SMD | machine-2-2 | 0 | last | 80 | A_on | 0.1941 | 0.1985 | 0.2772 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 79 | A_off | 0.1733 | 0.1763 | 0.2638 | 1.0 | False |
| SMD | machine-2-2 | 0 | best_val | 79 | A_on | 0.1944 | 0.1987 | 0.2792 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_off | 0.1769 | 0.1799 | 0.2740 | 1.0 | False |
| SMD | machine-2-2 | 1 | last | 80 | A_on | 0.1703 | 0.1734 | 0.2570 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 79 | A_off | 0.1727 | 0.1755 | 0.2665 | 1.0 | False |
| SMD | machine-2-2 | 1 | best_val | 79 | A_on | 0.1717 | 0.1750 | 0.2564 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_off | 0.1764 | 0.1792 | 0.2718 | 1.0 | False |
| SMD | machine-2-2 | 2 | last | 80 | A_on | 0.1875 | 0.1914 | 0.2599 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 79 | A_off | 0.1717 | 0.1743 | 0.2669 | 1.0 | False |
| SMD | machine-2-2 | 2 | best_val | 79 | A_on | 0.1819 | 0.1854 | 0.2516 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_off | 0.1779 | 0.1808 | 0.2844 | 1.0 | False |
| SMD | machine-2-2 | 3 | last | 80 | A_on | 0.2137 | 0.2183 | 0.2948 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 78 | A_off | 0.1761 | 0.1789 | 0.2830 | 1.0 | False |
| SMD | machine-2-2 | 3 | best_val | 78 | A_on | 0.2088 | 0.2132 | 0.2904 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_off | 0.5627 | 0.5025 | 0.5272 | 1.0 | False |
| SMD | machine-2-3 | 0 | last | 80 | A_on | 0.4119 | 0.3430 | 0.4117 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 58 | A_off | 0.5732 | 0.5137 | 0.5289 | 1.0 | False |
| SMD | machine-2-3 | 0 | best_val | 58 | A_on | 0.4154 | 0.3504 | 0.4623 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_off | 0.4689 | 0.4115 | 0.4709 | 1.0 | False |
| SMD | machine-2-3 | 1 | last | 80 | A_on | 0.5273 | 0.4413 | 0.5155 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 76 | A_off | 0.5076 | 0.4521 | 0.4947 | 1.0 | False |
| SMD | machine-2-3 | 1 | best_val | 76 | A_on | 0.5451 | 0.4653 | 0.5331 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_off | 0.4987 | 0.4405 | 0.4725 | 1.0 | False |
| SMD | machine-2-3 | 2 | last | 80 | A_on | 0.5653 | 0.4846 | 0.5454 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 76 | A_off | 0.5056 | 0.4431 | 0.4894 | 1.0 | False |
| SMD | machine-2-3 | 2 | best_val | 76 | A_on | 0.5852 | 0.4966 | 0.5597 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_off | 0.5116 | 0.4575 | 0.4926 | 1.0 | False |
| SMD | machine-2-3 | 3 | last | 80 | A_on | 0.4971 | 0.4301 | 0.4865 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 79 | A_off | 0.5175 | 0.4615 | 0.4930 | 1.0 | False |
| SMD | machine-2-3 | 3 | best_val | 79 | A_on | 0.4944 | 0.4245 | 0.4780 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_off | 0.4024 | 0.3940 | 0.3920 | 1.0 | False |
| SMD | machine-2-4 | 0 | last | 80 | A_on | 0.3589 | 0.2859 | 0.3263 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 80 | A_off | 0.4024 | 0.3940 | 0.3920 | 1.0 | False |
| SMD | machine-2-4 | 0 | best_val | 80 | A_on | 0.3589 | 0.2859 | 0.3263 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_off | 0.3091 | 0.2902 | 0.3505 | 1.0 | False |
| SMD | machine-2-4 | 1 | last | 80 | A_on | 0.3329 | 0.2315 | 0.3602 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 77 | A_off | 0.3117 | 0.2928 | 0.3496 | 1.0 | False |
| SMD | machine-2-4 | 1 | best_val | 77 | A_on | 0.3695 | 0.2642 | 0.3917 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_off | 0.3732 | 0.3642 | 0.3784 | 1.0 | False |
| SMD | machine-2-4 | 2 | last | 80 | A_on | 0.3550 | 0.3090 | 0.3531 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 75 | A_off | 0.3859 | 0.3775 | 0.3864 | 1.0 | False |
| SMD | machine-2-4 | 2 | best_val | 75 | A_on | 0.3512 | 0.3031 | 0.3487 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_off | 0.3424 | 0.3339 | 0.3715 | 1.0 | False |
| SMD | machine-2-4 | 3 | last | 80 | A_on | 0.3333 | 0.2732 | 0.3279 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 70 | A_off | 0.3532 | 0.3446 | 0.3744 | 1.0 | False |
| SMD | machine-2-4 | 3 | best_val | 70 | A_on | 0.3306 | 0.2740 | 0.3271 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_off | 0.4075 | 0.4017 | 0.4711 | 1.0 | False |
| SMD | machine-2-5 | 0 | last | 80 | A_on | 0.3248 | 0.3039 | 0.3293 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 79 | A_off | 0.4059 | 0.3993 | 0.4678 | 1.0 | False |
| SMD | machine-2-5 | 0 | best_val | 79 | A_on | 0.3312 | 0.3125 | 0.3314 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_off | 0.3854 | 0.3795 | 0.4442 | 1.0 | False |
| SMD | machine-2-5 | 1 | last | 80 | A_on | 0.2973 | 0.2764 | 0.2855 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 76 | A_off | 0.3884 | 0.3837 | 0.4537 | 1.0 | False |
| SMD | machine-2-5 | 1 | best_val | 76 | A_on | 0.3130 | 0.2983 | 0.3243 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_off | 0.3984 | 0.3917 | 0.4616 | 1.0 | False |
| SMD | machine-2-5 | 2 | last | 80 | A_on | 0.3281 | 0.3015 | 0.3273 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 78 | A_off | 0.4026 | 0.3961 | 0.4675 | 1.0 | False |
| SMD | machine-2-5 | 2 | best_val | 78 | A_on | 0.3427 | 0.3152 | 0.3412 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_off | 0.3704 | 0.3612 | 0.4257 | 1.0 | False |
| SMD | machine-2-5 | 3 | last | 80 | A_on | 0.3102 | 0.2789 | 0.3018 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 77 | A_off | 0.3997 | 0.3934 | 0.4580 | 1.0 | False |
| SMD | machine-2-5 | 3 | best_val | 77 | A_on | 0.3267 | 0.2989 | 0.3261 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_off | 0.3689 | 0.3234 | 0.4788 | 1.0 | False |
| SMD | machine-2-6 | 0 | last | 80 | A_on | 0.3637 | 0.2927 | 0.4456 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 75 | A_off | 0.3692 | 0.3223 | 0.4788 | 1.0 | False |
| SMD | machine-2-6 | 0 | best_val | 75 | A_on | 0.3679 | 0.2950 | 0.4499 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_off | 0.3663 | 0.3220 | 0.4791 | 1.0 | False |
| SMD | machine-2-6 | 1 | last | 80 | A_on | 0.3630 | 0.3009 | 0.4295 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 76 | A_off | 0.3662 | 0.3228 | 0.4791 | 1.0 | False |
| SMD | machine-2-6 | 1 | best_val | 76 | A_on | 0.3852 | 0.3301 | 0.4349 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_off | 0.3633 | 0.3152 | 0.4751 | 1.0 | False |
| SMD | machine-2-6 | 2 | last | 80 | A_on | 0.3306 | 0.2378 | 0.4164 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 79 | A_off | 0.3620 | 0.3142 | 0.4738 | 1.0 | False |
| SMD | machine-2-6 | 2 | best_val | 79 | A_on | 0.3266 | 0.2324 | 0.4057 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_off | 0.3729 | 0.3369 | 0.4807 | 1.0 | False |
| SMD | machine-2-6 | 3 | last | 80 | A_on | 0.3730 | 0.3255 | 0.4300 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 79 | A_off | 0.3713 | 0.3359 | 0.4804 | 1.0 | False |
| SMD | machine-2-6 | 3 | best_val | 79 | A_on | 0.3651 | 0.3188 | 0.4283 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_off | 0.8235 | 0.7396 | 0.8285 | 1.0 | False |
| SMD | machine-2-7 | 0 | last | 80 | A_on | 0.7924 | 0.5809 | 0.8306 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 78 | A_off | 0.8229 | 0.7406 | 0.8296 | 1.0 | False |
| SMD | machine-2-7 | 0 | best_val | 78 | A_on | 0.7906 | 0.5793 | 0.8245 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_off | 0.8297 | 0.7611 | 0.8296 | 1.0 | False |
| SMD | machine-2-7 | 1 | last | 80 | A_on | 0.7837 | 0.5989 | 0.8026 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 80 | A_off | 0.8297 | 0.7611 | 0.8296 | 1.0 | False |
| SMD | machine-2-7 | 1 | best_val | 80 | A_on | 0.7837 | 0.5989 | 0.8026 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_off | 0.8310 | 0.7549 | 0.8306 | 1.0 | False |
| SMD | machine-2-7 | 2 | last | 80 | A_on | 0.7964 | 0.6551 | 0.8140 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 79 | A_off | 0.8312 | 0.7547 | 0.8291 | 1.0 | False |
| SMD | machine-2-7 | 2 | best_val | 79 | A_on | 0.7906 | 0.6255 | 0.8114 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_off | 0.8296 | 0.7454 | 0.8289 | 1.0 | False |
| SMD | machine-2-7 | 3 | last | 80 | A_on | 0.7832 | 0.6340 | 0.8162 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 78 | A_off | 0.8302 | 0.7449 | 0.8300 | 1.0 | False |
| SMD | machine-2-7 | 3 | best_val | 78 | A_on | 0.7829 | 0.6207 | 0.8099 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_off | 0.9681 | 0.9494 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 0 | last | 80 | A_on | 0.9694 | 0.9376 | 0.9810 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 79 | A_off | 0.9682 | 0.9494 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 0 | best_val | 79 | A_on | 0.9694 | 0.9377 | 0.9811 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_off | 0.9678 | 0.9421 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 1 | last | 80 | A_on | 0.9693 | 0.9230 | 0.9779 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 80 | A_off | 0.9678 | 0.9421 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 1 | best_val | 80 | A_on | 0.9693 | 0.9230 | 0.9779 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_off | 0.9679 | 0.9511 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 2 | last | 80 | A_on | 0.9662 | 0.9319 | 0.9687 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 7 | A_off | 0.9680 | 0.9427 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 2 | best_val | 7 | A_on | 0.9695 | 0.9329 | 0.9810 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_off | 0.9680 | 0.9445 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 3 | last | 80 | A_on | 0.9653 | 0.9153 | 0.9506 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 77 | A_off | 0.9680 | 0.9427 | 0.9718 | 1.0 | False |
| SMD | machine-2-8 | 3 | best_val | 77 | A_on | 0.9682 | 0.9277 | 0.9748 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_off | 0.8338 | 0.8932 | 0.8107 | 1.0 | False |
| SMD | machine-2-9 | 0 | last | 80 | A_on | 0.7514 | 0.8022 | 0.7211 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 70 | A_off | 0.8317 | 0.8898 | 0.8033 | 1.0 | False |
| SMD | machine-2-9 | 0 | best_val | 70 | A_on | 0.7469 | 0.7973 | 0.7157 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_off | 0.8345 | 0.8925 | 0.8137 | 1.0 | False |
| SMD | machine-2-9 | 1 | last | 80 | A_on | 0.7440 | 0.7944 | 0.7140 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 17 | A_off | 0.8339 | 0.8890 | 0.8061 | 1.0 | False |
| SMD | machine-2-9 | 1 | best_val | 17 | A_on | 0.7006 | 0.7433 | 0.6738 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_off | 0.8320 | 0.8917 | 0.8061 | 1.0 | False |
| SMD | machine-2-9 | 2 | last | 80 | A_on | 0.7709 | 0.8167 | 0.7151 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 65 | A_off | 0.8298 | 0.8881 | 0.8043 | 1.0 | False |
| SMD | machine-2-9 | 2 | best_val | 65 | A_on | 0.7545 | 0.7989 | 0.6980 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_off | 0.8321 | 0.8889 | 0.8115 | 1.0 | False |
| SMD | machine-2-9 | 3 | last | 80 | A_on | 0.7836 | 0.8417 | 0.7571 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 73 | A_off | 0.8354 | 0.8924 | 0.8115 | 1.0 | False |
| SMD | machine-2-9 | 3 | best_val | 73 | A_on | 0.7723 | 0.8279 | 0.7366 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_off | 0.4169 | 0.3020 | 0.4686 | 1.0 | False |
| SMD | machine-3-1 | 0 | last | 80 | A_on | 0.3683 | 0.1923 | 0.4657 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 80 | A_off | 0.4169 | 0.3020 | 0.4686 | 1.0 | False |
| SMD | machine-3-1 | 0 | best_val | 80 | A_on | 0.3683 | 0.1923 | 0.4657 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_off | 0.4217 | 0.3157 | 0.4678 | 1.0 | False |
| SMD | machine-3-1 | 1 | last | 80 | A_on | 0.3844 | 0.2608 | 0.4645 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 77 | A_off | 0.4200 | 0.3131 | 0.4678 | 1.0 | False |
| SMD | machine-3-1 | 1 | best_val | 77 | A_on | 0.3900 | 0.2750 | 0.4652 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_off | 0.4167 | 0.3003 | 0.4657 | 1.0 | False |
| SMD | machine-3-1 | 2 | last | 80 | A_on | 0.3843 | 0.2802 | 0.4623 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 79 | A_off | 0.4184 | 0.3019 | 0.4657 | 1.0 | False |
| SMD | machine-3-1 | 2 | best_val | 79 | A_on | 0.3867 | 0.2836 | 0.4623 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_off | 0.4165 | 0.3060 | 0.4723 | 1.0 | False |
| SMD | machine-3-1 | 3 | last | 80 | A_on | 0.3829 | 0.2678 | 0.4683 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 79 | A_off | 0.4174 | 0.3077 | 0.4723 | 1.0 | False |
| SMD | machine-3-1 | 3 | best_val | 79 | A_on | 0.3749 | 0.2716 | 0.4734 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_off | 0.0675 | 0.0615 | 0.1146 | 1.0 | False |
| SMD | machine-3-2 | 0 | last | 80 | A_on | 0.0638 | 0.0590 | 0.1016 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 77 | A_off | 0.0672 | 0.0608 | 0.1145 | 1.0 | False |
| SMD | machine-3-2 | 0 | best_val | 77 | A_on | 0.0607 | 0.0556 | 0.0986 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_off | 0.0730 | 0.0664 | 0.1276 | 1.0 | False |
| SMD | machine-3-2 | 1 | last | 80 | A_on | 0.0443 | 0.0432 | 0.0918 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 79 | A_off | 0.0742 | 0.0677 | 0.1294 | 1.0 | False |
| SMD | machine-3-2 | 1 | best_val | 79 | A_on | 0.0438 | 0.0424 | 0.0924 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_off | 0.0586 | 0.0540 | 0.1155 | 1.0 | False |
| SMD | machine-3-2 | 2 | last | 80 | A_on | 0.0457 | 0.0450 | 0.1098 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 9 | A_off | 0.0805 | 0.0724 | 0.1368 | 1.0 | False |
| SMD | machine-3-2 | 2 | best_val | 9 | A_on | 0.0675 | 0.0629 | 0.1048 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_off | 0.0694 | 0.0631 | 0.1203 | 1.0 | False |
| SMD | machine-3-2 | 3 | last | 80 | A_on | 0.0907 | 0.0830 | 0.1726 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 80 | A_off | 0.0694 | 0.0631 | 0.1203 | 1.0 | False |
| SMD | machine-3-2 | 3 | best_val | 80 | A_on | 0.0907 | 0.0830 | 0.1726 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_off | 0.1327 | 0.1145 | 0.2013 | 1.0 | False |
| SMD | machine-3-3 | 0 | last | 80 | A_on | 0.0678 | 0.0647 | 0.1289 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 77 | A_off | 0.1345 | 0.1161 | 0.2042 | 1.0 | False |
| SMD | machine-3-3 | 0 | best_val | 77 | A_on | 0.0741 | 0.0703 | 0.1443 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_off | 0.1533 | 0.1360 | 0.2274 | 1.0 | False |
| SMD | machine-3-3 | 1 | last | 80 | A_on | 0.1096 | 0.1039 | 0.1935 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 80 | A_off | 0.1533 | 0.1360 | 0.2274 | 1.0 | False |
| SMD | machine-3-3 | 1 | best_val | 80 | A_on | 0.1096 | 0.1039 | 0.1935 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_off | 0.1340 | 0.1141 | 0.1968 | 1.0 | False |
| SMD | machine-3-3 | 2 | last | 80 | A_on | 0.0774 | 0.0709 | 0.1522 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 78 | A_off | 0.1344 | 0.1143 | 0.1982 | 1.0 | False |
| SMD | machine-3-3 | 2 | best_val | 78 | A_on | 0.0786 | 0.0726 | 0.1531 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_off | 0.1366 | 0.1197 | 0.2100 | 1.0 | False |
| SMD | machine-3-3 | 3 | last | 80 | A_on | 0.1111 | 0.1095 | 0.1906 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 79 | A_off | 0.1398 | 0.1234 | 0.2143 | 1.0 | False |
| SMD | machine-3-3 | 3 | best_val | 79 | A_on | 0.1093 | 0.1084 | 0.1855 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_off | 0.8845 | 0.8813 | 0.8801 | 1.0 | False |
| SMD | machine-3-4 | 0 | last | 80 | A_on | 0.8791 | 0.8653 | 0.8556 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 80 | A_off | 0.8845 | 0.8813 | 0.8801 | 1.0 | False |
| SMD | machine-3-4 | 0 | best_val | 80 | A_on | 0.8791 | 0.8653 | 0.8556 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_off | 0.9075 | 0.9114 | 0.8869 | 1.0 | False |
| SMD | machine-3-4 | 1 | last | 80 | A_on | 0.7929 | 0.6551 | 0.7265 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 77 | A_off | 0.8964 | 0.8989 | 0.8840 | 1.0 | False |
| SMD | machine-3-4 | 1 | best_val | 77 | A_on | 0.8833 | 0.8428 | 0.8106 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_off | 0.8863 | 0.8837 | 0.8811 | 1.0 | False |
| SMD | machine-3-4 | 2 | last | 80 | A_on | 0.8751 | 0.8590 | 0.8503 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 78 | A_off | 0.8855 | 0.8829 | 0.8811 | 1.0 | False |
| SMD | machine-3-4 | 2 | best_val | 78 | A_on | 0.8731 | 0.8586 | 0.8514 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_off | 0.8814 | 0.8786 | 0.8808 | 1.0 | False |
| SMD | machine-3-4 | 3 | last | 80 | A_on | 0.8380 | 0.7933 | 0.8027 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 77 | A_off | 0.8816 | 0.8782 | 0.8807 | 1.0 | False |
| SMD | machine-3-4 | 3 | best_val | 77 | A_on | 0.8408 | 0.7958 | 0.8045 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_off | 0.2560 | 0.1339 | 0.3455 | 1.0 | False |
| SMD | machine-3-5 | 0 | last | 80 | A_on | 0.2491 | 0.1325 | 0.3478 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 80 | A_off | 0.2560 | 0.1339 | 0.3455 | 1.0 | False |
| SMD | machine-3-5 | 0 | best_val | 80 | A_on | 0.2491 | 0.1325 | 0.3478 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_off | 0.2516 | 0.1295 | 0.3479 | 1.0 | False |
| SMD | machine-3-5 | 1 | last | 80 | A_on | 0.2480 | 0.1305 | 0.3595 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 77 | A_off | 0.2520 | 0.1303 | 0.3493 | 1.0 | False |
| SMD | machine-3-5 | 1 | best_val | 77 | A_on | 0.2447 | 0.1265 | 0.3566 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_off | 0.2581 | 0.1333 | 0.3467 | 1.0 | False |
| SMD | machine-3-5 | 2 | last | 80 | A_on | 0.2969 | 0.1722 | 0.3478 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 63 | A_off | 0.2583 | 0.1344 | 0.3465 | 1.0 | False |
| SMD | machine-3-5 | 2 | best_val | 63 | A_on | 0.2561 | 0.1392 | 0.3333 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_off | 0.2521 | 0.1294 | 0.3457 | 1.0 | False |
| SMD | machine-3-5 | 3 | last | 80 | A_on | 0.2523 | 0.1305 | 0.3486 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 78 | A_off | 0.2520 | 0.1292 | 0.3452 | 1.0 | False |
| SMD | machine-3-5 | 3 | best_val | 78 | A_on | 0.2563 | 0.1338 | 0.3599 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_off | 0.4817 | 0.5529 | 0.4858 | 1.0 | False |
| SMD | machine-3-6 | 0 | last | 80 | A_on | 0.3799 | 0.4261 | 0.3559 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 75 | A_off | 0.4785 | 0.5493 | 0.4855 | 1.0 | False |
| SMD | machine-3-6 | 0 | best_val | 75 | A_on | 0.3575 | 0.4051 | 0.3416 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_off | 0.4724 | 0.5428 | 0.4826 | 1.0 | False |
| SMD | machine-3-6 | 1 | last | 80 | A_on | 0.6343 | 0.7242 | 0.6101 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 79 | A_off | 0.4723 | 0.5428 | 0.4811 | 1.0 | False |
| SMD | machine-3-6 | 1 | best_val | 79 | A_on | 0.6242 | 0.7146 | 0.5942 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_off | 0.4887 | 0.5607 | 0.4880 | 1.0 | False |
| SMD | machine-3-6 | 2 | last | 80 | A_on | 0.5245 | 0.6166 | 0.5151 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 76 | A_off | 0.4868 | 0.5589 | 0.4871 | 1.0 | False |
| SMD | machine-3-6 | 2 | best_val | 76 | A_on | 0.5443 | 0.6368 | 0.5257 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_off | 0.5110 | 0.5835 | 0.4957 | 1.0 | False |
| SMD | machine-3-6 | 3 | last | 80 | A_on | 0.3800 | 0.4306 | 0.3762 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 63 | A_off | 0.5079 | 0.5813 | 0.4957 | 1.0 | False |
| SMD | machine-3-6 | 3 | best_val | 63 | A_on | 0.4263 | 0.4835 | 0.4318 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_off | 0.2199 | 0.1575 | 0.3198 | 1.0 | False |
| SMD | machine-3-7 | 0 | last | 80 | A_on | 0.2387 | 0.1439 | 0.2838 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 58 | A_off | 0.2235 | 0.1751 | 0.3225 | 1.0 | False |
| SMD | machine-3-7 | 0 | best_val | 58 | A_on | 0.2249 | 0.1290 | 0.2897 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_off | 0.2269 | 0.1961 | 0.3248 | 1.0 | False |
| SMD | machine-3-7 | 1 | last | 80 | A_on | 0.2228 | 0.1280 | 0.2669 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 80 | A_off | 0.2269 | 0.1961 | 0.3248 | 1.0 | False |
| SMD | machine-3-7 | 1 | best_val | 80 | A_on | 0.2228 | 0.1280 | 0.2669 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_off | 0.2296 | 0.1806 | 0.3219 | 1.0 | False |
| SMD | machine-3-7 | 2 | last | 80 | A_on | 0.2752 | 0.1886 | 0.3368 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 77 | A_off | 0.2317 | 0.1828 | 0.3225 | 1.0 | False |
| SMD | machine-3-7 | 2 | best_val | 77 | A_on | 0.2629 | 0.1740 | 0.3226 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_off | 0.2381 | 0.2085 | 0.3285 | 1.0 | False |
| SMD | machine-3-7 | 3 | last | 80 | A_on | 0.2714 | 0.1606 | 0.3088 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 75 | A_off | 0.2412 | 0.2108 | 0.3279 | 1.0 | False |
| SMD | machine-3-7 | 3 | best_val | 75 | A_on | 0.2514 | 0.1495 | 0.2975 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_off | 0.4559 | 0.4759 | 0.4270 | 1.0 | False |
| SMD | machine-3-8 | 0 | last | 80 | A_on | 0.3622 | 0.3747 | 0.4127 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 80 | A_off | 0.4559 | 0.4759 | 0.4270 | 1.0 | False |
| SMD | machine-3-8 | 0 | best_val | 80 | A_on | 0.3622 | 0.3747 | 0.4127 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_off | 0.4045 | 0.4241 | 0.3875 | 1.0 | False |
| SMD | machine-3-8 | 1 | last | 80 | A_on | 0.4985 | 0.5208 | 0.4612 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 50 | A_off | 0.3942 | 0.4173 | 0.3680 | 1.0 | False |
| SMD | machine-3-8 | 1 | best_val | 50 | A_on | 0.4778 | 0.4954 | 0.4501 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_off | 0.4329 | 0.4540 | 0.4085 | 1.0 | False |
| SMD | machine-3-8 | 2 | last | 80 | A_on | 0.5304 | 0.5426 | 0.4838 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 66 | A_off | 0.4247 | 0.4464 | 0.4050 | 1.0 | False |
| SMD | machine-3-8 | 2 | best_val | 66 | A_on | 0.5176 | 0.5296 | 0.4851 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_off | 0.4073 | 0.4291 | 0.3893 | 1.0 | False |
| SMD | machine-3-8 | 3 | last | 80 | A_on | 0.4443 | 0.4596 | 0.4073 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 78 | A_off | 0.3940 | 0.4161 | 0.3773 | 1.0 | False |
| SMD | machine-3-8 | 3 | best_val | 78 | A_on | 0.5059 | 0.5153 | 0.4575 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_off | 0.3803 | 0.2640 | 0.4688 | 1.0 | False |
| SMD | machine-3-9 | 0 | last | 80 | A_on | 0.3494 | 0.2316 | 0.4697 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 76 | A_off | 0.3806 | 0.2644 | 0.4688 | 1.0 | False |
| SMD | machine-3-9 | 0 | best_val | 76 | A_on | 0.3496 | 0.2316 | 0.4700 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_off | 0.3924 | 0.2844 | 0.4673 | 1.0 | False |
| SMD | machine-3-9 | 1 | last | 80 | A_on | 0.3595 | 0.2799 | 0.4658 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 80 | A_off | 0.3924 | 0.2844 | 0.4673 | 1.0 | False |
| SMD | machine-3-9 | 1 | best_val | 80 | A_on | 0.3595 | 0.2799 | 0.4658 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_off | 0.3845 | 0.2774 | 0.4691 | 1.0 | False |
| SMD | machine-3-9 | 2 | last | 80 | A_on | 0.3741 | 0.2675 | 0.4738 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 79 | A_off | 0.3840 | 0.2769 | 0.4691 | 1.0 | False |
| SMD | machine-3-9 | 2 | best_val | 79 | A_on | 0.3753 | 0.2570 | 0.4738 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_off | 0.3885 | 0.2792 | 0.4677 | 1.0 | False |
| SMD | machine-3-9 | 3 | last | 80 | A_on | 0.3694 | 0.3063 | 0.4685 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 79 | A_off | 0.3879 | 0.2775 | 0.4677 | 1.0 | False |
| SMD | machine-3-9 | 3 | best_val | 79 | A_on | 0.3686 | 0.3066 | 0.4673 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_off | 0.7977 | 0.8067 | 0.8683 | 1.0 | False |
| SMD | machine-3-10 | 0 | last | 80 | A_on | 0.7320 | 0.5637 | 0.7644 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_off | 0.8005 | 0.8097 | 0.8692 | 1.0 | False |
| SMD | machine-3-10 | 0 | best_val | 75 | A_on | 0.7727 | 0.7174 | 0.8335 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_off | 0.7873 | 0.7990 | 0.8419 | 1.0 | False |
| SMD | machine-3-10 | 1 | last | 80 | A_on | 0.7172 | 0.6245 | 0.7244 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 73 | A_off | 0.7812 | 0.7904 | 0.8388 | 1.0 | False |
| SMD | machine-3-10 | 1 | best_val | 73 | A_on | 0.6741 | 0.5675 | 0.6937 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_off | 0.5708 | 0.5574 | 0.6020 | 1.0 | False |
| SMD | machine-3-10 | 2 | last | 80 | A_on | 0.2136 | 0.1577 | 0.3590 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 26 | A_off | 0.6862 | 0.6665 | 0.7424 | 1.0 | False |
| SMD | machine-3-10 | 2 | best_val | 26 | A_on | 0.6497 | 0.3361 | 0.6723 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_off | 0.6945 | 0.6820 | 0.7091 | 1.0 | False |
| SMD | machine-3-10 | 3 | last | 80 | A_on | 0.6571 | 0.3785 | 0.6343 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 78 | A_off | 0.6417 | 0.6245 | 0.6438 | 1.0 | False |
| SMD | machine-3-10 | 3 | best_val | 78 | A_on | 0.5241 | 0.2980 | 0.5671 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_off | 0.2337 | 0.2723 | 0.3402 | 1.0 | False |
| SMD | machine-3-11 | 0 | last | 80 | A_on | 0.2064 | 0.1787 | 0.3052 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 77 | A_off | 0.2366 | 0.2744 | 0.3511 | 1.0 | False |
| SMD | machine-3-11 | 0 | best_val | 77 | A_on | 0.2043 | 0.1760 | 0.3064 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_off | 0.2129 | 0.2671 | 0.3048 | 1.0 | False |
| SMD | machine-3-11 | 1 | last | 80 | A_on | 0.1867 | 0.1993 | 0.2649 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_off | 0.2129 | 0.2671 | 0.3048 | 1.0 | False |
| SMD | machine-3-11 | 1 | best_val | 80 | A_on | 0.1867 | 0.1993 | 0.2649 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_off | 0.2300 | 0.2774 | 0.3464 | 1.0 | False |
| SMD | machine-3-11 | 2 | last | 80 | A_on | 0.2063 | 0.1904 | 0.3421 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 80 | A_off | 0.2300 | 0.2774 | 0.3464 | 1.0 | False |
| SMD | machine-3-11 | 2 | best_val | 80 | A_on | 0.2063 | 0.1904 | 0.3421 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_off | 0.2301 | 0.2520 | 0.3680 | 1.0 | False |
| SMD | machine-3-11 | 3 | last | 80 | A_on | 0.2038 | 0.1747 | 0.3371 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 72 | A_off | 0.2315 | 0.2533 | 0.3741 | 1.0 | False |
| SMD | machine-3-11 | 3 | best_val | 72 | A_on | 0.2082 | 0.1775 | 0.3427 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SMD/machine-2-1/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.262912434524565 | 79 / 0.2606784778534272 | 1216 |
| train/SMD/machine-2-1/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2753837126174439 | 49 / 0.2640948533189433 | 1216 |
| train/SMD/machine-2-1/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2617679204162957 | 76 / 0.2605599459092821 | 1215 |
| train/SMD/machine-2-1/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.263255675950331 | 74 / 0.2625122939623727 | 1167 |
| train/SMD/machine-2-2/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2059546237668819 | 45 / 0.2015579573830076 | 1164 |
| train/SMD/machine-2-2/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1952252484281395 | 80 / 0.1952252484281395 | 1209 |
| train/SMD/machine-2-2/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2185964401125102 | 31 / 0.2060793703809133 | 1030 |
| train/SMD/machine-2-2/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.218235699246084 | 35 / 0.2086015549005666 | 1163 |
| train/SMD/machine-2-3/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1123876835199733 | 71 / 0.112254690855164 | 1152 |
| train/SMD/machine-2-3/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.112748487964406 | 79 / 0.11250697280689 | 1197 |
| train/SMD/machine-2-3/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1132939466656516 | 75 / 0.1130927889851584 | 1197 |
| train/SMD/machine-2-3/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1121604077025349 | 80 / 0.1121604077025349 | 1150 |
| train/SMD/machine-2-4/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1550815990403122 | 76 / 0.1534505825584248 | 1141 |
| train/SMD/machine-2-4/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1558101961560188 | 78 / 0.1551721936318965 | 1185 |
| train/SMD/machine-2-4/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1564066952358105 | 79 / 0.1558511768843783 | 1142 |
| train/SMD/machine-2-4/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1563188161180341 | 76 / 0.1549873019621764 | 1187 |
| train/SMD/machine-2-5/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1137666958809758 | 74 / 0.1133318158923784 | 1174 |
| train/SMD/machine-2-5/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1112088900565241 | 80 / 0.1112088900565241 | 1175 |
| train/SMD/machine-2-5/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1158860792037825 | 79 / 0.1152592568236667 | 1175 |
| train/SMD/machine-2-5/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1112602894414259 | 80 / 0.1112602894414259 | 1175 |
| train/SMD/machine-2-6/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1195981878983347 | 70 / 0.1188943687675415 | 1461 |
| train/SMD/machine-2-6/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.123064407916675 | 74 / 0.1208358596754187 | 1463 |
| train/SMD/machine-2-6/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.119661222535187 | 78 / 0.1191262072212167 | 1419 |
| train/SMD/machine-2-6/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1213224484114696 | 73 / 0.1207571910058557 | 1418 |
| train/SMD/machine-2-7/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1075959630626399 | 80 / 0.1075959630626399 | 1190 |
| train/SMD/machine-2-7/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1085503606731533 | 80 / 0.1085503606731533 | 1190 |
| train/SMD/machine-2-7/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1085498609889849 | 77 / 0.1084147435374316 | 1146 |
| train/SMD/machine-2-7/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1074231339731934 | 80 / 0.1074231339731934 | 1188 |
| train/SMD/machine-2-8/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1902729247419473 | 78 / 0.1884858112385918 | 1168 |
| train/SMD/machine-2-8/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1906247584097209 | 72 / 0.1835006467557818 | 1208 |
| train/SMD/machine-2-8/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1874942223392792 | 78 / 0.1853548399254045 | 1166 |
| train/SMD/machine-2-8/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1939790058563547 | 76 / 0.1872759382567927 | 1209 |
| train/SMD/machine-2-9/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1298937309397118 | 78 / 0.1295627357161882 | 1410 |
| train/SMD/machine-2-9/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1310345159031856 | 75 / 0.1301723358570197 | 1410 |
| train/SMD/machine-2-9/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1314575055278644 | 74 / 0.1309516651526579 | 1412 |
| train/SMD/machine-2-9/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1323600517332113 | 78 / 0.131012565596339 | 1412 |
| train/SMD/machine-3-1/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.128187900419862 | 78 / 0.1281290050730417 | 1387 |
| train/SMD/machine-3-1/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1286320830982411 | 80 / 0.1286320830982411 | 1387 |
| train/SMD/machine-3-1/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1301741093679867 | 77 / 0.1296576134624659 | 1302 |
| train/SMD/machine-3-1/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1256375309258094 | 80 / 0.1256375309258094 | 1384 |
| train/SMD/machine-3-2/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.229377913532593 | 79 / 0.2286471416417922 | 1216 |
| train/SMD/machine-3-2/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2299003990229442 | 78 / 0.2267520261480044 | 1216 |
| train/SMD/machine-3-2/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2324487412242025 | 75 / 0.2312281555672134 | 1174 |
| train/SMD/machine-3-2/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2313806820078096 | 75 / 0.2307476862794408 | 1174 |
| train/SMD/machine-3-3/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1281235912927355 | 76 / 0.1186515813875798 | 1195 |
| train/SMD/machine-3-3/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1203766649832328 | 79 / 0.119254068329744 | 1195 |
| train/SMD/machine-3-3/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.121049533658495 | 74 / 0.1189749785131919 | 1195 |
| train/SMD/machine-3-3/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1201199857706106 | 71 / 0.1185156276611404 | 1195 |
| train/SMD/machine-3-4/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2764637177875263 | 75 / 0.2762021074864921 | 1184 |
| train/SMD/machine-3-4/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2781879256208812 | 65 / 0.2766551198576318 | 1184 |
| train/SMD/machine-3-4/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.2766869127384138 | 79 / 0.2755560569617105 | 1183 |
| train/SMD/machine-3-4/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.276531123342131 | 78 / 0.2762282644399754 | 1141 |
| train/SMD/machine-3-5/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1214621075034119 | 79 / 0.120962124072727 | 1167 |
| train/SMD/machine-3-5/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1207880897130105 | 79 / 0.1200418376021482 | 1123 |
| train/SMD/machine-3-5/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1214614037558534 | 79 / 0.1205629871237347 | 1163 |
| train/SMD/machine-3-5/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1208055463546072 | 79 / 0.1201925959868738 | 1163 |
| train/SMD/machine-3-6/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1264101667025449 | 75 / 0.1258539075080688 | 1423 |
| train/SMD/machine-3-6/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1280707654943902 | 76 / 0.1274809930797611 | 1423 |
| train/SMD/machine-3-6/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1266662977361857 | 78 / 0.1258495705755833 | 1421 |
| train/SMD/machine-3-6/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1277258964762029 | 80 / 0.1277258964762029 | 1420 |
| train/SMD/machine-3-7/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.0673812870834473 | 79 / 0.0659719416654459 | 1397 |
| train/SMD/machine-3-7/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.0672117125323811 | 80 / 0.0672117125323811 | 1397 |
| train/SMD/machine-3-7/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.065248312144343 | 74 / 0.0650472890031663 | 1396 |
| train/SMD/machine-3-7/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.0658567885828538 | 79 / 0.0656253185476072 | 1282 |
| train/SMD/machine-3-8/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1035438434198582 | 79 / 0.1012984571549029 | 1377 |
| train/SMD/machine-3-8/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1056165128807291 | 79 / 0.1049389230581947 | 1413 |
| train/SMD/machine-3-8/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1034694086963738 | 73 / 0.1030248935562298 | 1413 |
| train/SMD/machine-3-8/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1039788836741432 | 79 / 0.1037407981997814 | 1414 |
| train/SMD/machine-3-9/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1199961452152542 | 76 / 0.1194242679416042 | 1391 |
| train/SMD/machine-3-9/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1165208577553885 | 78 / 0.1161179522495663 | 1429 |
| train/SMD/machine-3-9/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1190069794311265 | 80 / 0.1190069794311265 | 1391 |
| train/SMD/machine-3-9/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1208953089902516 | 76 / 0.1195581303206907 | 1429 |
| train/SMD/machine-3-10/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1013516148436021 | 75 / 0.0983009471265601 | 1200 |
| train/SMD/machine-3-10/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1033336247409774 | 76 / 0.0984999461836905 | 1163 |
| train/SMD/machine-3-10/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1052306272317764 | 70 / 0.0978828872820088 | 1199 |
| train/SMD/machine-3-10/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1004266371754957 | 79 / 0.0991557132389664 | 1162 |
| train/SMD/machine-3-11/seed0/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1140638979164334 | 78 / 0.1139635907549213 | 1394 |
| train/SMD/machine-3-11/seed1/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1131655475374335 | 80 / 0.1131655475374335 | 1394 |
| train/SMD/machine-3-11/seed2/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1131576256372279 | 80 / 0.1131576256372279 | 1394 |
| train/SMD/machine-3-11/seed3/smd_cf_val_perm0_crsoff | 80 | 80 / 0.1126965366229326 | 76 / 0.1123061456835345 | 1392 |
| train/SMD/machine-2-1/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.2677004262232947 | 77 / 0.2637892625774121 | 1202 |
| train/SMD/machine-2-1/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.2676892976812862 | 60 / 0.2640355730847335 | 1238 |
| train/SMD/machine-2-1/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.2645138002070699 | 72 / 0.263298892263869 | 1166 |
| train/SMD/machine-2-1/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.2653082875079542 | 71 / 0.2632791976105242 | 1202 |
| train/SMD/machine-2-2/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.2031629778153255 | 43 / 0.1994856220431196 | 1184 |
| train/SMD/machine-2-2/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.2080781873816248 | 35 / 0.2053817920302661 | 1184 |
| train/SMD/machine-2-2/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.2085786004290274 | 50 / 0.2057949966226792 | 1183 |
| train/SMD/machine-2-2/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.2051570336270636 | 80 / 0.2051570336270636 | 1218 |
| train/SMD/machine-2-3/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1128886125265282 | 80 / 0.1128886125265282 | 1166 |
| train/SMD/machine-2-3/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1132928506263798 | 79 / 0.1126326386172924 | 1166 |
| train/SMD/machine-2-3/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1133425242673895 | 77 / 0.1130053622765267 | 1166 |
| train/SMD/machine-2-3/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1121684287943981 | 80 / 0.1121684287943981 | 1167 |
| train/SMD/machine-2-4/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1556875929381524 | 73 / 0.1543371397535268 | 1183 |
| train/SMD/machine-2-4/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1564432809383947 | 68 / 0.1555254596221496 | 1147 |
| train/SMD/machine-2-4/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1553704694117944 | 76 / 0.1541597372892431 | 1148 |
| train/SMD/machine-2-4/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1572138950439477 | 45 / 0.1554478809639317 | 1148 |
| train/SMD/machine-2-5/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1183602423213152 | 76 / 0.1178488725811951 | 1162 |
| train/SMD/machine-2-5/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1161345717194516 | 77 / 0.1158345188264373 | 1160 |
| train/SMD/machine-2-5/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1216098163719918 | 79 / 0.1209185820700729 | 1160 |
| train/SMD/machine-2-5/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1172333746948507 | 80 / 0.1172333746948507 | 1159 |
| train/SMD/machine-2-6/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.116586525471259 | 70 / 0.1165470585699761 | 1412 |
| train/SMD/machine-2-6/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1185967934190647 | 74 / 0.1176975185185118 | 1412 |
| train/SMD/machine-2-6/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1175396489546142 | 80 / 0.1175396489546142 | 1412 |
| train/SMD/machine-2-6/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1193477226969475 | 76 / 0.1187148642107125 | 1411 |
| train/SMD/machine-2-7/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1122825519837247 | 75 / 0.112097778863632 | 1189 |
| train/SMD/machine-2-7/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.111544784014464 | 69 / 0.1110214197743094 | 1189 |
| train/SMD/machine-2-7/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1132051871352696 | 77 / 0.1116020453073058 | 1188 |
| train/SMD/machine-2-7/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1104659893256187 | 80 / 0.1104659893256187 | 1189 |
| train/SMD/machine-2-8/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1937011980846255 | 45 / 0.1922956390138114 | 1206 |
| train/SMD/machine-2-8/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1913629239951495 | 72 / 0.1848981324471188 | 1172 |
| train/SMD/machine-2-8/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1872642668253519 | 78 / 0.1845478998751237 | 1172 |
| train/SMD/machine-2-8/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1921626917067073 | 76 / 0.1881665583081981 | 1173 |
| train/SMD/machine-2-9/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1326883636279962 | 79 / 0.1317892670166452 | 1407 |
| train/SMD/machine-2-9/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1303951353224444 | 78 / 0.1302127507479824 | 1375 |
| train/SMD/machine-2-9/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1321325555322738 | 78 / 0.1319038830469502 | 1405 |
| train/SMD/machine-2-9/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.130596297876791 | 80 / 0.130596297876791 | 1374 |
| train/SMD/machine-3-1/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1280864235660497 | 80 / 0.1280864235660497 | 1384 |
| train/SMD/machine-3-1/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1276474994658407 | 80 / 0.1276474994658407 | 1384 |
| train/SMD/machine-3-1/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1338119869076106 | 76 / 0.1333680713200484 | 1412 |
| train/SMD/machine-3-1/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1278335925401598 | 80 / 0.1278335925401598 | 1412 |
| train/SMD/machine-3-2/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.2318147568633258 | 78 / 0.230563691313036 | 1179 |
| train/SMD/machine-3-2/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.2422073486988118 | 78 / 0.2356710544404505 | 1178 |
| train/SMD/machine-3-2/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.2347076368145713 | 79 / 0.2346031371362788 | 1176 |
| train/SMD/machine-3-2/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.2325543571881014 | 75 / 0.2317877188506449 | 1208 |
| train/SMD/machine-3-3/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1277644530826389 | 79 / 0.1182721808334631 | 1124 |
| train/SMD/machine-3-3/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1200640020291141 | 54 / 0.1195182299631985 | 1183 |
| train/SMD/machine-3-3/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1225127250575327 | 79 / 0.1195145827752179 | 1183 |
| train/SMD/machine-3-3/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1207707802182378 | 76 / 0.1188697402532528 | 1183 |
| train/SMD/machine-3-4/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.2761826321133651 | 78 / 0.2758576575471261 | 1162 |
| train/SMD/machine-3-4/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.2783251446537008 | 74 / 0.2768084238745223 | 1163 |
| train/SMD/machine-3-4/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.2764193342655422 | 79 / 0.2751632569489957 | 1163 |
| train/SMD/machine-3-4/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.2772858837364469 | 67 / 0.2766805912595004 | 1164 |
| train/SMD/machine-3-5/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1221068761255613 | 79 / 0.1220990562742524 | 1175 |
| train/SMD/machine-3-5/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1213068797103264 | 79 / 0.1207475352410149 | 1146 |
| train/SMD/machine-3-5/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1208970376129648 | 77 / 0.1205642835544444 | 1175 |
| train/SMD/machine-3-5/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1215594476444096 | 77 / 0.1207338057103413 | 1176 |
| train/SMD/machine-3-6/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1261067575604382 | 74 / 0.1258797207689316 | 1375 |
| train/SMD/machine-3-6/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1281863309681997 | 79 / 0.1271888171752311 | 1403 |
| train/SMD/machine-3-6/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1273087153812429 | 78 / 0.1261197078738156 | 1375 |
| train/SMD/machine-3-6/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1273910734155214 | 80 / 0.1273910734155214 | 1404 |
| train/SMD/machine-3-7/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.0652021300268605 | 78 / 0.0648746357376726 | 1384 |
| train/SMD/machine-3-7/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.0667258512130077 | 78 / 0.0657669951739118 | 1383 |
| train/SMD/machine-3-7/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.0656443598092918 | 80 / 0.0656443598092918 | 1409 |
| train/SMD/machine-3-7/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.0663560026736747 | 80 / 0.0663560026736747 | 1411 |
| train/SMD/machine-3-8/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.104305282325449 | 76 / 0.1029245717957975 | 1415 |
| train/SMD/machine-3-8/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1069996960212942 | 79 / 0.104405902233888 | 1388 |
| train/SMD/machine-3-8/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1060798278779451 | 75 / 0.1053082233582652 | 1414 |
| train/SMD/machine-3-8/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1027120561558049 | 79 / 0.101389592650197 | 1414 |
| train/SMD/machine-3-9/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1197517440818587 | 77 / 0.1185999515900329 | 1388 |
| train/SMD/machine-3-9/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1195456298393384 | 78 / 0.1189533771676449 | 1415 |
| train/SMD/machine-3-9/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1189367175156944 | 78 / 0.1186298178971692 | 1415 |
| train/SMD/machine-3-9/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1178536282307343 | 79 / 0.1177879529437623 | 1388 |
| train/SMD/machine-3-10/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1038712107758826 | 75 / 0.100538530659765 | 1171 |
| train/SMD/machine-3-10/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.100643642422268 | 80 / 0.100643642422268 | 1196 |
| train/SMD/machine-3-10/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1032179727284833 | 79 / 0.0993919316092362 | 1197 |
| train/SMD/machine-3-10/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1032765583541389 | 79 / 0.1019306428468207 | 1169 |
| train/SMD/machine-3-11/seed0/smd_cf_val_perm0_crson | 80 | 80 / 0.1185444050916158 | 78 / 0.1181889121675005 | 1406 |
| train/SMD/machine-3-11/seed1/smd_cf_val_perm0_crson | 80 | 80 / 0.1157206024032568 | 80 / 0.1157206024032568 | 1405 |
| train/SMD/machine-3-11/seed2/smd_cf_val_perm0_crson | 80 | 80 / 0.1154575112788618 | 79 / 0.1151474048078054 | 1354 |
| train/SMD/machine-3-11/seed3/smd_cf_val_perm0_crson | 80 | 80 / 0.1163289188999243 | 79 / 0.1159384598446864 | 1403 |
| train/SMD/machine-2-1/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2920601540549891 | 52 / 0.2761758629652553 | 2353 |
| train/SMD/machine-2-1/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2834216012484613 | 62 / 0.2754095827762497 | 2377 |
| train/SMD/machine-2-1/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2726588715166699 | 74 / 0.2690833095449938 | 2428 |
| train/SMD/machine-2-1/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2855762414198982 | 45 / 0.272625362285454 | 2376 |
| train/SMD/machine-2-2/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2202350577539555 | 78 / 0.2188913242021931 | 2455 |
| train/SMD/machine-2-2/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2175812133222771 | 58 / 0.2061716686637043 | 2430 |
| train/SMD/machine-2-2/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2088513234654989 | 80 / 0.2088513234654989 | 2406 |
| train/SMD/machine-2-2/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2205927675382972 | 40 / 0.2105312134586215 | 2455 |
| train/SMD/machine-2-3/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1362071805477349 | 55 / 0.1255525617286057 | 2319 |
| train/SMD/machine-2-3/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1785968488803686 | 49 / 0.1307753539268744 | 2341 |
| train/SMD/machine-2-3/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1394013881423307 | 73 / 0.1341786988569531 | 2293 |
| train/SMD/machine-2-3/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1322166656084187 | 68 / 0.1289630687845363 | 2439 |
| train/SMD/machine-2-4/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1696618443529078 | 66 / 0.1693821576832756 | 2355 |
| train/SMD/machine-2-4/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1803545650566198 | 73 / 0.174301937988178 | 2380 |
| train/SMD/machine-2-4/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1784343918812464 | 74 / 0.1705595219142316 | 2401 |
| train/SMD/machine-2-4/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.21263181572174 | 54 / 0.1734732657279916 | 2495 |
| train/SMD/machine-2-5/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1441181033119675 | 79 / 0.1441097541215804 | 2349 |
| train/SMD/machine-2-5/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1601819534285624 | 73 / 0.1495418283447431 | 2370 |
| train/SMD/machine-2-5/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1573667356315725 | 78 / 0.1567036882534609 | 2506 |
| train/SMD/machine-2-5/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1567581947245909 | 75 / 0.1451766744795506 | 2414 |
| train/SMD/machine-2-6/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1380887945004828 | 66 / 0.1328440246637996 | 2801 |
| train/SMD/machine-2-6/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1330648615669377 | 76 / 0.1328714496298446 | 2865 |
| train/SMD/machine-2-6/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1397887696700425 | 71 / 0.133060588938106 | 2977 |
| train/SMD/machine-2-6/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1362842813754506 | 76 / 0.1319782737677368 | 3022 |
| train/SMD/machine-2-7/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1263787350771861 | 80 / 0.1263787350771861 | 2408 |
| train/SMD/machine-2-7/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1178528806610633 | 79 / 0.11771675637053 | 2408 |
| train/SMD/machine-2-7/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1269355051480611 | 77 / 0.1225337395986911 | 2533 |
| train/SMD/machine-2-7/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1293728728361756 | 79 / 0.1227903758934346 | 2575 |
| train/SMD/machine-2-8/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2110652827886598 | 80 / 0.2110652827886598 | 2440 |
| train/SMD/machine-2-8/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2081456126618663 | 78 / 0.2017518451250466 | 2440 |
| train/SMD/machine-2-8/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2193914215118785 | 75 / 0.2069474029634379 | 2562 |
| train/SMD/machine-2-8/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2178518830450785 | 71 / 0.2022991645751113 | 2561 |
| train/SMD/machine-2-9/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1480975622144653 | 80 / 0.1480975622144653 | 2970 |
| train/SMD/machine-2-9/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1498076248501525 | 79 / 0.1480925546037933 | 2846 |
| train/SMD/machine-2-9/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1595292629756042 | 76 / 0.1536778396580539 | 2990 |
| train/SMD/machine-2-9/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1970709902638605 | 78 / 0.1853758264462069 | 2987 |
| train/SMD/machine-3-1/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1371334131174615 | 78 / 0.1367778465757883 | 2918 |
| train/SMD/machine-3-1/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1387837274772431 | 80 / 0.1387837274772431 | 2977 |
| train/SMD/machine-3-1/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1442241558172377 | 80 / 0.1442241558172377 | 2889 |
| train/SMD/machine-3-1/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1345165590297588 | 80 / 0.1345165590297588 | 3007 |
| train/SMD/machine-3-2/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2540845813786656 | 74 / 0.2493187724495628 | 2399 |
| train/SMD/machine-3-2/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2486421051023693 | 80 / 0.2486421051023693 | 2475 |
| train/SMD/machine-3-2/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2658264039972215 | 62 / 0.2565520451569088 | 2420 |
| train/SMD/machine-3-2/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2513018253111129 | 80 / 0.2513018253111129 | 2400 |
| train/SMD/machine-3-3/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1261219564862919 | 67 / 0.1216197797304562 | 2373 |
| train/SMD/machine-3-3/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.141543314752563 | 44 / 0.1343592223564426 | 2372 |
| train/SMD/machine-3-3/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1250078028438619 | 71 / 0.1210543739470573 | 2438 |
| train/SMD/machine-3-3/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1305288532140146 | 79 / 0.1234376346184042 | 2474 |
| train/SMD/machine-3-4/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2859570286409631 | 77 / 0.2827202812817868 | 2308 |
| train/SMD/machine-3-4/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.283790214009293 | 79 / 0.2807846531352883 | 2418 |
| train/SMD/machine-3-4/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2794136728838275 | 80 / 0.2794136728838275 | 2348 |
| train/SMD/machine-3-4/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.2806851937962147 | 80 / 0.2806851937962147 | 2365 |
| train/SMD/machine-3-5/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.160158945434664 | 57 / 0.1405673976509765 | 2306 |
| train/SMD/machine-3-5/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1395202043016659 | 77 / 0.1376724724612983 | 2377 |
| train/SMD/machine-3-5/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1442203386082192 | 68 / 0.1409464085066657 | 2340 |
| train/SMD/machine-3-5/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1351968573549564 | 80 / 0.1351968573549564 | 2357 |
| train/SMD/machine-3-6/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1473303949361259 | 74 / 0.1355058364403332 | 2775 |
| train/SMD/machine-3-6/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1452420020535733 | 70 / 0.1422485760950109 | 2756 |
| train/SMD/machine-3-6/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1455148588952134 | 79 / 0.1450121818743534 | 2881 |
| train/SMD/machine-3-6/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1508448195511712 | 74 / 0.1419021512919005 | 2948 |
| train/SMD/machine-3-7/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1450222199061328 | 42 / 0.1168428776122069 | 2887 |
| train/SMD/machine-3-7/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1391732601911562 | 38 / 0.1149872243130741 | 2921 |
| train/SMD/machine-3-7/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1308990040260472 | 78 / 0.1210141500864692 | 2818 |
| train/SMD/machine-3-7/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1080297462456933 | 77 / 0.101505216632907 | 2851 |
| train/SMD/machine-3-8/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.179340677089371 | 77 / 0.1746077416869341 | 2799 |
| train/SMD/machine-3-8/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1610823105989903 | 78 / 0.1567711784078936 | 2831 |
| train/SMD/machine-3-8/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1534133845562668 | 75 / 0.1497109175980601 | 2900 |
| train/SMD/machine-3-8/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1721231560958059 | 79 / 0.1706263892127917 | 2948 |
| train/SMD/machine-3-9/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1210662495572813 | 77 / 0.1206623057994506 | 2915 |
| train/SMD/machine-3-9/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1228911262741762 | 80 / 0.1228911262741762 | 2947 |
| train/SMD/machine-3-9/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1227919025479616 | 80 / 0.1227919025479616 | 2859 |
| train/SMD/machine-3-9/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1254427303766387 | 77 / 0.1249876269716799 | 2953 |
| train/SMD/machine-3-10/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1159458345720015 | 73 / 0.1038211360123504 | 2376 |
| train/SMD/machine-3-10/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1143842122864998 | 78 / 0.1099081492326097 | 2422 |
| train/SMD/machine-3-10/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1070055757131076 | 78 / 0.1038968873723711 | 2509 |
| train/SMD/machine-3-10/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1119301389200941 | 65 / 0.1116943929981128 | 2493 |
| train/SMD/machine-3-11/seed0/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1513382581702231 | 68 / 0.1466698861071762 | 2753 |
| train/SMD/machine-3-11/seed1/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1368139047448361 | 80 / 0.1368139047448361 | 2858 |
| train/SMD/machine-3-11/seed2/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1447897880149849 | 80 / 0.1447897880149849 | 2860 |
| train/SMD/machine-3-11/seed3/smd_cf_val_perm2_crsoff | 80 | 80 / 0.1503023034231803 | 77 / 0.1481653629238857 | 2812 |
| train/SMD/machine-2-1/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2969628330331312 | 76 / 0.2882553594667123 | 2448 |
| train/SMD/machine-2-1/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2969750237647957 | 65 / 0.2859085424280384 | 2403 |
| train/SMD/machine-2-1/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2821220651781305 | 80 / 0.2821220651781305 | 2363 |
| train/SMD/machine-2-1/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2821924461092237 | 70 / 0.2789218228956583 | 2420 |
| train/SMD/machine-2-2/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2426594284127724 | 79 / 0.2330844964323186 | 2542 |
| train/SMD/machine-2-2/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2457842482725222 | 79 / 0.2423693384438463 | 2597 |
| train/SMD/machine-2-2/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.241669797426809 | 79 / 0.2386163648463965 | 2401 |
| train/SMD/machine-2-2/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2360783645831377 | 78 / 0.2315933333973228 | 2412 |
| train/SMD/machine-2-3/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1476950089647113 | 58 / 0.1471101899885818 | 2299 |
| train/SMD/machine-2-3/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1893118612634997 | 76 / 0.169416911672258 | 2065 |
| train/SMD/machine-2-3/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1471284160993356 | 76 / 0.144088194040733 | 2289 |
| train/SMD/machine-2-3/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1363133995578443 | 79 / 0.135657198434335 | 2356 |
| train/SMD/machine-2-4/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1866273190628617 | 80 / 0.1866273190628617 | 2495 |
| train/SMD/machine-2-4/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2198684128060144 | 77 / 0.2150327714315749 | 2323 |
| train/SMD/machine-2-4/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2068947080292129 | 75 / 0.1914953827530265 | 2395 |
| train/SMD/machine-2-4/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2160330579003059 | 70 / 0.1935975032025676 | 2382 |
| train/SMD/machine-2-5/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1826672996246476 | 79 / 0.1825531125075298 | 2371 |
| train/SMD/machine-2-5/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1794126383486184 | 76 / 0.1790376821929065 | 2421 |
| train/SMD/machine-2-5/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1777694129334606 | 78 / 0.1740115320748465 | 2402 |
| train/SMD/machine-2-5/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2032915011700577 | 77 / 0.1824915481820249 | 2376 |
| train/SMD/machine-2-6/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1609113236075253 | 75 / 0.1580849512332123 | 2892 |
| train/SMD/machine-2-6/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1512633197224076 | 76 / 0.150265347067859 | 2830 |
| train/SMD/machine-2-6/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1614014556118048 | 79 / 0.1566749649705437 | 2929 |
| train/SMD/machine-2-6/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1525654814996654 | 79 / 0.1514151089960514 | 2844 |
| train/SMD/machine-2-7/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1600088732226932 | 78 / 0.1600047956097175 | 2364 |
| train/SMD/machine-2-7/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1503384041841905 | 80 / 0.1503384041841905 | 2387 |
| train/SMD/machine-2-7/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1633833689406834 | 79 / 0.1611003905869676 | 2400 |
| train/SMD/machine-2-7/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.151430040739184 | 78 / 0.1511894174289077 | 2466 |
| train/SMD/machine-2-8/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2680473139636976 | 79 / 0.2629262091160261 | 2550 |
| train/SMD/machine-2-8/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2645516567601343 | 80 / 0.2645516567601343 | 2413 |
| train/SMD/machine-2-8/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2939116582543818 | 7 / 0.2696128162559344 | 2458 |
| train/SMD/machine-2-8/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2768068872399223 | 77 / 0.2749313780398603 | 2424 |
| train/SMD/machine-2-9/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2371641327185765 | 70 / 0.2318398595682243 | 2880 |
| train/SMD/machine-2-9/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2318907669159105 | 17 / 0.2091535807082549 | 2825 |
| train/SMD/machine-2-9/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2124587023356123 | 65 / 0.2023930396765876 | 2883 |
| train/SMD/machine-2-9/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2487330207269822 | 73 / 0.2416482150590212 | 2839 |
| train/SMD/machine-3-1/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1621211679143654 | 80 / 0.1621211679143654 | 2848 |
| train/SMD/machine-3-1/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1642456867450741 | 77 / 0.1633284178458826 | 2827 |
| train/SMD/machine-3-1/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1731406668690779 | 79 / 0.1717804226653153 | 2858 |
| train/SMD/machine-3-1/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1643727031422911 | 79 / 0.1635334595142473 | 2866 |
| train/SMD/machine-3-2/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2908752649861044 | 77 / 0.2905549806458347 | 2459 |
| train/SMD/machine-3-2/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.3139082051565854 | 79 / 0.3105756349714996 | 2527 |
| train/SMD/machine-3-2/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.3206278533998355 | 9 / 0.310610869942721 | 2426 |
| train/SMD/machine-3-2/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2944043435362815 | 80 / 0.2944043435362815 | 2482 |
| train/SMD/machine-3-3/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1528655507574409 | 77 / 0.1508262204218044 | 2575 |
| train/SMD/machine-3-3/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1788519351737071 | 80 / 0.1788519351737071 | 2517 |
| train/SMD/machine-3-3/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1541181264698184 | 78 / 0.1527909549862993 | 2401 |
| train/SMD/machine-3-3/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1536419031728962 | 79 / 0.1475455390233323 | 2425 |
| train/SMD/machine-3-4/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.3178270282043843 | 80 / 0.3178270282043843 | 2368 |
| train/SMD/machine-3-4/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.3517303820103951 | 77 / 0.3286995330193618 | 2331 |
| train/SMD/machine-3-4/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.3236627241564896 | 78 / 0.3233205931345282 | 2457 |
| train/SMD/machine-3-4/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.3213450018811156 | 77 / 0.3209120553135818 | 2318 |
| train/SMD/machine-3-5/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1506905579977981 | 80 / 0.1506905579977981 | 2347 |
| train/SMD/machine-3-5/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1462840722097599 | 77 / 0.1444888845328394 | 2364 |
| train/SMD/machine-3-5/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1582506945309109 | 63 / 0.156686197137744 | 2362 |
| train/SMD/machine-3-5/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1542928508682082 | 78 / 0.1527365966957188 | 2328 |
| train/SMD/machine-3-6/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1671145064692695 | 75 / 0.163373316401017 | 2833 |
| train/SMD/machine-3-6/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1657887245776903 | 79 / 0.1651244719000646 | 2785 |
| train/SMD/machine-3-6/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1654882393927771 | 76 / 0.1646647371752605 | 2917 |
| train/SMD/machine-3-6/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1700688361911567 | 63 / 0.1681824615328425 | 2854 |
| train/SMD/machine-3-7/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2106369785781419 | 58 / 0.1375167927381403 | 2787 |
| train/SMD/machine-3-7/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1228859151469696 | 80 / 0.1228859151469696 | 2793 |
| train/SMD/machine-3-7/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1476674355380695 | 77 / 0.1359065771759657 | 2793 |
| train/SMD/machine-3-7/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1392218084381212 | 75 / 0.1298316352825464 | 2855 |
| train/SMD/machine-3-8/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.2182964025542201 | 80 / 0.2182964025542201 | 2868 |
| train/SMD/machine-3-8/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.2322845296460085 | 50 / 0.2121433584926612 | 2805 |
| train/SMD/machine-3-8/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.2182723702556716 | 66 / 0.2068234419601148 | 2859 |
| train/SMD/machine-3-8/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.2232079594363046 | 78 / 0.2107229948385334 | 2856 |
| train/SMD/machine-3-9/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1625539928019816 | 76 / 0.1619694312905196 | 2697 |
| train/SMD/machine-3-9/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1615995628711701 | 80 / 0.1615995628711701 | 2797 |
| train/SMD/machine-3-9/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1582857834735428 | 79 / 0.1580888105546555 | 2823 |
| train/SMD/machine-3-9/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1534709821524611 | 79 / 0.1532837970662142 | 2857 |
| train/SMD/machine-3-10/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.158276811988563 | 75 / 0.155552678213771 | 2505 |
| train/SMD/machine-3-10/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1284973013427699 | 73 / 0.123394345262291 | 2361 |
| train/SMD/machine-3-10/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1775688740888996 | 26 / 0.1283238717236557 | 2376 |
| train/SMD/machine-3-10/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1318954850045579 | 78 / 0.1309049263513779 | 2421 |
| train/SMD/machine-3-11/seed0/smd_cf_val_perm2_crson | 80 | 80 / 0.1780669327882451 | 77 / 0.1695319667580349 | 2798 |
| train/SMD/machine-3-11/seed1/smd_cf_val_perm2_crson | 80 | 80 / 0.1820272970387919 | 80 / 0.1820272970387919 | 2842 |
| train/SMD/machine-3-11/seed2/smd_cf_val_perm2_crson | 80 | 80 / 0.1732685800052887 | 80 / 0.1732685800052887 | 2765 |
| train/SMD/machine-3-11/seed3/smd_cf_val_perm2_crson | 80 | 80 / 0.1795766847788647 | 72 / 0.1690276084879579 | 2779 |
