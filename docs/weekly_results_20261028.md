# PICAAD 주간 결과 정리 (2026-10-23 ~ 10-28)

## 0. 요약

- **실험 프로토콜을 하나로 맞췄어요.** PICAAD, CAROTS, OracleAD를 같은 데이터 분할, 같은 평가 스크립트로 다시 돌렸어요. PICAAD 쪽은 JS·KS의 ablation 프로토콜(H_B)에 batch만 512로 바꾼 설정이에요. SWaT는 모든 모델에서 5배 다운샘플링 버전을 써요.
- **checkpoint 선택 규칙을 정했어요.** best_smooth를 기본으로 써요. epoch 20 이상에서 val MAE의 3점 이동평균이 가장 낮은 epoch를 골라요.
- **새 base model로 prior alignment loss(tew+teg)를 끈 버전을 채택했어요.** PSM에서는 A-PR이 +4.28pp 올랐고, SWaT_ds5와 SMD28에서는 1pp 이내로 거의 같아요.
- **PSM ablation 결과 (new base)**
  - 6개 변형 모두 4개 seed 전부에서 Full보다 낮아요.
  - 가장 크게 기여하는 건 CRS 정렬과 개입 기반 reference 갱신이에요. 하나만 빼도 A-PR이 −13.9 ~ −14.1pp 떨어져요.
  - δ(−12.1pp)와 Prior(−10.8pp)도 크게 기여해요.
  - 직접 개입 loss는 old base에서는 효과가 없었지만 new base에서는 −4.0pp로 기여해요. Causal Attention mask는 old base에서 효과가 없어서 제외했어요.
- **CAROTS와 비교하면**
  - PSM: PICAAD가 A-PR·V-PR에서 앞서요.
  - SMD28: 비슷하거나 PICAAD가 조금 앞서요.
  - SWaT_ds5: CAROTS가 전반적으로 앞서고, 특히 V-PR은 −9.0pp 차이가 나요.

---

## 1. 공통 실험 프로토콜

| 항목 | 설정 |
|---|---|
| 데이터 | PSM, SMD 28개 엔티티 전체, SWaT 51변수 5배 median 다운샘플링(`data/SWaT_ds5`) |
| train / val 분할 | train 앞 80%는 학습, 뒤 20%는 validation. 모든 모델 동일 |
| 정규화, PCMCI+ prior | train 앞 80%에서만 fit해요 |
| PICAAD 학습 | 80 epoch, batch 512, LR PSM 5e-5 / SMD·SWaT 5e-4, seed 0–3 |
| checkpoint | **best_smooth (기본 규칙)**. best_val(val MAE 최소)과 last도 함께 저장 |
| 이상 점수 | A = P + C. P는 예측 오차, C는 causal 편차이고, calibration 없이 그대로 더해요 |
| 평가 | point label 기준. F1은 최적 threshold, R-F1과 Aff-F는 threshold 100개 탐색, VUS는 이상 구간 길이의 중앙값을 window로 써요. 앞 L−1개 점은 제외 |
| CAROTS | 공식 코드(kimanki/CAROTS@63a41f4)를 수정 없이 사용. 출력 점수는 위 평가 스크립트로 다시 계산 (window 점수를 window의 마지막 시점에 할당) |
| OracleAD | 논문 설명대로 다시 구현한 runner(v2). 출력 점수는 같은 평가 스크립트로 계산 |

모든 수치는 seed 4개 평균(%)이에요. SMD는 seed마다 28개 엔티티를 평균한 뒤 seed 평균을 냈어요. 메트릭 순서는 F1, R-F1, Aff-F, A-ROC, A-PR, V-ROC, V-PR이에요.

---

## 2. 메인 비교: PICAAD vs CAROTS vs OracleAD

- **PICAAD (new base)**: prior alignment loss를 끈 버전이고, 앞으로 기준으로 쓸 모델이에요.
- **PICAAD (old base)**: tew+teg가 켜진 이전 Full 모델이에요.
- 굵게 표시한 값은 데이터셋별 최고값이에요.

### PSM

