#!/usr/bin/env python3
"""Figure 4 (FEM_3-style): present 1D transfer-matrix benchmarks B1 and B3.

Loads the exact present-calculation pipelines from the authoritative
PROGRAM/paper9 validation/solver and replots them in the FEM_3 graphical
language.  No source curve is drawn, no error percentage is created: identical
scientific scope to paper9/figures/gen/fig04_benchmark_validation.py.
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, DATA)
from fem3style import apply, grid, legend, panel, spine_frame, BLUE, RED
from validation.b1_b2_b3_solver import BenchmarkB1, BenchmarkB3

OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.9))

    # ---- Panel (a): B1 classical bilayer, present TM == Rytov ----
    b1 = BenchmarkB1()
    omegas = np.linspace(0.001, 3.2, 3000)
    cos_vals = np.array([b1.rytov_cosKb(w) for w in omegas])
    valid = np.abs(cos_vals) <= 1.0
    w_valid = omegas[valid]
    k_valid = np.arccos(np.clip(cos_vals[valid], -1.0, 1.0)) / np.pi
    diff_w = np.diff(w_valid)
    splits = np.where(diff_w > 0.005)[0] + 1
    for i, (wc, kc) in enumerate(zip(np.split(w_valid, splits), np.split(k_valid, splits))):
        ax1.plot(kc, wc, color=BLUE, lw=1.5,
                 label="Present calculation (1D TM == Rytov)" if i == 0 else None)
    het_data = b1.compute_heterogeneous_dispersion()
    for idx, (w_lo, w_hi, width) in enumerate(het_data["band_gaps"][:4]):
        ax1.axhspan(w_lo, w_hi, color="0.72", alpha=0.45,
                    label="Bragg band gap" if idx == 0 else None)
        ax1.text(0.5, 0.5 * (w_lo + w_hi), f"Gap {idx+1}", ha="center", va="center",
                 fontsize=8, color="0.2")
    ax1.set_xlim(0.0, 1.0)
    ax1.set_ylim(0.0, 3.0)
    ax1.set_xlabel(r"Normalized Bloch wavenumber $\bar{k} = kb/\pi$")
    ax1.set_ylabel(r"Normalized frequency $\bar{\omega} = \omega/\omega_0$")
    panel(ax1, r"(a) B1: classical bilayer (AlN/BaTiO$_3$)")
    grid(ax1)
    legend(ax1, loc="upper left")
    ax1.text(0.95, 0.05,
             "Anchor: Li et al. (2024) Fig. 2(a) [GRAPH_ONLY raster]\n"
             "Shown: PRESENT calculation only (no source trace overlay)\n"
             r"Level 1 Homog. Err: $6.47 \times 10^{-16}$" "\n"
             r"Level 2 Ident. Err: $7.22 \times 10^{-16}$" "\n"
             "Comparison: qualitative graphical only - no error %",
             transform=ax1.transAxes, ha="right", va="bottom",
             fontsize=7, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.5", alpha=0.9))

    # ---- Panel (b): B3 dipolar gradient bilayer Pb/Brass ----
    b3 = BenchmarkB3()
    het_b3 = b3.compute_heterogeneous_dispersion(N_points=720)  # pinned run P11D-B3-R1
    omegas_b3 = np.linspace(0.01, 3.6, 720)
    pts = []
    for w_bar in omegas_b3:
        w = w_bar * b3.omega_0
        TA = b3.layer_T_sh(w, b3.a_1, b3.c_1, b3.d_1, b3.mu_1, b3.rho_1)[0]
        TB = b3.layer_T_sh(w, b3.a_2, b3.c_2, b3.d_2, b3.mu_2, b3.rho_2)[0]
        evs = np.linalg.eigvals(TB @ TA)
        for ev in evs:
            if abs(abs(ev) - 1.0) < 0.02:
                pts.append((abs(np.angle(ev)) / np.pi, w_bar))
    pts = np.array(pts)
    if len(pts):
        ax2.scatter(pts[:, 0], pts[:, 1], s=4, color=RED, alpha=0.85,
                    label="Present calculation (run P11D-B3-R1)")
    for idx, (w_lo, w_hi, width) in enumerate(het_b3["band_gaps"][:3]):
        ax2.axhspan(w_lo, w_hi, color="0.80", alpha=0.45,
                    label="Stop band" if idx == 0 else None)
        ax2.text(0.22, 0.5 * (w_lo + w_hi), f"Stop Band {idx+1}", ha="center", va="center",
                 fontsize=8, color="0.2")
    ax2.set_xlim(0.0, 1.0)
    ax2.set_ylim(0.0, 3.6)
    ax2.set_xlabel(r"Normalized Bloch wavenumber $\bar{k} = ka_1/\pi$")
    ax2.set_ylabel(r"Normalized frequency $\bar{\omega} = \omega/\omega_0$")
    panel(ax2, r"(b) B3: dipolar gradient bilayer (Pb/Brass)")
    grid(ax2)
    legend(ax2, loc="upper left")
    ax2.text(0.95, 0.05,
             "Anchor: Li et al. (2023) Fig. 4(c) [GRAPH_ONLY raster]\n"
             r"  (NO $\bar{c}/\bar{d}$ annotation; $\tau_R$ sweep is source Fig. 7)" "\n"
             r"  $\bar{c}/\bar{d}$ inherited from Fig. 3(b) [S], run P11D-B3-R1" "\n"
             r"Level 1 Homog. Err: $1.37 \times 10^{-13}$" "\n"
             r"Level 2 Ident. Err: $4.19 \times 10^{-14}$" "\n"
             "Comparison: qualitative graphical only - no error %",
             transform=ax2.transAxes, ha="right", va="bottom",
             fontsize=7, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.5", alpha=0.9))
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig04_benchmark_validation.pdf"))
    plt.close(fig)
    print("Generated fig04_benchmark_validation.pdf")


if __name__ == "__main__":
    main()
