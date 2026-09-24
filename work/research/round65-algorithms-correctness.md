# 第 65 轮｜算法、噪声、量子信息与容量的正确性深审

日期：2026-09-24。范围：`05-noise-channels.md`、`06-algorithmic-primitives.md`、`07-algorithms.md`、`08-applications.md`、`13-quantum-information.md`、`16-advanced-algorithms-verification.md`、`18-channels-capacities-complexity.md`，共约 5100 行。没有修改 `sources/`、阅读版生成文件或共享练习答案。本报告只陈述本轮检查范围，不宣称数学和实验前沿从此不会再有新结果。

## 核查方法与总结果

逐篇按“定义与参数约定—公式推导—数值例子—定理前提—资源模型—来源”读过，特别核对根保真度与平方保真度、单次和渐近容量、相位估计误差、查询复杂度与门复杂度的界线。用独立矩阵运算复核：振幅阻尼 $|+\rangle$ 输出、两种退极化参数、无歧义判别 POVM 的谱、QAOA 三顶点路径、QPE 边界例、Trotter 两个步数的谱范数、LCU 成功概率、Bell 加白噪声态的部分转置谱。复算结果与正文一致，具体数值列在下文。

本轮实质改进两处：第 05 章补出退极化参数换算推导及有效区间；第 18 章把擦除信道经典容量的上界写成对**任意跨多次联合编码**成立的 Holevo 维数界，再以 Fano 不等式连接到可靠速率。前者防止同名“退极化概率”混用，后者补上原文从直觉到容量结论的逻辑缺口。其余已检查的核心式与算例未发现需更正的数值错误。

## 逐篇记录

### 05｜混态、噪声与量子信道

- 查了 CPTP/Kraus 完备关系、转置非完全正的 Bell 部分转置谱、测量工具与 POVM 的区别、复位信道、比特/相位翻转、振幅阻尼、退极化及 $T_1,T_2,T_\phi$ 的适用条件。
- 复验 $\gamma=0.36$ 的 $|+\rangle$ 振幅阻尼输出为 $\begin{psmallmatrix}0.68&0.40\\0.40&0.32\end{psmallmatrix}$；$p=0.20$ 的本书退极化定义对应随机 Pauli 总概率 $q=0.15$，两种公式输出的最大矩阵元差在数值计算中约 $5.6\times10^{-17}$。
- 修订 §5.4：显式计算 $X\rho X+Y\rho Y+Z\rho Z=2I-\rho$，推出 $q=3p/4$；说明本书 $p\in[0,1]$ 只对应随机 Pauli 的 $q\in[0,3/4]$，而 $q>3/4$ 仍可为合法信道但 Bloch 向量变号，不能按“混入最大混态的概率 $p\le1$”解读。
- 来源：[IBM Quantum Learning 的量子信道讲义](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/quantum-channels)给出完全退极化的 Pauli 共轭求和；[Preskill 的 qubit 信道讲义](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-5-Qubit-Channels.pdf)用于检查弛豫与相干时间关系。

### 06｜量子算法的共同骨架

