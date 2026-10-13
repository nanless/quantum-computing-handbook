"""Independent reviewer calculations, standard library; no original foundations helper import."""
if not __debug__:
    raise RuntimeError('Independent numerical review requires assertions; run without -O.')

import sys,math,cmath,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'codes/algorithms'))
from round71_checks import close,mul,mv,adj,eye,inner,matclose,entropy

def tensor(v,w):return [x*y for x in v for y in w]
def kron(a,b):return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
                     for i in range(len(a)) for k in range(len(b))]
def outer(v):return [[x*y.conjugate() for y in v] for x in v]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def scale(s,a):return [[s*z for z in row] for row in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def kraus(ks,rho):
 out=[[0j]*len(rho) for _ in rho]
 for k in ks:out=add(out,mul(k,mul(rho,adj(k))))
 return out
I=eye(2);X=[[0j,1+0j],[1+0j,0j]];Z=[[1+0j,0j],[0j,-1+0j]]
H=scale(1/math.sqrt(2),[[1+0j,1+0j],[1+0j,-1+0j]])
Y=[[0j,-1j],[1j,0j]]
plus=[1/math.sqrt(2)+0j]*2
result={}
# 00: all bytes through units, and new exercise factors.
for n,u in [(20,20),(30,30)]:close((16*2**n)/2**u,16)
assert 16*4**20==16*2**40 and 16*4**30==16*2**60
assert (16*2**22)//(16*2**20)==4 and (16*4**22)//(16*4**20)==16
result['00']={'ket22_over20':4,'rho22_over20':16}
# 01: recover ket and expectation, and transpose counterexample.
w=scale(1/math.sqrt(2),[[1+0j,1+0j],[1j,-1j]])
c=mv(adj(w),[1+0j,0j]);matclose(mul(adj(w),mul(Z,w)),X)
for actual,expected in zip(mv(w,c),[1,0]):close(actual,expected)
close(inner(c,mv(X,c)),1);close(inner(c,mv(Z,c)),0)
result['01']={'passive_mean':1,'active_fixed_Z_mean':0}
# 02: direct output density element sum and state-dependent repeat probability.
m0=[[math.sqrt(.75)+0j,0j],[0j,.5+0j]]
m1=[[.5+0j,0j],[0j,math.sqrt(.75)+0j]]
rho=kraus([m0,m1],outer(plus));close(tr(mul(rho,rho)),7/8)
r0=mul(m0,mul(outer(plus),adj(m0)));p0=tr(r0).real
close(p0,.5);conditional=scale(1/p0,r0)
close(tr(kraus([m0],conditional)),5/8)
result['02']={'purity':tr(mul(rho,rho)).real,'repeat0_given0':5/8}
# 03: eigenprojectors rather than the author's specified analytic eigenvectors.
psi=[1/math.sqrt(3)+0j,1j/math.sqrt(3),0j,1/math.sqrt(3)+0j]
r=outer(psi)
ra=[[sum(r[2*i+b][2*j+b] for b in (0,1)) for j in (0,1)] for i in (0,1)]
rb=[[sum(r[2*a+i][2*a+j] for a in (0,1)) for j in (0,1)] for i in (0,1)]
lam=[(3+math.sqrt(5))/6,(3-math.sqrt(5))/6]
reconstruction=[0j]*4;terms=[]
for j in range(2):
 projector=scale(1/(lam[j]-lam[1-j]),add(ra,scale(-lam[1-j],I)))
 matclose(mul(projector,projector),projector)
 u=mv(projector,[1+0j,0j]);u=[v/math.sqrt(inner(u,u).real) for v in u]
 v=[sum(u[a].conjugate()*psi[2*a+b] for a in (0,1))/math.sqrt(lam[j]) for b in (0,1)]
 close(inner(v,v),1)
 for a,b in zip(mv(rb,v),v):close(a,lam[j]*b)
 term=[math.sqrt(lam[j])*z for z in tensor(u,v)]
 reconstruction=[a+b for a,b in zip(reconstruction,term)]
 terms.append(term)
for a,b in zip(reconstruction,psi):close(a,b)
result['03']={'weights':lam,'entropy':entropy(lam),'spectral_projector_reconstruction':True}
# 04: directly contract Alice's Bell bra with resource, without CNOT/H implementation.
bell_vectors=[[1/math.sqrt(2),0,0,1/math.sqrt(2)],
              [0,1/math.sqrt(2),1/math.sqrt(2),0],
              [1/math.sqrt(2),0,0,-1/math.sqrt(2)],
              [0,1/math.sqrt(2),-1/math.sqrt(2),0]]
resource=[1/math.sqrt(2),0,0,1/math.sqrt(2)]
inputs=[resource,[math.sqrt(3)/2,0j,0j,.5j],tensor(plus,[math.sqrt(3)/2,.5j])]
for rq in inputs:
 joint=tensor(rq,resource)
 for label,bra in enumerate(bell_vectors):
  raw=[sum(bra[2*q+a]*joint[8*r+4*q+2*a+b] for q in (0,1) for a in (0,1))
       for r in (0,1) for b in (0,1)]
  close(inner(raw,raw),.25)
  correction=I
  if label&1:correction=X
  if label&2:correction=mul(Z,correction)
  corrected=mv(kron(I,correction),[2*z for z in raw])
  matclose(outer(corrected),outer(rq)) # Bell-bra sign may be global.
result['04']={'inputs':3,'direct_Bell_branches_checked':12}
# 05: verify linear maps on all four matrix units, including off-diagonal units.
p,gamma=.25,.36
ksF=[scale(math.sqrt(1-p),I),scale(math.sqrt(p),X)]
ksA=[[[1+0j,0j],[0j,math.sqrt(1-gamma)+0j]],[[0j,math.sqrt(gamma)+0j],[0j,0j]]]
for a in (0,1):
 for b in (0,1):
  unit=[[complex(i==a and j==b) for j in (0,1)] for i in (0,1)]
  diff=add(kraus(ksA,kraus(ksF,unit)),scale(-1,kraus(ksF,kraus(ksA,unit))))
  matclose(diff,scale(p*gamma*complex(a==b),Z))
result['05']={'p_gamma':p*gamma,'four_matrix_units_checked':True}
# Q1: use joint density, local POVM effects to obtain each joint event.
Pplus=outer(plus);Pminus=outer([plus[0],-plus[1]])
P0=[[1+0j,0j],[0j,0j]];P1=[[0j,0j],[0j,1+0j]]
rows=[]
for phase in [0,math.pi/3,math.pi/2,math.pi]:
 rho=outer([1/math.sqrt(2)+0j,0j,0j,cmath.exp(1j*phase)/math.sqrt(2)])
 probs=[]
 for out in (P0,P1):
  effective=mul(H,mul(out,H))
  for record in (Pplus,Pminus):probs.append(tr(mul(kron(effective,record),rho)).real)
 expected=[(1+math.cos(phase))/4,(1-math.cos(phase))/4,(1-math.cos(phase))/4,(1+math.cos(phase))/4]
 for a,b in zip(probs,expected):close(a,b)
 rows.append(probs)
result['q1']={'POVM_density_probabilities':rows}
# Q2: covariance/commutator for many pure and mixed Bloch vectors, not just real psi.
for rx,ry,rz in [(1/math.sqrt(2),0,1/math.sqrt(2)),(0,1,0),(.2,.3,.4),(0,0,0)]:
 rho=scale(.5,add(I,add(scale(rx,X),add(scale(ry,Y),scale(rz,Z)))))
 mx=tr(mul(X,rho)).real;mz=tr(mul(Z,rho)).real
 covariance=tr(mul(scale(.5,add(mul(X,Z),mul(Z,X))),rho)).real-mx*mz
 comm=tr(mul(add(mul(X,Z),scale(-1,mul(Z,X))),rho))
 lhs=(1-mx*mx)*(1-mz*mz);rhs=covariance**2+abs(comm)**2/4
 close(covariance,-rx*rz);assert lhs+1e-10>=rhs
 close(lhs-rhs,1-rx*rx-ry*ry-rz*rz)
result['q2']={'Bloch_states_checked':4,'bound_slack_equals_1_minus_Bloch_norm_squared':True}
print(json.dumps(result,indent=2,ensure_ascii=False))
