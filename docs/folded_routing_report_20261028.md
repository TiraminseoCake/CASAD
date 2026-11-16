# PICAAD Routing Strength Prior 주입 통합 (Folded Routing) — 코드 확인 및 최소 변경 보고

- 작성일: 2026-10-28
- 작업 위치: worktree `/home/mschae/CASAD_folded`, branch `exp/folded-routing` (미커밋, push 없음)
- 기존 코드, 진행 중인 job, checkpoint, 결과 파일은 변경하지 않음. 검증은 모두 CPU에서 수행.

---

## 1. 현재 코드의 두 prior 주입 경로와 실제 계수

두 경로가 같은 W(정규화된 `te_prior_weight` buffer)와 같은 clamp(`clamp_min(1e-8)`)를 사용하므로, 계수를 그대로 합칠 수 있음.

| 경로 | 위치 | 실제 연산 |
|---|---|---|
| ψ 초기화 | `set_te_prior` | `pred_logits(ψ) = 0 + 1.0·I(대각, 모든 lag) + a·log(clamp(W, 1e-8))` |
| forward bias | `get_pred_weights` | `score = ψ + b·log(clamp(W, 1e-8)) [+ Δ(X)]` → `(score + log(G + 1e-12)) / T` → softmax |

- **계수**: a = `PRIOR.INIT_SCALE` = 0.25, b = `PRIOR.BLEND` = 0.35
  - hb Full(PSM, SMD, SWaT_ds5)과 진행 중인 ablation의 실행 config가 모두 이 값임 → ψ 전용 계수 = **0.60**
- **ψ_base**: 0이 아님. 대각에 self-loop bias +1.0이 모든 lag에 붙어 있으며, 변경 후에도 유지
- **temperature**: T = `PRED_TEMP` = 1.0이 ψ와 bias를 함께 나누므로 접어 넣어도 의미가 같음
- **a는 gate 초기화와 공유됨**: `edge_log_alpha += 0.5·a·logit(M)`
  - 따라서 공통 계수를 올리지 않고 **ψ 전용 계수를 분리**함
- **ψ를 직접 참조하는 곳 없음**: 모든 loss와 scoring은 `get_pred_weights`를 거침. tew 등 prior alignment loss도 routing weight를 사용하므로 의미가 유지됨

## 2. 변경한 파일과 내용

- 기준 코드: HEAD(6982ead) + 현재 실험에 쓰는 미커밋 수정 파일 복사본
- `data`는 원본 폴더 symlink, prior cache는 읽기만 함(cache hit)

| 파일 | 변경 |
|---|---|
| `config.py` | `PRIOR.FOLD_INTO_PSI = False`, `PRIOR.PSI_INIT_COEFF = -1.0` 추가. 음수면 INIT_SCALE 사용, FOLD가 켜져 있으면 INIT_SCALE + BLEND 사용 |
| `model/build.py` | `apply_prior_to_model`에서 ψ 계수를 계산해 전달. FOLD on이면 0.25 + 0.35 = 0.60을 **실제 config 값으로 계산**(하드코딩 아님) |
| `model/modeling_picaad.py` | ① `set_te_prior`가 ψ 계수와 gate 계수를 따로 받음(gate는 계속 INIT_SCALE) ② 접었는지 표시하는 persistent buffer `_prior_folded` 추가(checkpoint에 저장, 없는 기존 checkpoint는 load pre-hook으로 False 처리) ③ `_prior_folded=True`면 forward bias 생략 |
| `scripts/verify_folded_routing.py` | 검증용 스크립트(신규) |

- 변경하지 않은 것: gate, structural factor(0.05+0.95M), attention mask, Δ, 모든 loss, intervention, CRS, 데이터, epoch, checkpoint 규칙, scoring/평가 코드
- W buffer(`te_prior_weight`)도 그대로 유지

## 3. 검증 결과

조건: PSM, seed 0, 동일 batch 512개. 30 step 학습(6 epoch × 5 batch, CRS 활성 구간 포함).

