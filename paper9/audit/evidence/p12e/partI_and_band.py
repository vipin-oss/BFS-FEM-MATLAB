"""P12E: (1) reproducibility comparison of the two controlled runs;
(2) P3 failure envelope (what err32 would be needed to pass); (3) criterion applied to the
historical governing data and to the 3-mesh subset (design-level information only)."""
import json, math
def load(p): return json.load(open(p))
r1, r2 = load("/home/user/p12e_logs/production_run1.json"), load("/home/user/p12e_logs/production_run2.json")
ji = load("/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.json")

d1 = {k: v for k, v in r1.items() if k != "utc"}; d2 = {k: v for k, v in r2.items() if k != "utc"}
print("== 1. controlled reproducibility (run 1 vs run 2, identical configuration) ==")
print("   JSON identical except 'utc' field :", d1 == d2, f"(utc: {r1['utc']} vs {r2['utc']})")
a, b = r1["5i"], r2["5i"]
for f in ("omega","rel_err","slope","CI95","resid_max","eps_Delta","d16_32","criterion","criterion_pass"):
    print(f"   {f:16s} identical: {a[f] == b[f]}")
print("   omega", [f"{x:.17f}" for x in a["omega"]])
print("   rel_err", [f"{x:.6e}" for x in a["rel_err"]])
print(f"   slope {a['slope']:.15f}  CI95 [{a['CI95'][0]:.12f}, {a['CI95'][1]:.12f}]  resid_max {a['resid_max']:.8f}  eps_Delta {a['eps_Delta']:.6e}")
print(f"   exit codes: run1=1 run2=1 (P3 FAIL both)   TOTAL rows: {r1['PASS']+r1['FAIL']} PASS {r1['PASS']} FAIL {r1['FAIL']}")
print("   solver_config:", json.dumps(r1["solver_config"], indent=None)[:300])

print("\n== 2. P3 failure envelope: four-level fit residual as a function of the 32^2 datum ==")
hs = [1/4, 1/8, 1/16, 1/32]
e = a["rel_err"][:3]
def resid(e32):
    y = [math.log(x) for x in e] + [math.log(e32)]
    x = [math.log(h) for h in hs]
    n = len(x); xm = sum(x)/n; ym = sum(y)/n
    sxx = sum((xi-xm)**2 for xi in x); sl = sum((xi-xm)*(yi-ym) for xi, yi in zip(x, y))/sxx
    ic = ym - sl*xm
    return max(abs(yi-(ic+sl*xi)) for xi, yi in zip(x, y)), sl
print(f"   {'err32':>10s} {'slope':>8s} {'resid':>8s}  P3")
for e32 in (2.48e-15, 4.59e-14, 1.20e-13, 2.06e-13, 5.0e-13, 1.0e-12, 1.5e-12, 2.0e-12, 2.5e-12, 2.9e-12, 4.0e-12, 6.0e-12, 1.0e-11):
    r, sl = resid(e32)
    print(f"   {e32:>10.2e} {sl:>8.3f} {r:>8.3f}  {'PASS' if r <= math.log(1.5) else 'fail'}")
import numpy as np
lo_ok = None
for k in range(200, 20000):
    e32 = k*1e-12/1000
    if resid(e32)[0] <= math.log(1.5):
        lo_ok = e32; break
print(f"   -> P3 needs err32 >= ~{lo_ok:.2e} (4-level fit); every observed realization of the 32^2")
print("      datum, in every solver configuration tested (including both committed runs), lies")
print("      between 2.5e-15 and 2.1e-13 -- i.e. 10x-1000x BELOW the smallest passing value.")
print("      The h^4 trend extrapolated from the 16^2 datum is 2.9e-12 (P12D prediction 2.6e-12).")

print("\n== 3. criterion applied to the historical governing data (four-level, 3-point, subsets) ==")
def fit(oms, idx):
    errs = [abs(oms[i]-ji["5i"]["omega_exact"])/ji["5i"]["omega_exact"] for i in range(4)]
    hh = [hs[i] for i in idx]; ee = [errs[i] for i in idx]
    x = [math.log(h) for h in hh]; y = [math.log(v) for v in ee]; n = len(x)
    xm = sum(x)/n; ym = sum(y)/n; sxx = sum((xi-xm)**2 for xi in x)
    sl = sum((xi-xm)*(yi-ym) for xi, yi in zip(x, y))/sxx; ic = ym-sl*xm
    dof = n-2; se = math.sqrt(sum((yi-(ic+sl*xi))**2 for xi, yi in zip(x, y))/dof/sxx)
    t = {1: 12.706, 2: 4.303, 3: 3.182}.get(dof, 1.96)
    return sl, sl-t*se, sl+t*se, max(abs(yi-(ic+sl*xi)) for xi, yi in zip(x, y)), errs
for tag, oms, idx in (("HISTORICAL governing JSON (committed run 2)", ji["5i"]["omega"], [0,1,2,3]),
                      ("HISTORICAL first three meshes (P12D Route C subset)", ji["5i"]["omega"], [0,1,2]),
                      ("P12E Route-F run (accurate solver)", a["omega"], [0,1,2,3]),
                      ("P12E Route-F run, first three meshes", a["omega"], [0,1,2])):
    sl, lo, hi, rr, errs = fit(oms, idx)
    print(f"   {tag:52s} nfit={len(idx)} slope={sl:7.3f} CI=[{lo:7.3f},{hi:7.3f}] resid={rr:6.3f}"
          f" {'(P2 ok)' if lo>=1 else '(P2 FAIL)'} {'(P3 ok)' if rr<=math.log(1.5) else '(P3 FAIL)'}")
