#!/usr/bin/env python3
"""
paper9/verification/suite/test_p11b_forensic_remediation.py
Automated test suite verifying the complete remediation under P11B:
  - Benchmark B1: Level 1 homogeneous & Level 2 identical reduction.
  - Benchmark B2: Level 1 homogeneous & Level 2 identical reduction.
  - Benchmark B3: Level 1 homogeneous, Level 2 identical reduction, & branch calculation.
  - Case C Mesh Refinement: 4x4, 8x8, and 16x16 complete gap survival.
  - Case C Gauss Quadrature Sensitivity: 4x4 vs 6x6 Gauss points.
  - Case C Hierarchy: Delta[leg] >= Delta[path] >= Delta[complete].
  - Case C Complete 2D Band Gap verification on refined zone grids.
  - Table 2 Parameter Registry Provenance: Every parameter tagged [C], [A], or [S].
  - Machine-readable benchmark evidence policy integrity.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
import numpy as np
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "paper9") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "paper9"))

from paper9.validation.b1_b2_b3_solver import BenchmarkB1, BenchmarkB2, BenchmarkB3
from paper9.solver.bfs_bloch_solver import (
    assemble_mesh_KM,
    mat_caseC,
    solve_bloch_mesh,
    compute_gaps,
)
from paper9.production.p11_caseC_convergence import assemble_mesh_KM_ngauss


# ------------------------------------------------------------------------------
# 1. BENCHMARK B1 TESTS
# ------------------------------------------------------------------------------

def test_b1_solver_level1_and_level2():
    """Verify Benchmark B1 Level 1 homogeneous identity and Level 2 reductions."""
    b1 = BenchmarkB1()
    
    # Level 1 Homogeneous
    res_l1 = b1.run_level1_homogeneous()
    assert res_l1["status"] == "PASS"
    assert res_l1["max_error"] < 1e-14, f"B1 Level 1 error too large: {res_l1['max_error']}"
    
    # Level 2 Identical Reduction
    res_l2_id = b1.run_level2_identical_reduction()
    assert res_l2_id["status"] == "PASS"
    assert res_l2_id["max_error"] < 1e-14, f"B1 Level 2 id error too large: {res_l2_id['max_error']}"
    
    # Level 2 Heterogeneous Bilayer TM vs Rytov
    het = b1.compute_heterogeneous_dispersion(N_points=200)
    assert het["tr_rytov_max_diff"] < 1e-14, f"B1 TM vs Rytov diff: {het['tr_rytov_max_diff']}"
    assert len(het["band_gaps"]) >= 3
    # Check first gap location near [0.48, 0.52]
    gap1 = het["band_gaps"][0]
    assert 0.45 < gap1[0] < 0.50
    assert 0.50 < gap1[1] < 0.55


# ------------------------------------------------------------------------------
# 2. BENCHMARK B2 TESTS
# ------------------------------------------------------------------------------

def test_b2_solver_level1_and_level2():
    """Verify Benchmark B2 Level 1 homogeneous identity and Level 2 reductions."""
    b2 = BenchmarkB2(use_micro_scale=True)
    
    # Level 1 Homogeneous
    res_l1 = b2.run_level1_homogeneous()
    assert res_l1["status"] == "PASS"
    assert res_l1["max_error"] < 1e-13, f"B2 Level 1 error too large: {res_l1['max_error']}"
    
    # Level 2 Identical Reduction
    res_l2_id = b2.run_level2_identical_reduction()
    assert res_l2_id["status"] == "PASS"
    assert res_l2_id["max_error"] < 1e-13, f"B2 Level 2 id error too large: {res_l2_id['max_error']}"
    
    # Level 2 Heterogeneous Bilayer
    het = b2.compute_heterogeneous_dispersion(N_points=50)
    assert het["branches_count"] > 10
    assert len(het["band_gaps"]) >= 1


# ------------------------------------------------------------------------------
# 3. BENCHMARK B3 TESTS
# ------------------------------------------------------------------------------

def test_b3_solver_level1_level2_and_branches():
    """Verify Benchmark B3 Level 1, Level 2, and heterogeneous branch solves."""
    b3 = BenchmarkB3()
    
    # Level 1 Homogeneous
    res_l1 = b3.run_level1_homogeneous()
    assert res_l1["status"] == "PASS"
    assert res_l1["max_error"] < 1e-12, f"B3 Level 1 error too large: {res_l1['max_error']}"
    
    # Level 2 Identical Reduction
    res_l2_id = b3.run_level2_identical_reduction()
    assert res_l2_id["status"] == "PASS"
    assert res_l2_id["max_error"] < 1e-12, f"B3 Level 2 id error too large: {res_l2_id['max_error']}"
    
    # Heterogeneous Bilayer full dispersion solve
    het = b3.compute_heterogeneous_dispersion(N_points=100)
    assert het["branches_count"] > 20
    assert len(het["band_gaps"]) >= 2
    # Verify stop band 1 interval [0.34, 1.02]
    sb1 = het["band_gaps"][0]
    assert 0.30 < sb1[0] < 0.38
    assert 0.98 < sb1[1] < 1.06


# ------------------------------------------------------------------------------
# 4. CASE C CONVERGENCE TESTS (MESH & QUADRATURE)
# ------------------------------------------------------------------------------

def test_caseC_convergence_mesh_and_gap_survival():
    """Verify Case C complete band gap survives mesh refinement across 4x4, 8x8, 16x16."""
    # 4x4 mesh
    K4, M4 = assemble_mesh_KM(4, 4, 1.0, 1.0, mat_caseC)
    w_X_4, _, _ = solve_bloch_mesh(K4, M4, 4, 4, np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)
    gap_X_4 = float(w_X_4[3] - w_X_4[2])
    assert gap_X_4 > 2.5, f"4x4 gap at X is too small: {gap_X_4}"
    
    # 8x8 mesh
    K8, M8 = assemble_mesh_KM(8, 8, 1.0, 1.0, mat_caseC)
    w_X_8, _, _ = solve_bloch_mesh(K8, M8, 8, 8, np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)
    gap_X_8 = float(w_X_8[3] - w_X_8[2])
    assert gap_X_8 > 2.0, f"8x8 gap at X is too small: {gap_X_8}"
    
    # Load 16x16 mesh convergence artifact
    conv_file = REPO_ROOT / "paper9" / "results" / "raw" / "p11_caseC_convergence.json"
    assert conv_file.exists(), f"Convergence raw file missing: {conv_file}"
    with open(conv_file) as f:
        conv_data = json.load(f)
    mesh_16 = conv_data["mesh_convergence"]["16x16"]
    assert mesh_16["gap_at_X"] > 2.0, f"16x16 gap at X is not open: {mesh_16['gap_at_X']}"


def test_caseC_quadrature_sensitivity():
    """Verify Case C band gap invariance between 4x4 and 6x6 Gauss points."""
    K_q4, M_q4 = assemble_mesh_KM_ngauss(4, 4, 1.0, 1.0, mat_caseC, n_gauss=4)
    w_q4, _, _ = solve_bloch_mesh(K_q4, M_q4, 4, 4, np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)
    gap_q4 = float(w_q4[3] - w_q4[2])
    
    K_q6, M_q6 = assemble_mesh_KM_ngauss(4, 4, 1.0, 1.0, mat_caseC, n_gauss=6)
    w_q6, _, _ = solve_bloch_mesh(K_q6, M_q6, 4, 4, np.pi, 0.0, 1.0, 1.0, check_hermiticity=False)
    gap_q6 = float(w_q6[3] - w_q6[2])
    
    rel_diff = abs(gap_q6 - gap_q4) / gap_q4
    assert rel_diff < 0.02, f"Quadrature sensitivity exceeds 2%: {rel_diff:.4f}"


# ------------------------------------------------------------------------------
# 5. CASE C HIERARCHY & 2D COMPLETE GAP TESTS
# ------------------------------------------------------------------------------

def test_caseC_hierarchy_inequalities():
    """Verify strict directional-to-complete subset inequalities for Case C."""
    conv_file = REPO_ROOT / "paper9" / "results" / "raw" / "p11_caseC_convergence.json"
    with open(conv_file) as f:
        conv_data = json.load(f)
    ineq = conv_data["inequality_audit"]
    
    d_GX = ineq["delta_GX"]
    d_XM = ineq["delta_XM"]
    d_MG = ineq["delta_MG"]
    d_path = ineq["delta_path"]
    d_comp = ineq["delta_complete"]
    
    # Mathematical subset relations:
    # Delta[leg] >= Delta[path] >= Delta[complete]
    assert d_GX >= d_path - 1e-9, f"Delta[G-X] {d_GX} < Delta[path] {d_path}"
    assert d_XM >= d_path - 1e-9, f"Delta[X-M] {d_XM} < Delta[path] {d_path}"
    assert d_MG >= d_path - 1e-9, f"Delta[M-G] {d_MG} < Delta[path] {d_path}"
    assert d_path >= d_comp - 1e-9, f"Delta[path] {d_path} < Delta[complete] {d_comp}"
    assert min(d_GX, d_XM, d_MG) >= d_path - 1e-9


def test_caseC_complete_gap_on_refined_bz():
    """Verify complete band gap remains open on refined 21x21 zone grid."""
    conv_file = REPO_ROOT / "paper9" / "results" / "raw" / "p11_caseC_convergence.json"
    with open(conv_file) as f:
        conv_data = json.load(f)
    bz_21 = conv_data["bz_refinement"]["21x21"]
    assert bz_21["is_complete_open"] is True
    assert bz_21["delta_complete"] > 2.0
    assert bz_21["norm_gap_pct"] > 30.0


# ------------------------------------------------------------------------------
# 6. PARAMETER PROVENANCE & POLICY INTEGRITY
# ------------------------------------------------------------------------------

def test_table2_parameter_provenance_tags():
    """Verify that every parameter in Table 2 / params_master.yaml has a valid provenance tag."""
    params_file = REPO_ROOT / "paper9" / "params" / "params_master.yaml"
    assert params_file.exists(), f"Parameters file missing: {params_file}"
    with open(params_file) as f:
        params_dict = yaml.safe_load(f)["parameters"]
    
    valid_tags = {"[C]", "[A]", "[S]"}
    for param_name, data in params_dict.items():
        assert "tag" in data, f"Parameter {param_name} lacks 'tag'"
        tag = data["tag"]
        assert tag in valid_tags, f"Parameter {param_name} has invalid tag: {tag}"
        assert "source" in data and len(str(data["source"]).strip()) > 0, f"Parameter {param_name} missing source"
        assert "description" in data and len(str(data["description"]).strip()) > 0, f"Parameter {param_name} missing description"


def test_benchmark_evidence_json_policy_integrity():
    """Verify machine-readable benchmark evidence record adheres to evidence hierarchy."""
    policy_file = REPO_ROOT / "paper9" / "audit" / "benchmark_evidence.json"
    assert policy_file.exists(), f"Benchmark evidence file missing: {policy_file}"
    with open(policy_file) as f:
        policy = json.load(f)
    
    bmarks = policy["benchmarks"]
    for b_id in ["B1", "B2", "B3"]:
        assert b_id in bmarks, f"Benchmark {b_id} missing from evidence policy"
        entry = bmarks[b_id]
        assert entry["reference_data_available"] is False, f"{b_id} falsely claims reference data available"
        assert entry["quantitative_error_allowed"] is False, f"{b_id} allows manufactured quantitative error"
        assert entry["quantitative_error"] is None, f"{b_id} has non-null quantitative error"
        assert entry["level1_homogeneous_error"] < 1e-12, f"{b_id} Level 1 error too large"
        assert entry["level2_identical_reduction_error"] < 1e-12, f"{b_id} Level 2 error too large"
        assert "GRAPHICAL_ONLY" in entry["status"] or "PARTIAL" in entry["status"]
        assert len(entry["blocking_reason"]) > 10
