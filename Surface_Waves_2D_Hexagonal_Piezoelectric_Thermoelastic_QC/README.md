# Surface Waves in 2D Hexagonal Piezoelectric Thermoelastic Quasicrystals

Semi-analytical study of surface (Rayleigh-type) waves in a
two-dimensional hexagonal **piezoelectric thermoelastic quasicrystal**
half-space, comparing three phason dynamic models, with a
resolution-floor-limited model-discrimination methodology and fully
programmatic, checksummed reproduction.

## 1. What this project contains

The complete research project: manuscript (TeX + PDF + BibTeX), production
solver, study drivers, validated raw numerical data, validation suite
(V0–V5) plus a 22-check invariant gate, figure-generation programs and the
generated vector figures (PDF + EPS), thirteen audits, categorized
literature metadata, four provenance documents, manifests with SHA-256
checksums, and a one-command reproduction pipeline. Everything needed to
read, reproduce, audit, edit, and submit the paper — no private files, no
chat history.

## 2. Scientific problem

Surface-wave propagation along the free surface (z = 0) of a 2D-hexagonal
(6mm-type, Laue class 10) piezoelectric thermoelastic quasicrystal
half-space z > 0. Unknowns: phonon displacements u_x, u_z; phason
displacements w_x, w_z; temperature increment θ (Configuration I; the
electric potential φ is passive/decoupled in this configuration). Harmonic
ansatz exp[i(kx + pz − ωt)]; decaying roots Im p > 0; surface-wave condition
det B = 0 (free-surface BCs: σ_zz = σ_xz = 0, H_xz = H_zz = 0 with the
thermal/phason conditions of the manuscript).

## 3. Mathematical formulation

Generalized (Lord–Shulman) thermoelasticity coupled to phason elasticity
with non-symmetric phason stress (H_xz ≠ H_zx), 10th-degree characteristic
polynomial in p; frequency degree: Model A = 10, Model B = 8, Model C = 10.
Nondimensionalisation with k0 = 2π×10⁶ m⁻¹ (declared scale, never a working
wavenumber); starred quantities throughout. Full statement in
`manuscript/FINAL_MANUSCRIPT.tex`.

## 4. Models A / B / C

- **A — inertial phason dynamics** (ρ_w ∂²w/∂t² term).
- **B — diffusive phason dynamics** (first-order relaxation, D_w friction).
- **C — telegraph-type phason dynamics** (wave-telegraph operator; the
  production model) + Lord–Shulman heat conduction with relaxation τ0.

Documented exact limits: C → B and C → A reproduced to gates 1.11e-9 and
3.27e-9 (`tests/V3`).

## 5. Numerical method

Depth-root (surface-impedance lineage, Barnett–Lothe) semi-analytical
method: assembly of the 5×5 pencil M(Ω*, k*, p), polynomial root finding
with polishing, admissibility filtering (Im p > 0), branch tracking,
surface-matrix determinant/singular-value evaluation. No mesh, no
discretisation of the half-space. Two independent computation paths agree
(`tests/V1`).

## 6. Why no FEM

The half-space surface-wave problem is exactly the setting where the
root/determinant method is standard and exact to machine precision; FEM
would add discretisation error below the resolution floor under study.
Validation is by symbolic checks, limit gates, and two-path agreement —
not by code-vs-code comparison.

## 7. Repository structure

```
manuscript/     FINAL_MANUSCRIPT.{tex,bib,pdf} + figures/ + supplementary/
figures/        make_all_figures.py, style.py, output/ (figN.pdf + FigNN.eps)
solver/         production solver (matrix, roots, branch, gates, records)
drivers/        5 study drivers (baseline, friction map, thermal, BC, roots)
tests/V0..V5/   validation suite
results/        raw/ (read-only accepted data), validation/, manifests/,
                processed/ (empty by design)
verification/   verify_invariants.py + typed evidence dirs + reports/
audits/         13 audit documents (final + historical)
literature/     all_references.bib (47) + categorized metadata
provenance/     PARAMETER / REFERENCE / DATA / FIGURE provenance
manifests/      FILE_MANIFEST, FIGURE_MANIFEST, LITERATURE_MANIFEST, CHECKSUMS
archive/        README (historical ZIPs excluded from git; SHAs recorded)
run_all.py      one-command pipeline
```

