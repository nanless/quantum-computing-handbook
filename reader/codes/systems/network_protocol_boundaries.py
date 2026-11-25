"""Reproduce Chapter 12 rate denominators, blind masks, and repeater budgets."""

import cmath
import json
import math


def binary_entropy(probability):
    return -sum(value * math.log2(value) for value in (probability, 1 - probability) if value)


def teaching_di_rate(chsh, error):
    phase_probability = (1 + math.sqrt((chsh / 2) ** 2 - 1)) / 2
    return 1 - binary_entropy(error) - binary_entropy(phase_probability)


def main():
    bb84 = 1 - 2 * binary_entropy(0.05)
    di_rate = teaching_di_rate(2.612, 0.0285)
    assert math.isclose(bb84, 0.427206086, abs_tol=1e-9)
    assert math.isclose(di_rate, 0.411045829, abs_tol=1e-9)

    # For each allowed instruction and secret angle, average the two compatible projectors.
    for instruction in range(8):
        for target in range(8):
            phases = [cmath.exp(1j * math.pi / 4 * ((instruction - target - 4 * bit) % 8)) for bit in (0, 1)]
            assert abs(sum(phases) / 4) < 1e-15

    fiber_speed_km_s = 200_000
    end_to_end = 1000 / fiber_speed_km_s
    full_neighbor = 2 * 20 / fiber_speed_km_s
    middle_herald = full_neighbor / 2
    layer_duration = 1e-6
    block_bound = 1 / (2 * layer_duration)
    assert (end_to_end * 1000, 2 * end_to_end * 1000) == (5.0, 10.0)
    assert (middle_herald * 1e6, full_neighbor * 1e6, block_bound) == (100.0, 200.0, 500_000.0)

    efficiencies = (1.0, 0.8, 0.6)
    distance_bounds = [50 * math.log10(2 * efficiency) for efficiency in efficiencies]
    for efficiency, distance in zip(efficiencies, distance_bounds):
        transmission = efficiency * 10 ** (-0.02 * distance)
        assert math.isclose(transmission, 0.5, abs_tol=1e-14)
        assert efficiency * 10 ** (-0.02 * (distance + 0.001)) < 0.5

    duration = 624 * 3600
    print(json.dumps({
        'bb84_teaching_bit_per_sifted_key_bit': bb84,
        'di_teaching_bit_per_key_round': di_rate,
        'lu_11_km_heralds_per_record_second': 1_208_000 / duration,
        'lu_11_km_estimated_secret_bit_per_record_second': 135_300 / duration,
        'blind_mask_checked_conditions': 64,
        'whole_path_round_trip_ms': 2 * end_to_end * 1000,
        'whole_path_one_way_ms': end_to_end * 1000,
        'whole_neighbor_round_trip_us': full_neighbor * 1e6,
        'midpoint_herald_us': middle_herald * 1e6,
        'two_layer_pipeline_upper_blocks_per_s': block_bound,
        'distance_suprema_km': dict(zip(efficiencies, distance_bounds)),
    }, indent=2))


if __name__ == '__main__':
    main()
