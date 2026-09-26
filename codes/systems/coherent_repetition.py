"""Chapter 10: coherent X rotations, ideal syndrome recovery, exact amplitudes.

Run: python3 codes/systems/coherent_repetition.py
Standard library only. Basis |q0 q1 q2>, q0 most significant; logical basis 000,111.
No sampling, no hardware, no threshold claim. Recovery assumes perfect checks.
"""
import json
from math import cos, sin, isclose, sqrt


def syndrome(word):
    a, b, c = ((word >> shift) & 1 for shift in (2, 1, 0))
    return a ^ b, b ^ c


def recover(theta, logical):
    c, s = cos(theta / 2), sin(theta / 2)
    amplitude = [0j] * 8
    for source, value in zip((0, 7), logical):
        for target in range(8):
            weight = bin(source ^ target).count("1")
            amplitude[target] += value * c ** (3 - weight) * (-1j * s) ** weight
    correction = {(0, 0): 0, (1, 0): 4, (1, 1): 2, (0, 1): 1}
    branches = {key: [0j, 0j] for key in correction}
    for word, value in enumerate(amplitude):
        key = syndrome(word)
        fixed = word ^ correction[key]
        assert fixed in (0, 7)
        branches[key][fixed // 7] += value
    rho = [[sum(v[i] * v[j].conjugate() for v in branches.values())
            for j in range(2)] for i in range(2)]
    return rho


def formula(theta, logical):
    c, s = cos(theta / 2), sin(theta / 2)
    p = s * s
    failure = 3 * p * p * (1 - p) + p ** 3
    lam = 2 * c ** 3 * s ** 3
    rho = [[logical[i] * logical[j].conjugate() for j in range(2)] for i in range(2)]
    return [[(1 - failure) * rho[i][j] + failure * rho[1-i][1-j]
             - 1j * lam * (rho[1-i][j] - rho[i][1-j])
             for j in range(2)] for i in range(2)]


def main():
    inputs = ([1+0j, 0j], [0j, 1+0j], [1/sqrt(2), 1/sqrt(2)],
              [1/sqrt(2), 1j/sqrt(2)])
    worst = 0
    for theta in (0, .2, -.2, 1.1):
        for logical in inputs:
            actual, expected = recover(theta, logical), formula(theta, logical)
            worst = max(worst, max(abs(actual[i][j] - expected[i][j])
                                   for i in range(2) for j in range(2)))
            assert isclose((actual[0][0] + actual[1][1]).real, 1, abs_tol=1e-12)
            assert actual[0][0].real * actual[1][1].real >= abs(actual[0][1])**2 - 1e-12
    assert worst < 1e-12
    rho = recover(.2, inputs[0])
    assert abs(rho[0][1].imag) > .001
    print(json.dumps({"theta_rad": .2, "logical_p1": rho[1][1].real,
                      "logical_Y": -2 * rho[0][1].imag,
                      "stochastic_model_Y": 0, "max_formula_error": worst}, indent=2))


if __name__ == "__main__":
    main()
