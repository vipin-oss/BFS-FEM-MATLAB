#!/usr/bin/env python3
"""P11 Production Run for Case C / Study S2 (Composite Phononic Crystal with Circular Inclusion).

Computes:
  1. Baseline Case C band structure on 4x4 BFS mesh along Gamma-X-M-Gamma (r0 = 0.3).
  2. Full 2D Brillouin zone grid scan to compute Delta[complete].
  3. Parametric sweeps across inclusion radii r0 in {0.20, 0.25, 0.30, 0.35, 0.40}.
  4. Saves raw results to paper9/results/raw/p11_caseC_raw.json.
"""
from __future__ import annotations

import json
import os
import sys
import numpy as np
import scipy.linalg as la

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from paper9.solver.bfs_bloch_solver import (
    assemble_mesh_KM,
    build_mesh_bloch_T,
    build_path_k,
    compute_gaps,
    mat_caseC,
    solve_bloch_mesh,
)


def run_caseC_production():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    out_dir = os.path.join(repo_root, 'paper9/results/raw')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'p11_caseC_raw.json')

    print("Starting Case C Production Run...")
    
    # 1. Baseline Case C (r0 = 0.30)
    print("  Assembling baseline Case C (r0 = 0.30)...")
    K_c, M_c = assemble_mesh_KM(4, 4, 1.0, 1.0, mat_caseC)

    # Path Gamma-X-M-Gamma with N_seg = 20 (61 points)
    k_pts, s_norm, breakpoints = build_path_k(N_seg=20, L=1.0)
    path_bands = []
    for k in k_pts:
        w, _, _ = solve_bloch_mesh(K_c, M_c, 4, 4, k[0], k[1], 1.0, 1.0, check_hermiticity=False)
        path_bands.append(w[:8].tolist())
    path_bands = np.array(path_bands)

    # 2D BZ grid scan (11x11 = 121 points)
    kxs = np.linspace(0.0, np.pi, 11)
    kys = np.linspace(0.0, np.pi, 11)
    grid_bands = []
    for kx in kxs:
        for ky in kys:
            w, _, _ = solve_bloch_mesh(K_c, M_c, 4, 4, kx, ky, 1.0, 1.0, check_hermiticity=False)
            grid_bands.append(w[:8].tolist())
    grid_bands = np.array(grid_bands)

    gap_data = compute_gaps(path_bands, grid_bands, breakpoints, N_bands=6)

    # 2. Radius Sweep: r0 in {0.20, 0.25, 0.30, 0.35, 0.40}
    radii = [0.20, 0.25, 0.30, 0.35, 0.40]
    radius_results = {}

    for r in radii:
        print(f"  Running radius sweep: r0 = {r:.2f}...")
        def mat_r(x, y):
            return mat_caseC(x, y, r0=r, Lx=1.0, Ly=1.0)

        K_r, M_r = assemble_mesh_KM(4, 4, 1.0, 1.0, mat_r)
        
        # Path
        p_bands = []
        for k in k_pts:
            w, _, _ = solve_bloch_mesh(K_r, M_r, 4, 4, k[0], k[1], 1.0, 1.0, check_hermiticity=False)
            p_bands.append(w[:8].tolist())
        p_bands = np.array(p_bands)

        # 2D Grid
        g_bands = []
        for kx in kxs:
            for ky in kys:
                w, _, _ = solve_bloch_mesh(K_r, M_r, 4, 4, kx, ky, 1.0, 1.0, check_hermiticity=False)
                g_bands.append(w[:8].tolist())
        g_bands = np.array(g_bands)

        g_res = compute_gaps(p_bands, g_bands, breakpoints, N_bands=6)
        radius_results[f"r_{int(r*100)}"] = {
            "r0": r,
            "filling_fraction": float(np.pi * (r**2)),
            "path_bands": p_bands.tolist(),
            "gap_34": g_res["gaps"][2]
        }

    output = {
        "metadata": {
            "case": "Case C",
            "study": "Study S2",
            "matrix": "Epoxy (rho=1.0, mu=1.0, lam=3.088, ell2=0.01)",
            "inclusion": "YBCO (rho=5.546, mu=25.0, lam=64.19, ell2=0.04)",
            "contrast_mu": 25.0,
            "contrast_rho": 5.546,
            "mesh": "4x4 BFS C1 rectangular elements",
            "quadrature": "4x4 Gauss-Legendre with circular indicator function chi(x,y)",
            "n_dofs_global": 200,
            "n_dofs_master": 128
        },
        "baseline": {
            "r0": 0.30,
            "filling_fraction": float(np.pi * (0.30**2)),
            "s_norm": s_norm.tolist(),
            "breakpoints": breakpoints,
            "path_bands": path_bands.tolist(),
            "gaps": gap_data["gaps"]
        },
        "radius_sweep": radius_results
    }

    with open(out_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Case C Production Completed! Raw data saved to {out_file}")


if __name__ == "__main__":
    run_caseC_production()
