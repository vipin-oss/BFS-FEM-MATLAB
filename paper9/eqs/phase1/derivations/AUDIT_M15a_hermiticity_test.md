# PHASE-1 AUDIT RECORD — M15-a
## Blueprint eq. (68) `K̄(k) = K̄(−k)^H` and the Sec 4 / matrix-row 5a test: ruling

Status: **RESOLVED at the mathematical level — ruling (a)**; **blueprint amendment REQUIRED and
PROPOSED below, NOT applied** (awaiting explicit authorization). Blueprint v1.3 is unchanged
(sha256 `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`). M1–M9 mathematics
unchanged. M10 NOT STARTED. No numerical production, no published validation, no TV item.

Script: `scripts/audit_m15a_hermiticity_test.py` — **30 checks, all PASSED**
(`checks/audit_m15a_hermiticity_test.log`; deterministic, two consecutive runs byte-identical;
sha256 pre-run = post-run `bd801ef3a0ac1365e27f6be90826252852704f129805aa3f2d0d5b711580e505`).

Inputs (read-only): Blueprint v1.3 lines 403 (§4.5 row), 416 (pitfalls row), 587 (register
(66)–(68)), validation-matrix row 5a; `DERIVATION_M08.md`; `AUDIT_M8a_boundary_operator.md`
((O1)–(O6)); `DERIVATION_M09.md` §M9.7 (phase lemma), §M9.8 (flag), checks [C10], [C11],
[X1]–[X4]; `CALC_MASTER_PLAN.md` §A row M15 and §F14; `PHASE1_MANIFEST.md`; traceability matrix
row M15-a.

Independence policy. Nothing is imported from `m09_bloch_c1.py`. Every identity is re-derived
from the locked hypotheses only: (H1) `K`, `M` real symmetric (M6/M14: assembled from a real
quadratic energy and kinetic energy); (H2) tying `d = T(k) d̄` with `T` built from the unimodular
Bloch phases `μ_α = e^{i k·a_α}` (real `k`) on **every** tied DOF — value, first and mixed
derivative — exactly M9 (41)–(43), (D2). The M9 counterexample is reproduced from scratch and
independently recomputed in floating point; a second counterexample is built from an actual `C¹`
Hermite element derived from its shape functions.

---

## 1. Independent re-derivation of the matrix identities (script §A)

Let `K̄(k) = T(k)^H K T(k)`, `M̄(k) = T(k)^H M T(k)`. Pattern used: 6 DOFs, three master classes
and three slaves carrying the three phase types of M9 (D3) (`μ₁`, `μ₂`, `μ₁μ₂`), 21 free real
entries in `K`.

| # | Identity | Uses | Status |
|---|---|---|---|
| (I1) | `T(−k) = conj T(k)`, `T^H T = 2I` (isometry up to pair multiplicity) | unimodular phases | always [A1] |
| (I2) | `K̄(k)^H = K̄(k)` | (H1) only | always [A2] |
| (I3) | `K̄(−k) = conj K̄(k)` | (H1) + (I1) | always [A3] |
| (I4) | `K̄(−k)^H = K̄(k)^T`, hence `K̄(k) − K̄(−k)^H = K̄(k) − K̄(k)^T = 2i·Im K̄(k)` | (I2)+(I3) | always [A4] |
| (I5) | `Im K̄(k) ≠ 0` generically: e.g. `Im K̄₀₁ = K₀₄ sin θ₂ − K₁₃ sin θ₁ − K₃₄ sin(θ₁−θ₂)` | — | non-zero [A5] |
| (I6) | same three statements for `M̄` | (H1) | always [A7] |
| (I7) | `det(K̄(−k) − λM̄(−k)) = det(K̄(k) − λM̄(k))` for real `λ` ⇒ `ω_n(k) = ω_n(−k)` | (I2)+(I3) | always [A8] |

**Ruling on the status of (68).** By (I4) the literal statement `K̄(k) = K̄(−k)^H` is *exactly
equivalent* to `K̄(k) = K̄(k)^T`, i.e. (with Hermiticity) to **`K̄(k)` real**. Realness is not a
consequence of (H1)–(H2): by (I5) it requires additional relations between *distinct* entries of
`K` (coupling master-0↔slave-1 equal to coupling slave-0↔master-1, etc. — [A6]), which `K = K^T`
never supplies. **Eq. (68) is therefore incorrectly stated as a general property; it is
conditionally correct only under an additional realness hypothesis that the formulation does not
provide.** The physically required statements — real spectrum and `ω(k) = ω(−k)` — follow from
(I2)+(I3) alone (I7); (68) is not needed for them.

---

## 2. Counterexample — independently reproduced (script §B, §C)

