#!/usr/bin/env python3
"""Scientific vector figure from saved real local SDK outputs (not hardware data)."""
import json,pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=pathlib.Path(__file__).resolve().parents[2]
data=json.loads((root/'codes/algorithms/sdk73/results-all.json').read_text())['cases']
r=data['hhl']['cases'][1:5];w=data['walk']['rows']
plt.rcParams.update({'font.size':10,'svg.fonttype':'none'})
fig,ax=plt.subplots(1,3,figsize=(13.8,4.8),layout='constrained')
t=[x['phase_bits'] for x in r]
ax[0].plot(t,[x['flag_success'] for x in r],'o-',label='Flag = 1')
ax[0].plot(t,[x['phase_zero_and_flag_success'] for x in r],'s--',label='Flag = 1 and phase = 0')
ax[0].axhline(r[0]['ideal_success'],color='black',ls=':',label='Ideal reciprocal')
ax[0].set(title='A. Finite QPE: two success events',xlabel='Phase register size t (bits)',ylabel='Probability (dimensionless)',xticks=t)
ax[0].legend(loc='best',fontsize=8)
ax[1].plot(t,[x['mixed_root_fidelity'] for x in r],'o-',label='Root fidelity, flag-only mixed state')
ax[1].plot(t,[x['garbage_given_flag'] for x in r],'s--',label='P(nonzero phase | flag = 1)')
ax[1].set(title='B. Garbage is not solved by inversion',xlabel='Phase register size t (bits)',ylabel='Dimensionless value',xticks=t,ylim=(-.03,1.08))
ax[1].legend(loc='center right',fontsize=8)
ax[2].plot([x['steps'] for x in w],[x['marked_probability'] for x in w],'o-',label='SKW marked-vertex probability')
ax[2].axhline(1/16,color='black',ls=':',label='Unmarked / classical uniform marginal')
ax[2].plot(4,25/64,'s',ms=8,fillstyle='none',color='black',label='Selected earliest peak (4 steps)')
ax[2].set(title='C. Coherent walk search can overshoot',xlabel='Number of full walk steps',ylabel='Final marked probability',xticks=[0,4,8,12,16],ylim=(-.015,.46))
ax[2].legend(loc='upper center',bbox_to_anchor=(.5,-.17),fontsize=8)
for a in ax:a.grid(alpha=.25);a.spines[['top','right']].set_visible(False)
fig.suptitle('Signed off-grid HHL and 16-vertex discrete walk search',fontsize=13)
asset=root/'handbook/assets/round73-algorithms.svg';png=root/'work/rendered/round73-algorithms.png'
png.parent.mkdir(exist_ok=True,parents=True)
fig.savefig(asset);fig.savefig(png,dpi=160)
asset.write_text('\n'.join(x.rstrip() for x in asset.read_text().splitlines())+'\n')
print(asset);print(png)
