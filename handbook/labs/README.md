# 实验、练习与可复现代码总览

本手册把全书 **26 篇正文**（主篇第 00–21 章与量子力学基础篇 Q1–Q4）连接到本地可运行的动手实验与浏览器互动沙盒。学习每个主题时，建议先读题目、在草稿纸上写出预测，再运行程序核对每一步推导、答案与模型边界。全书 26 篇正文的 [271 道自检题及分级零跳步参考解答](../appendices/exercises.md)（含难度标签、防剧透核心提示与四步完整演算）均已收录于附录 D；离线统一检验入口现包含 **38 项**纯 Python 3 标准库实验与校验脚本。

## 怎样开始

1. **零安装视觉直觉上手（推荐首站）**：直接在浏览器打开[**离线交互量子实验台（6 模块沙箱）**](../../reader/lab/quantum-lab.html)——无需配置任何 Python 环境，即可交互体验 **01 MZI 干涉与密度矩阵**、**02 Bloch 球真弧沙盒**、**03 Ramsey 退相干与 Fisher 灵敏度**、**04 Bell 偏迹与 CHSH 博弈**、**05 Grover 半拍放大与过冲陷阱**以及 **06 $d=3$ 表面码注错解码**六大核心模型。
2. **零基础入门主线**：打开[基础实验册](foundations.md)，从 `F00`、`F01`、`F02` 起步亲手核对抽样波动、左共轭内积与 $Y$ 基测量门序，再跟进十一组诊断反例与开放动力学轨迹对照。
3. **算法与经典模拟路线**：使用[算法实验册](algorithms.md)，先完成 QPE 与 Grover（`06-A`、`07-A`），再贯通高阶算法与 QSVT 专题核验（LCHS、Carleman、6 门 PREPARE–SELECT、QROM 与 $4\times 4$ 负谱 QSVT），以及第 21 章稳定子表、MPS / 二维 PEPS 与含噪 Pauli 传播三引擎探究（`21-A`）。
4. **硬件、纠错、系统与传感路线**：使用[系统与传感实验册](systems.md)，逐层贯通读出告警、加权解码、魔法态调度、量子网络、编译映射、服务可用率与系统条件边界，并完成第 20 章量子传感、Huelga 退相位、原子钟与重力仪分步实验（`S20`）。
5. **统计方法与编译等价性路线**：用[统计与实验方法实验册](practice.md)核查有限样本下界、ZNE 固定总 shots 最优分配、BCa / Cluster Bootstrap、零失败反例、少聚类 $t_{B-1}$ 区间、多重比较与 QCEC 随机态探针。
6. **完整开源 SDK 隔离实跑**：读完核心章节后，按[完整 SDK 实验册](sdk-validation.md)的 11 组端到端工作流（`SDK-01` 至 `SDK-11`），对照 31 个开源项目在隔离环境中的真实输出、上游陷阱与验收边界。

## 全书 26 章三阶动手实验总图谱

下表按章节顺序整合了全书三层难度的本地实验：**一阶**为纯 Python 标准库手算核验；**二阶**为反例诊断、专题进阶与深度数学检验；**三阶**为完整开源 SDK 隔离环境实跑归档。全部一、二阶命令行均在**仓库根目录**运行。

