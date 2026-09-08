function lg = gk_legend(ax, h, labels, loc, varargin)
%GK_LEGEND Concise LaTeX legend with controlled placement.
%   Placement is chosen by the caller from available whitespace and is
%   independent of the plotting geometry, so a legend never has to be
%   traded against the data. Any '*outside' location is collision-free by
%   construction.
%
%   lg = gk_legend(ax, h, labels, 'northeast')
%   lg = gk_legend(ax, h, labels, 'southoutside', 'cols', 3)

S = gk_style();
cols = 1;
for k = 1:2:numel(varargin)
    if strcmpi(varargin{k}, 'cols')
        cols = varargin{k+1};
    end
end

if nargin < 4 || isempty(loc)
    loc = 'northeast';
end

lg = legend(ax, h, labels{:});
set(lg, 'Interpreter','latex', ...
        'FontSize', S.fsLegend, ...
        'FontName', gk_font(), ...
        'Location', loc, ...
        'Box','off', ...            % clean: no heavy legend frame
        'Color','none');

if cols > 1
    try
        set(lg, 'NumColumns', cols);
    catch
        % older interpreter: single column is an acceptable fallback
    end
end
end
