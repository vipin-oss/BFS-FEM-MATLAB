% FIG07  Identifiability: four independent diagnostics of one result.
%
% TYPE      : 4-panel  (log-log ray + semilog conditioning + profile curves +
%                       grouped bar comparison)
% PANELS    : (a) null direction: the B ray in the (tau_q, kappa^2) plane
%             (b) Fisher conditioning and 1 - |corr| vs B, twin axes
%             (c) profile likelihood at each computed B
%             (d) Monte Carlo (200 trials) vs Fisher s.e.(tau_q)
% DATA      : identifiability_results.csv, F5_profile_likelihood.csv,
%             monte_carlo_results.csv
% VERIFIED  : cond(F) at B=1 = 7.49868219902787e+16
%             corr(tau_q,kappa^2) at B=1 = 0.9999999999999997
%             MC vs Fisher at B=0.5: 12.3989 vs 12.3679 %
% SUPPORTS  : the SAME degeneracy is reached by three independent routes
%             (Fisher, profile likelihood, Monte Carlo), so it is not an
%             artefact of any single statistical device.
%
% ================= REQUIREMENT J: B = 1 MUST NOT VANISH =================
% Panel (b) plots cond(F), which spans 35.9 to 7.5e16. On a linear axis the
% B = 1 result would dominate and every other point would collapse onto the
% floor. A LOGARITHMIC ordinate is therefore used, which shows the full
% 15-decade rise without distorting any value, and the B = 1 point is
% additionally annotated with its exact magnitude.
%
% The companion trace 1 - |corr| on the right-hand axis is the complementary
% view: it DROPS to 3.3e-16 at B = 1, so the reader sees the same event from
% both directions and no single huge number can hide it.
%
% SCOPE. Every panel concerns the (tau_q, kappa^2) SPLIT. Panel (a) states
% the exact identity that causes it. The figure does not claim, and must not
% be read as claiming, that GK parameters are unidentifiable in general:
% alpha and B remain well determined and that is shown in fig08.
% ========================================================================

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

ID   = gk_readcsv('identifiability_results.csv');
PL   = gk_readcsv('F5_profile_likelihood.csv');
MC   = gk_readcsv('monte_carlo_results.csv');
CHI2 = 3.841458820694124;
ALPHA    = 1.0;      % reference configuration
TAU_TRUE = 0.03;

fig = figure('Units','inches','Position',[1 1 S.wFull 5.20], ...
             'Color','w','Visible','off');
AX = gk_grid(fig, 2, 2, 'top',0.145, 'bottom',0.135, ...
             'hgap',0.175, 'vgap',0.205, 'left',0.092, 'right',0.105);

% =====================================================================
% (a) null direction: the B ray
% =====================================================================
ax1 = AX(1,1);
axes(ax1);
tq = logspace(-2.6, -0.6, 200);
hold(ax1,'on');
h1 = loglog(ax1, tq, ALPHA*tq*1.00, '-',  'Color', S.blue,   'LineWidth', S.lw);
h2 = loglog(ax1, tq, ALPHA*tq*1.05, '--', 'Color', S.vermil, 'LineWidth', S.lw);
h3 = loglog(ax1, TAU_TRUE, ALPHA*TAU_TRUE, 'p', 'MarkerSize', 11, ...
            'MarkerFaceColor', S.black, 'MarkerEdgeColor', S.black);
set(ax1,'XScale','log','YScale','log');
hold(ax1,'off');
gk_axes(ax1);
gk_label(ax1,'Relaxation time $\tau_q$', ...
              'Nonlocal coefficient $\kappa^{2}$', ...
              'Null direction of the Fisher matrix');
gk_legend(ax1,[h1 h2 h3], ...
    {'Degeneracy ray, $\kappa^{2}=\alpha\tau_q$ ($B=1$)', ...
     'Off-resonance ray, $B=1.05$', ...
     'Reference configuration'},'northwest');
% the exact identity, placed in empty space below the ray
text(ax1, 0.97, 0.06, ...
     '$\partial T/\partial\tau_q = -\alpha\,\partial T/\partial\kappa^{2}$', ...
     'Units','normalized','Interpreter','latex','FontSize',S.fsAnnot, ...
     'HorizontalAlignment','right','BackgroundColor','w','EdgeColor',[0.75 0.75 0.75]);
gk_panel(ax1,'a');

% =====================================================================
% (b) Fisher conditioning + 1 - |corr|, twin axes, log ordinates
% =====================================================================
ax2 = AX(1,2);
axes(ax2);
B    = ID.B;
cond = ID.cond_F;
oneMinusCorr = 1 - abs(ID.corr_tq_k2);

[~, i1] = min(abs(B - 1.0));

hold(ax2,'on');
hC = plot(ax2, B, cond, '-o', 'Color', S.blue, 'LineWidth', S.lw, ...
          'MarkerFaceColor', S.blue, 'MarkerSize', S.msSmall);
plot(ax2, [1 1], [1e1 1e18], '--', 'Color', S.black, 'LineWidth', 0.9);
set(ax2,'YScale','log');
ylim(ax2,[1e1 1e18]);
set(ax2,'YTick',[1e2 1e6 1e10 1e14 1e18]);
gk_axes(ax2);
gk_label(ax2,'Resonance number $B$', ...
              'Condition number $\mathrm{cond}(\tilde{F})$', ...
              'Fisher-matrix conditioning');

