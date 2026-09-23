#!/usr/bin/env python3
"""Bogner-Fox-Schmit (BFS) C1 Bloch-Floquet finite element solver.

Provides validated element assembly, Bloch master-slave reduction,
generalized Hermitian eigensolving, MAC branch tracking, and gap extraction.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import eigh as geigh

# BFS shape function and Hermite indices
XEND = [0, 2, 2, 0]
YEND = [0, 0, 2, 2]


def idx(node: int, comp: int, typ: int) -> int:
    """DOF index: 4 nodes * 2 displacement components * 4 Hermite types = 32 DOFs."""
    return 8 * node + 4 * comp + typ


def hermite_num(s: float, h: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """1D cubic Hermite shape functions and their 1st and 2nd derivatives."""
    t = s / h
    H = np.array(
        [
            1.0 - 3.0 * t**2 + 2.0 * t**3,
            h * (t - 2.0 * t**2 + t**3),
            3.0 * t**2 - 2.0 * t**3,
            h * (-t**2 + t**3),
        ],
        dtype=float,
    )
    dH = np.array(
        [
            (-6.0 * t + 6.0 * t**2) / h,
            1.0 - 4.0 * t + 3.0 * t**2,
            (6.0 * t - 6.0 * t**2) / h,
            -2.0 * t + 3.0 * t**2,
        ],
        dtype=float,
    )
    d2H = np.array(
        [
            (-6.0 + 12.0 * t) / h**2,
            (-4.0 + 6.0 * t) / h,
            (6.0 - 12.0 * t) / h**2,
            (-2.0 + 6.0 * t) / h,
        ],
        dtype=float,
    )
    return H, dH, d2H


def gauss4() -> list[tuple[float, float]]:
    """4-point Gauss-Legendre quadrature on [-1, 1]. Exactly integrates polynomials up to degree 7."""
    a = np.sqrt(3.0 / 7.0 - 2.0 / 7.0 * np.sqrt(6.0 / 5.0))
    b = np.sqrt(3.0 / 7.0 + 2.0 / 7.0 * np.sqrt(6.0 / 5.0))
    wa = (18.0 + np.sqrt(30.0)) / 36.0
    wb = (18.0 - np.sqrt(30.0)) / 36.0
    return [(-b, wb), (-a, wa), (a, wa), (b, wb)]


def L_plane(l1: float, l2: float, theta: float) -> tuple[float, float, float]:
    """Rotated in-plane characteristic length tensor components L11, L22, L12.
    L = R^T diag(l1^2, l2^2) R where R is the planar rotation by angle theta.
    """
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]], dtype=float)
    D = np.diag([l1**2, l2**2])
    Lp = R.T @ D @ R
    return float(Lp[0, 0]), float(Lp[1, 1]), float(Lp[0, 1])


def semi_axes_from_ar(ar: float, l_iso: float = 0.20, rule: str = "volume_equivalent") -> tuple[float, float]:
    """Calculate semi-axes l1, l2 from aspect ratio AR = l1/l2.
    Default: volume_equivalent (area-preserving in 2D), so l1*l2 = l_iso^2.
    """
    if rule == "volume_equivalent":
        l1 = l_iso * np.sqrt(ar)
        l2 = l_iso / np.sqrt(ar)
    elif rule == "arithmetic_mean":
        l2 = 2.0 * l_iso / (ar + 1.0)
        l1 = ar * l2
    elif rule == "fixed_l2":
        l2 = 0.10
        l1 = ar * l2
    else:
        raise ValueError(f"Unknown scaling rule: {rule}")
    return float(l1), float(l2)


def assemble_KM(
    hx: float = 1.0,
    hy: float = 1.0,
    lam: float = 1.0,
    mu: float = 1.0,
    L11: float = 1.0,
    L22: float = 1.0,
    L12: float = 0.0,
    rho: float = 1.0,
    ell2: float = 0.04,
) -> tuple[np.ndarray, np.ndarray]:
    """Assemble 32x32 BFS element matrices:
    K = Kc + Kg (classical stiffness + Mindlin Form-II gradient stiffness with 1/10 factor)
    M = M0 + ell2 * Mg (classical mass + gradient micro-inertia mass).
    """
    Cbar = np.array([[lam + 2.0 * mu, lam, 0.0], [lam, lam + 2.0 * mu, 0.0], [0.0, 0.0, 2.0 * mu]], dtype=float)
    G = np.diag([1.0, 1.0, 2.0]) @ Cbar
    Lmat = np.array([[L11, L12], [L12, L22]], dtype=float)
    nd = gauss4()

    Kc = np.zeros((32, 32), dtype=float)
    Kg = np.zeros((32, 32), dtype=float)
    M0 = np.zeros((32, 32), dtype=float)
    Mg = np.zeros((32, 32), dtype=float)

    for xi, wi in nd:
        for eta, wj in nd:
            xv = (xi + 1.0) / 2.0 * hx
            yv = (eta + 1.0) / 2.0 * hy
            wjac = wi * wj * hx * hy / 4.0

            Hx, dHx, d2Hx = hermite_num(xv, hx)
            Hy, dHy, d2Hy = hermite_num(yv, hy)

            Nv = np.zeros((4, 4), dtype=float)
            Nx = np.zeros((4, 4), dtype=float)
            Ny = np.zeros((4, 4), dtype=float)
            Nxx = np.zeros((4, 4), dtype=float)
            Nxy = np.zeros((4, 4), dtype=float)
            Nyy = np.zeros((4, 4), dtype=float)

            for ndi in range(4):
                ax, ay = XEND[ndi], YEND[ndi]
                for ty in range(4):
                    dx = 1 if ty in (1, 3) else 0
                    dy = 1 if ty in (2, 3) else 0
                    ix, iy = ax + dx, ay + dy
                    Nv[ndi, ty] = Hx[ix] * Hy[iy]
                    Nx[ndi, ty] = dHx[ix] * Hy[iy]
                    Ny[ndi, ty] = Hx[ix] * dHy[iy]
                    Nxx[ndi, ty] = d2Hx[ix] * Hy[iy]
                    Nxy[ndi, ty] = dHx[ix] * dHy[iy]
                    Nyy[ndi, ty] = Hx[ix] * d2Hy[iy]

            Nmat = np.zeros((2, 32), dtype=float)
            B = np.zeros((3, 32), dtype=float)
            Bx = np.zeros((3, 32), dtype=float)
            By = np.zeros((3, 32), dtype=float)
            Nxmat = np.zeros((2, 32), dtype=float)
            Nymat = np.zeros((2, 32), dtype=float)

            for ndi in range(4):
                for c in range(2):
                    for ty in range(4):
                        j = idx(ndi, c, ty)
                        Nmat[c, j] = Nv[ndi, ty]
                        Nxmat[c, j] = Nx[ndi, ty]
                        Nymat[c, j] = Ny[ndi, ty]
                        if c == 0:
                            B[0, j] = Nx[ndi, ty]
                            B[2, j] = 0.5 * Ny[ndi, ty]
                            Bx[0, j] = Nxx[ndi, ty]
                            Bx[2, j] = 0.5 * Nxy[ndi, ty]
                            By[0, j] = Nxy[ndi, ty]
                            By[2, j] = 0.5 * Nyy[ndi, ty]
                        else:
                            B[1, j] = Ny[ndi, ty]
                            B[2, j] = 0.5 * Nx[ndi, ty]
                            Bx[1, j] = Nxy[ndi, ty]
                            Bx[2, j] = 0.5 * Nxx[ndi, ty]
                            By[1, j] = Nyy[ndi, ty]
                            By[2, j] = 0.5 * Nxy[ndi, ty]

            Kc += wjac * (B.T @ G @ B)
            Kg += wjac * (0.1) * (
                Lmat[0, 0] * (Bx.T @ G @ Bx)
                + Lmat[0, 1] * (Bx.T @ G @ By)
                + Lmat[1, 0] * (By.T @ G @ Bx)
                + Lmat[1, 1] * (By.T @ G @ By)
            )
            M0 += wjac * rho * (Nmat.T @ Nmat)
            Mg += wjac * rho * (Nxmat.T @ Nxmat + Nymat.T @ Nymat)

    return Kc + Kg, M0 + ell2 * Mg


def T_impl(kx: float, ky: float, L: float = 1.0) -> np.ndarray:
    """Bloch transformation matrix T (32x8) applying consistent Bloch phases
    to value and derivative DOFs for a 1-element BFS cell.
    """
    mx = np.exp(1j * kx * L)
    my = np.exp(1j * ky * L)
    phases = [1.0 + 0.0j, mx, mx * my, my]
    T = np.zeros((32, 8), dtype=complex)
    for n, ph in enumerate(phases):
        T[8 * n : 8 * (n + 1), :] = ph * np.eye(8, dtype=complex)
    return T


def reduce_mat(A: np.ndarray, T: np.ndarray) -> np.ndarray:
    """Bloch reduction: A_red = T^H A T."""
    return T.conj().T @ A @ T


def solve_bloch(
    K: np.ndarray,
    M: np.ndarray,
    kx: float,
    ky: float,
    L: float = 1.0,
    check_hermiticity: bool = True,
    tol_herm: float = 1e-12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, float]:
    """Solve the reduced Bloch eigenvalue problem [Kbar - omega^2 Mbar] d = 0.
    Returns:
        omegas: sorted frequencies sqrt(max(omega^2, 0)) (8,)
        omega2_vals: raw sorted omega^2 eigenvalues (8,)
        eigenvectors: Mbar-normalized eigenvectors (8, 8)
        Mbar: reduced mass matrix (8, 8)
        herm_err_K: relative Hermiticity error of Kbar
        herm_err_M: relative Hermiticity error of Mbar
    """
    T = T_impl(kx, ky, L)
    Kb = reduce_mat(K, T)
    Mb = reduce_mat(M, T)

    # Compute Hermiticity residuals
    nrm_K = np.linalg.norm(Kb, "fro")
    nrm_M = np.linalg.norm(Mb, "fro")
    diff_K = np.linalg.norm(Kb - Kb.conj().T, "fro")
    diff_M = np.linalg.norm(Mb - Mb.conj().T, "fro")
    herm_err_K = float(diff_K / nrm_K) if nrm_K > 0 else 0.0
    herm_err_M = float(diff_M / nrm_M) if nrm_M > 0 else 0.0

    if check_hermiticity:
        assert herm_err_K < tol_herm, f"Kbar non-Hermitian: rel error = {herm_err_K:.3e}"
        assert herm_err_M < tol_herm, f"Mbar non-Hermitian: rel error = {herm_err_M:.3e}"

    # Explicit Hermitization for machine-precision eigensolve
    Kb_sym = 0.5 * (Kb + Kb.conj().T)
    Mb_sym = 0.5 * (Mb + Mb.conj().T)

    w2, V = geigh(Kb_sym, Mb_sym)
    w2 = np.real(w2)
    idx_sort = np.argsort(w2)
    w2_sorted = w2[idx_sort]
    V_sorted = V[:, idx_sort]

    omegas = np.sqrt(np.maximum(w2_sorted, 0.0))
    return omegas, w2_sorted, V_sorted, Mb_sym, herm_err_K, herm_err_M


def track_modes_mac(
    path_omegas: np.ndarray,
    path_eigenvectors: list[np.ndarray],
    path_Mbars: list[np.ndarray],
) -> np.ndarray:
    """Modal Assurance Criterion (MAC) continuation along path to track mode identities.
    path_omegas: (N_pts, N_modes)
    Returns: tracked_omegas (N_pts, N_modes)
    """
    n_pts, n_modes = path_omegas.shape
    tracked = np.zeros_like(path_omegas)
    tracked[0, :] = path_omegas[0, :]

    curr_V = path_eigenvectors[0]
    perm = np.arange(n_modes)

    for i in range(1, n_pts):
        next_V = path_eigenvectors[i]
        Mbar = path_Mbars[i]

        # MAC matrix between previous tracked modes and current candidate modes
        # MAC_mn = |v_m^H M w_n|^2 / ((v_m^H M v_m)(w_n^H M w_n))
        MAC = np.zeros((n_modes, n_modes), dtype=float)
        for m in range(n_modes):
            vm = curr_V[:, m]
            denom_m = np.real(vm.conj().T @ Mbar @ vm)
            for n in range(n_modes):
                wn = next_V[:, n]
                denom_n = np.real(wn.conj().T @ Mbar @ wn)
                num = np.abs(vm.conj().T @ Mbar @ wn) ** 2
                MAC[m, n] = num / (denom_m * denom_n) if (denom_m > 0 and denom_n > 0) else 0.0

        # Greedy best matching
        matched_next = -np.ones(n_modes, dtype=int)
        used_next = set()
        for _ in range(n_modes):
            # Find largest entry in MAC not yet used
            best_val = -1.0
            best_m, best_n = -1, -1
            for m in range(n_modes):
                if matched_next[m] != -1:
                    continue
                for n in range(n_modes):
                    if n in used_next:
                        continue
                    if MAC[m, n] > best_val:
                        best_val = MAC[m, n]
                        best_m, best_n = m, n
            if best_m != -1 and best_n != -1:
                matched_next[best_m] = best_n
                used_next.add(best_n)

        # Fallback if any unmatched
        for m in range(n_modes):
            if matched_next[m] == -1:
                for n in range(n_modes):
                    if n not in used_next:
                        matched_next[m] = n
                        used_next.add(n)
                        break

        tracked[i, :] = path_omegas[i, matched_next]
        curr_V = next_V[:, matched_next]

    return tracked


def build_path_k(N_seg: int = 40, L: float = 1.0) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """Build Γ–X–M–Γ path with N_seg per segment (3*N_seg + 1 points total).
    Returns:
        k_pts: array of shape (3*N_seg + 1, 2)
        s_norm: array of normalized path coordinate in [0, 2 + sqrt(2)]
        breakpoints: indices of Γ, X, M, Γ [0, N_seg, 2*N_seg, 3*N_seg]
    """
    k_Gamma = np.array([0.0, 0.0])
    k_X = np.array([np.pi / L, 0.0])
    k_M = np.array([np.pi / L, np.pi / L])

    pts = []
    s_vals = []

    # Leg 1: Gamma -> X
    for j in range(N_seg):
        frac = j / N_seg
        pts.append(k_Gamma + frac * (k_X - k_Gamma))
        s_vals.append(frac * 1.0)

    # Leg 2: X -> M
    for j in range(N_seg):
        frac = j / N_seg
        pts.append(k_X + frac * (k_M - k_X))
        s_vals.append(1.0 + frac * 1.0)

    # Leg 3: M -> Gamma (including final point)
    for j in range(N_seg + 1):
        frac = j / N_seg
        pts.append(k_M + frac * (k_Gamma - k_M))
        s_vals.append(2.0 + frac * np.sqrt(2.0))

    breakpoints = [0, N_seg, 2 * N_seg, 3 * N_seg]
    return np.array(pts), np.array(s_vals), breakpoints


def build_half_bz_grid(Nx: int = 41, Ny: int = 81, L: float = 1.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Uniform grid covering the half BZ [0, pi/L] x [-pi/L, pi/L]."""
    kx = np.linspace(0.0, np.pi / L, Nx)
    ky = np.linspace(-np.pi / L, np.pi / L, Ny)
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    k_grid = np.column_stack([KX.ravel(), KY.ravel()])
    return KX, KY, k_grid


