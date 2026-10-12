# ks → js 인계: P0 최종 (2026-10-12)

| 파일 | 내용 |
|---|---|
| `KS_P0_FINAL_REPORT.md` | SWaT 진행 상태, SMD 28 entity CRS×PERM 통합 분석, 무결성 점검, PSM과의 차이, 게시 내역, 미확인 항목·필요 승인 |
| `smd28_crs_perm_paired.csv` | (entity, seed)별 4개 조건 값과 효과(a00/a01/a10/a11, CRS@PERM0, CRS@PERM2, 상호작용, 주효과). `P_raw`의 9개 지표와 best_val 예측 MAE. 각 조건의 best epoch 포함 |
| `smd28_entity_effects.csv` | entity별 4-seed 평균·sd(ddof=1), seed 부호 개수 |
| `smd28_uncertainty.csv` | 범위별(SMD28 / SMD8·SMD20 참고 / PSM 참고) 추정치, seed macro 4개와 평균·sd, entity 분포, entity cluster bootstrap(B=10000, seed 20261012) SE·95% CI, t 검정(보조·참고) |
| `coverage_and_provenance.json` | 캠페인 상태 스냅샷, 448 run 커버리지, 무결성 점검 결과, 참조 입력(js PSM 패키지, data-identity)의 commit·sha256, 게시 branch·commit, 알려진 한계 |
| `P3_STRUCTURAL_ABLATION_PLAN.md` | 다음 구조 대조 실험 설계(PCMCI+ / no-prior / 구조 맞춘 random prior / δ 제거). 구현·학습은 하지 않았다 |
| `supporting/smd28_runs.csv` | 분석 입력. 448 run × (무결성 필드 + 6 variant × 9 지표). run별 원본 파일에서 직접 수집했다 |
| `scripts/collect_smd28.py`, `scripts/analyze_smd28.py` | 수집·분석 스크립트. 경로는 인자로 받는다 |

## ks 결과 패키지 (각각 별도 branch)

| branch | commit |
|---|---|
| `results/cfval_abl_smdcrs/ks` | `94050082bc990b9ba8b7310da8bb646f5623ed97` |
| `results/cfval_abl_smdcrs20/ks` | `8b15ea7e7830e0b601ad9e3b24b2e452d5e605bd` |
| `results/cfval_abl_noalign/ks` | `04e66ebfd60b85227a871839043e026f5ca2631b` |
| `results/sp2x2/ks` | `097ad24cfc341b6de2a4f500afb07ff43b75f30e` |

받기: `git fetch origin 'refs/heads/results/*:refs/remotes/origin/results/*'`

- 게시 wrapper는 ks의 `<BOOTSTRAP>/ks/publish_redacted_ks.sh`(sha256 `a7beefc24efd663375f095e9562c1d285031556e40726583558f69687e97e432`)에 있다. js `publish_redacted.sh`의 ks판이다. 이 묶음에는 넣지 않았다. 스크립트 안의 비밀 패턴 정규식 문자열이 누출 스캐너에 걸리기 때문이다. 절차는 `KS_P0_FINAL_REPORT.md` §5에 적었다.

## 재현

```bash
python scripts/collect_smd28.py --runs_root <RUNS> --data_root <DATA_ROOT> \
    --ref_hashes <results/data-identity>/reports/data_identity/cfval_smd28_swat51_reference_hashes.json \
    --exec_repo <execution checkout at 49f630a> --out_dir <work>
python scripts/analyze_smd28.py --runs_csv <work>/smd28_runs.csv \
    --psm_metrics <results/cfval_abl_psmcrs/server8>/reports/experiments/cfval_abl_psmcrs/server8/cfval_abl_psmcrs_server8/metrics.csv \
    --out_dir <out> --boot 10000 --boot_seed 20261012
```

- `collect_smd28.py`는 checkpoint 원본이 있는 ks에서만 전부 실행된다. `--skip_ckpt`를 주면 checkpoint 해시와 `cls_ref` 검사를 건너뛴다.
- 게시된 패키지만으로 확인하려면 다음을 대조하면 된다. smdcrs/smdcrs20 `metrics.csv`의 best_val 행이 `supporting/smd28_runs.csv`와 같다(ks에서 대조한 결과 24,192개 값 모두 일치).
