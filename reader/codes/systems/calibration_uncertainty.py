"""Chapter 09: first-order uncertainty; synthetic independent binomial counts.

Run: python3 codes/systems/calibration_uncertainty.py
Standard library only, deterministic, no device calls. Delta method is not an
exact confidence interval, and is unreliable near a singular readout matrix.
"""
import json
from math import isclose, sqrt


def budget(q, a, b, sizes):
    if not (0 <= a < b <= 1 and a <= q <= b):
        raise ValueError("Require 0 <= a < b <= 1 and a <= q <= b")
    if len(sizes) != 3 or any(n <= 0 for n in sizes):
        raise ValueError("Three positive sample sizes required")
    p, gap = (q - a) / (b - a), b - a
    derivatives = (1 / gap, -(1 - p) / gap, -p / gap)
    coefficients = [d * d * x * (1 - x)
                    for d, x in zip(derivatives, (q, a, b))]
    terms = [c / n for c, n in zip(coefficients, sizes)]
    roots = [sqrt(c) for c in coefficients]
    if sum(roots) == 0:
        raise ValueError("Degenerate first-order allocation; use boundary-aware inference")
    allocation = [sum(sizes) * r / sum(roots) for r in roots]
    return {"p": p, "variance_terms": terms, "standard_error": sqrt(sum(terms)),
            "fixed_calibration_standard_error": sqrt(terms[0]),
            "optimal_continuous_sizes": allocation}


def main():
    result = budget(.48, .02, .94, (1000, 1000, 1000))
    assert isclose(result["p"], .5)
    assert result["standard_error"] > result["fixed_calibration_standard_error"]
    optimal = budget(.48, .02, .94, result["optimal_continuous_sizes"])
    assert optimal["standard_error"] < result["standard_error"]
    for bad in ((.48, .5, .5), (.48, .6, .7), (0, 0, 1), (1, 0, 1)):
        try:
            budget(*bad, (1000, 1000, 1000))
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid model accepted")
    result["optimized_standard_error"] = optimal["standard_error"]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
