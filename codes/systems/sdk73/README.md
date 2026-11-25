# 第73轮系统SDK：双基译码、三能级优化与先兆网络

核验2026-10-13。完整固定发布包实际执行；使用上一轮已完整安装的隔离环境并重新检查依赖及导出锁，新输入和输出全部放本目录，未更改72轮记录。本轮没有QPU、云账户、收费请求或设备波形加载。

## 重建和运行

在具有对应wheel或可构建依赖的平台，用Python3.11创建隔离环境：

```sh
python3.11 -m venv .venv-systems73
.venv-systems73/bin/python -m pip install -r codes/systems/sdk73/requirements-lock.txt
.venv-systems73/bin/python -m pip check
.venv-systems73/bin/python codes/systems/sdk73/qec_grid.py
.venv-systems73/bin/python codes/systems/sdk73/grape_three.py
.venv-systems73/bin/python codes/systems/sdk73/sequence_entanglement.py
.venv-systems73/bin/python codes/systems/sdk73/verify_saved_results.py
.venv-systems73/bin/python codes/systems/sdk73/plot_results.py
python3 codes/systems/round73_checks.py --case all
```

锁包括完整包的声明依赖；安装不代表所有依赖功能及上游所有测试都运行。脚本拒绝`-O`；脚本会写本目录的新结果，重跑时不要把归档计时和历史正文数字当必定相同。Stim的固定种子不能保证跨版本/SIMD逐bit相同，优化和系统调度也可能受平台影响；数学条件与实际样本分别保存。绘图使用Matplotlib矢量文字路径，PNG在本目录，SVG在`handbook/assets/`。

## 三条完整执行路径

| 入口 | 输入/流程 | 验收 | 原始证据 |
|---|---|---|---|
| qec_grid.py | X/Z存储 × d3/5/7 × p.001/.003/.006；全部固定7轮，10000 shots/点；2零噪控制各1000 | DEM建普通/相关两图、相同样本两译码、真实逻辑位判错；1000单shot输出与batch逐个一致 | 20份`.stim`/`.dem`/`.npz`；qec-grid-results.json；qec-run.log |
| grape_three.py | 三维RWA、80槽×.5 ns、±.12 rad/ns每路、目标(-iX)⊕1 | 实际qutip-qtrl受界优化16迭代；SciPy独立全矩阵对照；三维酉/两基输入泄漏；滤波和两参数敏感性扫描 | grape-three-amplitudes.csv、grape-three-results.json |
| sequence_entanglement.py | 920次独立新Timeline；两个真正BK两轮生成链路，全部两段就绪才交换 | 成功先兆两端更新；200us真实SDK Bell测量/消息与修正；205us两端配对；密度矩阵偏迹；510us有限存储过期 | sequence-entanglement-results.json完整事件/矩阵；sequence-run.log；未防护反例及初始错误日志 |

PyMatching普通/相关结果逐shot配对，分开保存救回与改错计数。每率有逐点精确95%区间和36率的Bonferroni同时区间；18个双侧条件配对检验另存，未用好看点代替全网格。所有率都是**七轮完整存储**口径。每点单shot服务纳秒数组包含热身后1000次调用，仅含Python+本地匹配，输入已收齐未来7轮；不是流式、队列或真实反馈。

控制的二维限制矩阵一般不是酉。JSON的`haar_unconditional_target_overlap`对计算输入作均匀平均并保留泄漏分母；不是后选择平均，也不是满三维迹目标g3。1ns滤波按每槽离散递推、只传播到原40ns，未补尾。没有带宽/斜率约束，没有通过事后失谐扫描宣称完成鲁棒优化或DRAG。

## SeQUeNCe版本防护与失败

第一次本书路由器只按非空receiver派发，漏掉BSM广播；第二次未偏迹SDK保留的测量中间位；修正后第三次理想目标断言仍失败。三个原日志分别为`sequence-run-initial.log`、`sequence-run-second.log`、`sequence-run-third.log`。这些是实际失败，不当成通过。

随后独立确认0.8.5的`sequence.components.bsm._eq_psi_plus`密度矩阵分支比较`outer(phi_plus, psi_plus)`，正确应为`outer(psi_plus, psi_plus.conj())`。种子730190原版实际交换先兆成功、标量f=1，却得到Phi−、目标Phi+重叠0，完整保存`sequence-unguarded-counterexample.json`。目标错误不能靠接受“ENTANGLED”来消除。

程序先再次运行未防护反例并断言出现，再在**当前进程**为这一判定加入本书适配：正确密度投影、绝对容差1e−12、rtol=0，ket分支继续原方法。随后完整重建920次Timeline。不会修改已安装包、vendor或历史快照；`installed-source-evidence.json`记录安装文件SHA-256。因此这组密度矩阵运行是“本书防护下通过”，不是上游原版未经修改通过或上游已修复。未来版本必须重新核对，不能无条件继续套此防护。

模型经典通道显式5us延迟，量子传播每端到中点5us；记忆`coherence_time`在本密度路径表示从制备开始的确定性硬截止，没有实现连续T2衰减。交换系数1是理想流程，不包含现实交换效率。普通交换元数据采用f1f2，而对称混合的实际密度矩阵重叠是f1f2+(1−f1)(1−f2)/3；混合输入0.9的13次实际输出全部核对0.813333，元数据0.81另存。单一标量不是密度矩阵的替代物。

## 独立复算

`verify_saved_results.py`不采样或优化，从全部182000条归档检测位重新构建两种匹配器并检查每个预测。`round73_checks.py`只用标准库解NPY/ZIP，核查哈希、全部实际/预测逻辑位、失败与配对计数、1000时长分位数；对三维CSV用缩放平方/49项Taylor指数独立传播，与六个Bloch轴态的二阶设计平均交叉；对920次网络更新与端点矩阵直接复算Bell重叠。有限输入验证不替代理论或安全证明。

上游来源：[PyMatching v2.4.0接口](https://github.com/oscarhiggott/PyMatching/blob/v2.4.0/src/pymatching/matching.py)、[qutip-qtrl指南](https://qutip.readthedocs.io/projects/qutip-qtrl/en/latest/guide/guide-control.html)、[SeQUeNCe v0.8.5 BSM](https://github.com/sequence-toolbox/SeQUeNCe/blob/v0.8.5/sequence/components/bsm.py)、[交换源码](https://github.com/sequence-toolbox/SeQUeNCe/blob/v0.8.5/sequence/entanglement_management/swapping.py)（访问2026-10-13）。本目录自编驱动不重新分发已安装第三方包；上游许可仍适用于其源码，原97份vendor材料不改动。

仍未验证：大码距阈值、拓扑/分布式容错门、泄漏/非Pauli电路级模型、流式译码与真实控制链；DRAG、滤波/鲁棒约束内联合优化、真实脉冲；网络纯化/多跳路由/连续存储噪声/安全证明及客户部署。
