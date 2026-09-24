"""P12F Part A/G: independent re-verification of the P12E findings from archived evidence.
No solver runs.  Everything recomputed from the evidence JSONs + committed artifacts."""
import json, math, hashlib, subprocess
from pathlib import Path
R = Path("/home/user/repo/paper9")
r1 = json.loads((R/"audit/evidence/p12e/production_run1.json").read_text())
r2 = json.loads((R/"audit/evidence/p12e/production_run2.json").read_text())
J  = json.loads((R/"verification/suite/p4b_5g_to_5i.json").read_text())

def ols(hs, errs):
    x=[math.log(h) for h in hs]; y=[math.log(e) for e in errs]; n=len(x)
    xm=sum(x)/n; ym=sum(y)/n; sxx=sum((xi-xm)**2 for xi in x)
    sl=sum((xi-xm)*(yi-ym) for xi,yi in zip(x,y))/sxx; ic=ym-sl*xm
    resid=[yi-(ic+sl*xi) for xi,yi in zip(x,y)]
    dof=n-2; se=math.sqrt(sum(r*r for r in resid)/dof/sxx)
    t={1:12.706,2:4.303,3:3.182,4:2.776}.get(dof,1.96)
    return dict(slope=sl, lo=sl-t*se, hi=sl+t*se, se=se, resid_max=max(abs(r) for r in resid), ic=ic, dof=dof)

print("="*80); print("A1. controlled-run errors recomputed from omega (not read from any summary)"); print("="*80)
d = r1["5i"]; oms = d["omega"]; om_ex = d["omega_exact"]
errs_calc = [abs(o-om_ex)/om_ex for o in oms]
claim = [1.509125e-08, 7.586990e-10, 4.589631e-11, 4.593939e-14]
for n,o,e,c in zip(d["meshes"], oms, errs_calc, claim):
    print(f"  {n:2d}x{n:<2d} omega={o!r}  err_recomputed={e:.15e}  P12E-claim={c:.6e}  rel_diff={abs(e-c)/c:.1e}")
print(f"  JSON rel_err == recomputation : {all(a==b for a,b in zip(d['rel_err'], errs_calc))}")

print(); print("="*80); print("A2/A3. four-level fit, CI, residual, P1-P4 recomputed"); print("="*80)
hs=[1/n for n in d["meshes"]]; f4 = ols(hs, errs_calc)
print(f"  slope  recomputed {f4['slope']!r}")
print(f"         P12E claim 5.902372359347142   identical={f4['slope']==d['slope']}")
print(f"  CI95   recomputed [{f4['lo']:.12f}, {f4['hi']:.12f}]   JSON [{d['CI95'][0]:.12f}, {d['CI95'][1]:.12f}]")
print(f"  resid  recomputed {f4['resid_max']!r}   JSON {d['resid_max']!r}   |diff|={abs(f4['resid_max']-d['resid_max']):.2e} (float ordering)")
P_MIN, R_MAX, FLOOR_MAX = 1.0, math.log(1.5), 1e-9
d16 = abs(oms[3]-oms[2])/oms[3]
crit = dict(P1=all(b<a for a,b in zip(errs_calc,errs_calc[1:])), P2=f4["lo"]>=P_MIN, P3=f4["resid_max"]<=R_MAX, P4=d16<=FLOOR_MAX)
print(f"  P1/P2/P3/P4 recomputed = {crit}")
print(f"  JSON criterion         = {{k: d['criterion'][k] for k in d['criterion']}}".replace("{k: d['criterion'][k] for k in d['criterion']}", str({k: d['criterion'][k] for k in ('P1_monotone_decreasing','P2_ci_lower_ge_P_MIN','P3_powerlaw_residual_le_R_MAX','P4_floor_datum_le_FLOOR_MAX')})))
print(f"  criterion_pass={d['criterion_pass']}  eps_Delta={d['eps_Delta']:.6e}  d16_32 recomputed={d16:.6e}")
print(f"  R_MAX={R_MAX!r}  P3 margin (resid - R_MAX) = {f4['resid_max']-R_MAX:.4f}")

