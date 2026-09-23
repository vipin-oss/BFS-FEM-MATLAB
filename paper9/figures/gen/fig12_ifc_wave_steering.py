#!/usr/bin/env python3
"""
fig12_ifc_wave_steering.py
Generate Figure 12: Wave-vector steering and group velocity deviation angle delta(phi) at fixed kbar = 0.5.
Data source: paper9/results/raw/p5_production_raw.json (Study S7).
Outputs: paper9/figures/out/fig12_ifc_wave_steering.pdf
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
    out_pdf = os.path.join(out_dir, 'fig12_ifc_wave_steering.pdf')

    with open(data_file) as f:
        data = json.load(f)['study_S7_ifc_steering']

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    cases = [
        ('AR_1_th_0', '$\\mathrm{AR}=1$ (Isotropic)', 'k--', 1.4),
        ('AR_5_th_45', '$\\mathrm{AR}=5, \\theta=45^\\circ$', '#2ca02c', 1.8),
        ('AR_10_th_45', '$\\mathrm{AR}=10, \\theta=45^\\circ$', '#d62728', 1.8),
    ]

    # Panel (a): Deviation angle delta = angle(vg) - angle(k) vs propagation direction phi at kbar = 0.5
    for key, lbl, style, lw in cases:
        c_data = data[key]
        phi = np.array(c_data['phi_deg'])
        delta = np.array(c_data['delta_deg'])
        d_max = c_data['delta_max_deg']
        lbl_full = f'{lbl} ($\\delta_{{\\max}} = {d_max:.2f}^\\circ$)'
        ax1.plot(phi, delta, style, lw=lw, label=lbl_full)

    ax1.set_xlabel('Wave vector direction $\\phi$ [deg]')
    ax1.set_ylabel('Steering angle $\\delta = \\angle \\mathbf{v}_g - \\angle \\mathbf{k}$ [deg]')
    ax1.set_title('(a) Steering Deviation $\\delta(\\phi)$ at $\\bar{k} = 0.5$', fontsize=10)
    ax1.set_xlim(0, 90)
    ax1.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax1.grid(True, ls=':', alpha=0.5)
    ax1.legend(loc='lower center', frameon=True, framealpha=0.9, fontsize=7.5)

    # Panel (b): Group velocity magnitude |v_g| vs direction phi at kbar = 0.5
    for key, lbl, style, lw in cases:
        c_data = data[key]
        phi = np.array(c_data['phi_deg'])
        vg = np.array(c_data['vg_mag'])
        ax2.plot(phi, vg, style, lw=lw, label=lbl)

    ax2.set_xlabel('Wave vector direction $\\phi$ [deg]')
    ax2.set_ylabel('Group velocity magnitude $|\\mathbf{v}_g|$')
    ax2.set_title('(b) Group Velocity Magnitude at $\\bar{k} = 0.5$', fontsize=10)
    ax2.set_xlim(0, 90)
    ax2.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax2.grid(True, ls=':', alpha=0.5)
    ax2.legend(loc='upper right', frameon=True, framealpha=0.9, fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
