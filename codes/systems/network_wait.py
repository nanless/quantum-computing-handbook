"""Chapter 12: asymmetric geometric waits, analytic result plus seeded sampling."""
import json
import math
import random


def moments(p, r):
    assert 0 < p <= 1 and 0 < r <= 1
    early = 1 / (p + r - p * r)
    return 1 / p + 1 / r - early, 1 / p + 1 / r - 2 * early


def geom(rng, p):
    assert 0 < p <= 1
    if p == 1:
        return 1
    return math.floor(math.log1p(-rng.random()) / math.log1p(-p)) + 1


def main():
    p, r, shots, seed = .1, .2, 200_000, 69012
    exact_total, exact_storage = moments(p, r)
    assert abs(exact_total - 80 / 7) < 1e-12
    assert abs(exact_storage - 55 / 7) < 1e-12
    assert moments(1, 1) == (1, 0)
    rng = random.Random(seed)
    totals, storage = [], []
    for _ in range(shots):
        x, y = geom(rng, p), geom(rng, r)
        totals.append(max(x, y))
        storage.append(abs(x - y))
    means = [sum(xs) / shots for xs in (totals, storage)]
    ses = [(sum((x - m)**2 for x in xs) / (shots - 1) / shots)**.5
           for xs, m in zip((totals, storage), means)]
    assert all(abs(m - exact) < 6 * se for m, exact, se in
               zip(means, (exact_total, exact_storage), ses))
    print(json.dumps(dict(seed=seed, shots=shots, exact_total_slots=exact_total,
                         exact_storage_slots=exact_storage, sample_means=means,
                         sample_standard_errors=ses), indent=2))


if __name__ == '__main__':
    main()
