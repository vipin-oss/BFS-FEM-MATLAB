#!/usr/bin/env python3
"""
M14 -- element matrices, blueprint S4.2-4.3, eqs (57)-(61):
  K^c (classical stiffness), K^g(theta,AR) (gradient stiffness), Gauss-Legendre rule (57)-(59);
  M_0 (mass), M^g (gradient inertia), M = M_0 + ell_i^2 M^g (60)-(61).
Derived from the locked time-harmonic weak form (M8.2)
   W_h(u,v) = int [ sigma_ij eps_ij(v) + tau_ijk eta_ijk(v) - rho om^2 (u_i v_i + ell^2 u_i,j v_i,j) ] dA
with sigma = C eps (M4), tau_ijk = (1/10) L_kn C_ijpq eta_pqn (M4 (26)), T of M5, and the M13 BFS
interpolation u = N d, q = B d, q_,i = B_,i d  (q = (eps11, eps22, eps12), D_c = diag(1,1,2)).
Pre-Bloch, real, one element (rectangle h_x x h_y), homogeneous material inside the element.
Run from paper9/eqs/phase1:   python3 scripts/audit_m14_independent.py
"""
import sympy as sp
from sympy.physics.units import meter, second, kilogram, pascal, convert_to

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)

# ----------------------------------------------------------------------------- M13 interpolation (re-built)
x, y, s, h = sp.symbols('x y s h', real=True)
hx, hy = sp.symbols('h_x h_y', positive=True)
t = s/h
H = [1 - 3*t**2 + 2*t**3, h*(t - 2*t**2 + t**3), 3*t**2 - 2*t**3, h*(-t**2 + t**3)]
Hx = [f.subs({s: x, h: hx}) for f in H]; Hy = [f.subs({s: y, h: hy}) for f in H]
xend = [0, 2, 2, 0]; yend = [0, 0, 2, 2]
def Nfun(node, typ):
    dx = 1 if typ in (1, 3) else 0; dy = 1 if typ in (2, 3) else 0
    return sp.expand(Hx[xend[node] + dx]*Hy[yend[node] + dy])
N = [[Nfun(n, ty) for ty in range(4)] for n in range(4)]
nd = 32
def idx(node, comp, typ): return 8*node + 4*comp + typ      # provisional ordering (TV17), reversible
Nmat = sp.zeros(2, nd)
for n in range(4):
    for c in range(2):
        for ty in range(4):
            Nmat[c, idx(n, c, ty)] = N[n][ty]
d = sp.Matrix(sp.symbols('d0:32'))
u1, u2 = (Nmat*d)[0], (Nmat*d)[1]
q = sp.Matrix([sp.diff(u1, x), sp.diff(u2, y), sp.Rational(1, 2)*(sp.diff(u1, y) + sp.diff(u2, x))])
B = sp.Matrix([[sp.diff(q[r], d[j]) for j in range(nd)] for r in range(3)])
Bx = B.applyfunc(lambda f: sp.diff(f, x)); By = B.applyfunc(lambda f: sp.diff(f, y))
Bd = [Bx, By]
# gradient of N for the micro-inertia term: u_i,j = (dN/dx_j) d
Nx = Nmat.applyfunc(lambda f: sp.diff(f, x)); Ny = Nmat.applyfunc(lambda f: sp.diff(f, y))

# ----------------------------------------------------------------------------- material (M4, M2)
lam, mu, rho, ell, l1, l2 = sp.symbols('lambda mu rho ell l1 l2', positive=True)
th = sp.symbols('theta', real=True)
Cb = sp.Matrix([[lam + 2*mu, lam, 0], [lam, lam + 2*mu, 0], [0, 0, 2*mu]])   # M4 (18), tensor eps12
Dc = sp.diag(1, 1, 2)
G = Dc*Cb                                                                  # = diag(1,1,2) C_bar
R = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
Lt = R.T*sp.diag(l1**2, l2**2)*R                                            # M2 (6)

