#!/usr/bin/env python3
"""P12W — correction-closure guards for the two residual P12V text findings.

P12V reported two *text-level* defects in the active machine record and deliberately did not fix
them (the phase was audit-only). P12W closes exactly those two:

* **P12V-F1** — `benchmarks.B3.reproduction_status` conflated the classical/literature level with
  the source's own published "Present" gradient curve ("source's own 0.50").
* **P12V-F2** — `benchmarks.B3.ambiguity_status` still attributed the residual to an untraced
  dipolar-gradient formulation/coefficient convention, which P12V superseded by establishing the
  repository matrix as the source's own Appendix 3 formulation.

The same superseded claim also survived in `gate_state.blocker` ("unverifiable formulation"), a
third text span inside the same active record; Part C of the P12W mandate (internal-contradiction
rule) closes it with the two fields above. No gate, route or number moved.

These guards pin the corrected wording and, just as importantly, pin that the correction changed
nothing else: no route, gate, number, hash, provenance or frozen P12S-era reason string moved, and
B1/B2/B3 keep their scientific statuses.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RECORD = REPO / "paper9" / "audit" / "benchmark_validation_record.json"
RAW = REPO / "paper9" / "audit" / "evidence" / "p12s" / "p12s_validation_record.json"

# Corrected content hash of the active record (P12U content `cdbfe6c2…` + the three P12W text-span
# corrections). The only edit P12W makes to this file.
RECORD_SHA256_P12W = "9ea0d4c8039b42c2644db3c679e3ff4b42b2a8a72b3977f6e54c1d301b718b51"
# Frozen P12S/P12U raw run record — P12W must leave it byte-identical.
RAW_SHA256 = "cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21"

# The three quantities that must never be re-conflated.
REPRODUCED_GRADIENT = "0.3391"          # repository / source-formulation reproduction at k_bar = 1
PUBLISHED_PRESENT = ("0.433", "0.436")  # published solid "Present" gradient curve of Fig. 4(c)
CLASSICAL_LEVEL = ("0.500", "~0.50")    # exact classical limit; dashed literature [34] curve

# Obsolete forms that must not survive in the *active* record (historical audit files may quote
# them as findings — that is faithful history and is checked separately).
OBSOLETE_F1 = (
    "source's own 0.50",
    "source's own 0.5)",
    "vs source's own 0.50",
)
OBSOLETE_F2 = (
    "SOURCE_UNAVAILABLE",
    "not pinned down",
    "unverifiable formulation",
)


def _record() -> dict:
    return json.loads(RECORD.read_text())


def _flat(s: str) -> str:
    return " ".join(s.split())


# --------------------------------------------------------------- 1. F1 wording
def test_f1_reproduction_status_distinguishes_the_three_quantities():
    st = _flat(_record()["benchmarks"]["B3"]["reproduction_status"])
    assert REPRODUCED_GRADIENT in st, "the reproduced (source-formulation) value ~0.3391 is missing"
    assert all(v in st for v in PUBLISHED_PRESENT), "the published solid 'Present' curve is missing"
    assert "0.433-0.436" in st, "the published 'Present' band must be stated as a band"
    assert all(v in st for v in CLASSICAL_LEVEL), "the classical/dashed level is missing"
    assert "classical" in st.lower() and "dashed" in st.lower()
    assert "Present" in st and "gradient" in st
    # the reproduced value must not be attributed to the source curve, and vice versa
    assert "NOT the source's Present gradient value" in st or "are NOT the source" in st
    assert "tuned" in st or "no parameter" in st


def test_f1_no_obsolete_conflation_remains_in_the_active_record():
    t = RECORD.read_text()
    for bad in OBSOLETE_F1:
        assert bad not in t, f"obsolete F1 phrase still in the active record: {bad!r}"


def test_f1_historical_finding_is_still_recorded_in_the_p12v_audit():
    """The P12V audit must keep quoting the defect it found (history is not rewritten)."""
    t = _flat((REPO / "paper9" / "audit" / "P12V_B2_B3_SOURCE_AUDIT.md").read_text())
    assert "P12V-F1" in t and "source's own 0.50" in t
    assert "P12V-F2" in t


# --------------------------------------------------------------- 2. F2 wording
def test_f2_ambiguity_status_keeps_the_formulation_and_the_residual_apart():
    st = _flat(_record()["benchmarks"]["B3"]["ambiguity_status"])
    # (a) the formulation is established as the source's own
    assert "formulation is established as the source's own" in st
    assert "Appendix 3" in st and "1e-16" in st and "60 digits" in st
    assert "recorded bands are reproduced" in st
    # (b) the residual is the unstated Fig. 4(c) configuration / curve data
    assert "parameter set/normalisation" in st and "curve data" in st
    assert "Fig. 4(c)" in st
    # (c) no unsupported inheritance from Fig. 3(b)
    assert "no inheritance of the Fig. 3(b) values assumed" in st
    # (d) still not validated
    assert "NOT_VALIDATED" in st
    # and it must not imply the formulation itself is ambiguous
    for bad in OBSOLETE_F2:
        assert bad not in st, f"obsolete F2 phrase still in ambiguity_status: {bad!r}"
    assert "NOT the formulation" in st


def test_c_blocker_clause_no_longer_calls_the_formulation_unverifiable():
    """Part C: the same superseded claim inside `gate_state.blocker` is closed too."""
    g = _record()["gate_state"]
    assert "unverifiable formulation" not in g["blocker"]
    assert "remain NOT_VALIDATED" in g["blocker"]
    assert "formulation itself is verified as the source's own Appendix 3" in g["blocker"]
    assert "gate definitions unchanged" in g["blocker"]


def test_f2_superseded_reason_clause_is_flagged_as_historical_not_operative():
    """The frozen P12S-era `reason` string keeps its old clause (byte-identical record), so the
    status field must say that this clause is historical text and not the operative status."""
    st = _flat(_record()["benchmarks"]["B3"]["ambiguity_status"])
    assert "historical text, not the operative status" in st


# --------------------------------------------------------------- 3. statuses
def test_b3_status_unchanged_by_the_correction():
    b3 = _record()["benchmarks"]["B3"]
    assert b3["route"] == "NOT_VALIDATED"
    assert b3["quantitative_error"] is None
    assert b3["graphical_validation"] == "NOT_APPLICABLE"


def test_b1_status_unchanged_by_the_correction():
    b1 = _record()["benchmarks"]["B1"]
    assert b1["route"] == "GRAPHICAL_VALIDATION"
    assert b1["graphical_validation"] == "PASS"
    assert b1["quantitative_error"] is None


def test_b2_status_unchanged_by_the_correction():
    b2 = _record()["benchmarks"]["B2"]
    assert b2["route"] == "NOT_VALIDATED"
    assert b2["quantitative_error"] is None
    assert "UNRESOLVED" in b2["ambiguity_status"]


# --------------------------------------------------------------- 4. nothing else moved
def test_only_the_corrected_text_spans_differ_from_the_pre_correction_record_contract():
    rec = _record()
    b = rec["benchmarks"]
    # routes / gates / numbers / hashes / provenance / frozen reason strings
    assert (b["B1"]["overlay_sha256"], b["B2"]["overlay_sha256"], b["B3"]["overlay_sha256"]) == (
        "e602e57c24dd37859eb2db1bb8e5a83701745e2412db700888d4ce0d4227f75b",
        "8e350a4ee69631e4627439502cf53facb2febe1c96920a794a83abb8a2e7760a",
        "0145def25fe8fd24a89516b84f8cea3f27a4425080d309a7bbdee7103efed49d",
    )
    for k in ("B1", "B2", "B3"):
        assert b[k]["evidence_path_sha256"] == RAW_SHA256
    assert b["B1"]["reproduction_status"].startswith("REPRODUCED (branch vertices")
    assert b["B2"]["reproduction_status"] == "NOT REPRODUCED under any admissible interpretation"
    assert b["B2"]["parameter_completeness"].startswith("INCOMPLETE")
    assert b["B3"]["parameter_completeness"] == "COMPLETE for the classical data; gradient conversion not verifiable"
    assert b["B3"]["omega0_reproduced_vs_stated_Hz"] == [411423336.09829, 410000000.0]
    assert b["B1"]["quantitative_error_reason"] == "no machine-readable numerical values published (data on request only)"
    assert b["B2"]["quantitative_error_reason"] == "no machine-readable numerical values published"
    assert b["B3"]["quantitative_error_reason"] == "no machine-readable numerical values published"
    # the frozen P12S-era reason strings still carry the P12U-corrected attribution
    for k in ("B1", "B2", "B3"):
        assert "0.436" in b[k]["reason"] or k != "B3"
    assert "0.436" in b["B3"]["reason"] and "0.500" in b["B3"]["reason"]
    # gates untouched
    g = rec["gate_state"]
    assert (g["PCR1"], g["G3"], g["G4"], g["P5"], g["R-1"], g["PCR5"], g["P13"]) == (
        "NOT PASS", "NOT MET", "NOT MET", "NOT PASS/OPEN", "OPEN", "PASS", "BLOCKED")
    assert rec["source_immutability"]["manuscript_modified"] is False
    assert rec["source_immutability"]["author_contact"] == "NONE"


def test_active_record_hash_pin_and_frozen_raw_record():
    assert hashlib.sha256(RECORD.read_bytes()).hexdigest() == RECORD_SHA256_P12W
    assert hashlib.sha256(RAW.read_bytes()).hexdigest() == RAW_SHA256, "P12S/P12U raw record was altered"


def test_p12u_reason_equality_guard_surface_is_intact():
    """P12U pins record.reason == raw.reason; that link must survive the P12W correction, which is
    precisely why the frozen reason clause is flagged instead of rewritten."""
    rec = _record()["benchmarks"]["B3"]["reason"]
    raw = json.loads(RAW.read_text())["benchmarks"]["B3"]["reason"]
    assert rec == raw
    # the obsolete *status* wording lived in ambiguity_status / gate_state, not in the frozen reason
    assert "not pinned down" not in rec
    assert "unverifiable formulation" not in rec
