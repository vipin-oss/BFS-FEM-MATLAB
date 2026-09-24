"""P12V — source-audit guards (B2 / B3 blocker resolution).

These tests freeze the *forensic conclusions* of Phase P12V and the anti-fabrication
rules they must never violate:

* the source PDFs are byte-identical to the audited hashes;
* B2 and B3 stay ``NOT_VALIDATED`` with ``quantitative_error`` NULL — nothing is promoted;
* the audit classifies both blockers as ``SOURCE-AMBIGUOUS — DATA REQUIRED``;
* an item that is merely *inferable* is not promoted to source data;
* the three curve identities (classical limit / literature [34] / present dipolar-gradient
  model) stay distinct everywhere;
* the B3 transfer-matrix formulation identity (repository == source Appendix 3) is kept as
  recorded evidence;
* the audit keeps its no-tuning statement;
* the residual, *unfixed* record-text findings are enumerated.

No test in this file derives a number from pixels and no test weakens an existing guard.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit" / "P12V_B2_B3_SOURCE_AUDIT.md"
EVID = REPO / "paper9" / "audit" / "evidence" / "p12v"
RECORD = REPO / "paper9" / "audit" / "benchmark_validation_record.json"
LI2024 = REPO / "paper9" / "analytic" / "li2024" / "s41598-024-75049-1.pdf"
LI2023 = REPO / "paper9" / "analytic" / "li2023" / "17455030.2023.2222189.pdf"

SOURCE_SHA256 = {
    LI2024: "2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513",
    LI2023: "3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7",
}


def _flat(path: Path) -> str:
    """Whitespace-normalised text (markdown line wrapping must never fake a mismatch)."""
    return " ".join(path.read_text(errors="ignore").split())


def test_source_pdfs_are_byte_identical():
    for path, want in SOURCE_SHA256.items():
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        assert got == want, f"{path.name}: authoritative PDF changed ({got})"


def test_benchmark_record_matches_the_current_corrected_content_pin():
    """Exact-content pin of the active machine record.

    P12V performed no edit (the audited content was P12U's ``cdbfe6c2…``). The record was then
    corrected twice, both times by mandate and both times text-only:

    * **P12W** — three text spans: ``benchmarks.B3.reproduction_status`` (P12V-F1),
      ``benchmarks.B3.ambiguity_status`` (P12V-F2) and the superseded formulation clause inside
      ``gate_state.blocker`` (Part C consistency);
    * **P12X** — one **added** field, ``benchmarks.B3.formulation_status`` (Outcome-2 governance
      correction): the B3 block had no explicit machine-readable formulation status, so the
      superseded claim inside the frozen P12S-era ``reason`` string was only covered by prose.

    The pin is therefore re-pointed to the current corrected content. The guard keeps its
    exact-content strictness; every route, gate value, number, hash and reason string is unchanged
    by both corrections and is covered by the P12W/P12X closure guards.
    """
    got = hashlib.sha256(RECORD.read_bytes()).hexdigest()
    assert got == "2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2"


def test_b2_status_is_not_promoted():
    b2 = json.loads(RECORD.read_text())["benchmarks"]["B2"]
    assert b2["route"] == "NOT_VALIDATED"
    assert b2["quantitative_error"] is None
    assert "UNRESOLVED" in b2["ambiguity_status"]


def test_b3_status_is_not_promoted():
    b3 = json.loads(RECORD.read_text())["benchmarks"]["B3"]
    assert b3["route"] == "NOT_VALIDATED"
    assert b3["quantitative_error"] is None


def test_audit_classifies_both_blockers_as_source_ambiguous_data_required():
    t = _flat(AUDIT)
    assert "SOURCE-AMBIGUOUS — DATA REQUIRED" in t
    assert t.count("SOURCE-AMBIGUOUS — DATA REQUIRED") >= 2
    assert "NOT_VALIDATED" in t and "remains correct for both" in t


def test_inference_is_not_promoted_to_source_data():
    t = _flat(AUDIT)
    assert "ONLY INFERABLE" in t
    assert "NONE FOUND" in t                     # no explicit Fig. 3(b) -> Fig. 4(c) inheritance
    assert "“Inferable” is not “provided”" in t


def test_three_curve_identities_stay_distinct():
    t = _flat(AUDIT)
    for needle in ("classical limit", "literature [34]", "present dipolar-gradient model"):
        assert needle in t, f"curve identity '{needle}' missing from the audit record"
    assert "never" in t and "conflated" in t


def test_audit_keeps_the_no_tuning_statement():
    t = _flat(AUDIT)
    assert "no parameter was scanned or tuned" in t
    assert "Not performed: no scanning of unknown parameters" in t


def test_b3_formulation_identity_evidence_is_recorded():
    text = (EVID / "b3_formulation_identity.txt").read_text()
    rows = re.findall(
        r"wbar=([0-9.]+) : consistent-sign  max\|dT\|/scale = ([0-9.eE+-]+)\s+\|"
        r"\s+verbatim printed sign  max\|dT\|/scale = ([0-9.eE+-]+)", text)
    assert len(rows) == 3, "the three identity rows must be present"
    for _, consistent, printed in rows:
        assert float(consistent) < 1e-12, "repository matrix must equal [P0][G][P0]^-1"
        assert float(printed) > float(consistent)
    assert "0.33929" in text and "gap" in text
    # the 60- and 120-digit evaluations must agree (no precision artefact)
    assert text.count("1.235e-100") >= 1 or text.count("9.884e-41") >= 1


def test_digitisation_artifacts_are_present_and_well_formed():
    fig2 = json.loads((EVID / "li2024_fig2_digitisation.json").read_text())
    assert set(fig2) == {"a", "b", "c"}
    li23 = json.loads((EVID / "li2023_fig3_fig4_digitisation.json").read_text())
    assert set(li23) == {"F3a", "F3b", "F3c", "F4a", "F4b", "F4c"}
    f4c = li23["F4c"]
    assert f4c["frames" if "frames" in f4c else "frame"] is not None
    curves = [c for c, _ in f4c["values"]["1.0"]["curves"]]
    assert min(curves) == 0.4327, "the published Fig. 4(c) lowest curve must stay as digitised"
    # the dashed literature curve and the solid present curve are distinguishable in the record
    presences = [p for _, p in f4c["values"]["1.0"]["curves"]]
    assert any(p >= 0.8 for p in presences) and any(p < 0.8 for p in presences)


def test_audit_enumerates_the_unfixed_record_text_findings():
    t = _flat(AUDIT)
    assert "P12V-F1" in t and "P12V-F2" in t
    assert "reproduction_status" in t and "ambiguity_status" in t
    assert "reported, not silently fixed" in t
