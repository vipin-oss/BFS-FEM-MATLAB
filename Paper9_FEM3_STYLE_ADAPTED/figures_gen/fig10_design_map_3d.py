#!/usr/bin/env python3
"""Figure 10 (FEM_3-style): (theta,AR) directional stop-band design map and
contour projection.  Data pipeline verbatim from fig10_design_map_3d.py;
the viridis colormap is retained because it is the Paper9 scientific encoding
of the design-map values (FEM_3 has no comparable 3D surface).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from fem3style import apply, grid, legend, panel

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    with open(os.path.join(DATA, "results/raw/p5_production_raw_mesh16.json")) as f:
        data = json.load(f)["study_S5_design_map"]

    ars = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    thetas = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]
    TH, AR = np.meshgrid(thetas, ars)
    Z = np.zeros_like(TH)
    for item in data:
        i = ars.index(item["AR"])
        j = thetas.index(item["theta_deg"])
        Z[i, j] = item["gaps"][1]["delta_GX"]

    apply()
    fig = plt.figure(figsize=(7.8, 3.6))

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(TH, AR, Z, cmap="viridis", edgecolor="k", lw=0.4, alpha=0.85)
    ax1.set_xlabel(r"$\theta$ [deg]", labelpad=4)
    ax1.set_ylabel(r"$\mathrm{AR}$", labelpad=4)
    ax1.set_zlabel(r"$\Delta_{GX}$", labelpad=4)
    ax1.set_title(r"(a) Response surface $\Delta_{GX}(\theta,\mathrm{AR})$", fontsize=10)
    ax1.view_init(elev=28, azim=-125)

    ax2 = fig.add_subplot(1, 2, 2)
    cp = ax2.contourf(TH, AR, Z, levels=12, cmap="viridis")
    cb = fig.colorbar(cp, ax=ax2, pad=0.04)
    cb.set_label(r"Directional gap $\Delta_{GX}$")
    cs = ax2.contour(TH, AR, Z, levels=[0.0], colors="crimson", linewidths=1.6, linestyles="--")
    ax2.clabel(cs, fmt=r"$\Delta=0$", fontsize=8)
    ax2.scatter(TH.flatten(), AR.flatten(), color="k", s=12, alpha=0.7,
                label="Evaluated points (42)")
    ax2.set_xlabel(r"Orientation angle $\theta$ [deg]")
    ax2.set_ylabel(r"Aspect ratio $\mathrm{AR}$")
    panel(ax2, "(b) Contour projection & stop-band regimes")
    ax2.set_xticks(thetas)
    ax2.set_yticks(ars)
    grid(ax2)
    legend(ax2, loc="lower left", fontsize=8, framealpha=0.7, outside=True)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig10_design_map_3d.pdf"))
    plt.close(fig)
    print("Generated fig10_design_map_3d.pdf")


if __name__ == "__main__":
    main()
