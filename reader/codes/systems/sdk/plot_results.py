"""Generate scientific figures from archived SDK data; no invented fit/threshold.
python codes/systems/sdk/plot_results.py
"""
import json,os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager
if not __debug__: raise RuntimeError('Run without -O')
OUT=Path(__file__).resolve().parent
ASSETS=OUT.parents[2]/'handbook/assets'
font_path=os.environ.get('HANDBOOK_CJK_FONT','/System/Library/Fonts/STHeiti Medium.ttc')
if not Path(font_path).exists(): raise RuntimeError('Set HANDBOOK_CJK_FONT to an installed CJK font file')
fontManager.addfont(font_path)
FONT=FontProperties(fname=font_path)
plt.rcParams.update({'svg.fonttype':'path','font.family':FONT.get_name(),'axes.unicode_minus':False,'font.size':11})

def save(fig,name):
    fig.savefig(ASSETS/f'{name}.svg',bbox_inches='tight')
    svg=ASSETS/f'{name}.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(OUT/f'{name}-preview.png',dpi=140,bbox_inches='tight')
    plt.close(fig)
rows=json.loads((OUT/'stim-matching-results.json').read_text())['cases'][1:]
fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
for row in rows:
    d=row['distance'];estimate=row['p_experiment'];lo,hi=row['exact_binomial_95']
    if estimate:
        ax.errorbar(d,estimate,yerr=[[estimate-lo],[hi-estimate]],fmt='o',color='#145f86',capsize=7,markersize=8)
        ax.annotate(f"{row['failures']}/20,000",(d,hi),xytext=(0,10),textcoords='offset points',ha='center')
    else:
        ax.plot(d,hi,'v',mfc='white',mec='#a14f17',ms=9)
        ax.annotate('',xy=(d,1e-6),xytext=(d,hi*.85),arrowprops=dict(arrowstyle='->',color='#a14f17'))
        ax.annotate('0/20,000：上界标记\n点估计为 0，未画在对数轴',(d,hi),xytext=(-12,15),textcoords='offset points',ha='right',color='#80431c')
ax.set_yscale('log');ax.set_ylim(8e-7,3e-3);ax.set_xticks([3,5,7]);ax.set_xlim(2.5,7.5)
ax.set_xlabel('码距 d（存储轮数也为 d）');ax.set_ylabel('每次完整 X 基存储失败概率 q（无量纲）')
ax.set_title('完整电路级抽样 + MWPM：逐点 95% 精确二项区间',pad=16)
ax.grid(True,which='major',alpha=.25);fig.text(.5,-.035,'合成 Pauli 噪声 p = 0.001；不是每周期错误率，也未拟合阈值。',ha='center',fontsize=11)
save(fig,'round72-systems-qec')
wave=np.loadtxt(OUT/'grape-amplitudes.csv',delimiter=',',skiprows=1)
record=json.loads((OUT/'grape-results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
wave=np.vstack([wave,np.r_[40,wave[-1,1:]]])
t=wave[:,0];axes[0].step(t,wave[:,1],where='post',lw=1.5,label='x 原始',color='#145f86')
axes[0].step(t,wave[:,2],where='post',lw=1.5,label='y 原始',color='#a14f17',linestyle='--')
axes[0].step(t,wave[:,3],where='post',lw=1,label='x 采样滤后',color='#145f86',linestyle=':')
axes[0].step(t,wave[:,4],where='post',lw=1,label='y 采样滤后',color='#a14f17',linestyle='-.')
for y in (-.12,.12):axes[0].axhline(y,color='#777',linestyle='--',lw=.7)
axes[0].set_xlabel('时间 t（ns）');axes[0].set_ylabel('控制角频率 u（rad/ns）');axes[0].set_ylim(-.14,.14);axes[0].set_xlim(0,40)
axes[0].set_title('每通道幅度受界；相邻槽未限制斜率');axes[0].legend(ncols=2,fontsize=10,loc='lower right')
sweep=record['detuning_sweep'];axes[1].plot([x['delta_MHz'] for x in sweep],[x['avg_gate_fidelity'] for x in sweep],marker='o',color='#145f86')
axes[1].axvline(5,color='#777',linestyle='--',lw=1);axes[1].set_xticks([3,4,5,6,7]);axes[1].set_ylim(.975,1.001)
axes[1].set_xlabel('失谐 Δ / (2π)（MHz）');axes[1].set_ylabel('平均门保真度 F_avg（无量纲）');axes[1].set_title('同一波形在不同漂移参数下的敏感性')
for ax in axes:ax.grid(alpha=.2)
fig.suptitle('GRAPE 的高精度目标限于设定模型：40 ns、80 槽、合成数据',fontsize=15)
fig.text(.5,-.04,'右图纵轴放大为 0.975—1.001；两能级无耗散；三能级泄漏另见 Q3。',ha='center',fontsize=11)
save(fig,'round72-systems-control')
