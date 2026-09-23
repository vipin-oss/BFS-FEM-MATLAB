#!/usr/bin/env python3
"""
paper9/verification/suite/test_p11d_remediation.py
P11D forensic remediation tests (A-F), added incrementally as each remediation
lands.  Every existing test must keep passing alongside these.

  A. Case-C complete-gap convergence (directly evaluated, across FE meshes x BZ grids)
  B. B2 no-PASS-on-bad-error (status fabrication regression)
  C. B2 registry consistency (single authoritative dataset)
  D. TV1 provenance class ([S] inherited/source-derived, never [C])
  E. B3 reproducibility (pinned run reproduces the manuscript values)
  F. Fig. 4 source-reference consistency (honest overlay, no fabricated source data)
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "paper9") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "paper9"))

from paper9.validation.b2_stable_tm import judge_status
from paper9.validation.b1_b2_b3_solver import BenchmarkB2


# ---------------------------------------------------------------------------
# A. Case-C complete-gap convergence (directly evaluated)
# ---------------------------------------------------------------------------

def test_a_caseC_complete_gap_convergence():
    """Delta_complete must be directly evaluated across FE meshes x BZ grids
    (min omega_4 - max omega_3 over the zone, never inferred from Delta_X),
    with the leg/path/complete hierarchy and an honest trend statement."""
    d = _load(REPO_ROOT / "paper9/results/raw/p11d_caseC_gap_convergence.json")
    definition = d["metadata"]["delta_complete_definition"].lower()
    assert "min" in definition and "max" in definition and "omega" in definition
    rows = d["convergence_matrix"]
    assert len(rows) >= 6, "min 6 (FE mesh x BZ grid) combinations required"
    assert {"4x4", "8x8", "16x16"} <= {r["fe_mesh"] for r in rows}
    assert {"4x4", "8x8", "16x16"} <= {r["fe_mesh"] for r in rows if r["N_bz"] == 41}
    for r in rows:
        # direct evaluation identity: never inferred from a path/leg quantity
        assert abs(r["delta_complete"] - (r["omega4_min"] - r["omega3_max"])) < 1e-12
        assert r["is_complete_open"] == (r["delta_complete"] > 0)
    # per-mesh directional legs and the subset hierarchy (leg >= path >= complete)
    pm = d["per_mesh_gaps"]
    for mesh in ("4x4", "8x8", "16x16"):
        g = pm[mesh]
        assert min(g["delta_GX"], g["delta_XM"], g["delta_MG"]) >= g["delta_path"] - 1e-12
        dc = g.get(f"delta_complete_at_41x41", None)
        assert dc is not None and g["delta_path"] >= dc - 1e-12
    # path-sampling control recorded
    assert "4x4_Nseg40" in d["path_sampling_control"]
    # FE-mesh trend at the finest BZ grid: data are DECREASING and the
    # manuscript must say so (no preferred outcome enforced on the physics --
    # the assertion pins the HONEST reporting of the observed run)
    seq = {r["fe_mesh"]: r["delta_complete"] for r in rows if r["N_bz"] == 41}
    assert seq["4x4"] > seq["8x8"] > seq["16x16"]
    ms = (REPO_ROOT / "paper9/latex/sections/sec06_results.tex").read_text()
    assert "2.5732" in ms, "manuscript keeps the pinned 2.5732 string (test_p7)"
    assert "not mesh-converged" in ms, "manuscript must state the honest trend"
    assert "2.7563" in ms and "overestimates it at" in ms, "ΔX vs Δcomplete distinction kept"


# ---------------------------------------------------------------------------
# B. B2 no-PASS-on-bad-error (status fabrication regression)
# ---------------------------------------------------------------------------

def test_b_judge_status_cannot_pass_on_bad_error():
    """(error >> tol AND status == PASS) must be impossible, for any inputs."""
    assert judge_status(1e-23, 1e-12) == "PASS"
    for err in (1e23, 1e11, 1e-3, 10.0, float("nan"), float("inf"), float("-inf"),
                None, "garbage"):
        for tol in (1e-12, 1e-6, 1e-9, 1.0):
            st = judge_status(err, tol)
            if st == "PASS":
                # only legal if a finite err really is <= tol
                assert isinstance(err, float) and math.isfinite(err) and err <= tol
            else:
                assert st == "FAIL"


def test_b_no_unconditional_pass_return_in_solver_sources():
    """Static guard: no `return {... "status": "PASS" ...}` literal in the solvers."""
    for rel in ("paper9/validation/b1_b2_b3_solver.py",
                "paper9/validation/b2_stable_tm.py"):
        src = (REPO_ROOT / rel).read_text()
        assert not re.search(r'"status":\s*"PASS"', src), \
            f"{rel} contains a hardcoded PASS status literal"


def test_b_b2_micro_status_is_derived():
    """The micro-scale config passes honestly: status agrees with max_error <= tol."""
    b2 = BenchmarkB2(use_micro_scale=True)
    for res in (b2.run_level1_homogeneous(), b2.run_level2_identical_reduction()):
        assert "tol" in res
        assert (res["status"] == "PASS") == (res["max_error"] <= res["tol"])
        assert res["status"] == "PASS"
        assert res["max_error"] < 1e-13


def test_b_b2_source_geometry_fails_honestly():
    """The source-geometry config (a = 0.01 m, float64 engine) must NOT report PASS:
    either it raises on overflow (honest refusal) or it FAILs with error >> tol."""
    b2 = BenchmarkB2(use_micro_scale=False)  # a_A = a_B = 0.01 m source geometry
    results = []
    for method in (b2.run_level1_homogeneous, b2.run_level2_identical_reduction):
        try:
            results.append(method())
        except OverflowError:
            continue  # honest refusal accepted
    if results:  # if it returned at all, it must be an honest FAIL
        for res in results:
            assert res["status"] != "PASS", \
                f"source-geometry float64 engine reported PASS: {res}"
            if math.isfinite(res["max_error"]):
                assert res["max_error"] > res["tol"]


def test_b_stable_engine_passes_source_geometry():
    """The stabilized engine (paper9/validation/b2_stable_tm.py) reproduces the
    identities for the source-geometry configuration honestly."""
    from paper9.validation.b2_stable_tm import StableB2
    sb = StableB2("CFG-DIM-MACRO")  # a = 0.01 m, dimensional l (source geometry)
    for res in (sb.level1_homogeneous(), sb.level2_identical_reduction()):
        assert (res["status"] == "PASS") == (res["max_error"] <= res["tol"])
        assert res["status"] == "PASS"


# ---------------------------------------------------------------------------
# C. B2 registry consistency (single authoritative dataset)
# ---------------------------------------------------------------------------

def _load(path: Path):
    with open(path) as f:
        return json.load(f)


def test_c_b2_registry_evidence_and_table_consistency():
    """benchmark_evidence.json and Table 3 cells must equal the registry run
    (regenerated, never hand-edited)."""
    reg = _load(REPO_ROOT / "paper9/results/raw/p11d_b2_gap_registry.json")
    ev = _load(REPO_ROOT / "paper9/audit/benchmark_evidence.json")
    tab = (REPO_ROOT / "paper9/tables/out/tab03_anchor_errors.tex").read_text()

    micro = reg["configs"]["CFG-DIM-MICRO"]
    gaps3 = [[round(g[0], 3), round(g[1], 3), round(g[2], 3)] for g in micro["scan"]["gaps"]]
    b2 = ev["benchmarks"]["B2"]
    assert b2["band_gaps_computed"] == gaps3
    assert b2["level1_homogeneous_error"] == micro["level1_homogeneous"]["max_error"]
    assert b2["level2_identical_reduction_error"] == micro["level2_identical_reduction"]["max_error"]
    g1 = gaps3[0]
    assert f"[{g1[0]:.3f}, {g1[1]:.3f}]" in tab, "Table 3 gap-1 cell must match the registry"
    # manuscript body text must quote the same regenerated values
    sec05 = (REPO_ROOT / "paper9/latex/sections/sec05_verification.tex").read_text()
    for g in gaps3[:5]:
        assert f"[{g[0]:.3f}, {g[1]:.3f}]" in sec05, f"sec05 must quote regenerated gap [{g[0]:.3f}, {g[1]:.3f}]"
    assert "4.10 \\times 10^{-57}" in sec05
    # all three labelled interpretations present
    assert set(reg["configs"]) == {"CFG-DIM-MICRO", "CFG-DIM-MACRO", "CFG-BAR-MACRO"}
    for cfg in reg["configs"].values():
        assert cfg["level1_homogeneous"]["status"] in ("PASS", "FAIL")
        assert "tol" in cfg["level1_homogeneous"]
    assert "AMBIGUITY" in b2["status"] or "ambiguous" in json.dumps(b2).lower()


# ---------------------------------------------------------------------------
# D. TV1 provenance class ([S], never [C])
# ---------------------------------------------------------------------------

def test_d_tv1_provenance_is_source_derived():
    tm = _load(REPO_ROOT / "paper9/audit/traceability_matrix.json")
    tv1 = tm["technical_variations"]["TV1"]
    assert "[S]" in tv1["status"], f"TV1 must be tagged [S]: {tv1['status']}"
    assert "[C]" not in tv1["status"].replace("[S]", ""), "TV1 must not carry [C]"
    res = tv1["resolution"]
    assert "Fig. 3(b)" in res or "Fig.~3(b)" in res
    assert "4(c)" in res  # documents that Fig. 4(c) annotates no c_bar/d_bar
    add = (REPO_ROOT / "paper9/audit/P3_TV_RESOLUTION.md").read_text()
    assert "CLOSED [S]" in add
    # manuscript must not present the values as author-specified Fig. 4(c) params
    sec05 = (REPO_ROOT / "paper9/latex/sections/sec05_verification.tex").read_text()
    assert "[S]" in sec05 and "inherited" in sec05


# ---------------------------------------------------------------------------
# E. B3 reproducibility (pinned run reproduces manuscript values)
# ---------------------------------------------------------------------------

def test_e_b3_pinned_run_reproducible():
    pin = _load(REPO_ROOT / "paper9/results/raw/p11d_b3_run_P11D-B3-R1.json")
    assert pin["run_id"] == "P11D-B3-R1"
    assert pin["resolution"]["N_points"] == 720
    assert pin["manuscript_values_reproduced"] is True
    assert pin["band_gaps_3dp"] == pin["manuscript_values_3dp"]
    # live recomputation from repo contents reproduces the pin
    from paper9.validation.b1_b2_b3_solver import BenchmarkB3
    b3 = BenchmarkB3()
    het = b3.compute_heterogeneous_dispersion(N_points=720)
    live3 = [[round(g[0], 3), round(g[1], 3), round(g[2], 3)] for g in het["band_gaps"][:3]]
    assert live3 == pin["band_gaps_3dp"], f"live {live3} != pin {pin['band_gaps_3dp']}"
    assert pin["level1_homogeneous"]["status"] == "PASS"
    assert pin["level2_identical_reduction"]["status"] == "PASS"
    assert pin["git_sha"], "pin must record the git SHA"


# ---------------------------------------------------------------------------
# F. Fig. 4 source-reference consistency (honest overlay; no dangling evidence)
# ---------------------------------------------------------------------------

def test_f_fig4_and_evidence_source_reference_consistency():
    fig_pdf = REPO_ROOT / "paper9/figures/out/fig04_benchmark_validation.pdf"
    assert fig_pdf.exists() and fig_pdf.read_bytes()[:5] == b"%PDF-"
    assert not (REPO_ROOT / "paper9/figures/out/fig04_anchor_overlays.pdf").exists()
    # every graphical_overlay referenced by the evidence registry must exist
    ev = _load(REPO_ROOT / "paper9/audit/benchmark_evidence.json")
    for bid, b in ev["benchmarks"].items():
        go = b.get("graphical_overlay")
        if go:
            assert (REPO_ROOT / go).exists(), f"dangling evidence file for {bid}: {go}"
    assert (REPO_ROOT / "paper9/audit/evidence/fig4c_overlay.png").exists()
    # the B3 evidence and figure must state the qualitative scope honestly
    b3 = ev["benchmarks"]["B3"]
    assert "3(b)" in b3["parameter_source"] and "[S]" in b3["parameter_source"]
    assert b3["quantitative_error_allowed"] is False and b3["quantitative_error"] is None
    figsrc = (REPO_ROOT / "paper9/figures/gen/fig04_benchmark_validation.py").read_text()
    assert "no error" in figsrc.lower()
    assert "no source trace overlay" in figsrc.lower() or "no source-curve overlay" in figsrc.lower()
    caption_src = (REPO_ROOT / "paper9/latex/sections/sec05_verification.tex").read_text()
    assert "no error percentages" in caption_src or "no source-curve overlay" in caption_src
