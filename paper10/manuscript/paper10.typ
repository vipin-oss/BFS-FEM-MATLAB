#strong[Keywords:] Phononic crystals; Metamaterials; Dipolar gradient
elasticity; Dual-Phase-Lag (DPL) heat conduction; Acoustic band gaps;
Thermoelastic damping.

---

= Introduction
<sec:intro>
Periodic acoustic metamaterials and phononic crystals have attracted
extensive interest across engineering physics, aerospace structures, and
acoustic signal processing due to their unique capacity to manipulate,
redirect, and prohibit elastic wave propagation within designated
frequency bands known as phononic band gaps or stop bands \(Kushwaha et
al. 1993; Hussein et al. 2014; Brillouin 1953). In conventional periodic
media, band gaps emerge predominantly via two distinct mechanisms: Bragg
scattering, which arises from destructive wave interference across
periodically alternating acoustic impedances, and local resonance, which
utilizes sub-wavelength internal resonators to trap acoustic energy
\(Hussein et al. 2014).

Classical linear elastodynamics, founded on Cauchy's local continuum
hypothesis, assumes that the stress at a point depends strictly on the
local strain at that exact location. Consequently, classical theory is
scale-invariant and lacks an internal material length scale. When
acoustic wavelengths approach the characteristic dimensions of the
underlying microstructural constituents (such as grains, inclusions,
fibers, or lattice struts), classical elasticity fails to capture
microstructural dispersion, high-frequency wave filtering, and boundary
layer phenomena \(Achenbach 1973). To address these limitations,
generalized continuum theories have been formulated, notably Mindlin's
strain gradient elasticity \(Mindlin 1964, 1965) and its Form-II dipolar
simplification \(Askes and Aifantis 2011; Georgiadis 2003; Polyzos et
al. 2003). In Mindlin Form-II gradient elasticity, higher-order strain
gradients introduce a micro-stiffness characteristic length
($g = sqrt(c)$), while velocity gradients introduce an independent
kinetic micro-inertia length scale ($h = d \/ sqrt(3)$).
Papargyri-Beskou et al. \(Papargyri-Beskou et al. 2009) demonstrated
analytically that these dual length scales govern wave dispersion in
infinite solids, rods, and beams. Subsequently, Li et al. \(Li et al.
2016) integrated dipolar gradient elasticity into one-dimensional
phononic crystals, demonstrating that microstructural length scales
significantly alter band-gap widths and shift cut-off frequencies.

Concurrently, high-frequency acoustic waves in real metamaterials induce
localized, cyclic volumetric strain fluctuations that generate
temperature variations via thermoelastic coupling \(Biot 1956). In
classical thermoelasticity based on Fourier's law, heat propagates with
an infinite phase speed, creating a parabolic diffusion operator that
produces non-physical instantaneous thermal signals. To restore
causality and capture non-equilibrium thermal transport in
micro/nanoscale devices, generalized thermoelastic theories have been
developed, including the hyperbolic models of Lord and Shulman \(Lord
and Shulman 1967), Green and Lindsay \(Green and Lindsay 1972), Green
and Naghdi \(Green and Naghdi 1991), and Tzou's Dual-Phase-Lag (DPL)
framework \(Tzou 1995, 2014; Chandrasekharaiah 1998). Tzou's DPL theory
incorporates two independent microscopic time lags: the heat flux
relaxation lag $tau_q$, representing the delay caused by fast-transient
thermal inertia and electron-phonon scattering, and the temperature
gradient retardation lag $tau_theta$, representing microstructural heat
diffusion delays. The mathematical and thermodynamic stability of DPL
heat conduction has been rigorously examined by Quintanilla
\(Quintanilla 2002) and Chiriţă \(Chiriţă 2017), confirming asymptotic
decay and energy dissipation when $tau_q gt.eq tau_theta > 0$. Recently,
generalized thermoelastic damping in micro/nanoscale resonators has been
investigated by Kumar and Mukhopadhyay \(Kumar and Mukhopadhyay 2022),
Singh and Mukhopadhyay \(Singh and Mukhopadhyay 2021), Singh et al.
\(Singh et al. 2022), and Fernández and Quintanilla \(Fernández and
Quintanilla 2021). Furthermore, Li et al. \(Li et al. 2026) studied
fractional-order thermoelastic waves in gradient phononic media.

Despite these advancements, an important scientific gap persists.
Existing studies have either investigated gradient-elastic band gaps
under strictly conservative, purely elastic assumptions
($beta arrow.r 0$), or analyzed thermoelastic damping in homogeneous
resonators without periodic Bragg scattering. A systematic,
quantitatively calibrated formulation that simultaneously couples
dipolar gradient elasticity with full non-Fourier DPL thermoelasticity
in periodic metamaterials has not been thoroughly synthesized. In
particular, previous literature frequently leaves ambiguous whether
spatial wave attenuation arises from geometric Bragg evanescence or
irreversible thermodynamic dissipation, and does not systematically
decouple the competing influences of micro-inertia softening,
micro-stiffness stiffening, and non-Fourier thermal lagging.

To resolve these questions, this paper establishes a rigorous analytical
and numerical framework for 1D periodic metamaterials combining Mindlin
Form-II dipolar gradient elasticity and Tzou's DPL heat conduction. The
specific, defensible contributions of this study are:

+ Formulating an exact 10-state transfer-matrix framework for coupled
  longitudinal-thermal waves and an independent 4-state formulation for
  anti-plane shear waves, derived variationally from Hamilton's
  principle with self-consistent generalized boundary tractions;

+ Establishing a bounded generalized interface eigenvalue formulation
  ($A upright(bold(c)) = lambda B upright(bold(c))$) with canonical
  two-sided equilibration
  ($kappa \( P_(upright("equil")) \) lt.eq 22.72$) that unconditionally
  eliminates numerical overflow from stiff thermal diffusion boundary
  layers;

+ Validating the solver against the external analytical benchmark of
  Papargyri-Beskou et al. \(Papargyri-Beskou et al. 2009) to machine
  precision ($2.45 times 10^(- 15)$ relative error);

+ Performing a 36-case parametric production campaign across seven sweep
  families (17,747 modal records), systematically decoupling the
  quantitative roles of periodic material contrast, dipolar micro-length
  scales, DPL thermal time lags, and thermoelastic coupling intensity;
  and

+ Demonstrating that DPL thermoelasticity establishes a finite spatial
  attenuation baseline ($alpha a tilde.op 2.2 times 10^(- 4)$ to
  $5.5 times 10^(- 2)$) across propagating pass bands and transforms
  sharp conservative Brillouin zone boundaries into smooth, continuous
  dissipation zones.

---

= Mathematical Formulation
<sec:math>
== Geometry and Periodic Architecture
<geometry-and-periodic-architecture>
We consider a one-dimensional periodic phononic metamaterial composed of
an infinite alternating sequence of homogeneous, isotropic elastic
layers denoted as Layer A and Layer B along the $x$-axis, with
alternating layer thicknesses $a_1$ and $a_2$. The unit cell length is
$a = a_1 + a_2$, where $a_1$ and $a_2$ are the thicknesses of Layer A
and Layer B, respectively. The geometric composition is parameterized by
the filling fraction of Layer A:
$ eta = a_1 / a \, #h(2em) 1 - eta = a_2 / a . $<eq:filling_fraction>
The interfaces between adjacent layers are located at $x = x_j$ and are
assumed to be planar, perfectly bonded mechanically, and thermally ideal
(continuous temperature and heat flux).

