#!/usr/bin/env python3
"""Round 73 real SDK tasks, separate from immutable round 72 evidence.
Tiny dense oracles are teaching implementations, not sparse/query cost proofs.
"""
import argparse, importlib.metadata as md, json, math, pathlib, platform, sys, time
import numpy as np
import scipy.linalg as la
if not __debug__: raise RuntimeError('Run without -O')
ROOT=pathlib.Path(__file__).resolve().parent
SEED=73007

def encoded(a):
    a=np.asarray(a)
    return {'real':a.real.tolist(),'imag':a.imag.tolist()}

def prepare(b):
    """Unitary completion with first column b, not answer-state preparation."""
    b=np.asarray(b,complex); assert abs(np.linalg.norm(b)-1)<1e-12
    basis=[b]
    for e in np.eye(len(b),dtype=complex):
        v=e.copy()
        for u in basis: v-=u*np.vdot(u,v)
        if np.linalg.norm(v)>1e-10: basis.append(v/np.linalg.norm(v))
    p=np.column_stack(basis)
    assert np.allclose(p.conj().T@p,np.eye(len(b)),atol=1e-12)
    return p

def hhl(a,b,t,scale=4.,cutoff=.5,constant=.5, name='case',shots=0):
    import cirq
    a=np.asarray(a,complex); b=np.asarray(b,complex)
    if not isinstance(t,(int,np.integer)) or isinstance(t,(bool,np.bool_)) or t<1: raise ValueError('Positive integer phase register size required')
    if b.ndim!=1 or len(b)<2: raise ValueError('One-dimensional input vector of dimension at least two required')
    d=len(b); n=int(round(math.log2(d))); m=2**t
    if d!=2**n or a.shape!=(d,d): raise ValueError('Power-of-two dimension required')
    if not np.allclose(a,a.conj().T): raise ValueError('Hermitian input required')
    if abs(np.linalg.norm(b)-1)>1e-12: raise ValueError('Normalized input required')
    if not 0<constant<=cutoff<scale: raise ValueError('Require 0<C<=cutoff<scale')
    eig,v=np.linalg.eigh(a)
    if np.min(abs(eig))<cutoff or max(abs(eig))>=scale: raise ValueError('Spectrum outside promised band')
    qs=cirq.LineQubit.range(t+n+1); phase=qs[:t]; system=qs[t:t+n]; flag=qs[-1]
    qpe=cirq.Circuit(cirq.H.on_each(*phase))
    for k,q in enumerate(phase):
        power=2**(t-1-k)
        u=la.expm(2j*math.pi*a*power/(2*scale))
        qpe.append(cirq.MatrixGate(u).on(*system).controlled_by(q))
    qpe.append(cirq.qft(*phase,without_reverse=False)**-1)
    signed=np.where(np.arange(m)<m/2,np.arange(m),np.arange(m)-m)*2*scale/m
    r=np.zeros(m); mask=abs(signed)>=cutoff; r[mask]=constant/signed[mask]
    circuit=cirq.Circuit(cirq.MatrixGate(prepare(b)).on(*system))+qpe
    for y in range(m):
        if r[y]:
            bits=[int(c) for c in format(y,f'0{t}b')]
            circuit.append(cirq.ry(2*math.asin(float(r[y]))).on(flag).controlled_by(*phase,control_values=bits))
    circuit+=cirq.inverse(qpe)
    sim=cirq.Simulator(dtype=np.complex128,seed=SEED+t)
    joint=sim.simulate(circuit,qubit_order=qs).final_state_vector.reshape(m,d,2)
    branch=joint[:,:,1]; p=float(np.vdot(branch,branch).real)
    pclean=float(np.vdot(branch[0],branch[0]).real)
    target=np.linalg.solve(a,b); ptarget=float(constant**2*np.vdot(target,target).real); target/=np.linalg.norm(target)
    # Independent spectral Fourier construction, NOT SDK circuit matrix reuse.
    grid=np.arange(m); f=np.exp(2j*math.pi*np.outer(grid,grid)/m)/np.sqrt(m)
    h=np.array([[1,1],[1,-1]])/np.sqrt(2)
    ht=h
    for _ in range(t-1): ht=np.kron(ht,h)
    beta=v.conj().T@b; ref=np.zeros((m,d),complex); fj=[]; tj=[]
    for j,e in enumerate(eig):
        q=f.conj().T@np.diag(np.exp(2j*math.pi*grid*e/(2*scale)))@ht
        q0=q[:,0]; g=q.conj().T@(r*q0)
        ref+=beta[j]*np.outer(g,v[:,j]); fj.append(float(np.sum(abs(q0)**2*r)))
        tj.append(float(np.sum(abs(q0)**2*r*r)))
    mismatch=float(np.max(abs(ref-branch))); assert mismatch<2e-12
    assert abs(p-sum(abs(beta)**2*np.array(tj)))<2e-12
    assert abs(pclean-sum(abs(beta)**2*np.array(fj)**2))<2e-12
    # A conditional branch can vanish even for an allowed spectrum. Comparing
    # amplitudes before normalization avoids assigning a state to roundoff.
    resolution = max(64 * float(np.finfo(float).eps), float(np.linalg.norm(ref - branch)))
    flag_resolved = math.sqrt(p) > resolution
    clean_resolved = math.sqrt(pclean) > resolution
    rho = branch.T @ branch.conj() / p if flag_resolved else None
    xclean = branch[0] / math.sqrt(pclean) if clean_resolved else None
    root_f = math.sqrt(max(0., float(np.vdot(target, rho @ target).real))) if flag_resolved else None
    clean_f = float(abs(np.vdot(target, xclean))) if clean_resolved else None
    residual = float(np.linalg.norm(a @ xclean - b * np.vdot(b, a @ xclean))) if clean_resolved else None
    np.savez_compressed(ROOT/f'hhl-{name}-t{t}.npz',A=a,b=b,joint=joint,phase_labels=signed,rotation_amplitudes=r,ideal_target=target,seed=SEED+t)
    (ROOT/f'hhl-{name}-t{t}-circuit.txt').write_text(str(circuit)+'\n')
    rec={'name':name,'phase_bits':t,'dimension':d,'basis_order':'phase (MSB first), system (MSB first), flag','scale':scale,'cutoff':cutoff,'C':constant,'A':encoded(a),'b':encoded(b),'eigenvalues':eig.tolist(),'ideal_success':ptarget,'flag_success':p,'phase_zero_and_flag_success':pclean,'garbage_probability':max(0.,p-pclean),'garbage_given_flag':max(0.,1-pclean/p) if flag_resolved else None,'mixed_root_fidelity':root_f,'mixed_squared_fidelity':root_f**2 if flag_resolved else None,'mixed_purity':float(np.trace(rho@rho).real) if flag_resolved else None,'clean_root_fidelity':clean_f,'clean_direction_residual':residual,'rho_given_flag':encoded(rho) if flag_resolved else None,'clean_amplitudes':encoded(xclean) if clean_resolved else None,'flag_state_resolved':flag_resolved,'clean_state_resolved':clean_resolved,'amplitude_resolution':resolution,'filter_mean_per_eigenvalue':fj,'filter_second_moment_per_eigenvalue':tj,'independent_max_amplitude_error':mismatch,'logical_operations':len(list(circuit.all_operations())),'qpe_base_controlled_U_calls_if_repeated':m-1,'forward_and_inverse_base_U_calls_if_repeated':2*(m-1)}
    if shots:
        measurement=circuit+cirq.Circuit(cirq.measure(*phase,key='phase'),cirq.measure(flag,key='flag'),cirq.measure(*system,key='system'))
        data=sim.run(measurement,repetitions=shots)
        ok=data.measurements['flag'][:,0]==1; clean=ok & (data.measurements['phase']==0).all(axis=1)
        np.savez_compressed(ROOT/f'hhl-{name}-t{t}-samples.npz',phase=data.measurements['phase'],flag=data.measurements['flag'],system=data.measurements['system'],seed=SEED+t)
        rec.update(shots=shots,flag_count=int(ok.sum()),clean_count=int(clean.sum()),garbage_count=int((ok & ~clean).sum()))
        assert abs(ok.mean()-p)<.025 and abs(clean.mean()-pclean)<.025
    return rec

