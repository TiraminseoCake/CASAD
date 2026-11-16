#!/bin/bash
# PSM ablation under the aligned protocol (batch 512, 80 epochs, scaler/prior on train_sub,
# best_smooth primary + best_val/last, LR 5e-5, seeds 0-3). One component removed per variant.
# Full = results/hb/PSM (reused). Resumable.
cd /home/mschae/CASAD
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY=/home/mschae/.conda/envs/oraclead/bin/python
OUT=results/ablation_hb/PSM
COMMON="SOLVER.BASE_LR 5e-5 SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True"
VARIANTS=(
  "no_delta|PICAAD.DYNAMIC_GRAPH False"
  "no_crsloss|PICAAD.START_CLS_EPOCH 81"
  "no_interv|PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH 0"
  "no_refupdate|PICAAD.INTERVENTION.UPDATE_REFERENCE False"
  "no_intloss|PICAAD.INTERVENTION.APPLY_LOSS False"
  "no_prioralign|PICAAD.ENABLE_PRIOR_LOSS False"
  "no_prior|PICAAD.PRIOR.TYPE none"
  "no_cattn|PICAAD.CAUSAL_ATTN_MASK_SCALE 0.0"
)
JOBS=(); for v in "${VARIANTS[@]}"; do for s in 0 1 2 3; do JOBS+=("$v|$s"); done; done
NGPU=4; NW=${NW:-16}
worker() {
  local w=$1 gpu=$(( $1 % NGPU ))
  for ((i=w; i<${#JOBS[@]}; i+=NW)); do
    IFS='|' read -r name opts seed <<< "${JOBS[$i]}"
    local rd=$OUT/$name/PSM_seed$seed
    [ -f $rd/summary.csv ] && continue
    mkdir -p $OUT/$name
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu start $name seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $PY main.py --cfg scripts/configs/ablation_psm.yaml RESULT_DIR $rd RESULT_DIR_LITERAL True \
      SEEDS "[$seed]" $COMMON $opts > $rd.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu done  $name seed$seed (exit $?)"
  done
}
mkdir -p $OUT
for ((w=0; w<NW; w++)); do worker $w & done
wait
echo "=== psm ablation done: $(date) ==="
