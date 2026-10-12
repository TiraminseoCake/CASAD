# P3 구조 대조 실험 프로토콜 — PCMCI+ prior / no-prior / 구조 맞춘 random prior / δ 제거

- **branch:** `exp/p3-structural-ablation` (base `49f630ac8d324ba01390c1a1dcaa4386cd94ae84`, trainer B). 실행 branch에는 병합하지 않는다.
- **커밋 이력**
  - `0271a149c0b9080486723f1b553c4fd1b02fbc21`: 최초 구현
  - `398187e618cd8a45eb5704c44ad886ad5a7e657a`: D 통제 수정, random prior 보존 보고, A-기존 run 비교 도구
  - 이 문서가 들어간 커밋: 검토 결과 기록. 코드 변경 없음
- **상태(2026-10-12):** 구현, 합성·단위 테스트, manifest·resolved config 검증을 마쳤다. **실데이터 학습은 아직 하지 않았다.** 다음 두 가지가 끝난 뒤 최종 승인을 받아 PSM → SMD 순서로 실행한다.
  - 기존 SWaT queue 완료
  - js 코드 검수
- 이 문서는 실데이터 결과를 보기 전에 고정했다. 결과를 본 뒤 정의를 바꾸지 않는다. 줄 번호는 이 branch 기준이다.

## 0. 질문

| 질문 | 대비 |
|---|---|
| Q1. PCMCI+ prior가 predictor(P score)에 도움이 되는가 (**1차 결론**) | A − N |
| Q2. 도움이 된다면 그 구조 자체 덕분인가, 희소도·lag 분포라는 형식 덕분인가 | A − R, R − N |
| Q3. dynamic correction δ가 도움이 되는가 | A − D |

1단계는 prediction-only 목적함수와 `P_raw`만 쓴다. CF·CRS·개입은 2단계에서 다룬다(별도 설계·승인).

## 1. 모든 arm에 공통으로 고정하는 것

| 항목 | 값 |
|---|---|
| 목적함수 | `ENABLE_PRIOR_LOSS=False`, `START_CLS_EPOCH=99999`, `PERM_PAIRS_PER_BATCH=0`, graphreg·inv 항 False. 결과적으로 `loss = 1.0 × L1 예측 손실` |
| 데이터·split | 기존 NPZ(sha256 = `results/data-identity` 기준값). val 0.2 시간순, train_sub만으로 표준화. test는 학습·선택에 쓰지 않는다 |
| 최적화 | 데이터셋 기본 LR(PSM 5e-5, SMD 5e-4, SWaT 5e-4; `utils/parser.py`), AdamW wd 0.01, batch(PSM·SMD 512, SWaT 128), 80 epoch, grad clip 1.0 |
| checkpoint | best_val = validation 예측 MAE 최소(`MIN_DELTA=0`, 첫 최솟값). last는 저장만 한다 |
| 평가 | `scripts/eval_ckpt.py --ckpt_tag best_val --cf off --calibrate off`. CF forward 0회. 주 지표는 `P_raw`, 보조로 C/G/A_off(이미 계산되는 값) |
| seed·대상 | PSM 0–3, SMD 28 entity × 0–3, (2단계) SWaT 0–1 |
| 계산 | ks GPU 4장, GPU당 job 1개, thread 4, launcher `scripts/run_experiments.py`(변경 없음), out_root는 checkout 밖 |

## 2. Arm과 구현

| arm | 설정 (`scripts/configs/p3_structural/<ds>_p3_<arm>.yaml`) | 의미 |
|---|---|---|
| **A** | `PRIOR.TYPE=pcmci`, `RANDOMIZE=none`, `USE_DYNAMIC_DELTA=True` | 기존 경로 그대로. 49f630a와 비트 동일(§3) |
| **N** | `PRIOR.TYPE=none` | prior를 계산·로드·적용하지 않는다. `set_te_prior`를 호출하지 않는다 |
| **R** | `PRIOR.TYPE=pcmci`, `RANDOMIZE=degree_preserving_v1` | A와 같은 cache prior를 seed마다 재배선한 뒤 A와 같은 `set_te_prior` 경로를 탄다 |
| **D** | `USE_DYNAMIC_DELTA=False` | A와 같은 모델·파라미터·초기화·batch 순서에서 δ만 더하지 않는다 |

