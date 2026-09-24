# 第六轮：全书教学架构与初学者体验缺口审查

> 日期：2026-09-22  
> 审查范围：`handbook/README.md`、`STYLE.md`、00–12 全部正文、四份内容附录与审校记录  
> 角色：全书教学架构与初学者体验审稿人  
> 本轮原则：只提出问题与改进方案，不直接修改正文或附录。

## 一、执行摘要

这套手册已经具备三项很难得的优点：

1. 对量子优势、硬件里程碑和厂商声明的边界非常谨慎；
2. 00–08 的多数公式都有可手算例，06–08 尤其重视查询成本、输入输出和经典基线；
3. 09–12 把控制、纠错、资源估算和网络工程放在同一系统边界内，明显优于只讲理想线路的普通入门材料。

但若以“零基础读者能够顺着读到入门研究生研究入口”为发布目标，目前仍有四个结构性缺口：

- **学习闭环有一处明确断裂**：练习附录第 0–3 章答案仍对应旧版题目，与当前正文自检题不匹配。
- **一般形式出现得早于正式定义**：第 02 章已经用密度矩阵、非选择测量、POVM 和 Kraus/测量算子语言，第 03 章继续使用混态与偏迹，而密度矩阵直到第 05 章才正式讲解。
- **量子信息论主干缺席**：只有纯态纠缠熵的一个公式，没有系统讲状态可区分性、迹距离、保真度、冯·诺依曼熵、条件熵、互信息、相对熵、数据处理不等式和 Holevo 界。结果是第 05、09、11、12 章反复使用“保真度”和“信息”时，读者没有统一数学尺度。
- **复杂度与研究方法的桥梁不足**：第 07 章列出 P/BPP/BQP/NP/QMA/PP/PSPACE，却没有先建立决定问题、承诺问题、归约、一致线路族和不同资源模型；通信复杂度完全缺席；第 11 章有优秀的审稿清单，却还不是一套可执行的研究工作流。

### 优先级统计

| 等级 | 数量 | 含义 |
|---|---:|---|
| P0 | 0 | 未发现会直接推翻全书主结论的教学架构错误 |
| P1 | 4 | 会让初学者用错答案、混淆概念或误解核心指标，发布前应处理 |
| P2 | 22 | 明显影响知识闭环、可读性、练习或研究衔接，应在主线修订中处理 |
| P3 | 4 | 高价值扩展，可在核心修订后加入 |

下文共列出 **30 条可执行改进**，每条均给出建议章位和验收方式。

## 二、与权威教材和公开课程对照后的总判断

### 2.1 权威材料呈现出的共同顺序

几套权威材料虽然深浅不同，但顺序高度一致：

1. **先建立有限维线性代数、纯态、测量与电路。** IBM 的 *Basics of Quantum Information* 从经典信息、单系统、多系统和电路开始，再以传态、超密编码和 CHSH 收束；Nielsen–Chuang 也先补量子力学与计算机科学基础。
2. **再进入密度矩阵、一般测量、信道和状态可区分性。** IBM 的 *General Formulation of Quantum Information* 明确按“密度矩阵 → 信道 → 一般测量 → 距离/相似度”的路径组织。Watrous 的研究生材料也把 states/measurements/channels、purification/fidelity、entropy/Holevo 排成连续知识链。
3. **量子信息论不是附属名词表，而是连接测量、通信、安全、噪声和纠错的桥。** Preskill 第 5 章把冯·诺依曼熵作为经典信息经量子信道传输、信息—扰动、纠缠量化和量子信息传输的共同语言。
4. **复杂度先讲问题模型，再讲类别包含。** Watrous 的量子复杂度讲义从 hardness、资源和 promise problem 开始，而不是先给字母缩写集合。
5. **通信复杂度是量子信息与量子算法之间的天然桥梁。** Watrous 公开课、MIT QIS 课程和 Buhrman 等人的综述都把“谁持有什么输入、允许共享什么资源、发送多少 bit/qubit、容许多大错误”作为独立模型。
6. **成熟课程不仅有自检，还有分层作业、项目和复现。** MIT 课程公开作业与解答，MIT QIS 课程包含项目汇报；研究出版规范要求数据、代码、协议和环境信息足以让他人复算。

### 2.2 当前手册与这些基准的相对位置

当前手册对“量子计算会被怎样夸大”讲得很强，对“为什么这些概念在数学上构成一门信息科学”讲得偏弱。读者能学会许多正确的警戒语，却不一定能回答以下研究生入门问题：

- 两个态“接近”究竟用什么量衡量？这个量有怎样的操作意义？
- 为什么测量或噪声不能增加可区分性？
- 一个子系统与另一个子系统共享了多少总关联？
- 为什么 $n$ 个量子比特的状态描述有 $2^n$ 个振幅，却不能读出 $2^n$ 个经典数？
- BQP 中的“问题”“输入规模”“一致电路”和“有界错误”分别是什么？
- 查询复杂度、时间复杂度、样本复杂度、通信复杂度和实验墙钟时间怎样区分？
- 怎样把一篇论文的主张变成一个可复算、可证伪的小项目？

因此，本轮最核心的建议不是继续添加更多硬件纪录，而是补齐“信息量—可区分性—复杂度—研究方法”这条中间脊梁。

