"""Bounded two-control GRAPE, independently propagated with scipy expm.
Run: python codes/systems/sdk/grape_control.py. Angular frequencies rad/ns.
"""
import importlib.metadata, json, platform
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from qutip import qeye,sigmax,sigmay,sigmaz
from qutip_qtrl import pulseoptim
if not __debug__: raise RuntimeError('Run without -O')
OUT=Path(__file__).resolve().parent
X,Y,Z=[q.full() for q in (sigmax(),sigmay(),sigmaz())]
TARGET=expm(-1j*np.pi*X/2)
DT=0.5; T=40.0; N=80; BOUND=0.12; DELTA=2*np.pi*0.005

def propagate(amplitudes,delta=DELTA,three=False):
    if three:
        a=np.diag(np.sqrt([1,2]),1).astype(complex)
        n=a.conj().T@a
        h0=-delta*n+(2*np.pi*(-0.2))/2*(n@(n-np.eye(3)))
        hx=(a+a.conj().T)/2; hy=(-1j*(a-a.conj().T))/2
    else: h0=delta*Z/2; hx=X/2; hy=Y/2
    u=np.eye(len(h0),dtype=complex)
    for ux,uy in amplitudes: u=expm(-1j*DT*(h0+ux*hx+uy*hy))@u
    return u

def scores(u):
    ftrace=abs(np.trace(TARGET.conj().T@u))/2
    return dict(trace_overlap=float(ftrace), qtrl_error=float(1-ftrace),
        process_overlap=float(ftrace**2), avg_gate_fidelity=float((2*ftrace**2+1)/3),
        transfer_p1=float(abs(u[1,0])**2))

if __name__=='__main__':
    np.random.seed(72014)
    result=pulseoptim.optimize_pulse_unitary(DELTA*sigmaz()/2,[sigmax()/2,sigmay()/2],qeye(2),
        -1j*sigmax(),num_tslots=N,evo_time=T,amp_lbound=-BOUND,amp_ubound=BOUND,
        fid_err_targ=1e-10,max_iter=500,max_wall_time=60,init_pulse_type='RND',
        optim_method='FMIN_L_BFGS_B',phase_option='PSU',gen_stats=True,log_level=0)
    amps=result.final_amps
    u=propagate(amps)
    assert amps.shape==(N,2) and np.max(np.abs(amps))<=BOUND+1e-12
    assert np.allclose(u,result.evo_full_final.full(),atol=1e-10)
    assert np.allclose(u.conj().T@u,np.eye(2),atol=1e-10)
    assert abs(scores(u)['qtrl_error']-result.fid_err)<1e-10
    assert result.fid_err < 1e-7
    rectangle=np.zeros_like(amps); rectangle[:,0]=np.pi/T
    # An explicitly specified one-pole sampled filter, not a claim about a real AWG.
    filtered=np.zeros_like(amps); retained=np.exp(-DT/1.0)
    prev=np.zeros(2)
    for j in range(N): prev=retained*prev+(1-retained)*amps[j]; filtered[j]=prev
    u3=propagate(amps,three=True)
    leak=[float(abs(u3[2,j])**2) for j in (0,1)]
    sweep=[dict(delta_MHz=float(f),**scores(propagate(amps,2*np.pi*f/1000))) for f in (3,4,5,6,7)]
    np.savetxt(OUT/'grape-amplitudes.csv', np.c_[np.arange(N)*DT,amps,filtered],delimiter=',',
        header='start_ns,ux_rad_per_ns,uy_rad_per_ns,filtered_ux,filtered_uy',comments='')
    data=dict(access_date='2026-10-13',python=platform.python_version(),
        versions={p:importlib.metadata.version(p) for p in ('qutip','qutip-qtrl','numpy','scipy')},
        seed=72014,duration_ns=T,step_ns=DT,slots=N,delta_rad_per_ns=DELTA,bound_rad_per_ns=BOUND,
        bound_equivalent_MHz=BOUND/(2*np.pi)*1000,iterations=result.num_iter,
        termination=result.termination_reason,independent_propagation_max_difference=float(np.max(abs(u-result.evo_full_final.full()))),
        initial=scores(propagate(result.initial_amps)),rectangle=scores(propagate(rectangle)),optimized=scores(u),
        sampled_one_pole_1ns=scores(propagate(filtered)),detuning_sweep=sweep,
        max_adjacent_step_rad_per_ns=float(np.max(abs(np.diff(amps,axis=0)))),
        three_level_alpha_MHz=-200,three_level_final_leakage_for_basis_inputs=leak,status='passed')
    (OUT/'grape-results.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
