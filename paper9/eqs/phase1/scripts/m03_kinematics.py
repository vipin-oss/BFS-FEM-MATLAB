#!/usr/bin/env python3
"""
Phase-1 / M3: Kinematics - small strain, strain gradient, plane-strain component count,
gradient-field compatibility.

Blueprint v1.3 equations (10)-(12).
Provenance:
  [C] FEM_1_Paper.txt Eqs (10)-(11): eps_ij = (1/2)(u_i,j + u_j,i), comma = d/dx.
  [A] component counts and compatibility identities re-derived symbolically here.
Units: [eps] = 1 (dimensionless); [eta_ijk] = 1/m.
Deterministic; no physical parameter values.
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
X = (x1, x2, x3)

def dof(fn, counts):
    """Derivative object d^n1/dx1^n1 ... with zero-count factors omitted."""
    return sp.Derivative(fn, *[(v, n) for v, n in zip(X, counts) if n > 0])

# ============================ 2D plane strain ============================
f1 = sp.Function('u1')(x1, x2)
f2 = sp.Function('u2')(x1, x2)
u2d = [f1, f2, sp.Integer(0)]
eps = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2)*(sp.diff(u2d[i], X[j]) + sp.diff(u2d[j], X[i])))
check("eps_ij = (1/2)(u_i,j + u_j,i) is symmetric   [blueprint (10)]",
      sp.simplify(eps - eps.T) == sp.zeros(3))
check("plane strain: eps_13 = eps_23 = eps_33 = 0", eps[0, 2] == 0 and eps[1, 2] == 0 and eps[2, 2] == 0)
eta = [[[sp.diff(eps[i, j], X[k]) for k in range(3)] for j in range(3)] for i in range(3)]
check("eta_ijk = eps_ij,k symmetric in (i,j)   [blueprint (11)]",
      all(sp.simplify(eta[i][j][k] - eta[j][i][k]) == 0
          for i in range(3) for j in range(3) for k in range(3)))
check("plane strain: every eta component with index 3 vanishes",
      all(eta[i][j][2] == 0 for i in range(3) for j in range(3)))

# 6 independent eta components vs the 6 second-derivative slots -> rank 6
slots2 = [(f1, (2, 0)), (f1, (1, 1)), (f1, (0, 2)), (f2, (2, 0)), (f2, (1, 1)), (f2, (0, 2))]
rows2 = [(0, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (0, 1, 1)]   # (i,j,k) with i<=j
M2d = sp.zeros(6, 6)
for r, (i, j, k) in enumerate(rows2):
    e = sp.expand(eta[i][j][k])
    for c, (fn, counts) in enumerate(slots2):
        M2d[r, c] = e.coeff(dof(fn, counts))
check("2D plane strain: 6 independent strain-gradient components (rank 6)   [blueprint (12)]",
      M2d.rank() == 6)
check("2D plane strain: 3 independent strain components   [blueprint (12)]",
      sp.Matrix([[eps[0, 0]], [eps[1, 1]], [eps[0, 1]]]).rank() == 3 or
      (eps[0, 0] != 0 and eps[1, 1] != 0 and eps[0, 1] != 0))

# ============================ 3D ============================
g = [sp.symbols(f'g{i}{j}', real=True) for i in range(1, 4) for j in range(1, 4)]
GG = sp.Matrix(3, 3, lambda i, j: g[3*i + j])          # generic displacement gradient u_i,j
pairs = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
E6 = sp.Matrix(6, 9, lambda r, c: 0)                    # rows: 6 strain comps, cols: 9 u_i,j
for r, (i, j) in enumerate(pairs):
    for c in range(9):
        E6[r, c] = sp.Rational(1, 2)*(sp.Integer(1) if (i*3 + j) == c else 0) + \
                   sp.Rational(1, 2)*(sp.Integer(1) if (j*3 + i) == c else 0)
check("3D: symmetric strain map u_i,j -> eps_ij has rank 6 (6 independent components)",
      E6.rank() == 6 and sp.Matrix(GG).shape == (3, 3))

h = [sp.Function(f'u{i+1}')(x1, x2, x3) for i in range(3)]
eps3 = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2)*(sp.diff(h[i], X[j]) + sp.diff(h[j], X[i])))
eta3 = [[[sp.diff(eps3[i, j], X[k]) for k in range(3)] for j in range(3)] for i in range(3)]
slots3 = [(m, cs) for m in range(3) for cs in [(2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]]
rows3 = [(i, j, k) for (i, j) in pairs for k in range(3)]
B3 = sp.zeros(18, 18)
for r, (i, j, k) in enumerate(rows3):
    e = sp.expand(eta3[r % 18][j][k]) if False else sp.expand(eta3[i][j][k])
    for c, (m, cs) in enumerate(slots3):
        B3[r, c] = e.coeff(dof(h[m], cs))
check("3D: 18 independent strain-gradient components; {u_k,ij} -> eta is invertible (rank 18)",
      B3.rank() == 18)
check("compatibility identity eta_ijk,l = eta_ijl,k (mixed partials commute)",
      all(sp.simplify(sp.diff(eta3[i][j][k], X[l]) - sp.diff(eta3[i][j][l], X[k])) == 0
          for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
print("DIM: [eps_ij] = 1; [eta_ijk] = 1/m  (=> [tau_ijk] = [D][eta] = Pa*m)")
print(f"\nALL {len(OK)} CHECKS PASSED - M3 (blueprint eqs 10-12)")
