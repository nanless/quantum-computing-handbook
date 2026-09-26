#!/usr/bin/env python3
"""Rebuild scientific SVGs from formulas. Requires matplotlib==3.9.4, numpy==2.0.2."""
import csv, pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'handbook/assets'
plt.rcParams.update({'font.size':13,'axes.spines.top':False,'axes.spines.right':False,
    'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white','svg.hashsalt':'quantum-round69'})

def save(fig,name):
    fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',metadata={'Date':None})
    target=OUT/(name+'.svg')
    target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
    plt.close(fig)

def main():
    phase=np.linspace(0,2*np.pi,401); probability=(1+np.cos(phase))/2
    fig,ax=plt.subplots(figsize=(9,4.7),layout='constrained')
    ax.plot(phase/np.pi,probability,color='#126b68',lw=2.8,label=r'$P_0=(1+\cos\phi)/2$')
    ax.scatter([0,2/3,1],[1,.25,0],s=70,facecolor='white',edgecolor='#934a22',zorder=4)
    for x,y,text in [(0,1,'0 deg: P = 1'),(2/3,.25,'120 deg: P = 1/4'),(1,0,'180 deg: P = 0')]:
        ax.annotate(text,(x,y),xytext=(15,15),textcoords='offset points',fontsize=12)
    ax.set(xlim=(-.04,2.04),ylim=(-.06,1.18),xlabel=r'Relative phase $\phi/\pi$ (dimensionless)',ylabel='Output probability (dimensionless)',title='Relative phase changes the interference output')
    ax.grid(alpha=.2); ax.legend(loc='upper right'); save(fig,'lab-phase-audio')
    t=np.linspace(0,4,801); ideal=(1+np.cos(2*np.pi*t))/2; decay=(1+np.exp(-t/1.5)*np.cos(2*np.pi*t))/2
    fig,axes=plt.subplots(2,1,figsize=(9,6.5),sharex=True,layout='constrained')
    for ax,y,label,style in [(axes[0],ideal,'Ideal: V = 1','-'),(axes[1],decay,'Decay: V = exp(-t / 1.5 s)','--')]:
        ax.plot(t,y,style,color='#126b68',lw=2.5,label=label)
        ax.axhline(.5,color='#777777',ls=':',lw=1.2); ax.set(ylim=(-.08,1.08),ylabel='Probability'); ax.legend(loc='upper right',fontsize=11); ax.grid(alpha=.2)
    axes[0].set_title('Teaching-time Ramsey signal: loss of contrast, not loss of all sound')
    axes[1].set_xlabel('Teaching time t (s); not laboratory time')
    save(fig,'lab-ramsey-audio')
    with (pathlib.Path(__file__).with_name('figure-data.csv')).open('w',newline='') as f:
        writer=csv.writer(f, lineterminator='\n'); writer.writerow(['teaching_time_s','ideal_probability','decaying_probability'])
        writer.writerows(zip(t,ideal,decay))
    fraction=np.linspace(.05,.95,181); multiplier=2.25/fraction+.25/(1-fraction)
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    ax.plot(fraction,multiplier,color='#126b68',lw=2.7,label=r'$N\,Var(\hat E_0)\leq 2.25/r+0.25/(1-r)$')
    ax.scatter([.5,.75],[5,4],s=65,color='#934a22',zorder=3)
    ax.annotate('Equal shots: 5',(.5,5),xytext=(-70,40),textcoords='offset points',arrowprops={'arrowstyle':'-'})
    ax.annotate('3:1 shots: 4',(.75,4),xytext=(-10,70),textcoords='offset points',arrowprops={'arrowstyle':'-'})
    ax.axhline(1,color='#777777',ls='--',label='Single raw estimate: bound = 1')
    ax.set(xlim=(0,1),ylim=(0,15),xlabel='Fraction r of total shots assigned to noise factor 1',ylabel='Worst-case variance bound × total shots N',title='Linear extrapolation amplifies sampling cost')
    ax.grid(alpha=.2); ax.legend(loc='upper center',fontsize=10); save(fig,'lab-zne-allocation')
    print('Generated 3 SVG figures and figure-data.csv')
if __name__=='__main__': main()
