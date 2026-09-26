"""
Benchmark Validation Runner for Paper 10 (Phase 2)
Tests:
1. Gate G2-C: Papargyri-Beskou et al. (2009) Gradient Elastic Dispersion Benchmark
2. Gate G2-B: Classical Acoustic Elastic Limit (c, d -> 0)
Generates machine-readable CSV & JSON results, and Figures 1, 2, and 3.
"""

import sys
import os
import json
import csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver.parameters import get_benchmark_papargyri_beskou_material, MaterialParameters
from solver.antiplane import AntiPlaneSolver


def run_papargyri_beskou_benchmark():
    print("================================================================================")
    print("GATE G2-C: Papargyri-Beskou et al. (2009, IJSS) Gradient Elasticity Benchmark")
    print("================================================================================")
    
    mat = get_benchmark_papargyri_beskou_material()
    solver = AntiPlaneSolver(mat, xi=0.0)
    
    # Prescribed test wavenumbers k across physical dispersion regimes (m^-1)
    k_grid = np.linspace(10.0, 2000.0, 50)
    
    results = []
    
    print(f"{'k (m^-1)':<12} | {'Omega_exact (rad/s)':<22} | {'Omega_num (rad/s)':<22} | {'Rel Error':<14} | {'Residual':<14} | {'Scaled cond(P)':<14}")
    print("-" * 105)
    
    max_rel_err = 0.0
    max_residual = 0.0
    worst_cond_P = 0.0
    worst_det_err = 0.0
    
    for k in k_grid:
        omega_pb = solver.papargyri_beskou_analytical_omega(k)
        omega_num, rel_err, residual = solver.solve_numerical_omega(k)
        
        # Check condition numbers and symplecticity at solved frequency
        P, cond_P_raw, cond_P_scaled = solver.compute_modal_matrix(omega_num)
        T_sol = solver.compute_transfer_matrix_analytical(omega_num, 0.01)
        symp = solver.check_symplectic_properties(T_sol)
        
        max_rel_err = max(max_rel_err, rel_err)
        max_residual = max(max_residual, residual)
        worst_cond_P = max(worst_cond_P, cond_P_scaled)
        worst_det_err = max(worst_det_err, symp["det_err"])
        
        results.append({
            "k": float(k),
            "omega_analytical": float(omega_pb),
            "omega_numerical": float(omega_num),
            "relative_error": float(rel_err),
            "eigenvalue_residual": float(residual),
            "scaled_cond_P": float(cond_P_scaled),
            "raw_cond_P": float(cond_P_raw),
            "det_T_error": float(symp["det_err"])
        })
        
        # Print sample rows
        if k in k_grid[::10] or k == k_grid[-1]:
            print(f"{k:<12.1f} | {omega_pb:<22.8e} | {omega_num:<22.8e} | {rel_err:<14.2e} | {residual:<14.2e} | {cond_P_scaled:<14.2f}")
            
    print("-" * 105)
    print(f"Gate G2-C Evaluation: Max Relative Error = {max_rel_err:.2e} (Gate threshold <= 0.5%)")
    pass_g2c = (max_rel_err <= 0.005)
    print(f"Gate G2-C Status: {'PASS' if pass_g2c else 'FAIL'}\n")
    
    # Save machine-readable files
    os.makedirs("paper10/validation", exist_ok=True)
    os.makedirs("paper10/figures", exist_ok=True)
    
    csv_file = "paper10/validation/benchmark_papargyri_beskou_results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved CSV results: {csv_file}")
    
    json_file = "paper10/validation/benchmark_papargyri_beskou_results.json"
    with open(json_file, "w") as f:
        json.dump({
            "benchmark": "Papargyri-Beskou et al. (2009) IJSS Eq. (28)",
            "material": mat.name,
            "Vs": mat.Vs,
            "c": mat.c,
            "d": mat.d,
            "max_relative_error": max_rel_err,
            "max_residual": max_residual,
            "worst_scaled_cond_P": worst_cond_P,
            "worst_det_err": worst_det_err,
            "gate_G2_C_status": "PASS" if pass_g2c else "FAIL",
            "data": results
        }, f, indent=2)
    print(f"Saved JSON results: {json_file}")
    
    # Generate Figure 1 & Figure 2
    # Fig 1: Analytical vs Numerical Papargyri-Beskou Dispersion
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    k_vals = [r["k"] for r in results]
    w_ex = [r["omega_analytical"] for r in results]
    w_num = [r["omega_numerical"] for r in results]
    
    ax.plot(k_vals, np.array(w_ex) / 1e6, 'b-', lw=2.2, label='Analytical PB (2009) Eq. (28)')
    ax.plot(k_vals, np.array(w_num) / 1e6, 'ro', ms=5, markevery=3, label='Numerical TMM Solver')
    ax.set_xlabel('Wavenumber $k$ (m$^{-1}$)', fontsize=11)
    ax.set_ylabel('Angular Frequency $\\omega$ (Mrad/s)', fontsize=11)
    ax.set_title('Figure 1: Benchmark Validation — Papargyri-Beskou (2009) vs TMM', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(frameon=True, fontsize=10)
    plt.tight_layout()
    fig1_path = "paper10/figures/fig1_papargyri_beskou_benchmark.png"
    plt.savefig(fig1_path)
    plt.close()
    print(f"Generated Figure 1: {fig1_path}")
    
    # Fig 2: Relative Error versus Wavenumber
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    err_vals = [r["relative_error"] for r in results]
    ax.semilogy(k_vals, np.maximum(err_vals, 1e-16), 'd-', color='#2ca02c', lw=1.8, ms=5, label='Relative Error $|\\omega_{\\rm num} - \\omega_{\\rm ex}| / \\omega_{\\rm ex}$')
    ax.axhline(0.005, color='red', linestyle='--', lw=1.5, label='Pass Criterion (0.5% Threshold)')
    ax.set_xlabel('Wavenumber $k$ (m$^{-1}$)', fontsize=11)
    ax.set_ylabel('Relative Error', fontsize=11)
    ax.set_title('Figure 2: Relative Error vs Wavenumber (Papargyri-Beskou Benchmark)', fontsize=12)
    ax.set_ylim([1e-17, 1e-1])
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.legend(frameon=True, fontsize=10)
    plt.tight_layout()
    fig2_path = "paper10/figures/fig2_benchmark_relative_error.png"
    plt.savefig(fig2_path)
    plt.close()
    print(f"Generated Figure 2: {fig2_path}")
    
    return max_rel_err, max_residual, worst_cond_P, worst_det_err, pass_g2c


def run_classical_limit_benchmark():
    print("\n================================================================================")
    print("GATE G2-B: Classical Acoustic Limit (c, d -> 0) Benchmark")
    print("================================================================================")
    
    # Test classical limit over micro-scale reduction
    scales = np.logspace(-4, -8, 5) # m
    k_test = 200.0 # m^-1
    
    class_results = []
    
    print(f"{'Scale (m)':<12} | {'Micro-stiffness c (m^2)':<24} | {'Omega_classical':<18} | {'Omega_numerical':<18} | {'Rel Error':<14}")
    print("-" * 94)
    
    max_class_err = 0.0
    
    for scale in scales:
        mat_class = MaterialParameters(
            name=f"Classical Limit scale={scale:.1e}",
            rho=2000.0,
            mu=2000.0 * 1000.0**2,
            lambda_param=4.0e9,
            c=float(scale**2),
            d=float(scale),
            alpha_t=0.0
        )
        solver = AntiPlaneSolver(mat_class, xi=0.0)
        omega_class = mat_class.Vs * k_test
        omega_num, _, _ = solver.solve_numerical_omega(k_test)
        err = abs(omega_num - omega_class) / omega_class
        max_class_err = max(max_class_err, err)
        
        class_results.append({
            "scale_m": float(scale),
            "c_m2": float(scale**2),
            "d_m": float(scale),
            "omega_classical": float(omega_class),
            "omega_numerical": float(omega_num),
            "relative_error": float(err)
        })
        print(f"{scale:<12.1e} | {scale**2:<24.1e} | {omega_class:<18.6e} | {omega_num:<18.6e} | {err:<14.2e}")
        
    print("-" * 94)
    print(f"Gate G2-B Evaluation: Asymptotic Error at 10^-8 m = {class_results[-1]['relative_error']:.2e} (Pass criterion <= 0.5%)")
    pass_g2b = (class_results[-1]["relative_error"] <= 0.005)
    print(f"Gate G2-B Status: {'PASS' if pass_g2b else 'FAIL'}\n")
    
    # Generate Figure 3: Classical Limit Convergence
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    sc_vals = [r["scale_m"] for r in class_results]
    err_class_vals = [r["relative_error"] for r in class_results]
    
    ax.loglog(sc_vals, np.maximum(err_class_vals, 1e-16), 's-', color='#1f77b4', lw=2, ms=6, label='TMM Error vs Classical Limit $\\omega = V_s k$')
    ax.axhline(0.005, color='red', linestyle='--', lw=1.5, label='Pass Criterion (0.5% Threshold)')
    ax.set_xlabel('Microstructure Scale Parameter $g, h$ (m)', fontsize=11)
    ax.set_ylabel('Relative Error vs Classical Dispersion', fontsize=11)
    ax.set_title('Figure 3: Classical Limit Asymptotic Recovery ($c, d \\to 0$)', fontsize=12)
    ax.set_ylim([1e-17, 1e-1])
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.legend(frameon=True, fontsize=10)
    plt.tight_layout()
    fig3_path = "paper10/figures/fig3_classical_limit.png"
    plt.savefig(fig3_path)
    plt.close()
    print(f"Generated Figure 3: {fig3_path}")
    
    return max_class_err, pass_g2b


if __name__ == "__main__":
    max_rel_err, max_res, worst_cond, worst_det, pass_g2c = run_papargyri_beskou_benchmark()
    max_class_err, pass_g2b = run_classical_limit_benchmark()
    
    print("================================================================================")
    print(f"SUMMARY: Gate G2-B (Classical Limit): {'PASS' if pass_g2b else 'FAIL'}")
    print(f"SUMMARY: Gate G2-C (Papargyri-Beskou): {'PASS' if pass_g2c else 'FAIL'} (Max Err: {max_rel_err:.2e})")
    print("================================================================================")
