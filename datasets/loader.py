from torch.utils.data import DataLoader

from datasets.build import build_train_dataset, build_val_dataset


def get_train_dataloader(cfg, train_TN):
    ds = build_train_dataset(cfg, train_TN)
    return DataLoader(
        ds,
        batch_size=cfg.TRAIN.BATCH_SIZE,
        shuffle=cfg.TRAIN.SHUFFLE,
        drop_last=cfg.TRAIN.DROP_LAST,
        num_workers=cfg.DATA_LOADER.NUM_WORKERS,
        pin_memory=cfg.DATA_LOADER.PIN_MEMORY,
    )


def get_val_dataloader(cfg, val_TN):
    """Validation loader: no shuffle, no drop_last, every window evaluated
    exactly once. Batch size falls back to TEST.BATCH_SIZE when
    VAL.EVAL_BATCH_SIZE is 0."""
    ds = build_val_dataset(cfg, val_TN)
    batch = int(cfg.VAL.EVAL_BATCH_SIZE) if int(cfg.VAL.EVAL_BATCH_SIZE) > 0 else cfg.TEST.BATCH_SIZE
    return DataLoader(
        ds,
        batch_size=batch,
        shuffle=False,
        drop_last=False,
        num_workers=cfg.DATA_LOADER.NUM_WORKERS,
        pin_memory=cfg.DATA_LOADER.PIN_MEMORY,
    )