% annotate the B = 1 magnitude so the key value is explicit, not implied
text(ax2, 1.15, cond(i1), sprintf('  $B=1$: %.3g', cond(i1)), ...
     'Interpreter','latex','FontSize',S.fsAnnot, ...
     'VerticalAlignment','middle','HorizontalAlignment','left');

% right-hand axis: 1 - |corr| collapses at B = 1
axPos = get(ax2,'Position');
ax2b  = axes('Position',axPos,'Color','none', ...
             'YAxisLocation','right','XAxisLocation','bottom', ...
             'XTick',[],'YScale','log','Box','off');
hold(ax2b,'on');
hR = plot(ax2b, B, oneMinusCorr, '-s', 'Color', S.vermil, ...
          'LineWidth', S.lw, 'MarkerFaceColor', S.vermil, 'MarkerSize', S.msSmall);
hold(ax2b,'off');
set(ax2b,'XLim',get(ax2,'XLim'),'YColor',S.vermil, ...
         'YTick',[1e-15 1e-10 1e-5 1e0]);
ylabel(ax2b,'$1-|\rho_{\tau_q\kappa^{2}}|$','Interpreter','latex', ...
       'Color',S.vermil,'FontSize',S.fsAxis);
set(ax2b,'FontSize',S.fsTick,'TickDir','out','TickLabelInterpreter','latex');
lgB = gk_legend(ax2, [hC hR], ...
    {'Condition number', 'Correlation deficit $1-|\rho_{\tau_q\kappa^{2}}|$'}, ...
    'southoutside');
gk_assert_legend_clear(ax2, lgB, 'warn');
axes(ax2);
gk_panel(ax2,'b');

% =====================================================================
% (c) profile likelihood at each computed B
% =====================================================================
ax3 = AX(2,1);
axes(ax3);
Bs   = sort(unique(PL.B));
lss  = {'-','--','-.',':','-'};
cols = [S.blue; S.green; S.vermil; S.purple; S.orange];
hold(ax3,'on');
hP = gobjects(1,numel(Bs)); lab = cell(1,numel(Bs));   % graphics-handle array
for k = 1:numel(Bs)
    sel = PL.B == Bs(k);
    tk  = PL.tau_q(sel); zk = PL.delta_sse_over_sigma2(sel);
    [tk,o] = sort(tk); zk = zk(o);
    hP(k) = plot(ax3, tk/TAU_TRUE, zk, lss{k}, 'Color', cols(k,:), ...
                 'LineWidth', S.lw);
    lab{k} = sprintf('$B=%g$', Bs(k));
end
hTh = plot(ax3, [1e-2 1e2], [CHI2 CHI2], '-', 'Color', S.black, 'LineWidth', 1.0);
set(ax3,'XScale','log');
hold(ax3,'off');
xlim(ax3,[min(PL.tau_q) max(PL.tau_q)]/TAU_TRUE);
ylim(ax3,[0 26]);
gk_axes(ax3);
gk_label(ax3,'$\tau_q/\tau_q^{\mathrm{true}}$', ...
              '$\Delta \mathrm{SSE}/\sigma^{2}$', ...
              'Profile likelihood in $\tau_q$');
% legend OUTSIDE the data area: at B=1 the profile is nearly flat across the
% whole grid, so no in-axes corner is reliably empty.
% Reserve a strip beneath panel (c) and park the legend there. Placing it
% outside the data area is the only construction that is guaranteed not to
% occlude a curve, which the runtime assertion below confirms.
pc = get(ax3,'Position');
set(ax3,'Position',[pc(1), pc(2)+0.115, pc(3), pc(4)-0.115]);
lgC = gk_legend(ax3,[hP hTh],[lab,{'$95\%$ threshold'}],'southoutside','cols',3);
set(lgC,'Units','normalized');
lp = get(lgC,'Position');
set(lgC,'Position',[pc(1)+pc(3)/2-lp(3)/2, pc(2)-0.038, lp(3), lp(4)]);
gk_assert_legend_clear(ax3, lgC, 'warn');
gk_panel(ax3,'c');

% =====================================================================
% (d) Monte Carlo vs Fisher
% =====================================================================
ax4 = AX(2,2);
axes(ax4);
mB  = MC.B;
mse = MC.mc_se_tau_q_pct;
fse = MC.fisher_se_tau_q_pct;
x   = 1:numel(mB);
w   = 0.34;
hold(ax4,'on');
hM = bar(ax4, x-w/2, mse, w, 'FaceColor', S.blue,   'EdgeColor', S.black, 'LineWidth',0.5);
hF = bar(ax4, x+w/2, fse, w, 'FaceColor', S.grey,   'EdgeColor', S.black, 'LineWidth',0.5);
hold(ax4,'off');
set(ax4,'YScale','log','XTick',x, ...
    'XTickLabel', arrayfun(@(v) sprintf('%g',v), mB, 'UniformOutput', false));
gk_axes(ax4);
gk_label(ax4,'Resonance number $B$', ...
              '$\mathrm{s.e.}(\tau_q)$ (\%)', ...
              'Sampling vs asymptotic uncertainty');
gk_legend(ax4,[hM hF], ...
    {'Monte Carlo estimate (200 trials)','Fisher-information estimate'},'northwest');
gk_panel(ax4,'d');

gk_suptitle(fig, {'Structural and practical non-identifiability of the $(\tau_q,\kappa^{2})$ split at $B=1$'});

gk_finish(fig, 'fig07_identifiability');
close(fig);

fprintf('    cond(F) at B=1 = %.15g\n', cond(i1));
fprintf('    1-|corr| at B=1 = %.6e\n', oneMinusCorr(i1));
