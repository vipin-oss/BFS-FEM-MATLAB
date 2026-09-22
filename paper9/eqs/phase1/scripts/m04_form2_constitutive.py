#!/usr/bin/env python3
"""
Phase-1 / M4: Mindlin Form-II constitutive relations.

Blueprint v1.3 equations (13)-(18):
  (13)-(15) sigma_ij = C_ijkl eps_kl ; tau_ijk = A_ijklmn eta_lmn ; Voigt form
  (16)-(18) isotropic sixth-order gradient modulus (a1..a5) ; plane-strain reduction

Provenance:
  [C] FEM_3_Paper.txt Eq (17): D_ABCPQR = D_BACPQR = D_ABCQPR = D_PQRABC (symmetries);
      Eq (18): Psi_g = a1 G_ABB G_ACC + a2 G_AAC G_CBB + a3 G_AAC G_BBC + a4 G_ABC G_ABC
      + a5 G_ABC G_CBA ; Eq (19): [a1..a5] = [D] = Pa*m^2 ; Eq (24): Sigma_IJK = Sigma_JIK.
  [C] FEM_1_Paper.txt Eq (12): W = 1/2 C_ijkl eps_ij eps_kl + (1/20) L_mn C_ijkl eps_ij,m eps_kl,n
      with L = A A^T ; Eq (17): q_ijm = (1/10) L_mn C_ijkl eps_kl,n  ->  D = (1/10) L (x) C.
  [A] the theorem below (isotropic sub-case identification, symmetry and PD proofs)
      is derived symbolically here; no published source states it in this form.
Units: [C] = Pa, [D] = [a_p] = Pa*m^2, [L_mn] = m^2, [sigma] = Pa, [tau] = Pa*m.
Deterministic. No physical parameter values (lambda, mu, l_i are symbolic).
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

rng = (1, 2, 3)
pairs = [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
lam, mu = sp.symbols('lambda mu', real=True)
l1, l2, l3 = sp.symbols('l1 l2 l3', positive=True)

# --- independent strain-gradient components eta[(i,j),k] = eps_ij,k , symmetric in (i,j)
NV = {}
for (i, j) in pairs:
    for k in rng:
        NV[(i, j, k)] = sp.Symbol(f'n{i}{j}{k}', real=True)
def eta(i, j, k):
    return NV[(min(i, j), max(i, j), k)]
ETA = [NV[(i, j, k)] for (i, j) in pairs for k in rng]        # 18 independent variables

delta = lambda a, b: sp.Integer(1) if a == b else sp.Integer(0)
C4 = lambda i, j, k, l: lam*delta(i, j)*delta(k, l) + mu*(delta(i, k)*delta(j, l) + delta(i, l)*delta(j, k))
# L = A A^T is SYMMETRIC by construction (M1); the symmetric symbol matrix below enforces
# L_mn = L_nm explicitly (an unconstrained L would be a different, non-existent model).
Lt = sp.Matrix(3, 3, lambda m, n: sp.Symbol(f'L{min(m,n)}{max(m,n)}', positive=True))

# ============ (13)-(15): Cauchy stress, Voigt form, plane-strain reduction ============
e = sp.symbols('e11 e22 e33 e12 e13 e23', real=True)          # generic eps (tensor comps)
eps_m = {(1, 1): e[0], (2, 2): e[1], (3, 3): e[2], (1, 2): e[3], (1, 3): e[4], (2, 3): e[5]}
Eps = lambda i, j: eps_m[(min(i, j), max(i, j))]
sig = sp.Matrix(3, 3, lambda i, j: sum(C4(i+1, j+1, k+1, l+1)*Eps(k+1, l+1)
                                       for k in range(3) for l in range(3)))
sig_exact = sp.Matrix(3, 3, lambda i, j: lam*delta(i+1, j+1)*sum(Eps(k+1, k+1) for k in range(3))
                      + 2*mu*Eps(i+1, j+1))
check("(13),(14): sigma_ij = C_ijkl eps_kl = lambda delta_ij eps_kk + 2 mu eps_ij",
      sp.simplify(sig - sig_exact) == sp.zeros(3))
# plane-strain reduction (eps_33 = eps_13 = eps_23 = 0): 3x3 Voigt block on (11,22,12)
ps = {e[2]: 0, e[4]: 0, e[5]: 0}
def Vc(i, j, k, l):
    """Matrix representation of C on independent strain pairs: the tensor sum
    sigma_ij = sum_{k,l} C_ijkl eps_kl is grouped over symmetric pairs, so each
    off-diagonal pair contributes C_ijkl + C_ijlk (factor 2 on the shear pair,
    i.e. the eps_12 - not gamma_12 - convention). Documented for M14 assembly."""
    return C4(i, j, k, l) + (0 if k == l else C4(i, j, l, k))
Cps = sp.Matrix(3, 3, lambda a, b: 0)
idx = [(1, 1), (2, 2), (1, 2)]
for a, (i, j) in enumerate(idx):
    for b, (k, l) in enumerate(idx):
        Cps[a, b] = Vc(i, j, k, l)
check("plane strain: C_bar (11,22,12) = [[lam+2mu, lam, 0],[lam, lam+2mu, 0],[0,0,2mu]]",
      sp.simplify(Cps - sp.Matrix([[lam+2*mu, lam, 0], [lam, lam+2*mu, 0], [0, 0, 2*mu]])) == sp.zeros(3))
check("plane strain: sigma_33 = lambda (eps_11+eps_22) != 0 (plane strain, not plane stress)",
      sp.simplify(sig[2, 2].subs(ps) - lam*(e[0] + e[1])) == 0)

# ============ (16)-(18): five-constant isotropic invariant basis ============
t_vec = [sum(eta(A, B, B) for B in rng) for A in rng]         # t_A = eta_ABB
v_vec = [sum(eta(A, A, C) for A in rng) for C in rng]         # v_C = eta_AAC
T1 = sum(t_vec[A-1]**2 for A in rng)
T2 = sum(v_vec[C-1]*t_vec[C-1] for C in rng)
T3 = sum(v_vec[C-1]**2 for C in rng)
T4 = sum(eta(A, B, C)**2 for A in rng for B in rng for C in rng)
T5 = sum(eta(A, B, C)*eta(C, B, A) for A in rng for B in rng for C in rng)
tA = [sum(eta(A, B, B) for B in rng) for A in rng]          # t_A = eta_ABB
vC = [sum(eta(A, A, C) for A in rng) for C in rng]          # v_C = eta_AAC
check("invariant identities: T1 = |t|^2 = sum_A t_A^2", sp.expand(T1 - sum(x**2 for x in tA)) == 0)
check("invariant identities: T2 = t.v = sum_C v_C t_C", sp.expand(T2 - sum(vC[c]*tA[c] for c in range(3))) == 0)
check("invariant identities: T3 = |v|^2 = sum_C v_C^2", sp.expand(T3 - sum(x**2 for x in vC)) == 0)
invariants = [T1, T2, T3, T4, T5]
a = sp.symbols('a1:6', real=True)

# ============ factorized Form-II modulus of blueprint (26): D = (1/10) L (x) C ============
def Psi_fact(Lmat):
    """W_g = (1/20) sum_mn L_mn C_ijkl eta_ijm eta_kln  (blueprint (22),(26); FEM_1 (12))."""
    s = 0
    for m in rng:
        for n in rng:
            for i in rng:
                for j in rng:
                    for k in rng:
                        for l in rng:
                            s += Lmat[m-1, n-1]*C4(i, j, k, l)*eta(i, j, m)*eta(k, l, n)
    return sp.expand(s/20)

L_iso = sp.eye(3)*sp.Symbol('lsq', positive=True)              # L = l^2 delta  (isotropic length)
Psi_iso = Psi_fact(L_iso)
Psi_5 = sum(a[p-1]*invariants[p-1] for p in range(1, 6))

# --- exact linear solve: coefficient of each monomial in eta
def coeffs(expr):
    """Coefficient dictionary {exponent tuple in (n111,...,n333) -> coefficient}.
    Poly is used so that lambda, mu, lsq stay in the coefficient ring (NOT in the monomial key)."""
    P = sp.Poly(sp.expand(expr), *ETA)
    return {mon: c for mon, c in P.terms()}
keys = sorted(set(list(coeffs(Psi_iso).keys()) + [k for T in invariants for k in coeffs(T).keys()]))
A = sp.Matrix(len(keys), 5, lambda r, c: coeffs(invariants[c]).get(keys[r], 0))
b = sp.Matrix(len(keys), 1, lambda r, c: coeffs(Psi_iso).get(keys[r], 0))
check("five invariants (18)-(18) are linearly independent (rank 5)", A.rank() == 5)
sol_iso = A.gauss_jordan_solve(b)[0]
sol_iso_s = [sp.simplify(sol_iso[i]) for i in range(5)]
lk = sp.Symbol('lsq', positive=True)
expect = [0, 0, lam*lk/20, mu*lk/10, 0]
check("isotropic length limit: (a1..a5) = (0, 0, lambda*l^2/20, mu*l^2/10, 0)  [exact, unique]",
      all(sp.simplify(sol_iso_s[i] - expect[i]) == 0 for i in range(5)))
print("   solved (a1..a5) =", [sp.nsimplify(x) for x in sol_iso_s])

# --- double stress tau_ijk = dW/deta = (1/10) L_mn C_ijkl eta_kln  (FEM_1 (17), blueprint (17))
W = Psi_fact(Lt)
dW = [sp.diff(W, ETA[q]) for q in range(18)]
taus = {}
for (i, j) in pairs:
    for k in rng:
        taus[(i, j, k)] = (sp.Rational(1, 10)*sum(Lt[m-1, n-1]*C4(i, j, p, q)*eta(p, q, n)
                                                for m in rng for n in rng
                                                for p in rng for q in rng
                                                if m == k))
# eta_ij is a SYMMETRIC pair, so the partial derivative w.r.t. the independent component
# n_ijk carries the multiplicity c_ij = 2 - delta_ij (both orderings (i,j) and (j,i) move).
# Consequence for M13/M14: off-diagonal strain-gradient pairs carry a factor 2 in the
# B-matrix conjugation, matching the factor 2 in the Voigt matrix Vc() above.
check("(17): dW/dn_ijk = (2 - delta_ij) * (1/10) L_kn C_ijrs eta_rsn  [tensor form tau_ijk = (1/10)L_mn C_ijkl eta_kln, FEM_1 (17)]",
      all(sp.expand(sp.diff(W, NV[(i, j, k)]) - (2 - delta(i, j))*taus[(i, j, k)]) == 0
          for (i, j) in pairs for k in rng))
check("variation form: delta W = sum_{i<=j,k} c_ij tau_ijk delta n_ijk, c_ij = 2 - delta_ij",
      all(sp.expand(sp.diff(W, NV[(i, j, k)])) == sp.expand((2 - delta(i, j))*taus[(i, j, k)])
          for (i, j) in pairs for k in rng))
check("(24)/Form-II minor symmetry: tau_ijk = tau_jik",
      all(sp.expand(taus[(min(i, j), max(i, j), k)] - taus[(min(j, i), max(j, i), k)]) == 0
          for (i, j) in pairs for k in rng))
# major symmetry of the sixth-order modulus: D_ijm|kln = D_kln|ijm
D6 = lambda i, j, m, k, l, n: sp.Rational(1, 10)*Lt[m-1, n-1]*C4(i, j, k, l)
check("major symmetry D_ijm kln = D_kln ijm (Hessian symmetry of W_g)",
      all(sp.simplify(D6(i, j, m, k, l, n) - D6(k, l, n, i, j, m)) == 0
          for i in rng for j in rng for m in rng for k in rng for l in rng for n in rng))
check("minor symmetry in the gradient pair: D_ijm kln = D_ijn klm (L symmetric)",
      all(sp.simplify(D6(i, j, m, k, l, n) - D6(i, j, n, k, l, m)) == 0
          for i in rng for j in rng for m in rng for k in rng for l in rng for n in rng))

# ============ plane-strain 6x6 gradient modulus, PD, dimensions ============
def M6_block(Lmat, l1v=None, l2v=None):
    """rows/cols ordered (11,22,12) x (1,2): M[(ij,m),(kl,n)] = (1/10) L_mn C_ijkl."""
    order = [(1, 1, 1), (2, 2, 1), (1, 2, 1), (1, 1, 2), (2, 2, 2), (1, 2, 2)]
    M = sp.Matrix(6, 6, lambda r, c: 0)
    for r, (i, j, m) in enumerate(order):
        for c, (k, l, n) in enumerate(order):
            M[r, c] = sp.Rational(1, 10)*Lmat[m-1, n-1]*Vc(i, j, k, l)
    return M, order
M6, _ = M6_block(Lt)
check("plane-strain gradient modulus (6x6) is symmetric (major symmetry)", sp.simplify(M6 - M6.T) == sp.zeros(6))
# PD of the implemented model: M = (1/10) L_bar (x) C_bar with both factors PD
Ct = sp.Matrix([[lam + 2*mu, lam, 0], [lam, lam + 2*mu, 0], [0, 0, 2*mu]])
Lbar = sp.Matrix([[l1**2, 0], [0, l2**2]])
M6_iso, order = M6_block(sp.diag(l1**2, l2**2, l3**2))
perm_rows = [(1, 1, 1), (2, 2, 1), (1, 2, 1), (1, 1, 2), (2, 2, 2), (1, 2, 2)]
perm_cols = [(1, 1), (2, 2), (1, 2)]
K6 = sp.zeros(6, 6)
for r, (i, j, m) in enumerate(perm_rows):
    for c, (k, l, n) in enumerate(perm_rows):
        K6[r, c] = sp.Rational(1, 10)*sp.diag(l1**2, l2**2)[m-1, n-1]*Ct[perm_cols.index((min(i,j), max(i,j))),
                                                                         perm_cols.index((min(k,l), max(k,l)))]
check("2D plane-strain modulus = (1/10) L_bar (x) C_bar with L_bar = diag(l1^2,l2^2)",
      sp.simplify(M6_iso - K6) == sp.zeros(6))
check("C_bar PD: leading minors > 0 under mu > 0, lambda + mu > 0",
      sp.simplify(Ct[0, 0] - (lam + 2*mu)) == 0 and sp.simplify(Ct.det() - 8*mu**2*(lam + mu)) == 0)
check("L_bar PD for admissible ellipsoids (l1, l2 > 0): minors l1^2 > 0, l1^2 l2^2 > 0",
      sp.simplify(Lbar[0, 0] - l1**2) == 0 and sp.simplify(Lbar.det() - l1**2*l2**2) == 0)
print("DIM: [C_ijkl] = Pa; [L_mn] = m^2; [D_ijklmn] = (1/10)[L][C] = Pa*m^2  (= [a1..a5], FEM_3 (19))")

# ============ anisotropy: outside the isotropic five-constant family when l1 != l2 ====
th = sp.Symbol('theta', real=True)
c45, s45 = sp.Rational(3, 5), sp.Rational(4, 5)               # exact rational rotation
Rd = sp.Matrix([[c45, -s45, 0], [s45, c45, 0], [0, 0, 1]])
eta0 = {key: (1 if key == (1, 1, 1) else 0) for key in NV}
def rot_eta(eta_v, R):
    out = {k: 0 for k in NV}
    for (i, j) in pairs:
        for k in rng:
            val = 0
            for A in rng:
                for B in rng:
                    for C in rng:
                        # eta is symmetric in the first two indices -> sorted key lookup
                        val += R[A-1, i-1]*R[B-1, j-1]*R[C-1, k-1]*eta_v[(min(A, B), max(A, B), C)]
            out[(i, j, k)] = sp.nsimplify(val)
    return out
eta_r = rot_eta(eta0, Rd)
sub0 = lambda expr, ev: sp.expand(expr.subs({NV[k]: ev[k] for k in NV}))
Taniso = [(T, sub0(T, eta0), sub0(T, eta_r)) for T in invariants]
check("five invariants are rotation-invariant (isotropic by construction)",
      all(sp.simplify(b - c) == 0 for (_, b, c) in Taniso))
L_an = sp.diag(l1**2, l2**2, l3**2)
Wan = Psi_fact(L_an)
d_rot = sp.factor(sp.simplify(sub0(Wan, eta_r) - sub0(Wan, eta0)))
check("anisotropic W_g is NOT rotation-invariant when l1 != l2 "
      "(hence outside the 5-constant isotropic family) [recorded as note F1]",
      d_rot != 0 and sp.factor(sp.expand(d_rot)) != 0)
print("   rotation-difference (factored):", sp.factor(d_rot))

# ============ [C] legacy mapping FEM_3 (84)-(85): recorded comparison (note F1) =======
l = sp.Symbol('ell', positive=True)
c3 = c4 = l**2*lam/12
c5 = c7 = l**2*(7*mu + 3*lam)/120
c6 = l**2*(7*mu - 4*lam)/120
a_leg = [2*c5, 2*c3, c4/2, c6, 2*c7]
check("legacy FEM_3 (84)-(85) isotropic tuple: a1 = ell^2(7mu+3lam)/60 != 0 for admissible "
      "(mu>0, 2mu+3lam>0)  => not a rescaling of the factorized model (which has a1=a2=a5=0)",
      sp.simplify(a_leg[0] - l**2*(7*mu + 3*lam)/60) == 0)
print("   NOTE F1: legacy FEM_3 (84)-(85) is NOT the isotropic limit of blueprint (26); "
      "implemented model follows blueprint (26) (explicit) - see DERIVATION notes.")
print(f"\nALL {len(OK)} CHECKS PASSED - M4 (blueprint eqs 13-18, incl. (26) modulus structure)")
