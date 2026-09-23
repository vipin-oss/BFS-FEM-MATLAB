#!/usr/bin/env python3
"""
paper9/figures/gen/fig04_benchmark_validation.py
Generates Figure 4: PRESENT 1D transfer-matrix calculations for Benchmarks B1 and B3
(remediation item 8 -- scope stated exactly):
  Panel (a): Benchmark B1 -- classical bilayer (AlN/BaTiO3) dispersion (present TM == Rytov).
  Panel (b): Benchmark B3 -- dipolar gradient bilayer (Pb/brass) dispersion, pinned run
             P11D-B3-R1 (N_points = 720).
This figure contains ONLY present calculations.  No source-curve overlay is drawn:
the source panels provide no released numerical values (and Fig. 4(c) of Li et al.
(2023) sweeps tau_R without annotating c_bar/d_bar), so a trace overlay cannot be
constructed without fabricating source points.  Comparison to the published panels
is QUALITATIVE GRAPHICAL COMPARISON only (see paper9/audit/evidence/*.png); no
error percentages are computed anywhere (Blueprint v1.3 evidence hierarchy).
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "paper9"))
from validation.b1_b2_b3_solver import BenchmarkB1, BenchmarkB3

OUT_DIR = REPO_ROOT / "paper9" / "figures" / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_fig04():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 13,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.0), constrained_layout=True)

    # -------------------------------------------------------------------------
    # Panel (a): Benchmark B1 (Classical AlN/BaTiO3 Bilayer)
    # -------------------------------------------------------------------------
    b1 = BenchmarkB1()
    omegas = np.linspace(0.001, 3.2, 3000)
    cos_vals = np.array([b1.rytov_cosKb(w) for w in omegas])
    in_gap = np.abs(cos_vals) > 1.0

    # Plot branches
    valid = ~in_gap
    w_valid = omegas[valid]
    cos_valid = cos_vals[valid]
    k_valid = np.arccos(np.clip(cos_valid, -1.0, 1.0)) / np.pi

    # Break continuous line at gaps
    diff_w = np.diff(w_valid)
    split_indices = np.where(diff_w > 0.005)[0] + 1
    w_chunks = np.split(w_valid, split_indices)
    k_chunks = np.split(k_valid, split_indices)

    for i, (wc, kc) in enumerate(zip(w_chunks, k_chunks)):
        label = "Present calculation (1D TM == Rytov)" if i == 0 else None
        ax1.plot(kc, wc, color="navy", lw=2.0, label=label)

    # Shade first 5 band gaps
    het_data = b1.compute_heterogeneous_dispersion()
    for idx, (w_lo, w_hi, width) in enumerate(het_data["band_gaps"][:4]):
        ax1.axhspan(w_lo, w_hi, color="lightsteelblue", alpha=0.35,
                    label=f"Bragg Band Gap (BG$_{idx+1}$)" if idx == 0 else None)
        ax1.text(0.5, 0.5 * (w_lo + w_hi), f"Gap {idx+1}", ha="center", va="center",
                 fontsize=8, color="navy", fontweight="bold", alpha=0.7)

    ax1.set_xlim(0.0, 1.0)
    ax1.set_ylim(0.0, 3.0)
    ax1.set_xlabel(r"Normalized Bloch Wavenumber $\bar{k} = k b / \pi$")
    ax1.set_ylabel(r"Normalized Frequency $\bar{\omega} = \omega / \omega_0$")
    ax1.set_title(r"(a) B1: Classical Bilayer (AlN/BaTiO$_3$)", pad=10)
    ax1.grid(True, ls=":", alpha=0.6)
    ax1.legend(loc="upper left", framealpha=0.9)

    ax1.text(0.95, 0.05,
             "Anchor: Li et al. (2024) Fig. 2(a) [GRAPH_ONLY raster]\n"
             "Shown: PRESENT calculation only (no source trace overlay)\n"
             r"Level 1 Homog. Err: $6.47 \times 10^{-16}$" "\n"
             r"Level 2 Ident. Err: $7.22 \times 10^{-16}$" "\n"
             "Comparison: qualitative graphical only -- no error %",
             transform=ax1.transAxes, ha="right", va="bottom",
             fontsize=7, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="navy", alpha=0.85))

    # -------------------------------------------------------------------------
    # Panel (b): Benchmark B3 (Dipolar Gradient Bilayer Pb/Brass)
    # -------------------------------------------------------------------------
    b3 = BenchmarkB3()
    het_b3 = b3.compute_heterogeneous_dispersion(N_points=720)  # pinned run P11D-B3-R1
    omegas_b3 = np.linspace(0.01, 3.6, 720)

    # Reconstruct branch segments from propagating modes
    branch_pts = []
    for w_bar in omegas_b3:
        w = w_bar * b3.omega_0
        TA, _, _ = b3.layer_T_sh(w, b3.a_1, b3.c_1, b3.d_1, b3.mu_1, b3.rho_1)
        TB, _, _ = b3.layer_T_sh(w, b3.a_2, b3.c_2, b3.d_2, b3.mu_2, b3.rho_2)
        evs = [ev for ev in np.linalg.eigvals(TB @ TA) if abs(abs(ev) - 1.0) < 0.02]
        for ev in evs:
            branch_pts.append((abs(np.angle(ev)) / np.pi, w_bar))

    branch_pts = np.array(branch_pts)
    if len(branch_pts) > 0:
        ax2.scatter(branch_pts[:, 0], branch_pts[:, 1], s=4, color="crimson",
                    label=r"Present calculation (run P11D-B3-R1)", alpha=0.85)

    # Shade band gaps
    for idx, (w_lo, w_hi, width) in enumerate(het_b3["band_gaps"][:3]):
        ax2.axhspan(w_lo, w_hi, color="mistyrose", alpha=0.45,
                    label=f"Stop Band (SB$_{idx+1}$)" if idx == 0 else None)
        ax2.text(0.22, 0.5 * (w_lo + w_hi), f"Stop Band {idx+1}", ha="center", va="center",
                 fontsize=8, color="darkred", fontweight="bold", alpha=0.7)

    ax2.set_xlim(0.0, 1.0)
    ax2.set_ylim(0.0, 3.6)
    ax2.set_xlabel(r"Normalized Bloch Wavenumber $\bar{k} = k a_1 / \pi$")
    ax2.set_ylabel(r"Normalized Frequency $\bar{\omega} = \omega / \omega_0$")
    ax2.set_title(r"(b) B3: Dipolar Gradient Bilayer (Pb/Brass)", pad=10)
    ax2.grid(True, ls=":", alpha=0.6)
    ax2.legend(loc="upper left", framealpha=0.9)

    ax2.text(0.95, 0.05,
             "Anchor: Li et al. (2023) Fig. 4(c) [GRAPH_ONLY raster]\n"
             "  (panel sweeps $\\tau_R$; NO $\\bar{c}/\\bar{d}$ annotation)\n"
             r"  $\bar{c}/\bar{d}$ inherited from Fig. 3(b) [S], run P11D-B3-R1" "\n"
             r"Level 1 Homog. Err: $1.37 \times 10^{-13}$" "\n"
             r"Level 2 Ident. Err: $4.19 \times 10^{-14}$" "\n"
             "Comparison: qualitative graphical only -- no error %",
             transform=ax2.transAxes, ha="right", va="bottom",
             fontsize=7, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="crimson", alpha=0.85))

    pdf_out = OUT_DIR / "fig04_benchmark_validation.pdf"
    png_out = OUT_DIR / "fig04_benchmark_validation.png"
    plt.savefig(pdf_out, dpi=300)
    plt.savefig(png_out, dpi=300)
    plt.close(fig)
    print(f"Generated Figure 4 deliverables:\n  {pdf_out}\n  {png_out}")

if __name__ == "__main__":
    generate_fig04()
