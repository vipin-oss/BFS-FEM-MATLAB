#!/usr/bin/env python3
"""
fig08_theta_sweep.py
Generate Figure 8: Orientation sweep theta in [0, 90 deg] at AR = 5.
Demonstrates acoustic frequency migration at X and diagonal symmetry at M.
Data source: paper9/results/raw/p5_production_raw_mesh16.json (Study S3).
Outputs: paper9/figures/out/fig08_theta_sweep.pdf
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
    out_pdf = os.path.join(out_dir, 'fig08_theta_sweep.pdf')

    with open(data_file) as f:
        data = json.load(f)['study_S3']

    thetas = [item['theta_deg'] for item in data]
    # At X = (pi/L, 0):
    # Branch 0 (index 0) = transverse acoustic mode (polarized in uy)
    # Branch 1 (index 1) = transverse microstructural gradient mode (polarized in uy,x)
    # Branch 2 (index 2) = longitudinal acoustic mode (polarized in ux, c_L/c_T = sqrt(3))
    # Branch 3 (index 3) = longitudinal microstructural gradient mode (polarized in ux,x)
    om_X_T = [item['omega_X'][0] for item in data]  # Branch 1 (transverse acoustic)
    om_X_L = [item['omega_X'][2] for item in data]  # Branch 3 (longitudinal acoustic)
    om_M_T = [item['omega_M'][0] for item in data]  # Branch 1 at M
    om_M_L = [item['omega_M'][2] for item in data]  # Branch 3 at M

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Zone-edge frequencies at X vs theta
    ax1.plot(thetas, om_X_T, 'bo-', lw=1.6, ms=5, label='Transverse acoustic $\\omega_T(X)$')
    ax1.plot(thetas, om_X_L, 'rs--', lw=1.6, ms=5, label='Longitudinal acoustic $\\omega_L(X)$')
    ax1.set_xlabel('Orientation angle $\\theta$ [deg]')
    ax1.set_ylabel('Zone-edge frequency $\\bar{\\omega}(X)$')
    ax1.set_title('(a) Acoustic Frequency Migration at $X$', fontsize=10)
    ax1.set_xlim(-5, 95)
    ax1.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax1.grid(True, ls=':', alpha=0.5)
    ax1.legend(loc='center', frameon=True, framealpha=0.7)

    # Panel (b): Corner frequencies at M vs theta (demonstrating exact diagonal symmetry)
    ax2.plot(thetas, om_M_T, 'g^-', lw=1.6, ms=5, label='Branch 1 at $M$')
    ax2.plot(thetas, om_M_L, 'mD--', lw=1.6, ms=5, label='Branch 3 at $M$')
    ax2.axvline(45, color='gray', ls=':', lw=1.0, label='Symmetry axis $\\theta = 45^\\circ$')
    ax2.set_xlabel('Orientation angle $\\theta$ [deg]')
    ax2.set_ylabel('Corner frequency $\\bar{\\omega}(M)$')
    ax2.set_title('(b) Diagonal Symmetry at $M$', fontsize=10)
    ax2.set_xlim(-5, 95)
    ax2.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax2.grid(True, ls=':', alpha=0.5)
    ax2.legend(loc='center left', frameon=True, framealpha=0.7)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
