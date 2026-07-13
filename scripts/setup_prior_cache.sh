#!/usr/bin/env bash
# Populate data/prior_cache/ from the pretrained_priors/ directory shipped
# with the repo, so run_all.sh / run_all_gat.sh can cache-hit on the
# CPU-heavy PCMCI+ prior computation.
#
# Each cache file is keyed by a hash that includes the raw training tensor
# bytes (see model/build.py _prior_cache_key). If the user's data_npz/*.npz
# files match the ones the priors were computed on, this transfer works.
# Otherwise the first training run will just recompute (and overwrite) the
# stale cache entry.
#
# Usage:
#   bash scripts/setup_prior_cache.sh
#   FORCE=1 bash scripts/setup_prior_cache.sh   # overwrite existing cache

set -u
FORCE="${FORCE:-0}"

cd "$(dirname "$0")/.."

SRC_DIR="pretrained_priors"
DST_DIR="data/prior_cache"

if [ ! -d "${SRC_DIR}" ]; then
    echo "[setup_prior_cache] ${SRC_DIR} not found; nothing to copy." >&2
    exit 1
fi

n_src=$(find "${SRC_DIR}" -maxdepth 1 -name '*.npz' | wc -l)
if [ "${n_src}" -eq 0 ]; then
    echo "[setup_prior_cache] no .npz files under ${SRC_DIR}." >&2
    exit 1
fi

mkdir -p "${DST_DIR}"

copied=0
skipped=0
overwrote=0

for src in "${SRC_DIR}"/*.npz; do
    name=$(basename "${src}")
    dst="${DST_DIR}/${name}"
    if [ -e "${dst}" ]; then
        if [ "${FORCE}" -eq 1 ]; then
            cp "${src}" "${dst}"
            overwrote=$((overwrote + 1))
        else
            skipped=$((skipped + 1))
        fi
    else
        cp "${src}" "${dst}"
        copied=$((copied + 1))
    fi
done

echo "[setup_prior_cache] source: ${SRC_DIR}  (${n_src} files)"
echo "[setup_prior_cache] target: ${DST_DIR}"
echo "  copied:    ${copied}"
echo "  skipped:   ${skipped}    (set FORCE=1 to overwrite)"
if [ "${FORCE}" -eq 1 ]; then
    echo "  overwrote: ${overwrote}"
fi
