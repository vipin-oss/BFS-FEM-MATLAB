# REVIEWER_RISK_AUDIT.md

Anticipated reviewer objections and where the manuscript/package answers
each. Status column: MITIGATED = answered in the current manuscript;
DECLARED = openly stated limitation; WATCH = check again at submission.

| # | Likely objection | Response in manuscript/package | Status |
|---|---|---|---|
| 1 | Parameters are surrogate/composite — "results are not for a real material" | §7.9 declares the set composite and partly surrogate; provenance/PARAMETER_PROVENANCE.md itemizes every value (ρ, c_e surrogate; ρ_w=ρ declared; k11 discrepancy vs li2017 declared) | DECLARED |
| 2 | B and C are numerically indistinguishable — "is there any point to Model C?" | Framed as a resolution-resolvable-region result (95/121 below benchmarked floor; gates show exact limits); Δ_AC ≈ 0.334 shows the method resolves what is resolvable | MITIGATED |
| 3 | "Differences below 1e-5 are roundoff" | Resolution floor is benchmarked (resolution_bench.csv), not assumed; 1e-16 dips retained, shaded, explained as cancellation reproduced at ≤3.3e-9 | MITIGATED |
| 4 | Phason BC choice barely matters (≤8.06e-6) — "why study it?" | Precisely because it is below/near the floor: it quantifies when BC modelling effort is justified; growth toward high Ω* documented | MITIGATED |
| 5 | Passive φ (decoupled electric potential) in Configuration I | Configuration and decoupling stated with the BC set; piezoelectric coupling enters via the constitutive set of the 2D-hex PQC; full electrostatic problem flagged as future work | DECLARED |
| 6 | No experimental comparison | Scope statement in abstract/intro; quasi-crystal experimental data for these coupled modes not available in literature | DECLARED |
| 7 | Semi-analytical vs FEM | Determinant/root method is the standard for half-space surface waves (barnett1985 lineage); no FEM by design; two-path validation (V1) | MITIGATED |
| 8 | "0.934208 vs 0.9326028 discrepancy" | Legacy coarse-scan record labelled and excluded; production value 0.932602758 with provenance in audits | MITIGATED |
| 9 | 1D-hex vs 2D-hex literature mix | Reference framing separates the two point-group families (literature/ categories) | MITIGATED |
| 10 | τ0 sweep is computational, not measured | τ0 declared computational parameter; sweep design in grids.json; Study 3 framed as sensitivity | DECLARED |
| 11 | deboissieu2012 page range missing in bib | Flagged in provenance/REFERENCE_PROVENANCE.md; fix before camera-ready | WATCH |
| 12 | Journal metrics/fit | AMM-Engl. Ed. (JIF 4.9) primary, Acta Mechanica (JIF 4.0) backup; re-verify at submission | WATCH |
| 13 | Reproducibility doubts | One command (run_all.py), 22-check invariant gate, checksums, clean-room reports (audits/CLEAN_ROOM_REPRODUCTION_REPORT.md) | MITIGATED |
