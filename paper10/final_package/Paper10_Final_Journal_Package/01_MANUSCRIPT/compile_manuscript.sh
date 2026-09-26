#!/bin/bash
# Compilation script for Paper 10 Manuscript
# (Phase-0 update: robust quoting + Typst numbering prelude + typst-py fallback)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Compiling Paper 10 Manuscript ==="

PANDOC_BIN="${PANDOC_BIN:-pandoc}"

echo "1. Generating typst intermediate from LaTeX source with pandoc..."
"$PANDOC_BIN" Paper10_Manuscript.tex -o paper10.typ --citeproc --bibliography=references.bib

echo "2. Applying label post-processing for Typst block references..."
python3 <<'PYFIX'
import re
with open('paper10.typ') as f:
    content = f.read()
fixed = re.sub(r'(\#figure\([\s\S]*?\))\s*\n\s*\]\s*(<tab:[\w_]+>)', r'\1 \2\n]', content)
fixed = re.sub(r'(\#figure\([\s\S]*?\))\s*\n\s*\]\s*(<fig:[\w_]+>)', r'\1 \2\n]', fixed)
with open('paper10.typ', 'w') as f:
    f.write(fixed)
PYFIX

echo "2.5 Prepending Typst numbering prelude (if missing)..."
python3 <<'PYPRE'
prelude = (
    '#set page(paper: "a4", margin: 2.5cm)\n'
    '#set text(size: 11pt, lang: "en")\n'
    '#set heading(numbering: "1.1")\n'
    '#set math.equation(numbering: "(1)")\n'
)
with open('paper10.typ') as f:
    src = f.read()
if 'set heading(numbering' not in src:
    with open('paper10.typ', 'w') as f:
        f.write(prelude + src)
PYPRE

echo "3. Compiling PDF via Typst..."
if command -v typst >/dev/null 2>&1; then
    typst compile paper10.typ Paper10_Manuscript.pdf
else
    # Fallback: typst Python bindings (pip install typst)
    python3 -c "import typst; typst.compile('paper10.typ', output='Paper10_Manuscript.pdf')"
fi

echo "✓ Paper10_Manuscript.pdf successfully compiled!"
python3 -c "import pymupdf; doc = pymupdf.open('Paper10_Manuscript.pdf'); print(f'Page count: {len(doc)} pages.')"
