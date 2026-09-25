#!/usr/bin/env python3
"""P12AC guards — Decision B, candidate classification, retraction and frozen invariants.

These guards protect the *governance* outcome of the final literature-resolution
pass (P12AC): B2/B3 stay source-limited and NOT_VALIDATED, the search for a
published replacement is closed permanently, the earlier "Appendix 3 mismatch"
claim stays retracted, and nothing frozen moved.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AUDIT = REPO / "paper9" / "audit"
RECORD = AUDIT / "P12AC_LITERATURE_RESOLUTION_DECISION_B.md"
EVIDENCE = AUDIT / "evidence" / "p12ac" / "lwz_tm_equivalence_results.json"
EVIDENCE_PY = AUDIT / "evidence" / "p12ac" / "lwz_tm_equivalence_check.py"

FROZEN = {
    "paper9/plan/blueprint/Paper9_Blueprint_v1.5.tex":
        "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    "paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex":
        "2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638",
    "paper9/audit/benchmark_validation_record.json":
        "44593c1a6b382691860062e1dcb87f41b051e77da02d99969ee0a71533a46fea",
    "paper9/audit/traceability_matrix.csv":
        "8d86528fde59b84fd30d7d8402b6d701d9311950bc2726e6a5e5eecc1eca8201",
    "paper9/audit/traceability_matrix.json":
        "83ff8723b0abd329c307c03772494cf9b9c93f7967be39c5d49ce31512934013",
    "paper9/verification/suite/rule_rfit.py":
        "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
}

PDFS = {
    "paper9/analytic/li2024/s41598-024-75049-1.pdf":
        "2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513",
    "paper9/analytic/li2023/17455030.2023.2222189.pdf":
        "3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7",
    "paper9/analytic/lwz2016/li2015.pdf":
        "88115557af9e9fb46c5f1bd64fdc023f1e6ca45a01257404d6115a6afc0cb48e",
    "paper9/analytic/pb2009/papargyri-beskou2009.pdf":
        "8ca9c8208d5fbe4a24fa954be641c98eba95bfdb97f9fc17e1a227479c3a8ddb",
}

DECISION_B = ("B2/B3 remain source-limited and NOT_VALIDATED because the published sources do not "
              "provide sufficient authoritative parameter/curve information")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _flat(path: Path) -> str:
    return " ".join(path.read_text().split())


def _rec() -> str:
    assert RECORD.exists(), "P12AC Decision B record is missing"
    return _flat(RECORD)


def _plain(path: Path) -> str:
    """Whitespace-flattened text with markdown emphasis removed."""
    return " ".join(re.sub(r"[*`>]", "", _flat(path)).split())


def _ev():
    assert EVIDENCE.exists(), "P12AC evidence JSON is missing"
    return json.loads(EVIDENCE.read_text())


def test_decision_b_record_states_the_decision():
    t = _plain(RECORD)
    assert DECISION_B in t
    assert "not a solver defect" in t.lower()
    assert "closed permanently" in t


def test_every_repository_held_candidate_is_classified():
    t = _rec()
    assert "SUPPORTING ONLY" in t
    # LWZ2016 is the SUPPORTING-ONLY candidate; each other held source is NOT COMPATIBLE
    for key in ("LWZ2016", "Li et al. 2024", "Li et al. 2023", "PB2009", "Mishra",
                "Zheng & Wei 2009", "Zhan & Wei 2010", "hosseini2021.pdf",
                "s10773-022-05163-1.pdf"):
        assert key in t, f"candidate {key} not classified in the record"
    assert t.count("NOT COMPATIBLE") >= 7
    assert "no admissible ACCEPTABLE replacement or augmentation exists" in t


def test_decision_b_does_not_move_any_gate():
    t = _rec().lower()
    for phrase in ("pcr1 therefore remains", "not pass"):
        assert phrase in t
    assert "g3" in t and "not met" in t
    assert "does not itself" in t and "authorise submission" in t


def test_retraction_of_the_earlier_appendix3_mismatch_is_recorded():
    t = _rec()
    assert "Retraction" in t
    assert "superseded" in t
    assert "3.6e-15" in t
    assert "96-member" in t
    assert "defective hand-reconstruction" in t


def test_path_forward_determinations_present():
    t = _rec()
    for key in ("PCR1", "P5", "R-1", "C-1", "P13", "limitation statement"):
        assert key in t
    assert "genuinely independent" in t
    assert "without lowering any gate" in t or "no gate lowered" in t


def test_evidence_bounds_and_band_edges():
    ev = _ev()
    assert ev["appendix3_vs_repo_max_over_points"] <= 1e-13
    assert ev["homogeneous_max_rel_residual"] <= 1e-12
    edges = ev["cell_band_edges_y"]
    for got, want in zip(edges, [0.6675, 0.6937, 1.2946]):
        assert abs(got - want) < 1e-3, (got, want)
    assert ev["fig3_digitised_grey_intervals_y"] == [[0.6036, 0.6627],
                                                     [0.8718, 1.1637],
                                                     [1.3136, 1.7120]]
    assert "no percentage error" in ev["fig3_digitisation_note"]
    assert ev["retracted_variant_sweep"]["best"]["max_abs_residual"] > 1e-3


def test_variant_family_is_bounded_and_layer_order_is_invariant():
    ev = _ev()
    v = ev["variant_edges_y"]
    assert len(v) == 6 and "V0_as_read" in v
    a = v["V0_as_read"]["edges_y"]
    b = v["V3_layers_swapped"]["edges_y"]
    assert a and b and max(abs(x - y) for x, y in zip(a, b)) < 1e-9
    # no source-conforming variant reproduces the digitised middle stop band
    dig = ev["fig3_digitised_grey_intervals_y"][1]
    for name in ("V0_as_read", "V1_c_ratio_reversed", "V2_d_ratio_reversed",
                 "V4_cbar_in_layer_units"):
        e = v[name]["edges_y"]
        gaps = [(e[i], e[i + 1]) for i in range(0, len(e) - 1, 2)]
        assert not any(abs(g[0] - dig[0]) < 0.01 and abs(g[1] - dig[1]) < 0.01
                       for g in gaps), f"{name} unexpectedly reproduces the digitised band"


def test_evidence_script_is_rerunnable_and_pins_the_solver():
    src = EVIDENCE_PY.read_text()
    assert "lwz_tm_sh_normal" in src
    assert "T_app3" in src and "T_fp" in src
    assert "no percentage error" in src


def test_frozen_governance_and_source_files_unchanged():
    for rel, want in FROZEN.items():
        p = REPO / rel
        assert p.exists(), f"missing frozen file {rel}"
        assert _sha(p) == want, f"frozen file changed: {rel}"
    for rel, want in PDFS.items():
        p = REPO / rel
        assert p.exists(), f"missing source PDF {rel}"
        assert _sha(p) == want, f"source PDF changed: {rel}"


# Files an authorised manuscript phase has edited relative to this commit: the P12AF re-tiering
# (sec05_verification.tex) and the P12AG build repair (ms.tex, package line only).
P12AF_AUTHORISED_MANUSCRIPT_FILES = {"paper9/latex/sections/sec05_verification.tex",
                                     "paper9/latex/ms.tex"}

# Manuscript paths an authorised later phase has edited relative to this commit: the P5 n = 16
# production repair (PI-authorised 2026-09-24) regenerates the production-dependent numbers in the
# abstract and Sections 1 and 5-9.  Anything outside this union is still an unauthorised change.
P5_MESH16_REPAIR_MANUSCRIPT_FILES = {"paper9/latex/ms.tex",
                                     "paper9/latex/sections/sec01_intro.tex",
                                     "paper9/latex/sections/sec04_fem.tex",
                                     "paper9/latex/sections/sec05_verification.tex",
                                     "paper9/latex/sections/sec06_results.tex",
                                     "paper9/latex/sections/sec07_steering.tex",
                                     "paper9/latex/sections/sec08_discussion.tex",
                                     "paper9/latex/sections/sec09_conclusions.tex"}
AUTHORISED_MANUSCRIPT_FILES = P12AF_AUTHORISED_MANUSCRIPT_FILES | P5_MESH16_REPAIR_MANUSCRIPT_FILES


def test_manuscript_and_solvers_untouched_by_this_phase():
    """git-based check; skipped when history is unavailable.

    P12AE recorded the PI grant and P12AF performs the scoped re-tiering, so the only manuscript path
    that may differ from HEAD is the P12AF-authorised file; anything else is an unauthorised change.
    """
    try:
        out = subprocess.run(["git", "diff", "--name-only", "HEAD", "--",
                              "paper9/latex", "paper9/validation"],
                             cwd=REPO, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        import pytest
        pytest.skip("git history unavailable")
    changed = {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}
    assert changed <= AUTHORISED_MANUSCRIPT_FILES, f"unauthorised changes: {sorted(changed)}"


def test_record_declares_what_did_not_change():
    t = _rec()
    assert "byte-unchanged" in t
    for tok in ("b96c8e76", "2ae0b1e8", "d4fed492", "2fad2d92", "8d86528f", "83ff8723", "5ba2c22e"):
        assert re.search(re.escape(tok), t), tok
    assert "NOT SENT" in t and "NOT AUTHORISED" in t
