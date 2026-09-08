% FIG08  Practical-identifiability parameter map in B.
%
% TYPE      : 3-panel  (semilog multi-parameter curves with shaded regime
%                       bands + zoomed band detail + heatmap)
% PANELS    : (a) Fisher s.e. of tau_q, kappa^2, alpha and B against B,
%                 with the verified >10/20/50/100 % regions shaded
%             (b) the same four standard errors on a linear ordinate,
%                 restricted to the well-conditioned range, so the reader
%                 can see that alpha and B are FLAT and small
%             (c) heatmap of s.e. by parameter and B: the whole story in
%                 one glance
% DATA      : identifiability_results.csv, bands.csv
% VERIFIED  : bands  >10 %  [0.44148437106171845, 3.4644170823980507]
%                    >20 %  [0.6279354286502288, 1.8044487761925194]
%                    >50 %  [0.8167166050159778, 1.2515715831250502]
%                    >100 % [0.9011515408884849, 1.115885560523925]
%
% ===================== THE CENTRAL SCOPE STATEMENT ======================
% This figure is the one that PREVENTS the over-claim. It shows that at
% B = 1 the standard errors of tau_q and kappa^2 diverge while those of
% alpha and B stay small and almost flat. The correct conclusion is that
% the (tau_q, kappa^2) SPLIT is not identifiable, NOT that GK parameters
% are unidentifiable.
%
% BUG FIXED HERE: the previous version emitted a literal "100\%" because a
% LaTeX escape leaked into a non-LaTeX string. Every percent sign in this
% script is written for the interpreter actually in use: '\%' inside
% 'Interpreter','latex' strings, and a bare '%' inside sprintf output that
% is rendered with the tex interpreter.
% ========================================================================

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

ID = gk_readcsv('identifiability_results.csv');
BD = gk_readcsv('bands.csv');

B    = ID.B;
seTq = ID.se_tau_q_pct;
seK2 = ID.se_kappa2_pct;
seAl = ID.se_alpha_pct;
seB  = ID.se_B_pct;

fig = figure('Units','inches','Position',[1 1 S.wFull 3.00], ...
             'Color','w','Visible','off');
AX = gk_grid(fig, 1, 3, 'top',0.190, 'bottom',0.180, 'hgap',0.135, ...
             'left',0.082, 'right',0.075);

% =====================================================================
% (a) all four standard errors, log ordinate, regime bands shaded
% =====================================================================
ax1 = AX(1,1);
axes(ax1);
hold(ax1,'on');

% shaded regime bands, palest = widest. Drawn first so curves sit on top.
%
% This figure's design (and its manuscript caption) shows exactly the four
% criteria 10/20/50/100%. bands.csv is shared with the manuscript's design
% table (tab:design), which separately added a 30% row; that row is
% deliberately excluded here so this panel continues to match its own
% published caption ("...exceeds 10, 20, 50 and 100%") rather than silently
% growing to five bands because the shared CSV grew.
keep = ismember(BD.criterion_pct, [10 20 50 100]);
critPct = BD.criterion_pct(keep);
Blo     = BD.B_lo(keep);
Bhi     = BD.B_hi(keep);

shades = [0.10 0.16 0.24 0.34];
[~, ord] = sort(critPct);                   % 10, 20, 50, 100
for k = 1:numel(ord)
    i  = ord(k);
    lo = Blo(i); hi = Bhi(i);
    gk_band(ax1, lo, hi, 1e-1, 1e10, S.bandFace, shades(k));
end

hTq = plot(ax1, B, seTq, '-o',  'Color', S.blue,   'LineWidth', S.lw, 'MarkerSize', S.msSmall, 'MarkerFaceColor', S.blue);
hK2 = plot(ax1, B, seK2, '--s', 'Color', S.vermil, 'LineWidth', S.lw, 'MarkerSize', S.msSmall, 'MarkerFaceColor', S.vermil);
hAl = plot(ax1, B, seAl, '-.^', 'Color', S.green,  'LineWidth', S.lw, 'MarkerSize', S.msSmall, 'MarkerFaceColor', S.green);
hB  = plot(ax1, B, seB,  ':d',  'Color', S.purple, 'LineWidth', S.lw, 'MarkerSize', S.msSmall, 'MarkerFaceColor', S.purple);
plot(ax1, [1 1], [1e-1 1e10], '--', 'Color', S.black, 'LineWidth', 0.9);

