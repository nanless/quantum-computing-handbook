"""Reproduce Chapter 08's small-model boundaries with the Python standard library.

Run python3 codes/algorithms/application_boundaries.py. The printed JSON holds an
analytic QAE error budget, exact tail/kernel results, and Ritz checks on a toy
active-space matrix. No SDK, quantum circuit sampling, or hardware is used.
"""

import json
import math
from fractions import Fraction
from random import Random

from v4_algorithms_lab import jacobi_sym_eigh


def finance_checks():
    returns = (0, 0, 10, 30)
    error_budget = {}
    for queries in (125, 1000, 8000):
        scale = queries ** (-1 / 3)
        probability = sum((1 + math.sin(2 * scale * (value / 30 - 0.5))) / 2
                          for value in returns) / len(returns)
        estimate = 30 * (0.5 + (probability - 0.5) / scale)
        error_budget[queries] = {
            "scale": scale,
            "encoding_bias": abs(estimate - 10),
            "rescaled_probability_error_if_1_over_M": 30 / (queries * scale),
        }
    for first, second in ((125, 1000), (1000, 8000)):
        assert 3.98 < error_budget[first]["encoding_bias"] / error_budget[second]["encoding_bias"] < 4.02
        assert math.isclose(error_budget[first]["rescaled_probability_error_if_1_over_M"] /
                            error_budget[second]["rescaled_probability_error_if_1_over_M"], 4)

    distribution = list(zip((0, 10, 20, 100), map(Fraction, ("0.50", "0.25", "0.20", "0.05"))))
    tail_results = {}
    for confidence in (Fraction(3, 4), Fraction(7, 10)):
        tail = 1 - confidence
        cumulative = Fraction()
        for var, probability in distribution:
            cumulative += probability
            if cumulative >= confidence:
                break
        remaining = tail
        mass = Fraction()
        for loss, probability in reversed(distribution):
            selected = min(remaining, probability)
            mass += loss * selected
            remaining -= selected
            if remaining == 0:
                break
        tail_mean = mass / tail
        excess = sum(probability * max(0, loss - var) for loss, probability in distribution)
        assert tail_mean == var + excess / tail
        tail_results[str(confidence)] = [var, str(tail_mean)]
    assert tail_results == {"3/4": [10, "36"], "7/10": [10, "95/3"]}
    return {"small_angle_budget": error_budget, "var_and_cvar": tail_results}


def kernel_and_variance_checks():
    ps = (Fraction(1, 16), Fraction(1, 64))
    echo_shots = [math.ceil(p * (1 - p) / (p / 2)**2) for p in ps]
    swap_shots = [math.ceil((1 - p**2) / (p / 2)**2) for p in ps]
    assert echo_shots == [60, 252]
    assert swap_shots == [1020, 16380]

    x, x_flipped = (3, 4, 0, 0), (-3, 4, 0, 0)
    assert tuple(entry ** 2 for entry in x) == tuple(entry ** 2 for entry in x_flipped)
    sq_overlaps = [Fraction((a + b)**2, 50) for a, b, *_ in (x, x_flipped)]
    assert sq_overlaps == [Fraction(49, 50), Fraction(1, 50)]

    inv_sqrt2 = 1 / math.sqrt(2)
    ghz_plus = [inv_sqrt2, 0, 0, inv_sqrt2]
    ghz_minus = [inv_sqrt2, 0, 0, -inv_sqrt2]
    global_kernel = sum(a * b for a, b in zip(ghz_plus, ghz_minus)) ** 2
    local_a = [[sum(state[a * 2 + j] * state[b * 2 + j] for j in range(2))
                for a in range(2) for b in range(2)] for state in (ghz_plus, ghz_minus)]
    # Both qubits have the same marginal in each swap-symmetric GHZ state.
    local_kernel = math.exp(-2 * sum((a - b)**2 for a, b in zip(*local_a)))
    assert global_kernel == 0 and local_kernel == 1

    # Exact second moment for uniform z on [-1, 1] is 1/3.
    z_squared = Fraction(1, 3)
    block_variance = z_squared / 4
    covariance = -z_squared / 4
    assert 2 * block_variance + 2 * covariance == 0
    # R_y(theta)|0> measured along Z has loss cos(theta). Four quadrature
    # points integrate sin^2/cos^2 exactly for a uniform circle.
    angles = [index * math.pi / 2 for index in range(4)]
    loss_variance = sum(math.cos(angle)**2 for angle in angles) / 4
    gradient_variances = [sum((math.sin(angle) / scale)**2 for angle in angles) / 4
                          for scale in (1, 2)]
    assert loss_variance == 0.5 and gradient_variances == [0.5, 0.125]
    return {
        "echo_shots": echo_shots, "swap_shots": swap_shots,
        "signed_vector_overlaps": list(map(str, sq_overlaps)),
        "ghz_global_and_local_kernels": [global_kernel, local_kernel],
        "dla_non_support_variance": str(z_squared),
        "dla_block_variance_and_covariance": [str(block_variance), str(covariance)],
        "same_loss_under_rescaling": loss_variance,
        "gradient_variances_under_rescaling": gradient_variances,
    }


