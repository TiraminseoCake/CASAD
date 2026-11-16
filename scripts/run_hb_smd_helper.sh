#!/bin/bash
# Helper for run_hb_protocol.sh: run SMD jobs that are still pending (no summary.csv and not running),
# on the GPUs left idle while the main queue's SWaT jobs finish. Same settings as the main queue.
cd /home/mschae/CASAD
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
PY=/home/mschae/.conda/envs/oraclead/bin/python
OUT=results/hb
COMMON="SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True"
JOBS=()
for s in 3 2 1 0; do for e in $(ls data/SMD | sed 's/\.npz//' | sort -r); do
  [ -f $OUT/SMD/${e}_seed$s/summary.csv ] || JOBS+=("$e|$s"); done; done
GPUS=(1 3 1 3 0 2 1 3 1 3 0 2); NW=${#GPUS[@]}
worker() {
  local w=$1 gpu=${GPUS[$1]}
  for ((i=w; i<${#JOBS[@]}; i+=NW)); do
    IFS='|' read -r ent seed <<< "${JOBS[$i]}"
    local rd=$OUT/SMD/${ent}_seed$seed
    [ -f $rd/summary.csv ] && continue
    pgrep -u $USER -f "RESULT_DIR $rd " > /dev/null && continue
    echo "[$(date '+%m-%d %H:%M')] helper GPU$gpu start SMD/$ent seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $PY main.py --cfg scripts/configs/ablation_smd.yaml RESULT_DIR $rd RESULT_DIR_LITERAL True \
      SEEDS "[$seed]" DATA.ENTITIES $ent SOLVER.BASE_LR 5e-4 $COMMON > $rd.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] helper GPU$gpu done  SMD/$ent seed$seed (exit $?)"
  done
}
echo "=== helper: ${#JOBS[@]} pending SMD jobs, $NW workers, $(date) ==="
for ((w=0; w<NW; w++)); do worker $w & done
wait
echo "=== helper done: $(date) ==="