- 모든 arm은 `DYNAMIC_GRAPH=True`다.
- 설정 12개는 `scripts/make_p3_configs.py`가 기존 `*_cf_val.yaml`에서 생성한다. 같은 데이터셋의 네 arm은 `PRIOR.TYPE`, `PRIOR.RANDOMIZE`, `USE_DYNAMIC_DELTA` 세 키만 다르다(테스트·plan 검증으로 확인).

**코드 변경** (기본값이면 49f630a와 동작 동일, §3 교차 커밋 테스트):

- `config.py:74-78`: `USE_DYNAMIC_DELTA`(기본 True). `config.py:119-127`: `PRIOR.TYPE`에 `none` 추가, `PRIOR.RANDOMIZE`(`none`|`degree_preserving_v1`), `RANDOMIZE_SALT`, `RANDOMIZE_SWAPS`(10).
  - 이 키들은 prior cache key에 들어가지 않는다. 그래서 R과 D는 A의 cache를 그대로 읽는다.
- `model/modeling_picaad.py:47,57,208`, `model/build.py:48`: `use_dynamic_delta=False`이면 `dynamic_q/k`는 A와 똑같이 만들되 `_compute_dynamic_delta`가 None을 반환한다.
- `model/build.py:90-91`, `:163-166`: TYPE `none`이면 `(None, None)`을 반환한다. PCMCI+ 계산도, cache 읽기·쓰기도 없다. launcher prior warm-up job은 no-op이 된다.
- `model/build.py:95-101`: 배열이 None이면 `set_te_prior`를 부르지 않는다. TYPE이 `none`이 아닌데 배열이 None이면 오류를 낸다.
- `model/prior_randomize.py`(신규): `prepare_seed_prior`, `degree_preserving_rewire`, `rewire_checks`(불변식, 위반 시 학습 시작 전 오류), `rewire_report`(§4 보존·변화 통계를 `prior_info`에 기록).
- `main.py:63-77`: seed마다 `prepare_seed_prior` → `set_seed` → `build_model` → `apply_prior_to_model` 순서다. no-prior면 `prior_cache_key=None`이다(`:333-334`). `prior_info`가 provenance와 checkpoint(`trainer.py:543`)에 기록된다.
- `scripts/eval_ckpt.py:244-254`: 저장된 설정이 `PRIOR.TYPE=none`이고 te_prior 버퍼가 0일 때만 `has_te_prior=False`를 허용한다. `prior_info`를 provenance에 기록한다(`:430`).
- 검증 도구:
  - `scripts/verify_p3_plan.py`: plan, resolved config, 데이터, cache 검사
  - `scripts/p3_random_prior_report.py`: §4 보존 통계
  - `scripts/compare_p3_a_to_runs.py`: §5 A와 기존 run 비교

**N이 실제로 갖는 상태**

- `pred_logits`는 0이고, 모든 lag 대각에 `SELF_LOOP_BIAS`가 더해진다(A에도 같은 항).
- `edge_log_alpha`는 `logit(0.15)`로 균일하다. `causal_mask_logits`는 0이라 초기 MHSA mask는 상수다.
- routing은 `pred_logits + δ + log σ(edge_log_alpha)`이고, gate는 `σ(edge_log_alpha)`다.
- prior 손실은 0이다.
- `cls_ref`는 epoch 1 뒤 self-causal fallback이 된다(1단계에서는 쓰이지 않음).
- 개입 샘플링은 균등이다(1단계에서는 호출되지 않음).
- CF source는 학습된 gate만으로 고른다.

### 2.1 D 통제 (10-12 수정, `0271a14` → `398187e`)

