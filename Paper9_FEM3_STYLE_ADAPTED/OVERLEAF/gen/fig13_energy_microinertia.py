#!/usr/bin/env python3
"""
fig13_energy_microinertia.py
Generate Figure 13: Higher-order energy flux partition and micro-inertia phase speed admissibility.
Data source: paper9/results/raw/p5_production_raw_mesh16.json (Study S8, S9).
Outputs: paper9/figures/out/fig13_energy_microinertia.pdf
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
    out_pdf = os.path.join(out_dir, 'fig13_energy_microinertia.pdf')

    with open(data_file) as f:
        d = json.load(f)
        s8 = d['study_S8_energy_flux']
        s9 = d['study_S9_microinertia']

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): Energy partition vs kbar
    k_s8 = [item['kbar'] for item in s8]
    Wg_pct = [item['Wg_over_W_major'] * 100 for item in s8]
    Tg_pct = [item['Tg_over_T'] * 100 for item in s8]

    ax1.plot(k_s8, Wg_pct, 'b-o', lw=1.6, ms=4, label='Gradient strain energy $\\langle W_g \\rangle / \\langle W \\rangle$')
    ax1.plot(k_s8, Tg_pct, 'r--s', lw=1.6, ms=4, label='Micro-inertia kinetic $\\langle T_g \\rangle / \\langle T \\rangle$')
    ax1.set_xlabel('Non-dimensional wavenumber $\\bar{k} = k L / \\pi$')
    ax1.set_ylabel('Energy fraction [\\%]')
    ax1.set_title('(a) Energy Partition vs Frequency', fontsize=10)
    ax1.set_xlim(0, 1.05)
    ax1.set_ylim(bottom=0)
    ax1.grid(True, ls=':', alpha=0.5)
    ax1.legend(loc='upper left', frameon=True, framealpha=0.9, fontsize=7.5)

    # Panel (b): Micro-inertia high-k phase velocity
    k_s9 = [item['kbar'] for item in s9]
    vp_bounded = [item['vp_ell_pos'] for item in s9]
    vp_unbounded = [item['vp_ell_zero'] for item in s9]
    vinf = s9[0]['vinf_theory']

    ax2.loglog(k_s9, vp_bounded, 'go-', lw=1.6, ms=4, label='$\\bar{\\ell} = 0.20 > 0$ (bounded)')
    ax2.loglog(k_s9, vp_unbounded, 'r^--', lw=1.6, ms=4, label='$\\bar{\\ell} = 0$ (unbounded, $\\propto \\bar{k}$)')
    ax2.axhline(vinf, color='darkgreen', ls=':', lw=1.4, label=f'Theoretical $v_{{T,\\infty}} = {vinf:.4f}$')

    ax2.set_xlabel('Wavenumber $\\bar{k} = k L / \\pi$')
    ax2.set_ylabel('Phase velocity $\\bar{v}_p = \\bar{\\omega} / (\\pi \\bar{k})$')
    ax2.set_title('(b) Micro-Inertia High-$k$ Admissibility', fontsize=10)
    ax2.grid(True, which='both', ls=':', alpha=0.5)
    ax2.legend(loc='upper left', frameon=True, framealpha=0.7, fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
