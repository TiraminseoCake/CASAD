# Running PICAAD validation-protocol experiments on another server

This guide covers the multi-GPU launcher `scripts/run_experiments.py`, the training entry
point `main.py` (validation protocol, `VAL.ENABLE=True`) and the explicit evaluator
`scripts/eval_ckpt.py`. Everything below is based on the implemented CLIs; nothing else is
implied. A git clone gives you **code, configs, manifests, tests and the small pretrained
PCMCI+ priors only**. Data, checkpoints, results and the conda environment are *not* in the
repository and have to be provided per server.

Verification status (be explicit about what was and was not checked):

| Item | Status |
|---|---|
| Unit tests (validation split/prior cache, val trainer, evaluator raw + calibrated, launcher with mocked GPUs and CPU mock jobs) | pass, CPU only |
| VAL-off native regression against the Phase-0 golden (synthetic, CPU) | exact |
| Pilot / full manifest `--dry-run` | done (plan JSON only) |
| Launcher on real GPUs (nvidia-smi probe, per-child `CUDA_VISIBLE_DEVICES`, locks) | **synthetic smoke done at commit 30631d9 (2026-09-10)**: two 6-epoch synthetic training jobs ran concurrently on two RTX A6000 (GPU 0/1, one job per GPU, child `cuda:0`), followed by `eval_ckpt.py` last/best_val with CF OFF/ON; queue `--resume` skipped all completed jobs. Record: `/mnt/data/PICAAD/smoke/20260910_gpu_smoke_30631d9/` (`SMOKE_REPORT.md`, `queue_run1.json`, `monitor/nvidia_smi_samples.csv`). Not exercised on real GPUs: external-process avoidance, cross-launcher lock contention, `--gpus auto`, OOM (mocked tests only). |
| Benchmark training / test evaluation on PSM, SWaT51, SMD | not run |

---

## 1. Environment

* Python 3.11, PyTorch (CUDA build matching the server's driver), numpy, pandas, PyYAML,
  yacs, scikit-learn, tigramite (PCMCI+). The reference machine used `torch` with CUDA 12.x;
  record the versions you install in the run's provenance (the checkpoints and
  `provenance.json` store `torch_version`).
* Check:

```bash
python -c "import torch, numpy, pandas, yaml, yacs, sklearn, tigramite; print(torch.__version__, torch.cuda.is_available(), torch.cuda.device_count())"
/usr/bin/nvidia-smi --query-gpu=index,uuid,memory.used,memory.total --format=csv,noheader
python -m unittest tests.test_phase1a_split_prior tests.test_phase1b_val_trainer tests.test_phase2a_eval_ckpt tests.test_phase2b_eval_calibrated tests.test_launcher
```

The launcher calls `/usr/bin/nvidia-smi` (or the first `nvidia-smi` on `PATH`). Shell
aliases (e.g. `nvidia-smi` → `nvitop`) do not affect it.

## 2. Data layout

Entity NPZ files with keys `train [T,N]`, `test [T,N]`, `label [T]`:

```
<data_root>/PSM/PSM.npz
<data_root>/SMD/machine-1-1.npz ... machine-3-11.npz   (28 entities)
<data_root>/SWaT51/swat.npz                            # N must be 51
```

`<data_root>` defaults to `<repo>/data_npz` and is passed with `--data_root` (or
`PICAAD_DATA_ROOT`). Generate NPZ with `scripts/prep/` if you only have raw files.

**SWaT must have 51 channels.** `scripts/configs/swat_cf_val.yaml` sets
`DATA.EXPECTED_N: 51`; loading any other export (e.g. the old 44-variable file produced
before commit 1f299a6) fails with a `ValueError` and no automatic channel selection or
padding is done. Check a file with:

```bash
python -c "import numpy as np; d=np.load('<data_root>/SWaT51/swat.npz'); print({k: d[k].shape for k in d.files})"
```

Record the NPZ sha256 (`sha256sum <file>`) — evaluation provenance stores it and
`--resume` uses it as part of the job identity.

## 3. Paths and environment variables

