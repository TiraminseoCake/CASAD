# P3 구조 대조 실험 설계 — PCMCI+ prior vs no-prior vs 구조 맞춘 random prior vs δ 제거

- 작성: ks 에이전트, 2026-10-12. 상태: **설계 문서만 작성했다.** 소스 구현과 학습은 하지 않았다.
- 기준 코드: trainer B `49f630ac8d324ba01390c1a1dcaa4386cd94ae84`. 아래 줄 번호는 모두 이 커밋 기준이다.
- 선행 문서: `Picaad_v3.md` §2.3(prior 주입 경로 7개), §6 P3, `KS_P0_FINAL_REPORT.md`.

## 0. 질문과 단계

| 질문 | 비교 |
|---|---|
| Q1. PCMCI+ prior가 predictor(P score)에 도움이 되는가 | A(실제 prior) vs N(no-prior) |
| Q2. 도움이 된다면 "그 구조" 덕분인가, 아니면 희소도·lag 분포라는 형식 덕분인가 | A vs R(구조 맞춘 random prior), R vs N |
| Q3. dynamic correction δ가 도움이 되는가 | A vs D(δ 제거 후 재학습) |

**1단계(이 문서의 범위).** 목적은 predictor 자체의 차이를 보는 것이다. 그래서 **prediction-only 목적함수와 `P_raw` 점수만** 쓴다.

- CRS·개입·prior 정렬 손실은 끈다.
- C/G/CF·calibration은 1단계 결론에 쓰지 않는다.
- 같은 perturbation profile을 no-prior predictor에 적용하는 CF 비교는 2단계다. Q1이 정리된 뒤에 한다.

## 1. 모든 arm에 공통으로 고정하는 것

| 항목 | 고정값 | 근거·확인 |
|---|---|---|
| 목적함수 | `ENABLE_PRIOR_LOSS=False`, `START_CLS_EPOCH=99999`, `INTERVENTION.PERM_PAIRS_PER_BATCH=0`. 나머지는 기본값(graphreg 세 항 False, `ENABLE_INV_LOSS=False`) | 결과적으로 `loss = 1.0 × L1 예측 손실`. 로그에서 80 epoch 내내 `tew=teg=cstruct=perm=graph=inv=0`인지 확인한다 |
| 데이터 | 기존 NPZ(sha256 = `results/data-identity` 기준값). val 0.2 시간순 분할, train_sub만으로 표준화. test는 학습·선택에 쓰지 않는다 | provenance의 split_id·fit_protocol·stats_check |
| seed | PSM 0–3, SMD 28 entity × 0–3. (2단계 SWaT 0–1) | 모든 arm이 같은 seed 번호를 쓴다 |
| 최적화 | 데이터셋 기본 LR(`utils/parser.py:18-22`: PSM 5e-5, SMD 5e-4, SWaT 5e-4), AdamW wd 0.01, batch 512, 80 epoch, grad clip 1.0 | resolved config diff가 arm 정의 키에서만 나야 한다 |
| checkpoint 선택 | validation 예측 MAE 최소(`VAL.MIN_DELTA=0`, 첫 최솟값) = best_val. last는 참고용 | P0와 같은 규칙이다. test 기반 선택은 금지 |
| 평가 | `scripts/eval_ckpt.py --ckpt_tag best_val --cf off --calibrate cfg`(CALIBRATE=False) | CF forward 0회. `P_raw`를 주 지표로 쓴다. 이미 계산되는 C/G/A_off는 보조로만 둔다 |
| 계산 조건 | ks GPU 4장, GPU당 job 1개, thread 4, 같은 launcher(`run_experiments.py`), derived YAML은 checkout 밖 | arm별 wall time을 기록한다(§5) |

## 2. Arm 정의

| arm | prior 입력 | 활성 prior 경로(prediction-only 기준) | δ |
|---|---|---|---|
| **A** 실제 PCMCI+ | 기존 cache(ParCorr, α 0.05, subsample 10000, τ_max 5, train_sub) | 1·2·3(초기화), 4(routing bias), 5(gate 구조 계수). 6·7은 목적함수에서 꺼짐 | on |
| **N** no-prior | **없음.** PCMCI+를 계산·로드하지 않는다. `set_te_prior`를 호출하지 않는다 | 없음 | on |
| **R** 구조 맞춘 random prior | A의 prior에서 만든 random 구조. A와 같은 `set_te_prior` 경로를 탄다 | A와 같다(구조만 random) | on |
| **D** δ 제거 | A와 같다 | A와 같다 | **off** (`PICAAD.DYNAMIC_GRAPH=False`, 기존 config 키) |
| (선택) **E** | N과 같다 | 없음 | off. prior×δ 2×2를 완성할 때만 쓴다. 별도 승인 |

