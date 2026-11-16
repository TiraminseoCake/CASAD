#!/bin/bash
# PSM Ablation Study — Round 2
# Run AFTER Round 1 finishes

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_psm.yaml
OUTDIR=results/ablation

echo "=== PSM Ablation Round 2: $(date) ==="

# GPU0: w/o Intervention (permutation robustness)
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/psm_no_interv RESULT_DIR_LITERAL True \
    PICAAD.LAM_ROBUST 0.0 \
    PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH 0 \
    > ${OUTDIR}/psm_no_interv.log 2>&1 &
echo "GPU0: w/o Intervention (PID=$!)"

# GPU1: Full baseline (for fair comparison, same config)
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR ${OUTDIR}/psm_full RESULT_DIR_LITERAL True \
    > ${OUTDIR}/psm_full.log 2>&1 &
echo "GPU1: Full baseline (PID=$!)"

echo "=== Round 2 Launched (2 configs) ==="
