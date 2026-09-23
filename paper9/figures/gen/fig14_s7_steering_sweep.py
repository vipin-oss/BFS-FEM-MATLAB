#!/usr/bin/env python3
"""
fig14_s7_steering_sweep.py
Generate Figure 14: P12B orientation sweep of S7 steering quantities on the
locked ring |k| = 0.5 pi / L.
(a) delta_max(theta) for AR = 5 and AR = 10 (exact theta <-> 90 deg - theta
    mirror symmetry; maxima at theta = 15 deg and 75 deg).
(b) Ring deviation field delta(phi) for AR = 10 at theta = 0 deg (solid) and
    theta = 90 deg (markers), showing the mirror relation
    delta(phi; 0) = delta(90 deg - phi; 90) exactly (curves overlay the mirror).
Data source: paper9/results/raw/p12b_s7_theta_sweep.json (P12B locked S7
extension; anchor-checked against study_S7_ifc_steering).
Outputs: paper9/figures/out/fig14_s7_steering_sweep.pdf/.png
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    data_file = os.path.join(repo_root, 'paper9/results/raw/p12b_s7_theta_sweep.json')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)

    with open(data_file) as f:
        d = json.load(f)
    sw = d['sweep']
    ms = d['M_s']
    ths = [0, 15, 30, 45, 60, 75, 90]

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5), dpi=300)

    # Panel (a): delta_max(theta) and phi*(theta)
    d5 = [sw[f"AR_5_th_{t}"]['delta_max_deg'] for t in ths]
    d10 = [sw[f"AR_10_th_{t}"]['delta_max_deg'] for t in ths]
    p5 = [sw[f"AR_5_th_{t}"]['phi_star_deg'] for t in ths]
    p10 = [sw[f"AR_10_th_{t}"]['phi_star_deg'] for t in ths]

    ax1.plot(ths, d5, 'o-', color='tab:blue', lw=1.6, ms=5,
             label='$\\delta_{\\max}$, AR=5')
    ax1.plot(ths, d10, 's-', color='tab:red', lw=1.6, ms=5,
             label='$\\delta_{\\max}$, AR=10')
    ax1.set_xlabel('Microstructure orientation $\\theta$ [deg]')
    ax1.set_ylabel('Max. steering deviation $\\delta_{\\max}$ [deg]')
    ax1.set_xticks(ths)
    ax1.grid(True, ls=':', alpha=0.5)
    ax1.legend(loc='lower left', frameon=True, framealpha=0.9)

    ax1b = ax1.twinx()
    ax1b.plot(ths, p5, 'o--', color='tab:blue', mfc='none', lw=1.0, ms=5,
              label='$\\phi^*$, AR=5')
    ax1b.plot(ths, p10, 's--', color='tab:red', mfc='none', lw=1.0, ms=5,
              label='$\\phi^*$, AR=10')
    ax1b.set_ylabel('Principal steering axis $\\phi^*$ [deg] (mod $90^\\circ$)')
    ax1b.set_ylim(-5, 95)
    ax1b.legend(loc='lower right', frameon=True, framealpha=0.9)
    ax1.set_title('(a) Steering strength & axis vs. $\\theta$', fontsize=10)
    ax1.set_xlim(-4, 94)

    # Panel (b): mirror co-symmetry of the ring deviation field (AR=10)
    ph = np.array(sw['AR_10_th_0']['phi_deg'])
    d0 = np.array(sw['AR_10_th_0']['delta_deg'])
    d90 = np.array(sw['AR_10_th_90']['delta_deg'])
    # mirror: delta(90 - phi; 90 deg) mapped onto the phi grid
    idx = (18 - np.arange(len(ph))) % 72
    d90_m = d90[idx]
    keep = ph <= 180.0
    ax2.plot(ph[keep], d0[keep], '-', color='tab:red', lw=2.0,
             label='$\\delta(\\phi;\\ \\theta=0^\\circ)$, AR=10')
    ax2.plot(ph[keep][::2], d90_m[keep][::2], 'o', color='navy', ms=4.5,
             mfc='none', mew=1.2,
             label='$\\delta(90^\\circ-\\phi;\\ \\theta=90^\\circ)$, AR=10')
    ax2.set_xlabel('Propagation angle $\\phi$ on ring $|\\bar{k}|=0.5$ [deg]')
    ax2.set_ylabel('Deviation $\\delta$ [deg]')
    ax2.set_xlim(0, 180)
    ax2.set_xticks([0, 30, 60, 90, 120, 150, 180])
    ax2.grid(True, ls=':', alpha=0.5)
    ax2.legend(loc='lower right', frameon=True, framealpha=0.9)
    ax2.set_title('(b) Mirror co-symmetry of $\\delta(\\phi)$, AR=10', fontsize=10)

    fig.tight_layout(w_pad=2.2)
    out_pdf = os.path.join(out_dir, 'fig14_s7_steering_sweep.pdf')
    out_png = os.path.join(out_dir, 'fig14_s7_steering_sweep.png')
    fig.savefig(out_pdf)
    fig.savefig(out_png)
    plt.close(fig)
    print(f"Generated {out_pdf}\nGenerated {out_png}")


if __name__ == '__main__':
    main()
