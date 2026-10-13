#!/usr/bin/env python3
"""Plot saved official QuTiP run, not fabricated data. Run in SDK environment."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'sdk/all-results.json').read_text())['cases']['qutip']['result']
t=np.array(r['times_us']);exact=np.array(r['exact_expect'])[0];mc=np.array(r['mcsolve_mean_expect'])[0]
se=np.array(r['empirical_standard_errors'])[0]
me=np.array(r['mesolve_density_matrices'])[:,1,1,0]
fig,axs=plt.subplots(2,1,figsize=(8.6,6.6),sharex=True,gridspec_kw={'height_ratios':[2,1]},layout='constrained')
axs[0].plot(t,exact,'-',color='#17294d',lw=2,label='Analytic ensemble')
axs[0].plot(t,me,'--',color='#be6a24',lw=1.5,label='mesolve')
axs[0].errorbar(t[::4],mc[::4],yerr=se[::4],fmt='s',ms=4,color='#247867',capsize=3,label='mcsolve mean ± 1 SE')
axs[0].set(ylabel='Excited population (dimensionless)',title='4096 trajectories approximate the ensemble state')
axs[0].legend(loc='upper right',fontsize=9)
axs[1].axhline(0,color='#17294d',lw=1)
axs[1].errorbar(t[::2],(mc-exact)[::2],yerr=se[::2],fmt='s-',ms=3,color='#247867',capsize=2)
axs[1].set(xlabel='Time (μs)',ylabel='MC minus analytic\n(dimensionless)')
for ax in axs:ax.grid(alpha=.25)
output=ROOT.parents[1]/'handbook/assets/round72-foundations-trajectories'
fig.savefig(output.with_suffix('.svg'));fig.savefig(output.with_suffix('.png'),dpi=170)
svg=output.with_suffix('.svg')
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
print(output.with_suffix('.svg'))
