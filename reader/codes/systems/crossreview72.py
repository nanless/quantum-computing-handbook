#!/usr/bin/env python3
"""Independent saved-data reviews; run in systems SDK environment.
Root SDK re-execution separately: workflow env python this_script.py --case root.
No shared author-result files are overwritten; review reports use independent names.
"""
import argparse,hashlib,importlib.util,json,math
from pathlib import Path
import numpy as np
if not __debug__: raise RuntimeError('Run without -O')
REPO=Path(__file__).resolve().parents[2];OUT=REPO/'work/research'
def read(path):return json.loads((REPO/path).read_text())
def complex_matrix(x):
 a=np.asarray(x);return a[...,0]+1j*a[...,1]
def root():
 p=REPO/'codes/sdk/workflows/validate_workflows.py';spec=importlib.util.spec_from_file_location('review_root72',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 data={name:fn() for name,fn in [('obp',m.obp_case),('mpf',m.mpf_case),('cutting',m.cutting_case)]}
 # Independently expected pulled observable for Rx(.4) then Ry(pi/6).
 expected={'Z':math.sqrt(3)/2*math.cos(.4),'Y':math.sqrt(3)/2*math.sin(.4),'X':-.5}
 for label,c in data['obp']['pulled_paulis']:assert abs(c-expected[label])<1e-12
 assert data['obp']['zero_accepted_slice_regression_observed'] and data['obp']['guarded_retained_slices']==2
 # Product formula reconstructed from explicit 2x2 exponential rotations, no Qiskit synthesis.
 X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);psi=np.array([1.,0.],complex);values=[]
 def rotation(P,angle):return math.cos(angle)*np.eye(2)-1j*math.sin(angle)*P
 for k in [2,4]:
  dt=.7/k;V=rotation(X,dt/2)@rotation(Z,dt)@rotation(X,dt/2)
  final=np.linalg.matrix_power(V,k)@psi;values.append(float(np.vdot(final,Z@final).real))
 assert np.max(abs(np.array(values)-data['mpf']['values']))<1e-12
 assert np.allclose(data['cutting']['reconstructed'],[1,1,0],atol=1e-12)
 data['independent_reference']={'obp_coefficients':expected,'mpf_matrix_values':values,'cutting_Bell_Paulis':[1,1,0]}
 data['author_script_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();return data,m.json_value

def algorithms():
 r=read('codes/algorithms/sdk/round72-results.json')['cases'];phases=r['pyqsp']['result']['phases_radians'];errors=[]
 for x in [-1,-.75,-.5,0,.5,.75,1]:
  v=np.array([1+0j,0j]);W=np.array([[x,1j*math.sqrt(1-x*x)],[1j*math.sqrt(1-x*x),x]])
  for j,phi in enumerate(reversed(phases)):
   v=np.exp(1j*phi*np.array([1,-1]))*v
   if j<len(phases)-1:v=W@v
  errors.append(abs(v[0].imag-(.8*x*x*x-.3*x)))
 assert max(errors)<1e-12
 samples=np.load(REPO/'codes/algorithms/sdk/shadow-samples.npz',allow_pickle=False);bits,recipes=samples['bits'],samples['recipes'];means=[];variances=[]
 for axis in [0,1,2]:
  values=np.array([9*((1-2*int(row[0]))*(1-2*int(row[1]))) if int(basis[0])==int(basis[1])==axis else 0 for row,basis in zip(bits,recipes)])
  means.append(float(np.mean(values)));variances.append(float(np.var(values)))
 assert np.allclose(means,r['pennylane']['result']['estimates'][:3])
 A=np.array([[1.5,-.5],[-.5,1.5]]);sol=np.linalg.solve(A,[1,0]);prob=float(sol@sol);sol=sol/np.linalg.norm(sol)
 assert np.allclose(sol,r['cirq']['result']['conditional_amplitudes']) and abs(prob-r['cirq']['result']['success_exact'])<1e-12
 squeeze=math.log(2)/2;seq=[1/math.cosh(squeeze)]
 for k in range(1,10):seq.append(seq[-1]*(2*k-1)/(2*k)*math.tanh(squeeze)**2)
 p=[seq[n//2] if n%2==0 else 0 for n in range(20)]
 assert np.allclose(p,r['thewalrus']['result']['probabilities_0_to_19'])
 return {'phase_reverse_action_max_error':max(errors),'phase_points':7,'shadow_means':means,'shadow_variances':variances,'hhl_dense_inverse_success':prob,'hhl_dense_inverse_normalized':sol.tolist(),'walrus_mass':sum(p),'status':'passed'}

def foundations():
 sdk=read('codes/foundations/sdk/all-results.json')['cases'];r=read('codes/foundations/round72-results.json')['cases']
 q=sdk['qutip']['result'];actual=complex_matrix(q['mesolve_density_matrices']);expected=[]
 for t in q['times_us']:
  b=.25*math.exp(-.7*t);c=-1j*math.sqrt(3)/4*np.exp((-.35+.9j)*t);expected.append([[1-b,c],[c.conjugate(),b]])
 error=float(np.max(abs(actual-np.array(expected))));assert error<1e-8
 t=sdk['tomography']['result'];J=complex_matrix(t['low_shot_process']['choi'])
 partial=np.array([[J[0,0]+J[1,1],J[0,2]+J[1,3]],[J[2,0]+J[3,1],J[2,2]+J[3,3]]])
 assert np.linalg.eigvalsh(J).min()>-1e-10 and abs(np.trace(J)-2)<1e-10 and np.max(abs(partial-np.eye(2)))>.04
 bloch=[0.,0.,0.]
 for row in t['state_counts']:
  c=row['counts'];bloch[[2,0,1][row['metadata']['m_idx'][0]]]=(c.get('0',0)-c.get('1',0))/row['shots']
 radius=np.linalg.norm(bloch);x,y,z=np.array(bloch)/radius;rho=np.array([[(1+z)/2,(x-1j*y)/2],[(x+1j*y)/2,(1-z)/2]])
 fit_error=float(np.max(abs(rho-complex_matrix(t['state_fitted']))));assert fit_error<1e-12
 tele=r['04'];counts=tele['counts_c1_c0'];imb=(counts['00']+counts['10']-counts['01']-counts['11'])/sum(counts.values());coherence=-1j*math.sqrt(3)/4*imb
 assert abs(complex_matrix(tele['sample_ensemble'])[0,1]-coherence)<1e-12
 joint=complex_matrix(r['03']['joint_density']);pt=np.zeros((4,4),complex)
 for a in range(2):
  for b in range(2):
   for c in range(2):
    for d in range(2):pt[2*a+d,2*c+b]=joint[2*a+b,2*c+d]
 low=float(np.linalg.eigvalsh(pt).min());assert abs(low-r['03']['minimum_eigenvalue_formula'])<1e-12
 return {'mesolve_analytic_matrix_max_error':error,'jump_probability':.25*(1-math.exp(-2.8)),
  'low_shot_CP_min_eigenvalue':float(np.linalg.eigvalsh(J).min()),'low_shot_TP_output_partial_error':float(np.max(abs(partial-np.eye(2)))),
  'state_raw_radius':float(radius),'state_independent_radial_error':fit_error,'teleport_missing_Z_expected_coherence':[coherence.real,coherence.imag],'partial_transpose_min_eigenvalue':low,'status':'passed'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['root','saved'],required=True);args=ap.parse_args()
 if args.case=='root':
  result,encoder=root();(OUT/'round72-systems-cross-root-sdk.json').write_text(json.dumps(result,indent=2,default=encoder)+'\n')
 else:
  for name,fn in [('algorithms',algorithms),('foundations',foundations)]:
   result=fn();(OUT/f'round72-systems-cross-{name}.json').write_text(json.dumps(result,indent=2)+'\n')
 print(args.case,'passed')
