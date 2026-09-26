"""Chapter 14: verify a routed CNOT on every basis vector and a complex state.

Index ordering is |q0 q1 q2>, q0 the most significant bit. No external SDK.
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


def main():
    states = [[complex(i == j) for i in range(8)] for j in range(8)]
    rng = random.Random(69014)
    psi = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(8)]
    norm = math.sqrt(sum(abs(a)**2 for a in psi))
    states.append([a / norm for a in psi])
    worst = 0.
    for state in states:
        ideal = cx(state, 0, 2)
        routed = cx(swap(state, 0, 1), 1, 2)
        interpreted = restore_logical_order(routed, (1, 0, 2))
        error = max(abs(a - b) for a, b in zip(ideal, interpreted))
        worst = max(worst, error)
        assert error < 1e-12
        restored = swap(routed, 0, 1)
        assert max(abs(a - b) for a, b in zip(ideal, restored)) < 1e-12
    # Without relabelling, basis |100> is a visible counterexample.
    assert cx(swap(states[4], 0, 1), 1, 2) != cx(states[4], 0, 2)
    print(json.dumps(dict(seed=69014, verified_states=len(states),
                         max_amplitude_error=worst, cx_without_restore=4,
                         cx_with_restore=7, logical_to_physical=[1, 0, 2]), indent=2))


if __name__ == '__main__':
    main()