### 2.1 N(no-prior)이 실제로 갖게 되는 상태

`has_te_prior=False`일 때의 코드 경로다.

- **초기화**
  - `pred_logits`는 0이고, 모든 lag의 대각에 `SELF_LOOP_BIAS=1.0`이 더해진다(`modeling_picaad.py:88-91`). 이것은 모델 기본값이다. A에도 똑같이 있다.
  - `edge_log_alpha`는 전부 `logit(GATE_INIT=0.15)`다(`:93`).
  - `causal_mask_logits`는 0이다(`:116`).
- **MHSA:** `_causal_attn_mask`(`:319-330`)는 `causal_mask_logits`를 쓴다. 초기값이 0이면 모든 key에 같은 상수 bias가 붙어 softmax에 영향이 없다. 이후 학습으로만 바뀐다.
- **routing:** `prior_bias=0`이다(`:239-242`). 점수는 `pred_logits + δ + log σ(edge_log_alpha)`다.
- **gate:** 구조 계수 `(0.05+0.95·M)`이 없다(`:197-201`). `g_eff = σ(edge_log_alpha)`다.
- **손실:** `causal_prior_losses`는 0을 반환한다(`:272-275`). 1단계에서는 어차피 꺼져 있다.
- **기준 텐서:** 처음에 `cls_ref=0`, `has_cls_ref=False`다(`:143-152`). PERM0에서는 epoch 1이 끝난 뒤 self-causal fallback(lag-1 대각)이 들어간다(`trainer.py:283-290`). 1단계에서는 CRS 손실이 꺼져 있어 `cls_ref`가 쓰이지 않는다. 하지만 2단계에서 CRS를 다시 켜면 이것이 "prior 대신 self-loop 기준"이 된다는 점을 기록해 둔다.
- **CF source 선택:** `_select_cf_sources`(`scoring.py:74-80`)는 학습된 `σ(edge_log_alpha)`의 source 합으로 고른다. N에서는 이 gate에 prior 성분(경로 2 초기화, `teg` 손실)이 없다.
- **개입 샘플링:** `te_prior_gate`가 None이면 균등 샘플링이다(`intervention.py:31-59`, `:141-143`). 1단계는 PERM0이라 호출되지 않는다.

"neutral = uniform prior를 같은 경로에 넣는 방식"은 **N으로 쓰지 않는다.**

- 경로 2가 `edge_log_alpha`를 +0.125·logit(1−1e-4) ≈ +1.15만큼 균일하게 올린다. 그러면 gate 초기값이 0.15에서 약 0.36으로 바뀐다.
- prior 손실을 켜면 routing을 균등 분포 쪽으로 당긴다.
- 이 방식은 "prior 없음"이 아니라 "다른 prior"다.

### 2.2 R(random prior) 생성 규칙 (사전 고정)

A의 cache에 있는 prior `(te_weight[τ,s,t], te_gate[τ,s,t])`에서 시작한다.

1. lag-1 self-loop(`priors.py:537`의 `self_mass`, `set_te_prior`의 `te_gate[0,i,i]=1`)는 **그대로 둔다**. PCMCI+가 발견한 정보가 아니라 구조 기본값이기 때문이다.
2. 나머지 edge `(τ, s→t)`(gate 1 또는 모호 edge 0.5)는 **lag마다 degree를 보존하며 무작위 재배선**한다. 각 edge는 자기 weight 값과 gate 값을 그대로 가져간다.
   - 방식은 double-edge swap이다. self-loop와 중복 edge가 생기면 기각한다. swap 횟수는 edge 수의 10배다.
   - 보존되는 것: lag별 target in-degree 수열, lag별 source out-degree 수열, lag별 edge 수, gate 0.5 edge 수, target별 weight 다중집합.
   - 파괴되는 것: "어느 source인가"라는 정체성.
   - out-degree를 보존하는 이유가 있다. 개입 샘플링(2단계)과 CF source 순위가 행 out-degree에 의존하기 때문이다.
