# Mathematical Derivations: Guyer–Krumhansl Conduction with Boundary Heat Loss

**Author:** Vipin Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Date:** September 2026  

---

## 1. Governing System in 1D

Consider a slab of thickness $L$ subject to a pulsed heat flux on the front surface ($x = 0$) and convective/radiative boundary heat losses at both front and rear surfaces ($x = L$).

The dimensional governing equations under the Guyer–Krumhansl (GK) model are:
$$\rho c \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0 \tag{1}$$
$$\tau_q \frac{\partial q}{\partial t} + q + \lambda_0 \frac{\partial T}{\partial x} - \kappa^2 \frac{\partial^2 q}{\partial x^2} = 0 \tag{2}$$
where $\rho$ is density, $c$ is specific heat capacity, $\lambda_0$ is baseline thermal conductivity, $\alpha_0 = \lambda_0 / (\rho c)$ is thermal diffusivity, $\tau_q$ is the thermal relaxation time, and $\kappa^2 = \ell^2$ is the nonlocal mean-free-path parameter.

### Boundary Conditions with Heat Loss
The sample exchanges heat with an ambient environment at temperature $T_0$ via linearized radiation and convection:
$$q(0, t) = q_{\mathrm{laser}}(t) - h_0 [T(0, t) - T_0] \tag{3a}$$
$$q(L, t) = h_L [T(L, t) - T_0] \tag{3b}$$
where $h_0, h_L$ are total effective heat transfer coefficients ($h = h_{\mathrm{conv}} + 4\varepsilon \sigma_{\mathrm{SB}} T_0^3$).

Initial conditions are quiescent:
$$T(x, 0) = T_0, \qquad q(x, 0) = 0 \tag{4}$$

---

## 2. Laplace-Domain Formulation

Let $\theta(x, t) = T(x, t) - T_0$. Applying the Laplace transform $\bar{\theta}(x, s) = \mathcal{L}\{\theta(x, t)\}$:
$$\rho c s \bar{\theta}(x, s) + \frac{d\bar{q}}{dx} = 0 \implies \frac{d\bar{q}}{dx} = -\rho c s \bar{\theta}(x, s) \tag{5}$$
$$(1 + \tau_q s)\bar{q}(x, s) - \kappa^2 \frac{d^2\bar{q}}{dx^2} = -\lambda_0 \frac{d\bar{\theta}}{dx} \tag{6}$$

Differentiating Eq. (6) with respect to $x$ and substituting Eq. (5):
$$(1 + \tau_q s)\frac{d\bar{q}}{dx} - \kappa^2 \frac{d^3\bar{q}}{dx^3} = -\lambda_0 \frac{d^2\bar{\theta}}{dx^2}$$
$$-(1 + \tau_q s)\rho c s \bar{\theta} + \kappa^2 \rho c s \frac{d^2\bar{\theta}}{dx^2} = -\lambda_0 \frac{d^2\bar{\theta}}{dx^2}$$
$$(\lambda_0 + \kappa^2 \rho c s)\frac{d^2\bar{\theta}}{dx^2} = \rho c s(1 + \tau_q s)\bar{\theta}$$
Dividing by $\rho c$:
$$(\alpha_0 + \kappa^2 s)\frac{d^2\bar{\theta}}{dx^2} = s(1 + \tau_q s)\bar{\theta}$$
Hence, the Laplace-domain temperature satisfies the Helmholtz equation:
$$\frac{d^2\bar{\theta}}{dx^2} - m^2(s)\bar{\theta} = 0 \tag{7}$$
where the propagation parameter $m(s)$ is:
$$m(s) = \sqrt{\frac{s(1 + \tau_q s)}{\alpha_0 + \kappa^2 s}} \tag{8}$$

---

## 3. Effective Boundary Impedance and Heat Flux Operator

The general solution of Eq. (7) is:
$$\bar{\theta}(x, s) = C_1 \cosh(m(L - x)) + C_2 \sinh(m(L - x)) \tag{9}$$

