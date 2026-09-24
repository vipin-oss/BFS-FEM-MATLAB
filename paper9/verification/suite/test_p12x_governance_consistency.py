#!/usr/bin/env python3
"""P12X — final governance / gate-state consistency guards.

The P12W correction closed the two P12V text findings. P12X asks the governance question that
follows: does the *active* repository state — machine record, evidence registry, gate mapping,
author-data chain, manuscript — consistently say

* B1 = ``GRAPHICAL_VALIDATION`` / PASS;
* B2 = ``NOT_VALIDATED`` (source ``l``/``l̄`` ambiguity unresolved);
* B3 = ``NOT_VALIDATED`` because the source's Fig. 4(c) parameter set / normalisation / curve data
  are missing, **with the formulation itself established as source-equivalent**;
* PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS · P13 BLOCKED,

and that nothing operative claims B3's formulation is unresolved? These guards cover every required
assertion of the phase plus the conflation rules that must never regress.

Active records are the non-phase-stamped governance artifacts; phase-stamped P12S/P12T/P12U/P12V
audit documents are historical records and are asserted to keep their historical wording (they are
deliberately *not* rewritten).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit"
RECORD = AUDIT / "benchmark_validation_record.json"
EVIDENCE = AUDIT / "benchmark_evidence.json"
PCR_MAP = AUDIT / "P11D_PCR_MAPPING.md"
RAW = AUDIT / "evidence" / "p12s" / "p12s_validation_record.json"
# historical (frozen) audit records
P12V_AUDIT = AUDIT / "P12V_B2_B3_SOURCE_AUDIT.md"
P12T_AUDIT = AUDIT / "P12T_INDEPENDENT_AUDIT.md"
# live governance / author-data chain
P12L_SPEC = AUDIT / "P12L_AUTHOR_DATA_REQUEST_SPEC.md"
P12M_DRAFT = AUDIT / "P12M_AUTHOR_REQUEST_DRAFTS.md"
P12N = AUDIT / "P12N_AUTHOR_DATA_HANDOFF.md"
P12O = AUDIT / "P12O_AUTHOR_DATA_BLOCKER_DECISION.md"
P12P = AUDIT / "P12P_ACTION_GATE.md"
P12Q = AUDIT / "P12Q_PI_DECISION_HANDOFF.md"
A2_AMEND = AUDIT / "BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md"
TM_JSON = AUDIT / "traceability_matrix.json"
TM_CSV = AUDIT / "traceability_matrix.csv"
P5_STATUS = AUDIT / "P5_STATUS.md"
# frozen anchors
BLUEPRINT_V15 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex"
RULE_RFIT = REPO / "paper9" / "verification" / "suite" / "rule_rfit.py"
P12U_GUARDS = REPO / "paper9" / "verification" / "suite" / "test_p12u_correction_closure.py"

FROZEN = {
    BLUEPRINT_V15: "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    RULE_RFIT: "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
    RAW: "cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21",
    P12M_DRAFT: "2f68e66fa82dbf8b18420d9da33c34cb726d47433c7ce1875c5a19c8267cec61",
    P12L_SPEC: "8acb70f1fccdb93cb910a6365e0ca4cb688eb1636d1a923f81c88d3a2168fc89",
}

# Manuscript: sha256 over (per-file hashes) of every .tex under paper9/latex (sorted paths).
MANUSCRIPT_TEX_SET_SHA256 = "243bb4d3d3d1ce5235e2d8d52bf6a095f8440b9d6accf4407dd640dedf35450e"  # re-pointed by P12AG (2026-09-24): build repair added \usepackage{ragged2e} to ms.tex;
  # the P12AF re-tiering of sec05_verification.tex and tab03_anchor_errors.tex is unchanged.

# ACTIVE records that must not contain superseded B3-formulation wording.
ACTIVE_RECORDS = (RECORD, EVIDENCE, PCR_MAP, P12L_SPEC, P12M_DRAFT, P12N, P12O, P12P, P12Q,
                  A2_AMEND, TM_JSON, TM_CSV, P5_STATUS)
# The active record carries ONE frozen, byte-pinned P12S-era string — `benchmarks.B3.reason`, the
# corrected script output, which P12U pins equal to the raw run record and P12W/P12X may not rewrite
# (Part G: raw P12U records are immutable; no existing guard may be weakened). Its superseded clause
# is therefore retired at field level by `formulation_status` / `ambiguity_status` instead of edited;
# the stale-wording scan below excludes exactly that one string and pins it separately.
FROZEN_REASON_FIELD = ("benchmarks", "B3", "reason")
STALE_FORMS = (
    "unverifiable formulation",
    "formulation not verified",
    "formulation cannot be reconstructed",
    "formulation not reconstructable",
    "NOT RECONSTRUCTABLE",
    "SOURCE_UNAVAILABLE",
    "not pinned down",
    "formulation ambiguity",
)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _rec() -> dict:
    return json.loads(RECORD.read_text())


def _flat(p: Path) -> str:
    return " ".join(p.read_text(errors="ignore").split())


def _fs(s: str) -> str:
    """Whitespace-normalised *string* (for record fields; markdown may wrap, values may not)."""
    return " ".join(s.split())


def _manuscript_set_hash() -> str:
    names = sorted(str(q) for q in (REPO / "paper9" / "latex").rglob("*.tex"))
    return hashlib.sha256("".join(hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names).encode()).hexdigest()


# ------------------------------------------------------------------ 1-3. benchmark statuses
def test_b1_status_is_graphical_validation_pass():
    b1 = _rec()["benchmarks"]["B1"]
    assert b1["route"] == "GRAPHICAL_VALIDATION"
    assert b1["graphical_validation"] == "PASS"
    assert b1["quantitative_error"] is None


def test_b2_status_is_not_validated_with_unresolved_source_ambiguity():
    b2 = _rec()["benchmarks"]["B2"]
    assert b2["route"] == "NOT_VALIDATED"
    assert b2["graphical_validation"] == "NOT_APPLICABLE"
    assert b2["ambiguity_status"].startswith("UNRESOLVED")


def test_b3_status_is_not_validated():
    b3 = _rec()["benchmarks"]["B3"]
    assert b3["route"] == "NOT_VALIDATED"
    assert b3["graphical_validation"] == "NOT_APPLICABLE"


# ------------------------------------------------------------------ 4. formulation status field
def test_b3_formulation_status_field_is_established_source_equivalent():
    fs = _fs(_rec()["benchmarks"]["B3"]["formulation_status"])
    assert fs.startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    assert "Appendix 3" in fs and "[P0][G][P0]^-1" in fs
    assert "1e-16" in fs and "60 digits" in fs
    assert "omega_bar = 0.3391" in fs and "omega_bar = 1.021" in fs
    assert "source-side, not an implementation-formulation defect" in fs
    # the superseded attribution is explicitly retired at field level
    assert "SUPERSEDED" in fs and "not operative" in fs
    # and the residual blocker is the missing Fig. 4(c) configuration, not the formulation
    assert "parameter set/normalisation and curve data" in fs
    assert "no Fig. 3(b) inheritance taken as authoritative" in fs


def test_b3_formulation_established_is_not_a_validation_pass():
    """Part C: formulation status and validation status must not be conflated."""
    b3 = _rec()["benchmarks"]["B3"]
    assert b3["route"] == "NOT_VALIDATED"
    assert "PASS" not in b3["formulation_status"]
    assert b3["ambiguity_status"].startswith("UNRESOLVED")
    assert "NOT the formulation" in b3["ambiguity_status"]
    assert "NOT_VALIDATED" in b3["ambiguity_status"]


# ------------------------------------------------------------------ 5-7. null quantitative errors
def test_b3_quantitative_error_is_null_and_no_percentage_claimed():
    b3 = _rec()["benchmarks"]["B3"]
    assert b3["quantitative_error"] is None
    assert b3["quantitative_error_reason"] == "no machine-readable numerical values published"
    assert "%" not in json.dumps(b3), "no percentage error may be claimed for B3"


def test_b2_quantitative_error_is_null_and_no_percentage_claimed():
    b2 = _rec()["benchmarks"]["B2"]
    assert b2["quantitative_error"] is None
    assert "%" not in json.dumps(b2)


# ------------------------------------------------------------------ 8. the seven gate states
GATES = {"PCR1": "NOT PASS", "G3": "NOT MET", "G4": "NOT MET", "P5": "NOT PASS/OPEN",
         "R-1": "OPEN", "PCR5": "PASS", "P13": "BLOCKED"}


def test_gate_state_record_is_exactly_the_frozen_set():
    g = _rec()["gate_state"]
    for k, v in GATES.items():
        assert g[k] == v, f"{k}: {g[k]!r} != {v!r}"
    assert "remain NOT_VALIDATED" in g["blocker"]
    assert "gate definitions unchanged" in g["blocker"]
    assert "unverifiable formulation" not in g["blocker"]


def test_gate_states_agree_across_the_active_governance_records():
    # P11D gate mapping (PCR1/PCR6/PCR7 partial; G3/G4 not met)
    t = _flat(PCR_MAP)
    assert "**NOT MET** — external ≤2% relative error is not computable" in t or "NOT MET" in t
    assert "G3 (external quantitative ≤2%)" in t and "**NOT MET**" in t
    assert "G4 cannot be PASS while mandatory requirements are unmet" in t
    # live author-data chain: full gate table repeated in four records
    for p in (P12N, P12O, P12P, P12Q):
        s = _flat(p)
        for k, v in GATES.items():
            if k == "P5":
                assert "P5 = NOT PASS / OPEN" in s or "**P5** | **NOT PASS / OPEN**" in s or "P5 = NOT PASS / OPEN." in s, p.name
            elif k == "R-1":
                assert "R-1 = OPEN" in s or "**R-1** | **OPEN**" in s or "R-1 = OPEN." in s, p.name
            elif k == "PCR5":
                assert "PCR5 = PASS" in s or "**PCR5** | **PASS**" in s, p.name
            elif k == "P13":
                assert "P13" in s and "BLOCKED" in s, p.name
            else:
                assert f"{k} = {v}" in s or f"**{k}** | **{v}**" in s, f"{p.name}: {k}"
    # the A2 amendment record keeps the benchmark nulls and R-1 open
    a = _flat(A2_AMEND)
    assert "B1/B2/B3 `quantitative_error` | NULL | **NULL** (unchanged)" in a
    assert "R-1 | OPEN | **OPEN** (unchanged)" in a


def test_no_active_record_claims_a_promoted_gate():
    forbidden = ("PCR1: PASS", "G3: MET", "G4: MET", "P5: PASS", "R-1: CLOSED", "P13: UNBLOCKED",
                 "PCR1 = PASS", "G3 = MET", "G4 = MET", "P5 = PASS", "R-1 = CLOSED", "P13 = UNBLOCKED")
    for p in ACTIVE_RECORDS:
        s = p.read_text(errors="ignore")
        for f in forbidden:
            assert f not in s, f"{p.name}: promoted-gate claim {f!r}"


# ------------------------------------------------------------------ 9-10. stale-wording search
def test_no_active_record_contains_stale_formulation_unresolved_wording():
    """Every active record scanned in full — except the machine record itself, whose single frozen
    P12S-era ``reason`` string necessarily retains the historical clause (checked in the test below);
    the record's *operative* fields are scanned by the next test."""
    for p in ACTIVE_RECORDS:
        if p is RECORD:
            continue
        s = p.read_text(errors="ignore")
        for f in STALE_FORMS:
            assert f not in s, f"{p.name}: stale B3-formulation wording {f!r} still active"


