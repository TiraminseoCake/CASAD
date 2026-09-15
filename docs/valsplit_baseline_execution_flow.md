# Val-Split Baseline 실험 실행 흐름 보고서

> **대상 결과**: `results/valsplit_baseline_20260911.csv`
> **실험 일자**: 2026-09-11
> **브랜치**: `feat/do-counterfactual`
> **설정 요약**: VAL_RATIO=0.2, EARLY_STOP=True, PATIENCE=10, CALIBRATE=False, A=P+C

---

## 1. CLI 진입점

```bash
python main.py --cfg scripts/configs/psm.yaml   # PSM 예시
python main.py --cfg scripts/configs/smd.yaml   # SMD
python main.py --cfg scripts/configs/swat.yaml  # SWaT
```

실행 시 `main.py:313` → `main()` 호출.

---

## 1-A. 사용된 YAML 설정 파일

### `scripts/configs/psm.yaml`
```yaml
DATA:
  NAME: PSM
  INPUT_DIR: data/PSM
SEEDS: [0, 1, 2, 3]
TRAIN:
  BATCH_SIZE: 512
  EVAL_EVERY: 5
TEST:
  BATCH_SIZE: 512
SOLVER:
  MAX_EPOCH: 80
  BASE_LR: 0.0001          # ⚠ YAML에는 1e-4이지만, parser fallback이 5e-5로 덮어씀
  GRADIENT_CLIP: 1.0
PICAAD:
  PRIOR:
    TYPE: pcmci
    PCMCI:
      ALPHA: 0.05
      SUBSAMPLE: 10000
  SCORING:
    CALIBRATE: False
EVAL:
  USE_MEDIAN_VUS_WINDOW: True
  DIAGNOSE_COMPONENTS: True
```

### `scripts/configs/smd.yaml`
```yaml
DATA:
  NAME: SMD
  INPUT_DIR: data/SMD
SEEDS: [0, 1, 2, 3]
TRAIN:
  BATCH_SIZE: 512
  EVAL_EVERY: 5
TEST:
  BATCH_SIZE: 512
SOLVER:
  MAX_EPOCH: 80
  BASE_LR: 0.0005
  GRADIENT_CLIP: 1.0
PICAAD:
  PRIOR:
    TYPE: pcmci
    PCMCI:
      ALPHA: 0.05
      SUBSAMPLE: 10000
  SCORING:
    CALIBRATE: False
EVAL:
  USE_MEDIAN_VUS_WINDOW: True
  DIAGNOSE_COMPONENTS: True
```

### `scripts/configs/swat.yaml`
```yaml
DATA:
  NAME: SWaT
  INPUT_DIR: data/SWaT
SEEDS: [0, 1, 2, 3]
TRAIN:
  BATCH_SIZE: 128
  EVAL_EVERY: 5
TEST:
  BATCH_SIZE: 128
SOLVER:
  MAX_EPOCH: 80
  BASE_LR: 0.0005
  GRADIENT_CLIP: 1.0
PICAAD:
  PRIOR:
    TYPE: pcmci
    PCMCI:
      ALPHA: 0.05
      SUBSAMPLE: 10000
  SCORING:
    CALIBRATE: False
EVAL:
  USE_MEDIAN_VUS_WINDOW: True
  DIAGNOSE_COMPONENTS: True
```

> **⚠ LR fallback 주의** (`utils/parser.py:18-22, 64-66`):
> `_DATASET_DEFAULT_LR = {'PSM': 5e-5, 'SMD': 5e-4, 'SWaT': 5e-4}`
> YAML에서 `BASE_LR`을 설정해도 CLI opts에서 설정한 것이 아니면 fallback이 덮어씁니다.
> PSM YAML의 `BASE_LR: 0.0001`은 실제로 무시되고 **5e-5**가 적용됩니다.
> SMD/SWaT은 YAML과 fallback이 동일(5e-4)하므로 차이 없음.

---

## 1-B. 관련 소스 파일 목록