- 查了可逆 oracle、Deutsch–Jozsa 的精确与随机经典基线、BV、幅度放大的反射符号、QFT 端序、QPE 非网格概率和前缀反例、受控幂成本、乘积公式与查询下界。
- 复验 $M=256,\phi=1/4-1/(10M)$ 时 $\Pr(y=64)=0.96753169497$。原文正确地区分圆周数值误差与二进制前缀正确性，未改。
- 来源：[Cleve 等人对相位估计的原始整理](https://arxiv.org/abs/quant-ph/9708016)、[Brassard 等人的幅度放大/估计论文](https://arxiv.org/abs/quant-ph/0005055)、[Beals 等人的多项式查询下界](https://arxiv.org/abs/quant-ph/9802049)。

### 07｜代表性量子算法

- 查了 Simon 承诺和 $s^\perp$ 采样、Grover 未知解数、Shor 阶与连分数的最小阶陷阱、Trotter 交换子界、qDRIFT 平均信道口径、HHL 后选择以及幅度估计定理。
- 对 $H=X+Z,t=0.2$ 独立矩阵计算，$r=4$ 的谱范数误差是 $0.009869971709$，$r=20$ 是 $0.001973461982$，与正文表相合；两者分别低于 $0.01$ 与 $0.002$ 的交换子上界。$N=35,a=2$ 的阶 12、$171/2048$ 的连分数和余数检查也已逐项核对。
- qDRIFT 原文已区分平均信道界与单条随机线路，HHL 原文已把 $C/\lambda_j$ 的负号和成功概率写明，本轮未改。
- 来源：[Shor 原论文](https://doi.org/10.1137/S0097539795293172)、[Childs 等人的交换子误差分析](https://doi.org/10.1103/PhysRevX.11.011020)、[Campbell 的 qDRIFT 原论文](https://arxiv.org/abs/1811.08017)、[Brassard 等人的幅度估计原论文](https://arxiv.org/abs/quant-ph/0005055)。

### 08｜应用与变分算法

- 查了 VQE 变分不等式的适用对象（精确期望值而非有限样本报告值）、$H=0.7Z+0.2X$ 的本征值、方差与样本分配、单边及三顶点路径 QAOA、QUBO 的 Pauli 展开、幅度估计的访问模型和 2026 年预印本措辞。
- 独立按三比特矩阵指数复算 $\beta=\pi/8,\gamma=\pi/3$ 的路径 QAOA 期望值，得 $1.6495190528383283$；解析式 $1+3\sqrt3/8$ 为 $1.649519052838329$。VQE 约 7780 次的“规划数”确为正态近似和固定单点，不被写成严格总成本。
- 核对 2026 年 [Floquet 多体观测量预印本](https://arxiv.org/abs/2607.24937)的 74 qubit、预印本性质与作者自述经典方法在所选区域未收敛；[困难线路采样预印本](https://arxiv.org/abs/2607.25941)和[另一观测量预印本](https://arxiv.org/abs/2607.25998)确有相应任务。原文没有把它们写成一般 VQE/QAOA 的实用优势定论，本轮未改。
- QAOA 解析式来源：[Wang 等人的原论文](https://arxiv.org/abs/1706.02998)。上述近期预印本随版本、复现和经典基线进展仍需更新。

### 13｜量子信息量度

- 查了熵和负条件熵、相对熵支持空间、Helstrom 判别、无歧义判别、根保真度约定、Holevo 上界与可访问互信息、无广播与熵不等式方向。
- 对等先验 $|0\rangle,|+\rangle$ 的无歧义 POVM，复验 $E_?$ 特征值约为 $0,0.828427125$，单态正确辨认率为 $1-1/\sqrt2\approx0.292893219$。Holevo 量 $\approx0.601$ bit 与可访问互信息 $\approx0.399$ bit 是不同对象。正文已说明根保真度 $F$ 与文献中常用的 $F^2$，未改。
- 来源：[Watrous 的量子信息教材](https://cs.uwaterloo.ca/~watrous/TQI/)、[Levitin 的二元态最优测量原工作](https://link.springer.com/chapter/10.1007/978-1-4899-1391-3_43)、[Barnum 等人的无广播定理](https://doi.org/10.1103/PhysRevLett.76.2818)。

### 16｜高级算法与验证

- 查了多项式查询下界、任意有限群 HSP 的查询/时间区分、四元素 Fourier 采样、四环两步 walk、element distinctness 的 $N^{2/3}$ 成本、LCU/block encoding 与 QSVT 的接口、经典阴影和能隙保真度证书。
- 复验 $H=0.6X+0.8Z$ 的谱范数恰为 1、LCU 归一化 $\lambda=1.4$、输入 $|0\rangle$ 的辅助位 0 概率 $25/49\approx0.51020408$。经典阴影单次 $Z$ 估计取值 3 或 0，均值 1、方差 2；能隙例中 $E-E_0\le0.10,\Delta=0.40$ 的占据下界为 0.75。
- 来源：[Ettinger–Høyer–Knill 的一般 HSP 查询论文](https://arxiv.org/abs/quant-ph/0401083)明确“多对数于群大小的查询”并不保证多项式时间；[Magniez 等人的量子行走搜索论文](https://arxiv.org/abs/quant-ph/0608026)说明建立、更新、检查成本；[Huang–Kueng–Preskill 的经典阴影论文](https://arxiv.org/abs/2002.08953)；[Haah 等人的态层析样本界](https://arxiv.org/abs/1508.01797)。本轮未改。

### 18｜信道、容量与复杂度

- 查了纯化和 Uhlmann 根保真度、未归一化 Choi 的 CP/TP 条件、Stein 引理的 i.i.d. 与错误方向、四种容量的资源模型、擦除信道的四个容量、负性/PPT、QMA/QIP、无共享随机性的量子指纹和连续变量方差约定。
- 复验 Bell 加白噪声 $p=0.6$ 的部分转置谱 $0.4,0.4,0.4,-0.2$，负性 0.2；擦除率 $\varepsilon=1/4$ 的 $C,Q,P,C_E$ 依次为 $0.75,0.50,0.50,1.50$。量子指纹的重复误报界 $(5/8)^{10}\approx0.0091$。
- 修订 §4.5：原文经典容量上界只用“每个未擦除 qubit 至多 1 bit”解释，未显式覆盖跨多次使用的纠缠输入。现在以擦除位置 $S$ 条件化，在**无预共享纠缠**的容量模型下用 Holevo 维数界得 $I(X:B,S)\le\mathbb E|S|=n(1-\varepsilon)$；再写出 Fano 不等式和数据处理，说明误码率趋零才推出速率上界。可达率仍由正交编码化为经典二元擦除信道得到。
- 来源：[Bennett–DiVincenzo–Smolin 的擦除信道论文](https://arxiv.org/abs/quant-ph/9701015)；[Schumacher–Westmoreland 的经典容量定理](https://doi.org/10.1103/PhysRevA.56.131)；[Devetak 的私密与量子容量论文](https://arxiv.org/abs/quant-ph/0304127)明确私密容量/密钥生成率和前向公共通信的关系；[Wilde 的量子信息论教材作者公开稿](https://markwilde.com/qit-notes.pdf)列出擦除信道经典容量；[Jain 等人的 QIP=PSPACE 论文](https://arxiv.org/abs/0907.4737)。

## 边界与交接

- 已改动的两篇仅为 05、18；没有新增练习题，因此共享练习答案无需同步修改。
- 本轮核对是按抽样公式、主要定理与每个显式数值例的深审，不能取代对所有引文逐句校勘，也不能替代未来对 2026 年预印本、硬件与复杂度研究的持续更新。
- 新增公式需要主代理在全书阅读版重建时再做 KaTeX 和移动布局检查；本组独立运行的既有量子力学计算脚本 `node tools/reader/check-qm-examples.mjs` 已通过，但它不覆盖新增 Fano 推导。
