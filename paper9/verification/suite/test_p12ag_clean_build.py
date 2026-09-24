"""P12AG guards — the clean-build repair.

P12AG repaired mechanical LaTeX/build defects only: a missing package declaration in `ms.tex`, two
malformed `\\multicolumn` column specs in generated tables (fixed in the generators and regenerated),
and text-mode `_`/`^` escaping in one generated table. No scientific claim, numerical value, benchmark
status, gate, threshold or conclusion changed.

These guards pin (a) the repair itself, (b) that the generators — not hand edits — own the generated
output, (c) that the escaped content is character-for-character the content that was already written,
and (d) that the manuscript compiles from the repository with zero LaTeX errors.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
LATEX = REPO / "paper9" / "latex"
TABLES_OUT = REPO / "paper9" / "tables" / "out"
TABLES_GEN = REPO / "paper9" / "tables" / "gen"
AUDIT = REPO / "paper9" / "audit"

MS = LATEX / "ms.tex"
SEC05 = LATEX / "sections" / "sec05_verification.tex"
TAB03 = TABLES_OUT / "tab03_anchor_errors.tex"

# P12AF content must survive P12AG
# sec05 is still byte-identical. tab03 was later given a Table-2 layout correction (P12AH:
# tabularx column spec + zero-width break hints, no content change) - pinned here at its post-P12AH
# bytes; the P12AH guard proves the content is unchanged by undoing the layout edits.
P12AF_CONTENT = {
    SEC05: "bfd45dd077e7cc4c542fef3fb3d24f89e1c1ea7958bf5052a97fb86b36d507c1",
    TAB03: "8b7de407e8898a204855f1f59bf3d5e0bd38a55fc36dafe957a8cf23b3bb8b4e",
}
P12AF_CONTENT_TAB03_AS_P12AF_LEFT_IT = "77fd75844415869f0ce94c720af38b7370635b004640591f69ce42fa5de5c113"

REPAIRED_OUTPUTS = [TABLES_OUT / "tab02_parameters.tex",
                    TABLES_OUT / "tab05_gap_summary.tex",
                    TABLES_OUT / "tab06_convergence_floor.tex"]

# The numbers in each repaired table, pinned as a digest of the SORTED numeric-token multiset.
# Measured at repair time against the pre-repair revision: identical before and after the repair
# (tab02 347 tokens, tab05 112, tab06 58) — i.e. the repair changed no number and added none.
NUMERIC_TOKEN_SHA256 = {
    # re-pinned in P12AH: this digest previously included the digits of the column specification
    # (L{3.5cm} etc.), which the layout repair changed.  Content tokens are unchanged and are
    # proved so byte-for-byte by test_p12ah_generator_and_layout.py (undo -> pre-layout bytes).
    "tab02_parameters.tex": "c1c5eb93bc2ea911663d8890be79d816f90e89e29fa7b13451a3ac1c73fff17c",
    "tab05_gap_summary.tex": "75bb31b63597a360c100ea14ed5e6f6b4acccfac975343f88893c1d7f44cb445",
    "tab06_convergence_floor.tex": "192ffe3c9f6407cbcd2f3426c09dda034e4f7de175b93574f374c5f8cffca6eb",
}

# values that must remain present verbatim
PINNED_VALUES = {
    "tab06_convergence_floor.tex": ["1.164855389329", "4.17", "4.63e-11", "$[3.15, 5.20]$"],
    "tab05_gap_summary.tex": ["1.155", "1.343", "1.542", "3.946"],
    "tab02_parameters.tex": ["1138.4", "3576.4", "2.2422e6", "1.288e9"],
}

MALFORMED_MULTICOLUMN = "{@{l@{}}"


def _sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _text_mode_hits(line: str) -> int:
    """Count raw `_`/`^` outside `$...$` (Skips \\verb-like control sequences and braced args)."""
    NO_ESCAPE = {"label", "ref", "cite", "input", "includegraphics", "begin", "end", "texttt"}
    hits, i, n, in_math = 0, 0, len(line), False
    while i < n:
        ch = line[i]
        if ch == "\\" and i + 1 < n:
            m = re.match(r"\\([A-Za-z@]+)", line[i:])
            if m:
                name = m.group(1)
                i += len(m.group(0))
                if name in NO_ESCAPE:                     # copy the braced argument verbatim
                    while i < n and line[i] == " ":
                        i += 1
                    depth = 0
                    while i < n and (line[i] == "{" or depth > 0):
                        if line[i] == "{":
                            depth += 1
                        elif line[i] == "}":
                            depth -= 1
                        i += 1
            else:
                i += 2
            continue
        if ch == "$":
            in_math = not in_math
            i += 1
            continue
        if not in_math and ch in "_^":
            hits += 1
        i += 1
    return hits


def _numeric_tokens(text: str) -> list[str]:
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("%"))
    # P12AH added layout-only markup to three of these tables (column specification, font size,
    # column separation, zero-width break hints, wrapped note rows).  None of it carries content,
    # so it is removed here and the P12AG digests below stay exactly as first pinned.
    body = re.sub(r"\\setlength\{\\tabcolsep\}\{[0-9.]+pt\}", "", body)
    body = body.replace(r"\hspace{0pt}", "")
    body = body.replace(r"\dimexpr\textwidth-2\tabcolsep\relax", "")
    body = re.sub(r"\\begin\{tabularx?\}[^\n]*", "", body)
    return re.findall(r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", body)


# ------------------------------------------------------------------ the repairs themselves
def test_ms_tex_loads_ragged2e_for_the_column_types_it_uses():
    t = MS.read_text()
    assert r"\newcolumntype{Y}{>{\RaggedRight\arraybackslash}X}" in t
    assert r"\newcolumntype{L}[1]{>{\RaggedRight\arraybackslash}p{#1}}" in t
    assert r"\usepackage{ragged2e}" in t, "\\RaggedRight is used without loading ragged2e"
    # the package must be requested before the column types are declared
    assert t.index(r"\usepackage{ragged2e}") < t.index(r"\newcolumntype{Y}")


# commit immediately before this phase's repair: the repair is measured against it, so the guard holds
# both before and after the P12AG commit. A later authorised manuscript change must be recorded there.
P12AG_PRE_REPAIR = "dbd68b600c641a20ede810c5110e9d3bed2ae101"


def test_ms_tex_differs_from_the_pre_repair_commit_only_by_the_package_line():
    try:
        out = subprocess.run(["git", "diff", "-U0", P12AG_PRE_REPAIR, "HEAD", "--", "paper9/latex/ms.tex"],
                             cwd=REPO, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git history unavailable")
    added = [l for l in out.splitlines() if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in out.splitlines() if l.startswith("-") and not l.startswith("---")]
    assert len(added) == 1 and not removed, f"ms.tex changed beyond the package line: {added} / {removed}"
    assert "ragged2e" in added[0]


def test_no_malformed_multicolumn_spec_survives():
    offenders = []
    for p in list(TABLES_OUT.glob("*.tex")) + list(TABLES_GEN.glob("*.py")):
        t = p.read_text()
        if MALFORMED_MULTICOLUMN in t:
            offenders.append(p.name)
    assert not offenders, f"malformed \\multicolumn column spec remains in: {offenders}"


def test_generators_reproduce_their_committed_outputs_byte_for_byte():
    """The generator, not a hand edit, owns each generated table (run in a scratch copy).

    tab03 joined this check in P12AH, when its stale template was reconciled with the P12AF-authorised
    content: before that, running it would have reverted the audited table.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "paper9" / "tables").mkdir(parents=True)
        (root / "paper9" / "params").mkdir(parents=True)
        (root / "paper9" / "results").mkdir(parents=True)
        subprocess.run(["cp", "-a", str(TABLES_GEN), str(root / "paper9" / "tables" / "gen")], check=True)
        (root / "paper9" / "tables" / "out").mkdir()
        for extra in ("params/params_master.yaml",):
            src = REPO / "paper9" / extra
            dst = root / "paper9" / extra
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        for extra in ("results/processed", "results/raw", "audit/evidence/p12h", "audit/evidence/p12b",
                      "verification/suite"):
            src = REPO / "paper9" / extra
            if src.exists():
                shutil.copytree(src, root / "paper9" / extra, dirs_exist_ok=True)
        for name in ("tab02_parameters", "tab03_anchor_errors", "tab05_gap_summary",
                     "tab06_convergence_floor"):
            r = subprocess.run(["python3", f"gen/{name}.py"], cwd=root / "paper9" / "tables",
                               capture_output=True, text=True)
            assert r.returncode == 0, f"{name} generator failed: {r.stderr[-400:]}"
            produced = (root / "paper9" / "tables" / "out" / f"{name}.tex").read_bytes()
            committed = (TABLES_OUT / f"{name}.tex").read_bytes()
            assert produced == committed, f"{name}.tex is not what its generator produces"


