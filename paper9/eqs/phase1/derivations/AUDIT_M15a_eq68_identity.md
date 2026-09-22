# M15-a AUDIT AND RULING — Blueprint v1.3 Eq. (68) `K̄(k) = K̄(−k)^H`

Status: **RESOLVED — ruling: option (a)**, with the Sec 4 test re-based on the provable pair and
**supplemented** by an independent phase/sign validation. Recorded, not applied: no blueprint edit.
M1–M9 mathematics and evidence untouched.

Scope of this record (and only this): the **verification statement** attached to the reduced
eigenproblem. No equation of the locked formulation is changed, no computed quantity changes, no
new physics is introduced, M10–M17 are not started, and no numerical/benchmark/manuscript result is
produced. This record is `[S]` (structural/verification decision) with the mathematical content `[A]`
(derived here) and `[C]` citations to the blueprint only.

Reproduce:

```
cd paper9/eqs/phase1
python3 scripts/audit_m15a_eq68_identity.py     # M15-a audit  (37 checks)
```

Deterministic (two consecutive runs byte-identical), SymPy exact arithmetic plus an independent
exact-`Fraction` toolchain for the counterexample; writes no files.
Script sha256 (pre-run = post-run, recorded in `checks/audit_m15a_eq68_identity.log`):
`590268236408fead836d878bd58e3748a9238c61c66c905092f6d8e77fede8dc`.

---

## M15-a.0 What is being ruled on `[C]`

Blueprint v1.3, verbatim:

- §4.5 row (line 403): "**Reduced Hermitian eigenproblem** `[K̄(k) − ω̄²M̄(k)]d̄ = 0`; **prove
  `K̄(k) = K̄(−k)^H`**; solver choice and the number of lowest bands extracted." → (66)–(68).
- Register (line 587): "(66)–(68) Reduced Hermitian eigenproblem; `K̄(k) = K̄(−k)^H`".
- Pitfalls table (line 416): "**Non-Hermitian `K̄`** | Wrong sign of the phase on the derivative
  DOFs. Test `‖K̄(k) − K̄(−k)^H‖/‖K̄‖ < 10^{−12}` on every run."

Recorded in M9 §M9.8 as **M15-a**, status TO BE VERIFIED, with three options not chosen by M9:
(a) restate (68) as the pair `K̄^H = K̄`, `K̄(−k) = conj(K̄(k))` and re-base the Sec 4 test;
(b) keep (68) literally; (c) defer to M15 with the pair plus reference checks.

This audit is independent of M9: the identities are re-derived from the locked formulation, the
counterexample is recomputed in a different toolchain, and the M9 script is not re-used.

## M15-a.1 Independent re-derivation `[A]`

**The tying matrix T(k) (exact role).** Sec 4.4 prescribes `d_slave = T(k)d_master` with `T`
diagonal complex phase; the phases are the ones derived in M9 (41)–(43) — i.e. **the phase is a
property of the NODE**, the same factor `μ_α` on the value DOF and on every derivative DOF
(`u_{,x}`, `u_{,y}`, `u_{,xy}`) and on both displacement components. Verified entrywise on the
16×4 cell structure table ([R1]); the master block is the identity, so `T` has full column rank
and the reduction is a **restriction to the subspace `S = range(T)`**, not a similarity ([R2]).
All statements below are statements about `S`.

**Structure theorem (Hermiticity is free).** For `K = K^H` and **any** complex `T`,
`(T^H K T)^H = T^H K^H T = T^H K T` ([R3]). No property of `T` — not unitarity, not unimodularity,
not the phase sign — is needed. *Consequence:* the Hermiticity of `K̄` is automatic and therefore
**carries no information about the Bloch phase table**; it cannot be the test the pitfalls row
thinks it is.

**Identity 1 (always true).** `K̄^H = K̄` ([R6]) — on the 8×2 cell model and again on the 3-node
model ([R12]).

