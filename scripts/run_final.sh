#!/bin/bash
# PICAAD final model (paper Table 2): prior alignment loss off, A = P + C, best_smooth checkpoint, seeds 0-3.
# Same settings as results/ablation_hb/{PSM,SMD,SWaT_ds5}/no_prioralign. Resumable.
# Usage: bash scripts/run_final.sh [PSM|SMD|SWaT_ds5 ...]   (default: all three)
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY=${PY:-python}
OUT=${OUT:-results/final}
NGPU=${NGPU:-$(nvidia-smi -L | wc -l)}; NW=${NW:-$((NGPU * 2))}
COMMON="SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True PICAAD.ENABLE_PRIOR_LOSS False"
DATASETS=("${@:-PSM SMD SWaT_ds5}"); DATASETS=(${DATASETS[@]})

JOBS=()
for ds in "${DATASETS[@]}"; do
  case $ds in
    PSM)      ents=(PSM) ;;
    SWaT_ds5) ents=(swat) ;;
    SMD)      ents=($(ls data/SMD/*.npz | xargs -n1 basename | sed 's/\.npz//')) ;;
  esac
  for s in 0 1 2 3; do for e in "${ents[@]}"; do JOBS+=("$ds|$e|$s"); done; done
done

worker() {
  local w=$1 gpu=$(( $1 % NGPU ))
  for ((i=w; i<${#JOBS[@]}; i+=NW)); do
    IFS='|' read -r ds ent seed <<< "${JOBS[$i]}"
    local rd=$OUT/$ds/${ent}_seed$seed
    [ -f $rd/summary.csv ] && continue
    case $ds in
      PSM)      opts="--cfg scripts/configs/ablation_psm.yaml SOLVER.BASE_LR 5e-5" ;;
      SWaT_ds5) opts="--cfg scripts/configs/ablation_swat.yaml DATA.INPUT_DIR data/SWaT_ds5 SOLVER.BASE_LR 5e-4 DATA.ENTITIES $ent" ;;
      SMD)      opts="--cfg scripts/configs/ablation_smd.yaml SOLVER.BASE_LR 5e-4 DATA.ENTITIES $ent" ;;
    esac
    mkdir -p $OUT/$ds
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu start $ds/$ent seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $PY main.py $opts RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$seed]" $COMMON > $rd.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu done  $ds/$ent seed$seed (exit $?)"
  done
}
for ((w=0; w<NW; w++)); do worker $w & done
wait
echo "=== final runs done: $(date) ==="
