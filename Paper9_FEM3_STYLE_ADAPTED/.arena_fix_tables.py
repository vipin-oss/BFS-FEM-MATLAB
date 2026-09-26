#!/usr/bin/env python3
"""Formatting-only rebuild of tab02, tab03, tab05 fragments.

All DATA cells, header text, captions, and footnotes are copied byte-for-byte
from the authoritative fragments; ONLY the LaTeX container changes.

Colspecs are hardcoded (they are fixed in the authoritative files).
"""
import re, os
PKG = "/home/user/BFS-FEM-MATLAB/Paper9_FEM3_STYLE_ADAPTED"
# authoritative fragments are in tables/tables_rebuilt (and also tables/ for legacy)
SRC_CANDIDATES = [
    os.path.join(PKG, "tables", "tables_rebuilt"),
    os.path.join(PKG, "tables"),
    os.path.join(PKG, "PROGRAM", "paper9", "tables", "out"),
]
SRC = next((p for p in SRC_CANDIDATES if os.path.isdir(p)), SRC_CANDIDATES[0])
DST = os.path.join(PKG, "OVERLEAF", "tables")

COLSPEC_TAB02 = "{@{}l >{\\raggedright\\arraybackslash}p{2.5cm} >{\\raggedright\\arraybackslash}p{1.8cm} c L{3.0cm} Y@{}}"
COLSPEC_TAB03 = "{@{}l >{\\raggedright\\arraybackslash}X >{\\raggedright\\arraybackslash}X ccc >{\\raggedright\\arraybackslash}p{2.0cm} >{\\raggedright\\arraybackslash}p{2.4cm}@{}}"
COLSPEC_TAB05 = "{@{}c c c r r r r c c@{}}"
COLSPEC_TAB05_FIX = "{@{}c c c r r r r c >{\\raggedright\\arraybackslash}p{2.6cm}@{}}"


def clean_row(s):
    """Return a body/header row with exactly one terminating '\\\\'."""
    return s.rstrip().rstrip("\\").rstrip() + " \\\\"


