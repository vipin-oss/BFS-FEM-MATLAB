# Mathematical Derivations for Paper 10: Extension E1
## Finite-Fluence Nonlinear Guyer–Krumhansl Heat Conduction

**Author:** V. Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Date:** 2026-09-27  

---

## 1. Governing Dimensional Equations

In one space dimension ($0 \le x \le L$), energy conservation in the absence of internal volumetric heat sources is:
$$\rho c \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0 \tag{1}$$
where:
* $T(x,t)$ is the absolute temperature field $[\si{\kelvin}]$,
* $q(x,t)$ is the heat flux $[\si{\watt\per\square\meter}]$,
* $\rho c$ is the volumetric heat capacity $[\si{\joule\per\cubic\meter\per\kelvin}]$.

The non-Fourier Guyer–Krumhansl (GK) constitutive law with temperature-dependent thermal conductivity $\lambda(T)$ is:
$$\tau_q \, \frac{\partial q}{\partial t} + q + \lambda(T)\,\frac{\partial T}{\partial x} - \kappa^2\,\frac{\partial^2 q}{\partial x^2} = 0 \tag{2}$$
where:
* $\tau_q$ is the heat flux relaxation time $[\si{\second}]$,
* $\kappa^2$ is the spatial nonlocality parameter $[\si{\square\meter}]$,
* $\lambda(T) = \lambda_0\left[1 + \beta_T(T - T_0)\right]$ is the thermal conductivity $[\si{\watt\per\meter\per\kelvin}]$,
* $\beta_T = \lambda_0^{-1} \left(\frac{\partial \lambda}{\partial T}\right)_{T_0}$ is the thermal conductivity sensitivity coefficient $[\si{\per\kelvin}]$.

---

## 2. Nondimensionalisation and Scaling

We define characteristic reference scales:
* Reference length: $L$ (slab thickness)
* Reference diffusivity: $\alpha_0 = \frac{\lambda_0}{\rho c}$
* Reference diffusion time: $t_{\mathrm{diff}} = \frac{L^2}{\alpha_0}$
* Reference temperature rise: $\Delta T_{\mathrm{ref}} = T_{\mathrm{end}} - T_0 = \frac{q_{\max} t_p}{\rho c L}$
* Reference peak flux: $q_{\max}$

We introduce the dimensionless variables:
$$\hat{x} = \frac{x}{L}, \qquad \hat{t} = \frac{\alpha_0 t}{L^2}, \qquad \hat{T} = \frac{T - T_0}{T_{\mathrm{end}} - T_0}, \qquad \hat{q} = \frac{q}{q_{\max}}$$

Dimensionless groups:
* Fourier pulse duration parameter: $\tau_\Delta = \frac{\alpha_0 t_p}{L^2}$
* Dimensionless relaxation time: $\hat{\tau}_q = \frac{\alpha_0 \tau_q}{L^2}$
* Dimensionless nonlocality coefficient: $\hat{\kappa}^2 = \frac{\kappa^2}{L^2}$
* Dimensionless fluence nonlinearity parameter: $\varepsilon_\lambda = \beta_T(T_{\mathrm{end}} - T_0) = \beta_T \Delta T_{\mathrm{ref}}$

### Step 2.1: Energy Equation Nondimensionalisation
From (1):
$$\rho c \, \frac{\Delta T_{\mathrm{ref}}}{t_{\mathrm{diff}}} \, \frac{\partial \hat{T}}{\partial \hat{t}} + \frac{q_{\max}}{L} \, \frac{\partial \hat{q}}{\partial \hat{x}} = 0$$
Using $t_{\mathrm{diff}} = L^2/\alpha_0$ and $\Delta T_{\mathrm{ref}} = \frac{q_{\max} t_p}{\rho c L}$:
$$\rho c \, \frac{q_{\max} t_p}{\rho c L} \, \frac{\alpha_0}{L^2} \, \frac{\partial \hat{T}}{\partial \hat{t}} + \frac{q_{\max}}{L} \, \frac{\partial \hat{q}}{\partial \hat{x}} = 0$$
$$\frac{q_{\max}}{L} \left( \frac{\alpha_0 t_p}{L^2} \right) \frac{\partial \hat{T}}{\partial \hat{t}} + \frac{q_{\max}}{L} \, \frac{\partial \hat{q}}{\partial \hat{x}} = 0 \implies \tau_\Delta \, \frac{\partial \hat{T}}{\partial \hat{t}} + \frac{\partial \hat{q}}{\partial \hat{x}} = 0 \tag{3}$$

