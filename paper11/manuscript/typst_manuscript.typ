#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  header: align(right)[
    #text(size: 8.5pt, fill: luma(100))[
      *Paper 11:* Invariance of GK Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss
    ]
  ],
  footer: align(center)[#context text(size: 9pt)[Page #counter(page).display()]]
)

#set text(
  font: "Liberation Serif",
  size: 11pt,
  lang: "en"
)

#let Bi = math.italic("Bi")
#let grad = math.nabla

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1.5em
)

// Title Block
#align(center)[
  #v(1em)
  #text(size: 17pt, weight: "bold")[
    Invariance of the Guyer--Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing
  ]
  #v(1.2em)
  #text(size: 12pt, weight: "bold")[Vipin Gupta] \
  #text(size: 10pt, style: "italic")[
    Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India \
    Email: vipin.gupta\@gurugramuniversity.ac.in
  ]
  #v(1em)
  #text(size: 10pt)[#datetime.today().display("[month repr:long] [day], [year]")]
  #v(1.5em)
]

// Abstract Block
#rect(
  width: 100%,
  stroke: 0.5pt + luma(150),
  fill: rgb(248, 249, 250),
  inset: 14pt,
  radius: 4pt
)[
  #align(center)[#text(weight: "bold", size: 11pt)[Abstract]]
  #v(0.5em)
  #text(size: 10pt)[
    In non-Fourier thermal transport characterization via laser flash analysis, the Guyer--Krumhansl (GK) constitutive model incorporates both thermal relaxation $tau_q$ and spatial nonlocality $kappa^2$. At the Fourier-resonance condition $B equiv kappa^2 / (alpha_0 tau_q) = 1$, idealized adiabatic analyses reveal an exact sensitivity collinearity $partial T / partial tau_q = -alpha_0 partial T / partial kappa^2$, which causes the Fisher information matrix to degenerate and precludes simultaneous estimation of $tau_q$ and $kappa^2$. In practical flash experiments, however, samples invariably experience convective and radiative heat losses at their irradiated and rear faces, characterized by non-zero Biot numbers ($Bi_0, Bi_L > 0$). In this study, we investigate whether boundary heat loss breaks this sensitivity collinearity and regularizes the parameter estimation problem. We formulate the coupled 1D GK transport system with Robin boundary conditions and analytically prove that at $B = 1$, the GK temperature field collapses identically to the classical Fourier heat conduction solution with the corresponding heat losses for all Biot numbers, all times, and all spatial positions. Consequently, the local sensitivity collinearity is an intrinsic bulk invariant that is completely unaffected by boundary cooling: across three decades of Biot numbers ($Bi in [0.001, 0.5]$), the correlation coefficient remains $rho = -1.0000000000$ ($|1+rho| <= 2.22 times 10^(-16)$), the residual norm satisfies $R_J tilde 10^(-9)$, and the 2-parameter Fisher condition number remains at the floating-point singularity floor ($tilde 10^(17)$). In a 3-parameter estimation framework $(tau_q, kappa^2, Bi)$, singular value decomposition reveals that the convective cooling parameter is cleanly identifiable ($sigma_1 / sigma_2 in [2.34, 4.90]$), yet the null space vector $(1, alpha_0, 0)^top$ with singular value $sigma_3 tilde 10^(-8)$ remains strictly unregularized. The mathematical proof and numerical solvers are certified via dual benchmarks: matching exact de Hoog Laplace-domain transfer function inversions ($L_infinity < 1.02 times 10^(-5)$) and the classical Cowan (1963) transcendental eigenvalue Fourier limit. These findings demonstrate that standard boundary heat-loss corrections cannot resolve the GK parameter identifiability degeneracy, and alternative regularization strategies must be sought.
  ]
  #v(0.8em)
  #text(size: 9.5pt)[
    *Keywords:* Guyer--Krumhansl heat conduction; Laser flash method; Boundary heat loss; Parameter identifiability; Fourier resonance; Sensitivity analysis.
  ]
]

#v(1.5em)

= 1. Introduction

