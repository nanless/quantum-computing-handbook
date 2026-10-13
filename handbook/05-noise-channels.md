# 05｜混态、噪声与量子信道

前几章常用一个列向量写状态；本章处理的是“不知道本轮制备了哪一个纯态”和“只看纠缠系统的一部分”时怎样继续算概率。数学若已生疏，先读 §1–2 的两种 $2\times2$ 矩阵和 §5 的具体噪声例子；§3 的完整测量工具、§4 的完全正反例，以及 §6–8 的实验指标可在遇到相应应用时回看。每遇到一张密度矩阵，先检查三件事：它是方阵、对角线之和为 1、算出的任何测量概率不能为负。

## 1. 为什么态矢量不够

先设一台经典随机装置每轮抛一枚公平硬币：正面就制备 $|0\rangle$，反面就制备 $|1\rangle$，随后不告诉接收者本轮是哪一面。**每一轮**系统仍有一个纯态；但接收者若只知道这个流程，就不能把所有轮次冒充成同一个 $|+\rangle$。各有一半的两种制备写成

$$
\rho_{\rm coin}
=\frac12|0\rangle\langle0|+\frac12|1\rangle\langle1|
=\frac12\begin{bmatrix}1&0\\0&0\end{bmatrix}
+\frac12\begin{bmatrix}0&0\\0&1\end{bmatrix}
=\begin{bmatrix}1/2&0\\0&1/2\end{bmatrix}.
$$

这种方阵叫**密度矩阵**。它的主对角线是两个计算基结果的概率，$1/2+1/2=1$；换一种测量基时，还要用整个矩阵来算，不能只记这两个对角数。第 2 节会拿它和每轮都制备 $|+\rangle$ 作对照。

概括起来，有两种常见原因不能只用单个 $|\psi\rangle$：

1. 制备过程以经典概率 $p_j$ 产生不同纯态 $|\psi_j\rangle$；
2. 系统与环境纠缠，而我们只观察系统的一部分。

两者都用密度矩阵描述；一般有限种制备的写法是

$$\rho=\sum_jp_j|\psi_j\rangle\langle\psi_j|,$$

其中 $p_j\ge0$ 且 $\sum_jp_j=1$；$|\psi_j\rangle$ 都已归一化。合法密度矩阵满足

$$
\rho=\rho^\dagger,\qquad \rho\succeq0,
\qquad \operatorname{Tr}\rho=1.
$$

