#!/bin/bash
# SWaT 5x median-downsampled (CAROTS protocol), batch 512, 4 seeds x 100 epochs, 1 seed per GPU.
# Seed 0 starts first so the new PCMCI+ prior is computed and cached once.
cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_swat.yaml
OUTDIR=results/swat_ds5
mkdir -p $OUTDIR
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8

launch() {
  local s=$1 rd=$OUTDIR/swat_ds5_bs512_seed$1
  CUDA_VISIBLE_DEVICES=$s nohup $PYTHON main.py --cfg $CFG \
    RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$s]" DATA.INPUT_DIR data/SWaT_ds5 \
    SOLVER.BASE_LR 5e-4 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 \
    > $rd.log 2>&1 &
  echo "[$(date '+%m-%d %H:%M')] GPU$s: seed $s (PID=$!)"
}

launch 0
until grep -q "training \.\.\." $OUTDIR/swat_ds5_bs512_seed0.log 2>/dev/null; do sleep 20; done
for s in 1 2 3; do launch $s; done
