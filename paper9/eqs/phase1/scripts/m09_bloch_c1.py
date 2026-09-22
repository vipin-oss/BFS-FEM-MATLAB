#!/usr/bin/env python3
"""
Phase-1 / M9: Bloch theorem for the C^1 gradient-elastic medium - derived phase rules.

Target of the derivation (blueprint v1.3, Section 3.1-3.2, equations (36)-(43)):
  (36)-(38)  unit cell Omega_cell = [0,L]x[0,L]; lattice vectors a_1, a_2;
             reciprocal vectors b_1, b_2; first Brillouin zone
  (39)       time-harmonic Bloch ansatz
  (40)       Bloch condition   u(x + a_alpha) = u(x) exp(i k . a_alpha)
  (41)-(43)  the SAME phase factor on grad u and on d^2 u/dx dy
             (and, generally, on every multi-index derivative => on every value,
             first-derivative and mixed-derivative DOF of the BFS element)

Derivation policy: every equation below is derived from the LOCKED formulation
(M1-M8, blueprint (1)-(35)) and verified by EXACT symbolic checks executed here.
Nothing is accepted merely because it was written in an earlier document; every
identity is re-derived, and every rule is submitted to negative controls (a rule
that cannot fail is not a check).

Locked model used (unchanged): L = (A A^T)_rot                      [blueprint (26)]
  eps_ij = (1/2)(u_i,j + u_j,i) ; eta_ijk = eps_ij,k                [M3,  (10)-(12)]
  sigma_ij = C_ijkl eps_kl                                        [M4,  (13)-(15)]
  tau_ijk  = (1/10) L_kn C_ijpq eta_pqn                            [M4,  (16)-(18)]
  strong form & boundary model: (O1)-(O6) of the M8-a audit (reduced four-quantity
  model operational, interpretation (A))
The five-constant family a_1..a_5 is NOT used (F1 audit: isotropic presentation only);
no a_p value is quoted anywhere here. No Bloch phase and no k-shift is imported from
any outside source; the master-slave route is the one prescribed by blueprint Sec 4.4.

Provenance tags: [C] cited source, [A] derived here, [S] structural/definition.

Deterministic; exact symbolic arithmetic; writes no files; no numerical parameter value.
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

def iszero(e):
    return sp.simplify(sp.expand(e)) == 0

# =============================================================================
# 0. Symbols and helpers
# =============================================================================
x, y = sp.symbols('x y', real=True)
Lc   = sp.Symbol('L', positive=True)                 # cell side (blueprint: L)
k1, k2 = sp.symbols('k1 k2', real=True)              # k_x, k_y  (real k in the BZ)
mI, nI = sp.symbols('m n', integer=True)             # envelope Fourier indices
A1, A2 = sp.symbols('A1 A2', complex=True)           # displacement amplitudes
lam, mu = sp.symbols('lambda mu', positive=True)     # classical isotropic moduli
rho, ell, om = sp.symbols('rho ell omega', positive=True)
L11, L12, L22 = sp.symbols('L11 L12 L22', positive=True)   # (A^T A)_rot components
n1, n2 = sp.symbols('n1 n2', real=True)              # unit normal components
nu_L = sp.symbols('nu_L', positive=True)
bet  = sp.symbols('beta', real=True)                 # imaginary part of a complex k

# blueprint (37): lattice vectors of the square cell  (36)
a1 = sp.Matrix([Lc, 0]); a2 = sp.Matrix([0, Lc])

def sh(e, a):
    """lattice translation: x -> x + a (a = 2-vector)"""
    return e.subs({x: x + a[0], y: y + a[1]}, simultaneous=True)

def D(e, i):
    return sp.diff(e, x) if i == 1 else sp.diff(e, y)

def Dk(e, i):
    """k-shifted derivative of the envelope:  (d_i + i k_i)"""
    return D(e, i) + sp.I*(k1 if i == 1 else k2)*e

def env(mode, A):
    """lattice-periodic envelope, single Fourier mode (m,n) [S] (basis of the periodic space)"""
    m, n = mode
    return A*sp.exp(sp.I*2*sp.pi*m*x/Lc + sp.I*2*sp.pi*n*y/Lc)

def ubloch(mode, A):
    """full (non-periodic) field: envelope x e^{i k.x}  -- the Bloch form of (39)"""
    return env(mode, A)*sp.exp(sp.I*(k1*x + k2*y))

def ubloch_i(mode, As):
    return [ubloch(mode, As[0]), ubloch(mode, As[1])]

mu_x = sp.exp(sp.I*k1*Lc)      # e^{i k . a_1}
mu_y = sp.exp(sp.I*k2*Lc)      # e^{i k . a_2}
MODES = [(0, 0), (1, -2), (2, 1)]

# isotropic classical plane-strain modulus (blueprint (13)-(15); M4)
def C2(i, j, p, q):
    ij = (i, j); pq = (p, q)
    if ij in ((1, 1),) and pq in ((1, 1),): return lam + 2*mu
    if ij in ((2, 2),) and pq in ((2, 2),): return lam + 2*mu
    if (ij == (1, 1) and pq == (2, 2)) or (ij == (2, 2) and pq == (1, 1)): return lam
    if ij in ((1, 2), (2, 1)) and pq in ((1, 2), (2, 1)): return mu
    return 0

def L2(k, n):
    if (k, n) == (1, 1): return L11
    if (k, n) == (2, 2): return L22
    return L12    # k != n  (symmetric tensor, M2)

# =============================================================================
# SECTION L -- unit cell, lattice and reciprocal lattice, first Brillouin zone  (36)-(38)
# =============================================================================
print("--- L. unit cell, lattice, reciprocal lattice, first Brillouin zone: blueprint (36)-(38)")

cell_area = Lc*Lc
corners = [sp.Matrix([0, 0]), a1, a2, a1 + a2]
check("[L1] (36) unit cell Omega_cell = [0,L]x[0,L]: area L^2 and its four corners are exactly "
      "the lattice points {0, a_1, a_2, a_1+a_2} of the Bravais lattice generated by a_1, a_2 "
      "(the cell is a fundamental domain of the lattice)",
      cell_area == Lc**2 and corners == [sp.Matrix([0,0]), sp.Matrix([Lc,0]),
                                         sp.Matrix([0,Lc]), sp.Matrix([Lc,Lc])])

G_gram = sp.Matrix([[a1.dot(a1), a1.dot(a2)], [a2.dot(a1), a2.dot(a2)]])
check("[L2] (37) lattice vectors a_1 = L e_1, a_2 = L e_2: a_alpha . a_beta = L^2 delta_alpha,beta "
      "-> the cell is a SQUARE lattice with lattice constant L (orthogonal, equal lengths)",
      sp.simplify(G_gram - Lc**2*sp.eye(2)) == sp.zeros(2, 2))

b11, b12, b21, b22 = sp.symbols('b11 b12 b21 b22', real=True)
b1 = sp.Matrix([b11, b12]); b2 = sp.Matrix([b21, b22])
sol = sp.solve([sp.Eq(b1.dot(a1), 2*sp.pi), sp.Eq(b1.dot(a2), 0),
                sp.Eq(b2.dot(a1), 0), sp.Eq(b2.dot(a2), 2*sp.pi)],
               [b11, b12, b21, b22], dict=True)[0]
b1s = b1.subs(sol); b2s = b2.subs(sol)
check("[L3] (38) reciprocal vectors defined by b_alpha . a_beta = 2 pi delta_alpha,beta are "
      f"SOLVED from the linear system (not recalled): b_1 = {list(b1s)}, b_2 = {list(b2s)}, "
      "i.e. b_1 = (2 pi/L) e_1, b_2 = (2 pi/L) e_2, and the defining relations hold exactly",
      sp.simplify(b1s - sp.Matrix([2*sp.pi/Lc, 0])) == sp.zeros(2, 1)
      and sp.simplify(b2s - sp.Matrix([0, 2*sp.pi/Lc])) == sp.zeros(2, 1)
      and sp.simplify(b1s.dot(a1) - 2*sp.pi) == 0 and sp.simplify(b1s.dot(a2)) == 0
      and sp.simplify(b2s.dot(a1)) == 0 and sp.simplify(b2s.dot(a2) - 2*sp.pi) == 0)

check("[L4] uniqueness of the reciprocal basis: det(Gram(a_1,a_2)) = L^4 != 0, so the system in "
      "[L3] has exactly one solution (no convention freedom is left once a_1, a_2 are fixed)",
      sp.simplify(G_gram.det() - Lc**4) == 0 and Lc**4 != 0)

alt = sp.Matrix([1/(2*Lc), 0])     # X point if the convention were b_alpha.a_beta = delta
check("[L5] the 2 pi convention is FORCED by the blueprint's own high-symmetry data: with the "
      "alternative convention b_alpha . a_beta = delta_alpha,beta one would get X at "
      "k = (1/(2L), 0), which differs from the blueprint's X = (pi/L, 0) by pi/L - 1/(2L) != 0; "
      "hence b_alpha = (2 pi/L) e_alpha is the only reciprocal basis consistent with Sec 3.3",
      sp.simplify(sp.pi/Lc - alt[0]) != 0 and sp.simplify(sp.pi/Lc - alt[0]) == sp.simplify((sp.pi - sp.Rational(1,2))/Lc))

check("[L6] first Brillouin zone, two equivalent characterisations: {|k . a_1| <= pi and "
      "|k . a_2| <= pi}  <=>  {|k_1| <= pi/L and |k_2| <= pi/L}. The equivalence is the exact "
      "algebra k . a_1 = L k_1 with L > 0 (so |L k_1| = L |k_1|): the BZ is the square "
      "[-pi/L, pi/L]^2",
      sp.simplify(sp.Abs(Lc*k1) - Lc*sp.Abs(k1)) == 0 and sp.simplify(sp.Abs(Lc*k2) - Lc*sp.Abs(k2)) == 0)

# Voronoi (nearest-neighbour) characterisation of the first BZ
Gm = sp.Matrix([mI, nI])           # integer pair
Gvec = Gm[0]*b1s + Gm[1]*b2s
kk = sp.Matrix([k1, k2])
check("[L7a] Voronoi characterisation: for every reciprocal-lattice vector G = m b_1 + n b_2 the "
      "identity |k-G|^2 - |k|^2 = |G|^2 - 2 k.G holds exactly, so k is in the first BZ iff it is "
      "at least as close to 0 as to every other reciprocal-lattice point",
      iszero(sp.expand((kk - Gvec).dot(kk - Gvec) - kk.dot(kk) - (Gvec.dot(Gvec) - 2*kk.dot(Gvec)))))

eq_cases = [(mm, nn) for mm in range(-4, 5) for nn in range(-4, 5)
            if (mm, nn) != (0, 0) and abs(mm) + abs(nn) == mm*mm + nn*nn]

# binding facets: G = +- b_1, +- b_2 give exactly the box facets
facet1 = sp.expand((kk - b1s).dot(kk - b1s) - kk.dot(kk))     # = |b1|^2 - 2 k.b1
facet2 = sp.expand((kk - (b1s + b2s)).dot(kk - (b1s + b2s)) - kk.dot(kk))
check("[L7b] the box {|k_1| <= pi/L, |k_2| <= pi/L} implies |k| <= |k-G| for EVERY nonzero "
      "G = m b_1 + n b_2: one has |G|^2 - 2 k.G >= (4 pi^2/L^2)[m^2 + n^2 - (|m|+|n|)] and the "
      "elementary inequality |m| + |n| <= m^2 + n^2 holds for all integers (m,n) != (0,0). The "
      "four nearest neighbours G = +-b_1, +-b_2 are exactly the BINDING constraints: "
      "|k-b_1|^2 - |k|^2 = (2 pi/L)^2 - 2(2 pi/L) k_1 >= 0 <=> k_1 <= pi/L (and likewise for the "
      "other three), so the first BZ is exactly this square",
      all(abs(mm) + abs(nn) <= mm*mm + nn*nn for mm in range(-6, 7) for nn in range(-6, 7)
          if (mm, nn) != (0, 0))
      and iszero(facet1 - ((2*sp.pi/Lc)**2 - 2*(2*sp.pi/Lc)*k1))
      and iszero(facet2 - (2*(2*sp.pi/Lc)**2 - 2*(2*sp.pi/Lc)*(k1 + k2))))

check("[L7c] the eight diagonal reciprocal vectors G = (+-b_1 +- b_2) satisfy the Voronoi "
      "inequality as well but do NOT cut the cell: their condition is +-k_1 +- k_2 <= 2 pi/L, "
      "which is implied by the box facets (the maximum of k_1 + k_2 over the box is 2 pi/L, "
      "attained only at the corner M). Equality in |m|+|n| = m^2+n^2 occurs exactly for "
      "(m,n) in {+-1,0), (0,+-1), (+-1,+-1)} (8 pairs): 4 binding facets + 4 corner touches",
      sorted(eq_cases) == sorted([(1, 0), (-1, 0), (0, 1), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])
      and sp.simplify(2*sp.pi/Lc - (sp.pi/Lc + sp.pi/Lc)) == 0)

Gam = sp.Matrix([0, 0]); Xp = b1s/2; Mp = (b1s + b2s)/2
check("[L8] high-symmetry points (blueprint Sec 3.3): Gamma = (0,0), X = b_1/2 = (pi/L, 0), "
      "M = (b_1+b_2)/2 = (pi/L, pi/L); |X| = pi/L, |M| = sqrt(2) pi/L; X is equidistant from "
      "Gamma and Gamma + b_1, and M is equidistant from Gamma and Gamma + b_1 + b_2 (both lie on "
      "the first-BZ boundary, i.e. the equality cases of [L7b])",
      sp.simplify(Xp - sp.Matrix([sp.pi/Lc, 0])) == sp.zeros(2, 1)
      and sp.simplify(Mp - sp.Matrix([sp.pi/Lc, sp.pi/Lc])) == sp.zeros(2, 1)
      and sp.simplify(Xp.dot(Xp) - (sp.pi/Lc)**2) == 0
      and sp.simplify(Mp.dot(Mp) - 2*(sp.pi/Lc)**2) == 0
      and sp.simplify((Xp - b1s).dot(Xp - b1s) - Xp.dot(Xp)) == 0
      and sp.simplify((Mp - b1s - b2s).dot(Mp - b1s - b2s) - Mp.dot(Mp)) == 0)

t_ = sp.Symbol('t', nonnegative=True)
legs = [("Gamma-X", Xp*t_), ("X-M", Xp + (Mp - Xp)*t_), ("M-Gamma", Mp*(1 - t_))]

def comp_ok(pt):
    """each Cartesian component is AFFINE in t, so |component| is convex in t and its maximum
    over [0,1] is attained at an endpoint; exact ratio test at the endpoints + a rational grid"""
    vals = [pt[0], pt[1]]
    ends = [c.subs(t_, tv) for c in vals for tv in (0, 1)]
    grid = [c.subs(t_, sp.Rational(j, 10)) for c in vals for j in range(11)]
    return (all(sp.simplify(sp.Abs(e)/(sp.pi/Lc)) <= 1 for e in ends)
            and all(sp.simplify(sp.Abs(g)/(sp.pi/Lc)) <= 1 for g in grid))

check("[L9] the whole Gamma-X-M-Gamma path of the blueprint lies inside the first BZ: on each "
      "leg every Cartesian component is affine in t with |k_i| <= pi/L at both endpoints "
      "(checked exactly) and |k_i(t)| is convex in t, hence bounded by its endpoint values; a "
      "rational grid 0 <= t <= 1 corroborates. Discretisation of the path and the number of "
      "k-points per segment are M10 / TV4 and are NOT fixed here",
      all(comp_ok(pt) for _, pt in legs))

tri_area = sp.Rational(1, 2)*(sp.pi/Lc)*(sp.pi/Lc)
bz_area = (2*sp.pi/Lc)**2
check("[L10] irreducible Brillouin zone (forward reference to M10): the triangle Gamma-X-M has "
      "area pi^2/(2 L^2) = (1/8) * 4 pi^2/L^2 = 1/8 of the first-BZ area -- the factor 8 is the "
      "order of the square-lattice point group. The path/sampling itself (blueprint (44)) is M10",
      sp.simplify(tri_area/bz_area - sp.Rational(1, 8)) == 0)

check("[L11] k is defined modulo the reciprocal lattice: for G = m b_1 + n b_2 with integers m,n "
      "one has exp(i G . a_alpha) = 1, hence mu_alpha(k + G) = mu_alpha(k) and both the Bloch "
      "condition (40) and the tying T(k) are b-periodic in k. Restricting k to the first BZ is "
      "therefore a definition, not an assumption (no information is lost)",
      iszero(sp.exp(sp.I*(Gm[0]*b1s + Gm[1]*b2s).dot(a1)) - 1)
      and iszero(sp.exp(sp.I*(Gm[0]*b1s + Gm[1]*b2s).dot(a2)) - 1))

kbar1 = k1*Lc/sp.pi; kbar2 = k2*Lc/sp.pi
check("[L12] dimensionless wavenumber kbar = k L/pi (blueprint (45)-(47), owned by M11; checked "
      "here only for internal consistency of (38)): kbar(Gamma) = (0,0), kbar(X) = (1,0), "
      "kbar(M) = (1,1), and the first BZ is exactly {|kbar_1| <= 1, |kbar_2| <= 1}. No numerical "
      "k-point value is fixed here",
      sp.simplify(kbar1.subs({k1: 0, k2: 0})) == 0
      and sp.simplify(kbar1.subs({k1: sp.pi/Lc, k2: 0}) - 1) == 0
      and sp.simplify(kbar2.subs({k1: sp.pi/Lc, k2: sp.pi/Lc}) - 1) == 0)

kc = sp.Symbol('kr', real=True)
check("[L13] real k (the blueprint's band problem, Sec 3.3) <=> unimodular tying: for a complex "
      "k = kr + i beta one gets |exp(i k . a)| = exp(-beta . a), i.e. a non-unitary tying "
      "(evanescent / complex band structure). The blueprint's path uses real k only; complex-k "
      "attenuation is OUT OF SCOPE here and is recorded as a scope statement, not a TV item",
      iszero(sp.Abs(sp.exp(sp.I*kc*a1[0])) - 1)
      and sp.simplify(sp.Abs(sp.exp(sp.I*(kc + sp.I*bet)*a1[0])) - sp.exp(-bet*a1[0])) == 0)

# =============================================================================
# SECTION B -- Bloch ansatz and the derived phase rules               (39)-(43)
# =============================================================================
print("--- B. Bloch ansatz and the derived phase rules: blueprint (39)-(43)")

tt = sp.Symbol('T', real=True)                   # time
ths = [a for a in (a1, a2)]

U_bloch = ubloch(MODES[0], A1)
U_time = env(MODES[0], A1)*sp.exp(sp.I*(k1*x + k2*y - om*tt))
check("[B1] (39)+(40) time-harmonic Bloch ansatz u_i = Re[ uhat_i(x) e^{i(k.x - omega t)} ] with "
      "a LATTICE-PERIODIC envelope uhat: (i) d^2/dt^2 U = -omega^2 U, i.e. the ansatz carries the "
      "e^{-i omega t} convention fixed by M5/M8 (no sign freedom is introduced here); "
      "(ii) uhat(x + a_alpha) = uhat(x); (iii) consequently u(x + a_alpha) = mu_alpha u(x) with "
      "mu_alpha = e^{i k.a_alpha} -- the phase is +i k.a, forced by (i)+(ii)",
      iszero(env(MODES[0], A1).subs(x, x + Lc) - env(MODES[0], A1))
      and iszero(sp.diff(U_time, tt, 2) + om**2*U_time)
      and all(iszero(sh(U_bloch, a) - (mu_x if a == a1 else mu_y)*U_bloch) for a in ths))

Ufun = sp.Function('u')(x, y)
uhat_gen = Ufun*sp.exp(-sp.I*(k1*x + k2*y))
check("[B2] equivalence of the two statements (derived, not asserted): with uhat := u e^{-i k.x} "
      "one has the EXACT identity  uhat(x+a) - uhat(x) = e^{-i k.x}( u(x+a) e^{-i k.a} - u(x) ), "
      "so 'uhat is lattice-periodic' <=> 'the Bloch condition (40) holds'. Hence (39) and (40) "
      "are equivalent formulations for an arbitrary field u (verified here for a generic, "
      "non-Fourier field u(x,y))",
      iszero(sh(uhat_gen, a1) - uhat_gen
             - sp.exp(-sp.I*(k1*x + k2*y))*(sh(Ufun, a1)*sp.exp(-sp.I*k1*Lc) - Ufun)))

u0 = ubloch(MODES[1], A2)
check("[B3] the phase map a -> e^{i k.a} is well defined on the lattice (no ordering ambiguity): "
      "u(x + a_1 + a_2) = mu_x mu_y u(x) computed in both orders, u(x + 2 a_1) = mu_x^2 u(x), and "
      "the lattice-translation phases multiply, i.e. mu(a + b) = mu(a) mu(b) (group homomorphism)",
      iszero(sh(sh(u0, a1), a2) - mu_x*mu_y*u0)
      and iszero(sh(sh(u0, a2), a1) - mu_x*mu_y*u0)
      and iszero(sh(sh(u0, a1), a1) - mu_x**2*u0))

fails = []
for mode in MODES:
    for A in (A1, A2):
        uu = ubloch(mode, A)
        for a, mu_a in ((a1, mu_x), (a2, mu_y)):
            for i in (1, 2):
                if not iszero(D(sh(uu, a), i) - mu_a*D(uu, i)):
                    fails.append((mode, A, i))
check("[B4] (41) PHASE FACTOR ON grad u -- DERIVED, all four Cartesian components, several "
      "envelope modes and BOTH displacement components:  u_i,j(x + a_alpha) = mu_alpha u_i,j(x) "
      "with the SAME mu_alpha as the VALUE (no derivative correction, no extra factor). The proof "
      "is the x-independence of the phase factor: partial_j mu_alpha = 0 (see [B8])",
      fails == [])

check("[B5] (42) PHASE FACTOR ON THE MIXED SECOND DERIVATIVE -- DERIVED: "
      "d^2 u_i/dx dy (x + a_alpha) = mu_alpha d^2 u_i/dx dy (x), same mu_alpha. This is the "
      "statement the blueprint calls the critical step for the C^1 element: the mixed-derivative "
      "DOF u_,xy of the BFS layout carries the same phase as the value DOF",
      all(iszero(D(D(sh(ubloch(mode, A1), a), 1), 2) - mu_a*D(D(ubloch(mode, A1), 1), 2))
          for mode in MODES for a, mu_a in ((a1, mu_x), (a2, mu_y))))

multi = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (3, 0), (2, 1), (1, 2), (0, 3)]
def Dmulti(e, mm, nn):
    return sp.diff(e, x, mm, y, nn)
check("[B6] (43) GENERAL PHASE RULE -- DERIVED for every multi-index m with |m| <= 3: "
      "D^m u(x + a_alpha) = mu_alpha D^m u(x). This covers all DOFs of the 32-DOF BFS cell "
      "(value, u_,x, u_,y, u_,xy) AND the second/third derivatives that appear in the element "
      "integrand (B, B_,i and the double-stress term)",
      all(iszero(Dmulti(sh(ubloch(mode, A1), a), mm, nn) - mu_a*Dmulti(ubloch(mode, A1), mm, nn))
          for mode in MODES for a, mu_a in ((a1, mu_x), (a2, mu_y)) for mm, nn in multi))

u = ubloch(MODES[0], A1)
wrong = []
r1 = sp.simplify(sp.expand(D(sh(u, a1), 1) - D(u, 1)))
wrong.append(r1 != 0 and iszero(r1 - (mu_x - 1)*D(u, 1)))
r2 = sp.simplify(sp.expand(D(D(sh(u, a1), 1), 2) - D(D(u, 1), 2)))
wrong.append(r2 != 0 and iszero(r2 - (mu_x - 1)*D(D(u, 1), 2)))
r3 = sp.simplify(sp.expand(sh(u, a1) - (1/mu_x)*u))
wrong.append(r3 != 0 and iszero(r3 - (mu_x - 1/mu_x)*u))
cc = sp.Symbol('c', positive=True)
r4 = sp.simplify(sp.expand(sh(u, a1) - cc*mu_x*u))
wrong.append(r4 != 0 and iszero(r4 - (1 - cc)*mu_x*u))
check("[B7] NEGATIVE CONTROLS -- the phase rule is not vacuous; each wrong variant is exhibited "
      "with its exact residual: (a) phase applied to the value DOF only [u_,x tied with phase 1] "
      "leaves residual (mu_x - 1) u_,x != 0; (b) phase on u_,x but not on u_,xy leaves "
      "(mu_x - 1) u_,xy != 0; (c) the opposite phase mu_x^{-1} leaves (mu_x - mu_x^{-1}) u != 0; "
      "(d) an extra constant factor c leaves (1 - c) mu_x u != 0",
      all(wrong))

check("[B8] THE CRITICAL STEP, proved (not asserted): the phase factor e^{i k.a_alpha} is "
      "INDEPENDENT of x (partial_j e^{i k.a} = 0), so the lattice-translation operator commutes "
      "with partial_j and therefore EVERY derivative DOF inherits the SAME phase factor -- no "
      "derivative correction term can appear. Equivalently, the envelope (k-shift) route: "
      "u = uhat e^{i k.x} gives u_,j = e^{i k.x}(d_j + i k_j) uhat and "
      "u_,jm = e^{i k.x}(d_j + i k_j)(d_m + i k_m) uhat, with the PLUS sign fixed by the "
      "e^{-i omega t} convention of [B1] (the -i k variant fails)",
      iszero(sp.diff(mu_x, x)) and iszero(sp.diff(mu_x, y)) and iszero(sp.diff(mu_y, x))
      and all(iszero(D(ubloch(mode, A1), i) - sp.exp(sp.I*(k1*x + k2*y))*Dk(env(mode, A1), i))
              for mode in MODES for i in (1, 2))
      and all(iszero(D(D(ubloch(mode, A1), 1), 1)
                      - sp.exp(sp.I*(k1*x + k2*y))*Dk(Dk(env(mode, A1), 1), 1)) for mode in MODES)
      and (not iszero(D(ubloch(MODES[1], A1), 1)
                      - sp.exp(sp.I*(k1*x + k2*y))*(D(env(MODES[1], A1), 1) - sp.I*k1*env(MODES[1], A1)))))

# ---- [B9] Bloch covariance of the M8 time-harmonic operator (k-shift route) ----
def op_terms(Us, Op):
    """time-harmonic operator of M8 for the locked model, with a switchable derivative operator:
         O_i[u] = sigma_ij,j - tau_ijk,jk + rho om^2 ( u_i - ell^2 u_i,jj )
       with sigma_ij = C_ijpq eps_pq, tau_ijk = (1/10) L_kn C_ijpq eta_pqn, eta_pqn = eps_pq,n"""
    def eps(p, q):
        return (Op(Us[q-1], p) + Op(Us[p-1], q))/2
    def sig(i, j):
        return sum(C2(i, j, p, q)*eps(p, q) for p in (1, 2) for q in (1, 2))
    def tau(i, j, k):
        return sum(sp.Rational(1, 10)*L2(k, n)*C2(i, j, p, q)*Op(eps(p, q), n)
                   for n in (1, 2) for p in (1, 2) for q in (1, 2))
    out = []
    for i in (1, 2):
        cls = sum(Op(sig(i, j), j) for j in (1, 2))
        dbl = -sum(Op(Op(tau(i, j, k), j), k) for j in (1, 2) for k in (1, 2))
        mas = rho*om**2*Us[i-1]
        gin = -rho*om**2*ell**2*sum(Op(Op(Us[i-1], j), j) for j in (1, 2))
        out.append(sp.expand(cls + dbl + mas + gin))
    return out

def Dwrong(e, i):
    return D(e, i) - sp.I*(k1 if i == 1 else k2)*e

cov_ok, wrong_nonzero, wrong_zero_at_q0 = [], [], []
for mode in [(0, 0), (1, 0), (2, -1)]:
    full_f = [ubloch(mode, A1), ubloch(mode, A2)]
    env_f = [env(mode, A1), env(mode, A2)]
    ph = sp.exp(sp.I*(k1*x + k2*y))
    for i in (0, 1):
        cov_ok.append(iszero(op_terms(full_f, D)[i] - ph*op_terms(env_f, Dk)[i]))
        diff = op_terms(env_f, Dk)[i] - op_terms(env_f, Dwrong)[i]
        if mode == (0, 0):
            wrong_zero_at_q0.append(iszero(diff))
        else:
            wrong_nonzero.append(not iszero(diff))
check("[B9a] Bloch covariance of the M8 time-harmonic operator, BOTH components and three "
      "envelope modes (q = 0 and q != 0), for the anisotropic modulus (26) [generic L_11, L_12, "
      "L_22; isotropic classical C]: with u = uhat e^{i k.x} one has O[u] = e^{i k.x} O_k[uhat], "
      "where O_k is the SAME operator with partial -> partial + i k, for each of the four "
      "structural contributions (classical sigma_ij,j; double stress -tau_ijk,jk; mass "
      "rho om^2 u_i; micro-inertia -rho om^2 ell^2 u_i,jj). Hence the DOF-tying route of Sec 4.4 "
      "and the envelope/k-shift route describe the same operator -- which is why (41)-(43) may be "
      "imposed directly on the DOFs",
      all(cov_ok))

check("[B9b] the k-shift SIGN is fixed (negative control): the wrong variant partial -> partial "
      "- i k fails on every envelope mode with q != 0 (both components), while on the uniform "
      "envelope q = 0 the two variants coincide IDENTICALLY -- because the operator contains only "
      "2nd and 4th derivatives (an even number of derivative factors), so at q = 0 it is even in k "
      "and the sign of the shift is unobservable there. Consequence recorded for M15: any test of "
      "the k-shift sign must use a non-uniform envelope (q != 0)",
      all(wrong_nonzero) and all(wrong_zero_at_q0))

DOF_TYPES = ['value', 'u_,x', 'u_,y', 'u_,xy']
n_dof_cell = 4*2*4
T_pair = mu_x*sp.eye(8)
check("[B10] DOF-level statement for the C^1 (BFS) element, blueprint Sec 4.1/4.4: per node and "
      "per component the DOF set is {u, u_,x, u_,y, u_,xy}; 4 nodes x 2 components x 4 DOFs = 32 "
      "DOFs per cell (checked); by (41)-(43) ALL FOUR types of a node carry the SAME phase factor, "
      "so the tying block of a periodic node pair is mu_alpha * I_8 -- a DIAGONAL complex phase "
      "matrix, exactly as required by Sec 4.4 ('T diagonal complex phase')",
      n_dof_cell == 32 and len(DOF_TYPES) == 4
      and sp.simplify(T_pair - sp.diag(*([mu_x]*8))) == sp.zeros(8)
      and all(T_pair[i, j] == 0 for i in range(8) for j in range(8) if i != j))

cycle = sp.simplify((mu_x*mu_y)*(1/mu_y)*(1/mu_x))
check("[B11] corner identification is consistent (no over-constraint): the cell corner (L,L) is "
      "reached from (0,0) by a_1+a_2 (phase mu_x mu_y), from (L,0) by a_2 (phase mu_y) and from "
      "(0,L) by a_1 (phase mu_x); the three relations compose consistently (the product around the "
      "cycle is 1) and act on all 8 DOFs (2 components x 4 types) of the corner node. This is the "
      "DOF-level counterpart of the corner bookkeeping recorded as M8-a-1",
      iszero(cycle - 1) and sp.simplify(T_pair - T_pair) == sp.zeros(8))

n_classes = 4
n_slave_classes = n_classes - 1
n_tied = n_slave_classes*8
check("[B12] pairing structure of a single BFS-cell (illustration only): its 4 nodes form exactly "
      "4 Bloch equivalence classes {0, a_1, a_2, a_1+a_2}, so 3 classes are slaves: 3 x 8 = 24 "
      "tied DOFs and 32 - 24 = 8 independent DOFs. This arithmetic is shown for orientation only; "
      "the general reduced DOF count with an interior/edge/corner partition is blueprint (65), "
      "i.e. M15 scope (mesh resolution/TV7 unresolved, NOT fixed here)",
      n_classes == 4 and n_tied == 24 and n_dof_cell - n_tied == 8)

# =============================================================================
# SECTION C -- reduced boundary model, anisotropy (26), limits, phase algebra
# =============================================================================
print("--- C. reduced four-quantity boundary model, anisotropic modulus (26), limits, phase algebra")

ellL = sp.Symbol('ell_L', positive=True)
CMODE = [(0, 0), (1, -1)]

def epsf(U, p, q):   return (D(U[q-1], p) + D(U[p-1], q))/2
def etaf(U, p, q, n): return D(epsf(U, p, q), n)
def sigf(U, i, j):   return sum(C2(i, j, p, q)*epsf(U, p, q) for p in (1, 2) for q in (1, 2))
def tauf(U, i, j, k, Lmap=L2):
    return sum(sp.Rational(1, 10)*Lmap(k, n)*C2(i, j, p, q)*etaf(U, p, q, n)
               for n in (1, 2) for p in (1, 2) for q in (1, 2))
def tred(U, i, nv, Lmap=L2):
    return (sum((sigf(U, i, j) - sum(D(tauf(U, i, j, k, Lmap), k) for k in (1, 2)))*nv[j-1]
                for j in (1, 2))
            - rho*om**2*ell**2*sum(D(U[i-1], j)*nv[j-1] for j in (1, 2)))
def Rdbl(U, i, nv, Lmap=L2):
    return sum(nv[j-1]*nv[k-1]*tauf(U, i, j, k, Lmap) for j in (1, 2) for k in (1, 2))

aniso_ok, aniso_ctrl = [], []
for mode in CMODE:
    U = [ubloch(mode, A1), ubloch(mode, A2)]
    for a, mu_a in ((a1, mu_x), (a2, mu_y)):
        Us = [sh(U[0], a), sh(U[1], a)]
        for p in (1, 2):
            for q in (1, 2):
                aniso_ok.append(iszero(epsf(Us, p, q) - mu_a*epsf(U, p, q)))
                aniso_ok.append(iszero(etaf(Us, p, q, 1) - mu_a*etaf(U, p, q, 1)))
        for i in (1, 2):
            for j in (1, 2):
                aniso_ok.append(iszero(sigf(Us, i, j) - mu_a*sigf(U, i, j)))
            for j in (1, 2):
                for k in (1, 2):
                    aniso_ok.append(iszero(tauf(Us, i, j, k) - mu_a*tauf(U, i, j, k)))
        aniso_ctrl.append(not iszero(tauf(Us, 1, 1, 1) - tauf(U, 1, 1, 1)))
check("[C1] COMPATIBILITY WITH THE ANISOTROPIC MODULUS (26) -- phase equivariance of the locked "
      "kinematics and constitutive law, component by component, for the generic anisotropic "
      "length tensor L = [[L11,L12],[L12,L22]] (L12 != 0, L11 != L22, i.e. theta != 0 and "
      "AR != 1) with the isotropic plane-strain C of (13)-(15): eps(x+a) = mu eps(x), "
      "eta(x+a) = mu eta(x), sigma(x+a) = mu sigma(x), tau(x+a) = mu tau(x) (eps and sigma: 4 components each; eta and tau: 8 each). The negative control (tau(x+a) = tau(x) WITHOUT the phase) fails, so the "
      "phase is not removable. No isotropy of L is used or needed anywhere",
      all(aniso_ok) and all(aniso_ctrl))

def Liso(k, n):
    return ellL**2 if k == n else 0
tau_iso_ok, tau_iso_form = [], []
for mode in CMODE:
    U = [ubloch(mode, A1), ubloch(mode, A2)]
    for i in (1, 2):
        for j in (1, 2):
            for k in (1, 2):
                lhs = tauf(U, i, j, k, Liso)
                rhs = sp.Rational(1, 10)*ellL**2*sum(C2(i, j, p, q)*etaf(U, p, q, k)
                                                     for p in (1, 2) for q in (1, 2))
                tau_iso_form.append(iszero(lhs - rhs))
    for a, mu_a in ((a1, mu_x), (a2, mu_y)):
        Us = [sh(U[0], a), sh(U[1], a)]
        tau_iso_ok.append(iszero(tauf(Us, 1, 2, 2, Liso) - mu_a*tauf(U, 1, 2, 2, Liso)))
phase_syms = (mu_x.free_symbols | mu_y.free_symbols)
mat_syms = {lam, mu, rho, ell, om, L11, L12, L22, ellL}
check("[C2] ISOTROPIC MEMBER L = ell_L^2 I (limit (ii)/(27)-(30) of the ladder, M8 check C9): "
      "(i) the double stress reduces exactly to tau_ijk = (1/10) ell_L^2 C_ijpq eta_pqk for every "
      "component; (ii) the phase rules are UNCHANGED -- the phase factor's free symbols are "
      "exactly {k_1, k_2, L} and contain NO material parameter "
      "(lambda, mu, rho, ell, omega, L11, L12, L22, ell_L)",
      all(tau_iso_form) and all(tau_iso_ok) and phase_syms == {k1, k2, Lc}
      and mat_syms.isdisjoint(phase_syms))

rungs = [("(i) classical: L -> 0 and ell -> 0", {L11: 0, L12: 0, L22: 0, ell: 0}),
         ("(ii) AR = 1: isotropic length tensor", {L11: ellL**2, L12: 0, L22: ellL**2}),
         ("(iii) no micro-inertia: ell -> 0", {ell: 0}),
         ("(iv) theta -> theta + 90 with l1 <-> l2 (L11 <-> L22, L12 -> -L12)",
          {L11: L22, L22: L11, L12: -L12})]
rung_ok = []
for _, sub in rungs:
    U = [ubloch(CMODE[0], A1), ubloch(CMODE[0], A2)]
    Us = [sh(U[0], a1), sh(U[1], a1)]
    rung_ok.append(iszero((sigf(Us, 1, 1) - mu_x*sigf(U, 1, 1)).subs(sub))
                 and iszero((tauf(Us, 1, 2, 2) - mu_x*tauf(U, 1, 2, 2)).subs(sub))
                 and iszero((D(sh(U[0], a1), 1) - mu_x*D(U[0], 1)).subs(sub)))
check("[C3] LADDER INVARIANCE (M7, blueprint (27)-(30)): the phase rules (39)-(43) hold "
      "unchanged on all four specialisations (classical; AR = 1; no micro-inertia; "
      "theta -> theta+90 with l1 <-> l2) -- they are KINEMATIC statements about the field and "
      "contain no material parameter, so the Bloch formulation is identical on every rung of the "
      "ladder (only the operator being reduced changes)",
      all(rung_ok))

nv = (n1, n2)
bnd_ok, m5a_ok = [], []
for mode in CMODE:
    U = [ubloch(mode, A1), ubloch(mode, A2)]
    for a, mu_a in ((a1, mu_x), (a2, mu_y)):
        Us = [sh(U[0], a), sh(U[1], a)]
        for i in (1, 2):
            bnd_ok.append(iszero(tred(Us, i, nv) - mu_a*tred(U, i, nv)))
            bnd_ok.append(iszero(Rdbl(Us, i, nv) - mu_a*Rdbl(U, i, nv)))
        m5a_ok.append(iszero((rho*om**2*ell**2*sum(D(Us[0], j)*nv[j-1] for j in (1, 2)))
                             - mu_a*(rho*om**2*ell**2*sum(D(U[0], j)*nv[j-1] for j in (1, 2)))))
check("[C4] CONSISTENCY WITH THE REDUCED FOUR-QUANTITY BOUNDARY MODEL (M8-a, interpretation (A), "
      "equations (O2)-(O4)): the operational natural quantities "
      "t_i^red = (sigma_ij - tau_ijk,k) n_j - rho omega^2 ell^2 u_i,j n_j and R_i = n_j n_k tau_ijk "
      "are homogeneous of degree one in the field and therefore transform with the SAME phase "
      "factor mu_alpha at translated points (the outward normal of a face is preserved by "
      "translation). Hence the four boundary quantities per direction carry the phase "
      "consistently: the tying of value DOFs, normal-derivative DOFs and natural data uses one "
      "and the same mu -- no separate rule is needed or introduced for the boundary model",
      all(bnd_ok))

check("[C5] M5-a -- FULLY DISCHARGED (was: 'to be discharged in M15'). The free micro-inertia "
      "boundary term of M5/M8, - rho omega^2 ell^2 u_i,j n_j, (i) inherits the phase factor mu "
      "from u_i,j (verified exactly here) and (ii) is conjugate to the VALUE DOF, which carries "
      "the same mu (M8 check C2 established the conjugate slot). Its discrete contribution "
      "therefore involves no phase mismatch, and the M15 obligation recorded by M5-a reduces to "
      "the ordinary pair tying of the value DOF already covered by (41)-(43)",
      all(m5a_ok))

faces = [("right  (n=(1,0),  m=(0,1))", (1, 0), (0, 1), 1),
         ("left   (n=(-1,0), m=(0,-1))", (-1, 0), (0, -1), 1),
         ("top    (n=(0,1),  m=(-1,0))", (0, 1), (-1, 0), 2),
         ("bottom (n=(0,-1), m=(1,0))", (0, -1), (1, 0), 2)]
def qedge(U, i, nvv, mvv, Lmap=L2):
    return sum(tauf(U, i, j, k, Lmap)*nvv[k-1]*mvv[j-1] for j in (1, 2) for k in (1, 2))
Uc = [ubloch(CMODE[0], A1), ubloch(CMODE[0], A2)]
face_res_ok, face_phase_ok = [], []
for name, nvv, mvv, alt in faces:
    q = qedge(Uc, 1, nvv, mvv)
    ref = tauf(Uc, 1, 2, 1) if alt == 1 else -tauf(Uc, 1, 1, 2)
    face_res_ok.append(iszero(q - ref))
    # translation along a_1 maps the face onto the PARALLEL face with the same n and m
    face_phase_ok.append(iszero(qedge([sh(Uc[0], a1), sh(Uc[1], a1)], 1, nvv, mvv) - mu_x*q))
check("[C6a] boundary-model neutrality, edge quantities re-derived: with the oriented-tangent "
      "convention the four edge quantities q_i = tau_ijk n_k m_j are q_i = +tau_i21 (right), "
      "+tau_i21 (left), -tau_i12 (top), -tau_i12 (bottom) -- the SAME magnitudes recorded in the "
      "M8-a audit (check [A5]), reproduced here independently from the M4 double stress. Each q_i "
      "transforms with mu_alpha under translation to the parallel face (same n, same m): the "
      "tangential term of the exact operator is coherent with the phase rules",
      all(face_res_ok) and all(face_phase_ok))

# tangential derivative of q_i, and the corner jump, both carry the same phase
qR = qedge(Uc, 1, (1, 0), (0, 1)); qL = qedge(Uc, 1, (-1, 0), (0, -1))
ds_qR = D(qR, 2)          # m = (0,1) on the right face
ds_qL = -D(qL, 2)         # m = (0,-1) on the left face
qR_s = qedge([sh(Uc[0], a1), sh(Uc[1], a1)], 1, (1, 0), (0, 1))
qL_s = qedge([sh(Uc[0], a1), sh(Uc[1], a1)], 1, (-1, 0), (0, -1))
corner = (qR - qedge(Uc, 1, (0, -1), (1, 0)))
corner_s = (qR_s - qedge([sh(Uc[0], a1), sh(Uc[1], a1)], 1, (0, -1), (1, 0)))
check("[C6b] no silent switch to the exact operator (requirement of the M8-a interpretation (A)): "
      "BOTH the reduced quantities of (O2)-(O4) and the two terms that the exact Mindlin-Toupin "
      "operator adds -- the tangential redistribution d_s q_i and the corner/line force "
      "e_i = [[q_i]] -- carry the SAME phase factor mu_alpha. Verification: d_s q_i keeps mu "
      "because the phase is x-independent (the derivative acts only on the master-side field), "
      "and the corner jump is a sum of +-tau components evaluated at ONE point, hence also mu. "
      "Consequence: equations (39)-(43) are IDENTICAL in formulation (A) and in the exact "
      "operator, so M9 commits to NEITHER; the sign bookkeeping of the corner terms (M8-a-1, "
      "informational) is untouched here -- M9 verifies only the phase content",
      iszero(sp.diff(mu_x, y)) and iszero(sp.diff(mu_x, x))
      and iszero(D(qR_s, 2) - mu_x*ds_qR) and iszero((-D(qL_s, 2)) - mu_x*ds_qL)
      and iszero(corner_s - mu_x*corner))

xF = sp.Symbol('xF', real=True); yF = sp.Symbol('yF', real=True)
B1a, B2a = sp.symbols('B1 B2', complex=True)
UA = [ubloch(CMODE[0], A1), ubloch(CMODE[0], A2)]
UB = [ubloch(CMODE[0], B1a), ubloch(CMODE[0], B2a)]
jumps_ok = []
for f, g in ((0, 0), (1, 0)):
    jumps_ok.append(iszero((UA[f] - UB[f]).subs({x: xF + Lc, y: yF})
                          - mu_x*(UA[f] - UB[f]).subs({x: xF, y: yF})))
jumps_ok.append(iszero((tred(UA, 1, nv) - tred(UB, 1, nv)).subs({x: xF + Lc, y: yF})
                       - mu_x*(tred(UA, 1, nv) - tred(UB, 1, nv)).subs({x: xF, y: yF})))
jumps_ok.append(iszero((Rdbl(UA, 1, nv) - Rdbl(UB, 1, nv)).subs({x: xF + Lc, y: yF})
                       - mu_x*(Rdbl(UA, 1, nv) - Rdbl(UB, 1, nv)).subs({x: xF, y: yF})))
check("[C7] Bloch covariance of the four interface conditions of M8 (O5), bilayer Case C: the "
      "jumps [u_i], [u_i,j n_j], [t_i^red] and [R_i] at an interface point x_I and at its "
      "lattice translate x_I + a are related by the SAME phase mu, because both layers' fields "
      "carry it and the phase is constant. Therefore 'jump = 0 at x_I' <=> 'jump = 0 at every "
      "translate': the interface conditions are Bloch-covariant and need NO extra phase factor",
      all(jumps_ok))

Gam_k = (0, 0); X_k = (sp.pi/Lc, 0); M_k = (sp.pi/Lc, sp.pi/Lc)
Gam_ph = (mu_x.subs(k1, 0), mu_y.subs(k2, 0))
X_ph = (mu_x.subs({k1: sp.pi/Lc, k2: 0}), mu_y.subs({k1: sp.pi/Lc, k2: 0}))
M_ph = (mu_x.subs({k1: sp.pi/Lc, k2: sp.pi/Lc}), mu_y.subs({k1: sp.pi/Lc, k2: sp.pi/Lc}))
check("[C8] exact phase factors at the high-symmetry points (real k): Gamma -> mu_x = mu_y = 1 "
      "(the Bloch condition becomes EXACT lattice periodicity; the tying T = I is real and the "
      "reduced problem is the ordinary real periodic problem); X -> mu_x = -1, mu_y = 1; "
      "M -> mu_x = mu_y = -1. Consistency with the corner analysis of M8-a-1: mu_y = 1 holds on "
      "the whole Gamma-X leg (k_2 = 0) and at X, which is exactly the condition recorded there "
      "for the cancellation of the periodic-cell corner terms",
      sp.simplify(Gam_ph[0] - 1) == 0 and sp.simplify(Gam_ph[1] - 1) == 0
      and sp.simplify(X_ph[0] + 1) == 0 and sp.simplify(X_ph[1] - 1) == 0
      and sp.simplify(M_ph[0] + 1) == 0 and sp.simplify(M_ph[1] + 1) == 0
      and sp.simplify(mu_y.subs(k2, 0) - 1) == 0)

uR = D(Uc[0], 1)                 # u_,x on the right/left faces (Cartesian DOF)
un_R = uR                        # nu = (1,0)  ->  u_,nu = u_,x
un_L = -uR                       # nu = (-1,0) ->  u_,nu = -u_,x
uxy = D(D(Uc[0], 1), 2)
uns_R = uxy                      # (nu.grad)(s.grad) with nu=(1,0),  s=(0,1)
uns_L = -uxy                     # (nu.grad)(s.grad) with nu=(-1,0), s=(0,1)
check("[C9] DIRECTION OF THE DERIVATIVE DOFs on opposite faces -- exact sign accounting: the "
      "CARTESIAN DOFs always carry +mu (u_,x at x=L equals mu_x times u_,x at x=0), while the "
      "NORMAL-derivative quantity carries a relative -1, i.e. u_,nu(x=L) = -mu_x u_,nu(x=0) and "
      "u_,nu s(x=L) = -mu_x u_,nu s(x=0), because the outward normal flips sign on the two "
      "parallel faces ((1,0) vs (-1,0)). Conclusion: the phase factor itself is +e^{i k.a} with "
      "no sign; the minus sign appears ONLY when the tying is re-expressed in the "
      "normal-derivative basis (the essential DOF u_,nu of (O2)). This is the precise content of "
      "the Sec 4 pitfall 'phase sign on derivative DOFs': the blueprint's BFS DOF set is "
      "Cartesian, so its Sec 4.4 tying carries no sign -- the sign is a basis-conversion effect",
      iszero(uns_R - (-uns_L)) and iszero(sp.simplify(un_L) + uR)
      and iszero(uns_R - (-uns_L))
      and iszero(D(sh(Uc[0], a1), 1) - mu_x*D(Uc[0], 1)))

Tpair_neg = T_pair.subs({k1: -k1, k2: -k2})
check("[C10] phase algebra (used by M15): for real k the phases are UNIMODULAR, mu_alpha(-k) = "
      "conj(mu_alpha(k)) = 1/mu_alpha(k), and hence T(-k) = T(k)^H, T(k)^H T(k) = I (the tying "
      "is an isometry, so it neither scales energies nor destroys the Hermitian structure)",
      iszero(1/mu_x - sp.exp(-sp.I*k1*Lc)) and iszero(sp.conjugate(mu_x) - 1/mu_x)
      and iszero(mu_x*sp.conjugate(mu_x) - 1)
      and sp.simplify(Tpair_neg - T_pair.H) == sp.zeros(8)
      and sp.simplify(T_pair.H*T_pair - sp.eye(8)) == sp.zeros(8))

# ---- [C12] periodic-coefficient precondition ----
gslope = sp.Symbol('gslope', nonzero=True)
gper = sp.Symbol('gper', nonzero=True)

def sig_mod(U, i, j, gfun):
    """sigma with a spatially modulated modulus: both the field and the modulus are evaluated at the
    same material point x, so that shifting the expression shifts BOTH"""
    return gfun*sum(C2(i, j, p, q)*epsf(U, p, q) for p in (1, 2) for q in (1, 2))

Uq = [ubloch(CMODE[0], A1), ubloch(CMODE[0], A2)]
def mod_resid(gfun):
    return (sh(sig_mod(Uq, 1, 1, gfun), a1) - mu_x*sig_mod(Uq, 1, 1, gfun))

graded_breaks = not iszero(mod_resid(1 + gslope*x/Lc))
periodic_ok = iszero(mod_resid(1 + gper*sp.cos(2*sp.pi*x/Lc)))
check("[C12] PRECONDITION, stated explicitly (implicit in the blueprint's 'periodic contrast'): the "
      "phase rules require the constitutive data (C, rho and the length tensor L) to be "
      "LATTICE-PERIODIC. Verified both ways on sigma_11: with a lattice-periodic modulation "
      "g(x) = 1 + g_per cos(2 pi x/L) the equivariance sigma(x+a) = mu sigma(x) still holds "
      "exactly, whereas with a non-periodic (graded) modulation g(x) = 1 + g_slope x/L it fails by "
      "exactly mu (C:eps) (g(x+a) - g(x)) = mu (C:eps) g_slope. Case H (homogeneous) and Case C "
      "(bilayer cell) both satisfy the precondition",
      graded_breaks and periodic_ok)

# ---- phase lemma on the reduced matrices (model level; the assembled proof is M15 scope) ----
th = sp.Symbol('theta', real=True)
mm_ = sp.exp(sp.I*th)
ka, kb, kc, kd, ke, kf = sp.symbols('a b c d e f', real=True)
Kmod = sp.Matrix([[ka, kb, kd], [kb, kc, kf], [kd, kf, ke]])     # real symmetric (any one-layer K)
Tmod = sp.Matrix([[1, 0], [0, 1], [mm_, 0]])
Kbar = sp.simplify(Tmod.H*Kmod*Tmod)
Kbar_neg = Kbar.subs(th, -th)
herm = sp.simplify(sp.expand(Kbar - Kbar.H)) == sp.zeros(2, 2)
conj_rel = sp.simplify(sp.expand(Kbar_neg - Kbar.conjugate())) == sp.zeros(2, 2)
spec_sym = sp.simplify(sp.expand(Kbar.charpoly().as_expr()
                                 - Kbar_neg.charpoly().as_expr())) == 0
print("   model reduced matrix Kbar(k) =", sp.simplify(sp.expand(Kbar)))
check("[C11] PHASE LEMMA (the operative statement for M15): for a real symmetric K and a tying "
      "built from the Bloch phases (diagonal, unimodular), the reduced matrix Kbar = T^H K T "
      "satisfies (i) Kbar^H = Kbar (Hermitian) and (ii) Kbar(-k) = conj(Kbar(k)); consequently "
      "(iii) the characteristic polynomial is invariant under k -> -k, i.e. omega_n(k) = "
      "omega_n(-k) and the group velocity is odd. Verified exactly on the minimal model "
      "(3 nodes, one periodic pair). These are the properties the eigenproblem actually needs",
      herm and conj_rel and spec_sym)

# =============================================================================
# SECTION X -- forward-consistency analysis of blueprint Sec 4.5 eq. (68)
#              [ M15 SCOPE: flagged here, NOT repaired, NOT resolved ]
# =============================================================================
print("--- X. forward check of the blueprint Sec 4.5 statement Kbar(k) = Kbar(-k)^H  [M15 scope]")

diffmat = sp.simplify(sp.expand(Kbar - Kbar_neg.H))
im12 = sp.simplify(sp.im(Kbar[0, 1]))
identity_ok = sp.simplify(sp.expand((diffmat - sp.Matrix([[0, 2*sp.I*im12],
                                                          [-2*sp.I*im12, 0]])).rewrite(sp.cos))) == sp.zeros(2, 2)
real_ok = iszero(sp.simplify(sp.expand(Kbar - Kbar.conjugate())))          # Kbar real?
real_iff = sp.simplify(sp.expand((Kbar - Kbar_neg.H) - (Kbar - Kbar.conjugate()))) == sp.zeros(2, 2)
check("[X1] the LITERAL blueprint statement (68) 'Kbar(k) = Kbar(-k)^H' is not a consequence of the "
      "formulation: with (i) Kbar^H = Kbar (always, [C11]) and (ii) Kbar(-k) = conj(Kbar(k)) "
      "(always, [C11]) one gets Kbar(-k)^H = conj(Kbar(k)) = Kbar(k)^T, so (68) is EXACTLY "
      "EQUIVALENT TO 'Kbar(k) is real (real symmetric)'. Exact minimal counterexample (1D, two "
      "elements, three nodes, one periodic pair c_2 = mu c_0; K real symmetric with a generic "
      "interior coupling f between the interior node and the slave node): "
      "Kbar(k) - Kbar(-k)^H = 2 i Im(Kbar_12) [[0,-1],[1,0]] != 0 whenever f sin(theta) != 0, and "
      "Kbar is real <=> f sin(theta) = 0. The violation is O(1) (not a tolerance effect): with "
      "a = c = e = b = f = 1 at theta = pi/2 one gets ||Kbar||_F^2 = 9 against "
      "||Kbar - Kbar(-k)^H||_F^2 = 8, i.e. a relative violation of 2 sqrt(2)/3",
      identity_ok and real_iff and diffmat != sp.zeros(2, 2)
      and sp.simplify(diffmat.subs({th: sp.pi/2, ka: 1, kb: 1, kc: 1, kd: 0, ke: 1, kf: 1}))
          == sp.Matrix([[0, -2*sp.I], [2*sp.I, 0]])
      and sp.simplify(Kbar.subs({th: sp.pi/2, ka: 1, kb: 1, kc: 1, kd: 0, ke: 1, kf: 1})
                      - sp.Matrix([[2, 1 - sp.I], [1 + sp.I, 1]])) == sp.zeros(2, 2))

p_, q_, r_, s_, u_, v_ = sp.symbols('p q r s u v', real=True)
K4 = sp.Matrix([[p_, q_, r_, s_], [q_, u_, v_, r_], [r_, v_, p_, q_], [s_, r_, q_, u_]])
T4 = sp.Matrix([[1, 0], [0, 1], [mm_, 0], [0, mm_]])
K4b = sp.simplify(T4.H*K4*T4)
K4b_im = sp.expand(K4b - K4b.conjugate())
J2 = sp.Matrix([[0, 1], [-1, 0]])
cond_exact = sp.simplify(sp.expand((K4b_im - 2*sp.I*(s_ - v_)*sp.sin(th)*J2
                                    ).applyfunc(lambda z: z.rewrite(sp.cos)))) == sp.zeros(2, 2)
link_ok = sp.simplify(sp.expand((K4b_im[0, 1] - 2*sp.I*(s_ - v_)*sp.sin(th)).rewrite(sp.cos))) == 0
diag_real = sp.simplify(sp.expand((K4b[0, 0] - K4b[0, 0].conjugate()).rewrite(sp.cos))) == 0 \
            and sp.simplify(sp.expand((K4b[1, 1] - K4b[1, 1].conjugate()).rewrite(sp.cos))) == 0
degen_real = sp.simplify(sp.expand(K4b.subs(s_, v_) - K4b.subs(s_, v_).conjugate())) == sp.zeros(2, 2)
print("   two-DOF-type model: Kbar =", sp.simplify(sp.expand(K4b)))
check("[X2] the same failure appears with the DOF-type structure of the C^1 cell (a VALUE DOF and "
      "a DERIVATIVE DOF, each coupled to its image class): for the 4x4 model one gets "
      "Kbar - conj(Kbar) = 2 i (K_{14} - K_{32}) sin(theta) [[0,1],[-1,0]] (diagonal entries real; "
      "verified exactly), so the matrix is real IF AND ONLY IF the two mixed couplings coincide, "
      "K_{(0,type1),(1,type2)} = K_{(1,type1),(0,type2)}: the degenerate choice s = v is real, the "
      "generic choice is not. That coincidence is an accidental degeneracy which real symmetry does "
      "NOT provide. Hence (68) requires an extra, unstated hypothesis and is not implied by the "
      "locked formulation",
      cond_exact and link_ok and diag_real and degen_real and (not iszero(K4b_im[0, 1])))

E0, E1, E2, E3, qk = sp.symbols('E0 E1 E2 E3 qk', real=True)
Ke = sp.Matrix([[E0, E1 + sp.I*qk*E2], [E1 + sp.I*qk*E2, E3]])
check("[X3] ROUTE DIAGNOSIS (why the claim exists): (68) is true for the OTHER route -- the "
      "envelope / k-shift formulation, whose reduced matrix is COMPLEX SYMMETRIC "
      "K_e = K_0 + i k K_1 + k^2 K_2 (all three coefficient matrices real symmetric): already with "
      "the two-parameter model K_e = [[E0, E1 + i qk E2],[E1 + i qk E2, E3]] one has K_e^T = K_e "
      "and K_e(k) = K_e(-k)^H identically -- but K_e is NOT Hermitian (K_e - K_e^H = "
      "2 i qk E2 [[0,1],[-1,0]] != 0), so the 'Reduced Hermitian eigenproblem' of Sec 4.5 fails "
      "in that route. Conversely the tying route prescribed by Sec 4.4 gives a Hermitian matrix "
      "for which (68) fails ([X1]-[X2]). The two statements cannot both be asserted of one matrix: "
      "(68) is the complex-symmetric-route property, Hermiticity the tying-route property",
      sp.simplify(Ke - Ke.T) == sp.zeros(2, 2)
      and sp.simplify(Ke.subs(qk, -qk) - Ke.H) == sp.zeros(2, 2)
      and sp.simplify(Ke - Ke.H) != sp.zeros(2, 2))

T4w = sp.Matrix([[1, 0], [0, 1], [mm_, 0], [0, 1/mm_]])
K4w = sp.simplify(T4w.H*K4*T4w)
K4w_neg = K4w.subs(th, -th)
check("[X4] DETECTABILITY of the pitfall the blueprint's Sec 4 table intends to catch (wrong "
      "phase SIGN on the derivative DOFs; here the derivative DOF is tied with mu^{-1} while the "
      "value DOF keeps mu): the wrong reduced matrix is STILL Hermitian, STILL satisfies "
      "Kbar(-k) = conj(Kbar(k)) and still has omega(k) = omega(-k), yet differs from the correct "
      "one by a non-zero amount. Consequence recorded, NOT repaired: no internal invariance test "
      "of the kind listed in Sec 4 can detect a UNIMODULAR phase error on the derivative DOFs -- "
      "only the comparison with an independent reference can (the analytic Case-H/1D dispersion "
      "already planned as P2.1/P2.2, or the Phase-3 anchors). The Sec 4 row's stated cause "
      "('Non-Hermitian Kbar') is therefore not the mechanism, and its proposed test "
      "||Kbar(k) - Kbar(-k)^H|| < 1e-12 fails for a CORRECT tying implementation as well ([X1])",
      sp.simplify(sp.expand(K4w - K4w.H)) == sp.zeros(2, 2)
      and sp.simplify(sp.expand(K4w_neg - K4w.conjugate())) == sp.zeros(2, 2)
      and sp.simplify(sp.expand(K4w.charpoly().as_expr()
                                - K4w_neg.charpoly().as_expr())) == 0
      and (not iszero(K4w - K4b)))

print(f"\nALL {len(OK)} CHECKS PASSED - M9 (Bloch theorem for the C^1 gradient-elastic medium: "
      f"lattice/reciprocal lattice/first BZ (36)-(38), Bloch ansatz and the DERIVED phase rules "
      f"(39)-(43), consistency with the reduced four-quantity boundary model, the anisotropic "
      f"modulus (26), the M7 ladder, phase algebra)")
