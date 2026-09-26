# 03｜多量子比特、纠缠与约化态

这一章从两个量子比特开始。读完后应能自己完成三件事：按固定顺序写出四个基态；判断一个**两比特纯态**是否可拆成两个单比特态；从联合态算出只看其中一方时的概率。最后再用这些计算区分纠缠与经典相关。需要复习列向量、矩阵乘法或张量积时，可以先回看[数学工具章](01-math.md)第 2、4、7 节。

第 1–4 节是主线，第 5–6 节帮助整理“纠缠究竟多在何处”；Bell 不等式和单配性可以读完主线后再看。这里所有基序都固定为 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$：左边的字符属于 $A$，右边属于 $B$。一些软件采用不同的比特显示顺序，照搬其结果前务必核对约定。

## 1. 从两个比特的四种结果到联合态

### 为什么是四维

一个经典比特有 0、1 两个可能值。两个比特一起记录时，要同时写出两人的结果：$00,01,10,11$，共 $2\times2=4$ 种。量子情形把它们记作四个相互正交的计算基态：

$$
|00\rangle=|0\rangle_A\otimes|0\rangle_B,
\quad |01\rangle=|0\rangle_A\otimes|1\rangle_B,
\quad |10\rangle=|1\rangle_A\otimes|0\rangle_B,
\quad |11\rangle=|1\rangle_A\otimes|1\rangle_B.
$$

张量积符号 $\otimes$ 的意思不是普通乘法，而是按两个系统的顺序组合坐标。以 $|0\rangle=(1,0)^T$、$|1\rangle=(0,1)^T$ 为例，先放第一个向量的第一项乘整个第二向量，再放第二项乘整个第二向量：

$$
|0\rangle\otimes|1\rangle
=\begin{bmatrix}1\cdot0\\1\cdot1\\0\cdot0\\0\cdot1\end{bmatrix}
=\begin{bmatrix}0\\1\\0\\0\end{bmatrix}.
$$

因此 $|01\rangle$ 是四维列向量的第二格，而 $|10\rangle$ 是第三格。两者不能互换；同样，$|0\rangle_A\otimes|1\rangle_B$ 不是“先写 B 再写 A”。

### 把两个单比特态真正乘开

设 $A$ 的态是 $|u\rangle=u|0\rangle+v|1\rangle$，$B$ 的态是 $|w\rangle=s|0\rangle+t|1\rangle$。其中 $u,v,s,t$ 是复数，且两个单比特态各自归一化。像普通括号相乘一样使用分配律，但不调换两个系统的顺序：

$$
\begin{aligned}
|u\rangle\otimes|w\rangle
&=(u|0\rangle+v|1\rangle)\otimes(s|0\rangle+t|1\rangle)\\
&=us|00\rangle+ut|01\rangle+vs|10\rangle+vt|11\rangle.
\end{aligned}
$$

四个系数的顺序是 $us,ut,vs,vt$。例如 $|+\rangle_A\otimes|1\rangle_B$，其中 $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$，可直接得到

$$
|+\rangle|1\rangle=\frac{|01\rangle+|11\rangle}{\sqrt2}
=\begin{bmatrix}0\\1/\sqrt2\\0\\1/\sqrt2\end{bmatrix}.
$$

测量两个比特的计算基时，出现 $01$ 和 $11$ 的概率各是振幅的模平方 $1/2$；$00$、$10$ 的概率是 0。这是一次测量的**四种可能结果**，不是一次测量同时读出四个数。

### 推广到 $n$ 个量子比特

$n$ 个量子比特的纯态位于 $2^n$ 维复向量空间：

$$|\psi\rangle=\sum_{x\in\{0,1\}^n}\alpha_x|x\rangle,
\qquad \sum_x|\alpha_x|^2=1.$$

这里 $x$ 是长度为 $n$ 的 0/1 字符串，每个 $\alpha_x$ 是一个复数振幅；对某一具体字符串 $x$ 做计算基测量，概率为 $|\alpha_x|^2$。之所以是 $2^n$，是因为每增加一个比特，每个旧字符串都各接出一个 0 和一个 1，数量翻倍。两比特有 4 个，三比特有 8 个。

式子列出了描述一般纯态所需的坐标数；它**不**表示一次测量能读出所有振幅，也不自动保证算法加速。准备态、实施操作、重复测量都需要资源。

## 2. 可分态与纠缠态

如果联合纯态能写成 $|u\rangle_A\otimes|w\rangle_B$，称为**可分纯态**或乘积态：可分别给 $A$、$B$ 指定单比特纯态。若写不成任何这样的乘积，就称为**纠缠纯态**。这个定义说的是整个联合态的结构，不是说两个比特是否放得很近，也不是说测量结果是否相关。

把一般两比特纯态按本章基序写成

$$|\psi\rangle=a|00\rangle+b|01\rangle+c|10\rangle+d|11\rangle$$

其中 $|a|^2+|b|^2+|c|^2+|d|^2=1$。判断这个**纯态**可分，有一个简短的四格测试：

$$ad-bc=0.$$

只有等式成立才可分；不等于零就是纠缠。这里 $a,b,c,d$ 可以是复数，计算时照常做复数乘法。

### 为什么这个测试成立

前一节已经乘开乘积态，得到 $a=us,b=ut,c=vs,d=vt$。于是

$$
ad-bc=(us)(vt)-(ut)(vs)=uvst-uvts=0.
$$