**Identity 2 (always true).** `T(−k) = conj(T(k))` for every unimodular phase table built from node
coordinates ([R4]); with `K` real symmetric ([R5], consistent with the M6/M7 assembly form
`K_g = (1/10)L_ij B^T_{,i}(D_c C̄)B_{,j}`), this gives `K̄(−k) = conj(K̄(k))` ([R7], [R12]).
The same statement holds for the wrong-sign table, so it too is not a correctness test by itself.

**Equivalence theorem.** From Identities 1–2: `K̄(−k)^H = conj(K̄(k))^H = K̄(k)^T`. Hence the literal
blueprint (68) is **exactly equivalent** to `K̄(k)^T = K̄(k)` ([R8]), i.e. to

> **(68) ⟺ `K̄(k)` is real (real symmetric)** — for every `k`.

**Characterisation of the exceptional set.** With a diagonal phase table,
`K̄_ij = Σ_{n,m} exp(i(φ_m − φ_n)) K_{(n,i),(m,j)}`, so (verified exactly, [R10])

```
Im(K̄_ij) = Σ_{n,m} sin(φ_m − φ_n) K_{(n,i),(m,j)}
          = γ_x sinθ_x + γ_y sinθ_y + γ_s sin(θ_x+θ_y) + γ_d sin(θ_y−θ_x)
```

with all four class coefficients `γ ≠ 0` for the model cell. Realness therefore forces
`sinθ_x = sinθ_y = 0`, i.e. `k_α·a_α ∈ πℤ`: a **finite 9-point subset** of the closed first BZ —
a measure-zero set. Verified explicitly ([R9]): the literal statement **passes at Γ, X, M** (all
phases there are ±1, so `K̄` is real) and **fails on the interior of every IBZ leg**
(Γ–X, Γ–M, X–M). A test that is correct only at the high-symmetry points is not a test.

**What the pair does give (everything the blueprint needs).** Real eigenvalues (equivalently: real
characteristic-polynomial coefficients) and `k`-evenness of the characteristic polynomial, i.e.
`ω_n(k) = ω_n(−k)` and odd group velocity — verified exactly ([R11]). None of this uses (68).

## M15-a.2 Independent counterexample verification `[A]`

Reconstructed from a **model**, not copied: 1D cell, nodes at `x = 0, L/2, L`, one periodic pair,
phase `μ = e^{iθ}`, real symmetric `K`. Direct multiplication gives the exact identity ([E1])

```
K̄ = [[a + c + 2d cosθ,  b + f e^{−iθ}],
     [b + f e^{iθ},      e            ]]
```

At the M9 test point (`a = b = c = e = f = 1`, `d = 0`, `θ = π/2`) this is `[[2, 1−i], [1+i, 1]]`
exactly ([E2]). Independent recomputation in exact `Fraction` arithmetic, **no SymPy/NumPy**, each
norm by three routes (component-wise, `tr(A^H A)`, `tr(A²)`):

| quantity | value | routes |
|---|---|---|
| `‖K̄‖_F²` | **9** | 9, 9, 9 ✔ CONFIRMED |
| `‖K̄ − K̄(−k)^H‖_F²` | **8** | 8, 8, 8 ✔ CONFIRMED |
| relative violation `√(8/9)` | **2√2/3 = 0.9428090415820634…** | exact `8/9`; 40-digit decimal agrees to 25 digits ✔ CONFIRMED |

Difference matrix `D = [[0, −2i], [2i, 0]]`, i.e. `2i·Im(K̄_12)` ([E4]); realness ⟺ `f sinθ = 0`
([E7]); rounding of the recorded value is sound — `0.9425 ≤ 2√2/3 < 0.9435`, so 0.943 ([E9]).
The violation exceeds the required `1e−12` by a factor ≈ `9.4·10^11`; it is O(1), not a tolerance
effect. **Verdict: the M9 counterexample is CONFIRMED, not rejected.**

**Erratum in the M9 record (recorded; the M9 record is not edited).** `DERIVATION_M09.md` §M9.8
item 1 prints the closed form `2i Im(K̄_12)[[0,−1],[1,0]] = −2i f sinθ[[0,−1],[1,0]]`, which carries
the **opposite overall sign** to the identity the M9 script itself verified. Correctly ([E6]):

