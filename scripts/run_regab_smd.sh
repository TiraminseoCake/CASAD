#!/usr/bin/env bash
# Regularizer ablation on SMD (all 28 entities, 4 seeds each):
#   baseline + 4 single-loss ablations, 4-way entity partitioning per config.
#
# Per config (baseline / no_gate / no_graph / no_lag / no_inv): 4 GPU × 7
# entities each × 4 seeds. Configs run sequentially; entities+seeds within a
# config run in parallel across 4 GPUs.
#
# Usage:
#   nohup bash scripts/run_regab_smd.sh > logs/regab_smd_master.log 2>&1 &
set -u

cd "$(dirname "$0")/.."

PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
CFG=scripts/configs/smd.yaml
DATE="$(date +%Y%m%d-%H%M%S)"
OUT_ROOT=results/parallel

if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[regab_smd] /'
fi
mkdir -p logs

SMD_1="machine-1-1,machine-1-2,machine-1-3,machine-1-4,machine-1-5,machine-1-6,machine-1-7"
SMD_2="machine-1-8,machine-2-1,machine-2-2,machine-2-3,machine-2-4,machine-2-5,machine-2-6"
SMD_3="machine-2-7,machine-2-8,machine-2-9,machine-3-1,machine-3-2,machine-3-3,machine-3-4"
SMD_4="machine-3-5,machine-3-6,machine-3-7,machine-3-8,machine-3-9,machine-3-10,machine-3-11"

# $1=gpu $2=out_tag $3=entities $4...=extra yacs overrides
launch_partition() {
    local gpu="$1" tag="$2" ents="$3"; shift 3
    local out="${OUT_ROOT}/smd_regab_${tag}_${DATE}"
    local logf="logs/regab_smd_${tag}_gpu${gpu}.log"
    mkdir -p "$out"
    local n_ents=$(echo "$ents" | awk -F',' '{print NF}')
    echo "[launch] GPU $gpu  ${tag}  entities=$n_ents"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" -u main.py \
        --cfg "$CFG" \
        SEEDS "[0,1,2,3]" \
        DATA.ENTITIES "$ents" \
        RESULT_DIR "$out" \
        RESULT_DIR_LITERAL True \
        SOLVER.MAX_EPOCH 80 \
        "$@" \
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

run_config() {
    # Launches one full config across 4 GPUs (7+7+7+7 entities, all seeds).
    local tag="$1"; shift
    launch_partition 0 "$tag" "$SMD_1" "$@"; P0=$!
    launch_partition 1 "$tag" "$SMD_2" "$@"; P1=$!
    launch_partition 2 "$tag" "$SMD_3" "$@"; P2=$!
    launch_partition 3 "$tag" "$SMD_4" "$@"; P3=$!
    wait_all "SMD config $tag" $P0 $P1 $P2 $P3
}

echo "[$(date +'%F %T')] SMD regularizer ablation START"

# Baseline is reused from results/parallel/smd_20260702-163856 (Option D:
# the intervention.py detach patch was reverted, so current code matches
# the code that produced that baseline). No in-tree baseline runs needed.
run_config no_gate  PICAAD.LOSS.W_GATE    0.0
run_config no_graph PICAAD.LOSS.W_GRAPH   0.0
run_config no_lag   PICAAD.LOSS.W_LAGMONO 0.0
run_config no_inv   PICAAD.LOSS.W_INV     0.0
# All four auxiliary regularizers disabled simultaneously — final validation
# that PICAAD's core losses (L_pred + L_prior + L_crs + L_int) suffice.
run_config no_all_4 \
    PICAAD.LOSS.W_GATE    0.0 \
    PICAAD.LOSS.W_GRAPH   0.0 \
    PICAAD.LOSS.W_LAGMONO 0.0 \
    PICAAD.LOSS.W_INV     0.0

echo "[$(date +'%F %T')] SMD regularizer ablation DONE"
echo "Result roots:"
ls -d "${OUT_ROOT}"/smd_regab_*_"${DATE}" 2>/dev/null
