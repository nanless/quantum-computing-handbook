"""Chapter 10: exhaustive three-bit X-error decoder; noiseless syndrome only."""
import itertools
import json
import math


ERRORS = list(itertools.product((0, 1), repeat=3))


def syndrome(e):
    return e[0] ^ e[1], e[1] ^ e[2]


def probability(e, rates):
    return math.prod(p if bit else 1 - p for bit, p in zip(e, rates))


def decoder(rates, weighted=True):
    assert len(rates) == 3 and all(0 < p < 1 for p in rates)
    result = {}
    for s in itertools.product((0, 1), repeat=2):
        candidates = [e for e in ERRORS if syndrome(e) == s]
        result[s] = (max(candidates, key=lambda e: probability(e, rates)) if weighted
                     else min(candidates, key=sum))
    return result


def failure(rates, table):
    # Same syndrome leaves residual 000 or logical X=111 for this X-only code.
    total = 0.0
    for e in ERRORS:
        residual = tuple(a ^ b for a, b in zip(e, table[syndrome(e)]))
        assert residual in ((0, 0, 0), (1, 1, 1))
        if residual == (1, 1, 1):
            total += probability(e, rates)
    return total


def main():
    rates = (.01, .2, .2)
    weighted, unweighted = decoder(rates), decoder(rates, False)
    assert weighted[(1, 0)] == (0, 1, 1)
    assert unweighted[(1, 0)] == (1, 0, 0)
    assert abs(sum(probability(e, rates) for e in ERRORS) - 1) < 1e-12
    assert abs(failure(rates, weighted) - .01) < 1e-12
    assert abs(failure(rates, unweighted) - .0432) < 1e-12
    equal = (.1,) * 3
    assert abs(failure(equal, decoder(equal)) - (3 * .1**2 * .9 + .1**3)) < 1e-12
    print(json.dumps({'weighted_failure': failure(rates, weighted),
                      'unweighted_failure': failure(rates, unweighted),
                      'syndrome_10_candidates': {''.join(map(str, e)): probability(e, rates)
                          for e in ERRORS if syndrome(e) == (1, 0)}}, indent=2))


if __name__ == '__main__':
    main()
