"""Re-decode every saved detector shot; no resampling or optimization, full SDK APIs."""
import hashlib,json
from pathlib import Path
import numpy as np
import stim,pymatching
from scipy.linalg import expm
if not __debug__: raise RuntimeError('Validation requires assertions; do not run with -O')
OUT=Path(__file__).resolve().parent
report=json.loads((OUT/'qec-grid-results.json').read_text()); rows=[]
for r in report['cases']+report['controls']:
    raw=OUT/r['file'];assert hashlib.sha256(raw.read_bytes()).hexdigest()==r['raw_sha256']
    archive=np.load(raw);det=np.unpackbits(archive['detectors'],axis=1,bitorder='little')[:,:r['detectors']]
    dem=stim.DetectorErrorModel.from_file(OUT/r['file'].replace('.npz','.dem'))
    for name,enabled in [('ordinary',False),('correlated',True)]:
        matcher=pymatching.Matching.from_detector_error_model(dem,enable_correlations=enabled)
        result=matcher.decode_batch(det,enable_correlations=enabled)
        assert np.array_equal(result,archive[name])
    rows.append(dict(file=r['file'],shots=r['shots'],both_predictions_replayed=True))
# The standard-library 49-term Taylor replay and six-state 2-design verify the control result independently.
import sys
sys.path.insert(0,str(OUT.parent))
from round73_checks import case14,case12
result=dict(status='passed',qec=rows,complete_shots=sum(r['shots'] for r in rows),control=case14(),network=case12())
(OUT/'saved-results-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
