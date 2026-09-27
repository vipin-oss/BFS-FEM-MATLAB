#!/usr/bin/env python3
"""
paper10/src/solver_e1.py
========================
Core forward solver for Extension E1: Finite-Fluence Nonlinear Guyer-Krumhansl
heat conduction.

Discretisation:
  - Staggered grid: Cell-centered temperatures T_i (i=0..Nx-1),
    cell-face heat fluxes q_{j+1/2} (j=0..Nx).
  - Spatial derivatives: 2nd-order centered differences.
  - Time integration: Stiff BDF (Backward Differentiation Formula).
"""

import numpy as np
from scipy.integrate import solve_ivp

def q_pulse(t, tau_Delta):
    """Smooth cosine laser pulse excitation."""
    if 0.0 < t <= tau_Delta:
        return 1.0 - np.cos(2.0 * np.pi * t / tau_Delta)
    else:
        return 0.0

def solve_e1(Nx=200, tau_q=0.02, kappa2=0.02, eps_lambda=0.0, tau_Delta=0.04, t_eval=None, rtol=1e-11, atol=1e-13):
    """
    Solve the full E1 model with finite relaxation and nonlocality.
    Returns:
        t_eval, T_rear (rear face temperature history at x=1)
    """
    if t_eval is None:
        t_eval = np.linspace(0.01, 1.0, 100)
    dx = 1.0 / Nx

    def rhs(t, y):
        T = y[:Nx]
        q_int = y[Nx:]
        q0 = q_pulse(t, tau_Delta)
        q = np.empty(Nx + 1)
        q[0] = q0
        q[1:Nx] = q_int
        q[Nx] = 0.0 # adiabatic rear face
        
        # Energy balance at cell centers
        dTdt = -(q[1:] - q[:-1]) / (tau_Delta * dx)
        
        # Constitutive flux equation at interior cell faces
        T_face = 0.5 * (T[:-1] + T[1:])
        dTdx = (T[1:] - T[:-1]) / dx
        d2qdx2 = (q[2:] - 2.0 * q[1:Nx] + q[:-2]) / (dx**2)
        
        dqdt = (-q_int - tau_Delta * (1.0 + eps_lambda * T_face) * dTdx + kappa2 * d2qdx2) / tau_q
        return np.concatenate([dTdt, dqdt])

    y0 = np.zeros(2 * Nx - 1)
    sol = solve_ivp(rhs, (0.0, t_eval[-1]), y0, method="BDF", t_eval=t_eval, rtol=rtol, atol=atol)
    
    # 2nd-order rear-face temperature extrapolation to x=1
    T_rear = 1.5 * sol.y[Nx-1, :] - 0.5 * sol.y[Nx-2, :]
    return t_eval, T_rear

def solve_e1_fourier_limit(Nx=200, eps_lambda=0.0, tau_Delta=0.04, t_eval=None, rtol=1e-10, atol=1e-12):
    """
    Solve the E1 model in the singular limit tau_q -> 0, kappa^2 -> 0.
    In this limit, the flux equation reduces to:
        q = -tau_Delta * (1 + eps_lambda * T) * dT/dx
    """
    if t_eval is None:
        t_eval = np.linspace(0.01, 1.0, 100)
    dx = 1.0 / Nx

    def rhs(t, T):
        q = np.empty(Nx + 1)
        q[0] = q_pulse(t, tau_Delta)
        q[Nx] = 0.0
        T_face = 0.5 * (T[:-1] + T[1:])
        dTdx = (T[1:] - T[:-1]) / dx
        q[1:Nx] = -tau_Delta * (1.0 + eps_lambda * T_face) * dTdx
        dTdt = -(q[1:] - q[:-1]) / (tau_Delta * dx)
        return dTdt

    y0 = np.zeros(Nx)
    sol = solve_ivp(rhs, (0.0, t_eval[-1]), y0, method="BDF", t_eval=t_eval, rtol=rtol, atol=atol)
    T_rear = 1.5 * sol.y[Nx-1, :] - 0.5 * sol.y[Nx-2, :]
    return t_eval, sol.y, T_rear
