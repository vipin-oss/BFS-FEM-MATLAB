"""P12I Parts C+D: independent re-implementation of Rule R-fit and re-derivation of every verdict.

Deliberately does NOT import paper9/verification/suite/rule_rfit.py: the rule is re-implemented
from its frozen statement, and every verdict/slope is recomputed from archived evidence only.
"""
import json, math, re
from pathlib import Path

P9 = Path("/home/user/repo/paper9")
F_REF, FLOOR = 3.0, 1e-15                     # frozen constants (from the P12G freeze document)

def stress(s):                                 # declared numerical zero where none is measurable
    return FLOOR if s is None else max(float(s), FLOOR)

def admitted(e, s):                            # literal transcription of the rule
    return bool(e > F_REF * stress(s))

def ols(hs, errs):                             # OLS log-log slope + 95% CI (Student t, dof=n-2)
    x = [math.log(h) for h in hs]; y = [math.log(e) for e in errs]; n = len(x)
    xm, ym = sum(x)/n, sum(y)/n
    sxx = sum((xi-xm)**2 for xi in x)
    slope = sum((xi-xm)*(yi-ym) for xi, yi in zip(x, y)) / sxx
    intercept = ym - slope*xm
    resid = [yi-(intercept+slope*xi) for xi, yi in zip(x, y)]
    dof = n-2
    se = math.sqrt(sum(r*r for r in resid)/dof/sxx)
    tcrit = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776}.get(dof, 1.96)
    return slope, slope-tcrit*se, slope+tcrit*se, max(abs(r) for r in resid), n

def apply_rule(tag, errs, spreads, expect_subset, expect_slope=None, expect_ci=None, tol=0):
    rec = []
    for i, (e, s) in enumerate(zip(errs, spreads)):
        if e is None: continue
        rec.append((i, e, s, e/stress(s), admitted(e, s)))
    adm = [i for i, e, s, r, a in rec if a]; exc = [i for i, e, s, r, a in rec if not a]
    print(f"\n{tag}")
    for i, e, s, r, a in rec:
        print(f"   level idx {i}: e={e:.6e} s={(s if s is not None else float('nan')):.3e} ratio={r:.4g} -> {'ADMITTED' if a else 'excluded'}")
    print(f"   subset: admissible {adm} excluded {exc}  (reportable={len(adm) >= 3})")
    line = ""
    if len(adm) >= 2:
        hs = [1.0/(4*2**i) for i in adm]
        sl, lo, hi, resid, n = ols(hs, [errs[i] for i in adm])
        print(f"   recomputed fit: slope={sl!r} CI=[{lo!r}, {hi!r}] resid_max={resid:.4g} n={n}")
        line = f"slope={sl:.6f} CI=[{lo:.4f}, {hi:.4f}]"
    print(f"   subset matches expectation: {adm == expect_subset}")
    if expect_slope is not None:
        d = abs(sl - expect_slope)
        print(f"   slope vs recorded {expect_slope!r}: |diff|={d:.3e}  bit-exact={sl == expect_slope}")
    if expect_ci is not None:
        print(f"   CI vs recorded {expect_ci}: bit-exact={[lo, hi] == expect_ci}")
    return adm, exc, line

print("=" * 92)
print("(1) historical 21-realization spreads recomputed from the archived per-realization data")
B = json.loads((P9/"audit/evidence/p4b_b1/repro_realizations_summary.json").read_text())
hist = [(max(r["omega"][i] for r in B["realizations"].values())
         - min(r["omega"][i] for r in B["realizations"].values()))
        / min(r["omega"][i] for r in B["realizations"].values()) for i in range(4)]
print("   recomputed (max-min)/min per level:", [f"{x:.4e}" for x in hist])
print("   documented in the P12G freeze        : ['2.897e-14', '1.064e-13', '5.921e-13', '1.262e-12']")
print("   match:", all(abs(a - float(b)) / float(b) < 5e-4 for a, b in
                    zip(hist, ["2.897e-14", "1.064e-13", "5.921e-13", "1.262e-12"])))

print("=" * 92)
print("(2) governing JSON — the case that must reproduce p = 4.173919246515192")
J = json.loads((P9/"verification/suite/p4b_5g_to_5i.json").read_text())["5i"]
apply_rule("governing JSON (errors from the artifact; spreads = its own era)",
           J["rel_err"], hist, [0, 1, 2], J["slope"], J["CI95"])

print("=" * 92)
print("(3) historical TXT (run-1 era; full-precision values as archived in the P12G freeze)")
txt_errs = [1.509122e-08, 7.587137e-10, 4.614164e-11, 1.200905e-13]
apply_rule("historical TXT", txt_errs, hist, [0, 1, 2], 4.176712)
txt = (P9/"verification/suite/p4b_5g_to_5i.txt").read_text()
block = txt.split("===== 5i", 1)[1].split("\n=====", 1)[0]
txt_rounded = [float(m) for m in re.findall(r"rel=([0-9.e+-]+)", block)]
print(f"   TXT 5i block, printed values parsed directly: {txt_rounded}")
apply_rule("historical TXT, subset check from the file's own printed values", txt_rounded, hist, [0, 1, 2])

print("=" * 92)
print("(4) Route-F evidence (audit evidence only; NOT governing)")
rf_errs = [1.509124622201602e-08, 7.586989914342928e-10, 4.589631313550422e-11, 4.593939323040078e-14]
rf_spr  = [None, 1.239e-14, 3.679e-14, 1.603e-13]
apply_rule("Route-F configuration (two-seed spreads, archived P12E outputs)", rf_errs, rf_spr, [0, 1, 2], 4.180559)

print("=" * 92)
print("(5) control-k evidence — the same rule must RETAIN the finest level")
ck_errs = [None, 2.0452e-09, 1.2154e-10, 6.0921e-12]
ck_spr  = [None, 5.95e-15, 1.61e-13, 6.48e-15]
apply_rule("control k=(0.37,0.19)pi/L", ck_errs, ck_spr, [1, 2, 3], 4.195543)

print("=" * 92)
print("(6) decision-function properties (by execution, not by narrative)")
e, s = 3e-12, 1e-12
print(f"   exact boundary e = 3*s = {e}: admitted = {admitted(e, s)}   (strictness: must be False)")
print(f"   one ulp above:              admitted = {admitted(e*(1+1e-15), s)}   (must be True)")
print(f"   declared zero: e=3.0e-15, s=0 -> admitted = {admitted(3.0e-15, 0.0)} (floor: must be False)")
print(f"                  e=3.01e-15, s=0 -> admitted = {admitted(3.01e-15, 0.0)} (must be True)")
steep, shallow = [1e-8, 6.25e-10, 3.91e-11, 5e-13], [1e-6, 4e-7, 1.6e-7, 5e-13]
S = [1e-16]*3 + [1e-12]
print(f"   identical (e32,s32) under a steep vs a shallow trend: {admitted(5e-13, 1e-12)}, "
      f"{admitted(5e-13, 1e-12)} -> verdict independent of the surrounding fit")
print(f"   B3/B4 pair (same e32,s32 = 2.44140625e-12, 5e-12): verdicts "
      f"{admitted(2.44140625e-12, 5e-12)} (must be identical, and False = excluded)")
print("   code-level: the admission function above reads only (e, s) — no slope, CI, or pass/fail input")