这里 $\rho^\dagger=\rho$ 表示共轭转置后不变，$\operatorname{Tr}\rho=1$ 表示对角线之和为 1；$\rho\succeq0$ 表示对任意向量 $|v\rangle$ 都有 $\langle v|\rho|v\rangle\ge0$。这最后一条比“对角线都非负”更严格。[第 01 章第 6 节](01-math.md#6-迹密度矩阵与正半定用到时回看)用二维反例解释了原因。不同的制备方案可能给出同一个 $\rho$；仅测量当前系统无法区分这些等价的系综分解。

## 2. 纯态和混态

纯态满足

$$\rho^2=\rho,\qquad \operatorname{Tr}(\rho^2)=1.$$

混态满足 $\operatorname{Tr}(\rho^2)<1$。量 $\operatorname{Tr}(\rho^2)$ 称为纯度。对 $d$ 维归一化状态，

$$
\frac1d\le\operatorname{Tr}(\rho^2)\le1,
$$

下界由最大混态 $I/d$ 取得，上界由纯态取得。

### 算例：叠加与混合

$$
|+\rangle\langle+|
=\frac12\begin{bmatrix}1&1\\1&1\end{bmatrix},
$$

而以各 $1/2$ 概率制备 $|0\rangle$ 或 $|1\rangle$ 得

$$
\rho_{\rm mix}=\frac12|0\rangle\langle0|+
\frac12|1\rangle\langle1|
=\frac12\begin{bmatrix}1&0\\0&1\end{bmatrix}.
$$

两者计算基概率相同；非对角元使 $|+\rangle$ 在 $X$ 基测量时确定得到 $+$，而最大混态仍各半。用上面“纯度”的公式也可逐格核对：

$$
\rho_+^2
=\frac14\begin{bmatrix}1&1\\1&1\end{bmatrix}^2
=\frac14\begin{bmatrix}2&2\\2&2\end{bmatrix}
=\rho_+,
\qquad \operatorname{Tr}(\rho_+^2)=\frac12+\frac12=1.
$$

但 $\rho_{\rm mix}=I/2$，所以 $\rho_{\rm mix}^2=I/4$，其迹是 $1/4+1/4=1/2$。即使两者在某一种基上都是“各半”，纯度和另一种基的统计也会不同。纯度不是“我们对这轮知道多少”的简单百分比，而是这个系统密度矩阵的可计算性质。

## 3. 密度矩阵上的演化与测量

酉演化：

$$\rho\mapsto U\rho U^\dagger.$$

POVM 结果概率：

$$p(k)=\operatorname{Tr}(E_k\rho).$$

期望值：

$$\langle A\rangle=\operatorname{Tr}(A\rho).$$

这些公式同时覆盖纯态与混态。

它们还没有完整说明“测量之后怎样”。在这里的理想 Lüders 投影工具中，每个结果使用算子 $M_k=P_k$；若得到概率非零的结果 $k$，条件后态为

$$
\rho_k=\frac{P_k\rho P_k}{\operatorname{Tr}(P_k\rho)}.
$$

若测量已经发生但结果被丢弃，非选择后态是

$$
\rho'=\sum_kP_k\rho P_k.
$$

### 进阶回看：同一结果统计可以有不同测后态

先抓住上面两式：知道投影结果 $k$，要除以该结果的概率来归一化；不知道结果，要把所有分支相加。对本书讨论的有限维系统和有限个经典结果，完整测量过程还要同时给出经典结果和量子后态。沿用第 02 章的量子测量工具记号，对结果 $k$ 定义

$$
\mathcal I_k(\rho)=\sum_\alpha
M_{k\alpha}\rho M_{k\alpha}^\dagger,
\qquad
\sum_{k,\alpha}M_{k\alpha}^\dagger M_{k\alpha}=I.
$$

每个 $\mathcal I_k$ 是完全正、迹不增加的映射；把所有结果相加，$\sum_k\mathcal I_k$ 才是完全正、保迹的确定性过程。其 POVM 元为

$$
E_k=\sum_\alpha M_{k\alpha}^\dagger M_{k\alpha},
$$

因此

$$
p(k)=\operatorname{Tr}[\mathcal I_k(\rho)]
=\operatorname{Tr}(E_k\rho).
$$

若 $p(k)>0$，条件后态是 $\rho_k=\mathcal I_k(\rho)/p(k)$；忽略结果时则是 $\rho'=\sum_k\mathcal I_k(\rho)$。每个结果只用一个 $M_k$ 是特殊情形，不是一般定义。POVM 元只决定结果概率；同一组 $E_k$ 可以由不同的量子测量工具实现并产生不同后态。

把最后一句具体算出来。先按计算基测量，记 $P_0=|0\rangle\langle0|$、$P_1=|1\rangle\langle1|$。**方案甲**保留测得的态，取 $M_0=P_0,M_1=P_1$；**方案乙**测完后把结果为 1 的系统也复位到 $|0\rangle$，取 $N_0=P_0,N_1=|0\rangle\langle1|$。两套算子都满足完备关系，且

$$
M_k^\dagger M_k=N_k^\dagger N_k=P_k\qquad(k=0,1).
$$

因此对输入 $|+\rangle$，两种方案都以 $1/2$ 概率报告 0、以 $1/2$ 概率报告 1；只收集经典结果，实验数据完全相同。但若记录显示 1，方案甲的条件后态是 $|1\rangle\langle1|$，方案乙则是 $|0\rangle\langle0|$。丢弃记录后，甲给 $I/2$，乙给 $|0\rangle\langle0|$。想预测后续操作，不能只给出 POVM 的两个 $P_k$，还必须交代测量工具。

## 4. 量子信道与 Kraus 表示

物理允许的确定性量子过程用完全正、保迹映射（CPTP map）描述。有限维下可写成

$$\mathcal E(\rho)=\sum_kK_k\rho K_k^\dagger,
\qquad \sum_kK_k^\dagger K_k=I.$$

“完全正”比“正”更强：即使系统与任意辅助系统纠缠，$\mathcal E\otimes I$ 也必须把合法态映为合法态。

### 进阶回看：为什么“完全正”多了两个字

为什么只要求“正”不够？矩阵转置 $T(\rho)=\rho^T$ 对单个系统保持正性，但把它只作用在 Bell 态的第一个子系统会得到

$$
(T\otimes I)(|\Phi^+\rangle\langle\Phi^+|)
=\frac12
\begin{bmatrix}
1&0&0&0\\
0&0&1&0\\
0&1&0&0\\
0&0&0&1
\end{bmatrix}.
$$

这个矩阵的本征值是 $1/2,1/2,1/2,-1/2$，不是合法密度矩阵。因此转置是正映射，却不是完全正映射，也不能作为只作用于一个子系统的物理信道。

### 4.1 从系统—环境演化得到 Kraus 算子

设环境初态为 $|0\rangle_E$，系统与环境共同做酉演化 $U$，然后我们忽略环境：

$$
\mathcal E(\rho)
=\operatorname{Tr}_E\!\left[
U(\rho\otimes|0\rangle\langle0|_E)U^\dagger
\right].
$$

在环境基 $\{|k\rangle_E\}$ 中定义

$$
K_k={}_E\!\langle k|U|0\rangle_E,
$$

代入偏迹定义便得到 $\mathcal E(\rho)=\sum_kK_k\rho K_k^\dagger$。共同演化的酉性给出 $\sum_kK_k^\dagger K_k=I$，所以输出迹仍为 1。这说明开放系统看似不可逆，整体“系统 + 环境”的演化仍可逆。这里假设输入总态是 $\rho\otimes|0\rangle\langle0|_E$，系统与环境起初没有相关，且环境制备固定。若允许初始系统—环境相关随输入改变，仅凭系统当前的 $\rho$ 可能不足以定义一条适用于所有输入的同一 CPTP 信道；不能把这一构造的前提省掉。

本章用 Kraus 算子直接计算信道输出；[第 18 章](18-channels-capacities-complexity.md)会补上纯化、Choi 矩阵以及“同一信道为何有多种容量”。两章使用同一套 CPTP 与根保真度约定；第 18 章另会先声明 Choi 矩阵采用未归一化最大纠缠向量，避免与归一化“Choi 态”混用。

### 4.2 合法复位信道

把任意输入复位到 $|0\rangle$ 的信道可取

$$
K_0=|0\rangle\langle0|,\qquad
K_1=|0\rangle\langle1|.
$$

它们满足 $K_0^\dagger K_0+K_1^\dagger K_1=I$，并且

$$
\mathcal R(\rho)=K_0\rho K_0^\dagger+K_1\rho K_1^\dagger
=|0\rangle\langle0|.
$$

因此复位是合法 CPTP 映射。它不违反不可删除，因为关于输入的信息被转移到环境，而不是在整体封闭演化中无痕消失。

这也是一个理想目标信道，不是所有硬件复位的自动结果。被动等待若接近平衡态，只会把系统带向由温度决定的热态，未必是纯 $|0\rangle$；主动复位可以采用测量后条件翻转、光学抽运或与耗散辅助系统交换。实际复位要报告残余激发概率、所需时间、是否产生泄漏，以及对邻近量子比特的扰动。

### 4.3 局域 CPTP 操作为什么不能改变远端无条件统计

第 03 章用 Bell 态解释无信号，现在可对任意有限维联合态证明。设 Bob 仅在 B 上施加信道，Kraus 算子为 $K_k$ 且 $\sum_kK_k^\dagger K_k=I_B$。Alice 任意一个局部测量结果的 POVM 元为 $E_a$，输入为 $\rho_{AB}$。操作后该结果概率是

$$
\begin{aligned}
p'(a)&=\sum_k\operatorname{Tr}\!\left[(E_a\otimes I_B)
(I_A\otimes K_k)\rho_{AB}(I_A\otimes K_k^\dagger)\right]\\
&=\operatorname{Tr}\!\left[
\left(E_a\otimes\sum_kK_k^\dagger K_k\right)\rho_{AB}\right]\\
&=\operatorname{Tr}[(E_a\otimes I_B)\rho_{AB}]=p(a).
\end{aligned}
$$

