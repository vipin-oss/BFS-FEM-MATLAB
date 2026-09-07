"""Journal figure style for Research Paper 1 (single visual language).

Imported by make_all_figures.py.  Paths resolve relative to the package root
so the package runs from any clean extraction directory.
"""
"""Figure redesign (Task 14) — journal-quality scientific visualization.

Reads ONLY the accepted raw data (study1_surface_waves/results, read-only).
No new simulations, no smoothing, no deletion.  Captions live in TEX only;
images contain axes, ticks, legends, panel letters and short scientific
annotations only.

Visual language (consistent paper-wide):
  model identity  : A=#D55E00 solid, B=#0072B2 dashed, C=#009E73 dash-dot
  D_w* level      : 1e-2=#E69F00, 1e0=#56B4E9, 1e2=#CC79A7, 1e4=#808080
  tau0* level     : viridis ramp (5 values)
  maps / surfaces : viridis (perceptual, not rainbow)
Grayscale-safe: models differ by line style, D_w levels by colour+context.
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from pathlib import Path
PKG = Path(__file__).resolve().parents[1]
RES = str(PKG / "results" / "raw")
OUT = str(PKG / "figures" / "output")

CA, CB, CC = "#D55E00", "#0072B2", "#009E73"
SM, SB, SC = "-", "--", "-."
DWCOL = {1e-2: "#E69F00", 1e0: "#56B4E9", 1e2: "#CC79A7", 1e4: "#808080"}
TAUCOL = [plt.cm.viridis(t) for t in (0.12, 0.32, 0.52, 0.72, 0.92)]

plt.rcParams.update({
    "font.family": "serif", "font.size": 8.5, "mathtext.fontset": "dejavuserif",
    "axes.linewidth": 0.7, "axes.grid": True, "grid.alpha": 0.22,
    "grid.linewidth": 0.45, "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "xtick.major.size": 2.6, "ytick.major.size": 2.6,
    "legend.frameon": False, "legend.fontsize": 7.2, "legend.handlelength": 2.2,
    "lines.linewidth": 1.15, "figure.dpi": 150, "savefig.bbox": "tight",
    "axes.labelsize": 9.0, "axes.titlesize": 9.0,
})

def read_csv(name):
    with open(os.path.join(RES, name)) as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines))

def farr(rows, key):
    return np.array([float(r[key]) if r[key] not in ("", "NaN") else np.nan
                     for r in rows])

def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name), format="pdf")
    plt.close(fig); print("wrote", name)

def panel(ax, lab):
    ax.text(-0.02, 1.04, lab, transform=ax.transAxes, fontsize=10,
            fontweight="bold", va="bottom")

def eps_delta():
    return float(read_csv("resolution_bench.csv")[0]["eps_Delta"])

def floor_rel():
    return eps_delta() / 0.4663

