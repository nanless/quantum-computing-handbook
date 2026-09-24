# 第 41 轮只读审稿：算法、应用、复杂性、网络与信息

审稿范围：`handbook/06-algorithmic-primitives.md`、`07-algorithms.md`、`08-applications.md`、`11-resources-benchmarks.md`、`12-security-network-frontiers.md`、`16-advanced-algorithms-verification.md`、`17-computation-models.md`、`18-channels-capacities-complexity.md`，以及相应 `appendices/exercises.md` 答案、`appendices/glossary.md` 术语。只读核查；未改正文，未碰 `sources/`。

## 结论与分级

- **P0（会导致核心结论错误）：未发现。**
- **P1（明确事实或计算错误、足以误导后续推导）：未发现。**
- **P2（在现有正确结论之前存在可修补的跳步或成本边界表达不足）：5 项。**
- **可选扩展：2 项。**

“未发现”仅指本次列出的章节和逐式核查范围，不代表完整学科内容已经穷尽。下面的 P2 都有明确修复位置和算例，适合下一轮正文改进。

## P2-1：擦除信道的量子容量算例少了“对所有输入最优化”的关键一行

位置：`handbook/18-channels-capacities-complexity.md` 第 4.5 节，“量子容量”段。现文只对最大混合输入 `I/2` 算得 `I_c=1-2ε`，随后直接给出完整容量 `max(0,1-2ε)`。现文引用可降解/反降解性质，结论正确，但初学者容易把“一个输入取得这个值”当成“已证明没有其他输入更好”。同节纠缠辅助容量反倒完整写出了任意输入态的最优化，形成讲解深度不一致。

可执行修复：补一句对任意 qubit 输入 `ρ` 的正交旗标熵计算：`S(B)=h₂(ε)+(1-ε)S(ρ)`，`S(RB)=h₂(ε)+εS(ρ)`，因此 `I_c(ρ, E_ε)=(1-2ε)S(ρ)`。当 `ε≤1/2` 时由 `S(ρ)≤1` 知 `I/2` 最优，再用可降解信道的单字母容量定理；当 `ε≥1/2` 时说明反降解导致零容量。若想顺手增强私密容量段，也可写明这里使用的是同一可降解信道的私密容量定理，而不仅是展示一个正交态编码的可达率。

