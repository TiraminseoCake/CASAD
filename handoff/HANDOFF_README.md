# js -> ks 인계 패키지 (2026-10-07)

js(8-GPU, 실행 식별자 server8)에서 완료한 실험 결과와, ks가 이어서 돌릴 실험의 계획·설정·경고를 담았다.
모든 학습 결과는 CODE_SHA `49f630ac8d324ba01390c1a1dcaa4386cd94ae84`, 추적 파일 수정 없음에서 나왔다.

## 0. 먼저 읽을 것

1. `PITFALLS.md` — 실행 전 필수. 특히 LR fallback(1번), CRS 끄는 방법(2번), PERM_PAIRS 의미(3번).
2. `plans/REMAINING_EXPERIMENTS.md` — 남은 실험 P1~P4, 우선순위·비용·검증 절차.
3. `KS_AGENT_BRIEF.md` — ks Claude 에이전트용 작업 지시서 (역할, 금지사항, P1~P3 절차, 보고 방식).
4. `reports/PSM_2x2_REPORT.md` — 이번 인계의 핵심 발견.

## 1. js에서 완료한 실험

결과 패키지는 각 캠페인의 전용 브랜치에 있다. **checkpoint, scores.npz, 데이터 NPZ, 로그는 포함되지 않는다**
(export 도구가 제외). 개인 경로는 `<BOOTSTRAP>`/`<HOME>` 등으로 치환했다.

| 캠페인 | 브랜치 | 내용 | job |
|---|---|---|---|
| cfval (baseline) | `results/cfval/server8` | SWaT51 x4 seed + SMD 20 entity x4 seed | 이미 게시됨 |
| cfval_abl_nocstruct | `results/cfval_abl_nocstruct/server8` | 위와 동일 조건, `START_CLS_EPOCH=81` | 273 |
| cfval_abl_noprior | `results/cfval_abl_noprior/server8` | 위와 동일 조건, `ENABLE_PRIOR_LOSS=False` | 273 |
| cfval_abl_psmcrs | `results/cfval_abl_psmcrs/server8` | **PSM 2x2** (PERM_PAIRS x START_CLS_EPOCH) x4 seed | 52 |

각 패키지 구성: `metrics.csv`, `run_manifest.json`, `config_resolved.yaml`, `provenance_summary.json`,
`artifacts.json`, `summary.md`. `metrics.csv`의 variant 열에 `P_raw / C_raw / G_raw / CF_raw / A_off / A_on`이 있고
지표 9종(AUC-PR, AUC-ROC, VUS-PR, VUS-ROC, Standard-F1, PA-F1, Event-based-F1, R-based-F1, Affiliation-F)이 붙는다.

### 받는 방법

    git fetch origin 'refs/heads/results/*:refs/remotes/origin/results/*'
    git worktree add /path/to/js_results origin/results/cfval_abl_psmcrs/server8
    # 또는 파일만:
    git show origin/results/cfval_abl_psmcrs/server8:reports/experiments/cfval_abl_psmcrs/server8/cfval_abl_psmcrs_server8/metrics.csv > psmcrs_metrics.csv

## 2. 핵심 발견 세 가지

### (1) CRS loss는 개입이 켜져 있을 때만 작동한다

PSM 2x2, P_raw AUC-PR, best_val, 4 seed:

| | CRS off | CRS on | Δ |
|---|---|---|---|
| 개입 off (PERM=0) | 0.4461 | 0.4430 | −0.0031 (p=0.79, 2/4 seed) |
| 개입 on (PERM=2) | 0.4460 | **0.5583** | **+0.1123** (p=0.0003, 4/4 seed) |

개입 단독으로도, CRS 단독으로도 효과가 0이다. 순수한 상호작용이다(상호작용 +0.1153 > 주효과 +0.0546/+0.0576).
원인은 `PITFALLS.md` 3번. PERM=0에서 `cls_ref`가 PCMCI prior로 고정되어 `cstruct`가 중복 prior 압력이 된다.

**기존 nocstruct 결론("CRS loss가 해롭다")의 적용 범위를 좁혀야 한다.**
정확히는 "cls_ref가 prior로 퇴화한 상태의 CRS loss는 해롭거나 무해하다"다.
SWaT/SMD에서 PERM=2를 확인하는 것이 P1이다.

