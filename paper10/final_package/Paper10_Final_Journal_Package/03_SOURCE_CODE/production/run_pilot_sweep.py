"""
Phase 3A Pilot Sweep Runner
Executes diagnostic sweep across 6 representative cases to evaluate numerical stability,
branch continuity, conditioning, and physical sanity before production sweeps.
"""

import sys
import os
import json
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver.parameters import MaterialParameters, UnitCellGeometry
from solver.antiplane import AntiPlaneSolver
from solver.coupled10 import Coupled10StateSolver


def get_production_materials():
    """Extract production material parameters locked in Blueprint Section 6."""
    a = 0.01  # 10 mm
    
    # Layer A (Epoxy)
    rho1 = 1180.0
    Vs1 = 1160.0
    Vp1 = 2830.0
    mu1 = rho1 * Vs1**2
    lambda1 = rho1 * Vp1**2 - 2.0 * mu1
    c1 = (0.5 * a)**2
    d1 = 0.5 * a
    
    # Layer B (Aluminum - normalized benchmark)
    rho2 = 0.1573 * rho1
    Vs2 = 0.5947 * Vs1
    Vp2 = 0.562 * Vp1
    mu2 = rho2 * Vs2**2
    lambda2 = rho2 * Vp2**2 - 2.0 * mu2
    c2 = c1 / 0.77
    d2 = d1 / 2.0
    
    matA = MaterialParameters(
        name="Epoxy (Layer A)",
        rho=rho1,
        mu=mu1,
        lambda_param=lambda1,
        c=c1,
        d=d1,
        k=0.2,
        cv=1000.0,
        alpha_t=6.0e-5,
        T0=300.0,
        tau_q=1.0e-11,
        tau_theta=2.0e-12
    )
    
    matB = MaterialParameters(
        name="Aluminum (Layer B)",
        rho=rho2,
        mu=mu2,
        lambda_param=lambda2,
        c=c2,
        d=d2,
        k=205.0,
        cv=900.0,
        alpha_t=2.3e-5,
        T0=300.0,
        tau_q=1.0e-11,
        tau_theta=2.0e-12
    )
    
    return matA, matB, a


def track_branches(prev_modes, curr_modes):
    """
    Branch tracking using linear sum assignment based on complex wavenumber proximity
    and modal overlap.
    """
    if prev_modes is None:
        # Assign initial branch IDs 0 to len-1
        for idx, m in enumerate(curr_modes):
            m["branch_id"] = idx
        return curr_modes
        
    N = len(prev_modes)
    cost_matrix = np.zeros((N, N))
    
    for i, m_prev in enumerate(prev_modes):
        k_prev = m_prev["kr_a"] + 1j * m_prev["ki_signed"]
        for j, m_curr in enumerate(curr_modes):
            k_curr = m_curr["kr_a"] + 1j * m_curr["ki_signed"]
            # Complex wavenumber distance normalized
            dist_k = abs(k_curr - k_prev) / (abs(k_prev) + 0.1)
            cost_matrix[i, j] = dist_k
            
    cost_matrix = np.nan_to_num(cost_matrix, nan=1e5, posinf=1e5, neginf=1e5)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Assign branch IDs based on matching
    for r, c in zip(row_ind, col_ind):
        curr_modes[c]["branch_id"] = prev_modes[r]["branch_id"]
        
    return curr_modes


