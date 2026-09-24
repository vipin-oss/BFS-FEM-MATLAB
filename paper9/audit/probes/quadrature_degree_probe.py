#!/usr/bin/env python3
"""P12C Part D audit probe — independent quadrature-degree verification.

Builds the plane-strain bicubic Hermite element (h = 1) from scratch, assembles
K^c, K^g(theta=0, L11=L22=1), M0 with tensor Gauss rules n = 2,3,4 and compares
against an n = 12 reference (exact for the polynomial degrees involved).
Checks the frozen M13/M14 claims: integrand degree six per coordinate,
4x4 = minimal exact rule on a homogeneous rectangle, 3x3 insufficient.

Also verifies (separately) that Gauss-point sampling of a piecewise-constant
indicator in a cut element is NOT exact and carries O(h) area error.

No repository data is read or written; pure audit probe.
"""
import numpy as np

def ph(t, d):
    if d == 0: return [1 - 3*t**2 + 2*t**3, t - 2*t**2 + t**3, 3*t**2 - 2*t**3, -t**2 + t**3]
    if d == 1: return [-6*t + 6*t**2, 1 - 4*t + 3*t**2, 6*t - 6*t**2, -2*t + 3*t**2]
    if d == 2: return [-6 + 12*t, -4 + 6*t, 6 - 12*t, -2 + 6*t]
    raise ValueError

LAM = MU = 1.0
C = np.array([[LAM + 2*MU, LAM, 0.0], [LAM, LAM + 2*MU, 0.0], [0.0, 0.0, MU]])

def assemble(n, L11=1.0, L22=1.0, L12=0.0):
    x, w = np.polynomial.legendre.leggauss(n); x = (x + 1) / 2; w = w / 2
    Kc = np.zeros((32, 32)); Kg = np.zeros((32, 32)); M0 = np.zeros((32, 32))
    for i in range(n):
        for j in range(n):
            xi, yi, ww = x[i], x[j], w[i] * w[j]
            B = np.zeros((3, 32)); Bx = np.zeros((3, 32)); By = np.zeros((3, 32)); N = np.zeros((2, 32))
            for a in range(4):
                for b in range(4):
                    k = a * 4 + b
                    f0x, f0y = ph(xi, 0)[a], ph(yi, 0)[b]
                    d1x, d1y = ph(xi, 1)[a], ph(yi, 1)[b]
                    d2x, d2y = ph(xi, 2)[a], ph(yi, 2)[b]
                    # u basis
                    N[0, k] = f0x * f0y
                    B[0, k] = d1x * f0y; B[1, k] = 0.0;      B[2, k] = f0x * d1y
                    Bx[0, k] = d2x * f0y; Bx[1, k] = 0.0;     Bx[2, k] = d1x * d1y
                    By[0, k] = d1x * d1y; By[1, k] = 0.0;     By[2, k] = f0x * d2y
                    # v basis
                    kk = k + 16
                    N[1, kk] = f0x * f0y
                    B[0, kk] = 0.0;       B[1, kk] = f0x * d1y; B[2, kk] = d1x * f0y
                    Bx[0, kk] = 0.0;      Bx[1, kk] = d1x * d1y; Bx[2, kk] = d2x * f0y
                    By[0, kk] = 0.0;      By[1, kk] = f0x * d2y; By[2, kk] = d1x * d1y
            Kc += ww * (B.T @ C @ B)
            M0 += ww * (N.T @ N)
            Kg += ww * (L11 * (Bx.T @ C @ Bx) + L22 * (By.T @ C @ By) + L12 * (Bx.T @ C @ By + By.T @ C @ Bx))
    return Kc, Kg / 10.0, M0

# monomial exactness sweep on the unit square (tensor rule, per-axis limit 2n-1)
def gauss_1d(n):
    x, w = np.polynomial.legendre.leggauss(n); return (x + 1) / 2, w / 2
print("monomial exactness per axis (max exponent passing both axes, 0..8 sweep):")
for n in (2, 3, 4):
    xq, wq = gauss_1d(n)
    mx = -1
    for p_ in range(9):
        for q_ in range(9):
            num = (wq @ xq**p_) * (wq @ xq**q_)
            if abs(num - 1.0 / ((p_ + 1) * (q_ + 1))) <= 1e-14:
                mx = max(mx, max(p_, q_))
    print(f"  n={n}: largest passing exponent={mx} (theory 2n-1={2*n-1})")

ref = assemble(12)
for n in (2, 3, 4):
    Kc, Kg, M0 = assemble(n)
    r = lambda A, B_: np.linalg.norm(A - B_) / max(np.linalg.norm(B_), 1e-300)
    print(f"n={n}: rel-Frobenius diff vs n=12 reference: Kc={r(Kc, ref[0]):.3e}  Kg={r(Kg, ref[1]):.3e}  M0={r(M0, ref[2]):.3e}")

# indicator-area probe (cut-element, piecewise-constant material)
x, w = np.polynomial.legendre.leggauss(4); x = (x + 1) / 2; w = w / 2
exact = np.pi / 4
print("\nquarter-disc indicator area, 4x4 Gauss per sub-element (exact = pi/4):")
for N in (1, 2, 4, 8, 16, 32):
    h = 1.0 / N
    xs = np.concatenate([h * (x + i) for i in range(N)]); ws = np.tile(w * h, N)
    X, Y = np.meshgrid(xs, xs); W = np.outer(ws, ws)
    est = float(np.sum(W * ((X * X + Y * Y) <= 1.0)))
    print(f"  N={N:2d} h={h:.4f}: err={abs(est - exact):.3e}  err/h={abs(est-exact)/h:.4f}")
