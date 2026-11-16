#!/bin/bash
# PSM HP Tuning - Round 2: L sweep continued + D sweep
# Run AFTER Round 1 finishes

set -e
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/psm_hp_base.yaml
DATE=$(date +%Y%m%d_%H%M)

echo "=== Round 2 Start: $DATE ==="

# GPU0: L=50
CUDA_VISIBLE_DEVICES=0 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_L50 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.L 50 \
    > results/hp_tuning/psm_L50.log 2>&1 &
echo "GPU0: L=50 (PID=$!)"

# GPU1: L=100
CUDA_VISIBLE_DEVICES=1 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_L100 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.L 100 \
    > results/hp_tuning/psm_L100.log 2>&1 &
echo "GPU1: L=100 (PID=$!)"

# GPU2: D=32
CUDA_VISIBLE_DEVICES=2 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_D32 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.D 32 \
    > results/hp_tuning/psm_D32.log 2>&1 &
echo "GPU2: D=32 (PID=$!)"

# GPU3: D=128
CUDA_VISIBLE_DEVICES=3 nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR results/hp_tuning/psm_D128 RESULT_DIR_LITERAL True \
    SOLVER.BASE_LR 5e-5 \
    PICAAD.D 128 \
    > results/hp_tuning/psm_D128.log 2>&1 &
echo "GPU3: D=128 (PID=$!)"

echo "=== Round 2 Launched ==="
