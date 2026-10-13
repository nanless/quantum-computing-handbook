#!/usr/bin/env python3
"""Eight independent small mathematical checks. Python >=3.9, standard library only."""
import argparse, cmath, hashlib, json, math
from pathlib import Path
from foundations_lab import I,X,Y,Z,mm,mv,dagger,outer,add,scale as matrix_scale,kron,close,matrix_close,trace,kraus_apply

def scale(c,a):return matrix_scale(a,c)
R=Path(__file__).resolve().parent

def packed(x):
    if isinstance(x,complex):return [x.real,x.imag]
    if isinstance(x,dict):return {k:packed(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [packed(v) for v in x]
    return x

def case00():
    a=2*16384;b=3*8192;c=12*128;d=12*512
    assert a+b+c+d==65024
    return {'readout_calibration_shots':a,'qst_shots':b,'qpt_training_shots':c,'qpt_holdout_shots':d,'total_preparations':a+b+c+d,'settings':[2,3,12,12]}

def case01():
    alpha,beta=.12,.23;det=1-alpha-beta
    A=[[1-alpha,beta],[alpha,1-beta]]
    inv=[[A[1][1]/det,-A[0][1]/det],[-A[1][0]/det,A[0][0]/det]]
    matrix_close(mm(inv,A),I)
    p=[.75,.25];q=mv(A,p);recovered=mv(inv,q)
    close(q[0],.7175);close(recovered[0],.75)
    perturb=mv(inv,[.01,-.01]);close(perturb[0],.01/.65)
    # A plausible noisy frequency may yield a signed estimate, not a physical probability.
    signed=mv(inv,[.9,.1]);assert signed[1]<0
    return {'assignment_columns':A,'inverse':inv,'ideal_probability':p,'reported_probability':q,'recovered':recovered,'input_frequency_perturbation':[.01,-.01],'corrected_perturbation':perturb,'signed_estimate':signed}

def case02():
    alpha,beta=.12,.23;d=1-alpha-beta;z=.5;m=beta-alpha+d*z
    close(m,.435);close((m-(beta-alpha))/d,z)
    n=8192;nc=16384
    measurement=(1-m*m)/(n*d*d)
    da=(z-1)/d;db=(z+1)/d
    calibration=da*da*alpha*(1-alpha)/nc+db*db*beta*(1-beta)/nc
    var=measurement+calibration
    return {'ideal_z':z,'reported_z':m,'measurement_variance':measurement,'calibration_delta_variance':calibration,'total_delta_standard_error':math.sqrt(var),'boundary':'first-order expansion, ideal stable calibration preparations'}

def case03():
    offset=.11;d=.65
    rawcorr=offset**2+d*d
    close(rawcorr,.4346);assert 2*rawcorr<1
    corrected=(rawcorr-offset*offset-offset*offset+offset**2)/(d*d)
    close(corrected,1)
    # Exhaustively sum reported joint probabilities, independent of affine correlation derivation.
    A=[[.88,.23],[.12,.77]];true=[[.5,0],[0,.5]]
    observed=[[sum(A[y][x]*A[z][w]*true[x][w] for x in (0,1) for w in (0,1)) for z in (0,1)] for y in (0,1)]
    c=sum((-1)**(y+z)*observed[y][z] for y in (0,1) for z in (0,1));close(c,rawcorr)
    return {'bell_reported_joint':observed,'reported_correlation':c,'reported_witness_sum':2*c,'corrected_correlation':corrected,'boundary':'independent classical readout errors; not device-independent Bell certification'}

def case04():
    # Alice's true m,n are uniform; asymmetric flip rates average to (alpha+beta)/2.
    e=(.12+.23)/2
    rho=[[.75,-1j*math.sqrt(3)/4],[1j*math.sqrt(3)/4,.25]]
    ks=[scale(math.sqrt((1-e)**2),I),scale(math.sqrt(e*(1-e)),X),scale(math.sqrt(e*(1-e)),Z),scale(e,mm(Z,X))]
    output=kraus_apply(ks,rho)
    bx=trace(mm(X,output)).real;by=trace(mm(Y,output)).real;bz=trace(mm(Z,output)).real
    close(by,(1-2*e)**2*math.sqrt(3)/2);close(bz,(1-2*e)*.5)
    total=[[0j,0j],[0j,0j]]
    for k in ks:total=add(total,mm(dagger(k),k))
    matrix_close(total,I)
    return {'average_record_flip_probability':e,'pauli_error_weights':[(1-e)**2,e*(1-e),e*(1-e),e*e],'output_density':output,'output_bloch':[bx,by,bz],'boundary':'ideal resources and gates; record flips already drove physical corrections'}

def case05():
    gamma=.36;r=.1;c=math.cos(math.pi/10);s=math.sin(math.pi/10);u=[[c,-s],[s,c]]
    ks=[scale(math.sqrt(1-r),[[1,0],[0,.8]]),scale(math.sqrt(1-r),[[0,.6],[0,0]]),scale(math.sqrt(r),[[.8,0],[0,1]]),scale(math.sqrt(r),[[0,0],[.6,0]])]
    J=[[0j]*4 for _ in range(4)]
    for k in ks:
        ku=mm(k,u);v=[ku[0][0],ku[1][0],ku[0][1],ku[1][1]];J=add(J,outer(v))
    ptr=[[sum(J[2*a+y][2*b+y] for y in (0,1)) for b in (0,1)] for a in (0,1)];matrix_close(ptr,I)
    plusi=outer([1/math.sqrt(2),1j/math.sqrt(2)])
    direct=kraus_apply([mm(k,u) for k in ks],plusi)
    M=scale(.5,add(I,Y));p=trace(mm(M,direct)).real
    # Choi Born formula contains ordinary input transpose, not conjugate transpose.
    prepT=[[plusi[j][i] for j in (0,1)] for i in (0,1)]
    choip=trace(mm(kron(prepT,M),J)).real;close(p,choip)
    def nll(q):return -3*math.log(q)-7*math.log(1-q)
    assert nll(.3)<nll(.3181818181818182)
    bad=add(scale(.5,kron(I,I)),scale(.1,kron(Y,I)))
    badptr=[[sum(bad[2*a+y][2*b+y] for y in (0,1)) for b in (0,1)] for a in (0,1)]
    matrix_close([[v.real for v in row] for row in badptr],I);assert abs(badptr[0][1])>.19
    return {'hermitian_real_tp_counterexample':bad,'counterexample_full_partial_trace':badptr,'analytic_rotated_damping_choi':J,'output_partial_trace':ptr,'y_plus_probability':p,'choi_born_probability':choip,'binomial_mle_p':.3,'jeffreys_posterior_mean':3.5/11,'nll_at_mle':nll(.3),'nll_at_posterior_mean':nll(3.5/11)}

def caseq1():
    alpha,beta=.12,.23
    probabilities=[]
    for phi in (0,math.pi/2,math.pi):
        p=(1+math.cos(phi))/2;q=(1-alpha)*p+beta*(1-p)
        probabilities.append({'phase_rad':phi,'ideal_zero':p,'reported_zero':q,'corrected_zero':(q-beta)/(1-alpha-beta)})
        close((q-beta)/(1-alpha-beta),p)
    visibility=(.88-.23)/(.88+.23)
    close(visibility,.65/1.11)
    return {'phase_samples':probabilities,'reported_max':.88,'reported_min':.23,'reported_visibility':visibility,'ideal_visibility':1,'boundary':'binary misassignment without loss, not the efficiency model of F72-Q1'}

def caseq2():
    # At t=0, Omega is exponentially small but not zero; trace-preserving driven Bloch RHS.
    omega=lambda t:1.1*math.exp(-((t-1.5)/.35)**2)
    def rhs(t,r):return [-.7*r[1]-.2*r[0],.7*r[0]-omega(t)*r[2]-.2*r[1],omega(t)*r[1]+.4*(1-r[2])]
    def rk4(n):
        r=[0.,1.,0.];dt=3/n
        for k in range(n):
            t=k*dt;a=rhs(t,r);b=rhs(t+dt/2,[r[j]+dt*a[j]/2 for j in range(3)])
            c=rhs(t+dt/2,[r[j]+dt*b[j]/2 for j in range(3)]);d=rhs(t+dt,[r[j]+dt*c[j] for j in range(3)])
            r=[r[j]+dt*(a[j]+2*b[j]+2*c[j]+d[j])/6 for j in range(3)]
        return r
    ref=rk4(2400);rows=[]
    for n in (150,300,600):
        got=rk4(n);err=max(abs(got[j]-ref[j]) for j in range(3));rows.append({'steps':n,'final_bloch':got,'max_difference_from_2400':err})
        assert sum(x*x for x in got)<=1+1e-10
    assert rows[0]['max_difference_from_2400']>rows[1]['max_difference_from_2400']>rows[2]['max_difference_from_2400']
    return {'time_unit':'us','final_time':3,'reference_2400_steps':ref,'rk4_convergence':rows,'initial_derivative':rhs(0,[0,1,0]),'boundary':'finite-input convergence; no statistical sampling or package calls'}
CASES={'00':case00,'01':case01,'02':case02,'03':case03,'04':case04,'05':case05,'q1':caseq1,'q2':caseq2}
def main():
    if not __debug__:raise RuntimeError('Run without -O')
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=list(CASES)+['all'],default='all');a=ap.parse_args()
    result={'scope':'synthetic mathematical checks, standard library only','cases':{}}
    for key,fn in CASES.items():
        if a.case in ('all',key):result['cases'][key]=packed(fn());print(key,'passed')
    (R/('round73-'+a.case+'-results.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
