#!/usr/bin/env bash
# Export a server's completed results into reports/experiments/<campaign>/<server>/<run_id>/ inside a SEPARATE
# publishing worktree on branch results/<campaign>/<server>, and optionally commit / push it.
#   scripts/publish_results.sh --campaign cfval --server server4 --out_root /srv/picaad/runs/cfval/server4            # export + dry-run (default)
#   scripts/publish_results.sh ... --commit                                                                            # commit in the publishing worktree
#   scripts/publish_results.sh ... --commit --push                                                                     # and push (never force)
# The execution checkout is never modified (HEAD, index, working tree); only the publishing worktree changes.
set -Eeuo pipefail

die() { echo "[publish] ERROR: $*" >&2; exit 2; }
log() { echo "[publish] $*" >&2; }

CAMPAIGN="" SERVER="" OUT_ROOT="" RUN_ID="" DO_COMMIT=0 DO_PUSH=0 REMOTE="${PICAAD_REMOTE:-origin}" PY="${PICAAD_PYTHON:-python}"
WORKTREE_ROOT="" DATA_ROOT="${PICAAD_DATA_ROOT:-}" PRIOR_CACHE="${PICAAD_PRIOR_CACHE:-}" QUEUE_NAME="" REDACT=() FAIL_ON_LEAK=1
while [ $# -gt 0 ]; do
  case "$1" in
    --campaign) CAMPAIGN="$2"; shift 2 ;; --server) SERVER="$2"; shift 2 ;; --out_root) OUT_ROOT="$2"; shift 2 ;;
    --run_id) RUN_ID="$2"; shift 2 ;; --queue_name) QUEUE_NAME="$2"; shift 2 ;;
    --commit) DO_COMMIT=1; shift ;; --push) DO_PUSH=1; shift ;; --remote) REMOTE="$2"; shift 2 ;;
    --python) PY="$2"; shift 2 ;; --worktree_root) WORKTREE_ROOT="$2"; shift 2 ;;
    --data_root) DATA_ROOT="$2"; shift 2 ;; --prior_cache_dir) PRIOR_CACHE="$2"; shift 2 ;;
    --redact_prefix) REDACT+=( "$2" ); shift 2 ;; --allow_leak) FAIL_ON_LEAK=0; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done
[ -n "$CAMPAIGN" ] && [ -n "$SERVER" ] && [ -n "$OUT_ROOT" ] || die "--campaign, --server and --out_root are required"
case "$SERVER" in server4|server8) ;; *) die "--server must be server4 or server8" ;; esac
[ "$DO_PUSH" = 1 ] && [ "$DO_COMMIT" = 0 ] && die "--push requires --commit"
REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
[ -d "$OUT_ROOT" ] || die "out_root not found: $OUT_ROOT"
BRANCH="results/${CAMPAIGN}/${SERVER}"
WORKTREE_ROOT="${WORKTREE_ROOT:-$OUT_ROOT/_publish}"
WT="$WORKTREE_ROOT/worktree_${CAMPAIGN}_${SERVER}"
EXEC_HEAD="$(git -C "$REPO" rev-parse HEAD)"

export_args=( export --out_root "$OUT_ROOT" --campaign "$CAMPAIGN" --server "$SERVER" )
[ -n "$RUN_ID" ] && export_args+=( --run_id "$RUN_ID" ); [ -n "$QUEUE_NAME" ] && export_args+=( --queue_name "$QUEUE_NAME" )
[ -n "$DATA_ROOT" ] && export_args+=( --data_root "$DATA_ROOT" ); [ -n "$PRIOR_CACHE" ] && export_args+=( --prior_cache_dir "$PRIOR_CACHE" )
for r in "${REDACT[@]:-}"; do [ -n "$r" ] && export_args+=( --redact_prefix "$r" ); done
[ "$FAIL_ON_LEAK" = 1 ] && export_args+=( --fail_on_leak )

if [ "$DO_COMMIT" = 0 ]; then
  STAGE="$WORKTREE_ROOT/dryrun_$(date +%Y%m%d-%H%M%S)"; mkdir -p "$STAGE"
  log "dry-run: exporting to $STAGE (no git operation; use --commit to publish on branch $BRANCH)"
  "$PY" "$REPO/scripts/export_results.py" "${export_args[@]}" --reports_root "$STAGE/reports/experiments"
  log "would stage: reports/experiments/$CAMPAIGN/$SERVER/<run_id>/{metrics.csv,run_manifest.json,config_resolved.yaml,provenance_summary.json,artifacts.json,summary.md}"
  find "$STAGE" -type f | sed "s#^$STAGE/#  #"
  exit 0
fi

