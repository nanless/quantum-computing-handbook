#!/usr/bin/env python3
"""Deterministic examples for chapters 13 and 18. Uses the Python standard library."""
from collections import defaultdict
from fractions import Fraction
from itertools import accumulate, product
import json
import math


def entropy(probabilities):
    return -math.fsum(p * math.log2(p) for p in probabilities if p > 0)


def information_examples():
    h = entropy([0.9, 0.1])
    zero_word_information = -math.log2(0.9)
    assert zero_word_information < h - 0.1
    high = (1 + 1 / math.sqrt(2)) / 2
    low = 1 - high
    selected_weight = math.fsum(
        math.prod(eigenvalues)
        for eigenvalues in product((high, low), repeat=3)
        if eigenvalues.count(low) <= 1
    )
    reference_squared_fidelity = selected_weight**2
    word_squared_overlap = reference_squared_fidelity + high**3 * (1 - selected_weight)
    assert math.isclose(selected_weight, 0.9419417382415921, abs_tol=1e-12)
    assert math.isclose(word_squared_overlap, 0.9233583034, abs_tol=1e-10)

    p = tuple(map(Fraction, ("1/2", "1/4", "1/4", "0")))
    q = tuple(map(Fraction, ("2/5", "2/5", "1/10", "1/10")))
    c = tuple(map(Fraction, ("3/5", "2/5")))
    system_prefixes = tuple(accumulate(p)), tuple(accumulate(q))
    joint_prefixes = tuple(
        tuple(accumulate(sorted((a * b for a, b in product(source, c)), reverse=True)))
        for source in (p, q)
    )
    assert system_prefixes[0][1] == Fraction(3, 4) < system_prefixes[1][1] == Fraction(4, 5)
    assert all(a >= b for a, b in zip(*joint_prefixes))

    rho = (Fraction(3, 4), Fraction(1, 4))
    sigma = (Fraction(1, 2), Fraction(1, 2))
    exact_acceptance = next(test for test in product((0, 1), repeat=2)
                            if sum(p_i * t for p_i, t in zip(rho, test)) == 1)
    beta_at_zero_alpha = sum(q_i * t for q_i, t in zip(sigma, exact_acceptance))
    assert beta_at_zero_alpha == 1
    assert math.isclose(1 - entropy(rho), 0.18872187554086717, abs_tol=1e-12)
    assert rho[0]**32 < Fraction(1, 100)

    states = dict(zip(product((0, 1), repeat=2),
                      map(Fraction, ("1/2", "0", "0", "1/2"))))
    ideal = {record: Fraction(1, 4) for record in states}
    full_distance = sum(abs(states[record] - ideal[record]) for record in states) / 2
    k_actual = tuple(sum(states[k, c_label] for c_label in (0, 1)) for k in (0, 1))
    k_ideal = (Fraction(1, 2), Fraction(1, 2))
    distance_without_record = sum(abs(a - b) for a, b in zip(k_actual, k_ideal)) / 2
    assert (distance_without_record, full_distance) == (0, Fraction(1, 2))
    upper_5441, upper_5442 = [2e-10 + 0.5 * 2**((length - 5500) / 2) for length in (5441, 5442)]
    assert upper_5441 < 1e-9 < upper_5442

    return {
        "typical_window_zero_word_excluded": True,
        "three_to_two_acceptance": selected_weight,
        "three_to_two_average_squared_overlap": word_squared_overlap,
        "three_to_two_reference_squared_fidelity": reference_squared_fidelity,
        "catalyst_joint_prefixes": [[str(entry) for entry in row] for row in joint_prefixes],
        "stein_alpha_zero_beta": str(beta_at_zero_alpha),
        "stein_relative_entropy_bits": 1 - entropy(rho),
        "security_distance_without_record": str(distance_without_record),
        "security_distance_with_record": str(full_distance),
        "secrecy_bound_5441": upper_5441,
        "secrecy_bound_5442": upper_5442,
    }


def fixed_five_qubit_coherent_information(q):
    """Group distinct Pauli strings by syndrome, logical X, and logical Z."""
    paulis = {(0, 0): 1 - q, (1, 0): q / 3, (0, 1): q / 3, (1, 1): q / 3}
    syndrome_probabilities = defaultdict(float)
    bell_probabilities = defaultdict(float)
    for errors in product(paulis, repeat=5):
        x, z = zip(*errors)
        syndrome = tuple(bit ^ x[0] for bit in x[1:])
        probability = math.prod(paulis[error] for error in errors)
        syndrome_probabilities[syndrome] += probability
        bell_probabilities[syndrome, x[0], sum(z) % 2] += probability
    assert math.isclose(math.fsum(bell_probabilities.values()), 1, abs_tol=1e-12)
    return 1 + entropy(syndrome_probabilities.values()) - entropy(bell_probabilities.values())


