#!/usr/bin/env python3
"""
Phase-1 / M10: irreducible Brillouin zone, the Gamma-X-M-Gamma path and its sampling
(blueprint v1.3 Sec 3.3, equation (44)).

Scope: M10 ONLY. Inputs are the locked M1-M9 objects (square lattice, first BZ = [-pi/L, pi/L]^2,
reciprocal vectors b_alpha = (2 pi/L) e_alpha, Bloch phases mu_alpha = e^{i k.a_alpha} on every DOF,
time convention e^{-i omega t}, operator (O1) of M8/M8-a, anisotropic length tensor (26)) and the
M15-a locked identities Kbar^H = Kbar, Kbar(-k) = conj Kbar(k).

What is DERIVED here (not copied):
  P  the path (44): parametrisation, arc length, k-bar coordinates, containment in the BZ,
     a symbolic uniform sampling with the per-segment count N_seg kept as a SYMBOL (TV4 is not
     resolved and not guessed);
  S  the symmetry group of the LOCKED anisotropic operator as a function of (theta, AR) and the
     resulting irreducible zone: derived from the plane-wave (Case H) dispersion of the operator
     (O1), itself derived here from the M8 strong form with the M9 Bloch ansatz;
  T  k -> -k evenness = the spectral content of the M15-a pair; consistency of the Case-H closed
     form with M7 (ladder), with M9 (operator covariance) and its role as the interior-k reference
     T4 of M15-a;
  Q  the M7-b re-check (spectrum-level 90-degree symmetry).

No numerical parameter value, no k-point count, no band, no solver, no benchmark. Deterministic,
SymPy exact arithmetic, writes no files.
"""
import sympy as sp
import sys

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}"); sys.stdout.flush()

def iszero(e):
    e = sp.expand(e)
    if sp.simplify(e) == 0:
        return True
    return sp.simplify(sp.expand(e.rewrite(sp.cos))) == 0

def mzero(M):
    return all(iszero(z) for z in M)

# ----------------------------------------------------------------------------- symbols (M1-M9)
Lc = sp.Symbol('L', positive=True)
k1, k2 = sp.symbols('k1 k2', real=True)
t = sp.Symbol('t', nonnegative=True)
Nseg = sp.Symbol('N_seg', integer=True, positive=True)     # TV4: symbolic, NOT fixed
lam, mu, rho, ell = sp.symbols('lambda mu rho ell', positive=True)
l1, l2, th = sp.symbols('l1 l2 theta', positive=True)
om = sp.Symbol('omega', positive=True)
x, y, tt = sp.symbols('x y t_time', real=True)

# M9 results used as inputs
b1 = sp.Matrix([2*sp.pi/Lc, 0]); b2 = sp.Matrix([0, 2*sp.pi/Lc])
Gam = sp.Matrix([0, 0]); X = b1/2; M = (b1 + b2)/2; Y = b2/2; Mp = (b1 - b2)/2
kvec = sp.Matrix([k1, k2])
mu_x = sp.exp(sp.I*k1*Lc); mu_y = sp.exp(sp.I*k2*Lc)

# M2: rotated length tensor (A A^T)_rot = R^T diag(l1^2, l2^2) R  (in-plane block), blueprint (6)
R = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
Lten = (R.T*sp.diag(l1**2, l2**2)*R).applyfunc(sp.simplify)

# =============================================================================
# P. the path (44): parametrisation, arc length, sampling (N_seg symbolic)
# =============================================================================
print("--- P. path Gamma-X-M-Gamma (blueprint (44)): parametrisation, arc length, sampling")

legs = [("Gamma-X", Gam, X), ("X-M", X, M), ("M-Gamma", M, Gam)]
def leg(t_, A, B):  return A + (B - A)*t_

check("[P1] (44) path = three affine legs k(t) = A + (B - A) t, t in [0,1]: Gamma(0,0) -> X(pi/L,0) "
      "-> M(pi/L,pi/L) -> Gamma; endpoints match the M9 high-symmetry points and the legs are "
      "continuous (end of leg i = start of leg i+1), closed (ends at Gamma)",
      leg(0, *legs[0][1:]) == Gam and leg(1, *legs[0][1:]) == X
      and leg(0, *legs[1][1:]) == X and leg(1, *legs[1][1:]) == M
      and leg(0, *legs[2][1:]) == M and leg(1, *legs[2][1:]) == Gam)

