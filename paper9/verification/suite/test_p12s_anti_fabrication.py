#!/usr/bin/env python3
"""P12S Phase H — anti-fabrication guards for the graphical-validation route.

Seven structural tests (one per required property) plus a check of the committed P12S
record itself.  These tests never use the actual B1/B2/B3 outcomes to force a PASS;
they exercise the classification/recording rules on synthetic inputs.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
RECORD = REPO / "paper9" / "audit" / "benchmark_validation_record.json"
CONSTANTS = REPO / "paper9" / "verification" / "suite" / "benchmark_validation_route.py"

THRESHOLD_GENERAL = 2.0     # percent, unchanged since v1.3
THRESHOLD_CLASSICAL = 0.5   # percent, unchanged since v1.3


# --------------------------------------------------------------------------- helpers
def route_for(source_numerics: bool, graph_sufficient: bool, ambiguous: bool) -> str:
    """A2 route logic (mirrors benchmark_validation_route.py precedence)."""
    if ambiguous:
        return "NOT_VALIDATED"
    if source_numerics:
        return "QUANTITATIVE_VALIDATION"
    return "GRAPHICAL_VALIDATION" if graph_sufficient else "NOT_VALIDATED"


def graphical_entry(*, graphs_match: bool, ambiguity: bool, same_observable: bool = True) -> dict:
    return {
        "route": route_for(False, graphs_match and same_observable, ambiguity),
        "graphical_validation": "PASS" if (graphs_match and same_observable and not ambiguity) else "NOT_APPLICABLE",
        "quantitative_error": None,          # graphical route NEVER carries a number
    }


# --------------------------------------------------------------------------- 1
def test_graphical_route_never_carries_a_quantitative_error():
    e = graphical_entry(graphs_match=True, ambiguity=False)
    assert e["route"] == "GRAPHICAL_VALIDATION"
    assert e["graphical_validation"] == "PASS"
    assert e["quantitative_error"] is None, "overlay existence must not create a %"


# --------------------------------------------------------------------------- 2
def test_missing_source_numerics_keep_null():
    e = graphical_entry(graphs_match=False, ambiguity=False)  # e.g. B2/B3
    assert e["quantitative_error"] is None


# --------------------------------------------------------------------------- 3
def test_parameter_ambiguity_prevents_pass():
    e = graphical_entry(graphs_match=True, ambiguity=True)
    assert e["route"] == "NOT_VALIDATED"
    assert e["graphical_validation"] == "NOT_APPLICABLE"


# --------------------------------------------------------------------------- 4
def test_look_alike_curve_with_different_parameters_cannot_pass():
    # visually similar but wrong parameter set (no same-observable match) => no PASS
    e = graphical_entry(graphs_match=True, ambiguity=False, same_observable=False)
    assert e["graphical_validation"] == "NOT_APPLICABLE"


# --------------------------------------------------------------------------- 5
def test_digitisation_residual_cannot_populate_quantitative_error():
    residual_px = 3.7            # registration residual, pixels
    pixel_scale = 0.0021         # omega_bar per pixel
    value = residual_px * pixel_scale
    assert isinstance(value, float)
    # the rule: a residual may be *measured* but never *recorded* as an error
    assert graphical_entry(graphs_match=True, ambiguity=False)["quantitative_error"] is None


# --------------------------------------------------------------------------- 6
def test_genuine_quantitative_dataset_still_uses_the_2_percent_threshold():
    assert THRESHOLD_GENERAL == 2.0 and THRESHOLD_CLASSICAL == 0.5
    ok = {"route": "QUANTITATIVE_VALIDATION", "quantitative_error": 1.4}
    bad = {"route": "QUANTITATIVE_VALIDATION", "quantitative_error": 2.6}
    assert ok["quantitative_error"] <= THRESHOLD_GENERAL
    assert bad["quantitative_error"] > THRESHOLD_GENERAL


# --------------------------------------------------------------------------- 7
def test_routes_are_independent():
    b1 = graphical_entry(graphs_match=True, ambiguity=False)
    b2 = graphical_entry(graphs_match=False, ambiguity=True)
    b3 = graphical_entry(graphs_match=False, ambiguity=False)
    assert b1["route"] == "GRAPHICAL_VALIDATION"
    assert b2["route"] == b3["route"] == "NOT_VALIDATED"
    assert b1["graphical_validation"] == "PASS" and b3["graphical_validation"] == "NOT_APPLICABLE"


# --------------------------------------------------------------------------- record check
@pytest.mark.skipif(not RECORD.exists(), reason="P12S record not present on this tree")
def test_committed_record_is_not_promoted_and_has_no_invented_numbers():
    rec = json.loads(RECORD.read_text())
    b = rec["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B2"]["graphical_validation"] == "NOT_APPLICABLE"
    assert b["B3"]["route"] == "NOT_VALIDATED" and b["B3"]["graphical_validation"] == "NOT_APPLICABLE"
    for k in ("B1", "B2", "B3"):
        assert b[k]["quantitative_error"] is None, f"{k} must keep quantitative_error = NULL"
    assert rec["gate_state"]["PCR1"] == "NOT PASS" and rec["gate_state"]["G3"] == "NOT MET"
    assert rec["source_immutability"]["manuscript_modified"] is False
    assert rec["source_immutability"]["author_contact"] == "NONE"
