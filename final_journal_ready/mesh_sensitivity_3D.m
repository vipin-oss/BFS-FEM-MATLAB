%% mesh_sensitivity_3D.m
%  3D mesh-sensitivity study for l/Lx=0.05
%  Meshes: 2x1x1 (12 nodes, 288 DOF), 4x2x2 (45 nodes, 1080 DOF), 6x3x3 (112 nodes, 2688 DOF)
%  Uses corrected mass formulation: Mscaled = Sscale*Mff*Sscale, eigs 6 modes + dense fallback

clear; clc; close all;

set(groot, 'defaultAxesFontName', 'Times New Roman');
set(groot, 'defaultAxesFontSize', 10);

Lx = 1.0; Ly = 0.20; Lz = 0.20;
E  = 200e9; nu = 0.30; rho = 7800;
traction_right = [1.0e6; 0.0; 0.0];
body_force     = [0.0; 0.0; 0.0];
bc_case        = "clamped_gradient";

l = 0.05; % l/Lx=0.05
AAT_iso = diag([l^2, l^2, l^2]);

meshes = [2 1 1; 4 2 2; 6 3 3];

fprintf('Mesh sensitivity for l=%.3f (l/Lx=%.2f)\n', l, l/Lx);
fprintf('%10s %10s %12s %12s %12s\n', 'Mesh', 'DOF', 'u_avg(um)', 'f1(Hz)', 'kappa');

for k=1:size(meshes,1)
    nelx=meshes(k,1); nely=meshes(k,2); nelz=meshes(k,3);
    nnx=nelx+1; nny=nely+1; nnz=nelz+1; nnode=nnx*nny*nnz; ndof=nnode*24;
    [u_avg, ~, f1, condest] = solve_3d_sg_rotated(Lx,Ly,Lz,E,nu,rho,nelx,nely,nelz,AAT_iso,traction_right,body_force,bc_case);
    fprintf('%2dx%1dx%1d %10d %12.4f %12.2f %12.3e\n', nelx,nely,nelz, ndof, u_avg*1e6, f1, condest);
end

function AAT_rot = build_rotated_AAT(lx, ly, lz, theta_deg)
    theta = theta_deg * pi / 180; c=cos(theta); s=sin(theta);
    R = [ c, -s, 0; s,  c, 0; 0,  0, 1]; D = diag([lx^2, ly^2, lz^2]); AAT_rot = R' * D * R;
end

