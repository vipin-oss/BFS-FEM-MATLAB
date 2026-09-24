# P12C Gate / PCR Forensic Audit (Part F)

Base `phase-1-symbolic @ 0d985029` (plus Parts A–E commits applied) · 2026-09-24.
Rule followed: **Blueprint v1.3 §10 definitions are authoritative; no gate is redefined, and
no status is promoted because tests pass.** Blueprint file hash re-verified in this audit:
`Paper9_Blueprint_v1.3.tex` = `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`
(unchanged by every P12A/P12B/P12C commit).

## 1. Frozen definitions (Blueprint v1.3 rev. 2, §10)

- **PCR1** all mandatory published benchmarks (Layers 1, 2a, 2b) PASS, max relative error ≤2 %
  (0.5 % only for the classical limit).
- **PCR2** benchmark configurations/parameters/assumptions/non-dimensionalisation/curves/errors
  in the **main manuscript**.
- **PCR3** analytical checks: closed-form dispersion (Layer 3), App. A high-k asymptotics,
  App. B energy-flux identity.
- **PCR4** the eight-test internal consistency suite (Layer 5) passes and is tabulated (Table 4).
- **PCR5** mesh convergence with **observed** rate (LSQ, 95 % CI) and resolution floor ε_Δ
  (Fig. 5, Table 6).
- **PCR6** every material/geometric/microstructural parameter provenance-tagged [C]/[A]/[S]
  (Table 2); no untagged number reaches the results.
- **PCR7** every major physical claim quantitatively supported: orientation gaps (normalised
  widths, S_θ, Table 5), wave steering (δ_max **and** a steering figure-of-merit, Fig. 12),
  micro-inertia necessity (App. A proof **and** Fig. 13(b)).
- **PCR8** novelty statements hedged; research gap objectively visible in Table 1.
- **G1** symbolic checks pass (week-1/2–3) · **G2** all 8 automated internal tests pass (week 6)
  · **G3** ≤2 % on all three external anchor layers (hard gate, do-not-submit rule) ·
  **G4** submission-ready release; PI signs G4 only after PCR1–PCR8 are checked; a failed PCR
  blocks submission exactly as G3 does.

## 2. Status matrix — verified in this audit, nothing promoted

| Item | Status now | Authority (most recent) | Verified here |
|---|---|---|---|
| PCR1 | **NOT MET / NOT PASS** | P11D mapping; P12A table; P12B §6 (“unchanged”) | external ≤2 % still uncomputable: no author numerical tables; no digitisation claims (sec05/§5.1 declarations) ✓ |
| PCR2 | **PASS** | P12A | B1/B2/B3 configurations, parameters, ambiguity preservation and N/A (Graphical Only) policy present in main text ✓ |
| PCR3 | **PASS** | P11D / P12A | 5g/5h evidence in Table 4 + App. A/B; guards recompute ✓ |
| PCR4 | **PASS** | P11D / P12A | Table 4 = 5a–5h; all rows PASS; Part C aligned §5.2 text to it ✓ |
| PCR5 | **PASS** (scoped to Layer-5 Case-H) | P11D mapping | Fig. 5 + Table 6 from the JSON; observed rate, CI, ε_Δ definition correct after Part E fix ✓ |
| PCR6 | **PASS** | P12A | Table 2 registry complete for B1/B2/B3; tags [C]/[A]/[S] ✓ |
| PCR7 | **PASS** | P12B (§6; new evidence) | δ_max (2.79°) ✓, steering FoM M_s reported (sec07/sec09; `fig12`, `fig14` present; `test_p12b_steering_fom.py`) ✓, micro-inertia App. A + `fig13` ✓ — promotion was made on delivered evidence, not on a green test |
| PCR8 | **PASS** | P11D / P12A | Table 1 with reported-quantity column ✓ |
| G1 | **MET** | P11D / P12A | symbolic/analytical evidence unchanged ✓ |
| G2 | **MET** | P11D / P12A | suite green (72/72 at this base; 5a–5h tabulated) ✓ |
| G3 | **NOT MET** | P11D / P12A / P12B — all “unchanged” | hard gate: no author float tables; B2 length-scale ambiguity preserved, not resolved ✓ |
| G4 | **NOT MET** | P11D / P12A / P12B — all “unchanged” | cannot be signed while G3/PCR1 unmet (blueprint: a failed PCR blocks submission exactly as G3) ✓ |
| P5 gate | **NOT PASS / OPEN** (two parallel pipelines; reconciliation outstanding) | `audit/P5_STATUS.md`, `audit/P5_READINESS.md` (pre-P12E versions in this tree) | manuscript contains **no** P5-production claims (grep: zero “production/P5” hits in `latex/sections/`); no basis for promotion |

P12C-specific effects checked: the Case-C 32²/64² work does **not** touch PCR1–PCR8 statuses or
G1–G4 statuses (no external anchor data; no new gate evidence claimed). P12C guard tests assert
only the Case-C evidence invariants (Parts A/B/G), never gate status.

## 3. Explicit no-promotion checks (all negative findings)

- No file in this tree claims G3 or PCR1 promotion; the newest statements (P12B §6) reaffirm
  NOT MET.
- P6/P9-era audits (`P6_FINAL_GATE_AUDIT.md`, `P9_FINAL_RELEASE_AUDIT.md`) use a **historical
  PCR numbering** (e.g. “PCR1 = Layer-1 classical limit”). They pertain to pre-P11 phases and
  are superseded by `P11D_PCR_MAPPING.md`; they must not be used to re-derive current statuses
  (catalogued in Part I).
- The blueprint’s own note (rev 1.2 → 1.3, editorial only) keeps G2 wording “all 8 automated
  internal tests” — consistent with Table 4 (5a–5h) and §5.2 after Part C.
- Gate G4 signature is a PI procedural act; no file in this repo signs it, so G4 remains NOT MET
  on both substantive (G3/PCR1) and procedural grounds.

## 4. Blockers that keep the release gate red (unchanged, evidence-based)

1. **G3/PCR1**: external quantitative ≤2 % impossible without author-released tables
   (B1–B3 graphical-only; B2 l/l̄ ambiguity preserved).
2. **P5**: production-map reconciliation outstanding (pre-P12E state; no P12E evidence here).
3. **P4B json↔txt divergence** (Part E, E-F1) — evidence-quality item, not a gate redefinition;
   feeds Part K blockers.
4. Case-C complete gap intentionally **not** mesh-converged → no converged-width claim may be
   made (blueprint-compatible; recorded as a scope limitation, not a gate).
