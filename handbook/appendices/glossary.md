# 术语表

本表按主题汇编全书核心物理、算法、纠错、密码、编译与系统工程术语。每个词条力求一句话讲清直觉，再补上精确定义和最常见的误解边界。

## 1. 量子力学基础术语

**双缝干涉与延迟选择量子擦除（double-slit interference & delayed-choice quantum eraser）**：单个粒子依次通过双缝后，两条路径的复振幅相干叠加形成明暗条纹；只要任何环境自由度记录了路径信息，即便没人读取，两条路径变得正交、条纹就会按 Englert 对偶 $\mathcal V^2 + D^2 \le 1$ 消失。量子擦除是在互补基下对路径标记做后选择，从总分布中分拣出两套互补子条纹；总屏幕分布始终不变，既无超光速传信也无逆因果。见 [Q1](../quantum-mechanics/01-experiments-states.md)。

**Born 规则**：把量子态与测量概率联系起来的物理公设。对归一化纯态和秩一投影，结果概率等于投影振幅的模平方；一般 POVM 测量写为 $p_m = \operatorname{Tr}(\rho E_m)$。

**可观测量与本征值**：有限维投影测量模型中，物理可观测量由厄米算符表示。单次测量只能读出它的某一个本征值；期望值是相同制备下多次重复测量的概率加权平均，未必等于某次单次读数。

**态制备不确定关系**：限制同一量子态上两个不对易可观测量分布宽度的基本界限。Robertson 形式为 $\Delta A\,\Delta B \ge \lvert\langle[A,B]\rangle\rvert/2$，Schrödinger 形式还包含对称协方差项；它刻画的是量子态本身的内禀分布宽度，而非仪器粗糙或测量扰动。见 [Q2](../quantum-mechanics/02-observables-dynamics.md)。

**定态**：不随时间变化的哈密顿量的能量本征态。随时间演化时它只积累全局相位，因此任何不显含时间的可观测量统计都保持不变；不同能量本征态的叠加才会产生真实振荡。

**Rabi 振荡**：受周期外场驱动的两能级系统中，占据概率随时间周期性翻转的现象。在共振、恒幅、旋波近似且忽略耗散时，从 $\lvert 0\rangle$ 出发有 $p_1(t) = \sin^2(\Omega t/2)$；换算门时长时必须分清角频率 $\Omega$（$\mathrm{rad/s}$）与普通频率 $\Omega/(2\pi)$（$\mathrm{Hz}$）。见 [Q3](../quantum-mechanics/03-levels-control.md)。

**旋波近似（RWA）**：在随驱动频率旋转的坐标系中，忽略相对于目标演化振荡极快的反旋转项。通常要求驱动强度与失谐均远小于载频（可通过 Bloch–Siegert 频移检验误差）。

**非谐性（anharmonicity）**：多能级系统相邻跃迁频率不相等的性质（如超导 transmon 中 $\alpha = \omega_{12} - \omega_{01} \ne 0$）。足够大的非谐性允许用特定频率脉冲单独寻址 $\lvert 0\rangle \leftrightarrow \lvert 1\rangle$，同时抑制向 $\lvert 2\rangle$ 能级的泄漏。

**波函数与概率密度**：量子态在连续位置表象中的复振幅 $\psi(x) = \langle x\vert\psi\rangle$。一维中 $\lvert\psi(x)\rvert^2 dx$ 给出粒子落在微小区间 $[x, x+dx]$ 内的概率，概率密度本身带有长度倒数量纲，不是单个点的概率。见 [Q4](../quantum-mechanics/04-wavefunctions-models.md)。

**零点能**：束缚量子系统基态相对于势能最低点的剩余能量（一维谐振子为 $\hbar\omega/2$），源于位置与动量不能同时无限压窄的不确定关系，不可被提取为无限能源。

**量子隧穿**：波函数穿过经典能量不足以越过的势垒而在另一侧产生非零透射概率的现象。定态散射过程中总能量严格守恒，无需用“暂时向自然界借能量”解释。

## 2. 量子计算、线路与信息基础术语

**复共轭与模平方**：对 $z = a + bi$，共轭为 $z^* = a - bi$，模平方为 $\lvert z\rvert^2 = z^* z = a^2 + b^2$。量子概率一律用模平方计算，不把复振幅直接普通平方。

**bra、ket 与左共轭内积**：ket $\lvert v\rangle$ 是列向量；bra $\langle v\rvert$ 是其逐项共轭转置的行向量。内积 $\langle u\vert v\rangle = \sum_j u_j^* v_j$ 对左侧向量取共轭，$\langle v\vert v\rangle$ 为向量长度的平方。

**振幅（amplitude）**：态矢量在给定正交归一基方向上的复数系数；复相位决定干涉相长还是相消，模平方给出测量概率。

**张量积**：把两个子系统按约定顺序（全书默认高位在左）合成联合希尔伯特空间的运算。对两分量列向量 $[a_0, a_1]^T$ 与 $[b_0, b_1]^T$，按 $00,01,10,11$ 排序得到 $[a_0 b_0, a_0 b_1, a_1 b_0, a_1 b_1]^T$。

**全局相位与相对相位**：给整个纯态同乘 $e^{i\gamma}$ 是全局相位，不影响任何测量概率；改变不同基分量之间的相位差是相对相位，换基或干涉后会直接改变输出概率。