```
K̄ − K̄(−k)^H = 2i Im(K̄_12) [[0, 1], [−1, 0]] = −2i f sinθ [[0, 1], [−1, 0]]
             = [[0, −2i f sinθ], [2i f sinθ, 0]]
```

No conclusion of M9 depends on the slip (equivalence to realness, the O(1) violation, and the
numbers 9, 8, 2√2/3 are identical). `DERIVATION_M09.md`, its log and its script are left exactly as
committed.

## M15-a.3 The wrong-sign derivative-DOF phase control `[A]`

Convention: value DOF tied with `μ`, derivative DOF tied with `μ^{-1}`.

**Field level.** For an exact Bloch field `u = e^{ikx}f(x)` (`f` periodic) both relations hold with
the same phase ([W1]): `u(x+L) = μu(x)` **and** `u_{,x}(x+L) = μu_{,x}(x)`. The wrong-sign control
asserts `u_{,x}(x+L) = μ^{-1}u_{,x}(x)`, with exact residual `(μ − μ^{-1})u_{,x} = +2i sin(kL)u_{,x}`
([W2]); the two conventions can coexist for one field only if `μ² = 1`, i.e. `sin(kL) = 0` ([W3]).

**Subspace level.** The wrong-sign column `(0,1,0,μ^{-1})` is **not** in the column space of the
correct tying matrix unless `μ² = 1`; the orthogonal residual has squared norm `2 sin²θ` ([W4]) —
i.e. the two discretisations restrict to **different** subspaces. The error is therefore *not* a
gauge or a reparametrisation.

**What it preserves.** (i) `T_w` is a legitimate complex matrix of full rank, so its reduced matrix
is **still exactly Hermitian** ([W5], from [R3]) — the Hermiticity guard cannot fire; (ii) its entries
are unimodular phases, so `K̄_w(−k) = conj(K̄_w(k))` **still holds** and its characteristic polynomial
is still `k`-even ([W6]). Both invariance tests listed in the blueprint **pass** for the wrong-sign
control. (iii) A third, grossly wrong table (phase omitted entirely, `T` constant real) also passes
both invariants while producing yet another spectrum ([W8]): the listed invariants are
**structure-blind in general**, not only for this particular bug.

**What it violates.** The discrete problem itself. The two reduced matrices share the trace but not
the determinant ([W7]):

```
det K̄_correct − det K̄_wrong = 4 sin²θ (s v − q²)   (≠ 0 generically; = 2 at θ = π/6,
                                                      (p,q,r,s,u,v) = (2,1,1,2,2,3/2))
```

so at a fixed generic `k` the spectra differ, and so does the reconstructed mode shape.

**Detectability.** Not detectable by Hermiticity or by `k`-evenness ([W5], [W6]); **detectable** by
any of ([W9], [W10]): (1) the structural phase rule — the tying entries at a node must carry the
same phase for all four DOF types, so the ratio `(u: phase)/(u_x: phase)` must be exactly 1
(wrong-sign gives `μ^{-2} ≠ 1`); (2) column membership of the tying built from node coordinates and
the derived phase rule (equivalently the field-level derivative relation), residual `‖r‖² = 2 sin²θ`;
(3) comparison against an independent reference at a **generic interior** `k` (the two spectra
differ there; they coincide only at the `sin(kL) = 0` points).

## M15-a.4 Classification of Eq. (68) `[A]`

(68) is **not a correct identity of the operational formulation** (it fails at a measure-zero set of
`k` only, and only by accident there). It is an **incorrectly stated stronger condition**, exactly
equivalent to the extra hypothesis "`K̄` is real", which the model does **not** provide: realness
requires `k·dx_ij ∈ πℤ` for every coupled pair — accidental degeneracies that real symmetry
(`K_ij = K_ji`) does not supply. The intended physical content of the sentence "prove
`K̄(k) = K̄(−k)^H`" in a Hermitian-eigenproblem context is the **pair** of Identities 1–2, both of
which are unconditional.

