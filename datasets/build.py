"""Entity data loader for PICAAD (NPZ-backed multivariate time series).

The NPZ layout expected under `cfg.DATA.INPUT_DIR`:
    {entity}.npz  with keys:
        train  : [T_train, N]
        test   : [T_test, N]
        label  : [T_test]  or  [T_test, K]  (K anomaly types, or-reduced)
"""
import glob
import os
from typing import List

import numpy as np

from datasets.sliding_window import SlidingWindowDataset
from datasets.split import split_and_standardize, split_time_ordered
from datasets.util import (
    make_pseudo_env_ids,
    reduce_label,
    standardize_train_test,
)


class EntityArrays:
    """Container for a single entity's standardized arrays + label + stats.

    ``train_z`` is the standardized *full* train series when VAL is off. When
    VAL is on it is the standardized chronological ``train_sub`` and ``val_z``
    holds the trailing validation block (standardized with train_sub
    statistics). ``val_boundary`` is the raw row index where val starts in the
    original train array (== T_train when VAL is off).
    """

    def __init__(self, name: str, train_z, test_z, y, mu, sd,
                 val_z=None, val_boundary=None, val_frac=0.0):
        self.name = name
        self.train_z = train_z
        self.test_z = test_z
        self.y = y
        self.mu = mu
        self.sd = sd
        self.N = train_z.shape[1]
        self.T_train = train_z.shape[0]
        self.T_test = test_z.shape[0]
        self.val_z = val_z if val_z is not None else train_z[:0]
        self.T_val = int(self.val_z.shape[0])
        self.val_boundary = int(val_boundary) if val_boundary is not None else self.T_train
        self.val_frac = float(val_frac)


def list_entities(cfg) -> List[str]:
    """List entity NPZ basenames under cfg.DATA.INPUT_DIR."""
    if cfg.DATA.ENTITIES:
        return [e.strip() for e in cfg.DATA.ENTITIES.split(',') if e.strip()]
    files = sorted(glob.glob(os.path.join(cfg.DATA.INPUT_DIR, '*.npz')))
    return [os.path.splitext(os.path.basename(f))[0] for f in files]


def load_entity(cfg, entity_name: str) -> EntityArrays:
    """Read one entity NPZ file and return standardized arrays.

    VAL off (default): identical to the native pipeline.
    VAL on: the raw train array is sliced chronologically into train_sub / val
    *before* standardization; mu/sd are fit on train_sub only and applied to
    train_sub, val and test.
    """
    path = os.path.join(cfg.DATA.INPUT_DIR, f'{entity_name}.npz')
    if not os.path.exists(path):
        raise FileNotFoundError(f'Entity NPZ not found: {path}')

    data = np.load(path)
    train = data['train'].astype(np.float32)
    test = data['test'].astype(np.float32)
    if train.ndim == 1:
        train = train[:, None]
    if test.ndim == 1:
        test = test[:, None]
    if train.shape[1] != test.shape[1]:
        raise ValueError(
            f'{entity_name}: N mismatch between train ({train.shape[1]}) '
            f'and test ({test.shape[1]})'
        )
    expected_n = int(getattr(cfg.DATA, 'EXPECTED_N', 0) or 0)
    if expected_n > 0 and train.shape[1] != expected_n:
        # No fallback, slicing or padding: a wrong preprocessing variant
        # (e.g. the 44-channel SWaT export) must fail loudly.
        raise ValueError(
            f'{entity_name}: N={train.shape[1]} but cfg.DATA.EXPECTED_N={expected_n} '
            f'(file: {path})'
        )

    y = reduce_label(data['label'], test.shape[0])

    val_enabled = bool(getattr(cfg, 'VAL', None) and cfg.VAL.ENABLE)
    val_frac = float(cfg.VAL.FRAC) if val_enabled else 0.0

    if cfg.DATA.SCALE == 'standard':
        if val_enabled:
            train_z, val_z, test_z, mu, sd, boundary = split_and_standardize(
                train, test, val_frac,
            )
        else:
            train_z, test_z, mu, sd = standardize_train_test(train, test)
            val_z, boundary = None, train.shape[0]
    elif cfg.DATA.SCALE == 'none':
        if val_enabled:
            train_sub, val_sub, boundary = split_time_ordered(train, val_frac)
            train_z = train_sub.astype(np.float32)
            val_z = val_sub.astype(np.float32)
        else:
            train_z = train.astype(np.float32)
            val_z, boundary = None, train.shape[0]
        test_z = test.astype(np.float32)
        mu = np.zeros((1, train.shape[1]), dtype=np.float32)
        sd = np.ones((1, train.shape[1]), dtype=np.float32)
    else:
        raise ValueError(f'Unknown DATA.SCALE: {cfg.DATA.SCALE}')

    return EntityArrays(
        entity_name, train_z, test_z, y, mu, sd,
        val_z=val_z, val_boundary=boundary, val_frac=val_frac,
    )


def build_train_dataset(cfg, train_TN) -> SlidingWindowDataset:
    L = cfg.PICAAD.L
    W = train_TN.shape[0] - L + 1
    env_ids = make_pseudo_env_ids(W, cfg.DATA.NUM_ENVS)
    return SlidingWindowDataset(train_TN, L, env_ids=env_ids, return_env=True)


def build_val_dataset(cfg, val_TN) -> SlidingWindowDataset:
    """Validation windows: built on the val block alone (no window crosses the
    train_sub/val boundary), no pseudo-env ids, plain ``x`` samples."""
    return SlidingWindowDataset(val_TN, cfg.PICAAD.L)


def build_test_dataset(cfg, test_TN) -> SlidingWindowDataset:
    return SlidingWindowDataset(test_TN, cfg.PICAAD.L)
