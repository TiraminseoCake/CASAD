#!/bin/bash
# SWaT 5x-downsampled (CAROTS protocol, data/SWaT_ds5) under the aligned protocol:
#   PICAAD: batch 512, 80 epochs, scaler+prior on train_sub, best_val/best_smooth/last, LR 5e-4, seeds 0-3
#   OracleAD (paper-faithful 2d_paper runner): same split (train_ratio 0.8), paper settings, 20 epochs, seeds 0-3
cd /home/mschae/CASAD
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
PY=/home/mschae/.conda/envs/oraclead/bin/python
OUT=results/hb/SWaT_ds5; OOUT=results/bench/oraclead_v2/SWaT_ds5
mkdir -p $OUT $OOUT
CFG=scripts/configs/ablation_swat.yaml
COMMON="DATA.INPUT_DIR data/SWaT_ds5 SOLVER.BASE_LR 5e-4 SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True"

# OracleAD needs no prior: start right away (GPU 1,3)
for s in 0 1 2 3; do
  od=$OOUT/seed$s; mkdir -p $od; g=$(( s % 2 == 0 ? 1 : 3 ))
  CUDA_VISIBLE_DEVICES=$g $PY /home/mschae/oraclead_transfer/oraclead-repro/src/runners/oraclead_npz_runner_2d_paper.py \
    --input_dir data/SWaT_ds5 --entities swat --dataset SWaT --L 10 --batch 1024 --epochs 20 --enc_layers 2 --dec_layers 2 \
    --lam_recon 0.1 --lam_dev 3.0 --sls_ema 0.0 --start_sls_epoch 2 --loss_norm sq --train_ratio 0.8 --seeds $s \
    --use_median_vus_window --save_per_seed --out_dir $od > $od/swat.log 2>&1 &
done

# PICAAD: prior once, then 4 seeds (GPU 0,2)
$PY scripts/precompute_priors.py --cfg $CFG $COMMON > $OUT/prior.log 2>&1
for s in 0 1 2 3; do
  rd=$OUT/swat_seed$s; g=$(( s % 2 == 0 ? 0 : 2 ))
  CUDA_VISIBLE_DEVICES=$g $PY main.py --cfg $CFG RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$s]" $COMMON > $rd.log 2>&1 &
done
wait
echo "=== swat_ds5 done: $(date) ==="