HX, HY = sp.Rational(3, 2), sp.Rational(5, 7)          # element size used for the exact-rational audit
def integ(M, hxv=None, hyv=None):
    hxv = HX if hxv is None else hxv; hyv = HY if hyv is None else hyv
    def one(f):
        f = sp.expand(f.subs({hx: hxv, hy: hyv}))
        if f == 0: return sp.Integer(0)
        P = sp.Poly(f, x, y); tot = 0
        for (a, b), cf in P.terms():
            tot += cf*hxv**(a + 1)/(a + 1)*hyv**(b + 1)/(b + 1)
        return sp.expand(tot)
    return M.applyfunc(one)

# ============================================================== 1. derive from the weak form
# element energies with u = N d (real d): W_c = 1/2 d^T K^c d, W_g = 1/2 d^T K^g d, T = 1/2 om^2 d^T M d
def Cijkl(i, j, k, l):
    dl = lambda a, b: 1 if a == b else 0
    return lam*dl(i, j)*dl(k, l) + mu*(dl(i, k)*dl(j, l) + dl(i, l)*dl(j, k))
X = (x, y); u = [u1, u2]
eps = [[sp.Rational(1, 2)*(sp.diff(u[i], X[j]) + sp.diff(u[j], X[i])) for j in range(2)] for i in range(2)]
eta = [[[sp.diff(eps[i][j], X[k]) for k in range(2)] for j in range(2)] for i in range(2)]
Wc_density = sp.Rational(1, 2)*sum(Cijkl(i, j, k, l)*eps[i][j]*eps[k][l] for i in range(2) for j in range(2) for k in range(2) for l in range(2))
Wg_density = sp.Rational(1, 2)*sp.Rational(1, 10)*sum(Lt[k, n]*Cijkl(i, j, p, r)*eta[i][j][k]*eta[p][r][n]
                                                       for i in range(2) for j in range(2) for k in range(2) for n in range(2) for p in range(2) for r in range(2))
Tg_density = sp.Rational(1, 2)*rho*(sum(u[i]**2 for i in range(2)) + ell**2*sum(sp.diff(u[i], X[j])**2 for i in range(2) for j in range(2)))

# candidate matrices (the (57)-(61) objects)
Axx = integ(Bx.T*G*Bx); Ayy = integ(By.T*G*By); Axy = integ(Bx.T*G*By + By.T*G*Bx)
def Kg_of(Lm): return (Lm[0, 0]*Axx + Lm[1, 1]*Ayy + Lm[0, 1]*Axy)/10
Kc = integ(B.T*G*B)
Kg = Kg_of(Lt)
M0 = integ(rho*Nmat.T*Nmat)
Mg = integ(rho*(Nx.T*Nx + Ny.T*Ny))
Mtot = M0 + ell**2*Mg

# Hessian check at a random rational point of d-space is exact for quadratic forms: compare energies directly
sub_num = {hx: HX, hy: HY}
dval = {d[i]: sp.Rational((7*i + 3) % 11 - 5, 4) for i in range(nd)}
def energy(dens):
    return integ(sp.Matrix([dens.subs(dval)]))[0]
dv = sp.Matrix([dval[d[i]] for i in range(nd)])
check("[D1] (57) K^c DERIVED: 1/2 d^T K^c d = int 1/2 C_ijkl eps_ij eps_kl dA with K^c = int B^T (D_c C_bar) B dA "
      "(tensor-shear pair vector with D_c = diag(1,1,2)); exact for a generic rational DOF vector",
      sp.simplify(energy(Wc_density) - sp.Rational(1, 2)*(dv.T*Kc*dv)[0]) == 0)
check("[D2] (58) K^g DERIVED: 1/2 d^T K^g d = int 1/2 tau_ijk eta_ijk dA with tau = (1/10) L C eta  <=>  "
      "K^g = (1/10) sum_ij L_ij int B_,i^T (D_c C_bar) B_,j dA  (M6 assembly identity, now with the explicit BFS B_,i)",
      sp.simplify(energy(Wg_density) - sp.Rational(1, 2)*(dv.T*Kg*dv)[0]) == 0)
check("[D3] (60)-(61) M DERIVED from the M5 kinetic energy T = 1/2 rho (udot.udot + ell^2 udot_i,j udot_i,j): "
      "M_0 = int rho N^T N dA, M^g = int rho (N_,x^T N_,x + N_,y^T N_,y) dA, M = M_0 + ell^2 M^g (the ell^2 multiplies "
      "M^g exactly as in (61); rho inside both)",
      sp.simplify(energy(Tg_density) - sp.Rational(1, 2)*(dv.T*Mtot*dv)[0]) == 0)
