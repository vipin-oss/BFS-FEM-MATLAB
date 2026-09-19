%% =======================================================================
%  parametric_study.m
%
%  Sensitivity of the torsional surface-wave dispersion curve to the
%  Gurtin-Murdoch surface elasticity parameter (mus*+tau0*) and to the
%  interface spring stiffnesses (ka*, kb*).
%
%  Rationale: main_dispersion.m shows that with *real* material constants
%  at a device (mm) length scale, (mus*+tau0*) is numerically tiny
%  (surface elasticity only matters at micro/nano scale). To still
%  demonstrate -- and quantify -- the qualitative effect of surface
%  elasticity for the manuscript (as Kielczynski et al. do for their own
%  spring-constant studies), this script sweeps the DIMENSIONLESS groups
%  directly over an illustrative O(1) range, independent of any specific
%  (mu_s, tau0, b) triple.
%
%  Uses the same material ratios (m1, rho1_ratio, rho3_ratio, s2_over_s0,
%  Omega_p) and root-tracking approach as main_dispersion.m.
%  =======================================================================

clear; clc; close all;

%% ---------------- Fixed material/geometry ratios (see main_dispersion.m)

mu1 = 3.86e10; rho1 = 8954;
rho2 = 1180; s44_2 = 70.03e-11;
rho3 = 2650; s0 = 1.474e-11; fp = 1e6;
omega_p = 2*pi*fp;

b = 0.35016e-3;
alpha = 0.5; beta = 1.5;

m1 = mu1*s44_2;
rho1_ratio = rho1/rho2;
rho3_ratio = rho3/rho2;
s2_over_s0 = s44_2/s0;
Omega_p = omega_p*b*sqrt(rho2*s44_2);

ka_star_fixed = 5;   % moderate spring coupling (held fixed for the
kb_star_fixed = 5;   % surface-elasticity sweep below)

%% ---------------- Sweep 1: surface elasticity (mus*+tau0*) --------------

surf_vals = [0, 0.2, 0.5, 1, 2];   % illustrative dimensionless range
xi_vals = linspace(0.05, 6, 200);

figure('Color','w'); hold on;
colors = lines(length(surf_vals));
for s_idx = 1:length(surf_vals)
    surf_star = surf_vals(s_idx);
    params = struct('alpha',alpha,'beta',beta,'m1',m1, ...
        'rho1_ratio',rho1_ratio,'rho3_ratio',rho3_ratio, ...
        's2_over_s0',s2_over_s0,'Omega_p',Omega_p, ...
        'ka_star',ka_star_fixed,'kb_star',kb_star_fixed, ...
        'mus_star',surf_star,'tau0_star',0);   % surf_star lumps mus*+tau0*

    Om_v = track_branch(xi_vals, params);
    valid = ~isnan(Om_v);
    plot(xi_vals(valid), Om_v(valid), 'Color', colors(s_idx,:), ...
        'LineWidth', 2, 'DisplayName', sprintf('\\mu_s^*+\\tau_0^* = %.1f', surf_star));
end
plot(xi_vals, xi_vals, 'k--', 'LineWidth', 1, 'DisplayName','\Omega=\xi (bulk shear)');
xlabel('\xi'); ylabel('\Omega');
title('Effect of Gurtin-Murdoch surface elasticity on the dispersion curve');
legend('Location','northwest'); grid on;

%% ---------------- Sweep 2: interface spring stiffness (ka*=kb*) ---------

k_vals = [0.5, 2, 5, 20, 100];   % weak -> near-rigid bonding

figure('Color','w'); hold on;
colors2 = lines(length(k_vals));
for k_idx = 1:length(k_vals)
    k_star = k_vals(k_idx);
    params = struct('alpha',alpha,'beta',beta,'m1',m1, ...
        'rho1_ratio',rho1_ratio,'rho3_ratio',rho3_ratio, ...
        's2_over_s0',s2_over_s0,'Omega_p',Omega_p, ...
        'ka_star',k_star,'kb_star',k_star, ...
        'mus_star',0.5,'tau0_star',0.2);

    Om_v = track_branch(xi_vals, params);
    valid = ~isnan(Om_v);
    plot(xi_vals(valid), Om_v(valid), 'Color', colors2(k_idx,:), ...
        'LineWidth', 2, 'DisplayName', sprintf('k_a^*=k_b^*=%.1f', k_star));
end
plot(xi_vals, xi_vals, 'k--', 'LineWidth', 1, 'DisplayName','\Omega=\xi (bulk shear)');
xlabel('\xi'); ylabel('\Omega');
title('Effect of interface spring stiffness on the dispersion curve');
legend('Location','northwest'); grid on;

%% ---------------- helper: branch tracking (shared logic) ----------------

function Omega_sol = track_branch(xi_vals, params)
    Omega_sol = NaN(size(xi_vals));

    xi0 = xi_vals(1);
    grid0 = linspace(1e-4, xi0*0.9999, 4000);
    D0 = arrayfun(@(Om) safe_det(xi0, Om, params), grid0);
    ok = isfinite(D0);
    grid0 = grid0(ok); D0 = D0(ok);
    sw0 = find(diff(sign(D0)) ~= 0);
    if isempty(sw0)
        return;   % leave all-NaN for this parameter set
    end
    j0 = sw0(end);
    try
        prevOmega = fzero(@(Om) safe_det(xi0, Om, params), [grid0(j0), grid0(j0+1)]);
    catch
        return;
    end
    Omega_sol(1) = prevOmega;

    widths = [0.01, 0.02, 0.05, 0.1, 0.2];
    for i = 2:length(xi_vals)
        xi = xi_vals(i);
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
                break;
            catch
            end
        end
    end
end

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
