#!/usr/bin/env python3
"""Make PNG page previews of the PDF using ImageMagick's text/vector renderer."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
PDF = HERE / "PlanB_Progress_Report.pdf"
OUTDIR = HERE / "preview"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SCALE = 2
PAGE_H = 842


def rgb(r: str, g: str, b: str) -> str:
    return "#" + "".join(f"{round(float(v) * 255):02x}" for v in (r, g, b))


def im_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def render_page(stream: bytes, page_num: int, output: Path) -> None:
    ops = stream.decode("ascii").splitlines()
    current_fill = "#000000"
    args = ["convert", "-size", f"{595*SCALE}x{842*SCALE}", "xc:white", "-antialias"]
    for op in ops:
        m = re.fullmatch(r"([0-9.]+) ([0-9.]+) ([0-9.]+) rg", op)
        if m:
            current_fill = rgb(*m.groups())
            continue
        m = re.fullmatch(r"([0-9.]+) ([0-9.]+) ([0-9.]+) ([0-9.]+) re f", op)
        if m:
            x, y, w, h = map(float, m.groups())
            x1, y1 = x*SCALE, (PAGE_H-y-h)*SCALE
            x2, y2 = (x+w)*SCALE, (PAGE_H-y)*SCALE
            args += ["-fill", current_fill, "-draw", f"rectangle {x1:g},{y1:g} {x2:g},{y2:g}"]
            continue
        m = re.fullmatch(r"([0-9.]+) ([0-9.]+) ([0-9.]+) RG ([0-9.]+) w ([0-9.]+) ([0-9.]+) ([0-9.]+) ([0-9.]+) re S", op)
        if m:
            r, g, b, sw, x, y, w, h = map(float, m.groups())
            x1, y1 = x*SCALE, (PAGE_H-y-h)*SCALE
            x2, y2 = (x+w)*SCALE, (PAGE_H-y)*SCALE
            args += ["-stroke", rgb(str(r),str(g),str(b)), "-strokewidth", str(sw*SCALE), "-fill", "none", "-draw", f"rectangle {x1:g},{y1:g} {x2:g},{y2:g}"]
            continue
        m = re.fullmatch(r"([0-9.]+) ([0-9.]+) ([0-9.]+) RG ([0-9.]+) w ([0-9.]+) ([0-9.]+) m ([0-9.]+) ([0-9.]+) l S", op)
        if m:
            r, g, b, sw, x1, y1, x2, y2 = map(float, m.groups())
            args += ["-stroke", rgb(str(r),str(g),str(b)), "-strokewidth", str(sw*SCALE), "-draw", f"line {x1*SCALE:g},{(PAGE_H-y1)*SCALE:g} {x2*SCALE:g},{(PAGE_H-y2)*SCALE:g}"]
            continue
        m = re.fullmatch(r"([0-9.]+) ([0-9.]+) ([0-9.]+) rg BT /(F1|F2) ([0-9.]+) Tf 1 0 0 1 ([0-9.-]+) ([0-9.-]+) Tm \((.*)\) Tj ET", op)
        if m:
            r, g, b, font, size, x, y, raw = m.groups()
            text = re.sub(r"\\([\\()])", r"\1", raw)
            x_px, y_px = float(x)*SCALE, (PAGE_H-float(y))*SCALE
            weight_font = FONT.replace("DejaVuSans.ttf", "DejaVuSans-Bold.ttf") if font == "F2" else FONT
            args += ["-font", weight_font, "-pointsize", str(round(float(size)*SCALE)), "-fill", rgb(r,g,b), "-stroke", "none", "-draw", f"text {x_px:g},{y_px:g} '{im_escape(text)}'"]
    args.append(str(output))
    subprocess.run(args, check=True)


def main() -> None:
    OUTDIR.mkdir(exist_ok=True)
    raw = PDF.read_bytes()
    streams = re.findall(rb"stream\n(.*?)\nendstream", raw, re.S)
    if len(streams) != 3:
        raise RuntimeError(f"Expected 3 page streams, found {len(streams)}")
    for i, stream in enumerate(streams, 1):
        output = OUTDIR / f"PlanB_Progress_Page{i}.png"
        render_page(stream, i, output)
        print(output)


if __name__ == "__main__":
    main()
