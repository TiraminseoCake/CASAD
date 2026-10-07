# cfval_abl_nocstruct / server8 / cfval_abl_nocstruct_server8

- exported: 2026-10-07T11:32:50+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 273 — {'success': 273} — **COMPLETE**
- exported eval jobs: 168, train jobs: 84; duplicates flagged: 0

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
| SWaT | swat | 2 | last | 80 | A_off | 0.6313 | 0.5414 | 0.7028 | 1.0 | False |
| SWaT | swat | 2 | last | 80 | A_on | 0.7531 | 0.6394 | 0.7387 | 1.0 | False |
| SWaT | swat | 2 | best_val | 59 | A_off | 0.6723 | 0.5680 | 0.7258 | 1.0 | False |
| SWaT | swat | 2 | best_val | 59 | A_on | 0.7474 | 0.6167 | 0.7386 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_off | 0.6835 | 0.5532 | 0.7515 | 1.0 | False |
| SWaT | swat | 3 | last | 80 | A_on | 0.7480 | 0.6076 | 0.7385 | 1.0 | False |
| SWaT | swat | 3 | best_val | 72 | A_off | 0.7002 | 0.5623 | 0.7520 | 1.0 | False |
| SWaT | swat | 3 | best_val | 72 | A_on | 0.7485 | 0.6099 | 0.7384 | 1.0 | False |
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

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SWaT/swat/seed0/swat_cf_val_nocstruct | 80 | 80 / 0.0051475986864211 | 73 / 0.0049514689892432 | 115181 |
| train/SWaT/swat/seed1/swat_cf_val_nocstruct | 80 | 80 / 0.0055690734401855 | 74 / 0.0051509114316716 | 115999 |
| train/SWaT/swat/seed2/swat_cf_val_nocstruct | 80 | 80 / 0.0051428281755355 | 59 / 0.0049107645926399 | 113955 |
| train/SWaT/swat/seed3/swat_cf_val_nocstruct | 80 | 80 / 0.0051362669680361 | 72 / 0.0049462348384827 | 114297 |
| train/SMD/machine-2-1/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.262912434524565 | 79 / 0.2606784778534272 | 1247 |
| train/SMD/machine-2-1/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.2753837126174439 | 49 / 0.2640948533189433 | 1246 |
| train/SMD/machine-2-1/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.2617679204162957 | 76 / 0.2605599459092821 | 1222 |
| train/SMD/machine-2-1/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.263255675950331 | 74 / 0.2625122939623727 | 1246 |
| train/SMD/machine-2-2/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.2059546237668819 | 45 / 0.2015579573830076 | 1203 |
| train/SMD/machine-2-2/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1952252484281395 | 80 / 0.1952252484281395 | 1196 |
| train/SMD/machine-2-2/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.2185964401125102 | 31 / 0.2060793703809133 | 1244 |
| train/SMD/machine-2-2/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.218235699246084 | 35 / 0.2086015549005666 | 1194 |
| train/SMD/machine-2-3/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1123876835199733 | 71 / 0.112254690855164 | 1141 |
| train/SMD/machine-2-3/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.112748487964406 | 79 / 0.11250697280689 | 1187 |
| train/SMD/machine-2-3/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1132939466656516 | 75 / 0.1130927889851584 | 1152 |
| train/SMD/machine-2-3/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1121604077025349 | 80 / 0.1121604077025349 | 1206 |
| train/SMD/machine-2-4/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1550815990403122 | 76 / 0.1534505825584248 | 1162 |
| train/SMD/machine-2-4/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1558101961560188 | 78 / 0.1551721936318965 | 1187 |
| train/SMD/machine-2-4/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1564066952358105 | 79 / 0.1558511768843783 | 1213 |
| train/SMD/machine-2-4/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1563188161180341 | 76 / 0.1549873019621764 | 1193 |
| train/SMD/machine-2-5/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1137666958809758 | 74 / 0.1133318158923784 | 1184 |
| train/SMD/machine-2-5/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1112088900565241 | 80 / 0.1112088900565241 | 1204 |
| train/SMD/machine-2-5/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1158860792037825 | 79 / 0.1152592568236667 | 1195 |
| train/SMD/machine-2-5/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1112602894414259 | 80 / 0.1112602894414259 | 1175 |
| train/SMD/machine-2-6/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1195981878983347 | 70 / 0.1188943687675415 | 1304 |
| train/SMD/machine-2-6/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.123064407916675 | 74 / 0.1208358596754187 | 1406 |
| train/SMD/machine-2-6/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.119661222535187 | 78 / 0.1191262072212167 | 1427 |
| train/SMD/machine-2-6/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1213224484114696 | 73 / 0.1207571910058557 | 1425 |
| train/SMD/machine-2-7/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1075959630626399 | 80 / 0.1075959630626399 | 1129 |
| train/SMD/machine-2-7/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1085503606731533 | 80 / 0.1085503606731533 | 1250 |
| train/SMD/machine-2-7/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1085498609889849 | 77 / 0.1084147435374316 | 1175 |
| train/SMD/machine-2-7/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1074231339731934 | 80 / 0.1074231339731934 | 1183 |
| train/SMD/machine-2-8/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1902729247419473 | 78 / 0.1884858112385918 | 1192 |
| train/SMD/machine-2-8/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1906247584097209 | 72 / 0.1835006467557818 | 1168 |
| train/SMD/machine-2-8/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1874942223392792 | 78 / 0.1853548399254045 | 1244 |
| train/SMD/machine-2-8/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1939790058563547 | 76 / 0.1872759382567927 | 1182 |
| train/SMD/machine-2-9/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1298937309397118 | 78 / 0.1295627357161882 | 1450 |
| train/SMD/machine-2-9/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1310345159031856 | 75 / 0.1301723358570197 | 1425 |
| train/SMD/machine-2-9/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1314575055278644 | 74 / 0.1309516651526579 | 1436 |
| train/SMD/machine-2-9/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1323600517332113 | 78 / 0.131012565596339 | 1415 |
| train/SMD/machine-3-1/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.128187900419862 | 78 / 0.1281290050730417 | 1399 |
| train/SMD/machine-3-1/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1286320830982411 | 80 / 0.1286320830982411 | 1397 |
| train/SMD/machine-3-1/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1301741093679867 | 77 / 0.1296576134624659 | 1392 |
| train/SMD/machine-3-1/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1256375309258094 | 80 / 0.1256375309258094 | 1384 |
| train/SMD/machine-3-2/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.229377913532593 | 79 / 0.2286471416417922 | 1171 |
| train/SMD/machine-3-2/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.2299003990229442 | 78 / 0.2267520261480044 | 1192 |
| train/SMD/machine-3-2/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.2324487412242025 | 75 / 0.2312281555672134 | 1214 |
| train/SMD/machine-3-2/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.2313806820078096 | 75 / 0.2307476862794408 | 1184 |
| train/SMD/machine-3-3/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1281235912927355 | 76 / 0.1186515813875798 | 1170 |
| train/SMD/machine-3-3/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1203766649832328 | 79 / 0.119254068329744 | 1173 |
| train/SMD/machine-3-3/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.121049533658495 | 74 / 0.1189749785131919 | 1209 |
| train/SMD/machine-3-3/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1201199857706106 | 71 / 0.1185156276611404 | 1209 |
| train/SMD/machine-3-4/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.2764637177875263 | 75 / 0.2762021074864921 | 1204 |
| train/SMD/machine-3-4/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.2781879256208812 | 65 / 0.2766551198576318 | 1152 |
| train/SMD/machine-3-4/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.2766869127384138 | 79 / 0.2755560569617105 | 1111 |
| train/SMD/machine-3-4/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.276531123342131 | 78 / 0.2762282644399754 | 1168 |
| train/SMD/machine-3-5/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1214621075034119 | 79 / 0.120962124072727 | 1176 |
| train/SMD/machine-3-5/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1207880897130105 | 79 / 0.1200418376021482 | 1146 |
| train/SMD/machine-3-5/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1214614037558534 | 79 / 0.1205629871237347 | 1202 |
| train/SMD/machine-3-5/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1208055463546072 | 79 / 0.1201925959868738 | 1188 |
| train/SMD/machine-3-6/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1264101667025449 | 75 / 0.1258539075080688 | 1391 |
| train/SMD/machine-3-6/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1280707654943902 | 76 / 0.1274809930797611 | 1410 |
| train/SMD/machine-3-6/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1266662977361857 | 78 / 0.1258495705755833 | 1455 |
| train/SMD/machine-3-6/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1277258964762029 | 80 / 0.1277258964762029 | 1431 |
| train/SMD/machine-3-7/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.0673812870834473 | 79 / 0.0659719416654459 | 1389 |
| train/SMD/machine-3-7/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.0672117125323811 | 80 / 0.0672117125323811 | 1380 |
| train/SMD/machine-3-7/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.065248312144343 | 74 / 0.0650472890031663 | 1469 |
| train/SMD/machine-3-7/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.0658567885828538 | 79 / 0.0656253185476072 | 1417 |
| train/SMD/machine-3-8/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1035438434198582 | 79 / 0.1012984571549029 | 1384 |
| train/SMD/machine-3-8/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1056165128807291 | 79 / 0.1049389230581947 | 1441 |
| train/SMD/machine-3-8/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1034694086963738 | 73 / 0.1030248935562298 | 1390 |
| train/SMD/machine-3-8/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1039788836741432 | 79 / 0.1037407981997814 | 1408 |
| train/SMD/machine-3-9/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1199961452152542 | 76 / 0.1194242679416042 | 1410 |
| train/SMD/machine-3-9/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1165208577553885 | 78 / 0.1161179522495663 | 1384 |
| train/SMD/machine-3-9/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1190069794311265 | 80 / 0.1190069794311265 | 1459 |
| train/SMD/machine-3-9/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1208953089902516 | 76 / 0.1195581303206907 | 1387 |
| train/SMD/machine-3-10/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1013516148436021 | 75 / 0.0983009471265601 | 1175 |
| train/SMD/machine-3-10/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1033336247409774 | 76 / 0.0984999461836905 | 1179 |
| train/SMD/machine-3-10/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1052306272317764 | 70 / 0.0978828872820088 | 1212 |
| train/SMD/machine-3-10/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1004266371754957 | 79 / 0.0991557132389664 | 1234 |
| train/SMD/machine-3-11/seed0/smd_cf_val_nocstruct | 80 | 80 / 0.1140638979164334 | 78 / 0.1139635907549213 | 1391 |
| train/SMD/machine-3-11/seed1/smd_cf_val_nocstruct | 80 | 80 / 0.1131655475374335 | 80 / 0.1131655475374335 | 1408 |
| train/SMD/machine-3-11/seed2/smd_cf_val_nocstruct | 80 | 80 / 0.1131576256372279 | 80 / 0.1131576256372279 | 1384 |
| train/SMD/machine-3-11/seed3/smd_cf_val_nocstruct | 80 | 80 / 0.1126965366229326 | 76 / 0.1123061456835345 | 1438 |
