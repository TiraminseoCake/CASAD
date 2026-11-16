#!/bin/bash
# OracleAD reimplemented per the NeurIPS 2025 paper (oraclead_npz_runner_2d_paper.py with paper settings:
# L=10, 2-layer LSTM enc/dec, AdamW, lr PSM 5e-5 / SMD,SWaT 5e-4, batch 1024, squared-L2 losses,
# lam_recon 0.1, lam_dev 3, per-epoch SLS from epoch 2, L2 dissimilarity, A = P * D, 20 epochs)
# under the shared protocol: fit on the first 80% of train, seeds 0-3. Resumable.
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
PY=/home/mschae/.conda/envs/oraclead/bin/python
RUNNER=/home/mschae/oraclead_transfer/oraclead-repro/src/runners/oraclead_npz_runner_2d_paper.py
CASAD=/home/mschae/CASAD
OUT=$CASAD/results/bench/oraclead_v2
NGPU=4; NW=${NW:-12}
JOBS=()
for s in 0 1 2 3; do JOBS+=("SWaT|swat|$s") ; JOBS+=("PSM|PSM|$s"); done
for s in 0 1 2 3; do for f in $CASAD/data/SMD/machine-*.npz; do JOBS+=("SMD|$(basename $f .npz)|$s"); done; done

worker() {
  local w=$1 gpu=$(( $1 % NGPU ))
  for ((i=w; i<${#JOBS[@]}; i+=NW)); do
    IFS='|' read -r ds ent seed <<< "${JOBS[$i]}"
    local od=$OUT/$ds/seed$seed
    [ -f $od/${ent}_seed$seed.npz ] && continue
    mkdir -p $od
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu start $ds/$ent seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $PY $RUNNER --input_dir $CASAD/data/$ds --entities $ent --dataset $ds \
      --L 10 --batch 1024 --epochs 20 --enc_layers 2 --dec_layers 2 --lam_recon 0.1 --lam_dev 3.0 \
      --sls_ema 0.0 --start_sls_epoch 2 --loss_norm sq --train_ratio 0.8 --seeds $seed \
      --use_median_vus_window --save_per_seed --out_dir $od > $od/${ent}.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu done  $ds/$ent seed$seed (exit $?)"
  done
}
mkdir -p $OUT
for ((w=0; w<NW; w++)); do worker $w & done
wait
echo "=== oraclead_v2 done: $(date) ==="