| 모델 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|
| PICAAD (new base) | 53.97 | 42.13 | **77.87** | 75.28 | **58.22**±2.84 | **71.76** | **54.69**±2.54 |
| PICAAD (old base) | 54.94 | 44.34 | 77.61 | 74.45 | 53.94±5.11 | 70.93 | 51.20±4.03 |
| CAROTS | **56.76** | **46.78** | 72.79 | **75.75** | 53.17±3.52 | 69.46 | 48.89±5.46 |
| OracleAD | 46.68 | 38.89 | 73.14 | 66.22 | 45.19±0.57 | 60.22 | 41.60±0.51 |

### SWaT_ds5

| 모델 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|
| PICAAD (new base) | 76.03 | 21.35 | 74.20 | 84.01 | 74.02±0.68 | 74.50 | 56.74±0.41 |
| PICAAD (old base) | 76.04 | 21.81 | 74.41 | 84.41 | 74.66±1.01 | 74.68 | 56.83±0.71 |
| CAROTS | **79.63** | **34.47** | **80.19** | **85.36** | **75.90**±1.03 | **79.18** | **65.74**±1.69 |
| OracleAD | 75.99 | 23.92 | 70.18 | 83.07 | 74.29±0.61 | 68.44 | 49.27±4.69 |

### SMD (28개 엔티티)

| 모델 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|
| PICAAD (new base) | 48.13 | 40.37 | 86.12 | 81.96 | 43.92±0.34 | **84.24** | 41.71±0.43 |
| PICAAD (old base) | 48.30 | **40.57** | **86.26** | 81.86 | **44.04**±0.59 | 84.04 | **41.77**±0.63 |
| CAROTS | **49.45** | 30.71 | 78.50 | **82.16** | 43.54±1.12 | 83.85 | 38.87±0.88 |
| OracleAD | 47.86 | 33.01 | 79.03 | 80.50 | 43.42±0.43 | 81.02 | 34.40±0.82 |

### 참고: SMD 개별 엔티티 (machine-2-1, machine-3-7)

| 엔티티 | 모델 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|---|
| machine-2-1 | PICAAD (new base) | 21.68 | **32.59** | 88.00 | 66.17 | 17.22 | 69.75 | 17.50 |
| | PICAAD (old base) | 21.79 | 32.18 | 88.28 | 66.53 | 17.56 | 70.12 | 17.87 |
| | CAROTS | 24.31 | 24.96 | 79.16 | **72.04** | 17.58 | **75.74** | 17.89 |
| | OracleAD | **32.60** | 32.52 | **92.95** | 68.10 | **28.95** | 72.83 | **28.93** |
| machine-3-7 | PICAAD (new base) | 32.41 | **18.19** | 66.71 | 68.41 | 23.19 | 72.51 | 17.97 |
| | PICAAD (old base) | 32.26 | **18.19** | 66.71 | 68.33 | 22.84 | 72.46 | 16.84 |
| | CAROTS | **54.30** | 10.04 | 66.71 | **79.78** | **42.82** | **82.36** | **34.81** |
| | OracleAD | 34.49 | 10.97 | 66.71 | 65.13 | 26.87 | 63.44 | 12.92 |

### 비교 메모

- **PSM**: new base가 A-PR(+5.1pp vs CAROTS), V-PR(+5.8pp vs CAROTS) 모두 최고예요. seed 편차도 old base(±5.1)보다 줄었어요(±2.8). 다만 F1, R-F1, A-ROC는 CAROTS가 높아요.
- **SWaT_ds5**: CAROTS가 7개 메트릭 모두 앞서요. A-PR 차이는 −1.9pp로 작지만, **V-PR −9.0pp, R-F1 −13.1pp**로 구간 단위 탐지에서 차이가 커요. 가장 큰 미해결 과제예요.
- **SMD28**: PICAAD가 R-F1(+9.7pp), Aff-F(+7.6pp), V-PR(+2.8pp)에서 앞서고, A-PR은 세 모델이 비슷해요(43.4–44.0).
- **SMD 2-1, 3-7**: PICAAD가 약한 엔티티예요. 2-1은 OracleAD가, 3-7은 CAROTS가 크게 앞서요.
- **OracleAD 재현 문제**: 우리 재구현의 PSM A-PR(45.19)은 논문 수치(68.11)와 동료의 재구현(55.37)보다 낮아요. 동료 코드(CTSAD f3b9aa4)를 받아야 원인을 확인할 수 있어요.

