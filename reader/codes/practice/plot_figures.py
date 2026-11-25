#!/usr/bin/env python3
"""Rebuild scientific SVGs from formulas. Requires matplotlib==3.9.4, numpy==2.0.2."""
import pathlib
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
    fraction=np.linspace(.05,.95,181); multiplier=2.25/fraction+.25/(1-fraction)
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    ax.plot(fraction,multiplier,color='#126b68',lw=2.7,label=r'$N\,Var(\hat E_0)\leq 2.25/r+0.25/(1-r)$')
    ax.scatter([.5,.75],[5,4],s=65,color='#934a22',zorder=3)
    ax.annotate('Equal shots: 5',(.5,5),xytext=(-70,40),textcoords='offset points',arrowprops={'arrowstyle':'-'})
    ax.annotate('3:1 shots: 4',(.75,4),xytext=(-10,70),textcoords='offset points',arrowprops={'arrowstyle':'-'})
    ax.axhline(1,color='#777777',ls='--',label='Single raw estimate: bound = 1')
    ax.set(xlim=(0,1),ylim=(0,15),xlabel='Fraction r of total shots assigned to noise factor 1',ylabel='Worst-case variance bound × total shots N',title='Linear extrapolation amplifies sampling cost')
    ax.grid(alpha=.2); ax.legend(loc='upper center',fontsize=10); save(fig,'lab-zne-allocation')
    print('Generated lab-zne-allocation.svg')
if __name__=='__main__': main()
