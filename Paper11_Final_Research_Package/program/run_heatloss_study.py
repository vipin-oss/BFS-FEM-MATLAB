"""
run_heatloss_study.py - Systematic Boundary Heat Loss Parameter Sweeps for Paper 11
Part of the Paper 11 Research Package.

Computes:
  1. Systematic Biot number sweep at Fourier resonance (B = 1.0):
     Bi in [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
     Evaluates J_tau_q, J_kappa^2, J_Bi, rho, 1+rho, R_J, SVD spectrum (sigma_1, sigma_2, sigma_3),
     and condition numbers for 2x2 and 3x3 Fisher information matrices.
  2. Off-resonance parameter sweep across B in [0.2, 2.0] for varying Bi in {0.0, 0.05, 0.2}.
  3. Time-resolved sensitivity profiles for representative Biot numbers.

Generates:
  - paper11/runs/calculations/heatloss_parameter_sweep.csv
  - paper11/runs/calculations/off_resonance_sweep.csv
  - paper11/runs/calculations/sensitivity_profiles.csv
"""

import sys
import os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver_gk_heatloss import solve_gk_heatloss

def run_resonance_heatloss_sweep():
    print("=" * 70)
    print("1. RUNNING FOURIER-RESONANCE (B = 1.0) HEAT-LOSS SWEEP")
    print("=" * 70)

    bi_list = [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
    t_eval = np.linspace(0.01, 1.0, 100)
    tau_q_0 = 0.02
    kappa2_0 = 0.02
    alpha_0 = 1.0
    Nx = 100
    h_rel = 1e-4

    results = []

    for Bi in bi_list:
        print(f"  Computing Bi = {Bi:5.3f} ...", end=" ", flush=True)

        d_tq = h_rel * tau_q_0
        d_k2 = h_rel * kappa2_0
        d_bi = h_rel * Bi if Bi > 0 else 1e-5

        # Base solution
        _, T_base, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi0=Bi, BiL=Bi, t_eval=t_eval)

        # Perturbation in tau_q
        _, Tp_tq, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0 + d_tq, kappa2=kappa2_0, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        _, Tm_tq, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0 - d_tq, kappa2=kappa2_0, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        J_tq = (Tp_tq - Tm_tq) / (2.0 * d_tq)

        # Perturbation in kappa2
        _, Tp_k2, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 + d_k2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        _, Tm_k2, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 - d_k2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        J_k2 = (Tp_k2 - Tm_k2) / (2.0 * d_k2)

        # Perturbation in Bi
        _, Tp_bi, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi0=Bi + d_bi, BiL=Bi + d_bi, t_eval=t_eval)
        _, Tm_bi, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi0=max(0.0, Bi - d_bi), BiL=max(0.0, Bi - d_bi), t_eval=t_eval)
        denom_bi = (2.0 * d_bi) if Bi > 0 else d_bi
        J_bi = (Tp_bi - Tm_bi) / denom_bi

        # 2-parameter collinearity metrics
        norm_tq = np.linalg.norm(J_tq)
        norm_k2 = np.linalg.norm(J_k2)
        rho_val = np.dot(J_tq, J_k2) / (norm_tq * norm_k2)
        one_plus_rho = 1.0 + rho_val
        res_norm = np.linalg.norm(J_tq + alpha_0 * J_k2) / norm_tq

        # 2x2 Fisher matrix
        J2 = np.column_stack([J_tq, J_k2])
        F2 = J2.T @ J2
        s2 = np.linalg.svd(J2, compute_uv=False)
        cond_F2 = (s2[0] / s2[1])**2

        # 3x3 Fisher matrix
        J3 = np.column_stack([J_tq, J_k2, J_bi])
        F3 = J3.T @ J3
        s3 = np.linalg.svd(J3, compute_uv=False)
        cond_F3 = (s3[0] / s3[2])**2

        # Observable subspace conditioning
        ratio_sigma1_sigma2 = s3[0] / s3[1]

        results.append({
            "Bi": Bi,
            "tau_q": tau_q_0,
            "kappa2": kappa2_0,
            "norm_J_tq": norm_tq,
            "norm_J_k2": norm_k2,
            "norm_J_bi": np.linalg.norm(J_bi),
            "rho": rho_val,
            "one_plus_rho": one_plus_rho,
            "R_J": res_norm,
            "sigma1_2p": s2[0],
            "sigma2_2p": s2[1],
            "cond_F2": cond_F2,
            "sigma1_3p": s3[0],
            "sigma2_3p": s3[1],
            "sigma3_3p": s3[2],
            "sigma1_over_sigma2": ratio_sigma1_sigma2,
            "cond_F3": cond_F3
        })
        print(f"Done! rho = {rho_val:.10f}, R_J = {res_norm:.2e}, sigma_3 = {s3[2]:.2e}")

    df = pd.DataFrame(results)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data" if os.path.isdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")) else os.path.join("runs", "calculations"), "heatloss_parameter_sweep.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"  Saved heat loss parameter sweep to: {out_path}\n")
    return df

