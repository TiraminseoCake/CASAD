#!/bin/bash
# SWaT Ablation Study — Round 2
# Run AFTER Round 1 finishes

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_swat.yaml
OUTDIR=results/ablation

echo "=== SWaT Ablation Round 2: $(date) ==="

# GPU0: w/o Dynamic Graph
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/swat_no_dyngraph RESULT_DIR_LITERAL True \
    PICAAD.DYNAMIC_GRAPH False \
    > ${OUTDIR}/swat_no_dyngraph.log 2>&1 &
echo "GPU0: w/o Dynamic Graph (PID=$!)"

# GPU1: w/o Intervention
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/swat_no_interv RESULT_DIR_LITERAL True \
    PICAAD.LAM_ROBUST 0.0 \
    PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH 0 \
    > ${OUTDIR}/swat_no_interv.log 2>&1 &
echo "GPU1: w/o Intervention (PID=$!)"

echo "=== Round 2 Launched ==="
