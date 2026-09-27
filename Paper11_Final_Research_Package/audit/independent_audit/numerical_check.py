"""
numerical_check.py - Independent Numerical Validation of GK Heat Loss Equivalence
Part of Paper 11 Independent Scientific Audit.

Tests all required Biot numbers:
  Bi in {0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5} at B = 1.0.
Calculates independent:
  - L_inf error
  - L_2 error
  - Relative error
Compares GK PDE solver vs exact analytical de Hoog Laplace inversion and Cowan Fourier solution.
"""

import sys
import os
import numpy as np
import mpmath as mp
import pandas as pd
from scipy.integrate import solve_ivp

tau_Delta = 0.04
omega = 2.0 * np.pi / tau_Delta

def pulse_transform(s):
    return (omega**2 / (s * (s**2 + omega**2))) * (1.0 - mp.exp(-s * tau_Delta))

def tf_gk_laplace(s, tau_q, kappa2, Bi):
    s = mp.mpc(s)
    m = mp.sqrt(s * (1.0 + tau_q * s) / (1.0 + kappa2 * s))
    mu = (1.0 + kappa2 * s) / (1.0 + tau_q * s)
    m_mu = m * mu
    Delta = (m_mu**2 + Bi**2) * mp.sinh(m) + 2.0 * Bi * m_mu * mp.cosh(m)
    return (m_mu / (tau_Delta * Delta)) * pulse_transform(s)

def tf_fourier_laplace(s, Bi):
    s = mp.mpc(s)
    m = mp.sqrt(s)
    Delta = (s + Bi**2) * mp.sinh(m) + 2.0 * Bi * m * mp.cosh(m)
    return (m / (tau_Delta * Delta)) * pulse_transform(s)

def q_pulse(t):
    if 0.0 < t <= tau_Delta:
        return 1.0 - np.cos(2.0 * np.pi * t / tau_Delta)
    return 0.0

def solve_gk_pde(Nx=400, tau_q=0.02, kappa2=0.02, Bi=0.1, t_eval=None):
    dx = 1.0 / Nx
    def rhs(t, y):
        T = y[:Nx]
        q_int = y[Nx:]
        T0 = 1.5 * T[0] - 0.5 * T[1]
        T1 = 1.5 * T[Nx - 1] - 0.5 * T[Nx - 2]

        q_front = q_pulse(t) - tau_Delta * Bi * T0
        q_rear = tau_Delta * Bi * T1

        q = np.empty(Nx + 1)
        q[0] = q_front
        q[1:Nx] = q_int
        q[Nx] = q_rear

        dTdt = -(q[1:] - q[:-1]) / (tau_Delta * dx)
        dTdx = (T[1:] - T[:-1]) / dx
        d2qdx2 = (q[2:] - 2.0 * q[1:Nx] + q[:-2]) / (dx**2)
        dqdt = (-q_int - tau_Delta * dTdx + kappa2 * d2qdx2) / tau_q
        return np.concatenate([dTdt, dqdt])

    y0 = np.zeros(2 * Nx - 1)
    sol = solve_ivp(rhs, (0.0, float(t_eval[-1])), y0, method="BDF", t_eval=t_eval, rtol=1e-10, atol=1e-12)
    T_rear = 1.5 * sol.y[Nx - 1, :] - 0.5 * sol.y[Nx - 2, :]
    return T_rear

def run_numerical_audit():
    print("=" * 80)
    print("INDEPENDENT NUMERICAL VALIDATION: BIOT SWEEP AT B = 1.0")
    print("=" * 80)

    bi_list = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5]
    t_eval = np.linspace(0.05, 1.0, 20)
    tau_q = 0.02
    kappa2 = 0.02
    Nx = 400
    mp.mp.dps = 25

    results = []

    for Bi in bi_list:
        print(f"  Evaluating Bi = {Bi:5.3f} ...", end=" ", flush=True)

        # 1. GK time-domain PDE solution
        T_pde = solve_gk_pde(Nx=Nx, tau_q=tau_q, kappa2=kappa2, Bi=Bi, t_eval=t_eval)

        # 2. Exact analytical Laplace inversion for GK (B=1)
        T_lap_gk = np.array([float(mp.invertlaplace(lambda s: tf_gk_laplace(s, tau_q, kappa2, Bi), t, method="dehoog", degree=20)) for t in t_eval])

        # 3. Exact analytical Laplace inversion for pure Fourier/Cowan
        T_lap_fou = np.array([float(mp.invertlaplace(lambda s: tf_fourier_laplace(s, Bi), t, method="dehoog", degree=20)) for t in t_eval])

        # Analytical equivalence between GK(B=1) and Fourier
        diff_analytical = np.max(np.abs(T_lap_gk - T_lap_fou))

        # PDE vs analytical Laplace
        err_vec = np.abs(T_pde - T_lap_gk)
        L_inf = np.max(err_vec)
        L_2 = np.sqrt(np.mean(err_vec**2))
        rel_err = np.max(err_vec / (np.abs(T_lap_gk) + 1e-12))

        results.append({
            "Bi": Bi,
            "Peak_T": np.max(T_pde),
            "L_inf_error": L_inf,
            "L_2_error": L_2,
            "Rel_error": rel_err,
            "Analytical_diff": diff_analytical,
            "Status": "PASS" if L_inf < 2e-5 and diff_analytical < 1e-14 else "FAIL"
        })
        print(f"Done! L_inf = {L_inf:.2e}, Rel = {rel_err:.2e}, Diff(GK-Fou) = {diff_analytical:.1e} [{results[-1]['Status']}]")

    df = pd.DataFrame(results)
    out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "numerical_check_results.csv")
    df.to_csv(out_csv, index=False)
    print(f"\nSaved independent numerical audit results to: {out_csv}")
    print("\nSUMMARY TABLE:")
    print(df[["Bi", "Peak_T", "L_inf_error", "L_2_error", "Rel_error", "Analytical_diff", "Status"]].to_string(index=False))

if __name__ == "__main__":
    run_numerical_audit()