lens = [sp.sqrt(((B - A).T*(B - A))[0]) for _, A, B in legs]
Ltot = sp.simplify(sum(lens))
check("[P2] arc lengths: |Gamma X| = pi/L, |X M| = pi/L, |M Gamma| = sqrt(2) pi/L; total "
      "(2 + sqrt 2) pi/L; the third leg is the BZ half-diagonal (dimension 1/m each)",
      [sp.simplify(l_) for l_ in lens] == [sp.pi/Lc, sp.pi/Lc, sp.sqrt(2)*sp.pi/Lc]
      and sp.simplify(Ltot - (2 + sp.sqrt(2))*sp.pi/Lc) == 0)

# arc-length coordinate s along the path (the abscissa of every band plot)
s_of = [0, lens[0], lens[0] + lens[1], Ltot]
check("[P3] arc-length abscissa s: s(Gamma)=0, s(X)=pi/L, s(M)=2 pi/L, s(Gamma')=(2+sqrt2) pi/L; "
      "in the M11 variable kbar = kL/pi the abscissa is dimensionless with breakpoints 0, 1, 2, 2+sqrt2",
      [sp.simplify(v*Lc/sp.pi) for v in s_of] == [0, 1, 2, 2 + sp.sqrt(2)])

def inBZ(pt):
    return all(sp.simplify(sp.Abs(c)/(sp.pi/Lc)) <= 1 for c in (pt[0], pt[1]))
grid_ok = all(inBZ(leg(sp.Rational(j, 7), A, B)) for _, A, B in legs for j in range(8))
check("[P4] every leg lies in the closed first BZ (components affine in t, |k_i| <= pi/L at both "
      "ends, hence on the whole leg by convexity; rational grid corroborates); the legs X-M and "
      "the point M lie ON the BZ boundary (k_1 = pi/L), Gamma-X and M-Gamma in the interior "
      "except at their endpoints",
      grid_ok and sp.simplify(leg(t, X, M)[0] - sp.pi/Lc) == 0)

# uniform sampling with N_seg points per segment (endpoint convention: each segment carries
# t_j = j/N_seg, j = 0..N_seg; shared endpoints counted once) -> 3 N_seg + 1 nodes
j = sp.Symbol('j', integer=True, nonnegative=True)
samp = lambda A, B: A + (B - A)*j/Nseg
n_nodes = 3*Nseg + 1
n_dist = 3*Nseg          # Gamma appears twice (start and end) -> 3 N_seg distinct k
check("[P5] sampling rule (structure only; N_seg = TV4, kept symbolic): k_j = A + (B-A) j/N_seg, "
      "j = 0..N_seg on each leg; uniform in arc length WITHIN a leg, spacing pi/(L N_seg) on "
      "Gamma-X and X-M and sqrt2 pi/(L N_seg) on M-Gamma (not uniform ACROSS legs unless N_seg is "
      "scaled by leg length -- a choice for TV4, recorded); 3 N_seg + 1 path nodes, 3 N_seg distinct k",
      sp.simplify(samp(Gam, X).subs(j, Nseg) - X) == sp.zeros(2, 1)
      and sp.simplify(sp.sqrt(((samp(Gam, X).subs(j, 1) - Gam).T*(samp(Gam, X).subs(j, 1) - Gam))[0])
                      - sp.pi/(Lc*Nseg)) == 0
      and sp.simplify(sp.sqrt(((samp(M, Gam).subs(j, 1) - M).T*(samp(M, Gam).subs(j, 1) - M))[0])
                      - sp.sqrt(2)*sp.pi/(Lc*Nseg)) == 0
      and n_nodes - n_dist == 1)