3. 정규화는 A와 같다(`(τ, source)`에 대해 target별 합 1).
4. **난수:** random prior 하나를 학습 seed 하나와 짝짓는다. RNG seed = `hash(entity, seed, "p3-random-v1")`다. 그래서 R도 A·N과 같은 run 수를 쓴다. random 구조의 변동은 seed 변동에 함께 들어간다.
5. 생성된 prior마다 sha256을 provenance에 기록한다. 다음 통계도 기록한다: lag별 in/out-degree 일치 여부, 실제 지지집합과의 Jaccard(우연 수준이어야 함), 보존 검사 결과.
6. 한계: R의 degree 수열은 실제 PCMCI+ 결과에서 왔다. 따라서 R은 "PCMCI-free"가 아니다. **구조 정체성만 뺀 대조군**이다.

### 2.3 D(δ 제거)의 주의점

- `DYNAMIC_GRAPH=False`면 `dynamic_q/k`(`modeling_picaad.py:95-98`)가 만들어지지 않는다. 그러면 그 뒤에 생성되는 모듈(`edge_value_head` 등)의 초기화 난수와 DataLoader shuffle 순서가 A와 달라진다(torch 전역 RNG를 공유하기 때문).
- 따라서 D와 A는 같은 seed 번호를 써도 초기화가 다르다. 그 차이는 seed 변동으로 흡수된다.
- 초기화까지 맞추려면 "q/k는 만들되 δ≡0"인 변형이 필요하다. 이것은 코드 변경이다. 1차 설계는 기존 config 키를 쓰고, 변형은 A−D 차이가 SESOI(§4)를 넘을 때만 확인용으로 둔다.

## 3. no-prior 누출 검증 (구현 후, 학습 전에 전부 통과해야 함)

### 3.1 정적 감사: prior가 닿는 모든 지점

| 경로 | 위치 | N에서 기대 동작 | 확인 테스트 |
|---|---|---|---|
| prior 생성·cache | `main.py:317-319`, `model/build.py:52-89` | PCMCI+를 호출하지 않는다. cache를 읽거나 쓰지 않는다. launcher prior job은 no-op | T4, T6 |
| 적용 | `main.py:63-68` → `apply_prior_to_model`(`model/build.py:92-97`) | 호출하지 않는다 | T1, T5 |
| 1 `pred_logits` 초기화 | `modeling_picaad.py:190` (블록 `:186-191`) | 더하지 않는다(self-loop bias만 남음) | T1, T2 |
| 2 `edge_log_alpha` 초기화 | `:191` | 더하지 않는다 | T1, T2 |
| 3 `causal_mask_logits` 초기화(MHSA) | `:194-195` | 0 유지 | T1, T2 |
| 4 routing prior bias | `:239-242` | 0 | T1, T3 |
| 5 gate 구조 계수 | `:197-201` | 없음 | T1, T3 |
| 6 prior 손실 | `:272-297`, `trainer.py:163-164` | 0(1단계는 플래그로도 꺼짐) | T4 |
| 7 `cls_ref` 초기값·CRS 손실 | `:183` (prior 버퍼 `:179-181`), `trainer.py:137`, `:283-307` | prior 대신 fallback. 1단계에서는 미사용 | T1, T5 |
| CF source 선택 | `scoring.py:74-80`, `:108` | 학습된 gate만 사용 | T1(2단계용) |
| 개입 샘플링 | `intervention.py:31-59`, `:141-143` | 균등. 1단계에서는 호출 0회 | T1, T4 |
| 평가 시 복원 | `eval_ckpt.py:66-67`, `:237` | `te_prior_*` 버퍼 0, `has_te_prior=False`로 복원. `set_te_prior` 미호출 | T6 |
| GAT prior bias | `modeling_picaad.py:374`(`GAT.ENABLE=False`라 미사용) | 사용 안 함을 확인 | T3 |

### 3.2 테스트 (CPU, 작은 N, 학습 없음)

- **T1 prior 불변성(가장 강한 검사).** no-prior 모드에서 서로 다른 prior 세 개를 공급한다. 실제 prior, R prior, 임의 난수 tensor다. 같은 seed로 다음이 **비트 단위로 동일**해야 한다.
  - 초기 `state_dict` 전체(파라미터 + 버퍼)
  - 고정 입력에 대한 forward 출력(pred, Π, gate)
  - 1-step 손실과 gradient
  - 1 epoch 뒤 `cls_ref`/`w_ref`
  - CF source 목록
  - PERM2를 임시로 켰을 때 개입 샘플 목록
  - 하나라도 다르면 prior 정보가 새는 경로가 남은 것이다.
