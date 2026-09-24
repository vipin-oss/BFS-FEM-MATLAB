"""P12AD guards — the internal reconciliation / transition decision alters no status, no gate and no number.

Each test pins one claim of `paper9/audit/P12AD_INTERNAL_RECONCILIATION_DECISION.md` against the live
repository state, so that the decision record cannot drift away from the artefacts it reasons about.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit"
SUITE = REPO / "paper9" / "verification" / "suite"

RECORD = AUDIT / "benchmark_validation_record.json"
P12AD = AUDIT / "P12AD_INTERNAL_RECONCILIATION_DECISION.md"
P5_STATUS = AUDIT / "P5_STATUS.md"
GOV_JSON = SUITE / "p4b_5g_to_5i.json"
RULE_RFIT = SUITE / "rule_rfit.py"
BP15 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex"
RAW_P5 = REPO / "paper9" / "results" / "raw" / "p5_production_raw.json"
HIL_P5 = REPO / "paper9" / "results" / "processed" / "p5_production_highlights.json"

MANUSCRIPT_TEX_SET_SHA256 = "243bb4d3d3d1ce5235e2d8d52bf6a095f8440b9d6accf4407dd640dedf35450e"  # re-pointed by P12AG (2026-09-24): build repair added \usepackage{ragged2e} to ms.tex;
  # the P12AF re-tiering of sec05_verification.tex and tab03_anchor_errors.tex is unchanged.
P5_PARAM_HASH = "09dd73f4ab49a3e93316da839fc3b18e36f94f3eb221a7a43cd7f529fb51dae8"

FROZEN = {
    BP15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    RULE_RFIT: "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
    GOV_JSON: "383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185",
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _flat(p: Path) -> str:
    return " ".join(p.read_text(errors="ignore").split())


def _rec() -> dict:
    return json.loads(RECORD.read_text())


def _doc() -> str:
    return _flat(P12AD)


def _manuscript_set_hash() -> str:
    names = sorted(str(q) for q in (REPO / "paper9" / "latex").rglob("*.tex"))
    return hashlib.sha256(
        "".join(hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names).encode()
    ).hexdigest()


# ------------------------------------------------------------------ A. structure and statuses
def test_record_has_the_eight_required_sections():
    t = _doc()
    for h in ("## A. Scientific validation status", "## B. P5 disposition", "## C. R-1 disposition",
              "## D. C-1 disposition", "## E. Exact manuscript limitation text",
              "## F. P13 transition decision", "## G. Exact minimum remaining authorisations",
              "## H. External benchmark hunt"):
        assert h in t, f"missing section {h}"


def test_section_a_matches_the_live_machine_record():
    b = _rec()["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B3"]["route"] == "NOT_VALIDATED"
    assert [b[k]["quantitative_error"] for k in ("B1", "B2", "B3")] == [None, None, None]
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    t = _doc()
    assert "`GRAPHICAL_VALIDATION` / **PASS**" in t
    assert "**`NOT_VALIDATED`** — source-limited" in t
    assert "**NULL × 3**" in t


def test_section_a_gate_set_is_exactly_the_frozen_gate_set():
    g = _rec()["gate_state"]
    assert (g["PCR1"], g["G3"], g["G4"], g["P5"], g["R-1"], g["PCR5"], g["P13"]) == (
        "NOT PASS", "NOT MET", "NOT MET", "NOT PASS/OPEN", "OPEN", "PASS", "BLOCKED")
    t = _doc()
    for s in ("**NOT PASS**", "**NOT MET**", "**NOT PASS/OPEN**", "**BLOCKED**"):
        assert s in t


def test_decision_record_promotes_no_gate_and_asserts_no_percentage():
    t = _doc()
    for bad in ("PCR1 PASS", "PCR1: PASS", "G3 MET", "**G3 PASS**", "G4 MET", "G4 PASS",
                "G3 is met", "G3 now met", "G4 is met", "B2 PASS", "B3 PASS",
                "validated benchmark B2", "validated benchmark B3"):
        assert bad not in t, f"promotion wording present: {bad!r}"
    # the only fraction-like numbers allowed are the pinned transfer-matrix bound and the rule constants
    assert "no percentage, error bar or agreement number" in t
    assert re.search(r"agreement of \d", t) is None


# ------------------------------------------------------------------ B. P5 record retention
def test_p5_retained_record_is_named_and_is_the_only_complete_matrix():
    t = _doc()
    assert "results/raw/p5_production_raw.json" in t
    assert "results/processed/p5_production_highlights.json" in t
    raw, hil = json.loads(RAW_P5.read_text()), json.loads(HIL_P5.read_text())
    assert raw["param_hash"] == hil["param_hash"] == P5_PARAM_HASH
    assert raw["git_commit"].startswith("15814972") and hil["git_commit"].startswith("15814972")
    assert P5_PARAM_HASH[:8] in t and "15814972" in t


def test_p5_gate_statement_is_not_adopted_by_this_phase():
    t = _doc()
    assert "**P5 therefore remains `NOT PASS/OPEN`**" in t
    assert "does **not** adopt the Part A gate statement" in t
    s = _flat(P5_STATUS)
    assert "Branch-level P5 gate: CONTESTED" in s, "P5_STATUS.md must stay byte-unchanged (contested)"
    assert _rec()["gate_state"]["P5"] == "NOT PASS/OPEN"


def test_p5_decision_does_not_touch_pcr1_g3_g4():
    t = _doc()
    assert "**none** — all three are preserved exactly as in §A" in t


# ------------------------------------------------------------------ C. R-1
def test_r1_decision_retains_the_governing_artifact_without_a_new_run():
    t = _doc()
    assert "R-1 remains `OPEN`" in t
    assert "not executed here" in t
    g = json.loads(GOV_JSON.read_text())
    s = json.dumps(g)
    assert "4.173919246515192" in s, "governing rate must be unchanged"
    assert "4.180559" not in t and "4.180559" not in s


def test_r1_decision_declares_no_rebaseline():
    t = _doc()
    assert "no re-baseline" in t
    assert "`5.485710` remains uncited" in t


# ------------------------------------------------------------------ D. C-1
def test_c1_decision_keeps_rule_rfit_frozen():
    t = _doc()
    assert "**Rule R-fit is not changed**" in t
    assert "frozen Rule R-fit" in t
    assert _sha(RULE_RFIT) == FROZEN[RULE_RFIT]


# ------------------------------------------------------------------ E. limitation text
def test_limitation_text_is_present_and_carries_every_required_element():
    doc = P12AD.read_text()
    block = doc.split("## E. Exact manuscript limitation text")[1].split("## F.")[0]
    flat = " ".join(block.replace(">", " ").split())
    assert "graphical" in flat and "no" in flat and "numerical percentage asserted" in flat
    assert "could **not** be quantitatively or authoritatively validated" in flat
    assert "insufficient to reproduce them independently" in flat
    assert "reported as **not validated**" in flat
    assert "No numerical agreement value and no error percentage is claimed" in flat
    assert "formulation-consistency check and **not** a validation" in flat
    assert "not any deficiency of the present solver" in flat
    assert re.search(r"\d\s*%", flat) is None, "no percentage may appear in the limitation text"


def test_manuscript_is_not_edited_by_this_phase():
    assert _manuscript_set_hash() == MANUSCRIPT_TEX_SET_SHA256
    t = _doc()
    assert "not edited by this phase" in t


# ------------------------------------------------------------------ F. P13
def test_p13_transition_requires_authorisation_and_claims_no_gate():
    t = _doc()
    assert "only under an explicit PI authorisation recorded as an internal preparation act" in t
    assert "**submission remains prohibited**" in t
    assert "no gate is promoted" in t
    assert "P13 stays `BLOCKED`" in t


def test_p13_decision_does_not_start_p13():
    t = _doc()
    assert "neither starts P13 nor authorises submission" in t


# ------------------------------------------------------------------ G/H
def test_minimum_authorisations_are_enumerated_and_bounded():
    t = _doc()
    for i in range(1, 7):
        assert f"| {i} |" in t
    assert "No item above authorises" in t
    assert "Option A (send) remains a PI act" in t


def test_hunt_is_declared_permanently_closed():
    t = _doc()
    assert "CLOSED PERMANENTLY" in t
    assert "No further candidate search, benchmark-hunt phase, literature pass or metadata-only audit loop" in t
    assert "must not be reopened as a hunt" in t


# ------------------------------------------------------------------ frozen artefacts
def test_frozen_artifacts_are_unchanged():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"


def test_record_and_register_untouched_by_this_phase():
    assert _sha(RECORD) == "2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2"
    assert _sha(AUDIT / "traceability_matrix.json") == "83ff8723b0abd329c307c03772494cf9b9c93f7967be39c5d49ce31512934013"
    assert _sha(AUDIT / "traceability_matrix.csv") == "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201"
    assert _sha(P5_STATUS) == "1a410f228c117f3ada13557d643e1f1498a0f17881890f464e94e2e3f8489c8c"
