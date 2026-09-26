# 13｜量子信息量度：熵、距离与可提取信息

前面的章节说明了怎样写量子态、做测量和描述噪声。本章回答进一步的问题：一个状态包含多少不确定性？两个状态有多容易区分？相关性有多强？把经典消息编码进量子态后，接收方最多能读出多少信息？

先把本章的主线固定下来：

| 问题 | 主要量 | 最小操作含义 |
|---|---|---|
| 一个态有多混合？ | von Neumann 熵 $S(\rho)$ | 纯态为 0，最大混态达到维数允许的最大值 |
| 两个候选态多容易区分？ | 迹距离 $T(\rho,\sigma)$ | 决定等先验二元判别的最优成功率 |
| 两个态多相似？ | 根保真度 $F(\rho,\sigma)$ | 等于纯态内积的模，并与迹距离互相约束 |
| 两部分共有多少总相关？ | 互信息 $I(A:B)$ | 局部处理不能增加它 |
| 编码中最多可读出多少经典信息？ | Holevo 量 $\chi$ | 上界约束任意测量后的经典互信息 |

这些量不能互相替代。学习时要把“定义—手算—操作含义”三步连在一起，而不是只记一张公式表。

若数学已有些生疏，第一遍可先读 §1–3：从一张两结果概率表到纯态、混态与 Bell 态的熵；再看 §6–7 的“区分”与“相似”。§4–5 的纠缠资源率和相对熵、§8–11 的信道与编码界适合读过相应任务后回看。下表是用来查“该选哪个量”的地图，不要求首次读时把五个名字背下来。

## 1. 从经典熵开始

先考虑一个结果出现概率为 $1/4$ 的事件。用以 2 为底的对数写，它的“意外程度”是 $-\log_2(1/4)=2$ bit；若结果概率为 $1/2$，则是 $-\log_2(1/2)=1$ bit。这里 bit 是信息量单位，不是说仪器一次输出了两个二进制位。越少见的结果，出现时带来的这项数值越大；概率为 1 的确定结果给 $-\log_2 1=0$。前面的负号是因为 $0<p\le1$ 时 $\log_2p\le0$，这样意外程度才非负。

实验前还不知道哪种结果会发生，就把各结果的意外程度按其概率加权平均。对离散随机变量 $X$，每个取值 $x$ 的概率为 $p(x)$，这个平均数称为 **Shannon 熵**：

$$
H(X)=-\sum_xp(x)\log_2p(x).
$$

约定 $0\log_20=0$。熵的单位是 bit。

### 二元熵

若 $X\in\{0,1\}$，且 $\Pr(X=1)=p$，则

$$
h_2(p)=-p\log_2p-(1-p)\log_2(1-p).
$$

- $p=0$ 或 $1$：结果确定，$h_2(p)=0$；
- $p=1/2$：最不确定，$h_2(p)=1$；
- $p=1/4$：$h_2(1/4)\approx0.811$ bit。

最后一项也能自己算：$X=1$ 的概率为 $1/4$，意外程度是 $-\log_2(1/4)=2$；$X=0$ 的概率为 $3/4$，意外程度是 $-\log_2(3/4)\approx0.415$。因此

$$
h_2(1/4)
=\frac14\cdot2+\frac34\cdot0.415
\approx0.500+0.311=0.811\text{ bit}.
$$

这不是说某一次实验读到“0.811 bit”这个物理标签，而是许多同分布结果的不确定性量度。

熵不是“随机数大小”。取值可能是很大的整数，只要结果确定，熵仍为零。

## 2. von Neumann 熵

量子态的熵沿用上面的思路：先求密度矩阵 $\rho$ 的特征值 $\lambda_1,\lambda_2,\ldots$，这些数非负且总和为 1，于是可把它们放进同一个 $-\sum\lambda\log_2\lambda$ 计算。**不是**把矩阵的每个元素都各自取一次对数。压缩的矩阵写法叫 von Neumann 熵：

$$
S(\rho)=-\operatorname{Tr}(\rho\log_2\rho).
$$

若谱分解为

$$\rho=\sum_j\lambda_j|j\rangle\langle j|,$$

则

$$S(\rho)=-\sum_j\lambda_j\log_2\lambda_j.$$

