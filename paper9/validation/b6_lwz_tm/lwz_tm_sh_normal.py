#!/usr/bin/env python3
"""Independent 1-D TM for LWZ2016 anti-plane SH, *normal incidence* (xi=0).

Source: Li, Wei & Zhou, Acta Mech. 227:1005-1023 (2016), PDF li2015.pdf.
Not Case-H, not Li 2023/2024.

Acceptance (declared *before* execution):
  Level 1 homogeneous: for each prescribed bulk wavenumber sigma,
  |lambda_closest - exp(i*sigma*a)| / 1  < 1e-8
  and |k_Bloch - sigma|/max(sigma, 1e-12) < 1e-8
  where k_Bloch = arg(lambda)/a on the propagating pair.
"""
from __future__ import annotations

import numpy as np

# ---- closed form (14.1), PDF p.4 ----


def omega_from_sigma(sigma, Vs, c, d):
    """(14.1) travelling SH: omega^2 = sigma^2 Vs^2 (1+c sigma^2) / (1 + d^2 sigma^2 / 3)."""
    s2 = sigma**2
    return float(np.sqrt(s2 * Vs**2 * (1.0 + c * s2) / (1.0 + (d**2 / 3.0) * s2)))


def sigma_tau_from_omega(omega, Vs, c, d):
    """sigma_sh, tau_sh after (12), PDF p.4. Real positive branches."""
    w2 = omega**2
    Vs2 = Vs**2
    ms = w2 * d**2 / (3.0 * Vs2)
    disc = (1.0 - ms) ** 2 + 4.0 * c * w2 / Vs2
    Delta = np.sqrt(disc)
    sig2 = (Delta - (1.0 - ms)) / (2.0 * c)
    tau2 = (Delta + (1.0 - ms)) / (2.0 * c)
    # numerical floor
    sig2 = max(float(np.real(sig2)), 0.0)
    tau2 = max(float(np.real(tau2)), 0.0)
    return np.sqrt(sig2), np.sqrt(tau2)


def layer_T_sh_normal(omega, a_j, c_j, d_j, mu_j, rho_j):
    """Appendix 3, r=s, epsilon=mu. T = t / (sigma^2 + tau^2). PDF p.18."""
    Vs = np.sqrt(mu_j / rho_j)
    sig, tau = sigma_tau_from_omega(omega, Vs, c_j, d_j)
    if sig == 0.0 or tau == 0.0 or c_j == 0.0:
        raise ValueError("degenerate sigma/tau/c")
    eps = mu_j
    sa, ca = np.sin(sig * a_j), np.cos(sig * a_j)
    sh, ch = np.sinh(tau * a_j), np.cosh(tau * a_j)
    t = np.zeros((4, 4), dtype=np.complex128)
    t[0, 0] = sig**2 * ch + tau**2 * ca
    t[0, 1] = sig * sa + tau * sh
    t[0, 2] = (tau * sa - sig * sh) / (c_j * eps * sig * tau)
    t[0, 3] = (ch - ca) / (c_j * eps)
    t[1, 0] = sig**2 * tau * sh - tau**2 * sig * sa
    t[1, 1] = sig**2 * ca + tau**2 * ch
    t[1, 2] = (ca - ch) / (c_j * eps)
    t[1, 3] = (tau * sh + sig * sa) / (c_j * eps)
    t[2, 0] = -c_j * eps * sig * tau * (sig**3 * sh + tau**3 * sa)
    t[2, 1] = c_j * eps * sig**2 * tau**2 * (ca - ch)
    t[2, 2] = tau**2 * ca + sig**2 * ch
    t[2, 3] = tau * sig * (tau * sa - sig * sh)
    t[3, 0] = c_j * eps * sig**2 * tau**2 * (ch - ca)
    t[3, 1] = c_j * eps * (tau**3 * sh - sig**3 * sa)
    t[3, 2] = -tau * sh - sig * sa
    t[3, 3] = tau**2 * ch + sig**2 * ca
    T = t / (sig**2 + tau**2)
    return T, sig, tau


def bloch_eigenvalues(T):
    return np.linalg.eigvals(T)


def propagating_k_from_T(T, a, sigma_ref=None):
    """Bloch k from eigenvalues with |lambda|~1, nearest to exp(i sigma a) if given."""
    w = bloch_eigenvalues(T)
    mag = np.abs(w)
    # unimodular pair
    idx = np.argsort(np.abs(mag - 1.0))[:2]
    cand = w[idx]
    if sigma_ref is not None:
        target = np.exp(1j * sigma_ref * a)
        j = int(np.argmin(np.abs(cand - target)))
        lam = cand[j]
        dist = abs(lam - target)
    else:
        # take arg in (-pi, pi]
        lam = cand[np.argmax(np.angle(cand))]  # positive k
        dist = min(abs(mag[idx] - 1.0))
    k = float(np.angle(lam) / a)
    return k, lam, float(dist)


def min_svd_residual(T, k, a):
    A = T - np.exp(1j * k * a) * np.eye(4, dtype=np.complex128)
    s = np.linalg.svd(A, compute_uv=False)
    return float(np.min(s)), float(np.linalg.cond(A))


def bilayer_T(omega, a1, a2, c1, c2, d1, d2, mu1, mu2, rho1, rho2):
    TA, *_ = layer_T_sh_normal(omega, a1, c1, d1, mu1, rho1)
    TB, *_ = layer_T_sh_normal(omega, a2, c2, d2, mu2, rho2)
    return TB @ TA  # (29) V_B^R = T_B T_A V_A^L


def scan_omega_for_k(k, a, a1, a2, c1, c2, d1, d2, mu1, mu2, rho1, rho2, omegas):
    """Acoustic-biased root: lowest-omega local min of svd residual."""
    recs = []
    for w in omegas:
        try:
            T = bilayer_T(w, a1, a2, c1, c2, d1, d2, mu1, mu2, rho1, rho2)
        except (ValueError, np.linalg.LinAlgError):
            continue
        res, cond = min_svd_residual(T, k, a)
        recs.append((w, res, cond))
    if not recs:
        return None, recs
    resv = np.array([r[1] for r in recs])
    # local minima
    loc = []
    for i in range(1, len(recs) - 1):
        if recs[i][1] <= recs[i - 1][1] and recs[i][1] <= recs[i + 1][1]:
            loc.append(recs[i])
    if not loc:
        loc = [min(recs, key=lambda t: t[1])]
    floor = min(t[1] for t in loc)
    good = [t for t in loc if t[1] <= 20.0 * floor + 1e-12]
    best = min(good, key=lambda t: t[0])  # lowest omega among decent local mins
    # parabolic refine on residual vs omega (3 nearest recs)
    ws = np.array([r[0] for r in recs])
    i = int(np.argmin(np.abs(ws - best[0])))
    if 0 < i < len(recs) - 1:
        x0, x1, x2 = recs[i - 1][0], recs[i][0], recs[i + 1][0]
        y0, y1, y2 = recs[i - 1][1], recs[i][1], recs[i + 1][1]
        denom = (x0 - x1) * (x0 - x2) * (x1 - x2)
        if abs(denom) > 0:
            a = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / denom
            b = (x2**2 * (y0 - y1) + x1**2 * (y2 - y0) + x0**2 * (y1 - y2)) / denom
            if a > 0:
                xv = -b / (2 * a)
                if min(x0, x2) <= xv <= max(x0, x2):
                    best = (float(xv), float(best[1]), float(best[2]))
    return best, recs
