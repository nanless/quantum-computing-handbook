#!/usr/bin/env python3
"""Two formula-derived figures, SVG delivery and PNG visual review.

Requires matplotlib; no external data and no sampled hardware results.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from round70_checks import amp_prob, chain_energies

ROOT=Path(__file__).resolve().parents[2]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none',
                     'svg.hashsalt':'round70-algorithms'})
OUT=ROOT/'handbook/assets'
PREVIEW=ROOT/'work/rendered'
PREVIEW.mkdir(exist_ok=True,parents=True)

def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),metadata={'Date':None},bbox_inches='tight',pad_inches=.2)
    path=OUT/(name+'.svg')
    path.write_text('\n'.join(x.rstrip() for x in path.read_text().splitlines())+'\n')
    fig.savefig(PREVIEW/(name+'.png'),dpi=150,bbox_inches='tight',pad_inches=.2)
    plt.close(fig)
    print(path)

def style(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.grid(alpha=.2)

fig,ax=plt.subplots(figsize=(8.2,5.3),layout='constrained')
xs=[i/800 for i in range(801)]
ax.plot(xs,xs,color='#00796b',lw=2,label='k = 0: direct sampling')
ax.plot(xs,[amp_prob(a,1) for a in xs],color='#b45309',ls='--',lw=2,label='k = 1: one Grover iteration')
ax.plot([.25,1],[1,1],'s',color='#b45309',markersize=7)
ax.annotate('Same p = 1 at a = 1/4 and a = 1',xy=(.25,1),xytext=(.13,1.105),
            fontsize=10,arrowprops={'arrowstyle':'->','color':'#475569'})
ax.set(xlim=(0,1.03),ylim=(-.02,1.20),xlabel='Initial good-state probability a (dimensionless)',
       ylabel='Measured success probability p (dimensionless)',title='A single Grover depth cannot identify every amplitude')
ax.set_yticks([0,.25,.5,.75,1])
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.18),ncol=2,framealpha=.95,fontsize=10)
style(ax)
save(fig,'round70-amplitude-aliasing')

fig,axes=plt.subplots(1,2,figsize=(11.5,4.7),layout='constrained')
a,b=axes
js=[i/100 for i in range(801)]
a.plot(js,[-j for j in js],color='#00796b',lw=2,label='Aligned: (+,+) or (-,-)')
a.plot(js,[j-4 for j in js],color='#b45309',lw=2,ls='--',label='Broken: (+,-)')
a.plot(js,[j+4 for j in js],color='#475569',lw=1.6,ls=':',label='Broken: (-,+)')
a.axvline(2,color='#334155',ls=':',lw=1)
a.plot([2],[-2],'o',color='#111827')
a.set(xlabel='Chain strength J (model units)',ylabel='Energy E (model units)',
      title='A. All ground states aligned only for J > 2')
a.legend(fontsize=9,loc='upper left')
b.plot(js,[2/max(2,j) for j in js],color='#3157a4',lw=2)
b.plot([3,8],[2/3,1/4],'s',color='#3157a4')
b.annotate('J=3: field 2/3',xy=(3,2/3),xytext=(3.3,.82),fontsize=10,
           arrowprops={'arrowstyle':'->'})
b.annotate('J=8: field 1/4',xy=(8,.25),xytext=(4.8,.4),fontsize=10,
           arrowprops={'arrowstyle':'->'})
b.set(xlabel='Chain strength J (model units)',ylabel='Field amplitude after scaling (dimensionless)',
      title='B. Scaling all coefficients to [-1, 1]',ylim=(0,1.13))
for ax in axes: style(ax)
fig.suptitle('Two-spin teaching model: E = -2sa + 2sb - J sa sb',fontsize=14)
save(fig,'round70-chain-strength')
