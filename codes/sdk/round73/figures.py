#!/usr/bin/env python3
"""Scientific plots from saved actual SDK results; SVG text is kept inspectable."""
import json,pathlib,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((HERE/(n+'-results.json')).read_text())
plt.rcParams.update({'svg.fonttype':'none','font.size':11})
fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
d=load('dynamic-mpf');ax=axs[0,0];ts=[r['time'] for r in d['records']]
ax.semilogy(ts,[r['references'][-1]['best_single_error'] for r in d['records']], 'o-',label='single S2, k=4')
ax.semilogy(ts,[r['references'][-1]['frobenius_error'] for r in d['records']], 's-',label='dynamic MPF, dt_ref=.025')
ax.set(title='A  Actual four-site Frobenius error',xlabel='Dimensionless time',ylabel='Frobenius norm');ax.legend();ax.grid(alpha=.2)
s=load('slc');ax=axs[0,1];x=[r['bias_tolerance'] for r in s['records']]
ax.plot(x,[r['bias_bound'] for r in s['records']],'o-',label='SLC deterministic bound')
ax.plot(x,[r['observed_bias'] for r in s['records']],'s-',label='dense residual-model bias')
ax.set(title='B  Shaded selection: bound versus bias',xlabel='Allowed bias',ylabel='Absolute expectation bias');ax.legend();ax.grid(alpha=.2)
p=load('pna');ax=axs[1,0];labels=['Noisy','PNA exact','PNA sampled','Wrong rates'];values=[p['noisy'],p['mitigated'],p['finite_shot']['estimate'],p['miscalibrated_value']]
ax.errorbar(range(4),values,yerr=[0,0,1.96*p['finite_shot']['standard_error'],0],fmt='o',capsize=5,label='sample: 1.96 SE, normal approximation')
ax.axhline(p['ideal'],ls='--',c='black',label='ideal');ax.set_xticks(range(4),labels);ax.set(title='C  PNA: finite shots and model mismatch',ylabel='XX expectation');ax.legend(fontsize=9);ax.grid(alpha=.2)
g=load('gst-long');ax=axs[1,1];errors=[r['error'] for r in g['unseen_predictions']]
ax.scatter([r['length'] for r in g['unseen_predictions']],errors,s=35);ax.set(title='D  GST predictions on unseen circuits',xlabel='Gate count',ylabel='Absolute population probability error');ax.set_xticks([17,23,31]);ax.grid(alpha=.2)
asset=ROOT/'handbook/assets/round73-workflows.svg';fig.savefig(asset);asset.write_text('\n'.join(line.rstrip() for line in asset.read_text().splitlines())+'\n')
(ROOT/'work/rendered').mkdir(parents=True,exist_ok=True);fig.savefig(ROOT/'work/rendered/round73-workflows-source.png',dpi=140)

(HERE/'figure-provenance.json').write_text(json.dumps({'inputs':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['dynamic-mpf-results.json','slc-results.json','pna-results.json','gst-long-results.json']},'generator_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'svg_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'scope':'saved actual SDK data; SVG produced by scientific plotting, not external raster generation'},indent=2)+'\n')