## 三、P1：发布前应处理的四个问题

### 1. 练习附录第 0–3 章答案与当前自检题错位（P1）

**现状证据**

- `00-overview.md:128–131` 的四题分别问 $|+\rangle/|-\rangle$、量子并行、加速成本和 PQC；`appendices/exercises.md:7–10` 却回答“最小数学结构、酉演化、门错误和研究优势主张”。
- `01-math.md:214–217` 要求归一化向量、张量积、验证 $H$ 酉性和计算 $\langle X\rangle$；附录第 1 章却回答复数方程、极坐标、$H|0\rangle$ 和投影概率。
- 第 02 与第 03 章的答案也互相错位：附录第 2 章是多比特/Bell/CNOT，附录第 3 章是单比特相位/旋转/层析。
- `appendices/audit-log.md` 仍写“68 道题逐题对应”和“第五轮未发现问题”，与当前文件事实不一致。

**影响**

初学者按正文链接查答案时会得到另一道题的解法；这不仅是排版问题，还会破坏自我诊断的可信度。

**建议章位与动作**

- 直接重写附录第 0–3 章，使题号、题干关键词和答案逐题对应当前正文；
- 在每个正文题目后加入稳定锚点，例如 `ex-01-03`，答案端反向链接题目；
- 更新审校记录，删除已经失真的“全部逐题对应”断言，改成由脚本检查题数和锚点的可验证记录。

**验收**

- 13 章自检题数量与附录答案数量逐章相等；
- 随机抽查每题的变量、输入态和数值与答案一致；
- 正文到答案、答案回正文均可跳转。

### 2. 密度矩阵和一般测量先使用、后定义（P1）

**现状证据**

- 第 02 章在第 121 行起直接用输入密度矩阵 $\rho$ 讲非选择测量，第 167 行进入 POVM 和测量算子；
- 第 03 章用 Bell 密度矩阵、经典混态和偏迹；
- 直到第 05 章开头才正式给出密度矩阵的系综定义、正半定与迹为 1 的条件。

**影响**

读者刚建立“量子态就是归一化 ket”的模型，就被要求接受另一套状态对象和一般测量形式；这容易把密度矩阵误解成纯态外积的记号技巧，而不是包含经典不确定性和约化态的一般状态描述。

**建议章位与动作**

推荐两种方案择一：

- **最小改动**：第 02 章只保留纯态投影测量和条件态；把非选择测量、POVM、测量工具整体移至第 05 章，在密度矩阵正式定义之后；第 03 章保留纯 Bell 态，经典混态和偏迹段落加一页“密度算符先导”。
- **理想改动**：把第 05 章拆成“05A 密度矩阵与一般测量”和“05B 信道与噪声”，第 03 章的约化态直接引用 05A 的定义。

IBM 的一般形式课程采用“密度矩阵 → 信道 → 一般测量”的明确递进，可作为结构校准：[General formulation of quantum information](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information)（持续维护，访问 2026-09-22）。

**验收**

任一符号 $\rho,E_k,M_k,K_k$ 第一次出现时，读者已经见过其对象类型、维数、合法条件和最小算例。

### 3. “保真度”贯穿后半书，却没有数学定义（P1）

**现状证据**

第 05 章只在指标表写“状态保真度：两个状态多接近”；第 09、11、12 章又频繁讨论门保真度、条件保真度和纠缠保真度，但没有给出状态保真度公式、平方/不开平方的两种约定，也没有说明平均门保真度与状态保真度不是同一个对象。

**影响**

初学者很容易把“99% 保真度”理解成“1% 独立错误概率”，恰好与第 11 章想纠正的误解相冲突。

**建议章位与动作**

- 在第 05 章新增“状态距离与相似度”小节，明确本书采用根保真度还是平方保真度；
- 先算纯态 $|0\rangle$ 与 $|+\rangle$，再算纯态与混态；
- 第 09/11/12 章每次出现“保真度”时标明对象和估计方法；
- 在术语表加入状态保真度、平均门保真度、过程保真度、条件保真度的分项定义。

IBM 官方课程明确警告保真度存在平方与不开平方两种常用约定：[Fidelity](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/purifications-and-fidelity/fidelity)（访问 2026-09-22）。

**验收**

全书任意一个“保真度 0.99”都能回答：比较什么对象、采用哪一定义、是否条件于成功事件、能否换算成错误率。

### 4. 复杂度类先列结论，缺少问题模型与归约语言（P1）

**现状证据**

第 07 章第 7 节直接列 P、BPP、BQP、NP、QMA、PP、PSPACE 及包含关系，却没有定义：

- 决定问题与搜索/函数/采样问题的区别；
- 输入长度和多项式资源；
- 承诺问题；
- 一致量子线路族；
- 多项式时间归约、hard 与 complete；
- 有界错误如何放大。

**影响**

读者可能把复杂度类当作算法清单，或把“在 BQP 中”“存在量子算法”“量子更快”三句话当成同义句。

**建议章位与动作**

