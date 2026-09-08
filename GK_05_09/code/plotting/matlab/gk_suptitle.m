function h = gk_suptitle(fig, txt)
%GK_SUPTITLE Figure-level title drawn in the margin reserved by gk_grid.
%
%   Implemented as a TEXT object in normalised figure coordinates rather
%   than an annotation textbox. A textbox re-wraps its contents to the box
%   width, which silently turned two-line titles into three lines and
%   pushed the first line off the canvas. A text object with an explicit
%   cell array of lines renders exactly the lines it is given, centred, and
%   grows upward from a fixed anchor, so nothing can be clipped.
%
%   txt may be a char array (newline separated) or a cell array of lines.

S = gk_style();

% JOURNAL STYLE. In the submitted manuscript each figure carries a full
% caption, so an in-graphic super-title duplicates information that the
% caption already provides and consumes vertical space. Super-titles are
% therefore suppressed by default. Set GK_SHOW_SUPTITLE = true in the base
% workspace to restore them for standalone/screen use.
show = false;
try
    show = evalin('base', 'GK_SHOW_SUPTITLE');
catch
    show = false;
end
if ~show
    h = [];
    return
end


if ischar(txt)
    lines = strsplit(txt, sprintf('\n'));
else
    lines = txt;
end

% Anchor the TOP of the block a fixed pad below the canvas edge and let the
% text grow downward. gk_grid reserves the space above the first panel.
topPad = 0.018;

% An invisible full-canvas axes hosts the title, which keeps normalised
% figure coordinates while avoiding backend-specific text-on-figure limits.
hostTag = 'gk_suptitle_host';
host = findall(fig, 'Type','axes', 'Tag', hostTag);
if isempty(host)
    host = axes('Parent', fig, 'Units','normalized', ...
                'Position',[0 0 1 1], 'Tag', hostTag);
end
set(host, 'Visible','off', 'XLim',[0 1], 'YLim',[0 1], 'HitTest','off');

h = text('Parent', host, ...
    'Units','normalized', ...
    'Position', [0.5, 1 - topPad, 0], ...
    'String', lines, ...
    'HorizontalAlignment','center', ...
    'VerticalAlignment','top', ...
    'FontSize', S.fsSuper, ...
    'FontName', gk_font(), ...
    'Interpreter','latex', ...
    'Clipping','off');
end