这说明**只要可分，测试一定得零**。反过来为何也成立？先看 $a\ne0$。由 $ad=bc$ 可得 $d=bc/a$，直接按四项展开：

$$
|\psi\rangle=(a|0\rangle+c|1\rangle)
\otimes\left(|0\rangle+\frac ba|1\rangle\right).
$$

右边展开所得的 $|11\rangle$ 系数是 $c(b/a)=d$。两因子在此未分别写成长度 1，但由于乘积已经是归一化态，总能把其中一个因子的长度移给另一个，分别归一化而不改联合态。若 $a=0$，由 $bc=0$ 可知至少 $b$、$c$ 中一个是零：$b\ne0$ 时，态为 $(b|0\rangle+d|1\rangle)\otimes|1\rangle$；$b=0$ 时，态为 $|1\rangle\otimes(c|0\rangle+d|1\rangle)$。所以没有漏掉边界情况。熟悉线性代数后，也可把 $a,b,c,d$ 排成 $2\times2$ 矩阵，理解为行列式为零、秩为一。

### 同样有相关性，却有不同结构

$$\frac{|00\rangle+|01\rangle}{\sqrt2}=|0\rangle\otimes|+\rangle$$

的四系数是 $(a,b,c,d)=(1/\sqrt2,1/\sqrt2,0,0)$，故 $ad-bc=0$。它是可分态。另一种可分态 $(|00\rangle+|10\rangle)/\sqrt2=|+\rangle\otimes|0\rangle$；交换左右两人的位置，四格便不同。

再看

$$|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}$$

的四系数 $(1/\sqrt2,0,0,1/\sqrt2)$。算得 $ad-bc=1/2\ne0$，所以它不是两个单比特纯态的乘积。不要把式中的加号解读成“两个比特预先约定好了同一个随机数”；第 6 节会把这两种情况放在相同测量基下检验。

**马上核对。** $|+\rangle_A|+\rangle_B$ 的四系数是多少？先乘两个括号，得四格都为 $1/2$；再算 $ad-bc=(1/2)(1/2)-(1/2)(1/2)=0$。

## 3. Bell 态

下面四个特别常用的纠缠纯态统称 **Bell 态**。每个态都只有两个非零振幅，两个模平方都是 $1/2$，所以长度为 1：

$$
|\Phi^\pm\rangle=\frac{|00\rangle\pm|11\rangle}{\sqrt2},\qquad
|\Psi^\pm\rangle=\frac{|01\rangle\pm|10\rangle}{\sqrt2}.
$$

先不要把 $\Phi$、$\Psi$、$+$、$-$ 当成四套新规则。$\Phi$ 这一对只含 $00,11$，$\Psi$ 这一对只含 $01,10$；右上角的 $+$ 或 $-$ 指两项之间的**相对符号**。例如 $\Phi^+$ 和 $\Phi^-$ 在计算基都有 $00,11$ 各半，却不是同一量子态。把其中一个整体乘以 $-1$ 是不可观察的全局相位；只翻转两个振幅中的一个，才会改变相对相位。

四个 Bell 态彼此正交。以最容易混淆的一对为例：

$$
\langle\Phi^+|\Phi^-\rangle
=\frac12(\langle00|+\langle11|)(|00\rangle-|11\rangle)
=\frac12(1-1)=0.
$$

其余跨 $\Phi$、$\Psi$ 的内积也为零，因为 $00,11$ 与 $01,10$ 各不相同。四维空间里有四个正交归一向量，所以它们也是一组基。若只有计算基测量，能分辨 $\Phi$ 与 $\Psi$ 这两组，却不能分辨同组的正负号；要看相对符号，必须改变测量基或进行合适的联合测量。

### 同一态换成 $X$ 基，会看到什么

第 02 章定义 $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$、$|-\rangle=(|0\rangle-|1\rangle)/\sqrt2$。将两个括号展开：

$$
\begin{aligned}
|++\rangle&=\tfrac12(|00\rangle+|01\rangle+|10\rangle+|11\rangle),\\
|--\rangle&=\tfrac12(|00\rangle-|01\rangle-|10\rangle+|11\rangle).
\end{aligned}
$$

两式相加时，中间的 $01,10$ 项抵消，故

$$|\Phi^+\rangle=\frac{|++\rangle+|--\rangle}{\sqrt2}.$$

同理，$|\Phi^-\rangle=(|+-\rangle+|-+\rangle)/\sqrt2$。所以测量两边的 $X$ 基时，$\Phi^+$ 只给同号 $++$ 或 $--$，$\Phi^-$ 只给异号 $+-$ 或 $-+$；每种允许结果的概率各是 $1/2$。**相对负号没有消失**，只是换基后表现为可见的相关类型变化。

### 实验上怎样证明不是普通相关

只看到 00 与 11 各约一半，不能证明制备了 $|\Phi^+\rangle$；经典混合态

$$
\frac12|00\rangle\langle00|+\frac12|11\rangle\langle11|
$$

也产生相同的计算基统计。实验至少还要测量其他基中的相干信息，并用态层析、纠缠见证或 Bell 不等式等方法给出带不确定度的判据。态层析依赖制备与测量模型；Bell 违背能作更强的设备无关陈述，但要求合适的测量设置并处理实验漏洞。“制备线路包含一个纠缠门”也不是纠缠已经成功的证据。

## 4. 局部操作不能单独揭示整个纠缠态

