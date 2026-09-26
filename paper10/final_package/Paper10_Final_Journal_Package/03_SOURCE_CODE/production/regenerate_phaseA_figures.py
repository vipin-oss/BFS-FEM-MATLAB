#!/usr/bin/env python3
"""
Phase-A Figure Regeneration (dispersion diagrams)
=================================================
Regenerates the branch-dot dispersion figures (fig1_baseline_dispersion,
fig3_material_contrast, fig5_filling_fraction, fig8_combined_interaction)
from the FROZEN production datasets using the Phase-A corrected mode
classification:

  propagating      : kr/pi > 0.01 and alpha_a < 0.05  -> solid colored points
  evanescent/complex: otherwise                        -> faint grey points

This removes the vertical band of near-zero-kr evanescent modes that the
former per-branch_id plotting mixed indiscriminately with the propagating
spectrum.  No solver re-run is performed; only archived CSVs are read.
"""

import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.abspath(os.path.dirname(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(PKG, "04_PRODUCTION_DATA")
FIGS = os.path.join(PKG, "02_FIGURES")

plt.rcParams.update({
    "font.size": 10, "axes.labelsize": 11, "axes.titlesize": 11,
    "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 8,
    "figure.dpi": 300,
})

ALPHA_PASS = 0.05
KR_MIN = 0.01


def load(fname):
    with open(os.path.join(DATA, fname)) as f:
        return list(csv.DictReader(f))


def plot_classified(ax, recs, color):
    prop = [r for r in recs if float(r["kr_a_over_pi"]) > KR_MIN and float(r["alpha_a"]) < ALPHA_PASS]
    evan = [r for r in recs if r not in prop]
    if evan:
        ax.plot([float(r["kr_a_over_pi"]) for r in evan], [float(r["Omega"]) for r in evan],
                ".", color="0.75", ms=2.5, alpha=0.55, zorder=1)
    if prop:
        ax.plot([float(r["kr_a_over_pi"]) for r in prop], [float(r["Omega"]) for r in prop],
                ".", color=color, ms=3, zorder=2)


def add_legend(ax, color):
    ax.plot([], [], ".", color=color, label="propagating modes")
    ax.plot([], [], ".", color="0.75", label="evanescent / complex-$k$")
    ax.legend(loc="upper left", fontsize=8, frameon=False)


def main():
    rec_s1 = load("S1_results.csv")
    rec_s2 = load("S2_results.csv")
    rec_s4 = load("S4_results.csv")
    rec_s7 = load("S7_results.csv")
    print("Frozen CSVs loaded.")

    # ---- Figure 1 (manuscript Fig. 3): baseline dispersion, S1 --------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    plot_classified(ax1, [r for r in rec_s1 if r["case_id"] == "S1_cons"], "b")
    plot_classified(ax2, [r for r in rec_s1 if r["case_id"] == "S1_dpl"], "r")
    add_legend(ax1, "b")
    add_legend(ax2, "r")
    ax1.set_title(r"(a) Conservative Baseline ($\beta \to 0$)", fontsize=11)
    ax1.set_xlabel(r"Real Bloch Wavenumber $k_r a / \pi$")
    ax1.set_ylabel(r"Normalized Frequency $\Omega = \omega a / (2\pi v_m)$")
    ax1.set_xlim([0.0, 1.0])
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax2.set_title("(b) Active DPL Thermoelastic Baseline", fontsize=11)
    ax2.set_xlabel(r"Real Bloch Wavenumber $k_r a / \pi$")
    ax2.set_xlim([0.0, 1.0])
    ax2.grid(True, linestyle="--", alpha=0.6)
    fig.suptitle("Baseline Bloch Dispersion across the First Brillouin Zone "
                 "(propagating vs. evanescent modes classified)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig1_baseline_dispersion.png"))
    plt.close(fig)
    print("  saved fig1_baseline_dispersion.png")

    # ---- Figure 3 (manuscript Fig. 5): material contrast, S2 ----------------
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    for (cid, title, ax) in [
        ("S2_chi00_cons", r"(a) Identical Layers ($\chi=0.0$)", axes[0]),
        ("S2_chi05_cons", r"(b) Intermediate Contrast ($\chi=0.5$)", axes[1]),
        ("S2_chi10_cons", r"(c) Full Contrast ($\chi=1.0$)", axes[2]),
    ]:
        plot_classified(ax, [r for r in rec_s2 if r["case_id"] == cid], "k")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel(r"$k_r a / \pi$")
        ax.set_xlim([0.0, 1.0])
        ax.grid(True, linestyle="--", alpha=0.6)
    axes[0].set_ylabel(r"Normalized Frequency $\Omega$")
    fig.suptitle("Material Contrast Sweep — Emergence and Evolution of Bragg Band Gaps", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig3_material_contrast.png"))
    plt.close(fig)
    print("  saved fig3_material_contrast.png")

    # ---- Figure 5 (manuscript Fig. 7): filling fraction, S4 -----------------
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    for (cid, title, ax) in [
        ("S4_eta02_cons", r"(a) Asymmetric Thin ($\eta=0.2$)", axes[0]),
        ("S4_eta05_cons", r"(b) Symmetric Baseline ($\eta=0.5$)", axes[1]),
        ("S4_eta08_cons", r"(c) Asymmetric Thick ($\eta=0.8$)", axes[2]),
    ]:
        plot_classified(ax, [r for r in rec_s4 if r["case_id"] == cid], "b")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel(r"$k_r a / \pi$")
        ax.set_xlim([0.0, 1.0])
        ax.grid(True, linestyle="--", alpha=0.6)
    axes[0].set_ylabel(r"Normalized Frequency $\Omega$")
    fig.suptitle(r"Layer Thickness Ratio ($\eta = a_1/a$) Effect on Bragg Band-Edge Frequencies", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig5_filling_fraction.png"))
    plt.close(fig)
    print("  saved fig5_filling_fraction.png")

    # ---- Figure 8 (manuscript Fig. 10): factorial interaction, S7 -----------
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.5), sharex=True, sharey=True)
    s7_cases = [
        ("S7_case1", "Case I: Pure Mechanical Bragg", "b"),
        ("S7_case2", "Case II: Active DPL Baseline", "r"),
        ("S7_case3", "Case III: Low Gradient + DPL", "g"),
        ("S7_case4", "Case IV: High Gradient + DPL", "m"),
        ("S7_case5", "Case V: Asymmetric Geometry + DPL", "orange"),
        ("S7_case6", "Case VI: High Thermal Lag + DPL", "purple"),
    ]
    for (cid, title, col), ax in zip(s7_cases, axes.flatten()):
        plot_classified(ax, [r for r in rec_s7 if r["case_id"] == cid], col)
        ax.set_title(title, fontsize=10)
        ax.set_xlim([0.0, 1.0])
        ax.grid(True, linestyle="--", alpha=0.6)
    axes[0, 0].set_ylabel(r"Normalized Frequency $\Omega$")
    axes[1, 0].set_ylabel(r"Normalized Frequency $\Omega$")
    for ax in axes[1, :]:
        ax.set_xlabel(r"Real Bloch Wavenumber $k_r a / \pi$")
    fig.suptitle("Combined Parameter Interaction — Factorial Comparison "
                 "(propagating vs. evanescent modes classified)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig8_combined_interaction.png"))
    plt.close(fig)
    print("  saved fig8_combined_interaction.png")


if __name__ == "__main__":
    main()