def test_escaped_characters_are_the_source_data_characters():
    """The escapes print characters that the source data actually contains — nothing new is rendered."""
    yaml_text = (REPO / "paper9" / "params" / "params_master.yaml").read_text()
    # P12AH inserted zero-width break opportunities after the escaped underscores so the long
    # identifiers can wrap; strip them to test the characters that are actually rendered.
    out = (TABLES_OUT / "tab02_parameters.tex").read_text().replace("\\hspace{0pt}", "")
    for source_literal, escaped in (("mu_matrix", r"mu\_matrix"),
                                    ("a_A", r"a\_A"),
                                    ("p11d_b2_gap_registry", r"p11d\_b2\_gap\_registry"),
                                    ("a1^2", r"a1\textasciicircum{}2")):
        assert source_literal in yaml_text, f"{source_literal} is not in the source data"
        assert escaped in out, f"{escaped} missing from the generated table"


def test_no_text_mode_underscore_or_caret_remains_in_the_parameter_table():
    p = TABLES_OUT / "tab02_parameters.tex"
    bad = [(n, l.strip()[:70]) for n, l in enumerate(p.read_text().splitlines(), 1)
           if not l.lstrip().startswith("%") and _text_mode_hits(l)]
    assert not bad, f"text-mode _/^ still present: {bad[:5]}"


