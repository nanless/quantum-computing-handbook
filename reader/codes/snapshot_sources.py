#!/usr/bin/env python3
"""Curated upstream excerpts. --refresh fetches HEAD; --fetch restores pinned files;
--verify (default) checks local bytes. Downloaded source is NEVER executed here.
Uses git and curl, no GitHub API token, no Python third-party dependencies.
"""
import argparse, concurrent.futures, datetime, hashlib, json, pathlib, subprocess, tempfile, os, re
BASE = pathlib.Path(__file__).resolve().parent
MANIFEST = BASE / 'vendor' / 'manifest.json'
PROJECTS = {
 'qiskit-algorithms': ('qiskit-community/qiskit-algorithms', ['qiskit_algorithms/amplitude_amplifiers/grover.py','qiskit_algorithms/amplitude_estimators/iae.py','qiskit_algorithms/phase_estimators/phase_estimation.py','qiskit_algorithms/minimum_eigensolvers/vqe.py']),
 'cirq': ('quantumlib/Cirq', ['examples/grover.py','examples/shor.py','examples/phase_estimator.py']),
 'pennylane': ('PennyLaneAI/pennylane', ['pennylane/templates/subroutines/qsvt.py','pennylane/qaoa/cost.py','pennylane/shadows/classical_shadow.py','pennylane/gradients/parameter_shift.py']),
 'openfermion': ('quantumlib/OpenFermion', ['src/openfermion/transforms/opconversions/jordan_wigner.py','src/openfermion/circuits/trotter/simulate_trotter.py']),
 'qualtran': ('quantumlib/Qualtran', ['qualtran/bloqs/qft/qft_text_book.py','qualtran/bloqs/arithmetic/addition.py','qualtran/bloqs/qubitization/qubitization_walk_operator.py','qualtran/bloqs/block_encoding/linear_combination.py']),
 'qiskit-addon-sqd': ('Qiskit/qiskit-addon-sqd', ['qiskit_addon_sqd/configuration_recovery.py','qiskit_addon_sqd/fermion.py']),
 'qutip': ('qutip/qutip', ['qutip/solver/mesolve.py','qutip/solver/mcsolve.py']),
 'quimb': ('jcmgray/quimb', ['quimb/tensor/circuit_gen.py','quimb/tensor/contraction.py']),
 'stim': ('quantumlib/Stim', ['src/stim/gen/gen_surface_code.cc','src/stim/gen/gen_rep_code.cc']),
 'pymatching': ('oscarhiggott/PyMatching', ['src/pymatching/matching.py']),
 'mitiq': ('unitaryfoundation/mitiq', ['mitiq/zne/scaling/folding.py','mitiq/zne/inference.py']),
 'dimod': ('dwavesystems/dimod', ['dimod/reference/samplers/exact_solver.py']),
 'qiskit': ('Qiskit/qiskit', ['qiskit/transpiler/passes/routing/sabre_swap.py','qiskit/quantum_info/states/utils.py','qiskit/quantum_info/operators/channel/kraus.py']),
 'sequence': ('sequence-toolbox/SeQUeNCe', ['sequence/entanglement_management/teleportation.py','sequence/entanglement_management/entanglement_protocol.py']),
 'liboqs': ('open-quantum-safe/liboqs', ['tests/example_kem.c']),
 'pyqsp': ('ichuang/pyqsp', ['pyqsp/angle_sequence.py','pyqsp/sym_qsp_opt.py','pyqsp/response.py']),
 'qutip-qtrl': ('qutip/qutip-qtrl', ['src/qutip_qtrl/pulseoptim.py','src/qutip_qtrl/grape.py']),
 'qiskit-addon-cutting': ('Qiskit/qiskit-addon-cutting', ['qiskit_addon_cutting/qpd/weights.py','qiskit_addon_cutting/cutting_reconstruction.py']),
 'qiskit-aer': ('Qiskit/qiskit-aer', ['qiskit_aer/noise/errors/standard_errors.py']),
 'qiskit-addon-mpf': ('Qiskit/qiskit-addon-mpf', ['qiskit_addon_mpf/static.py','qiskit_addon_mpf/dynamic.py','qiskit_addon_mpf/costs/lse.py','qiskit_addon_mpf/costs/exact.py']),
 'qiskit-addon-obp': ('Qiskit/qiskit-addon-obp', ['qiskit_addon_obp/backpropagation.py','qiskit_addon_obp/utils/truncating.py','qiskit_addon_obp/utils/metadata.py']),
 'qiskit-addon-sqd-hpc': ('Qiskit/qiskit-addon-sqd-hpc', ['include/qiskit/addon/sqd/subsampling.hpp','include/qiskit/addon/sqd/configuration_recovery.hpp','include/qiskit/addon/sqd/fermion.hpp','include/qiskit/addon/sqd/internal/parallel-rng.hpp']),
 'pauli-prop': ('Qiskit/pauli-prop', ['python/pauli_prop/propagation.py','src/lib.rs']),
 'thewalrus': ('XanaduAI/thewalrus', ['thewalrus/quantum/gaussian_checks.py']),
 'qiskit-experiments': ('qiskit-community/qiskit-experiments', ['qiskit_experiments/library/tomography/qpt_experiment.py','qiskit_experiments/library/tomography/tomography_analysis.py']),
 'pygsti': ('sandialabs/pyGSTi', ['pygsti/modelmembers/instruments/instrument.py']),
}
def command(args):
 return subprocess.check_output(args, stderr=subprocess.PIPE, timeout=90)