也就是说，先求密度矩阵的特征值，再计算这些特征值的 Shannon 熵；上面的矩阵对数在特征向量方向上分别作用为普通的 $\log_2\lambda_j$。对零特征值沿用 $0\log_20=0$ 的极限约定。

### 三个单比特例子

1. 纯态 $|+\rangle\langle+|$ 的特征值为 $1,0$，故 $S=0$。
2. 最大混态 $I/2$ 的特征值为 $1/2,1/2$，故 $S=1$ bit。
3. $\rho=\operatorname{diag}(3/4,1/4)$ 已经是对角矩阵，两个特征值直接读作 $3/4,1/4$，故 $S(\rho)=-(3/4)\log_2(3/4)-(1/4)\log_2(1/4)=h_2(1/4)\approx0.811$ bit。

纯态熵为零不表示测量结果一定确定。$|+\rangle$ 在计算基测量仍随机；$S(\rho)$ 描述态本身的混合度，不等于任意指定测量的输出熵。

## 3. 联合熵、条件熵与互信息

先回忆经典情形。联合分布 $p(x,y)$ 的互信息可以写成

$$
I(X:Y)=H(X)+H(Y)-H(X,Y)
=\sum_{x,y}p(x,y)\log_2\frac{p(x,y)}{p(x)p(y)}.
$$

若 $X,Y$ 独立，则 $p(x,y)=p(x)p(y)$，所以 $I(X:Y)=0$。量子定义保留前一个“边缘熵相加减联合熵”的结构，但条件熵可能为负。

对二分量子态 $\rho_{AB}$：

$$
S(A)=S(\rho_A),\quad
S(B)=S(\rho_B),\quad
S(AB)=S(\rho_{AB}).
$$

量子条件熵和互信息定义为

$$
S(A|B)=S(AB)-S(B),
$$

$$
I(A:B)=S(A)+S(B)-S(AB).
$$

互信息衡量总相关，包括经典相关与量子相关。它总是非负。条件熵却可能为负，这是量子情形与经典情形的重要差别。

### Bell 态的负条件熵

对 $|\Phi^+\rangle$：

- 联合态是纯态，所以 $S(AB)=0$；
- 两个约化态都是 $I/2$，所以 $S(A)=S(B)=1$。

这里的“约化态”可以亲手算出。把 $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$ 写成密度矩阵时，有四项：

$$
\rho_{AB}=\frac12\bigl(
|00\rangle\langle00|+|00\rangle\langle11|
+|11\rangle\langle00|+|11\rangle\langle11|
\bigr).
$$

只保留 $A$ 时，对 $B$ 做**偏迹**。其计算规则是 $\operatorname{Tr}_B(|ij\rangle\langle k\ell|)=\delta_{j\ell}|i\rangle\langle k|$：$B$ 的两个标号相同才留下该项。所以上式两项交叉项消失，得到

$$
\rho_A=\operatorname{Tr}_B\rho_{AB}
=\frac12\bigl(|0\rangle\langle0|+|1\rangle\langle1|\bigr)=I/2.
$$

同理 $\rho_B=I/2$。总态是纯态，局部却是最大混态；这正是下面负条件熵算例所用的两组特征值。

因此

$$S(A|B)=0-1=-1,$$

$$I(A:B)=1+1-0=2.$$

这里的 2 bit 不是说测量一个量子比特能无条件读出两个经典位，而是联合量子态中总相关的熵量。超密编码还需要预共享纠缠和传送一个量子比特。

### 经典相关混态

$$
\rho_{AB}=\frac12|00\rangle\langle00|+
\frac12|11\rangle\langle11|.
$$

此时 $S(A)=S(B)=1$，$S(AB)=1$，故

$$I(A:B)=1,\qquad S(A|B)=0.$$

这再次区分了 Bell 纠缠与共享随机比特。

## 4. 纯二分态的纠缠熵

若 $|\psi\rangle_{AB}$ 是纯态，则

$$S(\rho_A)=S(\rho_B).$$

这个共同值称为纯态的纠缠熵。若 Schmidt 分解为

$$
|\psi\rangle=\sum_j\sqrt{\lambda_j}|u_j\rangle|v_j\rangle,
$$

则

$$E(|\psi\rangle)=H(\{\lambda_j\})=-\sum_j\lambda_j\log_2\lambda_j.$$

