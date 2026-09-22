#!/usr/bin/env python3
"""
fig10_design_map_3d.py
Generate Figure 10: (theta, AR) directional stop-band design map and contour projection.
Data source: paper9/results/raw/p5_production_raw.json (Study S5).
Outputs: paper9/figures/out/fig10_design_map_3d.pdf
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    data_file = os.path.join(repo_root, 'paper9/results/raw/p5_production_raw.json')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig10_design_map_3d.pdf')

    with open(data_file) as f:
        data = json.load(f)['study_S5_design_map']

    ars = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    thetas = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]

    TH, AR = np.meshgrid(thetas, ars)
    Z = np.zeros_like(TH)

    for item in data:
        i = ars.index(item['AR'])
        j = thetas.index(item['theta_deg'])
        Z[i, j] = item['gaps'][1]['delta_GX'] # Band pair [2, 3] directional gap along Gamma-X

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig = plt.figure(figsize=(7.6, 3.5), dpi=300)

    # Panel (a): 3D surface plot
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    surf = ax1.plot_surface(TH, AR, Z, cmap='viridis', edgecolor='k', lw=0.4, alpha=0.85)
    ax1.set_xlabel('$\\theta$ [deg]', labelpad=4)
    ax1.set_ylabel('$\\mathrm{AR}$', labelpad=4)
    ax1.set_zlabel('$\\Delta_{GX}$', labelpad=4)
    ax1.set_title('(a) Response Surface $\\Delta_{GX}(\\theta, \\mathrm{AR})$', fontsize=9.5)
    ax1.view_init(elev=28, azim=-125)

    # Panel (b): 2D filled contour map
    ax2 = fig.add_subplot(1, 2, 2)
    cp = ax2.contourf(TH, AR, Z, levels=12, cmap='viridis')
    cb = fig.colorbar(cp, ax=ax2, pad=0.04)
    cb.set_label('Directional gap $\\Delta_{GX}$')

    # Contour of zero gap (regime boundary)
    cs = ax2.contour(TH, AR, Z, levels=[0.0], colors='crimson', linewidths=1.8, linestyles='--')
    ax2.clabel(cs, fmt='$\\Delta = 0$', fontsize=8)

    ax2.scatter(TH.flatten(), AR.flatten(), color='k', s=12, alpha=0.7, label='Evaluated points (42)')
    ax2.set_xlabel('Orientation angle $\\theta$ [deg]')
    ax2.set_ylabel('Aspect ratio $\\mathrm{AR}$')
    ax2.set_title('(b) Contour Projection & Stop-Band Regimes', fontsize=9.5)
    ax2.set_xticks(thetas)
    ax2.set_yticks(ars)
    ax2.grid(True, ls=':', alpha=0.4)
    ax2.legend(loc='lower left', frameon=True, framealpha=0.9, fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
