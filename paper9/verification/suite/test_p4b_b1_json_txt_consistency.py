"""B1 resolution guard — P4B 5g-5i governing JSON vs historical TXT (fast, deterministic).

Pins the outcome of the B1 provenance reconciliation
(`paper9/audit/P4B_B1_PROVENANCE_RECONCILIATION.md`):

  * the governing JSON is internally consistent — its slope / 95 % CI / eps_Delta are exactly
    reproducible from its own omega / rel_err arrays under the script's own fit-subset rule;
  * the JSON's 5i acceptance is definitional where the plan says it is (eps_Delta includes the
    16->32 change) — that definitional sub-check is documented, never silently changed;
  * the historical TXT keeps its documented run-1 bytes, is labelled, and does not silently
    diverge from the JSON outside the documented 5i fit-subset difference;
  * no theoretical convergence order is claimed anywhere, and the manuscript never quotes 5.4857;
  * only the JSON is consumed by tables / figures / production / manuscript.

An opt-in end-to-end re-run (env P4B_B1_FULL_RERUN=1, ~70 s) additionally executes the script in a
temporary directory and checks exit status, 21/21 PASS, schema, the 4x4 eigenvalue and the
documented stability band of the 3-point estimator.

Guard semantics (revised after the post-B1 independent audit, finding G-1):

  * the committed **expected values** (hashes and literals) are pinned exactly — any change to the
    governing JSON / TXT / script fails loudly, independent of environment;
  * the opt-in **re-run** is compared with *numerical-tolerance* semantics, not bit-equality:
    BLAS/thread configuration shifts the last bits of the dense 4x4 eigenvalue (documented:
    1.164855406907999 vs 1.1648554069080328, ~3.4e-14) while default configuration reproduces the
    committed bits across sandbox instances. A bit-exact assertion here tested an
    implementation/environment detail, not a scientific invariant (G-1);
  * the re-run's 4x4 eigenvalue must additionally satisfy a *property*: it lies inside the
    documented realization band (audit/evidence/p4b_b1) widened by a small tolerance. Material
    changes (mesh, k, parameters, quadrature) move this value by >= 1e-8, i.e. orders of magnitude
    outside every tolerance used here, so meaningful regressions are still detected.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

SUITE = Path(__file__).resolve().parent
PAPER9 = SUITE.parents[1]
REPO = SUITE.parents[2]

JSON_PATH = SUITE / "p4b_5g_to_5i.json"
TXT_PATH = SUITE / "p4b_5g_to_5i.txt"
PY_PATH = SUITE / "p4b_5g_to_5i.py"
PROV_PATH = SUITE / "p4b_5g_to_5i.txt.provenance.md"

JSON_SHA = "383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185"
TXT_SHA = "1daf0f322260327919ee321f0a88d308f637a1c0e6473af5fcccbc56c69b2263"
PY_SHA = "b1c8d9963b14a19e0f62b29434811635f9a8d721133987b87d8e25882516f6a0"

FIT_CUT = 1e-14                       # script's documented fit-subset cut (code, line ~429)
GOV_SLOPE = 4.173919246515192        # run 2 / governing JSON
GOV_CI = (3.1453687594104447, 5.202469733619939)
GOV_EPS = 4.6318154949690315e-11
GOV_D16_32 = 4.6318154949690315e-11
GOV_OMEGA = (1.164855406907999, 1.1648553902126322, 1.1648553893828701, 1.1648553893289162)
GOV_REL_ERR = (1.50912172477929e-08, 7.586511458421733e-10,
               4.632063300824643e-11, 2.4780585559967227e-15)
GOV_MESHES = (4, 8, 16, 32)
GOV_NOTE = "no theoretical order claimed"
TXT_SLOPE_TOKEN = "5.4857"           # run 1 / historical TXT
TXT_EPS_TOKEN = "4.626173e-11"
STABLE_3PT_BAND = (4.17, 4.19)       # 21 realizations: 4.173919 .. 4.183199

# G-1 (post-B1 audit): tolerance used for re-run comparisons, in units of dimensionless omega.
# Documented basis: thread-configuration jitter <= 5e-14; smallest *material* regression scale
# (any mesh/k/parameter/quadrature change) >= 1e-8 -> a 1e-12 tolerance separates the two by
# four orders of magnitude on both sides.
TOL_OMEGA_ABS = 1e-12
OMEGA4_BAND_PAD = 5e-13               # padding around the documented realization band
EVIDENCE_BUNDLE = PAPER9 / "audit" / "evidence" / "p4b_b1" / "repro_realizations_summary.json"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _lsq(hs, errs):
    x = np.log(np.asarray(hs, float))
    y = np.log(np.asarray(errs, float))
    n = len(x)
    xm, ym = x.mean(), y.mean()
    sxx = float(np.sum((x - xm) ** 2))
    slope = float(np.sum((x - xm) * (y - ym)) / sxx)
    yhat = ym + slope * (x - xm)
    dof = n - 2
    se = float(np.sqrt((np.sum((y - yhat) ** 2) / dof) / sxx))
    tcrit = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776}.get(dof, 1.96)
    return slope, slope - tcrit * se, slope + tcrit * se


@pytest.fixture(scope="module")
def rec():
    return json.loads(JSON_PATH.read_text())


def test_governing_json_bytes_pinned():
    assert _sha(JSON_PATH) == JSON_SHA, "governing P4B JSON changed — re-run the B1 reconciliation"
    assert _sha(PY_PATH) == PY_SHA, "P4B script changed — its provenance record must be re-verified"
    assert json.loads(JSON_PATH.read_text())["suite"] == "P4B 5g-5i"


def test_governing_slope_ci_eps_reproducible_from_own_evidence(rec):
    d = rec["5i"]
    hs = [1.0 / n for n in d["meshes"]]
    used = [(h, e) for h, e in zip(hs, d["rel_err"]) if e > FIT_CUT]
    assert len(used) == 3, "governing JSON must rest on the 3-point fit subset"
    slope, lo, hi = _lsq([u[0] for u in used], [u[1] for u in used])
    assert slope == pytest.approx(GOV_SLOPE, rel=1e-12)
    assert d["slope"] == pytest.approx(GOV_SLOPE, rel=1e-12)
    assert (d["CI95"][0], d["CI95"][1]) == pytest.approx(GOV_CI, rel=1e-12)
    assert (lo, hi) == pytest.approx(GOV_CI, rel=1e-12)


def test_governing_baseline_literals_frozen(rec):
    """Hash-independent baseline freeze (G-1 hardening + Part H mutations 1,2,3,4,6).

    Even if the file-hash pins above were updated by a careless maintainer, these literals fail on
    any change to the governing numbers, the fit data, the mesh set, the provenance/status fields
    or the documented non-convergence framing.
    """
    d = rec["5i"]
    assert d["slope"] == GOV_SLOPE
    assert tuple(d["CI95"]) == GOV_CI
    assert d["eps_Delta"] == GOV_EPS
    assert d["d16_32"] == GOV_D16_32
    assert tuple(d["omega"]) == GOV_OMEGA
    assert tuple(d["rel_err"]) == GOV_REL_ERR
    assert tuple(d["meshes"]) == GOV_MESHES
    assert d["note"] == GOV_NOTE
    assert d["floor_flag"] is True
    assert d["observable"].startswith("homogeneous acoustic omega_T")
    # provenance / status fields of the recorded run
    assert rec["suite"] == "P4B 5g-5i"
    assert rec["utc"].startswith("2026-09-22T15:00:35")
    assert (rec["PASS"], rec["FAIL"]) == (21, 0)
    assert rec["P4B"] == "PASS"
    assert rec["PCR1"] == "NOT PASS" and rec["G3"] == "not met" and rec["B6"] == "PARTIAL (unchanged)"
    assert rec["params"]["ell2"] == 0.04 and rec["params"]["l_iso"] == 0.2
    assert rec["params"]["lam"] == rec["params"]["mu"] == rec["params"]["rho"] == 1.0


def test_documented_omega4_realization_band_spans_thread_configs():
    """The ruled-out bit-exact assertion (G-1): the committed evidence records TWO omega(4x4)
    bit-values for the same code and inputs, differing only by BLAS thread configuration."""
    bundle = json.loads(EVIDENCE_BUNDLE.read_text())
    w4 = [r["omega"][0] for r in bundle["realizations"].values()]
    lo, hi = min(w4), max(w4)
    assert hi - lo <= 1e-12, "documented omega(4x4) spread grew beyond the tolerance basis"
    assert lo == 1.164855406907999          # default configuration (20/21 realizations)
    assert hi == 1.1648554069080328          # OMP_NUM_THREADS=1 probe (1/21)
    assert bundle["summary"]["n_realizations"] == 21
    om_ex = bundle["omega_exact"]
    for v in (lo, hi):
        assert abs(v - om_ex) / om_ex < 1e-7, "omega(4x4) far from the M11.3 closed form"


def test_fit_subset_rule_and_floor_definition(rec):
    d = rec["5i"]
    assert d["rel_err"][3] < FIT_CUT, "32^2 datum must be noise-limited in the governing run"
    d16_32 = abs(d["omega"][3] - d["omega"][2]) / d["omega"][3]
    assert d["d16_32"] == pytest.approx(d16_32, rel=1e-12)
    assert d["eps_Delta"] == pytest.approx(max(d16_32, d["rel_err"][3]), rel=1e-12)
    assert d["eps_Delta"] == pytest.approx(GOV_EPS, rel=1e-12)
    # the 16->32 sub-check can never fail by construction of eps_Delta — documented, not changed
    assert d["d16_32"] <= d["eps_Delta"] * (1 + 1e-15)
    recd = (PAPER9 / "audit" / "P4B_B1_PROVENANCE_RECONCILIATION.md").read_text()
    assert "cannot fail" in recd and "1e-14" in recd, "definitional sub-check must stay documented"


def test_historical_txt_bytes_pinned_and_labelled():
    assert _sha(TXT_PATH) == TXT_SHA, "historical run-1 TXT must never be edited or regenerated"
    txt = TXT_PATH.read_text()
    assert TXT_SLOPE_TOKEN in txt and "nfit=4" in txt and TXT_EPS_TOKEN in txt
    assert PROV_PATH.exists(), "the TXT must carry its provenance label file"
    prov = PROV_PATH.read_text()
    assert "run 1" in prov and "not the governing" in prov and TXT_SHA in prov


def test_txt_and_json_agree_outside_the_5i_fit_subset(rec):
    """The only admissible divergence is the 5i fit subset; 5g/5h and omega(4x4) must be identical."""
    txt = TXT_PATH.read_text()
    # 5h: full-precision shared values
    assert "6.911715833981807e-10" in txt
    assert rec["5h"]["max_rel_energy_vs_cd"] == pytest.approx(6.911715833981807e-10, rel=0)
    assert "3.6474033598987756e-07" in txt
    assert rec["5h"]["FE_vg_rel"] == pytest.approx(3.6474033598987756e-07, rel=0)
    # 5g: asymptotic bound and unbounded-branch endpoint
    assert "0.31622777" in txt and rec["5g"]["vinf_T"] == pytest.approx(0.3162277660168379, rel=0)
    assert rec["5g"]["v_ell0_kbar"]["200.0"] == pytest.approx(39.75093337488187, rel=1e-12)
    # every run is bit-identical at n=4 (dense LAPACK path, deterministic)
    assert rec["5i"]["omega"][0] == 1.164855406907999
    assert repr(rec["5i"]["omega"][0]) in txt.replace("oms=[", "oms=[") or "1.164855406907999" in txt


def test_no_theoretical_order_claimed_and_manuscript_uses_governing_values(rec):
    assert rec["5i"]["note"] == "no theoretical order claimed"
    assert "no theoretical order claimed" in json.dumps(rec["rows"])
    ms = (PAPER9 / "latex" / "ms.tex").read_text()
    sec05 = (PAPER9 / "latex" / "sections" / "sec05_verification.tex").read_text()
    assert "no theoretical order claimed" in ms
    for text in (ms, sec05):
        for m in re.finditer(r"theoretical order", text):
            window = text[max(0, m.start() - 24):m.end() + 4]
            assert "no theoretical order" in window, "unnegated theoretical-order claim found"
    for bad in ("5.4857", "5.485", "4.626173e-11", "4.626\\times 10^{-11}"):
        assert bad not in ms and bad not in sec05, f"historical run-1 value {bad} leaked into manuscript"
    assert "4.17" in ms and "4.17" in sec05 and "4.63" in ms


def test_only_the_json_is_consumed_downstream():
    consumers = [
        PAPER9 / "tables" / "gen" / "tab04_consistency_suite.py",
        PAPER9 / "tables" / "gen" / "tab06_convergence_floor.py",
        PAPER9 / "figures" / "gen" / "fig05_mesh_convergence.py",
        PAPER9 / "production" / "p5" / "p5_core.py",
    ]
    for c in consumers:
        t = c.read_text()
        assert "p4b_5g_to_5i.json" in t, f"{c.name} should consume the governing JSON"
        assert "p4b_5g_to_5i.txt" not in t, f"{c.name} must not consume the historical TXT"
    for d in (PAPER9 / "latex", PAPER9 / "tables" / "out", PAPER9 / "figures" / "out"):
        for p in list(d.rglob("*.tex")) + list(d.rglob("*.py")):
            assert "p4b_5g_to_5i.txt" not in p.read_text(), f"{p} must not cite the historical TXT"


@pytest.mark.skipif(os.environ.get("P4B_B1_FULL_RERUN") != "1",
                    reason="opt-in end-to-end rerun (P4B_B1_FULL_RERUN=1, ~70 s)")
def test_full_rerun_opt_in(rec):
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for f in (PY_PATH, SUITE / "p4a_5a_to_5f.py"):
            shutil.copy(f, tmp / f.name)
        proc = subprocess.run([sys.executable, "p4b_5g_to_5i.py"], cwd=tmp,
                              capture_output=True, text=True, timeout=900)
        assert proc.returncode == 0, proc.stdout[-2000:] + proc.stderr[-2000:]
        assert "TOTAL 21  PASS 21  FAIL 0" in proc.stdout
        out = json.loads((tmp / "p4b_5g_to_5i.json").read_text())
        assert set(rec) == set(out), "re-run schema differs from the governing JSON"
        assert out["5i"]["note"] == GOV_NOTE, "re-run dropped the no-theoretical-order note"
        assert (out["PASS"], out["FAIL"]) == (21, 0)
        d = out["5i"]
        assert tuple(d["meshes"]) == GOV_MESHES, "re-run changed the mesh sequence"
        hs = [1.0 / n for n in d["meshes"]]
        used = [(h, e) for h, e in zip(hs, d["rel_err"]) if e > FIT_CUT]
        slope, lo, hi = _lsq([u[0] for u in used], [u[1] for u in used])
        assert d["slope"] == pytest.approx(slope, rel=1e-12), "reported slope != its own fit"
        s3, _, _ = _lsq(hs[:3], d["rel_err"][:3])
        assert STABLE_3PT_BAND[0] <= s3 <= STABLE_3PT_BAND[1], (
            f"3-point estimator {s3:.6f} left the documented band {STABLE_3PT_BAND}")
        # G-1: numerical-tolerance determinism (not bit-equality) + documented property band.
        # Thread/BLAS configuration shifts the last bits of the dense 4x4 eigenvalue (~3.4e-14,
        # recorded in the evidence bundle); material changes move it by >= 1e-8.
        assert abs(d["omega"][0] - rec["5i"]["omega"][0]) <= TOL_OMEGA_ABS, (
            f"omega(4x4) moved by {abs(d['omega'][0] - rec['5i']['omega'][0]):.3e} "
            f"(> {TOL_OMEGA_ABS:.0e}) — beyond documented configuration jitter")
        bundle = json.loads(EVIDENCE_BUNDLE.read_text())
        w4 = [r["omega"][0] for r in bundle["realizations"].values()]
        assert min(w4) - OMEGA4_BAND_PAD <= d["omega"][0] <= max(w4) + OMEGA4_BAND_PAD, (
            "omega(4x4) outside the documented realization band")
        # re-run branch accounting: whatever branch the draw takes, the reported slope must be the
        # fit of its own selected points and the 4x4 datum must stay a real discretization value
        assert d["omega"][0] > d["omega"][1] > d["omega"][2] > d["omega"][3], (
            "omega_T must decrease monotonically with mesh refinement")
        assert abs(d["omega"][0] - bundle["omega_exact"]) / bundle["omega_exact"] < 1e-7
