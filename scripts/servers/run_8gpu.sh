#!/usr/bin/env bash
# 8-GPU server wrapper: one tmux session runs one launcher for one phase.
#   scripts/servers/run_8gpu.sh --phase pilot            # dry-run (default)
#   scripts/servers/run_8gpu.sh --phase pilot --execute  # start in tmux (session picaad_<campaign>_server8_pilot)
#   scripts/servers/run_8gpu.sh --phase pilot --status
#   scripts/servers/run_8gpu.sh --phase pilot --execute --resume   # queue resume (not training resume)
set -Eeuo pipefail
SERVER=server8
DEFAULT_GPUS=0,1,2,3,4,5,6,7
# shellcheck source=common.sh
. "$(dirname -- "${BASH_SOURCE[0]}")/common.sh"
picaad_main 8 "$@"
