# 第 17 轮交叉审稿：计算模型与新增算法数学复核

日期：2026-09-22  
审稿方式：只读，未修改 `handbook/` 或附录。

## 1. 范围与结论

本轮逐式复核了：

- `handbook/17-computation-models.md`；
- 第 16 轮在 `handbook/07-algorithms.md`、`08-applications.md`、`16-advanced-algorithms-verification.md` 新增的 qDRIFT、QLSA、QAOA、QSP、委托验证与跨尺度验证内容；
- `handbook/appendices/exercises.md` 第 17 章的 10 道答案；
- `handbook/README.md` 中第 17 章的入口与先修路线。

严重度统计：

| 等级 | 数量 | 结论 |
|---|---:|---|
| P0 | 0 | 未发现会使核心推导或结论失效的问题 |
| P1 | 0 | 未发现需要立即阻止发布的问题 |
| P2 | 7 | 均可定点修复，主要是定义域、假设、精确计数、教学对齐和引用覆盖 |

已确认无误的核心计算包括：

- MBQC 两个投影分支分别为 $H|\psi\rangle$ 与 $XH|\psi\rangle$，概率各为 $1/2$；
- $H(s)=-(1-s)X-sZ$ 的本征值为 $\pm\sqrt{s^2+(1-s)^2}$，最小谱隙为 $\sqrt2$；
- $p_s=0.2,\delta=0.01$ 时 $R=21$，纯退火段 TTS 为 $420\,\mu\mathrm{s}$，加入每轮 $100\,\mu\mathrm{s}$ 读出复位后为 $2.52\,\mathrm{ms}$；
- 理想瞬时 $X_1$ echo 中 $Z_1Z_2$ 抵消、$Z_2Z_3$ 累加，所得 $U=e^{-iJtZ_2Z_3}$；
- 三顶点路径的 $p=1$ QAOA 数值为 $1+3\sqrt3/8=1.6495190528\ldots$；
- qDRIFT 正系数算例的一阶平均生成项为 $-itH/N$；
- 二维 QLSA 例得到 $|x\rangle=(2|0\rangle+|1\rangle)/\sqrt5$、$\langle Z\rangle=3/5$；
- $W(x)$ 是酉矩阵，$W(x)^2$ 左上元为 $T_2(x)=2x^2-1$；
- 第 17 章答案 1–8、10 的结论与正文题意一致；第 9 题的教学目的正确，但精确整数计数需按 P2-4 修订。

## 2. P2 问题与精确修法

### P2-1｜qDRIFT 的“酉项”表述缺少 Hermitian 条件和负系数符号

**位置**：`handbook/07-algorithms.md` 第 4 节“现代模拟方法怎样选择”，当前第 322、335–361 行。

**问题**：表格写“按 $|\alpha_j|$ 随机抽取 Pauli/酉项”，容易让读者以为任意酉矩阵都能直接作为 Hamiltonian 项。标准 qDRIFT 假设

$$
H=\sum_j h_jH_j,
\qquad H_j=H_j^\dagger,
\qquad \|H_j\|=1,
$$

且每个 $e^{-i\tau H_j}$ 可实现。Pauli 串是 Hermitian unitary 的特例；一般“酉项”若非 Hermitian，不能直接充当 Hamiltonian 项。当前正系数 $0.6X+0.8Z$ 的算例本身正确，但没有告诉读者负系数应进入演化符号，也没有在误差句中点明 diamond-norm 信道误差。

**精确修法**：

1. 把表格中的“Pauli/酉项”改成“可高效演化的归一化 Hermitian 项（Pauli 串为特例）”；
2. 在算例前补一般一步：以 $p_j=|h_j|/\lambda$ 抽取 $j$，施加

   $$
   e^{-i(\lambda t/N)\operatorname{sgn}(h_j)H_j},
   \qquad \lambda=\sum_j|h_j|;
   $$

3. 把末句改为“在 diamond norm 的平均信道误差不超过 $\epsilon$ 的标准界下，$N=O(\lambda^2t^2/\epsilon)$”。

