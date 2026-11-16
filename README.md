# PICAAD: Prior-guided Interventional Causal Attention for Anomaly Detection

PICAAD is a multivariate time-series anomaly detector. A PCMCI+ causal prior guides how a lagged
predictor routes information between variables. During training, small interventions measure how strongly
each lagged edge actually drives the prediction. These measured strengths accumulate into a
causal reference strength (CRS). At test time, the anomaly score combines the prediction error with the
deviation of the current edge strengths from the CRS.

This branch holds the **final model used in the paper**, every run script, the per-run result CSVs
(main comparison and ablations), and the paper's LaTeX sources.

---

## Final model

| Component | Setting |
|---|---|
| Causal prior | PCMCI+ (Tigramite, ParCorr, α = 0.05, τ_max = 5, ≤ 10k contiguous training steps), self-link floor 0.25 |
| Encoder | per-variable LSTM (2 layers, d = 64) + 4-head attention with a prior-masked bias (5 warm-up epochs) |
| Routing | Π = softmax(ψ + Δ(X) + β·log W̃ + log G). ψ is initialized as self-loop + 0.25·log W̃; β = 0.35; G = g·(0.05 + 0.95·M) |
| Loss | L = L_pred (L1) + λ_crs·KL(CRS ‖ E) (from epoch 5, λ_crs = 1) + λ_int·L_int (λ_int = 0.1) |
| Intervention | 2 source–lag pairs per batch. The CRS is updated once per epoch by EMA (0.9) |
| Score | A = P + C (raw prediction deviation + strength deviation from the CRS) |
| Training | AdamW (wd 0.01, clip 1.0), batch 512, 80 epochs, LR 5e-5 (PSM) / 5e-4 (SMD, SWaT) |
| Checkpoint | `best_smooth`: minimum of the 3-epoch moving average of validation prediction MAE, epoch ≥ 20 |

The prior-alignment loss is **off** in the final model (`PICAAD.ENABLE_PRIOR_LOSS False`). The code default is
still `True` so older scripts reproduce unchanged. `scripts/run_final.sh` sets the final options explicitly.

## Repository layout

```
main.py, trainer.py, config.py     entry point, training loop, yacs defaults
model/                              PICAAD model, priors (PCMCI+), interventions, losses, scoring
layers/, datasets/, utils/          encoder blocks, npz loaders / splits, evaluation
metrics/paper_eval/                 shared evaluator (F1, R-F1, Aff-F, AUC-ROC/PR, VUS-ROC/PR)
scripts/run_final.sh                final model, all datasets, seeds 0-3
scripts/run_psm_ablation_noalign.sh PSM component ablation (paper Table 3)
scripts/run_noalign_check.sh        prior-alignment off on SMD + SWaT_ds5
scripts/run_hb_protocol.sh          prior-alignment on (old base) on all datasets
scripts/eval_score_components.py    post-hoc P / C / P+C scoring of saved checkpoints
scripts/collect_paper_results.py    rebuilds results/paper_final from the run CSVs and checks the paper numbers
scripts/baselines/                  CAROTS data conversion and shared-evaluator rescoring
scripts/configs/                    yaml configs (ablation_{psm,smd,swat}.yaml are used by the final runs)
results/paper_final/                every number in the paper's Experiments section (see its README)
results/{ablation_hb,hb,...}/       per-run CSVs and configs (checkpoints and logs are not tracked)
docs/paper/full/                    paper LaTeX (main.tex, experiments_revised.tex, refs.bib)
```

## Setup

```bash
pip install -r requirements.txt   # tested: python 3.10, torch 2.5.1+cu121, tigramite 5.2.10.1
```

Datasets are not included. Put them under `data/` as npz files with `train`, `test`, and `label` arrays:

