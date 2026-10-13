#!/usr/bin/env python3
"""Actual long-sequence CPTPLND GST with raw counts and unseen predictions."""
import json,pathlib,time,platform,importlib.metadata
import numpy as np
import pygsti
from pygsti.modelpacks import smq1Q_XYI
from pygsti.circuits import Circuit
HERE=pathlib.Path(__file__).resolve().parent

def main():
 if not __debug__:raise RuntimeError('Run without -O')
 started=time.perf_counter();target=smq1Q_XYI.target_model()
 true=target.depolarize(op_noise=.004,spam_noise=.008)
 start_model=target.depolarize(op_noise=.001,spam_noise=.001)
 start_model.set_all_parameterizations('CPTPLND')
 target.set_all_parameterizations('CPTPLND')
 prep=smq1Q_XYI.prep_fiducials();meas=smq1Q_XYI.meas_fiducials();germs=smq1Q_XYI.germs();lengths=[1,2,4,8]
 circuit_lists=pygsti.circuits.create_lsgst_circuit_lists(target,prep,meas,germs,lengths)
 circuits=circuit_lists[-1];shots=4096
 data=pygsti.data.simulate_data(true,circuits,shots,seed=73019)
 raw={str(c):{','.join(o):float(n) for o,n in data[c].counts.items()} for c in circuits}
 (HERE/'gst-long-counts.json').write_text(json.dumps(raw,indent=2)+'\n')
 results=pygsti.drivers.run_long_sequence_gst(data,target,prep,meas,germs,lengths,
   advanced_options={'objective':'logl','starting_point':start_model,'max_iterations':150,'tolerance':1e-7},verbosity=1,disable_checkpointing=True)
 assert len(results.estimates)==1,list(results.estimates)
 estimate_name=next(iter(results.estimates));estimate=results.estimates[estimate_name];fitted=estimate.models['final iteration estimate'];records=[]
 rng=np.random.default_rng(73191)
 for length in [17,23,31]:
  for repeat in range(4):
   labels=[('Gxpi2',0) if x==0 else ('Gypi2',0) for x in rng.integers(0,2,length)]
   c=Circuit(labels,line_labels=(0,));assert c not in data
   vector=np.asarray(true.preps['rho0'].to_dense()).reshape(-1)
   for label in labels:vector=true.operations[label].to_dense('HilbertSchmidt')@vector
   effect=np.asarray(true.povms['Mdefault']['0'].to_dense()).reshape(-1)
   reference=float(effect@vector);prediction=float(fitted.probabilities(c)[('0',)])
   ideal=float(target.probabilities(c)[('0',)])
   records.append({'circuit':str(c),'length':length,'dense_reference':reference,'fitted':prediction,'ideal_target':ideal,'error':abs(reference-prediction)})
 assert max(r['error'] for r in records)<.03
 nlls={};score_details={}
 for name,model in [('ideal',target),('fitted',fitted),('true',true)]:
  nll=0.;zero_violations=0;minimum=1.
  for c in circuits:
   probs=model.probabilities(c)
   for outcome,count in data[c].counts.items():
    probability=float(probs[outcome]);minimum=min(minimum,probability)
    if count>0 and probability<=0:zero_violations+=1
    nll-=float(count)*np.log(max(probability,1e-12))
  nlls[name]=float(nll);score_details[name]={'clipped_negative_log_score':float(nll),'floor':1e-12,'positive_count_zero_probability_violations':zero_violations,'minimum_probability':minimum,'true_negative_log_likelihood':'infinite' if zero_violations else float(nll)}
 assert nlls['fitted']<nlls['ideal']
 # Save representation, not a pickle containing executable deserialization.
 model_record={'rho':true.preps['rho0'].to_dense().tolist(),'effects':{k:v.to_dense().tolist() for k,v in true.povms['Mdefault'].items()},'true_operations':{str(k):v.to_dense('HilbertSchmidt').tolist() for k,v in true.operations.items()},'fitted_rho':fitted.preps['rho0'].to_dense().tolist(),'fitted_effects':{k:v.to_dense().tolist() for k,v in fitted.povms['Mdefault'].items()},'fitted_operations':{str(k):v.to_dense('HilbertSchmidt').tolist() for k,v in fitted.operations.items()}}
 result={'status':'passed','python':platform.python_version(),'pygsti_version':importlib.metadata.version('pygsti'),'estimate_key':estimate_name,'parameterization':'CPTPLND','objective':'logl','lengths':lengths,'circuit_counts':[len(x) for x in circuit_lists],'unique_settings':len(raw),'shots_per_setting':shots,'total_shots':len(raw)*shots,'seed':73019,'negative_log_likelihood':nlls,'score_details':score_details,'prediction_seed':73191,'prediction_reference':'untrained circuits, exact population probabilities; no held-out finite counts','unseen_predictions':records,'model':model_record,'elapsed_seconds':time.perf_counter()-started,'scope':'finite-shot local Markov model, simultaneous SPAM/gates, constrained long-sequence likelihood; not every GST variant or device experiment'}
 (HERE/'gst-long-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='model'},indent=2))
if __name__=='__main__':main()
