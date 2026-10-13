#!/usr/bin/env python3
"""Actual MPO dynamic MPF and an independent dense reference; no cloud."""
import json,math,pathlib,time,platform,importlib.metadata
from functools import partial
import numpy as np
from scipy.linalg import expm
from quimb.tensor import LocalHam1D,MPS_computational_state,MPO_identity
from qiskit_addon_mpf.backends.quimb_tebd import MPOState,TEBDEvolver
from qiskit_addon_mpf.dynamic import setup_dynamic_lse
from qiskit_addon_mpf.costs import setup_frobenius_problem
HERE=pathlib.Path(__file__).resolve().parent

class GuardedOrder4(TEBDEvolver):
 """Explicit process-local correction; upstream installed files unchanged."""
 def _step_order4(self, **sweep_opts):
  p=1/(4-4**(1/3))
  for fraction in [p,p,1-4*p,p,p]:self._step_order2(fraction,**sweep_opts)


def main():
 if not __debug__:raise RuntimeError('Run without -O')
 X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);I=np.eye(2)
 h2=.4*np.kron(X,X)+.2*np.kron(Y,Y)+.3*np.kron(Z,Z);n=4
 bonds=[np.kron(h2,np.eye(4)),np.kron(I,np.kron(h2,I)),np.kron(np.eye(4),h2)]
 even=bonds[0]+bonds[2];odd=bonds[1];ham=even+odd
 initial=np.zeros(16,complex);initial[5]=1 # |q0 q1 q2 q3> = |0101>
 model=LocalHam1D(n,H2=h2,cyclic=False);mps=MPS_computational_state('0101');steps=[2,3,4]
 split={'max_bond':16,'cutoff':1e-13,'cutoff_mode':'abs','method':'svd','renorm':False}
 records=[];started=time.perf_counter()
 p_bad=1/(4*4**(1/3));p_good=1/(4-4**(1/3))
 assert abs(4*p_good**3+(1-4*p_good)**3)<1e-14
 assert abs(4*p_bad**3+(1-4*p_bad)**3)>.01
 reference_orders=[]
 for mode,p in [('unpatched_quimb_1.15.0',p_bad),('guarded_suzuki',p_good)]:
  errors=[]
  for dt in [.1,.05,.025]:
   s2=lambda u:expm(-1j*even*u/2)@expm(-1j*odd*u)@expm(-1j*even*u/2)
   composed=np.eye(16,dtype=complex)
   for f in [p,p,1-4*p,p,p]:composed=s2(f*dt)@composed
   state=np.linalg.matrix_power(composed,int(round(1.2/dt)))@initial
   errors.append(float(np.linalg.norm(state-expm(-1j*ham*1.2)@initial)))
  ratios=[errors[j]/errors[j+1] for j in range(2)]
  assert all(3.8<r<4.2 for r in ratios) if mode.startswith('unpatched') else all(14<r<18 for r in ratios)
  reference_orders.append({'mode':mode,'p':p,'cubic_cancellation':4*p**3+(1-4*p)**3,'state_errors':errors,'halving_ratios':ratios})
 for t in [.4,.8,1.2]:
  states=[]
  for k in steps:
   dt=t/k;s=expm(-1j*even*dt/2)@expm(-1j*odd*dt)@expm(-1j*even*dt/2)
   states.append(np.linalg.matrix_power(s,k)@initial)
  dense_exact=expm(-1j*ham*t)@initial
  M=np.array([[abs(np.vdot(a,b))**2 for b in states] for a in states]);L=np.array([abs(np.vdot(a,dense_exact))**2 for a in states])
  refs=[]
  for dt_ref in [.05,.025]:
   lse=setup_dynamic_lse(steps,t,lambda:MPOState(MPO_identity(n)),
       partial(GuardedOrder4,H=model,dt=dt_ref,order=4,split_opts=split),
       partial(TEBDEvolver,H=model,order=2,split_opts=split),mps)
   errM=float(np.max(abs(lse.A-M)));errL=float(np.max(abs(lse.b-L)))
   assert errM<2e-10 and errL<3e-7,(errM,errL)
   problem,weights=setup_frobenius_problem(lse);problem.solve(solver='CLARABEL',tol_gap_abs=1e-12,tol_feas=1e-12,tol_gap_rel=1e-12,max_iter=1000)
   assert problem.status in ('optimal','optimal_inaccurate');c=np.asarray(weights.value)
   assert abs(sum(c)-1)<1e-9
   # Independent KKT solve for constrained least squares in the dense model.
   K=np.block([[2*M,np.ones((3,1))],[np.ones((1,3)),np.zeros((1,1))]])
   dense_c=np.linalg.solve(K,np.r_[2*L,1])[:3]
   rho=sum(cj*np.outer(v,v.conj()) for cj,v in zip(c,states));target=np.outer(dense_exact,dense_exact.conj())
   error=float(np.linalg.norm(rho-target));baseline=float(np.linalg.norm(np.outer(states[-1],states[-1].conj())-target))
   assert error<baseline,(error,baseline)
   refs.append({'dt_reference':dt_ref,'M':lse.A.tolist(),'L':lse.b.tolist(),'M_dense_error':errM,'L_dense_error':errL,'weights':c.tolist(),'dense_kkt_weights':dense_c.tolist(),'weight_delta':float(np.max(abs(c-dense_c))),'gamma':float(sum(abs(c))),'solver_status':problem.status,'rho_min_eigenvalue':float(np.linalg.eigvalsh(rho)[0]),'frobenius_error':error,'best_single_error':baseline,'dense_objective':float(c@M@c-2*L@c+1)})
  records.append({'time':t,'references':refs,'M_dense':M.tolist(),'L_dense':L.tolist(),'gram_eigenvalues':np.linalg.eigvalsh(M).tolist(),'condition_number':float(np.linalg.cond(M))})
 result={'status':'passed','python':platform.python_version(),'versions':{p:importlib.metadata.version(p) for p in ['qiskit-addon-mpf','quimb','cvxpy']},'elapsed_seconds':time.perf_counter()-started,'basis':'q0 q1 q2 q3, q0 highest bit; initial0101','hamiltonian':'sum bonds (.4XX+.2YY+.3ZZ), hbar=1, dimensionless time','trotter_steps':steps,'max_bond':16,'cutoff':1e-13,'reference_order_counterexample':reference_orders,'reference_guard':'explicit subclass corrected composition; upstream unchanged','records':records,'scope':'actual MPO backend and CLARABEL; dense16D checks; reference fourth-order finite step, not mathematically exact'}
 (HERE/'dynamic-mpf-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
