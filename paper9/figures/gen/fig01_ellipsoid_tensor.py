#!/usr/bin/env python3
"""
fig01_ellipsoid_tensor.py
Generate Figure 1: Schematic of the microstructural ellipsoid and rotated second-moment length tensor.
Formulas from Blueprint Section 2.1, Eqs. (1)-(9).
Outputs: paper9/figures/out/fig01_ellipsoid_tensor.pdf
"""
import os
import yaml
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    params_file = os.path.join(repo_root, 'paper9/params/params_master.yaml')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig01_ellipsoid_tensor.pdf')

    with open(params_file) as f:
        cfg = yaml.safe_load(f)['parameters']

    l_iso = cfg['l_iso']['value'] # 0.20

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'figure.titlesize': 11
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Ellipsoid geometries for AR = 1, 3, 5, 10 at theta = 45 deg
    t = np.linspace(0, 2*np.pi, 200)
    theta_fixed = np.deg2rad(45.0)
    R = np.array([[np.cos(theta_fixed), -np.sin(theta_fixed)],
                  [np.sin(theta_fixed),  np.cos(theta_fixed)]])

    ar_list = [1.0, 3.0, 5.0, 10.0]
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

    for ar, c in zip(ar_list, colors):
        l1 = l_iso * np.sqrt(ar)
        l2 = l_iso / np.sqrt(ar)
        coords = np.vstack([l1 * np.cos(t), l2 * np.sin(t)])
        rot_coords = R @ coords
        ax1.plot(rot_coords[0], rot_coords[1], label=f'$\\mathrm{{AR}} = {int(ar) if ar.is_integer() else ar}$', color=c, lw=1.5)

    ax1.set_aspect('equal')
    ax1.axhline(0, color='gray', ls='--', lw=0.6)
    ax1.axvline(0, color='gray', ls='--', lw=0.6)
    ax1.set_title('(a) Microstructural Ellipsoid ($\\theta = 45^\\circ$)', fontsize=10)
    ax1.set_xlabel('$x_1$ [m]')
    ax1.set_ylabel('$x_2$ [m]')
    ax1.legend(loc='upper right', frameon=True, framealpha=0.9)
    ax1.grid(True, ls=':', alpha=0.5)

    # Panel (b): Second-moment tensor components L_11, L_22, L_12 vs theta for AR = 5
    # Locked passive coordinate rotation: L = R^T diag(l1^2, l2^2) R (Blueprint Eq. 8)
    theta_sweep = np.linspace(0, 90, 181)
    theta_rad = np.deg2rad(theta_sweep)
    ar_b = 5.0
    l1_b = l_iso * np.sqrt(ar_b)
    l2_b = l_iso / np.sqrt(ar_b)

    L11 = l1_b**2 * np.cos(theta_rad)**2 + l2_b**2 * np.sin(theta_rad)**2
    L22 = l1_b**2 * np.sin(theta_rad)**2 + l2_b**2 * np.cos(theta_rad)**2
    L12 = (l2_b**2 - l1_b**2) * np.sin(theta_rad) * np.cos(theta_rad)

    ax2.plot(theta_sweep, L11, 'b-', label='$L_{11}(\\theta)$', lw=1.8)
    ax2.plot(theta_sweep, L22, 'r--', label='$L_{22}(\\theta)$', lw=1.8)
    ax2.plot(theta_sweep, L12, 'g-.', label='$L_{12}(\\theta)$', lw=1.8)

    ax2.set_title(f'(b) Tensor Components $\\mathbf{{L}}(\\theta)$ ($\\mathrm{{AR}} = {int(ar_b)}$)', fontsize=10)
    ax2.set_xlabel('Orientation angle $\\theta$ [deg]')
    ax2.set_ylabel('$L_{ij}$ [$\\mathrm{m}^2$]')
    ax2.set_xlim(0, 90)
    ax2.legend(loc='center right', frameon=True, framealpha=0.9)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
