"""Branch solvers (architecture items 8-9).

PRODUCTION route (frozen blueprint §6-7; task §12):
    prescribed real Omega  ->  solve real positive k*  ->  V* = Omega/k*.
k* is the SOLVED branch variable; k* = 1 is only an initial guess for the
first continuation point; k0 is only the nondimensionalisation scale.
Physical wavelength: lambda = 2*pi/(k* * k0).

ALTERNATE route (two-path consistency test, F2):
    prescribed real k*  ->  solve real positive Omega  ->  V* = Omega/k*.

Safeguards (blueprint §13 / task §13): log scan (NaN-aware: points without
exactly five admissible roots are invalid and never treated as data) +
local bracketed minimisation of every interior candidate; continuation
seed refined independently; jump detection; acceptance by residual level
(r < r_accept -> 'accepted', else 'resolved_min' with the residual
recorded); failures recorded as no_branch, never invented.
"""
import math
import numpy as np
from scipy.optimize import minimize_scalar
from . import residual as rs

_BIG = 1.0e6   # finite stand-in for invalid points INSIDE the optimiser only

# Branch-selection heuristic (documented in the audit): a tracked
# (continuation) candidate is preferred over the global-scan winner
# unless it is STALE:
#   yk > BRANCH_COMPETITION_RATIO * r_global      (global much better), or
#   yk > PREV_R_GROWTH * r_prev                   (residual jump along the
#                                                  sweep - branch lost), or
#   yk > R_STALE_ABS                              (above every legitimate
#                                                  resolved minimum of this
#                                                  system).
# Empirical calibration: legitimate tracked/competitor residual ratios
# peak near 100 (C with D_w* -> 1e-8, where the phason-branch friction
# floor ~1.1e-4 crosses the phonon branch's ~1e-6); stale seeds and
# degenerate regions give ratios >= 3e4 and residuals >= ~1.9e-3, while
# every legitimate resolved minimum in this study is <= 1.11e-4. The
# thresholds leave >= 4x margin on both sides. A true tracked branch
# changes residual by <= ~2x per grid step; 100x allows decade-spaced
# anchors. These affect branch SELECTION only, never branch positions.
BRANCH_COMPETITION_RATIO = 1.0e3
PREV_R_GROWTH = 1.0e2
R_STALE_ABS = 5.0e-4

# Degenerate-minimum rejection (documented in the audit): the secular
# landscape contains quasi-static (V* -> 0) regions where B is
# structurally near-rank-deficient (phason/thermal amplitudes collapse);
# their minima are numerical artifacts, not propagating surface waves.
# Every physical branch of this frozen system has V* >= 0.29 (phason-
# dominated 0.3107, phonon-Rayleigh 0.466); candidates with
# V* = Omega/k < DEGEN_V_MAX are rejected at SELECTION level (positions
# of accepted branches are untouched). If only degenerate candidates
# exist, the point is reported as 'degenerate_only' - never fabricated.
DEGEN_V_MAX = 0.15

def _parabolic_polish(x, f, lo=None, hi=None, h_rel=1e-4, iters=4):
    """Parabolic vertex polish of a scalar minimum ('multiple evaluations
    around the detected minimum', blueprint §13). scipy's bounded Brent
    has a built-in stopping floor of ~sqrt(eps_machine)*|x| ~ 1.5e-8
    relative, which is COARSER than the branch-position tolerance; the
    secular landscape near the minimum is smooth and quadratic (checked),
    so three-point parabola fits converge far below that floor.

    Safeguards: the vertex step is limited to the fit stencil (|(yl-yh)/den|
    <= 3, i.e. vertex within 1.5*h of the centre) so noise-level curvature
    cannot launch unbounded jumps; steps leaving the search bounds or the
    valid region, or increasing the residual, are rejected.
    """
    y0 = f(x)
    if not np.isfinite(y0):
        return x, y0
    xb, yb = x, y0
    h = h_rel
    for _ in range(iters):
        xl, xh = x * (1 - h), x * (1 + h)
        yl, yh = f(xl), f(xh)
        if not (np.isfinite(yl) and np.isfinite(yh)):
            h *= 0.1
            continue
        den = yl - 2 * y0 + yh
        if den <= 0 or abs(yl - yh) > 3.0 * den:
            h *= 0.1
            continue
        dx = 0.5 * h * (yl - yh) / den * x      # vertex offset (relative fit)
        xn = x + dx
        if lo is not None and xn < lo:
            xn = lo
        if hi is not None and xn > hi:
            xn = hi
        yn = f(xn)
        if np.isfinite(yn) and yn <= y0:
            x, y0 = xn, yn
            if yn < yb:
                xb, yb = xn, yn
        h *= 0.1
    return xb, yb

