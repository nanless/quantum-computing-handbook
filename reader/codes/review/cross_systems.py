"""Independent eight-topic review. Does not if not __debug__:
    raise RuntimeError('Independent numerical review requires assertions; run without -O.')

import systems implementation.

Matrix primitives come only from this handbook's foundations helpers; physical
circuits, recurrence, subgroup enumeration and probability propagation are new.
"""
import cmath
import itertools
import json
import math
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'codes/foundations'))
from foundations_lab import I,X,Y,Z,H,mm,mv,kron,tensor,outer,trace,inner,rotation


def check(a,b,tol=1e-10):
    assert abs(a-b)<tol,(a,b)


out={}
value=.01+.99*math.exp(-5)
errors=[]
for steps in (1000,2000,4000):
    v=1.
    for j in range(steps):
        v+=.0005/steps*(100*(1-v)-9900*v)
    errors.append(abs(v-value))
assert 1.9<errors[0]/errors[1]<2.1 and 1.9<errors[1]/errors[2]<2.1
out['09']={'thermal_limit':value,'euler_step_halving_errors':errors,
           'target_wait_us':100*math.log(99)}

# String Pauli language, independent from author's binary-mask implementation.
letters='IXYZ'
def product(a,b):
    return ''.join(x if y=='I' else y if x=='I' else 'I' if x==y
                   else next(z for z in 'XYZ' if z not in (x,y))
                   for x,y in zip(a,b))
def anti(a,b):
    return sum(x!=y and x!='I' and y!='I' for x,y in zip(a,b))%2
gens=['IIIXXXX','IXXIIXX','XIXIXIX','IIIZZZZ','IZZIIZZ','ZIZIZIZ']
stab={'IIIIIII'}
for g in gens:
    stab|={product(g,v) for v in list(stab)}
normal=[ ''.join(p) for p in itertools.product(letters,repeat=7)
         if all(not anti(''.join(p),g) for g in gens)]
assert len(stab)==64 and len(normal)==256
assert min(sum(c!='I' for c in v) for v in normal if v not in stab)==3
a,b='XIIIIII','IXXIIII'
assert [anti(a,g) for g in gens]==[anti(b,g) for g in gens]
assert product(a,b) in normal and product(a,b) not in stab
out['10']={'stabilizers':len(stab),'normalizer':len(normal),
           'boundary_difference':product(a,b),'distance':3}

parity_errors=[]
for p,n in itertools.product((0,.01,.2,.5), (0,1,2,100)):
    q=0.
    for j in range(n):
        q=p+(1-2*p)*q
    analytic=(1-(1-2*p)**n)/2
    parity_errors.append(abs(q-analytic))
    check(q,analytic)
out['11']={'grid_max_difference':max(parity_errors),
           'final100':(1-.98**100)/2,'at_least_one':1-.99**100}

# Bell noise is input to a physical CNOT/H circuit, followed by computational
# measurement; author instead directly contracts a Bell measurement bra.
def bell(x,z):
    return mv(kron(I,mm(rotation(Z,math.pi*z),rotation(X,math.pi*x))),
              [1/math.sqrt(2),0,0,1/math.sqrt(2)])
bells=[bell(x,z) for x,z in itertools.product(range(2),repeat=2)]
max_swap_error=0.
for w,v in (([.9,.1/3,.1/3,.1/3],)*2,([.9,.1,0,0],)*2,
            ([.55,.2,.15,.1],[.7,.1,.05,.15])):
    expected=[sum(w[a]*v[b] for a in range(4) for b in range(4) if a^b==c)
              for c in range(4)]
    for result in range(4):
        rho=[[0j]*4 for j in range(4)]
        for a,b in itertools.product(range(4),repeat=2):
            psi=tensor(bells[a],bells[b])
            after=[0j]*16
            for i,amp in enumerate(psi):
                after[i^(2 if i&4 else 0)]=amp
            psi=mv(kron(I,kron(H,kron(I,I))),after)
            raw=[psi[(r<<3)|(result<<1)|c] for r,c in itertools.product(range(2),repeat=2)]
            if result&1: raw=mv(kron(I,X),raw)
            if result&2: raw=mv(kron(I,Z),raw)
            branch=outer(raw)
            for i,j in itertools.product(range(4),repeat=2):
                rho[i][j]+=w[a]*v[b]*branch[i][j]
        check(trace(rho),.25)
        for c in range(4):
            actual=4*inner(bells[c],mv(rho,bells[c])).real
            max_swap_error=max(max_swap_error,abs(actual-expected[c]))
            check(actual,expected[c])
out['12']={'physical_circuit_vs_convolution_max_error':max_swap_error,
           'symmetric_hops4':(1+3*(13/15)**4)/4,
           'symmetric_hops8':(1+3*(13/15)**8)/4}

frame_errors=[]
def axis(phi):
    return [[math.cos(phi)*X[i][j]+math.sin(phi)*Y[i][j] for j in range(2)] for i in range(2)]
