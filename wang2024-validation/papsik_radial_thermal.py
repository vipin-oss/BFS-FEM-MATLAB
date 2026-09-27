#!/usr/bin/env python3
"""1-D radial finite-volume thermal baseline for Papšík et al. rod inputs.

This is a reduced homogeneous-cylinder thermal calculation, not the paper's
2-D axisymmetric ANSYS model and not a fracture simulation. It is useful for
checking the public h, radius, conductivity, density, and heat-capacity inputs
before a fracture model is attempted. Only the Python standard library is used.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ThermalMaterial:
    name: str
    rho: float  # kg/m^3
    cp: float  # J/(kg K)
    k: float  # W/(m K)


ALUMINA = ThermalMaterial("Alumina APDL", rho=3787.0, cp=880.0, k=34.0)
ZTA = ThermalMaterial("ZTA APDL", rho=4345.0, cp=665.0, k=22.0)
RADIUS = 2.5e-3  # m; 5 mm rod diameter from the public APDL geometry
H = 50_000.0  # W/(m^2 K); lateral convection in the public APDL input
T_AMBIENT = 20.0  # deg C
DELTA_T = 100.0  # K; APDL default when no temperature_difference is supplied
END_TIME = 0.100  # s; APDL thermal analysis end time


def solve_tridiagonal(lower: list[float], diag: list[float], upper: list[float], rhs: list[float]) -> list[float]:
    """Thomas algorithm for a strictly diagonally dominant tridiagonal system."""
    n = len(diag)
    if not (len(lower) == len(upper) == len(rhs) == n):
        raise ValueError("tridiagonal arrays must have equal lengths")
    c = upper.copy()
    d = rhs.copy()
    b = diag.copy()
    for i in range(1, n):
        if b[i - 1] == 0.0:
            raise ArithmeticError("zero pivot in tridiagonal solve")
        factor = lower[i] / b[i - 1]
        b[i] -= factor * c[i - 1]
        d[i] -= factor * d[i - 1]
    x = [0.0] * n
    x[-1] = d[-1] / b[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (d[i] - c[i] * x[i + 1]) / b[i]
    return x


def radial_step(
    old: list[float], material: ThermalMaterial, radius: float, h: float,
    ambient: float, dt: float,
) -> tuple[list[float], float]:
    """One backward-Euler FV step; returns new cell temperatures and heat rate out."""
    n = len(old)
    dr = radius / n
    # Unit axial length. Cell volume is an annulus; all axial-length factors cancel.
    cap = [
        material.rho * material.cp * math.pi * (((i + 1) * dr) ** 2 - (i * dr) ** 2)
        for i in range(n)
    ]
    conductance = [0.0] * n  # conductance between cell i-1 and i, i>=1
    for i in range(1, n):
        r_left_center = (i - 0.5) * dr
        r_right_center = (i + 0.5) * dr
        resistance = math.log(r_right_center / r_left_center) / (2.0 * math.pi * material.k)
        conductance[i] = 1.0 / resistance

    if h <= 0.0:
        boundary_g = 0.0
    else:
        outer_center = (n - 0.5) * dr
        r_cond = math.log(radius / outer_center) / (2.0 * math.pi * material.k)
        r_conv = 1.0 / (h * 2.0 * math.pi * radius)
        boundary_g = 1.0 / (r_cond + r_conv)

    lower = [0.0] * n
    diag = [0.0] * n
    upper = [0.0] * n
    rhs = [0.0] * n
    for i in range(n):
        g_left = conductance[i]
        g_right = conductance[i + 1] if i < n - 1 else boundary_g
        lower[i] = -g_left
        upper[i] = -g_right
        diag[i] = cap[i] / dt + g_left + g_right
        rhs[i] = cap[i] / dt * old[i]
        if i == n - 1:
            rhs[i] += boundary_g * ambient
    new = solve_tridiagonal(lower, diag, upper, rhs)
    heat_rate_out = boundary_g * (new[-1] - ambient)
    return new, heat_rate_out


def run(material: ThermalMaterial, n_cells: int, dt: float, h: float = H) -> dict[str, float]:
    steps_float = END_TIME / dt
    steps = round(steps_float)
    if abs(steps_float - steps) > 1.0e-10:
        raise ValueError("dt must divide the end time exactly")
    old = [T_AMBIENT + DELTA_T] * n_cells
    initial_energy_per_length = math.fsum(
        material.rho * material.cp * math.pi * (((i + 1) * RADIUS / n_cells) ** 2 - (i * RADIUS / n_cells) ** 2)
        * (old[i] - T_AMBIENT)
        for i in range(n_cells)
    )
    removed_energy = 0.0
    for _ in range(steps):
        old, q_out = radial_step(old, material, RADIUS, h, T_AMBIENT, dt)
        removed_energy += q_out * dt

    dr = RADIUS / n_cells
    outer_center = (n_cells - 0.5) * dr
    if h > 0.0:
        r_cond = math.log(RADIUS / outer_center) / (2.0 * math.pi * material.k)
        r_conv = 1.0 / (h * 2.0 * math.pi * RADIUS)
        boundary_g = 1.0 / (r_cond + r_conv)
        q_end = boundary_g * (old[-1] - T_AMBIENT)
        surface_temperature = T_AMBIENT + q_end / (h * 2.0 * math.pi * RADIUS)
    else:
        surface_temperature = old[-1]
    remaining_energy = math.fsum(
        material.rho * material.cp * math.pi * (((i + 1) * dr) ** 2 - (i * dr) ** 2)
        * (old[i] - T_AMBIENT)
        for i in range(n_cells)
    )
    balance_error = (initial_energy_per_length - removed_energy - remaining_energy) / initial_energy_per_length
    return {
        "center_c": old[0],
        "outer_cell_c": old[-1],
        "surface_c": surface_temperature,
        "removed_energy_j_per_m": removed_energy,
        "remaining_energy_j_per_m": remaining_energy,
        "energy_balance_relative": balance_error,
    }


def run_core_shell(n_cells: int, dt: float) -> dict[str, float]:
    """Thermal-only ZTA core / 0.4 mm alumina shell, using article geometry.

    The published article specifies the 400 um shell; the supplied APDL geometry
    file itself resets layer_thickness to zero. This calculation is therefore an
    independent article-geometry thermal case, not a reproduction of that APDL run.
    """
    shell_thickness = 0.4e-3
    interface_radius = RADIUS - shell_thickness
    dr = RADIUS / n_cells
    core_cells_float = interface_radius / dr
    core_cells = round(core_cells_float)
    if abs(core_cells_float - core_cells) > 1e-10:
        raise ValueError("mesh must align with the 0.4 mm shell interface")
    materials = [ZTA if i < core_cells else ALUMINA for i in range(n_cells)]
    steps_float = END_TIME / dt
    steps = round(steps_float)
    if abs(steps_float - steps) > 1e-10:
        raise ValueError("dt must divide the end time exactly")

    old = [T_AMBIENT + DELTA_T] * n_cells
    def cell_capacity(i: int) -> float:
        mat = materials[i]
        return mat.rho * mat.cp * math.pi * (((i + 1) * dr) ** 2 - (i * dr) ** 2)
    capacities = [cell_capacity(i) for i in range(n_cells)]
    initial_energy = math.fsum(capacities[i] * (old[i] - T_AMBIENT) for i in range(n_cells))
    removed_energy = 0.0

    outer_material = materials[-1]
    outer_center = (n_cells - 0.5) * dr
    r_cond = math.log(RADIUS / outer_center) / (2.0 * math.pi * outer_material.k)
    r_conv = 1.0 / (H * 2.0 * math.pi * RADIUS)
    boundary_g = 1.0 / (r_cond + r_conv)

    for _ in range(steps):
        conductance = [0.0] * n_cells
        for i in range(1, n_cells):
            r_face = i * dr
            r_left = (i - 0.5) * dr
            r_right = (i + 0.5) * dr
            resistance = (
                math.log(r_face / r_left) / (2.0 * math.pi * materials[i - 1].k)
                + math.log(r_right / r_face) / (2.0 * math.pi * materials[i].k)
            )
            conductance[i] = 1.0 / resistance

        lower = [0.0] * n_cells
        diag = [0.0] * n_cells
        upper = [0.0] * n_cells
        rhs = [0.0] * n_cells
        for i in range(n_cells):
            g_left = conductance[i]
            g_right = conductance[i + 1] if i < n_cells - 1 else boundary_g
            lower[i] = -g_left
            upper[i] = -g_right
            diag[i] = capacities[i] / dt + g_left + g_right
            rhs[i] = capacities[i] / dt * old[i]
            if i == n_cells - 1:
                rhs[i] += boundary_g * T_AMBIENT
        old = solve_tridiagonal(lower, diag, upper, rhs)
        removed_energy += boundary_g * (old[-1] - T_AMBIENT) * dt

    remaining_energy = math.fsum(capacities[i] * (old[i] - T_AMBIENT) for i in range(n_cells))
    q_end = boundary_g * (old[-1] - T_AMBIENT)
    surface_temperature = T_AMBIENT + q_end / (H * 2.0 * math.pi * RADIUS)
    return {
        "center_c": old[0],
        "outer_cell_c": old[-1],
        "surface_c": surface_temperature,
        "energy_balance_relative": (initial_energy - removed_energy - remaining_energy) / initial_energy,
    }


def main() -> None:
    print("Papšík public-input radial thermal baseline (reduced model; not ANSYS/FEM/fracture)")
    print(f"R={RADIUS*1e3:g} mm, h={H:g} W/(m^2 K), T_inf={T_AMBIENT:g} C, dT0={DELTA_T:g} K, t_end={END_TIME*1e3:g} ms")
    print("Cells  dt(ms)  Material          Tcenter(C)  Tsurface(C)  balance residual")
    outputs: dict[tuple[str, int, float], dict[str, float]] = {}
    mesh_counts = (50, 100, 200)
    time_steps = (1e-3, 5e-4, 2.5e-4)
    for material in (ALUMINA, ZTA):
        for n_cells in mesh_counts:
            for dt in time_steps:
                result = run(material, n_cells, dt)
                outputs[(material.name, n_cells, dt)] = result
                print(
                    f"{n_cells:5d}  {dt*1e3:6.3f}  {material.name:16s}"
                    f" {result['center_c']:11.5f} {result['surface_c']:12.5f}"
                    f" {result['energy_balance_relative']:+.3e}"
                )
                assert abs(result["energy_balance_relative"]) < 2e-10
                assert T_AMBIENT < result["surface_c"] < result["center_c"] < T_AMBIENT + DELTA_T

        # Check mesh convergence at fixed dt, and time convergence at fixed mesh.
        mesh_coarse = outputs[(material.name, 50, 2.5e-4)]
        mesh_fine = outputs[(material.name, 200, 2.5e-4)]
        time_coarse = outputs[(material.name, 200, 1e-3)]
        time_fine = outputs[(material.name, 200, 2.5e-4)]
        for coarse, fine in ((mesh_coarse, mesh_fine), (time_coarse, time_fine)):
            assert abs(fine["center_c"] - coarse["center_c"]) < 0.15
            assert abs(fine["surface_c"] - coarse["surface_c"]) < 0.15

    print("\nZTA core / 0.4 mm alumina shell (article geometry; thermal-only independent case)")
    layer_outputs: dict[tuple[int, float], dict[str, float]] = {}
    for n_cells in mesh_counts:
        for dt in time_steps:
            result = run_core_shell(n_cells, dt)
            layer_outputs[(n_cells, dt)] = result
            print(
                f"{n_cells:5d}  {dt*1e3:6.3f}  {'ZTA/A shell':16s}"
                f" {result['center_c']:11.5f} {result['surface_c']:12.5f}"
                f" {result['energy_balance_relative']:+.3e}"
            )
            assert abs(result["energy_balance_relative"]) < 2e-10
            assert T_AMBIENT < result["surface_c"] < result["outer_cell_c"] < T_AMBIENT + DELTA_T
    for coarse, fine in (
        (layer_outputs[(50, 2.5e-4)], layer_outputs[(200, 2.5e-4)]),
        (layer_outputs[(200, 1e-3)], layer_outputs[(200, 2.5e-4)]),
    ):
        assert abs(fine["center_c"] - coarse["center_c"]) < 0.15
        assert abs(fine["surface_c"] - coarse["surface_c"]) < 0.15

    # Adiabatic unit-limit check: with h=0, no heat can leave and a uniform
    # initial temperature must remain uniform to roundoff for any mesh/time step.
    insulated = run(ALUMINA, 40, 1e-3, h=0.0)
    assert abs(insulated["center_c"] - (T_AMBIENT + DELTA_T)) < 1e-9
    assert abs(insulated["surface_c"] - (T_AMBIENT + DELTA_T)) < 1e-9
    assert abs(insulated["energy_balance_relative"]) < 1e-10
    print("PASS: mesh/time refinement, energy balance, temperature ordering, and h=0 limit.")
    print("LIMIT: reduced radial thermal components only (homogeneous and layered); no finite-length/end effects, residual stress, cracks, or fracture criterion.")


if __name__ == "__main__":
    main()