---

## 3. Prior alignment loss 제거 확인 실험

**목적**: PSM ablation에서 prior alignment loss(tew: routing과 prior 강도의 JSD, teg: gate와 prior 연결의 BCE)를 끄면 성능이 올랐어요. 이게 다른 데이터셋에서도 유지되는지 확인했어요.

- 끈 것: tew, teg (`PICAAD.ENABLE_PRIOR_LOSS False`)
- 그대로 둔 것: CRS 정렬(cstruct), routing logit의 prior 항, causal attention mask, reference 초기값
- **판정 기준(실험 전에 정함)**: SWaT_ds5와 SMD28 모두 A-PR·V-PR 하락이 1pp 이내면 채택해요.

| 데이터셋 | 모델 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|---|
| PSM | old base | 54.94 | 44.34 | 77.61 | 74.45 | 53.94 | 70.93 | 51.20 |
| | align off | 53.97 | 42.13 | 77.87 | 75.28 | 58.22 | 71.76 | 54.69 |
| | **Δ** | −0.97 | −2.21 | +0.26 | +0.83 | **+4.28** | +0.83 | **+3.49** |
| SWaT_ds5 | old base | 76.04 | 21.81 | 74.41 | 84.41 | 74.66 | 74.68 | 56.83 |
| | align off | 76.03 | 21.35 | 74.20 | 84.01 | 74.02 | 74.50 | 56.74 |
| | **Δ** | −0.01 | −0.45 | −0.21 | −0.40 | **−0.64** | −0.18 | **−0.09** |
| SMD28 | old base | 48.30 | 40.57 | 86.26 | 81.86 | 44.04 | 84.04 | 41.77 |
| | align off | 48.13 | 40.37 | 86.12 | 81.96 | 43.92 | 84.24 | 41.71 |
| | **Δ** | −0.17 | −0.20 | −0.14 | +0.10 | **−0.12** | +0.20 | **−0.06** |

- **결론**: 기준을 통과해서 채택했어요. PSM에서는 크게 개선되고, 나머지 두 데이터셋은 차이가 없어요. 학습 loss도 두 개 줄어요.
- **seed별 A-PR 차이**
  - PSM: 4개 중 3개에서 올랐어요.
  - SWaT: −0.39 / +0.40 / −1.31 / −1.25로, 작지만 떨어지는 쪽이 많아요.
  - SMD: −0.55 / +0.36 / −0.55 / +0.27이에요. 엔티티별로는 A-PR이 오른 곳 16개, 떨어진 곳 12개예요. 가장 많이 떨어진 엔티티는 machine-3-8(−3.9pp)과 machine-3-10(−3.1pp)이에요.
- **checkpoint 규칙을 바꿔도(best_val, last) 같은 결론이에요.**

---

## 4. PSM ablation (old base 기준, 완료)

각 변형은 Full(old base)에서 구성요소 하나만 뺀 모델이에요. Δ는 같은 seed끼리 Full과 뺀 값의 평균이고, 괄호 안은 4개 seed 중 Full보다 낮았던 seed 수예요.