- **원인:** 최초 구현은 D를 `DYNAMIC_GRAPH=False`로 만들었다. 이 경우 `modeling_picaad.py`가 `dynamic_q/k`(nn.Linear, kaiming 초기화)를 만들지 않는다. 그래서 두 가지가 달라졌다.
  - 그 초기화에 쓰이던 전역 CPU RNG가 소비되지 않는다. 바로 뒤에 생성되는 `edge_value_head`(weight·bias)의 초기값이 달라진다. 앞서 생성되는 encoder·MHSA·`pred_logits`·`edge_log_alpha`와 뒤의 0 초기화 파라미터는 같다.
  - 모델 생성 뒤 RNG 상태가 달라진다. DataLoader `RandomSampler`(generator 없음)가 epoch마다 전역 RNG에서 shuffle seed를 뽑으므로, minibatch 순서도 달라진다.
- **수정:** `USE_DYNAMIC_DELTA=False`이면 q/k를 A와 똑같이 만들고 δ만 더하지 않는다.
  - q/k는 gradient를 받지 않는다. 그래서 AdamW가 건너뛰고(weight decay도 없음), gradient clip 계산에서도 빠진다. q/k는 초기값 그대로 남는다.
  - 기본값 True는 기존 동작 그대로다.
- **확인**(§3, 모두 통과)
  - 같은 seed에서 D와 A의 초기 state_dict 전체와 생성 후 RNG 상태가 같다.
  - D의 forward는 "δ를 None으로 강제한 A"와 같다.
  - D 학습은 "δ를 None으로 강제한 A" 학습과 checkpoint state·val curve가 비트 단위로 같다.
  - 네 arm의 학습 batch 순서가 모두 같다.
  - 수정 전 방식(`DYNAMIC_GRAPH=False`)은 `edge_value_head`와 RNG 상태가 다르다는 것도 테스트로 고정했다.

## 3. 검증 결과 (합성 데이터, CPU, 실데이터 학습 없음)

`CUDA_VISIBLE_DEVICES= python -m unittest tests.test_p3_structural -v` (교차 커밋: `PICAAD_BASE_REPO=<49f630a checkout>`)

| ID | 검사 | 결과 |
|---|---|---|
| T1 | no-prior 모델의 te_prior 버퍼를 0 / 실제 / 난수로 바꿔도 다음 항목이 비트 동일하다: forward, Π, prior 손실(0), gradient, 개입 손실·`cls_sum`, effective gate, CF source. `_update_epoch_refs`도 prior로 fallback하지 않는다. cache에 PCMCI+ prior가 있어도 no-prior 학습은 그 파일을 열지 않고 결과도 같다. PERM2+CRS를 켠 no-prior 학습도 재현된다 | 통과 |
| T2 | 같은 seed에서 `set_te_prior`가 쓰지 않는 파라미터는 A·N·R·D 모두 같다. A = N + 경로 1~3 가산항이 비트 단위로 성립한다 | 통과 |
| T3 | no-prior routing·gate·MHSA mask 식이 직접 계산과 같다 | 통과 |
| T4 | 네 arm 모두 매 epoch `loss_total == group_task`이고, causal·graphreg·robust·cstruct·perm은 정확히 0이다 | 통과 |
| T5 | checkpoint `prior_info`가 맞다. N은 `prior_cache_key=None`, 버퍼 0이다. R의 버퍼는 기록된 sha256의 재배선 prior를 정규화한 것과 같고, 보존 보고의 exact 항목이 모두 True다. D의 q/k는 초기값 그대로다 | 통과 |
| T6 | `eval_ckpt.py --cf off`가 네 arm을 모두 복원한다. CF forward는 0회다. N에 `--cf both`를 주면 거부한다 | 통과 |
| T7 | 기본 경로가 49f630a와 학습 결과(state_dict hash, val curve, best epoch) 기준으로 비트 동일하다 | 통과 |
| T8 | 재배선 불변식(합성 12 + 저장 prior 6), 결정성, seed·entity별 차이, 전역 RNG 비간섭, 보존 보고(§4의 13개는 항상 True, 3개는 이동 시 False) | 통과 |
| T9 | 네 arm(A·N·R·D)의 학습 batch 순서가 같다 | 통과 |
| D | §2.1의 초기화·RNG 동일성, forward 동치, "δ를 끈 A"와 학습 동치, 수정 전 방식의 원인 고정 | 통과 |
| 설정 | 생성 파일 = 생성기 출력, arm 간 3개 키만 다름, 12개를 실제 로더로 해석해 prediction-only·LR·epoch·VAL 확인, manifest 3개 `Plan` 전개 확인 | 통과 |

