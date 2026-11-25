#!/usr/bin/env python3
"""Deterministic checks for Chapters 16, 17 and 21; Python standard library only."""
from fractions import Fraction
from itertools import product
import cmath
import json
import math

from simulation_engines_lab import (
    ExactDensityMatrix,
    MPS3,
    StabilizerTableau,
    matmul,
    pauli_string_matrix,
)


def verification_examples():
    ideal = tuple(Fraction(x, 10) for x in (4, 3, 2, 1))
    reported = (0, 1, 0, 0)
    ideal_xeb = 4 * sum(p * p for p in ideal) - 1
    reported_xeb = 4 * sum(p * q for p, q in zip(ideal, reported)) - 1
    distance = sum(abs(p - q) for p, q in zip(ideal, reported)) / 2
    assert (ideal_xeb, reported_xeb, distance) == (Fraction(1, 5), Fraction(1, 5), Fraction(7, 10))

    values = (0, 0, 3)
    mean = Fraction(sum(values), len(values))
    variance_single_basis = sum((x - mean)**2 for x in values) / len(values)
    variance_independent_bases = variance_single_basis / 200
    assert mean == 1 and variance_single_basis == 2 and variance_independent_bases == Fraction(1, 100)

    actual = (0, 1)
    target_hamiltonian = (0, Fraction(1, 5))
    mistaken_hamiltonian = tuple(reversed(target_hamiltonian))
    energy_target = sum(x * y for x, y in zip(actual, target_hamiltonian))
    energy_mistaken = sum(x * y for x, y in zip(actual, mistaken_hamiltonian))
    assert energy_mistaken == 0 and energy_target == target_hamiltonian[1] and actual[0] == 0
    p = Fraction(1, 1000)
    energy_error_in_ha = 1000 - ((1 - p) * 1000 - p * 1000)
    assert energy_error_in_ha == 2

    time = 2 * math.pi / 3
    l_path_amplitude = 1 / 3 - cmath.exp(-1j * time) / 2 + cmath.exp(-3j * time) / 6
    assert math.isclose(abs(l_path_amplitude)**2, 0.75, abs_tol=1e-12)
    doubled_phase_distance = 2 * (math.pi - math.acos(-0.998))
    assert math.isclose(doubled_phase_distance, 0.12651219775, abs_tol=1e-9)

    return {
        "linear_xeb_ideal": str(ideal_xeb),
        "linear_xeb_reported": str(reported_xeb),
        "total_variation_distance": str(distance),
        "shadow_200_repeated_one_basis_sd": math.sqrt(variance_single_basis),
        "shadow_200_independent_bases_sd": math.sqrt(variance_independent_bases),
        "target_energy_versus_wrong_model": [str(energy_target), str(energy_mistaken)],
        "energy_error_in_ha": str(energy_error_in_ha),
        "laplacian_path_max": abs(l_path_amplitude)**2,
        "negative_spectral_mode_phase_distance": doubled_phase_distance,
    }


