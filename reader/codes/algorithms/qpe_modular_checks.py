#!/usr/bin/env python3
"""Recompute QPE wiring and fixed-width modular addition for Chapters 06–07.

Run from the repository root: python3 codes/algorithms/qpe_modular_checks.py.
Uses fixed small inputs, big-endian bit labels and only the standard library.
The width calculation models register arithmetic on basis states.
"""

import cmath
import json
import math


def reverse_bits(index, bits):
    return int(f"{index:0{bits}b}"[::-1], 2)


def phase_distribution(bits, phase, reverse_input=False, omit_inverse_swaps=False):
    size = 1 << bits
    state = [cmath.exp(2j * math.pi * k * phase) / math.sqrt(size) for k in range(size)]

    def reverse(values):
        return [values[reverse_bits(k, bits)] for k in range(size)]

    if reverse_input:
        state = reverse(state)
    # F = P C, where C omits the final SWAPs of the forward transform.
    # Omitting the initial SWAPs of the inverse implements C† = F† P.
    if omit_inverse_swaps:
        state = reverse(state)
    amplitudes = [
        sum(value * cmath.exp(-2j * math.pi * k * bit_value / size)
            for k, value in enumerate(state)) / math.sqrt(size)
        for bit_value in range(size)
    ]
    probabilities = [abs(value) ** 2 for value in amplitudes]
    assert abs(sum(probabilities) - 1) < 1e-12
    return probabilities


def modular_add_trace(data, increment, modulus, width):
    mask = (1 << width) - 1
    sign = 1 << (width - 1)
    total = (data + increment) & mask
    after_subtract = (total - modulus) & mask
    comparison = bool(after_subtract & sign)
    reduced = (after_subtract + (modulus if comparison else 0)) & mask
    uncompute = (reduced - increment) & mask
    comparison ^= not bool(uncompute & sign)
    restored = (uncompute + increment) & mask
    return restored, int(comparison)


def modular_add_in_domain(data, increment, modulus, enabled):
    # This conditional represents a separately computed range flag. It is
    # recomputed after the add, since the output stays in the same range class.
    if not enabled or data >= modulus:
        return data, 0
    return modular_add_trace(data, increment, modulus, (modulus - 1).bit_length() + 1)


def main():
    expected = [0, 0.25, 0.5, 0.25]
    assert all(abs(p - q) < 1e-12 for p, q in zip(
        phase_distribution(2, 0.25, omit_inverse_swaps=True), expected
    ))
    assert all(abs(p - q) < 1e-12 for p, q in zip(
        phase_distribution(2, 0.25, reverse_input=True), expected
    ))
    for bits in (2, 3):
        size = 1 << bits
        for label in range(size):
            for reverse in (False, True):
                outcome = phase_distribution(bits, label / size, reverse, reverse)
                assert abs(outcome[label] - 1) < 1e-12
        off_grid = phase_distribution(bits, 0.37)
        rewired = phase_distribution(bits, 0.37, True, True)
        assert all(abs(p - q) < 1e-12 for p, q in zip(off_grid, rewired))

    assert modular_add_trace(20, 20, 21, 5) == (8, 1)
    assert modular_add_trace(20, 20, 21, 6) == (19, 0)
    for modulus in (3, 5, 8, 21):
        limit = 1 << (modulus - 1).bit_length()
        for increment in range(modulus):
            for enabled in (False, True):
                outcomes = [modular_add_in_domain(data, increment, modulus, enabled)
                            for data in range(limit)]
                assert outcomes == [
                    ((data + increment) % modulus if enabled and data < modulus else data, 0)
                    for data in range(limit)
                ]
                assert len(set(outcomes)) == limit
    print(json.dumps({
        'wrong_inverse_wiring': expected,
        'mod21_five_bits': modular_add_trace(20, 20, 21, 5),
        'mod21_six_bits': modular_add_trace(20, 20, 21, 6),
        'status': 'passed',
    }, indent=2))


if __name__ == '__main__':
    main()