**수정 전후 테스트**

- `0271a14`: 전체 테스트 모듈 84개 OK(교차 커밋 포함, 건너뜀 0).
- `398187e`: 88개 OK(건너뜀 0).
  - 기존 84개 가운데 P3 파일의 D 관련 5개를 새 정의에 맞게 고쳤다. `test_delta_removed_model`, T5, T9, 초기화 동일성, 설정 해석이다.
  - 나머지 79개는 그대로 통과했다.
  - D 동치 3개와 보존 보고 1개, 총 4개를 새로 추가했다.
- checkpoint 파일 바이트는 49f630a와 다르다. payload에 `prior_info`가 추가되기 때문이다. 학습 동작이 같다는 것은 T7로 확인한다.

## 4. Random prior가 보존하는 것 (실제 cache prior 30개 × 계획 seed = 118개, `398187e`)

PSM 1개 × seed 0–3, SMD 28개 × 0–3, SWaT 1개 × 0–1이다. `scripts/p3_random_prior_report.py`로 계산했다(학습 없음).

| 통계 | 정확히 보존 |
|---|---|
| lag별 source 연결 수(out-degree), 전체 lag 합 out-degree | 118/118 |
| lag별 target 연결 수(in-degree) | 118/118 |
| lag별 edge 수(lag별 sparsity), lag별 cross edge 수 | 118/118 |
| self edge(모든 lag, 값 포함; lag-1 self loop 포함) | 118/118 |
| prior strength 분포: (lag, target)별 weight·gate 다중집합, lag별 weight 다중집합, 전체 weight 분포 | 118/118 |
| (lag, target)별 in-strength(weight 합), target별 열 합(정규화) | 118/118 (차이 ≤ 1e-6) |
| gate 0.5(모호 edge) 개수 | 118/118 |
| **(lag, source)별 out-strength(weight 합)** | **0/118. 보존 안 됨** |
| **source별 weight 다중집합(lag별·전체)** | **0/118. 보존 안 됨** |

**보존되지 않는 통계**(min / 중앙값 / max)

- (lag, source) out-strength
  - 실제 대비 상관 0.81 / 0.91 / 0.99
  - 상대 L1 변화 0.06 / 0.19 / 0.32
- source별 전체 out-strength 상관: 0.48 / 0.72 / 0.93
  - 연결 수는 같다. 하지만 어떤 target slot의 weight를 받느냐에 따라 강도가 바뀐다.
- 같은 lag의 상호 연결(i→j와 j→i): 합계 576 → 159(중앙값 5 → 1).
- 같은 (source, target)이 2개 이상 lag에 연결: 합계 1202 → 505(중앙값 10 → 4).
  - 재배선을 lag마다 독립으로 하기 때문에 lag 간 일관된 쌍이 줄어든다.
- 대칭 모호 쌍(양방향 gate 0.5): 실제 prior에 0개라 해당 없음.
- 실제 cross edge와의 겹침
  - Jaccard 0.05 / 0.11 / 0.22
  - 실제 edge 유지 비율 0.10 / 0.20 / 0.35
- 재배선이 불가능한 lag는 그대로 남는다. cross edge가 1개뿐이거나, 모든 edge가 한 source 또는 한 target을 공유하는 lag다. 예: machine-1-1의 lag 4(1개)와 lag 5(4개, swap 0회). 이런 lag는 `prior_info.per_lag`에 swap 수와 Jaccard로 기록된다.
- 해석상 주의: R은 차수·강도 분포·lag 형식이 같은 무작위 구조다. source별 강도, 상호 연결, lag 간 일관성까지 맞춘 대조군은 아니다. A−R 차이를 "구조 정체성" 효과로만 해석하지 않는다. 위 세 통계의 차이도 함께 기여할 수 있다.

