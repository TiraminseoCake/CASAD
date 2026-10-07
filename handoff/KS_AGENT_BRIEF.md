# ks 서버 Claude 에이전트 작업 지시서

이 문서는 ks(4-GPU 서버) Claude 에이전트에게 그대로 주는 지시서다.
js(8-GPU, 실행 식별자 server8)가 완료한 실험과 이어서 돌릴 실험의 정의가 함께 들어 있다.

---

## 0. 역할과 목표

PICAAD 공동 실험의 ks 측 실행과 최종 보고서 작성을 담당한다. 최종 산출물은 세 묶음을 합친 보고서다.

1. ks가 이미 완료한 결과 (PSM 4 seed, SMD machine-1-1..1-8 x 4 seed 등)
2. js가 완료한 결과 (cfval baseline, nocstruct, noprior, PSM 2x2)
3. ks가 이번에 새로 돌릴 결과 (아래 P1~P3)

## 1. 금지 사항 (반드시 지킬 것)

- 인증 토큰·개인키·SSH 접속 정보를 로그나 출력에 쓰지 않는다. SSH 계정·키·접근권한을 임의로 만들거나 추정하지 않는다.
- checkpoint(`*.pt`), score 배열(`scores.npz`), 데이터 NPZ, 실행 로그를 **GitHub 어느 브랜치에도 올리지 않는다.**
- force push를 하지 않는다. 개인 경로·데이터·checkpoint를 게시하지 않는다.
- 기존 working tree에 자동 pull/merge/rebase/reset/stash/clean을 하지 않는다. results/data 심볼릭 링크를 삭제·변경하지 않는다.
- 진행 중인 다른 실험의 프로세스, tmux, env, manifest, queue, output을 변경하지 않는다.
- 다른 사용자 홈이나 대형 파일시스템 전체를 무작정 탐색하지 않는다.
- 기존 conda 환경을 자동 upgrade/downgrade하거나 sudo 설치하지 않는다.
- **pinned 실행 코드(CODE_SHA 49f630ac8d324ba01390c1a1dcaa4386cd94ae84)의 추적 파일을 수정하지 않는다.**
  설정 변경은 checkout 밖(bootstrap 류 디렉토리)의 config/manifest로만 표현한다.
- 새 학습을 시작하기 전에 반드시 dry-run으로 큐를 확인하고 사람의 승인을 받는다.

## 2. 먼저 할 일 (조회만, 변경 없음)

    git fetch origin 'refs/heads/results/*:refs/remotes/origin/results/*'
    git worktree add <WORKDIR>/js_handoff origin/results/handoff/js-20261007

그 안의 `handoff/` 아래를 이 순서로 읽는다.

| 파일 | 왜 |
|---|---|
| `HANDOFF_README.md` | 전체 지도. js 완료 결과 목록과 핵심 발견 3가지 |
| `PITFALLS.md` | **실행 전 필수.** 6개 함정. 모르고 돌리면 결과를 잘못 해석한다 |
| `plans/REMAINING_EXPERIMENTS.md` | P1~P4 계획. 조건, 비용, 검증 절차 |
| `reports/PSM_2x2_REPORT.md` | 이번 인계의 핵심 발견 상세 |
| `configs/`, `manifests/`, `scripts/` | 설정 사본. 경로가 플레이스홀더다 |

js 결과 데이터는 별도 브랜치에 있다. 받는 법은 `HANDOFF_README.md` 1절.

| 캠페인 | 브랜치 |
|---|---|
| cfval baseline | `results/cfval/server8` |
| nocstruct | `results/cfval_abl_nocstruct/server8` |
| noprior | `results/cfval_abl_noprior/server8` |
| PSM 2x2 | `results/cfval_abl_psmcrs/server8` |

## 3. 환경 확인 (조회만)

보고할 것: python 경로와 버전, torch/CUDA 버전, GPU 수와 여유 메모리, 데이터 NPZ 경로와 sha256,
prior cache 디렉토리, GPU lock 디렉토리, 사용 가능한 디스크 용량.
**js와 버전이 다르면 그 사실을 보고하고 멈춘다.** 임의로 맞추지 않는다.

js 기준값: CODE_SHA 49f630a, torch 2.6.0+cu124, PSM N=25 / SWaT N=51 / SMD entity별 상이.

## 4. 수행할 실험 (우선순위 순)