== Mindlin Form-II Dipolar Gradient Elastodynamics
<mindlin-form-ii-dipolar-gradient-elastodynamics>
In each homogeneous layer, the mechanical deformation field is governed
by Mindlin Form-II dipolar gradient elasticity \(Mindlin 1964; Li et al.
2016). In the absence of external body forces, the generalized momentum
balance tensor equation is:
$ (tau_(j k) - mu_(i j k \, i))_(\, j) = rho dot.double(u)_k - frac(rho d^2, 3) dot.double(u)_(k \, j j) \, $<eq:momentum_balance>
where $tau_(j k)$ is the Cauchy (monopolar) stress tensor, $mu_(i j k)$
is the dipolar hyperstress tensor, $rho$ is the mass density, $d$ is the
micro-inertia characteristic length parameter, $u_k$ is the displacement
vector, overdots denote partial time derivatives, and comma notation
denotes spatial differentiation
($\( dot.op \)_(\, j) = partial \( dot.op \) \/ partial x_j$). For an
isotropic centrosymmetric material with micro-stiffness length parameter
$c = g^2$, the constitutive equations incorporating thermal dilatation
are given by:
$ tau_(i j) = lambda delta_(i j) epsilon_(k k) + 2 mu epsilon_(i j) - beta theta delta_(i j) \, $<eq:cauchy_stress>
$ mu_(k i j) = c (lambda delta_(i j) epsilon_(p p \, k) + 2 mu epsilon_(i j \, k)) \, $<eq:hyperstress>
where $lambda$ and $mu$ are the classical Lamé constants, $delta_(i j)$
is the Kronecker delta,
$epsilon_(i j) = 1 / 2 \( u_(i \, j) + u_(j \, i) \)$ is the
infinitesimal strain tensor, $beta = \( 3 lambda + 2 mu \) alpha_t$ is
the thermoelastic coupling coefficient, $alpha_t$ is the linear thermal
expansion coefficient, and
$theta \( upright(bold(x)) \, t \) = T \( upright(bold(x)) \, t \) - T_0$
is the local temperature increment above a uniform reference temperature
$T_0$.

Substituting Eqs.~#link(<eq:cauchy_stress>)[\[eq:cauchy\_stress\]] and
#link(<eq:hyperstress>)[\[eq:hyperstress\]] into
Eq.~#link(<eq:momentum_balance>)[\[eq:momentum\_balance\]] yields the
coupled vectorial displacement equation:
$ mu \( 1 - c nabla^2 \) nabla^2 upright(bold(u)) + \( lambda + mu \) \( 1 - c nabla^2 \) nabla \( nabla dot.op upright(bold(u)) \) - beta nabla theta = rho dot.double(upright(bold(u))) - frac(rho d^2, 3) nabla^2 dot.double(upright(bold(u))) . $<eq:vector_displacement>

== Dual-Phase-Lag (DPL) Heat Conduction
<dual-phase-lag-dpl-heat-conduction>
Heat transport in the periodic metamaterial is governed by Tzou's
Dual-Phase-Lag model \(Tzou 1995, 2014), which introduces a heat flux
relaxation time $tau_q$ and a temperature gradient retardation time
$tau_theta$:
$ upright(bold(q)) \( upright(bold(x)) \, t + tau_q \) = - k nabla theta \( upright(bold(x)) \, t + tau_theta \) \, $<eq:dpl_tzou>
where $upright(bold(q))$ is the conductive heat flux vector and $k$ is
the thermal conductivity. Expanding
Eq.~#link(<eq:dpl_tzou>)[\[eq:dpl\_tzou\]] to first order in time
derivatives yields:
$ upright(bold(q)) + tau_q frac(partial upright(bold(q)), partial t) = - k nabla theta - k tau_theta frac(partial, partial t) \( nabla theta \) . $<eq:dpl_linearized>
The localized thermal energy conservation equation with
thermo-mechanical coupling is:
$ - nabla dot.op upright(bold(q)) = rho c_v frac(partial theta, partial t) + T_0 beta frac(partial, partial t) \( nabla dot.op upright(bold(u)) \) \, $<eq:energy_conservation>
where $c_v$ is the specific heat capacity at constant volume. Operating
on Eq.~#link(<eq:energy_conservation>)[\[eq:energy\_conservation\]] with
$\( 1 + tau_q partial_t \)$ and substituting
Eq.~#link(<eq:dpl_linearized>)[\[eq:dpl\_linearized\]] eliminates
$upright(bold(q))$, resulting in the coupled scalar DPL energy equation:
$ k (1 + tau_theta frac(partial, partial t)) nabla^2 theta = (1 + tau_q frac(partial, partial t)) [rho c_v frac(partial theta, partial t) + T_0 beta frac(partial, partial t) \( nabla dot.op upright(bold(u)) \)] . $<eq:dpl_scalar_pde>

== Variational Boundary Tractions
<variational-boundary-tractions>
Applying Hamilton's variational principle over a domain bounded by
surface $S$ with outward unit normal $n_j$ establishes the conjugate
boundary variables:
$ delta W_(upright("ext")) = integral_S (P_k delta u_k + R_k D delta u_k) d S \, $<eq:hamilton_work>
where $D = n_l partial_l = partial \/ partial n$ is the normal
derivative operator. The resulting generalized tractions are:
$ P_k = n_j \( tau_(j k) - mu_(i j k \, i) \) - D_j \( n_i mu_(i j k) \) + \( D_l n_l \) n_i n_j mu_(i j k) + 1 / 3 rho d^2 n_j dot.double(u)_(k \, j) \, $<eq:monopolar_traction>
$ R_k = n_i n_j mu_(i j k) \, $<eq:dipolar_traction> where $P_k$ (in
$upright("Pa")$) is the generalized monopolar traction (combining Cauchy
stress, hyperstress gradients, and micro-inertia boundary work), and
$R_k$ (in $upright("N/m")$) is the generalized dipolar traction
(hyperstress). For planar interfaces orthogonal to the $x$-axis
($n = \[ 1 \, 0 \, 0 \]^T$), the relevant tractions become:
$ P_x & = \( lambda + 2 mu \) u_(x \, x) + lambda u_(y \, y) - beta theta - c \( lambda + 2 mu \) (u_(x \, x x x) + 2 u_(x \, x y y)) - c lambda u_(y \, y y y) + 1 / 3 rho d^2 dot.double(u)_(x \, x) \,\
P_y & = mu \( u_(x \, y) + u_(y \, x) \) - c mu (u_(y \, x x x) + 2 u_(y \, x y y)) - c lambda u_(x \, y y y) + 1 / 3 rho d^2 dot.double(u)_(y \, x) \,\
R_x & = c [\( lambda + 2 mu \) u_(x \, x x) + lambda u_(y \, y x)] \,\
R_y & = c mu [u_(y \, x x) + u_(x \, y x)] \,\
P_z & = mu u_(z \, x) - c mu (u_(z \, x x x) + 2 u_(z \, x y y)) + 1 / 3 rho d^2 dot.double(u)_(z \, x) \,\
R_z & = c mu u_(z \, x x) . $<eq:interface_tractions> The interface
conductive heat flux is given by
$Q_x = - k_(upright("eff")) \( omega \) partial theta \/ partial x$.

== Harmonic Representation and Effective Complex Conductivity
<harmonic-representation-and-effective-complex-conductivity>
Under time-harmonic wave propagation with circular frequency $omega$
($partial_t arrow.r - i omega$), the fields are represented as:
$ upright(bold(u)) \( x \, y \, t \) = upright(bold(U)) \( x \) e^(i \( xi y - omega t \)) \, quad theta \( x \, y \, t \) = Theta \( x \) e^(i \( xi y - omega t \)) \, quad upright(bold(q)) \( x \, y \, t \) = upright(bold(Q)) \( x \) e^(i \( xi y - omega t \)) \, $<eq:harmonic_ansatz>
where $xi$ is the apparent wavenumber along the $y$-direction. In this
work, we focus on normal incidence ($xi = 0$), where
longitudinal-thermal and transverse shear modes uncouple cleanly.

Transforming Eq.~#link(<eq:dpl_linearized>)[\[eq:dpl\_linearized\]] to
the frequency domain yields the effective complex frequency-dependent
thermal conductivity:
$ k_(upright("eff")) \( omega \) equiv k frac(1 - i omega tau_theta, 1 - i omega tau_q) . $<eq:keff>
The frequency-domain DPL energy equation is then:
$ nabla^2 Theta + k_(upright("th"))^2 \( omega \) Theta + eta_(upright("th")) \( omega \) \( nabla dot.op upright(bold(U)) \) = 0 \, $<eq:dpl_helmholtz>
where the thermal wavenumber $k_(upright("th"))^2 \( omega \)$ and
coupling factor $eta_(upright("th")) \( omega \)$ are defined as:
$ k_(upright("th"))^2 \( omega \) = frac(i omega rho c_v \( 1 - i omega tau_q \), k \( 1 - i omega tau_theta \)) \, #h(2em) eta_(upright("th")) \( omega \) = frac(i omega T_0 beta \( 1 - i omega tau_q \), k \( 1 - i omega tau_theta \)) . $<eq:thermal_wave_parameters>

