"""
run_validation.py - Dual Analytical and Numerical Validation Suite for Paper 11
Part of the Paper 11 Research Package.

Validates:
  1. Analytical Laplace vs Time-Domain PDE Benchmark:
     Compares PDE solver on Nx=400 against exact de Hoog Laplace inversion
     across Biot numbers Bi in {0.0, 0.01, 0.05, 0.1, 0.2, 0.5}.
  2. Classical Cowan (1963) Fourier Heat Loss Limit Benchmark:
     Compares PDE solver in the singular limit (tau_q -> 0, kappa^2 -> 0)
     against exact analytical Fourier transfer function across Bi.
  3. Spatial Mesh Refinement Study:
     Evaluates grid convergence on Nx in {100, 200, 400, 800} and computes
     observed order of accuracy p.

Generates:
  - paper11/runs/calculations/validation_laplace.csv
  - paper11/runs/calculations/validation_cowan.csv
  - paper11/runs/calculations/mesh_convergence.csv
"""

import sys
import os
import numpy as np
import pandas as pd

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver_gk_heatloss import solve_gk_heatloss
from analytic_laplace import solve_laplace_gk, solve_laplace_fourier

def run_laplace_validation():
    print("=" * 70)
    print("1. RUNNING ANALYTICAL LAPLACE VS TIME-DOMAIN PDE BENCHMARK")
    print("=" * 70)

    bi_list = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]
    t_eval = np.linspace(0.05, 1.0, 20)
    tau_q = 0.02
    kappa2 = 0.02
    Nx = 400

    results = []

    for Bi in bi_list:
        print(f"  Validating Bi = {Bi:5.3f} ...", end=" ", flush=True)
        # Numerical PDE solution
        _, T_pde, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q, kappa2=kappa2, Bi0=Bi, BiL=Bi, t_eval=t_eval)

        # Analytical Laplace inversion
        T_lap = solve_laplace_gk(t_eval, tau_q=tau_q, kappa2=kappa2, Bi0=Bi, BiL=Bi)

        diff = np.abs(T_pde - T_lap)
        err_inf = np.max(diff)
        err_2 = np.sqrt(np.mean(diff**2))
        err_rel = np.max(diff / (np.abs(T_lap) + 1e-12))
        peak_pde = np.max(T_pde)
        peak_lap = np.max(T_lap)

        results.append({
            "Bi": Bi,
            "tau_q": tau_q,
            "kappa2": kappa2,
            "Nx": Nx,
            "peak_PDE": peak_pde,
            "peak_Laplace": peak_lap,
            "L_inf_error": err_inf,
            "L_2_error": err_2,
            "rel_error": err_rel,
            "status": "PASS" if err_inf < 5e-5 else "FAIL"
        })
        print(f"Done! L_inf = {err_inf:.2e}, L_2 = {err_2:.2e} [{results[-1]['status']}]")

    df = pd.DataFrame(results)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs", "calculations", "validation_laplace.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"  Saved Laplace validation table to: {out_path}\n")
    return df

def run_cowan_fourier_validation():
    print("=" * 70)
    print("2. RUNNING CLASSICAL COWAN (1963) FOURIER LIMIT BENCHMARK")
    print("=" * 70)

    bi_list = [0.01, 0.05, 0.1, 0.2, 0.5]
    t_eval = np.linspace(0.05, 1.0, 20)
    # Singular limit: relaxation and nonlocality vanish
    tau_q_lim = 1e-6
    kappa2_lim = 1e-6
    Nx = 400

    results = []

    for Bi in bi_list:
        print(f"  Validating Cowan limit for Bi = {Bi:5.3f} ...", end=" ", flush=True)
        # PDE solver with vanishing non-Fourier parameters
        _, T_pde, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q_lim, kappa2=kappa2_lim, Bi0=Bi, BiL=Bi, t_eval=t_eval)

        # Exact Cowan Fourier transfer function inversion
        T_cowan = solve_laplace_fourier(t_eval, Bi0=Bi, BiL=Bi)

        diff = np.abs(T_pde - T_cowan)
        err_inf = np.max(diff)
        err_2 = np.sqrt(np.mean(diff**2))
        err_rel = np.max(diff / (np.abs(T_cowan) + 1e-12))

        results.append({
            "Bi": Bi,
            "tau_q_limit": tau_q_lim,
            "kappa2_limit": kappa2_lim,
            "peak_PDE": np.max(T_pde),
            "peak_Cowan": np.max(T_cowan),
            "L_inf_error": err_inf,
            "L_2_error": err_2,
            "rel_error": err_rel,
            "status": "PASS" if err_inf < 5e-5 else "FAIL"
        })
        print(f"Done! L_inf = {err_inf:.2e}, L_2 = {err_2:.2e} [{results[-1]['status']}]")

    df = pd.DataFrame(results)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs", "calculations", "validation_cowan.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved Cowan validation table to: {out_path}\n")
    return df

def run_mesh_convergence():
    print("=" * 70)
    print("3. RUNNING SPATIAL MESH CONVERGENCE STUDY")
    print("=" * 70)

    nx_list = [100, 200, 400, 800]
    t_eval = np.linspace(0.05, 1.0, 50)
    tau_q = 0.02
    kappa2 = 0.02
    Bi = 0.1

    sol_dict = {}
    for Nx in nx_list:
        print(f"  Solving Nx = {Nx} ...", end=" ", flush=True)
        _, T_rear, _, _ = solve_gk_heatloss(Nx=Nx, tau_q=tau_q, kappa2=kappa2, Bi0=Bi, BiL=Bi, t_eval=t_eval)
        sol_dict[Nx] = T_rear
        print("Done!")

    # Reference solution is Nx = 800
    T_ref = sol_dict[800]
    results = []
    prev_err = None

    for Nx in [100, 200, 400]:
        diff = np.abs(sol_dict[Nx] - T_ref)
        err_inf = np.max(diff)
        err_2 = np.sqrt(np.mean(diff**2))

        if prev_err is not None:
            order_p = np.log2(prev_err / err_inf)
        else:
            order_p = np.nan

        results.append({
            "Nx": Nx,
            "dx": 1.0 / Nx,
            "L_inf_error": err_inf,
            "L_2_error": err_2,
            "observed_order_p": order_p
        })
        prev_err = err_inf
        print(f"  Nx = {Nx:3d} | L_inf = {err_inf:.3e} | L_2 = {err_2:.3e} | Order p = {order_p:.2f}")

    df = pd.DataFrame(results)
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs", "calculations", "mesh_convergence.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved mesh convergence table to: {out_path}\n")
    return df

if __name__ == "__main__":
    run_laplace_validation()
    run_cowan_fourier_validation()
    run_mesh_convergence()
