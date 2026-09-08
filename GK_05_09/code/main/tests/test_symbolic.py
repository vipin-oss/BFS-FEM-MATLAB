"""Run the SymPy cross-check as part of the test suite (Step 4)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.symbolic import run_all


def test_all_symbolic_identities():
    res = run_all()
    bad = [r for r in res if r["status"] != "PASS"]
    assert not bad, f"symbolic failures: {[(r['id'], r['equation']) for r in bad]}"
    assert len(res) >= 23
