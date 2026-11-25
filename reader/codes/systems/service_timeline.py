"""Chapter 19: integrate a synthetic service log with overlapping downtime."""
import json


def union_length(intervals):
    merged = []
    for start, end in sorted(intervals):
        assert 0 <= start <= end <= 24
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return sum(b - a for a, b in merged)


def service_summary(planned, failure, degraded, peak=100_000, reduced=40_000):
    unavailable = union_length(planned + failure)
    out_of_spec = union_length(planned + failure + degraded)
    online = 24 - unavailable
    qualified = 24 - out_of_spec
    degraded_online = online - qualified
    raw_shots = (qualified * peak + degraded_online * reduced) * 3600
    qualified_shots = qualified * peak * 3600
    naive = (24 - union_length(planned)) * (24 - union_length(failure)) / 24 ** 2
    return {
        'online_hours': online,
        'qualified_hours': qualified,
        'degraded_online_hours': degraded_online,
        'online_fraction': online / 24,
        'qualified_fraction': qualified / 24,
        'naive_independent_fraction': naive,
        'raw_shots': raw_shots,
        'qualified_shots': qualified_shots,
        'qualified_wall_shots_per_second': qualified_shots / 86400,
    }


def main():
    planned, failure = [(2, 5)], [(4, 6)]
    original = service_summary(planned, failure, [(10, 12)])
    overlap = service_summary(planned, failure, [(5, 7)])
    assert union_length([]) == 0
    assert union_length([(0, 2), (1, 3), (3, 4)]) == 4
    assert original['online_hours'] == 20 and original['qualified_hours'] == 18
    assert original['raw_shots'] == 6_768_000_000
    assert overlap['qualified_hours'] == 19 and overlap['degraded_online_hours'] == 1
    assert overlap['raw_shots'] == 6_984_000_000
    print(json.dumps({**original, 'overlap_example': overlap}, indent=2))


if __name__ == '__main__':
    main()
