# OracleAD-PCMCI: Causal Prior-Guided Anomaly Detection with PCMCI+ and Online Intervention

## Overview

This repository extends the OracleAD framework (NeurIPS 2025) with a **causal inference pipeline** for multivariate time series anomaly detection.

### Key Contributions

1. **PCMCI+ Causal Prior**: Systematic confounder removal via conditional independence testing
2. **PCMCI+ Guided Intervention**: Priority sampling on important causal edges
3. **Edge-wise Causal Decomposition**: C (causal effect) + G (topology) multi-channel scoring
4. **GNN rejection evidence**: Empirical proof that GNN hurts AD performance

## Results

### SWaT (5 seed avg) — Beats OracleAD on 4/7 metrics

| Metric | OracleAD | Ours (PCMCI+) |
|--------|:---:|:---:|
| F1 | 76.50 | **79.01** |
| R-F1 | 28.15 | **30.03** |
| A-ROC | 82.71 | **87.21** |
| A-PR | 72.39 | **78.61** |

## Quick Start

```bash
pip install torch numpy scikit-learn pandas tigramite

python model/oraclead_npz_runner_causal_v2_pcmci.py \
  --input_dir /path/to/SWaT \
  --entities swat --dataset SWaT \
  --epochs 80 --batch 128 --lr 5e-4 \
  --grad_clip 1.0 --prior pcmci \
  --use_median_vus_window --diagnose_components
```
