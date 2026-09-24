# 第六轮扩展研究：高级理论、算法与计算例题缺口审计

日期：2026-09-22  
角色：高级理论、算法与计算例题审稿人  
审读范围：`handbook/00`—`12`、附录与两级 README；重点复核 `03`、`05`、`06`、`07`、`08`、`10`、`11`。  
本轮边界：只做缺口审计与补写设计，不修改正文。

## 1. 结论先行

现有教材已经有一条可靠的入门主线：线性代数—电路—oracle—QFT/QPE—Simon/Grover/Shor—量子模拟—变分算法—纠错—资源估算。抽查并复算 Simon 三比特例、Grover 二维旋转、Shor 的 $N=15$ 例、$H=X+Z$ 的 BCH 符号、单边 MaxCut 的 $p=1$ QAOA 公式和 VQE 一比特例后，没有发现需要立即改正的主公式错误。

但若目标同时是“初学者可读”和“入门研究生可继续做研究”，目前还有四类结构性缺口：

1. **量子信息的操作性量度缺失。** 现有正文有密度矩阵、纯度、纠缠熵和若干保真度名词，却没有把迹距离、保真度、相对熵、互信息、Holevo 信息与“能否区分、能读出多少、信道会怎样改变信息”连起来。
2. **算法优势只给结论，缺少证明工具。** Grover 的最优性、Simon 的查询优势、promise problem 与 total function 的差别都说到了，但没有 polynomial/adversary/hybrid 等下界框架，学生无法判断新算法宣称是否可信。
3. **现代算法栈停留在名词列表。** LCU、块编码、qubitization、QSP/QSVT、量子行走、hidden subgroup 仅被一句带过或完全缺席，尚未形成“输入模型—归一化—多项式逼近—查询复杂度—读出”的链条。
4. **验证与资源估算没有完全闭环。** 已有端到端资源图和基准清单很强，但还缺算法精度预算、任意旋转综合的 T 成本、tomography/shadows 的可测性边界，以及不同输出类型对应的验证协议。

建议不要把下列内容全部塞入第 07 章。更自然的分工是：

| 主题 | 建议落点 | 理由 |
|---|---|---|
| 状态距离、熵、Holevo、数据处理 | 第 05 章新增“信息量度”节 | 与密度矩阵、信道紧邻 |
| 查询模型与下界 | 第 06 章末新增一节 | 为第 07 章“加速”提供判准 |
| AE、HSP、量子行走、LCU/QSP | 第 07 章扩写 | 属算法主干 |
| QML 的访问模型与反量子化 | 第 08 章扩写 | 与应用证据边界直接相连 |
| tomography、shadows、任务特定验证 | 第 08 或第 11 章新增一节 | 把“得到答案”与“相信答案”分开 |
| 精度预算、门综合、oracle 展开 | 第 11 章扩写 | 把渐近复杂度落到容错资源 |

优先级定义：

- **A：应进入主线。** 缺失会让读者对“量子信息”“加速”或“可验证”形成不完整甚至误导性的心智模型。
- **B：应进入研究生入口。** 不影响最基础的电路学习，但决定能否读现代算法论文。
- **C：可放专题框或附录。** 用于建立边界感，不宜挤压主线。

下文共列出 **32 项**具体补写任务，其中 A 级 16 项、B 级 12 项、C 级 4 项。

---

## 2. A 级：应进入主线的缺口

### A1. 用“最优区分概率”引入迹距离，而不是只把保真度当实验分数

**当前缺口**  
第 05 章列出状态保真度、平均门保真度和金刚石范数，却没有定义状态迹距离，也没有说明这些量为何与实验决策有关。读者容易把“99% fidelity”误认为任何任务都有 99% 成功率。

**建议补写段落**  
定义

$$
D(\rho,\sigma)=\frac12\|\rho-\sigma\|_1.
$$

当两个状态先验概率各为 $1/2$ 时，最优单次判别成功率为

$$
p_{\rm guess}=\frac12\bigl(1+D(\rho,\sigma)\bigr).
$$

再固定全书保真度约定。建议用平方保真度

$$
F(\rho,\sigma)=\left\|\sqrt\rho\sqrt\sigma\right\|_1^2,
$$

并明确有些资料把其平方根叫 fidelity。给出 Fuchs–van de Graaf 关系

$$
1-\sqrt{F}\le D\le\sqrt{1-F}.
$$

**可复算例**  
比较 $|0\rangle$ 与 $|+\rangle$：

$$
F=|\langle0|+\rangle|^2=\frac12,qquad
D=\sqrt{1-F}=\frac1{\sqrt2}.
$$

故最优成功率为

$$
p_{\rm guess}=\frac12\left(1+\frac1{\sqrt2}\right)\approx0.8536,
$$

不是 $1-F=50\%$，也不是 $F=50\%$。这个例子能一次澄清“重叠、距离、错误率”三种数不能互换。

**图表**  
做一张“量度—操作任务—取值范围—是否对信道单调”的四列表。

**依据**  
Watrous, *The Theory of Quantum Information*, Chapter 3：<https://cs.uwaterloo.ca/~watrous/TQI/>。

### A2. 补齐 von Neumann 熵、条件熵与互信息的最小闭环

**当前缺口**  
第 03 章只在纯态 Schmidt 分解中使用 $S(\rho_A)$。尚未说明混态熵、联合熵、条件熵和互信息，因此“经典关联”和“量子关联”的差别仍主要靠测量例子表达。

**建议补写段落**

$$
S(A)=-\operatorname{Tr}(\rho_A\log_2\rho_A),
$$

$$
S(A|B)=S(AB)-S(B),qquad
I(A:B)=S(A)+S(B)-S(AB).
$$

强调量子条件熵可以为负，而互信息仍非负。负条件熵不是“负的不确定性”，而是纠缠可作为通信/合并资源的信号。

**可复算例**

- Bell 态：$S(A)=S(B)=1,S(AB)=0$，故 $I(A:B)=2$ bit，$S(A|B)=-1$ bit。
- 经典混合态 $\frac12(|00\rangle\langle00|+|11\rangle\langle11|)$：三个熵都是 $1,1,1$，故 $I=1$ bit，$S(A|B)=0$。

两者计算基统计相同，但总关联量不同。这个算例应紧接第 03 章现有 Bell 态/经典混合态对照。

**依据**  
Watrous, Chapters 5–6；其公开课程目录也把 entropy、relative entropy、strong subadditivity 分为连续单元：<https://cs.uwaterloo.ca/~watrous/TQI-notes/>。

### A3. 加入量子相对熵与数据处理不等式，建立“处理不会凭空增加可区分性”

**当前缺口**  
正文多次说噪声和丢弃信息会让任务更难，但没有一个统一的不等式支持这个直觉。

**建议补写段落**

$$
D(\rho\|\sigma)=\operatorname{Tr}\rho(\log\rho-\log\sigma),
$$

在 $\operatorname{supp}\rho\nsubseteq\operatorname{supp}\sigma$ 时取 $+\infty$。对任意 CPTP 信道 $\mathcal E$，

$$
D(\mathcal E(\rho)\|\mathcal E(\sigma))
\le D(\rho\|\sigma).
$$

