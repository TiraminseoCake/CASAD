#!/usr/bin/env bash
# Shared logic for the per-server tmux wrappers (scripts/servers/run_4gpu.sh, run_8gpu.sh).
# Reuses scripts/run_experiments.py (launcher) which in turn calls main.py and scripts/eval_ckpt.py.
# No training/eval logic lives here.
set -Eeuo pipefail

picaad_repo_root() { cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P; }

picaad_usage() {
  cat <<USAGE
Usage: $0 --phase pilot|full [--dry-run | --execute | --status] [--resume] [--env FILE] [--gpus LIST]
          [--campaign NAME] [--out-root DIR] [--code-sha SHA] [--no-tmux]
  --phase     pilot | full         (full is planning-only until approved)
  --dry-run   (default) expand the queue and write the plan JSON only; nothing runs
  --execute   start ONE launcher in ONE tmux session for this server/phase (refuses if the session exists)
  --status    print the persisted queue state of this server/phase
  --resume    with --execute: queue resume (skip jobs whose SUCCESS marker matches); NOT training resume
  --env FILE  server env file (default: configs/servers/\$SERVER.env, falls back to the .example with a warning)
  --gpus      override PICAAD_GPUS (comma-separated physical indices; never more than the server has)
  --no-tmux   run the launcher in the foreground instead of tmux (tests / debugging)
Environment (see configs/servers/*.env.example): PICAAD_PYTHON PICAAD_DATA_ROOT PICAAD_PRIOR_CACHE PICAAD_OUT_ROOT
  PICAAD_LOCK_DIR PICAAD_GPUS PICAAD_CAMPAIGN PICAAD_CODE_SHA PICAAD_THREADS_PER_JOB PICAAD_DATALOADER_WORKERS PICAAD_PRIOR_WORKERS
USAGE
}

picaad_die() { echo "[picaad-server] ERROR: $*" >&2; exit 2; }
picaad_log() { echo "[picaad-server] $*" >&2; }

# ---- argument parsing (sets globals) ----
picaad_parse_args() {
  PHASE="" MODE="dry-run" RESUME=0 ENV_FILE="" GPUS_CLI="" CAMPAIGN_CLI="" OUT_ROOT_CLI="" CODE_SHA_CLI="" NO_TMUX=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --phase) [ $# -ge 2 ] || picaad_die "--phase needs a value"; PHASE="$2"; shift 2 ;;
      --dry-run) MODE="dry-run"; shift ;;
      --execute) MODE="execute"; shift ;;
      --status) MODE="status"; shift ;;
      --resume) RESUME=1; shift ;;
      --env) [ $# -ge 2 ] || picaad_die "--env needs a value"; ENV_FILE="$2"; shift 2 ;;
      --gpus) [ $# -ge 2 ] || picaad_die "--gpus needs a value"; GPUS_CLI="$2"; shift 2 ;;
      --campaign) [ $# -ge 2 ] || picaad_die "--campaign needs a value"; CAMPAIGN_CLI="$2"; shift 2 ;;
      --out-root) [ $# -ge 2 ] || picaad_die "--out-root needs a value"; OUT_ROOT_CLI="$2"; shift 2 ;;
      --code-sha) [ $# -ge 2 ] || picaad_die "--code-sha needs a value"; CODE_SHA_CLI="$2"; shift 2 ;;
      --no-tmux) NO_TMUX=1; shift ;;
      -h|--help) picaad_usage; exit 0 ;;
      *) picaad_usage >&2; picaad_die "unknown argument: $1" ;;
    esac
  done
  case "$PHASE" in pilot|full) ;; *) picaad_usage >&2; picaad_die "--phase must be pilot or full" ;; esac
  if [ "$RESUME" = 1 ] && [ "$MODE" != "execute" ]; then picaad_die "--resume only applies together with --execute (queue resume, not training resume)"; fi
}

# ---- env loading: SERVER, DEFAULT_GPUS must be set by the caller ----
picaad_load_env() {
  REPO="$(picaad_repo_root)"
  local f="${ENV_FILE:-$REPO/configs/servers/${SERVER}.env}"
  if [ ! -f "$f" ]; then
    if [ -z "$ENV_FILE" ] && [ -f "$REPO/configs/servers/${SERVER}.env.example" ]; then
      picaad_log "WARNING: $f not found; using the .example file (edit and copy it before --execute)"
      f="$REPO/configs/servers/${SERVER}.env.example"
    else
      picaad_die "env file not found: $f"
    fi
  fi
  # shellcheck disable=SC1090
  set -a; . "$f"; set +a
  ENV_FILE_USED="$f"
  PYTHON="${PICAAD_PYTHON:-python}"
  DATA_ROOT="${PICAAD_DATA_ROOT:-}"; PRIOR_CACHE="${PICAAD_PRIOR_CACHE:-}"
  OUT_ROOT="${OUT_ROOT_CLI:-${PICAAD_OUT_ROOT:-}}"; LOCK_DIR="${PICAAD_LOCK_DIR:-/tmp/picaad_gpu_locks}"
  GPUS="${GPUS_CLI:-${PICAAD_GPUS:-$DEFAULT_GPUS}}"; CAMPAIGN="${CAMPAIGN_CLI:-${PICAAD_CAMPAIGN:-cfval}}"
  CODE_SHA="${CODE_SHA_CLI:-${PICAAD_CODE_SHA:-}}"
  THREADS="${PICAAD_THREADS_PER_JOB:-4}"; WORKERS="${PICAAD_DATALOADER_WORKERS:-0}"; PRIOR_WORKERS="${PICAAD_PRIOR_WORKERS:-1}"
  MANIFEST="$REPO/scripts/manifests/multiserver/${PHASE}_${SERVER}.yaml"
  [ -f "$MANIFEST" ] || picaad_die "manifest not found: $MANIFEST"
  SESSION="picaad_${CAMPAIGN}_${SERVER}_${PHASE}"
}

# ---- checks ----
picaad_check_gpus() {
  local max="$1" g
  IFS=',' read -r -a _gpus <<< "$GPUS"
  [ "${#_gpus[@]}" -ge 1 ] || picaad_die "empty GPU list"
  for g in "${_gpus[@]}"; do
    [[ "$g" =~ ^[0-9]+$ ]] || picaad_die "GPU entry '$g' is not a physical index"
    [ "$g" -lt "$max" ] || picaad_die "GPU index $g exceeds this server's range 0..$((max-1))"
  done
  [ "${#_gpus[@]}" -le "$max" ] || picaad_die "more GPUs listed than the server has ($max)"
}

picaad_check_paths() {
  [ -n "$DATA_ROOT" ] || picaad_die "PICAAD_DATA_ROOT is not set"
  [ -n "$OUT_ROOT" ] || picaad_die "PICAAD_OUT_ROOT is not set"
  case "$OUT_ROOT" in /*) ;; *) picaad_die "PICAAD_OUT_ROOT must be absolute: $OUT_ROOT" ;; esac
  # forbid output inside the Git checkout (results/ is now a tracked directory). Compare canonical paths on both
  # sides (readlink -m also canonicalises not-yet-existing leaves) and the literal path, so symlinked parents cannot hide it.
  local out_abs repo_abs
  out_abs="$(readlink -m -- "$OUT_ROOT" 2>/dev/null || printf '%s' "$OUT_ROOT")"; repo_abs="$(readlink -m -- "$REPO" 2>/dev/null || printf '%s' "$REPO")"
  case "$out_abs/" in "$repo_abs"/*|"$REPO"/*) picaad_die "PICAAD_OUT_ROOT ($out_abs) is inside the Git checkout ($repo_abs); use an external campaign/server path" ;; esac
  case "$OUT_ROOT/" in "$repo_abs"/*|"$REPO"/*) picaad_die "PICAAD_OUT_ROOT ($OUT_ROOT) is inside the Git checkout ($repo_abs); use an external campaign/server path" ;; esac
  case "$out_abs" in */"$CAMPAIGN"/*"$SERVER"*|*"$SERVER"*) ;; *) picaad_log "WARNING: out_root '$out_abs' does not mention server '$SERVER'; make sure servers do not share an out_root" ;; esac
  [ "$MODE" = "status" ] || [ -d "$DATA_ROOT" ] || picaad_die "PICAAD_DATA_ROOT does not exist: $DATA_ROOT"
}

picaad_check_code_sha() {
  local head; head="$(git -C "$REPO" rev-parse HEAD)"
  HEAD_SHA="$head"
  [ -n "$CODE_SHA" ] || picaad_die "PICAAD_CODE_SHA (or --code-sha) is required so every server runs the same commit"
  case "$head" in "$CODE_SHA"*) ;; *) picaad_die "HEAD $head does not match PICAAD_CODE_SHA $CODE_SHA (no pull/checkout is done by this wrapper)" ;; esac
  if [ -n "$(git -C "$REPO" status --porcelain --untracked-files=no)" ]; then
    picaad_log "WARNING: tracked files are modified in $REPO (launcher records the diff hash in every SUCCESS marker)"
  fi
}

# ---- launcher command (array; safe quoting) ----
picaad_build_launcher_cmd() {
  LAUNCHER_CMD=( "$PYTHON" "$REPO/scripts/run_experiments.py" --manifest "$MANIFEST" --gpus "$GPUS" --python "$PYTHON"
                 --data_root "$DATA_ROOT" --out_root "$OUT_ROOT" --lock_dir "$LOCK_DIR"
                 --threads_per_job "$THREADS" --dataloader_workers "$WORKERS" --prior_workers "$PRIOR_WORKERS" )
  [ -n "$PRIOR_CACHE" ] && LAUNCHER_CMD+=( --prior_cache_dir "$PRIOR_CACHE" )
  case "$MODE" in
    dry-run) LAUNCHER_CMD+=( --dry-run ) ;;
    status)  LAUNCHER_CMD+=( --status ) ;;
    execute) [ "$RESUME" = 1 ] && LAUNCHER_CMD+=( --resume ) ;;
  esac
  # test hook: PICAAD_LAUNCHER_OVERRIDE replaces "python run_experiments.py" (used by tests/test_server_wrappers.py)
  if [ -n "${PICAAD_LAUNCHER_OVERRIDE:-}" ]; then LAUNCHER_CMD=( "$PICAAD_LAUNCHER_OVERRIDE" "${LAUNCHER_CMD[@]:2}" ); fi
}

picaad_print_plan() {
  cat <<PLAN
[picaad-server] server=$SERVER phase=$PHASE mode=$MODE resume=$RESUME campaign=$CAMPAIGN
[picaad-server] repo=$REPO HEAD=$HEAD_SHA (PICAAD_CODE_SHA=$CODE_SHA) env=$ENV_FILE_USED
[picaad-server] manifest=$MANIFEST
[picaad-server] gpus=$GPUS (one job per GPU; no DDP; batch size and seeds come from the configs/manifest only)
[picaad-server] python=$PYTHON data_root=$DATA_ROOT prior_cache=${PRIOR_CACHE:-<config default>} out_root=$OUT_ROOT lock_dir=$LOCK_DIR
[picaad-server] training settings are taken from scripts/configs/*_cf_val.yaml as-is (80 epochs, PERM_PAIRS_PER_BATCH=0, CALIBRATE=False,
[picaad-server]   USE_COUNTERFACTUAL=True, SCORE_GAMMA=1.0; effective LR is decided by utils/parser.py, see run dir config.yaml)
[picaad-server] eval: last.pt and best_val.pt each -> scripts/eval_ckpt.py --cf both --calibrate cfg
[picaad-server] tmux session=$SESSION  log=$OUT_ROOT/_launcher/${SESSION}.log
[picaad-server] launcher: $(printf '%q ' "${LAUNCHER_CMD[@]}")
PLAN
}

# run the launcher in the foreground; tee the log; return the launcher's own exit code
picaad_run_foreground() {
  local log="$1"; mkdir -p "$(dirname -- "$log")"
  set +e
  "${LAUNCHER_CMD[@]}" 2>&1 | tee -a "$log"
  local rc=${PIPESTATUS[0]}
  set -e
  return "$rc"
}

picaad_tmux_start() {
  local log="$OUT_ROOT/_launcher/${SESSION}.log"
  command -v tmux >/dev/null 2>&1 || picaad_die "tmux not found"
  if tmux has-session -t "$SESSION" 2>/dev/null; then
    picaad_die "tmux session '$SESSION' already exists on this machine: one launcher per server/phase. Use --status, or attach: tmux attach -t $SESSION"
  fi
  mkdir -p "$OUT_ROOT/_launcher"
  # Inner command re-enters this wrapper in foreground mode so quoting stays exact; exit code is preserved via PIPESTATUS.
  local inner; inner="$(printf '%q ' "$0" --phase "$PHASE" --execute --no-tmux --env "$ENV_FILE_USED" --gpus "$GPUS" --campaign "$CAMPAIGN" --out-root "$OUT_ROOT" --code-sha "$CODE_SHA")"
  [ "$RESUME" = 1 ] && inner="$inner --resume"
  tmux new-session -d -s "$SESSION" -c "$REPO" "bash -lc $(printf '%q' "$inner; rc=\$?; echo \"[picaad-server] launcher exited rc=\$rc\" | tee -a $(printf '%q' "$log"); exit \$rc")"
  picaad_log "started tmux session '$SESSION' (attach: tmux attach -t $SESSION; log: $log)"
}

# ---- entry used by run_4gpu.sh / run_8gpu.sh ----
picaad_main() {
  local max_gpus="$1"; shift
  picaad_parse_args "$@"
  picaad_load_env
  picaad_check_gpus "$max_gpus"
  picaad_check_paths
  picaad_check_code_sha
  picaad_build_launcher_cmd
  picaad_print_plan
  case "$MODE" in
    dry-run|status)
      picaad_run_foreground "$OUT_ROOT/_launcher/${SESSION}.${MODE}.log" ;;
    execute)
      if [ "$NO_TMUX" = 1 ]; then
        picaad_run_foreground "$OUT_ROOT/_launcher/${SESSION}.log"
      else
        picaad_tmux_start
      fi ;;
  esac
}
