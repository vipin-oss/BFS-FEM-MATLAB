"""Part C: does the deployed 5i acceptance logic discriminate convergence quality?
Replicates p4b_5g_to_5i.py lines 424-462 predicate-for-predicate on SYNTHETIC error
sequences (no solver runs, no script modification)."""
import math
om_ex = 1.1648553893289133; hs=[1/4,1/8,1/16,1/32]

def lsq(hs,errs):
    x=[math.log(h) for h in hs]; y=[math.log(e) for e in errs]; n=len(x)
    xm=sum(x)/n; ym=sum(y)/n; sxx=sum((xi-xm)**2 for xi in x)
    sl=sum((xi-xm)*(yi-ym) for xi,yi in zip(x,y))/sxx
    yh=[ym+sl*(xi-xm) for xi in x]; dof=n-2
    se=math.sqrt((sum((yi-hi)**2 for yi,yh_i in zip(y,yh))/dof)/sxx) if False else math.sqrt((sum((yi-hi)**2 for yi,hi in zip(y,yh))/dof)/sxx)
    return sl, sl-{1:12.706,2:4.303,3:3.182,4:2.776}.get(dof,1.96)*se, sl+{1:12.706,2:4.303,3:3.182,4:2.776}.get(dof,1.96)*se

def deployed_acceptance(errs, oms_ratio_seq=None):
    """Mirror of the deployed 5i logic: fit cut e>1e-14; three checks.
    'oms' reconstruction is not needed - d16_32 is defined by the caller."""
    use=[(h,e) for h,e in zip(hs,errs) if e>1e-14]
    slope = lsq([u[0] for u in use],[u[1] for u in use])[0] if len(use)>=3 else float("nan")
    d16_32 = oms_ratio_seq
    eps = max(d16_32, errs[-1])
    c1 = True                                  # "computed omega_T on 4,8,16,32 meshes" -> finite values
    c2 = math.isfinite(slope)                  # slope check (fails only if <3 fit points)
    c3 = math.isfinite(eps)                    # eps check
    c4 = d16_32 <= eps + 1e-30                 # definitional sub-check
    return dict(nfit=len(use), slope=slope, eps=eps, c1=c1, c2=c2, c3=c3, c4=c4,
                PASS=all([c1,c2,c3,c4]))

print(f"{'sequence':38s} {'nfit':>4s} {'slope':>9s} {'checks':>16s}  verdict   classification")
cases = [
 ("true 4th-order (reference)",      [1e-8, 6.25e-10, 3.91e-11, 2.44e-12]),
 ("true 2nd-order",                  [1e-8, 2.5e-9, 6.25e-10, 1.56e-10]),
 ("NO convergence, 1st-order GROWTH",[1e-8, 2e-8, 4e-8, 8e-8]),
 ("flat plateau (zero convergence)", [1e-3, 1e-3, 1e-3, 1e-3]),
 ("oscillating, non-monotone",       [1e-8, 9e-8, 1e-9, 5e-9]),
 ("random noise around 1e-3",        [9.1e-4, 1.02e-3, 9.8e-4, 1.05e-3]),
 ("all errors near floor (<1e-14)",  [1e-8, 1e-15, 1e-16, 1e-17]),
]
for name, errs in cases:
    # d16_32 is solver-noise governed; give each case a plausible value so the definitional check is exercised
    d16 = abs(errs[3]-errs[2]) + 1e-13
    r = deployed_acceptance(errs, d16)
    ok = "PASS" if r["PASS"] else "FAIL"
    cls = "accepted - non-discriminating" if r["PASS"] else "rejected (degenerate fit subset)"
    print(f"{name:38s} {r['nfit']:>4d} {r['slope']:>9.3f} {str((r['c1'],r['c2'],r['c3'],r['c4'])):>16s}  {ok:8s}  {cls}")
print()
print("Independent quantities actually measured by 5i : omega_T(4,8,16,32)  [FE solver]")
print("Independent analytical reference                : omega_ex (M11.3 closed form)")
print("Derived (same data) quantities                  : rel_err, d16_32, eps_Delta, slope, CI95")
print("Quantities used by the acceptance predicate     : finiteness + d16_32 <= max(d16_32, err32)  [all derived]")
print()
print("eps_Delta is data-derived by definition (max of two measured ratios) - not an independently")
print("prescribed tolerance. The plan's candidate wording ('max over IBZ of |w32 - w(extrapolated)|',")
print("'final wording fixed when computed') confirms derivation-by-design.")
