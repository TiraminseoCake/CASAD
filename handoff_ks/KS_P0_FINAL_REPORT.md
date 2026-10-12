# KS P0 최종 보고 — SMD 28 entity CRS×PERM 통합 분석, SWaT 진행 상태, ks 결과 게시

- 작성: ks 에이전트, 2026-10-12 (KST). 기준 문서: `Picaad_v3.md`.
- 범위: 학습 코드 trainer B `49f630ac8d324ba01390c1a1dcaa4386cd94ae84`. 각 run의 best_val checkpoint(validation 예측 MAE 기준으로 선택)를 평가한 결과만 사용했다.
- 하지 않은 것: 새 학습, test 재평가, 새 점수 조합 탐색, 코드 수정, 진행 중 프로세스 변경. trainer A(`3151f58`) 재현 결과와 test 기준으로 고른 checkpoint는 섞지 않았다.
- 경로 표기: `<RUNS>`는 ks launcher 출력 루트, `<BOOTSTRAP>`는 실행 checkout 밖의 설정·manifest 루트다.
- 함께 제출한 파일: `smd28_crs_perm_paired.csv`, `smd28_entity_effects.csv`, `smd28_uncertainty.csv`, `coverage_and_provenance.json`, `P3_STRUCTURAL_ABLATION_PLAN.md`, `scripts/`, `supporting/smd28_runs.csv`

---

## 0. 요약

1. **SWaT CRS×PERM은 아직 학습 중이다(결과 없음).**
   - 상태(10-12 17:58): `cfval_abl_swatcrs2`의 PERM0 학습 4개가 5~6/80 epoch까지 진행됐다. PERM2 학습 4개와 eval 16개는 대기 중이다. 실패는 0이다.
   - 실측 속도는 epoch당 21~23분이다.
   - **예상 종료는 10-16 오후~밤이다(추정치).** v3에 적었던 10-17 저녁보다 당겨졌다. 2 epoch 측정 대신 4~5 epoch 측정을 쓴 결과다.
   - launcher·GPU 배정은 그대로 두었다.
2. **SMD 28 entity(448 run)에서 CRS×PERM 상호작용은 0과 구별되지 않는다.**
   - 주 지표 P_raw AUC-PR 상호작용 = **−0.0016**, entity cluster bootstrap 95% CI **[−0.0136, +0.0106]**(B=10000, seed 20261012).
   - 양수 entity 14개, 음수 entity 14개다.
   - PERM2에서의 CRS 효과는 −0.0006, CI [−0.0126, +0.0117]이다.
3. **PSM의 상호작용 +0.1153(4/4 seed)은 SMD 평균에서 재현되지 않는다.**
   - PSM 값은 SMD28 95% CI의 상한(+0.0106)보다 10배 이상 크다.
   - 다만 SMD에서는 entity 간 이질성이 크다. 네 seed가 모두 양수이면서 +0.04 이상인 entity가 3개다(machine-3-8 +0.090, 1-1 +0.063, 2-3 +0.044). 반대로 네 seed가 모두 음수이면서 −0.04 이하인 entity가 4개다(3-10 −0.089, 3-1 −0.055, 3-9 −0.044, 2-4 −0.042).
4. **PERM2+CRS는 두 데이터셋 모두에서 validation 예측 MAE를 키운다(예측이 나빠진다).**
   - SMD28: PERM2에서 CRS 효과 +0.0329, CI [+0.0266, +0.0397], 28개 중 27개 entity에서 악화.
   - PSM: best val MAE가 0.209에서 0.438로 2.1배가 된다.
   - PSM에서 AUC-PR이 오른 현상은 예측 품질 향상이 아니라 **predictor가 크게 바뀐 것과 함께** 나타난다.
5. **무결성 점검을 448/448 run 모두 통과했다.** 코드 SHA, 설정 차이(조작한 두 줄뿐), 로그의 활성 항, checkpoint의 `cls_ref`, best_val 선택, split·표준화·PCMCI+ key, 데이터 해시, 중복·누락·비유한 값을 모두 확인했다(§3).
6. **ks 결과 4개 캠페인을 원격에 게시했다.**
   - 대상: `results/{cfval_abl_smdcrs, cfval_abl_smdcrs20, cfval_abl_noalign, sp2x2}/ks`. 커밋 SHA는 §5에 있다.
   - 일반 push만 했다(force 없음). checkpoint·scores·데이터·로그·개인 경로는 포함하지 않았다.
   - 누출 재스캔 결과는 0건이다.

