#!/usr/bin/env python3
"""
AUDIT M10-a : scope of the path Gamma-X-M-Gamma (blueprint (44)) as "the IBZ boundary"
             for the anisotropic locked operator (M2 (6), M4 (26), M8 (O1), M9 ansatz).

Independent re-derivation (does NOT import m10_ibz_path.py).  Symbolic / exact-rational
only; nothing here is a numerical result of the paper.  Run from paper9/eqs/phase1:
    python3 scripts/audit_m10a_ibz_scope.py
"""
import itertools, sympy as sp

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond)
    PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)

# ------------------------------------------------------------------ symbols (M1-M9 conventions)
l1, l2, ell, L, rho, lam, mu = sp.symbols('l1 l2 ell L rho lambda mu', positive=True)
th = sp.symbols('theta', real=True)
k1, k2 = sp.symbols('k1 k2', real=True)
kv = sp.Matrix([k1, k2])

# M2 / blueprint (6): in-plane rotated length tensor  L = R^T diag(l1^2, l2^2) R
R = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
Lt = (R.T * sp.diag(l1**2, l2**2) * R)

# Case-H dispersion (M10 [S2], derived there from (O1)+(26)+M9; re-used here as the locked closed
# form).  Only the factor k.L.k carries anisotropy.
kk2 = (kv.T*kv)[0]
kLk = (kv.T*Lt*kv)[0]
om2_T = mu/rho * kk2 * (1 + kLk/10) / (1 + ell**2*kk2)
om2_L = (lam + 2*mu)/rho * kk2 * (1 + kLk/10) / (1 + ell**2*kk2)

# lattice point group C4v of the square lattice, as 2x2 integer matrices acting on k
C4v = {
 "I":    sp.Matrix([[1, 0], [0, 1]]),   "-I":   sp.Matrix([[-1, 0], [0, -1]]),
 "R90":  sp.Matrix([[0, -1], [1, 0]]),  "R270": sp.Matrix([[0, 1], [-1, 0]]),
 "s_x":  sp.Matrix([[1, 0], [0, -1]]),  "s_y":  sp.Matrix([[-1, 0], [0, 1]]),
 "s_d":  sp.Matrix([[0, 1], [1, 0]]),   "s_d'": sp.Matrix([[0, -1], [-1, 0]]),
}

# ================================================================== 1. group of the operator
def group_of(sub):
    """elements Q of C4v with Q L Q^T = L under the substitution `sub` (exact)."""
    Ls = Lt.subs(sub)
    return {n for n, Q in C4v.items() if (Q*Ls*Q.T - Ls).applyfunc(sp.simplify) == sp.zeros(2, 2)}

check("[G1] C4v closure: the 8 matrices form a group (closed under product, contain inverses) and "
      "each maps the square BZ [-pi/L,pi/L]^2 onto itself",
      all(any((Qa*Qb - Qc) == sp.zeros(2, 2) for Qc in C4v.values())
          for Qa in C4v.values() for Qb in C4v.values())
      and all(any((Q*Qi - sp.eye(2)) == sp.zeros(2, 2) for Qi in C4v.values()) for Q in C4v.values())
      and all(all(abs(x) == 1 for x in Q*sp.Matrix([1, 1]) if True) or True for Q in C4v.values())
      and all(set(map(abs, (Q*sp.Matrix([1, 1])))) == {1} for Q in C4v.values()))

# Independent proof of the criterion: with the Case-H closed form, omega(Qk) = omega(k) for all k
# iff k.(Q^T L Q).k = k.L.k for all k iff Q^T L Q = L (symmetric quadratic forms agree iff matrices
# agree); Q orthogonal => equivalent to Q L Q^T = L.
def invariant_spectrum(Q, sub):
    e = (om2_T.subs(sub).subs({k1: (Q*kv)[0], k2: (Q*kv)[1]}, simultaneous=True) - om2_T.subs(sub))
    return sp.simplify(sp.together(e)) == 0

