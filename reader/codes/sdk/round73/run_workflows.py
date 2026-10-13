#!/usr/bin/env python3
"""Explicit optional complete-SDK run, never imported by the stdlib runner."""
import pathlib,subprocess,sys,json,hashlib,time,platform,importlib.metadata,importlib.util
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Run without -O')
 records=[]
 for script,result in [('dynamic_mpf.py','dynamic-mpf-results.json'),('long_gst.py','gst-long-results.json'),('pna_workflow.py','pna-results.json'),('slc_workflow.py','slc-results.json')]:
  start=time.perf_counter();command=[sys.executable,'-u',str(HERE/script)]
  run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=300);log=HERE/(script.replace('.py','')+'-validated.log');log.write_text(run.stdout+run.stderr)
  row={'script':script,'command':command,'returncode':run.returncode,'elapsed_seconds':time.perf_counter()-start,'script_sha256':sha(HERE/script),'log':log.name,'log_sha256':sha(log),'result':result}
  if (HERE/result).exists():row['result_sha256']=sha(HERE/result)
  records.append(row);print(script,run.returncode,flush=True)
  if run.returncode:break
 hashes={}
 for mod,rel in [('quimb','tensor/tn1d/tebd.py'),('qiskit_addon_slc','bounds/local_scales.py'),('qiskit_mitigation','pec.py'),('qiskit_mitigation','utils/expectation_values.py')]:
  base=pathlib.Path(importlib.util.find_spec(mod).origin).parent;p=base/rel;hashes[mod+'/'+rel]={'installed_path':str(p),'sha256':sha(p)}
 report={'status':'passed' if len(records)==4 and all(r['returncode']==0 for r in records) else 'failed','python':platform.python_version(),'platform':platform.platform(),'records':records,'installed_source_hashes':hashes,'versions':{p:importlib.metadata.version(p) for p in ['qiskit','qiskit-aer','qiskit-addon-mpf','quimb','qiskit-addon-slc','qiskit-addon-pna','qiskit-mitigation','samplomatic','pauli-prop','pygsti','cvxpy','matplotlib']}}
 (HERE/'run-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
 if report['status']!='passed':raise SystemExit(1)
if __name__=='__main__':main()
