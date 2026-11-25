"""Check Chapter 14 examples with the standard library and the archived GRAPE waveform.

Run python3 codes/systems/compilation_boundaries.py. This small deterministic
simulation uses radians/ns and has no network, SDK, device, or random sampling.
"""

import cmath
import csv
import json
import math

from round73_checks import SDK, dagger, expm, eye, mm


def matrix_distance(left, right):
    return max(abs(x - y) for row_a, row_b in zip(left, right) for x, y in zip(row_a, row_b))


def gate_checks():
    identity = eye(4)
    phased = [[1j * z for z in row] for row in identity]
    assert matrix_distance(phased, identity) == math.sqrt(2)

    x = [[0, 1], [1, 0]]
    y = [[0, -1j], [1j, 0]]
    z = [[1, 0], [0, -1]]
    factor = 1 / math.sqrt(2)
    hadamard = [[factor, factor], [factor, -factor]]
    t_gate = [[1, 0], [0, (1 + 1j) * factor]]
    assert matrix_distance(mm(hadamard, mm(x, dagger(hadamard))), z) < 1e-12
    transformed = mm(t_gate, mm(x, dagger(t_gate)))
    expected = [[factor * (a + b) for a, b in zip(x_row, y_row)] for x_row, y_row in zip(x, y)]
    assert matrix_distance(transformed, expected) < 1e-12

    theta, angle_a, angle_b = math.pi / 4, math.pi / 3, -math.pi / 6
    frame = eye(4)
    reversed_frame = eye(4)
    for i, (a, b) in enumerate(((1, 1), (1, -1), (-1, 1), (-1, -1))):
        frame[i][i] = cmath.exp(-0.5j * (a * angle_a + b * angle_b))
        reversed_frame[i][i] = cmath.exp(-0.5j * (a * angle_b + b * angle_a))
    partial = eye(4)
    full = eye(4)
    compensated = eye(4)
    delta = angle_a - angle_b
    for i, j, sign in ((1, 2, 1), (2, 1, -1)):
        partial[i][i] = compensated[i][i] = math.cos(theta)
        partial[i][j] = 1j * math.sin(theta)
        compensated[i][j] = partial[i][j] * cmath.exp(1j * sign * delta)
        full[i][i], full[i][j] = 0, 1j
    error = matrix_distance(mm(partial, frame), mm(reversed_frame, partial))
    assert abs(error - 1) < 1e-12
    assert matrix_distance(mm(partial, frame), mm(frame, compensated)) < 1e-12
    assert matrix_distance(mm(full, frame), mm(reversed_frame, full)) < 1e-12
    return {"kak_no_phase_error_for_iI": math.sqrt(2), "h_and_t_exact_t_counts": [0, 1],
            "partial_iswap_blind_frame_swap_error": error,
            "partial_iswap_compensated_error": matrix_distance(mm(partial, frame), mm(frame, compensated)),
            "full_iswap_frame_swap_error": matrix_distance(mm(full, frame), mm(reversed_frame, full))}


def score(columns, angle):
    target = [[math.cos(angle / 2), -1j * math.sin(angle / 2)],
              [-1j * math.sin(angle / 2), math.cos(angle / 2)]]
    block = [[columns[j][i] for j in range(2)] for i in range(2)]
    adj_product = mm(dagger(target), block)
    trace_overlap = adj_product[0][0] + adj_product[1][1]
    survival_sum = sum(abs(z)**2 for row in block for z in row)
    return {
        "basis_leakage": [abs(column[2])**2 for column in columns],
        "unconditional_average_overlap": (survival_sum + abs(trace_overlap)**2) / 6,
    }


def drag_columns(beta, steps, leakage_coupling=1.0, detuning=0.0):
    duration, width = 20.0, 5.0
    alpha = -2 * math.pi * 0.25
    edge = math.exp(-(duration / 2 / width)**2 / 2)
    area = math.sqrt(2 * math.pi) * width * math.erf(duration / (2 * math.sqrt(2) * width)) - duration * edge
    scale = math.pi / (2 * area)
    dt = duration / steps

    def derivative(t, state):
        x = (t - duration / 2) / width
        gaussian = math.exp(-x*x / 2)
        drive = scale * (gaussian - edge)
        quadrature = beta * scale * x * gaussian / (alpha * width)
        transition = (drive - 1j * quadrature) / 2
        qutrit_link = math.sqrt(2) * leakage_coupling * transition
        c0, c1, c2 = state
        return (-1j * transition * c1,
                -1j * (transition.conjugate() * c0 - detuning * c1 + qutrit_link * c2),
                -1j * (qutrit_link.conjugate() * c1 + (alpha - 2 * detuning) * c2))

    columns = []
    for initial in (0, 1):
        state = tuple(complex(i == initial) for i in range(3))
        for step in range(steps):
            time = step * dt
            k1 = derivative(time, state)
            k2 = derivative(time + dt/2, tuple(c + dt*k/2 for c, k in zip(state, k1)))
            k3 = derivative(time + dt/2, tuple(c + dt*k/2 for c, k in zip(state, k2)))
            k4 = derivative(time + dt, tuple(c + dt*k for c, k in zip(state, k3)))
            state = tuple(c + dt*(a + 2*b + 2*d + e)/6 for c, a, b, d, e in zip(state, k1, k2, k3, k4))
        assert abs(sum(abs(c)**2 for c in state) - 1) < 1e-12
        columns.append(state)
    return columns


