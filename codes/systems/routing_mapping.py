"""Chapters 09 and 14: verify three nearest-neighbor implementations of CX(0, 2).

Run python3 codes/systems/routing_mapping.py. Only the standard library is used.
The phase check takes one common phase across all eight columns of the operator.
Index ordering is |q0 q1 q2>, q0 the most significant bit.
"""
import json
import math
import random


def bit(index, qubit):
    return (index >> (2 - qubit)) & 1


def cx(state, control, target):
    assert control != target and len(state) == 8
    result = [0j] * 8
    for i, amplitude in enumerate(state):
        j = i ^ (1 << (2 - target)) if bit(i, control) else i
        result[j] = amplitude
    return result


def swap(state, a, b):
    return cx(cx(cx(state, a, b), b, a), a, b)


def restore_logical_order(state, logical_to_physical):
    result = [0j] * 8
    for physical_index, amplitude in enumerate(state):
        logical_index = sum(bit(physical_index, p) << (2 - q)
                            for q, p in enumerate(logical_to_physical))
        result[logical_index] = amplitude
    return result


def bridge(state):
    for control, target in [(0, 1), (1, 2), (0, 1), (1, 2)]:
        state = cx(state, control, target)
    return state


def common_phase_error(reference_columns, actual_columns):
    pairs = [(expected, observed) for expected_column, observed_column in
             zip(reference_columns, actual_columns)
             for expected, observed in zip(expected_column, observed_column)]
    expected, observed = max(pairs, key=lambda pair: abs(pair[0]))
    phase = observed / expected
    assert abs(abs(phase) - 1) < 1e-12
    return max(abs(observed - phase * expected) for expected, observed in pairs), phase


def main():
    basis = [[complex(i == j) for i in range(8)] for j in range(8)]
    rng = random.Random(69014)
    psi = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(8)]
    norm = math.sqrt(sum(abs(a)**2 for a in psi))
    psi = [a / norm for a in psi]

    def expected(state):
        # Input bit q0 toggles physical bit q2, without using the CX routine.
        return [state[index ^ (index >> 2)] for index in range(8)]

    def routed(state):
        return cx(swap(state, 0, 1), 1, 2)

    mapping = (1, 0, 2)
    implementations = {
        "bridge": bridge,
        "with_unroute": lambda state: swap(routed(state), 0, 1),
        "with_final_relabel": lambda state: restore_logical_order(routed(state), mapping),
    }
    target = [expected(state) for state in basis]
    errors = {}
    for name, implementation in implementations.items():
        error, phase = common_phase_error(target, [implementation(state) for state in basis])
        errors[name] = error
        assert error < 1e-12
        assert max(abs(actual - phase * ideal)
                   for actual, ideal in zip(implementation(psi), expected(psi))) < 1e-12

    # A basis-dependent phase changes the operator even with identical readout.
    wrong_sign = target.copy()
    wrong_sign[4] = [-value for value in target[4]]
    assert common_phase_error(target, wrong_sign)[0] == 2
    assert routed(basis[4]) == basis[3]  # physical |011>
    assert expected(basis[4]) == basis[5]  # logical |101>
    print(json.dumps(dict(seed=69014, verified_states=len(basis) + 1,
                         max_amplitude_error=max(errors.values()), implementation_errors=errors,
                         cx_bridge=4, cx_without_restore=4, cx_with_restore=7,
                         logical_to_physical=list(mapping), no_fault_four=0.99**4,
                         no_fault_seven=0.99**7), indent=2))


if __name__ == '__main__':
    main()
