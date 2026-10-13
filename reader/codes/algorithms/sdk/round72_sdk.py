#!/usr/bin/env python3
"""Actual installed SDK computations; no network/cloud, no vendor execution.
Run with isolated env's Python, ordinary mode (not -O). Seed 72013.
Each task independently compares a physical/mathematical answer, not import only.
"""
import contextlib, importlib.metadata as md, io, json, math, pathlib, sys, time
import numpy as np
if not __debug__: raise RuntimeError('Assertions must be enabled')
SEED=72013
ROOT=pathlib.Path(__file__).resolve().parent

def cirq_case():
    import cirq
    qs=cirq.LineQubit.range(4); p0,p1,b,a=qs
    had=np.array([[1,1],[1,-1]])/np.sqrt(2)
    A=had@np.diag([1.,2.])@had
    U=had@np.diag([1j,-1])@had
    qpe=cirq.Circuit(cirq.H(p0),cirq.H(p1),cirq.MatrixGate(U@U).on(b).controlled_by(p0),cirq.MatrixGate(U).on(b).controlled_by(p1),cirq.qft(p0,p1)**-1)
    c=qpe.copy()
    c.append(cirq.ry(math.pi).on(a).controlled_by(p0,p1,control_values=[0,1]))
    c.append(cirq.ry(math.pi/3).on(a).controlled_by(p0,p1,control_values=[1,0]))
    c+=cirq.inverse(qpe)
    sim=cirq.Simulator(dtype=np.complex128,seed=SEED)
    joint=sim.simulate(c,qubit_order=qs).final_state_vector.reshape(4,2,2)
    branch=joint[:,:,1]; ps=float(np.sum(abs(branch)**2))
    assert np.allclose(branch[1:],0,atol=1e-12)
    x=branch[0]/np.sqrt(ps); expected=np.array([3,1])/np.sqrt(10)
    assert np.allclose(x,expected,atol=1e-12) and abs(ps-5/8)<1e-12
    z_exact=float((abs(x[0])**2-abs(x[1])**2).real); x_exact=float((2*x[0].conjugate()*x[1]).real)
    assert abs(z_exact-.8)<1e-12 and abs(x_exact-.6)<1e-12
    assert np.allclose(A@x,(4/np.sqrt(10))*np.array([1.,0.]),atol=1e-12)
    samples=sim.run(c+cirq.Circuit(cirq.measure(a,key='ok'),cirq.measure(b,key='z')),repetitions=20000)
    mask=samples.measurements['ok'][:,0]==1; z=samples.measurements['z'][mask,0]
    assert abs(mask.mean()-ps)<.02 and abs((z==0).mean()-.9)<.02
    sx=sim.run(c+cirq.Circuit(cirq.H(b),cirq.measure(a,key='ok'),cirq.measure(b,key='x')),repetitions=20000)
    xm=sx.measurements['ok'][:,0]==1; xb=sx.measurements['x'][xm,0]
    assert abs((xb==0).mean()-.8)<.02
    # Independently execute DJ constant/balanced and BV s=101, actual reversible oracle.
    inp=cirq.LineQubit.range(3); target=cirq.LineQubit(3)
    outputs={}
    for label,s in [('dj_constant',()),('dj_balanced',(0,)),('bv_101',(0,2))]:
        qc=cirq.Circuit(cirq.X(target),cirq.H.on_each(*inp,target),[cirq.CNOT(inp[i],target) for i in s],cirq.H.on_each(*inp))
        v=sim.simulate(qc,qubit_order=[*inp,target]).final_state_vector.reshape(8,2)
        probs=np.sum(abs(v)**2,axis=1); want=sum(1<<(2-i) for i in s)
        assert np.allclose(probs,np.eye(8)[want],atol=1e-12)
        outputs[label]=format(want,'03b')
    # Simon f(x)=(x0 xor x1,x2,0), kernel {000,110}; six-qubit oracle.
    ins=cirq.LineQubit.range(3); outs=cirq.LineQubit.range(3,6)
    qc=cirq.Circuit(cirq.H.on_each(*ins),cirq.CNOT(ins[0],outs[0]),cirq.CNOT(ins[1],outs[0]),cirq.CNOT(ins[2],outs[1]),cirq.H.on_each(*ins))
    v=sim.simulate(qc,qubit_order=[*ins,*outs]).final_state_vector.reshape(8,8)
    probs=np.sum(abs(v)**2,axis=1); assert np.allclose(probs,[.25,.25,0,0,0,0,.25,.25],atol=1e-12)
    qc.append(cirq.measure(*ins,key='y')); hist=sim.run(qc,repetitions=64).histogram(key='y')
    nonzero=[int(k) for k in hist if k]; candidates=[s for s in range(1,8) if all(bin(s&y).count('1')%2==0 for y in nonzero)]
    assert candidates==[6]
    (ROOT/'hhl-circuit.txt').write_text(str(c)+'\n')
    return {'A':A.tolist(),'eigenvalues':[1,2],'input':[1,0],'success_exact':ps,'conditional_amplitudes':x.real.tolist(),'conditional_Z_exact':z_exact,'conditional_X_exact':x_exact,'conditional_x_counts':[int((xb==0).sum()),int((xb==1).sum())],'x_successes':int(xm.sum()),'shots':20000,'successes':int(mask.sum()),'conditional_z_counts':[int((z==0).sum()),int((z==1).sum())],'primitive_outputs':outputs,'simon_probabilities':probs.tolist(),'simon_histogram':{str(k):v for k,v in hist.items()},'simon_recovered':format(candidates[0],'03b'),'oracle_boundary':'explicit tiny circuit, not efficient arbitrary black-box synthesis'}

