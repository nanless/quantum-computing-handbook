# 第 42 轮算法与信息章节修订记录

依据第 41 轮只读报告 `work/research/round41-algorithms-audit.md`，本轮只修改第 06、07、16、18 章及第 07 章相应练习答案；未改其他正文、先修页或 `sources/`。

| 第 41 轮问题 | 本轮落点 | 实施内容 |
|---|---|---|
| P2-5，异或首次出现未就地解释 | `handbook/06-algorithmic-primitives.md` 第 1 节 | 给出模 2 加法四行真值表；以常值 `f(0)=f(1)=1` 对比错误的单寄存器合并与正确的双寄存器正交输出；指出 `U_f^2=I`。 |
| P2-4，Shor 小倍数检查边界 | `handbook/07-algorithms.md` 第 3.3 节，`appendices/exercises.md` 第 7 章第 4 答 | 明确 `2×2=4` 只是小数算例；一般丢失因子 `gcd(k,r)` 可大，不能把无上界倍数枚举当作多项式后处理。 |
| P2-3，量子行走成本式跳步 | `handbook/16-advanced-algorithms-verification.md` 第 4.2 节 | 用 `δ_walk` 明确经典链谱隙，区别失败概率；带入 `ε=1/16,δ_walk=1/4,S=10,U=2,C=3` 算得 38，并把 `U` 改为 20 算得 182；说明抽象单位不可直接与门数比。 |
| 可选，相位桥 | 同章第 5.5 节 | 由二维信号酉的本征值 `x±i√(1−x²)=e^{±i arccos x}` 接到 qubitization 相位关系，同时保留反射次序的约定警告。 |
| P2-1，擦除信道未完成最优化步骤 | `handbook/18-channels-capacities-complexity.md` 第 4.5 节 | 对任意输入 `ρ` 计算 `S(B)=h₂(ε)+(1−ε)S(ρ)`、`S(RB)=h₂(ε)+εS(ρ)`，从而 `I_c=(1−2ε)S(ρ)`；对 `ε≤1/2` 由 `S(ρ)≤1` 证明最大混合输入最优，随后明确调用可降解定理；反降解区给零容量。 |
| P2-2，指纹双侧距离缺存在性 | 同章第 7.1 节 | 用随机长度 `m` 码字和集中界给出单对偏离概率 `≤2e^(−m/8)`，对 `<2^(2n−1)` 对作并合界，说明 `m=O(n)` 足以使所有对满足 `[1/4,3/4]`；对比 `Δ=1/2` 内积 0 与 `Δ=1` 内积 −1，解释上界不可省略；区分存在性、编码时间和通信计费。 |

## 独立复核

- oracle 真值表四行互异情形正确；对固定 `x`，`y↦y⊕f(x)` 是自身的逆，因此全映射也是置换。
- 量子行走代入：`1/√(1/16)=4`、`2/√(1/4)=4`，所以 `10+4(4+3)=38`；`U=20` 时 `10+4(40+3)=182`。
- 指纹随机码：若每个码字各位独立均匀，单对距离是 `Binomial(m,1/2)`，Hoeffding 界为 `Pr(|Δ−1/2|≥1/4)≤2exp(−m/8)`。至多 `2^(2n−1)` 个无序输入对，整体坏事件概率小于 `2^(2n)exp(−m/8)`；故 `m>16n ln2` 再留正余量便可使它小于 1。此论证只说明存在，不保证所选随机码有低成本编码实现。
- 擦除信道：`S(RB)` 中未擦除分支的参考—输出态仍纯、熵为 0；擦除分支只剩参考态，熵 `S(ρ)`；两分支旗标正交，故有二元熵加权和。`ε=1/4`、`ρ=I/2` 得 `I_c=1/2`，与原例数值一致。
- 二维信号酉 `W(x)=xI+i√(1−x²)X`，其本征值由 `X` 的 `±1` 本征值立即给出 `x±i√(1−x²)`，模长均为 1。

## 一手来源

- [IBM Quantum Learning：量子查询算法](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/introduction)：可逆查询模型与 Deutsch/Simon 算法教学入口。
- [Shor 原论文](https://doi.org/10.1137/S0097539795293172)：阶寻找和经典有理数恢复的原始复杂度背景。
- [Magniez 等：Search via Quantum Walk](https://arxiv.org/abs/quant-ph/0608026)：可逆 Markov 链的设置、更新、检查成本框架。
- [Low、Chuang：Hamiltonian Simulation by Qubitization](https://quantum-journal.org/papers/q-2019-07-12-163/)：归一化本征值与二维 walk 相位的关系。
- [Bennett、DiVincenzo、Smolin：Capacities of Quantum Erasure Channels](https://arxiv.org/abs/quant-ph/9701015)：擦除信道容量。
- [Devetak：private classical and quantum capacity](https://arxiv.org/abs/quant-ph/0304127)：可降解情形的私密与量子容量背景。
- [Buhrman 等：Quantum Fingerprinting](https://arxiv.org/abs/quant-ph/0102001)：双侧码距、相位指纹和 swap test 的原始方案。

本记录是内容修订与局部算术复核，不替代完整读者网页的公式渲染、链接、窄屏表格和视觉检查；那些检查由总览工作流统一执行。