To find the relationship between $\bar{q}(x, s)$ and $\frac{d\bar{\theta}}{dx}$, note that because $\bar{\theta}$ is a linear combination of spatial modes $e^{\pm m x}$, and $d\bar{q}/dx = -\rho c s \bar{\theta}$, the flux $\bar{q}(x, s)$ also satisfies the modal spatial equation:
$$\frac{d^2\bar{q}}{dx^2} = m^2(s)\bar{q}$$
Substituting this back into Eq. (6):
$$\left[(1 + \tau_q s) - \kappa^2 m^2(s)\right]\bar{q}(x, s) = -\lambda_0 \frac{d\bar{\theta}}{dx} \tag{10}$$

Substituting $m^2(s)$ from Eq. (8):
$$(1 + \tau_q s) - \kappa^2 \frac{s(1 + \tau_q s)}{\alpha_0 + \kappa^2 s} = (1 + \tau_q s)\left[1 - \frac{\kappa^2 s}{\alpha_0 + \kappa^2 s}\right] = (1 + \tau_q s)\left[\frac{\alpha_0}{\alpha_0 + \kappa^2 s}\right]$$
Therefore, Eq. (10) yields:
$$\bar{q}(x, s) = -\lambda_{\mathrm{eff}}(s) \frac{d\bar{\theta}}{dx} \tag{11}$$
where the dynamic Laplace-domain thermal conductivity $\lambda_{\mathrm{eff}}(s)$ is:
$$\lambda_{\mathrm{eff}}(s) = \lambda_0 \left[\frac{\alpha_0 + \kappa^2 s}{\alpha_0 (1 + \tau_q s)}\right] = \lambda_0 \left[\frac{1 + \left(\frac{\kappa^2}{\alpha_0}\right)s}{1 + \tau_q s}\right] \tag{12}$$

---

## 4. Analytical Proof of Theorem 1 (Heat-Loss Invariance)

Define the Guyer–Krumhansl resonance ratio:
$$B = \frac{\kappa^2}{\alpha_0 \tau_q}$$

### Case $B = 1$:
When $B = 1$, we have $\frac{\kappa^2}{\alpha_0} = \tau_q$. Substituting into Eq. (12):
$$\lambda_{\mathrm{eff}}(s) = \lambda_0 \left[\frac{1 + \tau_q s}{1 + \tau_q s}\right] \equiv \lambda_0 \tag{13}$$
and substituting into Eq. (8):
$$m^2(s) = \frac{s(1 + \tau_q s)}{\alpha_0(1 + \tau_q s)} \equiv \frac{s}{\alpha_0} \tag{14}$$

### Boundary Conditions at $B = 1$:
At the front surface $x = 0$:
$$\bar{q}(0, s) = -\left.\lambda_{\mathrm{eff}}(s)\frac{d\bar{\theta}}{dx}\right|_{x=0} = -\left.\lambda_0 \frac{d\bar{\theta}}{dx}\right|_{x=0}$$
The Robin boundary condition (3a) in the Laplace domain is:
$$\bar{q}(0, s) = \bar{q}_{\mathrm{laser}}(s) - h_0 \bar{\theta}(0, s)$$
$$-\left.\lambda_0 \frac{d\bar{\theta}}{dx}\right|_{x=0} + h_0 \bar{\theta}(0, s) = \bar{q}_{\mathrm{laser}}(s) \tag{15a}$$

At the rear surface $x = L$:
$$\bar{q}(L, s) = -\left.\lambda_{\mathrm{eff}}(s)\frac{d\bar{\theta}}{dx}\right|_{x=L} = -\left.\lambda_0 \frac{d\bar{\theta}}{dx}\right|_{x=L}$$
The Robin boundary condition (3b) is:
$$\bar{q}(L, s) = h_L \bar{\theta}(L, s)$$
$$-\left.\lambda_0 \frac{d\bar{\theta}}{dx}\right|_{x=L} = h_L \bar{\theta}(L, s) \tag{15b}$$

