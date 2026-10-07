#!/usr/bin/env bash
# Publish one campaign's results package on branch results/<campaign>/server8, with the bootstrap-path
# redaction that scripts/export_results.py misses (df.to_csv at export_results.py:226 is not redacted).
# Pinned execution code is never modified. Commits only; never pushes.
#   publish_redacted.sh <campaign> [--dry-run|--commit]
set -Eeuo pipefail
CAMP="${1:?campaign, e.g. cfval_abl_psmcrs}"; MODE="${2:---dry-run}"
ENV_FILE=<BOOTSTRAP>/server8/server8.env
set -a; . "$ENV_FILE"; set +a
REPO=<REPO>
OUT=<RUNS>/${CAMP}/server8
BRANCH="results/${CAMP}/server8"
WT="$OUT/_publish/worktree_${CAMP}_server8"
PY="$PICAAD_PYTHON"
BOOT=<BOOTSTRAP>
EXEC_HEAD="$(git -C "$REPO" rev-parse HEAD)"
[ -d "$OUT" ] || { echo "[pub] out_root missing: $OUT" >&2; exit 2; }

# ---- publishing worktree (execution checkout untouched) ----
mkdir -p "$(dirname "$WT")"
git -C "$REPO" fetch origin --prune >/dev/null 2>&1 || echo "[pub] WARNING: fetch failed (offline?)" >&2
REF="refs/remotes/origin/$BRANCH"
if [ ! -e "$WT/.git" ]; then
  if git -C "$REPO" show-ref --verify --quiet "$REF"; then
    git -C "$REPO" worktree add -B "$BRANCH" "$WT" "$REF" >/dev/null
  elif git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git -C "$REPO" worktree add "$WT" "$BRANCH" >/dev/null
  else
    git -C "$REPO" worktree add -b "$BRANCH" "$WT" "$EXEC_HEAD" >/dev/null
    echo "[pub] new branch $BRANCH from execution HEAD $EXEC_HEAD" >&2
  fi
fi
[ "$(git -C "$WT" rev-parse --abbrev-ref HEAD)" = "$BRANCH" ] || { echo "[pub] worktree not on $BRANCH" >&2; exit 2; }
if git -C "$REPO" show-ref --verify --quiet "$REF"; then
  git -C "$WT" merge-base --is-ancestor "$REF" HEAD || { echo "[pub] remote $BRANCH ahead/diverged; resolve manually (no force)" >&2; exit 2; }
fi
[ -z "$(git -C "$WT" status --porcelain --untracked-files=no)" ] || { echo "[pub] worktree has uncommitted tracked changes" >&2; exit 2; }

# ---- export ----
"$PY" "$REPO/scripts/export_results.py" export --out_root "$OUT" --campaign "$CAMP" --server server8 \
  --reports_root "$WT/reports/experiments" --data_root "$PICAAD_DATA_ROOT" --prior_cache_dir "$PICAAD_PRIOR_CACHE" \
  --redact_prefix "$BOOT" >/dev/null
PKG="$(ls -d "$WT/reports/experiments/$CAMP/server8"/*/ | head -1)"; PKG="${PKG%/}"
REL="reports/experiments/$CAMP/server8/$(basename "$PKG")"

# ---- post-redaction the export tool misses (metrics.csv / yaml keys / manifest warning list) ----
"$PY" - "$PKG" "$BOOT" <<'PYEOF'
import json, re, sys, pathlib
pkg, boot = pathlib.Path(sys.argv[1]), sys.argv[2]
ABS = re.compile(r'(?<![\w<>])/(?:mnt|srv|data|scratch|opt|home|Users|tmp|var|media)/[^\s"\'<>,]+')
for f in pkg.iterdir():
    if f.name == 'run_manifest.json':
        continue
    t = f.read_text()
    n = t.replace(boot, '<BOOTSTRAP>')
    n = re.sub(r'/(?:home|Users)/[^/\s"\',]+', '<HOME>', n)
    if n != t:
        f.write_text(n)
m = json.loads((pkg / 'run_manifest.json').read_text())
m.pop('redaction_warnings', None)
s = json.dumps(m, indent=1, default=str).replace(boot, '<BOOTSTRAP>')
s = re.sub(r'/(?:home|Users)/[^/\s"\',]+', '<HOME>', s)
(pkg / 'run_manifest.json').write_text(s)
leaks = sorted({x for f in pkg.iterdir() for x in ABS.findall(f.read_text())})
if leaks:
    print('[pub] LEAK after post-redaction:', leaks[:5], file=sys.stderr); sys.exit(3)
m2 = json.loads((pkg / 'run_manifest.json').read_text())
print(f"[pub] package ok  complete={m2['complete']}  jobs={m2['job_counts']}  leaks=0")
PYEOF

TRAIN_SHA="$("$PY" -c "import json,sys;print(','.join(json.load(open(sys.argv[1]))['training_code_sha']) or 'n/a')" "$PKG/run_manifest.json")"
COMPLETE="$("$PY" -c "import json,sys;print(json.load(open(sys.argv[1]))['complete'])" "$PKG/run_manifest.json")"
echo "[pub] campaign=$CAMP branch=$BRANCH pkg=$REL train_sha=$TRAIN_SHA complete=$COMPLETE"
if [ "$MODE" != "--commit" ]; then
  echo "[pub] dry-run: files staged nowhere. package contents:"; find "$PKG" -type f | sed "s#^$WT/#  #"
  exit 0
fi
git -C "$WT" add -- "$REL"
git -C "$WT" diff --cached --name-only | grep -v "^$REL/" && { echo "[pub] unexpected staged paths" >&2; exit 2; }
if git -C "$WT" diff --cached --quiet; then echo "[pub] nothing new to commit"; else
  git -C "$WT" commit -q -m "results($CAMP/server8): $(basename "$PKG") [training code $TRAIN_SHA; complete=$COMPLETE]" \
    -m "Exported by scripts/export_results.py from server8 (js), then bootstrap paths redacted to <BOOTSTRAP>/<HOME> (export_results.py:226 does not redact metrics.csv). Checkpoints, scores.npz, data NPZ and logs are excluded by the export tool. Publishing commit != training commit ($TRAIN_SHA). Execution checkout HEAD at export: $EXEC_HEAD." \
    -m "Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
  echo "[pub] committed $(git -C "$WT" rev-parse --short HEAD) on $BRANCH"
fi
[ "$(git -C "$REPO" rev-parse HEAD)" = "$EXEC_HEAD" ] || { echo "[pub] execution HEAD changed!" >&2; exit 2; }