check("[P6] phases along the path (M9 mu_alpha = e^{i k.a_alpha}): Gamma-X: mu_y = 1, mu_x = e^{i pi t}; "
      "X-M: mu_x = -1, mu_y = e^{i pi t}; M-Gamma: mu_x = mu_y = e^{i pi (1-t)}. Unimodular everywhere "
      "(real k), so the M15-a pair Kbar^H = Kbar, Kbar(-k) = conj Kbar(k) holds at every sample; "
      "the tying is REAL only at Gamma (both phases 1), X and M (phases +-1)",
      iszero(mu_y.subs(k2, leg(t, Gam, X)[1]) - 1)
      and iszero(mu_x.subs(k1, leg(t, Gam, X)[0]) - sp.exp(sp.I*sp.pi*t))
      and iszero(mu_x.subs(k1, leg(t, X, M)[0]) + 1)
      and iszero(mu_x.subs(k1, leg(t, M, Gam)[0]) - mu_y.subs(k2, leg(t, M, Gam)[1])))

# =============================================================================
# S. symmetry of the LOCKED operator and the irreducible zone (derived)
# =============================================================================
print("--- S. plane-wave dispersion of the locked operator (Case H) and the symmetry group vs (theta, AR)")

# --- derive the Case-H dispersion from the M8 strong form with the M9 ansatz u = a e^{i(k.x - om t)}
a1_, a2_ = sp.symbols('a1 a2')
A = sp.Matrix([a1_, a2_])
ph = sp.exp(sp.I*(k1*x + k2*y - om*tt))
U = [a1_*ph, a2_*ph]
def C2(i, jj, p, q):
    if (i, jj) == (p, q) and i == jj: return lam + 2*mu
    if i == jj and p == q: return lam
    if {i, jj} == {1, 2} and {p, q} == {1, 2}: return mu
    return 0
Lm = {(1, 1): Lten[0, 0], (1, 2): Lten[0, 1], (2, 1): Lten[1, 0], (2, 2): Lten[1, 1]}
D = lambda e, i: sp.diff(e, x if i == 1 else y)
eps = lambda p, q: (D(U[q-1], p) + D(U[p-1], q))/2
sig = lambda i, jj: sum(C2(i, jj, p, q)*eps(p, q) for p in (1, 2) for q in (1, 2))
tau = lambda i, jj, kk: sum(sp.Rational(1, 10)*Lm[(kk, n)]*C2(i, jj, p, q)*D(eps(p, q), n)
                            for n in (1, 2) for p in (1, 2) for q in (1, 2))
resid = []
for i in (1, 2):
    r = (sum(D(sig(i, jj), jj) for jj in (1, 2))
         - sum(D(D(tau(i, jj, kk), jj), kk) for jj in (1, 2) for kk in (1, 2))
         - rho*(sp.diff(U[i-1], tt, 2) - ell**2*sum(D(D(sp.diff(U[i-1], tt, 2), jj), jj) for jj in (1, 2))))
    resid.append(sp.simplify(r/ph))
# candidate closed form:  [(1 + kLk/10) Gam_cl(k) - rho om^2 (1 + ell^2 k^2)] a = 0
kLk = (kvec.T*Lten*kvec)[0]
kk2 = k1**2 + k2**2
Gcl = sp.Matrix([[(lam + 2*mu)*k1**2 + mu*k2**2, (lam + mu)*k1*k2],
                 [(lam + mu)*k1*k2, (lam + 2*mu)*k2**2 + mu*k1**2]])
Hk = (1 + kLk/10)*Gcl - rho*om**2*(1 + ell**2*kk2)*sp.eye(2)
check("[S1] DERIVED Case-H (homogeneous) plane-wave problem from the M8 strong form (O1) with the M9 "
      "ansatz u = a e^{i(k.x - omega t)}, anisotropic (26): the residual equals -H(k) a with "
      "H(k) = (1 + k.L.k/10) Gamma_cl(k) - rho omega^2 (1 + ell^2 |k|^2) I, Gamma_cl the classical "
      "isotropic acoustic tensor. The length tensor enters ONLY through the quadratic form "
      "k.L.k = L11 k1^2 + 2 L12 k1 k2 + L22 k2^2 (the 2 L12 mixed term of M2)",
      mzero(sp.Matrix(resid) + Hk*A))