The laser flash method, standardized in ASTM E1461 and originally formulated by Parker et al. (1961), represents the standard experimental technique for measuring thermal diffusivity and non-Fourier conduction parameters in advanced solids, thin films, and micro-architectured materials. While classical analysis relies on Fourier's law of diffusion, modern thermal engineering across micro- and nano-scale devices frequently encounters regimes where the phonon mean free path and relaxation times cannot be neglected. Under such conditions, hydrodynamic and non-local phonon transport is accurately described by the Guyer--Krumhansl (GK) equation (Guyer & Krumhansl 1966, Kovács 2018, Sellitto et al. 2025).

The GK model extends the classical Cattaneo--Vernotte hyperbolic equation by introducing a Laplacian term in the heat flux vector, capturing non-local phonon scattering and vorticity (Ván et al. 2017, Zhu et al. 2017):
$ tau_q (partial bold(q)) / (partial t) + bold(q) + lambda_0 grad T - kappa^2 grad^2 bold(q) = bold(0), $
where $tau_q$ is the flux relaxation time, $lambda_0$ is the intrinsic thermal conductivity, and $kappa^2$ is the non-local mean-free-path square parameter. When coupled with the conservation of energy, the non-dimensional system is governed by the resonance ratio:
$ B = kappa^2 / (alpha_0 tau_q), $
where $alpha_0 = lambda_0 / (rho c)$ is the baseline thermal diffusivity.

In a recent precursor computational study on idealized, adiabatic laser flash testing, an identifiability singularity was observed at the special ratio $B = 1$: the bulk transfer function collapses to a purely diffusive Helmholtz operator, resulting in an exact sensitivity collinearity:
$ (partial T) / (partial tau_q) = -alpha_0 (partial T) / (partial kappa^2). $
Under this condition, the $2 times 2$ Fisher Information Matrix (FIM) corresponding to the parameters $(tau_q, kappa^2)$ possesses a rank of 1, rendering individual parameter extraction impossible from rear-face temperature measurements alone.

In actual laboratory experiments, however, perfectly adiabatic conditions never exist. As first established in the classical foundations by Cowan (1963) and Cape and Lehman (1963), high-temperature and thin-slab laser flash measurements are subject to inevitable convective and radiative surface cooling. These boundary losses produce a pronounced temperature decay (cooling tail) after the initial rise, which experimentalists routinely fit to determine effective Biot numbers ($Bi = h L / lambda_0$). 

This physical reality raises a fundamental question: _Does the presence of boundary convective and radiative heat loss break the Fourier-resonance parameter singularity between $tau_q$ and $kappa^2$? Or is the Fourier-resonance sensitivity collinearity an intrinsic bulk property that remains strictly invariant to boundary cooling?_

In this work, we resolve this question definitively through analytical derivation and comprehensive numerical simulations. We formulate the coupled 1D Guyer--Krumhansl equation with front and rear Robin boundary conditions and prove analytically that at $B = 1$, the GK solution collapses identically to the classical Fourier heat conduction problem with convective heat loss. We systematically examine the parameter sensitivity, singular spectrum, and condition numbers across three orders of magnitude in Biot number ($Bi in [0.001, 0.5]$), demonstrating that boundary cooling cannot lift the local sensitivity singularity. Dual validation against analytical Laplace inversion and the classical Cowan (1963) transcendental benchmark certifies the mathematical and physical findings.

= 2. Mathematical Formulation

== 2.1 Dimensional Boundary-Value Problem

Consider a solid specimen of thickness $L$, initially at uniform ambient temperature $T_0$. At time $t = 0$, the front face ($x = 0$) is irradiated by a laser pulse delivering heat flux $q_("laser")(t)$, while both front and rear surfaces exchange heat with the surrounding environment via linearized convection and radiation with effective heat transfer coefficients $h_0$ and $h_L$.

The dimensional 1D governing equations are:
$ rho c (partial T) / (partial t) + (partial q) / (partial x) = 0, $
$ tau_q (partial q) / (partial t) + q + lambda_0 (partial T) / (partial x) - kappa^2 (partial^2 q) / (partial x^2) = 0, $
subject to the Robin boundary conditions:
$ q(0, t) = q_("laser")(t) - h_0 [T(0, t) - T_0], $
$ q(L, t) = h_L [T(L, t) - T_0], $
and quiescent initial conditions:
$ T(x, 0) = T_0, quad q(x, 0) = 0. $

== 2.2 Non-Dimensional Scaling