**Bloch 球**：把单比特密度矩阵写成 $\rho = (I + r_x X + r_y Y + r_z Z)/2$ 时，三维坐标 $\vec r = (r_x, r_y, r_z)$ 落在单位实心球内（$\lvert\vec r\rvert \le 1$）。纯态位于球面，混态位于球内，球心对应最大混态 $I/2$。见[第 02 章](../02-single-qubit.md)与[第 05 章](../05-noise-channels.md)。

**叠加（superposition）**：量子态在希尔伯特空间中的复线性组合，携带可干涉的相对相位，不同于经典概率混合。

**纠缠（entanglement）**：若复合态不能写成各子系统乘积态的凸组合（概率混合），则为纠缠态。对纯态，这等价于不能分解为 $\lvert\psi_A\rangle \otimes \lvert\psi_B\rangle$，且其约化密度矩阵为混态。见[第 03 章](../03-multiple-qubits.md)。

**CHSH 博弈（CHSH game）**：用双人合作博弈直观呈现 Bell 不等式的方法。Alice 与 Bob 各自收到随机比特 $x,y$，须在互不通信的前提下输出 $a,b$ 使 $a \oplus b = x \cdot y$。任何经典局域隐变量策略胜率上限为 $75\%$（对应 $S \le 2$），共享 Bell 态的量子策略可达 $\cos^2(\pi/8) \approx 85.4\%$（对应 Tsirelson 界 $S = 2\sqrt{2}$）。见[第 03 章](../03-multiple-qubits.md)。

**相干（coherence）**：不同基态分量之间可参与量子干涉的稳定相位关系；在指定基下体现为密度矩阵的非对角元。

**量子门（quantum gate）**：理想封闭量子系统中由酉算符表示的可逆演化操作。

**Toffoli 门（CCNOT 门）**：三比特双控非门，当且仅当两个控制比特都为 $\lvert 1\rangle$ 时翻转目标比特。它是经典可逆计算的通用门，加入 Hadamard 门即可实现量子计算的实数通用门集。见[第 04 章](../04-circuits-protocols.md)。

**延迟测量原理（principle of deferred measurement）**：量子线路中任何“中途测量并根据经典结果触发后续量子门”的操作，在输出统计上都等价于把经典控制改为受控量子门、将所有测量推迟到电路最末端执行。见[第 04 章](../04-circuits-protocols.md)。

**哈密顿量（Hamiltonian）**：描述封闭量子系统能量并生成时间演化的厄米算符。时间无关时演化算符为 $e^{-i\mathcal H t/\hbar}$；一般时变情形须保留时间排序。

**密度矩阵与纯度**：密度矩阵 $\rho$ 统一描述纯态 $\lvert\psi\rangle\langle\psi\rvert$ 与经典统计混态，满足厄米、正半定、迹为 1。纯度 $\operatorname{Tr}(\rho^2)$ 对纯态为 $1$，对 $d$ 维最大混态为 $1/d$。

**投影测量、POVM 与量子仪器（quantum instrument，亦称量子测量工具）**：投影测量用两两正交的投影算符 $\{P_m\}$ 给出概率 $p_m = \operatorname{Tr}(\rho P_m)$ 与 Lüders 条件后态 $P_m \rho P_m / p_m$；POVM 放宽为任意满足 $\sum_m E_m = I$ 的正半定算符 $\{E_m\}$，只规定结果概率而不单独决定测后态；量子仪器（亦称量子测量工具）则用一组完全正、迹不增映射 $\{\mathcal I_m\}$ 同时刻画结果概率 $\operatorname{Tr}\mathcal I_m(\rho)$ 与测后状态更新。见[第 02 章](../02-single-qubit.md)与[第 05 章](../05-noise-channels.md)。

**条件后态与非选择后态**：已知测量结果为 $m$ 且 $p_m > 0$ 时，归一化得到的分支状态 $\rho_m = \mathcal I_m(\rho)/p_m$ 称为条件后态；测量已发生但忽略或未记录结果时，按概率加权合并的状态 $\sum_m \mathcal I_m(\rho)$ 称为非选择后态。

**量子信道与 Kraus 算符**：描述开放系统确定性演化的完全正、保迹（CPTP）线性映射 $\mathcal E$。写成算符和 $\mathcal E(\rho) = \sum_k K_k \rho K_k^\dagger$ 时，$K_k$ 称为 Kraus 算符，满足 $\sum_k K_k^\dagger K_k = I$；同一信道的 Kraus 分解在酉等价下不唯一。

**退相干（decoherence）**：系统与环境发生纠缠导致量子相干性（密度矩阵非对角元）衰减的物理过程；它包含纯退相位，也受能量弛豫限制，但并非全部硬件噪声（如控制串扰、读出误判）的同义词。

**纯化（purification）**：把任意混态 $\rho_A$ 写成更大希尔伯特空间上某个纯态 $\lvert\Psi\rangle_{RA}$ 的约化态 $\rho_A = \operatorname{Tr}_R(\lvert\Psi\rangle\langle\Psi\rvert_{RA})$；不同纯化之间相差参考系统 $R$ 上的等距变换。

**Choi 矩阵**：将未归一化最大纠缠态 $\lvert\Omega\rangle\langle\Omega\rvert$ 的一半送入线性映射 $\mathcal E$ 得到的二分算符 $J_{\mathcal E} = (\mathcal I \otimes \mathcal E)(\lvert\Omega\rangle\langle\Omega\rvert)$。$J_{\mathcal E} \succeq 0$ 等价于 $\mathcal E$ 完全正，$\operatorname{Tr}_B J_{\mathcal E} = I$ 等价于保迹。见[第 18 章](../18-channels-capacities-complexity.md)。

