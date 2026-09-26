#!/usr/bin/env python3
"""Figure 3 (FEM_3-style): BFS 32-DOF element and Bloch boundary coupling.

Geometry/labels verbatim from PROGRAM/paper9/figures/gen/fig03_bfs_dof_bloch.py;
FEM_3 presentation layer only.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fem3style import apply, legend, panel

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    # --- Panel (a) ---
    ax1.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], "k-", lw=1.4)
    nodes = [(0, 0), (1, 0), (1, 1), (0, 1)]
    labels = ["Node 0\n(0,0)", "Node 1\n(L,0)", "Node 2\n(L,L)", "Node 3\n(0,L)"]
    for (nx, ny), lbl in zip(nodes, labels):
        ax1.scatter(nx, ny, color="black", s=28, zorder=5)
        ha = "right" if nx == 0 else "left"
        va = "top" if ny == 0 else "bottom"
        ox = -0.06 if nx == 0 else 0.06
        oy = -0.06 if ny == 0 else 0.06
        ax1.text(nx + ox, ny + oy, lbl, fontsize=8, ha=ha, va=va, fontweight="bold")
    ax1.text(0.5, 0.5,
             "BFS bicubic Hermite\n4 nodes $\u00d7$ 8 DOFs\n= 32 DOFs / cell\n$C^1$-conforming",
             ha="center", va="center", fontsize=8.5,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="0.97", edgecolor="0.35", lw=0.8))
    ax1.set_xlim(-0.35, 1.35)
    ax1.set_ylim(-0.35, 1.35)
    ax1.set_aspect("equal")
    panel(ax1, "(a) BFS Hermite element DOFs")
    ax1.axis("off")

    # --- Panel (b) ---
    ax2.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], "k-", lw=1.4)
    ax2.annotate("", xy=(1.0, 0.5), xytext=(0.0, 0.5),
                 arrowprops=dict(arrowstyle="->", color="0.25", lw=1.6, shrinkA=5, shrinkB=5))
    ax2.text(0.5, 0.55, r"$\mu_x = e^{\mathrm{i} k_x L}$ on all 4 DOF types",
             ha="center", va="bottom", fontsize=8.5)
    ax2.annotate("", xy=(0.5, 1.0), xytext=(0.5, 0.0),
                 arrowprops=dict(arrowstyle="->", color="0.25", lw=1.6, shrinkA=5, shrinkB=5))
    ax2.text(0.52, 0.25, r"$\mu_y = e^{\mathrm{i} k_y L}$ on all DOFs",
             ha="left", va="center", fontsize=8.5)
    ax2.scatter(0, 0, color="black", s=40, zorder=6, label="Retained master DOFs (Node 0, 8 DOFs)")
    ax2.scatter([1, 1, 0], [0, 1, 1], color="none", edgecolors="0.4", s=30, zorder=5,
                label="Slave boundary DOFs (24 DOFs)")
    ax2.set_xlim(-0.35, 1.35)
    ax2.set_ylim(-0.35, 1.35)
    ax2.set_aspect("equal")
    panel(ax2, "(b) Bloch boundary coupling")
    ax2.axis("off")
    legend(ax2, loc="lower center", fontsize=8)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig03_bfs_dof_bloch.pdf"))
    plt.close(fig)
    print("Generated fig03_bfs_dof_bloch.pdf")


if __name__ == "__main__":
    main()
