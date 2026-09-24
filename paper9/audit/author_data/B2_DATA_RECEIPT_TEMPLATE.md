# B2 — Author-Data Receipt Template (Layer 2a — strain-gradient, Li et al. 2024 Fig. 2(b))

**Template only — contains placeholders. No value has been received and no value may be entered
until the actual data arrive. Do not fill any field with an estimate.**

Governed by: `paper9/audit/P12M_AUTHOR_REQUEST_DRAFTS.md` §4 (acceptance protocol) and
`paper9/audit/P12L_AUTHOR_DATA_REQUEST_SPEC.md`. Thresholds are the existing ones — ≤ 2 % mandatory,
≤ 0.5 % classical-limit target for B1 only.

## 1. Source identity
| Field | Value |
|---|---|
| Benchmark | B2 (Layer 2a — strain-gradient, Li et al. 2024 Fig. 2(b)) |
| Source article | Li, Li, Guo, Wang & Wang, *Scientific Reports* **14**:24035 (2024), DOI 10.1038/s41598-024-75049-1 |
| Published item the data correspond to | Fig. 2(b) (f = 0, F = 0; AlN/BaTiO₃ bilayer with internal length scales) |
| Request sent (date / by whom) | `<pending>` |
| Response received (date) | `<pending>` |
| Provider / author attribution | `<pending>` |
| Provider's stated caveats | `<pending>` |

## 2. Received file(s)
| Field | Value |
|---|---|
| File name | `<pending>` |
| Format | `<pending>` (CSV / TXT / XLSX / MAT / JSON / other) |
| SHA-256 of the received file, unmodified | `<pending>` |
| Archived at (repository path) | `paper9/audit/author_data/<pending>` |
| Byte count | `<pending>` |
| Was the file modified in any way? | **must be recorded as NO or the file is re-archived** |

## 3. Correspondence and conventions
| Field | Value |
|---|---|
| Figure/table correspondence confirmed | `<pending>` |
| Interpolation/rounding performed by the provider | `<pending>` |
| Units of each column/quantity | `<pending>` |
| Normalisation of ω̄ | `<pending>` |
| Normalisation of k̄ | `<pending>` |
| Branch indexing (which branch is which) | `<pending>` |
| Boundary/interface conditions (where not already unambiguous) | `<pending>` |
| Numerical precision / generating tool (if stated) | `<pending>` |
| **`l` vs `l̄` — RESOLUTION (blocking)** | `<pending>` — must explicitly state: dimensional `l` (m) **or** normalised `l̄`; the normalising length and its value; the `l₁` convention; the coefficient convention (e.g. μ₀ = c₃₃ l²) |
| **Is the ambiguity resolved?** | `<pending>` — **if NOT resolved, this template cannot be completed and B2 stays blocked regardless of any data supplied** |

## 4. Parameters supplied
| Parameter | Value (as supplied) | Unit | Matches published text? |
|---|---|---|---|
| `<material 1: ρ, c33, thickness, length scales…>` | `<pending>` | `<pending>` | `<pending>` |
| `<material 2: ρ, c33, thickness, length scales…>` | `<pending>` | `<pending>` | `<pending>` |
| `<cell size / period>` | `<pending>` | `<pending>` | `<pending>` |
| `<length-scale values actually used in the figure>` | `<pending>` | `<pending>` | `<pending>` |

**Parameter/normalisation verification outcome:** `<pending>` — *(any mismatch must be resolved with the
provider before the comparison is used)*

## 5. Numerical data checksum / integrity
| Field | Value |
|---|---|
| Number of points supplied (curves) | `<pending>` |
| Gap-edge rows supplied | `<pending>` |
| First-four-branch-frequencies rows supplied (at stated k̄) | `<pending>` |
| Independent re-read of the file reproduces the same values? | `<pending>` |

## 6. Solver configuration used for the comparison run
| Field | Value |
|---|---|
| Script / entry point | `<pending>` (existing configuration only; no tuning) |
| Parameters used | **exactly as verified in §4** |
| Output artifact (JSON, archived) | `paper9/results/raw/<pending>` |
| Run date / environment | `<pending>` |

## 7. Comparison result
| Quantity | Author value | Independent value | Relative error |
|---|---|---|---|
| Gap edge 1 (lower) | `<pending>` | `<pending>` | `<pending>` |
| Gap edge 1 (upper) | `<pending>` | `<pending>` | `<pending>` |
| `<… further gap edges …>` | `<pending>` | `<pending>` | `<pending>` |
| Branch 1 at k̄ = `<pending>` | `<pending>` | `<pending>` | `<pending>` |
| Branch 2 at k̄ = `<pending>` | `<pending>` | `<pending>` | `<pending>` |
| Branch 3 at k̄ = `<pending>` | `<pending>` | `<pending>` | `<pending>` |
| Branch 4 at k̄ = `<pending>` | `<pending>` | `<pending>` | `<pending>` |
| **Maximum relative error** | — | — | `<pending>` |

## 8. Acceptance
| Field | Value |
|---|---|
| Acceptance threshold applied | **≤ 2 %** mandatory (no 0.5 % target for this benchmark) |
| Criterion met? | `<pending>` |
| PCR1 effect | `<pending>` — *(PCR1 status changes only when **all** mandatory benchmarks are closed)* |
| G3 effect | `<pending>` — *(completeness conditions also required)* |
| Evidence artifacts produced | `<pending>` |
| Reviewer (independent) | `<pending>` |
| Date of decision | `<pending>` |

## 9. Attestation
- No value in this template may be estimated, digitised, interpolated or inferred. `<pending>`
- Received file archived unmodified; hash recorded in §2. `<pending>`
- If the criterion is **not** met, the result is recorded as not met — the status is never adjusted to
  fit the data. `<pending>`