def hhl_case():
    angle=math.pi/5; v=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
    exact=v@np.diag([-1.,2.])@v.T
    offgrid=v@np.diag([-1.1,2.3])@v.T
    b=np.array([math.sqrt(.6),1j*math.sqrt(.4)])
    rows=[hhl(exact,b,3,name='signed-grid',shots=20000)]
    assert rows[0]['garbage_probability']<1e-12 and abs(rows[0]['mixed_root_fidelity']-1)<1e-12
    for t in [3,4,5,6]: rows.append(hhl(offgrid,b,t,name='signed-offgrid',shots=20000 if t==4 else 0))
    h=np.array([[1,1],[1,-1]])/np.sqrt(2); v4=np.kron(h,v)
    a4=v4@np.diag([-1.3,-.7,1.1,2.2])@v4.T
    rows.append(hhl(a4,np.array([1,1j,-1,1])/2,5,name='four-dimension'))
    assert rows[4]['mixed_root_fidelity']>.99 and rows[4]['garbage_given_flag']<rows[1]['garbage_given_flag']
    vanishing = hhl(3.1167157787684143 * np.eye(2), np.array([1., 0.]),
                    2, cutoff=2., name='vanishing-clean-branch')
    assert abs(vanishing['flag_success'] - .0337221092) < 1e-10
    assert vanishing['flag_state_resolved'] and not vanishing['clean_state_resolved']
    assert vanishing['clean_amplitudes'] is None and vanishing['clean_direction_residual'] is None
    # Reject singular/unsupported inputs rather than silently invert zero.
    rejected=[]
    for bad,label in [(np.diag([0.,1.]),'singular'),(np.array([[1.,1.],[0.,1.]]),'non-Hermitian'),(np.diag([-4.,1.]),'phase-alias-boundary')]:
        try: hhl(bad,np.array([1.,0.]),3,name='invalid')
        except ValueError: rejected.append(label)
        else: raise AssertionError('Invalid input accepted')
    for bad_t in [0,-1,1.5,True]:
        try: hhl(exact,b,bad_t)
        except ValueError: rejected.append('invalid-phase-size-'+str(bad_t))
        else: raise AssertionError('Invalid phase register accepted')
    return {'cirq':md.version('cirq-core'),'cases':rows,'vanishing_clean_branch':vanishing,'rejected':rejected,'scope':'Finite small Hermitian power-of-two dense matrix teaching interface, hard reciprocal cutoff; not full HHL filter/error theorem or sparse efficient implementation'}

