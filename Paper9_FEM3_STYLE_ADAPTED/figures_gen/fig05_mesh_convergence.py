#!/usr/bin/env python3
"""Figure 5 (FEM_3-style): mesh convergence, observed rate, resolution floor.

Data pipeline verbatim from paper9/figures/gen/fig05_mesh_convergence.py
(Rule R-fit, p4b_5g_to_5i.json + rule_rfit_governing.json).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from fem3style import apply, grid, legend, panel, spine_frame, BLUE, RED

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(PKG, "PROGRAM", "paper9")
OUT = os.path.join(PKG, "OVERLEAF", "figures")


def main():
    with open(os.path.join(DATA, "verification/suite/p4b_5g_to_5i.json")) as f:
        data = json.load(f)["5i"]
    with open(os.path.join(DATA, "audit/evidence/p12h/rule_rfit_governing.json")) as f:
        rule = json.load(f)
    F = rule["rule"]["F"]
    spread_floor = rule["rule"]["spread_floor"]
    spreads = np.array([max(s if s is not None else spread_floor, spread_floor)
                        for s in rule["reproducibility_inputs"]["governing_era"]["spreads"]])
    ratios = np.array(data["rel_err"]) / spreads
    in_fit = ratios > F

    meshes = np.array(data["meshes"])
    h_vals = 1.0 / meshes
    rel_err = np.array(data["rel_err"])
    slope = data["slope"]
    ci95 = data["CI95"]
    eps_Delta = data["eps_Delta"]

    apply()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5))

    # Panel (a): log-log convergence
    h_in, e_in = h_vals[in_fit], rel_err[in_fit]
    h_out, e_out = h_vals[~in_fit], rel_err[~in_fit]
    ax1.loglog(h_in, e_in, "o-", color=BLUE, lw=1.5, ms=5,
               label=f"FE error, in rate fit ({len(h_in)} levels)")
    if len(h_out):
        ax1.loglog(h_out, e_out, "s", mfc="white", mec=RED, mew=1.3, ms=6.5,
                   label=f"Resolution-limited ({len(h_out)} level, excluded)")
    h_fit = np.logspace(np.log10(h_in.min()), np.log10(h_in.max()), 50)
    err_fit = e_in[0] * (h_fit / h_in[0]) ** slope
    ax1.loglog(h_fit, err_fit, "k--", lw=1.2,
               label=rf"Empirical fit: $p = {slope:.2f}$ ($95\%$ CI: $[{ci95[0]:.2f}, {ci95[1]:.2f}]$)")
    ax1.axhline(eps_Delta, color="crimson", ls=":", lw=1.3,
                label=rf"Operational floor $\varepsilon_\Delta = {eps_Delta:.2e}$")
    ax1.axhline(float(spreads.max()), color="0.45", ls="-.", lw=1.0,
                label=rf"Measurement resolution (max $s_i$) $= {float(spreads.max()):.1e}$")
    ax1.set_xlabel(r"Element size $h = L/N$ [m]")
    ax1.set_ylabel(r"Relative error $|\omega_T - \omega_{\mathrm{exact}}|/\omega_{\mathrm{exact}}$")
    panel(ax1, "(a) Eigenvalue convergence (Case H)")
    grid(ax1, "both")
    legend(ax1, loc="lower right", fontsize=8, framealpha=0.7, outside=True)

    # Panel (b): stepwise mesh variation
    diff_meshes = [rf"${meshes[i]}^2 \to {meshes[i + 1]}^2$" for i in range(len(meshes) - 1)]
    rel_diffs = [abs(data["omega"][i + 1] - data["omega"][i]) / data["omega"][i + 1]
                 for i in range(len(meshes) - 1)]
    bars = ax2.bar(diff_meshes, rel_diffs,
                   color=["0.68", "0.80", "white"],
                   edgecolor=["0.25", "0.25", RED], width=0.55)
    bars[-1].set_hatch("//")
    ax2.axhline(eps_Delta, color="crimson", ls=":", lw=1.3)
    ax2.set_yscale("log")
    ax2.set_xlabel("Mesh refinement step")
    ax2.set_ylabel(r"Relative change $|\Delta\omega|/\omega$")
    panel(ax2, "(b) Stepwise mesh variation")
    grid(ax2, "both")
    legend(ax2, handles=[
        Patch(facecolor="white", edgecolor=RED, hatch="//",
              label="resolution-limited step (excluded from rate fit)"),
        Patch(facecolor="none", edgecolor="crimson", ls=":",
              label=rf"Operational floor $\varepsilon_\Delta = {eps_Delta:.2e}$"),
    ], loc="upper right", fontsize=7, framealpha=0.7, outside=True)
    ymax = max(rel_diffs)
    for bar, val in zip(bars, rel_diffs):
        cx = bar.get_x() + bar.get_width() / 2.0
        if val > 0.02 * ymax:
            ax2.text(cx, val * 0.45, f"{val:.1e}", ha="center", va="center",
                     fontsize=7.5, color="white", fontweight="bold")
        else:
            ax2.text(cx, val * 1.6, f"{val:.1e}", ha="center", va="bottom", fontsize=7.5)
    spine_frame(ax1), spine_frame(ax2)

    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "fig05_mesh_convergence.pdf"))
    plt.close(fig)
    print("Generated fig05_mesh_convergence.pdf")


if __name__ == "__main__":
    main()
