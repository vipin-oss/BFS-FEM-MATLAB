"""P12AH/P12AI guards - table layout repair (Table 2 in P12AH; five more in the P12AI closure).

The P12AH report measured, for each table that overflows the text width, a content-neutral configuration
and recorded it for authorisation.  The P12AI closure checked the rendered PDF and found that five of those
tables print content outside the physical page (whole columns invisible, "PASS" cut to "PAS", a provenance
column and a Rule R-fit footnote sentence absent from the printed page), so the minimum fix was applied to
exactly those five.  Table 6 (tab05) is readable and was deliberately NOT modified.

Every repair is layout only: column specification, table-internal font size, column separation, zero-width
break opportunities after escaped underscores in long identifiers, and the width of full-width note rows.
No character, number, symbol, caption, footnote or claim changed.

Proved per table, not asserted:
  * the committed file with the documented layout edits undone is byte-identical to the file as the phase
    found it (sha256 of the entry bytes pinned below);
  * running the table's generator in a scratch copy reproduces the committed bytes exactly, so the
    generator - not a hand edit - owns the file;
  * the table compiles alone with zero LaTeX errors and zero overfull boxes;
  * the numeric content is unchanged once layout markup is ignored;
  * Table 6 is byte-identical to the entry bytes because it was deliberately left alone.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
P9 = REPO / "paper9"
MS = P9 / "latex" / "ms.tex"
FIG05 = P9 / "figures" / "out" / "fig05_mesh_convergence.pdf"
ENTRY_COMMIT = "e986a13fdd82e8df1e2c93a534aa6ae4163bd8e6"   # the P12AH-verified state this closure starts from

# table -> generator that owns it, sha256 of the entry bytes, and the layout edits to undo (may be empty)
LAYOUT = {
    "tab01_literature_positioning": {
        "generator": 'paper9/tables/gen/tab01_literature_positioning.py',
        "entry_sha256": 'e47d4f7058c7249a2a63f79caf45e7d49468e23253ae1cbccdb54cd6b6049759',
        "undo_target": 'entry_commit',
        "undo": [
            ('\\footnotesize\n\\setlength{\\tabcolsep}{2pt}\n', '', 1),
            ('\\begin{tabularx}{\\textwidth}{@{}>{\\raggedright\\arraybackslash}p{2.0cm} c c >{\\raggedright\\arraybackslash}p{2.4cm} c c c >{\\raggedright\\arraybackslash}p{2.0cm} Y@{}}', '\\begin{tabularx}{\\textwidth}{@{}l c c l c c c l Y@{}}', 1),
        ],
    },

    "tab02_parameters": {
        "generator": 'paper9/tables/gen/tab02_parameters.py',
        "entry_sha256": '16c621f3f08c25abba540f6a90eb69e605380c7398f1b6beab2338c18b102fa9',
        "undo_target": 'entry_commit',
        "undo": [
            ('\\scriptsize\n\\setlength{\\tabcolsep}{2pt}\n', '', 1),
            ('\\begin{tabularx}{\\textwidth}{@{}l >{\\raggedright\\arraybackslash}p{2.5cm} >{\\raggedright\\arraybackslash}p{1.8cm} c L{3.0cm} Y@{}}', '\\begin{tabularx}{\\textwidth}{@{}l l l c L{3.5cm} Y@{}}', 1),
            ('\\_\\hspace{0pt}', '\\_', 41),
        ],
    },

    "tab03_anchor_errors": {
        "generator": 'paper9/tables/gen/tab03_anchor_errors.py',
        "entry_sha256": '77fd75844415869f0ce94c720af38b7370635b004640591f69ce42fa5de5c113',
        "undo_target": 'p12af_content',
        "undo": [
            ('\\setlength{\\tabcolsep}{2pt}\n', '', 1),
            ('\\begin{tabularx}{\\textwidth}{@{}l >{\\raggedright\\arraybackslash}X >{\\raggedright\\arraybackslash}X ccc >{\\raggedright\\arraybackslash}p{2.0cm} >{\\raggedright\\arraybackslash}p{2.4cm}@{}}', '\\begin{tabular}{lp{3.2cm}p{2.8cm}cccp{2.5cm}c}', 1),
            ('\\end{tabularx}', '\\end{tabular}', 1),
            ('GRAPHICAL\\_\\hspace{0pt}VALIDATION', 'GRAPHICAL\\_VALIDATION', 1),
            ('SOURCE\\_\\hspace{0pt}EQUATIONS', 'SOURCE\\_EQUATIONS', 1),
            ('GRAPH\\_\\hspace{0pt}ONLY', 'GRAPH\\_ONLY', 3),
        ],
    },

    "tab04_consistency_suite": {
        "generator": 'paper9/tables/gen/tab04_consistency_suite.py',
        "entry_sha256": '0ec19e556e401b18c811d2257015baba862fa359fa7b73559f0fc8983f968196',
        "undo_target": 'entry_commit',
        "undo": [
            ('\\begin{tabularx}{\\textwidth}{@{}l L{4.0cm} >{\\raggedright\\arraybackslash}p{3.6cm} l l c@{}}', '\\begin{tabularx}{\\textwidth}{@{}l L{4.5cm} l l l c@{}}', 1),
        ],
    },

    "tab05_gap_summary": {
        "generator": 'paper9/tables/gen/tab05_gap_summary.py',
        "entry_sha256": 'a696586b0b7c7c3a5e92cae3e57137483caa4941ab92c12669d06164aea30a9f',
        "undo_target": 'entry_commit',
        "undo": [
        ],
    },

    "tab06_convergence_floor": {
        "generator": 'paper9/tables/gen/tab06_convergence_floor.py',
        "entry_sha256": '478545af3e8dabc5d8e5f51e4716b50aa85198385f7350bc8102ef88baa8bd19',
        "undo_target": 'entry_commit',
        "undo": [
            ('\\footnotesize\n\\setlength{\\tabcolsep}{3pt}\n', '', 1),
            ('\\begin{tabularx}{\\textwidth}{@{}c c r l l c c >{\\raggedright\\arraybackslash}p{2.0cm}@{}}', '\\begin{tabularx}{\\textwidth}{@{}c c r l l c c l@{}}', 1),
            ('\\multicolumn{8}{@{}>{\\raggedright\\arraybackslash}p{\\dimexpr\\textwidth-2\\tabcolsep\\relax}@{}}', '\\multicolumn{8}{@{}l@{}}', 3),
        ],
    },

    "tab07_steering_sweep": {
        "generator": 'paper9/tables/gen/tab07_steering_sweep.py',
        "entry_sha256": 'bcf8ca92e2573ae0f2953d2ceb2aa420f4174b7a1ae982f67eccf0a3b57c2cfc',
        "undo_target": 'entry_commit',
        "undo": [
            ('\\multicolumn{5}{@{}>{\\raggedright\\arraybackslash}p{\\dimexpr\\textwidth-2\\tabcolsep\\relax}@{}}', '\\multicolumn{5}{@{}l@{}}', 2),
        ],
    },

}

UNREPAIRED = [t for t, v in LAYOUT.items() if not v["undo"]]


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _entry_text(table: str) -> str:
    return subprocess.run(["git", "show", f"{ENTRY_COMMIT}:paper9/tables/out/{table}.tex"],
                          cwd=REPO, capture_output=True, text=True, check=True).stdout


def _neutral_text(table: str) -> str:
    """The committed table with every layout edit undone (the content the phase started from)."""
    text = (P9 / "tables" / "out" / f"{table}.tex").read_text()
    for new, old, count in LAYOUT[table]["undo"]:
        assert text.count(new) == count, f"{table}: expected {count} of {new[:50]!r}, found {text.count(new)}"
        text = text.replace(new, old)
    return text


@pytest.mark.parametrize("table", sorted(LAYOUT))
def test_content_is_untouched_by_the_layout_repair(table):
    """Undoing the documented layout edits reproduces the pinned pre-layout content exactly."""
    neutral = _neutral_text(table)
    assert hashlib.sha256(neutral.encode()).hexdigest() == LAYOUT[table]["entry_sha256"]
    if LAYOUT[table]["undo_target"] == "entry_commit":
        assert neutral == _entry_text(table)


def test_tables_left_unrepaired_are_byte_identical_to_the_entry_commit():
    """Table 6 (tab05) prints completely, so it was deliberately left untouched."""
    assert UNREPAIRED, "expected at least one deliberately unrepaired table"
    for table in UNREPAIRED:
        assert (P9 / "tables" / "out" / f"{table}.tex").read_text() == _entry_text(table), table


@pytest.mark.parametrize("table", sorted(LAYOUT))
def test_generator_reproduces_the_committed_table(table):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "paper9" / "tables" / "gen").mkdir(parents=True)
        (root / "paper9" / "tables" / "out").mkdir(parents=True)
        shutil.copy2(REPO / LAYOUT[table]["generator"], root / LAYOUT[table]["generator"])
        inputs = ("paper9/params/params_master.yaml",
                  "paper9/verification/suite/p4b_5g_to_5i.json",
                  "paper9/audit/evidence/p12h/rule_rfit_governing.json",
                  "paper9/results/processed/table5_gap_summary.json",
                  "paper9/results/raw/p12b_s7_theta_sweep.json")
        for rel in inputs:
            src = REPO / rel
            if src.exists():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, root / rel)
        r = subprocess.run(["python3", str(root / LAYOUT[table]["generator"])],
                           capture_output=True, text=True, timeout=300)
        assert r.returncode == 0, r.stderr[-500:]
        fresh = root / "paper9" / "tables" / "out" / f"{table}.tex"
        assert _sha(fresh) == _sha(P9 / "tables" / "out" / f"{table}.tex"), "generated bytes differ"


@pytest.mark.parametrize("table", sorted(LAYOUT))
def test_no_number_moved_by_the_layout_repair(table):
    def tokens(s):
        s = re.sub(r"\\setlength\{\\tabcolsep\}\{[0-9.]+pt\}", "", s)
        s = re.sub(r"\\hspace\{0pt\}", "", s)
        s = s.replace(r"\dimexpr\textwidth-2\tabcolsep\relax", "")
        s = re.sub(r"\\begin\{tabularx?\}[^\n]*", "", s)   # the whole column specification
        return re.findall(r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    assert tokens((P9 / "tables" / "out" / f"{table}.tex").read_text()) == tokens(_neutral_text(table))


@pytest.mark.parametrize("table", [t for t, v in sorted(LAYOUT.items()) if v["undo"]])
def test_repaired_table_compiles_without_overfull_box(table):
    if shutil.which("pdflatex") is None:
        pytest.skip("TeX toolchain not installed in this environment")
    preamble = MS.read_text().split("\\begin{document}")[0].replace(
        "\\documentclass[11pt,a4paper]{article}",
        "\\documentclass[11pt,a4paper]{article}\n\\RequirePackage{ragged2e}")
    table_tex = (P9 / "tables" / "out" / f"{table}.tex").read_text()
    body_tex = table_tex if "\\begin{table" in table_tex else (
        "\\begin{table}[htbp]\\centering\n" + table_tex + "\n\\end{table}")
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        (work / "t.tex").write_text(preamble + "\n\\begin{document}\n" + body_tex + "\n\\end{document}\n")
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "t.tex"], cwd=work,
                           capture_output=True, timeout=300)
        log = (work / "t.log").read_text(errors="ignore")
    assert not re.search(r"^! ", log, flags=re.M), f"{table}: LaTeX errors"
    overfull = re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide", log)
    assert not overfull, f"{table} still overflows: {overfull}"
    assert "X Columns too narrow" not in log


def test_manuscript_prose_is_unchanged():
    assert _sha(P9 / "latex" / "sections" / "sec05_verification.tex") == \
        "bfd45dd077e7cc4c542fef3fb3d24f89e1c1ea7958bf5052a97fb86b36d507c1"


# ---------------------------------------------------------------- Figure 5 freshness, content-based
def test_figure_5_freshness_is_judged_by_content_not_mtime():
    """Supersedes the P12J mtime ordering check: the derivation inputs are pinned by hash."""
    recorded = json.loads((P9 / "audit" / "P12AH_FIGURE_FRESHNESS.json").read_text())
    assert _sha(FIG05) == recorded["fig05_output_sha256"], "Figure 5 bytes changed"
    for rel, want in recorded["inputs"].items():
        assert _sha(REPO / rel) == want, f"{rel} changed since Figure 5 was verified"
