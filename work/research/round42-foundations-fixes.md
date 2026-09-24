# 第 42 轮：先修与基础推导修订

依据 `round41-foundations-audit.md` 修订了五个授权文件，未改 `sources/`，也未改第 06 章或既有自检题号。

| 审稿问题 | 本轮改动 | 条件和核对 |
|---|---|---|
| 第 15 章代码所需准备不明 | `handbook/appendices/prerequisites.md:16–18` 加一条**可选** Python/NumPy 动手路线，仍明确编程不是前五章的理论先修。 | [NumPy 官方初学者教程](https://numpy.org/doc/stable/user/absolute_beginners)核对术语和建议入口。 |
| Bloch 球坐标直接给结论 | `handbook/02-single-qubit.md:89` 起从 $\alpha,\beta$ 与 $X,Y,Z$ 矩阵逐项推出 $r_x,r_y,r_z$；用 $\sqrt3|0\rangle/2+i|1\rangle/2$ 算出 $(0,\sqrt3/2,1/2)$ 和 $Y$ 的 $+1$ 概率；用 $R_y$ 再检查半角。 | 对照 [IBM Bloch 球课程](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere)。数值：向量范数平方 1，$p_Y(+)=0.9330127019$。 |
| Q4 用 $[\hat x,\hat p]$ 前无推导 | `handbook/quantum-mechanics/04-wavefunctions-models.md:46` 起对试探函数分别算 $\hat x\hat pf$、$\hat p\hat xf$，用乘积法则得到 $i\hbar f$；注明共同作用域。第 5 节回指第 2 节。 | 与[MIT 8.04 位置表示到谐振子的课程序列](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/)一致；没有把无界算符的形式式子推广到任意函数。 |
| CHSH 两个界缺少算例 | `handbook/03-multiple-qubits.md:218` 起分别演算经典每次 $s=\pm2$ 和 Bell 态上四种量子相关值，表中代入得到 $2\sqrt2$；说明四组实验需多轮制备。 | 独立数值为 $2.8284271247461903$；与 [IBM CHSH 教学](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game)和[原论文](https://doi.org/10.1103/PhysRevLett.23.880)核对。 |
| 传态四分支的关键等式跳步 | `handbook/04-circuits-protocols.md:124` 起从 $QAB$ 初态四项展开，写出 CNOT 后四项与 $H_Q$ 后的 `00/01/10/11` 分支表；逐行给 Bob 条件态和校正门。 | 以 $\alpha=0.6,\beta=0.8$ 的独立三比特数组演算，四行未归一化振幅依次为 `(0.3,0.4),(0.4,0.3),(0.3,-0.4),(-0.4,0.3)`，各概率恰为 0.25；与[Bennett 等原始传态方案](https://doi.org/10.1103/PhysRevLett.70.1895)对照。 |
| 非最大纠缠态的熵无数字 | `handbook/03-multiple-qubits.md:174` 用正文已有的权重 $3/4,1/4$ 得 $0.8112781244591328$ bit；明确混态不能直接以局部熵度量纠缠。 | 公式与 [IBM Schmidt 分解教程](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)的权重定义一致。 |

独立计算另核对了 Bell 态上 $E_{00}=E_{01}=E_{10}=+1/\sqrt2,E_{11}=-1/\sqrt2$；Bob 最后一分支用 $ZX$ 校正后精确回到 $|\psi\rangle$，用 $XZ$ 则仅差共同负号。`node tools/reader/check-qm-examples.mjs` 与 `check-qm-review.mjs` 均通过，后者仍为 181 题、181 答。全站 HTML 公式与桌面/手机渲染由主任务最终构建验证；本报告不替代该视觉复核。
