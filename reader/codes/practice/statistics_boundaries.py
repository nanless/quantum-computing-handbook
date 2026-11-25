#!/usr/bin/env python3
"""Deterministic chapter 15 statistical and circuit acceptance counterexamples."""
from fractions import Fraction
from itertools import product
from math import comb, floor, fsum, log, prod, sqrt
from random import Random
from statistics import mean, stdev
import json

from v4_practice_lab import student_t_ppf


def close(actual, expected, tolerance=1e-9):
    assert abs(actual - expected) <= tolerance, (actual, expected)


def witness_bounds(estimate, sizes, alpha=0.05):
    """Return the grouped two-sided and the independent-shot one-sided bounds."""
    simultaneous_radius = sum(sqrt(2 * log(6 / alpha) / n) / 4 for n in sizes)
    independent_radius = sqrt(log(1 / alpha) * sum(1 / n for n in sizes) / 8)
    return estimate - simultaneous_radius, estimate - independent_radius


def convolve(left, right):
    coefficients = [0.0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            coefficients[i + j] += x * y
    return coefficients


def binomial(n, p):
    return [comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)]


def witness_examples():
    outcomes = list(product((-1, 1), repeat=2))
    all_signs = [a * b for a, b in outcomes]
    accepted_by_basis = [[a * b for a, b in outcomes if a * b == target]
                         for target in (+1, -1, +1)]
    assert [len(batch) for batch in accepted_by_basis] == [2, 2, 2]
    xx, yy, zz = map(mean, accepted_by_basis)
    actual = (1 + mean(all_signs) - mean(all_signs) + mean(all_signs)) / 4
    filtered = (1 + xx - yy + zz) / 4
    assert actual == 0.25 and filtered == 1

    bounds = [witness_bounds(f, sizes) for f, sizes in (
        (0.65, (100,) * 3), (0.65, (400,) * 3),
        (0.6625, (1000,) * 3), (0.6625, (1000, 100, 1000)),
    )]
    for actual_pair, target in zip(bounds, ((.417924, .544009), (.533962, .597005),
                                             (.589111, .628983), (.536215, .595466))):
        for value, expected in zip(actual_pair, target):
            close(value, expected, 1e-6)

    sizes = (100,) * 3
    # With signed Bernoulli outcomes, f_hat = K/(2n) - 1/2.
    critical_totals = [floor(200 + 200 * (0.65 - bound)) + 1
                       for bound in witness_bounds(0.65, sizes)]
    assert critical_totals == [247, 222]
    probabilities = []
    for success in ((2 / 3,) * 3, (0.775, 0.75, 0.8)):
        columns = [binomial(n, p) for n, p in zip(sizes, success)]
        total = convolve(convolve(columns[0], columns[1]), columns[2])
        close(fsum(total), 1)
        probabilities.append([fsum(total[k:]) for k in critical_totals])
    close(probabilities[0][1], .00367401, 1e-8)
    close(probabilities[1][0], .0240004, 1e-7)
    close(probabilities[1][1], .934175, 1e-6)
    return {
        "mixed_product_true_overlap": actual, "biased_acceptance_rate_by_basis": [0.5] * 3,
        "postselected_false_overlap": filtered, "interval_lower_bounds": bounds,
        "critical_totals": critical_totals,
        "null_rejection_and_alternative_power": probabilities,
    }


def interval_examples():
    p = Fraction(1, 20)
    critical = student_t_ppf(.975, 3)
    covered = []
    for count in range(5):
        sample = [1] * count + [0] * (4 - count)
        lower = mean(sample) - critical * stdev(sample) / 2
        upper = mean(sample) + critical * stdev(sample) / 2
        if lower <= p <= upper:
            covered.append(count)
    assert covered == [1, 2, 3]
    coverage = sum(comb(4, k) * p**k * (1 - p)**(4-k) for k in covered)
    assert coverage == Fraction(29678, 160000)

    rare_fidelity = .999
    no_nondominant_sign = (1 - 2 * (1 - rare_fidelity) / 3) ** 300
    close(no_nondominant_sign, .8186761486)
    all_successes = [100] * 3
    # On this event, the empirical distribution in every group is a point mass.
    resampled = [k / 100 for k in all_successes]
    leave_one_out = [(k - 1) / 99 for k in all_successes]
    assert resampled == leave_one_out == [1, 1, 1]
    center = mean(leave_one_out)
    bca_defined = any(draw < center for draw in resampled) and stdev(leave_one_out) > 0
    assert not bca_defined

    crossing = 1 - (1 - .05)**100
    close(crossing, .994079470779666)
    assert .05 * 20 == 1 and 0 < .05 * 20
    return {
        "four_cluster_t_coverage": float(coverage),
        "all_ideal_signs_probability_for_f_0_999": no_nondominant_sign,
        "bca_defined_on_all_ideal_signs": bca_defined,
        "independent_fixed_e_value_crossing_probability_100_looks": crossing,
    }


def circuit_examples():
    # All indices label |q0 q1> with q0 the most significant bit.
    swap = (0, 2, 1, 3)
    decoded = [swap[swap[index] ^ 1] for index in range(4)]
    reference = [index ^ 2 for index in range(4)]
    assert decoded == reference and swap[1 ^ 1] != reference[1]
    n = 30
    phase = [-1 if index == 7 else 1 for index in range(8)]
    assert all(abs(amplitude) == 1 for amplitude in phase)
    assert (phase[0] + phase[-1]) / 2 == 0
    seed = 20261126
    rng = Random(seed)
    max_sampled_infidelity = max(
        2 * prod(rng.random() for _ in range(n)) for _ in range(16)
    )
    detection_upper_bound = 16 * 2 * 2**(-n) / 1e-6
    close(detection_upper_bound, .029802322387695312)
    assert max_sampled_infidelity < 1e-6

    candidate_readouts = (((.98, .01), (.02, .99)), ((.98, .40), (.02, .60)))
    assert [row[0] for row in candidate_readouts[0]] == [row[0] for row in candidate_readouts[1]]
    assert [row[1] for row in candidate_readouts[0]] != [row[1] for row in candidate_readouts[1]]
    z = (1, -1)
    assert all(eigenvalue**2 == 1 for eigenvalue in z)
    assert (z[0] - z[1]) / 2 == 1  # Z maps |+> to |->
    return {
        "decoded_compiled_basis_outputs": decoded, "output_only_on_input_01": swap[1 ^ 1],
        "logical_output_on_input_01": reference[1], "coherent_phase_error_overlap": 0,
        "product_probe_seed": seed, "max_sampled_product_probe_root_overlap_error": max_sampled_infidelity,
        "markov_union_bound_for_16_product_probes": detection_upper_bound,
    }


if __name__ == "__main__":
    print(json.dumps({
        "witness": witness_examples(),
        "intervals": interval_examples(),
        "circuit": circuit_examples(),
    }, indent=2))
