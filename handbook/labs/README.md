# 实验、练习、代码与声音

这里把全书 24 篇正文连接到可运行的小实验。先读题目、写预测，再运行程序；每题都有计算过程、答案和模型边界。既有的 [251 道自检及答案](../appendices/exercises.md)保持原编号，新增实验使用独立标签。

## 怎样开始

1. 零基础从[基础实验册](foundations.md)的 F00、F01、F02 开始。
2. 算法读者先做[QPE 与 Grover](algorithms.md)，再比较变分、QSVT 和容量。
3. 工程读者使用[系统实验册](systems.md)，逐层连接标签、译码、资源、网络、映射与服务可用率。
4. 用[统计实验](practice.md)检查结论是否受 shots、外推和多重比较影响。
5. 用[声音实验](audio.md)听相位和对比度的教学映射，并回到公式核对。声音是程序合成，不是真实设备录音。

## 逐章实验映射

| 章 | 可核对的问题 | 实验册 |
|---|---|---|
| 00 | 1000 次测量为何不必恰好一半 | [F00](foundations.md) |
| 01 | 复共轭、内积和换基 | [F01](foundations.md) |
| 02 | Y 基测量门序与相位 | [F02](foundations.md) |
| 03 | 非均匀纠缠态偏迹与远端旋转 | [F03](foundations.md) |
| 04 | 传态四个分支及复振幅修正 | [F04](foundations.md) |
| 05 | 阻尼、退相位与 T1/T2 | [F05](foundations.md) |
| 06 | 相位估计的模 1 网格误差 | [06-A](algorithms.md) |
| 07 | Grover 过度旋转与重复查询账 | [07-A](algorithms.md) |
| 08 | Pauli 分组预算、QAOA 输出分布 | [08-A](algorithms.md) |
| 09 | 稀有丢失事件中的告警可信度 | [S09](systems.md) |
| 10 | 非均匀独立噪声下的加权译码 | [S10](systems.md) |
| 11 | 魔法态供给与突发消费 | [S11](systems.md) |
| 12 | 两条快慢不同链路的等待 | [S12](systems.md) |
| 13 | 不等先验的 Helstrom 判别 | [F13](foundations.md) |
| 14 | 输出映射与线路等价 | [S14](systems.md) |
| 15 | 不等shots、外推、多重比较、后选择、零失败、时间预算、切割 | [P15-A–G](practice.md) |
| 16 | 非厄米矩阵的 QSVT 反例 | [16-A](algorithms.md) |
| 17 | MBQC 分支与重试失败预算 | [17-A](algorithms.md) |
| 18 | 擦除信道降解映射及熵 | [18-A](algorithms.md) |
| 19 | 故障区间并集、可用率与合格服务吞吐 | [S19](systems.md) |
| Q1 | 环境重叠的模与相位 | [FQ1](foundations.md) |
| Q2 | 时序和子系统能量零点 | [FQ2](foundations.md) |
| Q3 | 热占据、角频率和失谐 | [FQ3](foundations.md) |
| Q4 | 连续态离散化归一化及收敛 | [FQ4](foundations.md) |

章节实验覆盖并不表示每个研究算法都有完整生产实现。实现深度与尚未覆盖的主题见[算法、工业实践与开源对照](../appendices/software-practice.md)。

## 运行方式与结果

本轮自编数值实验使用 Python 3.9 及以上的标准库；不用账户、不调用云服务。不要加 `-O` 关闭断言。绘图程序另需指定版本的 matplotlib 和 NumPy；不重画图就无需安装它们。

```sh
python3 codes/run_all.py
```

在**仓库根目录**运行上面的统一入口；分章运行见[代码说明](../../codes/README.md)。检查项覆盖概率/态归一化、独立解析式、四个测量分支、资源边界、位序、离散化收敛、源码哈希与音频格式。数值通过意味着本模型在检查点一致，不是对全部物理公设、定理和工业优势的证明。

## 如何把练习改成自己的研究

一次只改变一个因素：先把初态换成含非零复相位的态，再改变噪声，再增加系统大小。记录何时解析断言仍成立、何时已越出模型条件。失败例子比只贴一张漂亮成功图更有价值。

真实硬件实验还需要软件锁定、编译与校准快照、原始计数、时间顺序和费用预算。第三方源码清单支持代码溯源，没有替读者完成这些设备实验。

## 第二组逐章练习：检验容易遗漏的条件

