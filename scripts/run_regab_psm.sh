#!/usr/bin/env bash
# Regularizer ablation on PSM: baseline + 4 single-loss ablations x 4 seeds.
#   ablations: W_GATE=0, W_GRAPH=0, W_LAGMONO=0, W_INV=0
#   goal: identify which auxiliary regularizers can be removed without loss.
#
# Layout: 4 GPUs, 5 groups (baseline + 4 ablations) x 4 seeds. We interleave
# by seed so each round exercises all 4 GPUs on the same ablation slice.
#
# Usage:
#   nohup bash scripts/run_regab_psm.sh > logs/regab_psm_master.log 2>&1 &
set -u

cd "$(dirname "$0")/.."

# Manual-launch gate. To run:  REGAB_ALLOW_PSM=1 bash scripts/run_regab_psm.sh
if [ "${REGAB_ALLOW_PSM:-0}" != "1" ] && [ -z "${REGAB_PSM_MANUAL:-}" ]; then
    echo "[regab_psm] Gated: PSM ablation held for manual review."
    echo "[regab_psm] To run: REGAB_ALLOW_PSM=1 bash scripts/run_regab_psm.sh"
    exit 0
fi

PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
CFG=scripts/configs/psm.yaml
DATE="$(date +%Y%m%d-%H%M%S)"
OUT_ROOT=results/parallel

if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[regab_psm] /'
fi
mkdir -p logs

# $1=gpu $2=out_tag $3=seed $4...=extra yacs overrides
launch_run() {
    local gpu="$1" tag="$2" seed="$3"; shift 3
    local out="${OUT_ROOT}/psm_regab_${tag}_${DATE}/PSM/seed${seed}"
    local logf="logs/regab_psm_${tag}_s${seed}_gpu${gpu}.log"
    mkdir -p "$out"
    echo "[launch] GPU $gpu  ${tag} seed$seed  → $out"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" -u main.py \
        --cfg "$CFG" \
        SEEDS "[${seed}]" \
        DATA.ENTITIES PSM \
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

echo "[$(date +'%F %T')] PSM regularizer ablation START"

# Baseline is reused from results/parallel/psm_20260701-221416 (Option D:
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

echo "[$(date +'%F %T')] PSM regularizer ablation DONE"
echo "Result roots:"
ls -d "${OUT_ROOT}"/psm_regab_*_"${DATE}" 2>/dev/null
