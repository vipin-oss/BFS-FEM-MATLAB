#!/usr/bin/env python3
"""Figure 6 (FEM_3-style): Case H band structure along Gamma-X-M-Gamma.

Data pipeline verbatim from paper9/figures/gen/fig06_caseH_dispersion.py.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, grid, legend, panel, spine_frame, BLUE, RED

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    with open(os.path.join(DATA, "results/raw/p5_production_raw_mesh16.json")) as f:
        data = json.load(f)["study_S1"]

    s1 = np.linspace(0, 1, 41)
    s2 = np.linspace(1, 2, 41)[1:]
    s3 = np.linspace(2, 2 + np.sqrt(2), 41)[1:]
    s_full = np.concatenate([s1, s2, s3])

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5), sharey=True)

    iso = np.array(data["AR_1_th_0"]["tracked_bands"])
    an0 = np.array(data["AR_10_th_0"]["tracked_bands"])
    an45 = np.array(data["AR_10_th_45"]["tracked_bands"])
    for b in range(4):
        l_iso = r"$\mathrm{AR}=1$ (isotropic)" if b == 0 else None
        l_an = r"$\mathrm{AR}=10,\ \theta=0^\circ$" if b == 0 else None
        ax1.plot(s_full, iso[:, b], "k--", lw=1.4, label=l_iso)
        ax1.plot(s_full, an0[:, b], "-", color=BLUE, lw=1.6, label=l_an)
    for b in range(4):
        l_iso = r"$\mathrm{AR}=1$ (isotropic)" if b == 0 else None
        l_an = r"$\mathrm{AR}=10,\ \theta=45^\circ$" if b == 0 else None
        ax2.plot(s_full, iso[:, b], "k--", lw=1.4, label=l_iso)
        ax2.plot(s_full, an45[:, b], "-", color=RED, lw=1.6, label=l_an)

    ticks = [0, 1, 2, 2 + np.sqrt(2)]
    tl = [r"$\Gamma$", r"$X$", r"$M$", r"$\Gamma$"]
    for ax, title in zip([ax1, ax2],
                         [r"(a) Isotropic vs $\mathrm{AR}=10$, $\theta=0^\circ$",
                          r"(b) Isotropic vs $\mathrm{AR}=10$, $\theta=45^\circ$"]):
        ax.set_xticks(ticks)
        ax.set_xticklabels(tl)
        for t in ticks:
            ax.axvline(t, color="0.5", ls=":", lw=0.7, zorder=0)
        panel(ax, title)
        ax.set_xlabel("Wave vector path")
        ax.set_xlim(0, 2 + np.sqrt(2))
        ax.set_ylim(bottom=0)
        grid(ax)
        legend(ax, loc="upper left", fontsize=8, framealpha=0.7)
        spine_frame(ax)
    ax1.set_ylabel(r"Non-dimensional frequency $\bar{\omega}$")

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig06_caseH_dispersion.pdf"))
    plt.close(fig)
    print("Generated fig06_caseH_dispersion.pdf")


if __name__ == "__main__":
    main()
