#!/usr/bin/env python3
"""Small, dependency-free reference calculations; not production quantum algorithms.

Run: python3 codes/algorithms/experiments.py [all|06|07|08|16|17|18]
All statevector indices use the displayed binary integer (most significant bit first).
Deterministic calculations are checked against independent analytic identities.
"""
import cmath
import json
import math
import sys

TOL = 1e-10


def close(a, b, tol=TOL):
    assert abs(a - b) < tol, (a, b)


def matmul(a, b):
    assert len(a[0]) == len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def dagger(a):
    return [[complex(a[j][i]).conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def identity(n):
    return [[float(i == j) for j in range(n)] for i in range(n)]


def matclose(a, b):
    assert len(a) == len(b) and len(a[0]) == len(b[0])
    for ra, rb in zip(a, b):
        for x, y in zip(ra, rb):
            close(x, y)


def qpe(phi, bits):
    """DFT sum, rather than the closed-form sine quotient (safe on-grid)."""
    assert bits >= 1
    m = 2**bits
    probs = [abs(sum(cmath.exp(2j * math.pi * k * (phi - y/m))
                     for k in range(m))/m)**2 for y in range(m)]
    close(sum(probs), 1)
    return probs


def chapter06():
    p = qpe(1/3, 2)
    expected = [1/16, (6+3*math.sqrt(3))/16, 3/16,
                (6-3*math.sqrt(3))/16]
    for x, y in zip(p, expected):
        close(x, y)
    boundary = qpe(1 - 1/64, 4)
    assert max(range(16), key=boundary.__getitem__) == 0
    distance = min(abs(1-1/64), abs(1-1/64-1))
    close(distance, 1/64)
    for bits in (1, 2, 3):
        for y in range(2**bits):
            close(qpe(y/2**bits, bits)[y], 1)
    return {'phi_1_over_3': p, 'near_one_peak': 0,
            'near_one_peak_probability': boundary[0],
            'circular_error': distance, 'controlled_U_calls_t4': 15}


def grover(n, marked, rounds):
    assert 0 < len(marked) < n and all(0 <= k < n for k in marked)
    state = [1/math.sqrt(n)] * n
    out = []
    theta = math.asin(math.sqrt(len(marked)/n))
    for k in range(rounds + 1):
        p = sum(abs(state[j])**2 for j in marked)
        close(p, math.sin((2*k+1)*theta)**2)
        close(sum(abs(a)**2 for a in state), 1)
        out.append(p)
        state = [-a if j in marked else a for j, a in enumerate(state)]
        mean = sum(state)/n
        state = [2*mean-a for a in state]
    return out


def chapter07():
    single = grover(16, {5}, 4)
    multi = grover(16, {0, 3, 8, 15}, 4)
    close(multi[1], 1)
    close(multi[3], 1/4)
    # A known lower bound p >= 1/4 for each independently restarted attempt.
    repetitions = math.ceil(math.log(0.01)/math.log(0.75))
    assert 0.75**repetitions <= 0.01 < 0.75**(repetitions-1)
    return {'single_target': single, 'four_targets': multi,
            'restarts_for_99_percent_at_p_quarter': repetitions}


def qaoa_path(gamma, beta):
    """Exact three-qubit p=1 simulation: phase cost then each X mixer."""
    costs = [((x >> 2) & 1 != (x >> 1) & 1) +
             ((x >> 1) & 1 != x & 1) for x in range(8)]
    state = [cmath.exp(-1j*gamma*c)/math.sqrt(8) for c in costs]
    for bit in range(3):
        state = [math.cos(beta)*state[x] -
                 1j*math.sin(beta)*state[x ^ (1 << bit)] for x in range(8)]
    probs = [abs(a)**2 for a in state]
    close(sum(probs), 1)
    expectation = sum(p*c for p, c in zip(probs, costs))
    analytic = 1 + 0.5*math.sin(4*beta)*math.sin(gamma)*(1+math.cos(gamma))
    close(expectation, analytic)
    return expectation, sum(probs[x] for x in (2, 5)), probs


def chapter08():
    theta = math.pi + math.atan2(0.2, 0.7)
    e = 0.7*math.cos(theta)+0.2*math.sin(theta)
    close(e, -math.sqrt(0.53))
    shift = ((0.7*math.cos(theta+math.pi/2)+0.2*math.sin(theta+math.pi/2))-
             (0.7*math.cos(theta-math.pi/2)+0.2*math.sin(theta-math.pi/2)))/2
    close(shift, 0)
    epsilon, delta = 0.02, 0.05
    # A Hoeffding bound on the weighted sum, using width 2*c_j / S_j.
    total = math.ceil(2*0.9**2*math.log(2/delta)/epsilon**2)
    while True:
        sz = round(total*7/9)
        sx = total-sz
        halfwidth = math.sqrt(2*(0.49/sz+0.04/sx)*math.log(2/delta))
        if halfwidth <= epsilon:
            break
        total += 1
    for gamma in (0, math.pi/3, 0.6, -0.9):
        for beta in (0, math.pi/8, 0.3):
            qaoa_path(gamma, beta)
    expected, optimal_p, probs = qaoa_path(math.pi/3, math.pi/8)
    close(expected, 1+3*math.sqrt(3)/8)
    close(optimal_p, (11+6*math.sqrt(3))/32)
    return {'vqe_exact_minimum': e, 'hoeffding_total_shots': total,
            'shots_Z': sz, 'shots_X': sx, 'guaranteed_halfwidth': halfwidth,
            'qaoa_mean_cut': expected, 'qaoa_optimal_cut_probability': optimal_p,
            'qaoa_probabilities_000_to_111': probs}


def chapter16():
    # Non-Hermitian A has A^2=0 but nonzero singular-value square.
    a = [[0, 0.5], [0, 0]]
    matclose(matmul(a, a), [[0, 0], [0, 0]])
    ata = matmul(dagger(a), a)
    matclose(ata, [[0, 0], [0, 0.25]])
    rows = []
    for x in (-1, -0.5, 0, 0.5, 1):
        w = [[x, 1j*math.sqrt(1-x*x)], [1j*math.sqrt(1-x*x), x]]
        matclose(matmul(dagger(w), w), identity(2))
        w2 = matmul(w, w)
        close(w2[0][0], 2*x*x-1)
        rows.append([x, w2[0][0].real, abs(w2[0][0])**2])
    return {'A_squared': [[0, 0], [0, 0]],
            'right_singular_square': [[z.real for z in row] for row in ata],
            'x_T2_probability': rows}


def chapter17():
    # MBQC conditional vectors, including complex input and nonzero angle.
    a, b = 1/math.sqrt(3), 1j*math.sqrt(2/3)
    alpha = math.pi/4
    branches = []
    target = [(a+cmath.exp(-1j*alpha)*b)/math.sqrt(2),
              (a-cmath.exp(-1j*alpha)*b)/math.sqrt(2)]
    for m in (0, 1):
        # Conditional unnormalised state after projecting measured qubit.
        v = [(a+(-1)**m*cmath.exp(-1j*alpha)*b)/2,
             (a-(-1)**m*cmath.exp(-1j*alpha)*b)/2]
        p = sum(abs(z)**2 for z in v)
        close(p, 0.5)
        v = [z/math.sqrt(p) for z in v]
        if m:
            v.reverse()  # apply known X correction
        for z, t in zip(v, target):
            close(z, t)
        branches.append(p)
    # One-sided Hoeffding: independently observed 20 successes / 100 trials.
    phat, trials, confidence_delta = 0.2, 100, 0.05
    lower = max(0, phat-math.sqrt(math.log(1/confidence_delta)/(2*trials)))
    required = math.ceil(math.log(0.01)/math.log1p(-lower))
    assert (1-lower)**required <= 0.01 < (1-lower)**(required-1)
    return {'mbqc_branch_probabilities': branches, 'successes': 20,
            'trials': trials, 'one_sided_95_percent_lower_p': lower,
            'repetitions_for_conditional_99_percent': required,
            'anneal_readout_reset_ms': required*0.120}


def binary_entropy(x):
    assert 0 <= x <= 1
    return -sum(p*math.log2(p) for p in (x, 1-x) if p)


def chapter18():
    # Explicit erasure output probabilities for diagonal input diag(q,1-q).
    rows = []
    for erasure in (0, 0.25, 0.5, 0.75, 1):
        candidates = []
        for j in range(101):
            q = j/100
            bob = [(1-erasure)*q, (1-erasure)*(1-q), erasure]
            env = [erasure*q, erasure*(1-q), 1-erasure]
            entropy = lambda v: -sum(p*math.log2(p) for p in v if p)
            ic = entropy(bob)-entropy(env)
            close(ic, (1-2*erasure)*binary_entropy(q))
            candidates.append(ic)
        maximum = max(candidates)
        close(maximum, max(0, 1-2*erasure))
        rows.append([erasure, 1-erasure, maximum, maximum, 2*(1-erasure)])
    # Entropy computation is a single-letter check, not an independent
    # proof of regularized quantum/private capacity; chapter gives the theorem.
    return {'columns': ['erasure', 'C', 'Q_theorem', 'P_theorem', 'CE'],
            'capacity_rows': rows, 'negative_Ic_at_e075_q05': -0.5}


def main():
    experiments = {'06': chapter06, '07': chapter07, '08': chapter08,
                   '16': chapter16, '17': chapter17, '18': chapter18}
    selected = sys.argv[1] if len(sys.argv) == 2 else 'all'
    if len(sys.argv) > 2 or selected not in {*experiments, 'all'}:
        raise SystemExit('Usage: experiments.py [all|06|07|08|16|17|18]')
    result = {key: fun() for key, fun in experiments.items()
              if selected in ('all', key)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
