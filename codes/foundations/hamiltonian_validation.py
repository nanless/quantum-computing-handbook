#!/usr/bin/env python3
"""Deterministic standard-library checks for Q3 and Q4.

Run from the repository root:
    python3 codes/foundations/hamiltonian_validation.py --case all
"""
import argparse
import json
from math import cos, exp, hypot, pi, sin, sqrt

from foundations_lab import I, X, Y, Z, add, close, dagger, matrix_close, mm, mv, scale, trace


def pauli_step(x, z, duration):
    """Exp[-i duration (x X + z Z)] with angular rates in rad/s."""
    magnitude = hypot(x, z)
    angle = magnitude * duration
    return add(scale(I, cos(angle)), scale(add(scale(X, x), scale(Z, z)),
                                          -1j * sin(angle) / magnitude))


def finite_pulse(phase, steps):
    """Step in the laboratory frame and compare in the rotating frame."""
    carrier = 2 * pi * 200e6
    drive = 2 * pi * 50e6
    duration = 10e-9
    interval = duration / steps
    laboratory = I
    for index in range(steps):
        middle = (index + 0.5) * interval
        step = pauli_step(drive * cos(carrier * middle + phase), -carrier / 2, interval)
        laboratory = mm(step, laboratory)
    # R(t) = exp(+i carrier t Z/2), so U_rot = R†(t) U_lab(t).
    rotating = mm(pauli_step(0, carrier / 2, duration), laboratory)
    matrix_close(mm(dagger(rotating), rotating), I)
    target = scale(add(scale(X, cos(phase)), scale(Y, -sin(phase))), -1j)
    overlap = trace(mm(dagger(target), rotating))
    return abs(rotating[1][0]) ** 2, 1 - (abs(overlap) ** 2 + 2) / 6


def dispersive(detuning, anharmonicity, coupling):
    """All inputs and outputs are ordinary frequency values in MHz."""
    detuning_12 = detuning + anharmonicity
    if detuning == 0 or detuning_12 == 0:
        raise ValueError("resonant transition is outside the dispersive model")
    chi_two = coupling ** 2 / detuning
    chi_three = chi_two - coupling ** 2 / detuning_12
    return {
        "chi_2ls_mhz": chi_two,
        "chi_three_level_mhz": chi_three,
        "vacuum_coupling_detuning_ratios": [
            abs(coupling / detuning), abs(sqrt(2) * coupling / detuning_12)
        ],
        "ncrit_ground": (detuning / (2 * coupling)) ** 2,
        "ncrit_first_excited": ((detuning_12 / (2 * coupling)) ** 2 - 1) / 3,
    }


def case_q3():
    hf_over_k = 6.62607015e-34 * 4e9 / 1.380649e-23
    populations = []
    for temperature_kelvin in (0.050, 50):
        weight = exp(-hf_over_k / temperature_kelvin)
        populations.append(weight / (1 + weight))
    close(populations[0], 0.02105382395)
    close(populations[1], 0.49904015256)

    duration = 4e-9
    detuning_phase = 2 * pi * 250e6 * duration
    drive_area = 0.1
    phase = hypot(detuning_phase, drive_area)
    first_order = (drive_area * sin(detuning_phase / 2) / detuning_phase) ** 2
    rabi = (drive_area * sin(phase / 2) / phase) ** 2
    close(detuning_phase, 2 * pi)
    close(first_order, 0, 1e-32)
    close(rabi, 4.009e-11, 1e-14)

    pulse_reports = []
    for phase, expected in ((0, (0.995944, 0.002704)),
                            (pi / 2, (0.964700, 0.023534))):
        coarse = finite_pulse(phase, 20_000)
        fine = finite_pulse(phase, 40_000)
        for calculation, reported in zip(fine, expected):
            close(calculation, reported, 5e-7)
        close(coarse[0], fine[0], 4e-9)
        pulse_reports.append({
            "phase_rad": phase,
            "p1": fine[0],
            "average_gate_infidelity": fine[1],
            "probability_change_on_halving_step": abs(coarse[0] - fine[0]),
            "leakage": 0,
        })

    below_cavity = dispersive(-1500, -250, 100)
    straddling = dispersive(150, -250, 10)
    close(below_cavity["ncrit_ground"], 56.25)
    close(below_cavity["ncrit_first_excited"], 25.1875)
    close(straddling["chi_three_level_mhz"] / straddling["chi_2ls_mhz"], 2.5)
    try:
        dispersive(250, -250, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("accepted a resonant 1 to 2 transition")
    return {
        "p1_at_50_mk_and_50_k": populations,
        "first_null_250_mhz_at_4_ns": {"first_order_p1": first_order, "rwa_p1": rabi},
        "finite_pulses": pulse_reports,
        "below_cavity": below_cavity,
        "straddling": straddling,
    }


def case_q4():
    current_and_gradient = []
    # Strip the common complex phase to avoid large phase roundoff. The current
    # is in units of hbar |C|²/(m L²); gradient density is in units of |C|²/L³.
    for u in (2, 10, 100):
        amplitude = 1 / (1 + u)
        derivative = -amplitude ** 2 + 1j * (1 + u)
        current = (amplitude * derivative).imag
        close(current, 1)
        assert abs(derivative) ** 2 >= (1 + u) ** 2
        current_and_gradient.append([u, current, abs(derivative) ** 2])

    spacing = 0.5
    grid_energy = 2 / spacing ** 2 + 10 * sin(pi * spacing) ** 2
    # Midpoint integration independently evaluates the trial state's Rayleigh
    # quotient. The analytical Rayleigh principle supplies the upper bound.
    samples = 256
    points = [(index + 0.5) / samples for index in range(samples)]
    rayleigh = sum(2 * (pi * cos(pi * x)) ** 2
                   + 20 * sin(pi * x) ** 4 for x in points) / samples
    close(grid_energy, 18)
    close(rayleigh, pi ** 2 + 7.5)
    assert grid_energy > rayleigh

    generator = [[0, -1], [1, 0]]
    matrix_close(mm(generator, generator), scale(I, -1))
    states = [mv(add(scale(I, cos(alpha)), scale(generator, sin(alpha))), [1, 0])
              for alpha in (0, pi / 2, pi)]
    for state in states:
        close(sum(abs(amplitude) ** 2 for amplitude in state), 1)
    top = [abs(state[1]) ** 2 for state in states]
    for occupancy, expected in zip(top, (0, 1, 0)):
        close(occupancy, expected)
    coherent_overlap = abs(states[-1][0]) * exp(-pi ** 2 / 2)
    distance = sqrt(1 - coherent_overlap ** 2)
    close(distance, 0.9999741381)

    linewidth_millihertz = 1e3 / (2 * pi * 167)
    close(linewidth_millihertz, 0.953, 0.001)
    assert 0 not in [index - 9 / 2 for index in range(10)]
    return {
        "tail_u_dimensionless_current_and_gradient_density": current_and_gradient,
        "one_point_grid_energy": grid_energy,
        "continuum_ground_energy_upper_bound": rayleigh,
        "fock_top_occupation_at_0_half_full": top,
        "fock_final_trace_distance": distance,
        "sr87_natural_linewidth_millihertz": linewidth_millihertz,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("all", "q3", "q4"), default="all")
    args = parser.parse_args()
    cases = {"q3": case_q3, "q4": case_q4}
    chosen = cases if args.case == "all" else (args.case,)
    print(json.dumps({case: cases[case]() for case in chosen}, indent=2))
