#!/usr/bin/env python3
"""Actual SLC bounds/scales and independent channel-removal bias checks."""
import json,pathlib,time,importlib.metadata
import numpy as np
from qiskit import QuantumCircuit,transpile
from qiskit.quantum_info import Pauli,SparsePauliOp,PauliLindbladMap,QubitSparsePauliList,DensityMatrix
from qiskit_addon_slc.utils import generate_noise_model_paulis
from qiskit_addon_slc.bounds import compute_forward_bounds,compute_backward_bounds,merge_bounds,compute_local_scales
from samplomatic.transpiler import generate_boxing_pass_manager
from samplomatic.utils import find_unique_box_instructions,get_annotation
from samplomatic.annotations import InjectNoise
from qiskit_aer.noise import PauliLindbladError
from qiskit_aer import AerSimulator
from samplomatic import build
from qiskit_mitigation import PEC
HERE=pathlib.Path(__file__).resolve().parent

def main():
 if not __debug__:raise RuntimeError('Run without -O')
 started=time.perf_counter();n=3;circuit=QuantumCircuit(n)
 for step in range(2):
  circuit.rx(.22+.04*step,range(n));circuit.barrier();circuit.cx(0,1);circuit.cx(1,2);circuit.barrier()
 observable=Pauli('IZI')
 boxing=generate_boxing_pass_manager(inject_noise_targets='gates',inject_noise_strategy='individual_modification',inject_noise_site='after',twirling_strategy='active',remove_barriers='after_stratification')
 circuit=transpile(circuit,basis_gates=['rz','sx','x','cx'],optimization_level=0)
 boxed=boxing.run(circuit);unique=find_unique_box_instructions(boxed)
 paulis=generate_noise_model_paulis(unique)
 rng=np.random.default_rng(73031);maps={ref:PauliLindbladMap.from_components(rng.uniform(.002,.008,len(ps)),QubitSparsePauliList.from_sparse_list(ps.to_sparse_list(),ps.num_qubits)) for ref,ps in paulis.items()}
 forward=compute_forward_bounds(boxed,paulis,observable,evolution_max_terms=256,eigval_max_qubits=3,atol=1e-12,num_processes=1)
 backward=compute_backward_bounds(boxed,paulis,evolution_max_terms=256,num_processes=1)
 merged=merge_bounds(boxed,forward,backward,maps)
 zero=np.zeros(2**n,complex);zero[0]=1;rho0=np.outer(zero,zero.conj());ideal=float(DensityMatrix.from_instruction(circuit).expectation_value(observable).real)
 def physical_output(mask=None,only_residual=False):
  rho=DensityMatrix(rho0)
  for item in boxed.data:
   op=item.operation
   if op.name=='barrier':continue
   qargs=[boxed.find_bit(q).index for q in item.qubits]
   if hasattr(op,'body'):
    rho=rho.evolve(op.body,qargs=qargs)
    ann=get_annotation(op,InjectNoise)
    if ann is not None:
     noise=maps[ann.ref];ps=noise.get_qubit_sparse_pauli_list_copy().to_pauli_list();rates=np.asarray(noise.rates)
     if mask is not None and only_residual:rates=rates*(1-mask[ann.modifier_ref])
     # Noise-model local indices use global canonical ascending order;
     # the box body's order can instead be [target, control].
     rho=rho.evolve(PauliLindbladError(ps,rates).to_quantumchannel(),qargs=sorted(qargs))
   else:rho=rho.evolve(op,qargs=qargs)
  return float(rho.expectation_value(observable).real)
 noisy=physical_output();records=[]
 for tolerance in [0.,.01,.03,.06]:
  mask,cost,bias=compute_local_scales(boxed,merged,maps,bias_tolerance=tolerance)
  assert all(set(np.unique(v))<=set([0.,1.]) for v in mask.values())
  residual=physical_output(mask,True);observed=abs(residual-ideal)
  assert observed<=bias+1e-10,(observed,bias)
  total_rate=0;kept=0
  for item in boxed.data:
   ann=get_annotation(item.operation,InjectNoise) if hasattr(item.operation,'body') else None
   if ann is not None:total_rate+=float(np.dot(mask[ann.modifier_ref],maps[ann.ref].rates));kept+=int(sum(mask[ann.modifier_ref]))
  assert abs(np.exp(4*total_rate)-cost)<1e-10
  records.append({'bias_tolerance':tolerance,'mask':{k:v.tolist() for k,v in mask.items()},'cost_gamma_squared':cost,'bias_bound':bias,'exact_residual_value':residual,'observed_bias':observed,'mitigated_occurrences':kept})
 # Known release edge: all-zero mask should have cost1; 0.1.0 indexes an empty list.
 try:compute_local_scales(boxed,merged,maps,bias_tolerance=10.)
 except IndexError as error:all_zero_regression=str(error)
 else:all_zero_regression=None
 # Explicit local guard: no inverse channel means empty selection and cost exactly1.
 zero_selection={get_annotation(i.operation,InjectNoise).modifier_ref:np.zeros(len(maps[get_annotation(i.operation,InjectNoise).ref])) for i in boxed.data if hasattr(i.operation,'body') and get_annotation(i.operation,InjectNoise) is not None}
 occurrence_refs={a.modifier_ref:a.ref for a in [get_annotation(i.operation,InjectNoise) for i in boxed.data if hasattr(i.operation,'body')] if a is not None}
 zero_bound=sum(float(np.dot(bound.rates,(1-np.exp(-2*maps[occurrence_refs[key]].rates))/2)) for key,bound in merged.items())
 zero_guard={'bias_tolerance':10.,'mask':{k:v.tolist() for k,v in zero_selection.items()},'cost_gamma_squared':1.,'bias_bound':zero_bound,'exact_residual_value':noisy,'observed_bias':abs(noisy-ideal),'mitigated_occurrences':0}
 assert zero_guard['observed_bias']<=zero_bound+1e-10
 template,samplex=build(boxed)
 # Full generated randomizations -> physical Aer circuits -> SDK PEC postprocess.
 annotations=[get_annotation(i.operation,InjectNoise) for i in boxed.data if hasattr(i.operation,'body') and get_annotation(i.operation,InjectNoise) is not None]
 batches=[];raw=[];backend=AerSimulator(method='density_matrix',max_parallel_threads=1)
 for record in [records[0],records[-1],zero_guard]:
  selection={k:np.asarray(v) for k,v in record['mask'].items()}
  output=samplex.sample({'pauli_lindblad_maps':maps,'local_scales':{k:-v for k,v in selection.items()}},num_randomizations=1024,rng=730101+len(batches))
  values=output['parameter_values'];signs=output['pauli_signs'];circuits=[]
  for params in values:
   bound=template.assign_parameters(params);physical=QuantumCircuit(n)
   for item in bound.data:
    op=item.operation;qargs=[bound.find_bit(q).index for q in item.qubits]
    if op.name=='barrier':
     # The R debug marker is immediately after this noisy entangler.
     label=op.label or ''
     if label.startswith('R') and '@inject_noise=' in label:
      index=int(label[1:label.index('@')]);ann=annotations[index];model=maps[ann.ref]
      physical.append(PauliLindbladError(model.get_qubit_sparse_pauli_list_copy().to_pauli_list(),model.rates),sorted(qargs))
    else:physical.append(op,qargs)
   physical.measure_all();circuits.append(physical)
  shots=64;seed=730201+len(batches)
  counts=backend.run(circuits,shots=shots,seed_simulator=seed).result().get_counts()
  data=np.zeros((len(values),1,shots,n),dtype=bool)
  for j,count in enumerate(counts):
   cursor=0
   for bitstring,frequency in count.items():
    data[j,0,cursor:cursor+frequency]=[bool(int(b)) for b in bitstring[::-1]];cursor+=frequency
   assert cursor==shots
  gamma=float(np.sqrt(record['cost_gamma_squared']))
  pub=PEC.compute_expectation_value_pec({'_meas':data,'pauli_signs':signs[:,None,:]},[SparsePauliOp(observable)],gamma,meas_bases=['ZZZ'])
  signed=(-1.)**signs.sum(axis=1);per_randomization=gamma*signed*(1-2*data[:,0,:,1].mean(axis=1))
  estimate=float(per_randomization.mean());cluster_se=float(per_randomization.std(ddof=1)/np.sqrt(len(values)))
  sdk_estimate=float(pub.data.evs[0]);assert abs(estimate-sdk_estimate)<1e-12
  raw_stds=float(pub.data.stds[0]);flat_variance=(gamma*gamma-estimate*estimate)/(len(values)*shots)
  assert abs(raw_stds-flat_variance)<1e-12 # 0.1.1 nonbroadcast branch puts variance in stds.
  clustered=PEC.compute_expectation_value_pec({'_meas':data,'pauli_signs':signs[:,None,:]},SparsePauliOp(observable),gamma,param_shape=(),param_basis_pairs=[((),'ZZZ')],broadcast_obs_and_params=True)
  assert abs(float(np.asarray(clustered.data.twirl_stds))-cluster_se*np.sqrt((len(values)-1)/len(values)))<1e-12
  assert abs(estimate-record['exact_residual_value'])<6*cluster_se+1e-6
  batches.append({'bias_tolerance':record['bias_tolerance'],'num_randomizations':len(values),'shots_per_randomization':shots,'seed':seed,'gamma':gamma,'estimate':estimate,'sdk_estimate':sdk_estimate,'cluster_standard_error':cluster_se,'sdk_raw_stds_field':raw_stds,'independent_flat_variance':flat_variance,'sdk_broadcast_cluster_se_ddof0':float(np.asarray(clustered.data.twirl_stds)),'reference':record['exact_residual_value'],'reference_error':abs(estimate-record['exact_residual_value']),'note':'cluster SE treats each randomization as independent; shots within its circuit share the sampled inverse channel'})
  raw.append({'parameters':values.tolist(),'pauli_signs':signs.tolist(),'counts':counts})
 (HERE/'slc-randomizations-counts.json').write_text(json.dumps(raw,indent=2)+'\n')
 result={'status':'passed','versions':{p:importlib.metadata.version(p) for p in ['qiskit-addon-slc','samplomatic','pauli-prop']},'num_qubits':n,'initial':'000','observable':'IZI','noise_site':'after','unique_noise_models':len(maps),'unique_error_terms':sum(len(ps) for ps in paulis.values()),'ideal':ideal,'noisy':noisy,'bounds':{mode:{k:v.rates.tolist() for k,v in d.items()} for mode,d in [('forward',forward),('backward',backward),('merged',merged)]},'noise_models':{k:{'paulis':v.get_qubit_sparse_pauli_list_copy().to_sparse_list(),'rates':v.rates.tolist()} for k,v in maps.items()},'records':records,'finite_pec_batches':batches,'all_zero_mask_regression':all_zero_regression,'all_zero_guard':zero_guard,'mask_convention':'installed0.1.0 returns0/1 selection; sampling cancellation needs negative selection, not raw mask','elapsed_seconds':time.perf_counter()-started,'scope':'full SLC selection, Samplomatic generation, local Aer noisy execution, PEC SDK postprocessing; synthetic learned rates, no cloud Executor or hardware noise learning'}
 (HERE/'slc-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
