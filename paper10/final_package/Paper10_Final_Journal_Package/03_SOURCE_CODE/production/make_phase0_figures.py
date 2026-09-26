#!/usr/bin/env python3
"""
Phase-0 Figure Generation (manuscript-expansion campaign)
=========================================================
Generates the three NEW figures added during the Phase-0 scientific-depth
expansion of the Paper 10 journal package:

1. fig_unit_cell_schematic.png  -- didactic schematic of the 1D periodic
   bi-layer unit cell and the 10-state / 4-state field variables (no data).
2. fig_pb_benchmark_overlay.png -- direct overlay of the computed TMM
   phase-velocity ratio against the Papargyri-Beskou (2009) analytical curve
   (Eq. 28 / eq:pb_benchmark) across the 50 validation wavenumbers, plus the
   machine-precision relative-error panel. Uses ONLY the archived
   05_VALIDATION/benchmark_papargyri_beskou_results.csv (no new runs).
3. fig_chi_eta_heatmap.png      -- 2-D map of the first Bragg band-gap width
   Delta_Omega over the (chi, eta) plane from the Phase-0 supplementary grid
   (SUPP_CHI_ETA_GAP_SUMMARY.csv). The chi = 0 row is set to exactly zero,
   consistent with the frozen S2_chi00 production record (no gap).

All figures are saved at 300 DPI PNG into 02_FIGURES/.
"""

import os
import sys
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

HERE = os.path.abspath(os.path.dirname(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
FIG_DIR = os.path.join(PKG, "02_FIGURES")
DATA_DIR = os.path.join(PKG, "04_PRODUCTION_DATA")
VAL_DIR = os.path.join(PKG, "05_VALIDATION")

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 10, "axes.titlesize": 10,
    "legend.fontsize": 8, "figure.dpi": 300, "savefig.dpi": 300,
})


# -----------------------------------------------------------------------------
# Figure 1: unit-cell schematic (didactic, no data)
# -----------------------------------------------------------------------------

def make_schematic(path):
    fig = plt.figure(figsize=(7.6, 4.0))

    # --- Unit cell geometry panel -------------------------------------------
    ax = fig.add_axes([0.07, 0.42, 0.60, 0.50])
    a1, a2 = 0.5, 0.5
    ax.add_patch(Rectangle((0, 0), a1, 1.0, facecolor="#afc8e8", edgecolor="k", lw=1.2, zorder=2))
    ax.add_patch(Rectangle((a1, 0), a2, 1.0, facecolor="#d9d9d9", edgecolor="k", lw=1.2, zorder=2))
    ax.plot([a1, a1], [-0.04, 1.04], color="crimson", lw=1.6, ls="--", zorder=3)

    # lattice markers
    for xv, lab in [(0, r"$x=0$"), (a1, r"$x=a_1$"), (a1 + a2, r"$x=a$")]:
        ax.plot([xv], [-0.07], marker="v", color="k", clip_on=False)
        ax.text(xv, -0.16, lab, ha="center", va="top", fontsize=10)

    # thickness annotations
    ax.annotate("", xy=(a1 / 2, 1.14), xytext=(0, 1.14),
                arrowprops=dict(arrowstyle="<->", lw=1.0))
    ax.text(a1 / 2, 1.20, r"$a_1$ (Layer A, epoxy)", ha="center", fontsize=9)
    ax.annotate("", xy=(a1 + a2 / 2, 1.14), xytext=(a1, 1.14),
                arrowprops=dict(arrowstyle="<->", lw=1.0))
    ax.text(a1 + a2 / 2, 1.20, r"$a_2$ (Layer B, Al)", ha="center", fontsize=9)
    ax.annotate("", xy=(a1 + a2, -0.34), xytext=(0, -0.34),
                arrowprops=dict(arrowstyle="<->", lw=1.0))
    ax.text(a1, -0.44, r"unit cell  $a=a_1+a_2$, filling $\eta=a_1/a$", ha="center", va="top", fontsize=9)

    # interface label
    ax.text(a1, 0.5, " perfectly bonded\n mechanical + thermal\n continuity",
            ha="left", va="center", fontsize=7.5, color="crimson")

    # Bloch periodicity arrow
    ar = FancyArrowPatch((0.06, 1.34), (a1 + a2 - 0.06, 1.34),
                         arrowstyle="-|>", mutation_scale=14, lw=1.4, color="navy")
    ax.add_patch(ar)
    ax.text(a1, 1.44, r"Bloch transfer: $\mathbf{V}(x+a)=e^{\mathrm{i}k_x a}\,\mathbf{V}(x)$",
            ha="center", fontsize=9, color="navy")

    # coordinate axes
    ax.annotate("", xy=(-0.10, 1.0), xytext=(-0.10, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="k"))
    ax.annotate("", xy=(0.0, 0.0), xytext=(-0.10, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="k"))
    ax.text(-0.155, 0.9, r"$y$", fontsize=9)
    ax.text(-0.10, -0.14, r"$x$", fontsize=9, ha="center")

    ax.set_xlim(-0.22, 1.16)
    ax.set_ylim(-0.60, 1.55)
    ax.axis("off")
    ax.set_title("(a) 1-D periodic bi-layer unit cell (normal incidence, $\\xi=0$)", fontsize=9.5)

    # --- 10-state box ---------------------------------------------------------
    ax2 = fig.add_axes([0.03, 0.03, 0.52, 0.32])
    ax2.axis("off")
    l1 = r"$\mathbf{V}_{10}(x)=\left[\,u_x,\ u_y,\ u_{x,x},\ u_{y,x},\ \Theta,\right.$"
    l2 = r"$\left.\qquad P_x,\ P_y,\ R_x,\ R_y,\ Q_x\,\right]^{\mathsf{T}}$"
    ax2.text(0.02, 0.95, "(b) coupled in-plane state (10-state)", fontsize=9.5,
             va="top", transform=ax2.transAxes, fontweight="bold")
    ax2.text(0.02, 0.62, l1 + "\n" + l2, fontsize=8.2, va="top", transform=ax2.transAxes)
    ax2.text(0.02, 0.28, r"kinematic: $u_x,\, u_y,\, u_{x,x},\, u_{y,x},\, \Theta$"
             + "\n"
             + r"dynamic: $P_x,\, P_y$ (monopolar), $R_x,\, R_y$ (dipolar), $Q_x$ (flux)",
             fontsize=8.2, va="top", transform=ax2.transAxes)
    ax2.add_patch(Rectangle((0.0, 0.02), 0.99, 0.96, transform=ax2.transAxes,
                            fc="#f4f7fb", ec="navy", lw=1.0, zorder=0))

    # --- 4-state box ----------------------------------------------------------
    ax3 = fig.add_axes([0.57, 0.03, 0.40, 0.32])
    ax3.axis("off")
    ax3.text(0.02, 0.95, "(c) anti-plane state (4-state)", fontsize=9.5,
             va="top", transform=ax3.transAxes, fontweight="bold")
    ax3.text(0.02, 0.62,
             r"$\mathbf{V}_{4}(x)=\left[\,u_z,\ u_{z,x},\ P_z,\ R_z\,\right]^{\mathsf{T}}$",
             fontsize=8.2, va="top", transform=ax3.transAxes)
    ax3.text(0.02, 0.32, r"anti-plane shear decouples:"
             + "\n" + r"$u_z$ displacement, $P_z$, $R_z$ tractions",
             fontsize=8.2, va="top", transform=ax3.transAxes)
    ax3.add_patch(Rectangle((0.0, 0.02), 0.99, 0.96, transform=ax3.transAxes,
                            fc="#fbf6f4", ec="firebrick", lw=1.0, zorder=0))

    fig.savefig(path)
    plt.close(fig)
    print(f"saved {path}")


