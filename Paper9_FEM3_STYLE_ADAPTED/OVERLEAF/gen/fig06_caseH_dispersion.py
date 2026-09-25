#!/usr/bin/env python3
"""
fig06_caseH_dispersion.py
Generate Figure 6: Case H band structure along Gamma-X-M-Gamma for AR=1 vs AR=10 at theta in {0, 45 deg}.
Data source: paper9/results/raw/p5_production_raw_mesh16.json (Study S1).
Outputs: paper9/figures/out/fig06_caseH_dispersion.pdf
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    data_file = os.path.join(repo_root, 'paper9/results/raw/p5_production_raw_mesh16.json')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig06_caseH_dispersion.pdf')

    with open(data_file) as f:
        data = json.load(f)['study_S1']

    # Path coordinate s
    s1 = np.linspace(0, 1, 41)
    s2 = np.linspace(1, 2, 41)[1:]
    s3 = np.linspace(2, 2 + np.sqrt(2), 41)[1:]
    s_full = np.concatenate([s1, s2, s3]) # 121 points

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300, sharey=True)

    # Panel (a): AR = 1 (isotropic) vs AR = 10, theta = 0 deg
    iso_bands = np.array(data['AR_1_th_0']['tracked_bands'])
    aniso0_bands = np.array(data['AR_10_th_0']['tracked_bands'])

    for b in range(4):
        lbl_iso = '$\\mathrm{AR}=1$ (Isotropic)' if b == 0 else None
        lbl_aniso = '$\\mathrm{AR}=10, \\theta=0^\\circ$' if b == 0 else None
        ax1.plot(s_full, iso_bands[:, b], 'k--', lw=1.2, label=lbl_iso)
        ax1.plot(s_full, aniso0_bands[:, b], 'b-', lw=1.6, label=lbl_aniso)

    # Panel (b): AR = 1 vs AR = 10, theta = 45 deg
    aniso45_bands = np.array(data['AR_10_th_45']['tracked_bands'])
    for b in range(4):
        lbl_iso = '$\\mathrm{AR}=1$ (Isotropic)' if b == 0 else None
        lbl_aniso = '$\\mathrm{AR}=10, \\theta=45^\\circ$' if b == 0 else None
        ax2.plot(s_full, iso_bands[:, b], 'k--', lw=1.2, label=lbl_iso)
        ax2.plot(s_full, aniso45_bands[:, b], 'r-', lw=1.6, label=lbl_aniso)

    ticks = [0, 1, 2, 2 + np.sqrt(2)]
    tick_labels = ['$\\Gamma$', '$X$', '$M$', '$\\Gamma$']

    for ax, title in zip([ax1, ax2], ['(a) Isotropic vs $\\mathrm{AR}=10, \\theta=0^\\circ$',
                                     '(b) Isotropic vs $\\mathrm{AR}=10, \\theta=45^\\circ$']):
        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels)
        for t in ticks:
            ax.axvline(t, color='gray', ls=':', lw=0.8)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('Wave vector path')
        ax.set_xlim(0, 2 + np.sqrt(2))
        ax.set_ylim(bottom=0)
        ax.grid(True, ls=':', alpha=0.4)
        ax.legend(loc='upper left', frameon=True, framealpha=0.9)

    ax1.set_ylabel('Non-dimensional frequency $\\bar{\\omega}$')

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