如果只拿到联合系统的一个比特，应该用什么状态预测它的测量结果？先要把两种“不知道”分开：一个**纯态** $|\psi\rangle$ 可以写成密度矩阵 $\rho=|\psi\rangle\langle\psi|$；若实验人员以经典概率 $p_j$ 制备不同纯态、又不告诉我们本轮是哪一个，状态是 $\rho=\sum_jp_j|\psi_j\rangle\langle\psi_j|$。后一式是概率加权的**矩阵**之和，不是把 ket 直接相加。完整合法性条件与一般演化留到第 05 章。

### 先把 Bell 态写成四乘四矩阵

Bell 态的密度矩阵为

$$
\rho_{AB}=|\Phi^+\rangle\langle\Phi^+|
=\frac12\left(
|00\rangle\langle00|+|00\rangle\langle11|
+|11\rangle\langle00|+|11\rangle\langle11|
\right).
$$

按 $00,01,10,11$ 作行列顺序，$|\Phi^+\rangle=(1,0,0,1)^T/\sqrt2$。列向量乘它的共轭行向量，逐格得到

$$
\rho_{AB}=\frac12
\begin{bmatrix}
1&0&0&1\\
0&0&0&0\\
0&0&0&0\\
1&0&0&1
\end{bmatrix}.
$$

左上角、右下角各表示 $00,11$ 的概率 $1/2$；右上角、左下角的 $1/2$ 是连接 $00$ 与 $11$ 的**相干项**，不是额外的测量结果概率。稍后会看到，经典混合缺少这两格。

### 偏迹究竟把哪些格相加

**约化态** $\rho_A$ 是只观察 $A$ 时的状态。要从联合态求它，对不观察的 $B$ 做**偏迹**，记作 $\rho_A=\operatorname{Tr}_B(\rho_{AB})$。名字中的“迹”提醒我们：固定 $A$ 的行列标签，把 $B$ 的相同标签 $0,0$ 与 $1,1$ 对应的格相加。若联合矩阵的元素写成 $\rho_{ab,cd}=\langle ab|\rho|cd\rangle$，则

$$
(\rho_A)_{a,c}=\rho_{a0,c0}+\rho_{a1,c1},
\qquad a,c\in\{0,1\}.
$$

例如左上格是 $\rho_{00,00}+\rho_{01,01}=1/2+0=1/2$；右上格是 $\rho_{00,10}+\rho_{01,11}=0+0=0$。另外两格也按相同规则计算，合起来就是

$$
\rho_A=\operatorname{Tr}_B(\rho_{AB})
=\frac12(|0\rangle\langle0|+|1\rangle\langle1|)
=\frac I2.
$$

![对 B 做偏迹时，联合矩阵中 B 的行列标签相同的两格相加，成为 A 的一格](assets/partial-trace-grid.svg)

图中只画了 $\rho_A$ 左上角与右下角的两个求和；非对角格也按同一规则配对。原矩阵里的相干项 $\rho_{00,11}$ 没有被“忽略是不重要的”，它只是不能影响单独观察 $A$ 的统计；一旦改做两比特联合测量，它仍会影响结果。

这并不是“删掉写有 $B$ 的符号”。一般定义是在 $B$ 的任意正交归一基 $\{|j\rangle_B\}$ 中求和：

$$
\operatorname{Tr}_B(\rho_{AB})
=\sum_j(I_A\otimes\langle j|_B)\rho_{AB}(I_A\otimes|j\rangle_B).
$$

前面四格规则正是这一定义在计算基 $j=0,1$ 中的写法。也可以直接对 ket-bra 的每一项使用

$$
\operatorname{Tr}_B(|a\rangle\langle c|\otimes|b\rangle\langle d|)
=\langle d|b\rangle\,|a\rangle\langle c|,
$$

这里 $a,c$ 属于 $A$，$b,d$ 属于 $B$；只有 $b=d$ 的项保留。于是 $|00\rangle\langle11|$ 和 $|11\rangle\langle00|$ 因 $\langle1|0\rangle=0$ 而消失，另外两项分别留下 $|0\rangle\langle0|$ 和 $|1\rangle\langle1|$。两种算法所得矩阵一致。

偏迹之所以是“只观察 $A$ 时的正确状态”，不只是因为它能给出计算基概率。对任意只作用在 $A$ 上的可观察量 $O_A$，都有

$$
\operatorname{Tr}\!\left[(O_A\otimes I_B)\rho_{AB}\right]
=\operatorname{Tr}(O_A\rho_A),
\qquad \rho_A=\operatorname{Tr}_B(\rho_{AB}).
$$

左边用完整联合态算局域实验，右边只用约化态算；两者对所有 $O_A$ 都相等。用最简单的 $O_A=|0\rangle\langle0|$ 检查，两边都给 Alice 测到 0 的概率 $1/2$。所以 $\rho_A$ 保留了 Alice 单独能测到的全部统计，而不是随意丢掉矩阵元。

### 算例：约化态不一定是最大混态

考虑部分纠缠纯态

$$
|\psi\rangle_{AB}=\frac{\sqrt3}{2}|00\rangle+\frac12|11\rangle.
$$

先核对归一化：$|\sqrt3/2|^2+|1/2|^2=3/4+1/4=1$。把列向量 $(\sqrt3/2,0,0,1/2)^T$ 乘共轭行向量，得到

