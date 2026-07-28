#!/usr/bin/env bash
# Optimized re-score orchestrator (v2):
#   1) Skip mult_raw for SWaT/SMD — those match the original training-time eval
#      and are already in results/parallel/*/{entity}/seed{k}/*_epoch_metrics.csv.
#      Only compute add_calib, add_raw, mult_calib.
#   2) For SWaT (1 entity, 4 seeds), split by seed so each of the 4 GPUs handles
#      one seed → 4× speedup vs one-process-4-seeds.
#   3) For SMD (28 entities, 4 seeds), partition entities across GPUs; run all
#      4 seeds per process (matches sanity-timing which was fast per SMD seed).
#
# PSM×3 already fully re-scored under results/rescored/psm_{baseline,cotrain,detach}/
# (all four fusions × 16 epochs × 4 seeds) → NOT re-run here.
#
# Usage:
#   nohup bash scripts/run_rescore_v2.sh > logs/rescore_v2_master.log 2>&1 &

set -u

cd "$(dirname "$0")/.."

RESULTS=results/parallel
OUT_ROOT=results/rescored
PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
RESCORE=scripts/rescore_4way.py
FUSIONS="add_calib,add_raw,mult_calib"

mkdir -p "$OUT_ROOT" logs

launch_swat() {
    # 1 seed per GPU. args: gpu cfg src_basename out_name seed
    local gpu="$1" cfg="$2" src="$3" out="$4" seed="$5"
    local logf="logs/rescore_v2_${out}_s${seed}_gpu${gpu}.log"
    echo "[launch swat] GPU $gpu  $out  seed $seed"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" "$RESCORE" \
        --cfg "$cfg" \
        --source_dir "$RESULTS/$src" \
        --out_dir "$OUT_ROOT/$out" \
        --entities swat \
        --seeds "$seed" \
        --fusions "$FUSIONS" \
        > "$logf" 2>&1 &
}

launch_smd() {
    # partition entities across GPU. args: gpu cfg src_basename out_name entities_csv
    local gpu="$1" cfg="$2" src="$3" out="$4" ents="$5"
    local logf="logs/rescore_v2_${out}_gpu${gpu}.log"
    echo "[launch smd ] GPU $gpu  $out  ents=$(echo "$ents" | awk -F',' '{print NF}')"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" "$RESCORE" \
        --cfg "$cfg" \
        --source_dir "$RESULTS/$src" \
        --out_dir "$OUT_ROOT/$out" \
        --entities "$ents" \
        --seeds "0,1,2,3" \
        --fusions "$FUSIONS" \
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

# SMD entities partitioned into 4 shards of 7 (28 total)
SMD_1="machine-1-1,machine-1-2,machine-1-3,machine-1-4,machine-1-5,machine-1-6,machine-1-7"
SMD_2="machine-1-8,machine-2-1,machine-2-2,machine-2-3,machine-2-4,machine-2-5,machine-2-6"
SMD_3="machine-2-7,machine-2-8,machine-2-9,machine-3-1,machine-3-2,machine-3-3,machine-3-4"
SMD_4="machine-3-5,machine-3-6,machine-3-7,machine-3-8,machine-3-9,machine-3-10,machine-3-11"

echo "[$(date +'%F %T')] rescore v2 START (fusions=$FUSIONS)"

# ============================================================
# Phase A: SWaT × 3 variants  (per-seed sharding on 4 GPUs)
# ============================================================
# Baseline: 4 seeds on 4 GPUs → single wait
launch_swat 0 scripts/configs/swat.yaml swat_20260702-163856 swat_baseline 0; P0=$!
launch_swat 1 scripts/configs/swat.yaml swat_20260702-163856 swat_baseline 1; P1=$!
launch_swat 2 scripts/configs/swat.yaml swat_20260702-163856 swat_baseline 2; P2=$!
launch_swat 3 scripts/configs/swat.yaml swat_20260702-163856 swat_baseline 3; P3=$!
wait_all "SWaT baseline (4 seeds ‖)" $P0 $P1 $P2 $P3

launch_swat 0 scripts/configs/swat_gat_slp.yaml swat_gat_slp_20260707-233712 swat_cotrain 0; P0=$!
launch_swat 1 scripts/configs/swat_gat_slp.yaml swat_gat_slp_20260707-233712 swat_cotrain 1; P1=$!
launch_swat 2 scripts/configs/swat_gat_slp.yaml swat_gat_slp_20260707-233712 swat_cotrain 2; P2=$!
launch_swat 3 scripts/configs/swat_gat_slp.yaml swat_gat_slp_20260707-233712 swat_cotrain 3; P3=$!
wait_all "SWaT cotrain (4 seeds ‖)" $P0 $P1 $P2 $P3

launch_swat 0 scripts/configs/swat_gat_slp.yaml swat_gat_slp_detach_20260712-204106 swat_detach 0; P0=$!
launch_swat 1 scripts/configs/swat_gat_slp.yaml swat_gat_slp_detach_20260712-204106 swat_detach 1; P1=$!
launch_swat 2 scripts/configs/swat_gat_slp.yaml swat_gat_slp_detach_20260712-204106 swat_detach 2; P2=$!
launch_swat 3 scripts/configs/swat_gat_slp.yaml swat_gat_slp_detach_20260712-204106 swat_detach 3; P3=$!
wait_all "SWaT detach (4 seeds ‖)" $P0 $P1 $P2 $P3

echo "[$(date +'%F %T')] SWaT DONE. Starting SMD."

# ============================================================
# Phase B: SMD × 3 variants  (entity partition on 4 GPUs)
# ============================================================
launch_smd 0 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_1"; P0=$!
launch_smd 1 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_2"; P1=$!
launch_smd 2 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_3"; P2=$!
launch_smd 3 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_4"; P3=$!
wait_all "SMD baseline" $P0 $P1 $P2 $P3

launch_smd 0 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_1"; P0=$!
launch_smd 1 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_2"; P1=$!
launch_smd 2 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_3"; P2=$!
launch_smd 3 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_4"; P3=$!
wait_all "SMD cotrain" $P0 $P1 $P2 $P3

launch_smd 0 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_1"; P0=$!
launch_smd 1 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_2"; P1=$!
launch_smd 2 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_3"; P2=$!
launch_smd 3 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_4"; P3=$!
wait_all "SMD detach" $P0 $P1 $P2 $P3

echo "[$(date +'%F %T')] ALL RESCORE V2 DONE"
