#!/usr/bin/env python3
"""Scientific SVG/PNG from actual round73 SDK outputs; no invented points."""
import hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
R=Path(__file__).resolve().parent
source=R/'sdk73/all-results.json'
data=json.loads(source.read_text())
assert all(v['status']=='passed' for v in data['cases'].values())
d=data['cases']['dynamics']['result']
t=np.array(d['times_us']);truth=np.array(d['independent_bloch']);mean=np.array(d['mc_means']);se=np.array(d['mc_standard_errors'])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,'axes.labelsize':11,'svg.fonttype':'none'})
fig,ax=plt.subplots(2,2,figsize=(12.6,8.6))
fig.subplots_adjust(left=.075,right=.97,top=.89,bottom=.10,wspace=.27,hspace=.43)
fig.suptitle('Driven open qubit: model, sampling and time-order convergence',fontsize=17,x=.52,y=.97)
fig.text(.075,.92,'Synthetic CPU data · time in μs · Ω, Δ in rad/μs · κ = 0.4 /μs',fontsize=11,color='#475569')
blue='#1e40af';orange='#b45309';green='#0f766e';gray='#64748b'
ax[0,0].plot(t,1.1*np.exp(-((t-1.5)/.35)**2),color=blue,lw=2.5,label='Gaussian Ω(t)')
ax[0,0].axhline(.7,color=orange,ls='--',lw=1.8,label='constant Δ = 0.7')
ax[0,0].set(xlabel='time t (μs)',ylabel='angular rate (rad/μs)',title='A. Narrow drive plus detuning',xlim=(0,3),ylim=(-.04,1.2))
ax[0,0].legend(loc='upper left',frameon=False)
ax[0,1].plot(t,truth[2],color=blue,lw=2.5,label='independent Bloch ODE')
ax[0,1].plot(t,np.array(d['mesolve_bloch'])[2],color=green,lw=1.6,ls='--',label='QuTiP mesolve')
stride=np.arange(0,len(t),4)
ax[0,1].errorbar(t[stride],mean[2,stride],yerr=se[2,stride],fmt='s',ms=4,color=orange,capsize=2,linewidth=1.1,label='2048 trajectories ± 1 SE')
ax[0,1].set(xlabel='time t (μs)',ylabel='mean Z (dimensionless)',title='B. Open evolution with finite trajectory noise',xlim=(0,3),ylim=(-.03,1))
ax[0,1].legend(loc='upper left',frameon=False,fontsize=9)
ax[1,0].axhline(0,color=gray,lw=1)
ax[1,0].fill_between(t,-se[2],se[2],color=blue,alpha=.12,label='pointwise ± 1 empirical SE')
ax[1,0].plot(t,mean[2]-truth[2],color=orange,lw=1.8,marker='s',markevery=4,ms=3.5,label='trajectory mean − reference')
ax[1,0].set(xlabel='time t (μs)',ylabel='Z residual (dimensionless)',title='C. Sampling error is separate from ODE error',xlim=(0,3))
ax[1,0].legend(loc='lower right',frameon=False,fontsize=9)
rows=d['closed_midpoint_convergence'];steps=np.array([r['steps'] for r in rows]);errs=np.array([r['max_final_bloch_error'] for r in rows])
ax[1,1].loglog(steps,errs,'o-',color=blue,lw=2,ms=6,label='ordered midpoint products')
ax[1,1].loglog(steps,errs[0]*(steps[0]/steps)**2,'--',color=green,lw=1.5,label='1 / steps² reference slope')
ax[1,1].axhline(d['wrong_integrated_max_bloch_error'],color=orange,lw=2,ls=':',label='single exponential of integral')
ax[1,1].set(xlabel='number of time slices (dimensionless)',ylabel='max final Bloch error',title='D. Closed system: preserve the time order',ylim=(3e-7,.15))
ax[1,1].xaxis.set_minor_formatter(NullFormatter())
ax[1,1].set_xticks(steps,[str(x) for x in steps]);ax[1,1].legend(loc='center right',frameon=False,fontsize=9)
for a in ax.flat:
    a.grid(True,alpha=.18)
    a.spines[['top','right']].set_visible(False)
fig.text(.075,.035,'Same trajectory at different times is correlated; pointwise SE is not a simultaneous confidence band.',fontsize=10,color='#475569')
out=R.parents[1]/'handbook/assets'
for ext in ('svg','png'):
    p=out/f'round73-foundations-dynamics.{ext}'
    fig.savefig(p,dpi=160,metadata={'Creator':'handbook round73 scientific generator'} if ext=='svg' else None)
    if ext=='svg':p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
(R/'round73-figure-provenance.json').write_text(json.dumps({'input':'sdk73/all-results.json','input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'outputs':['handbook/assets/round73-foundations-dynamics.svg','handbook/assets/round73-foundations-dynamics.png'],'kind':'scientific data plot, synthetic CPU SDK experiment'},indent=2)+'\n')
print('figure generated')
