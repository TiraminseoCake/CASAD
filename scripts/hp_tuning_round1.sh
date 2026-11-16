#!/bin/bash
# PSM HP Tuning - Round 1: LR sweep + L=20
# Baseline: LR=5e-5, L=10, D=64, LAM_CAUSAL=1.0 (already done)
# Each config: 2 seeds [0,1], ep100, ~4.5 hours per GPU

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/psm_hp_base.yaml
DATE=$(date +%Y%m%d_%H%M)

echo "=== Round 1 Start: $DATE ==="

# GPU0: LR=1e-4
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_lr1e-4 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 1e-4 \
    > results/hp_tuning/psm_lr1e-4.log 2>&1 &
echo "GPU0: LR=1e-4 (PID=$!)"

# GPU1: LR=5e-4
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_lr5e-4 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-4 \
    > results/hp_tuning/psm_lr5e-4.log 2>&1 &
echo "GPU1: LR=5e-4 (PID=$!)"

# GPU2: LR=1e-3
CUDA_VISIBLE_DEVICES=2 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_lr1e-3 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 1e-3 \
    > results/hp_tuning/psm_lr1e-3.log 2>&1 &
echo "GPU2: LR=1e-3 (PID=$!)"

# GPU3: L=20
CUDA_VISIBLE_DEVICES=3 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_L20 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.L 20 \
    > results/hp_tuning/psm_L20.log 2>&1 &
echo "GPU3: L=20 (PID=$!)"

echo "=== Round 1 Launched ==="
