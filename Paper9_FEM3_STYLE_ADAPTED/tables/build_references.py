#!/usr/bin/env python3
"""Build the Paper9 bibliography for the FEM_3-style adapted manuscript.

Correspondence decision (see REPORT, section D):
  * The ACTIVE bibliography (OVERLEAF/references.bib) is the byte-identical
    authoritative Paper9 .bib (original keys such as ``kushwaha1993``).  With
    ``\\bibliographystyle{elsarticle-num}``, BibTeX numbers entries in the
    order of FIRST citation, which is FEM_3's citation convention and which
    equals the stock ``unsrt`` numbering because the section files are
    byte-identical to the authoritative package.
  * A numerical-key PREVIEW (references_numeric.bib, ``ref1..ref15``) is also
    written for the report, with the exact first-citation key map.

No bibliographic field (authors, title, journal, volume, number, pages, year,
DOI, booktitle, address) is altered in either file; only the internal key
labels change in the preview.  A label map is printed for the report.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
SRC = os.path.join(PKG, "OVERLEAF", "PAPER9_ORIGINAL_manuscript.tex")
BIB_ORIG = os.path.join(PKG, "ORIGINAL", "references_original_keys.bib")
BIB_NUM = os.path.join(HERE, "references_numeric.bib")
MAP_TXT = os.path.join(HERE, "bib_key_map.txt")

USED_IN_ORIGINAL = [
    "askesaifantis2011",
    "bfs1965",
    "hosseinizhang2021",
    "kushwaha1993",
    "li2023anchorA",
    "li2024anchorB",
    "liweizhou2016",
    "mindlin1964",
    "mindlineshel1968",
    "mishra2026anchorC",
    "papargyribeskou2009",
    "polyzosfotiadis2012",
    "toupin1962",
    "zhanwei2010",
    "zhengwei2009",
]

# elsarticle-num numbers entries in order of FIRST CITATION (verified from the
# FEM_3 reference build: Shekarchizadeh et al. is [1] because it is cited
# first, in the abstract).  The citation order in Paper9 is fixed by the
# byte-identical section files and matches the stock `unsrt` numbering.
CITATION_ORDER = [
    "kushwaha1993",        # sec01 first citation -> [1]
    "mindlin1964",         # -> [2]
    "toupin1962",          # -> [3]
    "mindlineshel1968",    # -> [4]
    "askesaifantis2011",   # -> [5]
    "polyzosfotiadis2012", # -> [6]
    "papargyribeskou2009", # -> [7]
    "liweizhou2016",       # -> [8]
    "zhanwei2010",         # -> [9]
    "zhengwei2009",        # -> [10]
    "hosseinizhang2021",   # -> [11]
    "li2023anchorA",       # -> [12]
    "li2024anchorB",       # -> [13]
    "mishra2026anchorC",   # -> [14]
    "bfs1965",             # -> [15]
]


def assigned(key):
    return "ref%d" % (CITATION_ORDER.index(key) + 1)


def main():
    os.makedirs(OSL := os.path.dirname(BIB_ORIG), exist_ok=True)

    # Locate the original .bib file shipped in the package.
    bib_src = os.path.join(PKG, "OVERLEAF", "references.bib")
    if not os.path.exists(bib_src):
        print("ABORT: original references.bib not found at", bib_src)
        sys.exit(2)

    raw = open(bib_src, "r", encoding="utf-8").read()

    # Verify the keys we expect are all present (case-sensitive).
    keys = set()
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("@"):
            keys.add(line.split("{", 1)[1].rstrip(","))

    for k in USED_IN_ORIGINAL:
        if k not in keys:
            print("MISSING KEY (not in bib):", k)
    extra = sorted(keys - set(USED_IN_ORIGINAL))
    if extra:
        warn = "NOTE: bib contains keys not in USED_IN_ORIGINAL list: %s" % ", ".join(extra)
        print(warn)

    # Save the byte-identical original-key bibliography as a working artifact.
    with open(BIB_ORIG, "w", encoding="utf-8") as f:
        f.write(raw)

    # Rewrite entry keys in place (each ``@type{key,`` -> ``@type{ref<n>,``).
    numeric = raw
    for k in USED_IN_ORIGINAL:
        numeric = numeric.replace("{%s," % k, "{%s," % assigned(k))
    with open(BIB_NUM, "w", encoding="utf-8") as f:
        f.write(numeric)
    # The ACTIVE OVERLEAF bibliography is the byte-identical original-keyed
    # version; the numeric-keyed file is a report preview only.
    with open(os.path.join(PKG, "OVERLEAF", "references.bib"), "w", encoding="utf-8") as f:
        f.write(raw)
    print("OVERLEAF/references.bib -> byte-identical original-keyed version (active)")
    print("tables/references_numeric.bib -> numeric-keyed preview (ref1..ref15)")

    with open(MAP_TXT, "w", encoding="utf-8") as f:
        f.write("Paper9 references, numbered by FIRST-CITATION order (elsarticle-num style,\n")
        f.write("verified against the FEM_3 reference build, where [1] is the first-cited work).\n")
        f.write("The number is identical to the stock compiled `unsrt` numbering because the\n")
        f.write("section files are byte-identical to the authoritative Paper9 package.\n")
        f.write("The ACTIVE OVERLEAF/references.bib keeps the authoritative original keys;\n")
        f.write("this table maps them to the report numbers (and to the preview keys ref<n>).\n")
        f.write("-" * 78 + "\n")
        for i, k in enumerate(CITATION_ORDER, 1):
            f.write("[%2d] %-24s -> %s\n" % (i, k, assigned(k)))
        f.write("(No bibliographic field was altered; only the internal key labels changed.)\n")

    print("Wrote numeric bibliography ->", BIB_NUM)
    print("Wrote key map             ->", MAP_TXT)
    print()
    for i, k in enumerate(CITATION_ORDER, 1):
        print("[%2d] %-4s  %s" % (i, assigned(k), k))


if __name__ == "__main__":
    main()
