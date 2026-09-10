import fcntl
import hashlib
import os
import time

import numpy as np
import torch

from model.modeling_picaad import PICAAD
from model.priors import (
    build_cte_causal_prior,
    build_pcmci_causal_prior,
    build_te_causal_prior,
)


def build_model(cfg, N: int) -> PICAAD:
    """Instantiate PICAAD from cfg. N (number of variables) is entity-specific
    and passed in explicitly since it isn't part of the base yacs schema.
    """
    if cfg.MODEL.NAME != 'PICAAD':
        raise ValueError(f'Unknown MODEL.NAME: {cfg.MODEL.NAME}')

    model = PICAAD(
        N=N,
        L=cfg.PICAAD.L,
        tau_max=cfg.PICAAD.TAU_MAX,
        d=cfg.PICAAD.D,
        heads=cfg.PICAAD.HEADS,
        enc_layers=cfg.PICAAD.ENC_LAYERS,
        dropout=cfg.PICAAD.DROPOUT,
        mhsa_residual=cfg.PICAAD.MHSA_RESIDUAL,
        lag_win=cfg.PICAAD.LAG_WIN,
        pred_temp=cfg.PICAAD.PRED_TEMP,
        self_loop_bias=cfg.PICAAD.SELF_LOOP_BIAS,
        dynamic_graph=cfg.PICAAD.DYNAMIC_GRAPH,
        graph_hidden=cfg.PICAAD.GRAPH_HIDDEN,
        gate_init=cfg.PICAAD.GATE_INIT,
        te_prior_blend=cfg.PICAAD.PRIOR.BLEND,
        causal_attn_mask_scale=cfg.PICAAD.CAUSAL_ATTN_MASK_SCALE,
        causal_mask_warmup_epochs=cfg.PICAAD.CAUSAL_MASK_WARMUP,
        use_gat=cfg.PICAAD.GAT.ENABLE,
        gat_num_layers=cfg.PICAAD.GAT.NUM_LAYERS,
        gat_heads=cfg.PICAAD.GAT.HEADS,
        gat_dim=cfg.PICAAD.GAT.DIM,
        gat_dropout=cfg.PICAAD.GAT.DROPOUT,
        gat_same_lag_prior=cfg.PICAAD.GAT.SAME_LAG_PRIOR,
    )
    return model


def build_causal_prior(cfg, train_TN: np.ndarray):
    """Build (te_weight, te_gate) NPZ-compatible arrays from cfg + train data."""
    prior_type = cfg.PICAAD.PRIOR.TYPE
    tau_max = cfg.PICAAD.TAU_MAX

    if prior_type == 'pcmci':
        return build_pcmci_causal_prior(
            train_TN,
            tau_max=tau_max,
            ci_test=cfg.PICAAD.PRIOR.PCMCI.CI_TEST,
            pc_alpha=cfg.PICAAD.PRIOR.PCMCI.ALPHA,
            subsample=cfg.PICAAD.PRIOR.PCMCI.SUBSAMPLE,
            self_mass=cfg.PICAAD.PRIOR.SELF_MASS,
            seed=cfg.PICAAD.PRIOR.SEED,
        )
    if prior_type == 'cte':
        return build_cte_causal_prior(
            train_TN,
            tau_max=tau_max,
            num_bins=cfg.PICAAD.PRIOR.TE.BINS,
            num_chunks=cfg.PICAAD.PRIOR.TE.NUM_CHUNKS,
            chunk_len=cfg.PICAAD.PRIOR.TE.CHUNK_LEN,
            threshold=cfg.PICAAD.PRIOR.TE.THRESHOLD,
            self_mass=cfg.PICAAD.PRIOR.SELF_MASS,
            seed=cfg.PICAAD.PRIOR.SEED,
        )
    if prior_type == 'te':
        return build_te_causal_prior(
            train_TN,
            tau_max=tau_max,
            num_bins=cfg.PICAAD.PRIOR.TE.BINS,
            num_chunks=cfg.PICAAD.PRIOR.TE.NUM_CHUNKS,
            chunk_len=cfg.PICAAD.PRIOR.TE.CHUNK_LEN,
            threshold=cfg.PICAAD.PRIOR.TE.THRESHOLD,
            self_mass=cfg.PICAAD.PRIOR.SELF_MASS,
            seed=cfg.PICAAD.PRIOR.SEED,
        )
    raise ValueError(f'Unknown PICAAD.PRIOR.TYPE: {prior_type}')


def apply_prior_to_model(cfg, model: PICAAD, te_weight_np, te_gate_np):
    model.set_te_prior(
        torch.from_numpy(te_weight_np),
        torch.from_numpy(te_gate_np),
        init_scale=cfg.PICAAD.PRIOR.INIT_SCALE,
    )


