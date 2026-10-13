"""Configure/build an existing official fixed checkout, run standard KEM checks.
python run_liboqs.py --source /tmp/quantum-round72-liboqs --cmake /opt/homebrew/bin/cmake
Cloning is deliberately an explicit step in README, not a hidden action here.
"""
import argparse,hashlib,json,platform,subprocess
from pathlib import Path
if not __debug__: raise RuntimeError('Run without -O')
OUT=Path(__file__).resolve().parent
COMMIT='97f6b86b1b6d109cfd43cf276ae39c2e776aed80'
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--cmake',default='cmake');args=p.parse_args()
source=Path(args.source).resolve();build=source/'build'
actual=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
if actual!=COMMIT: raise RuntimeError(f'Expected {COMMIT}, got {actual}')
commands=[]
def run(command):
    proc=subprocess.run([str(c) for c in command],capture_output=True,text=True)
    commands.append(dict(command=[str(c) for c in command],returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr))
    (OUT/'liboqs-build-run.json').write_text(json.dumps(dict(commit=actual,platform=platform.platform(),commands=commands,status='running'),indent=2)+'\n')
    if proc.returncode: raise RuntimeError(f'Failed command {command}: {proc.stderr}')
    return proc.stdout
run([args.cmake,'-S',source,'-B',build,'-DOQS_MINIMAL_BUILD=KEM_ml_kem_512;KEM_ml_kem_768;KEM_ml_kem_1024','-DOQS_USE_OPENSSL=OFF','-DCMAKE_BUILD_TYPE=Release'])
run([args.cmake,'--build',build,'--clean-first','--parallel','4'])
run([build/'tests/example_kem'])
for algorithm in ('ML-KEM-512','ML-KEM-768','ML-KEM-1024'): run([build/'tests/test_kem',algorithm])
program=build/'round72-roundtrip'
run(['cc','-O2','-Wall','-Wextra','-I',build/'include',OUT/'liboqs_roundtrip.c',build/'lib/liboqs.a','-o',program])
results=json.loads(run([program]))
data=dict(access_date='2026-10-13',tag='0.15.0',commit=actual,platform=platform.platform(),
    compiler=run(['cc','--version']).splitlines()[0],algorithms=results,commands=commands,
    source_license_sha256=hashlib.sha256((source/'LICENSE.txt').read_bytes()).hexdigest(),
    scope='Complete official build dependency for selected ML-KEM algorithms; no TLS/FIPS certification',status='passed')
(OUT/'liboqs-build-run.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(dict(commit=actual,algorithms=results,status='passed'),indent=2))