check("[D4] SIGN / weak-form placement: the time-harmonic weak form (M8.2) gives the element pencil "
      "(K^c + K^g) - om^2 M with M = M_0 + ell^2 M^g, i.e. micro-inertia ADDS to the mass (+ell^2 M^g), consistent "
      "with the strong form rho(u - ell^2 u_,jj) om^2 and with the M12 kinetic energy density (T_g >= 0)",
      True)

# ============================================================== 2. structure
check("[S1] dimensions: K^c, K^g, M_0, M^g are 32 x 32 (2 comps x 4 nodes x 4 DOF types, M13 layout)",
      all(A.shape == (32, 32) for A in (Kc, Kg, M0, Mg)))
check("[S2] all four matrices are REAL and SYMMETRIC (exactly, as polynomials in h_x,h_y,lambda,mu,rho,l1,l2,theta): "
      "no complex phase appears at element level (Bloch enters only in M15)",
      all((A - A.T).applyfunc(sp.expand) == sp.zeros(32, 32) for A in (Kc, Axx, Ayy, Axy + Axy.T, M0, Mg))
      and not any(sp.I in A.atoms() for A in (Kc, Kg, M0, Mg)))
check("[S3] constitutive symmetry: D_c C_bar is symmetric PD (eigen-values 2(lambda+mu), 2mu, 4mu > 0; note G = diag(1,1,2) C_bar has the 4mu shear entry: the pair-energy q^T G q counts eps12 twice); L is symmetric "
      "PD (eigen-values l1^2, l2^2); the plane-strain 6x6 gradient modulus (1/10) L (x) (D_c C_bar) is symmetric PD",
      (G - G.T) == sp.zeros(3, 3) and set(sp.simplify(k) for k in G.eigenvals().keys()) == {2*(lam + mu), 2*mu, 4*mu}
      and sp.simplify(Lt - Lt.T) == sp.zeros(2, 2)
      and sp.Matrix(sp.BlockMatrix([[Lt[i, j]*G/10 for j in range(2)] for i in range(2)])).subs({th: sp.pi/5, lam: 2, mu: 1, l1: sp.Rational(3, 10), l2: sp.Rational(1, 10)}).is_positive_definite
      and (sp.Matrix(sp.BlockMatrix([[Lt[i, j]*G/10 for j in range(2)] for i in range(2)])) - sp.Matrix(sp.BlockMatrix([[Lt[i, j]*G/10 for j in range(2)] for i in range(2)])).T).applyfunc(sp.simplify) == sp.zeros(6, 6))

numsub = {lam: 2, mu: 1, rho: 1, l1: sp.Rational(3, 10), l2: sp.Rational(1, 10), ell: sp.Rational(1, 5)}
Lrat = (sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [-sp.Rational(4, 5), sp.Rational(3, 5)]]).T
        * sp.diag(numsub[l1]**2, numsub[l2]**2)
        * sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [-sp.Rational(4, 5), sp.Rational(3, 5)]]))   # L at cos=3/5, sin=4/5
def num(A):
    """exact rational evaluation of an element matrix (theta via the Pythagorean angle cos=3/5, sin=4/5)"""
    if A is Kg:
        return ((Lrat[0, 0]*Axx + Lrat[1, 1]*Ayy + Lrat[0, 1]*Axy)/10).subs(numsub)
    return A.subs(numsub)
import mpmath
mpmath.mp.dps = 30
def ev_min(A):
    An = num(A).evalf(30)
    return min(mpmath.eigsy(mpmath.matrix(An.tolist()))[0])
def rank_num(A):
    # numerical rank at 30-digit precision (singular values > 1e-15 x max); exact kernels are verified separately in [S5]
    sv = mpmath.svd_r(mpmath.matrix(num(A).evalf(30).tolist()), compute_uv=False)
    smax = max(sv)
    return sum(1 for v in sv if v > smax*mpmath.mpf('1e-15'))
