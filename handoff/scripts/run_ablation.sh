#!/usr/bin/env bash
# Thin wrapper (outside the checkout) for the js/server8 loss ablations. Uses scripts/run_experiments.py unchanged,
# the server8.env interpreter/data/cache/lock paths, and a campaign-specific out_root. One tmux session per campaign.
#   run_ablation.sh nocstruct|noprior|noalign [--dry-run(default)|--execute|--status] [--resume]
set -Eeuo pipefail
TAG="${1:?nocstruct|noprior|noalign|psmcrs}"; shift
case "$TAG" in nocstruct|noprior|noalign|psmcrs) ;; *) echo "[abl] unknown ablation $TAG" >&2; exit 2;; esac
ENV_FILE=<BOOTSTRAP>/server8/server8.env
AB=<BOOTSTRAP>/server8/ablation
MANIFEST=$AB/manifest_${TAG}_server8.yaml
REPO=<REPO>
MODE=dry-run; RESUME=0; NO_TMUX=0
for a in "$@"; do case "$a" in --dry-run) MODE=dry-run;; --execute) MODE=execute;; --status) MODE=status;; --resume) RESUME=1;; --no-tmux) NO_TMUX=1;; *) echo "[abl] unknown argument: $a" >&2; exit 2;; esac; done
[ "$RESUME" = 1 ] && [ "$MODE" != execute ] && { echo "[abl] --resume only with --execute" >&2; exit 2; }
set -a; . "$ENV_FILE"; set +a
CAMPAIGN="cfval_abl_${TAG}"; PY="$PICAAD_PYTHON"; OUT="<RUNS>/${CAMPAIGN}/server8"
LOCK="${PICAAD_LOCK_DIR:-<LOCKDIR>}"; GPUS="${PICAAD_GPUS:-0,1,2,3,4,5,6,7}"
SESSION="picaad_${CAMPAIGN}_server8"; QNAME="${CAMPAIGN}_server8"
HEAD="$(git -C "$REPO" rev-parse HEAD)"
[ "$HEAD" = "$PICAAD_CODE_SHA" ] || { echo "[abl] HEAD $HEAD != PICAAD_CODE_SHA $PICAAD_CODE_SHA" >&2; exit 2; }
[ -n "$(git -C "$REPO" status --porcelain --untracked-files=no)" ] && echo "[abl] WARNING: tracked files modified in $REPO" >&2
CMD=( "$PY" "$REPO/scripts/run_experiments.py" --manifest "$MANIFEST" --gpus "$GPUS" --python "$PY" --data_root "$PICAAD_DATA_ROOT"
      --out_root "$OUT" --lock_dir "$LOCK" --threads_per_job "${PICAAD_THREADS_PER_JOB:-4}" --dataloader_workers "${PICAAD_DATALOADER_WORKERS:-0}"
      --prior_workers "${PICAAD_PRIOR_WORKERS:-2}" )
[ -n "${PICAAD_PRIOR_CACHE:-}" ] && CMD+=( --prior_cache_dir "$PICAAD_PRIOR_CACHE" )
case "$MODE" in dry-run) CMD+=( --dry-run );; status) CMD+=( --status );; execute) [ "$RESUME" = 1 ] && CMD+=( --resume );; esac
LOG="$OUT/_launcher/${SESSION}.log"; mkdir -p "$OUT/_launcher"
cat <<PLAN
[abl] campaign=$CAMPAIGN server=server8 (display js) mode=$MODE resume=$RESUME queue=$QNAME session=$SESSION
[abl] repo=$REPO HEAD=$HEAD env=$ENV_FILE manifest=$MANIFEST
[abl] python=$PY data_root=$PICAAD_DATA_ROOT prior_cache=${PICAAD_PRIOR_CACHE:-<cfg>} out_root=$OUT lock_dir=$LOCK (shared) gpus=$GPUS
[abl] launcher: $(printf '%q ' "${CMD[@]}")
PLAN
run_fg() { local log="$1"; set +e; "${CMD[@]}" 2>&1 | tee -a "$log"; local rc=${PIPESTATUS[0]}; set -e; return "$rc"; }
case "$MODE" in
  dry-run|status) run_fg "$OUT/_launcher/${SESSION}.${MODE}.log" ;;
  execute)
    if [ "$NO_TMUX" = 1 ]; then run_fg "$LOG"; else
      command -v tmux >/dev/null 2>&1 || { echo "[abl] tmux not found" >&2; exit 2; }
      tmux has-session -t "$SESSION" 2>/dev/null && { echo "[abl] tmux session '$SESSION' already exists: one launcher per campaign." >&2; exit 2; }
      if [ -f "$OUT/_launcher/$QNAME/queue.json" ] && [ "$RESUME" = 0 ]; then echo "[abl] queue '$QNAME' already created; use --status or --execute --resume" >&2; exit 2; fi
      inner="$(printf '%q ' "$0" "$TAG" --execute --no-tmux)"; [ "$RESUME" = 1 ] && inner="$inner --resume"
      tmux new-session -d -s "$SESSION" -c "$REPO" "bash -lc $(printf '%q' "$inner; rc=\$?; echo \"[abl] launcher exited rc=\$rc\" | tee -a $(printf '%q' "$LOG"); exit \$rc")"
      echo "[abl] started tmux session '$SESSION' (attach: tmux attach -t $SESSION; log: $LOG)"
    fi ;;
esac
