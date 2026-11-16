#!/bin/bash
# PSM HP Tuning - Round 3: LAM_CAUSAL sweep
# Run AFTER Round 2 finishes

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/psm_hp_base.yaml
DATE=$(date +%Y%m%d_%H%M)

echo "=== Round 3 Start: $DATE ==="

# GPU0: LAM_CAUSAL=0.1
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_lamC0.1 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.LAM_CAUSAL 0.1 \
    > results/hp_tuning/psm_lamC0.1.log 2>&1 &
echo "GPU0: LAM_CAUSAL=0.1 (PID=$!)"

# GPU1: LAM_CAUSAL=0.5
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_lamC0.5 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.LAM_CAUSAL 0.5 \
    > results/hp_tuning/psm_lamC0.5.log 2>&1 &
echo "GPU1: LAM_CAUSAL=0.5 (PID=$!)"

# GPU2: LAM_CAUSAL=2.0
CUDA_VISIBLE_DEVICES=2 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_lamC2.0 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.LAM_CAUSAL 2.0 \
    > results/hp_tuning/psm_lamC2.0.log 2>&1 &
echo "GPU2: LAM_CAUSAL=2.0 (PID=$!)"

# GPU3: free — can use for Tier 2 HP
# e.g., TAU_MAX=3
CUDA_VISIBLE_DEVICES=3 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_tau3 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.TAU_MAX 3 PICAAD.LAG_WIN 3 \
    > results/hp_tuning/psm_tau3.log 2>&1 &
echo "GPU3: TAU_MAX=3 (PID=$!)"

echo "=== Round 3 Launched ==="
