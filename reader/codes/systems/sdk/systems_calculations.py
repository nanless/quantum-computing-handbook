"""Independent deterministic hand calculations for S72-09/11/14/19.
Uses the SDK environment only for scipy derivative and exact binomial limits.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm,expm_frechet
from scipy.stats import beta
if not __debug__: raise RuntimeError('Run without -O')
OUT=Path(__file__).resolve().parent
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
# Direct average of six cardinal states checks qubit average overlap.
states=[np.array([1,0]),np.array([0,1])]+[np.array([1,z])/math.sqrt(2) for z in (1,-1,1j,-1j)]
p=.001
average=sum((1-p)+p/3*sum(abs(np.vdot(s,P@s))**2 for P in (X,Y,Z)) for s in states)/6
assert abs(average-(1-2*p/3))<1e-15
# Frechet derivative at a noncommuting time slice, compared to centered perturbation.
dt=.5; ux=.081; uy=-.034; delta=2*math.pi*.005
A=-1j*dt*(delta*Z+ux*X+uy*Y)/2;E=-1j*dt*X/2
analytic=expm_frechet(A,E,compute_expm=False);eps=1e-6
finite=(expm(A+eps*E)-expm(A-eps*E))/(2*eps)
assert np.max(abs(analytic-finite))<1e-9
commuting_approx=E@expm(A)
# Queue: arrivals every 1 us, one 4 us batch among twenty 0.8 us jobs.
service=[.8,.8,4]+[.8]*17;rows=[];end=0
for n,s in enumerate(service):
    start=max(float(n),end);end=start+s
    rows.append(dict(job=n,arrival_us=n,service_us=s,start_us=start,finish_us=end,latency_us=end-n,miss_2us_deadline=end-n>2+1e-12))
assert sum(service)/len(service)<1
assert max(r['latency_us'] for r in rows)==4
result=dict(access_date='2026-10-13',pauli_noise=dict(p=p,qubit_average_overlap=average,two_qubit_average_error=4*p/5),
    frechet_max_diff=float(np.max(abs(analytic-finite))),naive_commuting_derivative_max_diff=float(np.max(abs(analytic-commuting_approx))),
    queue=dict(mean_service_us=sum(service)/len(service),max_latency_us=max(r['latency_us'] for r in rows),
    misses=sum(r['miss_2us_deadline'] for r in rows),jobs=rows),status='passed')
(OUT/'systems-calculations.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
