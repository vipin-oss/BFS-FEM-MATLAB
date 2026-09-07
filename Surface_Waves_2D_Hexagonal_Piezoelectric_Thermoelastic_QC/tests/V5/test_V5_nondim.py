"""V5 - nondimensionalisation arithmetic (blueprint Validation plan).

Every starred quantity must follow from the dimensional set in
params.json via the frozen scales, and the frozen target table must be
reproduced; frequency/wavelength maps round-trip. c_e* = 1 exactly (F1:
dimensional c_e absorbed into the thermal-row normalisation - never the
dimensional 500 J/(kg K)).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.material import Material, load_params, check_frozen

fails = []
par = load_params()
d = par["dimensional_SI"]
m = Material()

# 1. frozen table check (built-in, rtol 1e-4)
bad = check_frozen(par, m._base, m.meta, rtol=1e-4)
if bad:
    fails.append(f"check_frozen mismatches: {bad}")

# 2. exact scale identities (tight, analytic)
k0 = par["scales"]["k0"]
v0 = math.sqrt(d["C11"] / d["rho"])
if abs(v0 - 6917.1446) / 6917.1446 > 1e-6:
    fails.append(f"v0 = {v0!r} vs 6917.1446")
om0 = v0 * k0
if abs(om0 - 4.34617e10) / 4.34617e10 > 1e-4:
    fails.append(f"omega0 = {om0!r} vs 4.34617e10")
if abs(k0 - 2 * math.pi * 1e6) > 1e-9:
    fails.append("k0 != 2*pi*1e6")

# 3. F1: c_e* exactly 1 (never 500)
if m.c_e != 1.0:
    fails.append(f"c_e* = {m.c_e!r} != 1.0 exactly")

# 4. frequency map round-trips (Omega -> f = Omega*omega0/(2*pi))
def f_of(Om):
    return Om * om0 / (2 * math.pi)
if abs(f_of(1e-3) - 6.9e6) / 6.9e6 > 5e-3:
    fails.append(f"Omega=1e-3 -> f = {f_of(1e-3):.6g} Hz (expect ~6.9 MHz)")
if abs(f_of(1e3) - 6.9e12) / 6.9e12 > 5e-3:
    fails.append(f"Omega=1e3 -> f = {f_of(1e3):.6g} Hz (expect ~6.9 THz)")

# 5. crossover and telegraph scales
if abs(m.meta["Omega_c"] - 11467.5) / 11467.5 > 1e-4:
    fails.append(f"Omega_c = {m.meta['Omega_c']!r} vs 11467.5")
if abs(m.meta["tau_tel"] - 2 * m.rho_w / m.Dw) > 1e-15:
    fails.append("tau_telegraph identity")

# 6. wavelength map sanity: lambda = 2*pi/(k* * k0); at Omega=1 on model C's
# branch (k* ~ 2.14456 from the V3 sweep) lambda ~ 0.4663 mm-scale
lam = 2 * math.pi / (2.1445598 * k0)
if abs(lam - 0.46630e-6) / 0.46630e-6 > 1e-3:
    fails.append(f"lambda(Omega=1, C) = {lam:.6g} m (expect ~0.4663 um)")

# 7. starred set self-consistency: derive_starred reproduces m exactly
from solver.material import derive_starred
s2, meta2 = derive_starred(par)
for key, val in s2.items():
    if getattr(m, key) != val:
        fails.append(f"derive_starred mismatch at {key}")

if fails:
    print("V5 nondimensional arithmetic: FAIL -- STOP")
    for x in fails:
        print("   " + x)
    sys.exit(1)
print(f"v0={v0:.4f} m/s  omega0={om0:.5e} rad/s  Omega_c={m.meta['Omega_c']:.1f}"
      f"  f(1e-3)={f_of(1e-3):.4g} Hz  f(1e3)={f_of(1e3):.4g} Hz")
print("V5 nondimensional arithmetic: PASS")
