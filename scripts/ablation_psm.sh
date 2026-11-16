#!/bin/bash
# PSM Ablation Study — ep100, 4 seeds, default HP
# Full baseline already done (results/parallel/psm_no_earlystop_ep100_seed{0-3})
# 6 ablation configs on 4 GPUs = 2 rounds

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_psm.yaml
OUTDIR=results/ablation

mkdir -p $OUTDIR

echo "=== PSM Ablation Round 1: $(date) ==="

# GPU0: w/o Prior (complete removal)
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/psm_no_prior RESULT_DIR_LITERAL True \
    PICAAD.PRIOR.TYPE none \
    PICAAD.CAUSAL_ATTN_MASK_SCALE 0.0 \
    PICAAD.LAM_CAUSAL 0.0 \
    > ${OUTDIR}/psm_no_prior.log 2>&1 &
echo "GPU0: w/o Prior (PID=$!)"

# GPU1: w/o Causal Attention
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/psm_no_cattn RESULT_DIR_LITERAL True \
    PICAAD.CAUSAL_ATTN_MASK_SCALE 0.0 \
    > ${OUTDIR}/psm_no_cattn.log 2>&1 &
echo "GPU1: w/o Causal Attn (PID=$!)"

# GPU2: w/o CRS Loss (all causal regularization)
CUDA_VISIBLE_DEVICES=2 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/psm_no_crsloss RESULT_DIR_LITERAL True \
    PICAAD.LAM_CAUSAL 0.0 \
    > ${OUTDIR}/psm_no_crsloss.log 2>&1 &
echo "GPU2: w/o CRS Loss (PID=$!)"

# GPU3: w/o Dynamic Graph
CUDA_VISIBLE_DEVICES=3 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/psm_no_dyngraph RESULT_DIR_LITERAL True \
    PICAAD.DYNAMIC_GRAPH False \
    > ${OUTDIR}/psm_no_dyngraph.log 2>&1 &
echo "GPU3: w/o Dynamic Graph (PID=$!)"

echo "=== Round 1 Launched (4 configs). Wait for completion before Round 2. ==="
echo "Run 'scripts/ablation_psm_r2.sh' after these finish."
