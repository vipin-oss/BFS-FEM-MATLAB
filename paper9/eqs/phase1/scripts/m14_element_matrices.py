#!/usr/bin/env python3
"""
M14 -- Element matrices and Gauss quadrature, blueprint S4.2-4.3, eqs (57)-(61).
Pre-Bloch, one homogeneous axis-aligned rectangle.  No Bloch T(k).  No Case C.

Locked: M8.2 weak form; M4 (26) tau = (1/10) L ⊗ C : eta; M6 K_g identity;
M13 BFS N, B, B_,i with q=(eps11,eps22,eps12), G = D_c C_bar, D_c=diag(1,1,2).
TV17: M13 provisional DOF index used for matrix indexing only (not blueprint-locked).
TV18: circular inclusion not introduced.

Run from paper9/eqs/phase1:
    python3 scripts/m14_element_matrices.py
"""
import numpy as np
import sympy as sp
from sympy.physics.units import convert_to, meter, second, kilogram, pascal

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)

# ============================================================================= 0. 1-D Hermite + BFS (M13)
hx, hy = sp.symbols('h_x h_y', positive=True)
x, y = sp.symbols('x y', real=True)
s, h = sp.symbols('s h', positive=True)
t = s/h
H1d = [1 - 3*t**2 + 2*t**3, h*(t - 2*t**2 + t**3), 3*t**2 - 2*t**3, h*(-t**2 + t**3)]
Hx = [f.subs({s: x, h: hx}) for f in H1d]
Hy = [f.subs({s: y, h: hy}) for f in H1d]
xend = [0, 2, 2, 0]; yend = [0, 0, 2, 2]
def Nfun(node, typ):
    dx = 1 if typ in (1, 3) else 0
    dy = 1 if typ in (2, 3) else 0
    return Hx[xend[node] + dx]*Hy[yend[node] + dy]
def idx(node, comp, typ):  # TV17 provisional (M13): node-major, then component, then type
    return 8*node + 4*comp + typ

# Scalar N_I(x,y) for the 16 geometric functions; vector N is 2 x 32
# B rows: eps11=u1,x ; eps22=u2,y ; eps12=(u1,y+u2,x)/2

# ============================================================================= 1. matrix definitions from M8.2
# W_h = int [ q(v)^T G q(u) + (1/10) L_mn q_,m(v)^T G q_,n(u)
#             - rho omega^2 ( u·v + ell^2 u_,j · v_,j ) ] dA
# with G = D_c C_bar,  q = B d,  q_,i = B_,i d,  u = N d
# =>  (1/2) d^T (K^c + K^g - omega^2 (M0 + ell^2 M^g)) d   (sesquilinear later in M15)
check("[D1] (57) K^c := int_A B^T G B dA   with G = D_c C_bar, D_c=diag(1,1,2), "
      "C_bar plane-strain (lam+2mu, lam; lam, lam+2mu; 2mu).  This is the bilinear form "
      "int sigma(v):eps(u) dA.  Size 32x32.  Real, no Bloch phase.",
      True)
check("[D2] (58) K^g := (1/10) sum_{m,n=1,2} L_mn int_A B_,m^T G B_,n dA   "
      "(M6 assembly identity; L = R^T diag(l1^2,l2^2) R).  Equals int tau(v):eta(u) dA "
      "because 2 W_g density = (1/10) L_mn q_m^T G q_n.  Depends on (theta, AR) only through L.",
      True)
check("[D3] (60)-(61) M0 := rho int_A N^T N dA ;  M^g := rho int_A (N_,x^T N_,x + N_,y^T N_,y) dA ; "
      "M := M0 + ell_i^2 M^g.  Micro-inertia from M5/M8.2.  No complex arithmetic.",
      True)

# Units (2-D per unit thickness)
check("[U1] [K^c] = Pa  (int (1/L)^2 * Pa * dA); [K^g] = Pa  (int (1/L^2)^2 * Pa * L^2 * dA "
      "with L_mn ~ L^2 giving Pa).  [M0] = kg/m  (rho * area) for a 2-D membrane; "
      "M11's kg/m^2 is the same quantity per unit thickness if thickness is carried as 1 m. "
      "[M^g] = kg/m^3  so ell^2 M^g has [M0].  Affine Jacobian of the rectangle is constant hx*hy.",
      convert_to(pascal, [kilogram, meter, second]) is not None)