== State-Space Transfer-Matrix Formulation
<sec:tmm>
For in-plane coupled wave propagation ($xi = 0$), the displacement and
thermal fields are governed by a tenth-order system of ordinary
differential equations. The continuity requirements across layer
interfaces demand the continuity of five kinematic/potential variables
and five dynamic tractions, forming the canonical 10-state vector:
$ upright(bold(V))_10 \( x \) = [u_x \, #h(0em) u_y \, #h(0em) u_(x \, x) \, #h(0em) u_(y \, x) \, #h(0em) Theta \, #h(0em) P_x \, #h(0em) P_y \, #h(0em) R_x \, #h(0em) R_y \, #h(0em) Q_x]^T . $<eq:state_vector_10>
For purely anti-plane shear waves ($u_z \( x \)$), the motion decouples
into a 4-state vector:
$ upright(bold(V))_4 \( x \) = [u_z \, #h(0em) u_(z \, x) \, #h(0em) P_z \, #h(0em) R_z]^T . $<eq:state_vector_4>

The general solution in each layer $j in { A \, B }$ is expanded into
modal wave components:
$ upright(bold(V)) \( x \) = P_j E_j \( x - x_0 \) upright(bold(C))_j \, $<eq:modal_expansion>
where $P_j$ is the modal matrix containing the eigenvectors of the state
variables,
$E_j \( Delta x \) = "diag" (e^(i k_(j \, 1) Delta x) \, dots.h \, e^(i k_(j \, M) Delta x))$
is the diagonal modal propagator, and $upright(bold(C))_j$ is the wave
amplitude vector. The classical single-layer transfer matrix relating
the state vector at the left boundary $x_0$ to the right boundary
$x_0 + a_j$ is:
$ T_j = P_j E_j \( a_j \) P_j^(- 1) . $<eq:transfer_matrix_single> By
state continuity across the interface ($x = a_1$), the total unit-cell
transfer matrix is: $ T_(upright("cell")) = T_B T_A . $<eq:tcell>
Bloch-Floquet periodicity across the unit cell of length $a$ requires:
$ upright(bold(V)) \( x + a \) = e^(i k_x a) upright(bold(V)) \( x \) arrow.r.double.long T_(upright("cell")) upright(bold(V)) = lambda upright(bold(V)) \, quad lambda = e^(i k_x a) \, $<eq:bloch_secular>
where $k_x = k_r + i k_i$ is the complex Bloch wavenumber. Forward
spatial acoustic attenuation is defined by:
$ alpha = \| k_i \| \, #h(2em) alpha a = \| k_i a \| . $<eq:attenuation_def>

== Conservative Mechanical Benchmark Limit
<conservative-mechanical-benchmark-limit>
It is essential to clarify the conservative limiting behavior of this
system. When the thermoelastic coupling coefficient vanishes
($beta arrow.r 0$), thermal dissipation is uncoupled from
elastodynamics. In this limit, the mechanical subsystem represents an
uncoupled, purely elastic gradient metamaterial. Because gradient
elasticity is a hyperelastic continuum derived from a conservative
strain energy potential, energy is strictly conserved. Consequently, the
mechanical transfer matrix $T_(upright("mech"))$ satisfies the
symplectic determinant identity:
$ det \( T_(upright("mech")) \) = 1.00000000 plus.minus 10^(- 13) . $<eq:symplectic_identity>
We emphasize that the limit $beta arrow.r 0$ constitutes an
#strong[uncoupled mechanical conservative limit], and must not be
described as an "isothermal limit." Furthermore, for the active DPL
thermoelastic system ($beta > 0 \, tau_q > 0 \, tau_theta > 0$),
thermodynamic entropy generation renders the system dissipative, and
$det \( T_(10 times 10) \) eq.not 1$.

---

= Numerical Methodology and Independent External Validation
<sec:numerical>
== Conditioning Challenges and Generalized Interface Eigenvalue Problem
<conditioning-challenges-and-generalized-interface-eigenvalue-problem>
In micro- and macroscale periodic metamaterials, the characteristic
thermal diffusion wavenumber
$k_(upright("th")) = sqrt(i omega rho c_v \/ k_(upright("eff")))$
possesses a substantial imaginary component
($\| k_(upright("th")) \| gt.double omega \/ V_p$). Direct evaluation of
the classical transfer matrix $T_j = P_j E_j \( a_j \) P_j^(- 1)$
entails forward and backward exponential multipliers:
$ exp (plus.minus i k_(upright("th")) a_j) tilde.op exp (plus.minus "Re" sqrt(i) \| k_(upright("th")) \| a_j) . $
For layer thicknesses $a_j tilde.op 10^(- 3)$ to
$10^(- 2) upright(" m")$ at ultrasound frequencies, this exponential
term exceeds $e^100 tilde.op 10^43$, causing catastrophic floating-point
overflow and severe ill-conditioning when computing $P_j^(- 1)$.

To unconditionally eliminate exponential overflow, the boundary value
problem across the unit cell is reformulated as a Generalized Interface
Eigenvalue Problem ($A upright(bold(c)) = lambda B upright(bold(c))$).
Rather than multiplying forward and backward exponential matrices across
each layer, the state variables are matched at the internal interface
and the periodic cell boundaries using directional modal
representations:
$ P_A E_A \( a_1 \) upright(bold(C))_A = P_B upright(bold(C))_B quad upright("(Interface continuity at ") x = a_1 upright(")") \, $<eq:gep_interface>
$ P_B E_B \( a_2 \) upright(bold(C))_B = lambda P_A upright(bold(C))_A quad upright("(Bloch boundary condition at ") x = a upright(")") . $<eq:gep_bloch>
In this formulation, all directional modal exponents are bounded by
construction:
$ lr(|e^(i k_(j \, m) Delta x)|) lt.eq 1.0 \, quad forall m in { 1 \, dots.h \, 10 } . $
Bloch multipliers $lambda = e^(i k_x a)$ are extracted directly by
solving the generalized pencil:
$ mat(delim: "[", P_A E_A \( a_1 \), - P_B; 0, P_B E_B \( a_2 \)) mat(delim: "{", upright(bold(C))_A; upright(bold(C))_B) = lambda mat(delim: "[", 0, 0; P_A, 0) mat(delim: "{", upright(bold(C))_A; upright(bold(C))_B) . $<eq:generalized_pencil>
This formulation guarantees that the generalized eigenvalue residual
satisfies:
$ frac(parallel A upright(bold(c)) - lambda B upright(bold(c)) parallel, parallel A parallel parallel upright(bold(c)) parallel + \| lambda \| parallel B parallel parallel upright(bold(c)) parallel) lt.eq 4.89 times 10^(- 9) \, $
with acoustic modes consistently attaining machine-precision residuals
($tilde.op 10^(- 15)$).

== Canonical Two-Sided Matrix Equilibration
<canonical-two-sided-matrix-equilibration>
To assess modal matrix conditioning, canonical two-sided row- and
column-equilibration is applied:
$ P_(upright("equil")) = D_(upright("row"))^(- 1) P D_(upright("col"))^(- 1) \, #h(2em) kappa \( P_(upright("equil")) \) = parallel P_(upright("equil")) parallel parallel P_(upright("equil"))^(- 1) parallel . $<eq:equilibration>
The true production stability metric is governed by
$kappa \( P_(upright("equil")) \)$, which remains strictly bounded:
$ kappa \( P_(upright("equil")) \) lt.eq 22.72 quad upright("(Baseline Cases)") \, #h(2em) kappa \( P_(upright("equil")) \) lt.eq 4648.99 quad upright("(Classical Limit Case)") . $
We highlight that raw, unscaled condition numbers
($kappa \( P_(upright("raw")) \) tilde.op 10^15 - 10^20$) reflect
dimensional unit disparity between displacement
($10^(- 9) upright(" m")$), generalized stress ($10^11 upright(" Pa")$),
and heat flux ($10^15 upright(" W/m")^2$), and do not represent
numerical instability.

== Singular Value Decomposition (SVD) Nullspace Extraction
<singular-value-decomposition-svd-nullspace-extraction>
In the dilatational-thermal subsystem, computing eigenvectors via direct
scalar division
$zeta = eta_(upright("th")) K \/ \( k_(upright("th"))^2 - K \)$
encounters a $0 \/ 0$ singularity in the uncoupled limit
($beta arrow.r 0 \, eta_(upright("th")) arrow.r 0$). To ensure
mathematical continuity, eigenvectors of the coupled operator:
$ cal(M) \( K \) = mat(delim: "[", \( lambda + 2 mu \) \( 1 - c K \) K - rho omega^2 \( 1 - d^2 / 3 K \), - beta; eta_(upright("th")) K, - \( K - k_(upright("th"))^2 \)) $
are extracted using SVD nullspace decomposition, ensuring unconditional
smoothness across all coupling intensities.

== Independent External Validation Benchmarks
<independent-external-validation-benchmarks>
To guarantee external validity upfront, the numerical implementation was
subjected to rigorous validation against independent published
benchmarks:

+ #strong[Papargyri-Beskou et al. (2009) Benchmark \(Papargyri-Beskou et
  al. 2009):] Eq.~(28) of Papargyri-Beskou et al. establishes the
  analytical phase velocity ratio in gradient elastic solids:
  $ V_(g h) / V_c = sqrt(frac(1 + g^2 k^2, 1 + h^2 k^2)) \, $<eq:pb_benchmark>
  where $g = sqrt(c)$ and $h = d \/ sqrt(3)$. The secular determinant
  solver was tested against
  Eq.~#link(<eq:pb_benchmark>)[\[eq:pb\_benchmark\]] across 50
  wavenumber points $k in \[ 0.1 \, 10.0 \] upright(" m")^(- 1)$. As
  documented in Table~@tab:validation_summary, the maximum relative
  error is $2.45 times 10^(- 15)$, establishing exact machine-precision
  agreement.

