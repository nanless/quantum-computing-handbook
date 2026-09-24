# 符号表

| 符号 | 含义 |
|---|---|
| $i$ | 虚数单位，$i^2=-1$ |
| $z^*$ | 复数共轭 |
| $|z|^2=z^*z$ | 复数的模平方；若 $z=a+bi$，结果是非负实数 $a^2+b^2$ |
| $A^T$ | 转置 |
| $A^\dagger$ | 共轭转置 |
| $|\psi\rangle$ | ket，列向量 |
| $\langle\psi|$ | bra，$|\psi\rangle$ 的共轭转置 |
| $|+\rangle,|-\rangle$ | $(|0\rangle\pm|1\rangle)/\sqrt2$，即 $X$ 的两个本征态 |
| $\langle\phi|\psi\rangle$ | 内积 |
| $|a\rangle\langle b|$ | 外积/秩一算符 |
| $\otimes$ | 张量积；上下文明确时常省略 |
| $I$ | 恒等算符，维数由上下文决定 |
| $X,Y,Z$ | Pauli 算符 |
| $H,S,T$ | Hadamard 门、$S=\operatorname{diag}(1,i)$、$T=\operatorname{diag}(1,e^{i\pi/4})$；$T$ 也常称“$\pi/8$ 门” |
| $\rho$ | 密度矩阵 |
| $\operatorname{Tr}$ | 迹 |
| $\operatorname{Tr}_B$ | 对系统 $B$ 的偏迹 |
| $\mathcal E$ | 量子信道 |
| $K_j$ | Kraus 算子 |
| $\|v\|$ | 向量范数 |
| $\|A\|_\diamond$ | 信道差异常用的金刚石范数 |
| $O,\Omega,\Theta$ | 渐近上界、下界、同阶；常数及适用模型必须另行说明 |
| $n,N$ | 复杂度章节中 $n$ 常为输入位数，$N$ 常为候选项或矩阵维数；具体关系由问题给出，例如 $N=2^n$，二者不可随意互换 |
| $f=o(g)$；本书简写 $f\prec g$ | 当 $n\to\infty$ 时 $f(n)/g(n)\to0$；$\prec$ 是本书在增长率比较中的局部约定 |
| $\oplus$ | 比特异或，即模 2 加法 |
| $x\cdot y$ | 在 Simon 等算法中指 $\mathbb F_2$ 上的内积，结果取模 2 |
| $\mathbb F_2$ | 只含 0、1 的二元有限域，运算均取模 2 |
| $[[n,k,d]]$ | 用 $n$ 个物理量子比特编码 $k$ 个逻辑量子比特、码距为 $d$ 的量子码 |
| $H(X)$ | 经典 Shannon 熵 |
| $S(\rho)$ | von Neumann 熵 |
| $I(A:B)$ | 量子互信息 |
| $T(\rho,\sigma)$ | 迹距离，$\|\rho-\sigma\|_1/2$ |
| $F(\rho,\sigma)$ | 本书采用的根保真度 |
| $\chi$ | Holevo 量 |
| $|\Omega\rangle=\sum_i|i\rangle|i\rangle$ | 未归一化最大纠缠向量；第 18 章用它定义 Choi 矩阵 |
| $J_{\mathcal E}$ | 信道 $\mathcal E$ 的未归一化 Choi 矩阵；本书约定 $\operatorname{Tr}_B J_{\mathcal E}=I$ 表示保迹 |
| $D(\rho\|\sigma)$ | 量子相对熵；本书对数取底 2 |
| $D_H^\epsilon(\rho\|\sigma)$ | 第一类错误不超过 $\epsilon$ 时的假设检验相对熵 |
| $I_c(\rho,\mathcal E)$ | 输入 $\rho$ 通过信道 $\mathcal E$ 时的相干信息 |
| $C,Q,P,C_E$ | 无辅助经典容量、量子容量、私密经典容量、纠缠辅助经典容量 |
| $\mathcal N(\rho)$ | 二分态 $\rho$ 的负性；当 $\mathcal N$ 带信道自变量时也常表示信道，须由上下文区分 |
| $\hat q,\hat p$ | 连续变量正交分量；第 18 章采用 $[\hat q,\hat p]=i$ |
| $V$ | 连续变量态的协方差矩阵；第 18 章约定真空态 $V=I/2$ |

## 量子力学基础篇的物理符号

| 符号 | 含义与单位约定 |
|---|---|
| $h,\hbar=h/(2\pi)$ | 普朗克常数与约化普朗克常数，单位为焦耳秒；基础篇不默认它们等于 1 |
| $\mathcal H,\hat H$ | Hamiltonian，能量单位；区别于无量纲的 Hadamard 门 $H$ |
| $[A,B]=AB-BA$ | 对易子；交换两个算符的作用顺序所产生的差 |
| $\langle A\rangle,\Delta A$ | 同一制备下可观测量的期望值和标准差；$(\Delta A)^2=\langle A^2\rangle-\langle A\rangle^2$ |
| $U(t),R_\alpha(\theta)$ | 时间演化算符、绕指定轴的旋转门；指数中的角度为弧度 |
| $E_n,\omega,f$ | 能级、角频率（rad/s）、普通频率（Hz）；$\omega=2\pi f$，能隙为 $\hbar\omega=hf$ |
| $\Omega,\Delta,\Omega_R$ | Q3 中的驱动 Rabi 角频率、失谐 $\omega_0-\omega_d$、广义 Rabi 角频率 $\sqrt{\Omega^2+\Delta^2}$；均为 rad/s，不是渐近记号 $\Omega$ |
| $Z_E,Y_E$ | Q3 以低能态为逻辑 0 时采用的算符，$Z_E=-Z,Y_E=-Y$；这是该章明确指定的符号约定 |
| $\psi(x,t),\phi_n(x)$ | Q4 的位置波函数与定态空间部分；一维归一化波函数单位为长度的负二分之一次方 |
| $\hat x,\hat p$ | Q4 的物理位置、动量，满足 $[\hat x,\hat p]=i\hbar$；不要与第 18 章无量纲正交分量混用 |
| $\hat a,\hat a^\dagger,\hat N$ | 谐振子的降阶、升阶、数算符，$\hat N=\hat a^\dagger\hat a$；不是保持范数的量子门 |
| $k,\kappa$ | Q4 势垒外的波数与势垒内的衰减常数，单位均为长度的倒数 |

## 基顺序与线路顺序

- 多比特数学记号写成 $|q_{n-1}\cdots q_1q_0\rangle$，左边是高位；两比特列向量按 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$ 排列。
- “第几个量子比特”可能按线路从上到下编号，“第几个向量分量”则从 1 开始计数；涉及二者时必须明确说明。例如四维列向量的第 3 个分量对应 $|10\rangle$。
- 电路图从左向右读；算符乘积从右向左作用。
- 具体 SDK 可能用小端序显示字符串。软件示例必须另行注明，不把显示习惯混入数学定义。