---

## 1. 실행 상태 (읽기 전용 조회, 10-12 17:58 KST)

| 캠페인 | 상태 | queue 집계 | 비고 |
|---|---|---|---|
| `cfval_abl_swatcrs2` | **학습 중** | prior 4 성공 · train 4 실행 · train 4 대기 · eval 16 대기 · 실패 0 | SWaT51 seed0·1 × PERM{0,2} × CRS{off,on} |
| `cfval_abl_swatcrs` | 미실행(dry-run만) | — | 16-run 계획이다. swatcrs2(8-run 축소안)로 대체됐다 |
| `cfval_abl_smdcrs` | 완료 (`stopped=done`, 10-08 07:38) | prior 32 · train 128 · eval 256 모두 성공 | machine-1-1..1-8 × 4 seed × 4 조건 |
| `cfval_abl_smdcrs20` | 완료 (`stopped=done`, 10-11 15:44) | prior 80 · train 320 · eval 640 모두 성공 | machine-2-*, 3-*(js set 20개) |
| `cfval_abl_noalign` (ks) | 완료 (09-13 05:35) | prior 9 · train 36 · eval 72 모두 성공 | PSM 4 seed + SMD 1-* × 4 seed. `START_CLS_EPOCH=81`(MAX_EPOCH=80), `ENABLE_PRIOR_LOSS=False`, PERM0 |
| `sp2x2` (ks) | 완료 (10-06 23:16) | prior 8 · train 8 · eval 8 모두 성공 | 코드 `f50147d`. PSM seed0·SMD 1-1 seed0 × T0~T3. best_val만, CF off |

### SWaT 세부

- **실행 구조**
  - tmux `picaad_cfval_abl_swatcrs2_ks`에서 `run_ablation.sh swatcrs2 --execute --no-tmux`가 돈다.
  - `run_experiments.py`(PID 3648662)가 GPU lock 4개를 모두 잡고 있다.
  - GPU마다 학습 프로세스가 하나씩 돈다(PID 3648686/694/700/706, 각 약 1.2 GB).
- **진행도**
  - 시작은 15:45:47이다. epoch 1이 16:08에 끝났다.
  - 17:58 기준 seed1 crson은 6 epoch, 나머지 3개는 5 epoch다.
  - epoch 2 이후 속도는 21.3~22.9분/epoch이다(GPU 4개 동시 실행).
- **실행 직후 검증은 진행 중인 범위에서 통과다.**
  - crson 로그는 ep5부터 `use_cstruct=True`, crsoff는 `False`다.
  - 4개 job 모두 `perm=0`이다(현재 실행 중인 것은 전부 PERM0이다).
- **남은 순서(launcher manifest 순서)**
  - PERM0 학습 4개가 끝난다(약 10-13 20~22시).
  - PERM0 eval 8개(last·best_val, CF both)가 돈다. js 실측 SWaT eval은 1개당 약 1.5시간이다.
  - PERM2 학습 4개가 돈다. ks SMD 실측으로 PERM0의 2.1배, 약 62~65시간이다.
  - PERM2 eval 8개가 돈다.
  - **종료 추정: 10-16 오후~밤.** 실측이 아니라 추정이다.
- **실제로 남은 작업**
  1. 완료를 확인한다(SUCCESS.json 24개 = train 8 + eval 16, 실패·재시도 여부).
  2. 핸드오프 브리프의 4개 검증을 마저 한다(설정 diff, `use_cstruct` 76/0회, perm 0/≠0, checkpoint `cls_ref` 편차).
  3. 2×2를 분해한다. seed가 2개뿐이므로 효과 크기와 부호 일관성을 위주로 본다.
  4. §K.2-5의 사전 예측을 판정한다(SWaT 개입 불가 행 47.8% → 상호작용이 작을 것).
  5. 결과 export·게시를 한다(별도 승인 필요, §6).
  - seed 2·3 추가 실행은 계획에 없다. 2-seed 결과를 본 뒤 결정한다.

---

## 2. SMD 28 entity CRS×PERM 통합 분석

### 2.1 입력과 정의