def compute_gaps(
    path_bands: np.ndarray,
    grid_bands: np.ndarray,
    breakpoints: list[int],
    N_bands: int = 4,
) -> dict:
    """Compute band gaps across path, individual legs, and full 2D zone grid.
    path_bands: (N_path, N_modes)
    grid_bands: (N_grid, N_modes)
    breakpoints: [idx_G, idx_X, idx_M, idx_G_end]
    """
    gaps_info = []

    # Indices of individual legs
    iG, iX, iM, iG_end = breakpoints
    leg_GX = np.arange(iG, iX + 1)
    leg_XM = np.arange(iX, iM + 1)
    leg_MG = np.arange(iM, iG_end + 1)

    for n in range(N_bands - 1):
        # Upper branch n+1 vs lower branch n
        lower_path = path_bands[:, n]
        upper_path = path_bands[:, n + 1]

        lower_grid = grid_bands[:, n]
        upper_grid = grid_bands[:, n + 1]

        # Path gap
        max_lower_path = float(np.max(lower_path))
        min_upper_path = float(np.min(upper_path))
        delta_path = min_upper_path - max_lower_path

        # Leg directional gaps
        delta_GX = float(np.min(upper_path[leg_GX]) - np.max(lower_path[leg_GX]))
        delta_XM = float(np.min(upper_path[leg_XM]) - np.max(lower_path[leg_XM]))
        delta_MG = float(np.min(upper_path[leg_MG]) - np.max(lower_path[leg_MG]))

        # Complete gap over 2D BZ grid
        max_lower_grid = float(np.max(lower_grid))
        min_upper_grid = float(np.min(upper_grid))
        delta_complete = min_upper_grid - max_lower_grid

        # Mid-frequency and normalised width
        w_mid = 0.5 * (min_upper_grid + max_lower_grid) if (min_upper_grid + max_lower_grid) > 0 else 1.0
        norm_width = delta_complete / w_mid if w_mid > 0 else 0.0

        # Subset inequality check: delta_leg >= delta_path >= delta_complete
        ineq_holds = (
            (delta_GX >= delta_path - 1e-12)
            and (delta_XM >= delta_path - 1e-12)
            and (delta_MG >= delta_path - 1e-12)
            and (delta_path >= delta_complete - 1e-12)
        )

        gaps_info.append(
            {
                "band_pair": [n + 1, n + 2],
                "delta_GX": delta_GX,
                "delta_XM": delta_XM,
                "delta_MG": delta_MG,
                "delta_path": delta_path,
                "delta_complete": delta_complete,
                "omega_lower_max": max_lower_grid,
                "omega_upper_min": min_upper_grid,
                "omega_mid": w_mid,
                "norm_gap_width": norm_width,
                "inequality_holds": ineq_holds,
            }
        )

    return {"gaps": gaps_info}


