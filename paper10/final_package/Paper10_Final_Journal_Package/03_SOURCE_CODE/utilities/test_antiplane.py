"""
Unit test for 4-state Anti-Plane Solver
Verifies Gate G2-A (Implementation Integrity), Modal vs Analytical Transfer Matrix,
Symplectic Invariants, and Limiting Behavior.
"""
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver.parameters import get_benchmark_papargyri_beskou_material, MaterialParameters
from solver.antiplane import AntiPlaneSolver

def test_antiplane_solver_integrity():
    mat = get_benchmark_papargyri_beskou_material()
    solver = AntiPlaneSolver(mat, xi=0.0)
    
    omega = 5.0e4 # rad/s
    a_layer = 0.01 # 1 cm
    
    # 1. Check Characteristic Roots & Dimensions
    r_info = solver.compute_characteristic_roots(omega)
    roots = r_info["roots"]
    assert len(roots) == 4, f"Expected 4 roots, got {len(roots)}"
    print("✓ Characteristic roots count = 4: PASS")
    
    # 2. Check Modal Matrix P
    P, cond_P_raw, cond_P_scaled = solver.compute_modal_matrix(omega)
    assert P.shape == (4, 4), f"Expected 4x4 modal matrix, got {P.shape}"
    assert cond_P_scaled < 100.0, f"Scaled condition number of P too high: {cond_P_scaled}"
    print(f"✓ Modal matrix shape 4x4, raw cond(P) = {cond_P_raw:.2e}, scaled cond(P) = {cond_P_scaled:.2f}: PASS")
    
    # 3. Check Modal T vs Analytical T
    T_modal, cond_P_sc, cond_T_sc = solver.compute_transfer_matrix_modal(omega, a_layer)
    T_analytical = solver.compute_transfer_matrix_analytical(omega, a_layer)
    
    rel_diff = np.max(np.abs(T_modal - T_analytical) / (np.abs(T_analytical) + 1e-12))
    assert rel_diff < 1e-10, f"Relative discrepancy between modal and analytical T: {rel_diff}"
    print(f"✓ Modal T vs Analytical T relative discrepancy = {rel_diff:.2e}: PASS")
    
    # 4. Check Symplectic Invariant det(T) == 1
    symp = solver.check_symplectic_properties(T_analytical)
    assert symp["det_err"] < 1e-7, f"det(T) - 1 exceeded tolerance: {symp['det_err']}"
    print(f"✓ Symplectic det(T) error = {symp['det_err']:.2e}: PASS")
    
    # 5. Check Dispersion match with Papargyri-Beskou
    k_test = 200.0 # m^-1
    omega_num, rel_err, residual = solver.solve_numerical_omega(k_test, a_layer=a_layer)
    omega_pb = solver.papargyri_beskou_analytical_omega(k_test)
    assert rel_err < 1e-10, f"Relative error with Papargyri-Beskou: {rel_err}"
    print(f"✓ Numerical vs PB exact dispersion relative error = {rel_err:.2e}: PASS")

def test_classical_limit():
    # Classical limit: c -> 0, d -> 0
    # Use microscale = 1e-6 m (c = 1e-12 m^2, d = 1e-6 m)
    scale = 1e-6
    mat_class = MaterialParameters(
        name="Classical Elastic Limit",
        rho=2000.0,
        mu=2000.0 * 1000.0**2,
        lambda_param=4.0e9,
        c=scale**2,
        d=scale,
        alpha_t=0.0
    )
    solver = AntiPlaneSolver(mat_class, xi=0.0)
    
    k_test = 150.0 # m^-1
    omega_num, rel_err, residual = solver.solve_numerical_omega(k_test)
    omega_classical = mat_class.Vs * k_test
    
    err_class = abs(omega_num - omega_classical) / omega_classical
    assert err_class < 1e-5, f"Classical limit error too high: {err_class}"
    print(f"✓ Classical limit Vs*k relative error = {err_class:.2e}: PASS")

if __name__ == "__main__":
    test_antiplane_solver_integrity()
    test_classical_limit()
    print("\nALL ANTIMODE UNIT TESTS PASSED SUCCESSFULLY!")