- **입력**
  - 두 캠페인 run별 원본 파일만 읽었다. 목록: queue.json, train SUCCESS/config.yaml/val_metrics.csv/로그/best_val checkpoint, eval SUCCESS/provenance/metrics.csv.
  - 기존 집계 CSV는 **읽지 않았다**. `eval_summary_*.csv`, `smdcrs*_best_val_metrics.csv`, `report_numbers.json`이 여기에 해당한다.
  - 수집 스크립트는 `scripts/collect_smd28.py`, 분석 스크립트는 `scripts/analyze_smd28.py`다.
- **조건 코드**
  - a00 = PERM0·CRS off, a01 = PERM0·CRS on, a10 = PERM2·CRS off, a11 = PERM2·CRS on.
  - 실제 arm은 resolved config와 로그로 확인했다(§3).
- **효과(entity·seed마다 계산). 핸드오프 브리프의 식 그대로다.**
  - `CRS@PERM0 = a01−a00`, `CRS@PERM2 = a11−a10`
  - `상호작용 = (a11−a10)−(a01−a00)`
  - `CRS 주효과 = 평균(CRS@PERM0, CRS@PERM2)`
  - `PERM 주효과 = ((a10−a00)+(a11−a01))/2`
- **주 지표:** best_val checkpoint의 `P_raw` AUC-PR이다. 나머지는 보조 지표이고 기술적으로만 본다.
- **불확실성**
  - 112개 (entity, seed) 쌍을 독립 표본으로 **취급하지 않는다**.
  - entity를 cluster로 두고 paired cluster bootstrap을 한다. 뽑힌 entity는 4 seed × 4 조건을 함께 가져온다.
  - B=10000, `numpy.random.default_rng(20261012)`다. 한 scope 안에서는 같은 추출 행렬을 모든 지표에 쓴다. percentile 95% CI다.
  - 보조로 entity 평균에 대한 one-sample t(df=27)를 냈다.
  - 참고로 seed macro 4개에 대한 t(df=3)도 냈다. 이 검정은 entity 집합을 고정된 것으로 보고 하는 추론이다.
- **부분집합과 PSM**
  - 8개(ks) / 20개(js set) 부분집합과 PSM은 참고용으로 따로 표시한다.
  - 28개 추정치는 raw row에서 entity마다 같은 가중치로 계산했다. 부분집합 평균을 50:50으로 섞지 않았다.

### 2.2 주 결과 — `P_raw` AUC-PR, best_val

| 범위 | a00 | a01 | a10 | a11 | CRS@PERM0 | CRS@PERM2 | **상호작용** | CRS 주효과 | PERM 주효과 |
|---|---|---|---|---|---|---|---|---|---|
| **SMD28 (주 결과)** | 0.4343 | 0.4353 | 0.4411 | 0.4405 | +0.0010 [−0.0014, +0.0041] | −0.0006 [−0.0126, +0.0117] | **−0.0016 [−0.0136, +0.0106]** | +0.0002 [−0.0061, +0.0067] | +0.0060 [−0.0031, +0.0167] |
| ㄴ entity +/− | | | | | 14 / 14 | 15 / 13 | 14 / 14 | 15 / 13 | 18 / 10 |
| ㄴ entity-t p (df=27) | | | | | 0.51 | 0.93 | 0.81 | 0.95 | 0.25 |
| *참고* SMD8 (ks, 1-*) | 0.4138 | 0.4182 | 0.4236 | 0.4329 | +0.0044 [−0.0005, +0.0130] | +0.0093 [−0.0044, +0.0271] | +0.0048 [−0.0071, +0.0228] | +0.0068 [−0.0019, +0.0172] | +0.0122 [−0.0020, +0.0300] |
| *참고* SMD20 (js set) | 0.4425 | 0.4421 | 0.4481 | 0.4436 | −0.0004 [−0.0025, +0.0019] | −0.0045 [−0.0197, +0.0109] | −0.0041 [−0.0195, +0.0113] | −0.0025 [−0.0102, +0.0054] | +0.0036 [−0.0071, +0.0168] |
| *참고* PSM (js, 1 entity × 4 seed) | 0.4461 | 0.4430 | 0.4460 | 0.5583 | −0.0031 (sd 0.0207, p=0.79) | **+0.1123** (sd 0.0110, 4/4, p=0.0003) | **+0.1153** (sd 0.0303, 4/4, p=0.0047) | +0.0546 (p=0.0005) | +0.0576 (p=0.0010) |

