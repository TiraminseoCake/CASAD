# Soft-prior 2×2 pilot — 사전 확정 프로토콜

**작성 시점** 2026-10-06, **어떤 학습/평가 결과도 보기 전에 확정**했다.
**기준 commit** `49f630ac8d324ba01390c1a1dcaa4386cd94ae84` (trainer B)
**실험 branch** `exp/soft-prior-2x2`, **개발 worktree** `/mnt/data/PICAAD/dev/soft_prior_2x2`

선행 진단: `/mnt/data/PICAAD/runs/cfval/ops/routing_diag_49f630a/`
(보고서는 `/home/sgshin/workspace/PICAAD/REPORT.md`)

---

## 1. 왜 이 두 항인가 (진단에서 넘어온 전제)

진단에서 prior 안/밖 logit 격차가 −16.5(PSM baseline) / −18.1(SMD baseline) nat로 측정됐고,
네 항으로 분해됐다. 이 pilot은 그중 **구조적으로 고정된 두 항만** 건드린다.

| 항 | 격차 (PSM bl) | 성질 | 이번 pilot |
|---|---|---|---|
| `BLEND · log(max(te_prior_weight, 1e-8))` | −5.764 | 구조 고정 | **ρ로 완화** |
| `log(0.05 + 0.95·M)` 부분 | −2.996 | 구조 고정 | **g_min으로 완화** |
| `psi` (pred_logits) | −4.772 | 초기화 잔존 | **건드리지 않음** |
| `log sigmoid(edge_log_alpha)` | −2.845 | 학습 | 건드리지 않음 |
| `dynamic_delta` | −0.132 | window별 | 건드리지 않음 |

**`psi` 초기화 잔존(약 −4.8 nat)은 이번에 제거하지 않는다.** 진단 §3에서 그 값이
`PRIOR.INIT_SCALE = 0.25 × log(clamp_min 1e-8) = −4.605`의 초기화 잔존물이고
72–80 epoch 동안 max |drift| 0.03–0.20으로 사실상 정지해 있음을 확인했으나,
`set_te_prior`나 `INIT_SCALE`을 바꾸면 네 조건의 초기 state가 달라져
2×2 분리가 불가능해진다. 따라서 이번 pilot은 **forward만** 바꾼다.

그 결과 **ρ와 g_min만으로는 non-prior mass가 크게 열리지 않을 것으로 예상된다.**
진단 §8의 logit-space 추정(재학습 아님)으로는 ρ=0.1 + g_min 상당의 완화가
PSM baseline 기준 1.1e-06 → 약 6e-04 수준이다. 이 pilot의 목적은
"support를 열었는가"가 아니라 **"forward 제약을 완화했을 때 학습이 어떻게 반응하는가"**를
재학습으로 처음 관측하는 것이다.

---

## 2. 정확한 두 수정

### 2.1 Forward prior smoothing (ρ)

```
D     = tau_max * N
u     = 1 / D
p_rho = (1 - rho) * te_prior_weight + rho * u
```

- **routing의 forward prior-bias 입력에만** 적용한다.
- 기존 처리 순서를 유지한다: `prior_bias = BLEND * log(clamp_min(p_rho, 1e-8))`,
  이후 `score = psi + prior_bias + delta`, `logit = (score + log(gate_eff + 1e-12)) / TEMP`,
  `(τ, src)` 축 softmax. log/clamp/epsilon/temperature 순서는 바뀌지 않는다.
- `te_prior_weight`의 각 target column은 D개 원소에 대해 합이 1이므로
  `p_rho`의 column 합도 정확히 1이다: `(1-ρ)·1 + ρ·D·(1/D) = 1`. 재정규화하지 않는다.
- **buffer를 덮어쓰지 않는다.** `te_prior_weight`, `te_prior_gate`, `cls_ref`, `w_ref`는 불변이며
  `causal_prior_losses`와 `set_te_prior`는 원본 buffer를 계속 사용한다.
- `rho == 0`이면 원본 경로를 그대로 호출한다(early return, bit-identical).

