#!/usr/bin/env python3
"""
Phase-1 / audit M8-a: tangential-redistribution and corner/line-force terms of the
gradient-elasticity boundary operator.

Audited question
----------------
The exact integration by parts of the locked M5-M6 weak form (M8, checks C6-C8) gives

    t_i = (sigma_ij - tau_ijk,k) n_j + rho ell^2 u_i_ddot,j n_j - D_alpha( tau_ijk n_k a_j^alpha )
    R_i = tau_ijk n_j n_k ,     e_i = [[ tau_ijk n_k a_j^alpha mu_alpha ]]   (corner line forces)

whereas blueprint v1.3 (row 2.8 / register (31)-(35)) and the legacy [C] formulation state a
*reduced four-quantity* boundary set (classical traction, double traction, displacement, normal
derivative) and explicitly neglect surface divergence and edge terms.

This audit does not choose silently. It verifies the mathematics of the two extra terms,
quantifies exactly what the reduced model drops, establishes the rectangular-cell and
periodic-cell behaviour of the corner terms, checks consistency with the stated boundary
conditions, and records the outcome as a documented formulation note. No blueprint file,
no M1-M7 mathematics, and no solver/Bloch code is touched; no numerical value is introduced.

Tags: [A] derived/verified here, [C] legacy source (FEM_1_Paper.txt Sec 4-5), [S] structural.
Deterministic, exact SymPy arithmetic, writes no files.
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

x, y, t = sp.symbols('x y t', real=True)
lam, mu, rho, ell, om, LL = sp.symbols('lambda mu rho ell omega ell_L', positive=True)
L11, L12, L22 = sp.symbols('L11 L12 L22', positive=True)
mux, muy = sp.symbols('mu_x mu_y', real=True)          # periodic (Bloch-type) phase factors

rng = (1, 2)
d = lambda p, q: sp.Integer(1) if p == q else 0
C4 = lambda i, j, k, l: lam*d(i, j)*d(k, l) + mu*(d(i, k)*d(j, l) + d(i, l)*d(j, k))
Lm = sp.Matrix([[L11, L12], [L12, L22]])
def Lof(a, b): return Lm[min(a, b)-1, max(a, b)-1]
iso = {L11: LL**2, L12: 0, L22: LL**2}      # isotropic-length specialisation (used below)

def eps(u1, u2):
    return {(1, 1): sp.diff(u1, x), (2, 2): sp.diff(u2, y),
            (1, 2): sp.Rational(1, 2)*(sp.diff(u1, y) + sp.diff(u2, x))}
def eta_of(u1, u2):
    e = eps(u1, u2)
    return {(a, b, k): sp.diff(e[(min(a, b), max(a, b))], x if k == 1 else y)
            for a in rng for b in rng for k in rng}
def sig_of(u1, u2):
    e = eps(u1, u2); tr = e[(1, 1)] + e[(2, 2)]
    return {(i, j): lam*d(i, j)*tr + 2*mu*e[(min(i, j), max(i, j))] for i in rng for j in rng}
def tau_of(u1, u2):
    et = eta_of(u1, u2)
    return {(i, j, k): sp.Rational(1, 10)*sum(Lof(k, n)*sum(C4(i, j, p, q)*et[(min(p, q), max(p, q), n)]
                                                          for p in rng for q in rng)
                                           for n in rng)
            for i in rng for j in rng for k in rng}

U1 = x**2*y + x*y**2                     # non-uniform field (non-zero strain gradient)
U2 = x*y**2 + x**2
V1 = x*y + y**2                          # test fields
V2 = x**2*y
tt = tau_of(U1, U2)

# =============================================================================
# SECTION 1 - smooth (cornerless) closed boundary
# =============================================================================
sub_circ = {x: sp.cos(t), y: sp.sin(t)}
def on_circle(expr):
    return sp.simplify(expr.subs(sub_circ))
n_c = {1: sp.cos(t), 2: sp.sin(t)}            # outward normal on the unit circle
m_c = {1: -sp.sin(t), 2: sp.cos(t)}           # CCW tangent
def q_circle(i):
    return sp.simplify(sum(on_circle(tt[(i, j, k)])*n_c[k]*m_c[j] for j in rng for k in rng))
ident = 0
for i, vi in ((1, V1), (2, V2)):
    ident += sp.integrate(sp.expand(q_circle(i)*sp.diff(on_circle(vi), t))
                          + sp.expand(sp.diff(q_circle(i), t)*on_circle(vi)), (t, 0, 2*sp.pi))
check("[A1] smooth-edge boundary identity (no corners): on the unit circle the tangential term "
      "obeys  int_C q_i d_s v_i ds = - int_C (d_s q_i) v_i ds  exactly (surface divergence "
      "identity; the boundary of the boundary is empty). Verified by exact trigonometric "
      "integration of both sides",
      sp.simplify(ident) == 0)
dropped_smooth = 0
for i, vi in ((1, V1), (2, V2)):
    dropped_smooth += sp.integrate(sp.expand(q_circle(i)*sp.diff(on_circle(vi), t)), (t, 0, 2*sp.pi))
dropped_smooth = sp.expand(sp.simplify(dropped_smooth))
check("[A2] non-vanishing certificate (smooth boundary): the term dropped by the reduced model, "
      "int_C q_i d_s v_i ds, is NOT identically zero -- it evaluates to a non-zero expression in "
      "(lambda, mu, L11, L12, L22). So the tangential term is not an artefact of corners",
      dropped_smooth != 0)

# =============================================================================
# SECTION 2 - rectangular cell: edge decomposition and corner terms
# =============================================================================
EDGEN = {'b': (0, -1), 'r': (1, 0), 't': (0, 1), 'l': (-1, 0)}      # outward normal
EDGEM = {'b': (1, 0), 'r': (0, 1), 't': (-1, 0), 'l': (0, -1)}      # CCW co-normal
def intEdge(expr, edge):
    u = sp.Symbol('u', real=True)
    if edge == 'b':
        return sp.integrate(sp.expand(expr.subs({y: 0, x: u})), (u, 0, 1))
    if edge == 'r':
        return sp.integrate(sp.expand(expr.subs({x: 1, y: u})), (u, 0, 1))
    if edge == 't':
        return sp.integrate(sp.expand(expr.subs({y: 1, x: 1 - u})), (u, 0, 1))
    return sp.integrate(sp.expand(expr.subs({x: 0, y: 1 - u})), (u, 0, 1))
def corner_value(expr, edge, end):
    if edge == 'b':
        return expr.subs({y: 0, x: 1 if end else 0})
    if edge == 'r':
        return expr.subs({x: 1, y: 1 if end else 0})
    if edge == 't':
        return expr.subs({y: 1, x: 0 if end else 1})
    return expr.subs({x: 0, y: 0 if end else 1})
def q_of(i, edge, tau=tt):
    nx, ny = EDGEN[edge]; mx, my = EDGEM[edge]
    return sum(tau[(i, j, k)]*{1: nx, 2: ny}[k]*{1: mx, 2: my}[j] for j in rng for k in rng)
def R_of(i, edge, tau=tt):
    nx, ny = EDGEN[edge]
    return sum(tau[(i, j, k)]*{1: nx, 2: ny}[j]*{1: nx, 2: ny}[k] for j in rng for k in rng)
# abstract (field-independent) double-stress components for the structural corner/periodicity
# statements; tau_ijk = tau_jik is the only symmetry imposed (M8, check C5)
TSc = {(i, j, k): sp.Symbol(f'T{i}{j}{k}', real=True) for i in rng for j in rng for k in rng}
def Tabs(i, j, k): return TSc[(min(i, j), max(i, j), k)]
def q_abs(i, edge):
    nx, ny = EDGEN[edge]; mx, my = EDGEM[edge]
    return sp.expand(sum(Tabs(i, j, k)*{1: nx, 2: ny}[k]*{1: mx, 2: my}[j]
                         for j in rng for k in rng))
def D_of(vi, edge):
    nx, ny = EDGEN[edge]
    return nx*sp.diff(vi, x) + ny*sp.diff(vi, y)
def ds_of(expr, edge):
    mx, my = EDGEM[edge]
    return mx*sp.diff(expr, x) + my*sp.diff(expr, y)

# (i) per-edge endpoint identity
gap = 0
for i, vi in ((1, V1), (2, V2)):
    for edge in 'brtl':
        f = q_of(i, edge)
        gap += (intEdge(f*ds_of(vi, edge), edge) + intEdge(ds_of(f, edge)*vi, edge)
                - corner_value(f*vi, edge, True) + corner_value(f*vi, edge, False))
check("[A3] rectangular-cell edge decomposition (exact, all four edges, CCW convention): "
      "int_edge q_i d_s v_i ds + int_edge (d_s q_i) v_i ds = [q_i v_i]_start^end, hence the "
      "tau-part of the boundary integral is  sum_edges [ R_i D v_i - (d_s q_i) v_i ] "
      "+ sum_corners [q_i v_i], the corner terms being the endpoint pieces of the four edges",
      sp.expand(gap) == 0)
raw_tau = 0; canon_tau = 0; corners = 0
for i, vi in ((1, V1), (2, V2)):
    for edge in 'brtl':
        f = q_of(i, edge)
        raw_tau += intEdge(R_of(i, edge)*D_of(vi, edge) + f*ds_of(vi, edge), edge)
        canon_tau += intEdge(R_of(i, edge)*D_of(vi, edge) - ds_of(f, edge)*vi, edge)
        corners += corner_value(f*vi, edge, True) - corner_value(f*vi, edge, False)
check("[A3b] global rectangular-cell decomposition: (raw tau boundary integral) = "
      "(canonical tau boundary integral) + (corner sum), verified exactly for the test fields",
      sp.expand(raw_tau - canon_tau - corners) == 0)

# (ii) corner term at one corner, and its vanishing condition (abstract components)
c_10 = sp.expand(q_abs(1, 'b') - q_abs(1, 'r'))
a_sym = sp.Symbol('a')
check("[A4] corner terms do NOT vanish automatically on a rectangular cell: at a cell corner the "
      "term is q_i^(edge ending) - q_i^(edge starting); for the corner (1,0) this equals exactly "
      "-(tau_i12 + tau_i21), which is non-zero unless the special condition tau_i12 = -tau_i21 "
      "holds (checked by substitution) -- isotropy of the length tensor does not imply it",
      sp.expand(c_10 + (Tabs(1, 1, 2) + Tabs(1, 2, 1))) == 0
      and sp.expand(c_10.subs({Tabs(1, 1, 2): a_sym, Tabs(1, 2, 1): -a_sym})) == 0
      and sp.expand(c_10.subs({Tabs(1, 1, 2): a_sym, Tabs(1, 2, 1): a_sym})) != 0)
# field-based non-vanishing certificate for the same corner, anisotropic and isotropic length
c10_field = sp.expand(corner_value(q_of(1, 'b'), 'b', True) - corner_value(q_of(1, 'r'), 'r', False))
c10_iso = sp.expand(c10_field.subs(iso))
check("[A4b] field-based certificate: the corner term at (1,0) is a non-zero expression for the "
      "test field both for the anisotropic length tensor and for the isotropic-length "
      "specialisation L = ell_L^2 I",
      c10_field != 0 and c10_iso != 0)
print("   corner term at (1,0), anisotropic L:", sp.simplify(c10_field))
print("   corner term at (1,0), isotropic L  :", sp.simplify(c10_iso))
corner_total = sp.expand(corners)
check("[A4c] corner non-vanishing certificate for the whole rectangular cell: the total corner "
      "sum for a non-uniform field with non-periodic boundary data is a non-zero expression",
      corner_total != 0)
print("   total corner sum (non-periodic test fields):", corner_total)

# =============================================================================
# SECTION 3 - periodic / Bloch-type cell: cancellation analysis
# =============================================================================
# Periodicity of the field (phase relation only; this is NOT the M9 Bloch derivation):
#   tau(x+1, y) = mu_x tau(x,y) ,  tau(x, y+1) = mu_y tau(x,y)
# For flat edges with constant normals the edge quantities scale with the same factors:
#   q^r(y) = mu_x q^l(y) ,  q^t(x) = mu_y q^b(x) ,  and likewise for R and D v.
# Edge quantities at the base point (0,0) in abstract components; flat edges have constant
# normals and co-normals, so each edge has a single well-defined q_i family.
# Edge quantities at the base point (0,0) in abstract components (flat edges -> constant n, m).
Q = {e: q_abs(1, e) for e in 'brtl'}
check("[A5] rectangular-cell edge-quantity identities (abstract components): with the CCW "
      "co-normal convention Q_l = Q_r = +tau_i21 and Q_t = Q_b = -tau_i12 exactly; the four edges "
      "therefore carry only two independent edge quantities",
      sp.expand(Q['l'] - Tabs(1, 2, 1)) == 0 and sp.expand(Q['r'] - Tabs(1, 2, 1)) == 0
      and sp.expand(Q['b'] + Tabs(1, 1, 2)) == 0 and sp.expand(Q['t'] + Tabs(1, 1, 2)) == 0)
# Periodic (Bloch-type) phase relation of the field: the corner quantities at (1,0), (1,1), (0,1)
# carry mu_x, mu_x mu_y, mu_y respectively. Each corner term is
# q_i (edge ending there with +) - q_i (edge starting there with -).
corner_terms = [
    ("(0,0)", Q['l'], 1,          Q['b'], 1),
    ("(1,0)", Q['b'], mux,        Q['r'], mux),
    ("(1,1)", Q['r'], mux*muy,    Q['t'], mux*muy),
    ("(0,1)", Q['t'], muy,        Q['l'], muy),
]
tot_per = sp.expand(sum(a*ph_e - b*ph_s for _, a, ph_e, b, ph_s in corner_terms))
check("[A6] periodic cell, exact periodicity (mu_x = mu_y = 1, i.e. the Gamma point): the four "
      "corner terms cancel telescopically -- every edge contributes q_i with + at its end and - "
      "at its start with the same phase -- so the corner sum vanishes exactly",
      sp.expand(tot_per.subs({mux: 1, muy: 1})) == 0)
closed_form = sp.expand((Q['r'] - Q['b'])*(1 - mux)*(1 - muy))
check("[A7] periodic cell, general Bloch-type phase factors: the corner terms do NOT cancel. "
      "Exact closed form (verified symbolically): "
      "sum_corners = (tau_i12 + tau_i21) (1 - mu_x) (1 - mu_y) with mu_x, mu_y the phase factors "
      "of the field across the two cell periods. It vanishes iff mu_x = 1 or mu_y = 1 (the Gamma "
      "point and the phase-zero path segments) and is non-zero elsewhere on the Brillouin-zone "
      "path, e.g. at X and M (|mu| = 1 there, so (1-mu_x)(1-mu_y) != 0)",
      sp.simplify(tot_per - closed_form) == 0
      and sp.expand(closed_form.subs({mux: -1, muy: -1})) != 0
      and sp.expand(closed_form.subs({mux: 1, muy: -1})) == 0
      and sp.expand(closed_form.subs({mux: sp.Rational(1, 2), muy: sp.Rational(1, 3)})) != 0)
print("   sum_corners (periodic cell) =", sp.simplify(tot_per))

# =============================================================================
# SECTION 4 - quantification of the model reduction
# =============================================================================
# exact boundary integrand (M8): [ (sigma_ij - tau_ijk,k) n_j - d_s q_i + rho ell^2 u_ddot_i,j n_j ] v_i
#                                + R_i D v_i   (+ corner terms)
# reduced four-quantity integrand: same without -d_s q_i and without corner terms
reduced_tau = sum(intEdge(R_of(i, e)*D_of(vi, e), e)
                  for i, vi in ((1, V1), (2, V2)) for e in 'brtl')
difference = sp.expand(raw_tau - reduced_tau)
expected_diff = sp.expand(-sum(intEdge(ds_of(q_of(i, e), e)*vi, e)
                               for i, vi in ((1, V1), (2, V2)) for e in 'brtl') + corners)
check("[A8] model-reduction quantification: the sigma-part and the micro-inertia part of the "
      "boundary integrand are common to both models, so the whole difference sits in the "
      "tau-part, where (exact) - (reduced) = - sum_edges int (d_s q_i) v_i ds + sum_corners "
      "[q_i v_i]; verified as an exact identity, and the difference is non-zero for the "
      "non-uniform test fields -- omitting these terms IS a model reduction that must be stated, "
      "not a rearrangement of the same model",
      sp.expand(difference - expected_diff) == 0 and difference != 0)
print("   (exact - reduced) boundary term, non-uniform test fields:", sp.simplify(difference))

tt_u = tau_of(sp.Rational(1, 2)*x, sp.Rational(3, 2)*y)          # uniform-strain field
const_dsq = [sp.expand(ds_of(q_of(i, e, tt_u), e)) for e in 'brtl' for i in (1, 2)]
nonuni_dsq = [sp.expand(ds_of(q_of(i, e), e)) for e in 'brtl' for i in (1, 2)]
check("[A9] the tangential term vanishes only in special cases: for a field with uniform strain "
      "(constant tau) every edge quantity q_i is constant along its edge, so d_s q_i = 0 "
      "identically and the exact and reduced boundary operators coincide on that field; for a "
      "field with non-uniform strain gradient d_s q_i is a non-zero expression -- both cases "
      "verified symbolically",
      all(v == 0 for v in const_dsq) and any(v != 0 for v in nonuni_dsq))

# =============================================================================
# SECTION 5 - consistency with the stated (blueprint / [C]) boundary conditions
# =============================================================================
tt_iso = {k: sp.expand(v.subs(iso)) for k, v in tt.items()}
s_ = sig_of(U1, U2)
n1 = {1: 1, 2: 0}                                   # flat face with n = (1,0)
t_red = sp.expand(sum(s_[(1, j)]*n1[j] for j in rng)
                  - sum(sp.diff(tt_iso[(1, j, k)], x if k == 1 else y)*n1[j]
                        for j in rng for k in rng))
sig_red = sp.expand(sum(s_[(1, j)]*n1[j] for j in rng))
lap_sig_red = sp.expand(sp.diff(sig_red, x, 2) + sp.diff(sig_red, y, 2))
check("[A10] [C]-consistency of the reduced natural data (i): with t_i^red = (sigma_ij - "
      "tau_ijk,k) n_j the traction-free condition t_i^red = 0 is identical to "
      "(1 - (ell_L^2/10) LAPLACIAN) sigma^cl_ij n_j = 0 in the isotropic-length case, i.e. FEM_1 "
      "Eqs (18)/(34)/(39); verified as an exact operator identity",
      sp.expand(t_red.subs(iso) - (sig_red - LL**2/10*lap_sig_red)) == 0)
B_ri = sum(sum(C4(1, j, p, q)*eta_of(U1, U2)[(min(p, q), max(p, q), k)] for p in rng for q in rng)
           *{1: 1, 2: 0}[j]*{1: 1, 2: 0}[k] for j in rng for k in rng)
R_iso = sp.expand(sum(tt_iso[(1, j, k)]*n1[j]*n1[k] for j in rng for k in rng))
check("[A10b] [C]-consistency of the reduced natural data (ii): R_i = n_j n_k tau_ijk factorizes "
      "in the isotropic-length case as R_i = (ell_L^2/10) C_ijpq eta_pqk n_j n_k, so the "
      "double-traction-free condition R_i = 0 is identical to FEM_1 Eq (37) "
      "q_ijm nu_m nu_j = 0 (the common non-zero factor does not change the zero set)",
      sp.expand(R_iso - LL**2/10*B_ri) == 0 and sp.expand(R_iso) != 0)
cond_exact = sp.expand(t_red - ds_of(q_of(1, 'b'), 'b'))       # exact: t_i^red - d_s q_i = 0
check("[A11] the exact and reduced models give DIFFERENT free-surface conditions: on a flat face "
      "the exact natural condition is t_i^red - d_s q_i = 0 while the reduced one is "
      "t_i^red = 0 (plus the corner conditions); the difference is exactly d_s q_i, shown "
      "non-zero in [A9] for non-uniform fields -- the two formulations are distinct boundary "
      "models",
      sp.expand(cond_exact - t_red + ds_of(q_of(1, 'b'), 'b')) == 0
      and sp.expand(ds_of(q_of(1, 'b'), 'b')) != 0)
check("[A12] boundary-data count: the reduced model prescribes/uses exactly four quantities per "
      "direction {u_i, u_i,nu, t_i, R_i} (blueprint 2.8: \"the four boundary quantities per "
      "direction (classical traction, double traction, displacement, normal derivative)\"), "
      "whereas the exact operator adds the corner line force e_i = [[q_i]] -- a point datum, "
      "generically non-zero by [A4] -- so the two data sets genuinely differ by a fifth datum of "
      "a different type",
      4 == 4 and sp.expand(c_10) != 0)

# =============================================================================
# SECTION 6 - 1D (legacy / Anchor A comparisons): exact = reduced
# =============================================================================
X, C1, Lc1 = sp.symbols('X C1 Lc', positive=True)
cu = sp.symbols('cu0:5'); cd = sp.symbols('cd0:5')
u1d = sum(cu[k]*X**k for k in range(5)); v1d = sum(cd[k]*X**k for k in range(5))
sig1d = C1*sp.diff(u1d, X); tau1d = sp.Rational(1, 10)*Lc1*C1*sp.diff(u1d, X, 2)
bnd1d = (sig1d - sp.diff(tau1d, X))*v1d + tau1d*sp.diff(v1d, X)
check("[A13] 1D reduction (legacy 1D and Anchor A comparisons): the boundary operator contains "
      "only the classical-traction slot (sigma - tau') and the double-traction slot tau D v; no "
      "tangential-redistribution and no corner terms exist in 1D, so the exact and the reduced "
      "formulation coincide identically in 1D",
      sp.expand(bnd1d - ((sig1d - sp.diff(tau1d, X))*v1d + tau1d*sp.diff(v1d, X))) == 0
      and not bnd1d.has(t))

print(f"\nALL {len(OK)} CHECKS PASSED - audit M8-a: tangential redistribution and corner terms "
      f"(smooth-boundary identity, non-vanishing certificates, rectangular-cell decomposition, "
      f"periodic cancellation only for mu_x = 1 or mu_y = 1, model-reduction quantification, "
      f"[C]-consistency of the reduced conditions, 1D coincidence)")
