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

MANUSCRIPT_TEX_SET_SHA256 = "bd103c5f8ee14565f76d2dbc9dda221d5a620163f2ba654386f85edcc00d93b6"  # re-pointed by P12AG (2026-09-24): build repair added \usepackage{ragged2e} to ms.tex;; re-pointed again by the P5 n = 16 production repair (PI-authorised 2026-09-24), which updates the production-dependent numbers in Sections 1 and 5-9 and ms.tex; the P12AG value stays recorded in paper9/audit/P5_MESH16_REPAIR.md
  # re-pointed by the final-closure Table 5 caption correction (2026-09-25): the caption
  # listed the tabulated aspect-ratio subset as AR in {1, 2, 5, 10} while the regenerated
  # table tabulates AR in {1, 3, 5, 10} (tables/gen/tab05_gap_summary.py selects
  # [1.0, 3.0, 5.0, 10.0]); the caption is corrected to the tabulated subset. No number,
  # figure, table, gate, status or decision is changed; the previous value stays recorded
  # in paper9/audit/P5_MESH16_REPAIR.md.
  # re-pinned after the printed-precision reduction of the P5 n = 16 repair (PI-authorised
  # 2026-09-24): the mesh-stability rule moved S_theta to 2 dp, the delta_max invariance bound
  # to 1e-5 deg and the theta -> 90 - theta bound to 1e-7 deg; the previous value is recorded
  # in paper9/audit/P5_MESH16_REPAIR.md.
  # re-pointed once more by the final-closure Section 6 correction (2026-09-25): it removes the
  # unsupported Figure 10 caption claim of monotonic gap opening with increasing AR and the
  # Section 6 claim that no directional gap opens at AR = 1, both contradicted by the n = 16
  # production data recorded in this repository; the previous value stays recorded in
  # paper9/audit/P5_MESH16_REPAIR.md.
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
    # P5/R-1 follow the PI authorisation of 2026-09-24. PCR1/G3 follow the reassessment of 2026-09-25 (amendment A3, paper9/audit/PI_DECISION_A3_AMENDMENT.md): PCR1 NOT PASS -> PASS, G3 NOT MET -> MET. G4 remains NOT MET (PI signature not given) and P13 remains BLOCKED.
    assert (g["PCR1"], g["G3"], g["G4"], g["P5"], g["R-1"], g["PCR5"], g["P13"]) == (
        "PASS", "MET", "NOT MET", "PASS", "CLOSED", "PASS", "BLOCKED")
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
    # P12AD itself adopted no P5 gate sentence; the live PASS follows the later PI authorisation
    # of 2026-09-24 recorded in paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md.
    assert _rec()["gate_state"]["P5"] == "PASS"


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
    # re-pointed 2026-09-24: the deltas are the two PI-authorised gate values (P5 PASS,
    # R-1 CLOSED) and the provenance block recording them; see PI_DECISION_P5_GATE_ADOPTION.md
    # and PI_DECISION_R1_MEASURED_ADJUDICATION.md.
    # re-pointed 2026-09-25 for the A3 reassessment (PCR1 PASS, G3 MET) and its provenance
    # block; see paper9/audit/PI_DECISION_A3_AMENDMENT.md.
    assert _sha(RECORD) == "44593c1a6b382691860062e1dcb87f41b051e77da02d99969ee0a71533a46fea"
    assert _sha(AUDIT / "traceability_matrix.json") == "83ff8723b0abd329c307c03772494cf9b9c93f7967be39c5d49ce31512934013"
    assert _sha(AUDIT / "traceability_matrix.csv") == "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201"
    assert _sha(P5_STATUS) == "1a410f228c117f3ada13557d643e1f1498a0f17881890f464e94e2e3f8489c8c"