### 算例

$$
|\psi\rangle=\sqrt{0.9}|00\rangle+\sqrt{0.1}|11\rangle.
$$

约化态特征值为 $0.9,0.1$，所以纠缠熵

$$E=h_2(0.1)\approx0.469\text{ ebit}.$$

它小于 Bell 态的 1 ebit。ebit 是纯二分态纠缠熵的常用单位：一个 Bell 对含 1 ebit。这里的 $0.469$ ebit 应理解为渐近资源率。局域操作与经典通信（LOCC）是指相隔两地的参与者各自只操作手中的子系统，并可交换普通经典消息，但不直接传送量子系统。在这种免费操作约定下，许多份相同纯态可以做纠缠浓缩：当 $n\to\infty$ 时，输出 Bell 对数与 $n$ 的比率趋于 $h_2(0.1)\approx0.469$，同时输出态与相应理想 Bell 对的误差（例如迹距离）趋于零。它不是有限 $n$ 下的精确等式，更不表示单份态能确定性地变成“$0.469$ 个 Bell 对”。这里 $0.9,0.1$ 是 Schmidt 概率权重；Schmidt 系数本身是 $\sqrt{0.9},\sqrt{0.1}$。

对混态，约化熵不再单独等于纠缠量，因为它也可能来自经典混合。混态纠缠需要根据任务另选量度；本章不把它们压缩成一个“通用纠缠百分比”。

[第 18 章](18-channels-capacities-complexity.md)将用 LOCC 资源框架和可手算的负性说明：混态纠缠量必须连同任务与免费操作一起选择，并会区分两 qubit 的 PPT 充要判据与高维中的局限。

## 5. 相对熵与数据处理

经典 Kullback–Leibler 散度的量子对应为

$$
D(\rho\|\sigma)=
\operatorname{Tr}\bigl[\rho(\log_2\rho-\log_2\sigma)\bigr],
$$

前提是 $\operatorname{supp}(\rho)\subseteq\operatorname{supp}(\sigma)$，也就是 $\rho$ 不在 $\sigma$ 为零的方向上放置概率；否则定义为 $+\infty$。它通常不对称，因此不是数学意义上的距离。

数据处理不等式说，对任意量子信道 $\mathcal E$：

$$
D(\rho\|\sigma)\ge
D(\mathcal E(\rho)\|\mathcal E(\sigma)).
$$

直觉是：按相对熵衡量的信息，经过同一个物理处理或丢弃信息后不会增加。相对熵的精确操作含义可联系多副本、非对称假设检验；它不直接等于一次样本、等先验时的猜测成功率。后一个任务由下一节的迹距离精确刻画。测量本身也是信道，因此测量后的经典相对熵不会超过测量前的量子相对熵。

先用对角矩阵核对数量。令 $\rho=\operatorname{diag}(3/4,1/4)$、$\sigma=I/2$。两态已在同一基上对角，相对熵就是两组本征值的经典相对熵：

$$
\begin{aligned}
D(\rho\|\sigma)
&=\frac34\log_2\frac{3/4}{1/2}
 +\frac14\log_2\frac{1/4}{1/2}\\
&=1-h_2(1/4)\approx0.189\text{ bit}.
\end{aligned}
$$

若现在对两态施加**同一条**把任意输入复位为 $|0\rangle$ 的信道，两个输出相等，其相对熵变成 0。于是这个可手算的例子给出 $0.189\ge0$，但不能反推“只要一个具体信道使相对熵下降，就证明了对所有信道的数据处理不等式”；后者是更一般的定理。

[第 18 章](18-channels-capacities-complexity.md)会把这句话展开为量子 Stein 引理，明确区分第一类错误与第二类错误，并把结论写成最优错误概率的渐近指数而非有限样本近似。

## 6. 迹距离：最优区分能力

两个状态的迹距离定义为

$$
T(\rho,\sigma)=\frac12\|\rho-\sigma\|_1,
$$

其中

$$\|A\|_1=\operatorname{Tr}\sqrt{A^\dagger A}.$$

$0\le T\le1$。若先验概率各为 $1/2$，只给一个样本，在允许最优测量时正确判断状态的最大概率是 Helstrom 界：

$$
p_{\mathrm{guess}}^{\max}
=\frac12\bigl(1+T(\rho,\sigma)\bigr).
$$