def smallest_zero(function, lower, upper):
    assert function(lower) > 0 > function(upper)
    while upper - lower > 1e-13:
        midpoint = (lower + upper) / 2
        if function(midpoint) > 0:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2


def capacity_examples():
    eps = Fraction(1, 4)
    source = (0.5, 0.5)
    bob = tuple((1 - eps) * p for p in source) + (eps,)
    environment = tuple(eps * p for p in source) + (1 - eps,)
    coherent = entropy(bob) - entropy(environment)
    assisted = entropy(source) + coherent
    assert math.isclose(coherent, 0.5, abs_tol=1e-12)
    assert math.isclose(assisted, 1.5, abs_tol=1e-12)
    assert (1 - eps) * Fraction(1, 3) == eps

    low = fixed_five_qubit_coherent_information(0.19035)
    high = fixed_five_qubit_coherent_information(0.1908)
    assert low > 0 > high
    zero = smallest_zero(fixed_five_qubit_coherent_information, 0.19035, 0.1908)
    hashing_zero = smallest_zero(lambda q: 1 - entropy((1 - q, q / 3, q / 3, q / 3)), 0.18, 0.20)
    assert math.isclose(zero, 0.190356088046, abs_tol=1e-12)
    assert math.isclose(hashing_zero, 0.189289624915, abs_tol=1e-12)

    # For sqrt(.8)|00>+sqrt(.2)|11>, T_B moves cross terms into the 01,10 block.
    pt_spectrum = (0.8, 0.2, math.sqrt(0.8 * 0.2), -math.sqrt(0.8 * 0.2))
    log_negativity = math.log2(sum(map(abs, pt_spectrum)))
    entanglement_entropy = entropy(pt_spectrum[:2])
    assert math.isclose(log_negativity, 0.8479969065549501, abs_tol=1e-12)
    assert entanglement_entropy < log_negativity

    return {
        "erasure_epsilon_quarter": {
            "C": str(1 - eps), "Q": coherent, "P": coherent, "CE": assisted,
            "one_use_guess_error": str(eps / 2), "one_use_flagged_failure": str(eps),
        },
        "maximally_mixed_one_use_hashing_zero": hashing_zero,
        "five_qubit_fixed_input_zero": zero,
        "five_qubit_at_0_19035": low,
        "five_qubit_at_0_1908": high,
        "pure_state_partial_transpose_spectrum": pt_spectrum,
        "pure_state_log_negativity": log_negativity,
        "pure_state_entanglement_entropy": entanglement_entropy,
    }


def continuous_variable_examples():
    # hbar=1, r=ln(2)/2; probabilities indexed by k=n/2.
    squeezed_probabilities = [
        math.comb(2 * k, k) * (1 / 36)**k * 2 * math.sqrt(2) / 3
        for k in range(40)
    ]
    cutoff = 20
    tail = math.fsum(squeezed_probabilities[cutoff // 2:])
    number_tail = math.fsum(2 * k * p for k, p in enumerate(squeezed_probabilities) if 2 * k >= cutoff)
    distance = math.sqrt(tail)
    assert math.isclose(math.fsum(squeezed_probabilities), 1, abs_tol=1e-12)
    assert math.isclose(tail, 5.32982630768e-11, rel_tol=1e-11)
    assert math.isclose(number_tail, 1.07862529494e-9, rel_tol=1e-11)
    assert math.isclose(distance, 7.30056594223e-6, rel_tol=1e-11)

    def minimum_uncertainty_eigenvalue(a, b):
        return (a + b - math.sqrt((a - b)**2 + 1)) / 2

    correctly_ordered = min(minimum_uncertainty_eigenvalue(a, b) for a, b in ((0.25, 1), (0.125, 2)))
    covariance_only = min(minimum_uncertainty_eigenvalue(a, b) for a, b in ((0.25, 0.125), (1, 2)))
    assert correctly_ordered == 0 and covariance_only < -0.31
    heavy_tail_probability = Fraction(1, 8 * cutoff)
    assert cutoff * heavy_tail_probability == Fraction(1, 8)

    return {
        "squeezed_vacuum_cutoff": cutoff,
        "squeezed_tail_probability": tail,
        "squeezed_normalized_trace_distance": distance,
        "squeezed_photon_number_tail": number_tail,
        "minimum_uncertainty_eigenvalue_correct": correctly_ordered,
        "minimum_uncertainty_eigenvalue_covariance_only": covariance_only,
        "same_energy_heavy_tail_probability": str(heavy_tail_probability),
    }


if __name__ == "__main__":
    print(json.dumps({
        "chapter_13": information_examples(),
        "chapter_18": {**capacity_examples(), **continuous_variable_examples()},
    }, ensure_ascii=False, indent=2))
