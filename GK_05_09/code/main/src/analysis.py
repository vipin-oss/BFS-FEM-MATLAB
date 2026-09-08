"""Higher-level analyses: identifiability landscape, Monte Carlo, BIC, profile.

Implements sec:practical, sec:profile, sec:montecarlo, sec:bic.
All procedures follow calc:landscape, calc:mc, calc:profile, calc:bic.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares

from .model import Theta, Geometry
from .forward import forward, forward_and_jacobian
from .statistics import fisher, sigma_of, bic, CHI2_1_95
from .limits import TINY

# tab:models parameter counts
MODEL_K = {"fourier": 1, "mcv": 2, "nyiri": 2, "gk": 3}


def make_grid(cfg):
    return np.linspace(cfg["t_min"], cfg["t_max"], cfg["n_points"])


def landscape(B_values, cfg, geom):
    """calc:landscape: Fisher diagnostics versus B."""
    t = make_grid(cfg)
    rows = []
    for B in B_values:
        th = Theta.from_B(cfg["alpha"], cfg["tau_q"], B)
        r = fisher(th, t, geom, cfg["eta_noise"])
        rows.append(dict(B=B, cond=r["cond"], corr=r["corr_tq_k2"],
                         se_tau_q=r["se_tau_q"], se_kappa2=r["se_kappa2"],
                         se_alpha=r["se_alpha"], se_B=r["se_B"],
                         singular=r["singular"]))
    return rows


def _mc_trial(args):
    B, seed, cfg, geom = args
    t = make_grid(cfg)
    truth = Theta.from_B(cfg["alpha"], cfg["tau_q"], B)
    y0 = forward(truth, t, geom)
    sig = sigma_of(y0, cfg["eta_noise"])
    rng = np.random.default_rng(seed)                    # calc:mc PCG64
    y = y0 + rng.normal(0.0, sig, y0.size)

    def res(lp):
        return forward(Theta(*np.exp(lp)), t, geom) - y

    def jac(lp):
        th = Theta(*np.exp(lp))
        _, J = forward_and_jacobian(th, t, geom)
        return J * th.as_array()

    try:
        r = least_squares(res, np.log(truth.as_array()), jac=jac, method="lm",
                          xtol=1e-13, ftol=1e-13)       # calc:mc step 4
        return list(np.exp(r.x))
    except Exception:
        return None


def monte_carlo(B, cfg, geom, trials=None, seed_base=None, pool=None):
    """calc:mc. Started AT THE TRUTH (step 5) - stated, not hidden."""
    trials = trials or cfg["mc_trials"]
    seed_base = seed_base if seed_base is not None else cfg["mc_seed_base"]
    jobs = [(B, seed_base + i, cfg, geom) for i in range(trials)]
    res = list(pool.map(_mc_trial, jobs, chunksize=8)) if pool else \
          [_mc_trial(j) for j in jobs]
    est = np.array([r for r in res if r is not None])
    tq = est[:, 1] / cfg["tau_q"]
    al = est[:, 0] / cfg["alpha"]
    Bh = est[:, 2] / (est[:, 0] * est[:, 1]) / B
    q = lambda v, p: float(np.percentile(v, p))
    robust = (q(tq, 75) - q(tq, 25)) / 1.349 * 100.0     # calc:mc step 7
    return dict(B=B, n=int(len(est)), se_tau_q_robust_pct=robust,
                tq_p5=q(tq, 5), tq_p95=q(tq, 95),
                alpha_p5=q(al, 5), alpha_p95=q(al, 95),
                B_p5=q(Bh, 5), B_p95=q(Bh, 95))


def _fit_model(y, which, truth: Theta, t, geom, restarts=3):
    """Fit a constrained model (tab:models) and return its SSE."""
    def pred(a, tq, k2):
        return forward(Theta(a, max(tq, TINY), max(k2, TINY)), t, geom)

    if which == "fourier":
        f = lambda lp: pred(np.exp(lp[0]), TINY, TINY) - y
        p0 = np.log([truth.alpha])
    elif which == "mcv":
        f = lambda lp: pred(np.exp(lp[0]), np.exp(lp[1]), TINY) - y
        p0 = np.log([truth.alpha, truth.tau_q])
    elif which == "nyiri":
        f = lambda lp: pred(np.exp(lp[0]), TINY, np.exp(lp[1])) - y
        p0 = np.log([truth.alpha, truth.kappa2])
    else:
        f = lambda lp: pred(*np.exp(lp)) - y
        p0 = np.log(truth.as_array())
    best = np.inf
    for j in range(restarts):
        s0 = np.array(p0) if j == 0 else \
             np.array(p0) + np.random.default_rng(j).normal(0, 0.3, len(p0))
        try:
            r = least_squares(f, s0, method="lm", xtol=1e-12, ftol=1e-12)
            best = min(best, float(np.sum(r.fun ** 2)))
        except Exception:
            pass
    return best


def _bic_trial(args):
    B, seed, cfg, geom = args
    t = make_grid(cfg)
    truth = Theta.from_B(cfg["alpha"], cfg["tau_q"], B)
    y0 = forward(truth, t, geom)
    sig = sigma_of(y0, cfg["eta_noise"])
    y = y0 + np.random.default_rng(seed).normal(0.0, sig, y0.size)
    n = len(y)
    return {m: bic(_fit_model(y, m, truth, t, geom, cfg["bic_restarts"]), n,
                   MODEL_K[m]) for m in MODEL_K}


def bic_compare(B, cfg, geom, realisations=None, pool=None):
    """calc:bic: mean BIC over realisations, then Delta from the best model."""
    R = realisations or cfg["bic_realisations"]
    jobs = [(B, cfg["bic_seed_base"] + i, cfg, geom) for i in range(R)]
    res = list(pool.map(_bic_trial, jobs, chunksize=2)) if pool else \
          [_bic_trial(j) for j in jobs]
    mean = {m: float(np.nanmean([r[m] for r in res])) for m in MODEL_K}
    lo = min(mean.values())
    d = {m: mean[m] - lo for m in mean}
    return dict(B=B, delta=d, selected=min(d, key=d.get), mean_bic=mean)


def profile(B, cfg, geom, seed=4242, nodes=None, half=None):
    """calc:profile: profile likelihood in tau_q."""
    nodes = nodes or cfg["profile_nodes"]
    half = half or cfg["profile_log_half_width"]
    t = make_grid(cfg)
    truth = Theta.from_B(cfg["alpha"], cfg["tau_q"], B)
    y0 = forward(truth, t, geom)
    sig = sigma_of(y0, cfg["eta_noise"])
    y = y0 + np.random.default_rng(seed).normal(0.0, sig, y0.size)
    grid = cfg["tau_q"] * np.logspace(-half, half, nodes)

    def sse_fixed(tau):
        """Profile the nuisance parameters at fixed tau_q.

        MULTI-START IS REQUIRED. Near resonance the objective has a long flat
        valley along the ray kappa2 = alpha*tau_q*B, so a start anchored at the
        TRUE kappa2 becomes a poor guess once tau_q is moved far from truth
        (kappa2 must scale with tau_q to stay on the valley floor). Starts are
        therefore placed on several rays through the current tau_q, plus the
        fixed true-parameter start. Without this the profile does not converge
        and reports a spurious monotone curve.
        """
        starts = [np.log([truth.alpha, cfg["alpha"] * tau * Bs])
                  for Bs in (B, 1.0, 0.5, 2.0)]
        starts.append(np.log([truth.alpha, truth.kappa2]))
        best = np.inf
        for s0 in starts:
            try:
                r = least_squares(
                    lambda lp: forward(Theta(np.exp(lp[0]), tau, np.exp(lp[1])),
                                       t, geom) - y,
                    s0, method="lm", xtol=1e-13, ftol=1e-13)
                best = min(best, float(np.sum(r.fun ** 2)))
            except Exception:
                pass
        return best

    sse = np.array([sse_fixed(g) for g in grid])
    delta = (sse - np.nanmin(sse)) / sig ** 2            # eq:profile-stat
    ok = grid[delta <= CHI2_1_95]                        # eq:profile-threshold
    if len(ok) == 0:
        return dict(B=B, grid=grid, delta=delta, lo=None, hi=None,
                    width_factor=None, grid_limited=False)
    lo, hi = float(ok.min()), float(ok.max())
    return dict(B=B, grid=grid, delta=delta, lo=lo, hi=hi,
                width_factor=hi / lo,
                grid_limited=bool(lo <= grid[0] * 1.001 and hi >= grid[-1] * 0.999))
