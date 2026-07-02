#!/usr/bin/env bash
# Run cross-lag GAT variant (Option C) on PSM -> SMD -> SWaT sequentially,
# 4-GPU parallel per dataset. Baseline (MHSA) results should already exist
# under results/parallel/psm_*, smd_*, swat_* for comparison.
#
# Usage:
#   bash scripts/run_all_gat.sh                             # foreground (tmux)
#   nohup bash scripts/run_all_gat.sh > logs/run_all_gat.log 2>&1 &
#
# Each dataset writes to results/parallel/{dataset}_gat_{DATE}/ and produces
# summary_all_epochs.csv + summary_best_epoch.csv on completion.

set -u
GPUS="${GPUS:-0,1,2,3}"
SEEDS="${SEEDS:-0,1,2,3}"
EPOCHS="${EPOCHS:-80}"
DATE="$(date +%Y%m%d-%H%M%S)"

cd "$(dirname "$0")/.."
mkdir -p logs

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