**钻石范数（diamond norm，亦称完全有界迹范数）**：衡量两条量子信道最坏情况可区分度的标准距离，$\lVert\mathcal E - \mathcal F\rVert_\diamond = \sup_{\rho_{RA}} \lVert ((\mathcal E - \mathcal F) \otimes \mathcal I_R)(\rho_{RA}) \rVert_1$。它显式计入辅助纠缠参考系统 $R$，满足对线路串联的次可加性，是容错阈值分析的标准度量。见[第 18 章](../18-channels-capacities-complexity.md)。

**Shannon 熵与 von Neumann 熵**：经典分布的 Shannon 熵为 $H(X) = -\sum_x p(x)\log_2 p(x)$（约定 $0\log_2 0 = 0$）；量子态的 von Neumann 熵为其密度矩阵本征值的 Shannon 熵，$S(\rho) = -\operatorname{Tr}(\rho\log_2 \rho)$。见[第 13 章](../13-quantum-information.md)。

**量子互信息与量子状态合并（quantum state merging）**：二分态量子互信息为 $I(A:B) = S(A) + S(B) - S(AB)$，衡量经典与量子总相关。条件熵 $S(A\mid B) = S(AB) - S(B)$ 在量子信息中可为负值，量子状态合并定理赋予其精确操作意义：当 $S(A\mid B) > 0$ 时，把 $A$ 合并给持有 $B$ 的接收方需消耗每副本 $S(A\mid B)$ 对纠缠；当 $S(A\mid B) < 0$ 时，合并过程反而净产出 $\lvert S(A\mid B)\rvert$ 对可用 Bell 纠缠。见[第 13 章](../13-quantum-information.md)。

**迹距离、根保真度与平均门保真度**：迹距离 $T(\rho,\sigma) = \lVert\rho - \sigma\rVert_1 / 2$ 刻画最优单次态判别成功率；本书态保真度统一采用根保真度 $F(\rho,\sigma) = \lVert\sqrt\rho\sqrt\sigma\rVert_1$（纯态间为 $\lvert\langle\psi\vert\phi\rangle\rvert$）；平均门保真度 $F_{\mathrm{avg}}$ 则对所有纯输入态按 Haar 分布平均**平方**重叠，因此 $1 - F_{\mathrm{avg}}$ 不能随手改写成 $1 - F$。

**Holevo 量、可访问信息与无歧义判别（IDP）**：对量子态系综 $\{p_x, \rho_x\}$，Holevo 量 $\chi = S(\sum_x p_x \rho_x) - \sum_x p_x S(\rho_x)$ 给出任意测量所能提取的经典互信息（可访问信息 $I_{\mathrm{acc}}$）的普适上界。无歧义判别允许输出“无法判定”，一旦给出确定标签则要求零错误，比较成功率时须把放弃轮次计入总分母。见[第 13 章](../13-quantum-information.md)。

**局域操作与经典通信（LOCC）与负性（negativity）**：LOCC 指各方仅在本地操控自己的量子系统并交换经典通信，它是纠缠资源理论中的标准免费操作。负性 $\mathcal N(\rho) = (\lVert\rho^{T_B}\rVert_1 - 1)/2$ 与对数负性 $E_N(\rho) = \log_2(1 + 2\mathcal N(\rho))$ 是基于部分转置的可计算纠缠单调量，给出可蒸馏纠缠上界，但在高维系统中无法检出 PPT 束缚纠缠态。见[第 18 章](../18-channels-capacities-complexity.md)。

**相干信息、互补信道与信道容量**：相干信息 $I_c(\rho,\mathcal E) = S(B) - S(RB)$ 正则化后决定量子容量 $Q$；互补信道把输入映向 Stinespring 扩张中的环境输出，用于分析私密容量 $P$。信道容量随传输任务与免费辅助资源不同分为无辅助经典容量 $C$、量子容量 $Q$、私密经典容量 $P$ 与纠缠辅助经典容量 $C_E$。

**高斯态（Gaussian state）与 Wigner 准概率函数**：连续变量系统中由一阶矩和协方差矩阵完全刻画的态称为高斯态。Wigner 函数 $W(q,p)$ 是量子态在相空间中的实值准概率分布，其边缘积分还原位置与动量概率密度；对纯态，非高斯态必然出现 $W(q,p) < 0$ 的负值区（Hudson 定理），Wigner 负性是连续变量超越经典高效蒙特卡洛模拟的必要非经典资源。见[第 18 章](../18-channels-capacities-complexity.md)。

## 3. 算法、复杂度与前沿计算模型术语

**预言机（oracle）**：算法查询模型中封装特定函数或判定规则的可逆黑箱。查询复杂度只计算调用预言机的次数，门复杂度才计算实现它所需的基本量子门数；两者不可混为一谈。

**桶队 QRAM（Bucket-Brigade QRAM）**：将 $N$ 条经典数据以二叉树路由开关组织起来，按地址寄存器比特逐层激活从根到叶的一条路径，从而在单次查询中只让 $O(\log_2 N)$ 个开关处于活跃态的量子随机访问存储器架构。它虽显著压低了传统扇出结构的退相干暴露，但仍面临主动容错硬件机会成本与被动噪声累积瓶颈；现实容错资源估算中常以可编译 QROM 或 SelectSwap 电路替代。见[第 06 章](../06-algorithmic-primitives.md)。