# ---- publishing worktree (execution checkout untouched) ----
mkdir -p "$WORKTREE_ROOT"
git -C "$REPO" fetch "$REMOTE" --prune >/dev/null 2>&1 || log "WARNING: fetch from $REMOTE failed (offline?); continuing with local refs"
REMOTE_REF="refs/remotes/$REMOTE/$BRANCH"
if [ ! -d "$WT/.git" ] && [ ! -f "$WT/.git" ]; then
  if git -C "$REPO" show-ref --verify --quiet "$REMOTE_REF"; then
    git -C "$REPO" worktree add -B "$BRANCH" "$WT" "$REMOTE_REF" >/dev/null 2>&1 || die "cannot create worktree $WT from $REMOTE_REF"
    log "worktree $WT tracking $REMOTE/$BRANCH"
  elif git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git -C "$REPO" worktree add "$WT" "$BRANCH" >/dev/null 2>&1 || die "cannot create worktree $WT for existing local $BRANCH"
  else
    git -C "$REPO" worktree add -b "$BRANCH" "$WT" "$EXEC_HEAD" >/dev/null 2>&1 || die "cannot create worktree $WT (new branch $BRANCH from $EXEC_HEAD)"
    log "worktree $WT: new branch $BRANCH from execution HEAD $EXEC_HEAD"
  fi
fi
[ "$(git -C "$WT" rev-parse --abbrev-ref HEAD)" = "$BRANCH" ] || die "worktree $WT is not on $BRANCH"
if git -C "$REPO" show-ref --verify --quiet "$REMOTE_REF"; then
  # local branch must contain the remote tip; otherwise the remote is ahead / diverged -> stop
  if ! git -C "$WT" merge-base --is-ancestor "$REMOTE_REF" HEAD; then
    die "remote $REMOTE/$BRANCH ($(git -C "$WT" rev-parse --short "$REMOTE_REF")) is ahead of or diverged from local $BRANCH ($(git -C "$WT" rev-parse --short HEAD)); resolve manually (no force)"
  fi
fi
if [ -n "$(git -C "$WT" status --porcelain --untracked-files=no)" ]; then
  die "publishing worktree $WT has uncommitted tracked changes; resolve first"
fi

# ---- export into the worktree ----
"$PY" "$REPO/scripts/export_results.py" "${export_args[@]}" --reports_root "$WT/reports/experiments"
PKG_DIR="$(ls -d "$WT/reports/experiments/$CAMPAIGN/$SERVER"/*/ | head -1)"; [ -n "$RUN_ID" ] && PKG_DIR="$WT/reports/experiments/$CAMPAIGN/$SERVER/$RUN_ID"
REL="reports/experiments/$CAMPAIGN/$SERVER/$(basename -- "$PKG_DIR")"
[ -f "$WT/$REL/run_manifest.json" ] || die "export did not produce $REL/run_manifest.json"
TRAIN_SHA="$("$PY" -c "import json,sys; m=json.load(open(sys.argv[1])); print(','.join(m['training_code_sha']) or 'n/a')" "$WT/$REL/run_manifest.json")"
COMPLETE="$("$PY" -c "import json,sys; print(json.load(open(sys.argv[1]))['complete'])" "$WT/$REL/run_manifest.json")"

# stage ONLY the package path (never git add .)
git -C "$WT" add -- "$REL"
if git -C "$WT" diff --cached --quiet; then
  log "nothing new to commit for $REL (package content unchanged)"
else
  if git -C "$WT" diff --cached --name-only | grep -v "^$REL/"; then die "unexpected staged paths outside $REL"; fi
  git -C "$WT" commit -q -m "results($CAMPAIGN/$SERVER): $(basename -- "$PKG_DIR") [training code $TRAIN_SHA; complete=$COMPLETE]" \
    -m "Package exported by scripts/export_results.py from $SERVER. Publishing commit != training commit ($TRAIN_SHA). Execution checkout HEAD at export: $EXEC_HEAD." \
    -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
  log "committed $(git -C "$WT" rev-parse --short HEAD) on $BRANCH (worktree $WT); execution checkout HEAD unchanged: $(git -C "$REPO" rev-parse HEAD)"
fi
[ "$(git -C "$REPO" rev-parse HEAD)" = "$EXEC_HEAD" ] || die "execution checkout HEAD changed unexpectedly"

if [ "$DO_PUSH" = 1 ]; then
  if ! git -C "$WT" push "$REMOTE" "$BRANCH:$BRANCH"; then
    die "push of $BRANCH to $REMOTE rejected (remote ahead?); fetch and retry, never force"
  fi
  log "pushed $BRANCH to $REMOTE"
fi
