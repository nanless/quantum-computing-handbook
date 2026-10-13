#!/usr/bin/env python3
"""Full installed SDKs, independent local checks. No cloud/account requests.

Run with requirements-lock.txt in a separate Python 3.11 environment.
Package releases differ from the historical source excerpt commits.
"""
import argparse
import datetime
import importlib.metadata
import json
import math
import pathlib
import platform
import time
import traceback
import warnings

HERE = pathlib.Path(__file__).resolve().parent


def json_value(value):
    if isinstance(value, complex):return [value.real, value.imag]
    if hasattr(value, "item"):return value.item()
    raise TypeError(f"Unrecordable value: {type(value).__name__}")


def check_close(actual, expected, tol=1e-10):
    assert abs(actual - expected) < tol, (actual, expected, tol)


def qiskit_case():
    import numpy as np
    from qiskit import QuantumCircuit, transpile
    from qiskit.quantum_info import Operator, Statevector
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(0, 2)
    circuit.rz(0.4, 2)
    compiled = transpile(circuit, basis_gates=['rz', 'sx', 'x', 'cx'],
                         coupling_map=[[0,1],[1,0],[1,2],[2,1]],
                         optimization_level=3, seed_transpiler=72)
    assert Operator.from_circuit(compiled).equiv(Operator(circuit))
    state = Statevector.from_instruction(circuit)
    # Qiskit display order q2,q1,q0: the two occupied components are 000 and 101.
    expected = np.zeros(8, dtype=complex)
    expected[0], expected[5] = np.exp(-0.2j)/math.sqrt(2), np.exp(0.2j)/math.sqrt(2)
    assert np.max(np.abs(state.data-expected)) < 1e-12
    return {'packages':['qiskit'], 'input':'H(q0), CX(q0,q2), RZ(0.4,q2)',
            'basis_order':'q2 q1 q0; binary indices 000 and 101',
            'depth_before':circuit.depth(), 'depth_after':compiled.depth(),
            'native_gate_counts':dict(compiled.count_ops()),
            'layout_corrected_operator_equivalent':True,
            'occupied_probabilities':state.probabilities_dict()}


def algorithm_case():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter
    from qiskit.primitives import StatevectorSampler, StatevectorEstimator
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_algorithms import Grover, AmplificationProblem, VQE, IterativeAmplitudeEstimation, EstimationProblem
    from qiskit_algorithms.optimizers import COBYLA
    oracle = QuantumCircuit(2); oracle.cz(0,1)
    result = Grover(iterations=1, sampler=StatevectorSampler(default_shots=1024,seed=72)).amplify(
        AmplificationProblem(oracle,is_good_state=['11']))
    assert result.top_measurement == '11' and result.oracle_evaluation
    preparation=QuantumCircuit(1);preparation.ry(2*math.asin(math.sqrt(0.2)),0)
    iae_counts=[]; iae_pub_shots=[]
    class RecordingSampler(StatevectorSampler):
        def run(self, pubs, *, shots=None):
            job=super().run(pubs,shots=shots)
            for pub in job.result():
                iae_counts.append({k:v.get_counts() for k,v in pub.data.items()})
                # Count one quantum preparation per shot, not one per result register.
                registers=[sum(v.get_counts().values()) for v in pub.data.values()]
                assert len(set(registers))==1 and registers[0]==pub.metadata['shots']
                iae_pub_shots.append(registers[0])
            return job
    iae=IterativeAmplitudeEstimation(epsilon_target=0.005,alpha=0.05,
        sampler=RecordingSampler(default_shots=512,seed=np.random.default_rng(72))).estimate(
            EstimationProblem(preparation,objective_qubits=[0]))
    assert iae.confidence_interval[0]<=0.2<=iae.confidence_interval[1]
    assert iae.confidence_interval[1]-iae.confidence_interval[0]<=0.01
    assert max(iae.powers)>0
    executed_powers=list(iae.powers[1:])
    assert len(executed_powers)==len(iae_pub_shots)
    q_calls=sum(n*k for n,k in zip(iae_pub_shots,executed_powers))
    a_calls=sum(n*(k+1) for n,k in zip(iae_pub_shots,executed_powers))
    adag_calls=q_calls
    assert q_calls==iae.num_oracle_queries
    assert a_calls+adag_calls==sum(n*(2*k+1) for n,k in zip(iae_pub_shots,executed_powers))
    angle=Parameter('theta'); ansatz=QuantumCircuit(1); ansatz.ry(angle,0)
    observable=SparsePauliOp.from_list([('Z',0.7),('X',0.2)])
    counts=[]
    solver=VQE(StatevectorEstimator(),ansatz,COBYLA(maxiter=300,tol=1e-10),
               initial_point=[2.0], callback=lambda n,p,e,m:counts.append(float(e)))
    vqe=solver.compute_minimum_eigenvalue(observable)
    exact=-math.sqrt(0.7**2+0.2**2)
    check_close(vqe.eigenvalue.real,exact,1e-7)
    return {'packages':['qiskit-algorithms'], 'grover_iterations':1,
            'grover_raw_distribution':result.circuit_results,
            'grover_answer':result.top_measurement,
            'iae_estimation':float(iae.estimation),'iae_confidence_interval':list(iae.confidence_interval),
            'iae_powers':iae.powers,'iae_executed_powers':executed_powers,'iae_raw_counts':iae_counts,
            'iae_seed':72,'iae_rng_policy':'one persistent numpy Generator across adaptive batches; no per-batch integer reseeding',
            'iae_actual_shots_per_pub':iae_pub_shots,'iae_total_measurement_shots':sum(iae_pub_shots),
            'iae_A_calls':a_calls,'iae_A_inverse_calls':adag_calls,'iae_A_and_inverse_calls':a_calls+adag_calls,'iae_sampler_shots_per_pub':512,'iae_oracle_queries':iae.num_oracle_queries,'iae_shots':iae.shots,'vqe_energy':float(vqe.eigenvalue.real),
            'exact_ground_energy':exact,'objective_calls':len(counts),
            'objective_history':counts,'sampling':'Grover finite 1024; VQE exact StatevectorEstimator'}


