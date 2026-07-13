#!/usr/bin/env bash
# Print everything detect_free_gpus.sh looks at, so we can figure out why a
# GPU was (or wasn't) picked. Run this on the machine that had the wrong
# result and paste the output back.
#
# Usage:
#   bash scripts/gpu_debug.sh

NVSMI="/usr/bin/nvidia-smi"
[ -x "${NVSMI}" ] || NVSMI=$(command -v nvidia-smi 2>/dev/null || true)

echo "=========================================="
echo "  GPU DEBUG SNAPSHOT"
echo "  host: $(hostname)   user: ${USER} (uid=$(id -u))   date: $(date +'%F %T')"
echo "=========================================="

echo
echo "--- [1] index → uuid ---"
"${NVSMI}" --query-gpu=index,uuid --format=csv,noheader,nounits

echo
echo "--- [2] memory (free / used / total, MiB) ---"
"${NVSMI}" --query-gpu=index,memory.free,memory.used,memory.total \
           --format=csv,noheader,nounits

echo
echo "--- [3] utilization ---"
"${NVSMI}" --query-gpu=index,utilization.gpu,utilization.memory \
           --format=csv,noheader,nounits

echo
echo "--- [4] compute processes (uuid, pid, name, used_mem_MiB) ---"
"${NVSMI}" --query-compute-apps=gpu_uuid,pid,process_name,used_memory \
           --format=csv,noheader,nounits

echo
echo "--- [5] process owners (via /proc first, ps fallback) ---"
while IFS=', ' read -r uuid pid _rest; do
    [ -z "${pid}" ] && continue
    if [ -e "/proc/${pid}" ]; then
        uid=$(stat -c '%u' "/proc/${pid}" 2>/dev/null)
        uname=$(stat -c '%U' "/proc/${pid}" 2>/dev/null)
        src="/proc"
    else
        uid=$(ps -o uid= -p "${pid}" 2>/dev/null | tr -d ' ')
        uname=$(ps -o user= -p "${pid}" 2>/dev/null | tr -d ' ')
        src="ps"
    fi
    echo "  uuid=${uuid}  pid=${pid}  uid=${uid:-?}  user=${uname:-?}  (source=${src})"
done < <("${NVSMI}" --query-compute-apps=gpu_uuid,pid \
                     --format=csv,noheader,nounits 2>/dev/null)

echo
echo "--- [6] detect_free_gpus.sh (VERBOSE=1) ---"
VERBOSE=1 bash "$(dirname "$0")/detect_free_gpus.sh"

echo
echo "--- [7] envs affecting decision ---"
for v in FREE_MEM_THRESHOLD_MB MAX_GPUS EXCLUDE_GPUS IGNORE_PROCESSES STRICT_UNKNOWN_OWNER; do
    printf "  %-24s = %s\n" "${v}" "${!v:-<unset>}"
done
