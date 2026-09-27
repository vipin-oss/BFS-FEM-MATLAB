# Prior-Art Comparison Table: Paper 11 Novelty Audit

This table rigorously classifies all relevant literature identified during the search, verifying the presence or absence of the physical and mathematical ingredients comprising Paper 11.

---

## 1. Comparative Prior-Art Matrix

| Paper & Citation | Year | Journal | GK Transport? | Robin / Heat Loss? | Laser Flash? | Resonance ($B=1$)? | Parameter Identification? | Sensitivity / FIM? | Main Overlap | What Paper 11 Adds Beyond |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Parker et al.** [1]<br>`10.1063/1.1728417` | 1961 | *J. Appl. Phys.* | No (Fourier) | No (Adiabatic) | Yes | No | Yes ($\alpha_0$ via $t_{1/2}$) | No | Defines baseline experimental laser flash protocol. | Introduces non-Fourier GK transport, nonlocality, and Robin boundary heat losses. |
| **Cowan** [2]<br>`10.1063/1.1729335` | 1963 | *J. Appl. Phys.* | No (Fourier) | **Yes** ($Bi > 0$) | Yes | No | Yes (Heat-loss correction) | No | Solves classical Fourier flash with convective/radiative surface cooling. | Establishes non-Fourier GK transport; serves as the asymptotic validation limit of Paper 11. |
| **Cape & Lehman** [3]<br>`10.1063/1.1729711` | 1963 | *J. Appl. Phys.* | No (Fourier) | **Yes** ($Bi > 0$) | Yes | No | Yes (Dual $\alpha, Bi$ fitting) | No | Classical 2D series solutions for combined pulse and heat-loss effects. | Extends heat loss analysis from classical Fourier diffusion to non-local GK transport. |
| **Guyer & Krumhansl** [4]<br>`10.1103/PhysRev.148.778` | 1966 | *Phys. Rev.* | **Yes** | No | No | No | No | No | Microscopic derivation of the constitutive rate equation with $\tau_q$ and $\kappa^2$. | Applies GK constitutive theory to flash geometry, Robin boundary losses, and inverse analysis. |
| **Both et al.** [5]<br>`10.1515/jnet-2015-0038` | 2016 | *J. Non-Equilib. Thermodyn.* | **Yes** | No (Adiabatic) | Yes | **Yes** (Algebraic $\frac{\kappa^2}{\tau} = \alpha$) | Yes (Least-squares curve fit) | No | Observes that bulk GK PDE algebraically recovers Fourier equation at resonance. | Proves that Robin boundary heat loss preserves the cancellation; provides sensitivity Jacobian and FIM analysis. |
| **Ván et al.** [6]<br>`10.1209/0295-5075/118/50005` | 2017 | *EPL* | **Yes** | No (Adiabatic) | Yes | **Yes** (Reference boundary) | Yes (Material property fitting) | No | Validates GK model on room-temperature basalt/composite samples. | Formulates coupled Robin boundary-value problem and analyzes parameter identifiability degeneracy. |
| **Kovács** [7]<br>`10.1016/j.ijheatmasstransfer.2018.07.039` | 2018 | *Int. J. Heat Mass Transf.* | **Yes** | No (Adiabatic, $Bi=0$) | Yes | **Yes** (Notes $B=1$ limit) | No (Forward only) | No | Exact analytical Laplace-domain solution for adiabatic GK laser flash response. | **Incorporates front/rear Robin heat losses ($Bi > 0$), proves boundary impedance collapse $\lambda_{\mathrm{eff}} \to \lambda_0$, and evaluates Fisher information.** |
| **Precursor Study**<br>*(Unpublished Framework)* | — | *Unpublished* | **Yes** | No (Adiabatic, $Bi=0$) | Yes | **Yes** ($B=1$) | Yes | **Yes** ($J_{\tau_q} = -\alpha_0 J_{\kappa^2}$) | Discovers adiabatic Fourier-resonance sensitivity collinearity. | **Asks and answers whether realistic boundary cooling breaks the collinearity; proves exact invariance theorem under Robin BCs.** |
| **Paper 11**<br>*(Present Work)* | 2026 | *Target: Q1 Heat Transfer* | **Yes** | **Yes** ($Bi_0, Bi_L > 0$) | **Yes** | **Yes** ($B=1$) | **Yes** | **Yes** ($3\times 3$ FIM: SVD, null space) | **Integrates non-Fourier GK transport with Robin convective/radiative cooling in laser flash.** | **Proves Theorem 1: Heat-loss invariance of Fourier resonance; establishes that $Bi$ is identifiable while $(\tau_q, \kappa^2)$ null space is strictly invariant.** |

---

## 2. Bibliographic References

1. W. J. Parker, R. J. Jenkins, C. P. Butler, G. L. Abbott, *Flash method of determining thermal diffusivity, heat capacity, and thermal conductivity*, Journal of Applied Physics 32 (1961) 1679–1684. https://doi.org/10.1063/1.1728417
2. R. D. Cowan, *Pulse method of measuring thermal diffusivity at high temperatures*, Journal of Applied Physics 34 (1963) 926–927. https://doi.org/10.1063/1.1729335
3. J. A. Cape, G. W. Lehman, *Temperature and finite pulse-time effects in the flash method for measuring thermal diffusivity*, Journal of Applied Physics 34 (1963) 1909–1913. https://doi.org/10.1063/1.1729711
4. R. A. Guyer, J. A. Krumhansl, *Thermal conductivity, second sound, and phonon hydrodynamic phenomena in nonmetallic crystals*, Physical Review 148 (1966) 778–788. https://doi.org/10.1103/PhysRev.148.778
5. S. Both, B. Czél, T. Fülöp, G. Gróf, Á. Gyenis, R. Kovács, P. Ván, J. Verhás, *Deviation from the Fourier law in room-temperature heat pulse experiments*, Journal of Non-Equilibrium Thermodynamics 41 (2016) 41–48. https://doi.org/10.1515/jnet-2015-0038
6. P. Ván, A. Berezovski, T. Fülöp, Gy. Gróf, R. Kovács, Á. Lovas, J. Verhás, *Guyer-Krumhansl–type heat conduction at room temperature*, EPL (Europhysics Letters) 118 (2017) 50005. https://doi.org/10.1209/0295-5075/118/50005
7. R. Kovács, *Analytic solution of Guyer-Krumhansl equation for laser flash experiments*, International Journal of Heat and Mass Transfer 127 (2018) 631–636. https://doi.org/10.1016/j.ijheatmasstransfer.2018.07.039
