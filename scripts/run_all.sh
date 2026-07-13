#!/usr/bin/env bash
# Run PSM -> SMD -> SWaT sequentially, parallel per dataset.
#
# Auto-detects free GPUs via scripts/detect_free_gpus.sh unless GPUS is set.
# See detect_free_gpus.sh for the exact "free" definition (no other user's
# compute processes + free memory >= FREE_MEM_THRESHOLD_MB).
#
# Env vars (all optional):
#   GPUS, SEEDS, EPOCHS, MAX_GPUS, FREE_MEM_THRESHOLD_MB, EXCLUDE_GPUS
#
# Usage:
#   bash scripts/run_all.sh                             # foreground (tmux)
#   GPUS=4,5 bash scripts/run_all.sh                    # force these GPUs
#   MAX_GPUS=8 bash scripts/run_all.sh                  # use up to 8 free GPUs
#   nohup bash scripts/run_all.sh > logs/run_all.log 2>&1 &

set -u
SEEDS="${SEEDS:-0,1,2,3}"
EPOCHS="${EPOCHS:-80}"
DATE="$(date +%Y%m%d-%H%M%S)"

# Change to repo root regardless of where the script is invoked from
cd "$(dirname "$0")/.."
mkdir -p logs

# Seed the on-disk PCMCI+ prior cache from priors shipped with the repo
# (skips CPU-heavy recomputation per entity). No-op if already populated.
if [ -d pretrained_priors ]; then
    bash scripts/setup_prior_cache.sh 2>&1 | sed 's/^/[run_all] /'
fi

# Auto-detect free GPUs if the caller did not explicitly set GPUS.
GPUS="${GPUS:-}"
if [ -z "${GPUS}" ]; then
    export MAX_GPUS="${MAX_GPUS:-4}"
    GPUS=$(bash scripts/detect_free_gpus.sh)
    if [ -z "${GPUS}" ]; then
        echo "[run_all] no free GPU detected. Loosen threshold or set GPUS manually." >&2
        exit 1
    fi
fi
echo "[run_all] using GPUs: ${GPUS}  (SEEDS=${SEEDS} EPOCHS=${EPOCHS})"

run_one() {
    local ds="$1"
    local out="results/parallel/${ds,,}_${DATE}"    # lowercase dataset name
    local log="logs/parallel_${ds,,}_${DATE}.log"
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

# Run in the order the user asked. Each dataset is independent; a failure in
# one does NOT block the next (so an SMD hiccup at 3am doesn't skip SWaT).
run_one PSM  || echo "[warn] PSM finished with non-zero exit"
run_one SMD  || echo "[warn] SMD finished with non-zero exit"
run_one SWaT || echo "[warn] SWaT finished with non-zero exit"

echo
echo "[$(date +'%F %T')] ALL DONE."
echo "Result roots:"
ls -d results/parallel/*_"${DATE}" 2>/dev/null