def _refine(lo, hi, f, rel_xtol=1e-12):
    """Bounded scalar minimisation; scipy option is xatol (absolute).
    Final parabolic polish removes Brent's sqrt(eps) stopping floor;
    the polish stays inside the search bounds [lo, hi]."""
    xatol = rel_xtol * 0.5 * (abs(lo) + abs(hi))
    xatol = max(xatol, 1e-300)
    fb = lambda x: (lambda v: _BIG if not np.isfinite(v) else v)(f(x))
    res = minimize_scalar(fb, bounds=(lo, hi), method="bounded",
                          options=dict(xatol=xatol))
    x, y = _parabolic_polish(float(res.x), f, lo=lo, hi=hi)
    return x, y              # TRUE residual returned (may be NaN)

def _local_minima(xs, ys):
    """Interior indices whose finite value does not exceed finite neighbours."""
    idx = []
    for i in range(1, len(xs) - 1):
        y = ys[i]
        if not np.isfinite(y):
            continue
        l, r = ys[i - 1], ys[i + 1]
        if (not np.isfinite(l) or y <= l) and (not np.isfinite(r) or y <= r):
            idx.append(i)
    return idx

def _valid_intervals(xs, ys, min_points=2):
    """Maximal contiguous runs of finite residual values on the scan grid."""
    intervals = []
    start = None
    for i, y in enumerate(ys):
        if np.isfinite(y):
            if start is None:
                start = i
        else:
            if start is not None and i - start >= min_points:
                intervals.append((start, i - 1))
            start = None
    if start is not None and len(ys) - start >= min_points:
        intervals.append((start, len(ys) - 1))
    return intervals

def _adaptive_candidates(xs, f, ys, n_fine=48):
    """Candidate brackets from every valid interval: extended endpoint
    brackets (branches can sit AT the edge of the admissible-root region,
    e.g. model A just inside its grazing boundary) plus interior
    local minima of a fine scan. Purely a numerical search refinement.
    """
    n = len(xs)
    brackets = []
    for (a, b) in _valid_intervals(xs, ys, min_points=1):
        # extended endpoint brackets (reach one grid point beyond the
        # interval; invalid side is handled by the optimiser's NaN guard)
        if a > 0:
            brackets.append((xs[a - 1], xs[min(a + 1, n - 1)]))
        if b < n - 1:
            brackets.append((xs[max(b - 1, 0)], xs[b + 1]))
        if b > a:
            lo, hi = xs[a], xs[b]
            xf = np.geomspace(lo, hi, n_fine)
            yf = np.array([f(x) for x in xf])
            ints = _local_minima(xf, yf)
            for i in ints:
                brackets.append((xf[max(i - 1, 0)], xf[min(i + 1, n_fine - 1)]))
            if not ints:
                fin = np.flatnonzero(np.isfinite(yf))
                if len(fin):
                    j = int(fin[np.argmin(yf[fin])])
                    brackets.append((xf[max(j - 1, 0)], xf[min(j + 1, n_fine - 1)]))
    return brackets