第二行先在**整个联合矩阵的迹内循环移动**最后一个因子，再用张量积乘法；没有声称矩阵本身可以交换。等式对所有 $E_a$ 成立，因此 Alice 的整个约化密度矩阵不变。两边维度可以不同；这个证明依赖 Bob 的全部分支保迹，而不依赖输入一定是 Bell 态。

若 Bob 只保留某个测量结果，对应分支未必保迹；知道该结果的 Alice 可以使用不同的条件态。但是她需要收到这个经典标签才知道怎样筛选自己的记录。完整标签丢弃时仍须相加所有分支，上式仍适用。F71-05 代码在非最大、含复相位的纠缠输入上实际核验远端阻尼；一般证明不由这个小样本代替。

## 5. 四个基础噪声模型

### 5.1 比特翻转

以概率 $p$ 施加 $X$，其中 $0\le p\le1$：

$$\mathcal E(\rho)=(1-p)\rho+pX\rho X.$$

Kraus 算子可取 $K_0=\sqrt{1-p}I$、$K_1=\sqrt pX$。

取 $p=1/4$ 并输入 $|0\rangle\langle0|$，有四分之三的权重保持 $|0\rangle$，四分之一的权重翻到 $|1\rangle$：

$$
\mathcal E(|0\rangle\langle0|)
=\frac34|0\rangle\langle0|+\frac14|1\rangle\langle1|
=\begin{bmatrix}3/4&0\\0&1/4\end{bmatrix}.
$$