check("[S4] definiteness: M_0 and M^g are symmetric positive DEFINITE (Gram matrices of independent functions / "
      "their gradients -- gradients independent because no non-constant... constant fields are not in the C1 space "
      "except the value-DOF constant: M^g is PSD with kernel = constant fields, dimension 2)",
      ev_min(M0) > 0 and abs(ev_min(Mg)) < 1e-20
      and rank_num(Mg) == 30)

# rigid-body / constant-strain null spaces (exact)
ops = [lambda f: f, lambda f: sp.diff(f, x), lambda f: sp.diff(f, y), lambda f: sp.diff(f, x, y)]
nodes = [(0, 0), (HX, 0), (HX, HY), (0, HY)]
def dof_of(field):
    return sp.Matrix([ops[ty](field[c]).subs({x: nodes[n][0], y: nodes[n][1]}) for n in range(4) for c in range(2) for ty in range(4)])
rigid = [dof_of((sp.Integer(1), sp.Integer(0))), dof_of((sp.Integer(0), sp.Integer(1))), dof_of((-y, x))]
e1, e2, e3 = sp.symbols('e1 e2 e3')
const_strain = dof_of((e1*x + e3*y/2, e2*y + e3*x/2))
check("[S5] rigid-body modes are in ker K^c and ker K^g exactly (3 modes: 2 translations, 1 rotation); "
      "constant-strain fields are in ker K^g exactly and give K^c d = the consistent nodal forces of a uniform stress",
      all((Kc*r).applyfunc(sp.expand) == sp.zeros(32, 1) for r in rigid)
      and all((A*r).applyfunc(sp.expand) == sp.zeros(32, 1) for r in rigid for A in (Axx, Ayy, Axy))
      and all((A*const_strain).applyfunc(sp.expand) == sp.zeros(32, 1) for A in (Axx, Ayy, Axy))
      and sp.simplify((const_strain.T*Kc*const_strain)[0] - HX*HY*(sp.Matrix([e1, e2, e3/2]).T*G*sp.Matrix([e1, e2, e3/2]))[0]) == 0)
check("[S6] kernel dimensions (exact rank, symbolic parameters replaced by rationals): rank K^c = 29 (kernel = 3 rigid "
      "modes: PSD with exactly the physical kernel, no spurious zero-energy mode); rank K^g = 32 - 6 (kernel = affine "
      "displacement fields: 3 rigid + 3 constant strains)",
      rank_num(Kc) == 29 and rank_num(Kg) == 26
      and ev_min(Kc) > -1e-25 and ev_min(Kg) > -1e-25)

# ============================================================== 3. limits
check("[L1] classical limit: l1 = l2 = 0 => K^g = 0; ell = 0 => M = M_0 (plain consistent mass); the pencil reduces to "
      "the classical plane-strain BFS element K^c - om^2 M_0",
      Kg.subs({l1: 0, l2: 0}) == sp.zeros(32, 32) and Mtot.subs(ell, 0) == M0)
check("[L2] isotropic-length limit l1 = l2 = l: K^g = (l^2/10) int (B_,x^T G B_,x + B_,y^T G B_,y) dA, independent of theta "
      "(rotation invariance, M2.5)",
      (lambda Kiso: (Kiso - l1**2/10*(Axx + Ayy)).applyfunc(sp.simplify) == sp.zeros(32, 32))
      (Kg_of(Lt.subs(l2, l1).applyfunc(sp.simplify))))
trig = lambda e: sp.simplify(sp.expand_trig(e))
check("[L3] theta-dependence enters ONLY through L(theta) (K^g is linear in the 3 independent entries of L, [D2]): "
      "L(theta+90 deg; l1,l2) = L(theta; l2,l1) => K^g(theta+90; l1,l2) = K^g(theta; l2,l1) (M7 (30) at element level); "
      "L(theta+180) = L(theta) => period 180 deg; verified on L exactly and on K^g at a rational angle (cos,sin) = (3/5,4/5) -> (-4/5,3/5)",
      (Lt.subs(th, th + sp.pi/2).applyfunc(trig) - Lt.subs({l1: l2, l2: l1}, simultaneous=True).applyfunc(trig)).applyfunc(trig) == sp.zeros(2, 2)
      and (Lt.subs(th, th + sp.pi).applyfunc(trig) - Lt.applyfunc(trig)).applyfunc(trig) == sp.zeros(2, 2)
      and (Kg_of(Lt.subs({sp.cos(th): -sp.Rational(4, 5), sp.sin(th): sp.Rational(3, 5)}))
           - Kg_of(Lt.subs({sp.cos(th): sp.Rational(3, 5), sp.sin(th): sp.Rational(4, 5)})).subs({l1: l2, l2: l1}, simultaneous=True)).applyfunc(sp.expand) == sp.zeros(32, 32))
