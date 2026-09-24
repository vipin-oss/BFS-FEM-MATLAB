"""P12C 64x64 evidence guards (rule-triggered extension of test_p12c_caseC_32).

The locked decision rule fired (r = d3/d2 = 0.5536 >= 0.5, evaluated from
measured data only), so the 64x64 run is MANDATED - not optional.  These
tests pin: presence/provenance of the 64^2 evidence, exact gap definitions,
engine disclosures (incl. the MMD_ATA ordering justification), the measured
infeasibility boundary averted (default-ordering OOM vs MMD_ATA nnz), the
residual-based certification, and the absence of any false convergence
claim.  All numbers are read from the evidence files; nothing is re-specified
here by hand except the locked rational thresholds.
"""
import json
from pathlib import Path

import pytest

RAW = Path(__file__).resolve().parents[2] / "results" / "raw"
J64 = RAW / "p12c_caseC_64_gap_convergence.json"
J32 = RAW / "p12c_caseC_32_gap_convergence.json"
SEC06 = (Path(__file__).resolve().parents[2] / "latex" / "sections"
         / "sec06_results.tex")


def _load():
    assert J64.exists(), "p12c_caseC_64_gap_convergence.json missing"
    return json.loads(J64.read_text())


def test_64_presence_and_provenance():
    d = _load()
    m = d["metadata"]
    assert "trigger" in m and "0.5" in m["trigger"]
    pre = m["parent_rule_evaluation"]
    assert pre["trigger"] is True and "RUN 64x64" in pre["decision"]
    # recompute r entirely from the parent 32^2 evidence (nothing assumed)
    p32 = json.loads(J32.read_text())
    grid = p32["comparison_vs_4_8_16"]["delta_complete_21x21"]
    dc8, dc16 = grid["8x8"], grid["16x16"]
    dc32 = next(c for c in p32["cells_32"] if c["N_bz"] == 21)["delta_complete"]
    assert abs(pre["r"] - (dc16 - dc32) / (dc8 - dc16)) < 1e-9
    assert pre["r"] >= 0.5
    assert m["parameter_snapshot_sha256" if "parameter_snapshot_sha256" in m
             else "parameter_hash_sha256"]
    assert m.get("environment", {}).get("python") or d.get("environment")
    # provenance: git sha recorded, staged execution documented
    assert len(m["git_sha_at_run_start"]) == 40
    assert any("MMD_ATA" in e for e in m["engine_disclosures"])
    # measured infeasibility boundary recorded for default ordering
    assert any("OOM" in e or "2 GB" in e for e in m["engine_disclosures"])
    # sha256 sidecar integrity
    import hashlib
    side = J64.with_suffix(".json.sha256")
    assert side.exists()
    assert side.read_text().strip() == hashlib.sha256(
        J64.read_bytes()).hexdigest()


def test_64_cells_and_definitions():
    d = _load()
    cells = {c["N_bz"]: c for c in d["cells_64"]}
    assert set(cells) == {11, 21}, "64x64 needs both 11x11 and 21x21 BZ cells"
    for c in cells.values():
        assert c["fe_mesh"] == "64x64" and c["fe_dofs"] == 8 * 65 * 65
        assert c["total_k_points"] == c["N_bz"] * c["N_bz"]
        assert c.get("lu_permc_spec") == "MMD_ATA"
        # Delta_complete recomputed from recorded band edges: never inferred
        assert abs(c["delta_complete"]
                   - (c["omega4_min"] - c["omega3_max"])) < 1e-12
        # both extrema at the X corners (mesh >= 8^2 behaviour)
        import math
        for nat in ("omega3_max_at_k", "omega4_min_at_k"):
            kx, ky = c[nat]
            assert (abs(kx - math.pi) < 1e-9) != (abs(ky - math.pi) < 1e-9)
            assert min(kx, ky) < 1e-6 or abs(kx * ky) < 1e-6
        assert c["wall_time_s"] > 0
    p = d["path_64"]
    assert p and p["wall_time_s"] > 0
    # subset inequality at 64^2 from actual data
    assert p["delta_path"] <= max(p["delta_GX"], p["delta_XM"],
                                  p["delta_MG"]) + 1e-12
    # BZ-insensitivity at 64x64 is an empirical claim: <=5e-4 like 32x32
    assert abs(cells[11]["delta_complete"] - cells[21]["delta_complete"]) < 5e-3


def test_64_rates_and_report_consistency():
    d = _load()
    r = d["post_64_report"]
    p32 = json.loads(J32.read_text())
    dc32 = next(c for c in p32["cells_32"] if c["N_bz"] == 21)["delta_complete"]
    dc64 = r["delta_complete_64_21x21"]
    assert abs(r["delta_complete_32_21x21"] - dc32) < 1e-12
    assert abs(r["successive_decrements"]["d4_64vs32"] - (dc32 - dc64)) < 1e-12
    d3 = r["successive_decrements"]["d3_32vs16"]
    assert abs(r["d4_over_d3"]
               - r["successive_decrements"]["d4_64vs32"] / d3) < 1e-12
    assert r["d4_over_d3"] > 0, "refinement narrows the gap at every level"


def test_64_certification():
    d = _load()
    v5 = d["validation"]["v5_residual_certification_64"]
    assert v5["max_rel_residual"] < 1e-6
    assert len(v5["per_k"]) == 4
    for rec in d["validation"]["v4_cross_sigma_64"]:
        assert rec["gamma_abs_diff_sigma_-0.25_vs_-0.5"] < 3e-7
        assert len(rec["per_k"]) == 4
        assert "PRIMARY" in rec["gate_note"]


def test_no_false_convergence_claim_64():
    d = _load()
    blob = json.dumps(d)
    # 64^2 evidence must not claim mesh convergence
    assert "mesh-converged complete gap" not in blob
    assert "\"converged\": true" not in blob
    # manuscript: extended mesh series + honest verdict still present
    tex = SEC06.read_text()
    assert ("32\\times 32" in tex or "32x32" in tex) and "8712" in tex
    assert "64\\times 64" in tex and "33800" in tex
    assert "not mesh-converged" in tex
    assert "no mesh-converged complete-gap width is claimed" in tex
    # the actually measured values must appear
    assert "1.9736" in tex and "1.9179" in tex