### 2.2 Effective gate floor (g_min)

```
G_native = sigmoid(edge_log_alpha) * (0.05 + 0.95 * M)
G_floor  = g_min + (1 - g_min) * G_native
```

- **전체 effective gate에 floor를 준다.** 구조 계수 `0.05`를 `0.2/0.5/1.0`으로 바꾸는 실험이
  **아니다**. `0.05`와 `0.95`는 그대로 둔다.
- `g_min == 0`이면 원본 경로를 그대로 호출한다(early return, bit-identical).
- `has_te_prior == False` 분기에도 같은 floor를 적용한다(정의상 "전체 effective gate").
  이번 pilot의 모든 조건은 `has_te_prior == True`이므로 실제로는 사용되지 않는다.
- 값 범위: `G_native ∈ [0, 1]` → `G_floor ∈ [g_min, 1]`.

### 2.3 건드리지 않는 것 (명시)

`psi` 초기화 · attention bias · `edge_log_alpha` 초기화 · `PRIOR.INIT_SCALE` · `set_te_prior` ·
encoder · `dynamic_scale` (delta 배율) · optimizer · `WEIGHT_DECAY` · `C`(edge_strength) 정의 ·
`cls_ref`/`w_ref` 갱신 규칙 · CF source 선택 로직 · scorer.

---

## 3. 네 조건

| 조건 | ρ | g_min |
|---|---|---|
| T0 | 0.0 | 0.0 |
| T1 | 0.05 | 0.0 |
| T2 | 0.0 | 0.05 |
| T3 | 0.05 | 0.05 |

**T0는 native 경로와 동일해야 한다** — 회귀 기준선이다.

### 모든 조건에 공통 고정

| 항목 | 값 | 출처 |
|---|---|---|
| `INTERVENTION.PERM_PAIRS_PER_BATCH` | 0 | loss_perm 구조적 비활성 |
| `ENABLE_PRIOR_LOSS` | False | te_w / te_g 제거 |
| `START_CLS_EPOCH` | 81 | `MAX_EPOCH=80` → cstruct 영구 비활성 |
| `SOLVER.MAX_EPOCH` | 80 | |
| `ENABLE_GATE_LOSS` / `GRAPH` / `LAGMONO` / `INV` | False | auxiliary OFF |
| `SCORING.CALIBRATE` | False | |
| `SCORING.USE_COUNTERFACTUAL` | False | CF 완전 비활성 (§5) |
| `VAL.ENABLE` / `VAL.FRAC` / `SELECTION_METRIC` | True / 0.2 / `pred_mae` | best_val 선택 |
| `TRAIN.EVAL_EVERY` | 0 | 학습 중 test 평가 없음 |

**최적화되는 loss는 prediction loss 하나뿐이다.** causal prior는 초기화와 forward에만 남는다.

### 실효 learning rate (주의)

`utils/parser.py:18-22, 65-66`의 `_DATASET_DEFAULT_LR`가
CLI로 `SOLVER.BASE_LR`를 주지 않으면 **YAML 값을 조용히 덮어쓴다.**

| DATA.NAME | 실효 BASE_LR | 선행 진단 checkpoint |
|---|---|---|
| PSM | 5e-05 | 5e-05 ✓ |
| SMD | 5e-04 | 5e-04 ✓ |
| SWaT | 5e-04 | (js 범위) |

따라서 파생 YAML에 `BASE_LR`을 적어도 효력이 없다. 네 조건은 모두 같은 실효 LR을 쓰며
선행 진단의 baseline/noalign과 일치한다. 이 동작을 **변경하지 않는다**(기존 실행 경로 보존).

---

## 4. 데이터 / seed 범위

| 서버 | entity | seed | 조건 | job 수 |
|---|---|---|---|---|
| ks | PSM, SMD `machine-1-1` | 0 | T0–T3 | 8 |
| js | SWaT51 | 0 | T0–T3 | 4 |

- seed는 0 하나다. **seed 간 분산은 이 pilot으로 측정되지 않는다.**
- entity는 ks 2개 + js 1개다. 데이터셋 전체 일반화를 주장하지 않는다.
- 80 epoch, `last.pt`와 `best_val.pt`를 저장한다.

