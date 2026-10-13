#!/usr/bin/env python3
"""Standard-library independent checks for eight S72 chapters.
Uses archived real SDK samples/waveforms, never imports SDK or vendor files.
python3 codes/systems/round72_checks.py --case all
"""
import argparse,ast,csv,cmath,hashlib,json,math,struct,zipfile
from fractions import Fraction
from pathlib import Path
if not __debug__: raise RuntimeError('Run without -O')
ROOT=Path(__file__).resolve().parent;SDK=ROOT/'sdk'
def close(x,y,tol=1e-10): assert abs(x-y)<tol,(x,y,tol)
def load(name):return json.loads((SDK/name).read_text())
def eye(n):return [[complex(i==j) for j in range(n)] for i in range(n)]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,s):return [[x*s for x in r] for r in a]
def exponential(a):
    # Independent Taylor sum for matrices with norm bounded below 2 in this experiment.
    norm=max(sum(abs(x) for x in r) for r in a);assert norm<2
    out=eye(len(a));term=eye(len(a))
    for k in range(1,50):term=scale(mul(term,a),1/k);out=add(out,term)
    return out
X=[[0,1],[1,0]];Y=[[0,-1j],[1j,0]];Z=[[1,0],[0,-1]]
def wave():
    with (SDK/'grape-amplitudes.csv').open() as f:return [[float(x) for x in row] for row in list(csv.reader(f))[1:]]
def unpack_npy(raw):
    assert raw[:6]==b'\x93NUMPY'
    version=raw[6];size=struct.unpack('<H' if version==1 else '<I',raw[8:10 if version==1 else 12])[0]
    start=10 if version==1 else 12;meta=ast.literal_eval(raw[start:start+size].decode())
    assert not meta['fortran_order']
    return meta,raw[start+size:]
def saved_failure_counts(row):
    stem=f"d{row['distance']}-p{row['noise_each']:g}"
    raw=(SDK/f'{stem}-samples.npz').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['raw_sample_sha256']
    with zipfile.ZipFile(SDK/f'{stem}-samples.npz') as z:
        ma,a=unpack_npy(z.read('actual.npy'));mp,p=unpack_npy(z.read('prediction.npy'));mf,f=unpack_npy(z.read('failures.npy'))
    assert ma['descr']==mp['descr']=='|u1' and mf['descr']=='|b1'
    assert ma['shape']==mp['shape']==(row['shots'],1) and mf['shape']==(row['shots'],)
    computed=[(x&1)!=(y&1) for x,y in zip(a,p)]
    assert computed==[bool(x) for x in f]
    return sum(computed)
def cdf(n,k,p):
    if p==0:return 1.
    if p==1:return float(k>=n)
    term=math.exp(n*math.log1p(-p));total=term
    for j in range(k):term*=((n-j)/(j+1))*(p/(1-p));total+=term
    return total
def invert_cdf(n,k,target):
    lo,hi=0.,1.
    for _ in range(90):
        mid=(lo+hi)/2
        if cdf(n,k,mid)>target:lo=mid
        else:hi=mid
    return (lo+hi)/2
def ci(n,k):
    return [0 if k==0 else invert_cdf(n,k-1,.975),1 if k==n else invert_cdf(n,k,.025)]
def case09():
    p=.001
    # Six cardinal inputs: X,Y,Z squared expectations sum to 1 in each pure state.
    f=sum((1-p)+p/3 for _ in range(6))/6
    close(f,1-2*p/3);r2=4*p/5;close(r2,.0008)
    return {'p':p,'qubit_average_overlap':f,'two_qubit_average_error':r2,'reverse_two_qubit_p_for_r001':.001*5/4}
def case10():
    rows=load('stim-matching-results.json')['cases'];out=[]
    for row in rows:
        k=saved_failure_counts(row);assert k==row['failures']
        out.append({'d':row['distance'],'rounds':row['rounds'],'p':row['noise_each'],'shots':row['shots'],'recounted_failures':k})
    return {'raw_bitpacked_recount':out,'boundary':'No SDK resampling or redecoding; tests the archived logical evidence'}
def case11():
    rows=load('stim-matching-results.json')['cases'];out=[]
    for row in rows:
        interval=ci(row['shots'],row['failures'])
        for a,b in zip(interval,row['exact_binomial_95']):close(a,b,1e-11)
        out.append({'d':row['distance'],'p':row['noise_each'],'binomial_tail_inversion':interval})
    upper=1-math.exp(math.log(.05)/20000);close(upper,.000149775396777)
    return {'independent_CDF_intervals':out,'zero_failure_one_sided_95_upper':upper}
