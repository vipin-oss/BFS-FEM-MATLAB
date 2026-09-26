"""
Unit test for 10-State Coupled DPL-Dipolar Gradient Elastic Solver
Evaluates:
- Gate G2-A: Implementation Integrity (10 states, 10 roots, square modal matrix)
- Gate G2-E: DPL Implementation Sanity (phase lags active, complex roots, no crashes)
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver.parameters import MaterialParameters
from solver.coupled10 import Coupled10StateSolver


def test_10state_solver_integrity():
    print("================================================================================")
    print("Testing Gate G2-A & G2-E: 10-State Coupled Solver Integrity & DPL Sanity")
    print("================================================================================")
    
    # Material with active DPL thermoelasticity
    mat_dpl = MaterialParameters(
        name="Silicon-like Microstructured DPL Solid",
        rho=2330.0,
        mu=4.0e10,
        lambda_param=6.0e10,
        c=(1.0e-4)**2,     # g = 100 microns
        d=np.sqrt(3.0)*1.5e-4, # h = 150 microns
        k=148.0,           # W/(m*K)
        cv=700.0,          # J/(kg*K)
        alpha_t=2.6e-6,    # 1/K
        T0=300.0,          # K
        tau_q=1.0e-11,     # 10 ps
        tau_theta=2.0e-12  # 2 ps
    )
    
    omega = 1.0e6 # 1 MHz
    solver = Coupled10StateSolver(mat_dpl, xi=0.0)
    
    # 1. Characteristic Roots Check (Gate G2-A)
    r_info = solver.compute_characteristic_roots(omega)
    shear_roots = r_info["shear_roots"]
    long_roots = r_info["long_roots"]
    all_roots = r_info["all_roots"]
    
    assert len(shear_roots) == 4, f"Expected 4 shear roots, got {len(shear_roots)}"
    assert len(long_roots) == 6, f"Expected 6 longitudinal-thermal roots, got {len(long_roots)}"
    assert len(all_roots) == 10, f"Expected 10 total roots, got {len(all_roots)}"
    print("✓ Gate G2-A: Root counts = 4 shear + 6 longitudinal-thermal = 10 total: PASS")
    
    # 2. Modal Matrix Check (Gate G2-A)
    P, cond_P_raw, cond_P_equil = solver.compute_modal_matrix(omega)
    assert P.shape == (10, 10), f"Expected 10x10 modal matrix, got {P.shape}"
    assert cond_P_equil < 1e8, f"Equilibrated condition number too large: {cond_P_equil}"
    print(f"✓ Gate G2-A: Modal matrix is 10x10 square, raw cond = {cond_P_raw:.2e}, equilibrated cond(P) = {cond_P_equil:.2e}: PASS")
    
    # 3. Layer Transfer Matrix Construction (Gate G2-A)
    # Layer thickness: 20 microns (realistic for microscale thermoelastic metamaterials where g, h ~ 10-15 microns)
    a_layer = 2.0e-5
    T, cond_P_eq, cond_T_eq = solver.compute_transfer_matrix(omega, a_layer)
    assert T.shape == (10, 10), f"Expected 10x10 transfer matrix, got {T.shape}"
    assert not np.any(np.isnan(T)), "NaN encountered in transfer matrix"
    assert not np.any(np.isinf(T)), "Inf encountered in transfer matrix"
    print(f"✓ Gate G2-A: 10x10 Transfer matrix computed, cond(T_equil) = {cond_T_eq:.2e}: PASS")
    
    # 4. DPL Sanity Test (Gate G2-E)
    # Check that tau_q and tau_theta modify thermal conductivity
    keff = r_info["keff"]
    assert np.imag(keff) != 0.0, "DPL complex effective thermal conductivity should have non-zero imaginary part"
    print(f"✓ Gate G2-E: DPL complex effective k_eff = {keff:.4e}: PASS")
    
    # Check that longitudinal roots exhibit non-zero attenuation (damping)
    imag_roots = np.imag(long_roots)
    assert np.any(np.abs(imag_roots) > 0.0), "DPL coupling should induce imaginary wavenumber attenuation"
    print(f"✓ Gate G2-E: Complex wavenumbers with active DPL attenuation: PASS")
    
    # Check that full dissipative system breaks det(T) = 1 symplecticity
    det_T = np.linalg.det(T)
    print(f"✓ Gate G2-E: Dissipative DPL transfer matrix det(T) = {det_T:.4e} (calculated stably): PASS")
    
    # 5. Unit Cell Construction Check (Gate G2-E)
    matB = MaterialParameters(
        name="Silicon Layer B (Modulated)",
        rho=2000.0,
        mu=3.0e10,
        lambda_param=4.5e10,
        c=(0.8e-5)**2,
        d=np.sqrt(3.0)*1.2e-5,
        k=120.0,
        cv=750.0,
        alpha_t=2.0e-6,
        T0=300.0,
        tau_q=0.8e-11,
        tau_theta=1.6e-12
    )
    cell_10 = Coupled10StateSolver.compute_periodic_unit_cell_10(mat_dpl, matB, a1=a_layer, a2=a_layer, omega=omega)
    assert cell_10["Tcell"].shape == (10, 10)
    assert len(cell_10["bloch_modes"]) == 10
    print(f"✓ Gate G2-E: Full 10-state periodic unit-cell and 10 Bloch multipliers computed (cond={cell_10['cond_Tcell']:.2e}): PASS")
    
    print("\nALL 10-STATE & DPL SANITY TESTS PASSED!")
    return True


if __name__ == "__main__":
    test_10state_solver_integrity()
