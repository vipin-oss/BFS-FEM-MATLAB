"""P12H — C-1 synthetic discrimination suite (authorized P1–P4 predicates) and the P12G
Rule R-fit adversarial classification set, kept as permanent tests.

No solver runs; no scientific value is produced.  The criterion constants (P_MIN, R_MAX,
FLOOR_MAX) and the rule constants (F, SPREAD_FLOOR, seeds, tol, meshes) are pinned by
test_p12h_rule_rfit_governance.py; this file verifies the *behaviour* they must produce.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

SUITE = Path(__file__).resolve().parent
sys.path.insert(0, str(SUITE))
import rule_rfit as R  # noqa: E402

HS3 = [1 / 4, 1 / 8, 1 / 16]
HS4 = HS3 + [1 / 32]


def _evaluate(errs, d16):
    fit = R.lsq_loglog(HS3, errs[:3]) if len(errs) == 3 else R.lsq_loglog(HS4, errs)
    crit = R.check_criterion(errs, d16, fit["lo"], fit["resid_max"])
    return fit, crit


CONVERGENT_4 = [1e-8, 6.25e-10, 3.91e-11, 2.44e-12]
CONVERGENT_2 = [1e-8, 2.5e-9, 6.25e-10, 1.56e-10]
FLAT = [1e-3, 1e-3, 1e-3, 1e-3]
OSCILLATORY = [1e-8, 9e-8, 1e-9, 5e-9]
RANDOM = [9.1e-4, 1.02e-3, 9.8e-4, 1.05e-3]
ANTI = [1e-8, 2e-8, 4e-8, 8e-8]


@pytest.mark.parametrize("name,errs,d16,expect", [
    ("convergent 4th order", CONVERGENT_4, 2.4e-12, "PASS"),
    ("convergent 2nd order", CONVERGENT_2, 1.5e-10, "PASS"),
    ("flat plateau", FLAT, 1e-13, "FAIL"),
    ("oscillatory", OSCILLATORY, 4e-9, "FAIL"),
    ("random noise", RANDOM, 7e-5, "FAIL"),
    ("anti-convergent", ANTI, 4e-8, "FAIL"),
])
def test_required_discrimination(name, errs, d16, expect):
    _, crit = _evaluate(errs, d16)
    assert ("PASS" if all(crit.values()) else "FAIL") == expect, f"{name}: {crit}"


@pytest.mark.parametrize("key,errs,d16", [
    ("P1_monotone_decreasing", [1e-8, 6.25e-10, 6.30e-10, 2.44e-12], 2.4e-12),
    ("P2_ci_lower_ge_P_MIN", [1e-3, 9.5e-4, 9.2e-4, 9.0e-4], 1e-10),
    ("P3_powerlaw_residual_le_R_MAX", [1e-8, 6.25e-10, 1.95e-11, 2.44e-12], 2.4e-12),
    ("P4_floor_datum_le_FLOOR_MAX", [1e-6, 6e-8, 4e-9, 3e-10], 1e-8),
])
def test_each_predicate_can_fail(key, errs, d16):
    _, crit = _evaluate(errs, d16)
    assert crit[key] is False, f"{key} did not fire on its falsifying case"


@pytest.mark.parametrize("errs,d16", [
    (CONVERGENT_4, 2.4e-12),                    # all four predicates
    ([1e-4, 4.8e-5, 2.3e-5, 1.1e-5], 1e-9),     # marginal p ~ 1.06 (P2 boundary)
    (CONVERGENT_4, 1e-9),                       # floor datum exactly at the P4 bound
])
def test_accepted_sequences_keep_all_predicates(errs, d16):
    _, crit = _evaluate(errs, d16)
    assert all(crit.values()), crit


# ---- Rule R-fit adversarial classification (P12G set; expected verdicts frozen) ----
@pytest.mark.parametrize("tag,errs3,e32,s32,expect", [
    ("B1 above trend, above floor", [1e-8, 6.25e-10, 3.91e-11], 1e-10, 1e-16, True),
    ("B2 below trend, above floor", [1e-8, 6.25e-10, 3.91e-11], 2.5e-12, 1e-16, True),
    ("B3 inclusion would improve the estimate", [1.405e-09, 5.324e-11, 2.995e-11], 2.44140625e-12, 5e-12, False),
    ("B4 same pair, inclusion would worsen", [8.841e-10, 2.762e-10, 8.348e-11], 2.44140625e-12, 5e-12, False),
    ("B5 above floor, worsens the estimate", [1e-8, 6.25e-10, 3.91e-11], 1e-10, 1e-12, True),
    ("B6 noisy (e = s)", [1e-8, 6.25e-10, 3.91e-11], 1e-11, 1e-11, False),
    ("B7 converged at the noise level (e = s)", [1e-8, 6.25e-10, 3.91e-11], 3e-13, 3e-13, False),
    ("B8 exactly at the threshold (e = F*s)", [1e-8, 6.25e-10, 3.91e-11], 3e-12, 1e-12, False),
])
def test_rfit_adversarial_classification(tag, errs3, e32, s32, expect):
    adm, exc = R.admissible_subset(errs3 + [e32], [1e-16] * 3 + [s32])
    assert (32 in adm) is expect, f"{tag}: decision {adm}/{exc}"
    # the decision must be independent of whether inclusion helps the fit
    f3, f4 = R.lsq_loglog(HS3, errs3), R.lsq_loglog(HS4, errs3 + [e32])
    helper = dict(tag=tag, slope3=f3["slope"], slope4=f4["slope"], resid3=f3["resid_max"], resid4=f4["resid_max"])
    assert helper  # recorded for the audit; no assertion on the estimate itself by design


def test_P1_uses_a_strict_comparison():
    """P1 must be a STRICT monotone decrease: an exactly repeated error is not convergence.

    The composite verdict is not the discriminator here (a duplicate point also distorts the
    fit), so the predicate is pinned directly -- this is what closes mutation R13.
    """
    plateau = [1e-8, 6.25e-10, 6.25e-10, 2.44e-12]
    assert R.check_criterion(plateau, 2.44e-12, 3.0, 0.1)["P1_monotone_decreasing"] is False
    decreasing = [1e-8, 6.25e-10, 6.249e-10, 2.44e-12]
    assert R.check_criterion(decreasing, 2.44e-12, 3.0, 0.1)["P1_monotone_decreasing"] is True
    # a single equality anywhere in the sequence is enough to fail P1
    mid = [1e-8, 6.25e-10, 6.25e-10, 1.0e-10]
    assert R.check_criterion(mid, 1.0e-10, 3.0, 0.1)["P1_monotone_decreasing"] is False


def test_rfit_decision_invariant_to_surrounding_trend():
    e32, s32 = 5.0e-13, 1.0e-12
    steep = [1e-8, 6.25e-10, 3.91e-11]
    shallow = [1e-6, 4.0e-7, 1.6e-7]
    a, _ = R.admissible_subset(steep + [e32], [1e-16] * 3 + [s32])
    b, _ = R.admissible_subset(shallow + [e32], [1e-16] * 3 + [s32])
    assert (32 in a) is (32 in b) is False, "the verdict must not depend on the surrounding data"
