# F71 基础主线的八组展开练习

日期：2026-10-13。题目、逐步答案和限制直接放在八篇对应的主节内，标签为 F71-00–F71-05、F71-Q1–F71-Q2，不变更旧自检编号。新增程序由本书独立编写，只复用本目录原有自编矩阵助手。

Python 3.9 及以上、仅标准库，无硬件、网络或付费服务；全部输入固定，无随机采样，随机种子不适用。矩阵断言容差 `1e-10`，不要加 `-O` 关闭断言。从仓库根目录运行：

```sh
python3 codes/foundations/round71_checks.py --case all
python3 codes/foundations/round71_checks.py --case 03
python3 codes/foundations/round71_checks.py --case all --output /tmp/foundations-round71.json
python3 codes/foundations/generate_round71_eraser.py
```

`--case` 可取 `00 01 02 03 04 05 q1 q2 all`。结果见 [round71-results.json](round71-results.json)；复数存为 `[实部, 虚部]`，原来是实数的值仍为数值。所有模型和计数都是教学计算，不是硬件实验。脚本只做小矩阵及整数内存估算，不会分配 16 EiB 数组。

| 编号 | 题目与答案位置 | 输入与实际检查 |
|---|---|---|
| 00 | [全景 §3](../../00-overview.html#f71-00指数多个振幅怎样变成经典模拟成本) | n=20/30，每复数16byte；态矢量16MiB/16GiB，密度16TiB/16EiB |
| 01 | [数学 §3](../../01-math.html#f71-01换坐标与真正做门怎样分开) | 复Y本征基W；坐标与测量一起变换保持Z均值1，主动门后固定Z均值0 |
| 02 | [单比特 §7](../../02-single-qubit.html#f71-02把前面的非投影概率模型补成一次完整测量) | 原章E0/E1的平方根工具；各支1/2，纯度7/8，重测0条件概率5/8 |
| 03 | [纠缠 §5](../../03-multiple-qubits.html#f71-03从含复系数的态实际构造-schmidt-分解) | C=[[1,i],[0,1]]/√3；两侧偏迹、谱、配对向量和四复振幅重构；熵0.550048bit |
| 04 | [传态 §6](../../04-circuits-protocols.html#f71-04传态要保留联合关联不能只还原一个局部概率表) | RQAB基序，16振幅；Bell/复不等权/乘积输入，四分支全部校正；联合XX揭露测量重制备错误 |
| 05 | [噪声 §5](../../05-noise-channels.html#f71-05两个合法噪声信道交换次序为什么仍不同) | p=1/4、γ=.36；两顺序激发.16/.25；复输入差矩阵pγZ；B阻尼保持A约化态 |
| Q1 | [实验 §2.3](../../quantum-mechanics/01-experiments-states.html#f71-q1量子擦除分组条纹为什么不等于整体条纹恢复) | φ=0、π/3、π/2、π；四联合概率从路径-记录复振幅求得，条件条纹相反，边缘始终1/2 |
| Q2 | [不确定关系 §4](../../quantum-mechanics/02-observables-dynamics.html#f71-q2保留刚才舍去的实部能得到怎样更紧的下界) | π/8实态，X/Z；协方差-.5、两方差乘积.25，加强平方下界.25 |

## 图的公式和可复现性

[generate_round71_eraser.py](generate_round71_eraser.py)按129个均匀相位点连接公式曲线 `(1±cosφ)/2`，第三条为二者等权平均1/2。它输出 [Q1条件条纹图](../../handbook/assets/round71-foundations-eraser.svg)，坐标为rad与无量纲概率。实线/虚线/点线和方形/圆形标记可在黑白图中区分。它没有拟合实验计数；SVG是可复制的独立资源。宽窄屏及截图视觉验收由全书构建报告单独记录，生成成功不等于视觉验收已完成。

## 工程和开源对应范围

来源实际访问日期均为2026-10-13。

- [AerSimulator 0.17.1](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)：稠密数组内存、不同模拟方法。F71-00只是数组成本；稳定子/MPS可利用结构，不能将稠密成本当最优经典下界。
- [Qiskit Kraus API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Kraus)：组合方法 `compose`/`dot`/`front` 的顺序。F71-05给0.16/0.25最小输入，适合移植后检验接口。动态latest文档不能代替固定版本源码。
- [Qiskit Experiments ProcessTomography](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.ProcessTomography.html)：用多个输入和测量设置重建信道，可按经典位条件拟合；默认全过程设置数为4^n·3^n。F71-04关联核验是小规模教学诊断，没有安装或执行其拟合器，也没有宣称低成本完整实机过程认证。
- [IBM参考系统传态推导](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation)、[Preskill测量讲义](https://www.preskill.caltech.edu/ph219/chap3_15.pdf)、[Watrous数学预备](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)：定义与一般论证的来源。受版权保护教材只提供链接，未复制全文。

上述工程入口未在第三方库或硬件运行；自编小规模标准库实验已经运行。第三方源码及许可由 [vendor清单](../vendor/README.md)集中管理。数学有限案例不能替代一般定理证明；真实设备需要另记录制备/测量校准、时间漂移、条件记录和不确定度。
