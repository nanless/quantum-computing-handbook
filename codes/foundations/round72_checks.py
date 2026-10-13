#!/usr/bin/env python3
"""Eight chapter connections to installed official SDKs; local only, assertions on."""
import argparse, json, hashlib, sys
from pathlib import Path
import numpy as np
from sdk.validate_sdks import aer, tomography, qutip_run, pack, valid
ROOT=Path(__file__).resolve().parent

def mathematics():
    from scipy.linalg import expm
    import qutip as qt
    from qiskit.circuit.library import RXGate
    X=np.array([[0,1],[1,0]],complex);a=np.pi/4
    expected=np.cos(a)*np.eye(2)-1j*np.sin(a)*X
    scipy=expm(-1j*a*X);qutip=(-1j*a*qt.sigmax()).expm().full()
    qiskit=np.asarray(RXGate(2*a))
    for matrix in (scipy,qutip,qiskit):assert np.max(abs(matrix-expected))<1e-12
    wrong=np.exp(-1j*a*X)
    return {'angle_rad':2*a,'matrix_expected':expected,'scipy':scipy,'qutip':qutip,'qiskit':qiskit,
            'elementwise_wrong':wrong,'elementwise_wrong_column_norm_squared':float(np.vdot(wrong[:,0],wrong[:,0]).real)}

def local_damping():
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import DensityMatrix, partial_trace
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import amplitude_damping_error
    g=.36;r=.1;qc=QuantumCircuit(2);qc.h(1);qc.cx(1,0)
    qc.append(amplitude_damping_error(g,excited_state_population=r).to_instruction(),[0]);qc.save_density_matrix()
    rho=np.asarray(AerSimulator(method='density_matrix',max_parallel_threads=1).run(qc,shots=1).result().data(0)['density_matrix'])
    exact=np.array([[1-g*r,0,0,np.sqrt(1-g)],[0,g*r,0,0],[0,0,g*(1-r),0],[np.sqrt(1-g),0,0,1-g*(1-r)]])/2
    assert np.max(abs(rho-exact))<1e-12;valid(rho)
    alice=partial_trace(DensityMatrix(rho),[0]).data
    bob=partial_trace(DensityMatrix(rho),[1]).data
    assert np.max(abs(alice-np.eye(2)/2))<1e-12
    assert np.max(abs(bob-np.diag([.644,.356])))<1e-12
    pt=rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
    spectrum=np.linalg.eigvalsh(pt)
    analytic=(g-np.sqrt(g*g*(2*r-1)**2+4*(1-g)))/4
    assert abs(spectrum.min()-analytic)<1e-12 and spectrum.min()<0
    return {'gamma':g,'r':r,'qiskit_map':'A=q1(left), B=q0(right)','joint_density':rho,'alice':alice,'bob':bob,
            'partial_transpose_eigenvalues':spectrum,'minimum_eigenvalue_formula':float(analytic)}

def missing_feedback():
    from qiskit import QuantumCircuit,transpile
    from qiskit_aer import AerSimulator
    v=np.array([np.sqrt(3),1j])/2;backend=AerSimulator(method='density_matrix',max_parallel_threads=1)
    qc=QuantumCircuit(3,2);qc.initialize(v,0);qc.h(1);qc.cx(1,2);qc.cx(0,1);qc.h(0)
    qc.measure(0,0);qc.measure(1,1)
    with qc.if_test((qc.clbits[1],1)):qc.x(2)
    qc.save_density_matrix([2],label='bob')
    result=backend.run(transpile(qc,backend,optimization_level=0),shots=8192,seed_simulator=74).result()
    actual=np.asarray(result.data(0)['bob']);expected=np.diag([.75,.25]);valid(actual)
    assert np.max(abs(actual-expected))<.025
    return {'omitted':'Z conditioned on c0=Q','retained':'X conditioned on c1=A','counts_c1_c0':result.get_counts(),
            'input':v,'ideal_ensemble':expected,'sample_ensemble':actual,'max_error':float(np.max(abs(actual-expected)))}

def detector():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    eta0=1.;eta1=.25;phi=np.pi/2
    qc=QuantumCircuit(2,2);qc.h(0);qc.p(phi,0);qc.h(0)
    # Flag q1 starts 0: controlled Ry leaves it 0 with probability eta1 for port 1.
    qc.cry(2*np.arccos(np.sqrt(eta1)),0,1);qc.measure([0,1],[0,1])
    result=AerSimulator(max_parallel_threads=1).run(qc,shots=8192,seed_simulator=75).result()
    counts=result.get_counts();n0=counts.get('00',0);n1=counts.get('01',0);survive=n0+n1
    assert sum(counts.values())==8192 and counts.get('10',0)==0
    conditional=n0/survive;throughput=survive/8192
    expected_p0=(1+np.cos(phi))/2;expected_survive=eta0*expected_p0+eta1*(1-expected_p0)
    expected_cond=eta0*expected_p0/expected_survive
    assert abs(conditional-expected_cond)<.025 and abs(throughput-expected_survive)<.025
    return {'phase_rad':phi,'eta0':eta0,'eta1':eta1,'shots':8192,'counts_flag_port':counts,
            'detected_0':n0,'detected_1':n1,'lost':8192-survive,'conditional_p0':conditional,
            'throughput':throughput,'expected_conditional_p0':expected_cond,'expected_throughput':expected_survive,
            'model':'ideal ancillary flag dilation of unequal output detector efficiencies; synthetic data'}

def main():
    if not __debug__:raise SystemExit('Run without -O.')
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['all','00','01','02','03','04','05','q1','q2'],default='all');args=ap.parse_args()
    sdk=json.loads((ROOT/'sdk/all-results.json').read_text())
    assert all(v['status']=='passed' for v in sdk['cases'].values()),'Run SDK validator first.'
    cases={}
    # Saved results are reused with explicit hash: the SDK validator performs the full fits/solves.
    a=sdk['cases']['aer']['result'];t=sdk['cases']['tomography']['result'];q=sdk['cases']['qutip']['result']
    for name,fn in {'00':lambda:a['clifford_methods_counts'],'01':mathematics,'02':lambda:t,
                    '03':local_damping,'04':missing_feedback,'05':lambda:t,'q1':detector,'q2':lambda:q}.items():
        if args.case not in ('all',name):continue
        cases[name]=pack(fn());print(name,'passed',flush=True)
    report={'seed_base':72,'sdk_result_sha256':hashlib.sha256((ROOT/'sdk/all-results.json').read_bytes()).hexdigest(),
            'packages':sdk['packages'],'cases':cases,'scope':'local official SDK simulations; 00/02/05/q2 reuse the linked full validation report'}
    (ROOT/'round72-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
