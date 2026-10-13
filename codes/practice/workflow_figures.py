#!/usr/bin/env python3
"""Plot analytic MSE upper bounds; no simulated or measured shot counts.

Requires the pinned matplotlib/NumPy in requirements-figures.txt.
Run workflow_checks.py first. Standard-library numerical checks run separately.
"""
import json
import pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
root = HERE.parents[1]
assets = root / 'handbook/assets'
if not assets.exists():
    assets = root / 'assets'
data = json.loads((HERE / 'workflow-results.json').read_text())['MPF']
model = data['ideal_hamiltonian']
deeper_bias = abs(model['individual'][-1] - model['target'])
mpf_bias = abs(model['combined'] - model['target'])
shots = np.logspace(2, 7, 160)
plt.rcParams.update({'svg.fonttype': 'none', 'svg.hashsalt': 'quantum-round71-mpf',
                    'font.family': 'DejaVu Sans', 'font.size': 11})
fig, ax = plt.subplots(figsize=(8.6, 4.8), layout='constrained')
ax.loglog(shots, deeper_bias**2 + 1/shots, '-', color='#186f75', linewidth=2,
          label='4-step circuit: bias² + 1/N')
ax.loglog(shots, mpf_bias**2 + data['gamma']**2/shots, '--', color='#ab542a', linewidth=2,
          label='MPF (2,4): bias² + (5/3)²/N')
ax.set(xlabel='Total independent shots N (equal cost per shot)',
       ylabel='MSE upper bound (dimensionless squared)',
       title='Smaller ideal bias can require more shots')
ax.grid(True, which='both', alpha=0.22)
ax.legend(loc='lower left', framealpha=1)
fig.savefig(assets / 'workflow-mpf-budget.svg', metadata={'Date': None})
plt.close(fig)
figure = assets / 'workflow-mpf-budget.svg'
figure.write_text('\n'.join(line.rstrip() for line in figure.read_text().splitlines()) + '\n')
print('Generated workflow-mpf-budget.svg from workflow-results.json')
