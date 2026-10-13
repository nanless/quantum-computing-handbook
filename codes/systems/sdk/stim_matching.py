"""Circuit-level surface-code memory, full SDKs, no cloud calls.
Run: python codes/systems/sdk/stim_matching.py. Fixed model, not a hardware threshold.
"""
import hashlib, importlib.metadata, json, math, platform, time
from pathlib import Path
import numpy as np
import stim
import pymatching
from scipy.stats import beta
if not __debug__:
    raise RuntimeError('Run without -O: validation assertions are required')
OUT = Path(__file__).resolve().parent

def run(distance, probability, seed, shots=20000):
    circuit = stim.Circuit.generated('surface_code:rotated_memory_x', distance=distance,
        rounds=distance, after_clifford_depolarization=probability,
        before_round_data_depolarization=probability,
        before_measure_flip_probability=probability,
        after_reset_flip_probability=probability)
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    start=time.perf_counter()
    detections, actual=circuit.compile_detector_sampler(seed=seed).sample(shots, separate_observables=True)
    sample_time=time.perf_counter()-start
    start=time.perf_counter()
    predictions=matcher.decode_batch(detections)
    decode_time=time.perf_counter()-start
    failed=np.any(predictions != actual, axis=1)
    k=int(failed.sum())
    assert detections.shape==(shots,circuit.num_detectors)
    assert predictions.shape==actual.shape==(shots,1)
    assert np.array_equal(matcher.decode(detections[0]), predictions[0])
    if probability==0:
        assert k==0 and not detections.any() and not actual.any()
    lo=0.0 if k==0 else float(beta.ppf(0.025,k,shots-k+1))
    hi=1.0 if k==shots else float(beta.ppf(0.975,k+1,shots-k))
    suffix=f'd{distance}-p{probability:g}'
    (OUT/f'{suffix}.stim').write_text(str(circuit)+'\n')
    (OUT/f'{suffix}.dem').write_text(str(dem)+'\n')
    # Packed raw evidence retains every detector and logical bit, not just a best shot.
    np.savez_compressed(OUT/f'{suffix}-samples.npz', detectors=np.packbits(detections,axis=1,bitorder='little'),
        detector_count=circuit.num_detectors, actual=np.packbits(actual,axis=1,bitorder='little'),
        prediction=np.packbits(predictions,axis=1,bitorder='little'), failures=failed)
    digest=hashlib.sha256((OUT/f'{suffix}-samples.npz').read_bytes()).hexdigest()
    return dict(distance=distance, rounds=distance, noise_each=probability, shots=shots, seed=seed,
        detectors=circuit.num_detectors, measurements=circuit.num_measurements, qubit_index_span=circuit.num_qubits,
        logical_observables=circuit.num_observables, failures=k, p_experiment=k/shots,
        exact_binomial_95=[lo,hi], sample_seconds=sample_time, decode_batch_seconds=decode_time,
        decode_seconds_per_memory_shot=decode_time/shots, raw_sample_sha256=digest)

if __name__=='__main__':
    rows=[run(3,0.0,720100,1000)] + [run(d,0.001,720100+d) for d in (3,5,7)]
    data=dict(access_date='2026-10-13', python=platform.python_version(),platform=platform.platform(),
        versions={p:importlib.metadata.version(p) for p in ('stim','pymatching','numpy','scipy')},
        model='Pauli stochastic circuit-level noise; rotated X memory, rounds=distance; offline batch MWPM',
        cases=rows, status='passed')
    (OUT/'stim-matching-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
