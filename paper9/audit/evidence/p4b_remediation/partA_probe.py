"""Part A pipeline probe: stage-by-stage determinism, no new scientific production.
Only re-runs the *existing* P4B code path at small meshes + pure post-processing."""
import importlib.util, numpy as np, hashlib, math, json
spec = importlib.util.spec_from_file_location("p4b", "/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
P = mod.PARAMS; L = P["Lcell"]; ell = math.sqrt(P["ell2"])
L11, L22, L12 = mod.L_plane(P["l_iso"], P["l_iso"], 0.0)
kx, ky = 0.31*np.pi/L, 0.22*np.pi/L

def h(M):  # hash a sparse matrix by its CSR content
    M = M.tocsr()
    return hashlib.sha256(M.data.tobytes() + M.indices.tobytes() + M.indptr.tobytes()).hexdigest()[:16]

print("== STAGE 1: matrix assembly determinism (same process, repeated builds) ==")
for n in (8, 16):
    K1, M1 = mod.assemble_nxn_bloch(n, kx, ky, L, P["lam"], P["mu"], P["rho"], ell**2, L11, L22, L12)
    K2, M2 = mod.assemble_nxn_bloch(n, kx, ky, L, P["lam"], P["mu"], P["rho"], ell**2, L11, L22, L12)
    print(f"  n={n:2d}: K1==K2 hash {h(K1)}=={h(K2)} : {h(K1)==h(K2)} | M: {h(M1)==h(M2)} | nnz {K1.nnz}/{M1.nnz}")

print("== STAGE 3: eigensolver realization (same matrices, repeated calls) ==")
K8, M8 = mod.assemble_nxn_bloch(8, kx, ky, L, P["lam"], P["mu"], P["rho"], ell**2, L11, L22, L12)
r8 = [float(mod.acoustic_omegas(K8, M8, 2)[0]) for _ in range(4)]
print(f"  n=8  4 calls: {[f'{v:.17f}' for v in r8]}")
print(f"          spread = {max(r8)-min(r8):.3e} | distinct = {len(set(r8))}")

print("== STAGE 4/5/6: post-processing determinism + fit-subset flip point (committed data) ==")
J = json.load(open("/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.json"))
om_ex = J["5i"]["omega_exact"]; oms = J["5i"]["omega"]; hs = [1/n for n in J["5i"]["meshes"]]
def post(oms):
    errs = [abs(o-om_ex)/om_ex for o in oms]
    d = abs(oms[3]-oms[2])/oms[3]
    eps = max(d, errs[3])
    used = [e for e in errs if e > 1e-14]
    return errs, d, eps, len(used)
a, b = post(oms), post(oms)
print(f"  repeated post-processing on identical input identical: {a == b}")
# critical omega(32^2) band for the 1e-14 inclusion predicate (pure post-processing)
lo = om_ex*(1-1e-14); hi = om_ex*(1+1e-14)
print(f"  exclusion window for err32 < 1e-14: omega32 in ({lo:.16f}, {hi:.16f})  width={2*1e-14*om_ex:.3e}")
for tag, w32 in (("committed JSON", oms[3]), ("committed TXT", 1.1648553893287734)):
    d_lo = abs(w32 - om_ex)
    print(f"    {tag:14s} omega32={w32:.16f} |dW|={d_lo:.3e} -> {'EXCLUDED (3-pt fit)' if d_lo < 1e-14*om_ex else 'INCLUDED (4-pt fit)'}")
print(f"  => the inclusion predicate flips when |omega32 - omega_ex| crosses {1e-14*om_ex:.4e} (abs, dimensionless)")