for a,t,p in itertools.product((-.7,0,math.pi/2),(-1.2,.4,math.pi/2),(-.6,.2,1.1)):
    left=mm(rotation(axis(p),t),rotation(Z,a))
    right=mm(rotation(Z,a),rotation(axis(p-a),t))
    for i,j in itertools.product(range(2),repeat=2):
        frame_errors.append(abs(left[i][j]-right[i][j]));check(left[i][j],right[i][j])
out['14']={'arbitrary_equatorial_axis_max_error':max(frame_errors)}

# Exact finite-horizon crossing probability for the same alpha spending rule.
# Cumulative looks are dependent; retain full count distribution of survivors.
alive={0:1.};prev=0;crossed=0.
for j,n in enumerate((5,10,20),1):
    dist={}
    for count,prob in alive.items():
        for inc in range(n-prev+1):
            mass=prob*math.comb(n-prev,inc)*.5**(n-prev)
            k=count+inc
            lo=k/n-math.sqrt(math.log(j*(j+1)/.05)/(2*n))
            if lo>.5:crossed+=mass
            else:dist[k]=dist.get(k,0)+mass
    alive=dist;prev=n
assert crossed<=.05
check(crossed+sum(alive.values()),1)
out['15']={'p_null':.5,'look_sizes':[5,10,20],
           'exact_any_lower_bound_false_crossing':crossed,
           'is_only_finite_model_check_not_coverage_proof':True}

ks=[[[1,0],[0,0]],[[0,0],[0,1]]]
ls=[[[1,0],[0,0]],[[0,1],[0,0]]]
results=[]
for psi in ([1,0],[0,1],[math.sqrt(3)/2,.5j]):
    same=[]
    for ops in (ks,ls):
        # Explicit joint outcomes (a,b), not just same-result shortcut.
        probs=[inner(mv(b,mv(a,psi)),mv(b,mv(a,psi))).real for a in ops for b in ops]
        check(sum(probs),1);same.append(probs[0]+probs[3])
    check(same[0],1);check(same[1],abs(psi[0])**2);results.append(same)
out['19']={'same_result_probabilities':results}

rows=[]
for tau in (2.5e-9,5e-9,10e-9):
    omega=.1/tau;delta=2*math.pi*200e6
    norm=math.sqrt(omega**2+delta**2)
    unitary=rotation([[ (omega*X[i][j]+delta*Z[i][j])/norm for j in range(2)] for i in range(2)],norm*tau)
    prob=abs(mv(unitary,[1,0])[1])**2
    integral=(-1j*omega/2)*(cmath.exp(1j*delta*tau)-1)/(1j*delta)
    rows.append([tau*1e9,abs(integral)**2,prob])
assert rows[1][1]<1e-30 and rows[1][2]>1e-12
out['q3']={'matrix_exponential_and_first_order_probability':rows}

# Optional cross-check of the newly added software-practice sections 11-16.
weights=[-1/3,4/3]
values=[.25+.12/k**2+.03/k**4 for k in (2,4)]
comb=sum(a*b for a,b in zip(weights,values))
check(comb,.24953125)
variance=sum(c*c/n for c,n in zip(weights,(1800,7200)))
check(variance,25/81000)
exact=(1+math.cos(2*math.sqrt(2)*.7))/2
approx=[]
for k in (2,4):
    h=.7/k
    one_step=mm(mm(rotation(X,h),rotation(Z,2*h)),rotation(X,h))
    vec=[1,0]
    for _ in range(k):vec=mv(one_step,vec)
    approx.append(inner(vec,mv(Z,vec)).real)
estimate=sum(c*v for c,v in zip(weights,approx))
check(exact,.301106901,5e-10)  # manuscript gives only nine decimal places
assert abs(estimate-exact)<abs(approx[1]-exact)
u=rotation(Y,math.pi/6)
psi=mv(u,[1/math.sqrt(2)]*2)
check(inner(psi,mv(Z,psi)),-.5)
v=mv(u,[1,0])
check(.9*inner(v,mv(X,v))+.1*inner(mv(Z,v),mv(X,mv(Z,v))),.4)
hd=[[0,-1,0],[-1,0,0],[0,0,2]]
pd=[[1,0,1],[0,1,0],[0,0,0]]
fake=[.5,1/math.sqrt(2),.5]
embedded=mv(pd,fake)
physical=inner(embedded,mv(hd,embedded))/inner(embedded,embedded)
check(physical,-2*math.sqrt(2)/3)
out['software_11_16']={'MPF_polynomial':comb,'variance_upper':variance,
   'matrix_model_exact':exact,'step_estimates':approx,'MPF_matrix_estimate':estimate,
   'duplicate_physical_energy':physical.real,'qpt_5_settings':12**5,
   'qpt_10_settings':12**10}
payload=json.dumps({'date':'2026-10-13','independent_review':out},indent=2)+'\n'
(ROOT/'work/research/round71-cross-foundations-systems-results.json').write_text(payload)
print(payload)