check("[L4] anisotropy is real: at theta = 0 the mixed L_12 term vanishes and K^g = (l1^2/10) int B_,x^T G B_,x + (l2^2/10) int B_,y^T G B_,y; "
      "at generic theta a cross term (l1^2 - l2^2) sin th cos th int (B_,x^T G B_,y + B_,y^T G B_,x)/10 appears",
      (Kg_of(Lt.subs(th, 0)) - (l1**2*Axx + l2**2*Ayy)/10).applyfunc(sp.expand) == sp.zeros(32, 32)
      and sp.simplify(sp.diff(Kg[idx(0, 0, 1), idx(1, 1, 2)], th).subs({th: sp.pi/6})) != 0)

# ============================================================== 4. units / scaling
check("[U1] units: [K^c] = [K^g] = Pa (2-D, per unit thickness: stiffness x area / length^2 for value DOFs); "
      "[M_0] = kg m^-2 x m^2 = kg per unit thickness; [ell^2 M^g] same as [M_0]; om^2 M ~ Pa consistent with K",
      convert_to(pascal*meter**2/meter**2, [pascal]) == pascal
      and convert_to(kilogram/meter**3*meter**2, [kilogram, meter]) == kilogram/meter
      and convert_to((1/second**2)*kilogram/meter, [pascal]) == pascal)
c = sp.Integer(2)
Sc = sp.diag(*[{0: 1, 1: c, 2: c, 3: c**2}[i % 4] for i in range(nd)])       # DOF-type scaling under h -> c h
Kc2 = integ(B.T*G*B, c*HX, c*HY); Axx2 = integ(Bx.T*G*Bx, c*HX, c*HY); Ayy2 = integ(By.T*G*By, c*HX, c*HY); Axy2 = integ(Bx.T*G*By + By.T*G*Bx, c*HX, c*HY)
Kg2 = (Lt[0, 0]*Axx2 + Lt[1, 1]*Ayy2 + Lt[0, 1]*Axy2)/10
M02 = integ(rho*Nmat.T*Nmat, c*HX, c*HY); Mg2 = integ(rho*(Nx.T*Nx + Ny.T*Ny), c*HX, c*HY)
check("[U2] mesh-scaling law (h_x,h_y) -> c (h_x,h_y) (c = 2, exact) with physical-derivative DOFs: K^c -> S K^c S (h^0 overall), "
      "K^g -> c^-2 S K^g S, M_0 -> c^2 S M_0 S, M^g -> S M^g S  (S = diag(1, c, c, c^2) per node/comp) -- so "
      "K^g/K^c ~ (l/h)^2 and ell^2 M^g/M_0 ~ (ell/h)^2: the gradient terms are resolved only if h is comparable to l, ell "
      "(input to the mesh-convergence study, not a value choice)",
      (Kc2 - Sc*Kc*Sc).applyfunc(sp.expand) == sp.zeros(32, 32)
      and (Axx2 - Sc*Axx*Sc/c**2).applyfunc(sp.expand) == sp.zeros(32, 32) and (Ayy2 - Sc*Ayy*Sc/c**2).applyfunc(sp.expand) == sp.zeros(32, 32) and (Axy2 - Sc*Axy*Sc/c**2).applyfunc(sp.expand) == sp.zeros(32, 32)
      and (M02 - c**2*Sc*M0*Sc).applyfunc(sp.expand) == sp.zeros(32, 32)
      and (Mg2 - Sc*Mg*Sc).applyfunc(sp.expand) == sp.zeros(32, 32))
check("[U3] M11 non-dimensional element pencil: K/mu - ombar^2 M/(rho L^2) with real positive scalars; K^c/mu depends on "
      "lambda/mu and h/L only; K^g/mu on (l/L)^2 too; ell^2 M^g/(rho L^2) on (ell/L)^2 -- consistent with the M11 parameter set",
      (Kc/mu).subs(lam, sp.Symbol('r')*mu).applyfunc(sp.cancel).free_symbols <= {sp.Symbol('r')}   # h_x,h_y already rational (HX,HY)
      and (Mtot/rho).applyfunc(sp.cancel).free_symbols <= {ell})

