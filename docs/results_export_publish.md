# Exporting and publishing results

`scripts/export_results.py export` turns a launcher `out_root` into a small reproduction package;
`scripts/publish_results.sh` puts that package on a per-server results branch from a separate publishing worktree;
`scripts/export_results.py aggregate` combines packages from several servers after checking that they are comparable.

## Package (`reports/experiments/<campaign>/<server>/<run_id>/`)

| file | content |
|---|---|
| `metrics.csv` | one row per (exported eval job, variant): dataset/entity/seed, ckpt tag + epoch + sha256, val MAE, split id, fit protocol, data sha256, prior cache key, gamma, calibrate, CF top-k, VUS window, training code sha, eval code sha, device, torch, metrics; `result_kind=val_ckpt_eval` |
| `run_manifest.json` | campaign/server/run_id, launcher queue name and manifest, **training_code_sha** (from SUCCESS identities) vs `export_code` (the exporting checkout; the publishing commit is again different), `complete` flag, job status list (success/failed/blocked/pending all listed), duplicates |
| `config_resolved.yaml` | resolved training/eval config per config file, paths redacted |
| `provenance_summary.json` | per train job (identity, val-MAE curve summary, checkpoint sha256, GPU, timing) and per eval job (checkpoint, restore, data, scoring, CF profile, calibration, evaluator, forward passes, parity, device, time) |
| `artifacts.json` | sha256/size/relative path of everything **not** copied: checkpoints, scores.npz, logs, data NPZ identifiers |
| `summary.md` | human-readable status and fusion metrics table |

Rules: only jobs with `SUCCESS.json` (+ `provenance.json`/`metrics.csv` for eval) are exported; the package is `complete`
only if every job in the queue succeeded. If a logical job has several successful attempts, only the attempt recorded in
`queue.json` is exported and the others are listed under `duplicates` — nothing is chosen by metric. Absolute paths under
out_root / repo / data root / prior cache / `$HOME` become placeholders and secret-looking keys are dropped; the original
provenance files stay on the server. No checkpoint, `scores.npz`, data, log or symlink is copied.

```bash
python scripts/export_results.py export --out_root /srv/picaad/runs/cfval/server4 --campaign cfval --server server4 \
    --data_root /srv/picaad/data_npz --prior_cache_dir /srv/picaad/prior_cache            # -> reports/experiments/cfval/server4/<queue name>/
```

## Publishing (`scripts/publish_results.sh`)

```bash
scripts/publish_results.sh --campaign cfval --server server4 --out_root /srv/picaad/runs/cfval/server4              # export + dry-run (default)
scripts/publish_results.sh --campaign cfval --server server4 --out_root /srv/picaad/runs/cfval/server4 --commit     # commit on results/cfval/server4
scripts/publish_results.sh --campaign cfval --server server4 --out_root /srv/picaad/runs/cfval/server4 --commit --push
```

* Branch `results/<campaign>/<server>` lives in a **separate worktree** (`<out_root>/_publish/worktree_<campaign>_<server>`);
  the execution checkout's HEAD, index and working tree are never touched, so `PICAAD_CODE_SHA` and the launcher's resume
  identity stay valid while results are published.
* Default is export + dry-run into `<out_root>/_publish/dryrun_<ts>/`; `--commit` and `--push` must be explicit.
* Only `reports/experiments/<campaign>/<server>/<run_id>` is staged (no `git add .`); pushes are never forced. If the
  remote branch is ahead of or diverged from the local one, or the worktree has uncommitted tracked changes, the script
  stops and reports.
* Each server publishes only its own `<server>/` subtree, so the two servers never write the same file. The aggregate is
  produced separately (below) and is not part of a server branch.

## Aggregating two servers

```bash
python scripts/export_results.py aggregate --reports_root reports/experiments --campaign cfval --expected_seeds 0,1,2,3
# -> reports/experiments/cfval/_aggregate/aggregate_<ts>_<inputs hash>/{per_seed_results.csv, dataset_means.csv, aggregate_manifest.json, aggregate.md}
```

Before averaging, the aggregator checks that every package has `result_kind=val_ckpt_eval`, that the resolved config
signature (epochs, LR, batch, PERM, CALIBRATE, CF, gamma, CF_TOP_K, VAL, evaluator settings) is identical for the same
config file across packages, that `protocol/config/gamma/calibrate/cf_top_k/fit_protocol` do not differ within a dataset,
and that no logical result appears twice. PSM and SWaT are reported per seed with missing seeds listed; SMD is labelled
**full-SMD** only when all 28 entities have every expected seed, otherwise `partial-SMD (k/28 …)`. Test-selected epochs,
gamma sweeps and native training-time results are outside this pipeline and are never mixed in.
