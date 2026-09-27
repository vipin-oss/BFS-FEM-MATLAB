"""
sensitivity_check.py - Independent Sensitivity, Identifiability & Off-Resonance Audit
Part of Paper 11 Independent Scientific Audit.

Calculates independently:
  1. J_tau_q, J_kappa2, J_Bi across Biot numbers.
  2. Correlation coefficient rho, residual norm R_J, and defect |1 + rho|.
  3. Singular spectrum (sigma_1, sigma_2, sigma_3) of 3-parameter Fisher matrix.
  4. Null-vector projection onto (1, alpha_0, 0)^T.
  5. Off-resonance condition number sweep across B in [0.5, 1.5] for Bi in {0.0, 0.05, 0.20}.
"""

import sys
import os
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

tau_Delta = 0.04
alpha_0 = 1.0

def q_pulse(t):
    if 0.0 < t <= tau_Delta:
        return 1.0 - np.cos(2.0 * np.pi * t / tau_Delta)
    return 0.0

def solve_pde(Nx=150, tau_q=0.02, kappa2=0.02, Bi=0.1, t_eval=None):
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

def run_sensitivity_audit():
    print("=" * 80)
    print("INDEPENDENT SENSITIVITY AND IDENTIFIABILITY AUDIT")
    print("=" * 80)

    t_eval = np.linspace(0.01, 1.0, 100)
    tau_q_0 = 0.02
    kappa2_0 = 0.02
    h_rel = 1e-4
    Nx = 150

    bi_list = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5]
    results_sens = []

    print("\n--- 1. SENSITIVITY & SVD SPECTRUM AT B = 1.0 ---")
    for Bi in bi_list:
        d_tq = h_rel * tau_q_0
        d_k2 = h_rel * kappa2_0
        d_bi = h_rel * Bi if Bi > 0 else 1e-5

        Tp_tq = solve_pde(Nx=Nx, tau_q=tau_q_0 + d_tq, kappa2=kappa2_0, Bi=Bi, t_eval=t_eval)
        Tm_tq = solve_pde(Nx=Nx, tau_q=tau_q_0 - d_tq, kappa2=kappa2_0, Bi=Bi, t_eval=t_eval)
        J_tq = (Tp_tq - Tm_tq) / (2.0 * d_tq)

        Tp_k2 = solve_pde(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 + d_k2, Bi=Bi, t_eval=t_eval)
        Tm_k2 = solve_pde(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 - d_k2, Bi=Bi, t_eval=t_eval)
        J_k2 = (Tp_k2 - Tm_k2) / (2.0 * d_k2)

        Tp_bi = solve_pde(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi=Bi + d_bi, t_eval=t_eval)
        Tm_bi = solve_pde(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi=max(0.0, Bi - d_bi), t_eval=t_eval)
        denom_bi = (2.0 * d_bi) if Bi > 0 else d_bi
        J_bi = (Tp_bi - Tm_bi) / denom_bi

        norm_tq = np.linalg.norm(J_tq)
        norm_k2 = np.linalg.norm(J_k2)
        rho_val = float(np.dot(J_tq, J_k2) / (norm_tq * norm_k2))
        one_plus_rho = 1.0 + rho_val
        R_J = float(np.linalg.norm(J_tq + alpha_0 * J_k2) / norm_tq)

        # 3-parameter Jacobian & SVD
        J3 = np.column_stack([J_tq, J_k2, J_bi])
        U, S, Vt = np.linalg.svd(J3)
        cond_F3 = (S[0] / S[2])**2
        obs_cond = S[0] / S[1]

        # Check null vector projection
        # Null vector normalized: v_null = [1, alpha_0, 0] / sqrt(1 + alpha_0^2)
        v_null_expected = np.array([1.0, alpha_0, 0.0]) / np.sqrt(1.0 + alpha_0**2)
        v_null_computed = Vt[2, :]  # Right singular vector corresponding to sigma_3
        # Align sign
        if np.dot(v_null_computed, v_null_expected) < 0:
            v_null_computed = -v_null_computed
        null_alignment = float(np.dot(v_null_computed, v_null_expected))

        results_sens.append({
            "Bi": Bi,
            "rho": rho_val,
            "one_plus_rho": one_plus_rho,
            "R_J": R_J,
            "sigma_1": S[0],
            "sigma_2": S[1],
            "sigma_3": S[2],
            "sigma1_over_sigma2": obs_cond,
            "cond_F3": cond_F3,
            "null_alignment": null_alignment
        })
        print(f"  Bi = {Bi:5.3f} | rho = {rho_val:.10f} | R_J = {R_J:.2e} | SVD = [{S[0]:.2f}, {S[1]:.2f}, {S[2]:.2e}] | Alignment = {null_alignment:.6f}")

    df_sens = pd.DataFrame(results_sens)
    out_sens_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensitivity_audit_results.csv")
    df_sens.to_csv(out_sens_csv, index=False)
    print(f"\nSaved sensitivity audit results to: {out_sens_csv}")

    print("\n--- 2. OFF-RESONANCE AUDIT ACROSS B in [0.5, 1.5] ---")
    b_test = [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5]
    results_off = []
    for Bi in [0.0, 0.05, 0.20]:
        print(f"\n  Sweeping B for Bi = {Bi:4.2f}:")
        for B in b_test:
            k2_val = B * tau_q_0
            d_tq = h_rel * tau_q_0
            d_k2 = h_rel * k2_val

            Tp_tq = solve_pde(Nx=Nx, tau_q=tau_q_0 + d_tq, kappa2=k2_val, Bi=Bi, t_eval=t_eval)
            Tm_tq = solve_pde(Nx=Nx, tau_q=tau_q_0 - d_tq, kappa2=k2_val, Bi=Bi, t_eval=t_eval)
            J_tq = (Tp_tq - Tm_tq) / (2.0 * d_tq)

            Tp_k2 = solve_pde(Nx=Nx, tau_q=tau_q_0, kappa2=k2_val + d_k2, Bi=Bi, t_eval=t_eval)
            Tm_k2 = solve_pde(Nx=Nx, tau_q=tau_q_0, kappa2=k2_val - d_k2, Bi=Bi, t_eval=t_eval)
            J_k2 = (Tp_k2 - Tm_k2) / (2.0 * d_k2)

            J2 = np.column_stack([J_tq, J_k2])
            s2 = np.linalg.svd(J2, compute_uv=False)
            cond_F2 = float((s2[0] / s2[1])**2)
            rho_b = float(np.dot(J_tq, J_k2) / (np.linalg.norm(J_tq) * np.linalg.norm(J_k2)))

            results_off.append({
                "Bi": Bi,
                "B": B,
                "rho": rho_b,
                "cond_F2": cond_F2,
                "sigma1": s2[0],
                "sigma2": s2[1]
            })
            print(f"    B = {B:4.2f} | rho = {rho_b:.6f} | cond(F2) = {cond_F2:10.3e}")

    df_off = pd.DataFrame(results_off)
    out_off_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "off_resonance_audit_results.csv")
    df_off.to_csv(out_off_csv, index=False)
    print(f"\nSaved off-resonance audit results to: {out_off_csv}")

if __name__ == "__main__":
    run_sensitivity_audit()