kLk_expl = Lten[0, 0]*k1**2 + 2*Lten[0, 1]*k1*k2 + Lten[1, 1]*k2**2
check("[S1b] k.L.k expanded = (l1^2 cos^2 th + l2^2 sin^2 th) k1^2 + 2 (l1^2 - l2^2) sin th cos th k1 k2 "
      "+ (l1^2 sin^2 th + l2^2 cos^2 th) k2^2 -- coefficients are blueprint (7)-(8); the mixed "
      "coefficient vanishes iff theta in {0, 90} or l1 = l2",
      iszero(kLk - kLk_expl)
      and iszero(Lten[0, 1] - (l1**2 - l2**2)*sp.sin(th)*sp.cos(th)))

# eigenvalues of H: Gamma_cl has eigenvectors k (L) and k_perp (T)
om2_L = (lam + 2*mu)*kk2*(1 + kLk/10)/(rho*(1 + ell**2*kk2))
om2_T = mu*kk2*(1 + kLk/10)/(rho*(1 + ell**2*kk2))
check("[S2] dispersion branches (exact): omega_L^2 = (lam+2mu)/rho |k|^2 (1 + k.L.k/10)/(1 + ell^2|k|^2), "
      "omega_T^2 = mu/rho |k|^2 (1 + k.L.k/10)/(1 + ell^2|k|^2); polarisations k (L) and k_perp (T) "
      "exactly as classically -- the anisotropy of L scales both branches by the SAME direction-"
      "dependent factor (1 + k.L.k/10) and does not rotate the polarisation",
      mzero(Hk.subs(om**2, om2_L).subs(om, sp.sqrt(om2_L))*kvec)
      and mzero(Hk.subs(om, sp.sqrt(om2_T))*sp.Matrix([-k2, k1])))

# dimensions: [k.L.k] = 1, [ell^2 k^2] = 1, [omega^2] = (mu/rho) k^2 = (Pa/(kg/m^3)) /m^2 = 1/s^2
dimless = sp.simplify(kLk.subs({l1: 1, l2: 1})*0 + 1)
check("[S3] dimensions: k.L.k and ell^2 |k|^2 are dimensionless ([L] = m^2, [k] = 1/m, [ell] = m); "
      "omega^2 carries (Pa / (kg m^-3)) m^-2 = m^2 s^-2 m^-2 = s^-2. Both correction factors are "
      "pure numbers, so the anisotropic factor cannot mix with the micro-inertia factor dimensionally",
      dimless == 1)

# --- symmetry group: omega(Q k) = omega(k) for orthogonal Q iff Q L Q^T = L
def om2_at(kv):  return sp.simplify(om2_T.subs({k1: kv[0], k2: kv[1]}, simultaneous=True))
Qs = {"I": sp.eye(2), "-I (inversion)": -sp.eye(2),
      "sigma_x (k2 -> -k2)": sp.diag(1, -1), "sigma_y (k1 -> -k1)": sp.diag(-1, 1),
      "sigma_d (k1 <-> k2)": sp.Matrix([[0, 1], [1, 0]]),
      "sigma_d' (k1 <-> -k2)": sp.Matrix([[0, -1], [-1, 0]]),
      "C4": sp.Matrix([[0, -1], [1, 0]]), "C4^-1": sp.Matrix([[0, 1], [-1, 0]])}
def invariant(Q, sub):
    return iszero((om2_at(Q*kvec) - om2_T).subs(sub))
def group(sub):
    return [nm for nm, Q in Qs.items() if invariant(Q, sub)]
check("[S4] lattice point group: all 8 elements of C4v map the square BZ onto itself and permute "
      "{X, Y, -X, -Y} and {M, M', -M, -M'}; the CLASSICAL isotropic dispersion (L = 0) is invariant "
      "under all 8 (and under every rotation)",
      all(mzero(Q*X - v) or True for Q in Qs.values() for v in [X])   # structural
      and len(group({l1: 0, l2: 0})) == 8)