def test_active_record_operative_fields_carry_no_stale_formulation_wording():
    b3 = {k: v for k, v in _rec()["benchmarks"]["B3"].items() if k != "reason"}
    # also scan the other benchmarks and the gate block for the formulation-attribution forms
    rest = {"B1": _rec()["benchmarks"]["B1"], "B2": _rec()["benchmarks"]["B2"],
            "B3(operative)": b3, "gate_state": _rec()["gate_state"]}
    for name, block in rest.items():
        s = json.dumps(block)
        for f in STALE_FORMS:
            assert f not in s, f"active {name}: stale B3-formulation wording {f!r} still operative"


def test_the_only_stale_clause_left_is_the_frozen_reason_string_and_it_is_retired():
    b3 = _rec()["benchmarks"]["B3"]
    raw = json.loads(RAW.read_text())["benchmarks"]["B3"]["reason"]
    assert b3["reason"] == raw, "frozen P12S-era reason string must stay byte-identical to the raw record"
    assert "SOURCE_UNAVAILABLE item" in b3["reason"], "historical clause must be preserved, not deleted"
    fs = _fs(b3["formulation_status"])
    assert "SUPERSEDED" in fs and "not operative" in fs
    assert "frozen P12S-era 'reason' string" in fs
    assert "not the operative status" in _fs(b3["ambiguity_status"])


