"""V2 - classical elastic limit (frozen blueprint Validation V1, Fig. 2a).

Decoupling as defined in the frozen formulation: eta_R = 0 (R1=R2=R6=0,
phason rows decouple and phason field amplitudes are set to zero) and
thermal coupling removed (T0*beta1* -> 0; beta1* -> 0 as well, so the
phonon block is closed). The remaining phonon block is the SAME frozen
matrix entries reduced to (u_x, u_z).

Targets (blueprint §15):
  v_P/v0 = 1 and v_S/v0 = 0.5              (relative error <= 1e-12)
  surface branch -> classical Rayleigh velocity, analytic anchor
  v_R/v_S = 0.9325 for v_S/v_P = 0.5 (Rayleigh secular cubic solved
  in-test; branch tolerance 1e-8 documented).
Coupled free-phason anchors (stage-6 record 0.9348 / 0.934208 at k*=1)
are COMPUTED here from the production solver at low Omega and recorded
for Fig. 2a - the difference is phason surface compliance, quantified,
not fitted.
"""
import os, sys
import numpy as np
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.material import Material
from solver.matrix import pencil
from solver import branch as br

fails = []

# ---------- decoupled material (frozen entries, couplings removed) -------
m_dec = Material(overrides=dict(R1=0.0, R2=0.0, R6=0.0, beta1=0.0, T0b1=0.0))

def phonon_block(k, Omega):
    A0, A1, A2 = pencil(k, Omega, "C", m_dec)
    ix = np.ix_([0, 1], [0, 1])
    return A0[ix], A1[ix], A2[ix]

# ---------- 1. bulk velocities from the same frozen entries -------------
# p = 0: det M2 = (rho Om^2 - C11 k^2)(rho Om^2 - C66 k^2) built from
# A0(2x2) directly (no hand-typed factorisation):
k = 1.0
A0, A1, A2 = phonon_block(k, 0.0)
# det(A0(Omega)) at p=0 with the frozen entries: A0[0,0] = rho Om^2 - C11 k^2
# (rho*=1), off-diagonal zero at p=0, so det = (Om^2 - C11k^2)(Om^2 - C66k^2)
c11k2 = -A0[0, 0].real
c66k2 = -A0[1, 1].real
coeffs = [1.0, -(c11k2 + c66k2), c11k2 * c66k2]
r2 = np.roots(coeffs)
vP = np.sqrt(max(r2)) / k
vS = np.sqrt(min(r2)) / k
print(f"decoupled bulk:  v_P/v0 = {vP:.15f}   v_S/v0 = {vS:.15f}")
if abs(vP / m_dec.meta["vP"] - 1.0) > 1e-12:
    fails.append(f"vP/v0 error {abs(vP/m_dec.meta['vP']-1):.2e} > 1e-12")
if abs(vS / m_dec.meta["vP"] - 0.5) > 1e-12:
    fails.append(f"vS/v0 error {abs(vS/m_dec.meta['vP']-0.5):.2e} > 1e-12")

# ---------- 2. Rayleigh surface branch from the same machinery ----------
def r_rayleigh(k, Omega):
    """sigma_min/||B|| of the 2x2 classical surface system at (k, Omega)."""
    A0, A1, A2 = phonon_block(k, Omega)
    A2i = np.linalg.inv(A2)
    comp = np.zeros((4, 4), dtype=complex)
    comp[:2, 2:] = np.eye(2)
    comp[2:, :] = np.hstack([-A2i @ A0, -A2i @ A1])
    p = np.linalg.eigvals(comp)
    p = p[np.isfinite(p)]
    p = p[p.imag > 1e-12 * np.maximum(np.abs(p), 1e-300)]   # decay into z>0
    if len(p) != 2:
        return np.nan
    B = np.zeros((2, 2), dtype=complex)
    for j, pj in enumerate(sorted(p, key=lambda z: z.imag)):
        # eigenvector of the quadratic pencil for root pj
        Mv = A0 + pj * A1 + pj * pj * A2
        _, _, Vh = np.linalg.svd(Mv)
        a = Vh[-1].conj()                      # null vector, unit norm
        ux, uz = a[0], a[1]
        # EXACT frozen convention of solver/boundary.py (d/dx -> 1j*k,
        # d/dz -> 1j*p; beta1 = R = 0 in the decoupled limit):
        B[0, j] = 1j * (m_dec.C12 * k * ux + m_dec.C11 * pj * uz)  # sigma_zz
        B[1, j] = 1j * (m_dec.C66 * pj * ux + m_dec.C66 * k * uz)  # sigma_xz
    sv = np.linalg.svd(B, compute_uv=False)
    return sv[-1] / sv[0]

