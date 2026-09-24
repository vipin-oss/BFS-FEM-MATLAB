"""P12H Parts K/N: numerical cross-check, float/manuscript consistency, Blueprint checks, Route-F absence."""
import difflib, hashlib, json, math, re, sys
from pathlib import Path

REPO = Path("/home/user/repo"); P9 = REPO / "paper9"
sys.path.insert(0, str(P9 / "verification/suite"))
import rule_rfit as R

def sha(p): return hashlib.sha256((REPO / p).read_bytes()).hexdigest()
ok = []; bad = []
def check(name, cond, detail=""):
    (ok if cond else bad).append(name)
    print(f"  [{'ok ' if cond else 'FAIL'}] {name}{(' -- ' + detail) if detail else ''}")

print("=== 1. governing numerical artifact re-derivation (Rule R-fit from the artifact's own errors) ===")
J = json.loads((P9 / "verification/suite/p4b_5g_to_5i.json").read_text())["5i"]
ev = json.loads((P9 / "audit/evidence/p12h/rule_rfit_governing.json").read_text())
fit = R.fit_admissible(ev["expected_decisions"]["governing_era"]["evidence_errors"],
                       ev["reproducibility_inputs"]["governing_era"]["spreads"])
print(f"  rule fit: subset {fit['admissible']}, excluded {fit['excluded']}, slope {fit['fit']['slope']!r}")
print(f"  artifact: slope {J['slope']!r}, CI {J['CI95']}, eps_Delta {J['eps_Delta']!r}")
check("rule reproduces the governing slope bit-exactly", fit["fit"]["slope"] == J["slope"])
check("rule reproduces the governing CI bit-exactly",
      [fit["fit"]["lo"], fit["fit"]["hi"]] == list(J["CI95"]))
check("excluded level is 32^2 only", fit["excluded"] == [32] and fit["admissible"] == [4, 8, 16])
check("epsilon_Delta unchanged",
      abs(J["eps_Delta"] - 4.6318154949690315e-11) < 1e-26, f"{J['eps_Delta']!r}")

print("=== 2. Table 6 output vs JSON + rule record ===")
t6 = (P9 / "tables/out/tab06_convergence_floor.tex").read_text()
for m, e, s in zip((4, 8, 16, 32), J["rel_err"], ev["reproducibility_inputs"]["governing_era"]["spreads"]):
    check(f"tab06 reports e_{m} = {e:.2e}", f"{e:.2e}".replace("e-0", "e-") in t6 or f"{e:.2e}" in t6)
    check(f"tab06 reports s_{m} = {s:.2e}", f"{s:.2e}" in t6)
check("tab06 marks only 32^2 out of the fit", "no (ratio 0.00196)" in t6 and t6.count("& yes \\\\") == 3)
check("tab06 keeps '4.17' and 'no theoretical order claimed'", "4.17" in t6 and "no theoretical order claimed" in t6)
check("tab06 reports eps_Delta as mesh-change floor", "Operational resolution floor (mesh change)" in t6)
check("tab06 CI unchanged", "[3.15, 5.20]" in t6)

print("=== 3. Figure 5 generator + float consistency ===")
fg = (P9 / "figures/gen/fig05_mesh_convergence.py").read_text()
check("fig05 generator reads the Rule R-fit record", "rule_rfit_governing.json" in fg)
check("fig05 distinguishes in-fit and excluded levels",
      "in rate fit" in fg and "Resolution-limited" in fg and "Empirical fit" in fg)
check("fig05 output exists and is newer than both generators",
      (P9 / "figures/out/fig05_mesh_convergence.pdf").stat().st_mtime
      > max((P9 / "figures/gen/fig05_mesh_convergence.py").stat().st_mtime,
            (P9 / "tables/gen/tab06_convergence_floor.py").stat().st_mtime) - 1)
check("tab06 output newer than its generator",
      (P9 / "tables/out/tab06_convergence_floor.tex").stat().st_mtime
      >= (P9 / "tables/gen/tab06_convergence_floor.py").stat().st_mtime)

print("=== 4. manuscript wording and numbers ===")
sec05 = (P9 / "latex/sections/sec05_verification.tex").read_text()
sec09 = (P9 / "latex/sections/sec09_conclusions.tex").read_text()
ms    = (P9 / "latex/ms.tex").read_text()
check("sec05 states all four levels are reported, 32^2 resolution-limited",
      "all four levels" in sec05.lower() or "4^2$" in sec05)
