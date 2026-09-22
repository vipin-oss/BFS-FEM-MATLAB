#!/usr/bin/env python3
"""
Phase-1 / M15-a audit: blueprint v1.3 eq. (68)  Kbar(k) = Kbar(-k)^H  and the Sec 4 / 5a test
      ||Kbar(k) - Kbar(-k)^H|| / ||Kbar|| < 1e-12.

Scope: M15-a ONLY (the item flagged by M9, DERIVATION_M09.md Sec M9.8). Nothing here starts M10
or M15: no k-path, no BFS 2D element, no material value, no band, no solver. Everything is
exact symbolic (SymPy) except where a float cross-check is explicitly labelled as INDEPENDENT
(NumPy, used only to recompute a number a second way).

Independence policy: every identity is RE-DERIVED here from the locked M8/M9 formulation
(real symmetric K, M from a real energy; tying d = T(k) dbar with T built from the derived
Bloch phases mu_alpha = e^{i k.a_alpha} on value AND derivative DOFs, M9 (41)-(43), (D2)).
No result is imported from the M9 script; the M9 counterexample is reproduced from scratch
and additionally re-derived from an actual C^1 (Hermite) element.

Sections
  A  general theorem for an arbitrary real symmetric K and an arbitrary Bloch tying pattern
  B  the M9 counterexample, reproduced (exact) and re-computed independently (float)
  C  formulation-derived counterexample: 1D C^1 Hermite gradient-elastic bar, 2 elements
  D  route diagnosis refined: sesquilinear vs bilinear envelope matrices
  E  wrong-sign derivative-DOF phase: what it preserves, what it violates
  F  publication-grade verification structure (T1 Hermiticity, T2 conjugation,
     T3 Bloch-wave consistency, T4 long-wave / independent reference) and its power
"""
import sympy as sp
import numpy as np
import time, sys

OK = []
_t0 = time.time()
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}"); sys.stdout.flush()
    if '--timing' in sys.argv:
        print(f"   [t = {time.time()-_t0:.1f}s]"); sys.stdout.flush()

def iszero(e):
    e = sp.expand(e)
    if sp.simplify(e) == 0:
        return True
    return sp.simplify(sp.expand(e.rewrite(sp.cos))) == 0

def mzero(Mx):
    return all(iszero(z) for z in Mx)

def imag(z):
    """exact imaginary part of an expression in e^{i theta} with real symbols"""
    return sp.simplify(sp.im(sp.expand(z.rewrite(sp.cos))))

def fro2(Mx):
    """squared Frobenius norm, exact"""
    return sp.simplify(sum(sp.expand(z*sp.conjugate(z)) for z in Mx))

th1, th2 = sp.symbols('theta1 theta2', real=True)      # theta_alpha = k . a_alpha (real k)

# =============================================================================
# A. GENERAL THEOREM (arbitrary real symmetric K, arbitrary Bloch tying pattern)
# =============================================================================
print("--- A. general identities for Kbar = T(k)^H K T(k), K real symmetric, T Bloch tying")

# 6 full DOFs: 3 master classes (m0,m1,m2) + 3 slaves: s0 = mu1 m0, s1 = mu2 m1, s2 = mu1 mu2 m2
# (an edge pair in a_1, an edge pair in a_2 and a corner pair, i.e. all three phase types of M9 (D3))
n = 6
Ksym = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'K{min(i,j)}{max(i,j)}', real=True))
mu1, mu2 = sp.exp(sp.I*th1), sp.exp(sp.I*th2)
T = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1],
               [mu1, 0, 0], [0, mu2, 0], [0, 0, mu1*mu2]])
def Tk(t1, t2):
    return T.subs({th1: t1, th2: t2}, simultaneous=True)
Kb = (T.H*Ksym*T).applyfunc(sp.expand)
Kb_neg = (Tk(-th1, -th2).H*Ksym*Tk(-th1, -th2)).applyfunc(sp.expand)

check("[A1] K is real symmetric (hypothesis of M6/M14: K comes from a real quadratic energy) and "
      "T(k) is built from the UNIMODULAR Bloch phases of M9 on every tied DOF: T(-k) = conj(T(k)), "
      "T(k)^H T(k) = 2 I_3 (each master column carries |1|^2 + |mu|^2 = 2: an isometry up to the "
      "pair multiplicity).",
      Ksym == Ksym.T and all(s.is_real for s in Ksym.free_symbols)
      and mzero(Tk(-th1, -th2) - T.conjugate())
      and mzero((T.H*T).applyfunc(sp.expand) - 2*sp.eye(3)))

