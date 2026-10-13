"""Systems73 independent algorithm evidence review; no author functions are called."""
import json,math
from pathlib import Path
from fractions import Fraction
import numpy as np
if not __debug__:raise RuntimeError('Assertions must be enabled')
OUT=Path(__file__).resolve().parent; ALG=OUT.parents[1]/'algorithms'/'sdk73'
r=json.loads((ALG/'results-all.json').read_text());records={}
def decode(x):return np.array(x['real'])+1j*np.array(x['imag'])
# Independent scalar finite Fourier coefficient Q_yz uses Walsh parity, not author HT/F matrices.
hh=[]
for item in r['cases']['hhl']['cases']:
    raw=np.load(ALG/f"hhl-{item['name']}-t{item['phase_bits']}.npz");a=raw['A'];b=raw['b'];joint=raw['joint'];t=item['phase_bits'];M=2**t
    assert abs(np.vdot(joint,joint)-1)<1e-10
    vals,vec=np.linalg.eigh(a);ref=np.zeros(joint[:,:,1].shape,complex);ref_zero=np.zeros(joint[:,:,0].shape,complex)
    beta=vec.conj().T@b;ry=raw['rotation_amplitudes']
    x=np.arange(M);walsh=np.array([[(-1)**int((xx&z).bit_count()) for z in range(M)] for xx in range(M)])
    for i,lam in enumerate(vals):
        phase=np.exp(2j*np.pi*x*lam/(2*item['scale']))
        q=np.array([[sum(phase[xx]*np.exp(-2j*np.pi*xx*y/M)*walsh[xx,z] for xx in range(M))/M for z in range(M)] for y in range(M)])
        q0=q[:,0];ref+=beta[i]*np.outer(q.conj().T@(ry*q0),vec[:,i]);ref_zero+=beta[i]*np.outer(q.conj().T@(np.sqrt(1-ry**2)*q0),vec[:,i])
    err=float(max(np.max(abs(ref-joint[:,:,1])),np.max(abs(ref_zero-joint[:,:,0]))));assert err<1e-11
    p=float(np.sum(abs(ref)**2));pc=float(np.sum(abs(ref[0])**2));rho=np.einsum('ys,yt->st',ref,ref.conj())/p
    target=np.linalg.solve(a,b);target/=np.linalg.norm(target)
    fidelity=math.sqrt(float(np.vdot(target,rho@target).real));purity=float(np.trace(rho@rho).real)
    assert abs(p-item['flag_success'])<1e-12 and abs(pc-item['phase_zero_and_flag_success'])<1e-12
    assert abs(fidelity-item['mixed_root_fidelity'])<1e-12 and abs(purity-item['mixed_purity'])<1e-12
    assert np.max(abs(rho-decode(item['rho_given_flag'])))<1e-12
    if item.get('shots'):
        samples=np.load(ALG/f"hhl-{item['name']}-t{item['phase_bits']}-samples.npz");ok=samples['flag'][:,0]==1;clean=ok&np.all(samples['phase']==0,axis=1)
        assert int(ok.sum())==item['flag_count'] and int(clean.sum())==item['clean_count'] and int((ok&~clean).sum())==item['garbage_count']
    hh.append(dict(case=item['name'],bits=t,all_flag_amplitude_error=err,p_flag=p,p_clean=pc,root_fidelity=fidelity,purity=purity))
records['hhl']=hh
# Exact rational SKW steps, directly sum amplitudes at each position, then permute directional neighbours.
raw=np.load(ALG/'walk-states-samples.npz');v=[[Fraction(1,8) for x in range(16)] for j in range(4)];prob=[]
for step in range(17):
    arr=np.array(v,dtype=float).ravel();assert np.max(abs(arr-raw['states'][step]))<1e-12
    p=sum(v[j][0]**2 for j in range(4));prob.append(str(p))
    c=[[Fraction(0) for x in range(16)] for j in range(4)]
    for pos in range(16):
        if pos==0:
            for j in range(4):c[j][pos]=-v[j][pos]
        else:
            mean=sum(v[j][pos] for j in range(4))/2
            for j in range(4):c[j][pos]=mean-v[j][pos]
    v=[[c[j][x^(1<<(3-j))] for x in range(16)] for j in range(4)]
assert prob[4]=='25/64' and prob[8]=='1/256'
ints=raw['samples']@np.array([8,4,2,1]);counts=np.bincount(ints,minlength=16);assert np.array_equal(counts,r['cases']['walk']['histogram'])
records['walk']=dict(all_17_exact_marked_probabilities=prob,sample_counts_rebuilt=True)
# Selector extraction checks actual 8D amplitudes and all columns, not just target probability.
raw=np.load(ALG/'qsvt-matrices.npz');a=raw['A'];u=raw['U'];poly=.8*(a@a@a)-.3*a
assert np.max(abs(poly-raw['target']))<1e-15
h=np.array([[1,1],[1,-1]])/np.sqrt(2);Hs=np.kron(h,np.eye(4));controlled=np.zeros((8,8),complex);controlled[:4,:4]=u;controlled[4:,4:]=u.conj();constructed=Hs@controlled@Hs
assert np.max(abs(constructed-raw['selector_unitary']))<1e-12
assert np.max(abs(constructed[:2,:2]-poly))<2e-9
assert np.max(abs(raw['actual_state']-constructed[:,0]))<1e-12
p=float(np.sum(abs(raw['actual_state'][:2])**2));assert abs(p-.00444112)<1e-10
records['qsvt']=dict(target=poly.tolist(),selector_all_column_error=float(np.max(abs(constructed-raw['selector_unitary']))),both_ancilla_success=p)
# Four measurement branches from diagonal CZ signs and explicit bras, independent of dynamic SDK.
item=r['cases']['mbqc'];a=item['alpha'];b=item['beta'];inp=decode(item['input']);target=decode(item['target'])
graph=np.zeros((2,2,2),complex)
for i in range(2):
 for j in range(2):
  for k in range(2):graph[i,j,k]=inp[i]*(-1)**(i*j+j*k)/2
branches=[]
for m0 in range(2):
 for m1 in range(2):
  bra0=np.array([1,(-1)**m0*np.exp(-1j*a)])/np.sqrt(2);bra1=np.array([1,(-1)**m1*np.exp(-1j*((-1)**m0)*b)])/np.sqrt(2)
  out=np.einsum('i,j,ijk->k',bra0,bra1,graph);p=float(np.vdot(out,out).real);out/=np.sqrt(p)
  if m1:out=out[::-1]
  if m0:out[1]*=-1
  f=float(abs(np.vdot(target,out)));assert abs(p-.25)<1e-12 and abs(f-1)<1e-12
  branches.append(dict(m0=m0,m1=m1,p=p,root_fidelity=f))
raw=np.load(ALG/'mbqc-samples.npz');assert not raw['verification'].any();hist=np.bincount(2*raw['m0'][:,0]+raw['m1'][:,0],minlength=4);assert np.array_equal(hist,item['branch_counts'])
records['mbqc']=dict(branches=branches,raw_counts=hist.tolist(),raw_verification_failures=0)
result=dict(status='passed',reviewer='systems73',scope='independent archived matrices/flag branches, rational walk, all selector columns, four MBQC contractions; no author functions or rerun overwritten',records=records)
(OUT/'crossreview-algorithms-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
