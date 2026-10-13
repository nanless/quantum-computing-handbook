#!/usr/bin/env python3
"""Independent analytical checks for shadow nonlinear estimators and Fock tails."""
import argparse, itertools, json, math, pathlib
if not __debug__: raise RuntimeError('Do not use -O')
def shadow():
    N=6; exact=[]
    # |0>: Z shadow takes 3 with p=1/3, 0 with p=2/3.
    mean=second=u=0
    for k in range(N+1):
        probability=math.comb(N,k)*(1/3)**k*(2/3)**(N-k)
        z=3*k/N; purity=(1+z*z)/2
        mean+=probability*z; second+=probability*z*z; u+=probability*purity
    assert abs(mean-1)<1e-12 and abs(second-(1+2/N))<1e-12
    assert abs(u-(1+1/N))<1e-12
    # Two independent snapshots correct the square bias: U-statistic E=1.
    pair=sum(pa*pb*a*b for a,pa in [(0,2/3),(3,1/3)] for b,pb in [(0,2/3),(3,1/3)])
    assert abs(pair-1)<1e-12
    return {'N':N,'E_Zbar':mean,'E_Zbar_squared':second,'E_plugin_purity':u,'true_purity':1,'independent_pair_Z_product':pair,'single_snapshot_eigenvalues':[2,-1]}
def fock():
    alpha2=1.; rows=[]
    probs=[math.exp(-alpha2)*alpha2**n/math.factorial(n) for n in range(60)]
    for d in [4,8,12]:
        retained=sum(probs[:d]); tail=sum(probs[d:]); subtractive=1-retained
        assert abs(retained+tail-1)<1e-12 and abs(tail-subtractive)<1e-12
        root=math.sqrt(retained); trace=math.sqrt(tail)
        # Relative weights of truncated coherent state, independent recurrence.
        c=[math.exp(-.5)]
        for n in range(1,d): c.append(c[-1]/math.sqrt(n))
        assert abs(sum(a*a for a in c)-retained)<1e-12
        rows.append({'d':d,'retained_mass':retained,'tail':tail,'root_fidelity':root,'trace_distance':trace,'truncated_normalized_mean_n':sum(n*probs[n] for n in range(d))/retained,'exact_mean_n':alpha2})
    # For mu=1, omitted terms from n=60 have ratios <=1/61.
    p60=math.exp(-alpha2)*alpha2**60/math.factorial(60)
    remainder_bound=p60/(1-alpha2/61)
    assert remainder_bound<1e-80
    return {'alpha_squared':alpha2,'rows':rows,'summed_tail_through_n':59,'remaining_tail_upper_bound':remainder_bound,'boundary':'known infinite coherent state versus normalized projected state; not driven truncated-Hamiltonian error'}
def main():
    p=argparse.ArgumentParser(); p.add_argument('case',choices=['all','13','q4']); a=p.parse_args()
    r={}
    if a.case in ['all','13']: r['13']=shadow()
    if a.case in ['all','q4']: r['q4']=fock()
    print(json.dumps(r,indent=2))
    if a.case=='all': pathlib.Path(__file__).with_name('round72-results.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__': main()