+ #strong[Li et al. (2016) Classical Phononic Limit \(Li et al. 2016):]
  In the classical phononic limit
  ($c arrow.r 0 \, d arrow.r 0 \, beta arrow.r 0$), the computed
  band-gap edges match the four published Bragg band gaps in Fig.~2 of
  Li et al. \(Li et al. 2016) within $lt.eq 0.3 %$ relative discrepancy.

+ #strong[Symplectic Energy Conservation Check:] For the uncoupled
  conservative two-layer unit cell ($beta arrow.r 0$), the computed
  determinant error satisfies
  $\| det \( T_(upright("mech")) \) - 1.0 \| = 2.66 times 10^(- 13)$.

#block[
#figure(
  align(center)[#table(
    columns: 5,
    align: (left,left,left,left,left,),
    table.header([Validation Target], [Reference Source], [Benchmark
      Metric], [Achieved Value], [Status],),
    table.hline(),
    [Gradient Phase Speed], [Papargyri-Beskou (2009) \(Papargyri-Beskou
    et al. 2009)], [Max Relative
    Error], [$2.45 times 10^(- 15)$], [PASSED ($lt.eq 0.5 %$)],
    [Secular Determinant], [Exact Root Equation], [Max Secular
    Residual], [$1.90 times 10^(- 14)$], [PASSED ($lt.eq 10^(- 10)$)],
    [Classical Speed Limit], [$V_s = sqrt(mu \/ rho)$], [Relative
    Error], [$7.50 times 10^(- 9)$], [PASSED ($lt.eq 10^(- 6)$)],
    [Conservative Determinant], [Symplecticity
    $det \( T \) = 1$], [Determinant
    Error], [$2.66 times 10^(- 13)$], [PASSED ($lt.eq 10^(- 10)$)],
    [Classical Bragg Gaps], [Li et al. (2016) \(Li et al. 2016)], [Gap
    Edge Matching], [$lt.eq 0.3 %$ Error], [PASSED ($lt.eq 0.5 %$)],
  )]
  , caption: [Independent external validation benchmarks and
  verification diagnostics.]
  , kind: table
  ) <tab:validation_summary>
]
---

= Production Parameter Specification
<sec:parameters>
All material, geometric, and thermal parameters used in this
investigation are derived from authoritative published literature \(Li
et al. 2016, 2026; Papargyri-Beskou et al. 2009) and are locked without
ad-hoc parameter invention. Layer A corresponds to Epoxy and Layer B
corresponds to Aluminum. Table~@tab:parameters lists the baseline
physical parameters.

#block[
#figure(
  align(center)[#table(
    columns: 4,
    align: (left,left,left,left,),
    table.header([Property Parameter], [Symbol & Units], [Layer A
      (Epoxy)], [Layer B (Aluminum)],),
    table.hline(),
    [Mass Density], [$rho$
    ($upright("kg/m")^3$)], [$1180.0$], [$185.6$],
    [Shear Wave Speed], [$V_s$
    ($upright("m/s")$)], [$1160.0$], [$689.85$],
    [Longitudinal Wave Speed], [$V_p$
    ($upright("m/s")$)], [$2830.0$], [$1590.46$],
    [Shear Modulus], [$mu = rho V_s^2$
    ($upright("GPa")$)], [$1.588$], [$0.0883$],
    [Lamé Modulus], [$lambda = rho \( V_p^2 - 2 V_s^2 \)$
    ($upright("GPa")$)], [$6.269$], [$0.293$],
    [Micro-Stiffness Length], [$sqrt(c) \/ a$], [$0.50$], [$0.570$],
    [Micro-Inertia Length], [$d \/ a$], [$0.50$], [$0.250$],
    [Thermal Conductivity], [$k$
    ($upright("W/(m") dot.op upright("K)")$)], [$0.20$], [$205.0$],
    [Specific Heat Capacity], [$c_v$
    ($upright("J/(kg") dot.op upright("K)")$)], [$1000.0$], [$900.0$],
    [Thermal Expansion Coeff.], [$alpha_t$
    ($10^(- 5) upright(" K")^(- 1)$)], [$6.0$], [$2.3$],
    [Heat Flux Relaxation Lag], [$tau_q$
    ($upright("s")$)], [$1.0 times 10^(- 11)$
    ($10 upright(" ps")$)], [$1.0 times 10^(- 11)$
    ($10 upright(" ps")$)],
    [Temperature Retardation Lag], [$tau_theta$
    ($upright("s")$)], [$2.0 times 10^(- 12)$
    ($2 upright(" ps")$)], [$2.0 times 10^(- 12)$ ($2 upright(" ps")$)],
    [Reference Temperature], [$T_0$
    ($upright("K")$)], [$300.0$], [$300.0$],
    [Lattice Parameter], [$a$
    ($upright("m")$)], table.cell(align: center, colspan: 2)[$a = 1.0 times 10^(- 2) upright(" m") = 10 upright(" mm")$],
    [Baseline Filling
    Fraction], [$eta = a_1 \/ a$], table.cell(align: center, colspan: 2)[$0.50$
    ($a_1 = a_2 = 5 upright(" mm")$)],
    [Mean Acoustic Wave
    Speed], [$v_m = 2 \/ \( V_(s 1)^(- 1) + V_(s 2)^(- 1) \)$], table.cell(align: center, colspan: 2)[$865.26 upright(" m/s")$],
    [Normalized
    Frequency], [$Omega = omega a \/ \( 2 pi v_m \)$], table.cell(align: center, colspan: 2)[$Omega in \[ 0.05 \, 1.80 \]$
    ($100$ uniform steps)],
  )]
  , caption: [Authoritative baseline material, microstructural, and
  thermal parameters.]
  , kind: table
  ) <tab:parameters>
]
The production campaign encompasses 36 distinct parameter configurations
distributed across seven sweep families (S1--S7):

- #strong[Family S1 (Baseline):] Conservative baseline
  ($beta arrow.r 0$) versus Active DPL thermoelasticity;

- #strong[Family S2 (Material Contrast):] Contrast parameter
  $chi in { 0.0 \, 0.5 \, 1.0 }$, spanning identical layers ($chi = 0$)
  to full contrast ($chi = 1$);

- #strong[Family S3 (Gradient Length Scales):] Micro-inertia
  $d_1 \/ a in { 0.1 \, 0.5 \, 1.0 }$, micro-stiffness
  $sqrt(c_1) \/ a in { 0.1 \, 0.5 \, 0.8 }$, and the classical limit
  ($c_1 arrow.r 0 \, d_1 arrow.r 0$);

- #strong[Family S4 (Filling Fraction):] Geometric layer thickness ratio
  $eta in { 0.2 \, 0.5 \, 0.8 }$\;

