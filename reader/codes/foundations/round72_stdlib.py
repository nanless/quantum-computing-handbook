#!/usr/bin/env python3
"""Independent stdlib rechecks of saved F72 SDK outputs; no SDK imports/reruns."""
import argparse, cmath, hashlib, json, math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation_reports import write_result
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'round72-results.json'
def matrix(values):return [[complex(*v) for v in row] for row in values]
def equal(a,b,tol=1e-10):assert max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb))<tol

def recheck(case,r):
    if case=='00':
        for counts in r.values():assert set(counts)=={'00','11'} and sum(counts.values())==2048
    elif case=='01':
        a=r['angle_rad']/2;c=math.cos(a);s=math.sin(a)
        expected=[[c,-1j*s],[-1j*s,c]]
        for k in ['matrix_expected','scipy','qutip','qiskit']:equal(matrix(r[k]),expected)
        assert abs(r['elementwise_wrong_column_norm_squared']-2)<1e-12
    elif case=='02':
        bloch=[0.,0.,0.]
        # Experiments basis indices 0=Z,1=X,2=Y.
        for record in r['state_counts']:
            counts=record['counts'];n=sum(counts.values());assert n==record['shots']
            bloch[{0:2,1:0,2:1}[record['metadata']['m_idx'][0]]]=(counts.get('0',0)-counts.get('1',0))/n
        assert max(abs(x-y) for x,y in zip(bloch,r['state_raw_bloch']))<1e-12
        length=math.sqrt(sum(x*x for x in bloch));scale=max(1,length)
        x,y,z=[v/scale for v in bloch]
        equal(matrix(r['state_fitted']),[[(1+z)/2,(x-1j*y)/2],[(x+1j*y)/2,(1-z)/2]])
    elif case=='03':
        g=r['gamma'];p=r['r'];q=math.sqrt(1-g)
        equal(matrix(r['joint_density']),[[.5*(1-g*p),0,0,q/2],[0,g*p/2,0,0],[0,0,g*(1-p)/2,0],[q/2,0,0,.5*(1-g*(1-p))]])
        equal(matrix(r['alice']),[[.5,0],[0,.5]])
        equal(matrix(r['bob']),[[.5+g*(.5-p),0],[0,.5-g*(.5-p)]])
        lowest=(g-math.sqrt(g*g*(2*p-1)**2+4*(1-g)))/4
        assert abs(lowest-min(r['partial_transpose_eigenvalues']))<1e-12 and lowest<0
    elif case=='04':
        counts=r['counts_c1_c0'];n=sum(counts.values());assert n==8192
        factor=sum((1 if key[-1]=='0' else -1)*count for key,count in counts.items())/n
        inp=[complex(*v) for v in r['input']];off=inp[0]*inp[1].conjugate()*factor
        equal(matrix(r['sample_ensemble']),[[abs(inp[0])**2,off],[off.conjugate(),abs(inp[1])**2]])
    elif case=='05':
        for low in [False,True]:
            info=r['low_shot_process'] if low else r
            choi=matrix(info['choi'] if low else info['process_fitted_choi'])
            # Input first/output second: output partial trace must be I_input.
            trace=[[sum(choi[2*i+b][2*j+b] for b in range(2)) for j in range(2)] for i in range(2)]
            error=max(abs(trace[i][j]-(i==j)) for i in range(2) for j in range(2))
            target=info['tp_max_error'] if low else info['process_tp_max_error']
            assert abs(error-target)<1e-12
            if low:assert error>.04 and not info['is_tp']
            else:assert error<1e-10 and info['process_is_tp']
    elif case=='q1':
        c=r['counts_flag_port'];n=sum(c.values());a=c['00'];b=c['01']
        assert a==r['detected_0'] and b==r['detected_1'] and c['11']==r['lost']
        assert abs(a/(a+b)-r['conditional_p0'])<1e-12
        assert abs((a+b)/n-r['throughput'])<1e-12
        assert abs(r['eta0']/(r['eta0']+r['eta1'])-r['expected_conditional_p0'])<1e-12
    elif case=='q2':
        a=complex(*r['initial_state'][0][0]);b=complex(*r['initial_state'][1][0]);k=r['kappa'];w=r['omega']
        for t,exact,master in zip(r['times_us'],r['exact_density_matrices'],r['mesolve_density_matrices']):
            p=abs(b)**2*math.exp(-k*t);off=a*b.conjugate()*cmath.exp((-k/2+1j*w)*t)
            ref=[[1-p,off],[off.conjugate(),p]]
            equal(matrix(exact),ref);equal(matrix(master),ref,1e-8)
        expected_jump=abs(b)**2*(1-math.exp(-k*r['times_us'][-1]))
        assert abs(expected_jump-r['expected_jump_probability'])<1e-12
        assert abs(r['jump_trajectories']/r['trajectory_count']-r['observed_jump_probability'])<1e-12
    return {'status':'passed','scope':'saved SDK output independently recalculated; SDK not rerun'}
def main():
    if not __debug__:raise RuntimeError('Assertions require running without -O')
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',default='all',choices=['all','00','01','02','03','04','05','q1','q2']);args=parser.parse_args()
    data=json.loads(SOURCE.read_text());selected=data['cases'] if args.case=='all' else {args.case:data['cases'][args.case]}
    results={key:recheck(key,value) for key,value in selected.items()}
    report={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'cases':results}
    write_result(HERE/('round72-stdlib-'+args.case+'.json'), json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