**2.1 M9 minimal model, exact (SymPy).** `K = [[a,b,d],[b,c,f],[d,f,e]]`, node 2 = `μ`·node 0:
`K̄ = [[a+e+2d cos θ, b+f e^{−iθ}],[b+f e^{iθ}, c]]`; `K̄(k) − K̄(−k)^H = [[0, −2if sin θ],[2if sin θ, 0]]`.
At `a=b=c=e=f=1, d=0, θ=π/2`: `K̄ = [[2, 1−i],[1+i, 1]]`,
**`‖K̄‖_F² = 9`, `‖K̄ − K̄(−k)^H‖_F² = 8`, relative violation `2√2/3`** — reproduced exactly [B1]–[B3].

**2.2 Independent float recomputation (NumPy, matrices typed by hand).** literal-(68) residual
`0.942809041582` (`= 2√2/3` to 1e−12); Hermiticity residual `0.0`; conjugation residual `0.0` [B4].

**2.3 Formulation-derived counterexample (new).** 1D `C¹` cubic-Hermite element with DOFs
`{u, u′}` per node, element matrices *derived* from the shape functions for the 1D reduction of the
locked energy (`½E u′² + ½E g₂ u″²`, consistent mass), two elements, node 2 = `μ`·node 0 on value
**and** derivative (M9 (43)). Result: `K̄`, `M̄` Hermitian and conjugation-symmetric [C2], but
`Im K̄_(u₀,u₁) ≠ 0`, `Im K̄_(u₀′,u₁) ≠ 0` for generic `k` [C3]; with unit illustrative moduli
(`g₂ = h²/10`, *not* a production value) the literal-(68) residual at `kh = π/4` is **O(1)** and
vanishes only at Γ [C4]. So the literal test **fails for a correctly assembled, correctly tied
`C¹` gradient-elastic cell**; the counterexample is not an artefact of an abstract matrix.

---

## 3. Route diagnosis refined (script §D)

On the same Hermite element, the envelope (k-shift) route yields two different matrices:

- **sesquilinear** (test function conjugated — the variationally correct Galerkin form):
  Hermitian, `K_e(−k) = conj K_e(k)`, `K_e(−k)^H = K_e^T ≠ K_e` — the same structure as the tying
  route; **literal (68) fails** [D1];
- **bilinear** (no conjugation): complex symmetric, satisfies **literal (68) identically**, but is
  **not Hermitian** [D2].

Hence (68) is the identity of a complex-symmetric family with `K(−k) = conj K(k)`, and it is
incompatible with the "Reduced Hermitian eigenproblem" of §4.5 asserted of the same matrix. The
pair (I2)+(I3) is **route-independent**; (68) is not [D3]. This confirms and sharpens M9 [X3].

---

## 4. Wrong-sign derivative-DOF phase (script §E)

Variants: (W) value DOF with `μ`, derivative DOF with `μ⁻¹`; (Mis) derivative DOF with phase 1.

| Property | correct | (W) | (Mis) | check |
|---|---|---|---|---|
| `K̄^H = K̄`, `M̄^H = M̄` | ✓ | ✓ | ✓ | [E1],[E4] |
| `K̄(−k) = conj K̄(k)` | ✓ | ✓ | ✓ | [E1],[E4] |
| pencil charpoly even in `k` (`ω(k)=ω(−k)`) | ✓ | ✓ | ✓ | [E2],[E4] |
| BZ periodicity in `k` (test 5b) | ✓ | ✓ | — | [E2] |
| equals correct `K̄` at Γ (`μ=1`) | — | ✓ | ✓ | [E3] |
| equals correct `K̄` at X (`μ=−1`) | — | ✓ | ✗ | [E3],[E4] |
| equals correct `K̄` at interior `k` | — | ✗ | ✗ | [E3],[E4] |
| literal-(68) residual | O(1) | O(1) | — | [C4],[E5] |

**Why Hermiticity / k-evenness cannot detect it.** Any *diagonal unimodular* tying, whatever phase
sits on whichever DOF, satisfies (I1) and therefore (I2)–(I3) and (I7). The invariants test the
*algebraic form* of `T`, not the *assignment* of phases to DOFs. Moreover the wrong tying coincides
with the correct one wherever `μ² = 1` (Γ and X), so any check restricted to those points is blind.
The literal (68) residual is O(1) for both the correct and the wrong matrix [E5]: it has no
discriminating power in either direction.

---

## 5. Publication-grade verification structure (script §F)

