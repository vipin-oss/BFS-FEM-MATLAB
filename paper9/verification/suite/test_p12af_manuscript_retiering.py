"""P12AF guards — the authorised (P12AE decision B) manuscript re-tiering.

The PI grant recorded in `P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md` authorises a scoped,
byte-minimal manuscript edit: the B1/B2/B3 limitation statement and the Blueprint-v1.5 (amendment A2)
re-tiering in `paper9/latex/sections/sec05_verification.tex` and `paper9/tables/out/tab03_anchor_errors.tex`.

These guards prove that (a) exactly those two files changed, (b) the changes are the authorised ones,
(c) every numerical result, classification-independent field, gate, Blueprint byte, Rule R-fit byte,
source PDF and author-request file is unchanged, and (d) no gate was promoted and no percentage was
introduced. The phase record is `paper9/audit/P12AF_MANUSCRIPT_RETIERING_RECORD.md`.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
LATEX = REPO / "paper9" / "latex"
SEC05 = LATEX / "sections" / "sec05_verification.tex"
TAB03 = REPO / "paper9" / "tables" / "out" / "tab03_anchor_errors.tex"
AUDIT = REPO / "paper9" / "audit"
P12AE = AUDIT / "P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md"
RECORD = AUDIT / "benchmark_validation_record.json"

# post-P12AF manuscript set hash (sha256 over the concatenated per-file sha256, sorted paths)
MANUSCRIPT_TEX_SET_SHA256 = "243bb4d3d3d1ce5235e2d8d52bf6a095f8440b9d6accf4407dd640dedf35450e"  # re-pointed by P12AG (ms.tex build repair)
MANUSCRIPT_TEX_SET_SHA256_PRE = "5ba2c22e7e7db2f51ef76f56a1539ff170eb01cd0302c55fa724f7be180ca24b"

# Step 1 of the phase records the PI grant in this audit record; step 2 is the scoped edit of exactly
# two files (P12AE decision B); the five legacy guards below are re-pointed because they pinned the
# pre-edit manuscript bytes. Nothing else may differ from HEAD.
AUTHORISED_DIFFS = {
    "paper9/audit/P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md",
    "paper9/latex/sections/sec05_verification.tex",
    "paper9/tables/out/tab03_anchor_errors.tex",
    "paper9/verification/suite/test_p12x_governance_consistency.py",
    "paper9/verification/suite/test_p12y_traceability_cleanup.py",
    "paper9/verification/suite/test_p12ac_decision_b.py",
    "paper9/verification/suite/test_p12ad_decision_record.py",
    "paper9/verification/suite/test_p12ae_authorisation_record.py",
    # the new P12AF guard file itself
    "paper9/verification/suite/test_p12af_manuscript_retiering.py",
    # P12AG build repair (no scientific content)
    "paper9/latex/ms.tex",
    "paper9/tables/gen/tab02_parameters.py",
    "paper9/tables/gen/tab05_gap_summary.py",
    "paper9/tables/gen/tab06_convergence_floor.py",
    "paper9/tables/out/tab02_parameters.tex",
    "paper9/tables/out/tab05_gap_summary.tex",
    "paper9/tables/out/tab06_convergence_floor.tex",
    "paper9/verification/suite/test_p12ag_clean_build.py",
    # P12AH (Table-2 generator reconciliation + Table-2 layout repair; no scientific change)
    "paper9/tables/gen/tab03_anchor_errors.py",
    "paper9/tables/out/tab03_anchor_errors.tex",
    "paper9/verification/suite/test_p12ag_clean_build.py",
    "paper9/verification/suite/test_p12ah_generator_and_layout.py",
}

# paths whose bytes the phase may not touch at all (checked by git, independently of the allowlist)
FORBIDDEN_PATHS = ("paper9/validation", "paper9/results", "paper9/plan", "paper9/sources",
                   "paper9/figures")

# the last commit before the authorised edit: the phase's diff is measured against this, so the guard
# holds both before and after the phase commit. A later authorised manuscript edit must extend
# AUTHORISED_DIFFS explicitly in that phase.
P12AF_PRE_WORK = "73c7cec3bb181cd50184423b83bb00d10cb429e3"

# P12AH gave the long identifiers zero-width break hints and a width-aware column specification; those are
# layout, so the Table-2 row checks strip them and are anchored on the commit the layout repair started from
# rather than on live HEAD (which moves when the phase's own commits land).
P12AH_ENTRY = "b45ea785cadfc0ae09ffcba0c0d11153c6144bd4"


def _strip_layout_hints(text: str) -> str:
    return text.replace(r"\hspace{0pt}", "")


def _tab_at_entry() -> str:
    try:
        out = subprocess.run(["git", "show", f"{P12AH_ENTRY}:paper9/tables/out/tab03_anchor_errors.tex"],
                             cwd=REPO, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git history unavailable")
    return _strip_layout_hints(out.stdout)

FROZEN = {
    AUDIT / "benchmark_validation_record.json":
        "2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2",
    AUDIT / "P5_STATUS.md":
        "1a410f228c117f3ada13557d643e1f1498a0f17881890f464e94e2e3f8489c8c",
    REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex":
        "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
    REPO / "paper9" / "verification" / "suite" / "rule_rfit.py":
        "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
    AUDIT / "P12L_AUTHOR_DATA_REQUEST_SPEC.md":
        "8acb70f1fccdb93cb910a6365e0ca4cb688eb1636d1a923f81c88d3a2168fc89",
    AUDIT / "P12M_AUTHOR_REQUEST_DRAFTS.md":
        "2f68e66fa82dbf8b18420d9da33c34cb726d47433c7ce1875c5a19c8267cec61",
    AUDIT / "P12Q_PI_DECISION_HANDOFF.md":
        "1f06035024b29aed39688a293a613fed9b0069c887d9e36a0cfbafb22e3e6a54",
}

SOURCE_PDFS = {
    "Band-gaps-of-thermoelastic-waves-in-1D-phononic-crystal-with-fractional-order-generalized (1).pdf":
        "3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7",
    "hosseini2021.pdf":
        "234c164d9fe5b0bf743a1e4807a58ab46038a0130152976e014ab0553ac667e8",
    "s00707-026-04680-y.pdf":
        "eaa9b5f443a90378aea5210a7292bb14238f8da32f4e17ac6ff2f42c5cc4bd5b",
    "s10773-022-05163-1.pdf":
        "7f4bbadc05b41e89e73341ba61b2849384b5889db96b87a87cf70a48643d839d",
    "s41598-024-75049-1.pdf":
        "2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513",
    "zhan2010.pdf":
        "47b7a4395fc2fbd3dac2b579a88cfe134311060208a55b7dc133fb1ec65062f1",
    "zheng2009.pdf":
        "8898cd59a103d3402a32c5d80ebd697860db566864b545666c3839d833493f32",
}

GATE_STATE = {
    "PCR1": "NOT PASS", "G3": "NOT MET", "G4": "NOT MET", "P5": "NOT PASS/OPEN",
    "R-1": "OPEN", "PCR5": "PASS", "P13": "BLOCKED",
}

FORBIDDEN_PROMOTION = (
    "G3 is met", "G3 now met", "G4 is met", "PCR1 PASS", "PCR1 is satisfied",
    "passed validation", "validation passed", "benchmark B3 is validated",
    "B3 has been validated", "cleared G4", "gate G3 satisfied",
)


def _sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _flat(p: Path) -> str:
    return " ".join(Path(p).read_text(errors="ignore").split())


def _doc() -> str:
    return _flat(SEC05)


def _tab() -> str:
    # P12AH inserted zero-width break opportunities inside the long underscore identifiers; strip them
    # so these content assertions are layout-independent.
    return TAB03.read_text(errors="ignore").replace(r"\hspace{0pt}", "")


def _manuscript_set_hash() -> str:
    names = sorted(str(q) for q in LATEX.rglob("*.tex"))
    return hashlib.sha256(
        "".join(hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names).encode()
    ).hexdigest()


def _git_show(path: str) -> str:
    try:
        out = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=REPO,
                             capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git history unavailable")
    return out.stdout


def _rows(text: str) -> dict[str, str]:
    rows = {}
    for ln in text.splitlines():
        m = re.match(r"\\textbf\{(B\d)\}", ln)
        if m:
            rows[m.group(1)] = ln
    return rows


def _numeric_math(row: str) -> list[str]:
    """Math tokens that carry a digit — the table's numerical content."""
    return [t for t in re.findall(r"\$[^$]*\$", row) if re.search(r"\d", t)]


