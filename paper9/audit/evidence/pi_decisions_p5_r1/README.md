# Evidence bundle — P5 common-point cross-check and R-1 deployed-configuration reproducibility

**Purpose.** Raw supporting evidence for the two decision records prepared for PI signature:
`paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md` and `paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md`.
This bundle **supports** those records; it changes **no** status, number, threshold or gate. In particular
C-1 is untouched, P5 remains `NOT PASS/OPEN`, R-1 remains `OPEN`, and B2/B3 remain `NOT_VALIDATED`.

**Provenance.** Both measurements were executed on 2026-09-24 from the repository's own frozen modules at
HEAD `ca57a9d55774fadcbe1c5d17bf929fc8fa3ec516` (branch `phase-1-symbolic`, tri-equal), in a scratch workspace
outside the repository. They were committed afterwards into the repository as separately instructed (this
bundle; no record, register or artifact was edited to accommodate them). The scripts below are the **exact
files that ran** (byte-identical copies), so the as-executed output paths inside them are the workspace paths
of that run; the JSON/log files are the **as-executed outputs**.

**Supersession note.** `PI_DECISION_PACKAGE_P5_R1.md` §3 states that the raw artifacts are held outside the
repository and are not committed *by that package*. That statement was written at preparation time and remains
in that record unedited (no record was changed by this bundle); this bundle is the separate instruction
anticipated there.

---

## 1. Files (sha256)

| file | sha256 |
|---|---|
| `p5_common_point_crosscheck.py` | `32f9e7fb1851c3bcb3f52119e48e0128d51d839a262044eefa51373baf481594` |
| `p5_common_point_crosscheck.json` | `e6c053db40da59b2e5124ea9f2fc862d545c932d2c4e9ac8386f2359f1670036` |
| `p5_element_identity_two_configs.py` | `b5e99a6fa19695d7cb71d717ec3fb08329299b3c392d31001a5356548e94485c` |
| `p5_element_identity_two_configs_output.txt` | `5617b08509a5e00af1efeb98a4612af7641d028525c61a1784917ee2ee202315` |
| `r1_deployed_reproducibility.py` | `2af0a7d86b545a08f876f5300771b8fba9fe88877dabd21882eb0a2e689951d2` |
| `r1_deployed_reproducibility.json` | `8583c0c7c92d2c7763a3c0d415eb7ae2a17e99e8619c91df38daebc4a1b7a067` |
| `r1_deployed_reproducibility_stdout.txt` | `a3e2c2b6761061b0db9869e830a43124eb2dbf3996c075fd8812edc392608634` |

## 2. Measurement 1 — P5 common-point cross-check (the minimum comparison specified in the decision report)

**Question.** Are the two recorded P5 pipelines numerically different, or do they differ only in conventions
(path length, zone grid, reported band count, pilot orientation, AR parameterisation)?

**Method.** Both lineages evaluated at **both** pipelines' own operating points, at Γ, an interior point
k = (0.3π/L, 0.4π/L) and X, L = 1:

| config | semi-axes / orientation | L11 | L22 | L12 |
|---|---|---|---|---|
| Part A pilot | θ = 45°, AR = 3 area-preserving, l₁ = 0.3464101615, l₂ = 0.1154700538 | 0.0666666666666 | 0.0666666666666 | 0.0533333333335 |
| Part B pilot | θ = 30°, l₁ = 0.30, l₂ = 0.10 | 0.07 | 0.03 | 0.0346410161514 |

Lineage A: `paper9/solver/bfs_bloch_solver.py` (`assemble_KM` → `T_impl` → `reduce_mat`).
Lineage B: `paper9/verification/suite/p4b_5g_to_5i.py` (`assemble_nxn_bloch`, i.e. the frozen P4A/P4B assembly
reused by `paper9/production/p5/p5_core.py`).

**Results (from `p5_common_point_crosscheck.json`).**

| config | k | rel. \|ΔK\| | rel. \|ΔM\| | max \|Δω\| |
|---|---|---|---|---|
| Part A pilot | Γ | 6.9802e-16 | 1.1926e-17 | 3.4560e-09 † |
| Part A pilot | interior | 1.5704e-16 | 3.3562e-17 | 1.7764e-15 |
| Part A pilot | X | 2.3130e-16 | 1.7278e-17 | 4.8850e-15 |
| Part B pilot | Γ | 3.3391e-16 | 1.1926e-17 | 2.6390e-08 † |
| Part B pilot | interior | 4.9195e-16 | 3.3562e-17 | 2.6645e-15 |
| Part B pilot | X | 1.1529e-16 | 1.7278e-17 | 3.5527e-15 |

