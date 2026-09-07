# verification/

verify_invariants.py — 22-check science-preservation gate (PART-27 headline
values + branch identity); run anywhere: `python3 verification/verify_invariants.py`;
writes reports/INVARIANT_CHECK.md; nonzero exit on any failure.

Subdirectories map the validation evidence by type; the executable checks
live in tests/V*/ (single source) — commands below run them from the
package root:

- branch_identity/ : Ω*=1000 limit V_C(D_w*→0) = V_A (|ΔV| ~ 1e-10, NOT the
  0.467 phonon branch).  Run: `python3 verification/verify_invariants.py`
  (check "branch identity @Om=1000"); solver logic in solver/branch.py.
- symbolic/        : `python3 tests/V4/test_V4_symbolic.py` (symbolic checks
  of constitutive/pencil identities, e.g. H_xz != H_zx structure).
- model_limits/    : `python3 tests/V3/test_V3_model_limits.py` (Models
  B/C → classical/quasi-static limits; gates 1.11e-9 / 3.27e-9).
- two_path/        : `python3 tests/V1/test_V1_two_path.py` (two independent
  computation paths agree).
- reports/         : INVARIANT_CHECK.md (latest gate run snapshot).
