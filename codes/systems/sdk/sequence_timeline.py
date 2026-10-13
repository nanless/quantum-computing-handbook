"""SeQUeNCe 0.8.5 network events: real channel classes + explicit application ack.
No custom substitute simulator: Timeline/Process/Event schedule all transmissions.
"""
import importlib.metadata,json,platform
from pathlib import Path
import numpy as np
from sequence.kernel.timeline import Timeline
from sequence.kernel.event import Event
from sequence.kernel.process import Process
from sequence.topology.node import Node
from sequence.components.optical_channel import QuantumChannel,ClassicalChannel
from sequence.components.photon import Photon
if not __debug__: raise RuntimeError('Run without -O')
OUT=Path(__file__).resolve().parent
class Endpoint(Node):
    def __init__(self,name,timeline,seed):
        super().__init__(name,timeline,seed=seed);self.arrivals=[];self.acks=[];self.emitted=[]
    def emit(self,seq):
        photon=Photon(str(seq),self.timeline,wavelength=1550,location=self,quantum_state=(1+0j,0+0j))
        self.emitted.append((seq,int(self.timeline.now())))
        self.send_qubit('B',photon)
    def receive_qubit(self,src,qubit):
        self.arrivals.append((int(qubit.name),int(self.timeline.now())))
        assert np.allclose(qubit.quantum_state.state,(1,0))
        # An application ack, not a Bell-pair herald and not a QKD protocol.
        self.send_message(src,dict(seq=int(qubit.name),received=int(self.timeline.now())))
    def receive_message(self,src,msg):
        self.acks.append((msg['seq'],int(self.timeline.now())))

if __name__=='__main__':
    tl=Timeline(stop_time=2_000_000_000)
    a=Endpoint('A',tl,72012);b=Endpoint('B',tl,72013)
    qc=QuantumChannel('A-to-B',tl,attenuation=0.0002,distance=10_000,frequency=1e7)
    qc.set_ends(a,'B')
    cc=ClassicalChannel('B-to-A',tl,distance=10_000)
    cc.set_ends(b,'A')
    tl.init()
    count=1000; starts={}
    for seq in range(count):
        start=qc.schedule_transmit(seq*100_000)
        starts[seq]=start
        tl.schedule(Event(start,Process(a,'emit',[seq])))
    tl.run()
    expected_eta=10**(-0.0002*10_000/10)
    assert count==len(a.emitted) and 0<len(b.arrivals)<count
    assert len(a.acks)==len(b.arrivals)
    for seq,time in b.arrivals: assert time-starts[seq]==qc.delay
    for seq,time in a.acks: assert time-starts[seq]==qc.delay+cc.delay
    measured=len(b.arrivals)/count
    se=(expected_eta*(1-expected_eta)/count)**.5
    assert abs(measured-expected_eta)<6*se
    data=dict(access_date='2026-10-13',python=platform.python_version(),sequence_version=importlib.metadata.version('sequence'),
        requires_python=importlib.metadata.metadata('sequence').get('Requires-Python'),
        seed_sender=72012,seed_receiver=72013,unit='picosecond',distance_m=10000,attenuation_dB_per_m=0.0002,
        transmitted=count,received=len(b.arrivals),acks=len(a.acks),eta_expected=expected_eta,eta_observed=measured,
        quantum_delay_ps=int(qc.delay),classical_default_delay_ps=int(cc.delay),
        last_emission_ps=max(starts.values()),ack_delay_from_emission_ps=int(qc.delay+cc.delay),
        events_executed=tl.run_counter,emissions=a.emitted,arrivals=b.arrivals,acknowledgments=a.acks,
        boundary='Single polarization photon transmission and explicit acknowledgment; no entanglement, memory, dark counts or QKD security',status='passed')
    (OUT/'sequence-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('emissions','arrivals','acknowledgments')},indent=2))
