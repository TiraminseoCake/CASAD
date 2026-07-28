#!/usr/bin/env bash
# Retrain-ablation (Approach B, minimal):
#   PSM baseline × 4 routing-input ablations × 2 seeds = 8 training runs.
#
# For each ablation, we retrain from scratch with one routing input disabled
# BOTH at initialization and at forward time (see model/modeling_picaad.py
# for the disable_* logic). Comparing these against the original PSM baseline
# tells us whether the model can compensate for the missing input during
# training — a signal that post-hoc ablation cannot provide.
#
# Layout: 4 GPUs, 2 rounds. Each round launches 4 (ablation, seed) jobs.
#
# Usage:
#   nohup bash scripts/run_retrain_ablate.sh > logs/retrain_ablate_master.log 2>&1 &

set -u

cd "$(dirname "$0")/.."

PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
CFG=scripts/configs/psm.yaml
DATE="$(date +%Y%m%d-%H%M%S)"
OUT_ROOT=results/parallel

# Seed the on-disk PCMCI+ prior cache from priors shipped with the repo.
if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[retrain_ablate] /'
fi

mkdir -p logs

launch_run() {
    # $1=gpu $2=ablation_flag $3=out_tag $4=seed
    local gpu="$1" flag="$2" tag="$3" seed="$4"
    local out="${OUT_ROOT}/psm_retrain_${tag}_${DATE}/PSM/seed${seed}"
    local logf="logs/retrain_ablate_${tag}_s${seed}_gpu${gpu}.log"
    mkdir -p "$out"
    echo "[launch] GPU $gpu  ${tag} seed$seed  → $out"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" -u main.py \
        --cfg "$CFG" \
        SEEDS "[${seed}]" \
        DATA.ENTITIES PSM \
        RESULT_DIR "$out" \
        RESULT_DIR_LITERAL True \
        SOLVER.MAX_EPOCH 80 \
        PICAAD.ROUTING."$flag" True \
        > "$logf" 2>&1 &
}

wait_all() {
    local name="$1"; shift
    local pids=("$@")
    echo "[wait] $name  pids=${pids[*]}"
    for pid in "${pids[@]}"; do
        wait "$pid"
        echo "[done] pid=$pid  status=$?"
    done
}

echo "[$(date +'%F %T')] retrain-ablate START"

# ==== Round 1: seed 0 of each ablation ====
launch_run 0 DISABLE_PHI    no_phi    0; P0=$!
launch_run 1 DISABLE_W      no_W      0; P1=$!
launch_run 2 DISABLE_M      no_M      0; P2=$!
launch_run 3 DISABLE_MLEARN no_Mlearn 0; P3=$!
wait_all "Round 1 (seed 0)" $P0 $P1 $P2 $P3

# ==== Round 2: seed 1 of each ablation ====
launch_run 0 DISABLE_PHI    no_phi    1; P0=$!
launch_run 1 DISABLE_W      no_W      1; P1=$!
launch_run 2 DISABLE_M      no_M      1; P2=$!
launch_run 3 DISABLE_MLEARN no_Mlearn 1; P3=$!
wait_all "Round 2 (seed 1)" $P0 $P1 $P2 $P3

echo "[$(date +'%F %T')] ALL RETRAIN-ABLATE DONE"
echo "Result roots:"
ls -d results/parallel/psm_retrain_*_"${DATE}" 2>/dev/null
