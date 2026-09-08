"""Published calibration dataset and B arithmetic.

Implements sec:calibrations of GK_COMPLETE_CALCULATIONS.tex:
  eq:Bdef        B from tabulated (alpha, tau_q, kappa2)
  eq:B-186/275/384  worked basalt values
  eq:both-B      Both et al. B
  eq:both-Berr   propagated uncertainty
  eq:band20      band membership test
  eq:van-b       b = l^2/(tau alpha) equals B (sec:van-lb)

PROVENANCE IS MANDATORY. Each field is tagged LIT (literature), DER (derived
here) or NUM (computed here). Datasets are never merged: the Both et al.
capacitor (case 12) and the Van et al. capacitor (case 1) are different fits of
the same specimen type and are kept separate (check:both-vs-van).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from .model import B_of


@dataclass
class Case:
    idx: int
    source: str
    citekey: str
    specimen: str
    alpha_1e6: float           # LIT, 1e-6 m^2/s
    tau_q_s: float             # LIT, s
    kappa2_1e6: Optional[float]  # LIT, 1e-6 m^2 (None if source tabulates l/b)
    B_reported: Optional[float]  # LIT
    d_alpha: Optional[float] = None   # LIT uncertainty
    d_tau_q: Optional[float] = None
    d_kappa2: Optional[float] = None
    R2: Optional[float] = None
    note: str = ""

    @property
    def B_calc(self) -> Optional[float]:
        """DER via eq:Bdef. The 1e-6 factors cancel between numerator and
        denominator, so tabulated numbers may be used directly."""
        if self.kappa2_1e6 is None:
            return None
        return B_of(self.alpha_1e6, self.tau_q_s, self.kappa2_1e6)

    @property
    def B_used(self) -> float:
        """B used for band classification: derived where possible, else the
        authors' reported value (cases 1-4, see sec:van-lb)."""
        b = self.B_calc
        return b if b is not None else self.B_reported

    @property
    def dB_rel(self) -> Optional[float]:
        """DER: propagated relative uncertainty, eq:both-Berr (quadrature)."""
        if None in (self.d_alpha, self.d_tau_q, self.d_kappa2):
            return None
        return float(np.sqrt((self.d_kappa2 / self.kappa2_1e6) ** 2
                             + (self.d_alpha / self.alpha_1e6) ** 2
                             + (self.d_tau_q / self.tau_q_s) ** 2))

    def in_band(self, lo, hi) -> bool:
        return bool(lo <= self.B_used <= hi)


# --- the twelve audited cases, transcribed from the primary sources ---------
CASES = [
    Case(1, "Van et al. 2017", "Van2017", "capacitor 3.9 mm",
         2.13, 0.954, None, 2.23, note="authors' b used; see sec:van-lb"),
    Case(2, "Van et al. 2017", "Van2017", "limestone 1.7 mm",
         2.950, 0.991, None, 2.17, note="authors' b used; see sec:van-lb"),
    Case(3, "Van et al. 2017", "Van2017", "metal foam 5.1 mm",
         2.373, 0.402, None, 3.04, note="authors' b used; see sec:van-lb"),
    Case(4, "Van et al. 2017", "Van2017", "leucocratic 1.75 mm",
         4.77, 1.32, None, 1.77, note="authors' b used; see sec:van-lb"),
    Case(5, "earlier eval., in FeherKovacs2021 Table 1", "FeherKovacs2021",
         "basalt 1.86 mm", 0.55, 0.738, 0.509, 1.243),
    Case(6, "earlier eval., in FeherKovacs2021 Table 1", "FeherKovacs2021",
         "basalt 2.75 mm", 0.604, 0.955, 0.670, 1.171),
    Case(7, "earlier eval., in FeherKovacs2021 Table 1", "FeherKovacs2021",
         "basalt 3.84 mm", 0.68, 0.664, 0.480, 1.060),
    Case(8, "Feher & Kovacs 2021", "FeherKovacs2021", "basalt 1.86 mm",
         0.61, 0.211, 0.168, 1.295, R2=0.9975),
    Case(9, "Feher & Kovacs 2021", "FeherKovacs2021", "basalt 2.75 mm",
         0.61, 0.344, 0.268, 1.272, R2=0.9964),
    Case(10, "Feher & Kovacs 2021", "FeherKovacs2021", "basalt 3.84 mm",
         0.68, 1.000, 0.650, 0.940, R2=0.9986),
    Case(11, "Feher & Kovacs 2021", "FeherKovacs2021", "metal foam 5.2 mm",
         3.01, 0.304, 2.203, 2.395),
    Case(12, "Both et al. 2016", "Both2016", "capacitor 3.9 mm",
         1.958, 0.51, 1.53, None,
         d_alpha=0.004, d_tau_q=0.01, d_kappa2=0.03, R2=0.9996,
         note="only case reporting parameter uncertainties"),
]

# Same-specimen discrepancy, tab:discrepancy (all LIT)
DISCREPANCY = [
    ("basalt 1.86 mm", 0.738, 0.211, 0.9975),
    ("basalt 2.75 mm", 0.955, 0.344, 0.9964),
    ("basalt 3.84 mm", 0.664, 1.000, 0.9986),
]

FITTING_DOMAIN = (1.0, 3.0)   # eq:fitting-domain, LIT FeherKovacs2021


def aggregate(lo, hi):
    """Band membership counts over the twelve cases."""
    inside = [c for c in CASES if c.in_band(lo, hi)]
    return {"n_total": len(CASES), "n_inside": len(inside),
            "n_outside": len(CASES) - len(inside),
            "inside_idx": [c.idx for c in inside]}


def max_B_deviation():
    """DER: max |B_calc - B_reported| where both exist."""
    d = [abs(c.B_calc - c.B_reported) for c in CASES
         if c.B_calc is not None and c.B_reported is not None]
    return float(max(d)) if d else None
