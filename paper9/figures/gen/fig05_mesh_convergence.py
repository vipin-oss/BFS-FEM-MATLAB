#!/usr/bin/env python3
"""
fig05_mesh_convergence.py
Generate Figure 5: Mesh convergence of acoustic frequency, the observed rate fitted over the
levels admissible under Rule R-fit (Blueprint v1.4 section 5.7), and the operational resolution
floor.  Levels excluded from the rate fit are shown distinctly and labelled resolution-limited.
Data sources:
  * paper9/verification/suite/p4b_5g_to_5i.json          (governing Test 5i result; numerical baseline)
  * paper9/audit/evidence/p12h/rule_rfit_governing.json  (per-level reproducibility s_i, rule constants)
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

    # Rule R-fit inputs (Blueprint v1.4 §5.7): per-level reproducibility s_i and frozen constants.
    rule_file = os.path.join(repo_root, 'paper9/audit/evidence/p12h/rule_rfit_governing.json')
    with open(rule_file) as f:
        rule = json.load(f)
    F = rule['rule']['F']
    spread_floor = rule['rule']['spread_floor']
    spreads = np.array([max(s if s is not None else spread_floor, spread_floor)
                        for s in rule['reproducibility_inputs']['governing_era']['spreads']])
    ratios = np.array(data['rel_err']) / spreads
    in_fit = ratios > F

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

    # Panel (a): Log-log convergence of error vs element size h.
    # Levels admissible under Rule R-fit (in the rate fit) are drawn filled and joined;
    # levels excluded from the fit are drawn as open markers and are NOT joined.
    h_in, e_in = h_vals[in_fit], rel_err[in_fit]
    h_out, e_out = h_vals[~in_fit], rel_err[~in_fit]
    ax1.loglog(h_in, e_in, 'o-', color='#1f77b4', lw=1.8, ms=6,
               label=f'FE error, in rate fit ({len(h_in)} levels)')
    if len(h_out):
        ax1.loglog(h_out, e_out, 's', mfc='white', mec='#d62728', mew=1.8, ms=7,
                   label=f'Resolution-limited ({len(h_out)} level, excluded from fit)')
    # Trend line: empirical least-squares slope over the admissible levels (no theoretical order claimed)
    h_fit = np.logspace(np.log10(h_in.min()), np.log10(h_in.max()), 50)
    err_fit = e_in[0] * (h_fit / h_in[0])**slope
    ax1.loglog(h_fit, err_fit, 'k--', lw=1.2,
               label=f'Empirical fit: $p = {slope:.2f}$ ($95\\%$ CI: $[{ci95[0]:.2f}, {ci95[1]:.2f}]$)')

    ax1.axhline(eps_Delta, color='crimson', ls=':', lw=1.5,
                label=f'Operational floor $\\varepsilon_\\Delta = {eps_Delta:.2e}$')
    ax1.axhline(float(spreads.max()), color='0.45', ls='-.', lw=1.0,
                label=f'Measurement resolution (max $s_i$) $= {float(spreads.max()):.1e}$')
    ax1.set_xlabel('Element size $h = L/N$ [m]')
    ax1.set_ylabel('Relative error $|\\omega_T - \\omega_{\\mathrm{exact}}| / \\omega_{\\mathrm{exact}}$')
    ax1.set_title('(a) Eigenvalue Convergence (Case H)', fontsize=10)
    ax1.grid(True, which='both', ls=':', alpha=0.5)
    ax1.legend(loc='lower right', frameon=True, framealpha=0.9, fontsize=7.5)

    # Panel (b): Consecutive mesh relative difference |omega_{2N} - omega_N| / omega_{2N}
    diff_meshes = [f'${meshes[i]}^2 \\to {meshes[i+1]}^2$' for i in range(len(meshes)-1)]
    rel_diffs = [abs(data['omega'][i+1] - data['omega'][i]) / data['omega'][i+1] for i in range(len(meshes)-1)]

    bars = ax2.bar(diff_meshes, rel_diffs, color=['#aec7e8', '#7bafde', 'white'],
                   edgecolor=['navy', 'navy', '#d62728'], width=0.55)
    bars[-1].set_hatch('//')   # step involving the resolution-limited (excluded) level
    ax2.axhline(eps_Delta, color='crimson', ls=':', lw=1.5)
    ax2.set_yscale('log')
    ax2.set_xlabel('Mesh Refinement Step')
    ax2.set_ylabel('Relative change $|\\Delta\\omega| / \\omega$')
    ax2.set_title('(b) Stepwise Mesh Variation', fontsize=10)

    ax2.grid(True, which='both', ls=':', alpha=0.5, axis='y')
    from matplotlib.patches import Patch
    ax2.legend(handles=[
        Patch(facecolor='white', edgecolor='#d62728', hatch='//',
              label='resolution-limited step (excluded from rate fit)'),
        Patch(facecolor='none', edgecolor='crimson', ls=':', label=f'Operational floor $\\varepsilon_\\Delta = {eps_Delta:.2e}$'),
    ], loc='upper right', frameon=True, framealpha=0.95, fontsize=6.2)

    # Value labels: inside the two tall bars (no collision with the panel title); the smallest
    # bar keeps its label just above itself.  Presentation only -- no data, axes or limits change.
    ymax = max(rel_diffs)
    for bar, val in zip(bars, rel_diffs):
        cx = bar.get_x() + bar.get_width()/2.0
        if val > 0.02 * ymax:
            ax2.text(cx, val * 0.45, f'{val:.1e}', ha='center', va='center',
                     fontsize=7.5, color='white', fontweight='bold')
        else:
            ax2.text(cx, val * 1.6, f'{val:.1e}', ha='center', va='bottom', fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
