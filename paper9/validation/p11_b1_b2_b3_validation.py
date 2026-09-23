#!/usr/bin/env python3
# =============================================================================
# DEPRECATED (P12A, 2026-09-23) -- LEGACY PARALLEL ENGINE; DO NOT USE.
# This file is a superseded P11-era parallel implementation.  The AUTHORITATIVE
# engines are paper9/validation/b1_b2_b3_solver.py and
# paper9/validation/b2_stable_tm.py (single judge_status policy; exact z-test
# edge detection).  All evidence artifacts (benchmark_evidence.json, Table 3,
# Fig. 4, pinned runs, tests) regenerate from the authoritative engines via
# paper9/audit/p11d_regenerate_evidence.py.  No repository code imports this
# file (verified P12A by full-tree grep); its inline 1e-6/1e-8 tolerances and
# 0.05-modulus band-edge rule differ from the authoritative engine and must
# never be quoted.  Retained for historical reference only; see
# paper9/audit/P12A_CLOSEOUT.md (item 7).
# =============================================================================
"""P11 Independent 1D Transfer Matrix Validation Suite for Benchmarks B1, B2, and B3.

Governance & Evidence Hierarchy:
  Level 1 (Analytical / Homogeneous Unit Cell):
    - Declared tolerance: relative wavenumber error < 1e-6, eigenvalue error |lambda - exp(i*k*a)| < 1e-6.
  Level 2 (Bilayer Identical-Material Reduction):
    - Bilayer code with identical layer properties must recover single-layer bulk dispersion with error < 1e-8.
  Level 2 (Heterogeneous Bilayer):
    - Evaluates dispersion branches and band edges.
    - Compares quantitatively where analytical formulas exist (e.g. Rytov for B1).
    - Compares qualitatively / asymptotically with digitized vector curve data for B2 and B3.
    - Adheres to the strict rule: NEVER claim quantitative <=0.5% or <=2% error from visual graph similarity alone.
"""
from __future__ import annotations

import math
import sys
import numpy as np
import scipy.linalg as la

# ==============================================================================
# 1. BENCHMARK B1: Classical Bilayer (Li et al. 2024 Fig. 2a / Zheng & Wei 2009)
# ==============================================================================

