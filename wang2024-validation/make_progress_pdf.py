#!/usr/bin/env python3
"""Create a dependency-free, readable Hinglish PDF progress report."""
from __future__ import annotations

import textwrap
from pathlib import Path

OUT = Path(__file__).with_name("PlanB_Progress_Report.pdf")
W, H = 595.0, 842.0
NAVY = (0.08, 0.17, 0.29)
BLUE = (0.10, 0.37, 0.62)
PALE = (0.93, 0.96, 0.99)
INK = (0.13, 0.17, 0.22)
MUTED = (0.35, 0.40, 0.47)
GREEN = (0.10, 0.43, 0.32)
AMBER = (0.70, 0.39, 0.05)
RED = (0.65, 0.19, 0.19)


def pdf_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class Page:
    def __init__(self, number: int):
        self.number = number
        self.ops: list[str] = []
        self.y = 786.0
        self._rect(0, 0, W, H, (1, 1, 1))
        self._rect(0, 792, W, 50, NAVY)
        self.text(42, 811, "PLAN B | EXECUTION UPDATE", 10, True, (1, 1, 1))
        self.text(42, 780, "Thermal-shock validation study  |  Progress report", 8, False, MUTED)

    def _rect(self, x: float, y: float, w: float, h: float, color: tuple[float, float, float], stroke=None):
        r, g, b = color
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        if stroke is None:
            self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")
        else:
            sr, sg, sb = stroke
            self.ops.append(f"{sr:.3f} {sg:.3f} {sb:.3f} RG 0.8 w {x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")

    def text(self, x: float, y: float, s: str, size: float = 10, bold: bool = False, color=INK):
        r, g, b = color
        font = "F2" if bold else "F1"
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} rg BT /{font} {size:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({pdf_escape(s)}) Tj ET")

    def line(self, x1: float, y1: float, x2: float, y2: float, color=(0.82, 0.85, 0.89), width=0.7):
        r, g, b = color
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def heading(self, title: str, y: float | None = None):
        if y is None:
            y = self.y
        self.text(42, y, title, 15, True, NAVY)
        self.line(42, y - 7, 553, y - 7, (0.78, 0.83, 0.89), 1.0)
        self.y = y - 25

    def paragraph(self, text: str, x: float = 48, width: int = 88, size: float = 10, leading: float = 14, color=INK, bold=False):
        for raw in text.split("\n"):
            if not raw:
                self.y -= leading * 0.55
                continue
            lines = textwrap.wrap(raw, width=width, subsequent_indent="  ") or [""]
            for line in lines:
                self.text(x, self.y, line, size, bold, color)
                self.y -= leading
        self.y -= 2

    def bullet(self, text: str, width: int = 84, color=INK, size: float = 9.5, leading: float = 13):
        lines = textwrap.wrap(text, width=width, subsequent_indent="    ") or [text]
        self.text(50, self.y, "- " + lines[0], size, False, color)
        self.y -= leading
        for line in lines[1:]:
            self.text(61, self.y, line, size, False, color)
            self.y -= leading
        self.y -= 2

    def footer(self):
        self.line(42, 35, 553, 35, (0.84, 0.87, 0.90), 0.7)
        self.text(42, 21, "Plan B | Internal working update | No solver/experiment claims beyond this report", 7.5, False, MUTED)
        self.text(532, 21, str(self.number), 8, True, MUTED)

    def stream(self) -> bytes:
        self.footer()
        return ("\n".join(self.ops) + "\n").encode("ascii")


def table(page: Page, x: float, top: float, widths: list[float], headers: list[str], rows: list[list[str]], row_h: float = 34):
    total = sum(widths)
    page._rect(x, top - 27, total, 27, NAVY)
    cx = x
    for w, head in zip(widths, headers):
        page.text(cx + 7, top - 18, head, 8.2, True, (1, 1, 1))
        cx += w
    y = top - 27
    for ri, row in enumerate(rows):
        fill = PALE if ri % 2 == 0 else (1, 1, 1)
        page._rect(x, y - row_h, total, row_h, fill, (0.84, 0.87, 0.90))
        cx = x
        for w, cell in zip(widths, row):
            # Each cell is short by design; wrap lightly if needed.
            lines = textwrap.wrap(cell, width=max(10, int(w / 5.2)))
            yy = y - 13
            for line in lines[:2]:
                page.text(cx + 7, yy, line, 8.2, False, INK)
                yy -= 10
            cx += w
        y -= row_h
    return y


def make_pages() -> list[Page]:
    pages: list[Page] = []

    p = Page(1)
    p.text(42, 739, "Blueprint ka computational hissa execute hua", 20, True, NAVY)
    p.text(42, 714, "Seedhi baat: haan, software wala kaam chal raha hai; full fracture validation abhi nahi.", 10, False, MUTED)
    p._rect(42, 642, 511, 52, (0.91, 0.96, 0.93), (0.68, 0.82, 0.73))
    p.text(55, 674, "AB TAK KYA PASS HUA", 9, True, GREEN)
    p.text(55, 656, "Thermal code ke energy-balance, mesh/time refinement aur insulated-limit checks pass hue.", 9.3, False, INK)
    p.heading("Thermal model ke outputs", 616)
    p.paragraph("Public APDL ke h, radius aur thermal properties par 100 ms ka reduced radial calculation chalaya. Shock input 100 K APDL default tha; yeh ANSYS reproduction ya fracture prediction nahi hai.", width=86, size=9.3, leading=13)
    y = table(p, 42, 557, [173, 112, 112, 114], ["Case", "Center C", "Surface C", "Model"], [
        ["Alumina monolith", "99.685", "45.068", "radial FV"],
        ["ZTA monolith", "106.703", "40.180", "radial FV"],
        ["ZTA core + 0.4 mm Al shell", "105.458", "41.794", "radial FV*"],
    ], row_h=36)
    p.y = y - 18
    p.paragraph("*Shell thickness 0.4 mm article geometry se li gayi hai. Archived APDL geometry ise zero kar deti hai, isliye yeh independent thermal case hai, APDL run ka reproduction nahi.", width=88, size=8.5, leading=12, color=MUTED)
    p.heading("Aur kaun se checks hue?", p.y - 2)
    p.bullet("Shao sphere script rerun: 219.27 K, 548.32 K, 1290.95 K ke existing thresholds reproduce hue; comparison ab bhi coarse experimental text limits se hai.")
    p.bullet("Wang Appendix A algebra check rerun: published Eq. (A7) inconsistency wahi mili; yeh full PF-CZM solver test nahi hai.")
    p.text(42, 58, "Code: papsik_radial_thermal.py | Details: plan_b_execution_log.md", 8, True, BLUE)
    pages.append(p)

    p = Page(2)
    p.text(42, 739, "Full fracture run kyun nahi kiya?", 20, True, NAVY)
    p.text(42, 714, "Source files me kuch settings abhi uniquely traceable nahi hain.", 10, False, MUTED)
    p.heading("Reproduction se pehle 4 blockers", 675)
    p.bullet("Geometry: rod_height absent ho to APDL 5 mm default karta hai; article rod length 50 mm batata hai. Run command me 50 mm ka override documented nahi mila.", width=85)
    p.bullet("Layer: geometry file layer_thickness = 0 um set karti hai; 400 um shell ke liye source edit/override chahiye.", width=85)
    p.bullet("Temperature properties: 20 C row active hai; 320/620 C ke E aur expansion data commented out hain.", width=85)
    p.bullet("ZTA strength: APDL = 902 MPa, Weibull m=13.6; article Table 1 = 1025 MPa, m=5.3. Conversion/definition abhi unresolved hai.", width=85)
    p.bullet("Archive: metadata me CSV listed hai, par official preview HTTP 500 deta raha; ZIP/checksum locally verify nahi hue.", width=85)
    p.heading("Input sanity checks (not FEM)", p.y - 4)
    y = table(p, 42, p.y - 12, [126, 118, 118, 149], ["Material", "Diffusivity m2/s", "Biot number", "Gc J/m2"], [
        ["Alumina", "1.0202e-5", "3.6765", "25.403"],
        ["ZTA", "7.6140e-6", "5.6818", "46.181"],
    ], row_h=34)
    p.y = y - 22
    card_top = p.y - 8
    p._rect(42, card_top - 82, 511, 82, (1.00, 0.96, 0.91), (0.88, 0.74, 0.51))
    p.text(55, card_top - 19, "Interpretation", 10, True, AMBER)
    note = "Yeh differences paper galat hone ka proof nahi hain - kuch settings interactive ya undocumented ho sakti hain. Lekin guessed inputs se kiya run defensible reproduction nahi hoga, isliye fracture solver ko abhi rokna sahi hai."
    for j, line in enumerate(textwrap.wrap(note, width=82)):
        p.text(55, card_top - 38 - 12 * j, line, 8.7, False, INK)
    p.y = card_top - 98
    pages.append(p)

    p = Page(3)
    p.text(42, 739, "Agla kaam aur clear boundary", 20, True, NAVY)
    p.text(42, 714, "Execution status ko honestly separate rakha hai: kya run hua, kya pending hai.", 10, False, MUTED)
    p.heading("Computational next steps", 675)
    p.bullet("Official Zenodo archive/CSV ko readable download path se verify karna; phir material and parameter provenance lock karna.", width=86)
    p.bullet("Documented geometry/settings milne ke baad independent axisymmetric thermoelastic and crack-energy model banana; mesh/time/crack-step convergence dikhana.", width=86)
    p.bullet("Shao aur Papsik historical checks ko new prospective test se alag report karna. Published photos blind test nahi hain.", width=86)
    p.heading("Blueprint ki mandatory validation", p.y - 3)
    p.paragraph("Composite architecture ko predictively validate karne ke liye blueprint me prospective, blinded rod experiment rakha hai. Iske liye actual specimens, measured material properties, instrumented quench, aur lab ki zaroorat hai; yeh code repository se conduct nahi ho sakta.", width=86, size=9.3, leading=13)
    card_top = p.y - 8
    p._rect(42, card_top - 88, 511, 88, (0.97, 0.93, 0.93), (0.87, 0.70, 0.70))
    p.text(55, card_top - 20, "Abhi ke guardrails", 10, True, RED)
    guardrails = "No post-shock fitting. No author data request. No 3D simulation. Koi result Wang (2024) PF-CZM/FEM solver ko validate nahi karta. Q1 journal aim hai, acceptance guarantee nahi."
    for j, line in enumerate(textwrap.wrap(guardrails, width=84)):
        p.text(55, card_top - 40 - 13 * j, line, 9.0, False, INK)
    p.y = card_top - 105
    p.heading("Files", p.y - 3)
    p.bullet("plan_b_blueprint.md - complete research protocol and go/no-go gates.", width=86)
    p.bullet("plan_b_execution_log.md - executed checks, numerical outputs, and blockers.", width=86)
    p.bullet("papsik_radial_thermal.py - reduced thermal model; papsik_input_audit.py - input scale checks.", width=86)
    p.text(42, 58, "Source: Papsik et al. (2024), DOI 10.1016/j.engfracmech.2024.110121; Zenodo 13970234.", 7.8, False, MUTED)
    pages.append(p)

    return pages


def write_pdf(pages: list[Page], output: Path) -> None:
    # PDF objects: catalog=1, pages=2, Helvetica=3, Helvetica-Bold=4, then page/content pairs.
    objects: list[bytes] = [b""] * 4
    kids = []
    for page in pages:
        page_id = len(objects) + 1
        content_id = page_id + 1
        kids.append(f"{page_id} 0 R")
        stream = page.stream()
        page_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W:.0f} {H:.0f}] "
            "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")
        content_obj = f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"endstream"
        objects.extend([page_obj, content_obj])
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(pages)} >>".encode("ascii")
    objects[2] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    objects[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"

    data = bytearray(b"%PDF-1.4\n%PlanBProgress\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(data))
        data.extend(f"{idx} 0 obj\n".encode("ascii"))
        data.extend(obj)
        data.extend(b"\nendobj\n")
    xref_offset = len(data)
    data.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    data.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    data.extend(
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    output.write_bytes(data)


if __name__ == "__main__":
    write_pdf(make_pages(), OUT)
    print(OUT)