**相位回踢（phase kickback，亦译相位回传）**：当目标寄存器处于酉算符的本征态时，受控操作把本征值的相位写回控制寄存器的相对相位上，而目标态保持不变。它是 Deutsch–Jozsa、QPE 与 Shor 等核心算法的共同引擎。

**量子傅里叶变换（QFT）与量子相位估计（QPE）**：QFT 是离散傅里叶变换的酉实现，可在多项式门数内作用于振幅空间，但单次测量只返回一个比特串而非整张频谱表。QPE 结合受控幂 $U^{2^k}$ 与逆 QFT，把本征值相位 $e^{2\pi i\phi}$ 编码到控制寄存器读出。见[第 06 章](../06-algorithmic-primitives.md)。

**块编码（block encoding）、QSP、QSVT 与 GQSP**：块编码把非酉矩阵 $A$ 缩放后嵌进更大酉矩阵 $U$ 的左上子块（$(\langle 0\rvert\otimes I)U(\lvert 0\rangle\otimes I) = A/\alpha$）。量子信号处理（QSP）与量子奇异值变换（QSVT）通过交替施加信号算符与相位旋转，把多数主流算法统一到对奇异值施加多项式变换的框架下。2024 年提出的广义量子信号处理（GQSP）将单轴 $Z$ 旋转推广为任意 $SU(2)$ 单比特门，彻底取消了传统 QSP 的奇偶性约束，可一步合成任意满足 $\lvert P(e^{i\theta})\rvert \le 1$ 的复多项式。见[第 16 章](../16-advanced-algorithms-verification.md)。

**去量子化（dequantization，亦译反量子化）**：指在赋予经典算法与量子输入模型对等的 $\ell_2$ 范数采样—查询数据结构后，经典随机算法能够以仅多出多项式因子开销的方式复现原本被宣称具有指数加速的量子算法（代表性工作见 Tang 2019、Chia 等 2022 对低秩推荐与低秩线性代数的去量子化）。它专门用来检验“加速究竟来自量子计算还是来自强输入假设”，并不能攻破高秩、稀疏、良条件的 BQP 完备线性系统或量子物理模拟。见[第 07 章](../07-algorithms.md)。

**连续时间量子行走（CTQW）**：在图生成元（如邻接矩阵或拉普拉斯矩阵）$H$ 下按 $e^{-iHt}$ 演化顶点振幅的无硬币量子行走，与离散硬币行走及 MNRS 马尔可夫链搜索模型不同。见[第 16 章](../16-advanced-algorithms-verification.md)。

**稳定子表（Tableau）与 Gottesman–Knill 定理**：Aaronson–Gottesman 稳定子表用 $2n\times(2n+1)$ 二元辛矩阵（每行编码 $(x\mid z)\in\mathbb{F}_2^{2n}$ 与相位位 $r\in\mathbb{F}_2$，上半区存去稳定子、下半区存稳定子）追踪 $n$-比特稳定子态的演化。Gottesman–Knill 定理表明，仅由计算基初态、Clifford 门（$\{H, S, \mathrm{CNOT}\}$）、Pauli 测量与经典前馈构成的线路可在经典计算机上以 $O(n^2)$ 空间与多项式时间精确模拟；这说明高度纠缠本身并不足以带来经典难模拟性。见[第 04 章](../04-circuits-protocols.md)与[第 21 章](../21-stabilizer-classical-simulation.md)。

**魔术度（magic / non-stabilizerness）与稳定子秩**：刻画量子态或门操作偏离稳定子态集合（及其凸包）的非 Clifford 资源，典型来源是 $T$ 门与非 Clifford 旋转；若一个 $T$ 门作用在 $Z$ 本征态上则不产生魔术度。把纯态写成最少个数稳定子态线性叠加的项数称为精确稳定子秩 $\chi_{\mathrm{stab}}$（第 21 章亦简记 $\chi_S$），系数的最小 $\ell_1$ 范数平方称为稳定子展度 $\xi$，二者共同决定扩展稳定子经典模拟随 $T$ 门数目的指数标度。见[第 21 章](../21-stabilizer-classical-simulation.md)。

**矩阵乘积态（MPS）与键维（bond dimension）**：把一维链上 $n$-比特纯态的 $2^n$ 维振幅张量通过逐键奇异值分解（SVD）因式分解为 $n$ 个局域三阶张量的连乘，相邻张量间收缩的虚拟指标最大维数称为键维 $\chi$。只要跨切面纠缠熵满足一维面积律，存储量即可从 $O(2^n)$ 降至 $O(n\chi^2)$；将单键截断至前 $\chi'$ 个奇异值时，平方误差 $\epsilon_{\mathrm{trunc}} = \sum_{i>\chi'}\sigma_i^2 = 1 - F^2$，但在深度大、体积律纠缠的二维线路中 $\chi$ 会指数暴涨。见[第 21 章](../21-stabilizer-classical-simulation.md)。

