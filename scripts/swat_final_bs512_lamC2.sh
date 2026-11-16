#!/bin/bash
# SWaT final candidate: batch 512 + LAM_CAUSAL 2.0 (from SWaT HP tuning), 4 seeds x 100 epochs, 1 seed per GPU
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_swat.yaml
OUTDIR=results/swat_final
mkdir -p $OUTDIR
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8

for s in 0 1 2 3; do
  rd=$OUTDIR/swat_bs512_lamC2_seed$s
  CUDA_VISIBLE_DEVICES=$s nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$s]" \
    SOLVER.BASE_LR 5e-4 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 PICAAD.LAM_CAUSAL 2.0 \
    > $rd.log 2>&1 &
  echo "GPU$s: seed $s (PID=$!)"
done
