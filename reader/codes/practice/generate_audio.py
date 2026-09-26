#!/usr/bin/env python3
"""Synthetic sonification, NOT recordings of quantum hardware. Stdlib only."""
import array, hashlib, json, math, pathlib, sys, wave
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'handbook/assets/audio'
SR=22050; DURATION=4; CARRIER=440; GAIN=0.2

def signal(kind,t):
    carrier=2*math.pi*CARRIER*t
    if kind in ('phase-0','phase-120','phase-180'):
        phase={'phase-0':0,'phase-120':2*math.pi/3,'phase-180':math.pi}[kind]
        return GAIN*(math.sin(carrier)+math.sin(carrier+phase))
    phase=2*math.pi*t # exactly one synthetic fringe per second
    visibility=1 if kind=='ramsey-ideal' else math.exp(-t/1.5)
    probability=(1+visibility*math.cos(phase))/2
    return 2*GAIN*math.sqrt(max(0,probability))*math.sin(carrier)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]
    for kind in ['phase-0','phase-120','phase-180','ramsey-ideal','ramsey-decay']:
        samples=[]; floating=[]
        for i in range(SR*DURATION):
            t=i/SR
            ramp=min(1,t/0.01,(DURATION-1/SR-t)/0.01)
            x=signal(kind,t)*max(0,ramp)
            assert abs(x)<=0.400000001
            floating.append(x); samples.append(round(x*32767))
        pcm=array.array('h',samples)
        if sys.byteorder!='little': pcm.byteswap()
        dest=OUT/(kind+'.wav')
        with wave.open(str(dest),'wb') as out:
            out.setnchannels(1); out.setsampwidth(2); out.setframerate(SR)
            out.writeframes(pcm.tobytes())
        with wave.open(str(dest),'rb') as check:
            assert check.getnframes()==SR*DURATION and check.getnchannels()==1
        records.append({'file':dest.name,'frames':len(samples),'duration_s':DURATION,
          'peak':max(abs(x) for x in floating),
          'rms':math.sqrt(sum(x*x for x in floating)/len(floating)),
          'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    assert records[2]['peak']<1e-10
    assert abs(records[0]['rms']/records[1]['rms']-2)<0.002
    manifest={'origin':'synthetic classical teaching audio, not laboratory recording',
      'sample_rate_hz':SR,'channels':1,'pcm_bits':16,'carrier_hz':CARRIER,
      'component_gain':GAIN,'fade_s':0.01,'fringe_hz':1,'decay_time_s':1.5,
      'normalization':'same fixed gain; no per-file normalization','files':records}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))
if __name__=='__main__': main()
