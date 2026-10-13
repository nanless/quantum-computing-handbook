#!/usr/bin/env python3
"""Full PNA anti-noise observable plus independent dense noisy evolution."""
import json,pathlib,math,time,importlib.metadata
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp,PauliList
from qiskit_aer.noise import PauliLindbladError
from qiskit_aer.primitives import EstimatorV2
from qiskit_aer import AerSimulator
from qiskit_addon_pna import generate_noise_mitigating_observable
HERE=pathlib.Path(__file__).resolve().parent

def main():
 if not __debug__:raise RuntimeError('Run without -O')
 start=time.perf_counter();X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);I=np.eye(2);H=(X+Z)/math.sqrt(2)
 paulis={'I':I,'X':X,'Y':Y,'Z':Z};pm=lambda label:np.kron(paulis[label[0]],paulis[label[1]])
 rotation=lambda P,a:math.cos(a/2)*I-1j*math.sin(a/2)*P
 CX=np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]],complex) # q0 control, q1 target; orderq1q0
 pre=np.kron(H,I)@np.kron(rotation(X,.31),rotation(Y,.63))
 post=np.kron(rotation(X,.7),rotation(Y,.2))@CX
 labels=['XI','IZ','XX'];rates=np.array([.015,.008,.011]);obs=SparsePauliOp('XX');O=pm('XX')
 def circuit(model_rates=None):
  qc=QuantumCircuit(2);qc.ry(.63,0);qc.rx(.31,1);qc.h(1)
  if model_rates is not None:qc.append(PauliLindbladError(PauliList(labels),model_rates),[0,1])
  qc.cx(0,1);qc.ry(.2,0);qc.rx(.7,1)
  return qc
 noisy=circuit(rates);ideal=circuit();mitigating=generate_noise_mitigating_observable(noisy,obs,max_err_terms=64,max_obs_terms=64,atol=0,search_step=1,num_processes=1)
 v=pre@np.array([1,0,0,0],complex);rho=np.outer(v,v.conj())
 for label,r in zip(labels,rates):
  probability=-np.expm1(-2*r)/2;P=pm(label);rho=(1-probability)*rho+probability*P@rho@P
 rho=post@rho@post.conj().T;v0=post@v;ideal_value=float(np.vdot(v0,O@v0).real)
 noisy_value=float(np.trace(O@rho).real);corrected=float(np.trace(mitigating.to_matrix()@rho).real)
 assert abs(corrected-ideal_value)<2e-10,(corrected,ideal_value)
 estimator=EstimatorV2(options={'backend_options':{'method':'density_matrix','max_parallel_threads':1},'default_precision':0.0})
 sdk=[float(np.asarray(x.data.evs)) for x in estimator.run([(ideal,obs),(noisy,obs),(noisy,mitigating)]).result()]
 assert np.max(abs(np.array(sdk)-[ideal_value,noisy_value,corrected]))<1e-10
 # Independently pull O back through post, invert the Pauli eigenvalues, push forward.
 corrected_mid=post.conj().T@O@post
 for label,r in zip(labels[::-1],rates[::-1]):
  P=pm(label);commuting=(corrected_mid+P@corrected_mid@P)/2;anticommuting=(corrected_mid-P@corrected_mid@P)/2
  corrected_mid=commuting+np.exp(2*r)*anticommuting
 exact_observable=post@corrected_mid@post.conj().T
 assert np.max(abs(exact_observable-mitigating.to_matrix()))<1e-10
 wrong=generate_noise_mitigating_observable(circuit(rates*1.25),obs,max_err_terms=64,max_obs_terms=64,atol=0,search_step=1,num_processes=1)
 model_mismatch=float(np.trace(wrong.to_matrix()@rho).real)
 coeffs={label:float(c.real) for label,c in mitigating.to_list()}
 # Separate measurement circuit for each Pauli: no hidden covariance assumption.
 budget=20000;l1=sum(abs(c) for c in coeffs.values());allocation={label:max(1,int(budget*abs(c)/l1)) for label,c in coeffs.items()}
 allocation[max(allocation,key=allocation.get)]+=budget-sum(allocation.values())
 backend=AerSimulator(method='density_matrix',max_parallel_threads=1);sample_records=[];sample_value=0.;sample_variance=0.
 for index,(label,c) in enumerate(coeffs.items()):
  measured=noisy.copy()
  for q,axis in enumerate(label[::-1]):
   if axis=='X':measured.h(q)
   elif axis=='Y':measured.sdg(q);measured.h(q)
  measured.measure_all();shots=allocation[label];counts=backend.run(measured,shots=shots,seed_simulator=730401+index).result().get_counts()
  mu=sum(f*(-1)**sum(int(bit) for bit,axis in zip(bitstring,label) if axis!='I') for bitstring,f in counts.items())/shots
  variance=(1-mu*mu)/(shots-1);sample_value+=c*mu;sample_variance+=c*c*variance
  sample_records.append({'pauli':label,'coefficient':c,'shots':shots,'seed':730401+index,'counts':counts,'estimate':mu,'dense_noisy_reference':float(np.trace(pm(label)@rho).real)})
 sample_se=math.sqrt(sample_variance);assert abs(sample_value-ideal_value)<6*sample_se
 finite={'budget':budget,'estimate':sample_value,'standard_error':sample_se,'independent_pauli_circuits':True,'allocation':'integer N_j proportional to |c_j|, final remainder assigned to largest term','records':sample_records}
 (HERE/'pna-observable.json').write_text(json.dumps(coeffs,indent=2)+'\n')
 result={'status':'passed','versions':{p:importlib.metadata.version(p) for p in ['qiskit-addon-pna','qiskit-aer','pauli-prop']},'basis':'q1 q0, q0 control','noise_location':'beforeCX; exactly one noise layer','generators':labels,'rates':rates.tolist(),'ideal':ideal_value,'noisy':noisy_value,'mitigated':corrected,'sdk_estimator':sdk,'mitigating_terms':len(mitigating),'coefficients':coeffs,'finite_shot':finite,'coefficient_l1':float(sum(abs(mitigating.coeffs))),'operator_spectral_norm':float(np.linalg.norm(mitigating.to_matrix(),2)),'observable_dense_error':float(np.max(abs(exact_observable-mitigating.to_matrix()))),'miscalibration_factor':1.25,'miscalibrated_value':model_mismatch,'miscalibration_bias':abs(model_mismatch-ideal_value),'elapsed_seconds':time.perf_counter()-start,'scope':'full PNA pipeline exact local model; no hardware noise learning, finite-shot allocation and independent-circuit variance included'}
 (HERE/'pna-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