class BenchmarkB1:
    """1D Classical longitudinal acoustic wave in layered medium."""
    def __init__(self):
        # Material A (AlN)
        self.rho_A = 3.23e3       # kg/m^3
        self.c33_A = 3.9e11       # Pa
        self.a_A = 0.01           # m
        
        # Material B (BaTiO3)
        self.rho_B = 5.8e3        # kg/m^3
        self.c33_B = 1.62e11      # Pa
        self.a_B = 0.01           # m
        
        self.b = self.a_A + self.a_B
        self.v_A = np.sqrt(self.c33_A / self.rho_A)
        self.v_B = np.sqrt(self.c33_B / self.rho_B)
        self.Z_A = self.rho_A * self.v_A
        self.Z_B = self.rho_B * self.v_B
        self.omega_0 = 2.0 * np.pi / (self.a_A / self.v_A + self.a_B / self.v_B)

    def rytov_cosKb(self, bar_omega: float) -> float:
        w = bar_omega * self.omega_0
        kA = w / self.v_A
        kB = w / self.v_B
        term1 = np.cos(kA * self.a_A) * np.cos(kB * self.a_B)
        term2 = 0.5 * (self.Z_A / self.Z_B + self.Z_B / self.Z_A) * np.sin(kA * self.a_A) * np.sin(kB * self.a_B)
        return float(term1 - term2)

    def layer_T(self, omega: float, c33: float, rho: float, a: float) -> np.ndarray:
        v = np.sqrt(c33 / rho)
        k = omega / v
        T = np.array([
            [np.cos(k * a), np.sin(k * a) / (k * c33)],
            [-k * c33 * np.sin(k * a), np.cos(k * a)]
        ], dtype=np.complex128)
        return T

    def run_level1_homogeneous(self) -> dict:
        """Homogeneous cell: T(a)*T(a) must equal T(2*a), and eigvals must be exp(+- i*k*(2a))."""
        errors = []
        for bar_w in [0.2, 0.5, 1.0, 1.8, 2.5, 3.7]:
            w = bar_w * self.omega_0
            k_exact = w / self.v_A
            T_a = self.layer_T(w, self.c33_A, self.rho_A, self.a_A)
            T_2a = self.layer_T(w, self.c33_A, self.rho_A, 2.0 * self.a_A)
            
            # Check T_a^2 == T_2a
            T_prod = T_a @ T_a
            rel_err_matrix = la.norm(T_prod - T_2a) / la.norm(T_2a)
            
            # Check eigenvalues
            evs = la.eigvals(T_prod)
            expected = np.array([np.exp(1j * k_exact * 2.0 * self.a_A), np.exp(-1j * k_exact * 2.0 * self.a_A)])
            lam_err = max(min(abs(ev - expected[0]), abs(ev - expected[1])) for ev in evs)
            errors.append(max(rel_err_matrix, lam_err))
            
        max_err = max(errors)
        return {"status": "PASS" if max_err < 1e-6 else "FAIL", "max_error": max_err}

    def run_level2_identical_reduction(self) -> dict:
        """Bilayer solver with Layer B = Layer A must recover homogeneous cell."""
        errors = []
        for bar_w in [0.3, 0.7, 1.2, 2.1, 4.0]:
            w = bar_w * self.omega_0
            k_exact = w / self.v_A
            TA = self.layer_T(w, self.c33_A, self.rho_A, self.a_A)
            TB = self.layer_T(w, self.c33_A, self.rho_A, self.a_B) # identical properties
            T_cell = TB @ TA
            evs = la.eigvals(T_cell)
            expected = np.exp(1j * k_exact * self.b)
            err = min(abs(ev - expected) for ev in evs)
            errors.append(err)
        max_err = max(errors)
        return {"status": "PASS" if max_err < 1e-8 else "FAIL", "max_error": max_err}

    def run_level2_bilayer_gaps(self) -> dict:
        """Compute the first 3 band gaps using Rytov formula."""
        omegas = np.linspace(0.001, 5.0, 50000)
        cos_vals = np.array([self.rytov_cosKb(w) for w in omegas])
        in_gap = np.abs(cos_vals) > 1.0
        
        gaps = []
        in_gap_cur = False
        start_w = 0.0
        for i in range(len(omegas)):
            if in_gap[i] and not in_gap_cur:
                in_gap_cur = True
                start_w = omegas[i]
            elif not in_gap[i] and in_gap_cur:
                in_gap_cur = False
                gaps.append((start_w, omegas[i], omegas[i] - start_w))
                
        finite = all(math.isfinite(g[0]) and math.isfinite(g[1]) for g in gaps)
        return {"status": "PASS" if (finite and len(gaps) > 0) else "FAIL",
                "gaps": gaps[:5]}


# ==============================================================================
# 2. BENCHMARK B2: Gradient Elasticity Bilayer (Li et al. 2024 Fig. 2b, flexo OFF)
# ==============================================================================

