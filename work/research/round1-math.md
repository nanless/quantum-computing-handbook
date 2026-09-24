# 第一轮研究报告：量子计算教材的“数学与计算基础”知识树与审查标准

> 研究角色：数学与计算基础独立审查员  
> 完成日期：2026-09-22（Asia/Shanghai）  
> 资料访问日期：2026-09-22  
> 范围：复数、线性代数、狄拉克记号、态与测量、单/多量子比特、张量积与纠缠、量子门与电路、密度矩阵与偏迹、量子信道与噪声、不可克隆与不可删除，以及贯穿全章的例题、推导和图示设计。  
> 项目现状：本轮检查时，项目镜像中没有 `sources/` 教材正文或其他章节文件，只有 `AGENTS.md`。因此无法做逐页勘误；本报告提供完整的目标知识树、写作顺序、易错点、例题样板和后续逐章验收表。未改动任何 `sources/` 内容。

## 一、结论先行

面向“零基础读者到入门研究生”的教材，不应把数学预备知识写成一串孤立定义，也不应一上来照搬研究生层次的算子代数。最稳妥的主线是：

1. 从复振幅与二维向量开始，让读者先会算；
2. 用内积、正交、基与矩阵解释“态、门和测量”；
3. 先在纯态和投影测量框架内完成单量子比特与两量子比特的闭环；
4. 借 Bell 态引出张量积、纠缠和局部测量；
5. 再用“我们不知道制备过程”与“忽略环境”这两个真实问题引入密度矩阵、偏迹和混态；
6. 最后用“系统与环境共同做幺正演化”推导量子信道和 Kraus 表示，并以常见噪声模型、不可克隆和不可删除收束。

这一顺序刻意设置两层表述：正文给初学者直觉、二维/四维算例和图；“进阶框”给严格条件、一般维数表达、证明与术语。若把 POVM、完全正映射、Choi 矩阵等放在第一次介绍量子态之前，初学者会记住符号却失去物理意义；若完全略去这些内容，入门研究生又无法继续阅读量子信息文献。

必须优先修正或预防的高风险问题有八项：

- 把“量子叠加”说成经典概率混合；
- 把 Bloch 球表面当成包含所有单量子比特态；
- 忽略全局相位与相对相位的区别；
- 张量积基顺序、线路读序和软件比特序混在一起；
- 只给测量概率，不说明测量后的条件态与非选择态；
- 把“相关性”一律叫作纠缠；
- 只要求正性，不解释量子信道为何必须完全正；
- 把不可克隆/不可删除误写成“任何状态都不能复制”或“量子信息无法被擦除”。

## 二、资料依据与研究方法

### 2.1 核心权威资料

本报告优先使用作者公开教材、大学官方课程、出版社页面、官方技术文档和经典原始论文。各来源的具体用途如下。

