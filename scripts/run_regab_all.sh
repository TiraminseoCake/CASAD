#!/usr/bin/env bash
# Master orchestrator for the regularizer ablation study.
# Runs SMD -> SWaT -> PSM sequentially. Each dataset script drives 4 GPUs
# internally, so datasets cannot overlap.
#
# Prerequisite: `git apply -R` of the intervention.py detach patch was
# already performed. Baselines are reused from the existing
# {psm,swat,smd}_2026070* directories in results/parallel.
#
# Usage:
#   nohup bash scripts/run_regab_all.sh > logs/regab_all_master.log 2>&1 &
set -u
cd "$(dirname "$0")/.."

mkdir -p logs

STAMP() { date +'%F %T'; }

echo "[$(STAMP)] === REGAB ALL START ==="
echo "Order: SMD -> SWaT -> PSM"
echo "Each script writes to results/parallel/<dataset>_regab_*_<timestamp>/"
echo ""

echo "[$(STAMP)] === Phase 1: SMD ==="
bash scripts/run_regab_smd.sh
echo "[$(STAMP)] === Phase 1: SMD DONE ==="

# Paused here per user decision: review SMD no_all_4 result before deciding
# whether to launch SWaT/PSM. To resume, run these two scripts manually:
#   nohup bash scripts/run_regab_swat.sh > logs/regab_swat_master.log 2>&1 &
#   (wait for SWaT to finish, then)
#   nohup bash scripts/run_regab_psm.sh  > logs/regab_psm_master.log  2>&1 &
echo "[$(STAMP)] === REGAB (SMD-only) DONE. SWaT/PSM held for review. ==="

# --- ORIGINAL AUTO-CONTINUATION (disabled) ---
# echo "[$(STAMP)] === Phase 2: SWaT ==="
# bash scripts/run_regab_swat.sh
# echo "[$(STAMP)] === Phase 2: SWaT DONE ==="
#
# echo "[$(STAMP)] === Phase 3: PSM ==="
# bash scripts/run_regab_psm.sh
# echo "[$(STAMP)] === Phase 3: PSM DONE ==="
#
# echo "[$(STAMP)] === REGAB ALL DONE ==="
