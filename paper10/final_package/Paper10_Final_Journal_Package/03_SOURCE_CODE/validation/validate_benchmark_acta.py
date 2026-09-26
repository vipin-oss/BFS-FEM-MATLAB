import numpy as np
import matplotlib.pyplot as plt

def get_T_j(w, a_j, mu_j, rho_j, c_j, d_j, xi=0.0):
    Vs_j = np.sqrt(mu_j / rho_j)
    ms_j = (w**2 * d_j**2) / (3.0 * Vs_j**2)
    Delta_s = np.sqrt((1.0 - ms_j)**2 + 4.0 * c_j * w**2 / Vs_j**2)
    
    sigma_sq = 0.5 / c_j * (Delta_s - (1.0 - ms_j))
    tau_sq = 0.5 / c_j * (Delta_s + (1.0 - ms_j))
    
    beta_sq = sigma_sq - xi**2
    gamma_sq = tau_sq + xi**2
    
    beta_s = np.sqrt(complex(beta_sq))
    gamma_s = np.sqrt(complex(gamma_sq))
    
    # Components e_kn
    e11 = np.cos(beta_s * a_j)
    e12 = np.cosh(gamma_s * a_j)
    e13 = np.sin(beta_s * a_j) / beta_s if abs(beta_s) > 1e-12 else a_j
    e14 = np.sinh(gamma_s * a_j) / gamma_s if abs(gamma_s) > 1e-12 else a_j
    
    e21 = -beta_s * np.sin(beta_s * a_j)
    e22 = gamma_s * np.sinh(gamma_s * a_j)
    e23 = np.cos(beta_s * a_j)
    e24 = np.cosh(gamma_s * a_j)
    
    term_sig = sigma_sq + xi**2
    term_tau = tau_sq - xi**2
    e31 = mu_j * (-beta_s * (1.0 - ms_j) - c_j * beta_s * term_sig) * np.sin(beta_s * a_j)
    e32 = mu_j * (gamma_s * (1.0 - ms_j) - c_j * gamma_s * term_tau) * np.sinh(gamma_s * a_j)
    e33 = mu_j * ((1.0 - ms_j) + c_j * term_sig) * np.cos(beta_s * a_j)
    e34 = mu_j * ((1.0 - ms_j) - c_j * term_tau) * np.cosh(gamma_s * a_j)
    
    e41 = -mu_j * c_j * beta_s**2 * np.cos(beta_s * a_j)
    e42 = mu_j * c_j * gamma_s**2 * np.cosh(gamma_s * a_j)
    e43 = -mu_j * c_j * beta_s * np.sin(beta_s * a_j)
    e44 = mu_j * c_j * gamma_s * np.sinh(gamma_s * a_j)
    
    E = np.array([
        [e11, e12, e13, e14],
        [e21, e22, e23, e24],
        [e31, e32, e33, e34],
        [e41, e42, e43, e44]
    ], dtype=complex)
    
    T = np.zeros((4, 4), dtype=complex)
    denom = sigma_sq + tau_sq
    
    for k in range(4):
        T[k, 0] = (E[k, 0] * (denom - beta_s**2) + beta_s**2 * E[k, 1]) / denom
        term1 = (term_tau - (1.0 - ms_j) / c_j) * E[k, 2]
        term2 = ((1.0 - ms_j) / c_j + term_sig) * E[k, 3]
        T[k, 1] = (term1 + term2) / denom
        T[k, 2] = (E[k, 2] - E[k, 3]) / (mu_j * c_j * denom)
        T[k, 3] = (E[k, 1] - E[k, 0]) / (mu_j * c_j * denom)
        
    return T

# Geometry and Material parameters according to Section 6 of Li et al. (2016)
a = 1.0
a1 = 0.5 * a
a2 = 0.5 * a
Vs1 = 1.0
rho1 = 1.0
mu1 = rho1 * Vs1**2

Vs2 = 0.5947 * Vs1
rho2 = 0.1573 * rho1
mu2 = rho2 * Vs2**2

vm = a / (a1 / Vs1 + a2 / Vs2)

# High-resolution frequency grid
Omega_grid = np.linspace(0.002, 2.0, 1000)

# 1. Classical Case (Fig. 2)
print("Computing Classical Solution (Fig. 2)...")
classical_bands = []
classical_gaps = []

