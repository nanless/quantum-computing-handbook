#!/usr/bin/env python3
"""Formula-driven plots for P15-E/G; optional locked matplotlib/numpy environment."""
import math
import pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research_checks import zero_failure_upper
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT/'handbook/assets'
plt.rcParams.update({'font.size': 12, 'axes.spines.top': False,
    'axes.spines.right': False, 'svg.fonttype': 'none',
    'svg.hashsalt': 'round70-research', 'figure.facecolor': 'white'})

def save(fig, name):
    p = OUT/name
    fig.savefig(p, bbox_inches='tight', metadata={'Date': None})
    p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines())+'\n')
    plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5), layout='constrained')
ns = list(range(100, 10001, 25))
ax.plot(ns, [zero_failure_upper(n) for n in ns], color='#176b64', lw=2.5,
        label='Exact one-sided 95% upper bound after zero failures')
ax.axhline(.001, ls='--', color='#944528', label='Target failure probability: 0.001')
ax.scatter([1000, 2995], [zero_failure_upper(1000), zero_failure_upper(2995)],
           s=55, color='#944528', zorder=3)
ax.annotate('N = 1000: 0.00299125', (1000, zero_failure_upper(1000)),
            xytext=(30, 28), textcoords='offset points', arrowprops={'arrowstyle':'-'})
ax.annotate('N = 2995: below 0.001', (2995, zero_failure_upper(2995)),
            xytext=(30, 33), textcoords='offset points', arrowprops={'arrowstyle':'-'})
ax.set(xscale='log', yscale='log', xlabel='Pre-specified number of trials N (log scale)',
       ylabel='Failure probability upper bound (log scale)',
       title='Zero observed failures still leave uncertainty')
ax.grid(alpha=.2, which='both'); ax.legend(loc='upper right', fontsize=9)
save(fig, 'lab-zero-failure.svg')

fig, ax = plt.subplots(figsize=(9, 4.7), layout='constrained')
ks = list(range(5)); bounds = [9**k for k in ks]
ax.plot(ks, bounds, '-o', color='#176b64', lw=2.5,
        label='Independent single-gate product decomposition')
for k, val in zip(ks, bounds):
    ax.annotate(str(val), (k, val), xytext=(0, 10), textcoords='offset points', ha='center')
ax.set(xticks=ks, yscale='log', ylim=(.6, 30000),
       xlabel='Number of independently cut CNOT/CZ gates k',
       ylabel='Worst-case variance coefficient (log scale)',
       title='A product decomposition has coefficient 9^k')
ax.grid(alpha=.2); ax.legend(loc='upper left', fontsize=10)
fig.text(.5, -.015, 'Not a universal lower bound: joint decompositions can change the cost.',
         ha='center', fontsize=10)
save(fig, 'lab-cutting-overhead.svg')
print('Generated lab-zero-failure.svg and lab-cutting-overhead.svg')