### 학습 (Training) 경로
| 파일 | 역할 |
|---|---|
| `main.py` | 진입점, seed 루프, 최종 평가 오케스트레이션 |
| `config.py` | yacs 기반 기본 설정값 정의 |
| `utils/parser.py` | argparse + YAML 로드 + dataset LR fallback |
| `datasets/build.py` | entity 로드, `split_train_val()`, `SlidingWindowDataset` 생성 |
| `datasets/loader.py` | `get_train_dataloader()` — DataLoader 래핑 |
| `datasets/sliding_window.py` | `SlidingWindowDataset` 클래스 (시계열 → 윈도우) |
| `datasets/util.py` | `standardize_train_test()`, `reduce_label()`, `make_pseudo_env_ids()` |
| `model/build.py` | `build_model()`, `apply_prior_to_model()`, causal prior cache |
| `model/modeling_picaad.py` | `PICAAD` 모델 클래스 (forward, refs, gate) |
| `model/priors.py` | `build_pcmci_causal_prior()` — tigramite PCMCI+ |
| `trainer.py` | `PicaadTrainer` — 학습 루프, early stopping, ref 업데이트 |
| `model/losses.py` | `prediction_train_loss()`, `causal_structure_loss()`, etc. |
| `model/intervention.py` | `permutation_alignment_and_epoch_cls()` — 인과 개입 손실 |
| `layers/ops.py` | `normalize_causal_tensor_torch()`, `make_self_causal_fallback_torch()` |

### 평가 (Evaluation) 경로
| 파일 | 역할 |
|---|---|
| `main.py` (`_final_eval()`) | calibrator 피팅, 테스트 스코어링, 메트릭 수집 |
| `model/scoring.py` | `score_windows()`, `score_windows_raw()`, `apply_score_calibrator()` |
| `utils/evaluation.py` | `paper_eval_one()`, `run_epoch_eval()` |
| `metrics/paper_eval/metrics_api.py` | `get_metrics()` — F1, R-F1, Aff-F, AUC, VUS 계산 |
| `utils/misc.py` | `robust_loc_scale()`, `robust_zscore()`, `pct()`, `safe_mean_std()` |

### 데이터 파일
| 경로 | 내용 |
|---|---|
| `data/PSM/*.npz` | PSM 데이터셋 (train, test, label) |
| `data/SMD/*.npz` | SMD 데이터셋 (~28 entities) |
| `data/SWaT/*.npz` | SWaT 데이터셋 (51 변수) |
| `data/prior_cache/*.npz` | PCMCI+ prior 캐시 |

---

## 2. 설정 로드 (`main.py:223-224`)

```python
args = parse_args()       # utils/parser.py:25
cfg, _ = load_config(args) # utils/parser.py:45
```

### 2.1 `parse_args()` — `utils/parser.py:25-33`
- `--cfg`: YAML 설정 파일 경로
- `opts`: CLI 오버라이드 (예: `SOLVER.MAX_EPOCH 20`)

### 2.2 `load_config()` — `utils/parser.py:45-89`

1. `get_cfg_defaults()` → `config.py`에서 기본값 생성
2. `cfg.merge_from_file(args.cfg_file)` → YAML 병합
3. `cfg.merge_from_list(args.opts)` → CLI 오버라이드 병합
4. **Dataset-specific LR fallback** (`parser.py:18-22, 64-66`):
   - `_DATASET_DEFAULT_LR = {'PSM': 5e-5, 'SMD': 5e-4, 'SWaT': 5e-4}`
   - `user_set_lr`는 **CLI opts만 체크** (`cli_keys`), YAML은 체크하지 않음
   - 따라서 YAML에서 `BASE_LR`을 설정해도 CLI에서 명시하지 않으면 fallback이 덮어씀
   - **PSM**: YAML에 1e-4 → fallback 5e-5로 덮어씌워짐
   - **SMD/SWaT**: YAML과 fallback 모두 5e-4로 동일
5. `DATA.INPUT_DIR` 비어있으면 `{BASE_DIR}/{NAME}_npz`로 자동 설정
6. `RESULT_DIR` = `results/{DATA.NAME}/{auto_tag}_{timestamp}/`
7. `TRAIN.CKPT_DIR` = `{RESULT_DIR}/ckpt`

### 2.3 Baseline에서의 핵심 config 값

