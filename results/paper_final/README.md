# PICAAD 논문 실험 결과 모음

논문 Experiments 섹션(`sources/experiments_revised.tex`)에 들어가는 수치를 모두 원본 run에서 다시 계산해 모은 폴더예요.

- 다시 만들기: `python scripts/collect_paper_results.py` (CASAD 루트에서, oraclead env)
- 원본 run은 읽기만 해요. 스크립트가 논문 수치와 대조해서, 다르면 멈춰요.
- 지표는 %, 순서는 F1, R-F1, Aff-F, A-ROC, A-PR, V-ROC, V-PR이에요.
- SMD는 seed마다 28개 machine의 macro 평균을 낸 뒤, seed 평균을 내요.

## 공통 프로토콜

| 항목 | 설정 |
|---|---|
| 데이터 | PSM, SMD 28 machine, SWaT 51변수 5배 다운샘플(SWaT_ds5) |
| 분할 | train 앞 80% 학습, 뒤 20% validation. 정규화와 PCMCI+는 앞 80%에서만 fit |
| PICAAD | 80 epoch, batch 512, LR PSM 5e-5 / SMD·SWaT 5e-4, prior alignment OFF, A = P + C |
| checkpoint | best_smooth (epoch ≥ 20, val MAE 3점 이동평균 최소) |
| 평가 | 공통 evaluator(`paper_eval_one`), point adjustment 없음, t ≥ L−1, VUS window = 이상 구간 길이 중앙값 |
| seed | 0–3 (T4b만 0–7) |

## 표와 파일

| 논문 표 | 내용 | 요약 파일 (`tables/`) | run별 파일 (`per_run/`) | 원본 |
|---|---|---|---|---|
| `tab:dataset_statistics` | 데이터셋 통계 | `T1_dataset_statistics.csv` | – | `data/*/*.npz` |
| `tab:performance_comparison` (OracleAD, CAROTS, PICAAD 열) | 메인 비교 | `T2_main_ours_vs_causal.csv` | `T2_main_per_run.csv` | PICAAD: `results/ablation_hb/<DS>/no_prioralign` / CAROTS: `results/bench/eval_carots.csv` / OracleAD: `~/oraclead_faithful_v1/runs/floor_ep20/analysis/per_run.csv` |
| `tab:ablation` | PSM 구성요소 ablation | `T3_ablation_psm.csv` | `T3_ablation_per_run.csv` | `results/ablation_hb/PSM_noalign/<variant>`, + prior-align은 `results/hb/PSM` |
| `tab:prior_usage` (a) | prior-alignment loss ON − OFF | `T4a_prior_alignment_onoff.csv` | `T4a_prior_alignment_per_run.csv` | ON: `results/hb/<DS>` / OFF: `results/ablation_hb/<DS>/no_prioralign` |
| `tab:prior_usage` (b) | Persistent bias vs Folded (PSM, 8 seed) | `T4b_persistent_vs_folded_psm.csv` | `T4b_folded_per_seed.csv` | `results/orig_vs_folded/PSM/analysis_s0to7` |
| `tab:score_ablation` | P / C / P+C | `T5_score_components.csv` | `T5_score_components_per_run.csv` | `results/score_components` |

## 주의

- Table 2의 나머지 baseline 10개 열(A.E ~ CATCH)은 원래 draft PDF에 있던 값이에요. 이 폴더에는 원본 run이 없고, 같은 프로토콜로 돌렸는지 아직 확인하지 않았어요.
- OracleAD는 공식 코드가 없어서 JS가 다시 구현한 코드(CTSAD bundle e8f4a9f)로 돌렸어요. 이 코드는 외부 공유나 GitHub 업로드를 하지 않아요.
- OracleAD 논문에 보고된 PSM A-PR 68.11은 이 프로토콜의 결과가 아니라서 표에 쓰지 않아요.
