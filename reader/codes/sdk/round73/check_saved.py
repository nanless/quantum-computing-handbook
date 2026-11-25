#!/usr/bin/env python3
"""Independent stdlib checks of actual runtime evidence, not SDK imports."""
import json,pathlib,math,re,statistics,hashlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from validation_reports import ROOT, write_result


# The original raw lists have no separate batch IDs. These content identities
# bind the unchanged raw batches to the seeds in the archived summary.
SLC_BATCHES = (
 ('full', 730201, 0.0, 'b4b3d472ba3ef4f956d23b51a81c3801c7e2ca76914c650689944b58556ef881'),
 ('partial', 730202, 0.06, 'f7d4e7edd9754260bfaa1e392cbcc770a4b53d50ccda2dd1380affaa88763a2c'),
 ('none', 730203, 10.0, '204474cc61d9aa04e073f6422e265fca25a2983ccef6baa364e8d89157352896'),
)


def unique_object(pairs):
 out={}
 for key,value in pairs:
  if key in out: raise ValueError(f'Duplicate JSON key: {key!r}')
  out[key]=value
 return out


def load(name):
 return json.loads((HERE/name).read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def close(a,b,tol=1e-10):assert abs(a-b)<tol,(a,b)
def mv(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def gst():
 d=load('gst-long-results.json');m=d['model'];counts=load('gst-long-counts.json')
 def probability(circuit,fitted=False):
  v=m['fitted_rho' if fitted else 'rho'][:];ops=m['fitted_operations' if fitted else 'true_operations']
  for label in re.findall(r'\|([^|]+)\|',circuit):
   v=mv(ops['[]' if label.strip() in ('','[]') else label.strip()+':0'],v)
  return {label:dot(effect,v) for label,effect in m['fitted_effects' if fitted else 'effects'].items()}
 for fitted,name in [(False,'true'),(True,'fitted')]:
  total=0.
  for circuit,outcomes in counts.items():
   assert sum(outcomes.values())==4096 and all(n>=0 and n==int(n) for n in outcomes.values())
   probs=probability(circuit,fitted)
   total-=sum(n*math.log(max(probs[label],1e-12)) for label,n in outcomes.items())
  close(total,d['negative_log_likelihood'][name],1e-7)
 for r in d['unseen_predictions']:
  assert r['circuit'] not in counts;close(probability(r['circuit'])['0'],r['dense_reference']);close(probability(r['circuit'],True)['0'],r['fitted'])
 assert len(counts)*4096==d['total_shots']==1835008
 return {'settings':len(counts),'untrained_circuits':12,'scope':'saved Liouville contraction/counts; physicality independently checked by foundation cross review'}
def pna():
 d=load('pna-results.json');total=0.;variance=0.;budget=0
 for r in d['finite_shot']['records']:
  N=r['shots'];assert sum(r['counts'].values())==N
  mu=sum(f*(-1)**sum(int(b) for b,p in zip(bits,r['pauli']) if p!='I') for bits,f in r['counts'].items())/N
  close(mu,r['estimate']);total+=r['coefficient']*mu;variance+=r['coefficient']**2*(1-mu*mu)/(N-1);budget+=N
 close(total,d['finite_shot']['estimate']);close(math.sqrt(variance),d['finite_shot']['standard_error']);assert budget==20000
 # Generator independently contracts commuting / anticommuting Pauli terms.
 close(sum(abs(c) for c in d['coefficients'].values()),d['coefficient_l1'])
 close(d['mitigated'],d['ideal']);assert abs(total-d['ideal'])<6*math.sqrt(variance)
 return {'shots':budget,'estimate':total,'standard_error':math.sqrt(variance)}
def slc():
 d = load('slc-results.json')
 raw = load('slc-randomizations-counts.json')
 summary = d['finite_pec_batches']
 assert d['num_qubits'] == 3 and d['observable'] == 'IZI', 'Unexpected SLC observable or bit width'
 assert isinstance(raw, list) and len(raw) == len(SLC_BATCHES), 'Expected three raw SLC batches'
 assert isinstance(summary, list) and len(summary) == len(SLC_BATCHES), 'Expected three SLC summary batches'
 assert len({row['seed'] for row in summary}) == len(summary), 'Duplicate SLC summary seed'

 results = []
 seen = set()
 for record, batch, (mode, seed, tolerance, expected_digest) in zip(summary, raw, SLC_BATCHES):
  assert record['seed'] == seed and record['bias_tolerance'] == tolerance, f'{mode}: SLC identity mismatch'
  assert record['num_randomizations'] == 1024 and record['shots_per_randomization'] == 64, mode
  assert math.isfinite(record['gamma']) and record['gamma'] >= 1, mode
  assert all(isinstance(batch[key], list) and len(batch[key]) == 1024
             for key in ('parameters', 'pauli_signs', 'counts')), f'{mode}: incomplete SLC randomizations'
  per = []
  shots = 0
  for index, (parameters, signs, counts) in enumerate(zip(batch['parameters'], batch['pauli_signs'], batch['counts'])):
   case = f'{mode}, randomization {index}'
   assert len(parameters) == 33 and all(math.isfinite(value) for value in parameters), f'{case}: invalid parameters'
   assert len(signs) == 4 and all(type(sign) is bool for sign in signs), f'{case}: invalid sign vector'
   assert isinstance(counts, dict) and counts and all(
    re.fullmatch(r'[01]{3}', bits) and type(n) is int and n >= 0 for bits, n in counts.items()
   ), f'{case}: invalid counts or bit strings'
   n = sum(counts.values())
   assert n == 64, f'{case}: expected 64 shots, found {n}'
   shots += n
   mu = sum(count * (-1)**int(bits[-2]) for bits, count in counts.items()) / n
   per.append(record['gamma'] * (-1)**sum(signs) * mu)

  digest = hashlib.sha256(json.dumps(batch, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
  assert digest not in seen, f'{mode}: duplicate raw SLC batch'
  seen.add(digest)
  assert digest == expected_digest, f'{mode}: raw SLC batch does not match seed {seed}'
  estimate = statistics.mean(per)
  se = statistics.stdev(per) / math.sqrt(len(per))
  flat_variance = (record['gamma']**2 - estimate**2) / shots
  close(estimate, record['estimate'])
  close(estimate, record['sdk_estimate'])
  close(se, record['cluster_standard_error'])
  close(flat_variance, record['sdk_raw_stds_field'])
  close(flat_variance, record['independent_flat_variance'])
  close(se * math.sqrt((len(per) - 1) / len(per)), record['sdk_broadcast_cluster_se_ddof0'])
  assert abs(estimate - record['reference']) < 6*se
  results.append({
   'mode': mode, 'seed': seed, 'randomizations': len(per), 'shots': shots,
   'estimate': estimate, 'cluster_standard_error': se,
   'independent_flat_variance': flat_variance,
  })
 assert [row['bias_tolerance'] for row in d['records']] == [0.0, 0.01, 0.03, 0.06]
 for row in d['records']:
  assert row['observed_bias'] <= row['bias_bound'] + 1e-10
 return {
  'randomizations': sum(row['randomizations'] for row in results),
  'shots': sum(row['shots'] for row in results),
  'batches': results,
  'scope': 'independent signed count/cluster variance; bounds remain synthetic model conditions',
 }
def mpf():
 d=load('dynamic-mpf-results.json')
 for row in d['reference_order_counterexample']:
  p=row['p'];close(4*p**3+(1-4*p)**3,row['cubic_cancellation'])
  if row['mode']=='guarded_suzuki':assert abs(row['cubic_cancellation'])<1e-14;assert all(15<r<17 for r in row['halving_ratios'])
  else:assert all(3.9<r<4.1 for r in row['halving_ratios'])
 for r in d['records']:
  M=r['M_dense'];L=r['L_dense']
  for ref in r['references']:
   c=ref['weights'];close(sum(c),1,1e-8);close(sum(abs(x) for x in c),ref['gamma'])
   objective=dot(c,mv(M,c))-2*dot(c,L)+1
   close(objective,ref['frobenius_error']**2,3e-14);assert ref['frobenius_error']<ref['best_single_error']
 return {'times':3,'references':6,'scope':'objective and order checks; saved coefficients are ill-conditioned, not certified optimal'}
def hpc():
 d=load('hpc/results.json');outputs=[]
 for name in ['serial','threads1','threads2','threads4','threads8']:
  lines=[line for line in (HERE/'hpc'/f'philox-{name}.txt').read_text().splitlines() if line.startswith('philox')];outputs.append('\n'.join(lines));close(sum(float(l.split()[2]) for l in lines),1)
  for line in lines:bits=line.split()[1];assert bits[:4].count('1')==2 and bits[4:].count('1')==2
 assert len(set(outputs))==1;assert hashlib.sha256(outputs[0].encode()).hexdigest()==d['philox_sha256']
 return {'parallel_thread_counts':[1,2,4,8],'serial_identical':True}
def main():
 if not __debug__:raise RuntimeError('Run without -O')
 report_path = ROOT / 'work/research/sdk-saved-validation.json'
 results = {}
 for name, check in [('mpf', mpf), ('gst', gst), ('pna', pna), ('slc', slc), ('hpc', hpc)]:
  try:
   results[name] = check()
  except Exception as error:
   write_result(report_path, json.dumps({
    'status': 'failed', 'failed_case': name, 'error': f'{type(error).__name__}: {error}',
    'cases': results,
   }, indent=2) + '\n')
   raise
 write_result(report_path, json.dumps({'status': 'passed', 'cases': results}, indent=2) + '\n')
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()
