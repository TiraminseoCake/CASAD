# cfval / ks / pilot_49f630a

- exported: 2026-09-11T16:02:44+0900 (export tool commit 49f630ac8d324ba01390c1a1dcaa4386cd94ae84); training code sha: 49f630ac8d324ba01390c1a1dcaa4386cd94ae84
- result kind: `val_ckpt_eval` (validation-protocol checkpoints evaluated by scripts/eval_ckpt.py; CF OFF/ON on the same base scores)
- jobs: 8 — {'success': 8} — **COMPLETE**
- exported eval jobs: 4, train jobs: 2; duplicates flagged: 0

| dataset | entity | seed | ckpt | epoch | variant | AUC-PR | VUS-PR | Standard-F1 | gamma | calibrate |
|---|---|---|---|---|---|---|---|---|---|---|
| PSM | PSM | 0 | last | 80 | A_off | 0.4317 | 0.4181 | 0.4422 | 1.0 | False |
| PSM | PSM | 0 | last | 80 | A_on | 0.4876 | 0.4534 | 0.4685 | 1.0 | False |
| PSM | PSM | 0 | best_val | 72 | A_off | 0.4297 | 0.4162 | 0.4409 | 1.0 | False |
| PSM | PSM | 0 | best_val | 72 | A_on | 0.4890 | 0.4542 | 0.4689 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_off | 0.5263 | 0.5888 | 0.5120 | 1.0 | False |
| SMD | machine-1-1 | 0 | last | 80 | A_on | 0.4620 | 0.4977 | 0.4189 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_off | 0.5273 | 0.5878 | 0.5132 | 1.0 | False |
| SMD | machine-1-1 | 0 | best_val | 79 | A_on | 0.4608 | 0.4968 | 0.4158 | 1.0 | False |

## Training (validation MAE selection)
| job | epochs | last ep / MAE | best ep / MAE | duration s |
|---|---|---|---|---|
| train/PSM/PSM/seed0/psm_cf_val | 80 | 80 / 0.2194359598502921 | 72 / 0.2189876932551817 | 4733 |
| train/SMD/machine-1-1/seed0/smd_cf_val | 80 | 80 / 0.179562969143687 | 79 / 0.1783938993104982 | 1401 |
