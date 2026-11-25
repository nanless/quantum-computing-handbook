# 符号表与全书统一契约

全书 26 章（主篇 `00`–`21` 与量子力学基础篇 `Q1`–`Q4`）、附录与配套代码共享同一套核心符号与单位约定。阅读不同章节或对接开源 SDK 时，若遇到复用字母（例如 $H$、$\Omega$、$\gamma$、$\chi$），先看上下文给出的对象类型、维度与单位即可准确区分。

## 1. 量子计算与信息核心符号

| 符号 | 含义与统一约定 |
|---|---|
| $i$ | 虚数单位，$i^2 = -1$ |
| $z^*$ | 复数共轭；若 $z = a + bi$，则 $z^* = a - bi$ |
| $\lvert z\rvert^2 = z^* z$ | 复数的模平方，结果为非负实数 $a^2 + b^2$；求测量概率一律取模平方 |
| $A^T,\; A^\dagger$ | 矩阵转置、共轭转置（Hermitian 共轭） |
| $\lvert\psi\rangle,\; \langle\psi\rvert$ | ket（列向量）与 bra（列向量共轭转置后的行向量） |
| $\lvert +\rangle,\; \lvert -\rangle$ | $(\lvert 0\rangle \pm \lvert 1\rangle)/\sqrt{2}$，Pauli-$X$ 的两个本征态 |
| $\langle\phi\vert\psi\rangle$ | 左共轭内积 $\sum_j \phi_j^* \psi_j$（与 NumPy `np.vdot(phi, psi)` 一致） |
| $\lvert a\rangle\langle b\rvert$ | 外积 / 秩一线性算符 |
| $\otimes$ | 张量积（表示子系统组合）；上下文明确时可省略 |
| $I$ | 恒等算符，维数由上下文决定 |
| $X, Y, Z$ | 单比特 Pauli 算符 |
| $H, S, T$（量子门） | Hadamard 门、相位门 $S = \operatorname{diag}(1, i)$、$T = \operatorname{diag}(1, e^{i\pi/4})$；第 02 章旋转门处正式引入 $S,T$，须与经典熵 $H(X)$、von Neumann 熵 $S(\rho)$ 及总时间 $T$ 区分 |
| $R_x(\theta), R_y(\theta), R_z(\theta)$ | 单比特旋转门 $R_j(\theta) = e^{-i\theta \sigma_j / 2}$，旋转角 $\theta$ 单位为弧度 |
| $\mathrm{CNOT}, \mathrm{CZ}, \mathrm{SWAP}, \mathrm{Toffoli}$ | 标准多比特门；默认高位（左位）控低位（右位），$\mathrm{Toffoli}$ 即三比特受控非门（CCNOT） |
| $H$ 或 $\mathcal H$（哈密顿量） | 生成时间演化的厄米算符，与 Hadamard 门不同；物理单位下演化为 $e^{-i\mathcal H t / \hbar}$，算法模型常取 $\hbar = 1$ |
| $\log_2,\; \ln$ | **全书对数底数契约**：信息论、熵、容量与比特数一律写 $\log_2$；自然对数（如 MWPM 边权 $\ln\frac{1-p}{p}$、热分布与弛豫）一律写 $\ln$；**严禁使用不标底数的裸对数** |
| $\rho$ | 密度矩阵，满足厄米 $\rho^\dagger = \rho$、正半定 $\rho \succeq 0$ 与保迹 $\operatorname{Tr}(\rho) = 1$ |
| $\operatorname{Tr},\; \operatorname{Tr}_B$ | 矩阵迹、对子系统 $B$ 求偏迹 |
| $\mathcal E,\; \mathcal F$ | 量子信道（完全正且保迹的线性映射，CPTP）；全书统一用 $\mathcal E, \mathcal F$ 表示信道，不再用 $\mathcal N$ 表示信道 |
| $K_k$ | 量子信道的 Kraus 算符，$\mathcal E(\rho) = \sum_k K_k \rho K_k^\dagger$，满足 $\sum_k K_k^\dagger K_k = I$ |
| $E_m$ | POVM 测量元素，满足 $E_m \succeq 0$ 且 $\sum_m E_m = I$，结果概率 $p_m = \operatorname{Tr}(\rho E_m)$ |
| $\mathcal I_m$ | 量子仪器（quantum instrument，亦称量子测量工具）的第 $m$ 个分支映射（完全正、迹不增），$\sum_m \mathcal I_m$ 保迹；当 $p_m = \operatorname{Tr}\mathcal I_m(\rho) > 0$ 时，条件后态为 $\rho_m = \mathcal I_m(\rho)/p_m$ |
| $\mathcal D_p,\; \widetilde{\mathcal D}_q$ | 退极化信道：$\mathcal D_p(\rho) = (1-p)\rho + p\frac{I}{2}$ 等价于随机 Pauli 形式 $\widetilde{\mathcal D}_q(\rho) = (1-q)\rho + \frac{q}{3}(X\rho X + Y\rho Y + Z\rho Z)$，其中 $q = \frac{3}{4}p$；Stim `DEPOLARIZE1(q)` 对应平均门不保真度 $r = 2q/3$ |
| $q = A p$ | 读出混淆矩阵约定：全书统一按**列随机**定义（列对应真实态、行对应报告结果）；部分软件按行存储，二者互为转置 |
| $z_i,\; s_i$（QUBO / Ising） | Pauli 特征值变量 $z_i = 1 - 2x_i$（$x_i=0 \leftrightarrow +1,\; x_i=1 \leftrightarrow -1$）；退火软件常用自旋 $s_i = 2x_i - 1 = -z_i$，一阶项反号、二阶项同号 |
| $\lVert v\rVert,\; \lVert A\rVert_1,\; \lVert A\rVert_\infty$ | 向量欧氏范数、矩阵迹范数 $\operatorname{Tr}\sqrt{A^\dagger A}$、算符谱范数（最大奇异值） |
| $\lVert\mathcal E - \mathcal F\rVert_\diamond$ | 信道判别所用的钻石范数（完全有界迹范数）；连续变量在平均能量上限 $E$ 下采用能量受限钻石范数 $\lVert\mathcal E - \mathcal F\rVert_{\diamond, E}$ |
| $A = W \Sigma V^\dagger$ | 非厄米矩阵奇异值分解（SVD）：一般教材常写 $A = U\Sigma V^\dagger$，**第 16 章为避免与块编码酉矩阵 $U$ 撞名，统一写为 $A = W\Sigma V^\dagger$**（$W,V$ 分别为左、右奇异酉矩阵，$\Sigma$ 为非负奇异值对角阵） |
| $O, \Omega, \Theta$ | 渐近上界、下界、同阶记号；使用时需同时说明输入规模、计算模型与常数边界 |
| $n, N$ | 复杂度章节中 $n$ 常指输入比特数，$N$ 常指候选项数或状态空间维数（常有 $N = 2^n$），两者不可混用 |
| $\oplus,\; \mathbb F_2,\; x \cdot y$ | 模 2 加法（异或）、二元有限域 $\{0,1\}$、$\mathbb F_2$ 上按位内积（结果取模 2） |
| $[[n, k, d]]$ | 用 $n$ 个物理量子比特编码 $k$ 个逻辑量子比特、码距为 $d$ 的量子纠错码 |
| $H(X),\; S(\rho)$ | 经典 Shannon 熵 $-\sum_x p(x)\log_2 p(x)$、量子 von Neumann 熵 $-\operatorname{Tr}(\rho\log_2 \rho)$ |
| $I(A:B),\; I(A:C\mid B)$ | 量子互信息 $S(A)+S(B)-S(AB)$、条件互信息 $S(AB)+S(BC)-S(B)-S(ABC)$ |
| $T(\rho,\sigma)$ | 迹距离 $\lVert\rho - \sigma\rVert_1 / 2$，决定最优单次量子态判别成功率 |
| $F(\rho,\sigma),\; F^2$ | 本书统一采用的**根保真度** $F(\rho,\sigma) = \operatorname{Tr}\sqrt{\sqrt\rho\sigma\sqrt\rho} = \lVert\sqrt\rho\sqrt\sigma\rVert_1$（纯态间为 $\lvert\langle\psi\vert\phi\rangle\rvert$）；重叠概率或平方保真度显式写作 $F^2$ 或 $f = \langle\psi\vert\rho\vert\psi\rangle$ |
| $F_{\mathrm{avg}},\; r = 1 - F_{\mathrm{avg}}$ | 平均门保真度及平均门不保真度（对所有纯输入态按 Haar 测度平均**平方**重叠），与根保真度 $F$ 口径不同 |
| $\chi$ | Holevo 量，$\chi = S(\sum_x p_x \rho_x) - \sum_x p_x S(\rho_x)$，给出经典信息提取的普适上界 |
| $\lvert\Omega\rangle = \sum_i \lvert i\rangle\lvert i\rangle$ | 未归一化最大纠缠向量（范数平方为 $d_A$），用于第 18 章构造 Choi 矩阵 |
| $J_{\mathcal E}$ | 未归一化 Choi 矩阵 $J_{\mathcal E} = \sum_{i,j} \lvert i\rangle\langle j\rvert \otimes \mathcal E(\lvert i\rangle\langle j\rvert)$；$J_{\mathcal E} \succeq 0$ 等价于完全正，$\operatorname{Tr}_B J_{\mathcal E} = I_{A'}$ 等价于保迹 |
| $D(\rho\Vert\sigma),\; D_H^\epsilon(\rho\Vert\sigma)$ | 量子相对熵 $\operatorname{Tr}[\rho(\log_2\rho - \log_2\sigma)]$、第一类错误不超过 $\epsilon$ 的假设检验相对熵 |
| $I_c(\rho,\mathcal E)$ | 相干信息 $S(B) - S(RB) = -S(R\mid B)$，正则化后决定量子容量 |
| $C, Q, P, C_E$ | 无辅助经典容量、量子容量、私密经典容量、纠缠辅助经典容量 |
| $\mathcal N(\rho),\; E_N(\rho),\; C_{\mathrm{conc}}(\rho)$ | 二分态**负性** $\mathcal N(\rho) = (\lVert\rho^{T_B}\rVert_1 - 1)/2$、对数负性 $E_N(\rho) = \log_2(1 + 2\mathcal N(\rho))$、两比特共生度 $C_{\mathrm{conc}}(\rho)$（避免与经典容量 $C$ 混淆） |
| $\hat q, \hat p,\; V,\; W(q,p)$ | 第 18 章连续变量无量纲正交分量（满足 $[\hat q,\hat p] = i$）、协方差矩阵（真空态 $V = I/2$）与相空间 Wigner 准概率函数 |
| $\Omega$（连续变量辛形式） | 交错排序 $(q_1, p_1, \ldots, q_m, p_m)$ 下的块对角辛形式 $\bigoplus_j \bigl(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\bigr)$，使 $[R_j, R_k] = i\Omega_{jk}$ |
| $p_{\mathrm{eq}}$ | 第 05 章广义振幅阻尼（GAD）稳态的激发态 $\lvert 1\rangle$ 占据概率（无量纲，$p_{\mathrm{eq}}\in[0,1]$，不动点 $\rho_{\mathrm{eq}}=\operatorname{diag}(1-p_{\mathrm{eq}}, p_{\mathrm{eq}})$）；专记 $p_{\mathrm{eq}}$ 以区别于 Bloch 坐标 $r_z$ 与门错误率 $r$ |
| $\Lambda$ | 第 10、11 章量子纠错码的逻辑错误抑制因子（无量纲），刻画码距每增 $\Delta d = 2$ 时每轮逻辑错误率的压低倍数 $\Lambda \approx p_L(d)/p_L(d+2)$；$\Lambda > 1$ 表征物理噪声低于阈值 |
| $\mathrm{LF},\; \mathrm{EPLG}$ | 第 11 章并行门层系统基准（无量纲）：全链层保真度 $\mathrm{LF} = \prod_{\ell}\prod_{j\in\ell} F_{p,j}$ 与每层单双比特门等效错误率 $\mathrm{EPLG} = 1 - \mathrm{LF}^{1/n_{2Q}}$ |
| $\gamma_{\mathrm{PEC}}$ | 第 08、11、14 章概率误差抵消（PEC）的准概率 1-范数采样开销因子（无量纲，$\gamma_{\mathrm{PEC}} = e^{2\sum r_j} \ge 1$）；单层方差按 $\gamma_{\mathrm{PEC}}^2$ 放大，深 $L$ 层线路按 $\gamma_{\mathrm{PEC}}^{2L}$ 放大 |
| $S_q, S_p$（GKP 晶胞 $4\pi$） | 第 18 章无量纲相空间 $[\hat q,\hat p]=i$ 下方形 GKP 码位移稳定子 $S_q = e^{i2\sqrt\pi\hat q}$、$S_p = e^{-i2\sqrt\pi\hat p}$；对易相因子 $e^{4\pi i}=1$，围出相空间晶胞面积 $(2\sqrt\pi)^2 = 4\pi$，恰好容纳 $2$ 维逻辑量子比特 |
| $F_C(\theta)$ | 第 20 章经典 Fisher 信息，$F_C(\theta) = \sum_{x:\,p(x\mid\theta)>0}[\partial_\theta p(x\mid\theta)]^2 / p(x\mid\theta)$，单位 $[\theta]^{-2}$；决定固定测量装置下的经典 Cramér–Rao 下界 $\Delta\theta \ge 1/\sqrt{\nu F_C(\theta)}$ |
| $F_Q(\rho_\theta)$ | 第 20 章量子 Fisher 信息，$F_Q(\rho_\theta) = \operatorname{Tr}(\rho_\theta L_\theta^2)$，单位 $[\theta]^{-2}$；纯态幺正演化 $\lvert\psi_\theta\rangle = e^{-i\theta H}\lvert\psi_0\rangle$ 下化为 $F_Q = 4(\Delta H)^2$，给出一切合法量子测量的精度终极下界 |
| $L_\theta$ | 第 20 章对称对数导数（SLD），满足 $\partial_\theta\rho_\theta = \frac{1}{2}(\rho_\theta L_\theta + L_\theta\rho_\theta)$ 的厄米算符，单位 $[\theta]^{-1}$；其本征基构成饱和量子 Cramér–Rao 界的最优投影测量 |
| $\xi_R^2$ | 第 20 章 Wineland 自旋压缩参数（无量纲），$\xi_R^2 = N(\Delta J_\perp)^2 / \lvert\langle\vec J\rangle\rvert^2$；相干自旋态取 $\xi_R^2 = 1$，$\xi_R^2 < 1$ 表征突破标准量子极限且为多体纠缠的充分判据 |
| $\mathrm{SQL},\; \mathrm{HL}$ | 第 20 章精密测量基准标度：标准量子极限（$\Delta\phi_{\mathrm{SQL}} = 1/\sqrt{N}$，无纠缠探针满足 $F_Q \le N$）与海森堡极限（$\Delta\phi_{\mathrm{HL}} = 1/N$，$F_Q = N^2$）；对应无量纲相位估计误差随探针数 $N$ 的标度 |
| $(x\mid z)\in\mathbb{F}_2^{2n},\; r$（Tableau） | 第 21 章 $n$-比特 Pauli 串的二元辛向量编码（$x,z\in\mathbb{F}_2^n$，相位位 $r\in\mathbb{F}_2$ 表示符号 $(-1)^r$，无量纲）；Aaronson–Gottesman 稳定子表将其组织为 $2n\times(2n+1)$ 二元矩阵（前 $n$ 行为去稳定子、后 $n$ 行为稳定子） |
| $\chi$（MPS 键维） | 第 21 章矩阵乘积态（MPS）相邻格点虚拟键的最大维数（无量纲正整数），存储代价 $O(n\chi^2)$；注意按上下文与第 13 章 Holevo 量 $\chi$ 区分 |
| $w(P)$ | 第 21 章 $n$-比特 Pauli 串 $P$ 的权重（非恒等单比特因子 $X,Y,Z$ 的个数，无量纲整数 $0\le w(P)\le n$）；局域退极化伴随通道下按 $(1-p)^{w(P)}$ 衰减 |
| $\chi_{\mathrm{stab}}$（亦简记 $\chi_S$） | 第 21 章精确稳定子秩（无量纲正整数），即将纯态分解为稳定子态线性叠加所需的最少项数；与无量纲稳定子展度 $\xi(\lvert\psi\rangle)$ 共同刻画魔术度与扩展稳定子模拟复杂度 |

## 2. 量子力学基础篇与硬件控制物理符号

| 符号 | 含义与单位约定 |
|---|---|
| $h,\; \hbar = h/(2\pi)$ | 普朗克常数与约化普朗克常数，单位 $\mathrm{J\cdot s}$；物理篇中显式保留，不默认取 1 |
| $[A, B] = AB - BA$ | 对易子，衡量交换两算符作用顺序产生的差 |
| $\langle A\rangle,\; \Delta A$ | 同一量子态制备下可观测量的期望值与标准差，$(\Delta A)^2 = \langle A^2\rangle - \langle A\rangle^2$ |
| $E_n,\; \omega,\; f$ | 能级能量（$\mathrm{J}$）、角频率（$\mathrm{rad/s}$）、普通频率（$\mathrm{Hz}$）；满足 $\omega = 2\pi f$，能隙 $\hbar\omega = hf$ |
| $\Omega,\; \Delta,\; \Omega_{\mathrm{eff}}$ | 驱动 Rabi 角频率、**全书统一计算基失谐 $\Delta = \omega_d - \omega_0$**（驱动角频率减跃迁角频率）、有效 Rabi 角频率 $\sqrt{\Omega^2 + \Delta^2}$，单位均为 $\mathrm{rad/s}$ 或 $\mathrm{rad/ns}$ |
| $Z_E,\; Y_E,\; \delta_E$ | 常见原子物理与核磁共振教材使用的能量基符号：$Z_E = \lvert 1\rangle\langle 1\rvert - \lvert 0\rangle\langle 0\rvert = -Z$，$Y_E = -Y$，$\delta_E = \omega_0 - \omega_d = -\Delta$。因 $\Delta Z = \delta_E Z_E$，两套约定生成的哈密顿量矩阵元完全相同（详见 [Q3 第 6.2 节](../quantum-mechanics/03-levels-control.md#62-彻底消除跨章失谐符号坑计算基与能量基的等价对照表)与[第 14 章第 5.1 节](../14-compilation-control.md#51-旋转坐标系模型与跨章符号对齐)） |
| $T_1,\; T_2^*,\; T_2,\; T_\phi$ | 能量弛豫时间、含低频静态展宽的自由感应退相干时间、回波退相干时间与纯退相位时间；满足 $1/T_2 = 1/(2T_1) + 1/T_\phi$ |
| $\beta/\alpha$（DRAG 系数） | 第 14 章 DRAG 正交导数整形脉冲 $Q(t) = -(\beta/\alpha)\dot I(t)$ 的比例系数，其中 $\beta$ 为无量纲缩放系数、$\alpha = \omega_{12} - \omega_{01}$ 为非谐性角频率（单位 $\mathrm{rad/s}$），故 $\beta/\alpha$ 单位为 $\mathrm{s}$（或 $\mathrm{ns}$）；用于同步抑制 $\lvert 1\rangle\to\lvert 2\rangle$ 泄漏与 AC Stark 相移 |
| $\delta(t)$（动态解耦噪声） | 第 14 章量子比特空闲期的低频随机失谐角频率噪声，单位 $\mathrm{rad/s}$，对应噪声哈密顿量 $H_{\mathrm{noise}}(t) = \frac{\hbar}{2}\delta(t)Z$ 与调制累积相位 $\phi(T) = \int_0^T s(t)\,\delta(t)\,dt$ |
| $\psi(x,t),\; \phi_n(x),\; j(x,t)$ | Q4 一维位置波函数（单位 $\mathrm{m}^{-1/2}$）、定态空间波函数与概率流密度 |
| $\hat x,\; \hat p$ | Q4 物理位置与动量算符，满足 $[\hat x, \hat p] = i\hbar$；不要与第 18 章无量纲正交分量混用 |
| $\hat a,\; \hat a^\dagger,\; \hat N$ | 谐振子降阶、升阶与粒子数算符，$\hat N = \hat a^\dagger \hat a$（非酉算符） |
| $k,\; \kappa$ | Q4 势垒外波数与势垒内衰减常数，单位均为长度的倒数（$\mathrm{m}^{-1}$） |

## 3. 基顺序与线路顺序

- **高位在左（大端序）默认**：多比特计算基的列向量与张量积一律默认**高位在左**——两比特列向量依次对应 $\lvert 00\rangle, \lvert 01\rangle, \lvert 10\rangle, \lvert 11\rangle$，第 3 个分量对应 $\lvert 10\rangle$。在寄存器下标约定上，第 01–07、13 章常将左位记为 $A$（高位）、右位记为 $B$（低位），多比特二进制串也常将最高位写在左端；第 14–15 章的路由、编译与本地模拟器则按电路线序写作 $\lvert q_0 q_1\cdots q_{n-1}\rangle$，将 $q_0$ 置于最左高位（同样满足高位在左）。
- **时间与乘积反向**：量子电路图从左向右读取执行顺序；矩阵乘积从右向左作用，先做 $U$ 再做 $V$ 写作 $VU\lvert\psi\rangle$，信道复合同理写作 $\mathcal B \circ \mathcal A$。
- **小端序软件显示显式标注**：Qiskit 等部分软件默认采用**小端序**（little-endian）打印测量位串与排布态矢量，将电路第 0 条线 $q_0$ 置于最右低位（记作 $\lvert q_{n-1}\cdots q_1 q_0\rangle$，右端为 $q_0$）；每次在不同下标顺序或端序之间切换，都必须在公式与代码旁写明寄存器排列及位串规则，绝不在同一次推导中静默切换。

## 4. 跨章与开源软件核对速查表

把正文公式搬进程序或对照不同教材时，下面这些同名异义或口径差异最容易引发隐蔽错误，动笔和写代码前值得逐条过一遍：

| 容易混用的对象 | 全书统一标准与软件核对规则 |
|---|---|
| **$F$、$F^2$ 与 Bell 重叠** | 本书 $F(\rho,\sigma) = \lVert\sqrt\rho\sqrt\sigma\rVert_1$ 为根保真度；实验论文常报的态重叠概率 $\langle\Phi\vert\rho\vert\Phi\rangle$ 与 The Walrus 等库的 `fidelity` 往往采用平方口径 $F^2$，比较前先核对是否开根号 |
| **失谐 $\Delta$ 与 $\delta_E$** | Q3 与第 14 章已统一采用计算基 $Z = \lvert 0\rangle\langle 0\rvert - \lvert 1\rangle\langle 1\rvert$ 与 $\Delta = \omega_d - \omega_0$；阅读采用能量基 $H_0 = +\frac{\hbar\omega_0}{2}Z_E$ 的文献时，用 $Z_E = -Z,\; \delta_E = -\Delta$ 换算，同时核对时间单位（$\mathrm{rad/s}$ vs $\mathrm{rad/ns}$） |
| **$\Omega$ 的四种用法** | Q3 / 第 14 章的 Rabi 角频率带 $\mathrm{rad/s}$ 单位；第 18 章的辛形式 $\Omega$ 是无量纲矩阵；$\Omega(g)$ 是渐近下界；$\lvert\Omega\rangle$ 是未归一化最大纠缠向量。四者靠单位、参数与 ket 清晰区分 |
| **信道 $\mathcal E,\mathcal F$ 与负性 $\mathcal N(\rho)$** | 全书量子信道统一用 $\mathcal E, \mathcal F$，第 18 章纠缠负性专用 $\mathcal N(\rho)$；翻阅其他教材用 $\mathcal N$ 表示信道时，注意不要和负性混为一谈 |
| **SVD 与 QSVT 奇偶变换** | 第 16 章写 $A = W\Sigma V^\dagger$ 以区分块编码酉阵 $U$；非厄米矩阵的 QSVT 奇多项式输出 $W P_{\mathrm{odd}}(\Sigma) V^\dagger$、偶多项式输出 $V P_{\mathrm{even}}(\Sigma) V^\dagger$（或左侧版本），不能写成普通矩阵多项式 $P(A)$ |
| **QSP 相位与提取分量** | 对称 `sym_qsp` 常把实目标多项式放在 $\operatorname{Im} U_{00}$；完整复矩阵元 $U_{00}$、模平方与虚部平方是三个不同量。保存相位序列时须同时记录信号矩阵、乘积顺序、提取分量与多项式基（Chebyshev 基 vs 幂基） |
| **连续变量 $\hbar$ 与多模排序** | 第 18 章取 $[\hat q,\hat p]=i$（真空 $V=I/2$）与交错序 $(q_1,p_1,\ldots,q_m,p_m)$；Q4 物理坐标保留 $\hbar$；The Walrus 默认 `hbar=2` 且采用分组序 $(q_1,\ldots,q_m,p_1,\ldots,p_m)$，对照时须用置换矩阵并显式传入 `hbar=1` 或整体缩放 |
| **$\mathcal E^\dagger$ 与 $\mathcal E^{-1}$** | $\mathcal E^\dagger$ 是迹内积伴随（满足 $\operatorname{Tr}[O\mathcal E(\rho)] = \operatorname{Tr}[\mathcal E^\dagger(O)\rho]$，Heisenberg 演化与 Pauli 传播所用），不是噪声的逆信道；保迹信道的伴随保恒等算符 $\mathcal E^\dagger(I) = I$ |
| **$\mathcal B\circ\mathcal A$ 与 SDK `compose`** | 数学复合从右向左作用；不同 SDK 的 `compose` / `front` 参数方向不一，先用两个不对易的小矩阵实测方向，不只靠方法名猜测 |
| **$\Gamma$、$\gamma$ 与 $\gamma_{\mathrm{PEC}}$** | 大小写含义不同：$\Gamma = \sum_j \lvert c_j\rvert$ 在 MPF / QPD 中是无量纲系数绝对值和，第 19 章玻色存储中的 $\Gamma$ 则是带时间倒数单位的有效衰减率；$\gamma_{\mathrm{PEC}} = e^{2\sum r_j}$ 是 PEC 准概率采样放大因子（方差按 $\gamma_{\mathrm{PEC}}^2$ 增长）。小写 $\gamma$ 在第 05 章与 Q2 中为 $[0,1]$ 阻尼概率（$\gamma(t)=1-e^{-\kappa t}$），在 Q1 中为复路径记录重叠 $\langle d_1\vert d_0\rangle$，在 Q3 自旋例中为旋磁比，在 QAOA 中为旋转角 |
| **Lindblad 累积率 $r_j$ 与 Pauli 错率 $p_j$** | 在稀疏 Pauli 噪声模型（SLC / PNA）中，无量纲累积率 $r_j$ 与单次翻转概率满足 $p_j = (1 - e^{-2r_j})/2$，二者只在极小噪声下近似相等 |
| **GRAPE 二能级与三能级子空间保真度** | 二能级酉门中 $g = \lvert\operatorname{Tr}(U_{\mathrm{tar}}^\dagger U)\rvert/2$、过程重叠 $g^2$、平均门保真度 $F_{\mathrm{avg}} = (2g^2 + 1)/3$；三能级模型中截断到计算子空间的 $2\times 2$ 块 $M$ 不再酉，不后选择的 Haar 平均平方重叠为 $(\operatorname{Tr}(M^\dagger M) + \lvert\operatorname{Tr}(V^\dagger M)\rvert^2)/6$，不能直接套二能级公式 |
| **HHL 三种成功口径** | 需严格区分“辅助位成功”、“辅助位成功且相位寄存器清零”与“辅助位成功但相位有残余”；若只测辅助位，须对相位寄存器求偏迹并用混态根保真度评价，不能直接拿理想纯态分支对比 |
| **GST 的 Liouville 坐标与规范自由度** | 门集层析常用归一化 Pauli 基 $(I,X,Y,Z)/\sqrt{2}$ 表示过程矩阵；规范（gauge）变换同时变换制备、门与测量而保持一切预测概率不变，因此不能脱离规范逐格比对过程矩阵元素 |
| **概率分母、有效样本与聚类标准误** | 后选择统计须同时报告条件保留数与总尝试数；同一随机化电路内的所有 shots 共享同一噪声逆采样设置，估算标准误须按独立随机化批次计算聚类标准误（cluster SE），不能把总 shots 数直接当作独立样本量 |
| **$\chi$、$\chi_{\mathrm{stab}}$（$\chi_S$）与保真度口径** | 第 13 章 $\chi$ 为 Holevo 量（单位 bit）；第 21 章 $\chi$ 为无量纲 MPS 键维、$\chi_{\mathrm{stab}}$（章内亦简记 $\chi_S$）为稳定子秩。另在第 20 章由 Bures 距离算 QFI 时，采用本书根保真度系数为 $8$（$F_Q = 8\lim_{\delta\to 0}[1 - F(\rho_\theta,\rho_{\theta+\delta})]/\delta^2$），平方保真度文献则写系数 $4$ |

## 5. 一页高频核心公式速查表

下表按全书五篇 26 章归纳最常翻查的核心公式；全部沿用左共轭内积、大端序、$\log_2/\ln$ 明确底数与根保真度 $F$ 契约。

| 篇目与主题 | 高频核心公式 |
|---|---|
| **第一篇｜量子态、测量与 Bloch 球**（00–05、Q1–Q2） | $p_m = \operatorname{Tr}(\rho E_m)$，$\rho = \frac{1}{2}(I + r_x X + r_y Y + r_z Z)$（$\lvert\vec r\rvert \le 1$） |
| **第一篇｜动力学、不确定关系与 GAD**（Q2、05） | $U(t) = e^{-i\mathcal H t/\hbar}$，$\Delta A\,\Delta B \ge \frac{1}{2}\lvert\langle[A,B]\rangle\rvert$；$r_z' = (1-\gamma)r_z + \gamma(1-2p_{\mathrm{eq}})$ |
| **第二篇｜振幅放大与相位估计**（06–07） | $\lvert\psi_k\rangle = \sin((2k+1)\theta)\lvert\mathrm{good}\rangle + \cos((2k+1)\theta)\lvert\mathrm{bad}\rangle$，$k_{\mathrm{opt}} \approx \frac{\pi}{4}\sqrt{N/M}$ |
| **第二篇｜参数移位与零失败统计**（08、15） | $\partial_\theta\langle O\rangle = \frac{1}{2}\bigl(\langle O\rangle_{\theta+\pi/2} - \langle O\rangle_{\theta-\pi/2}\bigr)$；$p_{\mathrm{upper}} = 1 - \alpha^{1/N}$ |
| **第三篇｜驱动控制、退相干与 DRAG**（Q3、09、14） | $\Delta = \omega_d - \omega_0$，$\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}$，$Q(t) = -\frac{\beta}{\alpha}\dot I(t)$ |
| **第三篇｜纠错界与表面码压错**（10–11） | $2t + e < d$，$p_L(d) \approx A\Lambda^{-(d+1)/2}$（$\Lambda \approx p_{\mathrm{th}}/p > 1$） |
| **第三篇｜并行基准与 PEC 采样开销**（11、14、19） | $\mathrm{EPLG} = 1 - \mathrm{LF}^{1/n_{2Q}}$，$\gamma_{\mathrm{PEC}} = e^{2\sum r_j}$（$L$ 层方差放大 $\gamma_{\mathrm{PEC}}^{2L}$） |
| **第四篇｜QKD 安全率与无中继 PLOB 界**（12） | $r \ge 1 - h_2(e_b) - h_2(e_p)$，$C_{\mathrm{PLOB}}(\eta) = -\log_2(1-\eta)$ |
| **第四篇｜量子 Cramér–Rao 界与纯态 QFI**（20） | $\Delta\theta \ge \frac{1}{\sqrt{\nu F_Q(\rho_\theta)}}$，$F_Q(\lvert\psi_\theta\rangle) = 4(\Delta H)^2$ |
| **第四篇｜SQL / 海森堡极限与自旋压缩**（20） | $\Delta\phi_{\mathrm{SQL}} = \frac{1}{\sqrt{N}}$ vs. $\Delta\phi_{\mathrm{HL}} = \frac{1}{N}$，$\xi_R^2 = \frac{N(\Delta J_\perp)^2}{\lvert\langle\vec J\rangle\rvert^2} < 1$ |
| **第五篇｜熵、根保真度与 Holevo 界**（13、16、18） | $S(\rho) = -\operatorname{Tr}(\rho\log_2\rho)$，$F(\rho,\sigma) = \lVert\sqrt\rho\sqrt\sigma\rVert_1$，$I_{\mathrm{acc}} \le \chi$ |
| **第五篇｜稳定子辛内积与 MPS 截断**（21） | $(x_1\mid z_1)\odot(x_2\mid z_2) = x_1\cdot z_2 \oplus z_1\cdot x_2$，$\epsilon_{\mathrm{trunc}} = \sum_{i>\chi'}\sigma_i^2 = 1 - F^2$ |
| **第五篇｜含噪 Pauli 传播与 GKP 晶胞**（21、18） | $\mathcal D_p^\dagger(P) = (1-p)^{w(P)} P$，$S_q S_p = e^{4\pi i} S_p S_q$（$[\hat q,\hat p]=i$） |

配套程序校验与开源代码约定详见[逐章实验总览](../labs/README.md)与[算法、工业实践与开源代码对照](software-practice.md)。
