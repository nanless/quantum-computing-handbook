#!/usr/bin/env python3
"""Deterministic teaching checks; Python standard library only, no cloud jobs.

Run from repository root: python3 codes/algorithms/round70_checks.py all
All counts are specified synthetic fixtures, not hardware records. Basis order
is the displayed binary integer order; the Hadamard ancilla is the left bit.
"""
import argparse
import itertools
import json
import math
from pathlib import Path


def near(a, b, tol=1e-10):
    assert abs(a - b) <= tol, (a, b)


def norm(v):
    return math.sqrt(sum(abs(x) ** 2 for x in v))


def hadamard_prob(psi, upsi, phase):
    # Following controlled-U, phase=1 for X and -i for S-dagger then H.
    joint = [x / math.sqrt(2) for x in psi] + [phase*x/math.sqrt(2) for x in upsi]
    out = [(joint[j] + joint[j+2])/math.sqrt(2) for j in range(2)]
    out += [(joint[j] - joint[j+2])/math.sqrt(2) for j in range(2)]
    near(norm(out), 1)
    return sum(abs(x)**2 for x in out[:2])


def check06():
    psi = [1/math.sqrt(2)]*2
    rows = []
    for eigenvalue in (1j, -1j, 1, -1):
        upsi = ([eigenvalue*x for x in psi] if isinstance(eigenvalue, int)
                else [psi[0], eigenvalue*psi[1]])
        z = sum(x.conjugate()*y for x, y in zip(map(complex, psi), upsi))
        px, py = hadamard_prob(psi, upsi, 1), hadamard_prob(psi, upsi, -1j)
        near(px, (1+z.real)/2)
        near(py, (1+z.imag)/2)
        wrong = hadamard_prob(psi, upsi, 1j)
        near(2*wrong-1, -z.imag)
        rows.append({'U_11_or_scalar': str(eigenvalue), 'Re_z': z.real, 'Im_z': z.imag,
                     'p0_X': px, 'p0_Y': py, 'wrong_S_mean': 2*wrong-1})
    # Changing the reflection order alone does not preserve success probability.
    state = [.5, math.sqrt(3)/2]  # good, bad basis; a = 1/4.
    def reflection(v):
        dot = sum(a*b for a,b in zip(state,v))
        return [2*a*dot-b for a,b in zip(state,v)]
    ds = reflection([-state[0],state[1]])
    sd0 = reflection(state)
    sd = [-sd0[0],sd0[1]]
    near(abs(ds[0])**2,1)
    near(abs(sd[0])**2,.25)
    return {'hadamard_tests': rows, 'reflection_order_success':
            {'D_after_S':abs(ds[0])**2,'S_after_D':abs(sd[0])**2}}


def amp_prob(a, k):
    return min(1.0, max(0.0, math.sin((2*k+1)*math.asin(math.sqrt(a)))**2))


def bernoulli_log_likelihood(h, n, p):
    if p == 0:
        return 0.0 if h == 0 else -math.inf
    if p == 1:
        return 0.0 if h == n else -math.inf
    return h*math.log(p)+(n-h)*math.log1p(-p)


def check07():
    counts = [{'k': 0, 'successes': 25, 'shots': 100},
              {'k': 1, 'successes': 100, 'shots': 100}]
    def ll(a):
        return sum(bernoulli_log_likelihood(d['successes'], d['shots'], amp_prob(a,d['k']))
                   for d in counts)
    near(amp_prob(.25,1),1)
    near(amp_prob(1,1),1)
    for i in range(1001):
        a = i/1000
        near(amp_prob(a,1), a*(3-4*a)**2)
    maximum = max(range(1001), key=lambda i: ll(i/1000))/1000
    near(maximum,.25)
    assert ll(1) == -math.inf
    near(bernoulli_log_likelihood(0,100,0),0)
    near(bernoulli_log_likelihood(100,100,1),0)
    calls = sum(d['shots']*(2*d['k']+1) for d in counts)
    assert calls == 400
    return {'synthetic_counts': counts, 'grid_max_a': maximum, 'A_and_inverse_calls': calls,
            'good_reflections': 100, 'likelihood_a1': 'zero', 'log_likelihood_a025': ll(.25)}


def ry(theta, v):
    c, s = math.cos(theta/2), math.sin(theta/2)
    return [c*v[0]-s*v[1], s*v[0]+c*v[1]]