**Pauli 传播（Pauli propagation / 稀疏 Pauli 动力学 SPD）**：在 Heisenberg 绘景下把待测可观测量沿线路反向逐层展开为稀疏 Pauli 串之和 $\sum_P c_P P$，并按系数幅值或 Pauli 权重 $w(P)$ 截断微小项的经典模拟引擎。局域退极化噪声的伴随映射按 $(1-p)^{w(P)}$ 指数压制高权重串，且截断引入的期望值误差受舍弃系数 $\ell_1$ 范数严格上界控制；它已成为评估含噪或浅中深度百比特线路是否可被经典高效模拟的核心支柱之一。见[第 16 章](../16-advanced-algorithms-verification.md)、[第 21 章](../21-stabilizer-classical-simulation.md)与[开源实践对照](software-practice.md)。

**gflow 与 Pauli flow**：基于测量的量子计算（MBQC）中，决定簇态/图态上按什么偏序执行自适应前馈测量、从而以概率 1 实现确定性酉演化的图论结构条件。gflow 刻画赤道平面固定测量角下的确定性条件，Pauli flow 进一步允许测量平面包含 Pauli 固定角。见[第 17 章](../17-computation-models.md)。

**拓扑量子计算与任意子编织（Ising / Fibonacci）**：利用二维拓扑有序态中非阿贝尔任意子融合子空间的全局拓扑简并来编码逻辑量子比特，并通过绝热交换（编织）任意子世界线执行逻辑门的计算模型；由于逻辑信息非局域分布且受能隙保护，对局域微扰具有内禀抗噪性。Ising 任意子的编织群仅能生成有限 Clifford 门，要实现通用计算仍须借助非拓扑魔法态注入；Fibonacci 任意子（融合规则 $\tau\times\tau = 1 + \tau$）的编织表示在 $\mathrm{SU}(2)$ 中稠密，原则上仅靠编织即可实现通用量子计算。见[第 17 章](../17-computation-models.md)。

**QCMA、QMA、QIP 与 `MIP*=RE`**：QCMA 与 QMA 均由多项式时间量子验证者核对见证（前者见证为经典比特串，后者为量子态）；QIP 是单证明者量子交互式证明，满足 $\mathrm{QIP} = \mathrm{PSPACE}$；`MIP*=RE` 定理（2020/2021）证明允许多个互不通信的证明者共享任意量子纠缠时，可验证的语言类扩张至全部递归可枚举语言（包含停机问题），同时否定了 Connes 嵌入猜想。见[第 18 章](../18-channels-capacities-complexity.md)。

**通信复杂度（communication complexity）**：在各方本地计算免费的分布式模型下，完成联合任务最少须交换的经典比特或量子比特数（如同时消息模型下的量子指纹问题）。

**量子优势（quantum advantage）**：在明确规定的任务、误差容忍度、经典基线与资源口径下，量子方案优于已知最强经典方法。理论复杂度分离与现实设备墙钟时间加速须分开评估。

## 4. 硬件、纠错、密码与系统工程术语

**NISQ**：噪声中等规模量子设备阶段，核心特征是物理噪声仍限制可用线路深度，尚未建成大规模通用容错计算。

**Fluxonium 量子比特**：由小约瑟夫森结并联高电感超电感（superinductor）构成的磁通型超导量子比特。相较 transmon，它拥有高得多的非谐性（数 GHz 级）与更强的电荷/低频磁通免疫能力，单比特相干时间已突破毫秒量级，但低频读出与高保真双比特耦合设计更具挑战。见[第 09 章](../09-hardware.md)。

**物理量子比特与逻辑量子比特**：前者是硬件直接操控的物理二能级自由度；后者是由量子纠错码编码在多颗物理比特上、由纠错症状监测与容错操作保护的算法级量子比特。（在编译器语境下，“逻辑/虚拟比特”有时指尚未映射到芯片坐标的抽象线路线，阅读时需看上下文。）

**稳定子（stabilizer）、码距（code distance）与纠错症状（syndrome）**：稳定子是保持码空间不变的一组两两对易 Pauli 算符；测量它们的本征值即得到纠错症状，可在不泄露逻辑振幅的前提下定位错误。码距 $d$ 是触发非平凡逻辑作用且不被稳定子检出的最小 Pauli 权重，对未知位置错误与已知擦除满足联合纠错界 $2t + e < d$。见[第 10 章](../10-error-correction.md)。

**解码（Decoding，部分工程文献亦称译码）**：根据多轮纠错症状或探测事件图，利用经典算法（如最小权重完美匹配 MWPM、Union-Find、置信传播加有序统计 BP+OSD 等）推断最可能发生的物理错误等价类并输出 Pauli 帧修正的过程。在容错计算中，解码吞吐与尾延迟必须快于物理纠错周期，否则待处理症状积压会引发逻辑错误率雪崩。见[第 10 章](../10-error-correction.md)与[第 11 章](../11-resources-benchmarks.md)。

**五比特完美码（$[[5,1,3]]$ code）**：用 5 个物理比特编码 1 个逻辑比特、可纠正任意单比特 Pauli 错误的最小量子纠错码，精确饱和量子 Hamming 界。见[第 10 章](../10-error-correction.md)。

**晶格手术（lattice surgery）**：在二维近邻平面芯片上，通过临时合并与拆分相邻表面码补丁的边界稳定子测量，实现容错逻辑 CNOT 与多比特 Pauli 联合测量的主流方案，避免了跨芯片长程物理布线。见[第 10 章](../10-error-correction.md)。

**二元双循环（Bivariate Bicycle）qLDPC 码 / Gross 码**：高编码率量子低密度奇偶校验（qLDPC）码的代表家族，其中 IBM Gross 码为 $[[144, 12, 12]]$ 码（含辅助校验位共 288 物理比特编码 12 个码距 12 逻辑比特），阈值接近表面码但比特开销降低约一个量级，代价是每个比特需要度为 6 的非近邻长程连接。见[第 09 章](../09-hardware.md)与[第 10 章](../10-error-correction.md)。

