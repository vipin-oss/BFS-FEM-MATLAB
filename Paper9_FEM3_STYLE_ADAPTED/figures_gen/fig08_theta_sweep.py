#!/usr/bin/env python3
"""Figure 8 (FEM_3-style): orientation sweep theta in [0,90] at AR=5.

Data pipeline verbatim from paper9/figures/gen/fig08_theta_sweep.py.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, grid, legend, panel, spine_frame

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    with open(os.path.join(DATA, "results/raw/p5_production_raw_mesh16.json")) as f:
        data = json.load(f)["study_S3"]

    thetas = [item["theta_deg"] for item in data]
    om_X_T = [item["omega_X"][0] for item in data]
    om_X_L = [item["omega_X"][2] for item in data]
    om_M_T = [item["omega_M"][0] for item in data]
    om_M_L = [item["omega_M"][2] for item in data]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    ax1.plot(thetas, om_X_T, "o-", color="#1f77b4", lw=1.4, ms=4,
             label=r"Transverse acoustic $\omega_T(X)$")
    ax1.plot(thetas, om_X_L, "s--", color="#d62728", lw=1.4, ms=4,
             label=r"Longitudinal acoustic $\omega_L(X)$")
    ax1.set_xlabel(r"Orientation angle $\theta$ [deg]")
    ax1.set_ylabel(r"Zone-edge frequency $\bar{\omega}(X)$")
    panel(ax1, r"(a) Acoustic frequency migration at $X$")
    ax1.set_xlim(-5, 95)
    ax1.set_xticks([0, 15, 30, 45, 60, 75, 90])
    grid(ax1)
    legend(ax1, loc="center", framealpha=0.7)

    ax2.plot(thetas, om_M_T, "^--", color="#2ca02c", lw=1.4, ms=4,
             label=r"Transverse acoustic, $M$")
    ax2.plot(thetas, om_M_L, "D-", color="#9467bd", lw=1.4, ms=4,
             label=r"Longitudinal acoustic, $M$")
    ax2.axvline(45, color="0.55", ls=":", lw=1.0, label=r"Symmetry axis $\theta = 45^\circ$")
    ax2.set_xlabel(r"Orientation angle $\theta$ [deg]")
    ax2.set_ylabel(r"Corner frequency $\bar{\omega}(M)$")
    panel(ax2, r"(b) Diagonal symmetry at $M$")
    ax2.set_xlim(-5, 95)
    ax2.set_xticks([0, 15, 30, 45, 60, 75, 90])
    grid(ax2)
    legend(ax2, loc="center left", fontsize=8, framealpha=0.7)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig08_theta_sweep.pdf"))
    plt.close(fig)
    print("Generated fig08_theta_sweep.pdf")


if __name__ == "__main__":
    main()