| 章节 | 一阶：入门手算与标准库实验 | 二阶：核心反例与深度核验（含 CLI 命令） | 三阶：完整开源 SDK 实跑 |
|---|---|---|---|
| [00 全景与边界](../00-overview.md) | [F00：1000 次测量为何很少对半](foundations.md#f001000-次测量为何很少恰好对半)（`foundations_lab.py --case 00`） | 重复复制日志、态矢量/密度矩阵字节账与留出预算：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 00`）、[原理展开核验](../../codes/foundations/round71_checks.py)、[校准预算核验](../../codes/foundations/round73_checks.py) | Aer 多模拟表示与同一实验对照（[完整 SDK 实验册](sdk-validation.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [01 零基础数学工具](../01-math.md) | [F01：复共轭内积、外积与换基](foundations.md#f01不取复共轭会把长度算成复数)（`foundations_lab.py --case 01`） | 列归一非酉、被动换基 vs 主动施门、矩阵指数与逆条件数：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 01`）、[原理展开核验](../../codes/foundations/round71_checks.py)、[求逆放大核验](../../codes/foundations/round73_checks.py) | QuTiP 矩阵指数与线性逆条件数对照（[完整 SDK 实验册](sdk-validation.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [02 单量子比特](../02-single-qubit.md) | [F02：$Y$ 基测量门序与相位](foundations.md#f02y-基测量需要先-s再-h)（`foundations_lab.py --case 02`） | 有限层析负本征值、非投影 POVM 后态、不对称读出方差传播：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 02`）、[原理展开核验](../../codes/foundations/round71_checks.py)、[读出反演核验](../../codes/foundations/round73_checks.py) | Qiskit Experiments 态层析与读出反演（[完整 SDK 实验册](sdk-validation.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [03 多量子比特与纠缠](../03-multiple-qubits.md) | [F03：非均匀纠缠偏迹与远端旋转](foundations.md#f03非均匀纠缠态配合远端旋转检查偏迹方向)（`foundations_lab.py --case 03`） | 复相位纠缠轴、复系数 Schmidt 还原、双端错报见证：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 03`）、[原理展开核验](../../codes/foundations/round71_checks.py)、[双端错报核验](../../codes/foundations/round73_checks.py) | Aer 局部阻尼与纠缠衰变核验（[完整 SDK 实验册](sdk-validation.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [04 量子门、电路与协议](../04-circuits-protocols.md) | [F04：隐形传态四分支与复振幅校正](foundations.md#f04传态必须逐支检验复振幅)（`foundations_lab.py --case 04`） | 受控门全局相位变相对相位、纠缠输入传态、反馈读错位：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 04`）、[原理展开核验](../../codes/foundations/round71_checks.py)、[反馈错报核验](../../codes/foundations/round73_checks.py) | Aer 动态测量与含噪经典反馈传态（[完整 SDK 实验册](sdk-validation.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [05 混态、噪声与信道](../05-noise-channels.md) | [F05：振幅阻尼、纯退相位与 $T_1 / T_2$](foundations.md#f05布居与相干有不同时间常数)（`foundations_lab.py --case 05`） | 广义振幅阻尼、信道非交换、全复数 CP+TP 约束与多项 MLE：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 05`）、[原理展开核验](../../codes/foundations/round71_checks.py)、[过程层析核验](../../codes/foundations/round73_checks.py) | Aer 54 组噪声与 Experiments 过程层析（[完整 SDK 实验册](sdk-validation.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [06 量子算法共同骨架](../06-algorithmic-primitives.md) | [06-A：有限相位网格与圆周距离](algorithms.md#实验-06-a有限相位网格与圆周距离)（`experiments.py 06`） | 6 门 PREPARE–SELECT、4 项 QROM、固定点放大、量子计数与补码 QPE：[高阶算法核验实验](algorithms.md#高阶算法与-qsvt-专题核验)（`v4_algorithms_lab.py 06`）、[接口边界核验](../../codes/algorithms/round70_checks.py)、[反计算核验](../../codes/algorithms/round71_checks.py)、[有符号相位核验](../../codes/algorithms/round73_checks.py) | Cirq 可逆预言机与承诺条件核验（[算法基础归档](../../codes/algorithms/round72-README.md)、[算法进阶归档](../../codes/algorithms/sdk73/README.md)） |
| [07 代表性量子算法](../07-algorithms.md) | [07-A：Grover 过度旋转与重试查询账](algorithms.md#实验-07-a逐振幅检查过度旋转)（`experiments.py 07`） | LCHS 耗散核、Carleman 线性化边界、Shor $N=35$、ECDLP、泊松条件数与负谱 HHL：[高阶算法核验实验](algorithms.md#高阶算法与-qsvt-专题核验)（`v4_algorithms_lab.py 07`）、[混叠边界核验](../../codes/algorithms/round70_checks.py)、[满秩与负谱核验](../../codes/algorithms/round73_checks.py) | Cirq 非对角与负谱 HHL、Qiskit Algorithms Grover 与 IAE（[SDK-01](sdk-validation.md)） |
| [08 应用、变分与边界](../08-applications.md) | [08-A：Pauli 分组预算与 QAOA 分布](algorithms.md#实验-08-a测量预算与最优解概率)（`experiments.py 08`） | $\mathrm{H}_2$/SQD 阶梯、$K_3$ 与 WS-QAOA、背包罚项、期权 VaR/CVaR、QNG/DLA 与链式求导：[高阶算法核验实验](algorithms.md#高阶算法与-qsvt-专题核验)（`v4_algorithms_lab.py 08`）、[共享参数梯度核验](../../codes/algorithms/round70_checks.py)、[罚项阈值核验](../../codes/algorithms/round73_checks.py) | OpenFermion 费米映射、PennyLane/Qiskit VQE、SQD（[算法基础归档](../../codes/algorithms/round72-README.md)、[SDK-06](sdk-validation.md)） |
| [09 物理量子比特与控制栈](../09-hardware.md) | [S09：稀有丢失事件与告警精确率](systems.md#s09要让告警至少九成可信误报要压到多少)（`hardware_flags.py`） | 标定方差传播、有限温度被动复位与 $Y$ 故障双检查图：[系统边界核验](systems.md#3-系统条件边界与拓展核验导览)（`calibration_uncertainty.py`）、[模型边界核验](../../codes/systems/round71_checks.py)、[跨库换算核验](../../codes/systems/round73_checks.py) | 噪声参数跨库换算与刺激电路噪声对照（[系统基础归档](../../codes/systems/round72-README.md)、[系统进阶归档](../../codes/systems/sdk73/README.md)） |
| [10 量子纠错与容错计算](../10-error-correction.md) | [S10：非均匀独立噪声下的加权解码](systems.md#s10何时翻第一位与翻后两位一样可信)（`weighted_decoder.py`） | 症状测后相干逻辑误差、Steane 码擦除码距与双基相关匹配：[系统边界核验](systems.md#3-系统条件边界与拓展核验导览)（`coherent_repetition.py`）、[码距边界核验](../../codes/systems/round71_checks.py)、[双基解码复算](../../codes/systems/round73_checks.py) | Stim 电路级表面码采样 + PyMatching 普通与相关匹配解码（[系统基础归档](../../codes/systems/round72-README.md)、[系统进阶归档](../../codes/systems/sdk73/README.md)） |
| [11 资源估算与基准](../11-resources-benchmarks.md) | [S11：魔法态供给、库存与突发消费](systems.md#s11没有库存工厂够快也可能永远做不了下一层)（`factory_schedule.py`） | 批内漂移相关性压缩有效样本、每周期错率与解码耗时分布：[系统边界核验](systems.md#3-系统条件边界与拓展核验导览)（`correlated_shots.py`）、[周期错率核验](../../codes/systems/round71_checks.py)、[配对比较复算](../../codes/systems/round73_checks.py) | 失败置信区间、时间分母与 Qualtran 资源分解（[系统基础归档](../../codes/systems/round72-README.md)、[完整 SDK 总账](sdk-validation.md)） |
| [12 密码、网络与前沿](../12-security-network-frontiers.md) | [S12：两条异速量子链路的等待与存储](systems.md#s12把一条链路做成每轮必成功另一条仍然很慢)（`network_wait.py`） | 存储超时截止权衡、含噪 Bell 交换卷积与先兆过期事件：[系统边界核验](systems.md#3-系统条件边界与拓展核验导览)（`network_cutoff.py`）、[交换卷积核验](../../codes/systems/round71_checks.py)、[先兆过期复算](../../codes/systems/round73_checks.py) | SeQUeNCe 离散事件网络时序仿真 + `liboqs` 三种 ML-KEM 完整构建（[系统基础归档](../../codes/systems/round72-README.md)、[系统进阶归档](../../codes/systems/sdk73/README.md)） |
| [13 量子信息论](../13-quantum-information.md) | [F13：不等先验的 Helstrom 最优判别](foundations.md#f13先验不相等时08536不再是答案)（`foundations_lab.py --case 13`） | 后选择不违背收缩、互信息与阴影纯度偏差：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case 13`）、[互信息核验](../../codes/algorithms/round71_checks.py)、[混态保真核验](../../codes/algorithms/round73_checks.py) | PennyLane 采样非线性插件偏差与熵估对照（[算法基础归档](../../codes/algorithms/round72-README.md)、[算法进阶归档](../../codes/algorithms/sdk73/README.md)） |
| [14 编译、路由与脉冲控制](../14-compilation-control.md) | [S14：省 SWAP 后的输出映射与线路等价](systems.md#s14为什么只检查计算基概率还不够)（`routing_mapping.py`） | 共享控制资源冲突、虚拟 $Z$ 相位等式与三能级泄漏验收：[系统边界核验](systems.md#3-系统条件边界与拓展核验导览)（`resource_schedule.py`）、[相位等式核验](../../codes/systems/round71_checks.py)、[三能级脉冲复算](../../codes/systems/round73_checks.py) | Qiskit 线型编译布局 + `qutip-qtrl` 受约束 GRAPE 与三能级优化（[系统基础归档](../../codes/systems/round72-README.md)、[SDK-03](sdk-validation.md)） |
| [15 动手实践与研究方法](../15-practice-research.md) | [P15-A–G：Bell 下界、ZNE、后选择与切割](practice.md#p15-a同一个-bell-点估计为什么下界不同)（`experiments.py`、`research_checks.py`） | ZNE 固定总 shots 最优分配、BCa/Cluster Bootstrap、$k=0$ 反例、少聚类 $t_{B-1}$ 与 QCEC 探针：[高阶统计与等价性实验](practice.md#p15-hzne-固定总-shots-最优分配与指数偏差)（`v4_practice_lab.py`）、[偷看停止核验](../../codes/systems/round71_checks.py) | Mitiq 零噪声外推、归档独立重建与 SLC / PNA 缓解（[SDK-08](sdk-validation.md)、[SDK-09](sdk-validation.md)） |
| [16 高级算法与可扩展验证](../16-advanced-algorithms-verification.md) | [16-A：Chebyshev 信号多项式与非厄米反例](algorithms.md#实验-16-a信号多项式与非厄米反例)（`experiments.py 16`） | 显式 $4\times 4$ 负谱 QSVT 双约定与相干提取、小成功率放大与超立方体 SKW 行走：[高阶算法核验实验](algorithms.md#高阶算法与-qsvt-专题核验)（`v4_algorithms_lab.py 16`）、[后选择放大核验](../../codes/algorithms/round70_checks.py)、[量子行走核验](../../codes/algorithms/round73_checks.py) | `pyqsp` 对称相位求解、`quimb` 图行走、PennyLane 经典阴影与 Qualtran 块编码（[算法基础归档](../../codes/algorithms/round72-README.md)、[算法进阶归档](../../codes/algorithms/sdk73/README.md)） |
| [17 多元计算模型](../17-computation-models.md) | [17-A：MBQC 前馈校正与退火重试预算](algorithms.md#实验-17-a前馈和退火成功率)（`experiments.py 17`） | 退火链强度简并、回波时间失配与两步适应性 MBQC 四支校正：[退火链强度核验](../../codes/algorithms/round70_checks.py)、[回波相干核验](../../codes/algorithms/round71_checks.py)、[两步 MBQC 核验](../../codes/algorithms/round73_checks.py) | `dimod` QUBO / Ising 符号与穷举谱核验（[算法基础归档](../../codes/algorithms/round72-README.md)、[算法进阶归档](../../codes/algorithms/sdk73/README.md)） |
| [18 信道容量、复杂性与连续变量](../18-channels-capacities-complexity.md) | [18-A：擦除信道四种容量与相干信息网格](algorithms.md#实验-18-a擦除信道的四种任务)（`experiments.py 18`） | 有限块码与容量边界、连续变量协方差与多模排序、Fock 高能尾界：[擦除块码核验](../../codes/algorithms/round70_checks.py)、[高斯协方差核验](../../codes/algorithms/round71_checks.py)、[Fock 尾界核验](../../codes/algorithms/round73_checks.py) | The Walrus 高斯态协方差与光子数概率核验（[算法基础归档](../../codes/algorithms/round72-README.md)、[算法进阶归档](../../codes/algorithms/sdk73/README.md)） |
| [19 工程架构、运维与玻色码](../19-engineering-architecture.md) | [S19：故障区间并集、可用率与合格吞吐](systems.md#s19每秒成功很多却没有一个可用答案)（`service_timeline.py`） | 校准依赖失效传播、同 POVM 不同测后仪器与 QND 区分：[系统边界核验](systems.md#3-系统条件边界与拓展核验导览)（`calibration_dependencies.py`）、[测后仪器核验](../../codes/systems/round71_checks.py)、[队列分离复算](../../codes/systems/round73_checks.py) | pyGSTi 量子仪器重复读数、LGST 与长序列最大似然 GST（[SDK-05](sdk-validation.md)、[SDK-10](sdk-validation.md)） |
| [20 量子传感与精密测量](../20-quantum-sensing-metrology.md) | [S20：CFI/QFI、Huelga 坍塌与 HNLS 判据](systems.md#s20量子传感的-cfiqfihuelga-坍塌与-hnls-纠错判据)（`sensing_lab.py`） | Ramsey 偏置与 Bures 极限、GHZ 丢失与死时间反杀、原子钟阿兰偏差与重力仪 $T^2$ 标度、自旋压缩与 HNLS（[传感分步探究](systems.md#s20量子传感的-cfiqfihuelga-坍塌与-hnls-纠错判据)） | 开放传感基准与论文核查口径见[第 20 章 §8](../20-quantum-sensing-metrology.md)与[附录 F §5.5](../appendices/software-practice.md#55-量子传感评估与经典模拟引擎选型) |
| [21 稳定子与经典模拟引擎](../21-stabilizer-classical-simulation.md) | [21-A：稳定子表、MPS 与含噪 Pauli 传播三引擎](algorithms.md#实验-21-a稳定子表mps-与含噪-pauli-传播三引擎)（`simulation_engines_lab.py`） | 稳定子表 4 比特压测与魔法态展度、MPS SVD 截断与二维 PEPS/BP-TN 环长边界、含噪 Pauli 传播 $p$ 扫描与 $\ell_1$ 界（[三引擎分步探究](algorithms.md#实验-21-a稳定子表mps-与含噪-pauli-传播三引擎)） | Stim 稳定子采样、quimb 张量网络与 `pauli-prop` Rust 扩展实跑（[完整 SDK 总账](sdk-validation.md)） |
| [Q1 实验与量子态](../quantum-mechanics/01-experiments-states.md) | [FQ1：环境重叠的模长与相位移动条纹](foundations.md#fq1环境重叠的相位移动条纹模长改变可见度)（`foundations_lab.py --case q1`） | 不等权与退相干辨析、延迟选择擦除条件条纹与漏检错报区分：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case q1`）、[量子擦除核验](../../codes/foundations/round71_checks.py)、[错报浅条纹核验](../../codes/foundations/round73_checks.py) | 不等探测效率与擦除符合统计核验（[基础实跑说明](../../codes/foundations/round72-README.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [Q2 可观测量与演化](../quantum-mechanics/02-observables-dynamics.md) | [FQ2：脉冲时序与子系统能量零点](foundations.md#fq2子系统整体能量平移仍然只是全局相位)（`foundations_lab.py --case q2`） | 简并测后仪器、Schrödinger 加强不确定界、4096 轨迹主方程对照与时变 RK4 演化：[动力学轨迹实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case q2`）、[加强不确定核验](../../codes/foundations/round71_checks.py)、[时变开放演化核验](../../codes/foundations/round73_checks.py) | QuTiP 主方程与 2048/4096 随机量子轨迹对比（[基础实跑说明](../../codes/foundations/round72-README.md)、[基础实跑归档](../../codes/foundations/sdk73/README.md)） |
| [Q3 能级与物理量子比特](../quantum-mechanics/03-levels-control.md) | [FQ3：热占据、角频率与失谐峰高](foundations.md#fq3同一实验中核对温度频率与时间)（`foundations_lab.py --case q3`） | Rabi 失谐符号不可辨识性、矩形脉冲频谱零点与三维截断非酉：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case q3`）、[脉冲频谱核验](../../codes/systems/round71_checks.py)、[三能级泄漏复算](../../codes/systems/round73_checks.py) | `qutip-qtrl` 三能级泄漏抑制与频域滤波核验（[系统基础归档](../../codes/systems/round72-README.md)、[系统进阶归档](../../codes/systems/sdk73/README.md)） |
| [Q4 波函数与典型模型](../quantum-mechanics/04-wavefunctions-models.md) | [FQ4：连续态网格归一化与二阶收敛](foundations.md#fq4把连续波函数放到网格上时别漏掉根号步长)（`foundations_lab.py --case q4`） | Fock 截断对易子反例、方势垒透射共振与有限截断高能尾界：[基础诊断实验](foundations.md#基础诊断与动力学轨迹实验导览)（`diagnostic_lab.py --case q4`）、[势垒共振核验](../../codes/algorithms/round71_checks.py)、[截断尾界核验](../../codes/algorithms/round73_checks.py) | The Walrus 高斯态与连续态数值对照（[算法基础归档](../../codes/algorithms/round72-README.md)、[算法进阶归档](../../codes/algorithms/sdk73/README.md)） |

## 跨章软件工作流与交互实验台

除了逐章实验外，手册还提供三类横向动手入口：

- **6 模块离线交互量子实验台**：双击或直接打开[离线交互量子实验台](../../reader/lab/quantum-lab.html)，覆盖 MZI 干涉与密度矩阵、Bloch 球真弧沙盒、Ramsey 退相干与 Fisher 灵敏度对比、Bell 偏迹与 CHSH 博弈、Grover 半拍放大与 $d=3$ 表面码注错解码，零外网依赖。
- **软件工作流带解练习（`W1–W6`）与源码精读核验（`S04–S08`）**：见[算法、工业实践与开源对照](../appendices/software-practice.md)，连接多乘积公式、可观测量反向传播、含噪 Pauli 伴随、子空间对角化、并行随机数与过程层析；运行 `python3 codes/practice/workflow_checks.py` 与 [源码精读校验程序](../../codes/practice/source_reading_checks.py) 即可离线复算全部标准库小模型。
- **端到端开源 SDK 工作流（`SDK-01` 至 `SDK-11`）**：见[完整 SDK 实验册](sdk-validation.md)，汇总 **31 个开源项目（对应 122 份固定提交源码）** 的真实版本、运行日志、复现的上游陷阱与独立反例。

## 运行方式与结果

本册全部自编教学与核验程序均仅依赖 Python 3.9 及以上标准库，默认不请求云服务、不消耗付费额度。运行测试时**不要加 `-O`**（否则会关闭断言）。绘图程序另需指定版本的 Matplotlib 与 NumPy；不重画图就无需安装它们。

在**仓库根目录**运行统一入口，即可一键执行全部 **38 项**标准库验证脚本（已内置 `v4_algorithms_lab.py`、`v4_practice_lab.py`、`sensing_lab.py` 与 `simulation_engines_lab.py`，无需跑完再重复手跑），并同步校验 122 份第三方源码 SHA-256：

```sh
python3 codes/run_all.py
```

若只想单独复算某一专题（如高阶算法、统计重采样、量子传感或经典模拟三引擎），也可直接单独执行对应脚本：

```sh
python3 codes/algorithms/v4_algorithms_lab.py all
python3 codes/practice/v4_practice_lab.py
python3 codes/systems/sensing_lab.py
python3 codes/algorithms/simulation_engines_lab.py
```

分章运行方式、预期输出与依赖清单见[代码总说明](../../codes/README.md)。程序通过断言说明数值实现与明示模型自洽；小规模算例不能替代一般定理证明或真实硬件实验。完整开源 SDK 须在各自隔离虚拟环境中按锁定版本运行，不与默认标准库入口混跑。

## 如何把练习改成自己的研究

一次只改变一个因素：先把初态换成含非零复相位的态，再引入噪声或读出偏差，最后逐步扩大系统规模。记录解析断言在何处继续成立、在何处开始越出模型前提——一个精准定位失效边界的反例，往往比只贴一张漂亮的成功曲线更有研究价值。

迈向真实硬件实验时，还须同步保存软件依赖锁、编译布局与硬件校准快照、完整原始计数、采集时序与端到端机时预算。

## 归档校验与可追溯说明

为保持仓库历史 Git 提交、验证日志与数据文件 SHA-256 校验链的完整可追溯性，`codes/` 目录下的部分底层核验脚本与隔离环境归档文件夹保留其原始文件路径，不作重命名或篡改；其全部数学推导与反例结论均已按主题自然编入正文与各分册实验手册。如需查阅完整隔离环境的原始安装锁与运行日志，可直接进入四组专题档案：[基础 SDK 归档](../../codes/foundations/sdk73/README.md)、[算法 SDK 归档](../../codes/algorithms/sdk73/README.md)、[系统 SDK 归档](../../codes/systems/sdk73/README.md)与[进阶集成工作流归档](../../codes/sdk/round73/README.md)。