同时指出迹距离也满足收缩性 $D(\mathcal E(\rho),\mathcal E(\sigma))\le D(\rho,\sigma)$。这能统一解释：测量、退相干和丢弃子系统都不能增强任意两态的最优可区分性。

**可复算例**  
对角态等价于经典分布 $p=(3/4,1/4)$、$q=(1/2,1/2)$：

$$
D(p\|q)=\frac34\log_2\frac32+rac14\log_2\frac12\approx0.1887\ \text{bit}.
$$

把两个结果都粗粒化成同一标签后，两分布都变为 $(1)$，相对熵降为 0。

**依据**  
M. B. Ruskai, “Inequalities for Quantum Entropy,” <https://arxiv.org/abs/quant-ph/0205064>；Watrous, Chapter 5。

### A4. 用 Holevo 信息解释“$n$ 个量子比特不等于可读出 $2^n$ 个经典数”

**当前缺口**  
第 01、03、06、07 章都正确提醒“指数振幅不等于指数输出”，但缺少正式上界。

**建议补写段落**  
对经典—量子系综 $\{p_x,\rho_x\}$，定义

$$
\chi=S\!\left(\sum_xp_x\rho_x\right)-\sum_xp_xS(\rho_x).
$$

任何测量得到的经典互信息满足 $I(X:Y)\le\chi$。说明 Holevo 界约束的是从一次量子编码中可访问的经典信息，不否定叠加可用于干涉提取特定全局性质。

**可复算例**  
等概率编码 $|0\rangle,|+\rangle$。两输入都是纯态，故

$$
\bar\rho=\frac12(|0\rangle\langle0|+|+\rangle\langle+|)
=\begin{pmatrix}3/4&1/4\\1/4&1/4\end{pmatrix}.
$$

其本征值为 $(1\pm1/\sqrt2)/2$，所以

$$
\chi=h_2\!\left(\frac{1+1/\sqrt2}{2}\right)\approx0.6009\ \text{bit}.
$$

这比“一个 qubit 最多一个 bit”更细：非正交编码甚至达不到一整 bit。

**依据**  
Watrous 的 Holevo theorem 课程单元：<https://cs.uwaterloo.ca/~watrous/TQI-notes/>。

### A5. 正式定义查询模型，并把 bit oracle、phase oracle 与真实门成本分开

**当前缺口**  
第 06 章已区分查询复杂度和端到端成本，但还没有统一写出 oracle 模型。Simon、DJ、BV、Grover 的“调用一次”因此仍可能被理解为普通常数时间函数调用。

**建议补写段落**

$$
O_f|x,y\rangle=|x,y\oplus f(x)\rangle,
$$

布尔函数的相位 oracle 为

$$
S_f|x\rangle=(-1)^{f(x)}|x\rangle.
$$

用目标位 $| -\rangle$ 可由一次 $O_f$ 得到 $S_f$。反方向则需要写清辅助位和允许的受控调用。随后明确：查询复杂度把 oracle 视为单位成本；把谓词展开为可逆门、加载数据、清垃圾位后，门复杂度可能完全不同。

**可复算例**  
让 $f(x)$ 是一个 128 位数据库记录是否满足复杂约束。对 Grover 而言是“一次查询”；对工程资源而言应列出比较器、算术、QRAM/数据生成和反计算的门数。

**图表**  
画三层成本图：抽象查询 $\to$ 可逆 oracle 电路 $\to$ 逻辑/物理资源。

**依据**  
Beals et al., “Quantum Lower Bounds by Polynomials,” <https://arxiv.org/abs/quant-ph/9802049>；Watrous 量子查询课程：<https://jhwatrous.github.io/books-and-courses.html>。

### A6. 增加 polynomial method：至少让读者看懂“一次查询为何只能产生二次接受概率”

**当前缺口**  
正文写了 Grover 在黑箱模型中最优，却没有任何下界证明机制。读者无法区分“尚未找到更快算法”和“已证明不能更快”。

**建议补写段落**  
对输入位 $z_1,\ldots,z_N$ 的标准查询算法，做 $T$ 次查询后，每个振幅可表示为次数至多 $T$ 的多项式；接受概率是振幅模平方之和，因此次数至多 $2T$。若一个 Boolean 函数的任何近似多项式都必须有次数 $d$，则 $T\ge d/2$。

**可复算例**  
Deutsch 的两个 oracle 位 $z_0=f(0),z_1=f(1)$。算法输出“不同”的概率是

$$
z_0\oplus z_1=z_0+z_1-2z_0z_1,
$$

这是次数 2 的多项式，与一次量子查询的 $2T=2$ 完全一致。随后说明 OR 的近似次数为 $\Theta(\sqrt N)$，故 Grover 的 $\Theta(\sqrt N)$ 查询渐近最优。

**依据**  
Beals et al., <https://arxiv.org/abs/quant-ph/9802049>。

### A7. 给 Grover 最优性一个可视化 hybrid/adversary 证明骨架

**当前缺口**  
仅引用“渐近最优”不足以形成直觉。

**建议补写段落**  
比较“没有标记项”的 oracle 与“第 $j$ 项被标记”的 $N$ 个 oracle。一次查询只能按算法当前在 $j$ 上的振幅改变状态；对 $j$ 求平均，该振幅量级至多 $1/\sqrt N$。经过 $T$ 次，平均可区分距离至多为 $O(T/\sqrt N)$。要把正确目标与无目标情形以常数偏差区分，必须 $T=\Omega(\sqrt N)$。

这只是证明路线，不必在主线给完所有范数细节；可在边栏说明一般 adversary bound 实际刻画量子查询复杂度。

**图表**  
画“$N+1$ 条最终态轨迹”：每次查询只允许总平均距离增长 $O(1/\sqrt N)$。

**依据**  
Bennett et al., “Strengths and Weaknesses of Quantum Computing,” <https://doi.org/10.1137/S0097539796300933>；Lee et al., general adversary/state conversion, <https://arxiv.org/abs/1011.3020>。

### A8. 明确 promise/partial function 是指数查询优势的关键边界

**当前缺口**  
第 07 章已说 Simon 是承诺黑箱问题，但还缺统一总结。初学者容易从 DJ/Simon 推出“量子对普通 Boolean 函数也常有指数查询优势”。

**建议补写段落**  
区分：

- total function：每个 $\{0,1\}^N$ 输入都合法；
- partial/promise function：只要求在一个承诺子集上正确。

Beals 等工作说明对 total Boolean functions，确定性经典查询复杂度与有界错误量子查询复杂度之间至多是多项式关系；DJ、Simon 一类指数分离依赖 promise。不要把这个结论扩张到所有计算模型：Shor 的时间复杂度优势不是简单的 total Boolean query statement。

**图表**  
表格对比 DJ、Simon、Grover、Shor 的输入模型、承诺、量子查询、经典查询、端到端时间。

**依据**  
Beals et al., <https://arxiv.org/abs/quant-ph/9802049>。

### A9. 把幅度估计从一段复杂度结论扩成完整二维旋转推导

