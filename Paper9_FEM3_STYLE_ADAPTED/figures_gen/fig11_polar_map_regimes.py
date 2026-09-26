#!/usr/bin/env python3
"""Figure 11 (FEM_3-style): polar design regimes and orientation sensitivity.

Data pipeline verbatim from fig11_polar_map_regimes.py.  The plasma colormap
encoding is retained (Paper9 scientific encoding); ambient styling is FEM_3.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, grid, legend, panel

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    with open(os.path.join(DATA, "results/raw/p5_production_raw_mesh16.json")) as f:
        d = json.load(f)
    polar_data = d["study_S6_polar_map"]
    stheta_data = d["study_S6_sensitivity_Stheta"]
    s5_data = d["study_S5_design_map"]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    X_pos, Y_pos, vals_pos = [], [], []
    X_neg, Y_neg = [], []
    for item, s5_item in zip(polar_data, s5_data):
        x, y = item["X"], item["Y"]
        gap_val = s5_item["gaps"][1]["delta_GX"]
        if gap_val > 0:
            X_pos.append(x); Y_pos.append(y); vals_pos.append(gap_val)
        else:
            X_neg.append(x); Y_neg.append(y)

    th_arc = np.linspace(0, np.pi / 2, 100)
    for r in [1, 3, 5, 10]:
        ax1.plot(r * np.cos(th_arc), r * np.sin(th_arc), "0.60", ls=":", lw=0.7)
        ax1.text(r * np.cos(np.pi / 4) + 0.15, r * np.sin(np.pi / 4) + 0.15,
                 str(r), fontsize=7.5, color="0.4")
    for th_d in [0, 15, 30, 45, 60, 75, 90]:
        th_r = np.deg2rad(th_d)
        ax1.plot([0, 10 * np.cos(th_r)], [0, 10 * np.sin(th_r)], "0.60", ls=":", lw=0.5)

    sc = ax1.scatter(X_pos, Y_pos, c=vals_pos, cmap="plasma", s=30, edgecolors="k",
                     lw=0.5, label=r"$\Delta_{GX}>0$ (directional stop band)", zorder=5)
    if X_neg:
        ax1.scatter(X_neg, Y_neg, color="white", edgecolors="crimson", s=30, lw=1.0,
                    label=r"$\Delta_{GX}\leq 0$ (pass band)", zorder=5)
    cb = fig.colorbar(sc, ax=ax1, pad=0.03)
    cb.set_label(r"Directional gap $\Delta_{GX}$")
    ax1.set_aspect("equal")
    ax1.set_xlim(-0.5, 11)
    ax1.set_ylim(-0.5, 11)
    ax1.set_xlabel(r"$X = \mathrm{AR}\cos\theta$")
    ax1.set_ylabel(r"$Y = \mathrm{AR}\sin\theta$")
    panel(ax1, r"(a) Polar directional regimes ($\Gamma$-$X$)")
    grid(ax1)
    legend(ax1, loc="upper right", fontsize=7)
    for s in ax1.spines.values():
        s.set_linewidth(0.8)

    ars = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    stheta_vals = [stheta_data["AR_%d" % int(ar)]["S_theta_rad_inv"] for ar in ars]
    ax2.plot(ars, stheta_vals, "o-", color="#9467bd", lw=1.6, ms=5,
             label=r"Sensitivity $S_\theta$")
    ax2.set_xlabel(r"Aspect ratio $\mathrm{AR}$")
    ax2.set_ylabel(r"$S_\theta$ [$\mathrm{rad}^{-1}$]")
    panel(ax2, r"(b) Orientation sensitivity vs $\mathrm{AR}$")
    ax2.set_xticks(ars)
    grid(ax2)
    legend(ax2, loc="upper left", fontsize=8)
    for s in ax2.spines.values():
        s.set_linewidth(0.8)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig11_polar_map_regimes.pdf"))
    plt.close(fig)
    print("Generated fig11_polar_map_regimes.pdf")


if __name__ == "__main__":
    main()
