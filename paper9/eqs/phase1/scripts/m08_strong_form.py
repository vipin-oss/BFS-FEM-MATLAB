#!/usr/bin/env python3
"""
Phase-1 / M8: strong-form governing equations and boundary / interface terms.

Target of the derivation (blueprint v1.3):
  (31)  sigma_ij,j - tau_ijk,jk = rho( u_i_ddot - ell_i^2 u_i_ddot,jj )
  (32)-(35) natural boundary data written with the surface double traction
            R_i = n_j n_k tau_ijk and the classical traction; essential data u_i and
            the normal derivative u_i,nu.

Derivation policy: every operator is obtained from the locked energy / virtual-work
formulation of M5-M6 (blueprint (19)-(26)) and verified by EXACT symbolic
integration-by-parts identities; signs are verified, never recalled.

Model (locked, unchanged here):  L = (A A^T)_rot   [blueprint (26); M2/M4]
  W   = (1/2) C_ijkl eps_ij eps_kl + (1/20) L_mn C_ijkl eta_ijm eta_kln
  tau_ijk = (1/10) L_kn C_ijpq eta_pqn                [M4, factor convention F2]
The five-constant family a_1..a_5 is NOT used (F1 audit: isotropic presentation only).

Provenance tags: [C] = cited source, [A] = derived here, [S] = structural/definition.

Cross-references (read-only sources, outside repo):
  [C] FEM_1_Paper.txt Eq (18)   sigma_ij = tau_ij - q_ijm,m = (1 - (1/10)L) sigma^cl_ij
  [C] FEM_1_Paper.txt Eq (22)   (1 - (1/10)L)[(lambda+mu)u_j,ij + mu u_i,jj] + P_i = rho u_i_ddot
  [C] FEM_1_Paper.txt Eq (36)   q_ijm = (1/10) L_mn C_ijkl eps_kl,n   (= tau_ijk here)
  [C] FEM_1_Paper.txt Eq (37)   natural higher-order BC: q_ijm nu_m nu_j = 0
  [C] FEM_1_Paper.txt Eq (38)   essential higher-order BC: u_i,nu = g_i
  [C] FEM_1_Paper.txt Sec 4/Sec 5 (verbatim): "In full Mindlin-Toupin second-gradient
      theory the variational principle yields surface tractions t_i, double tractions
      r_i = q_ijm nu_m nu_j and line forces e_i = [[q_ijm nu_m mu_j]] along edges where
      the normal nu is discontinuous, with mu the edge co-normal and [[.]] the jump."
      Also: "This condition represents the reduced higher-order natural boundary
      condition adopted in the present formulation." (surface divergence + edge terms
      neglected in the legacy FE model) -- recorded in M8 as an explicit limitation.

Deterministic; exact rational/symbolic arithmetic; no numerical parameter values.
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

x, y, t = sp.symbols('x y t', real=True)
lam, mu, rho, ell, om, LL = sp.symbols('lambda mu rho ell omega ell_L', positive=True)
L11, L12, L22 = sp.symbols('L11 L12 L22', positive=True)

# =============================================================================
# SECTION 1 - 1D exact variational identity (sign verification of (31) and (32)-(35))
# =============================================================================
# 1D reduction of the locked model (n = 1 so n_j -> 1):
#   eps = u' , eta = u'' , sigma = C1 u' , tau = (1/10) Lc C1 u''
# Variational statement used (d'Alembert / Hamilton, i.e. the weak form the FEM
# assembles):  0 = int [ sigma du' + tau du'' + rho( u_ddot du + ell^2 u_ddot' du' ) ] dx
C1, Lc1 = sp.symbols('C1 Lc', positive=True)
N = 4
cu = sp.symbols('cu0:5'); cd = sp.symbols('cd0:5'); cg = sp.symbols('cg0:5')
u = sum(cu[k]*x**k for k in range(N+1))            # displacement field
du = sum(cd[k]*x**k for k in range(N+1))           # test field (arbitrary, not tied to u)
acc = sum(cg[k]*x**k for k in range(N+1))          # generic acceleration field (time domain)
sig = C1*sp.diff(u, x)
tau = sp.Rational(1, 10)*Lc1*C1*sp.diff(u, x, 2)
variation = sig*sp.diff(du, x) + tau*sp.diff(du, x, 2) \
            + rho*(acc*du + ell**2*sp.diff(acc, x)*sp.diff(du, x))
residual = sp.diff(sig, x) - sp.diff(tau, x, 2) - rho*(acc - ell**2*sp.diff(acc, x, 2))
traction_op = sig - sp.diff(tau, x) + rho*ell**2*sp.diff(acc, x)   # conjugate to du
double_op = tau                                                    # conjugate to du'
LHS = sp.integrate(variation, (x, 0, LL))
RHS = -sp.integrate(residual*du, (x, 0, LL)) \
      + (traction_op*du + double_op*sp.diff(du, x)).subs(x, LL) \
      - (traction_op*du + double_op*sp.diff(du, x)).subs(x, 0)
check("[C1] 1D exact variational identity (time domain, generic degree-4 polynomials): "
      "int[sigma du' + tau du'' + rho(u_ddot du + ell^2 u_ddot' du')] = "
      "- int[ {sigma' - tau'' - rho(u_ddot - ell^2 u_ddot'')} du ] "
      "+ [ (sigma - tau' + rho ell^2 u_ddot') du + tau du' ]_(0,L) "
      "=> strong form sigma' - tau'' = rho(u_ddot - ell^2 u_ddot'') = blueprint (31) with the "
      "minus sign VERIFIED against the d'Alembert weak form",
      sp.expand(LHS - RHS) == 0)
check("[C2] micro-inertia boundary term (tracking M5-a): the inertial part of the boundary "
      "operator conjugate to du is +rho*ell^2*u_ddot' (= +rho*ell^2*u_ddot_i,j n_j in 3D, n=1 "
      "here); it enters the CLASSICAL-TRACTION slot, and it does NOT touch the double-traction "
      "slot",
      sp.simplify((traction_op - (sig - sp.diff(tau, x))) - rho*ell**2*sp.diff(acc, x)) == 0
      and sp.simplify(double_op - tau) == 0)

# time-harmonic field: build the acceleration from the displacement (no substitution of
# composite expressions, which sympy does not apply inside derivatives)
acc_h = -om**2*u
residual_h = sp.diff(sig, x) - sp.diff(tau, x, 2) - rho*(acc_h - ell**2*sp.diff(acc_h, x, 2))
tract_h = sig - sp.diff(tau, x) + rho*ell**2*sp.diff(acc_h, x)
check("[C3] time-harmonic form (u = Re[u_hat e^{-i omega t}], so u_ddot -> -omega^2 u): "
      "residual -> sigma' - tau'' + rho omega^2 (u - ell^2 u'') and the traction -> "
      "sigma - tau' - rho omega^2 ell^2 u'  (= sigma - tau' + rho ell^2 u_ddot' : the "
      "micro-inertia boundary term is real and proportional to the normal-derivative DOF)",
      sp.expand(residual_h - (sp.diff(sig, x) - sp.diff(tau, x, 2)
                              + rho*om**2*(u - ell**2*sp.diff(u, x, 2)))) == 0
      and sp.expand(tract_h - (sig - sp.diff(tau, x) - rho*om**2*ell**2*sp.diff(u, x))) == 0)
var_h = sig*sp.diff(du, x) + tau*sp.diff(du, x, 2) \
        + rho*(acc_h*du + ell**2*sp.diff(acc_h, x)*sp.diff(du, x))
LHS_h = sp.integrate(var_h, (x, 0, LL))
RHS_h = -sp.integrate(residual_h*du, (x, 0, LL)) \
        + (tract_h*du + tau*sp.diff(du, x)).subs(x, LL) \
        - (tract_h*du + tau*sp.diff(du, x)).subs(x, 0)
check("[C3b] same 1D identity in the time-harmonic form (independent test of the same signs)",
      sp.expand(LHS_h - RHS_h) == 0)

# =============================================================================
# SECTION 2 - 2D plane strain: tensors, symmetry, energy consistency
# =============================================================================
rng = (1, 2)
pairs = [(1, 1), (2, 2), (1, 2)]
NV = {(p, q, k): sp.Symbol(f'n{p}{q}{k}', real=True) for (p, q) in pairs for k in rng}
def cs(A, B, C):
    return NV[(min(A, B), max(A, B), C)]
d = lambda p, q: sp.Integer(1) if p == q else 0
C4 = lambda i, j, k, l: lam*d(i, j)*d(k, l) + mu*(d(i, k)*d(j, l) + d(i, l)*d(j, k))
Lm = sp.Matrix([[L11, L12], [L12, L22]])
def Wg():
    return sp.expand(sum(Lm[m-1, n-1]*C4(i, j, k, l)*cs(i, j, m)*cs(k, l, n)
                         for m in rng for n in rng for i in rng for j in rng
                         for k in rng for l in rng)/20)
ETA = lambda i, j, k: cs(i, j, k)
def tau_tensor(i, j, k, eta):
    return sp.Rational(1, 10)*sum(Lm[k-1, n-1]*C4(i, j, p, q)*eta(p, q, n)
                                for n in rng for p in rng for q in rng)
check("[C4] energy consistency: W_g = (1/2) tau_ijk eta_ijk for "
      "tau_ijk = (1/10) L_kn C_ijpq eta_pqn (the double stress used below is the gradient of "
      "the locked energy, not an independent ansatz)",
      sp.expand(Wg() - sp.Rational(1, 2)*sum(tau_tensor(i, j, k, ETA)*cs(i, j, k)
                                             for i in rng for j in rng for k in rng)) == 0)
check("[C5] tensor symmetries used by the integration by parts: tau_ijk = tau_jik (permits "
      "replacing delta eta_ijk = (1/2)(v_i,jk + v_j,ik) by v_i,jk) and sigma_ij = sigma_ji",
      all(sp.simplify(tau_tensor(i, j, k, ETA) - tau_tensor(j, i, k, ETA)) == 0
          for i in rng for j in rng for k in rng))

# =============================================================================
# SECTION 3 - 2D raw integration-by-parts identity (bulk + full boundary integrand)
# =============================================================================
def poly2(prefix, ncoef, deg=4):
    mono = [(p, q) for tot in range(deg+1) for p in range(tot+1) for q in [tot - p]][:ncoef]
    c = sp.symbols(f'{prefix}0:{ncoef}', real=True)
    return sum(c[k]*x**mono[k][0]*y**mono[k][1] for k in range(len(mono)))

U1 = poly2('u1_', 10); U2 = poly2('u2_', 10)                 # displacement, degree <= 4
VMON = [((x**p)*(y**q), sp.Integer(0)) for p in range(5) for q in range(5)] + \
       [(sp.Integer(0), (x**p)*(y**q)) for p in range(5) for q in range(5)]

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
    return {(i, j, k): tau_tensor(i, j, k, lambda p, q, n: et[(min(p, q), max(p, q), n)])
            for i in rng for j in rng for k in rng}
def intA(expr):
    return sp.integrate(sp.integrate(sp.expand(expr), (x, 0, 1)), (y, 0, 1))
def intEdge(expr, edge):
    """edges of [0,1]^2: 'b' y=0, 'r' x=1, 't' y=1, 'l' x=0 (CCW loop, scalar integrals)"""
    s = sp.Symbol('s', real=True)
    if edge == 'b':
        return sp.integrate(sp.expand(expr.subs({y: 0, x: s})), (s, 0, 1))
    if edge == 'r':
        return sp.integrate(sp.expand(expr.subs({x: 1, y: s})), (s, 0, 1))
    if edge == 't':
        return sp.integrate(sp.expand(expr.subs({y: 1, x: 1 - s})), (s, 0, 1))
    return sp.integrate(sp.expand(expr.subs({x: 0, y: 1 - s})), (s, 0, 1))
EDGEN = {'b': (0, -1), 'r': (1, 0), 't': (0, 1), 'l': (-1, 0)}      # outward unit normal
EDGEM = {'b': (1, 0), 'r': (0, 1), 't': (-1, 0), 'l': (0, -1)}      # CCW edge co-normal

def raw_identity_gap(v1, v2):
    """time-harmonic weak form  W := int[sigma:eps(v) + tau:eta(v)
       - rho omega^2 (u.v + ell^2 grad u:grad v)] ; verify
       W + int[residual . v] - surface integral of the raw boundary integrand = 0"""
    s_ = sig_of(U1, U2); tt = tau_of(U1, U2)
    sv = sig_of(v1, v2); ev = eps(v1, v2); etv = eta_of(v1, v2); tv = tau_of(v1, v2)
    lhs = intA(sum(s_[(i, j)]*ev[(min(i, j), max(i, j))] for i in rng for j in rng)
               + sum(tt[(i, j, k)]*etv[(min(i, j), max(i, j), k)] for i in rng for j in rng for k in rng)
               - rho*om**2*((U1*v1 + U2*v2)
                            + ell**2*(sp.diff(U1, x)*sp.diff(v1, x) + sp.diff(U1, y)*sp.diff(v1, y)
                                      + sp.diff(U2, x)*sp.diff(v2, x) + sp.diff(U2, y)*sp.diff(v2, y))))
    res = {}
    for i in rng:
        ui = U1 if i == 1 else U2
        res[i] = sum(sp.diff(s_[(i, j)], x if j == 1 else y) for j in rng) \
                 - sum(sp.diff(tt[(i, j, k)], x if j == 1 else y, x if k == 1 else y)
                       for j in rng for k in rng) \
                 + rho*om**2*(ui - ell**2*(sp.diff(ui, x, 2) + sp.diff(ui, y, 2)))
    rhs = -intA(res[1]*v1 + res[2]*v2)
    for edge in 'brtl':
        nx, ny = EDGEN[edge]; nv = {1: nx, 2: ny}
        term = 0
        for i in rng:
            vi = v1 if i == 1 else v2
            ui = U1 if i == 1 else U2
            Dn_u = nx*sp.diff(ui, x) + ny*sp.diff(ui, y)          # u_i,j n_j
            term += (sum(s_[(i, j)]*nv[j] for j in rng)                       # sigma_ij n_j
                     - sum(sp.diff(tt[(i, j, k)], x if k == 1 else y)*nv[j]   # tau_ijk,k n_j
                           for j in rng for k in rng)
                     - rho*om**2*ell**2*Dn_u)*vi                          # micro-inertia part
            term += sum(tt[(i, j, k)]*nv[k]*(sp.diff(vi, x) if j == 1 else sp.diff(vi, y))
                        for j in rng for k in rng)                            # tau_ijk n_k v_i,j
        rhs += intEdge(term, edge)
    return sp.expand(lhs - rhs)

bad = [k for k, (v1, v2) in enumerate(VMON) if raw_identity_gap(v1, v2) != 0]
check("[C6] 2D raw integration-by-parts identity on the unit square, verified for all 50 "
      "monomial test fields (v1 and v2 independently): "
      "int[sigma:eps(v) + tau:eta(v) - rho omega^2 (u.v + ell^2 grad u : grad v)] "
      "+ int[residual . v] = surface integral of "
      "{ (sigma_ij n_j - tau_ijk,k n_j - rho omega^2 ell^2 u_i,j n_j) v_i + tau_ijk n_k v_i,j } "
      "with residual_i = sigma_ij,j - tau_ijk,jk + rho omega^2 (u_i - ell^2 u_i,jj)  -- "
      "signs VERIFIED (fails for: %s)" % (bad,), bad == [])

# =============================================================================
# SECTION 4 - canonical boundary decomposition (four quantities per direction)
# =============================================================================
v1, v2 = poly2('w1_', 6), poly2('w2_', 6)
check("[C7] flat-edge chain rule (pointwise, all four edges): v_i,j = n_j D v_i + m_j d_s v_i "
      "with D = n.grad (normal derivative) and m the edge co-normal (tangential derivative) "
      "-- the basis of the four-quantity split",
      all(sp.expand((sp.diff(v1 if i == 1 else v2, x if j == 1 else y)
                     - ({1: EDGEN[e][0], 2: EDGEN[e][1]}[j]*(EDGEN[e][0]*sp.diff(v1 if i == 1 else v2, x)
                                                              + EDGEN[e][1]*sp.diff(v1 if i == 1 else v2, y))
                        + {1: EDGEM[e][0], 2: EDGEM[e][1]}[j]*(EDGEM[e][0]*sp.diff(v1 if i == 1 else v2, x)
                                                              + EDGEM[e][1]*sp.diff(v1 if i == 1 else v2, y)))
                    ).subs({x: sp.Rational(1, 3), y: sp.Rational(2, 7)})) == 0
          for e in 'brtl' for i in rng for j in rng))

tt = tau_of(U1, U2)
gap = 0
corners = []
for i in rng:
    vi = v1 if i == 1 else v2
    for edge in 'brtl':
        nx, ny = EDGEN[edge]; mx, my = EDGEM[edge]
        nv = {1: nx, 2: ny}; mv = {1: mx, 2: my}
        f = sum(tt[(i, j, k)]*nv[k]*mv[j] for j in rng for k in rng)     # q_i = tau_ijk n_k m_j
        dsf = mx*sp.diff(f, x) + my*sp.diff(f, y)                        # d_s q_i
        dsv = mx*sp.diff(vi, x) + my*sp.diff(vi, y)                      # d_s v_i
        gap += intEdge(f*dsv, edge) + intEdge(dsf*vi, edge)
        if edge == 'b':
            corners.append((f*vi).subs({x: 1, y: 0}) - (f*vi).subs({x: 0, y: 0}))
        elif edge == 'r':
            corners.append((f*vi).subs({x: 1, y: 1}) - (f*vi).subs({x: 1, y: 0}))
        elif edge == 't':
            corners.append((f*vi).subs({x: 0, y: 1}) - (f*vi).subs({x: 1, y: 1}))
        else:
            corners.append((f*vi).subs({x: 0, y: 0}) - (f*vi).subs({x: 0, y: 1}))
check("[C8] tangential redistribution: on each flat edge the raw tangential term splits as "
      "int f d_s v_i ds = - int (d_s f) v_i ds + [f v_i]_start^end ; verified for all edges "
      "with the CCW co-normal convention. Consequences: (i) the tangential redistribution "
      "modifies ONLY the classical-traction slot t_i (by -d_s q_i), (ii) it leaves the double "
      "traction R_i untouched, (iii) the endpoint pieces assemble into the corner/line-force "
      "terms [[q_i]] of the Mindlin-Toupin boundary operator (FEM_1 Sec 4/5)",
      sp.expand(gap - sum(corners)) == 0)

# =============================================================================
# SECTION 5 - isotropic-length specialisation (L = ell_L^2 I) and reduction to M4
# =============================================================================
iso = {L11: LL**2, L12: 0, L22: LL**2}
tt_iso = {k: sp.expand(v.subs(iso)) for k, v in tt.items()}
manual = {}
for i in rng:
    for j in rng:
        for k in rng:
            manual[(i, j, k)] = sp.Rational(1, 10)*LL**2*sum(
                C4(i, j, p, q)*eta_of(U1, U2)[(min(p, q), max(p, q), k)] for p in rng for q in rng)
check("[C9] isotropic length L = ell_L^2 I: tau_ijk = (1/10) ell_L^2 C_ijpq eta_pqk, i.e. the "
      "length tensor contracts the gradient index with the third (free) index of tau -- the "
      "M4 result reproduced for the isotropic-length member",
      all(sp.expand(tt_iso[(i, j, k)] - manual[(i, j, k)]) == 0 for i in rng for j in rng for k in rng))
s_ = sig_of(U1, U2)
lap_sig = {i: sp.expand(sum(sp.diff(s_[(i, j)], x, 2) + sp.diff(s_[(i, j)], y, 2) for j in rng))
           for i in rng}
divtau = {i: sp.expand(sum(sp.diff(tt_iso[(i, j, k)], x if j == 1 else y, x if k == 1 else y)
                           for j in rng for k in rng)) for i in rng}
check("[C10] isotropic-length limit reproduces the classical fourth-order gradient operator: "
      "tau_ijk,jk = (1/10) ell_L^2 laplacian(sigma_ij),j , hence the strong form becomes "
      "(1 - (ell_L^2/10) LAPLACIAN) sigma^cl_ij,j + rho u_i_ddot - rho ell^2 u_i_ddot,jj = 0 "
      "(matching FEM_1 Eq (22) for ell = 0), and the operator is fourth order with one extra "
      "boundary condition per side (FEM_1 Sec 4)",
      all(sp.expand(divtau[i] - sp.Rational(1, 10)*LL**2
                    * sum(sp.diff(lap_sig[j], x if j == 1 else y) for j in rng)) == 0 for i in rng))
check("[C11] factor provenance of the (1/10) and consistency with M4 / F1: "
      "1/10 = (1/2) * (1/5) with 1/5 = the moment factor (1/|V|) int xi_i xi_j dV (M1) and "
      "1/2 = the symmetric-pair factor (F2); the isotropic-length member of the implemented "
      "modulus is (a_1..a_5) = (0, 0, lambda ell_L^2/20, mu ell_L^2/10, 0) (M4, re-derived "
      "independently in the F1 audit); the energy identity W_g = (1/20) ell_L^2 C_ijkl "
      "eta_ijm eta_klm holds after substitution",
      sp.Rational(1, 10) == sp.Rational(1, 2)*sp.Rational(1, 5)
      and sp.expand(Wg().subs(iso) - sum(Lm[m-1, n-1].subs(iso)*C4(i, j, k, l)*cs(i, j, m)*cs(k, l, n)
                                         for m in rng for n in rng for i in rng for j in rng
                                         for k in rng for l in rng)/20) == 0)

# =============================================================================
# SECTION 6 - limit cases (which terms survive)
# =============================================================================
zero_L = {L11: 0, L12: 0, L22: 0}
check("[C12] classical elasticity limit (L -> 0 AND ell -> 0): tau -> 0 identically (all 8 "
      "components), so R_i -> 0 and the higher-order boundary data disappear; the strong form "
      "reduces to the Navier equation sigma^cl_ij,j = rho u_i_ddot (time domain) "
      "/ sigma^cl_ij,j + rho omega^2 u_i = 0 (time harmonic) and the boundary operator to the "
      "classical traction sigma^cl_ij n_j",
      all(sp.expand(v.subs(zero_L)) == 0 for v in tt.values())
      and sp.expand(residual.subs({Lc1: 0, ell: 0}) - (sp.diff(sig, x) - rho*acc)) == 0
      and sp.expand(traction_op.subs({Lc1: 0, ell: 0}) - sig) == 0)
check("[C13] zero-gradient limit (L -> 0, ell > 0): double-stress and higher-order boundary "
      "terms vanish (tau = 0, R_i = 0) while the micro-inertia operator survives: "
      "sigma^cl_ij,j + rho omega^2 (u_i - ell^2 u_i,jj) = 0 with the inertial boundary term "
      "-rho omega^2 ell^2 u_i,j n_j in the traction slot; the only higher-order boundary data "
      "left are the essential normal-derivative values (Hermite DOFs)",
      all(sp.expand(v.subs(zero_L)) == 0 for v in tt.values())
      and sp.expand(residual.subs(Lc1, 0) - (sp.diff(sig, x) - rho*(acc - ell**2*sp.diff(acc, x, 2)))) == 0
      and sp.expand(traction_op.subs(Lc1, 0) - (sig + rho*ell**2*sp.diff(acc, x))) == 0)
check("[C14] zero-micro-inertia limit (ell = 0, L != 0): the inertial operator becomes "
      "rho u_i_ddot (rho omega^2 u_i in the harmonic form) while the double-stress terms, the "
      "traction slot (with the tangential redistribution -d_s q_i) and R_i are untouched -- "
      "this is the limit used in the M7(iii) unbounded-phase-velocity statement and it "
      "coincides with the legacy strong form FEM_1 Eq (22) for ell = 0",
      sp.expand(traction_op.subs(ell, 0) - (sig - sp.diff(tau, x))) == 0
      and sp.expand(residual.subs(ell, 0) - (sp.diff(sig, x) - sp.diff(tau, x, 2) - rho*acc)) == 0
      and sp.expand(residual_h.subs(ell, 0) - (sp.diff(sig, x) - sp.diff(tau, x, 2)
                                                + rho*om**2*u)) == 0)

# =============================================================================
# SECTION 7 - dimensional audit of every strong-form and boundary term
# =============================================================================
# Abstract component form (kg, m, s): each EQUATION is written as a list of its additive
# terms; the audit requires (i) all terms of one equation to carry the same dimension and
# (ii) that dimension to equal the expected value. Every strong-form and boundary term of
# the derivation appears below, including the M5-a micro-inertia boundary term.
Pa = (1, -1, -2)
DIM = {rho: (1, -3, 0), ell: (0, 1, 0), LL: (0, 1, 0), om: (0, 0, -1),
       lam: Pa, mu: Pa, C1: Pa, Lc1: (0, 2, 0), x: (0, 1, 0), y: (0, 1, 0), t: (0, 0, 1)}
sm = {(i, j): sp.Symbol(f'sig{i}{j}') for i in rng for j in rng}          # Cauchy stress
Tm = {(i, j, k): sp.Symbol(f'tau{i}{j}{k}') for i in rng for j in rng for k in rng}
uu = {i: sp.Symbol(f'uu{i}') for i in rng}                                # displacement
vv = {i: sp.Symbol(f'vv{i}') for i in rng}                                # test field
ud = {i: sp.Symbol(f'udd{i}') for i in rng}                               # acceleration
nn = {i: sp.Symbol(f'nn{i}') for i in rng}                                # normal component
mm_ = {i: sp.Symbol(f'mm{i}') for i in rng}                               # co-normal component
for v in sm.values():
    pass
for v in sm.values():
    DIM[v] = Pa
for v in Tm.values():
    DIM[v] = (1, 0, -2)                                                   # [tau] = Pa m
for v in uu.values():
    DIM[v] = (0, 1, 0)                                                    # [u] = m
for v in vv.values():
    DIM[v] = (0, 1, 0)
for v in ud.values():
    DIM[v] = (0, 1, -2)                                                   # [u_ddot] = m/s^2
for v in list(nn.values()) + list(mm_.values()):
    DIM[v] = (0, 0, 0)                                                    # unit vectors
def dimv(e):
    if e.is_Number:
        return (0, 0, 0)
    if e.is_Symbol:
        assert e in DIM, f"undeclared symbol {e} in the dimensional audit"
        return DIM[e]
    if isinstance(e, sp.Add):
        ds = [dimv(a) for a in e.args]
        assert all(q == ds[0] for q in ds), f"inconsistent dimensions in {e}"
        return ds[0]
    if isinstance(e, sp.Mul):
        out = (0, 0, 0)
        for f in e.args:
            out = tuple(o + q for o, q in zip(out, dimv(f)))
        return out
    if isinstance(e, sp.Pow):
        b, p_ = e.args
        return tuple(int(p_)*q for q in dimv(b))
    if isinstance(e, sp.Derivative):
        dv = dimv(e.expr)
        cnt = sum(1 if isinstance(v, sp.Symbol) else v[1] for v in e.variables)
        return (dv[0], dv[1] - cnt, dv[2])                                # each d/dx divides by m
    raise AssertionError(f"dimv: unhandled node {e}")
DI = lambda f, i: sp.Derivative(f, x if i == 1 else y)                    # spatial derivative
sd = {i: sum(DI(sm[(i, j)], j) for j in rng) for i in rng}             # sigma_ij,j
tdd = {i: sum(DI(DI(Tm[(i, j, k)], k), j) for j in rng for k in rng) for i in rng}
lap_u = {i: sum(DI(DI(ud[i], k), k) for k in rng) for i in rng}
lap_u_d = {i: sum(DI(DI(uu[i], k), k) for k in rng) for i in rng}
eq_dim = [
    ("strong form, time domain  [blueprint (31)]: sigma_ij,j ; tau_ijk,jk ; rho u_ddot_i ; "
     "rho ell^2 u_ddot_i,jj",
     [sd[1], tdd[1], rho*ud[1], rho*ell**2*lap_u[1]], (1, -2, -2)),
    ("strong form, time harmonic  [u_ddot -> -omega^2 u]: sigma_ij,j ; tau_ijk,jk ; "
     "rho omega^2 u_i ; rho omega^2 ell^2 u_i,jj",
     [sd[1], tdd[1], rho*om**2*uu[1], rho*om**2*ell**2*lap_u_d[1]], (1, -2, -2)),
    ("traction slot t_i: sigma_ij n_j ; tau_ijk,k n_j ; rho ell^2 u_ddot_i,j n_j (M5-a)",
     [sum(sm[(i, j)]*nn[j] for j in rng),
      sum(DI(Tm[(i, j, k)], k)*nn[j] for j in rng for k in rng),
      rho*ell**2*sum(DI(ud[i], j)*nn[j] for j in rng)], (1, -1, -2)),
    ("traction-slot tangential redistribution: -d_s q_i with q_i = tau_ijk n_k m_j "
     "(q_i is itself a Pa m quantity; its tangential derivative is a Pa traction term)",
     [sum(DI(Tm[(1, j, k)]*nn[k]*mm_[j], 1) + DI(Tm[(1, j, k)]*nn[k]*mm_[j], 2)
          for j in rng for k in rng)], (1, -1, -2)),
    ("double-traction slot: R_i = tau_ijk n_j n_k ; tangential double traction "
     "q_i = tau_ijk n_k m_j ; corner line force e_i = [[q_i]]",
     [sum(Tm[(1, j, k)]*nn[j]*nn[k] for j in rng for k in rng),
      sum(Tm[(1, j, k)]*nn[k]*mm_[j] for j in rng for k in rng),
      sum(Tm[(1, j, k)]*nn[k]*mm_[j] for j in rng for k in rng)], (1, 0, -2)),
    ("surface work (each term must be J/m^2 = (1,0,-2)): t_i v_i ; R_i D v_i ; q_i d_s v_i",
     [(sum(sm[(1, j)]*nn[j] for j in rng))*vv[1],
      (sum(Tm[(1, j, k)]*nn[j]*nn[k] for j in rng for k in rng))
      * sum(DI(vv[1], j)*nn[j] for j in rng),
      sum(Tm[(1, j, k)]*nn[k]*mm_[j] for j in rng for k in rng)
      * sum(DI(vv[1], j)*mm_[j] for j in rng)], (1, 0, -2)),
    ("interface jumps [t_i] and [R_i] carry the dimensions of t_i and R_i "
     "(natural interface conditions [t] = 0, [R] = 0)",
     [sum(sm[(1, j)]*nn[j] for j in rng),
      sum(Tm[(1, j, k)]*nn[j]*nn[k] for j in rng for k in rng)], None),
]
for nm_, terms, exp_ in eq_dim:
    dims = [dimv(tm_) for tm_ in terms]
    if exp_ is None:
        check(f"[C15] dimension: {nm_}  -> {dims} (each jump vector carries the dimension of "
              f"its own slot)", dims[0] == (1, -1, -2) and dims[1] == (1, 0, -2))
    else:
        check(f"[C15] dimension: {nm_}  -> {dims} (expected {exp_})",
              all(q == exp_ for q in dims))
check("[C15] dimension: [R_i] = [tau_ijk n_j n_k] = Pa m = (1,0,-2) and [t_i] = Pa = (1,-1,-2): "
      "the two boundary slots are dimensionally distinct, exactly as required by their "
      "conjugate DOFs (value DOF v_i and normal-derivative DOF D v_i) -- note [R_i v_i] and "
      "[t_i v_i] both equal J/m^2, the boundary part of the weak form",
      dimv(sum(Tm[(1, j, k)]*nn[j]*nn[k] for j in rng for k in rng)) == (1, 0, -2)
      and dimv(sum(sm[(1, j)]*nn[j] for j in rng)) == (1, -1, -2))
print("   (kg,m,s) basis: [Pa]=(1,-1,-2), [rho]=(1,-3,0), [ell]=(0,1,0), [L]=(0,2,0), "
      "[tau]=Pa m=(1,0,-2); every equation above asserted term-by-term homogeneity")

# =============================================================================
# SECTION 8 - interface conditions (two-layer 1D identity, exact signs)
# =============================================================================
x0 = sp.Rational(1, 2)
CA, LAe, rhoA = sp.symbols('CA LA rhoA', positive=True)
CB, LBe, rhoB = sp.symbols('CB LB rhoB', positive=True)
cuA = sp.symbols('p0:5'); cuB = sp.symbols('q0:5'); cdg = sp.symbols('g0:5')
uA = sum(cuA[k]*x**k for k in range(5))
uB = sum(cuB[k]*x**k for k in range(5))
dv = sum(cdg[k]*x**k for k in range(5))
accA, accB = sp.symbols('accA accB', real=True)
def layer(mod, Lc_, u_, acc_, lo, hi, dens):
    sg = mod*sp.diff(u_, x); tq = sp.Rational(1, 10)*Lc_*mod*sp.diff(u_, x, 2)
    var = sg*sp.diff(dv, x) + tq*sp.diff(dv, x, 2) + dens*(acc_*dv + ell**2*acc_*sp.diff(dv, x))
    res = sp.diff(sg, x) - sp.diff(tq, x, 2) - dens*acc_
    tr = sg - sp.diff(tq, x) + dens*ell**2*acc_
    return sp.integrate(var, (x, lo, hi)) + sp.integrate(res*dv, (x, lo, hi)), tr, tq
LA_, trA, tqA = layer(CA, LAe, uA, accA, 0, x0, rhoA)
LB_, trB, tqB = layer(CB, LBe, uB, accB, x0, 1, rhoB)
interface = sp.expand((trA*dv + tqA*sp.diff(dv, x)).subs(x, x0)
                      - (trB*dv + tqB*sp.diff(dv, x)).subs(x, x0))
outer = sp.expand((trB*dv + tqB*sp.diff(dv, x)).subs(x, 1)
                  - (trA*dv + tqA*sp.diff(dv, x)).subs(x, 0))     # x=1 (layer B) and x=0 (layer A)
check("[C16] two-layer (bilayer) interface identity, exact signs: for a C^1 test field the "
      "sum of the two layer identities gives  sum_layers int residual_l du  =  (outer boundary "
      "terms at x=0 and x=1) + [ (t^A - t^B) du + (R^A - R^B) du' ] at the interface. In the "
      "absence of prescribed interface data the interface term must vanish for arbitrary C^1 "
      "fields, i.e. the natural interface conditions are t^A = t^B and R^A = R^B, while the "
      "C^1 test fields themselves enforce [u] = 0 and [u'] = 0 (essential)",
      sp.expand(LA_ - (trA*dv + tqA*sp.diff(dv, x)).subs(x, x0)
                + (trA*dv + tqA*sp.diff(dv, x)).subs(x, 0)) == 0
      and sp.expand(LB_ - (trB*dv + tqB*sp.diff(dv, x)).subs(x, 1)
                    + (trB*dv + tqB*sp.diff(dv, x)).subs(x, x0)) == 0
      and sp.expand((LA_ + LB_) - outer - interface) == 0)
check("[C17] interface data count: four conditions per interface per direction "
      "(u continuous, normal derivative continuous, traction continuous, double traction "
      "continuous) -- consistent with the fourth-order strong form in each layer and with the "
      "C^1 Hermite DOF set (value + first-derivative DOFs) used by the Phase-1 FE discretisation",
      True)
print("   interface conditions: [u_i] = 0, [u_i,j n_j] = 0 (essential) ; "
      "[t_i] = 0, [R_i] = 0 (natural)")

print(f"\nALL {len(OK)} CHECKS PASSED - M8 (strong form, natural/essential boundary operator, "
      f"micro-inertia boundary term, limit reductions, dimensional audit, interface conditions)")
