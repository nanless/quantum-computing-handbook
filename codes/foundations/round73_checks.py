#!/usr/bin/env python3
"""Eight independent small mathematical checks. Python >=3.9, standard library only."""
import argparse, cmath, hashlib, json, math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation_reports import write_result
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
    # Correct first-order partial derivatives of r(m, alpha, beta) = (m + alpha - beta)/(1 - alpha - beta):
    # dr/dalpha = (1 + r)/d, dr/dbeta = (r - 1)/d.
    da=(1+z)/d;db=(z-1)/d
    # Independent central-difference and physical-boundary checks (r=+1 => dr/dbeta=0; r=-1 => dr/dalpha=0).
    def r_inv(mv,av,bv):return (mv+av-bv)/(1-av-bv)
    eps=1e-6
    close((r_inv(m,alpha+eps,beta)-r_inv(m,alpha-eps,beta))/(2*eps),da,1e-9)
    close((r_inv(m,alpha,beta+eps)-r_inv(m,alpha,beta-eps))/(2*eps),db,1e-9)
    m_zero=beta-alpha+d*1.0;m_one=beta-alpha+d*(-1.0)
    close((r_inv(m_zero,alpha,beta+eps)-r_inv(m_zero,alpha,beta-eps))/(2*eps),0.0,1e-9)
    close((r_inv(m_one,alpha+eps,beta)-r_inv(m_one,alpha-eps,beta))/(2*eps),0.0,1e-9)
    cal_alpha=da*da*alpha*(1-alpha)/nc
    cal_beta=db*db*beta*(1-beta)/nc
    calibration=cal_alpha+cal_beta
    var=measurement+calibration
    se=math.sqrt(var)
    close(var,0.0002749724,1e-9);close(se,0.0165822920,1e-9)
    # Full 3x3 covariance for the benchmark state r = (0, sqrt(3)/2, 1/2) under shared calibration.
    true_r=[0.0,math.sqrt(3)/2,0.5]
    mu=[(beta-alpha)+d*rv for rv in true_r]
    vm=[(1-mv*mv)/(n*d*d) for mv in mu]
    da_vec=[(1+rv)/d for rv in true_r];db_vec=[(rv-1)/d for rv in true_r]
    cov3=[[ (vm[i] if i==j else 0.0)+da_vec[i]*da_vec[j]*alpha*(1-alpha)/nc+db_vec[i]*db_vec[j]*beta*(1-beta)/nc for j in range(3)] for i in range(3)]
    # Explicit comparison with the legacy swapped-derivative bug archived in sdk73/validate_sdks.py (L66) and sdk73/all-results.json.
    da_legacy=(z-1)/d;db_legacy=(z+1)/d
    cal_legacy=da_legacy*da_legacy*alpha*(1-alpha)/nc+db_legacy*db_legacy*beta*(1-beta)/nc
    var_legacy=measurement+cal_legacy
    close(var_legacy,0.0002956304606601331,1e-12)
    return {'ideal_z':z,'reported_z':m,'measurement_variance':measurement,
        'calibration_alpha_variance':cal_alpha,'calibration_beta_variance':cal_beta,
        'calibration_delta_variance':calibration,'total_delta_variance':var,
        'total_delta_standard_error':se,
        'corrected_3x3_covariance':cov3,'corrected_3x3_covariance_diag':[cov3[i][i] for i in range(3)],
        'legacy_sdk73_archive_erratum':{
            'note':'Archived sdk73/validate_sdks.py (L66) and sdk73/all-results.json swapped dr/dalpha and dr/dbeta; historical archive is preserved unmodified.',
            'swapped_calibration_delta_variance':cal_legacy,
            'swapped_total_delta_variance':var_legacy,
            'swapped_total_delta_standard_error':math.sqrt(var_legacy)
        },
        'boundary':'first-order expansion, ideal stable calibration preparations'}

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

def archive_tomography():
    directory = R / 'sdk73'
    original = json.loads((directory / 'sdk-tp-counterexample.json').read_text())
    fitted = json.loads((directory / 'qpt-results.json').read_text())['cases']['qpt']
    assert original['version'] == '0.14.2' and fitted['status'] == 'passed'
    sources = {
        'default_trace_preserving': original['choi'],
        'explicit_single_component_partial_trace': fitted['result']['sdk_gaussian_choi'],
        'independent_multinomial_mle': fitted['result']['multinomial_mle_choi'],
    }
    input_states = {'zero': outer([1, 0]), 'one': outer([0, 1]),
                    'plus_i': outer([2**-.5, 1j * 2**-.5]), 'minus_i': outer([2**-.5, -1j * 2**-.5])}
    results = {}
    for method, encoded in sources.items():
        assert len(encoded) == 4 and all(len(row) == 4 for row in encoded)
        choi = [[complex(*entry) for entry in row] for row in encoded]
        partial = [[sum(choi[2*a+y][2*b+y] for y in range(2)) for b in range(2)] for a in range(2)]
        residual = max(abs(partial[i][j] - (i == j)) for i in range(2) for j in range(2))
        totals = {}
        for name, state in input_states.items():
            probability_sum = sum(state[j][i] * partial[i][j] for i in range(2) for j in range(2))
            assert abs(probability_sum.imag) < 1e-12
            totals[name] = probability_sum.real
        results[method] = {'max_complex_tp_residual': residual, 'output_probability_sums': totals}
    default = results['default_trace_preserving']
    assert 9e-4 < default['max_complex_tp_residual'] < 9.3e-4
    assert max(abs(default['output_probability_sums'][state] - 1) for state in ('zero', 'one')) < 1e-8
    assert min(abs(default['output_probability_sums'][state] - 1) for state in ('plus_i', 'minus_i')) > 9e-4
    for method in ('explicit_single_component_partial_trace', 'independent_multinomial_mle'):
        assert results[method]['max_complex_tp_residual'] < 1e-8
        assert all(abs(value - 1) < 1e-8 for value in results[method]['output_probability_sums'].values())
    return results


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
    return {'hermitian_real_tp_counterexample':bad,'counterexample_full_partial_trace':badptr,'analytic_rotated_damping_choi':J,'output_partial_trace':ptr,'y_plus_probability':p,'choi_born_probability':choip,'binomial_mle_p':.3,'jeffreys_posterior_mean':3.5/11,'nll_at_mle':nll(.3),'nll_at_posterior_mean':nll(3.5/11),'archived_tomography':archive_tomography()}

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
    write_result(R/('round73-'+a.case+'-results.json'), json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