- SMD의 각 칸은 추정치와 entity cluster bootstrap 95% CI다.
- PSM은 seed 평균, seed 간 sd(ddof=1), seed 기준 paired t(df=3)다. PSM은 entity가 하나라 entity bootstrap을 할 수 없다.
- 부분집합 수치는 ks 중간 보고의 값과 소수 넷째 자리까지 같다(예: SMD8 상호작용 +0.0048, SMD20 −0.0041). 다른 것은 불확실성 계산 방식뿐이다(§2.7).

### 2.3 Seed별 28-entity macro (4 seed, ddof=1)

| 효과 | seed0 | seed1 | seed2 | seed3 | 평균 ± sd | seed-t p (df=3) |
|---|---|---|---|---|---|---|
| CRS@PERM0 | +0.0001 | −0.0006 | +0.0022 | +0.0022 | +0.0010 ± 0.0014 | 0.27 |
| CRS@PERM2 | +0.0044 | −0.0010 | −0.0015 | −0.0042 | −0.0006 ± 0.0036 | 0.77 |
| **상호작용** | +0.0042 | −0.0004 | −0.0038 | −0.0064 | **−0.0016 ± 0.0046** | 0.54 |
| CRS 주효과 | +0.0022 | −0.0008 | +0.0003 | −0.0010 | +0.0002 ± 0.0015 | 0.81 |
| PERM 주효과 | +0.0066 | +0.0054 | +0.0065 | +0.0057 | +0.0060 ± 0.0006 | 0.0003 |

- 조건별 macro 평균 ± sd: a00 0.4343 ± 0.0020, a01 0.4353 ± 0.0013, a10 0.4411 ± 0.0010, a11 0.4405 ± 0.0034.
- **PERM 주효과 해석에 주의한다.** seed 간으로는 매우 일관된다(+0.0060 ± 0.0006). 즉 "이 28개 entity에서는" 재현된다. 그러나 entity 간 이질성 때문에 entity 모집단으로 일반화하면 CI가 0을 포함한다(18/10, entity-t p=0.25). 두 추론은 질문이 다르다. 일반화 주장의 근거로는 entity cluster CI를 쓴다.

### 2.4 Entity 간 효과 분포 (`P_raw` AUC-PR, entity별 4-seed 평균)

| 효과 | 최소 | Q1 | 중앙값 | Q3 | 최대 | entity sd |
|---|---|---|---|---|---|---|
| CRS@PERM0 | −0.0108 | −0.0016 | +0.0001 | +0.0012 | +0.0334 | 0.0077 |
| CRS@PERM2 | −0.0747 | −0.0092 | +0.0008 | +0.0085 | +0.0863 | 0.0335 |
| 상호작용 | −0.0888 | −0.0085 | −0.0000 | +0.0065 | +0.0895 | 0.0333 |
| PERM 주효과 | −0.0366 | −0.0026 | +0.0014 | +0.0071 | +0.0956 | 0.0272 |

- **상호작용의 seed 일관성:** 네 seed 모두 양수인 entity 9개, 모두 음수 6개, 혼재 13개다. (entity, seed) 쌍 기준으로는 양수가 61/112다.
- **크기가 큰 entity**(entity 평균 |상호작용| ≥ 0.04, 모두 네 seed 부호 일치)
  - 양수: machine-3-8 +0.0895, 1-1 +0.0626, 2-3 +0.0439
  - 음수: machine-3-10 −0.0888, 3-1 −0.0547, 3-9 −0.0442, 2-4 −0.0422
- 따라서 SMD 평균이 0에 가까운 것은 "모든 entity에서 작다"는 뜻이 아니다. **크게 양수인 entity와 크게 음수인 entity가 상쇄된 결과다.**
- 어떤 entity 특성이 부호를 가르는지는 분석하지 않았다. 사후 탐색이 되기 때문이다(§6).
- entity별 4-seed 평균·sd(ddof=1)와 seed 부호 개수는 `smd28_entity_effects.csv`에 있다.

### 2.5 보조 지표 (SMD28, `P_raw`, 추정치 [95% CI])