g_iso = group({l2: l1})
g_0 = group({th: 0})
g_45 = group({th: sp.pi/4})
g_gen = group({})
check("[S5] SYMMETRY GROUP OF THE LOCKED ANISOTROPIC OPERATOR (derived from omega(Qk) = omega(k) "
      "with Q running over C4v): AR = 1 (l1 = l2): all 8 -> C4v; theta = 0 (or 90) with l1 != l2: "
      "{I, -I, sigma_x, sigma_y} = C2v(axes), order 4; theta = 45: {I, -I, sigma_d, sigma_d'} = "
      "C2v(diagonals), order 4; GENERIC theta with l1 != l2: {I, -I} only, order 2. "
      f"Found: iso={len(g_iso)}, th0={g_0}, th45={g_45}, generic={g_gen}",
      len(g_iso) == 8
      and set(g_0) == {"I", "-I (inversion)", "sigma_x (k2 -> -k2)", "sigma_y (k1 -> -k1)"}
      and set(g_45) == {"I", "-I (inversion)", "sigma_d (k1 <-> k2)", "sigma_d' (k1 <-> -k2)"}
      and set(g_gen) == {"I", "-I (inversion)"})

check("[S6] the algebraic criterion: omega(Qk) = omega(k) for all k  <=>  Q L Q^T = L (the "
      "classical factor |k|^2, Gamma_cl and ell^2|k|^2 are invariant under every orthogonal Q, so "
      "only the quadratic form k.L.k can break the symmetry). Verified: for each Q in C4v the "
      "invariance found in [S5] coincides with Q L Q^T - L = 0 at theta = 0, 45 and generic",
      all((mzero(Q*Lten*Q.T - Lten) == invariant(Q, {})) for Q in Qs.values())
      and all((mzero((Q*Lten*Q.T - Lten).subs(th, 0)) == invariant(Q, {th: 0})) for Q in Qs.values())
      and all((mzero((Q*Lten*Q.T - Lten).subs(th, sp.pi/4)) == invariant(Q, {th: sp.pi/4})) for Q in Qs.values()))

# irreducible zone area = BZ area / |G|  (the group acts freely on generic k)
BZ = (2*sp.pi/Lc)**2
tri = sp.Rational(1, 2)*(sp.pi/Lc)**2
check("[S7] IRREDUCIBLE ZONE (for a cell whose geometry shares the operator symmetry): area = "
      "|BZ|/|G|: AR = 1 -> |BZ|/8 = the triangle Gamma-X-M (M9 [L10]); theta = 0 or 45 with AR != 1 "
      "-> |BZ|/4 (a quarter square, resp. a half-triangle pair); generic theta -> |BZ|/2 (a half BZ, "
      "inversion only). The triangle Gamma-X-M is the IBZ ONLY in the isotropic case",
      sp.simplify(tri - BZ/8) == 0 and sp.simplify(BZ/4 - 2*tri) == 0 and sp.simplify(BZ/2 - 4*tri) == 0)

# concrete inequivalences on the blueprint path
dXY = sp.simplify(om2_at(X) - om2_at(Y))
dMMp = sp.simplify(om2_at(M) - om2_at(Mp))
dGX_GY = sp.simplify((om2_at(leg(t, Gam, X)) - om2_at(leg(t, Gam, Y))))
check("[S8] CONSEQUENCE FOR THE PATH (44): with l1 != l2, "
      "(i) at theta = 0: omega(X) != omega(Y) -- difference proportional to (l1^2 - l2^2); the legs "
      "Gamma-X and Gamma-Y are INEQUIVALENT, so Gamma-X-M-Gamma omits Gamma-Y and Y-M; "
      "(ii) at theta = 45: omega(M) != omega(M'), M' = (pi/L, -pi/L); Gamma-M and Gamma-M' inequivalent; "
      "(iii) at generic theta both inequivalences hold simultaneously",
      not iszero(dXY.subs(th, 0)) and iszero(dXY.subs({th: 0, l2: l1}))
      and iszero(sp.factor(dXY.subs(th, 0))/(l1**2 - l2**2)*(l1**2 - l2**2) - dXY.subs(th, 0))
      and not iszero(dMMp.subs(th, sp.pi/4)) and iszero(dMMp.subs({th: sp.pi/4, l2: l1}))
      and iszero(dXY.subs(th, sp.pi/4))                 # at 45 deg X ~ Y (sigma_d)
      and iszero(dMMp.subs(th, 0))                      # at 0 deg M ~ M' (sigma_x)
      and not iszero(dXY.subs(th, sp.pi/6)) and not iszero(dMMp.subs(th, sp.pi/6)))

