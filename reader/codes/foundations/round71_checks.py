#!/usr/bin/env python3
"""Eight fixed teaching checks, no hardware, network, third-party packages or PRNG.

Tensor factors run left to right, most significant first. Python >=3.9.
Reuses only this handbook's own matrix helpers. Do not run with -O.
"""
import argparse
import cmath
import json
import math
from pathlib import Path

from foundations_lab import (I, X, Y, Z, H, ZERO, PLUS, close, dagger, mm,
                            mv, inner, outer, add, scale, trace, kron, tensor,
                            matrix_close, eig2, state_check, reduced_a,
                            kraus_apply, entropy)


def packed(value):
    if isinstance(value, complex):
        return [value.real, value.imag]
    if isinstance(value, dict):
        return {k: packed(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [packed(v) for v in value]
    return value


def case00():
    rows = []
    for n in (20, 30):
        rows.append(dict(qubits=n, amplitudes=2**n,
                         statevector_bytes=16*2**n,
                         density_matrix_entries=4**n,
                         density_matrix_bytes=16*4**n))
    assert rows[0]['statevector_bytes'] == 16*2**20
    assert rows[1]['density_matrix_bytes'] == 16*2**60
    ket_ratio=(16*2**22)//(16*2**20)
    rho_ratio=(16*4**22)//(16*4**20)
    assert ket_ratio==4 and rho_ratio==16
    # Integer arithmetic only: do not allocate an exponential array.
    return dict(bytes_per_complex=16, rows=rows, actual_large_allocation=False,
                n22_vs_n20_ratios=[ket_ratio,rho_ratio])


def case01():
    s = 1/math.sqrt(2)
    w = [[s, s], [1j*s, -1j*s]]
    matrix_close(mm(dagger(w), w), I)
    coords = mv(dagger(w), ZERO)
    z_new = mm(mm(dagger(w), Z), w)
    matrix_close(z_new, X)
    close(inner(coords, mv(z_new, coords)), 1)
    close(inner(coords, mv(Z, coords)), 0)
    wrong_coords = mv([[w[j][i] for j in range(2)] for i in range(2)],
                      [s, 1j*s])
    # The transpose loses which Y eigenstate is present.
    matrix_close(outer(wrong_coords), [[0, 0], [0, 1]])
    return dict(basis_matrix=w, passive_coordinates=coords,
                z_in_new_basis=z_new, passive_z_expectation=1,
                active_w_dagger_then_fixed_z_expectation=0,
                transpose_on_y_plus_wrong_probabilities=[abs(x)**2 for x in wrong_coords])


def case02():
    m0 = [[math.sqrt(3)/2, 0], [0, .5]]
    m1 = [[.5, 0], [0, math.sqrt(3)/2]]
    rho = outer(PLUS)
    after = kraus_apply([m0, m1], rho)
    branches = []
    for m in (m0, m1):
        raw = mv(m, PLUS)
        prob = inner(raw, raw).real
        close(prob, .5)
        conditional = [x/math.sqrt(prob) for x in raw]
        close(inner(conditional, mv(X, conditional)), math.sqrt(3)/2)
        branches.append(dict(probability=prob, conditional_amplitudes=conditional))
    matrix_close(after, [[.5, math.sqrt(3)/4], [math.sqrt(3)/4, .5]])
    close(trace(mm(after, after)), .875)
    repeated_zero = inner(mv(m0, branches[0]['conditional_amplitudes']),
                          mv(m0, branches[0]['conditional_amplitudes'])).real
    close(repeated_zero, .625)
    return dict(branches=branches, nonselective_density_matrix=after,
                purity=trace(mm(after, after)).real,
                x_plus_probability=(1+math.sqrt(3)/2)/2,
                repeat_zero_given_first_zero=repeated_zero)


def reduced_b(rho):
    return [[sum(rho[2*a+b][2*a+d] for a in range(2))
             for d in range(2)] for b in range(2)]


def case03():
    s = math.sqrt(3)
    psi = [1/s, 1j/s, 0, 1/s]
    c = [[1/s, 1j/s], [0, 1/s]]
    ra, rb = reduced_a(outer(psi)), reduced_b(outer(psi))
    matrix_close(ra, mm(c, dagger(c)))
    ct = [[c[j][i] for j in range(2)] for i in range(2)]
    cs = [[complex(v).conjugate() for v in row] for row in c]
    matrix_close(rb, mm(ct, cs))
    weights = [(3+math.sqrt(5))/6, (3-math.sqrt(5))/6]
    us, vs = [], []
    reconstructed = [0j]*4
    for lam in weights:
        t = 3*lam-2
        u = [1j/math.sqrt(1+t*t), t/math.sqrt(1+t*t)]
        v = [x/math.sqrt(lam) for x in mv(ct, [x.conjugate() for x in u])]
        close(inner(u,u), 1)
        close(inner(v,v), 1)
        for actual, expected in zip(mv(ra,u),u):
            close(actual, lam*expected)
        for j, amp in enumerate(tensor(u,v)):
            reconstructed[j] += math.sqrt(lam)*amp
        us.append(u)
        vs.append(v)
    close(inner(us[0],us[1]), 0)
    close(inner(vs[0],vs[1]), 0)
    for a,b in zip(reconstructed,psi):
        close(a,b)
    # Omitting conjugation in the partner formula changes relative phases.
    wrong = [0j]*4
    for lam,u in zip(weights,us):
        v_bad = [x/math.sqrt(lam) for x in mv(ct,u)]
        for j,amp in enumerate(tensor(u,v_bad)):
            wrong[j] += math.sqrt(lam)*amp
    assert max(abs(a-b) for a,b in zip(outer(wrong)[0],outer(psi)[0])) > .1
    return dict(coefficients=c, reduced_a=ra, reduced_b=rb,
                schmidt_weights=weights, schmidt_a=us, schmidt_b=vs,
                reconstructed_amplitudes=reconstructed,
                entanglement_entropy_bits=entropy(weights))


def teleport_reference(rq):
    bell = [1/math.sqrt(2),0,0,1/math.sqrt(2)]
    psi = tensor(rq,bell)  # R Q A B
    cnot = [0j]*16
    for idx,amp in enumerate(psi):
        cnot[idx ^ (2 if (idx >> 2) & 1 else 0)] = amp
    psi = mv(kron(I,kron(H,kron(I,I))),cnot)
    probs = []
    raw_sum = [[0j]*4 for _ in range(4)]
    for qa in range(4):
        raw = [psi[(r<<3)|(qa<<1)|b] for r in range(2) for b in range(2)]
        p = inner(raw,raw).real
        close(p,.25)
        raw_sum = add(raw_sum,outer(raw))
        corrected = [x/math.sqrt(p) for x in raw]
        if qa & 1:
            corrected = mv(kron(I,X),corrected)
        if qa & 2:
            corrected = mv(kron(I,Z),corrected)
        matrix_close(outer(corrected),outer(rq))
        probs.append(p)
    return probs,raw_sum


def case04():
    bell = [1/math.sqrt(2),0,0,1/math.sqrt(2)]
    probs,unknown = teleport_reference(bell)
    matrix_close(unknown,scale(kron(I,I),.25))
    # Also verify a complex, unequal-Schmidt input and a product input.
    teleport_reference([math.sqrt(3)/2,0,0,.5j])
    teleport_reference(tensor(PLUS,[math.sqrt(3)/2,.5j]))
    dephased = [[0j]*4 for _ in range(4)]
    dephased[0][0]=dephased[3][3]=.5
    close(trace(mm(kron(X,X),outer(bell))),1)
    close(trace(mm(kron(X,X),dephased)),0)
    return dict(tensor_order='R Q A B', alice_result_order='Q A',
                four_probabilities=probs, all_corrected_rb_match=True,
                rb_without_classical_result=unknown,
                corrected_xx=1, measure_reprepare_xx=0,
                tested_input_families=['Bell','complex unequal Schmidt','product'])


def damping(gamma):
    return [[[1,0],[0,math.sqrt(1-gamma)]], [[0,math.sqrt(gamma)],[0,0]]]


def case05():
    p,gamma=.25,.36
    flip=[scale(I,math.sqrt(1-p)),scale(X,math.sqrt(p))]
    damp=damping(gamma)
    rho=outer(ZERO)
    fd=kraus_apply(damp,kraus_apply(flip,rho))
    df=kraus_apply(flip,kraus_apply(damp,rho))
    close(fd[1][1],.16)
    close(df[1][1],.25)
    for psi in (ZERO,PLUS,[math.sqrt(3)/2,.5j]):
        rho=outer(psi)
        left=kraus_apply(damp,kraus_apply(flip,rho))
        right=kraus_apply(flip,kraus_apply(damp,rho))
        matrix_close(add(left,scale(right,-1)),scale(Z,p*gamma))
    # Independent four-dimensional local channel: no signaling from B to A.
    psi=[math.sqrt(3)/2,0,0,.5j]
    joint=outer(psi)
    out=add(*(mm(mm(kron(I,k),joint),dagger(kron(I,k))) for k in damp))
    matrix_close(reduced_a(out),reduced_a(joint))
    return dict(flip_probability=p,damping_probability=gamma,
                flip_then_damp_excitation=fd[1][1].real,
                damp_then_flip_excitation=df[1][1].real,
                difference_matrix=add(fd,scale(df,-1)),
                remote_cptp_leaves_local_density_matrix=True)


def caseq1():
    rows=[]
    for phi in (0,math.pi/3,math.pi/2,math.pi):
        joint=[1/math.sqrt(2),0,0,cmath.exp(1j*phi)/math.sqrt(2)]  # path, record
        in_x_record=mv(kron(I,H),joint)
        output=mv(kron(H,I),in_x_record)
        probs=[abs(x)**2 for x in output]  # detector 0+,0-,1+,1-
        target=[(1+math.cos(phi))/4,(1-math.cos(phi))/4,
                (1-math.cos(phi))/4,(1+math.cos(phi))/4]
        for a,b in zip(probs,target):
            close(a,b)
        close(probs[0]+probs[1],.5)
        close(probs[0]+probs[2],.5)
        rows.append(dict(phi_radians=phi,joint_probabilities=probs,
                         detector_zero_given_plus=2*probs[0],
                         detector_zero_given_minus=2*probs[1],
                         detector_zero_nonselective=probs[0]+probs[1]))
    return dict(tensor_order='path record',output_order=['0+','0-','1+','1-'],
                ideal_expected_counts_at_phi_zero_for_400_inputs=[200,0,0,200],
                rows=rows)


def caseq2():
    psi=[math.cos(math.pi/8),math.sin(math.pi/8)]
    means=[inner(psi,mv(a,psi)).real for a in (X,Z)]
    vars_=[1-m*m for m in means]
    sym=scale(add(mm(X,Z),mm(Z,X)),.5)
    cov=inner(psi,mv(sym,psi)).real-means[0]*means[1]
    comm=add(mm(X,Z),scale(mm(Z,X),-1))
    bound=.25*abs(inner(psi,mv(comm,psi)))**2
    close(cov,-.5)
    close(vars_[0]*vars_[1],.25)
    close(cov**2+bound,.25)
    settings=[inner(psi,mv(scale(add(X,Z),1/math.sqrt(2)),psi)).real,
              inner(psi,mv(scale(add(X,scale(Z,-1)),1/math.sqrt(2)),psi)).real]
    close(settings[0],1)
    close(settings[1],0)
    return dict(x_z_means=means,x_z_variances=vars_,symmetric_covariance=cov,
                variance_product=vars_[0]*vars_[1],robertson_squared_bound=bound,
                schrodinger_squared_bound=cov**2+bound,
                independent_diagonal_axis_means=settings)


CASES={'00':case00,'01':case01,'02':case02,'03':case03,
       '04':case04,'05':case05,'q1':caseq1,'q2':caseq2}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    if not __debug__:
        parser.error('Checks require assertions; run without Python -O.')
    parser.add_argument('--case',choices=['all']+list(CASES),default='all')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    selected=CASES if args.case=='all' else {args.case:CASES[args.case]}
    result=packed(dict(kind='fixed synthetic teaching models',date='2026-10-13',
                       tolerance=1e-10,random_seed=None,
                       cases={k:fn() for k,fn in selected.items()}))
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload,encoding='utf-8')
    print(payload,end='')


if __name__=='__main__':
    main()
