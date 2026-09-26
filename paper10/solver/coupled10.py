"""
Full 10-State Coupled DPL-Dipolar Gradient Elastic Transfer-Matrix Module
Implements Mindlin Form-II Gradient Elasticity coupled with Tzou Dual-Phase-Lag Heat Conduction.
State vector: V_in = [u_x, u_y, u_x,x, u_y,x, theta, P_x, P_y, R_x, R_y, q_x]^T
"""

import numpy as np
from typing import Tuple, Dict, Any, List
from .parameters import MaterialParameters


class Coupled10StateSolver:
    """
    10-State Transfer Matrix and Bloch Dispersion Solver for Coupled DPL Thermoelasticity
    with Dipolar Gradient Elasticity.
    """
    
    def __init__(self, mat: MaterialParameters, xi: float = 0.0):
        self.mat = mat
        self.xi = float(xi)  # Apparent wavenumber along y
        
    def compute_characteristic_roots(self, omega: float) -> Dict[str, Any]:
        """
        Compute all 10 spatial characteristic wave roots along the x-axis:
        - 4 Transverse shear roots (uncoupled from dilatation)
        - 6 Coupled longitudinal-thermal roots (from cubic polynomial in K = k_x^2 + xi^2)
        """
        Vs = self.mat.Vs
        Vp = self.mat.Vp
        c = self.mat.c
        d = self.mat.d
        rho = self.mat.rho
        cv = self.mat.cv
        beta = self.mat.beta
        T0 = self.mat.T0
        xi = self.xi
        
        # 1. Shear sector (4 roots)
        ms = self.mat.ms(omega)
        Delta_s = np.sqrt((1.0 - ms)**2 + 4.0 * c * (omega**2) / (Vs**2))
        
        term_den = Delta_s + (1.0 - ms)
        if term_den > 0:
            sigma_sq = (2.0 * omega**2 / Vs**2) / term_den
        else:
            sigma_sq = 0.5 / c * (Delta_s - (1.0 - ms))
        tau_sq = 0.5 / c * (Delta_s + (1.0 - ms))
        
        beta_sq = sigma_sq - xi**2
        gamma_sq = tau_sq + xi**2
        beta_s = np.sqrt(complex(beta_sq))
        gamma_s = np.sqrt(complex(gamma_sq))
        
        shear_kx = np.array([beta_s, -beta_s, 1j * gamma_s, -1j * gamma_s], dtype=complex)
        
        # 2. Longitudinal-thermal sector (6 roots)
        mp = self.mat.mp(omega)
        keff = self.mat.k_eff(omega)
        kth_sq = self.mat.kth_sq(omega)
        eta_th = self.mat.eta_th(omega)
        
        lambda_2mu = self.mat.lambda_param + 2.0 * self.mat.mu
        eps_th = (T0 * beta**2) / (rho * cv * lambda_2mu) if (rho * cv * lambda_2mu) > 0 else 0.0
        
        # Cubic coefficients for K = k_x^2 + xi^2: K^3 + A2*K^2 + A1*K + A0 = 0
        A2 = (1.0 - mp) / c - kth_sq
        A1 = - (omega**2) / (c * Vp**2) - ((1.0 - mp) * kth_sq) / c + (eps_th * kth_sq) / c
        A0 = (omega**2 * kth_sq) / (c * Vp**2)
        
        poly_coeffs = [1.0, A2, A1, A0]
        K_roots = np.roots(poly_coeffs)
        
        long_modes = []
        for K_val in K_roots:
            kx_pos = np.sqrt(complex(K_val - xi**2))
            kx_neg = -kx_pos
            den_zeta = kth_sq - K_val
            if abs(den_zeta) < 1e-15:
                zeta = complex(1e15)
            else:
                zeta = (eta_th * K_val) / den_zeta
                
            long_modes.append((kx_pos, zeta))
            long_modes.append((kx_neg, zeta))
            
        long_kx = np.array([m[0] for m in long_modes], dtype=complex)
        zeta_ratios = np.array([m[1] for m in long_modes], dtype=complex)
        all_roots = np.concatenate([long_kx, shear_kx])
        
        return {
            "omega": omega,
            "shear_roots": shear_kx,
            "long_roots": long_kx,
            "zeta_ratios": zeta_ratios,
            "long_modes": long_modes,
            "all_roots": all_roots,
            "K_roots": K_roots,
            "kth_sq": kth_sq,
            "keff": keff,
            "eta_th": eta_th
        }

    def _evaluate_state_vector(self, Ux: complex, Uy: complex, Theta: complex, kx: complex, omega: float, keff: complex) -> np.ndarray:
        """
        Evaluate full 10-component state vector from constitutive relations:
        V = [u_x, u_y, u_x,x, u_y,x, theta, P_x, P_y, R_x, R_y, q_x]^T
        """
        mu = self.mat.mu
        lam = self.mat.lambda_param
        lam_2mu = lam + 2.0 * mu
        c = self.mat.c
        d = self.mat.d
        rho = self.mat.rho
        beta = self.mat.beta
        xi = self.xi
        
        ux = Ux
        uy = Uy
        uxx = 1j * kx * Ux
        uyx = 1j * kx * Uy
        th = Theta
        
        # Generalized monopolar traction P_x
        term_px_x = 1j * kx * (lam_2mu * (1.0 + c * (kx**2 + 2.0 * xi**2)) - (1.0 / 3.0) * rho * (d**2) * (omega**2)) * Ux
        term_px_y = 1j * xi * (lam * (1.0 + c * xi**2)) * Uy
        Px = term_px_x + term_px_y - beta * Theta
        
        # Generalized monopolar traction P_y
        term_py_x = 1j * xi * (mu + c * lam * (xi**2)) * Ux
        term_py_y = 1j * kx * (mu * (1.0 + c * (kx**2 + 2.0 * xi**2)) - (1.0 / 3.0) * rho * (d**2) * (omega**2)) * Uy
        Py = term_py_x + term_py_y
        
        # Generalized dipolar hyperstress R_x
        Rx = -c * lam_2mu * (kx**2) * Ux - c * lam * kx * xi * Uy
        
        # Generalized dipolar hyperstress R_y
        Ry = -c * mu * kx * xi * Ux - c * mu * (kx**2) * Uy
        
        # Conductive heat flux q_x
        qx = -1j * keff * kx * Theta
        
        return np.array([ux, uy, uxx, uyx, th, Px, Py, Rx, Ry, qx], dtype=complex)

    def compute_modal_matrix(self, omega: float) -> Tuple[np.ndarray, float, float]:
        """
        Construct 10x10 modal matrix P_in at x = 0.
        First 6 columns: Longitudinal-thermal modes (derived from scalar potential Phi)
        Last 4 columns: Transverse shear modes (derived from vector potential Psi)
        Returns:
            P: 10x10 modal matrix
            cond_P_raw: unscaled condition number
            cond_P_equil: row- and column-equilibrated condition number
        """
        r_info = self.compute_characteristic_roots(omega)
        long_modes = r_info["long_modes"]
        shear_kx = r_info["shear_roots"]
        keff = r_info["keff"]
        xi = self.xi
        
        P = np.zeros((10, 10), dtype=complex)
        
        # --- Columns 0 to 5: Longitudinal-thermal modes (Phi = 1, Psi = 0) ---
        for col, (kx, zeta) in enumerate(long_modes):
            Ux = 1j * kx
            Uy = 1j * xi
            Theta = zeta
            P[:, col] = self._evaluate_state_vector(Ux, Uy, Theta, kx, omega, keff)
            
        # --- Columns 6 to 9: Transverse shear modes (Phi = 0, Psi = 1) ---
        for idx, kx in enumerate(shear_kx):
            col = 6 + idx
            Ux = 1j * xi
            Uy = -1j * kx
            Theta = 0.0
            P[:, col] = self._evaluate_state_vector(Ux, Uy, Theta, kx, omega, keff)
            
        cond_P_raw = float(np.linalg.cond(P))
        
        # Canonical equilibration: Row scaling then Column scaling
        row_norms = np.maximum(np.linalg.norm(P, axis=1, keepdims=True), 1e-30)
        P_r = P / row_norms
        col_norms = np.maximum(np.linalg.norm(P_r, axis=0, keepdims=True), 1e-30)
        P_equil = P_r / col_norms
        cond_P_equil = float(np.linalg.cond(P_equil))
        
        return P, cond_P_raw, cond_P_equil

    def compute_transfer_matrix(self, omega: float, a_j: float) -> Tuple[np.ndarray, float, float]:
        """
        Compute 10x10 layer transfer matrix T = P * G * P^-1.
        """
        P, cond_P_raw, cond_P_equil = self.compute_modal_matrix(omega)
        r_info = self.compute_characteristic_roots(omega)
        all_roots = r_info["all_roots"]
        
        G_diag = np.exp(1j * all_roots * a_j)
        G = np.diag(G_diag)
        
        # Inversion using balanced row-column scaling
        row_norms = np.maximum(np.linalg.norm(P, axis=1, keepdims=True), 1e-30)
        P_r = P / row_norms
        col_norms = np.maximum(np.linalg.norm(P_r, axis=0, keepdims=True), 1e-30)
        P_equil = P_r / col_norms
        
        # P = diag(row_norms) @ P_equil @ diag(col_norms)
        # P^-1 = diag(1/col_norms) @ P_equil^-1 @ diag(1/row_norms)
        P_eq_inv = np.linalg.inv(P_equil)
        D_col_inv = np.diag(1.0 / col_norms.ravel())
        D_row_inv = np.diag(1.0 / row_norms.ravel())
        P_inv = D_col_inv @ P_eq_inv @ D_row_inv
        
        T = P @ G @ P_inv
        
        # Equilibrated cond for T
        row_norms_T = np.maximum(np.linalg.norm(T, axis=1, keepdims=True), 1e-30)
        T_r = T / row_norms_T
        col_norms_T = np.maximum(np.linalg.norm(T_r, axis=0, keepdims=True), 1e-30)
        cond_T_equil = float(np.linalg.cond(T_r / col_norms_T))
        
        return T, cond_P_equil, cond_T_equil
        
    @staticmethod
    def compute_periodic_unit_cell_10(
        matA: MaterialParameters,
        matB: MaterialParameters,
        a1: float,
        a2: float,
        omega: float,
        xi: float = 0.0
    ) -> Dict[str, Any]:
        """
        Compute full 10x10 periodic unit-cell transfer matrix T_cell = T_B * T_A and Bloch eigenvalues.
        """
        solverA = Coupled10StateSolver(matA, xi=xi)
        solverB = Coupled10StateSolver(matB, xi=xi)
        
        TA, cond_PA, cond_TA = solverA.compute_transfer_matrix(omega, a1)
        TB, cond_PB, cond_TB = solverB.compute_transfer_matrix(omega, a2)
        Tcell = TB @ TA
        
        det_Tcell = np.linalg.det(Tcell)
        
        # Equilibrated cond
        r_T = np.maximum(np.linalg.norm(Tcell, axis=1, keepdims=True), 1e-30)
        Tc_r = Tcell / r_T
        c_T = np.maximum(np.linalg.norm(Tc_r, axis=0, keepdims=True), 1e-30)
        cond_Tcell = float(np.linalg.cond(Tc_r / c_T))
        
        eigvals, eigvecs = np.linalg.eig(Tcell)
        
        bloch_modes = []
        for ev in eigvals:
            log_ev = np.log(ev)
            k_complex_a = -1j * log_ev
            kr_a = float(np.real(k_complex_a))
            ki_a = float(np.imag(k_complex_a))
            
            kr_a_bz = abs(kr_a) % (2.0 * np.pi)
            if kr_a_bz > np.pi:
                kr_a_bz = 2.0 * np.pi - kr_a_bz
                
            bloch_modes.append({
                "eigval": complex(ev),
                "kr_a": kr_a_bz,
                "ki_a": abs(ki_a)
            })
            
        return {
            "omega": omega,
            "Tcell": Tcell,
            "det_Tcell": complex(det_Tcell),
            "cond_Tcell": cond_Tcell,
            "bloch_modes": bloch_modes
        }