| 지표 | CRS@PERM2 | 상호작용 | PERM 주효과 |
|---|---|---|---|
| AUC-ROC | +0.0011 [−0.0060, +0.0087] | +0.0015 [−0.0060, +0.0095] | +0.0041 [−0.0018, +0.0100] |
| VUS-PR | −0.0069 [−0.0220, +0.0075] | −0.0075 [−0.0221, +0.0065] | +0.0029 [−0.0081, +0.0148] |
| VUS-ROC | +0.0001 [−0.0064, +0.0067] | +0.0004 [−0.0065, +0.0074] | +0.0031 [−0.0019, +0.0083] |
| Standard-F1 | −0.0008 [−0.0102, +0.0090] | −0.0030 [−0.0139, +0.0076] | +0.0056 [−0.0021, +0.0145] |
| Affiliation-F | −0.0012 [−0.0046, +0.0024] | −0.0014 [−0.0060, +0.0038] | −0.0005 [−0.0023, +0.0012] |

- 주 보조 지표 5개 모두 상호작용과 CRS@PERM2의 CI가 0을 포함한다. 주 지표 결론과 같다.
- 나머지 보조 지표(CSV에 전부 있음) 중 CI가 0을 벗어난 것은 다음과 같다. Event-based-F1의 CRS 효과는 음수다(CRS@PERM0 −0.0036 [−0.0072, −0.0007], CRS@PERM2 −0.0140 [−0.0342, −0.0009]). R-based-F1의 PERM 주효과는 양수다(+0.0066 [+0.0010, +0.0138]). PA-F1의 CRS 효과는 음수다.
- 이들은 임계값을 label로 탐색하는 F1 계열이고, 45개 구간(9 지표 × 5 효과) 중 일부다. 근거로 쓰지 않는다. PA-F1은 point-adjust라 원래 주 지표가 아니다.
- VUS는 entity마다 window가 다르다(median window). 데이터셋 간 비교에는 AUC-PR/ROC가 안전하다.

### 2.6 예측 품질 — best_val checkpoint의 validation 예측 MAE (낮을수록 좋음)

| 범위 | a00 | a01 | a10 | a11 | CRS@PERM2 | 상호작용 | PERM 주효과 |
|---|---|---|---|---|---|---|---|
| SMD28 | 0.1998 | 0.2012 | 0.2229 | 0.2558 | **+0.0329** [+0.0266, +0.0397], 악화 27/28 | +0.0314 [+0.0253, +0.0378] | +0.0388 [+0.0312, +0.0472], 악화 28/28 |
| PSM (js) | 0.2142 | 0.2119 | 0.2088 | **0.4377** (seed sd 0.099) | **+0.2289**, 4/4, p=0.021 | +0.2311, p=0.019 | +0.1102 |

- PERM2와 CRS를 함께 켜면 두 데이터셋 모두 예측이 나빠진다. PSM에서는 MAE가 2배가 된다.
- PSM에서는 같은 조합에서 AUC-PR이 +0.11 오른다. SMD에서는 AUC-PR 평균 변화가 없다.
- `P_raw`는 예측 오차이므로, PSM의 AUC-PR 향상은 "평균 오차는 커졌지만 이상 구간에서 더 커지는" 방향의 변화다. **"더 좋은 predictor"로 해석하면 안 된다.**
- best epoch 평균도 다르다. PERM0 arm은 75.4 / 74.9이고, PERM2 arm은 70.7 / 70.4(최소 14 / 7)다. PERM2는 validation MAE 최저점이 더 이르다.
- 이 표는 기존 run 산출물(checkpoint의 `val_mae`)을 그대로 읽은 것이다. 새 지표나 점수를 만들지 않았다.

### 2.7 이전 부분집합 p값과의 관계

- ks 중간 보고의 p값(8개: 상호작용 p=0.3219, 20개: 0.3948)은 (entity, seed) 쌍 32/80개를 독립 표본으로 보고 계산한 것이다.
- 이 보고의 entity cluster 방식(SMD8 CI [−0.0071, +0.0228], SMD20 [−0.0195, +0.0113])으로 **대체한다**.
- 추정치 자체는 같다. 결론도 바뀌지 않는다(두 부분집합 모두 0과 구별되지 않음).

---

## 3. 결과 무결성 점검