$$
\rho_{AB}=\begin{bmatrix}
3/4&0&0&\sqrt3/4\\
0&0&0&0\\
0&0&0&0\\
\sqrt3/4&0&0&1/4
\end{bmatrix}.
$$

按同一四格规则偏迹，两个交叉项的 $B$ 标签不同，不能进入求和，所以

$$
\rho_A=\frac34|0\rangle\langle0|+
\frac14|1\rangle\langle1|
=\begin{bmatrix}3/4&0\\0&1/4\end{bmatrix}.
$$

直接从联合态计算 Alice 的 $Z$ 期望值，得到

$$
\langle\psi|(Z\otimes I)|\psi\rangle
=\frac34-\frac14=\frac12.
$$

从约化态计算也得到

$$
\operatorname{Tr}(Z\rho_A)=\frac34-\frac14=\frac12.
$$

整体态是纯态，但 $\operatorname{Tr}(\rho_A^2)=(3/4)^2+(1/4)^2=5/8<1$，所以局部态是混态；它又不等于 $I/2$，说明“纠缠纯态的局部状态”不必总是最大混态。

回到前面的 Bell 态：虽然整体是纯态，任一子系统却是最大混态 $I/2$。这里“最大混态”指本征值相等的单比特混态；无论测哪个方向，两个结果的概率都各半。它不表示每次实验没有确定记录。

### 测量一方：先算概率，再分清是否保留记录

让 Alice 在计算基测量 $A$。结果 0 对应投影 $P_0=|0\rangle\langle0|_A\otimes I_B$，结果 1 对应 $P_1=|1\rangle\langle1|_A\otimes I_B$。在 $|\Phi^+\rangle$ 上，$P_0|\Phi^+\rangle=|00\rangle/\sqrt2$，其长度平方是 $p_0=1/2$；归一化后，**已知结果为 0 的联合后态**是 $|00\rangle$。同理 $p_1=1/2$，已知结果为 1 的联合后态是 $|11\rangle$。

如果 Alice 做了测量，却丢弃或不公布记录，就不能挑选其中一个分支；联合态是两个条件态按结果概率混合：

$$
\rho'_{AB}=\frac12|00\rangle\langle00|+\frac12|11\rangle\langle11|.
$$

这仍有经典相关，但已不是原来的 Bell 纯态。Bob 单独的态在操作前后都是 $I/2$。若 Bob 只看自己的数据，他甚至分不出 Alice 是否已经测量；若后来收到 Alice 的经典记录，他才能按结果分组，看到条件相关。

同样方法用于部分纠缠态 $\sqrt3|00\rangle/2+|11\rangle/2$，Alice 得到 0、1 的概率分别是 $3/4,1/4$；条件联合后态仍分别为 $|00\rangle,|11\rangle$；丢弃记录后的联合态是 $\tfrac34|00\rangle\langle00|+\tfrac14|11\rangle\langle11|$。**概率随初态改变，但“条件态与非选择态不能混写”的规则不变。**

沿着刚才的方向看：Alice 测了 Bell 态，却不把结果告诉 Bob。Bob 必须把两个可能的条件态按概率合起来，所以他的无条件态仍是

$$
\rho_B'=\sum_{k=0}^1p_k\rho_{B|k}
=\tfrac12|0\rangle\langle0|+\tfrac12|1\rangle\langle1|=I/2.
$$

他单看本地统计，分不出 Alice 是否测量。交换 Alice、Bob 的角色，结论同样成立：Bob 在远方做局域操作，也不能改变 Alice 的无条件统计；若双方事后通过经典通信按记录分组，条件态可以不同。这叫**无信号性质**，不允许靠纠缠超光速传消息。本章只用 Bell 态作直观检查；一般证明还需第 05 章的局域量子操作形式。

**马上核对。** 对 $|\Psi^-\rangle=(|01\rangle-|10\rangle)/\sqrt2$，Alice 测到 0 时 Bob 是什么态？保留 $A=0$ 的项，得到未归一化 $|01\rangle/\sqrt2$；概率 $1/2$，条件态为 $|01\rangle$，所以 Bob 是 $|1\rangle$。

## 5. Schmidt 分解

刚才的 $\sqrt3|00\rangle/2+|11\rangle/2$ 有一个方便之处：两项中，$A$ 用到的 $|0\rangle,|1\rangle$ 互相正交，$B$ 用到的也是如此。Bell 态也有这种两边成对正交的写法。若一个纯态最初看上去有四项，适当给 $A$ 和 $B$ 各换一组正交归一基后，仍能得到这种形式；它叫 **Schmidt 分解**。一般二分纯态可以写成

$$|\psi\rangle_{AB}=\sum_{j=1}^{r}\sqrt{\lambda_j}
|u_j\rangle_A|v_j\rangle_B,$$

其中 $\lambda_j>0$、$\sum_j\lambda_j=1$，同侧的 $|u_j\rangle$ 两两正交，$|v_j\rangle$ 也两两正交。每个 $\sqrt{\lambda_j}$ 是一个非负振幅，$\lambda_j$ 是其平方；$r$ 是非零项的个数，叫 **Schmidt 秩**。例如部分纠缠态有两项，其 $\lambda_1=3/4,\lambda_2=1/4$，不是把振幅 $\sqrt3/2,1/2$ 直接当作概率。

偏迹一遍就能看出这个分解为何有用。把 $|\psi\rangle\langle\psi|$ 展开时，索引 $j\ne k$ 的交叉项含 $|v_j\rangle\langle v_k|$；对 $B$ 偏迹会乘上 $\langle v_k|v_j\rangle=0$。只有 $j=k$ 留下，于是