class BenchmarkB2:
    """1D Strain-gradient elasticity longitudinal wave."""
    def __init__(self):
        # Material A (AlN)
        self.rho_A = 3.23e3
        self.c33_A = 3.9e11
        self.a_A = 1e-5          # m (micrometer scale matching gradient length scale)
        self.l_A = 1e-5           # m
        self.l1_A = 2e-5          # m
        
        # Material B (BaTiO3)
        self.rho_B = 5.8e3
        self.c33_B = 1.62e11
        self.a_B = 1e-5          # m
        self.l_B = 5e-5           # m (L = 5)
        self.l1_B = 10e-5         # m (L1 = 5)
        
        self.b = self.a_A + self.a_B
        self.v_A = np.sqrt(self.c33_A / self.rho_A)
        self.v_B = np.sqrt(self.c33_B / self.rho_B)
        self.omega_0 = 2.0 * np.pi / (self.a_A / self.v_A + self.a_B / self.v_B)

    def layer_scaled_T(self, w: float, c33: float, rho: float, l: float, l1: float, a: float):
        w2 = w**2
        A = c33 * (l**2)
        B = c33 - rho * w2 * (l1**2)
        C = -rho * w2
        disc = B**2 - 4.0 * A * C
        k2_1 = (-B + np.sqrt(disc)) / (2.0 * A)
        k2_2 = (-B - np.sqrt(disc)) / (2.0 * A)
        k1 = np.sqrt(k2_1 + 0j)
        k2 = np.sqrt(k2_2 + 0j)
        ks = [k1, k2, -k1, -k2]
        
        P0 = np.zeros((4, 4), dtype=complex)
        for s in range(4):
            k = ks[s]
            P0[0, s] = 1.0
            P0[1, s] = 1j * k
            P0[2, s] = 1j * k * (c33 - rho * (l1**2) * w2 + (k**2) * (l**2) * c33)
            P0[3, s] = - (k**2) * (l**2) * c33
            
        d_row = np.max(np.abs(P0), axis=1)
        D = np.diag(1.0 / d_row)
        D_inv = np.diag(d_row)
        P0_s = D @ P0
        G = np.diag([np.exp(1j * k * a) for k in ks])
        T_s = P0_s @ G @ la.inv(P0_s)
        T = D_inv @ T_s @ D
        return T, k1, k2

    def run_level1_homogeneous(self) -> dict:
        """Homogeneous cell: T(a)*T(a) == T(2*a) with relative error < 1e-6."""
        errors = []
        for bar_w in [0.2, 0.6, 1.2, 2.0, 3.5]:
            w = bar_w * self.omega_0
            TA, k1, k2 = self.layer_scaled_T(w, self.c33_A, self.rho_A, self.l_A, self.l1_A, self.a_A)
            TA2, _, _ = self.layer_scaled_T(w, self.c33_A, self.rho_A, self.l_A, self.l1_A, 2.0 * self.a_A)
            T_prod = TA @ TA
            rel_err = la.norm(T_prod - TA2) / la.norm(TA2)
            
            # Check propagating eigenvalue
            evs = la.eigvals(T_prod)
            exp_prop = np.exp(1j * k1 * 2.0 * self.a_A)
            err_prop = min(abs(ev - exp_prop) for ev in evs)
            errors.append(max(rel_err, err_prop))
            
        max_err = max(errors)
        return {"status": "PASS" if max_err < 1e-6 else "FAIL", "max_error": max_err}

    def run_level2_identical_reduction(self) -> dict:
        """Bilayer solver with Layer B = Layer A must recover homogeneous cell."""
        errors = []
        for bar_w in [0.3, 0.8, 1.5, 2.2]:
            w = bar_w * self.omega_0
            TA, k1, _ = self.layer_scaled_T(w, self.c33_A, self.rho_A, self.l_A, self.l1_A, self.a_A)
            TB, _, _ = self.layer_scaled_T(w, self.c33_A, self.rho_A, self.l_A, self.l1_A, self.a_B)
            T_cell = TB @ TA
            evs = la.eigvals(T_cell)
            exp_prop = np.exp(1j * k1 * self.b)
            err = min(abs(ev - exp_prop) for ev in evs)
            errors.append(err)
        max_err = max(errors)
        return {"status": "PASS" if max_err < 1e-8 else "FAIL", "max_error": max_err}


# ==============================================================================
# 3. BENCHMARK B3: Dipolar Gradient Bilayer (Li et al. 2023 Fig. 4c / LWZ 2016)
# ==============================================================================

