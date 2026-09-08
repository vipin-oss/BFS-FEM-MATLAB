"""Laplace-domain objects: propagation factor, kernel, pulse, Talbot nodes.

Implements:
  eq:m2            m^2(s) = s(1+tau_q s)/(alpha + kappa2 s)
  def:branch       principal branch, Re m > 0
  eq:That          T_hat(x,s)
  eq:That-rear     T_hat(1,s)
  eq:Q0            pulse transform (analytic; poles removable, eq:removable)
  eq:factorisation T_hat = K_hat * Q0_hat
  eq:dm-dtq        dm/dtau_q
  eq:dm-dk2        dm/dkappa2
  eq:dKdm          dK_hat/dm = (1 - m coth m)/(tau_D s sinh m)
  eq:dK-dparams    chain rule to parameter derivatives
  eq:talbot-nodes  fixed-Talbot contour
  eq:tstar         t* = M tau_Delta / 10  (pole-collision time of the SPLIT form)

THIS FILE CONTAINS THE ONLY IMPLEMENTATION OF m^2(s) IN THE PROGRAM.
SOURCE: manuscript/GK_COMPLETE_CALCULATIONS.tex sections 5, 11, 21.
"""
from __future__ import annotations
import numpy as np

_UNDERFLOW = 1e-300


def m2(s, tau_q_hat, kappa2_hat, alpha_hat=1.0):
    """eq:m2. Authoritative. alpha_hat is 1 in the scaled problem (der:nd-flux)."""
    return s * (1.0 + tau_q_hat * s) / (alpha_hat + kappa2_hat * s)


def m_of(s, tau_q_hat, kappa2_hat, alpha_hat=1.0):
    """m(s) on the principal branch, def:branch (numpy sqrt gives Re>=0)."""
    return np.sqrt(m2(s, tau_q_hat, kappa2_hat, alpha_hat))


def csch(m):
    """1/sinh(m), overflow-safe: 2 e^-m /(1 - e^-2m). sec:program overflow guard."""
    e = np.exp(-m)
    den = 1.0 - e * e
    safe = np.where(np.abs(den) < _UNDERFLOW, 1.0, den)
    return np.where(np.abs(den) < _UNDERFLOW, 0.0 + 0j, 2.0 * e / safe)


def coth(m):
    """coth(m) = (1+e^-2m)/(1-e^-2m). sec:program overflow guard."""
    e2 = np.exp(-2.0 * m)
    den = 1.0 - e2
    safe = np.where(np.abs(den) < _UNDERFLOW, 1.0, den)
    return np.where(np.abs(den) < _UNDERFLOW, 1.0 + 0j, (1.0 + e2) / safe)


def K_hat(s, tau_q_hat, kappa2_hat, tau_D_hat):
    """eq:factorisation kernel: K = m/(tau_D s sinh m). Pole-free on iR."""
    m = m_of(s, tau_q_hat, kappa2_hat)
    return m * csch(m) / (tau_D_hat * s)


def dK_hat_dparams(s, tau_q_hat, kappa2_hat, tau_D_hat):
    """(dK/dtau_q_hat, dK/dkappa2_hat) via eq:dKdm and eq:dK-dparams."""
    m = m_of(s, tau_q_hat, kappa2_hat)
    dK_dm = csch(m) * (1.0 - m * coth(m)) / (tau_D_hat * s)
    denom = 1.0 + kappa2_hat * s                      # alpha_hat = 1
    dm_dtq = s ** 2 / (2.0 * m * denom)               # eq:dm-dtq
    dm_dk2 = -m * s / (2.0 * denom)                   # eq:dm-dk2
    return dK_dm * dm_dtq, dK_dm * dm_dk2


def Q0_hat(s, tau_D_hat):
    """eq:Q0 pulse transform. Provided for completeness and for the
    DELIBERATELY-WRONG split solver used by test T16; the production path
    never inverts this factor (res:talbot)."""
    w = 2.0 * np.pi / tau_D_hat
    return w ** 2 * (1.0 - np.exp(-s * tau_D_hat)) / (s * (s ** 2 + w ** 2))


def talbot_nodes(M: int, t: float):
    """eq:talbot-nodes. Returns (s0, s_k, weights_k, r).

    sec:program: M MUST be odd. An even M places theta=pi/2 on the contour,
    i.e. a node on the imaginary axis, which collides with the removable pulse
    pole at t* = M tau_Delta/10 (eq:tstar) whenever the split form is used.
    """
    k = np.arange(1, M)
    th = k * np.pi / M
    cot = 1.0 / np.tan(th)
    sig = th + (th * cot - 1.0) * cot
    r = 2.0 * M / (5.0 * t)
    s = r * th * (cot + 1j)
    return r + 0j, s, sig, r


def t_star(M: int, tau_D_hat: float) -> float:
    """eq:tstar: the split-form failure time. Diagnostic only."""
    return M * tau_D_hat / 10.0