def compute_group_velocity_2d(
    K: np.ndarray,
    M: np.ndarray,
    kx: float,
    ky: float,
    h: float = 1e-4,
    L: float = 1.0,
    branch: int = 0,
) -> tuple[np.ndarray, float, float]:
    """Compute group velocity v_g = grad_k omega by central differences at (kx, ky).
    Returns:
        vg: vector [vg_x, vg_y]
        v_phase: scalar phase velocity omega / |k|
        delta_deg: deviation angle between v_g and k in degrees
    """
    om_x_p, _, _, _, _, _ = solve_bloch(K, M, kx + h, ky, L, check_hermiticity=False)
    om_x_m, _, _, _, _, _ = solve_bloch(K, M, kx - h, ky, L, check_hermiticity=False)
    om_y_p, _, _, _, _, _ = solve_bloch(K, M, kx, ky + h, L, check_hermiticity=False)
    om_y_m, _, _, _, _, _ = solve_bloch(K, M, kx, ky - h, L, check_hermiticity=False)
    om_0, _, _, _, _, _ = solve_bloch(K, M, kx, ky, L, check_hermiticity=False)

    vg_x = (om_x_p[branch] - om_x_m[branch]) / (2.0 * h)
    vg_y = (om_y_p[branch] - om_y_m[branch]) / (2.0 * h)
    vg = np.array([vg_x, vg_y], dtype=float)

    kmag = np.hypot(kx, ky)
    v_phase = float(om_0[branch] / kmag) if kmag > 0 else 0.0

    # Deviation angle
    vg_mag = np.linalg.norm(vg)
    if kmag > 0 and vg_mag > 0:
        cos_delta = np.clip(np.dot(vg, [kx, ky]) / (vg_mag * kmag), -1.0, 1.0)
        delta_rad = np.arccos(cos_delta)
        delta_deg = np.rad2deg(delta_rad)
    else:
        delta_deg = 0.0

    return vg, v_phase, float(delta_deg)