## 5. A가 기존 prediction-only(noalign) run과 같은 학습 프로토콜인가

비교 대상은 ks `cfval_abl_noalign`(49f630a; PSM 4 seed, SMD machine-1-1..1-8 × 4 seed, 총 36 run)이다. `scripts/compare_p3_a_to_runs.py`, `398187e` 기준이다.

| 차이 나는 키 | 분류 | 내용 |
|---|---|---|
| `START_CLS_EPOCH` 99999 vs 81 | equivalent | 둘 다 `MAX_EPOCH=80`보다 커서 CRS 손실은 한 번도 켜지지 않는다 |
| `SCORING.USE_COUNTERFACTUAL` False vs True, `SCORING.SCORE_GAMMA` 0 vs 1 | eval-only | `VAL.ENABLE=True`에서는 trainer가 점수를 계산하지 않는다(test epoch eval 경로는 오류). 학습에 영향 없음 |
| `PRIOR.RANDOMIZE*`, `USE_DYNAMIC_DELTA` | new-default | 이 branch에서 추가된 키이며 기본값이다 |
| `RESULT_DIR`, `TRAIN.CKPT_DIR` | run-identity | 출력 위치 |

- 그 밖의 resolved config 키는 36 run 모두 같다(OTHER 0).
- 데이터 sha256, split id, PCMCI+ prior cache key도 36/36 같다.
- 기준 noalign run이 실제로 prediction-only였는지도 확인했다. 80 epoch 내내 causal·graphreg·robust·cstruct·perm이 0이고 `loss_total == group_task`였다.
- 따라서 A의 실데이터 학습은 noalign과 같은 프로토콜이다. 기본 경로가 49f630a와 비트 동일하므로(T7), **같은 seed의 noalign 학습을 비트 단위로 재현할 것으로 예상한다.**
  - 선례: sp2x2 T0가 같은 GPU에서 noalign val MAE를 비트 단위로 재현했다.
  - 이것을 실행 시 수용 검사로 쓴다(§7).

## 6. 분석 계획 (사전 고정)

- **주 지표:** best_val `P_raw` AUC-PR.
- **보조 지표**
  - validation 예측 MAE
  - AUC-ROC, VUS-PR, VUS-ROC, Standard-F1, Affiliation-F
- **대비:** A−N(1차), A−R, R−N, A−D. 이 4개로 고정한다.
- **불확실성:** P0와 같다.
  - SMD는 entity cluster paired bootstrap(B=10000, seed 20261012), seed별 28-entity macro(4개, ddof=1), entity 부호 개수다.
  - PSM은 seed 4개의 평균·sd·paired t(df=3)와 부호 개수다.
  - (entity, seed) 쌍을 독립 표본으로 보지 않는다.
- **AUC-PR ±0.01**
  - **탐색적 실용 효과 크기 기준으로만** 쓴다. 추정치와 95% CI를 이 기준에 비추어 "실용적으로 작다/크다/판정 불가"라고 서술하는 데에만 쓴다.
  - **통계적 동등성의 증거로 쓰지 않는다.** 동등성 검정은 하지 않는다. "동등"이나 "차이 없음"이라고 쓰지 않는다.

| 관찰 | 서술 |
|---|---|
| A−N의 CI가 0을 포함하고 ±0.01 안에 있음 | predictor 수준에서 prior 효과가 이 설계로는 실용적으로 작다(동등성 주장 아님) |
| A>N이고 A>R, R≈N | PCMCI+ 구조(§4의 보존되지 않는 통계 포함)가 도움이 된다는 근거 |
| A≈R>N | 차수·강도 분포·lag 형식이 도움이 된다는 근거 |
| A<N | prior가 predictor를 제약한다는 근거 |
| 그 밖의 경우 | 판정 불가로 보고 |

## 7. 실행 준비와 절차 (최종 승인 후)