| 키 | 값 | 출처 |
|---|---|---|
| `PICAAD.VAL_RATIO` | `0.2` | config.py:102 (수정됨) |
| `PICAAD.EARLY_STOP` | `True` | config.py:103 (수정됨) |
| `PICAAD.PATIENCE` | `10` | config.py:104 (수정됨) |
| `PICAAD.SCORING.CALIBRATE` | `False` | config.py (baseline 당시 False) |
| `SOLVER.MAX_EPOCH` | `80` | YAML |
| `SOLVER.BASE_LR` | PSM: **5e-5** (fallback), SMD/SWaT: **5e-4** | parser.py fallback |
| `PICAAD.L` | `10` | config.py:61 (기본값) |
| `PICAAD.TAU_MAX` | `5` | config.py:62 (기본값) |
| `PICAAD.D` | `64` | config.py:64 (기본값) |
| `TRAIN.BATCH_SIZE` | PSM/SMD: **512** (YAML), SWaT: **128** (YAML) | YAML 오버라이드 |
| `SEEDS` | `[0, 1, 2, 3]` (4개) | YAML |
| `EVAL.USE_MEDIAN_VUS_WINDOW` | `True` | YAML |
| `EVAL.DIAGNOSE_COMPONENTS` | `True` | YAML |
| `PICAAD.SCORING.P_AGG` | `mean` | config.py:148 (기본값) |
| `PICAAD.SCORING.C_AGG` | `fro` | config.py:150 (기본값) |
| `PICAAD.SCORING.CAUSAL_LAG_AGG` | `mean` | config.py:154 (기본값) |

---

## 3. 디바이스 설정 및 디렉토리 생성 (`main.py:230-240`)

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mkdir(cfg.RESULT_DIR)
# config.yaml 저장 (재현성 보장)
with open(os.path.join(cfg.RESULT_DIR, 'config.yaml'), 'w') as f:
    f.write(cfg.dump())