We introduce standard dimensionless variables:
$ hat(x) = x / L, quad hat(t) = (alpha_0 t) / L^2, quad theta = (T - T_0) / (Delta T_("ref")), quad hat(q) = q / q_("max"), $
where $Delta T_("ref") = (q_("max") t_p) / (rho c L)$, $tau_Delta = (alpha_0 t_p) / L^2$, $hat(tau)_q = (alpha_0 tau_q) / L^2$, $hat(kappa)^2 = kappa^2 / L^2$, and the Biot numbers are defined as:
$ Bi_0 = (h_0 L) / lambda_0, quad Bi_L = (h_L L) / lambda_0. $

Dropping hats for brevity, the dimensionless system is:
$ tau_Delta (partial theta) / (partial t) + (partial q) / (partial x) = 0, $
$ tau_q (partial q) / (partial t) + q + tau_Delta (partial theta) / (partial x) - kappa^2 (partial^2 q) / (partial x^2) = 0, $
with boundary conditions:
$ q(0, t) = q_("pulse")(t) - tau_Delta Bi_0 theta(0, t), $
$ q(1, t) = tau_Delta Bi_L theta(1, t), $
where $q_("pulse")(t) = 1 - cos(2 pi t / tau_Delta)$ for $0 <= t <= tau_Delta$, and $q_("pulse")(t) = 0$ for $t > tau_Delta$.

= 3. Analytical Invariance Theorem

== 3.1 Laplace-Domain Representation

Applying the Laplace transform $macron(theta)(x, s) = cal(L){theta(x, t)}$ and $macron(q)(x, s) = cal(L){q(x, t)}$:
$ (d macron(q)) / (d x) = -tau_Delta s macron(theta)(x, s), $
$ (1 + tau_q s) macron(q) - kappa^2 (d^2 macron(q)) / (d x^2) = -tau_Delta (d macron(theta)) / (d x). $
Differentiating with respect to $x$ and substituting yields the Helmholtz equation for temperature:
$ (d^2 macron(theta)) / (d x^2) - m^2(s) macron(theta) = 0, $
where the propagation parameter $m(s)$ is:
$ m(s) = sqrt((s(1 + tau_q s)) / (1 + kappa^2 s)). $
Because the spatial dependence of all modes is $exp(plus.minus m x)$, the heat flux satisfies $d^2 macron(q) / d x^2 = m^2(s) macron(q)$. Substituting this yields the dynamic flux-gradient relationship:
$ macron(q)(x, s) = -tau_Delta mu(s) (d macron(theta)) / (d x), quad "with" quad mu(s) equiv (1 + kappa^2 s) / (1 + tau_q s). $

== 3.2 Proof of Theorem 1 (Heat-Loss Invariance)

*Theorem 1.* _Let $B equiv kappa^2 / (alpha_0 tau_q) = 1$. Then for arbitrary Robin boundary parameters $Bi_0, Bi_L >= 0$, arbitrary pulse excitation $q_("pulse")(t)$, all spatial locations $x in [0, 1]$, and all times $t >= 0$, the Guyer--Krumhansl temperature field is identical to the classical Fourier heat conduction field with the same boundary heat losses:_
$ theta_("GK")(x, t; tau_q, kappa^2, Bi_0, Bi_L)|_(B=1) equiv theta_("Fourier")(x, t; Bi_0, Bi_L). $

_Proof._ In dimensionless variables, $alpha_0 = 1$. The resonance condition $B = 1$ implies $kappa^2 = tau_q$. Substituting this identity into the dynamic mobility:
$ mu(s) = (1 + tau_q s) / (1 + tau_q s) equiv 1. $
Similarly, substituting $kappa^2 = tau_q$ into the propagation parameter $m(s)$:
$ m(s) = sqrt((s(1 + tau_q s)) / (1 + tau_q s)) equiv sqrt(s). $
Consequently, the governing Helmholtz equation reduces to:
$ (d^2 macron(theta)) / (d x^2) - s macron(theta) = 0, $
and the boundary conditions become:
$ -tau_Delta (d macron(theta)) / (d x)|_(x=0) + tau_Delta Bi_0 macron(theta)(0, s) = macron(q)_("pulse")(s), $
$ -tau_Delta (d macron(theta)) / (d x)|_(x=1) - tau_Delta Bi_L macron(theta)(1, s) = 0. $
This boundary-value problem is formally identical to classical Fourier heat conduction with surface convection $Bi_0, Bi_L$. By uniqueness of the solution to the linear Helmholtz two-point boundary-value problem, $macron(theta)_("GK")(x, s)|_(B=1) equiv macron(theta)_("Fourier")(x, s)$. Taking the inverse Laplace transform establishes the theorem for all $t >= 0$ and $x in [0, 1]$. $square$

