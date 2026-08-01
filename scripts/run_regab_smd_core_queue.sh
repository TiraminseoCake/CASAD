#!/usr/bin/env bash
# Chains the SMD core-loss ablations:
#   1. Wait for any currently running SMD training to finish
#      (no_inv, and no_all_4 if bash re-read the appended line).
#   2. If smd_regab_no_all_4_* is missing, launch the standalone fallback.
#   3. Run no_prior -> no_crs -> no_int sequentially.
#
# Each subscript uses `wait` internally and blocks this script until done.
#
# Usage:
#   nohup bash scripts/run_regab_smd_core_queue.sh \
#       > logs/regab_smd_core_queue_master.log 2>&1 &
set -u
cd "$(dirname "$0")/.."

STAMP() { date +'%F %T'; }

wait_for_smd_idle() {
    local label="$1"
    echo "[$(STAMP)] Waiting for SMD training to be idle: $label"
    # Poll every 5 minutes for any main.py process using the SMD config.
    while pgrep -f "main\.py.*--cfg scripts/configs/smd\.yaml" > /dev/null 2>&1; do
        sleep 300
    done
    echo "[$(STAMP)] SMD idle: $label"
}

echo "[$(STAMP)] === SMD core-queue START ==="

# --- Phase 0: wait for currently running SMD (no_inv, no_all_4) to finish ---
wait_for_smd_idle "existing regab (no_inv, maybe no_all_4)"

# --- Phase 1: ensure no_all_4 has run; launch fallback if missing ---
if ls -d results/parallel/smd_regab_no_all_4_* > /dev/null 2>&1; then
    echo "[$(STAMP)] no_all_4 result dir already exists; skipping fallback"
else
    echo "[$(STAMP)] no_all_4 dir missing; launching standalone fallback"
    bash scripts/run_regab_smd_no_all_4.sh
    wait_for_smd_idle "no_all_4 fallback"
fi

# --- Phase 2: core-loss ablations, sequential ---
echo "[$(STAMP)] === Phase 2a: no_prior ==="
bash scripts/run_regab_smd_no_prior.sh
echo "[$(STAMP)] === Phase 2a: no_prior DONE ==="

echo "[$(STAMP)] === Phase 2b: no_crs ==="
bash scripts/run_regab_smd_no_crs.sh
echo "[$(STAMP)] === Phase 2b: no_crs DONE ==="

echo "[$(STAMP)] === Phase 2c: no_int ==="
bash scripts/run_regab_smd_no_int.sh
echo "[$(STAMP)] === Phase 2c: no_int DONE ==="

echo "[$(STAMP)] === SMD core-queue ALL DONE ==="
echo "Result dirs:"
ls -d results/parallel/smd_regab_{no_all_4,no_prior,no_crs,no_int}_* 2>/dev/null
