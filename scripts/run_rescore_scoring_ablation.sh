#!/usr/bin/env bash
# Score-component ablation rescoring (leave-one-out).
#   Baseline fusion: add_calib
#   Individual:      P_only, C_only, G_only     (already exist, recomputed for parity)
#   Leave-one-out:   no_P_add=C+G, no_C_add=P+G, no_G_add=P+C  (calibrated addition)
#
# Runs against the OLD baseline checkpoints (psm_20260701, swat_20260702,
# smd_20260702) so the anomaly-score table in the paper is apples-to-apples.
# GPU footprint is small (forward-only), so this can share GPU 0 with the
# ongoing SMD regularizer-ablation training.
#
# Usage:
#   nohup bash scripts/run_rescore_scoring_ablation.sh \
#       > logs/rescore_scoring_ablation_master.log 2>&1 &
set -u

cd "$(dirname "$0")/.."

RESULTS=results/parallel
OUT_ROOT=results/rescored_scoring_ablation
PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
RESCORE=scripts/rescore_best_epoch_only.py
FUSIONS="add_calib,P_only,C_only,G_only,no_P_add,no_C_add,no_G_add"
GPU=0

mkdir -p "$OUT_ROOT" logs

echo "[$(date +'%F %T')] scoring-ablation rescore START (GPU $GPU)"

# ==== PSM (1 entity, 4 seeds) ====
echo "[$(date +'%F %T')] PSM rescoring ..."
CUDA_VISIBLE_DEVICES="$GPU" "$PYTHON" "$RESCORE" \
    --cfg scripts/configs/psm.yaml \
    --source_dir "$RESULTS/psm_20260701-221416" \
    --out_dir "$OUT_ROOT/psm_baseline" \
    --entities PSM \
    --seeds "0,1,2,3" \
    --fusions "$FUSIONS" \
    > logs/rescore_scoring_ablation_psm.log 2>&1
echo "[$(date +'%F %T')] PSM DONE"

# ==== SWaT (1 entity, 4 seeds) ====
echo "[$(date +'%F %T')] SWaT rescoring ..."
CUDA_VISIBLE_DEVICES="$GPU" "$PYTHON" "$RESCORE" \
    --cfg scripts/configs/swat.yaml \
    --source_dir "$RESULTS/swat_20260702-163856" \
    --out_dir "$OUT_ROOT/swat_baseline" \
    --entities swat \
    --seeds "0,1,2,3" \
    --fusions "$FUSIONS" \
    > logs/rescore_scoring_ablation_swat.log 2>&1
echo "[$(date +'%F %T')] SWaT DONE"

# ==== SMD (28 entities, 4 seeds) ====
echo "[$(date +'%F %T')] SMD rescoring ..."
CUDA_VISIBLE_DEVICES="$GPU" "$PYTHON" "$RESCORE" \
    --cfg scripts/configs/smd.yaml \
    --source_dir "$RESULTS/smd_20260702-163856" \
    --out_dir "$OUT_ROOT/smd_baseline" \
    --seeds "0,1,2,3" \
    --fusions "$FUSIONS" \
    > logs/rescore_scoring_ablation_smd.log 2>&1
echo "[$(date +'%F %T')] SMD DONE"

echo "[$(date +'%F %T')] scoring-ablation rescore ALL DONE"
echo "Outputs: $OUT_ROOT/{psm,swat,smd}_baseline/"
