#!/usr/bin/env python3
"""Eleven reproducible, standard-library quantum foundations experiments.

Run from any directory: python3 foundations_lab.py --case all
Outputs JSON on stdout; --output PATH also saves it. No quantum hardware is used.
Vectors use left-to-right tensor factors (A, B, ...), most significant first.
All statistical draws use a local seeded PRNG and are synthetic, not Born tests.
"""
import argparse
import cmath
import json
import math
import random
from pathlib import Path

TOL = 1e-10
I = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
Y = [[0, -1j], [1j, 0]]
Z = [[1, 0], [0, -1]]
H = [[1 / math.sqrt(2), 1 / math.sqrt(2)],
     [1 / math.sqrt(2), -1 / math.sqrt(2)]]
ZERO = [1, 0]
PLUS = [1 / math.sqrt(2)] * 2


def close(a, b, tol=TOL):
    assert abs(a - b) <= tol, (a, b, tol)


def dagger(a):
    return [[complex(a[j][i]).conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def mm(a, b):
    assert len(a[0]) == len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, v):
    assert len(a[0]) == len(v)
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def inner(a, b):
    return sum(complex(x).conjugate() * y for x, y in zip(a, b))


def outer(v):
    return [[x * complex(y).conjugate() for y in v] for x in v]


def add(*matrices):
    return [[sum(a[i][j] for a in matrices)
             for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def scale(a, x):
    return [[x * v for v in row] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def kron(a, b):
    return [[x * y for x in row_a for y in row_b]
            for row_a in a for row_b in b]


def tensor(a, b):
    return [x * y for x in a for y in b]


def matrix_close(a, b, tol=TOL):
    assert len(a) == len(b) and len(a[0]) == len(b[0])
    for row_a, row_b in zip(a, b):
        for x, y in zip(row_a, row_b):
            close(x, y, tol)


def eig2(a):
    """Eigenvalues of a 2x2 Hermitian matrix (no positivity assumption)."""
    matrix_close(a, dagger(a))
    tr = trace(a).real
    gap = math.sqrt((a[0][0].real - a[1][1].real) ** 2 + 4 * abs(a[0][1]) ** 2)
    return [(tr - gap) / 2, (tr + gap) / 2]


def state_check(rho):
    close(trace(rho), 1)
    assert min(eig2(rho)) >= -TOL


def reduced_a(rho):
    assert len(rho) == 4
    return [[sum(rho[2*a+b][2*c+b] for b in range(2))
             for c in range(2)] for a in range(2)]


def kraus_apply(ks, rho):
    matrix_close(add(*(mm(dagger(k), k) for k in ks)), I)
    out = add(*(mm(mm(k, rho), dagger(k)) for k in ks))
    state_check(out)
    return out


def rotation(pauli, angle):
    return add(scale(I, math.cos(angle / 2)), scale(pauli, -1j * math.sin(angle / 2)))


def entropy(values):
    assert min(values) >= -TOL
    close(sum(values), 1)
    return -sum(x * math.log2(x) for x in values if x > 0)


def case00(seed):
    """Synthetic shots plus exact binomial/ Hoeffding quantities."""
    rng = random.Random(seed)
    n = 1000
    ones = sum(rng.random() < 0.5 for _ in range(n))
    radius = math.sqrt(math.log(2 / 0.05) / (2 * n))
    exact_balanced = math.comb(n, n // 2) / (2 ** n)
    close(sum(abs(x)**2 for x in mv(H, ZERO)), 1)
    assert 0 <= ones <= n and 0 < exact_balanced < 0.026
    # No assertion that every random batch must lie in a confidence interval.
    return dict(shots=n, zeros=n-ones, ones=ones, frequency=ones/n,
                theoretical_standard_deviation=math.sqrt(.25/n),
                hoeffding_radius_95=radius,
                probability_exactly_500_ones=exact_balanced)


def case01(seed):
    v = [1/math.sqrt(3), (1+1j)/math.sqrt(3)]
    rho = outer(v)
    state_check(rho)
    close(inner(v, v), 1)
    close(sum(x*x for x in v), (1+2j)/3)
    w = mv(H, v)
    close(inner(w, w), 1)
    matrix_close(mm(rho, rho), rho)
    return dict(norm_squared=inner(v,v).real,
                wrong_no_conjugation=[sum(x*x for x in v).real,
                                      sum(x*x for x in v).imag],
                output_probabilities=[abs(x)**2 for x in w], purity=trace(mm(rho,rho)).real)


def case02(seed):
    v = [math.sqrt(3)/2, .5j]
    s_dagger = [[1,0],[0,-1j]]
    correct = mv(H, mv(s_dagger, v))  # first S dagger, then H, then Z readout
    wrong = mv(s_dagger, mv(H, v))
    expected = (2+math.sqrt(3))/4
    close(abs(correct[0])**2, expected)
    close(abs(wrong[0])**2, .5)
    return dict(y_plus_probability=abs(correct[0])**2,
                wrong_gate_order_probability=abs(wrong[0])**2,
                bloch=[inner(v,mv(p,v)).real for p in (X,Y,Z)])


def case03(seed):
    v = [math.sqrt(3)/2,0,0,.5j]
    rho = outer(v)
    marginal = reduced_a(rho)
    matrix_close(marginal, [[.75,0],[0,.25]])
    ub = rotation(Y, .731)
    joint_u = kron(I,ub)
    after = mm(mm(joint_u,rho), dagger(joint_u))
    matrix_close(reduced_a(after), marginal)
    close(trace(mm(marginal,marginal)), .625)
    return dict(local_probabilities=[marginal[i][i].real for i in range(2)],
                local_purity=trace(mm(marginal,marginal)).real,
                remote_unitary_leaves_local_state=True)


def case04(seed):
    # Actual 8-component circuit, not the already-known teleportation identity.
    v = [math.sqrt(3)/2, .5j]
    bell = [1/math.sqrt(2),0,0,1/math.sqrt(2)]
    initial = tensor(v,bell)
    cnot = [0j]*8
    for idx, amplitude in enumerate(initial):
        q = (idx >> 2) & 1
        cnot[idx ^ (2 if q else 0)] = amplitude  # Q controls A
    evolved = mv(kron(H,kron(I,I)),cnot)
    probabilities = []
    bob_without_record = [[0j,0j],[0j,0j]]
    for result in range(4):
        raw = evolved[2*result:2*result+2]
        p = inner(raw,raw).real
        close(p,.25)
        probabilities.append(p)
        bob_without_record = add(bob_without_record,outer(raw))
        branch = [x/math.sqrt(p) for x in raw]
        if result & 1:
            branch = mv(X,branch)
        if result & 2:
            branch = mv(Z,branch)
        matrix_close(outer(branch),outer(v))
    matrix_close(bob_without_record, scale(I,.5))
    return dict(branch_probabilities=probabilities,
                all_four_corrected_density_matrices_match=True,
                bob_before_message_diagonal=[.5,.5])


def case05(seed):
    gamma = .36
    ks = [[[1,0],[0,math.sqrt(1-gamma)]], [[0,math.sqrt(gamma)],[0,0]]]
    out = kraus_apply(ks,outer(PLUS))
    matrix_close(out,[[.68,.4],[.4,.32]])
    # Compose independently parameterized channels and compare population vs coherence.
    t, t1, tphi = 40.,60.,60.  # all in microseconds
    gamma_t = 1-math.exp(-t/t1)
    damp = [[[1,0],[0,math.sqrt(1-gamma_t)]],[[0,math.sqrt(gamma_t)],[0,0]]]
    pz = (1-math.exp(-t/tphi))/2
    phase = [scale(I,math.sqrt(1-pz)),scale(Z,math.sqrt(pz))]
    total = kraus_apply(phase,kraus_apply(damp,outer(PLUS)))
    close(total[1][1],.5*math.exp(-2/3))
    close(total[0][1],.5*math.exp(-1))
    # Boundary cases gamma=0 and gamma=1 check identity/reset explicitly.
    matrix_close(kraus_apply([I],outer(PLUS)),outer(PLUS))
    matrix_close(kraus_apply([[[1,0],[0,0]],[[0,1],[0,0]]],outer(PLUS)),outer(ZERO))
    return dict(gamma=gamma, output_real=out, eigenvalues=eig2(out),
                t2_microseconds=1/(1/(2*t1)+1/tphi),
                population_at_40us=total[1][1].real,
                coherence_at_40us=total[0][1].real)


def case13(seed):
    # Unequal priors require the weighted Helstrom matrix, not unweighted T.
    rho, sigma = outer(ZERO),outer(PLUS)
    records=[]
    for prior in [.5,.9]:
        eig=eig2(add(scale(rho,prior),scale(sigma,-(1-prior))))
        pguess=(1+sum(abs(x) for x in eig))/2
        close(pguess,(1+math.sqrt(1-2*prior*(1-prior)))/2)
        records.append(dict(prior_zero=prior, success=pguess,
                            always_guess_more_likely=max(prior,1-prior)))
    close(records[1]['success'],(1+math.sqrt(.82))/2)
    return dict(helstrom=records, root_fidelity=1/math.sqrt(2),
                squared_fidelity=.5, entropy_diagonal_75_25=entropy([.75,.25]))


def caseq1(seed):
    # Trace out an explicit record qubit; complex gamma tests phase sign.
    gamma=.6*cmath.exp(1j*math.pi/3)
    d0=[1,0]
    d1=[gamma.conjugate(),math.sqrt(1-abs(gamma)**2)]
    values=[]
    for phi in [0,math.pi/3,math.pi,4*math.pi/3]:
        joint=[x/math.sqrt(2) for x in d0]+[cmath.exp(1j*phi)*x/math.sqrt(2) for x in d1]
        rho=reduced_a(outer(joint))
        state_check(rho)
        output=mm(mm(H,rho),H)
        p0=output[0][0].real
        close(p0,(1+(gamma*cmath.exp(-1j*phi)).real)/2)
        values.append(dict(phase_rad=phi,p0=p0))
    close(values[1]['p0'],.8)
    close(values[3]['p0'],.2)
    return dict(record_overlap_magnitude=.6, visibility=.6, phase_scan=values)


def caseq2(seed):
    rx,rz=rotation(X,math.pi/2),rotation(Z,math.pi/2)
    forward=mv(rz,mv(rx,ZERO))
    reverse=mv(rx,mv(rz,ZERO))
    close(abs(inner(PLUS,forward))**2,1)
    close(abs(inner(PLUS,reverse))**2,.5)
    bell=[1/math.sqrt(2),0,0,1/math.sqrt(2)]
    theta=.713
    local_identity_phase=kron(scale(I,cmath.exp(-1j*theta)),I)
    matrix_close(outer(mv(local_identity_phase,bell)),outer(bell))
    # Branch-dependent energy adds a relative phase; contrast theta=pi.
    branch_phase=kron([[1,0],[0,-1]],I)
    shifted=mv(branch_phase,bell)
    close(abs(inner(bell,shifted))**2,0)
    return dict(x_plus_forward=abs(inner(PLUS,forward))**2,
                x_plus_reverse=abs(inner(PLUS,reverse))**2,
                subsystem_identity_shift_changes_density_matrix=False,
                branch_phase_pi_bell_overlap_squared=abs(inner(bell,shifted))**2)


def caseq3(seed):
    h,kb=6.62607015e-34,1.380649e-23
    energy_kelvin=h*5e9/kb
    # exp(-x)/(1+exp(-x)) is stable at low T; exp(+x) may overflow.
    thermal=[]
    for temp in [.020,.050,300]:
        weight=math.exp(-energy_kelvin/temp)
        thermal.append(dict(temperature_K=temp,p1=weight/(1+weight)))
    omega,delta=2*math.pi*10e6,2*math.pi*6e6
    omega_r=math.hypot(omega,delta)
    tpeak=math.pi/omega_r
    ze=scale(Z,-1)
    generator=add(scale(X,omega/omega_r),scale(ze,delta/omega_r))
    u=rotation(generator,omega_r*tpeak)
    p1=abs(mv(u,ZERO)[1])**2
    close(p1,100/136)
    close(energy_kelvin,.23996215366831106)
    return dict(gap_divided_by_kb_K=energy_kelvin,thermal=thermal,
                detuned_peak_ns=tpeak*1e9,detuned_max_population=p1,
                resonant_pi_pulse_ns=math.pi/omega*1e9)


def caseq4(seed):
    # L=1, hbar^2/(2m)=1. N interior points, Dirichlet endpoints.
    # Analytic eigenpair of the discrete tridiagonal operator is checked by its action.
    records=[]
    for n in [15,31,63,127]:
        dx=1/(n+1)
        v=[math.sqrt(2*dx)*math.sin(math.pi*j*dx) for j in range(1,n+1)]
        close(inner(v,v),1)
        hv=[(2*v[j]-(v[j-1] if j else 0)-(v[j+1] if j<n-1 else 0))/dx**2
            for j in range(n)]
        e=inner(v,hv).real
        closed_form=4/dx**2*math.sin(math.pi/(2*(n+1)))**2
        close(e,closed_form,1e-9)
        assert max(abs(a-e*b) for a,b in zip(hv,v)) < 1e-8
        error=math.pi**2-e
        assert error>0
        records.append(dict(interior_points=n,dx=dx,energy=e,absolute_error=error))
    ratios=[records[j]['absolute_error']/records[j+1]['absolute_error'] for j in range(3)]
    assert all(3.97 < ratio < 4.01 for ratio in ratios)
    # Independent midpoint integration of continuous probability, not formula reuse.
    m=10000
    p=sum(2*math.sin(math.pi*(.25+(j+.5)*.5/m))**2*.5/m for j in range(m))
    close(p,.5+1/math.pi,2e-9)
    return dict(grid=records,error_ratios=ratios,middle_half_probability=p,
                exact_energy=math.pi**2)


CASES={'00':case00,'01':case01,'02':case02,'03':case03,'04':case04,
       '05':case05,'13':case13,'q1':caseq1,'q2':caseq2,'q3':caseq3,'q4':caseq4}


def json_real(value):
    if isinstance(value,complex):
        close(value.imag,0)
        return value.real
    raise TypeError(type(value).__name__)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=['all']+list(CASES),default='all')
    parser.add_argument('--seed',type=int,default=20260926)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    names=list(CASES) if args.case=='all' else [args.case]
    report={'schema_version':1,'seed':args.seed,'synthetic':True,
            'tensor_order':'left factor is most significant',
            'cases':{key:CASES[key](args.seed) for key in names}}
    payload=json.dumps(report,indent=2,ensure_ascii=False,default=json_real)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding='utf-8')
    print(payload,end='')


if __name__=='__main__':
    main()