| Test | Statement | Detects | Power on phase-sign error |
|---|---|---|---|
| **T1** Hermiticity | `‖K̄−K̄^H‖/‖K̄‖ < 1e−12`, same for `M̄` | non-symmetric `K`, wrong `T^H` (e.g. `T^T`), non-unimodular phase | **none** (necessary only) [F1] |
| **T2** conjugation | `‖K̄(−k) − conj K̄(k)‖/‖K̄‖ < 1e−12` (⇔ `K̄(−k) = K̄(k)^T`) | inconsistent `k → −k` handling, complex `K` | **none** (necessary only) [F1] |
| **T3** Bloch-wave consistency (new, internal) | for the nodal interpolant `d_full` of the exact plane wave `e^{ik·x}` (DOFs `e^{ikx_n}`, `ik e^{ikx_n}`, …): `‖T(k) d_master − d_full‖ = 0` at **interior** `k`; energy form: reduced Rayleigh quotient of `d_master` = full-cell quotient of `d_full` | wrong sign / missing phase on any derivative DOF; residual on the slave derivative DOF is exactly `ik(μ⁻¹−μ)` (W) or `ik(1−μ)` (Mis) | **full**, no reference solution needed [F2],[F3] |
| **T4** independent reference at **interior** `k` | Layer-3 closed-form dispersion (P2.1/P2.2) and Phase-3 anchors | any formulation/assembly error | **full** at `kh ≳ 0.3` (errors 8e−2 / 1e−2 vs 1e−7 correct) [F4b] |

**New finding beyond M9 [X4].** The long-wave slope test 5d (`ω → c|k|`, `k → 0`) is **blind** to
the derivative-DOF phase error: at `kh = 10⁻³` the relative error is `2e−8` (correct), `9e−7`
(wrong sign), `1.5e−7` (missing) — all within a `1e−6` slope tolerance, because the wrong tying
coincides with the right one at Γ and the discrepancy is O(k²) relative [F4a]. The independent
reference of T4 must therefore be evaluated at interior `k`, not as the `k → 0` slope only.

**Conclusion on the Sec 4 pitfalls row.** Its stated *cause* ("Non-Hermitian `K̄`" from a wrong
derivative-DOF phase sign) is not the mechanism, and its *test* fails for every correct
implementation. The row must be re-based on T1 + T2 (necessary invariants) **plus** T3 (the
internal sign-sensitive test) with T4 as the external confirmation. This is not a weakening: the
original test passes nothing correct and catches nothing wrong.

---

## 6. Ruling among (a), (b), (c)

- **(b) — REJECTED.** Keeping (68) literally would require "proving" realness of `K̄`, which is
  false for the `C¹` cell (§2.3) and would make mandatory test 5a fail on every correct run at every
  `k ∉ {Γ}`; it would also contradict "Hermitian eigenproblem" in the same row (§3).
- **(c) — REJECTED.** Deferring is not justified: the mathematics is fully determined now
  (I1)–(I7), the counterexample is formulation-derived, and M15's own acceptance criterion
  ("reduced `K`, `M` Hermitian by construction", `CALC_MASTER_PLAN` §F14 test) depends on the
  corrected statement; deferring would let M15 be built against a criterion known to be false.
- **(a) — ADOPTED.** Restate (68) as the pair (I2)+(I3), re-base test 5a on T1 + T2, and add T3 as
  the sign-sensitive internal test (with T4 at interior `k` as the reference layer, already in the
  approved plan). This preserves all physical content the blueprint intends (real spectrum,
  `ω(k)=ω(−k)`, detection of derivative-DOF phase errors) with statements that are actually
  provable in M15.

---

## 7. Blueprint impact — amendment REQUIRED, NOT applied (awaiting authorization)

Exact proposed wording (Blueprint v1.3 → v1.4; scientific, not editorial; four locations):

| Line | Current text | Proposed text | Reason |
|---|---|---|---|
| 403 (§4.5 row) | "prove $\bar{\bm K}(\bm k)=\bar{\bm K}(-\bm k)^{\mathsf H}$" | "prove $\bar{\bm K}(\bm k)^{\mathsf H}=\bar{\bm K}(\bm k)$ and $\bar{\bm K}(-\bm k)=\overline{\bar{\bm K}(\bm k)}$ (hence $\bar\omega_n(\bm k)=\bar\omega_n(-\bm k)$); same for $\bar{\bm M}$" | (I4): literal form ⇔ realness, false for the `C¹` cell |
| 587 (register (66)–(68)) | "$\bar{\bm K}(\bm k)=\bar{\bm K}(-\bm k)^{\mathsf H}$" | "$\bar{\bm K}^{\mathsf H}=\bar{\bm K}$; $\bar{\bm K}(-\bm k)=\overline{\bar{\bm K}(\bm k)}$" | same |
| 416 (pitfalls row) | "Non-Hermitian $\bar{\bm K}$ \| Wrong sign of the phase on the derivative DOFs. Test $\|\bar{\bm K}(\bm k)-\bar{\bm K}(-\bm k)^{\mathsf H}\|/\|\bar{\bm K}\|<10^{-12}$ on every run." | "Wrong phase on derivative DOFs \| A unimodular phase error on $u_{,x},u_{,y},u_{,xy}$ leaves $\bar{\bm K}$ Hermitian and $\bar\omega$ even in $\bm k$, so invariance tests cannot see it. Test on every run: (i) $\|\bar{\bm K}-\bar{\bm K}^{\mathsf H}\|/\|\bar{\bm K}\|<10^{-12}$ and $\|\bar{\bm K}(-\bm k)-\overline{\bar{\bm K}(\bm k)}\|/\|\bar{\bm K}\|<10^{-12}$; (ii) Bloch-wave consistency $\|\bm T(\bm k)\bm d_{\rm master}-\bm d_{\rm full}\|=0$ for the nodal interpolant of $e^{\mathrm i\bm k\cdot\bm x}$ at interior $\bm k$; (iii) Layer-3 analytic dispersion at interior $\bm k$." | §4–§5: mechanism and detectability |
| validation matrix row 5a | "Hermiticity $\|\bar{\bm K}(\bm k)-\bar{\bm K}(-\bm k)^{\mathsf H}\|/\|\bar{\bm K}\|<10^{-12}$" | "Hermiticity + conjugation: $\|\bar{\bm K}-\bar{\bm K}^{\mathsf H}\|/\|\bar{\bm K}\|<10^{-12}$, $\|\bar{\bm K}(-\bm k)-\overline{\bar{\bm K}(\bm k)}\|/\|\bar{\bm K}\|<10^{-12}$ (and for $\bar{\bm M}$); Bloch-wave consistency residual $=0$ at interior $\bm k$" | test 5a must be passable by a correct code |

