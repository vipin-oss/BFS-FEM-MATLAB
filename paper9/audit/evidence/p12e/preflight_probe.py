"""P12E pre-flight: feasibility of the authorized Route-F solver configuration (scratch only).
Computes the 5i sequence with tol=1e-14 + deterministic v0 + pinned threads, reports timing,
errors, four-level fit, residual and P1-P4.  Writes nothing into the repository."""
import os, sys, time
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[v] = "1"
import numpy as np, importlib.util, math
from scipy.sparse.linalg import eigsh
print("numpy", np.__version__, "| thread env pinned to 1", flush=True)
spec = importlib.util.spec_from_file_location("p4b", "/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
P = mod.PARAMS; L = P["Lcell"]
lam, mu, rho = P["lam"], P["mu"], P["rho"]
ell = np.sqrt(P["ell2"]); l_iso = P["l_iso"]
w0 = mod.omega0(mu, rho, L)
le2 = mod.leff2_dir(l_iso, l_iso, 0.0, 0.0); ellbar = ell / L
L11, L22, L12 = mod.L_plane(l_iso, l_iso, 0.0)
kx, ky = 0.31*np.pi/L, 0.22*np.pi/L
kbar = np.hypot(kx, ky)*L/np.pi
om_ex = np.sqrt(mod.ombar2_T(kbar, ellbar, le2))*w0
print(f"om_ex = {om_ex:.17f}  (committed JSON omega_exact = 1.1648553893289133)")

TOL = 1e-14; SEED = 20260924
def v0(nd):
    return np.random.default_rng(SEED).standard_normal(nd)

meshes = [4, 8, 16, 32]
oms, errs, timings = [], [], []
for n in meshes:
    t0 = time.time()
    Kh, Mh = mod.assemble_nxn_bloch(n, kx, ky, L, lam, mu, rho, ell**2, L11, L22, L12)
    ta = time.time()
    nd = Kh.shape[0]
    w, _ = eigsh(Kh, k=4, M=Mh, which="SM", tol=TOL, maxiter=10000, v0=v0(nd))
    w = np.sort(np.real(w))
    omT = float(np.sqrt(np.maximum(w[0], 0.0)))
    tb = time.time()
    err = abs(omT - om_ex)/om_ex
    oms.append(omT); errs.append(err); timings.append((ta-t0, tb-ta))
    print(f"  n={n:2d} nd={nd:5d} assemble={ta-t0:6.2f}s solve={tb-ta:7.2f}s  omT={omT:.17f}  rel_err={err:.6e}", flush=True)

hs = [1.0/n for n in meshes]
slope, lo, hi, se = mod.lsq_loglog_slope(hs, errs)
x = np.log(hs); y = np.log(errs)
yhat = (y.mean() - slope*x.mean()) + slope*x
resid = float(np.max(np.abs(y - yhat)))
d16 = abs(oms[3]-oms[2])/oms[3]
eps = max(d16, errs[3])
P_MIN, R_MAX, FLOOR_MAX = 1.0, math.log(1.5), 1e-9
print()
print(f"four-level fit : slope={slope:.12f} CI95=[{lo:.10f}, {hi:.10f}] se={se:.3e} resid_max={resid:.6f}")
print(f"eps_Delta={eps:.6e}  d16_32={d16:.6e}")
print(f"P1 monotone={all(b<a for a,b in zip(errs,errs[1:]))} | P2 CI-lo>={P_MIN}: {lo>=P_MIN} ({lo:.4f})"
      f" | P3 resid<={R_MAX:.4f}: {resid<=R_MAX} ({resid:.4f}) | P4 floor<={FLOOR_MAX:.0e}: {d16<=FLOOR_MAX} ({d16:.3e})")
print(f"timing total: {sum(a+b for a,b in timings):.1f}s (assemble {sum(a for a,_ in timings):.1f}s, solve {sum(b for _,b in timings):.1f}s)")
print(f"P12D prediction was p ~ 4.11-4.16, CI ~[3.88,4.33]  (not an acceptance target)")