† Γ is the zero/rigid cluster: the eigenvalue differences are ±5.8e-16, which the ω = √(ω²) mapping amplifies
(the physical branches coincide with 0.0 difference; see `p5_element_identity_two_configs_output.txt` and the
decision record's caveat). The interior and X values are the meaningful ones.

**Element-level identity (independent script).** At both configurations the single-element K and M produced by
the two lineages are **bitwise identical** (`max|ΔK| = max|ΔM| = 0.000e+00`), captured in
`p5_element_identity_two_configs_output.txt`. That capture is a deterministic re-execution of the script
(32 × 32 element-matrix assembly only — no eigensolver involved, hence bit-reproducible) performed at commit
time; its result is identical to the as-cited run.

**Conclusion carried into the record.** The two lineages are operator-identical; the recorded divergence is
convention/sampling/scope, not numerics.

## 3. Measurement 2 — R-1 deployed-configuration reproducibility (the exact P12AB Part E specification)

**Question.** On the **deployed** 5i configuration (`tol = 1e-12`, unpinned §5.7 start vector, meshes 4², 8²,
16², 32²), do independent realizations change the admissible subset or the fit verdict under the frozen
Rule R-fit (F = 3 strict, SPREAD_FLOOR 1e-15, ≥ 3 admissible levels, per-level spread s = (max − min)/min ω)?

**Method.** `r1_deployed_reproducibility.py` imports the frozen suite module
`paper9/verification/suite/p4b_5g_to_5i.py` and calls its own `assemble_nxn_bloch` / `acoustic_omegas`; five
realizations in one process: three on the deployed path as shipped (unpinned) and two under the Route-F
two-seed protocol (PCG64 seeds 20260924, 7) **at the deployed tolerance** (Route-F's tol = 1e-14 is *not*
imposed, per the specification). k = (0.31π, 0.22π)/L, ω̄_exact = 1.1648553893289133. Nothing in the repository
was modified; the governing artifact was not regenerated.

**Results (from `r1_deployed_reproducibility.json`, stdout in `r1_deployed_reproducibility_stdout.txt`).**

| family | realizations | admissible subset | fit slopes | flips |
|---|---|---|---|---|
| deployed path as shipped (unpinned) | 3 | {4², 8², 16²} in all 3 | 4.1785620603 / 4.1789475735 / 4.1803898441 | 0 / 3 |
| two-seed protocol at deployed tol | 2 | {4², 8², 16²} in both | 4.1799676366 / 4.1805695819 | 0 / 2 |

Per-level spreads (deployed family): 0 (4², dense path), 3.431158e-14, 1.164688e-13, 4.064016e-13 (32²); the
32² level is excluded in every realization (largest measured error 5.686191e-13 against the admitted threshold
1.219205e-12). Two-seed family spreads: 0, 1.219967e-14, 3.831460e-14, 5.276359e-13; 32² excluded in both.
The manuscript's two-decimal value `p = 4.17` is invariant.

## 4. Reproduction

```bash
# from the repository root at the recorded HEAD
python3 paper9/audit/evidence/pi_decisions_p5_r1/p5_element_identity_two_configs.py     # element identity, both configs
python3 paper9/audit/evidence/pi_decisions_p5_r1/p5_common_point_crosscheck.py         # writes <workspace>/r1_evidence/p5_crosscheck_final.json
python3 paper9/audit/evidence/pi_decisions_p5_r1/r1_deployed_reproducibility.py        # ~2.5 min (32² ARPACK levels); writes /tmp/r1_measurement.json
```

The two scripts write to their as-executed output paths (outside the repository); redirect or patch the output
path if a different destination is wanted. No solver result, table, figure or stored artifact is touched by
either script.

## 5. Declared limits

* The Γ-point ω comparison is √-amplified in the zero/rigid cluster († above) and is quoted with that caveat.
* Thread pinning was not enforced in the R-1 measurement (Route-F pinned threads); the measured spread is
  therefore *larger* than a pinned run's, i.e. the reported margins are conservative.
* The R-1 measurement adjudicates the deployed **configuration**; it does not claim reproducibility of the
  stored artifact itself (Property B), which is why the decision record's §5 states that limit explicitly.
* Nothing here validates any external benchmark: B1 stays `GRAPHICAL_VALIDATION/PASS`, **B2 and B3 stay
  `NOT_VALIDATED`** (`quantitative_error` NULL).