| CLI | Env | Meaning | Default |
|---|---|---|---|
| `--python` | `PICAAD_PYTHON` | interpreter used for child jobs | `sys.executable` |
| `--data_root` | `PICAAD_DATA_ROOT` | root of the NPZ folders above | `<repo>/data_npz` |
| `--prior_cache_dir` | `PICAAD_PRIOR_CACHE` | PCMCI+ cache directory (`PICAAD.PRIOR.CACHE_DIR`) | config value `data/prior_cache` |
| `--out_root` | `PICAAD_OUT_ROOT` | root of all outputs and launcher state | `<repo>/results/experiments` |
| `--lock_dir` | `PICAAD_LOCK_DIR` | per-GPU lock files shared by all launchers on the machine | `<tmp>/picaad_gpu_locks` |

Use a `--prior_cache_dir` that all launchers on the server share: the cache is keyed by
data bytes + PCMCI settings + split identity, and concurrent builders of the same key are
serialized by a lock and published atomically.

Limits: `--threads_per_job` (OMP/MKL/OpenBLAS per child), `--dataloader_workers`
(`DATA_LOADER.NUM_WORKERS`), `--prior_workers` (concurrent CPU PCMCI+ jobs),
`--max_parallel`. Manifest `defaults:` provide the same knobs.

## 4. GPUs

* `--gpus auto`: every GPU visible to the launcher that has no compute process of another
  process (any owner), used memory ≤ `--gpu_busy_mem_mb` (default 1000 MiB) and no lock held
  by another launcher.
* `--gpus 0,2` (physical indices or UUIDs): restricted to those; if the launcher itself runs
  with `CUDA_VISIBLE_DEVICES=...`, the list must be inside that set or the launcher exits.
* One job per GPU; no DDP/DataParallel. Right before each launch the launcher re-queries
  `nvidia-smi`, then takes `<lock_dir>/gpu_<uuid>.lock`. The child receives
  `CUDA_VISIBLE_DEVICES=<physical token>` and therefore sees `cuda:0`; `queue.json` records
  the physical index/UUID and the child's logical device. A checkpoint's saved
  `cfg.VISIBLE_DEVICES` does not override this (main.py only applies it when the variable
  is unset).
* OOM is a job failure; batch size, precision and model settings are never changed
  automatically.

## 5. Manifests

* `scripts/manifests/pilot_cfval.yaml` — approved first scope: PSM seed 0, SWaT51 seed 0,
  SMD machine-1-1 seed 0 with `scripts/configs/{psm,smd,swat}_cf_val.yaml`
  (validation protocol, `PERM_PAIRS_PER_BATCH: 0`, `CALIBRATE: False`,
  `USE_COUNTERFACTUAL: True`). 12 jobs: 3 prior + 3 train + 6 eval.
* `scripts/manifests/full_cfval.yaml` — seeds 0–3 and all 28 SMD entities (390 jobs).
  It is written for planning; it is **not** approved for execution.
* `scripts/manifests/example_eval_only.yaml` — evaluate existing checkpoints only.

Epochs, learning rate, warmup and CF settings come from the referenced config files; the
manifest only sets `epochs:` if you explicitly want to override `SOLVER.MAX_EPOCH`. Note
that `utils/parser.py` applies a per-dataset LR fallback when `SOLVER.BASE_LR` is not given
on the command line (PSM: 5e-5), so the effective LR is what `config.yaml` in the run
directory shows.

## 6. Commands

```bash
# expand the queue, write <out_root>/_launcher/<name>/queue_dryrun.json, start nothing
python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --gpus auto --dry-run \
    --data_root /srv/data/picaad_npz --prior_cache_dir /srv/data/picaad_prior_cache --out_root /srv/results/picaad

# train -> eval (last.pt and best_val.pt, CF OFF/ON in one eval job, --calibrate cfg)
python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --gpus 0,1,2 \
    --data_root /srv/data/picaad_npz --prior_cache_dir /srv/data/picaad_prior_cache --out_root /srv/results/picaad

# queue state
python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --out_root /srv/results/picaad --status

# queue resume: skip jobs whose SUCCESS.json identity (config sha256, data sha256, code commit + tracked diff,
# python, options) matches; everything else runs again in a NEW attempt directory
python scripts/run_experiments.py --manifest scripts/manifests/pilot_cfval.yaml --gpus auto --resume \
    --data_root /srv/data/picaad_npz --prior_cache_dir /srv/data/picaad_prior_cache --out_root /srv/results/picaad

# eval-only (existing checkpoints; e.g. a colleague's native last-epoch checkpoint)
python scripts/run_experiments.py --manifest scripts/manifests/example_eval_only.yaml --gpus auto --data_root /srv/data/picaad_npz --out_root /srv/results/picaad
# or directly:
python scripts/eval_ckpt.py --ckpt /path/PSM_seed0_ep80.pt --data_input_dir /srv/data/picaad_npz/PSM --out_dir /srv/results/picaad/eval_only/psm_ep80/attempt1 --verify_native_parity
```