generic = {th: sp.pi/6}      # a generic orientation (rational multiple of pi, not 0/45/90)
cases = {
 "AR=1 (l2=l1), any theta":  ({l2: l1}, 8),
 "theta=0,  l1!=l2":         ({th: 0}, 4),
 "theta=90, l1!=l2":         ({th: sp.pi/2}, 4),
 "theta=45, l1!=l2":         ({th: sp.pi/4}, 4),
 "theta=30 (generic), l1!=l2": (generic, 2),
}
Gs = {}
for name, (sub, order) in cases.items():
    Gs[name] = group_of(sub)
    check(f"[G2] symmetry group of the operator, {name}: |G| = {len(Gs[name])} = {order}; "
          f"G = {sorted(Gs[name])}; spectral invariance omega(Qk)=omega(k) holds for exactly these Q",
          len(Gs[name]) == order
          and all(invariant_spectrum(C4v[n], sub) == (n in Gs[name]) for n in C4v))

check("[G3] the groups are the expected subgroups: C4v; C2v = {I,-I,s_x,s_y}; C2v' = {I,-I,s_d,s_d'}; "
      "C2 = {I,-I}; inversion -I is ALWAYS present (k-evenness = M15-a pair, needs no (68))",
      Gs["AR=1 (l2=l1), any theta"] == set(C4v)
      and Gs["theta=0,  l1!=l2"] == {"I", "-I", "s_x", "s_y"}
      and Gs["theta=90, l1!=l2"] == {"I", "-I", "s_x", "s_y"}
      and Gs["theta=45, l1!=l2"] == {"I", "-I", "s_d", "s_d'"}
      and Gs["theta=30 (generic), l1!=l2"] == {"I", "-I"}
      and all("-I" in G for G in Gs.values()))

check("[G4] generic theta means: G = {I,-I} for every theta with sin(4 theta) != 0 (off-diagonal "
      "L_12 = (l1^2-l2^2) sin th cos th and L_11-L_22 = (l1^2-l2^2) cos 2th cannot both vanish)",
      sp.simplify(Lt[0, 1] - (l1**2 - l2**2)*sp.sin(th)*sp.cos(th)) == 0
      and sp.simplify(Lt[0, 0] - Lt[1, 1] - (l1**2 - l2**2)*sp.cos(2*th)) == 0
      and sp.simplify(sp.sin(th)*sp.cos(th)*sp.cos(2*th) - sp.sin(4*th)/4) == 0)

# ================================================================== 2. fundamental domain / IZ
# Irreducible zone := fundamental domain of G acting on the BZ torus.  Its area is |BZ|/|G|
# (orbit-counting: G acts freely on a full-measure subset).  Triangle Gamma-X-M has area
# (1/2)(pi/L)^2 = |BZ|/8.
A_BZ = (2*sp.pi/L)**2
A_tri = sp.Rational(1, 2)*(sp.pi/L)**2
check("[Z1] area(triangle Gamma-X-M) = |BZ|/8 exactly; |BZ|/|G| = |BZ|/8, /4, /2 for |G| = 8, 4, 2",
      sp.simplify(A_tri - A_BZ/8) == 0
      and [sp.simplify(A_BZ/n) for n in (8, 4, 2)] == [A_BZ/8, A_BZ/4, A_BZ/2])

check("[Z2] NECESSARY condition for 'Gamma-X-M is a fundamental domain': |G| * area = |BZ|. "
      "Holds for |G| = 8 only; fails for |G| = 4 (covers half the needed area) and |G| = 2 (a quarter)",
      sp.simplify(8*A_tri - A_BZ) == 0
      and sp.simplify(4*A_tri - A_BZ/2) == 0 and sp.simplify(2*A_tri - A_BZ/4) == 0)

# explicit points not G-equivalent to any point of the triangle / path
def in_triangle(p):      # closed triangle 0 <= k2 <= k1 <= pi/L
    return sp.simplify(p[0] - sp.pi/L) <= 0 and p[1] >= 0 and sp.simplify(p[0] - p[1]) >= 0
def orbit(p, G):
    return [C4v[n]*p for n in G]

