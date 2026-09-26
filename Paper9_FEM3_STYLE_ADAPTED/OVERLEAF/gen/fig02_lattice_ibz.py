#!/usr/bin/env python3
"""
fig02_lattice_ibz.py
Generate Figure 2: Direct lattice unit cell, reciprocal lattice, First Brillouin Zone,
and symmetry path Gamma-X-M-Gamma alongside the irreducible zone coverage.
Formulas from Blueprint Section 3.1-3.3, Eqs. (36)-(38), (44) and AUDIT_M10a.
Outputs: paper9/figures/out/fig02_lattice_ibz.pdf
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
    out_pdf = os.path.join(out_dir, 'fig02_lattice_ibz.pdf')

    with open(params_file) as f:
        cfg = yaml.safe_load(f)['parameters']

    L = cfg['Lcell']['value']

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Direct lattice unit cell
    ax1.plot([0, L, L, 0, 0], [0, 0, L, L, 0], 'k-', lw=1.5, label='Unit cell $\\Omega_0$')
    ax1.scatter([0, L, L, 0], [0, 0, L, L], color='blue', s=35, zorder=5, label='Lattice nodes')
    ax1.quiver(0, 0, L, 0, angles='xy', scale_units='xy', scale=1, color='darkgreen', width=0.015)
    ax1.quiver(0, 0, 0, L, angles='xy', scale_units='xy', scale=1, color='darkgreen', width=0.015)
    ax1.text(L/2, -0.12*L, '$\\mathbf{a}_1 = (L, 0)$', ha='center', va='top', color='darkgreen', fontsize=9)
    ax1.text(-0.08*L, L/2, '$\\mathbf{a}_2 = (0, L)$', ha='right', va='center', color='darkgreen', fontsize=9)
    ax1.set_xlim(-0.25*L, 1.25*L)
    ax1.set_ylim(-0.25*L, 1.25*L)
    ax1.set_aspect('equal')
    ax1.set_title('(a) Direct Space Unit Cell', fontsize=10)
    ax1.set_xlabel('$x_1$ [m]')
    ax1.set_ylabel('$x_2$ [m]')
    ax1.grid(True, ls=':', alpha=0.5)
    ax1.legend(loc='upper left', frameon=True, framealpha=0.7)

    # Panel (b): Reciprocal space first BZ and IBZ
    q = np.pi / L
    # First BZ boundary
    ax2.plot([-q, q, q, -q, -q], [-q, -q, q, q, -q], 'k--', lw=1.2, label='First BZ')
    # Half-BZ shaded (anisotropic IBZ)
    ax2.fill([0, q, q, 0], [-q, -q, q, q], color='#1f77b4', alpha=0.15, label='Anisotropic IBZ (half-BZ)')
    # Isotropic triangle shaded
    ax2.fill([0, q, q], [0, 0, q], color='#ff7f0e', alpha=0.25, label='Isotropic IBZ (1/8 BZ)')
    # Symmetry path Gamma - X - M - Gamma
    path_k = np.array([[0, 0], [q, 0], [q, q], [0, 0]])
    ax2.plot(path_k[:,0], path_k[:,1], 'r-', lw=2.0, label='Path $\\Gamma \\to X \\to M \\to \\Gamma$')

    # Mark points
    pts = {'$\\Gamma$': (0, 0), '$X$': (q, 0), '$M$': (q, q), '$Y$': (0, q)}
    for name, (px, py) in pts.items():
        ax2.scatter(px, py, color='darkred', s=30, zorder=6)
        offset = (0.08*q, 0.08*q) if name != '$Y$' else (-0.15*q, 0.08*q)
        ax2.text(px + offset[0], py + offset[1], name, fontsize=10, fontweight='bold', color='darkred')

    ax2.set_xlim(-1.25*q, 1.25*q)
    ax2.set_ylim(-1.25*q, 1.25*q)
    ax2.set_aspect('equal')
    ax2.set_title('(b) Reciprocal Space & Symmetry Path', fontsize=10)
    ax2.set_xlabel('$k_x$ [rad/m]')
    ax2.set_ylabel('$k_y$ [rad/m]')
    ax2.grid(True, ls=':', alpha=0.5)
    ax2.legend(loc='lower left', frameon=True, framealpha=0.7, fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
