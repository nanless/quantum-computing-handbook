#!/usr/bin/env python3
"""Rebuild the scientific figure. Requires matplotlib; experiments need only stdlib."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from experiments import grover, qpe

ROOT = Path(__file__).resolve().parents[2]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'svg.fonttype': 'none', 'svg.hashsalt': 'algorithms-round69'})
fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.7), layout='constrained')
fig.suptitle('Grover overshoot and phase-estimation wraparound', fontsize=17)
for ax in axes:
    ax.set_ylim(-0.02, 1.06)
    ax.set_ylabel('Probability (dimensionless)')
    ax.set_yticks([0, .25, .5, .75, 1])
    ax.grid(axis='y', alpha=.3)
    ax.spines[['top', 'right']].set_visible(False)
a, b = axes
a.plot(range(5), grover(16, {5}, 4), 'o-', color='#006d77', linewidth=2,
       label='1 target: circles')
a.plot(range(5), grover(16, {0, 3, 8, 15}, 4), 's--', color='#ba4a00', linewidth=2,
       label='4 targets: squares')
a.set_title('A. N = 16 candidates', loc='left')
a.set_xlabel('Grover iterations k (integer)')
a.set_xticks(range(5))
a.legend(loc='lower right', framealpha=.94)
b.bar(range(16), qpe(63/64, 4), color='#3157a4', width=.7)
b.set_title('B. True phase = 63/64; t = 4', loc='left')
b.set_xlabel('QPE output y (phase estimate = y / 16)')
b.set_xticks([0, 3, 6, 9, 12, 15])
b.annotate('P(y = 0) = 0.8112\nCircular error = 1/64', xy=(0, .81122),
           xytext=(3, .78), arrowprops={'arrowstyle':'->', 'color':'#334e68'},
           fontsize=11)
fig.savefig(ROOT/'handbook/assets/algorithm-lab-checks.svg', metadata={'Date':None}, bbox_inches='tight', pad_inches=0.22)
svg=ROOT/'handbook/assets/algorithm-lab-checks.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
preview=ROOT/'work/rendered/algorithm-lab-checks-preview.png'
preview.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(preview, dpi=150, bbox_inches='tight', pad_inches=0.22)
plt.close(fig)
print('handbook/assets/algorithm-lab-checks.svg')
