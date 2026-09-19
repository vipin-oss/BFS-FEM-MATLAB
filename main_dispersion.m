%% =======================================================================
%  main_dispersion.m
%
%  Torsional Surface Waves in a Thermoelastic Cylinder embedded in an
%  Elastic Metamaterial with Gurtin-Murdoch Surface Elasticity
%  (Annu Rani & M.S. Barak)
%
%  Solves the non-dimensional dispersion relation det(M(xi,Omega)) = 0
%  [manuscript Eqs. N1-N5 / the 5x5 determinant in Sec. "Dispersion
%  Equation"] by continuation in xi, and plots the dispersion curve,
%  phase velocity and group velocity of the new torsional surface wave.
%
%  IMPORTANT NOTE ON MULTIPLE BRANCHES
%  det(M)=0 has more than one root in Omega at a given xi (this is a
%  5-interface layered waveguide, so several guided-mode branches exist,
%  as is normal in this literature). This script tracks ONE branch by
%  continuation, seeded from the branch with the HIGHEST Omega found at
%  the smallest xi (interpreted here as the fundamental / new torsional
%  surface-wave branch). If you need higher-order branches, re-seed the
%  continuation from a different root at xi(1) (see Section 3).
%
%  -----------------------------------------------------------------------
%  PARAMETER PROVENANCE
%
%  Layer 2 (elastic, a<r<b) = PMMA, Layer 3 reference compliance (metama-
%  terial, omega->inf) = ST-Quartz-with-oscillators base value, fp = 1MHz:
%     Source: Table 1 & Sec. 4.1 of P. Kielczynski, K. Wieja, A. Balcerzak,
%     "New Torsional Surface Elastic Waves in Cylindrical Metamaterial
%      Waveguides for Sensing Applications," Sensors, 25(1), 143 (2025).
%
%  Layer 1 (thermoelastic core, elastic properties only -- the manuscript
%  shows the torsional mode is isochoric/thermally uncoupled, so Cv, K,
%  tau never enter the dispersion relation) = copper:
%     mu^(1) = 3.86e10 Pa, rho^(1) = 8954 kg/m^3
%     Standard LS-theory copper benchmark widely used in this literature
%     (Dhaliwal & Sherief (1980) and subsequent generalized-thermo-
%     elasticity papers). NOTE: Ponnusamy (2007, Int. J. Solids Struct.
%     44, 5336-5348) also lists a "copper at 4.2 K" set, but its printed
%     lambda = 8.20e11 Pa is about an order of magnitude above accepted
%     copper values, so it is not used here.
%
%  Geometry (a,b,c), interface springs (ka,kb) and Gurtin-Murdoch surface
%  constants (mu_s, tau0): NOT available in the literature for this exact
%  3-layer + surface-elasticity configuration (this is the novel model of
%  the present paper). Illustrative values are used, with b calibrated so
%  the non-dimensional Drude/plasmon cutoff Omega_p is O(1) (puts the new
%  wave regime inside the scanned xi window). mu_s, tau0 ~ O(1) N/m are
%  typical orders reported for metal/oxide surfaces in the Gurtin-Murdoch
%  literature (e.g. Miller & Shenoy, 2000). These MUST be justified/
%  varied in the final manuscript -- see parametric_study.m for a
%  dimensionless sensitivity sweep, which is the standard way this strand
%  of literature (Kielczynski et al.) demonstrates such effects without
%  committing to one exact physical scale.
%  =======================================================================

clear; clc; close all;

%% ---------------- 1. Dimensional material parameters -------------------

mu1   = 3.86e10;      % Pa   thermoelastic core (elastic props only) [Cu]
rho1  = 8954;         % kg/m^3

rho2    = 1180;         % kg/m^3   [PMMA, elastic layer]
s44_2   = 70.03e-11;    % Pa^-1

rho3  = 2650;          % kg/m^3   [ST-Quartz base, metamaterial layer]
s0    = 1.474e-11;     % Pa^-1   reference compliance, omega -> infinity
fp    = 1e6;           % Hz
omega_p = 2*pi*fp;     % rad/s

% Geometry -- b calibrated so Omega_p ~ O(1); a=0.5b, c=1.5b (illustrative)
b = 0.35016e-3;    % m
alpha = 0.5; beta = 1.5;
a = alpha*b; c = beta*b;

% Interface spring stiffnesses (illustrative, moderate coupling)
ka = 5/(b*s44_2);   % chosen so ka_star = 5  (see Sec. 2)
kb = 5/(b*s44_2);   % chosen so kb_star = 5

% Gurtin-Murdoch surface constants (illustrative, real order-of-magnitude)
mu_s = 5;    % N/m
tau0 = 1;    % N/m

%% ---------------- 2. Non-dimensional parameters -------------------------

m1 = mu1*s44_2;
ka_star  = ka*b*s44_2;
kb_star  = kb*b*s44_2;
mus_star = (mu_s/b)*s44_2;
tau0_star= (tau0/b)*s44_2;

rho1_ratio = rho1/rho2;
rho3_ratio = rho3/rho2;
s2_over_s0 = s44_2/s0;

Omega_p = omega_p*b*sqrt(rho2*s44_2);

fprintf('--- Non-dimensional parameters ---\n');
fprintf('alpha=%.4f beta=%.4f  m1=%.4f  rho1/rho2=%.4f  rho3/rho2=%.4f\n', ...
    alpha, beta, m1, rho1_ratio, rho3_ratio);
fprintf('ka*=%.4f kb*=%.4f  mus*=%.3e tau0*=%.3e  Omega_p=%.4f\n\n', ...
    ka_star, kb_star, mus_star, tau0_star, Omega_p);
if (mus_star+tau0_star) < 1e-3
    fprintf(['NOTE: (mus*+tau0*) = %.2e is numerically small at this\n' ...
        'mm-scale reference length -- the Gurtin-Murdoch correction is\n' ...
        'physically negligible here (as expected: surface elasticity\n' ...
        'matters most at micro/nano scales). Use parametric_study.m to\n' ...
        'inspect the effect over an illustrative O(1) dimensionless\n' ...
        'range.\n\n'], mus_star+tau0_star);
end

params = struct('alpha',alpha,'beta',beta,'m1',m1, ...
    'rho1_ratio',rho1_ratio,'rho3_ratio',rho3_ratio, ...
    's2_over_s0',s2_over_s0,'Omega_p',Omega_p, ...
    'ka_star',ka_star,'kb_star',kb_star, ...
    'mus_star',mus_star,'tau0_star',tau0_star);

%% ---------------- 3. Continuation-based root tracking -------------------

xi_vals = linspace(0.05, 6, 300);
Omega_sol = NaN(size(xi_vals));

% --- seed at xi(1): full scan, pick branch with HIGHEST Omega ----------
xi0 = xi_vals(1);
grid0 = linspace(1e-4, xi0*0.9999, 4000);
D0 = arrayfun(@(Om) safe_det(xi0, Om, params), grid0);
ok = isfinite(D0);
grid0 = grid0(ok); D0 = D0(ok);
sgn0 = sign(D0);
sw0 = find(diff(sgn0) ~= 0);
if isempty(sw0)
    error('No root bracket found at xi(1); widen the Omega scan range.');
end
j0 = sw0(end);   % highest-Omega crossing = fundamental branch (see header note)
prevOmega = fzero(@(Om) safe_det(xi0, Om, params), [grid0(j0), grid0(j0+1)]);
Omega_sol(1) = prevOmega;

% --- continuation: track the same branch for increasing xi -------------
widths = [0.01, 0.02, 0.05, 0.1, 0.2];
for i = 2:length(xi_vals)
    xi = xi_vals(i);
    found = false;
    for w = widths
        lo = max(1e-4, prevOmega - w);
        hi = min(xi*0.9999, prevOmega + w);
        if hi <= lo, continue; end
        ng = linspace(lo, hi, 40);
        vv = arrayfun(@(Om) safe_det(xi, Om, params), ng);
        okk = isfinite(vv);
        ng = ng(okk); vv = vv(okk);
        if numel(vv) < 2, continue; end
        sgc = find(diff(sign(vv)) ~= 0);
        if isempty(sgc), continue; end
        j = sgc(1);
        try
            r = fzero(@(Om) safe_det(xi, Om, params), [ng(j), ng(j+1)]);
            Omega_sol(i) = r;
            prevOmega = r;
            found = true;
            break;
        catch
        end
    end
    % if not found, prevOmega is kept so the next iteration retries
end

%% ---------------- 4. Phase and group velocity ---------------------------

v2 = 1/sqrt(rho2*s44_2);      % bulk shear-wave speed reference, layer 2 (m/s)

valid = ~isnan(Omega_sol);
xi_v  = xi_vals(valid);
Om_v  = Omega_sol(valid);

vp_nd = Om_v ./ xi_v;
vg_nd = gradient(Om_v, xi_v);

vp = vp_nd * v2;   % m/s
vg = vg_nd * v2;   % m/s

%% ---------------- 5. Plots ----------------------------------------------

figure('Color','w');
plot(xi_v, Om_v, 'b-', 'LineWidth', 2); hold on;
plot(xi_vals, xi_vals, 'g--', 'LineWidth', 1.2);
xlabel('\xi (dimensionless wavenumber, kb)');
ylabel('\Omega (dimensionless frequency)');
legend('New torsional surface wave (fundamental branch)', ...
    'Bulk shear wave (layer 2), \Omega=\xi','Location','northwest');
title('Dispersion curve of the new torsional elastic surface wave');
grid on;

figure('Color','w');
plot(xi_v, vp, 'r-', 'LineWidth', 2); hold on;
plot(xi_v, vg, 'k-', 'LineWidth', 2);
xlabel('\xi (dimensionless wavenumber, kb)');
ylabel('Velocity (m/s)');
legend('Phase velocity v_p','Group velocity v_g','Location','best');
title('Phase and group velocity vs. wavenumber');
grid on;

%% ---------------- helper: 5x5 determinant, guarded ----------------------

function D = safe_det(xi, Omega, p)
    g1s2 = xi^2 - p.rho1_ratio*Omega^2/p.m1;
    g2s2 = xi^2 - Omega^2;

    if abs(Omega) < 1e-10
        D = NaN; return;
    end
    s44_3_over_s0 = 1 - (p.Omega_p^2)/(Omega^2);
    if abs(s44_3_over_s0) < 1e-12
        D = NaN; return;
    end
    m3 = p.s2_over_s0 / s44_3_over_s0;

    g3s2 = xi^2 - p.rho3_ratio*Omega^2/m3;

    if g1s2 <= 0 || g2s2 <= 0 || g3s2 <= 0
        D = NaN; return;
    end

    g1s = sqrt(g1s2); g2s = sqrt(g2s2); g3s = sqrt(g3s2);

    alpha = p.alpha; beta = p.beta;
    ka_star = p.ka_star; kb_star = p.kb_star;
    mus_star = p.mus_star; tau0_star = p.tau0_star; m1 = p.m1;

    M = zeros(5,5);
    M(1,1) = m1*g1s*besseli(2, alpha*g1s);
    M(1,2) = -g2s*besseli(2, alpha*g2s);
    M(1,3) =  g2s*besselk(2, alpha*g2s);

    M(2,1) = m1*g1s*besseli(2, alpha*g1s) + ka_star*besseli(1, alpha*g1s);
    M(2,2) = -ka_star*besseli(1, alpha*g2s);
    M(2,3) = -ka_star*besselk(1, alpha*g2s);

    M(3,2) =  g2s*besseli(2, g2s);
    M(3,3) = -g2s*besselk(2, g2s);
    M(3,4) = -m3*g3s*besseli(2, g3s);
    M(3,5) =  m3*g3s*besselk(2, g3s);

    M(4,2) =  g2s*besseli(2, g2s) + kb_star*besseli(1, g2s);
    M(4,3) = -g2s*besselk(2, g2s) + kb_star*besselk(1, g2s);
    M(4,4) = -kb_star*besseli(1, g3s);
    M(4,5) = -kb_star*besselk(1, g3s);

    M(5,4) =  m3*g3s*besseli(2, beta*g3s) + (mus_star+tau0_star)*xi^2*besseli(1, beta*g3s);
    M(5,5) = -m3*g3s*besselk(2, beta*g3s) + (mus_star+tau0_star)*xi^2*besselk(1, beta*g3s);

    Dc = det(M);
    if ~isreal(Dc) || ~isfinite(Dc)
        D = NaN;
    else
        D = Dc;
    end
end
