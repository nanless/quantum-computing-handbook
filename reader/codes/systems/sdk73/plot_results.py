"""Recreate scientific figures from round73 raw-result tables; all labels have units."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
if not __debug__: raise RuntimeError('Validation requires assertions; do not run with -O')
HERE=Path(__file__).resolve().parent; ASSETS=HERE.parents[2]/'handbook'/'assets'
# HERE parents: systems, codes, repository
ASSETS=HERE.parents[2]/'handbook'/'assets'
plt.rcParams.update({'font.size':10,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False})
d=json.loads((HERE/'qec-grid-results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,4.5),sharey=True,constrained_layout=True)
for ax,b in zip(axes,('x','z')):
    for di,dist in enumerate((3,5,7)):
        rows=sorted([r for r in d['cases'] if r['basis']==b and r['distance']==dist],key=lambda r:r['noise_each'])
        for dec,marker,ls,offset in [('ordinary','o','-',-.00004),('correlated','s','--',.00004)]:
            x=[r['noise_each']+offset for r in rows]; y=np.array([r[dec+'_failures']/r['shots'] for r in rows]);
            lo=np.array([r[dec+'_simultaneous_ci'][0] for r in rows]); hi=np.array([r[dec+'_simultaneous_ci'][1] for r in rows])
            ax.errorbar(x,y,yerr=[y-lo,hi-y],label=f'd={dist}, {dec}',marker=(('o','^','D') if dec=='ordinary' else ('s','v','x'))[di],linestyle=ls,color=f'C{di}',capsize=3,lw=1.3,markersize=4)
    ax.set_title(f'{b.upper()}-basis memory, 7 rounds');ax.set_xlabel('Pauli / flip parameter p (dimensionless)');ax.set_ylim(-.003,.075);ax.grid(alpha=.2);ax.legend(fontsize=8,ncol=2)
axes[0].set_ylabel('Failures / complete memory shot (dimensionless)')
fig.suptitle('Same raw shots, two decoders; 10,000 shots / point\nError bars: simultaneous coverage >= 95% for 36 rates (Bonferroni)',fontsize=12)
fig.savefig(ASSETS/'round73-systems-qec.svg');fig.savefig(HERE/'round73-systems-qec-preview.png',dpi=150);plt.close(fig)

d=json.loads((HERE/'grape-three-results.json').read_text()); amps=np.loadtxt(HERE/'grape-three-amplitudes.csv',delimiter=',',skiprows=1)
fig,axes=plt.subplots(1,2,figsize=(11,5.3),constrained_layout=True)
for col,label,ls in [(1,'optimized x','-'),(2,'optimized y','--'),(3,'filtered x',':'),(4,'filtered y','-.')]:axes[0].step(np.r_[amps[:,0],40.0],np.r_[amps[:,col],amps[-1,col]],where='post',label=label,ls=ls)
axes[0].set_xlabel('Time (ns)');axes[0].set_ylabel('Angular-frequency envelope (rad/ns)');axes[0].set_title('3-level target, 80 slots, independent box bounds');axes[0].legend(fontsize=8,ncol=2,loc='upper center',bbox_to_anchor=(.5,-.18));axes[0].grid(alpha=.2)
xs=np.arange(3); labels=['2-level design\nin 3 levels','3-level design','3-level design\n1 ns sampled filter']
for j in (0,1):
    heights=[d['previous_two_level_waveform']['basis_leakage'][j],d['optimized']['basis_leakage'][j],d['one_ns_discrete_filter']['basis_leakage'][j]]
    axes[1].bar(xs+(j-.5)*.3,heights,width=.3,label=f'input |{j}>',hatch='' if j==0 else '//',edgecolor='black',alpha=.8)
axes[1].set_yscale('log');axes[1].set_ylabel('Final level-2 population (dimensionless)');axes[1].set_xticks(xs,labels);axes[1].legend();axes[1].set_title('Leakage suppression depends on the model');axes[1].grid(axis='y',alpha=.2)
fig.suptitle('40 ns synthetic three-level RWA; detuning +5 MHz, anharmonicity -200 MHz\nNo bandwidth constraint and no hardware waveform loading',fontsize=12)
fig.savefig(ASSETS/'round73-systems-control.svg');fig.savefig(HERE/'round73-systems-control-preview.png',dpi=150);plt.close(fig)
for name in ('round73-systems-qec.svg','round73-systems-control.svg'):
    svg=ASSETS/name
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
print('Two SVG and two PNG previews generated from archived outputs')
