function gk_arrow(ax, x0, y0, x1, y1, col, lw, headLen)
%GK_ARROW Data-space arrow drawn from plain line segments.
%   Used by the geometry schematic. Implemented as line segments rather
%   than annotation() so the arrow lives in DATA coordinates and therefore
%   stays correctly attached to the schematic at any figure size, and so it
%   behaves identically on MATLAB and GNU Octave.

if nargin < 8 || isempty(headLen)
    headLen = 0.055;
end
if nargin < 7 || isempty(lw)
    lw = 1.2;
end

plot(ax, [x0 x1], [y0 y1], '-', 'Color', col, 'LineWidth', lw);

th = atan2(y1 - y0, x1 - x0);
a  = 0.42;                       % half-angle of the arrow head
plot(ax, [x1 x1-headLen*cos(th-a)], [y1 y1-headLen*sin(th-a)], '-', ...
     'Color', col, 'LineWidth', lw);
plot(ax, [x1 x1-headLen*cos(th+a)], [y1 y1-headLen*sin(th+a)], '-', ...
     'Color', col, 'LineWidth', lw);
end