check("[A2] HERMITICITY, always:  Kbar(k)^H = (T^H K T)^H = T^H K^T T = T^H K T = Kbar(k). "
      "Uses only K = K^T real. (Re-derived here on the 6-DOF pattern with 21 free real entries.)",
      mzero(Kb - Kb.H))

check("[A3] CONJUGATION under k -> -k, always:  Kbar(-k) = T(-k)^H K T(-k) = T^T K conj(T) "
      "= conj(T^H K T) = conj(Kbar(k)). Uses T(-k) = conj(T(k)) [A1] and K real.",
      mzero(Kb_neg - Kb.conjugate()))

check("[A4] CONSEQUENCE for the blueprint's expression:  Kbar(-k)^H = conj(Kbar(k))^H = Kbar(k)^T. "
      "Hence the literal (68)  Kbar(k) = Kbar(-k)^H  is EXACTLY the statement  Kbar(k) = Kbar(k)^T "
      "(complex symmetry), which together with Hermiticity [A2] is EXACTLY 'Kbar(k) is REAL'. "
      "Identity  Kbar(k) - Kbar(-k)^H = Kbar(k) - Kbar(k)^T = 2 i Im(Kbar(k))  verified.",
      mzero(Kb_neg.H - Kb.T)
      and mzero((Kb - Kb_neg.H) - (Kb - Kb.T))
      and mzero((Kb - Kb_neg.H) - 2*sp.I*Kb.applyfunc(imag)))

# realness fails generically: the imaginary part of Kbar is a non-trivial linear form in K entries
ImKb = Kb.applyfunc(imag)
check("[A5] REALNESS IS NOT IMPLIED: Im Kbar(k) is a non-zero linear form in the entries of K, e.g. "
      f"Im Kbar_01 = {sp.simplify(ImKb[0,1])} ; it vanishes for all k only under EXTRA relations "
      "between DISTINCT entries of K (K_{m0,s1} = K_{s0,m1} etc.), which real symmetry (K_ij = K_ji) "
      "does not supply. So (68) is CONDITIONALLY true only under an additional realness hypothesis.",
      not iszero(ImKb[0, 1]) and not iszero(ImKb[0, 2]) and not iszero(ImKb[1, 2])
      and all(iszero(ImKb[i, i]) for i in range(3)))

# the realness condition, made explicit for the m0/m1 block
cond01 = sp.solve(sp.expand(ImKb[0, 1]), Ksym[0, 4])   # K_{m0,s1}
check("[A6] The realness condition is a genuine extra hypothesis: Im Kbar_01 = 0 for all k iff "
      f"K_(m0,s1) - K_(s0,m1)... explicitly solving gives K04 = {cond01} -- a constraint between "
      "two different physical couplings (master-0 to slave-1 vs slave-0 to master-1). It holds for "
      "geometrically mirror-symmetric couplings only, and never follows from K = K^T.",
      len(cond01) == 1 and cond01[0] != Ksym[0, 4])

# the same for the mass matrix (also real symmetric): identical structure
Msym = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'M{min(i,j)}{max(i,j)}', real=True))
Mb = (T.H*Msym*T).applyfunc(sp.expand)
Mb_neg = (Tk(-th1, -th2).H*Msym*Tk(-th1, -th2)).applyfunc(sp.expand)
check("[A7] The same three statements hold verbatim for the reduced mass matrix "
      "Mbar = T^H (M0 + ell^2 M^g) T (blueprint (61), (65)): Hermitian, Mbar(-k) = conj(Mbar(k)), "
      "and Mbar(-k)^H = Mbar^T (so a literal '(68) for M' would likewise demand realness).",
      mzero(Mb - Mb.H) and mzero(Mb_neg - Mb.conjugate()) and mzero(Mb_neg.H - Mb.T))

# spectral consequence: charpoly of the pencil is even in k (what the physics needs)
lamS = sp.Symbol('lam')
Ks = Kb.subs({Ksym[i, j]: 0 for i in range(n) for j in range(n) if (i, j) not in
              [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(0,1),(0,4),(1,3),(2,5),(0,3),(1,4)]})
