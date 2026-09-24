"""P12R amendment A2 (Blueprint v1.5, Section 13): external-validation evidence route.

Classification ONLY.  This module never computes a numerical error, never derives a
percentage from a curve or a figure, and never upgrades graphical evidence to
quantitative.  Its three outcomes are the fixed identifiers of Blueprint v1.5 A2.6:

    QUANTITATIVE_VALIDATION   source numerical values exist; existing thresholds apply
    GRAPHICAL_VALIDATION      no source numerics; labelled overlay comparison only
    NOT_VALIDATED             insufficient source, unresolved ambiguity, or work not done

Thresholds are the EXISTING ones and are not set here: the general benchmark criterion
is <= 2 % relative and the classical-limit target is <= 0.5 % (Blueprint v1.3/v1.4/v1.5,
unchanged by A2).
"""

from __future__ import annotations

ROUTE_QUANTITATIVE = "QUANTITATIVE_VALIDATION"
ROUTE_GRAPHICAL = "GRAPHICAL_VALIDATION"
ROUTE_NOT_VALIDATED = "NOT_VALIDATED"

ALL_ROUTES = (ROUTE_QUANTITATIVE, ROUTE_GRAPHICAL, ROUTE_NOT_VALIDATED)

# Existing criteria, restated for tooling.  A2 introduces no new threshold.
THRESHOLD_GENERAL_PCT = 2.0
THRESHOLD_CLASSICAL_PCT = 0.5

# Evidence hierarchy (A2.3): a lower route must never be presented as stronger.
HIERARCHY_RANK = {ROUTE_QUANTITATIVE: 3, ROUTE_GRAPHICAL: 2, ROUTE_NOT_VALIDATED: 1}


class FabricatedPrecisionError(ValueError):
    """A numerical error was asserted without source numerical values (A2.5)."""


def threshold_pct(classical_limit: bool = False) -> float:
    """The existing threshold applicable to a benchmark (A2.1(a)); unchanged by A2."""
    return THRESHOLD_CLASSICAL_PCT if classical_limit else THRESHOLD_GENERAL_PCT


def hierarchy_rank(route: str) -> int:
    """Evidence strength of a route (A2.3).  Raises on an unknown route."""
    if route not in HIERARCHY_RANK:
        raise ValueError(f"unknown route: {route!r}")
    return HIERARCHY_RANK[route]


def classify(
    benchmark: str,
    *,
    source_numerical_data: bool,
    parameters_sufficient: bool,
    graphical_reproduction_performed: bool,
    ambiguity_unresolved: bool = False,
    reported_error_pct: float | None = None,
    classical_limit: bool = False,
    overlay_available: bool = False,
) -> dict:
    """Classify one benchmark's external evidence into exactly one of the three states.

    Parameters mirror the facts a run must be able to state without inference:

    ``source_numerical_data``            source tables / released data / authors' values exist
    ``parameters_sufficient``            the source reports the parameters, normalisation and
                                         boundary/interface information needed to reconstruct
                                         the case (an unresolved ambiguity counts as NOT
                                         sufficient, A2.4)
    ``graphical_reproduction_performed`` the reconstruction + direct curve comparison was
                                         actually carried out (A2.2)
    ``ambiguity_unresolved``             a source definitional ambiguity (e.g. l vs l_bar) is
                                         still open
    ``reported_error_pct``               a relative error, ONLY admissible with source numerics
    ``overlay_available``                an overlay or equivalent figure was produced (A2.2 G5)

    The returned dict never carries a numerical error for a graphical or not-validated result.
    """
    if reported_error_pct is not None and not source_numerical_data:
        raise FabricatedPrecisionError(
            f"{benchmark}: a relative error was supplied although no source numerical values "
            "exist; graphical agreement may not be converted into a percentage (A2.5)"
        )

    def result(route: str, verdict: str, reason: str, err: float | None = None,
               threshold: float | None = None) -> dict:
        return {
            "benchmark": benchmark,
            "route": route,
            "verdict": verdict,
            "quantitative_error": err,
            "threshold_pct": threshold,
            "classical_limit": bool(classical_limit),
            "reason": reason,
            "requires_label": route == ROUTE_GRAPHICAL,
            "overlay_available": bool(overlay_available) if route == ROUTE_GRAPHICAL else False,
            "hierarchy_rank": HIERARCHY_RANK[route],
        }

    # A2.4 — an unresolved source ambiguity blocks the benchmark under either route.
    if ambiguity_unresolved:
        return result(ROUTE_NOT_VALIDATED, "NOT VALIDATED",
                      "unresolved source ambiguity: the case cannot be defined unambiguously")

    if source_numerical_data:
        # A2.1(a) — numerical source data exist: the quantitative route is mandatory and
        # the graphical route is not available for this benchmark (A2.3).
        if reported_error_pct is None:
            return result(ROUTE_NOT_VALIDATED, "NOT VALIDATED",
                          "source numerical values exist but no comparison has been performed; "
                          "the graphical route may not be used in their place")
        thr = threshold_pct(classical_limit)
        ok = reported_error_pct <= thr
        return result(ROUTE_QUANTITATIVE, "PASS" if ok else "FAIL",
                      "quantitative comparison against source numerical values",
                      err=float(reported_error_pct), threshold=thr)

    # A2.1(b)+(c) — no source numerics: graphical route if the source is sufficient AND the
    # reproduction was performed; otherwise not validated.
    if not parameters_sufficient:
        return result(ROUTE_NOT_VALIDATED, "NOT VALIDATED",
                      "insufficient source: parameters/normalisation/interface information "
                      "do not allow a reliable reconstruction")
    if not graphical_reproduction_performed:
        return result(ROUTE_NOT_VALIDATED, "NOT VALIDATED",
                      "graphical route not executed: no reconstruction and direct comparison "
                      "has been performed")
    return result(ROUTE_GRAPHICAL, "GRAPHICAL VALIDATION",
                  "graphical reproduction and direct curve comparison; no numerical error "
                  "asserted (A2.5)")
