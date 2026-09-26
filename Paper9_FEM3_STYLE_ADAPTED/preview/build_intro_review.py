#!/usr/bin/env python3
"""Build a readable PDF proof of Paper 9's revised Introduction and its cited sources.

This is an editorial review proof, not a replacement for pdflatex/BibTeX. The
Overleaf-ready manuscript remains OVERLEAF/manuscript.tex.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
OVERLEAF = PACKAGE / "OVERLEAF"
INTRO_PATH = OVERLEAF / "sections" / "sec01_intro.tex"
BIB_PATH = OVERLEAF / "references.bib"
OUT_PATH = HERE / "Introduction_Review_Preview.pdf"


def extract_bib_entries(text: str) -> list[str]:
    entries: list[str] = []
    pos = 0
    while True:
        match = re.search(r"@\w+\s*\{", text[pos:])
        if not match:
            break
        start = pos + match.start()
        opening = pos + match.end() - 1
        depth = 0
        for i in range(opening, len(text)):
            char = text[i]
            escaped = i > 0 and text[i - 1] == "\\"
            if char == "{" and not escaped:
                depth += 1
            elif char == "}" and not escaped:
                depth -= 1
                if depth == 0:
                    entries.append(text[start : i + 1])
                    pos = i + 1
                    break
        else:
            raise ValueError("Unbalanced braces in references.bib")
    return entries


def bib_key(entry: str) -> str:
    match = re.match(r"@\w+\s*\{\s*([^,]+)", entry)
    if not match:
        raise ValueError("Could not read a BibTeX key")
    return match.group(1).strip()


def bib_fields(entry: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    key_match = re.match(r"@\w+\s*\{\s*[^,]+,", entry)
    if not key_match:
        return fields
    text = entry[key_match.end() : -1]
    field_start = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*")
    cursor = 0
    while True:
        match = field_start.search(text, cursor)
        if not match:
            break
        name = match.group(1).lower()
        value_start = match.end()
        if value_start >= len(text):
            break
        opener = text[value_start]
        if opener == "{":
            depth = 0
            i = value_start
            while i < len(text):
                char = text[i]
                escaped = i > 0 and text[i - 1] == "\\"
                if char == "{" and not escaped:
                    depth += 1
                elif char == "}" and not escaped:
                    depth -= 1
                    if depth == 0:
                        fields[name] = text[value_start + 1 : i].strip()
                        cursor = i + 1
                        break
                i += 1
            else:
                raise ValueError(f"Unbalanced value in BibTeX field {name}")
        elif opener == '"':
            i = value_start + 1
            while i < len(text):
                if text[i] == '"' and text[i - 1] != "\\":
                    fields[name] = text[value_start + 1 : i].strip()
                    cursor = i + 1
                    break
                i += 1
            else:
                raise ValueError(f"Unbalanced quoted value in BibTeX field {name}")
        else:
            end = text.find(",", value_start)
            if end < 0:
                end = len(text)
            fields[name] = text[value_start:end].strip()
            cursor = end + 1
    return fields


def tex_plain(value: str) -> str:
    """Remove the common BibTeX/LaTeX wrappers while preserving readable text."""
    replacements = {
        r"\&": "&",
        r"\%": "%",
        r"\_": "_",
        r"\#": "#",
        r"\$": "$",
        r"\'e": "é",
        r"\'a": "á",
        r"\'i": "í",
        r"\'o": "ó",
        r"\'u": "ú",
        r"\"u": "ü",
        r"\"o": "ö",
        r"\"a": "ä",
        r"\~n": "ñ",
        r"\c{c}": "ç",
        r"\ss": "ß",
        "---": "—",
        "--": "–",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    # Common BibTeX title wrappers, including a single nested group.
    wrapper = re.compile(r"\\(?:textit|textbf|emph|mathrm|mathbf|bm|text|textrm|texttt)\{([^{}]*)\}")
    prior = None
    while prior != value:
        prior = value
        value = wrapper.sub(r"\1", value)
    value = re.sub(r"\\[A-Za-z]+", "", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def intro_citations_and_order(tex: str) -> tuple[str, list[str], dict[str, int]]:
    cite_pattern = re.compile(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}")
    order: list[str] = []
    number: dict[str, int] = {}

    def replace_cite(match: re.Match[str]) -> str:
        keys = [part.strip() for part in match.group(1).split(",") if part.strip()]
        for key in keys:
            if key not in number:
                number[key] = len(number) + 1
                order.append(key)
        nums = sorted({number[key] for key in keys})
        return "[" + ", ".join(str(n) for n in nums) + "]"

    return cite_pattern.sub(replace_cite, tex), order, number


def latex_to_readable(text: str) -> list[tuple[str, str]]:
    """Return ordered paragraph and contribution-list blocks from the Introduction."""
    text = re.sub(r"(?m)^\s*\\section\{[^}]*\}\s*$", "", text)
    text = re.sub(r"(?m)^\s*\\label\{[^}]*\}\s*$", "", text)
    text = re.sub(r"\\ref\{app:asymptotics\}", "A", text)
    section_refs = {
        "sec:continuum": "2",
        "sec:bloch": "3",
        "sec:fem": "4",
        "sec:verification": "5",
        "sec:results": "6",
        "sec:steering": "7",
        "sec:discussion": "8",
        "sec:conclusions": "9",
    }
    for label, value in section_refs.items():
        text = text.replace(r"\ref{" + label + "}", value)

    text = re.sub(r"\\begin\{enumerate\}(?:\[[^\]]*\])?", "\n__LIST_START__\n", text)
    text = re.sub(r"\\end\{enumerate\}", "\n__LIST_END__\n", text)
    text = re.sub(r"\\item\s*", "\n__ITEM__", text)

    def replace_braced_macro(source: str, macro: str, wrap) -> str:
        pattern = re.compile(r"\\" + re.escape(macro) + r"\{")
        while True:
            match = pattern.search(source)
            if not match:
                return source
            opening = match.end() - 1
            depth = 0
            closing = None
            for pos in range(opening, len(source)):
                if source[pos] == "{":
                    depth += 1
                elif source[pos] == "}":
                    depth -= 1
                    if depth == 0:
                        closing = pos
                        break
            if closing is None:
                return source
            inside = source[opening + 1 : closing]
            source = source[: match.start()] + wrap(inside) + source[closing + 1 :]

    # Preserve the square-root operation as readable plain text before unwrapping math.
    text = replace_braced_macro(text, "sqrt", lambda value: "sqrt(" + value + ")")
    command_map = {
        r"\theta": "theta",
        r"\ell": "ell ",
        r"\mu": "mu",
        r"\rho": "rho ",
        r"\Delta": "Delta",
        r"\Gamma": "Gamma",
        r"\infty": "infinity",
        r"\mathrm": "",
        r"\mathbf": "",
        r"\bm": "",
        r"\text": "",
        r"\textbf": "",
        r"\emph": "",
        r"\textrm": "",
        r"\textit": "",
        r"\times": " x ",
        r"\to": " to ",
        r"\le": "<=",
        r"\ge": ">=",
        r"\in": " in ",
        r"\approx": "about",
        r"\,": " ",
        r"\;": " ",
        r"\!": "",
        r"\&": "&",
        r"\%": "%",
        r"\_": "_",
    }
    for command, replacement in command_map.items():
        text = text.replace(command, replacement)
    for _ in range(3):
        text = re.sub(r"\\(?:mathrm|mathbf|bm|text|textbf|emph|textrm|textit)\{([^{}]*)\}", r"\1", text)
    text = text.replace("$", "")
    text = text.replace("~", " ")
    text = text.replace("\\\\", " ")
    text = text.replace("---", "—").replace("--", "–")
    text = re.sub(r"\\[A-Za-z]+", "", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+([_^])", r"\1", text)
    text = re.sub(r"\s+([,.;:)}\]])", r"\1", text)

    blocks: list[tuple[str, str]] = []
    current = ""
    in_list = False

    def flush() -> None:
        nonlocal current
        for fragment in re.split(r"\n\s*\n", current):
            clean = re.sub(r"\s+", " ", fragment).strip()
            if clean:
                blocks.append(("item" if in_list else "paragraph", clean))
        current = ""

    tokens = re.split(r"(__LIST_START__|__LIST_END__|__ITEM__)", text)
    for token in tokens:
        if token == "__LIST_START__":
            flush()
            in_list = True
        elif token == "__LIST_END__":
            flush()
            in_list = False
        elif token == "__ITEM__":
            flush()
            in_list = True
        else:
            current += token
    flush()
    return blocks


def make_reference(fields: dict[str, str]) -> str:
    authors = fields.get("author") or fields.get("editor") or ""
    author_text = tex_plain(authors).replace(" and ", "; ")
    title = tex_plain(fields.get("title", ""))
    year = tex_plain(fields.get("year", ""))
    journal = tex_plain(fields.get("journal", ""))
    booktitle = tex_plain(fields.get("booktitle", ""))
    publisher = tex_plain(fields.get("publisher", ""))
    volume = tex_plain(fields.get("volume", ""))
    number = tex_plain(fields.get("number", ""))
    pages = tex_plain(fields.get("pages", ""))
    doi = tex_plain(fields.get("doi", ""))

    source = journal or booktitle or publisher
    details = []
    if volume:
        details.append(volume + (f"({number})" if number else ""))
    if pages:
        details.append(pages)
    bits = [f"{author_text} ({year}). {title}."]
    if source:
        bits.append(source + (" " + ", ".join(details) if details else ""))
    if doi:
        bits.append("https://doi.org/" + doi)
    return ". ".join(bit.rstrip(".") for bit in bits if bit)


def on_page(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#D7DFE8"))
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, height - 15 * mm, width - 18 * mm, height - 15 * mm)
    canvas.setFont("Times-Roman", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(18 * mm, height - 11 * mm, "PAPER 9  |  INTRODUCTION REVIEW PROOF")
    canvas.drawString(18 * mm, 10 * mm, "Introduction only — not a full LaTeX manuscript build")
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def main() -> None:
    intro_source = INTRO_PATH.read_text(encoding="utf-8")
    bib_text = BIB_PATH.read_text(encoding="utf-8")
    entries = {bib_key(entry): bib_fields(entry) for entry in extract_bib_entries(bib_text)}
    cited_intro, citation_order, _ = intro_citations_and_order(intro_source)
    if len(citation_order) != 50:
        raise SystemExit(f"Expected 50 unique Introduction citations; found {len(citation_order)}")
    missing = [key for key in citation_order if key not in entries]
    if missing:
        raise SystemExit("Missing bibliography entries: " + ", ".join(missing))

    blocks = latex_to_readable(cited_intro)
    contribution_count = sum(kind == "item" for kind, _ in blocks)
    if contribution_count != 4:
        raise SystemExit(f"Expected four contribution items; found {contribution_count}")
    if re.search(r"\\begin\{table\*?\}|\\input\{tables/", intro_source):
        raise SystemExit("A table/input remains in the Introduction source")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReviewTitle", parent=styles["Title"], fontName="Times-Bold",
        fontSize=20, leading=24, textColor=colors.HexColor("#17365D"),
        alignment=TA_LEFT, spaceAfter=5,
    )
    subtitle_style = ParagraphStyle(
        "ReviewSubtitle", parent=styles["Normal"], fontName="Times-Italic",
        fontSize=11, leading=15, textColor=colors.HexColor("#475569"), spaceAfter=10,
    )
    note_style = ParagraphStyle(
        "ReviewNote", parent=styles["Normal"], fontName="Times-Roman",
        fontSize=9, leading=12, textColor=colors.HexColor("#334155"),
        backColor=colors.HexColor("#F1F5F9"), borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5, borderPadding=7, spaceBefore=2, spaceAfter=12,
    )
    body_style = ParagraphStyle(
        "ReviewBody", parent=styles["BodyText"], fontName="Times-Roman",
        fontSize=10.2, leading=13.3, alignment=TA_JUSTIFY,
        firstLineIndent=13, spaceAfter=7, textColor=colors.HexColor("#111827"),
        allowWidows=0, allowOrphans=0,
    )
    contribution_style = ParagraphStyle(
        "Contribution", parent=body_style, leftIndent=18, firstLineIndent=-18,
        spaceAfter=7,
    )
    section_style = ParagraphStyle(
        "ReviewSection", parent=styles["Heading1"], fontName="Times-Bold",
        fontSize=15, leading=18, textColor=colors.HexColor("#17365D"),
        spaceBefore=3, spaceAfter=10,
    )
    ref_style = ParagraphStyle(
        "RefEntry", parent=styles["Normal"], fontName="Times-Roman",
        fontSize=8.5, leading=10.5, leftIndent=18, firstLineIndent=-18,
        spaceAfter=4, alignment=TA_LEFT, textColor=colors.HexColor("#111827"),
        allowWidows=0, allowOrphans=0,
    )
    small_style = ParagraphStyle(
        "SmallNote", parent=styles["Normal"], fontName="Times-Italic",
        fontSize=8.5, leading=11, textColor=colors.HexColor("#64748B"),
        spaceAfter=8,
    )

    story = [
        Spacer(1, 5 * mm),
        Paragraph("Paper 9 — Introduction", title_style),
        Paragraph("First-pass review copy · FEM3-inspired numeric citation style", subtitle_style),
        HRFlowable(width="100%", thickness=1.1, color=colors.HexColor("#1F4E79"), spaceAfter=10),
        Paragraph(
            "<b>Review scope:</b> table-free Introduction; 50 unique sources cited in the Introduction. "
            "The section source and separate BibTeX file are the editable authority. This PDF is an "
            "Introduction-only reading proof, not the compiled full manuscript.",
            note_style,
        ),
        Paragraph("Introduction", section_style),
    ]

    contribution_index = 0
    for kind, block in blocks:
        escaped = html.escape(block, quote=False)
        if kind == "item":
            contribution_index += 1
            story.append(Paragraph(f"<b>C{contribution_index}.</b> {escaped}", contribution_style))
        else:
            story.append(Paragraph(escaped, body_style))

    story.extend([
        PageBreak(),
        Paragraph("References cited in the Introduction", section_style),
        Paragraph(
            "Numbering follows first-citation order in the current LaTeX source. "
            "The `.bib` file remains the machine-readable reference source.",
            small_style,
        ),
    ])
    for idx, key in enumerate(citation_order, 1):
        ref = html.escape(make_reference(entries[key]), quote=False)
        story.append(Paragraph(f"<b>[{idx}]</b> {ref}", ref_style))

    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=A4,
        rightMargin=19 * mm, leftMargin=19 * mm,
        topMargin=22 * mm, bottomMargin=17 * mm,
        title="Paper 9 — Introduction Review Proof",
        author="Paper 9 editorial review",
        subject="Table-free introduction with 50 cited references",
    )
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"Wrote {OUT_PATH}")
    print(f"Introduction citations: {len(citation_order)} unique sources")
    print(f"Bibliography entries available: {len(entries)}")


if __name__ == "__main__":
    main()