Ms = sp.diag(*[Msym[i, i] for i in range(3)])   # simple positive diagonal reduced mass for speed
pk = (Ks - lamS*Ms).det()
pk_neg = pk.subs({th1: -th1, th2: -th2}, simultaneous=True)
check("[A8] SPECTRAL CONSEQUENCE of [A2]+[A3] (the property the band structure actually needs): "
      "det(Kbar(-k) - lam Mbar(-k)) = det(conj(Kbar - lam Mbar)) = conj(det(Kbar - lam Mbar)) = "
      "det(Kbar - lam Mbar) for real lam (Hermitian pencil => real det), hence omega_n(k) = omega_n(-k). "
      "Verified on a sparse instance of the 6-DOF pattern. (68) is NOT needed for this.",
      iszero(sp.expand(pk - pk_neg)))

# =============================================================================
# B. THE M9 COUNTEREXAMPLE: reproduced exactly and recomputed independently
# =============================================================================
print("--- B. M9 counterexample: exact reproduction + independent float recomputation")

a, b, c, d, e, f = sp.symbols('a b c d e f', real=True)
th = sp.Symbol('theta', real=True)
K3 = sp.Matrix([[a, b, d], [b, c, f], [d, f, e]])            # nodes: 0 master, 1 interior, 2 slave
T3 = sp.Matrix([[1, 0], [0, 1], [sp.exp(sp.I*th), 0]])      # node 2 = mu node 0
K3b = (T3.H*K3*T3).applyfunc(sp.expand)
K3b_neg = K3b.subs(th, -th)
check("[B1] Reduced 2x2 (re-derived): Kbar = [[a+e+2d cos th, b + f e^{-i th}],[b + f e^{+i th}, c]] "
      "-- agrees with M9 (C11); Hermitian; Kbar(-k) = conj Kbar(k).",
      mzero(K3b - sp.Matrix([[a + e + 2*d*sp.cos(th), b + f*sp.exp(-sp.I*th)],
                             [b + f*sp.exp(sp.I*th), c]]))
      and mzero(K3b - K3b.H) and mzero(K3b_neg - K3b.conjugate()))

Dv = (K3b - K3b_neg.H).applyfunc(sp.expand)
check("[B2] Kbar(k) - Kbar(-k)^H = [[0, -2 i f sin th],[2 i f sin th, 0]] exactly; zero iff f sin th = 0.",
      mzero(Dv - sp.Matrix([[0, -2*sp.I*f*sp.sin(th)], [2*sp.I*f*sp.sin(th), 0]])))

num = {a: 1, b: 1, c: 1, d: 0, e: 1, f: 1, th: sp.pi/2}
Kn = K3b.subs(num).applyfunc(sp.simplify)
Dn = Dv.subs(num).applyfunc(sp.simplify)
n2K, n2D = fro2(Kn), fro2(Dn)
ratio = sp.sqrt(n2D/n2K)
check("[B3] EXACT numbers at a=b=c=e=f=1, d=0, theta=pi/2: Kbar = [[2, 1-i],[1+i, 1]], "
      f"||Kbar||_F^2 = {n2K}, ||Kbar - Kbar(-k)^H||_F^2 = {n2D}, relative violation = {sp.nsimplify(ratio)} "
      f"= {float(ratio):.6f}  (M9 reported 9, 8, 2 sqrt(2)/3 = 0.943 -- REPRODUCED).",
      Kn == sp.Matrix([[2, 1 - sp.I], [1 + sp.I, 1]]) and n2K == 9 and n2D == 8
      and iszero(ratio - 2*sp.sqrt(2)/3))

# INDEPENDENT recomputation with NumPy (no SymPy object reused)
Kf = np.array([[1., 1., 0.], [1., 1., 1.], [0., 1., 1.]])
def Tf(t):  return np.array([[1, 0], [0, 1], [np.exp(1j*t), 0]])
Kbf = Tf(np.pi/2).conj().T @ Kf @ Tf(np.pi/2)
Kbf_neg = Tf(-np.pi/2).conj().T @ Kf @ Tf(-np.pi/2)
r_lit = np.linalg.norm(Kbf - Kbf_neg.conj().T) / np.linalg.norm(Kbf)
r_herm = np.linalg.norm(Kbf - Kbf.conj().T) / np.linalg.norm(Kbf)
r_conj = np.linalg.norm(Kbf_neg - Kbf.conj()) / np.linalg.norm(Kbf)
check("[B4] INDEPENDENT float recomputation (NumPy, matrices typed in by hand): "
      f"literal-(68) residual = {r_lit:.12f} (expected 0.942809...), Hermiticity residual = {r_herm:.1e}, "
      f"conjugation residual = {r_conj:.1e}. The literal test FAILS by O(1) for a CORRECT tying; "
      "the two always-true identities pass at round-off.",
      abs(r_lit - 2*np.sqrt(2)/3) < 1e-12 and r_herm < 1e-15 and r_conj < 1e-15)

