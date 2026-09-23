#!/usr/bin/env python3
"""
fig05_mesh_convergence.py
Generate Figure 5: Mesh convergence of acoustic frequency and locked resolution floor.
Data source: paper9/verification/suite/p4b_5g_to_5i.json (Test 5i).
Outputs: paper9/figures/out/fig05_mesh_convergence.pdf
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    data_file = os.path.join(repo_root, 'paper9/verification/suite/p4b_5g_to_5i.json')
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig05_mesh_convergence.pdf')

    with open(data_file) as f:
        data = json.load(f)['5i']

    meshes = np.array(data['meshes']) # [4, 8, 16, 32]
    h_vals = 1.0 / meshes
    rel_err = np.array(data['rel_err'])
    slope = data['slope']
    ci95 = data['CI95']
    eps_Delta = data['eps_Delta']

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Log-log convergence of error vs element size h
    ax1.loglog(h_vals, rel_err, 'o-', color='#1f77b4', lw=1.8, ms=6, label='Observed FE error')
    # Trend line: empirical least-squares slope (no theoretical order claimed)
    h_fit = np.logspace(np.log10(h_vals.min()), np.log10(h_vals.max()), 50)
    err_fit = rel_err[0] * (h_fit / h_vals[0])**slope
    ax1.loglog(h_fit, err_fit, 'k--', lw=1.2, label=f'Empirical fit: $p = {slope:.2f}$ ($95\\%$ CI: $[{ci95[0]:.2f}, {ci95[1]:.2f}]$)')

    ax1.axhline(eps_Delta, color='crimson', ls=':', lw=1.5, label=f'Resolution floor $\\varepsilon_\\Delta = {eps_Delta:.2e}$')
    ax1.set_xlabel('Element size $h = L/N$ [m]')
    ax1.set_ylabel('Relative error $|\\omega_T - \\omega_{\\mathrm{exact}}| / \\omega_{\\mathrm{exact}}$')
    ax1.set_title('(a) Eigenvalue Convergence (Case H)', fontsize=10)
    ax1.grid(True, which='both', ls=':', alpha=0.5)
    ax1.legend(loc='lower right', frameon=True, framealpha=0.9, fontsize=7.5)

    # Panel (b): Consecutive mesh relative difference |omega_{2N} - omega_N| / omega_{2N}
    diff_meshes = [f'${meshes[i]}^2 \\to {meshes[i+1]}^2$' for i in range(len(meshes)-1)]
    rel_diffs = [abs(data['omega'][i+1] - data['omega'][i]) / data['omega'][i+1] for i in range(len(meshes)-1)]

    bars = ax2.bar(diff_meshes, rel_diffs, color=['#aec7e8', '#7bafde', '#2b7bba'], edgecolor='navy', width=0.55)
    ax2.axhline(eps_Delta, color='crimson', ls=':', lw=1.5, label=f'Floor $\\varepsilon_\\Delta = {eps_Delta:.2e}$')
    ax2.set_yscale('log')
    ax2.set_xlabel('Mesh Refinement Step')
    ax2.set_ylabel('Relative change $|\\Delta\\omega| / \\omega$')
    ax2.set_title('(b) Stepwise Mesh Variation', fontsize=10)
    ax2.grid(True, which='both', ls=':', alpha=0.5, axis='y')
    ax2.legend(loc='upper right', frameon=True, framealpha=0.9, fontsize=7.5)

    for bar, val in zip(bars, rel_diffs):
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.5, f'{val:.1e}', ha='center', va='bottom', fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