# ----------------------------------------------------------
# On-disk prior cache
# ----------------------------------------------------------
def _prior_cache_key(cfg, train_TN: np.ndarray, entity_name: str,
                     split_id: str = 'full') -> str:
    """Deterministic cache key from prior hyperparameters + training data
    (+ split identity).

    Any change to hyperparameters, tau_max, or the training tensor content
    invalidates the cache. Excludes irrelevant params (BLEND, INIT_SCALE are
    applied at model-init time and don't affect the prior arrays).

    ``split_id == 'full'`` (default, VAL off) reproduces the legacy key
    byte-for-byte: nothing is added to the hash input or the file name, so
    existing full-train caches keep hitting. Any other ``split_id`` (e.g.
    ``'val0.2_b105985'`` for a chronological train_sub) is mixed into the hash
    and appended to the file name, so a train_sub prior can never be confused
    with a full-train prior even though both share DATA.NAME/entity/PCMCI
    settings.
    """
    h = hashlib.sha256()
    p = cfg.PICAAD.PRIOR
    parts = [
        cfg.DATA.NAME, entity_name, p.TYPE,
        f'tau{cfg.PICAAD.TAU_MAX}',
        f'self{p.SELF_MASS:g}', f'sd{p.SEED}',
    ]
    if split_id != 'full':
        parts.append(f'split_{split_id}')
    if p.TYPE == 'pcmci':
        parts += [p.PCMCI.CI_TEST, f'a{p.PCMCI.ALPHA:g}', f'sub{p.PCMCI.SUBSAMPLE}']
    else:
        parts += [f'b{p.TE.BINS}', f'nc{p.TE.NUM_CHUNKS}',
                  f'cl{p.TE.CHUNK_LEN}', f'th{p.TE.THRESHOLD:g}']
    h.update('|'.join(parts).encode('utf-8'))
    h.update(np.ascontiguousarray(train_TN).tobytes())
    digest = h.hexdigest()[:16]
    prefix = f'{cfg.DATA.NAME}_{entity_name}_{p.TYPE}'
    if split_id != 'full':
        return f'{prefix}_{split_id}_{digest}'
    return f'{prefix}_{digest}'


def build_causal_prior_cached(cfg, train_TN: np.ndarray, entity_name: str,
                              split_id: str = 'full'):
    """Wraps build_causal_prior with an on-disk NPZ cache keyed by
    hyperparameters, the raw training tensor contents and ``split_id``.

    Callers on the legacy full-train path may omit ``split_id``. Callers that
    pass a chronological train_sub MUST pass the matching split identity
    (``datasets.split.split_id_for``) so the cache cannot silently reuse a
    full-train prior.
    """
    p = cfg.PICAAD.PRIOR
    if not p.CACHE_ENABLE:
        return build_causal_prior(cfg, train_TN)

    key = _prior_cache_key(cfg, train_TN, entity_name, split_id=split_id)
    cache_path = os.path.join(p.CACHE_DIR, f'{key}.npz')

    def _try_load():
        if not p.CACHE_REBUILD and os.path.exists(cache_path):
            try:
                data = np.load(cache_path)
                te_weight_np = data['te_weight']
                te_gate_np = data['te_gate']
                print(f'  [prior] cache hit: {cache_path}', flush=True)
                return te_weight_np, te_gate_np
            except Exception as e:
                print(f'  [prior] cache read failed ({e}); rebuilding', flush=True)
        return None

    hit = _try_load()
    if hit is not None:
        return hit

    # Concurrent builders of the *same key* (e.g. seed-parallel launchers)
    # serialize on a per-key lock; whoever wins builds once, the others load
    # the finished file. The key itself is unchanged; only the I/O is guarded.
    os.makedirs(p.CACHE_DIR, exist_ok=True)
    lock_path = cache_path + '.lock'
    with open(lock_path, 'w') as lock_f:
        fcntl.flock(lock_f, fcntl.LOCK_EX)
        try:
            hit = _try_load()
            if hit is not None:
                return hit

            t0 = time.time()
            te_weight_np, te_gate_np = build_causal_prior(cfg, train_TN)
            dt = time.time() - t0

            # atomic publish: write to a private temp file, then rename
            # np.savez appends '.npz' unless the name already ends with it
            tmp_path = f'{cache_path[:-4]}.tmp{os.getpid()}.npz'
            try:
                np.savez(tmp_path, te_weight=te_weight_np, te_gate=te_gate_np)
                os.replace(tmp_path, cache_path)
                print(f'  [prior] cached ({dt:.1f}s): {cache_path}', flush=True)
            except Exception as e:
                print(f'  [prior] cache write failed ({e}); continuing without cache', flush=True)
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
        finally:
            fcntl.flock(lock_f, fcntl.LOCK_UN)

    return te_weight_np, te_gate_np
