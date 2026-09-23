#!/usr/bin/env python3
"""
test_p8_remediation.py
Regression tests ensuring all findings from P8 Forensic Manuscript Audit
(FIND-01 through FIND-08) remain strictly remediated and verified.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LATEX_DIR = REPO_ROOT / "paper9" / "latex" / "sections"

def test_find05_mathematical_prefactor_tau_and_Kg():
    """FIND-05: Ensure factor 1/10 appears in double stress and Kg definitions."""
    sec02 = (LATEX_DIR / "sec02_continuum.tex").read_text(encoding="utf-8")
    assert r"\tau_{ijk} = \frac{1}{10}" in sec02 or r"\tau_{ijk} = \tfrac{1}{10}" in sec02, (
        "Factor 1/10 missing from double stress definition in sec02_continuum.tex"
    )

    sec04 = (LATEX_DIR / "sec04_fem.tex").read_text(encoding="utf-8")
    assert r"\bmK^g(\theta, \mathrm{AR}) = \frac{1}{10}" in sec04 or r"\bmK^g(\theta, \mathrm{AR}) = \tfrac{1}{10}" in sec04, (
        "Factor 1/10 missing from Kg definition in sec04_fem.tex"
    )

def test_find04_asymptotics_prefactor_and_params():
    """FIND-04: Ensure Appendix A and Sec 7.4 contain 1/10 factor, sqrt(10), and Table 2 params."""
    appA = (LATEX_DIR / "appA_asymptotics.tex").read_text(encoding="utf-8")
    assert r"\frac{1}{10} \mu l_{\mathrm{eff}}^2" in appA or r"\frac{1}{10}\mu l_{\mathrm{eff}}^2" in appA, (
        "Factor 1/10 missing from 1D PDE in appA_asymptotics.tex"
    )
    assert r"\sqrt{10}\,\bar{\ell}_{\mathrm{i}}" in appA or r"\sqrt{10}\bar{\ell}_{\mathrm{i}}" in appA, (
        "Denominator sqrt(10)*ell_i missing from appA_asymptotics.tex"
    )
    assert "0.20" in appA, "Baseline length scale 0.20 missing from appA_asymptotics.tex"
    assert "0.3162277" not in appA, "Synthetic ell_i parameter must not be used in appA_asymptotics.tex"

    sec07 = (LATEX_DIR / "sec07_steering.tex").read_text(encoding="utf-8")
    assert r"\sqrt{10}\,\bar{\ell}_{\mathrm{i}}" in sec07 or r"\sqrt{10}\bar{\ell}_{\mathrm{i}}" in sec07, (
        "Denominator sqrt(10)*ell_i missing from sec07_steering.tex"
    )
    assert "0.20" in sec07, "Baseline parameters 0.20 missing from sec07_steering.tex"

def test_find07_energy_flux_index():
    """FIND-07: Ensure divergence index on double stress power in Appendix B aligns with M17."""
    appB = (LATEX_DIR / "appB_energy_flux.tex").read_text(encoding="utf-8")
    assert r"\tau_{ikj} \dot{u}_{i,k}" in appB or r"\tau_{ikj}\dot{u}_{i,k}" in appB, (
        "Index placement in double stress flux term must have divergence index in third position (tau_{ikj})"
    )

def test_find08_operational_resolution_floor_notation():
    """FIND-08: Ensure resolution floor in Sec 5.7 references omega_T per Table 6."""
    sec05 = (LATEX_DIR / "sec05_verification.tex").read_text(encoding="utf-8")
    assert r"\bar{\omega}_T^{(32)}" in sec05, (
        "Resolution floor equation in sec05_verification.tex must reference omega_T"
    )

def test_find06_verb_validates_removed():
    """FIND-06: Ensure informal 'validates' is replaced in Sec 7.4."""
    sec07 = (LATEX_DIR / "sec07_steering.tex").read_text(encoding="utf-8")
    assert "This validates the constitutive role" not in sec07, (
        "Informal use of 'validates' must be replaced in sec07_steering.tex"
    )

def test_find01_fig06_caption_and_data_traceability():
    """FIND-01: Ensure Fig 6 caption correctly describes AR=10, Table 2 params, and delta_GX = +0.0431."""
    sec06 = (LATEX_DIR / "sec06_results.tex").read_text(encoding="utf-8")
    assert r"\mathrm{AR} = 10" in sec06, "Fig 6 description must state AR=10"
    assert r"\ell_{\mathrm{i}} = 0.20\,\mathrm{m}" in sec06 or r"\ell_{\mathrm{i}} = 0.20" in sec06, (
        "Fig 6 caption must list ell_i = 0.20 m matching Table 2"
    )
    assert r"\mu = 1.0\,\mathrm{Pa}" in sec06, "Fig 6 caption must list mu = 1.0 Pa matching Table 2"
    assert r"\rho = 1.0\,\mathrm{kg/m}^3" in sec06, "Fig 6 caption must list rho = 1.0 kg/m^3 matching Table 2"
    assert r"\Delta_{GX} = +0.0431" in sec06 or r"\Delta_{GX} = 0.0431" in sec06, (
        "Fig 6 must cite verified gap Delta_GX = +0.0431 for AR=10 at theta=45 deg"
    )
    assert "0.0898" not in sec06, "Rogue value 0.0898 (flux ratio) must not appear in sec06_results.tex"

def test_find02_design_map_max_gap_reconciliation():
    """FIND-02: Ensure maximum directional gap 0.0896 (at theta=30 deg, AR=10) replaces 0.1654."""
    for fname in ["sec06_results.tex", "sec08_discussion.tex", "sec09_conclusions.tex"]:
        text = (LATEX_DIR / fname).read_text(encoding="utf-8")
        assert "0.1654" not in text, f"Outdated value 0.1654 still present in {fname}"
        assert "0.0896" in text, f"Verified maximum gap 0.0896 missing from {fname}"

def test_find03_theta_sweep_migration_values():
    """FIND-03: Ensure theta-sweep mode drop values match raw data (2.915 -> 2.672 and 5.050 -> 4.628)."""
    sec06 = (LATEX_DIR / "sec06_results.tex").read_text(encoding="utf-8")
    assert "1.154" not in sec06 and "0.812" not in sec06, (
        "Spurious values 1.154 / 0.812 must be removed from sec06_results.tex"
    )
    assert "2.915" in sec06 and "2.672" in sec06, (
        "Transverse acoustic drop 2.915 -> 2.672 missing from sec06_results.tex"
    )
    assert "5.050" in sec06 and "4.628" in sec06, (
        "Longitudinal acoustic drop 5.050 -> 4.628 missing from sec06_results.tex"
    )

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