function [avg_ux_right, max_umag, freq_first, cond_est] = solve_3d_sg_rotated(Lx,Ly,Lz,E,nu,rho,nelx,nely,nelz,AAT_rot,traction_right,body_force,bc_case)
    lambda = E*nu/((1+nu)*(1-2*nu)); mu = E/(2*(1+nu));
    C = [lambda+2*mu, lambda, lambda, 0,0,0; lambda, lambda+2*mu, lambda, 0,0,0; lambda, lambda, lambda+2*mu, 0,0,0; 0,0,0,mu,0,0; 0,0,0,0,mu,0; 0,0,0,0,0,mu];
    nnx=nelx+1; nny=nely+1; nnz=nelz+1; nnode=nnx*nny*nnz; ndof_per_node=24; ndof=ndof_per_node*nnode;
    xgrid=linspace(0,Lx,nnx); ygrid=linspace(0,Ly,nny); zgrid=linspace(0,Lz,nnz);
    node_id=@(ix,iy,iz) (iz-1)*nnx*nny + (iy-1)*nnx + ix;
    coords=zeros(nnode,3);
    for iz=1:nnz, for iy=1:nny, for ix=1:nnx, n=node_id(ix,iy,iz); coords(n,:)=[xgrid(ix),ygrid(iy),zgrid(iz)]; end, end, end
    conn=zeros(nelx*nely*nelz,8); e=0;
    for ez=1:nelz, for ey=1:nely, for ex=1:nelx, e=e+1; conn(e,:)=[node_id(ex,ey,ez),node_id(ex+1,ey,ez),node_id(ex+1,ey+1,ez),node_id(ex,ey+1,ez),node_id(ex,ey,ez+1),node_id(ex+1,ey,ez+1),node_id(ex+1,ey+1,ez+1),node_id(ex,ey+1,ez+1)]; end, end, end
    nel=size(conn,1); K=sparse(ndof,ndof); M=sparse(ndof,ndof); F=zeros(ndof,1);
    [gp,gw]=gauss_1d_01(3);
    m11=AAT_rot(1,1); m22=AAT_rot(2,2); m33=AAT_rot(3,3); m12=AAT_rot(1,2); m13=AAT_rot(1,3); m23=AAT_rot(2,3);
    for e=1:nel, nodes=conn(e,:); xy=coords(nodes,:); hx=xy(2,1)-xy(1,1); hy=xy(4,2)-xy(1,2); hz=xy(5,3)-xy(1,3); detJ=hx*hy*hz;
        Ke=zeros(192,192); Me=zeros(192,192); Fe=zeros(192,1);
        for ig=1:length(gp), s=gp(ig); ws=gw(ig); for jg=1:length(gp), t=gp(jg); wt=gw(jg); for kg=1:length(gp), r=gp(kg); wr=gw(kg); wgt=ws*wt*wr*detJ;
            [N,Nx,Ny,Nz,Nxx,Nyy,Nzz,Nxy,Nxz,Nyz]=hermite_shape_3d(s,t,r,hx,hy,hz);
            [B,Bx,By,Bz,Nv]=make_B_matrices_3d(N,Nx,Ny,Nz,Nxx,Nyy,Nzz,Nxy,Nxz,Nyz);
            Kcl=B.'*C*B; Kg=(1/10)*(m11*(Bx.'*C*Bx)+m22*(By.'*C*By)+m33*(Bz.'*C*Bz)+m12*(Bx.'*C*By+By.'*C*Bx)+m13*(Bx.'*C*Bz+Bz.'*C*Bx)+m23*(By.'*C*Bz+Bz.'*C*By));
            Ke=Ke+(Kcl+Kg)*wgt; Me=Me+rho*(Nv.'*Nv)*wgt; Fe=Fe+Nv.'*body_force*wgt;
        end, end, end
        edofs=element_dofs(nodes,ndof_per_node); K(edofs,edofs)=K(edofs,edofs)+Ke; M(edofs,edofs)=M(edofs,edofs)+Me; F(edofs)=F(edofs)+Fe;
    end
    for ez=1:nelz, for ey=1:nely, e_right=(ez-1)*nelx*nely+(ey-1)*nelx+nelx; nodes=conn(e_right,:); xy=coords(nodes,:); hx=xy(2,1)-xy(1,1); hy=xy(4,2)-xy(1,2); hz=xy(5,3)-xy(1,3); edofs=element_dofs(nodes,ndof_per_node); Fe=zeros(192,1); s=1.0;
        for jg=1:length(gp), t=gp(jg); wt=gw(jg); for kg=1:length(gp), r=gp(kg); wr=gw(kg); faceJ=hy*hz;
            [N,Nx,Ny,Nz,Nxx,Nyy,Nzz,Nxy,Nxz,Nyz]=hermite_shape_3d(s,t,r,hx,hy,hz); [~,~,~,~,Nv]=make_B_matrices_3d(N,Nx,Ny,Nz,Nxx,Nyy,Nzz,Nxy,Nxz,Nyz); Fe=Fe+Nv.'*traction_right*(wt*wr*faceJ);
        end, end, F(edofs)=F(edofs)+Fe;
    end, end
    fixed_dofs=[]; left_nodes=[];
    for iz=1:nnz, for iy=1:nny, left_nodes(end+1)=node_id(1,iy,iz); end, end
    for n=left_nodes, fixed_dofs=[fixed_dofs,(n-1)*24+(1:24)]; end
    fixed_dofs=unique(fixed_dofs); free_dofs=setdiff(1:ndof,fixed_dofs);
    Kff=K(free_dofs,free_dofs); Ff=F(free_dofs); Mff=M(free_dofs,free_dofs);
    scale_diag=sqrt(abs(diag(Kff))); scale_diag(scale_diag<eps)=1.0; Sscale=spdiags(1./scale_diag,0,length(free_dofs),length(free_dofs));
    Kscaled=Sscale*Kff*Sscale; Fscaled=Sscale*Ff; cond_est=condest(Kscaled);
    y=Kscaled\Fscaled; D=zeros(ndof,1); D(free_dofs)=Sscale*y;
    u_nodes=D(1:24:end); right_nodes=[];
    for iz=1:nnz, for iy=1:nny, right_nodes(end+1)=node_id(nnx,iy,iz); end, end
    avg_ux_right=mean(u_nodes(right_nodes)); max_umag=max(abs(u_nodes));
    Mscaled=Sscale*Mff*Sscale;
    try, [V_eig,D_eig]=eigs(Kscaled,Mscaled,6,'smallestabs'); omega2=sort(real(diag(D_eig))); omega2=omega2(omega2>1e-8); freq_first=sqrt(omega2(1))/(2*pi);
    catch ME, warning('Eigs failed: %s, using dense eig',ME.message); [V_full,D_full]=eig(full(Kscaled),full(Mscaled)); omega2=sort(real(diag(D_full))); omega2=omega2(omega2>1e-8); freq_first=sqrt(omega2(1))/(2*pi); end
end

function edofs=element_dofs(nodes,ndof_per_node), edofs=zeros(1,numel(nodes)*ndof_per_node); c=0; for a=1:numel(nodes), n=nodes(a); edofs(c+1:c+ndof_per_node)=(n-1)*ndof_per_node+(1:ndof_per_node); c=c+ndof_per_node; end, end
function [gp,gw]=gauss_1d_01(n), x=[-sqrt(3/5),0,sqrt(3/5)]; w=[5/9,8/9,5/9]; gp=(x+1)/2; gw=w/2; end
function [H0,H1,H0x,H1x,H0xx,H1xx]=hermite_1d_two_nodes(s,L), h1=1-3*s^2+2*s^3; h2=L*(s-2*s^2+s^3); h3=3*s^2-2*s^3; h4=L*(-s^2+s^3); dh1=-6*s+6*s^2; dh2=L*(1-4*s+3*s^2); dh3=6*s-6*s^2; dh4=L*(-2*s+3*s^2); d2h1=-6+12*s; d2h2=L*(-4+6*s); d2h3=6-12*s; d2h4=L*(-2+6*s); H0=[h1,h3]; H1=[h2,h4]; H0x=(1/L)*[dh1,dh3]; H1x=(1/L)*[dh2,dh4]; H0xx=(1/L^2)*[d2h1,d2h3]; H1xx=(1/L^2)*[d2h2,d2h4]; end
function [N,Nx,Ny,Nz,Nxx,Nyy,Nzz,Nxy,Nxz,Nyz]=hermite_shape_3d(s,t,r,hx,hy,hz), [Hx0,Hx1,Hx0x,Hx1x,Hx0xx,Hx1xx]=hermite_1d_two_nodes(s,hx); [Hy0,Hy1,Hy0y,Hy1y,Hy0yy,Hy1yy]=hermite_1d_two_nodes(t,hy); [Hz0,Hz1,Hz0z,Hz1z,Hz0zz,Hz1zz]=hermite_1d_two_nodes(r,hz); xs=[1 2 2 1 1 2 2 1]; ys=[1 1 2 2 1 1 2 2]; zs=[1 1 1 1 2 2 2 2]; N=zeros(1,64); Nx=N; Ny=N; Nz=N; Nxx=N; Nyy=N; Nzz=N; Nxy=N; Nxz=N; Nyz=N; combos=[0 0 0;1 0 0;0 1 0;0 0 1;1 1 0;1 0 1;0 1 1;1 1 1]; for a=1:8, ix=xs(a); iy=ys(a); iz=zs(a); p=(a-1)*8; for q=1:8, cx=combos(q,1); cy=combos(q,2); cz=combos(q,3); [X,Xx,Xxx]=pickH(cx,ix,Hx0,Hx1,Hx0x,Hx1x,Hx0xx,Hx1xx); [Y,Yy,Yyy]=pickH(cy,iy,Hy0,Hy1,Hy0y,Hy1y,Hy0yy,Hy1yy); [Z,Zz,Zzz]=pickH(cz,iz,Hz0,Hz1,Hz0z,Hz1z,Hz0zz,Hz1zz); id=p+q; N(id)=X*Y*Z; Nx(id)=Xx*Y*Z; Ny(id)=X*Yy*Z; Nz(id)=X*Y*Zz; Nxx(id)=Xxx*Y*Z; Nyy(id)=X*Yyy*Z; Nzz(id)=X*Y*Zzz; Nxy(id)=Xx*Yy*Z; Nxz(id)=Xx*Y*Zz; Nyz(id)=X*Yy*Zz; end, end, end
function [H,Hd,Hdd]=pickH(flag,idx,H0,H1,H0d,H1d,H0dd,H1dd), if flag==0, H=H0(idx); Hd=H0d(idx); Hdd=H0dd(idx); else, H=H1(idx); Hd=H1d(idx); Hdd=H1dd(idx); end, end
function [B,Bx,By,Bz,Nv]=make_B_matrices_3d(N,Nx,Ny,Nz,Nxx,Nyy,Nzz,Nxy,Nxz,Nyz), B=zeros(6,192); Bx=B; By=B; Bz=B; Nv=zeros(3,192); for a=1:8, sp=(a-1)*8+(1:8); up=(a-1)*24+(1:8); vp=(a-1)*24+(9:16); wp=(a-1)*24+(17:24); Nv(1,up)=N(sp); Nv(2,vp)=N(sp); Nv(3,wp)=N(sp); B(1,up)=Nx(sp); B(2,vp)=Ny(sp); B(3,wp)=Nz(sp); B(4,vp)=Nz(sp); B(4,wp)=Ny(sp); B(5,up)=Nz(sp); B(5,wp)=Nx(sp); B(6,up)=Ny(sp); B(6,vp)=Nx(sp); Bx(1,up)=Nxx(sp); Bx(2,vp)=Nxy(sp); Bx(3,wp)=Nxz(sp); Bx(4,vp)=Nxz(sp); Bx(4,wp)=Nxy(sp); Bx(5,up)=Nxz(sp); Bx(5,wp)=Nxx(sp); Bx(6,up)=Nxy(sp); Bx(6,vp)=Nxx(sp); By(1,up)=Nxy(sp); By(2,vp)=Nyy(sp); By(3,wp)=Nyz(sp); By(4,vp)=Nyz(sp); By(4,wp)=Nyy(sp); By(5,up)=Nyz(sp); By(5,wp)=Nxy(sp); By(6,up)=Nyy(sp); By(6,vp)=Nxy(sp); Bz(1,up)=Nxz(sp); Bz(2,vp)=Nyz(sp); Bz(3,wp)=Nzz(sp); Bz(4,vp)=Nzz(sp); Bz(4,wp)=Nyz(sp); Bz(5,up)=Nzz(sp); Bz(5,wp)=Nxz(sp); Bz(6,up)=Nyz(sp); Bz(6,vp)=Nxz(sp); end, end