def refine_branch_near(Omega, model, m, bc, k_center, rel_width=0.03,
                       n_scan=401, rel_xtol=1.0e-13):
    """Branch-anchored candidate search: refine the local minimum of r(k)
    nearest to k_center within +/- rel_width (same refinement machinery
    as solve_k_at_Omega; degenerate quasi-static minima rejected).

    Purpose: branch-IDENTITY verification of continuation seeds. When the
    intended physical branch is known from the corresponding limit model
    (e.g. C(D_w*->0) must connect continuously, in model space, to model
    A's tracked branch), the seed candidate must be the local minimum
    near k_center = Omega / V_ref, NOT necessarily the global argmin:
    near-grazing branch minima can be far narrower than the generic scan
    step (measured width ~1.5e-4 relative at Omega=1000), so a generic
    enumeration can miss them entirely while finding spurious edge
    minima. Returns dict {'k','r'} or None.

    Returns None when no local minimum exists in the window - callers
    must treat that as 'intended branch not present', never substitute."""
    f = lambda k: rs.r_scalar(k, Omega, model, m, bc)
    xs = np.geomspace((1.0 - rel_width) * k_center,
                      (1.0 + rel_width) * k_center, n_scan)
    ys = np.array([f(x) for x in xs])
    return _refine_candidates(_adaptive_candidates(xs, f, ys), f, rel_xtol,
                              kmax=Omega / DEGEN_V_MAX)


def flag_discontinuities(Omegas, Vs, rel_jump=0.05):
    """Lightweight branch-jump diagnostic for continuation sweeps.

    Flags index i when |V_i / V_prev - 1| > rel_jump between CONSECUTIVE
    RESOLVED points of a tracked branch. On the frozen grids the
    neighbouring-frequency ratio is ~1.10 and physical branches move by
    at most a few percent per step, so the default rel_jump = 0.05 is
    generous (an order of magnitude below the ~50% wrong-branch jump it
    was added to detect; see ARENA_POST_CLAUDE_FIX_AUDIT.md).

    Diagnostic only: it never modifies data. Callers decide the
    consequence (the V3 model-limit test treats any flag as a failure
    because those sweeps must track a single branch by construction).

    Returns a list of (index, relative_change) tuples."""
    flags = []
    prev = None
    Vs = np.asarray(Vs, dtype=float)
    for i, v in enumerate(Vs):
        if not np.isfinite(v):
            continue
        if prev is not None and abs(v / prev - 1.0) > rel_jump:
            flags.append((i, abs(v / prev - 1.0)))
        prev = v
    return flags


def _refine_candidates(brackets, f, rel_xtol, kmax=None):
    """Refine every bracket; return the best point. If kmax is given,
    refined points with k > kmax are rejected (quasi-static degenerate-
    minimum rejection: V = Omega/k would fall below DEGEN_V_MAX)."""
    best = None
    for (lo, hi) in brackets:
        if hi <= lo:
            continue
        xk, yk = _refine(lo, hi, f, rel_xtol)
        if kmax is not None and xk > kmax:
            continue
        if np.isfinite(yk) and (best is None or yk < best[0]):
            best = (yk, xk)
    return None if best is None else dict(r=best[0], k=best[1])

def _window_candidates(f, lo, hi, Omega, m, n_scan):
    """Scan+candidate generation for one k-window (used for the global
    scan, window extensions, and continuation windows alike).

    Grazing-boundary sub-scans (numerical search refinement only):
    physical surface branches accumulate just above the k-values where a
    depth root grazes (Im p -> 0): k_g = Omega / v_c for each real
    characteristic speed v_c of the frozen system (P: sqrt(C11/rho),
    S: sqrt(C66/rho), phason shear: sqrt(K3)). These windows can be
    narrower than the coarse scan step at high Omega (model A and the
    D_w*->0 limit: dip width ~0.4%), so each is re-scanned finely.
    Invalid points (including the boundary itself) are handled by the
    NaN machinery.
    """
    xs = np.geomspace(lo, hi, n_scan)
    ys = np.array([f(x) for x in xs])
    brackets = _adaptive_candidates(xs, f, ys)
    for v_c in (math.sqrt(m.C11 / m.rho), math.sqrt(m.C66 / m.rho),
                math.sqrt(m.K3)):
        k_g = Omega / v_c
        if lo <= k_g <= hi:
            # extend to 1.10*k_g: physical branches sit up to a few percent
            # above grazing (e.g. the phonon branch at Omega/0.4663 = 2.144
            # * Omega, just above the S-grazing sub-scan edge at 2.12)
            xg = np.geomspace(k_g, min(1.10 * k_g, hi), 100)
            yg = np.array([f(x) for x in xg])
            brackets += _adaptive_candidates(xg, f, yg)
    return brackets