448개 run 전부에서 확인했다. 실패 항목은 0개다. 자세한 내용은 `coverage_and_provenance.json`에 있다.

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| 학습 코드 SHA | queue `code`, train/eval SUCCESS identity, checkpoint `code_fingerprint`(dirty=False), eval `code_fingerprint`(modified_tracked=[]) | 전부 `49f630a`, 추적 diff 없음 |
| 조건 설정 | config 파일 sha256이 실행 시점과 같은지 확인. 448개 resolved config를 평탄화해 비교(run 식별 키 RESULT_DIR·SEEDS·ENTITIES·CKPT_DIR 제외) | 값이 다른 키는 `PERM_PAIRS_PER_BATCH`와 `START_CLS_EPOCH` **두 개뿐**이다. arm 이름 = resolved 값(PERM 0/2, START 5/99999) |
| CRS 활성 | 로그의 epoch별 `use_cstruct` | CRS on: ep5~80에서 76회 True. CRS off: 0회 |
| PERM 활성 | 로그의 epoch별 `perm=` | PERM2: 80/80 epoch 0이 아님. PERM0: 80/80 epoch 0 |
| `cls_ref` 갱신 | checkpoint의 `max|cls_ref − normalize(te_prior_weight)|` | PERM0: 6.0e-08~2.4e-07(prior로 퇴화). PERM2: 0.49~0.9997 |
| split | val_frac 0.2, `boundary = round(0.8·T_train)`(`datasets/split.py`와 같은 식), train_sub+val = train, `fit_protocol=train_sub_val(_v2)` | 전부 일치 |
| 표준화·PCMCI+ | checkpoint의 mu/sd를 eval 때 다시 계산한 train_sub 통계와 비교. prior cache key에 split id와 `_pcmci_` 포함 여부 | 최대 차이 0.0. key 전부 `…_pcmci_val0.2_b<boundary>_…` |
| best_val 선택 | checkpoint epoch = val 예측 MAE argmin(첫 최소) = 최종 `best_epoch_so_far`. checkpoint `val_mae` = 그 최솟값 | 전부 일치. 형식 `val`, 프로토콜 `val_pred_mae_v2` |
| checkpoint 파일 | 디스크 sha256 = provenance sha256. strict load, state 불변, 로드 후 `set_te_prior` 미호출 | 전부 일치 |
| 데이터 | NPZ sha256 비교 대상: `results/data-identity`(123a4e8)의 기준값, train identity, checkpoint, eval provenance | 28/28 일치 |
| entity/seed/tag/evaluator | metrics.csv의 entity·seed·epoch, `best_val` tag, 6 variant. evaluator(`USE_MEDIAN_VUS_WINDOW`, `VUS_VERSION=opt`, `VUS_THRE=250`, `start_idx=9`), 점수 설정(`CALIBRATE=False`, γ=1, `P_AGG=mean`, `C_AGG=fro`, CF top-k 15) | 전부 일치. VUS window는 entity 안에서 일정 |
| 누락·중복·실패·비유한 | 28×4×4 논리 키, 논리 job당 attempt 수, queue에 없는 결과 디렉토리, 비유한 metric | 누락 0, 중복 0, 고아 디렉토리 0, 실패 0, 비유한 값 0 |
| 게시본과의 일치 | 게시한 smdcrs/smdcrs20 metrics.csv의 best_val 행과 분석 입력 비교 | 24,192개 값 + epoch·sha256, 불일치 0 |

### 해석상의 한계 (반드시 함께 읽을 것)

1. **PERM=2는 두 가지를 동시에 켠다.**
   - (a) 개입 정렬 손실 `0.1·perm`이 켜진다. `group_robust`, `trainer.py:176-186`·`:201`.
   - (b) 개입 효과로 `cls_ref`가 갱신된다. `_update_epoch_refs`, `:283-307`. PERM0에서는 `cls_cnt=0`이라 prior로 퇴화한다.
   - 따라서 이번 2×2의 "PERM" 요인은 (a)+(b)의 묶음이다. **CRS×PERM 상호작용이 기준 갱신 때문인지 개입 손실 때문인지는 이 설계로 식별할 수 없다.**
2. **source-lag 개입 구간이 서로 겹친다.**
   - `L=10`, `LAG_WIN=5`, `τ=1..5`이므로 lag τ의 입력 구간은 `[L−τ−5, L−τ)`다. 인접 lag와 4 step이 겹친다.
   - `intervene_local_window`(`intervention.py:8-28`)는 (τ, src) 개입 때 그 구간의 src 값을 batch 안에서 섞는다. 그러면 같은 src의 다른 lag encoder 입력도 함께 바뀐다.
   - 측정된 `cls_ref[τ, src, :]`는 lag별 효과가 아니다.
