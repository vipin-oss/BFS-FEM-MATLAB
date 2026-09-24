#!/usr/bin/env python3
"""P12S Phase C — panel extraction and plot-box detection for the published benchmarks.

Digitisation here is used ONLY as a graphical-registration tool (Blueprint v1.5 A2.5):
locating the published curve pixels so that an independently reproduced curve can be drawn
on top of the published panel.  No residual computed from this step may be reported as a
validation error percentage.

Panels (from the authoritative PDFs already in the repository):
  B1, B2 : paper9/analytic/li2024/s41598-024-75049-1.pdf  page 9  (Fig. 2, panels a and b)
  B3     : paper9/analytic/li2023/17455030.2023.2222189.pdf page 15 (Fig. 4, panel c)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

EXTRACT = Path("/home/user/p12s_extract")
OUT = Path(__file__).resolve().parents[2] / "paper9" / "audit" / "evidence" / "p12s"
OUT.mkdir(parents=True, exist_ok=True)

P12S_PANELS = {
    "B1": dict(src=EXTRACT / "li2024_p9_0_Im0.jpg", axis="row", index=0, xlim=(-1.0, 1.0), ylim=(0.0, 2.0)),
    "B2": dict(src=EXTRACT / "li2024_p9_0_Im0.jpg", axis="row", index=1, xlim=(-1.0, 1.0), ylim=(0.0, 2.0)),
    "B3": dict(src=EXTRACT / "li2023_p15_1_Im1.png", axis="col", index=2, xlim=(-1.0, 1.0), ylim=(0.0, 2.0)),
}


def _dark(a: np.ndarray, thr: int = 110) -> np.ndarray:
    return a < thr


def _long_runs(v: np.ndarray, thr: float) -> list[tuple[int, int]]:
    """Contiguous runs where v exceeds thr (axis-line detection)."""
    mask = v > thr
    out, s = [], None
    for i, m in enumerate(mask):
        if m and s is None:
            s = i
        elif not m and s is not None:
            out.append((s, i)); s = None
    if s is not None:
        out.append((s, len(mask)))
    return [r for r in out if r[1] - r[0] >= 2]


def detect_panels(img: np.ndarray, axis: str, n: int = 3):
    """Detect n panels and each panel's plot box on a full multi-panel figure.

    ``axis`` is the direction in which the panels are stacked ("row" for vertically
    stacked panels, "col" for side-by-side panels).  The axis lines of every panel form
    long runs in the *other* direction, so the split direction is found from the runs of
    the perpendicular axis lines.
    """
    dark = _dark(img)
    split_prof = dark.sum(axis=1 if axis == "row" else 0)      # profile along split axis
    perp_prof = dark.sum(axis=0 if axis == "row" else 1)       # profile along axis-line direction
    split_lines = _long_runs(split_prof, 0.5 * split_prof.max())
    # merge adjacent runs into one axis line
    merged = []
    for s, e in split_lines:
        if merged and s - merged[-1][1] <= 6:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    assert len(merged) >= 2 * n, f"expected >= {2*n} split-axis lines, found {len(merged)}"
    boxes = []
    for k in range(n):
        lo, hi = merged[2 * k][0], merged[2 * k + 1][1]
        band = dark[lo:hi, :] if axis == "row" else dark[:, lo:hi]
        prof = band.sum(axis=0 if axis == "row" else 1)
        lines = _long_runs(prof, 0.5 * prof.max())
        m2 = []
        for s, e in lines:
            if m2 and s - m2[-1][1] <= 6:
                m2[-1] = (m2[-1][0], e)
            else:
                m2.append((s, e))
        assert len(m2) >= 2, f"panel {k}: could not find its cross-axis lines ({len(m2)})"
        left, right = m2[0][0], m2[-1][1]
        panel = img[lo:hi, left:right] if axis == "row" else img[left:right, lo:hi]
        box = (0, right - left, 0, hi - lo) if axis == "row" else (0, hi - lo, 0, right - left)
        boxes.append(dict(panel=panel, box=box, crop=(lo, hi, left, right)))
    return boxes


def panel_arrays() -> dict:
    """Return, per benchmark, the cropped panel and the pixel<->data transform."""
    out = {}
    for bid, cfg in P12S_PANELS.items():
        full = np.asarray(Image.open(cfg["src"]).convert("L"))
        boxes = detect_panels(full, cfg["axis"], n=3)
        b = boxes[cfg["index"]]
        panel = b["panel"]
        left, right, top, bottom = b["box"]
        (x0, x1), (y0, y1) = cfg["xlim"], cfg["ylim"]
        out[bid] = dict(panel=panel, box=(left, right, top, bottom),
                        crop=b["crop"], xlim=cfg["xlim"], ylim=cfg["ylim"],
                        src=cfg["src"].name,
                        transform=dict(px_x0=left, px_x1=right, px_y0=top, px_y1=bottom,
                                       x0=x0, x1=x1, y0=y0, y1=y1))
        Image.fromarray(panel).save(OUT / f"{bid}_panel.png")
        print(f"  {bid}: panel {panel.shape} box(l,r,t,b)={(left,right,top,bottom)} "
              f"x:{x0}..{x1} y:{y0}..{y1}  <- {cfg['src'].name}")
    return out


def data_to_px(tr: dict, x: np.ndarray, y: np.ndarray):
    px = tr["px_x0"] + (np.asarray(x) - tr["x0"]) / (tr["x1"] - tr["x0"]) * (tr["px_x1"] - tr["px_x0"])
    py = tr["px_y1"] - (np.asarray(y) - tr["y0"]) / (tr["y1"] - tr["y0"]) * (tr["px_y1"] - tr["px_y0"])
    return px, py


def px_to_data(tr: dict, px: np.ndarray, py: np.ndarray):
    x = tr["x0"] + (np.asarray(px) - tr["px_x0"]) / (tr["px_x1"] - tr["px_x0"]) * (tr["x1"] - tr["x0"])
    y = tr["y0"] + (tr["px_y1"] - np.asarray(py)) / (tr["px_y1"] - tr["px_y0"]) * (tr["y1"] - tr["y0"])
    return x, y


if __name__ == "__main__":
    print("P12S panel extraction / plot-box detection")
    panels = panel_arrays()
    (OUT / "panels.json").write_text(json.dumps(
        {b: {k: (v if k != "panel" else None) for k, v in p.items()} for b, p in panels.items()},
        indent=1, default=str))
    print(f"  written: {OUT}/<BID>_panel.png and panels.json")
