#!/usr/bin/env python3
"""Independent standard-library checks, with explicit SDK archive comparison."""
import argparse, cmath, json, math, pathlib, sys
if not __debug__: raise RuntimeError('Assertions must be enabled')
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from validation_reports import ROOT as REPOSITORY, write_result

def mv(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def inner(a,b): return sum(x.conjugate()*y for x,y in zip(a,b))
def norm(v): return math.sqrt(sum(abs(x)**2 for x in v))
def matmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def encode(v): return {'real':[x.real for x in v],'imag':[x.imag for x in v]}

def phase():
    m=8; scale=4
    labels=[2*scale*(y if y<m/2 else y-m)/m for y in range(m)]
    assert labels==[0,1,2,3,-4,-3,-2,-1]
    assert abs(cmath.exp(2j*math.pi*4/8)-cmath.exp(2j*math.pi*(-4)/8))<1e-12
    a=[sum(cmath.exp(2j*math.pi*x*(-1/8-y/m)) for x in range(m))/m for y in range(m)]
    assert abs(abs(a[7])**2-1)<1e-12
    return {'labels':labels,'negative_one_label':7,'Nyquist_boundary_aliases':[4,-4]}

def hhl():
    rows=[]; c=.5; cutoff=.5; scale=4; angle=math.pi/5
    ca=math.cos(angle);sa=math.sin(angle); b=[math.sqrt(.6),1j*math.sqrt(.4)]
    beta=[ca*b[0]+sa*b[1],-sa*b[0]+ca*b[1]]
    for t in [3,4,5,6]:
        m=2**t; r=[c/(2*scale*(y if y<m/2 else y-m)/m) if abs(2*scale*(y if y<m/2 else y-m)/m)>=cutoff else 0 for y in range(m)]
        f=[]; second=[]
        for lam in [-1.1,2.3]:
            a=[sum(cmath.exp(2j*math.pi*x*(lam/(2*scale)-y/m)) for x in range(m))/m for y in range(m)]
            weights=[abs(z)**2 for z in a]; assert abs(sum(weights)-1)<1e-12
            fj=sum(p*ry for p,ry in zip(weights,r)); qj=sum(p*ry**2 for p,ry in zip(weights,r)); f.append(fj);second.append(qj)
            assert qj-fj**2>-1e-12
        p=sum(abs(z)**2*s for z,s in zip(beta,second)); pc=sum(abs(z)**2*s*s for z,s in zip(beta,f))
        rows.append({'phase_bits':t,'flag_success':p,'clean_success':pc,'garbage_given_flag':1-pc/p})
    assert rows[1]['garbage_given_flag']>rows[0]['garbage_given_flag']
    low, high = -1.1, 2.3
    off = ca*sa*(low-high)
    matrix = [[ca*ca*low+sa*sa*high, off], [off, sa*sa*low+ca*ca*high]]
    return {'C':c,'cutoff':cutoff,'scale':scale,'A':matrix,'b':encode(b),
            'eigenvalues':[low,high], 'rows':rows,
            'variance_identity':'garbage per eigenbranch = E[r^2]-(E[r])^2'}

def penalty():
    energy=(3-math.sqrt(2))/2; rows=[]
    for lam in [.5,energy,1.]:
        eig=[lam,energy,(3+math.sqrt(2))/2,3+lam]
        rows.append({'lambda':lam,'sector_energies':eig,'ground':min(eig),'one_particle_is_only_ground_sector':lam>energy})
    assert rows[0]['ground']==.5 and abs(rows[2]['ground']-energy)<1e-12
    for x0 in [0,1]:
        for x1 in [0,1]:
            lhs=(x0+x1-1)**2; z0=1-2*x0; z1=1-2*x1
            assert lhs==(1+z0*z1)/2
    return {'sector_ground_threshold':energy,'rows':rows,'pauli_penalty':'lambda*(I+Z0Z1)/2'}

def mixed():
    p=.6; overlap=.6; off=math.sqrt(p*(1-p))*overlap
    rho=[[p,off],[off,1-p]]; purity=sum(abs(z)**2 for row in rho for z in row)
    ideal=[math.sqrt(p),math.sqrt(1-p)]; f2=inner(ideal,mv(rho,ideal)).real
    assert abs(purity-.6928)<1e-12 and abs(f2-.808)<1e-12
    assert abs(1-f2-2*p*(1-p)*(1-overlap))<1e-12
    return {'rho':rho,'purity':purity,'root_fidelity':math.sqrt(f2),'squared_fidelity':f2,'same_computational_probabilities':[p,1-p]}

def polynomial():
    a=[[.2,.3],[.3,-.4]]; cube=matmul(matmul(a,a),a)
    poly=[[.8*cube[i][j]-.3*a[i][j] for j in range(2)] for i in range(2)]
    p=norm([poly[0][0],poly[1][0]])**2
    assert abs(p-.00444112)<1e-14
    x=.5; assert abs(.8*x**3-.3*x+.05)<1e-12
    return {'A':a,'P_A':poly,'selected_probability':p,'mean_retries':1/p,'walk_step4':25/64,'walk_step8':1/256}

def mbqc():
    # Exact three-qubit branches, all four outcomes. Independent partial contractions.
    alpha=math.pi/4; beta=math.pi/3; b=[1/math.sqrt(3),1j*math.sqrt(2/3)]
    h=[[1/math.sqrt(2),1/math.sqrt(2)],[1/math.sqrt(2),-1/math.sqrt(2)]]
    def j(angle,v): return mv(h,[cmath.exp(1j*angle/2)*v[0],cmath.exp(-1j*angle/2)*v[1]])
    target=j(beta,j(alpha,b));rows=[]
    # Input times |++>, with CZ01,CZ12.
    state=[b[x0]*(-1)**(x0*x1+x1*x2)/2 for x0 in [0,1] for x1 in [0,1] for x2 in [0,1]]
    for m0 in [0,1]:
        for m1 in [0,1]:
            physical_beta=(-1)**m0*beta
            result=[sum(state[4*x0+2*x1+x2]*((-1)**(m0*x0))*cmath.exp(-1j*alpha*x0)/math.sqrt(2)*((-1)**(m1*x1))*cmath.exp(-1j*physical_beta*x1)/math.sqrt(2) for x0 in [0,1] for x1 in [0,1]) for x2 in [0,1]]
            probability=norm(result)**2;out=[z/math.sqrt(probability) for z in result]
            if m1:out=out[::-1] # apply X before Z to undo X^m1 Z^m0
            if m0:out[1]*=-1
            fidelity=abs(inner(target,out));assert abs(probability-.25)<1e-12 and abs(fidelity-1)<1e-12
            rows.append({'m0':m0,'m1':m1,'physical_second_angle':physical_beta,'probability':probability,'root_fidelity_after_X_then_Z':fidelity})
    return {'alpha':alpha,'beta':beta,'target':encode(target),'branches':rows}

def tail():
    mean=.125;d=20;bound=mean/d; rare=.125/100
    assert rare<=bound
    distribution={0:1-rare,100:rare}
    actual_mean=sum(n*p for n,p in distribution.items()); assert abs(actual_mean-mean)<1e-15
    return {'mean_photon_number':mean,'cutoff_dimension':d,'Markov_tail_bound':bound,'same_energy_nonGaussian_tail':rare,'counterexample_distribution':distribution,'squeezed_gaussian_tail_round72':5.3298e-11}

def fock():
    rows=[]
    for d in [4,8,12]:
        # Actual exponential of finite anti-Hermitian generator a†-a on vacuum.
        generator=[[0j]*d for _ in range(d)]
        for n in range(1,d):generator[n][n-1]=math.sqrt(n);generator[n-1][n]=-math.sqrt(n)
        def series(stop):
            term=[1+0j]+[0j]*(d-1); value=term[:]
            for k in range(1,stop+1):
                term=[z/k for z in mv(generator,term)];value=[v+z for v,z in zip(value,term)]
            return value
        out=series(100);test=series(80);assert norm([a-b for a,b in zip(out,test)])<1e-12
        known=[math.exp(-.5)/math.sqrt(math.factorial(n)) for n in range(d)];mass=norm(known)**2;proj=[z/math.sqrt(mass) for z in known]
        n_out=norm(out); assert abs(n_out-1)<1e-12
        out_unit=[z/n_out for z in out]; overlap=inner(proj,out_unit); f=abs(overlap)
        # Use orthogonal component norm ||out_unit - <proj|out_unit>proj|| instead of sqrt(1 - f^2) to avoid catastrophic cancellation near f = 1.
        distance=norm([a-overlap*b for a,b in zip(out_unit,proj)]);gap=norm([a-b for a,b in zip(out,known)])
        rows.append({'dimension':d,'finite_generator_state':encode(out),'infinite_projected_state':known,'mass':mass,'root_fidelity_to_normalized_projection':f,'trace_distance_to_normalized_projection':distance,'raw_low_level_amplitude_difference':gap})
    assert rows[0]['trace_distance_to_normalized_projection']>.01
    assert rows[2]['trace_distance_to_normalized_projection']<rows[0]['trace_distance_to_normalized_projection']
    return {'alpha':1,'construction':'finite generator exponential compared with projection of known infinite coherent state','rows':rows,'series_80_100_agreement_boundary':'floating point convergence check, not interval arithmetic proof'}

CASES={'06':phase,'07':hhl,'08':penalty,'13':mixed,'16':polynomial,'17':mbqc,'18':tail,'q4':fock}


def compare_archive(data, path):
    """Compare the selected documented cases by identity, rather than row position."""
    if not path.is_file():
        raise FileNotFoundError(f'Missing required SDK archive {path}; use --math-only for stand-alone mathematics')
    recorded = json.loads(path.read_text(encoding='utf-8'))['cases']
    compared = []

    def close(observed, expected):
        assert math.isclose(observed, expected, rel_tol=0, abs_tol=1e-12), (observed, expected)

    def vector(observed, expected):
        assert len(observed) == len(expected), 'SDK vector length mismatch'
        for actual, target in zip(observed, expected):
            close(actual, target)

    def matrix(observed, expected):
        assert len(observed) == len(expected), 'SDK matrix row count mismatch'
        for actual_row, target_row in zip(observed, expected):
            vector(actual_row, target_row)

    if '07' in data:
        expected = data['07']
        rows = [row for row in recorded['hhl']['cases'] if row['name'] == 'signed-offgrid']
        by_bits = {row['phase_bits']: row for row in rows}
        assert len(rows) == 4 and set(by_bits) == {3, 4, 5, 6}, 'Missing or duplicate HHL signed-offgrid cases'
        for row in expected['rows']:
            archived = by_bits[row['phase_bits']]
            assert archived['dimension'] == 2, 'Unexpected HHL dimension'
            for field in ('C', 'cutoff', 'scale'):
                close(archived[field], expected[field])
            matrix(archived['A']['real'], expected['A'])
            matrix(archived['A']['imag'], [[0, 0], [0, 0]])
            vector(archived['b']['real'], expected['b']['real'])
            vector(archived['b']['imag'], expected['b']['imag'])
            vector(archived['eigenvalues'], expected['eigenvalues'])
            close(archived['flag_success'], row['flag_success'])
            close(archived['phase_zero_and_flag_success'], row['clean_success'])
        compared.append('hhl-signed-offgrid-3-4-5-6')

    if '16' in data:
        expected = data['16']
        rows = recorded['walk']['rows']
        by_step = {row['steps']: row for row in rows}
        assert len(rows) == len(by_step) and {4, 8} <= by_step.keys(), 'Missing or duplicate SDK walk steps'
        for step in (4, 8):
            close(by_step[step]['marked_probability'], expected[f'walk_step{step}'])
        qsvt = recorded['qsvt']
        vector(qsvt['polynomial_power_coefficients'], [0, -.3, 0, .8])
        matrix(qsvt['target']['real'], expected['P_A'])
        matrix(qsvt['target']['imag'], [[0, 0], [0, 0]])
        matrix(qsvt['unextracted_block']['real'], expected['P_A'])
        close(qsvt['extracted_success_probability'], expected['selected_probability'])
        compared.extend(['walk-4-and-8', 'qsvt-polynomial-and-success'])

    return compared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', nargs='?', default='all', choices=['all', *CASES])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--math-only', action='store_true', help='Skip SDK archive comparisons explicitly')
    mode.add_argument('--sdk-archive', type=pathlib.Path, default=ROOT/'sdk73/results-all.json',
                      help='Fixed archive to compare for chapters 07 and 16')
    args = parser.parse_args()
    data = {key: check() for key, check in CASES.items() if args.case in ('all', key)}
    if args.math_only or not {'07', '16'} & data.keys():
        compared = []
        status = 'skipped' if args.math_only else 'not_applicable'
    else:
        compared = compare_archive(data, args.sdk_archive)
        status = 'passed'
    print('round73 algorithms:', ', '.join(data), 'passed')
    print('SDK archive comparison:', status, ', '.join(compared))
    data['sdk_archive_comparison'] = {'status': status, 'comparisons': compared}
    suffix = 'math-only' if args.math_only else 'archive-comparison'
    name = f'algorithm-validation-{args.case}-{suffix}.json'
    write_result(REPOSITORY/'work/research'/name,
                 json.dumps(data, indent=2, ensure_ascii=False)+'\n')


if __name__=='__main__':main()
