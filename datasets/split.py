"""Chronological train/validation split for PICAAD's validation protocol.

The NPZ files under ``data_npz/`` carry a train/test split; this module
further slices the raw ``train`` series into a leading ``train_sub`` and a
trailing ``val`` block (``val_frac`` of the rows). The slice happens on the
raw array *before* standardization, and the two blocks are windowed
independently downstream (``datasets.build.build_train_dataset`` /
``build_val_dataset``), so no window straddles the boundary.

Statistics (mean/std) and the PCMCI+ prior are fit on ``train_sub`` only.
``val_frac == 0`` (VAL off) returns the original array unchanged.
"""
from typing import Tuple

import numpy as np

from datasets.util import standardize_train_test


def split_time_ordered(train_TN: np.ndarray, val_frac: float) -> Tuple[np.ndarray, np.ndarray, int]:
    """Slice ``train_TN`` chronologically into (train_sub, val, boundary).

    ``boundary`` is the raw row index where ``val`` begins:
    ``train_sub = train_TN[:boundary]``, ``val = train_TN[boundary:]``.
    ``val_frac == 0`` returns the full array plus an empty val block.
    """
    if val_frac < 0.0 or val_frac >= 1.0:
        raise ValueError(f'val_frac must be in [0, 1); got {val_frac}')
    T = train_TN.shape[0]
    if val_frac == 0.0:
        return train_TN, train_TN[T:T], T
    boundary = int(round(T * (1.0 - val_frac)))
    boundary = max(1, min(T - 1, boundary))
    return train_TN[:boundary], train_TN[boundary:], boundary


def split_and_standardize(train_TN: np.ndarray, test_TN: np.ndarray, val_frac: float):
    """Split ``train_TN`` chronologically, then standardize train_sub, val and
    test with (mu, sd) fit on ``train_sub`` only.

    Returns ``(train_sub_z, val_z, test_z, mu, sd, boundary)``. ``val_z`` is an
    empty ``[0, N]`` float32 array when ``val_frac == 0``. NaN/inf in ``val``
    are replaced by the train_sub column mean, mirroring
    ``standardize_train_test``'s handling of train/test.
    """
    train_sub, val_sub, boundary = split_time_ordered(train_TN, val_frac)
    train_sub_z, test_z, mu, sd = standardize_train_test(train_sub, test_TN)
    if val_sub.shape[0] == 0:
        val_z = np.empty((0, train_TN.shape[1]), dtype=np.float32)
    else:
        val_clean = np.where(np.isfinite(val_sub), val_sub, np.nan).astype(np.float32)
        val_clean = np.where(np.isnan(val_clean), mu.astype(np.float32), val_clean).astype(np.float32)
        val_z = ((val_clean - mu) / sd).astype(np.float32)
    return train_sub_z, val_z, test_z, mu, sd, boundary


def split_id_for(cfg, entity) -> str:
    """Split identity used to key the prior cache (and, later, checkpoints).

    ``'full'`` when VAL is off (legacy key, unchanged). Otherwise
    ``'val{FRAC:g}_b{boundary}'`` where ``boundary`` is the raw row index at
    which validation starts, e.g. ``'val0.2_b105985'`` for PSM.
    """
    val_enabled = bool(getattr(cfg, 'VAL', None) and cfg.VAL.ENABLE)
    if not val_enabled:
        return 'full'
    return f'val{float(cfg.VAL.FRAC):g}_b{int(entity.val_boundary)}'
