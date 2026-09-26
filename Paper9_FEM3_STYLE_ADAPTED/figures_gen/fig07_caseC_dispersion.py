#!/usr/bin/env python3
"""Figure 7 (FEM_3-style): Case C phononic crystal dispersion and gap tuning.

Data pipeline verbatim from paper9/figures/gen/fig07_caseC_dispersion.py.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, grid, legend, panel, spine_frame, BLUE, RED, GREEN

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")

PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b"]


def main():
    with open(os.path.join(DATA, "results/raw/p11_caseC_raw.json")) as f:
        data = json.load(f)

    baseline = data["baseline"]
    s_full = np.array(baseline["s_norm"])
    path_bands = np.array(baseline["path_bands"])
    gap_34 = baseline["gaps"][2]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    for b in range(6):
        ax1.plot(s_full, path_bands[:, b], color=PALETTE[b % len(PALETTE)], lw=1.4,
                 label="Band %d" % (b + 1))
    w_low = gap_34["omega_lower_max"]
    w_upp = gap_34["omega_upper_min"]
    ax1.axhspan(w_low, w_upp, color="0.80", alpha=0.5, hatch="//",
                label="Complete gap (%.2f-%.2f)" % (w_low, w_upp))
    ticks = [0, 1, 2, 2 + np.sqrt(2)]
    ax1.set_xticks(ticks)
    ax1.set_xticklabels([r"$\Gamma$", r"$X$", r"$M$", r"$\Gamma$"])
    ax1.set_xlim([0, 2 + np.sqrt(2)])
    ax1.set_ylim([0, 9.0])
    ax1.set_xlabel(r"Wave vector $\mathbf{k}$")
    ax1.set_ylabel(r"Normalized frequency $\bar{\omega} = \omega L/(\pi c_t)$")
    panel(ax1, r"(a) Case C baseline dispersion ($r_0/a = 0.30$)")
    grid(ax1)
    legend(ax1, loc="upper right", fontsize=7, framealpha=0.7, outside=True)

    r_sweep = data["radius_sweep"]
    radii, w_lows, w_upps, widths = [], [], [], []
    for v in sorted(r_sweep.values(), key=lambda item: item["r0"]):
        radii.append(v["r0"])
        g = v["gap_34"]
        w_lows.append(g["omega_lower_max"])
        w_upps.append(g["omega_upper_min"])
        widths.append(g["delta_complete"])
    radii = np.array(radii)
    w_lows = np.array(w_lows)
    w_upps = np.array(w_upps)
    widths = np.array(widths)

    ax2.fill_between(radii, w_lows, w_upps, color="0.80", alpha=0.5, hatch="//",
                     label="Complete gap region")
    ax2.plot(radii, w_lows, "o-", color=BLUE, ms=4, lw=1.4, label="Lower edge (Band 3)")
    ax2.plot(radii, w_upps, "s-", color=RED, ms=4, lw=1.4, label="Upper edge (Band 4)")
    ax2t = ax2.twinx()
    ax2t.plot(radii, widths, "^--", color=GREEN, ms=4, lw=1.4,
              label=r"Gap width $\Delta_{\mathrm{complete}}$")
    ax2t.set_ylabel(r"Gap width $\Delta_{\mathrm{complete}}$", color=GREEN)
    ax2t.set_ylim([0, 3.5])
    ax2.set_xlabel(r"Inclusion radius ratio $r_0/a$")
    ax2.set_ylabel(r"Normalized frequency $\bar{\omega}$")
    panel(ax2, "(b) Band gap tuning with inclusion size")
    ax2.set_xlim([0.18, 0.42])
    ax2.set_ylim([3.0, 8.5])
    grid(ax2)
    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2t.get_legend_handles_labels()
    legend(ax2, handles=h1 + h2, labels=l1 + l2, loc="upper left", fontsize=7, outside=True)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig07_caseC_dispersion.pdf"))
    plt.close(fig)
    print("Generated fig07_caseC_dispersion.pdf")


if __name__ == "__main__":
    main()