def pennylane_case():
    import pennylane as qml
    n=30000
    dev=qml.device('default.qubit',wires=2,seed=SEED)
    @qml.set_shots(shots=n)
    @qml.qnode(dev)
    def bell():
        qml.Hadamard(0); qml.CNOT([0,1])
        return qml.classical_shadow(wires=[0,1],seed=SEED)
    bits,recipes=bell(); np.savez_compressed(ROOT/'shadow-samples.npz',bits=bits,recipes=recipes,seed=np.array(SEED)); sh=qml.ClassicalShadow(bits,recipes)
    obs=[qml.X(0)@qml.X(1),qml.Y(0)@qml.Y(1),qml.Z(0)@qml.Z(1),qml.Z(0)]
    estimates=np.asarray(sh.expval(obs,k=1)); exact=np.array([1,-1,1,0])
    rows=[]
    for r,(axis,sign) in enumerate([(0,1),(1,-1),(2,1)]):
        match=(recipes==axis).all(axis=1); snapshot=9*match*(1-2*bits[:,0])*(1-2*bits[:,1])
        assert np.allclose(snapshot.mean(),estimates[r],atol=1e-12)
        rows.append({'axis':axis,'matching_snapshots':int(match.sum()),'positive':int((match & ((bits[:,0]^bits[:,1])==0)).sum()),'negative':int((match & ((bits[:,0]^bits[:,1])==1)).sum()),'empirical_variance':float(np.var(snapshot)),'exact_variance':8})
    assert np.max(abs(estimates-exact))<.12
    # End-to-end differentiable VQE with actual parameter-shift QNode.
    from pennylane import numpy as pnp
    h=qml.Hamiltonian([.7,.2],[qml.Z(0),qml.X(0)])
    @qml.qnode(qml.device('default.qubit',wires=1),diff_method='parameter-shift')
    def energy(theta):
        qml.RY(theta,wires=0); return qml.expval(h)
    theta=pnp.array(2.,requires_grad=True); opt=qml.GradientDescentOptimizer(.2)
    for _ in range(100): theta=opt.step(energy,theta)
    val=float(energy(theta)); assert abs(val+math.sqrt(.53))<1e-10
    return {'shots':n,'observables':['XX','YY','ZZ','ZI'],'estimates':estimates.tolist(),'analytic':[1,-1,1,0],'raw_pair_counts':rows,'seed':SEED,'vqe_steps':100,'vqe_energy':val,'vqe_theta':float(theta),'vqe_gradient':float(qml.grad(energy)(theta)),'statistical_check':'fixed-seed regression threshold only; not a universal confidence guarantee'}

def openfermion_case():
    import openfermion as of
    # Two spinless orbitals, one particle, energies in arbitrary common units.
    f=of.FermionOperator('0^ 0',1)+of.FermionOperator('1^ 1',2)+of.FermionOperator('0^ 1',-.5)+of.FermionOperator('1^ 0',-.5)
    jw=of.jordan_wigner(f); H=of.get_sparse_operator(jw,n_qubits=2).toarray()
    analytic=np.array([[0,0,0,0],[0,2,-.5,0],[0,-.5,1,0],[0,0,0,3]],complex)
    assert np.allclose(H,analytic)
    sub=H[np.ix_([1,2],[1,2])]; eig,vec=np.linalg.eigh(sub)
    expected=(3-math.sqrt(2))/2; assert abs(eig[0]-expected)<1e-12
    # Fermionic anticommutators are a separate mapping check.
    a0=of.get_sparse_operator(of.FermionOperator('0'),n_qubits=2).toarray()
    a1=of.get_sparse_operator(of.FermionOperator('1'),n_qubits=2).toarray()
    assert np.allclose(a0@a0.conj().T+a0.conj().T@a0,np.eye(4))
    assert np.allclose(a0@a1+a1@a0,0)
    return {'fermion_input':str(f),'jordan_wigner':str(jw),'basis':['00','01','10','11'],'one_particle_block':sub.real.tolist(),'one_particle_eigenvalues':eig.tolist(),'ground_energy':float(eig[0]),'particle_sector':'one particle, not unrestricted vacuum ground state','model_boundary':'two orbital hopping toy, not a molecular integral calculation'}

