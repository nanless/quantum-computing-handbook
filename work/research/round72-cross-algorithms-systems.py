"""Independent reviewer replay of S72 evidence, not author functions or new sampling."""
import json,math,pathlib
import numpy as np
from scipy.linalg import expm
from scipy.stats import binom
root=pathlib.Path(__file__).resolve().parents[2]; d=root/'codes/systems/sdk'; report={}
# Count failures from bits and verify CI tail probabilities directly as binomial events.
rows=json.loads((d/'stim-matching-results.json').read_text())['cases']; out=[]
for r in rows:
    stem=f"d{r['distance']}-p{r['noise_each']:g}"; z=np.load(d/(stem+'-samples.npz'),allow_pickle=False)
    actual=np.unpackbits(z['actual'],axis=1,bitorder='little')[:,:1]
    predicted=np.unpackbits(z['prediction'],axis=1,bitorder='little')[:,:1]
    k=int(np.any(actual!=predicted,axis=1).sum()); N=len(actual); assert k==r['failures']
    lo,hi=r['exact_binomial_95']
    if k: assert abs(binom.sf(k-1,N,lo)-.025)<1e-10
    assert abs(binom.cdf(k,N,hi)-.025)<1e-10
    if k==0: assert abs(hi-(1-.025**(1/N)))<1e-14
    out.append({'distance':r['distance'],'N':N,'failures':k,'ci':[lo,hi]})
report['qec']=out
# Same saved waveform, independently reconstruct 2D and 3D all-slot products.
w=np.loadtxt(d/'grape-amplitudes.csv',delimiter=',',skiprows=1); assert w.shape==(80,5)
X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1])
a=np.array([[0,1,0],[0,0,np.sqrt(2)],[0,0,0]],complex); number=a.conj().T@a
u2=np.eye(2,dtype=complex);u3=np.eye(3,dtype=complex)
for ux,uy in w[:,1:3]:
    u2=expm(-.5j*(2*np.pi*.005*Z+ux*X+uy*Y)/2)@u2
    h3=-2*np.pi*.005*number+(-2*np.pi*.2)/2*(number@number-number)+ux*(a+a.conj().T)/2-1j*uy*(a-a.conj().T)/2
    assert np.allclose(h3,h3.conj().T)
    u3=expm(-.5j*h3)@u3
assert np.allclose(u2.conj().T@u2,np.eye(2),atol=1e-12)
assert np.allclose(u3.conj().T@u3,np.eye(3),atol=1e-12)
g=abs(np.trace(1j*X@u2))/2; Favg=(2*g*g+1)/3
leak=abs(u3[2,:2])**2; saved=json.loads((d/'grape-results.json').read_text())
assert abs(g-saved['optimized']['trace_overlap'])<1e-12
assert np.allclose(leak,saved['three_level_final_leakage_for_basis_inputs'],atol=1e-12)
# Lowest-block drift differs from delta Z/2 by only scalar -delta/2.
h0=-2*np.pi*.005*number+(-2*np.pi*.2)/2*(number@number-number)
assert np.allclose(h0[:2,:2],2*np.pi*.005*(Z-np.eye(2))/2)
assert np.allclose((-1j*(a-a.conj().T)/2)[:2,:2],Y/2)
report['control']={'g':float(g),'F_avg':float(Favg),'leakage_0_1':leak.tolist(),'lowest_block_y_control_matches':True}
# Event pairing and model's explicit units, no source simulator reuse.
net=json.loads((d/'sequence-results.json').read_text()); starts=dict(net['emissions']); received=dict(net['arrivals']); ack=dict(net['acknowledgments'])
assert starts[999]==99_900_000 and set(received)==set(ack)
assert all(received[k]-starts[k]==50_000_000 for k in received)
assert all(ack[k]-received[k]==60_000_000 for k in received)
assert net['events_executed']==1000+2*len(received)==2248
report['network']={'received':len(received),'loss_expected':10**(-2/10),'roundtrip_us':110.,'last_emission_us':99.9}
# Synthetic FIFO sequence independent author implementation.
fin=0;lat=[]
for i in range(20): fin=max(float(i),fin)+(4 if i==2 else .8); lat.append(fin-i)
assert sum(t>2+1e-12 for t in lat)==10 and max(lat)==4
report['queue']={'misses':10,'max_latency_us':4.,'latencies_us':lat}
report['status']='passed'; path=root/'work/research/round72-cross-algorithms-systems-results.json';path.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
