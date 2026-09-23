#!/usr/bin/env python3
"""
test_p7_manuscript.py
Automated audit and verification test suite for Phase 11 full-scope manuscript.
Verifies LaTeX structure, references, citations, float inventory, gate compliance, and safety constraints.
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LATEX_DIR = REPO_ROOT / "paper9" / "latex"
BIB_FILE = REPO_ROOT / "paper9" / "bib" / "paper9.bib"
MASTER_TEX = LATEX_DIR / "ms.tex"

def test_p7_manuscript():
    print("=" * 70)
    print("RUNNING P11 MANUSCRIPT AUDIT")
    print("=" * 70)

    assert MASTER_TEX.exists(), f"Master LaTeX file not found: {MASTER_TEX}"
    master_content = MASTER_TEX.read_text(encoding="utf-8")

    # 1. Check section inputs
    input_pattern = re.compile(r"\\input\{([^}]+)\}")
    section_inputs = input_pattern.findall(master_content)
    print(f"[1] Found {len(section_inputs)} section inclusions in ms.tex:")
    full_content = master_content
    for sec in section_inputs:
        sec_path = LATEX_DIR / (sec if sec.endswith(".tex") else f"{sec}.tex")
        assert sec_path.exists(), f"Included section missing: {sec_path}"
        sec_text = sec_path.read_text(encoding="utf-8")
        full_content += "\n" + sec_text
        print(f"    - Inlined: {sec_path.name} ({len(sec_text.splitlines())} lines)")

    # 2. Check table inputs inside full content
    table_inputs = input_pattern.findall(full_content)
    # Filter for table files
    tex_tables = [t for t in table_inputs if "tables/out" in t or "tab0" in t]
    print(f"[2] Found {len(tex_tables)} table inclusions:")
    expected_tables = ["tab01", "tab02", "tab04", "tab05", "tab06"]
    for expected in expected_tables:
        matched = [t for t in tex_tables if expected in t]
        assert len(matched) == 1, f"Expected table {expected} not uniquely matched: {matched}"
        # verify file exists
        tbl_path = (LATEX_DIR / matched[0]).resolve()
        assert tbl_path.exists(), f"Table file does not exist: {tbl_path}"
        print(f"    - Table verified: {tbl_path.name}")

    # 3. Check figure inclusions
    fig_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
    fig_inclusions = fig_pattern.findall(full_content)
    print(f"[3] Found {len(fig_inclusions)} figure inclusions:")
    expected_figs = ["fig01", "fig02", "fig03", "fig05", "fig06", "fig07", "fig08", "fig09", "fig10", "fig11", "fig12", "fig13"]
    for expected in expected_figs:
        matched = [f for f in fig_inclusions if expected in f]
        assert len(matched) == 1, f"Expected figure {expected} not uniquely matched: {matched}"
        fig_path = (LATEX_DIR / matched[0]).resolve()
        assert fig_path.exists(), f"Figure file does not exist: {fig_path}"
        print(f"    - Figure verified: {fig_path.name}")

    # 4. Check Unblocked Sections and Case C Integration
    print("[4] Checking unblocked deliverables and verified content:")
    assert "fig:caseC_dispersion" in full_content, "Case C Figure label missing"
    assert "Figure~\\ref{fig:caseC_dispersion}" in full_content or "\\ref{fig:caseC_dispersion}" in full_content
    assert "Delta_{\\mathrm{complete}} = 2.5732" in full_content or "2.5732" in full_content
    assert "Benchmark B1" in full_content
    assert "Benchmark B2" in full_content
    assert "Benchmark B3" in full_content
    assert "Evidence Hierarchy" in full_content
    print("    - Case C, Benchmarks B1--B3, and Evidence Hierarchy verified.")

    # 5. Check Bibliography and Citations
    assert BIB_FILE.exists(), f"Bib file not found: {BIB_FILE}"
    bib_text = BIB_FILE.read_text(encoding="utf-8")
    bib_entry_keys = set(re.findall(r"@\w+\{\s*([^,]+),", bib_text))
    print(f"[5] Found {len(bib_entry_keys)} BibTeX entries in paper9.bib:")
    for k in sorted(bib_entry_keys):
        print(f"    - Bib entry: {k}")

    # Collect citations
    cite_pattern = re.compile(r"\\cite\{([^}]+)\}")
    all_cites = set()
    for match in cite_pattern.findall(full_content):
        for c in match.split(","):
            all_cites.add(c.strip())
    print(f"    - Found {len(all_cites)} unique citation keys in text.")

    # Cross check
    for c in all_cites:
        assert c in bib_entry_keys, f"Citation key '{c}' not found in paper9.bib!"

    orphans = bib_entry_keys - all_cites
    assert len(orphans) == 0, f"Found orphan BibTeX entries (cited nowhere): {orphans}"
    print("    - Citation integrity: 100% match, zero undefined, zero orphan entries.")

    # 6. Check Labels and References
    label_pattern = re.compile(r"\\label\{([^}]+)\}")
    ref_pattern = re.compile(r"\\ref\{([^}]+)\}")
    all_labels = set(label_pattern.findall(full_content))
    all_refs = set(ref_pattern.findall(full_content))
    print(f"[6] Found {len(all_labels)} labels and {len(all_refs)} references.")
    for r in all_refs:
        assert r in all_labels, f"Reference '{r}' does not match any label!"
    print("    - Cross-reference integrity: 100% match, zero undefined references.")

    # 7. Safety and Compliance Linting (Prohibited Claims)
    print("[7] Checking safety and compliance constraints:")
    forbidden_rules = [
        (r"O\(h\^4\.17\)", "Forbidden: empirical rate expressed as asymptotic O notation"),
        (r"theoretical\s+(?:fourth|4th)[-\s]order", "Forbidden: theoretical fourth-order convergence claim"),
        (r"complete\s+band\s+gap\s+in\s+Case\s+H", "Forbidden: claim of complete band gap in Case H"),
        (r"Case\s+H\s+exhibits\s+a\s+complete\s+band\s+gap", "Forbidden: claim of complete band gap in Case H"),
        (r"closed\s+2D\s+IFC", "Forbidden: claiming closed 2D IFC for Figure 12"),
    ]
    for regex, desc in forbidden_rules:
        match = re.search(regex, full_content, re.IGNORECASE)
        assert match is None, f"Safety violation detected: {desc} (match: '{match.group(0)}')"
        print(f"    - Clean: {desc}")

    print("=" * 70)
    print("ALL MANUSCRIPT AUDIT CHECKS PASSED (100%)")
    print("=" * 70)

if __name__ == "__main__":
    test_p7_manuscript()
