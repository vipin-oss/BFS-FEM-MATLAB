"""Estimation and statistical diagnostics.

Implements:
  eq:obsmodel     y_i = T(1,t_i) + eps,  eps ~ N(0, sigma^2)
  eq:sigma-def    sigma = eta * (max T - min T)
  eq:logJ         log-parameter Jacobian
  eq:fisher-def   F = J^T J / sigma^2
  eq:seB          delta-method standard error of B
  eq:sse          objective
  eq:profile-def / eq:profile-stat / eq:profile-threshold
  eq:bic          BIC = n ln(SSE/n) + k ln n
  eq:band-def     band where s.e.(tau_q) exceeds a target

SOURCE: GK_COMPLETE_CALCULATIONS.tex sections 11, 13, 14, 15, 16.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2

from .model import Theta, Geometry, kappa2_of
from .forward import forward, forward_and_jacobian

CHI2_1_95 = float(chi2.ppf(0.95, 1))     # eq:profile-threshold -> 3.841


def sigma_of(y, eta):
    """eq:sigma-def."""
    return eta * (np.max(y) - np.min(y))


def fisher(theta: Theta, t_phys, geom: Geometry, eta):
    """eq:logJ + eq:fisher-def. Returns dict of diagnostics."""
    y, J = forward_and_jacobian(theta, t_phys, geom)
    sig = sigma_of(y, eta)
    Jl = J * theta.as_array()                       # eq:logJ
    F = Jl.T @ Jl / sig ** 2                        # eq:fisher-def
    out = {"sigma": sig, "F": F, "cond": float(np.linalg.cond(F))}
    try:
        C = np.linalg.inv(F)
        d = np.diag(C)
        if np.any(d <= 0) or not np.all(np.isfinite(d)):
            raise np.linalg.LinAlgError
        se = np.sqrt(d) * 100.0
        g = np.array([-1.0, -1.0, 1.0])             # eq:seB: lnB = lnk2-lna-lntq
        out.update(se_alpha=float(se[0]), se_tau_q=float(se[1]),
                   se_kappa2=float(se[2]),
                   corr_tq_k2=float(C[1, 2] / np.sqrt(C[1, 1] * C[2, 2])),
                   se_B=float(np.sqrt(max(g @ C @ g, 0.0)) * 100.0),
                   singular=False)
    except np.linalg.LinAlgError:
        out.update(se_alpha=np.nan, se_tau_q=np.inf, se_kappa2=np.inf,
                   corr_tq_k2=np.nan, se_B=np.nan, singular=True)
    return out


def se_tau_q_at_B(B, t_phys, geom: Geometry, eta, alpha=1.0, tau_q=0.03):
    """Fisher relative s.e. of tau_q at a given B. Used by eq:band-def."""
    th = Theta.from_B(alpha, tau_q, B)
    r = fisher(th, t_phys, geom, eta)
    v = r["se_tau_q"]
    return np.inf if not np.isfinite(v) else v


def band_edge(target, lo, hi, t_phys, geom, eta, iters=50, **kw):
    """eq:band-def: bisection for the B at which s.e.(tau_q) = target.

    Bracket [lo,hi] must straddle the edge with lo inside the band.
    """
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if se_tau_q_at_B(mid, t_phys, geom, eta, **kw) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def fit(y_obs, theta0: Theta, t_phys, geom: Geometry, free=("alpha", "tau_q", "kappa2"),
        fixed=None, start=None, xtol=1e-13, ftol=1e-13):
    """eq:sse minimised over log-parameters, analytic Jacobian (eq:cfg-5)."""
    names = ["alpha", "tau_q", "kappa2"]
    base = dict(zip(names, theta0.as_array()))
    if fixed:
        base.update(fixed)
    idx = [names.index(f) for f in free]
    p0 = np.log([base[f] for f in free]) if start is None else np.log(start)

    def build(lp):
        v = dict(base)
        for f, x in zip(free, np.exp(lp)):
            v[f] = x
        return Theta(v["alpha"], v["tau_q"], v["kappa2"])

    def res(lp):
        return forward(build(lp), t_phys, geom) - y_obs

    def jac(lp):
        th = build(lp)
        _, J = forward_and_jacobian(th, t_phys, geom)
        return (J * th.as_array())[:, idx]

    r = least_squares(res, p0, jac=jac, method="lm", xtol=xtol, ftol=ftol)
    return build(r.x), float(np.sum(r.fun ** 2))


def bic(sse, n, k):
    """eq:bic."""
    return n * np.log(sse / n) + k * np.log(n)


def profile_tau_q(y_obs, theta_true: Theta, t_phys, geom: Geometry, grid):
    """eq:profile-def and eq:profile-stat. Returns (grid, Delta)."""
    sse = []
    for tau in grid:
        best = np.inf
        for jit in (0.0, 0.2):
            st = np.array([theta_true.alpha, theta_true.kappa2]) * np.exp(
                np.array([jit, -jit]))
            try:
                _, s = fit(y_obs, theta_true, t_phys, geom,
                           free=("alpha", "kappa2"), fixed={"tau_q": tau},
                           start=st)
                best = min(best, s)
            except Exception:
                pass
        sse.append(best)
    sse = np.array(sse)
    y0 = forward(theta_true, t_phys, geom)
    return np.array(grid), sse
