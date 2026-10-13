"""Complete qutip-qtrl three-level target optimization, independent SciPy replay and stress tests."""
import json, importlib.metadata, platform
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from qutip import Qobj,qeye
from qutip_qtrl import pulseoptim
if not __debug__: raise RuntimeError('Validation requires assertions; do not run with -O')
OUT=Path(__file__).resolve().parent
N=80; DT=.5; T=N*DT; BOUND=.12; DELTA=2*np.pi*.005; ALPHA=2*np.pi*(-.2)
a=np.diag(np.sqrt([1,2]),1).astype(complex); n=a.conj().T@a
hx=(a+a.conj().T)/2; hy=-1j*(a-a.conj().T)/2
h0=-DELTA*n+ALPHA/2*(n@(n-np.eye(3)))
# Target on |2> is explicit; global phase remains irrelevant under PSU.
target=np.array([[0,-1j,0],[-1j,0,0],[0,0,1]],complex)
def propagate(amps,delta=DELTA,alpha=ALPHA):
    drift=-delta*n+alpha/2*(n@(n-np.eye(3))); u=np.eye(3,dtype=complex)
    for ux,uy in amps: u=expm(-1j*DT*(drift+ux*hx+uy*hy))@u
    return u

def score(u):
    m=u[:2,:2]; tar=target[:2,:2]
    surv=float(np.trace(m.conj().T@m).real/2)
    # Haar average target overlap without postselection, a trace-decreasing projected map.
    avg=float((np.trace(m.conj().T@m).real+abs(np.trace(tar.conj().T@m))**2)/6)
    return dict(full_trace_overlap=float(abs(np.trace(target.conj().T@u))/3),survival_basis_average=surv,
       basis_leakage=[float(abs(u[2,j])**2) for j in (0,1)],haar_unconditional_target_overlap=avg,
       max_unitarity_error=float(np.max(abs(u.conj().T@u-np.eye(3)))))

if __name__=='__main__':
    np.random.seed(73014)
    res=pulseoptim.optimize_pulse_unitary(Qobj(h0),[Qobj(hx),Qobj(hy)],qeye(3),Qobj(target),
       num_tslots=N,evo_time=T,amp_lbound=-BOUND,amp_ubound=BOUND,fid_err_targ=1e-9,
       max_iter=600,max_wall_time=120,init_pulse_type='RND',optim_method='FMIN_L_BFGS_B',phase_option='PSU',gen_stats=True,log_level=0)
    amps=res.final_amps; u=propagate(amps)
    assert np.max(abs(amps))<=BOUND+1e-12
    assert np.max(abs(u-res.evo_full_final.full()))<1e-10
    assert res.fid_err<1e-6
    assert max(score(u)['basis_leakage'])<1e-5
    a_filter=np.exp(-DT/1); filtered=[]; prev=np.zeros(2)
    for row in amps: prev=a_filter*prev+(1-a_filter)*row; filtered.append(prev.copy())
    previous=np.loadtxt(OUT.parent/'sdk'/'grape-amplitudes.csv',delimiter=',',skiprows=1)[:,1:3]
    np.savetxt(OUT/'grape-three-amplitudes.csv',np.c_[np.arange(N)*DT,amps,filtered],delimiter=',',header='start_ns,ux_rad_per_ns,uy_rad_per_ns,filtered_ux,filtered_uy',comments='')
    data=dict(date='2026-10-13',status='passed',python=platform.python_version(),versions={p:importlib.metadata.version(p) for p in ('qutip','qutip-qtrl','numpy','scipy')},
       seed=73014,slots=N,duration_ns=T,slot_ns=DT,delta_MHz=5,alpha_MHz=-200,amplitude_bound_rad_per_ns=BOUND,
       target='-i X on levels 0,1 and identity on level 2; PSU global phase ignored',iterations=res.num_iter,termination=res.termination_reason,
       qtrl_error=float(res.fid_err),independent_matrix_max_error=float(np.max(abs(u-res.evo_full_final.full()))),
       initial=score(propagate(res.initial_amps)),previous_two_level_waveform=score(propagate(previous)),optimized=score(u),
       one_ns_discrete_filter=score(propagate(filtered)),detuning_sweep=[dict(delta_MHz=f,**score(propagate(amps,2*np.pi*f/1000))) for f in (3,4,5,6,7)],
       anharmonicity_sweep=[dict(alpha_MHz=f,**score(propagate(amps,alpha=2*np.pi*f/1000))) for f in (-220,-210,-200,-190,-180)],
       maximum_adjacent_step=float(np.max(abs(np.diff(amps,axis=0)))))
    (OUT/'grape-three-results.json').write_text(json.dumps(data,indent=2)+'\n'); print(json.dumps(data,indent=2))
