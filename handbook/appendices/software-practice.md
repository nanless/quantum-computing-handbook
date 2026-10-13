# 算法、工业实践与开源代码对照

核验日期：原条目为2026-09-26；第11–16节研究及第72轮完整SDK验证为2026-10-13，旧条目保留各自核验日。本页把全书已有主题连接到可运行教学实验、真实开源实现和产业证据。它覆盖本书主要算法族及工程环节，不声称穷尽整个量子计算领域。具体数学条件仍以对应章节为准；“有库实现”“可在真机运行”“已获得商业收益”“证明量子加速”是四个不同问题。

本地保存了 26 个项目的 97 份文件（源码、许可证、声明及部分原项目说明），固定到 40 位提交哈希；见[完整源码索引](../../codes/vendor/README.md)与[机器可读校验清单](../../codes/vendor/manifest.json)。这些是未改写的源码摘录，便于对照阅读；完整安装还需要原仓库的其余模块、依赖及构建步骤。教学代码与第三方摘录分别存放。第72轮另安装并实际运行全部26项目的完整发行包或完整C/C++提交；逐项目的版本、任务、原始样本、失败复现与验收边界见[完整SDK实验册](../labs/sdk-validation.md)。这不等于执行所有上游功能或证明工业优势。

## 1. 怎样读算法对照表

先问输入是什么、允许什么访问方式，再问输出究竟是一个 bit、一组样本、一个数，还是一个量子态。例如 HHL 类算法的输出通常是与解向量成比例的量子态；若任务要求完整打印所有分量，不能把后处理成本忽略。类似地，振幅估计中“一次 oracle”可能含有昂贵的数据加载和可逆算术。

表中的“本地源码”表示已经保存该项目的代表性文件，并不表示整行提到的所有变体均已实现。完整文件列表是可检查的界限；没有保存的模块明确标为外部入口或理论练习。

## 2. 基础算法与容错算法族