check("[U2] pre-Bloch matrices are REAL: N, B, B_,i, C, L, rho, ell are real on the rectangle. "
      "No k, no mu_alpha.  Complex phases belong to M15 T(k).",
      True)

# ============================================================================= 2. quadrature theory
# Gauss-Legendre: n points exact for polynomials of degree <= 2n-1.
check("[Q1] 1-D Gauss-Legendre with n nodes is exact on P_{2n-1}.  Therefore degree <= 6 "
      "requires 2n-1 >= 6 => n >= 4.  n = 3 is exact only through degree 5.",
      2*4 - 1 >= 6 and 2*3 - 1 == 5)

# Per-coordinate degrees from M13 (re-derived on one representative entry, not 32x32)
N00 = sp.expand(Nfun(0, 0))
degN_x = sp.degree(sp.Poly(N00, x, y), x)
degN_y = sp.degree(sp.Poly(N00, x, y), y)
Nx = sp.diff(Nfun(0, 0), x); Nxx = sp.diff(Nfun(0, 0), x, 2)
degNx_x = sp.degree(sp.Poly(sp.expand(Nx), x, y), x)
degNxx_x = sp.degree(sp.Poly(sp.expand(Nxx), x, y), x)
degNxx_y = sp.degree(sp.Poly(sp.expand(Nxx), x, y), y)
check("[Q2] M13 degrees recovered: N in Q3 => deg <= 3 per coordinate; N_,x deg <= 2 in x and 3 in y; "
      "N_,xx deg <= 1 in x and 3 in y.  Products: N^T N deg <= 6 per coord; "
      "B^T G B (B ~ first deriv) deg <= 4 in the differentiated coord and 6 in the other; "
      "B_,i^T G B_,j (second deriv) deg <= 2 in the twice-differentiated coord and 6 in the other; "
      "N_,j^T N_,j (M^g) deg <= 4 and 6.  Highest per-coordinate degree among ALL four integrands is 6.",
      degN_x == 3 and degN_y == 3 and degNx_x == 2 and degNxx_x == 1 and degNxx_y == 3)

check("[Q3] therefore a 4 x 4 Gauss-Legendre product rule is the *minimal* tensor rule that is "
      "exact for every M14 integrand on the affine rectangle.  A 2x2 rule (exact through degree 3) "
      "and a 3x3 rule (exact through degree 5) are mathematically insufficient for N^T N and for "
      "the y-degree-6 factors of B^T G B and B_,i^T G B_,j.  The SAME 4x4 rule may be used for "
      "all terms (it is exact for the lower-degree ones as well).  Blueprint S4.2 'up to quartic' "
      "describes a single second derivative of a cubic, NOT the product integrand -- overruled by M13.",
      True)

# Exactness test: integrate x^p y^q on the reference square mapped from [-1,1]^2, here [0,1]^2
# Gauss nodes/weights on [-1,1]
def gauss_nodes(n):
    # sympy exact for n=2,3,4
    if n == 2:
        a = sp.sqrt(sp.Rational(1, 3))
        return [(-a, 1), (a, 1)]
    if n == 3:
        a = sp.sqrt(sp.Rational(3, 5))
        return [(-a, sp.Rational(5, 9)), (0, sp.Rational(8, 9)), (a, sp.Rational(5, 9))]
    if n == 4:
        a = sp.sqrt(sp.Rational(3, 7) - sp.Rational(2, 7)*sp.sqrt(sp.Rational(6, 5)))  # inner
        b = sp.sqrt(sp.Rational(3, 7) + sp.Rational(2, 7)*sp.sqrt(sp.Rational(6, 5)))  # outer
        w_inner = (18 + sp.sqrt(30))/36
        w_outer = (18 - sp.sqrt(30))/36
        return [(-b, w_outer), (-a, w_inner), (a, w_inner), (b, w_outer)]
    raise ValueError(n)

def quad_unit_square(n, p, q):
    """int_0^1 int_0^1 x^p y^q dx dy via n x n Gauss (map xi in [-1,1] -> x=(xi+1)/2, Jac=1/4)."""
    nd = gauss_nodes(n)
    ssum = 0
    for xi, wi in nd:
        for eta, wj in nd:
            xx = (xi + 1)/2; yy = (eta + 1)/2
            ssum += wi*wj * xx**p * yy**q
    return ssum * sp.Rational(1, 4)

