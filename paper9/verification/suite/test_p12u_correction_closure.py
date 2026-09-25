#!/usr/bin/env python3
"""P12U — correction-closure guards for the P12T findings F1–F3.

These tests pin the exact factual statements that P12T found defective, so the same inconsistencies
cannot silently return. They do not re-open any scientific conclusion: the B1/B2/B3 routes, the
gates and every numerical field are asserted unchanged.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
P9 = REPO / "paper9"

RECORD = P9 / "audit" / "benchmark_validation_record.json"
AUDIT_MD = P9 / "audit" / "P12S_GRAPHICAL_VALIDATION_AUDIT.md"
CHECKPOINT = P9 / "audit" / "RECOVERY_CHECKPOINT_P12S.md"
IMPACT = P9 / "audit" / "P12S_MANUSCRIPT_IMPACT.md"
RUN_PY = P9 / "validation" / "p12s_run.py"
RAW = P9 / "audit" / "evidence" / "p12s" / "p12s_validation_record.json"

# ---- P12T-verified values (the only admissible sources for these statements) ----
F1_VERTICES_K0 = "0.0000 / 0.9795 / 1.0210 / 1.9809"
F1_VERTICES_K1 = "0.4799 / 0.5196 / 1.4998 / 1.9809"
F1_DEFECTIVE = ("1.4799", "0.5099")
F2_PRESENT_CURVE = "0.436"          # source's own gradient ("Present") curve at k_bar = 1
F2_CLASSICAL_LIMIT = ("0.500", "0.5")  # exact classical limit (k_bar/2)
F2_DEFECTIVE = (
    "source's own figure and the exact classical-limit value require 0.50",
    "source's own figure and the exact classical limit require 0.50",
    "require 0.50",
)


def _text(p: Path) -> str:
    return p.read_text()


def _flat(p: Path) -> str:
    """Whitespace-normalised text: prose may wrap, the recorded values may not change."""
    return " ".join(p.read_text().split())


# =============================================================== F1
def test_f1_record_carries_the_p12t_verified_vertices():
    st = " ".join(json.loads(RECORD.read_text())["benchmarks"]["B1"]["reproduction_status"].split())
    assert F1_VERTICES_K0 in st, st
    assert F1_VERTICES_K1 in st, st
    assert not any(d in st for d in F1_DEFECTIVE), st


def test_f1_audit_file_carries_the_p12t_verified_vertices():
    t = _flat(AUDIT_MD)
    assert F1_VERTICES_K0 in t
    assert F1_VERTICES_K1 in t
    assert not any(d in t for d in F1_DEFECTIVE), "defective B1 vertex strings still present"


def test_f1_no_defective_vertex_string_in_the_corrected_corpus():
    for p in (RECORD, AUDIT_MD, CHECKPOINT, IMPACT, RUN_PY, RAW):
        t = _text(p)
        assert not any(d in t for d in F1_DEFECTIVE), f"{p.name} still contains a defective vertex string"


# =============================================================== F2
@pytest.mark.parametrize("path", [RECORD, AUDIT_MD, CHECKPOINT, IMPACT, RUN_PY, RAW],
                         ids=lambda p: p.name if isinstance(p, Path) else str(p))
def test_f2_each_corrected_location_distinguishes_present_curve_from_classical_limit(path):
    t = _text(path)
    assert F2_PRESENT_CURVE in t, f"{path.name}: the source's own gradient-curve value 0.436 is missing"
    assert any(v in t for v in F2_CLASSICAL_LIMIT), f"{path.name}: the classical limit is not stated"
    assert "gradient" in t, f"{path.name}: the 'Present' gradient curve is not named"


def test_f2_no_location_attributes_the_classical_limit_to_the_source_curve():
    for p in (RECORD, AUDIT_MD, CHECKPOINT, IMPACT, RUN_PY, RAW):
        t = _text(p)
        for d in F2_DEFECTIVE:
            assert d not in t, f"{p.name}: defective F2 wording still present -> {d!r}"


def test_f2_literature_curve_is_labelled_as_the_separate_dashed_curve():
    # wherever the ~0.50 literature value is attributed, the dashed ('Li and Wei [34]') curve must be
    # named as such and must not be conflated with the source's own gradient curve
    for p in (RECORD, AUDIT_MD, CHECKPOINT, IMPACT, RUN_PY, RAW):
        t = _text(p)
        assert "dashed" in t, f"{p.name}: the literature [34] curve is not identified as the dashed curve"


# =============================================================== F3
def test_f3_run_script_readings_are_mutually_consistent():
    t = _text(RUN_PY)
    assert "(1,~0.45)" in t, "the accepted digitised reading (line 178) was altered"
    assert "0.436" in t and "0.500" in t, "the corrected reason must carry the P12T values"
    # the same file must not attribute the classical-limit value to the published figure
    assert "the source's own figure and the exact" not in t
    # numeric consistency of the two B3 readings: the digitised reading and the P12T measurement agree
    assert abs(0.45 - 0.436) <= 0.02


def test_f3_no_contradictory_baseline_remains():
    for p in (RUN_PY, RECORD, RAW):
        assert "require 0.50" not in _text(p), f"{p.name}: contradictory baseline remains"


# =============================================================== closure invariants
def test_corrections_changed_no_route_gate_or_numeric_field():
    rec = json.loads(RECORD.read_text())
    b = rec["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B2"]["graphical_validation"] == "NOT_APPLICABLE"
    assert b["B3"]["route"] == "NOT_VALIDATED" and b["B3"]["graphical_validation"] == "NOT_APPLICABLE"
    for k in ("B1", "B2", "B3"):
        assert b[k]["quantitative_error"] is None
    assert rec["gate_state"]["PCR1"] == "PASS"
    assert rec["gate_state"]["G3"] == "MET" and rec["gate_state"]["G4"] == "NOT MET"
    # The P12U corrections changed no gate; the two values below follow the later PI authorisation
    # of 2026-09-24 (PI_DECISION_P5_GATE_ADOPTION.md / PI_DECISION_R1_MEASURED_ADJUDICATION.md).
    assert rec["gate_state"]["P5"] == "PASS" and rec["gate_state"]["R-1"] == "CLOSED"
    assert rec["gate_state"]["PCR5"] == "PASS" and rec["gate_state"]["P13"] == "BLOCKED"
    # numeric content untouched by the correction (P12T-verified values)
    raw = json.loads(RAW.read_text())["benchmarks"]
    assert raw["B1"]["reproduced_gaps"][0] == pytest.approx([0.4801, 0.5199], abs=1e-9)
    assert raw["B2"]["barred_required_dps"] == pytest.approx(52131.0)
    assert raw["B3"]["reproduced_gaps"][0] == pytest.approx([0.3391, 1.0213], abs=1e-9)
    assert raw["B3"]["omega0_reproduced"] == pytest.approx(411423336.09829, rel=1e-12)


def test_overlays_unchanged_by_the_correction():
    man = json.loads(RECORD.read_text())["benchmarks"]
    assert man["B1"]["overlay_sha256"].startswith("e602e57c")
    assert man["B2"]["overlay_sha256"].startswith("8e350a4e")
    assert man["B3"]["overlay_sha256"].startswith("0145def2")


def test_record_evidence_hash_matches_the_actual_raw_record():
    """The machine record's evidence hash must track the raw record it points at."""
    rec = json.loads(RECORD.read_text())
    actual = hashlib.sha256(RAW.read_bytes()).hexdigest()
    for k in ("B1", "B2", "B3"):
        assert rec["benchmarks"][k]["evidence_path_sha256"] == actual, f"{k}: stale evidence hash"


def test_record_b3_reason_matches_the_corrected_script_output():
    """The machine record's B3 reason must equal the corrected script's own output string."""
    rec = json.loads(RECORD.read_text())
    raw = json.loads(RAW.read_text())
    assert rec["benchmarks"]["B3"]["reason"] == raw["benchmarks"]["B3"]["reason"]
    assert "0.436" in rec["benchmarks"]["B3"]["reason"] and "0.500" in rec["benchmarks"]["B3"]["reason"]
