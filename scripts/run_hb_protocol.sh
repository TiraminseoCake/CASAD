#!/bin/bash
# PICAAD main runs under the aligned protocol:
#   batch 512 for all datasets (this server); everything else follows the ablation protocol H_B:
#   80 epochs, scaler + PCMCI+ prior fit on train_sub (first 80% of train), checkpoint = best_val
#   (min validation prediction MAE; best_smooth and last also evaluated), seeds 0-3,
#   LR PSM 5e-5 / SMD 5e-4 / SWaT 5e-4. SMD = all 28 entities. Resumable.
cd /home/mschae/CASAD
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
PY=/home/mschae/.conda/envs/oraclead/bin/python
OUT=results/hb
mkdir -p $OUT
COMMON="SOLVER.MAX_EPOCH 80 TRAIN.BATCH_SIZE 512 TEST.BATCH_SIZE 512 DATA.FIT_ON_TRAIN_SUB True PICAAD.SELECT_BEST_VAL True"
declare -A CFG=([PSM]=scripts/configs/ablation_psm.yaml [SMD]=scripts/configs/ablation_smd.yaml [SWaT]=scripts/configs/ablation_swat.yaml)
declare -A LR=([PSM]=5e-5 [SMD]=5e-4 [SWaT]=5e-4)

# ---- 1) PCMCI+ priors on train_sub, once per entity (parallel over entity groups) ----
echo "[$(date '+%m-%d %H:%M')] priors start"
$PY scripts/precompute_priors.py --cfg ${CFG[PSM]} DATA.FIT_ON_TRAIN_SUB True SOLVER.BASE_LR 5e-5 > $OUT/prior_PSM.log 2>&1 &
$PY scripts/precompute_priors.py --cfg ${CFG[SWaT]} DATA.FIT_ON_TRAIN_SUB True SOLVER.BASE_LR 5e-4 > $OUT/prior_SWaT.log 2>&1 &
ENTS=($(ls data/SMD/*.npz | xargs -n1 basename | sed 's/\.npz//'))
for g in 0 1 2 3 4 5 6; do
  grp=$(for ((i=g; i<${#ENTS[@]}; i+=7)); do printf "%s," ${ENTS[$i]}; done | sed 's/,$//')
  $PY scripts/precompute_priors.py --cfg ${CFG[SMD]} DATA.FIT_ON_TRAIN_SUB True SOLVER.BASE_LR 5e-4 DATA.ENTITIES $grp > $OUT/prior_SMD_$g.log 2>&1 &
done
wait
echo "[$(date '+%m-%d %H:%M')] priors done"

# ---- 2) training queue: one job per (entity, seed) ----
JOBS=()
for s in 0 1 2 3; do JOBS+=("SWaT|swat|$s"); JOBS+=("PSM|PSM|$s"); done
for s in 0 1 2 3; do for e in "${ENTS[@]}"; do JOBS+=("SMD|$e|$s"); done; done
NGPU=4; NW=${NW:-12}
worker() {
  local w=$1 gpu=$(( $1 % NGPU ))
  for ((i=w; i<${#JOBS[@]}; i+=NW)); do
    IFS='|' read -r ds ent seed <<< "${JOBS[$i]}"
    local rd=$OUT/$ds/${ent}_seed$seed
    [ -f $rd/summary.csv ] && continue
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu start $ds/$ent seed$seed"
    CUDA_VISIBLE_DEVICES=$gpu $PY main.py --cfg ${CFG[$ds]} RESULT_DIR $rd RESULT_DIR_LITERAL True \
      SEEDS "[$seed]" DATA.ENTITIES $ent SOLVER.BASE_LR ${LR[$ds]} $COMMON > $rd.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu done  $ds/$ent seed$seed (exit $?)"
  done
}
mkdir -p $OUT/PSM $OUT/SMD $OUT/SWaT
for ((w=0; w<NW; w++)); do worker $w & done
wait
echo "=== hb done: $(date) ==="
