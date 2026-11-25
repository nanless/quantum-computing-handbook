#!/usr/bin/env python3
"""Deterministic offline checks for the circuit and noise chapters.

Run: python3 codes/foundations/circuit_channel_boundaries.py
Stdlib only. State and density matrices use highest bit first. No sampling or SDK.
"""
import cmath
from itertools import product
import json
import math

from foundations_lab import (
    H, I, PLUS, X, Y, Z, ZERO, add, close, dagger, entropy, kron, matrix_close,
    mm, mv, outer, rotation, scale, tensor, trace,
)


def circuit_checks():
    """Compare early measurement and coherent recording on R, A, B."""
    data = [math.sqrt(.3), 0, .4j, math.sqrt(.54)]
    record_cnot = [0j] * 8
    for index, amplitude in enumerate(data):
        a = index >> 1
        record_cnot[4 * a + index] = amplitude
    # Apply H on A after the recording and Z on B when R is 1.
    coherent = mv(kron(I, kron(H, I)), record_cnot)
    coherent = [amplitude * (-1) ** ((index >> 2) * (index & 1))
                for index, amplitude in enumerate(coherent)]

    branch_weights = []
    data_outputs = []
    for record in (0, 1):
        projector = kron(outer([1 - record, record]), I)
        projected = mm(mm(projector, outer(data)), projector)
        unitary = kron(H, I if record == 0 else Z)
        early_measurement = mm(mm(unitary, projected), dagger(unitary))
        late_measurement = outer(coherent[4 * record:4 * (record + 1)])
        matrix_close(late_measurement, early_measurement)
        branch_weights.append(trace(late_measurement).real)
        data_outputs.append(late_measurement)
    close(branch_weights[0], .3)
    close(branch_weights[1], .7)
    discarded_result = add(*data_outputs)
    data_bit_zero = (discarded_result[0][0] + discarded_result[1][1]).real
    close(data_bit_zero, .5)

    phase = cmath.exp(1j * math.pi / 4)
    t = [[1, 0], [0, phase]]
    assert mv(t, ZERO) == ZERO
    matrix_close(mm(mm(t, Z), dagger(t)), Z)
    matrix_close(mm(mm(t, X), dagger(t)), scale(add(X, Y), 1 / math.sqrt(2)))
    return {'record_weights': branch_weights, 'late_data_bit_zero': data_bit_zero,
            'deferred_instrument_unchanged': True, 't_gate_leaves_zero_state': True}


def noise_checks():
    """Recompute instrument probabilities, repeated errors and trace tests."""
    rho = outer(PLUS)
    k0, k1 = [[1, 0], [0, .8]], [[0, .6], [0, 0]]
    no_jump, jump = [mm(mm(k, rho), dagger(k)) for k in (k0, k1)]
    efficiency = .5
    no_click = add(no_jump, scale(jump, 1 - efficiency))
    click = scale(jump, efficiency)
    matrix_close(add(no_click, click), add(no_jump, jump))
    no_jump_p, no_click_p = trace(no_jump).real, trace(no_click).real
    close(no_jump_p, .82)
    close(no_click_p, .91)

    def negative_x_probability(angle):
        output = mv(H, mv(rotation(Z, angle), PLUS))
        return abs(output[1]) ** 2

    depth, epsilon = 10, .2
    independent = list(product((-1, 1), repeat=depth))
    p_independent = sum(negative_x_probability(epsilon * sum(row))
                        for row in independent) / len(independent)
    p_reused = sum(negative_x_probability(sign * depth * epsilon)
                   for sign in (-1, 1)) / 2
    close(p_independent, (1 - math.cos(epsilon) ** depth) / 2)
    close(p_reused, (1 - math.cos(epsilon * depth)) / 2)
    close(p_independent, .0911859661)
    close(p_reused, .7080734183)

    def two_point_output(state, elapsed):
        rotations = [rotation(Z, sign * elapsed) for sign in (-1, 1)]
        return scale(add(*(outer(mv(unitary, state)) for unitary in rotations)), .5)

    minus = mv(Z, PLUS)
    lost_plus = two_point_output(PLUS, math.pi / 2)
    lost_minus = two_point_output(minus, math.pi / 2)
    matrix_close(lost_plus, lost_minus)
    matrix_close(lost_plus, scale(I, .5))
    revived_plus = two_point_output(PLUS, math.pi)
    revived_minus = two_point_output(minus, math.pi)
    close(trace(mm(revived_plus, revived_minus)), 0)

    rho_y = outer([1 / math.sqrt(2), 1j / math.sqrt(2)])
    choi = add(scale(kron(I, I), .5), scale(kron(Y, I), .1))
    transpose = list(zip(*rho_y))
    correct_trace = trace(mm(kron(transpose, I), choi)).real
    missing_transpose_trace = trace(mm(kron(rho_y, I), choi)).real
    close(correct_trace, .8)
    close(missing_transpose_trace, 1.2)

    mixed = scale(I, .5)
    depolarized_at_one = scale(add(*(mm(mm(gate, outer(ZERO)), gate)
                                    for gate in (X, Y, Z))), 1 / 3)
    matrix_close(depolarized_at_one, [[1 / 3, 0], [0, 2 / 3]])
    matrix_close(scale(add(outer(PLUS), outer(minus)), .5), mixed)
    partial_entropy_drop = 1 - entropy([.75, .25])
    bound_in_kbt = partial_entropy_drop * math.log(2)
    swap_heat_in_kbt = math.log(3) / 4
    close(partial_entropy_drop, .1887218755)
    assert bound_in_kbt <= swap_heat_in_kbt < math.log(2)
    return {
        'no_jump': {'probability': no_jump_p, 'excited': no_jump[1][1].real / no_jump_p},
        'no_click': {'probability': no_click_p, 'excited': no_click[1][1].real / no_click_p},
        'independent_ten_layer_error': p_independent, 'reused_ten_layer_error': p_reused,
        'classical_two_point_revival': True, 'choi_trace': correct_trace,
        'choi_trace_without_transpose': missing_transpose_trace,
        'pauli_q_one_zero_input_probabilities': [depolarized_at_one[i][i].real for i in (0, 1)],
        'partial_entropy_drop_bits': partial_entropy_drop, 'swap_heat_over_kbt': swap_heat_in_kbt,
    }


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: assertions are part of the experiment')
    print(json.dumps({'circuit': circuit_checks(), 'noise': noise_checks()}, indent=2))
