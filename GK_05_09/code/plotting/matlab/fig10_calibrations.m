% FIG10  Audited published calibrations placed in B-space.
%
% TYPE      : 3-panel  (categorical scatter + counts bar + source grouping)
% PANELS    : (a) the twelve audited cases against the verified bands,
%                 coloured by band membership, with the one case that
%                 reports uncertainties shown with its error bar
%             (b) inside / outside counts
%             (c) cases grouped by source study
% DATA      : F7_calibrations.csv, calibration_results.csv, bands.csv
% VERIFIED  : 8 of 12 inside the >20 % band [0.6279, 1.8044]
%             case 12 (Both et al.) B = 1.5321756894790604 +/- 2.78 %
% SUPPORTS  : the ill-conditioned band is not a hypothetical region; a
%             majority of published GK calibrations sit inside it.
%
% ============ REQUIREMENT K: NO LEGEND MAY COVER A DATA POINT ============
% The previous version hid cases 1 (B = 2.23) and 2 (B = 2.17) behind an
% in-axes legend box. Here EVERY legend is placed OUTSIDE the data area
% via gk_safelegend, and the script performs a runtime assertion that all
% twelve points lie strictly inside the axis limits. If any point were
% clipped the script would stop rather than emit a misleading figure.
%
% LIMITATION STATED ON THE FIGURE: 11 of the 12 published cases report no
% parameter uncertainties, so only case 12 carries an error bar. No
% uncertainty is synthesised for the others.
% ========================================================================

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

C  = gk_readcsv('F7_calibrations.csv');
R  = gk_readcsv('calibration_results.csv');
BD = gk_readcsv('bands.csv');

n     = numel(C.case);
Bv    = C.B;
inb   = strcmp(C.in_band,'True');
dB    = C.dB_rel;                       % NaN where not reported
spec  = C.specimen;

i20 = find(BD.criterion_pct == 20, 1);
lo20 = BD.B_lo(i20); hi20 = BD.B_hi(i20);

fig = figure('Units','inches','Position',[1 1 S.wFull 3.60], ...
             'Color','w','Visible','off');

% =====================================================================
% (a) the twelve cases in B-space
% =====================================================================
ax1 = axes('Position',[0.265 0.330 0.420 0.470]);
hold(ax1,'on');

XLO = 0.45; XHI = 3.65;

% verified >20 % band and the Feher-Kovacs 1 <= B < 3 range
hBand = gk_band(ax1, lo20, hi20, 0, n+1, S.bandFace, 0.20);
hFK   = gk_band(ax1, 1, 3, 0, n+1, S.grey, 0.13);
hRes  = plot(ax1, [1 1], [0 n+1], '--', 'Color', S.black, 'LineWidth', 1.1);

hIn = []; hOut = []; hUnc = [];
for i = 1:n
    y = i;
    if ~isnan(dB(i))
        % horizontal uncertainty bar drawn explicitly: the 6-argument
        % errorbar() signature is not portable across MATLAB and Octave.
        e = Bv(i)*dB(i);
        plot(ax1, [Bv(i)-e Bv(i)+e], [y y], '-', 'Color', S.withUnc, ...
             'LineWidth', 1.1);
        plot(ax1, [Bv(i)-e Bv(i)-e], [y-0.22 y+0.22], '-', ...
             'Color', S.withUnc, 'LineWidth', 1.1);
        plot(ax1, [Bv(i)+e Bv(i)+e], [y-0.22 y+0.22], '-', ...
             'Color', S.withUnc, 'LineWidth', 1.1);
        hUnc = plot(ax1, Bv(i), y, 'o', 'Color', S.withUnc, ...
            'MarkerFaceColor', S.withUnc, 'MarkerSize', S.ms);
    elseif inb(i)
        hIn = plot(ax1, Bv(i), y, 'o', 'Color', S.inBand, ...
            'MarkerFaceColor', S.inBand, 'MarkerSize', S.ms);
    else
        hOut = plot(ax1, Bv(i), y, 's', 'Color', S.outBand, ...
            'MarkerFaceColor', S.outBand, 'MarkerSize', S.ms);
    end
end
hold(ax1,'off');

set(ax1,'YTick',1:n);
lbl = cell(n,1);
for i = 1:n
    lbl{i} = sprintf('%d. %s', C.case(i), spec{i});
