#!/usr/bin/env bash
# Launch rescore_4way.py across 4 GPUs for all 9 (dataset × variant) runs.
#
# Work partitioning:
#   PSM/SWaT are single-entity so we shard by (dataset, variant, seed) — 6
#   configs × 4 seeds = 24 seed-jobs assigned to whichever GPU is free.
#   SMD has 28 entities, so we shard by (variant, entity_partition) — 3
#   variants × 4 partitions of 7 entities each = 12 large jobs.
#
# Layout of --source_dir → --out_dir mapping (edit here if run dirs change):
#   psm_20260701-221416          → psm_baseline
#   smd_20260702-163856          → smd_baseline
#   swat_20260702-163856         → swat_baseline
#   psm_gat_slp_20260707-233712  → psm_cotrain
#   smd_gat_slp_20260707-233712  → smd_cotrain
#   swat_gat_slp_20260707-233712 → swat_cotrain
#   psm_gat_slp_detach_20260712-204106  → psm_detach
#   smd_gat_slp_detach_20260712-204106  → smd_detach
#   swat_gat_slp_detach_20260712-204106 → swat_detach
#
# Usage:
#   bash scripts/run_rescore_4way.sh
#   nohup bash scripts/run_rescore_4way.sh > logs/rescore_4way_master.log 2>&1 &

set -u

cd "$(dirname "$0")/.."

RESULTS=results/parallel
OUT_ROOT=results/rescored
mkdir -p "$OUT_ROOT" logs

PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
RESCORE=scripts/rescore_4way.py

# SMD 28 entities, partitioned into 4 shards of 7
SMD_ENT_1_1="machine-1-1,machine-1-2,machine-1-3,machine-1-4,machine-1-5,machine-1-6,machine-1-7"
SMD_ENT_1_2="machine-1-8,machine-2-1,machine-2-2,machine-2-3,machine-2-4,machine-2-5,machine-2-6"
SMD_ENT_1_3="machine-2-7,machine-2-8,machine-2-9,machine-3-1,machine-3-2,machine-3-3,machine-3-4"
SMD_ENT_1_4="machine-3-5,machine-3-6,machine-3-7,machine-3-8,machine-3-9,machine-3-10,machine-3-11"

launch() {
    # $1=gpu $2=cfg $3=source_dir_basename $4=out_dir_name $5=entities
    local gpu="$1" cfg="$2" src="$3" out="$4" ents="$5"
    local logf="logs/rescore_${out}_gpu${gpu}.log"
    echo "[launch] GPU $gpu  $cfg  →  $out  ents=$(echo "$ents" | awk -F',' '{print NF}')  log=$logf"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" "$RESCORE" \
        --cfg "$cfg" \
        --source_dir "$RESULTS/$src" \
        --out_dir "$OUT_ROOT/$out" \
        --entities "$ents" \
        --seeds "0,1,2,3" \
        > "$logf" 2>&1 &
}

wait_group() {
    local group_name="$1"; shift
    local pids=("$@")
    echo "[wait] $group_name  pids=${pids[*]}"
    for pid in "${pids[@]}"; do
        wait "$pid"
        echo "[done] pid=$pid  status=$?"
    done
}

echo "[$(date +'%F %T')] rescore START"

# ---- Group 1: PSM + SWaT (small, fast) across 4 GPUs ----
launch 0 scripts/configs/psm.yaml          psm_20260701-221416                psm_baseline PSM
P0=$!
launch 1 scripts/configs/psm_gat_slp.yaml  psm_gat_slp_20260707-233712        psm_cotrain  PSM
P1=$!
launch 2 scripts/configs/psm_gat_slp.yaml  psm_gat_slp_detach_20260712-204106 psm_detach   PSM
P2=$!
launch 3 scripts/configs/swat.yaml         swat_20260702-163856               swat_baseline swat
P3=$!
wait_group "PSM x3 + SWaT baseline" $P0 $P1 $P2 $P3

launch 0 scripts/configs/swat_gat_slp.yaml swat_gat_slp_20260707-233712        swat_cotrain swat
P0=$!
launch 1 scripts/configs/swat_gat_slp.yaml swat_gat_slp_detach_20260712-204106 swat_detach  swat
P1=$!
wait_group "SWaT cotrain + detach" $P0 $P1

echo "[$(date +'%F %T')] PSM + SWaT DONE. Starting SMD."

# ---- Group 2: SMD baseline across 4 GPUs (partitioned entities) ----
launch 0 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_ENT_1_1"
P0=$!
launch 1 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_ENT_1_2"
P1=$!
launch 2 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_ENT_1_3"
P2=$!
launch 3 scripts/configs/smd.yaml smd_20260702-163856 smd_baseline "$SMD_ENT_1_4"
P3=$!
wait_group "SMD baseline" $P0 $P1 $P2 $P3

# ---- Group 3: SMD cotrain ----
launch 0 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_ENT_1_1"
P0=$!
launch 1 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_ENT_1_2"
P1=$!
launch 2 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_ENT_1_3"
P2=$!
launch 3 scripts/configs/smd_gat_slp.yaml smd_gat_slp_20260707-233712 smd_cotrain "$SMD_ENT_1_4"
P3=$!
wait_group "SMD cotrain" $P0 $P1 $P2 $P3

# ---- Group 4: SMD detach ----
launch 0 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_ENT_1_1"
P0=$!
launch 1 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_ENT_1_2"
P1=$!
launch 2 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_ENT_1_3"
P2=$!
launch 3 scripts/configs/smd_gat_slp.yaml smd_gat_slp_detach_20260712-204106 smd_detach "$SMD_ENT_1_4"
P3=$!
wait_group "SMD detach" $P0 $P1 $P2 $P3

echo "[$(date +'%F %T')] ALL RESCORE DONE"