$$\rho_A=\sum_{j=1}^{r}\lambda_j|u_j\rangle\langle u_j|.$$

也就是说，$\lambda_j$ 同时是 $\rho_A$ 和 $\rho_B$ 的非零本征值。由此可以检查：

- $r=1$ 当且仅当纯态可分；
- $r>1$ 表示纠缠；
- 两边约化态虽然维度可以不同，但非零本征值相同。

一般定理可由系数矩阵的奇异值分解证明；第一次阅读不要求掌握这个证明，先把上面的偏迹和两个具体态算熟即可。

### 用熵比较这两个纯态

一个常用的**二分纯态纠缠量**是任一边约化态的熵。它衡量这些 Schmidt 权重是否均匀，这里取以 2 为底的对数、单位为 bit：

$$S(\rho_A)=-\operatorname{Tr}(\rho_A\log_2\rho_A)
=-\sum_j\lambda_j\log_2\lambda_j.$$

Bell 态的 Schmidt 系数 $\sqrt{\lambda_j}$ 为 $1/\sqrt2,1/\sqrt2$，权重 $\lambda_j$ 为 $1/2,1/2$。代入得到 $S=-(1/2)(-1)-(1/2)(-1)=1$ bit。若是乘积纯态，只有一项 $\lambda_1=1$，约定 $\log_2 1=0$，故 $S=0$。

前面的部分纠缠态 $\sqrt3|00\rangle/2+|11\rangle/2$ 也已经写成 Schmidt 形式，只是两个权重改为 $3/4,1/4$。其纠缠熵为

$$
S=-\frac34\log_2\frac34-\frac14\log_2\frac14
\approx0.811\ \text{bit}.
$$

把 $\log_2(1/4)=-2$ 先代进去，第二项贡献 $1/2$；第一项约为 $0.311$，总和约 $0.811$。它大于零，说明该纯态纠缠；又小于 Bell 态的 1 bit，说明两项权重不均匀时纠缠量较低。**这个判法只适用于二分纯态。**第 6 节的经典混合态局部熵也有 1 bit，却完全可以不纠缠。

## 6. 经典关联和量子纠缠的区别

想象两种制备程序。程序一每次都制备同一个纯态 $|\Phi^+\rangle$；程序二抛一枚公平经典硬币，正面制备 $|00\rangle$，反面制备 $|11\rangle$，却不告诉观察者硬币结果。程序二的联合状态是两个乘积纯态的概率混合，因此叫**可分混态**：

$$
\rho_{\text{ent}}=|\Phi^+\rangle\langle\Phi^+|,
$$

$$
\rho_{\text{mix}}=\frac12|00\rangle\langle00|
+\frac12|11\rangle\langle11|.
$$

把两个矩阵摆在同一基序下，差异一眼可见：

$$
\rho_{\text{ent}}=\frac12
\begin{bmatrix}1&0&0&1\\0&0&0&0\\0&0&0&0\\1&0&0&1\end{bmatrix},
\qquad
\rho_{\text{mix}}=\frac12
\begin{bmatrix}1&0&0&0\\0&0&0&0\\0&0&0&0\\0&0&0&1\end{bmatrix}.
$$

二者在计算基都只产生 $00$ 或 $11$，各占一半，所以单看这一组测量数据无法区分。但换到 $X$ 基就可以。第 3 节已经算出纯态 $|\Phi^+\rangle=(|++\rangle+|--\rangle)/\sqrt2$，故它只给同号结果，各占一半。对混合态，必须分别计算“本轮是 $|00\rangle$”与“本轮是 $|11\rangle$”，再按硬币概率加权；不能先把两条 ket 相加。无论哪一种乘积态，每边测 $X$ 基都是 $+,-$ 各半，所以四种联合结果各 $1/4$。

| $X$ 基结果 | $\rho_{\text{ent}}$ | $\rho_{\text{mix}}$ |
|---|---:|---:|
| $++$ | $1/2$ | $1/4$ |
| $+-$ | $0$ | $1/4$ |
| $-+$ | $0$ | $1/4$ |
| $--$ | $1/2$ | $1/4$ |

计算差别来自 $\rho_{\text{ent}}$ 中的非对角相干项 $|00\rangle\langle11|$ 与其共轭项；它们让异号振幅相消，却不存在于经典硬币混合。两态分别对 $A$ 或 $B$ 做偏迹，都得到 $I/2$：只看一边的任何测量都区分不了它们，必须比较两边在至少一种合适基下的联合统计。

这里的“可分混态”比第 2 节的“可分纯态”范围更广：混态只要能写成若干乘积纯态密度矩阵的概率混合，就叫可分。$\rho_{\text{mix}}$ 通常**不能写成单个乘积态的密度矩阵**，但它仍不纠缠。反过来，“$X$ 基同号”这一项证据也不能单独证明纠缠：例如 $\tfrac12|++\rangle\langle++|+\tfrac12|--\rangle\langle--|$ 是可分混态，恰好也给出 $X$ 基同号；还需把 $Z$、$X$ 等多组数据放在一起，并考虑统计误差与测量模型。

**马上核对。** 这两个态在 $Z\otimes Z$ 上的期望值都是 1；在 $X\otimes X$ 上，纠缠态是 1，经典混合态是 0。用上表算后一项：$(1/4+1/4)-(1/4+1/4)=0$。

