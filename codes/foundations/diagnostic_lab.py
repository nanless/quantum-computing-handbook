#!/usr/bin/env python3
"""Eleven fixed-input diagnostics; all inputs are synthetic, no hardware/network.

Uses the adjacent, book-authored foundations_lab.py matrix helpers. Python 3 stdlib.
Tensor basis: left factor is most significant. Angles: radians; times: seconds.
"""
import argparse
import json
import math
from pathlib import Path
from foundations_lab import (
    I, X, Y, Z, H, ZERO, PLUS, close, dagger, mm, mv, inner, outer,
    add, scale, trace, kron, tensor, matrix_close, eig2, state_check,
    kraus_apply, rotation,
)


def case00():
    # Enumerate all independent ten-block histories rather than infer independence.
    blocks, repeats = 10, 100
    values = [bin(mask).count('1') / blocks for mask in range(2**blocks)]
    mean = sum(values) / len(values)
    variance = sum((v - mean)**2 for v in values) / len(values)
    close(mean, .5)
    close(variance, .25 / blocks)
    return dict(blocks=blocks, repeats_per_block=repeats, recorded_rows=blocks*repeats,
                enumerated_histories=len(values), mean=mean,
                true_frequency_sd=math.sqrt(variance),
                wrongly_assumed_iid_sd=math.sqrt(.25/(blocks*repeats)),
                fixed_block_sample=[0, 1, 1, 0, 1, 0, 0, 1, 0, 1])


def case01():
    # Both columns have norm one, but are not orthogonal.
    a = [[1, 1], [0, 0]]
    input_norms = [inner(mv(a, v), mv(a, v)).real for v in [ZERO, [0, 1]]]
    plus_norm = inner(mv(a, PLUS), mv(a, PLUS)).real
    minus = [PLUS[0], -PLUS[1]]
    minus_norm = inner(mv(a, minus), mv(a, minus)).real
    close(input_norms[0], 1)
    close(input_norms[1], 1)
    close(plus_norm, 2)
    close(minus_norm, 0)
    matrix_close(mm(dagger(a), a), [[1, 1], [1, 1]])
    return dict(basis_output_norms=input_norms, plus_output_norm_squared=plus_norm,
                minus_output_norm_squared=minus_norm, a_dagger_a=[[1, 1], [1, 1]])


def case02():
    counts = {'X': [9, 1], 'Y': [9, 1], 'Z': [5, 5]}
    r = [(p-m)/(p+m) for p, m in counts.values()]
    rho = scale(add(I, scale(X, r[0]), scale(Y, r[1]), scale(Z, r[2])), .5)
    eigenvalues = eig2(rho)
    length = math.sqrt(sum(x*x for x in r))
    physical_r = [x/max(1, length) for x in r]
    physical_rho = scale(add(I, scale(X, physical_r[0]), scale(Y, physical_r[1])), .5)
    assert eigenvalues[0] < 0
    state_check(physical_rho)
    close(eigenvalues[0], (1-math.sqrt(1.28))/2)
    return dict(synthetic_counts_plus_minus=counts, bloch=r, bloch_length=length,
                raw_eigenvalues=eigenvalues, euclidean_projected_bloch=physical_r,
                projected_eigenvalues=eig2(physical_rho),
                method='Euclidean Bloch-ball projection, not claimed to be binomial MLE')


def case03():
    v = [1/math.sqrt(2), 0, 0, 1j/math.sqrt(2)]
    c = {name: inner(v, mv(kron(a, b), v)).real
         for name, a, b in [('ZZ', Z, Z), ('XX', X, X), ('XY', X, Y)]}
    for name, expected in [('ZZ', 1), ('XX', 0), ('XY', 1)]:
        close(c[name], expected)
    fixed = mv(kron(I, [[1, 0], [0, -1j]]), v)
    close(inner(fixed, mv(kron(X, X), fixed)), 1)
    return dict(correlations=c, original_witness=c['ZZ']+c['XX'],
                rotated_witness=c['ZZ']+c['XY'])


