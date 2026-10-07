# 남은 실험 계획 (js -> ks 인계, 2026-10-07)

우선순위 순서다. 각 항목에 목적, 조건, 실행법, 예상 비용, 검증 절차를 적었다.
모든 학습은 CODE_SHA 49f630a, 추적 파일 수정 없음을 전제한다.
`PITFALLS.md`를 먼저 읽을 것. 특히 2번(START_CLS_EPOCH=99999)과 3번(PERM_PAIRS 의미)은 이 계획의 전제다.

---

## P1. SWaT / SMD의 PERM_PAIRS=2 확인  (가장 중요)

### 목적
js의 PSM 2x2에서 **CRS loss는 개입이 켜져 있을 때만 작동한다**는 상호작용을 발견했다(P_raw AUC-PR +0.1123, 4/4 seed, p=0.0003).
PERM=0 단독, CRS 단독으로는 효과가 0이다. 이것이 PSM 한 데이터셋 결과인지, 모델의 일반적 성질인지 확인해야 한다.
확인되면 논문의 CRS 주장이 성립한다. 확인되지 않으면 PSM 특이 현상이다.

### 조건 (데이터셋당 2x2, seed 0-3)
`<BOOTSTRAP>/server8/handoff/pkg/configs/psm_cf_val_perm{0,2}_crs{on,off}.yaml`을 그대로 본떠
SWaT/SMD용 4개 config를 만든다. 조작은 두 줄뿐이다.

| 조건 | PERM_PAIRS_PER_BATCH | START_CLS_EPOCH |
|---|---|---|
| perm0_crsoff | 0 | 99999 |
| perm0_crson  | 0 | 5 |
| perm2_crsoff | 2 | 99999 |
| perm2_crson  | 2 | 5 |

나머지는 `*_cf_val.yaml` 기준값 그대로. SWaT은 `EXPECTED_N: 51`, batch 128, LR 5e-4. SMD는 batch 512, LR 5e-4.

### 비용 (js 실측 기반 외삽)
PERM=2는 PERM=0의 약 2.2배다(PSM: 4,900초 -> 10,900초).

| dataset | run 수 | PERM=0 run당 | PERM=2 run당 | GPU-시간 |
|---|---|---|---|---|
| SWaT | 16 | 약 23시간 | 약 50시간 | 약 580 |
| SMD (20 entity) | 320 | 약 20분 | 약 45분 | 약 170 |

SWaT이 매우 비싸다. **권고: SMD를 먼저 돌린다.** 170 GPU-시간이면 8 GPU에서 약 1일이다.
SWaT은 seed 2개(0,1)로 줄여 8 run(약 290 GPU-시간)만 확인하는 축소안도 가능하다.

### 실행
`<BOOTSTRAP>/server8/handoff/pkg/scripts/run_ablation.sh`의 tag 목록에 새 tag를 추가하고
`manifest_<tag>_<server>.yaml`을 만든다. `manifest_psmcrs_server8.yaml`이 4개 config를
한 manifest에 담는 예시다(train 스펙 4개, 각 seeds [0,1,2,3]).

    run_ablation.sh <tag> --dry-run      # 큐 확인
    run_ablation.sh <tag> --execute      # tmux 세션 1개로 실행
    run_ablation.sh <tag> --status

### 검증 (실행 직후 반드시)
1. resolved config diff가 조작 두 줄만인지 확인
2. `crson` 로그에 `use_cstruct=True`가 76회(ep5~80), `crsoff`에 `use_cstruct=False`가 80회
3. `perm2_*` 로그의 `perm=` 값이 0이 아닌지, `perm0_*`은 전부 0인지
4. checkpoint에서 `max|cls_ref - normalize(te_prior_weight)|`가 PERM=0은 ~1e-07, PERM=2는 >0.1인지

### 분석
2x2 요인 분해로 CRS 주효과, 개입 주효과, 상호작용을 분리한다. js가 쓴 식:

    CRS 주효과  = ((a01-a00) + (a11-a10)) / 2
    개입 주효과 = ((a10-a00) + (a11-a01)) / 2
    상호작용    = (a11-a10) - (a01-a00)

a00=perm0_crsoff, a01=perm0_crson, a10=perm2_crsoff, a11=perm2_crson.
PSM에서 상호작용(+0.1153)이 주효과(+0.0546, +0.0576)의 2배였다. 같은 패턴이 나오는지 본다.