**容错（fault tolerance）、阈值（threshold）与逻辑错误率**：容错要求单点物理故障不会经由门操作扩散成超出纠错码能力的错误风暴；阈值指物理错误率低于某一临界值后，增大码距可指数压低逻辑错误率。报告逻辑错误率时须标明按轮、按逻辑门还是按整段线路统计。

**Clifford 门、魔法态（magic state）与魔法态培育（magic state cultivation, MSC）**：Clifford 门将 Pauli 算符共轭为 Pauli 算符，单靠它们可高效经典模拟；通用容错计算还需注入非 Clifford 魔法态（如 $\lvert T\rangle$）。传统方案依赖占芯片面积巨大的魔法态蒸馏工厂；2024 年提出并于 2026 年在超导芯片上实证的魔法态培育（MSC）结合紧凑编码、逐步后选择筛选与表面码嫁接，把高保真逻辑 $\lvert T\rangle$ 态的时空开销压近单次晶格手术 CNOT。见[第 10 章](../10-error-correction.md)。

**耗散猫比特（dissipative cat qubit）**：把逻辑态编码在超导谐振腔的两个相反相干态 $\lvert\pm\alpha\rangle$ 中，并借助工程化双光子耗散稳定态流形的玻色量子比特。随平均光子数 $\lvert\alpha\rvert^2$ 增大，位翻转率指数下降而相位翻转率仅线性增长，形成强噪声偏置，从而可用外层一维重复码大幅节省纠错硬件。见[第 19 章](../19-engineering-architecture.md)。

**GKP 码（Gottesman–Kitaev–Preskill 网格码）**：将二维逻辑量子比特嵌入连续变量谐振子相空间网格态的玻色纠错码。在无量纲约定 $[\hat q,\hat p]=i$ 下，方形 GKP 码取位移稳定子 $S_q = e^{i2\sqrt\pi\hat q}$ 与 $S_p = e^{-i2\sqrt\pi\hat p}$，二者对易相因子为 $e^{4\pi i}=1$、围出面积 $4\pi$ 的相空间晶胞，可纠正幅值小于 $\sqrt\pi/2$ 的小位移误差；实际物理态须加高斯包络以保证有限能量，且其逻辑纠错能力依赖非高斯 Wigner 负性。见[第 18 章](../18-channels-capacities-complexity.md)。

**擦除（erasure）、泄漏（leakage）与损失（loss）**：泄漏指量子态逃出计算子空间（如跃迁至 $\lvert 2\rangle$）；损失指承载信息的原子或光子消失；擦除指错误位置已被可靠标志告知、但原信息未知。被及时探测的泄漏或损失可转化为擦除，使码距 $d$ 的纠错容量从 $\lfloor(d-1)/2\rfloor$ 提升至 $d - 1$。

**探测事件（detector event）与合并校验（supercheck）**：多轮纠错中相邻轮次校验结果发生跳变的时空节点称为探测事件，构成解码图的顶点；当某颗物理比特失效或丢失时，将其周围若干稳定子相乘消去该比特依赖所构成的新校验称为合并校验。

**每层门错误率与层保真度（EPLG & layer fidelity）**：面向百比特级处理器的并行系统基准。在一维比特链上同步施加整层并行双比特门，通过随机基准测量全链的层保真度（LF），再按边数几何平均折算为每层单个双比特门的等效错误率（EPLG），能真实暴露并行串扰。见[第 11 章](../11-resources-benchmarks.md)。

**后量子密码（PQC）与 HQC**：运行在经典计算机上、旨在抵御经典与量子攻击的密码算法体系。NIST 于 2024 年 8 月正式发布 FIPS 203（ML-KEM）、FIPS 204（ML-DSA）与 FIPS 205（SLH-DSA）三项格基与哈希基标准，并于 2025 年 3 月选定基于纠错码的 HQC（Hamming Quasi-Cyclic）作为 ML-KEM 的备份密钥封装标准候选。见[第 12 章](../12-security-network-frontiers.md)。

**隐式拒绝（implicit rejection）**：ML-KEM（FIPS 203）等密钥封装机制的安全设计：当解封装收到篡改密文时，仍按确定规则导出一个伪随机替代共享密钥而非直接报错，防止通过错误神谕泄露私钥信息；因此解封装返回成功本身不代替身份认证与密钥确认。见[第 12 章](../12-security-network-frontiers.md)。

**QKD、BB84、E91、QBER、信息协调与隐私放大**：量子密钥分发（QKD）利用量子态不可克隆或纠缠违背 Bell 不等式建立共享对称密钥，典型协议包括制备—测量型 BB84 与基于纠缠和 CHSH 检验的 E91 协议。量子比特错误率（QBER）是抽样比对出的比特不一致比例；随后通过经典信息协调纠错、并按安全界做隐私放大压缩出最终安全密钥。见[第 12 章](../12-security-network-frontiers.md)。

**成功先兆（herald）**：远程纠缠或概率性光子门中，由特定探测器点击或 Bell 测量结果给出的经典成功标志，可在不读取所承载未知量子信息的前提下确认操作成功。

## 5. 编译、脉冲控制与实验统计术语