def run_off_resonance_sweep():
    print("=" * 70)
    print("2. RUNNING OFF-RESONANCE PARAMETER SWEEPS ACROSS B AND Bi")
    print("=" * 70)

    b_vals = [0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.98, 0.99, 1.0, 1.01, 1.02, 1.05, 1.1, 1.2, 1.5, 2.0]
    bi_vals = [0.0, 0.05, 0.2]
    t_eval = np.linspace(0.01, 1.0, 100)
    tau_q_0 = 0.02
    Nx = 100
    h_rel = 1e-4

    results = []

    for Bi in bi_vals:
        print(f"  Sweeping B for Bi = {Bi} ...")
        for B in b_vals:
            kappa2_val = B * tau_q_0
            d_tq = h_rel * tau_q_0
            d_k2 = h_rel * kappa2_val

            _, Tp_tq, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0 + d_tq, kappa2=kappa2_val, Bi0=Bi, BiL=Bi, t_eval=t_eval)
            _, Tm_tq, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0 - d_tq, kappa2=kappa2_val, Bi0=Bi, BiL=Bi, t_eval=t_eval)
            J_tq = (Tp_tq - Tm_tq) / (2.0 * d_tq)

            _, Tp_k2, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_val + d_k2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
            _, Tm_k2, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_val - d_k2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
            J_k2 = (Tp_k2 - Tm_k2) / (2.0 * d_k2)

            norm_tq = np.linalg.norm(J_tq)
            norm_k2 = np.linalg.norm(J_k2)
            rho_val = np.dot(J_tq, J_k2) / (norm_tq * norm_k2)
            one_plus_rho = 1.0 + rho_val
            res_norm = np.linalg.norm(J_tq + J_k2) / norm_tq

            J2 = np.column_stack([J_tq, J_k2])
            s2 = np.linalg.svd(J2, compute_uv=False)
            cond_F2 = (s2[0] / s2[1])**2

            results.append({
                "Bi": Bi,
                "B": B,
                "tau_q": tau_q_0,
                "kappa2": kappa2_val,
                "rho": rho_val,
                "one_plus_rho": one_plus_rho,
                "R_J": res_norm,
                "cond_F2": cond_F2,
                "sigma1": s2[0],
                "sigma2": s2[1]
            })

    df = pd.DataFrame(results)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data" if os.path.isdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")) else os.path.join("runs", "calculations"), "off_resonance_sweep.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved off-resonance sweep to: {out_path}\n")
    return df

def run_sensitivity_profiles():
    print("=" * 70)
    print("3. GENERATING TIME-RESOLVED SENSITIVITY PROFILES")
    print("=" * 70)

    bi_samples = [0.0, 0.05, 0.2]
    t_eval = np.linspace(0.01, 1.0, 100)
    tau_q_0 = 0.02
    kappa2_0 = 0.02
    Nx = 100
    h_rel = 1e-4

    records = {"time": t_eval}

    for Bi in bi_samples:
        d_tq = h_rel * tau_q_0
        d_k2 = h_rel * kappa2_0
        d_bi = h_rel * Bi if Bi > 0 else 1e-5

        _, T_base, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        _, Tp_tq, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0 + d_tq, kappa2=kappa2_0, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        _, Tm_tq, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0 - d_tq, kappa2=kappa2_0, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        J_tq = (Tp_tq - Tm_tq) / (2.0 * d_tq)

        _, Tp_k2, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 + d_k2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        _, Tm_k2, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 - d_k2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        J_k2 = (Tp_k2 - Tm_k2) / (2.0 * d_k2)

        _, Tp_bi, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi0=Bi + d_bi, BiL=Bi + d_bi, t_eval=t_eval)
        _, Tm_bi, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0, Bi0=max(0.0, Bi - d_bi), BiL=max(0.0, Bi - d_bi), t_eval=t_eval)
        denom_bi = (2.0 * d_bi) if Bi > 0 else d_bi
        J_bi = (Tp_bi - Tm_bi) / denom_bi

        tag = f"Bi_{Bi:04.2f}".replace(".", "p")
        records[f"T_{tag}"] = T_base
        records[f"J_tau_q_{tag}"] = J_tq
        records[f"J_kappa2_{tag}"] = J_k2
        records[f"J_Bi_{tag}"] = J_bi

    df = pd.DataFrame(records)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data" if os.path.isdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")) else os.path.join("runs", "calculations"), "sensitivity_profiles.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved sensitivity profiles to: {out_path}\n")
    return df

if __name__ == "__main__":
    run_resonance_heatloss_sweep()
    run_off_resonance_sweep()
    run_sensitivity_profiles()