def run_case_sweep(case_id: str, case_name: str, matA: MaterialParameters, matB: MaterialParameters, a1: float, a2: float, Omega_grid: np.ndarray, vm: float, a_total: float):
    print(f"\n--- Running Pilot Case {case_id}: {case_name} ---")
    case_data = []
    prev_modes = None
    
    worst_cond_P = 0.0
    worst_cond_T = 0.0
    worst_det_err = 0.0
    
    for Om in Omega_grid:
        omega = Om * 2.0 * np.pi * vm / a_total
        
        # Compute unit cell
        cell_info = Coupled10StateSolver.compute_periodic_unit_cell_10(matA, matB, a1, a2, omega, xi=0.0)
        
        # Track condition numbers
        solverA = Coupled10StateSolver(matA, xi=0.0)
        _, _, cond_PA = solverA.compute_modal_matrix(omega)
        cond_Tcell = cell_info["cond_Tcell"]
        
        worst_cond_P = max(worst_cond_P, cond_PA)
        worst_cond_T = max(worst_cond_T, cond_Tcell)
        
        # Track branches
        raw_modes = cell_info["bloch_modes"]
        tracked_modes = track_branches(prev_modes, raw_modes)
        prev_modes = tracked_modes
        
        for m in tracked_modes:
            case_data.append({
                "case_id": case_id,
                "case_name": case_name,
                "Omega": float(Om),
                "omega_rad_s": float(omega),
                "branch_id": int(m["branch_id"]),
                "kr_a": float(m["kr_a"]),
                "ki_signed": float(m["ki_signed"]),
                "alpha_a": float(m["alpha_a"]),
                "is_forward_decaying": bool(m["is_forward_decaying"]),
                "eigval_real": float(np.real(m["eigval"])),
                "eigval_imag": float(np.imag(m["eigval"])),
                "cond_P_equil": float(cond_PA),
                "cond_Tcell": float(cond_Tcell)
            })
            
    print(f"  ✓ Completed {len(Omega_grid)} frequencies. Worst cond(P)={worst_cond_P:.2e}, worst cond(T)={worst_cond_T:.2e}")
        
    return case_data, worst_cond_P, worst_cond_T


