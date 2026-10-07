# 실행 전 반드시 읽을 함정 (js에서 실측으로 확인됨, CODE_SHA 49f630a)

아래 네 건은 모두 코드를 읽고 실행 로그·checkpoint로 검증한 사실이다. 모르고 돌리면 결과를 잘못 해석한다.

## 1. 데이터셋별 LR fallback이 YAML을 덮어쓴다

`utils/parser.py`의 `_DATASET_DEFAULT_LR = {'PSM': 5e-5, 'SMD': 5e-4, 'SWaT': 5e-4}`가
**CLI(`args.opts`)로 넘긴 키만** 사용자 지정으로 인정한다(`load_config`의 `cli_keys` 계산).
YAML에 적은 `SOLVER.BASE_LR`은 무시된다.

js 실측:

    YAML에 BASE_LR: 0.0001 이 적힌 psm_cf_val.yaml
      CLI 미지정        -> BASE_LR = 5e-05   (YAML 무시)
      CLI로 0.0001 명시 -> BASE_LR = 0.0001

SMD/SWaT는 YAML 값과 fallback이 같아 드러나지 않는다. **PSM만 노출된다.**
`scripts/run_experiments.py`는 경로 계열 opts만 붙이므로(`_common_path_opts`) manifest로 LR을 바꿀 수 없다.
PSM에서 5e-5가 아닌 LR을 쓰려면 launcher에 job별 opts 전달을 추가해야 한다(코드 변경).

js의 PSM 2x2는 전 조건 5e-5로 통일해 돌렸다.

## 2. CRS(cstruct) loss를 끄는 방법이 암묵적이다

`cstruct`에는 전용 ENABLE 플래그가 없다. 조건은 `ep >= PICAAD.START_CLS_EPOCH`뿐이다.
기존 nocstruct/noprior ablation은 `START_CLS_EPOCH=81`, `MAX_EPOCH=80`으로 껐다. 81 > 80이라 작동한다.

**`MAX_EPOCH`을 81 이상으로 올리면 조용히 다시 켜진다.**
새로 돌릴 때는 `START_CLS_EPOCH=99999`를 쓸 것. js의 PSM 2x2는 99999를 썼다.

## 3. PERM_PAIRS_PER_BATCH=0이면 cls_ref가 PCMCI prior로 퇴화한다

`set_te_prior`가 학습 전에 `cls_ref = normalize(te_prior_weight)`와 `has_cls_ref=True`를 설정한다.
`PERM_PAIRS_PER_BATCH=0`이면 개입 샘플이 없어 `cls_cnt`가 0이고, `_update_epoch_refs`의
`torch.where(cls_cnt>0, ..., fallback_cls)`가 항상 fallback을 택한다. 2 epoch 이후 fallback은
`cls_ref` 자신이므로 EMA가 `0.9*cls_ref + 0.1*cls_ref`로 고정점이 된다.

checkpoint 실측 `max|cls_ref - normalize(te_prior_weight)|`:

| 캠페인 | PERM_PAIRS | 차이 |
|---|---|---|
| cfval / nocstruct / noprior | 0 | 1.8e-07 (= 동일) |
| 동료 프로토콜 재현 | 2 | 0.73 ~ 1.00 |

**따라서 PERM=0에서의 CRS loss는 `ENABLE_PRIOR_LOSS`가 이미 하는 prior 정렬의 중복이다.**
기존 SWaT/SMD의 nocstruct 결론("CRS loss가 해롭다")은 이 퇴화 상태에만 적용된다.
js의 PSM 2x2가 보인 상호작용(PERM=2 + CRS on에서만 +0.112)이 그 근거다.

## 4. 죽은 설정 / 틀린 라벨

로그와 코드로 확인했다. 결과 해석에 영향이 있다.

- `LAM_GRAPHREG=0.05`는 **정확히 0을 곱한다.** graphreg 그룹의 gate/lagmono/graph 세 항이 전부 플래그 False다.
  로그에 `use_graph=True`가 ep3부터 찍히지만 `graph` 값은 80 epoch 전부 0이다(출력 플래그가 장식).
- `ENABLE_INV_LOSS=False`이므로 `inv`도 항상 0. `LAM_ROBUST=0.10`은 PERM=0이면 0을 곱한다.
- 실제 최적화되는 항은 PERM=0에서 `pred + tew + 0.5*teg` (+ `cstruct`) 셋 또는 넷뿐이다.
- `SCORE_ALPHA` / `SCORE_BETA`는 `apply_score_calibrator`에 인자로 전달되지만 본문에서 참조되지 않는다. **완전히 죽어 있다.**
- `S = C`다(C의 복사본). `main.py`가 출력하는 `"S=C+G"`와 `"A=P*S"`는 2026-09-07 커밋 792eb46 이전 수식의 잔재이고 **틀린 라벨**이다. 실제는 `A = P + C + gamma*CF`.
- `G`는 계산되지만 `A_off`/`A_on`에 들어가지 않는다. 따라서 `G_AGG`/`G_TOPK`/`GRAPH_LAG_AGG`는 보고 지표를 바꾸지 않는다.
- `C_AGG="fro"`는 Frobenius 노름이 아니라 N*N으로 나누는 RMS다(이름이 부정확).
- `P_TOPK`/`C_TOPK`/`G_TOPK`/`CALIB_CLIP_MIN`은 현재 설정에서 읽히지만 효과가 없다.

## 5. 스코어 채널의 척도 문제 (CALIBRATE=False)

모든 배포 config이 `SCORING.CALIBRATE: False`다. 보정 없이 원시값을 더한다.
C는 (tau*N)xN 단체 위 RMS로 O(1/(tau*N)), P는 O(0.1~1)이라 크기가 두 자릿수 다르다.

js 실측, 합성 스코어 판별폭(IQR) 점유율:

| dataset | P | C | CF |
|---|---|---|---|
| SWaT | 43.7% | **0.3%** | 56.0% |
| SMD | 19.2% | **1.6%** | 79.2% |

그 결과 `A_off = P + C`가 `P` 단독과 네 자리까지 같고, `A_on = P + C + CF`가 `P + CF`와 같다
(js에서 168 run 전수 확인, Spearman 0.99999, 지표 차 1e-4 미만).

**"C가 정보가 없다"가 아니라 "C가 가중될 기회를 못 받는다"가 정확하다.**
C 단독 AUC-PR은 SWaT 0.3504(무작위 기준선 0.1213)로 신호가 있다.
`CALIBRATE=True` 경로는 아직 한 번도 돌지 않았다.

## 6. export 도구의 누출

`scripts/export_results.py:226`의 `df.to_csv`는 Redactor를 거치지 않는다.
config 경로가 checkout 밖(bootstrap)에 있으면 `metrics.csv`의 `config` 열에 절대경로가 남는다.
js는 publish 후처리로 `<BOOTSTRAP>`/`<HOME>`으로 치환했다(`scripts/publish_redacted.sh` 참고).
ks도 config을 checkout 밖에 둘 경우 같은 후처리가 필요하다.