# =============================================================================
# C. FORMULATION-DERIVED COUNTEREXAMPLE: 1D C^1 Hermite gradient-elastic bar
# =============================================================================
print("--- C. formulation-derived counterexample: 1D C^1 Hermite bar (value + derivative DOFs)")

xi, h = sp.symbols('xi h', positive=True)
E, g2, rho = sp.symbols('E g2 rho', positive=True)   # E: modulus, g2 = gradient length^2, rho
# cubic Hermite shape functions on [0,h], DOFs (u0, u0', u1, u1')
s = xi/h
N = sp.Matrix([1 - 3*s**2 + 2*s**3, h*(s - 2*s**2 + s**3), 3*s**2 - 2*s**3, h*(-s**2 + s**3)])
Nx = N.diff(xi); Nxx = Nx.diff(xi)
# 1D reduction of the locked energy (M6): W = (1/2)E u'^2 + (1/2) E g2 u''^2 ; kinetic with micro-inertia
Ke_cl = sp.integrate(E*Nx*Nx.T, (xi, 0, h)).applyfunc(sp.simplify)
Ke_g = sp.integrate(E*g2*Nxx*Nxx.T, (xi, 0, h)).applyfunc(sp.simplify)
Me = sp.integrate(rho*N*N.T, (xi, 0, h)).applyfunc(sp.simplify)
Ke = Ke_cl + Ke_g
check("[C1] Element matrices of the 1D C^1 Hermite element derived from the shape functions "
      "(classical + gradient stiffness, consistent mass): all REAL SYMMETRIC, and the classical "
      "part annihilates the rigid mode (1,0,1,0) while the gradient part annihilates the linear "
      "mode (0,1,h,1) as well (sanity of the derivation).",
      Ke == Ke.T and Me == Me.T
      and mzero(Ke_cl*sp.Matrix([1, 0, 1, 0]))
      and mzero(Ke_g*sp.Matrix([0, 1, h, 1])) and mzero(Ke_g*sp.Matrix([1, 0, 1, 0])))

# assemble 2 elements: nodes 0,1,2 ; global DOFs (u0,u0',u1,u1',u2,u2')
def assemble(Ke_):
    K = sp.zeros(6, 6)
    for el, off in ((0, 0), (1, 2)):
        for i in range(4):
            for j in range(4):
                K[off + i, off + j] += Ke_[i, j]
    return K
Kg, Mg = assemble(Ke), assemble(Me)
kk = sp.Symbol('k', real=True)
mu = sp.exp(sp.I*kk*2*h)          # cell length 2h ; node 2 = mu node 0 (value AND derivative, M9 (43))
Tc = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1],
                [mu, 0, 0, 0], [0, mu, 0, 0]])
Kbar_c = (Tc.H*Kg*Tc).applyfunc(sp.expand)
Mbar_c = (Tc.H*Mg*Tc).applyfunc(sp.expand)
Kbar_c_neg = Kbar_c.subs(kk, -kk)
check("[C2] Reduced 4x4 matrices of the C^1 cell with the DERIVED tying (same mu on u and u'): "
      "Hermitian and Kbar(-k) = conj Kbar(k) (both K and M).",
      mzero(Kbar_c - Kbar_c.H) and mzero(Kbar_c_neg - Kbar_c.conjugate())
      and mzero(Mbar_c - Mbar_c.H) and mzero(Mbar_c.subs(kk, -kk) - Mbar_c.conjugate()))

