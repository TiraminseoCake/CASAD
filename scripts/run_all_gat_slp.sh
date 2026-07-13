#!/usr/bin/env bash
# Run cross-lag GAT + Same-Lag Prior (Option B / SLP) on PSM -> SMD -> SWaT
# sequentially, parallel per dataset. This restores the per-τ within-lag
# prior that the original PICAAD per-lag MHSA had, on top of the cross-lag
# structure introduced in Option C.
#
# Baseline (MHSA)  and GAT (Option C) results should already exist under
# results/parallel/{psm,smd,swat}_* and *_gat_*  for comparison.
#
# Env vars (all optional):
#   GPUS, SEEDS, EPOCHS, MAX_GPUS, FREE_MEM_THRESHOLD_MB, EXCLUDE_GPUS
#
# Usage:
#   bash scripts/run_all_gat_slp.sh                             # foreground (tmux)
#   nohup bash scripts/run_all_gat_slp.sh > logs/run_all_gat_slp.log 2>&1 &

set -u
SEEDS="${SEEDS:-0,1,2,3}"
EPOCHS="${EPOCHS:-80}"
DATE="$(date +%Y%m%d-%H%M%S)"

cd "$(dirname "$0")/.."
mkdir -p logs

# Seed the on-disk PCMCI+ prior cache from priors shipped with the repo.
if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[run_all_gat_slp] /'
fi

# Auto-detect free GPUs if the caller did not explicitly set GPUS.
GPUS="${GPUS:-}"
if [ -z "${GPUS}" ]; then
    export MAX_GPUS="${MAX_GPUS:-4}"
    GPUS=$(bash scripts/detect_free_gpus.sh)
    if [ -z "${GPUS}" ]; then
        echo "[run_all_gat_slp] no free GPU detected. Loosen threshold or set GPUS manually." >&2
        echo "[run_all_gat_slp] current GPU status:" >&2
        /usr/bin/nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu \
                             --format=csv,noheader 2>&1 | sed 's/^/  /' >&2
        exit 1
    fi
fi
echo "[run_all_gat_slp] using GPUs: ${GPUS}  (SEEDS=${SEEDS} EPOCHS=${EPOCHS})"

run_one() {
    local ds="$1"          # PSM_GAT_SLP / SMD_GAT_SLP / SWaT_GAT_SLP
    local tag="${ds,,}"
    local out="results/parallel/${tag}_${DATE}"
    local log="logs/parallel_${tag}_${DATE}.log"
    echo "=============================================="
    echo "[$(date +'%F %T')] START ${ds}  -> ${out}"
    echo "  log: ${log}"
    echo "=============================================="
    python scripts/run_parallel.py \
        --dataset "${ds}" \
        --gpus "${GPUS}" \
        --seeds "${SEEDS}" \
        --epochs "${EPOCHS}" \
        --out_dir "${out}" \
        2>&1 | tee "${log}"
    local rc=${PIPESTATUS[0]}
    echo "[$(date +'%F %T')] END   ${ds}  exit=${rc}"
    return "${rc}"
}

run_one PSM_GAT_SLP  || echo "[warn] PSM_GAT_SLP finished with non-zero exit"
run_one SMD_GAT_SLP  || echo "[warn] SMD_GAT_SLP finished with non-zero exit"
run_one SWaT_GAT_SLP || echo "[warn] SWaT_GAT_SLP finished with non-zero exit"

echo
echo "[$(date +'%F %T')] ALL DONE."
echo "Result roots:"
ls -d results/parallel/*_gat_slp_"${DATE}" 2>/dev/null