### A. 옵션 off(기본값) vs 기존 코드 — 완전 동일(bitwise)

- 초기 parameter·buffer, 첫 step의 routing·prediction·각 loss·모든 gradient, 30 step 후 parameter, torch/numpy RNG 상태가 모두 동일
- 차이는 새 buffer `_prior_folded` 하나가 추가된 것뿐

### B. Folded vs 기존 코드 (prior align on/off 두 설정 모두 같은 결과)

| 항목 | 결과 |
|---|---|
| ψ 이외의 초기 parameter와 buffer | 모두 동일 (`pred_logits`만 다름) |
| ψ_fold − (ψ_orig + 0.35·log W) | 최대 9.5e-7 (값 크기 최대 11.05, float32 반올림 수준) |
| 초기 routing weight | 최대 오차 6e-8 (static), 1.2e-7 (Δ 포함) |
| prediction / edge strength | 상대 오차 1.9e-7 / 2.3e-7 |
| loss: pred, teg | 동일 |
| loss: cstruct, tew | 차이 1.9e-9 / 1.2e-9 |
| **loss: perm** | **차이 3.2e-6 (상대 2.5e-4)** — 원인은 아래 |
| gradient (pred, cstruct, tew, teg) | 상대 노름 차이 3.7e-8 ~ 3.7e-6 |
| **gradient (perm)** | **상대 노름 차이 4.5e-2** |
| 데이터 순서, 개입 sampling RNG | 동일 |

#### perm 차이의 원인 (허용오차는 늘리지 않음)

- 초기에는 개입 효과 자체가 매우 작음: `delta_pos` 최댓값 3.8e-6
- `|x − pred_perm| − base_err`가 거의 0이며, 12,800개 원소 중 5,600~9,800개가 |r| < 1e-6
- 반올림 수준 차이(약 2e-7)만으로 `clamp(min=0)` 경계의 부호가 4,100~4,400개 원소에서 뒤집힘
- 이후 `normalize_vector`가 거의 0인 `delta_pos`를 정규화하면서 차이를 증폭
- 기존에 보고된 "초기 ReLU 경계" 문제와 같은 현상. 같은 원인으로 30 step 후 parameter 차이가 약 2e-4까지 벌어짐
- `pool.score.bias` gradient의 상대 오차가 커 보이지만, softmax 이동 불변성으로 원래 0이어야 하는 gradient(1e-13 수준)의 잡음이라 의미 없음

#### 별도로 발견한 점 (변경하지 않음, 검토 제안)

- 초기 perm gradient 노름이 2.8e3으로 pred(0.22)보다 훨씬 큼
- gradient clip(1.0)이 걸리면 학습 초반 업데이트 방향을 거의 perm이 결정
- 그런데 그 perm 신호가 위와 같이 반올림 잡음 수준임 → 연구팀 검토 필요

### C. checkpoint 복원

| 시나리오 | 결과 |
|---|---|
| Folded ckpt를 기존 config(FOLD off)로 복원 | `_prior_folded=True`로 복원되어 bias가 다시 더해지지 않음. ψ는 저장값과 동일, 출력은 FOLD on config 복원과 완전히 같음 |
| 기존 ckpt(`PSM/no_prioralign` seed0 best_smooth, epoch 79)를 새 코드로 복원 | FOLD off/on config 모두 `_prior_folded=False`로 복원. 출력이 기존 코드와 완전히 같음 |
| Folded ckpt를 기존 코드로 복원 | `_prior_folded` key가 없어 strict load 에러. 잘못 복원되지 않고 실패함 |
| epoch 복원 | `payload['epoch']`가 `_current_epoch`로 정상 복원 (79, 6 확인) |

### D. 학습 궤적은 동일하지 않음

AdamW weight decay(0.01)가 이제 접어 넣은 prior 성분(0.35·log W, 최대 크기 약 6.4)에도 적용됨. 초기 함수는 같지만 학습 궤적은 기존과 다름. 대략적인 감쇠량(lr·wd·steps):

