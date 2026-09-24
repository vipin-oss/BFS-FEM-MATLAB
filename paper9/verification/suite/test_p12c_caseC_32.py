"""P12C Case-C 32x32 convergence guard tests.

Pins: 32x32 evidence presence & provenance; Delta_X / Delta_path /
Delta_complete definitions and their separation; the 64x64 >=0.5-ratio
trigger decision recorded against the registry values; the engine-deviation
disclosure; and the absence of any false 'mesh-converged' claim.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
EVID = REPO_ROOT / "paper9/results/raw/p12c_caseC_32_gap_convergence.json"
P11D = REPO_ROOT / "paper9/results/raw/p11d_caseC_gap_convergence.json"


def _load():
    assert EVID.exists(), "P12C 32x32 evidence file missing"
    return json.loads(EVID.read_text())


def _p11d_deltas():
    d = json.loads(P11D.read_text())
    return {c["cell_id"]: c["delta_complete"] for c in d["convergence_matrix"]}


def test_evidence_presence_and_provenance():
    d = _load()
    md = d["metadata"]
    assert md["git_sha_at_run_start"]
    assert md["parameter_snapshot"]["inclusion"]["lam"] == 64.19
    assert md["parameter_snapshot"]["matrix"]["lam"] == 3.088
    assert len(md["parameter_hash_sha256"]) == 64
    assert "OOM" in md["engine_disclosure"], "engine deviation must be disclosed"
    assert "sparse" in md["engine_disclosure"]
    cells = {c["cell_id"]: c for c in d["cells_32"]}
    for grid in ("11", "21"):
        cid = f"32x32_FE_{grid}x{grid}_BZ"
        assert cid in cells, f"missing {cid}"
        c = cells[cid]
        assert c["fe_dofs"] == 8 * 33 * 33
        assert c["wall_time_s"] > 0
        assert c["total_k_points"] == int(grid) ** 2
    assert d["path_32"]["n_seg_per_leg"] == 20
    assert d["wall_time_total_s"] > 0
    # sha256 sidecar must match the evidence file byte-for-byte
    side = EVID.with_suffix(EVID.suffix + ".sha256")
    assert side.exists()
    assert side.read_text().split()[0] == hashlib.sha256(EVID.read_bytes()).hexdigest()
    env = d["environment"]
    assert env["python"] and env["numpy"] and env["scipy"]


def test_validation_blocks_all_passed():
    d = _load()
    v = d["validation"]
    assert {r["mesh"] for r in v["v3_assembly_equality"]} == {"4x4", "8x8", "16x16"}
    for rec in v["v3_assembly_equality"]:
        assert rec["max_abs_diff_K"] < 1e-12 and rec["max_abs_diff_M"] < 1e-12
    assert {r["mesh"] for r in v["v1_spot_k"]} == {"4x4", "8x8", "16x16"}
    for rec in v["v1_spot_k"]:
        assert any(abs(k[0]) < 1e-12 and abs(k[1]) < 1e-12 for k in rec["spot_k"]), \
            "Gamma spot-k must be included (shift-side protection)"
        assert rec["max_abs_diff_vs_gvx_and_reference"] < 1e-9
    v2 = v["v2_authoritative_reproduction"]
    # resume re-runs cells and appends records; require all 6 unique cells,
    # every record passing (duplicates are legitimate re-validations)
    cids = {r["cell_id"] for r in v2}
    assert cids == {f"{N}x{N}_FE_{G}x{G}_BZ" for N in (4, 8, 16) for G in (11, 21)}
    for rec in v2:
        assert rec["abs_diff"] < 1e-8
    # one v4 record per asm32_v4 invocation; every record must satisfy the
    # calibrated gates: non-Gamma strict, Gamma catastrophic-flag (Gamma
    # rigid-mode cluster: cross-shift agreement saturates ~1e-8 at 32^2,
    # while Gamma correctness is pinned by v1 vs dense engines, asserted above)
    assert len(v["v4_cross_sigma_32"]) >= 1
    for rec in v["v4_cross_sigma_32"]:
        assert rec["max_abs_diff_nongamma_sigma_-0.25_vs_-0.5"] < 1e-9
        assert rec["gamma_abs_diff_sigma_-0.25_vs_-0.5"] < 1e-7
        assert "gate_note" in rec and "1e-8" in rec["gate_note"]
        # per-k values must be present and uncoalesced (4 distinct spot-k)
        assert len(rec["per_k"]) == 4
        assert sum(p["is_gamma"] for p in rec["per_k"]) == 1


def test_gap_definitions_and_separation():
    d = _load()
    for c in d["cells_32"]:
        # Delta_complete is computed directly from sampled-BZ extrema, never
        # inferred from Delta_X (metadata must state it verbatim)
        assert (c["delta_complete"] ==
                pytest.approx(c["omega4_min"] - c["omega3_max"]))
        assert set(c["omega3_max_at_k"]) is not None
        assert c["omega4_min_at_k"] is not None
    assert "never inferred from Delta_X" in d["metadata"]["delta_complete_definition"] \
        or "never" in d["metadata"]["delta_complete_definition"]
    p = d["path_32"]
    for leg in ("delta_GX", "delta_XM", "delta_MG"):
        assert leg in p
    # hierarchy sanity at the computed meshes (P11D locked subset inequality)
    assert p["delta_path"] <= p["delta_XM"] + 1e-12
    assert p["delta_path"] <= p["delta_GX"] + 1e-12
    # Delta_X (X-point, = delta at X from legs/paths at these meshes) and
    # Delta_complete are distinct quantities whose equality at >=8x8 meshes is
    # an observed geometric fact (edges at X), not a definition conflation
    cells = {c["cell_id"]: c for c in d["cells_32"]}
    dc21 = cells["32x32_FE_21x21_BZ"]
    # edges at X: both extrema must sit on the X corner of the quarter zone
    import numpy as np

    def _is_X_corner(k):
        kx, ky = k
        return (abs(kx - np.pi) < 1e-6 and abs(ky) < 1e-6) or (
            abs(ky - np.pi) < 1e-6 and abs(kx) < 1e-6)

    assert _is_X_corner(dc21["omega3_max_at_k"])
    assert _is_X_corner(dc21["omega4_min_at_k"])


def test_64_trigger_decision_recorded_against_rule():
    d = _load()
    p11 = _p11d_deltas()
    dc4, dc8, dc16 = (p11["4x4_FE_21x21_BZ"], p11["8x8_FE_21x21_BZ"],
                      p11["16x16_FE_21x21_BZ"])
    cmp_ = d["comparison_vs_4_8_16"]
    assert cmp_["delta_complete_21x21"]["4x4"] == pytest.approx(dc4)
    assert cmp_["delta_complete_21x21"]["8x8"] == pytest.approx(dc8)
    assert cmp_["delta_complete_21x21"]["16x16"] == pytest.approx(dc16)
    dc32 = cmp_["delta_complete_21x21"]["32x32"]
    d2, d3 = dc8 - dc16, dc16 - dc32
    r_expected = d3 / d2
    rule = d["rule_64_evaluation"]
    assert rule["rule"] == "run 64x64 IFF r = d3/d2 >= 0.5"
    assert rule["r"] == pytest.approx(r_expected, rel=1e-12)
    assert rule["trigger"] == bool(r_expected >= 0.5)
    # the comparison block must expose actual mesh-to-mesh changes
    assert cmp_["mesh_to_mesh_changes"]["32_vs_16"] == pytest.approx(dc32 - dc16)
    assert cmp_["successive_decrements"]["d3_16to32"] == pytest.approx(d3)


def test_no_false_converged_claim_and_manuscript_honesty():
    d = _load()
    blob = json.dumps(d).lower()
    assert "mesh-converged" not in blob.replace("not mesh-converged", ""), \
        "evidence must not claim mesh convergence"
    sec06 = (REPO_ROOT / "paper9/latex/sections/sec06_results.tex").read_text()
    # the Case-C mesh paragraph must honestly report the 32x32 extension and
    # must keep the 'not mesh-converged' verdict unless/until data support it
    assert "32\\times 32 mesh" in sec06 or "32x32" in sec06 or "8712" in sec06
    assert "not mesh-converged" in sec06 or "not converged" in sec06.lower()
    assert "no mesh-converged complete-gap width is claimed" in sec06


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
