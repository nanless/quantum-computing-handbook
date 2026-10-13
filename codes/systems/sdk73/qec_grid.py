"""Fixed-round dual-basis surface memories; ordinary/correlated matching paired on raw shots."""
import hashlib, json, importlib.metadata, platform, time
from pathlib import Path
import numpy as np
import stim, pymatching
from scipy.stats import beta, binomtest
if not __debug__: raise RuntimeError('Validation requires assertions; do not run with -O')
OUT=Path(__file__).resolve().parent

def interval(k,n,alpha):
    return [0 if k==0 else float(beta.ppf(alpha/2,k,n-k+1)),1 if k==n else float(beta.ppf(1-alpha/2,k+1,n-k))]

def run(basis,d,p,seed,n=10000):
    stem=f'{basis}-d{d}-p{p:g}'
    c=stim.Circuit.generated('surface_code:rotated_memory_'+basis,distance=d,rounds=7,
      after_clifford_depolarization=p,before_round_data_depolarization=p,
      before_measure_flip_probability=p,after_reset_flip_probability=p)
    dem=c.detector_error_model(decompose_errors=True)
    ordinary=pymatching.Matching.from_detector_error_model(dem)
    correlated=pymatching.Matching.from_detector_error_model(dem,enable_correlations=True)
    det,actual=c.compile_detector_sampler(seed=seed).sample(n,separate_observables=True)
    start=time.perf_counter_ns(); po=ordinary.decode_batch(det); ordinary_ns=time.perf_counter_ns()-start
    start=time.perf_counter_ns(); pc=correlated.decode_batch(det,enable_correlations=True); correlated_ns=time.perf_counter_ns()-start
    fo=np.any(po!=actual,axis=1); fc=np.any(pc!=actual,axis=1)
    assert actual.shape==po.shape==pc.shape==(n,1)
    if p==0: assert not det.any() and not actual.any() and not fo.any() and not fc.any()
    # Warm-up then timed complete-shot service, not incremental/real-time feedback.
    for j in range(10): correlated.decode(det[j],enable_correlations=True)
    durations=[]
    for j in range(min(1000,n)):
        start=time.perf_counter_ns(); single=correlated.decode(det[j],enable_correlations=True); durations.append(time.perf_counter_ns()-start)
        assert np.array_equal(single,pc[j])
    np.savez_compressed(OUT/(stem+'.npz'),detectors=np.packbits(det,axis=1,bitorder='little'),detector_count=c.num_detectors,
       actual=np.packbits(actual,axis=1,bitorder='little'),ordinary=np.packbits(po,axis=1,bitorder='little'),
       correlated=np.packbits(pc,axis=1,bitorder='little'),ordinary_failed=fo,correlated_failed=fc,service_ns=np.array(durations,dtype=np.int64))
    (OUT/(stem+'.stim')).write_text(str(c)+'\n'); (OUT/(stem+'.dem')).write_text(str(dem)+'\n')
    rescue=int(np.sum(fo&~fc)); regress=int(np.sum(~fo&fc)); discord=rescue+regress
    row=dict(basis=basis,distance=d,rounds=7,noise_each=p,seed=seed,shots=n,detectors=c.num_detectors,
        ordinary_failures=int(fo.sum()),correlated_failures=int(fc.sum()),rescued=rescue,regressed=regress,
        paired_exact_two_sided_p=1.0 if discord==0 else float(binomtest(rescue,discord,.5).pvalue),
        ordinary_ci95=interval(int(fo.sum()),n,.05),correlated_ci95=interval(int(fc.sum()),n,.05),
        ordinary_simultaneous_ci=interval(int(fo.sum()),n,.05/36),correlated_simultaneous_ci=interval(int(fc.sum()),n,.05/36),
        ordinary_batch_ns=ordinary_ns,correlated_batch_ns=correlated_ns,
        service_ns_quantiles={str(q):float(np.quantile(durations,q,method='inverted_cdf')) for q in (.5,.95,.99,1)},
        raw_sha256=hashlib.sha256((OUT/(stem+'.npz')).read_bytes()).hexdigest(),file=stem+'.npz')
    print(stem, row['ordinary_failures'],row['correlated_failures'],flush=True)
    return row

if __name__=='__main__':
    controls=[run(b,3,0,730100+i,1000) for i,b in enumerate(('x','z'))]
    rows=[run(b,d,p,730000+1000*bi+100*di+pi) for bi,b in enumerate(('x','z')) for di,d in enumerate((3,5,7)) for pi,p in enumerate((.001,.003,.006))]
    result=dict(date='2026-10-13',status='passed',python=platform.python_version(),platform=platform.platform(),
       versions={p:importlib.metadata.version(p) for p in ('stim','pymatching','numpy','scipy')},
       family_intervals='Bonferroni alpha=.05/36 for 18 grid points times 2 decoders; controls excluded',
       latency_scope='1000 sequential full seven-round shots after 10 warm-ups; Python call and native decode only, future rounds known',controls=controls,cases=rows)
    (OUT/'qec-grid-results.json').write_text(json.dumps(result,indent=2)+'\n')