**`--resume` is queue resume, not training resume.** The trainer has no
resume-from-checkpoint support; an unfinished training job restarts from scratch in a new
`attemptN` directory. Completed jobs are skipped only when their identity matches.

Dry-run creates the launcher state directory and the plan JSON only; it creates no
experiment, cache or checkpoint output.

## 7. Outputs

```
<out_root>/<dataset>/<entity>/seed<k>/<config_stem>/attemptN/      # RESULT_DIR of main.py: config.yaml, *_val_metrics.csv,
                                                                    # ckpt/{entity}_seed{k}_{best_val,last}.pt, launcher_run.log, SUCCESS.json
<out_root>/<dataset>/<entity>/seed<k>/<config_stem>/eval/<tag>/attemptN/   # eval_ckpt --out_dir: metrics.csv, scores.npz, provenance.json,
                                                                           # config_resolved.yaml, SUCCESS.json
<out_root>/<dataset>/<entity>/seed<k>/<config_stem>/eval/<tag>/attemptN.log  # launcher log (kept outside --out_dir, which must be empty)
<out_root>/eval_only/<name>/attemptN/
<out_root>/_launcher/<manifest name>/queue.json | queue_dryrun.json | prior_logs/ | eval_summary_<ts>.csv
```

Failed attempts keep their partial output; nothing is overwritten. `eval_summary_*.csv`
is a plain concatenation of eval `metrics.csv` files (no selection by test metric).
Under `VAL.ENABLE=True` no test-set evaluation happens during training, `main._final_eval`
is not called and `scripts/aggregate_best_epoch.py` is not run.

## 8. Several servers

Do not run the same full manifest on two servers: attempt numbering and `SUCCESS.json` are
local to each `--out_root`, so both servers would train every job. Split the work
explicitly, one manifest per server, e.g. copy `full_cfval.yaml` and keep only a subset:

```yaml
# server A: full_cfval_serverA.yaml
train:
  - {dataset: PSM,  config: scripts/configs/psm_cf_val.yaml,  input_dir: PSM,    entities: [PSM],  seeds: [0, 1, 2, 3]}
  - {dataset: SWaT, config: scripts/configs/swat_cf_val.yaml, input_dir: SWaT51, entities: [swat], seeds: [0, 1], expected_n: 51}
# server B: full_cfval_serverB.yaml
train:
  - {dataset: SWaT, config: scripts/configs/swat_cf_val.yaml, input_dir: SWaT51, entities: [swat], seeds: [2, 3], expected_n: 51}
  - {dataset: SMD,  config: scripts/configs/smd_cf_val.yaml,  input_dir: SMD,    entities: [machine-1-1, machine-1-2, ...], seeds: [0, 1, 2, 3]}
```

Give each manifest a distinct `name:` (it names the state directory). On one server, two
launchers may run concurrently only with the same `--lock_dir`; they then never assign the
same GPU. Merge results afterwards by copying the `<out_root>/<dataset>/...` trees; every
`provenance.json` carries the checkpoint sha256, data sha256, code commit and GPU used.

## 9. What is not in the clone

* NPZ data (`data_npz/`), the PCMCI+ cache except the tracked `pretrained_priors/`
  (copy them into your `--prior_cache_dir` with `bash scripts/setup_prior_cache.sh` if the
  data bytes match), checkpoints, `results/`, snapshots, the conda environment.
* Server-specific paths: everything is passed via the CLI/env table in section 3.
