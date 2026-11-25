"""Standard-library independent round73 derivations and archived evidence checks.
Run python3 codes/systems/round73_checks.py --case all; no SDK, network, or device.
"""
import argparse, ast, csv, fractions, hashlib, json, math, struct, zipfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation_reports import write_result
if not __debug__: raise RuntimeError('Validation requires assertions; do not run with -O')
HERE=Path(__file__).resolve().parent; SDK=HERE/'sdk73'
def read(name):return json.loads((SDK/name).read_text())
def array_npy(data):
    assert data[:6]==b'\x93NUMPY'; version=data[6]
    size=2 if version==1 else 4; hlen=int.from_bytes(data[8:8+size],'little'); start=8+size+hlen
    header=ast.literal_eval(data[8+size:start].decode().strip()); assert not header['fortran_order']
    dtype=header['descr']; raw=data[start:]; shape=header['shape']
    formats={'|u1':'B','|b1':'?','<i8':'q'}
    if dtype not in formats: return shape,raw
    result=list(struct.unpack('<'+formats[dtype]*math.prod(shape),raw));return shape,result

def archived_qec():
    d=read('qec-grid-results.json'); rows=d['cases']+d['controls']; assert len(d['cases'])==18
    for r in rows:
        path=SDK/r['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==r['raw_sha256']
        with zipfile.ZipFile(path) as z:
            arrays={name[:-4]:array_npy(z.read(name)) for name in z.namelist()}
        a=arrays['actual'][1];o=arrays['ordinary'][1];c=arrays['correlated'][1]
        assert len(a)==len(o)==len(c)==r['shots']
        fo=[x!=y for x,y in zip(a,o)];fc=[x!=y for x,y in zip(a,c)]
        assert sum(fo)==r['ordinary_failures'] and sum(fc)==r['correlated_failures']
        assert fo==arrays['ordinary_failed'][1] and fc==arrays['correlated_failed'][1]
        assert sum(x and not y for x,y in zip(fo,fc))==r['rescued']
        assert sum(y and not x for x,y in zip(fo,fc))==r['regressed']
        assert r['ordinary_failures']-r['correlated_failures']==r['rescued']-r['regressed']
        t=sorted(arrays['service_ns'][1]);assert len(t)==1000 and min(t)>0
        for q,v in r['service_ns_quantiles'].items():assert t[math.ceil(float(q)*len(t))-1]==v
    return rows

def case09():
    probs={'I':.96,'X':.01,'Y':.02,'Z':.01};assert abs(sum(probs.values())-1)<1e-12
    bit=probs['X']+probs['Y'];phase=probs['Z']+probs['Y'];joint=probs['Y']
    assert abs(joint/bit-2/3)<1e-12 and joint>bit*phase
    return dict(bit=bit,phase=phase,joint=joint,independent_joint=bit*phase,phase_given_bit=joint/bit)
def case10():
    rows=archived_qec();assert all(r['rounds']==7 for r in rows)
    return dict(grid_points=18,complete_grid_shots=sum(r['shots'] for r in rows if r['noise_each']>0),control_shots=sum(r['shots'] for r in rows if r['noise_each']==0),rates=36)
def case11():
    r=next(r for r in archived_qec() if r['basis']=='x' and r['distance']==7 and r['noise_each']==.006)
    a,b=r['rescued'],r['regressed'];n=a+b
    # Exact symmetry/null sign test, calculated with integers independently of scipy.
    p=min(1,2*sum(math.comb(n,j) for j in range(min(a,b)+1))/2**n)
    assert abs(p-r['paired_exact_two_sided_p'])<1e-18
    upper=1-(.05/36/2)**(1/10000)
    return dict(rescued=a,regressed=b,paired_failure_difference=(b-a)/r['shots'],exact_p=p,zero_failure_simultaneous_upper=upper)
def case12():
    d=read('sequence-entanglement-results.json');assert sum(len(v) for v in d['groups'].values())==920
    totals={}
    for name,rows in d['groups'].items():
        assert sum(r['swapped'] for r in rows)==d['counts'][name]['swapped']
        for r in rows:
            if r['swapped']:
                assert r['swap_start_ps']==200000000 and r['generated_end_updates']==4
                updates=[u for u in r['updates'] if u['protocol']=='EntanglementSwappingB' and u['state']=='ENTANGLED']
                assert len(updates)==2 and all(u['t_ps']==205000000 for u in updates)
                rho=[[complex(*z) for z in row] for row in r['matrix']]
                overlap=(rho[0][0]+rho[3][3]+rho[0][3]+rho[3][0]).real/2
                assert abs(overlap-r['true_bell_overlap'])<1e-12
                assert abs(overlap-(.9**2+.1**2/3 if name=='mixed_input' else 1))<1e-10
                if name=='finite_cutoff':assert all(e['t_ps']==510000000 for e in r['expirations']) and len(r['expirations'])==2
        totals[name]=dict(trials=len(rows),end_to_end_successes=sum(r['swapped'] for r in rows))
    before=read('sequence-unguarded-counterexample.json');assert before['metadata_fidelity']==1 and abs(before['true_bell_overlap'])<1e-10
    eta=10**(-.0002*1000/10);totals['lossy_expectation']=dict(single_photon_transmission=eta,link_success=.5*eta**2,two_link_success=(.5*eta**2)**2)
    return totals

def eye(n):return [[complex(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def dagger(a):return [[complex(z).conjugate() for z in row] for row in zip(*a)]
def expm(a):
    norm=max(sum(abs(z) for z in row) for row in a);scale=max(0,math.ceil(math.log2(norm))) if norm else 0
    b=[[z/(2**scale) for z in row] for row in a];u=eye(len(a));term=eye(len(a))
    for k in range(1,50):
        term=mm(term,b);term=[[z/k for z in row] for row in term];u=[[x+y for x,y in zip(ur,tr)] for ur,tr in zip(u,term)]
    for _ in range(scale):u=mm(u,u)
    return u

def control_matrix(filtered=False):
    amps=list(csv.DictReader((SDK/'grape-three-amplitudes.csv').open()));u=eye(3);delta=2*math.pi*.005;alpha=2*math.pi*(-.2)
    for row in amps:
        x=float(row['filtered_ux' if filtered else 'ux_rad_per_ns']);y=float(row['filtered_uy' if filtered else 'uy_rad_per_ns'])
        a=(x-1j*y)/2;h=[[0,a,0],[a.conjugate(),-delta,math.sqrt(2)*a],[0,math.sqrt(2)*a.conjugate(),-2*delta+alpha]]
        v=expm([[-.5j*z for z in hr] for hr in h]);u=mm(v,u)
    return u

def case14():
    d=read('grape-three-results.json');records={}
    for filtered,name in ((False,'optimized'),(True,'one_ns_discrete_filter')):
        u=control_matrix(filtered);m=[row[:2] for row in u[:2]];target=[[0,-1j],[-1j,0]]
        a=mm(dagger(target),m);survival=sum(abs(z)**2 for row in m for z in row)/2
        avg=(2*survival+abs(a[0][0]+a[1][1])**2)/6
        leak=[abs(u[2][j])**2 for j in (0,1)]
        assert abs(avg-d[name]['haar_unconditional_target_overlap'])<1e-10
        assert max(abs(x-y) for x,y in zip(leak,d[name]['basis_leakage']))<1e-10
        # The six Bloch-axis pure states are a 2-design, an independent finite average.
        states=[[1,0],[0,1],[2**-.5,2**-.5],[2**-.5,-2**-.5],[2**-.5,1j*2**-.5],[2**-.5,-1j*2**-.5]]
        six=sum(abs(sum(v[i].conjugate()*a[i][j]*v[j] for i in range(2) for j in range(2)))**2 for v in states)/6
        assert abs(six-avg)<1e-12
        records[name]=dict(leakage=leak,survival=survival,unconditional_overlap=avg,six_state_overlap=six)
    return records
def case15():
    # Source-independent Bell density counterexample: wrong cross outer product is not a density matrix.
    ph=[2**-.5,0,0,2**-.5];ps=[0,2**-.5,2**-.5,0]
    cross=[[x*y.conjugate() for y in ps] for x in ph]
    correct=[[x*y.conjugate() for y in ps] for x in ps]
    assert abs(sum(cross[j][j] for j in range(4)))<1e-12
    assert abs(sum(correct[j][j] for j in range(4))-1)<1e-12
    assert any(abs(cross[i][j]-cross[j][i].conjugate())>.1 for i in range(4) for j in range(4))
    return dict(wrong_cross_trace=0,correct_projector_trace=1,wrong_cross_is_hermitian=False)
def case19():
    F=fractions.Fraction
    arrivals=[F(a) for a in (0,1,2,3,4)]
    service=[F(4,5),F(4,5),F(4,1),F(4,5),F(4,5)]
    end=F(0);rows=[]
    for a,s in zip(arrivals,service):
        start=max(a,end);wait=start-a;end=start+s;resp=end-a
        rows.append(dict(arrival=float(a),service=float(s),wait=float(wait),response=float(resp)))
    expected_responses=[F(4,5),F(4,5),F(4,1),F(19,5),F(18,5)]
    assert [r['response'] for r in rows]==[float(x) for x in expected_responses]
    assert max(r['response'] for r in rows)==4.0
    assert rows[3]['wait']==3.0 and rows[4]['wait']==2.8
    # A deterministic queue demonstration independent of machine timing samples.
    return dict(time_unit='us',rows=rows,max_response=4.0,p99_observed_service_not_a_deadline_bound=True)
def caseq3():
    d=case14();leak_plus=abs((.1+.1)/math.sqrt(2))**2;leak_minus=abs((.1-.1)/math.sqrt(2))**2
    assert abs(leak_plus-.02)<1e-12 and leak_minus==0
    # Positive square root on the |+> and |-> axes constructs legal orthonormal columns.
    vp=math.sqrt(.98);diag=(vp+1)/2;off=(vp-1)/2
    legal=[[diag,off],[off,diag],[.1,.1]]
    product=mm(dagger(legal),legal)
    assert max(abs(product[i][j]-(i==j)) for i in range(2) for j in range(2))<1e-12
    m=control_matrix();surv=sum(abs(m[i][j])**2 for i in (0,1) for j in (0,1))/2
    assert abs(1-surv-sum(d['optimized']['leakage'])/2)<1e-12
    return dict(average_survival=surv,average_leakage=1-surv)
CASES={'09':case09,'10':case10,'11':case11,'12':case12,'14':case14,'15':case15,'19':case19,'q3':caseq3}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['all']+list(CASES),default='all');args=p.parse_args()
    chosen=CASES if args.case=='all' else {args.case:CASES[args.case]}
    result=dict(status='passed',cases={k:f() for k,f in chosen.items()},scope='stdlib archive and mathematical checks; not SDK rerun')
    write_result(HERE/('round73-results.json' if args.case=='all' else f'round73-{args.case}-results.json'),
                 json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