def case04():
    v = tensor(PLUS, ZERO)
    ci = [[int(i == j) for j in range(4)] for i in range(4)]
    cminus = [[(1 if i < 2 else -1)*int(i == j) for j in range(4)] for i in range(4)]
    out_i = mv(kron(H, I), mv(ci, v))
    out_minus = mv(kron(H, I), mv(cminus, v))
    p_i = sum(abs(out_i[i])**2 for i in [2, 3])
    p_minus = sum(abs(out_minus[i])**2 for i in [2, 3])
    close(p_i, 0)
    close(p_minus, 1)
    return dict(control_one_after_h_with_CI=p_i, control_one_after_h_with_CminusI=p_minus)


def gad(gamma, excited):
    assert 0 <= gamma <= 1 and 0 <= excited <= 1
    q, u, d = math.sqrt(1-gamma), math.sqrt(excited), math.sqrt(1-excited)
    return [scale([[1, 0], [0, q]], d), scale([[0, math.sqrt(gamma)], [0, 0]], d),
            scale([[q, 0], [0, 1]], u), scale([[0, 0], [math.sqrt(gamma), 0]], u)]


def case05():
    gamma, excited = .36, .1
    ks = gad(gamma, excited)
    eq = [[1-excited, 0], [0, excited]]
    matrix_close(kraus_apply(ks, eq), eq)
    outputs = {name: kraus_apply(ks, outer(v))
               for name, v in [('zero', ZERO), ('one', [0, 1]), ('plus', PLUS)]}
    close(outputs['zero'][1][1], .036)
    close(outputs['one'][1][1], .676)
    close(outputs['plus'][1][1], .356)
    close(outputs['plus'][0][1], .4)
    for g in [0, .36, 1]:
        for e in [0, .1, 1]:
            out = kraus_apply(gad(g, e), outer(PLUS))
            close(out[1][1], (1-g)*.5+g*e)
            close(out[0][1], math.sqrt(1-g)*.5)
    return dict(gamma=gamma, equilibrium_excited_population=excited,
                output_excited_populations={k: a[1][1].real for k, a in outputs.items()},
                plus_coherence=outputs['plus'][0][1].real, fixed_point=eq,
                tested_parameter_pairs=9)


def case13():
    states = [ZERO, [.6, .8]]
    ks = [[[.5, 0], [0, 1]], [[math.sqrt(.75), 0], [0, 0]]]
    matrix_close(add(*(mm(dagger(k), k) for k in ks)), I)
    branch_vectors = [[mv(k, v) for v in states] for k in ks]
    success_prob = [inner(v, v).real for v in branch_vectors[0]]
    normalized = [[z/math.sqrt(p) for z in v]
                  for v, p in zip(branch_vectors[0], success_prob)]
    conditional_t = math.sqrt(1-abs(inner(*normalized))**2)
    initial_t = math.sqrt(1-abs(inner(*states))**2)
    # Retain both flags. Difference is block diagonal; sum block trace norms.
    flagged_t = sum(sum(abs(x) for x in eig2(add(outer(v[0]), scale(outer(v[1]), -1))))
                    for v in branch_vectors) / 2
    prior_given_success = success_prob[0]/sum(success_prob)
    weighted_delta = add(scale(outer(normalized[0]), prior_given_success),
                         scale(outer(normalized[1]), -(1-prior_given_success)))
    conditional_guess = (1+sum(abs(x) for x in eig2(weighted_delta)))/2
    assert conditional_t > initial_t and flagged_t <= initial_t+1e-10
    close(success_prob[0], .25)
    close(success_prob[1], .73)
    close(prior_given_success, 25/98)
    return dict(initial_equal_prior_trace_distance=initial_t, success_probabilities=success_prob,
                mean_success_probability=sum(success_prob)/2,
                conditional_trace_distance=conditional_t,
                prior_zero_given_success=prior_given_success,
                conditional_optimal_guess=conditional_guess, all_flags_trace_distance=flagged_t)


