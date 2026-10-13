#!/usr/bin/env python3
"""Independently recheck saved GST counts and PTM matrices without importing pyGSTi."""
import hashlib,json,re
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
record_path=ROOT/'codes/sdk/round73/gst-long-results.json'
counts_path=ROOT/'codes/sdk/round73/gst-long-counts.json'
r=json.loads(record_path.read_text());data=json.loads(counts_path.read_text())
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
basis=[m/np.sqrt(2) for m in [I,X,Y,Z]]
def matrix(v):return sum(c*p for c,p in zip(v,basis))
def choi(G):
 out=np.zeros((4,4),complex)
 for a in (0,1):
  for b in (0,1):
   e=np.zeros((2,2),complex);e[a,b]=1
   coefficients=np.array([np.trace(p@e) for p in basis])
   out[2*a:2*a+2,2*b:2*b+2]=matrix(G@coefficients)
 return out
def labels(c):return [v.strip()+':0' if v.strip() not in ('','[]') else '[]' for v in re.findall(r'\|([^|]+)\|',c)]
def probability(c,prep,effects,ops):
 v=np.array(prep)
 for label in labels(c):v=np.array(ops[label])@v
 return {k:float(np.array(e)@v) for k,e in effects.items()}
def spectra(model):
 rho=matrix(model['prep']);effects=[matrix(v) for v in model['effects'].values()]
 assert abs(np.trace(rho)-1)<1e-10 and np.linalg.eigvalsh(rho).min()>-1e-8
 assert np.max(abs(sum(effects)-I))<1e-10
 assert all(np.linalg.eigvalsh(e).min()>-1e-8 for e in effects)
 rows={}
 for key,g in model['ops'].items():
  J=choi(np.array(g));ptr=np.einsum('aibi->ab',J.reshape(2,2,2,2))
  assert np.max(abs(J-J.conj().T))<1e-10
  assert np.linalg.eigvalsh(J).min()>-1e-7
  assert np.max(abs(ptr-I))<1e-10
  rows[key]={'choi_eigenvalues':np.linalg.eigvalsh(J).tolist(),'tp_max_error':float(np.max(abs(ptr-I)))}
 return {'rho_eigenvalues':np.linalg.eigvalsh(rho).tolist(),'effect_eigenvalues':[np.linalg.eigvalsh(e).tolist() for e in effects],'operations':rows}
model=r['model'];true={'prep':model['rho'],'effects':model['effects'],'ops':model['true_operations']}
fit={'prep':model['fitted_rho'],'effects':model['fitted_effects'],'ops':model['fitted_operations']}
nll={};norm_error=0
for name,m in [('true',true),('fitted',fit)]:
 value=0;minimum=1
 for c,counts in data.items():
  assert sum(counts.values())==4096 and all(float(v).is_integer() and v>=0 for v in counts.values())
  p=probability(c,m['prep'],m['effects'],m['ops'])
  norm_error=max(norm_error,abs(sum(p.values())-1))
  assert min(p.values())>0;minimum=min(minimum,min(p.values()))
  value-=sum(n*np.log(p[o]) for o,n in counts.items())
 assert abs(value-r['negative_log_likelihood'][name])<1e-7
 nll[name]={'independent_negative_log_likelihood':float(value),'minimum_training_probability':float(minimum)}
assert len(data)==448 and sum(sum(v.values()) for v in data.values())==1835008
max_true=0;max_fit=0
for u in r['unseen_predictions']:
 assert u['circuit'] not in data
 assert len(labels(u['circuit']))==u['length']
 p=probability(u['circuit'],true['prep'],true['effects'],true['ops'])['0']
 q=probability(u['circuit'],fit['prep'],fit['effects'],fit['ops'])['0']
 max_true=max(max_true,abs(p-u['dense_reference']));max_fit=max(max_fit,abs(q-u['fitted']))
assert max_true<1e-12 and max_fit<1e-12
S=np.diag([1.,1.2,.8,1.1]);inv=np.linalg.inv(S)
gauge={'prep':S@np.array(fit['prep']),'effects':{k:np.array(v)@inv for k,v in fit['effects'].items()},'ops':{k:S@np.array(v)@inv for k,v in fit['ops'].items()}}
gauge_error=max(abs(probability(u['circuit'],fit['prep'],fit['effects'],fit['ops'])['0']-probability(u['circuit'],gauge['prep'],gauge['effects'],gauge['ops'])['0']) for u in r['unseen_predictions'])
assert gauge_error<1e-12
report={'status':'passed','independence':'NumPy dense PTM reconstruction, no pyGSTi import or fitter call','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [record_path,counts_path]},
 'settings':len(data),'shots':1835008,'spectra':{'true':spectra(true),'fitted':spectra(fit)},'nll':nll,'max_probability_normalization_error':norm_error,
 'unseen_training_members':0,'exact_prediction_crosscheck_error':max_true,'fitted_prediction_crosscheck_error':max_fit,
 'coordinate_gauge_probability_error':gauge_error,'gauge_boundary':'arbitrary invertible S is coordinate freedom, not itself physical channel',
 'review_findings':['ideal zero probabilities made finite only by floor 1e-12; label as clipped score, not finite exact likelihood','unseen predictions use exact generating probabilities, no held-out shot batch','persist unseen circuit generation seed 73191 and physical spectra/TP checks']}
(Path(__file__).resolve().parent/'round73-cross-gst-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
