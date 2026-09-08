function gk_axes(ax, varargin)
%GK_AXES Apply the house axis convention to one axes object.
%   Outward ticks, no top/right clutter, light grid, consistent tick length
%   and font. Applying this everywhere is what makes the eleven figures look
%   like one coherent set rather than eleven separate plots.
%
%   gk_axes(ax)                 default: box off, grid on
%   gk_axes(ax,'grid','off')    suppress the grid
%   gk_axes(ax,'box','on')      keep a full box (3-D axes need this)

S = gk_style();
wantGrid = 'on';
wantBox  = S.box;
for k = 1:2:numel(varargin)
    switch lower(varargin{k})
        case 'grid', wantGrid = varargin{k+1};
        case 'box',  wantBox  = varargin{k+1};
    end
end

set(ax, 'FontName', gk_font(), ...
        'FontSize', S.fsTick, ...
        'LineWidth', S.lwAxis, ...
        'TickDir', S.tickDir, ...
        'TickLength', S.tickLen, ...
        'Box', wantBox, ...
        'Layer', 'top', ...
        'TickLabelInterpreter', 'latex');

if strcmpi(wantGrid, 'on')
    set(ax, 'XGrid','on', 'YGrid','on', ...
            'GridAlpha', S.gridAlpha, 'GridLineStyle','-');
else
    set(ax, 'XGrid','off', 'YGrid','off');
end
end
