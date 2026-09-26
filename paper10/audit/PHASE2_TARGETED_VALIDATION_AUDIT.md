# PHASE 2 TARGETED INDEPENDENT VALIDATION AUDIT RECORD (FINAL RESOLUTION)

### Project: `paper10`
### Document: `paper10/audit/PHASE2_TARGETED_VALIDATION_AUDIT.md`
**Date:** 2026-09-26  
**Audited Baseline:** Commit `c0f1d31d4a0676edea540875ebbaca23b6b1f6f1`  
**Updated Baseline:** Authoritative TMM Secular Validation Resolution  
**Auditor:** Independent Mathematical & Numerical Auditor (Arena Agent)  
**Execution Stage:** Post-Audit Final Validation Correction  
**Status:** FULLY RESOLVED & PASSED

---

## 1. Audit 1 — Papargyri-Beskou Benchmark Independence (Resolved)

### 1.1 Resolution Summary
The targeted audit correctly identified that `solve_numerical_omega(k)` in `paper10/solver/antiplane.py` used a reference-centered search bracket $[0.8 \omega_{\text{PB}}, 1.2 \omega_{\text{PB}}]$ and solved the scalar root $\beta_s(\omega) - k = 0$, making it an internal characteristic-root consistency check.

**Correction Executed:**
1. Retained `solve_numerical_omega(k)` in `antiplane.py` explicitly labeled as:
   `[INTERNAL CHARACTERISTIC-ROOT CONSISTENCY CHECK]`.
2. Implemented `solve_tmm_secular_omega(k)` in `antiplane.py` as the **official authoritative external benchmark solver**:
   $$f(\omega) = \det\left[ T(\omega, a) - e^{i k a} I \right] = 0$$
   using an agnostic acoustic search bracket $\omega \in [0.5 V_s k, 2.0 V_s k]$ that depends **only on classical wave speed $V_s$ and wavenumber $k$**, having zero dependency on the Papargyri-Beskou formula or microstructural scale parameters $c, d$.
3. Re-ran the complete 50-point benchmark grid in `paper10/validation/run_benchmarks.py`.

### 1.2 Authoritative Independent Benchmark Evidence (50 Wavenumber Points)
- **Reference Equation:** $\omega_{\text{PB}}(k) = V_s k \sqrt{\frac{1 + c k^2}{1 + (d^2/3) k^2}}$ (evaluated strictly post-solve for comparison).
- **Numerical Equation:** $\det[T(\omega, a) - e^{i k a} I] = 0$ solved via Brent's method on $[0.5 V_s k, 2.0 V_s k]$.
- **Independent Maximum Relative Error:** $\mathbf{2.45 \times 10^{-15}}$ (Pass threshold $\le 0.5\%$).
- **Maximum Secular Residual:** $1.90 \times 10^{-14}$.
- **Convergence Failures:** 0.
- **Internal Scalar Check Maximum Error:** $3.87 \times 10^{-16}$.
- **Audit 1 Final Status:** **PASS** (complete mathematical independence established).

---

## 2. Audit 2 — DPL Complex-Wavenumber Sign Convention (Resolved)

### 2.1 Resolution Summary
- **Harmonic Convention:** $\exp(-i \omega t)$, space-time factor $\exp\left[ i(k_x x - \omega t) \right] = \exp\left[ i(k_r x - \omega t) \right] \exp(-k_i x)$ where $k_x = k_r + i k_i$.
- **Decay Physics:**
  - Forward waves ($k_r > 0$): $\exp(-k_i x) \to 0$ as $x \to +\infty \iff \mathbf{k_i > 0}$ ($|\lambda| \le 1$).
  - Backward waves ($k_r < 0$): $\exp(-k_i x) \to 0$ as $x \to -\infty \iff \mathbf{k_i < 0}$ ($|\lambda| \ge 1$).

### 2.2 Documentation & Implementation Distinction
To prevent conflating signed wavenumbers with attenuation magnitudes:
- **Signed Bloch Wavenumber:** $k_x a = k_r a + i k_i a$ where $k_i a = -\ln |\lambda_m|$ is preserved as `ki_signed`.
- **Attenuation Magnitude Diagnostic:** $\alpha a = |k_i a| = |\ln |\lambda_m||$ is recorded as `alpha_a` (and `ki_a` for backward compatibility).
- **Directional Classification:** Modes are classified as `is_forward_decaying = True` if $|\lambda_m| \le 1$ ($k_i a \ge 0$).
- **Audit 2 Final Status:** **PASS** (sign convention and attenuation diagnostics rigorously separated and documented).

---

## 3. Overall Phase 2 Gate Evaluation

### Overall Status: **PASS**

All requirements of Phase 2 are satisfied:
1. **Gate G2-A (Implementation Integrity):** PASS
2. **Gate G2-B (Classical Limit):** PASS (Asymptotic error $= 1.52 \times 10^{-11} \le 0.5\%$)
3. **Gate G2-C (Authoritative Independent Benchmark):** PASS (Max relative error $= 2.45 \times 10^{-15} \le 0.5\%$)
4. **Gate G2-D (Periodic Conservative Pilot):** PASS (252 pass-band points, 2 Bragg gaps, $\lvert\det(T_{\text{cell}})-1\rvert = 2.66 \times 10^{-13}$)
5. **Gate G2-E (DPL Implementation Sanity):** PASS (Active DPL phase lags, stable complex roots, signed wavenumber tracking)
