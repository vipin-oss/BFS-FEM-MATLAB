function S = gk_style()
%GK_STYLE Single source of truth for the visual language of Figures 1-9.
%   APPEARANCE ONLY. No scientific value is defined, derived or altered here.
%
%   NOTATION. Symbols follow the manuscript exactly:
%       \tau_q   relaxation time      (manuscript macro \tq)
%       \kappa^2 nonlocal coefficient (manuscript macro \kk)
%       B        resonance number     (manuscript macro \Bnum)
%       \alpha   diffusivity
%       N_x      finite-difference grid points
%       p        observed convergence order
%       \sigma   noise standard deviation
%       \mathrm{s.e.}  standard error
%
%   TERMINOLOGY. Curves are named for what they scientifically are. The
%   informal labels "this work", "published", "our result" are never used:
%       Reference solution      digitised published result
%       Present model           the model solved here
%       Numerical solution      finite-difference solution
%       Analytical solution     closed-form limit
%       Literature calibration  parameter set reported in the literature

% ---- typography -------------------------------------------------------
% One size system for every figure. Designed at S.wFull and inserted at
% \textwidth (scale ~0.91), so 8 pt declared lands near 7.3 pt printed.
S.fontName   = 'Times';
S.fsAxis     = 9.0;      % axis labels
S.fsTick     = 8.0;      % tick labels
S.fsLegend   = 8.0;      % legend entries
S.fsTitle    = 9.0;      % panel titles
S.fsPanel    = 10.0;     % (a) (b) (c) letters
S.fsAnnot    = 8.0;      % in-axes annotation
S.fsSuper    = 9.5;      % figure super-title
S.fsFloor    = 8.0;      % HARD floor, enforced in gk_finish

% ---- line and marker weights -----------------------------------------
S.lw         = 1.3;
S.lwThin     = 0.9;
S.lwAxis     = 0.75;
S.ms         = 4.5;
S.msSmall    = 3.4;

% ---- canvas widths (inches) ------------------------------------------
S.wFull      = 6.9;
S.wHalf      = 3.45;

% ---- tick and axis convention (requirement B) ------------------------
S.tickDir    = 'out';    % outward-facing ticks
S.tickLen    = [0.018 0.018];
S.box        = 'off';    % no top/right clutter
S.gridAlpha  = 0.12;

% ---- Okabe-Ito colour-blind-safe palette -----------------------------
S.black     = [  0   0   0]/255;
S.orange    = [230 159   0]/255;
S.sky       = [ 86 180 233]/255;
S.green     = [  0 158 115]/255;
S.yellow    = [240 228  66]/255;
S.blue      = [  0 114 178]/255;
S.vermil    = [213  94   0]/255;
S.purple    = [204 121 167]/255;
S.grey      = [110 110 110]/255;
S.lightgrey = [0.86 0.86 0.86];

% =====================================================================
% FIXED SCIENTIFIC IDENTITIES - identical in every figure of the paper
% Every identity carries colour AND line style AND marker, so the set
% remains readable in greyscale and for colour-blind readers.
% =====================================================================

% candidate models
S.model.Fourier = struct('col',S.blue,  'ls','-',  'mk','o','name','Fourier');
S.model.MCV     = struct('col',S.vermil,'ls','--', 'mk','s','name','MCV');
S.model.Nyiri   = struct('col',S.green, 'ls','-.', 'mk','^','name','Nyiri');
S.model.GK      = struct('col',S.black, 'ls',':',  'mk','d','name','GK');

% solution roles
S.ref    = struct('col',S.grey,   'ls','none','mk','o');  % reference solution
S.num    = struct('col',S.vermil, 'ls','-',   'mk','none');% present/numerical
S.resid  = struct('col',S.blue,   'ls','-',   'mk','none');% residual trace
S.bandCol= S.green;                                        % tolerance band

% the two reference cases
S.case1  = struct('col',S.blue,   'ls','-',  'mk','o');   % resonance
S.case2  = struct('col',S.vermil, 'ls','--', 'mk','s');   % over-diffusive

% parameters, used wherever several parameters share one axes
S.par.tau   = struct('col',S.blue,  'ls','-',  'mk','o');
S.par.kappa = struct('col',S.vermil,'ls','--', 'mk','s');
S.par.alpha = struct('col',S.green, 'ls','-.', 'mk','^');
S.par.B     = struct('col',S.purple,'ls',':',  'mk','d');

% estimators
S.fisher = struct('col',S.grey,  'ls','-', 'mk','none');
S.mc     = struct('col',S.blue,  'ls','none','mk','o');

% literature calibration membership
S.inBand  = S.blue;
S.outBand = S.vermil;
S.withUnc = S.purple;

% emphasis
S.bandFace  = S.vermil;   % ill-conditioned band shading
S.resonance = S.black;    % the B = 1 marker line
end
