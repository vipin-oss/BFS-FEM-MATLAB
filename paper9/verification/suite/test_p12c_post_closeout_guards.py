"""P12C post-closeout guards (Part G of the P12C forensic audit).

Pins the invariants that were previously only documented:

1. the five-mesh Case-C complete-gap series (4^2..64^2) and its monotonicity;
2. the series is computed, not interpolated (mid-point checks);
3. the successive decrements/ratios and the >=0.5 refinement-trigger record;
4. integrity of the 32^2/64^2 raw JSONs against their SHA-256 sidecars;
5. the non-convergence status and the absence of any false "mesh-converged" claim;
6. the Delta_X vs Delta_complete separation (4x4 material; >=8^2 at solver noise);
7. Blueprint v1.3 immutability (byte hash);
8. P11D Case-C evidence immutability (byte hashes);
9. presence of the P12C production scripts;
10. P12C provenance fields (run SHA, parameter hash, environment, engine disclosure,
    pre-registered rule, trigger decision, never-inferred-from-Delta_X note);
11. regression guards for the Part C manuscript corrections.

No file is written; all checks are read-only.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
P9 = REPO_ROOT / "paper9"
RAW = P9 / "results" / "raw"
J32 = RAW / "p12c_caseC_32_gap_convergence.json"
J64 = RAW / "p12c_caseC_64_gap_convergence.json"
P11D = RAW / "p11d_caseC_gap_convergence.json"
P11D_DX = RAW / "p11d_deltaX_check.json"
BLUEPRINT = P9 / "plan" / "blueprint" / "Paper9_Blueprint_v1.3.tex"
SEC04 = P9 / "latex" / "sections" / "sec04_fem.tex"
SEC05 = P9 / "latex" / "sections" / "sec05_verification.tex"
SEC06 = P9 / "latex" / "sections" / "sec06_results.tex"
SEC08 = P9 / "latex" / "sections" / "sec08_discussion.tex"
SEC09 = P9 / "latex" / "sections" / "sec09_conclusions.tex"
MSTEX = P9 / "latex" / "ms.tex"

# frozen constants (see P12C_POST_CLOSEOUT_FORENSIC_AUDIT.md, Part A)
SERIES_21 = {4: 2.5731869148388498, 8: 2.2503884154045233, 16: 2.0722484270604395,
             32: 1.9736363149301, 64: 1.9178891171692}
D3_RECORDED = 0.09861211213033805
D4_RECORDED = 0.05574719776087367
R_TRIGGER = 0.5535652777739338
BLUEPRINT_SHA = "ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f"
P11D_SHA = "1d4476f12d0b8ae9096e870436fbe0cd004dcd15e5edbb3663d827e8bedaf6ff"
P11D_DX_SHA = "7dbabbd3676c33d0f7adc995dc5dd7f0bc9065ea427b17fe5f36ee69ed24dbb2"
RUN_SHA = "11543157541c1b9bf9ec4106e1b68f468da9f4a2"
PARAM_SHA = "bb112a522e094b2b804396c080ea4f3683401a38d15efc15adeb577add6cb73b"


def _load(p):
    with open(p) as f:
        return json.load(f)


def _cell(doc, fe, n_bz):
    for c in doc.get("cells_32", doc.get("cells_64", [])):
        if c["cell_id"] == f"{fe}x{fe}_FE_{n_bz}x{n_bz}_BZ":
            return c
    raise KeyError(f"cell {fe}x{fe}_FE_{n_bz}x{n_bz}_BZ not found")


def _p11d_cell(fe, n_bz):
    for c in _load(P11D)["convergence_matrix"]:
        if c["cell_id"] == f"{fe}x{fe}_FE_{n_bz}x{n_bz}_BZ":
            return c
    raise KeyError(f"p11d cell {fe}x{fe}_FE_{n_bz}x{n_bz}_BZ not found")


def _series_21():
    out = {}
    for n in (4, 8, 16):
        out[n] = _p11d_cell(n, 21)["delta_complete"]
    out[32] = _cell(_load(J32), 32, 21)["delta_complete"]
    out[64] = _cell(_load(J64), 64, 21)["delta_complete"]
    return out


def test_five_mesh_series_and_monotonicity():
    s = _series_21()
    for n, ref in SERIES_21.items():
        assert abs(s[n] - ref) <= 5e-10, f"{n}x{n} delta_complete {s[n]} != {ref}"
    vals = [s[n] for n in (4, 8, 16, 32, 64)]
    assert all(a > b for a, b in zip(vals, vals[1:])), f"series not strictly decreasing: {vals}"
    for n in (4, 8, 16):
        assert _p11d_cell(n, 21)["is_complete_open"] is True
    assert _cell(_load(J32), 32, 21)["is_complete_open"] is True
    assert _cell(_load(J64), 64, 21)["is_complete_open"] is True


def test_series_is_not_interpolated():
    s = _series_21()
    mid_16_32 = 0.5 * (s[16] + s[32])
    mid_32_64 = 0.5 * (s[32] + s[64])
    assert abs(mid_16_32 - s[32]) > 1e-2, "32x32 value looks like an average of 16x16 and 32x32"
    assert abs(mid_32_64 - s[64]) > 1e-2, "64x64 value looks like an average of 32x32 and 64x64"


def test_decrements_ratios_and_trigger_record():
    s = _series_21()
    d2, d3 = s[8] - s[16], s[16] - s[32]
    d4 = s[32] - s[64]
    assert abs(d3 - D3_RECORDED) < 1e-9
    assert abs(d4 - D4_RECORDED) < 1e-9
    assert abs(d3 / d2 - R_TRIGGER) < 1e-9
    assert d3 / d2 >= 0.5 and d4 / d3 >= 0.5, "pre-registered >=0.5 trigger must have fired"
    m32, m64 = _load(J32)["metadata"], _load(J64)["metadata"]
    assert "r >= 0.5" in m32["rule_64"], "pre-registered 64x64 rule text changed"
    pre = m64["parent_rule_evaluation"]
    assert abs(pre["r"] - R_TRIGGER) < 1e-12
    assert pre["trigger"] is True and "RUN 64x64" in pre["decision"]
    assert m64["never_inferred_from_delta_X"] is True
    assert "0.5" in m64["trigger"]


def test_raw_json_sidecar_integrity():
    for j in (J32, J64):
        side = j.with_suffix(".json.sha256")
        assert side.exists(), f"missing sidecar {side}"
        digest = hashlib.sha256(j.read_bytes()).hexdigest()
        assert side.read_text().strip().split()[0] == digest, f"sidecar mismatch for {j.name}"


def test_non_convergence_status_and_no_false_convergence_claim():
    for j in (J32, J64):
        blob = j.read_text()
        assert "converged complete gap" not in blob
        stripped = blob.replace("not mesh-converged", "")
        assert "mesh-converged" not in stripped, f"unnegated 'mesh-converged' in {j.name}"
    sec06 = SEC06.read_text()
    assert "not mesh-converged" in sec06
    assert "no mesh-converged complete-gap width is claimed" in sec06
    assert "not mesh-converged" in SEC08.read_text()
    assert "not mesh-converged" in SEC09.read_text()


def test_deltaX_vs_delta_complete_separation():
    dx = _load(P11D_DX)["4x4"]["delta_X"]
    dc4 = _p11d_cell(4, 21)["delta_complete"]
    assert abs(dx - dc4) > 0.18, "4x4 Delta_X must differ materially from Delta_complete"
    for n in (8, 16):
        dxn = _load(P11D_DX)[f"{n}x{n}"]["delta_X"]
        assert abs(dxn - _p11d_cell(n, 21)["delta_complete"]) < 1e-9
    d32 = _load(J32)
    assert abs(d32["path_32"]["delta_XM"] - _cell(d32, 32, 21)["delta_complete"]) < 5e-9
    d64 = _load(J64)
    assert abs(d64["path_64"]["delta_XM"] - _cell(d64, 64, 21)["delta_complete"]) < 5e-9


def test_blueprint_v13_immutable():
    digest = hashlib.sha256(BLUEPRINT.read_bytes()).hexdigest()
    assert digest == BLUEPRINT_SHA, "Blueprint v1.3 was modified"


def test_p11d_case_c_evidence_immutable():
    assert hashlib.sha256(P11D.read_bytes()).hexdigest() == P11D_SHA
    assert hashlib.sha256(P11D_DX.read_bytes()).hexdigest() == P11D_DX_SHA


def test_p12c_production_scripts_present():
    for name, needle in [
        ("p12c_caseC_gap_convergence.py", "assemble_mesh_KM_ngauss_sparse"),
        ("p12c_caseC_gap_convergence_64.py", "MMD_ATA"),
        ("p12c_64_feasibility_probe.py", "feasib"),
    ]:
        p = P9 / "production" / name
        assert p.exists(), f"missing production script {name}"
        assert needle in p.read_text(), f"{name} does not contain {needle!r}"


def test_p12c_provenance_fields():
    m32, m64 = _load(J32)["metadata"], _load(J64)["metadata"]
    for m in (m32, m64):
        assert m["git_sha_at_run_start"] == RUN_SHA
        assert m["parameter_hash_sha256"] == PARAM_SHA
    for d in (_load(J32), _load(J64)):
        env = d["environment"]
        assert env["python"].startswith("3.13")
        assert env["numpy"] and env["scipy"]
    assert "subprocess" in m32["staged_execution_note"]
    assert "OOM" in m32["engine_disclosure"]


def test_part_c_manuscript_corrections_regression():
    sec04 = SEC04.read_text()
    assert "reach degree six per coordinate" in sec04, "sec04 quadrature-degree correction lost"
    sec05 = SEC05.read_text()
    assert r"residuals $\le 1.4 \times 10^{-13}$ (locked tolerances $\le 10^{-12}$)" in sec05
    assert r"\big/ \bar{\omega}_T^{(32)} = 4.63 \times 10^{-11}" in sec05, "eps_Delta must be relative"
    sec08 = SEC08.read_text()
    assert "fully solved" not in sec08
    assert "are resolved and closed within the master traceability matrix" not in sec08
    assert "TV18 is resolved via" not in sec08
    assert "no theoretical order claimed" in MSTEX.read_text()
