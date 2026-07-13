#!/usr/bin/env bash
# Detect free GPUs by combining "no other user's compute process" and
# "enough free memory". Prints comma-separated indices to stdout.
#
# By default a GPU is "free" iff:
#   1. no compute processes owned by users other than $USER are running on it, AND
#   2. free_memory >= FREE_MEM_THRESHOLD_MB
#
# Env vars:
#   FREE_MEM_THRESHOLD_MB   min free memory in MiB (default: 40000 = 40GB)
#   MAX_GPUS                cap the output to N GPUs (default: 0 = unlimited)
#   EXCLUDE_GPUS            comma-separated indices to never use (default: empty)
#   IGNORE_PROCESSES        1 = skip the "no other-user process" check, use
#                           memory threshold only (default: 0)
#   STRICT_UNKNOWN_OWNER    1 = if we cannot determine a process's owner
#                           (e.g. it just ended), assume other-user and mark
#                           the GPU as busy. Default: 1 (safe).
#   VERBOSE                 1 = print step-by-step decisions to stderr.
#
# Standalone usage:
#   bash scripts/detect_free_gpus.sh
#   MAX_GPUS=4 bash scripts/detect_free_gpus.sh
#   FREE_MEM_THRESHOLD_MB=30000 EXCLUDE_GPUS=0,7 bash scripts/detect_free_gpus.sh
#   VERBOSE=1 bash scripts/detect_free_gpus.sh    # <-- debug why a GPU was picked
#   IGNORE_PROCESSES=1 bash scripts/detect_free_gpus.sh

FREE_MEM_THRESHOLD_MB="${FREE_MEM_THRESHOLD_MB:-40000}"
MAX_GPUS="${MAX_GPUS:-0}"
EXCLUDE_GPUS="${EXCLUDE_GPUS:-}"
IGNORE_PROCESSES="${IGNORE_PROCESSES:-0}"
STRICT_UNKNOWN_OWNER="${STRICT_UNKNOWN_OWNER:-1}"
VERBOSE="${VERBOSE:-0}"

_log() {
    if [ "${VERBOSE}" -eq 1 ]; then
        echo "[detect] $*" >&2
    fi
}

MY_UID=$(id -u)
_log "self: USER=${USER}  UID=${MY_UID}"

# Prefer the actual binary path to avoid any shell alias (e.g. some setups
# alias `nvidia-smi` to `nvitop`, which does not accept --query-gpu).
NVSMI="/usr/bin/nvidia-smi"
if [ ! -x "${NVSMI}" ]; then
    # Fall back to unaliased lookup.
    NVSMI=$(command -v nvidia-smi 2>/dev/null || true)
fi
if [ -z "${NVSMI}" ] || [ ! -x "${NVSMI}" ]; then
    echo "[detect_free_gpus] nvidia-smi binary not found" >&2
    exit 1
fi

# Return the UID of a PID by reading /proc directly (survives race with `ps`).
# Falls back to `ps` if /proc is not available.
_pid_uid() {
    local pid="$1"
    if [ -e "/proc/${pid}" ]; then
        stat -c '%u' "/proc/${pid}" 2>/dev/null && return
    fi
    ps -o uid= -p "${pid}" 2>/dev/null | tr -d ' '
}

# Build a set of GPU indices that have compute processes owned by a *different*
# user than $USER. Those GPUs are considered "busy" regardless of free memory.
declare -A other_user_busy
if [ "${IGNORE_PROCESSES}" -eq 0 ]; then
    # `--query-compute-apps=gpu_uuid,pid` gives one line per process.
    # Map uuid → index via `--query-gpu=index,uuid`.
    declare -A uuid_to_idx
    while IFS=', ' read -r idx uuid; do
        [ -n "${idx}" ] && uuid_to_idx["${uuid}"]="${idx}"
    done < <("${NVSMI}" --query-gpu=index,uuid \
                        --format=csv,noheader,nounits 2>/dev/null)
    while IFS=', ' read -r uuid pid; do
        [ -z "${pid}" ] && continue
        gid="${uuid_to_idx[${uuid}]}"
        [ -z "${gid}" ] && continue

        # Look up the process owner. Compare by numeric UID to avoid docker
        # username mismatches (same UID, different name).
        uid=$(_pid_uid "${pid}")
        if [ -z "${uid}" ]; then
            # Process ended (race with nvidia-smi). Default: assume other user
            # (safer than picking a GPU that might immediately get re-taken).
            if [ "${STRICT_UNKNOWN_OWNER}" -eq 1 ]; then
                _log "gpu ${gid}: pid=${pid} owner unknown -> mark busy (STRICT)"
                other_user_busy["${gid}"]=1
            else
                _log "gpu ${gid}: pid=${pid} owner unknown -> skip (non-strict)"
            fi
        elif [ "${uid}" != "${MY_UID}" ]; then
            _log "gpu ${gid}: pid=${pid} owned by uid=${uid} (not ${MY_UID}) -> mark busy"
            other_user_busy["${gid}"]=1
        else
            _log "gpu ${gid}: pid=${pid} owned by me (uid=${uid}) -> ok"
        fi
    done < <("${NVSMI}" --query-compute-apps=gpu_uuid,pid \
                        --format=csv,noheader,nounits 2>/dev/null)
fi

# Query each GPU's free memory (MiB). Fields: index, memory.free
raw=$("${NVSMI}" --query-gpu=index,memory.free \
                  --format=csv,noheader,nounits 2>/dev/null)
if [ -z "${raw}" ]; then
    echo "[detect_free_gpus] nvidia-smi query returned empty" >&2
    exit 1
fi

# Turn EXCLUDE_GPUS "0,7" into an awk-friendly regex-safe set.
excl_pat=""
if [ -n "${EXCLUDE_GPUS}" ]; then
    excl_pat=$(echo "${EXCLUDE_GPUS}" | tr ',' '|')
fi

if [ "${VERBOSE}" -eq 1 ]; then
    _log "memory per GPU (free MiB):"
    echo "${raw}" | sed 's/^/[detect]   /' >&2
    _log "threshold: ${FREE_MEM_THRESHOLD_MB} MiB"
fi

# First filter by memory + user-provided exclusions.
mem_ok=$(echo "${raw}" | awk -F', ' \
    -v thresh="${FREE_MEM_THRESHOLD_MB}" \
    -v excl="${excl_pat}" \
    'BEGIN { split(excl, ex, "|"); for (k in ex) skip[ex[k]] = 1 }
     $2 + 0 >= thresh && !skip[$1] { print $1 }')
_log "GPUs passing memory+exclude filter: $(echo ${mem_ok} | tr '\n' ' ')"
_log "GPUs marked busy by other-user process: ${!other_user_busy[*]:-<none>}"

# Then drop any GPU busy with another user's process.
free_list=""
for g in ${mem_ok}; do
    if [ -z "${other_user_busy[${g}]:-}" ]; then
        free_list="${free_list}${g}
"
    else
        _log "gpu ${g}: dropped (busy by other user)"
    fi
done

if [ "${MAX_GPUS}" -gt 0 ]; then
    free_list=$(echo "${free_list}" | head -n "${MAX_GPUS}")
fi

# Join with commas, no trailing newline. Strip empty lines from the list.
echo "${free_list}" | sed '/^$/d' | paste -sd, -