| 데이터 | lr | step 수 | 접힌 성분 감쇠 |
|---|---|---|---|
| PSM | 5e-5 | 약 1.7만 | 약 0.8% |
| SMD | 5e-4 | 약 3.5천 | 약 1.8% |
| SWaT_ds5 | 5e-4 | 약 1.2만 | 약 6% |

→ "기존 학습을 정확히 재현한다"고 할 수 없음. optimizer 보정은 요청대로 넣지 않음.

## 4. 기존 실험 상태와 Folded 전환 시 분류

공통 설정(아래 표의 기준, 다른 경우만 별도 표기):
- PSM LR 5e-5, SMD·SWaT LR 5e-4
- 80 epoch, batch 512, train_sub fit, seed 0–3
- checkpoint: best_smooth 기본, best_val·last도 저장
- 점수 A = P + C (raw), 평가는 point label 기준 `paper_eval`
- SWaT는 5배 다운샘플(`data/SWaT_ds5`), 51 변수

| 상태 | 실험 | 모델 버전 | 분류 |
|---|---|---|---|
| 완료 | PICAAD Full, old base (`results/hb`, PSM / SMD28 / SWaT_ds5) | tew+teg on, 기존 routing | **새 학습 필요** |
| 완료 | PICAAD Full, new base (`ablation_hb/{PSM,SMD,SWaT_ds5}/no_prioralign`) | tew+teg off, 기존 routing | **새 학습 필요** |
| 완료 | PSM ablation, old base 8개 변형 (`ablation_hb/PSM`) | old base | 비교용으로만 재사용. Folded 결과로 쓰려면 새 학습 필요 |
| **진행 중** | PSM ablation, new base 6개 변형 (`ablation_hb/PSM_noalign`, 24 run, 18시경 완료 예정) | new base, 기존 routing | 중단하지 않음. Folded 결과로 쓰려면 5개 변형은 새 학습 필요, **w/o Prior는 그대로 재사용 가능**(prior가 없으면 두 경로 모두 꺼져 Folded와 같은 모델) |
| 완료 | CAROTS (공식 코드), OracleAD v2 | 외부 모델 | **그대로 재사용** |
| 완료 | scoring 분석(MAD·z 결합, CF, label mode, val threshold) | 이전 checkpoint (B00/hb, 일부 출처 혼재) | **설정 확인 필요**. Folded checkpoint 생성 후 **평가만 재실행** |
| 완료 | 이전 프로토콜 결과(B00 bs128, SWaT 원본 해상도) | 이전 프로토콜 | 참고용, 설정 확인 필요 |
| 대기 | SMD/SWaT ablation, Freeze-4, Random prior | – | 미구현·미실행 |

- 기존 checkpoint에 Folded config만 적용해 재평가하는 방식은 사용하지 않음
- 따라서 "평가만 재실행하면 되는" 기존 학습 결과는 없음

## 5. Folded를 최종 모델로 쓸 때 필요한 최소 실행 목록

기준: new base(prior align off) + Folded

1. **Folded Full**: PSM 4 + SMD28 × 4 (112) + SWaT_ds5 4 = **120 run** (noalign 확인 실험과 같은 구성, 약 12시간)
2. **Folded PSM ablation**: δ, CRS, I0U0, I1U0, I0U1 × 4 = **20 run** (약 7시간). w/o Prior는 재사용
3. **scoring 분석 재평가**: 필요한 경우에만 Folded checkpoint로 재계산 (학습 없음)
4. **CAROTS, OracleAD**: 그대로 사용

합계 140 run, GPU 약 1일.

---

### 참고

- 처음 요청에 있던 JS 기준 commit(`f485d8d`)은 서버와 원격 저장소 어디에서도 찾지 못함 → 검증은 현재 실험 코드 대비 결과임
- 연구팀 확인 전까지 기존 job 중단, 전체 재실행, 다른 loss·gate·scoring 변경, 원격 push는 하지 않음