3. **개입 샘플링은 PCMCI+ 행 out-degree에 비례한다**(`intervention.py:31-59`). out-degree가 0인 (τ, src) 행은 개입되지 않는다. 그 행의 `cls_ref`는 측정값을 받지 못한다.
4. PERM2 arm은 best epoch가 더 이르고 validation MAE가 더 높다(§2.6). 같은 선택 규칙을 써도 서로 다른 학습 단계의 predictor를 비교하게 된다.
5. SMD 결과는 SMD 28 entity에 대한 것이다. SWaT은 아직 없다. PSM은 단일 entity라 seed 수준 불확실성만 있다.

---

## 4. 기존 PSM 결과와의 차이

| | PSM (js, 4 seed) | SMD28 (ks, 28 entity × 4 seed) |
|---|---|---|
| CRS@PERM0 | −0.0031 (0과 구별 안 됨) | +0.0010 [−0.0014, +0.0041] |
| CRS@PERM2 | **+0.1123**, 4/4 seed | −0.0006 [−0.0126, +0.0117] |
| 상호작용 | **+0.1153**, 4/4 seed, p=0.0047 | −0.0016 [−0.0136, +0.0106] |
| 주효과(CRS / PERM) | +0.0546 / +0.0576 | +0.0002 / +0.0060 |
| a11의 val MAE / a10 | 2.10배 | 1.15배 |

- **"CRS 손실은 개입이 켜져 있을 때만 작동한다"는 PSM 관찰은 SMD 평균으로는 재현되지 않는다.** PSM 효과 크기는 SMD28 CI 상한의 10배가 넘는다.
- SMD에서 PSM 크기에 가까운 양의 상호작용은 3개 entity에서만 나타난다. 비슷한 크기의 음의 상호작용이 4개 entity에서 나타난다.
- 권장 서술은 v3 P0-5와 같다. "PSM에서는 크다. SMD에서는 평균 효과가 없고 entity마다 부호가 갈린다."
- 이 결과만으로 PSM 효과를 "특이 현상"이라고 단정하지 않는다. 판정은 SWaT(2 seed)이 나온 뒤에 한다(v3 P1 해석 분기).
- §K.2-5의 가설(개입 불가 행 비율이 낮을수록 상호작용이 크다)은 PSM 하나, SMD 하나에서 나온 상관이다. 사전 예측은 SWaT으로 판정한다. SMD entity 내부에서 이 상관을 확인하는 것은 이번 P0 정의에 없는 사후 분석이라 하지 않았다.

---

## 5. 결과 게시 (원격 branch, 전체 commit SHA)

| 캠페인 | branch | commit | package (`content_sha256` 앞 12자리) | 학습 코드 | 내용 |
|---|---|---|---|---|---|
| cfval_abl_smdcrs | `results/cfval_abl_smdcrs/ks` | `94050082bc990b9ba8b7310da8bb646f5623ed97` | `cfval_abl_smdcrs_ks` (f9e8fb605983) | 49f630a | job 416, complete |
| cfval_abl_smdcrs20 | `results/cfval_abl_smdcrs20/ks` | `8b15ea7e7830e0b601ad9e3b24b2e452d5e605bd` | `cfval_abl_smdcrs20_ks` (fbeb984cfea6) | 49f630a | job 1040, complete |
| cfval_abl_noalign (ks) | `results/cfval_abl_noalign/ks` | `04e66ebfd60b85227a871839043e026f5ca2631b` | `cfval_abl_noalign_ks` (e6a483e8d18a) | 49f630a | job 117, complete |
| sp2x2 (ks) | `results/sp2x2/ks` | `097ad24cfc341b6de2a4f500afb07ff43b75f30e` | `soft_prior_2x2_ks` (8ecea3618e55) | **f50147d** | job 24, complete |

- **브랜치 구조**
  - 네 커밋 모두 부모가 `49f630a`다.
  - 각 커밋은 `reports/experiments/<campaign>/ks/<run_id>/` 아래 파일 6개만 추가한다. 파일은 metrics.csv, run_manifest.json, config_resolved.yaml, provenance_summary.json, artifacts.json, summary.md다.
  - 게시 커밋은 학습 커밋과 다르다. 기준은 `run_manifest.json`의 `training_code_sha`다.
