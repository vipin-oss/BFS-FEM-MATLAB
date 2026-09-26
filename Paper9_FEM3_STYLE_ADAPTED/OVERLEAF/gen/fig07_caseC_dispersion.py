#!/usr/bin/env python3
"""fig07_caseC_dispersion.py
Generate Figure 7: Case C composite phononic crystal band structure and band-gap tuning.
Data source: paper9/results/raw/p11_caseC_raw.json (Study S2).
Outputs: paper9/figures/out/fig07_caseC_dispersion.pdf and fig07_caseC_dispersion.png
"""
from __future__ import annotations

import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    data_file = os.path.join(repo_root, 'paper9/results/raw/p11_caseC_raw.json')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig07_caseC_dispersion.pdf')
    out_png = os.path.join(out_dir, 'fig07_caseC_dispersion.png')

    with open(data_file) as f:
        data = json.load(f)

    baseline = data['baseline']
    s_full = np.array(baseline['s_norm'])
    path_bands = np.array(baseline['path_bands'])
    gap_34 = baseline['gaps'][2]

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # ---------------------------------------------------------
    # Panel (a): Baseline Case C Dispersion (r0 = 0.30)
    # ---------------------------------------------------------
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    for b in range(6):
        ax1.plot(s_full, path_bands[:, b], color=colors[b % len(colors)], lw=1.5, label=f'Band {b+1}')

    # Highlight complete band gap
    w_low = gap_34['omega_lower_max']
    w_upp = gap_34['omega_upper_min']
    ax1.axhspan(w_low, w_upp, color='gray', alpha=0.25, hatch='//', label=f'Complete Gap ({w_low:.2f}--{w_upp:.2f})')

    ticks = [0, 1, 2, 2 + np.sqrt(2)]
    tick_labels = ['$\\Gamma$', '$X$', '$M$', '$\\Gamma$']
    ax1.set_xticks(ticks)
    ax1.set_xticklabels(tick_labels)
    ax1.set_xlim([0, 2 + np.sqrt(2)])
    ax1.set_ylim([0, 9.0])
    ax1.set_xlabel('Wave vector $\\mathbf{k}$')
    ax1.set_ylabel('Normalized frequency $\\bar{\\omega} = \\omega L / (\\pi c_t)$')
    ax1.set_title('(a) Case C Baseline Dispersion ($r_0/a = 0.30$)')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right', frameon=True, framealpha=0.7, fontsize=7)

    # ---------------------------------------------------------
    # Panel (b): Band Gap Tuning vs Inclusion Radius r0
    # ---------------------------------------------------------
    r_sweep = data['radius_sweep']
    radii = []
    w_lows = []
    w_upps = []
    widths = []

    for k, v in sorted(r_sweep.items(), key=lambda item: item[1]['r0']):
        radii.append(v['r0'])
        g = v['gap_34']
        w_lows.append(g['omega_lower_max'])
        w_upps.append(g['omega_upper_min'])
        widths.append(g['delta_complete'])

    radii = np.array(radii)
    w_lows = np.array(w_lows)
    w_upps = np.array(w_upps)
    widths = np.array(widths)

    ax2.fill_between(radii, w_lows, w_upps, color='gray', alpha=0.25, hatch='//', label='Complete Gap Region')
    ax2.plot(radii, w_lows, 'b-o', ms=4, lw=1.5, label='Lower Edge (Band 3)')
    ax2.plot(radii, w_upps, 'r-s', ms=4, lw=1.5, label='Upper Edge (Band 4)')
    
    # Secondary axis for gap width
    ax2_twin = ax2.twinx()
    ax2_twin.plot(radii, widths, 'g-^', ms=4, lw=1.5, label='Gap Width $\\Delta_{\\mathrm{complete}}$')
    ax2_twin.set_ylabel('Gap width $\\Delta_{\\mathrm{complete}}$', color='g')
    ax2_twin.tick_params(axis='y', labelcolor='g')
    ax2_twin.set_ylim([0, 3.5])

    ax2.set_xlabel('Inclusion radius ratio $r_0 / a$')
    ax2.set_ylabel('Normalized frequency $\\bar{\\omega}$')
    ax2.set_title('(b) Band Gap Tuning with Inclusion Size')
    ax2.set_xlim([0.18, 0.42])
    ax2.set_ylim([3.0, 8.5])
    ax2.grid(True, linestyle=':', alpha=0.5)

    # Combined legend for ax2
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, framealpha=0.9, fontsize=7)

    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.savefig(out_png, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_pdf} and {out_png}")


if __name__ == '__main__':
    main()
