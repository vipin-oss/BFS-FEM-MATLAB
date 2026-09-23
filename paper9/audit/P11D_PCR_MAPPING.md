# P11D PCR Mapping — Blueprint v1.3 §10.4 (definitions authoritative)

Date: 2026-09-23.  Mapping: Blueprint §10.4 definition → manuscript location →
audit trail → evidence → status (re-evaluated from evidence in P11D; P11C
statuses noted where changed).  Blueprint terminology is authoritative; no PCR
is redefined here.

| PCR | Blueprint §10.4 definition (abridged) | Manuscript | Audit | Evidence | P11C status | P11D status |
|---|---|---|---|---|---|---|
| PCR1 | All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with max relative error ≤ 2% (0.5% target only for the classical limit) | Sec. 5.1 (B1/B2/B3 paragraphs), Table 3 | P11A/B/C findings CF-2, CF-5; P11D_REMEDIATION_AUDIT §12 | benchmark_evidence.json (quantitative_error: null for B1–B3 — author tables unreleased); internal Level-1/2 residuals only | PARTIAL | **NOT MET** — external ≤2% relative error is not computable without author-released numerical tables (G3); internal-identity residuals and graphical comparisons do not satisfy the Blueprint definition. B2 additionally carries an unresolved source l/l̄ ambiguity. |
| PCR2 | Benchmark configurations, exact parameters, model assumptions, non-dimensionalisation, reproduced dispersion curves, numerical comparisons and relative errors all appear in the MAIN manuscript | Sec. 5.1 items B1/B2/B3; Fig. 4 + caption; Table 3 | P11D_REMEDIATION_AUDIT §11 (claim audit) | fig04_benchmark_validation.pdf (present calculations, honest scope labels); p11d_b2_gap_registry.json; p11d_b3_run_P11D-B3-R1.json | PASS (caveat Fig. 4) | **PASS** — configurations/parameters/assumptions/non-dim curves are in the main text; external relative errors cannot exist and their absence + reason is stated in the main text (Table 3 footnote d); Fig. 4 scope corrected in P11D (present calculations only; qualitative graphical comparison; no error %). |
| PCR3 | Analytical checks pass: closed-form dispersion (Layer 3), Appendix A high-k asymptotics, Appendix B energy-flux identity | App. A, App. B; Table 4 rows 5g/5h | P3/p4b pipeline | p4b_5g_to_5i results; tab04_consistency_suite | PASS | **PASS** (unchanged) |
| PCR4 | The eight-test internal consistency suite (Layer 5, with PCR5) passes and is tabulated (Table 4) | Sec. 5.2; Table 4 | P4A/P4B scripts | tab04_consistency_suite.tex (5a–5h) | PASS | **PASS** (unchanged) |
| PCR5 | Mesh convergence demonstrated with observed rate (least-squares fit, 95% CI) and resolution floor ε_Δ reported (Fig. 5, Table 6) | Sec. 5.3; Fig. 5; Table 6 | P4B 5i | tab06_convergence_floor; fig05 | PASS | **PASS** (unchanged; scoped to the Layer-5 Case-H sequence. The Case-C complete-gap sequence is a separate study and is reported in Sec. 6 with its own honest trend: decreasing, not mesh-converged.) |
| PCR6 | Every material, geometric and microstructural parameter carries a provenance tag [C]/[A]/[S] (Table 2); no untagged number reaches the results | Table 2 (rows 6–30+); Sec. 5.1 | P3_TV_RESOLUTION (P11D addendum); traceability_matrix TV1 retag | tab02_parameters.tex (tagged rows); TV1 now [S]; B3 c̄/d̄ tagged [S] in Sec. 5.1; B2 l/l̄ semantics + ambiguity documented in Sec. 5.1 and p11d_b2_gap_registry.json | PARTIAL | **PARTIAL** — the ambiguous/derived values are now correctly tagged (TV1 [C]→[S]; B2 ambiguity documented), but the B1/B2/B3 benchmark parameter rows are still absent from the Table-2 registry (they are stated in Sec. 5.1 with in-text provenance). Closing this requires adding registry rows, not retagging. |
| PCR7 | Every major physical claim quantitatively supported: orientation-controlled gaps (normalised gap widths, S_θ, Table 5), wave steering (δ_max and a steering figure-of-merit, Fig. 12), micro-inertia necessity (Appendix A proof and Fig. 13(b)) | Sec. 6.4/Table 5; Sec. 7/Fig. 12; App. A/Fig. 13(b) | P11D_REMEDIATION_AUDIT §11 | tab05_gap_summary; fig12 (δ_max = 0.01°, 1.41°, 2.79° reported); appA | PARTIAL | **PARTIAL** — orientation gaps (S_θ, Table 5) and micro-inertia (App. A + Fig. 13(b)) are quantitatively supported; wave steering reports δ_max but the Blueprint-required steering FIGURE-OF-MERIT is not defined or reported. Not fabricated in P11D. |
| PCR8 | Novelty statements hedged per writing conventions; research gap objectively visible in Table 1 incl. reported-quantity column | Sec. 1; Table 1 | P11C | tab01_literature_positioning | PASS | **PASS** (unchanged) |

## Gate re-evaluation (Blueprint §10)

| Gate | P11C | P11D | Basis |
|---|---|---|---|
| G1 (analytical) | MET | **MET** | PCR3 evidence unchanged |
| G2 (internal verification) | MET | **MET** | PCR4/PCR5 evidence unchanged |
| G3 (external quantitative ≤2%) | NOT MET | **NOT MET** | Policy-fixed: graph/source-equation evidence and qualitative overlays do NOT satisfy the gate; no author numerical tables exist; no values invented |
| G4 (publication readiness) | PARTIAL | **NOT MET** | G3 NOT MET and PCR1/PCR6/PCR7 not fully met — G4 cannot be PASS while mandatory requirements are unmet (Blueprint: a failed PCR blocks submission exactly as G3 does) |
