# Multi-server execution (campaign `cfval`)

Wrappers `scripts/servers/run_4gpu.sh` / `run_8gpu.sh` start **one launcher in one tmux session per server and phase**
using the already verified `scripts/run_experiments.py` (which calls `main.py` and `scripts/eval_ckpt.py`). Nothing else is
re-implemented. Each server owns a disjoint manifest so no training job is planned twice.

## Work split

| phase | server4 (`scripts/manifests/multiserver/*_server4.yaml`) | server8 (`*_server8.yaml`) |
|---|---|---|
| pilot | PSM seed 0; SMD machine-1-1 seed 0 | SWaT51 seed 0 |
| full (planning only) | PSM seeds 0-3; SMD machine-1-1 … machine-1-8 x seeds 0-3 (36 train jobs) | SWaT51 seeds 0-3 **first**, then SMD machine-2-1 … 2-9, machine-3-1 … 3-11 x seeds 0-3 (84 train jobs) |

Full manifests together: 30 prior + 120 train + 240 eval jobs, train-job intersection 0 (checked by `tests/test_server_wrappers.py`).
Queue order = manifest order, so on server8 the four SWaT jobs take GPUs first and SMD jobs fill the remaining GPUs.
Entity names are explicit in the manifests; do not use `entities: all` in the multiserver files.

Settings are read from `scripts/configs/{psm,smd,swat}_cf_val.yaml` unchanged: 80 epochs, `PERM_PAIRS_PER_BATCH: 0`,
`CALIBRATE: False`, `USE_COUNTERFACTUAL: True`, `SCORE_GAMMA: 1.0`, VAL split 0.2, `last.pt` + `best_val.pt`. The effective
learning rate is decided by `utils/parser.py` (PSM falls back to 5e-5 unless given on the CLI) and is recorded in each run's
`config.yaml`. Each checkpoint (last, best_val) is evaluated by `scripts/eval_ckpt.py --cf both --calibrate cfg` (CF OFF and ON
in one job). No DDP, no batch-size changes, no extra seeds: the wrapper only passes paths and the GPU list.

## Per-server setup

1. Clone the repository and check out the campaign commit (`PICAAD_CODE_SHA`). The wrapper compares HEAD with that SHA and
   refuses to run otherwise; it never pulls, merges or checks out.
2. Copy `configs/servers/server4.env.example` → `configs/servers/server4.env` (or `server8`), edit the absolute paths:
   `PICAAD_PYTHON`, `PICAAD_DATA_ROOT` (PSM/, SMD/, SWaT51/ NPZ; SWaT must have 51 channels — the config has `EXPECTED_N: 51`),
   `PICAAD_PRIOR_CACHE`, `PICAAD_OUT_ROOT` (**outside the checkout**, campaign/server specific, e.g. `/srv/picaad/runs/cfval/server8`),
   `PICAAD_LOCK_DIR`, `PICAAD_GPUS` (default 0,1,2,3 / 0..7), `PICAAD_CAMPAIGN`, `PICAAD_CODE_SHA`. `.env` files are git-ignored
   (`configs/servers/*.env`). CLI flags `--gpus/--out-root/--code-sha/--campaign/--env` override the file.
3. Environment check: `python -m unittest tests.test_launcher tests.test_server_wrappers` and
   `python -c "import torch; print(torch.cuda.device_count())"`.

## Commands

```bash
scripts/servers/run_8gpu.sh --phase pilot                 # dry-run (default): plan JSON only, no job, no cache/checkpoint output
scripts/servers/run_8gpu.sh --phase pilot --execute       # one tmux session: picaad_cfval_server8_pilot
scripts/servers/run_8gpu.sh --phase pilot --status        # persisted queue state
scripts/servers/run_8gpu.sh --phase pilot --execute --resume   # queue resume: completed jobs (matching SUCCESS.json) are skipped
tmux attach -t picaad_cfval_server8_pilot                 # watch; Ctrl-b d to detach
scripts/servers/run_4gpu.sh --phase full                  # planning dry-run only; --execute requires approval
```

`--resume` is a **queue resume**. The trainer has no resume-from-checkpoint; an interrupted training job restarts from scratch in a
new `attemptN` directory. Starting `--execute` while the session exists is refused (one launcher per server/phase). Stop a run by
attaching and pressing Ctrl-C (the launcher terminates only its own child processes), then use `--status`.