**指令集架构（ISA）、布局与路由（SABRE / LightSABRE）**：ISA 规定芯片原生支持的门、测量、复位、拓扑连接与控制流约束。布局与路由负责把抽象线路比特映射到物理位置并插入 SWAP 满足连通性；SABRE 及其 Rust 加速改进版 LightSABRE 是当前主流的双向启发式路由算法。见[第 14 章](../14-compilation-control.md)。

**Weyl 室（Weyl chamber）与 KAK 分解（Cartan decomposition）**：任意两比特特殊酉门 $U\in\mathrm{SU}(4)$ 均可分解为前后两层局域单比特门夹住一个三参数非局域典型门 $\exp[i(k_x X\!\otimes\!X + k_y Y\!\otimes\!Y + k_z Z\!\otimes\!Z)]$，这就是 KAK（Cartan）分解。去除局域等价冗余后，参数 $(k_x,k_y,k_z)$ 落在名为 Weyl 室的四面体内，从而给出精确的最小双比特门综合判据——任意两比特门至多需要 3 个 $\mathrm{CNOT}$，底面 $k_z=0$ 上的门（如 $\mathrm{iSWAP}$）仅需 2 个 $\mathrm{CNOT}$。见[第 14 章](../14-compilation-control.md)。

**ZX 演算（ZX-calculus）**：把量子线路表示为由 $Z$ 基绿蜘蛛与 $X$ 基红蜘蛛及柔性连线组成的图形化线性代数语言，只要拓扑连接不变即可自由变形。借助蜘蛛融合律、双代数律、颜色变换与相位传送等完备重写规则，编译器可跨越远距离多比特纠缠识别并抵消或合并非 Clifford $T$ 门，是全局 $T$-count 优化与线路等价性验证的主力工具。见[第 14 章](../14-compilation-control.md)。

**DRAG 脉冲（Derivative Removal by Adiabatic Gate）**：在弱非谐比特的主同相脉冲包络 $I(t)$ 之外，向正交通道叠加其时间导数项 $Q(t) = -\frac{\beta}{\alpha}\dot I(t)$ 的脉冲整形技术，用于同时压制向 $\lvert 2\rangle$ 能级的泄漏以及伴随的 AC Stark 相位误差。见[第 14 章](../14-compilation-control.md)。

**动态解耦（dynamical decoupling, DD）**：在量子比特空闲等待期间插入特定定时与相位的重聚焦脉冲序列（如 Hahn 自旋回波、CPMG、XY4），通过周期翻转系统自旋把缓慢漂移的低频退相位噪声相互抵消。见 [Q3](../quantum-mechanics/03-levels-control.md) 与[第 14 章](../14-compilation-control.md)。

**动态电路与 Pauli 帧（Pauli frame）**：动态电路允许在单次执行中途完成测量、经典逻辑判断并即时反馈控制或复位。Pauli 帧在经典控制器里实时追踪纠错或前馈累积的 Pauli 修正，多数时候无需发射物理修正脉冲，只需调整后续非 Clifford 门和末态读出解释。

**线路切割（circuit cutting）与准概率分解（QPD）**：线路切割把超出单芯片规模的电路拆成若干较小的子电路分别执行，再把结果按准概率分解（QPD）的带符号实系数经典重构出目标期望值。系数绝对值之和 $\Gamma = \sum_j \lvert c_j\rvert$ 决定采样方差按 $\Gamma^2$ 放大，负系数表示带符号加权而非负概率。见[第 14 章](../14-compilation-control.md)与[第 19 章](../19-engineering-architecture.md)。

**误差缓解（QEM）、可观测量反向传播（OBP）与多乘积公式（MPF）**：误差缓解（如 ZNE、PEC）在不编码逻辑比特的前提下，用额外线路、采样预算和经典后处理减小期望值偏差，不能替代量子纠错。OBP 把线路末段共轭到待测可观测量上以缩短硬件深度；MPF 线性组合不同步长的 Trotter 期望值以抵消低阶模拟误差，负权重同样带来方差放大。见[第 08 章](../08-applications.md)与[开源实践对照](software-practice.md)。

**量子非破坏测量（QND）、读出判决保真度与复位**：QND 测量要求测量反作用尽量不破坏被测可观测量的本征态；读出判决保真度衡量经典分类标签与真实制备的一致比例，不单独刻画测后态与旁观串扰；复位是将比特恢复至初态 $\lvert 0\rangle$ 的物理操作，须同时报告残余激发、耗时与泄漏。见[第 19 章](../19-engineering-architecture.md)。

**门迹重叠与过程重叠**：在单比特理想酉门控制对照中，$g = \lvert\operatorname{Tr}(U_{\mathrm{tar}}^\dagger U)\rvert/2$ 忽略全局相位，过程重叠为 $g^2$，平均门保真度为 $F_{\mathrm{avg}} = (2g^2 + 1)/3$；三者与根保真度及器件泄漏率口径不同。见[第 14 章](../14-compilation-control.md)。

**重复运行次数（shots）、有效样本数与后选择（postselection）**：按规定线路与设置运行并记录一次输出为一次 shot；存在批次相关性或漂移时，有效样本数往往远低于原始 shots 总数。后选择只保留满足特定条件的记录来计算条件统计，报告条件保真度时必须同步报告接受率与总运行数。

**参数移位法则（parameter-shift rule）**：利用门生成元的谱特性，把期望值对门参数的精确导数写成少量参数平移线路期望值的线性组合；同一训练变量进入多扇门时须按链式法则逐门累加。见[第 08 章](../08-applications.md)。