**当前缺口**  
第 07 章只给 $O(1/\epsilon)$ 与 $O(1/\epsilon^2)$，没有解释为什么 QPE 能估计概率。

**建议补写段落**  
设

$$
A|0\rangle=\sin\theta|G\rangle+\cos\theta|B\rangle,
\qquad a=\sin^2\theta.
$$

定义两个反射组成的 Grover 算符 $Q$。在 $\operatorname{span}\{|G\rangle,|B\rangle\}$ 中，$Q$ 的本征值为 $e^{\pm2i\theta}$。对 $Q$ 做相位估计得到 $\tilde\theta$，再输出 $\tilde a=\sin^2\tilde\theta$。

必须给出误差定理，而不仅是大 $O$：经典 BHMT 版本使用参数 $M$ 时，以至少 $8/\pi^2$ 的概率满足

$$
|\tilde a-a|
\le \frac{2\pi\sqrt{a(1-a)}}{M}+\frac{\pi^2}{M^2}.
$$

**可复算例**  
若 $a=1/2$，则 $\theta=\pi/4$，$Q$ 的归一化相位为 $1/4$ 与 $3/4$。两位精确 QPE 可读出 `01` 或 `11`；二者都映回 $\sin^2(\pi/4)=1/2$。这还能解释为何两个相位分支给同一概率。

**依据**  
Brassard et al., “Quantum Amplitude Amplification and Estimation,” <https://arxiv.org/abs/quant-ph/0005055>。

### A10. 幅度估计必须比较总查询、最大相干深度和总 shots

**当前缺口**  
正文虽提醒无 QFT 变体可能增加常数，但没有足够的比较维度，容易出现“没有 QPE 所以仍保留全部二次优势且适合 NISQ”的误读。

**建议补写表**

| 方法 | 是否需受控 $Q$ | 最大 $Q$ 幂/相干深度 | 总查询标度 | 经典拟合 | 主要风险 |
|---|---|---:|---:|---|---|
| QPE 型 AE | 是 | $O(1/\epsilon)$ | $O(1/\epsilon)$ | 轻 | 深线路、受控反射 |
| 迭代 AE | 通常不需 QFT | 随轮次增大 | 近 $O(1/\epsilon)$ | 置信区间更新 | 多轮、常数和噪声 |
| 最大似然 AE | 可不用 QPE | 由 Grover 幂表决定 | 设计相关 | MLE | 偏差、模型失配、覆盖不足 |
| 直接采样 | 否 | 1 | $O(1/\epsilon^2)$ | 均值/区间 | 查询多但线路浅 |

**应加入的边界**  
若硬件限制最大 Grover 幂为常数，或者噪声使深线路信息快速衰减，渐近二次精度优势可能不能实现。任何金融/风险应用都要把状态制备和 payoff oracle 的调用计入每个 $Q$。

**依据**  
Grinko et al., iterative QAE, <https://arxiv.org/abs/1912.05559>；Suzuki et al., MLE AE, <https://arxiv.org/abs/1904.10246>。

### A11. 量子模拟先定义输入模型，再谈复杂度；加入 no-fast-forwarding

**当前缺口**  
第 07 章正确说复杂度依赖局域性、稀疏性、范数和 oracle，但没有定义这些模型，也没有解释为什么不能一般地把时间 $t$ 压成 $\operatorname{polylog}t$。

**建议补写段落**  
至少对比：

- $k$-local：$H=\sum_jH_j$，每项只作用于常数个量子比特；
- $d$-sparse oracle：给定行和序号，可查询非零元素位置和值；
- Pauli/LCU：$H=\sum_j\alpha_jU_j$；
- block encoding：通过更大酉矩阵的左上块访问 $H/\alpha$。

定义无量纲演化规模，例如稀疏模型中的 $\tau=d\|H\|_{\max}t$。说明一般黑箱 Hamiltonian 存在 no-fast-forwarding 下界：查询复杂度不能普遍次线性于演化时间尺度。特殊可对角化、可快速幂或可积结构可以例外，必须把结构写出。

**依据**  
Berry et al., “Efficient quantum algorithms for simulating sparse Hamiltonians,” <https://arxiv.org/abs/quant-ph/0508139>；Berry, Childs, Kothari, <https://arxiv.org/abs/1501.01715>。

### A12. 把 Trotter 误差从 $O(t^2/r)$ 变成可计算的交换子界与数值例

**当前缺口**  
$H=X+Z$ 的 BCH 推导正确，但只有量级，没有把目标误差反推步数。

**建议补写段落**  
对 Hermitian $A,B$ 的一阶公式，可给出简化范数界

$$
\left\|e^{-i(A+B)t}-
\left(e^{-iAt/r}e^{-iBt/r}\right)^r\right\|
\le \frac{t^2}{2r}\|[A,B]\|,
$$

并说明更一般多项、时变和高阶公式有不同常数与嵌套交换子。

**可复算例**  
$A=X,B=Z$ 时 $[X,Z]=-2iY$，故 $\|[X,Z]\|=2$。取 $t=0.2,r=4$，上界为

$$
\frac{0.2^2}{2\times4}\times2=0.01.
$$

若目标算法误差预算只有 $10^{-3}$，这个界说明 $r=4$ 不够；至少需要把该项压到相应预算以内。再列二阶对称公式

$$
e^{-iA\Delta/2}e^{-iB\Delta}e^{-iA\Delta/2}

$$

的全局误差阶为 $O(t^3/r^2)$，但门数和交换子常数也要比较。

**依据**  
Lloyd, universal simulation（现有参考）；Berry et al., <https://arxiv.org/abs/1412.4687>。

### A13. 用 PREPARE/SELECT 的二行推导真正讲清 LCU

**当前缺口**  
LCU 目前只出现在“现代方法包括……”的列表中。没有这一步，块编码和 QSP 无法自然接上。

**建议补写段落**  
若

$$
H=\sum_{\ell=0}^{L-1}\alpha_\ell U_\ell,qquad
\alpha_\ell\ge0,qquad
\lambda=\sum_\ell\alpha_\ell,
$$

构造

$$
\operatorname{PREPARE}|0\rangle
=\sum_\ell\sqrt{\alpha_\ell/\lambda}|\ell\rangle,
$$

$$
\operatorname{SELECT}=\sum_\ell|\ell\rangle\langle\ell|\otimes U_\ell.
$$

则

$$
W=(\operatorname{PREPARE}^\dagger\otimes I)
\operatorname{SELECT}
(\operatorname{PREPARE}\otimes I)
$$

满足

$$
(\langle0|\otimes I)W(|0\rangle\otimes I)=H/\lambda.
$$

负系数或复系数可吸收到 $U_\ell$ 的相位中。

**可复算例**  
$H=0.6X+0.8Z$，$\lambda=1.4$，

$$
\operatorname{PREPARE}|0\rangle
=\sqrt{3/7}|0\rangle+\sqrt{4/7}|1\rangle,
$$

`SELECT` 在辅助位 0/1 时分别施加 $X/Z$。逐项夹取辅助位 $|0\rangle$ 后即得 $(0.6X+0.8Z)/1.4$。

