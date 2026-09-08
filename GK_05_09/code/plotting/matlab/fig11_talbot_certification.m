% FIG11  Laplace-inversion certification: the even-M Talbot pole collision.
%
% TYPE      : 3-panel  (semilog error histories + grouped parity bars +
%                       scatter of split/convolution ratio)
% PANELS    : (a) absolute error against time for the split form at even
%                 M = 40 and odd M = 41, with the predicted collision
%                 instant t* = M tau_Delta / 10 marked, and the adopted
%                 convolution form for comparison
%             (b) error at t = t* for six node counts, grouped by parity,
%                 split form vs convolution form
%             (c) the failure ratio split/convolution per M, showing the
%                 parity dependence as a single number per case
% DATA      : F3_talbot_pole.csv, talbot_parity.csv
% VERIFIED  : M=20 split 1.94225149150898e+11 conv 9.960867541444762e-06
%             M=40 split 9.711257457544894e+10 conv 4.614663849045186e-06
%             M=41 split 2.6393178281902685e-04 conv 4.316972463169755e-06
%             M=60 split 5.330339507602452e+09 conv 1.020398076034823e-06
%             M=64 split 8.446664324082207e+10 conv 7.021927339589951e-07
%             M=81 split 2.590274573699425e-04
% SUPPORTS  : this is a property of the NUMERICAL INVERSION, not of the
%             physics. The exact solution is regular at t*. The adopted
%             convolution form is immune, which is why M = 41 (odd) is used
%             throughout the work.
%
% This is an honest negative result about a method, reported rather than
% hidden, and it is one of the strongest certification arguments available.

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

F3 = gk_readcsv('F3_talbot_pole.csv');
TP = gk_readcsv('talbot_parity.csv');

fig = figure('Units','inches','Position',[1 1 S.wFull 3.15], ...
             'Color','w','Visible','off');
AX = gk_grid(fig, 1, 3, 'top',0.190, 'bottom',0.300, 'hgap',0.155, 'left',0.082, 'right',0.030);

% =====================================================================
% (a) error histories
% =====================================================================
ax1 = AX(1,1);
axes(ax1);
series = {'40','41','conv41'};
labs   = {'Split formulation, even $M=40$', ...
          'Split formulation, odd $M=41$', ...
          'Convolution formulation, $M=41$'};
cols   = [S.vermil; S.blue; S.green];
lss    = {'-','--','-'};

hold(ax1,'on');
hc = {}; keep = {};   % collect handles in a CELL so no numeric coercion occurs
for k = 1:numel(series)
    m = strcmp(F3.solver, series{k});
    if ~any(m), continue; end
    t = F3.t_hat(m); e = abs(F3.abs_error(m));
    [t,o] = sort(t); e = e(o);
    hh = plot(ax1, t, e, lss{k}, 'Color', cols(k,:), 'LineWidth', S.lw);
    hc{end+1} = hh;          %#ok<AGROW>
    keep{end+1} = labs{k};   %#ok<AGROW>
end
% predicted collision instant for M = 40:  t* = M tau_Delta / 10
i40 = find(TP.M == 40, 1);
if ~isempty(i40)
    tstar = TP.t_star(i40);
    hStar = plot(ax1, [tstar tstar], [1e-8 1e12], '-.', ...
                 'Color', S.black, 'LineWidth', 0.9);
    hc{end+1} = hStar;
    keep{end+1} = 'Predicted collision instant $t^{*}=M\tau_\Delta/10$';
end
set(ax1,'YScale','log');
hold(ax1,'off');
ylim(ax1,[1e-9 1e12]);
set(ax1,'YTick',10.^(-9:3:12));
gk_axes(ax1);
gk_label(ax1,'$\hat{t}$','Absolute error', ...
              'Talbot pole collision in time');
h1 = [hc{:}];
lgT = gk_legend(ax1, h1, keep, 'southoutside', 'cols', 2);
set(lgT,'Units','normalized');
lp = get(lgT,'Position');
set(lgT,'Position',[0.5-lp(3)/2, 0.035, lp(3), lp(4)]);
gk_panel(ax1,'a');