### P1 — SWaT / SMD의 PERM_PAIRS=2 확인  (최우선)

**왜 중요한가.** js가 PSM에서 발견한 것은 CRS loss가 **개입이 켜져 있을 때만** 작동한다는 상호작용이다.

| | CRS off | CRS on | Δ |
|---|---|---|---|
| 개입 off (PERM=0) | 0.4461 | 0.4430 | −0.0031 (p=0.79) |
| 개입 on (PERM=2) | 0.4460 | **0.5583** | **+0.1123** (p=0.0003, 4/4 seed) |

기존 SWaT/SMD ablation은 전부 PERM=0이었고, 그 조건에서는 `cls_ref`가 PCMCI prior로 퇴화한다(`PITFALLS.md` 3번).
즉 **"CRS loss가 해롭다"는 기존 결론은 퇴화 상태에만 적용된다.** 이 상호작용이 SWaT/SMD에도 재현되는지가 논문의 CRS 주장을 좌우한다.

**조건.** 데이터셋당 2x2, seed 0-3. `configs/psm_cf_val_perm{0,2}_crs{on,off}.yaml`을 본떠 SWaT/SMD용 4개를 만든다.
조작은 두 줄뿐이다.

    PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH : 0 또는 2
    PICAAD.START_CLS_EPOCH                   : 5(on) 또는 99999(off)

**99999를 쓸 것. 81을 쓰지 말 것.** 81은 MAX_EPOCH=80에 의존하는 암묵적 방식이다(`PITFALLS.md` 2번).

**비용.** PERM=2는 PERM=0의 약 2.2배다.

| dataset | run | GPU-시간 추정 |
|---|---|---|
| SMD 20 entity | 320 | 약 170 |
| SWaT | 16 | 약 580 |

**SMD를 먼저 할 것.** SWaT은 비싸므로 seed 0,1로 줄인 8 run 축소안을 먼저 사람에게 제안한다.
ks GPU가 4장이므로 js 추정(8장 기준)보다 벽시계가 2배 걸린다. 계획 단계에서 ks 기준으로 다시 계산해 보고한다.

**실행.** `scripts/run_ablation.sh`를 ks 경로로 치환해 쓰고 tag를 추가한다.
`manifests/manifest_psmcrs_server8.yaml`이 4개 config를 한 manifest에 담은 예시다.

    run_ablation.sh <tag> --dry-run      # 먼저 이것만. 큐를 보고하고 승인을 받는다
    run_ablation.sh <tag> --execute
    run_ablation.sh <tag> --status

**실행 직후 검증 (4개 모두 확인하고 보고).**
1. resolved config diff가 조작 두 줄만인가
2. `crson` 로그에 `use_cstruct=True`가 76회(ep5~80), `crsoff`에 `use_cstruct=False`가 80회인가
3. `perm2_*` 로그의 `perm=` 값이 0이 아니고, `perm0_*`은 전부 0인가
4. checkpoint의 `max|cls_ref − normalize(te_prior_weight)|`가 PERM=0은 약 1e-07, PERM=2는 0.1 이상인가

**분석.** 2x2 요인 분해. a00=perm0_crsoff, a01=perm0_crson, a10=perm2_crsoff, a11=perm2_crson.

    CRS 주효과  = ((a01−a00) + (a11−a10)) / 2
    개입 주효과 = ((a10−a00) + (a11−a01)) / 2
    상호작용    = (a11−a10) − (a01−a00)

PSM에서 상호작용(+0.1153)이 주효과(+0.0546, +0.0576)의 2배였다. 같은 패턴인지 본다.
seed별 paired t 검정과 개선 seed 수를 함께 보고한다. seed가 4개뿐이므로 효과 크기와 부호 일관성을 함께 제시한다.

### P2 — CALIBRATE=True 재scoring  (학습 불필요)

`CALIBRATE: False`가 모든 config의 기본이라 채널별 robust z-score 경로가 한 번도 실행되지 않았다.
그 결과 C가 합성 스코어 판별폭의 0.3~1.6%만 차지해 참여하지 못한다. `A_off = P + C`가 `P` 단독과 네 자리까지 같다.
C 단독은 신호가 있다(SWaT AUC-PR 0.3504, 무작위 기준선 0.1213). **현재의 "C는 쓸모없다"는 결론은 보정 미시험을 전제한 것이다.**