**图表**  
一个三块线路图：PREPARE—SELECT—PREPARE$^\dagger$，并用颜色标出“成功左上块”。

**依据**  
Berry et al., truncated Taylor/LCU, <https://arxiv.org/abs/1412.4687>。

### A14. 定义块编码的归一化误差，防止把 $\alpha$ 当无关常数

**当前缺口**  
“块编码”没有定义；读者看现代论文时最容易漏掉 normalization factor，继而误读复杂度。

**建议补写段落**  
称酉矩阵 $U$ 是 $A$ 的 $(\alpha,a,\epsilon)$ 块编码，若

$$
\left\|A-alpha
(\langle0^a|\otimes I)U(|0^a\rangle\otimes I)
\right\|\le\epsilon.
$$

强调三项都影响算法：辅助位 $a$、误差 $\epsilon$、归一化 $\alpha\ge\|A\|$。很多算法复杂度依赖 $\alpha t$ 或 $\alpha\kappa$，不能只写矩阵维数。

**可复算例**  
上一个 LCU 例中

$$
H=\begin{pmatrix}0.8&0.6\\0.6&-0.8\end{pmatrix},
\qquad \|H\|=1,
$$

但直接 LCU 给出的归一化是 $\alpha=1.4$。这说明 $\alpha$ 取决于表示和访问方法，不总等于谱范数；更好的分解可以直接改善复杂度。

**依据**  
Gilyén et al., QSVT, <https://arxiv.org/abs/1806.01838>。

### A15. 建立“块编码 → qubitization → QSP/QSVT → 矩阵函数”的概念梯子

**当前缺口**  
第 07 章将五个现代术语并排列出，读者无法知道它们的依赖关系。

**建议补写段落**  
对 Hermitian $A$ 的块编码，qubitization 构造一个 walk operator，使 $A$ 的本征值 $\lambda$ 映到相位 $\theta$，典型关系为

$$
\cos\theta=\lambda/\alpha.
$$

QSP 通过交替固定信号酉和单量子比特相位旋转，实现满足奇偶性与有界性条件的低次多项式 $P(x)$；QSVT 将它提升为对块编码矩阵奇异值的多项式变换。算法设计因此变成：

$$
\text{目标函数 }f
\to\text{有界多项式近似 }P
\to P(A/\alpha)
\to\text{测量/后选择}.
$$

Hamiltonian 模拟对应逼近 $e^{-i\alpha tx}$，线性系统对应在避开零点的区间逼近 $1/x$，投影/符号函数对应逼近 $\operatorname{sgn}(x)$。

**可复算例**  
取 $A=\operatorname{diag}(1,0)$、$\alpha=1$ 和

$$
P(x)=T_2(x)=2x^2-1.
$$

则

$$
P(A)=\operatorname{diag}(1,-1).
$$

学生可逐本征值计算，理解“矩阵多项式”不是对每个矩阵元做多项式。边栏必须提醒：并非任意多项式都能无条件直接实现；次数、奇偶性、区间有界性和近似误差决定查询数。

**图表**  
建议画一张纵向“现代算法编译栈”，而不是五个互不相连的术语框。

**依据**  
Low and Chuang, qubitization, <https://quantum-journal.org/papers/q-2019-07-12-163/>；Gilyén et al., <https://arxiv.org/abs/1806.01838>。

### A16. 把算法验证升级为“按输出类型选择证据”，并纳入算法总成本

**当前缺口**  
第 06、08、11 章都提到验证，但目前主要是清单式提醒，尚未形成方法树。尤其容易把“和同一模拟器吻合”当作独立验证。

**建议补写表**

| 输出类型 | 首选验证 | 不能证明什么 |
|---|---|---|
| 因子、路径、可行解 | 经典直接验算 | 设备对难验证任务也正确 |
| 标量期望值 | 小规模精确解、守恒量、误差条、独立方法交叉检查 | 全态正确 |
| 已知目标态 | 稳定子测试、直接保真度估计、纠缠见证 | 未测方向完全正确 |
| 未知多体态 | 局域观测、随机测量/经典阴影、受限层析 | 完整密度矩阵已知 |
| 随机采样 | 小规模精确概率、统计检验、交叉熵等任务特定指标 | 大规模分布的无条件正确性 |
| 委托量子计算 | traps、交互/密码学验证协议 | 在无假设、零额外资源下验证 |

**可复算例：能量如何给保真度下界**  
若已知 Hamiltonian 基态能量 $E_0$、第一激发能隙 $\Delta$，且制备态能量为 $E$，则

$$
E\ge E_0+(1-F_0)\Delta
\quad\Rightarrow\quad
F_0\ge1-\frac{E-E_0}{\Delta}.
$$

例如 $E-E_0\le0.10,\Delta=0.40$，可推出基态占据至少 $0.75$。若不知道能隙，这个保真度保证就不能成立。

**依据**  
Gheorghiu, Kapourniotis, Kashefi, verification review, <https://arxiv.org/abs/1709.06984>；Flammia and Liu, direct fidelity estimation, <https://arxiv.org/abs/1104.4695>；Pallister et al., local state verification, <https://arxiv.org/abs/1709.03353>。

---

## 3. B 级：研究生入口应补的内容

### B1. 用隐藏子群问题统一 Simon 与 Shor，而不是把二者写成孤立算法

**当前缺口**  
Simon 与 Shor 已分别讲清，但共同的“余集态—Fourier sampling—找 annihilator/周期”结构没有显式出现。

**建议补写段落**  
给定群 $G$ 和函数 $f:G\to S$，承诺 $f$ 在隐藏子群 $H$ 的左陪集上常值，不同陪集取不同值。一次查询并忽略输出寄存器后得到随机陪集态

$$
|gH\rangle=\frac1{\sqrt{|H|}}\sum_{h\in H}|gh\rangle.
$$

Abelian 情形做群 Fourier 变换会采样到在 $H$ 上取 1 的角色，即 $H^\perp$。Simon 对应 $G=\mathbb Z_2^n,H=\{0,s\}$；周期寻找对应循环群上的隐藏周期（有限寄存器实现需处理近似峰）。

**可复算例**  
$s=101$ 时条件为 $z\cdot s=z_1\oplus z_3=0$，允许输出

$$
000,010,101,111.
$$

把它解释为 $H^\perp$，再和第 07 章 Simon 方程对应。

**重要边界**  
一般非 Abelian HSP 即使查询复杂度是 $\operatorname{poly}(\log|G|)$，经典后处理/量子测量也可能需要指数时间；“查询少”不等于“高效算法”。

**依据**  
Ettinger, Høyer, Knill, <https://arxiv.org/abs/quant-ph/0401083>；早期状态正交结果 <https://arxiv.org/abs/quant-ph/9901034>。

### B2. 增加量子行走的最小教学单元与 element distinctness 案例

**当前缺口**  
量子行走完全缺席，导致读者看不到 Grover 以外的通用搜索框架。

**建议补写段落**  
区分离散时间 coined walk、连续时间 walk 与基于可逆 Markov 链的 Szegedy/MNRS 搜索。先用 coined walk 说明位置寄存器与 coin 寄存器如何产生路径干涉，再解释算法复杂度为何依赖平稳分布中的 marked fraction、谱隙和更新/检查成本。

