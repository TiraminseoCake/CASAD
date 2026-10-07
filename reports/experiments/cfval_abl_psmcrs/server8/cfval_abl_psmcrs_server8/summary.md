# cfval_abl_psmcrs / server8 / cfval_abl_psmcrs_server8

- exported: 2026-10-07T11:32:17+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 52 — {'success': 52} — **COMPLETE**
- exported eval jobs: 32, train jobs: 16; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| PSM | PSM | 0 | last | 80 | A_off | 0.4317 | 0.4181 | 0.4422 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_on | 0.4876 | 0.4534 | 0.4685 | 1.0 | False |
| PSM | PSM | 0 | best_val | 72 | A_off | 0.4297 | 0.4162 | 0.4409 | 1.0 | False |
| PSM | PSM | 0 | best_val | 72 | A_on | 0.4890 | 0.4542 | 0.4689 | 1.0 | False |
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
| PSM | PSM | 0 | last | 80 | A_off | 0.4546 | 0.4371 | 0.4397 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_on | 0.4878 | 0.4570 | 0.4737 | 1.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_off | 0.4546 | 0.4371 | 0.4397 | 1.0 | False |
| PSM | PSM | 0 | best_val | 80 | A_on | 0.4878 | 0.4570 | 0.4737 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_off | 0.4471 | 0.4329 | 0.4396 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_on | 0.5394 | 0.4946 | 0.4807 | 1.0 | False |
| PSM | PSM | 1 | best_val | 78 | A_off | 0.4472 | 0.4329 | 0.4394 | 1.0 | False |
| PSM | PSM | 1 | best_val | 78 | A_on | 0.5384 | 0.4939 | 0.4799 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_off | 0.4373 | 0.4247 | 0.4454 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_on | 0.4977 | 0.4611 | 0.4717 | 1.0 | False |
| PSM | PSM | 2 | best_val | 72 | A_off | 0.4380 | 0.4251 | 0.4461 | 1.0 | False |
| PSM | PSM | 2 | best_val | 72 | A_on | 0.4960 | 0.4599 | 0.4710 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_off | 0.4455 | 0.4323 | 0.4474 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_on | 0.5401 | 0.4946 | 0.4828 | 1.0 | False |
| PSM | PSM | 3 | best_val | 78 | A_off | 0.4416 | 0.4283 | 0.4427 | 1.0 | False |
| PSM | PSM | 3 | best_val | 78 | A_on | 0.5404 | 0.4947 | 0.4824 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_off | 0.5625 | 0.5270 | 0.5358 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_on | 0.5248 | 0.4864 | 0.4748 | 1.0 | False |
| PSM | PSM | 0 | best_val | 79 | A_off | 0.5640 | 0.5285 | 0.5342 | 1.0 | False |
| PSM | PSM | 0 | best_val | 79 | A_on | 0.5253 | 0.4864 | 0.4722 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_off | 0.5479 | 0.5118 | 0.5264 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_on | 0.5185 | 0.4897 | 0.5337 | 1.0 | False |
| PSM | PSM | 1 | best_val | 77 | A_off | 0.5492 | 0.5139 | 0.5270 | 1.0 | False |
| PSM | PSM | 1 | best_val | 77 | A_on | 0.5299 | 0.4977 | 0.5320 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_off | 0.5618 | 0.5255 | 0.5149 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_on | 0.5238 | 0.4954 | 0.5051 | 1.0 | False |
| PSM | PSM | 2 | best_val | 78 | A_off | 0.5619 | 0.5251 | 0.5142 | 1.0 | False |
| PSM | PSM | 2 | best_val | 78 | A_on | 0.5235 | 0.4953 | 0.5050 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_off | 0.5611 | 0.5222 | 0.5334 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_on | 0.5560 | 0.5148 | 0.5221 | 1.0 | False |
| PSM | PSM | 3 | best_val | 72 | A_off | 0.5606 | 0.5227 | 0.5349 | 1.0 | False |
| PSM | PSM | 3 | best_val | 72 | A_on | 0.5546 | 0.5113 | 0.5174 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_off | 0.4345 | 0.4212 | 0.4376 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_on | 0.5064 | 0.4707 | 0.4718 | 1.0 | False |
| PSM | PSM | 0 | best_val | 74 | A_off | 0.4343 | 0.4212 | 0.4359 | 1.0 | False |
| PSM | PSM | 0 | best_val | 74 | A_on | 0.5058 | 0.4704 | 0.4720 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_off | 0.4521 | 0.4381 | 0.4467 | 1.0 | False |
| PSM | PSM | 1 | last | 80 | A_on | 0.5372 | 0.4929 | 0.4759 | 1.0 | False |
| PSM | PSM | 1 | best_val | 73 | A_off | 0.4500 | 0.4362 | 0.4472 | 1.0 | False |
| PSM | PSM | 1 | best_val | 73 | A_on | 0.5364 | 0.4924 | 0.4756 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_off | 0.4484 | 0.4343 | 0.4383 | 1.0 | False |
| PSM | PSM | 2 | last | 80 | A_on | 0.4998 | 0.4616 | 0.4722 | 1.0 | False |
| PSM | PSM | 2 | best_val | 80 | A_off | 0.4484 | 0.4343 | 0.4383 | 1.0 | False |
| PSM | PSM | 2 | best_val | 80 | A_on | 0.4998 | 0.4616 | 0.4722 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_off | 0.4454 | 0.4314 | 0.4417 | 1.0 | False |
| PSM | PSM | 3 | last | 80 | A_on | 0.5345 | 0.4899 | 0.4756 | 1.0 | False |
| PSM | PSM | 3 | best_val | 78 | A_off | 0.4451 | 0.4309 | 0.4405 | 1.0 | False |
| PSM | PSM | 3 | best_val | 78 | A_on | 0.5346 | 0.4896 | 0.4757 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/PSM/PSM/seed0/psm_cf_val_perm0_crson | 80 | 80 / 0.2194359598502921 | 72 / 0.2189876932551817 | 4952 |
| train/PSM/PSM/seed1/psm_cf_val_perm0_crson | 80 | 80 / 0.2111137406439951 | 80 / 0.2111137406439951 | 4985 |
| train/PSM/PSM/seed2/psm_cf_val_perm0_crson | 80 | 80 / 0.2104035403865575 | 74 / 0.2093808583795234 | 5051 |
| train/PSM/PSM/seed3/psm_cf_val_perm0_crson | 80 | 80 / 0.2093353842731222 | 78 / 0.2083046531007546 | 4903 |
| train/PSM/PSM/seed0/psm_cf_val_perm0_crsoff | 80 | 80 / 0.2228606312914118 | 80 / 0.2228606312914118 | 4874 |
| train/PSM/PSM/seed1/psm_cf_val_perm0_crsoff | 80 | 80 / 0.2150346761353447 | 78 / 0.2147238144316669 | 4911 |
| train/PSM/PSM/seed2/psm_cf_val_perm0_crsoff | 80 | 80 / 0.212836466651093 | 72 / 0.2127018737965794 | 4880 |
| train/PSM/PSM/seed3/psm_cf_val_perm0_crsoff | 80 | 80 / 0.2083982951837222 | 78 / 0.2063886755988197 | 4902 |
| train/PSM/PSM/seed0/psm_cf_val_perm2_crson | 80 | 80 / 0.3430838127105985 | 79 / 0.3428140536808151 | 10928 |
| train/PSM/PSM/seed1/psm_cf_val_perm2_crson | 80 | 80 / 0.5065519912701868 | 77 / 0.5058700186721906 | 11164 |
| train/PSM/PSM/seed2/psm_cf_val_perm2_crson | 80 | 80 / 0.3654201893632371 | 78 / 0.363837316013811 | 10998 |
| train/PSM/PSM/seed3/psm_cf_val_perm2_crson | 80 | 80 / 0.5433342381109129 | 72 / 0.5381741134949456 | 10966 |
| train/PSM/PSM/seed0/psm_cf_val_perm2_crsoff | 80 | 80 / 0.2170360046909804 | 74 / 0.216843002433977 | 10941 |
| train/PSM/PSM/seed1/psm_cf_val_perm2_crsoff | 80 | 80 / 0.2058484369248357 | 73 / 0.2038518337489263 | 11110 |
| train/PSM/PSM/seed2/psm_cf_val_perm2_crsoff | 80 | 80 / 0.2071009860822054 | 80 / 0.2071009860822054 | 9969 |
| train/PSM/PSM/seed3/psm_cf_val_perm2_crsoff | 80 | 80 / 0.2076064892609464 | 78 / 0.207365846076908 | 10425 |