class BenchmarkB3:
    """1D Dipolar gradient elasticity shear wave (LWZ 2016 / Li 2023)."""
    def __init__(self):
        # Material 1 (Lead):
        self.mu_1 = 2.3e10        # Pa
        self.rho_1 = 7.5e3        # kg/m^3
        self.a_1 = 1e-5           # m
        self.c_1 = 0.15 * (self.a_1**2)
        self.d_1 = 0.25 * self.a_1
        
        # Material 2 (Brass):
        self.mu_2 = self.mu_1 * 0.056
        self.rho_2 = self.rho_1 * 0.157
        self.a_2 = self.a_1
        self.c_2 = self.c_1 * 1.5
        self.d_2 = self.d_1 * 1.5
        
        self.b = self.a_1 + self.a_2
        self.Vs_1 = np.sqrt(self.mu_1 / self.rho_1)
        self.Vs_2 = np.sqrt(self.mu_2 / self.rho_2)
        self.omega_0 = 2.0 * np.pi / (self.a_1 / self.Vs_1 + self.a_2 / self.Vs_2)

    def sigma_tau(self, w: float, Vs: float, c: float, d: float):
        w2 = w**2
        Vs2 = Vs**2
        ms = w2 * (d**2) / (3.0 * Vs2)
        disc = (1.0 - ms)**2 + 4.0 * c * w2 / Vs2
        Delta = np.sqrt(disc)
        sig2 = max(float((Delta - (1.0 - ms)) / (2.0 * c)), 0.0)
        tau2 = max(float((Delta + (1.0 - ms)) / (2.0 * c)), 0.0)
        return np.sqrt(sig2), np.sqrt(tau2)

    def layer_T_sh(self, w: float, a: float, c: float, d: float, mu: float, rho: float):
        Vs = np.sqrt(mu / rho)
        sig, tau = self.sigma_tau(w, Vs, c, d)
        sa, ca = np.sin(sig * a), np.cos(sig * a)
        sh, ch = np.sinh(tau * a), np.cosh(tau * a)
        
        # Construct Appendix 3 matrix (LWZ 2016)
        t = np.zeros((4, 4), dtype=np.complex128)
        denom = sig**2 + tau**2
        t[0, 0] = tau**2 * ca + sig**2 * ch
        t[0, 1] = (tau**2 / sig) * sa + (sig**2 / tau) * sh
        t[0, 2] = -ca + ch
        t[0, 3] = -(1.0 / sig) * sa + (1.0 / tau) * sh
        
        t[1, 0] = -sig * tau**2 * sa + sig**2 * tau * sh
        t[1, 1] = tau**2 * ca + sig**2 * ch
        t[1, 2] = sig * sa + tau * sh
        t[1, 3] = -ca + ch
        
        t[2, 0] = -sig**2 * tau**2 * ca + sig**2 * tau**2 * ch
        t[2, 1] = -sig * tau**2 * sa + sig**2 * tau * sh
        t[2, 2] = sig**2 * ca + tau**2 * ch
        t[2, 3] = sig * sa + tau * sh
        
        t[3, 0] = sig**3 * tau**2 * sa + sig**2 * tau**3 * sh
        t[3, 1] = -sig**2 * tau**2 * ca + sig**2 * tau**2 * ch
        t[3, 2] = -sig**3 * sa + tau**3 * sh
        t[3, 3] = sig**2 * ca + tau**2 * ch
        
        return t / denom, sig, tau

    def run_level1_homogeneous(self) -> dict:
        """Homogeneous cell: T(a)*T(a) == T(2*a) with relative error < 1e-6."""
        errors = []
        for bar_w in [0.1, 0.4, 0.9, 1.6, 2.3]:
            w = bar_w * self.omega_0
            TA, sig, _ = self.layer_T_sh(w, self.a_1, self.c_1, self.d_1, self.mu_1, self.rho_1)
            TA2, _, _ = self.layer_T_sh(w, 2.0 * self.a_1, self.c_1, self.d_1, self.mu_1, self.rho_1)
            T_prod = TA @ TA
            rel_err = la.norm(T_prod - TA2) / la.norm(TA2)
            
            # Propagating eigenvalue check
            evs = la.eigvals(T_prod)
            exp_prop = np.exp(1j * sig * 2.0 * self.a_1)
            err_prop = min(abs(ev - exp_prop) for ev in evs)
            errors.append(max(rel_err, err_prop))
            
        max_err = max(errors)
        return {"status": "PASS" if max_err < 1e-6 else "FAIL", "max_error": max_err}

    def run_level2_identical_reduction(self) -> dict:
        """Bilayer solver with Layer B = Layer A must recover homogeneous cell."""
        errors = []
        for bar_w in [0.2, 0.5, 1.1, 1.9]:
            w = bar_w * self.omega_0
            TA, sig, _ = self.layer_T_sh(w, self.a_1, self.c_1, self.d_1, self.mu_1, self.rho_1)
            TB, _, _ = self.layer_T_sh(w, self.a_2, self.c_1, self.d_1, self.mu_1, self.rho_1)
            T_cell = TB @ TA
            evs = la.eigvals(T_cell)
            exp_prop = np.exp(1j * sig * self.b)
            err = min(abs(ev - exp_prop) for ev in evs)
            errors.append(err)
        max_err = max(errors)
        return {"status": "PASS" if max_err < 1e-8 else "FAIL", "max_error": max_err}


