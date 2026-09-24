"""P12E: independent certification of the Route-F eigenvalue values.
Checks (a) eigenpair residuals (backward-error certificate), (b) seed-to-seed variation at
the authorized tolerance, (c) a tighter tolerance.  Scratch only."""
import os, time
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[v] = "1"
import numpy as np, importlib.util, math
from scipy.sparse.linalg import eigsh
spec = importlib.util.spec_from_file_location("p4b", "/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
P = mod.PARAMS; L = P["Lcell"]; ell = math.sqrt(P["ell2"]); l_iso = P["l_iso"]
L11, L22, L12 = mod.L_plane(l_iso, l_iso, 0.0)
kx, ky = 0.31*np.pi/L, 0.22*np.pi/L
om_ex = np.sqrt(mod.ombar2_T(np.hypot(kx,ky)*L/np.pi, ell/L, mod.leff2_dir(l_iso,l_iso,0,0)))*mod.omega0(P["mu"],P["rho"],L)

def solve(Kh, Mh, tol, seed, k=4):
    nd = Kh.shape[0]
    t0 = time.time()
    w, v = eigsh(Kh, k=k, M=Mh, which="SM", tol=tol, maxiter=20000,
                 v0=np.random.default_rng(seed).standard_normal(nd))
    return np.sort(np.real(w)), v, time.time()-t0

print(f"{'n':>3s} {'tol':>7s} {'seed':>9s} {'time':>7s} {'omega_T':>20s} {'rel vs closed form':>19s} {'backward err':>13s} {'gap lam2/lam1':>13s}")
results = {}
for n in (8, 16, 32):
    Kh, Mh = mod.assemble_nxn_bloch(n, kx, ky, L, P["lam"], P["mu"], P["rho"], ell**2, L11, L22, L12)
    for tol, seed in ((1e-14, 20260924), (1e-14, 7)):
        w, v, dt = solve(Kh, Mh, tol, seed)
        x = np.real(v[:, 0]); lam = w[0]
        Kx = Kh @ x; Mx = Mh @ x
        r = Kx - lam * Mx
        bwd = np.linalg.norm(r) / (np.linalg.norm(Kx) + abs(lam)*np.linalg.norm(Mx))
        omT = math.sqrt(max(lam, 0.0))
        results[(n, tol, seed)] = omT
        print(f"{n:>3d} {tol:>7.0e} {seed:>9d} {dt:>6.1f}s {omT:>20.16f} {abs(omT-om_ex)/om_ex:>19.3e} {bwd:>13.3e} {w[1]/w[0]:>13.6f}", flush=True)
    if n == 32:
        w, v, dt = solve(Kh, Mh, 1e-15, 20260924)
        omT = math.sqrt(max(w[0], 0.0)); results[(32, 1e-15, 20260924)] = omT
        print(f"{n:>3d} {1e-15:>7.0e} {20260924:>9d} {dt:>6.1f}s {omT:>20.16f} {abs(omT-om_ex)/om_ex:>19.3e} {'-':>13s} {'-':>13s}", flush=True)

print()
for n in (8, 16, 32):
    a, b = results[(n, 1e-14, 20260924)], results[(n, 1e-14, 7)]
    print(f"n={n:2d}: seed-to-seed |domega| = {abs(a-b):.3e} (relative {abs(a-b)/a:.3e})")
if (32, 1e-15, 20260924) in results:
    c = results[(32, 1e-15, 20260924)]
    print(f"n=32: tol 1e-14 -> 1e-15 change |domega| = {abs(results[(32,1e-14,20260924)]-c):.3e} (relative {abs(results[(32,1e-14,20260924)]-c)/c:.3e})")
print()
print("committed (tol=1e-12 era) omega32 values: JSON 1.1648553893289162 | TXT 1.1648553893287734")
print("accurate omega32 (this probe)           :", f"{results[(32,1e-14,20260924)]:.16f}")
print("implied true err32 (vs closed form)     :", f"{abs(results[(32,1e-14,20260924)]-om_ex)/om_ex:.3e}")