**可复算例：四环一步一步走**  
在四个顶点的环上，以 $|v,R/L\rangle$ 表示方向。取初态 $|0,R\rangle$，每步先对 coin 做 $H$ 再条件平移：

$$
|0,R\rangle\to
\frac{|1,R\rangle+|3,L\rangle}{\sqrt2}.
$$

第二步为

$$
\frac12\bigl(
|2,R\rangle+|0,L\rangle+|0,R\rangle-|2,L\rangle
\bigr).
$$

负号是后续干涉的来源，不能把它当成经典随机游走的概率拆分。

**算法案例**  
element distinctness：判断 $N$ 个黑箱值中是否有重复。Ambainis 量子行走使用 $O(N^{2/3})$ 查询并匹配下界；这比直接 Grover 搜索所有 $\binom N2$ 对所需的 $O(N)$ 查询更好，说明“利用状态空间结构”可超过朴素平方根搜索。

**依据**  
Ambainis, <https://arxiv.org/abs/quant-ph/0311001>；Santha survey, <https://arxiv.org/abs/0808.0059>；Magniez et al., <https://doi.org/10.1137/090745854>。

### B3. 给 QPE 非精确相位写出完整输出分布，而非只说“集中在附近”

**当前缺口**  
第 06 章对可精确表示相位讲得清楚，但研究生需要会计算有限精度失败概率。

**建议补写公式**  
令 $M=2^t$，逆 QFT 后测得 $y$ 的概率为

$$
\Pr(y)=\frac1{M^2}
\frac{\sin^2\!\bigl(\pi M(\phi-y/M)\bigr)}
{\sin^2\!\bigl(\pi(\phi-y/M)\bigr)},
$$

在分母为零时取极限。它是有限长度 Dirichlet kernel 的平方。

**可复算例**  
$t=2,M=4,\phi=1/3$ 时，$y=0,1,2,3$ 的概率约为

$$
0.0625,\ 0.6998,\ 0.1875,\ 0.0502.
$$

最邻近的 $y=1$ 并非必然输出。由此再解释：额外控制位不是只提高分辨率，也可把失败概率压到目标水平。

**依据**  
Watrous phase estimation course：<https://cs.uwaterloo.ca/~watrous/QC-notes/>。

### B4. Shor 需要补“连分数何时保证恢复”和分母约分的概率链

**当前缺口**  
现有 $N=15$ 例正确展示 $1/2$ 会给出错误分母 2，但尚未说明一般恢复条件和整套成功概率来自哪里。

**建议补写段落**

若

$$
\left|\frac yQ-\frac kr\right|<\frac1{2r^2},
$$