set(ax1,'YScale','log');
set(ax1,'YTick',10.^(0:3:12));
ylim(ax1,[3e-1 1e13]);
xlim(ax1,[0 5.2]);
hold(ax1,'off');
gk_axes(ax1);
gk_label(ax1,'Resonance number $B$', ...
              'Fisher $\mathrm{s.e.}$ (\%)', ...
              'Standard error of all four parameters');
gk_legend(ax1,[hTq hK2 hAl hB], ...
    {'$\mathrm{s.e.}(\tau_q)$','$\mathrm{s.e.}(\kappa^{2})$', ...
     '$\mathrm{s.e.}(\alpha)$','$\mathrm{s.e.}(B)$'},'northeast','cols',2);
gk_panel(ax1,'a');

% =====================================================================
% (b) linear view: alpha and B are flat and small
% =====================================================================
ax2 = AX(1,2);
axes(ax2);
hold(ax2,'on');
hA2 = plot(ax2, B, seAl, '-.^', 'Color', S.green,  'LineWidth', S.lw, ...
     'MarkerSize', S.msSmall, 'MarkerFaceColor', S.green);
hB2 = plot(ax2, B, seB,  ':d',  'Color', S.purple, 'LineWidth', S.lw, ...
     'MarkerSize', S.msSmall, 'MarkerFaceColor', S.purple);
plot(ax2, [1 1], [0 14], '--', 'Color', S.black, 'LineWidth', 0.9);
hold(ax2,'off');
ylim(ax2,[0 14]); xlim(ax2,[0 5.2]);
gk_axes(ax2);
gk_label(ax2,'Resonance number $B$', ...
              'Fisher $\mathrm{s.e.}$ (\%)', ...
              '$\alpha$ and $B$ remain identifiable');
gk_legend(ax2,[hA2 hB2], ...
    {'$\mathrm{s.e.}(\alpha)$','$\mathrm{s.e.}(B)$'},'northeast');

gk_panel(ax2,'b');

% =====================================================================
% (c) heatmap: log10 s.e. by parameter and B
% =====================================================================
ax3 = AX(1,3);
axes(ax3);
Mse = [seTq.'; seK2.'; seAl.'; seB.'];
Lm  = log10(Mse);

% pcolor on an explicit cell grid rather than imagesc: imagesc produces an
% image object, which the painters vector renderer does not emit reliably,
% and the panel came out blank. pcolor emits real vector patches.
[nP, nB] = size(Lm);
Xe = 0.5:(nB+0.5);
Ye = 0.5:(nP+0.5);
Zp = nan(nP+1, nB+1);
Zp(1:nP, 1:nB) = Lm;
hP = pcolor(ax3, Xe, Ye, Zp);
set(hP,'EdgeColor',[1 1 1],'LineWidth',0.3);
colormap(ax3, gk_cmap());
set(ax3,'YDir','normal');
set(ax3,'YTick',1:nP,'YTickLabel',{'$\tau_q$','$\kappa^{2}$','$\alpha$','$B$'});
% Label a readable subset of the 15 computed B values: the endpoints, the
% resonance and two intermediate points. Every column is still drawn.
want = [0.1 0.5 1.0 2.0 5.0];
xt = zeros(1,numel(want));
for q = 1:numel(want)
    [~, xt(q)] = min(abs(B - want(q)));
end
xt = unique(xt);
set(ax3,'XTick',xt,'XTickLabel', ...
    arrayfun(@(v) sprintf('$%g$',v), B(xt), 'UniformOutput', false));
xlim(ax3,[0.5 nB+0.5]); ylim(ax3,[0.5 nP+0.5]);
gk_axes(ax3,'grid','off');
gk_label(ax3,'Resonance number $B$',[], ...
              'Standard-error map');
cb = colorbar(ax3,'eastoutside');
set(get(cb,'Label'),'String','$\log_{10}\,\mathrm{s.e.}$ (\%)', ...
    'Interpreter','latex','FontSize',S.fsAxis);
hold(ax3,'on');
[~, i1] = min(abs(B - 1.0));
plot(ax3, [i1 i1], [0.5 nP+0.5], '-', 'Color', S.black, 'LineWidth', 1.4);
hold(ax3,'off');
gk_panel(ax3,'c');

gk_suptitle(fig, {'Practical identifiability in $B$: only the $(\tau_q,\kappa^{2})$ split degrades'});

gk_finish(fig, 'fig08_parameter_map');
close(fig);

fprintf('    bands plotted in this figure:');
for k = 1:numel(critPct)
    fprintf(' >%g%%[%.4f,%.4f]', critPct(k), Blo(k), Bhi(k));
end
fprintf('\n');