- 在第 06 章开头或第 07 章复杂度节之前加入 4–6 页“计算问题与资源模型”；
- 用 Deutsch–Jozsa/Simon 解释承诺问题，用 Grover 区分查询下界与时间下界；
- 给一个最小归约例子，再解释 NP-hard、NP-complete、BQP 的关系；
- 把现有复杂度类包含图改成“已知包含 / 是否严格未知 / 不可比较未知”的图例。

Watrous 的公开讲义先定义 promise problem 再讨论 BQP/QMA：[Quantum Computation lecture 22](https://cs.uwaterloo.ca/~watrous/QC-notes/QC-notes.pdf)（2006）；更系统的综述见 [Quantum Computational Complexity](https://cs.uwaterloo.ca/~watrous/Papers/QuantumComputationalComplexity.pdf)（2008）。

**验收**

读者能够把一个新问题写成输入、yes/no 承诺、误差门槛和资源界，并能解释“查询优势为何不是自动的时间优势”。

## 四、P2：主线修订中应处理的二十二项

### 5. 新增一章“量子信息的度量与极限”（P2）

**建议章位**：第 05 章之后、现第 06 章算法骨架之前。理想情况下编号为新 06，后续章节顺延。

**最低知识树**：

1. 经典 Shannon 熵与二元熵；
2. 冯·诺依曼熵和谱；
3. 联合、边缘、条件熵与互信息；
4. 迹距离、保真度与态判别；
5. 量子相对熵与数据处理；
6. Holevo 信息和可访问信息上界；
7. 纯二分态纠缠熵；
8. 传态、超密编码和噪声信道的资源账本回扣。

**原因**：Watrous 的研究生教材把“purification/fidelity → state discrimination → entropy/source coding → Holevo”作为完整主线；Preskill 将冯·诺依曼熵视为信息传输、信息—扰动、纠缠量化与信道的共同语言。

**权威基准**：[Watrous, *The Theory of Quantum Information*](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)（2018）；[Preskill, Chapter 5: Quantum Information Theory](https://www.preskill.caltech.edu/ph229/notes/chap5.pdf)（官方讲义，访问 2026-09-22）。

**验收**：新增章节至少有 4 个可手算二级系统例题，并能被第 03、05、11、12 章交叉引用。

### 6. 补齐经典概率与统计的最低先修（P2）

**现状**：第 01 章标题写“概率、条件概率与期望值”，正文只定义期望，没有条件概率、Bayes、独立性、方差或协方差。

**建议章位**：第 01 章。

**动作**：加入条件概率与 Bayes、独立/相关、方差与标准误、二项分布、联合概率表。用“同一 Bell 统计”和“有限 shots”各做一个例子。

**验收**：第 02 章采样误差、第 08 章 VQE shots、第 11 章置信区间不再引入未讲概念。

### 7. 加入 SVD、奇异值和 Schmidt 分解的来源（P2）

**现状**：第 03 章直接陈述 Schmidt 分解；HHL 又使用条件数 $\kappa$，但第 01 章没有奇异值、SVD 或条件数。

**建议章位**：第 01 章末增加“可选但推荐：SVD 与算符范数”，第 03 章用 $2\times2$ 系数矩阵做一次 SVD 到 Schmidt 的推导。

**动作**：至少定义奇异值、谱范数、条件数，对矩阵 `diag(1,1/2)` 手算；把 Bell 态系数矩阵的两个奇异值与 Schmidt 权重联系起来。

**验收**：读者能解释 Schmidt 分解为何总存在，以及 HHL 中小奇异值为何造成困难。

### 8. 补一页 Hamiltonian、生成元、对易与连续时间演化（P2）

**现状**：第 02 章给旋转指数，第 07 章才给 $e^{-iHt}$；“可观察量”“生成元”“Hamiltonian”之间缺少桥梁，对易/不对易只在 Trotter 例中出现。

**建议章位**：第 02 章旋转门之后或第 05 章前的短节。

**动作**：用 $H=\omega Z/2$ 推导相对相位随时间变化；用 $[X,Z]\ne0$ 解释测量兼容性和 Trotter 误差的共同来源。不要扩展到波函数或偏微分方程。

**验收**：第 07 章量子模拟不再是第一次见到 Hamiltonian 动力学。

### 9. 加入纯化与经典—量子态（P2）

**现状**：第 05 章有 Stinespring 与偏迹，但没有“任意混态可视为更大纯态的约化态”；Holevo 和测量记录也缺少经典—量子态表示。

**建议章位**：第 05 章密度矩阵之后、新量子信息章之前。

**动作**：

- 手算 $I/2$ 的 Bell 纯化；
- 定义 $\rho_{XA}=\sum_xp_x|x\rangle\langle x|\otimes\rho_A^x$；
- 用它统一“保留测量记录”和“丢弃记录”。

**权威基准**：[IBM, Purifications](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)（访问 2026-09-22）。

**验收**：读者能从纯化解释约化混态、环境记录和 Uhlmann 保真度的直觉。

### 10. 用态判别给迹距离操作意义（P2）

**建议章位**：新量子信息章。

**动作**：定义

$$
D(\rho,\sigma)=\frac12\|\rho-\sigma\|_1,
$$

再以等先验的 $|0\rangle$ 与 $|+\rangle$ 手算最优判别成功率。随后说明量子信道不会增加迹距离。

**权威基准**：[IBM, Quantum state discrimination and tomography](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/discrimination-and-tomography)（访问 2026-09-22）；[Fuchs–van de Graaf, 1999](https://doi.org/10.1109/18.761271)。

**验收**：读者能把“两个状态有多容易被实验区分”转换成数值和成功概率。

### 11. 用三个二级谱例子讲熵，不只给定义（P2）

**建议章位**：新量子信息章。

**动作**：计算

- $S(|0\rangle)=0$；
- $S(I/2)=1$ bit；
- $S(\operatorname{diag}(3/4,1/4))=h_2(1/4)$；
- Bell 纯态整体熵为 0、局部熵为 1。

配一张“纯度与熵不是同一量但方向相反”的 Bloch 球半径图。

**验收**：第 03 章的“纠缠熵 1 bit”能够回链到一般定义，不再是孤立公式。

### 12. 补条件熵、互信息与相对熵的最小闭环（P2）

**建议章位**：新量子信息章，熵之后。

**动作**：

- 先用经典联合分布复习 $I(X:Y)$；
- 再定义 $I(A:B)=S(A)+S(B)-S(AB)$；
- 比较 Bell 态与经典相关混态的互信息；
- 用 Bell 态说明量子条件熵可以为负，但不要把负条件熵解释成“负的不确定性”；
- 定义量子相对熵并只陈述其操作/比较意义，不在主线证明强次可加性。

**权威基准**：[Wilde, Quantum Information Theory course](https://www.markwilde.com/teaching/2021-fall-qit/)（课程 2021，页面最后更新 2022-01-30）；[Watrous TQI](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)（2018）。

**验收**：读者能分别解释“混合程度”“总关联”“可区分性”三种量为何不能互换。

### 13. 正面回答 Holevo 问题（P2）

**现状**：全书多次纠正“$n$ 个量子比特可读取 $2^n$ 个经典数”，但没有给出信息论上限。

**建议章位**：新量子信息章结尾，并回链第 00、04、12 章。

**动作**：

- 定义 ensemble、accessible information 与
  $$\chi=S(\sum_xp_x\rho_x)-\sum_xp_xS(\rho_x);$$
- 用两个正交态说明可取满 1 bit；用两个非正交态说明可访问信息严格受限；
- 说明超密编码为何不违反 Holevo：预共享纠缠改变了资源账本。

**权威来源**：[Holevo, 1973](https://www.mathnet.ru/eng/ppi/v9/i3/p3)；[Preskill 第 5 章](https://www.preskill.caltech.edu/ph229/notes/chap5.pdf)。

**验收**：第 00 章对“指数振幅不可全部读出”的纠正从口头边界升级为可计算上限。

### 14. 用数据处理不等式串联噪声、测量与安全（P2）

**建议章位**：新量子信息章末。

**动作**：以“不论做什么信道，都不能把两个输入态变得更容易区分”为直觉，分别陈述迹距离收缩、保真度单调和相对熵数据处理。配一张流程图：输入态 → 信道/测量 → 可区分性不增加。

**验收**：读者能用同一原则理解噪声、QKD 信息泄漏和错误校正恢复的限制。

### 15. 新增“量子通信复杂度”最小节（P2）

**建议章位**：第 04 章协议之后作直觉入口，在复杂度章节中正式展开。

**动作**：先定义 Alice/Bob 各持输入、允许共享随机性/纠缠、消息是 bit/qubit、轮数和错误率；再给一个受控例子。建议选：

- Equality 的通信模型作为定义例；
- 或 DISJOINTNESS 的经典随机与量子复杂度数量级作结果例，但明确模型和误差；
- 用传态、超密编码写资源不等式，而非只列“消耗几个 bit/qubit”。

**权威来源**：[Buhrman, Cleve, Massar, de Wolf, *Nonlocality and communication complexity*](https://doi.org/10.1103/RevModPhys.82.665), *RMP* 82, 665 (2010)；[MIT QIS Lecture 18](https://ocw.mit.edu/courses/mas-865j-quantum-information-science-spring-2006/a3023c8cf793563ba7f31391d5135711_lecture_18.pdf)（Spring 2006）。

**验收**：读者能区分“纠缠不能通信”与“纠缠可降低完成分布式任务所需通信量”。

### 16. 加入单比特层析完整手算与实验流程（P2）

**现状**：第 03 章只提“态层析”，没有解释怎样做。

**建议章位**：第 05 章或新量子信息章。

**动作**：给定多份同态，分别估计 $\langle X\rangle,\langle Y\rangle,\langle Z\rangle$，重构

$$
\rho=\frac12(I+xX+yY+zZ).
$$

用 $|+i\rangle$ 做理想数据，再加入有限 shots 导致的非物理 Bloch 向量，解释最大似然或物理约束的必要性。顺带区分 tomography 与单次态判别。

**权威基准**：[IBM, discrimination and tomography](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/discrimination-and-tomography)（访问 2026-09-22）。

**验收**：读者能写出三组测量、从频数算期望并重构 $2\times2$ 密度矩阵。

### 17. 调整算法顺序，并在 Simon 前补 $\mathbb F_2$（P2）

**现状**：现第 07 章先 Simon、后 Grover；Simon 需要二元线性方程与高斯消元，而正文数学章只在符号表定义 $\mathbb F_2$。

**建议动作**：

- 第 07 章先用已经在第 06 章手算过的 Grover 建立完整算法信心；
- 再补一页 $\mathbb F_2$ 加法、内积、秩和两方程消元；
- 然后讲 Simon，最后过渡到 Shor 的周期/Fourier 思想。

**验收**：Simon 三比特例中的每一步线性代数都能在前文找到定义或例题。

### 18. 把 HHL 明确标为进阶，并补一个 $2\times2$ 例子（P2）

**现状**：HHL 小节一次引入 Hermitian、稀疏访问、条件数、相位估计、受控旋转和后选择，没有数值例；对初学者明显比相邻章节更陡。

**建议章位**：保留现章但标“研究生选读”，或移至应用前的进阶框。

**动作**：取 $A=\operatorname{diag}(1,1/2)$、$|b\rangle=|+\rangle$，先经典算归一化的 $A^{-1}|b\rangle$，再说明算法各寄存器承担的任务；明确 $\kappa=2$。

**验收**：读者不依赖抽象谱式也能算出一个目标态，并说清为何输出不是经典向量。

### 19. 为高认知负荷步骤补“过程图”，而不是继续堆公式（P2）

**现状**：全书只有 6 个 Mermaid 图、1 张已嵌入 SVG；隐形传态、相位估计、QFT、条件/非选择测量和综合征提取没有正式电路或状态流程图。

**建议优先制作**：

1. 第 02 章：测量树——保留记录与丢弃记录；
2. 第 04 章：隐形传态完整电路与四分支修正；
3. 第 06 章：QPE“相位回踢 → 逆 QFT → 比特串”的三栏图；
4. 第 07 章：Grover 二维旋转几何；
5. 第 05 章：四类单比特噪声对 Bloch 球的作用。

**验收**：每张图都能脱离颜色阅读，符号与正文同端序，并在图注中指出读者要观察的关系。

### 20. 将 QEC 教学拆成核心层与进阶层，并真正使用综合征图（P2）

**现状**：第 10 章从三比特码迅速跳到 Knill–Laflamme、稳定子、Steane、表面码、Eastin–Knill 和魔法态；`qec-syndrome.svg` 已存在但未嵌入正文，也没有辅助量子比特如何测稳定子的线路。

**建议章位与动作**：

- 核心层：三比特码 → 相位码 → syndrome 不读逻辑信息 → 距离/阈值；
- 进阶层：Knill–Laflamme → 稳定子/CSS → 表面码 → 容错门；
- 在三比特码段嵌入现有 SVG；
- 再补一张“数据比特—辅助比特—测量”的稳定子提取电路，说明门故障为何会传播。

**验收**：只读核心层的读者能解释 QEC；读进阶层的读者不会把“直接测 $Z_1Z_2$”误解成必须破坏性测量两个数据位。

### 21. 统一“证据等级”，嵌入证据阶梯图（P2）

**现状**：第 08 章把证据分四级；`evidence-ladder.svg` 是五级；第 11 章又采用另一套设备/系统/应用/逻辑基准分类。图目前未嵌入。

**建议动作**：定义一套全书主轴，例如：理论提案 → 小规模正确性 → 可扩展趋势 → 逻辑可靠性 → 端到端实用优势。第 08/09/11/12 章使用同一套名字，再在各自领域添加子指标。

**验收**：同一案例在不同章节不会被分到不同数量、不同名称的等级；SVG 与正文逐项一致。

### 22. 每章增加“学习目标—核心/选读—前后导航”（P2）

**现状**：README 有全书路线，但单章没有预计先修、学习目标、核心/进阶标签、建议用时和下一步。

**建议动作**：每章标题后固定四行：

- 先修；
- 学完能完成的三个动作；
- 核心/研究生选读段落；
- 下一章与分支路线。

对第 09、10、12 章尤其重要，因为它们同时服务“了解全貌”和“进入研究”两种读者。

**教育依据**：QCTF 主张从目标技能与学习结果反推教学方法，而不是只按主题堆内容：[Goorney et al., 2024](https://doi.org/10.1088/1361-6404/ad7e60)。

**验收**：读者在打开任何单章时，不依赖 README 也知道该读哪些段、读完应会什么。

### 23. 练习从“章末问答”升级为三级练习体系（P2）

**建议章位**：所有章节与练习附录。

**动作**：

- A 级：概念辨析与一步计算；
- B 级：完整手算、证明或反例；
- C 级：小研究任务/复现实验；
- 答案分成“提示”“关键步骤”“完整解”，避免读者一跳转就看到最终答案；
- 至少 1/3 题跨章节，例如“用迹距离解释噪声后的判别概率”。

**课程基准**：Nielsen–Chuang 官方介绍强调数百道练习；MIT 18.435 公开多套作业与解答：[MIT Quantum Computation assignments](https://ocw.mit.edu/courses/18-435j-quantum-computation-fall-2003/pages/assignments/)（Fall 2003）。

**验收**：每章至少 2 道 A、2 道 B、1 道 C；题目与答案锚点自动对齐。

### 24. 加入三个累计式“纸笔 + 可选模拟”项目（P2）

**建议项目**：

1. **态与测量项目**：从 $X/Y/Z$ 频数重构单比特态，比较迹距离和保真度；
2. **算法项目**：对 Grover/QPE 同时统计 oracle、门数、深度和 shots，画资源曲线；
3. **论文复现项目**：复现一张公开论文或 QED-C 小基准图，记录版本、种子、编译设置和误差条。

项目应允许只用纸笔/矩阵计算完成核心部分，代码是验证而不是门槛。

**权威基准**：[MIT MAS.865 QIS lecture/project structure](https://ocw.mit.edu/courses/mas-865j-quantum-information-science-spring-2006/pages/lecture-notes/)（Spring 2006）；[QED-C application-oriented benchmarks](https://quantumconsortium.org/publication/application-oriented-performance-benchmarks-for-quantum-computing/)（2021）。

**验收**：每个项目都有问题定义、输入、基线、输出质量、失败概率、资源和复现清单。

### 25. 新增“怎样做一项量子计算研究”的方法论附录（P2）

**建议章位**：新增 `appendices/research-workflow.md`，第 11 章链接。

**最低流程**：

1. 把主题改写成可证伪问题；
2. 固定计算模型、输入分布、精度和资源边界；
3. 查原始论文、后续更正与强反例；
4. 先复算最小实例；
5. 再复现代码/实验；
6. 预先定义基线和统计方法；
7. 保存原始数据、版本、种子、编译结果和校准快照；
8. 分开报告复现、复制和外推；
9. 记录负结果与适用边界；
10. 写出别人怎样推翻自己的结论。

**权威依据**：[National Academies, *Reproducibility and Replicability in Science*](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science)（2019）；[npj Quantum Information reporting standards](https://www.nature.com/npjqi/editorial-policies/reporting-standards)（持续维护，访问 2026-09-22）；[ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)（现行政策，访问 2026-09-22）。

**验收**：读者可用模板审计一篇理论论文、一篇硬件论文和一篇变分算法论文，而非只得到抽象建议。

### 26. 降低黑话密度与“审稿腔”，保持人类叙事（P2）

**现状**

- 09 与 12 章各有 34 次“不是/不能/不等于/必须/至少/不要/容易”等限制词，11 章有 29 次；这些边界多数正确，但连续出现会让正文像合规清单。
- 术语表只有 24 个左右的核心词，而正文使用 `ansatz`、贫瘠高原、mixer、herald、QCCD、Rydberg、Majorana、Andreev、gadget、Pauli frame、格码手术、Fock、块编码和 qubitization 等大量未收录术语。
- 术语表“码距”条目中的 `(d)` 与 `(\lfloor...\rfloor)` 没有数学定界符，显示效果不一致；“相位回传”作为主词，而正文始终以“相位回踢”为主。

**建议动作**

- 段落顺序改为“它是什么 → 一个具体例子 → 为什么有用 → 边界”，把限制性句子集中到统一的“边界”框；
- 第一次出现英文术语时给一句白话，不要只给括号缩写；
- 扩充术语表并统一主译名；
- 删除模板化重复句，例如连续多次“不能自动推出”“必须同时说明”，改为指向一次定义好的证据框架。

**验收**：任一段最多承担一个主要反例；每个专业缩写在首次出现处和术语表都有定义；随机请一名跨学科初学者复述段意，不依赖外部搜索。

## 五、P3：核心主线稳定后加入的四项

### 27. 信道表示、压缩与容量的进阶入口（P3）

在第 05/新信息论章的研究生选读中，加入 Choi 矩阵、Pauli transfer matrix、Schumacher 压缩和“经典容量/量子容量是不同问题”的地图。主线只需一个 qubit source 的压缩直觉，不应直接展开完整编码定理。

来源：[Schumacher, *Quantum coding*](https://doi.org/10.1103/PhysRevA.51.2738), *PRA* 51, 2738 (1995)；[Preskill Physics 219 course page](https://preskill.caltech.edu/ph229/index.html)（含 2025 Quantum Shannon Theory 讲义，访问 2026-09-22）。

### 28. 混态纠缠与 LOCC 的进阶入口（P3）

第 03 章已提醒“混态不能只看是否一个乘积”，但没有给可分混态、PPT 判据或 LOCC 的最小例子。可加入 Bell-diagonal 两比特例和一个纠缠见证，明确这不是完整混态纠缠理论。

来源：[Watrous TQI lecture notes](https://cs.uwaterloo.ca/~watrous/TQI-notes/)（含 separable operators、LOCC、partial transpose；官方页面访问 2026-09-22）。

### 29. 另列“算法模型地图”，不塞入核心算法章（P3）

可用一页对照门模型、测量驱动、绝热/退火、量子随机游走和模拟量子模拟器，说明它们的输入、控制与复杂度保证不同。正文第 12 章已有边界说明，但缺少一张正面比较表。不要在核心主线逐个展开算法。

### 30. 将易变里程碑移到独立版本化附录（P3）

第 09 与第 12 章的 2025–2026 里程碑很有事实核查价值，但会迅速老化并打断概念主线。建议正文保留“如何核查”，把具体纪录移至 `appendices/current-landscape.md`，逐条记录访问日期、来源状态、勘误和下次复核日期。

**验收**：稳定教材章节即使一年未更新仍成立；动态附录可独立替换而不改变概念章节分页和练习编号。

## 六、推荐的全书知识架构

### 6.1 最小改动版

不大幅改编号时，可以这样处理：

1. 第 01 章补概率统计、SVD 和条件数；
2. 第 02 章只保留纯态投影测量，把 POVM/非选择测量后移；
3. 第 05 章改成“密度矩阵 → 一般测量 → 信道 → 噪声 → 态距离”的顺序；
4. 在第 05 与第 06 之间增加“量子信息论桥接章”；
5. 第 07 章复杂度节前加问题模型与归约；
6. 第 04 与第 07 章分别加入通信复杂度直觉和正式模型；
7. 第 11 章链接新的研究工作流附录；
8. 先修复练习附录 0–3 章，再扩充新题。

### 6.2 理想重构版

| 阶段 | 章节 | 目标 |
|---|---|---|
| A 直觉与数学 | 00 全景；01 数学、概率与计算模型 | 建立共同语言，不先堆术语 |
| B 纯态主线 | 02 单比特；03 多比特与纠缠；04 门与协议 | 会手算纯态、电路、测量和资源账本 |
| C 一般量子信息 | 05 密度矩阵、测量与信道；06 距离、熵、互信息与 Holevo | 把混态、噪声、通信与信息极限连成一体 |
| D 算法与复杂度 | 07 算法骨架；08 代表算法；09 复杂度与通信复杂度 | 从“线路会运行”进到“资源优势在什么模型成立” |
| E 应用与系统 | 10 应用；11 硬件；12 QEC；13 资源与基准 | 理论、物理、纠错与端到端成本闭环 |
| F 安全与研究 | 14 安全、网络与前沿；研究方法附录 | 能读论文、复现结果和判断前沿主张 |

### 6.3 两条阅读轨道

- **零基础核心轨**：00–06 → Grover/QPE/Shor 的核心段 → 硬件概览 → 三比特码/阈值 → 资源清单。
- **入门研究生轨**：核心轨全部 + 相对熵/Holevo + 复杂度/通信复杂度 + 稳定子/容错 + 研究复现项目。

章节内用“核心”“研究生选读”标签，比把所有内容写成同一难度更适合当前混合受众。

## 七、建议新增的手算例、直觉与图

| 位置 | 手算或图 | 教学目的 |
|---|---|---|
| 01 | 条件概率表、二项方差 | 为 shots、置信区间、后选择打基础 |
| 01/03 | $2\times2$ SVD → Schmidt | 消除 Schmidt 分解的突然性 |
| 02 | 测量分支树 | 区分条件态与非选择态 |
| 04 | 隐形传态线路和四分支表 | 把长恒等式变成可追踪流程 |
| 05 | Bloch 球上的去极化/退相位/阻尼 | 让四个信道具有几何直觉 |
| 新 06 | $|0\rangle$ vs $|+\rangle$ 的 Helstrom 判别 | 给迹距离操作意义 |
| 新 06 | Bell 态与经典相关态的 $S,I(A:B)$ 对照表 | 区分纠缠、混合和总关联 |
| 新 06 | Holevo 的“编码—测量—经典变量”图 | 回答指数振幅为何不可全部读出 |
| 07 | QPE 三栏流程/标准线路 | 连接受控幂、逆 QFT 与输出 |
| 08 | Grover 二维旋转 | 解释过度旋转 |
| 08 | HHL 的 $2\times2$ 对角例 | 降低抽象谱式门槛 |
| 10/12 | 辅助比特稳定子测量线路 | 说明综合征如何“不读逻辑态” |
| 11/13 | 五级证据阶梯 SVG | 统一全书证据语言 |

## 八、权威来源与采用理由

以下来源均为原始论文、出版社页面、作者/大学官方课程或正式研究规范。动态网页统一记录访问日期 **2026-09-22**。

1. Michael Nielsen and Isaac Chuang, [*Quantum Computation and Quantum Information*](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE), 10th Anniversary Edition, Cambridge University Press, 2010/2011。用于校准“基础数学—电路—算法—信息论—纠错”的完整范围和练习密度。
2. John Watrous, [*Basics of Quantum Information*](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)，IBM Quantum Learning，持续维护。用于校准初学者纯态、电路和纠缠协议的顺序。
3. John Watrous, [*General Formulation of Quantum Information*](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information)，IBM Quantum Learning，持续维护。用于校准密度矩阵、信道、一般测量与状态距离的顺序。
4. John Watrous, [*The Theory of Quantum Information*](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf), Cambridge University Press, 2018。用于校准纯化、判别、保真度、熵、相对熵和信道距离的研究生核心范围。
5. John Preskill, [Physics 219 / Computer Science 219 Quantum Computation](https://preskill.caltech.edu/ph229/index.html)，Caltech 官方课程页，含更新至 2025–2026 的章节入口。用于校准量子基础、信息论、复杂度和纠错之间的桥接。
6. John Preskill, [Chapter 5: Quantum Information Theory](https://www.preskill.caltech.edu/ph229/notes/chap5.pdf)，官方讲义。用于熵、Holevo 信息、纠缠和通信主线。
7. Mark M. Wilde, [Quantum Information Theory course](https://www.markwilde.com/teaching/2021-fall-qit/)，Fall 2021，页面最后更新 2022-01-30。用于熵、信息量、数据处理、保真度和课程项目结构。
8. John Watrous, [Quantum Computational Complexity](https://cs.uwaterloo.ca/~watrous/Papers/QuantumComputationalComplexity.pdf), 2008。用于计算问题、资源模型、BQP/QMA/QIP 的严谨入口。
9. John Watrous, [Quantum Computation lecture notes](https://cs.uwaterloo.ca/~watrous/QC-notes/QC-notes.pdf), 2006。用于 promise problem、通信复杂度和本科入门顺序。
10. Harry Buhrman, Richard Cleve, Serge Massar, Ronald de Wolf, [Nonlocality and communication complexity](https://doi.org/10.1103/RevModPhys.82.665), *Reviews of Modern Physics* 82, 665–698 (2010)。用于通信复杂度模型与量子资源边界。
11. MIT OpenCourseWare, [MAS.865J Quantum Information Science lecture notes](https://ocw.mit.edu/courses/mas-865j-quantum-information-science-spring-2006/pages/lecture-notes/), Spring 2006。用于项目制教学、通信复杂度、信道容量和 QEC 的进阶顺序。
12. MIT OpenCourseWare, [18.435J Quantum Computation assignments](https://ocw.mit.edu/courses/18-435j-quantum-computation-fall-2003/pages/assignments/), Fall 2003。用于分层练习与答案组织。
13. Simon Goorney et al., [A framework for curriculum transformation in quantum information science and technology education](https://doi.org/10.1088/1361-6404/ad7e60), *European Journal of Physics* 45, 065702 (2024-10-28)。用于学习目标—技能—教学方法对齐。
14. Josephine Meyer et al., [Today’s interdisciplinary quantum information classroom](https://doi.org/10.1103/PhysRevPhysEducRes.18.010150), *Physical Review Physics Education Research* 18, 010150 (2022-06-30)。用于跨物理、计算机和工程背景的受众设计。
15. Christopher Fuchs and Jeroen van de Graaf, [Cryptographic Distinguishability Measures for Quantum-Mechanical States](https://doi.org/10.1109/18.761271), *IEEE Transactions on Information Theory* 45, 1216–1227 (1999)。用于迹距离—保真度关系。
16. Alexander Holevo, [Bounds for the Quantity of Information Transmitted by a Quantum Communication Channel](https://www.mathnet.ru/eng/ppi/v9/i3/p3), *Problems of Information Transmission* 9, 177–183 (1973)。用于 Holevo 界原始来源。
17. Benjamin Schumacher, [Quantum coding](https://doi.org/10.1103/PhysRevA.51.2738), *Physical Review A* 51, 2738–2747 (1995-04-01)。用于量子源编码和熵的操作意义。
18. National Academies, [*Reproducibility and Replicability in Science*](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science), 2019。用于区分复现与复制并建立研究工作流。
19. [npj Quantum Information reporting standards](https://www.nature.com/npjqi/editorial-policies/reporting-standards)，持续维护。用于数据、代码、算法、协议和可用性声明。
20. ACM, [Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)，现行政策。用于“可获得、可运行、可复用、结果被独立复算”的分级。
21. QED-C, [Application-oriented performance benchmarks for quantum computing](https://quantumconsortium.org/publication/application-oriented-performance-benchmarks-for-quantum-computing/), 2021。用于项目型复现与质量—时间—规模曲线。

## 九、建议实施顺序

### 第一批：阻断错误学习

1. 修复练习附录 0–3 章与审校记录；
2. 调整密度矩阵/POVM 的首次出现顺序；
3. 在第 05 章正式定义保真度和迹距离；
4. 为复杂度类补问题模型、promise 和归约。

### 第二批：补齐知识脊梁

5. 新增量子信息论桥接章；
6. 补概率统计、SVD、纯化、层析；
7. 加通信复杂度；
8. 调整 Simon/HHL 的难度坡度。

### 第三批：改善学习体验

9. 嵌入两张未使用 SVG，并统一证据等级；
10. 补测量、传态、QPE、Grover、噪声和综合征图；
11. 增加章节目标、核心/选读标签和三级练习；
12. 重写 09–12 的部分段落，使“正面解释”先于“边界清单”。

### 第四批：建立研究入口

13. 增加三个累计项目；
14. 新增研究工作流与复现模板；
15. 再按受众需要加入信道容量、混态纠缠和其他计算模型的 P3 扩展。

## 十、最终判断

当前手册已经是一套事实边界严谨、公式总体可靠、覆盖面很广的量子计算入门骨架，但还不是“量子计算与量子信息”完整研究入口。最关键的工作不是继续横向增加新硬件名词，而是：

1. 修复自检答案闭环；
2. 让密度矩阵和一般测量按认知顺序出现；
3. 补齐状态距离、保真度、熵、互信息、相对熵和 Holevo；
4. 补齐计算复杂度与通信复杂度的基本模型；
5. 把第 11 章的审稿清单升级为可执行的研究与复现方法。

完成这五项后，读者才能从“会算几个电路、会识别夸大宣传”稳定过渡到“会使用量子信息的数学语言、会判断复杂度声明、会独立复算一项研究结果”。