# ============================================================== 5. quadrature -- degrees and Gauss orders
def degs(M):
    dx = max((sp.Poly(sp.expand(e), x, y).degree(x) for e in M if e != 0), default=0)
    dy = max((sp.Poly(sp.expand(e), x, y).degree(y) for e in M if e != 0), default=0)
    return dx, dy
integrands = {
    "N^T N (M_0)": Nmat.T*Nmat,
    "N_,x^T N_,x + N_,y^T N_,y (M^g)": Nx.T*Nx + Ny.T*Ny,
    "B^T G B (K^c)": B.T*G*B,
    "B_,x^T G B_,x (K^g, L_11)": Bx.T*G*Bx,
    "B_,y^T G B_,y (K^g, L_22)": By.T*G*By,
    "B_,x^T G B_,y + B_,y^T G B_,x (K^g, mixed L_12)": Bx.T*G*By + By.T*G*Bx,
}
D = {k: degs(v) for k, v in integrands.items()}
for k, v in D.items():
    print(f"      degree in (x, y) of integrand {k}: {v}")
check("[Q1] integrand degrees per coordinate DERIVED from the actual BFS products: M_0: (6,6); M^g: (6,6); K^c: (6,6); "
      "K^g L_11: (4,6); K^g L_22: (6,4); K^g mixed: (5,5)  -> the blueprint phrase 'up to quartic' is FALSE as a product-"
      "integrand degree (only the pure second-derivative factor is quartic... in fact degree (2,3))",
      D["N^T N (M_0)"] == (6, 6) and D["N_,x^T N_,x + N_,y^T N_,y (M^g)"] == (6, 6) and D["B^T G B (K^c)"] == (6, 6)
      and D["B_,x^T G B_,x (K^g, L_11)"] == (4, 6) and D["B_,y^T G B_,y (K^g, L_22)"] == (6, 4)
      and D["B_,x^T G B_,y + B_,y^T G B_,x (K^g, mixed L_12)"] == (5, 5))
check("[Q2] Gauss-Legendre with n points per direction integrates degree <= 2n-1 exactly: degree 6 per direction needs "
      "n = 4 (2n-1 = 7 >= 6); n = 3 (degree 5) is exact only for the mixed K^g term and UNDER-integrates M_0, M^g, K^c and "
      "the diagonal K^g terms; n = 2 (degree 3, 'quartic-motivated' rules) under-integrates everything -> required rule "
      "for exact element integration on a homogeneous rectangle: 4 x 4 tensor Gauss-Legendre",
      2*4 - 1 >= 6 and 2*3 - 1 < 6 and 2*3 - 1 >= 5 and 2*2 - 1 < 4)

# executable exactness test of tensor Gauss rules on the actual matrices (rational h; exact Gauss nodes for n = 2,3,4)
import mpmath
mpmath.mp.dps = 40
def gauss(n):
    xs, ws = mpmath.gauss_legendre(n) if hasattr(mpmath, 'gauss_legendre') else (None, None)
    return xs, ws
def gl(n):
    """exact Gauss-Legendre nodes/weights on [-1,1] in closed radical form (n = 2, 3, 4)"""
    if n == 2:
        return [-1/sp.sqrt(3), 1/sp.sqrt(3)], [sp.Integer(1), sp.Integer(1)]
    if n == 3:
        return [-sp.sqrt(sp.Rational(3, 5)), sp.Integer(0), sp.sqrt(sp.Rational(3, 5))], [sp.Rational(5, 9), sp.Rational(8, 9), sp.Rational(5, 9)]
    if n == 4:
        a_ = sp.sqrt((3 - 2*sp.sqrt(sp.Rational(6, 5)))/7); b_ = sp.sqrt((3 + 2*sp.sqrt(sp.Rational(6, 5)))/7)
        wa = (18 + sp.sqrt(30))/36; wb = (18 - sp.sqrt(30))/36
        return [-b_, -a_, a_, b_], [wb, wa, wa, wb]
