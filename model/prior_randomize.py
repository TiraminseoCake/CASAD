"""P3 structural ablation: per-seed prior preparation.

``prepare_seed_prior`` is called once per (entity, seed) before the model is built. With the defaults
(PRIOR.TYPE != 'none', PRIOR.RANDOMIZE == 'none') it returns the loaded prior arrays unchanged, so the
original code path is untouched. With RANDOMIZE == 'degree_preserving_v1' the cross edges of the loaded prior
are rewired within each lag (sparsity/lag-matched random prior). With TYPE == 'none' there is no prior at all.

Only a local ``numpy.random.Generator`` seeded from (salt, dataset, entity, seed) is used, never the global
torch / numpy / python RNG, so model initialization and batch order are the same as without randomization.
"""
import hashlib

import numpy as np

RANDOMIZE_MODES = ('none', 'degree_preserving_v1')


def array_sha256(a) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def randomize_seed(salt: str, dataset: str, entity: str, seed: int) -> int:
    h = hashlib.sha256(f'{salt}|{dataset}|{entity}|{int(seed)}'.encode('utf-8')).digest()
    return int.from_bytes(h[:8], 'little')


def _cross_mask(w_tau: np.ndarray, g_tau: np.ndarray) -> np.ndarray:
    m = (g_tau > 0) | (w_tau > 0)
    np.fill_diagonal(m, False)
    return m


def degree_preserving_rewire(te_weight, te_gate, rng: np.random.Generator, swaps_per_edge: int = 10):
    """Rewire the cross edges (src != tgt) of a prior within each lag.

    Arrays are [tau_max, src, tgt]. Every incoming edge of a target is a *slot* that keeps its (weight, gate)
    values; a double-edge swap exchanges the sources of two slots: (a->b, v1), (c->d, v2) become (c->b, v1),
    (a->d, v2). A swap is rejected when it would create a self edge or a duplicate edge. Preserved exactly:
    per-lag in-degree of every target, per-lag out-degree of every source, every self edge (src == tgt at every
    lag, including the forced lag-1 self loop), and the multiset of (weight, gate) values of every target, hence
    its column sum. Destroyed: which source feeds which target among the cross edges.
    """
    w = np.asarray(te_weight)
    g = np.asarray(te_gate)
    if w.shape != g.shape or w.ndim != 3 or w.shape[1] != w.shape[2]:
        raise ValueError(f'prior arrays must be [tau, N, N] with equal shapes; got {w.shape} and {g.shape}')
    T, N, _ = w.shape
    w_new = np.zeros_like(w)
    g_new = np.zeros_like(g)
    diag = np.arange(N)
    w_new[:, diag, diag] = w[:, diag, diag]
    g_new[:, diag, diag] = g[:, diag, diag]
    per_lag = []
    for tau in range(T):
        src, tgt = np.nonzero(_cross_mask(w[tau], g[tau]))
        E = int(src.size)
        val_w = w[tau, src, tgt].copy()
        val_g = g[tau, src, tgt].copy()
        s = src.copy()
        present = set(zip(s.tolist(), tgt.tolist()))
        attempts = int(swaps_per_edge) * E if E >= 2 else 0
        accepted = 0
        for _ in range(attempts):
            i, j = (int(x) for x in rng.integers(0, E, size=2))
            if i == j:
                continue
            a, b, c, d = int(s[i]), int(tgt[i]), int(s[j]), int(tgt[j])
            if a == c or b == d or c == b or a == d:
                continue
            if (c, b) in present or (a, d) in present:
                continue
            present.difference_update(((a, b), (c, d)))
            present.update(((c, b), (a, d)))
            s[i], s[j] = c, a
            accepted += 1
        w_new[tau, s, tgt] = val_w
        g_new[tau, s, tgt] = val_g
        orig = set(zip(src.tolist(), tgt.tolist()))
        new = set(zip(s.tolist(), tgt.tolist()))
        union = orig | new
        per_lag.append({'tau': tau + 1, 'cross_edges': E, 'swap_attempts': attempts, 'swaps_accepted': accepted,
                        'slots_with_new_source': int(np.sum(s != src)),
                        'jaccard_with_input': (len(orig & new) / len(union)) if union else 1.0})
    return w_new, g_new, {'per_lag': per_lag, 'checks': rewire_checks(w, g, w_new, g_new)}


