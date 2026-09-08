% FIG01  Geometry and problem setup.
%
% TYPE      : schematic (vector drawing) + annotated mathematical setup
% PANELS    : 2   (a) physical domain, coordinates, dimensions, BC/IC, pulse
%                 (b) governing system, T-form, conditions, resonance number
% DATA      : none plotted. This figure carries the problem definition only;
%             every symbol shown is defined in the manuscript text.
% SUPPORTS  : the 1-D scope statement and the definition B = kappa^2/(alpha tau_q)
%
% NO SCIENTIFIC VALUE IS COMPUTED HERE. The figure is a definition diagram.

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);
S = gk_style();

fig = figure('Units','inches','Position',[1 1 S.wFull 2.95], ...
             'Color','w','Visible','off');

% =====================================================================
% (a) physical domain
% =====================================================================
ax = axes('Position',[0.045 0.10 0.46 0.78]);
hold(ax,'on');
axis(ax,[-0.42 1.42 -0.52 0.92]);
axis(ax,'off');

% specimen body
fill(ax, [0 1 1 0], [-0.18 -0.18 0.40 0.40], S.lightgrey, ...
     'EdgeColor', S.black, 'LineWidth', 1.0);

% hatching so it reads as a solid
for xh = linspace(0.04, 0.96, 24)
    plot(ax, [xh xh-0.05], [-0.18 0.40], '-', 'Color', [0.72 0.72 0.72], ...
         'LineWidth', 0.4);
end

% front face: incoming heat pulse (5 arrows)
for yy = linspace(-0.11, 0.33, 5)
    gk_arrow(ax, -0.36, yy, -0.02, yy, S.vermil, 1.2);
end
text(ax, -0.39, 0.52, 'heat pulse $q_0(t)$', 'Interpreter','latex', ...
     'Color', S.vermil, 'FontSize', S.fsAnnot, 'HorizontalAlignment','left');

% rear face: measurement
plot(ax, [1 1], [-0.18 0.40], '-', 'Color', S.blue, 'LineWidth', 3.0);
gk_arrow(ax, 1.34, 0.11, 1.03, 0.11, S.blue, 1.2);
text(ax, 1.36, 0.11, {'measured','$T(L,t)$'}, 'Interpreter','latex', ...
     'Color', S.blue, 'FontSize', S.fsAnnot, ...
     'HorizontalAlignment','left', 'VerticalAlignment','middle');

% adiabatic rear-face condition
text(ax, 0.50, 0.60, 'adiabatic rear face: $q(L,t)=0$', 'Interpreter','latex', ...
     'FontSize', S.fsAnnot, 'HorizontalAlignment','center');

% interior labels
text(ax, 0.50, 0.20, '$T(x,t),\; q(x,t)$', 'Interpreter','latex', ...
     'FontSize', S.fsAnnot, 'HorizontalAlignment','center');
text(ax, 0.50, 0.02, 'specimen', 'FontSize', S.fsAnnot, ...
     'HorizontalAlignment','center');

% coordinate axis with dimensions
plot(ax, [0 1.18], [-0.34 -0.34], '-', 'Color', S.black, 'LineWidth', 0.8);
plot(ax, [1.14 1.18 1.14], [-0.36 -0.34 -0.32], '-', 'Color', S.black, ...
     'LineWidth', 0.8);
text(ax, 1.21, -0.34, '$x$', 'Interpreter','latex', 'FontSize', S.fsAnnot);
plot(ax, [0 0], [-0.30 -0.38], '-', 'Color', S.black, 'LineWidth', 0.8);
plot(ax, [1 1], [-0.30 -0.38], '-', 'Color', S.black, 'LineWidth', 0.8);
text(ax, 0, -0.46, '$0$', 'Interpreter','latex', 'FontSize', S.fsAnnot, 'HorizontalAlignment','center');
text(ax, 1, -0.46, '$L$', 'Interpreter','latex', 'FontSize', S.fsAnnot, 'HorizontalAlignment','center');
text(ax, 0.02, 0.46, '$x=0$', 'Interpreter','latex', 'FontSize', S.fsAnnot, 'HorizontalAlignment','left');
text(ax, 0.98, 0.46, '$x=L$', 'Interpreter','latex', 'FontSize', S.fsAnnot, 'HorizontalAlignment','right');