## M15-a.5 Audit of the three recorded options → ruling `[A]`, `[S]`

- **(b) keep (68) literally — REFUTED mathematically.** A correct implementation (i) *fails* the
  mandatory every-run test on the interior of every IBZ leg, and (ii) *passes* it if only Γ, X, M
  are sampled, while the claim remains false there in the sense that realness is accidental. Both
  outcomes are unacceptable for a publication-grade verification statement; no implementation
  convention can rescue the literal form ([V1]).
- **(a) replace (68) conceptually by the pair — JUSTIFIED.** Both members are exact identities for
  any tying built from the derived phase rules ([R4], [R6], [R7], [R12]); they hold on the whole
  BZ; they are jointly sufficient for every physical statement needed — real eigenvalues,
  `ω_n(k) = ω_n(−k)`, odd group velocity ([R11]). Nothing is lost physically, nothing is gained
  physically, and the statement becomes provable ([V2]).
- **(c) defer to M15 — SUBSUMED.** Its valuable part (comparison with independent references) is the
  detection channel retained inside (a) ([W10]); only the numeric tolerances belong to M15/Phase 2
  (P2.1/P2.2 and the Phase-3 anchors). Deferring the *formulation* ruling would leave the every-run
  test wrong in the milestone that implements it ([V3]).

**RULING: option (a).** Reason: it is the only one of the three that is simultaneously (i) provable
from the locked formulation, (ii) sufficient for the physics the blueprint needs, and (iii)
consistent with the Sec 4.4 route the blueprint prescribes. This choice is made on mathematical
grounds, not on convenience: (b) is rejected although it needs no change at all, and (a) is adopted
although it obliges a further verification test ([V4]).

## M15-a.6 Four notions that must not be conflated (requirement 7) `[A]`

1. **Hermiticity** `K̄^H = K̄` — exact identity, but automatic for any `T` ([R3]). Scope: a
   code/assembly guard (it catches a non-real `K`, a genuinely asymmetric assembly, a complex
   arithmetic slip), **not** a Bloch-phase check.
2. **Time-reversal / conjugation** `K̄(−k) = conj(K̄(k))` — exact identity given real `K` and a
   unimodular table with `T(−k) = conj(T(k))` ([R4], [R7]). Physical content: `k`-even spectrum,
   odd group velocity. Also blind to phase-sign errors.
3. **Real / complex symmetry** — "`K̄` real" is an extra hypothesis, equivalent to the literal (68)
   ([R8]) and false almost everywhere ([R10]). The complex-symmetric **envelope (k-shift) route**
   satisfies (68) identically while being **non-Hermitian** (M9 [X3], unchanged): the two
   statements cannot both be asserted of one matrix, and the blueprint prescribes the tying route.
4. **Independent phase/sign validation** — the structural rule test and the subspace/reference
   tests ([W9], [W10]). This is the only channel that can detect a wrong-sign (or wrong-offset)
   phase, and it must be preserved.

**Changing a verification test is not changing the physical model.** Adopting (a) alters no
equation, no matrix, no number, and no assumption of the locked formulation: it replaces a claim
that is not provable (and that fails for correct code) by the two claims that are provable, and it
adds tests that detect the error the pitfalls row intends to catch. The model, the assembly, the
eigenproblem and every Phase-1 result stay exactly as verified.

## M15-a.7 Blueprint impact — amendment REQUIRED, recorded, NOT applied `[S]`

A blueprint change **is** required (the literal wording cannot be proved), but the blueprint is
**not edited here** — no edit in this milestone, and no silent replacement of any equation or test.
Proposed amendment (verbatim as recorded in the check log):

- **§4.5 row, clause "prove `K̄(k) = K̄(−k)^H`"** →
  "prove `K̄(k)^H = K̄(k)` and `K̄(−k) = conj(K̄(k))`; the spectrum is then real and `k`-symmetric,
  `ω_n(k) = ω_n(−k)`. (`K̄(k) = K̄(−k)^H` holds only when the phases of the coupled DOF pairs are
  real, i.e. on the measure-zero set `k·dx ∈ πℤ` — not on the interior of the IBZ legs — and is
  therefore not the operative identity.)"