---

## P2. CALIBRATE=True 재scoring  (학습 불필요)

### 목적
모든 config이 `CALIBRATE: False`라 채널별 robust z-score 경로가 한 번도 실행되지 않았다.
그 결과 C가 합성 스코어 판별폭의 0.3~1.6%만 차지해 참여하지 못한다(`PITFALLS.md` 5번).
보정을 켜면 C가 P/CF와 비슷한 비중을 받는다. C 단독 AUC-PR이 기준선을 크게 웃돌므로(SWaT 0.3504 vs 0.1213)
보정 후 기여 가능성이 있다. **"C가 쓸모없다"는 현재 결론은 보정 미시험을 전제한 것이다.**

### 실행
기존 checkpoint를 그대로 쓴다. 학습 없음. `scripts/eval_ckpt.py`를 `--calibrate on`으로 재실행하거나
manifest의 `eval.calibrate`를 바꿔 eval_only 큐를 만든다.
`scripts/manifests/example_eval_only.yaml`이 eval_only 스펙 예시다.

**주의:** `main.py:81-84`가 보정 적합 시 `cf_profile`을 넘기지 않아 `CALIBRATE=True`면 CF 채널이
조용히 빠진다(`A`에서 gamma=0이 됨). `scripts/eval_ckpt.py` 경로를 쓰는지 확인할 것.

### 비용
checkpoint당 수 분. js 실측으로 PSM 평가가 380초, 학습 데이터 보정 적합이 추가된다.
GPU 소요가 작아 다른 학습과 병행 가능하다.

### 분석
보정 전후로 `A_off = P + C`가 `P` 단독과 달라지는지, 그리고 `A_on`이 `P + CF`와 달라지는지가 핵심이다.
지금은 둘 다 1e-4 미만으로 같다.

---

## P3. cfval_abl_noalign  (준비 완료, 미실행)

### 목적
`START_CLS_EPOCH=81`과 `ENABLE_PRIOR_LOSS=False`를 동시에 적용해 두 정렬 손실을 모두 끈다.
manifest와 config이 2026-09-13에 준비됐고 dry-run을 통과했으나 실행하지 않았다.

### 우선순위가 내려간 이유
PSM 2x2 결과로 보아 이 실험은 `cls_ref`가 prior로 퇴화한 상태(PERM=0)에서 정렬 손실을 끄는 것이다.
해석 범위가 좁다. P1을 먼저 하고, P1 결과에 따라 `PERM=2 + noalign` 조건으로 재설계하는 편이 낫다.

### 실행 (그래도 돌릴 경우)
    run_ablation.sh noalign --dry-run
    run_ablation.sh noalign --execute
규모는 SWaT 4 + SMD 20x4 = 84 run. config은 `START_CLS_EPOCH=81`이므로 **99999로 고치는 것을 권한다**(`PITFALLS.md` 2번).

---

## P4. 재현 checkpoint의 CF 채널 계산  (js에서 수행 권장)

### 목적
동료 프로토콜 재현 124 run(PSM 4 + SWaT 8 + SMD 28x4)의 저장된 점수에 CF가 없다.
저장 키가 `P, C, A, y, start`뿐이다. 그 위에 올린 CCM-TAD pf1/sf1 평가도 CF 없이 진행됐다.
CF는 js 실측에서 SWaT AUC-PR 0.7404로 P(0.6653)보다 높은 **가장 강한 채널**이다. 재분석 가치가 있다.

### 왜 js인가
checkpoint가 js에 있다. 전송하면 checkpoint 공개 금지 원칙에 걸리고 용량도 크다.
js에서 scoring만 돌려 지표 CSV만 보내는 것이 맞다.

### 비용
checkpoint당 forward 16배(원본 1 + 소스 15). 학습 데이터 프로파일 적합이 추가된다.
기존 P/C 계산의 약 16배.

---

## 보고서 집계

`scripts/export_results.py aggregate --campaign <name>`이 `reports/experiments` 아래를 캠페인 단위로 모은다.
ks/js 양쪽 결과를 합치려면 **한 쪽이 양쪽 브랜치를 fetch**해야 한다. `HANDOFF_README.md`의 절차를 따를 것.
