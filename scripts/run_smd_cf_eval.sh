#!/bin/bash
# SMD CF scoring evaluation — all entities, all seeds, 4 GPUs parallel
set -e

RESULT_DIR="/home/mschae/CASAD/results/parallel/smd_paper_align_20260901"
CFG="/home/mschae/CASAD/scripts/configs/smd.yaml"
PYTHON="/home/mschae/.conda/envs/oraclead/bin/python"
SCRIPT="/home/mschae/CASAD/scripts/eval_cf.py"
OUTDIR="/home/mschae/CASAD/results/cf_eval_smd"
mkdir -p "$OUTDIR"

ENTITIES=(
  machine-1-1 machine-1-2 machine-1-3 machine-1-4 machine-1-5 machine-1-6 machine-1-7 machine-1-8
  machine-2-1 machine-2-2 machine-2-3 machine-2-4 machine-2-5 machine-2-6 machine-2-7 machine-2-8 machine-2-9
  machine-3-1 machine-3-2 machine-3-3 machine-3-4 machine-3-5 machine-3-6 machine-3-7 machine-3-8 machine-3-9 machine-3-10 machine-3-11
)
SEEDS=(0 1 2 3)
NUM_GPUS=4

job_idx=0
for ent in "${ENTITIES[@]}"; do
  for seed in "${SEEDS[@]}"; do
    gpu=$((job_idx % NUM_GPUS))
    ckpt_dir="${RESULT_DIR}/${ent}/seed${seed}/ckpt"
    outfile="${OUTDIR}/${ent}_seed${seed}.txt"

    if [ ! -d "$ckpt_dir" ]; then
      echo "SKIP: $ckpt_dir not found"
      continue
    fi

    CUDA_VISIBLE_DEVICES=$gpu $PYTHON $SCRIPT \
      --cfg "$CFG" \
      --ckpt-dir "$ckpt_dir" \
      --seed "$seed" \
      --entity "$ent" \
      --cf-top-k 15 \
      > "$outfile" 2>&1 &

    job_idx=$((job_idx + 1))

    # Wait when all GPUs are busy
    if [ $((job_idx % NUM_GPUS)) -eq 0 ]; then
      wait
    fi
  done
done

wait
echo "All SMD CF evaluations done."
echo "Results in: $OUTDIR"
