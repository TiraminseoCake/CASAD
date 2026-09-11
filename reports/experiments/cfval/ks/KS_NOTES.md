# ks (legacy server4) notes — campaign cfval, training code 49f630a

SMD coverage is **partial: 8/28 entities (machine-1-1..1-8) x 4 seeds**; PSM 4 seeds. Both packages (pilot_49f630a, remaining_49f630a) together = 36 train / 72 eval / 144 primary fusion rows. Values in [0,1]; deltas in pp.

## SMD per entity (best_val, 4-seed mean; paired CF ON-OFF from the same checkpoint)

| entity | AUC-PR off | AUC-PR on | Δ pp (seeds ↑/↓) | VUS-PR off | VUS-PR on | Δ pp |
|---|---|---|---|---|---|---|
| machine-1-1 | 0.5152 | 0.4202 | -9.49 (0/4) | 0.5792 | 0.4659 | -11.34 |
| machine-1-2 | 0.1763 | 0.3307 | +15.44 (4/0) | 0.1911 | 0.3456 | +15.45 |
| machine-1-3 | 0.2385 | 0.2278 | -1.07 (1/3) | 0.2242 | 0.2263 | +0.21 |
| machine-1-4 | 0.1302 | 0.1517 | +2.15 (4/0) | 0.1158 | 0.1468 | +3.10 |
| machine-1-5 | 0.5203 | 0.5394 | +1.90 (4/0) | 0.3785 | 0.4293 | +5.08 |
| machine-1-6 | 0.8649 | 0.8025 | -6.24 (0/4) | 0.8439 | 0.7683 | -7.56 |
| machine-1-7 | 0.6447 | 0.5086 | -13.61 (0/4) | 0.6530 | 0.5140 | -13.91 |
| machine-1-8 | 0.2584 | 0.2007 | -5.77 (0/4) | 0.2128 | 0.0979 | -11.49 |

## PSM (best_val, 4 seeds)

| seed | AUC-PR off | AUC-PR on | Δ pp | VUS-PR off | VUS-PR on | Δ pp |
|---|---|---|---|---|---|---|
| 0 | 0.4297 | 0.4890 | +5.93 | 0.4162 | 0.4542 | +3.80 |
| 1 | 0.4571 | 0.5322 | +7.51 | 0.4410 | 0.4893 | +4.83 |
| 2 | 0.4575 | 0.4886 | +3.11 | 0.4398 | 0.4549 | +1.52 |
| 3 | 0.4260 | 0.5495 | +12.35 | 0.4144 | 0.5019 | +8.74 |

Selection: validation prediction MAE only (no test involvement); last and best_val both kept. Not a reproduction of colleague paper_align runs (PERM=0 CF-config candidate).
