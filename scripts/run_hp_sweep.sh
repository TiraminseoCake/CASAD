#!/bin/bash
# PSM hyperparameter sweep: 4 configs × 1 seed, 1 GPU each
export PATH="/home/mschae/.conda/envs/oraclead/bin:$PATH"
cd /home/mschae/CASAD

OUT_ROOT="results/parallel/psm_hp_sweep_$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT_ROOT"

echo "=== PSM HP Sweep ==="
echo "Output: $OUT_ROOT"
echo ""

# Config A: L=20, d=64, tau=5
echo "[A] L=20 d=64 tau=5 lag=5 lr=1e-4"
CUDA_VISIBLE_DEVICES=0 python -u main.py \
    --cfg scripts/configs/psm_hp_a.yaml \
    SEEDS "[0]" DATA.ENTITIES PSM \
    RESULT_DIR "$OUT_ROOT/hp_a" RESULT_DIR_LITERAL True \
    > "$OUT_ROOT/hp_a.log" 2>&1 &
PID_A=$!

# Config B: L=20, d=128, tau=10, heads=8
echo "[B] L=20 d=128 tau=10 lag=5 lr=1e-4"
CUDA_VISIBLE_DEVICES=1 python -u main.py \
    --cfg scripts/configs/psm_hp_b.yaml \
    SEEDS "[0]" DATA.ENTITIES PSM \
    RESULT_DIR "$OUT_ROOT/hp_b" RESULT_DIR_LITERAL True \
    > "$OUT_ROOT/hp_b.log" 2>&1 &
PID_B=$!

# Config C: L=30, d=128, tau=10, lag=10, heads=8
echo "[C] L=30 d=128 tau=10 lag=10 lr=1e-4"
CUDA_VISIBLE_DEVICES=2 python -u main.py \
    --cfg scripts/configs/psm_hp_c.yaml \
    SEEDS "[0]" DATA.ENTITIES PSM \
    RESULT_DIR "$OUT_ROOT/hp_c" RESULT_DIR_LITERAL True \
    > "$OUT_ROOT/hp_c.log" 2>&1 &
PID_C=$!

# Config D: L=20, d=128, tau=5, lag=10, lr=3e-4, heads=8
echo "[D] L=20 d=128 tau=5 lag=10 lr=3e-4"
CUDA_VISIBLE_DEVICES=3 python -u main.py \
    --cfg scripts/configs/psm_hp_d.yaml \
    SEEDS "[0]" DATA.ENTITIES PSM \
    RESULT_DIR "$OUT_ROOT/hp_d" RESULT_DIR_LITERAL True \
    > "$OUT_ROOT/hp_d.log" 2>&1 &
PID_D=$!

echo ""
echo "PIDs: A=$PID_A B=$PID_B C=$PID_C D=$PID_D"
echo "Waiting for all to finish..."
wait $PID_A $PID_B $PID_C $PID_D
echo ""
echo "=== All done ==="

# Print results summary
echo ""
echo "=== Results ==="
for cfg in a b c d; do
    echo "--- Config ${cfg^^} ---"
    grep -E "seed 0.*A-PR=|seed 0.*F1=" "$OUT_ROOT/hp_${cfg}.log" | tail -1
done