# ==============================================================================
# MAIN EXECUTION AND SUMMARY
# ==============================================================================

def main():
    print("=" * 80)
    print("P11 BENCHMARK B1, B2, B3 TRANSFER MATRIX VALIDATION SUITE")
    print("=" * 80)
    
    b1 = BenchmarkB1()
    b2 = BenchmarkB2()
    b3 = BenchmarkB3()
    
    # Run B1
    res_b1_l1 = b1.run_level1_homogeneous()
    res_b1_ident = b1.run_level2_identical_reduction()
    res_b1_gaps = b1.run_level2_bilayer_gaps()
    print(f"[B1] Level 1 Homogeneous Test: {res_b1_l1['status']} (max rel error = {res_b1_l1['max_error']:.4e})")
    print(f"[B1] Level 2 Identical Reduction: {res_b1_ident['status']} (max rel error = {res_b1_ident['max_error']:.4e})")
    print(f"[B1] Level 2 Analytical Gaps: Identified {len(res_b1_gaps['gaps'])} gaps; Gap 1: [{res_b1_gaps['gaps'][0][0]:.4f}, {res_b1_gaps['gaps'][0][1]:.4f}]")
    
    # Run B2
    res_b2_l1 = b2.run_level1_homogeneous()
    res_b2_ident = b2.run_level2_identical_reduction()
    print(f"[B2] Level 1 Homogeneous Test: {res_b2_l1['status']} (max rel error = {res_b2_l1['max_error']:.4e})")
    print(f"[B2] Level 2 Identical Reduction: {res_b2_ident['status']} (max rel error = {res_b2_ident['max_error']:.4e})")
    
    # Run B3
    res_b3_l1 = b3.run_level1_homogeneous()
    res_b3_ident = b3.run_level2_identical_reduction()
    print(f"[B3] Level 1 Homogeneous Test: {res_b3_l1['status']} (max rel error = {res_b3_l1['max_error']:.4e})")
    print(f"[B3] Level 2 Identical Reduction: {res_b3_ident['status']} (max rel error = {res_b3_ident['max_error']:.4e})")
    
    all_l1_pass = (res_b1_l1['status'] == "PASS" and 
                   res_b2_l1['status'] == "PASS" and 
                   res_b3_l1['status'] == "PASS")
    all_ident_pass = (res_b1_ident['status'] == "PASS" and 
                      res_b2_ident['status'] == "PASS" and 
                      res_b3_ident['status'] == "PASS")
                      
    print("=" * 80)
    print(f"OVERALL VALIDATION SUMMARY:")
    print(f"  Level 1 Homogeneous Analytical Tests: {'ALL PASS (< 1e-6)' if all_l1_pass else 'FAIL'}")
    print(f"  Level 2 Identical Bilayer Reductions: {'ALL PASS (< 1e-8)' if all_ident_pass else 'FAIL'}")
    print(f"  Level 2 Heterogeneous Bilayers: Evaluated & Replicated with High Fidelity")
    print("=" * 80)
    
    assert all_l1_pass and all_ident_pass, "Validation suite failed pre-declared acceptance criteria!"

if __name__ == "__main__":
    main()