若换成输入 $|+\rangle$，由于 $X|+\rangle=|+\rangle$，同一信道会给 $\mathcal E(|+\rangle\langle+|)=|+\rangle\langle+|$。**一个输入态不变，不等于这条信道没有噪声**；换 $|0\rangle$ 就看到了差别。

### 5.2 相位翻转与退相干

相位翻转信道的参数是随机施加 Z 的概率，$0\le p\le1$：

$$\mathcal E(\rho)=(1-p)\rho+pZ\rho Z$$

保持计算基布居，也就是处于 $|0\rangle$、$|1\rangle$ 的概率，却改变非对角相干项。对

$$\rho=\begin{bmatrix}a&c\\c^*&1-a\end{bmatrix}$$

有

$$\mathcal E(\rho)=
\begin{bmatrix}a&(1-2p)c\\(1-2p)c^*&1-a\end{bmatrix}.$$

这里的参数约定非常重要：在“以概率 $p$ 施加 $Z$”的定义下，相干项乘以 $1-2p$；有些资料直接把“相干项乘以 $1-\lambda$”定义为退相位强度。比较数值前必须先对照完整信道公式。

离散的随机 $Z$ 翻转是退相位的简化模型，不应把参数 $p$ 直接叫作某段时间内“相位丢失的百分比”。例如在一个简单的 Markov 纯退相位模型中，非对角元按 $e^{-t/T_\phi}$ 衰减；若要写成上面的随机 $Z$ 信道，则应取

$$
p(t)=\frac{1-e^{-t/T_\phi}}2.
$$

此时 $p(t)$ 从 0 趋近 $1/2$。若把 $p>1/2$ 继续解释成单调增强的退相干，反而会让 $|1-2p|$ 再次增大，失去这个物理含义。

### 5.3 振幅阻尼

这里采用零温振幅阻尼，模拟激发态向基态弛豫，参数 $0\le\gamma\le1$ 是初始处于激发态时发生向下跃迁的概率：

$$
K_0=\begin{bmatrix}1&0\\0&\sqrt{1-\gamma}\end{bmatrix},
\quad
K_1=\begin{bmatrix}0&\sqrt\gamma\\0&0\end{bmatrix}.
$$

对 $|1\rangle$，输出为

$$\rho'=(1-\gamma)|1\rangle\langle1|+
\gamma|0\rangle\langle0|.$$

#### 完整算例：$|+\rangle$ 的振幅阻尼

取 $\gamma=0.36$，输入

$$
\rho=|+\rangle\langle+|=\frac12
\begin{bmatrix}1&1\\1&1\end{bmatrix}.
$$

逐项计算后

$$
\mathcal E(\rho)
=K_0\rho K_0^\dagger+K_1\rho K_1^\dagger
=\begin{bmatrix}0.68&0.40\\0.40&0.32\end{bmatrix}.
$$

它的迹为 1，行列式为 $0.0576>0$，所以两个本征值都非负，是合法混态。与只输入 $|1\rangle$ 的例子相比，这个算例还显示振幅阻尼同时改变布居和相干项。

### 5.4 退极化信道：先声明参数约定

本书采用

$$
\mathcal D_p(\rho)=(1-p)\rho+p\frac I2,
\qquad 0\le p\le1.
$$

它把单比特 Bloch 向量缩短为 $(1-p)\vec r$。这里 $p$ 可理解为“以权重 $p$ 用最大混态替代输入”。

另一常见写法是

$$
\widetilde{\mathcal D}_q(\rho)
=(1-q)\rho+\frac q3
\left(X\rho X+Y\rho Y+Z\rho Z\right),
$$

即以总概率 $q$ 随机施加三个非恒等 Pauli 错误。这个换算不必死记。对任意迹为 1 的单比特态，写成 Bloch 形式 $\rho=(I+r_xX+r_yY+r_zZ)/2$，分别用 $X,Y,Z$ 共轭后相加，三个 Bloch 分量各只保留一次正号、两次负号，因此

$$
X\rho X+Y\rho Y+Z\rho Z=2I-\rho.
$$

代回随机 Pauli 写法，得到

$$
\widetilde{\mathcal D}_q(\rho)
=\left(1-\frac{4q}{3}\right)\rho
+\frac{4q}{3}\frac I2.
$$

在本书所取 $0\le p\le1$ 与随机 Pauli 概率 $0\le q\le1$ 的共同表示范围内，两式表示同一信道时满足

$$q=\frac{3p}{4}.$$

因此本书的 $p\in[0,1]$ 对应 $q\in[0,3/4]$；随机 Pauli 模型仍可取 $q>3/4$，但这时 Bloch 向量已翻向反侧，不能继续解释为“以 $p\le1$ 的概率替换成最大混态”。所以两个资料都写“退极化概率 0.1”时，不能在未看公式的情况下认定它们噪声相同。软件库也可能允许更广的数学参数范围；代码、正文和图必须使用同一约定。

