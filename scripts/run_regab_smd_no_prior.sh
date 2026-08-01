#!/usr/bin/env bash
# SMD core-loss ablation: L_prior disabled (W_PRIOR=0).
# 28 entities x 4 seeds via 4-way partitioning across GPUs.
set -u
cd "$(dirname "$0")/.."

PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
CFG=scripts/configs/smd.yaml
DATE="$(date +%Y%m%d-%H%M%S)"
OUT_ROOT=results/parallel
mkdir -p logs

SMD_1="machine-1-1,machine-1-2,machine-1-3,machine-1-4,machine-1-5,machine-1-6,machine-1-7"
SMD_2="machine-1-8,machine-2-1,machine-2-2,machine-2-3,machine-2-4,machine-2-5,machine-2-6"
SMD_3="machine-2-7,machine-2-8,machine-2-9,machine-3-1,machine-3-2,machine-3-3,machine-3-4"
SMD_4="machine-3-5,machine-3-6,machine-3-7,machine-3-8,machine-3-9,machine-3-10,machine-3-11"

launch_partition() {
    local gpu="$1" ents="$2"
    local out="${OUT_ROOT}/smd_regab_no_prior_${DATE}"
    local logf="logs/regab_smd_no_prior_gpu${gpu}.log"
    mkdir -p "$out"
    echo "[launch] GPU $gpu  no_prior  entities=$(echo "$ents" | awk -F',' '{print NF}')"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" -u main.py \
        --cfg "$CFG" \
        SEEDS "[0,1,2,3]" \
        DATA.ENTITIES "$ents" \
        RESULT_DIR "$out" \
        RESULT_DIR_LITERAL True \
        SOLVER.MAX_EPOCH 80 \
        PICAAD.LOSS.W_PRIOR 0.0 \
        > "$logf" 2>&1 &
}

echo "[$(date +'%F %T')] SMD no_prior START"
launch_partition 0 "$SMD_1"; P0=$!
launch_partition 1 "$SMD_2"; P1=$!
launch_partition 2 "$SMD_3"; P2=$!
launch_partition 3 "$SMD_4"; P3=$!
echo "[wait] pids=$P0 $P1 $P2 $P3"
for pid in $P0 $P1 $P2 $P3; do wait "$pid"; echo "[done] pid=$pid status=$?"; done
echo "[$(date +'%F %T')] SMD no_prior DONE"
