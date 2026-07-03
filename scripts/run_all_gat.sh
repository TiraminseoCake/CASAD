#!/usr/bin/env bash
# Run cross-lag GAT variant (Option C) on PSM -> SMD -> SWaT sequentially,
# parallel per dataset. Baseline (MHSA) results should already exist under
# results/parallel/psm_*, smd_*, swat_* for comparison.
#
# By default this auto-detects free GPUs via scripts/detect_free_gpus.sh
# (skips GPUs currently used by *other* users' compute processes). Set the
# GPUS env var to override.
#
# Env vars (all optional):
#   GPUS                    "0,1,2,3" — explicit GPU list; empty = auto-detect
#   SEEDS                   default "0,1,2,3"
#   EPOCHS                  default 80
#   MAX_GPUS                cap auto-detected count (default 4)
#   FREE_MEM_THRESHOLD_MB   min free memory to consider (default 40000)
#   EXCLUDE_GPUS            never use these indices, comma-separated
#
# Usage:
#   bash scripts/run_all_gat.sh                             # foreground (tmux)
#   GPUS=4,5 bash scripts/run_all_gat.sh                    # force these GPUs
#   MAX_GPUS=8 bash scripts/run_all_gat.sh                  # use up to 8 free GPUs
#   EXCLUDE_GPUS=0,7 bash scripts/run_all_gat.sh            # skip these
#   nohup bash scripts/run_all_gat.sh > logs/run_all_gat.log 2>&1 &
#
# Each dataset writes to results/parallel/{dataset}_gat_{DATE}/ and produces
# summary_all_epochs.csv + summary_best_epoch.csv on completion.

set -u
SEEDS="${SEEDS:-0,1,2,3}"
EPOCHS="${EPOCHS:-80}"
DATE="$(date +%Y%m%d-%H%M%S)"

cd "$(dirname "$0")/.."
mkdir -p logs

# Seed the on-disk PCMCI+ prior cache from priors shipped with the repo
# (skips CPU-heavy recomputation per entity). No-op if already populated.
if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[run_all_gat] /'
fi

# Auto-detect free GPUs if the caller did not explicitly set GPUS.
GPUS="${GPUS:-}"
if [ -z "${GPUS}" ]; then
    export MAX_GPUS="${MAX_GPUS:-4}"
    GPUS=$(bash scripts/detect_free_gpus.sh)
    if [ -z "${GPUS}" ]; then
        echo "[run_all_gat] no free GPU detected. Loosen threshold or set GPUS manually." >&2
        echo "[run_all_gat] current GPU status:" >&2
        /usr/bin/nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu \
                             --format=csv,noheader 2>&1 | sed 's/^/  /' >&2
        exit 1
    fi
fi
echo "[run_all_gat] using GPUs: ${GPUS}  (SEEDS=${SEEDS} EPOCHS=${EPOCHS})"

run_one() {
    local ds="$1"          # PSM_GAT / SMD_GAT / SWaT_GAT
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

run_one PSM_GAT  || echo "[warn] PSM_GAT finished with non-zero exit"
run_one SMD_GAT  || echo "[warn] SMD_GAT finished with non-zero exit"
run_one SWaT_GAT || echo "[warn] SWaT_GAT finished with non-zero exit"

echo
echo "[$(date +'%F %T')] ALL DONE."
echo "Result roots:"
ls -d results/parallel/*_gat_"${DATE}" 2>/dev/null
