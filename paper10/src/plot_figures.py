#!/usr/bin/env python3
"""
paper10/src/plot_figures.py
===========================
Generates publication-quality figures for Paper 10:
  - Fig01_thermograms.pdf / .png:
      (a) Rear-face temperature history under finite fluence
      (b) Classical Fourier-limit convergence as tau_q -> 0
  - Fig02_sensitivity_colinearity.pdf / .png:
      (a) Linear activation of the null singular value sigma_2 & R_J vs eps_lambda
      (b) Regularisation of the Fisher condition number cond(F) vs eps_lambda
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))
from solver_e1 import solve_e1, solve_e1_fourier_limit
from solver_ref_fourier import solve_fourier_fvm_ref

def generate_figures():
    fig_dir = os.path.join(os.path.dirname(__file__), "../figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    t_eval = np.linspace(0.01, 1.0, 150)
    
    # ------------------------------------------------------------------
    # FIGURE 1: Thermograms and Fourier-Limit Convergence
    # ------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    
    # Panel (a): Thermograms at various eps_lambda
    for eps, col, lbl in [(0.0, "black", r"$\varepsilon_\lambda = 0.0$ (linear)"),
                          (0.01, "#1f77b4", r"$\varepsilon_\lambda = 0.01$ (1%)"),
                          (0.02, "#ff7f0e", r"$\varepsilon_\lambda = 0.02$ (2%)"),
                          (0.05, "#d62728", r"$\varepsilon_\lambda = 0.05$ (5%)")]:
        _, T_e1 = solve_e1(Nx=200, tau_q=0.02, kappa2=0.02, eps_lambda=eps, t_eval=t_eval)
        ax1.plot(t_eval, T_e1, color=col, lw=1.8, label=lbl)
        
    ax1.set_xlabel(r"Dimensionless time $\hat{t} = \alpha t / L^2$", fontsize=11)
    ax1.set_ylabel(r"Rear-face temperature $\hat{T}(1, \hat{t})$", fontsize=11)
    ax1.set_title("(a) Rear-Face Thermograms", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=9, loc="lower right")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.set_xlim([0, 1.0])
    ax1.set_ylim([0, 1.05])
    
    # Panel (b): Convergence to nonlinear Fourier reference as tau_q -> 0
    eps_test = 0.05
    _, _, T_ref = solve_fourier_fvm_ref(Nx=200, eps_lambda=eps_test, t_eval=t_eval)
    for tq, col, ls, lbl in [(0.020, "#d62728", "-", r"$\tau_q = 0.020$ (nominal)"),
                             (0.005, "#2ca02c", "--", r"$\tau_q = 0.005$"),
                             (0.001, "#9467bd", "-.", r"$\tau_q = 0.001$"),
                             (0.000, "black", ":", r"$\tau_q = 0$ (Fourier limit)")]:
        if tq == 0.0:
            _, _, T_curve = solve_e1_fourier_limit(Nx=200, eps_lambda=eps_test, t_eval=t_eval)
        else:
            _, T_curve = solve_e1(Nx=200, tau_q=tq, kappa2=tq, eps_lambda=eps_test, t_eval=t_eval)
        diff = np.abs(T_curve - T_ref)
        ax2.semilogy(t_eval, np.maximum(diff, 1e-12), color=col, linestyle=ls, lw=1.8, label=lbl)
        
    ax2.set_xlabel(r"Dimensionless time $\hat{t} = \alpha t / L^2$", fontsize=11)
    ax2.set_ylabel(r"Residual $|T_{\mathrm{E1}} - T_{\mathrm{ref}}|$", fontsize=11)
    ax2.set_title(r"(b) Fourier-Limit Convergence ($\varepsilon_\lambda = 0.05$)", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=9, loc="upper right")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.set_xlim([0, 1.0])
    ax2.set_ylim([1e-10, 2e-2])
    
    plt.tight_layout()
    fig1_pdf = os.path.join(fig_dir, "Fig01_thermograms.pdf")
    fig1_png = os.path.join(fig_dir, "Fig01_thermograms.png")
    fig.savefig(fig1_pdf)
    fig.savefig(fig1_png)
    plt.close(fig)
    print(f"Generated: {fig1_pdf} and {fig1_png}")
    
    # ------------------------------------------------------------------
    # FIGURE 2: Sensitivity Colinearity Lifting and Fisher Regularisation
    # ------------------------------------------------------------------
    # Read table_01 data
    csv_path = os.path.join(os.path.dirname(__file__), "../runs/final-paper-calculations/table_01_range_study.csv")
    data = np.genfromtxt(csv_path, delimiter=",", names=True)
    
    fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    
    eps_vals = data["eps_lambda"]
    sigma2_vals = data["sigma2"]
    R_J_vals = data["R_J"]
    cond_vals = data["cond_F"]
    
    # Panel (a): Linear activation of sigma2 and R_J vs eps_lambda
    ax3.plot(eps_vals * 100, sigma2_vals, "o-", color="#1f77b4", lw=2, ms=6, label=r"Smallest singular value $\sigma_2$")
    ax3.plot(eps_vals * 100, R_J_vals * 10, "s--", color="#ff7f0e", lw=2, ms=6, label=r"Colinearity deficit $R_J \times 10$")
    ax3.set_xlabel(r"Fluence nonlinearity $\varepsilon_\lambda$ (%)", fontsize=11)
    ax3.set_ylabel(r"Metric magnitude", fontsize=11)
    ax3.set_title("(a) Linear Activation of Parameter Mode", fontsize=12, fontweight="bold")
    ax3.legend(frameon=True, fontsize=9, loc="upper left")
    ax3.grid(True, linestyle=":", alpha=0.6)
    ax3.set_xlim([-0.2, 5.2])
    
    # Panel (b): Fisher condition number vs eps_lambda
    # Filter out eps=0 for log plot
    mask = eps_vals > 0
    ax4.loglog(eps_vals[mask] * 100, cond_vals[mask], "d-", color="#d62728", lw=2, ms=7, label=r"$\mathrm{cond}(F)$ (numerical)")
    # Overlay reference line proportional to eps^-2
    ref_x = np.linspace(0.4, 5.0, 50)
    ref_y = cond_vals[mask][0] * (0.5 / ref_x)**2
    ax4.loglog(ref_x, ref_y, "k--", lw=1.5, alpha=0.7, label=r"$\mathcal{O}(\varepsilon_\lambda^{-2})$ asymptotic scaling")
    
    ax4.set_xlabel(r"Fluence nonlinearity $\varepsilon_\lambda$ (%)", fontsize=11)
    ax4.set_ylabel(r"Fisher Condition Number $\mathrm{cond}(F)$", fontsize=11)
    ax4.set_title("(b) Regularisation of Fisher Singularity", fontsize=12, fontweight="bold")
    ax4.legend(frameon=True, fontsize=9, loc="upper right")
    ax4.grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    fig2_pdf = os.path.join(fig_dir, "Fig02_sensitivity_colinearity.pdf")
    fig2_png = os.path.join(fig_dir, "Fig02_sensitivity_colinearity.png")
    fig.savefig(fig2_pdf)
    fig.savefig(fig2_png)
    plt.close(fig)
    print(f"Generated: {fig2_pdf} and {fig2_png}")

if __name__ == "__main__":
    generate_figures()
