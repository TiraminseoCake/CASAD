#!/bin/bash
# PSM final base: tuned default (LR 5e-5, batch 512, L 10, D 64, LAM_CAUSAL 1.0), current code, 4 seeds x 100 epochs, 1 seed per GPU
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_psm.yaml
OUTDIR=results/psm_final
mkdir -p $OUTDIR
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8

for s in 0 1 2 3; do
  rd=$OUTDIR/psm_base_seed$s
  CUDA_VISIBLE_DEVICES=$s nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$s]" \
    SOLVER.BASE_LR 5e-5 \
    > $rd.log 2>&1 &
  echo "GPU$s: seed $s (PID=$!)"
done
