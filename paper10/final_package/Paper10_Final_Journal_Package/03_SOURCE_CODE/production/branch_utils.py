"""
Branch classification and tracking utilities (Phase-A correction)
=================================================================
Corrects the mode-classification / branch-tracking defect that affected the
dispersion and attenuation figures (vertical evanescent lines in the
dispersion diagrams; spurious attenuation spikes in the tracked acoustic
branch).

Physics-correct classification (plotting layer only -- the solver and all
frozen datasets are untouched):

  A Bloch mode recorded at (kr, ki) is genuinely PROPAGATING iff
      kr > kr_min            (not pinned to the zone centre with purely
                              imaginary/complex wavenumber)
      alpha_a < alpha_pass   (negligible spatial attenuation)

  Everything else is EVANESCENT/COMPLEX-WAVENUMBER (including the
  band-edge modes with |kr| -> 0 and alpha >= 0.05, and the strongly
  attenuated zone-boundary modes inside stop bands).

The acoustic branch used for attenuation figures is, at each frequency,
the *least-attenuated genuinely propagating* mode; inside stop bands (no
propagating candidate) it falls back to the least-attenuated mode overall
(the band-edge continuation), flagged as non-propagating.
"""

from collections import defaultdict

# Same thresholds as the frozen production `is_pass_band` definition
ALPHA_PASS = 0.05
KR_MIN = 0.01


def classify_mode(rec, alpha_pass=ALPHA_PASS, kr_min=KR_MIN):
    """Return True if the record is a genuinely propagating Bloch mode."""
    return (float(rec["kr_a_over_pi"]) > kr_min) and (float(rec["alpha_a"]) < alpha_pass)


def extract_acoustic_branch(records, alpha_pass=ALPHA_PASS, kr_min=KR_MIN):
    """Phase-A corrected acoustic-branch extraction.

    At each frequency the branch point is the least-attenuated genuinely
    propagating mode (the acoustic branch is, by definition, the mode with
    minimal spatial attenuation).  If no mode at that frequency propagates
    (stop band), the least-attenuated mode overall is used so the curve
    continues through the gap, flagged with ``_is_prop = False``.

    Returns a list of dict copies sorted by Omega, each carrying the boolean
    flag ``_is_prop``.
    """
    by_om = defaultdict(list)
    for r in records:
        by_om[float(r["Omega"])].append(r)

    pts = []
    for om in sorted(by_om):
        rows = [dict(r) for r in by_om[om]]
        for r in rows:
            r["_is_prop"] = classify_mode(r, alpha_pass, kr_min)
        prop = [r for r in rows if r["_is_prop"]]
        best = min(prop or rows, key=lambda r: float(r["alpha_a"]))
        best["_is_prop"] = bool(prop)
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
        if prev_om is not None and om - prev_om > 1e-9 + 1e-12:
            pass  # uniform grid; no gap handling needed
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
