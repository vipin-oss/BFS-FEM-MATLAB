#!/usr/bin/env python3
"""P12Y — traceability / governance cleanup guards.

P12X reported two follow-up findings. P12Y audits them and pins the conclusions:

* **P12X-F1** — `traceability_matrix.csv` row TV1 read ``CLOSED [C]`` while the authoritative
  `traceability_matrix.json` reads ``CLOSED [S]`` (P11D retag ``[C] -> [S]``). Verified as a
  **genuine stale active register value**: the CSV's TV rows were written at ``c150c0d`` (06:13)
  *before* the retag commit ``df7e26c`` (09:12) and were never re-synced. The register is an active
  governance artifact (cited by the master plan, P10/P11 stage audits and the P8/P9 release audits),
  so the smallest possible correction was applied: the **status cell only**, ``CLOSED [C]`` →
  ``CLOSED [S]``. Nothing else in any row, no benchmark status, no gate and no number changed.
* **P12X-F2** — `P12N` cites the “authoritative Blueprint v1.4 (line 457 …)” thresholds. Verified as
  **historical-only / no correction**: the citation sits inside P12N's “Package consistency audit
  (read-only; performed in this phase)” section — a statement of the state *at its time* — which the
  governing A2 amendment itself classifies as such (“remain valid as statements of the state *at
  their time*”, §5). ``[C]``/``[S]``/``[A]`` are the Blueprint's parameter-provenance tags
  (``[C]`` cited / ``[A]`` analytically defined / ``[S]`` assumed-with-justification); the same
  threshold values (≤ 2 %, ≤ 0.5 % classical) carry both versions, and v1.5 states them unchanged.
  The version chain is registered authoritatively in `plan/blueprint/PROVENANCE.md`, which declares
  v1.5 **CURRENT governing specification** and v1.4 **FROZEN, superseded**.

These guards freeze both conclusions and the immutability anchors the audit relied on.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit"
CSV = AUDIT / "traceability_matrix.csv"
TM_JSON = AUDIT / "traceability_matrix.json"
RECORD = AUDIT / "benchmark_validation_record.json"
P12N = AUDIT / "P12N_AUTHOR_DATA_HANDOFF.md"
P12L_BLOCKER = AUDIT / "P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md"
P12O = AUDIT / "P12O_AUTHOR_DATA_BLOCKER_DECISION.md"
P12Q = AUDIT / "P12Q_PI_DECISION_HANDOFF.md"
P12L_SPEC = AUDIT / "P12L_AUTHOR_DATA_REQUEST_SPEC.md"
P12M_DRAFT = AUDIT / "P12M_AUTHOR_REQUEST_DRAFTS.md"
A2_AMEND = AUDIT / "BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md"
PROVENANCE = REPO / "paper9" / "plan" / "blueprint" / "PROVENANCE.md"
BP14 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.4.tex"
BP15 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex"
AUDIT_DOC = AUDIT / "P12Y_TRACEABILITY_GOVERNANCE_CLEANUP.md"
RAW = AUDIT / "evidence" / "p12s" / "p12s_validation_record.json"

# ---- pins ------------------------------------------------------------------
# P12Y-era pins, retained as history: 4ce06f024bf41f12... / 0407f46038140db5...
CSV_SHA256_CORRECTED_P12Y = "4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04"
CSV_MINUS_TV1_SHA256_P12Y = "0407f46038140db55db6052fd0c109f25bd1e71a950fb7aa8953b4676df89b3b"
# P12AA re-pointed the two byte pins after the authorised O1/O2/O3 register remediation.
CSV_SHA256_CORRECTED = "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201"
CSV_MINUS_TV1_SHA256 = "e497a1e7a549c5276d52f39e98f57cb9f794bbe00c555fd86046ce442a255fc9"
TV1_NOTE = ("Section 4.2 text and Fig 3(b) in archival PDF verify c1=0.15, cR=1.5, "
            "d1=0.25, dR=1.5")
# P12AA aligned TV6 with the authoritative JSON (P12Z-O3), so LOCKED [S] rises to 3 and the
# PARTIAL [S] entry disappears; the P12Y-era tally is retained as history in the P12AA audit record.
TV_STATUS_TALLY = {"CLOSED [C]": 3, "CLOSED [S]": 4, "LOCKED [A]": 1, "LOCKED [S]": 3}
FROZEN = {
    BP15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    BP14: "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638",
    PROVENANCE: "f4ab0b71a36af5f25fb226b3453d59e7bf6fade06fbd5c140ffd72aeb0441418",
    P12N: "66fdb7c6af0b7acd88a8cf19c1597a979e9af8265a0037049703a2986af06e53",
    P12L_BLOCKER: "e9be752001af59f4aef35a7cd173b3faacc88deb42466557ae1928117b1f8d1f",
    P12O: "154b8d00148f8a4bf8d1b88acf8c94178bbc89c486cc7b045aa8906a9169917c",
    P12Q: "1f06035024b29aed39688a293a613fed9b0069c887d9e36a0cfbafb22e3e6a54",
    P12L_SPEC: "8acb70f1fccdb93cb910a6365e0ca4cb688eb1636d1a923f81c88d3a2168fc89",
    P12M_DRAFT: "2f68e66fa82dbf8b18420d9da33c34cb726d47433c7ce1875c5a19c8267cec61",
    A2_AMEND: "c008a00e1946599e7cf3eb23ffbc4cb52ea5356e40f7e1fbb5e37b9d8276b7b9",
    RAW: "cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21",
}
MANUSCRIPT_TEX_SET_SHA256 = "a934223187f6e78effe1a5caa93e307808f5958f99911c571ba929194022aaec"  # re-pointed by P12AF (2026-09-24): the authorised A2 manuscript re-tiering in sec05_verification.tex
GATES = {"PCR1": "NOT PASS", "G3": "NOT MET", "G4": "NOT MET", "P5": "NOT PASS/OPEN",
         "R-1": "OPEN", "PCR5": "PASS", "P13": "BLOCKED"}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _rows() -> list[dict]:
    return list(csv.DictReader(io.StringIO(CSV.read_text())))


def _tv_rows() -> list[dict]:
    return [r for r in _rows() if r["claim_id"].startswith("TV")]


def _rec() -> dict:
    return json.loads(RECORD.read_text())


def _flat(p: Path) -> str:
    return " ".join(p.read_text(errors="ignore").split())


def _manuscript_set_hash() -> str:
    names = sorted(str(q) for q in (REPO / "paper9" / "latex").rglob("*.tex"))
    return hashlib.sha256("".join(hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names).encode()).hexdigest()


# ------------------------------------------------------- F1: the register correction
def test_tv1_classification_now_matches_the_authoritative_retag():
    tv1 = [r for r in _rows() if r["claim_id"] == "TV1"][0]
    assert tv1["status"] == "CLOSED [S]"
    assert "[C]" not in tv1["status"]
    js = json.loads(TM_JSON.read_text())["technical_variations"]["TV1"]
    assert js["status"] == "CLOSED [S]"
    assert tv1["status"].split()[-1] == js["status"].split()[-1] == "[S]"


def test_tv1_correction_was_the_status_cell_only():
    # the P12Y-era byte pins are retained as history; the working pins track the P12AA-remediated state
    assert CSV_SHA256_CORRECTED_P12Y == "4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04"
    assert CSV_MINUS_TV1_SHA256_P12Y == "0407f46038140db55db6052fd0c109f25bd1e71a950fb7aa8953b4676df89b3b"
    assert _sha(CSV) == CSV_SHA256_CORRECTED
    lines = CSV.read_text().splitlines(keepends=True)
    rest = "".join(l for l in lines if not l.startswith("TV1,"))
    assert hashlib.sha256(rest.encode()).hexdigest() == CSV_MINUS_TV1_SHA256, \
        "the register outside the TV1 row is not the pinned current state"
    tv1 = [r for r in _rows() if r["claim_id"] == "TV1"][0]
    assert tv1["notes"] == TV1_NOTE, "the TV1 note must be byte-identical (status cell only)"
    assert tv1["claim_id"] == "TV1" and tv1["phase"] == "P11"


def test_register_row_structure_and_classes_unchanged_elsewhere():
    rows = _rows()
    assert len(rows) == 46
    tv = _tv_rows()
    assert len(tv) == 11
    from collections import Counter
    assert dict(Counter(r["status"] for r in tv)) == TV_STATUS_TALLY
    # every TV claim shared with the authoritative JSON carries the same provenance class
    js = json.loads(TM_JSON.read_text())["technical_variations"]
    shared = [r for r in tv if r["claim_id"] in js]
    assert shared, "expected TV rows shared with the JSON matrix"
    for r in shared:
        assert r["status"].split()[-1] == js[r["claim_id"]]["status"].split()[-1], \
            f"{r['claim_id']}: provenance class differs between the CSV and the JSON"


def test_retag_rationale_is_recorded_in_the_authoritative_matrix():
    res = json.loads(TM_JSON.read_text())["technical_variations"]["TV1"]["resolution"]
    assert "RETAGGED [C] -> [S] in P11D" in res
    assert "annotates NO c_bar/d_bar values" in res
    assert "must never be described as author-specified Fig. 4(c) parameters ([C])" in res
    # the retag record also lives in the TV-resolution addendum and the P11D remediation audit
    assert "CLOSED with provenance [S] (inherited / source-derived), NOT [C]" in _flat(AUDIT / "P3_TV_RESOLUTION.md")
    assert "CLOSED [C] → CLOSED [S]" in _flat(AUDIT / "P11D_REMEDIATION_AUDIT.md")


def test_provenance_tag_semantics_come_from_the_governing_blueprint():
    t = _flat(BP15)
    assert "[C] cited / [A] analytically defined / [S] assumed-with-justification" in t
    assert "Every parameter carries a provenance tag [C]/[A]/[S]" in t


def test_correction_changed_no_benchmark_status_gate_or_number():
    b = _rec()["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B2"]["ambiguity_status"].startswith("UNRESOLVED")
    assert b["B3"]["route"] == "NOT_VALIDATED"
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    for k in ("B1", "B2", "B3"):
        assert b[k]["quantitative_error"] is None
    g = _rec()["gate_state"]
    for k, v in GATES.items():
        assert g[k] == v, f"{k}: {g[k]!r}"
    # no percentage error anywhere in the benchmark record's blocks
    assert "%" not in json.dumps(b)
    # the register's numerical/claim rows were untouched (file-level pin above)


# ------------------------------------------------------- F2: the v1.4 references
def test_p12n_v14_citation_is_a_historical_check_statement_and_is_preserved():
    assert _sha(P12N) == FROZEN[P12N], "P12N must remain byte-identical (historical record)"
    t = _flat(P12N)
    assert "Package consistency audit (read-only; performed in this phase)" in t
    assert "Threshold wording agrees with the authoritative Blueprint v1.4 (line 457" in t
    assert "agrees — **no threshold introduced or changed**" in t


def test_governing_amendment_classifies_the_live_chain_as_statements_of_their_time():
    t = _flat(A2_AMEND)
    assert "remain valid as statements of the state *at their time*" in t
    for name in ("P12L_*", "P12N_*", "P12O_*", "P12Q_*"):
        assert name in t, f"A2 §5 must list {name}"
    assert _sha(A2_AMEND) == FROZEN[A2_AMEND]


def test_live_chain_records_are_byte_identical():
    for p in (P12L_BLOCKER, P12O, P12Q):
        assert _sha(p) == FROZEN[p], f"{p.name} was rewritten"


def test_provenance_declares_v15_current_and_v14_superseded():
    t = PROVENANCE.read_text()
    assert "| Paper9_Blueprint_v1.4.tex | 1.4 | 2ae0b1e8" in t
    assert "FROZEN, superseded by v1.5; byte-identical since creation" in t
    assert "| Paper9_Blueprint_v1.5.tex | 1.5 | b96c8e76" in t
    assert "CURRENT governing specification" in t
    assert "deliberately left unedited" in t


def test_v15_supersedes_v14_without_changing_the_thresholds():
    assert _sha(BP14) == FROZEN[BP14] and _sha(BP15) == FROZEN[BP15]
    def pcts(p: Path) -> set[str]:
        return {m.group(1) for m in re.finditer(r"(\d+(?:\.\d+)?)\s*\\?\\?%", p.read_text())}
    assert pcts(BP14) == pcts(BP15), "v1.5 must not introduce or remove a threshold value"
    assert {"0.5", "2"} <= pcts(BP15)
    a2 = _flat(A2_AMEND)
    assert "thresholds unchanged" in a2 and "2 %" in a2 and "0.5 %" in a2
    # and the active machine record declares v1.5 as its governing spec
    assert _rec()["governing_spec"].startswith("Paper9_Blueprint v1.5")


def test_no_active_record_claims_v14_is_the_governing_version():
    for p in (RECORD, CSV, TM_JSON, P12Q, P12O):
        s = p.read_text(errors="ignore")
        for bad in ("v1.4 is the governing", "governing Blueprint v1.4", "authoritative Blueprint v1.4"):
            if p is P12N:
                continue  # historical citation, asserted above
            assert bad not in s, f"{p.name}: {bad!r}"


# ------------------------------------------------------- the reported gap (no correction)
def test_register_version_gap_is_recorded_and_left_uncorrected():
    """P12Y-F3: the claim register's latest blueprint row is the P12H A1 row (BP-v1.4); no A2/v1.5
    row exists. Reported, not corrected (no false statement; v1.5 is registered in PROVENANCE.md)."""
    rows = _rows()
    ids = [r["claim_id"] for r in rows]
    assert "BP-v1.3" in ids and "BP-v1.4" in ids
    assert "BP-v1.5" not in ids, "if this ever fails, re-audit the P12Y-F3 disposition"
    t = _flat(AUDIT_DOC)
    assert "P12Y-F3" in t and "not corrected" in t.lower()


# ------------------------------------------------------- hierarchy / author-data / anchors
def test_author_requests_remain_drafts_and_unsent():
    assert _sha(P12L_SPEC) == FROZEN[P12L_SPEC]
    assert _sha(P12M_DRAFT) == FROZEN[P12M_DRAFT]
    assert "NOT AUTHORIZED / NOT SENT" in _flat(P12Q)
    for p in (P12O, P12Q):
        assert "NOT SENT" in _flat(p) or "not sent" in _flat(p).lower()


def test_immutability_anchors_used_by_this_audit():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"
    assert _manuscript_set_hash() == MANUSCRIPT_TEX_SET_SHA256
    for name in ("b3_formulation_identity.txt", "li2024_fig2_digitisation.json",
                 "li2023_fig3_fig4_digitisation.json"):
        assert (AUDIT / "evidence" / "p12v" / name).exists(), f"P12V evidence missing: {name}"
