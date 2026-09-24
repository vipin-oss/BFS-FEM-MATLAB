"""P12R governance guards — Blueprint v1.5 amendment A2 (external-validation evidence routes).

Synthetic classification tests plus governance guards.  Nothing here uses the actual
B1/B2/B3 benchmark outcomes; the synthetic cases are constructed facts, and no test may be
satisfied by loosening the classifier.  Run no solver; change no scientific value.

Guards:
  * the six required synthetic cases (quantitative / graphical / ambiguous / insufficient /
    similar-looking-but-different-parameters / graphical-never-quantitative);
  * no fabricated precision;
  * thresholds unchanged (2 % / 0.5 %) in the code AND in Blueprint v1.5;
  * v1.4 byte-identical, v1.5 = v1.4 + exactly the declared A2 blocks;
  * v1.5 declares non-promotion of PCR1/G3;
  * benchmark evidence and the prepared author-request drafts unchanged.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import sys
from pathlib import Path

import pytest

SUITE = Path(__file__).resolve().parent
PAPER9 = SUITE.parents[1]
REPO = SUITE.parents[2]

sys.path.insert(0, str(SUITE))
import benchmark_validation_route as BVR  # noqa: E402

BP_DIR = PAPER9 / "plan" / "blueprint"
V13 = BP_DIR / "Paper9_Blueprint_v1.3.tex"
V14 = BP_DIR / "Paper9_Blueprint_v1.4.tex"
V15 = BP_DIR / "Paper9_Blueprint_v1.5.tex"
AMENDMENT = PAPER9 / "audit" / "BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md"
EVIDENCE = PAPER9 / "audit" / "benchmark_evidence.json"
DRAFTS = PAPER9 / "audit" / "P12M_AUTHOR_REQUEST_DRAFTS.md"

V13_SHA = "ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f"
V14_SHA = "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638"
EVIDENCE_SHA = "e9191506ca0fb07a"          # prefix, as recorded in the P12-era anchors
DRAFTS_SHA = "2f68e66fa82dbf8b18420d9da33c34cb726d47433c7ce1875c5a19c8267cec61"   # P12M drafts, pinned at the A2 amendment


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ----------------------------------------------------------------- synthetic cases

def test_case1_numerical_data_routes_quantitative():
    r = BVR.classify("synthetic-num", source_numerical_data=True, parameters_sufficient=True,
                     graphical_reproduction_performed=True, reported_error_pct=1.2)
    assert r["route"] == BVR.ROUTE_QUANTITATIVE
    assert r["verdict"] == "PASS" and r["quantitative_error"] == 1.2
    assert r["threshold_pct"] == BVR.THRESHOLD_GENERAL_PCT
    # classical-limit benchmark uses the existing 0.5 % target, not a new threshold
    rc = BVR.classify("synthetic-num-classical", source_numerical_data=True,
                      parameters_sufficient=True, graphical_reproduction_performed=True,
                      reported_error_pct=0.4, classical_limit=True)
    assert rc["threshold_pct"] == BVR.THRESHOLD_CLASSICAL_PCT and rc["verdict"] == "PASS"
    rf = BVR.classify("synthetic-num-classical-fail", source_numerical_data=True,
                      parameters_sufficient=True, graphical_reproduction_performed=True,
                      reported_error_pct=0.6, classical_limit=True)
    assert rf["verdict"] == "FAIL"


def test_case2_graph_only_sufficient_parameters_routes_graphical():
    r = BVR.classify("synthetic-graph", source_numerical_data=False, parameters_sufficient=True,
                     graphical_reproduction_performed=True, overlay_available=True)
    assert r["route"] == BVR.ROUTE_GRAPHICAL
    assert r["verdict"] == "GRAPHICAL VALIDATION"
    assert r["quantitative_error"] is None and r["threshold_pct"] is None
    assert r["requires_label"] is True and r["overlay_available"] is True


def test_case3_graph_only_ambiguous_parameter_not_validated():
    r = BVR.classify("synthetic-ambiguous", source_numerical_data=False,
                     parameters_sufficient=True, graphical_reproduction_performed=True,
                     ambiguity_unresolved=True)
    assert r["route"] == BVR.ROUTE_NOT_VALIDATED and r["verdict"] == "NOT VALIDATED"
    assert r["quantitative_error"] is None
    assert "ambiguity" in r["reason"]


def test_case4_insufficient_source_not_validated():
    r = BVR.classify("synthetic-insufficient", source_numerical_data=False,
                     parameters_sufficient=False, graphical_reproduction_performed=False)
    assert r["route"] == BVR.ROUTE_NOT_VALIDATED
    # and a reconstruction that was never performed is also not validated
    r2 = BVR.classify("synthetic-not-reproduced", source_numerical_data=False,
                      parameters_sufficient=True, graphical_reproduction_performed=False)
    assert r2["route"] == BVR.ROUTE_NOT_VALIDATED and r2["verdict"] == "NOT VALIDATED"


def test_case5_similar_graph_but_different_parameters_must_not_pass():
    """A visually similar curve with an insufficient/different parameter set is not evidence."""
    r = BVR.classify("synthetic-lookalike", source_numerical_data=False,
                     parameters_sufficient=False, graphical_reproduction_performed=True,
                     overlay_available=True)
    assert r["route"] == BVR.ROUTE_NOT_VALIDATED
    assert r["verdict"] != "PASS"
    assert r["quantitative_error"] is None


def test_case6_graphical_agreement_stays_graphical_never_quantitative():
    r = BVR.classify("synthetic-graphical-only", source_numerical_data=False,
                     parameters_sufficient=True, graphical_reproduction_performed=True)
    assert r["route"] == BVR.ROUTE_GRAPHICAL
    assert r["route"] != BVR.ROUTE_QUANTITATIVE
    assert BVR.hierarchy_rank(r["route"]) < BVR.hierarchy_rank(BVR.ROUTE_QUANTITATIVE)
    assert r["quantitative_error"] is None and r["threshold_pct"] is None


def test_no_fabricated_precision_without_source_numerics():
    with pytest.raises(BVR.FabricatedPrecisionError):
        BVR.classify("synthetic-forged", source_numerical_data=False, parameters_sufficient=True,
                     graphical_reproduction_performed=True, reported_error_pct=1.9)
    with pytest.raises(BVR.FabricatedPrecisionError):
        BVR.classify("synthetic-forged-2", source_numerical_data=False, parameters_sufficient=False,
                     graphical_reproduction_performed=True, reported_error_pct=0.4)


def test_routes_are_exhaustive_and_exclusive():
    seen = set()
    for kw in (dict(source_numerical_data=True, parameters_sufficient=True,
                    graphical_reproduction_performed=True, reported_error_pct=0.1),
               dict(source_numerical_data=False, parameters_sufficient=True,
                    graphical_reproduction_performed=True),
               dict(source_numerical_data=False, parameters_sufficient=False,
                    graphical_reproduction_performed=False)):
        seen.add(BVR.classify("s", **kw)["route"])
    assert seen == set(BVR.ALL_ROUTES)


def test_hierarchy_never_inverts():
    assert (BVR.hierarchy_rank(BVR.ROUTE_QUANTITATIVE)
            > BVR.hierarchy_rank(BVR.ROUTE_GRAPHICAL)
            > BVR.hierarchy_rank(BVR.ROUTE_NOT_VALIDATED))
    # source numerics available => the graphical route may not be returned instead
    r = BVR.classify("s", source_numerical_data=True, parameters_sufficient=True,
                     graphical_reproduction_performed=True)
    assert r["route"] == BVR.ROUTE_NOT_VALIDATED      # pending comparison, not "graphical"
    r2 = BVR.classify("s", source_numerical_data=True, parameters_sufficient=True,
                      graphical_reproduction_performed=True, reported_error_pct=5.0)
    assert r2["route"] == BVR.ROUTE_QUANTITATIVE and r2["verdict"] == "FAIL"


# ----------------------------------------------------------------- governance guards

def test_thresholds_unchanged_in_code():
    assert BVR.THRESHOLD_GENERAL_PCT == 2.0
    assert BVR.THRESHOLD_CLASSICAL_PCT == 0.5


def test_blueprint_v13_and_v14_byte_identical():
    assert sha(V13) == V13_SHA, "historical Blueprint v1.3 must remain byte-identical"
    assert sha(V14) == V14_SHA, "Blueprint v1.4 must remain byte-identical (A2 adds v1.5)"


def test_v15_is_v14_plus_exactly_the_declared_blocks():
    a = V14.read_text().splitlines(keepends=True)
    b = V15.read_text().splitlines(keepends=True)
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
           if o[0] != "equal"]
    assert len(ops) == 8, f"expected the 8 declared A2 blocks, found {len(ops)}"
    kinds = [(tag, i1 + 1, i2) for tag, i1, i2, _, _ in ops]
    assert [k[0] for k in kinds].count("replace") == 6
    assert [k[0] for k in kinds].count("insert") == 2
    assert [k[1] for k in kinds][:6] == [95, 457, 471, 803, 886, 1046], kinds
    t = V15.read_text()
    assert t.count("{") == t.count("}"), "v1.5 brace balance must hold"
    assert V14_SHA in t and V13_SHA in t, "v1.5 must record its v1.4/v1.3 provenance"


def test_v15_defines_the_three_states_and_the_guards():
    t = V15.read_text()
    for token in (BVR.ROUTE_QUANTITATIVE, BVR.ROUTE_GRAPHICAL, BVR.ROUTE_NOT_VALIDATED):
        # identifiers are printed in LaTeX \texttt{} with escaped underscores
        assert token.replace("_", r"\_") in t, f"v1.5 must name the classification token {token}"
    assert "AMENDMENT A2" in t
    for phrase in ("Numerical source values $>$ published graphical source with sufficient parameters",
                   "No interpretation", "must never be converted into a numerical error",
                   "before B2 can be accepted"):
        assert phrase in t, f"v1.5 A2 must state: {phrase}"


def test_v15_declares_non_promotion_and_thresholds_unchanged():
    t = V15.read_text()
    assert "No automatic promotion" in t
    assert r"PCR1 remains" in t and "G3 remains" in t and "NOT MET" in t
    assert r"$\le 2\%$" in t and r"$\le 0.5\%$" in t, "existing thresholds must be restated unchanged"
    # the amendment must not claim a percentage for graphical evidence
    assert "no numerical percentage asserted" in t


def test_amendment_record_references_and_tests_exist():
    assert AMENDMENT.exists(), "the A2 amendment record must exist"
    t = AMENDMENT.read_text()
    for phrase in ("Decision table", "Delta v1.4", "A2.4", "no fabricated precision", "no gate moves"):
        assert phrase in t, f"amendment record must contain: {phrase}"
    assert "benchmark_validation_route.py" in t and "test_p12r_graphical_validation_route.py" in t


def test_benchmark_evidence_unchanged_and_still_null():
    assert sha(EVIDENCE).startswith(EVIDENCE_SHA), "benchmark evidence must be unchanged"
    d = json.loads(EVIDENCE.read_text())
    b = d.get("benchmarks", d)
    for k in ("B1", "B2", "B3"):
        assert b[k]["quantitative_error"] is None, f"{k} quantitative_error must remain NULL"


def test_author_request_package_not_deleted_or_modified():
    assert DRAFTS.exists(), "the prepared author-data request package must not be deleted"
    assert sha(DRAFTS) == DRAFTS_SHA, "the prepared author-data request drafts must be unchanged"
    t = DRAFTS.read_text()
    assert "NOT SENT" in t and "No message has been sent" in t