### Step 2.2: Constitutive Equation Nondimensionalisation
From (2):
$$\tau_q \, \frac{q_{\max} \alpha_0}{L^2} \, \frac{\partial \hat{q}}{\partial \hat{t}} + q_{\max} \hat{q} + \lambda_0\left(1 + \varepsilon_\lambda \hat{T}\right) \frac{\Delta T_{\mathrm{ref}}}{L} \, \frac{\partial \hat{T}}{\partial \hat{x}} - \kappa^2 \, \frac{q_{\max}}{L^2} \, \frac{\partial^2 \hat{q}}{\partial \hat{x}^2} = 0$$
Divide the entire equation by $q_{\max}$:
$$\left(\frac{\alpha_0 \tau_q}{L^2}\right) \frac{\partial \hat{q}}{\partial \hat{t}} + \hat{q} + \frac{\lambda_0 \Delta T_{\mathrm{ref}}}{q_{\max} L}\left(1 + \varepsilon_\lambda \hat{T}\right)\frac{\partial \hat{T}}{\partial \hat{x}} - \left(\frac{\kappa^2}{L^2}\right)\frac{\partial^2 \hat{q}}{\partial \hat{x}^2} = 0$$
Note that:
$$\frac{\lambda_0 \Delta T_{\mathrm{ref}}}{q_{\max} L} = \frac{\rho c \alpha_0}{q_{\max} L} \, \frac{q_{\max} t_p}{\rho c L} = \frac{\alpha_0 t_p}{L^2} = \tau_\Delta$$
Therefore:
$$\hat{\tau}_q \, \frac{\partial \hat{q}}{\partial \hat{t}} + \hat{q} + \tau_\Delta\left(1 + \varepsilon_\lambda \hat{T}\right)\frac{\partial \hat{T}}{\partial \hat{x}} - \hat{\kappa}^2 \, \frac{\partial^2 \hat{q}}{\partial \hat{x}^2} = 0 \tag{4}$$
Dropping hats for brevity yields equations (7) and (8) in the manuscript.

---

## 3. Linear Fourier-Resonance Sensitivity Colinearity

In the linear zero-fluence limit ($\varepsilon_\lambda = 0$), the system in dimensional form is:
$$\rho c \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0$$
$$\tau_q \, \frac{\partial q}{\partial t} + q + \lambda_0 \, \frac{\partial T}{\partial x} - \kappa^2 \, \frac{\partial^2 q}{\partial x^2} = 0$$

Applying the Laplace transform $\mathcal{L}\{f(t)\} = \bar{f}(s)$ with quiescent initial conditions $T(x,0) = 0, q(x,0) = 0$:
$$\rho c s \bar{T} + \frac{d\bar{q}}{dx} = 0 \implies \bar{q} = -\frac{\rho c s}{\frac{d}{dx}} \dots$$
$$(1 + \tau_q s)\bar{q} - \kappa^2 \frac{d^2\bar{q}}{dx^2} = -\lambda_0 \frac{d\bar{T}}{dx}$$
Differentiating the constitutive equation with respect to $x$ and substituting $d\bar{q}/dx = -\rho c s \bar{T}$:
$$-(1 + \tau_q s)\rho c s \bar{T} + \kappa^2 \rho c s \frac{d^2\bar{T}}{dx^2} = -\lambda_0 \frac{d^2\bar{T}}{dx^2}$$
$$\left(\lambda_0 + \kappa^2 \rho c s\right) \frac{d^2\bar{T}}{dx^2} = \rho c s (1 + \tau_q s)\bar{T}$$
Dividing by $\rho c$:
$$\left(\alpha + \kappa^2 s\right) \frac{d^2\bar{T}}{dx^2} = s (1 + \tau_q s)\bar{T} \implies \frac{d^2\bar{T}}{dx^2} = m^2(s) \bar{T} \tag{5}$$
where the propagation parameter is:
$$m^2(s) = \frac{s(1 + \tau_q s)}{\alpha + \kappa^2 s} = \frac{s}{\alpha} \, \frac{1 + \tau_q s}{1 + \left(\frac{\kappa^2}{\alpha \tau_q}\right)\tau_q s} \tag{6}$$