hold(ax,'off');
% The schematic axes are 'axis off' with custom limits, so the panel label is
% placed explicitly in figure coordinates rather than via the axes-relative
% default, which would fall outside the visible canvas.
annotation(fig,'textbox',[0.035 0.878 0.05 0.08],'String','(a)', ...
    'EdgeColor','none','FontWeight','bold','FontSize',S.fsPanel, ...
    'FontName',gk_font(),'Interpreter','tex', ...
    'HorizontalAlignment','left','VerticalAlignment','middle');

% =====================================================================
% (b) mathematical setup
% =====================================================================
ax2 = axes('Position',[0.555 0.10 0.43 0.78]);
axis(ax2,[0 1 0 1]);
axis(ax2,'off');

y = 0.985; dy = 0.079;

text(ax2, 0, y, 'Guyer--Krumhansl system', 'FontSize', S.fsAnnot, ...
     'FontWeight','bold', 'VerticalAlignment','top'); y = y - dy;
text(ax2, 0.02, y, '$\rho c\, \partial_t T = -\partial_x q$', ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top');
y = y - dy;
text(ax2, 0.02, y, ['$\tau_q\, \partial_t q + q = -\lambda\, \partial_x T' ...
     ' + \kappa^{2}\, \partial_{xx} q$'], ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top');
y = y - 1.28*dy;

text(ax2, 0, y, 'Single equation (T-form)', 'FontSize', S.fsAnnot, ...
     'FontWeight','bold', 'VerticalAlignment','top'); y = y - dy;
text(ax2, 0.02, y, ['$\tau_q\, \partial_{tt}T + \partial_t T = ' ...
     '\alpha\, \partial_{xx}T + \kappa^{2}\, \partial_{xxt}T$'], ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top');
y = y - 1.28*dy;

text(ax2, 0, y, 'Conditions', 'FontSize', S.fsAnnot, ...
     'FontWeight','bold', 'VerticalAlignment','top'); y = y - dy;
text(ax2, 0.02, y, 'IC:  $T(x,0)=0$,   $q(x,0)=0$', ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top');
y = y - dy;
text(ax2, 0.02, y, 'BC:  $q(0,t)=q_0(t)$,   $q(L,t)=0$', ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top');
y = y - dy;
text(ax2, 0.02, y, ['pulse:  $q_0 = 1-\cos(2\pi t/t_p)$,  $0<t\leq t_p$'], ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top');
y = y - 1.28*dy;

text(ax2, 0, y, 'Resonance number', 'FontSize', S.fsAnnot, ...
     'FontWeight','bold', 'VerticalAlignment','top'); y = y - dy;
text(ax2, 0.02, y, '$B = \kappa^{2}/(\alpha\tau_q)$', ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top', ...
     'Color', S.black);
y = y - dy;
text(ax2, 0.02, y, '$B = 1$:  Fourier solution recovered exactly', ...
     'Interpreter','latex','FontSize', S.fsAnnot, 'VerticalAlignment','top', ...
     'Color', S.vermil);

annotation(fig,'textbox',[0.505 0.878 0.05 0.08],'String','(b)', ...
    'EdgeColor','none','FontWeight','bold','FontSize',S.fsPanel, ...
    'FontName',gk_font(),'Interpreter','tex', ...
    'HorizontalAlignment','left','VerticalAlignment','middle');

gk_suptitle(fig, {'Problem definition: one-dimensional slab with rear-face observable'});
gk_finish(fig, 'fig01_geometry');
close(fig);

