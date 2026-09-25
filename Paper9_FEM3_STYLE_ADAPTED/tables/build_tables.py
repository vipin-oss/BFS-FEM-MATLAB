#!/usr/bin/env python3
"""Build the FEM_3-style table fragments and numeric bibliography for the
Paper9_FEM3_STYLE_ADAPTED package.

Writes:
  OVERLEAF/tables/*.tex  -- 7 active table fragments, byte-identical to the
                            authoritative Paper9 tables/out/ fragments.
  tables_rebuilt/*.tex    -- mirrored working copies for the report/audit.

Implementation: loads the authoritative byte-fragments from the package's
PROGRAM/paper9/tables/out/ tree and writes them verbatim.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
STOCK = os.path.join(PKG, "PROGRAM", "paper9", "tables", "out")
OUT_ACTIVE = os.path.join(PKG, "OVERLEAF", "tables")
OUT_WORK = os.path.join(HERE, "tables_rebuilt")

TABLE_IDS = [
    "tab01_literature_positioning",
    "tab02_parameters",
    "tab03_anchor_errors",
    "tab04_consistency_suite",
    "tab05_gap_summary",
    "tab06_convergence_floor",
    "tab07_steering_sweep",
]


def build_table(path):
    with open(path, "r", encoding="utf-8") as f:
        frag = f.read()
    return frag


def main():
    missing = [t for t in TABLE_IDS if not os.path.exists(os.path.join(STOCK, t + ".tex"))]
    if missing:
        print("ABORT: authoritative table fragments not found:", ", ".join(missing))
        sys.exit(2)
    os.makedirs(OUT_ACTIVE, exist_ok=True)
    os.makedirs(OUT_WORK, exist_ok=True)
    for tid in TABLE_IDS:
        frag = build_table(os.path.join(STOCK, tid + ".tex"))
        with open(os.path.join(OUT_ACTIVE, tid + ".tex"), "w", encoding="utf-8") as f:
            f.write(frag)
        with open(os.path.join(OUT_WORK, tid + ".tex"), "w", encoding="utf-8") as f:
            f.write(frag)
        print("built", tid + ".tex", len(frag), "chars")


if __name__ == "__main__":
    main()
