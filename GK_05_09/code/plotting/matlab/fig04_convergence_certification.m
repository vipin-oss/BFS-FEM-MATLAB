% FIG04  Consolidated numerical validation.  (Requirement G)
%
% ONE coherent story in four panels:
%   (a) spatial convergence        max abs error vs N_x, log-log, p=2 slope
%   (b) observed order             local p per refinement, p=2 indicated
%   (c) solver/truncation          series vs convolution, to the numerical floor
%   (d) independent certification  Monte Carlo vs Fisher standard errors
%
% Panel (d) is the strongest genuinely INDEPENDENT check available in the
% verified data: a 200-trial Monte Carlo study against the linearised Fisher
% prediction. The former bar chart of symbolic-limit residuals was removed
% from the main paper: those residuals are exact zeros, they duplicated the
% limit tests already tabulated, and they added no information to this story.
%
% DATA (read only)
%   fd_convergence_windows5.csv   spatial ladder, reference grid N_x = 3200
%   series_convergence.csv        eigenfunction truncation
%   monte_carlo_results.csv       200-trial Monte Carlo vs Fisher
%
% VALIDATION LANGUAGE. Panels (a)-(c) are numerical convergence of the
% present implementation. Panel (d) is validation of inverse-problem
% behaviour on controlled data. Neither is experimental validation.

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

FD  = gk_readcsv('fd_convergence_windows5.csv');
SER = gk_readcsv('series_convergence.csv');
MC  = gk_readcsv('monte_carlo_results.csv');

fig = figure('Units','inches','Position',[1 1 S.wFull 4.85], ...
             'Color','w','Visible','off');
AX = gk_grid(fig, 2, 2, 'top',0.130, 'bottom',0.090, ...
             'hgap',0.115, 'vgap',0.170, 'left',0.088);

% =====================================================================
% (a) spatial convergence
% =====================================================================
ax1 = AX(1,1); axes(ax1);
Nx = FD.Nx; err = FD.max_err;
hold(ax1,'on');
hE = plot(ax1, Nx, err, '-o', 'Color', S.blue, 'LineWidth', S.lw, ...
          'MarkerFaceColor', S.blue, 'MarkerSize', S.msSmall);
guide = err(1) * (Nx/Nx(1)).^(-2);          % reference slope, not a fit
hG = plot(ax1, Nx, guide, '--', 'Color', S.grey, 'LineWidth', S.lwThin);
hold(ax1,'off');
set(ax1,'XScale','log','YScale','log', ...
        'XTick',[100 200 400 800 1600], ...
        'XTickLabel',{'100','200','400','800','1600'});
xlim(ax1,[80 2000]);
gk_axes(ax1);
gk_label(ax1,'Grid points $N_x$', ...
              '$\max_t|\hat{T}_{N_x}-\hat{T}_{\mathrm{ref}}|$', ...
              'Finite-difference spatial convergence');
gk_legend(ax1,[hE hG], ...
    {'Finite-difference solution','$\mathcal{O}(h^{2})$ reference slope'},'southwest');
gk_panel(ax1,'a');

% =====================================================================
% (b) observed convergence order
% =====================================================================
ax2 = AX(1,2); axes(ax2);
ordv = FD.order(2:end);                      % transcribed, not recomputed
lbl  = cell(numel(ordv),1);
for k = 1:numel(ordv)
    lbl{k} = sprintf('$%d$--$%d$', Nx(k), Nx(k+1));
end
hold(ax2,'on');
hB = bar(ax2, 1:numel(ordv), ordv, 0.6);
set(hB,'FaceColor',S.sky,'EdgeColor',S.black,'LineWidth',0.5);
hT = plot(ax2, [0.4 numel(ordv)+0.6], [2 2], '--', ...
          'Color', S.vermil, 'LineWidth', S.lw);
for k = 1:numel(ordv)
    text(ax2, k, ordv(k)+0.09, sprintf('$%.2f$', ordv(k)), ...
        'HorizontalAlignment','center','FontSize',S.fsAnnot, ...
        'Interpreter','latex');
