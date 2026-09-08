function gk_anchor_figure(tag, caseName, stem)
%GK_ANCHOR_FIGURE Three-panel reproduction figure for one reference case.
%
%   PANELS
%     (a) reference solution and present model overlaid
%     (b) residual against the +/-2 sigma_d digitisation band
%     (c) cumulative distribution of |residual| relative to that band
%
%   The previous four-panel form showed the reference alone, then the
%   present model alone, then the overlay. The first two panels carried no
%   information the overlay did not already contain, so they are
%   consolidated into a single overlay panel and the freed space is used to
%   quantify the residual, which is the scientifically informative part.
%
%   TERMINOLOGY. The curves are named for the numerical object each one is:
%   "Digitised benchmark solution" is the published curve read off the source
%   figure, and "Present convolution solution" is the convolution formulation
%   evaluated at the literature parameters with no fitting. The informal
%   labels "this work", "published" and "reference" are not used anywhere.
%
%   DATA  F2_anchor_reproduction.csv, anchor_metrics.csv  (read only)
%
%   SCOPE. External validation of the FORWARD OPERATOR. Not validation of
%   the inverse conclusions, and not experimental validation.

S = gk_style();
A = gk_readcsv('F2_anchor_reproduction.csv');
M = gk_readcsv('anchor_metrics.csv');

sel = strcmp(A.figure, tag);
t   = A.t_hat(sel);
Tref= A.T_published(sel);
Tmod= A.T_phase5(sel);
[t, o] = sort(t);  Tref = Tref(o);  Tmod = Tmod(o);

mi     = find(strcmp(M.anchor, tag), 1);
nrmse  = M.nrmse_pct(mi);
rmse   = M.rmse(mi);
npts   = M.n(mi);
sigd   = M.sigma_d(mi);
within = M.within_2sigma_pct(mi);

res = Tmod - Tref;

fig = figure('Units','inches','Position',[1 1 S.wFull 3.15], ...
             'Color','w','Visible','off');
AX = gk_grid(fig, 1, 3, 'top',0.200, 'bottom',0.300, 'hgap',0.125, 'left',0.088, 'right',0.030);

% =====================================================================
% (a) overlay: reference solution and present model
% =====================================================================
ax1 = AX(1,1);
axes(ax1);
hold(ax1,'on');
hR = plot(ax1, t, Tref, 'o', 'MarkerSize', S.msSmall, ...
          'MarkerFaceColor', S.ref.col, 'MarkerEdgeColor', S.ref.col);
hM = plot(ax1, t, Tmod, '-', 'Color', S.num.col, 'LineWidth', S.lw);
hold(ax1,'off');
gk_axes(ax1);
gk_label(ax1, '$\hat{t}$', '$\hat{T}(L,\hat{t})$', 'Benchmark and present solution');

gk_panel(ax1,'a');

% =====================================================================
% (b) residual against the digitisation band
% =====================================================================
ax2 = AX(1,2);
axes(ax2);
hold(ax2,'on');
xb = [min(t) max(t) max(t) min(t)];
yb = [-2*sigd -2*sigd 2*sigd 2*sigd];
hB = gk_band(ax2, min(t), max(t), -2*sigd, 2*sigd, S.bandCol, 0.18);
plot(ax2, [min(t) max(t)], [0 0], '-', 'Color', S.black, 'LineWidth', 0.6);
hE = plot(ax2, t, res, '-', 'Color', S.resid.col, 'LineWidth', S.lwThin);
hold(ax2,'off');
gk_axes(ax2);
gk_label(ax2, '$\hat{t}$', 'Residual $\hat{T}_{\mathrm{num}}-\hat{T}_{\mathrm{ref}}$', ...
              'Residual against digitisation floor');

gk_panel(ax2,'b');

% =====================================================================
% (c) cumulative distribution of the scaled residual
% =====================================================================
ax3 = AX(1,3);
axes(ax3);
r  = sort(abs(res)/sigd);
cp = (1:numel(r))'/numel(r)*100;
hold(ax3,'on');
hC = plot(ax3, r, cp, '-', 'Color', S.case1.col, 'LineWidth', S.lw);
h2 = plot(ax3, [2 2], [0 100], '--', 'Color', S.black, 'LineWidth', S.lwThin);
hold(ax3,'off');
xlim(ax3,[0 max(3, min(6, max(r)))]);
ylim(ax3,[0 100]);
gk_axes(ax3);
gk_label(ax3, '$|\mathrm{residual}|/\sigma_d$', ...
              'Cumulative share of points (\%)', 'Residual size distribution');
% One shared key for the whole figure, placed in the reserved bottom strip.
% A key inside (a) or (b) covered the rising limb and the residual trace.
lgA = gk_legend(ax1, [hR hM hE hB], ...
    {'Digitised benchmark solution', 'Present convolution solution', ...
     'Residual $\hat{T}_{\mathrm{num}}-\hat{T}_{\mathrm{ref}}$', ...
     'Digitisation floor $\pm2\sigma_d$'}, 'southoutside', 'cols', 2);
set(lgA,'Units','normalized');
lpa = get(lgA,'Position');
set(lgA,'Position',[0.5-lpa(3)/2, 0.035, lpa(3), lpa(4)]);

% (c) carries only the threshold marker; the CDF itself needs no key.
% The dashed marker is already identified on the shared key; annotate only
% the quantitative result so nothing overlaps in this narrow panel.
text(ax3, 0.95, 0.22, sprintf('$%.1f\\%%$ of points\nwithin $2\\sigma_d$', within), ...
     'Units','normalized','Interpreter','latex','FontSize',S.fsAnnot, ...
     'HorizontalAlignment','right','VerticalAlignment','middle');
gk_panel(ax3,'c');

% Parameter provenance ("literature parameters, no fitting") belongs in the
% caption, not across the figure. The title carries only the identification
% of the case and the three headline agreement metrics.
gk_suptitle(fig, { ...
  sprintf('External validation of the forward operator: %s', caseName), ...
  sprintf('NRMSE $=%.3f\\%%$, \\quad RMSE $=%s$, \\quad $n=%d$', ...
          nrmse, gk_sci(rmse), round(npts)) });

gk_finish(fig, stem);
close(fig);

fprintf('    %s: NRMSE=%.4f%%  RMSE=%.4e  n=%d  within2sd=%.2f%%\n', ...
        tag, nrmse, rmse, round(npts), within);
end
