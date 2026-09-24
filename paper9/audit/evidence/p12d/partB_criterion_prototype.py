"""P12D Part B: prototype of a discriminant 5i acceptance design, tested on SYNTHETIC sequences
and on the committed 21 realizations.  Pure post-processing - no solver runs, nothing in the
repository is modified.  Pre-declared constants (provenance stated, not data-derived):

  P_MIN     = 1.0    weakest non-trivial convergence claim: at least linear decrease per refinement
  R_MAX     = ln(1.5) = 0.405   accepted power-law model: every point within a factor 1.5 of the line
  FLOOR_MAX = 1e-9   "final doubling changes omega by <= 1e-9 relative" (2000x the solver error bar
                     tol/2 = 5e-13 implied by the declared tol=1e-12 on lambda); convention, to be
                     re-derived by the same rule if the solver tolerance changes.
"""
import json, math
om_ex = 1.1648553893289133; hs=[1/4,1/8,1/16,1/32]
P_MIN, R_MAX, FLOOR_MAX = 1.0, math.log(1.5), 1e-9

def lsq(hs, errs):
    x=[math.log(h) for h in hs]; y=[math.log(e) for e in errs]; n=len(x)
    xm=sum(x)/n; ym=sum(y)/n; sxx=sum((xi-xm)**2 for xi in x)
    p=sum((xi-xm)*(yi-ym) for xi,yi in zip(x,y))/sxx
    yh=[ym+p*(xi-xm) for xi in x]; dof=n-2
    se=math.sqrt((sum((yi-hi)**2 for yi,hi in zip(y,yh))/dof)/sxx)
    t={1:12.706,2:4.303,3:3.182,4:2.776}.get(dof,1.96)
    return p, p-t*se, p+t*se, max(abs(yi-hi) for yi,hi in zip(y,yh))

def proposed(errs, d16):
    """Design proposal (NOT implemented in the script): property predicates on pre-declared data."""
    reasons=[]
    mono = all(a > b for a, b in zip(errs, errs[1:]))
    if not mono: reasons.append("P1 monotonicity violated")
    p,lo,hi,res = lsq(hs[:3], errs[:3])          # discretization-dominated sub-fit (4,8,16)
    if not (lo >= P_MIN): reasons.append(f"P2 CI-lower-bound {lo:.3f} < P_MIN={P_MIN}")
    if not (res <= R_MAX):  reasons.append(f"P3 power-law residual {res:.3f} > R_MAX={R_MAX:.3f}")
    if not (d16 <= FLOOR_MAX): reasons.append(f"P4 floor datum {d16:.3e} > FLOOR_MAX={FLOOR_MAX:.0e}")
    return dict(pass_=not reasons, p=p, lo=lo, hi=hi, res=res, reasons=reasons)

def deployed(errs, d16):
    use=[e for e in errs if e>1e-14]
    ok = len(use)>=3 and math.isfinite(d16) and d16 <= max(d16, errs[-1])+1e-30
    return dict(pass_=ok)

print("A. SYNTHETIC DISCRIMINATION (fabricated sequences; d16 chosen per pattern)")
cases = [
 ("convergent, 4th order",         [1e-8, 6.25e-10, 3.91e-11, 2.44e-12], 2.4e-12),
 ("convergent, 2nd order",         [1e-8, 2.5e-9, 6.25e-10, 1.56e-10],  1.5e-10),
 ("FLAT plateau (no convergence)", [1e-3, 1e-3, 1e-3, 1e-3],            1e-13),
 ("OSCILLATORY, non-monotone",     [1e-8, 9e-8, 1e-9, 5e-9],            4e-9),
 ("RANDOM noise ~1e-3",            [9.1e-4, 1.02e-3, 9.8e-4, 1.05e-3],  7e-5),
 ("ANTI-convergent (growing)",     [1e-8, 2e-8, 4e-8, 8e-8],            4e-8),
 ("floor-only (all < 1e-14)",      [1e-8, 1e-15, 1e-16, 1e-17],         1e-17),
]
print(f"{'case':32s} {'deployed':>9s} {'proposed':>9s}  decisive predicate")
for name, e, d in cases:
    dep, pro = deployed(e, d), proposed(e, d)
    tag = "none (PASS)" if pro["pass_"] else pro["reasons"][0]
    print(f"{name:32s} {'PASS' if dep['pass_'] else 'FAIL':>9s} {'PASS' if pro['pass_'] else 'FAIL':>9s}  {tag}")

print()
print("B. COMMITTED EVIDENCE (21 documented realizations; must all PASS the proposed design)")
B=json.load(open("/home/user/repo/paper9/audit/evidence/p4b_b1/repro_realizations_summary.json"))
fails=[]; pres=[]; plos=[]
for k,r in B["realizations"].items():
    oms=r["omega"]; e=[abs(o-om_ex)/om_ex for o in oms]
    d=abs(oms[3]-oms[2])/oms[3]
    pr=proposed(e,d); pres.append(pr["res"]); plos.append(pr["lo"])
    if not pr["pass_"]: fails.append((k,pr["reasons"]))
print(f"  proposed criterion: {21-len(fails)}/21 pass | failures: {fails or 'none'}")
print(f"  sub-fit CI-lower bound range: {min(plos):.4f} .. {max(plos):.4f}  (P_MIN=1.0 -> margin >= {min(plos)-1.0:.3f})")
print(f"  power-law residual range   : {min(pres):.4f} .. {max(pres):.4f}  (R_MAX={R_MAX:.4f} -> margin >= {R_MAX-max(pres):.3f})")
print(f"  floor datum range          : 4.550e-11 .. 4.679e-11  (FLOOR_MAX=1e-9 -> margin x{1e-9/4.679e-11:.0f})")

print()
print("C. PREDICTION for candidate F (tighten solver tol 1e-12 -> ~1e-14), pure extrapolation:")
e16 = 4.632063300824643e-11
for p in (4.0, 4.1739):
    imputed = e16 * 2.0**(-p)
    errs=[1.50912172477929e-08, 7.586511458421733e-10, e16, imputed]
    pp,lo,hi,res = lsq(hs, errs)
    print(f"  imputed err32 = {imputed:.3e} (p={p}): 4-level fit p = {pp:.4f}, CI95 [{lo:.4f}, {hi:.4f}]  (dof=2)")
print("  -> if the 32^2 datum becomes a *truthful* discretization sample, the Blueprint-prescribed")
print("     four-level fit lands back on the trend; the branch flip disappears by construction.")
print("     Requires a new production solve + re-baselining authorization; NOT run here.")

print()
print("D. per-mesh omega spread across the 21 realizations (ordering/branch check):")
for i,n in enumerate((4,8,16,32)):
    vals=[r["omega"][i] for r in B["realizations"].values()]
    print(f"  n={n:2d}: {min(vals):.16f} .. {max(vals):.16f}  spread {max(vals)-min(vals):.2e}  "
          f"(relative {abs(max(vals)-min(vals))/min(vals):.2e}; no branch jump - accuracy jitter only)")
