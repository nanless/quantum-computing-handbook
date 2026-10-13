#!/usr/bin/env python3
"""Independent stdlib models for S71-MPF/OBP/NOISE/SQD/RNG/TOMO.

No third-party code is imported. Basis is |0>, |1>; rotation angles are
radians. All matrices and samples are teaching inputs, not device data.
Run from either the repository or the portable reader with Python 3.9+.
"""
import cmath
import hashlib
import json
import math
import pathlib
import random
from fractions import Fraction


def matmul(a, b):
    assert len(a[0]) == len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def dagger(a):
    return [[complex(a[j][i]).conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def mv(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def inner(x, y):
    return sum(complex(v).conjugate() * w for v, w in zip(x, y))


def expectation(a, x):
    value = inner(x, mv(a, x))
    assert abs(value.imag) < 1e-12
    return value.real


def scale(a, coefficient):
    return [[coefficient * v for v in row] for row in a]


def add(a, b):
    return [[v + w for v, w in zip(ar, br)] for ar, br in zip(a, b)]


I = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
Z = [[1, 0], [0, -1]]


def pauli_exp(pauli, time):
    # exp(-i*time*P), P^2=I; time already includes the energy/hbar scale.
    return add(scale(I, math.cos(time)), scale(pauli, -1j * math.sin(time)))


def mpf():
    weights = [Fraction(-1, 3), Fraction(4, 3)]
    steps = [2, 4]
    assert sum(weights) == 1
    assert sum(w / k**2 for w, k in zip(weights, steps)) == 0
    true = Fraction(1, 4)
    samples = [true + Fraction(3, 25) / k**2 + Fraction(3, 100) / k**4
               for k in steps]
    combined = sum(w * x for w, x in zip(weights, samples))
    assert combined == Fraction(1597, 6400)
    assert combined - true == Fraction(-3, 6400)
    gamma = sum(abs(w) for w in weights)
    shots = [1800, 7200]
    variance_bound = sum(float(w)**2 / n for w, n in zip(weights, shots))
    assert math.isclose(variance_bound, float(gamma)**2 / sum(shots))
    # Nearby step counts give much larger absolute weights.
    nearby = [Fraction(-16, 9), Fraction(25, 9)]
    assert sum(nearby) == 1
    assert sum(w / k**2 for w, k in zip(nearby, [4, 5])) == 0
    assert sum(abs(w) for w in nearby) == Fraction(41, 9)
    # Independent exact two-dimensional Hamiltonian test, H=X+Z, hbar=1.
    t = 0.7
    exact_u = add(scale(I, math.cos(math.sqrt(2) * t)),
                  scale(add(X, Z), -1j * math.sin(math.sqrt(2) * t) / math.sqrt(2)))
    target = expectation(Z, mv(exact_u, [1, 0]))
    values = []
    for k in steps:
        slice_u = matmul(matmul(pauli_exp(X, t / (2*k)),
                               pauli_exp(Z, t / k)), pauli_exp(X, t / (2*k)))
        state = [1, 0]
        for _ in range(k):
            state = mv(slice_u, state)
        assert abs(inner(state, state) - 1) < 1e-12
        values.append(expectation(Z, state))
    mpf_value = sum(float(w) * x for w, x in zip(weights, values))
    assert abs(mpf_value - target) < abs(values[-1] - target)
    # This inequality is only for the specified ideal model and input.
    return {'steps': steps, 'weights': [str(w) for w in weights],
            'synthetic_values': list(map(float, samples)),
            'synthetic_combined': float(combined), 'gamma': float(gamma),
            'shots': shots, 'variance_upper_bound': variance_bound,
            'nearby_gamma': float(sum(abs(w) for w in nearby)),
            'ideal_hamiltonian': {'time': t, 'target': target,
                                 'individual': values, 'combined': mpf_value}}


def obp_noise():
    theta = math.pi / 6
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    u = [[c, -s], [s, c]]
    pulled_z = matmul(matmul(dagger(u), Z), u)
    analytic_z = add(scale(Z, math.cos(theta)), scale(X, -math.sin(theta)))
    assert max(abs(pulled_z[i][j] - analytic_z[i][j])
               for i in range(2) for j in range(2)) < 1e-12
    plus = [1 / math.sqrt(2)] * 2
    full = expectation(Z, mv(u, plus))
    assert math.isclose(full, expectation(pulled_z, plus), abs_tol=1e-12)
    truncated = expectation(scale(Z, math.cos(theta)), plus)
    discarded_l1 = abs(math.sin(theta))
    assert math.isclose(abs(full - truncated), discarded_l1, abs_tol=1e-12)
    p = 0.1
    state = mv(u, [1, 0])
    noisy_x = (1-p) * expectation(X, state) + p * expectation(X, mv(Z, state))
    pulled_noisy_x = matmul(matmul(dagger(u), scale(X, 1-2*p)), u)
    assert math.isclose(noisy_x, expectation(pulled_noisy_x, [1, 0]), abs_tol=1e-12)
    assert math.isclose(noisy_x, 0.4, abs_tol=1e-12)
    return {'theta_rad': theta, 'Z_on_plus': full,
            'truncated_Z_on_plus': truncated, 'discarded_l1_bound': discarded_l1,
            'phase_flip_probability': p, 'noisy_X_on_zero': noisy_x,
            'ideal_X_on_zero': expectation(X, state)}


def sqd():
    # Three arbitrary orthonormal labels; not a molecular chemistry model.
    h = [[0, -1, 0], [-1, 0, -1], [0, -1, 0]]
    ritz = [1/math.sqrt(2), 1/math.sqrt(2), 0]
    energy = expectation(h, ritz)
    residual = math.sqrt(sum(abs(v + w)**2 for v, w in zip(mv(h, ritz), ritz)))
    assert math.isclose(energy, -1)
    assert math.isclose(residual, 1/math.sqrt(2))
    assert energy >= -math.sqrt(2)
    # Duplicate columns are not an orthonormal basis. This independent
    # counterexample has exact ground energy -1, third eigenvalue 2.
    hd = [[0, -1, 0], [-1, 0, 0], [0, 0, 2]]
    duplicate_p = [[1, 0, 1], [0, 1, 0], [0, 0, 0]]
    gram = matmul(dagger(duplicate_p), duplicate_p)
    projected = matmul(matmul(dagger(duplicate_p), hd), duplicate_p)
    fake_vector = [0.5, 1/math.sqrt(2), 0.5]
    fake_eigenvalue = expectation(projected, fake_vector)
    physical_vector = mv(duplicate_p, fake_vector)
    physical_norm = inner(physical_vector, physical_vector).real
    physical_energy = expectation(hd, physical_vector) / physical_norm
    assert math.isclose(fake_eigenvalue, -math.sqrt(2))
    assert physical_energy >= -1 - 1e-12
    assert gram == [[1+0j, 0j, 1+0j], [0j, 1+0j, 0j], [1+0j, 0j, 1+0j]]
    return {'raw_labels': ['001', '010', '001'], 'distinct_dimension': 2,
            'full_ground_energy': -math.sqrt(2), 'ritz_energy': energy,
            'ritz_residual_norm': residual, 'duplicate_counterexample': {
                'true_ground': -1, 'naive_eigenvalue': fake_eigenvalue,
                'physical_rayleigh_quotient': physical_energy}}


def indexed_randomness():
    # Scheduling illustration, NOT an implementation of Philox or a proof
    # of independent streams. Stable job IDs are part of the saved input.
    tasks = list(range(6))
    def draw(task):
        key = hashlib.sha256(f'71:{task}'.encode('ascii')).digest()
        rng = random.Random(int.from_bytes(key, 'big'))
        return [rng.randrange(256) for _ in range(3)]
    forward = {i: draw(i) for i in tasks}
    reverse = {i: draw(i) for i in reversed(tasks)}
    assert forward == reverse
    return {'base_label': 71, 'draws_by_stable_task_id': forward,
            'reverse_schedule_matches': forward == reverse}


def tomography():
    settings = {str(n): 12**n for n in [1, 2, 5, 10]}
    assert settings['5'] == 248832
    assert settings['10'] == 61917364224
    gamma = 0.3
    # Two channels agree on |0><0| but disagree on the coherent |+> input.
    amplitude_offdiagonal = math.sqrt(1-gamma) / 2
    dephased_offdiagonal = 0.0
    assert amplitude_offdiagonal > dephased_offdiagonal
    return {'full_product_pauli_QPT_settings': settings,
            'shots_per_setting': 1000, 'five_qubit_total_shots': settings['5'] * 1000,
            'same_zero_input': True,
            'plus_input_amplitude_damping_offdiagonal': amplitude_offdiagonal,
            'plus_input_complete_dephasing_offdiagonal': dephased_offdiagonal}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: numerical checks need assertions')
    results = {'scope': 'independent authored ideal/synthetic models; no vendor execution',
               'MPF': mpf(), 'OBP_NOISE': obp_noise(), 'SQD': sqd(),
               'RNG': indexed_randomness(), 'TOMO': tomography()}
    dest = pathlib.Path(__file__).with_name('workflow-results.json')
    dest.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