== 3.3 Fisher Information Matrix and Null Space Structure

Differentiating the identity in Theorem 1 along the line $kappa^2 = alpha_0 tau_q$ immediately yields:
$ (partial theta) / (partial tau_q)|_(B=1) + alpha_0 (partial theta) / (partial kappa^2)|_(B=1) = 0 quad ==> quad bold(J)_(tau_q)(t) = -alpha_0 bold(J)_(kappa^2)(t). $

For a simultaneous 3-parameter estimation problem $bold(theta) = (tau_q, kappa^2, Bi)^top$, the sensitivity Jacobian is $bold(J) = [bold(J)_(tau_q) quad bold(J)_(kappa^2) quad bold(J)_(Bi)]$. The Jacobian admits an exact null vector:
$ bold(v)_("null") = mat(alpha_0; 1; 0), quad "such that" quad bold(J) bold(v)_("null") = bold(0). $
The corresponding Fisher Information Matrix $bold(F) = bold(J)^top bold(J)$ has eigenvalues $lambda_1 > 0, lambda_2 > 0, lambda_3 equiv 0$. Hence, $"rank"(bold(F)) = 2 < 3$, and $"cond"(bold(F)) = infinity$.

= 4. Numerical Architecture and Dual Validation

== 4.1 Numerical Scheme

The coupled system is solved on a staggered spatial grid with cell centers $x_(i+1/2)$ for $theta$ and cell interfaces $x_i$ for $q$. Boundary surface temperatures are extrapolated via second-order one-sided stencils: $theta(0) = 3/2 theta_1 - 1/2 theta_2$ and $theta(1) = 3/2 theta_N - 1/2 theta_(N-1)$. The resulting stiff differential-algebraic system is integrated in time using a Backward Differentiation Formula (BDF) solver with adaptive time stepping ($"rtol" = 10^(-10)$, $"atol" = 10^(-12)$).

== 4.2 Dual Validation Benchmarks

To ensure complete scientific rigor, the computational model is validated against two independent analytical benchmarks:
1. *Analytical Laplace Transfer Function:* The closed-form rear-face temperature transform:
   $ macron(theta)(1, s) = (m(s) mu(s)) / (tau_Delta Delta(s)) macron(q)_("pulse")(s), $
   where $Delta(s) = [m^2 mu^2 + Bi_0 Bi_L] sinh(m) + m mu (Bi_0 + Bi_L) cosh(m)$, inverted via the de Hoog algorithm to 25-digit precision.
2. *Cowan (1963) Fourier Benchmark:* In the singular limit $tau_q -> 0, kappa^2 -> 0$, the PDE solution is compared directly against the Cowan transcendental eigenvalue series with convective heat loss.

#align(center)[
  #table(
    columns: (1.5fr, 1.5fr, 1.5fr, 1.5fr, 1.5fr, 1fr),
    stroke: 0.5pt + luma(180),
    fill: (col, row) => if row == 0 { rgb(235, 240, 248) } else { none },
    inset: (x: 7pt, y: 6pt),
    [*Biot Number $Bi$*], [*Peak $theta_("PDE")$*], [*Peak $theta_("Laplace")$*], [*$L_infinity$ Error*], [*$L_2$ Error*], [*Status*],
    [0.000 (Adiabatic)], [0.999990], [1.000000], [$1.02 times 10^(-5)$], [$3.74 times 10^(-6)$], [*PASS*],
    [0.010], [0.985420], [0.985430], [$1.01 times 10^(-5)$], [$3.67 times 10^(-6)$], [*PASS*],
    [0.050], [0.930472], [0.930481], [$9.53 times 10^(-6)$], [$3.42 times 10^(-6)$], [*PASS*],
    [0.100], [0.865931], [0.865939], [$8.90 times 10^(-6)$], [$3.15 times 10^(-6)$], [*PASS*],
    [0.200], [0.758804], [0.758811], [$7.75 times 10^(-6)$], [$2.71 times 10^(-6)$], [*PASS*],
    [0.500], [0.540412], [0.540417], [$5.01 times 10^(-6)$], [$1.82 times 10^(-6)$], [*PASS*]
  )
]
#align(center)[*Table 1:* Dual validation benchmark results between PDE solver ($N_x = 400$) and analytical Laplace inversion.]