### 초기 state 동일성

같은 entity/seed의 네 조건은 **같은 native 초기 parameter/buffer에서 시작한다.**
ρ와 g_min은 forward 전용 float 속성이고 `state_dict`에 들어가지 않으며
`set_te_prior`를 수정하지 않으므로, 동일 seed·동일 prior에서 네 조건의 초기
`state_dict` hash는 같아야 한다. 이를 테스트로 검증한다.

**학습된 baseline/noalign checkpoint를 warm start로 쓰지 않는다.**
모든 조건은 native constructor + prior initialization에서 새로 시작한다.

`prior_cache_key`와 입력 데이터(`data_fingerprint`)가 조건 간 동일해야 한다 —
ρ/g_min은 prior 계산에 들어가지 않으므로 cache key가 달라지면 설정 오류다.

---

## 5. 평가 경로

**best_val checkpoint만 평가한다.** `last.pt`는 저장하되 이번 pilot에서 평가하지 않는다.

| 항목 | 값 |
|---|---|
| primary metric | `P_raw` |
| secondary metric | `A_off = P_raw + C_raw` (기존 정의) |
| `CALIBRATE` | False |
| CF | 완전 비활성 |

평가는 **기존 `scripts/eval_ckpt.py --cf off`를 재사용한다.** 새 scorer를 복제하지 않는다.

CF가 실제로 호출되지 않음이 코드 구조로 보장된다:
- `eval_ckpt.py:303` `if cf in ('on','both'):` 블록 전체가 건너뛰어짐 →
  `counterfactual_score_windows`와 `fit_cf_profile` 모두 호출 0
- `eval_ckpt.py:284-285` config가 `USE_COUNTERFACTUAL=False`면 `--cf on|both`를 **거부**
- `model/scoring.py:208` `use_cf = USE_COUNTERFACTUAL and cf_profile is not None`
- `eval_ckpt.py`의 `ForwardCounter`로 phase별 forward 수를 기록 →
  `cf_profile_fit_forward`, `test_cf_forward` 키가 **존재하지 않아야** 한다

**`gamma=0`만 설정하고 CF를 계속 계산하는 방식은 사용하지 않는다.** `SCORE_GAMMA`에
의존하지 않고, CF 계산 자체가 호출되지 않는 경로를 쓴다.

`A_off`는 `eval_ckpt.py:299`에서 `(P_raw + C_raw)`로 계산되며,
이는 `CALIBRATE=False`일 때 native `score_windows`의 `cal["A"] = P + C`와 동일한 값이다.

---

## 6. 성공/실패 판정 규칙 (사전 확정)

### 6.1 판정하지 않는 것

- **non-prior mass 증가만으로 성공 판정하지 않는다.** mass가 1e-06에서 1e-04로 올라가도
  그 자체는 성공이 아니다. §1에서 예상한 대로 ρ/g_min만으로는 mass가 크게 열리지 않으며,
  이 pilot은 mass 목표치를 설정하지 않는다.
- **test 결과를 보고 ρ / g_min / epoch / scorer를 바꾸지 않는다.**
  T0–T3 네 조건과 best_val 선택 규칙은 위에 확정됐고, 결과를 본 뒤 재조정하지 않는다.
  추가 값(ρ=0.1 등)을 탐색하려면 별도 pilot으로 새 프로토콜을 쓴다.
- best_val 선택은 `val_pred_mae` 기준이며, test metric으로 epoch을 고르지 않는다.

### 6.2 기록할 관측 (판정이 아니라 기록)

조건별로 다음을 기록하고, 네 조건을 **같은 축에서 나란히** 비교한다.

1. `val_pred_mae` best 값과 best epoch
2. best_val에서의 `P_raw` 및 `A_off` 기반 test metric
3. non-prior mass (진단 A1과 동일한 정의, best_val 상태에서)
4. prior 내부 재정규화 entropy, window 간 TV (진단 A4와 동일한 정의)
5. `psi` / `edge_log_alpha`의 초기화 대비 drift (진단 2c와 동일한 정의)

