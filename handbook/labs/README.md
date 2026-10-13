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

## 第四组逐章练习：完整SDK与独立复算

本轮在24篇正文就地补充F72/A72/S72练习，原题编号保持。完整版本、任务、原始样本、六组集成流程练习与限定范围见[完整SDK实验册](sdk-validation.md)。SDK安装和运行需各组隔离环境；默认标准库入口只做教学实验及保存结果的独立重算。

| 篇章 | 新标签与重点 | 代码入口 |
|---|---|---|
| [00](../00-overview.md) | F72-00：模拟表示与相同实验 | [运行与结果](../../codes/foundations/round72-README.md) |
| [01](../01-math.md) | F72-01：矩阵指数前置 | [运行与结果](../../codes/foundations/round72-README.md) |
| [02](../02-single-qubit.md) | F72-02：原计数/线性逆/PSD | [运行与结果](../../codes/foundations/round72-README.md) |
| [03](../03-multiple-qubits.md) | F72-03：局部阻尼与纠缠 | [运行与结果](../../codes/foundations/round72-README.md) |
| [04](../04-circuits-protocols.md) | F72-04：缺少反馈的传态 | [运行与结果](../../codes/foundations/round72-README.md) |
| [05](../05-noise-channels.md) | F72-05：CP与TP分开检查 | [运行与结果](../../codes/foundations/round72-README.md) |
| [Q1](../quantum-mechanics/01-experiments-states.md) | F72-Q1：不等探测效率 | [运行与结果](../../codes/foundations/round72-README.md) |
| [Q2](../quantum-mechanics/02-observables-dynamics.md) | F72-Q2：主方程与随机轨迹 | [运行与结果](../../codes/foundations/round72-README.md) |
| [06](../06-algorithmic-primitives.md) | A72-06：可逆oracle及承诺 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [07](../07-algorithms.md) | A72-07：完整非对角HHL | [运行与结果](../../codes/algorithms/round72-README.md) |
| [08](../08-applications.md) | A72-08：费米子映射与粒子数 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [13](../13-quantum-information.md) | A72-13：非线性插件偏差 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [16](../16-advanced-algorithms-verification.md) | A72-16：一般图行走/QSP/两位阴影 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [17](../17-computation-models.md) | A72-17：QUBO与自旋符号 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [18](../18-channels-capacities-complexity.md) | A72-18：Gaussian光子概率 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [Q4](../quantum-mechanics/04-wavefunctions-models.md) | A72-Q4：Fock截止与无限尾界 | [运行与结果](../../codes/algorithms/round72-README.md) |
| [09](../09-hardware.md) | S72-09：噪声参数换算 | [运行与结果](../../codes/systems/round72-README.md) |
| [10](../10-error-correction.md) | S72-10：电路级纠错与原样本 | [运行与结果](../../codes/systems/round72-README.md) |
| [11](../11-resources-benchmarks.md) | S72-11：失败区间/时间分母 | [运行与结果](../../codes/systems/round72-README.md) |
| [12](../12-security-network-frontiers.md) | S72-12：ML-KEM/网络时间轴 | [运行与结果](../../codes/systems/round72-README.md) |
| [14](../14-compilation-control.md) | S72-14：受约束GRAPE及梯度 | [运行与结果](../../codes/systems/round72-README.md) |
| [15](../15-practice-research.md) | S72-15：归档独立重建 | [运行与结果](../../codes/systems/round72-README.md) |
| [19](../19-engineering-architecture.md) | S72-19：反馈队列与截止 | [运行与结果](../../codes/systems/round72-README.md) |
| [Q3](../quantum-mechanics/03-levels-control.md) | S72-Q3：三能级泄漏/过滤 | [运行与结果](../../codes/systems/round72-README.md) |

上表的A72-16包含a/b/c三项独立练习；完整集成实验册另有R72-IAE、OBP、CUT、MPF、GST、HPC六组计算和实际SDK代码。全部样本为本地模拟或明示模型；没有新采集真机数据。

## 第三组逐章练习：从解释断点到独立核算

这组题于2026-10-13加入，分别嵌在每篇相关小节中，答案紧邻问题，不替换原题编号。每篇有独立标签，均有实际可运行的标准库核算；同一程序负责多篇时用章节参数选择。正文先给一般定义、条件或证明，程序再用固定小输入从独立路径核对。

