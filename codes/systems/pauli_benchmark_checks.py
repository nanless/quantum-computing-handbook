"""Independent Pauli-orbit and PEC arithmetic for Chapter 11.

Run: python3 codes/systems/pauli_benchmark_checks.py. No dependencies or RNG.
"""
from fractions import Fraction as F
from itertools import product
import json
import math


def convolve(first, second):
    return [sum(first[x] * second[x ^ y] for x in range(4)) for y in range(4)]


def apply_factors(p, invert):
    coefficients = [F(1), F(0), F(0), F(0)]
    for generator in (1, 2, 3):  # ZI, IZ and ZZ, modulo global phase.
        factor = [F(0)] * 4
        if invert:
            factor[0] = (1 - p) / (1 - 2*p)
            factor[generator] = -p / (1 - 2*p)
        else:
            factor[0], factor[generator] = 1 - p, p
        coefficients = convolve(coefficients, factor)
    return coefficients


def cnot_pauli(support):
    # Sign is unnecessary for the conjugation on this X-only orbit.
    x_control, x_target = support
    return x_control, x_target ^ x_control


def main():
    first = (1, 0)
    second = cnot_pauli(first)
    assert second == (1, 1) and cnot_pauli(second) == first
    p = F(1, 10)
    # Conjugating the tracked Pauli by IZ flips its sign iff target X is present.
    eigenvalues = [1 - 2*p*label[1] for label in (first, second)]
    orbit = math.prod(eigenvalues)
    assert orbit == F(4, 5)

    channel = apply_factors(p, invert=False)
    inverse = apply_factors(p, invert=True)
    assert convolve(channel, inverse) == [1, 0, 0, 0]
    fp = channel[0]
    gamma = sum(abs(weight) for weight in inverse)
    assert fp == F(73, 100) and gamma == F(59, 32) < 1 / fp**2

    # Independent direct enumeration of the eight raw sampling choices.
    outcomes = [F(0)] * 4
    for errors in product((0, 1), repeat=3):
        mask = (errors[0] * 1) ^ (errors[1] * 2) ^ (errors[2] * 3)
        weight = sum(errors)
        outcomes[mask] += p**weight * (1-p)**(3-weight)
    assert outcomes == channel

    mean = F(1, 5)
    weights = [(1 + mean/gamma) / 2, (1 - mean/gamma) / 2]
    assert sum(weight*value for weight, value in zip(weights, [gamma, -gamma])) == mean
    variance = sum(weight*(value-mean)**2
                   for weight, value in zip(weights, [gamma, -gamma]))
    assert variance == gamma**2 - mean**2
    print(json.dumps({"cnot_orbit": ["XI", "XX"], "two_cycle_decay": float(orbit),
                      "process_fidelity": float(fp), "inverse_coefficients": [str(c) for c in inverse],
                      "coalesced_gamma": float(gamma), "fidelity_inverse_squared": float(1/fp**2),
                      "factorwise_gamma": float((1-2*p)**-3),
                      "variance_at_mean_point_2": float(variance)}, indent=2))


if __name__ == "__main__":
    main()
