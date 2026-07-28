#!/usr/bin/env bash
# Approach A: routing-input ablation. Runs concurrently with v4.
# 5 variants (full + 4 ablations) per checkpoint, mult_raw fusion.
#
# Usage:
#   nohup bash scripts/run_rescore_v5_ablate.sh > logs/rescore_v5_master.log 2>&1 &

set -u

cd "$(dirname "$0")/.."

RESULTS=results/parallel
OUT_ROOT=results/rescored_ablate
PYTHON=/home/sgshin/.conda/envs/sgshin/bin/python
RESCORE=scripts/rescore_ablate_routing.py
VARIANTS="full,no_phi,no_W,no_M,no_Mlearn"

mkdir -p "$OUT_ROOT" logs

launch_swat_seed() {
    local gpu="$1" cfg="$2" src="$3" out="$4" seed="$5"
    local logf="logs/rescore_v5_${out}_s${seed}_gpu${gpu}.log"
    echo "[launch swat] GPU $gpu  $out  seed $seed"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" "$RESCORE" \
        --cfg "$cfg" \
        --source_dir "$RESULTS/$src" \
        --out_dir "$OUT_ROOT/$out" \
        --entities swat \
        --seeds "$seed" \
        --variants "$VARIANTS" \
        > "$logf" 2>&1 &
}

launch_smd_partition() {
    local gpu="$1" cfg="$2" src="$3" out="$4" ents="$5"
    local logf="logs/rescore_v5_${out}_gpu${gpu}.log"
    echo "[launch smd ] GPU $gpu  $out  ents=$(echo "$ents" | awk -F',' '{print NF}')"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" "$RESCORE" \
        --cfg "$cfg" \
        --source_dir "$RESULTS/$src" \
        --out_dir "$OUT_ROOT/$out" \
        --entities "$ents" \
        --seeds "0,1,2,3" \
        --variants "$VARIANTS" \
        > "$logf" 2>&1 &
}

launch_psm_seed() {
    local gpu="$1" cfg="$2" src="$3" out="$4" seed="$5"
    local logf="logs/rescore_v5_${out}_s${seed}_gpu${gpu}.log"
    echo "[launch psm ] GPU $gpu  $out  seed $seed"
    CUDA_VISIBLE_DEVICES="$gpu" nohup "$PYTHON" "$RESCORE" \
        --cfg "$cfg" \
        --source_dir "$RESULTS/$src" \
        --out_dir "$OUT_ROOT/$out" \
        --entities PSM \
        --seeds "$seed" \
        --variants "$VARIANTS" \
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

SMD_1="machine-1-1,machine-1-2,machine-1-3,machine-1-4,machine-1-5,machine-1-6,machine-1-7"
SMD_2="machine-1-8,machine-2-1,machine-2-2,machine-2-3,machine-2-4,machine-2-5,machine-2-6"
SMD_3="machine-2-7,machine-2-8,machine-2-9,machine-3-1,machine-3-2,machine-3-3,machine-3-4"
SMD_4="machine-3-5,machine-3-6,machine-3-7,machine-3-8,machine-3-9,machine-3-10,machine-3-11"

echo "[$(date +'%F %T')] rescore v5 (routing ablation) START"

# Run in same GPU / config order as v4 so both experiments can share
# the eval-CPU workload evenly.

for pair in \
    "scripts/configs/psm.yaml          psm_20260701-221416                 psm_baseline" \
    "scripts/configs/psm_gat_slp.yaml  psm_gat_slp_20260707-233712         psm_cotrain " \
    "scripts/configs/psm_gat_slp.yaml  psm_gat_slp_detach_20260712-204106  psm_detach  "; do
    set -- $pair; cfg="$1" src="$2" out="$3"
    launch_psm_seed 0 "$cfg" "$src" "$out" 0; P0=$!
    launch_psm_seed 1 "$cfg" "$src" "$out" 1; P1=$!
    launch_psm_seed 2 "$cfg" "$src" "$out" 2; P2=$!
    launch_psm_seed 3 "$cfg" "$src" "$out" 3; P3=$!
    wait_all "PSM $out" $P0 $P1 $P2 $P3
done

echo "[$(date +'%F %T')] v5 PSM DONE. Starting SWaT."

for pair in \
    "scripts/configs/swat.yaml         swat_20260702-163856                swat_baseline" \
    "scripts/configs/swat_gat_slp.yaml swat_gat_slp_20260707-233712        swat_cotrain " \
    "scripts/configs/swat_gat_slp.yaml swat_gat_slp_detach_20260712-204106 swat_detach  "; do
    set -- $pair; cfg="$1" src="$2" out="$3"
    launch_swat_seed 0 "$cfg" "$src" "$out" 0; P0=$!
    launch_swat_seed 1 "$cfg" "$src" "$out" 1; P1=$!
    launch_swat_seed 2 "$cfg" "$src" "$out" 2; P2=$!
    launch_swat_seed 3 "$cfg" "$src" "$out" 3; P3=$!
    wait_all "SWaT $out" $P0 $P1 $P2 $P3
done

echo "[$(date +'%F %T')] v5 SWaT DONE. Starting SMD."

for pair in \
    "scripts/configs/smd.yaml          smd_20260702-163856                 smd_baseline" \
    "scripts/configs/smd_gat_slp.yaml  smd_gat_slp_20260707-233712         smd_cotrain " \
    "scripts/configs/smd_gat_slp.yaml  smd_gat_slp_detach_20260712-204106  smd_detach  "; do
    set -- $pair; cfg="$1" src="$2" out="$3"
    launch_smd_partition 0 "$cfg" "$src" "$out" "$SMD_1"; P0=$!
    launch_smd_partition 1 "$cfg" "$src" "$out" "$SMD_2"; P1=$!
    launch_smd_partition 2 "$cfg" "$src" "$out" "$SMD_3"; P2=$!
    launch_smd_partition 3 "$cfg" "$src" "$out" "$SMD_4"; P3=$!
    wait_all "SMD $out" $P0 $P1 $P2 $P3
done

echo "[$(date +'%F %T')] ALL RESCORE V5 DONE"