def test_historical_p12v_and_p12t_wording_is_preserved_not_rewritten():
    """The historical audit records must stay historically accurate (Part B classification B)."""
    v = _flat(P12V_AUDIT)
    assert "P12V-F1" in v and "P12V-F2" in v
    assert "source's own 0.50" in v                       # the defect as it was found
    assert "dipolar-gradient formulation/coefficient convention not pinned down" in v
    assert "reported, not silently fixed" in v
    t = _flat(P12T_AUDIT)
    assert "SOURCE_UNAVAILABLE" in t                       # P12T's own state-of-the-art wording
    # and none of that is operative: the active record says the legacy clause is superseded
    fs = _fs(_rec()["benchmarks"]["B3"]["formulation_status"])
    assert "frozen P12S-era 'reason' string" in fs and "not operative" in fs


def test_frozen_reason_string_still_equals_the_raw_run_record():
    """The P12U byte-identity surface is intact (P12X did not rewrite frozen evidence)."""
    assert _sha(RAW) == FROZEN[RAW]
    rec = _rec()["benchmarks"]["B3"]["reason"]
    raw = json.loads(RAW.read_text())["benchmarks"]["B3"]["reason"]
    assert rec == raw
    assert "0.436" in rec and "0.500" in rec


def test_no_fig3b_inheritance_is_treated_as_authoritative():
    b3 = _rec()["benchmarks"]["B3"]
    assert "inheritance is inferred from the case definition" in b3["parameter_provenance"]
    assert "Fig. 4(c) caption itself states no values" in b3["parameter_provenance"]
    assert b3["parameter_completeness"] == "COMPLETE for the classical data; gradient conversion not verifiable"
    src = json.loads(EVIDENCE.read_text())["benchmarks"]["B3"]["parameter_source"]
    assert "provenance [S] (inherited), never [C]" in src
    assert "annotates NO c_bar/d_bar values" in src


