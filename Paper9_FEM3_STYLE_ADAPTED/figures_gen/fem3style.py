"""Shared FEM_3 graphical language for the Paper9_FEM3_STYLE_ADAPTED figures.

FEM_3 figure conventions (extracted from the MATLAB R2020a EPS sources of the
reference paper BFS_FEM3_main_AUDITED_FINAL.tex):
  * Times-family serif for ALL text and mathematics (STIX is the bundled,
    Times-metric-compatible matplotlib family; mathtext.fontset='stix' makes
    Greek/labels render in Times style),
  * single-column aspect ratio (wide, flat two-panel figures),
  * closed "box" axes with a thin frame,
  * soft dashed gray major-grid only,
  * solid/dashed curve distinction, modest marker size, thin legend box with a
    gray edge and white background,
  * restrained dark palette (black/gray + blue/red/green/orange accents).

Only the presentation layer lives here.  Every script that imports this module
must reproduce the authoritative data-extraction logic and numeric values
byte-for-byte from the original figure generator in
PROGRAM/paper9/figures/gen/.
"""
import matplotlib
import matplotlib.pyplot as plt

# FEM_3-consistent dark palette (restrained; no web-grade saturation).
BLUE = "#1f77b4"
RED = "#d62728"
GREEN = "#2ca02c"
ORANGE = "#ff7f0e"
PURPLE = "#9467bd"
GRAY = "0.45"
GRIDGRAY = "0.872"


def apply():
    matplotlib.rcParams.update({
        "font.family": "STIXGeneral",
        "mathtext.fontset": "stix",
        "font.size": 11,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "lines.linewidth": 1.5,
        "lines.markersize": 5,
        "lines.markeredgewidth": 0.8,
        "legend.frameon": True,
        "legend.framealpha": 1.0,
        "legend.edgecolor": "0.55",
        "legend.fancybox": False,
        "legend.borderaxespad": 0.6,
        "legend.handlelength": 1.8,
        "legend.handletextpad": 0.5,
        "legend.columnspacing": 1.0,
        "axes.grid": False,
        "figure.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def grid(ax, which="major"):
    """FEM_3 style: soft short-dash gray major grid behind the data."""
    ax.grid(True, which=which, ls=(0, (4, 3)), color=GRIDGRAY, lw=0.5, zorder=0)
    ax.set_axisbelow(True)


def legend(ax, **kwargs):
    kwargs.setdefault("frameon", True)
    kwargs.setdefault("framealpha", 1.0)
    kwargs.setdefault("edgecolor", "0.55")
    kwargs.setdefault("fancybox", False)
    kwargs.setdefault("fontsize", 9)
    leg = ax.legend(**kwargs)
    leg.get_frame().set_linewidth(0.6)
    return leg


def panel(ax, title):
    """Set a Times-style (a)/(b) panel title left-inline with the figure."""
    ax.set_title(title, fontsize=11, pad=6)


def spine_frame(ax):
    for s in ax.spines.values():
        s.set_linewidth(0.8)
