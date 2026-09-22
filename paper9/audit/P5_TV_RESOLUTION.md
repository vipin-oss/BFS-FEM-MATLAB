# P5 TV Register Resolution and Traceability Record

**Date:** 2026-09-22  
**Base Commit:** `15814972c812c70e0bb93da7635f75b831178520`  
**Phase:** Phase 5 (Main Scientific Production)

---

## 1. Resolved TV Items in Phase 5

### TV4 — k-points per IBZ segment and 2D zone-grid resolution
- **Status:** **LOCKED [S]**
- **Evidence / Justification:** 
  - Path discretisation: $N_{\mathrm{seg}} = 40$ segments per leg along $\Gamma \to X \to M \to \Gamma$ yielding $3 N_{\mathrm{seg}} + 1 = 121$ path nodes with exact breakpoints at $s \in \{0, 1, 2, 2+\sqrt{2}\}$.
  - 2D zone grid: $N_{kx} = 41, N_{ky} = 81$ uniform grid covering the half BZ $[0, \pi/L] \times [-\pi/L, \pi/L]$ ($3321$ nodes). Inversion symmetry $\omega(-\bm k) = \omega(\bm k)$ ensures complete BZ coverage for generic $\theta$.
  - Both path and grid resolutions provide spectral variation resolution far above the locked P4B resolution floor $\varepsilon_\Delta \approx 4.63 \times 10^{-11}$.

### TV6 — Case-H production parameters
- **Status:** **LOCKED [S] for Case H; Case C remains OPEN**
- **Evidence / Justification:**
  - Case H uses the frozen and validated parameter set from P4A/P4B [S-P4A]: $L_{\mathrm{cell}} = 1.0\,\mathrm{m}$, $\lambda = 1.0\,\mathrm{Pa}$, $\mu = 1.0\,\mathrm{Pa}$, $\rho = 1.0\,\mathrm{kg/m^3}$ (corresponding to $\lambda/\mu = 1.0$, $\nu = 0.25$ plane strain), $\ell^2 = 0.04\,\mathrm{m^2}$ ($\ell = 0.20\,\mathrm{m}$, $\bar\ell = 0.20$), $l_{\mathrm{iso}} = 0.20\,\mathrm{m}$ ($\bar l = 0.20$).
  - Anisotropic semi-axes follow the area-preserving (volume-equivalent) scaling $l_1 = l_{\mathrm{iso}}\sqrt{\mathrm{AR}}, l_2 = l_{\mathrm{iso}}/\sqrt{\mathrm{AR}}$, maintaining $\det(A^{\mathsf T}\!A)_{\mathrm{rot}} = l_{\mathrm{iso}}^4 = \mathrm{const}$. Baseline P4A test values $l_1 = 0.30, l_2 = 0.10$ for $\mathrm{AR} = 3$ are preserved.
  - Case C inclusion parameters (inclusion radius $R_{\mathrm{incl}}$, impedance contrast) are not invented and remain OPEN awaiting empirical/published anchor evidence.

### TV7 — Reported bands count N and spurious-mode filter
- **Status:** **LOCKED [S]**
- **Evidence / Justification:**
  - Lowest $N = 4$ physical branches reported (transverse acoustic $\omega_T$, longitudinal acoustic $\omega_L$, and the two lowest optical/gradient branches).
  - Spurious-mode filter: verifies Hermiticity $\|\bar{\bm K} - \bar{\bm K}^{\mathsf H}\|/\|\bar{\bm K}\| < 10^{-12}$, verifies real non-negative eigenvalues $\omega^2 \ge -10^{-12}$, filters high-frequency unphysical discretization modes, and maintains mode identity across branch crossings using Modal Assurance Criterion (MAC) continuation.

### TV15 — Non-dimensional phase velocity definition
- **Status:** **LOCKED [A]**
- **Evidence / Justification:**
  - Defined as $\bar v_p(\hat{\bm k}) = \bar\omega / (\pi \bar k)$ with $\bar k = |\bm k| L / \pi$, $\bar\omega = \omega / \omega_0$, $\omega_0 = \sqrt{\mu/(\rho L^2)}$. Classical limits $\bar v_{p,T} = 1.0$ and $\bar v_{p,L} = \sqrt{\lambda/\mu + 2} = \sqrt{3} \approx 1.73205$.

### TV16 — Orientation angle units and numerical derivative scheme
- **Status:** **LOCKED [S]**
- **Evidence / Justification:**
  - Orientation $\theta$ evaluated in radians for trigonometric tensor rotations; reported in degrees for display/tables.
  - Numerical angular derivative $\partial \Delta / \partial \theta$ computed on the 7-point orientation grid $\theta \in \{0^\circ, 15^\circ, \dots, 90^\circ\}$ ($\Delta\theta = 15^\circ = \pi/12\,\mathrm{rad}$) via second-order central differences in the interior and second-order forward/backward differences at $\theta = 0^\circ, 90^\circ$.
  - Sensitivity $S_\theta = \max_\theta |\partial\Delta/\partial\theta| / \max_\theta \Delta$ reported in $\mathrm{rad}^{-1}$ and $\mathrm{deg}^{-1}$.

### TV17 — DOF ordering and node numbering
- **Status:** **LOCKED [A]**
- **Evidence / Justification:**
  - 4 nodes numbered counter-clockwise: Node 0 $(0,0)$, Node 1 $(L,0)$, Node 2 $(L,L)$, Node 3 $(0,L)$.
  - 8 DOFs per node: $\{u_x, u_{x,x}, u_{x,y}, u_{x,xy}, u_y, u_{y,x}, u_{y,y}, u_{y,xy}\}$.
  - Global element index: `idx(node, comp, typ) = 8*node + 4*comp + typ`.

---

## 2. Unresolved TV Items (Kept OPEN, Not Silently Closed)

| TV Item | Description | Status | Reason |
|---|---|---|---|
| TV6 (Case C) | Case C inclusion geometry and contrast | **OPEN** | No published or frozen numbers in repo; parameters must not be invented. |
| TV14 | Case C reference phase nondimensionalization | **OPEN** | Pertains to Case C. |
| TV18 | BFS circular inclusion representation | **OPEN** | Pertains to Case C. |
| TV9 | Mishra 2026 homogeneous limit | **OPEN** | Pertains to Layer 4 published validation. |
| TV12 | Fig 4(c) axis ranges and sampling | **OPEN** | Pertains to Layer 2b published validation. |