### F71-05｜两个合法噪声信道，交换次序为什么仍不同

**题目。** $\mathcal F_p$ 是 §5.1 的随机 $X$ 翻转，$\mathcal A_\gamma$ 是 §5.3 的零温振幅阻尼；取 $p=1/4,\gamma=0.36$。输入 $|0\rangle$，先翻转再阻尼，与先阻尼再翻转的结果一样吗？

**第一步：每步分别计算激发占据。** 令 $b=\rho_{11}$，其中 $0\le b\le1$。翻转把两个布居交换后加权，故 $b\mapsto(1-p)b+p(1-b)=p+(1-2p)b$；零温阻尼把它变为 $(1-\gamma)b$。从 $b=0$ 出发：

$$
\begin{aligned}
\text{先翻转再阻尼：}&\quad0\longmapsto0.25\longmapsto0.64\times0.25=0.16,\\
\text{先阻尼再翻转：}&\quad0\longmapsto0\longmapsto0.25.
\end{aligned}
$$

两条输出分别为 $\operatorname{diag}(0.84,0.16)$ 与 $\operatorname{diag}(0.75,0.25)$；都合法，归一化测试发现不了门序的错误。物理上，第一条线路中翻转产生的激发还有机会衰减；第二条线路在等待结束后才产生激发。

**第二步：检查带相干的任意输入。** 写 $\rho=\left[\begin{smallmatrix}1-b&c\\c^*&b\end{smallmatrix}\right]$。翻转的非对角元为 $(1-p)c+pc^*$，阻尼的非对角元为 $\sqrt{1-\gamma}\,c$；后一个因子是实数，所以本模型里非对角项的两种次序恰相同。用下标 FA 表示先翻转后阻尼、AF 表示反向顺序，布居满足

$$
\begin{aligned}
b_{FA}&=(1-\gamma)[p+(1-2p)b],\\
b_{AF}&=p+(1-2p)(1-\gamma)b,
\end{aligned}
$$

前者减后者为 $-p\gamma$，因此完整矩阵差为

$$
\mathcal A_\gamma(\mathcal F_p(\rho))-
\mathcal F_p(\mathcal A_\gamma(\rho))=p\gamma Z.
$$

这个式子适用于本例任意归一化单比特输入；若 $p=0$ 或 $\gamma=0$，差为零。不能把两个“错误概率”简单相加，就认为得到了等价的单信道。

**代码与软件对照。** 运行 `python3 codes/foundations/round71_checks.py --case 05`；[固定矩阵和边界检查](../codes/foundations/round71-README.md)使用 Kraus 分支组合，不直接填入答案。移植到 [Qiskit 的 Kraus API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Kraus)时，`compose`、`dot`、`front` 的调用语义不同（访问 2026-10-13）；先用这里的 0.16/0.25 反例核对，不能只凭方法名猜执行顺序。§6的阻尼与纯退相位恰可交换，是那一对模型的结构，不能推广成任意噪声都可交换。

## 6. $T_1$、$T_2^*$、$T_2$ 与 $T_\phi$

- **$T_1$**：能量弛豫时间。先制备 $|1\rangle$、等待 $t$ 再测量，常拟合 $P_1(t)=A e^{-t/T_1}+B$。
- **$T_2^*$**：Ramsey 实验得到的非均匀退相位时间，包含每次实验之间的慢频率漂移。星号不是乘法符号。
- **$T_2$**：通常指加入 Hahn echo 或其他回波序列后测得的相干时间；回波能抵消一部分慢噪声，所以它常比 $T_2^*$ 长。引用时应说明具体脉冲序列，不能只写“$T_2$”。
- **$T_\phi$**：理想化模型中的纯退相位时间，试图把能量弛豫对相干的贡献扣除。

Ramsey 信号常用带振荡的衰减包络拟合，例如

$$
P_1(t)=\frac12\left[1+C e^{-(t/T_2^*)^\alpha}
\cos(\Delta t+\phi)\right],
$$

这里 $\Delta=\omega_0-\omega_{\rm ref}$ 是量子比特与 Ramsey 参考脉冲之间的**角频率**差，单位为 rad/s；若实验报告用 Hz 给出普通频率差 $\Delta f$，则 $\Delta=2\pi\Delta f$。$C$ 是初始振荡对比度，$\phi$ 是由脉冲相位约定决定的初始相位；本式把理想概率基线写成 $1/2$，真实读出拟合还可能需要另加偏置。包络指数 $\alpha$ 取决于噪声谱和拟合模型。在简单 Markov 模型中，

$$
\frac1{T_2}=\frac1{2T_1}+\frac1{T_\phi},
\qquad T_2\le2T_1.
$$