end
hold(ax2,'off');
set(ax2,'XTick',1:numel(ordv),'XTickLabel',lbl);
ylim(ax2,[0 2.75]); xlim(ax2,[0.4 numel(ordv)+0.6]);
gk_axes(ax2);
gk_label(ax2,'Refinement interval in $N_x$', ...
              'Observed order $p$','Observed convergence order');
text(ax2, numel(ordv)+0.52, 2.0, '$p=2$', 'Interpreter','latex', ...
     'FontSize', S.fsAnnot, 'Color', S.vermil, ...
     'HorizontalAlignment','right','VerticalAlignment','top');
gk_panel(ax2,'b');

% =====================================================================
% (c) series truncation against the convolution solution
% =====================================================================
ax3 = AX(2,1); axes(ax3);
hold(ax3,'on');
hS = plot(ax3, SER.N, SER.err, '-o', 'Color', S.green, ...
          'LineWidth', S.lw, 'MarkerFaceColor', S.green, 'MarkerSize', S.msSmall);
flo = min(SER.err);
hF = plot(ax3, [min(SER.N) max(SER.N)], [flo flo], ':', ...
          'Color', S.grey, 'LineWidth', S.lw);
hold(ax3,'off');
set(ax3,'XScale','log','YScale','log');
gk_axes(ax3);
gk_label(ax3,'Eigenfunction series terms $N$', ...
              '$\max_t|\hat{T}_{\mathrm{series}}-\hat{T}_{\mathrm{conv}}|$', ...
              'Series and convolution solver agreement');
gk_legend(ax3,[hS hF], ...
    {'Truncated eigenfunction series', ...
     sprintf('Double-precision floor, $%s$', gk_sci(flo))}, 'northeast');
gk_panel(ax3,'c');

% =====================================================================
% (d) independent certification: Monte Carlo vs Fisher
% =====================================================================
ax4 = AX(2,2); axes(ax4);
mB  = MC.B;
mse = MC.mc_se_tau_q_pct;
fse = MC.fisher_se_tau_q_pct;
x   = 1:numel(mB);
w   = 0.34;
% Paired markers rather than bars: on a logarithmic ordinate a bar has no
% meaningful baseline, and filled bars render with gradient artefacts in
% some backends. Markers compare the two estimates directly.
hold(ax4,'on');
for k = 1:numel(x)
    plot(ax4, [x(k) x(k)], [min(mse(k),fse(k)) max(mse(k),fse(k))], '-', ...
         'Color', S.lightgrey, 'LineWidth', 3.0);
end
hM = plot(ax4, x, mse, 'o', 'Color', S.blue, 'MarkerFaceColor', S.blue, ...
          'MarkerSize', S.ms+1, 'LineStyle','none');
hFi= plot(ax4, x, fse, 's', 'Color', S.black, 'MarkerFaceColor', S.grey, ...
          'MarkerSize', S.ms+1, 'LineStyle','none');
hold(ax4,'off');
set(ax4,'YScale','log','XTick',x,'XLim',[0.5 numel(x)+0.5], ...
    'XTickLabel', arrayfun(@(v) sprintf('$%g$',v), mB, 'UniformOutput', false));
ylim(ax4,[4 900]);
gk_axes(ax4);
gk_label(ax4,'Resonance number $B$', ...
              '$\mathrm{s.e.}(\tau_q)$ (\%)', ...
              'Sampling and asymptotic uncertainty');
gk_legend(ax4,[hM hFi], ...
    {'Monte Carlo estimate (200 trials)','Fisher-information estimate'}, ...
    'north','cols',1);
gk_panel(ax4,'d');

gk_suptitle(fig, {'Numerical validation of the solver and the inverse procedure'});

gk_finish(fig, 'fig04_convergence_certification');
close(fig);

fprintf('    FD ladder N_x=%s\n', mat2str(Nx(:).'));
fprintf('    orders %s\n', mat2str(ordv(:).'));
fprintf('    series floor %.6e\n', flo);
