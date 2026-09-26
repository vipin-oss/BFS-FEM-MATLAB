"""
Benchmark Validation Runner for Paper 10 (Phase 2 - Authoritative TMM Secular Benchmark)
Tests:
1. Gate G2-C: Papargyri-Beskou et al. (2009, IJSS) Gradient Elastic Dispersion Benchmark
   - Primary Authoritative: Independent TMM Secular Determinant Solve det(T - lambda*I) = 0
   - Secondary Diagnostic: Internal Scalar Characteristic-Root Consistency Check beta_s(w) - k = 0
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
    print("GATE G2-C: Papargyri-Beskou et al. (2009, IJSS) Authoritative Independent Benchmark")
    print("================================================================================")
    
    mat = get_benchmark_papargyri_beskou_material()
    solver = AntiPlaneSolver(mat, xi=0.0)
    
    # Prescribed test wavenumbers k across physical dispersion regimes (m^-1)
    k_grid = np.linspace(10.0, 2000.0, 50)
    
    results = []
    
    print(f"{'k (m^-1)':<10} | {'Omega_PB (rad/s)':<18} | {'Omega_TMM_indep':<18} | {'TMM Rel Err':<13} | {'Secular Res':<13} | {'Scalar Check Err':<16}")
    print("-" * 98)
    
    max_tmm_rel_err = 0.0
    max_secular_res = 0.0
    max_scalar_err = 0.0
    convergence_failures = 0
    
    for k in k_grid:
        omega_pb = solver.papargyri_beskou_analytical_omega(k)
        
        # 1. Authoritative Independent TMM Secular Solve
        try:
            omega_tmm, tmm_rel_err, secular_res = solver.solve_tmm_secular_omega(k)
        except Exception as e:
            convergence_failures += 1
            print(f"FAILED secular solve at k={k}: {e}")
            continue
            
        # 2. Internal Scalar Characteristic-Root Consistency Check
        omega_scalar, scalar_err, scalar_res = solver.solve_numerical_omega(k)
        
        # Condition numbers and symplecticity check
        P, cond_P_raw, cond_P_scaled = solver.compute_modal_matrix(omega_tmm)
        T_sol = solver.compute_transfer_matrix_analytical(omega_tmm, 0.005)
        symp = solver.check_symplectic_properties(T_sol)
        
        max_tmm_rel_err = max(max_tmm_rel_err, tmm_rel_err)
        max_secular_res = max(max_secular_res, secular_res)
        max_scalar_err = max(max_scalar_err, scalar_err)
        
        results.append({
            "k": float(k),
            "omega_analytical_pb": float(omega_pb),
            "omega_tmm_independent": float(omega_tmm),
            "tmm_relative_error": float(tmm_rel_err),
            "secular_residual": float(secular_res),
            "omega_scalar_consistency": float(omega_scalar),
            "scalar_consistency_rel_err": float(scalar_err),
            "scaled_cond_P": float(cond_P_scaled),
            "det_T_error": float(symp["det_err"])
        })
        
        # Print sample rows
        if k in k_grid[::10] or k == k_grid[-1]:
            print(f"{k:<10.1f} | {omega_pb:<18.6e} | {omega_tmm:<18.6e} | {tmm_rel_err:<13.2e} | {secular_res:<13.2e} | {scalar_err:<16.2e}")
            
    print("-" * 98)
    print(f"Independent TMM Secular Benchmark Evaluation (50 points):")
    print(f"  • Maximum Independent Relative Error: {max_tmm_rel_err:.2e} (Pass criterion <= 0.5%)")
    print(f"  • Maximum Secular Residual:           {max_secular_res:.2e}")
    print(f"  • Convergence Failures:               {convergence_failures}")
    print(f"Internal Scalar Characteristic-Root Check:")
    print(f"  • Maximum Scalar Consistency Error:  {max_scalar_err:.2e}")
    
    pass_g2c = (max_tmm_rel_err <= 0.005) and (convergence_failures == 0)
    print(f"\nGate G2-C Independent Benchmark Status: {'PASS' if pass_g2c else 'FAIL'}\n")
    
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
            "benchmark_type": "Authoritative Independent TMM Secular Determinant Solve",
            "material": mat.name,
            "Vs": mat.Vs,
            "c": mat.c,
            "d": mat.d,
            "points_count": len(results),
            "convergence_failures": convergence_failures,
            "max_tmm_relative_error": max_tmm_rel_err,
            "max_secular_residual": max_secular_res,
            "max_scalar_consistency_error": max_scalar_err,
            "gate_G2_C_status": "PASS" if pass_g2c else "FAIL",
            "data": results
        }, f, indent=2)
    print(f"Saved JSON results: {json_file}")
    
    # Generate Figure 1 & Figure 2
    # Fig 1: Analytical vs Independent Numerical TMM Dispersion
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    k_vals = [r["k"] for r in results]
    w_ex = [r["omega_analytical_pb"] for r in results]
    w_tmm = [r["omega_tmm_independent"] for r in results]
    
    ax.plot(k_vals, np.array(w_ex) / 1e6, 'b-', lw=2.2, label='Analytical Reference (PB 2009 Eq. 28)')
    ax.plot(k_vals, np.array(w_tmm) / 1e6, 'ro', ms=5, markevery=3, label='Independent TMM Secular Solve det(T-λI)=0')
    ax.set_xlabel('Wavenumber $k$ (m$^{-1}$)', fontsize=11)
    ax.set_ylabel('Angular Frequency $\\omega$ (Mrad/s)', fontsize=11)
    ax.set_title('Figure 1: Gate G2-C — Authoritative Independent TMM Benchmark vs PB (2009)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(frameon=True, fontsize=10)
    plt.tight_layout()
    fig1_path = "paper10/figures/fig1_papargyri_beskou_benchmark.png"
    plt.savefig(fig1_path)
    plt.close()
    print(f"Generated Figure 1: {fig1_path}")
    
    # Fig 2: Independent Relative Error versus Wavenumber
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    err_vals = [r["tmm_relative_error"] for r in results]
    ax.semilogy(k_vals, np.maximum(err_vals, 1e-16), 'd-', color='#2ca02c', lw=1.8, ms=5, label='Independent TMM Error $|\\omega_{\\rm TMM} - \\omega_{\\rm PB}| / \\omega_{\\rm PB}$')
    ax.axhline(0.005, color='red', linestyle='--', lw=1.5, label='Pass Criterion (0.5% Threshold)')
    ax.set_xlabel('Wavenumber $k$ (m$^{-1}$)', fontsize=11)
    ax.set_ylabel('Relative Error', fontsize=11)
    ax.set_title('Figure 2: Relative Error vs Wavenumber (Independent Secular TMM Solve)', fontsize=12)
    ax.set_ylim([1e-17, 1e-1])
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.legend(frameon=True, fontsize=10)
    plt.tight_layout()
    fig2_path = "paper10/figures/fig2_benchmark_relative_error.png"
    plt.savefig(fig2_path)
    plt.close()
    print(f"Generated Figure 2: {fig2_path}")
    
    return max_tmm_rel_err, max_secular_res, convergence_failures, pass_g2c


def run_classical_limit_benchmark():
    print("\n================================================================================")
    print("GATE G2-B: Classical Acoustic Limit (c, d -> 0) Benchmark")
    print("================================================================================")
    
    scales = np.logspace(-4, -8, 5) # m
    k_test = 200.0 # m^-1
    class_results = []
    
    print(f"{'Scale (m)':<12} | {'Micro-stiffness c (m^2)':<24} | {'Omega_classical':<18} | {'Omega_tmm_secular':<18} | {'Rel Error':<14}")
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
        omega_tmm, err, res = solver.solve_tmm_secular_omega(k_test)
        err_class = abs(omega_tmm - omega_class) / omega_class
        max_class_err = max(max_class_err, err_class)
        
        class_results.append({
            "scale_m": float(scale),
            "c_m2": float(scale**2),
            "d_m": float(scale),
            "omega_classical": float(omega_class),
            "omega_tmm": float(omega_tmm),
            "relative_error": float(err_class)
        })
        print(f"{scale:<12.1e} | {scale**2:<24.1e} | {omega_class:<18.6e} | {omega_tmm:<18.6e} | {err_class:<14.2e}")
        
    print("-" * 94)
    print(f"Gate G2-B Evaluation: Asymptotic Error at 10^-8 m = {class_results[-1]['relative_error']:.2e} (Pass criterion <= 0.5%)")
    pass_g2b = (class_results[-1]["relative_error"] <= 0.005)
    print(f"Gate G2-B Status: {'PASS' if pass_g2b else 'FAIL'}\n")
    
    # Generate Figure 3: Classical Limit Convergence
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    sc_vals = [r["scale_m"] for r in class_results]
    err_class_vals = [r["relative_error"] for r in class_results]
    
    ax.loglog(sc_vals, np.maximum(err_class_vals, 1e-16), 's-', color='#1f77b4', lw=2, ms=6, label='TMM Secular Error vs Classical $\\omega = V_s k$')
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
    max_tmm_err, max_res, fail_count, pass_g2c = run_papargyri_beskou_benchmark()
    max_class_err, pass_g2b = run_classical_limit_benchmark()
    
    print("================================================================================")
    print(f"SUMMARY: Gate G2-B (Classical Limit): {'PASS' if pass_g2b else 'FAIL'}")
    print(f"SUMMARY: Gate G2-C (Authoritative Independent Benchmark): {'PASS' if pass_g2c else 'FAIL'} (Max Err: {max_tmm_err:.2e})")
    print("================================================================================")
