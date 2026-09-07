"""Material/constants + nondimensionalisation module (architecture items 1-2).

Derives every starred quantity from the dimensional set in params.json via
the frozen scales (blueprint §5; frozen formulation §12-13) and asserts the
frozen target values. Nothing is independently invented; c_e* = 1 exactly
(F1: the dimensional c_e is absorbed into the thermal-row normalisation).
"""
import json, math, os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_params(path=None):
    if path is None:
        path = os.path.join(_ROOT, "params.json")
    with open(path) as f:
        return json.load(f)

def derive_starred(par_dict):
    d = par_dict["dimensional_SI"]
    k0 = par_dict["scales"]["k0"]
    # frozen symmetry-derived constants (dimensional)
    C66 = (d["C11"] - d["C12"]) / 2.0
    K6 = d["K1"] - d["K2"] - d["K3"]
    R6 = (d["R1"] - d["R2"]) / 2.0
    # frozen scales
    v0 = math.sqrt(d["C11"] / d["rho"])
    om0 = v0 * k0
    U0 = d["beta1"] * d["T0"] / (d["C11"] * k0)
    s = dict(
        C11=1.0, C12=d["C12"] / d["C11"], C66=C66 / d["C11"],
        K1=d["K1"] / d["C11"], K2=d["K2"] / d["C11"], K3=d["K3"] / d["C11"],
        K6=K6 / d["C11"],
        R1=d["R1"] / d["C11"], R2=d["R2"] / d["C11"], R6=R6 / d["C11"],
        beta1=1.0,                      # by displacement scaling U0
        rho=1.0, rho_w=d["rho_w"] / d["rho"],
        c_e=1.0,                        # F1: exactly 1 in the nondimensional thermal row
        k11=d["k11"] * k0 / (d["rho"] * d["c_e"] * v0),
        tau0=d["tau0"] * om0,
        T0b1=d["beta1"] ** 2 * d["T0"] / (d["C11"] * d["rho"] * d["c_e"]),
        Dw=d["D_w"] * v0 / (d["C11"] * k0),
    )
    meta = dict(k0=k0, v0=v0, om0=om0, U0=U0,
                Omega_c=s["Dw"] / s["rho_w"],
                tau_tel=2.0 * s["rho_w"] / s["Dw"],
                vS=math.sqrt(s["C66"] / s["rho"]), vP=math.sqrt(s["C11"] / s["rho"]))
    return s, meta

def check_frozen(par_dict, s, meta, rtol=1e-4):
    """Assert derived starred values against the frozen table (V5)."""
    tgt = par_dict["frozen_starred_targets"]
    mapping = {
        "C11s": s["C11"], "C12s": s["C12"], "C66s": s["C66"],
        "K1s": s["K1"], "K2s": s["K2"], "K3s": s["K3"], "K6s": s["K6"],
        "R1s": s["R1"], "R2s": s["R2"], "R6s": s["R6"],
        "rho_s": s["rho"], "rho_ws": s["rho_w"], "beta1s": s["beta1"], "ce_s": s["c_e"],
        "k11s": s["k11"], "tau0s": s["tau0"], "T0b1s": s["T0b1"], "Dws": s["Dw"],
        "v0": meta["v0"], "om0": meta["om0"], "U0": meta["U0"],
        "vS_over_v0": meta["vS"] / meta["vP"], "vP_over_v0": 1.0,
        "Omega_c": meta["Omega_c"], "tau_tel_s": meta["tau_tel"],
    }
    bad = []
    for key, got in mapping.items():
        want = tgt[key]
        if abs(got - want) > rtol * max(abs(want), 1e-300):
            bad.append((key, got, want))
    return bad

class Material:
    """Immutable nondimensional parameter set (with documented overrides)."""
    def __init__(self, par_dict=None, overrides=None):
        par_dict = par_dict or load_params()
        s, meta = derive_starred(par_dict)
        self._base = dict(s); self.meta = dict(meta)
        self.defaults = par_dict["solver_defaults"]
        for k, v in (overrides or {}).items():
            if k not in s:
                raise KeyError(f"unknown parameter override: {k}")
            s[k] = v
        self.__dict__.update(s)
        self.overrides = dict(overrides or {})
        # symmetry relations must hold by construction (machine check)
        assert abs(2 * self.C66 - (self.C11 - self.C12)) < 1e-14
        assert abs(self.K6 - (self.K1 - self.K2 - self.K3)) < 1e-14
        assert abs(2 * self.R6 - (self.R1 - self.R2)) < 1e-14

    def detA2(self, k):
        return (self.C11 * self.K1 - self.R1 ** 2) * (self.C66 * self.K3 - self.R6 ** 2) * self.k11