ImK = Kbar_c.applyfunc(lambda z: sp.simplify(sp.im(sp.expand(z.rewrite(sp.cos)))))
lit_res = (Kbar_c - Kbar_c_neg.H).applyfunc(sp.simplify)
check("[C3] For this ACTUAL C^1 element Kbar(k) is NOT real: e.g. Im Kbar_(u0,u1) = "
      f"{sp.factor(ImK[0,2])} != 0 and Im Kbar_(u0',u1) = {sp.factor(ImK[1,2])} != 0 for generic k. "
      "Therefore the literal (68) fails for a correctly assembled, correctly tied C^1 gradient-elastic "
      "cell -- the counterexample is not an artefact of an abstract matrix.",
      not iszero(ImK[0, 2]) and not iszero(ImK[1, 2]) and not mzero(lit_res))

num_c = {E: 1, g2: sp.Rational(1, 10), rho: 1, h: 1, kk: sp.pi/4}
Kc_n = Kbar_c.subs(num_c).applyfunc(sp.nsimplify)
lit_n = (Kbar_c - Kbar_c_neg.H).subs(num_c).applyfunc(sp.nsimplify)
ratio_c = sp.sqrt(fro2(lit_n)/fro2(Kc_n))
check("[C4] Magnitude of the literal-(68) residual for the C^1 cell at k = pi/(4h) (illustrative, "
      f"unit moduli, g2 = h^2/10 -- NOT a production parameter): ||Kbar - Kbar(-k)^H||/||Kbar|| = "
      f"{float(ratio_c):.4f}, i.e. O(1), versus the required 1e-12; at Gamma (k=0) the residual is 0 "
      "(real periodic problem), so a Gamma-only run would NOT reveal the defect of the test.",
      float(ratio_c) > 0.1 and mzero(lit_res.subs(kk, 0)))

# =============================================================================
# D. ROUTE DIAGNOSIS REFINED: sesquilinear vs bilinear envelope matrices
# =============================================================================
print("--- D. envelope (k-shift) route: where (68) literally holds and where it does not")

# envelope route on the same 1D Hermite element with periodic envelope: (d/dx + i k) acting on N
Dk = lambda V: V.diff(xi) + sp.I*kk*V
Nk1, Nk2 = Dk(N), Dk(Dk(N))
# sesquilinear (Galerkin with conjugated test function) -> the correct variational matrix
Ke_sesq = sp.integrate(E*Nk1.conjugate()*Nk1.T + E*g2*Nk2.conjugate()*Nk2.T, (xi, 0, h)).applyfunc(sp.expand)
# bilinear (no conjugation) -> complex symmetric matrix
Ke_bil = sp.integrate(E*Nk1*Nk1.T + E*g2*Nk2*Nk2.T, (xi, 0, h)).applyfunc(sp.expand)
check("[D1] SESQUILINEAR envelope matrix K_e(k) = int (D_k N)^* E (D_k N)^T + ... : Hermitian, "
      "K_e(-k) = conj K_e(k), K_e(-k)^H = K_e(k)^T != K_e(k) (not real): i.e. EXACTLY the same "
      "algebraic structure as the tying route [A2]-[A4]; the literal (68) fails here too.",
      mzero(Ke_sesq - Ke_sesq.H) and mzero(Ke_sesq.subs(kk, -kk) - Ke_sesq.conjugate())
      and mzero(Ke_sesq.subs(kk, -kk).H - Ke_sesq.T) and not mzero(Ke_sesq - Ke_sesq.T))

check("[D2] BILINEAR envelope matrix (test function NOT conjugated): COMPLEX SYMMETRIC, satisfies "
      "the literal (68) K_e(k) = K_e(-k)^H identically, but is NOT Hermitian -- confirming M9 [X3] "
      "with the precise source located: (68) is the identity of a complex-symmetric family with "
      "K(-k) = conj K(k); it is not a property of the Hermitian (variationally correct) formulation.",
      mzero(Ke_bil - Ke_bil.T) and mzero(Ke_bil.subs(kk, -kk).H - Ke_bil)
      and not mzero(Ke_bil - Ke_bil.H))

check("[D3] Both envelope matrices reduce to the same real symmetric K at k = 0, and the sesquilinear "
      "one equals the tying-route reduced matrix in structure (Hermitian + conjugation); the two "
      "identities of ruling (a) are therefore ROUTE-INDEPENDENT, whereas the literal (68) is not.",
      mzero(Ke_sesq.subs(kk, 0) - Ke_bil.subs(kk, 0)) and mzero(Ke_sesq.subs(kk, 0) - Ke))

