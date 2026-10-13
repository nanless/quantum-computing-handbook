#!/usr/bin/env python3
"""Fixed, offline teaching checks A71-06/07/08/13/16/17/18/Q4.

Python standard library only. No random samples, cloud calls or vendor execution.
Basis: integer order, leftmost displayed bit most significant. All inputs are
synthetic exact models or explicitly stipulated counts. Run without -O.
"""
import argparse
import cmath
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path

TOL = 1e-10


def close(a, b, tol=TOL):
    assert abs(a-b) <= tol, (a, b, abs(a-b))


def eye(n):
    return [[complex(i == j) for j in range(n)] for i in range(n)]


def adj(a):
    return [list(v) for v in zip(*[[z.conjugate() for z in row] for row in a])]


def mul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def mv(a, v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def inner(v,w):
    return sum(a.conjugate()*b for a,b in zip(v,w))


def matclose(a,b):
    assert len(a)==len(b) and all(len(x)==len(y) for x,y in zip(a,b))
    for ra,rb in zip(a,b):
        for x,y in zip(ra,rb): close(x,y)


def unitary(a):
    matclose(mul(adj(a),a),eye(len(a)))


def entropy(ps):
    close(sum(ps),1)
    assert all(p>=0 for p in ps)
    return -sum(p*math.log2(p) for p in ps if p)


def chapter06():
    cases = [("partial",[1+0j,0j],[.6+0j,.8+0j]),
             ("identical",[1+0j,0j],[1+0j,0j]),
             ("orthogonal",[1+0j,0j],[0j,1+0j]),
             ("imaginary",[1+0j,0j],[-1j,0j])]
    rows=[]
    for name,g0,g1 in cases:
        v=[z/math.sqrt(2) for z in g0+g1]
        rho=[[sum(v[2*i+w]*v[2*j+w].conjugate() for w in range(2))
              for j in range(2)] for i in range(2)]
        c=inner(g1,g0)
        matclose(rho,[[.5,c/2],[c.conjugate()/2,.5]])
        p0=sum(sum(rho,[])).real/2
        purity=sum(mul(rho,rho)[i][i] for i in range(2)).real
        close(p0,(1+c.real)/2)
        close(purity,(1+abs(c)**2)/2)
        # Reset Kraus operators on work register: |0><0|, |0><1|.
        reset=[[0j]*4 for _ in range(4)]
        for old in range(2):
            branch=[v[old],0j,v[2+old],0j]
            for i in range(4):
                for j in range(4): reset[i][j]+=branch[i]*branch[j].conjugate()
        reduced=[[sum(reset[2*i+w][2*j+w] for w in range(2))
                  for j in range(2)] for i in range(2)]
        matclose(reduced,rho)
        rows.append(dict(case=name,garbage_overlap=[c.real,c.imag],p0=p0,purity=purity))
    close(rows[0]['p0'],.8); close(rows[0]['purity'],.68)
    close(rows[-1]['p0'],.5); close(rows[-1]['purity'],1)
    return dict(cases=rows,reset_keeps_reduced_state=True)


def rank2(rows):
    pivots={}
    for row in rows:
        z=row
        while z:
            p=z.bit_length()-1
            if p in pivots: z^=pivots[p]
            else:
                pivots[p]=z
                break
    return len(pivots)


def full_rank(k,d):
    if k<d: return Fraction(0)
    return math.prod((1-Fraction(2**j,2**k) for j in range(d)),start=Fraction(1))


def chapter07():
    allowed=[0,1,6,7]  # s=110, dot(z,s)=0.
    for z in allowed: assert bin(z & 6).count('1')%2==0
    rows=[]
    for k in range(6):
        total=4**k
        count=sum(rank2(seq)==2 for seq in product(allowed,repeat=k))
        exact=Fraction(count,total)
        assert exact==full_rank(k,2)
        rows.append(dict(k=k,full_rank_sequences=count,total=total,probability=float(exact)))
    p=full_rank(9,2)
    close(float(1-p),767/131072)
    assert 1-p<=Fraction(3,512)<Fraction(1,100)
    assert full_rank(0,0)==1
    return dict(enumerated=rows,k9_success=float(p),k9_failure=float(1-p),union_failure_bound=3/512)


def weighted_moments(counts,c1,c2):
    n=sum(counts.values())
    mean1=sum(nc*(1-2*int(x[0])) for x,nc in counts.items())/n
    mean2=sum(nc*(1-2*int(x[1])) for x,nc in counts.items())/n
    e=sum(nc*(c1*(1-2*int(x[0]))+c2*(1-2*int(x[1]))) for x,nc in counts.items())/n
    e2=sum(nc*(c1*(1-2*int(x[0]))+c2*(1-2*int(x[1])))**2 for x,nc in counts.items())/n
    cov=sum(nc*(1-2*int(x[0]))*(1-2*int(x[1])) for x,nc in counts.items())/n-mean1*mean2
    return dict(mean_z1=mean1,mean_z2=mean2,mean_energy=e,second_moment=e2,variance=e2-e*e,covariance=cov)


def chapter08():
    bell={"00":1,"11":1}
    exact={}
    for sign in (1,-1):
        stats=weighted_moments(bell,1,sign)
        close(stats['covariance'],1)
        close(stats['variance'],2+2*sign)
        exact['plus' if sign==1 else 'minus']=stats
    counts1={"00":60,"11":40}
    counts2={"00":20,"01":40,"10":40,"11":0}
    first=weighted_moments(counts1,1,-1)
    second=weighted_moments(counts2,1,-1)
    close(first['mean_z1'],second['mean_z1']); close(first['mean_z2'],second['mean_z2'])
    close(first['variance'],0);close(second['second_moment'],3.2)
    return dict(exact_bell=exact,stipulated_counts=[counts1,counts2],paired_statistics=[first,second],
                total_preparations=100,independent_optimal_variance=.04,
                grouped_plus_variance=.04,grouped_minus_variance=0)


def marginal(table,indices):
    out={}
    for key,p in table.items():
        short=''.join(key[i] for i in indices)
        out[short]=out.get(short,0)+p
    return out


def information(table):
    ent={name:entropy(list(marginal(table,idx).values())) for name,idx in
         [('A',[0]),('B',[1]),('C',[2]),('AB',[0,1]),('AC',[0,2]),('BC',[1,2]),('ABC',[0,1,2])]}
    return dict(entropies=ent,MI=ent['A']+ent['C']-ent['AC'],
                CMI=ent['AB']+ent['BC']-ent['B']-ent['ABC'])


def chapter13():
    chain={"000":3/8,"001":1/8,"110":1/8,"111":3/8}
    xor={key:1/4 for key in ['000','011','101','110']}
    r1,r2=information(chain),information(xor)
    close(r1['CMI'],0);close(r1['MI'],1-entropy([.25,.75]))
    close(r2['MI'],0);close(r2['CMI'],1)
    # Independently reconstruct the chain using only AB and p(C|B).
    ab=marginal(chain,[0,1]); rebuilt={}
    for key,p in ab.items():
        for c in '01': rebuilt[key+c]=p*(.75 if c==key[1] else .25)
    assert rebuilt==chain
    return dict(chain_table=chain,chain=r1,xor_table=xor,xor=r2,chain_recovered_from_AB=True)


def chapter16():
    rows=[]
    for x in (-1,-.5,0,.5,1):
        s=math.sqrt(1-x*x)
        uo=[[complex(x),1j*s],[1j*s,complex(x)]]
        ur=[[complex(x),complex(s)],[complex(s),complex(-x)]]
        z=[[1+0j,0j],[0j,-1+0j]]
        qo,qr=mul(z,uo),mul(z,ur)
        unitary(uo);unitary(ur);unitary(qo);unitary(qr)
        matclose(mul(qo,qo),eye(2))
        close(qr[0][0]+qr[1][1],2*x)
        close(qr[0][0]*qr[1][1]-qr[0][1]*qr[1][0],1)
        # QSP's W equals the corrected walk in a phase-changed basis;
        # it is not the bare walk Z U_o, despite U_o and W sharing entries.
        phase_basis=[[1+0j,0j],[0j,1j]]
        matclose(mul(adj(phase_basis),mul(qr,phase_basis)),uo)
        uh=[[0j]*4 for _ in range(4)]
        for i in range(2):
            for j in range(2):
                uh[i][j+2]=uo[i][j]
                uh[i+2][j]=adj(uo)[i][j]
        unitary(uh);matclose(adj(uh),uh);matclose(mul(uh,uh),eye(4))
        g=[1/math.sqrt(2)+0j,0j,1/math.sqrt(2)+0j,0j]
        close(inner(g,mv(uh,g)),x)
        if abs(x)<1:
            b=[(y-x*v)/s for y,v in zip(mv(uh,g),g)]
            close(inner(g,b),0);close(inner(b,b),1)
            # Hermitianized signal subspace matrix, not just its top entry.
            projected=[[inner(v,mv(uh,w)) for w in (g,b)] for v in (g,b)]
            matclose(projected,ur)
            expected=[s*v-x*w for v,w in zip(g,b)]
            for v,w in zip(mv(uh,b),expected):close(v,w)
        rows.append(dict(x=x,bare_walk_eigenphases=[0,math.pi],
                         corrected_eigenphases=[math.acos(x),-math.acos(x)],hermitianized_signal_block=x))
    return dict(cases=rows,extra_signal_qubits=1,nonhermitian_counterexample_checked=True,
                QSP_signal_phase_basis_similarity_checked=True)


def chapter17():
    j=2*math.pi*1e6
    rows=[]
    for t1,t2 in [(50e-9,50e-9),(50.5e-9,49.5e-9),(49.5e-9,50.5e-9)]:
        vals=[];zz12=[];zz23=[]
        for basis in range(8):
            spins=[1-2*((basis>>b)&1) for b in (2,1,0)]
            a,b=spins[0]*spins[1],spins[1]*spins[2]
            zz12.append(a);zz23.append(b);vals.append(j*(a+b))
        d1=[[cmath.exp(-1j*vals[i]*t1) if i==k else 0j for k in range(8)] for i in range(8)]
        d2=[[cmath.exp(-1j*vals[i]*t2) if i==k else 0j for k in range(8)] for i in range(8)]
        flip=[[complex(i==(k^4)) for k in range(8)] for i in range(8)]
        actual=mul(flip,mul(d2,mul(flip,d1)))
        predicted=[[cmath.exp(-1j*j*((t1-t2)*zz12[i]+(t1+t2)*zz23[i])) if i==k else 0j
                    for k in range(8)] for i in range(8)]
        matclose(actual,predicted);unitary(actual)
        target=[cmath.exp(-1j*j*(t1+t2)*z) for z in zz23]
        error=max(abs(actual[i][i]-target[i]) for i in range(8))
        delta=j*(t1-t2)
        close(error,2*abs(math.sin(delta/2)))
        assert error<=abs(delta)+TOL
        state=[complex(i in (0,4))/math.sqrt(2) for i in range(8)]
        out=mv(actual,state)
        pminus=abs((out[0]-out[4])/math.sqrt(2))**2
        close(pminus,math.sin(delta)**2)
        close(abs(out[0])**2,.5);close(abs(out[4])**2,.5)
        rows.append(dict(t1_ns=t1/1e-9,t2_ns=t2/1e-9,residual_phase_rad=delta,
                         operator_norm_error=error,p_X_minus=pminus))
    return dict(J_rad_per_second=j,sufficient_1e_minus3_time_difference_ns=1e-3/j/1e-9,cases=rows)


def hermitian2_eigenvalues(a,b,c):
    disc=math.sqrt((a-b)**2+4*abs(c)**2)
    return [(a+b-disc)/2,(a+b+disc)/2]


def chapter18():
    cases=[('two_small',.1,.1,0),('squeezed',.25,1,0),('correlated',.5,.5,.4)]
    rows=[]
    for name,a,b,c in cases:
        eig=hermitian2_eigenvalues(a,b,c+.5j)
        physical=min(eig)>=-TOL
        assert physical==(a*b-c*c>=.25-TOL)
        scaled=hermitian2_eigenvalues(2*a,2*b,2*c+1j)
        for x,y in zip(scaled,eig):close(x,2*y)
        assert (min(scaled)>=-TOL)==physical
        rows.append(dict(case=name,V=[[a,c],[c,b]],classical_eigenvalues=hermitian2_eigenvalues(a,b,c),
                         determinant=a*b-c*c,quantum_check_eigenvalues=eig,is_physical=physical,
                         hbar2_V=[[2*a,2*c],[2*c,2*b]]))
    close(rows[2]['quantum_check_eigenvalues'][0],.5-math.sqrt(41)/10)
    return dict(hbar=1,ordering='q1,p1,q2,p2,...',cases=rows)


def transmission(e,g=4):
    """Closed form made continuous at the top; e=E/V0, g=L sqrt(2mV0)/hbar."""
    assert e>0 and g>0
    z=g*math.sqrt(abs(1-e))
    if e<1: ratio=math.sinh(z)/z if z else 1
    elif e>1: ratio=math.sin(z)/z if z else 1
    else: ratio=1
    return 1/(1+g*g*ratio*ratio/(4*e))


def solve(a,b):
    """Small complex Gaussian elimination with partial pivoting."""
    rows=[list(row)+[rhs] for row,rhs in zip(a,b)]
    n=len(rows)
    for j in range(n):
        pivot=max(range(j,n),key=lambda k:abs(rows[k][j]))
        rows[j],rows[pivot]=rows[pivot],rows[j]
        assert abs(rows[j][j])>1e-14
        d=rows[j][j];rows[j]=[z/d for z in rows[j]]
        for k in range(n):
            if k!=j:
                fac=rows[k][j];rows[k]=[v-fac*w for v,w in zip(rows[k],rows[j])]
    return [row[-1] for row in rows]


def barrier_matching(e,g):
    k=g*math.sqrt(e);z=g*math.sqrt(abs(1-e))
    if e<1:
        C=math.cosh(z);S=math.sinh(z)/z;Cp=z*math.sinh(z);Sp=C
    elif e>1:
        C=math.cos(z);S=math.sin(z)/z;Cp=-z*math.sin(z);Sp=C
    else: C,S,Cp,Sp=1,1,0,1
    wave=cmath.exp(1j*k)
    mat=[[1,-1,0,0],[-1j*k,0,-1,0],[0,C,S,-wave],[0,Cp,Sp,-1j*k*wave]]
    rhs=[-1,-1j*k,0,0]
    r,A,B,t=solve(mat,rhs)
    for observed,expected in zip(mv(mat,[r,A,B,t]),rhs):close(observed,expected)
    return abs(t)**2,abs(r)**2


def chapterq4():
    rows=[]
    for g in (2,4):
        es=[.1,.5,.9,1-1e-8,1,1+1e-8,1.5,2,1+(math.pi/g)**2,1+(2*math.pi/g)**2]
        for e in es:
            matched,refl=barrier_matching(e,g)
            expected=transmission(e,g)
            close(matched,expected);close(matched+refl,1)
            rows.append(dict(g=g,e=e,T_closed=expected,T_matched=matched,R_matched=refl))
        close(transmission(1,g),1/(1+g*g/4))
        for l in (1,2): close(transmission(1+(l*math.pi/g)**2,g),1)
    assert abs(transmission(1-1e-8,4)-.2)<2e-8
    assert abs(transmission(1+1e-8,4)-.2)<2e-8
    return dict(cases=rows,g4_top=.2,g4_first_resonance_e=1+math.pi**2/16,
                units='dimensionless stationary-scattering model, equal outer velocities')


CASES={'06':chapter06,'07':chapter07,'08':chapter08,'13':chapter13,'16':chapter16,
       '17':chapter17,'18':chapter18,'q4':chapterq4}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapter',choices=['all']+list(CASES),nargs='?',default='all')
    parser.add_argument('--write-results',action='store_true')
    args=parser.parse_args()
    if not __debug__: parser.error('Assertions are required; do not run Python with -O.')
    if args.write_results and args.chapter!='all':parser.error('--write-results requires all')
    names=list(CASES) if args.chapter=='all' else [args.chapter]
    result={name:CASES[name]() for name in names}
    payload=dict(access_date='2026-10-13',data_kind='deterministic synthetic teaching calculations',
                 tolerance=TOL,chapters=result)
    serialized=json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if args.write_results:Path(__file__).with_name('round71-results.json').write_text(serialized)
    print(serialized,end='')


if __name__=='__main__':main()
