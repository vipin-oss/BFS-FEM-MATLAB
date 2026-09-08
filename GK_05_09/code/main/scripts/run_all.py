"""Run everything: symbolic checks, unit tests, acceptance, analysis, figures."""
from __future__ import annotations
import subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
STEPS = [
    ("symbolic cross-check", [sys.executable, "-c",
        "import sys;sys.path.insert(0,'.');from src.symbolic import run_all;"
        "r=run_all();bad=[x for x in r if x['status']!='PASS'];"
        "print(f'symbolic: {len(r)-len(bad)}/{len(r)} PASS');"
        "sys.exit(1 if bad else 0)"]),
    ("unit tests", [sys.executable, "-m", "pytest", "tests/", "-q"]),
    ("acceptance T1-T24", [sys.executable, "scripts/run_acceptance.py"]),
    ("validation", [sys.executable, "scripts/run_validation.py"]),
    ("analysis", [sys.executable, "scripts/run_analysis.py"]),
    ("figures", [sys.executable, "scripts/generate_figures.py"]),
]
fail = []
for name, cmd in STEPS:
    print("\n" + "=" * 92); print(f"RUN: {name}"); print("=" * 92, flush=True)
    t0 = time.time()
    rc = subprocess.call(cmd, cwd=str(ROOT))
    print(f"-- {name}: {'OK' if rc == 0 else 'FAILED'} ({time.time()-t0:.1f}s)")
    if rc != 0:
        fail.append(name)
print("\n" + "=" * 92)
print("PIPELINE FAILURES:", fail if fail else "NONE")
sys.exit(1 if fail else 0)
