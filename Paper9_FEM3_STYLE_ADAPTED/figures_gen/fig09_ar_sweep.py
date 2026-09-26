#!/usr/bin/env python3
"""Figure 9 (FEM_3-style): aspect-ratio sweep AR in [1,10] at theta=45 deg.

Data pipeline verbatim from paper9/figures/gen/fig09_ar_sweep.py.
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
        data = json.load(f)["study_S4"]

    ars = [item["AR"] for item in data]
    om_X_T = [item["omega_X"][0] for item in data]
    om_X_L = [item["omega_X"][2] for item in data]
    om_M_T = [item["omega_M"][0] for item in data]
    om_M_L = [item["omega_M"][2] for item in data]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    ax1.plot(ars, om_X_T, "o-", color="#1f77b4", lw=1.4, ms=4,
             label=r"Transverse acoustic $\omega_T(X)$")
    ax1.plot(ars, om_X_L, "s--", color="#d62728", lw=1.4, ms=4,
             label=r"Longitudinal acoustic $\omega_L(X)$")
    ax1.set_xlabel(r"Aspect ratio $\mathrm{AR}$")
    ax1.set_ylabel(r"Zone-edge frequency $\bar{\omega}(X)$")
    panel(ax1, r"(a) Acoustic frequencies at $X$")
    ax1.set_xticks(ars)
    grid(ax1)
    legend(ax1, loc="lower right", fontsize=8, outside=True)

    ax2.plot(ars, om_M_T, "^--", color="#2ca02c", lw=1.4, ms=4,
             label=r"Transverse acoustic, $M$")
    ax2.plot(ars, om_M_L, "D-", color="#9467bd", lw=1.4, ms=4,
             label=r"Longitudinal acoustic, $M$")
    ax2.set_xlabel(r"Aspect ratio $\mathrm{AR}$")
    ax2.set_ylabel(r"Corner frequency $\bar{\omega}(M)$")
    panel(ax2, r"(b) Frequencies at $M$")
    ax2.set_xticks(ars)
    grid(ax2)
    legend(ax2, loc="center left", fontsize=8, outside=True)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig09_ar_sweep.pdf"))
    plt.close(fig)
    print("Generated fig09_ar_sweep.pdf")


if __name__ == "__main__":
    main()