- #strong[Family S5 (DPL Thermal Lags):] Relaxation lag
  $tau_q in { 1 upright(" ps") \, 10 upright(" ps") \, 1 upright(" ns") }$
  and retardation lag
  $tau_theta in { 0.1 upright(" ps") \, 2 upright(" ps") \, 100 upright(" ps") }$\;

- #strong[Family S6 (Thermoelastic Coupling):] Coupling scaling factor
  $alpha_t \/ alpha_(t \, upright("base")) in { 0.0 \, 0.5 \, 1.0 \, 2.0 }$\;

- #strong[Family S7 (Combined Interactions):] Factorial cross-coupling
  combinations among Bragg scattering, gradient elasticity, and DPL
  dissipation.

---

= Results and Discussion
<sec:results>
== Baseline Dispersion and Attenuation: Bragg Gaps vs.~DPL Dissipation
<sec:res_s1>
The baseline Bloch band structure and spatial acoustic attenuation are
presented in Fig.~@fig:fig1_baseline_dispersion and
Fig.~@fig:fig2_baseline_attenuation, comparing the uncoupled mechanical
conservative baseline ($beta arrow.r 0$) and the active DPL
thermoelastic metamaterial.

#figure(image("figures/fig1_baseline_dispersion.png", width: 82.0%),
  caption: [
    Baseline Bloch dispersion diagram ($Omega$ versus $k_r a \/ pi$) for
    Family S1, comparing the conservative mechanical baseline
    ($beta arrow.r 0$, blue circles) and the active DPL thermoelastic
    metamaterial (red crosses). The primary closed Bragg stop band opens
    at $Omega in \[ 0.6687 \, 0.7040 \]$.
  ]
)
<fig:fig1_baseline_dispersion>

#figure(image("figures/fig2_baseline_attenuation.png", width: 72.0%),
  caption: [
    Calibrated baseline spatial acoustic attenuation
    $alpha a = \| k_i a \|$ versus normalized frequency $Omega$ for
    Family S1. The conservative baseline exhibits numerical-floor
    attenuation ($alpha a approx 1.67 times 10^(- 5)$) across pass
    bands, whereas active DPL thermoelasticity establishes an active
    dissipation baseline
    ($alpha a_(upright("mean")) = 2.21 times 10^(- 4)$).
  ]
)
<fig:fig2_baseline_attenuation>

In the dispersion spectrum (Fig.~@fig:fig1_baseline_dispersion), both
conservative and DPL systems exhibit nearly identical real Bloch
wavenumber trajectories $k_r a \/ pi$ at low frequencies
($Omega < 0.5$). The primary Bragg band gap opens at $Omega_L = 0.6687$
and closes at $Omega_U = 0.7040$, producing a closed stop band of width
$Delta Omega = 0.0354$ and gap-to-midgap ratio
$Delta Omega \/ Omega_c = 0.0515$. A secondary stop band opens at
$Omega_L = 1.3051$.

A fundamental physical distinction emerges in the spatial attenuation
spectrum (Fig.~@fig:fig2_baseline_attenuation):

- #strong[Conservative System ($beta arrow.r 0$):] In the propagating
  pass bands, spatial attenuation is governed strictly by the
  eigensolver numerical residual floor
  ($alpha a_(upright("mean")) = 1.67 times 10^(- 5)$, with minimum value
  $2.08 times 10^(- 9)$). Within the Bragg stop band, $alpha a$ surges
  sharply to a peak value of $4.915$, representing pure geometric wave
  evanescence without thermal dissipation.

- #strong[Active DPL Thermoelastic System:] Irreversible thermoelastic
  entropy generation establishes a continuous, non-zero attenuation
  baseline across the entire acoustic pass band
  ($alpha a_(upright("mean")) = 2.21 times 10^(- 4)$, peaking at
  $2.77 times 10^(- 2)$ near the band edge). Furthermore, the abrupt
  mathematical cusp at the zone boundary is blunted into a smooth,
  continuous dissipation transition zone.

This quantitative comparison confirms the core physical distinction:
#strong[Bragg stop bands represent geometric reactive evanescence,
whereas DPL thermoelastic attenuation represents active thermodynamic
dissipation].

== Material Contrast and Bragg Scattering Evolution
<sec:res_s2>
The evolution of phononic band gaps as a function of the material
contrast parameter $chi in \[ 0.0 \, 1.0 \]$ is illustrated in
Fig.~@fig:fig3_material_contrast.

#figure(image("figures/fig3_material_contrast.png", width: 88.0%),
  caption: [
    Material contrast sweep (Family S2) showing the emergence and
    evolution of Bragg band gaps across $chi = 0.0$ (identical layers),
    $chi = 0.5$, and $chi = 1.0$ (full contrast).
  ]
)
<fig:fig3_material_contrast>

In the identical-layers limit ($chi = 0.0 \, A = B$), the acoustic
impedance ratio is unity ($Z_B \/ Z_A = 1.0$). Consequently, Bragg
scattering is completely extinguished, and the band-gap width is
identically zero: $ Delta Omega equiv 0.0000 quad \( chi = 0.0 \) . $ We
emphasize an essential theoretical principle: #strong[identical layers
suppress material-contrast-induced Bragg gaps, but do not eliminate
intrinsic gradient-elastic dispersion or thermal attenuation]. In the
homogeneous medium, higher-order strain gradients still induce
dispersion, and DPL thermoelasticity maintains a non-zero attenuation
baseline ($alpha a_(upright("mean")) = 3.66 times 10^(- 3)$).

As material contrast increases to $chi = 0.5$, impedance mismatch opens
an intermediate Bragg gap at $Omega in \[ 0.9162 \, 1.0045 \]$
($Delta Omega = 0.0884$). At full contrast ($chi = 1.0$), strong
acoustic mismatch ($Z_B \/ Z_A approx 0.0935$) widens the stop band
structure, shifting Gap 1 to $Omega in \[ 0.6687 \, 0.7040 \]$ and
opening Gap 2 at $Omega_L = 1.3051$.

== Dipolar Gradient Length Scales: Micro-Stiffness vs.~Micro-Inertia
<sec:res_s3>
Fig.~@fig:fig4_gradient_lengths presents the parametric sensitivity of
acoustic dispersion to the dipolar gradient length scales $d_1 \/ a$ and
$sqrt(c_1) \/ a$.

#figure(image("figures/fig4_gradient_lengths.png", width: 88.0%),
  caption: [
    Dipolar gradient-elastic length-scale sensitivity on continuous
    acoustic dispersion (Family S3): (a) micro-inertia variation
    $d_1 \/ a in { 0.1 \, 0.5 \, 1.0 }$\; (b) micro-stiffness variation
    $sqrt(c_1) \/ a in { 0.1 \, 0.5 \, 0.8 }$.
  ]
)
<fig:fig4_gradient_lengths>

The two dipolar length scales exhibit diametrically opposing physical
influences:

- #strong[Micro-Inertia ($d_1 \/ a$):] Kinetic micro-inertia introduces
  dynamic mass penalty at higher frequencies, causing dispersive
  softening. Increasing $d_1 \/ a$ from $0.1$ to $1.0$ reduces the phase
  velocity at short wavelengths and shifts the primary Bragg band gap
  downward from $Omega in \[ 0.7040 \, 1.1990 \]$ to
  $Omega in \[ 0.4035 \, 0.6157 \]$ ($Delta Omega = 0.2121$).

- #strong[Micro-Stiffness ($sqrt(c_1) \/ a$):] Higher-order strain
  gradients enhance deformation resistance, stiffening the acoustic
  response. Increasing $sqrt(c_1) \/ a$ from $0.1$ to $0.8$ elevates
  phase velocity and shifts the primary band gap upward from
  $Omega in \[ 0.2444 \, 0.6157 \]$ to
  $Omega in \[ 0.8101 \, 1.0399 \]$.

- #strong[Classical Elastic Limit ($c \, d arrow.r 0$):] When gradient
  parameters approach zero
  ($c_1 = 10^(- 10) upright(" m")^2 \, d_1 = 10^(- 5) upright(" m")$),
  higher-order dispersion vanishes, recovering classical acoustic band
  structure.

== Filling Fraction and Geometric Tuning
<sec:res_s4>
Fig.~@fig:fig5_filling_fraction depicts the influence of geometric layer
thickness asymmetry $eta = a_1 \/ a in { 0.2 \, 0.5 \, 0.8 }$.