def rewire_checks(w, g, w_new, g_new) -> dict:
    """Invariants that degree_preserving_rewire must keep (all must be True)."""
    T, N, _ = w.shape
    diag = np.arange(N)
    ok_in, ok_out, ok_vals = True, True, True
    for tau in range(T):
        m0, m1 = _cross_mask(w[tau], g[tau]), _cross_mask(w_new[tau], g_new[tau])
        ok_in &= bool(np.array_equal(m0.sum(axis=0), m1.sum(axis=0)))
        ok_out &= bool(np.array_equal(m0.sum(axis=1), m1.sum(axis=1)))
        for t in range(N):
            v0 = sorted(zip(w[tau, m0[:, t], t].tolist(), g[tau, m0[:, t], t].tolist()))
            v1 = sorted(zip(w_new[tau, m1[:, t], t].tolist(), g_new[tau, m1[:, t], t].tolist()))
            ok_vals &= (v0 == v1)
    cs0 = w.reshape(T * N, N).sum(axis=0)
    cs1 = w_new.reshape(T * N, N).sum(axis=0)
    return {
        'in_degree_per_lag_preserved': ok_in,
        'out_degree_per_lag_preserved': ok_out,
        'target_slot_values_preserved': ok_vals,
        'self_edges_preserved': bool(np.array_equal(w[:, diag, diag], w_new[:, diag, diag])
                                     and np.array_equal(g[:, diag, diag], g_new[:, diag, diag])),
        'column_sums_max_abs_diff': float(np.max(np.abs(cs0 - cs1))) if cs0.size else 0.0,
        'n_half_gates_preserved': int(np.sum(g == 0.5)) == int(np.sum(g_new == 0.5)),
        'n_nonzero_gates_preserved': int(np.sum(g > 0)) == int(np.sum(g_new > 0)),
    }


def _edge_mask(w_tau, g_tau):
    return (g_tau > 0) | (w_tau > 0)


def _multiset_equal(a, b, mask_a, mask_b, axis_groups):
    """True if, for every group index, the sorted values of a (where mask_a) equal those of b (where mask_b)."""
    for idx in axis_groups:
        if sorted(a[idx][mask_a[idx]].tolist()) != sorted(b[idx][mask_b[idx]].tolist()):
            return False
    return True


def _rank(x):
    r = np.empty(len(x)); r[np.argsort(x, kind='mergesort')] = np.arange(len(x)); return r


def _corr(x, y):
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def rewire_report(w, g, w_new, g_new) -> dict:
    """Which statistics of the input prior the randomized prior keeps EXACTLY, and how much the others change.

    Degrees and edge counts include self edges unless named 'cross'. 'strength' = sum of prior weights. Arrays are
    [tau, src, tgt]; weights are the (normalized) prior weights as stored in the cache.
    """
    w, g, w_new, g_new = (np.asarray(x) for x in (w, g, w_new, g_new))
    T, N, _ = w.shape
    m0 = np.stack([_edge_mask(w[t], g[t]) for t in range(T)])
    m1 = np.stack([_edge_mask(w_new[t], g_new[t]) for t in range(T)])
    c0 = np.stack([_cross_mask(w[t], g[t]) for t in range(T)])
    c1 = np.stack([_cross_mask(w_new[t], g_new[t]) for t in range(T)])
    d = np.arange(N)
    lag_tgt = [(t, slice(None), j) for t in range(T) for j in range(N)]
    lag = [(t,) for t in range(T)]
    lag_src = [(t, i, slice(None)) for t in range(T) for i in range(N)]
    src = [(slice(None), i, slice(None)) for i in range(N)]
    exact = {
        'out_degree_per_lag_source': bool(np.array_equal(m0.sum(2), m1.sum(2))),
        'out_degree_per_source_all_lags': bool(np.array_equal(m0.sum((0, 2)), m1.sum((0, 2)))),
        'in_degree_per_lag_target': bool(np.array_equal(m0.sum(1), m1.sum(1))),
        'edges_per_lag': bool(np.array_equal(m0.sum((1, 2)), m1.sum((1, 2)))),
        'cross_edges_per_lag': bool(np.array_equal(c0.sum((1, 2)), c1.sum((1, 2)))),
        'self_edges_every_lag': bool(np.array_equal(w[:, d, d], w_new[:, d, d]) and np.array_equal(g[:, d, d], g_new[:, d, d])),
        'weight_multiset_per_lag_target': _multiset_equal(w, w_new, m0, m1, lag_tgt),
        'gate_multiset_per_lag_target': _multiset_equal(g, g_new, m0, m1, lag_tgt),
        'weight_multiset_per_lag': _multiset_equal(w, w_new, m0, m1, lag),
        'weight_multiset_global': sorted(w[m0].tolist()) == sorted(w_new[m1].tolist()),
        'in_strength_per_lag_target': bool(np.allclose(w.sum(1), w_new.sum(1), rtol=0, atol=1e-6)),
        'column_sum_per_target': bool(np.allclose(w.reshape(T * N, N).sum(0), w_new.reshape(T * N, N).sum(0), rtol=0, atol=1e-6)),
        'half_gate_count': int(np.sum(g == 0.5)) == int(np.sum(g_new == 0.5)),
        # expected False (reported, not required):
        'weight_multiset_per_lag_source': _multiset_equal(w, w_new, m0, m1, lag_src),
        'weight_multiset_per_source': _multiset_equal(w, w_new, m0, m1, src),
        'out_strength_per_lag_source': bool(np.allclose(w.sum(2), w_new.sum(2), rtol=0, atol=1e-6)),
    }
    s0, s1 = w.sum(2), w_new.sum(2)                       # out-strength [tau, src]
    act = m0.sum(2) > 0
    tot0, tot1 = s0.sum(0), s1.sum(0)

    def recip(c):
        return int(sum(np.sum(np.triu(c[t] & c[t].T, 1)) for t in range(T)))

    def multi_lag(c):
        return int(np.sum(c.sum(0) >= 2))

    def sym_half(gg, c):
        return int(sum(np.sum(np.triu((gg[t] == 0.5) & (gg[t].T == 0.5) & c[t], 1)) for t in range(T)))
    inter, union = int(np.sum(c0 & c1)), int(np.sum(c0 | c1))
    changed = {
        'out_strength_per_lag_source_corr': _corr(s0[act], s1[act]),
        'out_strength_per_lag_source_spearman': _corr(_rank(s0[act]), _rank(s1[act])) if act.sum() >= 3 else None,
        'out_strength_per_lag_source_rel_l1': float(np.abs(s1 - s0).sum() / max(s0.sum(), 1e-12)),
        'out_strength_per_source_corr': _corr(tot0, tot1),
        'reciprocal_cross_pairs': [recip(c0), recip(c1)],                 # (i->j and j->i at the same lag) input, random
        'pairs_linked_at_2plus_lags': [multi_lag(c0), multi_lag(c1)],     # same (src, tgt) at >= 2 lags
        'symmetric_half_gate_pairs': [sym_half(g, c0), sym_half(g_new, c1)],
        'cross_support_jaccard': (inter / union) if union else 1.0,
        'cross_edges_kept_fraction': (inter / int(c0.sum())) if c0.sum() else 1.0,
    }
    return {'exact': exact, 'changed': changed}


