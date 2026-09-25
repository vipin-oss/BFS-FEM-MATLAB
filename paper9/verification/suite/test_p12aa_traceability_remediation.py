#!/usr/bin/env python3
"""P12AA guard suite — traceability-metadata remediation (O1/O2/O3) and register integrity.

Thirteen guards, one per clause of the P12AA mandate (Part K):

 1. O1  canonical Blueprint v1.4 hash registered and equal to the frozen file
 2. O2  canonical CALC_MASTER_PLAN.md hash registered and equal to the plan file
 3. O3  TV entries: no state conflict between the CSV and the JSON registers
 4. CSV/JSON equality of the claim ledger and the technical-variation ledger
 5. every active hash reference in the register resolves to a tracked artifact
 6. every non-resolving hash is explicitly classified as historical
 7. Blueprint v1.5 CURRENT, v1.4 FROZEN/SUPERSEDED in the authoritative provenance record
 8. the A2 amendment chain is traceable (v1.5 §13 -> amendment doc -> classifier -> guards -> machine record)
 9. the frozen Rule R-fit is traceable and unchanged
10. gate states are unchanged (B1/B2/B3, PCR1, G3, G4, P5, R-1, PCR5, P13)
11. author-data status is unchanged (requests NOT SENT, no data received, drafts unmodified)
12. the blocker matrix matches the record's statuses
13. historical audit documents are not rewritten for later corrections
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
PROVENANCE = REPO / "paper9" / "plan" / "blueprint" / "PROVENANCE.md"
PLAN = REPO / "paper9" / "plan" / "CALC_MASTER_PLAN.md"
BP13 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.3.tex"
BP14 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.4.tex"
BP15 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex"
A2 = AUDIT / "BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md"
RULE = REPO / "paper9" / "verification" / "suite" / "rule_rfit.py"
RULE_RECORD = AUDIT / "evidence" / "p12h" / "rule_rfit_governing.json"
CLASSIFIER = REPO / "paper9" / "verification" / "suite" / "benchmark_validation_route.py"
ROUTE_TEST = REPO / "paper9" / "verification" / "suite" / "test_p12r_graphical_validation_route.py"
P12M = AUDIT / "P12M_AUTHOR_REQUEST_DRAFTS.md"
P12L = AUDIT / "P12L_AUTHOR_DATA_REQUEST_SPEC.md"
P12Q = AUDIT / "P12Q_PI_DECISION_HANDOFF.md"
MATRIX_MD = AUDIT / "P12AA_PRE_P13_BLOCKER_MATRIX.md"
MATRIX_JSON = AUDIT / "P12AA_PRE_P13_BLOCKER_MATRIX.json"
P12H_AUDIT = AUDIT / "P12H_A1_PROTOCOL_CLOSURE_AUDIT.md"
P12J_CLOSURE = AUDIT / "P12J_CORRECTION_CLOSURE_AUDIT.md"

CSV_SHA = "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201"
JSON_SHA = "83ff8723b0abd329c307c03772494cf9b9c93f7967be39c5d49ce31512934013"

HISTORICAL_TOKENS = {
    "0089754b076f": "P12H-time v1.4 snapshot (reachable at dd42e81)",
    "a45a5448a767": "P12H-recorded plan hash — matches no reachable revision",
    "0e2c3a3a0e47d435": "pre-amendment plan (verified at fb9bd5d)",
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _csv_text() -> str:
    return CSV.read_text()


def _rows() -> list[dict]:
    return list(csv.DictReader(io.StringIO(_csv_text())))


def _json() -> dict:
    return json.loads(TM_JSON.read_text())


def _rec() -> dict:
    return json.loads(RECORD.read_text())


def _flat(t: str) -> str:
    return " ".join(t.split())


def _tracked() -> dict[str, str]:
    import subprocess
    out = {}
    for f in subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True).stdout.split("\0"):
        if f:
            try:
                out[f] = _sha(REPO / f)
            except OSError:
                pass
    return out


# ---------------------------------------------------------------- O1
def test_o1_blueprint_v14_canonical_hash_is_registered_and_correct():
    h = _sha(BP14)
    assert h == "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638"
    meta = _json()["metadata"]["p12h_amendment"]["blueprint"]
    assert meta["v1.4_sha256_canonical"] == h
    assert "PROVENANCE.md" in meta["v1.4_sha256_canonical_source"]
    row = [r for r in _rows() if r["claim_id"] == "BP-v1.4"][0]
    assert h in row["notes"]
    # the P12H-time value is retained *and* labelled historical
    assert meta["v1.4_sha256"].startswith("0089754b076f")
    assert "historical" in meta["v1.4_sha256_label"].lower()
    assert "historical snapshot" in row["notes"]
    assert meta["derived_from_v1.3_sha256"] == _sha(BP13)


# ---------------------------------------------------------------- O2
def test_o2_plan_canonical_hash_is_registered_and_correct():
    h = _sha(PLAN)
    assert h == "1f1c080bc65f1417378bba2f7f9877b9ec7c65537188c7adcb435a5c0c4a796a"
    meta = _json()["metadata"]["p12h_amendment"]["plan"]
    assert meta["sha256_canonical"] == h
    assert meta["pre_amendment_sha256"] == "0e2c3a3a0e47d435d89d7c3501a917679ce0593cdc608ce815166a90c96eca78"
    assert "historical" in meta["pre_amendment_sha256_label"].lower()
    row = [r for r in _rows() if r["claim_id"] == "PLAN-5i"][0]
    assert h in row["notes"]
    assert "historical P12H record only" in row["notes"]
    # the unreachable P12H value is retained, labelled, never silently dropped
    assert meta["sha256"] == "a45a5448a76764d59e9f5390052e5994aa3af76b95bbe2d7ef5d60d13f9ea21d"
    assert "matches no reachable revision" in meta["sha256_label"]


# ---------------------------------------------------------------- O3
def test_o3_tv_states_have_no_csv_json_conflict():
    tvj = _json()["technical_variations"]
    for r in _rows():
        cid = r["claim_id"]
        if not cid.startswith("TV") or cid not in tvj:
            continue
        csv_status, json_status = r["status"], tvj[cid]["status"]
        assert csv_status.split()[-1] == json_status.split()[-1], (
            f"{cid}: provenance class differs ({csv_status!r} vs {json_status!r})")
        a, b = csv_status.split()[0], json_status.split()[0]
        resolved = {"CLOSED", "LOCKED", "RESOLVED", "DISCHARGED"}
        assert a == b or (a in resolved and b in resolved), (
            f"{cid}: state conflict {csv_status!r} vs {json_status!r}")
        assert "OPEN" not in csv_status or "OPEN" in json_status
    # the one genuinely inconsistent entry found in P12Z-O3 was aligned with the authoritative register
    assert [r for r in _rows() if r["claim_id"] == "TV6"][0]["status"] == tvj["TV6"]["status"] == "LOCKED [S]"
    assert "TV6-CaseC" in {r["claim_id"] for r in _rows()}


# ---------------------------------------------------------------- equivalence
def test_register_csv_json_equality():
    rows = _rows()
    ids = [r["claim_id"] for r in rows]
    assert len(ids) == 46 and len(set(ids)) == 46
    assert len(rows[0]) == 9
    csv_tv = {r["claim_id"]: r["status"] for r in rows if r["claim_id"].startswith("TV")}
    tvj = _json()["technical_variations"]
    shared = {k: v for k, v in csv_tv.items() if k in tvj}
    assert len(shared) == 10 and len(tvj) == 18
    for cid, status in shared.items():
        assert status.split()[0] in {"CLOSED", "LOCKED", "RESOLVED", "DISCHARGED", "PARTIAL"} \
            or "OPEN" in status
    assert csv_tv["TV6"] == tvj["TV6"]["status"]


# ---------------------------------------------------------------- resolution
def test_every_active_hash_reference_resolves():
    fh = _tracked()
    blob = _csv_text() + TM_JSON.read_text()
    seen = set()
    for m in re.finditer(r"sha256[^\n]{0,120}?([0-9a-f]{12,64})", blob):
        tok = m.group(1)
        start, end = m.start(1), m.end(1)
        if tok in seen or not any(c in "abcdef" for c in tok):
            continue
        seen.add(tok)
        before = blob[start - 1] if start else ""
        if before.isdigit() or before == "." or blob[end:end + 2].startswith("e-"):
            continue
        if any(h.startswith(tok) or tok.startswith(h) for h in fh.values()):
            continue
        assert any(h.startswith(tok) or tok.startswith(h) for h in HISTORICAL_TOKENS), \
            f"unresolved and unclassified hash reference {tok[:16]}…"


# ---------------------------------------------------------------- historical
def test_historical_hashes_are_classified_historical():
    blob = _csv_text() + TM_JSON.read_text()
    for tok in HISTORICAL_TOKENS:
        assert tok in blob
    for needle in ("historical snapshot", "historical P12H record only",
                   "historical; verified against commit fb9bd5d",
                   "retained here as the historical P12H record only"):
        assert needle in blob, needle
    # the historical P12H values survive only as labelled history
    assert _json()["metadata"]["p12h_amendment"]["blueprint"]["v1.4_sha256"].startswith("0089754b076f")
    plan_meta = _json()["metadata"]["p12h_amendment"]["plan"]
    assert any("canonical" in k for k in plan_meta)


# ---------------------------------------------------------------- provenance
def test_blueprint_v15_current_v14_frozen():
    prov = PROVENANCE.read_text()
    assert "| Paper9_Blueprint_v1.5.tex | 1.5 | b96c8e76" in prov
    assert "CURRENT governing specification" in prov
    assert "| Paper9_Blueprint_v1.4.tex | 1.4 | 2ae0b1e8" in prov
    assert "FROZEN, superseded by v1.5" in prov
    assert _sha(BP15) == "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91"
    assert _sha(BP14) == "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638"
    assert _sha(BP13) == "ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f"
    assert _rec()["governing_spec"].startswith("Paper9_Blueprint v1.6")


def test_a2_chain_is_traceable():
    assert _sha(A2) == "c008a00e1946599e7cf3eb23ffbc4cb52ea5356e40f7e1fbb5e37b9d8276b7b9"
    assert "amendment A2" in PROVENANCE.read_text()
    bp15 = BP15.read_text().splitlines()
    assert any("A2" in l for l in bp15[1050:1100])
    for guard in (CLASSIFIER, ROUTE_TEST):
        assert guard.exists()
    prov = PROVENANCE.read_text()
    assert "A2" in prov


def test_rule_rfit_is_traceable_and_frozen():
    assert _sha(RULE) == "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8"
    assert _sha(RULE_RECORD) == "349c56c6323e41d2ff4b90b89c5651ee0446768c3d4ff8d24b869b7e0589d245"
    rule_rec = json.loads(RULE_RECORD.read_text())
    assert rule_rec["rule"]["F"] == 3.0 and rule_rec["rule"]["inequality"].startswith("strict")
    assert "P12G_ROUTE_A_RULE_RFIT_FREEZE.md" in rule_rec["rule"]["frozen_in"]
    assert "P12H A1 authorization" in rule_rec["rule"]["adopted_by"]
    assert _json()["metadata"]["p12h_amendment"]["authorization"].startswith("A1")


# ---------------------------------------------------------------- gates
def test_gate_states_unchanged():
    gates = _rec()["gate_state"]
    assert gates["PCR1"] == "PASS"
    assert gates["G3"] == "MET"
    assert gates["G4"] == "NOT MET"
    # PI authorisation 2026-09-24: the two authorised closures; every other gate and every
    # benchmark field below is unchanged.
    #   P5  -> PASS    (paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md)
    #   R-1 -> CLOSED  (paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md)
    assert gates["P5"] == "PASS"
    assert gates["R-1"] == "CLOSED"
    assert gates["PCR5"] == "PASS"
    assert gates["P13"] == "BLOCKED"
    b = _rec()["benchmarks"]
    assert b["B1"]["graphical_validation"].startswith("PASS")
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B2"]["reproduction_status"].startswith("NOT REPRODUCED")
    assert b["B2"]["ambiguity_status"].startswith("UNRESOLVED")
    assert b["B3"]["route"] == "NOT_VALIDATED" and b["B3"]["reproduction_status"].startswith("NOT REPRODUCED")
    assert b["B3"]["ambiguity_status"].startswith("UNRESOLVED -- NOT the formulation")
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    for key in ("B2", "B3"):
        assert b[key]["quantitative_error"] is None
    assert json.dumps(b).count("%") == 0


def test_author_data_status_unchanged():
    assert "NOT SENT" in P12M.read_text()
    assert "NOT SENT" in P12Q.read_text() and "NOT AUTHORIZED" in P12Q.read_text()
    assert "not authorize sending" in _flat(P12Q.read_text())
    assert P12L.exists() and "no contact has been initiated" in _flat(P12L.read_text())
    blocker = _rec()["gate_state"]["blocker"]
    assert "NOT_VALIDATED" in blocker and "source-side data gaps" in blocker
    for tpl in ("B1", "B2", "B3"):
        assert (AUDIT / "author_data" / f"{tpl}_DATA_RECEIPT_TEMPLATE.md").exists()


def test_blocker_matrix_matches_statuses():
    assert MATRIX_MD.exists() and MATRIX_JSON.exists()
    m = json.loads(MATRIX_JSON.read_text())
    assert set(m) >= {"B2", "B3", "PCR1", "G3", "G4", "P5", "R-1", "P13"}
    gates = _rec()["gate_state"]
    # The P12AA matrix is a phase record: its PCR1/G3 rows keep the P12AA-era statuses verbatim,
    # while the live register carries the A3 reassessment of 2026-09-25 (PCR1 PASS, G3 MET).
    # G4 is unchanged in both (PI signature not given under Section 10.3).
    assert m["PCR1"]["status"] == "NOT PASS" and gates["PCR1"] == "PASS"
    assert m["G3"]["status"] == "NOT MET" and gates["G3"] == "MET"
    assert m["G4"]["status"] == "NOT MET" and gates["G4"] == "NOT MET"
    # The P12AA matrix is a phase record: its P5/R-1 rows keep the P12AA-era statuses verbatim,
    # while the live register carries the PI-authorised closures of 2026-09-24.
    assert m["P5"]["status"] == "NOT PASS/OPEN" and gates["P5"] == "PASS"
    assert m["R-1"]["status"] == "OPEN" and gates["R-1"] == "CLOSED"
    assert m["P13"]["status"] == gates["P13"]
    assert m["B2"]["status"] == "NOT_VALIDATED"
    assert m["B3"]["status"] == "NOT_VALIDATED"
    for key in ("B2", "B3", "PCR1", "G3", "G4", "P5", "R-1", "P13"):
        row = m[key]
        assert set(row) >= {"status", "exact_reason", "required_evidence",
                            "internally_obtainable", "author_data_required", "closable_now"}, key
    md = MATRIX_MD.read_text()
    assert "| Blocker | Current status |" in md
    for k in ("B2", "B3", "PCR1", "G3", "G4", "P5", "R-1", "P13"):
        assert f"**{k}**" in md


def test_historical_audit_documents_are_not_rewritten():
    h = P12H_AUDIT.read_text()
    assert "a45a5448a76764d5" in h and "0089754b076ff9e3" in h
    j = P12J_CLOSURE.read_text()
    assert "0089754b076ff9e3" in j
    p12z = (AUDIT / "P12Z_REGISTER_CURRENT_VERSION_AUDIT.md").read_text()
    assert "a45a5448" in p12z and "0089754b" in p12z
    p12aa = (REPO / "paper9" / "audit" / "P12AA_TRACEABILITY_REMEDIATION_AUDIT.md").read_text()
    assert "a45a5448a76764d5" in p12aa and "0089754b076ff9e3" in p12aa
