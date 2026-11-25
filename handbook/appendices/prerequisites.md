# 入门先修：自测与补习路线

先做题 1–4，检查复数、矩阵和张量积是否顺手，再按学习目标补所需的概念。题 5–6 针对算法和统计实验，题 7 与选做 A–C 可按专题选择。[六篇总目录](../README.md)列出全书 26 章的阅读顺序。

## 1. 先选你当下想解决的问题

在手机上可左右滑动表格。表中的入口按学习目标选择，可以跨篇阅读。

| 你想做到的事 | 眼下最有用的准备 | 阅读入口 |
|---|---|---|
| 看懂量子态、纠缠、电路与噪声（第一篇） | 分数、条件概率、复数模平方、列向量与矩阵乘法、张量积 | [全景 00](../00-overview.md) → [数学 01](../01-math.md) → [单比特 02](../02-single-qubit.md) → [多比特 03](../03-multiple-qubits.md) → [电路 04](../04-circuits-protocols.md) → [噪声 05](../05-noise-channels.md) |
| 从实验理解量子过程，或推导连续波函数（第二篇） | Q1–Q3 先从矩阵算例入手。Q4 的完整推导用到一元导数、定积分与简单二阶微分方程 | [实验 Q1](../quantum-mechanics/01-experiments-states.md) → [演化 Q2](../quantum-mechanics/02-observables-dynamics.md) → [能级 Q3](../quantum-mechanics/03-levels-control.md)。想了解连续模型可从 Q2 转入[波函数 Q4](../quantum-mechanics/04-wavefunctions-models.md) |
| 手算 Grover、QPE、Shor，再用统计验证算法（第三篇） | 第一篇的量子态、门与测量。读 Shor 时补模运算，做有限样本实验时补二项抽样 | [算法骨架 06](../06-algorithmic-primitives.md) → [代表算法 07](../07-algorithms.md) → [变分与应用 08](../08-applications.md) → [实验方法 15](../15-practice-research.md) |
| 理解物理器件、纠错、编译控制与系统工程（第四篇） | 第一篇的多比特、线路与噪声；能级、失谐与实验标定可从 [Q3](../quantum-mechanics/03-levels-control.md) 补起 | [硬件 09](../09-hardware.md) → [纠错容错 10](../10-error-correction.md) → [基准资源 11](../11-resources-benchmarks.md) → [编译控制 14](../14-compilation-control.md) → [系统工程 19](../19-engineering-architecture.md) |
| 理解后量子密码、QKD 与量子网络（第五篇） | [03 的 Bell 态与 CHSH](../03-multiple-qubits.md)、[04 的隐形传态和不可克隆](../04-circuits-protocols.md)、[07 的 Shor 与 Grover](../07-algorithms.md) | [密码与网络 12](../12-security-network-frontiers.md)。安全证明中的信息量度可对照[第 13 章](../13-quantum-information.md)，容错网络专题可对照[第 10 章](../10-error-correction.md) |
| 区分各种信道容量，或学习连续变量（第五篇） | [03 的纠缠](../03-multiple-qubits.md)、[05 的信道](../05-noise-channels.md)和[13 的信息量度](../13-quantum-information.md)。验证复杂度一节可回看[第 07 章](../07-algorithms.md)，连续变量一节需要 [Q4 的谐振子](../quantum-mechanics/04-wavefunctions-models.md#4-量子谐振子用升降算符一步步搭出等间距能级梯)。 | [信道与容量 18](../18-channels-capacities-complexity.md)。研究光学模式与 GKP 网格码时进入[第 18 章 §9](../18-channels-capacities-complexity.md#9-连续变量cv量子信息正交分量wigner-相空间gkp-网格码与截断边界)。 |
| 推导量子传感的灵敏度与精度界（第五篇） | [03 的 GHZ 态与偏迹](../03-multiple-qubits.md)、[05 的退相位](../05-noise-channels.md)、[Q3 的 Ramsey 与回波](../quantum-mechanics/03-levels-control.md)；手算似然时用到一阶导数 | [传感 20](../20-quantum-sensing-metrology.md) §3.3 与 §6.2 分别引入根保真度和单模正交分量。深入混态距离可翻[第 13 章](../13-quantum-information.md)，深入多模连续变量可翻[第 18 章 §9](../18-channels-capacities-complexity.md#9-连续变量cv量子信息正交分量wigner-相空间gkp-网格码与截断边界) |
| 研究高级算法、其他计算模型与经典模拟（第六篇） | 16 从 [06](../06-algorithmic-primitives.md)、[07](../07-algorithms.md) 的算法原语起步。17 从[第 04 章的门与电路](../04-circuits-protocols.md)起步。21 的稳定子、MPS 与模拟器分别接续 [10](../10-error-correction.md)、[03](../03-multiple-qubits.md) 和 [15](../15-practice-research.md) | 按目标选读[高级算法 16](../16-advanced-algorithms-verification.md)、[计算模型 17](../17-computation-models.md)或[经典模拟 21](../21-stabilizer-classical-simulation.md) |

想先看实验的读者可以直接打开[离线交互量子实验台](../../reader/lab/quantum-lab.html)。[实验总览](../labs/README.md)中的默认离线验证脚本用 Python 标准库运行。第 15 章的 [NumPy 模拟器](../15-practice-research.md#2-从零手写-python-态矢量模拟器)可先用纸笔核对小矩阵，再用 [NumPy 入门教程](https://numpy.org/doc/stable/user/absolute_beginners)补数组操作。

## 2. 六道基础自测与四道专题热身

做题时先遮住“核对”段落，老老实实写出中间步骤。算完后问自己：是看不懂符号、算错了代数，还是算对了数字却说不清它代表什么？只要把卡住的那一环补齐，后面就会顺畅很多。

### 题 1：条件概率的分母

有 $2000$ 个彼此独立、按同一流程制备的实验样本，第一步有 $800$ 个通过筛选。只对这 $800$ 个样本继续测量，其中有 $200$ 个得到结果“1”。请问：第二步在“已通过第一步”条件下的结果 1 频率是多少？相对于最初 $2000$ 个样本的联合频率又是多少？

**核对。** 条件频率的分母是进入第二步的 $800$ 个，因此是 $200/800 = 1/4$；联合频率的分母是最初的总数 $2000$ 个，因此是 $200/2000 = 1/10$。第一步通过率为 $800/2000 = 2/5$，两者相乘 $(2/5)(1/4) = 1/10$，正好吻合。如果在后选择和条件分母上容易发懵，建议先看[第 00 章的最小随机比特实验](../00-overview.md#4-一个从头到尾的最小实验产生随机比特)和[第 15 章的有限样本统计工具箱](../15-practice-research.md#3-有限样本统计实用工具箱)。

### 题 2：复数振幅怎样归一化

给定未归一化列向量 $v = (2,\, 1-i)^T$。请把它归一化为单位长度向量，并求在计算基下测得 $0$ 和 $1$ 的概率。

**核对。** 先求长度的平方（逐项取模平方再相加）：

$$
\lvert 2\rvert^2 + \lvert 1-i\rvert^2 = 2^2 + \bigl(1^2 + (-1)^2\bigr) = 4 + 2 = 6.
$$

所以向量长度为 $\sqrt{6}$，归一化态矢量是 $\lvert\psi\rangle = (2,\, 1-i)^T / \sqrt{6}$。两个分量的振幅分别是 $2/\sqrt{6}$ 和 $(1-i)/\sqrt{6}$，各自取模平方得到测量概率 $4/6 = 2/3$ 和 $2/6 = 1/3$，相加恰好等于 $1$。记住：复振幅算概率一定要取模平方 $\lvert z\rvert^2 = z^* z$，绝不能直接把复数普通平方（否则 $(1-i)^2 = -2i$ 会算出复数概率）。如果这一步不熟，回读[数学 01 第 1 节：复数](../01-math.md#1-复数把旋转和缩放装进一个数)。

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

假设某二元测量结果的真实概率为 $p = 1/2$，独立重复采样 $N = 900$ 次。样本频率 $\hat p$ 的标准差是多少？如果一次实验测出 $459$ 次“0”和 $441$ 次“1”，能不能仅凭这组计数断言芯片存在偏差？

**核对。** 在独立同分布二项模型下，样本频率的标准差为

$$
\mathrm{sd}(\hat p) = \sqrt{\frac{p(1-p)}{N}} = \sqrt{\frac{0.5 \times 0.5}{900}} = \frac{1}{60} \approx 0.01667.
$$

实测频率 $459/900 = 0.51$，距离 $0.5$ 仅偏出 $0.01$，约等于 $0.60\sigma$，完全落在正常随机起伏内。因此这组数据既不能证明设备有偏差，也不能证明设备绝对完美——要测出 $1\%$ 级别的微小系统偏差，需要远大于 $900$ 次的样本量，还要检查各批次之间有没有时间漂移。详见[第 15 章第 3 节：有限样本统计实用工具箱](../15-practice-research.md#3-有限样本统计实用工具箱)。

### 题 7：微积分积分热身（只给准备读 Q4 或第 18 章连续变量的读者）

计算定积分 $\int_0^L \sin^2\!\left(\frac{\pi x}{L}\right)dx$，其中 $L > 0$ 为势阱宽度。

**核对。** 用降幂公式 $\sin^2 u = (1 - \cos 2u)/2$ 化简：

$$
\int_0^L \sin^2\!\left(\frac{\pi x}{L}\right)dx
= \int_0^L \frac{1 - \cos(2\pi x / L)}{2}\,dx
= \frac{L}{2} - \frac{1}{2}\left[\frac{L}{2\pi}\sin\!\left(\frac{2\pi x}{L}\right)\right]_0^L
= \frac{L}{2}.
$$

这说明把 $\sin(\pi x/L)$ 乘上常数 $\sqrt{2/L}$ 后，模平方在 $[0,L]$ 上的积分恰好为 $1$，这就是一维无限深方势阱的归一化基态波函数。如果对这里的三角化简和积分代入感到生疏，可以先复习一元微积分，再读[Q4 第 2 节：无限深方势阱](../quantum-mechanics/04-wavefunctions-models.md#2-无限深方势阱离散能级怎样从边界条件中长出来)。这道题不影响你学习全书绝大多数离散线路与算法章节。

### 选做热身 A：外积投影与本征值快检（用于决定是否跳过第 01 章 §3–§5）

已知 $\lvert +\rangle = (1, 1)^T/\sqrt{2}$ 与 Pauli-$X = \bigl(\begin{smallmatrix} 0 & 1 \\ 1 & 0 \end{smallmatrix}\bigr)$。请写出外积投影矩阵 $P_+ = \lvert +\rangle\langle +\rvert$，验证 $P_+^2 = P_+$，并求出 $X\lvert +\rangle$ 对应的本征值。

**核对。** 列向量乘行向量得 $2\times 2$ 矩阵：

$$
P_+ = \lvert +\rangle\langle +\rvert
= \frac{1}{2}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\begin{bmatrix} 1 & 1 \end{bmatrix}
= \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}.
$$

直接相乘得 $P_+^2 = \frac{1}{4}\bigl(\begin{smallmatrix} 2 & 2 \\ 2 & 2 \end{smallmatrix}\bigr) = P_+$，且 $\operatorname{Tr}(P_+) = 1$。再算 $X\lvert +\rangle = \frac{1}{\sqrt{2}}\bigl(\begin{smallmatrix} 0 & 1 \\ 1 & 0 \end{smallmatrix}\bigr)\bigl(\begin{smallmatrix} 1 \\ 1 \end{smallmatrix}\bigr) = \frac{1}{\sqrt{2}}\bigl(\begin{smallmatrix} 1 \\ 1 \end{smallmatrix}\bigr) = (+1)\lvert +\rangle$，本征值为 $+1$。若对外积与内积形状区分或特征值求解有犹豫，建议重点读[第 01 章 §3.2](../01-math.md#32-正交投影把手电筒的影子写成外积矩阵)与[§5 本征值与谱分解](../01-math.md#5-本征值本征向量与谱分解22-零跳步配方)。

### 选做热身 B：对数似然求导（面向第 20 章量子传感与 Fisher 信息）

设理想单比特 Ramsey 干涉仪输出结果为 `0` 与 `1` 的概率分别为 $p(0\mid\phi) = \cos^2(\phi/2)$、$p(1\mid\phi) = \sin^2(\phi/2)$（$\phi\in(0,\pi)$）。分别计算对数似然导数 $\partial_\phi \ln p(0\mid\phi)$ 与 $\partial_\phi \ln p(1\mid\phi)$，再代入经典 Fisher 信息公式 $F_C(\phi) = \sum_{x\in\{0,1\}} p(x\mid\phi)\bigl[\partial_\phi \ln p(x\mid\phi)\bigr]^2$。

**核对。** 由链式法则 $(\ln u)' = u'/u$：

$$
\frac{\partial}{\partial\phi}\ln\!\left(\cos^2\frac{\phi}{2}\right)
= \frac{2\cos(\phi/2)\cdot\bigl(-\frac{1}{2}\sin(\phi/2)\bigr)}{\cos^2(\phi/2)}
= -\tan\frac{\phi}{2},
\qquad
\frac{\partial}{\partial\phi}\ln\!\left(\sin^2\frac{\phi}{2}\right)
= +\cot\frac{\phi}{2}.
$$

代入经典 Fisher 信息定义并化简：

$$
F_C(\phi)
= \cos^2\frac{\phi}{2}\tan^2\frac{\phi}{2} + \sin^2\frac{\phi}{2}\cot^2\frac{\phi}{2}
= \sin^2\frac{\phi}{2} + \cos^2\frac{\phi}{2}
= 1.
$$

因此，在题设的开区间里，每次测量的相位信息为 $1$。若把相位扩到端点，例如 $\phi=0$，结果 $0$ 的概率为 $1$、导数为 $0$，结果 $1$ 在该点的概率为 $0$。按[符号表](notation.md)中只对正概率项求和的约定，端点的点值为 $0$，从内点趋近端点的极限为 $1$。这两种取法不同，因为端点的概率支持发生了变化。固定这一测量时，$+\phi$ 与 $-\phi$ 也给出一样的分布。要测有符号的微小失谐，可把读出偏置调到条纹半高处。估计频率时还要用 $\phi=2\pi f t$ 换元，询问时间 $t=0$ 时频率信息为 $0$。见[第 20 章](../20-quantum-sensing-metrology.md)。

### 选做热身 C：$\mathbb{F}_2$ 模 2 辛内积（面向第 10 章纠错与第 21 章稳定子表）

把两比特 Pauli 串编码为四位二元行向量 $(x_0, x_1 \mid z_0, z_1)\in\mathbb{F}_2^4$（其中 $I\mapsto(0,0),\; X\mapsto(1,0),\; Z\mapsto(0,1),\; Y\mapsto(1,1)$），两串是否对易由模 2 辛内积 $(x\mid z)\odot(x'\mid z') = (x\cdot z' \oplus z\cdot x')\bmod 2$ 决定（结果为 $0$ 对易，$1$ 反对易）。请分别计算 $P_1 = X_0 Z_1$ 与 $P_2 = Z_0 X_1$、以及 $P_1 = X_0 Z_1$ 与 $P_3 = Z_0 Z_1$ 的模 2 辛内积，判断它们对易还是反对易。

**核对。** 先写出三串的二元辛向量：

- $P_1 = X_0 Z_1 \mapsto x^{(1)}=(1,0),\; z^{(1)}=(0,1)$；
- $P_2 = Z_0 X_1 \mapsto x^{(2)}=(0,1),\; z^{(2)}=(1,0)$；
- $P_3 = Z_0 Z_1 \mapsto x^{(3)}=(0,0),\; z^{(3)}=(1,1)$。

逐位套用模 2 辛内积（注意 $1\oplus 1 = 0$）：

$$
\begin{aligned}
P_1 \odot P_2 &= \bigl(1\cdot 1 \oplus 0\cdot 0\bigr) \oplus \bigl(0\cdot 0 \oplus 1\cdot 1\bigr) = 1 \oplus 1 = 0 \quad\text{（对易！）}, \\
P_1 \odot P_3 &= \bigl(1\cdot 1 \oplus 0\cdot 1\bigr) \oplus \bigl(0\cdot 0 \oplus 1\cdot 0\bigr) = 1 \oplus 0 = 1 \quad\text{（反对易！）}.
\end{aligned}
$$

独立回验：$P_1$ 与 $P_2$ 在第 0 位（$X$ 与 $Z$）和第 1 位（$Z$ 与 $X$）各产生一个负号，$(-1)(-1) = +1$ 所以整体对易；$P_1$ 与 $P_3$ 仅在第 0 位反对易，整体反对易。掌握这个只用异或就能完成的计算规则，就拿到了[第 10 章稳定子码](../10-error-correction.md)与[第 21 章稳定子表模拟引擎](../21-stabilizer-classical-simulation.md)的通用钥匙。

## 3. 自测通关分流表：怎样高效跳读第 01 章并回到主线

做完自测后，按卡住的概念选择[第 01 章](../01-math.md)的小节，再回到正在学习的主题。

| 你的自测通关情况 | 第 01 章跳读建议 | 建议立刻衔接的主线入口 |
|---|---|---|
| **题 1–4 任一题卡壳** | 从[第 01 章 §1–§8](../01-math.md#1-复数把旋转和缩放装进一个数)中补对应的数学操作，再重做卡住的题 | 接着进入[第 02 章](../02-single-qubit.md)，想先看实验可选读 [Q1](../quantum-mechanics/01-experiments-states.md) §1–§5 |
| **题 1–4 全对，但选做 A（外积/本征值）犹豫** | 补[§3.2 正交投影](../01-math.md#32-正交投影把手电筒的影子写成外积矩阵)、[§4.4 被动换基与主动施门](../01-math.md#44-换坐标还是动了态被动换基与主动施门)和[§5 本征值与谱分解](../01-math.md#5-本征值本征向量与谱分解22-零跳步配方) | 沿第一篇继续阅读[第 02–05 章](../02-single-qubit.md) |
| **题 1–6 与选做 A 全部顺手通关** | 按需查[§6.3–§6.4 的矩阵指数、SVD 与求逆条件数](../01-math.md#63-矩阵指数从厄米算符生出酉门)和[§9 的复杂度口径](../01-math.md#9-进阶选读渐近复杂度口径与常数交叉点) | 从[第 02 章](../02-single-qubit.md)起步。若已能写出多比特态、逐门演算线路并给出测量概率，可进入[第 06 章](../06-algorithmic-primitives.md) |
| **准备读传感、稳定子或连续变量专题** | 用**选做 B**检查对数似然求导，用**选做 C**检查 $\mathbb{F}_2$ 辛内积，用**题 7**检查三角积分 | 按上表补足相应先修，再进入[第 20 章](../20-quantum-sensing-metrology.md)、[第 10 章](../10-error-correction.md)或[第 21 章](../21-stabilizer-classical-simulation.md)、[Q4](../quantum-mechanics/04-wavefunctions-models.md)或[第 18 章 §9](../18-channels-capacities-complexity.md#9-连续变量cv量子信息正交分量wigner-相空间gkp-网格码与截断边界) |

阅读过程中遇到不眼熟的符号或新词，随时翻查[符号表](notation.md)和[术语表](glossary.md)；做章末练习卡住时，先在[练习答案与推导提示](exercises.md)里展开该题的**核心提示**自己再推一步，最后核对四步零跳步全解。
