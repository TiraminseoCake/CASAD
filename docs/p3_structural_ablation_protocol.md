# P3 구조 대조 실험 프로토콜 — PCMCI+ prior / no-prior / 구조 맞춘 random prior / δ 제거

- branch: `exp/p3-structural-ablation` (base `49f630ac8d324ba01390c1a1dcaa4386cd94ae84`, trainer B). 실행 branch에는 병합하지 않는다.
- 상태(2026-10-12): 구현, 합성 데이터 테스트, manifest·resolved config 검증까지 승인되어 완료했다. **실데이터 학습은 별도 승인 후에만 시작한다.**
- 이 문서는 실데이터 결과를 보기 전에 고정했다. 결과를 본 뒤 정의를 바꾸지 않는다.
- 줄 번호: 이 branch 기준이다. 49f630a 기준 위치는 `KS_P0_FINAL_REPORT` 묶음의 `P3_STRUCTURAL_ABLATION_PLAN.md`에 있다.

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
| seed | PSM 0–3, SMD 28 entity × 0–3, (2단계) SWaT 0–1 |
| 계산 | ks GPU 4장, GPU당 job 1개, thread 4, launcher `scripts/run_experiments.py`(변경 없음), out_root는 checkout 밖 |

## 2. Arm과 구현

| arm | 설정 (`scripts/configs/p3_structural/<ds>_p3_<arm>.yaml`) | 의미 |
|---|---|---|
| **A** | `PRIOR.TYPE=pcmci`, `RANDOMIZE=none`, `DYNAMIC_GRAPH=True` | 기존 경로 그대로. 49f630a와 비트 동일(§3 T7) |
| **N** | `PRIOR.TYPE=none` | prior를 계산·로드·적용하지 않는다. `set_te_prior`를 호출하지 않는다 |
| **R** | `PRIOR.TYPE=pcmci`, `RANDOMIZE=degree_preserving_v1` | A와 같은 cache prior를 seed마다 재배선한 뒤 A와 같은 `set_te_prior` 경로를 탄다 |
| **D** | `DYNAMIC_GRAPH=False` | δ 없이 재학습한다(기존 config 키) |

- 설정 파일 12개는 `scripts/make_p3_configs.py`가 기존 `*_cf_val.yaml`에서 생성한다. 같은 데이터셋의 네 arm은 위 3개 키만 다르다(테스트로 확인).

**코드 변경** (기본값이면 동작 불변):

- `config.py:115-123`: `PRIOR.TYPE`에 `none`을 추가했다. `PRIOR.RANDOMIZE`(`none`|`degree_preserving_v1`), `RANDOMIZE_SALT`(`p3-random-v1`), `RANDOMIZE_SWAPS`(10)를 추가했다. 세 키 모두 prior cache key에 들어가지 않는다. 그래서 R은 A의 cache를 그대로 읽는다.
- `model/build.py:89-90`, `:162-165`: TYPE `none`이면 `build_causal_prior`(_cached)가 `(None, None)`을 반환한다. PCMCI+ 계산도, cache 읽기·쓰기도 없다. launcher의 prior warm-up job은 no-op이 된다.
- `model/build.py:94-100`: 배열이 None이면 `apply_prior_to_model`이 `set_te_prior`를 부르지 않는다. TYPE이 `none`이 아닌데 배열이 None이면 오류를 낸다.
- `model/prior_randomize.py`(신규): `prepare_seed_prior`, `degree_preserving_rewire`.
  - 처리 단위는 lag마다 cross edge(src≠tgt)다. target slot이 (weight, gate)를 가진 채로 source만 맞바꾸는 double-edge swap을 한다. self edge나 중복 edge가 생기면 기각한다. 시도 횟수는 edge 수의 10배다.
  - 보존: lag별 in-degree·out-degree, 모든 self edge(lag-1 self loop 포함), target별 (weight, gate) 다중집합(그래서 열 합도 같음), gate 0.5 개수.
  - RNG: 지역 `default_rng(sha256(salt|dataset|entity|seed))`. 전역 RNG를 쓰지 않는다.
- `main.py:63-77`: seed마다 `prepare_seed_prior` → `set_seed` → `build_model` → `apply_prior_to_model` 순서다. no-prior면 provenance에 `prior_cache_key=None`이 들어간다(`:333-334`). `prior_info`(type, randomize, 배열 sha256, 재배선 통계)가 provenance와 checkpoint(`trainer.py:543`)에 기록된다.
- `scripts/eval_ckpt.py:244-253`: 저장된 설정이 `PRIOR.TYPE=none`일 때만 `has_te_prior=False`를 허용한다. 이때 te_prior 버퍼가 0이 아니면 거부한다. 다른 checkpoint는 기존처럼 세 기준 플래그가 모두 있어야 한다. `prior_info`를 provenance에 기록한다(`:430`).

**N이 실제로 갖는 상태**

