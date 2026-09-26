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


def main():
    planned, failure, degraded = [(2, 5)], [(4, 6)], [(10, 12)]
    unavailable = union_length(planned + failure)
    out_of_spec = union_length(planned + failure + degraded)
    online_hours, qualified_hours = 24 - unavailable, 24 - out_of_spec
    assert unavailable == 4 and out_of_spec == 6
    assert union_length([]) == 0
    assert union_length([(0, 2), (1, 3), (3, 4)]) == 4
    peak, reduced = 100_000, 40_000
    # Here degraded interval does not overlap outage. Those shots fail the
    # declared quality threshold, although the machine can still produce them.
    raw_shots = (qualified_hours * peak + 2 * reduced) * 3600
    qualified_shots = qualified_hours * peak * 3600
    print(json.dumps(dict(online_hours=online_hours, qualified_hours=qualified_hours,
        online_fraction=online_hours / 24, qualified_fraction=qualified_hours / 24,
        naive_independent_fraction=(21 / 24) * (22 / 24),
        raw_shots=raw_shots, qualified_shots=qualified_shots,
        qualified_wall_shots_per_second=qualified_shots / 86400), indent=2))


if __name__ == '__main__':
    main()
