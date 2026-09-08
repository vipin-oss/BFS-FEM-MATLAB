function s = gk_sci(v, nd)
%GK_SCI Format a number as LaTeX scientific notation, e.g. 3.84\times10^{-3}.
%   MATLAB's %e produces "3.84e-03", which reads as raw output in a
%   publication figure. This renders it as proper mathematics instead.
if nargin < 2 || isempty(nd), nd = 2; end
if v == 0, s = '0'; return; end
e = floor(log10(abs(v)));
m = v / 10^e;
s = sprintf('%.*f\\times 10^{%d}', nd, m, e);
end