def rebuild_tab02():
    raw = open(os.path.join(SRC, "tab02_parameters.tex"), encoding="utf-8").read()
    lines = raw.splitlines()
    assert any("\\begin{tabularx}{\\textwidth}" + COLSPEC_TAB02 in l for l in lines), "tab02 colspec mismatch"
    hidx = next(i for i, l in enumerate(lines) if 'Symbol & Value & Unit' in l)
    header = clean_row(lines[hidx])
    mididx = next(i for i in range(hidx, len(lines)) if lines[i].strip() == '\\midrule')
    bottomidx = max(i for i, l in enumerate(lines) if l.strip() == '\\bottomrule')
    body = lines[mididx+1:bottomidx]
    note = [
        "% Table fragment for the FEM_3-style adapted package (formatting-only edit).",
        "% Every data row/cell below is byte-identical to the authoritative tab02_parameters.tex;",
        "% only the container changed: tabularx float -> xltabular so the 60+-row registry",
        "% breaks across pages (resolves the ~1300pt 'Float too large' truncation).",
    ]
    scaffold = [
        "\\begingroup",
        "\\setlength{\\LTcapwidth}{\\textwidth}",
        "\\setlength{\\tabcolsep}{2pt}",
        "\\begin{xltabular}{\\textwidth}" + COLSPEC_TAB02,
        "\\caption{Master simulation parameter registry with provenance classifications.}"
        "\\label{tab:master_params}\\\\",
        "\\toprule",
        "\\scriptsize",
        header,
        "\\midrule",
        "\\endfirsthead",
        "\\multicolumn{6}{@{}l@{}}{\\footnotesize\\emph{Table~\\ref{tab:master_params} --- continued"
        " from previous page}}\\\\",
        "\\toprule",
        header,
        "\\midrule",
        "\\endhead",
        "\\bottomrule",
        "\\endfoot",
        "\\bottomrule",
        "\\endlastfoot",
        "\\scriptsize",
    ]
    out = note + scaffold + list(body) + ["\\end{xltabular}", "\\endgroup"]
    open(os.path.join(DST, "tab02_parameters.tex"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("tab02 rebuilt: %d body rows" % len(body))


def rebuild_tab03():
    raw = open(os.path.join(SRC, "tab03_anchor_errors.tex"), encoding="utf-8").read()
    lines = raw.splitlines()
    assert any("\\begin{tabularx}{\\textwidth}" + COLSPEC_TAB03 in l for l in lines), "tab03 colspec mismatch"
    cap = next(l for l in lines if l.strip().startswith("\\caption{")).strip()
    hidx = [i for i, l in enumerate(lines) if "\\hline\\hline" in l]
    first, last = hidx[0], hidx[-1]
    header_row = clean_row(lines[first + 1])
    data_rows = [l.strip() for l in lines[first + 3:last] if l.strip()]
    assert len(data_rows) == 4, "expected 4 tab03 data rows, got %d" % len(data_rows)
    t_end = next(i for i, l in enumerate(lines) if l.strip() == "\\end{tabularx}")
    tble_end = next(i for i, l in enumerate(lines) if l.strip() == "\\end{table*}")
    footnote_lines = lines[t_end+1:tble_end]
    foots = [l.strip() for l in footnote_lines if l.strip().startswith('$^')]
    assert len(foots) == 7, "expected 7 footnotes, got %d" % len(foots)
    width = "\\dimexpr\\textwidth-2\\tabcolsep\\relax"
    note = [
        "% Table fragment for the FEM_3-style adapted package (formatting-only edit).",
        "% All caption/data-cell/footnote text byte-identical to the authoritative",
        "% tab03_anchor_errors.tex; only container changed: table* float -> xltabular so the",
        "% benchmark table + footnotes break across pages (resolves the 92pt overflow).",
    ]
    head_block = [
        "\\hline\\hline",
        "\\footnotesize",
        header_row,
        "\\hline",
    ]
    scaffold = [
        "\\begingroup",
        "\\setlength{\\LTcapwidth}{\\textwidth}",
        "\\renewcommand{\\arraystretch}{1.2}",
        "\\setlength{\\tabcolsep}{2pt}",
        "\\begin{xltabular}{\\textwidth}" + COLSPEC_TAB03,
        cap + "\\label{tab:anchor_errors}\\\\",
    ] + head_block + [
        "\\endfirsthead",
        "\\multicolumn{8}{@{}l@{}}{\\footnotesize\\emph{continued from previous page}}\\\\",
        "\\hline",
        header_row,
        "\\hline",
        "\\endhead",
        "\\hline",
        "\\endfoot",
        "\\hline\\hline",
        "\\endlastfoot",
    ]
    foot_rows = []
    for idx, f in enumerate(foots):
        txt = f.rstrip("\\").rstrip()
        if idx < len(foots) - 1:
            foot_rows.append("\\multicolumn{8}{@{}>{\\raggedright\\arraybackslash}p{%s}@{}}{%s}\\\\" % (width, txt))
        else:
            foot_rows.append("\\multicolumn{8}{@{}>{\\raggedright\\arraybackslash}p{%s}@{}}{%s}" % (width, txt))
    out = note + scaffold + data_rows + ["\\hline\\hline"] + foot_rows + ["\\end{xltabular}", "\\endgroup"]
    open(os.path.join(DST, "tab03_anchor_errors.tex"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("tab03 rebuilt: %d data rows, %d footnotes" % (len(data_rows), len(foot_rows)))


def rebuild_tab05():
    raw = open(os.path.join(SRC, "tab05_gap_summary.tex"), encoding="utf-8").read()
    assert ("\\begin{tabularx}{\\textwidth}" + COLSPEC_TAB05) in raw, "tab05 colspec mismatch"
    newbody = raw.replace(
        "\\begin{tabularx}{\\textwidth}" + COLSPEC_TAB05,
        "\\setlength{\\tabcolsep}{2pt}\n\\begin{tabularx}{\\textwidth}" + COLSPEC_TAB05_FIX, 1)
    note = ("% Table fragment for the FEM_3-style adapted package (formatting-only edit).\n"
            "% Data cells byte-identical to the authoritative tab05_gap_summary.tex;\n"
            "% only tabcolsep=2pt + a wrapping last column (c -> p{2.6cm}) were applied so\n"
            "% the wide headers fit the 1in-margin text width (adaptation-worsened overflow).\n")
    open(os.path.join(DST, "tab05_gap_summary.tex"), "w", encoding="utf-8").write(note + newbody)
    print("tab05 rebuilt (colsep 2pt + wrapping last column)")


def edit_sec05():
    p = os.path.join(PKG, "OVERLEAF", "sections", "sec05_verification.tex")
    s = open(p, encoding="utf-8").read()
    old = ("\\begin{table}[htbp]\n"
           "\\centering\n"
           "\\caption{Master simulation parameter registry with provenance classifications.}\n"
           "\\label{tab:master_params}\n"
           "\\input{tables/tab02_parameters.tex}\n"
           "\\end{table}")
    newline = "\\input{tables/tab02_parameters.tex}"
    assert old in s or newline in s, "sec05 tab02 wrapper state unexpected"
    if old in s:
        s = s.replace(old, "\\input{tables/tab02_parameters.tex}", 1)
        open(p, "w", encoding="utf-8").write(s)
        print("sec05: tab02 float wrapper removed (caption/label moved into fragment)")
    else:
        print("sec05: tab02 float wrapper already removed; no change")


if __name__ == "__main__":
    rebuild_tab02()
    rebuild_tab03()
    rebuild_tab05()
    edit_sec05()
