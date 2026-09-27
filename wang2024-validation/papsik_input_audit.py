#!/usr/bin/env python3
"""Source-input sanity audit for Papšík et al. (2024) public APDL inputs.

This script evaluates simple unit conversions and thermal scales from values
visible in the public Zenodo APDL files. It does NOT run ANSYS, reconstruct the
finite-fracture-mechanics solver, or validate any crack prediction.
Only Python's standard library is required.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Material:
    name: str
    density_kg_m3: float
    conductivity_w_mk: float
    heat_capacity_j_kgk: float
    young_pa: float
    poisson: float
    alpha_per_k: float
    kic_mpa_sqrt_m: float
    apdl_characteristic_strength_mpa: float
    apdl_weibull_modulus: float


# Values read from thermoshock-02-material-ALO.inp and
# thermoshock-02-material-ZTA.inp in Zenodo record 13970234.
ALUMINA = Material(
    name="Alumina (A100 APDL)",
    density_kg_m3=3787.0,
    conductivity_w_mk=34.0,
    heat_capacity_j_kgk=880.0,
    young_pa=367.0e9,
    poisson=0.22,
    alpha_per_k=8.39e-6,
    kic_mpa_sqrt_m=3.130,
    apdl_characteristic_strength_mpa=645.0,
    apdl_weibull_modulus=13.6,
)
ZTA = Material(
    name="ZTA (A20TZ APDL)",
    density_kg_m3=4345.0,
    conductivity_w_mk=22.0,
    heat_capacity_j_kgk=665.0,
    young_pa=333.0e9,
    poisson=0.22,
    alpha_per_k=8.95e-6,
    kic_mpa_sqrt_m=4.020,
    apdl_characteristic_strength_mpa=902.0,
    apdl_weibull_modulus=13.6,
)

# Shared settings read from the published APDL input files.
H_W_M2K = 50_000.0
RADIUS_M = 2.5e-3
ANALYSIS_END_S = 0.100


def fracture_energy_j_m2(material: Material) -> float:
    """Plane-strain Gc = K_Ic^2 (1-nu^2)/E, with K in SI units."""
    kic_pa_sqrt_m = material.kic_mpa_sqrt_m * 1.0e6
    return kic_pa_sqrt_m**2 * (1.0 - material.poisson**2) / material.young_pa


def scales(material: Material) -> dict[str, float]:
    diffusivity = material.conductivity_w_mk / (
        material.density_kg_m3 * material.heat_capacity_j_kgk
    )
    biot = H_W_M2K * RADIUS_M / material.conductivity_w_mk
    radial_diffusion_time = RADIUS_M**2 / diffusivity
    return {
        "diffusivity_m2_s": diffusivity,
        "radial_biot": biot,
        "radial_diffusion_time_s": radial_diffusion_time,
        "fourier_at_100ms": ANALYSIS_END_S / radial_diffusion_time,
        "diffusion_length_at_100ms_mm": math.sqrt(diffusivity * ANALYSIS_END_S) * 1e3,
        "fracture_energy_j_m2": fracture_energy_j_m2(material),
    }


def main() -> None:
    print("Papšík et al. (2024) public APDL input audit — not an FEM run")
    print("Source: Zenodo 13970234, CC BY 4.0; article DOI 10.1016/j.engfracmech.2024.110121")
    print(f"Shared APDL h={H_W_M2K:.0f} W/(m^2 K), R={RADIUS_M*1e3:.1f} mm, end time={ANALYSIS_END_S*1e3:.0f} ms")
    print("Thermal BC in source: lateral surface convects; end faces are commented out.")
    print("\nMaterial-derived checks:")
    print("Material             diffusivity (m^2/s)   Bi_R     R^2/a (s)   Fo(100ms)   sqrt(a t) (mm)   Gc (J/m^2)")
    for material in (ALUMINA, ZTA):
        result = scales(material)
        print(
            f"{material.name:20s} {result['diffusivity_m2_s']:14.6e}"
            f" {result['radial_biot']:8.4f} {result['radial_diffusion_time_s']:11.4f}"
            f" {result['fourier_at_100ms']:11.4f}"
            f" {result['diffusion_length_at_100ms_mm']:16.3f}"
            f" {result['fracture_energy_j_m2']:13.3f}"
        )

    # Basic arithmetic/unit-conversion regression checks against values calculated
    # independently from the APDL inputs. These are not solver-verification tests.
    assert abs(scales(ALUMINA)["fracture_energy_j_m2"] - 25.43) < 0.03
    assert abs(scales(ZTA)["fracture_energy_j_m2"] - 46.18) < 0.03
    assert 3.67 < scales(ALUMINA)["radial_biot"] < 3.69
    assert 5.67 < scales(ZTA)["radial_biot"] < 5.70

    print("\nSource configuration blockers (must resolve before a reproduction):")
    print("- Geometry input defaults rod_height to 5 mm when no parameter is supplied; article rods are 50 mm long.")
    print("- Geometry input sets layer_thickness=0 um; a core-shell model needs an explicit nonzero source edit/configuration.")
    print("- Material files activate only the 20 C table row; elevated-temperature E/alpha rows are commented out.")
    print("- ZTA APDL uses characteristic strength 902 MPa and m=13.6; article Table 1 reports 1025 MPa and m=5.3.")
    print("- No ANSYS solver was run; the CSV/material spreadsheet and full archive checksum were not independently retrieved/verified.")
    print("PASS: unit conversions and dimensionless-scale arithmetic are internally consistent.")
    print("LIMIT: this script is an input audit, not verification or validation of the thermal/fracture FEM.")


if __name__ == "__main__":
    main()
