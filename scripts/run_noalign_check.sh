#!/bin/bash
# Check whether turning off the prior alignment loss (tew + teg; PICAAD.ENABLE_PRIOR_LOSS False) generalizes
# beyond PSM. Same aligned protocol as results/hb (Full reused from there). SWaT_ds5 + all 28 SMD entities, seeds 0-3.
# SWaT jobs come first so each GPU holds one SWaT job plus SMD jobs. Resumable.
cd /home/mschae/CASAD
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY=/home/mschae/.conda/envs/oraclead/bin/python
OUT=results/ablation_hb
COMMON="SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True PICAAD.ENABLE_PRIOR_LOSS False"
ENTS=($(ls data/SMD/*.npz | xargs -n1 basename | sed 's/\.npz//'))
JOBS=()
for s in 0 1 2 3; do JOBS+=("SWaT_ds5|swat|$s"); done
for s in 0 1 2 3; do for e in "${ENTS[@]}"; do JOBS+=("SMD|$e|$s"); done; done
NGPU=4; NW=${NW:-16}
worker() {
  local w=$1 gpu=$(( $1 % NGPU ))
  for ((i=w; i<${#JOBS[@]}; i+=NW)); do
    IFS='|' read -r ds ent seed <<< "${JOBS[$i]}"
    local rd=$OUT/$ds/no_prioralign/${ent}_seed$seed
    [ -f $rd/summary.csv ] && continue
    if [ $ds = SWaT_ds5 ]; then
      opts="--cfg scripts/configs/ablation_swat.yaml DATA.INPUT_DIR data/SWaT_ds5 SOLVER.BASE_LR 5e-4"
    else
      opts="--cfg scripts/configs/ablation_smd.yaml SOLVER.BASE_LR 5e-4"
    fi
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu start $ds/$ent seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $PY main.py $opts RESULT_DIR $rd RESULT_DIR_LITERAL True \
      SEEDS "[$seed]" DATA.ENTITIES $ent $COMMON > $rd.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu done  $ds/$ent seed$seed (exit $?)"
  done
}
mkdir -p $OUT/SMD/no_prioralign $OUT/SWaT_ds5/no_prioralign
for ((w=0; w<NW; w++)); do worker $w & done
wait
echo "=== noalign check done: $(date) ==="