check("sec05 states the rule and the excluded level",
      "Rule~R-fit" in sec05 and "resolution-limited" in sec05)
check("sec05 keeps p = 4.17 and its CI", "4.17" in sec05 and "[3.15, 5.20]" in sec05)
check("sec05 keeps eps_Delta", "4.63 \\times 10^{-11}" in sec05)
check("sec09 says observed rate over admissible levels, not 'confirmed four-level'",
      "admissible under the pre-declared measurement-resolution rule" in sec09)
check("abstract keeps p = 4.17 and CI", "p = 4.17" in ms and "[3.15, 5.20]" in ms)
for name, txt in (("sec05", sec05), ("sec09", sec09), ("ms.tex", ms)):
    check(f"{name}: no theoretical order claimed / no four-level fit claim",
          "theoretical order" in txt or "observed" in txt)
check("no Route-F numerical value in any governed artifact",
      all("4.180559" not in (P9 / p).read_text() for p in
          ["plan/CALC_MASTER_PLAN.md", "plan/blueprint/Paper9_Blueprint_v1.4.tex",
           "latex/ms.tex", "latex/sections/sec05_verification.tex", "latex/sections/sec09_conclusions.tex",
           "tables/out/tab06_convergence_floor.tex", "figures/gen/fig05_mesh_convergence.py"]))

print("=== 5. Blueprint v1.3 preservation and v1.4 derivation ===")
b13, b14 = P9 / "plan/blueprint/Paper9_Blueprint_v1.3.tex", P9 / "plan/blueprint/Paper9_Blueprint_v1.4.tex"
check("v1.3 sha256 = ca71b91a...", sha("paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex").startswith("ca71b91a"))
d13 = b13.read_text().splitlines(keepends=True); d14 = b14.read_text().splitlines(keepends=True)
hunks = [h for h in difflib.SequenceMatcher(None, d13, d14).get_opcodes() if h[0] != "equal"]
print(f"  v1.3 -> v1.4 changed blocks: {len(hunks)}")
for tag, i1, i2, j1, j2 in hunks:
    print(f"    {tag}: v1.3 lines {i1+1}-{i2} -> v1.4 lines {j1+1}-{j2}")
check("exactly 4 changed blocks (version row, 5.7, matrix row 5, PCR5 item)", len(hunks) == 4)
t14 = b14.read_text()
check("v1.4 carries explicit v1.3 provenance (sha256)", "ca71b91aba4ca4ab" in t14)
check("v1.4 states the frozen rule (F = 3 strict, floor 1e-15, >=3 levels)",
      "pre-declared factor" in t14 and "$F = 3$" in t14 and "fewer than three levels" in t14)
check("v1.4 forbids subset choice from slope/CI (rule text is measurement-only)",
      "reproducibility of that level's eigenvalue" in t14            # P12H wording
      or ("measured reproducibility" in t14 and "reproducibility $s_i$ being measured" in t14))  # P12J wording (C1)
check("v1.4 removed the fixed four-level fit claim", "fitted by least squares from the four refinement levels" not in t14)
check("v1.4 keeps the resolution-floor and weak-anisotropy sentence",
      "smallest gap width distinguishable from noise" in t14 and "weak anisotropy effects to be claimed as real" in t14)
check("v1.4 brace balance unchanged", t14.count("{") == t14.count("}"))

print("=== 6. plan amendment checks ===")
pl = (P9 / "plan/CALC_MASTER_PLAN.md").read_text()
row = next(l for l in pl.splitlines() if l.startswith("| 5i |"))
check("row 5i carries Rule R-fit, F = 3, s_i, <3 admissible rule",
      "Rule R-fit" in row and "F = 3" in row and "≤ ε_Δ" not in row)
check("row 5i keeps observed rate / no theoretical order",
      "no theoretical order claimed" in row and "95 % CI" in row)
check("plan distinguishes the five quantities", "measurement resolution `s_i`" in pl
      and "observed convergence rate" in pl and "reported ε_Δ" in pl)
check("plan PCR5 wording updated", "**PCR5** now reads" in pl)
check("plan provenance recorded", "A1 adoption of frozen Rule R-fit" in pl)

print()
print(f"CHECKS PASSED: {len(ok)} | FAILED: {len(bad)}")
if bad:
    print("FAILED CHECKS:", bad)
sys.exit(1 if bad else 0)