### Conclusion of Proof:
Equations (7), (14), (15a), and (15b) are **IDENTICAL** to the classical Fourier heat conduction problem with convective/radiative cooling $h_0, h_L$:
$$\frac{d^2\bar{\theta}}{dx^2} - \frac{s}{\alpha_0}\bar{\theta} = 0, \quad -\lambda_0 \left.\frac{d\bar{\theta}}{dx}\right|_0 + h_0 \bar{\theta}(0) = \bar{q}_{\mathrm{laser}}(s), \quad -\lambda_0 \left.\frac{d\bar{\theta}}{dx}\right|_L - h_L \bar{\theta}(L) = 0$$
Since this boundary-value problem has a unique solution in the Laplace domain, it follows that:
$$\left.\bar{\theta}_{\mathrm{GK}}(x, s; \tau_q, \kappa^2, h_0, h_L)\right|_{B=1} \equiv \bar{\theta}_{\mathrm{Fourier}}(x, s; h_0, h_L) \tag{16}$$
Taking the inverse Laplace transform:
$$\left.\theta_{\mathrm{GK}}(x, t; \tau_q, \kappa^2, h_0, h_L)\right|_{B=1} \equiv \theta_{\mathrm{Fourier}}(x, t; h_0, h_L) \quad \forall t \ge 0, \; \forall x \in [0, L] \tag{17}$$

$\blacksquare$

---

## 5. Sensitivity Colinearity and Fisher Information Rank

Differentiating the identity $\theta_{\mathrm{GK}}|_{B=1} = \theta_{\mathrm{Fourier}}$ along the resonance manifold $\kappa^2 = \alpha_0 \tau_q$:
$$\left.\frac{\partial \theta}{\partial \tau_q}\right|_{B=1} d\tau_q + \left.\frac{\partial \theta}{\partial \kappa^2}\right|_{B=1} d\kappa^2 = 0$$
Since $d\kappa^2 = \alpha_0 d\tau_q$, it follows directly that:
$$\left.\frac{\partial \theta}{\partial \tau_q}\right|_{B=1} + \alpha_0 \left.\frac{\partial \theta}{\partial \kappa^2}\right|_{B=1} = 0$$
$$\implies \left.\frac{\partial \theta}{\partial \tau_q}\right|_{B=1} = -\alpha_0 \left.\frac{\partial \theta}{\partial \kappa^2}\right|_{B=1} \tag{18}$$
This holds for **arbitrary** values of $h_0$ and $h_L$.

### Structure of the 3-Parameter Fisher Information Matrix:
Let $\bm{\theta} = (\tau_q, \kappa^2, Bi)^\top$, where $Bi = Bi_0 = Bi_L$. The sensitivity Jacobian is:
$$\bm{J}(t) = \begin{bmatrix} J_{\tau_q}(t) & J_{\kappa^2}(t) & J_{Bi}(t) \end{bmatrix}$$
At $B = 1$:
$$J_{\kappa^2}(t) = -\frac{1}{\alpha_0} J_{\tau_q}(t)$$
Hence:
$$\bm{J}(t) = \begin{bmatrix} J_{\tau_q}(t) & -\frac{1}{\alpha_0}J_{\tau_q}(t) & J_{Bi}(t) \end{bmatrix}$$
The null vector of $\bm{J}$ is:
$$\bm{v}_{\mathrm{null}} = \begin{pmatrix} \alpha_0 \\ 1 \\ 0 \end{pmatrix}$$
since $\bm{J} \bm{v}_{\mathrm{null}} = \alpha_0 J_{\tau_q} - \frac{1}{\alpha_0}(\alpha_0) J_{\tau_q} + 0 \cdot J_{Bi} = 0$.

The Fisher Information Matrix $\bm{F} = \bm{J}^\top \bm{J}$ has eigenvalues:
$$\lambda_1 > 0, \quad \lambda_2 > 0, \quad \lambda_3 \equiv 0$$
Therefore, $\operatorname{rank}(\bm{F}) = 2 < 3$, and $\operatorname{cond}(\bm{F}) = \infty$.

**Physical interpretation:** Boundary heat loss provides independent information about the cooling rate, allowing $Bi$ to be well-conditioned and uniquely determined from the tail decay. However, boundary cooling has zero projection onto the null vector $\bm{v}_{\mathrm{null}}$, leaving the internal cancellation between relaxation $\tau_q$ and nonlocality $\kappa^2$ entirely unregularized.
