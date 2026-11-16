#!/bin/bash
# SMD final base on CAROTS entities: LR 5e-5 (from SMD tuning), batch 512, L 10, D 64, LAM_CAUSAL 1.0
# 2 entities x 4 seeds x 100 epochs, one job per (entity, seed), 2 jobs per GPU
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_smd.yaml
OUTDIR=results/smd_final
mkdir -p $OUTDIR
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8

i=0
for e in machine-2-1 machine-3-7; do
  for s in 0 1 2 3; do
    rd=$OUTDIR/smd_lr5e-5_${e}_seed$s
    CUDA_VISIBLE_DEVICES=$((i % 4)) nohup $PYTHON main.py --cfg $CFG \
      RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$s]" DATA.ENTITIES $e \
      SOLVER.BASE_LR 5e-5 \
      > $rd.log 2>&1 &
    echo "GPU$((i % 4)): $e seed $s (PID=$!)"
    i=$((i + 1))
  done
done