def download(url, optional=False):
 try: return command(['curl','-fsSL','--retry','2','--max-time','45',url])
 except subprocess.CalledProcessError as e:
  if optional and b'404' in e.stderr: return None
  raise RuntimeError('Download failed: '+url+' '+e.stderr.decode(errors='replace')[-180:]) from e

def save_file(name, repo, commit, rel, optional=False, destination=None):
 url=f'https://raw.githubusercontent.com/{repo}/{commit}/{rel}'
 data=download(url,optional)
 if data is None: return None
 dest=(destination or BASE/'vendor')/name/rel
 dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
 return {'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'url':url}

def refresh_project(pair, destination=None):
 name,(repo,paths)=pair
 sha=command(['git','ls-remote',f'https://github.com/{repo}.git','HEAD']).decode().split()[0]
 assert re.fullmatch(r'[0-9a-f]{40}',sha)
 records=[]
 for rel in ['LICENSE','LICENSE.txt','LICENSE.md','COPYING','NOTICE','NOTICE.txt','THIRD_PARTY_NOTICES.md','AUTHORS','AUTHORS.md']:
  record=save_file(name,repo,sha,rel,True,destination)
  if record: records.append(record)
 if not any(r['path'].startswith(('LICENSE','COPYING')) for r in records):
  raise RuntimeError(f'{name}: missing license; no source downloaded')
 for rel in paths:
  record=save_file(name,repo,sha,rel,True,destination)
  if record: records.append(record)
 if not any(r['path'] in paths for r in records): raise RuntimeError(name+': no source paths found')
 print(name,sha,len(records),'files',flush=True)
 return {'name':name,'repository':f'https://github.com/{repo}','commit':sha,
   'kind':'unmodified-source-excerpts-not-installable-package','files':records,
   'missing_requested_paths':[p for p in paths if p not in [r['path'] for r in records]]}

def verify(data, directory=None):
 count=0
 for project in data['projects']:
  assert re.fullmatch(r'[0-9a-f]{40}',project['commit'])
  for record in project['files']:
   assert not pathlib.PurePosixPath(record['path']).is_absolute() and '..' not in pathlib.PurePosixPath(record['path']).parts
   raw=((directory or BASE/'vendor')/project['name']/record['path']).read_bytes()
   assert hashlib.sha256(raw).hexdigest()==record['sha256'],record['path']
   assert len(raw)==record['bytes']; count+=1
 print(json.dumps({'projects':len(data['projects']),'verified_files':count},indent=2))

def replace_snapshot(staging):
 # Directory renames happen only after all downloads and hashes succeeded.
 # Roll back a publication error; callers must not run a concurrent build.
 current=BASE/'vendor'; backup=staging.parent/'previous'
 if current.exists(): os.replace(current,backup)
 try: os.replace(staging,current)
 except BaseException:
  if backup.exists(): os.replace(backup,current)
  raise

def refresh_readme(data):
 rows=['# Third-party source snapshots', '',
  'Unmodified excerpts, not installable packages. Retain all original license files.',
  'See manifest.json for exact source URLs and SHA-256. No upstream runtime tests performed.', '',
  '| Repository | Commit | Local files |','|---|---|---|']
 for p in data['projects']:
  files=' · '.join('['+f['path']+']('+p['name']+'/'+f['path']+')' for f in p['files'])
  rows.append('| ['+p['name']+']('+p['repository']+') | '+p['commit']+' | '+files+' |')
 return '\n'.join(rows)+'\n'

def main():
 if not __debug__: raise RuntimeError('Run without -O: integrity checks must stay enabled')
 parser=argparse.ArgumentParser(description=__doc__)
 mode=parser.add_mutually_exclusive_group()
 mode.add_argument('--refresh',action='store_true',help='Network: create NEW snapshots of current HEAD')
 mode.add_argument('--fetch',action='store_true',help='Network: restore exactly the existing manifest')
 mode.add_argument('--verify',action='store_true')
 args=parser.parse_args()
 if not args.refresh and not args.fetch:
  verify(json.loads(MANIFEST.read_text())); return
 with tempfile.TemporaryDirectory(prefix='.snapshot-',dir=BASE) as temp:
  staging=pathlib.Path(temp)/'next'; staging.mkdir()
  if args.refresh:
   with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    projects=list(pool.map(lambda pair: refresh_project(pair,staging),PROJECTS.items()))
   data={'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'curated excerpts; no upstream runtime tests performed','projects':projects}
   readme=refresh_readme(data)
  else:
   data=json.loads(MANIFEST.read_text())
   readme=(BASE/'vendor/README.md').read_text()
   for project in data['projects']:
    for record in project['files']:
     rel=pathlib.PurePosixPath(record['path'])
     assert not rel.is_absolute() and '..' not in rel.parts
     raw=download(record['url'])
     assert hashlib.sha256(raw).hexdigest()==record['sha256'],record['url']
     dest=staging/project['name']/record['path']
     dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw)
  verify(data,staging)
  (staging/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
  (staging/'README.md').write_text(readme)
  replace_snapshot(staging)
 verify(data)
if __name__=='__main__': main()