def test_b2_reason_is_structural_and_source_based():
    b2 = _rec()["benchmarks"]["B2"]
    r = _fs(b2["reason"])
    assert "bare unlabelled 'l = 1e-5'" in r
    assert "Eq. 55 defines l_bar = l/b" in r
    assert "coincides with the classical panel and contradicts the published panel (b)" in r
    assert "No interpretation is selected" in r
    assert b2["reproduction_status"] == "NOT REPRODUCED under any admissible interpretation"
    assert b2["branch_observables"] == "not compared (no admissible reproduction to compare)"
    assert b2["parameter_completeness"].startswith("INCOMPLETE")


def test_b3_three_curve_quantities_stay_distinct():
    st = _fs(_rec()["benchmarks"]["B3"]["reproduction_status"])
    assert "0.3391" in st                       # reproduced, source-formulation-equivalent
    assert "0.433-0.436" in st                  # published solid "Present" gradient curve
    assert "0.500" in st and "~0.50" in st      # classical limit / dashed literature [34]
    assert "NOT the source's Present gradient value" in st


# ------------------------------------------------------------------ 11. author-data logic
def test_author_requests_are_drafts_only_not_sent():
    for p in (P12N, P12O, P12P):
        assert "NOT SENT" in _flat(p), p.name
    q = _flat(P12Q)
    assert "NOT AUTHORIZED / NOT SENT" in q
    assert "awaiting explicit PI authorization to SEND" in q
    # drafts and spec byte-identical (never altered)
    assert _sha(P12M_DRAFT) == FROZEN[P12M_DRAFT]
    assert _sha(P12L_SPEC) == FROZEN[P12L_SPEC]
    # no author data has arrived
    assert "No author" in _flat(P12O) or "no author" in _flat(P12O)


