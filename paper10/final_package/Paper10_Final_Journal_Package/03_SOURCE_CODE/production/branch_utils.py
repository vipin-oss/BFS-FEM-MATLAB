"""
Branch classification and tracking utilities (Phase-A correction, rev.2)
=========================================================================
Corrects the mode-classification / branch-tracking defect that affected the
dispersion and attenuation figures (vertical evanescent lines in the
dispersion diagrams; spurious attenuation spikes and branch-hopping in the
tracked acoustic branch).

Physics-correct classification (plotting layer only -- the solver and all
frozen datasets are untouched):

  A Bloch mode recorded at (kr, ki) is genuinely PROPAGATING iff
      kr_a_over_pi > kr_min            (not pinned to a zone centre with a
                                        purely imaginary/complex wavenumber)
      alpha_a     < alpha_pass         (negligible spatial attenuation)
      [kr_a       < kr_max  optionally, matching the frozen production
       is_pass_band convention kr_a < pi - 0.01, which excludes the
       zone-boundary standing-wave points kr/pi -> 1 from pass-band
       statistics when requested]

Everything else is EVANESCENT/COMPLEX-WAVENUMBER.

Acoustic-branch extraction (rev.2 -- continuity-constrained)
------------------------------------------------------------
At each frequency the branch point is selected among the genuinely
propagating modes by CONTINUITY, not by alpha alone:

  1. Candidates within `continuity_window` of the previous accepted
     branch kr are collected; the least-attenuated among THEM is chosen
     (continuity first, attenuation as tie-breaker).
  2. If no candidate lies within the window, the least-attenuated
     propagating mode overall is chosen and flagged `_hopped = True`
     (a transparent, auditable branch swap -- e.g. a genuine branch
     termination).
  3. At frequencies with NO propagating mode (stop bands) the
     least-attenuated mode overall is used so the curve continues
     through the gap, flagged `_is_prop = False`; the continuity anchor
     is intentionally NOT updated from such fallback picks (an
     evanescent continuation must not poison the continuity test).

This is the sequential analogue of the Hungarian assignment used for the
branch_id labels, applied consistently to the acoustic-branch extraction.
"""

import math
from collections import defaultdict

# Same thresholds as the frozen production `is_pass_band` definition
ALPHA_PASS = 0.05
KR_MIN = 0.01
KR_MAX = math.pi - 0.01          # kr_a upper bound of the frozen pass-band rule


def classify_mode(rec, alpha_pass=ALPHA_PASS, kr_min=KR_MIN, kr_max=None):
    """Return True if the record is a genuinely propagating Bloch mode.

    With ``kr_max=None`` no upper bound is applied (used for dispersion
    diagrams, where zone-boundary standing-wave points at kr/pi -> 1 are
    real Bloch states and must be shown).  For pass-band statistics and
    branch tracking pass ``kr_max=KR_MAX`` to match the frozen production
    is_pass_band convention.
    """
    kr = float(rec["kr_a_over_pi"])
    return (
        (kr > kr_min)
        and (float(rec["alpha_a"]) < alpha_pass)
        and (kr_max is None or kr < kr_max)
    )


def extract_acoustic_branch(records, alpha_pass=ALPHA_PASS, kr_min=KR_MIN,
                            kr_max=KR_MAX, continuity_window=0.20):
    """Continuity-constrained acoustic-branch extraction (Phase-A rev.2)."""
    by_om = defaultdict(list)
    for r in records:
        by_om[float(r["Omega"])].append(r)

    pts = []
    anchor = None            # kr/pi of the last accepted propagating pick
    for om in sorted(by_om):
        rows = [dict(r) for r in by_om[om]]
        for r in rows:
            r["_is_prop"] = classify_mode(r, alpha_pass, kr_min, kr_max)
        prop = [r for r in rows if r["_is_prop"]]
        if prop:
            if anchor is not None:
                near = [r for r in prop
                        if abs(float(r["kr_a_over_pi"]) - anchor) <= continuity_window]
                best = min(near or prop, key=lambda r: float(r["alpha_a"]))
                best["_hopped"] = not near
            else:
                best = min(prop, key=lambda r: float(r["alpha_a"]))
                best["_hopped"] = False
            anchor = float(best["kr_a_over_pi"])
            best["_is_prop"] = True
        else:
            best = min(rows, key=lambda r: float(r["alpha_a"]))
            best["_is_prop"] = False
            best["_hopped"] = False
            # anchor deliberately left unchanged (stop-band fallback)
        pts.append(best)
    return pts


def spike_runs(pts, threshold):
    """Contiguous [Omega_L, Omega_U, peak] runs along a branch where alpha > threshold."""
    runs = []
    in_run = False
    start = None
    peak = 0.0
    prev_om = None
    for p in pts:
        om = float(p["Omega"])
        if float(p["alpha_a"]) > threshold:
            if not in_run:
                in_run, start, peak = True, om, float(p["alpha_a"])
            else:
                peak = max(peak, float(p["alpha_a"]))
        else:
            if in_run:
                runs.append((round(start, 4), round(prev_om, 4), round(peak, 4)))
                in_run = False
        prev_om = om
    if in_run:
        runs.append((round(start, 4), round(prev_om, 4), round(peak, 4)))
    return runs