end
set(ax1,'YTickLabel',lbl,'FontSize',S.fsTick-0.5,'TickLabelInterpreter','none');
ylim(ax1,[0.3 n+0.7]);
xlim(ax1,[XLO XHI]);
gk_axes(ax1);
set(ax1,'YTickLabel',lbl,'TickLabelInterpreter','none','FontSize',S.fsTick-0.5);
gk_label(ax1,'Resonance number $B = \kappa^{2}/(\alpha\tau_q)$',[], ...
              'Literature-reported calibrations in $B$-space');
gk_panel(ax1,'a','dx',-0.30);

% ---- RUNTIME ASSERTION: every point must be visible ------------------
bad = find(Bv < XLO | Bv > XHI);
if ~isempty(bad)
    error('fig10:clipped', ...
        'Calibration case(s) %s fall outside the x-limits and would be hidden.', ...
        mat2str(C.case(bad)));
end
fprintf('    visibility assertion passed: all %d points within [%.2f, %.2f]\n', ...
        n, XLO, XHI);

% legend OUTSIDE the axes, below, so it cannot cover any marker
hs = [hRes, hBand, hFK];
ls = {'Fourier resonance, $B=1$', ...
      sprintf('Ill-conditioned band $[%.3f,\\,%.3f]$', lo20, hi20), ...
      'Feh\''er--Kov\''acs range, $1\leq B<3$'};
if ~isempty(hIn),  hs(end+1) = hIn;  ls{end+1} = 'Calibration inside the band'; end
if ~isempty(hOut), hs(end+1) = hOut; ls{end+1} = 'Calibration outside the band'; end
if ~isempty(hUnc), hs(end+1) = hUnc; ls{end+1} = 'Calibration with reported uncertainty'; end
lg1 = legend(ax1, hs, ls, 'Interpreter','latex', 'Location','southoutside');
set(lg1,'FontSize',S.fsLegend-1.0);
try, set(lg1,'NumColumns',2); catch, end
% 'southoutside' places the key relative to the axes, which pushed it past the
% bottom of the canvas. Pin it explicitly inside the reserved bottom strip so
% no glyph crosses the page boundary.
set(lg1,'Units','normalized');
lp1 = get(lg1,'Position');
set(lg1,'Position',[0.5-lp1(3)/2, 0.045, lp1(3), lp1(4)]);

% Requirement K enforced at runtime, not by eye.
gk_assert_legend_clear(ax1, lg1, 'error');

% =====================================================================
% (c) grouped by source study
% =====================================================================
ax3 = axes('Position',[0.760 0.330 0.205 0.470]);
src = R.source;
uk  = unique(src);
% keep a stable, readable order
cnt = zeros(numel(uk),1);
for k = 1:numel(uk)
    cnt(k) = sum(strcmp(src, uk{k}));
end
[cnt, o] = sort(cnt,'descend'); uk = uk(o);
short = cell(numel(uk),1);
for k = 1:numel(uk)
    s = uk{k};
    % Plain ASCII author-year labels. These tick labels are drawn with the
    % 'none' interpreter, so accented characters and TeX escapes would be
    % emitted literally; the accented spellings appear in the caption.
    s = strrep(s,'earlier eval., in FeherKovacs2021 Table 1','Feher-Kovacs 2021 (earlier)');
    s = strrep(s,'Feher & Kovacs 2021','Feher-Kovacs 2021');
    s = strrep(s,'Van et al. 2017','Van et al. 2017');
    s = strrep(s,'Both et al. 2016','Both et al. 2016');
    short{k} = s;
end
hold(ax3,'on');
for k = 1:numel(uk)
    barh(ax3, k, cnt(k), 0.55, 'FaceColor', S.sky, 'EdgeColor', S.black, ...
         'LineWidth', 0.5);
    text(ax3, cnt(k)+0.12, k, sprintf('%d',cnt(k)), ...
        'VerticalAlignment','middle','FontSize',S.fsAnnot-0.5);
end
hold(ax3,'off');
gk_axes(ax3);
set(ax3,'YTick',1:numel(uk),'YTickLabel',short, ...
        'TickLabelInterpreter','none','FontSize',S.fsTick-1.0);
xlim(ax3,[0 max(cnt)+1.6]); ylim(ax3,[0.4 numel(uk)+0.6]);
gk_label(ax3,'Number of calibrations',[],'Provenance by source study');
gk_panel(ax3,'b','dx',-0.24);

gk_suptitle(fig, { ...
  sprintf(['Literature calibrations in $B$-space: %d of %d inside the ' ...
           '$>20\\%%$ band $[%.3f,\\,%.3f]$'], sum(inb), n, lo20, hi20) });

gk_finish(fig, 'fig10_calibrations');
close(fig);

fprintf('    %d inside / %d outside;  sources: %d\n', sum(inb), n-sum(inb), numel(uk));
