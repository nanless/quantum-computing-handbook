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
| $I(A:C\mid B)$ | 条件互信息，$S(AB)+S(BC)-S(B)-S(ABC)$；经典对角模型用$H$替换$S$，不等于普通互信息必然变小 |
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
| $\Omega$（连续变量） | 交错排序$(q_1,p_1,\ldots)$下的辛形式$\bigoplus_j\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)$，使$[R_j,R_k]=i\Omega_{jk}$；不同于Rabi角频率、渐近下界和最大纠缠向量$|\Omega\rangle$ |

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

- 多比特数学记号默认写成 $|q_{n-1}\cdots q_1q_0\rangle$，左边是高位；两比特列向量按 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$ 排列。
- “第几个量子比特”可能按线路从上到下编号，“第几个向量分量”则从 1 开始计数；涉及二者时必须明确说明。例如四维列向量的第 3 个分量对应 $|10\rangle$。
- 电路图从左向右读；算符乘积从右向左作用。
- 具体 SDK 可能用小端序显示字符串。软件示例必须另行注明，不把显示习惯混入数学定义。

实验可显式声明另一种寄存器排列，例如路由实验用 $|q_0q_1q_2\rangle$ 且 $q_0$ 在最高位。量子比特编号不是固有的二进制权重；每个例子必须列出寄存器顺序、基向量次序和软件显示规则，不能在一次计算中静默切换。

## 跨章与软件核对：相同字母怎样辨认对象

本书允许不同主题复用常用字母；对象的定义、维度与单位才决定公式的含义。比如门$H$是无量纲二维矩阵，Hamiltonian $\mathcal H$有能量单位，$H(X)$又是以bit计的经典熵。复制公式时连同附近定义一起复制，不能只凭字母选择计算程序。

| 容易混用的对象 | 本书与程序核对规则 |
|---|---|
| $F$、$F^2$与Bell重叠 | 本书$F(\rho,\sigma)=\|\sqrt\rho\sqrt\sigma\|_1$为根保真度；纯态重叠概率、Bell态重叠$\langle\Phi|\rho|\Phi\rangle$及有些软件的`fidelity`为平方口径；每次明确是否开根号 |
| $\Omega$的多个用法 | Q3的Rabi角频率有rad/s单位；第18章的辛形式是无量纲矩阵；$\Omega(g)$是渐近下界，$|\Omega\rangle$是Choi定义中的未归一化纠缠向量；四个对象由自变量、ket和单位区分 |
| CV坐标与物理位置/动量 | 第18章$[q,p]=i$，Q4$[x,p]=i\hbar$；传入默认$\hbar=2$的软件时需显式参数或一致缩放，真空方差由整个坐标约定决定 |
| 多模排序 | 第18章采用$(q_1,p_1,\ldots,q_m,p_m)$；The Walrus采用$(q_1,\ldots,q_m,p_1,\ldots,p_m)$；以置换矩阵同时变换均值、协方差和辛形式，不能只重新排列一行 |
| $\mathcal E^\dagger$与$\mathcal E^{-1}$ | 前者是迹内积的伴随，使$\operatorname{Tr}[O\mathcal E(\rho)]=\operatorname{Tr}[\mathcal E^\dagger(O)\rho]$；不代表逆噪声，保迹信道的伴随保恒等算符 |
| $\mathcal B\circ\mathcal A$与门$VU$ | 都从右向左作用，即先$\mathcal A$或$U$；SDK `compose`/`front`另查定义，用非交换小例核验 |
| POVM、工具与条件态 | $E_m$规定概率；$\mathcal I_m$是结果$m$对应的完全正、迹不增映射；$\rho_m=\mathcal I_m(\rho)/p_m$只在$p_m>0$时定义，不能丢掉$p_m$再等权平均 |
| 协方差与方差 | $\operatorname{Var}(aX+bY)=a^2\operatorname{Var}X+b^2\operatorname{Var}Y+2ab\operatorname{Cov}(X,Y)$；同批测量必须保留联合记录，量子算符的对称协方差则另按章节定义 |
| $\Gamma$与$\gamma$ | 软件实践中的$\Gamma=\sum_j|c_j|$是无量纲重构系数；第05章$\gamma\in[0,1]$是指定阻尼概率，连续时间耗散率则应有时间倒数单位 |
| shots、设置与有效样本 | shots是执行/读数次数，设置是不同制备和测量组合；独立性或漂移决定能否直接使用二项式方差，复制日志不会增加有效信息 |

这些检查连接[逐章第三组练习](../labs/README.md)与[源码约定对照](software-practice.md)。一般公式的条件由对应章节证明，小规模输出一致只是实现核查。
