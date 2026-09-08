"""DELIBERATELY DEFECTIVE reference solver: the split / second-shift form.

This is NOT part of the scientific pipeline. res:talbot PROHIBITS it. It is
implemented solely so acceptance test T16 can demonstrate the pole collision
at t* = M tau_Delta/10 (eq:tstar) that motivates the convolution formulation.

Never import this from any production module.
"""
from __future__ import annotations
import numpy as np
from .laplace import m_of, csch


def _talbot(fn, tvec, M):
    tvec = np.atleast_1d(np.asarray(tvec, float))
    out = np.zeros_like(tvec)
    for i, ti in enumerate(tvec):
        if ti <= 0:
            continue
        r = 2.0 * M / (5.0 * ti)
        acc = 0.5 * np.exp(r * ti) * np.real(fn(r + 0j))
        for k in range(1, M):
            th = k * np.pi / M
            cot = 1.0 / np.tan(th)
            s = r * th * (cot + 1j)
            sig = th + (th * cot - 1.0) * cot
            acc += np.real(np.exp(ti * s) * (1.0 + 1j * sig) * fn(s))
        out[i] = (r / M) * acc
    return out


def solve_split(tvec, tau_q_hat, kappa2_hat, tau_D_hat, M=40):
    """Split form: inverts w^2/(s(s^2+w^2)) ALONE, reinstating the poles that
    eq:removable shows are cancelled in the exact transform."""
    w = 2.0 * np.pi / tau_D_hat

    def G(s):
        m = m_of(s, tau_q_hat, kappa2_hat)
        return m * w ** 2 * csch(m) / (tau_D_hat * s ** 2 * (s ** 2 + w ** 2))

    tvec = np.atleast_1d(np.asarray(tvec, float))
    g1 = _talbot(G, tvec, M)
    ts = tvec - tau_D_hat
    g2 = np.zeros_like(tvec)
    msk = ts > 0
    if msk.any():
        g2[msk] = _talbot(G, ts[msk], M)
    return g1 - g2