| 来源 | 本报告用途 | 发布/更新信息 | 访问日期 |
|---|---|---:|---:|
| John Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/) | 数学预备、密度矩阵、偏迹、信道、测量的严格定义与章节边界 | Cambridge University Press 于 2018-04 出版；作者页提供手稿与勘误 | 2026-09-22 |
| John Watrous, [Basics of Quantum Information](https://learning.quantum.ibm.com/course/basics-of-quantum-information) | 初学者教学顺序：单系统→复合系统→电路→纠缠应用 | IBM 在线课程；页面未标明首发日期，访问时为持续维护页面 | 2026-09-22 |
| John Watrous, [General Formulation of Quantum Information](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information) | 密度矩阵→信道→一般测量→纯化/保真度的进阶顺序 | IBM 在线课程；页面未标明首发日期，访问时为持续维护页面 | 2026-09-22 |
| IBM Quantum Learning, [Density matrices](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/density-matrices) | Bloch 球内部、凸组合、多系统约化态 | 在线页面未标明首发日期 | 2026-09-22 |
| IBM Quantum Learning, [Quantum channels](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/quantum-channels) | Stinespring、Kraus、Choi 三种表示的教学连接 | 在线页面未标明首发日期 | 2026-09-22 |
| IBM Quantum Learning, [General measurements](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/general-measurements) | POVM、测量信道、状态判别与层析的边界 | 在线页面未标明首发日期 | 2026-09-22 |
| Michael Nielsen & Isaac Chuang, [Quantum Computation and Quantum Information, 10th Anniversary Edition](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE) | 量子计算与量子信息的经典本科高年级/研究生教材结构 | Cambridge University Press，2010 | 2026-09-22 |
| John Preskill, [Quantum Computation lecture notes](https://www.preskill.caltech.edu/ph229/) | 量子信息、信道、纠错与研究生层次衔接 | 讲义起源于 1998；站点显示章节在 2009、2020、2022 等时间更新 | 2026-09-22 |
| MIT OCW, Chuang & Shor, [Quantum Information Science lecture notes](https://ocw.mit.edu/courses/mas-865j-quantum-information-science-spring-2006/pages/lecture-notes/) | 密度矩阵、系统—环境、操作和算子和表示 | 课程开设于 Spring 2006 | 2026-09-22 |
| MIT OCW, Shor, [Lecture 2: Basics of Quantum Mechanics](https://www.ocw.mit.edu/courses/18-435j-quantum-computation-fall-2003/c1095b496b364b56aaa0cbb2d725234a_qc_lec02.pdf) | 复合系统、测量与幺正演化的简洁公理化表述 | 课程开设于 Fall 2003；OCW 页面近年重整不等于内容新发布 | 2026-09-22 |
| IBM Quantum Documentation, [Build noise models](https://quantum.cloud.ibm.com/docs/en/guides/build-noise-models) | 当前软件中 Kraus、Pauli、退极化、振幅/相位阻尼、热弛豫噪声的名称与参数提醒 | 持续维护页面；无稳定首发日期 | 2026-09-22 |

### 2.2 原始论文与定理来源

| 主题 | 原始来源 | 日期 |
|---|---|---:|
| Stinespring 扩张 | W. F. Stinespring, [Positive Functions on C*-Algebras](https://doi.org/10.1090/S0002-9939-1955-0069403-4), *Proc. AMS* 6, 211–216 | 1955-04 |
| Choi 完全正判据 | M.-D. Choi, [Completely Positive Linear Maps on Complex Matrices](https://doi.org/10.1016/0024-3795(75)90075-0), *Linear Algebra and its Applications* 10, 285–290 | 1975-06 |
| GKSL/Lindblad 生成元 | G. Lindblad, [On the Generators of Quantum Dynamical Semigroups](https://doi.org/10.1007/BF01608499), *Commun. Math. Phys.* 48, 119–130 | 1976-06 |
| GKSL 的独立结果 | V. Gorini, A. Kossakowski, E. C. G. Sudarshan, [Completely Positive Dynamical Semigroups of N-Level Systems](https://doi.org/10.1063/1.522979), *J. Math. Phys.* 17, 821–825 | 1976-05-01 |
| 不可克隆 | W. K. Wootters & W. H. Zurek, [A Single Quantum Cannot Be Cloned](https://doi.org/10.1038/299802a0), *Nature* 299, 802–803 | 1982-10-28 |
| 不可删除 | A. K. Pati & S. L. Braunstein, [Impossibility of Deleting an Unknown Quantum State](https://doi.org/10.1038/35004532), *Nature* 404, 164–165 | 2000-03-09 |

说明：原始论文用来核对定理边界，不宜直接作为初学者正文。严格证明与现代符号应以 Watrous、Nielsen–Chuang、Preskill 等教材交叉校准。

### 2.3 第一轮自检

- 已检查本地文件：没有教材正文，不能声称发现某一具体页的错误。
- 已区分“纯态简化框架”和“密度矩阵一般框架”，避免前后定义互相覆盖。
- 已核对不可克隆、不可删除的适用条件，并加入常见反例边界。
- 已对文中关键数值例题用矩阵计算复核：Bell 态约化密度矩阵为 $I/2$；振幅阻尼示例保持迹为 1 且本征值非负；$Y$ 方向纯态在 $X$ 基测量为各 $1/2$。
- 噪声模型中特别标记“退极化参数存在多种约定”，避免把不同软件或论文中的 $p$ 直接比较。

## 三、建议的整体教学架构

建议把本主题拆成 12 章，每章都采用固定节奏：生活化问题→最小数学工具→二维/四维手算→几何或线路图→一般公式→误区→练习→进阶框。

| 章 | 标题 | 读者离开本章时应能做什么 | 先修 |
|---:|---|---|---|
| 0 | 读图、符号与计算约定 | 看懂列向量、矩阵、线路方向、比特顺序 | 中学代数 |
| 1 | 复数与复振幅 | 计算共轭、模、相位，归一化二维复向量 | 0 |
| 2 | 向量空间、内积与矩阵 | 算内积、投影、基变换、共轭转置、本征值 | 1 |
| 3 | 狄拉克记号 | 在 ket、bra、外积、矩阵之间互译 | 2 |
| 4 | 单量子比特态 | 计算测量概率；区分全局/相对相位；读 Bloch 球 | 3 |
| 5 | 单量子比特门 | 验证幺正性；手算 X/Y/Z/H/S/T 与旋转 | 4 |
| 6 | 多量子比特与张量积 | 展开张量积、固定基顺序、作用局部门 | 3–5 |
| 7 | 纠缠、局部测量与线路 | 制备 Bell 态；判断二比特纯态是否可分；更新条件态 | 6 |
| 8 | 密度矩阵、混态与偏迹 | 区分叠加/混合；算纯度与约化态 | 7 |
| 9 | 一般测量 | 使用投影测量、POVM 和测量算子；分清概率与后态 | 8 |
| 10 | 量子信道 | 判断 CPTP；在 Kraus、系统—环境和 Choi 视角间转换 | 8–9 |
| 11 | 噪声与限制性定理 | 算常见噪声；证明不可克隆/不可删除；准确解释边界 | 10 |

依赖关系可画成一张路线图：

```text
复数 → 内积/矩阵 → 狄拉克记号 → 单比特态 → 单比特门
                         └────────→ 张量积 → Bell 态/纠缠 → 密度矩阵/偏迹
                                                        ├→ 一般测量
                                                        └→ 量子信道 → 噪声
                                                                   └→ 不可克隆/不可删除
```

不建议先讲量子硬件再补数学。硬件可作为动机穿插，但本模块的任务是建立不依赖特定平台的计算语言。

## 四、完整知识树与逐节点写作要求

### 4.1 复数：为什么概率之前先有振幅

#### 必讲内容

1. $z=a+bi$，$i^2=-1$；实部、虚部、共轭 $z^*=a-bi$。
2. 模与模平方：$|z|=\sqrt{a^2+b^2}$，$|z|^2=z^*z$。
3. 极坐标与欧拉公式：$z=re^{i\phi}=r(\cos\phi+i\sin\phi)$。
4. 乘法的几何意义：模相乘、相位相加。
5. “振幅是复数、概率是振幅模平方”，不可把振幅直接解释成概率。

#### 最小例题

令 $\alpha=(1+i)/2$，$\beta=1/\sqrt2$。验证

$$
|\alpha|^2+|\beta|^2=\frac{1^2+1^2}{4}+\frac12=1.
$$

所以 $(\alpha,\beta)^T$ 可作为归一化量子比特态。随后比较 $\alpha+\beta$ 与概率 $|\alpha+\beta|^2$，由交叉项 $\alpha^*\beta+\beta^*\alpha$ 引出干涉。

#### 常见误解

- “虚数是虚构的数”：应说它是满足既定代数规则的数系扩张。
- “相位不影响任何结果”：只有整体共同相位不影响孤立态；分量之间的相对相位会影响换基测量。
- “概率相加就是振幅相加”：互斥的经典事件概率相加；不可区分的量子路径先加振幅再取模平方。

#### 配图

- 复平面上的 $a+bi$、共轭和极坐标；
- 两个相量首尾相加，展示相长与相消；
- 同一组模、不同相对相位在 $X$ 基测量中得到不同统计的并排图。

### 4.2 线性代数：只教量子计算真正要用的部分

#### 主干

- 列向量、线性组合、张成、线性无关、维数、基；
- 复内积 $\langle v|w\rangle=v^\dagger w$，强调第一个因子要共轭；
- 范数、归一化、正交、标准正交基；
- 线性算子和矩阵表示；矩阵乘法是复合，不是逐元素乘；
- 共轭转置 $A^\dagger$、Hermitian 算子、幺正算子、投影算子、正半定矩阵；
- 迹、行列式；
- 本征值/本征向量、谱分解；
- 二维和四维情况下的基变换；
- 进阶框：SVD、Schmidt 分解所需的奇异值概念。

#### 必须推导的关系

若 $U^\dagger U=I$，则

$$
\|U|\psi\rangle\|^2
=\langle\psi|U^\dagger U|\psi\rangle
=\langle\psi|\psi\rangle,
$$

所以幺正演化保持总概率。这里应先给计算意义，再给“封闭系统可逆演化”的物理解释。

若 $A=A^\dagger$ 且 $A|a_j\rangle=a_j|a_j\rangle$，则本征值为实数；不同本征值对应的本征向量正交。正文可用两行证明，完整谱定理放进阶框。

#### 教学边界

不要在初学章节展开无限维 Hilbert 空间、泛函分析、C*-代数。应明确“本书前半部分只处理有限维复内积空间”；到信道一章再说明严格理论有更广范围。

### 4.3 狄拉克记号：作为运算语言，而不是神秘符号

#### 必讲翻译表

| 记号 | 矩阵意义 | 形状 |
|---|---|---|
| $|\psi\rangle$ | 列向量 | $d\times1$ |
| $\langle\psi|=(|\psi\rangle)^\dagger$ | 共轭转置后的行向量 | $1\times d$ |
| $\langle\phi|\psi\rangle$ | 内积/复数 | $1\times1$ |
| $|\psi\rangle\langle\phi|$ | 外积/算子 | $d\times d$ |
| $\langle i|A|j\rangle$ | $A$ 在给定基下的矩阵元 | 标量 |

必须逐项展开：若 $|\psi\rangle=(a,b)^T$，则 $\langle\psi|=(a^*,b^*)$，而不是 $(a,b)$。例如

$$
|\psi\rangle\langle\psi|
=\begin{pmatrix}|a|^2&ab^*\\a^*b&|b|^2\end{pmatrix}.
$$

#### 完备关系

对标准正交基 $\{|j\rangle\}$，

$$
I=\sum_j|j\rangle\langle j|,
\qquad
|\psi\rangle=\sum_j|j\rangle\langle j|\psi\rangle.
$$

这不应只作为公式背诵，要画出“向每个基方向投影，再把分量相加”的图。

### 4.4 单量子比特：代数、几何和实验统计三种视角

#### 纯态

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle,
\qquad |\alpha|^2+|\beta|^2=1.
$$

标准基测量得到 0、1 的概率分别为 $|\alpha|^2$、$|\beta|^2$。必须同时说明：单次测量不能读出 $\alpha,\beta$；估计概率需要许多独立、同样制备的样本。

#### 全局相位与 Bloch 参数化

任何纯态在忽略全局相位后可写为

$$
|\psi\rangle=\cos\frac\theta2|0\rangle+e^{i\phi}\sin\frac\theta2|1\rangle.
$$

为什么是半角：对应密度矩阵的 Bloch 向量

$$
\rho=\frac12(I+\mathbf r\cdot\boldsymbol\sigma),\qquad
\mathbf r=(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta).
$$

纯态在球面 $|\mathbf r|=1$，混态在球内 $|\mathbf r|<1$。绝不能画一张球面图后写“所有单量子比特态都在球面上”。

#### 可验证例题：相对相位

$$
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},\qquad
|-\rangle=\frac{|0\rangle-|1\rangle}{\sqrt2}.
$$

两者在 $Z$ 基中都是各 $1/2$，但在 $X$ 基中分别确定得到 $+$ 和 $-$。这说明“在一个基中的概率相同”不代表状态相同。

再取 $|{+i}\rangle=(|0\rangle+i|1\rangle)/\sqrt2$，在 $X$ 基测量：

$$
|\langle+|{+i}\rangle|^2
=\left|\frac{1+i}{2}\right|^2=\frac12,
\quad
|\langle-|{+i}\rangle|^2=\frac12.
$$

### 4.5 量子门：矩阵、几何与线路必须同步

#### 必讲门

$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
$$

$$
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad
S=\begin{pmatrix}1&0\\0&i\end{pmatrix},\quad
T=\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}.
$$

还应讲 $R_x(\theta)=e^{-i\theta X/2}$、$R_y(\theta)$、$R_z(\theta)$，并解释 Bloch 球旋转与全局相位的关系。

#### 门序例题

线路从左到右执行，但列向量公式右边的门先作用。若先 $H$ 后 $Z$：

$$
ZH|0\rangle=Z|+\rangle=|-\rangle.
$$

反过来先 $Z$ 后 $H$：

$$
HZ|0\rangle=H|0\rangle=|+\rangle.
$$

教材必须用颜色或时间箭头同时标出“线路顺序”和“矩阵乘积顺序”。

#### 关键边界

- 门矩阵必须幺正；测量、复位和噪声一般不是幺正门。
- 幺正门可逆，不代表所有经典函数本身可逆。不可逆经典计算需嵌入可逆计算，例如 $(x,y)\mapsto(x,y\oplus f(x))$。
- “H 创造叠加”是便捷说法，但不够严格：H 也会把 $|+\rangle$ 变回 $|0\rangle$。

### 4.6 张量积和多量子比特：最需要慢讲的数学关口

#### 从基开始

固定约定

$$
|00\rangle=|0\rangle\otimes|0\rangle=(1,0,0,0)^T,
$$

基顺序为 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$。若软件输出采用不同端序，必须单设“符号约定框”，不可静默切换。

展开：

$$
(a|0\rangle+b|1\rangle)\otimes(c|0\rangle+d|1\rangle)
=ac|00\rangle+ad|01\rangle+bc|10\rangle+bd|11\rangle.
$$

局部门：只对第一比特作用 $U$ 写作 $U\otimes I$，只对第二比特作用写作 $I\otimes U$。用 $X\otimes I$ 和 $I\otimes X$ 分别作用在 $|01\rangle$ 上，让读者手算。

#### 维数增长

$n$ 个量子比特的状态向量有 $2^n$ 个复振幅。应谨慎表述：这不表示一次测量能读出 $2^n$ 个经典数，也不自动意味着任意问题都有指数加速。

### 4.7 纠缠、Bell 态和局部测量

#### 可分与纠缠

二比特纯态

$$
|\psi\rangle=a|00\rangle+b|01\rangle+c|10\rangle+d|11\rangle
$$

可分当且仅当系数矩阵

$$
M=\begin{pmatrix}a&b\\c&d\end{pmatrix}
$$

秩为 1；对非零态，等价于 $ad-bc=0$。这个二维判据应在讲 Schmidt 分解前出现，便于手算。一般维数再用 Schmidt 秩判断。

#### Bell 态制备

$$
|00\rangle\xrightarrow{H\otimes I}
\frac{|00\rangle+|10\rangle}{\sqrt2}
\xrightarrow{\mathrm{CNOT}}
|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

逐列写 CNOT 的映射，并画四条计算基箭头，避免读者只认线路符号。

#### 局部测量

对 $|\Phi^+\rangle$ 测量第一个比特：结果 0、1 各为 $1/2$；条件于结果 0，联合态为 $|00\rangle$；条件于结果 1，联合态为 $|11\rangle$。若丢弃测量结果，后态是

$$
\frac12|00\rangle\langle00|+\frac12|11\rangle\langle11|,
$$

不是原来的 Bell 纯态。这里必须区分“条件后态”和“非选择测量后态”。

#### 纠缠不等于普通相关

对比

$$
\rho_{\mathrm{class}}=\tfrac12|00\rangle\langle00|+\tfrac12|11\rangle\langle11|
$$

与 $|\Phi^+\rangle\langle\Phi^+|$。二者在 $Z$ 基都有相同的完全相关统计，但 Bell 态有 $|00\rangle\langle11|$ 等相干项，在 $X$ 基的统计也显示量子相干。图中应把两张密度矩阵热图并排画。

### 4.8 密度矩阵：从“制备不确定性”和“忽略子系统”自然引入

#### 定义与性质

纯态：$\rho=|\psi\rangle\langle\psi|$。一般态满足：

1. $\rho=\rho^\dagger$；
2. $\rho\succeq0$；
3. $\operatorname{Tr}\rho=1$。

制备集合 $\{(p_i,|\psi_i\rangle)\}$ 对应

$$
\rho=\sum_i p_i|\psi_i\rangle\langle\psi_i|.
$$

强调：不同制备集合可能给同一个密度矩阵，物理上仅靠该系统的测量无法区分这些集合。

#### 叠加与混合的核心例题

相干叠加

$$
|+\rangle\langle+|=rac12\begin{pmatrix}1&1\\1&1\end{pmatrix};
$$

等概率经典混合

$$
\tfrac12|0\rangle\langle0|+	frac12|1\rangle\langle1|
=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}.
$$

两者 $Z$ 基统计相同，但 $X$ 基统计不同。非对角元不是在任何基下都叫“相干”；应说“相对于所选基的相干项”。

#### 纯度

纯态当且仅当 $\rho^2=\rho$，等价于 $\operatorname{Tr}(\rho^2)=1$。混态有 $1/d\le\operatorname{Tr}(\rho^2)<1$。不要把“纯度小”说成实验噪声的唯一证据；经典制备不确定性、与环境纠缠、实际噪声都可造成混态。

#### 偏迹

定义需要给“分量版”和“操作版”：

$$
\rho_A=\operatorname{Tr}_B(\rho_{AB})
=\sum_j(I_A\otimes\langle j|)\rho_{AB}(I_A\otimes|j\rangle).
$$

对 Bell 态，

$$
\rho_{AB}=\frac12\left(
|00\rangle\langle00|+|00\rangle\langle11|
+|11\rangle\langle00|+|11\rangle\langle11|
\right).
$$

对 $B$ 取偏迹时使用 $\operatorname{Tr}(|j\rangle\langle k|)=\delta_{jk}$，交叉项消失：

$$
\rho_A=\frac12(|0\rangle\langle0|+|1\rangle\langle1|)=\frac I2.
$$

必须指出：整体是纯态，局部却是最大混态，这不是矛盾，而是纠缠的基本特征。

#### Schmidt 分解

任意二部纯态可写成

$$
|\psi\rangle=\sum_{k=1}^r\sqrt{\lambda_k}|u_k\rangle|v_k\rangle,
\quad \lambda_k>0,\quad\sum_k\lambda_k=1.
$$

$r=1$ 可分，$r>1$ 纠缠；$\lambda_k$ 也是两个约化密度矩阵的非零本征值。正文用二比特 SVD 例子，证明放进阶框。

### 4.9 测量：概率、后态和“忽略结果”是三个问题

#### 投影测量

对正交投影 $\{P_m\}$，$P_mP_n=\delta_{mn}P_m$，$\sum_mP_m=I$：

$$
p(m)=\langle\psi|P_m|\psi\rangle=\operatorname{Tr}(P_m\rho).
$$

若得到 $m$，Lüders 更新为

$$
\rho_m=\frac{P_m\rho P_m}{p(m)}.
$$

忽略结果则

$$
\rho'=\sum_mP_m\rho P_m.
$$

#### POVM 与测量算子

POVM 元 $E_m\succeq0$ 且 $\sum_mE_m=I$，只决定概率 $p(m)=\operatorname{Tr}(E_m\rho)$。若还要后态，需要测量算子/仪器，例如 $M_m$ 满足 $E_m=M_m^\dagger M_m$，然后

$$
\rho_m=\frac{M_m\rho M_m^\dagger}{p(m)}.
$$

同一个 POVM 可对应不同的后态更新。教材若写“POVM 完全描述测量过程”而没有限定“仅指结果统计”，就是不准确的。

#### 期望值

Hermitian 可观测量 $A=\sum_ma_mP_m$ 的期望

$$
\langle A\rangle=\sum_ma_mp(m)=\operatorname{Tr}(A\rho).
$$

不要把期望值说成“单次测量通常得到的值”；它是重复实验结果的统计平均。

### 4.10 量子信道：从系统—环境模型推出来

#### 为什么不只讲幺正

现实中我们常忽略环境、丢弃子系统、做随机操作或测量而不保留结果。系统自身的演化于是一般不是幺正，而是量子信道 $\Phi$。

有限维量子信道应是线性、完全正、保迹（CPTP）映射。解释层次：

- 线性：经典随机混合不能因为描述方式不同而改变结果；
- 保迹：总概率仍为 1；
- 完全正：即使系统与任意辅助系统纠缠，$\Phi\otimes I$ 仍把合法态映为合法态。

“正”不足的标准反例是转置映射 $T$：它把单个系统的正矩阵映为正矩阵，但 $(T\otimes I)(|\Phi^+\rangle\langle\Phi^+|)$ 有负本征值，因此不是物理信道。建议画出部分转置矩阵并在进阶练习中求本征值 $\{1/2,1/2,1/2,-1/2\}$。

#### 从扩张到 Kraus

若系统与初态为 $|0\rangle_E$ 的环境共同做幺正 $U$，再丢弃环境：

$$
\Phi(\rho)=\operatorname{Tr}_E\left[U(\rho\otimes|0\rangle\langle0|)U^\dagger\right].
$$

在环境基 $\{|k\rangle\}$ 插入完备关系，定义

$$
K_k=\langle k|U|0\rangle_E,
$$

得到

$$
\Phi(\rho)=\sum_kK_k\rho K_k^\dagger,
\qquad
\sum_kK_k^\dagger K_k=I.
$$

最后一个条件保证保迹。Kraus 表示不唯一：$K_k$ 可在 Kraus 指标上做等距混合而表示同一信道。

#### 三种表示的教学角色

- Stinespring：说明“开放演化可看成更大系统的幺正演化”；
- Kraus：最适合手算和噪声模拟；
- Choi：最适合判断完全正、做过程层析和凸优化。

Choi 矩阵定义必须固定归一化约定，例如

$$
J(\Phi)=\sum_{i,j}|i\rangle\langle j|\otimes\Phi(|i\rangle\langle j|).
$$

不同文献使用归一化 Bell 态时会多出 $1/d$；教材需要提示这一差异。

### 4.11 噪声模型：每个模型都要给 Kraus、Bloch 图与算例

#### 比特翻转与相位翻转

$$
\Phi_X(\rho)=(1-p)\rho+pX\rho X,
\qquad
\Phi_Z(\rho)=(1-p)\rho+pZ\rho Z.
$$

Kraus 分别为 $\sqrt{1-p}I,\sqrt pX$ 和 $\sqrt{1-p}I,\sqrt pZ$。画 Bloch 球坐标被压缩/翻转的效果。

#### 退相位

可写成“以概率 $p$ 施加 $Z$”或用直接衰减非对角元的参数 $\lambda$。两种约定之间不应混用。若采用

$$
\Phi(\rho)=\begin{pmatrix}\rho_{00}&(1-2p)\rho_{01}\\(1-2p)\rho_{10}&\rho_{11}\end{pmatrix},
$$

就明确这是随机 $Z$ 约定；若希望相干项乘 $(1-\lambda)$，则另定义 $\lambda$。

#### 振幅阻尼

$$
K_0=\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix},\qquad
K_1=\begin{pmatrix}0&\sqrt\gamma\\0&0\end{pmatrix}.
$$

它描述 $|1\rangle$ 向 $|0\rangle$ 衰减。对 $|+\rangle$ 且 $\gamma=0.36$：

$$
\rho'=K_0|+\rangle\langle+|K_0^\dagger+K_1|+\rangle\langle+|K_1^\dagger
=\begin{pmatrix}0.68&0.40\\0.40&0.32\end{pmatrix}.
$$

可复核 $\operatorname{Tr}\rho'=1$，行列式 $0.0576>0$，因此是合法混态。此例同时训练矩阵乘法、Kraus 求和和合法性检查。

#### 退极化

必须先声明参数约定。可采用

$$
\Phi(\rho)=(1-p)\rho+p\frac I2,
$$

它把 Bloch 向量缩为 $(1-p)\mathbf r$。另一常见 Pauli 形式为

$$
(1-q)\rho+\frac q3(X\rho X+Y\rho Y+Z\rho Z),
$$

两式中的参数数值不相同。教材中的图、代码和公式必须用同一约定。

#### 与设备术语连接

可以在旁栏解释 $T_1$（能量弛豫）和 $T_2$（相位相干衰减），但不要把单一 Markov 模型写成所有硬件噪声的精确事实。相关噪声、串扰、泄漏、非 Markov 漂移和读出误差应在“模型局限”框中列出。IBM 当前噪声文档明确区分 Kraus、Pauli、退极化、振幅阻尼、相位阻尼、热弛豫与读出/复位误差，适合作为代码命名校对依据。

### 4.12 不可克隆：证明、边界和反例必须成套出现

#### 幺正内积证明

假设同一物理过程 $U$ 能把任意未知纯态和空白态复制：

$$
U|\psi\rangle|0\rangle=|\psi\rangle|\psi\rangle,
\qquad
U|\phi\rangle|0\rangle=|\phi\rangle|\phi\rangle.
$$

幺正保持内积，因此

$$
\langle\phi|\psi\rangle
=\langle\phi|\psi\rangle^2.
$$

令 $s=\langle\phi|\psi\rangle$，则 $s=s^2$，所以 $s=0$ 或 $1$。同一个完美复制器只能同时复制互相正交的状态，或本来相同的状态，不能完美复制任意非正交未知态。

#### 线性证明

若设备能复制 $|0\rangle$、$|1\rangle$，线性性给出

$$
U[(\alpha|0\rangle+\beta|1\rangle)|0\rangle]
=\alpha|00\rangle+\beta|11\rangle,
$$

而真正的两份副本应是

$$
(\alpha|0\rangle+\beta|1\rangle)^{\otimes2}
=\alpha^2|00\rangle+\alpha\beta|01\rangle
+\alpha\beta|10\rangle+\beta^2|11\rangle.
$$

一般不相等。

#### 必须写清的边界

- 已知正交基态可以被同一设备复制：CNOT 可将 $|0\rangle|0\rangle\mapsto|00\rangle$、$|1\rangle|0\rangle\mapsto|11\rangle$。
- 可以复制经典描述，然后重新制备；这要求先验知道状态。
- 可以做近似克隆、概率性克隆或克隆某个受限集合；定理禁止的是任意未知态的确定性完美克隆。
- 量子隐形传态不产生两份副本：原状态在协议过程中被测量破坏，并消耗纠缠和经典通信。

### 4.13 不可删除：最容易被误写的限制性定理

#### 正确任务

假设有两份相同未知态，试图用一个固定过程保留一份、把另一份变成与输入无关的空白态：

$$
|\psi\rangle|\psi\rangle|A\rangle
\longrightarrow
|\psi\rangle|0\rangle|A_\psi\rangle.
$$

线性/内积约束意味着未知态的信息不能凭空从第二份中消失；若输出系统看似被复位，信息必然转移到环境/辅助系统的关联中。原始论文为 Pati 与 Braunstein，2000-03-09。

#### 教材必须避免的错误说法

“不可删除定理说明量子比特不能被复位”是错的。复位信道

$$
\Phi(\rho)=|0\rangle\langle0|
$$

是合法 CPTP 映射；它只是把输入信息泄露/转移到环境，而不是在封闭、可逆演化中无痕消灭一份未知态。不可删除定理讨论的是对两份相同未知态进行“保留一份、无痕删掉另一份”的特定任务。

#### 与不可克隆的对照图

```text
不可克隆： |ψ>|0>  ↛ |ψ>|ψ>       （不能无中生有增加未知态副本）
不可删除： |ψ>|ψ>  ↛ |ψ>|0>       （不能无痕减少未知态副本）
开放复位： |ψ>_S|0>_E → |0>_S|ψ>_E（允许；信息转移到环境）
```

这张图应在正文出现，而不只是脚注。

## 五、一组可直接采用的“逐步推导型”例题

以下例题覆盖从初学者到入门研究生的递进层级。每题答案应展示中间步骤，而不是只给结果。

### 例 1：归一化与测量概率

给定未归一化向量 $v=(1+i,\sqrt2)^T$。

$$
\|v\|^2=|1+i|^2+|\sqrt2|^2=2+2=4,
$$

所以 $|\psi\rangle=v/2$。在 $Z$ 基测量，$p(0)=2/4=1/2$，$p(1)=2/4=1/2$。

### 例 2：外积与期望值

对 $|{+i}\rangle=(1,i)^T/\sqrt2$：

$$
\rho=\frac12\begin{pmatrix}1&-i\\i&1\end{pmatrix}.
$$

计算 $\langle Y\rangle=\operatorname{Tr}(Y\rho)=1$，$\langle X\rangle=\langle Z\rangle=0$；Bloch 向量为 $(0,1,0)$。

### 例 3：基变换测量

对 $|0\rangle$ 做 $X$ 基测量，利用 $|0\rangle=(|+\rangle+|-\rangle)/\sqrt2$，故两结果各 $1/2$。条件后态分别为 $|+\rangle$、$|-\rangle$。

### 例 4：门不对易

用 $|0\rangle$ 比较 $ZH|0\rangle=|-\rangle$ 与 $HZ|0\rangle=|+\rangle$，再计算 $HZ\neq ZH$。让读者同时按线路顺序和矩阵乘法检查。

### 例 5：张量积展开

$$
|+\rangle\otimes|1\rangle
=\frac{|01\rangle+|11\rangle}{\sqrt2}
=\frac1{\sqrt2}(0,1,0,1)^T.
$$

用 $I\otimes X$ 作用后得到 $(|00\rangle+|10\rangle)/\sqrt2$。

### 例 6：二比特可分判据

对 $|\psi\rangle=(|00\rangle+|01\rangle+|10\rangle+|11\rangle)/2$，系数矩阵行列式 $1/4-1/4=0$，且可因式分解为 $|+\rangle|+\rangle$。对 Bell 态，系数矩阵为 $I/\sqrt2$，行列式 $1/2\neq0$，所以纠缠。

### 例 7：Bell 态密度矩阵与偏迹

把

$$
\rho_{\Phi^+}=\frac12
\begin{pmatrix}
1&0&0&1\\
0&0&0&0\\
0&0&0&0\\
1&0&0&1
\end{pmatrix}
$$

按 $B$ 指标分块，对对应的 $2\times2$ 块取迹，得到 $\rho_A=I/2$。要求读者再算 $\rho_B$。

### 例 8：同样的 $Z$ 统计，不同的状态

比较 $|+\rangle\langle+|$ 与 $I/2$。两者 $Z$ 测量都是 $(1/2,1/2)$；$X$ 测量前者为 $(1,0)$，后者为 $(1/2,1/2)$。这是全书反复引用的基准例。

### 例 9：一般测量的完备性

给定 $M_0=|0\rangle\langle0|+\sqrt{1-\gamma}|1\rangle\langle1|$，$M_1=\sqrt\gamma|0\rangle\langle1|$，验证

$$M_0^\dagger M_0+M_1^\dagger M_1=I.$$

再对输入 $|1\rangle$ 求两结果概率与条件后态，连接到振幅阻尼的“量子跳跃”解释。

### 例 10：振幅阻尼信道

使用上一节 $\gamma=0.36$、输入 $|+\rangle$ 的完整矩阵计算，检查 Hermitian、迹、行列式/本征值。把“算输出”与“检查输出合法”作为两个评分点。

### 例 11：正但不完全正

对 Bell 态做第一子系统转置，得到

$$
\rho^{T_A}=\frac12
\begin{pmatrix}
1&0&0&0\\
0&0&1&0\\
0&1&0&0\\
0&0&0&1
\end{pmatrix},
$$

其中中间 $2\times2$ 块本征值为 $\pm1/2$，故整体有负本征值。这直观展示“完全正”不是多余术语。

### 例 12：不可克隆的数值反证

取 $|\psi\rangle=|0\rangle$、$|\phi\rangle=|+\rangle$，输入内积为 $1/\sqrt2$，理想双副本输出内积应为 $(1/\sqrt2)^2=1/2$。幺正过程不能改变内积，矛盾。

### 例 13：删除与复位的区别

构造 SWAP：$|\psi\rangle_S|0\rangle_E\mapsto|0\rangle_S|\psi\rangle_E$。只看系统 $S$，它被复位；看整体，信息没有消失。要求读者说明这为什么不违反不可删除。

## 六、图表与版式设计清单

### 6.1 必须有的图

1. 复平面：模、相位、共轭、相量相加。
2. ket/bra/内积/外积的形状图，标出 $d\times1$ 等尺寸。
3. Bloch 球：六个轴向纯态；另画球内混态，避免只画球面。
4. 全局相位与相对相位对照：同射线 vs 球面不同点。
5. H、X、Z、$R_x/R_y/R_z$ 的 Bloch 球旋转。
6. 电路时间方向与矩阵乘积顺序对照。
7. 张量积“二维×二维→四维”网格图及基序。
8. CNOT 对四个计算基态的真值表与箭头图。
9. Bell 制备线路，每一步的状态写在线路下方。
10. 纯乘积态与 Bell 态的系数矩阵/Schmidt 秩对照。
11. Bell 态和经典相关混态的密度矩阵热图。
12. 偏迹的索引收缩图；不要只给公式。
13. 投影测量树：分支概率、条件后态、忽略结果后的总态。
14. 系统—环境幺正→丢弃环境→Kraus 信道流程图。
15. 四类噪声在 Bloch 球上的几何效果。
16. 不可克隆/不可删除/开放复位三联图。

### 6.2 绘图规范

- 同一量用固定颜色：$|0\rangle$、$|1\rangle$、系统、环境、经典比特各自统一。
- 颜色之外再用线型或符号编码，保证色觉障碍读者可读。
- 任何矩阵热图必须有数值或色标，并注明基顺序。
- 电路图下方写出逐步状态；初次出现控制门时不能只放图标。
- Bloch 球注明它只完整表示“单量子比特密度矩阵”，不能直接表示二比特态。
- 图片说明要回答“图中看什么”，不能只写“Bloch 球示意图”。
- 长推导按等号对齐，每一步右侧用短语说明依据，如“插入完备关系”“使用正交性”。

## 七、语言与难度控制

### 7.1 应替换的模糊说法

| 不建议 | 建议改写 |
|---|---|
| “量子比特同时是 0 和 1” | “量子比特可处于 $\alpha|0\rangle+\beta|1\rangle$；测量概率及干涉由复振幅决定。” |
| “观察导致坍缩” | “按给定测量模型，得到结果 $m$ 后，条件态按明确公式更新。” |
| “纠缠粒子瞬间传递信息” | “局部结果具有相关性，但单方统计不能用于超光速传递可控信息。” |
| “量子并行一次算出所有答案” | “演化可同时改变许多振幅，但算法必须通过干涉把目标信息集中到可测统计中。” |
| “密度矩阵就是很多纯态的混合” | “密度矩阵统一描述制备不确定性和忽略子系统后的状态；同一矩阵可有多种系综分解。” |
| “噪声就是随机翻转” | “随机 Pauli 翻转只是部分噪声模型；能量弛豫、退相位、泄漏和相关噪声具有不同结构。” |
| “不可克隆意味着不能复制量子信息” | “不能用同一确定性物理过程完美复制任意未知、非正交量子态。” |
| “不可删除意味着不能擦除量子位” | “不能无痕删除两份相同未知态中的一份；复位可通过把信息转移到环境实现。” |

### 7.2 双层正文建议

- **主线正文**：只使用 $2\times2$、$4\times4$ 矩阵，给完整手算。
- **严格框**：给一般 $d$ 维定义、定理假设、证明。
- **计算实验**：用代码验证解析结果，但代码不能代替推导。
- **研究衔接**：列出术语英文、标准记号差异和继续阅读来源。

避免“显然”“容易得到”“不难证明”。若确实略去步骤，要说明略去的是代数展开、定理证明还是超出范围的背景。

## 八、逐章验收与缺陷扫描表

今后有正文后，每章至少按以下问题逐项检查。

### 8.1 正确性

- 是否在第一次出现时定义所有符号、维数和基顺序？
- ket 转 bra 时是否取了复共轭？
- 测量概率是否非负且和为 1？
- 后态是否归一化？是否区分条件/非选择后态？
- 所有门矩阵是否满足声称的幺正或 Hermitian 性？
- 张量积因子顺序是否从公式到图、代码、输出始终一致？
- 密度矩阵是否 Hermitian、正半定、迹为 1？
- 偏迹是否对正确子系统进行？
- Kraus 算子是否满足 $\sum K_k^\dagger K_k=I$？
- 噪声参数约定是否明示？
- 定理是否写全假设，是否错误扩大适用范围？

### 8.2 可学性

- 每引入一个抽象对象，是否先给具体二维例子？
- 每个公式是否说明“算什么”和“为什么需要”？
- 是否至少有一个错误示范或易混对照？
- 是否让读者在纸上完成一个短计算，而不是只看结论？
- 图是否与相邻正文共享同一符号和颜色？
- 是否跨越了未讲先修，例如在讲本征值前使用谱分解？
- 一段中是否同时引入超过三个新符号？若是，应拆分。

### 8.3 完整性

- 纯态讲完后，是否明确它只是一般状态的特殊情况？
- 纠缠是否同时有代数判据、局部统计和约化态三种视角？
- 测量是否覆盖概率、后态、忽略结果三部分？
- 信道是否说明完全正的必要性，而不只列 CPTP 缩写？
- 不可克隆/不可删除是否有允许情形和不适用情形？
- 每章是否有概念题、手算题、图解题和一个综合题？

### 8.4 人类写作风格

- 删除空泛句，如“量子世界充满无限可能”“让我们深入探索”。
- 不使用未解释的黑话，如“相干资源”“魔态”“信道可分解性”。
- 不把同一句结论用三种近义说法重复。
- 例子中的数字、状态和问题应服务于概念，不堆砌随机矩阵。
- 术语第一次出现写中文、英文和符号，后文固定一种称呼。

## 九、建议的练习体系与答案标准

每章设置四级题，防止全是机械算式或全是开放讨论。

1. **识别题**：指出维数、判断归一化、识别门或态。
2. **手算题**：完整算内积、门作用、测量、偏迹或 Kraus 输出。
3. **解释题**：用不超过三句话区分叠加/混合、相关/纠缠、复位/删除。
4. **综合题**：从线路得到状态，再求约化态、测量统计和噪声后的结果。

答案必须：

- 写出所用基顺序；
- 展示至少一个中间矩阵/状态；
- 对概率做归一化检查；
- 对密度矩阵做迹与正性检查；
- 对概念题指出定理条件，而非只给“是/否”。

可设置一个贯穿案例：从 $|00\rangle$ 制备 Bell 态，加入对第二比特的振幅阻尼，计算联合态、两个局部态、$Z$/$X$ 基相关性与条件测量后态。这个案例把前十章真正串起来。

## 十、后续多轮审查建议

### 第二轮：逐页数学审计

拿到正文后逐式复算，建立“公式编号—假设—维数—结果—数值测试”表。重点查共轭、门序、端序、偏迹指标和噪声参数。

### 第三轮：初学者可学性测试

让未学过量子力学、但学过高中数学或大学基础线代的读者试读。记录他们第一次卡住的位置，而不是只问“是否看懂”。重点观察狄拉克记号、张量积、条件测量和混态。

### 第四轮：研究生衔接审计

检查一般维数、POVM、CPTP、Choi、Schmidt 与信道等概念是否足以阅读标准文献；严格内容应放进阶框，不能反过来压垮主线。

### 第五轮：图文一致性与无障碍

核对图的基序、颜色、标签、归一化和文字说明；做灰度/色觉模拟；确保图不是装饰，而能独立回答一个问题。

### 第六轮：交叉一致性

统一全书的 $|q_1q_0\rangle$ 顺序、矩阵乘法方向、对数底、Bloch 向量、退极化参数、测量更新规则和“信道/操作/过程”等术语。

“某一轮没有发现问题”只能解释为：在预先定义的检查表、样例计算和读者测试范围内没有新问题；不能声称教材绝对无误。合理的停止条件是：所有高风险项关闭、所有公式通过独立复算、所有图通过一致性检查、目标读者完成核心练习时不再出现系统性卡点。

## 十一、可直接执行的完成标准

数学与计算基础模块达到可交付水平，应同时满足：

- 12 章知识链闭合，没有未讲先用；
- 每个抽象概念至少有一个二维/四维完整算例；
- 至少包含本报告列出的 16 类关键图；
- 至少 13 个基准例题全部给中间步骤并通过独立复算；
- 清楚区分纯态/混态、叠加/混合、相关/纠缠、概率/振幅、投影/POVM、正/完全正、删除/复位；
- 全书只采用一套基顺序与线路约定，软件差异用专栏说明；
- 不可克隆和不可删除同时给证明、反例边界与常见误读；
- 语言不依赖“神秘”“同时存在”“瞬间传递”等含混比喻；
- 初学者能完成主线题，入门研究生能读懂严格框并继续到 Watrous、Nielsen–Chuang、Preskill 等资料；
- 每次版本更新都重跑公式、图、术语和练习答案四类检查。

## 十二、来源使用备注

1. Watrous 2018 手稿偏严格，适合核对定义、定理和信道结构，不宜原样移植为初学者叙述。
2. IBM 两门 Watrous 课程的层次划分非常适合本项目：先纯态/电路，后密度矩阵/信道/一般测量；但软件端序与网页更新会变化，引用代码时要固定版本。
3. Nielsen–Chuang 适合建立完整学科结构；其 2010 周年版不是当前硬件状态的来源，本报告只把它用于稳定的理论基础。
4. Preskill 与 MIT OCW 适合补充系统—环境、算子和、测量和噪声的推导。
5. 原始论文用于准确划定不可克隆、不可删除、完全正和开放系统生成元的历史与逻辑边界；初学正文应使用现代记号重写，而不是长段引用。

---

本轮结论：由于尚无教材正文，当前最主要缺口不是某个局部段落，而是缺少可审查的正式内容。上述知识树可作为编写和下一轮逐页审计的共同基准。