def sqd_case():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.primitives import StatevectorSampler
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_addon_sqd.counts import counts_to_arrays
    from qiskit_addon_sqd.qubit import solve_qubit, project_operator_to_subspace, sort_and_remove_duplicates
    circuit=QuantumCircuit(2); circuit.ry(0.8,0);circuit.ry(0.6,1);circuit.cx(0,1);circuit.measure_all()
    raw=StatevectorSampler(default_shots=4096,seed=72).run([circuit]).result()[0].data.meas.get_counts()
    bits, probabilities=counts_to_arrays(raw)
    assert bits.shape==(4,2)
    ham=SparsePauliOp.from_list([('ZI',0.3),('IZ',0.7),('XI',0.2),('IX',0.15),('XX',0.1)])
    energy, states=solve_qubit(np.vstack([bits,bits[0]]),ham,k=1,which='SA',tol=1e-12,
                              v0=np.array([1.,0.,0.,0.]))
    exact=float(np.linalg.eigvalsh(ham.to_matrix())[0])
    check_close(float(energy[0]),exact)
    residual=float(np.linalg.norm(ham.to_matrix()@states[:,0]-energy[0]*states[:,0]))
    assert residual<1e-10
    restricted=np.array([[False,False],[True,True]])
    sub=project_operator_to_subspace(restricted,ham).toarray()
    restricted_energy=float(np.linalg.eigvalsh(sub)[0])
    assert restricted_energy>=exact-1e-12
    return {'packages':['qiskit-addon-sqd'],'raw_counts':raw,'shots':4096,
            'deduplicated_bitstrings':sort_and_remove_duplicates(bits).astype(int).tolist(),
            'hamiltonian':ham.to_list(),'full_subspace_energy':float(energy[0]),
            'dense_reference':exact,'residual_norm':residual,
            'restricted_dimension':2,'restricted_energy':restricted_energy,
            'scope':'sample -> deduplicate -> SDK projection/ARPACK; not molecular production benchmark'}


