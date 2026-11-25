#!/usr/bin/env python3
"""Compare one normalized 1D Poisson observable by two independent routes.

Run from the repository root: python3 codes/algorithms/poisson_scalar_baseline.py
Only the standard library is required. The spectral filter and Bernoulli draws
are ideal simulations, with no gate synthesis, hardware access, or noise.
"""

import json
import math
import random


def tridiagonal_solve(rhs):
    """Solve tridiag(-1, 2, -1) x = rhs with Dirichlet end conditions."""
    diagonal = [2.0] * len(rhs)
    source = rhs.copy()
    for i in range(1, len(rhs)):
        factor = 1 / diagonal[i - 1]
        diagonal[i] -= factor
        source[i] += factor * source[i - 1]
    solution = [0.0] * len(rhs)
    solution[-1] = source[-1] / diagonal[-1]
    for i in range(len(rhs) - 2, -1, -1):
        solution[i] = (source[i] + solution[i + 1]) / diagonal[i]
    return solution


def ideal_filtered_branch(n, site):
    """For normalized constant input, return flag and flag-plus-site probabilities."""
    scale = math.sqrt(2 / (n + 1))
    lambda_min = 4 * math.sin(math.pi / (2 * (n + 1))) ** 2
    modes = []
    for k in range(1, n + 1):
        angle = math.pi * k / (n + 1)
        eigenvalue = 4 * math.sin(angle / 2) ** 2
        overlap = scale * sum(math.sin(angle * j) for j in range(1, n + 1)) / math.sqrt(n)
        modes.append(lambda_min * overlap / eigenvalue)
    flag_probability = math.fsum(abs(weight) ** 2 for weight in modes)
    site_amplitude = math.fsum(
        weight * scale * math.sin(math.pi * k * site / (n + 1))
        for k, weight in enumerate(modes, 1)
    )
    return flag_probability, abs(site_amplitude) ** 2


def main():
    n, site = 15, 8
    epsilon, failure_budget, seed = 0.01, 0.05, 20261126
    solution = tridiagonal_solve([1.0] * n)
    exact = [j * (n + 1 - j) / 2 for j in range(1, n + 1)]
    assert max(abs(a - b) for a, b in zip(solution, exact)) < 1e-12
    classical_scalar = abs(solution[site - 1]) ** 2 / math.fsum(x**2 for x in solution)

    flag, joint = ideal_filtered_branch(n, site)
    spectral_scalar = joint / flag
    assert abs(spectral_scalar - classical_scalar) < 1e-12
    accepted_target = math.ceil(math.log(2 / failure_budget) / (2 * epsilon**2))
    rng = random.Random(seed)
    hits = accepted = attempts = 0
    while accepted < accepted_target:
        attempts += 1
        draw = rng.random()
        accepted += draw < flag
        hits += draw < joint
    estimate = hits / accepted
    assert abs(estimate - classical_scalar) < epsilon

    print(json.dumps({
        "interior_sites": n, "observed_site_one_based": site, "seed": seed,
        "additive_error_goal": epsilon, "confidence": 1 - failure_budget,
        "classical_scalar": classical_scalar, "classical_coordinate_at_site": solution[site - 1],
        "classical_elimination_steps": n - 1, "classical_back_substitution_steps": n - 1,
        "dense_input_entries_if_materialized": n**2,
        "ideal_spectral_scalar": spectral_scalar, "ideal_flag_probability": flag,
        "accepted_samples": accepted, "synthetic_attempts": attempts, "site_hits": hits,
        "synthetic_estimate": estimate,
    }, indent=2))


if __name__ == "__main__":
    main()
