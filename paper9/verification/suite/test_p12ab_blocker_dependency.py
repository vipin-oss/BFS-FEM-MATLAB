#!/usr/bin/env python3
"""P12AB guard suite — remaining-blocker dependency audit and P13 entry decision.

Ten guards, one per clause of the P12AB mandate (Part K):

 1. B2 dependency classification
 2. B3 dependency classification
 3. PCR1 dependency chain
 4. G3/G4 dependency chain
 5. P5 status
 6. R-1 status
 7. P13 prerequisite matrix
 8. no gate-lowering route
 9. author-request status
10. current Blueprint v1.5 governing specification

The guards are audit pins: they assert that the *reported* dependency structure and statuses stay in
agreement with the governing text and the active machine record. They promote nothing.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit"
RECORD = AUDIT / "benchmark_validation_record.json"
MATRIX_JSON = AUDIT / "P12AB_REMAINING_BLOCKER_MATRIX.json"
MATRIX_MD = AUDIT / "P12AB_REMAINING_BLOCKER_MATRIX.md"
AUDIT_DOC = AUDIT / "P12AB_REMAINING_BLOCKER_FORENSIC_AUDIT.md"
P12AA_MATRIX = AUDIT / "P12AA_PRE_P13_BLOCKER_MATRIX.json"
P5_STATUS = AUDIT / "P5_STATUS.md"
P5_HIGHLIGHTS = REPO / "paper9" / "results" / "processed" / "p5_production_highlights.json"
P5_RAW = REPO / "paper9" / "results" / "raw" / "p5_production_raw.json"
P12H = AUDIT / "P12H_A1_PROTOCOL_CLOSURE_AUDIT.md"
P12M = AUDIT / "P12M_AUTHOR_REQUEST_DRAFTS.md"
P12L_SPEC = AUDIT / "P12L_AUTHOR_DATA_REQUEST_SPEC.md"
P12Q = AUDIT / "P12Q_PI_DECISION_HANDOFF.md"
BPDIR = REPO / "paper9" / "plan" / "blueprint"
BP15 = BPDIR / "Paper9_Blueprint_v1.5.tex"
BP14 = BPDIR / "Paper9_Blueprint_v1.4.tex"
PROVENANCE = BPDIR / "PROVENANCE.md"
RULE = REPO / "paper9" / "verification" / "suite" / "rule_rfit.py"
MANUSCRIPT_SECTIONS = REPO / "paper9" / "latex" / "sections"

# PI authorisation 2026-09-24 (paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md,
# paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md): the live register now carries
# P5 = "PASS" and R-1 = "CLOSED". Phase-era records and matrices keep their own values
# verbatim; only live-record expectations follow the authorised change.
GATES = {"PCR1": "NOT PASS", "G3": "NOT MET", "G4": "NOT MET", "P5": "PASS",
         "R-1": "CLOSED", "PCR5": "PASS", "P13": "BLOCKED"}
FROZEN = {
    BP15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    BP14: "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638",
    PROVENANCE: "f4ab0b71a36af5f25fb226b3453d59e7bf6fade06fbd5c140ffd72aeb0441418",
    RULE: "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
}
P12M_SHA = "2f68e66fa82dbf8b18420d9da33c34cb726d47433c7ce1875c5a19c8267cec61"
P12L_SHA = "8acb70f1fccdb93cb910a6365e0ca4cb688eb1636d1a923f81c88d3a2168fc89"
MATRIX_ROWS = ("B2", "B3", "PCR1", "G3", "G4", "P5", "R-1", "C-1", "P13")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _rec() -> dict:
    return json.loads(RECORD.read_text())


def _m() -> dict:
    return json.loads(MATRIX_JSON.read_text())


def _flat(p: Path) -> str:
    return " ".join(p.read_text(errors="ignore").split())


def _mdflat(p: Path) -> str:
    """Flatten markdown, dropping blockquote markers so quoted sentences stay contiguous."""
    lines = [re.sub(r"^\s*>\s?", "", l) for l in p.read_text(errors="ignore").splitlines()]
    return " ".join(" ".join(lines).split())


# ---------------------------------------------------------------- 1. B2
def test_b2_dependency_classification():
    b2 = _rec()["benchmarks"]["B2"]
    assert b2["route"] == "NOT_VALIDATED"
    assert b2["ambiguity_status"].startswith("UNRESOLVED")
    assert b2["parameter_completeness"].startswith("INCOMPLETE")
    assert b2["reproduction_status"] == "NOT REPRODUCED under any admissible interpretation"
    row = _m()["B2"]
    assert row["status"] == "NOT_VALIDATED" and row["category"] == "AUTHOR DATA REQUIRED"
    assert "A2.4" in row["governing_rule"]
    assert "length-scale definition" in row["exact_missing_item"]
    doc = _flat(AUDIT_DOC)
    assert "A2.4" in doc and "necessary but not shown to be sufficient" in doc
    assert "NOT_VALIDATED" in doc


# ---------------------------------------------------------------- 2. B3
def test_b3_dependency_classification():
    b3 = _rec()["benchmarks"]["B3"]
    assert b3["route"] == "NOT_VALIDATED"
    assert b3["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    row = _m()["B3"]
    assert row["status"] == "NOT_VALIDATED" and row["category"] == "AUTHOR DATA REQUIRED"
    assert "G1" in row["governing_rule"] and "G2" in row["governing_rule"]
    assert "Fig. 4(c) parameter set" in row["exact_missing_item"]
    doc = _flat(AUDIT_DOC)
    assert "source-side parameter/normalisation insufficiency" in doc
    assert "is *not* validation" in doc or "Documentation is *not* validation" in doc


# ---------------------------------------------------------------- 3. PCR1
def test_pcr1_dependency_chain():
    t = BP15.read_text()
    assert "quantitative validation" in t and "graphical validation" in t
    assert "A benchmark that is neither is \\textbf{not validated}" in t
    assert _rec()["gate_state"]["PCR1"] == "NOT PASS"
    row = _m()["PCR1"]
    assert row["status"] == "NOT PASS"
    assert "B2" in row["exact_missing_item"] and "B3" in row["exact_missing_item"]
    doc = _flat(AUDIT_DOC)
    assert "PCR1 is **not** blocked by a requirement that every benchmark carry a quantitative error" in doc \
        or "not blocked by a requirement that every benchmark carry a quantitative error" in doc


# ---------------------------------------------------------------- 4. G3 / G4
def test_g3_g4_dependency_chain():
    t = BP15.read_text()
    assert "a benchmark met by neither route is \\textbf{not validated} and fails this gate" in t
    assert "the PI signs G4 only after PCR1--PCR8" in t
    gates = _rec()["gate_state"]
    assert gates["G3"] == "NOT MET" and gates["G4"] == "NOT MET"
    m = _m()
    assert m["G3"]["status"] == "NOT MET" and m["G4"]["status"] == "NOT MET"
    assert "PCR1" in m["G4"]["exact_missing_item"]
    doc = _flat(AUDIT_DOC)
    assert "G3 has no independent blocker beyond PCR1's" in doc
    assert "any failed pcr blocks exactly as g3 does" in doc.lower()


# ---------------------------------------------------------------- 5. P5
def test_p5_status():
    assert _rec()["gate_state"]["P5"] == "PASS"   # PI authorisation 2026-09-24
    assert _rec()["pi_authorisations_2026_09_24"]["P5"]["record"] == \
        "paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md"
    row = _m()["P5"]   # the P12AB matrix is a phase record and keeps its P12AB-era status
    assert row["status"] == "NOT PASS/OPEN" and row["category"] == "AUTHORISATION REQUIRED"
    assert "reconciliation decision" in row["exact_missing_item"]
    status = _mdflat(P5_STATUS)
    assert "CONTESTED" in status and "at most one [S] set and one gate statement can stand" in status
    hl = json.loads(P5_HIGHLIGHTS.read_text())
    assert hl["param_hash"] == "09dd73f4ab49a3e93316da839fc3b18e36f94f3eb221a7a43cd7f529fb51dae8"
    assert len(hl["completed_studies"]) == 8
    assert P5_RAW.exists()
    # the manuscript carries no P5-production claims (P12C finding, re-verified here)
    hits = [p for p in MANUSCRIPT_SECTIONS.glob("*.tex") if "production/p5" in p.read_text()]
    assert hits == []


# ---------------------------------------------------------------- 6. R-1
def test_r1_status():
    assert _rec()["gate_state"]["R-1"] == "CLOSED"   # PI authorisation 2026-09-24
    assert _rec()["pi_authorisations_2026_09_24"]["R-1"]["record"] == \
        "paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md"
    row = _m()["R-1"]   # the P12AB matrix is a phase record and keeps its P12AB-era status
    assert row["status"] == "OPEN" and row["category"] == "AUTHORISATION REQUIRED"
    h = _flat(P12H)
    assert "Property B is unachieved and closing it requires the explicitly unauthorized re-baseline" in h
    assert "must never be restated as solver or pipeline determinism" in h
    doc = _flat(AUDIT_DOC)
    for concern in ("Scientific reproducibility", "Solver determinism", "Environment sensitivity",
                    "Fit-subset reproducibility", "Governing-artifact reproducibility"):
        assert concern in doc, concern
    assert "CLOSED only after an authorised numerical rerun" in doc
    # no run was performed in this phase
    assert "not executed" in doc


# ---------------------------------------------------------------- 7. P13
def test_p13_prerequisite_matrix():
    m = _m()
    assert set(m) >= set(MATRIX_ROWS)
    assert m["P13"]["status"] == "BLOCKED"
    for key in MATRIX_ROWS:
        row = m[key]
        assert set(row) >= {"status", "evidence_available", "governing_rule", "exact_missing_item",
                            "supplier", "can_close_now", "next_legitimate_action"}, key
    md = MATRIX_MD.read_text()
    assert "| Blocker | Evidence available | Governing rule | Exact missing item" in md
    for key in MATRIX_ROWS:
        assert f"**{key}**" in md, key
    doc = _flat(AUDIT_DOC)
    checklist = doc[doc.index("Part G — P13 entry criteria"):doc.index("Part H — no-gate-lowering test")]
    for item in ("PCR1", "PCR2", "PCR3", "PCR4", "PCR5", "PCR6", "PCR7", "PCR8",
                 "G1", "G2", "G3", "G4", "P5", "R-1", "C-1", "G-1"):
        assert item in checklist, item
    for state in ("NOT PASS", "NOT MET", "OPEN", "CLOSED", "PENDING", "BLOCKED"):
        assert state in checklist, state
    assert "P13 BLOCKED — BOTH EXTERNAL AND INTERNAL BLOCKERS" in doc \
        or "BOTH EXTERNAL AND INTERNAL BLOCKERS" in doc


# ---------------------------------------------------------------- 8. no gate lowering
def test_no_gate_lowering_route():
    doc = _flat(AUDIT_DOC)
    assert doc.count("NOT PERMITTED") >= 9
    assert doc.count("PERMITTED ONLY WITH AUTHORISATION") >= 2
    # thresholds and the frozen rule are untouched
    t = BP15.read_text()
    assert "≤2\\%" in t or "$\\le2\\%$" in t or "le2" in t
    assert _sha(RULE) == FROZEN[RULE]
    rule_rec = json.loads((AUDIT / "evidence" / "p12h" / "rule_rfit_governing.json").read_text())
    assert rule_rec["rule"]["F"] == 3.0
    assert rule_rec["rule"]["min_admissible"] == 3
    # no percentage may be attached to the graphical routes
    assert "A2.5" in doc


# ---------------------------------------------------------------- 9. author requests
def test_author_request_status_unchanged():
    assert _sha(P12M) == P12M_SHA and _sha(P12L_SPEC) == P12L_SHA
    assert "PREPARED, NOT SENT" in _flat(P12M)
    assert "no contact has been initiated" in _flat(P12L_SPEC)
    q = _flat(P12Q)
    assert "NOT AUTHORIZED" in q and "NOT SENT" in q
    for tpl in ("B1", "B2", "B3"):
        assert (AUDIT / "author_data" / f"{tpl}_DATA_RECEIPT_TEMPLATE.md").exists()
    row = _m()["P13"]
    assert "author" in row["supplier"]
    doc = _flat(AUDIT_DOC)
    assert "Nothing was sent; no author was contacted." in doc


# ---------------------------------------------------------------- 10. governing spec
def test_current_blueprint_v15_governing_specification():
    for p, h in FROZEN.items():
        assert _sha(p) == h, p
    prov = PROVENANCE.read_text()
    tail = prov.split("Added 2026-09-24 (P12R)", 1)[1]
    assert "| Paper9_Blueprint_v1.5.tex | 1.5 | b96c8e76" in tail
    assert tail.count("CURRENT governing specification") == 1
    rec = _rec()
    assert rec["governing_spec"].startswith("Paper9_Blueprint v1.5")
    assert rec["gate_state"]["PCR5"] == "PASS"
    for k, v in GATES.items():
        assert rec["gate_state"][k] == v, k
    m = _m()
    assert "v1.5" in m["governing_specification"] and "A2" in m["governing_specification"]
    assert m["gate_logic_changed"] is False and m["thresholds_changed"] is False and m["routes_changed"] is False
    # the P12AA matrix is retained as history
    assert P12AA_MATRIX.exists()
