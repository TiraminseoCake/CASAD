# PSM ORIGINAL vs FOLDED 실험 설정

두 조건은 아래 구성이 모두 같고, **Routing의 prior 주입 위치만 다릅니다.**

- 표기: W = PCMCI+ strength prior(target별로 (τ, src) 방향 합이 1), M = PCMCI+ 연결 prior
- 모델: L = 10, τ_max = 5, lag_win = 5

---

## 1. Routing 방식

target별 routing weight:

`w = softmax_(τ, src) ( s + log G )`  (temperature 1.0)

| 조건 | score s | ψ 초기값 |
|---|---|---|
| ORIGINAL | ψ + 0.35·log W + Δ(X) | self-loop +1 + 0.25·log W |
| FOLDED | ψ + Δ(X) | self-loop +1 + 0.60·log W |

- ψ: 학습되는 routing logit (두 조건 모두 학습)
- Δ(X): Dynamic Correction. 인코더 출력 C로 `q(C)·k(C)ᵀ`를 계산
- Gate: `G = σ(edge_log_alpha) · (0.05 + 0.95·M)`
  - edge_log_alpha 초기값: `logit(0.15) + 0.125·logit(M)`
  - 학습됨
- 예측: `pred = Σ w·v + b`
- Edge strength: `E = w·|v|`
- Causal attention mask: lag별 MHSA에 `0.5·ramp·log σ(mask_logits)`를 더함
  - mask_logits 초기값: `0.5·logit(M)`
  - ramp: 처음 5 epoch 동안 0 → 1

## 2. Prior alignment

**사용하지 않음.** tew(routing과 W의 JSD), teg(gate와 M의 BCE) 모두 off.

prior는 loss가 아니라 다음 경로로만 반영됩니다.

- ψ 초기값 (ORIGINAL은 forward bias 포함)
- gate의 고정 factor와 초기값
- causal mask 초기값
- reference 초기값
- 개입 대상 샘플링

## 3. 직접 Intervention Loss

- **개입 대상**: batch마다 (τ, src) 2쌍. M의 source 중요도에 비례해 샘플링
- **개입 방법**: src 변수의 `[L−τ−5, L−τ)` 구간을 batch 안에서 permute
- **반응**: target별 오차 증가분

  `δ = mean_batch clamp( |x − x̂_perm| − |x − x̂|, 0 )`

  - 기준 오차 `|x − x̂|`는 detach
- **Loss**: `MSE( normalize(E[τ, src, :]), normalize(δ) )`
- **가중치**: 0.1, epoch 1부터

## 4. CRS alignment

- **Loss**: `KL( ref ‖ normalize(mean_batch E) )`
  - 정규화는 target별로 (τ, src) 방향
- **가중치**: 1.0, epoch 5부터

## 5. Reference 갱신

- **초기값**: W
- **매 epoch 끝에 갱신**
  1. 그 epoch에 개입한 (τ, src) 행별로 δ를 평균하고 정규화해 `epoch_ref`를 만든다
     - 개입하지 않은 행은 기존 ref 값을 사용
  2. `ref ← normalize( 0.9·ref + 0.1·epoch_ref )`
- gradient 없음 (no_grad)
- 갱신된 ref는 CRS loss의 target이자 anomaly score C의 기준으로 쓰임

## 6. Anomaly score

- **P**: `mean_i |x_L − pred|`
- **C**: τ별 `RMS( normalize(E_window) − ref )`를 τ에 대해 평균
- **주 score**: `A = P + C` (raw 합, calibration 없음)
- **보조**: 같은 checkpoint의 P_raw
- **시간축 정렬**: window 점수를 마지막 시점에 할당하고, 앞 L−1개 점은 제외

## 7. Checkpoint

- **best_smooth (주 규칙)**
  - 매 epoch validation MAE(train 뒤 20%, 예측 L1)를 기록
  - epoch ≥ 20 구간에서 3점 이동평균이 최소인 epoch를 선택
- best_val(val MAE 최소)과 last(epoch 80)도 저장 (보조)
- test 성능은 선택에 사용하지 않음 (5 epoch마다 기록만)
- **학습**: 80 epoch, batch 512, AdamW(lr 5e-5, weight decay 0.01), grad clip 1.0, early stopping 없음