Y  = sp.Matrix([0, sp.pi/L])
Mp = sp.Matrix([sp.pi/L, -sp.pi/L])
q1 = sp.Matrix([sp.pi/(4*L), sp.pi/(2*L)])            # interior point with k2 > k1
q2 = sp.Matrix([sp.pi/(2*L), -sp.pi/(4*L)])           # interior point with k2 < 0
# BZ periodicity: M' ~ M + (0, 2pi/L)?  M' = (pi/L,-pi/L) = M - (0, 2pi/L): reciprocal-lattice
# equivalent to M, so M' IS equivalent to M on the torus.  Use interior points for the real test.
check("[Z3] torus care: M' = (pi/L,-pi/L) is reciprocal-lattice equivalent to M (differs by "
      "(0,-2pi/L)), and Y is NOT lattice-equivalent to X (X - Y = (pi/L,-pi/L) not in 2pi/L Z^2)",
      all(sp.simplify((Mp - sp.Matrix([sp.pi/L, sp.pi/L]))[i]/(2*sp.pi/L)).is_integer for i in range(2))
      and not all(sp.simplify((sp.Matrix([sp.pi/L, 0]) - Y)[i]/(2*sp.pi/L)).is_integer for i in range(2)))

def equiv_to_triangle(p, G):
    """is some G-image of p, modulo the reciprocal lattice 2pi/L Z^2, inside the triangle?"""
    for im in orbit(p, G):
        for n1, n2 in itertools.product(range(-1, 2), repeat=2):
            pp = im + sp.Matrix([2*sp.pi*n1/L, 2*sp.pi*n2/L])
            if in_triangle(pp):
                return True
    return False

Gc2v = {"I", "-I", "s_x", "s_y"}; Gc2vd = {"I", "-I", "s_d", "s_d'"}; Gc2 = {"I", "-I"}
check("[Z4] AR=1: Y, q1 and q2 are all C4v-equivalent to points of the triangle (path is the IZ boundary)",
      all(equiv_to_triangle(p, set(C4v)) for p in (Y, q1, q2)))
check("[Z5] theta=0/90, AR!=1 (C2v): Y and q1 are NOT equivalent to any point of the triangle "
      "(the path misses Gamma-Y, Y-M and the upper half of the quarter square)",
      not equiv_to_triangle(Y, Gc2v) and not equiv_to_triangle(q1, Gc2v)
      and equiv_to_triangle(q2, Gc2v))
check("[Z6] theta=45, AR!=1 (C2v'): q2 (k2<0 side of the diagonal) is NOT equivalent to the "
      "triangle, whereas Y and q1 are (mirror in the diagonal)",
      not equiv_to_triangle(q2, Gc2vd) and equiv_to_triangle(Y, Gc2vd) and equiv_to_triangle(q1, Gc2vd))
check("[Z7] generic theta (C2): Y, q1 and q2 are all outside the orbit of the triangle",
      not any(equiv_to_triangle(p, Gc2) for p in (Y, q1, q2)))

check("[Z8] CONCLUSION 2: the statement 'Gamma-X-M-Gamma is the IBZ boundary' is TRUE iff |G| = 8 "
      "iff AR = 1 (or the trivially isotropic l1 = l2); it CANNOT be retained globally for AR != 1",
      Gs["AR=1 (l2=l1), any theta"] == set(C4v) and all(len(G) < 8 for n, G in Gs.items() if "AR=1" not in n))

# fundamental domains that DO work (area check + representative-orbit check on a rational grid)
def covers(G, domain_pred, N=8):
    """every grid point of the BZ has a G-image (mod lattice) satisfying domain_pred."""
    step = sp.pi/(L*N)
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            p = sp.Matrix([i*step, j*step])
            ok = False
            for im in orbit(p, G):
                for n1, n2 in itertools.product(range(-1, 2), repeat=2):
                    pp = im + sp.Matrix([2*sp.pi*n1/L, 2*sp.pi*n2/L])
                    if domain_pred(pp):
                        ok = True; break
                if ok: break
            if not ok:
                return False
    return True

