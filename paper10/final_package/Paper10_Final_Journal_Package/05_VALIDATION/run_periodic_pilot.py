"""
Gate G2-D: Periodic Conservative Two-Layer Pilot
Evaluates Transfer Matrix Bloch spectrum, Bragg band gaps, and Figure 4.
Reference: Li et al. (2016, Acta Mechanica 227(4), 1083-1100, Fig. 3)
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver.parameters import get_li_acta_mech_materials
from solver.antiplane import AntiPlaneSolver


def run_periodic_pilot():
    print("================================================================================")
    print("GATE G2-D: Two-Layer Conservative Periodic Phononic Crystal Pilot")
    print("================================================================================")
    
    a = 1.0
    matA, matB, geom = get_li_acta_mech_materials(a=a)
    vm = a / (geom.a1 / matA.Vs + geom.a2 / matB.Vs)
    
    # Frequency sweep matching normalized frequency Omega = omega * a / (2*pi*vm)
    Omega_grid = np.linspace(0.01, 1.8, 180)
    
    pass_band_points = []
    gap_points = []
    worst_det_err = 0.0
    worst_cond_T = 0.0
    
    for Om in Omega_grid:
        w = Om * 2.0 * np.pi * vm / a
        cell_info = AntiPlaneSolver.compute_periodic_unit_cell(matA, matB, geom.a1, geom.a2, w, xi=0.0)
        
        worst_det_err = max(worst_det_err, cell_info["det_err"])
        worst_cond_T = max(worst_cond_T, cell_info["cond_Tcell"])
        
        has_prop = False
        for mode in cell_info["bloch_modes"]:
            if mode["is_propagating"]:
                pass_band_points.append((mode["kr_a"] / np.pi, Om, mode["ki_a"]))
                has_prop = True
        
        if not has_prop:
            # Band gap
            min_ki = min(m["ki_a"] for m in cell_info["bloch_modes"])
            gap_points.append((Om, min_ki))
            
    # Contiguous gap intervals
    gap_intervals = []
    if gap_points:
        start_om = gap_points[0][0]
        prev_om = start_om
        for om, _ in gap_points[1:]:
            if om - prev_om > 0.025:
                gap_intervals.append((start_om, prev_om))
                start_om = om
            prev_om = om
        gap_intervals.append((start_om, prev_om))
        
    print(f"Computed {len(pass_band_points)} pass-band points across Omega in [0.01, 1.80].")
    print(f"Identified {len(gap_intervals)} material-contrast Bragg band gap(s):")
    for idx, (low, high) in enumerate(gap_intervals):
        print(f"  Bragg Gap {idx+1}: Omega in [{low:.4f}, {high:.4f}] -> Width = {high-low:.4f}")
        
    print(f"Unit-Cell Transfer Matrix Symplectic det(Tcell) Error: {worst_det_err:.2e}")
    print(f"Worst Unit-Cell Condition Number kappa(Tcell): {worst_cond_T:.2e}")
    
    # Gate G2-D condition: identified pass bands, at least one Bragg gap, and det_err < 1e-4
    pass_g2d = (len(gap_intervals) >= 1) and (len(pass_band_points) > 50) and (worst_det_err < 1e-4)
    print(f"\nGate G2-D Status: {'PASS' if pass_g2d else 'FAIL'}\n")
    
    # Generate Figure 4: Two-Layer Bloch Dispersion & Band Gap Diagnostic
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=300, sharey=True)
    
    # Subplot 1: Real Bloch wavenumber Re(ka)/pi vs Omega
    kr_vals = [p[0] for p in pass_band_points]
    om_vals = [p[1] for p in pass_band_points]
    ax1.plot(kr_vals, om_vals, 'b.', ms=4, label='Propagating Bloch Modes')
    
    # Shade band gaps
    for idx, (low, high) in enumerate(gap_intervals):
        ax1.axhspan(low, high, color='lightgray', alpha=0.6, label='Bragg Band Gap' if idx == 0 else "")
        ax2.axhspan(low, high, color='lightgray', alpha=0.6)
        
    ax1.set_xlabel('Real Bloch Wavenumber $k_r a / \\pi$', fontsize=11)
    ax1.set_ylabel('Normalized Frequency $\\Omega = \\omega a / (2\\pi v_m)$', fontsize=11)
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.8])
    ax1.set_title('(a) Real Dispersion $k_r a / \\pi$', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right', frameon=True, fontsize=9)
    
    # Subplot 2: Imaginary attenuation Im(ka)/pi vs Omega
    gap_om = [g[0] for g in gap_points]
    gap_ki = [g[1] / np.pi for g in gap_points]
    ax2.plot(gap_ki, gap_om, 'r.', ms=4, label='Evanescent Decay $k_i a / \\pi$')
    ax2.set_xlabel('Imaginary Attenuation $k_i a / \\pi$', fontsize=11)
    ax2.set_xlim([0.0, 2.0])
    ax2.set_title('(b) Evanescent Attenuation in Band Gaps', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right', frameon=True, fontsize=9)
    
    fig.suptitle('Figure 4: Gate G2-D — Conservative Two-Layer Periodic Bloch Dispersion (Li et al. 2016)', fontsize=12)
    plt.tight_layout()
    fig4_path = "paper10/figures/fig4_two_layer_bloch.png"
    plt.savefig(fig4_path)
    plt.close()
    print(f"Generated Figure 4: {fig4_path}")
    
    # Save JSON summary
    with open("paper10/validation/periodic_pilot_results.json", "w") as f:
        json.dump({
            "test": "Gate G2-D Conservative Two-Layer Periodic Pilot",
            "lattice_constant_a": a,
            "pass_band_points_count": len(pass_band_points),
            "bragg_gaps": [{"lower": low, "upper": high, "width": high-low} for low, high in gap_intervals],
            "worst_det_err": worst_det_err,
            "worst_cond_T": worst_cond_T,
            "gate_G2_D_status": "PASS" if pass_g2d else "FAIL"
        }, f, indent=2)
        
    return pass_g2d


if __name__ == "__main__":
    run_periodic_pilot()