#v(1em)

#figure(
  image("../figures/fig5_validation_dual_benchmarks.png", width: 95%),
  caption: [(a) Discrepancy between time-domain PDE solver and exact de Hoog Laplace inversion across Biot numbers. (b) Spatial grid refinement demonstrating asymptotic second-order accuracy ($p = 2.07 -> 2.32$).]
)

= 5. Results and Discussion

== 5.1 Thermal Response and Cooling Tails

#figure(
  image("../figures/fig1_heatloss_temperature_response.png", width: 95%),
  caption: [(a) Rear-face temperature histories $theta(1, t)$ for varying Biot numbers $Bi in {0.00, 0.05, 0.20}$ demonstrating peak suppression and cooling tails. (b) Numerical discrepancy between GK ($B=1$) and Cowan Fourier heat conduction solutions, confirming mathematical equivalence.]
)

Figure 1(a) displays the rear-face temperature histories $theta(1, t)$ for Biot numbers ranging from adiabatic ($Bi = 0$) to intense cooling ($Bi = 0.5$). As expected, boundary heat loss suppresses the peak rear-face temperature rise from $1.000$ to $0.540$ and induces a rapid exponential cooling tail. Crucially, as shown in Figure 1(b), the difference between the non-Fourier GK solution at $B = 1$ and the classical Cowan Fourier solution remains bounded below $10^(-5)$ across all time and all Biot numbers, verifying Theorem 1.

== 5.2 Persistent Sensitivity Collinearity

#figure(
  image("../figures/fig2_sensitivity_profiles_collinearity.png", width: 95%),
  caption: [(a) Front- and rear-face sensitivity profiles $bold(J)_(tau_q)(t)$ and $-alpha_0 bold(J)_(kappa^2)(t)$ for adiabatic and convective cooling, displaying exact point-by-point overlay. (b) Independent sensitivity profile $bold(J)_(Bi)(t) = partial theta / partial Bi$ associated with the cooling tail.]
)

Figure 2(a) illustrates the time-resolved sensitivity profiles $bold(J)_(tau_q)(t) = partial theta / partial tau_q$ and $-alpha_0 bold(J)_(kappa^2)(t) = -alpha_0 partial theta / partial kappa^2$ for both adiabatic ($Bi = 0$) and convective ($Bi = 0.2$) cases. In both regimes, the two curves fall precisely onto each other with zero visible separation at any time instant. 

Conversely, Figure 2(b) plots the sensitivity with respect to the Biot number, $bold(J)_(Bi)(t) = partial theta / partial Bi$. Unlike the non-Fourier parameters, $bold(J)_(Bi)$ exhibits a distinctly different temporal profile characterized by a sustained negative tail extending well into the cooling phase.

== 5.3 Invariance Across Biot Numbers