- **절차** (`<BOOTSTRAP>/ks/publish_redacted_ks.sh`, js `publish_redacted.sh`의 ks판)
  1. 실행 checkout(49f630a, clean)의 `export_results.py export`를 지원되는 옵션만으로 실행한다.
  2. 별도 publishing worktree에 export한다.
  3. 경로를 placeholder로 바꾸는 후처리를 한다. 대상은 `export_results.py:226`이 놓치는 metrics.csv의 `config` 열과, config_resolved.yaml의 경로 키다. 사용자명은 `<USER>`로 바꾼다.
  4. 누출 재스캔을 한다(절대경로, 사용자명, key/token 패턴, 파일 형식·크기). 0건일 때만 커밋했다.
  5. 그 package 경로만 stage했다.
  6. push 직전에 원격 ancestry를 다시 확인하고 일반 push를 했다.
- **확인한 것**
  - 실행 checkout의 HEAD·index는 변하지 않았다.
  - `publish_results.sh`(49f630a)는 `--server`를 server4/server8로 제한한다. 그래서 js와 같이 wrapper 방식을 썼다. 서버명 `ks`는 기존 `results/cfval/ks` 관례를 따랐다.
  - `sp2x2`는 기존 exporter 형식으로 그대로 export됐다. 그래서 별도 manifest는 만들지 않았다. CF off라 variant는 P/C/G/A_off 4개다.
- **받는 법:** `git fetch origin 'refs/heads/results/*:refs/remotes/origin/results/*'`
- 이 보고서 묶음(보고서·CSV·coverage·P3 설계·스크립트)은 별도 branch로 게시했다. branch와 SHA는 종료 보고에 적는다.

---

## 6. 미확인 항목과 다음에 필요한 승인

### 미확인 / 하지 않은 것

- **SWaT CRS×PERM:** 결과가 없다. 완료 후 §1의 남은 작업 1~4를 한다. 이것은 이미 승인된 P1의 일부다.
- **SMD entity 이질성의 원인:** 개입 불가 행 비율, 기준 성능 수준 등과의 관계를 분석하지 않았다. 사후 분석이다. 하려면 가설과 분석 정의를 먼저 고정한다.
- C/G/CF 채널과 fusion(A_off/A_on)의 CRS×PERM 효과는 분석하지 않았다. 주 비교가 `P_raw`이기 때문이다. 값은 `supporting/smd28_runs.csv`에 있다.
- PERM 요인 분해(개입 손실 vs `cls_ref` 갱신)는 하지 않았다. 별도 설계가 필요하다. 예: 개입 손실은 0으로 두고 기준만 갱신하는 arm. 코드 변경이 필요하다.
- js 쪽 noalign(`manifest_noalign_server8`)은 핸드오프 시점(10-07) 기준 미실행이었다. 그 뒤 상태는 확인하지 않았다. ks noalign은 SMD 1-*와 PSM만 덮는다.

### 다음에 필요한 승인

1. **SWaT 결과 게시:** 완료·검증 후 `results/cfval_abl_swatcrs2/ks`로 push할지. 이번 승인은 4개 캠페인과 이 보고 묶음에만 해당한다.
2. **SWaT seed 2·3 추가:** 2-seed 결과를 보고 결정한다.
3. **P2 calibrated rescoring(학습 없음):** 실행 승인이 필요하다. 그 전에 `robust_zscore` 0 클리핑 유지 여부를 고정해야 한다(v3 §K #11).
4. **P3 구조 대조:** 두 단계로 승인한다. (a) 별도 branch에서 no-prior / random-prior 구현과 단위 테스트(학습 없음). (b) 학습 실행. 1단계 PSM + SMD28 × 4 arm은 ks 4 GPU로 약 179 GPU-시간, 벽시계 약 45시간이다. SWaT이 끝난 뒤 시작한다. 설계는 `P3_STRUCTURAL_ABLATION_PLAN.md`에 있다.
5. 원하면 ks 중간 보고(`docs/ks_p1_crs_interaction_interim_report.md`)에 "이 보고로 대체됨" 표시를 하고 v3 §K.2-7의 두 오류를 고친다(문서 수정만).