### 从两组计数得到一个可检验的纠缠判据

上面的比较还能变成一个具体的**纠缠见证**：只测两组局域基，就能在结果足够明显时排除所有可分态。把一批相同制备的双比特样本分为两组；一组让两边都测 $Z$，另一组都测 $X$。每组把同号结果记作 $+1$、异号记作 $-1$，于是

$$
\begin{aligned}
C_Z&=\langle Z\otimes Z\rangle
=P_Z(00)+P_Z(11)-P_Z(01)-P_Z(10),\\
C_X&=\langle X\otimes X\rangle
=P_X(++)+P_X(--)-P_X(+-)-P_X(-+).
\end{aligned}
$$

这里的 $P_Z$ 和 $P_X$ 来自**不同批次**；不能说单次实验同时读出了两组结果。为什么 $C_Z+C_X>1$ 就足以证明纠缠？对任何乘积态 $\rho_A\otimes\rho_B$，令 $x_A=\operatorname{Tr}(X\rho_A)$、$z_A=\operatorname{Tr}(Z\rho_A)$，另一边同理。第 02 章的 Bloch 球告诉我们 $x_A^2+z_A^2\le1$、$x_B^2+z_B^2\le1$。乘积态的相关值相乘分解，故由二维向量的 Cauchy–Schwarz 不等式，

$$
C_X+C_Z=x_Ax_B+z_Az_B
\le\sqrt{x_A^2+z_A^2}\sqrt{x_B^2+z_B^2}\le1.
$$

可分混态是这些乘积态按非负概率的混合；$C_X+C_Z$ 对混合按同样概率加权，所以仍不可能超过 1。因此

$$
\boxed{C_X+C_Z>1\quad\Longrightarrow\quad\text{双比特态纠缠}.}
$$

把前面两种态代入：$|\Phi^+\rangle$ 有 $(C_Z,C_X)=(1,1)$，总和为 2；经典混合态有 $(1,0)$，恰在可分上界 1。再考虑带白噪声的教学模型 $\rho_q=q|\Phi^+\rangle\langle\Phi^+|+(1-q)I/4$，其中 $0\le q\le1$ 是 Bell 态所占的概率。因为 $I/4$ 在两组测量中都没有相关性，$C_Z=C_X=q$；例如 $q=0.8$ 时，两组结果各给 0.8，总和 1.6，超过可分上界。此时每组同号概率合计为 $(1+0.8)/2=0.9$，异号合计为 0.1。若每组分别测 1000 对，$Z$ 组的 $00,11,01,10$ **期望次数**依次是 $450,450,50,50$；$X$ 组的 $++,--,+-,-+$ 也是这四个期望次数。由计数重算任一组的相关值是 $(450+450-50-50)/1000=0.8$。实际次数会波动，不能把期望次数写成实验保证。