% =====================================================================
% (b) parity dependence at t = t*
% =====================================================================
ax2 = AX(1,2);
axes(ax2);
M     = TP.M;
split = TP.split_err;
conv  = TP.conv_err;
isEven = strcmp(TP.parity,'even');

x = 1:numel(M);
hold(ax2,'on');
for k = 1:numel(M)
    plot(ax2, [x(k) x(k)], [min(split(k),conv(k)) max(split(k),conv(k))], '-', ...
         'Color', S.lightgrey, 'LineWidth', 2.5);
end
hSp = plot(ax2, x, split, 's', 'Color', S.vermil, 'MarkerFaceColor', S.vermil, ...
           'MarkerSize', S.ms+1, 'LineStyle','none');
hCv = plot(ax2, x, conv,  'o', 'Color', S.green,  'MarkerFaceColor', S.green, ...
           'MarkerSize', S.ms+1, 'LineStyle','none');
hold(ax2,'off');
set(ax2,'YScale','log','XTick',x);
lbl = cell(numel(M),1);
for k = 1:numel(M)
    if isEven(k), pp = 'e'; else, pp = 'o'; end
    lbl{k} = sprintf('$%d$', M(k));
end
set(ax2,'XTickLabel',lbl);
xlim(ax2,[0.5 numel(M)+0.5]);
ylim(ax2,[1e-8 1e14]);
set(ax2,'YTick',10.^(-8:4:12));
gk_axes(ax2);
gk_label(ax2,'Talbot node count $M$', ...
              'Absolute error at $t^{*}$', ...
              'Parity dependence of the inversion');

gk_panel(ax2,'b');

% =====================================================================
% (c) failure ratio, one number per case
% =====================================================================
ax3 = AX(1,3);
axes(ax3);
ratio = split ./ conv;
hold(ax3,'on');
for k = 1:numel(M)
    if isEven(k)
        c = S.vermil; mk = 's';
    else
        c = S.blue;   mk = 'o';
    end
    plot(ax3, M(k), ratio(k), mk, 'Color', c, 'MarkerFaceColor', c, ...
         'MarkerSize', S.ms+1);
end
plot(ax3, [min(M)-4 max(M)+4], [1 1], '--', 'Color', S.black, 'LineWidth', 0.9);
% proxy handles for a clean two-entry legend, created while hold is still on
hE = plot(ax3, NaN, NaN, 's', 'Color', S.vermil, 'MarkerFaceColor', S.vermil, 'MarkerSize', S.ms+1);
hO = plot(ax3, NaN, NaN, 'o', 'Color', S.blue,   'MarkerFaceColor', S.blue,   'MarkerSize', S.ms+1);
hold(ax3,'off');
set(ax3,'YScale','log');
xlim(ax3,[min(M)-6 max(M)+6]);
ylim(ax3,[1e0 1e21]);
set(ax3,'YTick',10.^(0:4:16));
gk_axes(ax3);
gk_label(ax3,'Talbot node count $M$', ...
              'Error ratio, split / convolution', ...
              'Inversion failure ratio by parity');
% Parity is already encoded by marker and colour in panel (b); an extra
% legend here duplicated it, so panel (c) is annotated directly instead.
text(ax3, 0.50, 0.94, 'Even $M$: pole collision', 'Units','normalized', ...
     'Interpreter','latex','FontSize',S.fsAnnot,'Color',S.vermil, ...
     'HorizontalAlignment','center');
text(ax3, 0.50, 0.14, 'Odd $M$: no collision', 'Units','normalized', ...
     'Interpreter','latex','FontSize',S.fsAnnot,'Color',S.blue, ...
     'HorizontalAlignment','center');
gk_panel(ax3,'c');

gk_suptitle(fig, {'Transform-inversion certification: the convolution form is immune'});

gk_finish(fig, 'fig11_talbot_certification');
close(fig);

for k = 1:numel(M)
    fprintf('    M=%-3d %-5s split=%.6e conv=%.6e ratio=%.3e\n', ...
            M(k), TP.parity{k}, split(k), conv(k), ratio(k));
end
