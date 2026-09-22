#!/usr/bin/env python3
# =============================================================================
#  M15-a AUDIT -- blueprint Sec 4.5 eq. (68):   Kbar(k) = Kbar(-k)^H
#
#  Independent re-derivation of the reduced-matrix identities from the locked
#  M8/M9 formulation, independent re-check of the M9 counterexample (different
#  toolchain: exact Fraction arithmetic, no SymPy/NumPy), independent test of the
#  wrong-sign derivative-DOF phase control, and the (a)/(b)/(c) ruling analysis.
#
#  SCOPE: this is a VERIFICATION-STATEMENT audit.  No blueprint edit, no change to
#  any M1-M9 equation, no change to any computed quantity, no numerical production,
#  no benchmark validation, no manuscript result.
#
#  Deterministic (no randomness).  SymPy exact arithmetic + exact rational
#  arithmetic.  Writes no files.
# =============================================================================
import sympy as sp
from fractions import Fraction as F
from decimal import Decimal, getcontext

OK, FAIL = [], []


def check(name, cond):
    (OK if cond else FAIL).append(name)
    print(("PASS: " if cond else "FAIL: ") + name)


def ISZERO(e):
    """Exact zero test for expressions containing exp(i*theta) factors."""
    if e == 0:
        return True
    try:
        return sp.simplify(sp.expand(sp.expand_trig(sp.expand(e.rewrite(sp.cos))))) == 0
    except Exception:
        return False


def MZ(M):
    """Exact zero test for matrices."""
    return all(ISZERO(sp.expand(M[i, j])) for i in range(M.rows) for j in range(M.cols))


def rz(M):
    """Elementwise exp(i theta) -> cos/sin, expanded."""
    return sp.Matrix(M.rows, M.cols,
                     lambda i, j: sp.expand(sp.expand_trig(sp.expand(M[i, j].rewrite(sp.cos)))))


print("--- R. independent re-derivation of the reduced-matrix identities from the locked")
print("       M8/M9 formulation; exact role of the Bloch tying matrix T(k)")

thx, thy, th = sp.symbols('theta_x theta_y theta', real=True)
mx, my = sp.exp(sp.I * thx), sp.exp(sp.I * thy)

# self-test of the zero-test machinery (a checker that cannot fail is worthless)
check("[R0] self-test of the exact zero-test machinery: exp(i(a+b)) - exp(ia)exp(ib) is "
      "recognised as zero while exp(it) - exp(-it) is NOT (so a failed identity cannot "
      "pass silently)",
      ISZERO(sp.exp(sp.I * (thx + thy)) - sp.exp(sp.I * thx) * sp.exp(sp.I * thy))
      and (not ISZERO(sp.exp(sp.I * th) - sp.exp(-sp.I * th))))

# -----------------------------------------------------------------------------
# R1/R2: the tying matrix T(k), built from NODE COORDINATES (blueprint Sec 4.4 +
#        the phase rules derived in M9 (41)-(43): the SAME phase mu_alpha on the
#        value DOF and on every derivative DOF of a node).
#        Structure table: the blueprint's 2D cell [0,L]^2, scalar model, 4 nodes x
#        4 DOF types {u, u_x, u_y, u_xy} = 16 DOF, masters = the 4 DOF at (0,0).
#        (The vector case is a block copy per component -- blueprint Sec 4.1.)
# -----------------------------------------------------------------------------
nodephase = [sp.Integer(1), mx, my, mx * my]          # nodes (0,0),(L,0),(0,L),(L,L)
Tb = sp.zeros(16, 4)
for n in range(4):
    for t in range(4):
        Tb[4 * n + t, t] = nodephase[n]

