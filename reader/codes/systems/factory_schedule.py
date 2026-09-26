"""Chapter 11: ideal deterministic magic-state supply, unlimited storage."""
import json


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
    print(json.dumps([one, two], indent=2))


if __name__ == '__main__':
    main()
