"""PicaadTrainer: encapsulates the train loop, per-epoch eval, and reference
tensor (w_ref/cls_ref) maintenance for a single (entity, seed) run.
"""
import math
import os
import random
import subprocess

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from datasets.loader import get_train_dataloader, get_val_dataloader
from layers.ops import (
    make_self_causal_fallback_torch,
    normalize_causal_tensor_torch,
)
from model.intervention import (
    gradient_sensitivity_and_epoch_cls,
    permutation_alignment_and_epoch_cls,
)
from model.losses import (
    causal_structure_loss,
    graph_stability_loss,
    invariance_loss_from_tensor,
    prediction_train_loss,
)
from utils.evaluation import run_epoch_eval


# Group sub-weights (kept fixed as in the original picaad.py to preserve
# the achieved SWaT results; expose to cfg only if a future ablation needs it).
_W_TE_GATE = 0.50
_W_GRAPH = 0.50
_W_LAGMONO = 0.50
_W_INV = 0.50


class PicaadTrainer:
    def __init__(self, cfg, model, entity, seed,
                 device, writer=None, ckpt_dir=None, csv_path=None,
                 provenance=None):
        self.cfg = cfg
        self.model = model
        self.entity = entity          # datasets.build.EntityArrays
        self.seed = int(seed)
        self.device = device
        self.writer = writer
        self.writer_prefix = entity.name
        self.ckpt_dir = ckpt_dir
        self.csv_path = csv_path

        self.rng = np.random.default_rng(self.seed)

        self.model.to(device)
        self.model.reset_refs()

        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=cfg.SOLVER.BASE_LR,
            weight_decay=cfg.SOLVER.WEIGHT_DECAY,
        )
        self.train_loader = get_train_dataloader(cfg, entity.train_z)

        # ------------------------------------------------------------------
        # Validation protocol state (Phase 1-B). Everything below is inert
        # when cfg.VAL.ENABLE is False: the native loop, its test-set epoch
        # eval and checkpoint naming are untouched.
        # ------------------------------------------------------------------
        self.val_enabled = bool(getattr(cfg, 'VAL', None) and cfg.VAL.ENABLE)
        self.provenance = dict(provenance or {})
        self.val_loader = None
        self.val_csv_path = None
        self.best_val_ckpt_path = None
        self.last_ckpt_path = None
        self.best_val_mae = math.inf
        self.best_val_epoch = None
        self._global_step = 0
        if self.val_enabled:
            if entity.T_val < cfg.PICAAD.L + 1:
                raise ValueError(
                    f'{entity.name}: validation block too short '
                    f'(T_val={entity.T_val} < L+1={cfg.PICAAD.L + 1})'
                )
            self.val_loader = get_val_dataloader(cfg, entity.val_z)
            if csv_path:
                base, ext = os.path.splitext(csv_path)
                self.val_csv_path = base.replace('_epoch_metrics', '') + '_val_metrics' + (ext or '.csv')
            if ckpt_dir:
                self.best_val_ckpt_path = os.path.join(ckpt_dir, f'{entity.name}_seed{seed}_best_val.pt')
                self.last_ckpt_path = os.path.join(ckpt_dir, f'{entity.name}_seed{seed}_last.pt')

    def train(self):
        cfg = self.cfg
        Tlag = self.model.tau_max
        N = self.model.N
        epochs = cfg.SOLVER.MAX_EPOCH

        for ep in range(1, epochs + 1):
            self.model.train()
            self.model._current_epoch = ep

            w_sum = torch.zeros(Tlag, N, N, device=self.device)
            w_cnt = 0

            cls_sum = torch.zeros(Tlag, N, N, device=self.device)
            cls_cnt = torch.zeros(Tlag, N, 1, device=self.device)

            stats = self._empty_stats()
            steps = 0
            last_use_cstruct = False
            last_use_graph_loss = False

            use_grad_int = (cfg.PICAAD.INTERVENTION.LOSS_TYPE == 'gradient')

            for X, env in self.train_loader:
                X = X.to(self.device)
                if use_grad_int:
                    X.requires_grad_(True)
                env = torch.as_tensor(env, device=self.device, dtype=torch.long)

                (_, pred, _, pred_weights,
                 _, _, edge_strength, _, _) = self.model(X)

                xL = X[:, -1, :]

                loss_pred = prediction_train_loss(xL, pred, loss_type=cfg.PICAAD.TRAIN_LOSS_TYPE)

                if pred_weights.dim() == 4:
                    w_epoch_mean = pred_weights.mean(dim=0).detach()
                else:
                    w_epoch_mean = pred_weights.detach()
                w_sum += w_epoch_mean
                w_cnt += 1

                use_cstruct_loss = (ep >= cfg.PICAAD.START_CLS_EPOCH) and self.model.has_cls_ref
                use_graph_loss = (ep >= cfg.PICAAD.START_WREF_EPOCH) and self.model.has_w_ref
                last_use_cstruct = use_cstruct_loss
                last_use_graph_loss = use_graph_loss

                loss_cstruct = (
                    causal_structure_loss(edge_strength, self.model.cls_ref)
                    if use_cstruct_loss
                    else torch.tensor(0.0, device=self.device)
                )
                loss_graph = (
                    graph_stability_loss(pred_weights, self.model.w_ref)
                    if (use_graph_loss and cfg.PICAAD.ENABLE_GRAPH_LOSS)
                    else torch.tensor(0.0, device=self.device)
                )

                loss_gate = (
                    self.model.gate_sparsity()
                    if cfg.PICAAD.ENABLE_GATE_LOSS
                    else torch.tensor(0.0, device=self.device)
                )
                loss_lagmono = (
                    self.model.lag_monotonic_penalty()
                    if cfg.PICAAD.ENABLE_LAGMONO_LOSS
                    else torch.tensor(0.0, device=self.device)
                )
                if cfg.PICAAD.ENABLE_PRIOR_LOSS:
                    loss_te_w, loss_te_g = self.model.causal_prior_losses(pred_weights)
                else:
                    loss_te_w = torch.tensor(0.0, device=self.device)
                    loss_te_g = torch.tensor(0.0, device=self.device)

                if cfg.PICAAD.INTERVENTION.LOSS_TYPE == 'gradient':
                    loss_perm, batch_cls_sum, batch_cls_cnt = gradient_sensitivity_and_epoch_cls(
                        self.model, X, pred, xL, edge_strength,
                        margin=cfg.PICAAD.INTERVENTION.MARGIN_HIGH,
                    )
                else:
                    base_abs_err_ref = (xL - pred).abs().detach()
                    loss_perm, batch_cls_sum, batch_cls_cnt = permutation_alignment_and_epoch_cls(
                        self.model, X, xL, base_abs_err_ref, edge_strength, self.rng,
                        perm_pairs=cfg.PICAAD.INTERVENTION.PERM_PAIRS_PER_BATCH,
                        perm_mode=cfg.PICAAD.INTERVENTION.PERM_MODE,
                        fill_value=cfg.PICAAD.INTERVENTION.FILL_VALUE,
                        loss_type=cfg.PICAAD.INTERVENTION.LOSS_TYPE,
                        margin_high=cfg.PICAAD.INTERVENTION.MARGIN_HIGH,
                        margin_low=cfg.PICAAD.INTERVENTION.MARGIN_LOW,
                    )
                cls_sum += batch_cls_sum
                cls_cnt += batch_cls_cnt

                loss_inv = (
                    invariance_loss_from_tensor(edge_strength, env)
                    if cfg.PICAAD.ENABLE_INV_LOSS
                    else torch.tensor(0.0, device=self.device)
                )

                group_task = loss_pred
                group_causal = loss_te_w + _W_TE_GATE * loss_te_g
                if use_cstruct_loss:
                    group_causal = group_causal + loss_cstruct
                group_graphreg = loss_gate + _W_LAGMONO * loss_lagmono
                if use_graph_loss and cfg.PICAAD.ENABLE_GRAPH_LOSS:
                    group_graphreg = group_graphreg + _W_GRAPH * loss_graph
                group_robust = loss_perm + _W_INV * loss_inv

                loss = (
                    cfg.PICAAD.LAM_TASK * group_task
                    + cfg.PICAAD.LAM_CAUSAL * group_causal
                    + cfg.PICAAD.LAM_GRAPHREG * group_graphreg
                    + cfg.PICAAD.LAM_ROBUST * group_robust
                )

                self.optimizer.zero_grad(set_to_none=True)
                loss.backward()
                if cfg.SOLVER.GRADIENT_CLIP and cfg.SOLVER.GRADIENT_CLIP > 0:
                    nn.utils.clip_grad_norm_(self.model.parameters(), cfg.SOLVER.GRADIENT_CLIP)
                self.optimizer.step()
                self._global_step += 1

                self._accumulate_stats(stats, group_task, group_causal, group_graphreg,
                                        group_robust, loss, loss_pred,
                                        loss_te_w, loss_te_g, loss_cstruct, loss_graph,
                                        loss_gate, loss_lagmono, loss_perm, loss_inv)
                steps += 1

            self._update_epoch_refs(w_sum, w_cnt, cls_sum, cls_cnt)

            avg = {k: v / max(steps, 1) for k, v in stats.items()}
            self._print_epoch(ep, avg, last_use_cstruct, last_use_graph_loss)
            self._log_train_tb(ep, avg)

            if self.val_enabled:
                # reference tensors were updated above (_update_epoch_refs);
                # validation observes the post-update model and never touches
                # the test set.
                val_mae = self._run_val_epoch(ep)
                self._handle_val_result(ep, avg, val_mae)
            else:
                self._maybe_run_epoch_eval(ep, epochs)

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------
    @staticmethod
    def _empty_stats():
        return {
            "task": 0.0, "causal": 0.0, "graphreg": 0.0, "robust": 0.0, "total": 0.0,
            "pred": 0.0, "tew": 0.0, "teg": 0.0,
            "cstruct": 0.0, "graph": 0.0, "gate": 0.0, "lagmono": 0.0,
            "perm": 0.0, "inv": 0.0,
        }

    @staticmethod
    def _accumulate_stats(stats, gt, gc, gg, gr, total, lp, ltew, lteg,
                          lc, lg, lgate, llm, lperm, linv):
        stats["task"]     += float(gt.detach().cpu())
        stats["causal"]   += float(gc.detach().cpu())
        stats["graphreg"] += float(gg.detach().cpu())
        stats["robust"]   += float(gr.detach().cpu())
        stats["total"]    += float(total.detach().cpu())
        stats["pred"]     += float(lp.detach().cpu())
        stats["tew"]      += float(ltew.detach().cpu())
        stats["teg"]      += float(lteg.detach().cpu())
        stats["cstruct"]  += float(lc.detach().cpu())
        stats["graph"]    += float(lg.detach().cpu())
        stats["gate"]     += float(lgate.detach().cpu())
        stats["lagmono"]  += float(llm.detach().cpu())
        stats["perm"]     += float(lperm.detach().cpu())
        stats["inv"]      += float(linv.detach().cpu())

    def _update_epoch_refs(self, w_sum, w_cnt, cls_sum, cls_cnt):
        cfg = self.cfg
        Tlag = self.model.tau_max
        N = self.model.N
        with torch.no_grad():
            epoch_w = w_sum / max(w_cnt, 1)
            if not self.model.has_w_ref:
                self.model.w_ref.copy_(epoch_w)
                self.model.has_w_ref = True
            elif cfg.PICAAD.WREF_EMA <= 0.0:
                self.model.w_ref.copy_(epoch_w)
            else:
                beta = float(cfg.PICAAD.WREF_EMA)
                self.model.w_ref.mul_(beta).add_(epoch_w * (1.0 - beta))

            if self.model.has_cls_ref:
                fallback_cls = self.model.cls_ref
            elif self.model.has_te_prior:
                fallback_cls = self.model.te_prior_weight
            else:
                fallback_cls = make_self_causal_fallback_torch(
                    Tlag, N, device=self.device, dtype=cls_sum.dtype
                )

            epoch_cls_raw = torch.where(
                cls_cnt > 0,
                cls_sum / cls_cnt.clamp_min(1.0),
                fallback_cls,
            )
            epoch_cls = normalize_causal_tensor_torch(epoch_cls_raw)

            if not self.model.has_cls_ref:
                self.model.cls_ref.copy_(epoch_cls)
                self.model.has_cls_ref = True
            elif cfg.PICAAD.CLS_EMA <= 0.0:
                self.model.cls_ref.copy_(epoch_cls)
            else:
                beta = float(cfg.PICAAD.CLS_EMA)
                self.model.cls_ref.mul_(beta).add_(epoch_cls * (1.0 - beta))
                self.model.cls_ref.copy_(normalize_causal_tensor_torch(self.model.cls_ref))

    def _print_epoch(self, ep, avg, last_use_cstruct, last_use_graph_loss):
        print(
            f"  [ep {ep:02d}] "
            f"task={avg['task']:.6f} causal={avg['causal']:.6f} "
            f"graphreg={avg['graphreg']:.6f} robust={avg['robust']:.6f} "
            f"total={avg['total']:.6f} | "
            f"pred={avg['pred']:.6f} "
            f"tew={avg['tew']:.6f} teg={avg['teg']:.6f} "
            f"cstruct={avg['cstruct']:.6f} graph={avg['graph']:.6f} "
            f"gate={avg['gate']:.6f} lagmono={avg['lagmono']:.6f} "
            f"perm={avg['perm']:.6f} inv={avg['inv']:.6f} "
            f"has_cls={self.model.has_cls_ref} use_cstruct={last_use_cstruct} "
            f"has_wref={self.model.has_w_ref} use_graph={last_use_graph_loss}",
            flush=True,
        )

    def _log_train_tb(self, ep, avg):
        if self.writer is None:
            return
        w = self.writer
        p = self.writer_prefix
        w.add_scalar(f"{p}/train/group_task",     avg["task"],     ep)
        w.add_scalar(f"{p}/train/group_causal",   avg["causal"],   ep)
        w.add_scalar(f"{p}/train/group_graphreg", avg["graphreg"], ep)
        w.add_scalar(f"{p}/train/group_robust",   avg["robust"],   ep)
        w.add_scalar(f"{p}/train/total_loss",     avg["total"],    ep)
        w.add_scalar(f"{p}/train/pred_loss",         avg["pred"],    ep)
        w.add_scalar(f"{p}/train/te_weight_loss",    avg["tew"],     ep)
        w.add_scalar(f"{p}/train/te_gate_loss",      avg["teg"],     ep)
        w.add_scalar(f"{p}/train/causal_struct_loss",avg["cstruct"], ep)
        w.add_scalar(f"{p}/train/graph_loss",        avg["graph"],   ep)
        w.add_scalar(f"{p}/train/gate_loss",         avg["gate"],    ep)
        w.add_scalar(f"{p}/train/lagmono_loss",      avg["lagmono"], ep)
        w.add_scalar(f"{p}/train/perm_loss",         avg["perm"],    ep)
        w.add_scalar(f"{p}/train/inv_loss",          avg["inv"],     ep)

        with torch.no_grad():
            gate_np = self.model.edge_gate().detach().cpu().numpy()
            pw_global = self.model.get_pred_weights().detach().cpu().numpy()
            w.add_scalar(f"{p}/train/gate_mean",           float(gate_np.mean()),  ep)
            w.add_scalar(f"{p}/train/gate_max",            float(gate_np.max()),   ep)
            w.add_scalar(f"{p}/train/pred_weight_mean",    float(pw_global.mean()), ep)
            w.add_scalar(f"{p}/train/pred_weight_max",     float(pw_global.max()),  ep)
            w.add_scalar(f"{p}/train/pred_weight_entropy",
                         float(self.model.pred_weight_entropy().detach().cpu()), ep)
            w.add_scalar(f"{p}/train/w_ref_mean",   float(self.model.w_ref.mean().detach().cpu()),   ep)
            w.add_scalar(f"{p}/train/cls_ref_mean", float(self.model.cls_ref.mean().detach().cpu()), ep)
            w.add_scalar(f"{p}/train/cls_ref_std",  float(self.model.cls_ref.std().detach().cpu()),  ep)

        if ep % 10 == 0:
            w.add_histogram(f"{p}/train/gate_hist",        gate_np,  ep)
            w.add_histogram(f"{p}/train/pred_weight_hist", pw_global, ep)
            w.add_histogram(f"{p}/train/w_ref_hist",   self.model.w_ref.detach().cpu().numpy(),   ep)
            w.add_histogram(f"{p}/train/cls_ref_hist", self.model.cls_ref.detach().cpu().numpy(), ep)

    def _maybe_run_epoch_eval(self, ep, epochs_total):
        if self.val_enabled:
            raise RuntimeError(
                'test-set epoch evaluation is disabled under cfg.VAL.ENABLE=True; '
                'validation MAE selection is used instead (_run_val_epoch).'
            )
        every = self.cfg.TRAIN.EVAL_EVERY
        if every is None or every <= 0:
            return
        if (ep % every != 0) and (ep != epochs_total):
            return
        run_epoch_eval(
            self.model, self.entity.test_z, self.entity.y, self.device, self.cfg,
            ep=ep, seed=self.seed, name=self.entity.name,
            epochs_total=epochs_total,
            train_TN=self.entity.train_z,
            writer=self.writer, writer_prefix=self.writer_prefix,
            ckpt_dir=self.ckpt_dir, csv_path=self.csv_path,
            mu=self.entity.mu, sd=self.entity.sd,
        )

    # ------------------------------------------------------------------
    # Validation-based checkpoint selection (Phase 1-B)
    # ------------------------------------------------------------------
    @torch.no_grad()
    def _run_val_epoch(self, ep):
        """Prediction MAE on every validation window.

        sum(|x_L - pred|) over all windows and variables, divided by the total
        element count (shuffle=False, drop_last=False, so the trailing partial
        batch is weighted exactly like every other element). No optimizer
        step, no reference/accumulator update, no intervention. Model mode and
        all RNG states (python, numpy global, trainer generator, torch CPU/CUDA)
        are restored afterwards.
        """
        if not self.val_enabled or self.val_loader is None:
            raise RuntimeError('_run_val_epoch called without a validation loader')

        was_training = self.model.training
        py_state = random.getstate()
        np_state = np.random.get_state()
        gen_state = self.rng.bit_generator.state
        torch_cpu_state = torch.get_rng_state()
        cuda_states = torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None

        self.model.eval()
        try:
            sum_abs = 0.0
            count = 0
            for X in self.val_loader:
                X = X.to(self.device)
                out = self.model(X)
                pred = out[1]
                err = (X[:, -1, :] - pred).abs()
                sum_abs += float(err.sum().item())
                count += int(err.numel())
        finally:
            random.setstate(py_state)
            np.random.set_state(np_state)
            self.rng.bit_generator.state = gen_state
            torch.set_rng_state(torch_cpu_state)
            if cuda_states is not None:
                torch.cuda.set_rng_state_all(cuda_states)
            if was_training:
                self.model.train()

        return (sum_abs / count) if count > 0 else float('nan')

    def _handle_val_result(self, ep, avg_stats, val_mae):
        """Log the epoch row, update best-so-far (strict improvement only;
        ties keep the earlier best; non-finite never selected), save
        last.pt every epoch and best_val.pt on improvement."""
        val_valid = (val_mae is not None) and math.isfinite(val_mae)
        improved = val_valid and (val_mae + float(self.cfg.VAL.MIN_DELTA)) < self.best_val_mae
        if improved:
            self.best_val_mae = float(val_mae)
            self.best_val_epoch = int(ep)

        cls_ref = self.model.cls_ref.detach()
        w_ref = self.model.w_ref.detach()
        row = {
            'epoch': int(ep),
            'global_step': int(self._global_step),
            'train_pred_mae': float(avg_stats.get('pred', float('nan'))),
            'val_pred_mae': float(val_mae) if val_mae is not None else float('nan'),
            'val_is_finite': int(bool(val_valid)),
            'improved': int(bool(improved)),
            'best_epoch_so_far': int(self.best_val_epoch) if self.best_val_epoch is not None else -1,
            'best_val_mae_so_far': float(self.best_val_mae) if math.isfinite(self.best_val_mae) else float('nan'),
            'learning_rate': float(self.optimizer.param_groups[0]['lr']),
            'loss_total': float(avg_stats.get('total', float('nan'))),
            'group_task': float(avg_stats.get('task', float('nan'))),
            'group_causal': float(avg_stats.get('causal', float('nan'))),
            'group_graphreg': float(avg_stats.get('graphreg', float('nan'))),
            'group_robust': float(avg_stats.get('robust', float('nan'))),
            'cstruct': float(avg_stats.get('cstruct', float('nan'))),
            'perm': float(avg_stats.get('perm', float('nan'))),
            'warmup_ramp': float(self.model._warmup_ramp()),
            'has_cls_ref': int(self.model.has_cls_ref),
            'has_w_ref': int(self.model.has_w_ref),
            'cls_ref_mean': float(cls_ref.mean().item()),
            'w_ref_mean': float(w_ref.mean().item()),
        }
        if self.val_csv_path is not None:
            os.makedirs(os.path.dirname(self.val_csv_path) or '.', exist_ok=True)
            write_header = not os.path.exists(self.val_csv_path)
            pd.DataFrame([row]).to_csv(self.val_csv_path, mode='a', header=write_header, index=False)

        print(
            f'  [val ep {ep:02d} seed {self.seed}] val_mae={row["val_pred_mae"]:.6f}  '
            f'train_mae={row["train_pred_mae"]:.6f}  best_ep={row["best_epoch_so_far"]}  '
            f'best_mae={row["best_val_mae_so_far"]:.6f}' + ('  [best_val updated]' if improved else ''),
            flush=True,
        )
        if self.writer is not None:
            self.writer.add_scalar(f'{self.writer_prefix}/val/pred_mae', row['val_pred_mae'], ep)

        if self.ckpt_dir is None:
            return
        os.makedirs(self.ckpt_dir, exist_ok=True)
        payload = self._build_ckpt_payload(ep, val_mae)
        if self.last_ckpt_path is not None:
            torch.save(payload, self.last_ckpt_path)
        if improved and self.best_val_ckpt_path is not None:
            # Written from a fresh CPU copy; nothing in memory keeps aliasing
            # the live parameters, so later epochs cannot mutate the saved best.
            torch.save(payload, self.best_val_ckpt_path)
        save_every_n = int(getattr(self.cfg.VAL, 'SAVE_EVERY_N', 0) or 0)
        if self.cfg.VAL.SAVE_EVERY_EPOCH or (save_every_n > 0 and ep % save_every_n == 0):
            torch.save(payload, os.path.join(self.ckpt_dir, f'{self.entity.name}_seed{self.seed}_ep{ep}.pt'))

    def _build_ckpt_payload(self, ep, val_mae):
        """Self-contained checkpoint. Keys shared with the native payload
        (epoch, seed, entity, state_dict, cfg, mu, sd) keep their meaning;
        the rest records what is needed to restore and audit the epoch."""
        state_dict_cpu = {k: v.detach().to('cpu').clone() for k, v in self.model.state_dict().items()}
        opt_state = self.optimizer.state_dict()
        opt_state_cpu = {
            'state': {k: {kk: (vv.detach().to('cpu').clone() if torch.is_tensor(vv) else vv)
                          for kk, vv in st.items()} for k, st in opt_state['state'].items()},
            'param_groups': [dict(g) for g in opt_state['param_groups']],
        }
        rng_state = {
            'python': random.getstate(),
            'numpy_global': np.random.get_state(),
            'trainer_generator': self.rng.bit_generator.state,
            'torch_cpu': torch.get_rng_state().clone(),
        }
        if torch.cuda.is_available():
            rng_state['torch_cuda'] = [t.clone() for t in torch.cuda.get_rng_state_all()]
        return {
            'protocol': 'val_pred_mae_v2',
            'epoch': int(ep),
            'current_epoch': int(getattr(self.model, '_current_epoch', ep)),
            'seed': int(self.seed),
            'entity': self.entity.name,
            'val_mae': float(val_mae) if val_mae is not None else float('nan'),
            'best_val_mae_so_far': float(self.best_val_mae) if math.isfinite(self.best_val_mae) else float('nan'),
            'best_val_epoch_so_far': int(self.best_val_epoch) if self.best_val_epoch is not None else -1,
            'global_step': int(self._global_step),
            'state_dict': state_dict_cpu,
            'optimizer_state': opt_state_cpu,
            'scheduler_state': None,   # native trainer has no LR scheduler
            'rng_state': rng_state,
            'mu': np.asarray(self.entity.mu, dtype=np.float32),
            'sd': np.asarray(self.entity.sd, dtype=np.float32),
            'split_info': {
                'val_enabled': True,
                'val_frac': float(self.entity.val_frac),
                'val_boundary': int(self.entity.val_boundary),
                'T_train_sub': int(self.entity.T_train),
                'T_val': int(self.entity.T_val),
                'T_test': int(self.entity.T_test),
                'split_id': self.provenance.get('split_id'),
                'fit_protocol': 'train_sub_val_v2',
            },
            'cfg': self.cfg.dump(),
            'data_fingerprint': self.provenance.get('data_fingerprint'),
            'prior_cache_key': self.provenance.get('prior_cache_key'),
            'code_fingerprint': _git_fingerprint(),
            'torch_version': torch.__version__,
        }


def _git_fingerprint():
    """Best-effort commit hash, dirty flag and list of modified tracked files."""
    def _run(cmd):
        try:
            return subprocess.check_output(cmd, stderr=subprocess.DEVNULL,
                                           cwd=os.path.dirname(os.path.abspath(__file__))).decode().strip()
        except Exception:
            return None
    commit = _run(['git', 'rev-parse', 'HEAD'])
    status = _run(['git', 'status', '--porcelain', '--untracked-files=no'])
    # each porcelain line is '<XY> <path>'; _run strips the leading space of the
    # first line, so split on whitespace instead of slicing a fixed offset.
    modified = [l.split(None, 1)[1] for l in status.splitlines() if l.strip()] if status else []
    return {'commit': commit, 'dirty': (None if status is None else len(modified) > 0), 'modified_tracked': modified}
