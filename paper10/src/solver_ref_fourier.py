#!/usr/bin/env python3
"""
paper10/src/solver_ref_fourier.py
=================================
Independent benchmark solver for classical nonlinear Fourier heat conduction:
    rho*c * T_t = d/dx [ lambda_0 (1 + beta_T(T - T_0)) * T_x ]
Dimensionless form:
    T_t = d/dx [ (1 + eps_lambda * T) * T_x ]

Discretisation:
  - Conservative cell-centered Finite Volume Method (FVM).
  - Arithmetic interface conductivities with central flux stencils.
  - Time integration: Radau IIA (5th-order fully implicit Runge-Kutta).
  - Code completely independent of the staggered-grid BDF solver.
"""

import numpy as np
from scipy.integrate import solve_ivp

def q_pulse(t, tau_Delta):
    """Smooth cosine laser pulse excitation."""
    if 0.0 < t <= tau_Delta:
        return 1.0 - np.cos(2.0 * np.pi * t / tau_Delta)
    else:
        return 0.0

def solve_fourier_fvm_ref(Nx=200, eps_lambda=0.0, tau_Delta=0.04, t_eval=None, rtol=1e-10, atol=1e-12):
    """
    Solve the nonlinear Fourier heat equation via conservative FVM and Radau IIA.
    Returns:
        t_eval, T_domain (full temperature field), T_rear (rear face history at x=1)
    """
    if t_eval is None:
        t_eval = np.linspace(0.01, 1.0, 100)
    dx = 1.0 / Nx

    def rhs_fvm(t, T):
        J = np.empty(Nx + 1)
        J[0] = q_pulse(t, tau_Delta) / tau_Delta # heat flux into front face
        J[Nx] = 0.0                             # adiabatic rear face
        
        # Interface conductivities and temperature gradients
        T_inter = 0.5 * (T[:-1] + T[1:])
        k_inter = 1.0 + eps_lambda * T_inter
        dTdx = (T[1:] - T[:-1]) / dx
        J[1:Nx] = -k_inter * dTdx
        
        # Conservative divergence: dT_i/dt = - (J_{i+1} - J_i) / dx
        return (J[:-1] - J[1:]) / dx

    y0 = np.zeros(Nx)
    sol = solve_ivp(rhs_fvm, (0.0, t_eval[-1]), y0, method="Radau", t_eval=t_eval, rtol=rtol, atol=atol)
    
    # 2nd-order rear face temperature extrapolation
    T_rear = 1.5 * sol.y[Nx-1, :] - 0.5 * sol.y[Nx-2, :]
    return t_eval, sol.y, T_rear