def drag_checks():
    results = {}
    for beta, expected in ((0.0, 1.1628991e-5), (0.5, 2.8914764e-6), (1.0, 1.7219805e-11)):
        coarse = drag_columns(beta, 2000)
        fine = drag_columns(beta, 4000)
        assert matrix_distance(coarse, fine) < 2e-8
        result = score(fine, math.pi / 2)
        result["average_leakage"] = sum(result["basis_leakage"]) / 2
        assert math.isclose(result["average_leakage"], expected, rel_tol=2e-5)
        results[str(beta)] = result
    frame = (cmath.exp(0.0359j / 2), cmath.exp(-0.0359j / 2), 1)
    compensated = [tuple(z * frame[i] * frame[j] for i, z in enumerate(column))
                   for j, column in enumerate(fine)]
    results["virtual_z"] = score(compensated, math.pi / 2)
    assert abs(1 - results["virtual_z"]["unconditional_average_overlap"] - 1e-6) < 5e-9
    for mhz, expected in ((-0.483, 1.28e-7), (0.483, 1.72e-3)):
        columns = drag_columns(1, 4000, detuning=2 * math.pi * mhz / 1000)
        result = score(columns, math.pi / 2)
        assert math.isclose(1 - result["unconditional_average_overlap"], expected, rel_tol=0.01)
        results[f"detuning_{mhz}_MHz"] = result
    derivatives = []
    for steps in (2000, 4000):
        upper = drag_columns(1, steps, 1e-4)[1][2]
        lower = drag_columns(1, steps, -1e-4)[1][2]
        derivatives.append(abs((upper - lower) / (2e-4)))
    assert all(math.isclose(value, 2.84348e-6, rel_tol=3e-5) for value in derivatives)
    results["beta_one_derivative_at_zero_coupling"] = derivatives
    return results


def filter_checks():
    with (SDK / "grape-three-amplitudes.csv").open() as source:
        waveform = [(float(row["filtered_ux"]), float(row["filtered_uy"])) for row in csv.DictReader(source)]
    dt = 0.5
    alpha, delta = 2 * math.pi * -0.2, 2 * math.pi * 0.005
    decay = math.exp(-dt)
    last_x, last_y = waveform[-1]
    tail = [(last_x * decay**step, last_y * decay**step) for step in range(1, 21)]
    def propagate(waveform):
        unitary = eye(3)
        for ux, uy in waveform:
            link = (ux - 1j * uy) / 2
            h = [[0, link, 0], [link.conjugate(), -delta, math.sqrt(2) * link],
                 [0, math.sqrt(2) * link.conjugate(), -2 * delta + alpha]]
            unitary = mm(expm([[-1j * dt * z for z in row] for row in h]), unitary)
        return unitary

    def check(unitary):
        return score(list(zip(*unitary))[:2], math.pi)

    at_slot = check(propagate(waveform))
    with_tail = propagate([*waveform, *tail])
    extra_time = len(tail) * dt
    drift_removed = [list(row) for row in with_tail]
    free_phases = (0, -delta, -2 * delta + alpha)
    for i, phase in enumerate(free_phases):
        drift_removed[i] = [cmath.exp(1j * phase * extra_time) * z for z in drift_removed[i]]
    assert abs(at_slot["unconditional_average_overlap"] - 0.9809241) < 5e-8
    assert abs(at_slot["unconditional_average_overlap"] - check(with_tail)["unconditional_average_overlap"]) > 0.005
    return {"slot_ns": len(waveform) * dt, "added_tail_ns": extra_time,
            "at_slot": at_slot, "at_end_unadjusted_target": check(with_tail),
            "at_end_against_gate_followed_by_equal_idle": check(drift_removed),
            "tail_input_relative_amplitude_remaining": decay**len(tail)}


def feedback_and_cutting_checks():
    reports = {}
    for e in (0.03, 0.20):
        branches = [(m, b, (1 - e if m == b else e) / 2) for m in (0, 1) for b in (0, 1)]
        report_zero = sum(weight for _, b, weight in branches if b == 0)
        state_zero = sum(weight for m, b, weight in branches if m ^ b == 0)
        assert report_zero == 0.5 and state_zero == 1 - e
        reports[str(e)] = [report_zero, state_zero]

    e0, e1 = 0.03, 0.08
    readout = [[1 - e0, e1], [e0, 1 - e1]]
    reverse = [[0, 1], [1, 0]]
    reversed_readout = mm(reverse, mm(readout, reverse))
    symmetrized = [[(x + y) / 2 for x, y in zip(left, right)]
                   for left, right in zip(readout, reversed_readout)]
    gain = symmetrized[0][0] - symmetrized[1][0]
    assert math.isclose(gain, .89)
    degenerate = [[.5, .5], [.5, .5]]
    assert degenerate[0][0] - degenerate[1][0] == 0

    arrival_order = [("term_2", -0.2), ("term_1", 0.4)]
    coefficients = {"term_1": 1.5, "term_2": -0.5}
    by_label = sum(coefficients[key] * value for key, value in arrival_order)
    by_arrival = sum(scale * value for scale, (_, value) in zip(coefficients.values(), arrival_order))
    assert math.isclose(by_label, 0.7) and math.isclose(by_arrival, -0.5)
    return {"reported_zero_and_physical_zero": reports, "known_readout_gain": gain,
            "cutting_by_experiment_id": by_label, "cutting_by_arrival_order": by_arrival}


if __name__ == "__main__":
    print(json.dumps({"gates": gate_checks(), "drag": drag_checks(), "filter": filter_checks(),
                      "feedback_and_cutting": feedback_and_cutting_checks()}, indent=2))
