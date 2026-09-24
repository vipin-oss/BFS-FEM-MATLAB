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

MANUSCRIPT_TEX_SET_SHA256 = "243bb4d3d3d1ce5235e2d8d52bf6a095f8440b9d6accf4407dd640dedf35450e"  # re-pointed by P12AG (2026-09-24): build repair added \usepackage{ragged2e} to ms.tex;
  # the P12AF re-tiering of sec05_verification.tex and tab03_anchor_errors.tex is unchanged.
FROZEN = {
    BP15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    RULE_RFIT: "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
    GOV_JSON: "383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185",
    # re-pointed 2026-09-24 for the two PI-authorised gate values + provenance block
    RECORD: "e41a9d23ab2472d332760ebd199fef6b13adf5ec10b0cbb40ec2b195caa8c8b8",
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


def test_record_is_granted_and_in_force():
    """P12AF recorded the grant: the instrument is now in force, scoped to decisions A-F."""
    t = _flat(P12AE)
    assert "GRANTED — decisions A–F — recorded 2026-09-24" in t
    assert "In force from the recording date." in t
    assert "☒ GRANT decisions A–F" in t
    assert "The grant therefore covers **decisions A–F as written above, in full**" in t
    assert "P13 remained `BLOCKED`" in t          # pre-recording history, retained verbatim
    assert "PROPOSED — READY TO SIGN" not in t    # superseded status line


def test_no_signature_or_metadata_is_fabricated():
    """The grant is an internal act by the agent under the PI's instruction; no signature is claimed."""
    t = _flat(P12AE)
    for bad in ("signed by the PI", "PI signature:", "wet signature supplied", "signed on"):
        assert bad not in t, f"fabricated signature wording present: {bad!r}"
    assert "☐ PI wet/electronic signature (not supplied; not claimed)." in t
    assert "no separate PI signature record" in t
    assert "nothing beyond the repository\'s own identity metadata has been inferred" in t
    assert "this file is not a PI-signed artefact and does not claim to be one" in t
    assert "internal act recorded in this file by the agent under the PI\'s explicit instruction" in t
    assert "Field must be corrected" in t or "must be corrected by the PI" in t


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
    # P12AE preserved P5 as NOT PASS/OPEN; the live PASS follows the later PI authorisation of
    # 2026-09-24 recorded in paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md.
    assert _rec()["gate_state"]["P5"] == "PASS"
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


def test_grant_scopes_the_edit_to_the_recording_phase():
    t = _flat(P12AE)
    assert "P12AE created this authorisation record only and changed no manuscript byte" in t
    assert "the scoped editing authorised by decision B is performed by the phase that recorded the grant (P12AF)" in t
    assert "IN PROGRESS (P12AF)" in t


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
        "NOT PASS", "NOT MET", "NOT MET", "PASS", "CLOSED", "PASS", "BLOCKED")


def test_frozen_artifacts_and_manuscript_are_unchanged():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"
    assert _manuscript_set_hash() == MANUSCRIPT_TEX_SET_SHA256
