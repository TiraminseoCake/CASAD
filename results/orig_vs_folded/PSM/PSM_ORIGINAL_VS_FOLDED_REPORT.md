# PSM: ORIGINAL vs FOLDED Routing 비교

- 작성일: 2026-10-28
- 범위: PSM, seed 0–3, 두 조건만 비교 (다른 데이터셋과 추가 ablation은 실행하지 않음)
- 모델 자동 교체 없음

## 요약

- FOLDED 평균은 A-PR 54.80 / V-PR 51.95, ORIGINAL 평균은 58.22 / 54.69입니다.
- paired 차이 평균은 **A-PR −3.42pp, V-PR −2.74pp**입니다.
  - 95% CI: A-PR [−10.78, +3.94], V-PR [−8.79, +3.30]
  - 4개 seed 중 3개에서 낮았습니다.
- 차이의 대부분은 **seed 0 한 개(A-PR −10.21pp)**에서 나옵니다.
  - 나머지 3개 seed의 차이: −1.41 / −2.18 / +0.12
- 주 score(A = P+C)와 보조 score(P_raw)의 결과가 거의 같습니다.
- **판단: 이 결과만으로는 "성능이 유지된다"는 근거로 Folded 채택을 지지하기 어렵습니다.** 평균 하락이 통계적으로 확인된 것도 아닙니다. CI가 넓고, 한 seed의 영향이 큽니다. 아래 "남은 불확실성"을 참고하세요.

## 1. 비교 조건

| 조건 | routing score | ψ 초기값 |
|---|---|---|
| ORIGINAL | ψ + 0.35·log W + Δ(X) | self-loop +1 + 0.25·log W |
| FOLDED | ψ + Δ(X) | self-loop +1 + 0.60·log W |

- a = `PRIOR.INIT_SCALE` = 0.25, b = `PRIOR.BLEND` = 0.35이며, 실제 실행 config에서 확인한 값입니다.
- 두 경로는 같은 W와 같은 clamp(1e-8)를 씁니다.
- gate 초기값(0.5·a·logit M)은 바꾸지 않았습니다.
- 그 외 구성(gate, attention, Δ, loss, reference 갱신, scoring)은 두 조건이 같습니다. 자세한 내용은 `docs/psm_orig_vs_folded_setting.md`에 있습니다.

## 2. 프로토콜과 재사용 근거

| 항목 | 값 |
|---|---|
| 데이터 | `data/PSM`, point label |
| 분할 | train 앞 80% 학습, 뒤 20% validation |
| 표준화, PCMCI+ | train 앞 80%에서만 fit (prior cache `PSM_PSM_pcmci_d7f036a2…`, 8개 run 모두 같은 cache 사용) |
| 학습 | AdamW lr 5e-5, wd 0.01, scheduler 없음, grad clip 1.0, batch 512, 80 epoch |
| Loss | L_pred(L1) + 1.0·CRS(epoch ≥ 5) + 0.1·Intervention. prior alignment(tew, teg) 꺼짐 |
| Checkpoint | best_smooth: val MAE 3점 이동평균 최소, epoch ≥ 20. test는 선택에 쓰지 않음 |
| Score | A = P + C (raw, calibration 없음). 보조로 P_raw |
| 평가 | `paper_eval`. window 점수를 마지막 시점에 할당. A-PR은 average precision, VUS window는 이상 구간 길이의 중앙값 |

**ORIGINAL 재사용** (`results/ablation_hb/PSM/no_prioralign`, 10-26 실행)

- 학습 코드는 10-24 이후 바뀌지 않았습니다.
- FOLDED 코드와 다른 파일은 Folding을 넣은 3개(`config.py`, `model/build.py`, `model/modeling_picaad.py`)뿐입니다. 해시는 `provenance/code_hashes.txt`에 있습니다.
- resolved config의 차이는 `FOLD_INTO_PSI`, `PSI_INIT_COEFF`(기본값 −1, 즉 a+b) 키와 결과 경로뿐입니다. 자세한 내용은 `provenance/config_diff_orig_vs_folded.txt`에 있습니다.
- 다시 평가한 A 지표와 각 run이 기록한 지표의 차이는 최대 5.6e-17입니다.
- **실행 환경 차이**: ORIGINAL은 GPU 하나에 job 여러 개를 함께 돌렸고, FOLDED는 GPU당 job 1개로 돌렸습니다. 설정은 같고 GPU 비결정성만 다릅니다.

**실행 전 검증** (이전 Folding 검증을 재사용하고, 이번 설정에 필요한 항목만 추가 확인)

