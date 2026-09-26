#!/usr/bin/env python3
"""Figure 12 (FEM_3-style): wave-vector steering and group velocity deviation.

Data pipeline verbatim from fig12_ifc_wave_steering.py.
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
        data = json.load(f)["study_S7_ifc_steering"]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    cases = [
        ("AR_1_th_0", r"$\mathrm{AR}=1$ (isotropic)", "k--", 1.3),
        ("AR_5_th_45", r"$\mathrm{AR}=5$, $\theta=45^\circ$", "#2ca02c", 1.6),
        ("AR_10_th_45", r"$\mathrm{AR}=10$, $\theta=45^\circ$", "#d62728", 1.6),
    ]
    for key, lbl, style, lw in cases:
        c = data[key]
        phi = np.array(c["phi_deg"])
        delta = np.array(c["delta_deg"])
        d_max = c["delta_max_deg"]
        ax1.plot(phi, delta, style, lw=lw,
                 label=r"%s ($\delta_{\max}=%.2f^\circ$)" % (lbl, d_max))
    ax1.set_xlabel(r"Wave vector direction $\phi$ [deg]")
    ax1.set_ylabel(r"Steering angle $\delta = \angle\mathbf{v}_g - \angle\mathbf{k}$ [deg]")
    panel(ax1, r"(a) Steering deviation $\delta(\phi)$ at $\bar{k}=0.5$")
    ax1.set_xlim(0, 90)
    ax1.set_xticks([0, 15, 30, 45, 60, 75, 90])
    grid(ax1)
    legend(ax1, loc="lower left", fontsize=8)

    for key, lbl, style, lw in cases[:-1]:
        c = data[key]
        phi = np.array(c["phi_deg"])
        vg = np.array(c["vg_mag"])
        ax2.plot(phi, vg, style, lw=lw, label=lbl)
    c = data[cases[-1][0]]
    ax2.plot(np.array(c["phi_deg"]), np.array(c["vg_mag"]), cases[-1][2],
             lw=cases[-1][3], label=cases[-1][1])
    ax2.set_xlabel(r"Wave vector direction $\phi$ [deg]")
    ax2.set_ylabel(r"Group velocity magnitude $|\mathbf{v}_g|$")
    panel(ax2, r"(b) Group velocity magnitude at $\bar{k}=0.5$")
    ax2.set_xlim(0, 90)
    ax2.set_xticks([0, 15, 30, 45, 60, 75, 90])
    grid(ax2)
    legend(ax2, loc="upper right", fontsize=8)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig12_ifc_wave_steering.pdf"))
    plt.close(fig)
    print("Generated fig12_ifc_wave_steering.pdf")


if __name__ == "__main__":
    main()