기존 checkpoint로 `scripts/eval_ckpt.py`를 `--calibrate on`으로 재실행한다.
주의: `main.py:81-84`가 보정 적합 시 `cf_profile`을 넘기지 않아 CF 채널이 조용히 빠진다. `eval_ckpt.py` 경로를 쓸 것.

보정 전후로 `A_off`가 `P`와 달라지는지, `A_on`이 `P + CF`와 달라지는지가 핵심이다.

### P3 — cfval_abl_noalign  (우선순위 낮음)

`manifests/manifest_noalign_server8.yaml`과 `configs/*_noalign.yaml`이 준비돼 있다(미실행).
`START_CLS_EPOCH=81`과 `ENABLE_PRIOR_LOSS=False`를 함께 적용한다. **81을 99999로 고쳐 쓸 것.**

P1 결과를 본 뒤에 하는 편이 낫다. 지금 설계는 퇴화 상태(PERM=0)에서 정렬 손실을 끄는 것이라 해석 범위가 좁다.

### P4 — 재현 checkpoint의 CF 계산 — **ks가 하지 않는다**

checkpoint가 js에 있다. js가 수행한다. ks는 결과 지표만 받는다.

## 5. 결과 게시

캠페인별로 `results/<campaign>/<server>` 브랜치에 publish한다. `scripts/publish_results.sh`를 쓴다.

**반드시 할 후처리가 있다.** `export_results.py:226`의 `df.to_csv`가 Redactor를 거치지 않아,
config을 checkout 밖에 두면 `metrics.csv`의 `config` 열에 절대경로가 남는다.
js는 `scripts/publish_redacted.sh`로 후처리했다. 그 스크립트를 ks 경로로 치환해 쓰거나 같은 방식을 구현한다.
**커밋 전에 누출 재스캔을 하고 0건이 아니면 커밋하지 않는다.**

push는 사람이 한다. 에이전트는 커밋까지만 하고 push 명령을 제시한다.

## 6. 최종 보고서

세 묶음을 합친다. ks 기존 결과, js 결과, ks 신규 결과.

    git fetch origin 'refs/heads/results/*:refs/remotes/origin/results/*'
    python scripts/export_results.py aggregate --campaign <name> --expected_seeds 0,1,2,3

`aggregate`는 `result_kind`가 섞이면 거부한다(`export_results.py:307`). 캠페인 단위로 따로 돌린다.

**보고서에 반드시 넣을 각주.**

- 학습 코드 SHA와 publishing 커밋은 다르다. `run_manifest.json`의 `training_code_sha`가 기준이다.
- **SMD entity 집합이 서버마다 다르다.** js는 machine-2-*/3-* 20개, ks는 machine-1-* 8개, 동료 프로토콜 재현은 28개 전부다.
  서로 직접 평균 비교가 불가능하다. 공통 entity로 제한하거나 집합을 명시한다.
- VUS는 window 의존이다. `USE_MEDIAN_VUS_WINDOW: True`라 entity마다 window가 다르다.
  서버 간·데이터셋 간 비교는 AUC-PR / AUC-ROC가 안전하다.
- PA-F1은 point-adjust라 신뢰도가 낮다. 주 지표로 쓰지 않는다.
- `LAM_GRAPHREG=0.05`는 정확히 0을 곱한다(graphreg 3항 전부 플래그 False). 기존 문서가 "graphreg 활성"이라고 서술한 것은 사실과 다르다.
- `SCORE_ALPHA`/`SCORE_BETA`는 죽어 있다. `S = C`이고 `main.py`의 `"S=C+G"`, `"A=P*S"` 출력은 틀린 라벨이다.
- `G`는 계산되지만 `A_off`/`A_on`에 들어가지 않는다. 그런데 단독 성능이 C의 2배 이상이다.

## 7. 보고 방식

- **"준비 완료"와 "학습 완료"를 구별해서 보고한다.** 준비만 된 것을 완료로 쓰지 않는다.
- 새 학습을 시작하기 전에 dry-run 결과를 보고하고 멈춰 승인을 받는다.
- 수치를 보고할 때 seed 수와 표준편차를 함께 쓴다. seed가 적을 때 조기 결과로 결론을 내지 않는다.
  (js에서 seed 1~2개 조기 결과가 4개를 모으자 뒤집힌 사례가 있다.)
- 실패·재시도·중단이 있으면 숨기지 않고 로그와 함께 보고한다.
- 추정치와 실측치를 구별해 표기한다.
