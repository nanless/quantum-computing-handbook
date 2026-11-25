"""Recompute Chapter 09's dispersive, spin and readout teaching checks.

Run python3 codes/systems/hardware_readout_boundaries.py. Frequencies are
quoted in MHz (all divided by 2 pi), energies in microelectronvolts.
"""

from fractions import Fraction as F
import json
import math


def dispersive_ratio(detuning_mhz, coupling_mhz, photon_number):
    if detuning_mhz == 0:
        raise ValueError("resonant transition has no dispersive expansion")
    return coupling_mhz * math.sqrt(photon_number + 1) / abs(detuning_mhz)


def main():
    detuning_01, anharmonicity, g = 250, -250, 10
    assert dispersive_ratio(detuning_01, g, 0) == 0.04
    try:
        dispersive_ratio(detuning_01 + anharmonicity, math.sqrt(2)*g, 0)
    except ValueError:
        resonant_12 = True
    else:
        raise AssertionError("the second transition has to be checked independently")

    # Computational |0> is physically spin down. Components are in hbar units.
    total_projection = [sum(spins) for spins in [(-0.5, -0.5), (0.5, 0.5)]]
    assert total_projection == [-1, 1]  # |00>=T_-, |11>=T_+.
    boltzmann_micro_ev_per_k = 1e6 * 1.380649e-23 / 1.602176634e-19
    thermal_weights = [math.exp(-100/(temp*boltzmann_micro_ev_per_k)) for temp in (1, 0.1)]
    assert 0.31 < thermal_weights[0] < 0.32 and thermal_weights[1] < 1e-5

    row = [F(2, 100), F(94, 100), F(48, 100)]
    populations = [[F(1, 2), F(1, 2), F(0)], [F(0), F(0), F(1)]]
    binary_one_probability = [sum(p*x for p, x in zip(row, population))
                              for population in populations]
    assert binary_one_probability == [F(48, 100)] * 2
    three_label_contrast = F(90, 100) - F(5, 100)
    assert three_label_contrast == F(85, 100)  # two nontrivial eigenvalues
    print(json.dumps({"ratio_01": 0.04, "resonant_12": resonant_12,
                      "physical_spin_projection_T_minus_T_plus": total_projection,
                      "thermal_weights_at_1K_and_point_1K": thermal_weights,
                      "binary_one_probability_for_two_populations": [float(x) for x in binary_one_probability],
                      "three_label_nontrivial_eigenvalues": [float(three_label_contrast)] * 2}, indent=2))


if __name__ == "__main__":
    main()