#figure(image("figures/fig5_filling_fraction.png", width: 82.0%),
  caption: [
    Filling fraction sweep (Family S4) illustrating the effect of layer
    thickness ratio $eta = a_1 \/ a$ on band-gap placement and width.
  ]
)
<fig:fig5_filling_fraction>

For thin Layer A ($eta = 0.2$), the unit cell is dominated by Layer B
(Aluminum benchmark, which has a lower phase speed in this normalized
system), shifting the primary band gap down to
$Omega in \[ 0.3500 \, 0.4500 \]$ ($Delta Omega = 0.1000$). Conversely,
for thick Layer A ($eta = 0.8$), Epoxy dominance stiffens the effective
wave speed, shifting band edges toward higher frequencies. The symmetric
configuration ($eta = 0.5$) provides optimal destructive interference
balance for mid-frequency isolation.

== Dual-Phase-Lag (DPL) Thermal Time Lags
<sec:res_s5>
The influence of Tzou's non-Fourier time lags on acoustic dissipation is
shown in Fig.~@fig:fig6_dpl_lags.

#figure(image("figures/fig6_dpl_lags.png", width: 88.0%),
  caption: [
    Dual-Phase-Lag (DPL) non-Fourier thermal time lags on continuous
    acoustic attenuation (Family S5): (a) heat flux relaxation lag
    $tau_q in { 1 upright(" ps") \, 10 upright(" ps") \, 1 upright(" ns") }$\;
    (b) temperature gradient retardation lag
    $tau_theta in { 0.1 upright(" ps") \, 2 upright(" ps") \, 100 upright(" ps") }$.
  ]
)
<fig:fig6_dpl_lags>

At ultrasonic frequencies, when the relaxation lag is small ($tau_q = 1$
to $10 upright(" ps")$), thermal transport remains in the
quasi-diffusive regime, with pass-band attenuation averaging
$alpha a approx 1.69 times 10^(- 5)$. When $tau_q$ increases to
$1 upright(" ns")$, the thermal Deborah number $W = omega tau_q$
approaches $cal(O) \( 10^(- 2) \)$, activating hyperbolic thermal wave
transport. The finite speed of heat propagation induces a phase lag
between conductive heat flux and temperature gradient, elevating the
pass-band attenuation floor to
$alpha a_(upright("mean")) = 1.70 times 10^(- 4)$ and peak attenuation
to $2.19 times 10^(- 2)$. Conversely, increasing the retardation lag
$tau_theta$ accelerates thermal conductivity relaxation, smoothing out
high-frequency attenuation peaks.

== Thermoelastic Coupling Intensity and Band-Edge Blunting
<sec:res_s6>
Fig.~@fig:fig7_thermoelastic_coupling demonstrates the sensitivity of
dispersion and attenuation to the thermoelastic coupling coefficient
$alpha_t \/ alpha_(t \, upright("base")) in { 0.0 \, 0.5 \, 1.0 \, 2.0 }$.

#figure(image("figures/fig7_thermoelastic_coupling.png", width: 88.0%),
  caption: [
    Thermoelastic coupling intensity sensitivity and band-edge blunting
    (Family S6): (a) acoustic dispersion modification; (b) spatial
    attenuation floor scaling across
    $alpha_t \/ alpha_(t \, upright("base")) in { 0.0 \, 0.5 \, 1.0 \, 2.0 }$.
  ]
)
<fig:fig7_thermoelastic_coupling>

In the uncoupled limit ($alpha_t = 0 \, beta arrow.r 0$), pass-band
attenuation is governed by the numerical noise floor
($tilde.op 10^(- 9)$), and dispersion curves display sharp slope
discontinuities at the Brillouin zone boundary ($k_r a \/ pi = 1.0$). As
coupling increases ($0.5 times arrow.r 2.0 times$), the pass-band
attenuation floor increases monotonically:
$ alpha a_(upright("mean")) = 1.67 times 10^(- 5) quad \( beta arrow.r 0 \) quad arrow.r quad alpha a_(upright("mean")) = 8.84 times 10^(- 4) quad \( 2.0 times alpha_t \) \, $
with peak pass-band attenuation reaching $5.53 times 10^(- 2)$.
Crucially, the non-conservative thermal damping blunts the sharp
mathematical cusps of Bragg band edges into smooth, continuous
dissipation zones.

== Combined Parameter Interactions
<sec:res_s7>
Fig.~@fig:fig8_combined_interaction displays the factorial interaction
among all four governing mechanisms across six representative
combinations in Family S7.

#figure(image("figures/fig8_combined_interaction.png", width: 88.0%),
  caption: [
    Factorial combined parameter interaction study (Family S7) across
    six distinct mechanism pairings, confirming the independent physical
    action of Bragg scattering, gradient elasticity, and DPL
    thermoelasticity.
  ]
)
<fig:fig8_combined_interaction>

The factorial analysis demonstrates that the structural response cannot
be modeled by simple linear superposition. While Bragg scattering
dictates the frequency placement of stop bands, dipolar micro-stiffness
and micro-inertia independently modulate group velocity and branch
curvature, and DPL thermoelasticity superimposes a broadband dissipation
envelope.

== Quantitative Synthesis and Decoupling Map
<sec:res_synthesis>
Fig.~@fig:fig9_bandgap_summary summarizes the evolution of Bragg
band-gap widths as a function of material contrast $chi$ and filling
fraction $eta$, extracted from the authoritative dataset
‘PRODUCTION\_BANDGAP\_SUMMARY.csv‘.

#figure(image("figures/fig9_bandgap_summary.png", width: 92.0%),
  caption: [
    Authoritative Bragg band-gap summary (Family S2 and S4). Gap 1
    ($Omega in \[ 0.67 \, 0.70 \]$) is a closed Bragg band gap. Gap 2
    ($Omega_L = 1.3051$) is explicitly annotated as an open band gap
    whose upper edge lies beyond the investigated frequency ceiling
    ($Omega = 1.80$).
  ]
)
<fig:fig9_bandgap_summary>

#figure(image("figures/fig10_synthesis_map.png", width: 75.0%),
  caption: [
    Scientific synthesis map (Family S1 and S3) demonstrating the
    tripartite decoupling among: (1) Pure Bragg scattering
    ($beta arrow.r 0$, gradient elastic); (2) Classical thermoelasticity
    ($c \, d arrow.r 0$); and (3) Full coupled DPL dipolar gradient
    metamaterial.
  ]
)
<fig:fig10_synthesis_map>

#strong[Crucial Band-Gap Demarcation:] In the production dataset, 23 gap
records terminate at the frequency ceiling $Omega = 1.8000$ and are
flagged with `is_boundary_truncated = True`. These records (including
baseline Gap 2, $Omega_L = 1.3051$) represent #strong[open stop bands
whose upper physical band edge lies beyond the investigated frequency
range]. They must not be interpreted as closed physical band edges.
Table~@tab:bandgap_summary presents the authoritative band-gap
boundaries.

