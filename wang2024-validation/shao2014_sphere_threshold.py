#!/usr/bin/env python3
"""Independent reproduction of Shao et al. (2014) spherical-quench threshold.

This is a separate thermoelastic benchmark for the experimental source cited by
Wang et al. (2024). It is NOT a simulation or validation of Wang's PF-CZM code.
Only Python's standard library is used.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Alumina:
    # Shao et al. (2014), Table 1, average properties over 20--600 deg C.
    young_pa: float = 380.0e9
    poisson: float = 0.22
    tensile_strength_pa: float = 358.0e6
    convection_w_m2k: float = 80_000.0
    conductivity_w_mk: float = 18.4
    expansion_per_k: float = 7.7e-6


MATERIAL = Alumina()
RADII_MM = (2.10, 1.00, 0.56, 0.35, 0.11)
# (upper temperature range, E in GPa, strength in MPa, k in W/(m K), alpha in 1/K)
SHAO_TABLE1_ROWS = (
    (300, 383.0, 386.0, 24.9, 7.0e-6),
    (400, 382.0, 374.0, 22.2, 7.3e-6),
    (600, 380.0, 358.0, 18.4, 7.7e-6),
    (800, 378.0, 347.0, 15.7, 8.0e-6),
    (1300, 348.0, 324.0, 12.0, 8.7e-6),
)


def _characteristic_roots(biot: float, count: int) -> list[float]:
    """Solve beta_n*cot(beta_n)=1-Biot using one root per half-wave."""
    if biot <= 0.0:
        raise ValueError("Biot number must be positive")

    def residual(beta: float) -> float:
        return 1.0 - beta * math.cos(beta) / math.sin(beta) - biot

    roots: list[float] = []
    eps = 1.0e-10
    for n in range(count):
        if abs(biot - 1.0) < 1.0e-14:
            roots.append((n + 0.5) * math.pi)
            continue
        if biot < 1.0:
            lo = n * math.pi + eps
            hi = n * math.pi + 0.5 * math.pi - eps
        else:
            lo = n * math.pi + 0.5 * math.pi + eps
            hi = (n + 1) * math.pi - eps
        flo, fhi = residual(lo), residual(hi)
        if flo * fhi >= 0.0:
            raise ArithmeticError(f"Could not bracket eigenvalue n={n}, Bi={biot}")
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            fmid = residual(mid)
            if flo * fmid <= 0.0:
                hi, fhi = mid, fmid
            else:
                lo, flo = mid, fmid
        roots.append(0.5 * (lo + hi))
    return roots


def _series_terms(biot: float, count: int) -> list[tuple[float, float, float]]:
    terms = []
    for beta in _characteristic_roots(biot, count):
        sin_b, cos_b = math.sin(beta), math.cos(beta)
        # Shao et al. Eq. (6), temperature-series coefficient.
        a_n = 2.0 * (sin_b - beta * cos_b) / (beta - sin_b * cos_b)
        # Surface hoop-stress series after evaluating Eq. (9) at r=R.
        stress_coefficient = a_n * (
            3.0 * sin_b / beta**3 - 3.0 * cos_b / beta**2 - sin_b / beta
        )
        terms.append((beta, stress_coefficient, beta * beta))
    return terms


def dimensionless_surface_stress_max(biot: float, modes: int = 120) -> tuple[float, float]:
    """Return max_F q(F,Bi) and its Fourier number F.

    For cooling magnitude DeltaT>0, sigma_theta(R,F) =
    E*alpha*DeltaT/(1-nu) * q(F,Bi), where F=a*t/R^2. The maximum depends
    on Bi=hR/k, not on thermal diffusivity; diffusivity only sets the time of
    the maximum. This is why missing rho*cp does not prevent reproducing the
    threshold curve from Shao's Table 1.
    """
    terms = _series_terms(biot, modes)

    def q_at_log_fourier(log10_f: float) -> float:
        fourier = 10.0**log10_f
        return math.fsum(c * math.exp(-lam * fourier) for _, c, lam in terms)

    # Bracket the maximum on a log-time scan, then refine with golden-section.
    lo_log, hi_log, samples = -9.0, 1.0, 1200
    values = [
        q_at_log_fourier(lo_log + (hi_log - lo_log) * i / (samples - 1))
        for i in range(samples)
    ]
    best = max(range(samples), key=values.__getitem__)
    if best == 0 or best == samples - 1:
        raise ArithmeticError("Maximum lies outside the Fourier-number search range")
    a = lo_log + (hi_log - lo_log) * (best - 1) / (samples - 1)
    b = lo_log + (hi_log - lo_log) * (best + 1) / (samples - 1)

    phi = (math.sqrt(5.0) - 1.0) / 2.0
    x1, x2 = b - phi * (b - a), a + phi * (b - a)
    y1, y2 = q_at_log_fourier(x1), q_at_log_fourier(x2)
    for _ in range(100):
        if y1 < y2:
            a, x1, y1 = x1, x2, y2
            x2 = a + phi * (b - a)
            y2 = q_at_log_fourier(x2)
        else:
            b, x2, y2 = x2, x1, y1
            x1 = b - phi * (b - a)
            y1 = q_at_log_fourier(x1)
    log_f_max = 0.5 * (a + b)
    return q_at_log_fourier(log_f_max), 10.0**log_f_max


def critical_drop_k(q_max: float, material: Alumina = MATERIAL) -> float:
    return (
        material.tensile_strength_pa * (1.0 - material.poisson)
        / (material.young_pa * material.expansion_per_k * q_max)
    )


def main() -> None:
    print("Shao et al. (2014) — independent spherical-quench threshold reproduction")
    print("Model: spherical transient conduction + thermoelastic surface hoop stress;")
    print("        Table 1, 20–600 °C properties; no FEM and no Wang PF-CZM code.")
    print("R (mm)   Bi       q_max      F_at_max    predicted DeltaT_crit (K)")
    results: dict[float, tuple[float, float, float]] = {}
    for radius_mm in RADII_MM:
        radius_m = radius_mm * 1.0e-3
        biot = MATERIAL.convection_w_m2k * radius_m / MATERIAL.conductivity_w_mk
        q_max, fourier_max = dimensionless_surface_stress_max(biot)
        delta_crit = critical_drop_k(q_max)
        assert q_max > 0.0 and delta_crit > 0.0
        results[radius_mm] = (biot, q_max, delta_crit)
        print(
            f"{radius_mm:5.2f}   {biot:7.4f}   {q_max:8.6f}"
            f"   {fourier_max:9.6f}       {delta_crit:9.2f}"
        )

    # Basic numerical and physical checks; the 80- and 120-mode series agree.
    for radius_mm in RADII_MM:
        biot, q120, critical_120 = results[radius_mm]
        q80, _ = dimensionless_surface_stress_max(biot, modes=80)
        critical_80 = critical_drop_k(q80)
        assert abs(critical_80 - critical_120) / critical_120 < 1.0e-6
    criticals_in_radius_order = [results[r][2] for r in RADII_MM]
    assert all(a < b for a, b in zip(criticals_in_radius_order, criticals_in_radius_order[1:]))

    # Text-reported experimental checks in Shao et al. (2014), p. 4.
    # The observations are inequalities / approximate markers, not tabulated exact thresholds.
    crit_21 = results[2.10][2]
    crit_035 = results[0.35][2]
    crit_011 = results[0.11][2]
    diff_21 = 100.0 * (crit_21 - 240.0) / 240.0
    diff_035 = 100.0 * (crit_035 - 620.0) / 620.0
    print("\nComparison to the paper's text-reported observations (not exact tabulated points):")
    print(
        f"R=2.10 mm: predicted {crit_21:.1f} K vs ~240 K narrative marker "
        f"({diff_21:+.1f}%); prediction is lower."
    )
    print(
        f"R=0.35 mm: predicted {crit_035:.1f} K vs >620 K reported requirement "
        f"({diff_035:+.1f}% vs 620 K); prediction is lower."
    )
    print(
        f"R=0.11 mm: predicted {crit_011:.1f} K; no cracks are reported at 1280 K "
        f"(predicted threshold is {crit_011 - 1280.0:.1f} K higher)."
    )
    print("\nSensitivity to all Table 1 average-property rows (thresholds in K):")
    print("Range (°C)     R=2.10 mm     R=0.35 mm     R=0.11 mm")
    sensitivity: dict[int, tuple[float, float, float]] = {}
    for upper_c, young_gpa, strength_mpa, conductivity, expansion in SHAO_TABLE1_ROWS:
        material = Alumina(
            young_pa=young_gpa * 1.0e9,
            poisson=0.22,
            tensile_strength_pa=strength_mpa * 1.0e6,
            convection_w_m2k=80_000.0,
            conductivity_w_mk=conductivity,
            expansion_per_k=expansion,
        )
        criticals = []
        for radius_mm in (2.10, 0.35, 0.11):
            biot = material.convection_w_m2k * radius_mm * 1.0e-3 / material.conductivity_w_mk
            q_max, _ = dimensionless_surface_stress_max(biot)
            criticals.append(critical_drop_k(q_max, material))
        sensitivity[upper_c] = tuple(criticals)  # type: ignore[assignment]
        print(f"20–{upper_c:<4}       {criticals[0]:9.1f}      {criticals[1]:9.1f}      {criticals[2]:9.1f}")

    # Shao et al. state that their 20–400 and 20–600 °C property curves agree
    # with the experimental boundary; these rows should bracket the prose markers.
    assert sensitivity[400][0] > 240.0 > sensitivity[600][0]
    assert sensitivity[400][1] > 620.0 > sensitivity[600][1]
    assert sensitivity[400][2] > 1280.0 and sensitivity[600][2] > 1280.0
    print("RESULT: the 20–400 and 20–600 °C property rows bracket the two larger-sphere")
    print("         narrative markers and both predict no crack at 1280 K for R=0.11 mm.")

    # Diagnostic only: apply the same linear-elastic sphere formula to Wang 2024's
    # Table 2 values. This is not a reproduction of its PF-CZM or water-entry history.
    wang2024_material = Alumina(
        young_pa=370.0e9,
        poisson=0.22,
        tensile_strength_pa=180.0e6,
        convection_w_m2k=80_000.0,
        conductivity_w_mk=12.0,
        expansion_per_k=8.0e-6,
    )
    print("\nDiagnostic only: spherical threshold using Wang (2024) Table 2 material values")
    print("R (mm)   predicted DeltaT_crit (K); not a reproduction of the PF-CZM ball simulation")
    for radius_mm in RADII_MM:
        biot = wang2024_material.convection_w_m2k * radius_mm * 1.0e-3 / wang2024_material.conductivity_w_mk
        q_max, _ = dimensionless_surface_stress_max(biot)
        print(f"{radius_mm:5.2f}   {critical_drop_k(q_max, wang2024_material):9.1f}")
    print("         This exposes sensitivity to the non-matching tensile strength/property set;")
    print("         compare only as a parameter-traceability diagnostic, not experiment validation.")
    print("         The whole script checks Shao's analytic benchmark, not Wang's FEM solver.")


if __name__ == "__main__":
    main()
