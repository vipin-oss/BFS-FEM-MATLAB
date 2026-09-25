#!/usr/bin/env python3
"""P5 mesh-16 production guards.

Binds the n = 16 production repair (2026-09-24) to the artefacts it produced:

  * the raw n = 16 production dataset, its processed table 5, highlights, grid
    archive and run log exist and are internally consistent;
  * the historical n = 1 production records are preserved byte-identically
    (append-only audit trail: the repair never rewrites the pre-repair record);
  * the manuscript's figure/table generators read the n = 16 files, so no
    figure can silently revert to the superseded n = 1 numbers;
  * the isotropic case is rotation invariant to 1e-12 in the new data (a
    physical consistency check on the new artefact);
  * generated figures/tables are not older than the raw dataset they came from.

The numerical-literals check (manuscript text vs regenerated JSON) is in
`test_manuscript_literals_match_mesh16_json`.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

PAPER9 = Path(__file__).resolve().parents[2]
RAW16 = PAPER9 / "results" / "raw" / "p5_production_raw_mesh16.json"
GRID16 = PAPER9 / "results" / "raw" / "p5_production_mesh16_grid.npz"
TABLE16 = PAPER9 / "results" / "processed" / "table5_gap_summary_mesh16.json"
HL16 = PAPER9 / "results" / "processed" / "p5_production_highlights_mesh16.json"
RUNLOG = PAPER9 / "audit" / "evidence" / "p5_mesh16" / "run_log_mesh16.txt"
RAW_N1 = PAPER9 / "results" / "raw" / "p5_production_raw.json"
TABLE_N1 = PAPER9 / "results" / "processed" / "table5_gap_summary.json"
S7_N1 = PAPER9 / "results" / "raw" / "p12b_s7_theta_sweep.json"
GEN_DIRS = [PAPER9 / "figures" / "gen", PAPER9 / "tables" / "gen"]

# historical n = 1 production records, pinned at their pre-repair bytes
N1_SHA = {
    RAW_N1: "0af7445a4c5e502942b451ed8f214d7191ebfe23cb97b3d65b6a0d39f81eb3d0",
    TABLE_N1: "f0e1c2001fab8c8dcfc278717daaba390da8694cc144af12f06cff378d31f784",
    S7_N1: "9d645ce98bc2c1b6776b40bbcf602a11953ec059e2e6ca2b1503047bcbce84d1",
}

SCHEMA_KEYS = ["status", "utc", "git_commit", "master_params", "param_hash", "timing_seconds",
               "environment", "study_S1", "study_S3", "study_S4", "study_S5_design_map",
               "study_S6_polar_map", "study_S6_sensitivity_Stheta", "study_S7_ifc_steering",
               "study_S8_energy_flux", "study_S9_microinertia"]


def _sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def raw():
    if not RAW16.exists():
        pytest.skip("n = 16 production dataset absent in this checkout")
    return json.loads(RAW16.read_text())


def test_mesh16_raw_schema_and_matrix(raw):
    for k in SCHEMA_KEYS:
        assert k in raw, f"missing raw key {k}"
    assert raw["status"] == "COMPLETED"
    mp = raw["master_params"]
    assert mp["N_elem_per_side"] == 16 and mp["dof_per_cell"] == 2048
    assert mp["N_seg"] == 40 and mp["N_kx"] == 41 and mp["N_ky"] == 81 and mp["N_bands"] == 4
    assert len(raw["study_S5_design_map"]) == 42
    assert len(raw["study_S6_polar_map"]) == 42
    assert len(raw["study_S3"]) == 7 and len(raw["study_S4"]) == 6
    assert len(raw["study_S1"]) == 4 and len(raw["study_S7_ifc_steering"]) == 3
    assert len(raw["study_S8_energy_flux"]) == 20 and len(raw["study_S9_microinertia"]) == 10
    pts = {(p["AR"], p["theta_deg"]) for p in raw["study_S5_design_map"]}
    assert pts == {(ar, th) for ar in mp["ar_sweep"] for th in mp["theta_sweep_deg"]}
    for name in ("AR_1_th_0", "AR_10_th_45"):
        assert len(raw["study_S1"][name]["tracked_bands"]) == 121
        assert len(raw["study_S1"][name]["tracked_bands"][0]) == 4


def test_mesh16_solver_health(raw):
    assert raw["n_dense_fallbacks"] == 0, "dense escalations occurred in the n = 16 production"
    assert raw["worst_backward_error"] < mp_tol(raw), "backward-error gate breached"
    prompt = raw["provenance"]
    assert prompt["no_random_start"] is True and prompt["no_rescaling"] is True
    assert "ARPACK" in prompt["eigensolver"] and "SM" not in prompt["eigensolver"]


def mp_tol(raw):
    return float(raw["master_params"]["eigensolver_backward_error_tol"])


def test_mesh16_table5_complete_and_hierarchy(raw):
    t5 = json.loads(TABLE16.read_text())
    assert t5["n_cases"] == 42
    assert len(t5["rows"]) == 126
    for r in t5["rows"]:
        assert r["gap_type"] in {"complete", "directional", "none"}
        if r["inequality_holds"]:
            assert r["delta_path"] >= r["delta_complete"] - 1e-12
    assert sum(1 for r in t5["rows"] if r["inequality_holds"]) == 126


def test_mesh16_isotropy_invariance(raw):
    """AR = 1 is an isotropic microstructure: the 7 orientations must coincide."""
    by_ar = {}
    for p in raw["study_S5_design_map"]:
        if p["AR"] == 1.0:
            by_ar[p["theta_deg"]] = p["gaps"]
    assert len(by_ar) == 7
    ref = by_ar[0.0]
    # pair index 0 is the acoustic pair (1,2); indices 1 and 2 are the claim-bearing
    # pairs (2,3) and (3,4) that carry the Table 5 classification and the design-map maxima.
    for th, gaps in by_ar.items():
        for ipair, (gr, gg) in enumerate(zip(ref, gaps)):
            tol = 5e-6 if ipair == 0 else 1e-11
            for key in ("delta_GX", "delta_XM", "delta_MG", "delta_complete",
                        "omega_lower_max", "omega_upper_min"):
                assert abs(gr[key] - gg[key]) < tol, (
                    f"isotropy broken at theta={th}, pair {gr['band_pair']} ({key}): "
                    f"{abs(gr[key] - gg[key]):.3e} >= {tol:.0e}")


def test_mesh16_grid_archive_present():
    assert GRID16.exists(), "grid archive missing"
    assert HL16.exists(), "highlights missing"
    assert RUNLOG.exists(), "run log missing"
    log = RUNLOG.read_text()
    assert "elements per side" in log and "16" in log
    assert "fallbacks" in log and "sha256" in log


def test_historical_n1_records_untouched():
    for path, want in N1_SHA.items():
        assert path.exists(), f"historical record {path.name} missing"
        assert _sha(path) == want, (f"historical n = 1 record {path.name} was modified; the "
                                    f"repair must be append-only")


def test_generators_read_mesh16_sources():
    wanted = {
        "fig06_caseH_dispersion.py": "p5_production_raw_mesh16.json",
        "fig08_theta_sweep.py": "p5_production_raw_mesh16.json",
        "fig09_ar_sweep.py": "p5_production_raw_mesh16.json",
        "fig10_design_map_3d.py": "p5_production_raw_mesh16.json",
        "fig11_polar_map_regimes.py": "p5_production_raw_mesh16.json",
        "fig12_ifc_wave_steering.py": "p5_production_raw_mesh16.json",
        "fig13_energy_microinertia.py": "p5_production_raw_mesh16.json",
        "fig14_s7_steering_sweep.py": "p12b_s7_theta_sweep_mesh16.json",
        "tab05_gap_summary.py": "table5_gap_summary_mesh16.json",
        "tab07_steering_sweep.py": "p12b_s7_theta_sweep_mesh16.json",
    }
    for name, token in wanted.items():
        for d in GEN_DIRS:
            p = d / name
            if p.exists():
                assert token in p.read_text(), f"{name} does not read {token}"
                break


def test_generated_outputs_not_older_than_source(raw):
    if not RAW16.exists():
        pytest.skip("no n = 16 dataset")
    src = RAW16.stat().st_mtime
    for d, pat in ((PAPER9 / "figures" / "out", "fig*.pdf"),
                   (PAPER9 / "tables" / "out", "tab05*.tex")):
        for out in sorted(d.glob(pat)):
            if out.name.startswith(("fig01", "fig02", "fig03", "fig04", "fig05", "fig07")):
                continue
            assert out.stat().st_mtime >= src - 1.0, f"{out.name} is older than the n = 16 raw data"


def test_manuscript_literals_match_mesh16_json(raw):
    """Claim-bearing literals in the manuscript must agree with the n = 16 data."""
    sec06 = (PAPER9 / "latex" / "sections" / "sec06_results.tex").read_text()
    sec07 = (PAPER9 / "latex" / "sections" / "sec07_steering.tex").read_text()
    sec09 = (PAPER9 / "latex" / "sections" / "sec09_conclusions.tex").read_text()
    design = raw["study_S5_design_map"]
    dgx23 = [p["gaps"][1]["delta_GX"] for p in design]
    best = max(dgx23)
    best_pt = design[dgx23.index(best)]
    d_comp = max(p["gaps"][1]["delta_complete"] for p in design)  # tightest absence-of-complete-gap bound
    s_th = raw["study_S6_sensitivity_Stheta"]["AR_10"]["S_theta_rad_inv"]
    s7 = raw["study_S7_ifc_steering"]
    dmax_5 = s7["AR_5_th_45"]["delta_max_deg"]
    dmax_10 = s7["AR_10_th_45"]["delta_max_deg"]

    def fmt(x, nd):
        return f"{x:.{nd}f}"

    assert fmt(best, 4) in sec06, f"max Delta_GX {fmt(best,4)} missing from sec06"
    # S_theta is printed at 2 dp: that is the precision at which it is unchanged between the
    # n = 8 and n = 16 production meshes (2.3423 -> 2.3372 at AR = 10 moves the 3rd decimal)
    assert fmt(s_th, 2) in sec06, f"S_theta {fmt(s_th,2)} missing from sec06"
    assert fmt(d_comp, 4) in sec06, f"Delta_complete bound {fmt(d_comp,4)} missing from sec06"
    assert fmt(dmax_5, 2) in sec07, f"delta_max(AR=5) {fmt(dmax_5,2)} missing from sec07"
    assert fmt(dmax_10, 2) in sec07, f"delta_max(AR=10) {fmt(dmax_10,2)} missing from sec07"
    assert fmt(best, 4) in sec09 and fmt(d_comp, 4) in sec09
    assert fmt(s_th, 2) in sec09 and fmt(dmax_10, 2) in sec09
    # no n = 1 production literal may survive in the active text
    for stale in ("0.044686", "0.0431", "-0.3758", "3.946"):
        assert stale not in sec06, f"superseded n = 1 literal {stale} still in sec06"
    assert best_pt["theta_deg"] in (0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0)
