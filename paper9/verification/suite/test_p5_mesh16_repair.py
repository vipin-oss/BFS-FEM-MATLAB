"""P5 n = 16 production repair: provenance, reproducibility and numerical traceability.

PI-authorised 2026-09-24 (see paper9/audit/P5_MESH16_REPAIR.md).  The N = 1 production record is
preserved unchanged -- these guards pin the superseding n = 16 artefact set, prove that the
Table-5 gap classification was recomputed from the new data rather than carried over, and check
that every production-dependent number the active manuscript quotes is the printed form of the
authoritative n = 16 JSON.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
P9 = REPO / "paper9"
EV = P9 / "audit/evidence/p5_mesh16"
LATEX = P9 / "latex"

# Written by pipeline stage 1 on completion of the n = 16 production pass (2026-09-24 23:55 local).
ART_N16 = {
    "results/raw/p5_production_raw_mesh16.json":
        "2a8267b4f3f9bfc209597c54e53c26afc261e220669ccdbbad4b194038376e69",
    "results/raw/p5_production_mesh16_grid.npz":
        "91963453f8c8a7472325154719b3339aa483317b705b3d4a64b2367a509ff81c",
    "results/processed/table5_gap_summary_mesh16.json":
        "d3d633c337a37b3443930d99ce9217e1f5734064201611da2c2823688894f9e4",
    "results/processed/p5_production_highlights_mesh16.json":
        "c3ae8f3e79728cceeb4c905d2e4f0ace2077219758a9b1ddb5c70d6668a5ce47",
    "results/raw/p12b_s7_theta_sweep_mesh16.json":
        "75428b7ca8271818dab2e69ef03db8f2245c2e8585be0e3fbc32edd6e470867e",
    "audit/evidence/p5_mesh16/run_log_mesh16.txt":
        "00500cbd3d3e69eb82411429082d7b3529c12e4e85ca393a5594deb5726ed871",
}

# The n = 8 leg of the same repair: produced by the same code paths, used only for the mesh comparison.
ART_N8 = {
    "results/raw/p5_production_raw_mesh8.json":
        "d69cd6b6d0ea75b1a0d5c39ca231e9a13d260a2ac7a71bf6b96479772092a9e9",
    "results/raw/p5_production_mesh8_grid.npz":
        "33069aada0ddbdba0c5925cde3171a6801e9970b9e8fd29a34002c889f0bc0d5",
    "results/processed/table5_gap_summary_mesh8.json":
        "dfd0150ef794574379df94dce2a143655e1e18a036b1b00bb2b2e3b465b19dc2",
    "results/processed/p5_production_highlights_mesh8.json":
        "5cf5702d8d3e31d9577fc852e39bf60caf8ec923a398ccec787cdc4cbf2e00d9",
    "results/raw/p12b_s7_theta_sweep_mesh8.json":
        "6e737cf6a10c0e7fe8409524f06b570b2ef1299ce1ed655733e19d3d08b2eba4",
}

# Historical N = 1 production artefacts: never rewritten, never re-baselined (append-only record).
ART_N1_UNTOUCHED = {
    "results/raw/p5_production_raw.json":
        "0af7445a4c5e502942b451ed8f214d7191ebfe23cb97b3d65b6a0d39f81eb3d0",
    "results/processed/table5_gap_summary.json":
        "f0e1c2001fab8c8dcfc278717daaba390da8694cc144af12f06cff378d31f784",
    "results/raw/p12b_s7_theta_sweep.json":
        "9d645ce98bc2c1b6776b40bbcf602a11953ec059e2e6ca2b1503047bcbce84d1",
}

# Rows whose gap classification moved when the production discretisation went n = 1 -> n = 16.
# Every one of them is the (3, 4) pair changing directional -> none.
RECLASSIFIED_ROWS = {
    (2.0, 75.0), (2.0, 90.0), (3.0, 60.0), (3.0, 75.0), (3.0, 90.0),
    (5.0, 60.0), (5.0, 75.0), (5.0, 90.0), (7.0, 60.0), (7.0, 75.0),
    (7.0, 90.0), (10.0, 30.0), (10.0, 75.0), (10.0, 90.0),
}

# Production-dependent literals the N = 1 run quoted; none of them may survive in the manuscript.
RETIRED_LITERALS = ("0.0896", "0.0431", "3.946", "0.3758", "0.5632")


def _sha(rel: str) -> str:
    return hashlib.sha256((P9 / rel).read_bytes()).hexdigest()


def _raw16() -> dict:
    return json.loads((P9 / "results/raw/p5_production_raw_mesh16.json").read_text())


def _tab16_rows() -> list[dict]:
    return json.loads(
        (P9 / "results/processed/table5_gap_summary_mesh16.json").read_text())["rows"]


def _raw8() -> dict:
    return json.loads((P9 / "results/raw/p5_production_raw_mesh8.json").read_text())


def _tab8_rows() -> list[dict]:
    return json.loads(
        (P9 / "results/processed/table5_gap_summary_mesh8.json").read_text())["rows"]


def _s78() -> dict:
    return json.loads((P9 / "results/raw/p12b_s7_theta_sweep_mesh8.json").read_text())


def _tab1_rows() -> list[dict]:
    return json.loads((P9 / "results/processed/table5_gap_summary.json").read_text())["rows"]


def _s716() -> dict:
    return json.loads((P9 / "results/raw/p12b_s7_theta_sweep_mesh16.json").read_text())


def _ms() -> str:
    return (LATEX / "ms.tex").read_text()


def _sec(name: str) -> str:
    return (LATEX / "sections" / name).read_text()


# ------------------------------------------------------------------ provenance
def test_artefacts_are_the_recorded_n16_set():
    for rel, want in ART_N16.items():
        assert _sha(rel) == want, f"{rel} is not the recorded n = 16 artefact"


def test_historical_n1_artefacts_are_untouched():
    for rel, want in ART_N1_UNTOUCHED.items():
        assert _sha(rel) == want, f"{rel} must stay byte-identical (historical N = 1 record)"


def test_run_configuration_is_the_frozen_formulation():
    mp = _raw16()["master_params"]
    assert mp["N_elem_per_side"] == 16 and mp["dof_per_cell"] == 2048
    assert mp["elem_size_h"] == pytest.approx(1.0 / 16)
    assert (mp["N_seg"], mp["N_kx"], mp["N_ky"], mp["N_bands"]) == (40, 41, 81, 4)
    assert mp["tol_herm"] == 1e-12
    r = _raw16()
    assert r["status"] == "COMPLETED"
    assert r["n_dense_fallbacks"] == 0, "deterministic eigensolve only; no fallback was needed"
    assert r["worst_backward_error"] < 1e-11
    assert len(r["study_S5_design_map"]) == 42, "same 42-point (theta, AR) matrix"


def test_reproducibility_record_is_complete():
    r = _raw16()
    for key in ("git_commit", "param_hash", "environment", "utc", "provenance"):
        assert r.get(key), f"reproducibility record lacks {key}"
    assert r["n_solves_total"] > 0 and r["timing_seconds"] > 0
    assert "supersedes" in r["provenance"]
    assert (EV / "run_log_mesh16.txt").exists()


# ------------------------------------------------------------------ classification
def test_table5_classification_was_recomputed_not_carried_over():
    rows16 = _tab16_rows()
    rows1 = _tab1_rows()
    assert len(rows16) == len(rows1) == 126
    key = lambda r: (r["AR"], r["theta_deg"], tuple(r["band_pair"]))  # noqa: E731
    t1 = {key(r): r["gap_type"] for r in rows1}
    changed = {key(r)[:2] for r in rows16 if t1.get(key(r)) != r["gap_type"]}
    assert changed == RECLASSIFIED_ROWS, f"reclassified rows moved: {sorted(changed ^ RECLASSIFIED_ROWS)}"
    for r in rows16:
        if tuple(r["band_pair"]) == (3, 4) and (r["AR"], r["theta_deg"]) in RECLASSIFIED_ROWS:
            assert t1[key(r)] == "directional" and r["gap_type"] == "none"
    counts = {g: sum(1 for r in rows16 if r["gap_type"] == g) for g in ("none", "directional")}
    assert counts == {"none": 84, "directional": 42}
    assert all(r["inequality_holds"] for r in rows16)


# ------------------------------------------------------------------ manuscript traceability
def test_manuscript_numbers_are_the_printed_n16_values():
    rows = _tab16_rows()
    dcomp = max(r["delta_complete"] for r in rows)
    dgx = max(r["delta_GX"] for r in rows)
    d45 = [r for r in rows if r["AR"] == 10.0 and r["theta_deg"] == 45.0
           and tuple(r["band_pair"]) == (2, 3)]
    assert round(abs(dcomp), 4) == 0.3235
    assert round(dgx, 4) == 0.0677 and round(d45[0]["delta_GX"], 4) == 0.0043
    for text in (_ms(), _sec("sec06_results.tex"), _sec("sec08_discussion.tex"), _sec("sec09_conclusions.tex")):
        assert "0.3235" in text          # the design-map bound on Delta_complete
    for text in (_sec("sec06_results.tex"), _sec("sec08_discussion.tex"), _sec("sec09_conclusions.tex")):
        assert "0.0677" in text          # the maximum directional gap
    for text in (_sec("sec06_results.tex"), _sec("sec08_discussion.tex")):
        assert "0.0043" in text          # the Gamma-X gap quoted for AR = 10, theta = 45 deg
    s_theta = {k: v["S_theta_rad_inv"] for k, v in _raw16()["study_S6_sensitivity_Stheta"].items()}
    assert round(max(s_theta.values()), 3) == 2.337
    assert s_theta["AR_1"] < 1e-10, "isotropic case must have vanishing orientation sensitivity"
    for text in (_ms(), _sec("sec06_results.tex"), _sec("sec09_conclusions.tex")):
        assert "2.34" in text            # the maximum orientation sensitivity, at its printed 2 dp
    s7 = _s716()
    assert round(s7["M_s"]["AR_5"]["M_s_deg"]) == 0 and round(s7["M_s"]["AR_10"]["M_s_deg"]) == 10
    sec07 = _sec("sec07_steering.tex")
    assert "M_s(\\mathrm{AR}=5) = 0^\\circ" in sec07 and "M_s(\\mathrm{AR}=10) = 10^\\circ" in sec07
    dm5, dm10 = (s7["sweep"][f"AR_{a}_th_0"]["delta_max_deg"] for a in (5, 10))
    assert round(dm5, 4) == 1.4146 and round(dm10, 4) == 2.7846
    assert "1.4146^\\circ" in sec07 and "2.7846^\\circ" in sec07
    # the quoted symmetry bound must be a true upper bound on the measured residual
    resid = max(max(max(v["headless_180_max_dev_deg"],
                        max(v["mirror_delta(ph;th)=delta(90-ph;90-th)_max_dev_deg"].values()))
                    for v in s7["symmetry_checks"].values()), 0.0)
    assert resid <= 1.3e-6, "Section 7 quotes a 1.3e-6 bound; the measurement must not exceed it"


def test_epsilon_delta_margin_is_anchored_on_the_n16_evidence():
    eps = _raw16()["master_params"]["eps_Delta"]
    rows = _tab16_rows()
    smallest_positive = min(r["delta_GX"] for r in rows if r["delta_GX"] > 0)
    assert smallest_positive / eps > 1e7, "the manuscript claims at least seven orders of margin"
    quoted = [r for r in rows if r["AR"] == 10.0 and r["theta_deg"] == 45.0
              and tuple(r["band_pair"]) == (2, 3)][0]["delta_GX"]
    assert abs(quoted - 4.3e-3) < 5e-5
    sec05 = _sec("sec05_verification.tex")
    assert "4.3\\times10^{-3}" in sec05 and "9\\times10^{7}" in sec05
    assert "seven orders" in sec05


def test_no_n1_production_number_survives_in_the_active_manuscript():
    texts = [_ms()] + [p.read_text() for p in sorted((LATEX / "sections").glob("*.tex"))]
    for literal in RETIRED_LITERALS:
        offenders = [t[:40] for t in texts if literal in t]
        assert not offenders, f"N = 1 literal {literal} still in the manuscript"


def test_n8_leg_artefacts_are_the_recorded_set():
    for rel, want in ART_N8.items():
        assert _sha(rel) == want, f"{rel} is not the recorded n = 8 comparison artefact"


def test_s7_n8_comparison_leg_uses_the_same_definitions():
    """The n = 8 leg is the same measurement on a coarser mesh, not a different study."""
    s8, s16 = _s78(), _s716()
    assert s8["discretisation"]["N_elem_per_side"] == 8 and s8["discretisation"]["DOF"] == 512
    assert s16["discretisation"]["N_elem_per_side"] == 16
    assert s8["solver_calls"] == s16["solver_calls"]          # same ring, sampling, branch, step
    assert s8["definitions"]["theta_grid_deg"] == s16["definitions"]["theta_grid_deg"]
    assert s8["definitions"]["AR_list"] == s16["definitions"]["AR_list"]
    assert set(s8["sweep"]) == set(s16["sweep"])
    # The independent anchor: the locked S7 ring must agree with the matching P5 production
    # study_S7 value.  The two runs share the formulation but not the eigensolver iteration path,
    # so the comparison is held at 1e-6 relative; the stricter 1e-9 flag is recorded per case.
    for k, a in s8["anchor_check_vs_p5_production_raw_mesh8"].items():
        assert a["rel_diff"] < 1e-6, f"{k}: n = 8 anchor not reproduced"
    for k, a in s16["anchor_check_vs_p5_mesh16"].items():
        if k == "AR_10_th_45":
            assert a["pass_lt_1e-9"] and a["rel_diff"] < 1e-9, k
        else:
            assert a["rel_diff"] < 1e-6, k


def test_steering_values_are_mesh_independent_at_printed_precision():
    s8, s16 = _s78(), _s716()
    for k, v in s16["sweep"].items():
        assert round(s8["sweep"][k]["delta_max_deg"], 4) == round(v["delta_max_deg"], 4), k
    for ar in ("AR_5", "AR_10"):
        assert s8["M_s"][ar]["M_s_deg"] == s16["M_s"][ar]["M_s_deg"] == (0.0 if ar == "AR_5" else 10.0)
    # theta = 45 deg at AR = 10 sits on an exact four-fold tie of the ring sampling: the discrete
    # argmax picks the smallest representative of the tie, which differs between meshes (5 vs 85).
    # The tabulated value is the n = 16 one; no mesh-independent reading depends on that row.
    assert s16["sweep"]["AR_10_th_45"]["phi_star_deg"] == 5.0
    assert s8["sweep"]["AR_10_th_45"]["phi_star_deg"] == 85.0


def test_printed_precision_is_mesh_independent():
    """Every bound and printed digit the manuscript reports must survive the n = 8 mesh."""
    for tag, s in (("n8", _s78()), ("n16", _s716())):
        for ar in ("AR_5", "AR_10"):
            v = [s["sweep"][f"{ar}_th_{th}"]["delta_max_deg"] for th in (0, 15, 30, 45, 60, 75, 90)]
            span = max(v) - min(v)
            assert span <= 1e-5, f"{tag}/{ar}: the printed 1e-5 deg invariance bound fails"
            assert 100.0 * span / min(v) <= 5e-4, f"{tag}/{ar}: the printed 5e-4 % bound fails"
        sc = s["symmetry_checks"]
        assert max(sc[a]["headless_180_max_dev_deg"] for a in sc) <= 1.3e-6
        assert max(max(sc[a]["mirror_delta(ph;th)=delta(90-ph;90-th)_max_dev_deg"].values())
                   for a in sc) <= 1.3e-6
        assert max(sc[a]["delta_max_th_eq_90mth_max_dev_deg"] for a in sc) <= 1e-7


def test_table5_printed_precision_is_mesh_independent():
    """Table 5 is printed at the finest precision that survives the n = 8 mesh (two decimals for the
    larger columns, three for the small Delta_GX entries, two for S_theta)."""
    rows16, rows8 = _tab16_rows(), _tab8_rows()
    key = lambda r: (r["AR"], r["theta_deg"], tuple(r["band_pair"]))  # noqa: E731
    d8 = {key(r): r for r in rows8}
    printed = [r for r in rows16 if tuple(r["band_pair"]) == (2, 3) and r["AR"] in (1.0, 3.0, 5.0, 10.0)
               and r["theta_deg"] in (0.0, 45.0, 90.0)]
    assert len(printed) == 12, "the table prints twelve rows"
    for r in printed:
        assert round(d8[key(r)]["delta_GX"], 3) == round(r["delta_GX"], 3), key(r)
        for f in ("delta_path", "delta_complete", "norm_gap_width"):
            assert round(d8[key(r)][f], 2) == round(r[f], 2), (key(r), f)
    st8 = _raw8()["study_S6_sensitivity_Stheta"]
    st16 = _raw16()["study_S6_sensitivity_Stheta"]
    for a in st16:
        assert round(st8[a]["S_theta_rad_inv"], 2) == round(st16[a]["S_theta_rad_inv"], 2), a
    tab05 = (P9 / "tables/out/tab05_gap_summary.tex").read_text()
    assert "$\\mathrm{AR}=10: 2.34$" in tab05
    assert "unchanged between the $n = 8$ and $n = 16$" in tab05


# ------------------------------------------------------------------ n = 8 vs n = 16
def test_n8_vs_n16_comparison_is_recorded():
    p = EV / "mesh_comparison.json"
    if not p.exists():
        pytest.skip("pipeline stage 5 (verify_p5_mesh16.py) has not written the comparison yet")
    cmp = json.loads(p.read_text())
    assert len(cmp["cases"]) == 42
    # This is the CONVERGED pair: no gap classification moves between n = 8 and n = 16 (the
    # 14-row reclassification in the Table-5 test above is the N = 1 -> n = 16 comparison).
    assert cmp["summary"]["classification_changes"] == 0
    assert cmp["summary"]["max_abs_diff_omega_X"] < 1e-2
    assert cmp["summary"]["max_abs_diff_omega_M"] < 1e-2
    assert all(g["band_pair"] for row in cmp["cases"] for g in row["gaps"])