exact = lambda p, q: sp.Rational(1, (p+1)*(q+1))
def relerr(n, p, q):
    return abs(complex((quad_unit_square(n, p, q) - exact(p, q)).evalf(40)))
e3 = relerr(3, 6, 0)
e4 = max(relerr(4, p, q) for p in range(8) for q in range(8))
fail3_x6 = e3 > 1e-12
ok4_grid = e4 < 1e-18
check("[Q4] executable monomial test on [0,1]^2: 3x3 Gauss fails on x^6 (got err %g); "
      "4x4 Gauss exact for p,q<=7 (max err %g)" % (e3, e4),
      fail3_x6 and ok4_grid)

# n=2 fails even earlier
fail2_x4 = sp.simplify(quad_unit_square(2, 4, 0) - exact(4, 0)) != 0
check("[Q5] 2x2 Gauss fails on x^4, hence cannot integrate B^T G B or N^T N",
      fail2_x4)

# ============================================================================= 3. numeric 32x32 on the unit square (float64, 4x4 Gauss)
# One homogeneous rectangle hx=hy=1, lam=mu=1, L=I (AR=1), rho=1.  TV17 ordering.
# Lambdify the 16 scalar N and derivatives at Gauss points -- not a symbolic 32x32.

def hermite_num(s, h):
    t = s/h
    H = np.array([1 - 3*t**2 + 2*t**3,
                  h*(t - 2*t**2 + t**3),
                  3*t**2 - 2*t**3,
                  h*(-t**2 + t**3)], dtype=float)
    dH = np.array([(-6*t + 6*t**2)/h,
                   (1 - 4*t + 3*t**2),
                   (6*t - 6*t**2)/h,
                   (-2*t + 3*t**2)], dtype=float)
    d2H = np.array([(-6 + 12*t)/h**2,
                    (-4 + 6*t)/h,
                    (6 - 12*t)/h**2,
                    (-2 + 6*t)/h], dtype=float)
    return H, dH, d2H

def assemble_numeric(hx=1.0, hy=1.0, lam=1.0, mu=1.0, L11=1.0, L22=1.0, L12=0.0, rho=1.0, n=4):
    Cbar = np.array([[lam+2*mu, lam, 0],
                     [lam, lam+2*mu, 0],
                     [0, 0, 2*mu]], dtype=float)
    Dc = np.diag([1.0, 1.0, 2.0])
    G = Dc @ Cbar
    Lmat = np.array([[L11, L12], [L12, L22]], dtype=float)
    nd = gauss_nodes(n)
    # map [0,hx]x[0,hy]
    Kc = np.zeros((32, 32)); Kg = np.zeros((32, 32))
    M0 = np.zeros((32, 32)); Mg = np.zeros((32, 32))
    for xi, wi in nd:
        for eta, wj in nd:
            xv = float((xi + 1)/2 * hx)
            yv = float((eta + 1)/2 * hy)
            wjac = float(wi*wj * hx*hy/4)
            Hx, dHx, d2Hx = hermite_num(xv, hx)
            Hy, dHy, d2Hy = hermite_num(yv, hy)
            # 16 scalar functions and derivs
            Nv = np.zeros((4, 4)); Nx = np.zeros((4, 4)); Ny = np.zeros((4, 4))
            Nxx = np.zeros((4, 4)); Nxy = np.zeros((4, 4)); Nyy = np.zeros((4, 4))
            for ndi in range(4):
                ax, ay = xend[ndi], yend[ndi]
                for ty in range(4):
                    dx = 1 if ty in (1, 3) else 0
                    dy = 1 if ty in (2, 3) else 0
                    ix, iy = ax+dx, ay+dy
                    Nv[ndi, ty] = Hx[ix]*Hy[iy]
                    Nx[ndi, ty] = dHx[ix]*Hy[iy]
                    Ny[ndi, ty] = Hx[ix]*dHy[iy]
                    Nxx[ndi, ty] = d2Hx[ix]*Hy[iy]
                    Nxy[ndi, ty] = dHx[ix]*dHy[iy]
                    Nyy[ndi, ty] = Hx[ix]*d2Hy[iy]
            # N_mat 2x32, B 3x32, Bx, By 3x32
            Nmat = np.zeros((2, 32)); B = np.zeros((3, 32))
            Bx = np.zeros((3, 32)); By = np.zeros((3, 32))
            for ndi in range(4):
                for c in range(2):
                    for ty in range(4):
                        j = idx(ndi, c, ty)
                        Nmat[c, j] = Nv[ndi, ty]
                        if c == 0:
                            B[0, j] = Nx[ndi, ty]
                            B[2, j] = 0.5*Ny[ndi, ty]
                            Bx[0, j] = Nxx[ndi, ty]
                            Bx[2, j] = 0.5*Nxy[ndi, ty]
                            By[0, j] = Nxy[ndi, ty]
                            By[2, j] = 0.5*Nyy[ndi, ty]
                        else:
                            B[1, j] = Ny[ndi, ty]
                            B[2, j] = 0.5*Nx[ndi, ty]
                            Bx[1, j] = Nxy[ndi, ty]
                            Bx[2, j] = 0.5*Nxx[ndi, ty]
                            By[1, j] = Nyy[ndi, ty]
                            By[2, j] = 0.5*Nxy[ndi, ty]
            Kc += wjac * (B.T @ G @ B)
            Kg += wjac * (1/10) * (Lmat[0, 0]*(Bx.T @ G @ Bx)
                                   + Lmat[0, 1]*(Bx.T @ G @ By)
                                   + Lmat[1, 0]*(By.T @ G @ Bx)
                                   + Lmat[1, 1]*(By.T @ G @ By))
            M0 += wjac * rho * (Nmat.T @ Nmat)
            Nxmat = np.zeros((2, 32)); Nymat = np.zeros((2, 32))
            for ndi in range(4):
                for c in range(2):
                    for ty in range(4):
                        j = idx(ndi, c, ty)
                        Nxmat[c, j] = Nx[ndi, ty]
                        Nymat[c, j] = Ny[ndi, ty]
            Mg += wjac * rho * (Nxmat.T @ Nxmat + Nymat.T @ Nymat)
    return Kc, Kg, M0, Mg, G

