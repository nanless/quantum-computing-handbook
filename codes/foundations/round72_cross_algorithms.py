#!/usr/bin/env python3
"""Independent review of four A72 derivations; uses saved SDK raw data."""
import json, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
if not __debug__:
    raise RuntimeError('Assertions required')
H = np.array([[1,1],[1,-1]]) / np.sqrt(2)
U = H @ np.diag([1j,-1]) @ H
# Explicit positive-sign DFT, independent of Cirq QFT.
F = np.array([[np.exp(2j*np.pi*j*k/4)/2 for k in range(4)] for j in range(4)])
ctrl = np.zeros((8,8), complex)
for k in range(4):
    ctrl[2*k:2*k+2,2*k:2*k+2] = np.linalg.matrix_power(U,k)
Q = np.kron(F.conj().T,np.eye(2)) @ ctrl @ np.kron(np.kron(H,H),np.eye(2))
initial = np.zeros(16,complex); initial[0] = 1
before = np.kron(Q,np.eye(2)) @ initial
assert np.max(abs(before.reshape(4,2,2)[1,:,0]-np.array([1,1])/2)) < 1e-12
assert np.max(abs(before.reshape(4,2,2)[2,:,0]-np.array([1,-1])/2)) < 1e-12
hhl = []
for C in [1.,.5]:
    rot = np.eye(16,dtype=complex)
    for label,lam in [(1,1),(2,2)]:
        a = C/lam; c = np.sqrt(1-a*a); R = np.array([[c,-a],[a,c]])
        rot[4*label:4*label+4,4*label:4*label+4] = np.kron(np.eye(2),R)
    final = np.kron(Q.conj().T,np.eye(2)) @ rot @ before
    branch = final.reshape(4,2,2)[:,:,1]; p = float(np.linalg.norm(branch)**2); x = branch[0]/np.sqrt(p)
    assert np.max(abs(branch[1:])) < 1e-12
    assert np.max(abs(x-np.array([3,1])/np.sqrt(10))) < 1e-12
    assert abs(p-C*C*5/8) < 1e-12
    hhl.append({'C':C,'success':p,'x_real':x.real.tolist(),'max_nonzero_phase':float(np.max(abs(branch[1:])))})
sdk = json.loads((ROOT/'codes/algorithms/sdk/round72-results.json').read_text())
ph = sdk['cases']['pyqsp']['result']['phases_radians']; errors = []
for x in [-1,-1/np.sqrt(8),-.5,0,.5,1/np.sqrt(8),1]:
    W = np.array([[x,1j*np.sqrt(1-x*x)],[1j*np.sqrt(1-x*x),x]]); V = np.eye(2,dtype=complex)
    for j,phi in enumerate(ph):
        if j: V = V @ W
        V = V @ np.diag([np.exp(1j*phi),np.exp(-1j*phi)])
    errors.append(float(abs(V[0,0].imag-(.8*x**3-.3*x))))
    assert abs(np.linalg.det(V)-1) < 1e-12
raw = np.load(ROOT/'codes/algorithms/sdk/shadow-samples.npz',allow_pickle=False)
bits = raw['bits'].astype(int); bases = raw['recipes']; counts = []
for axis in range(3):
    mask = np.all(bases==axis,axis=1); product = (1-2*bits[:,0])*(1-2*bits[:,1]); counts.append(int(mask.sum()))
    assert np.all(product[mask]==[1,-1,1][axis])
assert counts == [3376,3386,3304]
N = 6; u = plug = 0
for k in range(7):
    w = math.comb(N,k)*(1/3)**k*(2/3)**(N-k); plug += w*(1+(k/2)**2)/2
    pair = (9*k*k-9*k)/(N*(N-1)); u += w*(1+pair)/2
assert abs(plug-7/6) < 1e-12 and abs(u-1) < 1e-12
p60 = math.exp(-1)/math.factorial(60); remainder = p60/(1-1/61)
assert remainder < 1e-80
result = {'date':'2026-10-13','independent_hhl_DFT_matrix':hhl,'qsp_max_selected_error':max(errors),
          'shadow_matching_counts':counts,'plugin_purity_mean':plug,'U_statistic_purity_mean':u,
          'CV_tail_after_59_upper_bound':remainder,
          'scope':'independent fixed-input reconstruction and saved raw data; not repeated full SDK installation'}
(ROOT/'work/research/round72-cross-foundations-algorithms-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
