#!/usr/bin/env bash
# Run PSM -> SMD -> SWaT sequentially with 4-GPU parallelism.
#
# Usage:
#   bash scripts/run_all.sh                             # foreground (current terminal)
#   nohup bash scripts/run_all.sh > run_all.log 2>&1 &  # background, terminal-safe
#
# Each dataset writes to results/parallel/{dataset}_{DATE}/ and produces
# summary_all_epochs.csv + summary_best_epoch.csv on completion.

set -u
GPUS="${GPUS:-0,1,2,3}"
SEEDS="${SEEDS:-0,1,2,3}"
EPOCHS="${EPOCHS:-80}"
DATE="$(date +%Y%m%d-%H%M%S)"

# Change to repo root regardless of where the script is invoked from
cd "$(dirname "$0")/.."
mkdir -p logs

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
