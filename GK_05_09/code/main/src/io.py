"""Result serialisation with provenance."""
from __future__ import annotations
import json, subprocess, datetime, platform
from pathlib import Path
import numpy as np

# Program root is the enclosing package folder (code/main). Scientific input
# data live in the central data/ tree so the package can be laid out as
#   manuscript/  code/  data/  (see the top-level README).
ROOT      = Path(__file__).resolve().parent.parent   # .../code/main
PROJECT   = ROOT.parent.parent                       # .../  (package root)
INPUT_DIR = PROJECT / "data" / "input"               # digitised source data (read-only)
RESULTS = ROOT / "results"
ACCEPT  = ROOT / "acceptance"
FIGS    = ROOT / "figures"
for _p in (RESULTS, ACCEPT, FIGS):
    _p.mkdir(exist_ok=True)

SOURCE_DOC = "manuscript/GK_COMPLETE_CALCULATIONS.tex"


def git_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "not-a-git-repo"


def provenance():
    return {"source_document": SOURCE_DOC,
            "git_commit": git_commit(),
            "timestamp_utc": datetime.datetime.now(
                datetime.timezone.utc).isoformat(timespec="seconds"),
            "python": platform.python_version(),
            "numpy": np.__version__}


class _Enc(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            v = float(o)
            return v if np.isfinite(v) else str(v)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return super().default(o)


def save_json(path, payload):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    body = {"provenance": provenance(), "data": payload}
    p.write_text(json.dumps(body, indent=2, cls=_Enc))
    return p


def save_csv(path, rows, header):
    import csv
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return p