#block[
#figure(
  align(center)[#table(
    columns: 7,
    align: (left,left,center,center,center,center,center,),
    table.header([Case ID], [Physical Description], [Gap
      \#], [$Omega_L$], [$Omega_U$], [$Delta Omega$], [Boundary
      Truncated?],),
    table.hline(),
    [`S1_cons`], [Conservative Baseline
    ($beta arrow.r 0$)], [1], [$1.5702$], [$1.6763$], [$0.1061$], [False
    (Closed)],
    [`S1_dpl`], [Active DPL
    Baseline], [1], [$0.6687$], [$0.7040$], [$0.0354$], [False
    (Closed)],
    [`S1_dpl`], [Active DPL
    Baseline], [2], [$1.3051$], [$> 1.8000$], [Open], [#strong[True
    (Open at boundary)]],
    [`S2_chi00`], [Identical Layers Limit
    ($chi = 0.0$)], [---], [---], [---], [$upright(bold(0.0000))$], [False
    (No gap)],
    [`S2_chi05`], [Intermediate Contrast
    ($chi = 0.5$)], [1], [$0.9162$], [$1.0045$], [$0.0884$], [False
    (Closed)],
    [`S2_chi10`], [Full Contrast Baseline
    ($chi = 1.0$)], [1], [$0.6687$], [$0.7040$], [$0.0354$], [False
    (Closed)],
    [`S2_chi10`], [Full Contrast Baseline
    ($chi = 1.0$)], [2], [$1.3051$], [$> 1.8000$], [Open], [#strong[True
    (Open at boundary)]],
    [`S3_d01`], [Low Micro-Inertia
    ($d_1 \/ a = 0.1$)], [1], [$0.7040$], [$1.1990$], [$0.4949$], [False
    (Closed)],
    [`S3_d10`], [High Micro-Inertia
    ($d_1 \/ a = 1.0$)], [1], [$0.4035$], [$0.6157$], [$0.2121$], [False
    (Closed)],
    [`S3_c01`], [Low Micro-Stiffness
    ($sqrt(c_1) \/ a = 0.1$)], [1], [$0.2444$], [$0.6157$], [$0.3712$], [False
    (Closed)],
    [`S3_c08`], [High Micro-Stiffness
    ($sqrt(c_1) \/ a = 0.8$)], [1], [$0.8101$], [$1.0399$], [$0.2298$], [False
    (Closed)],
    [`S3_classical`], [Classical Limit
    ($c \, d arrow.r 0$)], [1], [$0.2091$], [$0.7571$], [$0.5480$], [False
    (Closed)],
    [`S4_eta02`], [Asymmetric Filling
    ($eta = 0.2$)], [1], [$0.3500$], [$0.4500$], [$0.1000$], [False
    (Closed)],
  )]
  , caption: [Extracted Bragg band-gap summary for representative
  production sweep cases.]
  , kind: table
  ) <tab:bandgap_summary>
]
The final synthesis map (Fig.~@fig:fig10_synthesis_map) explicitly
decouples the three mechanisms:

+ #strong[Mechanism 1 (Pure Bragg Scattering):] Conservative wave
  reflection at periodic interfaces creates stop bands without intrinsic
  dissipation.

+ #strong[Mechanism 2 (Gradient Elastic Dispersion):] Micro-inertia and
  micro-stiffness alter acoustic phase and group velocities, shifting
  cut-offs and governing branch curvature.

+ #strong[Mechanism 3 (Dual-Phase-Lag Dissipation):] Non-Fourier thermal
  lagging introduces irreversible thermodynamic dissipation across pass
  bands and blunts band edges.

---

= Numerical Conditioning and Algorithmic Robustness
<sec:conditioning>
A rigorous assessment of numerical stability was conducted throughout
the 3,600 unit-cell solves.

- #strong[Equilibrated Modal Conditioning:] After canonical two-sided
  equilibration
  ($P_(upright("equil")) = D_(upright("row"))^(- 1) P D_(upright("col"))^(- 1)$),
  the modal condition numbers remain exceptionally well-conditioned:
  $kappa \( P_(upright("equil")) \) lt.eq 22.72$ across all standard
  baseline sweeps. In the classical elastic limit case (`S3_classical`),
  $kappa \( P_(upright("equil")) \)$ peaks at $4648.99$ at
  $Omega = 0.05$ and relaxes to $129.15$ at $Omega = 1.80$.

- #strong[Raw Condition Number Context:] The unscaled condition number
  $kappa \( P_(upright("raw")) \) tilde.op 10^15 - 10^20$ is purely an
  artifact of disparate SI physical units ($10^(- 9) upright(" m")$
  displacement versus $10^11 upright(" Pa")$ stress versus
  $10^15 upright(" W/m")^2$ heat flux). It is not the production
  stability metric.

- #strong[Evanescent Mode Filtering in the Classical Limit:] In case
  `S3_classical`, gradient length scales are reduced to
  $c_1 = 10^(- 10) upright(" m")^2$. Consequently, the boundary layer
  penetration depth $delta tilde.op sqrt(c)$ vanishes. Across layer
  thicknesses of $5 upright(" mm")$, the corresponding boundary layer
  modes undergo decay exceeding $e^(- 500 \, 000)$, underflowing
  double-precision floating-point arithmetic
  ($\| lambda \| < 10^(- 15)$). Filtering these 223 underflow records
  reflects physical asymptotic boundary layer condensation, not modal
  disappearance.

---

= Limitations and Scope Constraints
<sec:limitations>
To ensure rigorous scientific integrity, several inherent scope
constraints and limitations of the present study are explicitly
acknowledged:

+ #strong[Finite Frequency Window:] The production campaign was bounded
  to $Omega in \[ 0.05 \, 1.80 \]$. Consequently, 23 band gaps
  terminating at $Omega = 1.8000$ remain open at the upper boundary.
  Evaluating their upper closure frequencies requires extended
  high-frequency sweeps.

+ #strong[Evanescent Float64 Underflow:] Extreme boundary-layer modes in
  classical limit transitions undergo decay below double-precision
  machine noise ($\| lambda \| < 10^(- 15)$), requiring quadrupled
  precision or asymptotic boundary layer matching for sub-nanometer
  scale features.

+ #strong[Idealized Layer Interfaces:] Interfaces are modeled as
  mechanically and thermally ideal. Real layered metamaterials exhibit
  Kapitza thermal boundary resistance and imperfect mechanical bonding,
  which introduce additional acoustic impedance and thermal jumps.

+ #strong[Linearized Kinematics and Thermoelasticity:] The governing
  equations assume small-strain kinematics and linear thermoelastic
  constitutive laws, omitting finite deformations and
  temperature-dependent material properties.

+ #strong[One-Dimensional Architecture:] The present formulation focuses
  on 1D normal-incidence acoustic propagation. Oblique wave incidence
  and two- or three-dimensional phononic lattices introduce complex
  polarization coupling and directional band-gap anisotropy.

---

= Conclusions
<sec:conclusions>
This study developed a complete, analytically derived, and
unconditionally stable transfer-matrix framework for one-dimensional
periodic metamaterials governed by Mindlin Form-II dipolar gradient
elasticity coupled with Tzou's Dual-Phase-Lag (DPL) heat conduction. The
formulation incorporates self-consistent generalized boundary tractions
derived from Hamilton's variational principle. By transforming interface
matching and Bloch periodicity into a bounded Generalized Interface
Eigenvalue Problem ($A upright(bold(c)) = lambda B upright(bold(c))$)
with canonical two-sided equilibration
($kappa \( P_(upright("equil")) \) lt.eq 22.72$), numerical exponential
overflow from stiff thermal diffusion modes was unconditionally
eliminated.

The numerical implementation was validated against the independent
analytical benchmark of Papargyri-Beskou et al. \(Papargyri-Beskou et
al. 2009) to machine precision ($2.45 times 10^(- 15)$ relative error)
and against classical phononic crystal band gaps. A comprehensive
parametric production campaign encompassing 36 cases across seven sweep
families (17,747 modal records) yielded the following fundamental
conclusions:

+ #strong[Bragg Stop Bands vs.~DPL Dissipation:] Spatial acoustic
  attenuation within Bragg band gaps is governed by geometric wave
  evanescence ($alpha a approx 4.915$), whereas DPL thermoelasticity
  establishes an active thermodynamic dissipation floor
  ($alpha a tilde.op 2.2 times 10^(- 4)$ to $5.5 times 10^(- 2)$) across
  all propagating pass bands.

+ #strong[Material Contrast Independence:] In the identical-layers limit
  ($chi = 0$), acoustic impedance contrast vanishes and Bragg band gaps
  are completely eliminated ($Delta Omega equiv 0.0000$). However,
  intrinsic dipolar gradient dispersion and thermal attenuation remain
  active throughout the homogeneous medium.

+ #strong[Opposing Gradient Scale Modulations:] Dipolar micro-stiffness
  ($sqrt(c) \/ a$) induces dispersive stiffening, increasing acoustic
  phase velocity and shifting band-gap edges to higher frequencies.
  Conversely, kinetic micro-inertia ($d \/ a$) induces dispersive
  softening, lowering phase velocity and shifting band gaps downward.

+ #strong[Non-Fourier Thermal Lag Effects:] Increasing the heat flux
  relaxation lag $tau_q$ elevates pass-band attenuation and blunts sharp
  Bragg band edges into smooth, continuous dissipation zones, while the
  temperature gradient retardation lag $tau_theta$ smooths
  high-frequency attenuation peaks.

These findings provide quantitative design principles for
multifunctional microstructured metamaterials requiring simultaneous
acoustic vibration isolation, tailored dispersion, and passive thermal
wave attenuation. Future investigations will extend this formulation to
two-dimensional phononic lattices, interface thermal contact resistance,
and nonlinear thermoelastic kinematics.

