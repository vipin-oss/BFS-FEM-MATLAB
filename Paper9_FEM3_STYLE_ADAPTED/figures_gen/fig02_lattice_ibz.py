#!/usr/bin/env python3
"""Figure 2 (FEM_3-style): direct lattice cell and Brillouin zone / IBZ.

Data logic verbatim from PROGRAM/paper9/figures/gen/fig02_lattice_ibz.py.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, grid, legend, panel, spine_frame

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    with open(os.path.join(DATA, "params", "params_master.yaml")) as f:
        cfg = yaml.safe_load(f)["parameters"]
    L = cfg["Lcell"]["value"]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5), sharey=False)

    # --- Panel (a): direct space unit cell ---
    ax1.plot([0, L, L, 0, 0], [0, 0, L, L, 0], "k-", lw=1.5, label=r"Unit cell $\Omega_0$")
    ax1.scatter([0, L, L, 0], [0, 0, L, L], color="black", s=22, zorder=5, label="Lattice nodes")
    ax1.quiver(0, 0, L, 0, angles="xy", scale_units="xy", scale=1, color="black", width=0.010)
    ax1.quiver(0, 0, 0, L, angles="xy", scale_units="xy", scale=1, color="black", width=0.010)
    ax1.text(L / 2, -0.12 * L, r"$\mathbf{a}_1 = (L,0)$", ha="center", va="top", fontsize=9)
    ax1.text(-0.08 * L, L / 2, r"$\mathbf{a}_2 = (0,L)$", ha="right", va="center", fontsize=9)
    ax1.set_xlim(-0.25 * L, 1.25 * L)
    ax1.set_ylim(-0.25 * L, 1.25 * L)
    ax1.set_aspect("equal")
    panel(ax1, "(a) Direct space unit cell")
    ax1.set_xlabel(r"$x_1$ [m]")
    ax1.set_ylabel(r"$x_2$ [m]")
    grid(ax1)
    legend(ax1, loc="upper left")

    # --- Panel (b): reciprocal space BZ and IBZ ---
    q = np.pi / L
    ax2.plot([-q, q, q, -q, -q], [-q, -q, q, q, -q], "k--", lw=1.3, label="First BZ")
    ax2.fill([0, q, q, 0], [-q, -q, q, q], color="#1f77b4", alpha=0.15, label="Anisotropic IBZ (half-BZ)")
    ax2.fill([0, q, q], [0, 0, q], color="#ff7f0e", alpha=0.25, label="Isotropic IBZ (1/8 BZ)")
    pk = np.array([[0, 0], [q, 0], [q, q], [0, 0]])
    ax2.plot(pk[:, 0], pk[:, 1], "r-", lw=2.0, label=r"Path $\Gamma \to X \to M \to \Gamma$")
    for name, (px, py) in {r"$\Gamma$": (0, 0), r"$X$": (q, 0), r"$M$": (q, q), r"$Y$": (0, q)}.items():
        ax2.scatter(px, py, color="darkred", s=20, zorder=6)
        off = (0.08 * q, 0.08 * q) if name != r"$Y$" else (-0.15 * q, 0.08 * q)
        ax2.text(px + off[0], py + off[1], name, fontsize=10, fontweight="bold", color="darkred")
    ax2.set_xlim(-1.25 * q, 1.25 * q)
    ax2.set_ylim(-1.25 * q, 1.25 * q)
    ax2.set_aspect("equal")
    panel(ax2, "(b) Reciprocal space & symmetry path")
    ax2.set_xlabel(r"$k_x$ [rad/m]")
    ax2.set_ylabel(r"$k_y$ [rad/m]")
    grid(ax2)
    legend(ax2, loc="lower left")
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig02_lattice_ibz.pdf"))
    plt.close(fig)
    print("Generated fig02_lattice_ibz.pdf")


if __name__ == "__main__":
    main()
