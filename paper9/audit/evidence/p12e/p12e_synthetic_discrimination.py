"""P12E Part D: synthetic discrimination suite for the authorized P1-P4 criterion.
Arguments: [module_path] (default: the staged implementation).  Exit 0 iff all checks hold.
NOTE on predicate independence: P1 is logically *implied* by the others for a decreasing,
power-law-consistent sequence (a sequence can only break monotonicity by departing from the
trend by >= the inter-mesh ratio 16).  P1 is therefore asserted at predicate level, while
P2/P3/P4 are each shown to be able to fail alone."""
import importlib.util, math, sys
MOD = sys.argv[1] if len(sys.argv) > 1 else "/home/user/p12e_stage/paper9/verification/suite/p4b_5g_to_5i.py"
spec = importlib.util.spec_from_file_location("p4b_routeF", MOD)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
HS = [1/4, 1/8, 1/16, 1/32]

def evaluate(errs, d16):
    slope, lo, hi, se = m.lsq_loglog_slope(HS, errs)
    res = m.loglog_max_abs_residual(HS, errs, slope)
    crit = m.check_5i_criterion([4,8,16,32], errs, d16, lo, res)
    return dict(slope=slope, lo=lo, res=res, crit=crit)

ok_all = True
print("== A. required discrimination ==")
CASES = [
 ("convergent 4th order",      [1e-8, 6.25e-10, 3.91e-11, 2.44e-12], 2.4e-12, "PASS"),
 ("convergent 2nd order",      [1e-8, 2.5e-9, 6.25e-10, 1.56e-10],   1.5e-10, "PASS"),
 ("flat plateau",              [1e-3, 1e-3, 1e-3, 1e-3],             1e-13,   "FAIL"),
 ("oscillatory non-monotone",  [1e-8, 9e-8, 1e-9, 5e-9],             4e-9,    "FAIL"),
 ("random noise ~1e-3",        [9.1e-4, 1.02e-3, 9.8e-4, 1.05e-3],  7e-5,    "FAIL"),
 ("anti-convergent (growing)", [1e-8, 2e-8, 4e-8, 8e-8],             4e-8,    "FAIL"),
]
for name, errs, d16, expect in CASES:
    r = evaluate(errs, d16); verdict = "PASS" if all(r["crit"].values()) else "FAIL"
    good = verdict == expect; ok_all &= good
    print(f"  {'ok ' if good else 'BAD'} {name:26s} -> {verdict} (expected {expect})  slope={r['slope']:7.3f} ci_lo={r['lo']:7.3f} resid={r['res']:5.3f} failing={[k for k,v in r['crit'].items() if not v]}")

print("\n== B. predicate-level falsification (mutation targets) ==")
UNIT = [
 ("P1", "P1_monotone_decreasing",      [1e-8, 6.25e-10, 6.30e-10, 2.44e-12], 2.4e-12),
 ("P1b(strict)","P1_monotone_decreasing",[1e-8, 6.25e-10, 6.25e-10, 2.44e-12], 2.4e-12),
 ("P2", "P2_ci_lower_ge_P_MIN",        [1e-3, 9.5e-4, 9.2e-4, 9.0e-4],       1e-10),
 ("P3", "P3_powerlaw_residual_le_R_MAX",[1e-8, 6.25e-10, 1.95e-11, 2.44e-12],2.4e-12),
 ("P4", "P4_floor_datum_le_FLOOR_MAX", [1e-6, 6e-8, 4e-9, 3e-10],            1e-8),
]
for tag, key, errs, d16 in UNIT:
    r = evaluate(errs, d16)
    good = (r["crit"][key] is False)
    ok_all &= good
    others = {k: v for k, v in r["crit"].items() if k != key}
    print(f"  {'ok ' if good else 'BAD'} {tag}: {key} -> {r['crit'][key]} (must be False) | others {others}")

print("\n== C. accepted sequences must keep all predicates True ==")
for name, errs, d16 in (("4th order", [1e-8, 6.25e-10, 3.91e-11, 2.44e-12], 2.4e-12),
                        ("2nd order", [1e-8, 2.5e-9, 6.25e-10, 1.56e-10], 1.5e-10),
                        ("decreasing power law p=1.2", [1e-4, 4.35e-5, 1.9e-5, 8.3e-6], 1e-9),
                        ("marginal p=1.062 law", [1e-4, 4.8e-5, 2.3e-5, 1.1e-5], 1e-9),
                        ("floor exactly at the P4 bound", [1e-8, 6.25e-10, 3.91e-11, 2.44e-12], 1e-9)):
    r = evaluate(errs, d16); good = all(r["crit"].values()); ok_all &= good
    print(f"  {'ok ' if good else 'BAD'} {name}: {r['crit']}")

print("\n== D. pre-declared constants + controlled environment (pinned) ==")
import os
_src = open(MOD).read()
good = 'os.environ.get("P4B_THREADS", "1")' in _src
ok_all &= good
print(f"  {'ok ' if good else 'BAD'} thread pin default in source: os.environ.get(\"P4B_THREADS\", \"1\") present = {good}")
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    good = os.environ.get(v) == m._THREADS
    ok_all &= good
    print(f"  {'ok ' if good else 'BAD'} {v} = {os.environ.get(v)} (pinned to {m._THREADS})")
consts = {"P_MIN": (m.P_MIN, 1.0), "R_MAX": (m.R_MAX, math.log(1.5)), "FLOOR_MAX": (m.FLOOR_MAX, 1e-9),
          "FIT_MESHES": (tuple(m.FIT_MESHES), (4, 8, 16, 32)), "EIGSOLVER_TOL": (m.EIGSOLVER_TOL, 1e-14),
          "V0_SEED": (m.V0_SEED, 20260924)}
for k, (got, want) in consts.items():
    good = (got == want) or (abs(float(got) - float(want)) < 1e-15)
    ok_all &= good
    print(f"  {'ok ' if good else 'BAD'} {k} = {got} (expected {want})")
print("\nALL CHECKS:", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