def mpf_case():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import PauliEvolutionGate
    from qiskit.quantum_info import SparsePauliOp, Statevector
    from qiskit.synthesis import SuzukiTrotter
    from qiskit_addon_mpf.static import setup_static_lse
    from qiskit_addon_mpf.costs import setup_exact_problem
    steps=[2,4]; lse=setup_static_lse(steps,order=2,symmetric=True)
    analytical=lse.solve(); problem,coeff=setup_exact_problem(lse);problem.solve(solver='CLARABEL')
    assert problem.status=='optimal'
    assert np.max(np.abs(coeff.value-np.array([-1/3,4/3])))<1e-8
    ham=SparsePauliOp.from_list([('X',1),('Z',1)]); z=SparsePauliOp('Z');t=0.7
    expectations=[]; gate_counts=[]; product_values=[]
    for k in steps:
        circ=QuantumCircuit(1)
        circ.append(PauliEvolutionGate(ham,time=t,synthesis=SuzukiTrotter(order=2,reps=k)),[0])
        # Explicit synthesis is essential: evaluating the high-level gate's exact
        # matrix would silently bypass the product-formula approximation.
        native=circ.decompose(reps=5)
        expectations.append(float(Statevector.from_instruction(native).expectation_value(z).real))
        gate_counts.append(dict(native.count_ops()))
        assert all(instruction.operation.name=='u' for instruction in native.data)
        # Independent Strang product: exp(-i dt X/2) exp(-i dt Z) exp(-i dt X/2).
        dt=t/k; X=np.array([[0,1],[1,0]],complex)
        half=np.cos(dt/2)*np.eye(2)-1j*np.sin(dt/2)*X
        middle=np.diag([np.exp(-1j*dt),np.exp(1j*dt)])
        matrix=np.linalg.matrix_power(half@middle@half,k)
        vector=matrix@np.array([1,0])
        reference=float((abs(vector[0])**2-abs(vector[1])**2).real)
        check_close(expectations[-1],reference,1e-12);product_values.append(reference)
    exact=0.5+0.5*math.cos(2*math.sqrt(2)*t)
    assert np.max(abs(analytical-np.array([-1/3,4/3])))<1e-12
    assert np.max(abs(coeff.value-analytical))<1e-8
    combined=float(np.dot(analytical,expectations))
    assert abs(combined-exact)<abs(expectations[-1]-exact)
    return {'packages':['qiskit-addon-mpf'],'steps':steps,'coefficients':analytical.tolist(),
            'cvxpy_status':problem.status,'solver':'CLARABEL','gamma':float(np.sum(np.abs(analytical))),
            'synthesized_gate_counts':gate_counts,'independent_strang_values':product_values,'values':expectations,'combined':combined,'exact':exact,
            'scope':'static MPF constraint solver and explicitly synthesized circuits; dynamic TN backend not exercised'}


def obp_case():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator,SparsePauliOp,Statevector
    from qiskit_addon_obp import backpropagate
    from qiskit_addon_obp.utils.simplify import OperatorBudget
    first=QuantumCircuit(1); first.rx(0.4,0)
    last=QuantumCircuit(1); last.ry(math.pi/6,0)
    full=first.compose(last); observable=SparsePauliOp('Z')
    pulled, remaining, meta=backpropagate(observable,[first,last],operator_budget=OperatorBudget(max_paulis=8))
    assert len(remaining)==2-meta.num_backpropagated_slices==0
    u=Operator(full).data; dense=u.conj().T@observable.to_matrix()@u
    assert np.max(np.abs(pulled.to_matrix()-dense))<1e-12
    target=float(Statevector.from_instruction(full).expectation_value(observable).real)
    reconstructed=float(Statevector.from_label('0').expectation_value(pulled).real)
    check_close(reconstructed,target)
    rejected,stopped,stopmeta=backpropagate(observable,[first,last],operator_budget=OperatorBudget(max_paulis=1))
    assert stopmeta.num_backpropagated_slices==0
    # 0.3.0 returns slices[:-0] == [] and aliases the rejected candidate.
    # Guard using the authoritative accepted-slice count, then recheck semantics.
    sdk_zero_slice_bug=(len(stopped)==0 and len(rejected)>1)
    assert sdk_zero_slice_bug
    guarded_observable,guarded_remaining=observable.copy(),[first.copy(),last.copy()]
    assert len(guarded_remaining)==2-stopmeta.num_backpropagated_slices
    assert np.max(abs(guarded_observable.to_matrix()-np.diag([1,-1])))<1e-12
    guarded_state=Statevector.from_instruction(guarded_remaining[0].compose(guarded_remaining[1]))
    check_close(float(guarded_state.expectation_value(guarded_observable).real),target)
    return {'packages':['qiskit-addon-obp'],'pulled_paulis':pulled.to_list(),'full_expectation':target,
            'reconstructed_expectation':reconstructed,'backpropagated_slices':meta.num_backpropagated_slices,
            'one_term_budget_sdk_retained_slices':len(stopped),'zero_accepted_slice_regression_observed':sdk_zero_slice_bug,'guarded_retained_slices':len(guarded_remaining),'scope':'exact dense comparison; no truncation or QPU'}