- **T2 초기화 동등성.** 같은 seed에서 A와 N 모델의 파라미터 중 `set_te_prior`가 건드리지 않는 것은 전부 비트 동일해야 한다. 건드리는 세 개(`pred_logits`, `edge_log_alpha`, `causal_mask_logits`)는 "N 초기값 + 경로 1~3의 가산항 = A 초기값"이 정확히 성립해야 한다. R도 A와 같은 식으로 검사한다.
- **T3 forward 동등성.** N에서 routing logit이 `pred_logits + δ + log(σ(edge_log_alpha)+1e-12)`와 같고, MHSA mask가 `causal_mask_logits`만의 함수인지 직접 계산과 대조한다.
- **T4 런타임 로그 단언.** 모든 epoch에서 다음을 확인한다. `tew=teg=cstruct=perm=inv=0`, `use_cstruct=False`, `has_te_prior=False`(N). prior cache 접근이 0회(N)인지 파일 접근 hook이나 로그 marker로 확인한다.
- **T5 checkpoint 단언.** N의 `te_prior_weight/gate`가 전부 0이고 `_has_te_prior=False`다. A·R의 prior 버퍼 sha256이 provenance 기록과 같다.
- **T6 평가 provenance 단언.** N의 `prior_cache_key=None`, `restore.flags.has_te_prior=False`, `forward_passes.test_cf_forward=0`이다.
- **T7 기본 경로 비트 재현.** 새 코드의 A 경로(TYPE `pcmci`, RANDOMIZE `none`)가 49f630a와 비트 동일해야 한다. 기존 ks `cfval_abl_noalign` 결과로 확인한다. 이 결과는 `START_CLS_EPOCH=81`, `MAX_EPOCH=80`이라 99999와 동작이 같다. PSM seed0와 SMD machine-1-1 seed0의 val curve, best epoch, best_val checkpoint sha256을 비교한다. sp2x2 T0에서 쓴 방식과 같다.
- **T8 R 생성 검사.** §2.2-5의 보존 통계가 모든 entity·seed에서 정확히 일치하는지 확인한다. 실제 지지집합과의 Jaccard 분포도 보고한다.
- **T9 데이터 순서 동등성.** A·N·R의 같은 seed에서 첫 K개 batch 인덱스 hash가 같아야 한다. D는 §2.3 때문에 달라질 수 있으며, 그 사실을 기록한다.

### 3.3 사후 진단 (결과가 아니라 해석 보조)

- N과 R이 학습 후 실제 PCMCI+ 지지집합에 routing 질량을 얼마나 두는지 본다. 우연 기대값(지지집합 비율 1.6~4.1%)과 비교한다. 이것으로 "prior 없이도 그 구조를 다시 찾는가"를 기술한다.
- A·N·R·D의 gate 분포, 장벽(v3 §2.3 정의), δ 크기를 비교한다.

## 4. 분석 계획 (사전 고정)

- **주 지표:** best_val의 `P_raw` AUC-PR.
- **보조 지표**
  - validation 예측 MAE(predictor 품질)
  - AUC-ROC, VUS-PR, VUS-ROC, Standard-F1, Affiliation-F
- **주 대비**
  1. A−N (Q1, **1차 결론**)
  2. A−R, R−N (Q2)
  3. A−D (Q3)
  - 대비는 4개로 고정한다. 1차 결론은 A−N 하나로 내린다.
- **불확실성:** P0와 같은 방식이다(`scripts/analyze_smd28.py`의 정의를 그대로 쓴다).
  - SMD는 entity cluster paired bootstrap(B=10000, seed 20261012), seed별 28-entity macro, entity 부호 개수를 낸다.
  - PSM은 seed 4개 수준의 평균·sd·paired t(df=3)·부호 개수를 낸다.
  - (entity, seed) 쌍을 독립 표본으로 취급하지 않는다.
- **SESOI(제안, 승인 필요):** AUC-PR ±0.01.
  - "차이 없음"은 95% CI가 ±0.01 안에 있을 때만 쓴다.
  - CI가 0을 포함하지만 ±0.01을 넘으면 "판정 불가"로 쓴다.
- **해석 표**
  - A≈N: 1단계 predictor 수준에서 prior는 불필요하다.
  - A>N, A>R, R≈N: PCMCI+ 구조 자체가 도움이 된다.
  - A≈R>N: 희소도·lag 형식이 도움이 된다. 구조 정체성은 아니다.
  - A<N: prior가 predictor를 제약한다. v3 §2.3의 장벽 관찰과 연결된다.
  - 결과를 본 뒤 정의를 바꾸지 않는다.

## 5. 비용과 일정 (ks 실측 기반 추정)

