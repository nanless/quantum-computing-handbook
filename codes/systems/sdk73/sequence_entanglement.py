"""Full Barrett--Kok heralding followed by real SDK swapping and expiry, no manual Bell pairs."""
import json, importlib.metadata, platform
from pathlib import Path
import numpy as np
import sequence.components.bsm as bsm_module
from sequence.kernel.timeline import Timeline
from sequence.kernel.event import Event
from sequence.kernel.process import Process
from sequence.topology.node import Node, BSMNode
from sequence.components.memory import Memory
from sequence.components.optical_channel import QuantumChannel, ClassicalChannel
from sequence.entanglement_management.generation import EntanglementGenerationA
from sequence.entanglement_management.swapping import EntanglementSwappingA, EntanglementSwappingB
if not __debug__: raise RuntimeError('Validation requires assertions; do not run with -O')
OUT=Path(__file__).resolve().parent

class Manager:
    def __init__(self,owner): self.owner=owner; self.rows=[]
    def update(self,protocol,memory,state):
        self.rows.append(dict(t_ps=int(self.owner.timeline.now()),node=self.owner.name,memory=memory.name,state=state,
            protocol=type(protocol).__name__,bsm_res=getattr(protocol,'bsm_res',None),fidelity=float(memory.fidelity),remote=dict(memory.entangled_memory)))
        if state=='RAW': memory.reset()

class Router(Node):
    def __init__(self,name,tl,count,seed,coherence,fidelity):
        super().__init__(name,tl,seed=seed); self.resource_manager=Manager(self); self.received=[]; self.expirations=[]
        self.mem=[]
        for i in range(count):
            m=Memory(f'{name}.m{i}',tl,fidelity,1e6,1,coherence,500)
            m.owner=self; m.add_receiver(self); m.attach(self); self.add_component(m); self.mem.append(m)
    def init(self):
        for m in self.mem: m.reset()
    def get(self,photon,**kwargs): self.send_qubit(kwargs['dst'],photon)
    def receive_message(self,src,msg):
        self.received.append(dict(t_ps=int(self.timeline.now()),src=src,receiver=msg.receiver,type=str(msg.msg_type),meas_res=getattr(msg,'meas_res',None)))
        for p in list(self.protocols):
            if p.name==msg.receiver or (msg.receiver is None and getattr(p,'middle',None)==src):
                p.received_message(src,msg); return
        raise RuntimeError('Unrouted protocol message '+str(msg.receiver))
    def memory_expire(self,m):
        self.expirations.append(dict(t_ps=int(self.timeline.now()),memory=m.name))
        for p in list(self.protocols):
            if m in p.memories: p.memory_expire(m)

class Coordinator:
    def __init__(self,tl,nodes): self.tl=tl; self.nodes=nodes; self.swap_started=None
    def swap_if_ready(self):
        a,b,c=self.nodes
        if not all(m.fidelity>0 for m in (a.mem[0],b.mem[0],b.mem[1],c.mem[0])): return
        pa=EntanglementSwappingB(a,'swap-a',a.mem[0]); pc=EntanglementSwappingB(c,'swap-c',c.mem[0])
        pb=EntanglementSwappingA(b,'swap-b',b.mem[0],b.mem[1],success_prob=1,degradation=1)
        pa.set_others(pb.name,b.name,[m.name for m in b.mem]); pc.set_others(pb.name,b.name,[m.name for m in b.mem])
        pb.set_others(pa.name,a.name,[a.mem[0].name]); pb.set_others(pc.name,c.name,[c.mem[0].name])
        a.protocols=[pa]; b.protocols=[pb]; c.protocols=[pc]
        self.swap_started=int(self.tl.now()); pa.start(); pc.start(); pb.start()

