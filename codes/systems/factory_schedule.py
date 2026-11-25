"""Chapter 11: ideal deterministic magic-state supply, unlimited storage."""
import json
from math import comb


def schedule(demands, factories, period=3, layer_duration=1):
    assert factories > 0 and period > 0 and layer_duration > 0
    time = consumed = 0
    starts = []
    for demand in demands:
        assert isinstance(demand, int) and demand >= 0
        consumed += demand
        # First batch arrives at period, not t=0. Production continues during gates.
        batches = (consumed + factories - 1) // factories
        start = max(time, batches * period)
        assert (start // period) * factories >= consumed
        starts.append(start)
        time = start + layer_duration
    return dict(factories=factories, starts=starts, finish=time,
                states_used=consumed, states_produced=(time // period) * factories)


def main():
    one, two = schedule([1, 3, 1], 1), schedule([1, 3, 1], 2)
    assert one['starts'] == [3, 12, 15] and one['finish'] == 16
    assert two['starts'] == [3, 6, 9] and two['finish'] == 10
    assert schedule([], 1)['finish'] == 0
    uniform = schedule([10] * 10, 20, period=20, layer_duration=10)
    front_loaded = schedule([91] + [1] * 9, 20, period=20, layer_duration=10)
    assert uniform['finish'] == 120 and front_loaded['finish'] == 200

    def supply_at_least_three(attempts):
        return 1 - sum(comb(attempts, k) * .08 ** k * .92 ** (attempts - k)
                       for k in range(3))

    assert abs(supply_at_least_three(38) - .595318) < 1e-6
    assert supply_at_least_three(76) <= .95 < supply_at_least_three(77)
    print(json.dumps([one, two, uniform, front_loaded, {
        'supply_probability_38': supply_at_least_three(38),
        'minimum_attempts_at_95_percent': 77,
    }], indent=2))


if __name__ == '__main__':
    main()
