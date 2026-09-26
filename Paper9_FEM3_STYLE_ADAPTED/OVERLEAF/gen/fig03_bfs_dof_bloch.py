#!/usr/bin/env python3
"""
fig03_bfs_dof_bloch.py
Generate Figure 3: BFS Hermite bicubic 32-DOF layout and Bloch phase boundary pairing.
Formulas from Blueprint Section 3.2, 4.1, Eqs. (41)-(43), (53)-(56).
Outputs: paper9/figures/out/fig03_bfs_dof_bloch.pdf
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    out_dir = os.path.join(repo_root, 'paper9/figures/out')
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, 'fig03_bfs_dof_bloch.pdf')

    plt.rcParams.update({
        'font.size': 9,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4), dpi=300)

    # Panel (a): BFS Element 32-DOF layout
    ax1.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=1.5)
    nodes = [(0, 0), (1, 0), (1, 1), (0, 1)]
    labels = ['Node 0\n(0, 0)', 'Node 1\n(L, 0)', 'Node 2\n(L, L)', 'Node 3\n(0, L)']
    dof_text = '{u, u_{,x}, u_{,y}, u_{,xy}}\n$\\times 2$ components ($u_x, u_y$)\n= 8 DOFs / node'

    for (nx, ny), lbl in zip(nodes, labels):
        ax1.scatter(nx, ny, color='crimson', s=45, zorder=5)
        ha = 'right' if nx == 0 else 'left'
        va = 'top' if ny == 0 else 'bottom'
        ox = -0.06 if nx == 0 else 0.06
        oy = -0.06 if ny == 0 else 0.06
        ax1.text(nx + ox, ny + oy, lbl, fontsize=8, ha=ha, va=va, fontweight='bold', color='crimson')

    ax1.text(0.5, 0.5, 'BFS Bicubic Hermite\n4 nodes $\\times$ 8 DOFs\n= 32 DOFs / cell\n$C^1$-conforming',
             ha='center', va='center', fontsize=8.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6f2ff', edgecolor='#1f77b4', lw=1.2))

    ax1.set_xlim(-0.35, 1.35)
    ax1.set_ylim(-0.35, 1.35)
    ax1.set_aspect('equal')
    ax1.set_title('(a) BFS Hermite Element DOFs', fontsize=10)
    ax1.axis('off')

    # Panel (b): Bloch Phase Boundary Reduction
    ax2.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=1.5)
    # Left to right coupling
    ax2.annotate('', xy=(1.0, 0.5), xytext=(0.0, 0.5),
                 arrowprops=dict(arrowstyle="->", color='#1f77b4', lw=2.0, shrinkA=5, shrinkB=5))
    ax2.text(0.5, 0.55, '$\\mu_x = e^{\\mathrm{i} k_x L}$ on all 4 DOF types',
             ha='center', va='bottom', color='#1f77b4', fontsize=8.5, fontweight='bold')

    # Bottom to top coupling
    ax2.annotate('', xy=(0.5, 1.0), xytext=(0.5, 0.0),
                 arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2.0, shrinkA=5, shrinkB=5))
    ax2.text(0.52, 0.25, '$\\mu_y = e^{\\mathrm{i} k_y L}$\non all DOFs',
             ha='left', va='center', color='#2ca02c', fontsize=8.5, fontweight='bold')

    # Reduced DOFs
    ax2.scatter(0, 0, color='darkmagenta', s=60, zorder=6, label='Retained master DOFs (Node 0, 8 DOFs)')
    ax2.scatter([1, 1, 0], [0, 1, 1], color='gray', s=35, zorder=5, label='Slave boundary DOFs (24 DOFs)')

    ax2.set_xlim(-0.35, 1.35)
    ax2.set_ylim(-0.35, 1.35)
    ax2.set_aspect('equal')
    ax2.set_title('(b) Bloch Boundary Coupling', fontsize=10)
    ax2.axis('off')
    ax2.legend(loc='lower center', frameon=True, framealpha=0.9, fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Generated {out_pdf}')

if __name__ == '__main__':
    main()