**순서:** ① PSM(4 seed × 4 arm) → ② SMD(28 entity × 4 seed × 4 arm) → (③ SWaT 2단계는 별도 승인)

1. 최종 승인된 커밋을 별도 실행 worktree(`exec/p3_<sha>`)로 checkout한다. dev worktree에서는 실행하지 않는다.
2. `run_experiments.py --dry-run`을 돌리고 세 가지를 검사한다.
   - `verify_p3_plan.py`: 실패 0
   - `compare_p3_a_to_runs.py`: OTHER 0, identity 일치
   - `p3_random_prior_report.py`: exact 13개 전부 True
3. 보고하고 승인을 받는다.
4. PSM manifest를 tmux에서 실행한다. 진행 중인 다른 실험은 선점하지 않는다.
5. **수용 검사(PSM):** A의 seed 0–3 val curve(80 epoch)와 best epoch·val MAE가 noalign PSM seed 0–3과 비트 단위로 같아야 한다.
   - 다르면 분석 전에 원인을 보고한다.
   - 결과(성능)를 보고 설정을 바꾸지는 않는다.
6. PSM 완료·검증 후 SMD manifest를 실행한다. SMD machine-1-* × seed 0–3의 A에도 같은 수용 검사를 한다.
7. 완료 후 무결성 점검(P0 항목 + `prior_info`)과 §6 분석을 한다. 게시는 별도 승인을 받는다.

## 8. 비용과 대상 (ks 실측 기반 추정, GPU 4장, GPU당 job 1개)

| 실험 | 대상 | 학습 run | 학습 시간/run (실측 근거) | 평가 (CF off) | GPU-시간 | 벽시계 |
|---|---|---|---|---|---|---|
| ① P3-PSM | PSM × seed 0–3 × 4 arm | 16 | 약 79분 (ks noalign PSM 78.5분, sp2x2 PSM 79~81분) | 약 2.4분 | 약 22 | 약 5.5시간 |
| ② P3-SMD | SMD 28 entity × seed 0–3 × 4 arm | 448 | 약 20~23분 (ks noalign SMD 1-* 19.8분, sp2x2 SMD 1-1 약 23분) | 약 1.0분 | 약 157~180 | 약 39~45시간 |
| ①+② | | 464 | | | **약 179~202** | **약 45~50시간** |
| ③ P3-SWaT (2단계, 선택) | SWaT51 × seed 0–1 × 4 arm | 8 | 약 29시간 (swatcrs2 PERM0 실측 epoch 속도) | P-only라 CF eval(약 1.5시간)보다 짧음(미실측) | 약 236 | 약 59시간 |

- D는 δ를 계산하지 않아 A보다 조금 가볍다(따로 실측하지 않음).
- 시작 가능 시점은 ks GPU 4장을 쓰는 SWaT CRS×PERM seed 0–3 queue 두 개가 끝난 뒤(추정 10-20 저녁~10-21)와 js 검수 뒤 가운데 늦은 쪽이다.

## 9. 위험과 한계

- N의 gate 초기값(0.15 균일)은 A(prior 안 약 0.36, 밖 약 0.053)와 다르다. 이것은 prior 효과의 정의에 포함된다(경로 2).
- `SELF_LOOP_BIAS`와 lag-1 self loop는 모든 arm에 남는다. 모델 기본값이지 PCMCI+ 정보가 아니다.
- R은 §4대로 source별 강도, 상호 연결, lag 간 일관성을 보존하지 않는다. degree 수열은 실제 PCMCI+ 결과에서 왔다.
- D는 학습되지 않는 q/k를 가진다. 파라미터 수는 A와 같다. 파라미터 수를 비교할 때 이 점을 밝힌다.
- 데이터셋마다 AdamW decay 누적곱이 다르다(SWaT 0.29, PSM 0.992, SMD 0.982). 그래서 초기화로 들어간 prior(경로 1~3)의 잔존량이 데이터셋마다 다르다.
- 1단계는 CRS·개입·CF와 prior의 상호작용을 다루지 않는다.
