#!/usr/bin/env python3
"""Independent stdlib checks of actual runtime evidence, not SDK imports."""
import json,pathlib,math,re,statistics,hashlib
HERE=pathlib.Path(__file__).resolve().parent
load=lambda name:json.loads((HERE/name).read_text())
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
 d=load('slc-results.json');raw=load('slc-randomizations-counts.json')
 for record,batch in zip(d['finite_pec_batches'],raw):
  per=[]
  for count,signs in zip(batch['counts'],batch['pauli_signs']):
   N=sum(count.values());assert N==64
   mu=sum(n*(-1)**int(bits[-2]) for bits,n in count.items())/N
   per.append(record['gamma']*(-1)**sum(signs)*mu)
  estimate=statistics.mean(per);se=statistics.stdev(per)/math.sqrt(len(per));close(estimate,record['estimate']);close(se,record['cluster_standard_error'])
  flat_variance=(record['gamma']**2-estimate**2)/(len(per)*64)
  close(flat_variance,record['sdk_raw_stds_field']);close(se*math.sqrt((len(per)-1)/len(per)),record['sdk_broadcast_cluster_se_ddof0'])
  assert abs(estimate-record['reference'])<6*se
 for r in d['records']:assert r['observed_bias']<=r['bias_bound']+1e-10
 return {'randomizations':sum(r['num_randomizations'] for r in d['finite_pec_batches']),'shots':sum(r['num_randomizations']*r['shots_per_randomization'] for r in d['finite_pec_batches']),'scope':'independent signed count/cluster variance; bounds remain synthetic model conditions'}
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
 results={name:function() for name,function in [('mpf',mpf),('gst',gst),('pna',pna),('slc',slc),('hpc',hpc)]}
 (HERE/'saved-checks.json').write_text(json.dumps({'status':'passed','cases':results},indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
