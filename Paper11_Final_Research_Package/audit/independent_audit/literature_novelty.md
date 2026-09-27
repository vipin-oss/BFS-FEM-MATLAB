# Literature Novelty Audit: Paper 11 (Heat-Loss Invariance)

**Audit Date:** September 2026  
**Auditor:** Independent Scientific Audit Agent  
**Subject:** Novelty Assessment of "Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing"

---

## 1. Prior Art and Comparison Table

| Citation & Journal | Physical Model | Boundary Conditions | Parameter Identifiability / Sensitivity Result | Relation to Paper 11 & Distinct Contribution |
| :--- | :--- | :--- | :--- | :--- |
| **Parker et al. (1961)**<br>*J. Appl. Phys.* | Classical Fourier diffusion | Adiabatic (idealized) | Determines $\alpha_0$ via half-rise time ($t_{1/2}$) | Baseline flash method; assumes instantaneous pulse and zero heat loss. No non-Fourier terms. |
| **Cowan (1963)**<br>*J. Appl. Phys.* | Classical Fourier diffusion | Convective/radiative cooling (Robin BCs, $Bi > 0$) | Solves transcendental eigenvalue equation for heat-loss corrections | Establishes classical heat-loss correction; serves as Benchmark 2 for Paper 11 in the singular limit $\tau_q, \kappa^2 \to 0$. |
| **Cape & Lehman (1963)**<br>*J. Appl. Phys.* | Classical Fourier diffusion | Combined finite-pulse width and Robin heat loss | Analytical 2D series solutions for $\alpha_0$ and $Bi$ | Classical standard for dual corrections in ASTM E1461. No non-local or relaxation effects. |
| **Guyer & Krumhansl (1966)**<br>*Phys. Rev.* | Phonon hydrodynamics (GK equation) | Unbounded crystal / infinite medium | Microscopic derivation of $\tau_q$ (normal/umklapp) and $\kappa^2$ | Fundamental constitutive model derivation. No flash analysis, no boundary losses, no inverse problem. |
| **Both et al. (2016)**<br>*J. Non-Equilib. Thermodyn.* | Guyer–Krumhansl heat conduction | Adiabatic flash pulse | Notes algebraic reduction to Fourier when $\kappa^2/\tau = \alpha$ | Identifies forward "Fourier resonance" algebraic identity; no sensitivity or identifiability analysis, no heat loss. |
| **Ván et al. (2017)**<br>*Continuum Mech. Thermodyn.* | Guyer–Krumhansl continuum mechanics | Adiabatic flash pulse | Validates GK model against room-temperature rock/foam data | Forward experimental validation; does not evaluate Fisher information or boundary heat loss. |
| **Kovács (2018)**<br>*Int. J. Heat Mass Transfer* | Analytical Guyer–Krumhansl solution | Adiabatic pulse ($q(0,t) = q_0, q(L,t) = 0$) | Closed-form Laplace inversion for forward pulse response | Benchmarks GK forward response under adiabatic conditions. Explicitly omits convective/radiative heat loss ($Bi = 0$). |
| **Precursor Study (Unpublished Framework)** | Linear Guyer–Krumhansl flash model | Adiabatic boundary conditions ($Bi_0 = Bi_L = 0$) | Discovers local sensitivity collinearity $J_{\tau_q} = -\alpha_0 J_{\kappa^2}$ at $B = 1$ | Proves adiabatic singularity; does not consider or solve the boundary heat loss problem ($Bi > 0$). |
| **Paper 11 (This Work)** | Coupled Guyer–Krumhansl transport | **Convective/radiative Robin BCs ($Bi_0, Bi_L > 0$)** | **Proves Theorem 1: Heat-loss invariance of Fourier resonance; $J_{\tau_q} \equiv -\alpha_0 J_{\kappa^2}$ persists identically; $Bi$ identifiable ($\sigma_1/\sigma_2 \in [2.3, 4.9]$) while null vector $(1, \alpha_0, 0)^\top$ remains unregularized** | **First rigorous proof that boundary cooling cannot regularize the GK parameter singularity, establishing a fundamental no-go theorem for heat-loss corrections in laser flash analysis.** |

---

## 2. Specific Defensible Novelty Claim

The specific and mathematically defensible novelty of Paper 11 is defined as follows:

> *"At the Fourier-resonance condition $B \equiv \kappa^2 / (\alpha_0 \tau_q) = 1$, the inclusion of arbitrary linear Robin convective and radiative boundary heat losses ($Bi_0, Bi_L \ge 0$) does not regularize the Guyer–Krumhansl sensitivity singularity $\partial T / \partial \tau_q = -\alpha_0 \partial T / \partial \kappa^2$. The invariance is exact, holding across all time, all spatial locations, and for arbitrary thermal excitations because both the bulk propagation factor $m^2(s)$ and the dynamic surface impedance $\lambda_{\mathrm{eff}}(s)$ collapse simultaneously to their classical Fourier counterparts."*

---

## 3. Analysis of Existing Literature Overlap

1. **Does the literature already contain GK with Robin boundary conditions?**
   While generic Robin conditions are standard in classical heat transfer, closed-form analytical solutions and systematic parameter identifiability of the coupled GK Robin system have not been reported in the laser flash literature.
2. **Has the Fourier-resonance degeneracy with heat loss been studied?**
   No. Existing non-Fourier laser flash studies either treat adiabatic pulses (Kovács 2018) or assume classical Fourier behavior when applying Cowan heat-loss corrections.
3. **Is the paper merely a repackaging of the precursor?**
   No. The precursor demonstrated non-identifiability under the assumption of adiabatic insulation. A major open question in thermal metrology is whether realistic experimental features (such as cooling tails) provide the missing information to break parameter degeneracies. Paper 11 resolves this question with a definitive no-go theorem, showing that boundary heat loss provides information *only* about the cooling parameter $Bi$, while leaving the non-Fourier null space strictly invariant.
