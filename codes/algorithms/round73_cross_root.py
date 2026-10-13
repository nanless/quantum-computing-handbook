#!/usr/bin/env python3
"""Independent bit-action/spectral review of root's real dynamic-MPF records."""
import json, math, pathlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]

def ham_from_bit_action(edges):
    h=np.zeros((16,16),complex)
    for x in range(16):
        for j in edges:
            z0=1-2*((x>>(3-j))&1); z1=1-2*((x>>(2-j))&1)
            h[x,x]+=.3*z0*z1
            flip=x^(1<<(3-j))^(1<<(2-j)); h[flip,x]+=.4-.2*z0*z1
    return h

def propagator(h,t):
    ev,v=np.linalg.eigh(h);return (v*np.exp(-1j*ev*t))@v.conj().T

def main():
    original=json.loads((ROOT/'codes/sdk/round73/dynamic-mpf-results.json').read_text())
    e=ham_from_bit_action([0,2]);o=ham_from_bit_action([1]);h=e+o
    psi=np.eye(16,dtype=complex)[:,5]
    def s2(t):return propagator(e,t/2)@propagator(o,t)@propagator(e,t/2)
    orders=[]
    for p in [1/(4*4**(1/3)),1/(4-4**(1/3))]:
        errors=[]
        for dt in [.1,.05,.025]:
            u=np.eye(16,dtype=complex)
            for fraction in [p,p,1-4*p,p,p]:u=s2(fraction*dt)@u
            exact=propagator(h,1.2)@psi;v=np.linalg.matrix_power(u,round(1.2/dt))@psi
            errors.append(float(np.linalg.norm(v-exact)))
        orders.append(dict(p=p,cubic=4*p**3+(1-4*p)**3,errors=errors,ratios=[errors[0]/errors[1],errors[1]/errors[2]]))
    for a,b in zip(orders,original['reference_order_counterexample']):
        assert np.max(abs(np.array(a['errors'])-b['state_errors']))<1e-12
    rows=[]
    for row in original['records']:
        t=row['time'];states=[np.linalg.matrix_power(s2(t/k),k)@psi for k in [2,3,4]];true=propagator(h,t)@psi
        m=np.array([[abs(np.vdot(x,y))**2 for y in states] for x in states]);l=np.array([abs(np.vdot(x,true))**2 for x in states])
        assert np.max(abs(m-np.array(row['M_dense'])))<1e-12
        assert np.max(abs(l-np.array(row['L_dense'])))<1e-12
        checks=[]
        for rec in row['references']:
            c=np.array(rec['weights']);rho=sum(cj*np.outer(v,v.conj()) for cj,v in zip(c,states));target=np.outer(true,true.conj())
            err=float(np.linalg.norm(rho-target));minimum=float(np.linalg.eigvalsh(rho)[0])
            assert abs(err-rec['frobenius_error'])<2e-12
            assert abs(minimum-rec['rho_min_eigenvalue'])<1e-12
            gradient=2*(m@c-l);projected=gradient-gradient.mean()
            # Direct output is primary: ill-conditioned coefficients need not match.
            checks.append(dict(dt=rec['dt_reference'],direct_error=err,min_eigenvalue=minimum,coefficient_delta=rec['weight_delta'],projected_gradient_norm=float(np.linalg.norm(projected)),gamma=sum(abs(c))))
        rows.append(dict(time=t,gram_condition=np.linalg.cond(m),checks=checks))
    out=dict(status='passed',scope='independent Hamiltonian via X/Y/Z bit action and eigh, not root kron/expm; output and convergence checks',orders=orders,records=rows)
    (ROOT/'codes/algorithms/round73-cross-root-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