def caseq1():
    # Same visibility, different purity: unequal paths vs partial path recording.
    rows = []
    for p, gamma in [(.9, 1), (.5, .6)]:
        off = math.sqrt(p*(1-p))*gamma
        rho = [[p, off], [off, 1-p]]
        state_check(rho)
        maxima = inner(PLUS, mv(rho, PLUS)).real
        minima = inner(PLUS, mv(mm(mm(Z, rho), Z), PLUS)).real
        visibility = (maxima-minima)/(maxima+minima)
        purity = trace(mm(rho, rho)).real
        close(visibility, .6)
        rows.append(dict(path_zero=p, record_overlap=gamma, p0_max=maxima,
                         p0_min=minima, visibility=visibility, purity=purity))
    close(rows[0]['purity'], 1)
    close(rows[1]['purity'], .68)
    return rows


def caseq2():
    v = [1/math.sqrt(2), 1/math.sqrt(2), 0]
    rho = outer(v)
    p = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
    luders = mm(mm(p, rho), p)
    refined = [[rho[i][i] if i == j else 0 for j in range(3)] for i in range(3)]
    repeat_luders = inner(v, mv(luders, v)).real
    repeat_refined = inner(v, mv(refined, v)).real
    close(trace(luders), 1)
    close(repeat_luders, 1)
    close(repeat_refined, .5)
    return dict(energy_zero_probability=1, return_probability_luders=repeat_luders,
                return_probability_refine_then_forget=repeat_refined)


def caseq3():
    omega, delta, t = 2*math.pi*10e6, 2*math.pi*6e6, 50e-9
    def prob(d):
        f = math.hypot(omega, d)
        return omega**2/f**2 * math.sin(f*t/2)**2
    plus, minus = prob(delta), prob(-delta)
    close(plus, minus)
    # New, explicit Ramsey model H_eff = hbar*delta*Z/2; not ZE of Q3 drive.
    tau = 1/(4*6e6)
    y = [inner(mv(rotation(Z, d*tau), PLUS),
               mv(Y, mv(rotation(Z, d*tau), PLUS))).real for d in [delta, -delta]]
    close(y[0], 1)
    close(y[1], -1)
    return dict(rabi_time_seconds=t, population_plus_detuning=plus,
                population_minus_detuning=minus, ramsey_time_seconds=tau,
                ramsey_Y_expectations=y, ramsey_convention='H_eff = hbar*delta*Z/2')


def caseq4():
    d = 4
    a = [[math.sqrt(j) if j == i+1 else 0 for j in range(d)] for i in range(d)]
    comm = add(mm(a, dagger(a)), scale(mm(dagger(a), a), -1))
    target = [[(1-d*int(i == d-1))*int(i == j) for j in range(d)] for i in range(d)]
    matrix_close(comm, target)
    close(trace(comm), 0)
    population = [.97, 0, 0, .03]
    avg = sum(population[i]*comm[i][i] for i in range(d)).real
    close(avg, .88)
    return dict(cutoff_dimension=d, commutator_diagonal=[comm[i][i].real for i in range(d)],
                synthetic_populations=population, commutator_expectation=avg,
                expectation_error_vs_identity=1-avg)


CASES = {'00': case00, '01': case01, '02': case02, '03': case03, '04': case04,
         '05': case05, '13': case13, 'q1': caseq1, 'q2': caseq2, 'q3': caseq3, 'q4': caseq4}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=['all', *CASES], default='all')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    selected = CASES if args.case == 'all' else {args.case: CASES[args.case]}
    result = {'data_type': 'fixed synthetic inputs and analytic model calculations',
              'random_seed': None, 'cases': {key: run() for key, run in selected.items()}}
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered+'\n', encoding='utf-8')
    print(rendered)


if __name__ == '__main__':
    main()