- `pred_logits`는 0이고, 모든 lag 대각에 `SELF_LOOP_BIAS`가 더해진다. A에도 같은 항이 있다.
- `edge_log_alpha`는 `logit(0.15)`로 균일하다. `causal_mask_logits`는 0이라 초기 MHSA mask는 상수다.
- routing은 `pred_logits + δ + log σ(edge_log_alpha)`이고, gate는 `σ(edge_log_alpha)`다.
- prior 손실은 0이다.
- `cls_ref`는 epoch 1 뒤 self-causal fallback이 된다. 1단계에서는 쓰이지 않는다.
- 개입 샘플링은 균등이다(1단계에서는 호출되지 않음).
- CF source는 학습된 gate만으로 고른다.

**D의 주의점:** `dynamic_q/k`가 생성되지 않는다. 그래서 같은 seed라도 이후 모듈 초기화와 batch 순서가 A와 다르다(테스트로 확인했다. A·N·R은 같다). 이 차이는 seed 변동에 포함된다.

## 3. 검증 결과 (합성 데이터, CPU, 실데이터 학습 없음)

`CUDA_VISIBLE_DEVICES= python -m unittest tests.test_p3_structural -v` (기준 비교: `PICAAD_BASE_REPO=<49f630a checkout>`)

| ID | 검사 | 결과 |
|---|---|---|
| T1 | no-prior 모델의 te_prior 버퍼를 0 / 실제 / 난수로 바꿔도 forward, Π, prior 손실(0), gradient, 개입 손실·`cls_sum`, effective gate, CF source가 비트 동일하다. `_update_epoch_refs`도 prior로 fallback하지 않는다. cache에 PCMCI+ prior가 있어도 no-prior 학습이 그 파일을 열지 않고 결과도 같다. PERM2+CRS를 켠 no-prior 학습도 재현된다 | 통과 |
| T2 | 같은 seed에서 `set_te_prior`가 쓰지 않는 파라미터는 A·N·R 모두 같다. A = N + 경로 1~3 가산항이 비트 단위로 성립한다 | 통과 |
| T3 | no-prior routing·gate·MHSA mask 식이 직접 계산과 같다 | 통과 |
| T4 | 네 arm 모두 매 epoch `loss_total == group_task`이고, causal·graphreg·robust·cstruct·perm은 정확히 0이다 | 통과 |
| T5 | checkpoint `prior_info`가 맞다. N은 `prior_cache_key=None`, 버퍼 0, `_has_te_prior=False`다. R의 버퍼는 기록된 sha256의 재배선 prior를 정규화한 것과 같다. D에는 `dynamic_q`가 없다 | 통과 |
| T6 | `eval_ckpt.py --cf off`가 네 arm을 모두 복원한다. CF forward는 0회다. N에 `--cf both`를 주면 거부한다 | 통과 |
| T7 | 기본 경로(A 설정 키)가 49f630a와 학습 결과(state_dict hash, val curve, best epoch) 기준으로 비트 동일하다 | 통과 |
| T8 | 재배선 불변식(합성 12개 + 저장된 prior 6개)이 성립한다. 결정적이다. seed와 entity에 따라 달라진다. 전역 RNG를 건드리지 않는다 | 통과 |
| T9 | A·N·R의 학습 batch 순서가 같다 | 통과 |
| 설정 | 생성 파일 = 생성기 출력이다. arm 간 차이는 3개 키뿐이다. 12개 파일을 실제 로더(`utils/parser.load_config`)로 해석했을 때 prediction-only 플래그, LR, epoch, VAL이 맞다. manifest 3개를 launcher `Plan`으로 전개한 결과(train/eval 개수, `--cf off`, `--calibrate off`)가 맞다 | 통과 |

- 기존 테스트 모듈 전체도 이 branch에서 다시 돌렸다. 결과는 커밋 메시지와 ks 보고에 적는다.
- checkpoint 파일 자체는 49f630a와 바이트가 다르다. payload에 `prior_info` 키가 추가되기 때문이다. 학습 동작이 같다는 것은 T7로 확인한다.

## 4. 실제 prior에서 R의 모양 (학습 없이 cache prior로 계산)

val0.2 split의 PCMCI+ cache prior 29개(PSM, SMD 28) × seed 0–3을 계산했다.

- 불변식은 모두 성립한다. 열 합 차이는 최대 1.8e-7이다.
- 새 source를 받은 cross edge 비율은 73~93%다(중앙값 88%).
- lag별 실제 지지집합과의 Jaccard는 중앙값 0.165, 최대 0.58이다.
  - machine-1-1이 0.53으로 높다. hub source가 강하면 degree를 보존하는 재배선 공간이 좁아지기 때문이다.
  - 따라서 R은 "실제 구조와 완전히 무관한 prior"가 아니라 "차수가 같은 무작위 구조"다. A−R 해석 때 entity별 Jaccard를 함께 본다.
- cross edge 수: PSM 37(N=25), SMD 47~152(N=38).

## 5. 분석 계획 (사전 고정)

- **주 지표:** best_val `P_raw` AUC-PR.
- **보조 지표**
  - validation 예측 MAE
  - AUC-ROC, VUS-PR, VUS-ROC, Standard-F1, Affiliation-F
