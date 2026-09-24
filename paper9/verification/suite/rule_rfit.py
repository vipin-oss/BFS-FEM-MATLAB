"""Rule R-fit — governing admissibility rule for the 5i observed convergence rate (P12H / A1).

Frozen in P12G (paper9/audit/P12G_ROUTE_A_RULE_RFIT_FREEZE.md) and adopted here by the
authorized A1 decision (P12H).  It is a *verification-side* implementation: it re-derives
the admissibility decision and the resulting least-squares rate from recorded evidence.
It runs no solver and writes no scientific result.

Rule (verbatim from the freeze):
  A refinement level i participates in the least-squares rate fit  <=>
        e_i > F * max(s_i, SPREAD_FLOOR)
  with e_i = the level's relative error against the closed-form reference and s_i = the
  level's measured reproducibility (relative spread of its eigenvalue between the two
  pre-registered start vectors at the frozen solver configuration).  The inequality is
  strict; the rate is reported only if >= MIN_ADMISSIBLE levels are admissible.

Nothing in this module may be changed without a new authorization: the constants below are
pinned by paper9/verification/suite/test_p12h_rule_rfit_governance.py.
"""
from __future__ import annotations

import math

# ---- frozen Rule R-fit constants (P12G freeze; F must remain exactly 3) ----
F = 3.0                       # decision margin
SPREAD_FLOOR = 1e-15          # declared numerical zero (dense/bit-deterministic path)
MESHES = (4, 8, 16, 32)       # Blueprint v1.4 §5.7 prescribed refinement levels
MIN_ADMISSIBLE = 3            # LS rate + 95% CI require dof >= 1
V0_SEED_A = 20260924          # pre-registered start-vector seeds (measurement protocol)
V0_SEED_B = 7
EIGSOLVER_TOL = 1e-14         # frozen solver configuration
EIGSOLVER_MAXITER = 10000
THREADS = 1

# ---- C-1 acceptance predicate constants (P12E authorized, unchanged) ----
P_MIN = 1.0                   # P2: CI lower bound >= weakest non-trivial convergence claim
R_MAX = math.log(1.5)         # P3: every point within a factor 1.5 of the fitted line
FLOOR_MAX = 1e-9              # P4: final-doubling floor datum bound


def spread_used(s):
    """Effective reproducibility used by the rule (declared zero where none is measurable)."""
    if s is None:
        return SPREAD_FLOOR
    return max(float(s), SPREAD_FLOOR)


def is_admissible(e, s):
    """Strict admission test for one level."""
    return bool(float(e) > F * spread_used(s))


def level_ratio(e, s):
    return float(e) / spread_used(s)


def decide(errs, spreads, meshes=MESHES):
    """Full per-level decision record for one configuration."""
    out = []
    for n, e, s in zip(meshes, errs, spreads):
        if e is None:
            continue
        out.append(dict(mesh=n, err=e, spread=s, spread_used=spread_used(s),
                        ratio=level_ratio(e, s), admissible=is_admissible(e, s)))
    return out


def admissible_subset(errs, spreads, meshes=MESHES):
    """(admissible meshes, excluded meshes) under the frozen rule."""
    recs = decide(errs, spreads, meshes)
    return ([r["mesh"] for r in recs if r["admissible"]],
            [r["mesh"] for r in recs if not r["admissible"]])


def lsq_loglog(hs, errs):
    """Least-squares log-log slope with 95% CI (Student t, dof = n-2) and max abs residual."""
    x = [math.log(h) for h in hs]
    y = [math.log(e) for e in errs]
    n = len(x)
    xm, ym = sum(x) / n, sum(y) / n
    sxx = sum((xi - xm) ** 2 for xi in x)
    slope = sum((xi - xm) * (yi - ym) for xi, yi in zip(x, y)) / sxx
    intercept = ym - slope * xm
    resid = [yi - (intercept + slope * xi) for xi, yi in zip(x, y)]
    dof = n - 2
    se = math.sqrt(sum(r * r for r in resid) / dof / sxx)
    tcrit = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776}.get(dof, 1.96)
    return dict(slope=slope, lo=slope - tcrit * se, hi=slope + tcrit * se, se=se,
                resid_max=max(abs(r) for r in resid), n=n, dof=dof)


def fit_admissible(errs, spreads, meshes=MESHES):
    """Apply the rule, then fit the admissible levels.  Returns the full record."""
    adm, exc = admissible_subset(errs, spreads, meshes)
    rec = dict(admissible=adm, excluded=exc, reportable=len(adm) >= MIN_ADMISSIBLE, fit=None)
    if rec["reportable"]:
        hs = [1.0 / n for n in adm]
        rec["fit"] = lsq_loglog(hs, [errs[list(meshes).index(n)] for n in adm])
    return rec


def check_criterion(errs, d16_32, ci_lo, resid_max):
    """Authorized P1–P4 5i acceptance (C-1).  Returns the four predicate outcomes."""
    errs = [e for e in errs if e is not None]
    return {
        "P1_monotone_decreasing": bool(all(b < a for a, b in zip(errs, errs[1:]))),
        "P2_ci_lower_ge_P_MIN": bool(ci_lo >= P_MIN),
        "P3_powerlaw_residual_le_R_MAX": bool(resid_max <= R_MAX),
        "P4_floor_datum_le_FLOOR_MAX": bool(d16_32 <= FLOOR_MAX),
    }