### (2) C 채널은 척도 때문에 합성 스코어에 참여하지 못한다

`CALIBRATE=False`에서 C는 판별폭의 0.3%(SWaT)/1.6%(SMD)만 차지한다.
`A_off = P + C`가 `P` 단독과 네 자리까지 같고, `A_on = P + C + CF`가 `P + CF`와 같다(168 run 전수 확인).
C 단독은 신호가 있다(SWaT AUC-PR 0.3504 vs 무작위 0.1213). `CALIBRATE=True`는 미시험(P2).

### (3) CF가 가장 강한 보조 채널이다 (단, 지표에 따라 다름)

js cfval baseline, best_val AUC-PR:

| dataset | P | C | G | CF | A_off | A_on |
|---|---|---|---|---|---|---|
| SWaT | 0.6653 | 0.3298 | 0.4422 | **0.7404** | 0.6658 | **0.7482** |
| SMD | 0.4421 | 0.0671 | 0.2648 | 0.3199 | 0.4421 | **0.4536** |

SWaT에서 CF 단독이 P보다 +0.075 높다. 다만 구간 기반 지표(Event-F1, R-F1, Affiliation-F, PA-F1)는
CF를 더하면 내려간다. 주 지표를 AUC-PR로 쓸 때만 `A_on`이 유리하다.
그리고 PSM의 `perm2_crson` 조건에서는 처음으로 `A_on < A_off`가 된다(P가 강해지면 CF가 해롭다).

## 3. 남은 실험

`plans/REMAINING_EXPERIMENTS.md` 참조. 요약:

| | 실험 | 담당 권고 | 비용 |
|---|---|---|---|
| P1 | SWaT/SMD PERM_PAIRS=2 확인 | **ks** | SMD 약 170, SWaT 약 580 GPU-시간 |
| P2 | CALIBRATE=True 재scoring | ks 또는 js (학습 불필요) | 작음 |
| P3 | cfval_abl_noalign | ks (우선순위 낮음) | 84 run |
| P4 | 재현 checkpoint의 CF 계산 | **js** (checkpoint가 js에 있음) | 중간 |

설정 사본은 `configs/`, manifest는 `manifests/`, 실행 래퍼는 `scripts/run_ablation.sh`에 있다.
**경로가 `<BOOTSTRAP>`, `<RUNS>`, `<CASAD>`, `<REPO>`, `<CONDA>`, `<LOCKDIR>`, `<DATA_NPZ>` 플레이스홀더다.
ks 경로로 치환해 쓸 것.**

## 4. 최종 보고서 작성

양쪽 결과를 한 곳에서 합쳐야 한다.

    # ks에서
    git fetch origin 'refs/heads/results/*:refs/remotes/origin/results/*'
    # 각 브랜치의 패키지를 reports/experiments/ 아래로 모은 뒤
    python scripts/export_results.py aggregate --campaign <name> --expected_seeds 0,1,2,3

`aggregate`는 `result_kind`가 섞이면 거부한다(`export_results.py:307`). 캠페인 단위로 따로 돌릴 것.

보고서에 반드시 포함할 각주:

- 학습 코드 SHA와 publishing 커밋은 다르다. `run_manifest.json`의 `training_code_sha`가 기준이다.
- SMD entity 집합이 서버마다 다르다. js는 machine-2-*/3-* 20개, ks는 machine-1-* 8개였다.
  동료 프로토콜 재현은 28개 전부다. **직접 평균 비교 불가.**
- VUS는 window 의존이다. `USE_MEDIAN_VUS_WINDOW: True`라 entity마다 window가 다르다.
  서버 간·데이터셋 간 비교는 AUC-PR/AUC-ROC가 안전하다.
- PA-F1은 point-adjust라 신뢰도가 낮다. 주 지표로 쓰지 말 것.
- `PITFALLS.md` 4번의 죽은 설정 목록. 특히 `LAM_GRAPHREG=0.05`가 0을 곱한다는 사실은
  기존 문서가 "graphreg 활성"이라고 서술한 것과 모순된다.

## 5. 전송에서 제외한 것

다음은 원칙상 GitHub에 올리지 않았다. 필요하면 별도 협의 후 직접 전송한다.

- checkpoint(`*.pt`), score 배열(`scores.npz`), 데이터 NPZ, 실행 로그
- SSH 접속 정보, 토큰, 키
