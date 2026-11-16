"""Build and cache the PCMCI+ prior for every entity once, before launching parallel seeds
(several seeds of the same entity would otherwise compute and write the same cache file concurrently).
Honors DATA.FIT_ON_TRAIN_SUB exactly as main.py does.

Usage:
    python scripts/precompute_priors.py --cfg scripts/configs/ablation_smd.yaml DATA.FIT_ON_TRAIN_SUB True [KEY VALUE ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets.build import list_entities, load_entity, split_train_val
from model.build import build_causal_prior_cached
from utils.parser import load_config, parse_args


def main():
    cfg, _ = load_config(parse_args())
    for name in list_entities(cfg):
        entity = load_entity(cfg, name)
        prior_input = entity.train_z
        if getattr(cfg.DATA, 'FIT_ON_TRAIN_SUB', False):
            prior_input, _ = split_train_val(entity.train_z, cfg.PICAAD.VAL_RATIO)
        print(f'[{name}] prior input T={prior_input.shape[0]}', flush=True)
        build_causal_prior_cached(cfg, prior_input, name)


if __name__ == '__main__':
    main()