def trial(seed,attenuation=0,coherence=-1,fidelity=1,require_target=True):
    tl=Timeline(stop_time=1000000000,formalism='density_matrix')
    a=Router('A',tl,1,seed,coherence,fidelity); b=Router('B',tl,2,seed+1,coherence,fidelity); c=Router('C',tl,1,seed+2,coherence,fidelity)
    left=BSMNode('L',tl,['A','B'],seed=seed+3); right=BSMNode('R',tl,['B','C'],seed=seed+4)
    for n in (left,right):
        detector=n.get_components_by_type('SingleAtomBSM')[0]
        detector.update_detectors_params('efficiency',1)
        detector.update_detectors_params('dark_count',0)
    for n,dst in ((a,left),(b,left),(b,right),(c,right)):
        qc=QuantumChannel('q'+n.name+dst.name,tl,attenuation=attenuation,distance=1000,frequency=1e6); qc.set_ends(n,dst.name)
    nodes=[a,b,c,left,right]
    for src in nodes:
        for dst in nodes:
            if src!=dst:
                cc=ClassicalChannel('cc'+src.name+dst.name,tl,distance=1000,delay=5000000); cc.set_ends(src,dst.name)
    for src,sm,mid,dst,dm in ((a,a.mem[0],left,b,b.mem[0]),(b,b.mem[1],right,c,c.mem[0])):
        ps=EntanglementGenerationA.create(src,'eg'+sm.name,mid.name,dst.name,sm)
        pd=EntanglementGenerationA.create(dst,'eg'+dm.name,mid.name,src.name,dm)
        src.protocols.append(ps); dst.protocols.append(pd)
        ps.set_others(pd.name,dst.name,[dm.name]); pd.set_others(ps.name,src.name,[sm.name])
    tl.init()
    for n in (a,b,c):
        for p in n.protocols: p.start()
    coordinator=Coordinator(tl,[a,b,c])
    # Fixed control gate at 200 us: generation is never silently replaced by manual input pairs.
    tl.schedule(Event(200000000,Process(coordinator,'swap_if_ready',[])))
    tl.stop_time=250000000; tl.run()
    rows=[r for n in (a,b,c) for r in n.resource_manager.rows]
    success=(a.mem[0].entangled_memory['node_id']=='C' and c.mem[0].entangled_memory['node_id']=='A')
    true_overlap=None; rho=None; keys=None
    if success:
        qa,qc=a.mem[0].qstate_key,c.mem[0].qstate_key
        state=tl.quantum_manager.get(qa); keys=state.keys
        assert qa in keys and qc in keys
        # SDK density representation retains measured middle keys. Trace them out explicitly.
        tensor=np.asarray(state.state).reshape((2,)*(2*len(keys)))
        remaining=len(keys)
        for ix in sorted((j for j,k in enumerate(keys) if k not in (qa,qc)),reverse=True):
            tensor=np.trace(tensor,axis1=ix,axis2=ix+remaining); remaining-=1
        rho=tensor.reshape(4,4); phi=np.array([1,0,0,1])/np.sqrt(2)
        true_overlap=float(np.real(phi@rho@phi)); assert abs(np.trace(rho)-1)<1e-10
        assert np.linalg.eigvalsh(rho).min()>-1e-10
        if fidelity==1 and require_target: assert abs(true_overlap-1)<1e-10
    before_expiry=dict(A=dict(a.mem[0].entangled_memory),C=dict(c.mem[0].entangled_memory))
    tl.stop_time=1000000000; tl.run()
    return dict(seed=seed,attenuation_db_per_m=attenuation,coherence_s=coherence,raw_fidelity=fidelity,
        generated_end_updates=sum(r['state']=='ENTANGLED' and r['protocol']=='BarretKokA' for r in rows),
        swapped=success,swap_start_ps=coordinator.swap_started,true_bell_overlap=true_overlap,
        metadata_fidelity=float(next((r['fidelity'] for r in rows if r['protocol']=='EntanglementSwappingB' and r['state']=='ENTANGLED'),0)),
        memory_before_expiry=before_expiry,memory_after_window=dict(A=dict(a.mem[0].entangled_memory),C=dict(c.mem[0].entangled_memory)),
        updates=rows,messages=[r for n in (a,b,c) for r in n.received],expirations=[r for n in (a,b,c) for r in n.expirations],
        matrix=None if rho is None else [[[float(z.real),float(z.imag)] for z in row] for row in rho],state_keys=keys,executed_events=tl.run_counter)

if __name__=='__main__':
    # Retain actual unguarded counterexample before changing this process-local adapter.
    before=trial(730190,require_target=False)
    assert before['swapped'] and before['metadata_fidelity']==1 and before['true_bell_overlap']<1e-10
    (OUT/'sequence-unguarded-counterexample.json').write_text(json.dumps(before,indent=2)+'\n')
    original=bsm_module._eq_psi_plus
    def density_guard(state,formalism):
        if formalism=='density_matrix':
            psi=np.array([0,1,1,0])/np.sqrt(2)
            return bool(np.allclose(state.state,np.outer(psi,psi.conj()),atol=1e-12,rtol=0))
        return original(state,formalism)
    bsm_module._eq_psi_plus=density_guard
    ideal=[trial(730120+10*i) for i in range(400)]
    lossy=[trial(740120+10*i,attenuation=.0002) for i in range(400)]
    finite=[trial(750120+10*i,coherence=.0005) for i in range(40)]
    short=[trial(760120+10*i,coherence=.00001) for i in range(40)]
    mixed=[trial(770120+10*i,fidelity=.9) for i in range(40)]
    assert any(r['swapped'] for r in ideal) and any(r['swapped'] for r in finite)
    assert all(not r['swapped'] for r in short)
    for r in finite:
        if r['swapped']: assert r['memory_after_window']['A']['node_id'] is None and r['memory_after_window']['C']['node_id'] is None
    for r in mixed:
        if r['swapped']:
            assert abs(r['true_bell_overlap']-(.9**2+.1**2/3))<1e-10
            assert abs(r['metadata_fidelity']-.9**2)<1e-10
    result=dict(date='2026-10-13',status='passed',python=platform.python_version(),version=importlib.metadata.version('sequence'),
       scope='fresh density-matrix timelines; two genuine BK links; no retries; fixed 200us ideal-success swapping; expiry is hard cutoff, not continuous T2',
       groups={'ideal':ideal,'lossy':lossy,'finite_cutoff':finite,'short_cutoff':short,'mixed_input':mixed})
    result['counts']={k:dict(trials=len(v),swapped=sum(r['swapped'] for r in v),generated_links=sum(r['generated_end_updates'] for r in v)//2) for k,v in result['groups'].items()}
    (OUT/'sequence-entanglement-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['counts'],indent=2))
