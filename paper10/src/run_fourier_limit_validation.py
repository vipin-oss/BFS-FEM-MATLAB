#!/usr/bin/env python3
"""
paper10/src/run_fourier_limit_validation.py
===========================================
Generates:
  - Table 2: Classical nonlinear Fourier limit validation of E1 solver
    against independent FVM Radau IIA benchmark.
  - Table 3: Reference solver spatial mesh convergence study (Nx = 100, 200, 400 vs 800).
"""

import os
import sys
import csv
import numpy as np

# Ensure local imports work
sys.path.append(os.path.dirname(__file__))
from solver_e1 import solve_e1_fourier_limit, solve_e1
from solver_ref_fourier import solve_fourier_fvm_ref

def compute_fourier_validation(Nx=200, tau_Delta=0.04, output_csv_val=None, output_csv_mesh=None):
    t_eval = np.linspace(0.01, 1.0, 100)
    cases = [0.0, 0.01, 0.02, 0.05]
    
    print("=" * 80)
    print("RUNNING CLASSICAL NONLINEAR FOURIER LIMIT VALIDATION")
    print("=" * 80)
    
    val_rows = []
    for eps in cases:
        _, T_field_ref, T_ref = solve_fourier_fvm_ref(Nx=Nx, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        _, T_field_e1, T_lim = solve_e1_fourier_limit(Nx=Nx, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        
        diff = np.abs(T_lim - T_ref)
        e_inf = np.max(diff)
        idx_max = np.argmax(diff)
        t_max = t_eval[idx_max]
        e_2 = np.linalg.norm(diff) / np.linalg.norm(T_ref)
        e_peak = np.abs(T_lim[-1] - T_ref[-1]) / T_ref[-1]
        delta_T_rear = np.max(T_ref) - np.min(T_ref)
        delta_T_domain = np.max(T_field_ref) - np.min(T_field_ref)
        
        row = {
            "eps_lambda": eps,
            "delta_T_rear": delta_T_rear,
            "delta_T_domain": delta_T_domain,
            "E_inf": e_inf,
            "E_2": e_2,
            "E_peak": e_peak,
            "t_diff_max": t_max
        }
        val_rows.append(row)
        print(f"eps={eps:0.2f} | DeltaT={delta_T_rear:.4f} | E_inf={e_inf:.4e} (t={t_max:.3f}) | E_2={e_2:.4e} | E_peak={e_peak:.4e}")

    if output_csv_val:
        os.makedirs(os.path.dirname(os.path.abspath(output_csv_val)), exist_ok=True)
        with open(output_csv_val, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["eps_lambda", "delta_T_rear", "delta_T_domain", "E_inf", "E_2", "E_peak", "t_diff_max"])
            writer.writeheader()
            for r in val_rows:
                writer.writerow(r)
        print(f"Validation table written to: {output_csv_val}")

    print("\n" + "=" * 80)
    print("RUNNING REFERENCE SOLVER MESH CONVERGENCE STUDY")
    print("=" * 80)
    mesh_rows = []
    for eps in cases:
        _, _, T_800 = solve_fourier_fvm_ref(Nx=800, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        _, _, T_400 = solve_fourier_fvm_ref(Nx=400, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        _, _, T_200 = solve_fourier_fvm_ref(Nx=200, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        _, _, T_100 = solve_fourier_fvm_ref(Nx=100, eps_lambda=eps, tau_Delta=tau_Delta, t_eval=t_eval)
        
        e100 = np.max(np.abs(T_100 - T_800))
        e200 = np.max(np.abs(T_200 - T_800))
        e400 = np.max(np.abs(T_400 - T_800))
        p12 = np.log2(e100 / e200)
        p24 = np.log2(e200 / e400)
        
        row = {
            "eps_lambda": eps,
            "e100": e100,
            "e200": e200,
            "e400": e400,
            "order_p_100_200": p12,
            "order_p_200_400": p24
        }
        mesh_rows.append(row)
        print(f"eps={eps:0.2f} | e100={e100:.4e} | e200={e200:.4e} | e400={e400:.4e} | p12={p12:.2f} | p24={p24:.2f}")

    if output_csv_mesh:
        os.makedirs(os.path.dirname(os.path.abspath(output_csv_mesh)), exist_ok=True)
        with open(output_csv_mesh, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["eps_lambda", "e100", "e200", "e400", "order_p_100_200", "order_p_200_400"])
            writer.writeheader()
            for r in mesh_rows:
                writer.writerow(r)
        print(f"Mesh convergence table written to: {output_csv_mesh}")

    return val_rows, mesh_rows

if __name__ == "__main__":
    out_val = os.path.join(os.path.dirname(__file__), "../runs/final-paper-calculations/table_02_fourier_limit_validation.csv")
    out_mesh = os.path.join(os.path.dirname(__file__), "../runs/final-paper-calculations/table_03_mesh_convergence.csv")
    compute_fourier_validation(Nx=200, output_csv_val=out_val, output_csv_mesh=out_mesh)
