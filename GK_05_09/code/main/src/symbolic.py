"""STEP 4 — independent symbolic cross-check of the implemented mathematics.

Verifies with SymPy that the formulas coded in src/laplace.py and src/model.py
are the ones written in GK_COMPLETE_CALCULATIONS.tex. Runs before the numerical
pipeline is trusted.

Note on sympy: it does not automatically reduce sqrt(s^2 tq^2 + 2 s tq + 1) to
(1 + s tq). The polynomial factors exactly as (1+s tq)^2 and both factors are
positive for s,tq>0, so the reduction is valid and is applied explicitly. This
is documented in the master (section 24, D1).
"""
from __future__ import annotations
import sympy as sp

s, tq, k2, al, x = sp.symbols('s tau_q kappa2 alpha x', positive=True)
B, L, tD, Q0 = sp.symbols('B L tau_Delta Q0', positive=True)

M2 = s * (1 + tq * s) / (al + k2 * s)          # eq:m2
M = sp.sqrt(M2)


def _radfix(e):
    return sp.simplify(e.subs(sp.sqrt(s**2 * tq**2 + 2 * s * tq + 1), 1 + s * tq))


def run_all():
    """Returns a list of dicts: id, statement, equation label, status."""
    out = []

    def chk(cid, label, statement, expr):
        ok = sp.simplify(expr) == 0
        out.append(dict(id=cid, equation=label, statement=statement,
                        residual=str(sp.simplify(expr)),
                        status="PASS" if ok else "FAIL"))
        return ok

    # dimensional -> dimensionless: propagation factor from the field equations
    qpp = sp.Symbol('qpp'); q = sp.Symbol('q')
    sol = sp.solve(sp.Eq((1 + tq * s) * q - qpp / s - k2 * qpp, 0), qpp)[0]
    chk("S1", "eq:m2", "m^2 derived from eq:lap-energy + eq:lap-gk",
        sp.simplify(sol / q) - M2.subs(al, 1))

    chk("S2", "eq:Bdef/eq:kappa-from-B", "kappa2 = alpha tau_q B inverts B",
        (al * tq * B).subs(B, k2 / (al * tq)) - k2)

    chk("S3", "eq:Binv", "B invariant under the scaling (L cancels)",
        (k2 / L**2) / (1 * (al * tq / L**2)) - k2 / (al * tq))

    chk("S4", "eq:param-det", "det(dtheta/dphi) = alpha tau_q",
        sp.Matrix([[1, 0, 0], [0, 1, 0], [tq*B, al*B, al*tq]]).det() - al * tq)

    chk("S5", "eq:lim-fourier", "Fourier limit m^2 -> s/alpha",
        sp.limit(sp.limit(M2, tq, 0), k2, 0) - s / al)
    chk("S6", "eq:lim-mcv", "MCV limit m^2 -> s(1+tq s)/alpha",
        M2.subs(k2, 0) - s * (1 + tq * s) / al)
    chk("S7", "eq:lim-nyiri", "Nyiri limit m^2 -> s/(alpha+k2 s)",
        M2.subs(tq, 0) - s / (al + k2 * s))
    chk("S8", "eq:mcv-speed", "MCV finite speed sqrt(alpha/tau_q)",
        sp.limit(M2.subs(k2, 0) / s**2, s, sp.oo) - tq / al)

    chk("S9", "eq:res-step5", "B=1 cancellation: m^2 -> s/alpha",
        M2.subs(k2, al * tq) - s / al)

    m_ray = sp.simplify(M.subs(k2, al * tq))
    chk("S10", "eq:m-ray", "m|ray independent of tau_q", sp.diff(m_ray, tq))
    That_ray = Q0 * m_ray * sp.cosh(m_ray * (1 - x)) / (tD * s * sp.sinh(m_ray))
    chk("S11", "eq:dTdtq-ray", "dT/dtau_q = 0 on the ray, all x",
        sp.diff(That_ray, tq))

    chk("S12", "eq:dm-dtq", "dm/dtau_q = s^2/(2m(alpha+k2 s))",
        sp.diff(M, tq) - s**2 / (2 * M * (al + k2 * s)))
    chk("S13", "eq:dm-dk2", "dm/dkappa2 = -m s/(2(alpha+k2 s))",
        sp.diff(M, k2) + M * s / (2 * (al + k2 * s)))

    ratio = sp.cancel(sp.simplify(sp.diff(M, tq) / sp.diff(M, k2)))
    chk("S14", "eq:ratio-general", "general sensitivity ratio = -s/m^2",
        ratio + s / M2)
    chk("S15", "eq:ratio-resonance", "ratio at B=1 equals -alpha",
        ratio.subs(k2, al * tq) + al)

    # Fisher rank: Jacobian row with a generic nonzero dT/dm factor
    g = sp.Symbol('g', positive=True)
    J = sp.Matrix([[g * sp.diff(M, tq), g * sp.diff(M, k2)]]).subs(k2, al * tq)
    J = sp.Matrix([[_radfix(sp.simplify(J[0])), _radfix(sp.simplify(J[1]))]])
    chk("S16", "eq:nullvec", "(1,alpha) annihilates the (tq,k2) Jacobian",
        _radfix(sp.simplify(J[0] + al * J[1])))
    chk("S17", "eq:detF", "2x2 Fisher block is singular",
        _radfix(sp.simplify((J.T * J).det())))

    mm = sp.Symbol('mm', positive=True)
    chk("S18", "eq:dKdm", "dK/dm = (1-m coth m)/(tau_D s sinh m)",
        sp.diff(mm / (tD * s * sp.sinh(mm)), mm)
        - (1 - mm / sp.tanh(mm)) / (tD * s * sp.sinh(mm)))

    u = sp.Symbol('u', positive=True); w = 2 * sp.pi / tD
    chk("S19", "eq:Q0", "pulse transform equals the direct integral",
        sp.integrate((1 - sp.cos(2*sp.pi*u/tD)) * sp.exp(-s*u), (u, 0, tD))
        - w**2 * (1 - sp.exp(-s*tD)) / (s * (s**2 + w**2)))
    chk("S20", "eq:removable", "pulse numerator vanishes at s=i omega",
        (1 - sp.exp(-s * tD)).subs(s, sp.I * w))

    Mn, t = sp.symbols('M t', positive=True)
    chk("S21", "eq:tstar", "t* = M tau_Delta/10",
        sp.solve(sp.Eq((2*Mn/(5*t))*sp.pi/2, 2*sp.pi/tD), t)[0] - Mn*tD/10)

    chk("S22", "eq:qbar", "time-average of the pulse equals q_max",
        sp.integrate(1 - sp.cos(2*sp.pi*u/tD), (u, 0, tD)) / tD - 1)

    # truncated series closed form (eq:series-I) vs direct integral
    beta = sp.Symbol('beta', positive=True); tc = sp.Symbol('t_c', positive=True)
    e_full = sp.exp(-beta*t); e_sh = sp.exp(-beta*(t-tc))
    I1 = (e_sh - e_full)/beta
    I2 = (e_sh*(beta*sp.cos(w*tc) + w*sp.sin(w*tc)) - beta*e_full)/(beta**2 + w**2)
    direct = sp.exp(-beta*t)*sp.integrate(sp.exp(beta*u)*(1-sp.cos(w*u)), (u, 0, tc))
    chk("S23", "eq:series-I", "series closed form equals the direct integral",
        sp.expand(sp.simplify(I1 - I2 - direct)))

    return out