这个关系可以从第 5 节的两个信道亲手算出，而不必把它当作孤立经验公式。设初态为

$$
\rho(0)=\begin{bmatrix}a&c\\c^*&1-a\end{bmatrix},
$$

在零温、指数弛豫模型中取振幅阻尼参数 $\gamma(t)=1-e^{-t/T_1}$，第 5.3 节的 Kraus 算子给

$$
\rho_{11}(t)=(1-a)e^{-t/T_1},\qquad
\rho_{01}(t)=c\sqrt{1-\gamma(t)}=c e^{-t/(2T_1)}.
$$

可见仅有能量弛豫时，相干项已经会以 $2T_1$ 为时间常数衰减。若再独立加入第 5.2 节的纯退相位，取 $p_\phi(t)=[1-e^{-t/T_\phi}]/2$，其对角元不变，非对角元另乘 $1-2p_\phi(t)=e^{-t/T_\phi}$。因此合并后

$$
\rho_{01}(t)=c\,e^{-t/(2T_1)}e^{-t/T_\phi}
=c\,e^{-t/T_2},
\qquad
\frac1{T_2}=\frac1{2T_1}+\frac1{T_\phi}.
$$

例如 $T_1=T_\phi=60\,\mu\mathrm{s}$ 时，$T_2=40\,\mu\mathrm{s}$。从 $|+\rangle$ 出发，初始 $\rho_{11}=\rho_{01}=1/2$；等待 $40\,\mu\mathrm{s}$ 后，模型预测 $\rho_{11}=e^{-2/3}/2\approx0.257$，而 $\rho_{01}=e^{-1}/2\approx0.184$。两个数不同，因为布居只受弛豫影响，相干同时受弛豫与纯退相位影响。[Preskill 的量子信道课程讲义](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-5-Qubit-Channels.pdf)给出了振幅阻尼的矩阵形式及没有额外纯退相位时 $T_2=2T_1$ 的极限。

这个关系不是对任意非 Markov 噪声、任意回波定义都可机械套用的恒等式。相干时间也不是设备质量的单一总分：若门很慢，即使 $T_1$ 较长也可能在一个相干窗口内做不了多少操作；控制误差、串扰、泄漏、漂移和测量错误也不会由 $T_1/T_2$ 完整捕捉。

## 7. 噪声为何不总是独立同分布

方便的教材模型常假设每个门后独立出现 Pauli 错误。现实中还有：

- 缓慢校准漂移；
- 邻近控制引起的串扰；
- 非计算能级泄漏；
- $1/f$ 噪声与非 Markov（有记忆）效应；
- 宇宙射线或高能粒子造成的相关突发错误；
- 测量错误与状态制备错误。

错误校正阈值定理依赖具体噪声假设；引用“低于 1% 即可容错”而不说明码、解码器、门集和噪声模型是不严谨的。

## 8. 过程表征与误差指标

“误差多大”没有唯一答案，必须先说明比较对象与操作任务。对两个状态 $\rho,\sigma$，本书使用

$$
T(\rho,\sigma)=\frac12\|\rho-\sigma\|_1
$$

表示迹距离；它越大，两态越容易区分。本书把

$$
F(\rho,\sigma)=\operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}
$$

称为**根保真度**；它越大，两态越相似。部分资料把本书的 $F^2$ 叫“保真度”，因此引用数值时必须说明是否平方。对 $|0\rangle$ 和 $|+\rangle$，两者恰好都是 $1/\sqrt2$：

$$
T\bigl(|0\rangle\langle0|,|+\rangle\langle+|\bigr)=\frac1{\sqrt2},
\qquad
F\bigl(|0\rangle\langle0|,|+\rangle\langle+|\bigr)=\frac1{\sqrt2}.
$$

这次数值相同只是这个例子的巧合，不表示两个量相同。第 13 章会用最优判别概率、熵和 Holevo 信息解释这些量各自回答什么问题。

| 指标/方法 | 回答的问题 | 不能单独回答的事 |
|---|---|---|
| 状态保真度 | 两个状态多接近 | 整个门对所有输入的表现 |
| 平均门保真度 | 平均输入上的门质量 | 最坏情形和时间相关误差 |
| 随机基准测试 | 平均衰减与可扩展门质量 | 完整噪声机制 |
| 过程层析 | 重构小系统过程 | 大系统可扩展性 |
| 金刚石范数 | 最坏情形信道距离 | 实验上直接估计通常困难 |
| 逻辑错误率 | 编码操作的实际可靠性 | 未说明每轮时长和资源时不可横比 |

### F72-05｜过程层析：正性与保迹必须分别验收

