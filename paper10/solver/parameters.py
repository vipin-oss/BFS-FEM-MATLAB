"""
Material and Geometry Parameter Module for Paper 10
Coupled DPL-Gradient Elastic Phononic Crystal Formulation
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MaterialParameters:
    """Constitutive parameters for a single isotropic gradient-thermoelastic layer."""
    name: str
    rho: float        # Mass density (kg/m^3)
    mu: float         # Shear modulus (Pa)
    lambda_param: float  # Lamé first parameter (Pa)
    c: float          # Micro-stiffness length-scale squared, c = g^2 (m^2)
    d: float          # Micro-inertia length-scale, d = sqrt(3)*h (m)
    
    # Thermal parameters
    k: float = 0.2           # Thermal conductivity (W/(m*K))
    cv: float = 1000.0       # Specific heat capacity at constant deformation (J/(kg*K))
    alpha_t: float = 0.0     # Linear thermal expansion coefficient (1/K)
    T0: float = 300.0        # Reference ambient temperature (K)
    tau_q: float = 0.0       # Heat flux relaxation phase lag (s)
    tau_theta: float = 0.0   # Temperature gradient retardation phase lag (s)
    
    @property
    def beta(self) -> float:
        """Thermoelastic dilatational coupling coefficient beta = (3*lambda + 2*mu)*alpha_t (Pa/K)."""
        return (3.0 * self.lambda_param + 2.0 * self.mu) * self.alpha_t
    
    @property
    def Vs(self) -> float:
        """Classical shear wave speed (m/s)."""
        return np.sqrt(self.mu / self.rho)
    
    @property
    def Vp(self) -> float:
        """Classical longitudinal wave speed (m/s)."""
        return np.sqrt((self.lambda_param + 2.0 * self.mu) / self.rho)
    
    @property
    def g(self) -> float:
        """Micro-stiffness length scale (m)."""
        return np.sqrt(self.c)
    
    @property
    def h(self) -> float:
        """Micro-inertia length scale (m), where h = d / sqrt(3)."""
        return self.d / np.sqrt(3.0)
    
    def ms(self, omega: float) -> float:
        """Non-dimensional shear micro-inertia parameter: ms = omega^2 * d^2 / (3 * Vs^2) = omega^2 * h^2 / Vs^2."""
        return (omega**2 * self.d**2) / (3.0 * self.Vs**2)
    
    def mp(self, omega: float) -> float:
        """Non-dimensional longitudinal micro-inertia parameter: mp = omega^2 * d^2 / (3 * Vp^2)."""
        return (omega**2 * self.d**2) / (3.0 * self.Vp**2)
    
    def k_eff(self, omega: float) -> complex:
        """Effective DPL complex thermal conductivity: k_eff = k * (1 - i*omega*tau_theta) / (1 - i*omega*tau_q)."""
        if self.tau_q == 0.0 and self.tau_theta == 0.0:
            return complex(self.k)
        num = 1.0 - 1j * omega * self.tau_theta
        den = 1.0 - 1j * omega * self.tau_q
        return self.k * (num / den)
    
    def kth_sq(self, omega: float) -> complex:
        """Complex thermal wave parameter: kth^2 = i * omega * rho * cv / k_eff."""
        keff = self.k_eff(omega)
        return 1j * omega * self.rho * self.cv / keff
    
    def eta_th(self, omega: float) -> complex:
        """Thermal-to-dilatational coupling coefficient: eta_th = i * omega * T0 * beta / k_eff."""
        keff = self.k_eff(omega)
        return 1j * omega * self.T0 * self.beta / keff


@dataclass(frozen=True)
class UnitCellGeometry:
    """1D Unit Cell geometry for bi-layer phononic crystal."""
    a1: float   # Thickness of Layer A (m)
    a2: float   # Thickness of Layer B (m)
    
    @property
    def a(self) -> float:
        """Total unit cell lattice constant (m)."""
        return self.a1 + self.a2


def get_benchmark_papargyri_beskou_material() -> MaterialParameters:
    """
    Standard material parameters for Papargyri-Beskou et al. (2009) benchmark.
    Pure conservative gradient elasticity: beta = 0, tau_q = tau_theta = 0.
    """
    Vs = 1000.0         # m/s
    rho = 2000.0        # kg/m^3
    mu = rho * Vs**2    # Pa
    lambda_param = 2.0 * mu  # Poisson ratio nu = 0.333
    g = 0.001           # 1 mm
    h = 0.0015          # 1.5 mm
    c = g**2            # m^2
    d = np.sqrt(3.0) * h  # m
    
    return MaterialParameters(
        name="Papargyri-Beskou Benchmark Solid",
        rho=rho,
        mu=mu,
        lambda_param=lambda_param,
        c=c,
        d=d,
        alpha_t=0.0  # Conservative mechanical limit
    )


def get_li_acta_mech_materials(a: float = 1.0) -> tuple[MaterialParameters, MaterialParameters, UnitCellGeometry]:
    """
    Bi-layer gradient elasticity benchmark from Li, Wei & Zhou (2016, Acta Mechanica).
    Layer A and Layer B parameters for shear wave band gap calculations.
    """
    a1 = 0.5 * a
    a2 = 0.5 * a
    geom = UnitCellGeometry(a1=a1, a2=a2)
    
    rho1 = 1.0
    Vs1 = 1.0
    mu1 = rho1 * Vs1**2
    lambda1 = 2.0 * mu1
    c1 = (0.5 * a)**2
    d1 = 0.5 * a
    
    rho2 = 0.1573 * rho1
    Vs2 = 0.5947 * Vs1
    mu2 = rho2 * Vs2**2
    lambda2 = 2.0 * mu2
    c2 = c1 / 0.77
    d2 = d1 / 2.0
    
    matA = MaterialParameters(
        name="Li2016 Layer A",
        rho=rho1,
        mu=mu1,
        lambda_param=lambda1,
        c=c1,
        d=d1,
        alpha_t=0.0
    )
    
    matB = MaterialParameters(
        name="Li2016 Layer B",
        rho=rho2,
        mu=mu2,
        lambda_param=lambda2,
        c=c2,
        d=d2,
        alpha_t=0.0
    )
    
    return matA, matB, geom