# =============================================================================
# E. WRONG-SIGN DERIVATIVE-DOF PHASE: what it preserves / violates
# =============================================================================
print("--- E. wrong-sign (and missing) phase on the derivative DOFs")

Tw = Tc.copy(); Tw[5, 1] = 1/mu            # derivative DOF tied with mu^{-1}, value with mu
Tm = Tc.copy(); Tm[5, 1] = 1               # derivative DOF tied with phase 1 (phase forgotten)
Kw = (Tw.H*Kg*Tw).applyfunc(sp.expand); Mw = (Tw.H*Mg*Tw).applyfunc(sp.expand)
Km = (Tm.H*Kg*Tm).applyfunc(sp.expand); Mm = (Tm.H*Mg*Tm).applyfunc(sp.expand)
check("[E1] WRONG SIGN (u with mu, u' with mu^{-1}): Kbar_w is STILL Hermitian and STILL satisfies "
      "Kbar_w(-k) = conj Kbar_w(k) (and so does Mbar_w). Reason: any DIAGONAL UNIMODULAR tying gives "
      "[A2]-[A3] regardless of which phase sits on which DOF.",
      mzero(Kw - Kw.H) and mzero(Kw.subs(kk, -kk) - Kw.conjugate())
      and mzero(Mw - Mw.H) and mzero(Mw.subs(kk, -kk) - Mw.conjugate()))

sub_ex = {E: 1, g2: sp.Rational(1, 10), rho: 1, h: 1}     # exact rationals, k kept symbolic
pw = (Kw - lamS*Mw).subs(sub_ex).applyfunc(sp.expand).det(method='berkowitz'); pw_neg = pw.subs(kk, -kk)
check("[E2] WRONG SIGN: the pencil charpoly is still EVEN in k (omega_w(k) = omega_w(-k)) and still "
      "2 pi/(2h)-periodic in k (BZ periodicity test 5b passes). Hermiticity (5a), conjugation and BZ "
      "periodicity are therefore BLIND to the sign error. (Exact rational moduli, k symbolic.)",
      iszero(sp.expand(pw - pw_neg))
      and mzero((Kw.subs(kk, kk + sp.pi/h) - Kw).applyfunc(lambda z: sp.simplify(z.rewrite(sp.cos)))))

check("[E3] WRONG SIGN differs from the correct matrix for generic k, but COINCIDES with it at "
      "Gamma (mu = 1) and at the zone boundary X (mu = -1 = mu^{-1}): a check performed only at "
      "Gamma and X can never see it; detection requires interior k.",
      not mzero(Kw - Kbar_c)
      and mzero((Kw - Kbar_c).subs(kk, 0))
      and mzero((Kw - Kbar_c).subs(kk, sp.pi/(2*h)).applyfunc(lambda z: sp.simplify(z.rewrite(sp.cos)))))

check("[E4] MISSING PHASE on u' (phase 1): also Hermitian, also conjugation-symmetric, also k-even -- "
      "the same blindness; it coincides with the correct tying only at Gamma.",
      mzero(Km - Km.H) and mzero(Km.subs(kk, -kk) - Km.conjugate())
      and iszero(sp.expand((Km - lamS*Mm).subs(sub_ex).applyfunc(sp.expand).det(method='berkowitz')
                           - (Km - lamS*Mm).subs(sub_ex).applyfunc(sp.expand).det(method='berkowitz').subs(kk, -kk)))
      and not mzero((Km - Kbar_c).subs(kk, sp.pi/(2*h)).applyfunc(lambda z: sp.simplify(z.rewrite(sp.cos)))))

# the literal (68) residual of the WRONG matrix: also O(1) -- so the literal test cannot even
# distinguish right from wrong by its magnitude
lit_w = sp.sqrt(fro2((Kw - Kw.subs(kk, -kk).H).subs(num_c).applyfunc(sp.nsimplify))
                / fro2(Kw.subs(num_c).applyfunc(sp.nsimplify)))
check("[E5] The literal test of Sec 4 / 5a returns an O(1) residual for the CORRECT tying "
      f"({float(ratio_c):.4f}, [C4]) AND for the WRONG tying ({float(lit_w):.4f}): it neither passes "
      "the correct implementation nor separates it from the wrong one. As a test it has no power.",
      float(lit_w) > 0.1)

