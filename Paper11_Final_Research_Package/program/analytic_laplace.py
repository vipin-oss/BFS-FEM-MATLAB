"""
analytic_laplace.py - Exact Analytical Laplace-Domain Solutions and Inversions
Part of the Paper 11 Research Package.

Provides:
  1. Exact Laplace-domain transfer functions for 1D Guyer-Krumhansl conduction
     with front and rear Robin boundary heat losses (Bi0, BiL).
  2. Exact classical Fourier heat-loss transfer function (Cowan 1963 / Cape & Lehman 1963).
  3. High-precision numerical Laplace inversion via mpmath (de Hoog method).
"""

import mpmath as mp
import numpy as np

def pulse_transform(s, tau_Delta=0.04):
    """
    Laplace transform of smooth raised-cosine pulse:
      q(t) = 1 - cos(omega*t) for 0 <= t <= tau_Delta, where omega = 2*pi/tau_Delta.
      L{q(t)} = [omega^2 / (s*(s^2 + omega^2))] * [1 - exp(-s*tau_Delta)]
    """
    omega = 2.0 * mp.pi / tau_Delta
    return (omega**2 / (s * (s**2 + omega**2))) * (1.0 - mp.exp(-s * tau_Delta))

def transfer_function_gk(s, tau_q=0.02, kappa2=0.02, Bi0=0.1, BiL=0.1, tau_Delta=0.04):
    """
    Exact closed-form Laplace-domain transfer function for rear-face temperature:
      T_bar(1, s) = [ m * mu / (tau_Delta * Delta(s)) ] * q_bar_pulse(s)
    where:
      m^2(s) = s * (1 + tau_q*s) / (1 + kappa2*s)
      mu(s)  = (1 + kappa2*s) / (1 + tau_q*s)
      m*mu   = sqrt( s * (1 + kappa2*s) / (1 + tau_q*s) )
      Delta(s) = ( (m*mu)^2 + Bi0*BiL ) * sinh(m) + m*mu * (Bi0 + BiL) * cosh(m)
    """
    s = mp.mpc(s)
    m = mp.sqrt(s * (1.0 + tau_q * s) / (1.0 + kappa2 * s))
    mu = (1.0 + kappa2 * s) / (1.0 + tau_q * s)
    m_mu = m * mu
    Delta = (m_mu**2 + Bi0 * BiL) * mp.sinh(m) + m_mu * (Bi0 + BiL) * mp.cosh(m)
    q_s = pulse_transform(s, tau_Delta)
    return (m_mu / (tau_Delta * Delta)) * q_s

def transfer_function_fourier(s, Bi0=0.1, BiL=0.1, tau_Delta=0.04):
    """
    Exact Laplace-domain transfer function for classical Fourier laser flash
    with Robin convective/radiative cooling (Cowan 1963 / Cape & Lehman 1963).
    Equivalent to transfer_function_gk with tau_q = kappa2 = 0.
    """
    s = mp.mpc(s)
    m = mp.sqrt(s)
    Delta = (s + Bi0 * BiL) * mp.sinh(m) + m * (Bi0 + BiL) * mp.cosh(m)
    q_s = pulse_transform(s, tau_Delta)
    return (m / (tau_Delta * Delta)) * q_s

def solve_laplace_gk(t_eval, tau_q=0.02, kappa2=0.02, Bi0=0.1, BiL=0.1, tau_Delta=0.04, dps=25, degree=20):
    """
    Computes rear-face temperature history by numerical Laplace inversion of the
    exact Guyer-Krumhansl transfer function using the de Hoog algorithm.
    """
    mp.mp.dps = dps
    t_eval = np.atleast_1d(t_eval)
    T_out = np.zeros(len(t_eval), dtype=float)

    f_s = lambda s: transfer_function_gk(s, tau_q, kappa2, Bi0, BiL, tau_Delta)
    for i, t in enumerate(t_eval):
        val = mp.invertlaplace(f_s, t, method="dehoog", degree=degree)
        T_out[i] = float(mp.re(val))

    return T_out

def solve_laplace_fourier(t_eval, Bi0=0.1, BiL=0.1, tau_Delta=0.04, dps=25, degree=20):
    """
    Computes rear-face temperature history by numerical Laplace inversion of the
    exact classical Cowan Fourier heat loss transfer function.
    """
    mp.mp.dps = dps
    t_eval = np.atleast_1d(t_eval)
    T_out = np.zeros(len(t_eval), dtype=float)

    f_s = lambda s: transfer_function_fourier(s, Bi0, BiL, tau_Delta)
    for i, t in enumerate(t_eval):
        val = mp.invertlaplace(f_s, t, method="dehoog", degree=degree)
        T_out[i] = float(mp.re(val))

    return T_out

if __name__ == "__main__":
    t_test = [0.1, 0.3, 0.5, 0.8, 1.0]
    print("Testing Analytical Laplace Solutions (Bi = 0.1):")
    T_gk = solve_laplace_gk(t_test, tau_q=0.02, kappa2=0.02, Bi0=0.1, BiL=0.1)
    T_fou = solve_laplace_fourier(t_test, Bi0=0.1, BiL=0.1)
    for t, tg, tf in zip(t_test, T_gk, T_fou):
        print(f"t = {t:.2f} | T_GK(B=1) = {tg:.8f} | T_Fourier = {tf:.8f} | diff = {abs(tg - tf):.2e}")