## 8. Installation

```bash
pip install -r requirements.txt          # numpy, matplotlib, pypdf
# LaTeX (for the manuscript): texlive-latex-base/-recommended/-extra
#                             + texlive-fonts-recommended
```

## 9. One-command reproduction

```bash
python3 run_all.py
```

Environment check → 22-check invariant gate → regenerate all 11 figures
from `results/raw/` → compile the manuscript (rerun-stable) → write
`REPRODUCTION_REPORT.md` with an explicit PASS/FAIL. Modes:
`--check-only` (science gate only), `--from-scratch` (re-run all drivers
and tests first). No absolute paths; no hidden dependencies.

## 10. Verification

`verification/verify_invariants.py` (22 checks, latest: **22/22 PASS**)
re-reads every headline value from the shipped raw data, including the
branch identity at Ω*=1000: V_C(D_w*→0) = 0.3107266158 with |ΔV| ≈ 2.4e-11
(the incorrect ~0.467 phonon branch is NOT selected). Any change to the
accepted baseline exits nonzero and stops the pipeline.

## 11. Figures

**All 11 scientific figures are generated programmatically from the shipped
raw numerical data** by `figures/make_all_figures.py` (no hand-drawn data,
no hand-typed result values, no smoothing/deletion of anomalies). Vector
outputs: `figures/output/figN.pdf` (authoritative) and `FigNN.eps`
(pdftops conversions; Fig10 carries one rasterized colour-mesh layer that
matplotlib's PDF backend embedded — identical in both formats). Captions
live only in the TeX. See `manifests/FIGURE_MANIFEST.md`,
`audits/FIGURE_DATA_TRACEABILITY.md`, `audits/SPIKE_AND_ANOMALY_AUDIT.md`.

## 12. Manuscript

`manuscript/FINAL_MANUSCRIPT.pdf` — 29 pages, 11 figures, 3 tables,
0 LaTeX errors/warnings/undefined references. Source: `.tex` + `.bib`
(47 entries). Journal-ready figure copies in `manuscript/figures/`.

## 13. Literature

`literature/all_references.bib` (47 verified entries; 29 web-verified
2026-09-06), categorized metadata in 7 topic folders, availability status
in `literature/MISSING_REFERENCE_PAPERS.md`. No copyrighted PDFs are
redistributed; nothing fabricated.

## 14. Provenance

`provenance/`: every parameter (with surrogate/declared labels), every
reference (verification method + flags), every data file (byte-copy chain
from the upstream accepted package, SHA-256 `b8178605…c4244ec2`), and
every figure (script → raw data mapping). Solver record hash
`8c0abbabe66776dd`.

## 15. Current status

COMPLETE and ACCEPTED; science frozen. See `PROJECT_STATUS.md`. Remaining
work is submission logistics (author block, funding/COI, camera-ready
reference fixes).

## 16. Limitations

Parameter set composite and partly surrogate (declared); no experimental
comparison; φ passive in Configuration I; sub-floor model differences are
resolution statements, not physical identities; τ0 sweep is computational.
Full list in `audits/REVIEWER_RISK_AUDIT.md`.

## 17. Citation

Authors to be supplied at submission (no author data is invented in this
archive). Until publication, cite as: *"Surface waves in 2D hexagonal
piezoelectric thermoelastic quasicrystals — manuscript and reproducible
archive, 2026-09-07 snapshot"* plus this repository URL and commit SHA.

## 18. License / usage note

Research archive. Code may be used and adapted with attribution to this
repository; manuscript text is the authors' work — do not redistribute the
PDF as your own. Third-party literature is NOT included; obtain via
publishers/DOIs.