Logs: `$PICAAD_OUT_ROOT/_launcher/<session>.log` (tee of the launcher output; the launcher's own exit code is preserved),
per-job logs and `SUCCESS.json` under `$PICAAD_OUT_ROOT/<dataset>/<entity>/seed<k>/<config>/attemptN/` and `.../eval/<tag>/attemptN/`.

## Locks and duplicates

`PICAAD_LOCK_DIR` locks are per machine: they stop two launchers **on the same server** from using one GPU. They do **not** know
about the other server. Duplicate training across servers is prevented only by the disjoint manifests and by giving each server
its own out_root; never run the same full manifest on both machines.

## Not covered by this wrapper

Data, checkpoints, prior caches and the conda environment are not in the clone. The GPU probe was exercised on a 4-GPU machine
only (synthetic smoke, commit 30631d9); an 8-GPU machine has not been tested yet.

## Getting the code on another server (pinned execution worktree)

The launcher records the code identity and the wrappers refuse to run unless `HEAD == PICAAD_CODE_SHA`, so every server
should execute from a checkout pinned to the same commit. Keep that execution worktree separate from the publishing
worktree that `scripts/publish_results.sh` creates under `<out_root>/_publish/`.

```bash
# one-time clone (any branch), then fetch the campaign branch
git clone git@github.com:TiraminseoCake/CASAD.git /srv/picaad/src
cd /srv/picaad/src && git fetch origin integration/cfval-multiserver

# pinned, detached execution worktree for CODE_SHA (nothing is ever pulled or checked out inside it)
CODE_SHA=<commit reported for the campaign>
git worktree add --detach /srv/picaad/exec/cfval_${CODE_SHA:0:7} "$CODE_SHA"
cd /srv/picaad/exec/cfval_${CODE_SHA:0:7}
cp configs/servers/server8.env.example configs/servers/server8.env      # set PICAAD_CODE_SHA=$CODE_SHA and the absolute paths
python -m unittest tests.test_server_wrappers tests.test_export_publish tests.test_launcher
scripts/servers/run_8gpu.sh --phase pilot                               # dry-run
```

The publishing worktree is created automatically by `scripts/publish_results.sh --commit` (branch
`results/<campaign>/<server>`); do not run experiments from it.

## Preflight and synthetic smoke on the 8-GPU server

The hardware of the 8-GPU machine (GPU model, VRAM, CPU, RAM, CUDA/driver) is not assumed here; record it there:

```bash
/usr/bin/nvidia-smi --query-gpu=index,uuid,name,memory.total,driver_version --format=csv,noheader
nproc; free -g | head -2; python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.device_count())"
python -c "import numpy as np; d=np.load('<data_root>/SWaT51/swat.npz'); print({k: d[k].shape for k in d.files})"   # must be N=51
```

Synthetic two-GPU smoke through the launcher (no benchmark data, config unchanged, ~1 minute):

```bash
S=/srv/picaad/runs/smoke_$(git rev-parse --short HEAD); mkdir -p $S/data/SYN $S/cache $S/out $S/locks
python -c "from tests.test_phase1b_val_trainer import _synth_npz; _synth_npz('$S/data/SYN/synthA.npz'); _synth_npz('$S/data/SYN/synthB.npz')"
cat > $S/gpu_smoke.yaml <<'YAML'
name: gpu_smoke
defaults: {threads_per_job: 4, prior_workers: 2, eval: {ckpt_tags: [last, best_val], cf: both, calibrate: cfg, verify_native_parity: true}}
train:
  - {dataset: PSM, config: scripts/configs/psm_cf_val.yaml, input_dir: SYN, entities: [synthA, synthB], seeds: [0], epochs: 6, expected_n: 6}
YAML
python scripts/run_experiments.py --manifest $S/gpu_smoke.yaml --gpus 0,1 --python "$(which python)" \
    --data_root $S/data --prior_cache_dir $S/cache --out_root $S/out --lock_dir $S/locks --poll_seconds 1
python scripts/run_experiments.py --manifest $S/gpu_smoke.yaml --out_root $S/out --status     # 8 jobs, one per GPU at a time
```

Expected: `queue.json` shows the two training jobs on two different GPU UUIDs with overlapping intervals, four eval jobs
with `native_parity` all true in their `provenance.json`, and a second run with `--resume` skipping all six train/eval jobs.
Keep `$S` as the smoke record for that machine.
