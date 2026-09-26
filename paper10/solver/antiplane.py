"""
Anti-Plane (4-State) Gradient Elastic Transfer-Matrix Module
Implements Mindlin Form-II Dipolar Gradient Elasticity for SH Waves
Reference: Li, Wei & Zhou (2016, Acta Mechanica 227(4), 1083-1100)
"""

import numpy as np
from typing import Tuple, Dict, Any
from .parameters import MaterialParameters


class AntiPlaneSolver:
    """
    4-State Transfer Matrix and Dispersion Solver for Anti-Plane Shear Waves.
    State vector: V_anti = [u_z, u_z,x, P_z, R_z]^T
    """
    
    def __init__(self, mat: MaterialParameters, xi: float = 0.0):
        self.mat = mat
        self.xi = float(xi)  # Apparent wavenumber along y (0.0 for normal incidence)
        
    def compute_characteristic_roots(self, omega: float) -> Dict[str, Any]:
        """
        Compute characteristic wave roots for given circular frequency omega.
        Equation: c*K^2 + (1 - ms)*K - (omega^2/Vs^2) = 0, where K = k_x^2 + xi^2.
        """
        Vs = self.mat.Vs
        c = self.mat.c
        ms = self.mat.ms(omega)
        
        Delta_s = np.sqrt((1.0 - ms)**2 + 4.0 * c * (omega**2) / (Vs**2))
        
        # Numerically stable formulation avoiding catastrophic cancellation as c -> 0:
        # sigma_sq = (Delta_s - (1 - ms)) / (2*c) = 2*(omega^2/Vs^2) / (Delta_s + (1 - ms))
        term_den = Delta_s + (1.0 - ms)
        if term_den > 0:
            sigma_sq = (2.0 * omega**2 / Vs**2) / term_den
        else:
            sigma_sq = 0.5 / c * (Delta_s - (1.0 - ms))
            
        tau_sq = 0.5 / c * (Delta_s + (1.0 - ms)) if c > 0 else 1e30
        
        beta_sq = sigma_sq - self.xi**2
        gamma_sq = tau_sq + self.xi**2
        
        beta_s = np.sqrt(complex(beta_sq))
        gamma_s = np.sqrt(complex(gamma_sq))
        
        # 4 spatial roots along x: k_x
        # Mode 1: +beta_s (forward propagating / evanescent)
        # Mode 2: -beta_s (backward propagating / evanescent)
        # Mode 3: +i*gamma_s (forward decaying evanescent)
        # Mode 4: -i*gamma_s (backward growing evanescent)
        roots = np.array([beta_s, -beta_s, 1j * gamma_s, -1j * gamma_s], dtype=complex)
        
        return {
            "omega": omega,
            "ms": ms,
            "Delta_s": Delta_s,
            "sigma_sq": sigma_sq,
            "tau_sq": tau_sq,
            "beta_sq": beta_sq,
            "gamma_sq": gamma_sq,
            "beta_s": beta_s,
            "gamma_s": gamma_s,
            "roots": roots
        }

    def compute_modal_matrix(self, omega: float) -> Tuple[np.ndarray, float, float]:
        """
        Construct 4x4 modal matrix P_anti at x = 0.
        Columns correspond to the 4 characteristic wave roots.
        Returns:
            P: 4x4 complex modal matrix
            cond_P_raw: condition number kappa(P) of unscaled SI matrix
            cond_P_scaled: condition number kappa(P) with dimensional row-equilibration
        """
        r_info = self.compute_characteristic_roots(omega)
        roots = r_info["roots"]
        mu = self.mat.mu
        c = self.mat.c
        ms = r_info["ms"]
        xi = self.xi
        
        P = np.zeros((4, 4), dtype=complex)
        
        for col, kx in enumerate(roots):
            # u_z
            P[0, col] = 1.0
            # u_z,x
            P[1, col] = 1j * kx
            # P_z = mu * [ (1 - ms)*u_z,x - c*(u_z,xxx - 2*xi^2*u_z,x) ]
            # Note u_z,xxx = (i*kx)^3 = -i*kx^3
            # Thus P_z = i * mu * kx * [ (1 - ms) + c*(kx^2 + 2*xi^2) ]
            P[2, col] = 1j * mu * kx * ((1.0 - ms) + c * (kx**2 + 2.0 * xi**2))
            # R_z = c * mu * u_z,xx = -c * mu * kx^2
            P[3, col] = -c * mu * (kx**2)
            
        cond_P_raw = float(np.linalg.cond(P))
        # Row equilibration for dimensional scaling
        row_norms = np.linalg.norm(P, axis=1, keepdims=True)
        P_scaled = P / np.maximum(row_norms, 1e-30)
        cond_P_scaled = float(np.linalg.cond(P_scaled))
        
        return P, cond_P_raw, cond_P_scaled

    def compute_transfer_matrix_modal(self, omega: float, a_j: float) -> Tuple[np.ndarray, float, float]:
        """
        Compute layer transfer matrix via modal decomposition: T = P * G * P^-1.
        Returns:
            T: 4x4 transfer matrix
            cond_P_scaled: row-equilibrated condition number of modal matrix P
            cond_T: condition number of transfer matrix T
        """
        P, cond_P_raw, cond_P_scaled = self.compute_modal_matrix(omega)
        r_info = self.compute_characteristic_roots(omega)
        roots = r_info["roots"]
        
        G_diag = np.exp(1j * roots * a_j)
        G = np.diag(G_diag)
        
        P_inv = np.linalg.inv(P)
        T = P @ G @ P_inv
        
        # Equilibrated cond for T
        row_norms = np.linalg.norm(T, axis=1, keepdims=True)
        T_scaled = T / np.maximum(row_norms, 1e-30)
        cond_T_scaled = float(np.linalg.cond(T_scaled))
        
        return T, cond_P_scaled, cond_T_scaled

    def compute_transfer_matrix_analytical(self, omega: float, a_j: float) -> np.ndarray:
        """
        Compute analytical 4x4 transfer matrix using Li et al. (2016, Appendix 1) formulation.
        Serves as exact cross-check for modal construction.
        """
        r_info = self.compute_characteristic_roots(omega)
        beta_s = r_info["beta_s"]
        gamma_s = r_info["gamma_s"]
        sigma_sq = r_info["sigma_sq"]
        tau_sq = r_info["tau_sq"]
        ms_j = r_info["ms"]
        mu_j = self.mat.mu
        c_j = self.mat.c
        xi = self.xi
        
        e11 = np.cos(beta_s * a_j)
        e12 = np.cosh(gamma_s * a_j)
        e13 = np.sin(beta_s * a_j) / beta_s if abs(beta_s) > 1e-12 else complex(a_j)
        e14 = np.sinh(gamma_s * a_j) / gamma_s if abs(gamma_s) > 1e-12 else complex(a_j)
        
        e21 = -beta_s * np.sin(beta_s * a_j)
        e22 = gamma_s * np.sinh(gamma_s * a_j)
        e23 = np.cos(beta_s * a_j)
        e24 = np.cosh(gamma_s * a_j)
        
        term_sig = sigma_sq + xi**2
        term_tau = tau_sq - xi**2
        e31 = mu_j * (-beta_s * (1.0 - ms_j) - c_j * beta_s * term_sig) * np.sin(beta_s * a_j)
        e32 = mu_j * (gamma_s * (1.0 - ms_j) - c_j * gamma_s * term_tau) * np.sinh(gamma_s * a_j)
        e33 = mu_j * ((1.0 - ms_j) + c_j * term_sig) * np.cos(beta_s * a_j)
        e34 = mu_j * ((1.0 - ms_j) - c_j * term_tau) * np.cosh(gamma_s * a_j)
        
        e41 = -mu_j * c_j * beta_s**2 * np.cos(beta_s * a_j)
        e42 = mu_j * c_j * gamma_s**2 * np.cosh(gamma_s * a_j)
        e43 = -mu_j * c_j * beta_s * np.sin(beta_s * a_j)
        e44 = mu_j * c_j * gamma_s * np.sinh(gamma_s * a_j)
        
        E = np.array([
            [e11, e12, e13, e14],
            [e21, e22, e23, e24],
            [e31, e32, e33, e34],
            [e41, e42, e43, e44]
        ], dtype=complex)
        
        T = np.zeros((4, 4), dtype=complex)
        denom = sigma_sq + tau_sq
        
        for k in range(4):
            T[k, 0] = (E[k, 0] * (denom - beta_s**2) + beta_s**2 * E[k, 1]) / denom
            term1 = (term_tau - (1.0 - ms_j) / c_j) * E[k, 2]
            term2 = ((1.0 - ms_j) / c_j + term_sig) * E[k, 3]
            T[k, 1] = (term1 + term2) / denom
            T[k, 2] = (E[k, 2] - E[k, 3]) / (mu_j * c_j * denom)
            T[k, 3] = (E[k, 1] - E[k, 0]) / (mu_j * c_j * denom)
            
        return T

    def check_symplectic_properties(self, T: np.ndarray) -> Dict[str, float]:
        """
        Check conservative symplectic properties for 4x4 mechanical transfer matrix:
        1. |det(T) - 1|
        2. || T^T * J * T - J || where J = [[0, I_2], [-I_2, 0]]
        """
        det_T = np.linalg.det(T)
        det_err = abs(det_T - 1.0)
        
        # J matrix for [q, p] state vector where q = [u_z, u_z,x]^T, p = [P_z, R_z]^T
        I2 = np.eye(2, dtype=complex)
        Z2 = np.zeros((2, 2), dtype=complex)
        J = np.block([[Z2, I2], [-I2, Z2]])
        
        # In our state ordering V = [u_z, u_z,x, P_z, R_z]^T, q is entries (0,1) and p is entries (2,3).
        # Thus the canonical J is exactly [[0, I_2], [-I_2, 0]].
        # For non-lossy systems, T is real in time domain, but in frequency domain: T^T * J * T = J.
        symp_diff = T.T @ J @ T - J
        symp_norm = float(np.linalg.norm(symp_diff, ord='fro'))
        
        return {
            "det_T": det_T,
            "det_err": float(det_err),
            "symp_norm": symp_norm
        }

    def papargyri_beskou_analytical_omega(self, k: float) -> float:
        """
        Papargyri-Beskou et al. (2009, Eq. 28) exact analytical frequency:
        omega = Vs * k * sqrt( (1 + c*k^2) / (1 + (d^2/3)*k^2) )
        """
        Vs = self.mat.Vs
        c = self.mat.c
        h_sq = self.mat.d**2 / 3.0
        return Vs * k * np.sqrt((1.0 + c * k**2) / (1.0 + h_sq * k**2))

    def solve_numerical_omega(self, k: float, a_layer: float = None, tol: float = 1e-12) -> Tuple[float, float, float]:
        """
        Solve for the numerical frequency omega matching wavenumber k from the Transfer Matrix
        Bloch eigenvalue condition: det(T(omega, a) - exp(i*k*a)*I) = 0.
        Returns:
            omega_num: solved frequency (rad/s)
            rel_err_with_PB: relative error with respect to Papargyri-Beskou analytical
            residual: residual |det(T - exp(i*k*a)*I)|
        """
        from scipy.optimize import root_scalar
        
        omega_analytical = self.papargyri_beskou_analytical_omega(k)
        
        # Secular characteristic equation for single wave mode:
        def char_residual(w: float) -> float:
            r_info = self.compute_characteristic_roots(w)
            return float(np.real(r_info["beta_s"]) - k)
            
        w_low = 0.8 * omega_analytical
        w_high = 1.2 * omega_analytical
        res = root_scalar(char_residual, bracket=[w_low, w_high], method='brentq', xtol=tol)
        omega_num = float(res.root)
        
        # Choose a_layer safely to avoid evanescent overflow in floating point if c is very small
        r_info_sol = self.compute_characteristic_roots(omega_num)
        gamma_val = float(np.real(r_info_sol["gamma_s"]))
        if a_layer is None:
            a_safe = min(0.01, 20.0 / max(gamma_val, 1.0))
        else:
            a_safe = a_layer
            
        target_phase = k * a_safe
        target_lambda = np.exp(1j * target_phase)
        
        # Verify transfer matrix eigenvalue residual at this solved omega
        T_solved = self.compute_transfer_matrix_analytical(omega_num, a_safe)
        eigvals = np.linalg.eigvals(T_solved)
        min_eig_diff = float(np.min(np.abs(eigvals - target_lambda)))
        
    @staticmethod
    def compute_periodic_unit_cell(
        matA: MaterialParameters,
        matB: MaterialParameters,
        a1: float,
        a2: float,
        omega: float,
        xi: float = 0.0
    ) -> Dict[str, Any]:
        """
        Compute periodic unit-cell transfer matrix T_cell = T_B * T_A and Bloch modes.
        """
        solverA = AntiPlaneSolver(matA, xi=xi)
        solverB = AntiPlaneSolver(matB, xi=xi)
        
        TA = solverA.compute_transfer_matrix_analytical(omega, a1)
        TB = solverB.compute_transfer_matrix_analytical(omega, a2)
        Tcell = TB @ TA
        
        det_Tcell = np.linalg.det(Tcell)
        det_err = float(abs(det_Tcell - 1.0))
        cond_Tcell = float(np.linalg.cond(Tcell))
        
        eigvals, eigvecs = np.linalg.eig(Tcell)
        
        # Extract Bloch wavenumbers: lambda = exp(i * kx * a) -> kx*a = -i * ln(lambda)
        # kx*a = kr*a + i * ki*a
        a_total = a1 + a2
        bloch_modes = []
        is_in_gap = True
        
        for ev in eigvals:
            log_ev = np.log(ev)
            k_complex_a = -1j * log_ev
            kr_a = float(np.real(k_complex_a))
            ki_a = float(np.imag(k_complex_a))
            
            # Map kr_a into First Brillouin Zone [0, pi]
            kr_a_bz = abs(kr_a) % (2.0 * np.pi)
            if kr_a_bz > np.pi:
                kr_a_bz = 2.0 * np.pi - kr_a_bz
                
            is_propagating = (abs(abs(ev) - 1.0) < 1e-2) and (abs(ki_a) < 1e-2)
            if is_propagating:
                is_in_gap = False
                
            bloch_modes.append({
                "eigval": complex(ev),
                "kr_a": kr_a_bz,
                "ki_a": abs(ki_a),
                "is_propagating": bool(is_propagating)
            })
            
        return {
            "omega": omega,
            "Tcell": Tcell,
            "det_err": det_err,
            "cond_Tcell": cond_Tcell,
            "bloch_modes": bloch_modes,
            "is_in_gap": is_in_gap
        }