Consequential (non-blueprint) edits, also pending the same authorization: `CALC_MASTER_PLAN.md`
§A row M15 ("proof `K̄(k)=K̄(−k)^H`") and §F14; `PHASE1_FORMULATION_PLAN.md` row M15. Test count
(eight, 5a–5h) is unchanged: 5a is re-based, not removed; T3 lives inside 5a. Layer-3 (T4) is
already in the plan; only the requirement "at interior `k`, not the `k→0` slope alone" is new.

**Which later work depends on it:** M15 (proof obligation (66)–(68); §F14 criterion); Phase-4A
test 5a; the Week-6 gate G2 ("all 8 automated internal tests pass") — with the literal 5a, G2 could
never be passed by a correct implementation.

---

## 8. Checks performed (30, all PASSED)

| # | Content | Result |
|---|---|---|
| A1–A8 | general identities (I1)–(I7) on a 6-DOF three-phase pattern; realness condition explicit; spectral evenness | PASSED |
| B1–B4 | M9 counterexample re-derived exactly; `9`, `8`, `2√2/3`; independent NumPy recomputation `0.942809041582` | PASSED |
| C1–C4 | `C¹` Hermite element derived; correct tying Hermitian + conjugation; `K̄` not real; O(1) literal residual, zero only at Γ | PASSED |
| D1–D3 | sesquilinear vs bilinear envelope matrices; (68) holds only for the non-Hermitian bilinear form; pair is route-independent | PASSED |
| E1–E5 | wrong-sign and missing-phase tyings: preserve Hermiticity, conjugation, k-evenness, BZ periodicity; coincide with correct at Γ (and X for wrong sign); literal test O(1) for both | PASSED |
| F1–F5 | T1/T2 zero for right and wrong; T3 detects (exact residuals `ik(μ⁻¹−μ)`, `ik(1−μ)`); 5d slope blind; finite-k reference detects; structure ruling | PASSED |

Failures encountered and fixed during the audit (traceability): (1) `sp.im` on `e^{iθ}`
expressions needs a trigonometric rewrite before simplification (helper `imag`, robust `iszero`);
(2) the 4×4 symbolic pencil determinant with five symbolic parameters did not terminate — replaced
by exact rationals for the moduli with `k` kept symbolic (Berkowitz), which is what the statement
needs; (3) the first draft of T4 used the `k → 0` slope and **failed** — the failure is itself the
finding [F4a] and the check was split into [F4a] (blind) and [F4b] (interior `k`, detecting).

## 9. Traceability

| Object | Source | Record | Checks | Status |
|---|---|---|---|---|
| M15-a ruling | blueprint 403/416/587/5a; M9 §M9.8 | this record | A1–F5 | RESOLVED — (a); amendment proposed, NOT applied |
| identities (I2),(I3) | (H1),(H2) | §1 | A2,A3,A7,C2,D1 | proven, route-independent |
| literal (68) ⇔ realness | (I4) | §1 | A4,A5,A6,B2,C3 | refuted as a general claim |
| counterexample `9/8/2√2/3` | M9 [X1] | §2 | B3,B4 | independently reproduced |
| wrong-sign detectability | M9 [X4] | §4–§5 | E1–E5,F1–F4b | confirmed; T3 supplies an internal detector; 5d blind (new) |
| blueprint amendment | §7 | this record | — | AWAITING AUTHORIZATION |
