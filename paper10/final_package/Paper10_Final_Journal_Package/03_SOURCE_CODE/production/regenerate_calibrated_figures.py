#!/usr/bin/env python3
"""
Regenerates only the audited and calibrated production figures (Figs 2, 4, 6, 7, 9, 10)
from the authoritative Phase 3B datasets without rerunning the full solver sweeps.
"""

import os
import csv
import matplotlib.pyplot as plt

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# Phase-A: fall back to the packaged frozen datasets/figures when the full
# paper10 working tree is not present (self-contained package operation).
if os.path.isdir(os.path.join(repo_root, "paper10", "production", "results")):
    results_dir = os.path.join(repo_root, "paper10", "production", "results")
    figures_dir = os.path.join(repo_root, "paper10", "figures", "phase3b")
else:
    results_dir = os.path.join(repo_root, "04_PRODUCTION_DATA")
    figures_dir = os.path.join(repo_root, "02_FIGURES")
results_dir = os.path.normpath(os.path.abspath(results_dir))
figures_dir = os.path.normpath(os.path.abspath(figures_dir))


def extract_acoustic_branch(records, **kwargs):
    """
    Phase-A rev.2 continuity-constrained acoustic-branch extraction.
    Shared implementation in branch_utils.py; verbatim local fallback below
    keeps this script standalone-capable.
    """
    return _extract_acoustic_branch_impl(records, **kwargs)


try:
    from branch_utils import extract_acoustic_branch as _extract_acoustic_branch_impl
except ImportError:  # pragma: no cover - standalone fallback (verbatim copy)
    def _extract_acoustic_branch_impl(records, alpha_pass=0.05, kr_min=0.01,
                                      kr_max=None, continuity_window=0.15):
        import math as _math
        if kr_max is None:
            kr_max = _math.pi - 0.01
        by_om = {}
        for r in records:
            by_om.setdefault(float(r["Omega"]), []).append(r)
        pts = []
        anchor = None
        for om in sorted(by_om):
            rows = [dict(r) for r in by_om[om]]
            for r in rows:
                kr = float(r["kr_a_over_pi"])
                r["_is_prop"] = (kr > kr_min) and (float(r["alpha_a"]) < alpha_pass) and (kr < kr_max)
            prop = [r for r in rows if r["_is_prop"]]
            if prop:
                if anchor is not None:
                    near = [r for r in prop
                            if abs(float(r["kr_a_over_pi"]) - anchor) <= continuity_window]
                    best = min(near or prop, key=lambda r: float(r["alpha_a"]))
                    best["_hopped"] = not near
                else:
                    best = min(prop, key=lambda r: float(r["alpha_a"]))
                    best["_hopped"] = False
                anchor = float(best["kr_a_over_pi"])
                best["_is_prop"] = True
            else:
                best = min(rows, key=lambda r: float(r["alpha_a"]))
                best["_is_prop"] = False
                best["_hopped"] = False
            pts.append(best)
        return pts


