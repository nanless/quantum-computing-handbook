#!/usr/bin/env python3
"""Run installed official SDKs offline; independent analytic expectations, no vendor imports.
Python >=3.11. Run without -O. Outputs counts, matrices, tolerances and versions.
"""
import argparse
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
import sys
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parent


def pack(x):
    if isinstance(x, np.ndarray):
        return pack(x.tolist())
    if isinstance(x, complex):
        return [x.real, x.imag]
    if isinstance(x, np.generic):
        return pack(x.item())
    if isinstance(x, dict):
        return {str(k): pack(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [pack(v) for v in x]
    return x


def valid(rho, tol=1e-8):
    assert np.max(abs(rho-rho.conj().T)) < tol
    assert abs(np.trace(rho)-1) < tol
    assert np.linalg.eigvalsh(rho).min() > -tol


def analytic_damping(rho, gamma, r):
    b, c = rho[1, 1].real, rho[0, 1]
    bp, cp = (1-gamma)*b + gamma*r, np.sqrt(1-gamma)*c
    return np.array([[1-bp, cp], [cp.conjugate(), bp]])


def aer():
    from qiskit import QuantumCircuit, transpile
    from qiskit.quantum_info import Choi, Kraus, Statevector
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import amplitude_damping_error
    backend = AerSimulator(method='density_matrix', max_parallel_threads=1)
    states = [np.array(v,complex) for v in ([1,0],[0,1],[1,1],[1,-1],[1,1j],[np.sqrt(3),1j])]
    states = [v/np.linalg.norm(v) for v in states]
    max_error=0.; rows=[]
    for gamma in (0.,.36,1.):
        for r in (0.,.1,1.):
            error=amplitude_damping_error(gamma, excited_state_population=r)
            channel=error.to_quantumchannel()
            assert channel.is_cptp()
            assert Kraus(channel).is_cp() and Kraus(channel).is_tp()
            choi=Choi(channel).data
            # Qiskit Choi factors: input first, output second; unnormalized trace d=2.
            expected=np.array([[1-gamma*r,0,0,np.sqrt(1-gamma)],
                               [0,gamma*r,0,0],
                               [0,0,gamma*(1-r),0],
                               [np.sqrt(1-gamma),0,0,1-gamma*(1-r)]],complex)
            assert np.allclose(choi,expected,atol=1e-12)
            assert np.linalg.eigvalsh(choi).min() > -1e-10
            assert np.allclose(np.einsum('aibi->ab',choi.reshape(2,2,2,2)),np.eye(2))
            for v in states:
                rho=np.outer(v,v.conj())
                qc=QuantumCircuit(1);qc.set_density_matrix(rho)
                qc.append(error.to_instruction(),[0]);qc.save_density_matrix()
                result=backend.run(qc,shots=1,seed_simulator=72).result()
                assert result.success
                actual=np.array(result.data(0)['density_matrix'])
                target=analytic_damping(rho,gamma,r)
                err=float(np.max(abs(actual-target)));max_error=max(max_error,err)
                assert err<1e-11;valid(actual)
                if gamma==.36 and r==.1:
                    rows.append({'input':v,'output':actual,'expected':target,'max_error':err})
    # Real dynamic classical feedback in the simulator, 6 inputs, all 4 Alice branches.
    tele=[]
    for idx,v in enumerate(states):
        qc=QuantumCircuit(3,2);qc.initialize(v,0);qc.h(1);qc.cx(1,2)
        qc.cx(0,1);qc.h(0);qc.measure(0,0);qc.measure(1,1)
        with qc.if_test((qc.clbits[1],1)):qc.x(2)
        with qc.if_test((qc.clbits[0],1)):qc.z(2)
        qc.save_density_matrix([2],label='bob')
        compiled=transpile(qc,backend,optimization_level=0)
        data=backend.run(compiled,shots=4096,seed_simulator=720+idx).result()
        assert data.success
        actual=np.array(data.data(0)['bob']);target=np.outer(v,v.conj())
        err=float(np.max(abs(actual-target)));assert err<1e-11
        counts=data.get_counts();assert sum(counts.values())==4096 and set(counts)=={'00','01','10','11'}
        tele.append({'input':v,'bob':actual,'max_error':err,'alice_counts_c1_c0':counts})
    # Statevector and stabilizer agree for a Clifford Bell circuit, with explicit qubit map.
    cliff=QuantumCircuit(2);cliff.h(1);cliff.cx(1,0);cliff.measure_all()
    samples={}
    for method in ('statevector','stabilizer'):
        res=AerSimulator(method=method,max_parallel_threads=1).run(cliff,shots=2048,seed_simulator=72).result()
        assert res.success and set(res.get_counts()) <= {'00','11'}
        samples[method]=res.get_counts()
    return {'model':'local CPU simulation, no device or cloud jobs','channel_inputs':54,
            'gamma_grid':[0,.36,1],'equilibrium_excited_grid':[0,.1,1],
            'channel_max_matrix_error':max_error,'selected_channel_samples':rows,
            'dynamic_teleportation':tele,'clifford_methods_counts':samples,
            'qiskit_bit_order':'q0 rightmost; teleportation c1c0 = A,Q; Bell A=q1 B=q0'}


def tomography():
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import DensityMatrix, Choi
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import amplitude_damping_error
    from qiskit_experiments.library import StateTomography, ProcessTomography
    backend=AerSimulator(method='density_matrix',max_parallel_threads=1)
    qc=QuantumCircuit(1);qc.ry(np.pi/3,0);qc.s(0)
    state=np.array([np.sqrt(3)/2,.5j]);target=np.outer(state,state.conj())
    qst=StateTomography(qc);qst.analysis.set_options(fitter='linear_inversion',rescale_positive=True)
    ed=qst.run(backend,shots=8192,seed_simulator=72).block_for_results(timeout=120)
    assert ed.analysis_status().name=='DONE', str(ed.errors())
    fit=np.array(ed.analysis_results('state',dataframe=True).iloc[0].value.data);valid(fit)
    assert np.max(abs(fit-target))<.025
    raw=[]
    for datum in ed.data():
        raw.append({'counts':datum['counts'],'metadata':datum['metadata'],'shots':datum['shots']})
    # Rebuild rho directly from raw X/Y/Z counts, independent of the SDK fitter.
    rvec=np.zeros(3)
    for datum in raw:
        basis=int(datum['metadata']['m_idx'][0]);n=datum['shots'];counts=datum['counts']
        rvec[[2,0,1][basis]]=(counts.get('0',0)-counts.get('1',0))/n
    x,y,z=rvec
    direct=np.array([[(1+z)/2,(x-1j*y)/2],[(x+1j*y)/2,(1-z)/2]])
    # In d=2, a trace-one Hermitian matrix outside the Bloch ball projects
    # to its positive eigenvector projector. This independently reproduces
    # the fitter's additive eigenvalue redistribution, not a guessed tolerance.
    radius=np.linalg.norm(rvec)
    independent_psd=direct if radius<=1 else np.eye(2)/2+(direct-np.eye(2)/2)/radius
    assert np.max(abs(independent_psd-fit))<1e-12
    # Full 1-qubit process tomography: 4 preparations x 3 measurement bases.
    noise=amplitude_damping_error(.36,excited_state_population=.1)
    circuit=QuantumCircuit(1);circuit.append(noise.to_instruction(),[0])
    qpt=ProcessTomography(circuit);qpt.analysis.set_options(fitter='linear_inversion',target=None)
    pd=qpt.run(backend,shots=16384,seed_simulator=73).block_for_results(timeout=120)
    assert pd.analysis_status().name=='DONE', str(pd.errors())
    fit_choi=Choi(pd.analysis_results('state',dataframe=True).iloc[0].value)
    exact=Choi(noise.to_quantumchannel())
    error=float(np.linalg.norm(fit_choi.data-exact.data))
    assert error<.065 and fit_choi.is_cp()
    trace_output=np.einsum('aibi->ab',fit_choi.data.reshape(2,2,2,2))
    tp_error=float(np.max(abs(trace_output-np.eye(2))))
    # PSD rescaling does not enforce TP. Preserve this diagnostic, don't assert exact CPTP.
    raw_process=[{'counts':d['counts'],'metadata':d['metadata'],'shots':d['shots']} for d in pd.data()]
    assert len(raw)==3 and len(raw_process)==12
    # Low-shot stress case: PSD rescaling alone need not preserve the TP affine constraint.
    low=qpt.run(backend,shots=32,seed_simulator=76).block_for_results(timeout=120)
    assert low.analysis_status().name=='DONE',str(low.errors())
    low_choi=Choi(low.analysis_results('state',dataframe=True).iloc[0].value)
    low_partial=np.einsum('aibi->ab',low_choi.data.reshape(2,2,2,2))
    assert low_choi.is_cp() and abs(np.trace(low_choi.data)-2)<1e-10
    low_counts=[{'counts':d['counts'],'metadata':d['metadata'],'shots':d['shots']} for d in low.data()]
    assert len(low_counts)==12
    return {'model':'local finite-shot simulation; trusted ideal measurement bases',
            'fitter':'linear_inversion, positive rescale, trace rescale; not exact TP constraint',
            'state_settings':3,'state_shots_per_setting':8192,'state_counts':raw,
            'state_expected':target,'state_fitted':fit,'state_raw_linear_inverse':direct,
            'state_independent_psd':independent_psd,'state_raw_bloch':rvec,'state_raw_bloch_length':float(radius),
            'state_psd_crosscheck_error':float(np.max(abs(independent_psd-fit))),
            'state_raw_eigenvalues':np.linalg.eigvalsh(direct),'state_fitted_eigenvalues':np.linalg.eigvalsh(fit),
            'state_max_abs_error':float(np.max(abs(fit-target))),
            'process_settings':12,'process_shots_per_setting':16384,'process_counts':raw_process,
            'process_expected_choi':exact.data,'process_fitted_choi':fit_choi.data,
            'process_frobenius_error':error,'process_is_cp':bool(fit_choi.is_cp()),
            'process_is_tp':bool(fit_choi.is_tp()),'process_tp_max_error':tp_error,
            'low_shot_process':{'shots_per_setting':32,'counts':low_counts,'choi':low_choi.data,
                'trace_output':low_partial,'is_cp':bool(low_choi.is_cp()),'is_tp':bool(low_choi.is_tp()),
                'tp_max_error':float(np.max(abs(low_partial-np.eye(2))))}}


def qutip_run():
    import qutip as qt
    # Units: t in us; H/hbar in rad/us; kappa in 1/us, sqrt(kappa) in 1/sqrt(us).
    kappa=.7;omega=.9;times=np.linspace(0,4,41)
    ground,excited=qt.basis(2,0),qt.basis(2,1)
    psi=(np.sqrt(3)*ground+1j*excited)/2
    h=-omega*qt.sigmaz()/2
    collapse=np.sqrt(kappa)*ground*excited.dag()
    pop=excited.proj()
    target=[]
    for t in times:
        b=.25*np.exp(-kappa*t);c=-1j*np.sqrt(3)/4*np.exp((-kappa/2+1j*omega)*t)
        target.append(np.array([[1-b,c],[c.conjugate(),b]]))
    target=np.array(target)
    opts={'store_states':True,'atol':1e-11,'rtol':1e-10,'progress_bar':''}
    me=qt.mesolve(h,psi,times,[collapse],e_ops=[pop,qt.sigmax(),qt.sigmay()],options=opts)
    me_matrices=np.array([x.full() for x in me.states]);me_error=float(np.max(abs(me_matrices-target)))
    assert me_error<2e-8
    for rho in me_matrices:valid(rho)
    mc_opts={**opts,'keep_runs_results':True,'map':'serial'}
    mc=qt.mcsolve(h,psi,times,[collapse],e_ops=[pop,qt.sigmax(),qt.sigmay()],ntraj=4096,seeds=72,options=mc_opts)
    matrices=np.array([x.full() for x in mc.average_states])
    for rho in matrices:valid(rho)
    runs=np.asarray(mc.runs_expect,dtype=float) # operator, trajectory, time
    empirical_se=np.std(runs,axis=1,ddof=1)/np.sqrt(mc.num_trajectories)
    # std_expect is population trajectory SD, not the SE of the trajectory mean.
    sdk_sd=np.asarray(mc.std_expect)
    assert np.max(abs(sdk_sd-np.std(runs,axis=1,ddof=0)))<1e-6
    # Same underlying runs: prefixes are correlated, so no fitted convergence claim.
    prefixes=[{'n':n,'jump_frequency':sum(len(t)>0 for t in mc.col_times[:n])/n,
               'expected_jump_se':float(np.sqrt(.25*(1-np.exp(-kappa*4))*(1-.25*(1-np.exp(-kappa*4)))/n))}
              for n in (256,1024,4096)]
    exact_expect=np.stack([target[:,1,1].real,2*target[:,0,1].real,-2*target[:,0,1].imag])
    mc_expect=np.asarray(mc.average_expect)
    difference=abs(mc_expect-exact_expect)
    assert np.all(difference < 6*empirical_se+2e-7)
    jumps=[len(t)>0 for t in mc.col_times];jump_probability=sum(jumps)/4096
    expected_jump=.25*(1-np.exp(-kappa*4))
    mc_matrix_error=float(np.max(abs(matrices-target)))
    # Independent Bernoulli trajectory indicator uncertainty, not hardware shot noise.
    jump_se=float(np.sqrt(expected_jump*(1-expected_jump)/4096))
    assert abs(jump_probability-expected_jump)<6*jump_se
    return {'model':'zero-temperature Markov Lindblad model, local CPU',
            'time_unit':'us','hamiltonian_over_hbar_unit':'rad/us','rate_unit':'1/us',
            'kappa':kappa,'omega':omega,'collapse_matrix':collapse.full(),'initial_state':psi.full(),
            'times_us':times,'exact_density_matrices':target,'mesolve_density_matrices':me_matrices,
            'mcsolve_density_matrices':matrices,'mesolve_max_matrix_error':me_error,
            'mcsolve_max_matrix_error':mc_matrix_error,'trajectory_count':mc.num_trajectories,
            'seed':72,'observable_order':['excited population','X','Y'],
            'exact_expect':exact_expect,'mcsolve_mean_expect':mc_expect,
            'sdk_trajectory_standard_deviations':sdk_sd,'trajectory_prefixes':prefixes,
            'empirical_standard_errors':empirical_se,'comparison_rule':'abs discrepancy < 6 empirical SE + 2e-7; regression check, not coverage proof',
            'jump_trajectories':sum(jumps),'expected_jump_probability':expected_jump,
            'observed_jump_probability':jump_probability,'jump_standard_error':jump_se}


def main():
    if not __debug__:raise RuntimeError('Run without -O: assertions must remain enabled.')
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['aer','tomography','qutip','all'],default='all');args=ap.parse_args()
    report={'python':sys.version,'platform':platform.platform(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'packages':{k:importlib.metadata.version(k) for k in ['numpy','scipy','qiskit','qiskit-aer','qiskit-experiments','qutip']},'cases':{}}
    failed=False
    for name,fn in {'aer':aer,'tomography':tomography,'qutip':qutip_run}.items():
        if args.case not in (name,'all'):continue
        try:report['cases'][name]={'status':'passed','result':pack(fn())};print(name,'passed',flush=True)
        except Exception as ex:
            failed=True;report['cases'][name]={'status':'failed','error':str(ex),'traceback':traceback.format_exc()};print(report['cases'][name]['traceback'],flush=True)
    (ROOT/(args.case+'-results.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if failed:raise SystemExit(1)

if __name__=='__main__':main()
