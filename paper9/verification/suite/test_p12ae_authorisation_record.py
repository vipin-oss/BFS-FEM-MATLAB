"""P12AE guards — the prepared PI-authorisation record changes no scientific record, no classification,
no gate, no Blueprint byte, no Rule R-fit byte and no manuscript byte.

The record is an *instrument*: these guards prove (a) that it is prepared and inert (not approved), and
(b) that preparing it moved nothing else in the repository.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit"
SUITE = REPO / "paper9" / "verification" / "suite"

P12AE = AUDIT / "P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md"
P12AD = AUDIT / "P12AD_INTERNAL_RECONCILIATION_DECISION.md"
RECORD = AUDIT / "benchmark_validation_record.json"
P5_STATUS = AUDIT / "P5_STATUS.md"
GOV_JSON = SUITE / "p4b_5g_to_5i.json"
RULE_RFIT = SUITE / "rule_rfit.py"
BP15 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex"

MANUSCRIPT_TEX_SET_SHA256 = "5ba2c22e7e7db2f51ef76f56a1539ff170eb01cd0302c55fa724f7be180ca24b"
FROZEN = {
    BP15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    RULE_RFIT: "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
    GOV_JSON: "383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185",
    RECORD: "2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2",
    P5_STATUS: "1a410f228c117f3ada13557d643e1f1498a0f17881890f464e94e2e3f8489c8c",
    AUDIT / "traceability_matrix.json": "83ff8723b0abd329c307c03772494cf9b9c93f7967be39c5d49ce31512934013",
    AUDIT / "traceability_matrix.csv": "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201",
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _flat(p: Path) -> str:
    return " ".join(p.read_text(errors="ignore").split())


def _plain(p: Path) -> str:
    """Whitespace-flattened text with markdown emphasis/quote markers removed (prose only)."""
    t = p.read_text(errors="ignore").replace(">", " ").replace("*", " ").replace("`", " ")
    return " ".join(t.split())


def _rec() -> dict:
    return json.loads(RECORD.read_text())


def _manuscript_set_hash() -> str:
    names = sorted(str(q) for q in (REPO / "paper9" / "latex").rglob("*.tex"))
    return hashlib.sha256(
        "".join(hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names).encode()
    ).hexdigest()


def _blockquote(path: Path, start: str, stop: str | None) -> str:
    text = path.read_text(errors="ignore")
    seg = text.split(start, 1)[1]
    if stop:
        seg = seg.split(stop, 1)[0]
    lines = [ln.lstrip("> ").strip() for ln in seg.splitlines() if ln.strip().startswith(">")]
    return " ".join(" ".join(lines).split())


# ------------------------------------------------------------------ the instrument
def test_record_exists_and_carries_decisions_a_to_f():
    t = _flat(P12AE)
    for h in ("### A. P13 manuscript-preparation transition", "### B. Manuscript editing",
              "### C. P5", "### D. R-1", "### E. C-1", "### F. Non-satisfaction statement"):
        assert h in t, f"missing decision section {h}"


def test_record_is_proposed_and_not_in_force():
    t = _flat(P12AE)
    assert "PROPOSED — READY TO SIGN — NOT SIGNED — NOT IN FORCE" in t
    assert "It is an authorisation instrument prepared for the PI to grant (or withhold)" in t
    assert "P13 remains `BLOCKED`" in t


def test_no_approval_is_claimed_or_inferred():
    t = _flat(P12AE)
    for bad in ("is approved", "has been approved", "has approved", "APPROVED",
                "signed by the PI on", "GRANTED (", "the PI has authorised the transition"):
        assert bad not in t, f"approval wording present: {bad!r}"
    assert "the agent does not sign, complete or infer it" in t
    assert "No explicit PI approval exists today" in t or "no explicit PI approval exists today" in t


def test_decision_a_is_preparation_only():
    t = _flat(P12AE)
    assert "AUTHORISE P13 MANUSCRIPT-PREPARATION TRANSITION ONLY" in t
    assert "does NOT mean PCR1, G3, or G4 has passed" in t
    assert "It does NOT authorise submission." in t


def test_decision_b_lists_the_six_required_items():
    t = _flat(P12AE)
    for phrase in ("insert the approved B1/B2/B3 limitation statement",
                   "perform the required A2 manuscript re-tiering",
                   "preserve B2 and B3 as `NOT_VALIDATED`",
                   "preserve the B3 formulation status as `ESTABLISHED / SOURCE-EQUIVALENT`",
                   "no numerical agreement value and no error percentage is claimed for B2/B3",
                   "not evidence of solver failure"):
        assert phrase in t, f"decision B missing: {phrase!r}"


def test_decision_b_scopes_the_edit_and_bounds_it():
    t = _flat(P12AE)
    assert "paper9/latex/sections/sec05_verification.tex" in t
    assert "paper9/tables/out/tab03_anchor_errors.tex" in t
    assert "nothing outside this list may change" in t
    assert "no percentage, ratio or \"agreement\" figure may be introduced anywhere" in t
    assert "Gate G3 formally `NOT MET`" in t


def test_decision_c_preserves_p5_exactly():
    t = _flat(P12AE)
    assert "retained numerical production record = the Part A matrix" in t
    assert "the P5 PASS gate sentence is NOT adopted" in t
    assert "P5 remains `NOT PASS/OPEN`" in t
    assert _rec()["gate_state"]["P5"] == "NOT PASS/OPEN"
    assert "Branch-level P5 gate: CONTESTED" in _flat(P5_STATUS)


def test_decision_d_preserves_r1_without_rerun_or_rebaseline():
    t = _flat(P12AE)
    assert "OPEN` as an internal governance item" in t
    assert "no rerun and no re-baseline is authorised by this phase" in t
    assert "4.173919246515192" in json.dumps(json.loads(GOV_JSON.read_text()))


def test_decision_e_preserves_c1_and_rule_rfit():
    t = _flat(P12AE)
    assert "closed as a criterion item under the frozen Rule R-fit" in t
    assert "No amendment to Rule R-fit" in t


def test_decision_f_statement_is_exact():
    t = _plain(P12AE)
    assert ("This authorisation permits controlled manuscript preparation only. It does not constitute "
            "PCR1, G3, or G4 satisfaction and does not authorise submission.") in t


def test_statuses_are_preserved_in_the_instrument():
    t = _flat(P12AE)
    for s in ("| PCR1 | **NOT PASS** |", "| G3 | **NOT MET** |", "| G4 | **NOT MET** |",
              "| P5 | **NOT PASS/OPEN** |", "| R-1 | **OPEN** |"):
        assert s in t, f"status row missing: {s!r}"


def test_author_data_route_and_hunt_are_preserved():
    t = _flat(P12AE)
    assert "**NOT SENT / NOT AUTHORISED**" in t
    assert "this instrument sends nothing and contacts no author" in t
    assert "permanently CLOSED" in t


def test_manuscript_editing_is_the_next_phase_not_this_one():
    t = _flat(P12AE)
    assert "Manuscript editing is the NEXT phase, not this one." in t
    assert "P12AE creates this authorisation record only." in t


def test_annex_limitation_statement_is_verbatim_from_p12ad():
    a = _blockquote(P12AD, "## E. Exact manuscript limitation text", "## F.")
    b = _blockquote(P12AE, "## Annex — the approved limitation statement", "## Verification performed")
    assert a and b
    assert a == b, "the annex statement must be the P12AD §E text, verbatim"


# ------------------------------------------------------------------ nothing else moved
def test_benchmark_classifications_unchanged():
    b = _rec()["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B3"]["route"] == "NOT_VALIDATED"
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    assert [b[k]["quantitative_error"] for k in ("B1", "B2", "B3")] == [None, None, None]


def test_pcr1_g3_g4_and_the_gate_set_are_unchanged():
    g = _rec()["gate_state"]
    assert (g["PCR1"], g["G3"], g["G4"], g["P5"], g["R-1"], g["PCR5"], g["P13"]) == (
        "NOT PASS", "NOT MET", "NOT MET", "NOT PASS/OPEN", "OPEN", "PASS", "BLOCKED")


def test_frozen_artifacts_and_manuscript_are_unchanged():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"
    assert _manuscript_set_hash() == MANUSCRIPT_TEX_SET_SHA256