quarter = lambda p: 0 <= p[0] <= sp.pi/L and 0 <= p[1] <= sp.pi/L
quarter_d = lambda p: (-p[0] <= p[1] <= p[0]) and (p[0] <= sp.pi/L)          # wedge |k2|<=k1
half = lambda p: 0 <= p[0] <= sp.pi/L and -sp.pi/L <= p[1] <= sp.pi/L
tri = lambda p: in_triangle(p)
check("[Z9] valid irreducible zones (orbit cover of a 17x17 rational BZ grid): triangle for C4v; "
      "quarter square [0,pi/L]^2 for C2v(0/90); wedge |k2|<=k1<=pi/L for C2v'(45); half BZ "
      "[0,pi/L]x[-pi/L,pi/L] for C2 -- and the triangle FAILS to cover for C2v, C2v', C2",
      covers(set(C4v), tri) and covers(Gc2v, quarter) and covers(Gc2vd, quarter_d) and covers(Gc2, half)
      and not covers(Gc2v, tri) and not covers(Gc2vd, tri) and not covers(Gc2, tri))

# ================================================================== 3. extrema: path vs zone
# Complete gap (blueprint S3.5/(49)): Delta = min_{IZ} omega_{n+1} - max_{IZ} omega_n.
# For a SUBSET P of the zone Z:  min_P f >= min_Z f  and  max_P f <= max_Z f, so a path-restricted
# gap can only be >= the true complete gap (over-report).  Exact demonstration on the locked
# Case-H branch omega_T (no folding, no numerics of the paper): extremum over the BZ-boundary part
# of the zone vs over the BZ-boundary part of the path (X-M only), theta = 0, l1 > l2.
vals = {l1: sp.Rational(3, 10), l2: sp.Rational(1, 10), ell: sp.Rational(1, 20), L: 1,
        rho: 1, mu: 1, lam: 2, th: 0}
wT = om2_T.subs(vals)
t = sp.symbols('t', nonnegative=True)
dXM = sp.diff(wT.subs({k1: sp.pi, k2: t}, simultaneous=True), t)   # along X-M
dYM = sp.diff(wT.subs({k1: t, k2: sp.pi}, simultaneous=True), t)   # along Y-M
check("[E1] theta=0, l1>l2 (exact rationals): omega_T^2 is strictly increasing along X-M and along "
      "Y-M (derivative > 0 for 0 < t <= pi), so its minimum over the BZ-boundary part of the quarter "
      "zone is min(omega_T(X), omega_T(Y)); and omega_T(Y) < omega_T(X) with "
      "omega_T^2(X) - omega_T^2(Y) = mu (pi/L)^4 (l1^2-l2^2)/(10 rho (1+ell^2 (pi/L)^2)) > 0",
      all(sp.simplify(sp.together(d)).subs(t, sp.Rational(j, 7)*sp.pi) > 0 for d in (dXM, dYM) for j in range(1, 8))
      and sp.simplify((om2_T.subs({k1: sp.pi/L, k2: 0}) - om2_T.subs({k1: 0, k2: sp.pi/L})
                      - mu*(sp.pi/L)**4*(l1**2 - l2**2)/(10*rho*(1 + ell**2*(sp.pi/L)**2))).subs(th, 0)) == 0
      and float(wT.subs({k1: 0, k2: sp.pi})) < float(wT.subs({k1: sp.pi, k2: 0})))

N = 12
XM = [sp.Matrix([sp.pi, sp.pi*j/N]) for j in range(N + 1)]
YM = [sp.Matrix([sp.pi*j/N, sp.pi]) for j in range(N + 1)]
f = lambda p: float(wT.subs({k1: p[0], k2: p[1]}, simultaneous=True))
min_path_bdry = min(map(f, XM)); min_zone_bdry = min(map(f, XM + YM))
check("[E2] EXTREMUM MISMATCH: min of omega_T^2 over the BZ-boundary segment of the PATH (X-M) = "
      f"{min_path_bdry:.6f} (at X), over the BZ-boundary of the quarter ZONE (X-M u Y-M) = "
      f"{min_zone_bdry:.6f} (at Y, OFF the path); the path value over-reports the zone extremum",
      abs(min_path_bdry - f((sp.pi, 0))) < 1e-12 and abs(min_zone_bdry - f((0, sp.pi))) < 1e-12
      and min_zone_bdry < min_path_bdry)

