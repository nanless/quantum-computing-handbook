#!/usr/bin/env python3
"""Fixed synthetic examples for P15-D--G. Python 3.9+, standard library only.

No sampling seed: enumerate small distributions exactly. These examples do not
execute vendor files, use cloud accounts, or represent new hardware experiments.
"""
import json
import math
import pathlib


def zero_failure_upper(n, alpha=0.05):
    if not isinstance(n, int) or n < 1 or not 0 < alpha < 1:
        raise ValueError('positive integer n and 0 < alpha < 1 required')
    return -math.expm1(math.log(alpha) / n)


def binomial_cdf(k, n, p):
    """Direct finite sum: intended for the small n=20 coverage check only."""
    return sum(math.comb(n, j) * p**j * (1-p)**(n-j)
               for j in range(k+1))


def exact_upper(k, n, alpha=0.05):
    if not (isinstance(k, int) and isinstance(n, int) and 0 <= k <= n
            and n > 0 and 0 < alpha < 1):
        raise ValueError('invalid binomial input')
    if k == n:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(70):
        mid = (lo + hi) / 2
        if binomial_cdf(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: assertions verify the examples')
    rows = [dict(method='A', attempts=1000, accepted=800, correct=720),
            dict(method='B', attempts=1000, accepted=250, correct=240)]
    for r in rows:
        assert 0 <= r['correct'] <= r['accepted'] <= r['attempts']
        r.update(acceptance=r['accepted']/r['attempts'],
                 conditional=r['correct']/r['accepted'],
                 joint=r['correct']/r['attempts'])
        assert math.isclose(r['acceptance'] * r['conditional'], r['joint'])
    assert rows[1]['conditional'] > rows[0]['conditional']
    assert rows[1]['joint'] < rows[0]['joint']

    alpha, target = 0.05, 0.001
    n_required = math.ceil(math.log(alpha)/math.log1p(-target))
    assert n_required == 2995
    assert zero_failure_upper(n_required) <= target
    assert zero_failure_upper(n_required-1) > target
    upper = zero_failure_upper(1000)
    assert math.isclose((1-upper)**1000, alpha, rel_tol=1e-12)
    assert math.isclose(exact_upper(0, 20), zero_failure_upper(20))
    limits = [exact_upper(k, 20) for k in range(21)]
    # Independent coverage enumeration, not a rerun of the bisection equation.
    coverages = []
    for i in range(201):
        p = i / 200
        coverage = sum(math.comb(20, k)*p**k*(1-p)**(20-k)
                       for k in range(21) if limits[k] >= p-1e-14)
        assert coverage >= 0.95-1e-12
        coverages.append(coverage)

    # Equal wall-clock budget C=9000 cost units, shot costs 1 and 9.
    weights, costs = [1.5, -0.5], [1, 9]
    allocations = {'equal_shots': [900, 900], 'time_optimal': [4500, 500]}
    allocation_results = {}
    for name, ns in allocations.items():
        cost = sum(c*n for c, n in zip(costs, ns))
        variance = sum(a*a/n for a, n in zip(weights, ns))
        assert cost == 9000
        allocation_results[name] = dict(shots=ns, cost=cost, variance_bound=variance)
    lower_bound = sum(abs(a)*math.sqrt(c) for a, c in zip(weights, costs))**2/9000
    assert math.isclose(allocation_results['time_optimal']['variance_bound'], lower_bound)

    # QPD estimator Z = gamma * sign(a_j) * X_j; X_j is +/-1.
    means, gamma = [0.4, -0.2], sum(abs(a) for a in weights)
    outcomes = []
    for a, mean in zip(weights, means):
        for x in [-1, 1]:
            probability = abs(a)/gamma*(1+x*mean)/2
            outcomes.append((probability, math.copysign(gamma, a)*x))
    assert math.isclose(sum(p for p, _ in outcomes), 1)
    expectation = sum(p*z for p, z in outcomes)
    variance = sum(p*(z-expectation)**2 for p, z in outcomes)
    assert math.isclose(expectation, sum(a*m for a, m in zip(weights, means)))
    assert math.isclose(expectation, 0.7)
    assert math.isclose(variance, 3.51)
    assert math.isclose(variance, gamma**2-expectation**2)
    report = {
        'data_kind': 'fixed synthetic counts and exact finite distributions',
        'seed': None,
        'postselection': rows,
        'zero_failure': {'n': 1000, 'alpha': alpha, 'upper': upper,
                         'target': target, 'required_n': n_required,
                         'coverage_check_n': 20, 'grid_points': len(coverages),
                         'minimum_grid_coverage': min(coverages)},
        'wall_clock_allocation': allocation_results,
        'qpd': {'weights': weights, 'conditional_means': means,
                'gamma': gamma, 'expectation': expectation, 'variance': variance,
                'independent_CNOT_cut_bounds': {str(k): 9**k for k in range(5)}}}
    dest = pathlib.Path(__file__).with_name('research-results.json')
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
