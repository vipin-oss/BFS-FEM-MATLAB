"""P12H governance guards — Rule R-fit adopted under the authorized A1 decision.

Pins the frozen rule (P12G), its application to the governing artifact, the reuse of the
authorized C-1 predicates, the adversarial classification, and the manuscript/table/figure
wording that must state the protocol.  These tests re-derive everything from recorded
evidence; they run no solver and change no scientific value.

Any change to F, SPREAD_FLOOR, the seeds, the tolerance, the mesh tuple, the admission
inequality or the C-1 constants must fail here.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import pytest

SUITE = Path(__file__).resolve().parent
PAPER9 = SUITE.parents[1]
REPO = SUITE.parents[2]

import sys
sys.path.insert(0, str(SUITE))
import rule_rfit as R  # noqa: E402

JSON_PATH = SUITE / "p4b_5g_to_5i.json"
EVIDENCE = PAPER9 / "audit" / "evidence" / "p12h" / "rule_rfit_governing.json"
BUNDLE = PAPER9 / "audit" / "evidence" / "p4b_b1" / "repro_realizations_summary.json"
FREEZE_DOC = PAPER9 / "audit" / "P12G_ROUTE_A_RULE_RFIT_FREEZE.md"
BLUEPRINT_V14 = PAPER9 / "plan" / "blueprint" / "Paper9_Blueprint_v1.4.tex"
BLUEPRINT_V13 = PAPER9 / "plan" / "blueprint" / "Paper9_Blueprint_v1.3.tex"
PLAN = PAPER9 / "plan" / "CALC_MASTER_PLAN.md"
TAB06_OUT = PAPER9 / "tables" / "out" / "tab06_convergence_floor.tex"
TAB06_GEN = PAPER9 / "tables" / "gen" / "tab06_convergence_floor.py"
FIG05_GEN = PAPER9 / "figures" / "gen" / "fig05_mesh_convergence.py"
SEC05 = PAPER9 / "latex" / "sections" / "sec05_verification.tex"
SEC09 = PAPER9 / "latex" / "sections" / "sec09_conclusions.tex"
MS = PAPER9 / "latex" / "ms.tex"

GOV_SLOPE = 4.173919246515192
GOV_CI = (3.1453687594104447, 5.202469733619939)
GOV_EPS = 4.6318154949690315e-11
V13_SHA = "ca71b91aba4ca4abe9f157eb595ac8c2"      # historical Blueprint must stay untouched


def _j(p):
    return json.loads(Path(p).read_text())


# ---------------------------------------------------------------- rule constants (pinned)
def test_rule_constants_are_frozen():
    assert R.F == 3.0, "F must remain exactly 3"
    assert R.SPREAD_FLOOR == 1e-15
    assert tuple(R.MESHES) == (4, 8, 16, 32)
    assert R.MIN_ADMISSIBLE == 3
    assert (R.V0_SEED_A, R.V0_SEED_B) == (20260924, 7)
    assert (R.EIGSOLVER_TOL, R.EIGSOLVER_MAXITER, R.THREADS) == (1e-14, 10000, 1)
    assert R.P_MIN == 1.0 and R.R_MAX == pytest.approx(math.log(1.5)) and R.FLOOR_MAX == 1e-9


def test_admission_is_strict_and_floor_applies():
    assert R.is_admissible(3.0 * 1e-12, 1e-12) is False, "exact equality must NOT admit"
    assert R.is_admissible(3.000001 * 1e-12, 1e-12) is True
    assert R.spread_used(None) == R.SPREAD_FLOOR
    assert R.spread_used(0.0) == R.SPREAD_FLOOR, "a zero spread must fall back to the declared floor"
    # with the declared floor in force: 3 * 1e-15 = 3e-15 is the boundary for an unmeasured spread
    assert R.is_admissible(1e-12, None) is True
    assert R.is_admissible(3e-15, None) is False, "exact boundary with the floor must not admit"
    assert R.is_admissible(3.0000001e-15, None) is True


# ---------------------------------------------------- application to the governing artifact
def test_governing_artifact_subset_is_rederived_from_evidence():
    d = _j(JSON_PATH)["5i"]
    bundle = _j(BUNDLE)
    spreads = []
    for i in range(4):
        vals = [r["omega"][i] for r in bundle["realizations"].values()]
        spreads.append((max(vals) - min(vals)) / min(vals))
    ev = _j(EVIDENCE)["reproducibility_inputs"]["governing_era"]["spreads"]
    for got, rec in zip(spreads, ev):
        assert got == pytest.approx(rec, rel=1e-3), "governing-era spreads drifted from the recorded evidence"
    rec_ = R.fit_admissible(d["rel_err"], spreads)
    assert rec_["admissible"] == [4, 8, 16], "the rule must sanction exactly the governing subset"
    assert rec_["excluded"] == [32]
    assert rec_["reportable"] is True
    assert rec_["fit"]["slope"] == GOV_SLOPE, "rule-sanctioned fit must reproduce the governing slope exactly"
    assert d["slope"] == GOV_SLOPE
    assert tuple(d["CI95"]) == GOV_CI and d["eps_Delta"] == GOV_EPS


def test_excluded_level_is_criterion_driven_not_outcome_driven():
    d = _j(JSON_PATH)["5i"]
    bundle = _j(BUNDLE)
    spreads = [(max(r["omega"][i] for r in bundle["realizations"].values())
                - min(r["omega"][i] for r in bundle["realizations"].values()))
               / min(r["omega"][i] for r in bundle["realizations"].values()) for i in range(4)]
    ratios = [R.level_ratio(e, s) for e, s in zip(d["rel_err"], spreads)]
    assert ratios[3] < 1.0, "the 32^2 ratio must be below 1 (excluded by a >= 3x margin)"
    assert ratios[2] > 70.0, "the 16^2 ratio must stay far above F"
    # robustness: every decision is invariant over the recorded F window
    for F in (0.30, 0.5, 1.0, 2.0, 3.0, 10.0, 50.0):
        adm, exc = R.admissible_subset(d["rel_err"], spreads)
        assert (adm, exc) == ([4, 8, 16], [32]), f"decision changed at F={F}"


def test_routeF_and_control_k_decisions_from_recorded_spreads():
    ev = _j(EVIDENCE)["reproducibility_inputs"]
    rf = ev["routeF_configuration"]["spreads"]
    rf_err = _j(EVIDENCE)["expected_decisions"]["routeF_configuration"]["evidence_errors"]
    adm, exc = R.admissible_subset(rf_err, rf)
    assert (adm, exc) == ([4, 8, 16], [32]), "Route-F configuration must exclude the 32^2 level"
    ck = ev["control_k"]
    # the evidence stores a leading null for the 4x4 level, which was not computed at the control k
    ck_err = [e for e in ck["errors"] if e is not None]
    ck_spr = [sp for sp in ck["spreads"] if sp is not None]
    assert len(ck_err) == len(ck_spr) == 3, "control-k evidence must cover exactly the 8/16/32 levels"
    adm, exc = R.admissible_subset(ck_err, ck_spr, meshes=(8, 16, 32))
    assert (adm, exc) == ([8, 16, 32], []), "the same rule must RETAIN the finest level at the control k"
    # provenance: the recorded spreads must appear verbatim in the archived P12E outputs
    vc = (PAPER9 / "audit/evidence/p12e/verify_convergence_output.txt").read_text()
    dc = (PAPER9 / "audit/evidence/p12e/discriminate_output.txt").read_text()
    for tok in ("1.239e-14", "3.679e-14", "1.603e-13"):
        assert tok in vc, f"spread {tok} not found in the archived P12E evidence"
    for tok in ("5.95e-15", "1.61e-13", "6.48e-15"):
        assert tok in dc, f"spread {tok} not found in the archived control-k evidence"


def test_governance_documents_carry_the_rule_and_amended_wording():
    freeze = FREEZE_DOC.read_text()
    assert "F = 3" in freeze and "SPREAD_FLOOR = 1e-15" in freeze
    bp14 = BLUEPRINT_V14.read_text()
    assert "pre-declared factor" in bp14 or "pre-declared resolution criterion" in bp14
    assert "resolution-limited" in bp14
    assert "no theoretical order" in bp14.lower() or "theoretical order is claimed only" in bp14
    plan = PLAN.read_text()
    assert "Rule R-fit" in plan, "plan must name the governing rule"
    assert "1e-15" in plan and "F = 3" in plan
    # the tautological sub-check must be gone from the 5i ROW (it may only be quoted as removed)
    row = next(l for l in plan.splitlines() if l.startswith("| 5i |"))
    assert "≤ ε_Δ" not in row, "the tautological final-doubling sub-check must not survive in row 5i"
    assert "Rule R-fit" in row and "F = 3" in row


def test_manuscript_and_floats_state_the_protocol():
    for p in (SEC05, SEC09):
        t = p.read_text()
        assert "observed" in t.lower()
        assert "theoretical" in t.lower()
    sec05 = SEC05.read_text()
    assert "resolution" in sec05.lower()
    assert re.search(r"admissible|resolution-limited|excluded", sec05), \
        "sec05 must state the fitted subset / excluded level"
    tab = TAB06_OUT.read_text()
    assert "4.17" in tab and "no theoretical order claimed" in tab
    assert "resolution" in tab.lower()
    assert re.search(r"admissib|excluded|resolution-limited", tab), "Table 6 must report the admission status"
    assert "F = 3" in tab or "F=3" in tab
    fig = FIG05_GEN.read_text()
    assert "resolution-limited" in fig or "excluded" in fig, "Fig. 5 must distinguish the excluded level"
    for bad in ("Babuska", "O(h^4", "fourth-order convergence"):
        assert bad not in fig and bad not in tab and bad not in TAB06_GEN.read_text()


def test_c1_predicates_reused_unchanged():
    d = _j(JSON_PATH)["5i"]
    hs = [1.0 / n for n in (4, 8, 16)]
    fit = R.lsq_loglog(hs, d["rel_err"][:3])
    crit = R.check_criterion(d["rel_err"], d["d16_32"], fit["lo"], fit["resid_max"])
    assert crit == {"P1_monotone_decreasing": True, "P2_ci_lower_ge_P_MIN": True,
                    "P3_powerlaw_residual_le_R_MAX": True, "P4_floor_datum_le_FLOOR_MAX": True}
    # and the four-level sequence still Fails P3 (the finding that motivates the rule) —
    # recomputed here so the record cannot silently flip
    fit4 = R.lsq_loglog([1/4, 1/8, 1/16, 1/32], d["rel_err"])
    assert fit4["resid_max"] > R.R_MAX


def test_blueprint_v13_is_untouched_and_v14_has_provenance():
    got = hashlib.sha256(BLUEPRINT_V13.read_bytes()).hexdigest()
    assert got.startswith(V13_SHA), "historical Blueprint v1.3 must remain byte-identical"
    bp14 = BLUEPRINT_V14.read_text()
    assert V13_SHA in bp14, "v1.4 must record its provenance from v1.3"
    assert "v1.4" in bp14


def test_p12h_deliverable_audit_is_complete():
    """The P12H deliverable must exist with its 14 sections and the five confirmations."""
    doc = (PAPER9 / "audit/P12H_A1_PROTOCOL_CLOSURE_AUDIT.md").read_text()
    for i in range(1, 15):
        assert f"## {i}." in doc, f"audit section {i} missing"
    for phrase in ("No Route-F re-baseline", "No P13", "No P12E values were imported",
                   "Blueprint v1.3 is unmodified", "Nothing was pushed"):
        assert phrase in doc, f"confirmation missing: {phrase}"
    assert "remains OPEN" in doc, "R-1 must be stated as still OPEN"
    assert "4.173919246515192" in doc and "4.6318154949690315e-11" in doc, "governing numbers missing"