def walk_case():
    import cirq
    # SKW coined search on the four-dimensional hypercube. Coin is 4 directions.
    n=4; nc=2; N=2**n; dim=n*N; target=0
    coin=cirq.LineQubit.range(nc); pos=cirq.LineQubit.range(nc,nc+n); qs=[*coin,*pos]
    sc=np.ones(n)/np.sqrt(n); g=2*np.outer(sc,sc)-np.eye(n)
    step=cirq.Circuit(cirq.MatrixGate(g).on(*coin))
    step.append(cirq.MatrixGate(-g).on(*coin).controlled_by(*pos,control_values=[0]*n))
    for j in range(n):
        step.append(cirq.X(pos[j]).controlled_by(*coin,control_values=[int(x) for x in format(j,'02b')]))
    cp=np.kron(g,np.eye(N)); cp[np.ix_(np.arange(n)*N+target,np.arange(n)*N+target)]=-np.eye(n)
    shift=np.zeros((dim,dim))
    for j in range(n):
        for x in range(N): shift[j*N+(x^(1<<(n-1-j))),j*N+x]=1
    w=shift@cp; assert np.allclose(w.conj().T@w,np.eye(dim))
    ev,vec=np.linalg.eig(w); assert np.allclose(w@vec,vec*ev,atol=1e-12)
    # Independent iterative dense multiplication compared with SDK states each prefix.
    ref=np.ones(dim)/np.sqrt(dim); c=cirq.Circuit(cirq.H.on_each(*qs)); sim=cirq.Simulator(dtype=np.complex128,seed=SEED)
    rows=[]; allstates=[]
    transition=np.zeros((N,N))
    for x in range(N):
        for j in range(n): transition[x^(1<<j),x]+=1/n
    classical=np.ones(N)/N; absorbing=transition.copy(); absorbing[:,target]=0; absorbing[target,target]=1
    for k in range(17):
        got=sim.simulate(c,qubit_order=qs).final_state_vector
        mismatch=float(np.max(abs(got-ref))); assert mismatch<1e-12
        probs=np.sum(abs(got.reshape(n,N))**2,axis=0); allstates.append(got)
        rows.append({'steps':k,'marked_probability':float(probs[target]),'position_probabilities':probs.tolist(),'classical_uniform_marginal':1/N,'classical_first_hit_by_step':float(classical[target]),'independent_amplitude_error':mismatch})
        c+=step; ref=w@ref; classical=absorbing@classical
    peak=max(range(9),key=lambda k:rows[k]['marked_probability']); assert peak==4
    selected=cirq.Circuit(cirq.H.on_each(*qs))
    for _ in range(peak): selected+=step
    data=sim.run(selected+cirq.Circuit(cirq.measure(*pos,key='position')),repetitions=20000)
    ints=data.measurements['position']@np.array([8,4,2,1]); hist=np.bincount(ints,minlength=N)
    assert abs(hist[target]/20000-rows[peak]['marked_probability'])<.02
    unmarked=cirq.Circuit(cirq.H.on_each(*qs))
    for _ in range(4):
        unmarked+=cirq.Circuit(cirq.MatrixGate(g).on(*coin))
        for j in range(n): unmarked.append(cirq.X(pos[j]).controlled_by(*coin,control_values=[int(x) for x in format(j,'02b')]))
    un=sim.simulate(unmarked,qubit_order=qs).final_state_vector
    assert np.allclose(abs(un)**2,1/dim)
    np.savez_compressed(ROOT/'walk-states-samples.npz',states=np.asarray(allstates),samples=data.measurements['position'],seed=SEED,shift=shift,coin=g,marked_step=w)
    (ROOT/'walk-circuit.txt').write_text(str(selected)+'\n')
    return {'cirq':md.version('cirq-core'),'N':N,'hypercube_dimension':n,'marked_vertex':target,'basis_order':'coin label (MSB first), position x (MSB first)','rows':rows,'selected_steps':peak,'selection_rule':'precomputed earliest maximum within 0..8, before sampling; no measured-count selection','shots':20000,'histogram':hist.tolist(),'marked_count':int(hist[target]),'boundary':'SKW coined hypercube search, not CTQW or full MNRS; dense coin toy, exact simulations and one finite-shot regression, not scalable advantage evidence'}

