#!/usr/bin/env python3
"""Figure 13 (FEM_3-style): energy partition and micro-inertia admissibility.

Data pipeline verbatim from fig13_energy_microinertia.py.
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
        d = json.load(f)
    s8 = d["study_S8_energy_flux"]
    s9 = d["study_S9_microinertia"]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    k_s8 = [it["kbar"] for it in s8]
    Wg = [it["Wg_over_W_major"] * 100 for it in s8]
    Tg = [it["Tg_over_T"] * 100 for it in s8]
    ax1.plot(k_s8, Wg, "o-", color="#1f77b4", lw=1.4, ms=4,
             label=r"Gradient strain energy $\langle W_g\rangle/\langle W\rangle$")
    ax1.plot(k_s8, Tg, "s--", color="#d62728", lw=1.4, ms=4,
             label=r"Micro-inertia kinetic $\langle T_g\rangle/\langle T\rangle$")
    ax1.set_xlabel(r"Non-dimensional wavenumber $\bar{k} = kL/\pi$")
    ax1.set_ylabel("Energy fraction [\\%]")
    panel(ax1, "(a) Energy partition vs wavenumber")
    ax1.set_xlim(0, 1.05)
    ax1.set_ylim(bottom=0)
    grid(ax1)
    legend(ax1, loc="upper left", fontsize=8)

    k_s9 = [it["kbar"] for it in s9]
    vp_b = [it["vp_ell_pos"] for it in s9]
    vp_u = [it["vp_ell_zero"] for it in s9]
    vinf = s9[0]["vinf_theory"]
    ax2.loglog(k_s9, vp_b, "o-", color="#2ca02c", lw=1.4, ms=4,
               label=r"$\bar{\ell}=0.20>0$ (bounded)")
    ax2.loglog(k_s9, vp_u, "^--", color="#d62728", lw=1.4, ms=4,
               label=r"$\bar{\ell}=0$ (unbounded, $\propto\bar{k}$)")
    ax2.axhline(vinf, color="darkgreen", ls=":", lw=1.3,
                label=r"Theoretical $v_{T,\infty}=%.4f$" % vinf)
    ax2.set_xlabel(r"Wavenumber $\bar{k} = kL/\pi$")
    ax2.set_ylabel(r"Phase velocity $\bar{v}_p = \bar{\omega}/(\pi\bar{k})$")
    panel(ax2, r"(b) Micro-inertia high-$k$ admissibility")
    grid(ax2, "both")
    legend(ax2, loc="upper left", fontsize=8, framealpha=0.7)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig13_energy_microinertia.pdf"))
    plt.close(fig)
    print("Generated fig13_energy_microinertia.pdf")


if __name__ == "__main__":
    main()