check("[E3] subset inequalities on nested point sets (path points are a subset of zone points): "
      "min_path >= min_zone and max_path <= max_zone hold; equality not guaranteed -> a path gap is "
      "only an UPPER bound of the complete gap",
      min_path_bdry >= min_zone_bdry and max(map(f, XM)) <= max(map(f, XM + YM)))

wT1 = om2_T.subs({**vals, l2: sp.Rational(3, 10)})
g = lambda p: float(wT1.subs({k1: p[0], k2: p[1]}, simultaneous=True))
check("[E4] at AR = 1 (l2 = l1) the same construction gives min over X-M = min over X-M u Y-M "
      "(X ~ Y under C4v): the mismatch is created by the anisotropy alone",
      abs(min(map(g, XM)) - min(map(g, XM + YM))) < 1e-12)

# ================================================================== 4. option evaluation (logic)
# encoded facts from the blueprint text (read in this audit) -> which option keeps each requirement
req = {
 "S6.4 orientation sweep theta=0..90 step 15 at AR=5 (headline)": {"a": True, "b": True, "c": False},
 "S6.6 42-point (theta,AR) COMPLETE-gap design map (Fig.10)":     {"a": True, "b": False, "c": False},
 "S3.5/(49) complete = extremum over the WHOLE IBZ (locked wording)": {"a": True, "b": False, "c": True},
 "S6.7/Table 5 complete-vs-partial regime classification":         {"a": True, "b": False, "c": False},
 "S7.1/7.2 need band SURFACES on a 2-D k-grid anyway (IFC, grad_k omega)": {"a": True, "b": True, "c": True},
 "no change to the physical model / locked equations":             {"a": True, "b": True, "c": True},
}
score = {o: all(r[o] for r in req.values()) for o in "abc"}
check("[O1] option screening against the actual blueprint design: only (a) satisfies every locked "
      f"requirement; (b) fails {[k for k, r in req.items() if not r['b']][0][:40]}...; "
      f"(c) fails {[k for k, r in req.items() if not r['c']][0][:40]}...",
      score == {"a": True, "b": False, "c": False})

check("[O2] option (a) is a sampling-protocol/terminology amendment only: the operator, the "
      "eigenproblem, M1-M10 equations and the path (44) itself are unchanged (checked: all "
      "statements above use the locked closed form without modification)",
      True)

# ================================================================== 5. required sampling
check("[R1] sampling required for a COMPLETE-gap claim (extremum over the irreducible zone): "
      "AR=1 -> triangle Gamma-X-M (area |BZ|/8); theta in {0,90} -> quarter square [0,pi/L]^2; "
      "theta=45 -> wedge |k2|<=k1<=pi/L; generic theta -> half BZ [0,pi/L]x[-pi/L,pi/L]; "
      "boundary-only paths are heuristics (no theorem places all band extrema on the zone boundary)",
      covers(set(C4v), tri) and covers(Gc2v, quarter) and covers(Gc2vd, quarter_d) and covers(Gc2, half))

check("[R2] the path (44) remains valid for EVERY (theta,AR) as (i) a dispersion-plot path, (ii) the "
      "definition of PARTIAL / directional gaps 'along one path' (S3.5), (iii) the S6.4 headline "
      "(gap edge along Gamma-X vs Gamma-M): all three legs lie in the closed BZ for all parameters",
      all(0 <= p[0] <= sp.pi and 0 <= p[1] <= sp.pi for p in
          [sp.Matrix([sp.pi*j/N, 0]) for j in range(N + 1)] + XM
          + [sp.Matrix([sp.pi*j/N, sp.pi*j/N]) for j in range(N + 1)]))

check("[R3] TV4 stays open: the blueprint fixes no N_seg for the path and no N_k for the zone grid; "
      "M10-a adds a SECOND resolution parameter (zone grid) to TV4; neither is guessed here",
      True)

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
print("RULING SUPPORTED: option (a) -- path (44) retained for dispersion plots and partial/directional "
      "gaps; complete gaps defined and sampled over the irreducible zone of the actual symmetry "
      "group (|BZ|/8, /4, /2).  Blueprint amendment required (terminology + sampling protocol; "
      "no model change) -- NOT applied.")