则 $k/r$ 的既约形式会出现在 $y/Q$ 的连分数收敛分数中。取 $Q\gtrsim N^2$ 可使分辨率足够，因为 $r<N$。但若 $\gcd(k,r)>1$，收敛分数只给 $r/\gcd(k,r)$；每个候选必须先做 $a^{r'}\bmod N$ 验证，再通过更多样本或候选倍数恢复真实阶。

**可复算例**  
$N=21,a=2$ 的阶为 6。若采到 $k=2$，相位为 $2/6=1/3$，连分数返回 3；但

$$
2^3=8\not\equiv1\pmod{21},
$$

所以 3 不是阶。若另一次得到分母 2，也不能直接取 2；可检验最小公倍数 6。这个例子比 $N=15$ 更直接展示多个约分样本如何合并。

**依据**  
Shor 原论文（现有正文引用）；Watrous phase estimation/factoring course：<https://jhwatrous.github.io/books-and-courses.html>。

### B5. 复杂度章节需要一张“已知包含、等价、未知关系”图

**当前缺口**  
现有包含链是正确的，但只列 P/BPP/BQP/NP/QMA/PP/PSPACE，尚未展示为什么 postselection 和 interactive proof 是理解 PP/PSPACE 的关键，也没有把 complete problem 放进图中。

**建议补写图与限定**

$$
\mathrm P\subseteq\mathrm{BPP}\subseteq\mathrm{BQP}
\subseteq\mathrm{QMA}\subseteq\mathrm{PP}\subseteq\mathrm{PSPACE},
$$

以及

$$
\mathrm{NP}\subseteq\mathrm{QMA},\qquad
\mathrm{PostBQP}=\mathrm{PP},\qquad
\mathrm{QIP}=\mathrm{PSPACE}.
$$

图中必须用不同线型区分“包含”“相等”“是否严格未知”，并显式写“NP 与 BQP 的一般包含关系未知”。

配两个 complete problem：

- 量子线路接受概率问题是典型 BQP-complete promise problem；
- 逆多项式 promise gap 的 $k$-local Hamiltonian 是 QMA-complete，2-local 版本也已知 QMA-complete。

**不能误写**  
PostBQP 不是现实设备可免费获得的能力；postselection 事件可指数罕见。QIP=PSPACE 也不表示普通 BQP 机器能在多项式时间解 PSPACE。

**依据**  
Aaronson, PostBQP=PP, <https://www.scottaaronson.com/papers/pp.pdf>；Jain et al., QIP=PSPACE, <https://arxiv.org/abs/0907.4737>；Watrous survey, <https://arxiv.org/abs/0804.3401>；Kempe, Kitaev, Regev, 2-local Hamiltonian, <https://arxiv.org/abs/quant-ph/0406180>。

### B6. 在每个“加速”旁边标注它究竟是哪一种复杂度

**当前缺口**  
教材虽强调端到端成本，但查询、门、样本、通信、空间和墙钟仍散落在各章。

**建议补写统一表**

| 资源模型 | 单位是什么 | 典型算法 | 常见偷换 |
|---|---|---|---|
| 查询复杂度 | oracle 调用 | Simon、Grover、AE | oracle 构造当免费 |
| 门/时间复杂度 | 基本门或时间步 | Shor、模拟 | 忽略路由、综合、纠错 |
| 样本复杂度 | 态副本/shots | tomography、shadows | 把测量设置数当总 shots |
| 通信复杂度 | 交换 qubit/bit | 指纹、分布式协议 | 忽略预共享纠缠 |
| 空间复杂度 | qubit/经典内存 | QIP/PSPACE 讨论 | 把空间包含当时间算法 |
| 墙钟/能耗 | 完整系统资源 | 实验优势 | 两边系统边界不同 |

每章结尾的“优势”表可增加一列“资源模型”，避免一个 $O(\cdot)$ 脱离语境。

**依据**  
Watrous, <https://arxiv.org/abs/0804.3401>；Ettinger et al. 的 HSP 查询/时间分离 <https://arxiv.org/abs/quant-ph/0401083>。

### B7. QML 先写数据访问模型，再谈维度或核

**当前缺口**  
第 08 章已有很好的六问清单，但“数据原本在哪里”还缺可操作分类。

**建议补写表**

| 输入 | 允许的访问 | 必须计入的成本 |
|---|---|---|
| 经典显式向量 | 顺序读取/普通 RAM | 至少读入所需元素 |
| 振幅态 $|x\rangle$ | 假设有态制备 oracle | 构建、更新、重复制备 |
| QRAM/采样访问 | 索引查询或 $\ell_2$-sampling | 数据结构建立与一致性 |
| 原生量子数据 | 多份未知态 | 副本数、测量破坏、采集成本 |

随后用 Tang 的量子启发推荐算法说明：若量子算法把强 $\ell_2$ 采样访问当成免费，经典算法获得可比较访问后，原先的指数差可能消失。结论应是“访问模型决定比较”，不是“所有 QML 都已被反量子化”。

**依据**  
E. Tang, <https://arxiv.org/abs/1807.04271>；量子启发奇异值变换 <https://arxiv.org/abs/1910.05699>。

### B8. 把“电路难模拟”与“预测任务难学”明确分开

**当前缺口**  
现有正文已说 Hilbert 空间大不等于优势，但需要一个更精确的证据框架。

**建议补写段落**  
区分三件事：

1. 生成或精确模拟某量子态/核矩阵困难；
2. 估计训练任务所需的少量统计量困难；
3. 在给定数据分布上取得更低泛化误差困难。

第一项不自动推出第二、三项。经典学习器可能不模拟量子过程，而直接从数据中学到同样的预测规则。Huang 等结果表明，数据本身可显著缩小某些“量子模型难模拟”带来的预测优势。

同时给一个正面反例：Liu、Arunachalam、Temme 构造了基于离散对数困难性的监督学习分离；它说明严谨量子学习优势是可能的，但需要明确的数据分布、计算假设、核估计和误差模型，不能由“量子特征空间很大”推出。

**依据**  
Huang et al., <https://doi.org/10.1038/s41467-021-22539-9>；Liu et al., <https://arxiv.org/abs/2010.02174>。

### B9. 增加量子核集中与 shots 爆炸的定量边界

**当前缺口**  
第 08 章有 barren plateau，却没有核方法的对应病态。

**建议补写段落**  
若量子核 $K(x,x')$ 的样本间差异随 $n$ 指数缩小，例如特征信号尺度为 $\delta=2^{-cn}$，则用独立 shots 估计到小于该差异的加性误差通常需要

$$
S=O(1/\delta^2)=O(2^{2cn}).
$$

此时“核在理想数学上可区分”不等于有限 shots 能学到。表达力过强、全局测量、纠缠和噪声都可能导致核集中。

**可复算例**  
若两类核均值只差 $\delta=1/32$，仅让标准误差降到 $\delta/2$ 的朴素 Bernoulli 估计就需数量级 $4/\delta^2=4096$ shots；当差异随 qubit 数指数缩小时，shots 也指数增长。

**依据**  
Thanasilp et al., “Exponential concentration in quantum kernel methods,” <https://doi.org/10.1038/s41467-024-49287-w>。

### B10. 单列“全态层析、目标验证、经典阴影”三者的任务差异

**当前缺口**  
第 05、08、11 章提到层析、保真度和经典阴影，但没有阻止读者把“预测很多 observable”误写成“重构完整量子态”。

**建议补写表**

| 任务 | 输出 | 样本规模核心依赖 | 何时合适 |
|---|---|---|---|
| 全态层析 | 完整 $d\times d$ 描述 | 一般态随 $d=2^n$ 指数增长 | 很小系统、模型诊断 |
| 目标态验证/DFE | 与已知目标的保真度或通过率 | 依赖目标结构 | 已知理想态 |
| 经典阴影 | 指定许多 observable 的估计 | $\log M$ 乘 shadow norm，而非无条件与 $n$ 无关 | 局域/低 shadow-norm 量 |

经典阴影的一般样本式应写成

$$
N=O\!\left(
\frac{\log(M/\delta)}{\epsilon^2}
\max_i\|O_i\|_{\rm shadow}^2
\right).
$$

对局域 Pauli 测量，权重为 $k$ 的 Pauli 串方差尺度可到 $3^k$，所以“对 $M$ 只对数增长”不能省略 observable 复杂度。

**可复算例：单 qubit shadow**  
对 $|0\rangle$ 随机选 $X,Y,Z$ 基测量。估计 $\langle Z\rangle$ 时，若选到 $Z$，单次估计量为 3；选到 $X/Y$ 时为 0。于是

$$
\mathbb E[\hat Z]=\frac13\times3=1,
\qquad
\operatorname{Var}(\hat Z)=3-1=2.
$$

它无偏，但单次值可超出物理期望值范围，必须靠多次平均和置信区间。

**依据**  
Huang, Kueng, Preskill, <https://arxiv.org/abs/2002.08953>；Haah et al., sample-optimal tomography, <https://arxiv.org/abs/1508.01797>；Flammia and Liu, <https://arxiv.org/abs/1104.4695>。

### B11. 资源估算加入统一的精度预算，而不只从逻辑错误率反推码距

**当前缺口**  
第 11 章已完整覆盖物理/逻辑资源，却没有展示应用精度如何分配给模型、算法、综合、采样和噪声。

**建议补写段落**  
对一个标量输出，可用保守三角界规划

$$
\epsilon_{\rm total}
\le
\epsilon_{\rm model}
+\epsilon_{\rm state}
+\epsilon_{\rm alg}
+\epsilon_{\rm synth}
+\epsilon_{\rm stat}
+\epsilon_{\rm noise}.
$$

这些预算不应机械平均：压低不同误差一单位的资源代价不同，应做敏感性优化。成功概率预算也要分给态制备失败、算法内禀失败、逻辑故障和验证漏检。

**可复算例**  
若化学目标总误差为 $10^{-3}$ Hartree，而模型/活性空间已占 $4\times10^{-4}$、态制备占 $2\times10^{-4}$，剩余只余 $4\times10^{-4}$ 给模拟、相位估计、综合、统计和逻辑噪声。若资源表却让每项各用 $10^{-3}$，端到端声明无效。

**图表**  
在第 11 章现有资源漏斗前加“误差预算树”，之后再映射到 logical qubits、T count、code distance。

**依据**  
Reiher et al. 的端到端化学资源估算强调编码、精度、门综合和纠错：<https://arxiv.org/abs/1605.03590>。

### B12. 把任意旋转综合误差转换成 T count

**当前缺口**  
第 10、11 章解释了 T count/T depth 和魔法态工厂，却没有说明高级算法中的连续角旋转如何产生大量 T 门。

**建议补写段落**  
在 Clifford+$T$ 模型中，算法给出的 $R_z(\theta)$ 通常要近似综合。Ross–Selinger 的无辅助位模型中，典型 T count 约为

$$
3\log_2(1/\epsilon)+O(\log\log(1/\epsilon)),
$$

精确常数和最优性依赖门集、辅助位、允许测量/随机化及数论假设。

**可复算例**  
若单个旋转需算符范数误差约 $10^{-10}$，主项为

$$
3\log_2(10^{10})\approx99.7,
$$

即约百个 T 门量级。若算法有 $10^8$ 个此类旋转，不能只报“$10^8$ 个单量子比特门”。同时说明逐门分配 $\epsilon_{\rm synth}=\epsilon_{\rm total}/G$ 是保守并合界，不一定是最优预算。

**依据**  
Ross and Selinger, <https://arxiv.org/abs/1403.2975>。

---

## 4. C 级：专题框或附录可补的内容

### C1. 一般 adversary bound 的地位：它不是又一个算法，而是查询复杂度刻画

建议用一页专题解释 adversary matrix 如何比较不同输入、oracle 查询一次最多改变多少加权内积，以及负权 adversary bound 与有界错误量子查询复杂度等价（常数因子内）。主线不必证明谱范数优化，只需让研究生知道 polynomial method 与 adversary method 是两条互补工具。

来源：Lee et al., <https://arxiv.org/abs/1011.3020>；Reichardt, <https://arxiv.org/abs/1005.1601>。

### C2. 量子信息量度应补“纯化—Uhlmann—信道单调性”的证明路线

建议作为第 05 章高级框：每个混态都可纯化；不同纯化由环境上的等距变换联系；Uhlmann 定理把混态保真度写成纯化重叠最大值；因此可快速推出保真度在量子信道下不减（状态更难区分）。这条路线能把 Stinespring、偏迹、保真度三个现有孤立点连接起来。

来源：Watrous, Chapters 2–3，<https://cs.uwaterloo.ca/~watrous/TQI/>。

### C3. 非 Abelian HSP 作为“查询优势不等于时间优势”的反例框

不要展开群表示论，只保留结论和逻辑：任意有限群 HSP 可用 $\operatorname{poly}(\log|G|)$ 次 oracle 调用在信息论上识别隐藏子群，但已知构造可需指数时间；困难转移到联合测量和经典处理。这是全书最干净的“query vs time”反例之一。

来源：Ettinger, Høyer, Knill, <https://arxiv.org/abs/quant-ph/0401083>。

### C4. 用两个历史资源估算做敏感性案例，而不是引用一个“所需 qubit 数”

可以并排展示同一 RSA-2048 目标在不同架构/算法假设下的估算：2019 年 Gidney–Ekerå 在 $10^{-3}$ 物理错误率、1 微秒表面码周期、10 微秒反应时间等假设下估计约 2000 万 noisy qubits、约 8 小时；2025 年后续工作在近似剩余算术、yoked codes、magic-state cultivation 和更长运行时间等不同设计下把 qubit 估算降到百万以下。教学重点不是哪一个数字“正确”，而是：

- 空间与时间可以交换；
- 算术、码、工厂和反应时间都会改变结论；
- 资源估算必须保存版本、假设和不确定区间。

来源：Gidney and Ekerå, <https://arxiv.org/abs/1905.09749>；Gidney 2025, <https://arxiv.org/abs/2505.15917>。

---

## 5. 另有四项“横向改造”，宜与上述补写同时完成

以下四项不另计 32 项主题数，但它们决定新增内容是否真正可学。

### 5.1 每个算法固定使用同一张“六问卡”

建议在第 07 章开头固定模板：

1. 输入规模是什么？
2. 输入通过什么 oracle/数据结构访问？
3. 输出是 bit string、样本、标量还是量子态？
4. 成功概率与误差是加性、相对还是 promise gap？
5. 查询、门、qubit、shots、验证各多少？
6. 对比的经典算法与硬件边界是什么？

之后 Simon、Grover、Shor、HHL、AE、模拟、QML 都按同样字段收尾。这样读者能横向比较，而不是记七套叙述。

### 5.2 每个渐近式至少配一个小规模数字预算

建议新增：

- Grover：$N=10^6$，约 $785$ 次查询；若每次 oracle 为 $10^4$ 个逻辑门，则仅 oracle 已约 $7.85\times10^6$ 门。
- AE：$\epsilon=10^{-2}$ 时理想 $1/\epsilon$ 与直接采样 $1/\epsilon^2$ 的数量级差，但同时列最大 Grover 幂。
- Trotter：给定交换子范数和误差预算反推 $r$。
- rotation synthesis：从 $\epsilon$ 反推 T count。
- shadows：从 observable 权重 $k$ 反推 $3^k$ 方差因子。

### 5.3 复杂度声明必须把“最坏情形、平均情形、特定实例”分栏

Shor 是有严格最坏情形多项式量子算法（对相应数论任务与随机重复框架）；VQE/QAOA 的实验通常是特定实例启发式；量子优势实验常是特定随机实例分布。建议在证据表中增一列“保证范围”。

### 5.4 练习答案要覆盖新增的操作性判断，而非只算矩阵

建议新增至少八题：

1. 算 $|0\rangle$ 与 $|+\rangle$ 的 $F,D,p_{\rm guess}$。
2. 比较 Bell 态与经典混合态的 $S(A|B)$ 和 $I(A:B)$。
3. 写 Deutsch 接受概率的二次多项式。
4. 从 AE 的 $a=1/2$ 恢复两支相位。
5. 构造 $0.6X+0.8Z$ 的 LCU block encoding。
6. 算四环 coined walk 两步态。
7. 用 QPE 的 Dirichlet-kernel 公式计算 $\phi=1/3,t=2$。
8. 对给定 $E-E_0$ 与能隙 $\Delta$ 求基态保真度下界。

---

## 6. 对现有文本的精确风险提示

本轮没有发现需要立即改正文的 P0 级数学错误，但后续扩写时要避免以下高风险表述：

1. **“经典阴影只需 $O(\log M)$ 次测量。”** 缺少 shadow norm、$\epsilon$、失败概率后是误导；对高权重/全局 observable 仍可指数昂贵。
2. **“QSP 可以实现任意矩阵函数。”** 必须有 block encoding、谱区间、多项式有界/奇偶条件和近似误差；一般非 Hermitian 矩阵不能直接按本征值任意变换。
3. **“AE 在 NISQ 上仍有二次优势。”** 需要以总 oracle 调用和最大相干深度为口径证明，不能由“没有 QFT”自动推出。
4. **“量子行走给所有图搜索平方加速。”** 复杂度依赖谱隙、marked fraction、setup/update/check cost；不同 walk 模型不能混写。
5. **“HSP 统一了 Shor，所以所有 HSP 都高效。”** 非 Abelian 情形的后处理/测量可能指数昂贵。
6. **“量子核难以经典模拟，所以学习有优势。”** 生成难、估计难、预测难是不同命题。
7. **“层析是验证量子算法的金标准。”** 全态层析通常指数扩展；已知目标或少量 observable 应优先任务特定验证。
8. **“逻辑 T count 就是运行时间。”** 还取决于 T depth、工厂吞吐、路由、测量反馈、码距和反应时间。
9. **“$\alpha$ 只是 block encoding 的记号。”** 它常直接乘进查询复杂度，且依赖矩阵表示。
10. **“BQP 包含关系图说明真实机器能力。”** 复杂度类是渐近、容错、统一电路模型；不等于近期设备或单实例墙钟表现。

---

## 7. 建议的三阶段实施顺序

### 第一阶段：先修心智模型

完成 A1–A10、A16。即先补信息量度、查询下界和幅度估计，再补验证方法树。完成后，读者能回答“量到了什么、加速相对什么、为什么不能更快、怎样相信答案”。

### 第二阶段：补现代算法栈

完成 A11–A15、B1–B4。用一张统一图把 Fourier/HSP 与 block-encoding/QSP 两条主线并列；量子行走作为第三条搜索主线。

### 第三阶段：把理论换算成研究资源

完成 B5–B12 与 C4。将 complexity class、QML 证据、tomography/shadows、精度预算、T 综合和物理资源连成闭环。

若篇幅受限，优先删除完整证明的技术细节，不应删除：定义、输入模型、一个手算例、一个边界条件和一条原始来源。

---

## 8. 核心来源与证据索引

以下优先列原始论文、作者公开教材或正式课程；每条说明它支撑本报告的哪一类补写。

### 量子信息量度

1. John Watrous, *The Theory of Quantum Information*：迹距离、Holevo–Helstrom、保真度、熵、信道距离。<https://cs.uwaterloo.ca/~watrous/TQI/>
2. Watrous 公开课程目录：purification/fidelity、relative entropy、strong subadditivity、Holevo theorem、channel distinguishability。<https://cs.uwaterloo.ca/~watrous/TQI-notes/>
3. M. B. Ruskai, “Inequalities for Quantum Entropy”：相对熵单调性、强次可加与 Holevo bound。<https://arxiv.org/abs/quant-ph/0205064>

### 查询下界与复杂度

4. Beals et al., “Quantum Lower Bounds by Polynomials”：$T$ 查询算法接受概率次数至多 $2T$；total 与 promise function 的边界。<https://arxiv.org/abs/quant-ph/9802049>
5. Bennett et al., “Strengths and Weaknesses of Quantum Computing”：黑箱搜索下界与 oracle 世界边界。<https://doi.org/10.1137/S0097539796300933>
6. Lee et al., “Quantum query complexity of state conversion”：一般 adversary bound 对查询复杂度的刻画。<https://arxiv.org/abs/1011.3020>
7. John Watrous, “Quantum Computational Complexity”：BQP、QMA、QIP 等复杂度框架。<https://arxiv.org/abs/0804.3401>
8. Scott Aaronson, “Quantum Computing, Postselection, and PP”：PostBQP=PP。<https://www.scottaaronson.com/papers/pp.pdf>
9. Jain, Ji, Upadhyay, Watrous, “QIP = PSPACE”。<https://arxiv.org/abs/0907.4737>
10. Kempe, Kitaev, Regev, “The Complexity of the Local Hamiltonian Problem”：2-local Hamiltonian QMA-complete。<https://arxiv.org/abs/quant-ph/0406180>

### 幅度估计、模拟与矩阵变换

11. Brassard et al., “Quantum Amplitude Amplification and Estimation”：AE 的相位结构和误差界。<https://arxiv.org/abs/quant-ph/0005055>
12. Grinko et al., “Iterative Quantum Amplitude Estimation”：无 QPE 的置信区间式 AE。<https://arxiv.org/abs/1912.05559>
13. Suzuki et al., “Amplitude Estimation without Phase Estimation”：不同 Grover 幂加最大似然。<https://arxiv.org/abs/1904.10246>
14. Berry et al., sparse Hamiltonian simulation/no-fast-forwarding。<https://arxiv.org/abs/quant-ph/0508139>
15. Berry et al., truncated Taylor/LCU Hamiltonian simulation。<https://arxiv.org/abs/1412.4687>
16. Berry, Childs, Kothari, nearly optimal sparse simulation。<https://arxiv.org/abs/1501.01715>
17. Low and Chuang, “Hamiltonian Simulation by Qubitization”。<https://quantum-journal.org/papers/q-2019-07-12-163/>
18. Gilyén et al., “Quantum Singular Value Transformation and Beyond”：block encoding 与 QSVT 的统一框架。<https://arxiv.org/abs/1806.01838>

### 量子行走与隐藏子群

19. Ambainis, element distinctness $O(N^{2/3})$ 查询算法。<https://arxiv.org/abs/quant-ph/0311001>
20. Santha, quantum walk algorithms survey。<https://arxiv.org/abs/0808.0059>
21. Magniez et al., “Search via Quantum Walk”。<https://doi.org/10.1137/090745854>
22. Ettinger, Høyer, Knill, arbitrary finite-group HSP 的多项式查询/指数时间分离。<https://arxiv.org/abs/quant-ph/0401083>

### QML 边界

23. E. Tang, quantum-inspired recommendation systems：可比较采样访问下的反量子化。<https://arxiv.org/abs/1807.04271>
24. Huang et al., “Power of data in quantum machine learning”：难模拟不自动等于难预测。<https://doi.org/10.1038/s41467-021-22539-9>
25. Thanasilp et al., quantum kernel concentration。<https://doi.org/10.1038/s41467-024-49287-w>
26. Liu, Arunachalam, Temme, 严格监督学习量子优势构造。<https://arxiv.org/abs/2010.02174>

### 验证、层析与资源

27. Huang, Kueng, Preskill, “Predicting Many Properties…from Very Few Measurements”：经典阴影及 $\log M$ 依赖的适用条件。<https://arxiv.org/abs/2002.08953>
28. Haah et al., “Sample-optimal tomography of quantum states”：一般态层析的样本复杂度。<https://arxiv.org/abs/1508.01797>
29. Flammia and Liu, “Direct Fidelity Estimation from Few Pauli Measurements”。<https://arxiv.org/abs/1104.4695>
30. Gheorghiu, Kapourniotis, Kashefi, quantum verification review。<https://arxiv.org/abs/1709.06984>
31. Ross and Selinger, arbitrary $z$ rotations 的 Clifford+$T$ 综合。<https://arxiv.org/abs/1403.2975>
32. Reiher et al., FeMoco 端到端资源估算。<https://arxiv.org/abs/1605.03590>
33. Gidney and Ekerå, RSA-2048 资源估算及明确硬件假设。<https://arxiv.org/abs/1905.09749>

## 9. 验收标准

后续正文补写完成后，可用以下标准判断本轮缺口是否真正关闭：

- 读者能手算至少两个状态的 $F,D,p_{\rm guess}$，并知道 fidelity 约定差异；
- 能用 Bell 态和经典混合态算出不同的互信息/条件熵；
- 能解释一次查询为何给至多二次接受概率，并说清 Grover 最优性的模型；
- 能从 Grover 二维旋转推到 AE 的两个本征相位和误差界；
- 能从 LCU 的 PREPARE/SELECT 算出块编码左上块；
- 能说清 block-encoding normalization 为什么影响复杂度；
- 能把 Simon 与 Shor 放在 Abelian HSP 图中，同时指出一般 HSP 不必时间高效；
- 能区分量子行走的结构化搜索与对候选对做朴素 Grover；
- 能在 QML 声明中列出数据访问、经典基线、shots、泛化和反量子化风险；
- 能解释 tomography、target verification、classical shadows 各自输出什么；
- 能把应用误差预算一路换算到旋转综合、T count、逻辑失败率和物理资源；
- 所有新增“优势”结论都同时写明输入模型、输出、误差、成功概率与经典比较对象。

达到这些标准后，教材才真正覆盖从初学计算到现代量子算法论文阅读所需的理论桥梁。
