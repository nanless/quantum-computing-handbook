#!/usr/bin/env python3
"""Round73 complete SDK workflows, synthetic CPU data; no network or vendor imports."""
import argparse, hashlib, importlib.metadata as md, json, platform, sys, traceback
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)

def pack(x):
    if isinstance(x,np.ndarray):return pack(x.tolist())
    if isinstance(x,np.generic):return pack(x.item())
    if isinstance(x,complex):return [x.real,x.imag]
    if isinstance(x,dict):return {str(k):pack(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [pack(v) for v in x]
    return x

def raw(ed):return [{'counts':d['counts'],'shots':d['shots'],'metadata':d['metadata']} for d in ed.data()]
def fitted(ed):
    ed.block_for_results(timeout=180)
    assert ed.analysis_status().name=='DONE',ed.errors()
    return np.array(ed.analysis_results('state',dataframe=True).iloc[0].value.data)
def bloch_from_counts(data):
    v=np.zeros(3)
    for d in data:v[[2,0,1][d['metadata']['m_idx'][0]]]=(d['counts'].get('0',0)-d['counts'].get('1',0))/d['shots']
    return v

def readout():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel,ReadoutError
    from qiskit_experiments.library import LocalReadoutError,StateTomography
    from qiskit_experiments.library.tomography.basis import PauliMeasurementBasis
    # A[y,x] is reported y given true x; Aer ReadoutError instead takes rows true x.
    A=np.array([[.88,.23],[.12,.77]])
    noise=NoiseModel();noise.add_all_qubit_readout_error(ReadoutError(A.T))
    backend=AerSimulator(method='density_matrix',noise_model=noise,max_parallel_threads=1)
    cal=LocalReadoutError([0]).run(backend,shots=16384,seed_simulator=730).block_for_results(timeout=180)
    assert cal.analysis_status().name=='DONE',cal.errors()
    mitigator=cal.analysis_results('Local Readout Mitigator',dataframe=True).iloc[0].value
    Ahat=mitigator.assignment_matrix();calraw=raw(cal)
    own=np.zeros((2,2))
    for d in calraw:
        x=int(d['metadata']['state_label']);own[:,x]=[d['counts'].get(str(y),0)/d['shots'] for y in (0,1)]
    assert np.max(abs(Ahat-own))<1e-12
    qc=QuantumCircuit(1);qc.ry(np.pi/3,0);qc.s(0)
    qst=StateTomography(qc);qst.analysis.set_options(fitter='linear_inversion',rescale_positive=False)
    ed=qst.run(backend,shots=8192,seed_simulator=731)
    unmit=fitted(ed);counts=raw(ed)
    corrected=qst.analysis.run(ed,replace_results=False,measurement_basis=PauliMeasurementBasis(mitigator=mitigator))
    corrected.block_for_results(timeout=180)
    assert corrected.analysis_status().name=='DONE',corrected.errors()
    table=corrected.analysis_results('state',dataframe=True);mit=np.array(table.iloc[-1].value.data)
    observed=bloch_from_counts(counts)
    # readout affine relation m=(beta-alpha)+(1-alpha-beta)*r for +/- convention.
    alpha=Ahat[1,0];beta=Ahat[0,1];d=1-alpha-beta
    independent_r=(observed-(beta-alpha))/d
    direct=(I+independent_r[0]*X+independent_r[1]*Y+independent_r[2]*Z)/2
    assert np.max(abs(mit-direct))<1e-11
    v=np.array([np.sqrt(3)/2,.5j]);target=np.outer(v,v.conj())
    assert np.linalg.norm(mit-target)<.03
    assert np.linalg.norm(mit-target)<np.linalg.norm(unmit-target)
    # First-order calibration and target-shot variance; one calibration reused for axes creates covariance.
    true_r=np.array([0,np.sqrt(3)/2,.5]);mu=(.23-.12)+.65*true_r
    variance_measure=(1-mu**2)/(8192*.65**2)
    da=(true_r-1)/.65;db=(true_r+1)/.65
    covariance=np.diag(variance_measure)+np.outer(da,da)*(.12*.88/16384)+np.outer(db,db)*(.23*.77/16384)
    assert np.linalg.eigvalsh(covariance).min()>0
    return {'model':'stationary independent classical readout flips, ideal preparations and basis gates',
        'calibration_seed':730,'tomography_seed':731,'calibration_counts':calraw,'tomography_counts':counts,
        'true_assignment_columns':A,'fitted_assignment_columns':Ahat,'condition_number_2':float(np.linalg.cond(Ahat)),
        'unmitigated_density':unmit,'mitigated_density':mit,'independent_density':direct,'target_density':target,
        'observed_bloch':observed,'corrected_bloch':independent_r,'corrected_eigenvalues':np.linalg.eigvalsh(mit),
        'unmitigated_frobenius_error':float(np.linalg.norm(unmit-target)),
        'mitigated_frobenius_error':float(np.linalg.norm(mit-target)),
        'independent_reconstruction_error':float(np.max(abs(mit-direct))),
        'delta_method_total_covariance':covariance,'covariance_units':'dimensionless squared',
        'variance_boundary':'first-order delta approximation with known generating rates, not bootstrap or coverage proof'}

def feedback():
    from qiskit import QuantumCircuit,transpile
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel,ReadoutError
    A=np.array([[.88,.23],[.12,.77]])
    noise=NoiseModel();noise.add_readout_error(ReadoutError(A.T),[0]);noise.add_readout_error(ReadoutError(A.T),[1])
    backend=AerSimulator(method='density_matrix',noise_model=noise,max_parallel_threads=1)
    v=np.array([np.sqrt(3)/2,.5j]);rho=np.outer(v,v.conj())
    qc=QuantumCircuit(3,2);qc.initialize(v,0);qc.h(1);qc.cx(1,2);qc.cx(0,1);qc.h(0)
    qc.measure(0,0);qc.measure(1,1)
    with qc.if_test((qc.clbits[1],1)):qc.x(2)
    with qc.if_test((qc.clbits[0],1)):qc.z(2)
    qc.save_density_matrix([2],label='bob')
    result=backend.run(transpile(qc,backend,optimization_level=0),shots=16384,seed_simulator=735).result()
    assert result.success
    got=np.asarray(result.data(0)['bob']);error_prob=(.12+.23)/2
    weights=[(1-error_prob)**2,error_prob*(1-error_prob),error_prob*(1-error_prob),error_prob**2]
    paulis=[I,X,Z,Z@X];expected=sum(w*k@rho@k.conj().T for w,k in zip(weights,paulis))
    assert np.max(abs(got-expected))<.015
    return {'model':'ideal resource and gates, only two independent asymmetric Alice readout flips',
        'shots':16384,'seed':735,'reported_alice_counts_c1c0':result.get_counts(),
        'input_density':rho,'bob_density':got,'analytic_density':expected,
        'average_flip_probability':error_prob,'pauli_error_weights_I_X_Z_ZX':weights,
        'max_matrix_error':float(np.max(abs(got-expected))),
        'boundary':'post-processing Alice counts cannot undo physical gates already triggered by wrong records'}

def qpt():
    import cvxpy as cp
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Choi
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import amplitude_damping_error
    from qiskit_experiments.library import ProcessTomography
    from qiskit_experiments.library.tomography.basis import PauliMeasurementBasis,PauliPreparationBasis
    from qiskit_experiments.library.tomography.fitters import cvxpy_gaussian_lstsq
    from qiskit_experiments.library.tomography.fitters.fitter_data import tomography_fitter_data
    backend=AerSimulator(method='density_matrix',max_parallel_threads=1)
    qc=QuantumCircuit(1);qc.ry(np.pi/5,0);qc.append(amplitude_damping_error(.36,excited_state_population=.1).to_instruction(),[0])
    exp=ProcessTomography(qc,analysis=None)
    train=exp.run(backend,shots=128,seed_simulator=732).block_for_results(timeout=180)
    hold=exp.run(backend,shots=512,seed_simulator=733).block_for_results(timeout=180)
    data=raw(train);held=raw(hold);assert len(data)==len(held)==12
    arrays=tomography_fitter_data(train.data())
    sdk,meta=cvxpy_gaussian_lstsq(*arrays,measurement_basis=PauliMeasurementBasis(),preparation_basis=PauliPreparationBasis(),
        psd=True,trace_preserving=True,solver='SCS',eps=1e-9,max_iters=200000)
    bad_sdk=sdk.copy();bad_meta=meta.copy()
    bad_partial=np.einsum('aibi->ab',bad_sdk.reshape(2,2,2,2))
    assert np.max(abs(bad_partial-I))>1e-5
    (R/'sdk-tp-counterexample.json').write_text(json.dumps(pack({'version':'0.14.2','metadata':bad_meta,'choi':bad_sdk,'output_partial_trace':bad_partial,'max_tp_error':float(np.max(abs(bad_partial-I))),'cause':'hermitian=True skips imaginary partial-trace constraints; Hermitian off-diagonal entries need not be real'}),indent=2)+'\n')
    # Official full partial_trace constraint enforces both real and imaginary components.
    sdk,meta=cvxpy_gaussian_lstsq(*arrays,measurement_basis=PauliMeasurementBasis(),preparation_basis=PauliPreparationBasis(),
        psd=True,partial_trace=np.array([I]),solver='SCS',eps=1e-9,max_iters=200000)
    preps=[np.diag([1,0]),np.diag([0,1]),(I+X)/2,(I+Y)/2];axes=[Z,X,Y]
    # Independent basis construction, avoiding SDK vectorization/partial-trace helpers.
    J=cp.Variable((4,4),hermitian=True)
    constraints=[J>>0]
    for a in (0,1):
        for b in (0,1):constraints.append(J[2*a,2*b]+J[2*a+1,2*b+1]==int(a==b))
    prob=[];freq=[];counts=[];var=[];operators=[]
    for d in data:
        pidx=d['metadata']['p_idx'][0];midx=d['metadata']['m_idx'][0];n=d['shots']
        for y in (0,1):
            M=(I+(-1)**y*axes[midx])/2
            B=np.kron(preps[pidx].T,M);operators.append(B)
            prob.append(cp.real(cp.trace(B@J)))
            k=d['counts'].get(str(y),0);counts.append(k);freq.append(k/n)
            posterior=(k+.5)/(n+1);var.append(posterior*(1-posterior)/(n+2))
    prob=cp.hstack(prob);freq=np.array(freq);counts=np.array(counts);var=np.array(var)
    w=1/np.sqrt(var);w=w/np.linalg.norm(w)
    loss=cp.sum_squares(cp.multiply(1/np.sqrt(var),prob-freq))
    problem=cp.Problem(cp.Minimize(loss),constraints);problem.solve(solver='SCS',eps=1e-9,max_iters=200000)
    assert problem.status=='optimal';own=J.value.copy()
    from qiskit_experiments.library.tomography.fitters import lstsq_utils
    basis,frequencies,weights=lstsq_utils.lstsq_data(*arrays,measurement_basis=PauliMeasurementBasis(),preparation_basis=PauliPreparationBasis(),measurement_qubits=(0,),preparation_qubits=(0,),weights=lstsq_utils.binomial_weights(arrays[0],arrays[1]))
    manual=np.array([b.reshape(16) for b in operators])
    print('design diagnostics',np.max(abs(manual-basis)),np.max(abs(freq-frequencies.ravel())),np.max(abs(w-weights.ravel())),flush=True)
    np.savez_compressed(R/'qpt-design-diagnostic.npz',sdk=sdk,independent=own,manual_design=manual,sdk_design=basis,frequencies=freq,sdk_frequencies=frequencies,weights=w,sdk_weights=weights)
    assert np.max(abs(sdk-own))<2e-5,(np.max(abs(sdk-own)),meta)
    # True multinomial likelihood: count-weighted log probabilities, no Gaussian replacement.
    mle_problem=cp.Problem(cp.Minimize(-cp.sum(cp.multiply(counts,cp.log(prob)))),constraints+[prob>=1e-10])
    mle_problem.solve(solver='SCS',eps=1e-8,max_iters=200000)
    assert mle_problem.status=='optimal';mle=J.value.copy()
    assert np.sum(counts)==1536
    def tp(j):return np.einsum('aibi->ab',j.reshape(2,2,2,2))
    for j in (sdk,own,mle):
        assert np.linalg.eigvalsh(j).min()>-2e-6
        assert np.max(abs(tp(j)-I))<2e-6
    # Independent rotated Kraus formula, input first/output second.
    c=np.cos(np.pi/10);s=np.sin(np.pi/10);U=np.array([[c,-s],[s,c]])
    ks=[np.sqrt(.9)*np.diag([1,.8]),np.sqrt(.9)*np.array([[0,.6],[0,0]]),
        np.sqrt(.1)*np.diag([.8,1]),np.sqrt(.1)*np.array([[0,0],[.6,0]])]
    truth=sum(np.outer((k@U).T.reshape(4),(k@U).T.reshape(4).conj()) for k in ks)
    outputs=[]
    for pidx in range(4):
        v=bloch_from_counts([d for d in data if d['metadata']['p_idx'][0]==pidx])
        outputs.append((I+v[0]*X+v[1]*Y+v[2]*Z)/2)
    a,b,plus,plusi=outputs;off=plus-(a+b)/2+1j*(plusi-(a+b)/2)
    linear=np.block([[a,off],[off.conj().T,b]])
    def likelihood(j,rows):
        total=0.
        for d in rows:
            for y in (0,1):
                M=(I+(-1)**y*axes[d['metadata']['m_idx'][0]])/2
                p=float(np.trace(np.kron(preps[d['metadata']['p_idx'][0]].T,M)@j).real)
                total-=d['counts'].get(str(y),0)*np.log(max(p,1e-12))
        return float(total)
    assert likelihood(mle,data)<=likelihood(sdk,data)+1e-4
    return {'model':'trusted ideal preparations and Pauli measurements; rotated generalized amplitude damping',
        'training_seed':732,'holdout_seed':733,'training_shots_per_setting':128,'holdout_shots_per_setting':512,
        'training_counts':data,'holdout_counts':held,'sdk_fitter_metadata':meta,
        'default_tp_claim_counterexample_choi':bad_sdk,'default_tp_claim_partial_trace':bad_partial,'sdk_gaussian_choi':sdk,'independent_gaussian_choi':own,'multinomial_mle_choi':mle,'analytic_choi':truth,
        'raw_linear_choi':linear,'raw_linear_eigenvalues':np.linalg.eigvalsh(linear),
        'gaussian_crosscheck_max_error':float(np.max(abs(sdk-own))),
        'gaussian_eigenvalues':np.linalg.eigvalsh(sdk),'gaussian_output_partial_trace':tp(sdk),
        'mle_min_predicted_probability':float(min(np.trace(b@mle).real for b in operators)),'mle_eigenvalues':np.linalg.eigvalsh(mle),'mle_output_partial_trace':tp(mle),
        'gaussian_normalized_weights':w,'observed_frequencies':freq,
        'training_negative_log_likelihood':{'gaussian':likelihood(sdk,data),'multinomial_mle':likelihood(mle,data)},
        'holdout_negative_log_likelihood':{'gaussian':likelihood(sdk,held),'multinomial_mle':likelihood(mle,held),'true':likelihood(truth,held)},
        'frobenius_errors':{'gaussian':float(np.linalg.norm(sdk-truth)),'multinomial_mle':float(np.linalg.norm(mle-truth))},
        'boundary':'holdout is one independent batch, no guarantee MLE has best holdout fit; no SPAM joint estimation'}

def dynamics():
    import qutip as qt
    from scipy.integrate import solve_ivp
    from scipy.linalg import expm
    t=np.linspace(0,3,61);delta=.7;kappa=.4
    def omega(s):return 1.1*np.exp(-((s-1.5)/.35)**2)
    h=[delta/2*qt.sigmaz(),[.5*qt.sigmax(),lambda s:omega(s)]]
    g,e=qt.basis(2,0),qt.basis(2,1);psi=(g+1j*e).unit();L=np.sqrt(kappa)*g*e.dag()
    ops=[qt.sigmax(),qt.sigmay(),qt.sigmaz()]
    # Independent real Bloch differential equations; density operator absent from this solver.
    def rhs(s,r):return [-delta*r[1]-kappa*r[0]/2,delta*r[0]-omega(s)*r[2]-kappa*r[1]/2,omega(s)*r[1]+kappa*(1-r[2])]
    independent=solve_ivp(rhs,[0,3],[0,1,0],t_eval=t,method='DOP853',rtol=2e-12,atol=2e-13,max_step=.02).y
    assert independent.shape==(3,61)
    settings=[(1e-5,1e-4,.25),(1e-8,1e-7,.05),(1e-11,1e-10,.01)]
    convergence=[];last=None
    for atol,rtol,step in settings:
        last=qt.mesolve(h,psi,t,[L],e_ops=ops,options={'atol':atol,'rtol':rtol,'max_step':step,'store_states':True,'progress_bar':''})
        r=np.array(last.expect);err=float(np.max(abs(r-independent)))
        convergence.append({'atol':atol,'rtol':rtol,'max_internal_step_us':step,'max_bloch_error':err})
    for state in last.states:
        a=state.full();assert abs(np.trace(a)-1)<2e-8
        assert np.max(abs(a-a.conj().T))<2e-8 and np.linalg.eigvalsh(a).min()>-2e-8
    assert convergence[-1]['max_bloch_error']<3e-8
    assert convergence[-1]['max_bloch_error']<convergence[0]['max_bloch_error']
    mc=qt.mcsolve(h,psi,t,[L],e_ops=ops,ntraj=2048,seeds=734,
        options={'atol':1e-10,'rtol':1e-9,'max_step':.02,'keep_runs_results':True,'map':'serial','progress_bar':''})
    runs=np.asarray(mc.runs_expect,dtype=float);means=runs.mean(axis=1);se=runs.std(axis=1,ddof=1)/np.sqrt(2048)
    assert np.max(np.sum(means**2,axis=0))<1+1e-8
    assert len({tuple(s.spawn_key) for s in mc.seeds})==2048
    assert np.max(abs(means-np.array(mc.average_expect)))<1e-12
    assert np.all(abs(means-independent)<6*se+3e-7)
    # Covariance between times must use paired values from each trajectory.
    covariance=np.cov(runs[2,:,20],runs[2,:,60],ddof=1)/2048
    np.savez_compressed(R/'trajectory-observables.npz',runs_xyz=runs,times_us=t,jump_counts=np.array([len(x) for x in mc.col_times]))
    # Closed driven case, independent time-ordered midpoint product vs integrated Hamiltonian.
    closed=qt.sesolve(h,psi,t,e_ops=ops,options={'atol':1e-12,'rtol':1e-11,'max_step':.01,'progress_bar':''})
    products=[]
    for n in (40,80,160,320):
        v=psi.full().ravel();dt=3/n
        for k in range(n):v=expm(-1j*dt*(delta*Z+omega((k+.5)*dt)*X)/2)@v
        rv=np.array([np.vdot(v,a@v).real for a in (X,Y,Z)])
        products.append({'steps':n,'max_final_bloch_error':float(np.max(abs(rv-np.array(closed.expect)[:,-1])))})
    assert all(products[i]['max_final_bloch_error']>products[i+1]['max_final_bloch_error'] for i in range(3))
    from scipy.integrate import quad
    wrong=expm(-1j*(delta*3*Z+quad(omega,0,3,epsabs=1e-12)[0]*X)/2)@psi.full().ravel()
    wrong_r=np.array([np.vdot(wrong,a@wrong).real for a in (X,Y,Z)])
    return {'time_unit':'us','hamiltonian_over_hbar_unit':'rad/us','rate_unit':'1/us','delta':delta,'kappa':kappa,
        'pulse':'Omega(t)=1.1 exp(-((t-1.5)/0.35)^2) rad/us','initial_bloch':[0,1,0],
        'times_us':t,'independent_bloch':independent,'mesolve_bloch':last.expect,'tolerance_convergence':convergence,
        'mc_seed':734,'trajectory_count':2048,'mc_means':means,'mc_standard_errors':se,
        'z_mean_time1_time3_covariance':covariance,'jump_count_histogram':np.bincount([len(x) for x in mc.col_times]),
        'seed_spawn_keys':[list(s.spawn_key) for s in mc.seeds],'mc_jump_times_us':mc.col_times,
        'closed_midpoint_convergence':products,'closed_exact_final_bloch':np.array(closed.expect)[:,-1],
        'wrong_integrated_exponential_bloch':wrong_r,
        'wrong_integrated_max_bloch_error':float(np.max(abs(wrong_r-np.array(closed.expect)[:,-1]))),
        'boundary':'Markov zero-temperature damping; ODE convergence is finite-input evidence; six-SE regression is not simultaneous coverage'}

def main():
    if not __debug__:raise RuntimeError('Run without -O')
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['readout','feedback','qpt','dynamics','all'],default='all');a=ap.parse_args()
    report={'python':sys.version,'platform':platform.platform(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'packages':{n:md.version(n) for n in ['numpy','scipy','qiskit','qiskit-aer','qiskit-experiments','qutip','cvxpy','scs','clarabel']},'cases':{}}
    failed=False
    for name,fn in [('readout',readout),('feedback',feedback),('qpt',qpt),('dynamics',dynamics)]:
        if a.case not in ['all',name]:continue
        try:report['cases'][name]={'status':'passed','result':pack(fn())};print(name,'passed',flush=True)
        except Exception as e:failed=True;report['cases'][name]={'status':'failed','error':str(e),'traceback':traceback.format_exc()};print(traceback.format_exc(),flush=True)
    report['exit_code']=1 if failed else 0
    (R/(a.case+'-results.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if failed:raise SystemExit(1)
if __name__=='__main__':main()