| Dataset | Path | Preparation |
|---|---|---|
| PSM | `data/PSM/PSM.npz` | `scripts/prep/prep_psm_to_npz.py` |
| SMD | `data/SMD/machine-*.npz` (28 files) | `scripts/prep/prep_smd_to_npz.py` |
| SWaT_ds5 | `data/SWaT_ds5/swat.npz` | SWaT (51 variables) with 5× non-overlapping median aggregation of observations and labels; trailing incomplete block dropped |

PCMCI+ priors are computed on first use and cached in `data/prior_cache/`. You can also precompute them with
`scripts/precompute_priors.py`.

## Reproduce

```bash
bash scripts/run_final.sh                 # PSM, SMD, SWaT_ds5 x seeds 0-3 -> results/final/
bash scripts/run_final.sh PSM             # one dataset
bash scripts/run_psm_ablation_noalign.sh  # PSM ablation
python scripts/collect_paper_results.py   # rebuild results/paper_final and verify against the paper
```

## Results

Seeds 0–3, mean (%). SMD is macro-averaged over 28 machines. All methods are scored with the same evaluator,
without point adjustment. CAROTS uses its official code. OracleAD uses a re-implementation that is not
included in this repository.

| Dataset | Method | F1 | R-F1 | Aff-F | A-ROC | A-PR | V-ROC | V-PR |
|---|---|---|---|---|---|---|---|---|
| PSM | CAROTS | 56.76 | 46.78 | 72.79 | 75.75 | 53.17 | 69.46 | 48.89 |
| PSM | OracleAD | 53.32 | 47.49 | 77.46 | 73.23 | 55.30 | 67.95 | 47.37 |
| PSM | **PICAAD** | 53.97 | 42.13 | 77.87 | 75.28 | **58.22** | **71.76** | **54.69** |
| SMD | CAROTS | 49.45 | 30.71 | 78.50 | 82.16 | 43.54 | 83.85 | 38.87 |
| SMD | OracleAD | 50.16 | 37.80 | 84.70 | 83.82 | 46.49 | 85.16 | 41.87 |
| SMD | **PICAAD** | 48.13 | **40.37** | **86.12** | 81.96 | 43.92 | 84.24 | 41.71 |
| SWaT_ds5 | CAROTS | 79.63 | 34.47 | 80.19 | 85.36 | 75.90 | 79.18 | 65.74 |
| SWaT_ds5 | OracleAD | 75.83 | 22.83 | 75.25 | 84.53 | 74.65 | 74.06 | 57.13 |
| SWaT_ds5 | **PICAAD** | 76.03 | 21.35 | 74.20 | 84.01 | 74.02 | 74.50 | 56.74 |

### PSM ablation

Δ is the paired difference from Full in percentage points. Parentheses give the number of seeds (out of 4) that fell below Full.

| Variant | A-PR | V-PR | ΔA-PR | ΔV-PR |
|---|---|---|---|---|
| PICAAD (Full) | **58.22** | **54.69** | – | – |
| w/o Prior | 47.43 | 45.53 | −10.79 (4/4) | −9.16 (4/4) |
| w/o Δ | 46.12 | 44.33 | −12.09 (4/4) | −10.36 (4/4) |
| w/o CRS loss | 44.11 | 42.79 | −14.11 (4/4) | −11.90 (4/4) |
| w/o Intervention | 44.13 | 42.69 | −14.08 (4/4) | −12.00 (4/4) |
| w/o CRS update | 44.32 | 42.98 | −13.90 (4/4) | −11.72 (4/4) |
| w/o L_int | 54.26 | 50.26 | −3.96 (4/4) | −4.43 (4/4) |
| + prior-alignment loss | 53.94 | 51.20 | −4.28 (3/4) | −3.49 (3/4) |

`results/paper_final/` also contains:
- the prior-alignment on/off comparison on all three datasets,
- persistent bias vs. folded routing on PSM over 8 seeds (the folded variant's code lives on the `exp/folded-routing` branch),
- the post-hoc P / C / P+C score composition.

Each table comes with its per-run CSVs.