```

---

## 4. Entity 로드 (`main.py:242-263`)

### 4.1 `list_entities()` — `datasets/build.py:38-43`
- `cfg.DATA.ENTITIES` 비어있으면 `{INPUT_DIR}/*.npz` glob하여 entity 이름 리스트 생성
- PSM: 단일 entity, SMD: ~28개 machine entity, SWaT: 단일 entity (51 변수)

### 4.2 `load_entity()` — `datasets/build.py:46-77`
1. `{INPUT_DIR}/{entity_name}.npz` 로드
2. NPZ에서 `train`, `test`, `label` 추출
3. `reduce_label()`: 다차원 label을 1D binary로 축소
4. `standardize_train_test()` (`DATA.SCALE='standard'` 일 때):
   - train 기준 (mu, sd) 계산
   - train, test 모두 z-score 정규화
5. `EntityArrays` 객체 반환:
   - `.train_z`: `[T_train, N]` z-score 정규화된 훈련 데이터
   - `.test_z`: `[T_test, N]` z-score 정규화된 테스트 데이터
   - `.y`: `[T_test]` 이진 라벨
   - `.mu`, `.sd`: 정규화 통계량
   - `.N`: 변수 수, `.T_train`, `.T_test`: 시계열 길이

---

## 5. Causal Prior 구축 (`main.py:269`)

```python
te_weight_np, te_gate_np = build_causal_prior_cached(cfg, entity.train_z, entity.name)
```

### `build_causal_prior_cached()` — `model/build.py:127-159`

1. **Cache key 생성** (`_prior_cache_key`, `build.py:102-124`):
   - `DATA.NAME`, `entity_name`, `PRIOR.TYPE`, `TAU_MAX`, `SELF_MASS`, `SEED`
   - PCMCI일 때: `CI_TEST`, `ALPHA`, `SUBSAMPLE`
   - 훈련 데이터 SHA-256 해시 포함 → 데이터 바뀌면 cache 무효화
2. **Cache 조회**: `data/prior_cache/{key}.npz`
   - 존재하면 즉시 로드 (cache hit)
   - 없으면 `build_causal_prior()` 호출 후 저장
3. **PCMCI+ prior** (`PRIOR.TYPE='pcmci'`):
   - `build_pcmci_causal_prior()` → tigramite 라이브러리 사용
   - `ci_test='ParCorr'`, `alpha=0.05`, `subsample=10000`
   - 반환: `te_weight_np [tau_max, N, N]`, `te_gate_np [tau_max, N, N]`

---

## 6. Seed별 실행 루프 (`main.py:283-284`)

```python
for seed in seeds:  # YAML: [0, 1, 2, 3] (4개 seed)
    metrics.append(_run_seed(cfg, entity, seed, te_weight_np, te_gate_np, device))
```

---

## 7. `_run_seed()` — `main.py:52-72`

### 7.1 모델 빌드 (`main.py:59-60`)

```python
model = build_model(cfg, N=entity.N).to(device)
apply_prior_to_model(cfg, model, te_weight_np, te_gate_np)
```

#### `build_model()` — `model/build.py:16-48`
- `PICAAD` 모델 인스턴스 생성
- 주요 파라미터: `N`, `L=10`, `tau_max=5`, `d=64`, `heads=4`, `enc_layers=2`
- `dynamic_graph=True`, `gate_init=0.15`

#### `apply_prior_to_model()` — `model/build.py:91-96`
- `model.set_te_prior(te_weight, te_gate, init_scale=0.25)`
- Causal prior를 모델의 `te_prior_weight`, `te_prior_gate` 텐서로 설정

### 7.2 Trainer 생성 (`main.py:65-69`)

```python
trainer = PicaadTrainer(cfg, model, entity, seed, device=device, ...)
```

---

## 8. `PicaadTrainer.__init__()` — `trainer.py:39-68`

1. 모델을 device로 이동, `reset_refs()` 호출 (cls_ref, w_ref 초기화)
2. AdamW optimizer 생성 (`lr`, `weight_decay` from config)
3. **Val-split** (`trainer.py:62-68`):
   ```python
   val_ratio = getattr(cfg.PICAAD, 'VAL_RATIO', 0.0)  # 0.2
   if val_ratio > 0:
       train_data, self.val_data = split_train_val(entity.train_z, val_ratio)
   ```
   - `split_train_val()` (`datasets/build.py:80-84`): 시간 순서 기준 뒤쪽 20%를 validation으로 분리
   - `train_data = train_z[:split]`, `val_data = train_z[split:]`
   - **이 분리가 핵심**: 실제 학습에 사용되는 데이터가 80%로 줄어들어 정규화 효과 발생
4. `get_train_dataloader()` (`datasets/loader.py:6-15`):
   - `build_train_dataset()` → `SlidingWindowDataset(train_data, L, env_ids, return_env=True)`
   - `DataLoader(batch_size=128, shuffle=True)`

---

## 9. `PicaadTrainer.train()` — `trainer.py:70-228`

### 9.1 Early stopping 초기화 (`trainer.py:76-80`)

```python
early_stop = getattr(cfg.PICAAD, 'EARLY_STOP', False) and self.val_data is not None
patience = getattr(cfg.PICAAD, 'PATIENCE', 10)
best_val_loss = float('inf')
patience_counter = 0
best_state = None
```

### 9.2 학습 루프 (매 epoch, `trainer.py:82-224`)

각 epoch에서:

#### (a) Forward pass (`trainer.py:99-106`)
```python
for X, env in self.train_loader:
    (_, pred, _, pred_weights, _, _, edge_strength, _, _) = self.model(X)
```
- **모델 forward**: 입력 `X [B, L, N]` → 9-tuple 반환
  - `pred [B, N]`: 다음 시점 예측
  - `pred_weights [tau_max, N, N]`: 예측 가중치 (routing)
  - `edge_strength [B, tau_max, N, N]`: causal structure

#### (b) Loss 계산 (`trainer.py:110-189`)

총 loss = λ_task × group_task + λ_causal × group_causal + λ_graphreg × group_graphreg + λ_robust × group_robust

| 그룹 | 구성 | λ |
|---|---|---|
| **task** | `prediction_train_loss` (L1) | 1.0 |
| **causal** | `te_weight_loss` + 0.5×`te_gate_loss` + `causal_structure_loss` (ep ≥ 5) | 1.0 |
| **graphreg** | `gate_sparsity` + 0.5×`lag_monotonic_penalty` | 0.05 |
| **robust** | `permutation_alignment_loss` + 0.5×`invariance_loss` | 0.10 |

- `causal_structure_loss`: ep ≥ `START_CLS_EPOCH`(5) 이후 활성화, cls_ref와의 차이
- `permutation_alignment_and_epoch_cls()`: 인과 개입 기반 정렬 손실 + CLS 누적

#### (c) Backward + gradient clip (`trainer.py:192-196`)
```python
self.optimizer.zero_grad(set_to_none=True)
loss.backward()
nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
self.optimizer.step()
```

#### (d) Reference tensor 업데이트 (`trainer.py:204`)
```python
self._update_epoch_refs(w_sum, w_cnt, cls_sum, cls_cnt)
```
- **w_ref** (routing reference, Π_ref): EMA(β=0.9)로 epoch-mean pred_weights를 누적
- **cls_ref** (causal reference structure, CRS): EMA(β=0.9)로 epoch-mean edge_strength 누적 후 normalize

#### (e) Early stopping 판정 (`trainer.py:210-222`)
```python
if early_stop:
    val_loss = self._compute_val_loss()
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        best_state = copy.deepcopy(self.model.state_dict())
    else:
        patience_counter += 1
        if patience_counter >= patience:
            break
```

**`_compute_val_loss()`** (`trainer.py:233-248`):
- val_data를 SlidingWindowDataset으로 감싸서 prediction loss 계산
- 오직 **prediction loss만** 사용 (causal, graph 등 제외)
- `loss = prediction_train_loss(X[:, -1, :], pred, loss_type='l1')`

#### (f) Best state 복원 (`trainer.py:226-228`)
```python
if best_state is not None:
    self.model.load_state_dict(best_state)
```

---

## 10. `_final_eval()` — `main.py:75-205`

학습 완료 후 최종 평가.

### 10.1 Calibrator 피팅 (baseline에서는 비활성)

```python
calibrator = None
if cfg.PICAAD.SCORING.CALIBRATE:  # baseline: False → 건너뜀
    train_scores = score_windows(model, entity.train_z, ...)
    calibrator = fit_score_calibrator(train_scores)
```

**참고**: baseline 당시 `CALIBRATE=False`이므로 calibrator는 None.

### 10.2 테스트 스코어링 (`main.py:97-101`)

```python
test_scores = score_windows(model, entity.test_z, device,
                            batch=cfg.TEST.BATCH_SIZE,
                            scoring_cfg=cfg.PICAAD.SCORING,
                            calibrator=None,  # baseline
                            cf_profile=None)
```

#### `score_windows()` — `model/scoring.py:204-246`

1. **`score_windows_raw()`** 호출 (`scoring.py:149-201`):
   - 테스트 데이터를 SlidingWindowDataset → DataLoader로 변환
   - 각 window `X [B, L, N]`에 대해:
     - **P (Prediction score)**: `err = |x_true - pred|`, `P_AGG='mean'` → 변수 차원 평균
     - **C (Causal structure deviation)**: `normalize(edge_strength) - cls_ref`, Frobenius norm + lag mean
     - **G (Routing deviation)**: `pred_weights - w_ref`, Frobenius norm + lag mean
   - 반환: `{"P_raw": [W], "C_raw": [W], "G_raw": [W]}`

2. **Calibrator 없으므로 비보정 경로** (`scoring.py:228-241`):
   ```python
   cal = {
       "P": raw["P_raw"],
       "C": raw["C_raw"],
       "G": raw["G_raw"],
       "S": cal["C"].copy(),
       "A": (cal["P"] + cal["C"]).astype(np.float32),  # ← A = P + C
   }
   ```
   - **G는 계산되지만 A에 포함되지 않음**
   - `A = P + C` (2-view scoring)

### 10.3 Timeline 변환 (`main.py:103-113`)

```python
score_t_dict = score_components_to_timeline(
    {k: test_scores[k] for k in comp_keys if k in test_scores},
    Tt=Tt, start=start,
)
```
- `score_components_to_timeline()` (`scoring.py:38-44`):
  - window-level 스코어 `[W]`를 timestamp-level `[T_test]`로 변환
  - `start = L - 1 = 9` (처음 9개 타임스텝은 NaN)
  - `arr[start:] = window_scores`

### 10.4 메트릭 계산 (`main.py:117-121`)

```python
mtr_A = paper_eval_one(A_t, entity.y, start, cfg.EVAL)
```

#### `paper_eval_one()` — `utils/evaluation.py:22-48`

1. `score = A_t[start:]`, `labels = y[start:]` (NaN 제거)
2. `sliding_window`:
   - `USE_MEDIAN_VUS_WINDOW=True` (YAML) → `get_median_anomaly_length(labels)` 사용
3. `paper_get_metrics()` (`metrics/paper_eval/metrics_api.py`):
   - **Standard-F1**: 최적 threshold에서의 F1
   - **R-based-F1**: Range-based F1
   - **Affiliation-F**: Affiliation-based F measure
   - **AUC-ROC**: Area Under ROC Curve
   - **AUC-PR**: Area Under Precision-Recall Curve
   - **VUS-ROC**: Volume Under Surface (ROC variant, window=100)
   - **VUS-PR**: Volume Under Surface (PR variant, window=100)

### 10.5 반환값

```python
return (A_PR, A_ROC, F1, PA_F1, EV_F1, R_F1, Aff_F1, VUS_ROC, VUS_PR)
```

---

## 11. Seed 집계 및 저장 (`main.py:286-310`)

```python
A_PR_m, A_PR_s = safe_mean_std([m[0] for m in metrics])
# ... (모든 메트릭에 대해 mean ± std 계산)
```

`_summarize_and_save()` → `{RESULT_DIR}/summary.csv` 저장.

---

## 12. 전체 실행 다이어그램

```
main()
 ├─ parse_args() + load_config()
 │   └─ config.py defaults → YAML merge → CLI merge → dataset LR fallback
 ├─ set_devices() + mkdir()
 ├─ for entity in list_entities():
 │   ├─ load_entity()
 │   │   └─ NPZ → standardize(mu, sd) → EntityArrays
 │   ├─ build_causal_prior_cached()
 │   │   └─ PCMCI+ → (te_weight, te_gate) [tau_max, N, N]
 │   └─ for seed in [0,1,2,3]:  (YAML: 4 seeds)
 │       └─ _run_seed()
 │           ├─ build_model() → PICAAD(N, L=10, d=64, ...)
 │           ├─ apply_prior_to_model()
 │           ├─ PicaadTrainer.__init__()
 │           │   ├─ split_train_val(train_z, 0.2)
 │           │   │   └─ 80% train, 20% val (temporal)
 │           │   └─ DataLoader(SlidingWindowDataset, batch=128, shuffle=True)
 │           ├─ trainer.train()
 │           │   └─ for ep in 1..80:
 │           │       ├─ forward + loss + backward + step
 │           │       ├─ update w_ref (EMA 0.9), cls_ref (EMA 0.9)
 │           │       ├─ early_stop check:
 │           │       │   ├─ _compute_val_loss() [pred loss on val set]
 │           │       │   ├─ if improved → save best_state
 │           │       │   └─ if patience(10) exhausted → break
 │           │       └─ restore best_state after loop
 │           └─ _final_eval()
 │               ├─ CALIBRATE=False → calibrator=None
 │               ├─ score_windows(test_z)
 │               │   ├─ score_windows_raw() → P_raw, C_raw, G_raw
 │               │   └─ A = P + C (G 미포함)
 │               ├─ score_components_to_timeline()
 │               └─ paper_eval_one(A_t, y)
 │                   └─ F1, R-F1, Aff-F, A-ROC, A-PR, V-ROC, V-PR
 └─ _summarize_and_save() → summary.csv
```

---

## 13. Baseline 결과 (`valsplit_baseline_20260911.csv`)

| Dataset | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|
| PSM | 53.87±2.15 | 41.55±1.78 | 77.00±0.31 | 74.44±2.22 | 58.09±4.66 | 70.83±2.40 | 53.42±3.77 |
| SMD | 50.00±1.00 | 41.67±0.60 | 87.42±0.86 | 82.97±1.14 | 45.29±1.05 | 85.15±1.01 | 43.31±1.19 |
| SWaT | 76.89±0.87 | 28.06±2.45 | 76.34±0.70 | 83.52±0.51 | 73.65±1.17 | 73.12±0.54 | 57.57±1.23 |

### 실험 조건 정리

| 항목 | PSM | SMD | SWaT |
|---|---|---|---|
| lr | **5e-5** (fallback) | 5e-4 | 5e-4 |
| batch_size | 512 (YAML) | 512 (YAML) | 128 (YAML) |
| max_epoch | 80 | 80 | 80 |
| val_ratio | 0.2 | 0.2 | 0.2 |
| early_stop | True | True | True |
| patience | 10 | 10 | 10 |
| CALIBRATE | False | False | False |
| scoring | A = P + C | A = P + C | A = P + C |
| seeds | [0,1,2,3] | [0,1,2,3] | [0,1,2,3] |
| USE_MEDIAN_VUS_WINDOW | True | True | True |
| DIAGNOSE_COMPONENTS | True | True | True |
| N (변수 수) | 25 | ~38 | 51 |

---

## 14. 핵심 관찰 사항

1. **Val-split의 정규화 효과**: 훈련 데이터를 80%만 사용하면서 과적합이 줄어들어 메트릭 개선
2. **Early stopping의 역할**: val prediction loss 기준으로 최적 epoch에서 조기 종료, 과적합 방지
3. **Scoring은 P+C (2-view)**: G(routing deviation)는 계산되지만 최종 A 스코어에 미포함
4. **Calibration 미적용**: robust z-score 정규화 없이 raw P, C 값 그대로 합산
5. **CRS/Π_ref는 EMA로 학습 중 누적**: ep ≥ 5부터 causal structure loss 활성화, 점진적 안정화