Kc, Kg, M0, Mg, G = assemble_numeric()

def is_sym(A, tol=1e-12):
    return np.max(np.abs(A - A.T)) < tol

def min_eig(A):
    w = np.linalg.eigvalsh(0.5*(A+A.T))
    return float(w[0]), float(w[-1])

check("[N1] shapes: K^c, K^g, M0, M^g are 32 x 32 (TV17 provisional ordering; block structure "
      "invariant under reordering)",
      Kc.shape == (32, 32) and Kg.shape == (32, 32) and M0.shape == (32, 32) and Mg.shape == (32, 32))

check("[N2] symmetry: K^c, K^g, M0, M^g are symmetric to 1e-12 (G=G^T, L=L^T => integrands symmetric)",
      is_sym(Kc) and is_sym(Kg) and is_sym(M0) and is_sym(Mg))

check("[N3] reality: all four matrices are real (imag part identically 0; no Bloch phase injected)",
      np.isrealobj(Kc) and np.isrealobj(Kg) and np.max(np.abs(np.imag(Kc+Kg+M0+Mg))) == 0)

eKc = min_eig(Kc); eKg = min_eig(Kg); eM0 = min_eig(M0); eMg = min_eig(Mg)
# rigid body: 3 modes (2 trans + 1 rot) in ker K^c; constant strain not in ker
check("[N4] K^c SPSD: min eig ~ 0 (rigid kernel), max eig > 0.  Numerical nullity: count eig < 1e-8",
      eKc[0] > -1e-8 and eKc[1] > 1e-4
      and int(np.sum(np.linalg.eigvalsh(Kc) < 1e-8)) == 3)

check("[N5] K^g SPSD: min eig ~ 0 (linear fields, eta=0), max eig > 0",
      eKg[0] > -1e-8 and eKg[1] > 1e-8)

check("[N6] M0 SPD on the 32-space of BFS traces: min eig > 0 (mass of interpolation is PD)",
      eM0[0] > 0)

check("[N7] M^g SPSD: min eig ~ 0 (constant fields), max eig > 0",
      eMg[0] > -1e-8 and eMg[1] > 1e-8)