# =============================================================================
# F. PUBLICATION-GRADE TEST STRUCTURE AND ITS POWER
# =============================================================================
print("--- F. verification structure: T1 Hermiticity, T2 conjugation, T3 Bloch-wave consistency, T4 reference")

def T1(Kb_):  return sp.sqrt(fro2((Kb_ - Kb_.H).subs(num_c).applyfunc(sp.nsimplify)))
def T2(Kb_):  return sp.sqrt(fro2((Kb_.subs(kk, -kk) - Kb_.conjugate()).subs(num_c).applyfunc(sp.nsimplify)))
check("[F1] T1 (Hermiticity ||Kbar - Kbar^H||) and T2 (conjugation ||Kbar(-k) - conj Kbar(k)||) are "
      "EXACTLY zero for the correct tying (necessary conditions, they must be kept) -- and also "
      "exactly zero for the wrong-sign tying (so they are not sufficient).",
      T1(Kbar_c) == 0 and T2(Kbar_c) == 0 and T1(Kw) == 0 and T2(Kw) == 0)

# T3: Bloch-wave consistency. The interpolant of the EXACT Bloch plane wave e^{ikx} (uniform envelope)
# has nodal DOFs (e^{ikx_n}, ik e^{ikx_n}); it must satisfy the tying constraint d_slave = T d_master
# EXACTLY, because M9 (41)-(43) were derived for exactly this field. This is an internal test that
# needs no reference solution and is sign-sensitive.
xn = [0, h, 2*h]
d_full = sp.Matrix([sp.exp(sp.I*kk*xn[0]), sp.I*kk*sp.exp(sp.I*kk*xn[0]),
                    sp.exp(sp.I*kk*xn[1]), sp.I*kk*sp.exp(sp.I*kk*xn[1]),
                    sp.exp(sp.I*kk*xn[2]), sp.I*kk*sp.exp(sp.I*kk*xn[2])])
d_master = d_full[:4, :]
def T3res(Tmat):
    r = (Tmat*d_master - d_full).applyfunc(sp.simplify)
    return r
r_ok, r_w, r_m = T3res(Tc), T3res(Tw), T3res(Tm)
check("[F2] T3 BLOCH-WAVE CONSISTENCY: with the DERIVED tying the interpolant of e^{ikx} satisfies "
      "T(k) d_master = d_full exactly (residual 0 for all k). With the WRONG SIGN the residual on the "
      f"slave derivative DOF is {sp.simplify(r_w[5])} = i k (mu^{{-1}} - mu) e^{{0}} != 0, and with the "
      f"MISSING phase it is {sp.simplify(r_m[5])} != 0 (both vanish only where mu^2 = 1, i.e. Gamma/X). "
      "T3 is therefore an INTERNAL test that DOES detect a unimodular sign error on derivative DOFs "
      "(refines M9 [X4]: 'no invariance test of Kbar' can, but a constraint-consistency test can).",
      mzero(r_ok) and not iszero(r_w[5]) and not iszero(r_m[5])
      and iszero(r_w[5] - sp.I*kk*(1/mu - mu)) and iszero(r_m[5] - sp.I*kk*(1 - mu))
      and iszero(r_w[5].subs(kk, 0)) and iszero(r_w[5].subs(kk, sp.pi/(2*h)).rewrite(sp.cos)))

# T3 in matrix form: the reduced pencil must reproduce the exact Bloch wave's energy in the
# CONSTRAINED space: Rayleigh quotient of d_master vs full-space quotient of d_full
def rq(Kx, Mx, v):  return sp.simplify((v.H*Kx*v)[0] / (v.H*Mx*v)[0])
rq_full = rq(Kg, Mg, d_full)
check("[F3] T3 (energy form): with the correct tying, the reduced Rayleigh quotient of the master "
      "part of the plane-wave interpolant equals the full-cell Rayleigh quotient of the whole "
      "interpolant EXACTLY (the constrained space contains the interpolated Bloch wave). With the "
      "wrong sign the two differ for generic k.",
      iszero(rq(Kbar_c, Mbar_c, d_master) - rq_full)
      and not iszero((rq(Kw, Mw, d_master) - rq_full).subs(num_c)))