# ==============================================================================
# Multi-Element Mesh Assembly & Case C (Phononic Crystal with Inclusion)
# ==============================================================================

def assemble_mesh_KM(
    Nx: int,
    Ny: int,
    Lx: float = 1.0,
    Ly: float = 1.0,
    mat_func: any = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Assemble global K and M matrices for an Nx x Ny BFS rectangular mesh.
    
    mat_func(x, y) must return (lam, mu, rho, L11, L22, L12, ell2) at Gauss quadrature points.
    Implements standard quadrature-level material indicator function for circular inclusions (TV18).
    """
    hx = Lx / Nx
    hy = Ly / Ny
    n_nodes = (Nx + 1) * (Ny + 1)
    n_dofs = n_nodes * 8

    K = np.zeros((n_dofs, n_dofs), dtype=float)
    M = np.zeros((n_dofs, n_dofs), dtype=float)
    nd = gauss4()

    def node_id(ix: int, iy: int) -> int:
        return iy * (Nx + 1) + ix

    for ey in range(Ny):
        for ex in range(Nx):
            elem_nodes = [
                node_id(ex, ey),
                node_id(ex + 1, ey),
                node_id(ex + 1, ey + 1),
                node_id(ex, ey + 1),
            ]
            x0 = ex * hx
            y0 = ey * hy

            for xi, wi in nd:
                for eta, wj in nd:
                    xv = (xi + 1.0) / 2.0 * hx
                    yv = (eta + 1.0) / 2.0 * hy
                    xg = x0 + xv
                    yg = y0 + yv
                    wjac = wi * wj * hx * hy / 4.0

                    lam, mu, rho, L11, L22, L12, ell2 = mat_func(xg, yg)
                    Cbar = np.array(
                        [[lam + 2.0 * mu, lam, 0.0], [lam, lam + 2.0 * mu, 0.0], [0.0, 0.0, 2.0 * mu]],
                        dtype=float,
                    )
                    G = np.diag([1.0, 1.0, 2.0]) @ Cbar
                    Lmat = np.array([[L11, L12], [L12, L22]], dtype=float)

                    Hx, dHx, d2Hx = hermite_num(xv, hx)
                    Hy, dHy, d2Hy = hermite_num(yv, hy)

                    Nv = np.zeros((4, 4), dtype=float)
                    Nx_ = np.zeros((4, 4), dtype=float)
                    Ny_ = np.zeros((4, 4), dtype=float)
                    Nxx = np.zeros((4, 4), dtype=float)
                    Nxy = np.zeros((4, 4), dtype=float)
                    Nyy = np.zeros((4, 4), dtype=float)

                    for ndi in range(4):
                        ax, ay = XEND[ndi], YEND[ndi]
                        for ty in range(4):
                            dx = 1 if ty in (1, 3) else 0
                            dy = 1 if ty in (2, 3) else 0
                            ix, iy = ax + dx, ay + dy
                            Nv[ndi, ty] = Hx[ix] * Hy[iy]
                            Nx_[ndi, ty] = dHx[ix] * Hy[iy]
                            Ny_[ndi, ty] = Hx[ix] * dHy[iy]
                            Nxx[ndi, ty] = d2Hx[ix] * Hy[iy]
                            Nxy[ndi, ty] = dHx[ix] * dHy[iy]
                            Nyy[ndi, ty] = Hx[ix] * d2Hy[iy]

                    Nmat = np.zeros((2, 32), dtype=float)
                    B = np.zeros((3, 32), dtype=float)
                    Bx = np.zeros((3, 32), dtype=float)
                    By = np.zeros((3, 32), dtype=float)
                    Nxmat = np.zeros((2, 32), dtype=float)
                    Nymat = np.zeros((2, 32), dtype=float)

                    for ndi in range(4):
                        for c in range(2):
                            for ty in range(4):
                                j = idx(ndi, c, ty)
                                Nmat[c, j] = Nv[ndi, ty]
                                Nxmat[c, j] = Nx_[ndi, ty]
                                Nymat[c, j] = Ny_[ndi, ty]
                                if c == 0:
                                    B[0, j] = Nx_[ndi, ty]
                                    B[2, j] = 0.5 * Ny_[ndi, ty]
                                    Bx[0, j] = Nxx[ndi, ty]
                                    Bx[2, j] = 0.5 * Nxy[ndi, ty]
                                    By[0, j] = Nxy[ndi, ty]
                                    By[2, j] = 0.5 * Nyy[ndi, ty]
                                else:
                                    B[1, j] = Ny_[ndi, ty]
                                    B[2, j] = 0.5 * Nx_[ndi, ty]
                                    Bx[1, j] = Nxy[ndi, ty]
                                    Bx[2, j] = 0.5 * Nxx[ndi, ty]
                                    By[1, j] = Nyy[ndi, ty]
                                    By[2, j] = 0.5 * Nxy[ndi, ty]

                    Ke = wjac * (
                        B.T @ G @ B
                        + 0.1
                        * (
                            Lmat[0, 0] * (Bx.T @ G @ Bx)
                            + Lmat[0, 1] * (Bx.T @ G @ By)
                            + Lmat[1, 0] * (By.T @ G @ Bx)
                            + Lmat[1, 1] * (By.T @ G @ By)
                        )
                    )
                    Me = wjac * rho * (Nmat.T @ Nmat + ell2 * (Nxmat.T @ Nxmat + Nymat.T @ Nymat))

                    edofs = []
                    for ndi in range(4):
                        gn = elem_nodes[ndi]
                        for c in range(2):
                            for ty in range(4):
                                edofs.append(gn * 8 + c * 4 + ty)
                    edofs = np.array(edofs)
                    K[np.ix_(edofs, edofs)] += Ke
                    M[np.ix_(edofs, edofs)] += Me

    return K, M


def build_mesh_bloch_T(
    Nx: int,
    Ny: int,
    kx: float,
    ky: float,
    Lx: float = 1.0,
    Ly: float = 1.0,
) -> np.ndarray:
    """Bloch transformation matrix T for an Nx x Ny mesh of BFS elements.
    Reduces global DOFs (8*(Nx+1)*(Ny+1)) to master DOFs (8*Nx*Ny).
    """
    n_nodes = (Nx + 1) * (Ny + 1)
    n_masters = Nx * Ny
    T = np.zeros((n_nodes * 8, n_masters * 8), dtype=complex)

    def master_id(ix: int, iy: int) -> int:
        return iy * Nx + ix

    def global_node_id(ix: int, iy: int) -> int:
        return iy * (Nx + 1) + ix

    mx = np.exp(1j * kx * Lx)
    my = np.exp(1j * ky * Ly)

    for iy in range(Ny + 1):
        for ix in range(Nx + 1):
            g_node = global_node_id(ix, iy)
            if ix < Nx and iy < Ny:
                m_node = master_id(ix, iy)
                phase = 1.0 + 0j
            elif ix == Nx and iy < Ny:
                m_node = master_id(0, iy)
                phase = mx
            elif ix < Nx and iy == Ny:
                m_node = master_id(ix, 0)
                phase = my
            else:
                m_node = master_id(0, 0)
                phase = mx * my
            for d in range(8):
                T[g_node * 8 + d, m_node * 8 + d] = phase

    return T


def solve_bloch_mesh(
    K: np.ndarray,
    M: np.ndarray,
    Nx: int,
    Ny: int,
    kx: float,
    ky: float,
    Lx: float = 1.0,
    Ly: float = 1.0,
    check_hermiticity: bool = True,
    tol_herm: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Solve the reduced Bloch eigenvalue problem on an Nx x Ny mesh."""
    T = build_mesh_bloch_T(Nx, Ny, kx, ky, Lx, Ly)
    Kb = T.conj().T @ K @ T
    Mb = T.conj().T @ M @ T

    if check_hermiticity:
        nrm_K = np.linalg.norm(Kb, "fro")
        nrm_M = np.linalg.norm(Mb, "fro")
        diff_K = np.linalg.norm(Kb - Kb.conj().T, "fro")
        diff_M = np.linalg.norm(Mb - Mb.conj().T, "fro")
        if nrm_K > 0:
            assert diff_K / nrm_K < tol_herm, f"Mesh Kbar non-Hermitian: rel error = {diff_K/nrm_K:.3e}"
        if nrm_M > 0:
            assert diff_M / nrm_M < tol_herm, f"Mesh Mbar non-Hermitian: rel error = {diff_M/nrm_M:.3e}"

    Kb_sym = 0.5 * (Kb + Kb.conj().T)
    Mb_sym = 0.5 * (Mb + Mb.conj().T)

    w2, V = geigh(Kb_sym, Mb_sym)
    w2 = np.real(w2)
    idx_sort = np.argsort(w2)
    w2_sorted = w2[idx_sort]
    V_sorted = V[:, idx_sort]
    omegas = np.sqrt(np.maximum(w2_sorted, 0.0))

    return omegas, w2_sorted, V_sorted


def mat_caseC(
    x: float,
    y: float,
    r0: float = 0.3,
    Lx: float = 1.0,
    Ly: float = 1.0,
    inclusion_type: str = "ybco_epoxy",
) -> tuple[float, float, float, float, float, float, float]:
    """Material parameters for Case C: circular inclusion in matrix.
    
    Standard TV6 / TV14 / TV18 choices:
      - Geometry: circular inclusion radius r0 in unit cell [0, Lx] x [0, Ly].
      - Standard material contrast (Zhan & Wei 2010):
          Matrix (Epoxy):   rho_m = 1.0,   mu_m = 1.0,  lam_m = 3.088, ell2 = 0.01, L11 = L22 = 0.01
          Inclusion (YBCO): rho_i = 5.546, mu_i = 25.0, lam_i = 64.19, ell2 = 0.04, L11 = L22 = 0.04
    """
    xc, yc = 0.5 * Lx, 0.5 * Ly
    r = np.sqrt((x - xc) ** 2 + (y - yc) ** 2)
    if r <= r0:
        # Inclusion properties
        return 64.19, 25.0, 5.546, 0.04, 0.04, 0.0, 0.04
    else:
        # Matrix properties
        return 3.088, 1.0, 1.0, 0.01, 0.01, 0.0, 0.01