def main():
    plt.rcParams.update({
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9,
        "figure.dpi": 300
    })

    # Load datasets
    with open(os.path.join(results_dir, "S1_results.csv")) as f:
        rec_s1 = list(csv.DictReader(f))
    with open(os.path.join(results_dir, "S3_results.csv")) as f:
        rec_s3 = list(csv.DictReader(f))
    with open(os.path.join(results_dir, "S5_results.csv")) as f:
        rec_s5 = list(csv.DictReader(f))
    with open(os.path.join(results_dir, "S6_results.csv")) as f:
        rec_s6 = list(csv.DictReader(f))
    with open(os.path.join(results_dir, "PRODUCTION_BANDGAP_SUMMARY.csv")) as f:
        bandgap_table = list(csv.DictReader(f))

    # Figure 2: Baseline Attenuation Diagram (S1)  [Phase-A corrected branch]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    b_cons = extract_acoustic_branch([r for r in rec_s1 if r["case_id"] == "S1_cons"])
    b_dpl = extract_acoustic_branch([r for r in rec_s1 if r["case_id"] == "S1_dpl"])
    # Shade documented Bragg stop-band windows (Table 3)
    ax.axvspan(0.6687, 0.7040, color='crimson', alpha=0.10)
    ax.axvspan(1.3051, 1.80, color='crimson', alpha=0.10)
    ax.axvspan(1.5702, 1.6763, color='navy', alpha=0.10)
    for pts, col, lbl, ls in [(b_cons, 'b', r'Conservative Baseline ($\beta \to 0$)', '-'),
                              (b_dpl, 'r', r'Active DPL Thermoelasticity', '--')]:
        prop = [p for p in pts if p["_is_prop"]]
        stop = [p for p in pts if not p["_is_prop"]]
        ax.semilogy([float(p["Omega"]) for p in prop], [max(float(p["alpha_a"]), 1e-12) for p in prop],
                    ls, color=col, lw=1.8, label=lbl)
        if stop:
            ax.semilogy([float(p["Omega"]) for p in stop], [max(float(p["alpha_a"]), 1e-12) for p in stop],
                        'o', mfc='none', color=col, ms=4.5, mew=1.0,
                        label=lbl.split('(')[0].strip() + ' — stop-band (non-propagating)')
    ax.set_xlabel(r'Normalized Frequency $\Omega = \omega a / (2\pi v_m)$')
    ax.set_ylabel(r'Spatial Attenuation Magnitude $\alpha a = |k_i a|$')
    ax.set_title('Figure 2: Calibrated Baseline Spatial Acoustic Attenuation vs Frequency', fontsize=11)
    ax.set_ylim([1e-9, 1e1])
    ax.grid(True, which="both", linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', fontsize=7.5)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "fig2_baseline_attenuation.png"))
    plt.close()
    print("  ✓ Figure 2: Calibrated Baseline Attenuation regenerated.")

    # Figure 4: Dipolar Gradient Length Sweep (S3)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    for cid, col, lbl in [("S3_d01", 'g', r'$d_1/a=0.1$'), ("S3_d05", 'b', r'$d_1/a=0.5$ (base)'), ("S3_d10", 'm', r'$d_1/a=1.0$')]:
        c_pts = extract_acoustic_branch([r for r in rec_s3 if r["case_id"] == cid])
        if c_pts:
            ax1.plot([float(r["kr_a_over_pi"]) for r in c_pts], [float(r["Omega"]) for r in c_pts], color=col, lw=1.8, label=lbl)
    ax1.set_title(r'(a) Micro-Inertia Variation ($d_1/a$)', fontsize=11)
    ax1.set_xlabel(r'$k_r a / \pi$')
    ax1.set_ylabel(r'Normalized Frequency $\Omega$')
    ax1.set_xlim([0.0, 1.0])
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right')

    for cid, col, lbl in [("S3_c01", 'c', r'$\sqrt{c_1}/a=0.1$'), ("S3_c05", 'b', r'$\sqrt{c_1}/a=0.5$ (base)'), ("S3_c08", 'r', r'$\sqrt{c_1}/a=0.8$')]:
        c_pts = extract_acoustic_branch([r for r in rec_s3 if r["case_id"] == cid])
        if c_pts:
            ax2.plot([float(r["kr_a_over_pi"]) for r in c_pts], [float(r["Omega"]) for r in c_pts], color=col, lw=1.8, label=lbl)
    ax2.set_title(r'(b) Micro-Stiffness Variation ($\sqrt{c_1}/a$)', fontsize=11)
    ax2.set_xlabel(r'$k_r a / \pi$')
    ax2.set_xlim([0.0, 1.0])
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='lower right')

    fig.suptitle('Figure 4: Dipolar Gradient-Elastic Length Scale Sensitivity on Acoustic Dispersion', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "fig4_gradient_lengths.png"))
    plt.close()
    print("  ✓ Figure 4: Calibrated Gradient Lengths regenerated.")

    # Figure 6: DPL Thermal-Lag Sweep (S5)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for cid, col, lbl in [("S5_tauq_1ps", 'g', r'$\tau_q = 1\ \mathrm{ps}$'),
                          ("S5_tauq_10ps", 'b', r'$\tau_q = 10\ \mathrm{ps}$ (base)'),
                          ("S5_tauq_1ns", 'r', r'$\tau_q = 1\ \mathrm{ns}$')]:
        c_pts = extract_acoustic_branch([r for r in rec_s5 if r["case_id"] == cid])
        if c_pts:
            ax1.semilogy([float(r["Omega"]) for r in c_pts], [max(float(r["alpha_a"]), 1e-12) for r in c_pts], color=col, lw=1.8, label=lbl)
    ax1.set_title(r'(a) Heat Flux Relaxation Lag $\tau_q$', fontsize=11)
    ax1.set_xlabel(r'Normalized Frequency $\Omega$')
    ax1.set_ylabel(r'Spatial Attenuation Magnitude $\alpha a = |k_i a|$')
    ax1.set_ylim([1e-6, 1e1])
    ax1.grid(True, which="both", linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right')

    for cid, col, lbl in [("S5_tauth_01ps", 'orange', r'$\tau_\theta = 0.1\ \mathrm{ps}$'),
                          ("S5_tauq_10ps", 'b', r'$\tau_\theta = 2.0\ \mathrm{ps}$ (base)'),
                          ("S5_tauth_100ps", 'purple', r'$\tau_\theta = 100\ \mathrm{ps}$')]:
        c_pts = extract_acoustic_branch([r for r in rec_s5 if r["case_id"] == cid])
        if c_pts:
            ax2.semilogy([float(r["Omega"]) for r in c_pts], [max(float(r["alpha_a"]), 1e-12) for r in c_pts], color=col, lw=1.8, label=lbl)
    ax2.set_title(r'(b) Temperature Gradient Retardation Lag $\tau_\theta$', fontsize=11)
    ax2.set_xlabel(r'Normalized Frequency $\Omega$')
    ax2.grid(True, which="both", linestyle='--', alpha=0.6)
    ax2.legend(loc='lower right')

    fig.suptitle('Figure 6: Dual-Phase-Lag (DPL) Non-Fourier Thermal Time Lags on Acoustic Dissipation', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "fig6_dpl_lags.png"))
    plt.close()
    print("  ✓ Figure 6: Calibrated DPL Lags regenerated.")

    # Figure 7: Thermoelastic Coupling Sweep (S6)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    coup_cases = [("S6_alpha00", 'k', r'$\beta \to 0$ (Conservative)'),
                  ("S6_alpha05", 'g', r'$0.5 \alpha_{t,\mathrm{base}}$'),
                  ("S6_alpha10", 'b', r'$1.0 \alpha_{t,\mathrm{base}}$ (Active Baseline)'),
                  ("S6_alpha20", 'r', r'$2.0 \alpha_{t,\mathrm{base}}$ (Strong Coupling)')]
    for cid, col, lbl in coup_cases:
        c_pts = extract_acoustic_branch([r for r in rec_s6 if r["case_id"] == cid])
        if c_pts:
            ax1.plot([float(r["kr_a_over_pi"]) for r in c_pts], [float(r["Omega"]) for r in c_pts], color=col, lw=1.6, label=lbl)
            ax2.semilogy([float(r["Omega"]) for r in c_pts], [max(float(r["alpha_a"]), 1e-12) for r in c_pts], color=col, lw=1.6, label=lbl)

    ax1.set_title(r'(a) Dispersion Curve Modification', fontsize=11)
    ax1.set_xlabel(r'Real Bloch Wavenumber $k_r a / \pi$')
    ax1.set_ylabel(r'Normalized Frequency $\Omega$')
    ax1.set_xlim([0.0, 1.0])
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right')

    ax2.set_title(r'(b) Thermoelastic Attenuation Floor', fontsize=11)
    ax2.set_xlabel(r'Normalized Frequency $\Omega$')
    ax2.set_ylabel(r'Spatial Attenuation $\alpha a$')
    ax2.set_ylim([1e-6, 1e1])
    ax2.grid(True, which="both", linestyle='--', alpha=0.6)
    ax2.legend(loc='lower right')

    fig.suptitle('Figure 7: Thermoelastic Coupling Intensity Sensitivity & Band-Edge Blunting', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "fig7_thermoelastic_coupling.png"))
    plt.close()
    print("  ✓ Figure 7: Calibrated Thermoelastic Coupling regenerated.")

    # Figure 9: Band-Gap Summary Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    chi_vals = [0.0, 0.5, 1.0]
    widths_chi = [0.0, 0.0884, 0.0354]
    ax1.plot(chi_vals, widths_chi, 'bo-', lw=2, ms=6, label=r'Bragg Gap 1 ($\Omega \approx 0.67 - 0.70$, Closed)')
    ax1.axhline(0.4949, color='red', linestyle='--', lw=1.5, label=r'Gap 2 at $\chi=1.0$ (Truncated at $\Omega=1.80$)')
    ax1.text(0.08, 0.42, 'Gap 2: Open at $\Omega=1.80$;\nupper edge outside investigated range', color='red', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='linen', edgecolor='red', alpha=0.8))
    ax1.set_xlabel(r'Material Contrast Parameter $\chi$')
    ax1.set_ylabel(r'Band-Gap Width $\Delta\Omega$')
    ax1.set_title('(a) Band-Gap Width vs Material Contrast', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper left', fontsize=8.5)

    eta_vals = [0.2, 0.5, 0.8]
    eta_widths = [0.1000, 0.0354, 0.0800]
    ax2.plot(eta_vals, eta_widths, 'rs-', lw=2, ms=6, label=r'Bragg Gap 1 ($\Omega \approx 0.35 - 0.70$, Closed)')
    ax2.axhline(0.4949, color='darkred', linestyle='--', lw=1.5, label=r'Gap 2 at $\eta=0.5$ (Truncated at $\Omega=1.80$)')
    ax2.text(0.22, 0.42, 'Gap 2: Open at $\Omega=1.80$;\nupper edge outside investigated range', color='darkred', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='linen', edgecolor='darkred', alpha=0.8))
    ax2.set_xlabel(r'Layer A Filling Fraction $\eta = a_1/a$')
    ax2.set_ylabel(r'Band-Gap Width $\Delta\Omega$')
    ax2.set_title(r'(b) Band-Gap Width vs Filling Fraction $\eta$', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='lower center', fontsize=8.5)

    fig.suptitle('Figure 9: Authoritative Bragg Band-Gap Summary (Gap 2 Annotated as Open at $\Omega=1.80$)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "fig9_bandgap_summary.png"))
    plt.close()
    print("  ✓ Figure 9: Calibrated Band Gap Summary regenerated.")

    # Figure 10: Compact Synthesis Map (Bragg vs Gradient vs DPL)
    fig, ax = plt.subplots(figsize=(8, 5))
    c_s1_cons = extract_acoustic_branch([r for r in rec_s1 if r["case_id"] == "S1_cons"])
    c_s3_class = extract_acoustic_branch([r for r in rec_s3 if r["case_id"] == "S3_classical"])
    c_s1_dpl = extract_acoustic_branch([r for r in rec_s1 if r["case_id"] == "S1_dpl"])

    if c_s1_cons:
        ax.plot([float(r["kr_a_over_pi"]) for r in c_s1_cons], [float(r["Omega"]) for r in c_s1_cons], 'b-', lw=2.2, label=r'Mechanism 1: Pure Bragg Scattering ($\beta \to 0$, Gradient Elastic)')
    if c_s3_class:
        ax.plot([float(r["kr_a_over_pi"]) for r in c_s3_class], [float(r["Omega"]) for r in c_s3_class], 'k--', lw=2.0, label=r'Mechanism 2: Classical Thermoelasticity ($c, d \to 0$)')
    if c_s1_dpl:
        ax.plot([float(r["kr_a_over_pi"]) for r in c_s1_dpl], [float(r["Omega"]) for r in c_s1_dpl], 'r-.', lw=2.2, label=r'Mechanism 3: Full Coupled DPL + Dipolar Gradient Metamaterial')

    ax.set_xlabel(r'Real Bloch Wavenumber $k_r a / \pi$', fontsize=11)
    ax.set_ylabel(r'Normalized Frequency $\Omega = \omega a / (2\pi v_m)$', fontsize=11)
    ax.set_title('Figure 10: Scientific Synthesis Map — Decoupling Bragg, Gradient, and DPL Mechanisms', fontsize=11)
    ax.set_xlim([0.0, 1.0])
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', framealpha=0.95)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "fig10_synthesis_map.png"))
    plt.close()
    print("  ✓ Figure 10: Calibrated Synthesis Map regenerated.")


if __name__ == "__main__":
    main()
