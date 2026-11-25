#!/usr/bin/env python3
"""Recompute the Chapter 02–03 measurement examples with the standard library.

Run from the repository root: python3 codes/foundations/measurement_validation.py
Fixed matrices and one exact binomial sum, no random seed or external devices.
Probabilities are dimensionless; tensor factors are in big-endian order.
"""

import json
from itertools import product
from math import comb, sqrt

from foundations_lab import I, X, Y, Z, add, close, dagger, eig2, inner, kron, matrix_close, mm, mv, outer, scale, trace


def instrument_and_readout():
    p0 = [[1, 0], [0, 0]]
    p1 = [[0, 0], [0, 1]]
    reset_after_one = [[0, 1], [0, 0]]
    matrix_close(mm(dagger(reset_after_one), reset_after_one), p1)
    matrix_close(add(p0, p1), I)
    rho1 = p1
    after_reset = mm(mm(reset_after_one, rho1), dagger(reset_after_one))
    close(trace(mm(p1, rho1)), 1)
    close(trace(mm(p1, after_reset)), 0)

    # The third level can trigger either label. Repreparing the corresponding
    # eigenstate gives an exactly repeatable instrument despite both effects
    # having a fractional eigenvalue on that third level.
    e0 = [[1, 0, 0], [0, 0, 0], [0, 0, 0.5]]
    e1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0.5]]
    matrix_close(add(e0, e1), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    for label, effect in enumerate((e0, e1)):
        state = [int(index == label) for index in range(3)]
        close(trace(mm(effect, outer(state))), 1)
        close((effect[2][2])**2, 0.25)

    diagonal = [[0.05, 0], [0, 0.90]]
    coherent = add(diagonal, scale(X, 0.10))
    for effect in (diagonal, coherent):
        assert min(eig2(effect)) >= 0
        assert min(eig2(add(I, scale(effect, -1)))) >= 0
        close(trace(mm(effect, p0)), 0.05)
        close(trace(mm(effect, p1)), 0.90)
    state = [sqrt(0.9), sqrt(0.1)]
    probabilities = [inner(state, mv(effect, state)).real for effect in (diagonal, coherent)]
    for actual, expected in zip(probabilities, (0.135, 0.195)):
        close(actual, expected)

    estimates = [0.36 / (1 - 2 * rate) for rate in (0.19, 0.21)]
    mean = sum(estimates) / len(estimates)
    covariance = -sum((r - mean)**2 for r in estimates) / len(estimates)
    close(covariance, -0.00040089037)
    exact = sum(comb(400, count) for count in range(190, 211)) / 2**400
    close(exact, 0.706291881838)
    return {
        'repeat_label_one': {'Luders': 1, 'measure_then_reset': 0},
        'three_level_reprepared_labels': [1, 1],
        'coherent_input_report_one': probabilities,
        'shared_calibration_covariance_xz': covariance,
        'exact_binomial_probability_190_through_210': exact,
    }


def joint_measurements():
    xx, yy, zz = kron(X, X), kron(Y, Y), kron(Z, Z)
    negative_yy = scale(yy, -1)
    matrix_close(mm(xx, zz), negative_yy)
    matrix_close(mm(zz, xx), negative_yy)
    vectors = [[v / sqrt(2) for v in row]
               for row in ([1, 0, 0, 1], [1, 0, 0, -1], [0, 1, 1, 0], [0, 1, -1, 0])]
    labels = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for state, (sx, sz) in zip(vectors, labels):
        for actual, expected in zip(mv(xx, state), (sx * v for v in state)):
            close(actual, expected)
        for actual, expected in zip(mv(zz, state), (sz * v for v in state)):
            close(actual, expected)
    matrix_close(add(*(outer(state) for state in vectors)), kron(I, I))

    def bob_marginal(joint):
        return [sum(joint[2 * a + b][2 * a + b].real for a in range(2)) for b in range(2)]

    bell_density = outer(vectors[0])
    for pauli in (Z, X):
        projectors = [kron(scale(add(I, scale(pauli, sign)), 0.5), I) for sign in (1, -1)]
        joint = add(*(mm(mm(projector, bell_density), projector) for projector in projectors))
        for observed, prior in zip(bob_marginal(joint), bob_marginal(bell_density)):
            close(observed, prior)
    close(bell_density[1][1] + bell_density[2][2], 0)  # differing Z outcomes

    state = [sqrt(3) / 2, 0, 0, 0.5]
    success, failure = [[1 / sqrt(3), 0], [0, 1]], [[sqrt(2 / 3), 0], [0, 0]]
    matrix_close(add(mm(dagger(success), success), mm(dagger(failure), failure)), I)
    branch = mv(kron(success, I), state)
    probability = inner(branch, branch).real
    close(probability, 0.5)
    close(abs(inner(vectors[0], [v / sqrt(probability) for v in branch])), 1)
    mixed_product = kron(scale(I, 0.5), [[1, 0], [0, 0]])
    purity = trace(mm(mixed_product, mixed_product))
    close(purity, 0.5)

    wins = []
    for a0, a1, b0, b1 in product((0, 1), repeat=4):
        answers_a, answers_b = (a0, a1), (b0, b1)
        wins.append(sum(answers_a[x] ^ answers_b[y] == x * y
                        for x, y in product((0, 1), repeat=2)) / 4)
    assert (min(wins), max(wins)) == (0.25, 0.75)

    return {
        'bell_labels_xx_zz': labels,
        'bob_z_marginal': bob_marginal(bell_density),
        'local_filter_success_probability': probability,
        'mixed_product_purity': purity,
        'chsh_fixed_win_bounds_for_local_models': [min(wins), max(wins)],
    }


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    print(json.dumps({'02': instrument_and_readout(), '03': joint_measurements()}, indent=2))