def prepare_seed_prior(cfg, te_weight_np, te_gate_np, entity_name: str, seed: int):
    """Returns (te_weight, te_gate, prior_info) for one (entity, seed); te_* are None for PRIOR.TYPE='none'."""
    p = cfg.PICAAD.PRIOR
    ptype, mode = str(p.TYPE), str(p.RANDOMIZE)
    if mode not in RANDOMIZE_MODES:
        raise ValueError(f'unknown PICAAD.PRIOR.RANDOMIZE {mode!r}; expected one of {RANDOMIZE_MODES}')
    if ptype == 'none':
        if mode != 'none':
            raise ValueError("PICAAD.PRIOR.RANDOMIZE needs a loaded prior; it cannot be combined with PRIOR.TYPE='none'")
        if te_weight_np is not None or te_gate_np is not None:
            raise ValueError("PRIOR.TYPE='none' but prior arrays were supplied")
        return None, None, {'type': 'none', 'randomize': 'none'}
    if te_weight_np is None or te_gate_np is None:
        raise ValueError(f'PRIOR.TYPE={ptype!r} requires prior arrays')
    info = {'type': ptype, 'randomize': mode,
            'input_weight_sha256': array_sha256(te_weight_np), 'input_gate_sha256': array_sha256(te_gate_np)}
    if mode == 'none':
        info.update({'weight_sha256': info['input_weight_sha256'], 'gate_sha256': info['input_gate_sha256']})
        return te_weight_np, te_gate_np, info
    rseed = randomize_seed(str(p.RANDOMIZE_SALT), str(cfg.DATA.NAME), entity_name, seed)
    rng = np.random.default_rng(rseed)
    w_new, g_new, stats = degree_preserving_rewire(te_weight_np, te_gate_np, rng, int(p.RANDOMIZE_SWAPS))
    bad = [k for k, v in stats['checks'].items() if k != 'column_sums_max_abs_diff' and v is not True]
    if bad or stats['checks']['column_sums_max_abs_diff'] > 1e-5:
        raise RuntimeError(f'randomized prior violates invariants {bad} / {stats["checks"]}')
    info.update({'salt': str(p.RANDOMIZE_SALT), 'rng_seed': rseed, 'swaps_per_edge': int(p.RANDOMIZE_SWAPS),
                 'weight_sha256': array_sha256(w_new), 'gate_sha256': array_sha256(g_new), **stats,
                 'report': rewire_report(te_weight_np, te_gate_np, w_new, g_new)})
    return w_new, g_new, info
