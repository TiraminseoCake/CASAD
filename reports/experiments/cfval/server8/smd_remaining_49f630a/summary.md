# cfval / server8 / smd_remaining_49f630a

- exported: 2026-09-13T01:00:47+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 260 — {'success': 260} — **COMPLETE**
- exported eval jobs: 160, train jobs: 80; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
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

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/SMD/machine-2-1/seed0/smd_cf_val | 80 | 80 / 0.2677004262232947 | 77 / 0.2637892625774121 | 1179 |
| train/SMD/machine-2-1/seed1/smd_cf_val | 80 | 80 / 0.2676892976812862 | 60 / 0.2640355730847335 | 1165 |
| train/SMD/machine-2-1/seed2/smd_cf_val | 80 | 80 / 0.2645138002070699 | 72 / 0.263298892263869 | 1167 |
| train/SMD/machine-2-1/seed3/smd_cf_val | 80 | 80 / 0.2653082875079542 | 71 / 0.2632791976105242 | 1166 |
| train/SMD/machine-2-2/seed0/smd_cf_val | 80 | 80 / 0.2031629778153255 | 43 / 0.1994856220431196 | 1176 |
| train/SMD/machine-2-2/seed1/smd_cf_val | 80 | 80 / 0.2080781873816248 | 35 / 0.2053817920302661 | 1175 |
| train/SMD/machine-2-2/seed2/smd_cf_val | 80 | 80 / 0.2085786004290274 | 50 / 0.2057949966226792 | 1175 |
| train/SMD/machine-2-2/seed3/smd_cf_val | 80 | 80 / 0.2051570336270636 | 80 / 0.2051570336270636 | 1164 |
| train/SMD/machine-2-3/seed0/smd_cf_val | 80 | 80 / 0.1128886125265282 | 80 / 0.1128886125265282 | 1156 |
| train/SMD/machine-2-3/seed1/smd_cf_val | 80 | 80 / 0.1132928506263798 | 79 / 0.1126326386172924 | 1169 |
| train/SMD/machine-2-3/seed2/smd_cf_val | 80 | 80 / 0.1133425242673895 | 77 / 0.1130053622765267 | 1130 |
| train/SMD/machine-2-3/seed3/smd_cf_val | 80 | 80 / 0.1121684287943981 | 80 / 0.1121684287943981 | 1168 |
| train/SMD/machine-2-4/seed0/smd_cf_val | 80 | 80 / 0.1556875929381524 | 73 / 0.1543371397535268 | 1142 |
| train/SMD/machine-2-4/seed1/smd_cf_val | 80 | 80 / 0.1564432809383947 | 68 / 0.1555254596221496 | 1165 |
| train/SMD/machine-2-4/seed2/smd_cf_val | 80 | 80 / 0.1553704694117944 | 76 / 0.1541597372892431 | 1141 |
| train/SMD/machine-2-4/seed3/smd_cf_val | 80 | 80 / 0.1572138950439477 | 45 / 0.1554478809639317 | 1165 |
| train/SMD/machine-2-5/seed0/smd_cf_val | 80 | 80 / 0.1183602423213152 | 76 / 0.1178488725811951 | 1157 |
| train/SMD/machine-2-5/seed1/smd_cf_val | 80 | 80 / 0.1161345717194516 | 77 / 0.1158345188264373 | 1151 |
| train/SMD/machine-2-5/seed2/smd_cf_val | 80 | 80 / 0.1216098163719918 | 79 / 0.1209185820700729 | 1134 |
| train/SMD/machine-2-5/seed3/smd_cf_val | 80 | 80 / 0.1172333746948507 | 80 / 0.1172333746948507 | 1143 |
| train/SMD/machine-2-6/seed0/smd_cf_val | 80 | 80 / 0.116586525471259 | 70 / 0.1165470585699761 | 1393 |
| train/SMD/machine-2-6/seed1/smd_cf_val | 80 | 80 / 0.1185967934190647 | 74 / 0.1176975185185118 | 1396 |
| train/SMD/machine-2-6/seed2/smd_cf_val | 80 | 80 / 0.1175396489546142 | 80 / 0.1175396489546142 | 1375 |
| train/SMD/machine-2-6/seed3/smd_cf_val | 80 | 80 / 0.1193477226969475 | 76 / 0.1187148642107125 | 1409 |
| train/SMD/machine-2-7/seed0/smd_cf_val | 80 | 80 / 0.1122825519837247 | 75 / 0.112097778863632 | 1182 |
| train/SMD/machine-2-7/seed1/smd_cf_val | 80 | 80 / 0.111544784014464 | 69 / 0.1110214197743094 | 1165 |
| train/SMD/machine-2-7/seed2/smd_cf_val | 80 | 80 / 0.1132051871352696 | 77 / 0.1116020453073058 | 1248 |
| train/SMD/machine-2-7/seed3/smd_cf_val | 80 | 80 / 0.1104659893256187 | 80 / 0.1104659893256187 | 1200 |
| train/SMD/machine-2-8/seed0/smd_cf_val | 80 | 80 / 0.1937011980846255 | 45 / 0.1922956390138114 | 1261 |
| train/SMD/machine-2-8/seed1/smd_cf_val | 80 | 80 / 0.1913629239951495 | 72 / 0.1848981324471188 | 1213 |
| train/SMD/machine-2-8/seed2/smd_cf_val | 80 | 80 / 0.1872642668253519 | 78 / 0.1845478998751237 | 1231 |
| train/SMD/machine-2-8/seed3/smd_cf_val | 80 | 80 / 0.1921626917067073 | 76 / 0.1881665583081981 | 1206 |
| train/SMD/machine-2-9/seed0/smd_cf_val | 80 | 80 / 0.1326883636279962 | 79 / 0.1317892670166452 | 1465 |
| train/SMD/machine-2-9/seed1/smd_cf_val | 80 | 80 / 0.1303951353224444 | 78 / 0.1302127507479824 | 1433 |
| train/SMD/machine-2-9/seed2/smd_cf_val | 80 | 80 / 0.1321325555322738 | 78 / 0.1319038830469502 | 1448 |
| train/SMD/machine-2-9/seed3/smd_cf_val | 80 | 80 / 0.130596297876791 | 80 / 0.130596297876791 | 1449 |
| train/SMD/machine-3-1/seed0/smd_cf_val | 80 | 80 / 0.1280864235660497 | 80 / 0.1280864235660497 | 1463 |
| train/SMD/machine-3-1/seed1/smd_cf_val | 80 | 80 / 0.1276474994658407 | 80 / 0.1276474994658407 | 1459 |
| train/SMD/machine-3-1/seed2/smd_cf_val | 80 | 80 / 0.1338119869076106 | 76 / 0.1333680713200484 | 1461 |
| train/SMD/machine-3-1/seed3/smd_cf_val | 80 | 80 / 0.1278335925401598 | 80 / 0.1278335925401598 | 1446 |
| train/SMD/machine-3-2/seed0/smd_cf_val | 80 | 80 / 0.2318147568633258 | 78 / 0.230563691313036 | 1235 |
| train/SMD/machine-3-2/seed1/smd_cf_val | 80 | 80 / 0.2422073486988118 | 78 / 0.2356710544404505 | 1221 |
| train/SMD/machine-3-2/seed2/smd_cf_val | 80 | 80 / 0.2347076368145713 | 79 / 0.2346031371362788 | 1247 |
| train/SMD/machine-3-2/seed3/smd_cf_val | 80 | 80 / 0.2325543571881014 | 75 / 0.2317877188506449 | 1243 |
| train/SMD/machine-3-3/seed0/smd_cf_val | 80 | 80 / 0.1277644530826389 | 79 / 0.1182721808334631 | 1275 |
| train/SMD/machine-3-3/seed1/smd_cf_val | 80 | 80 / 0.1200640020291141 | 54 / 0.1195182299631985 | 1230 |
| train/SMD/machine-3-3/seed2/smd_cf_val | 80 | 80 / 0.1225127250575327 | 79 / 0.1195145827752179 | 1229 |
| train/SMD/machine-3-3/seed3/smd_cf_val | 80 | 80 / 0.1207707802182378 | 76 / 0.1188697402532528 | 1203 |
| train/SMD/machine-3-4/seed0/smd_cf_val | 80 | 80 / 0.2761826321133651 | 78 / 0.2758576575471261 | 1190 |
| train/SMD/machine-3-4/seed1/smd_cf_val | 80 | 80 / 0.2783251446537008 | 74 / 0.2768084238745223 | 1215 |
| train/SMD/machine-3-4/seed2/smd_cf_val | 80 | 80 / 0.2764193342655422 | 79 / 0.2751632569489957 | 1216 |
| train/SMD/machine-3-4/seed3/smd_cf_val | 80 | 80 / 0.2772858837364469 | 67 / 0.2766805912595004 | 1191 |
| train/SMD/machine-3-5/seed0/smd_cf_val | 80 | 80 / 0.1221068761255613 | 79 / 0.1220990562742524 | 1201 |
| train/SMD/machine-3-5/seed1/smd_cf_val | 80 | 80 / 0.1213068797103264 | 79 / 0.1207475352410149 | 1212 |
| train/SMD/machine-3-5/seed2/smd_cf_val | 80 | 80 / 0.1208970376129648 | 77 / 0.1205642835544444 | 1189 |
| train/SMD/machine-3-5/seed3/smd_cf_val | 80 | 80 / 0.1215594476444096 | 77 / 0.1207338057103413 | 1207 |
| train/SMD/machine-3-6/seed0/smd_cf_val | 80 | 80 / 0.1261067575604382 | 74 / 0.1258797207689316 | 1436 |
| train/SMD/machine-3-6/seed1/smd_cf_val | 80 | 80 / 0.1281863309681997 | 79 / 0.1271888171752311 | 1425 |
| train/SMD/machine-3-6/seed2/smd_cf_val | 80 | 80 / 0.1273087153812429 | 78 / 0.1261197078738156 | 1406 |
| train/SMD/machine-3-6/seed3/smd_cf_val | 80 | 80 / 0.1273910734155214 | 80 / 0.1273910734155214 | 1415 |
| train/SMD/machine-3-7/seed0/smd_cf_val | 80 | 80 / 0.0652021300268605 | 78 / 0.0648746357376726 | 1425 |
| train/SMD/machine-3-7/seed1/smd_cf_val | 80 | 80 / 0.0667258512130077 | 78 / 0.0657669951739118 | 1465 |
| train/SMD/machine-3-7/seed2/smd_cf_val | 80 | 80 / 0.0656443598092918 | 80 / 0.0656443598092918 | 1458 |
| train/SMD/machine-3-7/seed3/smd_cf_val | 80 | 80 / 0.0663560026736747 | 80 / 0.0663560026736747 | 1449 |
| train/SMD/machine-3-8/seed0/smd_cf_val | 80 | 80 / 0.104305282325449 | 76 / 0.1029245717957975 | 1448 |
| train/SMD/machine-3-8/seed1/smd_cf_val | 80 | 80 / 0.1069996960212942 | 79 / 0.104405902233888 | 1449 |
| train/SMD/machine-3-8/seed2/smd_cf_val | 80 | 80 / 0.1060798278779451 | 75 / 0.1053082233582652 | 1441 |
| train/SMD/machine-3-8/seed3/smd_cf_val | 80 | 80 / 0.1027120561558049 | 79 / 0.101389592650197 | 1452 |
| train/SMD/machine-3-9/seed0/smd_cf_val | 80 | 80 / 0.1197517440818587 | 77 / 0.1185999515900329 | 1447 |
| train/SMD/machine-3-9/seed1/smd_cf_val | 80 | 80 / 0.1195456298393384 | 78 / 0.1189533771676449 | 1453 |
| train/SMD/machine-3-9/seed2/smd_cf_val | 80 | 80 / 0.1189367175156944 | 78 / 0.1186298178971692 | 1452 |
| train/SMD/machine-3-9/seed3/smd_cf_val | 80 | 80 / 0.1178536282307343 | 79 / 0.1177879529437623 | 1397 |
| train/SMD/machine-3-10/seed0/smd_cf_val | 80 | 80 / 0.1038712107758826 | 75 / 0.100538530659765 | 1214 |
| train/SMD/machine-3-10/seed1/smd_cf_val | 80 | 80 / 0.100643642422268 | 80 / 0.100643642422268 | 1240 |
| train/SMD/machine-3-10/seed2/smd_cf_val | 80 | 80 / 0.1032179727284833 | 79 / 0.0993919316092362 | 1218 |
| train/SMD/machine-3-10/seed3/smd_cf_val | 80 | 80 / 0.1032765583541389 | 79 / 0.1019306428468207 | 1234 |
| train/SMD/machine-3-11/seed0/smd_cf_val | 80 | 80 / 0.1185444050916158 | 78 / 0.1181889121675005 | 1470 |
| train/SMD/machine-3-11/seed1/smd_cf_val | 80 | 80 / 0.1157206024032568 | 80 / 0.1157206024032568 | 1448 |
| train/SMD/machine-3-11/seed2/smd_cf_val | 80 | 80 / 0.1154575112788618 | 79 / 0.1151474048078054 | 1447 |
| train/SMD/machine-3-11/seed3/smd_cf_val | 80 | 80 / 0.1163289188999243 | 79 / 0.1159384598446864 | 1501 |
