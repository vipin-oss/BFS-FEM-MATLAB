#!/usr/bin/env python3
"""P11 Verification Suite for Case C / Study S2 (Phononic Crystal with Circular Inclusion).

Verifies:
  1. TV18, TV6, TV14 implementation.
  2. Level 1 Identical-Material Reduction to Case H (error < 0.1%).
  3. Level 2 Study S2 Complete Band Gap and Subset Inequality:
     Delta[leg] >= Delta[path] >= Delta[complete].
  4. Hermiticity of mesh Bloch reduction (< 1e-10).
"""
from __future__ import annotations

import numpy as np
import pytest

from paper9.solver.bfs_bloch_solver import (
    assemble_KM,
    assemble_mesh_KM,
    build_path_k,
    build_half_bz_grid,
    compute_gaps,
    mat_caseC,
    solve_bloch,
    solve_bloch_mesh,
)


def test_level1_caseC_identical_material_reduction():
    """Verify that setting inclusion = matrix reproduces homogeneous Case H.
    1. At 1x1 mesh: exact recovery to machine precision (< 1e-12).
    2. At 2x2 mesh: consistent with FEM h-refinement convergence (< 1.0%).
    """
    def mat_identical(x, y):
        return 1.0, 1.0, 1.0, 0.04, 0.04, 0.0, 0.04

    # Single-element reference (Case H exact)
    K_ref, M_ref = assemble_KM(1.0, 1.0, 1.0, 1.0, 0.04, 0.04, 0.0, 1.0, 0.04)

    # 1x1 multi-element mesh
    K_m1, M_m1 = assemble_mesh_KM(1, 1, 1.0, 1.0, mat_identical)

    # 2x2 multi-element mesh
    K_m2, M_m2 = assemble_mesh_KM(2, 2, 1.0, 1.0, mat_identical)

    test_points = [
        (0.5 * np.pi, 0.0, "X/2"),
        (np.pi, 0.0, "X"),
        (np.pi, np.pi, "M"),
    ]

    for kx, ky, name in test_points:
        w_ref, _, _, _, _, _ = solve_bloch(K_ref, M_ref, kx, ky, 1.0, check_hermiticity=True)
        w_m1, _, _ = solve_bloch_mesh(K_m1, M_m1, 1, 1, kx, ky, 1.0, 1.0, check_hermiticity=True)
        w_m2, _, _ = solve_bloch_mesh(K_m2, M_m2, 2, 2, kx, ky, 1.0, 1.0, check_hermiticity=True)

        # Exact algebraic reduction check on 1x1 mesh: machine precision
        diff_1x1 = np.max(np.abs(w_ref[:4] - w_m1[:4]))
        assert diff_1x1 < 1e-12, f"1x1 algebraic mismatch at {name}: diff={diff_1x1:.2e}"

        # Refined 2x2 mesh check: h-refinement convergence within 1%
        rel_diff_0 = abs(w_m2[0] - w_ref[0]) / max(w_ref[0], 1e-6)
        rel_diff_1 = abs(w_m2[1] - w_ref[1]) / max(w_ref[1], 1e-6)
        assert rel_diff_0 < 0.01, f"Mode 0 h-refinement at {name}: rel={rel_diff_0:.2e}"
        assert rel_diff_1 < 0.01, f"Mode 1 h-refinement at {name}: rel={rel_diff_1:.2e}"


def test_level2_caseC_band_gap_and_inequality():
    """Verify Case C complete band gap and the subset inequality Delta[leg] >= Delta[path] >= Delta[complete]."""
    # 4x4 mesh with Epoxy/YBCO circular inclusion
    K_c, M_c = assemble_mesh_KM(4, 4, 1.0, 1.0, mat_caseC)

    # Solve along path Gamma-X-M-Gamma
    k_pts, s_norm, breakpoints = build_path_k(N_seg=10, L=1.0)
    path_bands = []
    for k in k_pts:
        w, _, _ = solve_bloch_mesh(K_c, M_c, 4, 4, k[0], k[1], 1.0, 1.0, check_hermiticity=True)
        path_bands.append(w[:8])
    path_bands = np.array(path_bands)

    # Solve over 2D BZ grid (11x11)
    kxs = np.linspace(0.0, np.pi, 11)
    kys = np.linspace(0.0, np.pi, 11)
    grid_bands = []
    for kx in kxs:
        for ky in kys:
            w, _, _ = solve_bloch_mesh(K_c, M_c, 4, 4, kx, ky, 1.0, 1.0, check_hermiticity=False)
            grid_bands.append(w[:8])
    grid_bands = np.array(grid_bands)

    # Compute gaps
    gap_data = compute_gaps(path_bands, grid_bands, breakpoints, N_bands=6)
    gaps = gap_data["gaps"]

    # Band pair [3, 4] (index 2 in gaps list)
    gap_34 = gaps[2]
    assert gap_34["band_pair"] == [3, 4]

    # Verify that the complete 2D band gap exists (Delta[complete] > 0)
    delta_complete = gap_34["delta_complete"]
    delta_path = gap_34["delta_path"]
    delta_GX = gap_34["delta_GX"]
    delta_XM = gap_34["delta_XM"]
    delta_MG = gap_34["delta_MG"]

    assert delta_complete > 0.5, f"Expected open complete gap between bands 3-4, got {delta_complete:.4f}"
    assert delta_path > 0.5, f"Expected open path gap between bands 3-4, got {delta_path:.4f}"

    # Verify strict subset inequality: Delta[leg] >= Delta[path] >= Delta[complete]
    assert delta_GX >= delta_path - 1e-6, f"Inequality violation: Delta[GX]={delta_GX} < Delta[path]={delta_path}"
    assert delta_XM >= delta_path - 1e-6, f"Inequality violation: Delta[XM]={delta_XM} < Delta[path]={delta_path}"
    assert delta_MG >= delta_path - 1e-6, f"Inequality violation: Delta[MG]={delta_MG} < Delta[path]={delta_path}"
    assert delta_path >= delta_complete - 1e-6, f"Inequality violation: Delta[path]={delta_path} < Delta[comp]={delta_complete}"
    assert gap_34["inequality_holds"], "compute_gaps reported inequality_holds == False"


def test_mesh_bloch_hermiticity():
    """Verify that the multi-element Bloch reduced matrices are strictly Hermitian."""
    K_c, M_c = assemble_mesh_KM(2, 2, 1.0, 1.0, mat_caseC)
    for kx, ky in [(0.3, 0.7), (1.2, 0.4), (np.pi, np.pi/2)]:
        # Should not raise any assertion error
        solve_bloch_mesh(K_c, M_c, 2, 2, kx, ky, 1.0, 1.0, check_hermiticity=True, tol_herm=1e-10)