- **대비:** A−N(1차), A−R, R−N, A−D. 이 4개로 고정한다.
- **불확실성:** P0와 같다(`KS_P0_FINAL_REPORT`의 `scripts/analyze_smd28.py` 정의).
  - SMD는 entity cluster paired bootstrap(B=10000, seed 20261012), seed별 28-entity macro(4개, ddof=1), entity 부호 개수다.
  - PSM은 seed 4개의 평균·sd·paired t(df=3)와 부호 개수다.
  - (entity, seed) 쌍을 독립 표본으로 보지 않는다.
- **AUC-PR ±0.01**
  - **탐색적 실용 효과 크기 기준으로만** 쓴다.
  - 차이의 추정치와 95% CI를 이 기준에 비추어 "실용적으로 작다/크다/판정 불가"라고 서술하는 데에만 쓴다.
  - **통계적 동등성의 증거로 쓰지 않는다.** 동등성 검정(TOST 등)은 하지 않는다. "동등하다"나 "차이가 없다"고 쓰지 않는다.
- **해석 표**(서술용. 결과를 본 뒤 정의를 바꾸지 않는다)

| 관찰 | 서술 |
|---|---|
| A−N의 CI가 0을 포함하고 ±0.01 안에 있음 | predictor 수준에서 prior 효과가 이 설계로는 실용적으로 작다(동등성 주장 아님) |
| A>N이고 A>R, R≈N | PCMCI+ 구조 자체가 도움이 된다는 근거 |
| A≈R>N | 희소도·lag 형식이 도움이 되며, 구조 정체성의 근거는 아님 |
| A<N | prior가 predictor를 제약한다는 근거(v3 §2.3의 장벽 관찰과 연결) |
| 그 밖의 경우 | 판정 불가로 보고 |

## 6. 비용과 대상 (ks 실측 기반 추정, 1 job/GPU, GPU 4장)

| 실험 | 대상 | 학습 run | 학습 시간/run (실측 근거) | 평가 (CF off) | GPU-시간 | 벽시계 |
|---|---|---|---|---|---|---|
| P3-PSM | PSM × seed 0–3 × 4 arm | 16 | 약 79분 (ks noalign PSM 78.5분, sp2x2 PSM 79~81분) | 약 2.4분 | 약 22 | 약 5.5시간 |
| P3-SMD | SMD 28 entity × seed 0–3 × 4 arm | 448 | 약 20~23분 (ks noalign SMD 1-* 19.8분, sp2x2 SMD 1-1 약 23분) | 약 1.0분 | 약 157~180 | 약 39~45시간 |
| **1단계 합계** | | 464 | | | **약 179~202** | **약 45~50시간** |
| P3-SWaT (2단계, 선택) | SWaT51 × seed 0–1 × 4 arm | 8 | 약 29시간 (swatcrs2 PERM0 실측 epoch 속도) | P-only라 CF eval(약 1.5시간)보다 짧음(미실측) | 약 236 | 약 59시간 |

- D arm은 q/k가 없어 조금 가볍다(따로 실측하지 않음).
- **시작 가능 시점:** ks GPU 4장은 SWaT CRS×PERM seed 0–3 queue 두 개가 쓰고 있다. 완료 추정은 10-20 저녁~10-21이다. 그 전에 시작하려면 우선순위 결정이 필요하다.
- **축소안:** SMD 28 × seed 0–1 + PSM 4 seed. 약 100 GPU-시간, 약 25시간이다. 대신 seed macro sd 추정이 약해진다.

## 7. 학습 승인 후 실행 절차

1. 이 branch 커밋을 별도 실행 worktree(`exec/p3_<sha>`)로 checkout한다. dev worktree에서는 실행하지 않는다.
2. `run_experiments.py --dry-run`으로 queue를 확인하고 `scripts/verify_p3_plan.py`로 검증한다. 검증 항목: resolved config, config·데이터 sha256, A·R·D의 cache hit 여부, N의 prior job no-op.
3. 보고하고 승인을 받는다.
4. tmux에서 launcher를 실행한다. 진행 중인 다른 실험은 선점하지 않는다.
5. 완료 후 무결성 점검(P0와 같은 항목 + `prior_info`)과 §5 분석을 한다. 게시는 별도 승인을 받는다.

## 8. 위험과 한계

- N의 gate 초기값(0.15 균일)은 A(prior 안 약 0.36, 밖 약 0.053)와 다르다. 이것은 prior 효과의 정의에 포함된다(경로 2).
- `SELF_LOOP_BIAS`와 lag-1 self loop는 모든 arm에 남는다. 모델 기본값이지 PCMCI+ 정보가 아니다.
- R의 degree 수열은 실제 PCMCI+ 결과에서 왔다. hub가 강한 entity는 실제 지지집합과 상당히 겹친다(§4).
- D는 초기화와 batch 순서까지 A와 다르다(§2).
- 데이터셋마다 AdamW decay 누적곱이 다르다(SWaT 0.29, PSM 0.992, SMD 0.982; v3 §K.2-2). 그래서 초기화로 들어간 prior(경로 1~3)의 잔존량이 데이터셋마다 다르다.
- 1단계는 CRS·개입·CF와 prior의 상호작용을 다루지 않는다.