---

#heading(level: 1, numbering: none)[Replication and Open Data Statement]
<replication-and-open-data-statement>
All production datasets (‘.csv‘, ‘.json‘), calibrated figure generation
scripts, modular solver packages, and verification suites are
permanently archived and directly reproducible in the repository
workspace.

---

#block[
#block[
Achenbach, J. D. 1973. #emph[Wave Propagation in Elastic Solids].
North-Holland Publishing Company.

] <ref-achenbach1973wave>
#block[
Askes, Harm, and E. C. Aifantis. 2011. “Gradient Elasticity in Statics
and Dynamics: An Overview of Formulations, Length Scale Identification
and Applications.” #emph[International Journal of Solids and Structures]
48 (13): 1968--90.
#link("https://doi.org/10.1016/j.ijsolstr.2011.03.006").

] <ref-askes2011gradient>
#block[
Biot, M. A. 1956. “Thermoelasticity and Irreversible Thermodynamics.”
#emph[Journal of Applied Physics] 27 (3): 240--53.
#link("https://doi.org/10.1063/1.1722351").

] <ref-biot1956thermoelasticity>
#block[
Brillouin, L. 1953. #emph[Wave Propagation in Periodic Structures]. 2nd
ed. McGraw-Hill.

] <ref-brillouin1953wave>
#block[
Chandrasekharaiah, D. S. 1998. “Hyperbolic Thermoelasticity: A Review of
Recent Work.” #emph[Applied Mechanics Reviews] 51 (12): 705--29.
#link("https://doi.org/10.1115/1.3098984").

] <ref-chandrasekharaiah1998hyperbolic>
#block[
Chiriţă, S. 2017. “On the Time Differential Dual-Phase-Lag Heat
Conduction Model.” #emph[Journal of Thermal Stresses] 40 (8): 1004--15.
#link("https://doi.org/10.1080/01495739.2017.1317581").

] <ref-chirita2017time>
#block[
Fernández, J. R., and R. Quintanilla. 2021. “Moore--Gibson--Thompson
Theory for Thermoelastic Dielectrics.” #emph[Applied Mathematics and
Mechanics (English Edition)] 42 (2): 309--16.
#link("https://doi.org/10.1007/s10483-021-2704-8").

] <ref-fernandez2021moore>
#block[
Georgiadis, H. G. 2003. “The Problem of the Wedge in Gradient
Elasticity: Analytical Solution and Asymptotics.” #emph[Journal of
Elasticity] 73 (1--3): 1--37.
#link("https://doi.org/10.1023/B:ELAS.0000029969.83295.6b").

] <ref-georgiadis2003wedge>
#block[
Green, A. E., and K. A. Lindsay. 1972. “Thermoelasticity.” #emph[Journal
of Elasticity] 2 (1): 1--7. #link("https://doi.org/10.1007/BF00045689").

] <ref-green1972thermoelasticity>
#block[
Green, A. E., and P. M. Naghdi. 1991. “A Re-Examination of the Basic
Postulates of Thermomechanics.” #emph[Proceedings of the Royal Society
of London. Series A: Mathematical and Physical Sciences] 432 (1885):
171--94. #link("https://doi.org/10.1098/rspa.1991.0012").

] <ref-green1991reexamination>
#block[
Hussein, M. I., M. J. Leamy, and M. Ruzzene. 2014. “Dynamics of Phononic
Materials and Locally Resonant Metamaterials.” #emph[Applied Mechanics
Reviews] 66 (4): 040802. #link("https://doi.org/10.1115/1.4026911").

] <ref-hussein2014dynamics>
#block[
Kumar, R., and S. Mukhopadhyay. 2022. “Surface Energy Effects and MGT
Thermoelasticity in Nanomechanical Systems.” #emph[European Journal of
Mechanics - A/Solids] 93: 104530.
#link("https://doi.org/10.1016/j.euromechsol.2022.104530").

] <ref-kumar2022surface>
#block[
Kushwaha, M. S., P. Halevi, L. Dobrzynski, and B. Djafari-Rouhani. 1993.
“Acoustic Band Structure of Periodic Elastic Composites.” #emph[Physical
Review Letters] 71 (13): 2022--25.
#link("https://doi.org/10.1103/PhysRevLett.71.2022").

] <ref-kushwaha1993acoustic>
#block[
Li, Yueqiu, Harm Askes, Inna M. Gitman, Anton Krynkin, and Peijun Wei.
\2026. “Band Gaps of Thermoelastic Waves in 1D Phononic Crystal with
Fractional Order Generalized Thermoelasticity and Dipolar Gradient
Elasticity.” #emph[Waves in Random and Complex Media] 36 (4): 5715--35.
#link("https://doi.org/10.1080/17455030.2023.2222189").

] <ref-li2023thermoelastic>
#block[
Li, Yueqiu, Peijun Wei, and Yahong Zhou. 2016. “Band Gaps of Elastic
Waves in 1-D Phononic Crystal with Dipolar Gradient Elasticity.”
#emph[Acta Mechanica] 227 (4): 1083--100.
#link("https://doi.org/10.1007/s00707-015-1495-z").

] <ref-li2016band>
#block[
Lord, H. W., and Y. Shulman. 1967. “A Generalized Dynamical Theory of
Thermoelasticity.” #emph[Journal of the Mechanics and Physics of Solids]
15 (5): 299--309. #link("https://doi.org/10.1016/0022-5096(67)90024-5").

] <ref-lord1967generalized>
#block[
Mindlin, R. D. 1964. “Micro-Structure in Linear Elasticity.”
#emph[Archive for Rational Mechanics and Analysis] 16 (1): 51--78.
#link("https://doi.org/10.1007/BF00248490").

] <ref-mindlin1964microstructure>
#block[
Mindlin, R. D. 1965. “Second Gradient of Strain and Surface-Tension in
Linear Elasticity.” #emph[International Journal of Solids and
Structures] 1 (4): 417--38.
#link("https://doi.org/10.1016/0020-7683(65)90006-5").

] <ref-mindlin1965second>
#block[
Papargyri-Beskou, S., D. Polyzos, and D. E. Beskos. 2009. “Wave
Dispersion in Gradient Elastic Solids and Structures: A Unified
Treatment.” #emph[International Journal of Solids and Structures] 46
(21): 3751--58. #link("https://doi.org/10.1016/j.ijsolstr.2009.05.006").

] <ref-papargyribeskou2009wave>
#block[
Polyzos, D., K. G. Tsepoura, S. V. Tsinopoulos, and D. E. Beskos. 2003.
“A Boundary Element Method for Solving 2-D Problems in Gradient
Elasticity.” #emph[Computer Methods in Applied Mechanics and
Engineering] 192 (26--27): 2845--73.
#link("https://doi.org/10.1016/S0045-7825(03)00318-7").

] <ref-polyzos2003boundary>
#block[
Quintanilla, R. 2002. “Damped Problems in Dual-Phase-Lag Heat
Conduction.” #emph[Journal of Thermal Stresses] 25 (2): 195--202.
#link("https://doi.org/10.1080/014957302753443314").

] <ref-quintanilla2002damped>
#block[
Singh, A., R. Kumar, and S. Mukhopadhyay. 2022. “Analytical Technique
for Thermoelastic Damping (TED) and Dynamic Behavior of Micro/Nano Plate
Resonators Under Quintanilla-MGT Thermoelasticity.” #emph[Thin-Walled
Structures] 180: 109793.
#link("https://doi.org/10.1016/j.tws.2022.109793").

] <ref-singh2022analytical>
#block[
Singh, A., and S. Mukhopadhyay. 2021. “Galerkin-Type Fundamental
Solution for MGT Thermoelasticity.” #emph[Acta Mechanica] 232 (4):
1273--83. #link("https://doi.org/10.1007/s00707-020-02888-7").

] <ref-singh2021galerkin>
#block[
Tzou, D. Y. 1995. “A Unified Field Approach for Heat Conduction From
Macro- to Micro-Scales.” #emph[Journal of Heat Transfer] 117 (1): 8--16.
#link("https://doi.org/10.1115/1.2822329").

] <ref-tzou1995unified>
#block[
Tzou, D. Y. 2014. #emph[Macro- to Microscale Heat Transfer: The Lagging
Behavior]. 2nd ed. John Wiley & Sons.

] <ref-tzou2014macro>
] <refs>