| 算法族与章节 | 输入与输出 | 实现/实践入口 | 最容易漏算的条件或成本 |
|---|---|---|---|
| Deutsch–Jozsa、Bernstein–Vazirani，06 | 满足承诺的布尔 oracle → 分类或隐藏串 | 本章显式线路；第72轮Cirq完整oracle运行见06章A72-06 | 承诺、oracle 构造、经典随机算法基线 |
| Simon / 隐藏子群，06、16 | 隐藏结构函数 → 约束样本与经典恢复 | 正文推导及 GF(2) 消元；摘录仍非完整SDK；第72轮补可逆oracle/采样小例，非任意隐藏子群系统 | 多次采样、线性独立性、经典后处理 |
| QFT / QPE，06 | 可控酉算子与输入态 → 相位分布 | Cirq 相位估计例、Qiskit 相位估计、Qualtran QFT 源码；[圆周边界实验](../labs/algorithms.md) | 本征态重叠、受控幂的执行成本、模 1 误差 |
| Grover / 振幅放大，07 | 可制备初态及成功判据 → 标记样本 | Cirq 与 Qiskit Grover；[重试账本实验](../labs/algorithms.md) | 初始成功率、未知解数、反射、解的验证与总重试成本 |
| 振幅估计及迭代变体，07、16 | 制备和成功投影 → 概率估计 | Qiskit `iae.py` 固定源码 | 每个 Grover 幂的深度；置信保证不同于一次点估计 |
| Shor / 阶寻找，07 | 整数及模乘电路 → 周期候选、经典因子 | Cirq `examples/shor.py`；正文 15/35 例 | 可逆模算术、辅助位、连分数、失败分支；小整数例不代表破解规模 |
| 乘积公式 Hamiltonian 模拟，07、16 | 局域项、总时间与精度 → 近似演化 | OpenFermion 映射与 `simulate_trotter.py` 固定源码；第72轮已安装完整包并执行费米子映射，未遍历全部Trotter实现 | 非对易误差、时间步、分解后门数 |
| LCU / block-encoding / qubitization，16 | 加权算子访问 → 嵌入块与演化 | Qualtran `LinearCombination` 与 `QubitizationWalkOperator` 源码，另有QFT/加法 | 归一化因子、选择/制备 oracle、后选择与辅助位 |
| QSP / QSVT，16 | 块编码与可实现多项式 → 奇异值变换 | PennyLane `qsvt.py`、pyqsp相位求解与响应源码；[非厄米反例](../labs/algorithms.md) | 奇偶约束、相位约定；不能把奇异值变换一概写成矩阵多项式 |
| HHL / 量子线性系统，07、16 | 矩阵访问、右端态 → 解态或少量可观测量 | 07章A72-07完整非对角HHL，Cirq实际QPE→倒数旋转→反计算→后选择 | 条件数、稀疏/块访问、态制备、精度与结果读出 |
| 量子行走，16 | 图或 Markov 链访问 → 搜索/谱信息 | 16章A72-16a完整quimb一般小图行走；图搜索和qubitization仍须区分 | 建立成本、更新成本、谱隙、标记比例 |
| 容错算术与资源分解，11、16 | 高级子程序 → 分解与逻辑资源 | [Qualtran](https://github.com/quantumlib/Qualtran)，本地加法/QFT 源码 | 逻辑门数不等于物理位数；路由、工厂和等待需再估算 |

Qualtran 官方说明其仍是实验预览，接口和个别算法可能变化；固定提交有助复查，不意味着库结果已经被独立证明。更多原始算法论文见[参考资料](references.md)及各章文献。

## 3. 近中期算法、估计与经典基线

| 方法 | 实际工作分解 | 本地/外部代码 | 应如何比较 |
|---|---|---|---|
| VQE | 参数化态 → 多组 Pauli 测量 → 经典优化 | Qiskit `vqe.py`；[08 实验](../labs/algorithms.md) | 同一基组、活性空间、精度；计入优化调用和全部 shots |
| QAOA | 成本层和混合层 → 采样 → 可行解筛选 | PennyLane `qaoa/cost.py`；08 三顶点路径图精确分布 | 与穷举、局部搜索、成熟整数规划在相同时间预算比较 |
| SQD | 量子样本 → 组态恢复 → 子空间经典对角化 | Qiskit addon 的恢复与费米子模块 | 对比精选组态相互作用/DMRG；记录子空间维度和经典内存 |
| 量子核/变分学习 | 数据编码 → 重叠或测量特征 → 学习 | PennyLane 完整项目入口；本轮不存完整训练流水线 | 数据集划分、预处理、调参预算、强经典模型及数据加载成本 |
| 随机测量/经典阴影，16 | 随机测量与快照逆映射 → 可观测量估计 | PennyLane `ClassicalShadow` 后处理源码；第72轮完整两位随机采集/后处理已运行；未复现大规模硬件实验 | 目标可观测量族、方差/阴影范数、多重比较 |
| ZNE / PEC / 读出缓解，08、15 | 额外线路/校准 → 带权估计 | Mitiq 折叠和外推源码；[ZNE 预算实验](../labs/practice.md) | 总 shots、校准、噪声漂移、偏差与方差分别记录 |
| 退火 / QUBO，17 | 建模、嵌入、采样、链修复与验证 | dimod `ExactSolver` 为经典基线；云求解器另行获取 | 建模损失、链长、可行率、端到端 TTS；混合器不等于纯 QPU |
| MPS / 张量网络 | 线路/态的分解与收缩 → 可观测量 | quimb 的线路生成及收缩源码 | bond dimension、截断误差、收缩顺序、收敛；“位数多”不自动难 |
| 主方程/轨迹法，05、09 | Hamiltonian、耗散算符 → 密度矩阵或轨迹 | QuTiP `mesolve.py` 与 `mcsolve.py`；两种模型入口均已归档 | 马尔可夫近似、截断维度、步长/容差、迹与正性 |

对于 SQD，官方工具文档说明先从量子设备采样，再用经典计算做组态恢复和投影对角化；这与“量子处理器独自计算整个分子答案”不同。[SQD 官方说明](https://quantum.cloud.ibm.com/docs/en/addons/qiskit-addon-sqd)

## 4. 工程算法同样需要实测

| 环节 | 问题及输入输出 | 代码入口 | 必须保留的实验信息 |
|---|---|---|---|
| 编译、布局、SABRE 路由，14 | 抽象门图和连接图 → 原生线路与映射 | Qiskit SABRE Python 入口；[末态映射实验](../labs/systems.md) | 初/末布局、随机种子、设备 target、门数、时长及误差 |
| 稳定子电路采样，10 | Pauli 噪声电路 → 探测事件/逻辑可观测量 | Stim 表面码/重复码生成器 | 电路级模型、边界、轮数、相关错误；不是任意非Clifford模拟器 |
| 匹配译码，10 | 探测事件与图权重 → 逻辑预测 | PyMatching `matching.py` | 权重来源、相关性、时空边界、总失败次数、置信区间 |
| 魔法态工厂调度，11 | 带时间的需求和产出 → 停顿与缓存 | [自编离散事件实验](../labs/systems.md) | 吞吐不够描述突发需求；要有库存、首件延迟和时间线 |
| 网络协议，12 | 链路成功/记忆/交换 → 纠缠服务 | SeQUeNCe 传态及协议基类；两链路等待实验 | 丢包、经典信令、同步、储存寿命及保真度，不能只报链路距离 |
| 擦除标记、校准、运维，09、19 | 观测标签与维护事件 → 判定与可用率 | 自编 Bayes 与区间并集实验 | 基率、误报、事件重叠；小模型不替代生产监控 |
| 后量子密码，12 | 经典随机数/密钥 → 封装与解封装 | liboqs 的 C 语言 KEM 例子 | 这是经典密码代码，不是量子算法；研究原型不等于生产安全认证 |
| 最优控制/GRAPE，14 | 控制参数与目标酉 → 优化脉冲 | qutip-qtrl `pulseoptim.py` 与 `grape.py` 固定摘录；第72轮完整包受约束优化及泄漏/过滤测试已运行 | 带宽、幅度、泄漏、硬件传递函数、梯度和鲁棒性 |

Stim 的官方范围是稳定子操作，`stim.Circuit` 的噪声模型亦有限制；把任意振幅阻尼和 T 门直接塞进去不是同一个模拟问题。[Stim 官方能力与限制](https://github.com/quantumlib/Stim)

## 5. 工业实践：用完整工作流审查，不能只贴厂商名称

### 5.1 电子结构：量子样本加经典子空间计算

**目标**：给定分子几何、轨道基组和活性空间，估计能量或其他可观测量。输入的轨道积分本身通常由经典程序得到；不同的基组和活性空间意味着不同任务。

**公开证据**：IBM 2025 年的 SQD 技术报告介绍了 Heron 与 Fugaku 联合计算氮分子和铁硫簇的流程。它支持“公开展示了量子与超级计算机协作的电子结构计算”，不能单独推出“所有化学任务更快”或“已形成商业利润”。[IBM 研究报告，2025-03-23](https://research.ibm.com/publications/sample-based-quantum-diagonalization-for-electronic-structure-on-quantum-centric-supercomputers)

**复现路线**：先在可精确对角化的小体系验证费米子映射；再保存全部 bitstring、恢复前后的粒子数约束及子空间；最后比较同一 Hamiltonian 下的经典方法。源码中的组态恢复与 `fermion.py` 是两个不同阶段，不能把恢复策略的成功当作能量无偏的证明。

**还缺什么才能证明优势**：强经典基线的收敛曲线、相同误差容限、经典节点数/内存、量子 shots 和排队执行时间，以及更换规模后的结果。对完整生产化部署，本仓库没有私有日志，不能补造。

### 5.2 优化：建模成本和混合求解器边界

**目标**：排程、路径或资源分配中找到满足约束的低成本解。首先区分业务原问题与编码后的 QUBO；罚项太小可能产生低能量但不可行的结果，罚项过大可能压缩有效系数精度。

**公开入口**：D-Wave 官方工业优化文档展示通过 Leap 混合服务求解业务模型，并将直接使用 QPU 的研究路径分开。[工业优化文档](https://docs.dwavequantum.com/en/latest/industrial_optimization/index.html)、[模型与采样工作流](https://docs.dwavequantum.com/en/latest/industrial_optimization/workflow.html)

**复现路线**：先用本地 dimod 的穷举求解器核对极小实例；扩大后用成熟经典启发式或整数规划。记录同一约束、同一可行性检查与同一时间上限下的解质量分布。若服务包含经典预处理和后处理，结果应标为混合工作流，不能把全部改善归因于量子退火。

**证据边界**：厂商 API 可用、客户案例或合同是工程/商业采用证据；量子加速需要对具体任务和基线另证。云硬件有费用及账户依赖，本轮只整理公开代码，没有执行付费任务。

### 5.3 误差缓解：可靠估计与额外预算

**公开证据**：2023 年 IBM 的受控实验在指定模型和观测量上比较噪声缓解与经典近似。它是研究“噪声设备能否得到可用期望值”的案例；仅靠其标题不能作为 2026 年所有经典方法仍无法匹敌的证明。[原始论文](https://www.nature.com/articles/s41586-023-06096-3)

**复现路线**：使用已知理想值的小电路检查缓解偏差，再固定 shots 总预算，比较原始与缓解估计的均方误差。保留每种噪声缩放的原始计数。Mitiq 的折叠程序说明如何构造额外线路，外推程序说明如何处理结果；这两步的物理假设和统计开销需要分开核验。

### 5.4 纠错、网络与安全基础设施

纠错工作流是“电路与噪声 → syndrome → 译码 → 与真实逻辑翻转比较”。只看译码器平均运行时间会漏掉最坏延迟和硬件反馈期限。Stim/PyMatching 的公开源码有助复算模拟，但不是生产控制栈的全部。实验硬件证据见[10 章](../10-error-correction.md)，运维定义见[19 章](../19-engineering-architecture.md)。

网络模拟器能验证调度或协议逻辑，却不证明实测光纤损耗、记忆寿命已经达到模拟设置。SeQUeNCe 本地摘录是仿真协议代码；工程参数须来自自己的校准或公开实验。

PQC 的工程目标是替换受未来量子攻击威胁的经典密码。liboqs 官方把项目定位于原型与实验；本地 KEM 例子用于理解 API 流程，不能凭运行成功宣称侧信道、参数选择、随机数和系统集成都安全。[liboqs 官方说明](https://github.com/open-quantum-safe/liboqs)

## 6. 源码阅读练习与答案

### S01：为什么下载一个 Python 文件却不能直接运行？

找到 `vqe.py` 或 `qsvt.py` 的 import，列出其内部模块和外部依赖。答案：源码摘录仅保存算法的关键实现；它仍依赖包内类型、算子、电路表示和其他库。正确办法是按清单中的固定 commit 获取完整项目，在隔离环境按该提交的安装说明安装；不要靠连续修改 import 把摘录拼成不明版本。

### S02：如何证明手中的源码没有悄悄改变？

运行 `python3 codes/snapshot_sources.py --verify`。程序逐文件比较字节长度和 SHA-256，并核对提交字段长度。答案：匹配意味着本地字节与本清单一致；清单不提供作者身份的密码学背书，也不证明算法数学正确。源 URL、提交和许可证共同提供可追溯性，运行测试提供另一层证据。

### S03：同样叫“运行通过”，证据有何不同？

把“本地教学断言通过”“原库自带测试通过”“特定芯片实验复现”“优于强经典基线”排序。答案：它们回答不同问题，不能简单看成同一分数的高低。第71轮执行教学断言、文件校验和阅读版检查。第72轮追加26项目完整安装或构建后的实际本地任务，其中SQD-HPC另执行49项完整上游测试；这仍不等于所有库的全部上游测试，也没有新的真机实验。

## 7. 明确没有交付的部分

第72轮已经实际运行完整小实例HHL、一般图行走、两比特经典阴影、受约束GRAPE与Gaussian光子概率，详细输入输出见[SDK实验册](../labs/sdk-validation.md)。任意规模隐藏子群、拓扑量子计算、分布式容错、完整shading/PNA、动态MPF与生产部署仍未实现；本轮小实例与完整软件安装都不能替代这些系统的复现。未收集闭源生产代码、私有设备固件、付费后端数据及未经授权的录音。用户可以从表中看到这些差距，不会把一份有限代码目录误认为全领域完整实现。

## 8. 新增源码怎样逐步读：从数学对象走到实现

这一节针对实际保存在 `codes/vendor/` 的新增文件，不把项目名称当成算法说明。访问与下载核验日期为2026-09-26；完整commit与许可见[清单](../../codes/vendor/manifest.json)。每个条目都先指出正文连接，再说明输入输出、阅读顺序和未完成验证。S04、S05、S06、S08的独立数学复算可运行 `python3 codes/practice/source_reading_checks.py`，见[程序](../../codes/practice/source_reading_checks.py)与[固定样本结果](../../codes/practice/source-reading-results.json)；它不导入第三方摘录，S07的工程讨论不能由这几项数值断言替代。

### 8.1 QSP相位求解：先核对多项式基，再核对复响应

对应[第16章](../16-advanced-algorithms-verification.md)。多项式系数不是一种无需约定的数列。同一组数字可表示幂基 $1,x,x^2,\ldots$，也可表示Chebyshev基 $T_0,T_1,T_2,\ldots$；后者满足 $T_0=1,T_1=x,T_2=2x^2-1$。

本地[相位入口](../../codes/vendor/pyqsp/pyqsp/angle_sequence.py)的 `QuantumSignalProcessingPhases` 在固定commit中把列表/数组直接构造为 `Chebyshev` 对象。因此 $x^2=(T_0+T_2)/2$ 应用系数 `[0.5,0,0.5]` 表达；幂基中的 `[0,0,1]` 在这个入口会成为 $2x^2-1$。有些上游README段落仍讨论另一种基约定，不能越过固定源码的实际转换逻辑。这个局部核查不意味着已证明整个求相位算法正确。

随后读[对称相位迭代](../../codes/vendor/pyqsp/pyqsp/sym_qsp_opt.py)的 `newton_solver` 和[响应计算](../../codes/vendor/pyqsp/pyqsp/response.py)的 `ComputeQSPResponse`。需要同时记录signal operator、测量基、相位顺序和读取实部/虚部的约定；`sym_qsp` 路径返回矩阵元，不能把复矩阵元直接当测量概率。

**源码练习S04。** 在 $x=0,1/2,1$ 比较上述两组系数的值。答案：目标 $x^2$ 为 $(0,1/4,1)$，错误解释为 $T_2$ 时是 $(-1,-1/2,1)$；仅检查端点1发现不了错误。完整安装后还须检查区间内近似误差与酉响应，而非只看优化器“收敛”标志。源码定位依据为[pyqsp作者仓库](https://github.com/ichuang/pyqsp)，第71轮未运行完整环境；第72轮已实际求相位并独立重建响应，见16章A72-16b，未声称全套上游测试。

### 8.2 LCU与qubitization：被隐藏的归一化因子

对应[第16章](../16-advanced-algorithms-verification.md)。本地[LinearCombination](../../codes/vendor/qualtran/qualtran/bloqs/block_encoding/linear_combination.py)组合若干块编码。假设输入第 $i$ 项的归一化是 $\alpha_i$、组合权重是 $\lambda_i$，该构造记录的归一化为 $\alpha=\sum_i|\lambda_i|\alpha_i$，并非总取1。

**源码练习S05。** 若 $A=0.3X-0.4Z$，两项各有 $\alpha_i=1$，组合归一化为0.7。利用 $XZ+ZX=0$，有 $A^2=(0.3^2+0.4^2)I=0.25I$，所以谱范数为0.5，确实不超过0.7。这里0.7是这个构造的系数上界，不是最小可能归一化；改变构造会影响资源。

再读[qubitization行走算子](../../codes/vendor/qualtran/qualtran/bloqs/qubitization/qubitization_walk_operator.py)，跟踪prepare/select、辅助寄存器和反射。源码中能构造对象不代表这些oracle已廉价实现；资源研究要把分解成本和后选择成功率带回正文。与图搜索中的一般量子行走也不可仅因名称相同就互换。依据为[Qualtran官方项目](https://github.com/quantumlib/Qualtran)，第71轮仅保存与阅读选定模块；第72轮追加模算术域与实际门分解任务，不能由此断言全部LCU访问成本已实现。

### 8.3 经典阴影：保存测量基，理解非物理的单个快照

对应[第16章的测量与验证](../16-advanced-algorithms-verification.md)。[PennyLane后处理代码](../../codes/vendor/pennylane/pennylane/shadows/classical_shadow.py)同时接收 `bits` 和 `recipes`，形状都是“shots数×测量位数”。只保存0/1而丢掉各次选用的Pauli基，就缺少逆映射所需信息。[官方API说明](https://docs.pennylane.ai/en/stable/code/api/pennylane.ClassicalShadow.html)也区分局域统计和昂贵的全态重构。

**源码练习S06。** 单比特某次在X基得到正结果，相应快照为 $\hat\rho=3|+\rangle\langle+|-I$。在X基本征向量上，它的本征值是2和−1，迹为1却不是正半定。它是统计逆映射的单次估计量，不是这次实验制备出的密度矩阵；负本征值本身不能判定程序错误。多个快照平均的期望可恢复目标态，但有限样本均值仍可能非物理。

工程核查应保留测量基生成规则、种子、原始位串、目标可观测量列表，以及是否在看到数据后挑目标。此处归档的是后处理模块，没有保存所有设备采集实现，第72轮另实际保存30000次两位随机阴影样本并独立重算；这仍不是大体系硬件实验。

### 8.4 变分梯度：参数、门角度和计算图是三层对象

对应[第08章的参数共享反例](../08-applications.md)。[parameter_shift.py](../../codes/vendor/pennylane/pennylane/gradients/parameter_shift.py)是量子线路参数梯度变换入口，后续还需要经典计算图把门参数导数传回共享参数。两处门角都使用同一个训练变量，并不意味着可把整条线路的该变量平移一次后直接套单门二点规则。

源码阅读时列出：可训练门参数索引、每个生成元的谱/频率、各移位线路、组合系数，以及外部参数的链式法则。核验样本使用[本书算法检查](../../codes/algorithms/round70_checks.py)；它独立比较正确逐门规则、错误整体移位和解析导数。本地保存上游梯度模块，不把本书标准库实验当作PennyLane完整测试。

### 8.5 主方程与量子轨迹：一个平均不等于一条随机实现

对应[第05章](../05-noise-channels.md)和[第09章](../09-hardware.md)。QuTiP的[mesolve](../../codes/vendor/qutip/qutip/solver/mesolve.py)处理密度矩阵等确定性演化；新增[mcsolve](../../codes/vendor/qutip/qutip/solver/mcsolve.py)入口通过量子轨迹进行随机求解。比较二者须使用同一个Hamiltonian、塌缩算符、初态与时间网格，再比较轨迹平均的可观测量和抽样误差。

增加轨迹数处理蒙特卡洛误差，缩小积分容差处理数值积分误差，增大截断Hilbert空间处理截断误差；这三种调整不是同一件事。单条轨迹不必与密度矩阵曲线重合。第71轮没有安装完整QuTiP；第72轮完整执行主方程和4096条轨迹，保存同模型参数与标准误，见Q2的F72-Q2。物理模型另由独立解析式核验。接口原始入口见[QuTiP官方仓库](https://github.com/qutip/qutip)。

### 8.6 GRAPE与CRAB：优化出的脉冲还要通过设备约束

对应[第14章](../14-compilation-control.md)。新增qutip-qtrl的[pulseoptim.py](../../codes/vendor/qutip-qtrl/src/qutip_qtrl/pulseoptim.py)与[grape.py](../../codes/vendor/qutip-qtrl/src/qutip_qtrl/grape.py)，原许可为BSD三条款。先从目标酉算子、漂移Hamiltonian $H_0$、控制算符 $H_j$、时间网格与幅度数组读起，理解 $H(t)=H_0+\sum_j u_j(t)H_j$。各项与时间相乘后必须是无量纲的指数参数；若采用 $\hbar=1$，仍须统一角频率单位。

GRAPE利用离散控制变量的梯度；CRAB用有限基函数参数化脉冲再优化系数。不同参数化、梯度计算和终止准则影响成本与局部极值，不能说二者之一无条件先进。`grape_unitary` 的原docstring还明确标为实验性工作；归档不能把该函数自动升级为生产保障。[项目官方说明](https://github.com/qutip/qutip-qtrl)确认该包从QuTiP核心分离并支持这两类方法。

**源码练习S07。** 软件算出某脉冲在二能级模型中达到很小的目标误差，还需至少检查什么？答案：时间离散收敛、驱动幅度/带宽、控制链传递函数、向高能级泄漏、失谐和噪声鲁棒性、真实读出和校准。数学目标函数下降只支持该模型中的优化，不自动说明任意波形发生器能输出该脉冲。

### 8.7 线路切割：采样权重与重构顺序必须同时保留

对应[第14章](../14-compilation-control.md)、[第19章](../19-engineering-architecture.md)及[P15-G](../labs/practice.md)。新增[weights.py](../../codes/vendor/qiskit-addon-cutting/qiskit_addon_cutting/qpd/weights.py)与[cutting_reconstruction.py](../../codes/vendor/qiskit-addon-cutting/qiskit_addon_cutting/cutting_reconstruction.py)。前者区分精确计入的权重和抽样权重；后者要求结果顺序与子实验和可观测量的生成顺序一致。

**源码练习S08。** 两项权重为1.5和−0.5，两组均值0.4和−0.2，正确结果是0.7；若仅交换结果顺序却不交换系数，得到 $1.5(-0.2)-0.5(0.4)=-0.5$。两个数都在 $[-1,1]$，所以“输出在物理范围内”抓不到顺序错误。作业ID、分区标签、可观测量和系数的对应关系都应保存，不能按任务完成先后盲目拼接。

该项目实现流程见[官方文档](https://qiskit.github.io/qiskit-addon-cutting/)。第71轮保存权重与重构入口；第72轮追加Bell线路的完整分区、生成、精确本地执行与重构，见R72-CUT。自动切口搜索、真机执行和全链路工业基准仍未完成。

### 8.8 噪声模型：名字相同，平衡态参数仍须核对

新增[Aer standard_errors.py](../../codes/vendor/qiskit-aer/qiskit_aer/noise/errors/standard_errors.py)，用于对照退极化、振幅阻尼等模型。核查顺序是“读取矩阵或映射—验证保迹—寻找固定点—比对文字参数”。基础组发现某官方页面的平衡占据文字与其Kraus固定点不一致，具体核查放在[第05章](../05-noise-channels.md)及该组审查报告；不修改原始vendor文件掩盖上游差异。

固定commit来源为[Qiskit Aer官方项目](https://github.com/Qiskit/qiskit-aer)。第72轮安装完整官方Aer wheel并执行54输入噪声及动态传态；没有从源编译Aer C++后端。完整包运行证据与摘录字节校验分别保存。

## 9. 新方法与工业工作流：下一步究竟缺什么证据？

[IBM于2026-03-12发布的量子与高性能计算参考架构说明](https://research.ibm.com/blog/quantum-centric-supercomputing-system-reference-architecture)把量子处理器放进异构计算流程，并讨论SQD、经典子空间计算和工作流编排（访问2026-09-26，厂商技术说明）。它支持“公开提出并描述这一体系结构与实例”，不能单独证明某业务在相同质量和总成本下优于强经典方法。

下面这些入口来自[官方addons目录](https://quantum.cloud.ibm.com/docs/en/guides/addons)（访问2026-09-26）。它们帮助发现比单个算法更完整的工作流，第70轮尚未保存和运行表中四类项目；第71轮已保存MPF、OBP、SQD-HPC以及Pauli传播引擎的固定摘录并增加独立教学核算，见第11–16节。第72轮追加完整安装/构建和明示本地任务，见下表及SDK实验册；工业部署仍未复现。

| 方法/环节 | 要理解的核心变化 | 必须补做的验证 | 本轮状态 |
|---|---|---|---|
| Multi-product formulas | 用多个演化近似的带权组合控制误差 | 总shots、负权重方差、近似误差与同预算单一乘积公式比较 | 第72轮完整SDK已实际运行静态约束解/合成线路；动态TN未运行 |
| Operator backpropagation | 把一部分线路作用转移到待测可观测量 | 可观测量项数增长、截断偏差、测量分组和经典开销 | 第72轮完整SDK正常路径已运行；一项预算发现0.3.0缺陷，保留复现/防护 |
| SQD for HPC | 使样本子空间对角化适配经典HPC流程 | 子空间/节点规模、内存、通信、收敛和同Hamiltonian基线 | 完整Python SQD投影求解及C++HPC测试/三阶段驱动已运行；多节点未复现 |
| Shaded lightcones / Pauli propagation | 利用目标可观测量相关结构缩减噪声处理工作 | 被忽略项的误差、噪声模型标定、与完整PEC的预算比较 | 完整Rust wheel传播/截断已运行；完整shading工作流未运行 |

这些方法可能改变误差与成本的分配，不取消读入、经典预处理、校准、通信、采样和验证。一个可审查的工业实验应保存相同业务输入下的经典与量子混合两条完整流程，先设可行性和误差门槛，再画质量随端到端时间/成本变化的曲线。公开证据若只有论文图或供应商案例，就明确写这一层，不能补造客户生产日志。

## 10. 覆盖状态与可继续研究的边界

| 材料层 | 当前可交付 | 仍不能据此宣称 |
|---|---|---|
| 章节解释与自编小模型 | 全书对应章节、就地详解、固定样本和断言 | 已实现任意规模的全部算法 |
| 第三方固定源码 | 26项目97文件，来源/许可/commit/哈希 | 是完整SDK或已通过所有上游测试 |
| 完整SDK本地任务 | 26项目完整安装/构建，HHL、行走、CV及各表列任务实际执行 | 任意规模全部算法、全部上游测试或生产验证 |
| 工业证据 | 原论文、官方工作流和限定场景 | 闭源生产代码、私有日志或普遍商业优势 |
| 新增方法观察 | 四类官方工作流入口与第11–16节明示的源码/核算状态 | 动态TN、完整shading等上层工作流都已运行，或已经证明普适优越性 |

下载范围围绕教材主题与许可明确的代表性实现，不无差别复制整个生态或不明来源合集。下一次扩展应先选可验证的问题和最小实例，再补完整环境与测试；新的模型或更大源码目录都不应代替这一验证步骤。

## 11. 多乘积公式：抵消近似误差之后还要算方差

本节至第16节的资料访问日期为2026-10-13。新增固定源码见[vendor清单](../../codes/vendor/manifest.json)，独立教学核算为[workflow_checks.py](../../codes/practice/workflow_checks.py)及[固定结果](../../codes/practice/workflow-results.json)。上面的旧核验日期仍描述旧条目；新增文件不意味着重新运行了所有上游项目。

一个常见限制是：更细的Trotter步长可以减小模拟误差，却需要更深的线路。多乘积公式（MPF）尝试分别执行不同步数的近似演化，再组合所需的期望值。这里的经典带权组合不等于把几条线路的振幅相干相加；负系数组成的矩阵也不一定是可制备的密度矩阵。[官方教程](https://qiskit.github.io/qiskit-addon-mpf/tutorials/01_getting_started.html)采用可观测量重构流程；理论入口为[良态条件多乘积公式论文](https://quantum-journal.org/papers/q-2023-07-25-1067/)。

### 11.1 先解两条约束，再看哪项误差留下

以下是独立构造的教学误差模型，**不是任意Hamiltonian的统一误差定理**。固定总时间、初态和可观测量，假定步数足够大时具有展开

$$
E_k=E_*+\frac{a}{k^2}+\frac{b}{k^4}+O(k^{-6}).
$$

选择$k_1=2,k_2=4$。要让组合$\widetilde E=c_1E_2+c_2E_4$保留目标值并消去首项误差，需要

$$
c_1+c_2=1,\qquad \frac{c_1}{4}+\frac{c_2}{16}=0.
$$

第二式乘以16得到$4c_1+c_2=0$；减去第一式，得到$3c_1=-1$。因此$c_1=-1/3,c_2=4/3$。剩余四阶项的系数是

$$
-\frac1{3\cdot16}+\frac4{3\cdot256}=-\frac1{64}.
$$

**练习S71-MPF。** 取$E_*=1/4,a=0.12,b=0.03$，在本题中高阶项恰为零。求各次结果、重构误差，以及总9000次独立测量的保守方差。每次读数为$\pm1$，两组独立，先忽略单次执行时长的差别。

**逐步答案。** $E_2=0.25+0.03+0.001875=0.281875$；$E_4=0.25+0.0075+0.0001171875=0.2576171875$。代入得到$\widetilde E=0.24953125$，误差为$-0.00046875$，与$-b/64$相同。这只是近似偏差，不含采样误差。

设各组样本数为$N_j$、单次方差为$v_j\le1$，则

$$
\operatorname{Var}(\widetilde E)=\sum_j\frac{c_j^2v_j}{N_j}
\le\sum_j\frac{c_j^2}{N_j}.
$$

在固定$N_1+N_2=N$下，Cauchy–Schwarz给出最小保守上界$\Gamma^2/N$，其中$\Gamma=\sum_j|c_j|=5/3$；取$N_j=N|c_j|/\Gamma$达到它。所以$N_1=1800,N_2=7200$，上界为$25/81000\approx0.000308642$。已知真实$v_j$时最优分配是$N_j\propto|c_j|\sqrt{v_j}$；若单次耗时不同，要使用[第15章](../15-practice-research.md)的时间预算，而非继续沿用这组比例。

**加问。** 为什么不总选两个很接近的步数？取$(4,5)$，约束解为$(-16/9,25/9)$，因此$\Gamma=41/9$，保守采样系数$\Gamma^2$约20.75，比$(2,4)$的约2.78大得多。步数更细不自动意味着总体均方误差更小；还需核对展开有效区间、噪声与权重稳定性。[官方稳定性说明](https://qiskit.github.io/qiskit-addon-mpf/explanations/mpf_stability.html)

### 11.2 一个真正用矩阵演化的最小实例

配套程序另取$\mathcal H=X+Z$、$\hbar=1$、无量纲时间$t=0.7$、初态$|0\rangle$和测量$Z$。由于$(X+Z)^2=2I$，精确演化可直接写成

$$
U(t)=\cos(\sqrt2t)I-i\frac{\sin(\sqrt2t)}{\sqrt2}(X+Z).
$$

二阶分片为$S_2(h)=e^{-ihX/2}e^{-ihZ}e^{-ihX/2}$，重复$k$次，其中$h=t/k$。程序得到精确期望约0.301106901；2步和4步分别约0.353680816、0.314159980；重构约0.300986367。读者应先用$e^{-ihX}=\cos hI-i\sin hX$复算每个二维矩阵，再比较概率和期望，不能把复矩阵元直接当读数。

![更小的近似偏差仍需要足够采样预算：两种独立测量方案的均方误差上界](../assets/workflow-mpf-budget.svg)

图按该理想模型的精确偏差，加上$1/N$或$(5/3)^2/N$的方差上界绘制；横轴是总独立shots，纵轴是无量纲均方误差上界，两轴为对数。它不是实测误差曲线，也没有计入深线路更长的执行时间、门噪声、漂移或校准。负权重降低理想偏差，但在预算不足时，本例的保守上界仍可能更大。[图生成器](../../codes/practice/workflow_figures.py)

源码从[static.py](../../codes/vendor/qiskit-addon-mpf/qiskit_addon_mpf/static.py)的约束矩阵读起，再看[LSE](../../codes/vendor/qiskit-addon-mpf/qiskit_addon_mpf/costs/lse.py)和[优化约束](../../codes/vendor/qiskit-addon-mpf/qiskit_addon_mpf/costs/exact.py)。[dynamic.py](../../codes/vendor/qiskit-addon-mpf/qiskit_addon_mpf/dynamic.py)另包含依时间变化的构造，不能把本题的固定系数说成全部动态MPF的实现。第71轮仅核验固定字节与独立模型；第72轮实际执行cvxpy/CLARABEL静态解及分解后的Suzuki电路，见R72-MPF。动态MPF张量网络后端仍未执行。

## 12. 可观测量反向传播：线路缩短后到底要测什么

设原线路分为前半$V$和后半$U$，测量厄米算符$O$。令前半输出$\rho_V=V\rho V^\dagger$，利用迹的循环性，有

$$
\operatorname{Tr}(O U\rho_VU^\dagger)=\operatorname{Tr}(U^\dagger O U\rho_V).
$$

因此可以省去设备上的后半线路，改测$O'=U^\dagger O U$。这保留的是指定期望值，不保证原末态、全部测量分布或所有后续用途都一样。新可观测量可能展开成许多Pauli项，经典传播和量子测量成本随之增加。[官方OBP说明](https://qiskit.github.io/qiskit-addon-obp/)与[API](https://qiskit.github.io/qiskit-addon-obp/apidocs/qiskit_addon_obp.html)

**练习S71-OBP。** 在$|0\rangle,|1\rangle$顺序中，$U=R_y(\theta)$，$O=Z$，$\theta=\pi/6$，前半输出为$|+\rangle$。求反向传播结果；若为省测量丢弃其$X$项，误差多大？

**逐步答案。** 令$c=\cos(\theta/2),s=\sin(\theta/2)$，则

$$
U=\begin{pmatrix}c&-s\\s&c\end{pmatrix},\qquad
U^\dagger ZU=
\begin{pmatrix}c^2-s^2&-2cs\\-2cs&s^2-c^2\end{pmatrix}
=\cos\theta Z-\sin\theta X.
$$

在$|+\rangle$上$\langle Z\rangle=0,\langle X\rangle=1$，因此正确期望是$-1/2$。只测保留的$\cos\theta Z$得到0，偏差为$1/2$。正负号可直接由上述矩阵核对；把$UOU^\dagger$当成$U^\dagger OU$会得到相反方向。

一般若丢弃$D=\sum_{j\in R}d_jP_j$，每个Pauli串满足$\|P_j\|_\infty=1$，则对任何归一化密度矩阵

$$
|\operatorname{Tr}(D\rho)|\le\|D\|_\infty\le\sum_{j\in R}|d_j|.
$$

这给出确定性偏差界；不是shot数增加就能消掉的统计标准误。本题只有一项且$|+\rangle$正好达到上界。多层截断在酉传播下可把各层算符范数误差相加；若改用噪声逆映射或准概率缓解，必须重新检查其范数放大，不能自动套酉情形。

源码重点为[backpropagate](../../codes/vendor/qiskit-addon-obp/qiskit_addon_obp/backpropagation.py)、[截断预算](../../codes/vendor/qiskit-addon-obp/qiskit_addon_obp/utils/truncating.py)和[metadata](../../codes/vendor/qiskit-addon-obp/qiskit_addon_obp/utils/metadata.py)。记录输入线路分片、返回剩余线路、传播后的可观测量、实际丢弃系数与累计预算，才能复查重构。该项目的高阶$L_p$预算需要额外假设；本题只使用上面独立证明的$L_1$界，没有把所有范数互换。

## 13. Pauli传播与噪声：Heisenberg方向不能凭名称猜

理想门之外，信道的伴随映射定义为

$$
\operatorname{Tr}[O\mathcal E(\rho)]=\operatorname{Tr}[\mathcal E^\dagger(O)\rho].
$$

这里$\mathcal E^\dagger$表示相对于迹内积的伴随，不是信道的逆操作。若$\mathcal E(\rho)=\sum_jK_j\rho K_j^\dagger$，就有$\mathcal E^\dagger(O)=\sum_jK_j^\dagger O K_j$。保迹条件使$\mathcal E^\dagger(I)=I$，但不会让所有$O$都不变。[第05章信道定义](../05-noise-channels.md)

**练习S71-NOISE。** 先在$|0\rangle$上做$R_y(\pi/6)$，再经历概率$p=0.1$的相位翻转$\mathcal E(\rho)=(1-p)\rho+pZ\rho Z$，最后测量$X$。分别从状态与可观测量计算输出。

**逐步答案。** $ZXZ=-X$，所以$\mathcal E^\dagger(X)=(1-2p)X=0.8X$。又由矩阵乘法得到$U^\dagger XU=\cos\theta X+\sin\theta Z$，在$|0\rangle$上的期望为$\sin\theta=1/2$。最终结果是$0.8/2=0.4$。从输出态分别算“未翻转”和“翻转”分支，得到$0.9(0.5)+0.1(-0.5)=0.4$。只传播理想门会报告0.5，忽略的是模型偏差，不是少取几次样本。

本地[Python入口](../../codes/vendor/pauli-prop/python/pauli_prop/propagation.py)负责线路、Pauli和方向约定，[Rust核心](../../codes/vendor/pauli-prop/src/lib.rs)包含传播、项合并与截断。官方文档说明它可用于理想/含噪传播，以及OBP等上层方法；截断让对象保持稀疏，但需要报告近似误差。[Pauli propagation官方说明](https://quantum.cloud.ibm.com/docs/en/addons/pauli-prop)

本轮保存的是传播引擎，**没有**保存完整shaded-lightcone或PNA工作流，第72轮另安装完整官方wheel并实际调用其Rust扩展传播；没有从源编译Rust扩展。噪声模型应从标定或受控实验取得；本题的$p=0.1$是明示教学参数。传播引擎存在不等于这些参数已经在工业设备上验证。

## 14. SQD与HPC：去重、投影和随机流分别负责什么

SQD把采样得到的组态用于构建经典子空间，再在该子空间内求解。HPC实现帮助组织较大的经典计算；并不把采样、组态修复、对角化和验证变成免费的步骤。新增源码包括[子采样](../../codes/vendor/qiskit-addon-sqd-hpc/include/qiskit/addon/sqd/subsampling.hpp)、[组态恢复](../../codes/vendor/qiskit-addon-sqd-hpc/include/qiskit/addon/sqd/configuration_recovery.hpp)、[组态整理](../../codes/vendor/qiskit-addon-sqd-hpc/include/qiskit/addon/sqd/fermion.hpp)与[并行随机流](../../codes/vendor/qiskit-addon-sqd-hpc/include/qiskit/addon/sqd/internal/parallel-rng.hpp)。[官方项目说明](https://qiskit.github.io/qiskit-addon-sqd-hpc/)

### 14.1 样本数量不等于子空间维数

**练习S71-SQD。** 三个正交基向量$e_1,e_2,e_3$的Hamiltonian为

$$
\mathcal H=\begin{pmatrix}0&-1&0\\-1&0&-1\\0&-1&0\end{pmatrix}.
$$

原始标签列表为`001,010,001`，本题把它们分别对应$e_1,e_2,e_1$；这是任意三维教学模型，不是分子轨道编码。去重后子空间只含$e_1,e_2$。求子空间基态和能量，并比较全空间结果。

**逐步答案。** 投影矩阵$P=(e_1,e_2)$满足$P^\dagger P=I_2$，$\mathcal H_S=P^\dagger\mathcal HP=\left(\begin{smallmatrix}0&-1\\-1&0\end{smallmatrix}\right)$。其基态为$(1,1)^T/\sqrt2$，Ritz能量是$-1$。全空间特征方程为$-\lambda(\lambda^2-2)=0$，基态能量是$-\sqrt2$；因此$-1$是上界，仍有约0.414214的误差。

把子空间向量嵌回全空间为$\psi_S=(1,1,0)^T/\sqrt2$，则$\mathcal H\psi_S+\psi_S=(0,0,-1/\sqrt2)^T$，残差范数$1/\sqrt2$。一个低残差可能帮助定位某个本征值，但若没有谱隙、能量顺序等额外信息，不能仅凭残差证明它就是全空间基态。大模型中无法精确对角化时，仍应检查相同Hamiltonian下的子空间扩展、残差和强经典基线。

**加问。** 如果把重复的$e_1$作为新的正交维度，会怎样？另取$\mathcal H_D=\left(\begin{smallmatrix}0&-1&0\\-1&0&0\\0&0&2\end{smallmatrix}\right)$，真实最低能量为$-1$。使用$P_D=(e_1,e_2,e_1)$得到Gram矩阵$G=P_D^\dagger P_D$，它含两个相同列且奇异；直接把$P_D^\dagger\mathcal H_DP_D$当正交基下的Hamiltonian会得到伪最低值$-\sqrt2<-1$。正确方法是去重/正交化，或在独立支撑上处理广义本征问题$H_Sc=EGc$。代码还核对将伪本征向量还原到物理空间后的Rayleigh商，确认错误来自归一化口径。

### 14.2 固定seed还不一定固定并行结果

**练习S71-RNG。** 同样六个任务，按正序和逆序执行，怎样让每个任务得到同一组教学随机样本？

**逐步答案。** 保存稳定任务ID，并让每个任务的随机流由“主种子、任务ID、算法版本”决定；不要把“第几条线程”当任务身份。程序把字符串`71:任务ID`经SHA-256映射为本地`random.Random`的种子，比较两种执行顺序，逐任务输出相同。这只演示调度不变性，**不是Philox实现，也不证明这些伪随机流在统计意义上独立**。重新编号任务仍会改变样本，ID映射必须随输入保存。

官方[随机数说明](https://qiskit.github.io/qiskit-addon-sqd-hpc/random-number-generation.html)区分按工作项索引定位的counter-based引擎与按线程分配的普通引擎；固定提交中的相关逻辑见上述`parallel-rng.hpp`。因此工业复现实验还要记录引擎类型、主种子、任务编号、线程数、编译选项和归约顺序；“使用MPI/HPC”不自动保证位级可重复，也不说明本仓库已做多节点运行。

## 15. 过程层析：输入覆盖、条件记录与设置数量

只验证一个输入态，通常不足以确认一个未知过程。振幅阻尼与完全退相位都保持$|0\rangle\langle0|$，却对$|+\rangle$产生不同输出；前者在阻尼参数$\gamma=0.3$时非对角元为$\sqrt{0.7}/2\approx0.418330$，后者为0。因此“零态测试通过”不能替代过程层析。相同的测量结果概率也不确定测后操作，见[第02章](../02-single-qubit.md)与[第19章](../19-engineering-architecture.md)。

**练习S71-TOMO。** 每比特用4个线性独立制备态和3个Pauli测量基，完整积式$n$比特QPT需要多少设置？5比特每设置1000 shots，总量是多少？

**逐步答案。** 输入制备设置有$4^n$，输出测量设置有$3^n$；每一输入要遍历每一测量，因此总设置$12^n$。1、2、5、10比特分别为12、144、248832、61917364224。5比特的总shots为248832000，尚未计入校准、复位、批次重复和线路编译。每设置含$2^n$种可能结果，不能再把这个数自动乘成必须执行的设置数。

这与[ProcessTomography官方默认方案](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.ProcessTomography.html)及本地[qpt_experiment.py](../../codes/vendor/qiskit-experiments/qiskit_experiments/library/tomography/qpt_experiment.py)对应。它不是所有层析方法的普适下界；已知结构、压缩感知、选择少量目标指标或其他制备/测量模型会改变需求。

中途测量的条件分支还必须保留经典结果、各分支次数和归一化方式。[tomography_analysis.py](../../codes/vendor/qiskit-experiments/qiskit_experiments/library/tomography/tomography_analysis.py)提供阅读入口；不能只保存每支归一化矩阵后丢掉发生概率，再把它们等权相加。统计拟合、完全正约束、读出误差与SPAM假设各自回答不同问题，第71轮没有运行拟合器；第72轮追加真实QST/QPT拟合、原计数和低shots CP/TP反例，见02/05章F72；仍无真机层析。

## 16. 把软件约定带回全书公式

跨项目同名函数并不自动采用本书同一个约定。下面三项检查应在写实验记录时完成，而不是看到不一致输出后再猜原因。

| 对照对象 | 本书约定与固定源码差异 | 可核验的操作 |
|---|---|---|
| Gaussian协方差 | 第18章采用$[\hat q,\hat p]=i$、真空$V=I/2$；Walrus `is_valid_cov`默认`hbar=2` | 传入`hbar=1`，或连同坐标和全部协方差做一致缩放；不能只改一个真空数字 |
| 保真度 | 本书$F$是根保真度；Walrus `fidelity`的docstring采用纯态重叠模平方 | 对齐$F$与$F^2$再比较；纯态内积模为0.8时两者是0.8与0.64 |
| 信道组合 | $\mathcal B\circ\mathcal A$表示先$\mathcal A$再$\mathcal B$；SDK `compose(front=...)`指定对象顺序 | 在非交换信道上画出输入→输出链，用Kraus乘积核查，不只读方法名 |

仪器模型另可阅读[pyGSTi Instrument](../../codes/vendor/pygsti/pygsti/modelmembers/instruments/instrument.py)：它把结果标签与相应操作放在同一对象内，而不只保存一个POVM概率表。保留各分支的完全正映射、发生概率与合并后的保迹性质，才能描述动态测量和反馈。该文件的存在不意味着本书已经运行门集层析拟合，或已经证明某设备测量满足QND。依据为[pyGSTi官方源码](https://github.com/sandialabs/pyGSTi/blob/master/pygsti/modelmembers/instruments/instrument.py)（Apache-2.0，原NOTICE保留，访问2026-10-13）。

前两行可直接阅读[gaussian_checks.py](../../codes/vendor/thewalrus/thewalrus/quantum/gaussian_checks.py)中的定义、参数和平方说明；第71轮未安装The Walrus；第72轮实际运行完整包并以独立概率公式核对，显式hbar与排序见18章A72-18。相应正文新增物理性算例见[第18章](../18-channels-capacities-complexity.md)。

第三行的固定源码为[kraus.py](../../codes/vendor/qiskit/qiskit/quantum_info/operators/channel/kraus.py)，本书非交换诊断见[第05章](../05-noise-channels.md)。若先施加Kraus集合$\{A_j\}$，再施加$\{B_k\}$，组合集合是$\{B_kA_j\}$；这可从$\mathcal B(\mathcal A(\rho))$逐项展开得到。源码阅读与小模型核算不能替代完整SDK版本的集成测试。

新增来源覆盖了原第9节四类后续研究项中的MPF、OBP与SQD-HPC，以及Pauli传播引擎。完整shaded-lightcone/PNA、任意规模HHL、全部工业工作流、私有设备控制代码和真机优势复现仍不在本轮交付内；覆盖表应据此更新，不能因为源码数量增加就删除这些缺口。
