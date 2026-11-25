# 入门先修：自测与补习路线

读量子计算之前，不需要先修完一整套大学量子力学。你需要哪些先修工具，完全取决于当下想读懂哪一部分内容。下面的五篇 26 章路线表和七道短题，帮你快速定位眼下容易卡住的那一步；哪一题卡壳，就顺着题后的链接去补那一小节，不必从头重修所有前置课程。

## 1. 先选你当下想解决的问题

在手机上可左右滑动下表，查看最右侧的五篇 26 章推荐阅读顺序。

| 你想做到的事 | 眼下最有用的准备 | 推荐阅读顺序（对应五篇 26 章体系） |
|---|---|---|
| 看懂单比特、纠缠、基础线路与噪声（第一篇） | 分数与条件概率、复数模平方、二维列向量与矩阵乘法、张量积 | [全景 00](../00-overview.md) → [数学 01](../01-math.md) → [实验 Q1](../quantum-mechanics/01-experiments-states.md) → [单比特 02](../02-single-qubit.md) → [演化 Q2](../quantum-mechanics/02-observables-dynamics.md) → [多比特 03](../03-multiple-qubits.md) → [电路 04](../04-circuits-protocols.md) → [噪声 05](../05-noise-channels.md) |
| 手算 Grover、QPE、Shor 与变分应用，并动手写模拟器做统计验收（第二篇） | 走完第一篇，再熟悉模运算、对数底数、二项抽样与 Python/NumPy 基础 | [算法骨架 06](../06-algorithmic-primitives.md) → [代表算法 07](../07-algorithms.md) → [变分与应用 08](../08-applications.md) → [实践路线 15](../15-practice-research.md) |
| 理解真实器件、脉冲控制、纠错与整机系统工程（第三篇） | 读完第一篇，熟悉[数学 01 的矩阵指数与条件数](../01-math.md)，再补能量、角频率与旋转坐标系 | [能级 Q3](../quantum-mechanics/03-levels-control.md) → [硬件 09](../09-hardware.md) → [编译控制 14](../14-compilation-control.md) → [纠错容错 10](../10-error-correction.md) → [基准资源 11](../11-resources-benchmarks.md) → [系统工程 19](../19-engineering-architecture.md) |
| 搞清后量子密码、QKD 与量子网络（第四篇上） | 第一篇电路与噪声、Shor 算法直觉、基础条件概率与二元熵 | [密码与网络 12](../12-security-network-frontiers.md)（衔接[第 04 章](../04-circuits-protocols.md)、[第 07 章](../07-algorithms.md)、[第 10 章](../10-error-correction.md)） |
| 入门量子传感与精密测量、推导 SQL 与海森堡极限（第四篇下） | 一阶求导与似然函数、GHZ 态、退相位信道、Ramsey/回波与根保真度 | [能级 Q3](../quantum-mechanics/03-levels-control.md) + [噪声 05](../05-noise-channels.md) + [信息量度 13](../13-quantum-information.md) → [量子传感 20](../20-quantum-sensing-metrology.md)（光学压缩另需[第 18 章第 9 节](../18-channels-capacities-complexity.md)） |
| 掌握稳定子表、MPS 与 Pauli 传播，看透经典模拟边界（第五篇） | 模 2 异或运算、Schmidt/SVD 分解、Clifford 群、稳定子群与态矢量模拟 | [多比特 03](../03-multiple-qubits.md) + [电路 04](../04-circuits-protocols.md) + [纠错 10](../10-error-correction.md) + [实践 15](../15-practice-research.md) → [经典模拟边界 21](../21-stabilizer-classical-simulation.md)（与[第 16 章](../16-advanced-algorithms-verification.md)互照） |
| 亲手推导波函数、势阱、谐振子、隧穿并攻克连续变量与信道容量（第五篇） | 读至演化 Q2 与信息量度 13，另需一元微积分与简单二阶微分方程 | [信息量度 13](../13-quantum-information.md) → [计算模型 17](../17-computation-models.md) → [波函数 Q4](../quantum-mechanics/04-wavefunctions-models.md) → [信道与连续变量 18](../18-channels-capacities-complexity.md) |
| 亲手运行、改写第 15 章的模拟器与全书 36 个本地脚本 | Python 变量、函数与循环基础；熟悉 NumPy 数组建立与运算 | 先手算[数学 01 的矩阵算例](../01-math.md#4-矩阵与量子算符从线性变换到酉门厄米算符)，再参考 [NumPy 入门教程](https://numpy.org/doc/stable/user/absolute_beginners)，最后动手写[实践 15 的 Python 态矢量模拟器](../15-practice-research.md#2-从零手写-python-态矢量模拟器) |

[第 01 章：零基础数学工具](../01-math.md)会从复数和列向量一步步讲起；下面的自测用来帮你判断，在此之前是否需要花半小时热身一下分数、条件概率或模运算。写代码能帮你快速验算，但并非读懂前五章的前提——第 15 章里的矩阵乘法 `@` 和左共轭内积 `np.vdot`，都能先在草稿纸上用手算摸透。此外，[逐章实验册](../labs/README.md)中的 36 个教学脚本仅依赖 Python 标准库，不装 NumPy 也能直接运行核对。

这种分层安排也和主流公开课程一致：[IBM 的量子信息基础课程](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)主要要求基本线性代数、复数与函数基础；而 [MIT 8.04 量子物理 I 课程说明](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/pages/syllabus/)则把波动与微分方程列为正式先修，对应本书第五篇选读的 Q4 深度。

## 2. 七道短题：拿张草稿纸直接算

做题时先遮住“核对”段落，老老实实写出中间步骤。算完后问自己：是看不懂符号、算错了代数，还是算对了数字却说不清它代表什么？只要把卡住的那一环补齐，后面就会顺畅很多。

### 题 1：条件概率的分母

有 $2000$ 个彼此独立、按同一流程制备的实验样本，第一步有 $800$ 个通过筛选。只对这 $800$ 个样本继续测量，其中有 $200$ 个得到结果“1”。请问：第二步在“已通过第一步”条件下的结果 1 频率是多少？相对于最初 $2000$ 个样本的联合频率又是多少？

**核对。** 条件频率的分母是进入第二步的 $800$ 个，因此是 $200/800 = 1/4$；联合频率的分母是最初的总数 $2000$ 个，因此是 $200/2000 = 1/10$。第一步通过率为 $800/2000 = 2/5$，两者相乘 $(2/5)(1/4) = 1/10$，正好吻合。如果在后选择和条件分母上容易发懵，建议先看[第 00 章的最小随机比特实验](../00-overview.md#4-一个从头到尾的最小实验产生随机比特)和[第 15 章的有限样本统计工具箱](../15-practice-research.md#3-有限样本统计实用工具箱)。

### 题 2：复数振幅怎样归一化

给定未归一化列向量 $v = (1,\, 1+i)^T$。请把它归一化为单位长度向量，并求在计算基下测得 $0$ 和 $1$ 的概率。

**核对。** 先求长度的平方（逐项取模平方再相加）：

$$
\lvert 1\rvert^2 + \lvert 1+i\rvert^2 = 1^2 + (1^2 + 1^2) = 1 + 2 = 3.
$$

所以向量长度为 $\sqrt{3}$，归一化态矢量是 $\lvert\psi\rangle = (1,\, 1+i)^T / \sqrt{3}$。两个分量的振幅分别是 $1/\sqrt{3}$ 和 $(1+i)/\sqrt{3}$，各自取模平方得到测量概率 $1/3$ 和 $2/3$，相加恰好等于 $1$。记住：复振幅算概率一定要取模平方 $\lvert z\rvert^2 = z^* z$，绝不能直接把复数普通平方。如果这一步不熟，回读[数学 01 第 1 节：复数](../01-math.md#1-复数把旋转和缩放装进一个数)。

### 题 3：矩阵乘法按什么顺序作用

已知 Hadamard 门和 Pauli-$Z$ 门矩阵为

$$
H = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix},
\qquad
Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}.
$$

从基态 $\lvert 0\rangle = (1,0)^T$ 出发，计算 $HZH\lvert 0\rangle$。

**核对。** 算符乘积从右向左依次作用：

1. 最右边的 $H$ 先作用：$H\lvert 0\rangle = (1,\,1)^T/\sqrt{2}$；
2. 中间的 $Z$ 把第二个分量翻号：$ZH\lvert 0\rangle = (1,\,-1)^T/\sqrt{2}$；
3. 最左边的 $H$ 再作用：$HZH\lvert 0\rangle = \frac{1}{2}(1-1,\, 1+1)^T = (0,\,1)^T = \lvert 1\rangle$。

矩阵写出的顺序与电路图从左到右的时间顺序正好相反。若这里容易算混，补读[数学 01 第 4 节：矩阵与量子算符](../01-math.md#4-矩阵与量子算符从线性变换到酉门厄米算符)以及[第 02 章：单量子比特](../02-single-qubit.md)。

### 题 4：两比特系统的基顺序

按全书约定的大端序基 $\lvert 00\rangle,\lvert 01\rangle,\lvert 10\rangle,\lvert 11\rangle$，写出 $\lvert 1\rangle \otimes \lvert +\rangle$ 的四维列向量，其中 $\lvert +\rangle = (\lvert 0\rangle + \lvert 1\rangle)/\sqrt{2}$。

**核对。** 先按线性分配律展开：

$$
\lvert 1\rangle \otimes \lvert +\rangle = \lvert 1\rangle \otimes \frac{\lvert 0\rangle + \lvert 1\rangle}{\sqrt{2}} = \frac{\lvert 10\rangle + \lvert 11\rangle}{\sqrt{2}}.
$$

对应到四维列向量就是 $(0,\, 0,\, 1,\, 1)^T/\sqrt{2}$。张量积描写的是“把两个独立子系统并在一起构成的联合状态”，不是先后做两次单比特操作。若想再练几遍矩阵分块张量积，读[数学 01 第 7 节：张量积](../01-math.md#7-张量积多比特系统的印章分块法则)，再对照[第 03 章：多量子比特](../03-multiple-qubits.md)。

### 题 5：模运算周期与成本口径

第一问：依次算出 $2^k \bmod 15$ 在 $k = 0,1,2,3,4$ 时的值，找出从 $k=0$ 出发的最短重复周期。第二问：若某搜索问题共有 $N = 2^{20}$ 个候选项，一种算法约需调用 $\sqrt{N}$ 次检查黑箱，而每次黑箱调用内部要展开成 $100$ 个基本门，仅黑箱部分大约需要多少个基本门？

**核对。** 第一问依次算出：$2^0=1$，$2^1=2$，$2^2=4$，$2^3=8$，$2^4=16 \equiv 1 \pmod{15}$。到 $k=4$ 首次回到 $1$，所以最短周期是 $r = 4$。这是理解[第 07 章 Shor 算法教学例子](../07-algorithms.md)所需的数论热身。

第二问中，$\sqrt{N} = \sqrt{2^{20}} = 2^{10} = 1024$ 次黑箱调用；把每次调用的内部门数算进来，仅黑箱部分就要约 $1024 \times 100 = 102{,}400$ 个基本门，还没计入反射门、路由、纠错与重复运行。学[第 06 章：算法的共同骨架](../06-algorithmic-primitives.md)时，务必把“查询黑箱的次数”和“实际物理/逻辑门数”区分开。

### 题 6：有限采样有多大随机波动

假设某二元测量结果的真实概率为 $p = 1/2$，独立重复采样 $N = 400$ 次。样本频率 $\hat p$ 的标准差是多少？如果一次实验测出 $204$ 次“0”和 $196$ 次“1”，能不能仅凭这组计数断言芯片存在偏差？

**核对。** 在独立同分布二项模型下，样本频率的标准差为

$$
\mathrm{sd}(\hat p) = \sqrt{\frac{p(1-p)}{N}} = \sqrt{\frac{0.5 \times 0.5}{400}} = 0.025.
$$

实测频率 $204/400 = 0.51$，距离 $0.5$ 只差 $0.01$，还不到半个标准差（$0.4\sigma$），完全落在正常随机起伏内。因此这组数据既不能证明设备有偏差，也不能证明设备绝对完美——要测出 $1\%$ 级别的微小系统偏差，需要更大的样本量，还要检查各批次之间有没有时间漂移。详见[第 15 章第 3 节：有限样本统计实用工具箱](../15-practice-research.md#3-有限样本统计实用工具箱)。

### 题 7：微积分热身（只给准备读 Q4 或第 20 章导数推导的读者）

计算定积分 $\int_0^L \sin^2\!\left(\frac{\pi x}{L}\right)dx$，其中 $L > 0$ 为势阱宽度。

**核对。** 用降幂公式 $\sin^2 u = (1 - \cos 2u)/2$ 化简：

$$
\int_0^L \sin^2\!\left(\frac{\pi x}{L}\right)dx
= \int_0^L \frac{1 - \cos(2\pi x / L)}{2}\,dx
= \frac{L}{2} - \frac{1}{2}\left[\frac{L}{2\pi}\sin\!\left(\frac{2\pi x}{L}\right)\right]_0^L
= \frac{L}{2}.
$$

这说明把 $\sin(\pi x/L)$ 乘上常数 $\sqrt{2/L}$ 后，模平方在 $[0,L]$ 上的积分恰好为 $1$，这就是一维无限深方势阱的归一化基态波函数。如果对这里的三角化简和积分代入感到生疏，可以先复习一元微积分，再读[Q4 第 2 节：无限深方势阱](../quantum-mechanics/04-wavefunctions-models.md#2-无限深方势阱离散能级怎样从边界条件中长出来)。这道题不影响你学习全书绝大多数离散线路与算法章节。

## 3. 自测完怎样回到主线

- **题 1–4** 是第一篇（`00–05` 与 `Q1–Q2`）的日常工具，算顺手后可以直接进入主线；
- **题 5–6** 对应第二篇算法与统计实践（`06–08` 与 `15`），并在评估基准、传感与模拟误差时反复用到；
- **题 7** 专供第五篇选读 Q4（及第 18 章连续变量、第 20 章连续参数求导）使用。

阅读过程中遇到不眼熟的符号或新词，随时翻查[符号表](notation.md)和[术语表](glossary.md)；做章末练习卡住时，再对照[练习答案](exercises.md)定位自己卡在定义、代数还是物理理解上。