def computation_models():
    graph = (0.5, 0.5, 0.5, -0.5)
    branch_probabilities = {}
    for x, z in product((0, 1), repeat=2):
        projected = (graph[z] + (-1)**x * graph[z + 2]) / math.sqrt(2)
        branch_probabilities[str(x) + str(z)] = abs(projected)**2
    assert math.isclose(branch_probabilities["00"], 0.5, abs_tol=1e-12)
    assert math.isclose(branch_probabilities["11"], 0.5, abs_tol=1e-12)
    assert branch_probabilities["01"] == branch_probabilities["10"] == 0
    photon_loss = 1 - (1 - 0.027)**4
    assert math.isclose(photon_loss, 0.103704200559, abs_tol=1e-12)

    # The saturated-gap qubit is held at the starting point, then swept quickly.
    # Use exact exponentials for midpoint-constant slices of the fast segment.
    eta = 0.1
    steps = 2000
    step = eta / steps
    vector = (1.0 + 0j, 0j)
    for i in range(steps):
        u = (i + 0.5) / steps
        smooth_path = u**2 * (3 - 2 * u)
        c, x = math.cos(math.pi * smooth_path), math.sin(math.pi * smooth_path)
        a, b = vector
        vector = (
            math.cos(step) * a + 1j * math.sin(step) * (c * a + x * b),
            math.cos(step) * b + 1j * math.sin(step) * (x * a - c * b),
        )
    assert math.isclose(sum(abs(v)**2 for v in vector), 1, abs_tol=1e-12)
    final_ground = abs(vector[1])**2
    assert final_ground < eta**2

    first = cmath.exp(-1j * math.pi / 8)
    second = cmath.exp(3j * math.pi / 8)
    assert max(abs(x**4 + 1j) for x in (first, second)) < 1e-12
    assert max(abs(x**8 + 1) for x in (first, second)) < 1e-12
    h = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
    sigma1 = [[first, 0], [0, second]]
    sigma2 = matmul(matmul(h, sigma1), h)
    lhs = matmul(matmul(sigma1, sigma2), sigma1)
    rhs = matmul(matmul(sigma2, sigma1), sigma2)
    braid_error = max(abs(a - b) for l, r in zip(lhs, rhs) for a, b in zip(l, r))
    assert braid_error < 1e-12
    return {
        "graph_measurement_joint_probabilities": branch_probabilities,
        "four_photon_loss_event": photon_loss,
        "constant_gap_fast_sweep_probability": final_ground,
        "constant_gap_bound": eta**2,
        "ising_r_power_4": "-iI",
        "ising_r_power_8": "-I",
        "braid_residual": braid_error,
    }


def simulator_examples():
    repeats = []
    for forced in (0, 1):
        tableau = StabilizerTableau(1)
        tableau.h(0)
        tableau.s(0)
        tableau.h(0)
        assert tableau.destabilizers() == ["+X"] and tableau.stabilizers() == ["-Y"]
        assert tableau.measure_z(0, forced_outcome=forced) == (forced, True)
        tableau.assert_symplectic_invariants()
        assert tableau.measure_z(0) == (forced, False)
        repeats.append(forced)

    wrong_row_product = matmul([[0, 1j], [-1j, 0]], pauli_string_matrix("X"))
    assert wrong_row_product == [[1j, 0], [0, -1j]]

    numeric_ranks = []
    for e in (1e-6, 1e-8, 1e-9, 1e-10):
        state = [complex(math.sqrt(1 - e**2)), 0j, 0j, 1j * e, 0j, 0j, 0j, 0j]
        mps = MPS3.from_statevector(state)
        mps.assert_left_canonical()
        assert (len(mps.sigma1), len(mps.sigma2)) == (1, 2)
        assert math.isclose(mps.sigma2[1], e, rel_tol=1e-12)
        assert max(abs(a - b) for a, b in zip(mps.contract_statevector(), state)) < 1e-12
        numeric_ranks.append(mps.sigma2[1])

    noise = 0.02
    density = ExactDensityMatrix(2, [1, 0, 0, 0])
    density.apply_depolarizing(0, noise)
    density.apply_depolarizing(1, noise)
    local_zz = density.expectation_pauli("ZZ")
    # Apply full two-qubit replacement to |00><00| as a classical mixture.
    full = (1 - 3 * noise / 4, noise / 4, noise / 4, noise / 4)
    zz = (1, -1, -1, 1)
    joint_zz = sum(a * b for a, b in zip(full, zz))
    assert math.isclose(local_zz, 0.9604, abs_tol=1e-12)
    assert math.isclose(joint_zz, 0.98, abs_tol=1e-12)

    return {
        "tableau_repeats": repeats,
        "literal_incompatible_row_product": "+iZ",
        "mps_second_bond_small_singular_values": numeric_ranks,
        "local_noise_zz": local_zz,
        "two_qubit_block_noise_zz": joint_zz,
    }


if __name__ == "__main__":
    print(json.dumps({
        "chapter_16": verification_examples(),
        "chapter_17": computation_models(),
        "chapter_21": simulator_examples(),
    }, indent=2))
