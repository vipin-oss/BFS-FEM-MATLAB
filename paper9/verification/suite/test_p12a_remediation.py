"""P12A remediation guard tests.

G1: the corrected B3 source-figure claim can never regress to "Fig. 4(c)
    sweeps tau_R" (the tau_R sweep is the source's Figure 7; fig4c_raw.png is
    pixel-identical to Figure 7 -- P12A finding, verified by byte comparison
    of the source PDF embedded images).
G2: the B2 registry semantics state the SOURCE normalization l_bar = l/b
    (b = a_A + a_B), with the engine-side l/a convention recorded separately.
G3: the fig4c overlay is built from the GENUINE Fig. 4 raster
    (li2023_p15_img1_Im1.png) rendered in grayscale, and the identification
    note exists.
G4: PCR6 closure -- every B1/B2/B3 parameter family reaching the results is
    present and tagged in params_master.yaml and in regenerated Table 2.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load(path: Path):
    with open(path) as f:
        return json.load(f)


def test_g1_tau_r_claim_never_regresses():
    """No live evidence/generator/manuscript file may claim Fig. 4(c) sweeps tau_R."""
    files = [
        REPO_ROOT / "paper9/audit/benchmark_evidence.json",
        REPO_ROOT / "paper9/audit/traceability_matrix.json",
        REPO_ROOT / "paper9/audit/p11d_regenerate_evidence.py",
        REPO_ROOT / "paper9/figures/gen/fig04_benchmark_validation.py",
        REPO_ROOT / "paper9/latex/sections/sec05_verification.tex",
        REPO_ROOT / "paper9/tables/out/tab03_anchor_errors.tex",
    ]
    import re
    bad_claim = re.compile(r"4\(c\)[^\n]{0,160}sweeps?\s*(?:\$?\\\\?tau|tau)", re.I)
    for f in files:
        txt = f.read_text()
        assert not bad_claim.search(txt), f"{f} regressed to the false 'Fig. 4(c) sweeps tau_R' claim"
    # and the corrected truth must be present in the live registry
    ev = _load(REPO_ROOT / "paper9/audit/benchmark_evidence.json")
    b3 = ev["benchmarks"]["B3"]
    assert "Fig. 7" in b3["parameter_source"]
    assert "3(b)" in b3["parameter_source"] and "[S]" in b3["parameter_source"]


def test_g2_b2_registry_semantics_source_normalization():
    reg = _load(REPO_ROOT / "paper9/results/raw/p11d_b2_gap_registry.json")
    sem = reg["parameter_semantics"]
    assert "l / b" in sem["l_bar"], "source l_bar = l/b definition must be stated"
    assert "b = a_A + a_B" in sem["l_bar"]
    assert "Li et al. (2024)" in sem["ambiguity_status"], "wrong-year citation must not return"
    # provenance note of the P12A prose-only correction must be present
    assert "p12a_note" in reg
    # numeric integrity: three configs with derived statuses still present
    assert set(reg["configs"]) == {"CFG-DIM-MICRO", "CFG-DIM-MACRO", "CFG-BAR-MACRO"}


def test_g3_fig4c_overlay_uses_genuine_figure4():
    src = (REPO_ROOT / "paper9/audit/p11d_regenerate_evidence.py").read_text()
    assert "li2023_p15_img1_Im1.png" in src, "overlay must embed the genuine Fig. 4 raster"
    assert 'cmap="gray"' in src, "grayscale raster must render in grayscale, not false colour"
    note = REPO_ROOT / "paper9/audit/evidence/fig4c_raw_IS_FIGURE7.md"
    assert note.exists(), "misidentification note must exist beside the retained raster"
    assert "Figure 7" in note.read_text()
    assert (REPO_ROOT / "paper9/audit/evidence/fig4c_overlay.png").exists()
    # the genuine raster is the 1500x437 grayscale Fig. 4, not the 1500x354 Fig. 7
    from PIL import Image
    im = Image.open(REPO_ROOT / "paper9/audit/evidence/li2023_p15_img1_Im1.png")
    assert im.size == (1500, 437)
    im7 = Image.open(REPO_ROOT / "paper9/audit/evidence/fig4c_raw.png")
    assert im7.size == (1500, 354)


def test_g4_pcr6_b1b2b3_registry_rows_present_and_tagged():
    with open(REPO_ROOT / "paper9/params/params_master.yaml") as f:
        params = yaml.safe_load(f)["parameters"]
    fams = {"b1_": 0, "b2_": 0, "b3_": 0}
    for k, v in params.items():
        for fam in fams:
            if k.startswith(fam):
                fams[fam] += 1
                assert v["tag"] in ("[C]", "[A]", "[S]"), f"{k} missing provenance tag"
                assert v["source"].strip(), f"{k} missing source"
    assert fams["b1_"] >= 10, fams
    assert fams["b2_"] >= 8, fams
    assert fams["b3_"] >= 10, fams
    # inherited B3 values must be [S], never [C]
    assert params["b3_cbar_1"]["tag"] == "[S]"
    assert params["b3_dbar_1"]["tag"] == "[S]"
    # the ambiguity statement must accompany the B2 caption rows
    assert "AMBIGUOUS" in params["b2_l_caption"]["unit"]
    # regenerated Table 2 must contain the rows
    tab = (REPO_ROOT / "paper9/tables/out/tab02_parameters.tex").read_text()
    for frag in ("DIM-MICRO", "$\\bar{c}_1$", "$\\mu_1$", "$l{=}l_1{=}f{=}0$", "[S]", "[A]"):
        assert frag in tab, f"Table 2 missing {frag}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
