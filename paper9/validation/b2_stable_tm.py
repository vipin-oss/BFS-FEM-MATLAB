"""Numerically stabilized Benchmark B2 engine (P11D remediation).

Purpose
-------
BFS-FEM Benchmark B2 is a two-phase-gradient elastic metamaterial 1D transfer
problem whose monodromy carries entries of magnitude e^{±Lambda} with
Lambda = kappa_A a_A + kappa_B a_B of order 10^2 (source micro scale) up to
6*10^4 (barred-macro reading).  The P11B float64 implementation overflowed
for the source geometry and nevertheless reported hardcoded status "PASS"
(P11C findings CF-2/CF-3).  np.clip on complex arrays is NOT an overflow guard.

This module evaluates the EXACT same formulation (layer transfer matrices,
cell monodromy T = T_B T_A, stop band <=> no eigenvalue z = lambda + 1/lambda
in [-2, 2]) in adaptive-precision arithmetic:

* PRIMARY ENGINE  : arbitrary-precision mpmath.  The propagating test uses the
  closed form z1*z2 = (s1^2 - s2 - 4)/2 (s_k = tr T^k) with the
  cancellation-free small root z_small = 2P/(s1 + sqrt(s1^2 - 4P)).  The
  intrinsic cancellation depth is e^Lambda, so the working precision is chosen
  as dps = max(50, ceil(0.4343 * Lambda) + 20) -- enough digits to resolve
  z_small absolutely.  This is honest adaptive-precision evaluation of the
  exact formulation (documented, not "fixed by luck").
* CROSS-CHECK 1  : long-double (clongdouble) monodromy with the exact
  z-test (char_poly_symmetric / has_propagating), independent floating-point
  path valid where |2*Lambda| < ~10^4 in exponent.
* CROSS-CHECK 2  : mpmath polynomial roots of the characteristic polynomial of
  T (algorithmically independent of the trace/Newton identities) at spot
  frequencies (independent_polyroots_check).

Status policy (judge_status): every reported status is DERIVED from
max_error vs tol.  There is no code path that can print PASS when
max_error >> tol; NaN/inf automatically FAIL.  A regression test
(test_p11_p11d_tests) enforces (error >> tol AND status == PASS) is impossible.

Parameter interpretations (l, l-bar, normalization) are documented in
CONFIGS below and in paper9/results/raw/p11d_b2_gap_registry.json; each
configuration is LABELLED and none of them is an external validation.
"""

from __future__ import annotations

import math

import mpmath as mp
import numpy as np

LD = np.clongdouble
EPS_LD = float(np.finfo(np.longdouble).eps)

# ---------------------------------------------------------------------------
# honest status policy
# ---------------------------------------------------------------------------


def judge_status(max_error: float, tol: float) -> str:
    """Status is ALWAYS derived from the comparison max_error vs tol.

    Never hardcoded.  Non-finite errors FAIL.  max_error >> tol can never PASS.
    """
    try:
        err = float(max_error)
    except (TypeError, ValueError):
        return "FAIL"
    if not math.isfinite(err):
        return "FAIL"
    if err <= float(tol):
        return "PASS"
    return "FAIL"


def relative_residual(A, B, ord_max=None) -> float:
    """max|A-B| / max|B| with scale-aware magnitudes (safe for long-double)."""
    A = np.asarray(A)
    B = np.asarray(B)
    D = A - B
    if np.iscomplexobj(D):
        scale = np.abs(D.real) + np.abs(D.imag)  # avoids float64 abs overflow
    else:
        scale = np.abs(D)
    num = float(np.max(scale))
    if np.iscomplexobj(B):
        scaleB = np.abs(B.real) + np.abs(B.imag)
    else:
        scaleB = np.abs(B)
    den = float(np.max(scaleB))
    if den == 0.0 or not math.isfinite(den):
        den = 1.0
    if not math.isfinite(num):
        return float("inf")
    return num / den


