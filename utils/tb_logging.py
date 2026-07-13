"""TensorBoard writer selection.

Exposes:
    SummaryWriter  -- selected class (torch.utils.tensorboard preferred, then tensorboardX)
    TB_BACKEND     -- string label for the backend that was loaded, or None
"""

SummaryWriter = None
TB_BACKEND = None
try:
    from torch.utils.tensorboard import SummaryWriter as _TorchSummaryWriter
    SummaryWriter = _TorchSummaryWriter
    TB_BACKEND = "torch.utils.tensorboard"
except Exception:
    try:
        from tensorboardX import SummaryWriter as _XSummaryWriter
        SummaryWriter = _XSummaryWriter
        TB_BACKEND = "tensorboardX"
    except Exception:
        SummaryWriter = None
        TB_BACKEND = None