def solve_k_at_Omega(Omega, model, m, bc, k_seed=None, n_scan=None,
                     kmin_fac=None, kmax_fac=None, rel_xtol=1e-15,
                     r_prev=None):
    """Production route. Returns record dict; never fabricates a branch.

    k_seed / r_prev: branch-tracking state from the previous sweep point
    (r_prev enables the residual-continuity staleness check)."""
    d = m.defaults
    n_scan = n_scan or int(d["n_scan"])
    kmin_fac = kmin_fac or float(d["scan_kmin_factor"])
    kmax_fac = kmax_fac or float(d["scan_kmax_factor"])
    r_accept = float(d["r_accept"])

    f = lambda k: rs.r_scalar(k, Omega, model, m, bc)   # NaN marks invalid
    k_lo, k_hi = kmin_fac * Omega, kmax_fac * Omega
    k_degen = Omega / DEGEN_V_MAX      # candidate-level degenerate cutoff
    brackets = _window_candidates(f, k_lo, k_hi, Omega, m, n_scan)
    best = _refine_candidates(brackets, f, rel_xtol, kmax=k_degen)
    if best is not None:
        best["route"] = "global"
    # single window extension if the winner sits at the outer edge;
    # an edge winner of the extension is itself suspect and NOT accepted
    # (recorded via the retained interior best + jump/status flags)
    if best is not None and best["k"] > 0.98 * k_hi:
        xs2 = np.geomspace(k_hi, 8.0 * k_hi, n_scan)
        ys2 = np.array([f(x) for x in xs2])
        b2 = _refine_candidates(_adaptive_candidates(xs2, f, ys2), f,
                                rel_xtol, kmax=k_degen)
        if (b2 is not None and b2["r"] < best["r"]
                and b2["k"] < 0.98 * 8.0 * k_hi):
            best = dict(r=b2["r"], k=b2["k"], route="global_ext")
    # continuation candidate: refined with the SAME scan+candidate
    # machinery on a local window (plain bracketed Brent can miss a
    # narrow minimum sitting next to an invalid-region wall).
    #
    # SELECTION RULE (documented in the audit): continuation-preferred,
    # with a competition guard. When a seed is supplied and the tracked
    # branch yields a finite refined residual, it is the reported branch
    # UNLESS its residual exceeds BRANCH_COMPETITION_RATIO times the
    # global-scan winner's residual - in that case the tracked point is
    # not a genuinely resolved branch point at this Omega (e.g. a stale
    # seed far from the branch, or the tracked branch has died) and the
    # global winner is used, with the jump flag set. Rationale: global-
    # argmin selection does not commute with parameter limits (tiny-but-
    # finite phason friction raises the phason-branch residual floor
    # above the phonon branch's while both remain resolved minima), so
    # argmin selection can flip between physical branches mid-sweep;
    # branch tracking keeps V*(Omega) on one physical branch. The
    # staleness calibration (BRANCH_COMPETITION_RATIO = 1e3,
    # R_STALE_ABS = 1e-2, see constants above) leaves ~10x margin
    # between legitimate tracked branches and stale/degenerate
    # candidates; it affects branch SELECTION only, never positions.
    jump = False
    k_comp, r_comp = np.nan, np.nan
    gbest = best                      # global-scan (or extension) winner
    if gbest is not None:
        k_comp, r_comp = gbest["k"], gbest["r"]
    selected = gbest
    if k_seed is not None and np.isfinite(k_seed) and k_seed > 0:
        cbest = _refine_candidates(
            _window_candidates(f, 0.7 * k_seed, 1.4 * k_seed, Omega, m, 96),
            f, rel_xtol, kmax=k_degen)
        if cbest is not None:
            xk, yk = cbest["k"], cbest["r"]
            stale = yk > R_STALE_ABS or (
                gbest is not None and yk > BRANCH_COMPETITION_RATIO * gbest["r"]
            ) or (
                r_prev is not None and np.isfinite(r_prev)
                and yk > PREV_R_GROWTH * r_prev
            )
            if gbest is not None and abs(xk - gbest["k"]) / xk > float(d["branch_jump_flag_rel"]):
                jump = True
            if not stale:
                selected = dict(k=xk, r=yk, route="continuation")
    # (degenerate minima are already rejected at candidate level via
    # kmax; see DEGEN_V_MAX - no physical candidate is ever displaced by
    # a quasi-static artifact, and no artifact is ever reported)
    best = selected
    if best is None or not np.isfinite(best["r"]):
        # diagnostic: was the landscape dominated by degenerate minima?
        raw = _refine_candidates(brackets, f, rel_xtol)   # unfiltered probe
        if raw is not None and raw["k"] > k_degen:
            return dict(Ok=False, Omega=Omega, model=model, k=np.nan, V=np.nan,
                        r=np.nan, n_ad=0, n_grazing=0, condB=np.nan, jump=jump,
                        status="degenerate_only", root_flags=0, max_root_res=np.nan,
                        k_comp=raw["k"], r_comp=raw["r"])
        return dict(Ok=False, Omega=Omega, model=model, k=np.nan, V=np.nan,
                    r=np.nan, n_ad=0, n_grazing=0, condB=np.nan, jump=False,
                    status="no_branch", root_flags=0, max_root_res=np.nan,
                    k_comp=np.nan, r_comp=np.nan)
    full = rs.secular(best["k"], Omega, model, m, bc)
    rr = full["rr"]
    status = "accepted" if best["r"] < r_accept else "resolved_min"
    return dict(Ok=True, Omega=Omega, model=model, k=best["k"],
                V=Omega / best["k"], r=best["r"], n_ad=full["n_ad"],
                n_grazing=full["n_grazing"], condB=full["condB"], jump=jump,
                status=status, root_flags=int(rr["root_flags"].sum()),
                max_root_res=float(np.max(rr["root_residuals"])) if full["n_ad"] else np.nan,
                k_comp=k_comp, r_comp=r_comp)

