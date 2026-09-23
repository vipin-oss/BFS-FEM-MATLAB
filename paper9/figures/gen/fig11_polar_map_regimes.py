#!/usr/bin/env python3
"""
fig11_polar_map_regimes.py
Generate Figure 11: Polar design map (X=AR*cos(theta), Y=AR*sin(theta)) and sensitivity S_theta.
Data sources: paper9/results/raw/p5_production_raw.json (Study S6).
Outputs: paper9/figures/out/fig11_polar_map_regimes.pdf
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
    out_pdf = os.path.join(out_dir, 'fig11_polar_map_regimes.pdf')

    with open(data_file) as f:
        d = json.load(f)
        polar_data = d['study_S6_polar_map']
        stheta_data = d['study_S6_sensitivity_Stheta']
        s5_data = d['study_S5_design_map']

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Polar design space (X = AR*cos(theta), Y = AR*sin(theta))
    X_pos, Y_pos, vals_pos = [], [], []
    X_neg, Y_neg, vals_neg = [], [], []

    for item, s5_item in zip(polar_data, s5_data):
        x = item['X']
        y = item['Y']
        gap_val = s5_item['gaps'][1]['delta_GX'] # Band pair [2, 3] along Gamma-X
        if gap_val > 0:
            X_pos.append(x)
            Y_pos.append(y)
            vals_pos.append(gap_val)
        else:
            X_neg.append(x)
            Y_neg.append(y)
            vals_neg.append(gap_val)

    # Polar arcs for AR = 1, 3, 5, 10
    th_arc = np.linspace(0, np.pi/2, 100)
    for r in [1, 3, 5, 10]:
        ax1.plot(r * np.cos(th_arc), r * np.sin(th_arc), 'gray', ls=':', lw=0.7)
        ax1.text(r * np.cos(np.pi/4), r * np.sin(np.pi/4), f'${r}$', fontsize=7, color='gray', ha='center', va='center')

    # Rays for thetas
    for th_d in [0, 15, 30, 45, 60, 75, 90]:
        th_r = np.deg2rad(th_d)
        ax1.plot([0, 10*np.cos(th_r)], [0, 10*np.sin(th_r)], 'gray', ls=':', lw=0.5)

    sc = ax1.scatter(X_pos, Y_pos, c=vals_pos, cmap='plasma', s=35, edgecolors='k', lw=0.5, label='$\\Delta_{GX} > 0$ (Directional stop band, $\\Gamma-X$)', zorder=5)
    if X_neg:
        ax1.scatter(X_neg, Y_neg, color='white', edgecolors='crimson', s=35, lw=1.2, label='$\\Delta_{GX} \\leq 0$ (Pass band, $\\Gamma-X$)', zorder=5)

    cb = fig.colorbar(sc, ax=ax1, pad=0.03)
    cb.set_label('Directional gap $\\Delta_{GX}$')

    ax1.set_aspect('equal')
    ax1.set_xlim(-0.5, 11)
    ax1.set_ylim(-0.5, 11)
    ax1.set_xlabel('$X = \\mathrm{AR}\\cos\\theta$')
    ax1.set_ylabel('$Y = \\mathrm{AR}\\sin\\theta$')
    ax1.set_title('(a) Polar Directional Regimes ($\\Gamma-X$)', fontsize=10)
    ax1.legend(loc='upper right', frameon=True, framealpha=0.9, fontsize=7)

    # Panel (b): Sensitivity S_theta vs AR
    ars = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    stheta_vals = [stheta_data[f'AR_{int(ar)}']['S_theta_rad_inv'] for ar in ars]

    ax2.plot(ars, stheta_vals, 'mo-', lw=1.8, ms=6, label='Sensitivity $S_\\theta = \\frac{\\max |\\partial\\Delta/\\partial\\theta|}{\\max \\Delta}$')
    ax2.set_xlabel('Aspect ratio $\\mathrm{AR}$')
    ax2.set_ylabel('$S_\\theta$ [$\\mathrm{rad}^{-1}$]')
    ax2.set_title('(b) Orientation Sensitivity vs $\\mathrm{AR}$', fontsize=10)
    ax2.set_xticks(ars)
    ax2.grid(True, ls=':', alpha=0.5)
    ax2.legend(loc='upper left', frameon=True, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
