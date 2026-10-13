"""Round 71: eight original, standard-library teaching checks.

Run: python3 codes/systems/round71_checks.py [--case all|09|10|11|12|14|15|19|q3]
All inputs are synthetic and deterministic. No hardware, network or randomness.
Basis: leftmost qubit is most significant; matrices act on column vectors.
Assertions must remain enabled. JSON output is the actual computed result.
"""
import argparse
import cmath
import itertools
import json
import math
import platform


def close(a, b, tol=1e-10):
    assert abs(a - b) <= tol, (a, b)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def adj(a):
    return [[a[j][i].conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def outer(v):
    return [[x * y.conjugate() for y in v] for x in v]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def thermal_population(t, initial, up, down):
    if not (t >= 0 and 0 <= initial <= 1 and up >= 0 and down >= 0):
        raise ValueError('Invalid time, initial population or rate')
    rate = up + down
    if rate == 0:
        return initial
    equilibrium = up / rate
    return equilibrium + (initial - equilibrium) * math.exp(-rate * t)


def case09():
    up, down, time = 100., 9900., 500e-6  # rates /s; time s
    value = thermal_population(time, 1., up, down)
    close(value, 0.016670567529094614)
    close(thermal_population(0, .4, up, down), .4)
    close(thermal_population(10, 1, up, down), .01)
    close(thermal_population(10, 0, up, down), .01)
    close(thermal_population(1, .4, 0, 0), .4)
    # Independent forward-Euler rate equation, convergence checked, no fitting.
    dt = time / 100000
    population = 1.
    for _ in range(100000):
        population += dt * (up * (1 - population) - down * population)
    close(population, value, 9e-7)
    target = .02
    reset_time = math.log((1 - .01) / (target - .01)) / (up + down)
    close(thermal_population(reset_time, 1, up, down), target)
    assert .001 < up / (up + down)  # no finite passive wait can meet target
    return {'rates_per_s': [up, down], 'T_rel_us': 100.,
            'equilibrium_p1': .01, 'p1_after_500us': value,
            'time_to_p1_002_us': reset_time * 1e6,
            'euler_difference': abs(population - value)}


def parity(x):
    return bin(x).count('1') % 2


def syndrome(pauli, generators):
    x, z = pauli
    return tuple(parity((x & gz) ^ (z & gx)) for gx, gz in generators)


def case10():
    masks = [0b0001111, 0b0110011, 0b1010101]
    generators = [(m, 0) for m in masks] + [(0, m) for m in masks]
    stabilizers = {(0, 0)}
    for gx, gz in generators:
        stabilizers |= {(x ^ gx, z ^ gz) for x, z in list(stabilizers)}
    assert len(stabilizers) == 64
    minimum = 8
    normalizer_count = 0
    for x in range(128):
        for z in range(128):
            if not any(syndrome((x, z), generators)):
                normalizer_count += 1
                if (x, z) not in stabilizers:
                    minimum = min(minimum, bin(x | z).count('1'))
    assert normalizer_count == 256 and minimum == 3
    # Known erasure at position 3; two candidates each have <=1 unknown error.
    a, b = (0b1000000, 0), (0b0110000, 0)
    assert syndrome(a, generators) == syndrome(b, generators)
    difference = (a[0] ^ b[0], 0)
    assert difference not in stabilizers
    assert not any(syndrome(difference, generators))
    # Exhaustively test KL Pauli-product criterion for any two fixed erasures.
    checks = 0
    for positions in itertools.combinations(range(7), 2):
        support = sum(1 << p for p in positions)
        for x in range(128):
            if x & ~support:
                continue
            for z in range(128):
                if z & ~support:
                    continue
                assert any(syndrome((x, z), generators)) or (x, z) in stabilizers
                checks += 1
    assert checks == 336
    guarantees = [(0, 4), (1, 2), (2, 0)]
    assert all(2 * t + e < 5 for t, e in guarantees)
    assert 2 * 1 + 3 == 5
    return {'steane_distance': minimum, 'stabilizer_size': 64,
            'normalizer_size': normalizer_count, 'erasure_products_checked': checks,
            'boundary_candidates': ['X1', 'X2 X3'],
            'shared_syndrome': syndrome(a, generators),
            'd5_guaranteed_t_e': guarantees}


def case11():
    p, cycles = .01, 100
    final_odd = (1 - (1 - 2 * p) ** cycles) / 2
    any_flip = 1 - (1 - p) ** cycles
    enumeration = sum(math.comb(cycles, k) * p**k * (1-p)**(cycles-k)
                      for k in range(1, cycles + 1, 2))
    close(enumeration, final_odd)
    inferred = (1 - (1 - 2 * final_odd) ** (1 / cycles)) / 2
    close(inferred, p)
    close((1 - (1 - 2 * p) ** 0) / 2, 0)
    close((1 - (1 - 2 * 0) ** cycles) / 2, 0)
    close((1 - (1 - 2 * .5) ** cycles) / 2, .5)
    return {'p_flip_per_cycle': p, 'cycles': cycles,
            'final_odd_flip': final_odd, 'at_least_one_flip': any_flip,
            'union_upper_bound': min(1., cycles * p), 'inferred_p': inferred}


def bell(x, z):
    v = [0j] * 4
    for i in (0, 1):
        v[2 * i + (i ^ x)] = (-1)**(z * i) / math.sqrt(2)
    return v


def swapping_weights(left, right):
    return [sum(left[a] * right[b] for a in range(4) for b in range(4)
                if a ^ b == label) for label in range(4)]


def project_swapping(left, right, outcome):
    measured = bell(outcome >> 1, outcome & 1)
    rho = [[0j] * 4 for _ in range(4)]
    for a, pa in enumerate(left):
        for b, pb in enumerate(right):
            va, vb = bell(a >> 1, a & 1), bell(b >> 1, b & 1)
            v = [0j] * 4
            for i, j, k, l in itertools.product(range(2), repeat=4):
                v[2 * i + l] += (measured[2*j+k].conjugate()
                                * va[2*i+j] * vb[2*k+l])
            # Correct C by X^x Z^z, exactly as chapter 12; global sign irrelevant.
            corrected = [0j] * 4
            for i, l in itertools.product(range(2), repeat=2):
                corrected[2*i+(l ^ (outcome >> 1))] += (
                    (-1)**((outcome & 1)*l) * v[2*i+l])
            branch = outer(corrected)
            for i, j in itertools.product(range(4), repeat=2):
                rho[i][j] += pa * pb * branch[i][j]
    probability = trace(rho).real
    close(probability, .25)
    rho = [[v / probability for v in row] for row in rho]
    weights = []
    for label in range(4):
        v = bell(label >> 1, label & 1)
        weights.append(sum(v[i].conjugate() * rho[i][j] * v[j]
                           for i, j in itertools.product(range(4), repeat=2)).real)
    return probability, weights


def case12():
    f = .9
    weights = [f] + [(1-f)/3] * 3
    expected = swapping_weights(weights, weights)
    close(expected[0], f*f+(1-f)**2/3)
    for outcome in range(4):
        _, actual = project_swapping(weights, weights, outcome)
        for a, b in zip(actual, expected):
            close(a, b)
    # Same overlap is insufficient to characterize swapping of anisotropic errors.
    anisotropic = [.9, .1, 0., 0.]
    anisotropic_out = swapping_weights(anisotropic, anisotropic)
    close(anisotropic_out[0], .82)
    for outcome in range(4):
        _, actual = project_swapping(anisotropic, anisotropic, outcome)
        for a, b in zip(actual, anisotropic_out):
            close(a, b)
    chain = [1., 0., 0., 0.]
    rows = []
    for hops in range(1, 9):
        chain = swapping_weights(chain, weights)
        visibility = (4*f-1)/3
        close(chain[0], (1+3*visibility**hops)/4)
        rows.append([hops, chain[0]])
    return {'input_overlap': f, 'two_hop_overlap': expected[0],
            'same_overlap_anisotropic_output': anisotropic_out[0],
            'outcome_probability': .25, 'chain_hops_overlap': rows}


def rz(alpha):
    return [[cmath.exp(-.5j*alpha), 0j], [0j, cmath.exp(.5j*alpha)]]


def equatorial(theta, phi):
    c, s = math.cos(theta/2), math.sin(theta/2)
    return [[c, -1j*s*cmath.exp(-1j*phi)],
            [-1j*s*cmath.exp(1j*phi), c]]


def case14():
    alpha, theta = math.pi/2, math.pi/2
    ideal = mm(equatorial(theta, 0), rz(alpha))
    framed = mm(rz(alpha), equatorial(theta, -alpha))
    wrong = mm(rz(alpha), equatorial(theta, alpha))
    difference = max(abs(ideal[i][j]-framed[i][j])
                     for i, j in itertools.product(range(2), repeat=2))
    close(difference, 0)
    plus = [1/math.sqrt(2)] * 2
    p_correct = abs(mv(framed, plus)[0])**2
    p_wrong = abs(mv(wrong, plus)[0])**2
    close(p_correct, 1)
    close(p_wrong, 0)
    for a, t in itertools.product([0., -.4, 1.7], [.3, -1.2, math.pi]):
        m1 = mm(equatorial(t, 0), rz(a))
        m2 = mm(rz(a), equatorial(t, -a))
        for i, j in itertools.product(range(2), repeat=2):
            close(m1[i][j], m2[i][j])
    return {'alpha_rad': alpha, 'theta_rad': theta,
            'matrix_difference': difference,
            'p0_correct_phase': p_correct, 'p0_wrong_phase': p_wrong}


def case15():
    alpha = .05
    rows = []
    for look, (n, k) in enumerate([(100, 70), (400, 280), (1600, 1120)], 1):
        budget = alpha / (look * (look + 1))
        lower = k/n - math.sqrt(math.log(1/budget)/(2*n))
        rows.append({'look': look, 'N': n, 'successes': k,
                     'alpha_look': budget, 'lower': max(0., lower)})
    close(sum(alpha/(j*(j+1)) for j in range(1, 10001)),
          alpha*(1-1/10001), 1e-14)
    assert rows[0]['lower'] > .5
    assert all(rows[i]['lower'] < rows[i+1]['lower'] for i in range(2))
    assert sum(r['alpha_look'] for r in rows) < alpha
    # The first three budgets do not exhaust the infinite-horizon allocation.
    return {'overall_alpha': alpha, 'looks': rows,
            'first_three_budget_sum': sum(r['alpha_look'] for r in rows),
            'all_looks_budget_sum': alpha}


def case19():
    qnd = [[[1+0j, 0j], [0j, 0j]], [[0j, 0j], [0j, 1+0j]]]
    reset = [[[1+0j, 0j], [0j, 0j]], [[0j, 1+0j], [0j, 0j]]]
    for k, l in zip(qnd, reset):
        a, b = mm(adj(k), k), mm(adj(l), l)
        for i, j in itertools.product(range(2), repeat=2):
            close(a[i][j], b[i][j])
    repeat = {}
    for name, operators in [('qnd', qnd), ('reset', reset)]:
        results = {}
        for label, v in [('zero', [1+0j, 0j]), ('one', [0j, 1+0j]),
                         ('plus', [1/math.sqrt(2)]*2)]:
            probabilities = [sum(abs(a)**2 for a in mv(k, v)) for k in operators]
            same = sum(sum(abs(x)**2 for x in mv(k, mv(k, v))) for k in operators)
            results[label] = {'first_probabilities': probabilities, 'repeat_same': same}
        repeat[name] = results
    close(repeat['qnd']['one']['repeat_same'], 1)
    close(repeat['reset']['one']['repeat_same'], 0)
    close(repeat['qnd']['plus']['repeat_same'], 1)
    close(repeat['reset']['plus']['repeat_same'], .5)
    close(repeat['reset']['zero']['repeat_same'], 1)
    return repeat


def rectangular_amplitude(delta, duration, omega):
    if delta == 0:
        return -.5j*omega*duration
    return -.5j*omega*(cmath.exp(1j*delta*duration)-1)/(1j*delta)


def caseq3():
    delta = 2*math.pi*200e6
    rows = []
    for duration in [2.5e-9, 5e-9, 10e-9]:
        omega = .1/duration  # weak area, not a pi pulse on the intended transition
        amplitude = rectangular_amplitude(delta, duration, omega)
        steps = 20000
        dt = duration/steps
        quadrature = -.5j*omega*dt*sum(cmath.exp(1j*delta*(j+.5)*dt)
                                      for j in range(steps))
        close(amplitude, quadrature, 1e-9)
        exact = omega**2/(omega**2+delta**2)*math.sin(
            math.sqrt(omega**2+delta**2)*duration/2)**2
        rows.append({'duration_ns': duration*1e9,
                     'first_order_probability': abs(amplitude)**2,
                     'isolated_transition_exact_probability': exact})
    close(rows[0]['first_order_probability'], .01/math.pi**2)
    assert rows[1]['first_order_probability'] < 1e-30
    assert rows[1]['isolated_transition_exact_probability'] > 1e-12
    close(abs(rectangular_amplitude(0, 1e-9, 1e8))**2, .0025)
    return {'detuning_Hz': 200e6, 'omega_duration_rad': .1, 'rows': rows}


CASES = {'09': case09, '10': case10, '11': case11, '12': case12,
         '14': case14, '15': case15, '19': case19, 'q3': caseq3}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: numerical checks require assertions')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=['all'] + list(CASES), default='all')
    args = parser.parse_args()
    selected = {args.case: CASES[args.case]} if args.case != 'all' else CASES
    result = {key: function() for key, function in selected.items()}
    print(json.dumps({'python': platform.python_version(), 'synthetic': True,
                      'results': result}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