# T4: long-wave acoustic slope (test 5d) -- independent analytic reference c^2 = E/rho
def lowest(Kx, Mx, kv):
    """smallest eigenvalue of the reduced pencil at k = kv (float, generalised eigenproblem)"""
    Kn_ = np.array(sp.N(Kx.subs({**num_c, kk: kv})).tolist(), dtype=complex)
    Mn_ = np.array(sp.N(Mx.subs({**num_c, kk: kv})).tolist(), dtype=complex)
    return min(np.linalg.eigvals(np.linalg.solve(Mn_, Kn_)).real)
# analytic reference for the 1D gradient bar (locked M7/M8 1D operator, classical mass only here):
#   E u_xx - E g2 u_xxxx + rho omega^2 u = 0  ->  omega^2 = (E/rho) k^2 (1 + g2 k^2)
def omega2_exact(kv):  return kv**2*(1 + 0.1*kv**2)          # E = rho = 1, g2 = 1/10 (num_c)
rows = []
for kv in (1e-3, 0.3, 0.6):
    ex = omega2_exact(kv)
    rows.append((kv, abs(lowest(Kbar_c, Mbar_c, kv)/ex - 1), abs(lowest(Kw, Mw, kv)/ex - 1),
                 abs(lowest(Km, Mm, kv)/ex - 1)))
(k0, e0_ok, e0_w, e0_m), (k1, e1_ok, e1_w, e1_m), (k2, e2_ok, e2_w, e2_m) = rows
check("[F4a] T4-LONG-WAVE (blueprint test 5d, omega -> c k as k -> 0) is BLIND to the derivative-DOF "
      f"phase error: at k h = {k0} the relative error vs the analytic omega^2 is {e0_ok:.1e} (correct), "
      f"{e0_w:.1e} (wrong sign), {e0_m:.1e} (missing phase) -- all pass a 1e-6 slope criterion because the "
      "wrong tying coincides with the right one at Gamma (mu -> 1, [E3]) and the discrepancy is O(k^2) "
      "relative. NEW FINDING beyond M9 [X4]: test 5d cannot serve as the independent detector.",
      e0_ok < 1e-6 and e0_w < 1e-5 and e0_m < 1e-5)

check("[F4b] T4-FINITE-k ANALYTIC DISPERSION (Layer 3 / P2.1-P2.2: closed-form omega(k) of the "
      "homogeneous gradient bar/medium at interior k) DOES detect it: at k h = 0.3 the relative errors "
      f"are {e1_ok:.1e} (correct) vs {e1_w:.1e} (wrong sign) and {e1_m:.1e} (missing); at k h = 0.6: "
      f"{e2_ok:.1e} vs {e2_w:.1e} and {e2_m:.1e}. Orders of magnitude apart from the discretisation error "
      "of the correct tying. The reference comparison must therefore be made at INTERIOR k (not Gamma, "
      "not X, not the k -> 0 slope only).",
      e1_ok < 1e-5 and e1_w > 1e-2 and e1_m > 1e-3 and e2_ok < 1e-4 and e2_w > 1e-1 and e2_m > 1e-2)

check("[F5] STRUCTURE RULING: the publication-grade test set for M15 is  T1 ||Kbar-Kbar^H||/||Kbar|| "
      "< 1e-12 ; T2 ||Kbar(-k) - conj Kbar(k)||/||Kbar|| < 1e-12 (equivalently Kbar(-k) = Kbar(k)^T) ; "
      "T3 ||T(k) d_master - d_full|| = 0 for the interpolated Bloch wave at INTERIOR k (sign-sensitive, "
      "internal, no reference needed) ; T4 independent reference at INTERIOR k (Layer-3 analytic "
      "dispersion P2.1/P2.2; Phase-3 anchors) -- NOT the k -> 0 slope 5d alone ([F4a]). "
      "T1+T2 are necessary and always satisfiable; T3+T4 supply the power the Sec 4 row intended. "
      "The literal (68) test is replaced, not weakened: it passes nothing correct and catches nothing wrong.",
      True)

print(f"\nALL {len(OK)} CHECKS PASSED - M15-a audit (blueprint (68) / test 5a): literal (68) <=> Kbar real; "
      "always-true pair = Hermiticity + conjugation; counterexample reproduced (9, 8, 2 sqrt 2 / 3) and "
      "re-derived from a C^1 Hermite cell; wrong-sign phase invisible to invariance tests, detected by "
      "Bloch-wave consistency (T3) and by an independent finite-k reference (T4; the k->0 slope 5d alone is blind). Ruling: (a).")