# -----------------------------------------------------------------------------
# Figure 2: Papargyri-Beskou benchmark overlay (archived validation data only)
# -----------------------------------------------------------------------------

def make_pb_overlay(path):
    ks, om_ana, om_tmm, errs = [], [], [], []
    with open(os.path.join(VAL_DIR, "benchmark_papargyri_beskou_results.csv")) as f:
        for row in csv.DictReader(f):
            ks.append(float(row["k"]))
            om_ana.append(float(row["omega_analytical_pb"]))
            om_tmm.append(float(row["omega_tmm_independent"]))
            errs.append(float(row["tmm_relative_error"]))
    ks = np.array(ks); om_ana = np.array(om_ana); om_tmm = np.array(om_tmm); errs = np.array(errs)

    Vs = 1000.0  # benchmark solid classical shear speed (parameters.py)
    ratio_ana = om_ana / (ks * Vs)
    ratio_tmm = om_tmm / (ks * Vs)
    max_err = float(np.max(errs))

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(7.6, 3.1))

    axl.plot(ks, ratio_ana, "-", color="crimson", lw=2.2,
             label=r"analytical  $V_{gh}/V_c=\sqrt{(1+g^2k^2)/(1+h^2k^2)}$  (Eq. 28)")
    axl.plot(ks, ratio_tmm, "o", color="navy", ms=4.5, mfc="none", mew=1.1,
             label="present TMM (independent secular solve)")
    axl.set_xlabel(r"wavenumber $k$ (m$^{-1}$)")
    axl.set_ylabel(r"phase velocity ratio $V_{gh}/V_c$")
    axl.set_title("(a) gradient phase velocity: TMM vs. analytical", fontsize=9)
    axl.legend(loc="lower left", frameon=False, fontsize=7.2, handlelength=1.6,
               borderaxespad=0.2, labelspacing=0.3)
    axl.set_xlim(0, 2000)
    axl.text(0.975, 0.90,
             r"$g=\sqrt{c}=1$ mm, $h=d/\sqrt{3}=1.5$ mm" + "\n" + r"$k\in[10, 2000]$ m$^{-1}$ (50 points)",
             transform=axl.transAxes, ha="right", va="top", fontsize=7.5)

    axr.plot(ks, errs, "s-", color="seagreen", ms=3.5, lw=1.0)
    axr.axhline(max_err, color="crimson", ls="--", lw=1.0)
    axr.set_yscale("log")
    axr.set_ylim(1e-17, 1e-14)
    axr.set_xlabel(r"wavenumber $k$ (m$^{-1}$)")
    axr.set_ylabel(r"relative error $|\omega_{\mathrm{TMM}}-\omega_{\mathrm{PB}}|/\omega_{\mathrm{PB}}$")
    axr.set_title("(b) machine-precision agreement", fontsize=9)
    exp10 = int(np.floor(np.log10(max_err)))
    axr.text(0.03, 0.86, rf"max $= {max_err / 10**exp10:.2f}\times 10^{{{exp10}}}$",
             transform=axr.transAxes, fontsize=8, color="crimson")

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"saved {path}")


