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
                 'weight_sha256': array_sha256(w_new), 'gate_sha256': array_sha256(g_new), **stats})
    return w_new, g_new, info