def solve_Omega_at_k(k, model, m, bc, Om_seed, n_scan=120, rel_xtol=1e-15,
                     n_local=240, local_halfwidth=0.03):
    """Alternate route for the two-path test: fixed real k*, solve Omega.

    The narrow secular dip (~0.3% wide in Omega at fixed k for the
    weakly damped surface mode) sits on a monotone background, so a coarse
    global scan alone cannot bracket it. Per the F2 test definition the
    two routes are compared AT COMMON PHYSICAL BRANCH POINTS: the
    production route supplies Om_seed, and a dense local scan around it
    (plus the coarse global scan, which guards against deeper competing
    minima elsewhere) resolves the dip. This is a numerical search
    refinement only - the residual function and the branch definition are
    unchanged.
    """
    f = lambda Om: rs.r_scalar(k, Om, model, m, bc)
    brackets = []
    xs = np.geomspace(0.3 * Om_seed, 3.0 * Om_seed, n_scan)
    ys = np.array([f(x) for x in xs])
    brackets += _adaptive_candidates(xs, f, ys)
    xl = np.geomspace((1 - local_halfwidth) * Om_seed,
                      (1 + local_halfwidth) * Om_seed, n_local)
    yl = np.array([f(x) for x in xl])
    brackets += _adaptive_candidates(xl, f, yl)
    best = _refine_candidates(brackets, f, rel_xtol)
    if best is None:
        return dict(Ok=False, k=k, Omega=np.nan, V=np.nan, r=np.nan)
    return dict(Ok=True, k=k, Omega=best["k"], V=best["k"] / k, r=best["r"])

def sweep_Omega(Omegas, model, m, bc, **kw):
    """Continuation sweep along the production route."""
    out = []
    k_seed = None
    for Om in Omegas:
        rec = solve_k_at_Omega(Om, model, m, bc, k_seed=k_seed, **kw)
        out.append(rec)
        if rec["Ok"]:
            k_seed = rec["k"]
    return out