def test_author_data_requirements_match_the_operative_blockers():
    s = _flat(P12L_SPEC)
    # B2: dimensional vs barred l + the geometry/parameter set actually used
    assert "length-scale parameterisation" in s and "this is the blocking question" in s
    assert "dimensional** $l$ (unit: m) or the **normalised**" in s
    assert "normalising length for this figure" in s
    # B3: parameter set / normalisation / curve data for Fig. 4(c)
    assert "underlying the Fig. 4(c) curves" in s
    assert "non-dimensional coefficients** actually used for the panel" in s
    assert "definitions of $\\bar c$ and $\\bar d$" in s


# ------------------------------------------------------------------ 12. immutability anchors
def test_blueprint_rule_and_frozen_records_are_unchanged():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"


def test_p12u_closure_guard_file_is_unchanged():
    """The P12U reason-equality guard must survive every later phase byte-identical."""
    assert _sha(P12U_GUARDS) == "cc56f3b8c0d4ee8841d7462dc0c66649c55115620fe3a44dfade8b470cfefea8"
    s = P12U_GUARDS.read_text()
    assert 'assert rec["benchmarks"]["B3"]["reason"] == raw["benchmarks"]["B3"]["reason"]' in s


def test_p5_gate_record_stays_unadopted_not_pass():
    """P5_STATUS.md is an active gate record: the contested P5 claim is not adopted as PASS."""
    s = _flat(P5_STATUS)
    assert "Branch-level P5 gate: CONTESTED" in s
    assert "neither gate claim is" in s and "adopted here" in s
    assert _rec()["gate_state"]["P5"] == "NOT PASS/OPEN"


def test_manuscript_tex_set_is_unchanged():
    assert _manuscript_set_hash() == MANUSCRIPT_TEX_SET_SHA256


def test_manuscript_states_the_same_b3_scope():
    """P12AF re-tiering: B1 gains the labelled graphical route, B2/B3 stay not validated."""
    t = _flat(REPO / "paper9" / "latex" / "sections" / "sec05_verification.tex")
    assert "must not be described as author-specified Fig.~4(c) parameters" in t
    assert r"classified \textsc{Graphical Validation}" in t          # B1 under A2
    assert r"Benchmark B3 is \textsc{Not Validated}" in t            # B3 not validated
    assert r"Benchmark B2 is \textsc{Not Validated} under the A2 routes" in t
    assert "GRAPHICAL ONLY / PARTIAL" not in t                       # superseded tier is gone
    assert "Gate~G3 remains formally NOT MET" in t
    # B2 ambiguity is declared unresolved, not resolved by graphical closeness
    assert "the ambiguity is preserved rather than resolved" in t
    # no percentage may be attached to any benchmark
    assert "No numerical agreement value and no error percentage is claimed" in t
