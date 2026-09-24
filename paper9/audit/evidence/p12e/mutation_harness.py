"""P12E Part H: mutation matrix for the Route-F configuration and the P1-P4 criterion.
Each mutation is applied to an isolated copy of the staged implementation; the discrimination
suite must then FAIL (exit != 0).  Unmutated control must PASS."""
import shutil, subprocess, sys, re
from pathlib import Path
SRC = Path("/home/user/p12e_stage/paper9/verification/suite/p4b_5g_to_5i.py")
DISC = "/home/user/p12e_stage/paper9/verification/suite/p12e_synthetic_discrimination.py"
WORK = Path("/home/user/p12e_stage/paper9/verification/suite")  # same dir: module imports p4a_5a_to_5f.py relative to HERE
orig = SRC.read_text()

MUT = [
 ("M5  tolerance  1e-14 -> 1e-12",            "EIGSOLVER_TOL = 1e-14", "EIGSOLVER_TOL = 1e-12"),
 ("M6  v0 seed    20260924 -> 7",             "V0_SEED = 20260924", "V0_SEED = 7"),
 ("M7  threads pin removed (default 4)",      'os.environ.get("P4B_THREADS", "1")', 'os.environ.get("P4B_THREADS", "4")'),
 ("M8  3-point fit (FIT_MESHES 4,8,16)",      "FIT_MESHES = (4, 8, 16, 32)", "FIT_MESHES = (4, 8, 16)"),
 ("M9  mesh list mutated (4,8,16,64)",        "FIT_MESHES = (4, 8, 16, 32)", "FIT_MESHES = (4, 8, 16, 64)"),
 ("M10 P1 weakened (strict -> non-strict)",   "bool(all(b < a for a, b in zip(rel_err, rel_err[1:])))", "bool(all(b <= a for a, b in zip(rel_err, rel_err[1:])))"),
 ("M10b P1 disabled",                         'bool(all(b < a for a, b in zip(rel_err, rel_err[1:])))', 'True'),
 ("M11 P2 threshold weakened (P_MIN 1.0 -> 0.0)", "P_MIN = 1.0", "P_MIN = 0.0"),
 ("M11b P2 logic tightened (>= 1.5)",         "bool(ci_lo >= P_MIN)", "bool(ci_lo >= 1.5)"),
 ("M12 P3 threshold weakened (ln1.5 -> ln10)", "R_MAX = float(np.log(1.5))", "R_MAX = float(np.log(10.0))"),
 ("M13 P4 threshold weakened (1e-9 -> 1e-5)", "FLOOR_MAX = 1e-9", "FLOOR_MAX = 1e-5"),
 ("M13b P4 logic tightened (< bound)",        "bool(d16_32 <= FLOOR_MAX)", "bool(d16_32 < FLOOR_MAX)"),
]
def run(mod):
    r = subprocess.run([sys.executable, DISC, str(mod)], capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]

ctrl = SRC
rc, last = run(ctrl)
print(f"{'control (unmutated)':46s} exit={rc}  {'DETECTED-as-expected' if rc == 0 else 'PROBLEM'}: {last}")
undetected = []
for name, old, new in MUT:
    assert old in orig, f"mutation anchor missing: {name}"
    mod = WORK / ("_mut_" + re.sub(r'\W+', '_', name) + ".py")
    mod.write_text(orig.replace(old, new, 1))
    rc, last = run(mod)
    ok = rc != 0
    if not ok: undetected.append(name)
    print(f"{name:46s} exit={rc}  {'DETECTED' if ok else '*** UNDETECTED ***'}: {last[:60]}")
print()
print("mutations detected:", f"{len(MUT)-len(undetected)}/{len(MUT)}", "| undetected:", undetected or "none")
print("cleanup:", [f.unlink() for f in WORK.glob("_mut_*.py")] and "done")
sys.exit(0 if not undetected else 1)
