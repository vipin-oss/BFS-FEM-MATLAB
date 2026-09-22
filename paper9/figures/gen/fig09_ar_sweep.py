#!/usr/bin/env python3
"""
fig09_ar_sweep.py
Generate Figure 9: Aspect-ratio sweep AR in [1, 10] at theta = 45 deg.
Data source: paper9/results/raw/p5_production_raw.json (Study S4).
Outputs: paper9/figures/out/fig09_ar_sweep.pdf
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    data_file = os.path.join(repo_root, 'paper9/results/raw/p5_production_raw.json')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig09_ar_sweep.pdf')

    with open(data_file) as f:
        data = json.load(f)['study_S4']

    ars = [item['AR'] for item in data]
    om_X_T = [item['omega_X'][0] for item in data]
    om_X_L = [item['omega_X'][1] for item in data]
    om_M_T = [item['omega_M'][0] for item in data]
    om_M_L = [item['omega_M'][2] for item in data]

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Zone-edge frequencies at X vs AR
    ax1.plot(ars, om_X_T, 'bo-', lw=1.6, ms=5, label='Transverse $\\omega_T(X)$')
    ax1.plot(ars, om_X_L, 'rs--', lw=1.6, ms=5, label='Longitudinal $\\omega_L(X)$')
    ax1.set_xlabel('Aspect ratio $\\mathrm{AR}$')
    ax1.set_ylabel('Zone-edge frequency $\\bar{\\omega}(X)$')
    ax1.set_title('(a) Acoustic Frequencies at $X$ vs $\\mathrm{AR}$', fontsize=10)
    ax1.set_xticks(ars)
    ax1.grid(True, ls=':', alpha=0.5)
    ax1.legend(loc='lower right', frameon=True, framealpha=0.9)

    # Panel (b): Corner frequencies at M vs AR
    ax2.plot(ars, om_M_T, 'g^-', lw=1.6, ms=5, label='Branch 1 at $M$')
    ax2.plot(ars, om_M_L, 'mD--', lw=1.6, ms=5, label='Branch 3 at $M$')
    ax2.set_xlabel('Aspect ratio $\\mathrm{AR}$')
    ax2.set_ylabel('Corner frequency $\\bar{\\omega}(M)$')
    ax2.set_title('(b) Frequencies at $M$ vs $\\mathrm{AR}$', fontsize=10)
    ax2.set_xticks(ars)
    ax2.grid(True, ls=':', alpha=0.5)
    ax2.legend(loc='center left', frameon=True, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
