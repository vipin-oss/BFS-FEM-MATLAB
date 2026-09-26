#!/usr/bin/env python3
"""Figure 14 (FEM_3-style): orientation sweep of the S7 steering pattern.

Data pipeline verbatim from fig14_s7_steering_sweep.py
(p12b_s7_theta_sweep_mesh16.json).
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
    with open(os.path.join(DATA, "results/raw/p12b_s7_theta_sweep_mesh16.json")) as f:
        d = json.load(f)
    sw = d["sweep"]
    ths = [0, 15, 30, 45, 60, 75, 90]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.5))

    d5 = [sw["AR_5_th_%d" % t]["delta_max_deg"] for t in ths]
    d10 = [sw["AR_10_th_%d" % t]["delta_max_deg"] for t in ths]
    p5 = [sw["AR_5_th_%d" % t]["phi_star_deg"] for t in ths]
    p10 = [sw["AR_10_th_%d" % t]["phi_star_deg"] for t in ths]

    ax1.plot(ths, d5, "o-", color="#1f77b4", lw=1.4, ms=4, label=r"$\delta_{\max}$, AR=5")
    ax1.plot(ths, d10, "s-", color="#d62728", lw=1.4, ms=4, label=r"$\delta_{\max}$, AR=10")
    ax1.set_xlabel(r"Microstructure orientation $\theta$ [deg]")
    ax1.set_ylabel(r"Max. steering deviation $\delta_{\max}$ [deg]")
    ax1.set_xticks(ths)
    grid(ax1)
    legend(ax1, loc="lower left", fontsize=8, framealpha=0.7)

    ax1b = ax1.twinx()
    ax1b.plot(ths, p5, "o--", color="#1f77b4", mfc="none", lw=1.0, ms=4, label=r"$\phi^*$, AR=5")
    ax1b.plot(ths, p10, "s--", color="#d62728", mfc="none", lw=1.0, ms=4, label=r"$\phi^*$, AR=10")
    ax1b.set_ylabel(r"Principal steering axis $\phi^*$ [deg] (mod $90^\circ$)")
    ax1b.set_ylim(-5, 95)
    legend(ax1b, loc="lower right", fontsize=8, framealpha=0.7)
    panel(ax1, r"(a) Steering strength & axis vs $\theta$")
    ax1.set_xlim(-4, 94)

    ph = np.array(sw["AR_10_th_0"]["phi_deg"])
    d0 = np.array(sw["AR_10_th_0"]["delta_deg"])
    d90 = np.array(sw["AR_10_th_90"]["delta_deg"])
    idx = (18 - np.arange(len(ph))) % 72
    d90_m = d90[idx]
    keep = ph <= 180.0
    ax2.plot(ph[keep], d0[keep], "-", color="#d62728", lw=1.6,
             label=r"$\delta(\phi;\ \theta=0^\circ)$, AR=10")
    ax2.plot(ph[keep][::2], d90_m[keep][::2], "o", color="#1f77b4", ms=4,
             mfc="none", mew=1.0, label=r"$\delta(90^\circ-\phi;\ \theta=90^\circ)$, AR=10")
    ax2.set_xlabel(r"Propagation angle $\phi$ on ring $|\bar{k}|=0.5$ [deg]")
    ax2.set_ylabel(r"Deviation $\delta$ [deg]")
    ax2.set_xlim(0, 180)
    ax2.set_xticks([0, 30, 60, 90, 120, 150, 180])
    grid(ax2)
    legend(ax2, loc="lower right", fontsize=8, framealpha=0.7)
    panel(ax2, r"(b) Mirror co-symmetry of $\delta(\phi)$, AR=10")

    fig.tight_layout(w_pad=2.2)
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig14_s7_steering_sweep.pdf"))
    plt.close(fig)
    print("Generated fig14_s7_steering_sweep.pdf")


if __name__ == "__main__":
    main()
