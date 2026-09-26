#!/usr/bin/env python3
"""Figure 1 (FEM_3-style): microstructural ellipsoid and rotated length tensor.

This analytic schematic uses the locked baseline length $l_{\mathrm{iso}}=0.20$ m
from the case-parameter table. Its rotation convention matches Section 2;
the presentation follows the FEM_3 graphical language.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, grid, legend, panel, spine_frame, BLUE, RED, GREEN, ORANGE

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    l_iso = 0.20  # m; locked Case-H baseline in OVERLEAF/tables/tab01_case_parameters.tex

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    # --- Panel (a): ellipses for AR in {1,3,5,10} at theta = 45 deg ---
    t = np.linspace(0, 2 * np.pi, 200)
    th = np.deg2rad(45.0)
    R_global_to_local = np.array([[np.cos(th), -np.sin(th)],
                                  [np.sin(th),  np.cos(th)]])
    Rm = R_global_to_local.T  # local principal coordinates to global (clockwise theta)
    colors = [BLUE, GREEN, ORANGE, RED]
    for ar, c in zip([1.0, 3.0, 5.0, 10.0], colors):
        l1 = l_iso * np.sqrt(ar)
        l2 = l_iso / np.sqrt(ar)
        rc = Rm @ np.vstack([l1 * np.cos(t), l2 * np.sin(t)])
        ax1.plot(rc[0], rc[1], color=c, lw=1.5,
                 label=r"$\mathrm{AR} = %s$" % (int(ar) if ar.is_integer() else ar))
    ax1.axhline(0, color="0.6", ls="--", lw=0.7, zorder=0)
    ax1.axvline(0, color="0.6", ls="--", lw=0.7, zorder=0)
    ax1.set_aspect("equal")
    panel(ax1, r"(a) Microstructural ellipse ($\theta = 45^\circ$ clockwise)")
    ax1.set_xlabel(r"$x_1$ [m]")
    ax1.set_ylabel(r"$x_2$ [m]")
    grid(ax1)
    legend(ax1, loc="upper right", outside=True)

    # --- Panel (b): L_ij(theta) for AR = 5 (clockwise passive convention) ---
    th_s = np.linspace(0, 90, 181)
    th_r = np.deg2rad(th_s)
    ar_b = 5.0
    l1b = l_iso * np.sqrt(ar_b)
    l2b = l_iso / np.sqrt(ar_b)
    L11 = l1b ** 2 * np.cos(th_r) ** 2 + l2b ** 2 * np.sin(th_r) ** 2
    L22 = l1b ** 2 * np.sin(th_r) ** 2 + l2b ** 2 * np.cos(th_r) ** 2
    L12 = (l2b ** 2 - l1b ** 2) * np.sin(th_r) * np.cos(th_r)
    ax2.plot(th_s, L11, "-", color=BLUE, lw=1.6, label=r"$L_{11}(\theta)$")
    ax2.plot(th_s, L22, "--", color=RED, lw=1.6, label=r"$L_{22}(\theta)$")
    ax2.plot(th_s, L12, "-.", color=GREEN, lw=1.6, label=r"$L_{12}(\theta)$")
    panel(ax2, r"(b) Tensor components $\mathbf{L}(\theta)$ ($\mathrm{AR} = 5$)")
    ax2.set_xlabel(r"Orientation angle $\theta$ [deg]")
    ax2.set_ylabel(r"$L_{ij}$ [$\mathrm{m}^2$]")
    ax2.set_xlim(0, 90)
    grid(ax2)
    legend(ax2, loc="center right", framealpha=0.7, outside=True)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig01_ellipsoid_tensor.pdf"))
    plt.close(fig)
    print("Generated fig01_ellipsoid_tensor.pdf")


if __name__ == "__main__":
    main()