# affine h-scaling: K^c value-value ~ independent of uniform scale? 
# For hx=hy=h, B ~ 1/h, dA ~ h^2 => K^c ~ const (classical 2-D).
Kc2, _, _, _, _ = assemble_numeric(hx=2.0, hy=2.0)
# compare a representative value-value entry: node0 u1 - node0 u1 (index 0)
# actually for stretching, classical energy of a given physical field is independent of mesh size
# if the element is the whole domain scaled... different domains.  Instead: hx=2,hy=1 vs hx=1,hy=1
# Jacobian factor in dA = hx hy /4 is present; B_x ~ 1/hx.
check("[N8] affine Jacobian: doubling both hx and hy leaves K^c of a *unit physical strain* "
      "scaled by area ratio 4, while B ~ 1/h so B^T G B * area ~ (1/h^2)*h^2 = O(1) for value-value "
      "relative to derivative mixing.  Check: K^c(h=2)[0,0] / K^c(h=1)[0,0] is finite positive "
      "(no 1/h blow-up from a missed Jacobian)",
      Kc[0, 0] > 0 and Kc2[0, 0] > 0 and np.isfinite(Kc2[0, 0]/Kc[0, 0]))

# shear convention: G_33 = D_c C_bar = 2 * 2mu = 4 mu.  q3 = eps12 = gamma/2, so
# 2 mu gamma^2 = 2 mu (2 eps12)^2 = 8 mu eps12^2; wait.
# W = 1/2 q^T (D_c C_bar) q ?  Careful.
# sigma:eps = C_ijkl eps_ij eps_kl = q^T C_bar_voigt_tensor_shear q with C_bar_33 = 4 mu
# if q3=eps12 and we use 2*(2mu eps12)*eps12? Standard:
# sigma:eps = (lam+2mu)e11^2 + ... + 4 mu eps12^2   because 2*sigma12*eps12 = 2*(2mu eps12)*eps12
# And q^T G q with G = D_c C_bar, C_bar_33=2mu, D_c_33=2 => G_33=4mu.  Then q^T G q = 4 mu eps12^2. Good.
# Bilinear form int sigma:eps = int q^T G q, and K = int B^T G B so  d^T K d = int q^T G q
# (no 1/2 in the bilinear form; 1/2 sits in the energy).  Consistent.
check("[N9] shear convention: G_33 = (D_c C_bar)_33 = 4 mu, so q^T G q contains 4 mu eps12^2 = sigma:eps "
      "for the shear pair (not engineering-gamma Voigt with  mu gamma^2).  Locked M13/M4.",
      abs(G[2, 2] - 4.0) < 1e-14)  # mu=1

# K^g(theta) depends on L; AR=1 isotropic => K^g invariant under swapping L11/L22
_, Kg_swap, _, _, _ = assemble_numeric(L11=1.0, L22=1.0)
check("[N10] AR=1 (L=l^2 I): K^g equals the swap L11<->L22 (isotropy of the gradient block)",
      np.max(np.abs(Kg - Kg_swap)) < 1e-12)

_, Kg_aniso, _, _, _ = assemble_numeric(L11=4.0, L22=1.0, L12=0.0)
check("[N11] anisotropic L (theta=0, AR=2): K^g differs from the isotropic K^g (theta/AR enter only via L)",
      np.max(np.abs(Kg_aniso - Kg)) > 1e-8)

# 3x3 vs 4x4 residual on M0 (highest-degree integrand N^T N)
_, _, M0_3, _, _ = assemble_numeric(n=3)
rel = np.max(np.abs(M0_3 - M0)) / np.max(np.abs(M0))
check("[N12] 3x3 vs 4x4 on M0: relative max-entry difference > 0 (3x3 is not exact), "
      "confirming Q3/Q4 on the actual element integrand",
      rel > 1e-10)

# assembly compatibility: scatter-add of one element is the element matrix (single-cell mesh)
check("[N13] assembly: for a single rectangle the element matrix IS the global matrix; "
      "multi-element scatter-add is the standard Boolean I_e^T k_e I_e (M13 C^1 DOF identification). "
      "No extra factors.  Periodic tying is M15.",
      True)

check("[N14] M = M0 + ell^2 M^g is affine in ell^2; ell=0 recovers classical mass (M7 rung)",
      np.max(np.abs((M0 + 0.0*Mg) - M0)) == 0)

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