Omega0 = 0.5                       # arbitrary scale; k* is the solved variable
xs = np.geomspace(Omega0 / 0.4995, Omega0 / 0.30, 400)   # V in (0.30, 0.4995)
ys = np.array([r_rayleigh(x, Omega0) for x in xs])
fin = np.isfinite(ys)
i0 = int(np.argmin(np.where(fin, ys, np.inf)))
lo = xs[max(i0 - 1, 0)]; hi = xs[min(i0 + 1, len(xs) - 1)]
fb = lambda x: (lambda v: 1e6 if not np.isfinite(v) else v)(r_rayleigh(x, Omega0))
res = minimize_scalar(fb, bounds=(lo, hi), method="bounded",
                      options=dict(xatol=1e-15 * hi))
kR = br._parabolic_polish(float(res.x), lambda x: r_rayleigh(x, Omega0),
                          lo=lo, hi=hi)[0]
VR = Omega0 / kR
ratio_num = VR / 0.5

# analytic Rayleigh anchor: beta^6 - 8 beta^4 + 8(3-2g) beta^2 - 16(1-g) = 0
g = 0.25
c = np.roots([1, 0, -8, 0, 8 * (3 - 2 * g), 0, -16 * (1 - g)])
beta = sorted(x.real for x in c if abs(x.imag) < 1e-9 and 0 < x.real < 1)
ratio_ana = beta[0]
print(f"decoupled surface: V_R/v_S numerical = {ratio_num:.12f}   "
      f"analytic = {ratio_ana:.12f}   (stage-6 record 0.9348 / 0.934208)")
if abs(ratio_num / ratio_ana - 1.0) > 1e-8:
    fails.append(f"Rayleigh anchor error {abs(ratio_num/ratio_ana-1):.2e} > 1e-8")

# ---------- 3. coupled low-Omega anchors (recorded, not gated) ----------
bc = dict(phason="free", thermal="isothermal")
rows = []
for model in ("A", "B", "C"):
    for Om in (1e-5, 1e-4, 1e-3):
        out = br.solve_k_at_Omega(Om, model, Material(), bc)
        rows.append((model, Om, out["V"], out["V"] / 0.5, out["r"], out["status"]))
        print(f"coupled {model} Om={Om:g}: V*={out['V']:.12f}  "
              f"V*/v_S={out['V']/0.5:.8f}  r={out['r']:.3e}  [{out['status']}]")

# ---------- write Fig. 2a raw data ----------
outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "results")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "v2_elastic_limit.csv"), "w") as f:
    f.write("# V2 elastic limit raw data (see test header)\n")
    f.write(f"vP_over_v0,{vP:.16e}\nvS_over_v0,{vS:.16e}\n")
    f.write(f"VR_over_vS_numerical,{ratio_num:.16e}\n")
    f.write(f"VR_over_vS_analytic,{ratio_ana:.16e}\n")
    f.write("model,Omega,Vstar,Vstar_over_vS,r,status\n")
    for row in rows:
        f.write(f"{row[0]},{row[1]:.6e},{row[2]:.16e},{row[3]:.16e},"
                f"{row[4]:.6e},{row[5]}\n")

if fails:
    print("\nV2 elastic limit: FAIL -- STOP")
    for x in fails:
        print("   " + x)
    sys.exit(1)
print("\nV2 elastic limit: PASS")
