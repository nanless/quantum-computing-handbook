#!/usr/bin/env python3
"""Run only local, authored stdlib experiments; verify vendor bytes and audio."""
import datetime, hashlib, json, pathlib, platform, subprocess, sys, wave
ROOT=pathlib.Path(__file__).resolve().parents[1]
COMMANDS=[['foundations/foundations_lab.py','--case','all'],['algorithms/experiments.py','all'],
 ['systems/hardware_flags.py'],['systems/weighted_decoder.py'],['systems/factory_schedule.py'],
 ['systems/network_wait.py'],['systems/routing_mapping.py'],['systems/service_timeline.py'],
 ['practice/experiments.py'],['snapshot_sources.py','--verify'],['tests/test_snapshot_sources.py']]

def main():
    if not __debug__: raise RuntimeError('Run without -O: assertions are part of validation')
    results=[]
    for args in COMMANDS:
        command=[sys.executable,str(ROOT/'codes'/args[0]),*args[1:]]
        run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90)
        results.append({'command':'python3 codes/'+' '.join(args),'returncode':run.returncode,
          'stdout':run.stdout,'stderr':run.stderr})
        print(('PASS' if run.returncode==0 else 'FAIL'),args[0],flush=True)
    audio_dir=ROOT/'handbook/assets/audio'
    if not audio_dir.exists(): audio_dir=ROOT/'assets/audio'  # portable reader layout
    manifest=json.loads((audio_dir/'manifest.json').read_text())
    audio=[]
    for entry in manifest['files']:
        path=audio_dir/entry['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
        with wave.open(str(path),'rb') as w:
            assert w.getnchannels()==manifest['channels']
            assert w.getframerate()==manifest['sample_rate_hz']
            assert w.getsampwidth()*8==manifest['pcm_bits']
            assert w.getnframes()==entry['frames']
            assert w.getnframes()/w.getframerate()==entry['duration_s']
        audio.append(entry['file'])
    report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'python':platform.python_version(),'checks':results,'verified_audio':audio,
      'scope':'authored stdlib tests, vendor integrity, WAV format; no upstream execution'}
    dest=ROOT/'work/research/round69-code-validation.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if any(x['returncode'] for x in results): raise SystemExit(1)
    print('All local checks passed; 5 WAV files verified.')
if __name__=='__main__': main()
