#!/usr/bin/env python3
"""Rebuild formula-driven plot. Requires numpy/matplotlib from SDK lock."""
import json, math, pathlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=pathlib.Path(__file__).resolve().parents[2]
data=json.loads((root/'codes/algorithms/sdk/round72-results.json').read_text())
phase=np.array(data['cases']['pyqsp']['result']['phases_radians'])
fig,axes=plt.subplots(1,3,figsize=(15,4.4),constrained_layout=True)
t=np.linspace(0,math.sqrt(2)*math.pi,601); c=np.cos(math.sqrt(2)*t)
for y,label,style in [((1+c)**2/4,'vertex 0','-'),(np.sin(math.sqrt(2)*t)**2/2,'vertex 1','--'),((1-c)**2/4,'vertex 2','-.')]: axes[0].plot(t,y,style,label=label,lw=2)
axes[0].axvline(math.pi/math.sqrt(2),color='black',lw=.8,ls=':')
axes[0].set(xlabel='time t (model units)',ylabel='position probability',title='A. Three-vertex continuous-time walk',ylim=(-.02,1.05)); axes[0].legend(fontsize=9)
x=np.linspace(-1,1,401); actual=[]
for a in x:
    W=np.array([[a,1j*np.sqrt(1-a*a)],[1j*np.sqrt(1-a*a),a]])
    U=np.diag(np.exp(1j*phase[0]*np.array([1,-1])))
    for phi in phase[1:]: U=U@W@np.diag(np.exp(1j*phi*np.array([1,-1])))
    actual.append(U[0,0].imag)
axes[1].plot(x,.8*x**3-.3*x,'-',lw=2,label='target 0.3 T1 + 0.2 T3')
axes[1].plot(x[::20],np.array(actual)[::20],'x',ms=5,label='independent QSP reconstruction')
axes[1].set(xlabel='signal x (dimensionless)',ylabel='imaginary amplitude Im U00',title='B. Synthesized symmetric QSP'); axes[1].legend(fontsize=9)
d=np.arange(2,17); tails=np.array([sum(math.exp(-1)/math.factorial(n) for n in range(int(k),65)) for k in d])
axes[2].semilogy(d,tails,'o-',ms=4,label='omitted probability')
axes[2].semilogy(d,np.sqrt(tails),'s--',ms=4,label='trace distance = sqrt(tail)')
axes[2].set(xlabel='Fock dimension d (integer)',ylabel='dimensionless error',title='C. Coherent-state cutoff, |alpha|²=1'); axes[2].legend(fontsize=9)
for ax in axes: ax.grid(alpha=.22); ax.tick_params(labelsize=9)
(root/'handbook/assets').mkdir(exist_ok=True)
fig.savefig(root/'handbook/assets/round72-algorithms.svg')
svg=root/'handbook/assets/round72-algorithms.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
preview=root/'work/rendered/round72-algorithms.png'; preview.parent.mkdir(parents=True,exist_ok=True); fig.savefig(preview,dpi=160)
print(preview)