def cutting_case():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.primitives import SamplerResult
    from qiskit.result import QuasiDistribution
    from qiskit.quantum_info import PauliList,Statevector
    from qiskit_addon_cutting import partition_problem,generate_cutting_experiments,reconstruct_expectation_values
    from qiskit_addon_cutting.utils.simulation import simulate_statevector_outcomes
    circuit=QuantumCircuit(2);circuit.h(0);circuit.cx(0,1)
    observables=PauliList(['XX','ZZ','IZ'])
    problem=partition_problem(circuit,partition_labels='AB',observables=observables)
    subexperiments,coefficients=generate_cutting_experiments(problem.subcircuits,problem.subobservables,num_samples=np.inf)
    results={label:SamplerResult([QuasiDistribution(simulate_statevector_outcomes(c)) for c in circuits],
                                [{'shots':None} for c in circuits]) for label,circuits in subexperiments.items()}
    estimates=reconstruct_expectation_values(results,coefficients,problem.subobservables)
    target=[float(Statevector.from_instruction(circuit).expectation_value(o).real) for o in observables]
    assert np.max(np.abs(np.array(target)-estimates))<1e-12
    return {'packages':['qiskit-addon-cutting'],'observables':['XX','ZZ','IZ'],
            'local_qubit_counts':{k:v.num_qubits for k,v in problem.subcircuits.items()},
            'subexperiment_counts':{k:len(v) for k,v in subexperiments.items()},
            'qpd_terms':len(coefficients),'gamma':sum(abs(float(c[0])) for c in coefficients),
            'reconstructed':list(estimates),'target':target,
            'scope':'complete partition/experiment generation/exact local outcome simulation/reconstruction; no finite-shot inference'}


def mitiq_case():
    import cirq
    from mitiq.zne import execute_with_zne,RichardsonFactory
    from mitiq.zne.scaling import fold_gates_at_random
    q=cirq.LineQubit(0);circuit=cirq.Circuit(cirq.X(q));p=0.02;calls=[]
    def executor(c):
        noisy=cirq.Circuit()
        for gate in c.all_operations():
            noisy.append(gate); noisy.append(cirq.depolarize(p).on(*gate.qubits))
        rho=cirq.DensityMatrixSimulator(seed=72).simulate(noisy).final_density_matrix
        value=float((rho[0,0]-rho[1,1]).real)
        calls.append({'operations':len(list(c.all_operations())),'value':value})
        return value
    raw=executor(circuit)
    mitigated=float(execute_with_zne(circuit,executor,factory=RichardsonFactory(scale_factors=[1,3,5]),
                                     scale_noise=fold_gates_at_random))
    for row in calls:check_close(row['value'],-(1-4*p/3)**row['operations'],2e-7)
    assert abs(mitigated+1)<abs(raw+1)
    return {'packages':['mitiq'],'cirq_pauli_probability':p,'raw':raw,'mitigated':mitigated,
            'ideal':-1,'executor_calls':calls,'scope':'exact synthetic channel; finite-shot variance/calibration not inferred'}