for Om in Omega_grid:
    w = Om * 2.0 * np.pi * vm / a
    k1 = w / Vs1
    k2 = w / Vs2
    Z1 = mu1 * k1
    Z2 = mu2 * k2
    cos_ka = np.cos(k1 * a1) * np.cos(k2 * a2) - 0.5 * (Z1/Z2 + Z2/Z1) * np.sin(k1 * a1) * np.sin(k2 * a2)
    if abs(cos_ka) <= 1.0:
        ka = np.arccos(cos_ka)
        classical_bands.append((ka / np.pi, Om))
    else:
        classical_gaps.append(Om)

# Find contiguous gap ranges
def get_gap_intervals(gap_list, threshold=0.005):
    if not gap_list:
        return []
    intervals = []
    start = gap_list[0]
    prev = gap_list[0]
    for val in gap_list[1:]:
        if val - prev > threshold:
            intervals.append((start, prev))
            start = val
        prev = val
    intervals.append((start, prev))
    return intervals

class_gap_intervals = get_gap_intervals(classical_gaps)
print("Classical Band Gaps [Omega_lower, Omega_upper]:")
for idx, (low, high) in enumerate(class_gap_intervals):
    print(f"  Gap {idx+1}: [{low:.4f}, {high:.4f}] -> Width = {high-low:.4f}")

# 2. Gradient Elasticity Case (Fig. 3)
print("\nComputing Gradient Elasticity Solution (Fig. 3)...")
c1 = (0.5 * a)**2
c2 = c1 / 0.77
d1 = 0.5 * a
d2 = d1 / 2.0

gradient_bands = []
gradient_gaps = []

for Om in Omega_grid:
    w = Om * 2.0 * np.pi * vm / a
    TA = get_T_j(w, a1, mu1, rho1, c1, d1, xi=0.0)
    TB = get_T_j(w, a2, mu2, rho2, c2, d2, xi=0.0)
    Tcell = TB @ TA
    eigvals = np.linalg.eigvals(Tcell)
    
    propagating = False
    for ev in eigvals:
        if abs(abs(ev) - 1.0) < 1e-2:
            phase = np.angle(ev)
            if 0 <= phase <= np.pi:
                gradient_bands.append((phase / np.pi, Om))
                propagating = True
                
    if not propagating:
        gradient_gaps.append(Om)

grad_gap_intervals = get_gap_intervals(gradient_gaps)
print("Gradient Elasticity Band Gaps [Omega_lower, Omega_upper]:")
for idx, (low, high) in enumerate(grad_gap_intervals):
    print(f"  Gap {idx+1}: [{low:.4f}, {high:.4f}] -> Width = {high-low:.4f}")

# Create Publication-Quality Plot matching Fig. 2 and Fig. 3 of Li et al. (2016)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Classical
for low, high in class_gap_intervals:
    ax1.axhspan(low, high, color='gray', alpha=0.55, edgecolor='none')
cb_x = [pt[0] for pt in classical_bands]
cb_y = [pt[1] for pt in classical_bands]
ax1.plot(cb_x, cb_y, 'k-', linewidth=1.2)
ax1.plot([-x for x in cb_x], cb_y, 'k-', linewidth=1.2)
ax1.set_xlim([-1, 1])
ax1.set_ylim([0, 2])
ax1.set_xlabel(r'$ka / \pi$', fontsize=13)
ax1.set_ylabel(r'$\omega a / (2\pi v_m)$', fontsize=13)
ax1.set_title(r'Classical Phononic Crystal (Reproduced Fig. 2, $\bar{\xi}=0$)', fontsize=13, fontweight='bold')
ax1.grid(True, linestyle=':', alpha=0.6)

# Plot 2: Gradient Elasticity
for low, high in grad_gap_intervals:
    ax2.axhspan(low, high, color='gray', alpha=0.55, edgecolor='none')
gb_x = [pt[0] for pt in gradient_bands]
gb_y = [pt[1] for pt in gradient_bands]
ax2.plot(gb_x, gb_y, 'b.', markersize=2.5)
ax2.plot([-x for x in gb_x], gb_y, 'b.', markersize=2.5)
ax2.set_xlim([-1, 1])
ax2.set_ylim([0, 2])
ax2.set_xlabel(r'$ka / \pi$', fontsize=13)
ax2.set_ylabel(r'$\omega a / (2\pi v_m)$', fontsize=13)
ax2.set_title(r'Gradient Elasticity Phononic Crystal (Reproduced Fig. 3, $\bar{\xi}=0$)', fontsize=13, fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
out_file = '/home/user/vg_workspace/feasibility/benchmark_validation_acta_mech.png'
plt.savefig(out_file, dpi=300)
print(f"\nFinal publication benchmark validation saved to: {out_file}")
