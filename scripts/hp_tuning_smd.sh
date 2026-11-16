#!/bin/bash
# SMD HP Tuning on CAROTS entities (machine-2-1, machine-3-7) — one-at-a-time sweep
# Baseline: LR=5e-4, BATCH=512, L=10, D=64, LAM_CAUSAL=1.0 -> results/ablation/smd_full (seeds 0,1)
# Each job: 1 entity x 1 seed, 100 epochs. 3 jobs per GPU x 4 GPUs = 12 workers.

cd /home/mschae/CASAD
PYTHON=/home/mschae/.conda/envs/oraclead/bin/python
CFG=scripts/configs/ablation_smd.yaml
OUTDIR=results/hp_tuning_smd
mkdir -p $OUTDIR
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8}
export MKL_NUM_THREADS=$OMP_NUM_THREADS
export OPENBLAS_NUM_THREADS=$OMP_NUM_THREADS

CONFIGS=(
  "lr5e-5|SOLVER.BASE_LR 5e-5"
  "lr1e-4|SOLVER.BASE_LR 1e-4"
  "lr1e-3|SOLVER.BASE_LR 1e-3"
  "bs128|SOLVER.BASE_LR 5e-4 TRAIN.BATCH_SIZE 128 TEST.BATCH_SIZE 128"
  "L20|SOLVER.BASE_LR 5e-4 PICAAD.L 20"
  "L50|SOLVER.BASE_LR 5e-4 PICAAD.L 50"
  "D32|SOLVER.BASE_LR 5e-4 PICAAD.D 32"
  "D128|SOLVER.BASE_LR 5e-4 PICAAD.D 128"
  "lamC0.5|SOLVER.BASE_LR 5e-4 PICAAD.LAM_CAUSAL 0.5"
  "lamC2.0|SOLVER.BASE_LR 5e-4 PICAAD.LAM_CAUSAL 2.0"
)
if [ -n "$ONLY" ]; then
  SEL=(); for c in "${CONFIGS[@]}"; do [[ " $ONLY " == *" ${c%%|*} "* ]] && SEL+=("$c"); done
  CONFIGS=("${SEL[@]}")
fi
ENTITIES=(machine-2-1 machine-3-7)
SEEDS=(0 1)
NWORKERS=${NWORKERS:-12}
NGPU=4

JOBS=()
for c in "${CONFIGS[@]}"; do for e in "${ENTITIES[@]}"; do for s in "${SEEDS[@]}"; do JOBS+=("$c|$e|$s"); done; done; done

run_worker() {
  local w=$1 gpu=$(( $1 % NGPU ))
  for ((i=w; i<${#JOBS[@]}; i+=NWORKERS)); do
    IFS='|' read -r name opts ent seed <<< "${JOBS[$i]}"
    local rd=$OUTDIR/smd_${name}_${ent}_seed${seed}
    [ -f $rd/summary.csv ] && { echo "skip $rd"; continue; }
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu start $rd"
    CUDA_VISIBLE_DEVICES=$gpu $PYTHON main.py --cfg $CFG \
      RESULT_DIR $rd RESULT_DIR_LITERAL True SEEDS "[$seed]" DATA.ENTITIES $ent $opts \
      > $rd.log 2>&1
    echo "[$(date '+%m-%d %H:%M')] GPU$gpu done  $rd (exit $?)"
  done
}

echo "=== SMD HP tuning: ${#JOBS[@]} jobs, $NWORKERS workers, $(date) ==="
for ((w=0; w<NWORKERS; w++)); do run_worker $w & done
wait
echo "=== all done: $(date) ==="
