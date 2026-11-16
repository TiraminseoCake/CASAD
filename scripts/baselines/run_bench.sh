#!/bin/bash
# Baseline re-runs in this environment: CAROTS (official code, official per-dataset settings) and
# OracleAD (base runner defaults) on PSM, SWaT, SMD(28) x seeds 0-3. Resumable: finished jobs are skipped.
# Usage: bash scripts/baselines/run_bench.sh [carots|oraclead|all]
WHAT=${1:-all}
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
CAROTS_DIR=/home/mschae/external/CAROTS
CAROTS_PY=/home/mschae/.conda/envs/carots/bin/python
OAD_PY=/home/mschae/.conda/envs/oraclead/bin/python
CASAD=/home/mschae/CASAD
SEEDS=(0 1 2 3)
NGPU=4
ENTS=($(ls $CASAD/data/SMD | sed 's/\.npz//' | sed 's/machine-//'))

# ---------------- CAROTS ----------------
CJOBS=()
for s in "${SEEDS[@]}"; do
  CJOBS+=("SWaT|$s|SOLVER.BASE_LR 0.0003 SOLVER.WEIGHT_DECAY 0.001")
  CJOBS+=("PSM|$s|SOLVER.BASE_LR 0.0003 SOLVER.WEIGHT_DECAY 0.001")
done
for s in "${SEEDS[@]}"; do for e in "${ENTS[@]}"; do
  CJOBS+=("SMD_$e|$s|SOLVER.BASE_LR 0.001 SOLVER.WEIGHT_DECAY 0.001")
done; done

carots_worker() {
  local w=$1 nw=$2 gpu=$(( $1 % NGPU ))
  cd $CAROTS_DIR
  for ((i=w; i<${#CJOBS[@]}; i+=nw)); do
    IFS='|' read -r name seed opts <<< "${CJOBS[$i]}"
    local rd=bench/seed$seed
    [ -f $rd/$name/test.txt ] && continue
    rm -rf $rd/$name
    echo "[$(date '+%m-%d %H:%M')] CAROTS GPU$gpu start $name seed$seed"
    $CAROTS_PY main.py DATA.NAME $name $opts SEED $seed VISIBLE_DEVICES $gpu \
      RESULT_DIR $rd/ TRAIN.CHECKPOINT_DIR $rd/ DATA_LOADER.NUM_WORKERS 2 \
      > bench_logs/${name}_s$seed.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] CAROTS GPU$gpu done  $name seed$seed (exit $?)"
  done
}

# ---------------- OracleAD ----------------
OJOBS=()
for s in "${SEEDS[@]}"; do
  OJOBS+=("SWaT|swat|$s") ; OJOBS+=("PSM|PSM|$s")
done
for s in "${SEEDS[@]}"; do for e in "${ENTS[@]}"; do OJOBS+=("SMD|machine-$e|$s"); done; done

oraclead_worker() {
  local w=$1 nw=$2 gpu=$(( $1 % NGPU ))
  cd $CASAD
  for ((i=w; i<${#OJOBS[@]}; i+=nw)); do
    IFS='|' read -r ds ent seed <<< "${OJOBS[$i]}"
    local od=results/bench/oraclead/$ds/seed$seed
    [ -f $od/$ent.npz ] && continue
    mkdir -p $od
    echo "[$(date '+%m-%d %H:%M')] OracleAD GPU$gpu start $ds/$ent seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $OAD_PY scripts/baselines/run_oraclead.py --input_dir data/$ds \
      --entities $ent --seed $seed --out_dir $od > $od/$ent.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] OracleAD GPU$gpu done  $ds/$ent seed$seed (exit $?)"
  done
}

mkdir -p $CAROTS_DIR/bench_logs $CASAD/results/bench
if [ "$WHAT" = carots ] || [ "$WHAT" = all ]; then
  NC=16; for ((w=0; w<NC; w++)); do carots_worker $w $NC & done
fi
if [ "$WHAT" = oraclead ] || [ "$WHAT" = all ]; then
  NO=8; for ((w=0; w<NO; w++)); do oraclead_worker $w $NO & done
fi
wait
echo "=== bench done: $(date) ==="