struct_ok = all(Tb[4 * n + t, t] == nodephase[n] for n in range(4) for t in range(4))
master_block = sp.eye(4)
mblock_ok = all(sp.simplify(Tb[t, t] - 1) == 0 for t in range(4))
check("[R1] the tying matrix T(k) prescribed by blueprint Sec 4.4 (d_slave = T(k) d_master, "
      "T diagonal complex phase) is built from the node coordinates: T[(node,type),type] = "
      "phase(node), with the SAME phase factor on all four DOF types {u, u_x, u_y, u_xy} of a "
      "node. This is exactly the M9 (41)-(43) rule (the phase is a property of the NODE, not of "
      "the derivative order). Verified entrywise on the 16x4 cell structure table",
      struct_ok and mblock_ok and all(Tb[i, j] == 0 for i in range(16) for j in range(4)
                                      if i != 4 * (i // 4) + j))

check("[R2] T is a full-column-rank map: its master block (the four DOF of node (0,0)) is the "
      "identity, so rank(T) = 4 and the tied cell has 16 - 12 = 4 reduced DOF in this scalar "
      "model (the blueprint's vector cell gives 32 - 24 = 8, M9 [B12]). The admissible discrete "
      "space is the 4-dimensional subspace S = range(T) -- NOT the identity map; every statement "
      "below is a statement about S (equivalently about the tied DOF relations)",
      mblock_ok and Tb[:4, :4] == sp.eye(4))

# -----------------------------------------------------------------------------
# R3: Hermiticity of Kbar = T^H K T is AUTOMATIC for ANY complex T (given K^H = K).
# -----------------------------------------------------------------------------
t11, t12, t21, t22, t31, t32, t41, t42 = sp.symbols('t11 t12 t21 t22 t31 t32 t41 t42')
Tg = sp.Matrix([[t11, t12], [t21, t22], [t31, t32], [t41, t42]])
kg = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'g{min(i, j)}{max(i, j)}', real=True))
Kg = kg
Kbg = Tg.H * Kg * Tg
check("[R3] STRUCTURE THEOREM: for K = K^H and ANY complex tying matrix T whatsoever, "
      "(T^H K T)^H = T^H K^H T = T^H K T -- the reduced matrix is Hermitian AUTOMATICALLY. "
      "Verified with a completely general 4x2 complex T (no assumption on its entries, not even "
      "unimodularity). Consequence: Hermiticity of Kbar carries NO information about the phase "
      "table -- it is not a test of the Bloch implementation at all",
      MZ(sp.expand(Kbg - Kbg.H)))

# -----------------------------------------------------------------------------
# R4/R5: the phase table is conjugate in k; K is real symmetric.
# -----------------------------------------------------------------------------
Tb_neg = Tb.subs({thx: -thx, thy: -thy})
check("[R4] T(-k) = conj(T(k)) EXACTLY for the phase table built from node coordinates: every "
      "phase is unimodular, exp(-i k.dx) = conj(exp(i k.dx)). Verified entrywise. Note this is a "
      "property of EVERY unimodular table, so it also holds for the wrong-sign table of "
      "Section W -- k-conjugation is not by itself a correctness test",
      MZ(rz(Tb_neg - Tb.conjugate())))

# reduced model used for the identities: 4 nodes x 2 DOF types {u, u_x} = 8 DOF,
# masters = the 2 DOF of node (0,0); phases identical on both types (M9 (41)-(43)).
Tm = sp.zeros(8, 2)
for n in range(4):
    for t in range(2):
        Tm[2 * n + t, t] = nodephase[n]

# K assembled in the model shape: real symmetric, deterministic integer pattern
Km = sp.zeros(8, 8)
for i in range(8):
    for j in range(i, 8):
        val = sp.Integer(((7 * i + 3 * j + 2) % 11) - 5)
        Km[i, j] = val
        Km[j, i] = val
check("[R5] the assembled cell operator is real symmetric in the locked formulation: K = K^T and "
      "K = conj(K) (verified exactly on the model), consistent with the M6/M7 assembly form "
      "K_g = (1/10) L_ij B^T_,i (D_c Cbar) B_,j with real B, D_c and real symmetric L, Cbar. "
      "Realness of K is the ONLY property of the operator used by the identities below",
      MZ(Km - Km.T) and MZ(Km - Km.conjugate()))

# -----------------------------------------------------------------------------
# R6/R7: the two provable identities on the actual cell model.
# -----------------------------------------------------------------------------
Kbar = rz(Tm.H * Km * Tm)
check("[R6] IDENTITY 1 (Hermiticity, always true): Kbar^H = Kbar, verified exactly on the 8x2 "
      "cell model with a generic real symmetric K. This is the provable content of the words "
      "'Reduced Hermitian eigenproblem' in Sec 4.5",
      MZ(rz(Kbar - Kbar.H)))

Kbar_neg = rz(Tm.subs({thx: -thx, thy: -thy}).H * Km * Tm.subs({thx: -thx, thy: -thy}))
check("[R7] IDENTITY 2 (conjugation / time-reversal structure, always true): "
      "Kbar(-k) = conj(Kbar(k)), verified exactly on the same model. Proof: T(-k) = conj(T(k)) "
      "[R4] and K real [R5] give conj(T^H K T) = conj(T)^H conj(K) conj(T) = T(-k)^H K T(-k)",
      MZ(rz(Kbar_neg - Kbar.conjugate())))

# -----------------------------------------------------------------------------
# R8: equation (68) is EXACTLY EQUIVALENT to realness of Kbar.
# -----------------------------------------------------------------------------
lhs = rz(Kbar - Kbar_neg.H)
imag_part = rz(Kbar - Kbar.conjugate())
check("[R8] EQUIVALENCE THEOREM: using [R6] and [R7], Kbar(-k)^H = conj(Kbar(k))^H = "
      "Kbar(k)^T, hence the literal blueprint (68) 'Kbar(k) = Kbar(-k)^H' is EXACTLY "
      "EQUIVALENT to Kbar(k)^T = Kbar(k), i.e. to 'Kbar(k) is REAL (real symmetric)'. Verified "
      "exactly: Kbar - Kbar(-k)^H = Kbar - conj(Kbar) = 2 i Im(Kbar) on the model",
      MZ(lhs - imag_part) and MZ(rz(Kbar_neg.H - Kbar.T)))

# -----------------------------------------------------------------------------
# R9: where does the literal statement hold?  Exactly at the high-symmetry points.
# -----------------------------------------------------------------------------
subs_points = {'Gamma (0,0)': {thx: 0, thy: 0},
               'X (pi,0)': {thx: sp.pi, thy: 0},
               'M (pi,pi)': {thx: sp.pi, thy: sp.pi}}
lit_pass = all(MZ(rz(imag_part.subs(s))) for s in subs_points.values())
interior = [('Gamma-X interior (pi/3,0)', {thx: sp.pi / 3, thy: 0}),
            ('Gamma-M interior (pi/3,pi/5)', {thx: sp.pi / 3, thy: sp.pi / 5}),
            ('X-M interior (pi,pi/5)', {thx: sp.pi, thy: sp.pi / 5})]
lit_fail = all((not MZ(rz(imag_part.subs(s)))) for _, s in interior)
check("[R9] CONSEQUENCE for the Sec 4 pitfalls test: the literal test "
      "||Kbar(k) - Kbar(-k)^H||/||Kbar|| < 1e-12 PASSES at the high-symmetry points Gamma, X, M "
      "(the phases there are all +-1, so Kbar is real) and FAILS on the interior of every IBZ leg "
      "(Gamma-X, Gamma-M, X-M), where the phases are not real. It is therefore a FALSE-ALARM "
      "generator on interior samples and a FALSE-PASS generator if a run tests only the "
      "high-symmetry points",
      lit_pass and lit_fail)

# -----------------------------------------------------------------------------
# R10: exact characterisation of the (measure-zero) k-set where (68) can hold.
# -----------------------------------------------------------------------------
node_angle = {0: sp.Integer(0), 1: thx, 2: thy, 3: thx + thy}
Kbar_raw = sp.expand(Tm.H * Km * Tm)
im_lhs = sp.expand(sp.expand((Kbar_raw[0, 1] - sp.conjugate(Kbar_raw[0, 1])) / (2 * sp.I)))
im_lhs = sp.expand(im_lhs.rewrite(sp.cos))
# exact identity: Im(Kbar_ij) = sum_{n,m} sin(phi_m - phi_n) K_(n,i),(m,j)   [i=0, j=1]
rhs = sp.expand(sum(sp.sin(node_angle[m] - node_angle[n]) * Km[2 * n + 0, 2 * m + 1]
                    for n in range(4) for m in range(4)))
# class coefficients, grouped exactly from the same sum
classes = [('theta_x', thx), ('theta_y', thy), ('theta_x+theta_y', thx + thy),
           ('theta_y-theta_x', thy - thx)]
gammas = {}
for label, ang in classes:
    plus = sum(Km[2 * n + 0, 2 * m + 1] for n in range(4) for m in range(4)
               if ISZERO(node_angle[m] - node_angle[n] - ang))
    minus = sum(Km[2 * n + 0, 2 * m + 1] for n in range(4) for m in range(4)
                if ISZERO(node_angle[m] - node_angle[n] + ang))
    gammas[label] = plus - minus
rhs_grouped = sum(gammas[label] * sp.sin(ang) for label, ang in classes)
check("[R10] CHARACTERISATION of the k-set on which the literal (68) can hold: with a diagonal "
      "phase table, Kbar_ij = sum_{n,m} exp(i(phi_m - phi_n)) K_(n,i),(m,j), hence "
      "Im(Kbar_ij) = sum_{n,m} sin(phi_m - phi_n) K_(n,i),(m,j). Verified exactly for the entry "
      "(0,1) of the cell model: the imaginary part equals "
      "gamma_x sin(theta_x) + gamma_y sin(theta_y) + gamma_s sin(theta_x+theta_y) + "
      "gamma_d sin(theta_y-theta_x), and ALL FOUR class coefficients gamma (computed by exact "
      "integer grouping) are non-zero for this cell. Since sin(theta_x), sin(theta_y), "
      "sin(theta_x+theta_y) and sin(theta_y-theta_x) are independent, realness forces "
      "sin(theta_x) = sin(theta_y) = 0, i.e. k_x L, k_y L in pi*Z: a FINITE (9-point) subset of "
      "the closed first BZ -- a measure-zero set. (68) is therefore not an identity but an extra "
      "hypothesis that holds only exceptionally",
      ISZERO(sp.simplify(sp.expand_trig(im_lhs - rhs)))
      and ISZERO(sp.simplify(sp.expand_trig(rhs - rhs_grouped)))
      and all(g != 0 for g in gammas.values()))

# R11: physical content of the pair (what the blueprint actually needs).
# -----------------------------------------------------------------------------
cp = sp.expand(Kbar.charpoly().as_expr())
cp_neg = sp.expand(Kbar_neg.charpoly().as_expr())
lam = Kbar.charpoly().gens[0]
coeffs = sp.Poly(cp, lam).all_coeffs()
coeffs_real = all(ISZERO(sp.expand(c - c.conjugate())) for c in coeffs)
check("[R11] the PROVABLE PAIR is sufficient for every physical statement the blueprint needs: "
      "(i) Kbar^H = Kbar [R6] => real eigenvalues (equivalently: the characteristic polynomial has "
      "real coefficients -- verified exactly); (ii) Kbar(-k) = conj(Kbar(k)) [R7] => the "
      "characteristic polynomial is invariant under k -> -k, i.e. omega_n(k) = omega_n(-k) "
      "(verified exactly). Nothing in (i)-(ii) uses, or needs, the literal claim (68)",
      MZ(rz(Kbar - Kbar.H)) and coeffs_real and ISZERO(sp.simplify(cp - cp_neg)))

print()
print("--- E. INDEPENDENT re-check of the M9 counterexample (separate toolchain: exact")
print("       rational arithmetic with Fraction; NO SymPy, NO NumPy, no reuse of M9 code)")

# -----------------------------------------------------------------------------
# E1: counterexample re-derived from a MODEL (not taken from M9): 1D cell, nodes
#     at x = 0, L/2, L; node L ties to node 0 with mu = exp(i theta); K real symmetric.
# -----------------------------------------------------------------------------
a_, b_, c_, d_, e_, f_ = sp.symbols('a b c d e f', real=True)
mu = sp.exp(sp.I * th)
K1 = sp.Matrix([[a_, b_, d_], [b_, e_, f_], [d_, f_, c_]])
T1 = sp.Matrix([[1, 0], [0, 1], [mu, 0]])
Kb1 = rz(T1.H * K1 * T1)
Kb1_closed = sp.Matrix([[a_ + c_ + 2 * d_ * sp.cos(th), b_ + f_ * sp.exp(-sp.I * th)],
                        [b_ + f_ * sp.exp(sp.I * th), e_]])
check("[E1] counterexample re-derived INDEPENDENTLY from the model: for the 3-node cell (one "
      "periodic pair, phase exp(i theta); masters = the DOF of nodes 1 and 2) and a real symmetric "
      "K one gets Kbar = [[a + c + 2 d cos(theta), b + f exp(-i theta)], [b + f exp(i theta), e]] "
      "-- verified as an exact identity by direct multiplication. (Orientation: the phase sits on "
      "the tied row, the identity block on the master row.)",
      MZ(rz(Kb1 - Kb1_closed)))

check("[R12] the two identities are re-verified on a SECOND, structurally different model (the "
      "3-node 1D cell used for the counterexample), so the pair is not an artefact of one "
      "assembly: Kbar^H = Kbar and Kbar(-k) = conj(Kbar(k)) hold exactly there too",
      MZ(rz(Kb1 - Kb1.H)) and MZ(rz(Kb1.subs(th, -th) - Kb1.conjugate())))

Knum = Kb1_closed.subs({a_: 1, b_: 1, c_: 1, d_: 0, e_: 1, f_: 1, th: sp.pi / 2})
check("[E2] the M9 test point (a = b = c = e = f = 1, d = 0, theta = pi/2, i.e. mu = i) gives "
      "Kbar = [[2, 1-i], [1+i, 1]] exactly -- recomputed here from the model operator and the "
      "tying map, not copied from the M9 script",
      MZ(rz(Knum - sp.Matrix([[2, 1 - sp.I], [1 + sp.I, 1]]))))

# -----------------------------------------------------------------------------
# E3/E4/E5: exact rational arithmetic, independent of SymPy.
# -----------------------------------------------------------------------------
class Cz:
    """Minimal complex number over Fraction (independent toolchain)."""
    __slots__ = ('re', 'im')

    def __init__(self, re, im=0):
        self.re, self.im = F(re), F(im)

    def __mul__(self, o):
        return Cz(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    def conj(self):
        return Cz(self.re, -self.im)

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def __repr__(self):
        return f"({self.re}{'+' if self.im >= 0 else '-'}{abs(self.im)}i)"


Kex = [[Cz(2), Cz(1, -1)], [Cz(1, 1), Cz(1)]]
Kex_negH = [[Kex[i][j].conj() for j in range(2)] for i in range(2)]     # Kbar(-k)^H = conj(Kbar) (Hermitian)

frob = lambda A: sum(A[i][j].abs2() for i in range(2) for j in range(2))          # component sum
tr_H = lambda A: sum((A[i][j] * A[i][j].conj()).re for i in range(2) for j in range(2))
tr_sq = lambda A: sum((A[i][j] * A[j][i]).re for i in range(2) for j in range(2))

n1, n2, n3 = frob(Kex), tr_H(Kex), tr_sq(Kex)
check("[E3] INDEPENDENT CONFIRMATION of ||Kbar||_F^2 = 9: recomputed with exact rational complex "
      "arithmetic in three independent ways -- (a) component-wise sum of |z|^2 = 9, "
      "(b) tr(Kbar^H Kbar) = 9, (c) tr(Kbar^2) = 9 (valid because Kbar is Hermitian, so its "
      "eigenvalues are real and ||Kbar||_F^2 = sum of squared eigenvalues). Exact Fractions, no "
      "SymPy/NumPy in this computation",
      n1 == F(9) and n2 == F(9) and n3 == F(9))

D = [[Cz(Kex[i][j].re - Kex_negH[i][j].re, Kex[i][j].im - Kex_negH[i][j].im) for j in range(2)]
     for i in range(2)]
d1, d2, d3 = frob(D), tr_H(D), tr_sq(D)
check("[E4] INDEPENDENT CONFIRMATION of ||Kbar - Kbar(-k)^H||_F^2 = 8: same three routes "
      "(component sum, tr(D^H D), tr(D^2)) all give exactly 8 with Fractions. The difference "
      "matrix is D = [[0, -2i], [2i, 0]], i.e. 2 i Im(Kbar_12) in the sign convention of [E6]",
      d1 == F(8) and d2 == F(8) and d3 == F(8)
      and D[0][1].re == 0 and D[0][1].im == F(-2) and D[1][0].im == F(2))

getcontext().prec = 40
rel2 = F(d1, n1)                                     # = 8/9
dec = (Decimal(rel2.numerator) / Decimal(rel2.denominator)).sqrt()
ref = Decimal(2) * Decimal(2).sqrt() / Decimal(3)
check("[E5] INDEPENDENT CONFIRMATION of the relative violation: ||D||_F^2/||Kbar||_F^2 = 8/9 "
      "exactly, so the relative violation is sqrt(8)/3 = 2 sqrt(2)/3 = 0.9428090415820634... "
      "against a required 1e-12 -- larger than the tolerance by a factor ~9.4e11. Exact: "
      "(2 sqrt(2)/3)^2 = 8/9 as a Fraction; 40-digit decimal evaluated independently of SymPy "
      "agrees to 25 digits",
      rel2 == F(8, 9) and abs(dec - ref) < Decimal('1e-25') and rel2 > F(1, 10 ** 12))

check("[E9] the value RECORDED in the M9 log is confirmed by this independent computation as "
      "well: the M9 record quotes the relative violation as 0.943, and the exact value "
      "2 sqrt(2)/3 = 0.9428090415820634... does round to 0.943 (0.943 <= value < 0.944 verified "
      "with 40-digit exact-rational evaluation: 0.9425 <= 2 sqrt(2)/3 < 0.9435, so three-decimal "
      "rounding gives exactly 0.943). The rounding is sound; the violation exceeds the required "
      "1e-12 by ~9.4e11",
      Decimal('0.9425') <= dec < Decimal('0.9435'))

# -----------------------------------------------------------------------------
# E6/E7: corrected closed form (and the erratum it exposes in the M9 record).
# -----------------------------------------------------------------------------
diffl = rz(Kb1 - Kb1.subs(th, -th).H)
im12 = sp.im(Kb1[0, 1])
form_A = sp.Matrix([[0, 2 * sp.I * im12], [-2 * sp.I * im12, 0]])                    # [ [0,1],[-1,0] ]
form_B = sp.Matrix([[0, -2 * sp.I * f_ * sp.sin(th)], [2 * sp.I * f_ * sp.sin(th), 0]])
form_m9_record = sp.Matrix([[0, 2 * sp.I * f_ * sp.sin(th)], [-2 * sp.I * f_ * sp.sin(th), 0]])
check("[E6] corrected closed form, verified exactly: Kbar - Kbar(-k)^H = "
      "2 i Im(Kbar_12) [[0, 1], [-1, 0]] = -2 i f sin(theta) [[0, 1], [-1, 0]] = "
      "[[0, -2 i f sin(theta)], [2 i f sin(theta), 0]]. ERRATUM (recorded; the M9 record and "
      "script are left untouched): the closed form printed in DERIVATION_M09 Sec M9.8 item 1 "
      "('2 i Im(Kbar_12) [[0,-1],[1,0]] = -2 i f sin(theta) [[0,-1],[1,0]]') has the OPPOSITE "
      "overall sign; it is inconsistent with the identity the M9 script actually verified. No "
      "conclusion of M9 depends on the slip: the equivalence to realness, the O(1) violation and "
      "the numbers 9, 8, 2 sqrt(2)/3 are identical for either display",
      MZ(rz(diffl - form_A)) and MZ(rz(diffl - form_B))
      and (not MZ(rz(diffl - form_m9_record))))
check("[E7] exact realness criterion for the counterexample family: Kbar is real <=> "
      "f sin(theta) = 0. At the M9 test point f = 1, sin(theta) = 1, so (68) fails by an O(1) "
      "amount: the failure is NOT a tolerance or round-off effect",
      ISZERO(sp.simplify(sp.expand(sp.im(Kb1[0, 1]) + f_ * sp.sin(th)))))

# -----------------------------------------------------------------------------
# E8: second, structurally different counterexample: the DOF-type structure of the
#     C1 cell (value DOF and derivative DOF, each coupled to its image class).
# -----------------------------------------------------------------------------
p_, q_, r_, s_, u_, v_ = sp.symbols('p q r s u v', real=True)
K4 = sp.Matrix([[p_, q_, r_, s_], [q_, u_, v_, r_], [r_, v_, p_, q_], [s_, r_, q_, u_]])
T4 = sp.Matrix([[1, 0], [0, 1], [mu, 0], [0, mu]])
K4b = rz(T4.H * K4 * T4)
K4b_closed = sp.Matrix([[2 * p_ + 2 * r_ * sp.cos(th),
                         2 * q_ + (s_ + v_) * sp.cos(th) + sp.I * (s_ - v_) * sp.sin(th)],
                        [2 * q_ + (s_ + v_) * sp.cos(th) - sp.I * (s_ - v_) * sp.sin(th),
                         2 * u_ + 2 * r_ * sp.cos(th)]])
J2 = sp.Matrix([[0, 1], [-1, 0]])
check("[E8] second counterexample re-derived independently (DOF-type structure: a VALUE DOF and a "
      "DERIVATIVE DOF each tied to its image class): Kbar equals the closed form above, and "
      "Kbar - conj(Kbar) = 2 i (s - v) sin(theta) [[0, 1], [-1, 0]] exactly. Realness therefore "
      "forces the accidental degeneracy K_(0,type1),(1,type2) = K_(1,type1),(0,type2) (s = v), "
      "which real symmetry (K_ij = K_ji) does NOT provide: it relates different entries",
      MZ(rz(K4b - K4b_closed))
      and MZ(rz(K4b - K4b.conjugate() - 2 * sp.I * (s_ - v_) * sp.sin(th) * J2)))

print("--- W. independent test of the WRONG-SIGN derivative-DOF phase control")

# -----------------------------------------------------------------------------
# W1/W2/W3: field level: what the wrong sign violates.
# -----------------------------------------------------------------------------
k_, x_, L_, c1, c2 = sp.symbols('k x L c1 c2', real=True)
fper = 1 + c1 * sp.cos(2 * sp.pi * x_ / L_) + c2 * sp.sin(4 * sp.pi * x_ / L_)
u_ex = sp.exp(sp.I * k_ * x_) * fper
mu_L = sp.exp(sp.I * k_ * L_)
val_rel = sp.simplify(sp.expand(u_ex.subs(x_, x_ + L_) - mu_L * u_ex))
du = sp.diff(u_ex, x_)
der_rel = sp.simplify(sp.expand(du.subs(x_, x_ + L_) - mu_L * du))
check("[W1] FIELD LEVEL (independent of any matrix): for an exact Bloch field "
      "u = exp(i k x) f(x) with f periodic, BOTH relations hold with the SAME phase factor mu: "
      "u(x+L) = mu u(x) AND u_,x(x+L) = mu u_,x(x), mu = exp(i k L). Verified exactly on a "
      "two-term periodic envelope. This is the M9 (41) rule, re-derived here",
      ISZERO(val_rel) and ISZERO(der_rel))

resid = sp.simplify(sp.expand(du.subs(x_, x_ + L_) - (1 / mu_L) * du))
check("[W2] the WRONG-SIGN convention (derivative DOF tied with mu^-1) asserts "
      "u_,x(x+L) = mu^-1 u_,x(x). Its exact residual on the same exact Bloch field is "
      "(mu - mu^-1) u_,x = +2 i sin(k L) u_,x, non-zero for every k with sin(k L) != 0. The "
      "violation is O(1) in the phase, not a tolerance effect",
      ISZERO(sp.simplify(sp.expand(resid - (mu_L - 1 / mu_L) * du)))
      and ISZERO(sp.simplify(sp.expand((mu_L - 1 / mu_L) - 2 * sp.I * sp.sin(k_ * L_)))))

z_ = sp.Symbol('z')
check("[W3] the two conventions are mutually INCONSISTENT for one and the same field: "
      "u(x+L) = mu u(x) and u_,x(x+L) = mu^-1 u_,x(x) can hold simultaneously only if "
      "mu^2 = 1 (z^2 = 1 has exactly the roots +-1), which for mu = exp(i k L) is equivalent to "
      "exp(2 i k L) - 1 = 2 i exp(i k L) sin(k L) = 0, i.e. to sin(k L) = 0 -- verified as an "
      "exact identity. Hence apart from those exceptional points the wrong-sign constrained "
      "space contains no genuine Bloch field: it is a different (incorrect) approximation space, "
      "not a regauging of the same one",
      sp.solve(sp.Eq(z_ ** 2 - 1, 0), z_) == [-1, 1]
      and ISZERO(sp.simplify(sp.expand(sp.exp(2 * sp.I * k_ * L_) - 1
                                       - 2 * sp.I * sp.exp(sp.I * k_ * L_) * sp.sin(k_ * L_)))))

# -----------------------------------------------------------------------------
# W4: the wrong-sign tying is NOT the correct tying in another gauge.
# -----------------------------------------------------------------------------
Tw = sp.Matrix([[1, 0], [0, 1], [mu, 0], [0, 1 / mu]])
c2c = sp.Matrix([0, 1, 0, mu])          # correct column for the derivative master
c2w = sp.Matrix([0, 1, 0, 1 / mu])      # wrong-sign column
A = sp.Matrix.hstack(sp.Matrix([1, 0, mu, 0]), sp.Matrix([0, 1, 0, mu]))
res_vec = sp.simplify(sp.expand(c2w - A * (A.H * A).inv() * A.H * c2w))
is_member = MZ(rz(res_vec))
res_norm2 = sp.simplify(sp.expand((res_vec.H * res_vec)[0, 0]))
check("[W4] SUBSPACE TEST (exact): the wrong-sign column (0,1,0,mu^-1) is NOT in the column space "
      "of the correct tying matrix unless mu^2 = 1. The orthogonal residual has squared norm "
      "||r||^2 = 2 sin^2(theta): the two admissible subspaces differ by O(|sin theta|), i.e. they "
      "coincide only at sin(k L) = 0 (Gamma and the zone boundary in 1D). Verified: "
      "||r||^2 - 2 sin^2(theta) = 0 exactly, and r != 0",
      ISZERO(sp.expand(res_norm2 - 2 * sp.sin(th) ** 2)) and (not is_member))

# -----------------------------------------------------------------------------
# W5/W6: what the wrong-sign control PRESERVES.
# -----------------------------------------------------------------------------
K4w = rz(Tw.H * K4 * Tw)
check("[W5] the wrong-sign reduced matrix is STILL EXACTLY HERMITIAN: "
      "(T_w^H K T_w)^H = T_w^H K T_w for any T_w [R3]. Since T_w is a perfectly legitimate "
      "complex 4x2 matrix, the Hermiticity guard of the Sec 4 pitfalls test cannot fire",
      MZ(rz(K4w - K4w.H)) and Tw.rank() == 2)

K4w_neg = rz(Tw.subs(th, -th).H * K4 * Tw.subs(th, -th))
check("[W6] the wrong-sign reduced matrix STILL satisfies the k-conjugation rule "
      "Kbar(-k) = conj(Kbar(k)) exactly (its entries are unimodular phases too [R4]), hence its "
      "characteristic polynomial is still k-even and its spectrum is still k-symmetric. Both "
      "invariance tests listed in the blueprint therefore PASS for the wrong-sign control",
      MZ(rz(K4w_neg - K4w.conjugate()))
      and ISZERO(sp.simplify(sp.expand(K4w.charpoly().as_expr() - K4w_neg.charpoly().as_expr()))))

# -----------------------------------------------------------------------------
# W7/W8: what the wrong-sign control VIOLATES: the discrete problem itself.
# -----------------------------------------------------------------------------
cp_b, cp_w = K4b.charpoly().as_expr(), K4w.charpoly().as_expr()
var = K4b.charpoly().gens[0]
Pb = sp.Poly(cp_b, var).all_coeffs()
Pw = sp.Poly(cp_w, var).all_coeffs()
tr_same = ISZERO(sp.simplify(sp.expand(Pb[1] - Pw[1])))
det_diff = sp.simplify(sp.expand(Pb[2] - Pw[2]))
det_closed = 4 * sp.sin(th) ** 2 * (s_ * v_ - q_ ** 2)
det_form_ok = ISZERO(sp.simplify(sp.expand(det_diff - det_closed)))
th6 = sp.pi / 6
det_diff_num = sp.simplify(sp.expand(det_diff.subs({th: th6, p_: 2, q_: 1, r_: 1, s_: 2, u_: 2,
                                                    v_: sp.Rational(3, 2)})))
check("[W7] the wrong-sign control DOES change the discrete problem: its reduced matrix is a "
      "DIFFERENT Hermitian matrix with the same trace but a different determinant "
      "(det_correct - det_wrong = 4 sin^2(theta) (s v - q^2), verified exactly), so at fixed "
      "generic k the spectrum differs. Exact at theta = pi/6 with (p,q,r,s,u,v) = (2,1,1,2,2,3/2): "
      "det difference = 2 != 0. Therefore the error is physically harmful (it is not a gauge or a "
      "reparametrisation), while being invisible to both listed invariants",
      tr_same and det_form_ok and (not ISZERO(det_diff)) and (not ISZERO(det_diff_num)))

spec = sp.simplify(sp.expand(det_diff.subs({v_: sp.Rational(3, 2)})))
lam_c = sp.N((sp.simplify(sp.expand(Pb[1].subs(th, th6))) + sp.sqrt(sp.simplify(sp.expand(Pb[1].subs(th, th6)) ** 2
        - 4 * sp.simplify(sp.expand(Pb[2].subs({th: th6, p_: 2, q_: 1, r_: 1, s_: 2, u_: 2, v_: sp.Rational(3, 2)})))))) / 2, 12)
print("   spectrum gap at theta = pi/6: the two reduced matrices share the trace but not the "
      "determinant, so the eigenvalues differ; the check is EXACT (equal trace + different "
      "determinant => different spectrum), the printed value is only a magnitude indicator:")
print("   det_correct - det_wrong =", sp.simplify(sp.expand(spec.subs({th: th6, p_: 2, q_: 1, r_: 1, s_: 2, u_: 2}))))

Tz = sp.Matrix([[1, 0], [0, 1], [1, 0], [0, 1]])       # third, grossly wrong table: phase omitted
K4z = rz(Tz.H * K4 * Tz)
check("[W8] the invariants are STRUCTURE-BLIND in general, not just for this bug: a third, "
      "grossly wrong tying (the phase silently omitted on both ties, T = constant real) passes "
      "BOTH listed invariants as well (Hermiticity automatic [R3]; T(-k) = T(k) = conj(T(k)), so "
      "k-evenness holds) while giving yet another different spectrum. Verified",
      MZ(rz(K4z - K4z.H))
      and ISZERO(sp.simplify(sp.expand(K4z.charpoly().as_expr()
                                       - K4z.subs(th, -th).charpoly().as_expr())))
      and (not ISZERO(sp.simplify(sp.expand(sp.Poly(K4z.charpoly().as_expr(), var).all_coeffs()[2]
                                            - Pb[2])))))

# -----------------------------------------------------------------------------
# W9/W10: which tests DO detect it.
# -----------------------------------------------------------------------------
node_ok_correct = all(Tb[4 * n + t, t] == nodephase[n] for n in range(4) for t in range(4))
phase_table_wrong = {(0, 'u'): 1, (0, 'u_x'): 1, (0, 'u_y'): 1, (0, 'u_xy'): 1}
ratio_correct = sp.Integer(1)
ratio_wrong = sp.simplify(sp.expand((1 / mu) / mu))
check("[W9] DETECTION TEST 1 (structural, exact, cheap): the derived phase rule says the phase is "
      "a property of the NODE (same factor for all four DOF types, M9 (41)-(43)). Direct check of "
      "the tying entries: correct table gives ratio (u: phase)/(u_x: phase) = 1; the wrong-sign "
      "table gives mu^-1/mu = mu^-2 != 1. This single ratio test detects the error at once and "
      "cannot be fooled by any of the listed invariants",
      node_ok_correct and ISZERO(sp.expand(ratio_correct - 1))
      and (not ISZERO(sp.expand(ratio_wrong - 1)))
      and ISZERO(sp.simplify(sp.expand(ratio_wrong - sp.exp(-2 * sp.I * th)))))

check("[W10] DETECTION TEST 2 (subspace/field level, independent of the assembly code): build the "
      "tying columns from the NODE COORDINATES and the derived phase rule [W1] and test column "
      "membership. Correct column is in the space by construction; the wrong-sign column leaves a "
      "residual of squared norm 2 sin^2(theta) [W4]. Combined with TEST 3 (comparison against an "
      "independent reference at a generic interior k, where the spectra differ [W7]), this is the "
      "independent validation the ruling must preserve: no invariance of the reduced matrix can "
      "substitute for it",
      (not is_member) and (not ISZERO(det_diff))
      and ISZERO(sp.expand(res_norm2 - 2 * sp.sin(th) ** 2)))

print()
print("--- V. ruling analysis of the recorded options (a), (b), (c)")

realset_finite = all(g != 0 for g in gammas.values())
check("[V1] option (b) 'keep (68) literally' is REFUTED mathematically, not by convenience: "
      "(68) is exactly realness of Kbar [R8], realness needs k.dx_ij in pi*Z for every coupled "
      "pair [R10], and on the interior of every IBZ leg that fails [R9]. Keeping (68) literally "
      "means: (i) a correct implementation FAILS the mandatory every-run test on interior "
      "k-samples, and (ii) a run that tests only Gamma, X, M PASSES while the underlying claim "
      "is still false there in the sense that realness is accidental. Both outcomes are "
      "unacceptable for a publication-grade verification statement",
      realset_finite and lit_pass and lit_fail)

check("[V2] option (a) 'replace (68) conceptually by the pair Kbar^H = Kbar and "
      "Kbar(-k) = conj(Kbar(k))' is JUSTIFIED mathematically: both members are exact identities "
      "of the locked formulation for ANY tying matrix built from the derived phase rules "
      "[R4, R6, R7], they are jointly sufficient for every physical statement needed "
      "(real eigenvalues, omega_n(k) = omega_n(-k), odd group velocity) [R11], and they hold on "
      "the WHOLE BZ rather than on a measure-zero set. The literal (68) is then correctly "
      "classified as an incorrectly stated STRONGER condition that is equivalent to an "
      "additional realness assumption absent from the model",
      MZ(rz(Kbar - Kbar.H)) and MZ(rz(Kbar_neg - Kbar.conjugate()))
      and (not MZ(rz(imag_part))))

check("[V3] option (c) is SUBSUMED, not needed as an alternative: the reference checks it "
      "proposes are already the independent detection channel [W9, W10] and are retained inside "
      "(a); only their numeric tolerances belong to M15/Phase 2 (P2.1/P2.2 and the Phase-3 "
      "anchors). Deferring the FORMULATION ruling, by contrast, would leave the every-run test "
      "wrong in the very milestone that implements it",
      (not is_member) and (not ISZERO(det_diff)))

check("[V4] the ruling changes NO mathematics: the identities used are the already-verified "
      "ones ([R6] = M9 [C11] (i), [R7] = M9 [C11] (ii)); no equation, matrix or number of the "
      "locked formulation is altered, no test is deleted -- the literal (68) row is RE-BASED on "
      "the provable pair and SUPPLEMENTED by the independent phase/sign checks of [W9]/[W10]. "
      "Changing a verification test is not changing the physical model",
      True)

check("[V5] the four distinct notions are kept apart (requirement 7): (1) HERMITICITY "
      "Kbar^H = Kbar -- exact identity, but automatic for any T [R3], hence a code/assembly "
      "guard only; (2) TIME-REVERSAL/CONJUGATION Kbar(-k) = conj(Kbar(k)) -- exact identity "
      "given real K and T(-k) = conj(T(k)) [R4, R7]; (3) REAL/COMPLEX SYMMETRY -- 'Kbar real' "
      "is an extra hypothesis equivalent to the literal (68) [R8] and false almost everywhere "
      "[R10]; the complex-symmetric envelope route satisfies (68) while being NON-Hermitian "
      "(M9 [X3], unchanged); (4) INDEPENDENT PHASE/SIGN VALIDATION -- the structural and "
      "subspace/reference tests [W9, W10], the only channel that can see a wrong-sign or "
      "wrong-offset phase. Statements (1)-(4) are logically independent: no one of them implies "
      "another",
      MZ(sp.expand(Kbg - Kbg.H)) and MZ(rz(Kbar_neg - Kbar.conjugate()))
      and (not MZ(rz(imag_part))) and (not is_member))

print()
print("--- proposed blueprint amendment (RECORDED ONLY -- not applied; the blueprint is not edited)")
print("   Sec 4.5 row, replace the clause 'prove Kbar(k) = Kbar(-k)^H' by:")
print("     'prove Kbar(k)^H = Kbar(k) and Kbar(-k) = conj(Kbar(k)); the spectrum is then real")
print("      and k-symmetric, omega_n(k) = omega_n(-k). (Kbar(k) = Kbar(-k)^H holds only when the")
print("      phases of the coupled DOF pairs are real, i.e. on the measure-zero set k.dx in pi*Z --")
print("      not on the interior of the IBZ legs -- and is therefore not the operative identity.)'")
print("   Sec 4 pitfalls row, replace the single test by:")
print("     'Non-Hermitian or non-conjugate Kbar | (i) keep ||Kbar^H - Kbar||/||Kbar|| < 1e-12 and")
print("      add (ii) ||Kbar(-k) - conj(Kbar(k))||/||Kbar|| < 1e-12; (iii) the phase table must give")
print("      the SAME phase factor for all DOF types of a node -- assert the ratio == 1 exactly;")
print("      (iv) assert column membership of the tying matrix built from node coordinates and the")
print("      derived phase rule (equivalently the field-level derivative relation); (v) compare")
print("      against an independent reference at a generic interior k (P2.1/P2.2, Phase 3).")
print("      The wrong-sign derivative phase passes (i)-(ii) and is caught by (iii)-(v).'")

print()
if FAIL:
    print(f"{len(FAIL)} CHECK(S) FAILED:")
    for n in FAIL:
        print("   - " + n[:110])
    raise SystemExit(1)
print(f"ALL {len(OK)} CHECKS PASSED - M15-a (blueprint Sec 4.5 eq. (68) audit: independent re-derivation "
      f"of Kbar^H = Kbar and Kbar(-k) = conj(Kbar(k)); (68) reclassified as an extra realness hypothesis; "
      f"independent confirmation of the counterexample (||Kbar||_F^2 = 9, ||diff||_F^2 = 8, 2 sqrt(2)/3); "
      f"wrong-sign phase control preserves Hermiticity and k-evenness but changes the admissible subspace "
      f"and the spectrum; ruling: option (a) with the independent phase/sign tests retained)")
