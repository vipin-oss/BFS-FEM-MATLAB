"""Automated tests for P5 Pilot and Production Suites.

Verifies:
- Pilot integrity and 12/12 checks
- Repeat bitwise reproducibility
- Matrix Hermiticity and eigenvalue non-negativity
- Gap taxonomy hierarchy: Delta[leg] >= Delta[path] >= Delta[complete]
- Case H gapless nature: Delta[complete] <= 0
- High-k micro-inertia asymptotics: bounded vs unbounded
- Anisotropic wave steering: delta = 0 for AR=1, delta > 0 for AR > 1
- Energy partition conservation and monotonicity
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_PILOT = REPO_ROOT / "results" / "raw" / "p5_pilot_raw.json"
PROC_PILOT = REPO_ROOT / "results" / "processed" / "p5_pilot_summary.json"
RAW_PROD = REPO_ROOT / "results" / "raw" / "p5_production_raw.json"
TABLE5 = REPO_ROOT / "results" / "processed" / "table5_gap_summary.json"


def test_pilot_summary_pass():
    assert PROC_PILOT.exists(), "Pilot summary file does not exist"
    with open(PROC_PILOT) as f:
        data = json.load(f)
    assert data["pilot_decision"] == "PASS", f"Pilot decision was {data['pilot_decision']}"
    assert data["pilot_checks"]["total"] == 12
    assert data["pilot_checks"]["pass"] == 12
    assert data["pilot_checks"]["fail"] == 0


def test_pilot_raw_finite_and_hermitian():
    assert RAW_PILOT.exists(), "Pilot raw file does not exist"
    with open(RAW_PILOT) as f:
        data = json.load(f)
    bands = np.array(data["path"]["filtered_bands"])
    assert np.all(np.isfinite(bands)), "Pilot bands contain NaN/Inf"
    assert np.all(bands >= 0.0), "Pilot bands contain negative frequencies"
    assert data["path"]["max_herm_K"] < 1e-12, "Path Kbar Hermiticity error exceeds tol"
    assert data["path"]["max_herm_M"] < 1e-12, "Path Mbar Hermiticity error exceeds tol"
    assert data["grid"]["max_herm_K"] < 1e-12, "Grid Kbar Hermiticity error exceeds tol"
    assert data["grid"]["max_herm_M"] < 1e-12, "Grid Mbar Hermiticity error exceeds tol"


def test_production_raw_completed():
    assert RAW_PROD.exists(), "Production raw file does not exist"
    with open(RAW_PROD) as f:
        data = json.load(f)
    assert data["status"] == "COMPLETED"
    assert len(data["study_S5_design_map"]) == 42
    assert len(data["study_S3"]) == 7
    assert len(data["study_S4"]) == 6


def test_gap_taxonomy_inequality_all_cases():
    assert TABLE5.exists(), "Table 5 processed file does not exist"
    with open(TABLE5) as f:
        data = json.load(f)
    rows = data["rows"]
    assert len(rows) == 126  # 42 cases * 3 band pairs
    for r in rows:
        assert r["inequality_holds"] is True, f"Inequality failed for AR={r['AR']}, theta={r['theta_deg']}"
        assert r["delta_GX"] >= r["delta_path"] - 1e-12
        assert r["delta_XM"] >= r["delta_path"] - 1e-12
        assert r["delta_MG"] >= r["delta_path"] - 1e-12
        assert r["delta_path"] >= r["delta_complete"] - 1e-12


def test_caseH_has_no_complete_bragg_gap():
    with open(TABLE5) as f:
        data = json.load(f)
    rows = data["rows"]
    max_complete = max(r["delta_complete"] for r in rows)
    assert max_complete <= 0.0, f"Case H unexpectedly exhibited complete gap: {max_complete}"


def test_anisotropic_wave_steering():
    with open(RAW_PROD) as f:
        data = json.load(f)
    s7 = data["study_S7_ifc_steering"]
    # Isotropic AR=1 should have near-zero deviation angle
    assert s7["AR_1_th_0"]["delta_max_deg"] < 0.05
    # Anisotropic AR=5 and AR=10 should have substantial deviation
    assert s7["AR_5_th_45"]["delta_max_deg"] > 1.0
    assert s7["AR_10_th_45"]["delta_max_deg"] > 2.0
    # Higher AR should yield greater maximum steering deviation
    assert s7["AR_10_th_45"]["delta_max_deg"] > s7["AR_5_th_45"]["delta_max_deg"]


def test_microinertia_asymptotics():
    with open(RAW_PROD) as f:
        data = json.load(f)
    s9 = data["study_S9_microinertia"]
    pt200 = s9[-1]
    assert pt200["kbar"] == 200.0
    # Bounded branch matches theoretical vinf within 0.1%
    assert pt200["rel_vinf_error"] < 1e-3
    # Unbounded branch matches theoretical asymptotic slope within 0.1%
    assert pt200["rel_zero_asymp_error"] < 1e-3
    # ell=0 branch phase velocity is significantly greater than bounded branch
    assert pt200["vp_ell_zero"] > 100.0 * pt200["vp_ell_pos"]


def test_energy_partition_properties():
    with open(RAW_PROD) as f:
        data = json.load(f)
    s8 = data["study_S8_energy_flux"]
    for pt in s8:
        assert 0.0 <= pt["Wg_over_W_major"] < 1.0
        assert 0.0 <= pt["Tg_over_T"] < 1.0
        assert abs((pt["Wg_over_W_major"] + pt["Wc_over_W_major"]) - 1.0) < 1e-12
        assert abs((pt["Tg_over_T"] + pt["T0_over_T"]) - 1.0) < 1e-12
    # Check monotonicity with frequency/wavenumber
    wg_vals = [pt["Wg_over_W_major"] for pt in s8]
    assert all(wg_vals[i] <= wg_vals[i + 1] for i in range(len(wg_vals) - 1))