- ψ 외 초기 parameter와 buffer: 같음
- 초기 routing weight 차이: 최대 1.2e-7
- loss 차이: perm을 뺀 나머지는 ≤ 2e-9
  - perm은 상대 2.5e-4 차이가 납니다. 초기 ReLU 경계에서 반올림 차이가 생기기 때문입니다.
- RNG(데이터 순서, 개입 샘플링): 같음
- gate와 Δ(30 step 변화량, ORIGINAL / FOLDED)
  - edge_log_alpha: 8.17e-3 / 8.16e-3
  - dynamic_q: 5.06e-3 / 5.04e-3
- checkpoint 복원
  - FOLDED checkpoint는 `_prior_folded=True`로 복원되어 bias가 다시 더해지지 않습니다.
  - 기존 checkpoint는 기존 방식으로 복원되며 출력이 같습니다.
  - 이번 FOLDED run 4개 모두 `prior_folded=True`를 확인했습니다.
- 초기 함수는 대응하지만, 학습 궤적은 같지 않습니다. AdamW weight decay가 접힌 prior 성분에도 걸리고, 초기 perm ReLU 경계 차이도 있기 때문입니다.

## 3. 결과

### 3.1 seed별 결과 (best_smooth, 주 score A = P+C)

| seed | ORIGINAL ep | ORIGINAL A-PR | ORIGINAL V-PR | FOLDED ep | FOLDED A-PR | FOLDED V-PR | ΔA-PR | ΔV-PR |
|---|---|---|---|---|---|---|---|---|
| 0 | 79 | 60.34 | 56.28 | 80 | 50.13 | 48.12 | **−10.21** | **−8.16** |
| 1 | 80 | 54.52 | 51.47 | 78 | 53.12 | 50.44 | −1.41 | −1.03 |
| 2 | 77 | 60.54 | 57.12 | 80 | 58.36 | 54.78 | −2.18 | −2.34 |
| 3 | 80 | 57.46 | 53.91 | 80 | 57.58 | 54.46 | +0.12 | +0.56 |

### 3.2 평균 ± 표본 표준편차 (주 score A)

| 조건 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|
| ORIGINAL | 53.97±1.80 | 42.13±0.23 | 77.87±0.53 | 75.28±1.74 | **58.22±2.84** | 71.76±1.94 | **54.69±2.54** |
| FOLDED | 52.77±0.77 | 42.23±1.00 | 77.76±1.06 | 73.78±0.89 | **54.80±3.88** | 70.67±0.79 | **51.95±3.23** |

### 3.3 paired 차이 (FOLDED − ORIGINAL, pp, t 분포 df = 3)

| score | 지표 | 평균 | 표준편차 | 95% CI | 부호 (+/−) |
|---|---|---|---|---|---|
| A | A-PR | −3.42 | 4.63 | [−10.78, +3.94] | 1 / 3 |
| A | V-PR | −2.74 | 3.80 | [−8.79, +3.30] | 1 / 3 |
| P_raw | A-PR | −3.37 | 4.66 | [−10.78, +4.04] | 1 / 3 |
| P_raw | V-PR | −2.71 | 3.86 | [−8.85, +3.43] | 1 / 3 |

나머지 지표의 paired 결과는 `analysis/paired_comparison.csv`에 있습니다.

### 3.4 주 score와 P_raw의 일관성

- 8개 run 모두 A와 P_raw의 A-PR 차이가 0.35pp 이내입니다.
- paired 차이의 방향과 크기도 같습니다.
- 따라서 이번 차이는 C score 때문이 아니라 **예측 경로(P) 자체**에서 생긴 것입니다.

### 3.5 seed 0의 큰 하락

| | ORIGINAL | FOLDED |
|---|---|---|
| 선택 epoch의 val MAE | 0.481 | 0.570 |
| test A-PR 기록 (5 epoch마다, 선택에는 미사용) | epoch 10 이후 59–66 | epoch 10에 48.5로 떨어진 뒤 50 근처 유지 |
| best_val A-PR | 60.23 | 50.13 |
| last A-PR | 60.08 | 50.13 |

- FOLDED seed 0은 학습 초반(epoch 10 이전)에 다른 해로 갈라졌고, validation 예측 오차도 18% 높습니다.
- 어떤 checkpoint 규칙을 써도 결과가 같습니다.
- 다른 seed에서는 val MAE 방향이 일정하지 않습니다.
  - seed 3: FOLDED val MAE가 더 낮고, A-PR은 같습니다.
  - seed 1: FOLDED val MAE가 조금 낮고, A-PR은 −1.4pp입니다.

## 4. 해석과 남은 불확실성

1. **Folded 채택을 지지한다고 말하기 어렵습니다.**
   - 평균은 −3.4pp이고, 4개 중 3개 seed에서 낮습니다.
   - seed 0을 빼도 평균은 −1.2pp입니다.
   - 반대로 CI가 0을 포함하므로 하락이 확인된 것도 아닙니다. seed 4개로는 두 방향 모두 결론을 낼 수 없습니다.
