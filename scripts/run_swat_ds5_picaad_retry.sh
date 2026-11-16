#!/bin/bash
# Retry of PICAAD SWaT_ds5 seeds (first attempt hit CUDA OOM while GPUs were shared).
# Runs 4 seeds immediately, two per GPU on GPUs 1 and 3 (most free memory). Prior is already cached.
cd /home/mschae/CASAD
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
GPUS=(1 3 1 3)
PY=/home/mschae/.conda/envs/oraclead/bin/python
OUT=results/hb/SWaT_ds5
COMMON="DATA.INPUT_DIR data/SWaT_ds5 SOLVER.BASE_LR 5e-4 SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True"
echo "[$(date '+%m-%d %H:%M')] start PICAAD SWaT_ds5 retry"
for s in 0 1 2 3; do
  rd=$OUT/swat_seed$s
  CUDA_VISIBLE_DEVICES=${GPUS[$s]} $PY main.py --cfg scripts/configs/ablation_swat.yaml RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$s]" $COMMON > $rd.log 2>&1 &
done
wait
echo "=== swat_ds5 picaad done: $(date) ==="