- **§4 pitfalls row, replace the single test by a test set:**
  "(i) keep `‖K̄^H − K̄‖/‖K̄‖ < 1e−12` and add (ii) `‖K̄(−k) − conj(K̄(k))‖/‖K̄‖ < 1e−12`;
  (iii) the phase table must give the **same** phase factor for all DOF types of a node — assert the
  ratio `== 1` exactly; (iv) assert column membership of the tying matrix built from node
  coordinates and the derived phase rule (equivalently the field-level derivative relation);
  (v) compare against an independent reference at a generic interior `k` (P2.1/P2.2, Phase 3).
  The wrong-sign derivative phase passes (i)–(ii) and is caught by (iii)–(v)."

**Why necessary:** under the literal text the mandatory run test fails for a correct implementation
and passes for a wrong-sign phase error — i.e. it is both false-alarming and non-diagnostic for the
pitfall it is attached to.

## M15-a.8 Decision on the 1e−12 Sec-4 test `[S]`

**SUPPLEMENTED (re-based + extended), not retained unchanged, not replaced by a weaker test, not
deferred.** The Hermiticity guard is kept because it does catch genuine assembly asymmetries; its
scope is stated honestly (it cannot see phase errors). It is re-based on the provable identities
(items (i)–(ii) above) and supplemented by (iii)–(v), which **preserve an independent test capable of
detecting wrong-sign Bloch derivative phases** ([W9], [W10]). Deferral would leave the milestone that
implements the eigenproblem without a working diagnostic.

## M15-a.9 Consequences for M13/M15 and for published validation `[S]` (forward, not started)

- **M13 (element/reduced assembly):** the tying must be built from node coordinates with the derived
  phase rule (same phase for all DOF types of a node); tests (iii)–(iv) can be asserted at assembly
  time at negligible cost. Nothing else changes; no new workstream is created.
- **M15 (reduced eigenproblem, band structure, mode tracking):** prove the **pair**, not (68);
  implement the supplemented test set; the eigenproblem, Jacobi scaling, condition number and MAC
  continuation are unaffected in their formulation. Reported dispersion symmetry must be stated as
  `ω_n(k) = ω_n(−k)` (from the pair), never as consequence of (68).
- **Published validation (Phase 2/3 anchors A–D):** reference comparisons at **generic interior `k`**
  are a genuine validation of the phase convention, since a wrong-sign phase changes the spectrum
  there ([W7]); at `sin(kL) = 0` points it does not — so anchor comparisons must include interior
  `k` samples. The manuscript may retain the "Hermitian eigenproblem" language (true) and must not
  claim (68) as an identity.

## M15-a.10 Checks performed (37, all PASSED) and non-scope

Checks: `[R0]`–`[R12]` (re-derivation, structure theorem, equivalence, characterisation, physical
content), `[R12]`–`[E9]` in section E (independent counterexample: 9, 8, 2√2/3, erratum,
second model), `[W1]`–`[W10]` (wrong-sign control: preserved/violated properties, detectability),
`[V1]`–`[V5]` (options audit, ruling, distinctions). Full output in
`checks/audit_m15a_eq68_identity.log` (37 PASS / 0 FAIL; script sha256 recorded pre-run = post-run).

**Not done (deliberate):** no blueprint edit; no change to (66)–(68) or to any M1–M9 file
(`DERIVATION_M09.md`, `m09_bloch_c1.py` and their recorded sha256 values are unchanged); no test
deleted (the guard is re-based and extended); no M10–M17 work; no numerical parameter value, no
solver code, no benchmark comparison, no manuscript result, no scientific PASS claim.

## M15-a.11 Erratum register (audit trail) `[S]`

| # | Item | Consequence |
|---|---|---|
| M15-a-E1 | `DERIVATION_M09.md` §M9.8 item 1 prints the closed form with the opposite overall sign (corrected form in M15-a.2) | Documentation only; no conclusion, number or verified identity of M9 is affected; M9 files left untouched per the preservation rule |