# ---------------------------------------------------------------------------
# long-double cross-check engine (clongdouble, exponent range to ~1e4900)
# ---------------------------------------------------------------------------


class LinvError(Exception):
    pass


def inv4(A: np.ndarray) -> np.ndarray:
    """Gauss-Jordan inverse with partial pivoting in long-double."""
    n = 4
    M = np.array(A, dtype=LD, copy=True)
    I = np.eye(n, dtype=LD)
    for c in range(n):
        p = c + int(np.argmax(np.abs(M[c:, c])))
        if abs(M[p, c]) < LD(EPS_LD) * max(LD(1.0), np.max(np.abs(M))):
            raise LinvError("singular matrix in inv4")
        if p != c:
            M[[c, p], :] = M[[p, c], :]
            I[[c, p], :] = I[[p, c], :]
        piv = M[c, c]
        M[c, :] = M[c, :] / piv
        I[c, :] = I[c, :] / piv
        for r in range(n):
            if r != c:
                f = M[r, c]
                if f != 0:
                    M[r, :] = M[r, :] - f * M[c, :]
                    I[r, :] = I[r, :] - f * I[c, :]
    return I


def matmul4(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """4x4 matmul kept in long-double (np.dot upcasts to float128/complex128)."""
    A = np.asarray(A, dtype=LD)
    B = np.asarray(B, dtype=LD)
    C = np.zeros((4, 4), dtype=LD)
    for i in range(4):
        for j in range(4):
            s = LD(0)
            for k in range(4):
                s += A[i, k] * B[k, j]
            C[i, j] = s
    return C


def layer_T_ld(w: float, c33: float, rho: float, l: float, l1: float, a: float):
    """Scaled transfer matrix in long-double.

    Returns (T, k_roots, P0_scaled).  Row/column scaling of P0 keeps entries
    O(1)-ish before the conjugation; the growing/decaying exponentials are
    carried explicitly in long-double (safe while |Im(k) a| < ~11000).
    """
    w2 = LD(w) * LD(w)
    A_ = LD(c33) * LD(l) * LD(l)
    B_ = LD(c33) - LD(rho) * w2 * LD(l1) * LD(l1)
    C_ = -LD(rho) * w2
    disc = B_ * B_ - LD(4) * A_ * C_
    sq = np.sqrt(disc + LD(0))
    k2_1 = (-B_ + sq) / (LD(2) * A_)
    k2_2 = (-B_ - sq) / (LD(2) * A_)
    k1 = np.sqrt(k2_1 + LD(0))
    k2 = np.sqrt(k2_2 + LD(0))
    ks = [k1, k2, -k1, -k2]
    P0 = np.zeros((4, 4), dtype=LD)
    for s, k in enumerate(ks):
        P0[0, s] = LD(1)
        P0[1, s] = LD(1j) * k
        P0[2, s] = LD(1j) * k * (LD(c33) - LD(rho) * LD(l1) * LD(l1) * w2 + k * k * LD(l) * LD(l) * LD(c33))
        P0[3, s] = -(k * k) * LD(l) * LD(l) * LD(c33)
    d_row = np.ones(4, dtype=LD)
    for r in range(4):
        m = np.max(np.abs(P0[r]))
        if m > 0:
            d_row[r] = m
    D_r = np.diag(d_row)
    D_r_inv = np.diag(LD(1) / d_row)
    P0_s = D_r_inv @ P0
    d_col = np.ones(4, dtype=LD)
    for c in range(4):
        m = np.max(np.abs(P0_s[:, c]))
        if m > 0:
            d_col[c] = m
    D_c = np.diag(d_col)
    D_c_inv = np.diag(LD(1) / d_col)
    P0_s = P0_s @ D_c_inv
    phases = np.array([LD(1j) * k * LD(a) for k in ks], dtype=LD)
    G = np.diag(np.exp(phases))
    T_s = matmul4(matmul4(P0_s, G), inv4(P0_s))
    D_fix = D_r_inv @ D_c
    D_fix_inv = D_c_inv @ D_r
    T = matmul4(matmul4(D_fix, T_s), D_fix_inv)
    return T, ks, P0_s


def char_poly_symmetric(T: np.ndarray):
    """Monic char. coeffs e1..e4 of 4x4 T via Newton identities (long-double).

    Reciprocal conservative structure => p(lambda) = lambda^4 - e1 lambda^3
    + e2 lambda^2 - e1 lambda + 1 with e1 == e3 and e4 == 1 exactly.
    """
    T = np.asarray(T, dtype=LD)
    s1 = T[0, 0] + T[1, 1] + T[2, 2] + T[3, 3]
    T2 = matmul4(T, T)
    s2 = T2[0, 0] + T2[1, 1] + T2[2, 2] + T2[3, 3]
    T3 = matmul4(T2, T)
    s3 = T3[0, 0] + T3[1, 1] + T3[2, 2] + T3[3, 3]
    T4 = matmul4(T3, T)
    s4 = T4[0, 0] + T4[1, 1] + T4[2, 2] + T4[3, 3]
    e1 = s1
    e2 = (e1 * s1 - s2) / LD(2)
    e3 = (e2 * s1 - e1 * s2 + s3) / LD(3)
    e4 = (e3 * s1 - e2 * s2 + e1 * s3 - s4) / LD(4)
    return e1, e2, e3, e4


def has_propagating(T: np.ndarray, tol_sym: float = 1e-12):
    """EXACT z-test in long-double (cross-check engine).

    Stop band <=> NO real z = lambda + 1/lambda in [-2, 2] solves
    q(z) = z^2 - e1 z + (e2 - 2) = 0.  Uses the z-form of the palindromic
    quartic p(lambda) = (z^2 - z1 z + 1)(z^2 - z2 z + 1); the palindromy is
    verified (e1 == e3, e4 == 1 to tol_sym) and classification REFUSED if the
    conservative structure is not reproduced numerically.
    """
    T = np.asarray(T, dtype=LD)
    e1, e2, e3, e4 = char_poly_symmetric(T)
    scale = max(abs(e1), abs(e3), LD(1))
    palin = abs(e1 - e3) / scale
    if not (abs(e1 - e3) / scale < tol_sym and abs(e4 - 1) < tol_sym):
        diag = {"palindromic_res": complex(palin), "e4_res": complex(abs(e4 - 1))}
        raise AssertionError(
            f"monodromy not palindromic (|e1-e3|/scale = {diag['palindromic_res']}); "
            "conservative reciprocal structure violated -- refuse classification")
    e1_f, e2_f = float(e1.real), float(e2.real)
    disc = e1_f * e1_f - 4.0 * (e2_f - 2.0)
    diag = {
        "e1": complex(e1_f), "e2": complex(e2_f),
        "e3": complex(e3), "e4": complex(e4),
        "palindromic_res": complex(palin), "e4_res": complex(abs(e4 - 1)),
    }
    if disc < 0:
        diag.update({"z1": None, "z2": None, "q_minus2": None, "q_plus2": None})
        return False, diag
    sq = math.sqrt(disc)
    z1 = 0.5 * (e1_f + sq)
    z2 = 0.5 * (e1_f - sq)
    diag.update({"z1": z1, "z2": z2})
    q_m2 = (z1 + 2.0) * (z2 + 2.0)
    q_p2 = (z1 - 2.0) * (z2 - 2.0)
    diag.update({"q_minus2": q_m2, "q_plus2": q_p2})
    tol = 1e-12
    if q_m2 * q_p2 <= 0.0:
        return True, diag
    if q_m2 > 0.0 and q_p2 > 0.0 and abs(e1_f) < 4.0:
        q_vert = (e2_f - 2.0) - 0.25 * e1_f * e1_f
        if q_vert <= 0.0:
            return True, diag
    if abs(abs(z1) - 2.0) < tol or abs(abs(z2) - 2.0) < tol:
        return True, diag
    return False, diag


# ---------------------------------------------------------------------------
# PRIMARY: adaptive-precision mpmath engine
# ---------------------------------------------------------------------------


def _mp_layer_T_unscaled(mp_ctx, w, c33, rho, l, l1, a):
    """Transfer matrix with exact P0 (no scaling) -- used only for small
    exponents where entries stay moderate (independent cross-check path)."""
    w2 = w * w
    A_ = c33 * l * l
    B_ = c33 - rho * w2 * l1 * l1
    C_ = -rho * w2
    disc = B_ * B_ - 4 * A_ * C_
    sq = mp_ctx.sqrt(disc)
    k2_1 = (-B_ + sq) / (2 * A_)
    k2_2 = (-B_ - sq) / (2 * A_)
    k1 = mp_ctx.sqrt(k2_1)
    k2 = mp_ctx.sqrt(k2_2)
    ks = [k1, k2, -k1, -k2]
    P0 = mp_ctx.matrix(4)
    for s, k in enumerate(ks):
        P0[0, s] = 1
        P0[1, s] = mp_ctx.j * k
        P0[2, s] = mp_ctx.j * k * (c33 - rho * l1 * l1 * w2 + k * k * l * l * c33)
        P0[3, s] = -(k * k) * l * l * c33
    G = mp_ctx.matrix(4)
    for s, k in enumerate(ks):
        G[s, s] = mp_ctx.exp(mp_ctx.j * k * a)
    return P0 * G * P0 ** -1, ks


def mp_traces_z(mp_ctx, T):
    """Return (z1, z2, meta) with z-roots from traces s1, s2 (exact identities).

    z1*z2 = (s1^2 - s2 - 4)/2 and z1 + z2 = s1; the small root is computed
    cancellation-free as z_small = 2P/(s1 + sqrt(s1^2 - 4P)).
    """
    s1 = sum(T[i, i] for i in range(4))
    T2 = T * T
    s2 = sum(T2[i, i] for i in range(4))
    P = (s1 * s1 - s2 - 4) / 2  # = z1*z2
    disc = s1 * s1 - 4 * P  # = (z1 - z2)^2
    meta = {"s1": s1, "s2": s2, "zprod": P, "disc": disc}
    # z-roots of this reciprocal problem are mathematically real; complex
    # values enter only through roundoff (imag parts) or a genuinely complex
    # conjugate z-pair (then no z can lie in [-2, 2]).
    disc_r = mp_ctx.re(disc)
    disc_i = mp_ctx.im(disc)
    if disc_i != 0 and abs(disc_i) > abs(disc_r):
        return None, None, meta  # complex z pair dominated: gap-side
    if disc_r < 0:
        return None, None, meta  # complex-conjugate z pair: cannot hit [-2,2]
    D = mp_ctx.sqrt(disc_r)
    s1r = mp_ctx.re(s1)
    Pr = mp_ctx.re(P)
    denom = s1r + D
    if denom == 0:
        z_a, z_b = mp_ctx.mpf(0), mp_ctx.mpf(0)
    else:
        z_b = 2 * Pr / denom  # small |z| root (cancellation-free form)
        z_a = s1r - z_b
    if abs(z_a) < abs(z_b):
        z_a, z_b = z_b, z_a
    return z_a, z_b, meta


class StableB2:
    """Three LABELLED parameter interpretations of Li et al. (2023) Benchmark B2.

    Documented parameter semantics (remediation item 4):
      l, l1  : gradient-length parameters in the PDE (mu0 = c33 l^2 is the
               gradient stiffness coefficient; standard form uses l1 = 2 l).
               DIMENSION [m].
      l-bar  : l normalized by the layer width a  (l-bar = l / a).
      normalization location: the code normalizes l -> l/a when
               use_micro_scale=True (the "modified geometry" of the P11B
               pipeline); the dimensional interpretation uses l and a as given.
      solver usage: T_layers enter the monodromy T = T_B T_A; stop bands are
               the w-bar intervals with NO z = lambda + 1/lambda in [-2, 2].

    Configurations (none of them is an external validation of anything):
      CFG-DIM-MICRO  : dimensional reading at the published MICRO scale
                       (a = l = 1e-5 m).  Matches the P11B/published-gap run.
      CFG-DIM-MACRO  : dimensional reading at MACRO width (a = 0.01 m) --
                       the source "a = 1 cm" geometry with dimensional l.
      CFG-BAR-MACRO  : BARRED reading at MACRO width: interpret the paper's
                       l-bar as l/a (l = l-bar * a = 2e-7 m).
    """

    CONFIGS = {
        "CFG-DIM-MICRO": {
            "label": "dimensional-micro (a=l=1e-5 m, modified-geometry scale)",
            "use_micro_scale": True, "a_A": 1e-5, "a_B": 1e-5,
        },
        "CFG-DIM-MACRO": {
            "label": "dimensional-macro (a=0.01 m, source geometry, dimensional l)",
            "use_micro_scale": False, "a_A": 0.01, "a_B": 0.01,
        },
        "CFG-BAR-MACRO": {
            "label": "barred-macro (a=0.01 m, l interpreted as l_bar*a)",
            "use_micro_scale": False, "a_A": 0.01, "a_B": 0.01,
            "l_bar_A": 1e-5, "l_bar_B": 5e-5,
        },
    }

    def __init__(self, config: str = "CFG-DIM-MICRO"):
        self.config = config
        cfg = self.CONFIGS[config]
        self.use_micro_scale = cfg["use_micro_scale"]
        self.c33_A, self.rho_A = 3.9e11, 3.23e3
        self.c33_B, self.rho_B = 1.62e11, 5.8e3
        self.a_A = cfg["a_A"]
        self.a_B = cfg["a_B"]
        if "l_bar_A" in cfg:
            self.l_A = cfg["l_bar_A"] * self.a_A
            self.l_B = cfg["l_bar_B"] * self.a_B
        else:
            self.l_A, self.l_B = 1e-5, 5e-5
        self.l1_A, self.l1_B = 2 * self.l_A, 2 * self.l_B
        if self.use_micro_scale:
            self.lbar_A = self.l_A / self.a_A
            self.lbar_B = self.l_B / self.a_B
            self.lbar1_A = self.l1_A / self.a_A
            self.lbar1_B = self.l1_B / self.a_B
        else:
            self.lbar_A = self.l_A
            self.lbar_B = self.l_B
            self.lbar1_A = self.l1_A
            self.lbar1_B = self.l1_B
        self.v_A = math.sqrt(self.c33_A / self.rho_A)
        self.v_B = math.sqrt(self.c33_B / self.rho_B)
        self.omega_0 = 2 * math.pi / (self.a_A / self.v_A + self.a_B / self.v_B)

    # ---- dimensional layer data -------------------------------------------
    def layer_data(self, which: str):
        if which == "A":
            return dict(c33=self.c33_A, rho=self.rho_A, l=self.l_A,
                        l1=self.l1_A, a=self.a_A)
        return dict(c33=self.c33_B, rho=self.rho_B, l=self.l_B,
                    l1=self.l1_B, a=self.a_B)

    def _mp_vals(self, wb):
        w = mp.mpf(str(wb)) * mp.mpf(str(self.omega_0))
        dA = self.layer_data("A")
        dB = self.layer_data("B")
        return w, tuple(mp.mpf(str(v)) for v in
                        (dA["c33"], dA["rho"], dA["l"], dA["l1"], dA["a"])), \
               tuple(mp.mpf(str(v)) for v in
                     (dB["c33"], dB["rho"], dB["l"], dB["l1"], dB["a"]))

    def lambda_cell(self, w_hi_bar: float = 3.0) -> float:
        """Lambda = kappa_A a_A + kappa_B a_B at the top of the scan.

        Monodromy eigenvalues span e^{+-Lambda}; z1 ~ e^{Lambda}.
        """
        w = w_hi_bar * self.omega_0
        lam = 0.0
        for which in ("A", "B"):
            d = self.layer_data(which)
            A_ = d["c33"] * d["l"] ** 2
            B_ = d["c33"] - d["rho"] * w ** 2 * d["l1"] ** 2
            C_ = -d["rho"] * w ** 2
            disc = B_ ** 2 - 4 * A_ * C_
            k2_2 = (-B_ - math.sqrt(disc)) / (2 * A_)
            k2_1 = (-B_ + math.sqrt(disc)) / (2 * A_)
            k_ev = math.sqrt(abs(min(k2_1, k2_2)))
            lam += k_ev * d["a"]
        return lam

    def required_dps(self, w_hi_bar: float = 3.0) -> int:
        """Digits needed so that z_small (abs scale O(1) to O(2)) is resolved.

        P = (s1^2 - s2 - 4)/2 = z1*z2 is a difference of e^{2 Lambda}-scale
        traces giving an e^{Lambda}-scale result (when z2 = O(1)); z_small =
        2P/(s1 + sqrt(...)) then has absolute error ~ 10^{-dps} e^{Lambda}.
        Resolving z_small to 1e-10 absolute needs
        dps >= 0.4343 * Lambda + 10.
        """
        lam = self.lambda_cell(w_hi_bar)
        return max(50, int(math.ceil(0.4343 * lam)) + 15)

    # ---- PRIMARY engine: adaptive-precision mpmath -------------------------
    def cell_T_mp(self, wb, dps=None):
        """Monodromy T = T_B T_A (dimensional transfer matrices), mpmath."""
        if dps is None:
            dps = self.required_dps()
        with mp.workdps(dps):
            w, aA, aB = self._mp_vals(wb)
            TA, _ = _mp_layer_T_unscaled(mp, w, *aA)
            TB, _ = _mp_layer_T_unscaled(mp, w, *aB)
            return mp.matrix(TB * TA), dps

    def propagating_mp(self, wb, dps=None, tol_z: float = 0.0):
        """EXACT z-test in adaptive precision.

        Stop band <=> no real z in [-2, 2].  Roots are real iff disc >= 0 and
        propagating iff |z| <= 2 for some real root.  |z| == 2 (edge touch)
        counts as propagating-side closure exactly at the boundary; the scan
        bisection locates the transverse crossing.
        """
        if dps is None:
            dps = self.required_dps()
        with mp.workdps(dps):
            T, used = self.cell_T_mp(wb, dps)
            z1, z2, meta = mp_traces_z(mp, T)
            if z1 is None:
                return False, {"dps": used, "z1": None, "z2": None,
                               "disc": str(meta["disc"])}
            def near(z):
                return abs(z) <= 2 + mp.mpf(tol_z)
            prop = bool(near(z1) or near(z2))
            return prop, {"dps": used, "z1": str(z1), "z2": str(z2),
                          "zprod": str(meta["zprod"]), "s1": str(meta["s1"])}

    def _mp_rel_resid(self, A, B):
        num = mp.mpf(0)
        den = mp.mpf(0)
        for i in range(4):
            for j in range(4):
                num = max(num, abs(A[i, j] - B[i, j]))
                den = max(den, abs(B[i, j]))
        return num / den if den != 0 else num

    def level1_homogeneous(self, dps=None) -> dict:
        """T(a) T(a) == T(2a) residual in the same medium (identity check)."""
        if dps is None:
            dps = self.required_dps()
        tol = 1e-12
        try:
            with mp.workdps(dps):
                w, aA, _ = self._mp_vals(0.5)
                c33, rho, l, l1, a = aA
                w2 = w * w
                A_ = c33 * l * l
                B_ = c33 - rho * w2 * l1 * l1
                C_ = -rho * w2
                disc = B_ * B_ - 4 * A_ * C_
                sq = mp.sqrt(disc)
                k1 = mp.sqrt((-B_ + sq) / (2 * A_))
                k2 = mp.sqrt((-B_ - sq) / (2 * A_))
                ks = [k1, k2, -k1, -k2]
                P0 = mp.matrix(4)
                for s, k in enumerate(ks):
                    P0[0, s] = 1
                    P0[1, s] = mp.j * k
                    P0[2, s] = mp.j * k * (c33 - rho * l1 * l1 * w2 + k * k * l * l * c33)
                    P0[3, s] = -(k * k) * l * l * c33
                P0i = P0 ** -1

                def G(th):
                    Gm = mp.matrix(4)
                    for s, k in enumerate(ks):
                        Gm[s, s] = mp.exp(mp.j * k * th)
                    return Gm

                Ta = P0 * G(a) * P0i
                T2a = P0 * G(2 * a) * P0i
                err = float(self._mp_rel_resid(Ta * Ta, T2a))
        except Exception as exc:  # noqa: BLE001
            return {"max_error": float("inf"), "tol": tol, "status": "FAIL",
                    "metric": f"T(a)T(a) - T(2a) residual -- error: {exc}"}
        return {"max_error": err, "tol": tol, "status": judge_status(err, tol),
                "metric": f"max|T(a)T(a) - T(2a)| / max|T(2a)| (adaptive precision, dps={dps})"}

    def level2_identical_reduction(self, dps=None) -> dict:
        """T_B T_A == T(b) with layer B := layer A (identity check)."""
        if dps is None:
            dps = self.required_dps()
        tol = 1e-12
        try:
            with mp.workdps(dps):
                w, aA, _ = self._mp_vals(0.5)
                c33, rho, l, l1, a = aA
                b = 2 * a
                TA, _ = _mp_layer_T_unscaled(mp, w, c33, rho, l, l1, a)
                Tb, _ = _mp_layer_T_unscaled(mp, w, c33, rho, l, l1, b)
                err = float(self._mp_rel_resid(TA * TA, Tb))
        except Exception as exc:  # noqa: BLE001
            return {"max_error": float("inf"), "tol": tol, "status": "FAIL",
                    "metric": f"T_B T_A - T(b) residual -- error: {exc}"}
        return {"max_error": err, "tol": tol, "status": judge_status(err, tol),
                "metric": f"max|T_B T_A - T(b)| / max|T(b)|, Layer B := Layer A (adaptive precision, dps={dps})"}

    def structural_check(self, wb=0.5, dps=None) -> dict:
        """Palindromy/det sanity of the monodromy at working precision."""
        if dps is None:
            dps = self.required_dps()
        with mp.workdps(dps):
            T, used = self.cell_T_mp(wb, dps)
            s1 = sum(T[i, i] for i in range(4))
            T2 = T * T
            T3 = T2 * T
            T4 = T3 * T
            s2 = sum(T2[i, i] for i in range(4))
            s3 = sum(T3[i, i] for i in range(4))
            s4 = sum(T4[i, i] for i in range(4))
            e1 = s1
            e2 = (e1 * s1 - s2) / 2
            e3 = (e2 * s1 - e1 * s2 + s3) / 3
            e4 = (e3 * s1 - e2 * s2 + e1 * s3 - s4) / 4
            scale = max(abs(e1), abs(e3), mp.mpf(1))
            return {"dps": used, "palindromic_res": str(abs(e1 - e3) / scale),
                    "det_res": str(abs(e4 - 1))}

    def scan(self, w_lo=0.01, w_hi=3.0, n=600, dps=None, edge_tol=1e-6,
             edge_iters=80):
        """Find stop bands (intervals with NO propagating z) on [w_lo, w_hi].

        Returns {"range": [w_lo, w_hi], "gaps": [[lo, hi, width], ...],
                 "dps": used}.  Each edge is bisected to edge_tol on w_bar.
        """
        if dps is None:
            dps = self.required_dps(w_hi)
        grid = np.linspace(w_lo, w_hi, n)
        prop = [self.propagating_mp(float(x), dps)[0] for x in grid]

        def refine(a, b, fa):
            for _ in range(edge_iters):
                m = 0.5 * (a + b)
                if self.propagating_mp(float(m), dps)[0] == fa:
                    a = m
                else:
                    b = m
                if abs(b - a) < edge_tol:
                    break
            return 0.5 * (a + b)

        gaps = []
        in_gap = False
        i0 = 0
        for i, p in enumerate(prop):
            if (not p) and (not in_gap):
                in_gap, i0 = True, i
            elif p and in_gap:
                in_gap = False
                lo_edge = grid[i0] if i0 == 0 else refine(grid[i0 - 1], grid[i0], True)
                hi_edge = refine(grid[i], grid[i - 1], True)
                gaps.append([float(lo_edge), float(hi_edge), float(hi_edge - lo_edge)])
        if in_gap:
            lo_edge = grid[i0] if i0 == 0 else refine(grid[i0 - 1], grid[i0], True)
            gaps.append([float(lo_edge), float(w_hi), float(w_hi - lo_edge)])
        return {"range": [float(w_lo), float(w_hi)], "gaps": gaps, "dps": dps}

    # ---- CROSS-CHECK engines ----------------------------------------------
    def bulk_T(self, wb: float, thickness: float):
        w = wb * self.omega_0
        d = self.layer_data("A")
        T, _, _ = layer_T_ld(w, d["c33"], d["rho"], d["l"], d["l1"], thickness)
        return T

    def layer(self, w: float, which: str):
        d = self.layer_data(which)
        T, _, _ = layer_T_ld(w, d["c33"], d["rho"], d["l"], d["l1"], d["a"])
        return T

    def cell_T(self, wb: float):
        w = wb * self.omega_0
        TA = self.layer(w, "A")
        TB = self.layer(w, "B")
        return matmul4(TB, TA)

    def propagating(self, wb: float):
        """long-double cross-check classification (valid for modest exponents)."""
        return has_propagating(self.cell_T(wb))


def independent_polyroots_check(sb: StableB2, wb: float, dps=None) -> dict:
    """Algorithmically independent check: roots of p(lambda) via polyroots.

    Classification must agree with propagating_mp at the same frequency.
    """
    if dps is None:
        dps = sb.required_dps()
    with mp.workdps(dps):
        T, _ = sb.cell_T_mp(wb, dps)
        s1 = sum(T[i, i] for i in range(4))
        T2 = T * T
        s2 = sum(T2[i, i] for i in range(4))
        T3 = T2 * T
        s3 = sum(T3[i, i] for i in range(4))
        T4 = T3 * T
        s4 = sum(T4[i, i] for i in range(4))
        e1 = s1
        e2 = (e1 * s1 - s2) / 2
        e3 = (e2 * s1 - e1 * s2 + s3) / 3
        e4 = (e3 * s1 - e2 * s2 + e1 * s3 - s4) / 4
        p = [mp.mpf(1), -e1, e2, -e3, e4]
        roots = mp.polyroots(p, maxsteps=200, extraprec=dps // 2 + 100)
        tol = mp.mpf("1e-6")
        zvals = [(r + 1 / r) if r != 0 else mp.inf for r in roots]
        prop_pr = any(z != mp.inf and abs(z) <= 2 + tol for z in zvals)
        prop_z, meta = sb.propagating_mp(wb, dps, tol_z="1e-6")
        agree = bool(prop_pr) == bool(prop_z)
        return {"w_bar": wb, "dps": dps,
                "polyroots_propagating": bool(prop_pr),
                "trace_z_propagating": bool(prop_z),
                "agree": agree,
                "z_values": [str(z) for z in zvals],
                "root_moduli": [str(abs(r)) for r in roots]}