### 6.3 이 pilot이 답할 수 있는 질문

- T0가 native noalign을 재현하는가 (회귀 확인)
- ρ와 g_min이 **학습 과정에서** `psi`/`edge_log_alpha`의 거동을 바꾸는가
  (진단은 추론 시점 재가중만 측정했다)
- 두 항의 효과가 가산적인가 (T3 vs T1+T2)
- 제약 완화가 prediction 성능을 해치는가

### 6.4 이 pilot이 답할 수 없는 질문

- seed/entity 간 분산 (seed 1개)
- `psi` 초기화를 함께 고치면 어떻게 되는가 (범위 밖, §1)
- 옵션이 활성화된 모델의 CF 거동 (**범위 밖**, §7)
- 최적 ρ/g_min (탐색하지 않는다)

---

## 7. 명시적 범위 밖

| 항목 | 이유 |
|---|---|
| **C gauge 보정** | 진단 C2에서 `edge_strength`가 gauge 의존(예측 불변 변환이 `C` 7–13%, `cstruct` 14–20% 변경)임을 확인했으나, 이번 pilot은 `C` 정의를 바꾸지 않는다. `A_off`의 `C_raw`는 기존 정의 그대로다. |
| **CF source 선택 변경** | `_select_cf_sources`의 raw-gate 사용과 prior outdegree 의존(Spearman 0.96–0.98)을 확인했으나 수정하지 않는다. |
| **weight decay 변경** | 진단 3b에서 prior 밖 gradient가 decay pull의 ~1e-9배임을 확인했으나 `WEIGHT_DECAY=0.01`을 유지한다. |
| **`psi` / `INIT_SCALE` / `set_te_prior`** | §1, §2.3 |
| **옵션 활성 모델의 CF 평가** | 이번 pilot은 CF를 끈 상태로만 평가한다. ρ/g_min이 CF source 선택과 effect에 주는 영향은 별도 작업이다. **native(옵션 0) CF 경로의 회귀는 보존한다.** |
| **trainer A / 3151f58 / PERM=2** | 기준 commit 밖. 가져오지 않는다. |

---

## 8. 보존 규칙

- 기존 실행 worktree(`/mnt/data/PICAAD/exec/cfval_49f630a`), checkpoint, 결과,
  진행 중 job을 변경하지 않는다.
- 기존 실행 branch에 병합하지 않는다.
- 공유는 `exp/soft-prior-2x2`의 일반 push만 허용하며 **force push를 금지한다.**
- 인증/remote 충돌 시 로컬 commit을 보존하고 보고한다.
- 진단/테스트가 RNG·parameter·buffer를 바꾸지 않음을 검증한다.

---

## 9. 검증 항목 (테스트로 확인)

| # | 항목 | 테스트 |
|---|---|---|
| 1 | T0와 native noalign의 forward/loss 및 짧은 학습 회귀 | `test_t0_*` |
| 2 | `p_rho`와 `G_floor`의 정확한 식·shape·범위 | `test_formula_*` |
| 3 | ρ=0 / g_min=0에서 원본 경로 유지 (bit-identical) | `test_zero_options_*` |
| 4 | 네 조건 초기 state 동일, 원본 prior/reference buffer 불변 | `test_init_state_*`, `test_buffers_*` |
| 5 | checkpoint에 옵션 저장, strict restore / `current_epoch` 복원 | `test_ckpt_*` |
| 6 | prior cache key와 입력 데이터가 조건 간 동일 | `test_cache_key_*` |
| 7 | 진단이 RNG/parameter/buffer를 바꾸지 않음 | `test_probe_*` |
| 8 | pilot 평가에서 CF fitting/forward 호출 0 | `test_eval_cf_off_*` |

테스트는 합성 fixture와 CPU에서 돈다(`tests/test_phase1b_val_trainer._synth_npz` 재사용).
**이번 작업에서 실데이터 학습과 test 평가는 수행하지 않는다.**
