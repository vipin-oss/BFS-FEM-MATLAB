"""Limiting cases and the truncated eigenfunction series.

Implements:
  eq:lim-fourier   tau_q,kappa2 -> 0
  eq:lim-mcv       kappa2 -> 0
  eq:lim-nyiri     tau_q -> 0
  eq:mcv-speed     v = sqrt(alpha/tau_q)
  eq:series-TN     truncated series (der:series), used ONLY for anchor Fig.2
  eq:series-a0, eq:series-an, eq:series-I

SOURCE: GK_COMPLETE_CALCULATIONS.tex sections 7 and 20.3.
"""
from __future__ import annotations
import numpy as np

TINY = 1e-12   # numerical stand-in for an exactly-zero constrained parameter


def m2_limit(s, which, tau_q_hat=0.0, kappa2_hat=0.0, alpha_hat=1.0):
    """Closed forms of eq:lim-fourier / eq:lim-mcv / eq:lim-nyiri."""
    if which == "fourier":
        return s / alpha_hat
    if which == "mcv":
        return s * (1.0 + tau_q_hat * s) / alpha_hat
    if which == "nyiri":
        return s / (alpha_hat + kappa2_hat * s)
    if which == "gk":
        return s * (1.0 + tau_q_hat * s) / (alpha_hat + kappa2_hat * s)
    raise ValueError(f"unknown limit '{which}'")


def mcv_wave_speed(alpha, tau_q):
    """eq:mcv-speed."""
    return np.sqrt(alpha / tau_q)


def T_series(t_hat, N, tau_D_hat):
    """eq:series-TN: rear-face temperature truncated at N modes.

    Valid at the Fourier-resonance parameters kappa2 = alpha tau_q, where the
    operator is exactly Fourier (eq:res-step5). Used ONLY to reproduce the
    anchor's truncation study (test T4).
    """
    t = np.asarray(t_hat, float)
    w = 2.0 * np.pi / tau_D_hat
    tc = np.minimum(t, tau_D_hat)
    T = (tc - np.sin(w * tc) / w) / tau_D_hat          # eq:series-a0
    for n in range(1, N + 1):
        beta = (n * np.pi) ** 2
        A = 2.0 * (-1) ** n / tau_D_hat                # rear face cos(n pi)
        e_full = np.exp(-beta * t)
        e_sh = np.exp(-beta * (t - tc))
        I1 = (e_sh - e_full) / beta                    # eq:series-I
        I2 = (e_sh * (beta * np.cos(w * tc) + w * np.sin(w * tc))
              - beta * e_full) / (beta ** 2 + w ** 2)
        T += A * (I1 - I2)                             # eq:series-an
    return T