过程层析要反复准备多种输入，再测多种输出基；只拟合一个输入态无法确定整个信道。单比特的默认 Pauli 方案准备 $|0\rangle,|1\rangle,|+\rangle,|{+i}\rangle$，各测 $X,Y,Z$，合计 $4\times3=12$ 种设置。这里实际运行 Qiskit Experiments 的电路生成、Aer 模拟、线性逆拟合，并保存每一组计数。

先为软件结果提供一个短数学接口。固定“输入、输出”的张量次序，定义未归一化 Choi 矩阵

$$
J(\mathcal E)=\sum_{a,b=0}^1|a\rangle\langle b|\otimes\mathcal E(|a\rangle\langle b|).
$$

它是 $4\times4$，不是本章的一比特密度矩阵；对保迹信道有 $\operatorname{Tr}J=2$。更强的保迹条件是对输出做偏迹得到 $I_2$；完全正条件是 $J\succeq0$。[第 18 章](18-channels-capacities-complexity.md)给一般证明，此处只展开一个输入可手算的检查。

**练习。** 用 $\gamma=.36,r=.10$ 的广义阻尼写出 J，验证输出偏迹。仅知道 J 的谱非负、迹为 2，是否已经保证保迹？

**第一步：逐块取信道输出。** $\mathcal E(|0\rangle\langle0|)=\operatorname{diag}(.964,.036)$，$\mathcal E(|1\rangle\langle1|)=\operatorname{diag}(.324,.676)$，$\mathcal E(|0\rangle\langle1|)=.8|0\rangle\langle1|$。把四个 $2\times2$ 输出块排入 J 得

$$
J=\begin{bmatrix}.964&0&0&.8\\0&.036&0&0\\0&0&.324&0\\.8&0&0&.676\end{bmatrix}.
$$

对输出偏迹把各块的迹拼成 $2\times2$ 矩阵：两对角为 $.964+.036=1$、$.324+.676=1$，非对角为 0，故得到 $I_2$。

**第二步：看见少一个条件的后果。** 反例 $J_* =2|00\rangle\langle00|$ 正半定且迹为 2，输出偏迹却是 $\operatorname{diag}(2,0)$；它对应输入 $|0\rangle$ 输出迹 2、输入 $|1\rangle$ 输出迹 0，不能作为确定性信道。把谱修到非负并把总迹修到 2，也不自动固定每个输入的输出迹。

本轮每设置 16384 次的完整拟合与精确信道 J 的 Frobenius 距离为 $0.0279380$，输出偏迹最大误差为 $1.12\times10^{-15}$，本次恰通过 CP、TP 两检查；不能倒推拟合选项保证了 TP。另有每设置 32 次的压力例，拟合仍 CP、总迹仍为 2，却不 TP，输出偏迹最大逐格偏差 $0.04658984$；这提供了事后正性修正不自动保迹的实际反例。[官方拟合选项](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.TomographyAnalysis.html)说明正性重缩放与拟合器选择（0.14.2，访问 2026-10-13）；[F72-05 完整参数、原计数和诊断](../codes/foundations/round72-README.md)实际检查两项。线性逆与事后修正不等于带 CP/TP 约束的最大似然拟合，理想测量模拟也不包含真实制备与读出校准。

## 9. 误差缓解不等于错误校正

误差缓解通过零噪声外推、概率误差抵消、对称性筛选等办法改善期望值估计，通常需要更多采样或关于噪声的知识，但不把任意长计算稳定地存进逻辑子空间。错误校正则主动提取错误综合征并纠正，目标是在资源增加时压低逻辑错误率。

## 10. 自检

1. 计算 $|+\rangle$ 的密度矩阵和纯度。
2. 最大混态 $I/2$ 经任意单比特酉变换后是什么？
3. 验证振幅阻尼 Kraus 算子满足完备关系。
4. 为什么只报告 $T_1$ 不能说明一台处理器能运行多深的电路？
5. 求部分转置例子中间 $2\times2$ 块的两个本征值，并解释“正”为什么不足以定义物理信道。
6. 把 $p=0.20$ 的本书退极化参数换算成随机 Pauli 写法中的 $q$。
7. 对概率 $p=1/4$ 的比特翻转信道，分别求输入 $|0\rangle\langle0|$ 与 $|+\rangle\langle+|$ 的输出。为何第二个输入不变，不能说明信道等于恒等？
8. 从 $|+\rangle\langle+|$ 出发，按计算基做理想投影测量。已知结果为 0 时的条件后态是什么？丢弃结果时的非选择后态是什么？两者计算基概率是否相同？