| 章节与标签 | 分步练习及解释重点 | 核算程序 |
|---|---|---|
| [00：F71-00](../00-overview.md) | 振幅数组与密度矩阵的实际字节数；表示成本与模拟困难区别 | [基础](../../codes/foundations/round71_checks.py) `--case 00` |
| [01：F71-01](../01-math.md) | 含复数的换基；坐标变化与主动门分开计算 | [基础](../../codes/foundations/round71_checks.py) `--case 01` |
| [02：F71-02](../02-single-qubit.md) | 非投影POVM的平方根工具、每支后态和非选择态 | [基础](../../codes/foundations/round71_checks.py) `--case 02` |
| [03：F71-03](../03-multiple-qubits.md) | 从复系数四项态构造两侧Schmidt向量并逐格还原 | [基础](../../codes/foundations/round71_checks.py) `--case 03` |
| [04：F71-04](../04-circuits-protocols.md) | 与参考位纠缠的输入传态，四分支与联合关联 | [基础](../../codes/foundations/round71_checks.py) `--case 04` |
| [05：F71-05](../05-noise-channels.md) | 合法噪声不交换；局域保迹与无信号的一般证明 | [基础](../../codes/foundations/round71_checks.py) `--case 05` |
| [06：A71-06](../06-algorithmic-primitives.md) | 垃圾态内积怎样压低干涉；复位为何不等于反计算 | [算法](../../codes/algorithms/round71_checks.py) `06` |
| [07：A71-07](../07-algorithms.md) | Simon固定采样预算的满秩概率和失败上界 | [算法](../../codes/algorithms/round71_checks.py) `07` |
| [08：A71-08](../08-applications.md) | 共测的协方差、配对原始计数和总制备预算 | [算法](../../codes/algorithms/round71_checks.py) `08` |
| [09：S71-09](../09-hardware.md) | 有限温度的被动复位底限、初态与速率方程 | [系统](../../codes/systems/round71_checks.py) `--case 09` |
| [10：S71-10](../10-error-correction.md) | 未知错误加已知擦除的距离条件及边界反例 | [系统](../../codes/systems/round71_checks.py) `--case 10` |
| [11：S71-11](../11-resources-benchmarks.md) | 每周期概率、最终奇偶翻转与至少一次事件区别 | [系统](../../codes/systems/round71_checks.py) `--case 11` |
| [12：S71-12](../12-security-network-frontiers.md) | 两段噪声Bell对交换；四分支与标签卷积 | [系统](../../codes/systems/round71_checks.py) `--case 12` |
| [13：A71-13](../13-quantum-information.md) | 经典Markov链与XOR的条件互信息 | [算法](../../codes/algorithms/round71_checks.py) `13` |
| [14：S71-14](../14-compilation-control.md) | 虚拟Z后的脉冲相位、矩阵等式和错误对照 | [系统](../../codes/systems/round71_checks.py) `--case 14` |
| [15：S71-15](../15-practice-research.md) | 多次查看与停止规则；预先分配错误概率 | [系统](../../codes/systems/round71_checks.py) `--case 15` |
| [16：A71-16](../16-advanced-algorithms-verification.md) | qubitization信号条件、反例和厄米化构造 | [算法](../../codes/algorithms/round71_checks.py) `16` |
| [17：A71-17](../17-computation-models.md) | echo时间失配的残余耦合与不可见相位误差 | [算法](../../codes/algorithms/round71_checks.py) `17` |
| [18：A71-18](../18-channels-capacities-complexity.md) | 协方差物理性、正矩阵反例、hbar与多模排序 | [算法](../../codes/algorithms/round71_checks.py) `18` |
| [19：S71-19](../19-engineering-architecture.md) | 相同POVM、不同测后过程；QND与重复性区别 | [系统](../../codes/systems/round71_checks.py) `--case 19` |
| [Q1：F71-Q1](../quantum-mechanics/01-experiments-states.md) | 两组相反的条件擦除条纹与整体概率 | [基础](../../codes/foundations/round71_checks.py) `--case q1` |
| [Q2：F71-Q2](../quantum-mechanics/02-observables-dynamics.md) | 不确定关系中保留对称协方差的加强界 | [基础](../../codes/foundations/round71_checks.py) `--case q2` |
| [Q3：S71-Q3](../quantum-mechanics/03-levels-control.md) | 矩形脉冲频谱零点；泄漏近似的条件 | [系统](../../codes/systems/round71_checks.py) `--case q3` |
| [Q4：A71-Q4](../quantum-mechanics/04-wavefunctions-models.md) | 势垒顶连续极限、超势垒反射、共振及边界匹配 | [算法](../../codes/algorithms/round71_checks.py) `q4` |

源码实践另有S71-MPF、OBP、NOISE、SQD、RNG、TOMO六组[带解练习](../appendices/software-practice.md)，连接权重约束、采样预算、截断偏差、噪声伴随、投影归一化、并行样本与过程层析。运行 `python3 codes/practice/workflow_checks.py`；固定结果可与逐步答案对照。它们是自编小模型，不导入vendor、不申请真机作业。

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
