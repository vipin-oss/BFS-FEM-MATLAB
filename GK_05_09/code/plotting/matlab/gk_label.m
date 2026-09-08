function gk_label(ax, xs, ys, ts)
%GK_LABEL Set x label, y label and title with the LaTeX interpreter.
%   Centralising this removes the class of defect where a mathematical
%   string was passed to an axis without 'Interpreter','latex' and rendered
%   as raw text such as "$tau_q$" or "au_q".
%
%   Pass [] to leave an entry unchanged.

S = gk_style();
fn = gk_font();

if nargin >= 2 && ~isempty(xs)
    xlabel(ax, xs, 'Interpreter','latex', 'FontSize', S.fsAxis, 'FontName', fn);
end
if nargin >= 3 && ~isempty(ys)
    ylabel(ax, ys, 'Interpreter','latex', 'FontSize', S.fsAxis, 'FontName', fn);
end
if nargin >= 4 && ~isempty(ts)
    title(ax, ts, 'Interpreter','latex', 'FontSize', S.fsTitle, ...
          'FontWeight','normal', 'FontName', fn);
end
end