def case12():
    n=load('sequence-results.json');em=dict(n['emissions']);ar=dict(n['arrivals']);ack=dict(n['acknowledgments'])
    assert len(em)==1000 and len(ar)==len(ack)==624 and set(ar)==set(ack)
    for seq,t in ar.items():assert t-em[seq]==50_000_000
    for seq,t in ack.items():assert t-em[seq]==110_000_000
    eta=10**(-n['attenuation_dB_per_m']*n['distance_m']/10);close(eta,n['eta_expected'])
    c=load('liboqs-build-run.json');assert c['status']=='passed'
    sizes=[[r[k] for k in ('public_key_bytes','secret_key_bytes','ciphertext_bytes','shared_secret_bytes')] for r in c['algorithms']]
    assert sizes==[[800,1632,768,32],[1184,2400,1088,32],[1568,3168,1568,32]]
    assert all(r['valid_roundtrips']==r['tampered_different_secrets']==10 for r in c['algorithms'])
    return {'network_received':len(ar),'eta':eta,'ack_delay_us':110,'kem_bytes':sizes,'scope':'Archived C run and network event checks, no security proof'}
def pauli_propagate():
    u=eye(2);delta=2*math.pi*.005
    for t,ux,uy,*_ in wave():
        q=math.sqrt(delta**2+ux**2+uy**2)
        k=add(add(scale(X,ux),scale(Y,uy)),scale(Z,delta))
        v=add(scale(eye(2),math.cos(q*.5/2)),scale(k,-1j*math.sin(q*.5/2)/q))
        u=mul(v,u)
    return u
def case14():
    u=pauli_propagate();g=abs(1j*(u[1][0]+u[0][1]))/2
    close(g,load('grape-results.json')['optimized']['trace_overlap'],1e-12)
    return {'Pauli_closed_form_overlap':g,'average_gate_fidelity':(2*g*g+1)/3,'g_error':1-g}
def case15():
    counts=case10();assert len(counts['raw_bitpacked_recount'])==4
    r=load('saved-results-verification.json');assert r['status']=='passed'
    close(case14()['Pauli_closed_form_overlap'],r['trace_overlap'],1e-12)
    return {'raw_samples_hashed':4,'waveform_rebuilt':True,'scope':'Internal evidence consistency, not model correctness or cross-machine seed identity'}
def case19():
    services=[Fraction(4,5)]*20;services[2]=4;end=Fraction(0);rows=[]
    for n,s in enumerate(services):
        start=max(Fraction(n),end);end=start+s;latency=end-n
        rows.append({'job':n,'start':float(start),'finish':float(end),'latency':float(latency),'miss':latency>2})
    assert sum(r['miss'] for r in rows)==10 and max(r['latency'] for r in rows)==4
    close(float(sum(services)/20),.96)
    return {'rational_queue':rows,'mean_service_us':.96,'max_latency_us':4,'misses':10}
def caseq3():
    a=[[0,1,0],[0,0,math.sqrt(2)],[0,0,0]];adag=[[a[j][i] for j in range(3)] for i in range(3)]
    hx=scale(add(a,adag),.5);hy=scale(add(a,scale(adag,-1)),-.5j)
    delta=2*math.pi*.005;alpha=-2*math.pi*.2
    h0=[[0,0,0],[0,-delta,0],[0,0,-2*delta+alpha]];u=eye(3)
    for t,ux,uy,*_ in wave():u=mul(exponential(scale(add(add(h0,scale(hx,ux)),scale(hy,uy)),-.5j)),u)
    leak=[abs(u[2][j])**2 for j in (0,1)]
    expected=load('grape-results.json')['three_level_final_leakage_for_basis_inputs']
    for x,y in zip(leak,expected):close(x,y,1e-12)
    dagger=[[u[j][i].conjugate() for j in range(3)] for i in range(3)]
    uu=mul(dagger,u);error=max(abs(uu[i][j]-(i==j)) for i in range(3) for j in range(3));assert error<1e-12
    return {'Taylor3D_leakage':leak,'unitarity_max_error':error,'terms_per_exponential':49}
CASES={'09':case09,'10':case10,'11':case11,'12':case12,'14':case14,'15':case15,'19':case19,'q3':caseq3}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['all']+list(CASES),default='all');args=ap.parse_args()
    results={name:fn() for name,fn in CASES.items() if args.case in ('all',name)}
    report={'access_date':'2026-10-13','implementation':'Python standard library only; independent formulas and archived SDK data','cases':results,'status':'passed'}
    (ROOT/('round72-results.json' if args.case=='all' else f'round72-{args.case}-results.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':list(results),'status':'passed'},ensure_ascii=False))
