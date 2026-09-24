# P4B R-1 — Pipeline Reproducibility Audit

Date 2026-09-24 · HEAD `6f7850dd4f6947ed001e9489d4d7f8217a4804df` (branch `phase-1-symbolic`) ·
P12C base `0d985029`. No push · no P12E · no P12C calculation · no new scientific production ·
no change to any authoritative artifact. Evidence: existing committed data + small probes
(`/home/user/p4b_remediation_logs/partA_probe.py`, `partBD_probe.py`).

**Terminology (used strictly).**
*Artifact-level reproducibility* — the committed artifact's values re-derive from its own data and
its provenance is established. *Pipeline-level reproducibility* — re-executing the production path
returns the same reported quantity within a stated tolerance. *Solver-level determinism* —
executions return bit-identical eigenvalues. *Scientific validation* — independent physical
evidence confirms the quantity measures what it claims (not addressed here).

## 1. The complete path, stage by stage

| # | stage | code | determinism class | evidence |
|---|---|---|---|---|
| 1 | matrix assembly | `assemble_nxn_bloch` (l.117) → `p4a.assemble_KM` (local 32×32 element, phase folding `red`, conjugate-phase scaling, CSR + 0.5(A+Aᴴ) Hermitisation) | **deterministic** | repeated builds in one process: K/M CSR content hashes identical at n = 8 (`995ad3727f727cdd`, 36518 nnz) and n = 16 (`e0a3e09d53517ce2`, 145840 nnz) |
| 2 | eigenproblem definition | K̄, M̄ from stage 1; `acoustic_omegas` l.171 | **deterministic** | same matrices ⇒ same generalised problem (K̄, M̄ content-hashed above); branch selection by size: nd ≤ 128 → dense (`geigh`, l.176), else iterative (`eigsh`, l.179) |
| 3 | numerical eigensolver realization | `geigh` (dense, n = 4, nd = 128) / `eigsh(which="SM", tol=1e-12, maxiter=10000)` **no start vector** (n = 8, 16, 32) | **NOT deterministic per call; dense path deterministic per configuration only** | n = 8, four calls on identical matrices: 1.16485539021267592 / …21263240 / …21260665 / …21267859, spread 7.2e-14, 4 distinct values; n = 16 two calls differ 9.9e-14, n = 32 two calls differ 5.5e-13 (B1 probes); explicit `v0` ⇒ bit-identical (0.0) |
| 4 | post-processing | ω extraction (`sort`, `sqrt(max(λ,0))`, first mode), `rel_err` (l.420), `d16_32` (l.426), `eps_delta` (l.437) | **deterministic** | repeated evaluation on identical ω arrays gives bit-identical `(rel_err, d16_32, eps)` tuples |
| 5 | fit-subset selection | `use.append` under `if e > 1e-14` (l.429-432); `len(use) >= 3` gate (l.433) | **deterministic given the ω array — but its input is a stage-3 quantity** | the predicate compares `err32` against a constant whose equivalent ω-window is ±1.165e-14 abs — *narrower* than the solver's own call-to-call jitter at n = 32 (1e-13 … 5e-13) |
| 6 | regression + reporting | `lsq_loglog_slope` (l.184), CI via Student-t, JSON write (l.515-527) | **deterministic given the subset** | OLS reimplementation reproduces the reported slope/CI exactly for both committed runs |

## 2. Which stage causes the branch selection — and why it is inevitable

The branch (3-point vs 4-point fit) is decided **only** by stage 5 acting on stage 3's noise.

- The inclusion predicate `err32 > 1e-14` is equivalent to
  `|ω₃₂ − ω_ex| > 1.1649e-14` (dimensionless). The *entire* decision window is 2.33e-14 wide.
- Stage 3's own variability at n = 32 is **1e-13 … 5e-13** (probes; identical matrices, same
  process). The window is therefore **smaller than the solver's own jitter** by roughly one order of
  magnitude: the predicate is not resolving discretization physics, it is sampling solver noise.
- Committed evidence sits on opposite sides of that window by chance:
  run 2 ω₃₂ = 1.1648553893289162 → |Δω| = 2.887e-15 → **excluded** (3-point fit);
  run 1 ω₃₂ = 1.1648553893287734 → |Δω| = 1.399e-13 → **included** (4-point fit).
- Consequence for the reported quantity: under the deployed rule the slope over the 21 documented
  realizations spans **4.173919 … 5.497868 (26.6 %)**, with 20/21 draws taking the 4-point branch.
  Under a rule that fixes the subset (or the comment's own 10·min_err rule) all 21 draws take the
  3-point branch and the slope spans **4.173919 … 4.183199 (0.222 %)**.
- The second reported quantity, ε_Δ = max(d16_32, err32), is also realization-dependent:
  **4.5505e-11 … 4.6790e-11 (2.78 %)** across the same realizations; the quoted 4.63e-11 is the
  governing run's realization.

## 3. Determination

| question | answer |
|---|---|
| Where does the branch selection originate? | Stage 5's fixed `1e-14` cut applied to a stage-3 (solver-noise-limited) input at n = 32. Stages 1, 2, 4, 6 are deterministic and are *not* involved. |
| **Artifact-level reproducibility** of the governing JSON | **Established.** Slope 4.173919246515192, CI [3.1453687594104447, 5.202469733619939], ε_Δ 4.6318154949690315e-11 re-derive exactly from the committed ω array under the code's own rule; provenance fixed by B1. |
| **Pipeline-level reproducibility** of the reported slope | **NOT achieved** (R-1 open). A fresh execution normally reports a 4-point value (4.64 … 7.16); only ~1-in-21 draws reproduce the recorded branch. |
| **Solver-level determinism** | **Not achieved** for the iterative path (unpinned start vector); the dense path is deterministic *within a fixed thread configuration* (documented G-1 evidence: 1.164855406907999 vs …80328). |
| **Scientific validation** | Not attempted or claimed here; no independent physical confirmation of p = 4.17 exists or is asserted. |
| Does the manuscript's 4.17 become "wrong"? | No. It is the recorded run's value, it lies inside the 0.222 % stable 3-point band, and the abstract states "no theoretical order claimed". The exposure is *reproducibility*, not correctness. |

## 4. Consumer impact (no action taken)

The reported slope flows to Table 6 / Figure 5 / the manuscript text via the committed JSON only
(verified: `tab04`, `tab06`, `fig05`, `p5_core`, guards). None of them re-derive the slope, so the
pipeline exposure is confined to *future regenerations* of the governing JSON; the committed
manuscript artifacts are unaffected.

## 5. R-1 status

**OPEN — requires explicit re-baselining authorization before any fix.** Both candidate remedies
diagnosed (Part B of `P4B_POST_B1_REMEDIATION_READINESS.md`) change the executed production rule, so
per this task's constraints nothing was implemented. Until then the correct characterisations are:
artifact-level reproducibility (established), pipeline-level reproducibility (not established),
solver-level determinism (not established for the iterative path), scientific validation (absent).
