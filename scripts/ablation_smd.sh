#!/bin/bash
# SMD Ablation Study — ep100, 4 seeds
# Full + 6 ablations = 7 configs on 4 GPUs = 2 rounds

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_smd.yaml
OUTDIR=results/ablation

mkdir -p $OUTDIR

echo "=== SMD Ablation Round 1: $(date) ==="

# GPU0: Full baseline
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/smd_full RESULT_DIR_LITERAL True \
    > ${OUTDIR}/smd_full.log 2>&1 &
echo "GPU0: Full (PID=$!)"

# GPU1: w/o Prior
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/smd_no_prior RESULT_DIR_LITERAL True \
    PICAAD.PRIOR.TYPE none \
    PICAAD.CAUSAL_ATTN_MASK_SCALE 0.0 \
    PICAAD.LAM_CAUSAL 0.0 \
    > ${OUTDIR}/smd_no_prior.log 2>&1 &
echo "GPU1: w/o Prior (PID=$!)"

# GPU2: w/o Causal Attention
CUDA_VISIBLE_DEVICES=2 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/smd_no_cattn RESULT_DIR_LITERAL True \
    PICAAD.CAUSAL_ATTN_MASK_SCALE 0.0 \
    > ${OUTDIR}/smd_no_cattn.log 2>&1 &
echo "GPU2: w/o Causal Attn (PID=$!)"

# GPU3: w/o CRS Loss
CUDA_VISIBLE_DEVICES=3 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/smd_no_crsloss RESULT_DIR_LITERAL True \
    PICAAD.LAM_CAUSAL 0.0 \
    > ${OUTDIR}/smd_no_crsloss.log 2>&1 &
echo "GPU3: w/o CRS Loss (PID=$!)"

echo "=== Round 1 Launched ==="