def test_numerical_tokens_are_unchanged_in_the_repaired_tables():
    """The repair added no number, removed no number and changed no value."""
    for p in REPAIRED_OUTPUTS:
        tokens = sorted(_numeric_tokens(p.read_text()))
        got = hashlib.sha256("\n".join(tokens).encode()).hexdigest()
        assert got == NUMERIC_TOKEN_SHA256[p.name], f"{p.name} numerical tokens changed"
        for v in PINNED_VALUES[p.name]:
            assert v in p.read_text(), f"{p.name} lost {v}"


# ------------------------------------------------------------------ P12AF content preserved
def test_p12af_edited_files_are_byte_identical():
    for p, want in P12AF_CONTENT.items():
        assert _sha(p) == want, f"{p} changed after P12AF"


def test_statuses_and_gates_are_unchanged():
    rec = json.loads((AUDIT / "benchmark_validation_record.json").read_text())
    b = rec["benchmarks"]
    assert b["B1"]["route"] == "GRAPHICAL_VALIDATION" and b["B1"]["graphical_validation"] == "PASS"
    assert b["B2"]["route"] == "NOT_VALIDATED" and b["B3"]["route"] == "NOT_VALIDATED"
    assert b["B3"]["formulation_status"].startswith("ESTABLISHED / SOURCE-EQUIVALENT")
    assert [b[k]["quantitative_error"] for k in ("B1", "B2", "B3")] == [None, None, None]
    g = rec["gate_state"]
    assert (g["PCR1"], g["G3"], g["G4"], g["P5"], g["R-1"]) == (
        "NOT PASS", "NOT MET", "NOT MET", "NOT PASS/OPEN", "OPEN")


def test_blueprint_and_rule_and_p5_status_are_unchanged():
    frozen = {
        REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex":
            "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91",
        REPO / "paper9" / "verification" / "suite" / "rule_rfit.py":
            "d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8",
        AUDIT / "P5_STATUS.md":
            "1a410f228c117f3ada13557d643e1f1498a0f17881890f464e94e2e3f8489c8c",
        AUDIT / "benchmark_validation_record.json":
            "2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2",
    }
    for p, want in frozen.items():
        assert _sha(p) == want, f"{p} changed"


# ------------------------------------------------------------------ the build itself
def test_manuscript_compiles_from_the_repository_with_zero_errors(tmp_path):
    if shutil.which("pdflatex") is None or shutil.which("bibtex") is None:
        pytest.skip("TeX toolchain not installed in this environment")
    work = tmp_path / "build"
    work.mkdir()
    shutil.copytree(LATEX, work / "latex")
    (work / "tables").mkdir()
    shutil.copytree(TABLES_OUT, work / "tables" / "out")
    (work / "figures").mkdir()
    shutil.copytree(REPO / "paper9" / "figures" / "out", work / "figures" / "out")
    (work / "bib").mkdir()
    shutil.copy2(REPO / "paper9" / "bib" / "paper9.bib", work / "bib" / "paper9.bib")

    def run(cmd):
        return subprocess.run(cmd, cwd=work / "latex", capture_output=True, text=True, timeout=600)

    run(["pdflatex", "-interaction=nonstopmode", "ms.tex"])
    run(["pdflatex", "-interaction=nonstopmode", "ms.tex"])
    r = run(["bibtex", "ms"])
    assert "error" not in r.stdout.lower(), r.stdout[-400:]
    for _ in range(3):
        final = run(["pdflatex", "-interaction=nonstopmode", "ms.tex"])

    log = (work / "latex" / "ms.log").read_text(errors="ignore")
    assert not re.search(r"^! ", log, flags=re.M), "LaTeX errors present in the build"
    assert "no output PDF file produced" not in log
    assert (work / "latex" / "ms.pdf").exists(), "no PDF produced"
    assert "Citation" not in log or "undefined" not in log.split("Citation", 1)[1][:40]
    assert not re.search(r"Reference .* undefined", log)
    assert not re.search(r"File .* not found", log)
    assert "Rerun to get" not in log, "cross-references/bibliography did not settle"