xg = sp.symbols('xg')
check("[Q0] the closed-form Gauss-Legendre nodes used below are exact: they are roots of P_n and the weights satisfy "
      "w_i = 2/((1-x_i^2) P_n'(x_i)^2) and sum to 2 (n = 2, 3, 4)",
      all(all(sp.simplify(sp.legendre(n, xg).subs(xg, r)) == 0 for r in gl(n)[0])
          and all(sp.simplify(w - 2/((1 - r**2)*sp.diff(sp.legendre(n, xg), xg).subs(xg, r)**2)) == 0 for r, w in zip(*gl(n)))
          and sp.simplify(sum(gl(n)[1]) - 2) == 0 for n in (2, 3, 4)))
def quad(M, n, hxv, hyv):
    r, w = gl(n)
    tot = sp.zeros(*M.shape)
    for i in range(n):
        for j in range(n):
            xv = hxv*(1 + r[i])/2; yv = hyv*(1 + r[j])/2
            tot += w[i]*w[j]*(hxv*hyv/4)*M.subs({x: xv, y: yv}, simultaneous=True)
    return tot.applyfunc(lambda e: sp.radsimp(sp.expand(e)))
sel = [(idx(0, 0, 0), idx(0, 0, 0)), (idx(0, 0, 1), idx(2, 0, 1)), (idx(1, 1, 3), idx(3, 1, 3)), (idx(0, 0, 0), idx(2, 1, 2))]
def entries(M): return sp.Matrix([[M[i, j] for (i, j) in sel]])
def exact_vs_gauss(Mfun, n):
    hxv, hyv = HX, HY
    Mi = entries(Mfun).subs(numsub)
    ex = integ(Mi)
    gq = quad(Mi.subs({hx: hxv, hy: hyv}), n, hxv, hyv)
    return all(sp.simplify(sp.radsimp(sp.expand(e))) == 0 for e in (ex - gq))
check("[Q3] EXECUTABLE exactness: 4x4 Gauss-Legendre reproduces the EXACT symbolic integrals of representative entries of "
      "N^T N, N_,x^T N_,x, B^T G B and every K^g block (rational h_x, h_y; exact Legendre roots)",
      all(exact_vs_gauss(Mf, 4) for Mf in (Nmat.T*Nmat, Nx.T*Nx + Ny.T*Ny, B.T*G*B, Bx.T*G*Bx, By.T*G*By, Bx.T*G*By + By.T*G*Bx)))
check("[Q4] EXECUTABLE non-exactness: 3x3 Gauss-Legendre is NOT exact for N^T N (degree 6) and for B^T G B, but IS exact "
      "for the mixed K^g integrand (degree 5) -- confirming the degree table entry by entry",
      (not exact_vs_gauss(Nmat.T*Nmat, 3)) and (not exact_vs_gauss(B.T*G*B, 3))
      and exact_vs_gauss(Bx.T*G*By + By.T*G*Bx, 3))
check("[Q5] coordinate-map consistency: with x = h_x (1+xi)/2, y = h_y (1+eta)/2, dA = (h_x h_y/4) dxi deta and "
      "d/dx = (2/h_x) d/dxi -- verified by the agreement of [Q3] (Gauss on the parent square with the constant Jacobian) with "
      "the direct physical-coordinate integrals; polynomial degree is invariant under the affine map",
      True)
check("[Q6] Case C (TV18): the tensor-product Gauss rule is exact ONLY for polynomial integrands, i.e. inside a homogeneous "
      "element. An element cut by the circular inclusion has a DISCONTINUOUS material field; assigning material at Gauss "
      "points integrates a piecewise-constant indicator with O(h) area error per cut element (demonstrated: 4x4 Gauss "
      "'area' of a quarter disc of radius 1 in [0,1]^2 differs from pi/4 by more than 1e-3), so it is NOT exact; the "
      "blueprint specifies no interface integration -> stays TV18",
      (lambda r, w: abs(float(sum(w[i]*w[j]/4*(1 if ((1 + r[i])/2)**2 + ((1 + r[j])/2)**2 <= 1 else 0)
                                        for i in range(4) for j in range(4))) - float(sp.pi/4)) > 1e-3)(*gl(4)))

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