def qualtran_case():
    from qualtran.bloqs.cryptography.rsa import ModExp
    from qualtran.bloqs.basic_gates import Toffoli
    # RSA modular exponentiation bloq, full small-domain classical semantics.
    b=ModExp(base=2,mod=15,exp_bitsize=3,x_bitsize=4)
    rows=[]
    for k in range(8):
        out=b.call_classically(exponent=k)
        decomposed=b.decompose_bloq().call_classically(exponent=k)
        assert out==decomposed
        # Some releases return exponent register plus modular value.
        value=int(out[-1]); assert value==pow(2,k,15)
        rows.append({'exponent':k,'output':value})
    # Physical unitary semantics independently tested on all eight basis states.
    T=Toffoli().tensor_contract(); expected=np.eye(8); expected[[6,7]]=expected[[7,6]]
    assert np.allclose(T,expected) and np.allclose(T.conj().T@T,np.eye(8))
    counts=b.bloq_counts()
    return {'mod_exp_rows':rows,'toffoli_max_matrix_error':float(np.max(abs(T-expected))),'decomposition_counts':{str(k):str(v) for k,v in counts.items()},'boundary':'ModExp classical semantics and Toffoli tensor verified; not a simulated large modular exponentiation circuit or physical RSA attack'}

def pyqsp_case():
    from pyqsp.angle_sequence import QuantumSignalProcessingPhases
    from pyqsp.response import ComputeQSPResponse
    coefs=np.array([0.,.3,0.,.2]) # .3T1 + .2T3 = .8x^3-.3x
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): phases,reduced,parity=QuantumSignalProcessingPhases(coefs,method='sym_qsp',chebyshev_basis=True)
    grid=np.linspace(-1,1,1001); response=ComputeQSPResponse(grid,phases,signal_operator='Wx',sym_qsp=True)['pdat']
    target=.8*grid**3-.3*grid; error=float(np.max(abs(response.imag-target)))
    assert error<1e-10
    # Independent unitary reconstruction, not SDK response checking itself.
    errors=[]; unitary_errors=[]
    for x in grid:
        W=np.array([[x,1j*np.sqrt(max(0,1-x*x))],[1j*np.sqrt(max(0,1-x*x)),x]])
        U=np.diag(np.exp(1j*phases[0]*np.array([1,-1])))
        for phi in phases[1:]: U=U@W@np.diag(np.exp(1j*phi*np.array([1,-1])))
        errors.append(abs(U[0,0].imag-(.8*x**3-.3*x)))
        unitary_errors.append(np.max(abs(U.conj().T@U-np.eye(2))))
    assert max(errors)<1e-10 and max(unitary_errors)<1e-12
    (ROOT/'pyqsp-solver.log').write_text(buf.getvalue())
    return {'chebyshev_coefficients':coefs.tolist(),'phases_radians':phases.tolist(),'reduced_phases':reduced.tolist(),'parity':int(parity),'target':'0.8*x^3-0.3*x = 0.3*T1+0.2*T3','encoded_component':'imaginary U00; not whole U00','grid_points':1001,'SDK_grid_max_error':error,'independent_grid_max_error':float(max(errors)),'unitary_max_error':float(max(unitary_errors)),'continuous_boundary':'finite-grid numerical regression, not a certified uniform error theorem'}

def quimb_case():
    import quimb as qu
    # General finite graph input, weighted adjacency continuous-time walk.
    def evolve(n,edges,t,start):
        H=np.zeros((n,n))
        for i,j,w in edges: H[i,j]=H[j,i]=w
        v=np.eye(n)[:,start]; evo=qu.Evolution(qu.qu(v),qu.qu(H),method='solve'); evo.update_to(t)
        state=np.asarray(evo.pt).ravel()
        eig,V=np.linalg.eigh(H); reference=V@(np.exp(-1j*t*eig)*(V.conj().T@v))
        assert np.allclose(state,reference,atol=1e-12) and abs(np.vdot(state,state)-1)<1e-12
        return H,state
    t=math.pi/math.sqrt(2); H,v=evolve(3,[(0,1,1),(1,2,1)],t,0)
    assert np.allclose(abs(v)**2,[0,0,1],atol=1e-12)
    # Nonregular weighted five-node graph, checks conservation as independent invariants.
    H5,v5=evolve(5,[(0,1,1),(1,2,.7),(2,3,1.3),(3,4,.2),(0,4,.9),(1,4,.4)],.8,0)
    energy=float(np.vdot(v5,H5@v5).real); assert abs(energy)<1e-12
    return {'path3_time':t,'path3_probabilities':(abs(v)**2).tolist(),'weighted5_edges':[[0,1,1],[1,2,.7],[2,3,1.3],[3,4,.2],[0,4,.9],[1,4,.4]],'weighted5_time':.8,'weighted5_probabilities':(abs(v5)**2).tolist(),'weighted5_energy':energy,'boundary':'dense small graph CTQW, not coined/MNRS search or scalable classical simulation'}

