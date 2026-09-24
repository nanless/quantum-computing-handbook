# 第 31 轮调研：Q2 可观测量与时间演化

## 任务与产物

本轮负责新增 `handbook/quantum-mechanics/02-observables-dynamics.md`，并把 8 道自检题的完整答案写入 `work/research/round31-qm2-answers.md`，供总编统一并入练习附录。本轮没有修改其他章节、共享附录或图片。

章节定位为量子力学基础篇第二章，先修是全书第 01、02 章和基础篇 Q1。目标读者是初学者和入门研究生：保留可复算的有限维推导，同时把公设、数学结论、实验统计和适用边界分开。

## 一手与大学课程来源

1. H. P. Robertson, [“The Uncertainty Principle,” *Physical Review* 34, 163–164 (1929)](https://doi.org/10.1103/PhysRev.34.163)。APS 页面核实了作者、期刊、卷页、发表日期与 DOI。正文用它标注一般可观测量不确定关系的原始出处，没有从二手材料转引历史结论。
2. MIT OpenCourseWare, [22.51 Course Notes, Chapter 3: Axioms of Quantum Mechanics](https://ocw.mit.edu/courses/22-51-quantum-theory-of-radiation-interactions-fall-2012/9cdcc3c1e36da2ae3e2f925d5b435ab6_MIT22_51F12_Ch3.pdf)。讲义明确给出：可观测量测量结果为本征值、Born 概率、投影后态；期望值是重复测量的平均；兼容可观测量以对易定义；Robertson 关系从 Cauchy–Schwarz 和中心化算符推出。正文的教学顺序与此一致，但重新写成有限维投影语言并补足简并投影 $P_a$。
3. MIT OpenCourseWare, [8.04 Lecture 6: Time Evolution and the Schrödinger Equation](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/resources/mit8_04s13_lec06/)。用于核对本科层次的薛定谔方程、能量本征态和时间演化定位。
4. MIT OpenCourseWare, [8.321 Lecture 8: General Time Dependent Hamiltonians](https://ocw.mit.edu/courses/8-321-quantum-theory-i-fall-2017/579cb61c4eaa494b9adb90830d921099_MIT8_321F17_lec8.pdf)。讲义逐项区分三种情况：时不变 Hamiltonian；任意时刻两两对易，可对积分直接取指数；一般不对易，必须让较晚时间的演化算符排在左边。正文的两段 $X/Z$ 反例正是为初学者具体化这一点。
5. John Preskill, [*Foundations II: Measurement and Evolution*](https://www.preskill.caltech.edu/ph229/notes/chap3.pdf)。用于核对投影测量、非选择测量和封闭系统幺正演化与开放系统通道的边界。本章只讲封闭系统，不提前展开主方程。

## 教学结构与取舍

### 1. 测量从“可能结果”讲起

先写有限维厄米算符的谱分解

$$
A=\sum_a aP_a,
$$

再分别给出结果、概率和条件后态。这样避免初学者把“物理量对应厄米算符”误解成单次实验直接返回 $\langle A\rangle$。正文用 $Z$ 的 $\pm1$ 读数算例明确显示：期望值可为 $1/2$，但单次仪器读数不可能是 $1/2$。

本章限定理想尖锐可观测量；一般 POVM 已在全书第 02 章出现，不在这里重复扩展。对简并谱仍用 $P_a$ 投影到整个本征子空间，避免只适用于非简并本征值的写法。

### 2. Robertson 推导保留所有关键中间步

正文没有只引用结论，而是依次完成：

1. 定义 $\widetilde A=A-\langle A\rangle I$、$\widetilde B=B-\langle B\rangle I$；
2. 把方差写成向量范数；
3. 使用 Cauchy–Schwarz；
4. 令 $z=\langle\widetilde A\widetilde B\rangle$，从 $z-z^*$ 取出对易子；
5. 使用 $|z|^2\ge(\operatorname{Im}z)^2$；
6. 得到 $\Delta A\Delta B\ge|\langle[A,B]\rangle|/2$。

同时安排两个互补的 Pauli 例子：

- $Y$ 的 $+1$ 本征态上，$\Delta X=\Delta Z=1$，且 $[X,Z]=-2iY$，下界等于 1，关系饱和。
- Bloch 向量 $(1/\sqrt2,0,1/\sqrt2)$ 的实系数态上，$\langle Y\rangle=0$，Robertson 右端为零，但 $\Delta X=\Delta Z=1/\sqrt2$。这直接拆解“下界为零就是无不确定性”的常见误读。

没有扩展到 Robertson–Schrödinger 协方差加强式，因为当前目标是让初学者真正理解最小证明和状态依赖下界；加强式可在后续高阶章节出现。

### 3. 动力学明确标为公设

正文把

$$
i\hbar\frac{d}{dt}|\psi(t)\rangle
=\mathcal H(t)|\psi(t)\rangle
$$

称为封闭系统的动力学公设，没有伪装成从线性代数“证明”出的定律。随后才在时不变条件下验证

$$
U(t)=e^{-i\mathcal Ht/\hbar}
$$

满足微分方程、初值和酉性。

为避免全书两个常用 $H$ 混淆，本章用 $\mathcal H$ 表示 Hamiltonian，用 $H_{\rm Had}$ 表示 Hadamard 门，并专列判读规则。

### 4. 用谱分解连接定态与相对相位

从

$$
\mathcal H=\sum_nE_nP_n
$$

得到

$$
U(t)=\sum_ne^{-iE_nt/\hbar}P_n.
$$

能量本征态只积累全局相位，所以时间无关测量统计保持不变；不同能量的叠加态积累 $e^{-i(E_1-E_0)t/\hbar}$ 相对相位。此安排把第 01、02 章已有的“全局相位/相对相位”自然接到真实时间演化上。

### 5. 单量子比特算例保留量纲

正文实际推导：

$$
\mathcal H_Z=\frac{\hbar\omega}{2}Z
\Longrightarrow U_Z(t)=R_z(\omega t),
$$

$$
\mathcal H_X=\frac{\hbar\Omega}{2}X
\Longrightarrow U_X(t)=R_x(\Omega t).
$$

对 $X$ 驱动，从 $|0\rangle$ 得

$$
p(1,t)=\sin^2(\Omega t/2),
\qquad t_\pi=\pi/|\Omega|.
$$

若实验报告普通频率 $f=\Omega/(2\pi)$，则 $t_\pi=1/(2f)$。正文给出 $f=10\,\mathrm{MHz}\Rightarrow50\,\mathrm{ns}$；自检题另用 $25\,\mathrm{MHz}\Rightarrow20\,\mathrm{ns}$，防止读者只照抄示例数字。

### 6. 用两段操作证明普通积分不够

设置两段等时长脉冲，每段旋转 $\pi/2$：

$$
U_{X\to Z}=R_z(\pi/2)R_x(\pi/2),
$$

$$
U_{Z\to X}=R_x(\pi/2)R_z(\pi/2).
$$

二者对 $|0\rangle$ 分别给出（忽略全局相位）$|+\rangle$ 与 $|{-i}\rangle$。末态测 $X$ 的 $+1$ 概率分别为 1 和 $1/2$。两种时间安排却有相同的普通积分 $\pi(X+Z)/4$；因此单写 $\exp[-(i/\hbar)\int\mathcal Hdt]$ 无法同时正确。这个反例已经足以引入时间排序，无需在基础章展开 Dyson 级数。

## 独立复算

用矩阵计算复核了以下数值与恒等式：

- $[X,Z]=-2iY$；
- $|{+i}\rangle$ 上 $\Delta X\Delta Z=1$，Robertson 右端为 1；
- $\cos(\pi/8)|0\rangle+\sin(\pi/8)|1\rangle$ 上两个标准差均为 $1/\sqrt2$，右端为 0；
- $R_z(\pi/2)R_x(\pi/2)|0\rangle=e^{-i\pi/4}|+\rangle$；
- $R_x(\pi/2)R_z(\pi/2)|0\rangle=e^{-i\pi/4}|{-i}\rangle$；
- $\Omega/(2\pi)=25\,\mathrm{MHz}$ 时 $t_\pi=20\,\mathrm{ns}$；
- 自检第 1 题的 $\langle A\rangle=1/2$、$\Delta A=3/2$。

## 交付边界

- 新章含 8 道自检题，没有直接改共享练习附录；完整答案另存草稿。
- 答案链接按要求写为 `../appendices/exercises.md#量子力学-q2`。
- 本章没有新增科学 SVG；视觉资产由主审统一规划。
- 没有提前扩展连续谱算符的定义域、开放系统主方程、Dyson/Magnus 展开或 Robertson–Schrödinger 加强式，以免破坏基础篇的前置知识顺序。