依据：[Bennett、DiVincenzo、Smolin 的原始擦除信道容量论文](https://arxiv.org/abs/quant-ph/9701015)；[Devetak 的私密/量子容量原论文](https://arxiv.org/abs/quant-ph/0304127)。

## P2-2：量子指纹的纠错码存在性与“上界也要限制”只给结论，没有最小构造直觉

位置：`handbook/18-channels-capacities-complexity.md` 第 7.1 节。现文正确要求任意不同码字的距离同时满足 `δ≤Δ≤1−δ`，因为相位指纹内积是 `1−2Δ`。但“取一个长度 `m=O(n)` 的二元码”紧接着进入公式，未向初学者说明：为什么可以同时要求指数多个码字彼此既不太近也不近乎互补？这与普通课本只保证**最小**距离的纠错码要求不同。

可执行修复：加一个两三句的存在性说明：随机选取长度 `m=c n` 的码字时，任意给定一对的距离集中在 `m/2` 附近；令常数 `c` 足够大后，对至多 `2^{2n}` 对码字应用并合界，仍可使所有不同对落在如 `[m/4,3m/4]` 内。明确这只是存在性直觉，不自动给高效编码电路；然后给一个 `Δ=1/2` 时内积为零、`Δ≈1` 时内积反而接近 `−1` 的两行比较。图中的 `O(log n)` 通信也依赖编码可高效计算，不能只从存在性推出实现时间。

依据：[Buhrman、Cleve、Watrous、de Wolf 的量子指纹原论文](https://arxiv.org/abs/quant-ph/0102001)；[Watrous 保存的作者论文 PDF](https://jhwatrous.github.io/BuhrmanCleveWatrousdeWolf2001.pdf)明确给出双侧距离的概率性存在论证。

## P2-3：量子行走搜索的成本式突然出现，未给读者可代入的小数值例

位置：`handbook/16-advanced-algorithms-verification.md` 第 4.2 节。四环 coined walk 有逐态展开，接着立刻给 `S+ε^{-1/2}(U/√δ+C)`。虽然各字母定义了，但这里的 `δ` 是**经典 Markov 链谱隙**，与第 6/12/17 章的失败概率/精度 `δ` 语境不同；读者也看不出 `S,U,C` 如何决定“比 Grover 好”。

可执行修复：先用一句话说明这里重新使用 `δ`，仅指对应可逆经典链的谱隙，不是测量失败概率。补一个明确标成“代入练习、非特定硬件”的例子：若 `ε=1/16, δ=1/4, S=10, U=2, C=3`，框架给出的成本尺度为 `10+4(2/(1/2)+3)=38` 个抽象单位；再说明这些单位在算法具体实现中才可比较，不能把结果直接当作物理门数。若要体现结构收益，拿相同输入规模的检查/更新成本作一行对比。

依据：[Magniez、Nayak、Roland、Santha 的量子行走搜索原论文](https://arxiv.org/abs/quant-ph/0608026)。

## P2-4：Shor 小例中的“尝试分母的小倍数”应标明只是局部补救，不能作为一般恢复保证

位置：`handbook/07-algorithms.md` 第 3.3、3.4 节。两处给 `k/r` 约分后可检查候选分母的小倍数，15 和 35 的例子恰好只需乘 2。正文随后也写了重采样/合并样本，故不是错误；但当前叙事可能让初学者把“找小倍数”记成普遍高效的 Shor 后处理。

可执行修复：在第二个例子 `2×6=12` 后添一句：这些数字小，倍数检查是演示办法；一般情形丢失的因子 `gcd(k,r)` 未必小，不能把无上界的倍数枚举计入多项式时间保证。正式论证依赖足够精度的 Fourier 采样、模幂验证及受控次数的重试/候选合并。练习答案第 7 章第 4 题可同样补半句。

依据：[Shor 原论文](https://doi.org/10.1137/S0097539795293172)；[IBM Quantum 的相位估计与分解课程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/introduction)。

## P2-5：第 6 章首次使用异或符号时没有当场解释

位置：`handbook/06-algorithmic-primitives.md` 第 1 节，第一次写 `U_f|x⟩|y⟩=|x⟩|y⊕f(x)⟩` 的前后。审稿再查第 00–05 章，未找到 `⊕` 或“异或”的先行文字定义；符号附录虽有解释，读者到此可能已停在第一条 oracle 公式上。这是教学跳步，不是公式错误。

可执行修复：在公式前就解释“`⊕` 是模 2 加法（异或），相同得 0、不同得 1”，给出两行小真值表：`y=0` 时 `y⊕f=f`，`y=1` 时 `y⊕f=1−f`；或列出 `0⊕0=0, 0⊕1=1, 1⊕0=1, 1⊕1=0`。紧接着给一个真正非单射的最小例：取常值函数 `f(0)=f(1)=1`，天真单寄存器映射会把正交的 `|0⟩,|1⟩` 都变成 `|1⟩`，不可能酉；保留 `x` 的两个寄存器版本却把 `|0,0⟩→|0,1⟩`、`|1,0⟩→|1,1⟩`，仍为正交态，且再次施加 `U_f` 即还原输入。这比现文只写抽象 `f(0)=f(1)` 更容易让初学者看见为什么要额外保留 `x`。

依据：[IBM Quantum Learning 的量子查询算法课程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/introduction)以 oracle 模型引出 Deutsch 类算法；此项主要是对本书实际阅读顺序的内部教学审查。

## 可选扩展

1. `handbook/16-advanced-algorithms-verification.md` 第 5.4 节的 `cos θ_λ=λ/α` 已注明约定依赖，但可借第 5.5 节的 `W(x)` 直接写 `x±i√(1−x²)=e^{±i arccos x}`，把 qubitization 的“值变相位”与下一节二阶 Chebyshev 算例接起来。依据：[Low、Chuang 的 qubitization 原论文](https://quantum-journal.org/papers/q-2019-07-12-163/)。
2. `handbook/12-security-network-frontiers.md` 第 2.2 节的 NIST 状态截至 2026-09-22 写法已核对，现时仍是 ML-KEM/ML-DSA/SLH-DSA 三项 2024 最终 FIPS，HQC 2025 被选择用于后续标准化。此节时间敏感，下一次更新时重新核对 NIST 而不要把本轮“无误”当成长期事实。依据：[NIST PQC 标准化项目页](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post_Quantum_Cryptography-Standardization)。

## 逐式复核抽样

- `06`：Grover 二维反射矩阵、QPE `φ=1/3,M=4` 的四项分布和最近格点 `4/π²` 下界；式子与边界条件一致。
- `07`：Simon `s=110` 的 Hadamard 支持集和满秩期望 `10/3`；Shor 的 `N=15`、`N=35` 模周期、`171/2048` 连分数与 `≈0.684` QPE 概率；`X+Z` 的交换子范数、`r=20` 预算；HHL 二维归一化；未发现算术偏差。
- `08`：VQE 最优值 `−√0.53`、独立分组 shots 的 `7:2` 分配及 `7780` 规划数；单边和三点路径的 QAOA 角度/期望均按正文符号约定自洽。
- `11`：`d=17`、旋转表面码裸补丁 `577`、100 数据补丁 `57,700`、20 kW 能耗算例无算术偏差；示意假设有标识。
- `12`：BB84 全截获重发时筛后 QBER `1/4`；两段链路 `E[max]≈14.74`、`E|X−Y|≈9.47` 和相干因子 `≈0.679`；Bell 交换四结果与 Pauli 修正一致。
- `16–18`：QSP 两次信号调用产生 `T₂(x)`；MBQC `J(−α)X=ZJ(α)`；八位唯一目标 Grover 第 12/13 次概率分别约 `0.999947/0.986186`；qubit 擦除信道四容量、量子指纹 swap-test `5/8` 与 `10` 次误报约 `0.0091`；均无明显算式错误。

本轮只做文本、公式、出处和 Mermaid **语义**审查；没有替代整站在宽屏/手机上的实际渲染检查。图形方面未发现会改变科学含义的箭头错误，但排版美观须由渲染截图单独确认。