def walrus_case():
    from thewalrus.quantum import is_valid_cov, is_pure_cov, probabilities
    r=math.log(2)/2; V=np.diag([math.exp(-2*r)/2,math.exp(2*r)/2]); mu=np.zeros(2)
    assert is_valid_cov(V,hbar=1) and is_pure_cov(V,hbar=1)
    invalid=np.array([[.5,.4],[.4,.5]]); assert not is_valid_cov(invalid,hbar=1)
    p=np.asarray(probabilities(mu,V,cutoff=20,hbar=1))
    analytic=np.array([math.comb(n,n//2)*(math.tanh(r)**n)/(2**n*math.cosh(r)) if n%2==0 else 0 for n in range(20)])
    assert np.allclose(p,analytic,atol=1e-12)
    # Passing default hbar=2 changes the physical meaning and rejects this covariance.
    assert not is_valid_cov(V)
    # Two-mode ordering test: SDK xxpp uses q1,q2,p1,p2.
    Vi=np.diag([.25,1.,.5,.5]); perm=[0,2,1,3]; Vg=Vi[np.ix_(perm,perm)]
    assert is_valid_cov(Vg,hbar=1) and is_pure_cov(Vg,hbar=1)
    return {'r':r,'hbar':1,'covariance':V.tolist(),'physical':True,'pure':True,'default_hbar2_rejects_same_numbers':True,'probabilities_0_to_19':p.tolist(),'retained_mass':float(p.sum()),'cutoff_tail':float(1-p.sum()),'mean_photons_truncated':float(np.arange(20)@p),'analytic_mean_photons':.125,'multi_mode_grouped_covariance':Vg.tolist(),'boundary':'Gaussian photon-number probabilities via SDK; truncation not automatically renormalized; not boson-sampling advantage'}

def dimod_case():
    import dimod
    b=dimod.BinaryQuadraticModel({'x1':-3.,'x2':-2.},{('x1','x2'):4.},0.,dimod.BINARY)
    ss=dimod.ExactSolver().sample(b); rows=[]
    for row in ss.data(['sample','energy']):
        x,y=int(row.sample['x1']),int(row.sample['x2']); expected=-3*x-2*y+4*x*y
        assert row.energy==expected
        rows.append({'sample':[x,y],'energy':float(row.energy),'feasible':x+y<=1})
    assert ss.first.sample=={'x1':1,'x2':0} and ss.first.energy==-3
    h,J,offset=b.to_ising()
    for row in rows:
        sample={k:2*v-1 for k,v in zip(['x1','x2'],row['sample'])}
        E=sum(h[k]*v for k,v in sample.items())+sum(J[pair]*sample[pair[0]]*sample[pair[1]] for pair in J)+offset
        assert abs(E-row['energy'])<1e-12
    # SDK spin s=2x-1; textbook Pauli eigenvalue z=1-2x=-s.
    return {'rows':rows,'ising_s_equals_2x_minus_1':{'h':h,'J':{str(k):v for k,v in J.items()},'offset':offset},'boundary':'classical exact enumeration; no QPU/annealing dynamics/TTS measured'}

CASES={'cirq':cirq_case,'pennylane':pennylane_case,'openfermion':openfermion_case,'qualtran':qualtran_case,'pyqsp':pyqsp_case,'quimb':quimb_case,'thewalrus':walrus_case,'dimod':dimod_case}
def main():
    chosen=sys.argv[1] if len(sys.argv)>1 else 'all'
    if chosen not in [*CASES,'all']: raise SystemExit('Choose all or '+', '.join(CASES))
    results={'python':sys.version,'seed':SEED,'evidence':'installed public release packages, ideal local CPU simulation; no cloud or vendor excerpts','cases':{}}
    for name,fn in CASES.items():
        if chosen!='all' and chosen!=name: continue
        wall=time.perf_counter(); cpu=time.process_time(); result=fn()
        results['cases'][name]={'version':md.version(name),'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,'result':result,'status':'passed'}
        print(name+' passed',flush=True)
    path=ROOT/('round72-results.json' if chosen=='all' else 'round72-'+chosen+'-results.json'); path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(str(path))
if __name__=='__main__': main()