print(); print("="*80); print("A4. reproducibility: run1 vs run2"); print("="*80)
a = {k:v for k,v in r1.items() if k!="utc"}; b = {k:v for k,v in r2.items() if k!="utc"}
print(f"  JSON equal except utc      : {a==b}")
print(f"  utc                        : {r1['utc']} | {r2['utc']}")
for f in ("omega","rel_err","slope","CI95","resid_max","eps_Delta","d16_32","criterion","criterion_pass"):
    print(f"    {f:16s} bit-identical: {r1['5i'][f]==r2['5i'][f]}")
print(f"  solver_config identical    : {r1['solver_config']==r2['solver_config']}  -> {json.dumps(r1['solver_config'])[:150]}...")

print(); print("="*80); print("A5. hidden-subset check"); print("="*80)
for tag, idx in {"4,8,16,32 (all)":[0,1,2,3], "4,8,16":[0,1,2], "8,16,32":[1,2,3], "4,8,32":[0,1,3]}.items():
    r = ols([hs[i] for i in idx], [errs_calc[i] for i in idx])
    print(f"  fit {tag:14s}: slope={r['slope']:10.6f} resid={r['resid_max']:7.4f}  == reported: {r['slope']==d['slope']}")
print("  reported == all-four slope  :", d["slope"]==f4["slope"])
print("  patch diff removes the legacy subset filter:", "if e > 1e-14:" in (R/'audit/evidence/p12e/routeF_patch.diff').read_text())
print("  staged script residual filters:", subprocess.run(["grep","-c","if e > 1e-14\\|use.append\\|10\\*min_err","/home/user/p12e_stage/paper9/verification/suite/p4b_5g_to_5i.py"],capture_output=True,text=True).stdout.strip())

print(); print("="*80); print("A6/G. 32^2 datum vs the 4^2->16^2 trend — three solver generations"); print("="*80)
cases = [("Route-F controlled run (tol 1e-14, v0, threads=1)", oms),
         ("historical governing JSON (run 2, tol 1e-12, unseeded)", J["5i"]["omega"]),
         ("historical TXT (run 1, same era)", [1.164855406907999,1.164855390212705,1.1648553893826616,1.1648553893287734])]
summary = {}
for tag, o in cases:
    ex = J["5i"]["omega_exact"]; e = [abs(x-ex)/ex for x in o]
    t3 = ols(hs[:3], e[:3]); f4c = ols(hs, e)
    pred32 = math.exp(t3["ic"] + t3["slope"]*math.log(1/32))
    ratio = e[3]/pred32
    summary[tag] = dict(errs=e, t3=t3, f4=f4c, pred32=pred32, ratio=ratio)
    print(f"  {tag}")
    print(f"    errs              : {[f'{x:.5e}' for x in e]}")
    print(f"    3-pt (4,8,16) rate: {t3['slope']:.6f}  CI [{t3['lo']:.4f}, {t3['hi']:.4f}]  resid {t3['resid_max']:.4f}")
    print(f"    4-pt rate         : {f4c['slope']:.6f}  CI [{f4c['lo']:.4f}, {f4c['hi']:.4f}]  resid {f4c['resid_max']:.4f}")
    print(f"    trend-pred err32  : {pred32:.4e} | observed {e[3]:.4e} | obs/pred = {ratio:.4e}  ({pred32/e[3]:.0f}x below trend)")
print(); print("="*80); print("G. pairwise observed rates (Route-F run and historical JSON)"); print("="*80)
for tag, o in (("Route-F", oms), ("historical JSON", J["5i"]["omega"])):
    ex = J["5i"]["omega_exact"]; e = [abs(x-ex)/ex for x in o]
    pr = [math.log(e[i]/e[i+1])/math.log(2) for i in range(3)]
    print(f"  {tag:16s}: 4->8 = {pr[0]:.3f} | 8->16 = {pr[1]:.3f} | 16->32 = {pr[2]:.3f}")