**经典阴影（classical shadow）、插件估计与 U 统计量**：经典阴影通过对随机基测量结果施加逆测量通道生成单次统计快照，用于高效估计大量局域可观测量；单个快照不必半正定。把无偏线性估计直接代入平方或熵等非线性公式（插件估计）会引入同快照二次噪声偏差，对纯度等二次量可用不同独立快照交叉乘积的 U 统计量消去该偏差。见[第 13 章](../13-quantum-information.md)与[第 16 章](../16-advanced-algorithms-verification.md)。

**Fock 截止与归一化投影**：用有限数态基底 $\{\lvert 0\rangle,\dots,\lvert d-1\rangle\}$ 截断连续变量希尔伯特空间称为 Fock 截止。若截断漏掉尾概率 $\tau$，归一化投影态与原纯态的根保真度为 $\sqrt{1-\tau}$、迹距离为 $\sqrt{\tau}$；先截断哈密顿量再演化与先演化再截断并不等价。见 [Q4](../quantum-mechanics/04-wavefunctions-models.md) 与[第 18 章](../18-channels-capacities-complexity.md)。

**Ritz 值与 Ritz 向量**：把哈密顿量投影到有限子空间对角化得到的近似本征值与本征向量；在精确厄米投影与正交归一化基底下，最低 Ritz 值构成全空间基态能量的严格上界（SQD 等子空间方法的核心性质）。

**置信区间与贝叶斯可信区间**：频率学派置信区间的覆盖率刻画重复抽样时区间构造规则覆盖未知固定参数的长期比例；贝叶斯可信区间则刻画给定先验、模型与已观测数据后参数的后验概率区间。见[第 15 章](../15-practice-research.md)。

**到达目标成功率时间（TTS）、良率、可用率、MTBF / MTTR 与实验清单（manifest）**：TTS 核算达到规定总体成功概率所需的端到端时间（含编排、运行、重复与后处理）；器件良率与系统可用率 $\approx \mathrm{MTBF}/(\mathrm{MTBF}+\mathrm{MTTR})$ 是芯片制造与整机运维的核心指标；可复现实验清单则随作业归档代码版本、校准快照、编译选项、原始计数与后处理规则。见[第 15 章](../15-practice-research.md)、[第 17 章](../17-computation-models.md)与[第 19 章](../19-engineering-architecture.md)。

## 6. 量子传感与精密测量术语

**经典 Fisher 信息与量子 Fisher 信息（CFI & QFI）**：对固定测量方案的输出分布 $p(x\mid\theta)$，经典 Fisher 信息 $F_C(\theta) = \sum_{x:\,p>0}[\partial_\theta p(x\mid\theta)]^2 / p(x\mid\theta)$ 决定无偏估计方差的经典 Cramér–Rao 下界 $\Delta\theta \ge 1/\sqrt{\nu F_C(\theta)}$。对参数化量子态 $\rho_\theta$ 遍历所有合法 POVM 取极大值即得量子 Fisher 信息 $F_Q(\rho_\theta) = \operatorname{Tr}(\rho_\theta L_\theta^2)$（$L_\theta$ 为对称对数导数），纯态幺正演化下化为 $4(\Delta H)^2$，且按本书根保真度满足 $F_Q = 8\lim_{\delta\to 0}[1 - F(\rho_\theta,\rho_{\theta+\delta})]/\delta^2$。见[第 20 章](../20-quantum-sensing-metrology.md)。

**标准量子极限（SQL）、海森堡极限（HL）与自旋压缩（spin squeezing）**：$N$ 个彼此独立的探针测量无量纲相位时，精度上限为标准量子极限 $\Delta\phi_{\mathrm{SQL}} = 1/\sqrt{N}$（满足 $F_Q \le N$）；利用多体纠缠（如理想 GHZ 态）理论上可达海森堡极限 $\Delta\phi_{\mathrm{HL}} = 1/N$（$F_Q = N^2$），但在独立马尔可夫退相位噪声下 GHZ 态会迅速退回 $O(1/\sqrt{N})$（Huelga 界）。真实实验常借助单轴扭转等制备自旋压缩态，通过压窄敏感方向的集体自旋涨落使 Wineland 参数 $\xi_R^2 = N(\Delta J_\perp)^2/\lvert\langle\vec J\rangle\rvert^2 < 1$，在兼顾抗噪性的同时稳健突破 SQL。见[第 20 章](../20-quantum-sensing-metrology.md)。

**HNLS 纠错传感条件（Hamiltonian-Not-in-Lindblad-Span）**：周思思等人（2018）给出的马尔可夫噪声下量子纠错辅助传感能否恢复海森堡标度的精确充要判据：信号生成元 $H$ 不能落入噪声 Lindblad 算符张成子空间 $\mathcal S = \operatorname{span}\{I, L_k, L_k^\dagger, L_j^\dagger L_k\}$ 内（即 $H \notin \mathcal S$）。当 $H = Z/2$ 面对横向位翻转 $L = X$ 时 HNLS 成立，可编码压噪并恢复海森堡标度；面对平行退相位 $L = Z$ 或能量弛豫 $L = \lvert 0\rangle\langle 1\rvert$ 时 $H \in \mathcal S$，任何纠错码都无法突破 SQL 标度。见[第 20 章](../20-quantum-sensing-metrology.md)。
