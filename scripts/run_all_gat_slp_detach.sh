#!/usr/bin/env bash
# Run cross-lag GAT + Same-Lag Prior (Option B / SLP) with stop-gradient patch
# applied to intervention alignment loss (Point 9 / detach variant).
# See intervention.py: pred_perm forward is wrapped in torch.no_grad() so that
# the MSE(cur, delta) is a one-way distillation (grad flows through cur only,
# not through delta). Prevents co-training leakage where the model reduces the
# loss by manipulating delta itself rather than aligning cur to delta.
#
# Env vars (all optional):
#   GPUS, SEEDS, EPOCHS, MAX_GPUS, FREE_MEM_THRESHOLD_MB, EXCLUDE_GPUS
#
# Usage:
#   bash scripts/run_all_gat_slp_detach.sh                             # foreground
#   nohup bash scripts/run_all_gat_slp_detach.sh > logs/run_all_gat_slp_detach.log 2>&1 &

set -u
SEEDS="${SEEDS:-0,1,2,3}"
EPOCHS="${EPOCHS:-80}"
DATE="$(date +%Y%m%d-%H%M%S)"

# Use the conda env python that has torch installed. The run_parallel.py
# launcher uses sys.executable to spawn main.py subprocesses, so this pins the
# whole chain to the correct interpreter regardless of the caller's shell env.
PYTHON="${PYTHON:-/home/sgshin/.conda/envs/sgshin/bin/python}"

cd "$(dirname "$0")/.."
mkdir -p logs

if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[run_all_gat_slp_detach] /'
fi

GPUS="${GPUS:-}"
if [ -z "${GPUS}" ]; then
    export MAX_GPUS="${MAX_GPUS:-4}"
    GPUS=$(bash scripts/detect_free_gpus.sh)
    if [ -z "${GPUS}" ]; then
        echo "[run_all_gat_slp_detach] no free GPU detected. Loosen threshold or set GPUS manually." >&2
        echo "[run_all_gat_slp_detach] current GPU status:" >&2
        /usr/bin/nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu \
                             --format=csv,noheader 2>&1 | sed 's/^/  /' >&2
        exit 1
    fi
fi
echo "[run_all_gat_slp_detach] using GPUs: ${GPUS}  (SEEDS=${SEEDS} EPOCHS=${EPOCHS})"

run_one() {
    local ds="$1"
    local tag="${ds,,}_detach"
    local out="results/parallel/${tag}_${DATE}"
    local log="logs/parallel_${tag}_${DATE}.log"
    echo "=============================================="
    echo "[$(date +'%F %T')] START ${ds} (detach)  -> ${out}"
    echo "  log: ${log}"
    echo "=============================================="
    "${PYTHON}" scripts/run_parallel.py \
        --dataset "${ds}" \
        --gpus "${GPUS}" \
        --seeds "${SEEDS}" \
        --epochs "${EPOCHS}" \
        --out_dir "${out}" \
        2>&1 | tee "${log}"
    local rc=${PIPESTATUS[0]}
    echo "[$(date +'%F %T')] END   ${ds} (detach)  exit=${rc}"
    return "${rc}"
}

run_one PSM_GAT_SLP  || echo "[warn] PSM_GAT_SLP (detach) finished with non-zero exit"
run_one SMD_GAT_SLP  || echo "[warn] SMD_GAT_SLP (detach) finished with non-zero exit"
run_one SWaT_GAT_SLP || echo "[warn] SWaT_GAT_SLP (detach) finished with non-zero exit"

echo
echo "[$(date +'%F %T')] ALL DONE (detach)."
echo "Result roots:"
ls -d results/parallel/*_gat_slp_detach_"${DATE}" 2>/dev/null