def qng_checks():
    theta, learning_rate = 0.2, 0.01
    local_gradient = math.sin(theta)
    metric = local_gradient**2 / 4
    longitude_step = -learning_rate * local_gradient / metric
    coordinate_energy = local_gradient * math.sin(longitude_step)
    geodesic_energy = -math.sin(4 * learning_rate)
    coordinate_velocity = local_gradient * longitude_step / learning_rate
    assert math.isclose(coordinate_velocity, -4)
    assert math.isclose(coordinate_energy, -0.0397303, abs_tol=1e-7)
    assert math.isclose(geodesic_energy, -0.0399893, abs_tol=1e-7)
    return {"longitude_step": longitude_step, "coordinate_step_energy": coordinate_energy,
            "great_circle_step_energy": geodesic_energy}


def addition_weight(occupation, filling):
    floor = 0.01
    if occupation < filling:
        return floor * occupation / filling
    return floor + (1 - floor) * (occupation - filling) / (1 - filling)


def score_samples(samples, hamiltonian, sector):
    support = sorted(set(samples), key=sector.index)
    indices = [sector.index(bitstring) for bitstring in support]
    projection = [[hamiltonian[i][j] for j in indices] for i in indices]
    energies, vectors = jacobi_sym_eigh(projection)
    vector = [row[0] for row in vectors]
    energy = energies[0]
    assert math.isclose(sum(amplitude**2 for amplitude in vector), 1)
    residual = math.sqrt(sum(
        (sum(term * amp for term, amp in zip(row, vector)) - energy * vector[i])**2
        for i, row in enumerate(projection)
    ))
    assert residual < 1e-12
    occupation = [sum(abs(amplitude)**2 * int(bit) for amplitude, bit in zip(vector, bits))
                  for bits in zip(*support)]
    return {"support": support, "energy": energy, "residual": residual, "occupation": occupation}


def recovery_checks():
    sector = ("1010", "0101", "1001", "0110")
    hamiltonian = [
        [-1.1246, 0.1820, 0.0800, 0.0800],
        [0.1820, 0.4318, -0.0500, -0.0500],
        [0.0800, -0.0500, -0.2000, 0.0400],
        [0.0800, -0.0500, 0.0400, -0.2000],
    ]
    legal = sector[:2]
    base = score_samples(legal, hamiltonian, sector)
    w0, w1 = [addition_weight(1 - u, 0.5) for u in base["occupation"][:2]]
    threshold = w0 / (w0 + w1)
    random = Random(20261126)
    noisy = "1101"
    draws = (0.0, 0.5, random.random())
    branches = []
    for draw in draws:
        bit = 0 if draw < threshold else 1
        recovered = noisy[:bit] + "0" + noisy[bit + 1:]
        assert recovered in sector
        branches.append(score_samples((*legal, recovered), hamiltonian, sector))
    classic = score_samples((*legal, "1001"), hamiltonian, sector)
    full = score_samples(sector, hamiltonian, sector)
    assert branches[0] == base and branches[1] == branches[2] == classic
    assert full["energy"] < classic["energy"] < base["energy"] < hamiltonian[0][0]
    assert [round(row["energy"], 4) for row in (base, classic, full)] == [-1.1456, -1.1532, -1.1601]
    assert abs(1 - threshold - 0.999731) < 2e-6
    next_occupation = [(a + b) / 2 for a, b in zip(base["occupation"], classic["occupation"])]
    assert all(math.isclose(sum(next_occupation[spin:spin + 2]), 1) for spin in (0, 2))
    assert math.comb(36, 27)**2 == 8862957169158400
    return {"reported_seed": 20261126, "drop_weights": [w0, w1], "probability_of_expanding_support": 1 - threshold,
            "base": base, "sampled_branches": branches, "same_rank_classical": classic,
            "next_occupation_from_two_batches": next_occupation, "full": full}


if __name__ == "__main__":
    print(json.dumps({"finance": finance_checks(), "kernels_and_dla": kernel_and_variance_checks(),
                      "qng": qng_checks(),
                      "configuration_recovery": recovery_checks()}, indent=2))