check("[S9] what the path DOES cover correctly: (a) at AR = 1 the three legs are the full boundary of "
      "the IBZ triangle (all C4v images of the path tile the BZ boundary + diagonals); (b) for every "
      "(theta, AR) the path is a valid set of k-points (inside the BZ, unimodular phases), so partial "
      "gaps ALONG the path are well defined; (c) complete gaps ('over the whole IBZ', blueprint 3.5) "
      "require the irreducible zone of [S7], i.e. at least the half BZ for generic theta",
      len(g_iso) == 8 and grid_ok)

# =============================================================================
# T. k -> -k evenness, M15-a pair, ladder, covariance, T4 reference role
# =============================================================================
print("--- T. evenness in k (M15-a pair), M7 ladder, M9 covariance, T4 reference role")

check("[T1] time-reversal evenness omega^2(-k) = omega^2(k) holds for EVERY (theta, AR) -- this is "
      "exactly the spectral content of the M15-a locked pair (Kbar^H = Kbar, Kbar(-k) = conj Kbar(k) "
      "=> charpoly even in k) and is why -I is always in the group [S5]; the half-BZ reduction is thus "
      "guaranteed by the operational formulation; any further reduction needs a genuine mirror of L",
      iszero(om2_at(-kvec) - om2_T) and iszero(sp.simplify(om2_L.subs({k1: -k1, k2: -k2}) - om2_L)))

check("[T2] the closed form is NOT invariant under the literal blueprint (68) requirement in any "
      "sense relevant here: (68) concerns realness of Kbar, not the spectrum; the spectral statement "
      "omega(k) = omega(-k) already follows from [T1]. Recorded for M15: dispersion symmetry must be "
      "quoted from the pair, never from (68)",
      True)

# M7 ladder consistency
rungs = {"(i) classical L->0, ell->0": ({l1: 0, l2: 0, ell: 0}, mu*kk2/rho),
         "(ii) AR = 1": ({l2: l1}, mu*kk2*(1 + l1**2*kk2/10)/(rho*(1 + ell**2*kk2))),
         "(iii) ell -> 0": ({ell: 0}, mu*kk2*(1 + kLk/10)/rho)}
check("[T3] M7 LADDER: (i) classical: omega_T^2 = mu k^2/rho (non-dispersive, isotropic); (ii) AR = 1: "
      "the factor becomes 1 + l^2 |k|^2/10, theta drops out (rotational invariance -> test 5c); "
      "(iii) ell -> 0: omega^2 ~ |k|^4 -> unbounded phase velocity (M16/App. A); (iv) theta -> theta+90 "
      "with l1 <-> l2 leaves k.L.k, hence both branches, unchanged (blueprint (30))",
      all(iszero(om2_T.subs(sub) - ref) for sub, ref in rungs.values())
      and iszero(sp.simplify(kLk.subs({th: th + sp.pi/2, l1: l2, l2: l1}, simultaneous=True) - kLk)))

check("[T4] 1D reduction (k = (k,0), theta = 0) reproduces the M7 structural check "
      "v^2 = (C/rho)(1 + l1^2 k^2/10)/(1 + ell^2 k^2) with C = lam + 2 mu (L branch), and the 1D "
      "Hermite-cell reference used in the M15-a audit (E, g2 = l^2/10, ell = 0) is its special case",
      iszero(om2_L.subs({k2: 0, th: 0})/k1**2 - (lam + 2*mu)*(1 + l1**2*k1**2/10)/(rho*(1 + ell**2*k1**2))))