#align(center)[
  #table(
    columns: (0.9fr, 1.4fr, 1.1fr, 1.1fr, 1fr, 1fr, 1.1fr, 1fr, 1.3fr),
    stroke: 0.5pt + luma(180),
    fill: (col, row) => if row == 0 { rgb(235, 240, 248) } else { none },
    inset: (x: 5pt, y: 5pt),
    [*$Bi$*], [*Correlation $rho$*], [*$|1+rho|$*], [*Residual $R_J$*], [*$sigma_1$*], [*$sigma_2$*], [*$sigma_3$*], [*$sigma_1/sigma_2$*], [*$"cond"(F_(3 times 3))$*],
    [0.000], [-1.0000000000], [$1.11 times 10^(-16)$], [$5.37 times 10^(-9)$], [31.82], [13.57], [$7.37 times 10^(-8)$], [2.34], [$1.86 times 10^(17)$],
    [0.001], [-1.0000000000], [$1.11 times 10^(-16)$], [$5.37 times 10^(-9)$], [31.81], [13.55], [$7.35 times 10^(-8)$], [2.35], [$1.87 times 10^(17)$],
    [0.005], [-1.0000000000], [$0.00 times 10^(00)$], [$5.38 times 10^(-9)$], [31.75], [13.44], [$7.36 times 10^(-8)$], [2.36], [$1.86 times 10^(17)$],
    [0.010], [-1.0000000000], [$2.22 times 10^(-16)$], [$5.39 times 10^(-9)$], [31.68], [13.30], [$7.36 times 10^(-8)$], [2.38], [$1.85 times 10^(17)$],
    [0.050], [-1.0000000000], [$0.00 times 10^(00)$], [$5.41 times 10^(-9)$], [31.13], [12.27], [$7.25 times 10^(-8)$], [2.54], [$1.84 times 10^(17)$],
    [0.100], [-1.0000000000], [$1.11 times 10^(-16)$], [$5.48 times 10^(-9)$], [30.47], [11.11], [$7.16 times 10^(-8)$], [2.74], [$1.81 times 10^(17)$],
    [0.200], [-1.0000000000], [$1.11 times 10^(-16)$], [$8.11 times 10^(-9)$], [29.27], [9.15], [$1.10 times 10^(-7)$], [3.20], [$7.05 times 10^(16)$],
    [0.500], [-1.0000000000], [$1.11 times 10^(-16)$], [$5.81 times 10^(-9)$], [26.25], [5.35], [$6.50 times 10^(-8)$], [4.90], [$1.63 times 10^(17)$]
  )
]
#align(center)[*Table 2:* Systematic parameter sweep across Biot numbers at Fourier resonance ($B = 1.0$): Collinearity metrics, singular spectrum, and condition numbers.]

#v(1em)

#figure(
  image("../figures/fig3_invariance_metrics_vs_biot.png", width: 95%),
  caption: [(a) Collinearity metrics $log_10(R_J)$ and $log_10(|1+rho|)$ as functions of Biot number, demonstrating exact horizontal invariance. (b) Condition numbers $"cond"(F_(2 times 2))$ and $"cond"(F_(3 times 3))$ pinned at the numerical singularity floor $tilde 10^(17)$.]
)

Across all Biot numbers, $rho = -1.0000000000$, with the defect $|1+rho|$ bounded by machine epsilon ($2.22 times 10^(-16)$). The residual norm remains flat at $R_J approx (5.37 - 8.11) times 10^(-9)$, representing the truncation error of the central finite-difference approximation. Consequently, as shown in Figure 3, the condition number of the $2 times 2$ Fisher matrix remains pinned at the machine-singularity limit $tilde 10^(17)$.

== 5.4 Singular Spectrum and Resonance Canyon

#figure(
  image("../figures/fig4_singular_spectrum_and_canyon.png", width: 95%),
  caption: [(a) SVD spectrum $(sigma_1, sigma_2, sigma_3)$ across Biot numbers, showing clean isolation of the null singularity $sigma_3 tilde 10^(-8)$. (b) The Fourier-resonance singularity canyon centered at $B = 1.0$, demonstrating persistent collinearity across all Biot numbers.]
)

In the full 3-parameter system $(tau_q, kappa^2, Bi)$, singular value decomposition reveals the underlying structural geometry:
1. The leading singular value $sigma_1 in [26.2, 31.8]$ corresponds to the principal thermal diffusion mode.
2. The second singular value $sigma_2 in [5.35, 13.57]$ corresponds directly to the convective cooling tail. The condition ratio of this observable subspace is $sigma_1 / sigma_2 in [2.34, 4.90]$, indicating that the Biot number $Bi$ can be estimated with high statistical precision.
3. The third singular value $sigma_3 tilde 10^(-8)$ corresponds strictly to the null vector $bold(v)_("null") = (1, alpha_0, 0)^top$. 

As illustrated in Figure 4(a), boundary heat loss populates an entirely orthogonal dimension in parameter space without projecting onto the null vector. 

Finally, Figure 4(b) displays the condition number $"cond"(F_(2 times 2))$ as a function of the resonance ratio $B in [0.2, 2.0]$. Away from resonance (e.g., $B = 0.5$ or $B = 1.5$), the condition number drops sharply to moderate values ($tilde 10^2$), where heat loss causes minor quantitative shifts. However, at $B = 1.0$, an ultra-sharp singularity canyon occurs where $"cond"(F)$ spikes to $10^(17)$, regardless of whether $Bi = 0$, $Bi = 0.05$, or $Bi = 0.20$.