这个判据是**充分条件而非必要条件**：若总和不超过 1，不能反推“不纠缠”。漏检不一定是因为关联落在别的轴上。例如 $|\Phi^-\rangle=(|00\rangle-|11\rangle)/\sqrt2$ 与 $|\Phi^+\rangle$ 同样在 $X,Z$ 两轴有强相关，但它的 $(C_Z,C_X)=(1,-1)$，直接相加为 0；只是这条见证的**符号取向**不合适。若事先改用 $|C_X|+|C_Z|>1$，它仍是充分条件：对每个乘积态，把上面的 Cauchy–Schwarz 证明中的两项分别取绝对值，右边仍不超过 1；对可分混态再用三角不等式即可。这样 $|\Phi^-\rangle$ 的两项绝对值之和为 2。即使绝对值版也不能检测所有纠缠态。真实计数还要给出采样误差和测量校准的不确定度，确认超过界限不是偶然波动或基设置错误。这种“测少量相关量来排除可分态”的方法属于纠缠见证，与下一节检验 Bell 局域隐藏变量模型的 CHSH 不等式不是同一个问题；[Audenaert 与 Plenio 的原始论文](https://arxiv.org/abs/quant-ph/0608067)专门讨论了由 $XX$、$ZZ$ 两组相关统计判断何时能确认纠缠。

## 7. Bell 不等式说明什么

前六节已经足以计算本章的常见量子线路。以下是**进阶回看**：Bell 不等式检验的是一类“相关性可由共享的局域信息解释”的模型，并不把任何单次测量结果当成证据。这个结论有明确的假设与数值上限。

在测量设置独立、远端结果满足 Bell 局域性等假设下，局域隐藏变量模型满足 Bell/CHSH 不等式。设小写 $a,b$ 分别是 Alice、Bob 选择的测量设置，大写 $A,B$ 是两人本轮记录到的结果，$\lambda$ 代表模型假定的共享信息。“测量设置独立”是指 $\lambda$ 的分布不随本轮设置改变；“Bell 局域性”可写成

$$
p(A,B\mid a,b,\lambda)
=p(A\mid a,\lambda)p(B\mid b,\lambda),
$$

即给定隐藏变量 $\lambda$ 后，Alice 的结果分布不依赖 Bob 的设置 $b$，反之亦然。这个结论也覆盖结果带随机性的局域模型，不需要把“每个结果早已写死”另列为基本假设。Bell/CHSH 实验不是“证明观察者意识创造现实”，也不是“允许超光速通信”。

接下来取 $A,B\in\{+1,-1\}$。$E(a,b)$ 是固定这一对设置、重复很多轮后的两端**乘积平均值**。同号时乘积 $+1$，异号时 $-1$，因此 $E=P(\text{同号})-P(\text{异号})$。例如同号占 $3/4$、异号占 $1/4$，相关值就是 $1/2$。我们不能从一次实验的一对结果估计它。让 $a,a'$ 表示 Alice 可选的两种设置，$b,b'$ 表示 Bob 的，标准 CHSH 表达式为

$$S=E(a,b)+E(a,b')+E(a',b)-E(a',b')$$

对上述 Bell 局域模型满足 $|S|\le2$；量子理论可达到 $2\sqrt2$，称 Tsirelson 界。实验检验需处理探测、局域性和测量设置独立性等漏洞。确定性结果可以作为局域随机模型的一种等价细化来使用，但不是 CHSH 结论额外要求自然界满足的前提。

这两个数可以在一个具体例子里逐项核对。先看局域模型：若给定隐藏变量后把两端结果写为 $a_0,a_1,b_0,b_1\in\{+1,-1\}$，则一次确定取值的 CHSH 组合是

$$
s=a_0b_0+a_0b_1+a_1b_0-a_1b_1
=a_0(b_0+b_1)+a_1(b_0-b_1).
$$

$b_0,b_1$ 若相同，第一个括号为 $\pm2$、第二个为 0；若相反，两个括号的角色互换。因此每次 $s=\pm2$，按任意经典概率分布取平均后都有 $|S|\le2$。允许局域结果本身带随机性，也可以把额外随机选择并入隐藏变量再取平均，不会提高这个界。

量子例子取 $|\Phi^+\rangle$，令 Alice 测量 $A_0=Z,A_1=X$，Bob 测量 $B_0=(Z+X)/\sqrt2,B_1=(Z-X)/\sqrt2$。这些 $B_j$ 也是只有 $\pm1$ 结果的合法二值可观测量，因为 $X^2=Z^2=I$ 且 $XZ+ZX=0$，所以 $B_j^2=I$。在 $|\Phi^+\rangle$ 上，$\langle Z\otimes Z\rangle=\langle X\otimes X\rangle=1$，而 $\langle Z\otimes X\rangle=\langle X\otimes Z\rangle=0$；例如 $Z\otimes X$ 把 $|00\rangle,|11\rangle$ 送到与原态正交的 $|01\rangle,|10\rangle$ 组合。展开 $E_{ij}=\langle\Phi^+|A_i\otimes B_j|\Phi^+\rangle$：

| 设置 $(i,j)$ | 相关值 $E_{ij}$ | 代入 $S$ 的符号 |
|---|---:|---:|
| $(0,0)$ | $+1/\sqrt2$ | $+$ |
| $(0,1)$ | $+1/\sqrt2$ | $+$ |
| $(1,0)$ | $+1/\sqrt2$ | $+$ |
| $(1,1)$ | $-1/\sqrt2$ | $-$ |

把表中的四项按上面的 CHSH 公式依次取 $+,+,+,-$，得到

$$
\begin{aligned}
S&=\frac1{\sqrt2}+\frac1{\sqrt2}+\frac1{\sqrt2}\\
 &\quad-\left(-\frac1{\sqrt2}\right)\\
 &=\frac4{\sqrt2}=2\sqrt2.
\end{aligned}
$$

这里的正负号是四种测量设置的相关统计，不是一次实验同时读出四个不兼容的量；实验需要多轮制备，并按设置分组估计各个 $E_{ij}$。

上面的例子只说明 $2\sqrt2$ **能够达到**；“界”还要求任何合规量子策略都不能更高。以下是可在学完矩阵范数后再读的核对。设两方分别进行二值投影测量，所得 $\pm1$ 可观测算符记作 $A_0,A_1$ 与 $B_0,B_1$。例如某次测量的两个投影为 $P_+,P_-$，那么对应可观测算符是 $A=P_+-P_-$；由于 $P_+P_-=0$ 且 $P_++P_-=I$，有 $A^2=I$。**平方等于 $I$ 的是这个 $\pm1$ 算符，不是单个投影 $P_\pm$**，后者满足的是 $P_\pm^2=P_\pm$。不同方的算符作用在不同系统上，因而可交换。把 CHSH 组合写成

$$
\mathcal B=A_0\otimes(B_0+B_1)+A_1\otimes(B_0-B_1).
$$

展开平方时，$(B_0+B_1)(B_0-B_1)=-[B_0,B_1]$，两项平方之和为 $4I$，于是

$$
\mathcal B^2=4I-[A_0,A_1]\otimes[B_0,B_1].
$$

算符范数 $\|M\|$ 表示 $M$ 对单位向量可能造成的最大长度变化。这里 $\|A_i\|=\|B_j\|=1$，由三角不等式与 $\|MN\|\le\|M\|\|N\|$ 可得每个交换子的范数至多为 2；因此 $\|\mathcal B^2\|\le4+2\times2=8$。由于 $\mathcal B$ 是厄米算符，任意单位态上都有 $|\langle\mathcal B\rangle|\le\|\mathcal B\|=\sqrt{\|\mathcal B^2\|}\le2\sqrt2$。前面的 Bell 态例子恰好取到等号。这个推导证明了二值投影测量情形的量子上界；一般二值测量可扩充系统后用投影测量表示，界不会提高。

## 8. 单配性（进阶回看）

这一节只讨论一个容易核对的特殊情形，不把“纠缠不能分享”当成没有条件的口号。若 $A,B$ 的联合态已经是 Bell 纯态 $|\Phi^+\rangle_{AB}$，则包含第三系统 $C$ 的任意联合态只能写成

$$
\rho_{ABC}=|\Phi^+\rangle\langle\Phi^+|_{AB}\otimes\rho_C.
$$

理由是：$AB$ 的约化态在 $|\Phi^+\rangle$ 以外的方向上概率为零；合法密度矩阵是正半定的，因此完整联合态不可能在这些方向留下分量或与它们的交叉项。于是 $C$ 既不能与 $AB$ 纠缠，也不能与其有经典相关。若三方总态是纯态，也可从 Schmidt 分解看出：$AB$ 的约化态只有一个非零本征值，$AB|C$ 分解便只有一项。

这不表示“只要有一点纠缠，就与第三方完全无关”。例如三比特态 $(|000\rangle+|111\rangle)/\sqrt2$ 中，$AB$ 的约化态是 $\tfrac12|00\rangle\langle00|+\tfrac12|11\rangle\langle11|$：$A,B$ 有经典相关，三方整体仍是纠缠纯态，但 $AB$ 不是 Bell 纯态。一般情形中“纠缠能分给多少方”需要选定纠缠量后写出相应的不等式；三比特的一个定量版本见 [Coffman、Kundu 与 Wootters 的原始论文](https://doi.org/10.1103/PhysRevA.61.052306)。单配性有助于理解量子密钥分发为何可检测某些窃听行为，但实际安全结论还需要写清协议、设备和攻击模型。

## 9. 常见误区

- 相关性不等于纠缠；经典共享随机数也能产生完美相关。
- 两个量子比特处于同一个实验装置，不意味着它们必然纠缠。
- 纠缠不是一种可独立储存在单个粒子里的属性，而是联合态的性质。
- 对混态，不能只用“能否写成一个乘积”判断；可分混态是乘积态的概率混合。
- 纠缠多不等于任何算法都更快；还需匹配任务与可利用的测量结构。

## 10. 自检

1. 用 $ad-bc$ 判断 $(|00\rangle+|10\rangle)/\sqrt2$ 是否纠缠，并给出分解。
2. 求 $|\Psi^-\rangle$ 的任一单比特约化态。
3. 为什么只在计算基测量，无法区分 $\rho_{\text{ent}}$ 与 $\rho_{\text{mix}}$？
4. “Alice 一测量，Bob 立即知道她的结果”错在哪里？
5. 按本章的基顺序，把 $|+\rangle_A|1\rangle_B$ 写成四维列向量；列出计算基测量的四个概率。
6. 判断 $(|00\rangle+|01\rangle+|10\rangle+|11\rangle)/2$ 是否纠缠。不要只凭“有四项”猜测。
7. 在 $X$ 基测两边：分别列出 $|\Phi^+\rangle$ 与 $\rho_{\text{mix}}$ 的 $++,+-,-+,--$ 概率，并核对每组和为 1。
8. 对 $|\psi\rangle=(\sqrt3|00\rangle+|11\rangle)/2$，把 $\rho_A$ 的四格都从 $\rho_{AB}$ 的对应两格相加算出来。
9. 对第 8 题的态，在 $A$ 的计算基测量：写出两个结果概率、各自的条件联合后态，以及丢弃记录后的联合态。
10. 若 $|\Phi^-\rangle=(|00\rangle-|11\rangle)/\sqrt2$，两边在 $X$ 基测量，哪些联合结果有可能出现？各是多少概率？
11. 为什么 $\rho_{\text{mix}}$ 的单比特约化态也有 1 bit 熵，却不能据此断言联合态有 1 bit 纠缠？

答案见[练习与答案：第 3 章](appendices/exercises.md#第-3-章)。

## 配套数值实验与展开答案

对含复相位的非最大纠缠态逐格偏迹，再施加远端局域旋转，确认本地约化态不变。明确比较完整矩阵，而不只比较一个计算基概率。

题目和逐步解答见[基础实验册](labs/foundations.md)，本章程序编号为 `03`。可从[代码说明](../codes/foundations/README.md)进入独立脚本与保存的运行结果。所有模拟样本均明确标作合成数据，不是硬件实验。

## 参考起点

- John Watrous, [Quantum information: multiple systems](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/quantum-information)：联合基序、张量积与局部测量。
- John Watrous, [Multiple systems and reduced states](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/multiple-systems)：偏迹和约化态的定义与例子。
- John Watrous, [*The Theory of Quantum Information*, §1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)：Schmidt 分解的数学证明。
- John Watrous, [Entanglement in action](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/introduction)：明确比较纠缠与经典共享随机性。
- J. S. Bell, [On the Einstein Podolsky Rosen paradox](https://cds.cern.ch/record/111654/files/vol1p195-200_001.pdf), *Physics Physique Физика* 1, 195–200 (1964)。
- J. F. Clauser, M. A. Horne, A. Shimony and R. A. Holt, [Proposed experiment to test local hidden-variable theories](https://doi.org/10.1103/PhysRevLett.23.880), *Physical Review Letters* 23, 880–884 (1969)：CHSH 不等式的原始论文。
- B. S. Cirel'son, [Quantum generalizations of Bell's inequality](https://doi.org/10.1007/BF00417500), *Letters in Mathematical Physics* 4, 93–100 (1980)：量子上界的原始论文。