2. **원인을 분리하지 못했습니다.** 이론적으로 두 방식의 차이는 두 가지입니다.
   - weight decay가 ψ를 당기는 기준점. ORIGINAL은 prior 쪽, FOLDED는 균등 쪽으로 당깁니다. PSM 기준 접힌 성분의 감쇠는 약 0.8%입니다.
   - 초기 perm ReLU 경계 반올림 차이
   
   두 번째 원인만으로도 seed 0처럼 궤적이 크게 갈라질 수 있습니다. ORIGINAL 자체의 seed 간 편차도 ±2.8pp(old base에서는 ±5.1pp)로 큽니다.
3. **실행 간 비결정성의 크기를 모릅니다.** 같은 설정·같은 seed로 ORIGINAL을 다시 돌렸을 때 결과가 얼마나 흔들리는지 측정한 적이 없습니다. 그래서 seed 0의 −10pp가 Folding 때문인지, 단순한 궤적 분기인지 이 실험으로는 구분할 수 없습니다.

## 5. 다음 단계 제안 (실행하지 않음, 연구팀 결정 필요)

1. **실행 간 비결정성 측정**: ORIGINAL seed 0–3을 같은 설정으로 한 번 더 돌립니다(4 run, 약 2.5시간). ORIGINAL끼리의 차이가 FOLDED와의 차이만큼 크다면, 이번 결과는 노이즈로 봐야 합니다.
2. **seed 확장**: 두 조건 모두 seed 4–7을 추가합니다(8 run).
3. 두 단계 모두 끝나기 전까지 최종 모델은 ORIGINAL로 유지하는 것을 권장합니다.

## 산출물

| 파일 | 내용 |
|---|---|
| `analysis/per_seed_metrics.csv` | 조건 × seed × score(A, P_raw)별 전체 지표, 각 run 자체 CSV 값과의 대조 |
| `analysis/paired_comparison.csv` | score × 지표별 평균, 표준편차, seed별 차이, 95% CI, 부호 |
| `provenance/` | 코드·데이터 해시, Folding diff, ORIGINAL과 FOLDED의 resolved config, config diff, 실행 및 평가 스크립트, ORIGINAL 실행 명령 |
| `folded/PSM_seed*/` | FOLDED run (checkpoint, val curve, epoch별 지표) |
| `queue.log`, `analysis.log` | 실행 및 평가 로그 |

## 추가: seed 4–7 확장 (2026-10-29, 8 seed)

- 같은 설정으로 seed 4–7을 두 조건에서 새로 학습했어요(8 run, 모두 exit 0). 평가는 `analysis_s0to7/`에 있고, 재계산한 A와 run CSV의 차이는 최대 5.6e-17이에요.

| Seed | ORIGINAL A-PR / V-PR | FOLDED A-PR / V-PR | ΔA-PR | ΔV-PR |
|---|---|---|---|---|
| 0 | 60.34 / 56.28 | 50.13 / 48.12 | −10.21 | −8.16 |
| 1 | 54.52 / 51.47 | 53.12 / 50.44 | −1.41 | −1.03 |
| 2 | 60.54 / 57.12 | 58.36 / 54.78 | −2.18 | −2.34 |
| 3 | 57.46 / 53.91 | 57.58 / 54.46 | +0.12 | +0.56 |
| 4 | 60.97 / 56.69 | 57.37 / 53.73 | −3.60 | −2.96 |
| 5 | 54.63 / 50.67 | 56.29 / 51.94 | +1.66 | +1.27 |
| 6 | 60.47 / 55.95 | 58.60 / 54.11 | −1.88 | −1.84 |
| 7 | 55.61 / 51.15 | 56.93 / 52.91 | +1.32 | +1.76 |
| **Mean ± sd** | **58.07±2.84 / 54.15±2.71** | 56.05±2.94 / 52.56±2.30 | **−2.02** | **−1.59** |
| 95% CI (t₇) | | | [−5.17, +1.12] | [−4.24, +1.05] |
| FOLDED 우세 seed | | | 3/8 | 3/8 |

- P_raw도 같은 방향이에요(ΔA-PR −2.01, CI [−5.12, +1.10]).
- seed 0을 빼면 ΔA-PR 평균은 −0.85(seed 1–7)이고, 새 seed 4–7만 보면 −0.63이에요.
- 결론: 8 seed에서도 FOLDED가 ORIGINAL보다 낫다는 근거는 없어요. 차이는 유의하지 않고, 평균은 ORIGINAL 쪽이에요. ORIGINAL 유지 권고는 그대로예요.
