function gk_panel(ax, letter, varargin)
%GK_PANEL Panel label (a), (b), ... in a fixed position OUTSIDE the axes.
%   Identical relative placement in every panel of every figure, above the
%   axes box and clear of the title, so a panel label can never overprint a
%   title, a curve or a tick label.
%
%   gk_panel(ax,'a')
%   gk_panel(ax,'a','dx',-0.02,'dy',0.01)

S  = gk_style();
dx = 0; dy = 0;
for k = 1:2:numel(varargin)
    switch lower(varargin{k})
        case 'dx', dx = varargin{k+1};
        case 'dy', dy = varargin{k+1};
    end
end

label = sprintf('(%s)', letter);
text(ax, -0.16 + dx, 1.20 + dy, label, ...
    'Units','normalized', ...
    'FontWeight','bold', ...
    'FontSize', S.fsPanel, ...
    'FontName', gk_font(), ...
    'VerticalAlignment','bottom', ...
    'HorizontalAlignment','left', ...
    'Interpreter','tex', ...
    'Clipping','off');
end
