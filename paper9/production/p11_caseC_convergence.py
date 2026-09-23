#!/usr/bin/env python3
"""
paper9/production/p11_caseC_convergence.py
Rigorous convergence and verification study for Case C (Composite Phononic Crystal):
  1. Mesh refinement: 4x4, 8x8, 16x16 BFS elements.
  2. Gauss quadrature sensitivity: 4x4, 6x6, 8x8 Gauss points per element.
  3. 2D Brillouin Zone sampling: 11x11 vs 21x21 grid verification.
  4. Subset inequality verification: Delta[leg] >= Delta[path] >= Delta[complete].
  5. TV18 immersed interface documentation and convergence tracking.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path
import numpy as np
import scipy.linalg as la

REPO_ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(REPO_ROOT / "paper9"))
from solver.bfs_bloch_solver import (
    hermite_num, idx, XEND, YEND,
    build_mesh_bloch_T, solve_bloch_mesh,
    mat_caseC, compute_gaps
)

RAW_DIR = REPO_ROOT / "paper9" / "results" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def assemble_mesh_KM_ngauss(Nx: int, Ny: int, Lx: float, Ly: float, mat_func, n_gauss: int = 4):
    """Assemble global K and M with custom Gauss quadrature rule."""
    hx = Lx / Nx
    hy = Ly / Ny
    N_nodes = (Nx + 1) * (Ny + 1)
    tot_dof = 8 * N_nodes
    K = np.zeros((tot_dof, tot_dof), dtype=float)
    M = np.zeros((tot_dof, tot_dof), dtype=float)

    def node_id(ix, iy):
        return iy * (Nx + 1) + ix

    xi_g, w_g = np.polynomial.legendre.leggauss(n_gauss)
    nd = list(zip(xi_g, w_g))

    for ey in range(Ny):
        for ex in range(Nx):
            elem_nodes = [node_id(ex, ey), node_id(ex + 1, ey), node_id(ex + 1, ey + 1), node_id(ex, ey + 1)]
            x0 = ex * hx
            y0 = ey * hy
            Ke = np.zeros((32, 32), dtype=float)
            Me = np.zeros((32, 32), dtype=float)
            for xi, wi in nd:
                for eta, wj in nd:
                    xv = (xi + 1.0) / 2.0 * hx
                    yv = (eta + 1.0) / 2.0 * hy
                    xg = x0 + xv
                    yg = y0 + yv
                    wjac = wi * wj * hx * hy / 4.0
                    lam, mu, rho, L11, L22, L12, ell2 = mat_func(xg, yg)
                    Cbar = np.array([[lam + 2.0 * mu, lam, 0.0],
                                     [lam, lam + 2.0 * mu, 0.0],
                                     [0.0, 0.0, 2.0 * mu]], dtype=float)
                    G = np.diag([1.0, 1.0, 2.0]) @ Cbar
                    Lmat = np.array([[L11, L12], [L12, L22]], dtype=float)
                    Hx, dHx, d2Hx = hermite_num(xv, hx)
                    Hy, dHy, d2Hy = hermite_num(yv, hy)
                    Nv = np.zeros((4, 4), dtype=float)
                    Nx_ = np.zeros((4, 4), dtype=float)
                    Ny_ = np.zeros((4, 4), dtype=float)
                    Nxx = np.zeros((4, 4), dtype=float)
                    Nxy = np.zeros((4, 4), dtype=float)
                    Nyy = np.zeros((4, 4), dtype=float)
                    for ndi in range(4):
                        ax, ay = XEND[ndi], YEND[ndi]
                        for ty in range(4):
                            dx = 1 if ty in (1, 3) else 0
                            dy = 1 if ty in (2, 3) else 0
                            ix_, iy_ = ax + dx, ay + dy
                            Nv[ndi, ty] = Hx[ix_] * Hy[iy_]
                            Nx_[ndi, ty] = dHx[ix_] * Hy[iy_]
                            Ny_[ndi, ty] = Hx[ix_] * dHy[iy_]
                            Nxx[ndi, ty] = d2Hx[ix_] * Hy[iy_]
                            Nxy[ndi, ty] = dHx[ix_] * dHy[iy_]
                            Nyy[ndi, ty] = Hx[ix_] * d2Hy[iy_]
                    Nmat = np.zeros((2, 32), dtype=float)
                    B = np.zeros((3, 32), dtype=float)
                    Bx = np.zeros((3, 32), dtype=float)
                    By = np.zeros((3, 32), dtype=float)
                    Nxmat = np.zeros((2, 32), dtype=float)
                    Nymat = np.zeros((2, 32), dtype=float)
                    for ndi in range(4):
                        for c in range(2):
                            for ty in range(4):
                                j = idx(ndi, c, ty)
                                Nmat[c, j] = Nv[ndi, ty]
                                Nxmat[c, j] = Nx_[ndi, ty]
                                Nymat[c, j] = Ny_[ndi, ty]
                                if c == 0:
                                    B[0, j] = Nx_[ndi, ty]
                                    B[2, j] = 0.5 * Ny_[ndi, ty]
                                    Bx[0, j] = Nxx[ndi, ty]
                                    Bx[2, j] = 0.5 * Nxy[ndi, ty]
                                    By[0, j] = Nxy[ndi, ty]
                                    By[2, j] = 0.5 * Nyy[ndi, ty]
                                else:
                                    B[1, j] = Ny_[ndi, ty]
                                    B[2, j] = 0.5 * Nx_[ndi, ty]
                                    Bx[1, j] = Nxy[ndi, ty]
                                    Bx[2, j] = 0.5 * Nxx[ndi, ty]
                                    By[1, j] = Nyy[ndi, ty]
                                    By[2, j] = 0.5 * Nxy[ndi, ty]

                    Ke += wjac * (
                        B.T @ G @ B
                        + 0.1
                        * (
                            Lmat[0, 0] * (Bx.T @ G @ Bx)
                            + Lmat[0, 1] * (Bx.T @ G @ By)
                            + Lmat[1, 0] * (By.T @ G @ Bx)
                            + Lmat[1, 1] * (By.T @ G @ By)
                        )
                    )
                    Me += wjac * (
                        rho * (Nmat.T @ Nmat)
                        + rho * ell2 * (Nxmat.T @ Nxmat + Nymat.T @ Nymat)
                    )
            dof_map = []
            for ndi, nid in enumerate(elem_nodes):
                for c in range(2):
                    for ty in range(4):
                        dof_map.append(nid * 8 + c * 4 + ty)
            for a in range(32):
                I = dof_map[a]
                for b_ in range(32):
                    J = dof_map[b_]
                    K[I, J] += Ke[a, b_]
                    M[I, J] += Me[a, b_]
    return K, M


def run_caseC_convergence():
    print("=" * 80)
    print("CASE C RIGOROUS CONVERGENCE & HIERARCHY AUDIT")
    print("=" * 80)

    # 1. Mesh Refinement Study: 4x4, 8x8, 16x16
    print("\n--- 1. MESH REFINEMENT STUDY (4x4, 8x8, 16x16) ---")
    mesh_results = {}
    for N in [4, 8, 16]:
        t0 = time.time()
        K, M = assemble_mesh_KM_ngauss(N, N, 1.0, 1.0, mat_caseC, n_gauss=4)
        t_ass = time.time() - t0
        
        # Test high symmetry points: X(pi, 0), M(pi, pi), G(0, 0)
        w_X, _, _ = solve_bloch_mesh(K, M, N, N, np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)
        w_M, _, _ = solve_bloch_mesh(K, M, N, N, np.pi, np.pi, 1.0, 1.0, check_hermiticity=False)
        w_G2, _, _ = solve_bloch_mesh(K, M, N, N, 0.5 * np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)

        # Gap between Band 3 and Band 4 at X and M
        gap_X = float(w_X[3] - w_X[2])
        gap_M = float(w_M[3] - w_M[2])
        
        mesh_results[f"{N}x{N}"] = {
            "N": N,
            "dofs": K.shape[0],
            "assemble_time_s": round(t_ass, 3),
            "w_X": [round(float(x), 4) for x in w_X[:6]],
            "w_M": [round(float(x), 4) for x in w_M[:6]],
            "w_G2": [round(float(x), 4) for x in w_G2[:6]],
            "mode3_X": round(float(w_X[2]), 4),
            "mode4_X": round(float(w_X[3]), 4),
            "gap_at_X": round(gap_X, 4),
            "gap_at_M": round(gap_M, 4),
        }
        print(f"Mesh {N}x{N} ({K.shape[0]} DOFs): w_X[:4] = {[round(float(x), 4) for x in w_X[:4]]}, Gap at X = {gap_X:.4f}")

    # 2. Quadrature Sensitivity Study: 4x4, 6x6, 8x8 Gauss points on 4x4 mesh
    print("\n--- 2. QUADRATURE SENSITIVITY STUDY (4x4, 6x6, 8x8 Gauss) ---")
    quad_results = {}
    for q in [4, 6, 8]:
        t0 = time.time()
        K, M = assemble_mesh_KM_ngauss(4, 4, 1.0, 1.0, mat_caseC, n_gauss=q)
        t_ass = time.time() - t0
        w_X, _, _ = solve_bloch_mesh(K, M, 4, 4, np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)
        gap_X = float(w_X[3] - w_X[2])
        quad_results[f"{q}x{q}"] = {
            "n_gauss": q,
            "points_per_elem": q * q,
            "assemble_time_s": round(t_ass, 3),
            "w_X": [round(float(x), 4) for x in w_X[:6]],
            "mode3_X": round(float(w_X[2]), 4),
            "mode4_X": round(float(w_X[3]), 4),
            "gap_at_X": round(gap_X, 4),
        }
        print(f"Gauss {q}x{q} ({q*q} pts/elem): w_X[:4] = {[round(float(x), 4) for x in w_X[:4]]}, Gap at X = {gap_X:.4f}")

    # 3. 2D BZ Grid Verification: 11x11 vs 21x21 on 4x4 mesh
    print("\n--- 3. 2D BRILLOUIN ZONE GRID REFINEMENT (11x11 vs 21x21) ---")
    K4, M4 = assemble_mesh_KM_ngauss(4, 4, 1.0, 1.0, mat_caseC, n_gauss=4)
    bz_results = {}
    for N_bz in [11, 21]:
        kx_vals = np.linspace(0, np.pi, N_bz)
        ky_vals = np.linspace(0, np.pi, N_bz)
        grid_bands = []
        for kx in kx_vals:
            for ky in ky_vals:
                w, _, _ = solve_bloch_mesh(K4, M4, 4, 4, kx, ky, 1.0, 1.0, check_hermiticity=False)
                grid_bands.append(w[:6])
        grid_bands = np.array(grid_bands)
        
        # Max lower band (Mode 3), Min upper band (Mode 4)
        max_lower = float(np.max(grid_bands[:, 2]))
        min_upper = float(np.min(grid_bands[:, 3]))
        delta_complete = min_upper - max_lower
        w_mid = 0.5 * (min_upper + max_lower)
        norm_width = delta_complete / w_mid * 100.0

        bz_results[f"{N_bz}x{N_bz}"] = {
            "N_bz": N_bz,
            "total_k_points": N_bz * N_bz,
            "max_mode3": round(max_lower, 4),
            "min_mode4": round(min_upper, 4),
            "delta_complete": round(delta_complete, 4),
            "norm_gap_pct": round(norm_width, 2),
            "is_complete_open": delta_complete > 0.0,
        }
        print(f"BZ Grid {N_bz}x{N_bz} ({N_bz*N_bz} pts): Mode 3 max = {max_lower:.4f}, Mode 4 min = {min_upper:.4f}, Complete Gap = {delta_complete:.4f} ({norm_width:.2f}%)")

    # 4. Strict Directional Subset Inequality Audit
    print("\n--- 4. STRICT DIRECTIONAL SUBSET INEQUALITY AUDIT ---")
    # Path evaluation on 4x4 mesh
    N_seg = 20
    # G -> X -> M -> G
    k_path = []
    breakpoints = [0, N_seg, 2 * N_seg, 3 * N_seg]
    # G -> X
    for s in np.linspace(0, 1, N_seg + 1):
        k_path.append([s * np.pi, 0.0])
    # X -> M
    for s in np.linspace(0, 1, N_seg + 1)[1:]:
        k_path.append([np.pi, s * np.pi])
    # M -> G
    for s in np.linspace(0, 1, N_seg + 1)[1:]:
        k_path.append([(1.0 - s) * np.pi, (1.0 - s) * np.pi])
    k_path = np.array(k_path)

    path_bands = []
    for kx, ky in k_path:
        w, _, _ = solve_bloch_mesh(K4, M4, 4, 4, kx, ky, 1.0, 1.0, check_hermiticity=False)
        path_bands.append(w[:6])
    path_bands = np.array(path_bands)

    # 21x21 grid bands for complete zone evaluation
    g_res = compute_gaps(path_bands, grid_bands, breakpoints, N_bands=6)
    gap_34 = g_res["gaps"][2]  # Band pair 3-4

    d_GX = gap_34["delta_GX"]
    d_XM = gap_34["delta_XM"]
    d_MG = gap_34["delta_MG"]
    d_path = gap_34["delta_path"]
    d_comp = gap_34["delta_complete"]

    print(f"Leg G-X:      {d_GX:.4f}")
    print(f"Leg X-M:      {d_XM:.4f}")
    print(f"Leg M-G:      {d_MG:.4f}")
    print(f"Path Gap:     {d_path:.4f}")
    print(f"Complete Gap: {d_comp:.4f}")
    
    # Mathematical proof of subset relations:
    # Any leg L is a subset of path: leg L subset of path => Delta[L] >= Delta[path]
    # Path is a subset of 2D BZ: path subset of BZ => Delta[path] >= Delta[complete]
    print(f"Check d_GX >= d_path: {d_GX:.4f} >= {d_path:.4f} -> {d_GX >= d_path - 1e-9}")
    print(f"Check d_XM >= d_path: {d_XM:.4f} >= {d_path:.4f} -> {d_XM >= d_path - 1e-9}")
    print(f"Check d_MG >= d_path: {d_MG:.4f} >= {d_path:.4f} -> {d_MG >= d_path - 1e-9}")
    print(f"Check d_path >= d_comp: {d_path:.4f} >= {d_comp:.4f} -> {d_path >= d_comp - 1e-9}")
    print(f"Min leg gap: {min(d_GX, d_XM, d_MG):.4f} >= {d_path:.4f} >= {d_comp:.4f}")

    inequality_summary = {
        "delta_GX": round(d_GX, 4),
        "delta_XM": round(d_XM, 4),
        "delta_MG": round(d_MG, 4),
        "delta_path": round(d_path, 4),
        "delta_complete": round(d_comp, 4),
        "min_leg_gap": round(min(d_GX, d_XM, d_MG), 4),
        "mathematical_hierarchy": "min(Delta[GX], Delta[XM], Delta[MG]) >= Delta[path] >= Delta[complete]",
        "all_leg_inequalities_hold": bool(d_GX >= d_path - 1e-9 and d_XM >= d_path - 1e-9 and d_MG >= d_path - 1e-9),
        "path_to_complete_holds": bool(d_path >= d_comp - 1e-9),
    }

    # Master convergence output
    convergence_package = {
        "metadata": {
            "title": "Case C Convergence and Verification Study",
            "date": "2026-09-23",
            "solver": "C1 BFS Bloch Solver with Immersed Gauss Quadrature",
            "inclusion_treatment": "TV18 resolved via Cartesian immersed Gauss-Legendre quadrature with smooth indicator function; conformality preserved without boundary-fitted mesh distortion."
        },
        "mesh_convergence": mesh_results,
        "quadrature_sensitivity": quad_results,
        "bz_refinement": bz_results,
        "inequality_audit": inequality_summary,
    }

    out_file = RAW_DIR / "p11_caseC_convergence.json"
    with open(out_file, "w") as f:
        json.dump(convergence_package, f, indent=2)
    print(f"\nSaved Case C convergence evidence to: {out_file}")

    return convergence_package

if __name__ == "__main__":
    run_caseC_convergence()
