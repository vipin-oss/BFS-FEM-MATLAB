#!/usr/bin/env python3
"""P12Z — traceability register current-version / A2 governance guards.

P12Y recorded one observation (**P12Y-F3**): the register has no explicit A2 / Blueprint-v1.5 row.
P12Z audited the register schema, the A2 chain and the CSV/JSON consistency, and decided

    **A — NO CORRECTION — CURRENT TRACEABILITY SUFFICIENT**

because the governing schema does not require a register row per blueprint revision (version
governance is carried by `paper9/plan/blueprint/PROVENANCE.md`, the file the register's own `BP-v1.3`
row cites as its derivation document), and because no link of the A2 chain loses traceability.
These guards freeze that decision. In particular they assert that **no register row was added and no
register file was touched** (no cosmetic completion), that there is exactly one *operative* current
governing blueprint (v1.5; the older `CURRENT` label sits above the additive amendment marker and is
declared stale by the file itself), that v1.4 remains historical/frozen, that A2 is traceable through
v1.5 §13 + the amendment record + the route classifier/guards + B1's route label, and that the
known P12Z observations (O1 v1.4 hash citation, O2 plan hash citation, O3 state-word-only TV
divergences) are *reported, not rewritten*.
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
AUDIT_DOC = AUDIT / "P12Z_REGISTER_CURRENT_VERSION_AUDIT.md"
A2_AMEND = AUDIT / "BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md"
P12Y_DOC = AUDIT / "P12Y_TRACEABILITY_GOVERNANCE_CLEANUP.md"
BPDIR = REPO / "paper9" / "plan" / "blueprint"
PROVENANCE = BPDIR / "PROVENANCE.md"
BP15 = BPDIR / "Paper9_Blueprint_v1.5.tex"
BP14 = BPDIR / "Paper9_Blueprint_v1.4.tex"
BP13 = BPDIR / "Paper9_Blueprint_v1.3.tex"
BP12 = BPDIR / "Paper9_Blueprint_v1.2.tex"
ROUTE = REPO / "paper9" / "verification" / "suite" / "benchmark_validation_route.py"
ROUTE_TEST = REPO / "paper9" / "verification" / "suite" / "test_p12r_graphical_validation_route.py"
P12Y_TEST = REPO / "paper9" / "verification" / "suite" / "test_p12y_traceability_cleanup.py"
PLAN = REPO / "paper9" / "plan" / "CALC_MASTER_PLAN.md"

# ---- pins ------------------------------------------------------------------
# P12AA re-pointed these two byte pins after the authorised O1/O2/O3 register remediation
# (canonical v1.4 hash, canonical plan hash, TV6 state word). The P12Z-era values are retained as
# history: CSV 4ce06f024bf41f12... / JSON f332e03117b60643... (see P12AA_TRACEABILITY_REMEDIATION_AUDIT.md).
CSV_SHA = "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201"
JSON_SHA = "83ff8723b0abd329c307c03772494cf9b9c93f7967be39c5d49ce31512934013"
FROZEN = {
    BP15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    BP14: "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638",
    BP13: "ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f",
    BP12: "742acc9ec97864999595e6c6248017285944747fe02c11eac86521334b06fe9c",
    PROVENANCE: "f4ab0b71a36af5f25fb226b3453d59e7bf6fade06fbd5c140ffd72aeb0441418",
    A2_AMEND: "c008a00e1946599e7cf3eb23ffbc4cb52ea5356e40f7e1fbb5e37b9d8276b7b9",
    ROUTE: "c5b26190248a1e7c6b82ca2858abe9698dcd61c2794a92ce46c678cb609e1870",
    ROUTE_TEST: "8e83d16e55ae963c77e6978f21c6db9d55dca05bc0f8f4ae0b8eb4197b602907",
    RECORD: "e41a9d23ab2472d332760ebd199fef6b13adf5ec10b0cbb40ec2b195caa8c8b8",
}
COLUMNS = ["claim_id", "phase", "object_or_claim", "blueprint_ref", "module_or_equation",
           "derivation_doc", "check_log", "status", "notes"]
# P12AA aligned TV6 with the authoritative JSON (P12Z-O3): LOCKED [S] 3, no PARTIAL row remains.
TV_TALLY = {"CLOSED [C]": 3, "CLOSED [S]": 4, "LOCKED [A]": 1, "LOCKED [S]": 3}
# TV6 was remediated in P12AA; the two remaining divergences are the repository's own accepted
# resolution-word variants (CLOSED vs LOCKED, identical provenance class) and stay unnormalised.
STATE_WORD_DIVERGENCES = {"TV14": ("CLOSED [S]", "LOCKED [S]"),
                          "TV18": ("CLOSED [S]", "LOCKED [S]")}
P12AA_DOC = AUDIT / "P12AA_TRACEABILITY_REMEDIATION_AUDIT.md"
# P12H-era register citations that no longer match the artifacts (P12Z-O1 / P12Z-O2), kept verbatim
V14_CITED = "0089754b076ff9e3"
PLAN_CITED = "a45a5448a76764d5"
PLAN_PRE_AMENDMENT = "0e2c3a3a0e47d435"
# PI authorisation 2026-09-24 (paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md,
# paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md): the live register now carries
# P5 = "PASS" and R-1 = "CLOSED". Phase-era records and matrices keep their own values
# verbatim; only live-record expectations follow the authorised change.
GATES = {"PCR1": "NOT PASS", "G3": "NOT MET", "G4": "NOT MET", "P5": "PASS",
         "R-1": "CLOSED", "PCR5": "PASS", "P13": "BLOCKED"}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _flat(p: Path) -> str:
    return " ".join(p.read_text(errors="ignore").split())


def _rows() -> list[dict]:
    return list(csv.DictReader(io.StringIO(CSV.read_text())))


def _tv_json() -> dict:
    return json.loads(TM_JSON.read_text())["technical_variations"]


def _rec() -> dict:
    return json.loads(RECORD.read_text())


# ------------------------------------------------------ decision A: nothing added
def test_register_files_are_byte_identical_no_row_added():
    assert _sha(CSV) == CSV_SHA
    assert _sha(TM_JSON) == JSON_SHA


def test_no_bp_v15_or_a2_row_exists_anywhere_in_the_register():
    ids = [r["claim_id"] for r in _rows()]
    assert "BP-v1.5" not in ids
    assert not any("v1.5" in i or "A2" in i for i in ids)
    blob = CSV.read_text() + TM_JSON.read_text()
    assert "v1.5" not in blob and "A2" not in blob
    assert "b96c8e76" not in blob, "the v1.5 hash must not be asserted inside the register"


def test_the_p12y_f3_disposition_is_preserved_and_the_decision_is_a():
    assert "P12Y-F3" in _flat(P12Y_DOC) and "not corrected" in _flat(P12Y_DOC).lower()
    assert "BP-v1.5" in _flat(P12Y_TEST)  # the P12Y guard still pins the absence
    t = _flat(AUDIT_DOC)
    assert "NO CORRECTION — CURRENT TRACEABILITY SUFFICIENT" in t
    assert "Decision: A" in t


# ------------------------------------------------------ register schema evidence
def test_register_schema_is_the_documented_claim_ledger():
    rows = _rows()
    assert list(rows[0].keys()) == COLUMNS
    assert len(rows) == 46 and len(CSV.read_text().splitlines()) == 47
    assert len({r["claim_id"] for r in rows}) == 46, "claim ids must be unique"
    families = {}
    for r in rows:
        m = re.match(r"[A-Za-z]+", r["claim_id"])
        families[m.group(0)] = families.get(m.group(0), 0) + 1
    assert families == {"BP": 2, "PLAN": 2, "M": 25, "F": 4, "TV": 11, "RFIT": 1, "RNAME": 1}
    # every row is phase-stamped (the register is an append-only claim ledger, not a state index)
    assert all(r["phase"] for r in rows)


def test_blueprint_rows_are_phase_stamped_revision_events():
    bp = [r for r in _rows() if r["claim_id"].startswith("BP-")]
    assert [r["claim_id"] for r in bp] == ["BP-v1.3", "BP-v1.4"]
    assert {r["phase"] for r in bp} == {"P0", "P12H"}
    assert all(r["status"] == "LOCKED" for r in bp)
    assert all("governing specification" in r["object_or_claim"] for r in bp)
    # the v1.3 row delegates version provenance to the authoritative ledger
    v13 = bp[0]
    assert v13["derivation_doc"] == "paper9/plan/blueprint/PROVENANCE.md"
    assert "ca71b91a" in v13["notes"]


# ------------------------------------------------------ exactly one current spec
def test_provenance_declares_exactly_one_operative_current_governing_blueprint():
    t = PROVENANCE.read_text()
    marker = "Added 2026-09-24 (P12R)"
    assert t.count("CURRENT governing specification") == 2
    head, tail = t.split(marker, 1)
    assert head.count("CURRENT governing specification") == 1, "pre-amendment history only"
    assert tail.count("CURRENT governing specification") == 1, "exactly one operative CURRENT row"
    assert "deliberately left unedited" in t, "the stale historical rows are declared so by the file"
    assert "| Paper9_Blueprint_v1.5.tex | 1.5 | b96c8e76" in tail
    assert tail.index("Paper9_Blueprint_v1.5.tex") < tail.index("CURRENT governing specification") + 200


def test_v14_is_historical_frozen_and_superseded():
    t = PROVENANCE.read_text()
    tail = t.split("Added 2026-09-24 (P12R)", 1)[1]
    assert "| Paper9_Blueprint_v1.4.tex | 1.4 | 2ae0b1e8" in tail
    assert "FROZEN, superseded by v1.5; byte-identical since creation" in tail
    assert "| Paper9_Blueprint_v1.2.tex | 1.2 | 742acc9e" in t and "FROZEN, superseded" in t
    # no active record treats v1.4 as governing
    assert not _rec()["governing_spec"].startswith("Paper9_Blueprint v1.4")


def test_frozen_blueprint_files_match_their_declared_hashes():
    assert _sha(BP15) == FROZEN[BP15]
    assert _sha(BP14) == FROZEN[BP14]
    assert _sha(BP13) == FROZEN[BP13]
    assert _sha(BP12) == FROZEN[BP12]


def test_current_governing_specification_is_machine_identifiable():
    rec = _rec()
    assert rec["governing_spec"] == "Paper9_Blueprint v1.5 (A2 graphical-validation route)"
    assert rec["governing_spec"].startswith("Paper9_Blueprint v1.5")
    assert "A2" in rec["governing_spec"]
    # the active benchmark record is the only machine record carrying a governing-spec field
    hits = [p for p in sorted(AUDIT.glob("*.json")) if '"governing_spec"' in p.read_text()]
    assert hits == [RECORD], f"unexpected governing_spec carriers: {hits}"


# ------------------------------------------------------ A2 traceability chain
def test_a2_is_traceable_through_the_frozen_blueprint_and_its_record():
    t = BP15.read_text()
    assert "\\section{AMENDMENT A2" in t
    assert "revision 1.4 $\\to$ 1.5" in t
    for state in ("Quantitative validation", "Graphical validation", "Not validated"):
        assert state in t, f"the blueprint must name the state: {state}"
    assert "A2.4" in t and "A2.5" in t and "A2.6" in t and "A2.8" in t
    a2 = _flat(A2_AMEND)
    assert _sha(A2_AMEND) == FROZEN[A2_AMEND]
    assert "no gate moves because A2 exists" in a2
    assert "no change to the quantitative thresholds" in a2
    assert "*existing* thresholds (≤ 2 %; ≤ 0.5 % classical target)" in a2
    assert "remain valid as statements of the state *at their time*" in a2
    # the version ledger states the threshold invariance explicitly
    assert "Quantitative thresholds unchanged (<= 2 %; <= 0.5 % classical target)" in _flat(PROVENANCE)


def test_the_route_classifier_and_its_guards_implement_the_a2_contract():
    assert _sha(ROUTE) == FROZEN[ROUTE]
    t = ROUTE.read_text()
    for ident in ("QUANTITATIVE_VALIDATION", "GRAPHICAL_VALIDATION", "NOT_VALIDATED"):
        assert f'"{ident}"' in t
    assert "THRESHOLD_GENERAL_PCT = 2.0" in t and "THRESHOLD_CLASSICAL_PCT = 0.5" in t
    assert _sha(ROUTE_TEST) == FROZEN[ROUTE_TEST]


def test_b1_b2_b3_routes_carry_the_a2_labels():
    b = _rec()["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION"
    assert b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED"
    assert b["B3"]["route"] == "NOT_VALIDATED"
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")


# ------------------------------------------------------ CSV / JSON consistency
def test_tv_provenance_classes_agree_between_csv_and_json():
    tvj = _tv_json()
    assert len(tvj) == 18
    assert all(re.search(r"(CLOSED|LOCKED|RESOLVED|DISCHARGED)", v["status"]) for v in tvj.values())
    tv = [r for r in _rows() if r["claim_id"].startswith("TV")]
    assert len(tv) == 11
    from collections import Counter
    assert dict(Counter(r["status"] for r in tv)) == TV_TALLY
    for r in tv:
        if r["claim_id"] in tvj:
            assert r["status"].split()[-1] == tvj[r["claim_id"]]["status"].split()[-1], r["claim_id"]


def test_state_word_only_divergences_are_documented_not_rewritten():
    tvj = _tv_json()
    for cid, (csv_word, json_word) in STATE_WORD_DIVERGENCES.items():
        row = [r for r in _rows() if r["claim_id"] == cid][0]
        assert row["status"] == csv_word
        assert tvj[cid]["status"] == json_word
        assert csv_word.split()[-1] == json_word.split()[-1], "no provenance-class conflict"
    t = _flat(AUDIT_DOC)
    assert "P12Z-O3" in t and "not rewritten" in t
    # P12AA remediated the one genuine state conflict (TV6) and recorded the decision
    tv6 = [r for r in _rows() if r["claim_id"] == "TV6"][0]
    assert tv6["status"] == tvj["TV6"]["status"] == "LOCKED [S]"
    a = _flat(P12AA_DOC)
    assert "P12AA-O3" in a and "TV14/TV18" in a


def test_historical_hash_citations_are_recorded_not_rewritten():
    blob = CSV.read_text() + TM_JSON.read_text()
    assert V14_CITED in blob and PLAN_CITED in blob and PLAN_PRE_AMENDMENT in blob
    # O1: the v1.4 hash cited is the P12H-time one; the frozen file carries the P12J-corrected hash
    assert V14_CITED not in _sha(BP14)
    # O2: the plan hash cited does not correspond to any reachable revision
    assert _sha(PLAN)[:16] != PLAN_CITED
    assert _sha(PLAN)[:16] != PLAN_PRE_AMENDMENT, "the pre-amendment value is the historical one"
    t = _flat(AUDIT_DOC)
    assert "P12Z-O1" in t and "P12Z-O2" in t and "Reported, not corrected" in t


# ------------------------------------------------------ gates / numbers unchanged
def test_gate_states_and_null_policy_unchanged():
    rec = _rec()
    for k, v in GATES.items():
        assert rec["gate_state"][k] == v, f"{k}: {rec['gate_state'][k]!r}"
    for k in ("B1", "B2", "B3"):
        assert rec["benchmarks"][k]["quantitative_error"] is None
    blob = json.dumps(rec["benchmarks"])
    assert "%" not in blob, "no percentage may enter any benchmark block"


def test_immutability_anchors_used_by_this_audit():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"
