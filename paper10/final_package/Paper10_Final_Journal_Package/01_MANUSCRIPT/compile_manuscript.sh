#!/bin/bash
# Compilation script for Paper 10 Manuscript
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Compiling Paper 10 Manuscript ==="
echo "1. Generating typst intermediate from LaTeX source with pandoc..."
pandoc Paper10_Manuscript.tex -o paper10.typ --citeproc --bibliography=references.bib

echo "2. Applying label post-processing for Typst block references..."
python3 -c "
import re
with open('paper10.typ') as f:
    content = f.read()
fixed = re.sub(r'(\#figure\([\s\S]*?\))\s*\n\s*\]\s*(<tab:[\w_]+>)', r'\1 \2\n]', content)
fixed = re.sub(r'(\#figure\([\s\S]*?\))\s*\n\s*\]\s*(<fig:[\w_]+>)', r'\1 \2\n]', fixed)
with open('paper10.typ', 'w') as f:
    f.write(fixed)
"

echo "3. Compiling PDF via Typst..."
typst compile paper10.typ Paper10_Manuscript.pdf

echo "✓ Paper10_Manuscript.pdf successfully compiled!"
python3 -c "import pymupdf; doc = pymupdf.open('Paper10_Manuscript.pdf'); print(f'Page count: {len(doc)} pages.')"