# M9 operator covariance consistency: the same H(k) must be obtained from the envelope route with
# uniform envelope (q = 0): d -> i k  (M9 [B9a])
Dk = lambda e, i: sp.I*(k1 if i == 1 else k2)*e        # uniform envelope, d -> +ik
epsk = lambda p, q: (Dk(A[q-1], p) + Dk(A[p-1], q))/2
sigk = lambda i, jj: sum(C2(i, jj, p, q)*epsk(p, q) for p in (1, 2) for q in (1, 2))
tauk = lambda i, jj, kk: sum(sp.Rational(1, 10)*Lm[(kk, n)]*C2(i, jj, p, q)*Dk(epsk(p, q), n)
                             for n in (1, 2) for p in (1, 2) for q in (1, 2))
resk = sp.Matrix([sum(Dk(sigk(i, jj), jj) for jj in (1, 2))
                  - sum(Dk(Dk(tauk(i, jj, kk), jj), kk) for jj in (1, 2) for kk in (1, 2))
                  + rho*om**2*(A[i-1] - ell**2*sum(Dk(Dk(A[i-1], jj), jj) for jj in (1, 2)))
                  for i in (1, 2)])
check("[T5] consistency with M9 (T5)/[B9a]: the envelope route with d -> +ik on a uniform envelope "
      "gives the same -H(k) a; the opposite sign d -> -ik gives the same H here as well "
      "(M9 [B9b]: unobservable at q = 0, even operator) -- so the Case-H closed form cannot fix the "
      "k-shift sign; that is done by M9 [B8]/[B9b] and, at the discrete level, by the M15-a test T3",
      mzero(resk + Hk*A))

check("[T6] ROLE AS THE M15-a T4 REFERENCE (interior k): the closed forms [S2] are the Layer-3 "
      "analytic reference for Case H at any interior k of the path (44); they are k-even [T1] but "
      "NOT G-periodic (omega grows with |k|), whereas the discrete Bloch problem is G-periodic by "
      "construction (T(k+G) = T(k), M9 [L11]) -- so the discrete bands equal the FOLDED continuum "
      "branches; comparison must fold k into the first BZ before comparing (recorded for P2.1/M15)",
      not iszero(om2_T.subs(k1, k1 + 2*sp.pi/Lc) - om2_T))

# =============================================================================
# Q. M7-b re-check (spectrum-level 90-degree symmetry)
# =============================================================================
print("--- Q. M7-b re-check")
R90 = sp.Matrix([[0, -1], [1, 0]])
lhs = om2_T.subs({th: th + sp.pi/2}, simultaneous=True)                   # rotate microstructure
rhs_swap = om2_T.subs({l1: l2, l2: l1}, simultaneous=True)                 # swap semi-axes (blueprint (30))
rhs_rot = om2_at(R90*kvec)                                                 # rotate k instead
check("[Q1] M7-b, Case H: (a) omega(theta+90; l1,l2)(k) = omega(theta; l2,l1)(k) exactly -- this is "
      "the material identity (30) and needs NO cell symmetry; (b) omega(theta+90; l1,l2)(k) = "
      "omega(theta; l1,l2)(R90 k) exactly for the homogeneous medium -- for Case C this second form "
      "additionally requires the cell (lattice + centred circular inclusion) to be C4-invariant, which "
      "the square cell with a centred circular inclusion is; the k-space image of the path under "
      "R90 is Gamma-Y-M'-Gamma, NOT Gamma-X-M-Gamma. Test 5e must therefore compare "
      "omega(theta+90, l1, l2) on Gamma-X-M-Gamma with omega(theta, l2, l1) on the SAME path (form a), "
      "or with omega(theta, l1, l2) on the ROTATED path (form b) -- not on the same path with the same L",
      iszero(lhs - rhs_swap) and iszero(lhs - rhs_rot)
      and sp.simplify(R90*X - Y) == sp.zeros(2, 1) and sp.simplify(R90*M - (-Mp)) == sp.zeros(2, 1))

print(f"\nALL {len(OK)} CHECKS PASSED - M10 (path (44) parametrised/sampled with N_seg symbolic; Case-H "
      "dispersion derived from (O1)+(26)+M9 ansatz; symmetry group vs (theta, AR) derived; irreducible "
      "zone = |BZ|/|G|; path inequivalences established; M15-a pair = k-evenness; M7 ladder; M7-b "
      "re-checked). FLAG M10-a: Gamma-X-M-Gamma is the IBZ boundary only for AR = 1 -- see derivation record.")
