"""P12B steering figure-of-merit guard tests.

Pins the locked S7-extension sweep conventions, the computed M_s values, the
verified field symmetries, the legacy S7 anchor reproduction, and the
manuscript/table/figure integration of the reported numbers (registry-first:
no hand-entered values).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
EVID = REPO_ROOT / "paper9/results/raw/p12b_s7_theta_sweep.json"


def _load():
    return json.loads(EVID.read_text())


def test_locked_conventions_and_registry_params():
    d = _load()
    p5 = json.loads(
        (REPO_ROOT / "paper9/results/raw/p5_production_raw.json").read_text())
    assert d["master_params"] == p5["master_params"], (
        "P12B must run on the locked P5 parameter basis")
    defs = d["definitions"]
    assert defs["theta_grid_deg"] == [0, 15, 30, 45, 60, 75, 90]
    assert defs["AR_list"] == [5.0, 10.0]
    sc = d["solver_calls"]
    L = d["master_params"]["Lcell"]
    assert sc["k_rad"] == pytest.approx(0.5 * np.pi / L)  # S7 ring, unchanged
    assert sc["phi_n_points"] == 73 and sc["branch"] == 0
    assert sc["fd_step_h"] == 1e-4
    assert set(d["sweep"]) == {f"AR_{a:g}_th_{t:g}"
                               for a in (5.0, 10.0)
                               for t in (0, 15, 30, 45, 60, 75, 90)}


def test_m_s_definition_and_values():
    d = _load()
    for AR in ("5", "10"):
        m = d["M_s"][f"AR_{AR}"]
        p0 = d["sweep"][f"AR_{AR}_th_0"]["phi_star_deg"]
        p90 = d["sweep"][f"AR_{AR}_th_90"]["phi_star_deg"]
        assert p0 == pytest.approx(45.0) and p90 == pytest.approx(45.0)
        assert m["M_s_deg"] == pytest.approx(p90 - p0)
        assert m["M_s_deg"] == pytest.approx(0.0, abs=1e-12)
        # refined parabolic estimate agrees with the discrete grid value
        assert abs(m["M_s_refined_deg"]) < 5e-5


def test_verified_symmetries_and_legacy_anchor():
    d = _load()
    for AR in ("5", "10"):
        chk = d["symmetry_checks"][f"AR_{AR}"]
        assert chk["headless_180_max_dev_deg"] < 1e-6  # arccos rounding at delta~0
        assert max(chk["mirror_delta(ph;th)=delta(90-ph;90-th)_max_dev_deg"]
                   .values()) < 1e-8
        assert chk["theta0_vs_theta90_mirrored_max_dev_deg"] < 1e-8
        assert chk["delta_max_th_eq_90mth_max_dev_deg"] < 1e-8
        # theta=0 and theta=90 fields are mirrors, hence NOT pointwise equal
        assert chk["theta0_vs_theta90_direct_max_dev_deg"] > 1e-3
    for cfg, a in d["legacy_anchor_check"].items():
        assert a["pass_lt_1e-9"], f"{cfg}: locked pipeline not reproduced"
        # in fact the reproduction is exact (same code path)
        assert a["rel_diff"] == pytest.approx(0.0, abs=1e-14)


def test_manuscript_and_table_integration():
    d = _load()
    ms = d["M_s"]
    sec07 = (REPO_ROOT / "paper9/latex/sections/sec07_steering.tex").read_text()
    assert "M_s(\\mathrm{AR}=5) = M_s(\\mathrm{AR}=10) = +0.0000^\\circ" in sec07
    assert "\\phi^*(90^\\circ) = \\phi^*(0^\\circ) = 45.00^\\circ" in sec07
    assert "[1.4135^\\circ,\\,1.4425^\\circ]" in sec07
    assert "[2.7866^\\circ,\\,2.8227^\\circ]" in sec07
    assert "\\label{fig:s7_steering_sweep}" in sec07
    assert "\\label{tab:steering_sweep}" in sec07
    abstract = (REPO_ROOT / "paper9/latex/ms.tex").read_text()
    assert "M_s = \\phi^*(90^\\circ) - \\phi^*(0^\\circ) = 0.0000^\\circ" in abstract
    concl = (REPO_ROOT / "paper9/latex/sections/sec09_conclusions.tex").read_text()
    assert "(45^\\circ-\\theta) \\bmod 90^\\circ" in concl
    assert "0.0000^\\circ" in concl
    # table rows match the evidence numbers exactly (registry-first)
    tab = (REPO_ROOT / "paper9/tables/out/tab07_steering_sweep.tex").read_text()
    sw = d["sweep"]
    for th in (0, 15, 30, 45, 60, 75, 90):
        r5, r10 = sw[f"AR_5_th_{th}"], sw[f"AR_10_th_{th}"]
        row = (f"${th}^\\circ$ & {r5['delta_max_deg']:.4f} & {r5['phi_star_deg']:.0f} "
               f"& {r10['delta_max_deg']:.4f} & {r10['phi_star_deg']:.0f} \\\\")
        assert row in tab, f"table row for theta={th} missing/stale"
    assert ("$M_s(\\mathrm{AR}{=}5) = "
            f"{ms['AR_5']['M_s_deg']:+.4f}^\\circ$") in tab
    assert ("$M_s(\\mathrm{AR}{=}10) = "
            f"{ms['AR_10']['M_s_deg']:+.4f}^\\circ$") in tab
    for f_ in ("paper9/figures/out/fig14_s7_steering_sweep.pdf",
               "paper9/figures/out/fig14_s7_steering_sweep.png"):
        pth = REPO_ROOT / f_
        assert pth.exists() and pth.stat().st_size > 10000, f_


def test_live_recompute_matches_evidence():
    """Recompute phi* and M_s from the locked solver path; must reproduce the
    stored evidence (protects against evidence file drift)."""
    sys.path.insert(0, str(REPO_ROOT / "paper9"))
    from solver.bfs_bloch_solver import (
        assemble_KM, L_plane, semi_axes_from_ar, compute_group_velocity_2d)

    d = _load()
    mp = d["master_params"]
    L, l_iso = mp["Lcell"], mp["l_iso"]
    lam, mu, rho, ell2 = mp["lam"], mp["mu"], mp["rho"], mp["ell2"]
    k_rad = 0.5 * np.pi / L
    phis = np.linspace(0.0, 2.0 * np.pi, 73)

    def phi_star(AR, th_deg):
        l1, l2 = semi_axes_from_ar(AR, l_iso=l_iso, rule="volume_equivalent")
        L11, L22, L12 = L_plane(l1, l2, float(np.deg2rad(th_deg)))
        K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22,
                           L12=L12, rho=rho, ell2=ell2)
        delta = []
        for phi in phis:
            _, _, dd = compute_group_velocity_2d(
                K, M, k_rad * np.cos(phi), k_rad * np.sin(phi),
                h=1e-4, L=L, branch=0)
            delta.append(dd)
        delta = np.asarray(delta)
        i0 = int(np.flatnonzero(delta >= delta.max() * (1.0 - 1e-12))[0])
        return float(np.rad2deg(phis[i0]) % 90.0), float(delta.max())

    for AR in (5.0, 10.0):
        p0, dmax0 = phi_star(AR, 0.0)
        p90, dmax90 = phi_star(AR, 90.0)
        ev = d["sweep"]
        assert p0 == pytest.approx(ev[f"AR_{AR:g}_th_0"]["phi_star_deg"])
        assert p90 == pytest.approx(ev[f"AR_{AR:g}_th_90"]["phi_star_deg"])
        assert dmax0 == pytest.approx(ev[f"AR_{AR:g}_th_0"]["delta_max_deg"])
        assert dmax90 == pytest.approx(ev[f"AR_{AR:g}_th_90"]["delta_max_deg"])
        assert (p90 - p0) == pytest.approx(
            d["M_s"][f"AR_{AR:g}"]["M_s_deg"], abs=1e-12)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