def qsvt_case():
    import pennylane as qml
    # Actual matrix block encoding plus a synthesized odd polynomial circuit.
    a=np.array([[.2,.3],[.3,-.4]])
    poly=[0.,-.3,0.,.8]
    op=qml.qsvt(a,poly,encoding_wires=[0,1])
    u=qml.matrix(op,wire_order=[0,1])
    @qml.qnode(qml.device('default.qubit',wires=2))
    def signal_circuit():
        qml.qsvt(a,poly,encoding_wires=[0,1])
        return qml.state()
    signal_state=np.asarray(signal_circuit())
    assert np.allclose(signal_state,u[:,0],atol=1e-10)
    want=.8*np.linalg.matrix_power(a,3)-.3*a
    block=u[:2,:2]
    # Official QSVT API stores the real polynomial in the real block.
    assert np.allclose(block.real,want,atol=2e-9)
    assert np.allclose(u.conj().T@u,np.eye(4),atol=1e-10)
    # Remove the imaginary companion coherently with a selector ancilla:
    # (U + U*)/2 is a block of H controlled(U,U*) H, not a nonunitary replacement.
    sel=np.zeros((8,8),complex); sel[:4,:4]=u; sel[4:,4:]=u.conj()
    hs=np.kron(np.array([[1,1],[1,-1]])/np.sqrt(2),np.eye(4))
    combined=hs@sel@hs; assert np.allclose(combined[:2,:2],want,atol=2e-9)
    dev=qml.device('default.qubit',wires=3)
    @qml.qnode(dev)
    def run():
        qml.Hadamard(0)
        qml.ctrl(qml.QubitUnitary(u,wires=[1,2]),control=0,control_values=[0])
        qml.ctrl(qml.QubitUnitary(u.conj(),wires=[1,2]),control=0,control_values=[1])
        qml.Hadamard(0)
        return qml.state()
    state=np.asarray(run()); assert np.allclose(state,combined[:,0],atol=1e-10)
    p=float(np.vdot(state[:2],state[:2]).real); x=state[:2]/np.sqrt(p)
    assert np.allclose(x,want[:,0]/np.linalg.norm(want[:,0]),atol=1e-8)
    np.savez_compressed(ROOT/'qsvt-matrices.npz',A=a,U=u,target=want,selector_unitary=combined,actual_state=state)
    return {'pennylane':md.version('pennylane'),'eigenvalues':np.linalg.eigvalsh(a).tolist(),'polynomial_power_coefficients':poly,'target':encoded(want),'unextracted_block':encoded(block),'full_matrix_unitarity_error':float(np.max(abs(u.conj().T@u-np.eye(4)))),'real_block_error':float(np.max(abs(block.real-want))),'extracted_success_probability':p,'extracted_state':encoded(x),'qsvt_operation':str(op),'qsvt_angles':qml.poly_to_angles(poly,'QSVT').tolist(),'signal_state':encoded(signal_state),'boundary':'Actual QSVT signal synthesis and real-part selector circuit for real Hermitian 2x2; selector uses tiny dense compiled matrices, not general efficient conjugation or fault-tolerant gate synthesis'}