### 先验不是各半时，先把权重放进矩阵

若先验为 $\eta$ 与 $1-\eta$，其中 $0\le\eta\le1$，则最优成功率是

$$
p_{\rm guess}^{\max}
=\frac12\left(1+\|\eta\rho-(1-\eta)\sigma\|_1\right).
$$

它不能只由未加权的 $T(\rho,\sigma)$ 和上面的等先验公式给出。即使完全不测量，总猜更常见的态也已有 $\max(\eta,1-\eta)$ 的成功率。设 $\rho=|0\rangle\langle0|,\sigma=|+\rangle\langle+|$，先验为 0.9、0.1，加权差矩阵是 $\left[\begin{smallmatrix}0.85&-0.05\\-0.05&-0.05\end{smallmatrix}\right]$。其本征值为 $(0.8\pm\sqrt{0.82})/2$，迹范数为 $\sqrt{0.82}$，最优成功率约 0.952769，高于总猜 0 的 0.9。[实验 F13](labs/foundations.md#f13先验不相等时08536不再是答案)给出完整特征方程和独立运行代码；一般公式可对照 [Watrous 教材第 3 章](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)。

### 例 1：正交态

$\rho=|0\rangle\langle0|$、$\sigma=|1\rangle\langle1|$，则 $T=1$，所以 $p_{\rm guess}=1$。计算基测量可完美区分。

### 例 2：非正交纯态

对纯态 $|\psi\rangle,|\phi\rangle$：

$$
T=\sqrt{1-|\langle\psi|\phi\rangle|^2}.
$$

取 $|\psi\rangle=|0\rangle$、$|\phi\rangle=|+\rangle$，内积模平方为 $1/2$，所以

$$
T=\frac1{\sqrt2},\qquad
p_{\rm guess}^{\max}=\frac12\left(1+\frac1{\sqrt2}\right)
\approx0.8536.
$$

若测量每次都必须在两个标签中选一个，非正交态不能被单次测量零错误地区分。这不排除“无歧义判别”：若允许第三种“无法判断”结果，线性无关的非正交纯态可以在部分轮次中零错误地认出。对这里等先验的 $|0\rangle,|+\rangle$，最优无歧义判别的成功概率为 $1-|\langle0|+\rangle|=1-1/\sqrt2\approx0.2929$，其余轮次必须报告无法判断。

### 把无歧义判别的测量写出来

令

$$
s=|\langle0|+\rangle|=\frac1{\sqrt2},
\qquad
c=\frac1{1+s}=2-\sqrt2.
$$

构造三个 POVM 元素：

$$
E_0=c|-\rangle\langle-|,
\qquad
E_+=c|1\rangle\langle1|,
\qquad
E_?=I-E_0-E_+.
$$

结果 $0$ 表示认定输入为 $|0\rangle$，结果 $+$ 表示认定输入为 $|+\rangle$，结果 $?$ 表示无法判断。先检查它不会误判：

$$
\langle+|E_0|+\rangle=0,
\qquad
\langle0|E_+|0\rangle=0.
$$

$E_0,E_+$ 都是非负常数乘以秩一投影，因此正半定。第三个元素在计算基中是

$$
E_?=
\begin{bmatrix}
1-c/2 & c/2\\
c/2 & 1-3c/2
\end{bmatrix},
$$

本征值为

$$
0,\qquad2(\sqrt2-1).
$$

两者都非负，所以 $E_?\succeq0$；三个元素之和又是 $I$，这确实是一组合法 POVM。两个输入被正确认出的概率分别为

$$
\langle0|E_0|0\rangle
=\langle+|E_+|+\rangle
=\frac c2
=1-\frac1{\sqrt2}.
$$

还要说明这个构造为什么最优。对任意零误判的三结果 POVM，记两个输入得到“无法判断”的概率为

$$
f_0=\langle0|E_?|0\rangle,
\qquad
f_+=\langle+|E_?|+\rangle.
$$

零误判意味着 $E_0|+\rangle=0$ 与 $E_+|0\rangle=0$；这里用了“正半定算符在某态上的期望为零，则它消去该态”。因此

$$
\langle0|E_?|+\rangle
=\langle0|+\rangle=s.
$$

对正半定的 $E_?$ 使用柯西—施瓦茨不等式（这里需要的具体形式就是下一行第一式），再用算术—几何平均不等式，得到

$$
f_0f_+\ge
|\langle0|E_?|+\rangle|^2=s^2,
$$

$$
\frac{f_0+f_+}{2}
\ge\sqrt{f_0f_+}
\ge s.
$$

等先验时，左边就是平均失败概率。因此任何零误判方案的成功率都不超过 $1-s$，而上面的构造恰好达到它。

## 7. 保真度：状态有多相似

本书采用“根保真度”约定：

$$
F(\rho,\sigma)=
\operatorname{Tr}\sqrt{\sqrt\rho\,\sigma\sqrt\rho}.
$$

若其中一个态是纯态：

$$
F(|\psi\rangle\langle\psi|,\sigma)
=\sqrt{\langle\psi|\sigma|\psi\rangle}.
$$

若两者都是纯态：

$$F=|\langle\psi|\phi\rangle|.$$

部分文献把 $F^2$ 称为保真度。引用数字时必须说明是否平方。本书的 $F$ 满足 Fuchs–van de Graaf 不等式：

$$
1-F(\rho,\sigma)
\le T(\rho,\sigma)
\le\sqrt{1-F(\rho,\sigma)^2}.
$$

### 算例

令 $\rho=|0\rangle\langle0|$，$\sigma=I/2$：

$$F=\sqrt{\langle0|I/2|0\rangle}=\frac1{\sqrt2},$$

$$T=\frac12\left\|\begin{bmatrix}1/2&0\\0&-1/2\end{bmatrix}\right\|_1=\frac12.$$

上下界为 $1-1/\sqrt2\le1/2\le1/\sqrt2$，成立。

## 8. 信道不会增加可区分性

对任意量子信道 $\mathcal E$：

$$
T(\mathcal E(\rho),\mathcal E(\sigma))
\le T(\rho,\sigma),
$$

$$
F(\mathcal E(\rho),\mathcal E(\sigma))
\ge F(\rho,\sigma).
$$

噪声和丢弃子系统通常让状态更难区分：迹距离缩小，保真度增大。第二个不等式中的“保真度变大”不是设备变好，而是两个候选输出变得更相似。

## 9. Holevo 信息：一组量子态能承载多少可访问经典信息

Alice 以概率 $p_x$ 选择经典消息 $x$，并发送量子态 $\rho_x$。平均态为

$$
\bar\rho=\sum_xp_x\rho_x.
$$

Holevo 量定义为

$$
\chi=S(\bar\rho)-\sum_xp_xS(\rho_x).
$$

接收方选择 POVM $\{M_y\}$ 测量量子态，得到经典结果 $Y$。把所有测量中经典互信息的最大值定义为可访问互信息：

$$
I_{\rm acc}(\{p_x,\rho_x\})
=\max_{\{M_y\}}I(X:Y).
$$

Holevo 界说明，任意一个具体测量都满足

$$I(X:Y)\le\chi.$$

若所发送系统的 Hilbert 空间维数为 $d$，还有

$$
I_{\rm acc}\le\chi\le\log_2d.
$$

因此在没有预共享纠缠、只发送一个 $n$ 量子比特寄存器的模型中，$d=2^n$，可访问经典信息不超过 $n$ bit。这个结论不是说量子态的数学描述只有 $n$ 个参数，也不是说改变资源模型后仍能忽略额外资源。预共享纠缠会改变通信所需资源：超密编码既消耗预共享 Bell 对，也发送一个量子比特，因此没有违反上述无辅助模型的维数上界。

### 正交编码

Alice 以各 $1/2$ 概率发送 $|0\rangle$ 或 $|1\rangle$。两态纯，所以第二项为零；平均态为 $I/2$，故

$$\chi=S(I/2)=1.$$

计算基测量达到 1 bit。

### 非正交编码

Alice 以各 $1/2$ 概率发送 $|0\rangle$ 或 $|+\rangle$。平均态

$$
\bar\rho=\frac12|0\rangle\langle0|+
\frac12|+\rangle\langle+|
=\begin{bmatrix}3/4&1/4\\1/4&1/4\end{bmatrix}.
$$

其特征值为

$$
\lambda_\pm=\frac12\left(1\pm\frac1{\sqrt2}\right).
$$

因两个条件态都纯，

$$
\chi=h_2\left(\frac12\left(1+\frac1{\sqrt2}\right)\right)
\approx0.601\text{ bit}.
$$

这给出任何单次测量所能取得互信息的上界，但此例并不能达到该上界。先把一个实际测量写出来。取正交基

$$
|m_0\rangle=
\cos\frac\pi8|0\rangle-
\sin\frac\pi8|1\rangle,
$$

$$
|m_+\rangle=
\sin\frac\pi8|0\rangle+
\cos\frac\pi8|1\rangle,
$$

并测量投影 $|m_0\rangle\langle m_0|$ 与 $|m_+\rangle\langle m_+|$。把结果 $m_0$ 记为 $Y=0$、结果 $m_+$ 记为 $Y=+$。令

$$
q=\cos^2\frac\pi8
=\frac12\left(1+\frac1{\sqrt2}\right),
$$

$$
p_e=\sin^2\frac\pi8
=\frac12\left(1-\frac1{\sqrt2}\right)
\approx0.1464.
$$

四个条件概率为：

| 输入 $X$ | $Y=0$ | $Y=+$ |
|---|---:|---:|
| $0$ | $q$ | $p_e$ |
| $+$ | $p_e$ | $q$ |

例如

$$
\Pr(Y=0\mid X=+)
=|\langle m_0|+\rangle|^2
=p_e.
$$

两个输入等先验且信道对称，所以两个输出也各以 $1/2$ 概率出现，$H(Y)=1$ bit；给定输入后的输出熵为 $H(Y|X)=h_2(p_e)$。这个具体测量取得

$$
I(X:Y)=H(Y)-H(Y|X)
=1-h_2(p_e)
\approx0.399\text{ bit}.
$$

对等先验二元纯态集合，Levitin 的最优测量结果表明，这组投影测量同时达到最小错误率和最大互信息。因此在本例中

$$
I_{\rm acc}=1-h_2(p_e)\approx0.399\text{ bit}<\chi\approx0.601\text{ bit}.
$$

这组数直接展示了“可访问互信息”与 Holevo 上界之间可能有严格间隙。Helstrom 测量优化二元猜测错误率；最大互信息与最小错误率是相关但不同的优化目标，本例中最优测量相同是这个对称二元纯态情形的性质，不能推广成一般等价。

从“给定态集合的上界”走到“每次信道使用可传多少”，还需优化编码并考虑多次联合使用。[第 18 章](18-channels-capacities-complexity.md)将区分经典、量子、私密与纠缠辅助经典容量，声明各自的免费资源，并用可达率与上界两面完整计算 qubit 擦除信道。

## 10. 无广播比不可克隆更一般

不可克隆讨论任意未知纯态的完美复制。无广播定理扩展到混态：一组状态能被同一个信道广播，当且仅当这些状态彼此对易。广播要求两个输出的边缘态都等于输入态，不要求联合输出是两个独立副本。

因此：

- 彼此正交、可共同对角化的经典信息可以广播；
- 一般不对易量子态不能被完美广播；
- “量子信息不能复制”必须保留候选态集合和完美、通用等条件。

## 11. 熵不等式的地图

| 性质 | 公式 | 直觉 |
|---|---|---|
| 次可加性 | $S(AB)\le S(A)+S(B)$ | 联合不确定性不超过分别相加 |
| Araki–Lieb | $|S(A)-S(B)|\le S(AB)$ | 两边熵差受联合熵限制 |
| 强次可加性 | $S(ABC)+S(B)\le S(AB)+S(BC)$ | 条件互信息非负 |
| 数据处理 | $I(A:C)\ge I(A:\mathcal E(C))$ | 局部处理不能创造与外部的相关 |

强次可加性是量子信息论的核心工具。初学阶段重点是会用结论判断方向，不必在本章掌握完整证明。

## 12. 指标选择清单

- 问“态有多混合”：看 $S(\rho)$ 或纯度，但二者不是同一个量。
- 问“两个态能否区分”：看迹距离和具体先验下的 Helstrom 界。
- 问“两个态有多接近”：看保真度，并说明平方约定。
- 问“两个子系统共有多少总相关”：看互信息。
- 问“纯二分态有多少纠缠”：看约化熵。
- 问“编码的经典消息最多能提取多少信息”：看 Holevo 量和通信模型。

不要把一个指标叫作通用的“量子信息含量”。不同操作任务对应不同量度。

## 13. 常见误区

- 纯态熵为零，不等于所有测量都无随机性。
- 互信息为 2 bit，不等于能从一个孤立量子比特读出 2 bit。
- 保真度提高可能只是噪声把两个候选态压得更相似。
- 相对熵不对称，不是普通距离。
- Holevo 界限制可访问经典信息，不表示能一次读出量子态的全部振幅。
- 约化熵只对整体纯态可直接作为纠缠熵。

## 14. 自检

1. 求 $\rho=\operatorname{diag}(0.8,0.2)$ 的 von Neumann 熵。
2. 对 Bell 态和经典相关混态分别计算 $S(AB)$、$S(A|B)$ 与 $I(A:B)$。
3. 等概率区分 $|0\rangle$ 与 $(\sqrt3|0\rangle+|1\rangle)/2$，求最优成功概率。
4. 在本书约定下，求 $|+\rangle$ 与 $I/2$ 的保真度和迹距离。
5. 计算等概率 $|0\rangle,|1\rangle$ 编码的 Holevo 量，并说明哪种测量达到它。
6. 为什么对混合 $\rho_{AB}$，$S(\rho_A)$ 一般不能直接称为纠缠量？

答案见[练习与答案：第 13 章](appendices/exercises.md#第-13-章)。

## 配套数值实验与展开答案

重新求不等先验的 Helstrom 成功率，并核对根保真度与软件平方保真度的关系。改变先验会改变最优判别，两个候选态本身的保真度却不变。

题目和逐步解答见[基础实验册](labs/foundations.md)，本章程序编号为 `13`。可从[代码说明](../codes/foundations/README.md)进入独立脚本与保存的运行结果。所有模拟样本均明确标作合成数据，不是硬件实验。

## 参考起点

- John Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/)，第 3、5、6 章。
- D. Petz, [Monotonicity of quantum relative entropy revisited](https://arxiv.org/abs/quant-ph/0209053) (2002)：相对熵的数据处理性质及其等号条件。
- John Preskill, [Quantum Computation lecture notes](https://www.preskill.caltech.edu/ph229/)，量子态、熵与量子 Shannon 理论章节。
- John Preskill, [Ph/CS 219A Lecture 2: Density Operators](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-2-Density-Operators.pdf)（偏迹的计算规则）。
- IBM Quantum Learning, [Fidelity](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/purifications-and-fidelity/fidelity)，含两种保真度约定与 Fuchs–van de Graaf 不等式。
- A. S. Holevo, [Bounds for the quantity of information transmitted by a quantum communication channel](https://www.mathnet.ru/eng/ppi903), *Problems of Information Transmission* 9, 177–183 (1973)。
- C. H. Bennett, H. J. Bernstein, S. Popescu, B. Schumacher, [Concentrating partial entanglement by local operations](https://doi.org/10.1103/PhysRevA.53.2046), *Physical Review A* 53, 2046–2052 (1996)：纯态纠缠熵作为渐近 Bell 对浓缩率的原始结果。
- I. D. Ivanovic, [How to differentiate between non-orthogonal states](https://doi.org/10.1016/0375-9601(87)90222-2), *Physics Letters A* 123, 257–259 (1987)；D. Dieks, [Overlap and distinguishability of quantum states](https://doi.org/10.1016/0375-9601(88)90840-7), *Physics Letters A* 126, 303–306 (1988)；A. Peres, [How to differentiate between non-orthogonal states](https://doi.org/10.1016/0375-9601(88)91034-1), *Physics Letters A* 128, 19 (1988)：无歧义判别的原始工作。
- L. B. Levitin, [Optimal Quantum Measurements for Two Pure and Mixed States](https://link.springer.com/chapter/10.1007/978-1-4899-1391-3_43), in *Quantum Communications and Measurement*, pp. 439–448, Plenum Press (1995)：二元纯态集合的最大互信息与最优测量。
- H. Barnum et al., [Noncommuting mixed states cannot be broadcast](https://doi.org/10.1103/PhysRevLett.76.2818), *Physical Review Letters* 76, 2818 (1996)。