本组题目和完整解答直接放在相应正文的“新增诊断练习”“实操扩展B”或“练习与实验”中；不必在两个文档间来回找答案。原251道自检与上表第一组实验继续保留。全部新数值程序已接入统一入口，输入是合成计数或明示模型。

| 章节入口 | 新练习要回答的问题 | 程序 |
|---|---|---|
| [00](../00-overview.md) | 重复复制的日志为何不能算独立shots | [基础诊断00](../../codes/foundations/diagnostic_lab.py) |
| [01](../01-math.md) | 两列归一化为何还不保证酉性 | [基础诊断01](../../codes/foundations/diagnostic_lab.py) |
| [02](../02-single-qubit.md) | 合法计数为何重构出负本征值 | [基础诊断02](../../codes/foundations/diagnostic_lab.py) |
| [03](../03-multiple-qubits.md) | 复相位纠缠应测哪个相关方向 | [基础诊断03](../../codes/foundations/diagnostic_lab.py) |
| [04](../04-circuits-protocols.md) | 门的全局相位加控制后为何不能删 | [基础诊断04](../../codes/foundations/diagnostic_lab.py) |
| [05](../05-noise-channels.md) | 有限温度阻尼为何也能激发基态 | [基础诊断05](../../codes/foundations/diagnostic_lab.py) |
| [06](../06-algorithmic-primitives.md) | Hadamard测试如何读复期望值的实部和虚部 | [算法检查06](../../codes/algorithms/round70_checks.py) |
| [07](../07-algorithms.md) | 单个Grover深度为什么分不清不同振幅 | [算法检查07](../../codes/algorithms/round70_checks.py) |
| [08](../08-applications.md) | 多个门共享参数时如何正确求导 | [算法检查08](../../codes/algorithms/round70_checks.py) |
| [09](../09-hardware.md) | 如何把有限标定样本的不确定性一起算 | [标定传播](../../codes/systems/calibration_uncertainty.py) |
| [10](../10-error-correction.md) | 综合征测后为何仍有相干逻辑误差 | [相干重复码](../../codes/systems/coherent_repetition.py) |
| [11](../11-resources-benchmarks.md) | 批内漂移怎样减少有效独立信息 | [相关shots](../../codes/systems/correlated_shots.py) |
| [12](../12-security-network-frontiers.md) | 存储超时怎样交换速率与条件质量 | [网络超时](../../codes/systems/network_cutoff.py) |
| [13](../13-quantum-information.md) | 后选择为何不违反迹距离收缩定理 | [基础诊断13](../../codes/foundations/diagnostic_lab.py) |
| [14](../14-compilation-control.md) | 不共用比特的门为何还不能并行 | [共享资源调度](../../codes/systems/resource_schedule.py) |
| [15](../15-practice-research.md) | 后选择、零失败、时间预算、负权重怎样报告 | [P15-D–G](../../codes/practice/research_checks.py) |
| [16](../16-advanced-algorithms-verification.md) | 小成功率为何放大条件态误差 | [算法检查16](../../codes/algorithms/round70_checks.py) |
| [17](../17-computation-models.md) | 链强度阈值为何有简并和缩放代价 | [算法检查17](../../codes/algorithms/round70_checks.py) |
| [18](../18-channels-capacities-complexity.md) | 有限块码可靠性为何不能等同信道容量 | [算法检查18](../../codes/algorithms/round70_checks.py) |
| [19](../19-engineering-architecture.md) | 校准更新怎样传播失效和拒绝过期发布 | [校准依赖](../../codes/systems/calibration_dependencies.py) |
| [Q1](../quantum-mechanics/01-experiments-states.md) | 相同可见度能否区分不等权与退相干 | [基础诊断q1](../../codes/foundations/diagnostic_lab.py) |
| [Q2](../quantum-mechanics/02-observables-dynamics.md) | 同一简并读数能否来自不同测后作用 | [基础诊断q2](../../codes/foundations/diagnostic_lab.py) |
| [Q3](../quantum-mechanics/03-levels-control.md) | Rabi人口能否辨认失谐符号 | [基础诊断q3](../../codes/foundations/diagnostic_lab.py) |
| [Q4](../quantum-mechanics/04-wavefunctions-models.md) | Fock截断如何改变对易子 | [基础诊断q4](../../codes/foundations/diagnostic_lab.py) |

此外，[源码阅读练习S04–S08](../appendices/software-practice.md)把多项式基、LCU归一化、阴影快照、控制约束和重构顺序连接到固定的上游文件。四组数值题有[独立复算代码](../../codes/practice/source_reading_checks.py)，工程讨论题保留其无法单靠程序断言验收的边界。