**依据**：E. Campbell, [A random compiler for fast Hamiltonian simulation](https://arxiv.org/abs/1811.08017)（预印本 2018；PRL 2019），原文明确要求归一化 Hermitian 项并比较平均量子信道。

### P2-2｜TTS 公式未声明 $p_s$ 与 $\delta$ 的定义域和边界值

**位置**：`handbook/17-computation-models.md` 第 5 节，当前第 176–193 行。

**问题**：

$$
R=\left\lceil\frac{\log\delta}{\log(1-p_s)}\right\rceil
$$

只在 $0<p_s<1$、$0<\delta<1$ 时可直接使用。若 $p_s=0$，分母为 0，任何有限重复都不能成功；若 $p_s=1$，实际只需一次，但把公式机械代入或取极限会得到 0。正文算例位于内部区间，因此数值没有错；缺陷在公式边界。

**精确修法**：公式前改为“对 $0<p_s<1$、$0<\delta<1$”；公式后补“$p_s=0$ 时有限 $R$ 无法达到目标，$p_s=1$ 时取 $R=1$”。若 $p_s$ 来自有限样本估计，建议再说明公平基准应把估计不确定性带入 TTS，而不是只代入点估计。

**引用补强**：当前 Kadowaki–Nishimori 论文支持量子退火起点，但不是这套 TTS 基准公式的直接出处。建议增列 T. F. Rønnow et al., [Defining and detecting quantum speedup](https://arxiv.org/abs/1401.2910)（2014），其 TTS 定义同时区分退火段和端到端时间。

### P2-3｜绝热—门模型“多项式等价”的条件仍可再收紧

**位置**：`handbook/17-computation-models.md` 第 4.2 节，当前第 163–168 行。

**问题**：现文“在明确的局域性、精度和路径构造下”方向正确，且随后已经否定“任意线性插值都有效”。不过“路径构造”过于含混，初学者仍可能把定理理解为任意连续局域 $H(s)$ 都能高效转换，而忽略路径本身必须高效描述，以及 Hamiltonian 范数、导数、演化时间和目标误差都属于资源账。

**精确修法**：将首句收紧为：

> 对高效可描述的局域（或相应稀疏访问）Hamiltonian 路径，并把所需精度、Hamiltonian 范数与导数、演化时间纳入资源计数时，闭系统绝热计算与标准门模型在计算复杂度意义下多项式等价。

保留后面的四条“不表示”；它们写得准确。

**依据**：D. Aharonov et al., [Adiabatic Quantum Computation is Equivalent to Standard Quantum Computation](https://arxiv.org/abs/quant-ph/0405098)（2004），证明的是受控构造下的模型级多项式等价，不是任意物理插值的统一性能保证。

### P2-4｜8 位 Grover 例把渐近近似值舍入成 13，但精确最佳整数是 12

**位置**：

- `handbook/17-computation-models.md` 第 8.1 节，当前第 310–322 行；
- `handbook/17-computation-models.md` 自检第 9 题；
- `handbook/appendices/exercises.md` 第 17 章答案 9，当前第 484–492 行。

**问题**：$\frac\pi4\sqrt{256}=12.566\ldots$ 是大 $N$ 渐近估计，不是可直接向上取整的精确最优迭代数。唯一目标时令

$$
\theta=\arcsin(1/\sqrt{256})=\arcsin(1/16),
$$

$r$ 次 Grover 迭代的成功概率为

$$
p_r=\sin^2[(2r+1)\theta].
$$

离连续最优点

$$
r_*^{\rm cont}=\frac{\pi}{4\theta}-\frac12
=12.05818\ldots
$$

最近的整数是 $r=12$；此时 $p_{12}\approx0.999947$，而 $p_{13}\approx0.986186$。现文使用“约”并不破坏 $O(\sqrt N)$ 教学结论，但“即约 13 次”会让初学者误以为应机械向上取整。

**精确修法**：改成“渐近式给出约 $12.6$；按精确旋转角选择的最佳整数为 12 次。这里无论 12 还是粗略说十余次，都只是 oracle 级成本”。同步改自检题和答案标题，不改变“查询不等于普通加密”的教学重点。

**依据**：M. Boyer et al., [Tight bounds on quantum searching](https://arxiv.org/abs/quant-ph/9605034)（1996），给出任意迭代次数下的成功概率分析。

### P2-5｜第 17 章自检第 10 题依赖未列入先修的第 16 章

**位置**：

- `handbook/17-computation-models.md` 当前第 345–347、371 行；
- `handbook/appendices/exercises.md` 第 17 章答案 10，当前第 494–503 行；
- `handbook/README.md` 第 17 章路线，当前第 92 行。

**问题**：正文只用一行提问式表格链接到第 16 章，未在本章解释 Mahadev/LWE、有限量子客户端陷阱式 MBQC 或多证明者 rigidity；自检却要求完整说出这三种信任模型。README 给第 17 章列的先修是 04、07、09、14，没有第 16 章。答案内容本身正确，但考查范围与学习路线错位。

**精确修法（二选一）**：

1. 保留题目：在第 9 节表格后加入 4–6 句最小信任模型摘要，并把 README 第 17 章先修改为“04、07、09、14、16”；或
2. 保持第 17 章独立：把第 10 题替换成正文已完整讲授的模型辨析题，例如让读者比较“门—绝热等价”和“退火器性能声明”的证据条件，将现答案留在第 16 章练习。

对初学路线而言，方案 2 更紧凑，也避免第 16、17 章重复。

### P2-6｜第 17 章有三处无必要的英文术语回退

**位置**：`handbook/17-computation-models.md` 当前第 32、120、284、294、298 行。

**问题**：STYLE 要求术语首次出现时给白话解释。当前直接使用 `schedule`、`observable`、`primitive`；其中“可观察量”已在前文定义，却在本章图和正文中又退回英文，“密码 primitive”则没有中文解释。这些词不会造成公式错误，但会破坏面向初学者的一致语体。

**精确修法**：

- 首次写“调度函数（schedule，即 $s$ 随物理时间变化的规则）”，后文只写“调度函数”；
- 两处 `observable` 统一改为“可观察量”；
- “密码 primitive”改为“密码原语（组成协议的基础运算，例如分组加密或哈希）”。

`time to solution`、`refocusing` 已在首次出现处给出中文解释，可保留。

### P2-7｜三顶点 QAOA 公式正确，但参考起点缺直接支持它的一手来源

**位置**：

- `handbook/08-applications.md` 第 3 节“三顶点路径”，当前第 206–249 行；
- 同章参考起点，当前第 437–449 行。

**问题**：公式与数值复算无误，但现有参考起点列出 QAOA 原始论文和综述，没有列出推导一般图 $p=1$ MaxCut 边期望公式的直接一手来源。Farhi–Goldstone–Gutmann 原始文献足以支持 QAOA 框架，却不如后续一般图解析公式直接支持这里的 $d_u,d_v$ 表达式。

**精确修法**：在第 8 章参考起点增列：Z. Wang, S. Hadfield, Z. Jiang, E. G. Rieffel, [Quantum Approximate Optimization Algorithm for MaxCut: A Fermionic View](https://arxiv.org/abs/1706.02998)（预印本 2017；PRA 2018）。无需改正文推导。

## 3. 无问题域的明确结论

### MBQC：0 个 P0/P1/P2

逐支投影、概率归一化、$X^mH$ 伴随算符和适应性边界均正确；小簇态没有被误写成通用容错证明。现有 Raussendorf–Browne–Briegel 原始来源支持正文。

### 二能级绝热谱计算：0 个公式问题

矩阵、行列式、本征值、最小点和端点基态均正确。P2-3 只收紧等价定理的适用条件，不是修改该算例。

### echo：0 个 P0/P1/P2

时间顺序、共轭关系、对易性和总相位均正确；正文也已列出瞬时脉冲、等时、精确 Hamiltonian、有限脉冲和不可对易残余项等物理边界。

### QAOA 数学：0 个公式问题

单边与三顶点路径的符号、角度和数值均正确。P2-7 仅为直接引用覆盖问题。

### QSP / block encoding：0 个 P0/P1/P2

$W(x)$ 的定义域、酉性、平方矩阵、Chebyshev 多项式次数与奇偶性说明均正确；正文也明确不同信号酉和相位约定不可混用。

### QLSA：0 个 P0/P1/P2

条件数、逆矩阵作用、归一化、$Z$ 期望和“量子态输出不等于打印全部分量”均正确，且验证成本的 $\kappa$ 边界有一手来源覆盖。

### 委托验证与跨尺度验证：0 个事实错误

第 16 章关于陷阱式 MBQC、多证明者 rigidity、Mahadev/LWE、阴影范数、能隙证书和跨尺度偏差的新增内容未发现公式或事实错误。P2-5 是第 17 章考题先修错位，不是答案内容错误。

## 4. 一手来源核对记录

以下网页均于 2026-09-22 访问，只用原始论文或作者公开稿核对疑点：

1. R. Raussendorf, D. E. Browne, H. J. Briegel, [Measurement-based quantum computation on cluster states](https://arxiv.org/abs/quant-ph/0301052)（MBQC 通用性、伴随算符与适应性）。
2. D. Aharonov et al., [Adiabatic Quantum Computation is Equivalent to Standard Quantum Computation](https://arxiv.org/abs/quant-ph/0405098)（绝热—门模型多项式等价的构造边界）。
3. T. F. Rønnow et al., [Defining and detecting quantum speedup](https://arxiv.org/abs/1401.2910)（重复成功率与 TTS 口径）。
4. E. Campbell, [A random compiler for fast Hamiltonian simulation](https://arxiv.org/abs/1811.08017)（qDRIFT 的 Hermitian 项、抽样和平均信道误差）。
5. Z. Wang et al., [Quantum Approximate Optimization Algorithm for MaxCut: A Fermionic View](https://arxiv.org/abs/1706.02998)（一般图 $p=1$ QAOA 解析式）。
6. M. Boyer et al., [Tight bounds on quantum searching](https://arxiv.org/abs/quant-ph/9605034)（Grover 任意迭代次数的成功概率）。
7. A. Parra-Rodriguez et al., [Digital-Analog Quantum Computation](https://arxiv.org/abs/1812.03637)（数字—模拟模型与快局域控制边界）。

## 5. 验收建议

本轮没有 P0/P1，正文的主要数学链可以保留。下一轮只需处理上述 7 个 P2：其中 P2-1、P2-2、P2-4 涉及公式或算法定义的精确性；P2-3 涉及定理适用域；P2-5、P2-6 涉及初学者路线与语言；P2-7 是直接引用补强。修复后应再次同步核对第 17 章自检第 9、10 题与答案，而不必重写本章结构。
