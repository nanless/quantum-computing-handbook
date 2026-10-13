"""Reconstruct evidence from saved inputs, without resampling/optimizing.
Run with the locked SDK environment. NPZ reads disallow pickle.
"""
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.stats import beta
import stim,pymatching
if not __debug__: raise RuntimeError('Run without -O')
OUT=Path(__file__).resolve().parent
cases=json.loads((OUT/'stim-matching-results.json').read_text())['cases'];qec=[]
for row in cases:
    stem=f"d{row['distance']}-p{row['noise_each']:g}"
    file=OUT/f'{stem}-samples.npz'
    assert hashlib.sha256(file.read_bytes()).hexdigest()==row['raw_sample_sha256']
    data=np.load(file,allow_pickle=False)
    det=np.unpackbits(data['detectors'],axis=1,bitorder='little')[:,:row['detectors']]
    obs=np.unpackbits(data['actual'],axis=1,bitorder='little')[:,:1]
    pred=np.unpackbits(data['prediction'],axis=1,bitorder='little')[:,:1]
    matcher=pymatching.Matching.from_detector_error_model(stim.DetectorErrorModel.from_file(OUT/f'{stem}.dem'))
    assert np.array_equal(matcher.decode_batch(det),pred)
    failed=np.any(obs!=pred,axis=1);assert np.array_equal(failed,data['failures'])
    k=int(failed.sum());n=len(failed);assert k==row['failures'] and n==row['shots']
    ci=[0 if k==0 else beta.ppf(.025,k,n-k+1),1 if k==n else beta.ppf(.975,k+1,n-k)]
    assert np.allclose(ci,row['exact_binomial_95'],rtol=1e-12,atol=1e-15)
    circuit=stim.Circuit.from_file(OUT/f'{stem}.stim')
    active={t.value for ins in circuit.flattened() if ins.name!='QUBIT_COORDS' for t in ins.targets_copy() if t.is_qubit_target}
    assert len(active)==2*row['distance']**2-1
    qec.append(dict(distance=row['distance'],noise_each=row['noise_each'],failures=k,actual_qubits=len(active)))
wave=np.loadtxt(OUT/'grape-amplitudes.csv',delimiter=',',skiprows=1)
assert np.allclose(wave[:,0],np.arange(80)*.5)
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
u=np.eye(2,dtype=complex)
for ux,uy in wave[:,1:3]:u=expm(-1j*.5*(2*np.pi*.005*Z+ux*X+uy*Y)/2)@u
trace=abs(np.trace((1j*X)@u))/2
record=json.loads((OUT/'grape-results.json').read_text())
assert abs(trace-record['optimized']['trace_overlap'])<1e-12
# Independent full 3D expansion checks leakage, not just two-level overlap.
a=np.diag(np.sqrt([1,2]),1);n=a.T@a;u3=np.eye(3,dtype=complex)
for ux,uy in wave[:,1:3]:
    h=-2*np.pi*.005*n+(-2*np.pi*.2)/2*(n@(n-np.eye(3)))+ux*(a+a.T)/2-1j*uy*(a-a.T)/2
    u3=expm(-1j*.5*h)@u3
leak=[float(abs(u3[2,j])**2) for j in (0,1)]
assert np.allclose(leak,record['three_level_final_leakage_for_basis_inputs'],atol=1e-12)
network=json.loads((OUT/'sequence-results.json').read_text());emissions=dict(network['emissions'])
assert len(emissions)==1000 and len(network['arrivals'])==len(network['acknowledgments'])==624
for seq,t in network['arrivals']:assert t-emissions[seq]==50_000_000
for seq,t in network['acknowledgments']:assert t-emissions[seq]==110_000_000
summary=dict(qec=qec,trace_overlap=float(trace),three_level_leakage=leak,
    network_received=len(network['arrivals']),network_ack_delay_ps=110_000_000,status='passed')
(OUT/'saved-results-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