| 변형 | 바꾼 설정 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR | ΔA-PR | ΔV-PR |
|---|---|---|---|---|---|---|---|---|---|---|
| **Full (old base)** | – | 54.94 | 44.34 | 77.61 | 74.45 | 53.94 | 70.93 | 51.20 | – | – |
| w/o δ (동적 routing) | DYNAMIC_GRAPH False | 45.05 | 43.66 | 78.62 | 63.98 | 46.53 | 62.40 | 44.67 | −7.41 (4/4) | −6.53 (4/4) |
| w/o CRS loss | START_CLS_EPOCH 81 | 44.11 | 49.52 | 79.19 | 62.29 | 44.40 | 61.02 | 43.04 | −9.54 (4/4) | −8.16 (4/4) |
| w/o Intervention (I0U0) | PERM_PAIRS_PER_BATCH 0 | 44.48 | 43.07 | 79.07 | 62.40 | 44.75 | 61.04 | 43.21 | −9.19 (4/4) | −7.99 (4/4) |
| w/o ref. update (I1U0) | UPDATE_REFERENCE False | 44.05 | 44.11 | 79.33 | 62.38 | 45.43 | 61.07 | 43.92 | −8.51 (4/4) | −7.28 (4/4) |
| w/o int. loss (I0U1) | APPLY_LOSS False | 51.79 | 43.38 | 79.24 | 71.45 | 54.33 | 67.90 | 50.00 | +0.39 (2/4) | −1.20 (4/4) |
| w/o prior align (tew+teg) | ENABLE_PRIOR_LOSS False | 53.97 | 42.13 | 77.87 | 75.28 | 58.22 | 71.76 | 54.69 | +4.28 (1/4) | +3.49 (1/4) |
| w/o Prior | PRIOR.TYPE none | 46.08 | 41.67 | 78.87 | 65.35 | 47.43 | 63.62 | 45.53 | −6.51 (4/4) | −5.67 (4/4) |
| w/o Causal Attn mask | CAUSAL_ATTN_MASK_SCALE 0 | 50.96 | 42.35 | 76.46 | 71.73 | 54.68 | 68.07 | 50.87 | +0.74 (2/4) | −0.33 (2/4) |

**해석**

1. **CRS 정렬과 개입 기반 reference 갱신이 핵심이에요.** 개입 측정값은 두 경로로 쓰여요.
   - I: 측정값을 직접 맞추는 loss
   - U: 측정값으로 CRS reference를 갱신하는 경로

   U를 끄거나(I1U0) CRS 자체를 끄면 A-PR이 44–45 수준으로 떨어져요. I만 끄면(I0U1) 거의 변화가 없어요. 그래서 기여는 **"개입 반응으로 만든 정상 reference에 맞춰 학습한다"**로 설명하는 게 맞아요. 동료 보고서의 결론과도 같은 방향이에요.
2. **δ와 Prior도 4개 seed 모두에서 기여해요.** Prior를 빼면 학습 예측 오차는 더 낮아지는데(epoch 80 기준 0.147 vs Full 0.166) 탐지 성능은 떨어져요.
3. **Causal Attn mask와 직접 개입 loss는 PSM에서 효과가 없어요.**
4. **prior alignment loss는 오히려 방해가 돼요.** 그래서 3절의 확인 실험을 거쳐 새 base로 채택했어요.
5. **checkpoint 규칙을 바꿔도 결론은 같아요.** PSM은 val loss가 끝까지 줄어서 best_smooth, best_val, last가 모두 epoch 75–80을 골랐고, 수치 차이는 0.2pp 이내예요.

동료 결과와 비교하면, 효과의 방향은 모두 같고 크기는 조금 작아요. δ는 동료 −11.50pp vs 우리 −7.41pp, reference 갱신은 −10.21pp vs −8.51pp예요.

---

## 5. PSM ablation (new base 기준, 완료)

각 변형은 Full(new base, prior alignment loss off)에서 구성요소 하나만 뺀 모델이에요. 표기 방식은 4절과 같아요. Causal Attn 변형은 old base에서 효과가 없어서 제외했어요. 새 base에서 CRS loss를 끄면 L_C 전체가 0이 돼요(tew와 teg가 이미 꺼져 있기 때문이에요).

| 변형 | 바꾼 설정 | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR | ΔA-PR | ΔV-PR |
|---|---|---|---|---|---|---|---|---|---|---|
| **Full (new base)** | – | 53.97 | 42.13 | 77.87 | 75.28 | 58.22 | 71.76 | 54.69 | – | – |
| w/o δ (동적 routing) | DYNAMIC_GRAPH False | 44.80 | 44.03 | 78.95 | 63.60 | 46.12 | 62.08 | 44.33 | −12.09 (4/4) | −10.36 (4/4) |
| w/o CRS loss | START_CLS_EPOCH 81 | 43.91 | 47.34 | 78.99 | 61.98 | 44.11 | 60.73 | 42.79 | −14.11 (4/4) | −11.90 (4/4) |
| w/o Intervention (I0U0) | PERM_PAIRS_PER_BATCH 0 | 44.51 | 43.45 | 79.29 | 62.28 | 44.13 | 60.93 | 42.69 | −14.08 (4/4) | −12.00 (4/4) |
| w/o ref. update (I1U0) | UPDATE_REFERENCE False | 43.93 | 44.19 | 79.49 | 62.08 | 44.32 | 60.83 | 42.98 | −13.90 (4/4) | −11.72 (4/4) |
| w/o int. loss (I0U1) | APPLY_LOSS False | 49.46 | 42.29 | 78.96 | 69.88 | 54.26 | 66.90 | 50.26 | −3.96 (4/4) | −4.43 (4/4) |
| w/o Prior | PRIOR.TYPE none | 46.08 | 41.67 | 78.87 | 65.35 | 47.43 | 63.62 | 45.53 | −10.79 (4/4) | −9.16 (4/4) |

