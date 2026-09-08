function c = gk_tint(col, frac)
%GK_TINT Blend a colour towards white and return an opaque RGB triple.
%   Shaded regions are drawn as pre-blended SOLID colours rather than with
%   'FaceAlpha'. Transparency is unreliable in vector (painters) output:
%   several backends rasterise or ignore it, which produced banded gradient
%   artefacts in place of flat tints. Pre-blending is exactly equivalent
%   visually over a white page and is safe in every renderer and in print.
%
%   c = gk_tint([0.83 0.37 0], 0.18)   18 % of the colour over white
if nargin < 2 || isempty(frac), frac = 0.18; end
frac = max(0, min(1, frac));
c = 1 - frac*(1 - col);
end
