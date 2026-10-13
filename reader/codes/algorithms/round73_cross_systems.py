#!/usr/bin/env python3
"""Independent systems review: raw decoder arrays, binomial-tail CI, Haar quadrature, Bell records."""
import csv,json,math,pathlib,hashlib
import numpy as np
from scipy.stats import binom
import stim,pymatching
ROOT=pathlib.Path(__file__).resolve().parents[2];SYS=ROOT/'codes/systems/sdk73'

def inverse_ci(k,n,alpha):
    tail=alpha/2
    def bisect(fn,increasing):
        lo=0.;hi=1.
        for _ in range(70):
            mid=(lo+hi)/2
            if (fn(mid)<tail)==increasing:lo=mid
            else:hi=mid
        return (lo+hi)/2
    lower=0 if k==0 else bisect(lambda p:binom.sf(k-1,n,p),True)
    upper=1 if k==n else bisect(lambda p:binom.cdf(k,n,p),False)
    return np.array([lower,upper])

def main():
    qec=json.loads((SYS/'qec-grid-results.json').read_text());qc=[]
    for r in qec['cases']+qec['controls']:
        path=SYS/r['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==r['raw_sha256']
        raw=np.load(path);det=np.unpackbits(raw['detectors'],axis=1,bitorder='little')[:,:r['detectors']];actual=np.unpackbits(raw['actual'],axis=1,bitorder='little')[:,:1];errs=[]
        dem=stim.DetectorErrorModel.from_file(path.with_suffix('.dem'))
        for method,enabled in [('ordinary',False),('correlated',True)]:
            pm=pymatching.Matching.from_detector_error_model(dem,enable_correlations=enabled);pred=pm.decode_batch(det,enable_correlations=enabled)
            err=(pred[:,0]!=actual[:,0]);errs.append(err);k=int(err.sum());assert k==r[method+'_failures']
            for alpha,label in [(.05,'ci95'),(.05/36,'simultaneous_ci')]:
                got=inverse_ci(k,r['shots'],alpha);assert np.max(abs(got-np.array(r[method+'_'+label])))<1e-10
        rescue=int(np.sum(errs[0]&~errs[1]));regress=int(np.sum(~errs[0]&errs[1]));discord=rescue+regress
        pair=1. if discord==0 else min(1.,2*sum(math.comb(discord,j) for j in range(min(rescue,regress)+1))/2**discord)
        assert abs(pair-r['paired_exact_two_sided_p'])<1e-12
        qc.append(dict(file=r['file'],shots=r['shots'],rescued=rescue,regressed=regress,paired_p=pair,decoder_replayed=True,binomial_tail_CI_inversion=True))
    amp=np.genfromtxt(SYS/'grape-three-amplitudes.csv',delimiter=',',names=True);control=[]
    gd=json.loads((SYS/'grape-three-results.json').read_text())
    nodes,weights=np.polynomial.legendre.leggauss(3)
    target=np.array([[0,-1j],[-1j,0]])
    for columns,name in [(('ux_rad_per_ns','uy_rad_per_ns'),'optimized'),(('filtered_ux','filtered_uy'),'one_ns_discrete_filter')]:
        u=np.eye(3,dtype=complex)
        for row in amp:
            x=row[columns[0]];y=row[columns[1]];z=(x-1j*y)/2
            h=np.diag([0,-2*math.pi*.005,-4*math.pi*.005+2*math.pi*(-.2)]).astype(complex)
            h[0,1]=z;h[1,0]=z.conjugate();h[1,2]=math.sqrt(2)*z;h[2,1]=math.sqrt(2)*z.conjugate()
            ev,v=np.linalg.eigh(h);step=(v*np.exp(-.5j*ev))@v.conj().T;u=step@u
        m=u[:2,:2];a=target.conj().T@m
        # Independent exact second-moment quadrature, not author's six-axis design.
        avg=0.
        for z,w in zip(nodes,weights):
            for j in range(8):
                s=np.array([math.sqrt((1+z)/2),np.exp(2j*math.pi*j/8)*math.sqrt((1-z)/2)])
                avg+=w/16*abs(np.vdot(s,a@s))**2
        closed=(np.trace(m.conj().T@m).real+abs(np.trace(a))**2)/6
        leak=abs(u[2,:2])**2
        assert abs(avg-closed)<1e-12
        assert abs(avg-gd[name]['haar_unconditional_target_overlap'])<1e-10
        assert np.max(abs(leak-gd[name]['basis_leakage']))<1e-10
        control.append(dict(name=name,Haar_quadrature_overlap=float(avg),basis_leakage=leak.tolist(),unitarity_error=float(np.max(abs(u.conj().T@u-np.eye(3))))))
    net=json.loads((SYS/'sequence-entanglement-results.json').read_text());network=[];ph=np.array([1,0,0,1])/math.sqrt(2)
    for name,records in net['groups'].items():
        for r in records:
            if not r['swapped']:continue
            arr=np.array(r['matrix']);rho=arr[:,:,0]+1j*arr[:,:,1];overlap=float(np.vdot(ph,rho@ph).real)
            assert abs(np.trace(rho)-1)<1e-10 and np.linalg.eigvalsh(rho).min()>-1e-10
            assert abs(overlap-(.8133333333333334 if name=='mixed_input' else 1))<1e-10
            if name=='finite_cutoff':
                assert len(r['expirations'])==2 and all(x['t_ps']==510000000 for x in r['expirations'])
                assert r['memory_after_window']['A']['node_id'] is None and r['memory_after_window']['C']['node_id'] is None
        if name=='short_cutoff':assert not any(r['swapped'] for r in records)
        network.append(dict(group=name,trials=len(records),swapped=sum(x['swapped'] for x in records),matrix_and_expiry_rechecked=True))
    bad=json.loads((SYS/'sequence-unguarded-counterexample.json').read_text());a=np.array(bad['matrix']);rho=a[:,:,0]+1j*a[:,:,1]
    assert abs(np.vdot(ph,rho@ph))<1e-10 and bad['metadata_fidelity']==1
    out=dict(status='passed',qec=qc,complete_shots=sum(x['shots'] for x in qc),control=control,network=network,unguarded_metadata_mismatch_confirmed=True,scope='independent archive rerun and alternate mathematics; network events not resampled, no latency retiming')
    (ROOT/'codes/algorithms/round73-cross-systems-results.json').write_text(json.dumps(out,indent=2)+'\n');print('systems cross passed',out['complete_shots'],'QEC shots')
if __name__=='__main__':main()