### The Fourier-Resonance Cancellation
Define the non-dimensional resonance ratio:
$$B = \frac{\kappa^2}{\alpha \tau_q}$$
When $B = 1$:
$$m^2(s) = \frac{s}{\alpha} \, \frac{1 + \tau_q s}{1 + 1 \cdot \tau_q s} \equiv \frac{s}{\alpha} \tag{7}$$
The factor $(1 + \tau_q s)$ cancels identically from the numerator and denominator!  
As a direct consequence, $m^2(s)$ reduces identically to the classical Fourier diffusion propagation factor, and $\bar{T}(x,s)$ is completely independent of $\tau_q$.

### Sensitivity Colinearity
Differentiating $m^2(s)$ with respect to $\tau_q$ and $\kappa^2$ in the neighborhood of $B = 1$:
$$\frac{\partial m^2}{\partial \tau_q} = \frac{s^2}{\alpha + \kappa^2 s} = \frac{s^2}{\alpha(1 + \tau_q s)}$$
$$\frac{\partial m^2}{\partial \kappa^2} = -\frac{s^2(1 + \tau_q s)}{(\alpha + \kappa^2 s)^2} = -\frac{s^2(1 + \tau_q s)}{\alpha^2(1 + \tau_q s)^2} = -\frac{s^2}{\alpha^2(1 + \tau_q s)}$$
Comparing the two sensitivities:
$$\frac{\partial m^2}{\partial \tau_q} = -\alpha \, \frac{\partial m^2}{\partial \kappa^2} \tag{8}$$
Since the temperature solution depends on the parameters solely through $m^2(s)$ (via $\frac{\partial T}{\partial \theta} = \frac{\partial T}{\partial m^2}\frac{\partial m^2}{\partial \theta}$), we obtain the exact collinearity identity:
$$\frac{\partial T}{\partial \tau_q} = -\alpha \, \frac{\partial T}{\partial \kappa^2} \tag{9}$$
This establishes rank deficiency $\operatorname{rank}(J) = 1$, $\sigma_2 = 0$, and $\operatorname{cond}(F) = \infty$.

---

## 4. Nonlinear Breakdown Under Finite Fluence

When $\varepsilon_\lambda \ne 0$, the local effective diffusivity is:
$$\alpha(x,t) = \frac{\lambda(T(x,t))}{\rho c} = \alpha_0\left[1 + \varepsilon_\lambda \hat{T}(x,t)\right]$$
The local resonance parameter becomes space- and time-dependent:
$$B(x,t) = \frac{\kappa^2}{\alpha(x,t)\tau_q} = \frac{\kappa^2}{\alpha_0 \tau_q\left[1 + \varepsilon_\lambda \hat{T}(x,t)\right]} = \frac{1}{1 + \varepsilon_\lambda \hat{T}(x,t)} \tag{10}$$
Because the slab experiences a transient temperature gradient ($T(0,t) > T(1,t)$), $B(x,t)$ deviates non-uniformly from unity across $x \in [0,L]$.  
This destroys the spatial algebraic cancellation, breaking the colinearity relation (9) and activating the second singular value $\sigma_2 > 0$.

---

## 5. Classical Nonlinear Fourier Limit ($\tau_q \to 0, \kappa^2 \to 0$)

Setting $\hat{\tau}_q \to 0$ and $\hat{\kappa}^2 \to 0$ in (4) eliminates flux relaxation and nonlocality:
$$\hat{q} = -\tau_\Delta\left(1 + \varepsilon_\lambda \hat{T}\right)\frac{\partial \hat{T}}{\partial \hat{x}} \tag{11}$$
Substituting (11) into the energy equation (3):
$$\tau_\Delta \, \frac{\partial \hat{T}}{\partial \hat{t}} - \frac{\partial}{\partial \hat{x}}\left[\tau_\Delta\left(1 + \varepsilon_\lambda \hat{T}\right)\frac{\partial \hat{T}}{\partial \hat{x}}\right] = 0$$
Dividing by $\tau_\Delta$:
$$\frac{\partial \hat{T}}{\partial \hat{t}} = \frac{\partial}{\partial \hat{x}}\left[\left(1 + \varepsilon_\lambda \hat{T}\right)\frac{\partial \hat{T}}{\partial \hat{x}}\right] \tag{12}$$
This is the classical nonlinear parabolic heat conduction equation with temperature-dependent thermal conductivity.