def rotation_expectation(a,b):
    v = ry(b,ry(a,[1,0]))
    near(norm(v),1)
    return abs(v[0])**2-abs(v[1])**2


def check08():
    t = math.pi/8
    shift = math.pi/2
    partial1 = (rotation_expectation(t+shift,t)-rotation_expectation(t-shift,t))/2
    partial2 = (rotation_expectation(t,t+shift)-rotation_expectation(t,t-shift))/2
    wrong = (rotation_expectation(t+shift,t+shift)-rotation_expectation(t-shift,t-shift))/2
    derivative = -2*math.sin(2*t)
    near(partial1+partial2,derivative)
    near(wrong,0)
    for i in range(101):
        x = i*math.pi/50
        near(rotation_expectation(x,x),math.cos(2*x))
    return {'theta':t, 'wrong_shared_shift':wrong, 'partial_derivatives':[partial1,partial2],
            'correct_gradient':derivative, 'single_gate_shift_std_bound':1/math.sqrt(2000),
            'finite_difference_h001_std_bound':1/(.01*math.sqrt(2000))}


def check16():
    rows=[]
    for e in (.001,.00005):
        v,w=[.01,0],[.01,e]
        r,s=norm(v),norm(w)
        d=norm([x/r-y/s for x,y in zip(v,w)])
        bound=2*e/r
        assert d <= bound
        p,pt=r*r,s*s
        assert max(0,r-e)**2 <= pt <= min(1,(r+e)**2)
        overlap=sum((x/r)*(y/s) for x,y in zip(v,w))
        near(overlap**2, .0001/(.0001+e*e))
        rows.append({'epsilon':e,'ideal_success':p,'actual_success':pt,
                     'conditional_vector_error':d,'error_bound':bound,
                     'root_fidelity':overlap,'squared_fidelity':overlap**2})
    near(.01*math.sqrt(.0001)/2,.00005)
    return rows


def chain_energies(j):
    return [(a,b,-2*a+2*b-j*a*b) for a,b in itertools.product((-1,1),repeat=2)]


def check17():
    rows=[]
    for j in (1,2,3,8):
        es=chain_energies(j)
        ground=min(e for a,b,e in es)
        minima=[(a,b) for a,b,e in es if e==ground]
        broken=sum(a!=b for a,b in minima)
        assert broken == (1 if j<=2 else 0)
        rows.append({'J':j,'four_energies':es,'ground_energy':ground,'ground_states':minima,
                     'broken_ground_states':broken,'scaled_field_magnitude':2/max(2,j)})
    return rows


def erase_fail_rate(code, eps):
    results=[]
    for word in code:
        fail=0.0
        for mask in itertools.product((0,1),repeat=3): # 1 is an erasure.
            p=math.prod(eps if erased else 1-eps for erased in mask)
            candidates=[x for x in code if all(erased or a==b
                                               for a,b,erased in zip(x,word,mask))]
            assert word in candidates
            if len(candidates)!=1:
                fail+=p
        results.append(fail)
    for result in results:
        near(result,results[0])
    return results[0]


def check18():
    repeat=['000','111']
    parity=[f'{a}{b}{a^b}' for a,b in itertools.product((0,1),repeat=2)]
    rows=[]
    for eps in (0,.25,.5,.75,1):
        r=erase_fail_rate(repeat,eps)
        p=erase_fail_rate(parity,eps)
        near(r,eps**3)
        near(p,3*eps**2-2*eps**3)
        rows.append({'erasure_probability':eps,'repeat_block_failure':r,'parity_block_failure':p})
    return {'repeat_code':repeat,'parity_code':parity,'all_eight_masks_checked_per_message':True,
            'rates_bit_per_use':[1/3,2/3],'results':rows}


CHECKS={'06':check06,'07':check07,'08':check08,'16':check16,'17':check17,'18':check18}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapter',choices=['all',*CHECKS])
    parser.add_argument('--write-results',action='store_true')
    args=parser.parse_args()
    selected=CHECKS if args.chapter=='all' else {args.chapter:CHECKS[args.chapter]}
    result={key:fn() for key,fn in selected.items()}
    document=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    print(document,end='')
    if args.write_results:
        assert args.chapter=='all','Write complete results only.'
        Path(__file__).with_name('round70-results.json').write_text(document)

if __name__=='__main__':
    main()
