#!/usr/bin/env bash
# Regularizer ablation on SWaT: baseline + 4 single-loss ablations x 4 seeds.
# SWaT is slower per epoch than PSM, so total wall-clock scales up accordingly.
#
# Usage:
#   nohup bash scripts/run_regab_swat.sh > logs/regab_swat_master.log 2>&1 &
set -u

cd "$(dirname "$0")/.."

# Manual-launch gate: this script is normally NOT called by run_regab_all.sh
# (that master pauses after SMD). To run SWaT, either invoke this script
# directly (which sets REGAB_ALLOW_SWAT=1 in the environment) or:
#   REGAB_ALLOW_SWAT=1 bash scripts/run_regab_swat.sh
if [ "${REGAB_ALLOW_SWAT:-0}" != "1" ] && [ -z "${REGAB_SWAT_MANUAL:-}" ]; then
    echo "[regab_swat] Gated: SWaT ablation held for manual review of SMD results."
    echo "[regab_swat] To run: REGAB_ALLOW_SWAT=1 bash scripts/run_regab_swat.sh"
    exit 0
fi

PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
CFG=scripts/configs/swat.yaml
DATE="$(date +%Y%m%d-%H%M%S)"
OUT_ROOT=results/parallel

if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[regab_swat] /'
fi
mkdir -p logs

# $1=gpu $2=out_tag $3=seed $4...=extra yacs overrides
launch_run() {
    local gpu="$1" tag="$2" seed="$3"; shift 3
    local out="${OUT_ROOT}/swat_regab_${tag}_${DATE}/SWaT/seed${seed}"
    local logf="logs/regab_swat_${tag}_s${seed}_gpu${gpu}.log"
    mkdir -p "$out"
    echo "[launch] GPU $gpu  ${tag} seed$seed  → $out"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" -u main.py \
        --cfg "$CFG" \
        SEEDS "[${seed}]" \
        DATA.ENTITIES swat \
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

echo "[$(date +'%F %T')] SWaT regularizer ablation START"

# Baseline is reused from results/parallel/swat_20260702-163856 (Option D:
# the intervention.py detach patch was reverted, so current code matches
# the code that produced that baseline). No in-tree baseline runs needed.

# ==== Ablation rounds: one seed per round, 4 ablations in parallel ====
for seed in 0 1 2 3; do
    launch_run 0 no_gate  "$seed" PICAAD.LOSS.W_GATE    0.0; P0=$!
    launch_run 1 no_graph "$seed" PICAAD.LOSS.W_GRAPH   0.0; P1=$!
    launch_run 2 no_lag   "$seed" PICAAD.LOSS.W_LAGMONO 0.0; P2=$!
    launch_run 3 no_inv   "$seed" PICAAD.LOSS.W_INV     0.0; P3=$!
    wait_all "ablation seed=$seed" $P0 $P1 $P2 $P3
done

# ==== no_all_4: all four auxiliary regularizers disabled simultaneously.
#      4 seeds x 1 config = 4 runs, spread across 4 GPUs in one round.
launch_run 0 no_all_4 0 \
    PICAAD.LOSS.W_GATE 0.0 PICAAD.LOSS.W_GRAPH 0.0 \
    PICAAD.LOSS.W_LAGMONO 0.0 PICAAD.LOSS.W_INV 0.0; P0=$!
launch_run 1 no_all_4 1 \
    PICAAD.LOSS.W_GATE 0.0 PICAAD.LOSS.W_GRAPH 0.0 \
    PICAAD.LOSS.W_LAGMONO 0.0 PICAAD.LOSS.W_INV 0.0; P1=$!
launch_run 2 no_all_4 2 \
    PICAAD.LOSS.W_GATE 0.0 PICAAD.LOSS.W_GRAPH 0.0 \
    PICAAD.LOSS.W_LAGMONO 0.0 PICAAD.LOSS.W_INV 0.0; P2=$!
launch_run 3 no_all_4 3 \
    PICAAD.LOSS.W_GATE 0.0 PICAAD.LOSS.W_GRAPH 0.0 \
    PICAAD.LOSS.W_LAGMONO 0.0 PICAAD.LOSS.W_INV 0.0; P3=$!
wait_all "no_all_4 seeds 0..3" $P0 $P1 $P2 $P3

echo "[$(date +'%F %T')] SWaT regularizer ablation DONE"
echo "Result roots:"
ls -d "${OUT_ROOT}"/swat_regab_*_"${DATE}" 2>/dev/null