def mbqc_case():
    import cirq
    q0,q1,q2=cirq.LineQubit.range(3)
    alpha=math.pi/4; beta=math.pi/3; b=np.array([1/math.sqrt(3),1j*math.sqrt(2/3)])
    h=np.array([[1,1],[1,-1]])/np.sqrt(2)
    def j(angle): return h@np.diag([np.exp(1j*angle/2),np.exp(-1j*angle/2)])
    target=j(beta)@j(alpha)@b
    c=cirq.Circuit(cirq.MatrixGate(prepare(b)).on(q0),cirq.H(q1),cirq.H(q2),cirq.CZ(q0,q1),cirq.CZ(q1,q2),cirq.rz(-alpha).on(q0),cirq.H(q0),cirq.measure(q0,key='m0'))
    c.append(cirq.rz(-beta).on(q1))
    c.append(cirq.rz(2*beta).on(q1).with_classical_controls('m0'))
    c.append([cirq.H(q1),cirq.measure(q1,key='m1'),cirq.X(q2).with_classical_controls('m1'),cirq.Z(q2).with_classical_controls('m0')])
    c.append(cirq.MatrixGate(prepare(target).conj().T).on(q2))
    c.append(cirq.measure(q2,key='verification'))
    data=cirq.Simulator(dtype=np.complex128,seed=SEED+17).run(c,repetitions=20000)
    assert not data.measurements['verification'].any()
    outcomes=2*data.measurements['m0'][:,0]+data.measurements['m1'][:,0]
    hist=np.bincount(outcomes,minlength=4); assert np.max(abs(hist/20000-.25))<.02
    np.savez_compressed(ROOT/'mbqc-samples.npz',m0=data.measurements['m0'],m1=data.measurements['m1'],verification=data.measurements['verification'],seed=SEED+17)
    (ROOT/'mbqc-circuit.txt').write_text(str(c)+'\n')
    return {'cirq':md.version('cirq-core'),'alpha':alpha,'beta':beta,'input':encoded(b),'target':encoded(target),'shots':20000,'branch_counts':hist.tolist(),'verification_failures':int(data.measurements['verification'].sum()),'boundary':'Real conditional midcircuit classical feedback in local ideal simulator; verifier has known target inverse, not blind delegated universal verification or physical feedforward latency measurement'}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('case',nargs='?',choices=['all','hhl','walk','qsvt','mbqc'],default='all'); args=parser.parse_args()
    records={}; failed=False
    for name,fn in [('hhl',hhl_case),('walk',walk_case),('qsvt',qsvt_case),('mbqc',mbqc_case)]:
        if args.case not in ['all',name]: continue
        start=time.time()
        try: data=fn(); records[name]={'status':'passed','elapsed_seconds':time.time()-start,**data}
        except Exception as ex:
            import traceback; traceback.print_exc(); records[name]={'status':'failed','error':repr(ex),'elapsed_seconds':time.time()-start}; failed=True
        print(name,records[name]['status'],flush=True)
    doc={'python':sys.version,'platform':platform.platform(),'seed':SEED,'cases':records}
    (ROOT/f'results-{args.case}.json').write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
    return int(failed)
if __name__=='__main__': raise SystemExit(main())
