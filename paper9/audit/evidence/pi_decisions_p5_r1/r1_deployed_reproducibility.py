#!/usr/bin/env python3
"""R-1 minimal measurement — two independent realizations on the DEPLOYED 5i configuration.

Specification (P12AB Part E, exact run required, never executed until now):
  on the deployed 5i configuration (tol = 1e-12, unpinned start vector, n_mesh in {4,8,16,32}),
  execute two independent realizations and record, per level, the relative error e_i and its
  measured reproducibility s_i; then apply frozen Rule R-fit (F = 3 strict, unchanged) and report
  whether the admissible subset and the fit verdict are invariant across realizations.

Nothing in the repository is modified: this script only imports the frozen suite module and calls
its own functions.  Two realization families are measured:

  (a) "unpinned"  - the deployed path exactly as shipped (scipy eigsh with default v0);
  (b) "two-seed"  - the Route-F seed protocol (PCG64 seeds 20260924 and 7) but at the DEPLOYED
                    tolerance 1e-12 (Route-F pins tol = 1e-14; the spec says not to pin it).

Rule R-fit (frozen, P12G/P12H): level i is admissible iff e_i > F * max(s_i, SPREAD_FLOOR),
F = 3.0, SPREAD_FLOOR = 1e-15; at least 3 admissible levels are required to fit; the reported rate
is the least-squares log-log slope over the admissible levels.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

P9 = Path("/home/user/repo/paper9")
sys.path.insert(0, str(P9))

spec = importlib.util.spec_from_file_location("p4b", P9 / "verification" / "suite" / "p4b_5g_to_5i.py")
p4b = importlib.util.module_from_spec(spec)
sys.modules["p4b"] = p4b
spec.loader.exec_module(p4b)

F, SPREAD_FLOOR, MIN_ADM = 3.0, 1e-15, 3
DEPLOYED_TOL = 1e-12

P = p4b.PARAMS
L = P["Lcell"]; lam, mu, rho = P["lam"], P["mu"], P["rho"]
ell = float(np.sqrt(P["ell2"])); l_iso = P["l_iso"]
L11, L22, L12 = p4b.L_plane(l_iso, l_iso, 0.0)
print("frozen params:", P, "| L_plane:", (L11, L22, L12))

kx, ky = 0.31 * np.pi / L, 0.22 * np.pi / L
kbar = np.hypot(kx, ky) * L / np.pi
om_ex = float(np.sqrt(p4b.ombar2_T(kbar, ell / L, l_iso ** 2)) * p4b.omega0(mu, rho, L))
print(f"k=({kx:.12f},{ky:.12f})  omega_exact(M11.3) = {om_ex:.16f}")
print("threads: OMP=%s OPENBLAS=%s MKL=%s" % (os.environ.get("OMP_NUM_THREADS"),
                                              os.environ.get("OPENBLAS_NUM_THREADS"),
                                              os.environ.get("MKL_NUM_THREADS")))

MESHES = [4, 8, 16, 32]
MATS = {n: p4b.assemble_nxn_bloch(n, kx, ky, L, lam, mu, rho, ell ** 2, L11, L22, L12)
        for n in MESHES}

def deployed_omega(n):
    """the shipped acoustic_omegas(): ndof<=128 dense (deterministic), else eigsh tol=1e-12 unpinned"""
    return float(p4b.acoustic_omegas(MATS[n][0], MATS[n][1], 2)[0])

def seeded_omega(n, seed):
    Kh, Mh = MATS[n]
    nd = Kh.shape[0]
    if nd <= 128:
        return float(p4b.acoustic_omegas(Kh, Mh, 2)[0])
    from scipy.sparse.linalg import eigsh
    w, _ = eigsh(Kh, k=4, M=Mh, which="SM", tol=DEPLOYED_TOL, maxiter=10000,
                 v0=np.random.default_rng(seed).standard_normal(nd))
    return float(np.sort(np.real(w))[0] ** 0.5)

def realise(kind, tag):
    out = {}
    for n in MESHES:
        t0 = time.time()
        if kind == "unpinned":
            om = deployed_omega(n)
        else:
            om = seeded_omega(n, tag)
        out[n] = om
        print(f"   [{kind}:{tag}] n={n:2d}  omega_T = {om:.16f}  rel_err = {abs(om-om_ex)/om_ex:.6e}"
              f"  ({time.time()-t0:.1f}s)", flush=True)
    return out

REAL = {}
print("\n--- realization 1 (unpinned, deployed path) ---"); REAL["unpinned_1"] = realise("unpinned", None)
print("\n--- realization 2 (unpinned, deployed path) ---"); REAL["unpinned_2"] = realise("unpinned", None)
print("\n--- realization 3 (unpinned, deployed path) ---"); REAL["unpinned_3"] = realise("unpinned", None)
print("\n--- realization 4 (two-seed protocol, seed 20260924, deployed tol) ---"); REAL["seed_a"] = realise("seed", 20260924)
print("\n--- realization 5 (two-seed protocol, seed 7, deployed tol) ---"); REAL["seed_b"] = realise("seed", 7)

def spread(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return 0.0
    return float((max(vals) - min(vals)) / min(vals))

def verdict_family(name, runs):
    """apply frozen Rule R-fit to a family of realizations"""
    rows = []
    for n in MESHES:
        oms = [r[n] for r in runs]
        s = spread(oms)
        for r in runs:
            e = abs(r[n] - om_ex) / om_ex
            rows.append(dict(mesh=n, omega=oms, s=s, e=e))
    # per-realization verdict
    res = []
    for idx, r in enumerate(runs):
        adm, ratios = [], {}
        for n in MESHES:
            e = abs(r[n] - om_ex) / om_ex
            s = spread([x[n] for x in runs])
            thr = F * max(s, SPREAD_FLOOR)
            ratios[n] = e / thr
            if e > thr:
                adm.append(n)
        slope = None
        if len(adm) >= MIN_ADM:
            hs = [1.0 / n for n in adm]
            es = [abs(r[n] - om_ex) / om_ex for n in adm]
            slope = float(p4b.lsq_loglog_slope(hs, es)[0])
        res.append(dict(realization=idx + 1, admissible=adm, ratios=ratios, slope=slope))
    print(f"\n=== Rule R-fit applied to family '{name}' ({len(runs)} realizations) ===")
    for n in MESHES:
        e = abs(runs[0][n] - om_ex) / om_ex
        s = spread([x[n] for x in runs])
        print(f"   level {n:2d}: e = {e:.6e}  s(measured) = {s:.6e}  threshold F*max(s,1e-15) = "
              f"{F*max(s, SPREAD_FLOOR):.6e}  ratio e/thr = {e/(F*max(s, SPREAD_FLOOR)):.4g}")
    for r in res:
        print(f"   realization {r['realization']}: admissible = {r['admissible']}  slope = "
              f"{None if r['slope'] is None else round(r['slope'], 12)}")
    inv = len({tuple(r["admissible"]) for r in res}) == 1
    slopes = {None if r["slope"] is None else round(r["slope"], 10) for r in res}
    print(f"   -> admissible subset invariant across realizations: {inv}")
    print(f"   -> reported slope set across realizations: {slopes}")
    return dict(realizations=res, invariant=bool(inv), slopes=sorted(str(s) for s in slopes))

summary = {
    "k": [kx, ky], "omega_exact": om_ex, "deployed_tol": DEPLOYED_TOL,
    "rule": {"F": F, "spread_floor": SPREAD_FLOOR, "min_admissible": MIN_ADM},
    "realizations": REAL,
    "unpinned_family": verdict_family("unpinned (deployed path as shipped)",
                                      [REAL["unpinned_1"], REAL["unpinned_2"], REAL["unpinned_3"]]),
    "twoseed_family": verdict_family("two-seed Route-F protocol at deployed tol",
                                     [REAL["seed_a"], REAL["seed_b"]]),
}
Path("/tmp/r1_measurement.json").write_text(json.dumps(summary, indent=1, default=str))
print("\nwritten /tmp/r1_measurement.json")