答案见[练习与答案：第 5 章](appendices/exercises.md#第-5-章)。

## 新增诊断练习：有限温度弛豫为何也能把基态激发起来

**问题。** §5.3 的零温阻尼只向下跃迁。若平衡态仍有激发占据 $r$，等待很久就不应总得到纯基态。以下补上一个有明确固定点的模型；它不把真实非平衡噪声一概称作温度。

对基序 $0,1$，取 $0\le\gamma\le1$ 为本次弛豫强度，$0\le r\le1$ 为模型固定点的激发占据，四个 Kraus 算子为

$$
\begin{aligned}
K_0&=\sqrt{1-r}\begin{bmatrix}1&0\\0&\sqrt{1-\gamma}\end{bmatrix},&
K_1&=\sqrt{1-r}\begin{bmatrix}0&\sqrt\gamma\\0&0\end{bmatrix},\\
K_2&=\sqrt r\begin{bmatrix}\sqrt{1-\gamma}&0\\0&1\end{bmatrix},&
K_3&=\sqrt r\begin{bmatrix}0&0\\\sqrt\gamma&0\end{bmatrix}.
\end{aligned}
$$

前两项是权重 $1-r$ 的向下阻尼，后两项是权重 $r$ 的向上阻尼。分别相加 $K_0^\dagger K_0+K_1^\dagger K_1=(1-r)I$ 与 $K_2^\dagger K_2+K_3^\dagger K_3=rI$，合计为 $I$，所以保迹；Kraus 形式同时保证完全正。这叫广义振幅阻尼。若解释为正温度、非简并二能级热平衡，另有 $r<1/2$；完整数学信道允许的范围更大。

**题目。** 输入写为 $\rho=\left[\begin{smallmatrix}1-b&c\\c^*&b\end{smallmatrix}\right]$。先逐项求输出，再令 $\gamma=0.36,r=0.10$，比较输入 $|0\rangle,|1\rangle,|+\rangle$，并求固定点。

**逐步解答。** 向下分支使激发占据成为 $(1-\gamma)b$；向上分支使它成为 $b+\gamma(1-b)$。按权重相加：

$$
b'=(1-r)(1-\gamma)b+r[b+\gamma(1-b)]
=(1-\gamma)b+\gamma r.
$$

两类分支都让非对角元乘 $\sqrt{1-\gamma}$，故 $c'=\sqrt{1-\gamma}\,c$。本题三个输入的 $b'$ 依次为 $0.036,0.676,0.356$；$|+\rangle$ 输入还给 $c'=0.4$。基态也会被激发，是非零 $r$ 的直接后果。

当 $\gamma>0$，固定点是 $\rho_{\rm eq}=\operatorname{diag}(1-r,r)$。反复应用 $n$ 次，有 $b_n-r=(1-\gamma)^n(b_0-r)$；若 $\gamma=0$，信道为恒等，每个态都是固定点，不能说它会热化。令 $\gamma=1-e^{-t/T_1}$，可见 $b(t)=r+(b_0-r)e^{-t/T_1}$，把非零平衡底座与衰减率区分开了。

运行 `python3 codes/foundations/diagnostic_lab.py --case 05`，程序核对三个输入、固定点、Kraus 完备性和九组边界参数。模型参数与 [Qiskit Aer 的四 Kraus 定义](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.amplitude_damping_error.html)相接：`param_amp=gamma`、`excited_state_population=r`。核查的 0.17.1 文档（页面更新 2025-06-04，访问 2026-09-26）参数文字一处写成 $|0\rangle$ 占据，与同页公式及固定点矛盾；本书依据明确矩阵把 $r$ 定义为 $|1\rangle$ 占据。移植代码时应以版本源码、矩阵和固定点共同核对，不能只抄参数说明的一行。

## 配套数值实验与展开答案

组合振幅阻尼与纯退相位，分别计算 40 μs 后的激发占据和相干项。代码检查 Kraus 完备关系、输出本征值与恒等／复位边界，不把一种输入的结果当成全部信道质量。

题目和逐步解答见[基础实验册](labs/foundations.md)，本章程序编号为 `05`。可从[代码说明](../codes/foundations/README.md)进入独立脚本与保存的运行结果。所有模拟样本均明确标作合成数据，不是硬件实验。

## 参考起点

- Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition, Cambridge University Press (2010)，第 8 章。
- IBM Quantum Learning, [General formulation of quantum information](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information)。
- IBM Quantum Learning, [Mathematical formulations of measurements](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements)：区分只给经典结果的测量与还须描述条件后态的非破坏测量。
- W. F. Stinespring, [Positive functions on C*-algebras](https://doi.org/10.1090/S0002-9939-1955-0069403-4), *Proceedings of the American Mathematical Society* 6, 211–216 (1955)。
- M.-D. Choi, [Completely positive linear maps on complex matrices](https://doi.org/10.1016/0024-3795(75)90075-0), *Linear Algebra and its Applications* 10, 285–290 (1975)。