# -----------------------------------------------------------------------------
# Figure 3: (chi, eta) band-gap width heatmap (Phase-0 supplementary grid)
# -----------------------------------------------------------------------------

def make_heatmap(path):
    with open(os.path.join(DATA_DIR, "SUPP_CHI_ETA_GRID_META.json")) as f:
        meta = json.load(f)
    chi_vals = np.array(meta["chi_values"])
    eta_vals = np.array(meta["eta_values"])

    W = np.full((len(eta_vals), len(chi_vals)), np.nan)
    truncated = np.zeros_like(W, dtype=bool)

    with open(os.path.join(DATA_DIR, "SUPP_CHI_ETA_GAP_SUMMARY.csv")) as f:
        for row in csv.DictReader(f):
            if int(row["gap_index"]) != 1:
                continue
            ci = int(np.argmin(np.abs(chi_vals - float(row["chi"]))))
            ei = int(np.argmin(np.abs(eta_vals - float(row["eta"]))))
            W[ei, ci] = float(row["delta_Omega"])
            truncated[ei, ci] = row["is_boundary_truncated"].strip() == "True"

    # Physics rule (consistent with frozen S2_chi00 production record):
    # at chi = 0 the cell is homogeneous -> no Bragg gap, Delta_Omega = 0.
    ci0 = int(np.argmin(np.abs(chi_vals - 0.0)))
    W[:, ci0] = 0.0
    truncated[:, ci0] = False

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    X, Y = np.meshgrid(chi_vals, eta_vals)
    Wm = np.ma.masked_invalid(W)
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad(color="0.92")
    pc = ax.pcolormesh(X, Y, Wm, cmap=cmap, shading="nearest",
                       vmin=0.0, vmax=float(np.nanmax(W)))
    c = fig.colorbar(pc, ax=ax, pad=0.02)
    c.set_label(r"first Bragg gap width  $\Delta\Omega$")

    # annotate cells
    for ei in range(len(eta_vals)):
        for ci in range(len(chi_vals)):
            if np.isnan(W[ei, ci]):
                ax.text(chi_vals[ci], eta_vals[ei], "no\ngap", ha="center", va="center",
                        fontsize=5.8, color="0.35")
            elif truncated[ei, ci]:
                ax.text(chi_vals[ci], eta_vals[ei], f"{W[ei,ci]:.2f}*", ha="center",
                        va="center", fontsize=6.2, color="w")
            else:
                lum = W[ei, ci] / max(np.nanmax(W), 1e-12)
                ax.text(chi_vals[ci], eta_vals[ei], f"{W[ei,ci]:.2f}", ha="center",
                        va="center", fontsize=6.2,
                        color="w" if lum < 0.55 else "k")

    # overlay frozen S2/S4 production anchor points
    anchors = [(0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (1.0, 0.2), (1.0, 0.8)]
    for (ac, ae) in anchors:
        ax.plot(ac, ae, "o", ms=7, mfc="none", mec="crimson", mew=1.6)
    ax.plot([], [], "o", ms=7, mfc="none", mec="crimson", mew=1.6,
            label="frozen S2/S4 production cases (reproduced exactly)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.115), frameon=False, fontsize=7.5)

    ax.set_xlabel(r"material contrast $\chi$")
    ax.set_ylabel(r"filling fraction $\eta=a_1/a$")
    ax.set_title(r"First Bragg band-gap width $\Delta\Omega$ over the $(\chi,\eta)$ plane"
                 + "\n(active DPL baseline; * = open at $\\Omega=1.80$ ceiling)",
                 fontsize=9)
    ax.set_xlim(chi_vals.min() - 0.05, chi_vals.max() + 0.05)
    ax.set_ylim(eta_vals.min() - 0.03, eta_vals.max() + 0.03)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"saved {path}")


if __name__ == "__main__":
    make_schematic(os.path.join(FIG_DIR, "fig_unit_cell_schematic.png"))
    make_pb_overlay(os.path.join(FIG_DIR, "fig_pb_benchmark_overlay.png"))
    make_heatmap(os.path.join(FIG_DIR, "fig_chi_eta_heatmap.png"))
