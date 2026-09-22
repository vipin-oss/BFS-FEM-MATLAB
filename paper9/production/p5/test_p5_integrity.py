#!/usr/bin/env python3
"""P5 integrity tests (fast; no 32^2 solves).

Covers the machinery that the P5 production dataset relies on:
  sampling conventions (M10.1 / M10-a §6), symmetry-group identification and the
  irreducible-zone mask (M10.3), the frozen gap definitions (M12.3), the band
  solver's two paths (dense vs shift-invert), hermiticity residuals, MAC branch
  tracking, the documented spurious-mode accounting, parameter hashing,
  immutability of raw outputs and the parameters-only lint.

Run:  python3 -m pytest production/p5/test_p5_integrity.py -q
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import lint_p5_params as lint  # noqa: E402
import p5_core as core  # noqa: E402

PARAMS_FILE = core.REPO / "params" / "p5_pilot_params.yaml"
SMALL = {                      # cheap solver settings for tests only
    "sigma_shift": -1.0e-06, "tol": 1.0e-12, "maxiter": 20000,
    "dense_max_dof": 2048, "n_proc": 1, "progress_cadence": 25, "mac_min": 0.9,
    "neg_tol": -1.0e-10, "null_tol": 1.0e-10, "herm_tol": 1.0e-12, "bz_tol": 1.0e-10,
    "bz_omega_tol": 1.0e-08, "det_tol": 1.0e-10, "ordering_slack_tol": 1.0e-08,
    "group_tol": 1.0e-09, "aniso_witness_tol": 1.0e-06, "k_norm_tol": 1.0e-12,
    "check_k": [0.37, 0.21], "deg_tol": 1.0e-06,
}


def small_conf(n_mesh=4, n_bands=4, l1=0.30, l2=0.10, theta_deg=30.0, ell2=0.04):
    return {"n_mesh": n_mesh, "n_bands": n_bands, "L": 1.0, "lam": 1.0, "mu": 1.0,
            "rho": 1.0, "ell2": ell2, "l1": l1, "l2": l2,
            "theta_rad": float(np.deg2rad(theta_deg)), "theta_deg": theta_deg,
            "AR": l1 / l2}


# --------------------------------------------------------------------------- #
# sampling conventions
# --------------------------------------------------------------------------- #
def test_path_points_structure_and_breakpoints():
    L, n = 1.0, 7
    ks, legs = core.path_points(L, n)
    assert ks.shape == (3 * n + 1, 2) and legs.shape == (3 * n + 1,)   # M10.1
    assert np.allclose(ks[0], [0.0, 0.0])
    assert np.allclose(ks[n], [np.pi / L, 0.0])          # X
    assert np.allclose(ks[2 * n], [np.pi / L, np.pi / L])  # M
    assert np.allclose(ks[-1], [0.0, 0.0])                # Gamma (closed)
    kb = ks * L / np.pi                      # barred abscissa: 0, 1, 2 at the corners
    assert kb[0, 0] == pytest.approx(0.0)
    assert kb[n, 0] == pytest.approx(1.0)                       # X
    assert kb[2 * n, 0] + kb[2 * n, 1] == pytest.approx(2.0)     # M
    assert kb[-1, 0] + kb[-1, 1] == pytest.approx(0.0)           # closed at Gamma
    assert sorted(set(legs.tolist())) == [0, 1, 2]
    assert math.sqrt(2.0) > 0.0


def test_zone_grid_symmetry_and_extent():
    L, n = 1.0, 5
    ks, (n1, n2) = core.zone_grid(L, n, n)
    assert len(ks) == n * n
    assert ks.min() == pytest.approx(-np.pi / L) and ks.max() == pytest.approx(np.pi / L)
    assert np.any(np.all(ks == 0.0, axis=1))
    assert np.allclose(ks[::-1], -ks)          # symmetric about k = 0


def test_zone_grid_is_superset_of_every_irreducible_domain():
    ks, _ = core.zone_grid(1.0, 9, 9)
    for group, frac in (("C4v", 0.125), ("C2v", 0.25), ("C2v'", 0.25), ("C2", 0.5)):
        mask = core.irreducible_subset(ks, group)
        assert abs(mask.sum() / len(ks) - frac) < 0.08, (group, mask.sum() / len(ks))


# --------------------------------------------------------------------------- #
# point group of the locked operator (M10.3)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("theta,l1,l2,expect", [
    (0.0, 0.2, 0.2, "C4v"), (37.0, 0.2, 0.2, "C4v"),
    (0.0, 0.30, 0.10, "C2v"), (90.0, 0.30, 0.10, "C2v"),
    (45.0, 0.30, 0.10, "C2v'"),
    (30.0, 0.30, 0.10, "C2"), (15.0, 0.30, 0.10, "C2"),
])
def test_point_group_table(theta, l1, l2, expect):
    assert core.point_group(theta, l1, l2, 1e-9) == expect


def test_group_cardinality_and_inversion_membership():
    for group, card in (("C4v", 8), ("C2v", 4), ("C2v'", 4), ("C2", 2)):
        els = core.group_elements(group)
        assert len(els) == card
        assert any(np.allclose(Q, -np.eye(2)) for Q in els.values())  # -I always in G


def test_anisotropic_symmetry_group_matches_spectrum():
    """G elements are symmetries; R90 is NOT (C4v not imposed) for AR != 1."""
    conf = small_conf(n_mesh=4, n_bands=4, l1=0.30, l2=0.10, theta_deg=30.0)
    k = np.array([0.37, 0.21]) * np.pi
    base = core.omega_from_w2(core.band_solve(k[0], k[1], conf, SMALL)["w2"])
    for name, Q in core.group_elements("C2").items():
        kq = Q @ k
        wq = core.omega_from_w2(core.band_solve(kq[0], kq[1], conf, SMALL)["w2"])
        assert np.max(np.abs(wq - base)) < 1e-8, name
    kq = core.group_elements("C4v")["R90"] @ k
    wq = core.omega_from_w2(core.band_solve(kq[0], kq[1], conf, SMALL)["w2"])
    assert np.max(np.abs(wq - base)) > 1e-4        # R90 is not a symmetry


def test_k_evenness_on_zone_grid():
    conf = small_conf(n_mesh=4, n_bands=4)
    ks, _ = core.zone_grid(1.0, 5, 5)
    w = np.array([core.omega_from_w2(core.band_solve(k[0], k[1], conf, SMALL)["w2"]) for k in ks])
    assert np.max(np.abs(w - w[::-1])) < 1e-10


# --------------------------------------------------------------------------- #
# gap definitions (M12.3)
# --------------------------------------------------------------------------- #
def test_gap_definition_nested_sets_monotonicity():
    """S1 subset of S2  =>  Delta[S1] >= Delta[S2] (M12 G1/E3)."""
    w = np.array([[1.0, 3.0], [2.0, 4.0], [1.5, 9.0], [0.5, 5.0]])
    small = np.array([True, True, False, False])
    big = np.ones(4, bool)
    assert core.delta_gap(w, small, 1) >= core.delta_gap(w, big, 1)


def test_path_gap_is_not_a_complete_gap():
    """A positive gap along the path may coexist with an overlap in the zone."""
    w_path = np.array([[1.0, 2.0], [1.2, 5.0], [0.8, 2.5]])
    legs = np.array([0, 1, 2])
    w_zone = np.array([[1.0, 1.95], [1.5, 1.4], [0.9, 2.4]])   # band overlap at k_1=1.5
    mask = np.ones(3, bool)

    p1 = core.gap_table(w_path, legs, w_zone, mask, "C", 1e-8)["pairs"][0]
    assert p1["path_Gamma-X-M-Gamma"] == pytest.approx(2.0 - 1.2)       # +0.8 (path only)
    assert p1["complete_irreducible_zone"] == pytest.approx(1.4 - 1.5)  # -0.1 (overlap)
    assert p1["complete_gap_claimed"] is False                          # never claimed
    assert p1["directional"]["Gamma-X"] == pytest.approx(2.0 - 1.0)


def test_gap_table_reports_negative_ordering_slack_truthfully():
    """Sampled path extrema can exceed sampled zone extrema: the slack is reported."""
    w_path = np.array([[1.0, 2.0], [1.6, 2.2], [1.6, 2.2]])
    legs = np.array([0, 1, 2])
    w_zone = np.array([[1.0, 2.5], [1.45, 2.6], [1.2, 2.7]])
    mask = np.ones(3, bool)
    p1 = core.gap_table(w_path, legs, w_zone, mask, "C", 1e-8)["pairs"][0]
    assert p1["ordering_slack_path_minus_complete"] == pytest.approx(0.4 - 1.05)
    assert p1["ordering_ok_within_slack"] is False           # flagged, not hidden


def test_case_h_never_claims_a_complete_gap():
    w_path = np.array([[1.0, 2.0], [1.2, 5.0], [0.8, 2.5]])
    w_zone = np.array([[1.0, 1.95], [1.5, 1.4], [0.9, 2.4]])
    g = core.gap_table(w_path, np.array([0, 1, 2]), w_zone, np.ones(3, bool), "H", 1e-8)
    assert all(not p["complete_gap_claimed"] for p in g["pairs"])


def test_case_h_has_no_complete_gap_in_the_locked_closed_form():
    """M12 G6 with the M10.2 closed form: folded acoustic branches overlap (Delta <= 0)."""
    L, lam, mu, rho, ell2, l1, l2, th = 1.0, 1.0, 1.0, 1.0, 0.04, 0.30, 0.10, np.deg2rad(30.0)
    k1 = np.linspace(-np.pi / L, np.pi / L, 41)
    K1, K2 = np.meshgrid(k1, k1, indexing="ij")
    L11 = l1 ** 2 * np.cos(th) ** 2 + l2 ** 2 * np.sin(th) ** 2
    L12 = (l1 ** 2 - l2 ** 2) * np.sin(th) * np.cos(th)
    L22 = l1 ** 2 * np.sin(th) ** 2 + l2 ** 2 * np.cos(th) ** 2
    kk = K1 ** 2 + K2 ** 2
    klk = L11 * K1 ** 2 + 2 * L12 * K1 * K2 + L22 * K2 ** 2
    fac = kk * (1.0 + klk / 10.0) / (1.0 + ell2 * kk)
    wT = np.sqrt((mu / rho) * fac).ravel()
    wL = np.sqrt(((lam + 2 * mu) / rho) * fac).ravel()
    w = np.sort(np.stack([wT, wL], axis=1), axis=1)
    assert core.delta_gap(w, np.ones(len(w), bool), 1) <= 0.0


# --------------------------------------------------------------------------- #
# solver paths, hermiticity, tracking, filter
# --------------------------------------------------------------------------- #
def test_dense_and_shiftinvert_agree():
    conf = small_conf(n_mesh=8, n_bands=6)
    k = (0.31 * np.pi, -0.17 * np.pi)
    dense = core.band_solve(k[0], k[1], conf, {**SMALL, "dense_max_dof": 100000})
    si = core.band_solve(k[0], k[1], conf, {**SMALL, "dense_max_dof": 0})
    assert np.max(np.abs(dense["w2"] - si["w2"])) < 1e-10


def test_hermiticity_residual_small():
    conf = small_conf(n_mesh=4, n_bands=4)
    for k in ([0.0, 0.0], [0.4 * np.pi, 0.27 * np.pi], [np.pi, np.pi]):
        K, M = core.reduced_matrices(k[0], k[1], conf)
        h = core.hermiticity_residual(K, M)
        assert h["K_rel"] < 1e-14 and h["M_rel"] < 1e-14


def test_mac_and_mass_orthonormality():
    conf = small_conf(n_mesh=8, n_bands=4)
    k = (0.4 * np.pi, 0.13 * np.pi)
    r = core.band_solve(k[0], k[1], conf, {**SMALL, "dense_max_dof": 100000}, with_vectors=True)
    K, M = core.reduced_matrices(k[0], k[1], conf)
    V = r["V"]
    G = V.conj().T @ (M @ V)
    assert np.max(np.abs(G - np.eye(G.shape[0]))) < 1e-10      # M-orthonormal
    assert core.mac(V[:, 0], V[:, 0], M) == pytest.approx(1.0, abs=1e-12)
    Vp = V[:, 0] + 1e-2 * V[:, 1]
    assert core.mac(Vp, V[:, 1], M) < 1e-3


def test_track_branches_identity_swap_and_degeneracy():
    M = np.eye(2)
    a = np.array([[1.0, 0.0]]).T
    b = np.array([[0.0, 1.0]]).T
    w_sep = [1.0, 4.0]
    AB = np.hstack([a, b])
    r = core.track_branches([AB], [AB], [M], [w_sep], [w_sep], SMALL, 2)
    assert r["min_mac"] == pytest.approx(1.0) and r["reordering_steps"] == []
    # a reordering of the sorted spectrum is reported, and the matched modes still agree
    r2 = core.track_branches([AB], [np.hstack([b, a])], [M], [w_sep], [w_sep], SMALL, 2)
    assert r2["reordering_steps"] == [1] and r2["min_mac"] == pytest.approx(1.0)
    # a matched mode that genuinely changed shape is caught by the MAC metric
    c = (a + b) / np.sqrt(2.0)
    r4 = core.track_branches([AB], [np.hstack([a, c])], [M], [w_sep], [w_sep], SMALL, 2)
    assert r4["min_mac"] == pytest.approx(0.5) and r4["reordering_steps"] == []
    # degenerate subspace at either endpoint -> that mode is not evaluable
    w_deg = [2.0, 2.0 + 1e-12]
    M3, I3 = np.eye(3), np.eye(3)
    r3 = core.track_branches([I3], [I3], [M3], [[2.0, 2.0 + 1e-12, 5.0]], [[1.0, 4.0, 9.0]],
                             SMALL, 3)
    assert r3["n_steps_without_evaluable_mode"] == 0 and r3["min_mac"] == pytest.approx(1.0)
    r5 = core.track_branches([AB], [AB], [M], [w_deg], [w_deg], SMALL, 2)
    assert r5["n_steps_without_evaluable_mode"] == 1
    # a reported mode whose partner sits in the buffer is matched, not failed
    r6 = core.track_branches([np.hstack([a, b, c])], [np.hstack([b, c, a])], [M],
                             [[1.0, 4.0, 9.0]], [[1.0, 4.0, 9.0]], SMALL, 2)
    assert r6["min_mac"] == pytest.approx(1.0) and r6["matched_into_buffer_steps"] == [1]
    # a reported mode whose partner sits in the last guard columns is flagged
    r7 = core.track_branches([np.hstack([a, b, c])], [np.hstack([b, c, a])], [M],
                             [[1.0, 4.0, 9.0]], [[4.0, 9.0, 1.0]], SMALL, 3)
    assert r7["steps_with_guard_risk"] == [1]


def test_mode_filter_accounts_without_dropping():
    f = core.mode_filter(np.array([1.0, -1e-3, 1e-12, np.nan]), SMALL)
    assert f["nonfinite"] == 1 and f["negative"] == 1 and f["null_modes"] == 1
    ok = core.mode_filter(np.array([1.0, 2.0]), SMALL)
    assert ok == {"nonfinite": 0, "negative": 0, "null_modes": 0}


def test_omega_from_w2_clips_only_at_zero():
    assert np.allclose(core.omega_from_w2(np.array([4.0, -1e-22])), [2.0, 0.0])


# --------------------------------------------------------------------------- #
# parameters, provenance, immutability, lint
# --------------------------------------------------------------------------- #
def test_params_file_is_complete_and_hashed_deterministically():
    p = core.load_params(PARAMS_FILE)
    vals = core.resolved_values(p)
    assert set(vals) == {"L", "lam", "mu", "rho", "l1", "l2", "ell2"}
    assert all("tag" in e and "source" in e for e in p["parameters"])
    h1 = core.params_hash(p)
    p2 = core.load_params(PARAMS_FILE)
    assert h1 == core.params_hash(p2)
    p2["sampling"] = dict(p2["sampling"], n_bands=p2["sampling"]["n_bands"] + 1)
    assert core.params_hash(p2) != h1


def test_pilot_params_declare_their_status():
    p = core.load_params(PARAMS_FILE)
    assert p["meta"]["status"] == "PILOT"
    assert p["meta"]["case"] == "H"
    assert abs(p["study"]["AR"] - core.resolved_values(p)["l1"] / core.resolved_values(p)["l2"]) < 1e-12


def test_raw_outputs_are_write_once(tmp_path):
    path = tmp_path / "x.bin"
    h = core.write_immutable(path, b"abc")
    assert path.read_bytes() == b"abc" and not (path.stat().st_mode & 0o222)
    with pytest.raises(SystemExit):
        core.write_immutable(path, b"abc")


def test_lint_parameters_only_rule():
    p = core.load_params(PARAMS_FILE)
    rep = lint.lint_file(HERE / "p5_core.py", p)
    rep2 = lint.lint_file(HERE / "p5_run.py", p)
    assert rep["violations"] == [], rep["violations"]
    assert rep2["violations"] == [], rep2["violations"]
    assert rep["n_literals"] > 0 and rep2["n_literals"] > 0
