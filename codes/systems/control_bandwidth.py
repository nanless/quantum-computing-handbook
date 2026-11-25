"""Reproduce the Chapter 19 teaching examples with the Python standard library."""

import cmath
import json
import math


def sampled_tone(frequency_mhz, sample_rate_mhz, sample):
    return cmath.exp(2j * math.pi * frequency_mhz * sample / sample_rate_mhz)


def cavity_frequency_ghz(side_mm, m, n):
    return 2.998e8 * math.hypot(m, n) / (2 * math.sqrt(11.7) * side_mm * 1e-3) / 1e9


def main():
    centers_mhz = list(range(-900, 901, 200))
    aliases = len({center % 1000 for center in centers_mhz})
    assert aliases == 5
    assert len({center % 2000 for center in centers_mhz}) == 10
    for low, high in zip(centers_mhz[:5], centers_mhz[5:]):
        for index in range(20):
            assert abs(sampled_tone(low, 1000, index) - sampled_tone(high, 1000, index)) < 1e-12

    occupied_edge_mhz = max(centers_mhz) + 20
    guard_mhz = 2000 / 2 - occupied_edge_mhz
    peak = 50_000 * 2_000_000_000 * 24
    assert guard_mhz == 80 and peak == 2_400_000_000_000_000

    modes = {(m, n): cavity_frequency_ghz(20, m, n) for m, n in [(1, 1), (1, 2), (2, 1), (2, 2)]}
    assert {mode for mode, frequency in modes.items() if 4 <= frequency <= 6} == {(1, 2), (2, 1)}
    assert modes[1, 2] == modes[2, 1]
    small_cavity = cavity_frequency_ghz(10, 1, 1)
    assert math.isclose(small_cavity, 6.1976, abs_tol=0.00005) and small_cavity > 6
    probability = 0.01
    entropy = -probability * math.log2(probability) - (1 - probability) * math.log2(1 - probability)
    assert math.isclose(entropy, 0.0807931359, abs_tol=1e-10)

    print(json.dumps({
        'complex_tone_classes_at_1_gsample_per_s': aliases,
        'guard_mhz_at_2_gsample_per_s': guard_mhz,
        'adc_peak_bit_per_s': peak,
        'adc_mean_bit_per_s': peak // 2,
        'cavity_10_mm_tm_110_ghz': small_cavity,
        'cavity_20_mm_tm_210_ghz': modes[2, 1],
        'iid_entropy_bit_per_position': entropy,
    }, indent=2))


if __name__ == '__main__':
    main()
