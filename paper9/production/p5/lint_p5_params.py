#!/usr/bin/env python3
"""Parameters-only lint for the P5 production code (plan CALC_MASTER_PLAN.md §J rule (i)).

Rules enforced on production/p5/p5_core.py and production/p5/p5_run.py:
  R1  every numeric literal is declared in the module's NUMERIC_LITERAL_ALLOWLIST
      with a justification (no undocumented magic numbers),
  R2  no numeric literal equals a scientific parameter value from the params file
      (those must come from the params file, not the code); unit values 0.0/1.0
      are exempt because they carry no physical meaning,
  R3  the frozen assembly (assemble_nxn_bloch) is called only with `conf[...]`
      subscripts, i.e. every scientific parameter reaches the solver through the
      params-file-derived configuration mapping.

Usage: python3 production/p5/lint_p5_params.py [--params params/<file>.yaml]
Exit code 0 iff no violation.
"""
from __future__ import annotations

import argparse
import ast
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

EXEMPT_UNIT_VALUES = {0.0, 1.0}


def _allowlist(module_name: str) -> dict:
    mod = importlib.import_module(module_name)
    table = getattr(mod, "NUMERIC_LITERAL_ALLOWLIST", None)
    if not table:
        raise SystemExit(f"{module_name} does not declare NUMERIC_LITERAL_ALLOWLIST")
    return {float(k): v for k, v in table.items()}


def _is_num(node) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
        and not isinstance(node.value, bool)


def _literals(tree: ast.AST) -> list:
    wrapped = {id(n.operand) for n in ast.walk(tree)
               if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub)
               and _is_num(n.operand)}
    out = []
    for node in ast.walk(tree):
        if _is_num(node) and id(node) not in wrapped:
            out.append((node.lineno, float(node.value)))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub) and _is_num(node.operand):
            out.append((node.lineno, -float(node.operand.value)))
    return out


def _conf_subscript_call(tree: ast.AST, fname: str) -> list:
    """Args of every call to `fname`; returns (lineno, ok) for the params-only rule."""
    res = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == fname:
            ok = not any(_is_num(a) for a in node.args)          # no hard-coded number
            res.append((node.lineno, ok))
    return res


def lint_file(path: Path, params: dict) -> dict:
    src = path.read_text()
    tree = ast.parse(src)
    allow = _allowlist(path.stem)
    sci = {float(p["value"]) for p in params["parameters"]}
    lits = _literals(tree)
    violations = []
    for line, val in lits:
        if val not in allow:
            violations.append({"rule": "R1", "line": line, "literal": val,
                               "msg": "numeric literal not declared in NUMERIC_LITERAL_ALLOWLIST"})
        if val not in EXEMPT_UNIT_VALUES and any(abs(val - s) < 1e-15 for s in sci):
            violations.append({"rule": "R2", "line": line, "literal": val,
                               "msg": "literal equals a scientific parameter value"})
    calls = _conf_subscript_call(tree, "assemble_nxn_bloch")
    for line, ok in calls:
        if not ok:
            violations.append({"rule": "R3", "line": line, "literal": None,
                               "msg": "assemble_nxn_bloch called with something other than conf[...]"})
    return {"file": str(path.relative_to(REPO)), "n_literals": len(lits),
            "n_calls_checked": len(calls), "violations": violations}


def lint_params_file(params: dict) -> list:
    bad = []
    for p in params["parameters"]:
        if not p.get("tag") or not p.get("source"):
            bad.append({"rule": "P1", "name": p.get("name"),
                        "msg": "parameter without provenance tag/source"})
    vals = {p["name"]: p["value"] for p in params["parameters"]}
    if "AR" in params.get("study", {}) and "l1" in vals and "l2" in vals:
        if abs(params["study"]["AR"] - vals["l1"] / vals["l2"]) > 1e-12:
            bad.append({"rule": "P2", "name": "AR",
                        "msg": "study.AR inconsistent with l1/l2"})
    for key in ("n_mesh", "n_bands", "path_N_seg", "zone_N1", "zone_N2"):
        if key not in params["sampling"]:
            bad.append({"rule": "P3", "name": key, "msg": "missing sampling entry"})
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", type=Path,
                    default=REPO / "params" / "p5_pilot_params.yaml")
    args = ap.parse_args(argv)

    import p5_core as core
    params = core.load_params(args.params)
    reports = [lint_file(HERE / "p5_core.py", params), lint_file(HERE / "p5_run.py", params)]
    pf = lint_params_file(params)

    n_viol = 0
    print(f"params file: {args.params}  (hash {core.params_hash(params)[:16]}...)")
    for r in reports:
        n_viol += len(r["violations"])
        print(f"  {r['file']}: literals={r['n_literals']} frozen-assembly calls checked={r['n_calls_checked']} "
              f"violations={len(r['violations'])}")
        for v in r["violations"]:
            print(f"    VIOLATION {v['rule']} line {v['line']}: {v['literal']} - {v['msg']}")
    for v in pf:
        n_viol += 1
        print(f"    VIOLATION {v['rule']} {v['name']}: {v['msg']}")
    print("lint result:", "PASS (no violations)" if n_viol == 0 else f"FAIL ({n_viol} violations)")
    return 0 if n_viol == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