= 6. Conclusions

In this study, we investigated the effect of convective and radiative boundary heat loss on the Guyer--Krumhansl parameter identifiability singularity at Fourier resonance ($B = 1$). Through analytical proof in the Laplace domain and high-order numerical simulations across three decades of Biot numbers ($Bi in [0.001, 0.5]$), we established the following conclusions:
1. *Invariance Theorem:* At $B equiv kappa^2 / (alpha_0 tau_q) = 1$, the Guyer--Krumhansl temperature field collapses identically to the classical Fourier heat conduction solution with the corresponding Robin boundary conditions.
2. *Persistence of Sensitivity Singularity:* Boundary heat loss does not break the local sensitivity collinearity $partial T / partial tau_q = -alpha_0 partial T / partial kappa^2$. Across all tested Biot numbers, the correlation coefficient remains $rho = -1.0000000000$, and the condition number of the Fisher information matrix remains at the floating-point singularity floor ($tilde 10^(17)$).
3. *Subspace Separation:* In a simultaneous 3-parameter estimation framework $(tau_q, kappa^2, Bi)$, the cooling parameter $Bi$ is cleanly identifiable from the cooling tail with an observable condition ratio $sigma_1 / sigma_2 in [2.34, 4.90]$. However, the null space $(1, alpha_0, 0)^top$ remains strictly unregularized.
4. *Experimental Implications:* Standard laser flash heat-loss correction procedures (such as Cowan or Cape--Lehman methods) cannot resolve the structural identifiability degeneracy in materials near Fourier resonance. Experimentalists must instead employ strategies that perturb the bulk transport condition, such as varying sample thickness to drive the effective non-dimensional ratio off-resonance, performing multi-thickness joint inversions, or operating in high-fluence nonlinear thermal regimes.

= References

- ASTM International, ASTM E1461-13: Standard Test Method for Thermal Diffusivity by the Flash Method, ASTM International, West Conshohocken, PA, 2013.
- J. A. Cape, G. W. Lehman, Temperature and finite pulse-time effects in the flash method for measuring thermal diffusivity, Journal of Applied Physics 34 (1963) 1909–1913.
- R. D. Cowan, Pulse method of measuring thermal diffusivity at high temperatures, Journal of Applied Physics 34 (1963) 926–927.
- F. R. de Hoog, J. H. Knight, A. N. Stokes, An improved method for numerical inversion of Laplace transforms, SIAM Journal on Scientific and Statistical Computing 3 (1982) 357–366.
- R. A. Guyer, J. A. Krumhansl, Solution of the Boltzmann equation for phonons, Physical Review 148 (1966) 766–778.
- R. A. Guyer, J. A. Krumhansl, Thermal conductivity, second sound, and phonon hydrodynamic phenomena in nonmetallic crystals, Physical Review 148 (1966) 778–788.
- R. Kovács, Analytic solution of the Guyer–Krumhansl equation for laser flash experiments, International Journal of Heat and Mass Transfer 127 (2018) 631–636.
- W. J. Parker, R. J. Jenkins, C. P. Butler, G. L. Abbott, Flash method of determining thermal diffusivity, heat capacity, and thermal conductivity, Journal of Applied Physics 32 (1961) 1679–1684.
- A. Sellitto, I. Carlomagno, V. A. Cimmelli, Nonlinear Guyer–Krumhansl equation and boundary conditions in nanolayers with heat-flux dependent mean free path, Zeitschrift für angewandte Mathematik und Physik 76 (2025) 1–18.
- A. Talbot, The accurate numerical inversion of Laplace transforms, IMA Journal of Applied Mathematics 23 (1979) 97–120.
- P. Ván, R. Kovács, T. Fülöp, Galilean relativistic fluid mechanics, Continuum Mechanics and Thermodynamics 29 (2017) 585–601.
- K. Zhu, Z. Guo, M. Wang, Nonlocal effects and slip heat flow in nanolayers using modified Guyer–Krumhansl equation, Scientific Reports 7 (2017) 10416.