def main():
    t_start = time.time()
    print("================================================================================")
    print("PHASE 3A PILOT SWEEP — 6 REPRESENTATIVE TEST CASES")
    print("================================================================================")
    
    matA_base, matB_base, a = get_production_materials()
    vm = a / (0.5 * a / matA_base.Vs + 0.5 * a / matB_base.Vs)
    Omega_grid = np.linspace(0.05, 1.80, 50)
    
    all_results = []
    case_summaries = {}
    
    # ---------------------------------------------------------
    # CASE 1: Baseline Conservative Periodic (beta -> 0)
    # ---------------------------------------------------------
    matA_c1 = MaterialParameters(**{**matA_base.__dict__, "alpha_t": 0.0})
    matB_c1 = MaterialParameters(**{**matB_base.__dict__, "alpha_t": 0.0})
    data_c1, cond_p1, cond_t1 = run_case_sweep(
        "C1", "Conservative Baseline (beta -> 0)", matA_c1, matB_c1, 0.005, 0.005, Omega_grid, vm, a
    )
    all_results.extend(data_c1)
    
    # Also evaluate pure mechanical conservative transfer matrix check (4x4 SH sector)
    worst_mech_det_err = 0.0
    for Om in Omega_grid:
        w = Om * 2.0 * np.pi * vm / a
        cell_mech = AntiPlaneSolver.compute_periodic_unit_cell(matA_c1, matB_c1, 0.005, 0.005, w, xi=0.0)
        worst_mech_det_err = max(worst_mech_det_err, cell_mech["det_err"])
    print(f"  ✓ Authoritative 4x4 Mechanical Conservative Symplecticity Error: {worst_mech_det_err:.2e}")
    case_summaries["C1"] = {"worst_cond_P": cond_p1, "worst_cond_T": cond_t1, "worst_mech_det_err": worst_mech_det_err}
    
    # ---------------------------------------------------------
    # CASE 2: Baseline Active DPL Periodic
    # ---------------------------------------------------------
    data_c2, cond_p2, cond_t2 = run_case_sweep(
        "C2", "Active DPL Baseline", matA_base, matB_base, 0.005, 0.005, Omega_grid, vm, a
    )
    all_results.extend(data_c2)
    case_summaries["C2"] = {"worst_cond_P": cond_p2, "worst_cond_T": cond_t2, "worst_det_err": None}
    
    # ---------------------------------------------------------
    # CASE 3: Weak Contrast / Identical Layers (A = B)
    # ---------------------------------------------------------
    data_c3, cond_p3, cond_t3 = run_case_sweep(
        "C3", "Identical Layers Limit (A = B)", matA_base, matA_base, 0.005, 0.005, Omega_grid, vm, a
    )
    all_results.extend(data_c3)
    case_summaries["C3"] = {"worst_cond_P": cond_p3, "worst_cond_T": cond_t3, "worst_det_err": None}
    
    # ---------------------------------------------------------
    # CASE 4: Asymmetric Thickness (eta = 0.2: a1=2mm, a2=8mm)
    # ---------------------------------------------------------
    data_c4, cond_p4, cond_t4 = run_case_sweep(
        "C4", "Asymmetric Filling Fraction (eta = 0.2)", matA_base, matB_base, 0.002, 0.008, Omega_grid, vm, a
    )
    all_results.extend(data_c4)
    case_summaries["C4"] = {"worst_cond_P": cond_p4, "worst_cond_T": cond_t4, "worst_det_err": None}
    
    # ---------------------------------------------------------
    # CASE 5: Classical Elastic Limit (c, d -> 0)
    # ---------------------------------------------------------
    scale = 1.0e-5
    matA_c5 = MaterialParameters(**{**matA_base.__dict__, "c": scale**2, "d": scale})
    matB_c5 = MaterialParameters(**{**matB_base.__dict__, "c": scale**2, "d": scale})
    data_c5, cond_p5, cond_t5 = run_case_sweep(
        "C5", "Classical Limit Pilot (c, d -> 0)", matA_c5, matB_c5, 0.005, 0.005, Omega_grid, vm, a
    )
    all_results.extend(data_c5)
    case_summaries["C5"] = {"worst_cond_P": cond_p5, "worst_cond_T": cond_t5, "worst_det_err": None}
    
    # ---------------------------------------------------------
    # CASE 6: Extended Relaxation Lag (tau_q = 1e-9 s, tau_theta = 1e-10 s)
    # ---------------------------------------------------------
    matA_c6 = MaterialParameters(**{**matA_base.__dict__, "tau_q": 1.0e-9, "tau_theta": 1.0e-10})
    matB_c6 = MaterialParameters(**{**matB_base.__dict__, "tau_q": 1.0e-9, "tau_theta": 1.0e-10})
    data_c6, cond_p6, cond_t6 = run_case_sweep(
        "C6", "Extended Relaxation Lag (tau_q=1ns)", matA_c6, matB_c6, 0.005, 0.005, Omega_grid, vm, a
    )
    all_results.extend(data_c6)
    case_summaries["C6"] = {"worst_cond_P": cond_p6, "worst_cond_T": cond_t6, "worst_det_err": None}
    
    runtime = time.time() - t_start
    print(f"\n================================================================================")
    print(f"PILOT SWEEP COMPLETED IN {runtime:.2f} s. Total Data Points: {len(all_results)}")
    print("================================================================================")
    
    # Save machine-readable files
    os.makedirs("paper10/production", exist_ok=True)
    os.makedirs("paper10/figures/phase3a", exist_ok=True)
    
    csv_file = "paper10/production/PHASE3A_PILOT_RESULTS.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)
    print(f"Saved CSV: {csv_file}")
    
    json_file = "paper10/production/PHASE3A_PILOT_RESULTS.json"
    with open(json_file, "w") as f:
        json.dump({
            "phase": "3A",
            "runtime_seconds": runtime,
            "cases_count": 6,
            "frequency_points": len(Omega_grid),
            "total_modes_extracted": len(all_results),
            "case_summaries": case_summaries
        }, f, indent=2)
    print(f"Saved JSON: {json_file}")
    
    # ---------------------------------------------------------
    # GENERATE DIAGNOSTIC FIGURES (Figures 1 to 5)
    # ---------------------------------------------------------
    print("\nGenerating Diagnostic Figures in paper10/figures/phase3a/...")
    
    # Helper to filter case data
    def get_case(cid):
        return [r for r in all_results if r["case_id"] == cid and r["is_forward_decaying"]]
        
    c1_fwd = get_case("C1")
    c2_fwd = get_case("C2")
    c3_fwd = get_case("C3")
    c4_fwd = get_case("C4")
    c6_fwd = get_case("C6")
    
    # Figure 1: Complex Bloch dispersion kr*a/pi vs Omega
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    for b in range(10):
        b_pts = [r for r in c2_fwd if r["branch_id"] == b]
        if b_pts:
            ax.plot([r["kr_a"]/np.pi for r in b_pts], [r["Omega"] for r in b_pts], '.-', ms=4, lw=1.2, label=f'Branch {b}' if b < 5 else "")
    ax.set_xlabel('Real Bloch Wavenumber $k_r a / \\pi$', fontsize=11)
    ax.set_ylabel('Normalized Frequency $\\Omega = \\omega a / (2\\pi v_m)$', fontsize=11)
    ax.set_title('Figure 1: Complex Bloch Real Dispersion (Case C2: Active DPL)', fontsize=12)
    ax.set_xlim([0.0, 1.0])
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig("paper10/figures/phase3a/fig1_bloch_dispersion.png")
    plt.close()
    
    # Figure 2: Attenuation Magnitude alpha*a vs Omega
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    for b in range(10):
        b_pts = [r for r in c2_fwd if r["branch_id"] == b]
        if b_pts:
            ax.semilogy([r["Omega"] for r in b_pts], [max(r["alpha_a"], 1e-6) for r in b_pts], '.-', ms=4, lw=1.2, label=f'Branch {b}' if b < 5 else "")
    ax.set_xlabel('Normalized Frequency $\\Omega$', fontsize=11)
    ax.set_ylabel('Attenuation Diagnostic $\\alpha a = |k_i a|$', fontsize=11)
    ax.set_title('Figure 2: Spatial Attenuation Spectra Across Branches (Case C2)', fontsize=12)
    ax.set_ylim([1e-6, 50.0])
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig("paper10/figures/phase3a/fig2_attenuation.png")
    plt.close()
    
    # Figure 3: Conditioning Diagnostics
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    om_c2 = [r["Omega"] for r in c2_fwd[::5]]
    cond_p_c2 = [r["cond_P_equil"] for r in c2_fwd[::5]]
    cond_t_c2 = [r["cond_Tcell"] for r in c2_fwd[::5]]
    ax.semilogy(om_c2, cond_p_c2, 'b^-', ms=5, lw=1.5, label='Modal Matrix $\\kappa(P_{\\rm equil})$')
    ax.semilogy(om_c2, cond_t_c2, 'ro-', ms=5, lw=1.5, label='Transfer Matrix $\\kappa(T_{\\rm cell})$')
    ax.axhline(1e12, color='red', linestyle='--', label='Warning Threshold ($10^{12}$)')
    ax.set_xlabel('Normalized Frequency $\\Omega$', fontsize=11)
    ax.set_ylabel('Condition Number $\\kappa$', fontsize=11)
    ax.set_title('Figure 3: Numerical Conditioning vs Frequency (Case C2)', fontsize=12)
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig("paper10/figures/phase3a/fig3_conditioning.png")
    plt.close()
    
    # Figure 4: Branch Tracking Continuity Diagnostic
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    for b in range(5):
        b_pts = [r for r in c4_fwd if r["branch_id"] == b]
        if b_pts:
            ax.plot([r["Omega"] for r in b_pts], [r["kr_a"]/np.pi for r in b_pts], 'o-', ms=3, lw=1.5, label=f'Tracked Branch {b}')
    ax.set_xlabel('Normalized Frequency $\\Omega$', fontsize=11)
    ax.set_ylabel('Tracked Real Wavenumber $k_r a / \\pi$', fontsize=11)
    ax.set_title('Figure 4: Branch Tracking Continuity Across Frequency (Case C4)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig("paper10/figures/phase3a/fig4_branch_tracking.png")
    plt.close()
    
    # Figure 5: Direct Comparison: Conservative (C1) vs Active DPL (C2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300, sharey=True)
    
    # Subplot 1: Conservative C1
    for b in range(5):
        b_pts = [r for r in c1_fwd if r["branch_id"] == b]
        if b_pts:
            ax1.plot([r["kr_a"]/np.pi for r in b_pts], [r["Omega"] for r in b_pts], 'b.', ms=4)
    ax1.set_xlabel('Real Bloch Wavenumber $k_r a / \\pi$', fontsize=11)
    ax1.set_ylabel('Normalized Frequency $\\Omega$', fontsize=11)
    ax1.set_title(r'(a) Conservative Limit ($\beta \to 0$)', fontsize=11)
    ax1.set_xlim([0.0, 1.0])
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Subplot 2: Active DPL C2
    for b in range(5):
        b_pts = [r for r in c2_fwd if r["branch_id"] == b]
        if b_pts:
            ax2.plot([r["kr_a"]/np.pi for r in b_pts], [r["Omega"] for r in b_pts], 'r.', ms=4)
    ax2.set_xlabel('Real Bloch Wavenumber $k_r a / \\pi$', fontsize=11)
    ax2.set_title('(b) Active DPL Thermoelasticity', fontsize=11)
    ax2.set_xlim([0.0, 1.0])
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    fig.suptitle('Figure 5: Phase 3A Pilot Diagnostic — Conservative Limit vs Active DPL', fontsize=12)
    plt.tight_layout()
    plt.savefig("paper10/figures/phase3a/fig5_conservative_vs_dpl.png")
    plt.close()
    
    print("All diagnostic figures generated successfully.")
    return all_results, case_summaries, runtime


if __name__ == "__main__":
    main()