| 단계 | 범위 | run | 학습 (실측 평균, GPU 4장 동시 실행 기준) | 평가 (CF off 실측) | GPU-시간 | 벽시계 (4 GPU) |
|---|---|---|---|---|---|---|
| 1단계 SMD | 28 entity × 4 seed × 4 arm | 448 | PERM0 약 20분/run (smdcrs·smdcrs20 PERM0 평균 19.6~21.1분) | 약 1.0분 (sp2x2 SMD) | 약 157 | 약 39시간 |
| 1단계 PSM | 4 seed × 4 arm | 16 | 약 78.5분/run (noalign PSM) | 약 2.4분 (sp2x2 PSM) | 약 22 | 약 5.5시간 |
| **1단계 합계** | | 464 | | | **약 179** | **약 45시간** |
| 2단계 SWaT (선택) | 2 seed × 4 arm | 8 | 약 29.5시간/run (swatcrs2 PERM0 실측 속도) | P-only라 CF eval(약 1.5시간)보다 훨씬 짧을 것(미실측) | 약 236 | 약 59시간 |

- 추가 학습 비용이 없는 부분
  - A·N·R은 step당 계산량이 같다. routing은 τ×N 전체에 대한 dense softmax이고, prior는 값만 바꾼다. D는 q/k가 없어 조금 가볍다.
  - PCMCI+ cache는 이미 있다(A·R·D). N은 PCMCI+가 필요 없다.
- **축소안(승인 시 선택):** SMD 28 × seed 0–1 + PSM 4 seed. 약 100 GPU-시간, 약 25시간이다. seed가 2개라 seed macro sd 추정이 약해진다.
- **기존 결과 재사용:** ks `cfval_abl_noalign`(PSM 4 seed + SMD 1-* × 4 seed)은 A arm과 같은 조건이다. 그러나 이전 지시("T0를 과거 noalign 결과로 자동 대체하지 않는다")에 따라 A도 새로 학습한다. noalign은 T7 비트 재현 대조에만 쓴다. 재사용하려면 별도 승인을 받는다.
- **시작 시점:** `cfval_abl_swatcrs2` 종료 후(추정 10-16 오후~밤). 진행 중인 실험은 선점하지 않는다.

## 6. 구현 요구사항 (미구현, 승인 후 별도 branch)

- **branch:** 49f630a에서 새로 판다. 예: `exp/p3-structural-ablation`. 실행 branch에 병합하지 않는다. 일반 push만 하고 force는 하지 않는다.
- **config 키 (기본값이면 49f630a와 비트 동일해야 함)**
  - `PICAAD.PRIOR.TYPE='none'`: `build_causal_prior_cached`와 `apply_prior_to_model`을 건너뛴다. launcher prior job은 no-op이다. provenance에는 `prior_cache_key=None`, `prior='none'`을 남긴다.
  - `PICAAD.PRIOR.RANDOMIZE ∈ {'none', 'degree_preserving_v1'}`: 실제 prior를 로드한 뒤 `set_te_prior` 전에 §2.2 규칙을 적용한다. random prior sha256과 보존 통계를 provenance에 남긴다.
  - δ 제거는 기존 `PICAAD.DYNAMIC_GRAPH=False`를 쓴다.
- **eval_ckpt.py:** `has_te_prior=False` checkpoint가 strict load되는지 확인한다. 필요하면 최소한으로 수정한다.
- **테스트:** §3.2의 T1~T9. T7은 GPU 1장, 짧은 학습 재현이라 실행 시점에 별도 승인을 받는다.
- 기존 실행 worktree, checkpoint, 결과, 진행 중 job은 건드리지 않는다. 설정은 checkout 밖 derived YAML로 표현한다. 학습 전에 dry-run 큐를 보고하고 승인을 받는다.

## 7. 위험과 한계

- N의 gate 초기값(0.15 균일)은 A(prior 안 약 0.36, 밖 약 0.053)와 다르다. 이것은 "prior 효과"의 정의에 포함된다(경로 2).
- `SELF_LOOP_BIAS`(전 lag 대각 +1.0)와 lag-1 self-loop는 모든 arm에 남는다. 모델 기본값이지 PCMCI+ 정보가 아니다.
- 데이터셋마다 결과가 다를 수 있다. AdamW decay 누적곱이 SWaT 0.29, PSM 0.992, SMD 0.982라서(v3 §K.2-2) 초기화로 들어간 prior(경로 1~3)의 잔존량이 데이터셋마다 다르다. 2단계 SWaT은 1단계 결과를 본 뒤 결정한다.
- 1단계는 prediction-only라서 CRS·개입과 prior의 상호작용은 다루지 않는다. 그것은 2단계(CF/CRS 재도입)와 P0 보고 §6의 PERM 분해 설계에서 다룬다.