**해석**

1. **모든 변형이 4개 seed 전부에서 Full보다 낮아요.** old base 때보다 기여가 더 뚜렷해요.
2. **CRS 정렬과 reference 갱신이 여전히 핵심이에요.** CRS, I0U0, I1U0을 끄면 모두 A-PR 44 수준으로 떨어져요(−13.9 ~ −14.1pp). 셋이 거의 같은 수준이라, "개입 반응으로 갱신한 reference에 CRS를 맞추는 경로"가 하나의 단위로 작동한다고 볼 수 있어요.
3. **δ(−12.1pp)와 Prior(−10.8pp)의 기여가 old base(−7.4, −6.5pp)보다 커요.** w/o Prior는 prior가 없어 tew·teg가 원래 작동하지 않으므로 old base와 같은 run이에요(수치 동일). 따라서 Prior의 기여가 커진 건 Full이 올라간 효과예요.
4. **직접 개입 loss(I0U1)가 이제 기여해요.** old base에서는 +0.39pp로 효과가 없었는데, 새 base에서는 −3.96pp(4/4)예요. prior alignment loss가 빠지면서 직접 개입 loss가 하는 역할이 드러난 것으로 보여요. 다만 seed 간 편차(±3.1)가 커서 크기는 조심해서 봐야 해요.
5. checkpoint는 대부분 epoch 77–80이 선택됐어요.

---

## 6. 남은 과제

| 과제 | 내용 |
|---|---|
| SWaT V-PR 격차 | CAROTS 대비 −9.0pp, R-F1 −13.1pp. 구간 단위 탐지가 약한 원인을 분석해야 해요 |
| 논문 수정 | L_C 정의를 cstruct만으로 바꾸고, prior의 역할을 "routing 초기 구조 지침"으로 다시 써야 해요. 주 성능표도 new base 수치로 바꿔요 |
| 코드와 논문 불일치 | L_int의 stop-gradient(코드는 detach 안 함), L_crs KL 방향(코드는 KL(CRS‖E)), ψ 자기 연결 bias +1.0 |
| OracleAD 재현 차이 | PSM A-PR: 우리 45.19, 동료 55.37, 논문 68.11. 동료 코드를 받아 비교해야 해요 |
| 추가 ablation | SMD, SWaT_ds5에서 핵심 변형 확인. Freeze-4, Random prior 변형은 아직 구현하지 않았어요 |
| Folded routing | PSM에서 ORIGINAL vs FOLDED 4-seed 비교 진행 중(10/28 저녁 시작) |

---

## 부록: 결과 파일 위치

| 내용 | 경로 |
|---|---|
| PICAAD old base (PSM / SMD / SWaT_ds5) | `results/hb/{PSM,SMD,SWaT_ds5}` |
| PICAAD new base, SMD / SWaT_ds5 | `results/ablation_hb/{SMD,SWaT_ds5}/no_prioralign` |
| PSM ablation, old base (new base Full 포함) | `results/ablation_hb/PSM/<variant>` |
| PSM ablation, new base | `results/ablation_hb/PSM_noalign/<variant>` |
| CAROTS 평가 | `results/bench/eval_carots.csv` |
| OracleAD 평가 | `results/bench/eval_oraclead_v2_{PSM,SMD,SWaT_ds5}.csv` |
| 실행 스크립트 | `scripts/run_hb_protocol.sh`, `scripts/run_psm_ablation.sh`, `scripts/run_noalign_check.sh`, `scripts/run_psm_ablation_noalign.sh` |
