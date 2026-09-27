"""
plot_figures.py - Generates Publication-Ready Figures for Paper 11
Part of the Paper 11 Research Package.

Outputs both vector PDF and 300-DPI PNG formats to:
  - paper11/figures/
  - paper11/overleaf/figures/
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Use publication-style matplotlib configuration
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 13,
    "lines.linewidth": 1.8,
    "lines.markersize": 6,
    "grid.alpha": 0.4,
    "grid.linestyle": "--"
})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, "figures")
OVERLEAF_FIG_DIR = os.path.join(BASE_DIR, "overleaf", "figures")
DATA_DIR = os.path.join(BASE_DIR, "runs", "calculations")

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(OVERLEAF_FIG_DIR, exist_ok=True)

def save_fig(fig, base_name):
    for d in [FIG_DIR, OVERLEAF_FIG_DIR]:
        pdf_path = os.path.join(d, f"{base_name}.pdf")
        png_path = os.path.join(d, f"{base_name}.png")
        fig.savefig(pdf_path, bbox_inches="tight", format="pdf")
        fig.savefig(png_path, bbox_inches="tight", dpi=300, format="png")
    print(f"  Saved {base_name}.pdf and {base_name}.png")

def plot_fig1():
    print("Generating Figure 1: Temperature Response and Heat Loss Tails...")
    df_prof = pd.read_csv(os.path.join(DATA_DIR, "sensitivity_profiles.csv"))
    df_lap = pd.read_csv(os.path.join(DATA_DIR, "validation_laplace.csv"))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    # Subplot (a): Temperature histories
    ax = axes[0]
    time = df_prof["time"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    bi_tags = [("Bi_0p00", "Bi = 0.00 (Adiabatic)", colors[0]),
               ("Bi_0p05", "Bi = 0.05", colors[1]),
               ("Bi_0p20", "Bi = 0.20", colors[2])]

    for tag, label, c in bi_tags:
        ax.plot(time, df_prof[f"T_{tag}"], label=f"GK ({label})", color=c, lw=2.0)

    ax.set_xlabel(r"Dimensionless Time, $t$")
    ax.set_ylabel(r"Rear-Face Temperature, $T(1, t)$")
    ax.set_title(r"(a) Rear-Face Thermal Response across Biot Numbers")
    ax.legend(loc="lower right", framealpha=0.95)
    ax.grid(True)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.05)

    # Subplot (b): Exact analytical difference between GK (B=1) and Fourier
    ax = axes[1]
    df_cowan = pd.read_csv(os.path.join(DATA_DIR, "validation_cowan.csv"))
    ax.semilogy(df_cowan["Bi"], df_cowan["L_inf_error"], "s-", color="#d62728", lw=2.0, label=r"$L_\infty$ Error vs Cowan Fourier limit")
    ax.semilogy(df_cowan["Bi"], df_cowan["L_2_error"], "o--", color="#9467bd", lw=2.0, label=r"$L_2$ Error vs Cowan Fourier limit")
    ax.set_xlabel(r"Biot Number, $\mathrm{Bi}$")
    ax.set_ylabel(r"Numerical Discrepancy, $\Delta T$")
    ax.set_title(r"(b) Absolute Identity with Cowan (1963) Fourier Solution")
    ax.legend(loc="upper right", framealpha=0.95)
    ax.grid(True)
    ax.set_ylim(1e-7, 1e-4)

    plt.tight_layout()
    save_fig(fig, "fig1_heatloss_temperature_response")
    plt.close(fig)

def plot_fig2():
    print("Generating Figure 2: Sensitivity Profiles & Collinearity...")
    df_prof = pd.read_csv(os.path.join(DATA_DIR, "sensitivity_profiles.csv"))
    time = df_prof["time"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    # Subplot (a): Exact overlay of J_tau_q and -alpha*J_kappa2
    ax = axes[0]
    ax.plot(time, df_prof["J_tau_q_Bi_0p00"], "-", color="#1f77b4", lw=2.2, label=r"$J_{\tau_q}$ ($Bi = 0.0$)")
    ax.plot(time, -df_prof["J_kappa2_Bi_0p00"], "--", color="#1f77b4", lw=2.2, dashes=(4, 3), label=r"$-\alpha_0 J_{\kappa^2}$ ($Bi = 0.0$)")

    ax.plot(time, df_prof["J_tau_q_Bi_0p20"], "-", color="#d62728", lw=2.2, label=r"$J_{\tau_q}$ ($Bi = 0.2$)")
    ax.plot(time, -df_prof["J_kappa2_Bi_0p20"], "--", color="#d62728", lw=2.2, dashes=(4, 3), label=r"$-\alpha_0 J_{\kappa^2}$ ($Bi = 0.2$)")

    ax.set_xlabel(r"Dimensionless Time, $t$")
    ax.set_ylabel(r"Sensitivity Amplitude")
    ax.set_title(r"(a) Exact Sensitivity Collinearity: $J_{\tau_q}(t) \equiv -\alpha_0 J_{\kappa^2}(t)$")
    ax.legend(loc="upper right", framealpha=0.95, ncol=2)
    ax.grid(True)
    ax.set_xlim(0, 1.0)

    # Subplot (b): Sensitivity with respect to Biot number J_Bi
    ax = axes[1]
    ax.plot(time, df_prof["J_Bi_Bi_0p05"], "-", color="#ff7f0e", lw=2.0, label=r"$J_{\mathrm{Bi}}$ ($Bi = 0.05$)")
    ax.plot(time, df_prof["J_Bi_Bi_0p20"], "-", color="#2ca02c", lw=2.0, label=r"$J_{\mathrm{Bi}}$ ($Bi = 0.20$)")
    ax.axhline(0, color="gray", lw=0.8, ls=":")

    ax.set_xlabel(r"Dimensionless Time, $t$")
    ax.set_ylabel(r"Heat Loss Sensitivity, $J_{\mathrm{Bi}} = \partial T / \partial \mathrm{Bi}$")
    ax.set_title(r"(b) Independent Cooling Tail Sensitivity Profile")
    ax.legend(loc="lower left", framealpha=0.95)
    ax.grid(True)
    ax.set_xlim(0, 1.0)

    plt.tight_layout()
    save_fig(fig, "fig2_sensitivity_profiles_collinearity")
    plt.close(fig)

def plot_fig3():
    print("Generating Figure 3: Invariance Metrics Across Biot Numbers...")
    df_sweep = pd.read_csv(os.path.join(DATA_DIR, "heatloss_parameter_sweep.csv"))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    # Subplot (a): Collinearity metrics
    ax = axes[0]
    bi = df_sweep["Bi"]
    rj = df_sweep["R_J"]
    # Treat 1+rho: take absolute or clip to eps
    one_plus_rho_abs = np.maximum(np.abs(df_sweep["one_plus_rho"]), 1e-16)

    ax.semilogy(bi, rj, "s-", color="#d62728", lw=2.0, label=r"Residual Norm $R_J = \|J_{\tau_q} + \alpha_0 J_{\kappa^2}\| / \|J_{\tau_q}\|$")
    ax.semilogy(bi, one_plus_rho_abs, "^--", color="#1f77b4", lw=2.0, label=r"Collinearity Defect $|1 + \rho|$ (Machine Precision)")

    ax.set_xlabel(r"Biot Number, $\mathrm{Bi}$")
    ax.set_ylabel(r"Singularity Metric")
    ax.set_title(r"(a) Invariance of Sensitivity Collinearity to Heat Loss")
    ax.set_ylim(1e-17, 1e-7)
    ax.legend(loc="center right", framealpha=0.95)
    ax.grid(True)

    # Subplot (b): Condition number cond(F)
    ax = axes[1]
    ax.semilogy(bi, df_sweep["cond_F2"], "d-", color="#9467bd", lw=2.0, label=r"$\operatorname{cond}(F_{2\times 2})$: $(\tau_q, \kappa^2)$ Subspace")
    ax.semilogy(bi, df_sweep["cond_F3"], "o--", color="#8c564b", lw=2.0, label=r"$\operatorname{cond}(F_{3\times 3})$: $(\tau_q, \kappa^2, \mathrm{Bi})$ Full System")
    ax.axhline(1e16, color="black", ls=":", lw=1.2, label=r"Floating-Point Singularity Threshold")

    ax.set_xlabel(r"Biot Number, $\mathrm{Bi}$")
    ax.set_ylabel(r"Fisher Information Condition Number")
    ax.set_title(r"(b) Fisher Condition Numbers vs Biot Number")
    ax.set_ylim(1e15, 1e18)
    ax.legend(loc="lower right", framealpha=0.95)
    ax.grid(True)

    plt.tight_layout()
    save_fig(fig, "fig3_invariance_metrics_vs_biot")
    plt.close(fig)

def plot_fig4():
    print("Generating Figure 4: Singular Spectrum and Resonance Canyon...")
    df_sweep = pd.read_csv(os.path.join(DATA_DIR, "heatloss_parameter_sweep.csv"))
    df_off = pd.read_csv(os.path.join(DATA_DIR, "off_resonance_sweep.csv"))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    # Subplot (a): 3-parameter singular values
    ax = axes[0]
    bi = df_sweep["Bi"]
    ax.semilogy(bi, df_sweep["sigma1_3p"], "s-", color="#2ca02c", lw=2.0, label=r"$\sigma_1$ (Dominant Diffusive-Relaxation Mode)")
    ax.semilogy(bi, df_sweep["sigma2_3p"], "o-", color="#ff7f0e", lw=2.0, label=r"$\sigma_2$ (Convective Cooling Mode)")
    ax.semilogy(bi, df_sweep["sigma3_3p"], "^--", color="#d62728", lw=2.0, label=r"$\sigma_3$ (Null Space Singularity, $\sim 10^{-8}$)")

    ax.set_xlabel(r"Biot Number, $\mathrm{Bi}$")
    ax.set_ylabel(r"Singular Values, $\sigma_i$")
    ax.set_title(r"(a) 3-Parameter SVD Spectrum: Complete Separation of Modes")
    ax.set_ylim(1e-9, 1e2)
    ax.legend(loc="center right", framealpha=0.95)
    ax.grid(True)

    # Subplot (b): Off-resonance singularity canyon
    ax = axes[1]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for Bi_val, c in zip([0.0, 0.05, 0.2], colors):
        sub = df_off[df_off["Bi"] == Bi_val].sort_values("B")
        ax.semilogy(sub["B"], sub["cond_F2"], "o-", color=c, lw=2.0, label=f"Bi = {Bi_val:4.2f}")

    ax.axvline(1.0, color="red", ls="--", lw=1.2, label=r"Resonance $B = 1.0$")
    ax.set_xlabel(r"Guyer-Krumhansl Resonance Ratio, $B = \kappa^2 / (\alpha_0 \tau_q)$")
    ax.set_ylabel(r"Fisher Condition Number, $\operatorname{cond}(F_{2\times 2})$")
    ax.set_title(r"(b) Persistent Singularity Canyon Centered at $B = 1.0$")
    ax.set_ylim(1e1, 1e18)
    ax.legend(loc="upper right", framealpha=0.95)
    ax.grid(True)

    plt.tight_layout()
    save_fig(fig, "fig4_singular_spectrum_and_canyon")
    plt.close(fig)

def plot_fig5():
    print("Generating Figure 5: Dual Validation Benchmarks...")
    df_lap = pd.read_csv(os.path.join(DATA_DIR, "validation_laplace.csv"))
    df_mesh = pd.read_csv(os.path.join(DATA_DIR, "mesh_convergence.csv"))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    # Subplot (a): Laplace validation errors
    ax = axes[0]
    ax.plot(df_lap["Bi"], df_lap["L_inf_error"] * 1e5, "s-", color="#1f77b4", lw=2.0, label=r"$L_\infty$ Error ($\times 10^{-5}$)")
    ax.plot(df_lap["Bi"], df_lap["L_2_error"] * 1e5, "o--", color="#ff7f0e", lw=2.0, label=r"$L_2$ Error ($\times 10^{-5}$)")
    ax.set_xlabel(r"Biot Number, $\mathrm{Bi}$")
    ax.set_ylabel(r"Discrepancy vs Exact Laplace Solution ($10^{-5}$)")
    ax.set_title(r"(a) Analytical Laplace Benchmark (de Hoog Inversion)")
    ax.legend(loc="upper right", framealpha=0.95)
    ax.grid(True)
    ax.set_ylim(0, 1.5)

    # Subplot (b): Spatial grid convergence
    ax = axes[1]
    ax.loglog(df_mesh["dx"], df_mesh["L_inf_error"], "s-", color="#d62728", lw=2.0, label=r"Observed $L_\infty$ Error")
    # Reference 2nd order line
    dx_ref = df_mesh["dx"].values
    ref_line = df_mesh["L_inf_error"].values[0] * (dx_ref / dx_ref[0])**2
    ax.loglog(dx_ref, ref_line, "k--", lw=1.5, label=r"Ideal $O(\Delta x^2)$ Slope")

    ax.set_xlabel(r"Spatial Grid Spacing, $\Delta x$")
    ax.set_ylabel(r"Discretization Error, $L_\infty$")
    ax.set_title(r"(b) Spatial Grid Refinement & Second-Order Convergence")
    ax.legend(loc="lower right", framealpha=0.95)
    ax.grid(True)

    plt.tight_layout()
    save_fig(fig, "fig5_validation_dual_benchmarks")
    plt.close(fig)

if __name__ == "__main__":
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4()
    plot_fig5()
    print("All 5 publication figures generated successfully!")
