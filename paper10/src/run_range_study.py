#!/usr/bin/env python3
"""
paper10/src/run_range_study.py
==============================
Generates Table 1: Systematic finite-fluence / nonlinearity range study
for Extension E1 across eps_lambda in {0.0, 0.005, 0.01, 0.02, 0.03, 0.05}.
"""

import os
import sys
import csv
import numpy as np

# Ensure local imports work
sys.path.append(os.path.dirname(__file__))
from solver_e1 import solve_e1

def compute_range_study(Nx=200, h_rel=1e-4, tau_Delta=0.04, output_csv=None):
    alpha = 1.0
    tau_q_0 = 0.02
    kappa2_0 = 0.02
    t_eval = np.linspace(0.01, 1.0, 100)
    eps_list = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05]
    
    results = []
    print("=" * 80)
    print("RUNNING EXTENSION E1 SYSTEMATIC RANGE STUDY")
    print("=" * 80)
    
    for eps in eps_list:
        d_tq = h_rel * tau_q_0
        d_k2 = h_rel * kappa2_0
        
        # Central difference for tau_q
        _, T_p_tq = solve_e1(Nx=Nx, tau_q=tau_q_0 + d_tq, kappa2=kappa2_0, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        _, T_m_tq = solve_e1(Nx=Nx, tau_q=tau_q_0 - d_tq, kappa2=kappa2_0, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        J_tq = (T_p_tq - T_m_tq) / (2.0 * d_tq)
        
        # Central difference for kappa2
        _, T_p_k2 = solve_e1(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 + d_k2, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        _, T_m_k2 = solve_e1(Nx=Nx, tau_q=tau_q_0, kappa2=kappa2_0 - d_k2, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        J_k2 = (T_p_k2 - T_m_k2) / (2.0 * d_k2)
        
        norm_tq = np.linalg.norm(J_tq)
        norm_k2 = np.linalg.norm(J_k2)
        R_J = np.linalg.norm(J_tq + alpha * J_k2) / norm_tq
        rho = np.dot(J_tq, J_k2) / (norm_tq * norm_k2)
        one_plus_rho = 1.0 + rho
        
        J_mat = np.column_stack([J_tq, J_k2])
        U, S, Vt = np.linalg.svd(J_mat)
        sv_ratio = S[0] / S[1]
        cond_F = sv_ratio**2
        
        row = {
            "eps_lambda": eps,
            "rho": rho,
            "one_plus_rho": one_plus_rho,
            "R_J": R_J,
            "sigma1": S[0],
            "sigma2": S[1],
            "sv_ratio": sv_ratio,
            "cond_F": cond_F
        }
        results.append(row)
        print(f"eps={eps:0.3f} | rho={rho:.12f} | 1+rho={one_plus_rho:.4e} | R_J={R_J:.4e} | sigma1={S[0]:.4f} | sigma2={S[1]:.4e} | cond(F)={cond_F:.4e}")

    if output_csv:
        os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
        with open(output_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["eps_lambda", "rho", "one_plus_rho", "R_J", "sigma1", "sigma2", "sv_ratio", "cond_F"])
            writer.writeheader()
            for r in results:
                writer.writerow(r)
        print(f"Results successfully written to: {output_csv}")

    return results

if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(__file__), "../runs/final-paper-calculations/table_01_range_study.csv")
    compute_range_study(Nx=200, h_rel=1e-4, output_csv=out_path)
