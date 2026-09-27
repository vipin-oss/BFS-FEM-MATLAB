#!/usr/bin/env python3
"""Independent one-element thermoelastic limiting-case check for Wang et al. (2024).

This is an algebraic verification of Appendix A at the PF-CZM strength onset,
not a finite-element/Abaqus reproduction. It uses only Python's standard library.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    E_pa: float = 370e9           # Table 2: 370 GPa
    nu: float = 0.22              # Table 2
    alpha_per_K: float = 8.0e-6   # Table 2: 1/K
    ft_pa: float = 180e6          # Table 2: 180 MPa
    gc_n_per_mm: float = 0.0425   # Table 2: N/mm


M = Material()


def isotropic_normal_stress(eps_x: float, delta_t_signed_K: float) -> tuple[float, float, float]:
    """Return (sigma_x, sigma_y, sigma_z) for eps=[eps_x,eps_x,0].

    The four lateral faces are traction-free; the z-normal strain is constrained
    to zero, matching Appendix A's stated one-direction constraint.
    """
    e_th = M.alpha_per_K * delta_t_signed_K
    elastic = (eps_x - e_th, eps_x - e_th, -e_th)
    lam = M.E_pa * M.nu / ((1.0 + M.nu) * (1.0 - 2.0 * M.nu))
    mu = M.E_pa / (2.0 * (1.0 + M.nu))
    trace = sum(elastic)
    return tuple(lam * trace + 2.0 * mu * e for e in elastic)  # type: ignore[return-value]


def appendix_a5_residual(eps_x: float, delta_t_signed_K: float) -> float:
    """Left-hand side of printed Eq. (A5), in strain units."""
    e_th = M.alpha_per_K * delta_t_signed_K
    return (1.0 - M.nu) * (eps_x - e_th) + M.nu * (eps_x - e_th) - M.nu * e_th


def appendix_a6_sigma_z(eps_x: float, delta_t_signed_K: float) -> float:
    """Right-hand side of printed Eq. (A6)."""
    e_th = M.alpha_per_K * delta_t_signed_K
    denom = (1.0 + M.nu) * (1.0 - 2.0 * M.nu)
    return M.E_pa / denom * (2.0 * M.nu * (eps_x - e_th) - (1.0 - M.nu) * e_th)


def main() -> None:
    # Use signed DeltaT for the equations: cooling by theta means DeltaT=-theta.
    # The plotted/documented "temperature drop" is the positive magnitude theta.
    theta_crit_K = M.ft_pa / (M.E_pa * M.alpha_per_K)
    delta_t_signed_K = -theta_crit_K

    # Isotropic thermoelastic solution of sigma_x=sigma_y=0, eps_z=0.
    eps_x_correct = (1.0 + M.nu) * M.alpha_per_K * delta_t_signed_K
    sigma_correct = isotropic_normal_stress(eps_x_correct, delta_t_signed_K)

    # Eq. (A7) as printed in the paper uses (1-nu), which is tested separately.
    eps_x_printed = (1.0 - M.nu) * M.alpha_per_K * delta_t_signed_K
    sigma_printed = isotropic_normal_stress(eps_x_printed, delta_t_signed_K)
    sigma_z_a6_printed = appendix_a6_sigma_z(eps_x_printed, delta_t_signed_K)

    # For PF-CZM, d=0 at onset makes Eq. (A11) reduce to E^2 alpha^2 theta^2 / ft^2 = 1.
    a11_rhs_at_onset = (M.E_pa * M.alpha_per_K * theta_crit_K / M.ft_pa) ** 2
    a11_onset_residual = 1.0 - a11_rhs_at_onset

    # Eq. (25), using 0.0425 N/mm = 42.5 N/m.
    gc_n_per_m = M.gc_n_per_mm * 1000.0
    lch_m = M.E_pa * gc_n_per_m / (M.ft_pa**2)

    # Assertions: correct isotropic state satisfies Appendix A5/A6/A8 and the PF-CZM onset.
    assert abs(appendix_a5_residual(eps_x_correct, delta_t_signed_K)) < 1e-14
    assert abs(sigma_correct[0]) < 1e-6 and abs(sigma_correct[1]) < 1e-6
    assert abs(sigma_correct[2] - M.ft_pa) < 1e-6
    assert abs(appendix_a6_sigma_z(eps_x_correct, delta_t_signed_K) - M.ft_pa) < 1e-6
    assert abs(a11_onset_residual) < 1e-14

    # The printed A7 value does not satisfy the free-side condition or its own A5/A6.
    assert abs(appendix_a5_residual(eps_x_printed, delta_t_signed_K)) > 1e-8
    assert abs(sigma_printed[0]) > 1e6
    assert abs(sigma_z_a6_printed - M.ft_pa) > 1e6

    print("Wang et al. (2024), Appendix A one-element limit — independent algebra check")
    print("Scope: no FE mesh/solver; homogeneous isotropic element, eps_z=0, four free faces.")
    print("Convention: positive theta is cooling magnitude; signed DeltaT = -theta.")
    print(f"E*alpha = {M.E_pa * M.alpha_per_K / 1e6:.6f} MPa/K")
    print(f"PF-CZM onset theta_c = ft/(E*alpha) = {theta_crit_K:.9f} K")
    print(f"At onset: sigma_z = {sigma_correct[2] / 1e6:.6f} MPa; H = {0.5 * M.E_pa * M.alpha_per_K**2 * theta_crit_K**2:.6f} J/m^3")
    print(f"Correct free-side strain (A5/A6/A8): eps_x = {eps_x_correct:.12g}; sigma_x = {sigma_correct[0]:.6g} Pa")
    print(f"Eq. (A7) as printed:             eps_x = {eps_x_printed:.12g}; sigma_x = {sigma_printed[0] / 1e6:.6f} MPa")
    print(f"A5 residual using printed A7 = {appendix_a5_residual(eps_x_printed, delta_t_signed_K):.12g}")
    print(f"A6 sigma_z using printed A7 = {sigma_z_a6_printed / 1e6:.6f} MPa (A8 gives 180.000000 MPa)")
    print(f"PF-CZM A11 onset residual at d=0 = {a11_onset_residual:.3g}")
    print(f"Derived Griffith length l_ch = {lch_m * 1e3:.9f} mm")
    print("NOT COMPUTED: absolute d(DeltaT) curves; the base-case l_c is not reported, so a1=4/pi*l_ch/l_c is unknown.")


if __name__ == "__main__":
    main()