# ------------------------------------------------------------------ scope of the change
def test_manuscript_set_hash_is_the_authorised_post_edit_value():
    assert _manuscript_set_hash() == MANUSCRIPT_TEX_SET_SHA256
    assert MANUSCRIPT_TEX_SET_SHA256 != MANUSCRIPT_TEX_SET_SHA256_PRE


def test_only_the_authorised_files_differ_from_head():
    """Production content (manuscript, tables, validation, results, plan, sources, figures, suite).

    `paper9/audit` is excluded from the diff scope: audit records legitimately change every phase (the
    P12AE grant recording and this phase's own record), and the sources/validation/results areas are
    guarded here precisely so that they cannot.
    """
    try:
        out = subprocess.run(["git", "diff", "--name-only", P12AF_PRE_WORK, "HEAD", "--",
                              "paper9/latex", "paper9/tables", "paper9/validation", "paper9/results",
                              "paper9/plan", "paper9/sources", "paper9/figures", "paper9/verification"],
                             cwd=REPO, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git history unavailable")
    changed = {ln.strip() for ln in out.splitlines() if ln.strip()}
    assert changed <= AUTHORISED_DIFFS, f"unauthorised changes: {sorted(changed - AUTHORISED_DIFFS)}"
    assert "paper9/latex/sections/sec05_verification.tex" in changed
    assert "paper9/tables/out/tab03_anchor_errors.tex" in changed
    for f in changed:
        assert not f.startswith(FORBIDDEN_PATHS), f"frozen path changed: {f}"


def test_guard_pins_were_repointed_not_removed():
    """Each manuscript pin moved to the authorised post-edit value; the old pin is gone."""
    for name in ("test_p12x_governance_consistency.py", "test_p12y_traceability_cleanup.py",
                 "test_p12ad_decision_record.py", "test_p12ae_authorisation_record.py"):
        t = (REPO / "paper9" / "verification" / "suite" / name).read_text()
        assert MANUSCRIPT_TEX_SET_SHA256 in t, f"{name} does not pin the post-edit hash"
        assert MANUSCRIPT_TEX_SET_SHA256_PRE not in t, f"{name} still pins the pre-edit hash"


# ------------------------------------------------------------------ table re-tiering
def test_tab03_b1_status_is_graphical_validation_pass():
    row = _rows(_tab())["B1"]
    assert r"\textbf{B1}" in row
    assert r"GRAPHICAL\_VALIDATION / PASS" in row
    assert r"GRAPH\_ONLY / EQN$^c$" in row          # ref-data-type cell preserved
    assert r"PARTIAL" not in row


def test_tab03_b3_status_is_not_validated_and_partial_is_gone():
    row = _rows(_tab())["B3"]
    assert r"NOT VALIDATED$^g$" in row
    assert r"GRAPH\_ONLY$^d$" in row                # ref-data-type cell preserved
    assert r"PARTIAL" not in row


def test_tab03_b2_and_b5_rows_are_byte_identical_to_the_pre_phase_state():
    head, cur = _rows(_tab_at_entry()), _rows(_tab())
    for b in ("B2", "B5"):
        assert cur[b] == head[b], f"{b} row changed: {cur[b]!r}"


def test_tab03_numerical_cells_are_unchanged():
    head, cur = _rows(_tab_at_entry()), _rows(_tab())
    for b in ("B1", "B2", "B3", "B5"):
        assert _numeric_math(cur[b]) == _numeric_math(head[b]), f"{b} numerical cells changed"


def test_tab03_footnotes_retiered_and_new_footnote_added():
    t = _tab()
    assert r"$^g$ B3 is NOT externally validated" in t
    assert "formulation-consistency finding, not a validation" in t
    assert "no percentage is asserted for any graphically compared benchmark" in t
    assert "under the labelled graphical route (A2)" in t
    assert r"$^e$ B2 is NOT externally validated" in t      # B2 footnote untouched
    assert "amendment A2" in t


def test_tab03_declares_no_percentage_for_any_benchmark():
    t = _tab()
    assert "no percentage is asserted for any graphically compared benchmark" in t
    assert not re.search(r"\d\s*\\?%", t)                   # no percentage value anywhere


# ------------------------------------------------------------------ sec05 re-tiering
def test_sec05_b1_is_graphical_validation_without_a_percentage():
    t = _doc()
    assert "validated under the Blueprint's labelled graphical route (v1.5 \\S13, amendment A2)" in t
    assert r"classified \textsc{Graphical Validation}" in t
    assert "no numerical percentage is asserted" in t


def test_sec05_b2_b3_are_not_validated():
    t = _doc()
    assert r"Benchmark B2 is \textsc{Not Validated} under the A2 routes" in t
    assert r"Benchmark B3 is \textsc{Not Validated}" in t
    assert "GRAPHICAL ONLY / PARTIAL" not in t
    assert r"explicitly \emph{not} a benchmark validation" in t


def test_sec05_limitation_paragraph_is_present_and_outside_the_enumerate():
    raw = SEC05.read_text()
    i = raw.find(r"\paragraph{External Benchmark Coverage.}")
    assert i > 0, "limitation paragraph missing"
    assert raw[:i].count(r"\begin{enumerate}") == raw[:i].count(r"\end{enumerate}")
    t = _doc()
    for phrase in ("could \\textbf{not} be quantitatively or authoritatively validated",
                   "insufficient to reproduce them independently",
                   "the corresponding verification gate is \\textbf{not} claimed as met",
                   "No numerical agreement value and no error percentage is claimed for any of the three benchmarks.",
                   "formulation-consistency check and \\textbf{not} a validation of the two benchmarks",
                   "not any deficiency of the present solver"):
        assert phrase in t, f"limitation element missing: {phrase!r}"


def test_sec05_evidence_declaration_keeps_g3_not_met():
    t = _doc()
    assert "Gate~G3 remains formally NOT MET" in t
    assert "Benchmark~B1 satisfies the graphical route" in t
    assert "Benchmarks~B2 and B3 remain \\textsc{Not Validated}" in t


def test_no_promotion_wording_in_the_edited_files():
    blob = (_doc() + " " + _tab()).lower()
    for bad in FORBIDDEN_PROMOTION:
        assert bad.lower() not in blob, f"promotion wording present: {bad!r}"


# ------------------------------------------------------------------ nothing else moved
def test_grant_is_recorded_as_an_internal_act():
    t = _flat(P12AE)
    assert "GRANTED — decisions A–F — recorded 2026-09-24" in t
    assert "In force from the recording date." in t
    assert "☐ PI wet/electronic signature (not supplied; not claimed)." in t


def test_benchmark_classifications_and_gate_state_unchanged():
    r = json.loads(RECORD.read_text())
    b = r["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B3"]["route"] == "NOT_VALIDATED"
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    assert [b[k]["quantitative_error"] for k in ("B1", "B2", "B3")] == [None, None, None]
    g = r["gate_state"]
    assert {k: g[k] for k in GATE_STATE} == GATE_STATE


def test_frozen_artifacts_sources_and_author_requests_unchanged():
    for p, want in FROZEN.items():
        assert _sha(p) == want, f"{p} changed"
    for name, want in SOURCE_PDFS.items():
        assert _sha(REPO / "paper9" / "sources" / name) == want, f"{name} changed"
