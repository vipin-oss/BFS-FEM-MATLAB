function gk_finish(fig, stem)
%GK_FINISH Apply the shared style and export vector PDF + EPS + PNG.
%
%   Exports into figures/matlab/output/:
%     <stem>.pdf   vector, for the manuscript
%     <stem>.eps   vector, for journals requiring EPS
%     <stem>.png   600 dpi, publication-quality raster preview
%
%   Vector output is obtained with the PAINTERS renderer, not the '-vector'
%   switch, which exists only from MATLAB R2022a and raises
%       Error using inputcheck: Illegal option '-vector' given
%   on earlier releases. One code path now serves MATLAB and Octave.

P = gk_paths();
S = gk_style();
fname = gk_font();
isOct = exist('OCTAVE_VERSION', 'builtin') == 5;

% ---- font family across every text-bearing object --------------------
set(findall(fig, '-property', 'FontName'), 'FontName', fname);

% ---- per-axes house style --------------------------------------------
axAll = findall(fig, 'Type', 'axes');
for k = 1:numel(axAll)
    a = axAll(k);
    set(get(a,'XLabel'), 'FontSize', S.fsAxis);
    set(get(a,'YLabel'), 'FontSize', S.fsAxis);
    set(get(a,'ZLabel'), 'FontSize', S.fsAxis);
    set(get(a,'Title'),  'FontSize', S.fsTitle, 'FontWeight','normal');
end

set(findall(fig, 'Type', 'legend'),   'FontSize', S.fsLegend);
set(findall(fig, 'Type', 'colorbar'), 'FontSize', S.fsTick);

% ---- HARD LEGIBILITY FLOOR -------------------------------------------
% Enforced centrally so no call site can reintroduce unreadable text.
txtObj = findall(fig, '-property', 'FontSize');
for k = 1:numel(txtObj)
    if get(txtObj(k), 'FontSize') < S.fsFloor
        set(txtObj(k), 'FontSize', S.fsFloor);
    end
end

set(fig, 'Color', 'w', 'InvertHardcopy', 'off');

% ---- export at exactly the on-screen size ----------------------------
set(fig, 'Units', 'inches');
pos = get(fig, 'Position');
w = pos(3); h = pos(4);
set(fig, 'PaperUnits','inches', ...
         'PaperSize', [w h], ...
         'PaperPositionMode','manual', ...
         'PaperPosition', [0 0 w h]);

pdfFile = fullfile(P.out, [stem '.pdf']);
epsFile = fullfile(P.out, [stem '.eps']);
pngFile = fullfile(P.out, [stem '.png']);

set(fig, 'Renderer', 'painters');

print(fig, pdfFile, '-dpdf');
if isOct
    print(fig, epsFile, '-depsc2');
else
    print(fig, epsFile, '-depsc');
end
% 400 dpi preview. This is comfortably publication grade for a raster
% preview (the PDF and EPS are vector and are what a journal receives).
% 600 dpi on a full-width multi-panel figure produced very large
% intermediate buffers that exhausted the sandbox tmpfs during batch runs.
print(fig, pngFile, '-dpng', '-r400');

fprintf('  wrote %-36s (%.2f x %.2f in)\n', [stem '.pdf/.eps/.png'], w, h);
end