def pygsti_case():
    import numpy as np
    from pygsti.modelpacks import smq1Q_XYI
    from pygsti.modelmembers.instruments import Instrument
    from pygsti.circuits import Circuit
    model=smq1Q_XYI.target_model()
    effects=[np.asarray(model.povms['Mdefault'][label].to_dense()).reshape(-1) for label in ['0','1']]
    maps=[np.outer(e,e) for e in effects]
    model.instruments[('Im',0)]=Instrument({'0':maps[0],'1':maps[1]},state_space=model.state_space)
    x90=model.operations[('Gxpi2',0)].to_dense('HilbertSchmidt')
    flip=x90@x90
    model.instruments[('Ir',0)]=Instrument({'0':maps[0],'1':flip@maps[1]},state_space=model.state_space)
    records={}
    for name in ['Im','Ir']:
        probabilities=model.probabilities(Circuit([('Gypi2',0),(name,0),(name,0)],line_labels=(0,)))
        matching=sum(float(value) for outcome,value in probabilities.items() if outcome[0]==outcome[1])
        records[name]={'probabilities':{','.join(k):float(v) for k,v in probabilities.items()},'repeat_agreement':matching}
    check_close(records['Im']['repeat_agreement'],1)
    check_close(records['Ir']['repeat_agreement'],0.5)
    # Separate model without instruments for linear gate-set tomography.
    import pygsti
    target_model=smq1Q_XYI.target_model()
    true_model=target_model.depolarize(op_noise=0.01,spam_noise=0.015)
    prep=smq1Q_XYI.prep_fiducials();meas=smq1Q_XYI.meas_fiducials()
    circuits=pygsti.circuits.create_lgst_circuits(prep,meas,target_model)
    dataset=pygsti.data.simulate_data(true_model,circuits,num_samples=16384,seed=72)
    fitted=pygsti.algorithms.run_lgst(dataset,prep,meas,target_model,svd_truncate_to=4,check=True)
    raw={str(c):{','.join(o):float(n) for o,n in dataset[c].counts.items()} for c in circuits}
    (HERE/'gst-counts.json').write_text(json.dumps(raw,indent=2)+'\n')
    unique_settings=len(set(circuits))
    assert len(circuits)==unique_settings==len(raw)==len(dataset)==92
    assert all(abs(sum(counts.values())-16384)<1e-10 for counts in raw.values())
    total_samples=sum(sum(counts.values()) for counts in raw.values())
    assert total_samples==92*16384
    holdout=[]; gauge_errors=[]
    # Nontrivial invertible change of Liouville coordinates; no physical channel claim.
    S=np.diag([1.,1.2,.8,1.1]); Sinv=np.linalg.inv(S)
    for length in range(1,13):
        circuit=Circuit([('Gxpi2',0)]*length,line_labels=(0,))
        # Independent dense Liouville multiplication, not the probability engine.
        vector=np.asarray(true_model.preps['rho0'].to_dense()).reshape(-1)
        gate=true_model.operations[('Gxpi2',0)].to_dense('HilbertSchmidt')
        effect=np.asarray(true_model.povms['Mdefault']['0'].to_dense()).reshape(-1)
        dense=float(effect@np.linalg.matrix_power(gate,length)@vector)
        predicted=float(fitted.probabilities(circuit)[('0',)])
        assert abs(predicted-dense)<0.03
        transformed=float((effect@Sinv)@np.linalg.matrix_power(S@gate@Sinv,length)@(S@vector))
        gauge_errors.append(abs(transformed-dense));check_close(transformed,dense,1e-12)
        holdout.append({'length':length,'is_in_training_set':circuit in dataset,
                        'dense_probability':dense,'lgst_probability':predicted,'gauge_changed_probability':transformed})
    return {'packages':['pygsti'],'basis':str(model.basis),'instrument_models':records,
            'lgst_settings':len(circuits),'lgst_unique_settings':unique_settings,'lgst_total_samples':int(total_samples),
            'lgst_shots_per_setting':16384,'lgst_holdouts':holdout,'gauge_S':S.tolist(),'gauge_max_probability_difference':max(gauge_errors),
            'scope':'installed instrument engine plus finite-shot LGST fit and length1-12 dense references (training overlap flagged); not long-sequence MLE GST or a QND experiment'}


def pauli_case():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import SparsePauliOp,Operator
    from pauli_prop import propagate_through_circuit
    circuit=QuantumCircuit(1);circuit.ry(math.pi/6,0)
    z=SparsePauliOp('Z');u=Operator(circuit).data
    exact=u.conj().T@z.to_matrix()@u
    propagated,error=propagate_through_circuit(z,circuit,max_terms=4,atol=0.0,frame='h')
    assert np.max(np.abs(propagated.to_matrix()-exact))<1e-12
    truncated,bound=propagate_through_circuit(z,circuit,max_terms=1,atol=0.0,frame='h')
    plus=np.array([1,1])/math.sqrt(2)
    bias=abs(np.vdot(plus,(truncated.to_matrix()-exact)@plus))
    check_close(bound,0.5);check_close(bias,0.5)
    return {'packages':['pauli-prop'],'full_terms':propagated.to_list(),'full_discarded_l1':error,
            'one_term_result':truncated.to_list(),'discarded_l1_bound':bound,'plus_state_bias':float(bias),
            'scope':'actual Rust extension propagation; shading/PNA workflows not claimed'}


CASES={'qiskit':qiskit_case,'algorithms':algorithm_case,'sqd':sqd_case,'mpf':mpf_case,
       'obp':obp_case,'cutting':cutting_case,'mitiq':mitiq_case,'pygsti':pygsti_case,'pauli-prop':pauli_case}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=['all']+list(CASES),default='all')
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Run without -O: checks require assertions')
    records=[]
    for name in (CASES if args.case=='all' else [args.case]):
        print('RUN',name,flush=True);start=time.perf_counter()
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter('always')
            try:
                result=CASES[name]();versions={p:importlib.metadata.version(p) for p in result['packages']}
                record={'case':name,'status':'passed','versions':versions,'checks':result}
            except Exception as exc:
                record={'case':name,'status':'failed','error':repr(exc),'traceback':traceback.format_exc()}
            record['warnings']=sorted(set(str(w.message) for w in observed))
        record['elapsed_seconds']=time.perf_counter()-start;records.append(record)
        print(record['status'].upper(),name,flush=True)
    report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),
            'platform':platform.platform(),'scope':'installed official SDK CPU tasks; no cloud/QPU, not all upstream tests',
            'records':records}
    (HERE/f'results-{args.case}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2, default=json_value)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2, default=json_value))
    if any(r['status']!='passed' for r in records):raise SystemExit(1)


if __name__=='__main__':main()
