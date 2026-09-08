% FIG05  Parameter study: the degeneracy in the observable.
%
% TYPE      : 3-panel  (overlaid response curves + control + semilog spread)
% PANELS    : (a) rear-face response along the B = 1 ray, tau_q over 100x
%             (b) control at B = 1.05, same tau_q sweep
%             (c) spread over tau_q for both cases, log scale
% DATA      : F1_degeneracy.csv
% VERIFIED  : ray spread at B=1     = 1.156e-11
%             control spread B=1.05 = 2.595081290055712e-02
%             ratio                 = 2.244e9
% SUPPORTS  : the observable is invariant along the resonance ray while the
%             control at B = 1.05 separates cleanly. This is the direct,
%             model-free demonstration of the degeneracy being studied.
%
% SCOPE. This shows the (tau_q, kappa^2) SPLIT is not resolvable at B = 1.
% It does NOT show that GK parameters are generally unidentifiable.

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

D = gk_readcsv('F1_degeneracy.csv');

tags   = {'0.003','0.03','0.3'};
tauLbl = {'$\tau_q = 0.003$','$\tau_q = 0.03$','$\tau_q = 0.3$'};
cols   = [S.blue; S.vermil; S.green];
lss    = {'-','--',':'};

fig = figure('Units','inches','Position',[1 1 S.wFull 3.10], ...
             'Color','w','Visible','off');
AX = gk_grid(fig, 1, 3, 'top',0.185, 'bottom',0.300, 'hgap',0.125, 'left',0.085, 'right',0.030);

% =====================================================================
% (a) responses along the B = 1 ray
% =====================================================================
ax1 = AX(1,1);
axes(ax1); hold(ax1,'on');
h1 = gobjects(1,numel(tags));   % graphics-handle array (see gk_grid.m note)
for k = 1:numel(tags)
    m = strcmp(D.tau_q_or_tag, tags{k});
    t = D.t_hat(m);  y = D.T_or_spread_B1(m);
    [t,o] = sort(t); y = y(o);
    h1(k) = plot(ax1, t, y, lss{k}, 'Color', cols(k,:), 'LineWidth', S.lw);
end
hold(ax1,'off');
gk_axes(ax1);
gk_label(ax1,'$\hat{t}$','$\hat{T}(L,\hat{t})$', ...
              'On the resonance ray, $\kappa^{2}=\alpha\tau_q$');
gk_legend(ax1, h1, tauLbl, 'southeast');   % lower-right is empty in (a)
gk_panel(ax1,'a');

% =====================================================================
% (b) control at B = 1.05
% =====================================================================
ax2 = AX(1,2);
axes(ax2); hold(ax2,'on');
for k = 1:numel(tags)
    m = strcmp(D.tau_q_or_tag, tags{k});
    t = D.t_hat(m);  y = D.T_or_spread_B105(m);
    [t,o] = sort(t); y = y(o);
    plot(ax2, t, y, lss{k}, 'Color', cols(k,:), 'LineWidth', S.lw);
end
hold(ax2,'off');
gk_axes(ax2);
gk_label(ax2,'$\hat{t}$','$\hat{T}(L,\hat{t})$', ...
              'Off-resonance comparison, $B=1.05$');
gk_panel(ax2,'b');

% =====================================================================
% (c) spread over tau_q, both cases
% =====================================================================
ax3 = AX(1,3);
axes(ax3);
m  = strcmp(D.tau_q_or_tag, 'spread');
t  = D.t_hat(m);
s1 = D.T_or_spread_B1(m);
s2 = D.T_or_spread_B105(m);
[t,o] = sort(t); s1 = s1(o); s2 = s2(o);

hold(ax3,'on');
hA = semilogy(ax3, t, s1, '-',  'Color', S.blue,   'LineWidth', S.lw);
hB = semilogy(ax3, t, s2, '--', 'Color', S.vermil, 'LineWidth', S.lw);
set(ax3,'YScale','log');
hold(ax3,'off');
ylim(ax3,[1e-13 1e-1]);
set(ax3,'YTick',10.^(-13:3:-1));
gk_axes(ax3);
gk_label(ax3,'$\hat{t}$', ...
              'Spread of $\hat{T}$ over the $\tau_q$ sweep', ...
              'Sensitivity on and off resonance');
% Two long entries: centre the key under the whole figure rather than under
% panel (c), where it would overrun the right edge.
lgS = gk_legend(ax3, [hA hB], ...
    {'On-resonance condition, $B=1$', ...
     'Off-resonance control, $B=1.05$'}, 'southoutside', 'cols', 2);
set(lgS,'Units','normalized');
lps = get(lgS,'Position');
set(lgS,'Position',[0.5-lps(3)/2, 0.030, lps(3), lps(4)]);
gk_panel(ax3,'c');

gk_suptitle(fig, {'Structural degeneracy: the rear-face history is invariant along the $B=1$ ray'});

gk_finish(fig, 'fig05_parameter_study');
close(fig);

fprintf('    B=1 spread max = %.6e   B=1.05 spread max = %.15e   ratio = %.3e\n', ...
        max(s1), max(s2), max(s2)/max(s1));
