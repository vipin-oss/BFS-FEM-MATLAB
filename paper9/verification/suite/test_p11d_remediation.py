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
