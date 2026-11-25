# 自检题参考解答（全书 26 章 271 题 V4 分级零跳步版）

本附录汇集全书 **26 章（主篇第 00–21 章 + 物理篇 Q1–Q4）全部 271 道章末自检题**的 V4 零跳步参考解答，并针对 6 个薄弱或高密度章节增补 **14 道独立标签盲区精练**（`练 00-C/D`、`练 05-C/D`、`练 13-C/D/E`、`练 14-C/D/E`、`练 Q2-C/D`、`练 Q3-C/D`）。每道题统一采用“**难度徽章（`【基础】`/`【计算】`/`【进阶】`）+ 防剧透核心提示 + 四步零跳步全解**（题意与约定 → 核心提示 → 完整分步演算 → 结论与边界回验 → 易错坑提醒）”结构：卡在思路时可先看「核心提示」自行推进，再核对完整推导。既有 271 道自检题号、所属章节与锚点保持 100% 稳定；在 Web 阅读版中，每章末尾同样提供自动按题折叠的本章解答面板。

## 五篇 26 章自检题速查与难度分布目录

全书正文章节按五篇教学主序编排；本附录各章解答保留既有 `## 第 N 章` / `## 量子力学 QN` 标题与顺序以维持全书交叉链接与锚点 100% 稳定。下表按五篇学习主序汇总每章自检题数、难度分级统计（`【基础】` / `【计算】` / `【进阶】`）与本附录盲区增补精练，方便按学习路径直达。

| 所属篇目 | 章节正文 | 解答锚点 | 自检题数 | 基础 / 计算 / 进阶 | 附录盲区增补 |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **第一篇 · 入门、数学与量子态基础** | [第 0 章｜全景导览](../00-overview.md) | [直达解答](#第-0-章) | 6 | 4 / 2 / 0 | 练 00-C/D |
| 〃 | [第 1 章｜零基础数学工具](../01-math.md) | [直达解答](#第-1-章) | 14 | 6 / 8 / 0 | — |
| 〃 | [量子力学 Q1｜从实验认识量子态](../quantum-mechanics/01-experiments-states.md) | [直达解答](#量子力学-q1) | 7 | 3 / 4 / 0 | — |
| 〃 | [第 2 章｜单量子比特](../02-single-qubit.md) | [直达解答](#第-2-章) | 11 | 5 / 6 / 0 | — |
| 〃 | [量子力学 Q2｜可观测量与时间演化](../quantum-mechanics/02-observables-dynamics.md) | [直达解答](#量子力学-q2) | 8 | 1 / 4 / 3 | 练 Q2-C/D |
| 〃 | [第 3 章｜多量子比特与纠缠](../03-multiple-qubits.md) | [直达解答](#第-3-章) | 11 | 4 / 5 / 2 | — |
| 〃 | [第 4 章｜量子门、电路与基础协议](../04-circuits-protocols.md) | [直达解答](#第-4-章) | 9 | 2 / 5 / 2 | — |
| 〃 | [第 5 章｜混态、噪声与量子信道](../05-noise-channels.md) | [直达解答](#第-5-章) | 8 | 3 / 4 / 1 | 练 05-C/D |
| **第二篇 · 核心算法、应用与实验实践** | [第 6 章｜量子算法的共同骨架](../06-algorithmic-primitives.md) | [直达解答](#第-6-章) | 14 | 6 / 5 / 3 | — |
| 〃 | [第 7 章｜代表性量子算法](../07-algorithms.md) | [直达解答](#第-7-章) | 15 | 6 / 6 / 3 | — |
| 〃 | [第 8 章｜应用、变分算法与证据边界](../08-applications.md) | [直达解答](#第-8-章) | 15 | 6 / 7 / 2 | — |
| 〃 | [第 15 章｜实践路线与论文复核](../15-practice-research.md) | [直达解答](#第-15-章) | 8 | 4 / 3 / 1 | — |
| **第三篇 · 物理硬件、编译、纠错与系统工程** | [量子力学 Q3｜从能级到物理量子比特](../quantum-mechanics/03-levels-control.md) | [直达解答](#量子力学-q3) | 8 | 3 / 5 / 0 | 练 Q3-C/D |
| 〃 | [第 9 章｜主流硬件平台与物理噪声](../09-hardware.md) | [直达解答](#第-9-章) | 11 | 6 / 5 / 0 | — |
| 〃 | [第 14 章｜编译、调度与物理控制](../14-compilation-control.md) | [直达解答](#第-14-章) | 8 | 3 / 4 / 1 | 练 14-C/D/E |
| 〃 | [第 10 章｜量子纠错与容错计算](../10-error-correction.md) | [直达解答](#第-10-章) | 10 | 6 / 3 / 1 | — |
| 〃 | [第 11 章｜基准测试与容错资源估算](../11-resources-benchmarks.md) | [直达解答](#第-11-章) | 9 | 5 / 4 / 0 | — |
| 〃 | [第 19 章｜可维护量子系统工程](../19-engineering-architecture.md) | [直达解答](#第-19-章) | 12 | 7 / 4 / 1 | — |
| **第四篇 · 密码、网络与精密测量** | [第 12 章｜量子密码、后量子与网络](../12-security-network-frontiers.md) | [直达解答](#第-12-章) | 17 | 7 / 9 / 1 | — |
| 〃 | [第 20 章｜量子传感与精密测量](../20-quantum-sensing-metrology.md) | [直达解答](#第-20-章) | 10 | 0 / 6 / 4 | — |
| **第五篇 · 信息理论、高级算法、模拟边界与计算模型** | [第 13 章｜量子信息量度](../13-quantum-information.md) | [直达解答](#第-13-章) | 6 | 2 / 3 / 1 | 练 13-C/D/E |
| 〃 | [第 16 章｜高级算法与验证](../16-advanced-algorithms-verification.md) | [直达解答](#第-16-章) | 12 | 3 / 5 / 4 | — |
| 〃 | [第 21 章｜稳定子与经典模拟引擎](../21-stabilizer-classical-simulation.md) | [直达解答](#第-21-章) | 10 | 3 / 4 / 3 | — |
| 〃 | [第 17 章｜量子计算模型全景](../17-computation-models.md) | [直达解答](#第-17-章) | 10 | 4 / 5 / 1 | — |
| 〃 | [量子力学 Q4｜波函数、势阱与原子能级](../quantum-mechanics/04-wavefunctions-models.md) | [直达解答](#量子力学-q4) | 8 | 3 / 4 / 1 | — |
| 〃 | [第 18 章｜信道、容量、复杂度与连续变量](../18-channels-capacities-complexity.md) | [直达解答](#第-18-章) | 14 | 3 / 9 / 2 | — |
| **全书合计（26 章）** | — | [实验与扩展索引](#配套实验册与进阶练习索引) | **271** | **105 / 129 / 37** | **14 道** |

## 第 0 章

1. **【基础】计算 $|+\rangle$ 的振幅、概率与归一化**

   - **题意与约定**：单量子比特处于二维复向量空间 $\mathbb{C}^2$，计算基为 $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$、$|1\rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$。按 Born 规则，测量得到某一基态的概率等于对应复振幅的模平方 $|\alpha|^2 = \alpha^*\alpha$。
   - **核心提示**：把 $|+\rangle$ 展开成计算基 $\{|0\rangle,|1\rangle\}$ 的线性组合读出各分量振幅，再按 Born 规则对振幅取模平方 $|\alpha|^2=\alpha^*\alpha$ 并核对总和。
   - **完整分步演算**：把 $|+\rangle$ 改写为两个计算基态的线性组合，逐项读出复振幅与测量概率：

     $$
     |+\rangle
     = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
     = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle
     = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix}.
     $$

     因此结果 `0` 与 `1` 的振幅均为 $\alpha_0 = \alpha_1 = \frac{1}{\sqrt{2}}$。因为 $\frac{1}{\sqrt{2}}$ 为实数，其复共轭等于自身，逐项取模平方得：

     $$
     P(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{\sqrt{2}} \cdot \frac{1}{\sqrt{2}} = \frac{1}{2},
     \qquad
     P(1) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{\sqrt{2}} \cdot \frac{1}{\sqrt{2}} = \frac{1}{2}.
     $$

   - **结论与边界回验**：两项概率相加得 $P(0) + P(1) = \frac{1}{2} + \frac{1}{2} = 1$。计算基下的 `0` 与 `1` 构成互斥且完备的全部可能结果，两项之和等于 $1$ 正说明 $|+\rangle$ 已经归一化（态矢量长度为 $\sqrt{1/2 + 1/2} = 1$）。
   - **易错坑提醒**：不要把振幅 $\frac{1}{\sqrt{2}} \approx 0.707$ 直接当成概率，也不要把两个振幅直接相加去检查归一化（$\frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} = \sqrt{2} \neq 1$），归一化检查的对象永远是模平方之和。

2. **【基础】分辨 $|+\rangle$ 与 $|-\rangle$ 的相对相位及 $H$ 门干涉结果**

   - **题意与约定**：在二维计算基下比较 $|+\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ 与 $|-\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}$，并使用 Hadamard 门 $H = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$ 检验两态是否等价。
   - **核心提示**：先比较 $|+\rangle$ 与 $|-\rangle$ 在计算基下模平方为何抹掉符号差异，再把 Hadamard 矩阵 $H=\frac{1}{\sqrt{2}}\begin{bmatrix}1&1\\1&-1\end{bmatrix}$ 逐行左乘两个列向量，观察相长与相消干涉。
   - **完整分步演算**：先核对两态直接在计算基下的测量概率。对 $|-\rangle$，$|0\rangle$ 的振幅为 $\frac{1}{\sqrt{2}}$、$|1\rangle$ 的振幅为 $-\frac{1}{\sqrt{2}}$，取模平方时负号消失：

     $$
     P_-(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2},
     \qquad
     P_-(1) = \left|-\frac{1}{\sqrt{2}}\right|^2 = \left(-\frac{1}{\sqrt{2}}\right)\left(-\frac{1}{\sqrt{2}}\right) = \frac{1}{2}.
     $$

     两态在计算基下都各占 $1/2$，但 $|-\rangle$ 的第二项比 $|+\rangle$ 多一个负号（即两分量间的相对相位差了 $\pi$）。现在把同一个 $H$ 门分别乘在两个列向量上，逐行展开：

     $$
     \begin{aligned}
     H|+\rangle
     &= \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\right)
        \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right)
      = \frac{1}{2}\begin{bmatrix} 1\cdot 1 + 1\cdot 1 \\ 1\cdot 1 + (-1)\cdot 1 \end{bmatrix}
      = \frac{1}{2}\begin{bmatrix} 2 \\ 0 \end{bmatrix}
      = \begin{bmatrix} 1 \\ 0 \end{bmatrix}
      = |0\rangle, \\
     H|-\rangle
     &= \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\right)
        \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}\right)
      = \frac{1}{2}\begin{bmatrix} 1\cdot 1 + 1\cdot(-1) \\ 1\cdot 1 + (-1)\cdot(-1) \end{bmatrix}
      = \frac{1}{2}\begin{bmatrix} 0 \\ 2 \end{bmatrix}
      = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
      = |1\rangle.
     \end{aligned}
     $$

   - **结论与边界回验**：经过 $H$ 门后，$|+\rangle$ 在计算基测得 `0` 的概率为 $|1|^2 = 1$、测得 `1` 的概率为 $0$；$|-\rangle$ 测得 `0` 的概率为 $0$、测得 `1` 的概率为 $|1|^2 = 1$。两组输出概率和均为 $1$，且结果彻底分开，由此确定两态不是同一个量子态。
   - **易错坑提醒**：一组固定测量基下的概率表抹掉了相对相位信息，无法完整刻画量子态；只要插入后续门操作让不同路径重新汇合，相对相位就会通过相长与相消干涉直接改变测量概率。

3. **【计算】单比特最小随机实验的四步流程与千次抽样波动**

   - **题意与约定**：对应第 0 章第 4 节的最小实验，设独立重复测量次数 $N = 1000$，单次理想测得 `1` 的理论概率 $p = 1/2$，记总计测得 `1` 的次数为随机变量 $K$（无量纲计数）。
   - **核心提示**：先按时间顺序梳理制备、门操作、单次测量与统计报告四步，再用二项分布 $B(N,p)$ 的期望 $Np$ 与标准差 $\sqrt{Np(1-p)}$ 评估千次抽样的自然涨落尺度。
   - **完整分步演算**：从初态到报告结果按先后顺序至少经历四步：
     - 制备初态 $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$；
     - 施加 Hadamard 门 $H$，逐行乘得 $H|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix} = |+\rangle$；
     - 在计算基下执行一次测量，按 $P(0) = P(1) = \frac{1}{2}$ 得到单次经典输出 `0` 或 `1`；
     - 重复采样与统计报告：独立重复执行上述三步 $N = 1000$ 次，统计计数、给出误差区间并核查系统偏差。

     对于 $N = 1000$ 次独立试验，$K$ 服从二项分布 $B(1000, 1/2)$，其期望次数、恰好命中 $500$ 次的精确概率与计数标准差分别为：

     $$
     \mathbb{E}[K] = Np = 1000 \times \frac{1}{2} = 500,
     \qquad
     \Pr(K = 500) = \binom{1000}{500} 2^{-1000} \approx 0.025225,
     $$

     $$
     \sigma_K = \sqrt{Np(1-p)} = \sqrt{1000 \times \frac{1}{2} \times \frac{1}{2}} = \sqrt{250} \approx 15.81.
     $$

   - **结论与边界回验**：频率 $\hat{p} = K/1000$ 的标准差为 $\sigma_{\hat{p}} = \sigma_K / 1000 \approx 0.01581$（约 $1.58$ 个百分点）。精确累加二项分布可知，$K$ 落在 $[469, 531]$（约 $500 \pm 2\sigma_K$）内的概率约为 $95.37\%$；而恰好等于 `500:500` 的概率仅约 $2.52\%$，因此测得如 `520:480` 这样的偏离属于正常随机涨落。
   - **易错坑提醒**：一是不要把期望值 $500$ 误当成每批实验必定出现的精确计数；二是仅看到汇总比例 `500:500` 同样不能证明独立随机性（例如确定交替序列 `010101…` 或 10 个独立比特各复制 100 次都可能凑出 `500:500`），真实实验还须核查初态复位、门操控与读出误判等系统偏差。

4. **【基础】剖析“量子并行”解释的关键缺口**

   - **题意与约定**：考虑 $n$ 个量子比特组成的 $2^n$ 维复向量空间 $\mathbb{C}^{2^n}$，计算基为 $\{|x\rangle : x \in \{0,1\}^n\}$，一般纯态记作 $|\psi\rangle = \sum_{x \in \{0,1\}^n} \alpha_x |x\rangle$。
   - **核心提示**：区分“演化过程中态矢量在 $2^n$ 维空间并行携带复振幅”与“一次计算基测量按 Born 规则只返回一个 $n$ 位经典串”这两件事，再思考算法靠什么把有用信息集中到可测结果。
   - **完整分步演算**：以最常见的 $n$ 比特均匀叠加态为例，把 $H^{\otimes n}$ 作用在 $|0\rangle^{\otimes n}$ 上：

     $$
     H^{\otimes n}|0\rangle^{\otimes n}
     = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} |x\rangle,
     \qquad
     P(x) = \left|\frac{1}{\sqrt{2^n}}\right|^2 = \frac{1}{2^n}.
     $$

     尽管数学表达式里同时包含了 $2^n$ 个计算基分支的复振幅，但按照量子测量公理，一次计算基测量只会按概率分布 $\{|\alpha_x|^2\}$ 随机坍缩并交出**唯一一个** $n$ 位经典字符串 $x$，绝不会把全部 $2^n$ 个振幅表一次性打印出来。因此，仅仅构造叠加态把所有输入同时送进电路，还完全没有回答怎样把正确答案读出来。
   - **结论与边界回验**：全部 $2^n$ 个结果的概率相加为 $\sum_{x=0}^{2^n-1} \frac{1}{2^n} = 1$。以 $n = 30$ 为例，经典计算机用双精度复数稠密存储该态需要 $16 \times 2^{30}\ \mathrm{byte} = 16\ \mathrm{GiB}$，但一次计算基测量向实验者交付的仅仅是 $30$ 个经典比特，远不是 $16\ \mathrm{GiB}$ 的完整振幅表。
   - **易错坑提醒**：真正的量子算法不是靠“同时算完再全部抄下来”，而是利用问题的周期性、对称性或代数结构精心设计干涉电路，让通往错误答案的路径振幅相互抵消、通往目标性质的路径相互增强，从而把有用信息集中到可测出的结果或统计量里。

5. **【计算】审查“量子算法更快”声明的必查账本与查询开销换算**

   - **题意与约定**：在查询模型下，一次预言机调用记作 $1$ 个抽象查询步；现实墙钟时间以秒（$\mathrm{s}$）为单位，设单步经典检查耗时 $t_{\mathrm{cl}} = 10^{-9}\ \mathrm{s}$，单次量子预言机调用耗时 $t_{\mathrm{q}} = 10^{-3}\ \mathrm{s}$。
   - **核心提示**：把抽象查询步数与真实墙钟时间分开记账：先列出任务标准、数据装载与经典基线等端到端账目，再用 $T_{\mathrm{cl}}=t_{\mathrm{cl}}N$ 与 $T_{\mathrm{q}}=t_{\mathrm{q}}\sqrt{N}$ 比较给定规模下的耗时。
   - **完整分步演算**：面对任何“量子更快”的宣称，至少须追问并对齐以下核心条件（任选三项远不能替代完整比较）：
     - **任务本身与成功标准**：是精确求解、采一个样本还是估一个期望值？误差上限 $\varepsilon$、失败概率 $\delta$ 与重复采样次数是多少？
     - **输入规模与访问模型**：规模 $N$ 对应数据条数还是比特数？经典数据装载成量子态、预言机内部电路实现以及最终输出读出分别消耗多少成本？
     - **端到端系统开销与公平经典基线**：编译后的物理门数与深度、量子纠错与实时解码延迟、经典后处理耗时是多少？是否与同任务、同误差下的最强经典算法（含经典多核并行）对齐？

     “约 $1000$ 次预言机查询”只是查询模型中的抽象计数单位；在真实硬件上，每实现一次预言机调用，内部往往要拆解成成千上万个逻辑门、辅助比特反计算和纠错循环，因此 $1000$ 次查询绝不等于 $1000$ 个物理门。用第 0 章第 5 节的交叉点模型直接核算 $N = 10^6$（此时 $\sqrt{N} = 1000$）：

     $$
     T_{\mathrm{cl}}(10^6) = 10^{-9} \times 10^6\ \mathrm{s} = 10^{-3}\ \mathrm{s},
     \qquad
     T_{\mathrm{q}}(10^6) = 10^{-3} \times \sqrt{10^6}\ \mathrm{s} = 1\ \mathrm{s}.
     $$

     再解量子追平经典的不等式：

     $$
     10^{-3}\sqrt{N} \le 10^{-9} N
     \iff 10^6 \le \sqrt{N}
     \iff N \ge 10^{12}.
     $$

   - **结论与边界回验**：在 $N = 10^6$ 时，虽然查询次数少了 $1000$ 倍，但量子总耗时 $1\ \mathrm{s}$ 反而比经典的 $1\ \mathrm{ms}$ 慢了 $1000$ 倍；直到 $N = 10^{12}$ 处，两边耗时才同为 $1000\ \mathrm{s}$。若进一步计入经典搜索可按核心数 $P$ 线性并行、而 Grover 并行仅获 $\sqrt{P}$ 倍加速，实际交叉点还会推得更远。
   - **易错坑提醒**：切勿把抽象的查询次数 $O(\sqrt{N})$ 直接等同于物理门数，更不能把它直接换算成更短的墙钟运行时间；只有把装载、实现、纠错、采样与读出全部纳入同一资源账本，才能谈端到端优势。

6. **【基础】区分后量子密码（PQC）与量子密码**

   - **题意与约定**：按运行载体、安全依据、工程部署方式与代表协议四个维度，区分后量子密码（Post-Quantum Cryptography, PQC）与量子密码（如量子密钥分发 QKD）。
   - **核心提示**：从运行载体（经典芯片 vs 量子信道）、安全依据（数学难题 vs 物理定律）、部署方式与功能范围（密钥交换+签名 vs 密钥分发）四个维度对照 PQC 与 QKD。
   - **完整分步演算**：
     - **后量子密码（PQC）本质上是经典密码算法**：它完全运行在普通经典计算机、服务器、手机与现有互联网协议之上，既不传输量子态，也不需要量子硬件。它的“后量子”含义是“在设计时考虑未来大规模容错量子计算机的攻击”，选用基于格困难问题、哈希函数或纠错码等目前已知量子算法也难以高效攻破的数学难题（例如 NIST 于 2024 年发布的经典标准 FIPS 203 ML-KEM、FIPS 204 ML-DSA、FIPS 205 SLH-DSA，以及 2026 年迁移指南 NIST IR 8547）。
     - **量子密码依赖量子物理系统与量子信道**：以 BB84 量子密钥分发（QKD）为代表，它必须在通信双方之间实际发送与测量单光子或纠缠态等物理量子载体，依靠不可克隆定理与测量扰动来检测窃听，并依赖已认证的经典信道、专用光学链路以及相应的设备与中继信任模型。
     - **安全位数直觉对照（第 0 章入门量化视角）**：在算法攻击威胁上，Shor 算法使 RSA-2048 与 256 位椭圆曲线（ECC）在容错量子机上跌至多项式复杂度而彻底失效，而对对称加密 AES 仅提供 Grover 平方级加速——AES-128 的穷举搜索复杂度从 $2^{128}$ 降至约 $2^{64}$ 次预言机查询，只需把对称密钥加倍至 AES-256 即可把量子搜索门槛拉回约 $2^{128}$。因此抵御量子计算威胁的核心瓶颈是公钥交换与数字签名，PQC 用纯软件数学算法直接替换这一层，而 QKD 则属于另一条物理层对称密钥协商路线（标准化清单、认证前提与 PLOB 损耗界详见[第 12 章第 1 题](#第-12-章)）。
   - **结论与边界回验**：从密码体系定位检验：Shor 算法主要威胁 RSA、椭圆曲线（ECC）等传统公钥体制，而对 AES 等对称密码仅提供 Grover 平方级加速（密钥从 $128$ 位加倍到 $256$ 位即可维持安全余量）；PQC 通过纯软件/固件升级即可替换现有公钥与签名基础设施，与需要铺设量子物理信道的 QKD 解决的是不同层面的工程问题。
   - **易错坑提醒**：不要被两个名词里共同出现的“量子”二字误导而以为部署 PQC 需要先买一台量子计算机；PQC 保护的是经典信息系统的今天与未来，靠的是数学难题而非量子硬件。

### 练 00-C：【基础】量子科技三大支柱分工辨析与“量子新闻”四维红旗核查

- **题意与约定**：对应[第 00 章第 1.1 节](../00-overview.md#11-量子科技的三大支柱全景计算通信与传感)与[第 7 节](../00-overview.md#7-20252026-年走到哪一步了从物理比特迈向早期纠错)。某科技报道宣称：“A 机构发布了 1,000 量子比特处理器，意味着明年就能破解 RSA-2048 银行加密并顺便实现全国量子互联网通信。”请依据量子科技三大支柱（量子计算、量子通信、量子精密测量）的分工边界，以及 2025–2026 年硬件里程碑核查四项红旗，逐条拆解这条报道混同了哪些对象。
- **核心提示**：先区分“计算 / 通信 / 传感”三类技术各自依赖的核心物理载体与任务目标，再核对“物理比特数 vs 容错逻辑比特数”“单点硬件演示 vs 破译 RSA-2048 所需的百万级物理比特与长距离光纤中继”之间的鸿沟。
- **完整分步演算**：
  - **第一层：三大支柱边界澄清**：
    - **量子计算**依赖可控多比特纠缠与相干干涉电路（如超导、离子阱、中性原子处理器），目标是加速特定数学、模拟与优化计算，本身不是远距离通信网络；
    - **量子通信**依赖光纤或自由空间光子链路与量子密钥分发（QKD）/ 量子中继协议，目标是密钥协商或远端纠缠分发，并不能直接替代通用处理器跑算法；
    - **量子精密测量（传感）**：利用单自旋、原子钟或光干涉仪的相位灵敏度测量微弱磁场、时间与引力场（详见[第 20 章](../20-quantum-sensing-metrology.md)）。
  - **第二层：四维新闻红旗核查**：
    - **红旗 1（物理比特数偷换逻辑比特数）**：1,000 个未经纠错或仅部分连接的物理比特远不是 1,000 个容错逻辑比特；主流资源估算（见[第 11 章](../11-resources-benchmarks.md)）表明，以表面码在物理错率 $p \sim 10^{-3}$ 下运行 Shor 算法分解 RSA-2048，需要数千个高质量逻辑比特与约 $10^6$–$10^7$ 量级物理比特（配合低错率双比特门与实时解码），绝非“1,000 物理比特明年可破”；
    - **红旗 2（只报比特数不报门错率、连通性与相干深度）**：缺失双比特门错误率、是否低于纠错阈值（$\Lambda > 1$）与有效逻辑错误率指标时，单纯堆高比特数无法运行深层算法；
    - **红旗 3（把处理器能力错挂到“全国量子互联网”）**：芯片内近邻耦合与跨数百公里光纤量子中继（需光子接口、多跳纠缠交换与长寿命量子存储）属于完全不同的硬件体系；
    - **红旗 4（混淆“可行性里程碑”与“端到端实用优势”）**：2025–2026 年的标志性进展集中在早期逻辑存储低于阈值、中小规模逻辑门演示与特定物理观测量模拟，距离大规模通用容错商业破密仍有清晰的多阶段工程路障。
- **结论与边界回验**：该报道同时犯了“混淆量子计算与量子通信支柱”和“把物理比特总数冒充百万级容错逻辑资源”两类错误；评估任何量子里程碑必须同时核验支柱归属、物理/逻辑口径、阈值与错误率、以及端到端系统资源账本。
- **易错坑提醒**：不要因为某一支柱已经工程化（例如原子钟精密测量或城域点对点 QKD），就默认另一支柱（大规模通用容错量子计算机）也已同步进入商用阶段。

### 练 00-D：【计算】$n = 40$ 比特态矢量与密度矩阵经典内存墙精确核算

- **题意与约定**：对应[第 00 章第 3.4 节](../00-overview.md#34-指数级振幅意味着什么一张经典模拟内存账单)。采用 IEEE-754 双精度复数（`complex128`，每个复数占 $16\ \mathrm{byte}$），分别精确计算 $n = 30$ 与 $n = 40$ 比特稠密纯态矢量（$2^n$ 个复数）与稠密密度矩阵（$2^n \times 2^n = 4^n$ 个复数）的内存需求（按二进制单位 $1\ \mathrm{GiB} = 2^{30}\ \mathrm{B},\; 1\ \mathrm{TiB} = 2^{40}\ \mathrm{B},\; 1\ \mathrm{EiB} = 2^{60}\ \mathrm{B},\; 1\ \mathrm{YiB} = 2^{80}\ \mathrm{B}$），并说明为何“稠密内存装不下”不等于“任何 40 比特线路都不可经典模拟”。
- **核心提示**：先写出 $M_{\mathrm{ket}}(n) = 16 \times 2^n\ \mathrm{B}$ 与 $M_\rho(n) = 16 \times 4^n = 16 \times 2^{2n}\ \mathrm{B}$ 两条精确公式，再用 $2^{10}$ 进制单位换算，最后对照第 21 章的紧凑结构模拟引擎划清边界。
- **完整分步演算**：
  - **第一步：$n = 30$ 比特基线核算**：

    $$
    M_{\mathrm{ket}}(30) = 16 \times 2^{30}\ \mathrm{B} = 16\ \mathrm{GiB},
    \qquad
    M_\rho(30) = 16 \times 2^{60}\ \mathrm{B} = 16\ \mathrm{EiB} \approx 1.845 \times 10^{19}\ \mathrm{B}.
    $$

  - **第二步：$n = 40$ 比特内存墙核算**（每增加 $10$ 个比特，态矢量扩大 $2^{10} = 1024$ 倍，密度矩阵扩大 $4^{10} = 2^{20} = 1{,}048{,}576$ 倍）：

    $$
    M_{\mathrm{ket}}(40) = 16 \times 2^{40}\ \mathrm{B} = 16\ \mathrm{TiB} = 16{,}384\ \mathrm{GiB} \approx 1.759 \times 10^{13}\ \mathrm{B},
    $$

    $$
    M_\rho(40) = 16 \times 4^{40}\ \mathrm{B} = 16 \times 2^{80}\ \mathrm{B} = 16\ \mathrm{YiB} \approx 1.934 \times 10^{25}\ \mathrm{B}.
    $$

  - **第三步：物理量级与经典模拟边界**：
    - $16\ \mathrm{TiB}$ 虽远超单台桌面工作站，但仅相当于大型超算几十至上百个高内存节点之和，仍可做全振幅分布式态矢量模拟；
    - 而 $16\ \mathrm{YiB}$（约 $1.68 \times 10^7\ \mathrm{EiB}$）已远超当今地球全部数据中心存储容量总和，暴力稠密密度矩阵模拟彻底不可行；
    - 但这只是**暴力稠密数组**的存储下界：若 40 比特线路仅含 Clifford 门（稳定子模拟仅需 $O(n^2)$ 比特）、或具有一维低纠缠结构（MPS 仅需 $O(n\chi^2)$ 参数）、或含较强退极化噪声且仅测局域观测量（Pauli 传播），笔记本电脑即可在毫秒至秒级精确求解（详见[第 21 章](../21-stabilizer-classical-simulation.md)）。
- **结论与边界回验**：$n = 40$ 时双精度稠密态矢量需 $16\ \mathrm{TiB}$、稠密密度矩阵需 $16\ \mathrm{YiB}$（两者相差 $2^{40} \approx 1.10 \times 10^{12}$ 倍）。检验倍率：$M_{\mathrm{ket}}(40)/M_{\mathrm{ket}}(30) = 2^{10} = 1024$，$M_\rho(40)/M_\rho(30) = 4^{10} = 2^{20}$，完全自洽。
- **易错坑提醒**：不要把“暴力稠密矩阵需要 $2^{2n}$ 字节”直接等同于“量子计算已超越所有经典模拟算法”，更不要在含噪模拟中默认密度矩阵只比态矢量大 2 倍——它是平方倍 $2^n$ 倍！

## 第 1 章

1. **【基础】复数四则运算、模平方与概率取值边界**

   - **题意与约定**：在复数域 $\mathbb{C}$ 中，虚数单位满足 $i^2 = -1$；对 $z = a + bi$（$a, b \in \mathbb{R}$），其复共轭为 $z^* = a - bi$，模平方为 $|z|^2 = z^* z = a^2 + b^2$。合法概率必须落在闭区间 $[0, 1]$ 内。
   - **核心提示**：按复数乘法分配律并代入 $i^2=-1$，用共轭乘分母完成除法化简；再对照归一化概率公理 $0\le P\le 1$ 检验单个未归一化模平方的边界。
   - **完整分步演算**：依次逐项展开乘法、模平方与分母实数化：

     $$
     \begin{aligned}
     (1 + 2i)(3 - i)
     &= 1\cdot 3 + 1\cdot(-i) + 2i\cdot 3 + 2i\cdot(-i) \\
     &= 3 - i + 6i - 2i^2 \\
     &= 3 + 5i - 2(-1)
      = 5 + 5i,
     \end{aligned}
     $$

     $$
     |1 + i|^2
     = (1 + i)^*(1 + i)
     = (1 - i)(1 + i)
     = 1^2 - i^2
     = 1 - (-1)
     = 2,
     $$

     $$
     \frac{1}{1 + i}
     = \frac{1 \cdot (1 - i)}{(1 + i)(1 - i)}
     = \frac{1 - i}{2}
     = \frac{1}{2} - \frac{1}{2}i.
     $$

     虽然 $|1 + i|^2 = 2 \ge 0$ 是非负实数，但因为 $2 > 1$ 超出了 $[0, 1]$，它绝不能直接充当归一化量子态中某一结果的测量概率；只有先将包含该分量的整个态矢量归一化（使所有分量模平方之和为 $1$），才能把对应振幅的模平方解读为概率。
   - **结论与边界回验**：验算倒数乘回原数：$(1 + i)\cdot\frac{1 - i}{2} = \frac{1 - i^2}{2} = \frac{2}{2} = 1$；验算乘法模长守恒：$|1+2i|^2\cdot|3-i|^2 = (1+4)(9+1) = 50$，而 $|5+5i|^2 = 25 + 25 = 50$，完全一致。
   - **易错坑提醒**：计算复数模平方时切忌写成 $(1+i)^2 = 1 + 2i + i^2 = 2i$（那是复数直接平方，不是模平方）；同时牢记非负只是概率的必要条件，还必须满足 $\le 1$ 且全空间总和为 $1$。

2. **【基础】求 $|p\rangle = [1, i]^T$ 的左矢、内积与归一化向量**

   - **题意与约定**：$|p\rangle = \begin{bmatrix} 1 \\ i \end{bmatrix} \in \mathbb{C}^2$。本书统一采用**左反线性**内积 $\langle u|v\rangle = \sum_j u_j^* v_j$，左矢 $\langle p| = (|p\rangle)^\dagger$ 须先逐项取复共轭再转置为行向量。
   - **核心提示**：记住左矢 $\langle p|$ 是列向量 $|p\rangle$ 的**共轭转置**（虚部必须变号），再按行乘列算内积 $\langle p|p\rangle$ 并除以范数 $\sqrt{\langle p|p\rangle}$。
   - **完整分步演算**：先构造左矢 $\langle p|$，再行乘列算内积 $\langle p|p\rangle$ 与范数 $\||p\rangle\|$：

     $$
     \langle p| = \begin{bmatrix} 1 \\ i \end{bmatrix}^\dagger = \begin{bmatrix} 1^* & i^* \end{bmatrix} = \begin{bmatrix} 1 & -i \end{bmatrix},
     $$

     $$
     \langle p|p\rangle
     = \begin{bmatrix} 1 & -i \end{bmatrix}\begin{bmatrix} 1 \\ i \end{bmatrix}
     = 1\cdot 1 + (-i)\cdot i
     = 1 - i^2
     = 1 - (-1)
     = 2.
     $$

     于是向量长度为 $\||p\rangle\| = \sqrt{\langle p|p\rangle} = \sqrt{2}$。将原向量除以长度 $\sqrt{2}$，得归一化列向量：

     $$
     |\hat{p}\rangle
     = \frac{1}{\sqrt{2}}|p\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ i \end{bmatrix}
     = \begin{bmatrix} 1/\sqrt{2} \\ i/\sqrt{2} \end{bmatrix}.
     $$

   - **结论与边界回验**：对 $|\hat{p}\rangle$ 逐项算模平方之和：$\left|\frac{1}{\sqrt{2}}\right|^2 + \left|\frac{i}{\sqrt{2}}\right|^2 = \frac{1}{2} + \left(-\frac{i}{\sqrt{2}}\right)\left(\frac{i}{\sqrt{2}}\right) = \frac{1}{2} + \frac{1}{2} = 1$，确已归一化。
   - **易错坑提醒**：如果忘记把左矢里的 $i$ 共轭成 $-i$，直接用普通转置 $[1, i]$ 去乘 $[1, i]^T$，会算出 $1 + i^2 = 0$，把一个非零向量的长度错算成 $0$。

3. **【计算】归一化复向量 $[1, 1+i]^T$ 并回验概率和**

   - **题意与约定**：给定二维未归一化复列向量 $|v\rangle = \begin{bmatrix} 1 \\ 1 + i \end{bmatrix} \in \mathbb{C}^2$，求单位向量 $|\hat{v}\rangle = |v\rangle / \||v\rangle\|$ 并检验各分量模平方之和为 $1$。
   - **核心提示**：先逐分量算出 $|\alpha_0|^2$ 与 $|\alpha_1|^2$（注意复数 $|a+bi|^2=a^2+b^2$），求和开根号得范数，再把每个分量除以范数并回验模平方之和。
   - **完整分步演算**：先逐分量算模平方再求和，求得范数平方与长度：

     $$
     \langle v|v\rangle
     = |1|^2 + |1 + i|^2
     = 1^2 + (1^2 + 1^2)
     = 1 + 2
     = 3,
     \qquad
     \||v\rangle\| = \sqrt{3}.
     $$

     将每个分量同除以 $\sqrt{3}$，得到归一化列向量：

     $$
     |\hat{v}\rangle
     = \frac{1}{\sqrt{3}}\begin{bmatrix} 1 \\ 1 + i \end{bmatrix}
     = \begin{bmatrix} 1/\sqrt{3} \\ (1 + i)/\sqrt{3} \end{bmatrix}.
     $$

   - **结论与边界回验**：独立检查归一化后两个分量的模平方之和：

     $$
     \left|\frac{1}{\sqrt{3}}\right|^2 + \left|\frac{1 + i}{\sqrt{3}}\right|^2
     = \frac{1}{3} + \frac{(1 - i)(1 + i)}{3}
     = \frac{1}{3} + \frac{2}{3}
     = 1.
     $$

   - **易错坑提醒**：归一化除以的是长度 $\sqrt{3}$ 而不是范数平方 $3$；若错除以 $3$，新向量的模平方之和会变成 $\frac{1}{9} + \frac{2}{9} = \frac{1}{3} \neq 1$。

4. **【计算】求 $|1\rangle$ 在 $\{|+\rangle, |-\rangle\}$ 基中的坐标并还原**

   - **题意与约定**：在 $\mathbb{C}^2$ 中，标准正交基 $\{|+\rangle, |-\rangle\}$ 满足 $|+\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}$、$|-\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}$。向量 $|1\rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ 在该正交归一基下的坐标由左反线性内积 $c_+ = \langle +|1\rangle$、$c_- = \langle -|1\rangle$ 给出。
   - **核心提示**：利用标准正交基的投影坐标公式 $c_+=\langle +|1\rangle$、$c_-=\langle -|1\rangle$ 求出两个展开系数，再代回 $c_+|+\rangle+c_-|-\rangle$ 验证是否精确还原 $|1\rangle$。
   - **完整分步演算**：先写出左矢 $\langle +| = \frac{1}{\sqrt{2}}[1, 1]$ 与 $\langle -| = \frac{1}{\sqrt{2}}[1, -1]$，逐项行乘列算坐标：

     $$
     c_+ = \langle +|1\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}\begin{bmatrix} 0 \\ 1 \end{bmatrix}
     = \frac{1\cdot 0 + 1\cdot 1}{\sqrt{2}}
     = \frac{1}{\sqrt{2}},
     $$

     $$
     c_- = \langle -|1\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -1 \end{bmatrix}\begin{bmatrix} 0 \\ 1 \end{bmatrix}
     = \frac{1\cdot 0 + (-1)\cdot 1}{\sqrt{2}}
     = -\frac{1}{\sqrt{2}}.
     $$

     把两个坐标代回线性展开式 $c_+|+\rangle + c_-|-\rangle$ 逐步还原 $|1\rangle$：

     $$
     \begin{aligned}
     \frac{1}{\sqrt{2}}|+\rangle - \frac{1}{\sqrt{2}}|-\rangle
     &= \frac{1}{\sqrt{2}}\cdot\frac{|0\rangle + |1\rangle}{\sqrt{2}}
        - \frac{1}{\sqrt{2}}\cdot\frac{|0\rangle - |1\rangle}{\sqrt{2}} \\
     &= \frac{|0\rangle + |1\rangle - |0\rangle + |1\rangle}{2}
      = \frac{2|1\rangle}{2}
      = |1\rangle.
     \end{aligned}
     $$

   - **结论与边界回验**：新基坐标的模平方之和为 $|c_+|^2 + |c_-|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 + \left|-\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2} + \frac{1}{2} = 1$，换到另一组正交归一基后向量长度保持严格不变。
   - **易错坑提醒**：只有当目标基 $\{|e_j\rangle\}$ **彼此正交且各自归一**时，才能直接用内积 $\langle e_j|v\rangle$ 读坐标；且写还原式时务必保留 $c_-$ 的负号，否则相加会得到 $|0\rangle$ 而非 $|1\rangle$。

5. **【计算】矩阵作用在向量上与求共轭转置 $M^\dagger$**

   - **题意与约定**：给定 $2 \times 2$ 复矩阵 $M = \begin{bmatrix} 1 & i \\ 0 & 2 \end{bmatrix}$ 与 $2 \times 1$ 列向量 $|p\rangle = \begin{bmatrix} 1 \\ i \end{bmatrix}$，计算矩阵-向量乘积 $M|p\rangle$ 与伴随矩阵（共轭转置）$M^\dagger = (M^*)^T$，并指明每个结果的对象类型。
   - **核心提示**：矩阵乘列向量按“左矩阵行点乘右列向量”逐行展开；求共轭转置 $M^\dagger=(M^T)^*$ 时同时交换行列位置并把所有虚部取反。
   - **完整分步演算**：先按“行乘列”逐行计算 $M|p\rangle$：

     $$
     M|p\rangle
     = \begin{bmatrix} 1 & i \\ 0 & 2 \end{bmatrix}\begin{bmatrix} 1 \\ i \end{bmatrix}
     = \begin{bmatrix} 1\cdot 1 + i\cdot i \\ 0\cdot 1 + 2\cdot i \end{bmatrix}
     = \begin{bmatrix} 1 + (-1) \\ 2i \end{bmatrix}
     = \begin{bmatrix} 0 \\ 2i \end{bmatrix}.
     $$

     再分两步求 $M^\dagger$——第一步逐格取复共轭得 $M^*$，第二步将行与列互换（转置）：

     $$
     M^* = \begin{bmatrix} 1^* & i^* \\ 0^* & 2^* \end{bmatrix}
         = \begin{bmatrix} 1 & -i \\ 0 & 2 \end{bmatrix}
     \quad\xrightarrow{\text{转置}}\quad
     M^\dagger = (M^*)^T = \begin{bmatrix} 1 & 0 \\ -i & 2 \end{bmatrix}.
     $$

     对象类型区分：$M|p\rangle = \begin{bmatrix} 0 \\ 2i \end{bmatrix}$ 是 **$2 \times 1$ 列向量**；$M^\dagger = \begin{bmatrix} 1 & 0 \\ -i & 2 \end{bmatrix}$ 是 **$2 \times 2$ 矩阵**（可作用在向量上的算符），二者都不是标量数值。
   - **结论与边界回验**：利用恒等式 $(M|p\rangle)^\dagger = \langle p|M^\dagger$ 做独立核验：左边为 $\begin{bmatrix} 0 & -2i \end{bmatrix}$；右边用 $\langle p| = [1, -i]$ 乘以 $M^\dagger$ 得 $[1\cdot 1 + (-i)(-i),\; 1\cdot 0 + (-i)\cdot 2] = [1 - 1,\; -2i] = [0, -2i]$，两边完全吻合。
   - **易错坑提醒**：求 $M^\dagger$ 时切忌只转置不取共轭（那样会错得 $\begin{bmatrix} 1 & 0 \\ i & 2 \end{bmatrix}$），也切忌只共轭不转置（那样停留在 $M^*$ 而非 $M^\dagger$）。

6. **【计算】外积 $|u\rangle\langle u|$、迹与投影概率的迹表达式**

   - **题意与约定**：给定归一化单比特态 $|u\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}} = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ i \end{bmatrix} \in \mathbb{C}^2$，计算 $2 \times 2$ 外积矩阵 $|u\rangle\langle u|$、其迹 $\operatorname{Tr}(|u\rangle\langle u|)$，以及与投影算符 $P_0 = |0\rangle\langle 0|$ 相乘后的迹 $\operatorname{Tr}(|0\rangle\langle 0|\,|u\rangle\langle u|)$。
   - **核心提示**：先把 $|u\rangle$ 写成 $2\times 1$ 列向量、$\langle u|$ 写成 $1\times 2$ 共轭行向量，按列乘行拼出 $2\times 2$ 外积矩阵，再取主对角之和算迹并利用迹的循环性核对投影概率。
   - **完整分步演算**：先对 $|u\rangle$ 取共轭转置得到左矢 $\langle u| = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -i \end{bmatrix}$，再按“列乘行”逐格写出 $2 \times 2$ 外积：

     $$
     |u\rangle\langle u|
     = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ i \end{bmatrix}\right)
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -i \end{bmatrix}\right)
     = \frac{1}{2}\begin{bmatrix} 1\cdot 1 & 1\cdot(-i) \\ i\cdot 1 & i\cdot(-i) \end{bmatrix}
     = \frac{1}{2}\begin{bmatrix} 1 & -i \\ i & 1 \end{bmatrix}.
     $$

     求主对角线元素之和即得迹：

     $$
     \operatorname{Tr}(|u\rangle\langle u|) = \frac{1}{2} + \frac{1}{2} = 1.
     $$

     再写出投影矩阵 $P_0 = |0\rangle\langle 0| = \begin{bmatrix} 1 \\ 0 \end{bmatrix}\begin{bmatrix} 1 & 0 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$，逐格做矩阵乘法并求迹：

     $$
     P_0|u\rangle\langle u|
     = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}
       \left(\frac{1}{2}\begin{bmatrix} 1 & -i \\ i & 1 \end{bmatrix}\right)
     = \frac{1}{2}\begin{bmatrix} 1\cdot 1 + 0\cdot i & 1\cdot(-i) + 0\cdot 1 \\ 0\cdot 1 + 0\cdot i & 0\cdot(-i) + 0\cdot 1 \end{bmatrix}
     = \frac{1}{2}\begin{bmatrix} 1 & -i \\ 0 & 0 \end{bmatrix},
     $$

     $$
     \operatorname{Tr}\bigl(|0\rangle\langle 0|\,|u\rangle\langle u|\bigr) = \frac{1}{2} + 0 = \frac{1}{2}.
     $$

   - **结论与边界回验**：利用 Born 规则与迹循环性质独立核验：$\operatorname{Tr}(|0\rangle\langle 0|\,|u\rangle\langle u|) = \langle 0|u\rangle\langle u|0\rangle = |\langle 0|u\rangle|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}$，且 $(|u\rangle\langle u|)^\dagger = |u\rangle\langle u|$ 满足厄米性。
   - **易错坑提醒**：外积右上格是 $1\cdot(-i) = -i$、左下格是 $i\cdot 1 = +i$；如果漏掉左矢 $\langle u|$ 里的复共轭，会把矩阵错算成 $\frac{1}{2}\begin{bmatrix} 1 & i \\ i & -1 \end{bmatrix}$，不仅不再厄米，迹还会变成 $0$。

7. **【基础】验证 Pauli-$X$ 矩阵的本征态 $|+\rangle, |-\rangle$ 与本征值**

   - **题意与约定**：在 $\mathbb{C}^2$ 计算基下，$X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$，$|+\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}$，$|-\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}$。若非零向量 $|v\rangle$ 满足 $X|v\rangle = \lambda|v\rangle$，则 $\lambda$ 为对应本征值。
   - **核心提示**：把 Pauli-$X$ 矩阵分别左乘 $|+\rangle$ 与 $|-\rangle$ 的列向量，观察输出是否为原列向量的常数倍 $X|\psi\rangle=\lambda|\psi\rangle$，直接读出对应本征值。
   - **完整分步演算**：保留归一化系数 $\frac{1}{\sqrt{2}}$，逐行做矩阵乘列向量运算：

     $$
     X|+\rangle
     = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 0\cdot 1 + 1\cdot 1 \\ 1\cdot 1 + 0\cdot 1 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}
     = (+1)|+\rangle,
     $$

     $$
     X|-\rangle
     = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 0\cdot 1 + 1\cdot(-1) \\ 1\cdot 1 + 0\cdot(-1) \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} -1 \\ 1 \end{bmatrix}
     = (-1)\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}
     = (-1)|-\rangle.
     $$

     因此 $|+\rangle$ 对应的本征值是 $+1$，$|-\rangle$ 对应的本征值是 $-1$。
   - **结论与边界回验**：核对迹与行列式：本征值之和 $(+1)+(-1) = 0 = \operatorname{Tr}(X)$，本征值之积 $(+1)(-1) = -1 = \det(X)$；两本征态内积 $\langle +|-\rangle = \frac{1}{2}(1\cdot 1 + 1\cdot(-1)) = 0$，满足厄米矩阵不同本征值对应本征态正交。
   - **易错坑提醒**：本征值 $-1$ 代表测量可观测量 $X$ 时可能读出的物理量数值（而非概率），且本征向量按定义必须是非零向量（零向量 $X\vec{0}=\lambda\vec{0}$ 不算本征态）。

8. **【计算】大端序张量积 $|1\rangle\otimes|+\rangle$ 与 $(H\otimes I)|01\rangle$ 的双路径计算**

   - **题意与约定**：两比特态空间为 $\mathbb{C}^4$，全书统一采用高位在左的大端序基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$，分别对应四维标准单位列向量。
   - **核心提示**：在大端序基 $(|00\rangle,|01\rangle,|10\rangle,|11\rangle)$ 下，按分块规则将前向量的每个元素乘入后向量；算 $(H\otimes I)|01\rangle$ 时可分别用“分位作用 $(H|0\rangle)\otimes(I|1\rangle)$”与“$4\times 4$ 分块矩阵乘法”两条路径互验。
   - **完整分步演算**：先按定义展开 $|1\rangle\otimes|+\rangle$：

     $$
     |1\rangle\otimes|+\rangle
     = |1\rangle \otimes \frac{|0\rangle + |1\rangle}{\sqrt{2}}
     = \frac{|10\rangle + |11\rangle}{\sqrt{2}}
     = \begin{bmatrix} 0 \\ 1 \end{bmatrix} \otimes \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 0\cdot 1 \\ 0\cdot 1 \\ 1\cdot 1 \\ 1\cdot 1 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 0 \\ 0 \\ 1 \\ 1 \end{bmatrix}.
     $$

     再求 $(H\otimes I)|01\rangle$，提供两条独立路径交叉核对：
     - **路径一（混合乘积律）**：直接利用 $(A\otimes B)(|u\rangle\otimes|v\rangle) = (A|u\rangle)\otimes(B|v\rangle)$，

       $$
       (H\otimes I)|01\rangle
       = (H|0\rangle)\otimes(I|1\rangle)
       = \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right)\otimes|1\rangle
       = \frac{|01\rangle + |11\rangle}{\sqrt{2}}
       = \frac{1}{\sqrt{2}}\begin{bmatrix} 0 \\ 1 \\ 0 \\ 1 \end{bmatrix}.
       $$

     - **路径二（印章分块构造 $4 \times 4$ 矩阵）**：把 $H$ 的每个元素乘以 $2 \times 2$ 矩阵 $I$ 拼成 $H\otimes I$，再乘以 $|01\rangle = [0, 1, 0, 0]^T$（即读出第 $2$ 列）：

       $$
       (H\otimes I)|01\rangle
       = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 1 & 0 & -1 & 0 \\ 0 & 1 & 0 & -1 \end{bmatrix}\begin{bmatrix} 0 \\ 1 \\ 0 \\ 0 \end{bmatrix}
       = \frac{1}{\sqrt{2}}\begin{bmatrix} 0 \\ 1 \\ 0 \\ 1 \end{bmatrix}.
       $$

   - **结论与边界回验**：两条路径得到完全一致的结果；两个输出态各自的模平方之和均为 $0 + \frac{1}{2} + 0 + \frac{1}{2} = 1$（及 $0 + 0 + \frac{1}{2} + \frac{1}{2} = 1$），均满足归一化。
   - **易错坑提醒**：张量积不满足交换律，$|1\rangle\otimes|+\rangle$ 把 $|+\rangle$ 放在第二比特（位置 `10, 11`），而 $(H\otimes I)|01\rangle = |+\rangle\otimes|1\rangle$ 把 $|+\rangle$ 放在第一比特（位置 `01, 11`），两者的四维列向量完全不同。

9. **【计算】贝叶斯定理求筛查后验概率 $\Pr(A \mid +)$**

   - **题意与约定**：记事件 $A$ 为“样本具有性质 $A$”，$\bar{A}$ 为“无性质 $A$”，$+$ 为“测试阳性”。题设先验 $\Pr(A) = 0.01$、$\Pr(\bar{A}) = 1 - 0.01 = 0.99$，条件概率 $\Pr(+\mid A) = 0.90$、$\Pr(+\mid \bar{A}) = 0.05$。
   - **核心提示**：先用全概率公式算出总阳性率 $\Pr(+)=\Pr(+\mid A)\Pr(A)+\Pr(+\mid\bar A)\Pr(\bar A)$，再代入贝叶斯公式 $\Pr(A\mid +)=\frac{\Pr(+\mid A)\Pr(A)}{\Pr(+)}$。
   - **完整分步演算**：第一步按全概率公式把“有 $A$ 且阳性”与“无 $A$ 且阳性”两种互斥情形相加，求出总阳性率 $\Pr(+)$：

     $$
     \begin{aligned}
     \Pr(+)
     &= \Pr(+\mid A)\Pr(A) + \Pr(+\mid \bar{A})\Pr(\bar{A}) \\
     &= 0.90 \times 0.01 + 0.05 \times 0.99 \\
     &= 0.009 + 0.0495
      = 0.0585.
     \end{aligned}
     $$

     第二步代入贝叶斯公式并约分为最简分数：

     $$
     \Pr(A\mid +)
     = \frac{\Pr(+\mid A)\Pr(A)}{\Pr(+)}
     = \frac{0.009}{0.0585}
     = \frac{90}{585}
     = \frac{2}{13}
     \approx 0.1538 \quad (15.38\%).
     $$

   - **结论与边界回验**：用 **$10{,}000$ 份样本的自然频率表**独立回验：

     | 真实类别 | 样本总数 | 测试阳性（$+$） | 测试阴性（$-$） |
     | :--- | ---: | ---: | ---: |
     | 有性质 $A$（$1\%$） | $100$ | $100 \times 0.90 = 90$ | $10$ |
     | 无性质 $A$（$99\%$） | $9{,}900$ | $9{,}900 \times 0.05 = 495$ | $9{,}405$ |
     | **合计** | **$10{,}000$** | **$585$** | **$9{,}415$** |

     表中全部 $585$ 份阳性样本里真正有性质 $A$ 的恰为 $90$ 份，占比 $90 / 585 = 2/13 \approx 15.38\%$，同时阳性与阴性总数 $585 + 9415 = 10{,}000$ 严丝合缝。
   - **易错坑提醒**：切忌把灵敏度 $\Pr(+\mid A) = 90\%$ 错当成后验概率 $\Pr(A\mid +)$；当性质 $A$ 在总体中很罕见（基础率仅 $1\%$）时，庞大的无 $A$ 群体哪怕只有 $5\%$ 假阳性率，产生的假阳性人数（$495$）也会远超真阳性人数（$90$）。

10. **【计算】独立重复试验的成功次数期望、频率期望与标准差**

    - **题意与约定**：独立执行 $N = 100$ 次伯努利（$0/1$）试验，每次成功概率 $p = 1/4$、失败概率 $1 - p = 3/4$。记成功总次数为 $K = \sum_{j=1}^{100} X_j$（$X_j \in \{0, 1\}$），样本频率为 $\hat{p} = K / N$。
    - **核心提示**：把 $N$ 次独立伯努利试验的总成功数 $K$ 视为二项分布 $B(N,p)$，套用 $\mathbb E[K]=Np$、$\mathbb E[\hat p]=p$ 与 $\sigma_{\hat p}=\sqrt{p(1-p)/N}$，并区分期望值与单批实测实现。
    - **完整分步演算**：由期望的线性性与独立随机变量的方差可加性，先算单次试验的期望与方差：

      $$
      \mathbb{E}[X_j] = p = \frac{1}{4},
      \qquad
      \operatorname{Var}(X_j) = p(1 - p) = \frac{1}{4} \cdot \frac{3}{4} = \frac{3}{16}.
      $$

      再依次求出成功次数 $K$ 的期望与标准差，以及频率 $\hat{p} = K/100$ 的期望与标准差：

      $$
      \mathbb{E}[K] = Np = 100 \times \frac{1}{4} = 25,
      \qquad
      \sigma_K = \sqrt{Np(1 - p)} = \sqrt{100 \times \frac{3}{16}} = \sqrt{\frac{75}{4}} = \frac{5\sqrt{3}}{2} \approx 4.33,
      $$

      $$
      \mathbb{E}[\hat{p}] = \frac{\mathbb{E}[K]}{100} = \frac{1}{4} = 0.25,
      \qquad
      \sigma_{\hat{p}} = \sqrt{\frac{p(1 - p)}{N}} = \sqrt{\frac{3/16}{100}} = \sqrt{\frac{3}{1600}} = \frac{\sqrt{3}}{40} \approx 0.0433.
      $$

      因此频率标准差约为 $4.33$ 个百分点。**不保证**一次实验恰好成功 $25$ 次：单批试验恰好得到 $K = 25$ 的精确二项概率仅为

      $$
      \Pr(K = 25) = \binom{100}{25}\left(\frac{1}{4}\right)^{25}\left(\frac{3}{4}\right)^{75} \approx 0.0918 \quad (9.18\%).
      $$

    - **结论与边界回验**：量纲与比例自洽：$\sigma_K / N = 4.3301 / 100 = 0.043301 = \sigma_{\hat{p}}$；典型单批计数在 $25 \pm 4.33$（大致 $21$ 到 $29$ 次）附近波动是常态。
    - **易错坑提醒**：方差公式 $\operatorname{Var}(\hat{p}) = p(1-p)/N$ 严格依赖“各次试验相互独立且概率恒定”的前提；如果不同轮次间存在系统漂移或结果正相关，真实标准差会大于 $\frac{\sqrt{3}}{40}$。

11. **【计算】计算基概率与矩阵乘法求期望值 $\langle X\rangle$**

    - **题意与约定**：给定归一化单比特态 $|\psi\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}} = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ i \end{bmatrix} \in \mathbb{C}^2$，Pauli 矩阵 $X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$，采用左反线性内积计算 $\langle X\rangle = \langle\psi|X|\psi\rangle$。
    - **核心提示**：先对 $|\psi\rangle$ 各计算基分量取模平方求概率，再严格按左矢—矩阵—右矢次序分步计算 $\langle\psi|X|\psi\rangle$（注意先算 $X|\psi\rangle$，再左乘共轭行向量 $\langle\psi|$）。
    - **完整分步演算**：先对两个计算基振幅取模平方求概率：

      $$
      p(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2},
      \qquad
      p(1) = \left|\frac{i}{\sqrt{2}}\right|^2 = \left(-\frac{i}{\sqrt{2}}\right)\left(\frac{i}{\sqrt{2}}\right) = \frac{-i^2}{2} = \frac{1}{2}.
      $$

      再用显式矩阵乘法两步计算 $\langle X\rangle$：先算右半部分列向量 $X|\psi\rangle$，再左乘左矢 $\langle\psi| = \frac{1}{\sqrt{2}}[1, -i]$：

      $$
      X|\psi\rangle
      = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}\left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ i \end{bmatrix}\right)
      = \frac{1}{\sqrt{2}}\begin{bmatrix} i \\ 1 \end{bmatrix},
      $$

      $$
      \langle X\rangle
      = \langle\psi|(X|\psi\rangle)
      = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -i \end{bmatrix}\right)
        \left(\frac{1}{\sqrt{2}}\begin{bmatrix} i \\ 1 \end{bmatrix}\right)
      = \frac{1}{2}\bigl(1\cdot i + (-i)\cdot 1\bigr)
      = \frac{i - i}{2}
      = 0.
      $$

    - **结论与边界回验**：计算基概率和为 $\frac{1}{2} + \frac{1}{2} = 1$。再用 $X$ 的本征基 $\{|+\rangle, |-\rangle\}$ 独立回验 $\langle X\rangle$：

      $$
      \langle +|\psi\rangle = \frac{1 + i}{2} \implies p(+) = \frac{1^2 + 1^2}{4} = \frac{1}{2},
      \qquad
      \langle -|\psi\rangle = \frac{1 - i}{2} \implies p(-) = \frac{1^2 + (-1)^2}{4} = \frac{1}{2},
      $$

      期望值为 $(+1)\cdot\frac{1}{2} + (-1)\cdot\frac{1}{2} = 0$，与矩阵乘法完全吻合。
    - **易错坑提醒**：两点高频失误：一是算 $p(1)$ 时把 $\frac{i}{\sqrt{2}}$ 直接平方成 $-\frac{1}{2}$；二是看到 $\langle X\rangle = 0$ 就以为单次测量 $X$ 会读出 $0$——单次测 $X$ 只能得到本征值 $+1$ 或 $-1$，这里的 $0$ 是大量独立测量的长期平均值。

12. **【基础】用上下界证明 $T(n) = 3n^2 + 7n + 2$ 属于 $\Theta(n^2)$**

    - **题意与约定**：按渐近紧界定义，若存在正常数 $c_1, c_2 > 0$ 与门槛 $n_0 \ge 1$，使所有 $n \ge n_0$ 均满足 $c_1 g(n) \le T(n) \le c_2 g(n)$，则记作 $T(n) = \Theta(g(n))$。
    - **核心提示**：在 $n\ge 1$ 上利用 $n\le n^2$ 与 $1\le n^2$ 把低阶项向上放缩为 $n^2$ 的常数倍，再舍去非负低阶项得到下界常数，从而验证 $c_1 n^2\le T(n)\le c_2 n^2$。
    - **完整分步演算**：当 $n \ge 1$ 时，$n > 0$ 且 $n \le n^2$、$1 \le n^2$，逐项放大低次项以求上界、舍去正低次项以求下界：

      $$
      \begin{aligned}
      \text{下界：} &\quad 3n^2 + 7n + 2 \ge 3n^2, \\
      \text{上界：} &\quad 3n^2 + 7n + 2 \le 3n^2 + 7n^2 + 2n^2 = 12n^2.
      \end{aligned}
      $$

      合并得到对一切 $n \ge 1$ 成立的双边不等式：

      $$
      3n^2 \le T(n) \le 12n^2.
      $$

      显式取定义参数 $c_1 = 3$、$c_2 = 12$、$n_0 = 1$，因此 $T(n) = \Theta(n^2)$。
    - **结论与边界回验**：代入边界点 $n = 1$ 核对：$3(1)^2 = 3 \le T(1) = 3 + 7 + 2 = 12 \le 12(1)^2 = 12$（上界取等）；代入 $n = 10$ 核对：$300 \le T(10) = 372 \le 1200$，双边不等式均成立。
    - **易错坑提醒**：$T(n) = \Theta(n^2)$ 只刻画 $n$ 增大时的增长阶（忽略常数因子与低次项），绝不表示对每个具体的 $n$ 耗时就等于 $n^2$；且大 $O$ 仅给上界，必须同时证明同阶下界 $\Omega(n^2)$ 才能写 $\Theta(n^2)$。

13. **【基础】归一化三维复列向量 $[1, i, 1-i]^T$**

    - **题意与约定**：给定三维复向量 $|w\rangle = \begin{bmatrix} 1 \\ i \\ 1 - i \end{bmatrix} \in \mathbb{C}^3$，按三维左反线性内积 $\langle w|w\rangle = \sum_{j=1}^3 |w_j|^2$ 归一化。
    - **核心提示**：高维向量归一化与二维完全同法：把三个复分量的模平方相加开根号得欧氏范数 $\||w\rangle\|$，再将原向量除以该范数并回验三项模平方之和。
    - **完整分步演算**：先逐分量写出模平方并相加求长度：

      $$
      \begin{aligned}
      \langle w|w\rangle
      &= |1|^2 + |i|^2 + |1 - i|^2 \\
      &= 1^2 + 1^2 + \bigl(1^2 + (-1)^2\bigr) \\
      &= 1 + 1 + 2 = 4,
      \end{aligned}
      \qquad
      \||w\rangle\| = \sqrt{4} = 2.
      $$

      把三个分量同除以长度 $2$，得归一化列向量：

      $$
      |\hat{w}\rangle
      = \frac{1}{2}\begin{bmatrix} 1 \\ i \\ 1 - i \end{bmatrix}
      = \begin{bmatrix} 1/2 \\ i/2 \\ (1 - i)/2 \end{bmatrix}.
      $$

    - **结论与边界回验**：逐项验算新向量的模平方之和：

      $$
      \left|\frac{1}{2}\right|^2 + \left|\frac{i}{2}\right|^2 + \left|\frac{1 - i}{2}\right|^2
      = \frac{1}{4} + \frac{1}{4} + \frac{1^2 + (-1)^2}{4}
      = \frac{1 + 1 + 2}{4}
      = 1.
      $$

    - **易错坑提醒**：$|1 - i|^2$ 是实部平方加虚部平方 $1^2 + (-1)^2 = 2$，不要误算成 $(1-i)^2 = -2i$，也不要漏掉虚部前面的负号平方后为 $+1$。

14. **【基础】为什么 $O(\sqrt{N})$ 次预言机查询推不出墙钟时间加速**

    - **题意与约定**：将理论查询复杂度 $Q(N) = O(\sqrt{N})$ 与真实端到端墙钟时间 $T_{\mathrm{wall}}$（单位：$\mathrm{s}$）按统一资源账本拆解对比。
    - **核心提示**：区分“抽象预言机查询次数”与“现实墙钟时间”，从单次预言机内部门分解、数据装载/读出、纠错与解码开销以及经典基线时钟速率四个环节拆解。
    - **完整分步演算**：查询模型把整次预言机调用打包成 $1$ 步黑箱开销，而真实设备的总墙钟时间至少由以下各项累加：

      $$
      T_{\mathrm{wall}}
      = T_{\mathrm{prep}} + Q(N)\cdot t_{\mathrm{q}} + T_{\mathrm{readout}} + T_{\mathrm{classical}}.
      $$

      其中每一项都可能抹平甚至逆转 $O(\sqrt{N})$ 的查询优势：
      - **预言机内部实现成本 $t_{\mathrm{q}}$**：单次抽象查询展开成基本逻辑门、辅助位反计算、路由与容错纠错循环后，可能需要极高的物理门数与微秒至毫秒级延迟；
      - **数据与初态装载 $T_{\mathrm{prep}}$**：把外部经典数据装入量子态若需 $\Omega(N)$ 步，总体复杂度便退回经典量级；
      - **重复采样与经典后处理 $T_{\mathrm{readout}} + T_{\mathrm{classical}}$**：满足目标置信度所需的重复次数、纠错症状实时解码与误差缓解都会计入总时间；
      - **大 $O$ 隐含常数与经典基线**：即使单次量子查询只比经典慢 $10^6$ 倍，也需要 $N \ge 10^{12}$ 才能在单核时间上追平，若经典端再结合多核并行或利用数据结构（如索引），交叉点会更遥远。
    - **结论与边界回验**：回忆第 0 章的交叉点检验：当 $N = 10^6$、$t_{\mathrm{cl}} = 10^{-9}\ \mathrm{s}$、$t_{\mathrm{q}} = 10^{-3}\ \mathrm{s}$ 时，量子查询数虽仅为 $\sqrt{N} = 1000$，墙钟时间却为 $1\ \mathrm{s}$，比经典的 $1\ \mathrm{ms}$ 反而慢了 $1000$ 倍。
    - **易错坑提醒**：比较算法快慢必须固定同一任务、同一误差与置信标准、同一输入访问模型，并将装载、编译、纠错与读出成本全部摊进墙钟时间，绝不能用抽象查询步数直接等价于真实运行速度。

## 第 2 章

1. **【基础】定位 $|{-i}\rangle = (|0\rangle - i|1\rangle)/\sqrt{2}$ 在 Bloch 球上的轴点**

   - **题意与约定**：单比特纯态记作 $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\varphi}\sin(\theta/2)|1\rangle$（$\theta \in [0, \pi]$，$\varphi \in [0, 2\pi)$），对应三维 Bloch 单位向量 $\vec{r} = (\sin\theta\cos\varphi,\; \sin\theta\sin\varphi,\; \cos\theta)$；Pauli 矩阵 $Y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}$。
   - **核心提示**：把目标态与 Bloch 球通用参数化 $\cos(\theta/2)|0\rangle+e^{i\varphi}\sin(\theta/2)|1\rangle$ 逐项对照，读出极角 $\theta$ 与方位角 $\varphi$，或直接计算 Pauli 期望 $(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)$。
   - **完整分步演算**：将 $|{-i}\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{-i}{\sqrt{2}}|1\rangle$ 与标准形式对照：$\cos(\theta/2) = \frac{1}{\sqrt{2}}$ 且 $\sin(\theta/2) = \frac{1}{\sqrt{2}}$ 给出 $\theta/2 = \frac{\pi}{4}$，即 $\theta = \frac{\pi}{2}$；由 $e^{i\varphi} = -i = e^{-i\pi/2} = e^{i 3\pi/2}$ 得相对相位 $\varphi = \frac{3\pi}{2}$（等价于 $-\frac{\pi}{2}$）。代入三维球坐标公式：

     $$
     \vec{r}
     = \left(\sin\frac{\pi}{2}\cos\frac{3\pi}{2},\; \sin\frac{\pi}{2}\sin\frac{3\pi}{2},\; \cos\frac{\pi}{2}\right)
     = (1\cdot 0,\; 1\cdot(-1),\; 0)
     = (0, -1, 0).
     $$

     因此它对应 Bloch 球六个轴点中的 **$-y$ 轴点**。再用矩阵乘法逐行检验它确实是 $Y$ 的 $-1$ 本征态：

     $$
     Y|{-i}\rangle
     = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -i \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 0\cdot 1 + (-i)(-i) \\ i\cdot 1 + 0\cdot(-i) \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} -1 \\ i \end{bmatrix}
     = -\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -i \end{bmatrix}
     = (-1)|{-i}\rangle.
     $$

   - **结论与边界回验**：检查 Bloch 向量长度 $|\vec{r}| = \sqrt{0^2 + (-1)^2 + 0^2} = 1$（纯态落在球面上）；同时用坐标公式独立回验：$r_x = 2\operatorname{Re}(\alpha^*\beta) = 2\operatorname{Re}(-i/2) = 0$，$r_y = 2\operatorname{Im}(\alpha^*\beta) = 2\operatorname{Im}(-i/2) = -1$，$r_z = |\alpha|^2 - |\beta|^2 = \frac{1}{2} - \frac{1}{2} = 0$，结果一致。
   - **易错坑提醒**：本征值 $-1$ 是测量 $Y$ 时确定出现的物理读数（$-y$ 轴方向），绝不表示概率为负；另注意算 $r_y = 2\operatorname{Im}(\alpha^*\beta)$ 时共轭取在第一分量 $\alpha$ 上，写反共轭位置会把 $+y$ 和 $-y$ 颠倒。

2. **【计算】逐格计算 $HZH$ 并识别等价单比特门**

   - **题意与约定**：在 $\mathbb{C}^2$ 计算基下，$H = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$、$Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$、$X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$。算符乘积 $HZH$ 必须保持从右到左的次序，先算 $ZH$，再左乘 $H$。
   - **核心提示**：按矩阵乘法结合律先算 $ZH$（或 $HZ$），再乘以另一个 $H$，把 $2\times 2$ 矩阵的四个位置逐格算完后对照 Pauli 矩阵族识别。
   - **完整分步演算**：第一步逐格计算 $ZH$：

     $$
     ZH
     = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1\cdot 1 + 0\cdot 1 & 1\cdot 1 + 0\cdot(-1) \\ 0\cdot 1 + (-1)\cdot 1 & 0\cdot 1 + (-1)\cdot(-1) \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix}.
     $$

     第二步将 $H$ 左乘刚才的结果，逐格展开全部四个矩阵元：

     $$
     \begin{aligned}
     H(ZH)
     &= \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\right)
        \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix}\right) \\
     &= \frac{1}{2}\begin{bmatrix} 1\cdot 1 + 1\cdot(-1) & 1\cdot 1 + 1\cdot 1 \\ 1\cdot 1 + (-1)\cdot(-1) & 1\cdot 1 + (-1)\cdot 1 \end{bmatrix}
      = \frac{1}{2}\begin{bmatrix} 0 & 2 \\ 2 & 0 \end{bmatrix}
      = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
      = X.
     \end{aligned}
     $$

     因此 $HZH = X$（Pauli-$X$ 门，即比特翻转门）。
   - **结论与边界回验**：在两个计算基态上独立检验作用效果：$HZH|0\rangle = HZ|+\rangle = H|-\rangle = |1\rangle = X|0\rangle$；$HZH|1\rangle = HZ|-\rangle = H|+\rangle = |0\rangle = X|1\rangle$，两基态完全吻合。
   - **易错坑提醒**：矩阵乘法一般不满足交换律，绝不能看到两边各有一个 $H$ 就跳过中间的 $Z$ 把两个 $H$ 消成 $H^2 Z = Z$——实际上 $H$ 把 $Z$ 轴和 $X$ 轴互换，才让 $HZH$ 变成了 $X$。

3. **【基础】对 $(3|0\rangle + 4|1\rangle)/5$ 做计算基测量的概率与条件后态**

   - **题意与约定**：给定归一化单比特纯态 $|\psi\rangle = \frac{3}{5}|0\rangle + \frac{4}{5}|1\rangle = \begin{bmatrix} 3/5 \\ 4/5 \end{bmatrix} \in \mathbb{C}^2$；计算基投影算符为 $P_0 = |0\rangle\langle 0| = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$、$P_1 = |1\rangle\langle 1| = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$。
   - **核心提示**：对计算基展开态按 Born 规则求模平方得各结果概率；投影测量得到结果 $m$ 后，条件后态是对应投影算符作用后重新归一化的本征态。
   - **完整分步演算**：先计算两个投影分支的未归一化向量，再算长度平方得概率，最后除以长度得归一化条件后态：

     $$
     P_0|\psi\rangle = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}\begin{bmatrix} 3/5 \\ 4/5 \end{bmatrix} = \begin{bmatrix} 3/5 \\ 0 \end{bmatrix},
     \qquad
     p(0) = \|P_0|\psi\rangle\|^2 = \left|\frac{3}{5}\right|^2 = \frac{9}{25},
     $$

     $$
     |\psi_{\mid 0}\rangle = \frac{P_0|\psi\rangle}{\sqrt{p(0)}} = \frac{1}{3/5}\begin{bmatrix} 3/5 \\ 0 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} = |0\rangle.
     $$

     同理对结果 `1` 计算：

     $$
     P_1|\psi\rangle = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 3/5 \\ 4/5 \end{bmatrix} = \begin{bmatrix} 0 \\ 4/5 \end{bmatrix},
     \qquad
     p(1) = \|P_1|\psi\rangle\|^2 = \left|\frac{4}{5}\right|^2 = \frac{16}{25},
     $$

     $$
     |\psi_{\mid 1}\rangle = \frac{P_1|\psi\rangle}{\sqrt{p(1)}} = \frac{1}{4/5}\begin{bmatrix} 0 \\ 4/5 \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix} = |1\rangle.
     $$

     **补充验证（若测量后丢弃结果记录）**：此时不能挑选其中一个纯态矢量，而须写成按概率加权的非选择密度矩阵：

     $$
     \rho' = p(0)|0\rangle\langle 0| + p(1)|1\rangle\langle 1|
           = \frac{9}{25}\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} + \frac{16}{25}\begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}
           = \begin{bmatrix} 9/25 & 0 \\ 0 & 16/25 \end{bmatrix}.
     $$

   - **结论与边界回验**：$p(0) + p(1) = \frac{9}{25} + \frac{16}{25} = \frac{25}{25} = 1$；两个条件后态长度均为 $1$；非选择态的迹 $\operatorname{Tr}(\rho') = \frac{9}{25} + \frac{16}{25} = 1$ 且半正定。
   - **易错坑提醒**：投影后的未归一化分支 $\frac{3}{5}|0\rangle$ 携带的是发生概率的平方根，真正描述测后物理态的条件后态必须除以 $\sqrt{p(0)} = \frac{3}{5}$ 重新归一化，不能直接把 $\frac{3}{5}|0\rangle$ 当成合法条件后态。

4. **【基础】测量次数扩大 $100$ 倍为何频率误差通常只缩小 $10$ 倍**

   - **题意与约定**：设独立重复测量次数为 $N$，单次出现某结果的真实概率恒为 $p \in (0, 1)$，样本频率记作 $\hat{p} = K / N$，用频率标准差 $\sigma_{\hat{p}}$ 刻画典型统计误差尺度。
   - **核心提示**：写出独立同分布抽样频率标准差公式 $\sigma_{\hat p}=\sqrt{p(1-p)/N}$，观察分母中 $N$ 的幂次如何决定样本量放大与统计误差缩小的比例关系。
   - **完整分步演算**：在独立同分布前提下，频率标准差为 $\sigma_{\hat{p}}(N) = \sqrt{\frac{p(1-p)}{N}}$。当采样次数从 $N$ 扩大 $100$ 倍变为 $100N$ 而 $p$ 不变时，计算两次标准差的精确比值：

     $$
     \frac{\sigma_{\hat{p}}(100N)}{\sigma_{\hat{p}}(N)}
     = \frac{\sqrt{\dfrac{p(1-p)}{100N}}}{\sqrt{\dfrac{p(1-p)}{N}}}
     = \frac{1}{\sqrt{100}}
     = \frac{1}{10}.
     $$

     由于样本量 $N$ 位于分母的平方根内（即标准量子散粒噪声标度 $1/\sqrt{N}$），想把统计误差压缩 $10$ 倍，就必须付出 $10^2 = 100$ 倍的重复测量次数。
   - **结论与边界回验**：代入具体数字 $p = 1/2$ 检验：$N = 100$ 时 $\sigma_{\hat{p}}(100) = \sqrt{\frac{1/4}{100}} = 0.05$（$5$ 个百分点）；扩大百倍到 $N = 10{,}000$ 时 $\sigma_{\hat{p}}(10{,}000) = \sqrt{\frac{1/4}{10{,}000}} = 0.005$（$0.5$ 个百分点），恰好缩小 $10$ 倍。
   - **易错坑提醒**：这里的“通常”指重复做整批实验时的典型涨落尺度，既不保证单次具体某批样本误差一定正好缩小 $10$ 倍，也绝不能靠增大 $N$ 消除门校准偏置、读出错判或参数漂移等系统误差。

5. **【计算】在计算基与 $X$ 基下对比纯态 $|+\rangle$ 和经典等权混态**

   - **题意与约定**：对比两个对象——（甲）每次固定制备的纯态 $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$；（乙）以各 $1/2$ 概率经典随机制备 $|0\rangle$ 或 $|1\rangle$ 得到的系综 $\rho_{\mathrm{mix}} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1|$。$X$ 基为 $\{|+\rangle, |-\rangle\}$。
   - **核心提示**：先比较两对象在 $Z$ 基下的概率分布，再分别在 $X$ 基计算“纯态直接投影 $|\langle +|\psi\rangle|^2$”与“混态先对基态求概率再按经典权重平均”两种算法；也可从施加 $H$ 门后 Bloch 球几何位置对照。
   - **完整分步演算**：
     - **计算基统计**：对（甲），$p_{\text{甲}}(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}$、$p_{\text{甲}}(1) = \frac{1}{2}$；对（乙），半数轮次必得 `0`、半数轮次必得 `1`，故总概率同样是 $p_{\text{乙}}(0) = \frac{1}{2}$、$p_{\text{乙}}(1) = \frac{1}{2}$。两者在计算基统计完全相同。
     - **$X$ 基统计**：对（甲），先用左反线性内积求 $+$ 振幅与概率：

       $$
       \langle +|+\rangle = \frac{1}{2}\begin{bmatrix} 1 & 1 \end{bmatrix}\begin{bmatrix} 1 \\ 1 \end{bmatrix} = 1
       \implies
       p_{\text{甲}}(+) = |\langle +|+\rangle|^2 = 1.
       $$

       对（乙），先分别算出 $|0\rangle$ 和 $|1\rangle$ 在 $X$ 基测得 $+$ 的内积与概率：

       $$
       \langle +|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \frac{1}{\sqrt{2}} \implies |\langle +|0\rangle|^2 = \frac{1}{2},
       $$

       $$
       \langle +|1\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}\begin{bmatrix} 0 \\ 1 \end{bmatrix} = \frac{1}{\sqrt{2}} \implies |\langle +|1\rangle|^2 = \frac{1}{2}.
       $$

       按全概率公式以各 $1/2$ 的制备权重相加，得（乙）测得 $+$ 的概率：

       $$
       p_{\text{乙}}(+)
       = \frac{1}{2}|\langle +|0\rangle|^2 + \frac{1}{2}|\langle +|1\rangle|^2
       = \frac{1}{2}\cdot\frac{1}{2} + \frac{1}{2}\cdot\frac{1}{2}
       = \frac{1}{2}.
       $$

     - **电路实现与 Bloch 球几何对照（第 2 章量子线路视角）**：在量子电路上，$X$ 基测量等价于**先施加一个 $H$ 门再做计算基测量**——在 Bloch 球上，$H$ 门把位于球面 $+x$ 轴 $(+1, 0, 0)$ 的纯态 $|+\rangle$ 旋转到北极 $|0\rangle$（确定测得 `0`），却把位于球心 $(0, 0, 0)$ 的等权混态 $I/2$ 留在原地不动（仍各半输出 `0` 与 `1`）；从 Stern–Gerlach 实验装置与密度矩阵纯度视角的对照见[量子力学 Q1 第 5 题](#量子力学-q1)。
   - **结论与边界回验**：对（甲），$p_{\text{甲}}(-) = |\langle -|+\rangle|^2 = 0$，$1 + 0 = 1$；对（乙），$p_{\text{乙}}(-) = \frac{1}{2}\cdot\frac{1}{2} + \frac{1}{2}\cdot\frac{1}{2} = \frac{1}{2}$，$\frac{1}{2} + \frac{1}{2} = 1$。两者在 $X$ 基下给出截然不同的概率（$1$ 对 $1/2$），从而可以区分。
   - **易错坑提醒**：不能保证**只测一次**就一定分清两者——因为（乙）也有 $50\%$ 概率给出 $+$（与（甲）撞车），唯有测到 $-$ 时可立即排除（甲），一般须借助多轮重复采样的统计频率来区分。

6. **【基础】逐步演算 $H \to Z \to H$ 作用于 $|0\rangle$ 的状态与末态概率**

   - **题意与约定**：按电路从左到右的时间顺序依次对 $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ 施加 $H$、$Z$、$H$，对应矩阵从右向左连续作用 $H(Z(H|0\rangle))$。
   - **核心提示**：电路图从左向右读、矩阵乘法从右向左作用：依次把 $H$、$Z$、$H$ 三个矩阵乘在列向量 $|0\rangle$ 上写出每拍中间态，最后对末态的 $|1\rangle$ 分量取模平方。
   - **完整分步演算**：分三步逐行展开：

     $$
     |\psi_1\rangle
     = H|0\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}
     = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
     = |+\rangle,
     $$

     $$
     |\psi_2\rangle
     = Z|\psi_1\rangle
     = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}\left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}
     = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
     = |-\rangle,
     $$

     $$
     \begin{aligned}
     |\psi_3\rangle
     = H|\psi_2\rangle
     &= H\left(\frac{|0\rangle - |1\rangle}{\sqrt{2}}\right)
      = \frac{H|0\rangle - H|1\rangle}{\sqrt{2}} \\
     &= \frac{1}{\sqrt{2}}\left(\frac{|0\rangle + |1\rangle}{\sqrt{2}} - \frac{|0\rangle - |1\rangle}{\sqrt{2}}\right)
      = \frac{2|1\rangle}{2}
      = |1\rangle.
     \end{aligned}
     $$

     最终在计算基测得 `1` 的概率为：

     $$
     p(1) = |\langle 1|\psi_3\rangle|^2 = |\langle 1|1\rangle|^2 = 1.
     $$

   - **结论与边界回验**：结合第 2 题已经验证的恒等式 $HZH = X$ 做独立核验：$HZH|0\rangle = X|0\rangle = |1\rangle$，概率 $p(0) = 0$、$p(1) = 1$，和为 $1$，两路结果完全一致。
   - **易错坑提醒**：中间态 $|+\rangle$ 和 $|-\rangle$ 在计算基下测得 `0/1` 的概率都是各半，看起来似乎“没变化”；正是最后的 $H$ 门通过干涉把 $Z$ 门写入的相对负号转换成确定的概率差异。

7. **【计算】对 $|\psi\rangle = (\sqrt{3}|0\rangle + i|1\rangle)/2$ 做 $X$ 基测量与丢弃记录后的密度矩阵**

   - **题意与约定**：给定归一化单比特纯态 $|\psi\rangle = \frac{1}{2}\begin{bmatrix} \sqrt{3} \\ i \end{bmatrix} \in \mathbb{C}^2$，在 $X$ 基 $\{|+\rangle, |-\rangle\}$ 下用左反线性内积求振幅、概率与非选择后态 $\rho'$。
   - **核心提示**：先用左反线性内积求 $X$ 基振幅 $\langle +|\psi\rangle$ 与 $\langle -|\psi\rangle$ 并取模平方得概率；丢弃测量记录时按非选择测量规则 $\rho_{\mathrm{post}}=P_+\rho P_+ + P_-\rho P_-$ 写加权外积和。
   - **完整分步演算**：先逐行展开 $\langle +|\psi\rangle$ 与 $\langle -|\psi\rangle$，并按复数模平方算概率：

     $$
     \langle +|\psi\rangle
     = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}\right)
       \left(\frac{1}{2}\begin{bmatrix} \sqrt{3} \\ i \end{bmatrix}\right)
     = \frac{\sqrt{3} + i}{2\sqrt{2}},
     $$

     $$
     p(+)
     = |\langle +|\psi\rangle|^2
     = \frac{(\sqrt{3} - i)(\sqrt{3} + i)}{(2\sqrt{2})^2}
     = \frac{3 + 1}{8}
     = \frac{1}{2},
     $$

     $$
     \langle -|\psi\rangle
     = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -1 \end{bmatrix}\right)
       \left(\frac{1}{2}\begin{bmatrix} \sqrt{3} \\ i \end{bmatrix}\right)
     = \frac{\sqrt{3} - i}{2\sqrt{2}},
     \qquad
     p(-)
     = \frac{(\sqrt{3} + i)(\sqrt{3} - i)}{8}
     = \frac{3 + 1}{8}
     = \frac{1}{2}.
     $$

     已知结果为 $+$ 时，条件后态是 $|+\rangle$；已知结果为 $-$ 时，条件后态是 $|-\rangle$。若执行了理想 $X$ 基投影测量却丢弃测量记录，把两个外积矩阵逐格写开再按概率加权相加：

     $$
     |+\rangle\langle +| = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix},
     \qquad
     |-\rangle\langle -| = \frac{1}{2}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix},
     $$

     $$
     \rho'
     = p(+)|+\rangle\langle +| + p(-)|-\rangle\langle -|
     = \frac{1}{4}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
       + \frac{1}{4}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}
     = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
     = \frac{I}{2}.
     $$

   - **结论与边界回验**：原态归一化检验 $\frac{3}{4} + \frac{1}{4} = 1$；测量概率和 $p(+) + p(-) = \frac{1}{2} + \frac{1}{2} = 1$；非选择态 $\rho' = I/2$ 满足 $\operatorname{Tr}(\rho') = 1$，而纯度从原纯态的 $1$ 降为 $\operatorname{Tr}(\rho'^2) = \frac{1}{4} + \frac{1}{4} = \frac{1}{2}$。
   - **易错坑提醒**：$\rho' = \frac{1}{2}|+\rangle\langle +| + \frac{1}{2}|-\rangle\langle -| = \frac{I}{2}$ 表示我们对已发生的测量结果一无所知所形成的统计混态，绝不代表“单次记录同时既是正号又是负号”。

8. **【计算】计算 $R_y(\pi/2)|0\rangle$ 的输出态、计算基概率与 Bloch 坐标**

   - **题意与约定**：绕 Bloch 球 $y$ 轴旋转整角 $\theta$ 的单比特门定义为 $R_y(\theta) = \begin{bmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{bmatrix}$（注意矩阵中用的是半角 $\theta/2$）。
   - **核心提示**：记住旋转门参数带**半角** $\theta/2$：将 $\theta=\pi/2$ 代入 $R_y(\theta)=\begin{bmatrix}\cos(\theta/2)&-\sin(\theta/2)\\\sin(\theta/2)&\cos(\theta/2)\end{bmatrix}$ 作用在 $|0\rangle$ 上，再算概率与 $(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)$。
   - **完整分步演算**：代入 $\theta = \frac{\pi}{2}$，得半角 $\frac{\theta}{2} = \frac{\pi}{4}$，且 $\cos\frac{\pi}{4} = \sin\frac{\pi}{4} = \frac{1}{\sqrt{2}}$，写出旋转矩阵并逐行乘以 $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$：

     $$
     R_y\!\left(\frac{\pi}{2}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix},
     \qquad
     R_y\!\left(\frac{\pi}{2}\right)|0\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}
     = |+\rangle.
     $$

     由输出态 $|+\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$，直接算得计算基概率 $p(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}$、$p(1) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}$。代入 $\alpha = \beta = \frac{1}{\sqrt{2}}$ 求 Bloch 坐标：

     $$
     \begin{aligned}
     r_x &= 2\operatorname{Re}(\alpha^*\beta) = 2\operatorname{Re}\!\left(\frac{1}{2}\right) = 1, \\
     r_y &= 2\operatorname{Im}(\alpha^*\beta) = 2\operatorname{Im}\!\left(\frac{1}{2}\right) = 0, \\
     r_z &= |\alpha|^2 - |\beta|^2 = \frac{1}{2} - \frac{1}{2} = 0.
     \end{aligned}
     $$

     因此 Bloch 坐标为 $(1, 0, 0)$（$+x$ 轴点）。
   - **结论与边界回验**：概率和 $\frac{1}{2} + \frac{1}{2} = 1$；Bloch 向量长度 $|\vec{r}| = \sqrt{1^2 + 0^2 + 0^2} = 1$；几何上从北极 $+z = (0,0,1)$ 按右手法则绕 $+y$ 轴旋转 $+90^\circ$，正好转到 $+x = (1,0,0)$，与代数计算严丝合缝。
   - **易错坑提醒**：千万不要在旋转矩阵里漏除 $2$ 而把 $\cos(\pi/2)=0, \sin(\pi/2)=1$ 直接填进去——那样会错算成 $|1\rangle$（实为绕 $y$ 轴旋转 $\pi$ 即 $R_y(\pi)|0\rangle$）。

9. **【计算】POVM 元素 $E_0 = \operatorname{diag}(3/4, 1/4)$ 的读出概率与测后态边界**

   - **题意与约定**：第 2 章第 7 节给出二元非投影 POVM $E_0 = \begin{bmatrix} 3/4 & 0 \\ 0 & 1/4 \end{bmatrix}$、$E_1 = I - E_0 = \begin{bmatrix} 1/4 & 0 \\ 0 & 3/4 \end{bmatrix}$；输入态为 $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$。按 POVM 规则，结果 $k$ 的概率为 $p(k) = \langle\psi|E_k|\psi\rangle$。
   - **核心提示**：用 POVM 概率公式 $P(m)=\langle\psi|E_m|\psi\rangle$ 计算输出概率；回答第二问时回忆 $E_m=M_m^\dagger M_m$ 在左乘任意酉阵 $U_m$ 下保持不变的自由度。
   - **完整分步演算**：逐项展开矩阵夹心乘法算报告 `0` 的概率：

     $$
     p(0)
     = \langle 0|E_0|0\rangle
     = \begin{bmatrix} 1 & 0 \end{bmatrix}
       \begin{bmatrix} 3/4 & 0 \\ 0 & 1/4 \end{bmatrix}
       \begin{bmatrix} 1 \\ 0 \end{bmatrix}
     = \begin{bmatrix} 1 & 0 \end{bmatrix}
       \begin{bmatrix} 3/4 \\ 0 \end{bmatrix}
     = \frac{3}{4}.
     $$

     **仅凭 $E_0$ 不能确定测量后的状态**。因为同一 POVM 元素 $E_0 = M_0^\dagger M_0$ 对应无穷多种物理量子仪器，只要给测量算符左乘任意酉门 $U$（满足 $U^\dagger U = I$），就得到相同的 $E_0$ 却产生不同的后态。例如比较以下两台实现同一个 $E_0$ 的仪器：
     - **仪器甲（温和测量）**：取 $M_0 = \sqrt{E_0} = \operatorname{diag}(\sqrt{3}/2,\; 1/2)$，输入 $|0\rangle$ 报 `0` 时后态为 $\frac{M_0|0\rangle}{\sqrt{3/4}} = |0\rangle$；
     - **仪器乙（翻转测量）**：取 $N_0 = X\sqrt{E_0} = \begin{bmatrix} 0 & 1/2 \\ \sqrt{3}/2 & 0 \end{bmatrix}$，满足 $N_0^\dagger N_0 = \sqrt{E_0}X^\dagger X\sqrt{E_0} = E_0$，但输入 $|0\rangle$ 报 `0` 时后态却变成 $\frac{N_0|0\rangle}{\sqrt{3/4}} = |1\rangle$（也可以在读出后强制复位到任意固定态）。
   - **结论与边界回验**：顺手验算另一结果概率 $p(1) = \langle 0|E_1|0\rangle = \frac{1}{4}$，总概率 $p(0) + p(1) = \frac{3}{4} + \frac{1}{4} = 1$；两台仪器的 $E_0$ 完备关系均为 $E_0 + E_1 = I$ 且半正定。
   - **易错坑提醒**：绝对不要把正算符直接乘在态上得到的 $E_0|0\rangle$ 当作测后态——$E_0$ 只负责给概率，测后演化必须由额外给定的测量算符（或一般量子仪器）决定。

10. **【基础】计算 $p = 1/2, N = 400$ 时的频率标准差并界定统计含义**

    - **题意与约定**：独立重复试验总次数 $N = 400$，单次成功概率恒为 $p = 1/2$，记样本频率为 $\hat{p} = K / N$，计算无量纲标准差 $\sigma_{\hat{p}}$。
    - **核心提示**：将 $p=1/2$ 与 $N=400$ 代入频率标准差公式 $\sigma_{\hat p}=\sqrt{p(1-p)/N}$，再按概率分布含义区分“标准差（典型涨落尺度）”与“绝对上界”。
    - **完整分步演算**：将 $p = 1/2$、$1 - p = 1/2$、$N = 400$ 代入频率标准差公式并逐步化简：

      $$
      \sigma_{\hat{p}}
      = \sqrt{\frac{p(1 - p)}{N}}
      = \sqrt{\frac{(1/2)(1/2)}{400}}
      = \sqrt{\frac{1/4}{400}}
      = \sqrt{\frac{1}{1600}}
      = \frac{1}{40}
      = 0.025.
      $$

      换算成百分比即 $2.5$ 个百分点（等价于 $400$ 次计数标准差 $\sigma_K = 400 \times 0.025 = 10$ 次）。**它不能保证每一批实验的误差都小于 $0.025$**。
    - **结论与边界回验**：在 $N = 400$ 的二项分布正态近似下，样本频率落在真值 $0.5 \pm 1\sigma_{\hat{p}} = [0.475, 0.525]$ 内的概率约为 $68.3\%$，也就是说大约还有近三分之一（约 $31.7\%$）的批次误差会超过 $0.025$；要覆盖约 $95\%$ 批次需要约 $\pm 2\sigma_{\hat{p}} = \pm 0.05$。
    - **易错坑提醒**：切勿把标准差误读为“确定性最大误差上界”，也不要忘记该公式成立的前提是各次测量独立且设备无漂移。

11. **【计算】计算 $R_z(\pi/2)|+\rangle$、提取全局相位并核对 Bloch 轴点与概率**

    - **题意与约定**：绕 Bloch 球 $z$ 轴旋转整角 $\varphi$ 的单比特门为 $R_z(\varphi) = \begin{bmatrix} e^{-i\varphi/2} & 0 \\ 0 & e^{i\varphi/2} \end{bmatrix}$，输入态 $|+\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}$。
    - **核心提示**：将 $\varphi=\pi/2$ 代入 $R_z(\varphi)=\operatorname{diag}(e^{-i\varphi/2},e^{i\varphi/2})$ 作用于 $|+\rangle$，提出 $|0\rangle$ 分量的相位作为整体全局相位后，读出剩余相对相位对应的 Bloch 轴点。
    - **完整分步演算**：代入 $\varphi = \frac{\pi}{2}$ 得半角 $\frac{\varphi}{2} = \frac{\pi}{4}$，逐行做矩阵乘法写出两个振幅：

      $$
      R_z\!\left(\frac{\pi}{2}\right)|+\rangle
      = \begin{bmatrix} e^{-i\pi/4} & 0 \\ 0 & e^{i\pi/4} \end{bmatrix}
        \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right)
      = \begin{bmatrix} e^{-i\pi/4}/\sqrt{2} \\ e^{i\pi/4}/\sqrt{2} \end{bmatrix}
      = \frac{e^{-i\pi/4}|0\rangle + e^{i\pi/4}|1\rangle}{\sqrt{2}}.
      $$

      因此 $|0\rangle$ 与 $|1\rangle$ 的振幅分别为 $\frac{e^{-i\pi/4}}{\sqrt{2}}$ 与 $\frac{e^{i\pi/4}}{\sqrt{2}}$。现在提取公因子 $e^{-i\pi/4}$ 到最前面，利用指数相减 $\frac{e^{i\pi/4}}{e^{-i\pi/4}} = e^{i(\pi/4 - (-\pi/4))} = e^{i\pi/2} = i$：

      $$
      R_z\!\left(\frac{\pi}{2}\right)|+\rangle
      = e^{-i\pi/4}\cdot\frac{|0\rangle + e^{i\pi/2}|1\rangle}{\sqrt{2}}
      = e^{-i\pi/4}\cdot\frac{|0\rangle + i|1\rangle}{\sqrt{2}}
      = e^{-i\pi/4}|{+i}\rangle.
      $$

      去掉不可观测的全局相位 $e^{-i\pi/4}$ 后，物理态为 $|{+i}\rangle$，对应 Bloch 球的 **$+y$ 轴点** $(0, 1, 0)$。检查计算基测量概率：

      $$
      p(0) = \left|\frac{e^{-i\pi/4}}{\sqrt{2}}\right|^2 = \frac{e^{+i\pi/4}e^{-i\pi/4}}{2} = \frac{1}{2},
      \qquad
      p(1) = \left|\frac{e^{i\pi/4}}{\sqrt{2}}\right|^2 = \frac{e^{-i\pi/4}e^{i\pi/4}}{2} = \frac{1}{2}.
      $$

      计算基概率仍为 $(1/2, 1/2)$，**没有改变**。
    - **结论与边界回验**：概率和 $\frac{1}{2} + \frac{1}{2} = 1$；几何上 $|+\rangle$ 位于 $+x$ 轴点 $(1,0,0)$，绕 $+z$ 轴按右手法则旋转 $+90^\circ$ 正好落到 $+y$ 轴点 $(0,1,0)$，与上述代数结果完全一致。
    - **易错坑提醒**：$R_z(\varphi)$ 在计算基中是对角相位门，不会改变计算基概率分布，但它实实在在地把两分量间的**相对相位**从 $0$ 改成了 $+\frac{\pi}{2}$；如果再对输出态测 $Y$ 基（或先做 $S^\dagger$ 再做 $H$ 测计算基），就会看到决定性的变化。

## 第 3 章

1. **【基础】用 $ad - bc$ 判别 $(|00\rangle + |10\rangle)/\sqrt{2}$ 的可分性并分解**

   - **题意与约定**：两比特纯态在 $\mathbb{C}^4$ 大端序基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$ 下写作 $a|00\rangle + b|01\rangle + c|10\rangle + d|11\rangle$。该态可分当且仅当系数行列式 $ad - bc = 0$。
   - **核心提示**：按大端序 $(|00\rangle,|01\rangle,|10\rangle,|11\rangle)$ 读出四分量 $(a,b,c,d)$，计算判别式 $ad-bc$ 是否为零；若为零，尝试提出公因子写成 $|u\rangle_A\otimes|v\rangle_B$。
   - **完整分步演算**：逐项读出四个振幅系数：

     $$
     a = \frac{1}{\sqrt{2}}, \qquad b = 0, \qquad c = \frac{1}{\sqrt{2}}, \qquad d = 0.
     $$

     代入判别式 $ad - bc$：

     $$
     ad - bc
     = \frac{1}{\sqrt{2}} \cdot 0 - 0 \cdot \frac{1}{\sqrt{2}}
     = 0 - 0
     = 0.
     $$

     因此该态是**可分态（非纠缠态）**。提取第二比特公共因子 $|0\rangle_B$ 完成张量积分解：

     $$
     \frac{|00\rangle + |10\rangle}{\sqrt{2}}
     = \left(\frac{|0\rangle_A + |1\rangle_A}{\sqrt{2}}\right) \otimes |0\rangle_B
     = |+\rangle_A \otimes |0\rangle_B.
     $$

   - **结论与边界回验**：将分解结果按分配律乘回展开：$|+\rangle\otimes|0\rangle = \frac{1}{\sqrt{2}}(|0\rangle+|1\rangle)\otimes|0\rangle = \frac{|00\rangle+|10\rangle}{\sqrt{2}}$；检查两因子长度均为 $1$，联合态模平方之和 $\frac{1}{2} + 0 + \frac{1}{2} + 0 = 1$。
   - **易错坑提醒**：不要看到“两项叠加”就凭直觉猜成纠缠态——只有当两项里**两个**比特同时相互绑定（如 $|00\rangle$ 与 $|11\rangle$）时 $ad - bc$ 才非零；本题第二比特始终固定在 $|0\rangle$，可直接提出公因子。

2. **【计算】计算单态 $|\Psi^-\rangle$ 的单比特约化密度矩阵 $\rho_A$ 与 $\rho_B$**

   - **题意与约定**：两比特单态为 $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}} \in \mathbb{C}^4$（大端序）。对子系统 $B$ 取偏迹的线性规则为 $\operatorname{Tr}_B(|i\rangle\langle k|_A \otimes |j\rangle\langle l|_B) = |i\rangle\langle k|_A\,\langle l|j\rangle_B$，对子系统 $A$ 取偏迹同理。
   - **核心提示**：先写出 $|\Psi^-\rangle\langle\Psi^-|$ 的 $4\times 4$ 密度矩阵（或展开为双下标求和），再按偏迹定义对被丢弃子系统的相同基态求和提取 $2\times 2$ 约化矩阵。
   - **完整分步演算**：先展开四项联合密度矩阵 $\rho_{AB} = |\Psi^-\rangle\langle\Psi^-|$：

     $$
     \begin{aligned}
     \rho_{AB}
     &= \left(\frac{|01\rangle - |10\rangle}{\sqrt{2}}\right)
        \left(\frac{\langle 01| - \langle 10|}{\sqrt{2}}\right) \\
     &= \frac{1}{2}\Bigl(|01\rangle\langle 01| - |01\rangle\langle 10| - |10\rangle\langle 01| + |10\rangle\langle 10|\Bigr).
     \end{aligned}
     $$

     第一步对 $B$ 求偏迹算 $\rho_A = \operatorname{Tr}_B(\rho_{AB})$，显式写出全部四项的内积因子：

     $$
     \begin{aligned}
     \rho_A
     &= \frac{1}{2}\Bigl(
        |0\rangle\langle 0|\underbrace{\langle 1|1\rangle}_{1}
        - |0\rangle\langle 1|\underbrace{\langle 0|1\rangle}_{0}
        - |1\rangle\langle 0|\underbrace{\langle 1|0\rangle}_{0}
        + |1\rangle\langle 1|\underbrace{\langle 0|0\rangle}_{1}
        \Bigr) \\
     &= \frac{1}{2}\bigl(|0\rangle\langle 0| + |1\rangle\langle 1|\bigr)
      = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
      = \frac{I}{2}.
     \end{aligned}
     $$

     第二步对称地对 $A$ 求偏迹算 $\rho_B = \operatorname{Tr}_A(\rho_{AB})$：

     $$
     \begin{aligned}
     \rho_B
     &= \frac{1}{2}\Bigl(
        \underbrace{\langle 0|0\rangle}_{1}|1\rangle\langle 1|
        - \underbrace{\langle 1|0\rangle}_{0}|1\rangle\langle 0|
        - \underbrace{\langle 0|1\rangle}_{0}|0\rangle\langle 1|
        + \underbrace{\langle 1|1\rangle}_{1}|0\rangle\langle 0|
        \Bigr) \\
     &= \frac{1}{2}\bigl(|0\rangle\langle 0| + |1\rangle\langle 1|\bigr)
      = \frac{I}{2}.
     \end{aligned}
     $$

   - **结论与边界回验**：$\operatorname{Tr}(\rho_A) = \operatorname{Tr}(\rho_B) = \frac{1}{2} + \frac{1}{2} = 1$，特征值均为 $\{1/2, 1/2\} \succeq 0$；纯度 $\operatorname{Tr}(\rho_A^2) = \frac{1}{4} + \frac{1}{4} = \frac{1}{2}$（最大混态），印证 $|\Psi^-\rangle$ 是最大纠缠态。
   - **易错坑提醒**：单态里的负号只藏在交叉项 $-|01\rangle\langle 10| - |10\rangle\langle 01|$ 里，偏迹后两项全部归零，因此四个 Bell 态 $|\Phi^\pm\rangle, |\Psi^\pm\rangle$ 的单比特约化态全都是 $I/2$，单看局部无法分辨它们。

3. **【基础】为什么仅在计算基测量无法区分 $\rho_{\mathrm{ent}}$ 与 $\rho_{\mathrm{mix}}$**

   - **题意与约定**：在大端序基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$ 下，对比最大纠缠纯态 $\rho_{\mathrm{ent}} = |\Phi^+\rangle\langle\Phi^+|$（$|\Phi^+\rangle = \frac{|00\rangle+|11\rangle}{\sqrt{2}}$）与经典相关混态 $\rho_{\mathrm{mix}} = \frac{1}{2}|00\rangle\langle 00| + \frac{1}{2}|11\rangle\langle 11|$。
   - **核心提示**：写出 $\rho_{\mathrm{ent}}=|\Phi^+\rangle\langle\Phi^+|$ 与 $\rho_{\mathrm{mix}}$ 完整的 $4\times 4$ 矩阵，比较两者的主对角元与非对角相干元，确认计算基测量仅读取哪一部分矩阵元。
   - **完整分步演算**：把两张 $4 \times 4$ 密度矩阵并排完整写出：

     $$
     \rho_{\mathrm{ent}}
     = \begin{bmatrix}
       1/2 & 0 & 0 & 1/2 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       1/2 & 0 & 0 & 1/2
       \end{bmatrix},
     \qquad
     \rho_{\mathrm{mix}}
     = \begin{bmatrix}
       1/2 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 1/2
       \end{bmatrix}.
     $$

     在计算基下，测得任意两位串 $ab \in \{00, 01, 10, 11\}$ 的概率为 $p(ab) = \langle ab|\rho|ab\rangle = \rho_{ab,ab}$，即**只读取密度矩阵的主对角元**。对照两张矩阵的主对角线，两者均为 $(1/2,\; 0,\; 0,\; 1/2)$，丝毫不差；区别完全藏在 $\rho_{\mathrm{ent}}$ 右上角与左下角的非对角相干项 $\frac{1}{2}|00\rangle\langle 11| + \frac{1}{2}|11\rangle\langle 00|$ 里。
     **跨章侧重对照（第 3 章密度矩阵结构视角）**：本题重在看清计算基测量只读取 $4\times 4$ 密度矩阵的主对角元、看不见非对角相干元；如何在实验论文复核中用三基 Bell 见证定量证伪假纠缠，见[第 15 章第 2 题](#第-15-章)。
   - **结论与边界回验**：两组计算基概率和均为 $\frac{1}{2} + 0 + 0 + \frac{1}{2} = 1$。要揭示非对角相干项，必须改测非对角基（如 $X$ 基）：在第 7 题可见，两边测 $X$ 基时 $\rho_{\mathrm{ent}}$ 只给出同号结果（$++, --$ 各 $1/2$），而 $\rho_{\mathrm{mix}}$ 给出四种结果各 $1/4$。
   - **易错坑提醒**：看到“总是同时测出 `00` 或 `11`”绝不足以声称存在量子纠缠——经典装在两个密封信封里的成对硬币（$\rho_{\mathrm{mix}}$）也能产生一模一样的计算基完美关联；必须用至少两组不对易测量基（如 $Z$ 基与 $X$ 基）交叉检验相干项。

4. **【进阶】剖析“Alice 一测量，Bob 立即知道她的结果”错在哪里**

   - **题意与约定**：以共享最大纠缠态 $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ 为例，比较 Alice 分别采取（不测、测 $Z$ 基、测 $X$ 基）三种本地策略时，Bob 在**未收到经典消息前**的无条件局部约化态 $\rho_B$。
   - **核心提示**：利用无信号定理验证：分别计算 Alice 不测量、在 $Z$ 基测量并平均、在 $X$ 基测量并平均三种情况下 Bob 的约化密度矩阵 $\rho_B=\operatorname{Tr}_A(\rho_{AB})$，看它是否依赖 Alice 的选择。
   - **完整分步演算**：
     - **Alice 不测量**：直接偏迹得 $\rho_B = \operatorname{Tr}_A(|\Phi^+\rangle\langle\Phi^+|) = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{I}{2}$；
     - **Alice 测 $Z$ 基**：她以各 $1/2$ 概率得 `0`（Bob 条件态 $|0\rangle$）或 `1`（Bob 条件态 $|1\rangle$），在 Bob 尚不知道她结果时的非选择约化态为：

       $$
       \rho_B^{(Z)} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{I}{2};
       $$

     - **Alice 测 $X$ 基**：由 $|\Phi^+\rangle = \frac{|++\rangle + |--\rangle}{\sqrt{2}}$，她以各 $1/2$ 概率得 $+$（Bob 条件态 $|+\rangle$）或 $-$（Bob 条件态 $|-\rangle$），Bob 的非选择约化态为：

       $$
       \rho_B^{(X)}
       = \frac{1}{2}|+\rangle\langle +| + \frac{1}{2}|-\rangle\langle -|
       = \frac{1}{4}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
         + \frac{1}{4}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}
       = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
       = \frac{I}{2}.
       $$

     可见无论 Alice 是否测量、选什么基测量、测得什么结果，只要她的经典消息还没送达，Bob 手里的本地密度矩阵始终恒为 $I/2$，对任意本地可观测量 $M_B$ 都有 $\operatorname{Tr}(M_B\rho_B) = \frac{1}{2}\operatorname{Tr}(M_B)$，根本观测不到任何变化。
   - **结论与边界回验**：三种情形下 $\rho_B = \rho_B^{(Z)} = \rho_B^{(X)} = I/2$，迹均为 $1$，完美符合无信号定理（no-signaling theorem）。
   - **易错坑提醒**：把“知道 Alice 结果后的**条件态**（如 $|0\rangle$ 或 $|+\rangle$）”混同于“Bob 本地能看到的**无条件约化态**（$I/2$）”是产生超光速错觉的根源；只有等经典通信到达并把两边记录配对后，条件关联才浮现出来。

5. **【基础】写出 $|+\rangle_A|1\rangle_B$ 的四维列向量与计算基概率**

   - **题意与约定**：按大端序两比特基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$，将单比特态 $|+\rangle_A = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ 与 $|1\rangle_B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ 做张量积。
   - **核心提示**：按高位在左大端序将 $|+\rangle_A\otimes|1\rangle_B$ 逐项展开到 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$，写出四维列向量并逐项取模平方。
   - **完整分步演算**：先按基态分配律展开，再按克罗内克分块写出四维列向量：

     $$
     |+\rangle_A \otimes |1\rangle_B
     = \left(\frac{|0\rangle_A + |1\rangle_A}{\sqrt{2}}\right) \otimes |1\rangle_B
     = \frac{|01\rangle + |11\rangle}{\sqrt{2}}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix} \otimes \begin{bmatrix} 0 \\ 1 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1\cdot 0 \\ 1\cdot 1 \\ 1\cdot 0 \\ 1\cdot 1 \end{bmatrix}
     = \begin{bmatrix} 0 \\ 1/\sqrt{2} \\ 0 \\ 1/\sqrt{2} \end{bmatrix}.
     $$

     按 `00, 01, 10, 11` 顺序逐项取振幅模平方，得四个计算基概率：

     $$
     p(00) = |0|^2 = 0, \qquad
     p(01) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}, \qquad
     p(10) = |0|^2 = 0, \qquad
     p(11) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}.
     $$

   - **结论与边界回验**：四个概率之和 $0 + \frac{1}{2} + 0 + \frac{1}{2} = 1$；也可按独立子系统乘积检验：$p(ab) = p_A(a)\,p_B(b)$，因 $p_A(0) = p_A(1) = \frac{1}{2}$ 且 $p_B(0) = 0, p_B(1) = 1$，相乘直接算得 $(0, 1/2, 0, 1/2)$。
   - **易错坑提醒**：不要把 $|+\rangle_A|1\rangle_B$ 与 $|1\rangle_A|+\rangle_B = [0, 0, 1/\sqrt{2}, 1/\sqrt{2}]^T$ 弄反；大端序下第一个比特决定了列向量的上半段（$A=0$）与下半段（$A=1$）。

6. **【基础】用 $ad - bc$ 判断四项均匀叠加态是否纠缠**

   - **题意与约定**：给定大端序四维归一化纯态 $|\psi\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$，利用双比特纯态可分充要判据 $ad - bc = 0$ 检验。
   - **核心提示**：不要凭项数直觉判断纠缠：读出四分量 $(a,b,c,d)$ 严格计算判别式 $ad-bc$，再检验能否因式分解为两个单比特叠加态的张量积。
   - **完整分步演算**：读出四个系数 $a = b = c = d = \frac{1}{2}$，代入行列式判据：

     $$
     ad - bc
     = \frac{1}{2}\cdot\frac{1}{2} - \frac{1}{2}\cdot\frac{1}{2}
     = \frac{1}{4} - \frac{1}{4}
     = 0.
     $$

     因此该态**不纠缠**，是严格可分的乘积纯态。直接写出张量积分解并逐项展开核对：

     $$
     |+\rangle_A \otimes |+\rangle_B
     = \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right) \otimes \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right)
     = \frac{1}{2}\bigl(|00\rangle + |01\rangle + |10\rangle + |11\rangle\bigr).
     $$

   - **结论与边界回验**：四项概率之和 $4 \times (1/2)^2 = 1$。作一个最小反例对照：若仅把最后一项改负号得到 $\frac{1}{2}(|00\rangle + |01\rangle + |10\rangle - |11\rangle)$，虽然同样有四项，但 $ad - bc = \frac{1}{2}\left(-\frac{1}{2}\right) - \frac{1}{2}\cdot\frac{1}{2} = -\frac{1}{2} \neq 0$，它反而是最大纠缠态。
   - **易错坑提醒**：**项数多绝不等于纠缠**；能否因式分解取决于四个系数是否满足成比例关系 $ad = bc$，必须用代数判据计算，不能凭展开后有几项肉眼猜。

7. **【计算】两边测 $X$ 基对比 $|\Phi^+\rangle$ 与 $\rho_{\mathrm{mix}}$ 的联合概率分布**

   - **题意与约定**：两比特 $X$ 基为 $\{|++\rangle, |+-\rangle, |-+\rangle, |--\rangle\}$。利用逆换基公式 $|0\rangle = \frac{|+\rangle + |-\rangle}{\sqrt{2}}$、$|1\rangle = \frac{|+\rangle - |-\rangle}{\sqrt{2}}$，分别计算 $|\Phi^+\rangle$ 与 $\rho_{\mathrm{mix}} = \frac{1}{2}|00\rangle\langle 00| + \frac{1}{2}|11\rangle\langle 11|$ 的四组概率。
   - **核心提示**：利用 $|0\rangle=\frac{|+\rangle+|-\rangle}{\sqrt{2}}$、$|1\rangle=\frac{|+\rangle-|-\rangle}{\sqrt{2}}$ 将 $|\Phi^+\rangle$ 与 $\rho_{\mathrm{mix}}$ 中的 $|00\rangle,|11\rangle$ 换到两比特 $X$ 基，再比较四项联合概率。
   - **完整分步演算**：
     - **对纠缠纯态 $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$**：先逐项把 $|00\rangle$ 与 $|11\rangle$ 展开到 $X$ 基：

       $$
       \begin{aligned}
       |00\rangle &= \frac{|+\rangle + |-\rangle}{\sqrt{2}} \otimes \frac{|+\rangle + |-\rangle}{\sqrt{2}}
                   = \frac{1}{2}\bigl(|++\rangle + |+-\rangle + |-+\rangle + |--\rangle\bigr), \\
       |11\rangle &= \frac{|+\rangle - |-\rangle}{\sqrt{2}} \otimes \frac{|+\rangle - |-\rangle}{\sqrt{2}}
                   = \frac{1}{2}\bigl(|++\rangle - |+-\rangle - |-+\rangle + |--\rangle\bigr).
       \end{aligned}
       $$

       两式相加再除以 $\sqrt{2}$，交叉项 $|+-\rangle$ 与 $|-+\rangle$ 正负精确抵消：

       $$
       |\Phi^+\rangle
       = \frac{1}{2\sqrt{2}}\bigl(2|++\rangle + 2|--\rangle\bigr)
       = \frac{|++\rangle + |--\rangle}{\sqrt{2}}.
       $$

       逐项取模平方，按 $++, +-, -+, --$ 顺序得概率：

       $$
       p_{\Phi^+}(++) = \frac{1}{2}, \qquad
       p_{\Phi^+}(+-) = 0, \qquad
       p_{\Phi^+}(-+) = 0, \qquad
       p_{\Phi^+}(--) = \frac{1}{2}.
       $$

     - **对经典混态 $\rho_{\mathrm{mix}}$**：按乘积内积规则，单比特内积满足 $|\langle \pm|0\rangle|^2 = |\langle \pm|1\rangle|^2 = \frac{1}{2}$。因此对分支 $|00\rangle$，任意 $X$ 基结果 $s_1 s_2 \in \{++, +-, -+, --\}$ 的概率均为

       $$
       |\langle s_1 s_2|00\rangle|^2
       = |\langle s_1|0\rangle|^2 \, |\langle s_2|0\rangle|^2
       = \frac{1}{2} \cdot \frac{1}{2}
       = \frac{1}{4}.
       $$

       同理分支 $|11\rangle$ 的四个概率也各为 $\frac{1}{4}$。以各 $\frac{1}{2}$ 权重加权平均，得：

       $$
       p_{\mathrm{mix}}(s_1 s_2)
       = \frac{1}{2}\cdot\frac{1}{4} + \frac{1}{2}\cdot\frac{1}{4}
       = \frac{1}{4} \qquad \bigl(\text{四组依次为 } \tfrac{1}{4},\; \tfrac{1}{4},\; \tfrac{1}{4},\; \tfrac{1}{4}\bigr).
       $$

   - **结论与边界回验**：两组概率各自相加：$|\Phi^+\rangle$ 为 $\frac{1}{2} + 0 + 0 + \frac{1}{2} = 1$；$\rho_{\mathrm{mix}}$ 为 $\frac{1}{4} + \frac{1}{4} + \frac{1}{4} + \frac{1}{4} = 1$，均精确归一化。
   - **易错坑提醒**：$|\Phi^+\rangle$ 在 $X$ 基的相消干涉依赖于 $|00\rangle$ 与 $|11\rangle$ 之间的相干叠加；经典混态 $\rho_{\mathrm{mix}}$ 是“先算概率再相加”，没有跨分支振幅干涉，因此四种结果彻底打平为各 $1/4$。

8. **【计算】从 $\rho_{AB}$ 逐格相加求非均匀纠缠态的约化态 $\rho_A$**

   - **题意与约定**：给定归一化两比特纯态 $|\psi\rangle = \frac{\sqrt{3}|00\rangle + |11\rangle}{2} = \begin{bmatrix} \sqrt{3}/2 \\ 0 \\ 0 \\ 1/2 \end{bmatrix} \in \mathbb{C}^4$（大端序 `00, 01, 10, 11`）。对 $B$ 求偏迹的矩阵元公式为 $(\rho_A)_{ac} = \sum_{b=0}^1 \rho_{ab, cb} = \rho_{a0,c0} + \rho_{a1,c1}$。
   - **核心提示**：先把非均匀纠缠态写成 $4\times 4$ 矩阵 $\rho_{AB}$，再按偏迹分块公式 $(\rho_A)_{ij}=\sum_{k\in\{0,1\}}(\rho_{AB})_{ik,jk}$ 逐格把左上、右上、左下、右下四个 $2\times 2$ 块的主对角相加。
   - **完整分步演算**：先按列乘行写出 $4 \times 4$ 联合密度矩阵 $\rho_{AB} = |\psi\rangle\langle\psi|$：

     $$
     \rho_{AB}
     = \begin{bmatrix} \sqrt{3}/2 \\ 0 \\ 0 \\ 1/2 \end{bmatrix}
       \begin{bmatrix} \sqrt{3}/2 & 0 & 0 & 1/2 \end{bmatrix}
     = \begin{bmatrix}
       3/4 & 0 & 0 & \sqrt{3}/4 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       \sqrt{3}/4 & 0 & 0 & 1/4
       \end{bmatrix}.
     $$

     再按“把 $B$ 的行、列标签相同的对应两格相加”（等价于对四个 $2 \times 2$ 子块逐块取迹）算出 $\rho_A$ 的全部四格：

     $$
     \begin{aligned}
     (\rho_A)_{00} &= \rho_{00,00} + \rho_{01,01} = \frac{3}{4} + 0 = \frac{3}{4}, \\
     (\rho_A)_{01} &= \rho_{00,10} + \rho_{01,11} = 0 + 0 = 0, \\
     (\rho_A)_{10} &= \rho_{10,00} + \rho_{11,01} = 0 + 0 = 0, \\
     (\rho_A)_{11} &= \rho_{10,10} + \rho_{11,11} = 0 + \frac{1}{4} = \frac{1}{4}.
     \end{aligned}
     $$

     拼成 $2 \times 2$ 约化密度矩阵：

     $$
     \rho_A = \begin{bmatrix} 3/4 & 0 \\ 0 & 1/4 \end{bmatrix}.
     $$

   - **结论与边界回验**：$\operatorname{Tr}(\rho_A) = \frac{3}{4} + \frac{1}{4} = 1$，本征值 $\frac{3}{4}, \frac{1}{4} \ge 0$（正半定），纯度 $\operatorname{Tr}(\rho_A^2) = \frac{9}{16} + \frac{1}{16} = \frac{10}{16} = \frac{5}{8} \in (1/2, 1)$，表明 $|\psi\rangle$ 是部分纠缠态（既非可分纯态，也非最大纠缠态）。
   - **易错坑提醒**：不要误把 $\rho_{AB}$ 右上角的 $\sqrt{3}/4$（坐标是 `00, 11`，这里 $B$ 的行标 $0 \neq$ 列标 $1$）加进 $(\rho_A)_{01}$ 里——偏迹只对 $B$ 下标**相同**的对角位求和。

9. **【计算】对第 8 题态的 $A$ 位做计算基测量：概率、条件后态与非选择态**

   - **题意与约定**：沿用第 8 题纯态 $|\psi\rangle = \frac{\sqrt{3}}{2}|00\rangle + \frac{1}{2}|11\rangle$。仅在 $A$ 位做计算基投影测量，对应四维投影算符为 $P_0 = |0\rangle\langle 0|_A \otimes I_B$ 与 $P_1 = |1\rangle\langle 1|_A \otimes I_B$。
   - **核心提示**：构造仅作用在 $A$ 位的投影算符 $P_0=|0\rangle\langle 0|\otimes I_B$ 与 $P_1=|1\rangle\langle 1|\otimes I_B$，先求概率 $p_m=\langle\psi|P_m|\psi\rangle$ 与归一化条件联合后态，再按概率加权求和得非选择态。
   - **完整分步演算**：分别计算两个投影后的未归一化分支、发生概率及除以 $\sqrt{p}$ 后的归一化条件联合后态：

     $$
     P_0|\psi\rangle = \frac{\sqrt{3}}{2}|00\rangle,
     \qquad
     p(0) = \|P_0|\psi\rangle\|^2 = \left|\frac{\sqrt{3}}{2}\right|^2 = \frac{3}{4},
     \qquad
     |\psi_{\mid 0}\rangle = \frac{P_0|\psi\rangle}{\sqrt{3/4}} = \frac{(\sqrt{3}/2)|00\rangle}{\sqrt{3}/2} = |00\rangle,
     $$

     $$
     P_1|\psi\rangle = \frac{1}{2}|11\rangle,
     \qquad
     p(1) = \|P_1|\psi\rangle\|^2 = \left|\frac{1}{2}\right|^2 = \frac{1}{4},
     \qquad
     |\psi_{\mid 1}\rangle = \frac{P_1|\psi\rangle}{\sqrt{1/4}} = \frac{(1/2)|11\rangle}{1/2} = |11\rangle.
     $$

     若测量已经执行但丢弃结果记录，不能任选其一，联合状态变为按概率加权的非选择混态密度矩阵：

     $$
     \rho'_{AB}
     = p(0)|00\rangle\langle 00| + p(1)|11\rangle\langle 11|
     = \frac{3}{4}|00\rangle\langle 00| + \frac{1}{4}|11\rangle\langle 11|
     = \begin{bmatrix}
       3/4 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 1/4
       \end{bmatrix}.
     $$

   - **结论与边界回验**：概率和 $p(0) + p(1) = \frac{3}{4} + \frac{1}{4} = 1$；非选择态的迹 $\operatorname{Tr}(\rho'_{AB}) = 1$。再做**无信号独立回验**：对 $\rho'_{AB}$ 求 $A$ 侧偏迹得 $\operatorname{Tr}_A(\rho'_{AB}) = \frac{3}{4}|0\rangle\langle 0| + \frac{1}{4}|1\rangle\langle 1| = \operatorname{diag}(3/4, 1/4)$，与测量前对原态 $\rho_{AB}$ 求得的 $\rho_B$ 完全相同！
   - **易错坑提醒**：对比 $\rho_{AB}$ 与 $\rho'_{AB}$ 可以看到，对 $A$ 测计算基后丢弃记录，恰好清零了 $\rho_{AB}$ 右上与左下角的相干项 $\sqrt{3}/4$，把纠缠纯态变成了经典相关的可分混态。

10. **【计算】两边测 $X$ 基计算 $|\Phi^-\rangle$ 的可能结果与概率**

    - **题意与约定**：给定 Bell 态 $|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}$，将其变换到两比特 $X$ 基 $\{|++\rangle, |+-\rangle, |-+\rangle, |--\rangle\}$ 下求各联合结果概率。
    - **核心提示**：将 $|0\rangle=(|+\rangle+|-\rangle)/\sqrt{2}$ 与 $|1\rangle=(|+\rangle-|-\rangle)/\sqrt{2}$ 代入 $|\Phi^-\rangle=(|00\rangle-|11\rangle)/\sqrt{2}$，展开并合并同类项，观察哪些 $X$ 基项相消。
    - **完整分步演算**：代入第 7 题中已逐项乘开的 $|00\rangle$ 与 $|11\rangle$ 的 $X$ 基展开式，这次执行**相减**操作：

      $$
      \begin{aligned}
      |\Phi^-\rangle
      &= \frac{|00\rangle - |11\rangle}{\sqrt{2}} \\
      &= \frac{1}{2\sqrt{2}}\Bigl[\bigl(|++\rangle + |+-\rangle + |-+\rangle + |--\rangle\bigr)
         - \bigl(|++\rangle - |+-\rangle - |-+\rangle + |--\rangle\bigr)\Bigr] \\
      &= \frac{1}{2\sqrt{2}}\bigl(0\cdot|++\rangle + 2|+-\rangle + 2|-+\rangle + 0\cdot|--\rangle\bigr) \\
      &= \frac{|+-\rangle + |-+\rangle}{\sqrt{2}}.
      \end{aligned}
      $$

      逐项取模平方，得四种可能结果的概率：

      $$
      p(++) = 0, \qquad
      p(+-) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}, \qquad
      p(-+) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}, \qquad
      p(--) = 0.
      $$

      因此只有反关联的 $+-$ 与 $-+$ 两个结果可能出现，概率各为 $1/2$。
    - **结论与边界回验**：四项概率之和 $0 + \frac{1}{2} + \frac{1}{2} + 0 = 1$；也可通过内积回验 $|\Phi^-\rangle$ 与 $|\Phi^+\rangle = \frac{|++\rangle+|--\rangle}{\sqrt{2}}$ 正交：$\langle\Phi^+|\Phi^-\rangle = 0$，两态在 $X$ 基下的非零支撑集完全互补。
    - **易错坑提醒**：计算基的相对负号（$|00\rangle - |11\rangle$）在计算基下看不出与 $|\Phi^+\rangle$ 的差别，但切到 $X$ 基后立即把关联方向从“必同号（$++, --$）”整体翻转成“必反号（$+-, -+$）”。

11. **【进阶】为什么 $\rho_{\mathrm{mix}}$ 的局部熵为 $1\ \mathrm{bit}$ 却不代表有 $1\ \mathrm{bit}$ 纠缠**

    - **题意与约定**：冯·诺依曼熵定义为 $S(\rho) = -\operatorname{Tr}(\rho\log_2\rho) = -\sum_j \lambda_j \log_2 \lambda_j$（以 $2$ 为底，单位为 $\mathrm{bit}$，约定 $0\log_2 0 = 0$）。对比 $\rho_{\mathrm{mix}} = \frac{1}{2}|00\rangle\langle 00| + \frac{1}{2}|11\rangle\langle 11|$ 与纯态 $\rho_{\mathrm{ent}} = |\Phi^+\rangle\langle\Phi^+|$ 的局部熵与联合熵。
    - **核心提示**：对比 $\rho_{\mathrm{mix}}$ 与 $|\Phi^+\rangle$ 的约化态与整体纯度：先检验 $\rho_{\mathrm{mix}}$ 能否写成乘积态的凸组合（可分定义），再说明局部熵仅在整体为纯态时才度量纠缠。
    - **完整分步演算**：先对 $\rho_{\mathrm{mix}}$ 求偏迹得 $\rho_A = \operatorname{Tr}_B(\rho_{\mathrm{mix}}) = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{I}{2}$，其两个特征值均为 $\frac{1}{2}$，故局部熵为：

      $$
      S(\rho_A)
      = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2}
      = -\frac{1}{2}(-1) - \frac{1}{2}(-1)
      = 1\ \mathrm{bit}.
      $$

      然而检验**联合态本身**的特征值与联合熵：$\rho_{\mathrm{mix}} = \operatorname{diag}(1/2, 0, 0, 1/2)$ 的特征值为 $\{1/2, 1/2, 0, 0\}$，因此其联合熵为：

      $$
      S(\rho_{\mathrm{mix}})
      = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2}
      = 1\ \mathrm{bit} > 0.
      $$

      作为对比，纠缠纯态 $\rho_{\mathrm{ent}}$ 的特征值为 $\{1, 0, 0, 0\}$，其联合熵 $S(\rho_{\mathrm{ent}}) = -1\log_2 1 = 0\ \mathrm{bit}$。因为 $\rho_{\mathrm{mix}}$ 本身就是两个乘积态 $|00\rangle$ 与 $|11\rangle$ 的 $50/50$ 经典概率混合，按定义属于**可分混态**（纠缠度严格为 $0$），它局部呈现的 $1\ \mathrm{bit}$ 熵完全来自我们对“经典硬币翻出哪一面”的无知，而非量子纠缠。
      **跨章侧重对照（第一篇态几何视角）**：本题立足“局部 Bloch 球心 vs 整体可分凸分解”建立几何直觉；若想看同一问题在连续 Werner 态族中的 PPT 负性跃迁，见[第 13 章第 6 题](#第-13-章)；若想从量子相干信息与可蒸馏纠缠收束，见[第 18 章第 13 题](#第-18-章)。
    - **结论与边界回验**：按定义检验可分性：$\rho_{\mathrm{mix}} = \sum_{k=0}^1 p_k \rho_A^{(k)} \otimes \rho_B^{(k)}$（其中 $p_0 = p_1 = \frac{1}{2}$，$\rho_A^{(k)} = \rho_B^{(k)} = |k\rangle\langle k|$），完全符合可分混态定义；其部分转置 $\rho_{\mathrm{mix}}^{T_B} = \rho_{\mathrm{mix}} \succeq 0$ 亦无任何负特征值。
    - **易错坑提醒**：**只有当二分联合态整体是纯态（$S(\rho_{AB}) = 0$）时**，子系统的约化熵 $S(\rho_A) = S(\rho_B)$ 才可以直接作为该二分态的纠缠熵；一旦联合态本身是混态，绝不能拿局部熵直接断言存在纠缠。

## 第 4 章

1. **【基础】写出 $\mathrm{CNOT}_{1\to 2}$ 的 $4 \times 4$ 矩阵并核对第 3 列**

   - **题意与约定**：两比特态空间为 $\mathbb{C}^4$，固定高位在左的大端序计算基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$，依次对应第 $1, 2, 3, 4$ 个标准单位列向量。第一位为控制位、第二位为目标位：控制位为 $0$ 时目标位不变，控制位为 $1$ 时目标位翻转（$0 \leftrightarrow 1$）。
   - **核心提示**：按大端序基 $(|00\rangle,|01\rangle,|10\rangle,|11\rangle)$ 依次列出 CNOT 对四个基态的像，把每个像的坐标向量摆成对应列；第 3 列即输入第 3 个基态 $|10\rangle$ 时的输出。
   - **完整分步演算**：逐个计算四个计算基态的输出向量：

     $$
     \begin{aligned}
     \mathrm{CNOT}_{1\to 2}|00\rangle &= |00\rangle = \begin{bmatrix} 1 \\ 0 \\ 0 \\ 0 \end{bmatrix}, &
     \mathrm{CNOT}_{1\to 2}|01\rangle &= |01\rangle = \begin{bmatrix} 0 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \\
     \mathrm{CNOT}_{1\to 2}|10\rangle &= |11\rangle = \begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \end{bmatrix}, &
     \mathrm{CNOT}_{1\to 2}|11\rangle &= |10\rangle = \begin{bmatrix} 0 \\ 0 \\ 1 \\ 0 \end{bmatrix}.
     \end{aligned}
     $$

     按矩阵的列规则（第 $j$ 列等于第 $j$ 个基态的输出列向量），把四个输出列依次排开得到 $4 \times 4$ 矩阵：

     $$
     \mathrm{CNOT}_{1\to 2}
     = \begin{bmatrix}
       1 & 0 & 0 & 0 \\
       0 & 1 & 0 & 0 \\
       0 & 0 & 0 & 1 \\
       0 & 0 & 1 & 0
       \end{bmatrix}.
     $$

     **第 3 列的由来**：在大端序 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$ 中，第 $3$ 个基态是 $|10\rangle$；它的第一控制位是 $1$，因此第二目标位从 $0$ 翻转成 $1$，输出为第 $4$ 个基态 $|11\rangle = [0, 0, 0, 1]^T$，于是矩阵第 $3$ 列唯一的 $1$ 落在第 $4$ 行。
   - **结论与边界回验**：每行每列恰有一个 $1$（置换矩阵），故满足酉性 $\mathrm{CNOT}^\dagger\mathrm{CNOT} = I_4$；且它是实对称矩阵，$\mathrm{CNOT}^2 = I_4$。
   - **易错坑提醒**：如果改用小端序软件把 $q_0$ 放在最右侧，相同的“$q_0$ 控制 $q_1$”矩阵会变成翻转 $|01\rangle \leftrightarrow |11\rangle$ 的不同置换矩阵；动笔写矩阵前必须先锁定基序与哪一位做控制位。

2. **【计算】从 $|01\rangle$ 经 $H \otimes I$ 与 $\mathrm{CNOT}$ 制备 $|\Psi^+\rangle$ 并求测量概率**

   - **题意与约定**：两比特大端序基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$。电路先对第一比特做 $H$（第二比特做恒等 $I$），再施加第一位控制、第二位目标的 $\mathrm{CNOT}_{1\to 2}$。
   - **核心提示**：先对第一比特做 $H$（第二比特保持 $I$）得到中间叠加态，再逐项按“控制位为 $1$ 时翻转目标位”规则施加 CNOT，最后读出各基态振幅的模平方。
   - **完整分步演算**：第一步用张量积混合乘积律 $(H\otimes I)(|u\rangle\otimes|v\rangle) = (H|u\rangle)\otimes(I|v\rangle)$ 展开：

     $$
     |\psi_1\rangle
     = (H \otimes I)|01\rangle
     = (H|0\rangle) \otimes (I|1\rangle)
     = \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right) \otimes |1\rangle
     = \frac{|01\rangle + |11\rangle}{\sqrt{2}}.
     $$

     第二步逐项施加 $\mathrm{CNOT}_{1\to 2}$（$|01\rangle \mapsto |01\rangle$，$|11\rangle \mapsto |10\rangle$）：

     $$
     |\psi_2\rangle
     = \mathrm{CNOT}_{1\to 2}\!\left(\frac{|01\rangle + |11\rangle}{\sqrt{2}}\right)
     = \frac{|01\rangle + |10\rangle}{\sqrt{2}}
     = |\Psi^+\rangle
     = \begin{bmatrix} 0 \\ 1/\sqrt{2} \\ 1/\sqrt{2} \\ 0 \end{bmatrix}.
     $$

     对四个计算基振幅逐项取模平方，得测量概率：

     $$
     p(01) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}, \qquad
     p(10) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}, \qquad
     p(00) = p(11) = 0.
     $$

   - **结论与边界回验**：四项概率之和 $0 + \frac{1}{2} + \frac{1}{2} + 0 = 1$；检查系数行列式 $ad - bc = 0\cdot 0 - \frac{1}{\sqrt{2}}\cdot\frac{1}{\sqrt{2}} = -\frac{1}{2} \neq 0$，确认输出态 $|\Psi^+\rangle$ 是最大纠缠态。
   - **易错坑提醒**：不要以为 $H$ 接 $\mathrm{CNOT}$ 永远只造出 $|\Phi^+\rangle = \frac{|00\rangle+|11\rangle}{\sqrt{2}}$——该标准 Bell 制备电路会把四个计算基态 $|00\rangle, |01\rangle, |10\rangle, |11\rangle$ 一一对应地映成四个正交 Bell 态 $|\Phi^+\rangle, |\Psi^+\rangle, |\Phi^-\rangle, |\Psi^-\rangle$。

3. **【计算】用矩阵乘法把四分量叠加态送入 $\mathrm{CNOT}$ 并检验自逆性**

   - **题意与约定**：按大端序 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$，给定四维列向量 $|v\rangle = \frac{1}{\sqrt{30}}\begin{bmatrix} 1 \\ 2 \\ 3 \\ 4 \end{bmatrix} \in \mathbb{C}^4$，施加第 1 题矩阵 $\mathrm{CNOT}_{1\to 2}$。
   - **核心提示**：把四维列向量写成 $(a_{00},a_{01},a_{10},a_{11})^T$，左乘 CNOT 矩阵相当于交换后两个分量；再施加一次 CNOT 检验是否回到原向量以验证 $\mathrm{CNOT}^2=I$。
   - **完整分步演算**：直接用 $4 \times 4$ 矩阵逐行乘以列向量 $|v\rangle$：

     $$
     |v'\rangle
     = \mathrm{CNOT}_{1\to 2}|v\rangle
     = \begin{bmatrix}
       1 & 0 & 0 & 0 \\
       0 & 1 & 0 & 0 \\
       0 & 0 & 0 & 1 \\
       0 & 0 & 1 & 0
       \end{bmatrix}
       \left(\frac{1}{\sqrt{30}}\begin{bmatrix} 1 \\ 2 \\ 3 \\ 4 \end{bmatrix}\right)
     = \frac{1}{\sqrt{30}}\begin{bmatrix}
       1\cdot 1 + 0 + 0 + 0 \\
       0 + 1\cdot 2 + 0 + 0 \\
       0 + 0 + 0 + 1\cdot 4 \\
       0 + 0 + 1\cdot 3 + 0
       \end{bmatrix}
     = \frac{1}{\sqrt{30}}\begin{bmatrix} 1 \\ 2 \\ 4 \\ 3 \end{bmatrix}.
     $$

     写回狄拉克记号为：

     $$
     |v'\rangle = \frac{|00\rangle + 2|01\rangle + 4|10\rangle + 3|11\rangle}{\sqrt{30}}.
     $$

     再做一次 $\mathrm{CNOT}_{1\to 2}$，同样逐行相乘：

     $$
     \mathrm{CNOT}_{1\to 2}|v'\rangle
     = \begin{bmatrix}
       1 & 0 & 0 & 0 \\
       0 & 1 & 0 & 0 \\
       0 & 0 & 0 & 1 \\
       0 & 0 & 1 & 0
       \end{bmatrix}
       \left(\frac{1}{\sqrt{30}}\begin{bmatrix} 1 \\ 2 \\ 4 \\ 3 \end{bmatrix}\right)
     = \frac{1}{\sqrt{30}}\begin{bmatrix} 1 \\ 2 \\ 3 \\ 4 \end{bmatrix}
     = |v\rangle,
     $$

     因此连续做两次 $\mathrm{CNOT}$ 会精准回到原输入态 $|v\rangle$。
   - **结论与边界回验**：检查输入与输出的范数平方：

     $$
     \||v'\rangle\|^2
     = \frac{1^2 + 2^2 + 4^2 + 3^2}{30}
     = \frac{1 + 4 + 16 + 9}{30}
     = \frac{30}{30}
     = 1,
     $$

     与输入长度 $1$ 严格守恒，且逐分量印证了 $\mathrm{CNOT}^2 = I_4$。
   - **易错坑提醒**：$\mathrm{CNOT}$ 作用在叠加态上并不是“先把控制位测成 $0$ 或 $1$ 再决定翻不翻”，而是按线性性同时对后两个基态分量 $|10\rangle$ 与 $|11\rangle$ 交换振幅。

4. **【计算】量子隐形传态中测得 `10` 时的条件态、校正与结果概率**

   - **题意与约定**：三比特顺序固定为 $Q, A, B$（Alice 持有 $Q, A$，Bob 持有 $B$）。未知输入态 $|\psi\rangle_Q = \frac{\sqrt{3}}{2}|0\rangle + \frac{1}{2}|1\rangle$（即 $\alpha = \frac{\sqrt{3}}{2},\; \beta = \frac{1}{2}$），预共享 Bell 态为 $|\Phi^+\rangle_{AB} = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$。
   - **核心提示**：将隐形传态三比特初态 $|\psi\rangle_Q|\Phi^+\rangle_{AB}$ 按前两比特 $(Q,A)$ 的四个 Bell 基（或经过 $\mathrm{CNOT}_{Q\to A}$ 与 $H_Q$ 后的计算基）改写，挑出 `10` 分支读出 Bob 条件态与所需 Pauli 校正门。
   - **完整分步演算**：按第 4 章第 5.1 节的传态核心恒等式，Alice 完成 $\mathrm{CNOT}_{Q\to A}$ 与 $H_Q$ 后三比特联合态为：

     $$
     \begin{aligned}
     |\Omega\rangle_{QAB}
     = \frac{1}{2}\Bigl[\;&
       |00\rangle_{QA}(\alpha|0\rangle + \beta|1\rangle)_B
       + |01\rangle_{QA}(\beta|0\rangle + \alpha|1\rangle)_B \\
     &+ |10\rangle_{QA}(\alpha|0\rangle - \beta|1\rangle)_B
       + |11\rangle_{QA}(-\beta|0\rangle + \alpha|1\rangle)_B
       \Bigr].
     \end{aligned}
     $$

     抽出 Alice 测得 $QA = 10$ 对应的未归一化分支（代入 $\alpha = \frac{\sqrt{3}}{2},\; \beta = \frac{1}{2}$）：

     $$
     |\tilde{\phi}_{10}\rangle_B
     = \frac{1}{2}\bigl(\alpha|0\rangle - \beta|1\rangle\bigr)
     = \frac{1}{2}\left(\frac{\sqrt{3}}{2}|0\rangle - \frac{1}{2}|1\rangle\right)
     = \frac{\sqrt{3}}{4}|0\rangle - \frac{1}{4}|1\rangle.
     $$

     第一步求测得 `10` 的概率——对未归一化分支的各振幅取模平方求和：

     $$
     p(10)
     = \left|\frac{\sqrt{3}}{4}\right|^2 + \left|-\frac{1}{4}\right|^2
     = \frac{3}{16} + \frac{1}{16}
     = \frac{4}{16}
     = \frac{1}{4}.
     $$

     第二步将未归一化分支除以 $\sqrt{p(10)} = \frac{1}{2}$，得 Bob 校正前的**归一化条件态**：

     $$
     |\phi_{10}\rangle_B
     = \frac{|\tilde{\phi}_{10}\rangle_B}{1/2}
     = \frac{\sqrt{3}}{2}|0\rangle - \frac{1}{2}|1\rangle
     = Z|\psi\rangle.
     $$

     第三步 Bob 收到经典消息 `10` 后，对 $B$ 施加本地 $Z$ 门，逐行矩阵乘得校正后的态：

     $$
     Z|\phi_{10}\rangle_B
     = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
       \begin{bmatrix} \sqrt{3}/2 \\ -1/2 \end{bmatrix}
     = \begin{bmatrix} \sqrt{3}/2 \\ +1/2 \end{bmatrix}
     = \frac{\sqrt{3}|0\rangle + |1\rangle}{2}
     = |\psi\rangle.
     $$

   - **结论与边界回验**：输入态归一化 $\frac{3}{4} + \frac{1}{4} = 1$；校正前条件态长度平方 $\frac{3}{4} + \frac{1}{4} = 1$；其余三支 `00, 01, 11` 概率同样均为 $\frac{1}{4}$，四支总概率 $4 \times \frac{1}{4} = 1$。
   - **易错坑提醒**：不要看到校正前的归一化条件态长度为 $1$ 就误以为 `10` 的发生概率是 $1$——概率必须从测量前带着整体因子 $\frac{1}{2}$ 的**未归一化分支** $|\tilde{\phi}_{10}\rangle_B$ 算模平方得到。

5. **【进阶】不假定具体系数：一般证明未收消息时 Bob 局部态恒为 $I/2$**

   - **题意与约定**：设 Alice 输入的是**任意**归一化未知单比特纯态 $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$，仅知 $|\alpha|^2 + |\beta|^2 = 1$（不对 $\alpha, \beta$ 赋任何具体数值），其输入密度矩阵记作 $\rho = |\psi\rangle\langle\psi| = \begin{bmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{bmatrix}$。
   - **核心提示**：对任意未知态 $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$，把 Alice 测量四种结果对应的 Bob 条件态连同各自概率 $1/4$ 做凸组合求和（或直接对初态后演化态求 $Q,A$ 的偏迹），利用 $|\alpha|^2+|\beta|^2=1$ 化简。
   - **完整分步演算**：由第 4 题的传态恒等式 $|\Omega\rangle_{QAB}$，四个测量结果 `00, 01, 10, 11` 各自的概率均为 $\frac{1}{4}(|\alpha|^2 + |\beta|^2) = \frac{1}{4}$，与 $\alpha, \beta$ 无关；对应 Bob 的四个归一化条件态依次为 $|\psi\rangle$、$X|\psi\rangle$、$Z|\psi\rangle$、$XZ|\psi\rangle$。因为 Bob 尚未收到 Alice 的两位经典消息，他手里的无条件局部约化密度矩阵是这四个等概率分支的统计混合：

     $$
     \rho_B
     = \frac{1}{4}\Bigl(
       |\psi\rangle\langle\psi|
       + X|\psi\rangle\langle\psi|X^\dagger
       + Z|\psi\rangle\langle\psi|Z^\dagger
       + XZ|\psi\rangle\langle\psi|(XZ)^\dagger
       \Bigr)
     = \frac{1}{4}\bigl(\rho + X\rho X + Z\rho Z + XZ\rho ZX\bigr).
     $$

     利用 $X^\dagger = X$、$Z^\dagger = Z$、$(XZ)^\dagger = Z^\dagger X^\dagger = ZX$，逐格算出这四张 $2 \times 2$ 矩阵：

     $$
     \begin{aligned}
     \rho
     &= \begin{bmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{bmatrix}, &
     X\rho X
     &= \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
        \begin{bmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{bmatrix}
        \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
      = \begin{bmatrix} |\beta|^2 & \alpha^*\beta \\ \alpha\beta^* & |\alpha|^2 \end{bmatrix}, \\
     Z\rho Z
     &= \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
        \begin{bmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{bmatrix}
        \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
      = \begin{bmatrix} |\alpha|^2 & -\alpha\beta^* \\ -\alpha^*\beta & |\beta|^2 \end{bmatrix}, &
     XZ\rho ZX
     &= X(Z\rho Z)X
      = \begin{bmatrix} |\beta|^2 & -\alpha^*\beta \\ -\alpha\beta^* & |\alpha|^2 \end{bmatrix}.
     \end{aligned}
     $$

     将四张矩阵逐格相加并除以 $4$：
     - 左上格与右下格均为 $\frac{1}{4}\bigl(|\alpha|^2 + |\beta|^2 + |\alpha|^2 + |\beta|^2\bigr) = \frac{2(|\alpha|^2 + |\beta|^2)}{4} = \frac{1}{2}$；
     - 右上格为 $\frac{1}{4}\bigl(\alpha\beta^* + \alpha^*\beta - \alpha\beta^* - \alpha^*\beta\bigr) = 0$；
     - 左下格为 $\frac{1}{4}\bigl(\alpha^*\beta + \alpha\beta^* - \alpha^*\beta - \alpha\beta^*\bigr) = 0$。

     合并得对**一切**归一化输入态恒成立的精确结论：

     $$
     \rho_B
     = \frac{1}{4}\begin{bmatrix} 2(|\alpha|^2 + |\beta|^2) & 0 \\ 0 & 2(|\alpha|^2 + |\beta|^2) \end{bmatrix}
     = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
     = \frac{I}{2}.
     $$

     因为 $\rho_B = I/2$ 中完全不含有 $\alpha$ 和 $\beta$ 的任何信息，输入 $|0\rangle$（$\alpha=1, \beta=0$）与输入 $|1\rangle$（$\alpha=0, \beta=1$）在 Bob 端给出**完全相同**的密度矩阵 $I/2$，无论 Bob 选何种本地测量，统计分布都丝毫不差，因此绝不可能判断输入是 $|0\rangle$ 还是 $|1\rangle$。
   - **结论与边界回验**：检验迹 $\operatorname{Tr}(\rho_B) = \frac{1}{2} + \frac{1}{2} = 1$；特例核对分支四的精确符号：$XZ|0\rangle = X(Z|0\rangle) = X|0\rangle = +|1\rangle$（无负号），而 $XZ|1\rangle = X(Z|1\rangle) = X(-|1\rangle) = -|0\rangle$（带全局负号），两种特例的四个分支均恰有两份 $|0\rangle\langle 0|$ 与两份 $|1\rangle\langle 1|$，平均后皆为 $I/2$。
   - **易错坑提醒**：证明“对任意输入都不可分辨”不能只靠代一两个特例（如 $|0\rangle$ 和 $|1\rangle$）敷衍了事，必须保留一般符号 $(\alpha, \beta)$ 展示非对角相干项 $\pm\alpha\beta^*$ 与 $\pm\alpha^*\beta$ 精确相消，且注意 $XZ|0\rangle = +|1\rangle$ 并不带负号。

6. **【计算】超密编码发送 `11`：逐拍演化与必得结果的完整推导**

   - **题意与约定**：两比特顺序为 $A, B$（大端序），初始共享 Bell 态 $|\Phi^+\rangle_{AB} = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$。Alice 依次在 $A$ 位施加 $X_A$（即 $X_A\otimes I_B$）与 $Z_A$（即 $Z_A\otimes I_B$），把比特 $A$ 送给 Bob 后，Bob 依次施加 $\mathrm{CNOT}_{A\to B}$ 与 $H_A\otimes I_B$ 并在计算基测量。
   - **核心提示**：从 $|\Phi^+\rangle_{AB}$ 出发，按题设顺序对 $A$ 位依次施加 $X_A$ 和 $Z_A$ 得到对应 Bell 态，再让 Bob 执行逆 Bell 电路（先 $\mathrm{CNOT}_{A\to B}$，再 $H_A\otimes I_B$）逐拍演算。
   - **完整分步演算**：分四拍逐项写出每一步演化：
     - **第 1 拍（Alice 施加 $X_A \otimes I_B$）**：翻转第一位 $A$（$|0\rangle \leftrightarrow |1\rangle$），第二位 $B$ 不动：

       $$
       |\psi_1\rangle
       = (X_A \otimes I_B)\!\left(\frac{|00\rangle + |11\rangle}{\sqrt{2}}\right)
       = \frac{|10\rangle + |01\rangle}{\sqrt{2}}
       = \frac{|01\rangle + |10\rangle}{\sqrt{2}}.
       $$

     - **第 2 拍（Alice 施加 $Z_A \otimes I_B$）**：第一位为 $0$ 的 $|01\rangle$ 不变，第一位为 $1$ 的 $|10\rangle$ 乘上 $-1$：

       $$
       |\psi_2\rangle
       = (Z_A \otimes I_B)\!\left(\frac{|01\rangle + |10\rangle}{\sqrt{2}}\right)
       = \frac{|01\rangle - |10\rangle}{\sqrt{2}}
       = |\Psi^-\rangle.
       $$

     - **第 3 拍（Bob 施加 $\mathrm{CNOT}_{A\to B}$）**：$|01\rangle$ 控制位为 $0$ 不变，$|10\rangle$ 控制位为 $1$ 翻转第二位变成 $|11\rangle$：

       $$
       |\psi_3\rangle
       = \mathrm{CNOT}_{A\to B}\!\left(\frac{|01\rangle - |10\rangle}{\sqrt{2}}\right)
       = \frac{|01\rangle - |11\rangle}{\sqrt{2}}
       = \left(\frac{|0\rangle_A - |1\rangle_A}{\sqrt{2}}\right) \otimes |1\rangle_B
       = |-\rangle_A \otimes |1\rangle_B.
       $$

     - **第 4 拍（Bob 施加 $H_A \otimes I_B$）**：展开 $H_A|-\rangle_A = \frac{H|0\rangle - H|1\rangle}{\sqrt{2}} = \frac{(|0\rangle+|1\rangle) - (|0\rangle-|1\rangle)}{2} = |1\rangle_A$：

       $$
       |\psi_4\rangle
       = (H_A \otimes I_B)\bigl(|-\rangle_A \otimes |1\rangle_B\bigr)
       = (H_A|-\rangle_A) \otimes |1\rangle_B
       = |1\rangle_A \otimes |1\rangle_B
       = |11\rangle.
       $$

     最终在计算基测得 `11` 的概率为 $|\langle 11|11\rangle|^2 = 1$，确定性地解码出 Alice 想发送的两位经典消息 `11`。
   - **结论与边界回验**：每一步态矢量均保持归一化（模平方和始终为 $1$）；另可用第 2 题“Bell 制备电路的逆电路”快速回验：Bell 制备把 $|11\rangle \mapsto |\Psi^-\rangle$，故逆电路 $H_A \cdot \mathrm{CNOT}_{A\to B}$ 必然把 $|\Psi^-\rangle$ 准确映回 $|11\rangle$。
   - **易错坑提醒**：注意 Alice 先 $X_A$ 后 $Z_A$ 对应整体算符 $Z_A X_A$（矩阵从右到左），作用于 $|\Phi^+\rangle$ 恰好给出 $+|\Psi^-\rangle$；若顺序颠倒成先 $Z_A$ 后 $X_A$，会多出一个整体负号 $-|\Psi^-\rangle$，虽然不改最终测量概率 $1$，但按协议约定顺序演算更不易出错。

7. **【计算】受控 $Z$ 门上的相位回踢与 $H$ 门干涉转换**

   - **题意与约定**：两比特顺序为控制位 $C$、目标位 $T$（大端序）。受控 $Z$ 门定义为 $\mathrm{CZ}|0t\rangle = |0t\rangle$、$\mathrm{CZ}|1t\rangle = |1\rangle(Z|t\rangle) = (-1)^t |1t\rangle$（仅对 $|11\rangle$ 乘 $-1$）。初态为 $|+\rangle_C |1\rangle_T$。
   - **核心提示**：先把输入 $|+\rangle|1\rangle$ 展开为两项，按 $\mathrm{CZ}$ 仅给 $|11\rangle$ 附加负号的规则算出输出态并提取公因子 $|1\rangle$，看控制位变成哪个 $X$ 本征态、以及 $H$ 门如何把相对相位转成计算基确定输出。
   - **完整分步演算**：先把输入乘积态展开为计算基叠加，再逐项作用 $\mathrm{CZ}$：

     $$
     |+\rangle_C |1\rangle_T
     = \left(\frac{|0\rangle_C + |1\rangle_C}{\sqrt{2}}\right) \otimes |1\rangle_T
     = \frac{|01\rangle + |11\rangle}{\sqrt{2}},
     $$

     $$
     \mathrm{CZ}\!\left(\frac{|01\rangle + |11\rangle}{\sqrt{2}}\right)
     = \frac{\mathrm{CZ}|01\rangle + \mathrm{CZ}|11\rangle}{\sqrt{2}}
     = \frac{|01\rangle - |11\rangle}{\sqrt{2}}
     = \left(\frac{|0\rangle_C - |1\rangle_C}{\sqrt{2}}\right) \otimes |1\rangle_T
     = |-\rangle_C |1\rangle_T.
     $$

     目标位 $|1\rangle_T$ 纹丝不动，本征值 $-1$ 被“回踢”到了控制位的相对相位里。
     - **直接测控制位计算基**：控制位处于 $|-\rangle_C = \frac{1}{\sqrt{2}}|0\rangle_C - \frac{1}{\sqrt{2}}|1\rangle_C$，两项概率为

       $$
       p(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}, \qquad
       p(1) = \left|-\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2},
       $$

       负号在取模平方时消失，所以结果仍各占一半。
     - **对控制位再施加 $H_C$ 后测计算基**：逐行展开 $H_C|-\rangle_C$：

       $$
       (H_C \otimes I_T)\bigl(|-\rangle_C |1\rangle_T\bigr)
       = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}\right) \otimes |1\rangle_T
       = \begin{bmatrix} 0 \\ 1 \end{bmatrix}_C \otimes |1\rangle_T
       = |1\rangle_C |1\rangle_T.
       $$

       此时控制位测得 `1` 的概率为 $|1|^2 = 1$，必定输出 `1`。
   - **结论与边界回验**：前后两步态矢量归一化均成立，概率和分别为 $\frac{1}{2}+\frac{1}{2}=1$ 与 $0+1=1$；若目标位换成 $|0\rangle_T$（$Z|0\rangle = +|0\rangle$），控制位保持 $|+\rangle_C$，经 $H_C$ 后必得 `0`——两类本征值 $+1/-1$ 被 $100\%$ 无错分开。
   - **易错坑提醒**：不要误以为受控门永远“只改目标位、不改控制位”——一旦目标位处于受控算符的本征态而控制位处于叠加态，相位就会逆向回踢到控制位上，而这正是第 6 章诸多量子算法的核心发动机。

8. **【进阶】阐明隐形传态与合法复位为何不违反三大基本禁令**

   - **题意与约定**：依次核对不可克隆定理（Wootters–Zurek 1982）、相对论无超光速传讯（无信号定理）以及不可删除定理（Pati–Braunstein 2000）的精确适用前提与边界。
   - **核心提示**：逐一核对三条禁令的严格前提：传态是否同时保留原件（不可克隆）、未收经典比特前局部约化态是否含输入信息（无信号）、以及 $\mathrm{SWAP}$ 复位在“系统+环境”整体上是否保内积搬移（不可删除）。
   - **完整分步演算**：
     - **传态为何不违反不可克隆定理**：不可克隆定理禁止的是把单份未知态 $|\psi\rangle$ 变成同时存在的两份拷贝 $|\psi\rangle|\psi\rangle$。在隐形传态中，Alice 对 $Q, A$ 做 Bell 基测量后，她手里的 $Q, A$ 已经坍缩为经典测量结果对应态，原态信息在发送端被彻底破坏；待 Bob 收到经典消息完成校正后，全空间中**始终最多只存在一份** $|\psi\rangle$（从 $Q$ 转移到了 $B$），从未同时出现两份副本。
     - **传态为何不能超光速传讯**：如第 5 题已严格证明，在 Alice 的两位经典消息送达 Bob 之前，Bob 的无条件局部态恒为 $\rho_B = I/2$，与输入态 $|\psi\rangle$ 完全无关。Bob 必须等待经由普通经典信道传输（速度不超过光速 $c$）的两位消息 $(m, n)$ 到达后才能做校正还原，因此传态过程严格服从因果律。
     - **合法复位为何不违反不可删除定理**：不可删除定理针对的是封闭酉演化 $U|\psi\rangle|\psi\rangle|A\rangle = |\psi\rangle|0\rangle|A_\psi\rangle$，由酉性保内积推得 $\langle A_\phi|A_\psi\rangle = \langle\phi|\psi\rangle$——这意味着映射 $|\psi\rangle \mapsto |A_\psi\rangle$ 必须是**等距映射**，未知量子态绝不能在封闭系统内被无痕抹除或部分压缩，只能整份搬移进辅助系统。拿系统 $S$ 与初态为 $|0\rangle_E$ 的环境比特 $E$ 做一次 $\mathrm{SWAP}$：

       $$
       |\psi\rangle_S |0\rangle_E \xrightarrow{\mathrm{SWAP}} |0\rangle_S |\psi\rangle_E.
       $$

       局部只看 $S$ 时，它确实干净地复位回了 $|0\rangle_S$；但放眼封闭整体 $S + E$，原态 $|\psi\rangle$ 正如等距搬移定理所预言的那样，原封不动地转存到了环境 $E$ 里（随后实验者丢弃环境不再追踪），并没有从宇宙中无痕消失，故丝毫不违反不可删除定理。
   - **结论与边界回验**：检查 $\mathrm{SWAP}$ 复位的内积守恒：输入内积 $\langle\phi|\psi\rangle_S\langle 0|0\rangle_E = \langle\phi|\psi\rangle$，输出内积 $\langle 0|0\rangle_S\langle\phi|\psi\rangle_E = \langle\phi|\psi\rangle$，封闭整体完全可逆、酉性严格成立。
   - **易错坑提醒**：不可删除定理禁止的是“封闭系统无痕销毁”，绝不是说量子芯片不能把比特清零复用；现实硬件的主动复位本质上都是通过谐振腔等环境把比特里的状态排走。

9. **【基础】先 $H$ 后 $Z$ 的矩阵顺序、作用结果与换序对比**

   - **题意与约定**：量子电路从左向右表示时间先后，矩阵作用于右端列向量时**从右向左**依次乘上。在 $\mathbb{C}^2$ 中，$H = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$、$Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$、$|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$。
   - **核心提示**：记住“线路从左向右、矩阵从右向左”约定：先写出“先 $H$ 后 $Z$”对应的矩阵乘积次序并作用在 $|0\rangle$ 上，再交换次序重算一次，对比两者输出态和计算基/X 基概率。
   - **完整分步演算**：先施加 $H$、再施加 $Z$，应先让 $H$ 紧挨着输入态 $|0\rangle$，再左乘 $Z$，因此整体矩阵写成 **$ZH$**（而非 $HZ$）。先用两步矩阵乘法计算 $ZH|0\rangle$：

     $$
     ZH|0\rangle
     = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix}\right)
     = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}
     = |-\rangle.
     $$

     若交换门序改成先 $Z$ 后 $H$（整体矩阵 $HZ$），逐行计算 $HZ|0\rangle$：

     $$
     HZ|0\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}
       \left(\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix}\right)
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}\begin{bmatrix} 1 \\ 0 \end{bmatrix}
     = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}
     = |+\rangle.
     $$

     检验两输出态的内积：

     $$
     \langle +|-\rangle
     = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}\right)
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}\right)
     = \frac{1 - 1}{2}
     = 0,
     $$

     可见两态严格正交。若随后再施加一个 $H$ 门并在计算基测量，前者给出 $H|-\rangle = |1\rangle$（必测得 `1`），后者给出 $H|+\rangle = |0\rangle$（必测得 `0`），一次测量即可 $100\%$ 区分。
   - **结论与边界回验**：也可先乘出两张 $2 \times 2$ 整体矩阵独立核对：$ZH = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix}$、$HZ = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}$，两者不等（$[H, Z] \neq 0$），且各自的第一列恰为 $|-\rangle$ 与 $|+\rangle$。
   - **易错坑提醒**：把电路图从左到右读出的“先 $H$ 后 $Z$”顺手抄成矩阵乘积 $HZ$ 是初学者最常犯的读写方向错位；记口诀“**电路左先做，矩阵右先乘**”可彻底避坑。

## 第 5 章

1. **【基础】计算 $|+\rangle$ 的密度矩阵 $\rho_+$ 与纯度 $\operatorname{Tr}(\rho_+^2)$**

   - **题意与约定**：给定归一化单比特纯态 $|+\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix} \in \mathbb{C}^2$，其密度矩阵为外积 $\rho_+ = |+\rangle\langle +|$，纯度定义为 $\operatorname{Tr}(\rho_+^2) \in [1/d, 1]$（单比特 $d=2$ 时范围为 $[1/2, 1]$，等于 $1$ 当且仅当为纯态）。
   - **核心提示**：按外积定义 $\rho_+=|+\rangle\langle +|$ 写出 $2\times 2$ 矩阵，再用矩阵乘法算 $\rho_+^2$ 并取对角元之和求纯度 $\operatorname{Tr}(\rho_+^2)$。
   - **完整分步演算**：先写出左矢 $\langle +| = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}$，按“列乘行”逐格算外积：

     $$
     \rho_+
     = |+\rangle\langle +|
     = \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ 1 \end{bmatrix}\right)
       \left(\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}\right)
     = \frac{1}{2}\begin{bmatrix} 1\cdot 1 & 1\cdot 1 \\ 1\cdot 1 & 1\cdot 1 \end{bmatrix}
     = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}.
     $$

     再逐格计算矩阵平方 $\rho_+^2 = \rho_+ \rho_+$：

     $$
     \rho_+^2
     = \left(\frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}\right)
       \left(\frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}\right)
     = \frac{1}{4}\begin{bmatrix} 1\cdot 1 + 1\cdot 1 & 1\cdot 1 + 1\cdot 1 \\ 1\cdot 1 + 1\cdot 1 & 1\cdot 1 + 1\cdot 1 \end{bmatrix}
     = \frac{1}{4}\begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix}
     = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
     = \rho_+.
     $$

     对主对角元求和即得纯度：

     $$
     \operatorname{Tr}(\rho_+^2) = \frac{1}{2} + \frac{1}{2} = 1.
     $$

     因为 $\operatorname{Tr}(\rho_+^2) = 1$（且 $\rho_+^2 = \rho_+$），它是纯态。
   - **结论与边界回验**：核对密度矩阵三公理：厄米性 $\rho_+^\dagger = \rho_+$，归一化 $\operatorname{Tr}(\rho_+) = \frac{1}{2} + \frac{1}{2} = 1$，行列式 $\det(\rho_+) = \frac{1}{4} - \frac{1}{4} = 0$ 故特征值为 $\{1, 0\} \succeq 0$，全部满足。
   - **易错坑提醒**：不要误把密度矩阵 $\rho_+$ 的对角元平方直接加起来当成纯度（$\frac{1}{4} + \frac{1}{4} = \frac{1}{2}$ 会漏掉两个非对角相干元 $1/2$ 的乘积贡献！），一定要先做完整的矩阵乘法 $\rho_+^2$ 再求迹。

2. **【基础】证明最大混态 $I/2$ 在任意单比特酉变换下保持不变**

   - **题意与约定**：单比特最大混态为 $\rho = \frac{I}{2} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}$，任意单比特酉矩阵 $U \in \mathrm{U}(2)$ 满足 $UU^\dagger = U^\dagger U = I$，封闭酉演化将密度矩阵映为 $\rho' = U\rho U^\dagger$。
   - **核心提示**：把 $\rho=I/2$ 代入封闭酉演化公式 $\rho'=U\rho U^\dagger$，把标量系数 $1/2$ 提到前面，利用酉矩阵定义 $UU^\dagger=I$ 一步化简。
   - **完整分步演算**：利用矩阵乘法的标量线性性、单位矩阵性质 $UI = U$ 以及酉性 $UU^\dagger = I$ 逐步化简：

     $$
     U\left(\frac{I}{2}\right)U^\dagger
     = \frac{1}{2}\,(U I U^\dagger)
     = \frac{1}{2}\,(U U^\dagger)
     = \frac{1}{2}I
     = \frac{I}{2}.
     $$

     因此最大混态 $I/2$ 经过任意单比特酉变换后**仍然是 $I/2$**，完全不变。
   - **结论与边界回验**：从 Bloch 球几何与纯度双角度回验：密度矩阵 $\rho = \frac{1}{2}(I + \vec{r}\cdot\vec{\sigma})$ 中，$I/2$ 对应球心 $\vec{r} = (0, 0, 0)$；任意单比特酉门在 Bloch 球上都是绕球心的三维刚体旋转 $R \in \mathrm{SO}(3)$，把原点映回自身 $R\vec{0} = \vec{0}$。同时纯度 $\operatorname{Tr}\bigl((I/2)^2\bigr) = \frac{1}{2}$ 保持最小不变。
   - **易错坑提醒**：酉变换改变不了最大混态 $I/2$，但**非保单位的开放量子信道**可以改变它——例如零温振幅阻尼信道 $\mathcal{A}_\gamma$ 把球心 $I/2$ 推向北极 $|0\rangle\langle 0|$，得到 $\operatorname{diag}\bigl(\frac{1+\gamma}{2},\; \frac{1-\gamma}{2}\bigr)$（本质是把熵排入低温环境，而非靠单比特封闭酉门“提纯”）。

3. **【计算】验证零温振幅阻尼信道两个 Kraus 算符的完备性**

   - **题意与约定**：零温振幅阻尼信道的弛豫概率参数满足 $\gamma \in [0, 1]$（故 $\sqrt{1-\gamma}$ 与 $\sqrt{\gamma}$ 均为非负实数），Kraus 算符为 $K_0 = \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix}$ 与 $K_1 = \begin{bmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{bmatrix}$。保迹条件（完备关系）要求 $K_0^\dagger K_0 + K_1^\dagger K_1 = I$。
   - **核心提示**：分别写出 $K_0^\dagger$ 与 $K_1^\dagger$，逐格计算矩阵乘积 $K_0^\dagger K_0$ 和 $K_1^\dagger K_1$，再相加检验是否对所有 $\gamma\in[0,1]$ 恒等于单位阵 $I$。
   - **完整分步演算**：第一步先对 $K_0, K_1$ 显式取共轭转置（因为元素皆为实数，只需转置）：

     $$
     K_0^\dagger = \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix},
     \qquad
     K_1^\dagger = \begin{bmatrix} 0 & 0 \\ \sqrt{\gamma} & 0 \end{bmatrix}.
     $$

     第二步逐格做矩阵乘法，分别算出 $K_0^\dagger K_0$ 与 $K_1^\dagger K_1$：

     $$
     K_0^\dagger K_0
     = \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix}
       \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix}
     = \begin{bmatrix} 1\cdot 1 + 0 & 0 \\ 0 & 0 + (\sqrt{1-\gamma})^2 \end{bmatrix}
     = \begin{bmatrix} 1 & 0 \\ 0 & 1-\gamma \end{bmatrix},
     $$

     $$
     K_1^\dagger K_1
     = \begin{bmatrix} 0 & 0 \\ \sqrt{\gamma} & 0 \end{bmatrix}
       \begin{bmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{bmatrix}
     = \begin{bmatrix} 0\cdot 0 + 0\cdot 0 & 0\cdot\sqrt{\gamma} + 0\cdot 0 \\ \sqrt{\gamma}\cdot 0 + 0\cdot 0 & \sqrt{\gamma}\cdot\sqrt{\gamma} + 0\cdot 0 \end{bmatrix}
     = \begin{bmatrix} 0 & 0 \\ 0 & \gamma \end{bmatrix}.
     $$

     第三步将两矩阵逐格相加：

     $$
     K_0^\dagger K_0 + K_1^\dagger K_1
     = \begin{bmatrix} 1 & 0 \\ 0 & 1-\gamma \end{bmatrix}
       + \begin{bmatrix} 0 & 0 \\ 0 & \gamma \end{bmatrix}
     = \begin{bmatrix} 1 & 0 \\ 0 & (1-\gamma) + \gamma \end{bmatrix}
     = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
     = I.
     $$

   - **结论与边界回验**：由迹的循环性立得 $\operatorname{Tr}\bigl(\mathcal{A}_\gamma(\rho)\bigr) = \operatorname{Tr}\bigl((K_0^\dagger K_0 + K_1^\dagger K_1)\rho\bigr) = \operatorname{Tr}(\rho)$，严格保迹。检验两个极限边界：$\gamma = 0$ 时 $K_0 = I, K_1 = 0$（无衰减恒等信道）；$\gamma = 1$ 时 $K_0 = |0\rangle\langle 0|, K_1 = |0\rangle\langle 1|$（完全复位到 $|0\rangle$），两者均满足完备性。
   - **易错坑提醒**：千万不要把乘法顺序写反成 $K_1 K_1^\dagger$！算一下就会发现 $K_1 K_1^\dagger = \begin{bmatrix} \gamma & 0 \\ 0 & 0 \end{bmatrix}$，从而 $K_0 K_0^\dagger + K_1 K_1^\dagger = \operatorname{diag}(1+\gamma,\; 1-\gamma) \neq I$——这正好反映了振幅阻尼**保迹但非保单位**（TP 而非 unital）的本质。

4. **【基础】为什么只报告 $T_1$ 不能决定一台处理器能跑多深的电路**

   - **题意与约定**：$T_1$（单位：$\mu\mathrm{s}$ 或 $\mathrm{ms}$）只度量量子比特从激发态 $|1\rangle$ 弛豫到基态 $|0\rangle$ 的空闲能量衰减时间尺度；实际电路可运行深度还取决于门时长 $t_{\mathrm{gate}}$、退相位时间 $T_2 / T_\phi$ 与多种非空闲误差。
   - **核心提示**：比较能量弛豫时间 $T_1$ 与纯退相位 $T_\phi$（及 $T_2,T_2^*$）、单双比特门时长与错误率、读出/串扰误差的关系，指出决定深电路可用性的完整误差预算要素。
   - **完整分步演算**：至少有四类关键因素独立于 $T_1$ 决定实际电路深度：
     - **相干时间与门时长的比值 $T_1 / t_{\mathrm{gate}}$**：电路能执行多少层门看的是“一个相干寿命里能塞进多少个门”，而不是 $T_1$ 的绝对秒数。若硬件 A 的 $T_1 = 100\,\mu\mathrm{s}$、双比特门 $t_{\mathrm{gate}} = 50\,\mathrm{ns}$（比值 $2000$），硬件 B 的 $T_1 = 1000\,\mu\mathrm{s}$、双比特门 $t_{\mathrm{gate}} = 20\,\mu\mathrm{s}$（比值仅 $50$），B 的 $T_1$ 长十倍却可能跑更浅的电路。
     - **纯退相位 $T_\phi$ 与总相位相干 $T_2$**：两者通过

       $$
       \frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}
       \implies
       T_2 = \left(\frac{1}{2T_1} + \frac{1}{T_\phi}\right)^{-1}
       $$

       耦合。一旦存在强烈环境频率抖动使 $T_\phi \ll T_1$，量子叠加相位早在远小于 $T_1$ 的时间里就已洗白。
     - **主动操控与多比特误差**：单/双比特门的相干过旋转与校准失准、相邻比特间的串扰、跃迁到 $|2\rangle$ 等更高能级的泄漏误差，以及状态制备与读出错判（SPAM）误差，都不反映在空闲 $T_1$ 里。
     - **时间相关性与芯片布线**：低频 $1/f$ 噪声引起的慢漂移（$T_2^*$）会打破无记忆指数模型，而芯片连接稀疏带来的额外 $\mathrm{SWAP}$ 路由也会大幅拉长实际编译深度。
   - **结论与边界回验**：代入具体数值检验：$T_1 = 100\,\mu\mathrm{s}$ 但纯退相位 $T_\phi = 5\,\mu\mathrm{s}$ 时，

     $$
     T_2 = \left(\frac{1}{200} + \frac{1}{5}\right)^{-1}\mu\mathrm{s} = \frac{200}{41}\,\mu\mathrm{s} \approx 4.88\,\mu\mathrm{s},
     $$

     不到 $T_1$ 的二十分之一，且始终满足物理上限 $T_2 \le 2T_1$。
   - **易错坑提醒**：把单比特空闲 $T_1$ 曲线直接当成整机性能或门保真度指标是硬件宣传中最常见的误导；评估有效深度必须联合核查双比特门错误率、$T_2/t_{\mathrm{gate}}$、连接拓扑、泄漏与读出指标。

5. **【进阶】求 $(T \otimes \mathcal{I})(|\Phi^+\rangle\langle\Phi^+|)$ 中间 $2 \times 2$ 块的本征值并阐明完全正的必要性**

   - **题意与约定**：两比特大端序基为 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$，对最大纠缠态 $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ 的第一比特做矩阵转置 $T$、第二比特保持恒等 $\mathcal{I}$，得到 $4 \times 4$ 部分转置矩阵 $(T\otimes\mathcal{I})(|\Phi^+\rangle\langle\Phi^+|)$。
   - **核心提示**：先把 $|\Phi^+\rangle\langle\Phi^+|$ 写成 $4\times 4$ 分块矩阵，仅对第一比特（或按题设对转置侧）做块转置得到 $(T\otimes\mathcal I)(\rho)$，提取非零的 $2\times 2$ 子块求特征多项式与本征值，判断是否正半定。
   - **完整分步演算**：按第 5 章第 4.1 节把四个外积项的第一比特转置（$|0\rangle\langle 1|_A \mapsto |1\rangle\langle 0|_A$，$|1\rangle\langle 0|_A \mapsto |0\rangle\langle 1|_A$），得块对角矩阵 $\frac{1}{2}\mathrm{SWAP}$：

     $$
     (T \otimes \mathcal{I})\bigl(|\Phi^+\rangle\langle\Phi^+|\bigr)
     = \begin{bmatrix}
       1/2 & 0 & 0 & 0 \\
       0 & 0 & 1/2 & 0 \\
       0 & 1/2 & 0 & 0 \\
       0 & 0 & 0 & 1/2
       \end{bmatrix}.
     $$

     该矩阵拆成三个互不耦合的对角块：第 $1$ 行单独的 $1\times 1$ 块 $[1/2]$ 与第 $4$ 行单独的 $1\times 1$ 块 $[1/2]$ 各自直接给出本征值 $+1/2$。对中间的 $2 \times 2$ 块 $B = \begin{bmatrix} 0 & 1/2 \\ 1/2 & 0 \end{bmatrix}$ 列特征方程 $\det(B - \lambda I) = 0$：

     $$
     \det\begin{bmatrix} -\lambda & 1/2 \\ 1/2 & -\lambda \end{bmatrix}
     = (-\lambda)(-\lambda) - \left(\frac{1}{2}\right)\left(\frac{1}{2}\right)
     = \lambda^2 - \frac{1}{4}
     = 0
     \implies
     \lambda = +\frac{1}{2}\ \text{或}\ -\frac{1}{2}.
     $$

     因此中间 $2 \times 2$ 块的两个本征值为 **$+1/2$ 与 $-1/2$**，整张 $4 \times 4$ 矩阵的完整谱为 $\{1/2,\; 1/2,\; 1/2,\; -1/2\}$。
     - **为何“正”不足以定义物理信道**：单系统上的转置映射 $T(\rho) = \rho^T$ 保持特征多项式不变，能把一切单比特合法密度矩阵映成合法密度矩阵，因而是**正映射**。但真实物理系统随时可能与远方未受操作的辅助系统处于纠缠态（如 $|\Phi^+\rangle$）；如果仅作用于单比特的物理过程是 $T$，则联合态经过 $T \otimes \mathcal{I}$ 后出现了负本征值 $-1/2$，在对应本征态（单态 $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$）上会预测出荒谬的负概率：

       $$
       \langle\Psi^-|\bigl[(T \otimes \mathcal{I})(|\Phi^+\rangle\langle\Phi^+|)\bigr]|\Psi^-\rangle = -\frac{1}{2} < 0.
       $$

       因此，任何局域物理信道即使与任意维度的闲置纠缠辅助系统并用也必须保持半正定性，这就是要求**完全正**（CP）而不只要求正映射的根本原因。
   - **结论与边界回验**：四个本征值之和 $\frac{1}{2} + \frac{1}{2} + \frac{1}{2} - \frac{1}{2} = 1 = \operatorname{Tr}\bigl(\frac{1}{2}\mathrm{SWAP}\bigr)$，说明部分转置保迹却破坏正半定性。
   - **易错坑提醒**：不要误以为“$T \otimes \mathcal{I}$ 出现负本征值”意味着部分转置没有用——虽然它绝不可能是物理演化信道，但正因为可分态经部分转置必仍半正定，它反过来成为第 3 章极其好用的 PPT 纠缠判据。

6. **【计算】推导退极化参数换算 $q = 3p/4$ 并换算 $p = 0.20$**

   - **题意与约定**：本书单比特退极化信道主定义为 $\mathcal{D}_p(\rho) = (1-p)\rho + p\frac{I}{2}$（$0 \le p \le 1$）；随机 Pauli 写法为 $\widetilde{\mathcal{D}}_q(\rho) = (1-q)\rho + \frac{q}{3}(X\rho X + Y\rho Y + Z\rho Z)$（总错率 $q$ 均分给 $X, Y, Z$ 各 $q/3$）。
   - **核心提示**：利用 Pauli 泡利旋转恒等式 $\frac{1}{4}(\rho+X\rho X+Y\rho Y+Z\rho Z)=\frac{I}{2}$ 把 $\frac{I}{2}$ 展开代入 $\mathcal D_p(\rho)=(1-p)\rho+p\frac{I}{2}$，合并 $\rho$ 与三个 Pauli 项系数对照 $\widetilde{\mathcal D}_q$。
   - **完整分步演算**：第一步将任意单比特密度矩阵写成 Bloch 展开 $\rho = \frac{1}{2}(I + r_x X + r_y Y + r_z Z)$，利用 Pauli 算符与自身对易、与另外两个反对易的性质（例如 $XZX = -Z$），逐项计算三个共轭结果之和：

     $$
     \begin{aligned}
     X\rho X &= \frac{1}{2}(I + r_x X - r_y Y - r_z Z), \\
     Y\rho Y &= \frac{1}{2}(I - r_x X + r_y Y - r_z Z), \\
     Z\rho Z &= \frac{1}{2}(I - r_x X - r_y Y + r_z Z).
     \end{aligned}
     $$

     三式相加，单位阵项相加得 $\frac{3}{2}I$，每个 $r_j\sigma_j$ 均为“一正两负”相加得 $-\frac{1}{2}r_j\sigma_j$：

     $$
     X\rho X + Y\rho Y + Z\rho Z
     = \frac{1}{2}(3I - r_x X - r_y Y - r_z Z)
     = 2I - \frac{1}{2}(I + r_x X + r_y Y + r_z Z)
     = 2I - \rho.
     $$

     第二步将 $2I - \rho$ 代回 $\widetilde{\mathcal{D}}_q(\rho)$ 并整理同类项：

     $$
     \widetilde{\mathcal{D}}_q(\rho)
     = (1 - q)\rho + \frac{q}{3}(2I - \rho)
     = \left(1 - q - \frac{q}{3}\right)\rho + \frac{2q}{3}I
     = \left(1 - \frac{4q}{3}\right)\rho + \frac{4q}{3}\cdot\frac{I}{2}.
     $$

     与 $\mathcal{D}_p(\rho) = (1-p)\rho + p\frac{I}{2}$ 逐项比对系数，得到精确换算公式：

     $$
     p = \frac{4q}{3} \iff q = \frac{3p}{4}.
     $$

     第三步代入 $p = 0.20$：

     $$
     q = \frac{3 \times 0.20}{4} = 0.15,
     \qquad
     \frac{q}{3} = 0.05.
     $$

     即随机 Pauli 写法中总翻转概率 $q = 0.15$，其中 $X, Y, Z$ 各自以 $0.05$ 概率发生，不发生错误（施加 $I$）的概率为 $1 - q = 0.85$。
   - **结论与边界回验**：概率和检验 $(1 - q) + 3\cdot\frac{q}{3} = 0.85 + 0.05 + 0.05 + 0.05 = 1$；另核对最大混合极限 $p = 1$ 时 $q = 3/4$（$I, X, Y, Z$ 各占 $1/4$，恰好给出完全退极化 $I/2$）；再附单比特平均门错误率 $r = \frac{p}{2} = \frac{2}{3}q = 0.10$ 便于与模拟器口径对照。
   - **易错坑提醒**：不同文献与软件（如 Qiskit 与 Stim 的 `DEPOLARIZE1`）分别使用 $p$、$q$ 或平均门错误率 $r$ 三个相差常数因子的数字；引用“退极化率”前务必先核对定义式，绝不能直接把 $p = 0.20$ 当成 $q = 0.20$ 代入。

7. **【计算】比特翻转信道 $\mathcal{F}_{1/4}$ 对 $|0\rangle\langle 0|$ 与 $|+\rangle\langle +|$ 的输出与不动点辨析**

   - **题意与约定**：错误概率 $p = 1/4$ 的比特翻转信道定义为 $\mathcal{F}_{1/4}(\rho) = (1-p)\rho + p X\rho X = \frac{3}{4}\rho + \frac{1}{4}X\rho X$（Kraus 算符为 $K_0 = \frac{\sqrt{3}}{2}I$、$K_1 = \frac{1}{2}X$）。
   - **核心提示**：将 $\rho=|0\rangle\langle 0|$ 与 $\rho=|{+}\rangle\langle{+}|$ 分别代入 $\mathcal F_{1/4}(\rho)=\frac{3}{4}\rho+\frac{1}{4}X\rho X$；对第二问注意 $X|+\rangle=+|+\rangle$ 的本征态性质。
   - **完整分步演算**：
     - **输入一：$\rho_0 = |0\rangle\langle 0|$**。因 $X|0\rangle = |1\rangle$，共轭项为 $X|0\rangle\langle 0|X = (X|0\rangle)(\langle 0|X^\dagger) = |1\rangle\langle 1|$，代入信道得：

       $$
       \mathcal{F}_{1/4}\bigl(|0\rangle\langle 0|\bigr)
       = \frac{3}{4}|0\rangle\langle 0| + \frac{1}{4}|1\rangle\langle 1|
       = \begin{bmatrix} 3/4 & 0 \\ 0 & 1/4 \end{bmatrix}.
       $$

     - **输入二：$\rho_+ = |+\rangle\langle +|$**。因 $|+\rangle$ 是 $X$ 的 $+1$ 本征态（$X|+\rangle = |+\rangle$），共轭项为 $X|+\rangle\langle +|X = (X|+\rangle)(\langle +|X^\dagger) = |+\rangle\langle +|$，两项合并得：

       $$
       \mathcal{F}_{1/4}\bigl(|+\rangle\langle +|\bigr)
       = \frac{3}{4}|+\rangle\langle +| + \frac{1}{4}|+\rangle\langle +|
       = \left(\frac{3}{4} + \frac{1}{4}\right)|+\rangle\langle +|
       = |+\rangle\langle +|
       = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}.
       $$

     - **为何第二个输入不变不能说明信道等于恒等**：恒等信道 $\mathcal{I}$ 必须保持**所有**合法输入态都不变；只要存在哪怕一个输入态发生改变，该信道就不是恒等信道。本题第一个输入 $|0\rangle\langle 0|$ 已经退化成混态 $\operatorname{diag}(3/4, 1/4)$，本身就是明确反例。
   - **结论与边界回验**：两个输出的迹均为 $\frac{3}{4}+\frac{1}{4} = 1$ 与 $\frac{1}{2}+\frac{1}{2} = 1$；但 $\mathcal{F}_{1/4}(|0\rangle\langle 0|)$ 的纯度由 $1$ 降为 $\left(\frac{3}{4}\right)^2 + \left(\frac{1}{4}\right)^2 = \frac{10}{16} = \frac{5}{8} < 1$。从 Bloch 球几何看，比特翻转把整颗球沿 $y, z$ 方向压扁成绕 $x$ 轴对称的椭球，而 $|+\rangle$ 恰好落在保持不动的 $x$ 轴顶点 $(1,0,0)$ 上，所以它正好是该噪声的不动点。
   - **易错坑提醒**：实验标定噪声时若只拿恰好对准噪声不变轴的特殊初态去测（例如只测 $|0\rangle$ 检查纯退相位，或只测 $|+\rangle$ 检查比特翻转），会得出“零错误”的假象；必须准备跨多轴的完备探针态集合（如 $|0\rangle, |1\rangle, |+\rangle, |+i\rangle$）。

8. **【计算】从 $|+\rangle\langle +|$ 做计算基理想投影测量：条件后态与非选择后态对比**

   - **题意与约定**：初态 $\rho_+ = |+\rangle\langle +| = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$，计算基投影算符 $P_0 = |0\rangle\langle 0| = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$、$P_1 = |1\rangle\langle 1| = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$。按 Lüders 规则，结果 $m$ 的概率为 $p(m) = \operatorname{Tr}(P_m\rho_+ P_m)$，条件后态为 $\rho_{\mid m} = P_m\rho_+ P_m / p(m)$，丢弃结果的非选择后态为 $\rho' = \sum_m P_m\rho_+ P_m$。
   - **核心提示**：用计算基投影算符 $P_0=|0\rangle\langle 0|$、$P_1=|1\rangle\langle 1|$，先按 $P_0\rho_+ P_0/\operatorname{Tr}(P_0\rho_+)$ 求条件后态，再按 $P_0\rho_+ P_0+P_1\rho_+ P_1$ 求非选择后态，最后对照纯度与 $X$ 基概率。
   - **完整分步演算**：先逐格做三明治矩阵乘法算出两个未归一化分支 $P_0\rho_+ P_0$ 与 $P_1\rho_+ P_1$：

     $$
     P_0 \rho_+ P_0
     = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}
       \left(\frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}\right)
       \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}
     = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix}
       \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}
     = \begin{bmatrix} 1/2 & 0 \\ 0 & 0 \end{bmatrix}
     = \frac{1}{2}|0\rangle\langle 0|,
     $$

     $$
     P_1 \rho_+ P_1
     = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}
       \left(\frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}\right)
       \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}
     = \frac{1}{2}\begin{bmatrix} 0 & 0 \\ 1 & 1 \end{bmatrix}
       \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}
     = \begin{bmatrix} 0 & 0 \\ 0 & 1/2 \end{bmatrix}
     = \frac{1}{2}|1\rangle\langle 1|.
     $$

     - **已知结果为 `0` 的条件后态**：先求概率 $p(0) = \operatorname{Tr}(P_0\rho_+ P_0) = \frac{1}{2}$，再除以 $p(0)$ 归一化：

       $$
       \rho_{\mid 0}
       = \frac{P_0\rho_+ P_0}{p(0)}
       = \frac{\frac{1}{2}|0\rangle\langle 0|}{1/2}
       = |0\rangle\langle 0|
       = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}.
       $$

     - **丢弃测量结果时的非选择后态**：将两个未归一化分支直接相加：

       $$
       \rho'
       = P_0\rho_+ P_0 + P_1\rho_+ P_1
       = \begin{bmatrix} 1/2 & 0 \\ 0 & 0 \end{bmatrix}
         + \begin{bmatrix} 0 & 0 \\ 0 & 1/2 \end{bmatrix}
       = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
       = \frac{I}{2}.
       $$

     - **比较两者随后的计算基概率**：对条件后态 $\rho_{\mid 0} = |0\rangle\langle 0|$，再测计算基得 `(0, 1)` 的概率为 **$(1, 0)$**；对非选择后态 $\rho' = I/2$，再测计算基得 `(0, 1)` 的概率为 **$(1/2, 1/2)$**——两者**完全不同**。
   - **结论与边界回验**：$p(0) + p(1) = \frac{1}{2} + \frac{1}{2} = 1$；条件后态纯度 $\operatorname{Tr}(\rho_{\mid 0}^2) = 1$（纯态），非选择后态纯度 $\operatorname{Tr}(\rho'^2) = \frac{1}{2}$（最大混态），两者迹均为 $1$。
   - **易错坑提醒**：条件后态反映的是“已经读出并筛选出结果 `0` 那一部分子样本”的物理态，非选择后态反映的是“测量已发生但没有查看或丢弃了读数记录”的全体系综；两者描述不同的实验信息条件，绝不能混为一谈。

### 练 05-C：【计算】广义振幅阻尼（GAD）稳态布居 $p_{\mathrm{eq}}$ 与 $4\times 4$ Pauli 传递矩阵（PTM）手算

- **题意与约定**：对应[第 05 章第 5.5 节](../05-noise-channels.md#55-有限温度的广义振幅阻尼generalized-amplitude-damping)。单比特广义振幅阻尼信道 $\mathcal{E}_{\mathrm{GAD}}$ 在有限温度热浴下的稳态 $|1\rangle$ 占据专记为 $p_{\mathrm{eq}} \in [0, 1]$，弛豫概率为 $\gamma \in [0, 1]$。取 $p_{\mathrm{eq}} = 0.1$、$\gamma = 0.4$，写出 4 个标准 Kraus 算符，验证保迹性 $\sum_{k=0}^3 K_k^\dagger K_k = I$，再在规范化 Pauli 基 $\{I, X, Y, Z\}$ 下逐格算出 $4\times 4$ Pauli 传递矩阵 $R_{ij} = \frac{1}{2}\operatorname{Tr}\bigl(\sigma_i\,\mathcal{E}_{\mathrm{GAD}}(\sigma_j)\bigr)$ 与 Bloch 稳态坐标 $r_z^*$。
- **核心提示**：把 GAD 拆成权重 $(1-p_{\mathrm{eq}})$ 的“向 $|0\rangle$ 弛豫”与权重 $p_{\mathrm{eq}}$ 的“向 $|1\rangle$ 热激发”两组振幅阻尼 Kraus 算符，再分别代入 $\mathcal{E}_{\mathrm{GAD}}(I), \mathcal{E}_{\mathrm{GAD}}(X), \mathcal{E}_{\mathrm{GAD}}(Y), \mathcal{E}_{\mathrm{GAD}}(Z)$ 读出 PTM 的每一列。
- **完整分步演算**：
  - **第一步：写出四个 Kraus 算符并检验保迹性（TP）**：令 $q = 1 - p_{\mathrm{eq}} = 0.9$、$p_{\mathrm{eq}} = 0.1$、$\gamma = 0.4$（故 $1 - \gamma = 0.6,\; \sqrt{1-\gamma} = \sqrt{0.6} \approx 0.774597$）：

    $$
    K_0 = \sqrt{1-p_{\mathrm{eq}}}\begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix}, \quad
    K_1 = \sqrt{1-p_{\mathrm{eq}}}\begin{bmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{bmatrix},
    $$

    $$
    K_2 = \sqrt{p_{\mathrm{eq}}}\begin{bmatrix} \sqrt{1-\gamma} & 0 \\ 0 & 1 \end{bmatrix}, \quad
    K_3 = \sqrt{p_{\mathrm{eq}}}\begin{bmatrix} 0 & 0 \\ \sqrt{\gamma} & 0 \end{bmatrix}.
    $$

    逐项求 $K_k^\dagger K_k$ 并相加：

    $$
    \begin{aligned}
    K_0^\dagger K_0 + K_1^\dagger K_1 &= (1-p_{\mathrm{eq}})\left(\begin{bmatrix} 1 & 0 \\ 0 & 1-\gamma \end{bmatrix} + \begin{bmatrix} 0 & 0 \\ 0 & \gamma \end{bmatrix}\right) = (1-p_{\mathrm{eq}})I, \\
    K_2^\dagger K_2 + K_3^\dagger K_3 &= p_{\mathrm{eq}}\left(\begin{bmatrix} 1-\gamma & 0 \\ 0 & 1 \end{bmatrix} + \begin{bmatrix} \gamma & 0 \\ 0 & 0 \end{bmatrix}\right) = p_{\mathrm{eq}} I,
    \end{aligned}
    $$

    两式相加恰得 $\sum_{k=0}^3 K_k^\dagger K_k = (1-p_{\mathrm{eq}} + p_{\mathrm{eq}})I = I$，完全正保迹（CPTP）严格成立。
  - **第二步：逐列计算 $\mathcal{E}_{\mathrm{GAD}}(\sigma_j)$**：
    - 对 $I = \operatorname{diag}(1, 1)$：

      $$
      \mathcal{E}_{\mathrm{GAD}}(I)
      = \begin{bmatrix} (1-p_{\mathrm{eq}})(1+\gamma) + p_{\mathrm{eq}}(1-\gamma) & 0 \\ 0 & (1-p_{\mathrm{eq}})(1-\gamma) + p_{\mathrm{eq}}(1+\gamma) \end{bmatrix}
      = I + \gamma(1 - 2p_{\mathrm{eq}})Z.
      $$

      代入 $p_{\mathrm{eq}} = 0.1,\; \gamma = 0.4$，漂移项 $t_z = \gamma(1 - 2p_{\mathrm{eq}}) = 0.4 \times 0.8 = 0.32$，即 $\mathcal{E}_{\mathrm{GAD}}(I) = I + 0.32\,Z$（这说明 GAD 不是单位保真 unital 信道！）。
    - 对 $X = \begin{bmatrix}0 & 1\\ 1 & 0\end{bmatrix}$ 与 $Y = \begin{bmatrix}0 & -i\\ i & 0\end{bmatrix}$：$K_1 X K_1^\dagger = K_3 X K_3^\dagger = 0$，仅 $K_0, K_2$ 贡献非对角缩放因子 $\sqrt{1-\gamma}$，故

      $$
      \mathcal{E}_{\mathrm{GAD}}(X) = \sqrt{1-\gamma}\,X \approx 0.774597\,X, \qquad
      \mathcal{E}_{\mathrm{GAD}}(Y) = \sqrt{1-\gamma}\,Y \approx 0.774597\,Y.
      $$

    - 对 $Z = \operatorname{diag}(1, -1)$：

      $$
      \mathcal{E}_{\mathrm{GAD}}(Z)
      = \begin{bmatrix} (1-p_{\mathrm{eq}})(1-\gamma) + p_{\mathrm{eq}}(1-\gamma) & 0 \\ 0 & -(1-p_{\mathrm{eq}})(1-\gamma) - p_{\mathrm{eq}}(1-\gamma) \end{bmatrix}
      = (1-\gamma)Z = 0.6\,Z.
      $$

  - **第三步：组装 $4\times 4$ PTM 并验证不动点**：利用 $\frac{1}{2}\operatorname{Tr}(\sigma_i\sigma_j) = \delta_{ij}$，直接读出 PTM：

    $$
    R_{\mathrm{GAD}} =
    \begin{bmatrix}
    1 & 0 & 0 & 0 \\
    0 & \sqrt{1-\gamma} & 0 & 0 \\
    0 & 0 & \sqrt{1-\gamma} & 0 \\
    \gamma(1-2p_{\mathrm{eq}}) & 0 & 0 & 1-\gamma
    \end{bmatrix}
    \approx
    \begin{bmatrix}
    1 & 0 & 0 & 0 \\
    0 & 0.774597 & 0 & 0 \\
    0 & 0 & 0.774597 & 0 \\
    0.32 & 0 & 0 & 0.6
    \end{bmatrix}.
    $$

    Bloch 向量迭代为 $r'_z = 0.6\,r_z + 0.32$，令 $r'_z = r_z^*$ 解得不动点 $r_z^* = \frac{0.32}{1 - 0.6} = 0.8 = 1 - 2p_{\mathrm{eq}}$，对应稳态密度矩阵 $\rho_{\mathrm{eq}} = \frac{1}{2}(I + 0.8\,Z) = 0.9|0\rangle\langle 0| + 0.1|1\rangle\langle 1|$，其激发态布居恰好为 $p_{\mathrm{eq}} = 0.1$。
- **结论与边界回验**：零温极限 $p_{\mathrm{eq}} = 0$ 时 $t_z = \gamma$、稳态 $r_z^* = 1$（纯基态 $|0\rangle$），精确退化回标准零温振幅阻尼；高温极限 $p_{\mathrm{eq}} = 1/2$ 时 $t_z = 0$、稳态 $r_z^* = 0$（最大混态 $I/2$）。PTM 首行恒为 $(1,0,0,0)$ 印证保迹性。
- **易错坑提醒**：切勿把部分教材记作“基态平衡占据 $p$”的约定与本书“激发态 $|1\rangle$ 平衡占据 $p_{\mathrm{eq}}$”混用，否则 $t_z = \gamma(1 - 2p_{\mathrm{eq}})$ 的符号会正好颠倒！

### 练 05-D：【计算】$T_1, T_2, T_\phi$ 联合换算与 $2T_1$ 相干极限物理边界检验

- **题意与约定**：对应[第 05 章第 6.3 节](../05-noise-channels.md#63-亲手推导-1t_2--12t_1--1t_phi)。在独立马尔可夫弛豫与纯退相位模型中，横向相干时间 $T_2$、纵向能量弛豫时间 $T_1$ 与纯退相位时间 $T_\phi$ 满足速率叠加律 $\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}$（各时间单位均为 $\mu\mathrm{s}$，速率单位 $\mathrm{s}^{-1}$）。(a) 若某超导比特测得 $T_1 = 80\,\mu\mathrm{s}$、$T_2 = 60\,\mu\mathrm{s}$，求纯退相位时间 $T_\phi$ 与纯退相位率 $\Gamma_\phi = 1/T_\phi$；(b) 若另一份实验草稿报出“$T_1 = 50\,\mu\mathrm{s},\; T_2 = 120\,\mu\mathrm{s}$”，请用上述公式做物理自洽检验并指出可能原因。
- **核心提示**：先把速率关系改写为 $\frac{1}{T_\phi} = \frac{1}{T_2} - \frac{1}{2T_1}$ 求解第一问，再用非负速率条件 $\Gamma_\phi = 1/T_\phi \ge 0$ 推导出 $T_2 \le 2T_1$ 上界来审查第二问。
- **完整分步演算**：
  - **第一问（反解 $T_\phi$ 与 $\Gamma_\phi$）**：将 $T_1 = 80\,\mu\mathrm{s}$（故 $2T_1 = 160\,\mu\mathrm{s}$）与 $T_2 = 60\,\mu\mathrm{s}$ 代入速率叠加式：

    $$
    \frac{1}{T_\phi} = \frac{1}{T_2} - \frac{1}{2T_1}
    = \frac{1}{60} - \frac{1}{160}
    = \frac{8 - 3}{480}
    = \frac{5}{480}
    = \frac{1}{96}\ \mu\mathrm{s}^{-1}.
    $$

    取倒数并换算标准单位得：

    $$
    T_\phi = 96\,\mu\mathrm{s}, \qquad
    \Gamma_\phi = \frac{1}{96 \times 10^{-6}\ \mathrm{s}} \approx 1.042 \times 10^4\ \mathrm{s}^{-1}.
    $$

    回验：$\frac{1}{2\times 80} + \frac{1}{96} = \frac{3 + 5}{480} = \frac{8}{480} = \frac{1}{60}\ \mu\mathrm{s}^{-1} = \frac{1}{T_2}$，精确吻合。
  - **第二问（审查 $T_1 = 50\,\mu\mathrm{s},\; T_2 = 120\,\mu\mathrm{s}$）**：在独立马尔可夫 Lindblad 模型中，纯退相位率必须非负（$\Gamma_\phi \ge 0$），这刚性给出相干上限 $T_2 \le 2T_1$。把草稿数据代入计算：

    $$
    2T_1 = 100\,\mu\mathrm{s} < 120\,\mu\mathrm{s} = T_2
    \quad\Longrightarrow\quad
    \frac{1}{T_\phi} = \frac{1}{120} - \frac{1}{100} = -\frac{1}{600}\ \mu\mathrm{s}^{-1} < 0.
    $$

    出现负纯退相位率违背马尔可夫完全正演化假设！工程上看到 $T_2 > 2T_1$ 必须排查四类原因：① $T_1$ 与 $T_2$ 并非同一时间段测量，期间发生了 TLS 漂移（测 $T_2$ 时实际 $T_1$ 更高）；② 拟合区间过短或置信误差宽，统计涨落把点估计推过 $2T_1$；③ 读出或脉冲衰减拟合函数错把 $T_2$ 定义写成其他倍率；④ 强非马尔可夫环境或特定多能级/驱动保护场景已超出简单单比特马尔可夫模型。
- **结论与边界回验**：(a) $T_\phi = 96\,\mu\mathrm{s}$、$\Gamma_\phi \approx 1.042 \times 10^4\,\mathrm{s}^{-1}$；(b) $T_2 = 120\,\mu\mathrm{s} > 2T_1 = 100\,\mu\mathrm{s}$ 在独立马尔可夫单比特模型下非法（导出负退相位率），必须核查测量同步性、误差棒与拟合口径。
- **易错坑提醒**：能量弛豫 $T_1$ 对非对角相干的贡献因子是 $1/(2T_1)$ 而非 $1/T_1$——因此理想无纯退相位极限是 $T_2 = 2T_1$，切勿误记为 $T_2 \le T_1$！

## 第 6 章

1. **【基础】逐行推导相位回踢恒等式 $U_f|x\rangle|-\rangle = (-1)^{f(x)}|x\rangle|-\rangle$**

   - **题意与约定**：设输入寄存器为 $n$ 比特计算基态 $|x\rangle$（$x \in \{0,1\}^n$），辅助目标位处于 $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$；布尔函数 $f:\{0,1\}^n \to \{0,1\}$ 对应的标准可逆预言机定义为 $U_f|x, y\rangle = |x,\; y \oplus f(x)\rangle$（$\oplus$ 为模 $2$ 加法）。
   - **核心提示**：把 $|x\rangle|-\rangle$ 按 $|-\rangle=(|0\rangle-|1\rangle)/\sqrt{2}$ 拆成两项，应用标准预言机定义 $U_f|x,y\rangle=|x,y\oplus f(x)\rangle$，再分别讨论 $f(x)=0$ 与 $f(x)=1$ 两种情形合并为 $(-1)^{f(x)}$。
   - **完整分步演算**：先展开辅助态 $|-\rangle$，再按线性算符 $U_f$ 的分配律逐项作用：

     $$
     \begin{aligned}
     U_f|x\rangle|-\rangle
     &= U_f\left(|x\rangle \otimes \frac{|0\rangle - |1\rangle}{\sqrt{2}}\right) \\
     &= \frac{U_f|x, 0\rangle - U_f|x, 1\rangle}{\sqrt{2}} \\
     &= \frac{|x,\; 0 \oplus f(x)\rangle - |x,\; 1 \oplus f(x)\rangle}{\sqrt{2}} \\
     &= |x\rangle \otimes \frac{|f(x)\rangle - |1 \oplus f(x)\rangle}{\sqrt{2}}.
     \end{aligned}
     $$

     因为 $f(x)$ 只取 $0$ 或 $1$，分两种情形逐一核对第二寄存器：
     - 当 $f(x) = 0$ 时，$0 \oplus 0 = 0$、$1 \oplus 0 = 1$，第二寄存器为 $\frac{|0\rangle - |1\rangle}{\sqrt{2}} = (+1)|-\rangle = (-1)^0|-\rangle$；
     - 当 $f(x) = 1$ 时，$0 \oplus 1 = 1$、$1 \oplus 1 = 0$，第二寄存器为 $\frac{|1\rangle - |0\rangle}{\sqrt{2}} = -\frac{|0\rangle - |1\rangle}{\sqrt{2}} = (-1)|-\rangle = (-1)^1|-\rangle$。

     合并两种情形，并将标量因子 $(-1)^{f(x)}$ 提到整个乘积态前面：

     $$
     U_f|x\rangle|-\rangle = (-1)^{f(x)}|x\rangle|-\rangle.
     $$

   - **结论与边界回验**：对单个 $|x\rangle$，输出仍是输入寄存器与辅助位 $|-\rangle$ 的**乘积态**（无残留纠缠），模长 $|(-1)^{f(x)}|^2 = 1$ 严格保范；当输入为叠加态 $\sum_x \alpha_x |x\rangle|-\rangle$ 时，由线性性得 $\left(\sum_x \alpha_x (-1)^{f(x)}|x\rangle\right)\otimes|-\rangle$，辅助位依然完全分离，函数值已无损转化为各分支间的相对相位。
   - **易错坑提醒**：如果辅助位初态误准备成 $|+\rangle$ 而非 $|-\rangle$，由于 $|f(x)\rangle + |1 \oplus f(x)\rangle = |0\rangle + |1\rangle$ 恒不变，相位回踢就会彻底失效（无论 $f(x)$ 取 $0$ 还是 $1$ 都是 $+1$）。

2. **【基础】对比 Deutsch–Jozsa 的确定性经典基线与随机经典基线**

   - **题意与约定**：布尔函数 $f:\{0,1\}^n \to \{0,1\}$ 定义在 $N = 2^n$ 个输入上，满足承诺条件“$f$ 要么为常值函数，要么为平衡函数（恰好一半输入为 $0$、一半为 $1$）”。比较确定性零错误经典查询数、允许失败率 $\delta$ 的随机经典查询数与量子查询数。
   - **核心提示**：分别思考“要求 100% 确定不出错（最坏情形必须跨过一半输入）”与“允许极小错误率 $\delta$（独立随机抽查 $k$ 次都同值的概率按 $2^{-(k-1)}$ 衰减）”两种经典基线的查询次数差异。
   - **完整分步演算**：
     - **确定性零错误经典基线**：在最坏情况下，经典算法连续查询了 $2^{n-1}$ 个不同输入且返回值全为 $0$，此时仍无法排除“恰好把平衡函数所有为 $0$ 的一半全抽光了”的可能；直到查第 $2^{n-1} + 1$ 个不同输入，才必定 $100\%$ 确定 $f$ 是常值还是平衡。因此最坏查询次数为 **$2^{n-1} + 1$**（随 $n$ 指数增长）。
     - **随机经典基线**：随机抽取 $k$ 个输入查询；只要看到两个返回值不同就确定判“平衡”，若 $k$ 次返回值全相同就猜“常值”（常值函数永远不会猜错，唯一可能出错的是把平衡函数误判为常值）。须严格区分两种抽样方式：
       - **有放回独立抽样 $k$ 次**：平衡函数每次取 $0$ 或 $1$ 的概率均恒为 $1/2$，$k$ 次全 $0$ 概率 $(1/2)^k$、全 $1$ 概率 $(1/2)^k$，误判概率**精确等于**：

         $$
         P_{\mathrm{err}}^{\text{有放回}}(k) = \left(\frac{1}{2}\right)^k + \left(\frac{1}{2}\right)^k = 2^{1-k}.
         $$

       - **无放回抽取 $k$ 个互异输入**：误判概率为组合比（对 $k \ge 2$ 严格小于 $2^{1-k}$，且当 $k > 2^{n-1}$ 时精确为 $0$）：

         $$
         P_{\mathrm{err}}^{\text{无放回}}(k)
         = \frac{2\binom{2^{n-1}}{k}}{\binom{2^n}{k}}
         \le 2^{1-k}.
         $$

     - **量子基线**：在承诺成立的前提下，Deutsch–Jozsa 算法仅用 **$1$ 次**量子预言机查询即以概率 $1$ 精确区分。
   - **结论与边界回验**：在随机经典算法中，要使误判率 $\delta \le 10^{-3}$，只需解 $2^{1-k} \le 10^{-3} \implies k \ge 1 + \log_2(1000) \approx 10.97$，取 $k = 11$ 即可保证误判率 $\le 2^{-10} = \frac{1}{1024} \approx 0.098\%$——查询次数是与 $n$ 无关的常数 $O(\log_2(1/\delta))$。
   - **易错坑提醒**：Deutsch–Jozsa 展示的是相对**确定性零错误**经典模型的指数查询分离，绝不能笼统宣称“相对所有经典算法实现指数加速”，因为极简随机经典抽样只要常数次查询就能把错误率压到极低。

3. **【计算】用振幅均值反演法手算目标为 $|01\rangle$ 的四项 Grover 搜索**

   - **题意与约定**：两比特搜索空间维数 $N = 2^2 = 4$，唯一目标 $M = 1$ 为 $|01\rangle$。固定大端序基 $(|00\rangle, |01\rangle, |10\rangle, |11\rangle)$，记振幅四元组为 $(a_{00}, a_{01}, a_{10}, a_{11})$。一轮 Grover 迭代包含：相位标记 $S_G$（仅把目标振幅取反）与扩散反射 $D$（将每个振幅关于当前平均值 $\bar{a}$ 对称翻转，$a_x' = 2\bar{a} - a_x$）。
   - **核心提示**：固定基序 $(|00\rangle,|01\rangle,|10\rangle,|11\rangle)$，从全 $1/2$ 振幅出发：先翻转目标 $|01\rangle$ 的符号，再求四个振幅的算术平均值 $\bar a$，最后逐分量代入均值反射公式 $a'_x=2\bar a-a_x$。
   - **完整分步演算**：
     - **步骤 1（制备均匀初态）**：施加 $H^{\otimes 2}|00\rangle$，四个基态振幅均为 $1/\sqrt{4} = 1/2$：

       $$
       \vec{a}^{(0)} = \left(\frac{1}{2},\; \frac{1}{2},\; \frac{1}{2},\; \frac{1}{2}\right).
       $$

     - **步骤 2（相位标记 $S_G$）**：仅翻转目标 $|01\rangle$（第 $2$ 分量）的符号：

       $$
       \vec{a}^{(1)} = \left(\frac{1}{2},\; -\frac{1}{2},\; \frac{1}{2},\; \frac{1}{2}\right).
       $$

     - **步骤 3（计算平均振幅 $\bar{a}$）**：把四个分量相加除以 $4$：

       $$
       \bar{a}
       = \frac{\frac{1}{2} + \left(-\frac{1}{2}\right) + \frac{1}{2} + \frac{1}{2}}{4}
       = \frac{1}{4},
       \qquad
       2\bar{a} = \frac{1}{2}.
       $$

     - **步骤 4（关于均值反射 $a_x' = 2\bar{a} - a_x = \frac{1}{2} - a_x$）**：逐项代入四个分量：

       $$
       \begin{aligned}
       a_{00}' &= \frac{1}{2} - \frac{1}{2} = 0, &
       a_{01}' &= \frac{1}{2} - \left(-\frac{1}{2}\right) = 1, \\
       a_{10}' &= \frac{1}{2} - \frac{1}{2} = 0, &
       a_{11}' &= \frac{1}{2} - \frac{1}{2} = 0.
       \end{aligned}
       $$

     末态为 $\vec{a}' = (0, 1, 0, 0)$，即精确变成目标态 $|01\rangle$，单次迭代后测得 $|01\rangle$ 的概率为 $|1|^2 = 1$。
     **跨章侧重对照（第 6 章原语直觉视角）**：本题用四项算例建立“相位标记 + 关于均值反射”的单轮几何画面；若需追踪第 $2$ 轮过度旋转（over-rotation）的逐振幅递推与成功率暴跌，见[第 7 章第 12 题](#第-7-章)。
   - **结论与边界回验**：每步态矢量均归一化——初始 $4\times(1/4)=1$，标记后 $4\times(1/4)=1$，扩散后 $0^2 + 1^2 + 0^2 + 0^2 = 1$。几何回验：初始夹角满足 $\sin\theta = \sqrt{M/N} = \sqrt{1/4} = 1/2 \implies \theta = \pi/6$，一轮旋转 $2\theta$ 后总角为 $3\theta = \pi/2$，故成功率 $\sin^2(\pi/2) = 1$。
   - **易错坑提醒**：$N = 4, M = 1$ 一轮必中是 $3\theta = \pi/2$ 的罕见巧合，绝不代表一般规模的 Grover 搜索一次就成功；而且如果在这一例上多跑一轮（$k = 2$），角度转到 $5\theta = 5\pi/6$，成功率反而会因过旋转跌回 $\sin^2(5\pi/6) = 1/4$。

4. **【计算】展开 $\operatorname{QFT}_4|2\rangle$ 并用左反线性内积检验与 $\operatorname{QFT}_4|1\rangle$ 正交**

   - **题意与约定**：四维（$Q = 2^2 = 4$）量子傅里叶变换定义为 $\operatorname{QFT}_4|x\rangle = \frac{1}{\sqrt{4}}\sum_{y=0}^3 e^{2\pi i xy / 4}|y\rangle$（$x \in \{0, 1, 2, 3\}$），计算基按大端序排为 $|0\rangle, |1\rangle, |2\rangle, |3\rangle$。检验正交采用本书统一的**左反线性**内积 $\langle u|v\rangle = \sum_{y=0}^3 u_y^* v_y$。
   - **核心提示**：把 $x=2$ 与 $x=1$ 分别代入 $Q=4$ 的量子傅里叶变换公式 $\operatorname{QFT}_4|x\rangle=\frac{1}{2}\sum_{y=0}^3 e^{2\pi i xy/4}|y\rangle$（注意 $e^{i\pi/2}=i$），再用左反线性内积逐项相加验证正交。
   - **完整分步演算**：第一步将 $x = 2$ 代入定义式，化简指数 $e^{2\pi i (2y)/4} = e^{i\pi y} = (-1)^y$ 并逐项列出 $y = 0, 1, 2, 3$：

     $$
     \begin{aligned}
     \operatorname{QFT}_4|2\rangle
     &= \frac{1}{2}\sum_{y=0}^3 e^{2\pi i (2y)/4}|y\rangle
      = \frac{1}{2}\sum_{y=0}^3 e^{i\pi y}|y\rangle \\
     &= \frac{1}{2}\Bigl(e^{0}|0\rangle + e^{i\pi}|1\rangle + e^{2i\pi}|2\rangle + e^{3i\pi}|3\rangle\Bigr) \\
     &= \frac{|0\rangle - |1\rangle + |2\rangle - |3\rangle}{2}
      = \frac{1}{2}\begin{bmatrix} 1 \\ -1 \\ 1 \\ -1 \end{bmatrix}.
     \end{aligned}
     $$

     第二步将 $x = 1$ 代入定义式，化简指数 $e^{2\pi i (1\cdot y)/4} = e^{i\pi y/2} = i^y$ 并逐项写出 $\operatorname{QFT}_4|1\rangle$：

     $$
     \begin{aligned}
     \operatorname{QFT}_4|1\rangle
     &= \frac{1}{2}\sum_{y=0}^3 i^y |y\rangle
      = \frac{1}{2}\Bigl(1\cdot|0\rangle + i|1\rangle + i^2|2\rangle + i^3|3\rangle\Bigr) \\
     &= \frac{|0\rangle + i|1\rangle - |2\rangle - i|3\rangle}{2}
      = \frac{1}{2}\begin{bmatrix} 1 \\ i \\ -1 \\ -i \end{bmatrix}.
     \end{aligned}
     $$

     第三步显式执行左反线性内积。先以 $\operatorname{QFT}_4|1\rangle$ 作左矢（必须把各复振幅取共轭：$+i \mapsto -i$、$-i \mapsto +i$），得到 $\langle\operatorname{QFT}_4(1)| = \frac{1}{2}\begin{bmatrix} 1 & -i & -1 & +i \end{bmatrix}$，再行乘列逐项展开：

     $$
     \begin{aligned}
     \langle\operatorname{QFT}_4(1)\mid\operatorname{QFT}_4(2)\rangle
     &= \left(\frac{1}{2}\begin{bmatrix} 1 & -i & -1 & i \end{bmatrix}\right)
        \left(\frac{1}{2}\begin{bmatrix} 1 \\ -1 \\ 1 \\ -1 \end{bmatrix}\right) \\
     &= \frac{1}{4}\bigl(1\cdot 1 + (-i)(-1) + (-1)\cdot 1 + i(-1)\bigr) \\
     &= \frac{1}{4}(1 + i - 1 - i)
      = 0.
     \end{aligned}
     $$

     若反过来以实向量 $\operatorname{QFT}_4|2\rangle$ 作左矢，则按复指数求和等价写出：

     $$
     \langle\operatorname{QFT}_4(2)\mid\operatorname{QFT}_4(1)\rangle
     = \frac{1}{4}\sum_{y=0}^3 \bigl(e^{2\pi i(2y)/4}\bigr)^* e^{2\pi i(1\cdot y)/4}
     = \frac{1}{4}\sum_{y=0}^3 e^{2\pi i(1-2)y/4}
     = \frac{1}{4}(1 - i - 1 + i)
     = 0.
     $$

     两者内积严格为 $0$，确认输出彼此正交。
   - **结论与边界回验**：两输出态的范数平方分别为 $\frac{|1|^2 + |-1|^2 + |1|^2 + |-1|^2}{4} = 1$ 与 $\frac{|1|^2 + |i|^2 + |-1|^2 + |-i|^2}{4} = 1$，既保长又保正交，与 $\operatorname{QFT}_4$ 的酉性完全一致。
   - **易错坑提醒**：算复向量内积时切忌忘记给左侧左矢取共轭——若直接拿 $[1, i, -1, -i]$（未共轭）与 $[1, -1, 1, -1]^T$ 相乘，虽然本例巧合消掉，但在计算 $\langle\operatorname{QFT}_4(1)|\operatorname{QFT}_4(1)\rangle$ 时就会错算出 $\frac{1 - 1 + 1 - 1}{4} = 0$，把单位向量长度算成零。

5. **【基础】为什么高效 QFT 电路不等于能高效输出完整经典傅里叶数组**

   - **题意与约定**：对 $n$ 个量子比特（数组长度 $N = 2^n$），标准 QFT 电路门数为 $O(n^2) = O(\log_2^2 N)$（近似 QFT 可进一步降至 $O(n\log_2(n/\epsilon))$），而经典快速傅里叶变换（FFT）耗时为 $O(N\log_2 N) = O(n 2^n)$。
   - **核心提示**：区分“在量子态振幅中以 $O(n^2)$ 门准备好傅里叶系数”与“测量只能采样输出单个索引而非吐出全部 $2^n$ 个复数”；想读出完整经典数组仍受输出维度下界约束。
   - **完整分步演算**：把 QFT 直接当成经典 FFT 替代品会在输入和输出两端同时撞上指数墙：
     - **输出读出墙（$\Omega(2^n)$）**：QFT 把频谱系数编码进了 $n$ 比特量子态的 $2^n$ 个复振幅里，但单次计算基测量只能按模平方概率返回**一个** $n$ 位样本，根本不会吐出全部 $2^n$ 个复数。如果任务要求把全部 $N = 2^n$ 个频谱系数打印成经典数组，单是写出输出与逐项估计振幅的测量次数就至少需要 $\Omega(2^n)$，指数优势瞬间消失。
     - **输入装载墙（$\Omega(2^n)$）**：要对一段任意给定的长度为 $N = 2^n$ 的经典音频或图像数组做变换，先得把全部 $2^n$ 个经典数据装进量子态振幅中；对无特殊解析结构的任意数组，状态制备电路本身通常就需要 $\Omega(2^n)$ 个门。
   - **结论与边界回验**：以 $n = 20$（$N \approx 10^6$ 采样点）为例，QFT 核心线路虽仅约几百个门，但把全部百万个复频谱读出来仍至少需要百万量级以上的测量与经典存储开销。QFT 真正发挥威力的场景，是作为内部量子子程序（如 QPE、Shor 周期寻找），把周期信息集中到少数高概率主峰后，只靠少量采样就能读出全局周期。
   - **易错坑提醒**：千万不要只盯着中间一段电路的 $O(n^2)$ 门数就宣称“量子傅里叶变换把经典 FFT 指数加速了”；比较端到端任务必须核对输入是经典数组还是已有量子态，输出是完整系数表还是单一频峰样本。

6. **【基础】为什么相位估计（QPE）中受控 $U^{2^j}$ 的实现成本必须单独说明**

   - **题意与约定**：标准相位估计使用 $t$ 个控制比特，对应相位寄存器网格总数 $Q = 2^t$（精度约 $1/Q = 2^{-t}$），依次对系统寄存器施加受控幂 $\text{c-}U^{2^0}, \text{c-}U^{2^1}, \dots, \text{c-}U^{2^{t-1}}$。
   - **核心提示**：注意相位估计要依次施加 $U^{2^0},U^{2^1},\dots,U^{2^{t-1}}$：若只能把单次 $U$ 串联重复 $2^j$ 次，总门数将随控制位数 $t$ 指数爆炸，除非 $U$ 存在快速模幂或结构化快进方法。
   - **完整分步演算**：首先核算如果只能把受控门 $\text{c-}U$ 当作无内部结构的黑箱按顺序重复调用，完成整套受控幂总共需要调用 $\text{c-}U$ 的次数：

     $$
     N_{\mathrm{call}}
     = \sum_{j=0}^{t-1} 2^j
     = 1 + 2 + 4 + \cdots + 2^{t-1}
     = 2^t - 1
     = Q - 1.
     $$

     按等比数列求和，顺序调用次数与目标精度倒数 $Q = 2^t$ 呈线性（关于控制位数 $t$ 呈**指数级**）增长！更进一步，访问模型决定着成本量级的根本分水岭：
     - **纯黑箱模型**：仅给出无控黑箱 $U$ 时，一般甚至不能免费构造出受控版本 $\text{c-}U$（第 4 章已指出受控操作对全局相位敏感）；即便允许调用 $\text{c-}U$，无快进结构时也必须付出 $2^t - 1$ 次顺序调用（例如每多要 $1$ 位二进制精度，门数翻倍）。
     - **有特殊代数结构模型**：在 Shor 算法中，$U_a|y\rangle = |ay \bmod N\rangle$ 的高次幂满足 $U_a^{2^j}|y\rangle = |(a^{2^j}\bmod N)\,y \bmod N\rangle$，系数 $a^{2^j}\bmod N$ 可在经典计算机上用重复平方高效预计算，因此每个受控 $U_a^{2^j}$ 与单次模乘门数同阶，总成本才降为关于 $t$ 的多项式级（在部分可快进哈密顿量中也同理）。
   - **结论与边界回验**：代入 $t = 10$（$Q = 1024$）检验：虽然线路图上只画了 $10$ 个受控方块，但若按顺序黑箱展开，需要调用 $2^{10} - 1 = 1023$ 次 $\text{c-}U$；当 $t = 20$ 时，顺序调用数暴涨至 $1{,}048{,}575$ 次。
   - **易错坑提醒**：不要被 QPE 电路图里那 $t$ 个大小相同的方框欺骗而以为受控幂只花 $O(t)$ 的门数；报告任何 QPE 算法复杂度时，必须明确写清 $U^{2^j}$ 是按黑箱顺序重复，还是借助问题结构实现了快进电路。

7. **【进阶】把 Deutsch 问题的接受概率写成多项式并核对一次查询次数界**

   - **题意与约定**：一比特布尔函数 $f:\{0,1\} \to \{0,1\}$ 由两个布尔变量 $z_0 = f(0) \in \{0,1\}$ 与 $z_1 = f(1) \in \{0,1\}$ 完全决定。Deutsch 判定任务要求：当 $f$ 为平衡（$z_0 \neq z_1$）时输出接受（概率 $1$），当 $f$ 为常值（$z_0 = z_1$）时输出拒绝（概率 $0$）。多项式方法定理指出：$T$ 次量子查询后，任意基态振幅关于 $(z_0, z_1)$ 的多项式次数至多为 $T$，取模平方后接受概率多项式次数至多为 $2T$。
   - **核心提示**：对布尔变量 $z_0,z_1\in\{0,1\}$，把函数值判定（平衡时输出 $1$、常值时输出 $0$）写成多线性实多项式 $P(z_0,z_1)$ 并检查总次数，再对照多项式法“$T$ 次查询振幅至多 $T$ 次、概率取模平方至多 $2T$ 次”的界。
   - **完整分步演算**：在布尔取值 $z_0, z_1 \in \{0,1\}$ 上，衡量“二者不同”的异或函数 $z_0 \oplus z_1$ 恰可写成如下二次多线性多项式：

     $$
     P(z_0, z_1) = z_0 \oplus z_1 = z_0 + z_1 - 2z_0 z_1.
     $$

     在全部四个布尔输入 $(z_0, z_1) \in \{0,1\}^2$ 上逐项代入核验：

     $$
     \begin{aligned}
     P(0, 0) &= 0 + 0 - 2(0)(0) = 0 \quad (\text{常值，拒绝}), \\
     P(0, 1) &= 0 + 1 - 2(0)(1) = 1 \quad (\text{平衡，接受}), \\
     P(1, 0) &= 1 + 0 - 2(1)(0) = 1 \quad (\text{平衡，接受}), \\
     P(1, 1) &= 1 + 1 - 2(1)(1) = 0 \quad (\text{常值，拒绝}).
     \end{aligned}
     $$

     该多项式的最高次项为 $-2z_0 z_1$，总次数为 $\deg(P) = 2$。对一次量子查询（$T = 1$），多项式方法给出的接受概率次数上界为 $2T = 2 \times 1 = 2$。由于 $\deg(P) = 2 \le 2T$，Deutsch 算法用一次查询精确实现该接受概率与次数上界完全相容、毫不违背。
   - **结论与边界回验**：对比 Deutsch 线路一次查询后的输出态振幅：结果 `1` 的振幅为 $\frac{(-1)^{z_0} - (-1)^{z_1}}{2} = \frac{(1 - 2z_0) - (1 - 2z_1)}{2} = z_1 - z_0$（次数恰为 $1 \le T$），取模平方并利用布尔幂等律 $z_j^2 = z_j$ 得 $(z_1 - z_0)^2 = z_0^2 + z_1^2 - 2z_0 z_1 = z_0 + z_1 - 2z_0 z_1$，精确吻合！
   - **易错坑提醒**：$\deg(P) \le 2T$ 只是存在 $T$ 次精确量子查询算法的**必要条件**，而不是充分条件——不能反过来认为随便写一个次数为 $2$ 的布尔多项式就一定能用一次量子查询算出来。

8. **【基础】混合法查询下界为何不能直接推出任意数据库系统的墙钟时间下界**

   - **题意与约定**：Bennett–Bernstein–Brassard–Vazirani（1997）的混合法下界针对的是“无结构黑箱预言机查询模型”，以单次预言机调用为单位步数，在规模 $N$ 中证明无结构量子搜索至少需要 $\Omega(\sqrt{N})$ 次查询。
   - **核心提示**：回看混合法证明所依赖的前提：算法只能把函数当作无结构黑箱逐次查询；现实数据库往往具备排序索引、哈希表、树结构或可并行硬件访问，打破了黑箱无结构假设。
   - **完整分步演算**：把混合法下界的推导逻辑与现实数据库系统的真实瓶颈逐项对照：
     - **混合法锁定的前提**：混合法通过逐时刻对比“空预言机运行轨迹”与“标记某目标 $x^*$ 的预言机运行轨迹”，利用总振幅偏移不超过 $2\sum_{t=1}^T |\alpha_{x^*}^{(t)}|$ 及 Cauchy–Schwarz 不等式，证得要把成功概率抬到常数必须满足

       $$
       T = \Omega(\sqrt{N}).
       $$

       这一证明严格假定了访问接口只能按无结构黑箱逐点查询 $f(x)$，且把一次查询记作单位 $1$。
     - **现实数据库系统改变了结构与成本模型**：现实数据库通常拥有 B+ 树索引、哈希表、排序键、缓存局部性、列式压缩、多核/SIMD 并行读取，同时还伴随着磁盘/网络 I/O 延迟、数据装载与谓词计算等开销。一旦改变访问模型或利用数据结构（例如有序数组二分查找只需 $O(\log_2 N)$ 次经典比较，哈希索引期望 $O(1)$ 次），原本针对“无结构黑箱”的 $\Omega(\sqrt{N})$ 下界便不再适用；反之，若数据库确实毫无索引，也必须把经典数据装载进量子态或硬件 QRAM 的真实墙钟开销一并计入。
   - **结论与边界回验**：对 $N = 10^9$ 条已建 B+ 树索引的记录，经典检索只需约 $\log_2(10^9) \approx 30$ 次树节点比较，远远少于无结构量子下界 $\sqrt{10^9} \approx 3.16 \times 10^4$ 次——这并未推翻混合法下界，而是因为索引提供了黑箱模型禁止使用的结构信息。
   - **易错坑提醒**：查询下界证明的是“在**固定黑箱接口**下的抽象调用次数底线”，既不能把它误用成所有现实数据库系统的墙钟下界，也不能反过来把无结构 Grover 加速宣传成能取代带索引的经典关系型数据库。

9. **【基础】列出 $f(0) = 0, f(1) = 1$ 时 $U_f$ 对四基态的作用并证明可逆性**

   - **题意与约定**：输入与目标各 $1$ 比特，按大端序两比特计算基 $(|0,0\rangle, |0,1\rangle, |1,0\rangle, |1,1\rangle)$，标准可逆预言机定义为 $U_f|x, y\rangle = |x,\; y \oplus f(x)\rangle$（$\oplus$ 为模 $2$ 加法），给定 $f(0) = 0$、$f(1) = 1$。
   - **核心提示**：按 $U_f|x,y\rangle=|x,y\oplus f(x)\rangle$ 逐一计算四个计算基态的输出像，写出 $4\times 4$ 置换矩阵并验证 $U_f^\dagger U_f=I$（或 $U_f^2=I$）。
   - **完整分步演算**：将四个基态的 $(x, y)$ 逐一代入 $U_f|x, y\rangle = |x,\; y \oplus f(x)\rangle$：

     $$
     \begin{aligned}
     U_f|0, 0\rangle &= |0,\; 0 \oplus f(0)\rangle = |0,\; 0 \oplus 0\rangle = |0, 0\rangle, \\
     U_f|0, 1\rangle &= |0,\; 1 \oplus f(0)\rangle = |0,\; 1 \oplus 0\rangle = |0, 1\rangle, \\
     U_f|1, 0\rangle &= |1,\; 0 \oplus f(1)\rangle = |1,\; 0 \oplus 1\rangle = |1, 1\rangle, \\
     U_f|1, 1\rangle &= |1,\; 1 \oplus f(1)\rangle = |1,\; 1 \oplus 1\rangle = |1, 0\rangle.
     \end{aligned}
     $$

     把这四列排成 $4 \times 4$ 矩阵，它恰好就是第一位控制、第二位目标的 $\mathrm{CNOT}_{1\to 2}$ 门：

     $$
     U_f = \begin{bmatrix}
       1 & 0 & 0 & 0 \\
       0 & 1 & 0 & 0 \\
       0 & 0 & 0 & 1 \\
       0 & 0 & 1 & 0
     \end{bmatrix}.
     $$

     **为何可逆**：对任意基态 $|x, y\rangle$ 连续作用两次 $U_f$，利用模 $2$ 加法的自逆性 $f(x) \oplus f(x) = 0$：

     $$
     U_f^2|x, y\rangle
     = U_f|x,\; y \oplus f(x)\rangle
     = |x,\; (y \oplus f(x)) \oplus f(x)\rangle
     = |x,\; y \oplus 0\rangle
     = |x, y\rangle.
     $$

     因此 $U_f$ 不仅是一一对应的双射（四个不同正交基态映到四个互异正交基态，绝不合并），而且满足 $U_f^{-1} = U_f^\dagger = U_f$，是严格的酉算符。
   - **结论与边界回验**：检查矩阵乘积 $U_f^\dagger U_f = U_f^2 = I_4$；若换成常值函数 $f(0) = f(1) = 0$，则 $U_f = I_4$；若换成 $f(0) = f(1) = 1$，则 $U_f = I \otimes X$，无论 $f$ 本身是否可逆（例如多对一常值函数），扩成 $|x, y\oplus f(x)\rangle$ 之后永远可逆。
   - **易错坑提醒**：不要把“函数 $f(x)$ 本身是否可逆”与“量子预言机 $U_f$ 是否可逆”混为一谈——$U_f$ 通过保留原输入 $x$ 并把函数值异或到额外目标寄存器 $y$ 上，使任何布尔函数都能合法嵌入可逆酉电路。

10. **【计算】两控制位相位估计手算：$U = \operatorname{diag}(1, i)$ 与本征态 $|1\rangle$**

    - **题意与约定**：目标酉算符 $U = \begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix}$，输入本征态 $|u\rangle = |1\rangle$；控制寄存器使用 $t = 2$ 个量子比特，相位网格总数 $Q = 2^2 = 4$。按大端序将控制寄存器记作 $|k_1 k_0\rangle$（对应整数 $k = 2k_1 + k_0 \in \{0, 1, 2, 3\}$），低位 $k_0$ 控制 $U^{2^0} = U$，高位 $k_1$ 控制 $U^{2^1} = U^2 = \operatorname{diag}(1, -1)$。
    - **核心提示**：先算出本征值 $i=e^{2\pi i\phi}$ 对应的精确相位 $\phi$，再经 $H^{\otimes 2}$ 与受控 $U^{2^0},U^{2^1}$ 相位回踢写出控制寄存器四个基态的相位因子，与 $\operatorname{QFT}_4|y\rangle$ 比对即可读出逆 QFT 输出。
    - **完整分步演算**：先核对本征值与真相位：

      $$
      U|1\rangle = i|1\rangle = e^{i\pi/2}|1\rangle = e^{2\pi i (1/4)}|1\rangle,
      \qquad
      \phi = \frac{1}{4}.
      $$

      - **第 1 拍（控制位施加 $H^{\otimes 2}$）**：从 $|00\rangle|1\rangle$ 演化为四条等振幅分支的均匀叠加：

        $$
        \bigl(H^{\otimes 2} \otimes I\bigr)|00\rangle|1\rangle
        = \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}\otimes|1\rangle
        = \frac{1}{2}\sum_{k=0}^3 |k\rangle|1\rangle.
        $$

      - **第 2 拍（依次施加受控 $U$ 与受控 $U^2$）**：对每一分支 $|k_1 k_0\rangle|1\rangle$，合起来施加 $U^{2k_1 + k_0} = U^k$，由相位回踢给对应分支乘上 $i^k$：
        - $k = 0$（$|00\rangle$）：$i^0 = 1$；
        - $k = 1$（$|01\rangle$）：$i^1 = i$；
        - $k = 2$（$|10\rangle$）：$i^2 = -1$；
        - $k = 3$（$|11\rangle$）：$i^3 = -i$。

        此时系统态仍保持分离在 $|1\rangle$，控制寄存器状态为：

        $$
        |\psi_{\mathrm{ctrl}}\rangle
        = \frac{|00\rangle + i|01\rangle - |10\rangle - i|11\rangle}{2}
        = \frac{1}{2}\sum_{k=0}^3 e^{2\pi i \cdot 1 \cdot k / 4}|k\rangle
        = \operatorname{QFT}_4|1\rangle.
        $$

      - **第 3 拍（对控制寄存器施加逆变换 $\operatorname{QFT}_4^{-1}$）**：利用 $\operatorname{QFT}_4^{-1}\operatorname{QFT}_4 = I_4$，一步精确还原整数 $y = 1$：

        $$
        \operatorname{QFT}_4^{-1}|\psi_{\mathrm{ctrl}}\rangle
        = \operatorname{QFT}_4^{-1}\bigl(\operatorname{QFT}_4|1\rangle\bigr)
        = |1\rangle
        = |01\rangle.
        $$

      测量控制寄存器必得两位二进制串 **`01`**（概率为 $1$），对应估计相位 $\hat{\phi} = \frac{y}{Q} = \frac{1}{4}$。
    - **结论与边界回验**：四条分支模平方之和为 $\frac{|1|^2 + |i|^2 + |-1|^2 + |-i|^2}{4} = 1$；也可用第 4 题已算过的 $\operatorname{QFT}_4|1\rangle$ 表达式直接比对，四项系数完全重合。因为 $\phi = 1/4$ 恰好落在 $Q = 4$ 网格点上，命中概率为精确 $100\%$。
    - **易错坑提醒**：接线顺序必须与大端序对齐——高位 $k_1$ 对应权重 $2^1$ 控 $U^2$、低位 $k_0$ 对应权重 $2^0$ 控 $U$；若把两根控制线接反，电路会算出倒序位串 `10`（误报 $\phi = 1/2$）。

11. **【进阶】由初态电路 $A$ 构造一般振幅放大的反射算符 $D$ 与资源账本**

    - **题意与约定**：设一般制备电路 $A$ 从全零态 $|0^n\rangle$ 制备初态 $|\psi_0\rangle = A|0^n\rangle$（$A$ 为 $n$ 比特酉算符，$A^\dagger A = AA^\dagger = I$）。记关于全零态的反射算符为 $S_0 = 2|0^n\rangle\langle 0^n| - I$。
    - **核心提示**：把关于均匀态 $|s\rangle$ 的反射 $2|s\rangle\langle s|-I$ 推广到任意初态 $|\psi_0\rangle=A|0^n\rangle$，利用共轭恒等式 $A(2|0^n\rangle\langle 0^n|-I)A^\dagger$；清点单轮开销时别忘把 $A$ 与 $A^\dagger$ 一并算入。
    - **完整分步演算**：构造算符 $D = A S_0 A^\dagger$，代入 $S_0$ 按矩阵分配律展开验证它正是关于初态 $|\psi_0\rangle$ 的反射：

      $$
      \begin{aligned}
      D
      &= A S_0 A^\dagger
       = A\bigl(2|0^n\rangle\langle 0^n| - I\bigr)A^\dagger \\
      &= 2\bigl(A|0^n\rangle\bigr)\bigl(\langle 0^n|A^\dagger\bigr) - A I A^\dagger \\
      &= 2|\psi_0\rangle\langle\psi_0| - I.
      \end{aligned}
      $$

      核验 $D$ 的反射几何效果：
      - 作用于 $|\psi_0\rangle$：$D|\psi_0\rangle = 2|\psi_0\rangle\underbrace{\langle\psi_0|\psi_0\rangle}_{1} - |\psi_0\rangle = +|\psi_0\rangle$（沿初态方向保持不变）；
      - 作用于任意与 $|\psi_0\rangle$ 正交的态 $|\psi_\perp\rangle$（$\langle\psi_0|\psi_\perp\rangle = 0$）：$D|\psi_\perp\rangle = 2|\psi_0\rangle\cdot 0 - |\psi_\perp\rangle = -|\psi_\perp\rangle$（垂直分量精确反号）。

      对应到量子电路图（从左到右执行、矩阵从右到左相乘），实现 $D$ 的三段操作依次为：**逆运行 $A^\dagger$ $\longrightarrow$ 全零态反射 $S_0$ $\longrightarrow$ 正运行 $A$**。
      - **为何只数“标记查询”会低估实际线路成本**：一轮完整的振幅放大迭代 $\mathcal{Q} = D S_G = A S_0 A^\dagger S_G$，除了 $1$ 次标记好态的预言机 $S_G$ 外，**每一轮**都必须额外付出 $1$ 次 $A^\dagger$、$1$ 次 $A$ 以及 $1$ 次 $n$ 比特多控反射 $S_0 = -X^{\otimes n}(\mathrm{C}^{n-1}Z)X^{\otimes n}$（用干净辅助位分解仍需 $2(n-2)$ 个 Toffoli 门）。若初态制备 $A$ 本身是一段深层状态装载或概率分布制备电路，总门数和电路深度往往由 $A, A^\dagger$ 与多控门主导，仅统计 $S_G$ 调用次数会严重低估真实成本。
    - **结论与边界回验**：检验特例 $A = H^{\otimes n}$（标准 Grover）：因 $H^\dagger = H$，立刻还原为熟悉的 $D = H^{\otimes n}(2|0^n\rangle\langle 0^n| - I)H^{\otimes n} = 2|s\rangle\langle s| - I$，且 $D^\dagger D = (2|\psi_0\rangle\langle\psi_0|-I)^2 = 4|\psi_0\rangle\langle\psi_0| - 4|\psi_0\rangle\langle\psi_0| + I = I$（酉且自逆）。
    - **易错坑提醒**：不要把电路执行次序写反成先 $A$ 后 $A^\dagger$——矩阵乘积 $A S_0 A^\dagger$ 中最靠右的是 $A^\dagger$，所以电路里必须先用 $A^\dagger$ 把 $|\psi_0\rangle$ 退回 $|0^n\rangle$，做完 $S_0$ 反射后再用 $A$ 推回 $|\psi_0\rangle$。

12. **【计算】无耦合两比特精确演化与同比特 $H = X + Z$ 的不对易检验**

    - **题意与约定**：取自然单位 $\hbar = 1$。第一问为两比特哈密顿量 $H = Z_A \otimes I_B + I_A \otimes X_B$，初态 $|00\rangle = |0\rangle_A \otimes |0\rangle_B$，演化算符 $U(t) = e^{-iHt}$；第二问为单比特哈密顿量 $H_1 = X + Z$。
    - **核心提示**：第一问利用 $[Z_A\otimes I_B,I_A\otimes X_B]=0$ 把联合演化因子分解为两比特独立演化，单独算 $e^{-itX_B}|0\rangle_B$；第二问计算 $[X,Z]$ 检验同比特两项是否对易，判断能否拆成单因子乘积。
    - **完整分步演算**：
      - **第一问（精确演化与 $B = 1$ 概率）**：先检验两项的对易子（用混合乘积律）：

        $$
        (Z_A \otimes I_B)(I_A \otimes X_B) = Z_A \otimes X_B,
        \qquad
        (I_A \otimes X_B)(Z_A \otimes I_B) = Z_A \otimes X_B,
        $$

        故 $[Z_A \otimes I_B,\; I_A \otimes X_B] = 0$，两项严格对易！因此矩阵指数可以**精确拆分**为两个单比特演化的张量积：

        $$
        e^{-i(Z_A \otimes I_B + I_A \otimes X_B)t}
        = e^{-i Z_A t} \otimes e^{-i X_B t}.
        $$

        分别计算两比特各自的演化（利用 $Z|0\rangle = +|0\rangle$ 与 $X^2 = I \implies e^{-iXt} = \cos t\,I - i\sin t\,X$）：

        $$
        e^{-i Z_A t}|0\rangle_A = e^{-it}|0\rangle_A,
        $$

        $$
        e^{-i X_B t}|0\rangle_B
        = (\cos t\,I - i\sin t\,X)|0\rangle_B
        = \cos t|0\rangle_B - i\sin t|1\rangle_B.
        $$

        相乘得到时刻 $t$ 的精确两比特联合态：

        $$
        |\psi(t)\rangle
        = e^{-it}|0\rangle_A \otimes \bigl(\cos t|0\rangle_B - i\sin t|1\rangle_B\bigr)
        = e^{-it}\cos t|00\rangle - i e^{-it}\sin t|01\rangle.
        $$

        测得 $B = 1$ 的唯一非零分支是 $|01\rangle$，对其复振幅取模平方得：

        $$
        p(B = 1)
        = \bigl|-i e^{-it}\sin t\bigr|^2
        = |-i|^2 \cdot |e^{-it}|^2 \cdot \sin^2 t
        = 1 \cdot 1 \cdot \sin^2 t
        = \sin^2 t.
        $$

      - **第二问（同比特 $H_1 = X + Z$ 能否直接拆成两指数之积）**：**不能**当作精确等式！因为 $X$ 与 $Z$ 作用在同一个比特上且彼此**反对易而不对易**：

        $$
        [X, Z] = XZ - ZX
        = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} - \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}
        = \begin{bmatrix} 0 & -2 \\ 2 & 0 \end{bmatrix}
        = -2iY \neq 0.
        $$

        在基态 $|0\rangle$ 上一眼可验：$XZ|0\rangle = X|0\rangle = |1\rangle$，而 $ZX|0\rangle = Z|1\rangle = -|1\rangle \neq |1\rangle$。由 Baker–Campbell–Hausdorff 公式，单次乘积 $e^{-iZt}e^{-iXt}$ 只是精确演化 $e^{-i(X+Z)t}$ 的一阶 Trotter 近似（存在 $O(t^2)$ 误差），必须切分成 $r$ 小步 $\bigl(e^{-iZt/r}e^{-iXt/r}\bigr)^r$ 才能随 $r$ 增大逼近精确演化。
    - **结论与边界回验**：第一问总概率 $p(B=0) + p(B=1) = \cos^2 t + \sin^2 t = 1$；检验特殊时刻：$t = 0$ 时 $\sin^2 0 = 0$（停在 $|00\rangle$），$t = \pi/2$ 时 $\sin^2(\pi/2) = 1$（$X$ 翻转整 $\pi$ 角把 $B$ 精确翻成 $|1\rangle$）。第二问在 $t = \pi/2$ 时，单步乘积给出 $p_{\mathrm{Trotter}}(1) = 1$，而精确演化给出 $p_{\mathrm{exact}}(1) = \frac{1}{2}\sin^2(\frac{\pi}{\sqrt{2}}) \approx 0.3166 \neq 1$，偏差极其显著。
    - **易错坑提醒**：指数拆乘定律 $e^{A+B} = e^A e^B$ 仅在 $[A, B] = 0$ 时精确成立；动手拆哈密顿量之前，务必先检查各项是否作用在不同比特上或彼此对易。

13. **【计算】三次独立运行多数表决的正确率与系统偏差失效分析**

    - **题意与约定**：二选一判定任务中，单次独立运行判断正确的概率为 $p = 2/3$、判断错误的概率为 $1 - p = 1/3$。独立运行 $3$ 次，采用多数表决规则：只要至少 $2$ 次（即恰有 $2$ 次或 $3$ 次）正确，整体判定即正确。
    - **核心提示**：对 $3$ 次独立试验，把“恰对 $2$ 次”与“全对 $3$ 次”的二项概率相加；第二问从事件独立性假设切入，思考系统偏差如何引入正相关甚至使三次同错。
    - **完整分步演算**：设 $K \in \{0, 1, 2, 3\}$ 为 $3$ 次独立运行中的正确次数，$K$ 服从二项分布 $B(3, 2/3)$。分别算出恰有 $3$ 次正确与恰有 $2$ 次正确的互斥概率并相加：

      $$
      \begin{aligned}
      P_{\mathrm{maj}}
      &= \Pr(K = 3) + \Pr(K = 2) \\
      &= \binom{3}{3}p^3 + \binom{3}{2}p^2(1 - p) \\
      &= 1 \cdot \left(\frac{2}{3}\right)^3 + 3 \cdot \left(\frac{2}{3}\right)^2\left(\frac{1}{3}\right) \\
      &= \frac{8}{27} + 3 \cdot \frac{4}{9} \cdot \frac{1}{3}
       = \frac{8}{27} + \frac{12}{27}
       = \frac{20}{27}
       \approx 0.7407 \quad (74.07\%).
      \end{aligned}
      $$

      多数表决把正确率从单次的 $2/3 \approx 66.67\%$ 提升到了 $20/27 \approx 74.07\%$。
      - **为何受同一系统偏差影响时不能照搬此公式**：乘法项 $p^3$ 与 $p^2(1-p)$ 严格依赖“三次运行彼此独立、且每次正确率均为 $p = 2/3$”两个前提。如果三次运行共享同一个错误预言机、同一份未校准读出偏置或同一方向的设备漂移，错误事件之间就会高度正相关（甚至确定性同步出错）：例如在极端完全正相关的情况下，要么三次全对（概率 $2/3$）、要么三次全错（概率 $1/3$），多数表决正确率纹丝不动停在 $2/3$；若系统偏差直接导致恒错，重复再多次正确率也永远是 $0$。
    - **结论与边界回验**：独立核对失败概率（恰有 $1$ 次或 $0$ 次正确）：

      $$
      \Pr(K = 1) + \Pr(K = 0)
      = \binom{3}{1}\left(\frac{2}{3}\right)\left(\frac{1}{3}\right)^2 + \binom{3}{0}\left(\frac{1}{3}\right)^3
      = \frac{6}{27} + \frac{1}{27}
      = \frac{7}{27},
      $$

      与成功概率相加得 $\frac{20}{27} + \frac{7}{27} = \frac{27}{27} = 1$，完全自洽。
    - **易错坑提醒**：多数表决（Chernoff 指数放大）只能压低**独立随机统计误差**，绝不能修复算法或硬件里的系统偏差；做重复放大前必须先核查误差源是否跨轮次相关。

14. **【进阶】相位网格 $Q = 256$ 的二进制前缀边界反例与 Dirichlet 核概率**

    - **题意与约定**：相位寄存器使用 $t = 8$ 个控制比特，相位网格总数 $Q = 2^8 = 256$（部分文献记作 $M = 256$），真相位 $\phi = \frac{1}{4} - \frac{1}{10Q}$。按第 6 章第 6.3 节，圆周距离定义为 $d_{\mathbb{T}}(\phi, y/Q) = \min_{k\in\mathbb{Z}} |\phi - y/Q - k|$，Dirichlet 核概率公式为 $\Pr(y) = \left[\frac{\sin(\pi Q\Delta)}{Q\sin(\pi\Delta)}\right]^2$（其中 $\Delta = \phi - y/Q$）。
    - **核心提示**：先把 $\phi=1/4-1/(10Q)$ 写成二进制小数读出真实前两位，再比较整数网格点 $y=Q/4$ 与 $Q\phi$ 的距离 $\delta=|Q\phi-y|$，代入 QPE 的 Dirichlet 核概率公式 $\frac{\sin^2(\pi\delta)}{Q^2\sin^2(\pi\delta/Q)}$。
    - **完整分步演算**：
      - **步骤 1（求真相位小数与二进制前两位）**：代入 $Q = 256$ 精确计算 $\phi$：

        $$
        \phi
        = \frac{1}{4} - \frac{1}{10 \times 256}
        = \frac{1}{4} - \frac{1}{2560}
        = 0.25 - 0.000390625
        = 0.249609375.
        $$

        因为 $\frac{1}{4} = 0.01_2$，而 $\phi$ 严格小于 $\frac{1}{4}$（仅比它小了一点点），它的精确二进制展开必然形如 $0.0011111111\ldots_2$，因此真相位的**前两位是 `00`**。
      - **步骤 2（求 $y = 64$ 对应的二进制前两位）**：把读出整数 $y = 64$ 除以网格总数 $Q = 256$：

        $$
        \frac{y}{Q} = \frac{64}{256} = \frac{1}{4} = 0.01000000_2.
        $$

        如果粗暴截断只保留输出的前两位，就会报告 **`01`**——与真相位前两位 `00` 两位全不相同！
      - **步骤 3（核算数值误差与命中概率，解释为何估计依然极佳）**：计算圆周数值距离与偏差 $\Delta = \phi - \frac{64}{256} = -\frac{1}{2560}$：

        $$
        d_{\mathbb{T}}\!\left(\phi,\; \frac{64}{256}\right)
        = \left|-\frac{1}{2560}\right|
        = \frac{1}{2560}
        \approx 0.000390625
        \ll \frac{1}{4}.
        $$

        误差仅有约 $0.00039$，比两位二进制步长 $0.25$ 小了整整 $640$ 倍！再把 $\Delta = -\frac{1}{2560}$ 代入 Dirichlet 核概率公式计算该输出出现的概率：

        $$
        \Pr(64)
        = \left[\frac{\sin\!\bigl(\pi \cdot 256 \cdot (-1/2560)\bigr)}{256\sin\!\bigl(\pi \cdot (-1/2560)\bigr)}\right]^2
        = \left[\frac{\sin(\pi/10)}{256\sin(\pi/2560)}\right]^2
        \approx 0.9675 \quad (96.75\%).
        $$

        可见电路以高达 $96.75\%$ 的概率给出数值极其精准的估计 $y = 64$，只是因为 $\phi$ 紧贴在二进制进位边界 $0.01_2$ 左侧，极微小的正方向圆周抖动就跨过进位线导致二进制前缀从 `00` 翻成 `01`。
    - **结论与边界回验**：利用小角近似 $\sin(\pi/2560) \approx \pi/2560$ 快速手算核对分母：$256 \times \frac{\pi}{2560} = \frac{\pi}{10}$，故 $\Pr(64) \approx \left(\frac{\sin(\pi/10)}{\pi/10}\right)^2 = \left(\frac{0.309017}{0.314159}\right)^2 \approx (0.98363)^2 \approx 0.9675$，与精确值四位有效数字完全一致。
    - **易错坑提醒**：相位估计定理保证的是**圆周数值距离** $d_{\mathbb{T}}(\phi, y/Q) \le 2^{-n}$，而不是“输出比特串前 $n$ 位逐位无错”；如果不额外承诺真相位远离所有二进有理分界点，单纯增加更多控制比特也永远无法消除这类边界进位翻转例。

## 第 7 章

> 对应章节：《07｜代表性量子算法：从隐藏周期到量子模拟》

1. **【基础】Simon 算法中 $s = 101$ 的全部正交比特串**

   - **题意与约定**：考察 Simon 算法的线性约束 $z \cdot s \equiv 0 \pmod{2}$。将三比特串记作 $z = z_1 z_2 z_3 \in \{0,1\}^3$，把隐藏周期 $s = 101$ 代入模 $2$ 内积定义，再逐一检验全部 $2^3 = 8$ 个三比特串。
   - **核心提示**：把 $s=101$ 代入模 $2$ 内积条件 $z\cdot s=(z_1\cdot 1)\oplus(z_2\cdot 0)\oplus(z_3\cdot 1)=0$，化简成关于各位的简单等式后逐一筛查全部 $8$ 个三比特串。
   - **完整分步演算**：按模 $2$ 内积展开约束方程：

     $$
     z \cdot s = (z_1 \cdot 1) \oplus (z_2 \cdot 0) \oplus (z_3 \cdot 1) = z_1 \oplus z_3 = 0 \pmod{2},
     $$

     等价于 $z_1 = z_3$，而中间位 $z_2 \in \{0, 1\}$ 不受约束。逐个核对全部 $8$ 个串：
     - $z = 000$：$0 \oplus 0 = 0$（满足）；$z = 001$：$0 \oplus 1 = 1$（排除）；
     - $z = 010$：$0 \oplus 0 = 0$（满足）；$z = 011$：$0 \oplus 1 = 1$（排除）；
     - $z = 100$：$1 \oplus 0 = 1$（排除）；$z = 101$：$1 \oplus 1 = 0$（满足）；
     - $z = 110$：$1 \oplus 0 = 1$（排除）；$z = 111$：$1 \oplus 1 = 0$（满足）。

     共得到 $4 = 2^{3-1}$ 个允许串，与“非零 $s$ 对应 $(n-1)$ 维正交子空间”完全一致。
     - **算法求解演示（第 7 章经典 $\mathbb{F}_2$ 消元视角）**：若两轮独立采样分别抽中 $z^{(1)} = 010$ 与 $z^{(2)} = 101$，对应方程 $s_2 = 0$ 与 $s_1 \oplus s_3 = 0$，秩恰为 $n - 1 = 2$，结合非零承诺 $s \ne 000$ 立即唯一锁定 $s = 101$；反之若抽到 `000` 或与前两串线性相关的 `111`（因 $010 \oplus 101 = 111$），方程秩不增加，必须补采（群论陪集分解与奇偶权重对照见[第 16 章第 3 题](#第-16-章)）。
   - **结论与边界回验**：满足 $z \cdot s = 0$ 的三比特串共有 $4$ 个，分别是 `000`、`010`、`101`、`111`；单次理想采样在这四个串上均匀分布（各占概率 $1/4$）。
   - **易错坑提醒**：不要误以为一次采样就能读出 $s$，也不要漏掉全零串 `000`——`000` 与任何 $s$ 内积都为 $0$，但它不提供关于 $s$ 的新方程，仍需收集 $n - 1 = 2$ 条线性无关方程再经 $\mathbb{F}_2$ 高斯消元求解。

2. **【计算】Grover 搜索在 $N = 10^6$ 下的查询次数与门级下界**

   - **题意与约定**：考察查询复杂度与门复杂度的区分。对唯一目标（$M = 1$）的无结构搜索，先由旋转角公式求出最优 Grover 迭代次数 $k$，再乘以单次预言机的内部门数，评估实际门规模下界。
   - **核心提示**：套用唯一目标 Grover 最优查询次数公式 $k\approx\frac{\pi}{4}\sqrt{N}$ 算出查询量级，再乘以单次预言机内部门数估算总门数下界。
   - **完整分步演算**：设搜索空间大小 $N = 10^6$、目标数 $M = 1$，初始好态振幅 $\sin\theta = \sqrt{M/N} = 10^{-3}$，由于 $\theta = \arcsin(10^{-3}) \approx 10^{-3}\,\mathrm{rad}$ 很小，迭代 $k$ 轮后好态概率为 $\sin^2\bigl((2k + 1)\theta\bigr)$。令 $(2k + 1)\theta \approx \frac{\pi}{2}$ 得：

     $$
     k \approx \frac{\pi}{4\theta} - \frac{1}{2} \approx \frac{\pi}{4}\sqrt{10^6} - 0.5 \approx 785.398 - 0.5 \approx 785.
     $$

     回验 $k = 785$ 时，$(2\times 785 + 1)\arcsin(10^{-3}) = 1571 \times 0.00100000017 \approx 1.571000\,\mathrm{rad}$，命中概率 $\sin^2(1.571000) \approx 0.99999996$。若每次调用预言机需要 $10^4$ 个基本门，仅预言机本身就消耗：

     $$
     785 \times 10^4 = 7.85 \times 10^6\ \text{个门}.
     $$

   - **结论与边界回验**：Grover 查询次数约为 $785$ 次（$10^2\text{--}10^3$ 量级）；计入每次 $10^4$ 门的预言机后，总门数至少达到 $7.85 \times 10^6$（约千万门量级），且尚未计入扩散算子多控反射、芯片路由、量子纠错与重跑开销。
   - **易错坑提醒**：把“约 $785$ 次查询”直接当成“约 $785$ 个逻辑门”或“一定比经典计算机快”。一次抽象查询内部可能藏着成千上万个可逆算术门，必须把预言机展开到同一门级与墙钟时间口径才能与经典并行搜索比较。

3. **【计算】Shor 算法中 $N = 21,\, a = 2$ 的求阶与因子检验**

   - **题意与约定**：考察 Shor 算法的经典数论约化流程：先检查 $\gcd(a, N) = 1$，再顺次计算 $a^x \bmod N$ 找出最小正整数阶 $r$，验证两个好阶条件（$r$ 为偶数且 $a^{r/2} \not\equiv -1 \pmod{N}$），最后用欧几里得算法求最大公因数。
   - **核心提示**：先确认 $\gcd(2,21)=1$，逐次计算 $2^1,2^2,\dots\bmod 21$ 直到首次出现 $1$ 得到阶 $r$，再检验 $r$ 是否为偶数以及 $2^{r/2}\not\equiv -1\pmod{21}$，最后算 $\gcd(2^{r/2}\pm 1,21)$。
   - **完整分步演算**：因 $\gcd(2, 21) = 1$，逐项计算 $2^x \bmod 21$：
     - $2^1 \equiv 2$，$2^2 \equiv 4$，$2^3 \equiv 8$，$2^4 \equiv 16$；
     - $2^5 = 32 = 21 + 11 \equiv 11$；
     - $2^6 = 2 \times 11 = 22 = 21 + 1 \equiv 1 \pmod{21}$。

     首次回到 $1$ 时指数为 $r = 6$。检查两个条件：① $r = 6$ 为偶数，半阶 $r/2 = 3$；② $2^3 = 8 \not\equiv -1 \equiv 20 \pmod{21}$。利用平方差分解 $2^6 - 1 = (2^3 - 1)(2^3 + 1) \equiv 0 \pmod{21}$，分别计算最大公因数：

     $$
     \gcd(2^3 - 1, 21) = \gcd(7, 21) = 7, \qquad \gcd(2^3 + 1, 21) = \gcd(9, 21) = 3.
     $$

     回验 $3 \times 7 = 21$，确为两个非平凡素因子。
   - **结论与边界回验**：底数 $a = 2$ 模 $21$ 的阶为 $r = 6$，满足全部好阶条件，本轮可直接分解出非平凡因子 $3$ 与 $7$。
   - **易错坑提醒**：忽略检验 $a^{r/2} \equiv -1 \pmod{N}$ 或直接用 $2^r - 1$ 算公因数。只有半阶幂 $a^{r/2}$ 既不模 $N$ 余 $1$ 也不余 $-1$ 时，$N$ 的素因子才会拆散到 $a^{r/2} - 1$ 与 $a^{r/2} + 1$ 两侧。

4. **【基础】分解 $N = 15$ 时测得相位 $1/2$ 为何不够**

   - **题意与约定**：考察 QPE 相位读数 $k/r$ 与连分数恢复分母时的“约分丢因子”陷阱。连分数只能恢复既约分数 $k'/r'$ 的分母 $r'$，当抽中的分支编号 $k$ 与真阶 $r$ 不互素时，$r'$ 只是 $r$ 的真约数。
   - **核心提示**：把 QPE 输出写成 $k/r$，思考当随机分支编号 $k$ 与真实阶 $r$ 存在公因子时，约分后的既约分数分母 $r'$ 与真阶 $r$ 之间是什么关系，以及连分数算法能恢复哪一个。
   - **完整分步演算**：在 $N = 15,\, a = 2$ 中，$2^1, 2^2, 2^3, 2^4 \bmod 15$ 依次为 $2, 4, 8, 1$，真实阶 $r = 4$。理想 QPE 等概率输出四个相位 $\phi_k = k/4$（$k \in \{0, 1, 2, 3\}$）。当抽中 $k = 2$ 时，读出相位为：

     $$
     \frac{k}{r} = \frac{2}{4} = \frac{1}{2}.
     $$

     对其做连分数展开，给出的候选分母为 $d = 2$。代入经典模幂验证：

     $$
     2^2 \bmod 15 = 4 \not\equiv 1 \pmod{15},
     $$

     验证失败！根本原因是 $\gcd(k, r) = \gcd(2, 4) = 2 > 1$，约分抹掉了因子 $2$。
   - **结论与边界回验**：相位 $1/2$ 是 $2/4$ 约分后的结果，连分数仅能给出伪分母 $2$，经 $2^2 \equiv 4 \not\equiv 1 \pmod{15}$ 检验被拒绝；标准做法是重新采样直至抽中与 $r$ 互素的 $k$（如 $k = 1$ 或 $3$），或对多次采得的真约数取最小公倍数。
   - **易错坑提醒**：以为小例里顺手试乘小倍数 $2 \times 2 = 4$ 总能补救。对大整数 $N$，丢失的公因子 $\gcd(k, r)$ 可能很大，无上界枚举倍数不具有多项式时间保证，不能替代重新采样。

5. **【基础】HHL 算法为何通常不适合“打印全部解分量”**

   - **题意与约定**：考察 HHL 的输出形态（量子态编码 vs 经典坐标数组）与读出复杂度下界，对应 Aaronson 四重细则中的第四重（输出读出瓶颈）。
   - **核心提示**：区分 HHL 输出的“编码解向量的量子态 $|x\rangle$”与“$N$ 个经典浮点坐标数组”：从量子态层析提取全部 $N$ 个分量至少需要多少次测量？再对比需要提取单一标量特征值 $\langle x|M|x\rangle$ 的情形。
   - **完整分步演算**：设线性方程组 $A\vec{x} = \vec{b}$ 维数为 $N$，HHL 算法制备的是归一化量子态：

     $$
     |x\rangle = \frac{1}{\lVert A^{-1}\vec{b}\rVert}\sum_{j=0}^{N-1} x_j |j\rangle.
     $$

     该态只需 $n = \lceil\log_2 N\rceil$ 个量子比特存储，但量子测量每次只能按概率 $|x_j|^2 / \lVert\vec{x}\rVert^2$ 返回一个下标 $j$，无法一次吐出全部 $N$ 个复振幅。若任务要求把全部 $N$ 个解分量打印到经典内存（哪怕仅达到 $\ell_2$ 误差 $\epsilon$），仅输出结果的长度就是 $N$ 个浮点数，且层析/振幅估计至少需要 $\Omega(N/\epsilon)$ 至 $\Omega(N/\epsilon^2)$ 次重复制备 $|x\rangle$。一旦乘上 $\Omega(N)$ 读出成本，HHL 相对经典共轭梯度法 $O(Ns\sqrt{\kappa}\ln(1/\epsilon))$ 的 $O(\log_2 N)$ 维度优势瞬间归零。
   - **结论与边界回验**：HHL 只输出量子态 $|x\rangle$ 而非经典坐标清单；打印全部分量必然付出至少 $\Omega(N)$ 的读出代价，彻底抵消指数加速，因此 HHL 只适合提取某个可高效测量的全局标量（如 $\langle x|M|x\rangle$）。
   - **易错坑提醒**：把“制备出 $|x\rangle$ 只需 $O(\log_2 N)$ 规模”误读为“求出了全部 $N$ 个数值解”，并忽略估计单个全局标量到误差 $\epsilon$ 时采样或 QAE 还会额外引入 $1/\epsilon^2$ 或 $1/\epsilon$ 的乘法因子。

6. **【基础】理想量子模拟之外的四类端到端成本**

   - **题意与约定**：考察端到端量子算法资源核算框架。教科书常把注意力集中在主演化线路 $e^{-iHt}$ 的抽象步数上，而现实落地必须补齐从输入到输出的全链路开销。
   - **核心提示**：把视角从单纯演化电路 $e^{-iHt}$ 拉开到完整任务链路，按“初态制备 → 哈密顿量编码/编译 → 测量与采样 → 纠错与经典后处理”四个环节逐一盘点遗漏成本。
   - **完整分步演算**：将一条真实量子模拟任务从头到尾拆开，理想演化之外至少包含以下核心成本环节：
     1. **初态制备与输入装载成本**：制备与目标物理基态有足够大重叠的初态 $|\psi_0\rangle$，或把经典系数/数据装载进线路；
     2. **哈密顿量编码与门编译开销**：将抽象项 $H_\gamma$ 编译为原生 Clifford+$T$ 门（或 LCU 的 PREPARE/SELECT 线路），以及受限于硬件拓扑连通性的 SWAP 路由深度；
     3. **量子纠错与魔法态资源成本**：为维持长线路低逻辑错误率所需的码距扩张、物理比特倍增、魔法态蒸馏/培育池以及实时经典解码延迟；
     4. **重复测量、输出读出与经典后处理成本**：按目标统计精度 $\epsilon$ 重复执行全流程 $O(1/\epsilon^2)$（或 QAE 的 $O(1/\epsilon)$）次、计算置信区间，并与同精度下的强经典算法比较墙钟时间。
   - **结论与边界回验**：除理想演化线路外，端到端成本至少必须计入初态制备、哈密顿量编译与路由、纠错与魔法态开销、重复采样读出及经典后处理等环节（任选其中四项并明确具体开销来源即可完整作答）。
   - **易错坑提醒**：仅拿“Trotter 步数 $r$ 是多项式”就直接宣称实用优势，忽略单步内部的 $T$-count 编译、魔法态等待时间和为压低采样方差付出的巨额重复运行次数。

7. **【计算】$H = X + Z,\, t = 0.2$ 的一阶 Trotter 步数对易子估算**

   - **题意与约定**：考察一阶 Lie–Trotter 公式的谱范数对易子误差上界 $\left\|e^{-i(A+B)t} - (e^{-iAt/r}e^{-iBt/r})^r\right\| \le \frac{t^2}{2r}\|[A, B]\|$。先严格算出对易子 $[X, Z]$ 及其谱范数，再解不等式求出充分步数 $r$。
   - **核心提示**：先计算矩阵对易子 $[X,Z]$ 及其谱范数 $\|[X,Z]\|$，再代入一阶 Trotter 误差上界 $\frac{t^2}{2r}\|[X,Z]\|\le\varepsilon$ 反解最小正整数步数 $r$。
   - **完整分步演算**：令 $A = X,\, B = Z$，用 Pauli 乘法规则 $XZ = -iY$、$ZX = +iY$ 计算对易子：

     $$
     [X, Z] = XZ - ZX = -iY - (iY) = -2iY.
     $$

     因 $Y$ 的本征值为 $\pm 1$，谱范数 $\|Y\| = 1$，故 $\|[X, Z]\| = |-2i|\cdot\|Y\| = 2$。将 $t = 0.2$ 与 $\|[X, Z]\| = 2$ 代入一阶误差上界：

     $$
     \frac{t^2}{2r}\|[X, Z]\| = \frac{0.2^2}{2r}\times 2 = \frac{0.04}{r}.
     $$

     要求上界不超过 $2 \times 10^{-3}$：

     $$
     \frac{0.04}{r} \le 2 \times 10^{-3} \iff r \ge \frac{0.04}{0.002} = 20.
     $$

     用精确矩阵指数数值独立验算：$r = 20$ 时实际谱范数误差为 $0.001973 < 0.002$（$r = 19$ 时实际误差为 $0.002077 > 0.002$，在本题中恰好也非常贴近上界）。
   - **结论与边界回验**：按一阶对易子上界估算，至少需要 $r = 20$ 步（共 $2r = 40$ 次单比特指数旋转门）。
   - **易错坑提醒**：把对易子上界算出的 $r \ge 20$ 误解为一般情况下的必要下界——上界给出的是保证达标的充分步数，在许多高维局域体系中实际误差可能远小于粗略上界；另外也不要漏掉 $[X, Z] = -2iY$ 里的系数 $2$。

8. **【进阶】幅度估计 $a = 1/2$ 时相位 $1/4$ 与 $3/4$ 为何对应同一概率**

   - **题意与约定**：考察 QPE 型量子幅度估计（BHMT）中 Grover 算符 $\mathcal{Q}$ 的共轭本征值结构。初态是 $\mathcal{Q}$ 两个共轭本征态的等权叠加，QPE 输出对称双峰 $\phi_+ = \theta/\pi$ 与 $\phi_- = 1 - \theta/\pi$，但还原概率时取 $\sin^2(\pi\phi)$ 消除了正负角歧义。
   - **核心提示**：回忆 Grover 迭代算符 $\mathcal Q$ 在二维子空间上的两个本征值为共轭对 $e^{\pm 2i\theta}$（对应相位 $\phi$ 与 $1-\phi$），再将两个相位分别代入还原公式 $a=\sin^2(\pi\phi)$ 验证结果。
   - **完整分步演算**：由 $a = \sin^2\theta = \frac{1}{2}$ 且 $\theta \in [0, \pi/2]$，得 $\sin\theta = \frac{1}{\sqrt{2}} \implies \theta = \frac{\pi}{4}$。Grover 算符 $\mathcal{Q}$ 在二维不变子空间中的两个本征值为：

     $$
     \lambda_+ = e^{+2i\theta} = e^{+i\pi/2} = e^{2\pi i(1/4)}, \qquad
     \lambda_- = e^{-2i\theta} = e^{-i\pi/2} = e^{2\pi i(3/4)}.
     $$

     因此 QPE 等概率输出归一化相位 $\tilde\phi = 1/4$ 与 $\tilde\phi = 3/4$（后者在圆周上等价于负相位 $-1/4$，对应旋转角 $-\pi/4$）。套用还原公式 $\tilde a = \sin^2(\pi\tilde\phi)$ 分别核验：

     $$
     \tilde\phi = \frac{1}{4}:\ \sin^2\!\left(\frac{\pi}{4}\right) = \left(\frac{\sqrt{2}}{2}\right)^2 = \frac{1}{2}; \qquad
     \tilde\phi = \frac{3}{4}:\ \sin^2\!\left(\frac{3\pi}{4}\right) = \left(\frac{\sqrt{2}}{2}\right)^2 = \frac{1}{2}.
     $$

     等价地，用折叠公式 $\tilde\theta = \pi\min(\tilde\phi,\, 1 - \tilde\phi)$ 对两者都得到 $\tilde\theta = \pi/4$。
   - **结论与边界回验**：相位 $1/4$ 与 $3/4$ 分别对应 Grover 旋转角 $+\pi/4$ 与 $-\pi/4$（在圆周上关于 $0$ 对称），经 $\sin^2(\pi\tilde\phi)$ 映射后给出完全相同的概率估计 $\tilde a = 1/2$。
   - **易错坑提醒**：误以为出现两个等高测量峰说明算法出错或结果有歧义。双峰是初态 $A|0^n\rangle$ 等权投影到 $|\Psi_\pm\rangle$ 的必然结果，只要恢复目标是概率 $a = \sin^2\theta$，两峰提供的信息完全一致。

9. **【进阶】$\mathrm{PostBQP} = \mathrm{PP}$ 为何不意味着现实量子机可高效解 $\mathrm{PP}$**

   - **题意与约定**：考察理论复杂度类模型（允许后选择的 $\mathrm{PostBQP}$）与物理可实现模型（$\mathrm{BQP}$）的本质区别。后选择在数学定义中免费丢弃失败分支，但在物理现实中只能靠重复试验等待极小概率事件发生。
   - **核心提示**：对照 $\mathrm{PostBQP}$ 与 $\mathrm{BQP}$ 的定义差别：前者允许以零成本强制保留指数级稀有的后选择分支，而现实物理实验想要拿到一次成功分支需付出与接受率倒数成正比的重复次数。
   - **完整分步演算**：$\mathrm{PostBQP}$ 在多项式时间量子线路的基础上额外赋予一项非物理能力：允许指定一个后选择比特，强制只保留该比特测得 `1` 的条件分布，即便事件 `1` 的原始发生概率低至指数级小 $p_{\mathrm{post}} = 2^{-\mathrm{poly}(n)}$。Aaronson（2005）证明 $\mathrm{PostBQP} = \mathrm{PP}$，恰恰说明“免费后选择”本身注入了巨大的计算威力。在现实的 $\mathrm{BQP}$ 设备上模拟一次成功的后选择，独立重复运行的期望次数为：

     $$
     \mathbb{E}[\text{重试次数}] = \frac{1}{p_{\mathrm{post}}} = 2^{\mathrm{poly}(n)},
     $$

     这直接退化为指数时间开销，超出多项式时间类 $\mathrm{BQP}$ 的能力边界（目前复杂度理论普遍相信 $\mathrm{BQP} \subsetneq \mathrm{PP}$）。
   - **结论与边界回验**：$\mathrm{PostBQP} = \mathrm{PP}$ 是理论模型之间的等价定理，依赖于物理上不可免费获得的指数级后选择能力；现实量子计算机属于 $\mathrm{BQP}$，并不能借此在多项式时间内解决所有 $\mathrm{PP}$ 或 $\mathrm{NP}$ 问题。
   - **易错坑提醒**：把物理实验里的“小规模后选择”（例如成功率 $10\%$ 时多跑 $10$ 次）外推到大规模问题，忽略一旦接受率随规模 $n$ 指数衰减，重试墙钟时间就会指数爆炸。

10. **【进阶】稀疏预言机、LCU 与块编码三种输入模型各隐藏了什么成本**

    - **题意与约定**：考察哈密顿量模拟与量子线性系统算法的接口记账。把一次抽象访问记为 $O(1)$ 查询时，不同输入模型把截然不同的电路实现、辅助比特和归一化代价藏进了黑盒内部。
    - **核心提示**：分别拆解三种输入接口在抽象“一次访问”背后的电路账：稀疏预言机的行列定位与振幅查表电路、LCU 的 $\mathrm{PREPARE}/\mathrm{SELECT}$ 与 1-范数 $\lambda$、块编码的缩放因子 $\alpha$ 与辅助位后选择概率。
    - **完整分步演算**：逐一拆开三种模型的内部实现成本：
      - **稀疏预言机（Sparse Oracle）**：要求提供两个可逆黑盒 $O_F$（给出行号 $j$ 与序号 $\ell$ 返回第 $\ell$ 个非零元列号）和 $O_H$（返回矩阵元 $H_{jk}$ 的二进制编码）。“访问一次”隐藏了定位稀疏非零结构、按目标精度计算矩阵元数值以及反计算清零垃圾辅助位的全部可逆算术电路开销。
      - **酉算符线性组合（LCU）**：把 $H = \sum_{j=1}^{L} \alpha_j U_j$（$\alpha_j > 0$）拆成 $\mathrm{PREPARE}$ 与 $\mathrm{SELECT}$ 两个子线路。“访问一次”隐藏了将系数 $\sqrt{\alpha_j/\lambda}$ 装载到 $\lceil\log_2 L\rceil$ 个辅助比特的态制备成本、按辅助比特逐项受控执行 $L$ 个 $U_j$ 的多控门深度，以及 1-范数 $\lambda = \sum_j \alpha_j$ 带来的演化步数放大。
      - **块编码（Block Encoding）**：将 $H/\alpha$ 嵌入更大酉矩阵 $U$ 的左上子块（$(\langle 0^a|\otimes I)U(|0^a\rangle\otimes I) = H/\alpha$）。“访问一次”隐藏了构造整个高维酉矩阵 $U$ 的逻辑门数、所需的 $a$ 个辅助比特、放大模拟成本的缩放因子 $\alpha \ge \|H\|$，以及块编码本身的截断近似误差 $\epsilon_{\mathrm{BE}}$。
    - **结论与边界回验**：稀疏预言机隐藏稀疏索引与矩阵元算术电路；LCU 隐藏 $\mathrm{PREPARE}/\mathrm{SELECT}$ 电路与 $\lambda$ 放大；块编码隐藏大酉矩阵门数、辅助比特数、缩放因子 $\alpha$ 与编码误差。横向比较算法复杂度前，必须将三者展开到相同的门级资源口径。
    - **易错坑提醒**：看到某算法声称“只需 $O(\log_2 N)$ 次查询”就默认它端到端也是对数时间，没有核查把给定物理哈密顿量塞进黑盒接口本身是否需要多项式甚至 $\Theta(N)$ 门数。

11. **【基础】Simon 算法 $s = 110$ 的三次测量方程与非零承诺求解**

    - **题意与约定**：考察 Simon 算法的经典 $\mathbb{F}_2$ 线性方程组求解与样本冗余现象。先把每次测得的比特串 $z$ 写成模 $2$ 线性方程，再检查线性独立性，最后结合“$s \neq 000$”的承诺唯一锁定 $s$。
    - **核心提示**：把每次测得的 $z$ 依次写成模 $2$ 线性方程 $z\cdot s=0$，检查哪条方程与先前重复（不增加秩），再联立独立方程并结合非零承诺 $s\neq 000$ 确定唯一解。
    - **完整分步演算**：设未知隐藏串为 $s = s_1 s_2 s_3 \in \{0, 1\}^3$，逐条写出三次测量给出的模 $2$ 方程 $z \cdot s = 0 \pmod{2}$：
      - 第 1 次测得 $z^{(1)} = 001$：$(0\cdot s_1) \oplus (0\cdot s_2) \oplus (1\cdot s_3) = 0 \implies s_3 = 0$；
      - 第 2 次测得 $z^{(2)} = 110$：$(1\cdot s_1) \oplus (1\cdot s_2) \oplus (0\cdot s_3) = 0 \implies s_1 \oplus s_2 = 0 \iff s_1 = s_2$；
      - 第 3 次测得 $z^{(3)} = 001$：再次给出 $s_3 = 0$，与第 1 条完全重合，系数矩阵的秩仍停留在 $2$，**没有增加任何新信息**。

      联立独立方程 $s_3 = 0$ 与 $s_1 = s_2$，齐次线性方程组的解空间含两个向量：$s = 000$ 与 $s = 110$。由本题（及 Simon 承诺）已知 $s \neq 000$，排除平凡零解后唯一确定 $s = 110$。回验：$001 \cdot 110 = 0$，$110 \cdot 110 = 1 \oplus 1 = 0$，全部满足。
    - **结论与边界回验**：三条方程依次为 $s_3 = 0$、$s_1 \oplus s_2 = 0$、$s_3 = 0$；第 3 次测量（`001`）与第 1 次重复、未增加信息；联合前两条独立方程与 $s \neq 000$ 的承诺，唯一解得 $s = 110$。
    - **易错坑提醒**：把“完成了 $k$ 次量子查询”误当成“已经攒齐 $k$ 条线性无关方程”。随机采样可能重复命中已有行或其线性组合，实际需要检验 $\mathbb{F}_2$ 高斯消元的秩是否达到 $n - 1$。

12. **【计算】$N = 4$ 且目标为 `11` 的 Grover 一轮逐振幅手算**

    - **题意与约定**：考察 Grover 迭代 $\mathcal{Q} = D S_G$ 的两步操作（相位标记 $S_G$ 与关于均值反射 $D = 2|s\rangle\langle s| - I$）。固定计算基顺序 $|00\rangle, |01\rangle, |10\rangle, |11\rangle$，一步步算清全部四个振幅。
    - **核心提示**：沿用大端序 $(|00\rangle,|01\rangle,|10\rangle,|11\rangle)$，从全 $1/2$ 均匀态依次执行标记 $S_G$、求均值 $\bar a$ 与扩散反射 $2\bar a-a_x$；算完第 $1$ 轮后不妨顺手再推第 $2$ 轮，感受过旋转现象。
    - **完整分步演算**：
      1. **均匀初态**：$|s\rangle = H^{\otimes 2}|00\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$，四个振幅依次为 $\left(\frac{1}{2},\, \frac{1}{2},\, \frac{1}{2},\, \frac{1}{2}\right)$。
      2. **标记预言机 $S_G$**：仅把目标态 $|11\rangle$ 的振幅反号，其余不变，得到：

         $$
         S_G|s\rangle = \frac{1}{2}|00\rangle + \frac{1}{2}|01\rangle + \frac{1}{2}|10\rangle - \frac{1}{2}|11\rangle,
         $$

         标记后四个振幅为 $\left(\frac{1}{2},\, \frac{1}{2},\, \frac{1}{2},\, -\frac{1}{2}\right)$。
      3. **计算平均振幅 $\bar{a}$**：

         $$
         \bar{a} = \frac{1}{4}\left(\frac{1}{2} + \frac{1}{2} + \frac{1}{2} - \frac{1}{2}\right) = \frac{1}{4} \times 1 = \frac{1}{4}.
         $$

      4. **扩散算子 $D$（关于均值反射 $a_x \mapsto 2\bar{a} - a_x = \frac{1}{2} - a_x$）**：
         - $a'_{00} = \frac{1}{2} - \frac{1}{2} = 0$；$a'_{01} = \frac{1}{2} - \frac{1}{2} = 0$；$a'_{10} = \frac{1}{2} - \frac{1}{2} = 0$；
         - $a'_{11} = \frac{1}{2} - \left(-\frac{1}{2}\right) = 1$。

         核验归一化：$0^2 + 0^2 + 0^2 + 1^2 = 1$。
      - **算法迭代深化：第 $2$ 轮过度旋转（over-rotation）逐振幅手算（与[第 6 章第 3 题](#第-6-章)拉开递进层次）**：从第 $1$ 轮所得确定目标态 $\vec{a}^{(1)} = (0, 0, 0, 1)$ 出发，如果算法不知道已达峰值而继续执行第 $2$ 轮 Grover 迭代 $\mathcal{Q} = D S_G$：
        - 再次标记 $S_G$：仅把 $|11\rangle$ 反号，得 $(0, 0, 0, -1)$；
        - 计算新平均振幅：$\bar{a}^{(2)} = \frac{0 + 0 + 0 - 1}{4} = -\frac{1}{4}$，故 $2\bar{a}^{(2)} = -\frac{1}{2}$；
        - 关于均值反射 $a''_x = 2\bar{a}^{(2)} - a_x = -\frac{1}{2} - a_x$，逐分量算得：

          $$
          a''_{00} = a''_{01} = a''_{10} = -\frac{1}{2},
          \qquad
          a''_{11} = -\frac{1}{2} - (-1) = +\frac{1}{2}.
          $$

        此时归一化仍成立（$4\times(1/4) = 1$），但测得目标 `11` 的概率已从 $100\%$ 暴跌回 $|+1/2|^2 = 1/4 = \sin^2(5\pi/6)$——恰好退回无任何搜索时的随机猜测水平！这直观解释了为何 Grover 是二维平面上的周期旋转而非单调收敛。
    - **结论与边界回验**：标记后四个振幅为 $\left(\frac{1}{2}, \frac{1}{2}, \frac{1}{2}, -\frac{1}{2}\right)$，平均振幅 $\bar{a} = \frac{1}{4}$，扩散后四个振幅变为 $(0, 0, 0, 1)$，一次迭代即以概率 $1$ 精准测得 `11`。
    - **易错坑提醒**：误把 $N = 4,\, M = 1$ 的精确特例（因 $\arcsin(1/2) = \pi/6$，恰好 $3 \times \frac{\pi}{6} = \frac{\pi}{2}$）当成一般 Grover 一次就能 $100\%$ 命中；对一般 $N$ 不仅需要 $\approx \frac{\pi}{4}\sqrt{N}$ 轮，而且再多转反而会过旋转导致成功率暴跌。

13. **【计算】$Q = 16$ 周期态经 QFT 后 $y = 4$ 与 $y = 1$ 的振幅推导**

    - **题意与约定**：考察 QFT 如何通过相长干涉与相消干涉将周期结构转换为频谱尖峰。套用第 07 章第 2.2 节的 QFT 定义 $F_{16}|x\rangle = \frac{1}{\sqrt{16}}\sum_{y=0}^{15} e^{2\pi i xy / 16}|y\rangle$，直接写出输出态 $|y\rangle$ 的振幅公式再代入 $y = 4$ 与 $y = 1$。
    - **核心提示**：把周期态代入 $\operatorname{QFT}_{16}|x\rangle=\frac{1}{4}\sum_{y=0}^{15}e^{2\pi i xy/16}|y\rangle$，对 $x\in\{0,4,8,12\}$ 写出等比级数求和 $\sum_{m=0}^3 (e^{i\pi y/2})^m$，分别代入 $y=4$ 与 $y=1$。
    - **完整分步演算**：输入周期态可写成 $|P\rangle = \frac{1}{2}\sum_{j=0}^{3} |4j\rangle$。由线性性施加 $F_{16}$：

      $$
      F_{16}|P\rangle = \frac{1}{2}\sum_{j=0}^{3} \left(\frac{1}{4}\sum_{y=0}^{15} e^{2\pi i (4j)y / 16}|y\rangle\right)
      = \sum_{y=0}^{15} \underbrace{\left(\frac{1}{8}\sum_{j=0}^{3} e^{2\pi i j y / 4}\right)}_{A_y}|y\rangle.
      $$

      - **代入 $y = 4$**：指数因子变为 $e^{2\pi i j \cdot 4 / 4} = e^{2\pi i j} = 1$（对 $j = 0, 1, 2, 3$ 均成立），四项完全同相相长：

        $$
        A_4 = \frac{1 + 1 + 1 + 1}{8} = \frac{4}{8} = \frac{1}{2}.
        $$

      - **代入 $y = 1$**：四项依次是 $e^0 = 1$、$e^{i\pi/2} = i$、$e^{i\pi} = -1$、$e^{3i\pi/2} = -i$，在单位圆上均匀对称分布、两两相消：

        $$
        A_1 = \frac{1 + i - 1 - i}{8} = 0.
        $$

      同理，仅 $y \in \{0, 4, 8, 12\}$ 四处非零且振幅均为 $1/2$，概率和为 $4 \times (1/2)^2 = 1$。
    - **结论与边界回验**：$y = 4$ 处四条周期分支同相叠加，给出 $A_4 = 1/2$（概率 $1/4$）；$y = 1$ 处四项对应单位圆四等分点 $1, i, -1, -i$，完全相消得 $A_1 = 0$。
    - **易错坑提醒**：漏算输入态系数 $1/2$ 或 QFT 归一化因子 $1/\sqrt{16} = 1/4$ 而算错总系数 $1/8$；另外若换用逆 QFT，仅指数取负号，四根峰的位置 $\{0, 4, 8, 12\}$ 与概率 $1/4$ 完全不变。

14. **【计算】二维对角 HHL（$A = \operatorname{diag}(1, 2),\, |b\rangle = |+\rangle,\, C = 1$）成功概率与解态**

    - **题意与约定**：考察 HHL 的受控旋转与后选择归一化规则。对角矩阵直接读出本征值 $\lambda_1 = 1,\, \lambda_2 = 2$，先核查常数 $C$ 的合法性（$0 < C \le \min_j |\lambda_j|$），写出辅助比特为 `1` 的未归一化分支，再分别求范数平方（成功概率）与归一化条件解态。
    - **核心提示**：先确认旋转常数 $C\le\lambda_{\min}$ 合法，把 $|b\rangle=|+\rangle$ 写成两个本征态的叠加，对每个本征分支按受控旋转 $\sqrt{1-(C/\lambda_j)^2}|0\rangle+(C/\lambda_j)|1\rangle$ 写出辅助位振幅，再对辅助位为 $|1\rangle$ 分支求成功概率并重归一化。
    - **完整分步演算**：矩阵 $A = \operatorname{diag}(1, 2)$ 的两个本征态为 $|0\rangle$（$\lambda_1 = 1$）与 $|1\rangle$（$\lambda_2 = 2$），故 $C = 1 \le \min(1, 2)$ 合法，受控 $R_y(\theta_j)$ 旋转角满足 $\sin(\theta_j/2) = C/\lambda_j \le 1$（即 $\theta_j = 2\arcsin(C/\lambda_j)$）。经 QPE、受控旋转与理想逆 QPE 清零相位位后，系统与辅助比特的联合态为：

      $$
      \frac{1}{\sqrt{2}}|0\rangle\Bigl(\sqrt{1 - 1^2}|0\rangle_a + 1|1\rangle_a\Bigr)
      + \frac{1}{\sqrt{2}}|1\rangle\Bigl(\sqrt{1 - (1/2)^2}|0\rangle_a + \frac{1}{2}|1\rangle_a\Bigr).
      $$

      抽出辅助比特为 $|1\rangle_a$ 的未归一化分支（即 $C A^{-1}|b\rangle$）：

      $$
      |\tilde{x}\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{2\sqrt{2}}|1\rangle.
      $$

      计算辅助比特测得 `1` 的成功概率 $p_{\mathrm{succ}} = \langle\tilde{x}|\tilde{x}\rangle$：

      $$
      p_{\mathrm{succ}} = \left|\frac{1}{\sqrt{2}}\right|^2 + \left|\frac{1}{2\sqrt{2}}\right|^2 = \frac{1}{2} + \frac{1}{8} = \frac{5}{8} = 0.625.
      $$

      将 $|\tilde{x}\rangle$ 除以 $\sqrt{p_{\mathrm{succ}}} = \sqrt{5/8} = \frac{\sqrt{5}}{2\sqrt{2}}$ 得归一化条件解态：

      $$
      |x\rangle = \frac{2\sqrt{2}}{\sqrt{5}}\left(\frac{1}{\sqrt{2}}|0\rangle + \frac{1}{2\sqrt{2}}|1\rangle\right)
      = \frac{2|0\rangle + |1\rangle}{\sqrt{5}}.
      $$

      回验归一化：$(2/\sqrt{5})^2 + (1/\sqrt{5})^2 = 4/5 + 1/5 = 1$，且 $A|x\rangle = (2|0\rangle + 2|1\rangle)/\sqrt{5} \propto |+\rangle = |b\rangle$。
    - **结论与边界回验**：辅助比特测得 `1` 的成功概率为 $p_{\mathrm{succ}} = 5/8 = 62.5\%$；成功后的归一化条件解态为 $|x\rangle = \frac{2|0\rangle + |1\rangle}{\sqrt{5}}$。
    - **易错坑提醒**：把未归一化分支 $|\tilde{x}\rangle$ 直接当成物理态，或忘记把成功概率 $5/8$ 记进运行总账——其余 $3/8$ 的运行会测得辅助比特 `0`（失败态 $|1\rangle|0\rangle_a$），必须重跑或配合振幅放大。

15. **【基础】分解 $N = 15$ 选到坏底数 $a = 14$ 的求阶与失败原因**

    - **题意与约定**：考察 Shor 算法经典约化中的“负一坏条件”$a^{r/2} \equiv -1 \pmod{N}$。验证 $14$ 模 $15$ 的最小正阶 $r$ 后，代入 $\gcd(a^{r/2} \pm 1, N)$ 观察平方差为何未能拆开 $15$。
    - **核心提示**：计算 $14^1,14^2\bmod 15$（提示：$14\equiv -1\pmod{15}$）找出阶 $r$，再检验 Shor 好阶第二条件 $a^{r/2}\not\equiv -1\pmod{N}$ 为何在此失效并导致 $\gcd$ 退化。
    - **完整分步演算**：因 $\gcd(14, 15) = 1$ 且 $14 \equiv -1 \pmod{15}$，逐次计算幂次模 $15$：

      $$
      14^1 \equiv 14 \not\equiv 1 \pmod{15}, \qquad
      14^2 = 196 = 13 \times 15 + 1 \equiv 1 \pmod{15}.
      $$

      故最小正阶为 $r = 2$（是偶数，半阶 $r/2 = 1$）。此时半阶幂为 $14^{2/2} = 14 \equiv -1 \pmod{15}$，直接触发坏条件！将其代入最大公因数公式：

      $$
      \gcd(14^1 - 1, 15) = \gcd(13, 15) = 1, \qquad
      \gcd(14^1 + 1, 15) = \gcd(15, 15) = 15.
      $$

      因为 $15$ 整除了整个括号 $(14 + 1)$，而与另一侧 $(14 - 1) = 13$ 互素，$15$ 的两个素因子 $3$ 和 $5$ 没有分居两侧，导致只吐出平凡因子 $1$ 和 $15$。
    - **结论与边界回验**：$a = 14$ 模 $15$ 的最小正阶为 $r = 2$；阶虽完全求对且为偶数，但因 $a^{r/2} = 14 \equiv -1 \pmod{15}$ 满足平凡坏条件，两个最大公因数仅给出平凡因子 $1$ 和 $15$，须重新随机选取底数 $a$（如 $a = 2, 7, 11$）再试。
    - **易错坑提醒**：误以为算不出非平凡因子一定是量子相位估计或连分数出了错。Shor 算法在量子求阶 $100\%$ 准确的前提下，仍有来自经典数论约化的固有失败分支（奇阶或 $a^{r/2} \equiv -1 \pmod{N}$），对奇合数 $N$（含 $m \ge 2$ 个不同奇素因子）单次抽中好底数的概率至少为 $1 - 2^{1-m} \ge 1/2$。

## 第 8 章

> 对应章节：《08｜应用、变分算法与证据边界》

1. **【基础】VQE 变分原理的保证范围与有限采样“击穿基态”反例**

   - **题意与约定**：考察 Rayleigh–Ritz 变分原理的数学前提与“精确期望”和“有限次采样估计”的区别。先把任意归一化试探态在哈密顿量本征基下展开证明下界，再逐项剖析为何实验读数可以偶然低于真实基态能量 $E_0$。
   - **核心提示**：把任意归一化试探态在哈密顿量本征基下展开证明精确期望 $\langle\psi|H|\psi\rangle\ge E_0$；再区分“数学精确期望”与“分项 Pauli 有限采样估计的统计涨落”，解释为何后者可偶然落到 $E_0$ 以下。
   - **完整分步演算**：设厄米哈密顿量 $H$ 的正交归一特征系为 $\{|E_k\rangle\}$，对应特征值按升序排列 $E_0 \le E_1 \le \cdots \le E_{d-1}$。把任意归一化态展开为 $|\psi(\boldsymbol\theta)\rangle = \sum_k d_k |E_k\rangle$（满足 $\sum_k |d_k|^2 = 1$）。用左共轭内积和正交性 $\langle E_j|E_k\rangle = \delta_{jk}$ 逐项计算精确能量期望：

     $$
     E(\boldsymbol\theta)
     = \langle\psi(\boldsymbol\theta)|H|\psi(\boldsymbol\theta)\rangle
     = \sum_{j,k} d_j^* d_k E_k \langle E_j|E_k\rangle
     = \sum_k |d_k|^2 E_k
     \ge E_0 \sum_k |d_k|^2 = E_0.
     $$

     该不等式只约束**同一哈密顿量模型的精确期望值**，既不保证浅层试探线路族一定包含真实基态 $|E_0\rangle$，也不保证经典优化器能避开局部极小或找到全局最优。反过来，实验中各不对易 Pauli 项是分批独立抽样测量的：例如在 $H = 0.7Z + 0.2X$ 的精确基态（$E_0 = -\sqrt{0.53} \approx -0.728$）上，分别测一次 $Z$ 和一次 $X$，有超过 $62\%$ 的概率同时读到 $-1$，拼出的样本估计为 $\widehat E = 0.7(-1) + 0.2(-1) = -0.9 < E_0$。此外，读出缓解或零噪声外推（ZNE）也可能引入偏置。
   - **结论与边界回验**：变分原理严格保证任何归一化态的精确能量期望 $E(\boldsymbol\theta) \ge E_0$，但不保证试探态表达力足够或优化器收敛到 $E_0$；有限次测量样本均值存在随机波动，叠加误差缓解偏置后完全可能偶然低于 $E_0$。
   - **易错坑提醒**：看到某次实机实验的 VQE 能量点估计比经典 FCI 基准还低，就以为“量子结果打破了变分原理或算得更准”；必须先检查误差棒、置信区间、误差缓解偏差以及两边哈密顿量截断是否一致。

2. **【计算】单边 MaxCut 的 $p = 1$ QAOA 期望割值 $\langle C\rangle$ 完整验证**

   - **题意与约定**：考察 $p = 1$ QAOA 的交替演化 $|\gamma, \beta\rangle = e^{-i\beta(X_1 + X_2)} e^{-i\gamma C}|++\rangle$。按计算基大端序 $|00\rangle, |01\rangle, |10\rangle, |11\rangle$ 逐振幅推演，拆开实部虚部求模平方。
   - **核心提示**：对单边割算符 $C=\frac{1}{2}(I-Z_1 Z_2)$ 与初态 $|++\rangle$，先算相位分离 $e^{-i\gamma C}|++\rangle$，再把混频器 $e^{-i\beta(X_1+X_2)}=R_x(2\beta)\otimes R_x(2\beta)$ 逐项作用（或在海森堡绘景共轭 $Z_1 Z_2$），最后求 $\langle C\rangle$。
   - **完整分步演算**：单边代价算符 $C = \frac{I - Z_1 Z_2}{2}$ 在 `01`、`10` 上取本征值 $1$，在 `00`、`11` 上取 $0$。
     1. **初态与代价层**：$|++\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$ 经 $e^{-i\gamma C}$ 作用后，只给 `01`、`10` 乘相位 $e^{-i\gamma}$：

        $$
        |\psi_C\rangle = \frac{1}{2}\left(|00\rangle + |11\rangle + e^{-i\gamma}|01\rangle + e^{-i\gamma}|10\rangle\right).
        $$

     2. **混合层展开**：记 $c = \cos\beta,\, s = \sin\beta$，因 $X_1, X_2$ 对易，两比特混合算符为 $(cI - isX_1)\otimes(cI - isX_2) = c^2 I - ics(X_1 + X_2) - s^2 X_1 X_2$。
     3. **汇总末态 $|01\rangle$ 的振幅 $A_{01}$**：四条输入分支跳到 $|01\rangle$ 的贡献依次为：$|00\rangle \to \frac{1}{2}(-ics)$、$|11\rangle \to \frac{1}{2}(-ics)$、$|01\rangle \to \frac{1}{2}e^{-i\gamma}c^2$、$|10\rangle \to \frac{1}{2}e^{-i\gamma}(-s^2)$。合并并用二倍角公式 $2cs = \sin(2\beta)$、$c^2 - s^2 = \cos(2\beta)$ 得：

        $$
        A_{01} = \frac{1}{2}\Bigl[-i\sin(2\beta) + e^{-i\gamma}\cos(2\beta)\Bigr]
        = \frac{1}{2}\Bigl[\cos\gamma\cos(2\beta) - i\bigl(\sin(2\beta) + \sin\gamma\cos(2\beta)\bigr)\Bigr].
        $$

     4. **取模平方求 $\langle C\rangle$**：实部平方加虚部平方（利用 $\cos^2\gamma + \sin^2\gamma = 1$ 与 $2\sin(2\beta)\cos(2\beta) = \sin(4\beta)$）：

        $$
        |A_{01}|^2 = \frac{1}{4}\Bigl[\cos^2(2\beta) + \sin^2(2\beta) + \sin(4\beta)\sin\gamma\Bigr]
        = \frac{1}{4}\bigl[1 + \sin(4\beta)\sin\gamma\bigr].
        $$

        由对称性 $A_{10} = A_{01}$，故期望割值 $\langle C\rangle = |A_{01}|^2 + |A_{10}|^2 = \frac{1}{2}[1 + \sin(4\beta)\sin\gamma]$。取 $\beta = \pi/8,\, \gamma = \pi/2$ 时得 $A_{01} = A_{10} = -i/\sqrt{2}$，概率各 $1/2$，$\langle C\rangle = 1$。
   - **结论与边界回验**：单边 $p = 1$ QAOA 的期望割值为 $\langle C\rangle = \frac{1}{2}[1 + \sin(4\beta)\sin\gamma]$，在 $\beta = \pi/8,\, \gamma = \pi/2$ 处取到全局最大值 $1$。
   - **易错坑提醒**：看到单边图上 $\langle C\rangle = 1$ 且每次都采到最优割，就误以为一般图上 QAOA 高期望值也保证每次采到最优解；在一般大图上，高期望值通常对应分布在众多次优解上的平均，须单独报告最优串命中概率。

3. **【进阶】参数化线路表达力越强，训练为何反而可能越困难**

   - **题意与约定**：考察变分线路中“表达力”与“可训练性”的根本权衡，以及动力李代数（DLA）贫瘠高原理论和有限采样噪声吞没梯度的机制。
   - **核心提示**：把参数化线路的表达力与高维希尔伯特空间测度集中联系起来：当线路逼近 Haar 随机或高维动力李代数（DLA）时，代价函数梯度方差如何随比特数 $n$ 指数衰减，以及有限采样噪声如何淹没信号。
   - **完整分步演算**：表达力强只说明线路输出覆盖的态空间范围广，却直接触发三类训练障碍：
     1. **贫瘠高原指数塌陷**：按 Ragone 等（2024）的动力李代数（DLA）统一理论，对无迹生成元构成的深参数化线路，当满足 $\rho \in i\mathfrak{g}$ 或 $O \in i\mathfrak{g}$ 时，损失函数与梯度的方差按 $1/\dim(\mathfrak{g})$ 缩放。若高表达力线路生成的李代数维数 $\dim(\mathfrak{g})$ 随比特数 $n$ 指数增长（如全 $\mathfrak{su}(2^n)$ 的维数 $4^n - 1$），梯度方差就会指数坍缩至零，整个景观沦为平坦高原。
     2. **采样噪声淹没真实下降方向**：假设两参数点的真实目标差仅为 $\Delta E = 0.01$，但每点有限次采样估计的标准差为 $\sigma = 0.02$，独立作差的标准差为 $\sqrt{0.02^2 + 0.02^2} = 0.02\sqrt{2} \approx 0.0283$，远超信号 $0.01$，优化器几乎在随机游走。
     3. **噪声与全局测量叠加**：硬件退极化噪声与全局投影观测量会进一步指数压扁梯度；反之，若强行把 $\dim(\mathfrak{g})$ 压到多项式级以恢复可训练性，又往往会把线路推回经典高效可模拟区间。
   - **结论与边界回验**：高表达力线路常伴随指数级 $\dim(\mathfrak{g})$，触发梯度指数消失的贫瘠高原，在有限采样噪声下无法分辨下降方向，导致训练反而远比受限结构线路困难。
   - **易错坑提醒**：把经典深度学习里“网络越深越宽越好训”的直觉照搬到量子变分线路，忽略量子态空间呈 $2^n$ 指数膨胀且梯度只能靠有限次测量估计、无法像经典反向传播那样廉价读出中间激活值。

4. **【基础】量子机器学习（QML）声明中数据装载为何是核心关卡**

   - **题意与约定**：考察 QML 端到端复杂度里的“输入/输出瓶颈”：振幅编码在形式上只需 $n = \log_2 N$ 个比特存 $N$ 个数，但制备任意量子态与读出结果的物理成本不能被静默豁免。
   - **核心提示**：区分“振幅编码只占 $\log_2 N$ 个比特”与“把 $N$ 个经典数据装载进量子态所需的门数下界”，再计入期望值估计所需的反复重复制备倍率。
   - **完整分步演算**：要把一段长度为 $N = 2^n$ 的任意无结构经典数据向量 $\vec{x} \in \mathbb{C}^N$ 精确装载为归一化振幅态 $|\psi_x\rangle = \frac{1}{\|\vec{x}\|}\sum_{j=0}^{N-1} x_j |j\rangle$，普通量子门电路一般需要 $\Theta(N)$ 个基本门（仅遍历并读入普通内存中的 $N$ 个数本身就需要 $\Omega(N)$ 时间）。即便寄希望于 QRAM，构建与维护含 $O(N)$ 个高相干路由节点的硬件及其容错机会成本同样是 $\Omega(N)$。此外，训练过程包含大量样本与多轮迭代，每次评估都因测量破坏量子态而必须重新制备输入态，总装载成本随之成倍累加。
     - **振幅装载复杂度定量拆解**：要把任意 $N = 2^n$ 维经典实向量装载成振幅编码态 $|\psi_x\rangle = \sum_{j=0}^{N-1} x_j |j\rangle$，在没有假设硬件级零开销 QRAM 的情况下，通用态制备电路至少需要 $\Omega(N)$ 个基础门；再乘以将最终期望值估计到误差 $\varepsilon$ 所需的 $O(1/\varepsilon^2)$ 次独立重复制备，端到端总门操作量至少为 $\Omega(N/\varepsilon^2)$——仅数据装载一项就已抵消许多宣称针对经典 $O(N)$ 算法的指数加速。
   - **结论与边界回验**：若量子方案把“数据已免费处于量子态”作为起点，却让经典算法自行承担 $\Omega(N)$ 的数据读入，比较就不公平；一旦计入实际数据装载与反复重复制备成本，许多声称的 QML 指数加速会被彻底抵消。
   - **易错坑提醒**：把“$n$ 比特可存 $2^n$ 个复振幅”等同于“能用 $O(\log_2 N)$ 时间把 $N$ 条经典数据读进量子计算机”。

5. **【基础】从“可行性演示”升级到“实用优势”至少还缺哪四类证据**

   - **题意与约定**：考察评估量子应用宣称的证据阶梯。小规模电路跑出非随机数字只验证了“能运行”，距离端到端实用优势还有四道必须补齐的硬门槛。
   - **核心提示**：按科研证据阶梯，从统计显著性与误差界、同预算最强经典基线、含 I/O 与调参的端到端墙钟成本以及可扩展趋势四个维度核查“实用优势”的硬门槛。
   - **完整分步演算**：升级为实用优势至少还须提供以下四类完整证据：
     1. **固定任务与可信误差标尺**：预先冻结具体问题定义、精度/容错标准与完整统计置信区间，核验结果确实可信且可独立复现；
     2. **强经典基线的同预算对比**：把当前最强、最匹配的经典算法（而非随机猜测或暴力穷举 $2^n$）放在可比的硬件、时间与能耗预算下同场实测；
     3. **端到端全账本开销**：完整计入数据装载、编译路由、误差缓解或纠错、重复采样、外层调参以及经典后处理的真实墙钟时间；
     4. **面向规模增长的趋势证据**：展示当问题规模 $n$ 持续放大时，量子方案在时间、能耗或精度上的优势能够站稳并扩大，而非仅在特定微调小实例上偶发胜出。
     - **端到端墙钟成本账本公式**：评判任何应用宣称是否跨过“实用优势”门槛，须对照端到端总解题时间账本：

       $$
       T_{\mathrm{total}} = T_{\mathrm{prep/compile}} + M_{\mathrm{shots}}\bigl(T_{\mathrm{circ}} + T_{\mathrm{meas}} + T_{\mathrm{reset}}\bigr) + T_{\mathrm{post}},
       $$

       并同步核查有限样本标准误 $\sigma \propto 1/\sqrt{M_{\mathrm{shots}}}$ 下的置信区间是否真正优于同预算、同误差口径的最强经典求解器。
   - **结论与边界回验**：至少还缺四类核心证据：固定任务与统计可信度验证、强经典算法同预算基线、涵盖输入输出与调参的端到端总成本账本、以及规模扩展趋势与独立复现。
   - **易错坑提醒**：把“量子线路在真机上跑通并优于纯随机输出”混写成“展示了实用量子优势”，或拿理论查询分离直接替代端到端墙钟对比。

6. **【基础】误差缓解（QEM）后的更准期望值为何不等同于受保护的逻辑量子比特**

   - **题意与约定**：考察近期误差缓解（QEM）与容错量子纠错（QEC）在保护对象、数学机制与资源随深度标度上的本质分水岭。
   - **核心提示**：比较 QEM 与 QEC 的作用对象（经典期望后处理 vs 保护物理/逻辑量子态）、能否接入后续深度线路，以及采样开销随线路深度的指数标度。
   - **完整分步演算**：QEM（如 ZNE、PEC）并不在电路执行期间监测或纠正量子态上的错误，而是通过多次带噪采样、外推或按准概率权重线性组合测量读数来估计最终的经典期望值 $\langle O\rangle$。它以“方差和采样开销暴涨”换取“偏差下降”：例如严格无偏的概率误差抵消（PEC），单层采样开销因子为 $\gamma_{\mathrm{PEC}} > 1$，经深度 $L$ 层电路后的样本放大倍数按指数爆炸：

     $$
     M_{\mathrm{PEC}} = \gamma_{\mathrm{PEC}}^{2L}.
     $$

     而且 QEM 结束时只交出一个经典期望数字，中途并不存在一个高保真、可继续输入下一段算法子程序的受保护量子态。相反，QEC 通过把逻辑信息编码进冗余物理比特、反复提取纠错症状并实时解码修正，在物理错误率低于阈值时，只需多项式增加码距 $d$ 就能使逻辑错误率呈指数下降，持续保护整个未知逻辑态。
     - **采样指数墙数值算例（第 8 章变分期望估算视角）**：以概率误差消除（PEC）为例，设单层电路的准概率 1-范数放大因子仅 $\gamma = 1.05$，要保持相同统计精度，所需采样数按 $\gamma^{2L}$ 膨胀：

       $$
       L = 100\text{ 层}:\ 1.05^{200} \approx 1.73 \times 10^{4}\text{ 倍},
       \qquad
       L = 500\text{ 层}:\ 1.05^{1000} \approx 1.55 \times 10^{21}\text{ 倍}.
       $$

       这清楚表明 QEM 只能在浅至中等深度抢救经典期望值，无法跨越深电路指数墙（与[第 10 章第 8 题](#第-10-章)的容错阈值下指数压错标度形成鲜明镜像对照）。
   - **结论与边界回验**：QEM 只修正最终经典期望统计且采样代价随电路深度呈指数墙（如 $\gamma_{\mathrm{PEC}}^{2L}$）；QEC 才是通过冗余编码和纠错症状循环在阈值下持续保护逻辑量子态的可扩展方案，两者不可混为一谈。
   - **易错坑提醒**：看到一篇 QEM 论文把某观测量的估计误差从 $15\%$ 压低到 $1\%$，就误以为该芯片已经等价于运行了高保真容错逻辑比特。

7. **【进阶】“量子核难以经典精确模拟”为何不能自动推出预测优势**

   - **题意与约定**：考察机器学习里的“特征映射模拟困难”与“监督学习泛化预测优势”之间的逻辑断层（对应 Huang 等 2021 的数据力量定理）。
   - **核心提示**：区分“从头模拟量子态输出分布很难”与“在已有带标签训练数据的监督学习任务中泛化得更好”这两个截然不同的计算问题（参考数据力量与经典核几何差异）。
   - **完整分步演算**：量子核方法用电路制备特征态 $|\phi(\mathbf{x})\rangle$ 并估计内积 $K(\mathbf{x}, \mathbf{x}') = |\langle\phi(\mathbf{x})|\phi(\mathbf{x}')\rangle|^2$。哪怕从第一性原理经典精确计算整条特征线路的完整态矢量属于经典困难问题，也无法自动推出分类/回归预测优势，原因有三：第一，学习任务的目标是利用有限个带标签训练样本 $\{(\mathbf{x}_i, y_i)\}$ 对测试集做出准确预测，经典学习器可以直接从训练数据中学习输入到标签的规律（数据本身提供了额外计算资源），完全不必去模拟量子态；第二，过于复杂、难以模拟的深量子特征映射往往触发核值指数集中（所有不同样本的核值趋向同一常数），反而丧失区分力；第三，真正要确立预测优势，必须在明确的训练/测试分布上用调优后的强经典模型检验测试集泛化误差，并把量子核估计的全部采样预算算进去。
     - **数据力量（Power of Data）定量判据**：按 Huang 等（2021）建立的经典—量子核几何差异 $g_{CQ} = \sqrt{\|\sqrt{K_Q}\,K_C^{-1}\sqrt{K_Q}\|_\infty}$，即使量子核矩阵元素 $K_Q(x, x') = |\langle\phi(x)|\phi(x')\rangle|^2$ 自身难以从头经典精确模拟，只要利用带标签训练集估算出的 $g_{CQ}$ 不随系统规模显著大于 $\sqrt{N_{\mathrm{train}}}$（例如特征映射过于表达力强导致核矩阵指数集中于单位阵附近），经典核机器凭借训练数据本身就能达到相近的泛化预测误差。
   - **结论与边界回验**：经典难以精确模拟某个量子态，只说明“态模拟任务”困难，不代表“从带标签数据做预测”也一定需要量子计算机；必须凭公开数据集、严格测试集泛化误差与强经典基线证明预测优势。
   - **易错坑提醒**：把“希尔伯特空间维度 $2^n$ 很大”或“特征线路不可经典模拟”直接当成量子机器学习优于经典深度学习或核支持向量机的充分证明。

8. **【计算】核值差异缩小 $4$ 倍时的采样开销倍数计算**

   - **题意与约定**：考察独立有界采样下样本数 $S$ 与目标统计分辨率 $\delta$ 之间的反平方标度关系 $S \propto 1/\delta^2$。先求出信号差异缩小的倍数，再平方得出样本需求倍数，并交代分布前提。
   - **核心提示**：利用有界独立抽样的方差关系 $\sigma\propto 1/\sqrt{S}$（即所需样本数 $S\propto 1/\delta^2$），先求出信号分辨间隔 $\delta$ 缩小的倍数，再据此推算采样次数倍率。
   - **完整分步演算**：原有用差异为 $\delta_1 = \frac{1}{16}$，缩小后为 $\delta_2 = \frac{1}{64}$，缩小倍数为：

     $$
     \frac{\delta_1}{\delta_2} = \frac{1/16}{1/64} = 4.
     $$

     在相同的独立有界读数方差上界模型（例如 Hoeffding 界或最坏方差上界 $\sigma_{\max}^2$ 固定不变）下，要以同等置信度分辨间距 $\delta$，所需重复测量次数满足 $S \propto \sigma_{\max}^2 / \delta^2$，因此新旧样本数之比为：

     $$
     \frac{S_2}{S_1} = \left(\frac{\delta_1}{\delta_2}\right)^2 = 4^2 = 16.
     $$

   - **结论与边界回验**：在相同最坏方差上界与置信度前提下，有用差异缩小 $4$ 倍会使重复测量次数增至原来的约 $16$ 倍。
   - **易错坑提醒**：线性直觉误以为“信号变小 $4$ 倍、采样多跑 $4$ 倍就够”；统计标准差按 $1/\sqrt{S}$ 下降，分辨力每提高 $k$ 倍，采样成本都要翻 $k^2$ 倍——这也是量子核指数集中一旦发生便迅速撞上采样墙的原因（实际常数还会受具体分布方差及同时估计多对核元素的多重检验校正影响）。

9. **【计算】$H = 0.7Z + 0.2X$ 的特殊角能量与精确基态能量计算**

   - **题意与约定**：考察单比特 VQE 试探态 $|\psi(\theta)\rangle = R_y(\theta)|0\rangle = \cos\frac{\theta}{2}|0\rangle + \sin\frac{\theta}{2}|1\rangle$ 的能量计算，以及利用 Pauli 反对易关系计算 $H^2$ 直接求精确特征值的技巧。
   - **核心提示**：将 $|\psi(\theta)\rangle=R_y(\theta)|0\rangle$ 代入 $\langle Z\rangle=\cos\theta$、$\langle X\rangle=\sin\theta$ 计算特殊角能量；求精确基态时直接展开 $H^2=(aZ+bX)^2$ 利用 $XZ+ZX=0$ 读出本征值模长。
   - **完整分步演算**：
     1. **计算 $\theta = 0$**：此时 $|\psi(0)\rangle = |0\rangle$，$\langle Z\rangle = 1,\, \langle X\rangle = 0$，故：

        $$
        E(0) = 0.7(1) + 0.2(0) = 0.7.
        $$

     2. **计算 $\theta = \pi/2$**：此时 $|\psi(\pi/2)\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) = |+\rangle$，$\langle Z\rangle = 0,\, \langle X\rangle = 1$，故：

        $$
        E\!\left(\frac{\pi}{2}\right) = 0.7(0) + 0.2(1) = 0.2.
        $$

     3. **用 $H^2$ 求精确特征值**：利用 $Z^2 = X^2 = I$ 与反对易关系 $ZX + XZ = 0$ 展开：

        $$
        H^2 = (0.7Z + 0.2X)^2 = 0.49 Z^2 + 0.04 X^2 + 0.14(ZX + XZ) = 0.53 I.
        $$

        因而 $H$ 的两个特征值平方均为 $0.53$，即 $\pm\sqrt{0.53}$；再查迹 $\operatorname{Tr}(H) = 0.7\operatorname{Tr}(Z) + 0.2\operatorname{Tr}(X) = 0$，确认两特征值一正一负，故精确基态能量为：

        $$
        E_0 = -\sqrt{0.53} \approx -0.728011.
        $$

        （按 $E(\theta) = 0.7\cos\theta + 0.2\sin\theta = \sqrt{0.53}\cos(\theta - \arctan(2/7))$，真正最优角落在 $\theta^* = \arctan(2/7) + \pi \approx 3.4199\,\mathrm{rad}$。）
   - **结论与边界回验**：$E(0) = 0.7$，$E(\pi/2) = 0.2$，精确最低能量为 $E_0 = -\sqrt{0.53} \approx -0.728$。仅在两三个离散参数点里挑最低值 $0.2$，连负值区都没进去，远不能代表全局最优。
   - **易错坑提醒**：算出 $H^2 = 0.53I$ 后忘记核对 $\operatorname{Tr}(H) = 0$ 来排除两个特征值同号（都是 $+\sqrt{0.53}$ 或都是 $-\sqrt{0.53}$）的可能；同时不要把少量试探点里的最小值当成已收敛的基态能量。

10. **【计算】$\theta = 0$ 试探态各测 $100$ 次 $Z$ 与 $X$ 的预期计数与理论能量**

    - **题意与约定**：考察不同测量基下量子态的测量概率与有限样本二项分布的期望与波动。把 $|\psi(0)\rangle = |0\rangle$ 分别在 $Z$ 基和 $X$ 基展开，求单次概率再乘以测量次数 $N = 100$。
    - **核心提示**：先将试探态 $|\psi(0)\rangle=|0\rangle$ 分别在 $Z$ 基与 $X$ 基展开算出单次测得 $+1/-1$ 的概率，再乘以 $100$ 得预期计数，并按线性组合 $0.7\langle Z\rangle+0.2\langle X\rangle$ 核算理论能量。
    - **完整分步演算**：
      - **$Z$ 基测量（$100$ 次）**：$|0\rangle$ 是 $Z$ 的 $+1$ 本征态，$P(Z=+1) = |\langle 0|0\rangle|^2 = 1$、$P(Z=-1) = 0$。因此在理想无噪下，$100$ 次测量预期得到 **$100$ 次 $+1$、$0$ 次 $-1$**，$\langle Z\rangle = +1$。
      - **$X$ 基测量（$100$ 次）**：将 $|0\rangle$ 写成 $\frac{|+\rangle + |-\rangle}{\sqrt{2}}$，得 $P(X=+1) = |\langle +|0\rangle|^2 = \frac{1}{2}$、$P(X=-1) = |\langle -|0\rangle|^2 = \frac{1}{2}$。$100$ 次独立测量的预期计数为 **$50$ 次 $+1$、$50$ 次 $-1$**（但单批 $+1$ 计数服从二项分布 $B(100, 1/2)$，标准差为 $\sqrt{100 \times 0.5 \times 0.5} = 5$ 次），理论期望 $\langle X\rangle = 0$。
      - **理论能量**：$E(0) = 0.7\langle Z\rangle + 0.2\langle X\rangle = 0.7(1) + 0.2(0) = 0.7$。
    - **结论与边界回验**：$Z$ 基预期为 $100$ 次 $+1$、$0$ 次 $-1$；$X$ 基预期为 $50$ 次 $+1$、$50$ 次 $-1$；理论能量为 $0.7$。因为 $X$ 测量具有本征量子随机性（计数标准差达 $5$ 次），单批实测很可能出现 $47/53$ 或 $54/46$，不能把“预期计数”当成每批必得的确定结果。
    - **易错坑提醒**：误以为理想量子芯片测 $|0\rangle$ 的 $X$ 分量就该每次精确输出 $50$ 个 $+1$ 和 $50$ 个 $-1$，把理论期望值与单次有限批次样本频率混为一谈。

11. **【计算】两项目 QUBO 枚举验证与 Pauli-$Z$ / 退火 Ising 哈密顿量核对**

    - **题意与约定**：考察二元约束优化向 Pauli-$Z$ 哈密顿量的代数翻译（$x_i = \frac{I - Z_i}{2}$）以及与第 17 章量子退火自旋约定（$s_i = 2x_i - 1 = -z_i$）的跨章符号桥。
    - **核心提示**：先将 $00,01,10,11$ 逐一代入原 QUBO 函数 $F(x_1,x_2)$ 列表；再用替换 $x_i=(I-Z_i)/2$ 检验对角哈密顿量 $H_F$ 在各基态上的本征值，并注意自旋约定 $s_i=2x_i-1=-z_i$ 的负号差异。
    - **完整分步演算**：
      1. **逐项代入 $F(x_1, x_2) = -3x_1 - 2x_2 + 4x_1 x_2$**：
         - $(0, 0)$：$F(0, 0) = 0 - 0 + 0 = 0$（合法）；
         - $(1, 0)$：$F(1, 0) = -3(1) - 0 + 0 = -3$（合法，全局最优）；
         - $(0, 1)$：$F(0, 1) = 0 - 2(1) + 0 = -2$（合法）；
         - $(1, 1)$：$F(1, 1) = -3(1) - 2(1) + 4(1)(1) = -1$（违背 $x_1 + x_2 \le 1$，被罚后高于合法最优 $-3$）。
      2. **核对门线路 Pauli-$Z$ 哈密顿量 $H_F = -\frac{3}{2}I + \frac{1}{2}Z_1 + Z_1 Z_2$ 在 $|10\rangle$ 上的值**：在大端序下，$|10\rangle$ 对应 $x_1 = 1,\, x_2 = 0$，由 $z_i = 1 - 2x_i$ 得 $Z_1|10\rangle = -|10\rangle$、$Z_2|10\rangle = +|10\rangle$，故 $Z_1 Z_2|10\rangle = (-1)(+1)|10\rangle = -|10\rangle$。逐项代入：

         $$
         \langle 10|H_F|10\rangle = -\frac{3}{2} + \frac{1}{2}(-1) + (-1) = -\frac{3}{2} - \frac{1}{2} - 1 = -3 = F(1, 0).
         $$

      3. **跨章自旋符号对照**：在量子退火库常用的自旋约定 $s_i = 2x_i - 1 = -z_i$ 下，同一目标写为 $F = -\frac{3}{2} - \frac{1}{2}s_1 + s_1 s_2$（一阶局域场反号、二阶耦合项因 $(-z_1)(-z_2) = z_1 z_2$ 保持同号）。
    - **结论与边界回验**：四个比特串的 $F$ 依次为 $0, -3, -2, -1$，最低点在合法方案 $(1, 0)$；$H_F$ 在 $|10\rangle$ 上精确给出 $-3$，完全吻合。
    - **易错坑提醒**：把 QUBO 翻译成哈密顿量只完成了问题编码，并没有替我们解出最优解；此外在门线路（$z_i = 1 - 2x_i$）与退火软件（$s_i = 2x_i - 1$）间移植系数时若忘记把一阶场系数取反，会把最优解整个翻转。

12. **【计算】二值收益 $p = 1/4$ 经典采样次数计算与 QAE 实现前提**

    - **题意与约定**：考察独立伯努利抽样的标准差公式 $\sigma_{\hat p} = \sqrt{p(1-p)/N}$，反解样本量下界 $N$，再对照量子幅度估计（QAE）$O(1/\epsilon)$ 查询优势背后的硬件与电路前提。
    - **核心提示**：套用伯努利样本频率标准差公式 $\sigma_{\hat p}=\sqrt{p(1-p)/N}\le 0.01$ 反解经典最小样本量 $N$；第二问列出把 QAE 二次查询加速兑现为实际加速所需的状态制备、相干深度与反射开销前提。
    - **完整分步演算**：单次 0/1 收益服从伯努利分布 $\mathrm{Bernoulli}(p)$，代入 $p = 1/4$ 得单次方差：

      $$
      \operatorname{Var}(X) = p(1 - p) = \frac{1}{4}\times\frac{3}{4} = \frac{3}{16} = 0.1875.
      $$

      $N$ 次独立采样的样本频率 $\hat p$ 标准差为 $\sigma_{\hat p} = \sqrt{\frac{3}{16N}}$。令其不超过 $0.01 = 10^{-2}$，两边平方求解：

      $$
      \frac{3}{16N} \le 10^{-4}
      \iff N \ge \frac{3}{16 \times 10^{-4}} = \frac{30000}{16} = 1875.
      $$

      回验：当 $N = 1875$ 时，$\sigma_{\hat p} = \sqrt{3 / 30000} = \sqrt{10^{-4}} = 0.01$，精确达标。注意这仅是 $1\sigma$ 标准差要求，若需 $95\%$ 置信区间半宽 $\le 0.01$，样本量还需乘约 $1.96^2 \approx 3.84$ 倍。
    - **结论与边界回验**：经典独立采样至少需要 $N = 1{,}875$ 次才能将样本频率标准差压至 $0.01$；QAE 的 $O(1/\epsilon)$ 查询优势前提是能够相干、可逆地实现概率分布装载 $A$、逆操作 $A^\dagger$ 及收益判别预言机，且端到端必须计入逻辑门深度、容错纠错开销与强经典方差缩减/准蒙特卡洛基线。
    - **易错坑提醒**：把 $1\sigma$ 标准差 $0.01$ 误当成“误差绝不超过 $0.01$”，或把 QAE 在抽象查询模型下的平方加速直接当成近期含噪设备上已落地的金融定价加速。

13. **【基础】相对能量差与保守总误差界计算**

    - **题意与约定**：考察量子化学中相对能量差 $\Delta E = E_B - E_A$ 的误差合成。区分“统计估计误差”与“模型截断误差”，并用三角不等式给出未证明误差抵消前的保守上界。
    - **核心提示**：先算能量差 $\Delta E=E_B-E_A$，再用三角不等式 $|\delta(E_B-E_A)|\le|\delta E_B|+|\delta E_A|$ 给出未证明误差相消时的保守总误差界，并区分统计误差与截断系统误差。
    - **完整分步演算**：
      1. **计算能量差估计值**：

         $$
         \widehat{\Delta E} = E_B - E_A = (-1.60) - (-1.72) = +0.12\,\mathrm{eV}.
         $$

      2. **单点保守误差上界**：对 $E_A$ 和 $E_B$，各自存在估计误差界 $0.01\,\mathrm{eV}$ 与模型误差界 $0.03\,\mathrm{eV}$，单点最坏总误差不超过 $0.01 + 0.03 = 0.04\,\mathrm{eV}$。
      3. **差值保守总误差界**：由三角不等式 $|\delta(\Delta E)| = |\delta E_B - \delta E_A| \le |\delta E_B| + |\delta E_A|$：

         $$
         \Delta_{\text{保守}} = 0.04\,\mathrm{eV} + 0.04\,\mathrm{eV} = 0.08\,\mathrm{eV}.
         $$

      比较目标精度：$0.08\,\mathrm{eV} > 0.02\,\mathrm{eV}$，超出目标整整 $4$ 倍。
    - **结论与边界回验**：能量差为 $0.12\,\mathrm{eV}$，保守总误差界为 $0.08\,\mathrm{eV}$，**不能**满足 $0.02\,\mathrm{eV}$ 的目标精度要求。
    - **易错坑提醒**：想当然地假设两个几何构型的模型系统误差会“大部分自动相消”，或者直接把系统模型误差当成独立随机变量做平方和开根号。在没有独立证据证明系统偏差同向抵消之前，必须采用三角不等式保守上界。

14. **【基础】2026 年特定物理观测量优势预印本为何不能推出一般 VQE/QAOA 实用优势**

    - **题意与约定**：考察科研证据的分层与外推边界，严格从题目要求的三个维度——任务类型、证据阶段、经典基线——拆解为何特化多体实验不能外推为通用变分算法的商业/实用优势。
    - **核心提示**：严格沿题目要求的“任务类型（专用多体观测量 vs 通用优化/化学）”“证据阶段（预印本 vs 长期独立复现）”与“经典基线（前沿张量网络/Pauli 传播）”三条线逐项拆解外推缺口。
    - **完整分步演算**：
      1. **任务维度不同**：2026 年的相关预印本聚焦于精心构造的特定困难线路采样（如掺杂 Clifford 线路）或定制多体物理观测量演化，不需要做大规模高维变分寻参或任意经典数据装载；而一般分子基态（VQE）、商业约束优化（QAOA）与机器学习任务涉及截然不同的哈密顿量结构、测量路障与优化景观。
      2. **证据阶段不同**：预印本与厂商公告仍处于同行评审与独立第三方复现之前，其噪声假设、截断标准与系统误差尚待学术共同体严格检验，不能按定论引用。
      3. **经典基线动态演进**：少数几种经典模拟器在某个规模不收敛，不代表所有经典算法都束手无策——例如 2026 年 8 月 Manabe–Gu–Pan 的经典张量网络预印本利用一维砖墙结构把单比特 $T$ 门吸收进相邻双比特张量而不增加收缩宽度，在多 GPU 上精准复算了前述掺杂 Clifford 采样实验的全部公开批次振幅，既独立验证了硬件保真度，也把该拓扑拉回了经典精确模拟区间。
    - **结论与边界回验**：由于任务结构、同行评审证据阶段与经典基线演进三方面都存在本质鸿沟，特定多体物理观测量的预印本结果即便可信，也绝不能外推为一般 VQE 或 QAOA 的实用优势证明。
    - **易错坑提醒**：把“某台量子机在一个专为它设计的物理基准上跑赢了当前某一经典模拟器”偷换概念成“量子变分算法已经在化工、金融或物流优化上全面超越经典计算”。

15. **【计算】两点线性零噪声外推（ZNE）零点值与方差放大计算**

    - **题意与约定**：考察 ZNE“用方差换偏差”的定量代价。由线性噪声模型 $E(c) = E(0) + a c$ 联立两个噪声倍增点 $\lambda$ 与 $2\lambda$ 消去斜率 $a$，再用独立随机变量线性组合方差公式 $\operatorname{Var}(\alpha X + \beta Y) = \alpha^2\operatorname{Var}(X) + \beta^2\operatorname{Var}(Y)$ 求外推方差。
    - **核心提示**：在两点线性噪声模型 $E(c)=E(0)+ac$ 下联立 $c=\lambda$ 与 $c=2\lambda$ 消去斜率 $a$ 写出零噪声线性组合系数 $(w_1,w_2)$，再按独立方差线性叠加公式 $\mathrm{Var}(w_1\widehat E_1+w_2\widehat E_2)=(w_1^2+w_2^2)\sigma^2$ 求方差倍率。
    - **完整分步演算**：
      1. **线性外推到零噪声**：列方程 $\widehat E(\lambda) = \widehat E(0) + a\lambda$ 与 $\widehat E(2\lambda) = \widehat E(0) + 2a\lambda$。用第一式的 $2$ 倍减去第二式消去 $a\lambda$：

         $$
         \widehat E(0) = 2\widehat E(\lambda) - \widehat E(2\lambda)
         = 2(-0.60) - (-0.55) = -1.20 + 0.55 = -0.65.
         $$

      2. **计算外推方差与标准差**：设两噪声点独立测量且方差均为 $v$，则线性组合 $2\widehat E(\lambda) - 1\cdot\widehat E(2\lambda)$ 的方差为：

         $$
         \operatorname{Var}\bigl(\widehat E(0)\bigr) = 2^2 \operatorname{Var}\bigl(\widehat E(\lambda)\bigr) + (-1)^2 \operatorname{Var}\bigl(\widehat E(2\lambda)\bigr) = 4v + v = 5v,
         $$

         标准差放大至原单点标准差的 $\sqrt{5} \approx 2.236$ 倍（要维持与原单点相同的标准差，总采样数需成倍增加）。
    - **结论与边界回验**：线性外推的零噪声估计值为 $\widehat E(0) = -0.65$；外推估计的方差放大为 $5v$（标准差为原来的 $\sqrt{5}$ 倍）。
    - **易错坑提醒**：误把减法当成“方差也相减”（错算成 $4v - v = 3v$）；独立误差的方差只会按系数平方相加。同时别忘了：如果真实噪声衰减是指数而非线性的，线性外推还会留下系统模型偏差，且外推数值本身不保证满足物理范围 $[-1, 1]$ 或变分下界 $E_0$。

## 第 9 章

> 对应章节：《09｜主流硬件平台与物理噪声特性》

1. **【基础】为何不能仅凭量子比特数横向比较超导处理器与中性原子阵列**

   - **题意与约定**：考察硬件平台的多维工程权衡（DiVincenzo 准则与全栈指标口径）。超导芯片与中性原子阵列在门时长、连通性、并行度、时钟频率和主要失效模式上横跨数个数量级，单一“物理比特数”无法代表同等计算能力。
   - **核心提示**：从门时长、连接拓扑、并行搬运能力、双比特门错误率与泄漏/丢原子等失效模式对比超导与中性原子，说明单一物理比特计数为何抹平了跨数量级的系统差异。
   - **完整分步演算**：对比两大平台的核心运行参数即可看出端倪：
     - **门速度与纠错周期**：超导双比特门仅需 $20\text{--}100\,\mathrm{ns}$（整轮纠错周期约 $1.1\,\mu\mathrm{s}$）；中性原子 Rydberg 双比特门约 $200\text{--}300\,\mathrm{ns}$，但包含光镊原子搬运、重排与荧光成像的完整循环通常落在毫秒级，时钟慢数个量级。
     - **连通性与拓扑重构**：超导芯片多为固定二维近邻连接，远距耦合须插 `SWAP` 路由；中性原子阵列可借助声光偏转器（AOD）动态搬运实现可重构连接与整块横向门。
     - **主要失效与统计口径**：超导芯片主要受 $T_1/T_2$、串扰与 $|2\rangle$ 态泄漏制约；中性原子阵列需同时核算光镊装载率、原子逃逸丢失（可转化为擦除标记）与连续补原子开销。例如 Caltech 6,100 原子阵列展示的是静态装载与长相干存储能力，不能直接等同于 6,100 个高速全并行纠错比特。
   - **结论与边界回验**：评价不同硬件平台必须在同一目标任务下并行核对物理比特数、并行双比特门保真度、拓扑连通性、相干与门时长比值 $T_2 / t_{2Q}$、读出复位速度、泄漏/丢失率以及实际能支撑的逻辑比特质量，不能单凭物理比特数比大小。
   - **易错坑提醒**：看到“某中性原子阵列达到数千比特、某超导芯片仅一百多比特”就断定前者算力领先几十倍，忽略了时钟速度、有效门层吞吐、动态搬运延迟与是否真正实现低于阈值纠错等关键维度。

2. **【基础】$T_1$、$T_2^*$、门错误率与 SPAM 各测量什么物理环节**

   - **题意与约定**：考察硬件表征中四个最常被混用的基础指标。逐一对应它们的物理过程、标准实验协议与噪声来源，明确为何它们不可互相替代。
   - **核心提示**：按“能量弛豫、自由进动失相干、门操作保真度、初态制备与测量误差”四类物理过程逐一匹配 $T_1$、$T_2^*$、门错误率与 SPAM。
   - **完整分步演算**：
     - **$T_1$（能量弛豫时间）**：测量激发态 $|1\rangle$ 向基态 $|0\rangle$ 耗散能量的特征时间。通过反转恢复实验（先施加 $X_\pi$ 准备 $|1\rangle$，空闲等待时间 $t$ 后测 $Z$ 基，拟合 $P_1(t) = A e^{-t/T_1} + B$）测得。
     - **$T_2^*$（自由演化有效退相位时间）**：测量叠加态在无回波保护下的相对相位保持时间，包含能量弛豫 $T_1$ 与静态/慢漂移引起的非均匀展宽。通过 Ramsey 干涉实验（$R_y(\pi/2) \to \tau \to R_y(-\pi/2) \to M_Z$）测得，通常远短于加自旋回波或动态解耦后的 $T_2$。
     - **门错误率（Gate Error Rate）**：测量实际施加单比特或双比特控制门偏离理想酉操作的程度（如随机基准测试 RB 测得的平均门错误率 $r = 1 - F_{\mathrm{avg}}$），综合反映相干脉冲失准、驱动噪声、串扰、$|2\rangle$ 泄漏及门期间的退相干。
     - **SPAM 误差（State Preparation and Measurement Error）**：测量初始化制备初态与终端读出判决两端的合并失真（如热激发残留、读出中途 $|1\rangle\to|0\rangle$ 弛豫与 $I\text{-}Q$ 信号重叠判错）。
   - **结论与边界回验**：$T_1$ 刻画空闲能量衰减，$T_2^*$ 刻画含慢漂移的自由退相位，门错误率刻画控制操作本身的偏差，SPAM 刻画电路首尾制备与读出的失真；四者对应完全不同的物理与实验环节，必须分别报告。
   - **易错坑提醒**：用空闲 $T_1$ 估算门保真度（忽略脉冲失准与串扰），或拿单门错误率推算整条电路成功率却忘了把往往高出一个量级的 SPAM 误差单列核算。

3. **【基础】光子门的条件保真度为何必须和损耗、接受率一起报告**

   - **题意与约定**：考察光子量子计算中的概率性门操作与后选择分母问题。线性光学纠缠/融合门依赖光子不可区分干涉与探测反作用，一旦丢光子就被后选择剔除，单独报“保留下来的成功事件有多准”会严重掩盖真实产率。
   - **核心提示**：区分“只在幸存事件子集上统计的条件保真度”与“端到端光子全到达的接受率 $p_{\mathrm{acc}}$”，思考多光子链路上透射率 $\eta^m$ 如何导致有效事件率 $R_{\mathrm{eff}}=f_{\mathrm{rep}}p_{\mathrm{acc}}$ 指数坍塌。
   - **完整分步演算**：在光子平台中，端到端链路存在单光子源效率、波导/光纤传输、开关插损与探测器效率等多重损耗。设单次实验成功触发有效先兆（或全部光子均被探测到）的**接受率**为 $p_{\mathrm{acc}}$，原始时钟重复率为 $f_{\mathrm{rep}}$，则单位时间真正交付的有效事件率（有效吞吐）为：

     $$
     R_{\mathrm{eff}} = f_{\mathrm{rep}} \cdot p_{\mathrm{acc}}.
     $$

     **条件保真度**只在“已经通过筛选、成功被探测到”的那一小部分子集（占比 $p_{\mathrm{acc}}$）上统计，分子分母把所有丢光子的失败轮次全部扔掉了。如果某次实验条件保真度高达 $99\%$，但损耗巨大导致 $p_{\mathrm{acc}} = 10^{-6}$，那么每百万次尝试才有一次有效输出，实际算法根本无法按所需速率推进。
     - **光学平台损耗标度算例（第 9 章物理层侧重）**：设单光子从产生、波导路由到探测的端到端总透过率为 $\eta = 0.5$（对应约 $3\ \mathrm{dB}$ 总损耗），若某概率门或融合操作需要 $m$ 个光子同时到达才能通过先兆筛选，则理想接受率随光子数指数衰减：

       $$
       p_{\mathrm{acc}}(m) \approx \eta^m = 0.5^m
       \quad\Longrightarrow\quad
       p_{\mathrm{acc}}(6) = \frac{1}{64} \approx 1.56\%,
       \qquad
       p_{\mathrm{acc}}(10) = \frac{1}{1024} \approx 0.098\%.
       $$

       因此光学实验必须把条件保真度与端到端损耗、接受率一并汇报（系统吞吐与置信区间宽度放大见[第 11 章第 3 题](#第-11-章)，科研论文审稿清单见[第 15 章第 6 题](#第-15-章)）。
   - **结论与边界回验**：条件保真度只描述“幸存子集”的质量，无法反映光路损耗带来的指数级产率坍塌；严谨的光学实验报告必须将条件保真度与端到端损耗、接受率、先兆判据、重复率及每秒有效成功事件数捆绑披露。
   - **易错坑提醒**：拿光子实验的“条件门保真度 $99.5\%$”直接和超导或离子阱的“确定性门保真度 $99.5\%$”做对等比较，忘记检查背后是否藏着极低的后选择接受率。

4. **【基础】“离子全连接”与“拓扑保护”各自必须附加哪些限定条件**

   - **题意与约定**：考察硬件科普中两个最易被过度简化的标签。逐一拆解它们的真实物理实现边界与尚未解决的工程瓶颈。
   - **核心提示**：分别思考离子阱“单阱全连接”在离子数增多后遇到的声子谱拥挤与 QCCD 分区搬运瓶颈，以及拓扑量子比特对能隙保护前提、非阿贝尔编织实证与非 Clifford 门补充的依赖。
   - **完整分步演算**：
     - **“离子全连接”的限定**：在单条短离子链中，任意一对离子确实可以借助共享集体振动模实现直接双比特门（MS 门），在图论拓扑上呈全连接；但第一，这**不代表所有离子对可以零代价同时并发执行纠缠门**，因为多门共享同一振动模池会互相干扰；第二，离子数增加到几十颗以上时，振动谱变得极度拥挤（模拥挤）且串扰加剧，工程上必须转向 QCCD 分区架构（如 Quantinuum Helios），靠电极搬运和协同冷却把不同区间的离子凑到一起——因此逻辑上虽全连接，却要支付毫秒级搬运时间、加热与门区并行度限制。
     - **“拓扑保护”的限定**：理论上非局域 Majorana 零模对局域微扰具有随纳米线长度按 $e^{-L/\xi}$ 指数抑制的退相干保护；但第一，实验上必须逐级跨越证据阶梯，严格排除平庸 Andreev 束缚态（ABS）伪装，并拿出错误率随长度 $L$ 指数下降的直接实测证据；第二，即使在理想 Ising/Majorana 拓扑模型中，编织仅生成有限的 Clifford 门群，**通用计算必需的非 Clifford $T$ 门不受拓扑保护**，仍需魔法态注入与蒸馏；第三，控制、宇称读出与游离电子引发的**准粒子中毒**同样不在被动拓扑保护之内，宏观容错机仍须叠加主动纠错码。
   - **结论与边界回验**：“离子全连接”须限定链长规模、并行度以及 QCCD 搬运与冷却的时间代价；“拓扑保护”须限定在经证实的体能隙拓扑相与 Clifford 编织范围内，不自动覆盖非 Clifford 门、读出控制误差与准粒子中毒。
   - **易错坑提醒**：把“逻辑拓扑全连接”误解为“全芯片无开销无限并发”，或把“拓扑保护”误解为“造出拓扑比特就不再需要量子纠错和魔法态蒸馏”。

5. **【基础】SWAP 路由与经典反馈延迟如何改变抽象线路的实际成本**

   - **题意与约定**：考察硬件物理约束如何向上传导到编译深度、总门数与相干预算。分别从空间维度（缺乏直连边）与时间维度（中途测量+条件操作）拆解实际成本膨胀。
   - **核心提示**：从空间（近邻连接图插入 SWAP 令门数和深度倍增）与时间（中途测量、经典通信与实时解码等待期间的相干衰减）两条轴拆解抽象电路到物理执行的成本膨胀。
   - **完整分步演算**：
     - **空间维度的 SWAP 路由成本**：教科书抽象电路假设任意两比特可直接做双比特门。落到二维近邻或重六角拓扑的实体芯片时，若两比特相距 $k$ 条边，编译器必须在芯片上插入一连串 `SWAP` 门把它们搬到相邻位置（必要时还要换回）。每个 `SWAP` 门在常见原生门集下需拆成 $3$ 个 `CNOT`（或等效 `CZ` + 单门），于是原本 $1$ 个抽象双比特门瞬间膨胀为 $3(k-1)+1$（单程）甚至 $6(k-1)+1$（往返）个物理双比特门——不仅门数和电路深度成倍攀升，还会同步放大累积门误差与空闲比特的退相干暴露时间。
     - **时间维度的经典反馈延迟成本**：在动态电路（如隐形传态前馈、主动复位）和实时量子纠错中，需要执行“中途测量 $\to$ 信号解调判别 $\to$ 经典电子学传输与解码决策 $\to$ 下发条件校正脉冲”。在这段经典反馈延迟 $\tau_{\mathrm{fb}}$ 期间，芯片上所有未测量的活量子比特只能原地空闲等待，持续承受 $T_1$ 弛豫与 $T_2$ 退相位；若 $\tau_{\mathrm{fb}}$ 逼近甚至超过相干时间或纠错周期，活比特还没等到指令就已退相干失真，还会触发实时解码积压。
   - **结论与边界回验**：SWAP 路由以倍增双比特门数与深度为代价弥补拓扑缺边，大幅拉高累计误差；经典反馈延迟则把通信与实时解码耗时直接转化为活比特的空闲退相干损失，两者共同决定了抽象电路能否在真实硬件上跑通。
   - **易错坑提醒**：只统计抽象 QASM 线路里的门数就预估真机成功率，忽视编译映射后的 SWAP 膨胀倍数和动态电路中每一百纳秒实时反馈对活比特相干性的持续吞噬。

6. **【计算】“105 比特处理器”“101 比特编码实验”“一个逻辑存储比特”的口径拆解**

   - **题意与约定**：考察物理比特、数据比特、测量辅助比特、专用清理比特与逻辑比特五类容易混淆的计数口径，以 Google Willow 表面码存储实验（*Nature* 638, 2025）为具体标尺精确拆账。
   - **核心提示**：先区分芯片总物理比特数、参与单次编码实验的物理比特数与最终编码出的逻辑比特数，再把码距 $d=7$ 表面码的数据比特 $d^2$、校验辅助比特 $d^2-1$ 与专用清理比特逐项加总核对。
   - **完整分步演算**：
     - **105 比特处理器**：指整块超导芯片上制造并接入测控的全部**物理量子比特总数**，反映芯片硬件体量。
     - **101 比特编码实验**：指在这次码距 $d = 7$ 旋转表面码逻辑存储实验中实际调动参与运行的物理比特数。按旋转表面码最小裸补丁公式 $2d^2 - 1$，当 $d = 7$ 时：
       - 数据比特数：$d^2 = 7^2 = 49$ 个；
       - 纠错症状测量辅助比特数：$d^2 - 1 = 49 - 1 = 48$ 个（合计 $49 + 48 = 97$ 个最小补丁比特）；
       - 额外泄漏清除辅助比特（leakage removal qubits）：$4$ 个。
       三者相加：

       $$
       49 + 48 + 4 = 101\ \text{个物理量子比特}.
       $$

     - **一个逻辑存储比特**：指上述 $101$ 个物理比特通过多轮纠错循环协同编码并保护起来的**单份逻辑量子信息**（$1$ 个逻辑比特，处于静态存储模式，尚未覆盖完整通用逻辑门集）。
   - **结论与边界回验**：$105$ 是整片芯片物理比特总量，$101$ 是单次 $d = 7$ 表面码实验实际动用的物理资源（拆为 $49$ 个数据比特 $+ 48$ 个测量比特 $+ 4$ 个泄漏清除比特），而这整套资源共同维护的是 $1$ 个逻辑存储比特。
   - **易错坑提醒**：把“101 比特纠错实验”误读为“芯片已经造出了 101 个逻辑比特”，或者把 1 个逻辑存储比特的成功直接等同于具备长序列通用容错计算能力。

7. **【计算】理想低温空闲 $T_1 = 100\,\mu\mathrm{s}$ 等待 $5\,\mu\mathrm{s}$ 的存活概率与门保真度辨析**

   - **题意与约定**：考察理想零温单向能量弛豫公式 $P_1(t) = e^{-t/T_1}$（即 $P_1(t) = A e^{-t/T_1} + B$ 中取 $A = 1,\, B = 0$），代入时间比值算出概率，再辨析空闲存活率与门保真度的口径差异。
   - **核心提示**：将 $t=5\,\mu\mathrm{s}$ 与 $T_1=100\,\mu\mathrm{s}$ 代入零温空闲指数衰减公式 $P_1(t)=e^{-t/T_1}$；再辨析空闲弛豫保真度为何不等于运行实际微波门时的综合门保真度。
   - **完整分步演算**：将 $t = 5\,\mu\mathrm{s}$ 与 $T_1 = 100\,\mu\mathrm{s}$ 代入指数衰减律（先核对时间单位一致，均以微秒计）：

     $$
     \frac{t}{T_1} = \frac{5\,\mu\mathrm{s}}{100\,\mu\mathrm{s}} = 0.05,
     $$

     $$
     P_1(5\,\mu\mathrm{s}) = e^{-0.05} \approx 1 - 0.05 + \frac{0.05^2}{2} - \frac{0.05^3}{6} \approx 0.951229 \approx 95.12\%.
     $$

     相应的向下弛豫概率为 $1 - 0.951229 = 0.048771 \approx 4.88\%$。
   - **结论与边界回验**：等待 $5\,\mu\mathrm{s}$ 后仍留在 $|1\rangle$ 的概率约为 $0.95123$（约 $95.12\%$）；**不能**把 $95.1\%$ 直接称为门保真度。因为该数只刻画特定初态 $|1\rangle$ 在“无任何脉冲驱动的低温空闲”下的能量弛豫，既未对所有输入纯态求平均（$|0\rangle$ 零温下不弛豫），也完全未计入纯退相位 $T_\phi$、控制脉冲失准、串扰与高能级 $|2\rangle$ 泄漏，更忽略了有限温度下向上热激发 $p_\infty$ 的影响。
   - **易错坑提醒**：拿 $e^{-t_{\mathrm{gate}}/T_1}$ 当成单比特门保真度的全部，或者以为等待时间只要远小于 $T_1$ 就几乎没有错误——实际只等 $5\%$ 的 $T_1$ 时长，$|1\rangle$ 就已经有接近 $5\%$ 的概率掉回 $|0\rangle$，远高于表面码约 $1\%$ 的物理阈值。

8. **【计算】基于第 5.3 节不对称读出标定表反演真实 $p(1)$ 及依赖前提**

   - **题意与约定**：考察列随机读出混淆矩阵 $q = Ap$ 的一维反演方程 $q_{\mathrm{obs},1} = a(1 - p) + bp$。先从第 5.3 节 2,000 次标定表读出假阳率 $a$ 与真阳率 $b$，再代入观测频率 $\hat q = 480/1000$ 反解 $\hat p$，并逐条列出反演成立的统计与物理假设。
   - **核心提示**：从第 5.3 节标定表读出假阳性率 $a=P(\text{报 }1\mid 0)$ 与真阳性率 $b=P(\text{报 }1\mid 1)$，代入一维列随机关系 $q_{\mathrm{obs},1}=a(1-p)+bp$ 反解真实 $p(1)$，再列出独立同分布与漂移平稳等前提。
   - **完整分步演算**：由第 5.3 节标定表（$n_0 = 1000$ 次制备 $|0\rangle$ 报 `1` 计 $20$ 次；$n_1 = 1000$ 次制备 $|1\rangle$ 报 `1` 计 $940$ 次），读出两个条件概率与读出对比度分母 $g$：

     $$
     a = P(\text{报 }1 \mid \text{真 }0) = \frac{20}{1000} = 0.02, \qquad
     b = P(\text{报 }1 \mid \text{真 }1) = \frac{940}{1000} = 0.94, \qquad
     g = b - a = 0.94 - 0.02 = 0.92.
     $$

     设未知样本真实为 $|1\rangle$ 的概率为 $p$，按全概率公式写出报 `1` 的总概率：

     $$
     q_{\mathrm{obs},1} = a(1 - p) + bp = a + (b - a)p = 0.02 + 0.92p.
     $$

     未知样本 $1{,}000$ 次测量中报 `1` 共 $480$ 次，样本频率 $\hat q = 480 / 1000 = 0.48$。反解真实概率估计值：

     $$
     \hat p = \frac{\hat q - a}{b - a} = \frac{0.48 - 0.02}{0.92} = \frac{0.46}{0.92} = 0.50.
     $$

     （独立回验不确定度：仅计未知态抽样并除以 $g = 0.92$ 得固定标定标准误 $\approx 0.01717$；若按三变量 Delta 方法同步计入 $n_0 = n_1 = 1000$ 的标定抽样误差，总标准误略增至 $\approx 0.01781$。）
   - **结论与边界回验**：反演估计的真实概率为 $\hat p(1) = 0.50$（$50\%$）。该校正依赖五项核心假设：① 标定阶段 $|0\rangle$、$|1\rangle$ 制备本身可靠无显著系统偏差；② 读出混淆矩阵在标定与未知样本测量期间保持时不变（无漂移）；③ 未知样本严格局限在 $\{|0\rangle, |1\rangle\}$ 二能级计算子空间内，不存在向 $|2\rangle$ 态等非计算能级的显著泄漏；④ 多比特场景下无随态变化的读出串扰；⑤ 有限采样（$N, n_0, n_1$）引入的统计波动在可接受误差区间内。
   - **易错坑提醒**：只用原始观测值 $48\%$ 却忽略了 $1\to 0$（$6\%$）比 $0\to 1$（$2\%$）重三倍的不对称读出偏差，或反演时忘记除以对比度 $g = 0.92$ 会同步放大统计方差，甚至在出现严重 $|2\rangle$ 泄漏时仍硬套二能级逆矩阵。

9. **【计算】$100$ 个独立光子的全到达概率（$\eta = 0.99$ 与 $0.999$）及条件保真度边界**

   - **题意与约定**：考察光学损耗的指数级联惩罚 $P_{\mathrm{all}} = \eta^n$。分别代入 $\eta = 0.99$ 与 $\eta = 0.999$、$n = 100$ 精确计算全到达概率，并与条件保真度对比。
   - **核心提示**：利用 $n$ 个独立光子的联合到达概率 $P_{\mathrm{all}}=\eta^n$（可借助 $\ln P=n\ln\eta$ 或直接计算幂次）分别代入 $\eta=0.99$ 与 $0.999$，再与条件保真度的分母口径对比。
   - **完整分步演算**：假设 $100$ 个光子各自独立存活且端到端单光子生存率为 $\eta$，全部 $100$ 个光子同时抵达探测器的概率为 $\eta^{100}$：
     - 当 $\eta = 0.99$（单光子损耗 $1\%$）时：

       $$
       P_{\mathrm{all}}(0.99) = 0.99^{100} = e^{100\ln(0.99)} \approx e^{-1.00503} \approx 0.36603 \approx 36.6\%.
       $$

     - 当 $\eta = 0.999$（单光子损耗 $0.1\%$）时：

       $$
       P_{\mathrm{all}}(0.999) = 0.999^{100} = e^{100\ln(0.999)} \approx e^{-0.10005} \approx 0.90479 \approx 90.5\%.
       $$

     可见单光子损耗仅差 $0.9$ 个百分点，百光子联合存活率就从 $90.5\%$ 暴跌到 $36.6\%$；若规模扩至 $n = 1000$，$\eta = 0.99$ 时的原始全到达率会骤降至 $0.99^{1000} \approx 4.3 \times 10^{-5}$！
   - **结论与边界回验**：单光子生存率 $0.99$ 与 $0.999$ 对应的百光子原始全到达概率分别约为 $36.6\%$ 与 $90.5\%$。条件保真度只衡量“全部到达后的子集有多准”，不能代替原始全到达率来判断系统产率与可扩展性。
   - **易错坑提醒**：误以为“单光子效率 $99\%$ 已经很高了，多光子电路应该差不多”，忽略了无纠错纠删机制时联合存活率随光子数呈指数崩塌（这也是现代光子路线必须转向常数深度资源态 + FBQC 擦除容错的根本原因；若存在损耗相关性或主动补光子机制，则需按具体事件定义重算）。

10. **【计算】三比特线形连接 $0\text{—}1\text{—}2$ 路由 $\mathrm{CNOT}(0, 2)$ 的门数与无故障概率**

    - **题意与约定**：考察近邻拓扑受限时的 `SWAP` 路由展开与独立故障模型下的连乘衰减。先写出保留原逻辑—物理映射的完整相邻门序列计数，再计算 $7$ 门全部无故障的概率。
    - **核心提示**：先把远距 $\mathrm{CNOT}(0,2)$ 拆解为“移近 SWAP + 相邻 CNOT + 恢复 SWAP”并按每个 SWAP $=3$ 个 CNOT 计总门数 $G$，再用独立无故障连乘 $(1-p)^G$ 计算概率。
    - **完整分步演算**：在 $0\text{—}1\text{—}2$ 线形拓扑中，物理比特 $0$ 与 $2$ 没有直连边，不能直接施加 $\mathrm{CNOT}(0, 2)$。若要求执行完毕后各逻辑比特回到原物理位置，标准路由序列分三步：
      1. 施加 $\mathrm{SWAP}(1, 2)$：把原在位置 $2$ 的逻辑比特搬到与 $0$ 相邻的位置 $1$（消耗 $3$ 个 `CNOT`）；
      2. 在相邻位置 $0, 1$ 间施加目标操作 $\mathrm{CNOT}(0, 1)$（消耗 $1$ 个 `CNOT`）；
      3. 再次施加 $\mathrm{SWAP}(1, 2)$：将两比特换回原映射位置（消耗 $3$ 个 `CNOT`）。

      总双比特门数为 $3 + 1 + 3 = 7$ 个（抽象线路原本仅 $1$ 个）。在“每门独立且单门故障率为 $p = 1\% = 0.01$、任一故障即算失败”的理想模型下，七门全部无故障的概率为：

      $$
      P_{\text{无故障}} = (1 - 0.01)^7 = 0.99^7 \approx 0.932065 \approx 93.2\%.
      $$

      对比抽象单门的 $99.0\%$，失败率从 $1\%$ 猛增至约 $6.79\%$（近 $7$ 倍）。
      - **跨平台物理对比（第 9 章硬件视角）**：超导固定耦合平面拓扑必须付出这 $6$ 个额外 `CNOT` 路由代价；而在具备可移动光镊的中性原子阵列或 QCCD 分区离子阱中，可通过物理搬运直接拉近比特间距，此时原本的“额外双比特门错误”被转化为“搬运耗时、运动加热与空闲退相干误差”（编译期布局优化与省去回程 `SWAP` 的收益分析见[第 14 章第 1–2 题](#第-14-章)）。
    - **结论与边界回验**：恢复原映射总共需要 $7$ 个双比特 `CNOT` 门；在理想独立 $1\%$ 故障模型下，七门均不故障的概率约为 $93.2\%$。
    - **易错坑提醒**：忘记还原映射（只算前 $4$ 个门）或忘记 `SWAP` 本身要拆成 $3$ 个 `CNOT`；另外要分清 $93.2\%$ 是题设独立故障模型下的“全无故障概率”，并非真实器件的实测门层保真度（真实硬件还有空闲退相干、串扰、相关错或原生 `iSWAP` 门优化）。

11. **【基础】原子阵列动态解耦 $T_2 = 12.6\,\mathrm{s}$ 与自由演化 $T_2^* = 14.0\,\mathrm{ms}$ 为何不能推出“任意线路无误等 12 秒”**

    - **题意与约定**：考察静态解耦相干寿命与实际执行通用量子线路之间的多重鸿沟。先辨明 $T_2$ 与 $T_2^*$ 的测量条件与 $900$ 倍量级差，再逐条指出其与“无误执行线路”的区别。
    - **核心提示**：对比动态解耦 $T_2$（仅对静态空闲比特反复插回波脉冲压低频相位漂移）与实际线路执行（门操作误差、激光串扰、原子丢失、搬运加热与读出误差），明确静态寿命不能外推为通用线路时长。
    - **完整分步演算**：
      1. **实验协议与物理量不同**：$T_2^* = 14.0\,\mathrm{ms}$ 是未施加回波保护的自由演化（Ramsey）退相位时间，直接暴露在光镊微分光频移与磁场慢漂移下；$T_2 = 12.6\,\mathrm{s}$（是 $T_2^*$ 的 $12.6 / 0.014 = 900$ 倍）是在静态存储期间持续插入大量动态解耦（XY/CPMG 等）翻转脉冲，人为滤除低频静态噪声才测得的“静态存储极限”。
      2. **相干时间 $T_2$ 绝非“无误窗口”**：指数衰减中等待 $t = T_2$ 意味着相干幅已经掉到 $1/e \approx 36.8\%$，远超容错允许的百分之一乃至千分之一误差门槛。
      3. **运行真实线路会打断解耦并引入新噪声**：一旦开始执行任意单/双比特门、Rydberg 激发、光镊搬运重排或中途荧光读出，不仅动态解耦序列难以全程无缝兼容所有门操作，还会额外引入双比特门误差、Rydberg 态自发衰变、多普勒频移、并发串扰以及原子逃逸丢失。
    - **结论与边界回验**：$T_2 = 12.6\,\mathrm{s}$ 与 $T_2^* = 14.0\,\mathrm{ms}$ 对应不同脉冲条件和单位量级，前者仅刻画带动态解耦保护的空闲存储衰减常数（到达 $T_2$ 时相干性已损失超过 $63\%$），绝不能据此宣称任何量子线路都能无误等待约 $12$ 秒。
    - **易错坑提醒**：把论文摘要里最亮眼的“秒级动态解耦相干时间 $T_2$”误解成“芯片可以无损运行十几秒钟的复杂计算线路”。

## 第 10 章

> 对应章节：《10｜量子纠错与容错计算》

1. **【基础】三比特重复码的纠错症状测量为何不泄露未知振幅 $\alpha$ 与 $\beta$**

   - **题意与约定**：考察量子纠错的核心原则——“只问错误，不问数据”。写出三比特重复码逻辑态与两位奇偶稳定子 $Z_1 Z_2, Z_2 Z_3$，逐项检验无论有无单比特翻转，两个逻辑基分支都具有完全相同的稳定子本征值。
   - **核心提示**：把稳定子 $Z_1 Z_2$ 与 $Z_2 Z_3$ 分别作用在逻辑态的两个基分支 $|000\rangle$、$|111\rangle$（以及单比特翻转后的分支）上，观察两分支是否共享完全相同的校验本征值，从而判定测量是否区分 $\alpha$ 与 $\beta$。
   - **完整分步演算**：三比特比特翻转重复码将单比特未知态 $\alpha|0\rangle + \beta|1\rangle$ 编码为：

     $$
     |\psi_L\rangle = \alpha|000\rangle + \beta|111\rangle.
     $$

     纠错症状测量不单独读出任何单个物理比特，而是测量相邻两比特的联合奇偶算符 $g_1 = Z_1 Z_2$ 与 $g_2 = Z_2 Z_3$：
     - **无错时**：$Z_1 Z_2|000\rangle = (+1)(+1)|000\rangle = +|000\rangle$，同时 $Z_1 Z_2|111\rangle = (-1)(-1)|111\rangle = +|111\rangle$；对 $Z_2 Z_3$ 同样皆为 $+1$，整条态满足本征值 $(+1, +1)$（纠错症状 `00`）。
     - **发生单比特翻转（以 $X_2$ 为例）**：受扰态变为 $X_2|\psi_L\rangle = \alpha|010\rangle + \beta|101\rangle$。逐项验证两个分量：

       $$
       Z_1 Z_2|010\rangle = (+1)(-1)|010\rangle = -|010\rangle, \qquad
       Z_1 Z_2|101\rangle = (-1)(+1)|101\rangle = -|101\rangle;
       $$

       $$
       Z_2 Z_3|010\rangle = (-1)(+1)|010\rangle = -|010\rangle, \qquad
       Z_2 Z_3|101\rangle = (+1)(-1)|101\rangle = -|101\rangle.
       $$

     可见，$|010\rangle$ 与 $|101\rangle$ 落入**同一个**联合本征子空间（纠错症状 `11`）。因此投影算符把整条叠加态原封不动地送进该错误子空间，测量结果概率与 $\alpha, \beta$ 完全无关，不破坏两者的相对幅度与相位；随后施加 $X_2$ 即可恢复 $\alpha|000\rangle + \beta|111\rangle$。
   - **结论与边界回验**：纠错症状测量只读取相邻比特“是否一致”的相对奇偶信息，逻辑基态 $|0_L\rangle$ 与 $|1_L\rangle$（及受同一单错作用后的两支）对校验算符具有完全相同的本征值，因而绝不会区分或坍缩未知振幅 $\alpha$ 与 $\beta$。
   - **易错坑提醒**：误以为纠错症状 `11` 唯一意味着“一定发生了 $X_2$”。事实上双比特错 $X_1 X_3$ 也会产生一模一样的纠错症状 `11`；只有在“物理翻转率较低、以至多一错为最可能解释”的解码假设下，纠错症状才直接对应单比特修正。

2. **【基础】三比特比特翻转重复码为何无法检测单个 $Z$ 相位错误**

   - **题意与约定**：考察相位翻转 $Z$ 在计算基下的作用与对易关系。直接把 $Z_1$ 作用在编码态上，检验两条 $Z$ 型奇偶校验的本征值，并对照 Knill–Laflamme 条件看清它为何直接退化为逻辑错误。
   - **核心提示**：把单比特相位错误 $Z_1$ 作用到编码态 $\alpha|000\rangle+\beta|111\rangle$ 上，分别检查它与稳定子 $Z_1 Z_2, Z_2 Z_3$ 的对易关系，看纠错症状是否仍为全正。
   - **完整分步演算**：对编码态 $|\psi_L\rangle = \alpha|000\rangle + \beta|111\rangle$ 在第 $1$ 比特上施加单个相位翻转错误 $Z_1$（因 $Z|0\rangle = +|0\rangle,\ Z|1\rangle = -|1\rangle$）：

     $$
     Z_1|\psi_L\rangle = \alpha(Z_1|000\rangle) + \beta(Z_1|111\rangle) = \alpha|000\rangle - \beta|111\rangle.
     $$

     用两条稳定子生成元 $g_1 = Z_1 Z_2$ 与 $g_2 = Z_2 Z_3$ 检查纠错症状：因为所有 Pauli-$Z$ 算符彼此对易（$g_1 Z_1 = Z_1 g_1$、$g_2 Z_1 = Z_1 g_2$），受错态仍满足：

     $$
     g_1(Z_1|\psi_L\rangle) = +(Z_1|\psi_L\rangle), \qquad
     g_2(Z_1|\psi_L\rangle) = +(Z_1|\psi_L\rangle),
     $$

     纠错症状恒为 `00`，与完全无错时一模一样！从稳定子与 Knill–Laflamme 视角看，$Z_1$ 与所有稳定子对易却不在稳定子群内（$P Z_1 P = |000\rangle\langle 000| - |111\rangle\langle 111| \neq cP$），它本身就是一条权重为 $1$ 的逻辑相位算符 $\bar{Z}$，把逻辑态 $|+_L\rangle$ 静默翻转成了 $|-_L\rangle$。
   - **结论与边界回验**：三比特比特翻转重复码的所有校验都是 $Z$ 型算符，与单个 $Z_j$ 错误全部对易，产生的纠错症状恒为 `00`，因此完全无法检测单个 $Z$ 相位错误（其相位码距 $d_Z = 1$）。
   - **易错坑提醒**：以为“有了 3 比特纠错就能防住任意单比特噪声”。量子比特同时面临比特翻转（$X$）与相位翻转（$Z$）两类正交错误，必须引入 $X$ 型校验（如 Shor 九比特码、五比特码或 CSS/表面码）才能真正纠正任意单比特量子错误。

3. **【基础】稳定子码记号 $[[n, k, d]]$ 的含义与码距 $d = 5$ 的纠错 / 纠擦除上限**

   - **题意与约定**：考察稳定子码三元组的严格定义、码距与未知位置纠错数 $t$、已知位置擦除数 $e$ 之间的基本公式及联合预算不等式 $2t + e < d$。
   - **核心提示**：回忆 $[[n,k,d]]$ 三参数分别对应物理比特数、逻辑比特数与码距，再套用未知位置纠错上限 $t=\lfloor(d-1)/2\rfloor$ 与已知位置擦除纠错上限 $e=d-1$（以及联合界 $2t+e<d$）。
   - **完整分步演算**：在稳定子码记号 $[[n, k, d]]$（双括号用于区别经典线性码 $[n, k, d]$）中：
     - $n$：参与编码的物理量子比特数；
     - $k$：编码出的逻辑量子比特数（码空间维数为 $2^k$，对应 $n - k$ 条独立稳定子生成元）；
     - $d$：码距，即非平凡逻辑 Pauli 算符（正规化子中不属于稳定子群的算符 $N(\mathcal{S})\setminus\mathcal{S}$）的最小 Pauli 权重。

     代入码距 $d = 5$：
     1. **纯未知位置错误**：任意两个权重不超过 $t$ 的错误之积权重 $\le 2t$，要求 $2t \le d - 1$ 才不至于构成不可检测的逻辑错误，故最大可纠个数为：

        $$
        t = \left\lfloor\frac{d - 1}{2}\right\rfloor = \left\lfloor\frac{5 - 1}{2}\right\rfloor = 2.
        $$

     2. **纯已知位置擦除**：硬件提前标出出错物理比特位置时，两个擦除支集均限制在同一批 $e$ 个比特内，其差权重至多 $e$，要求 $e \le d - 1$，故最大可纠个数为：

        $$
        e = d - 1 = 5 - 1 = 4.
        $$

     （两者同时存在时满足联合预算 $2t + e < 5$，例如还可同时纠正 $1$ 个未知错加 $2$ 个已知擦除。）
   - **结论与边界回验**：$[[n, k, d]]$ 分别表示物理比特数 $n$、逻辑比特数 $k$ 与码距 $d$；码距 $d = 5$ 最多可纠正 $2$ 个未知位置错误，或最多 $4$ 个已知位置擦除。
   - **易错坑提醒**：把已知擦除能纠 $4$ 个和未知错能纠 $2$ 个当成可以“同时”发生（误以为能一起纠 $2 + 4 = 6$ 个），违背联合预算 $2t + e \le d - 1 = 4$。

4. **【计算】Steane $[[7, 1, 3]]$ 码中 $X_5$ 与 $Z_6$ 的纠错症状逐项手算**

   - **题意与约定**：考察 CSS 码的解耦检错律（$Z$ 稳定子抓 $X$ 错、$X$ 稳定子抓 $Z$ 错）与对易/反对易判定规则：同位置不同非平凡 Pauli 反对易（记症状比特 `1`），相同或含 $I$ 则对易（记 `0`）。
   - **核心提示**：利用 CSS 码解耦规律：$X_5$ 只可能与含 $Z_5$ 的 $Z$ 型稳定子反对易，$Z_6$ 只可能与含 $X_6$ 的 $X$ 型稳定子反对易；逐行检查 Steane 码六个生成元在第 5 位与第 6 位的 Pauli 算符即可读出两位三元组症状。
   - **完整分步演算**：列出第 10 章 §4.2 的 6 条 Steane $[[7, 1, 3]]$ 稳定子生成元（从左到右对应第 $1$ 至第 $7$ 比特）：
     - $X$ 型：$g_{X,1} = IIIXXXX$，$g_{X,2} = IXXIIXX$，$g_{X,3} = XIXIXIX$；
     - $Z$ 型：$g_{Z,1} = IIIZZZZ$，$g_{Z,2} = IZZIIZZ$，$g_{Z,3} = ZIZIZIZ$。

     1. **计算 $X_5 = IIIIXII$ 的纠错症状**：
        - 与三条 $X$ 型生成元：所有位置均为 $X$ 或 $I$，全部对易 $\implies$ $X$ 检查症状为 `000`。
        - 与三条 $Z$ 型生成元（只需核对第 $5$ 位）：
          - $g_{Z,1}$ 第 $5$ 位为 $Z$：$Z X = -X Z$（反对易 $\to$ `1`）；
          - $g_{Z,2}$ 第 $5$ 位为 $I$：$I X = +X I$（对易 $\to$ `0`）；
          - $g_{Z,3}$ 第 $5$ 位为 $Z$：$Z X = -X Z$（反对易 $\to$ `1`）。
          合得 $Z$ 检查症状为 **`101`**（恰为二进制 $101_2 = 5$，直接指出第 $5$ 位发生 $X$ 错！）。
     2. **计算 $Z_6 = IIIIIZI$ 的纠错症状**：
        - 与三条 $Z$ 型生成元：全部对易 $\implies$ $Z$ 检查症状为 `000`。
        - 与三条 $X$ 型生成元（只需核对第 $6$ 位）：
          - $g_{X,1}$ 第 $6$ 位为 $X$：$X Z = -Z X$（反对易 $\to$ `1`）；
          - $g_{X,2}$ 第 $6$ 位为 $X$：$X Z = -Z X$（反对易 $\to$ `1`）；
          - $g_{X,3}$ 第 $6$ 位为 $I$：$I Z = +Z I$（对易 $\to$ `0`）。
          合得 $X$ 检查症状为 **`110`**（恰为二进制 $110_2 = 6$，直接指出第 $6$ 位发生 $Z$ 错！）。
   - **结论与边界回验**：$X_5$ 触发 $Z$ 检查症状 `101`（$X$ 检查为 `000`）；$Z_6$ 触发 $X$ 检查症状 `110`（$Z$ 检查为 `000`）。
   - **易错坑提醒**：把“谁抓谁”记反，误以为 $X$ 错误由 $X$ 稳定子检测；记住只有**不同种类**的 Pauli 算符（$X$ 与 $Z$）才反对易，所以永远是 $Z$ 检查定位 $X$ 错、$X$ 检查定位 $Z$ 错（而 $Y = iXZ$ 会同时点亮两边）。

5. **【基础】物理错误率低于纠错阈值后，为何工程资源开销仍可能不可接受**

   - **题意与约定**：考察表面码逻辑错误率标度 $\varepsilon_L \approx c\,(p / p_{\mathrm{th}})^{(d+1)/2} = c\,\Lambda^{-(d+1)/2}$ 的定量敏感性，看清“略低于阈值（$\Lambda$ 接近 $1$）”与“远低于阈值（$\Lambda$ 较大）”在码距与物理比特数上的天壤之别。
   - **核心提示**：回看阈值下表面码逻辑错误率标度 $\varepsilon_L\approx c(p/p_{\mathrm{th}})^{(d+1)/2}$：若 $p$ 仅勉强略低于 $p_{\mathrm{th}}$，要压到算法级 $10^{-10}$ 以下所需的码距 $d$、物理比特数 $O(d^2)$、解码功耗与魔术态工厂规模会如何急剧膨胀？
   - **完整分步演算**：阈值定理只保证当 $p < p_{\mathrm{th}}$（即每增两阶码距的错误抑制因子 $\Lambda = p_{\mathrm{th}}/p > 1$）时，逻辑错误率原则上随码距 $d$ 指数下降。但如果物理错误率仅勉强低于阈值，所需码距就会暴涨。举例对比：要将逻辑错误率压低 $10^{10}$ 倍（需 $\Lambda^{(d-1)/2} \approx 10^{10}$，即 $d \approx 1 + \frac{20}{\log_{10}\Lambda}$）：
     - 若物理错率远低于阈值，使 $\Lambda = 10$（如 $p \approx 0.1\,p_{\mathrm{th}}$）：只需 $d \approx 21$，单逻辑比特旋转表面码裸面积为 $2d^2 - 1 = 881$ 个物理比特；
     - 若物理错率仅略低于阈值，使 $\Lambda = 1.2$：因 $\log_{10}(1.2) \approx 0.0792$，所需码距飙升至 $d \approx 253$，单逻辑比特裸面积猛增至 $2\times 253^2 - 1 \approx 1.28 \times 10^5$ 个物理比特（膨胀上百倍！）。

     除此之外，码距翻倍还会同步放大每一轮症状提取的测控带宽、晶格手术逻辑门周期（每步耗时 $\propto d$）、魔法态工厂足迹以及实时经典解码器的算力与尾延迟压力。
   - **结论与边界回验**：“低于阈值”只是纠错能起作用的定性起点；若 $p$ 距离 $p_{\mathrm{th}}$ 不够远（$\Lambda$ 仅略大于 $1$），达到算法级低逻辑错误率所需的码距 $d$、物理比特数、路由与实时解码资源仍会大到工程上难以承受。
   - **易错坑提醒**：把“实验首次跨过纠错阈值（$\Lambda > 1$）”误以为“距离造出百万门容错机只剩简单复制粘贴”，忽略 $\Lambda$ 从 $2$ 提高到 $10$ 往往决定整机规模是十万级还是上亿级物理比特。

6. **【进阶】Eastin–Knill 定理严格限制了什么，又没有否定什么**

   - **题意与约定**：考察容错通用门集的经典禁行定理及其工程绕行路线。明确定理的前提（能检测任意单物理子系统错误的非平凡有限维码 + 横向门）与结论边界。
   - **核心提示**：精确复述 Eastin–Knill 定理的前提（可检单比特错误的非平凡有限维码 + 横向门）与结论（横向门群有限、无法通用），再列举魔术态蒸馏/培育、码切换与晶格手术等绕行路径。
   - **完整分步演算**：
     - **严格限制了什么**：Eastin 与 Knill（*PRL* 2009）证明，对于任何能够检测任意单个物理子系统错误的非平凡有限维量子纠错码，其全体**横向编码门**（transversal gates，即拆成各子系统上独立局域酉操作之张量积的保码空间门）只能构成一个有限离散群，**不可能在逻辑酉群中稠密**——也就是说，**不存在任何单一纠错码能仅靠横向门实现通用量子计算**。例如 Steane 码可横向实现全部 Clifford 门，却无法横向实现 $T$ 门；15 比特 Reed–Muller 码可横向实现 $T$ 门，却不能横向实现 $H$ 门。
     - **没有否定什么**：该定理**绝没有否定通用容错量子计算本身的可行性**，它只是说明必须跳出“单码纯横向门”的窄框，引入至少一种非纯横向容错机制来补齐最后一个非 Clifford 门，包括：**魔法态注入与蒸馏**（如 15-to-1）、**魔法态培育**（Magic State Cultivation, MSC）、**码切换**（code switching，如在 2D 与 3D 色码间切换）、**规范固定**（gauge fixing）以及**晶格手术**（lattice surgery）。
   - **结论与边界回验**：Eastin–Knill 定理排除了用单一纠错码的纯横向门实现通用门集的可能；它没有否定通用容错计算，工程上通过魔法态蒸馏/培育、码切换或晶格手术等机制补齐通用门集。
   - **易错坑提醒**：误以为 Eastin–Knill 定理意味着“量子纠错无法执行非 Clifford 门”或“非 Clifford 门必然不是容错的”。

7. **【基础】容错资源估算为何通常单列 $T$-count、$T$-depth 与魔法态工厂 / 培育池开销**

   - **题意与约定**：考察容错架构下 Clifford 门与非 Clifford 门（以 $T$ 门为代表）之间巨大的物理成本鸿沟。
   - **核心提示**：对照容错架构中 Clifford 门（横向或晶格手术廉价实现）与非 Clifford 门（如 $T$ 门需魔术态蒸馏或培育池）的物理时空体积差距，说明为何 $T$-count 决定总能耗/比特预算而 $T$-depth 制约逻辑运行墙钟时间。
   - **完整分步演算**：在表面码等主流稳定子容错方案中，逻辑 Clifford 门（$H, S, \mathrm{CNOT}$）可借横向操作、Pauli 帧经典软件追踪或晶格手术较廉价地实现（部分 Pauli 修正甚至零物理门开销）。但受 Eastin–Knill 定理制约，构成通用门集所必需的非 Clifford $T$ 门（或 Toffoli 门）无法直接横向执行，必须先制备含噪的物理魔法态 $|T\rangle = \frac{|0\rangle + e^{i\pi/4}|1\rangle}{\sqrt{2}}$，再经过多级**魔法态蒸馏工厂**或**魔法态培育池**（MSC）提纯至算法要求的极低逻辑错误率，最后通过门隐形传态路由注入数据逻辑比特。因此：
     - **$T$-count** 决定总共要生产多少枚高纯度魔法态，直接锚定工厂总产量与算法能耗；
     - **$T$-depth** 决定串行非 Clifford 层的最小轮数，与工厂并行产率、解码反应时间共同锁死算法总墙钟时间；
     - **工厂 / 培育池足迹** 在经典表面码资源估算中往往吞噬全芯片数十个百分点乃至过半的物理比特面积。
   - **结论与边界回验**：在稳定子容错框架下，非 Clifford $T$ 门（及其魔法态制备、提纯与注入）才是决定时空体积和物理比特数的首要瓶颈，因此资源估算必须将 $T$-count、$T$-depth 与魔法态供给系统单独记账。
   - **易错坑提醒**：沿用近期含噪（NISQ）时代的习惯，只看总门数或 `CNOT` 门数来衡量容错算法成本，忽略在容错架构下 $1$ 个 $T$ 门的时空代价往往比 $1$ 个 Clifford 门高出数个量级。

8. **【基础】量子误差缓解（QEM）与量子纠错（QEC）的根本差异**

   - **题意与约定**：考察两类抗噪范式在作用对象、运行机制、资源标度以及物理结果形态上的四维对比。
   - **核心提示**：从作用对象、抗噪机制、阈值下/无阈值资源随深度的标度以及最终交付物（经典期望值 vs 可复用逻辑量子态）四个维度对照 QEM 与 QEC。
   - **完整分步演算**：
     - **目标与产物不同**：QEM 通过多次重复运行含噪线路并对测量读数做经典后处理（外推、准概率重加权或对称性筛选），仅恢复最终经典期望值 $\langle O\rangle$ 的更低偏差估计；QEC 通过将逻辑信息编码进冗余物理比特、反复提取纠错症状并实时解码修正（或更新 Pauli 帧），主动保护整个未知逻辑量子态本身。
     - **资源标度不同**：QEM 用不断放大的统计方差与采样次数换取偏差缩减，随着电路深度 $L$ 或门数增加，其采样开销一般呈指数增长（如 PEC 的 $\gamma_{\mathrm{PEC}}^{2L}$），存在根本的可扩展天花板；QEC 在物理错误率低于阈值后，只需多项式增加物理比特数与码距 $d$，即可让逻辑错误率随 $d$ 呈指数压低，支持任意长通用算法。
     - **硬件门槛不同**：QEM 不要求中途测量、实时解码或大量冗余物理比特，适用于近期浅层含噪设备；QEC 需要高质量中途测量、主动复位、低串扰与实时低延迟解码器。
     - **阈值下指数压错标度对照（第 10 章容错编码视角）**：与[第 8 章第 6 题](#第-8-章)展示的 QEM 指数采样墙相反，只要物理错误率 $p$ 低于纠错阈值 $p_{\mathrm{th}}$，表面码每轮逻辑错误率随码距 $d$ 呈指数下降：

       $$
       p_L(d) \approx A\left(\frac{p}{p_{\mathrm{th}}}\right)^{(d+1)/2}.
       $$

       例如在 $p/p_{\mathrm{th}} = 0.1$ 时，码距每增大 $2$（物理比特仅多项式级按 $O(d^2)$ 增长），逻辑错误率即压缩 $10$ 倍：从 $d = 3$ 升至 $d = 15$ 即可把每轮逻辑错误率压低 $10^6$ 倍，且所得结果是可继续送入任意深后续逻辑线路的受保护量子态。
   - **结论与边界回验**：QEM 是在不保护量子态的前提下用指数级采样换取经典期望偏差下降的近期统计技术；QEC 是借冗余编码与纠错症状反馈在阈值下实现指数级逻辑错误抑制的可扩展容错体系，QEM 无法替代 QEC。
   - **易错坑提醒**：把 QEM 看作“轻量级 QEC”，以为只要把误差缓解算法不断改进，就能绕过量子纠错直接跑 Shor 算法或百万门化学模拟。

9. **【计算】无辅助位 Clifford+$T$ 近似 $z$ 旋转的 $T$-count 增量与物理资源边界**

   - **题意与约定**：考察 Ross–Selinger（2016）单比特 $z$ 旋转最优无辅助位综合公式 $N_T(\epsilon) \approx 3\log_2(1/\epsilon) + O(\log_2\log_2(1/\epsilon))$。先精确算出 $\epsilon$ 从 $10^{-6}$ 收紧到 $10^{-12}$ 时的主项差值，再说明为何不能把 $T$-count 增量直接等同于整机物理资源增量。
   - **核心提示**：把 $\epsilon_1=10^{-3}$ 与 $\epsilon_2=10^{-9}$ 分别代入主项 $N_T(\epsilon)\approx 3\log_2(1/\epsilon)$ 求差值 $\Delta N_T=3\log_2(\epsilon_1/\epsilon_2)$，再指出总资源还受码距与蒸馏开销约束。
   - **完整分步演算**：分别代入 $\epsilon_1 = 10^{-6}$ 与 $\epsilon_2 = 10^{-12}$ 计算主项（注意必须明写以 $2$ 为底的对数 $\log_2$，利用 $\log_2 10 \approx 3.321928$）：

     $$
     N_T^{\text{主项}}(10^{-6}) = 3\log_2(10^6) = 18\log_2 10 \approx 18 \times 3.321928 \approx 59.795,
     $$

     $$
     N_T^{\text{主项}}(10^{-12}) = 3\log_2(10^{12}) = 36\log_2 10 \approx 36 \times 3.321928 \approx 119.589.
     $$

     两者相减得主项增量：

     $$
     \Delta N_T^{\text{主项}} = 3\bigl[\log_2(10^{12}) - \log_2(10^6)\bigr] = 3\log_2(10^6) \approx 59.795 \approx 60\ \text{个 } T\ \text{门}.
     $$

     误差收紧整整 $6$ 个数量级（缩小 $10^6$ 倍），$T$-count 仅增加约 $60$ 个（翻倍），这正是 Solovay–Kitaev / Ross–Selinger 对数综合缩放的巨大威力。
   - **结论与边界回验**：$T$-count 主项约增加 $59.8$（约 $60$ 个 $T$ 门）。但这**不等于**完整的物理资源增量：一方面综合公式还含次阶常数项与具体旋转角依赖；另一方面，更严苛的整机误差目标往往还会逼迫算法整体提高表面码码距 $d$、升级魔法态工厂蒸馏级数（或切换更高纯度培育方案），并同步改变 $T$-depth、路由等待周期与经典解码负载。
   - **易错坑提醒**：忘写对数底数误用自然对数 $\ln(10^6) \approx 13.8$（错算成增加约 $41.4$ 个 $T$ 门），或以为“单个旋转门多花 $60$ 个 $T$ 门”可以直接按固定比例换算成物理比特增量，忽略了容错码距跳档带来的非线性整机跃升。

10. **【计算】三比特重复码编码 $|+\rangle$ 所得态与乘积态 $|+\rangle^{\otimes 3}$ 的单次测量区分**

    - **题意与约定**：考察“量子纠错编码”与“不可克隆复制”的本质区别。分别完整展开编码态和三份乘积态在计算基下的 8 个分量，直接对比单次计算基测量的可能输出集合。
    - **核心提示**：分别在 8 维计算基下完整展开编码态 $\frac{|000\rangle+|111\rangle}{\sqrt{2}}$（GHZ 纠缠态）与三份乘积态 $|+\rangle^{\otimes 3}$，比较两者的支撑基串集合——只需思考单次计算基测量能否出现 `001` 等异位串。
    - **完整分步演算**：
      1. **三比特重复码编码态**：编码线路把 $|0\rangle|00\rangle \mapsto |000\rangle$、$|1\rangle|00\rangle \mapsto |111\rangle$，由线性性作用于 $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ 得三比特 GHZ 纠缠态：

         $$
         |\psi_{\mathrm{enc}}\rangle = \frac{|000\rangle + |111\rangle}{\sqrt{2}}.
         $$

         在计算基下，只有 `000` 和 `111` 两个全同串有非零概率（各为 $|1/\sqrt{2}|^2 = 1/2$），其余 $6$ 个混合串（`001, 010, 011, 100, 101, 110`）的概率全部严格为 **$0$**。
      2. **三份独立乘积态 $|+\rangle^{\otimes 3}$**：将三个括号逐项展开：

         $$
         |+\rangle^{\otimes 3}
         = \frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes \frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes \frac{|0\rangle + |1\rangle}{\sqrt{2}}
         = \frac{1}{2\sqrt{2}}\sum_{x \in \{0,1\}^3} |x\rangle.
         $$

         全部 $8$ 个三比特串振幅均为 $\frac{1}{2\sqrt{2}}$，概率各为 $\left|\frac{1}{2\sqrt{2}}\right|^2 = \frac{1}{8}$（总和 $8 \times \frac{1}{8} = 1$）。
      3. **单次计算基测量的区分**：测量 $|+\rangle^{\otimes 3}$ 有高达 $6 \times \frac{1}{8} = \frac{3}{4} = 75\%$ 的概率落入非全同串（例如 `001` 概率为 $1/8$），而理想编码态 $|\psi_{\mathrm{enc}}\rangle$ 绝对不可能输出任何非全同串（只要单次测出 `001` 等六串之一，即可 $100\%$ 确定该态不是编码态）。
    - **结论与边界回验**：编码 $|+\rangle$ 得到的是高度纠缠的三比特态 $\frac{|000\rangle + |111\rangle}{\sqrt{2}}$，而非三份独立副本 $|+\rangle^{\otimes 3}$；一次计算基测量中，编码态只能产出 `000` 或 `111`（各 $1/2$），而乘积态有 $3/4$ 的概率产出 `001` 等六个非全同串（每串 $1/8$）。
    - **易错坑提醒**：把三比特重复码口头上理解成“把一个未知量子比特复制成三份做少数服从多数表决”，违背不可克隆定理；纠错编码做的是**跨比特纠缠扩展**，而非制造独立副本。

## 第 11 章

> 对应章节：《11｜基准测试与容错资源估算》

1. **【基础】随机基准测试（RB）的平均门错误为何不能直接预测长结构化线路的表现**

   - **题意与约定**：考察 RB 协议的群均化机制（Clifford 2-设计把任意噪声平均成各向同性去极化信道）与结构化算法线路中相干误差、串扰及慢漂移累积之间的本质错位。
   - **核心提示**：回忆 RB 用随机 Clifford 门把任意噪声通道“旋转平均”成各向同性退极化；对照结构化算法线路中相干旋转角同向线性叠加、特定对串扰与时变漂移如何打破随机平均假设。
   - **完整分步演算**：RB 通过随机插入大量 Clifford 门，把任意门噪声 $\mathcal{E}$ 平均为单参数去极化信道 $\mathcal{D}_\alpha$，再由衰减率 $\alpha$ 算出平均门错误率 $r = \frac{d-1}{d}(1-\alpha)$。这在长结构化算法线路中存在四重盲区：
     1. **相干误差的平方根鸿沟**：设单门存在固定相干过旋转角 $\theta$（如 $e^{-i\theta Z/2}$），随机均化使正负相位抵消，RB 测得的平均错误率仅为二阶小量 $r \propto \theta^2$；但在结构化重复电路中，相干小角度会沿同一方向线性叠加，对应的最坏信道偏差（钻石距离）按一阶缩放 $\frac{1}{2}\|\mathcal{U}_\theta - \mathcal{I}\|_\diamond = O(\theta) = O(\sqrt{r})$。例如 $r \sim 10^{-4}$ 时，钻石距离可高达 $10^{-2}$ 量级（差两个量级！）。
     2. **掩盖特定差门与门依赖噪声**：RB 给出的是整组 Clifford 门的平均表现，可能掩盖算法高频调用的某一个表现极差的双比特门。
     3. **忽略并发串扰与路由上下文**：单/双比特孤立 RB 不反映百比特全芯片并行运行时的残余 $ZZ$ 串扰与频率碰撞。
     4. **忽略非马尔可夫漂移与高能级泄漏**：慢漂移、时间相关噪声和向 $|2\rangle$ 态的泄漏会破坏纯指数衰减假设，在深线路中造成远高于 $1 - (1-r)^G$ 的失真。
   - **结论与边界回验**：RB 的随机均化抹平了相干误差的方向性累积，也掩盖了特定差门、并行串扰、慢漂移和泄漏，因此平均门错误率 $r$ 不能直接预测长结构化线路的真实成功率（需结合镜像电路、循环基准测试 CB、门集层析 GST 与应用基准综合评估）。
   - **易错坑提醒**：拿芯片手册上孤立 RB 测得的 $r = 0.001$ 直接套入 $(1 - r)^G$，误以为一定能稳跑一千门结构化算法。

2. **【计算】$p = 10^{-3},\, G = 1{,}000$ 独立错误算例说明了什么，又没有说明什么**

   - **题意与约定**：考察独立门故障连乘近似 $(1 - p)^G \approx e^{-pG}$ 的定量直觉及其严格适用边界。先精确算出数值并对照指数近似，再拆解模型忽略的现实物理因素。
   - **核心提示**：分别用精确幂 $(1-p)^G$ 与指数近似 $e^{-pG}$ 计算 $p=10^{-3},G=1000$ 的无故障概率，再逐条核查模型背后“独立、无相关、无串扰、无读出错误与无纠错”的理想前提。
   - **完整分步演算**：假设一条电路含 $G = 1{,}000$ 个门，每门以概率 $p = 10^{-3}$ 独立发生故障，且只要任意一门出错就导致整次运行失败。全部 $G$ 门均无故障的概率为：

     $$
     P(\text{全无错}) = (1 - p)^G = (1 - 10^{-3})^{1000} = 0.999^{1000}.
     $$

     取自然对数利用 $\ln(1 - x) \approx -x - \frac{x^2}{2}$ 精确计算：

     $$
     1000\ln(0.999) \approx 1000\bigl(-0.001 - 5\times 10^{-7}\bigr) = -1.0005003
     \implies 0.999^{1000} \approx 0.36770,
     $$

     与一阶指数近似 $e^{-pG} = e^{-1} \approx 0.36788$（约 $36.8\%$）高度一致。
   - **结论与边界回验**：
     - **说明了什么**：即便单门精度高达 $99.9\%$（错误率 $10^{-3}$），面对 $1{,}000$ 门规模的线路时，误差量与门数相乘（$pG = 1$）就会让无错概率骤降至仅约 $36.8\%$；要运行百万门乃至十亿门级算法，单靠硬压物理错误率远远不够，必须引入容错量子纠错。
     - **没有说明什么**：该简化模型既没有刻画相干误差沿结构化电路线性叠加（最坏失败率可按 $G^2 p$ 更快崩塌）或宇宙射线等空间关联突发错误，也没有计入容错纠错码可实时修正部分错误的情形，更不等于真实电路在具体观测量上的保真度。
   - **易错坑提醒**：把 $36.8\%$ 当成所有含 $1{,}000$ 个 $99.9\%$ 门的真实芯片线路的精确成功率，或者误以为 $p = 10^{-3}$ 已经足以直接跑深层无纠错算法。

3. **【计算】条件保真度为 $99\%$、接受率为 $1\%$ 时为何绝不能省略接受率**

   - **题意与约定**：考察后选择与检错实验中的“质量—产率双指标绑定原则”。用具体重复率代入算出有效吞吐缩水倍数，并指出省略接受率会造成的两类严重误导。
   - **核心提示**：先用有效事件率 $R_{\mathrm{eff}}=f_{\mathrm{rep}}p_{\mathrm{acc}}$ 核算吞吐缩水与多步级联的 $p_{\mathrm{acc}}^k$ 衰减，再比较用留存样本数 $N_{\mathrm{kept}}$ 与原始总尝试数 $N_{\mathrm{raw}}$ 计算置信区间时的宽度差异。
   - **完整分步演算**：设设备原始尝试重复率为 $f_{\mathrm{rep}} = 10^5\,\mathrm{s}^{-1}$，但后选择或错误检测的接受率仅为 $p_{\mathrm{acc}} = 1\% = 0.01$，则每秒真正留下来可用的有效事件数为：

     $$
     R_{\mathrm{eff}} = f_{\mathrm{rep}} \cdot p_{\mathrm{acc}} = 10^5 \times 0.01 = 10^3\ \text{次/秒},
     $$

     高达 $99\%$ 的原始运行都被丢弃了！如果某项多步任务需要连续 $k$ 次独立后选择全部通过，总接受率还会按 $0.01^k$ 指数崩塌（$k = 3$ 时仅剩 $10^{-6}$），墙钟时间瞬间暴涨百万倍。此外，如果接受条件与某些特定输出状态相关，强行丢弃样本还可能扭曲原任务的无偏输出分布。
     - **系统基准与统计区间放大核算（第 11 章专属深化）**：接受率不仅压缩每秒有效交付率，还会按 $1/\sqrt{p_{\mathrm{acc}}}$ 急剧放大统计不确定度！设原始总运行 $N_{\mathrm{raw}} = 10^4$ 次、接受率 $p_{\mathrm{acc}} = 1\%$，则真正进入条件保真度统计的留存样本只有 $N_{\mathrm{kept}} = N_{\mathrm{raw}} p_{\mathrm{acc}} = 100$ 次（标准误直接放大 $1/\sqrt{0.01} = 10$ 倍）。若这 $100$ 次中成功 $99$ 次（$\hat{F}_{\mathrm{cond}} = 0.99$），按双侧 $95\%$ Wilson 区间（$z \approx 1.96$）对照两种分母：

       $$
       \text{正确留存分母 }(N_{\mathrm{kept}}=100):\ [0.9455,\; 0.9982]\ (\text{宽 }5.27\text{ 个百分点}),
       $$

       $$
       \text{误用原始分母 }(N_{\mathrm{raw}}=10^4):\ [0.9879,\; 0.9918]\ (\text{宽 }0.39\text{ 个百分点}).
       $$

       一旦省略 $p_{\mathrm{acc}} = 1\%$ 或错用原始运行次数作分母，置信区间宽度会被虚压约 $13.5$ 倍，严重高估实验统计精度（光子损耗机理见[第 9 章第 3 题](#第-9-章)，论文完整披露条目见[第 15 章第 6 题](#第-15-章)）。
   - **结论与边界回验**：省略 $1\%$ 的接受率只报“$99\%$ 保真度”，会把“扔掉 $99\%$ 失败样本后留下的极少数幸存结果很准”误导成“设备正以高吞吐稳定输出高精度答案”；必须把条件保真度、接受率、原始尝试总数与每秒有效产率一并报告。
   - **易错坑提醒**：拿检错后选择（error detection，靠丢弃坏样本换高保真度）的数字直接与主动纠错（error correction，不丢样本且可连续扩展）的结果横向比高低。

4. **【基础】证明逻辑存储低于阈值后，距离通用容错计算还缺哪些证据**

   - **题意与约定**：考察容错量子计算的能力阶梯。“静态存储低于阈值（$\Lambda > 1$）”只是验证了逻辑信息能被保住，距离运行通用容错算法仍需打通一整套动态逻辑操作与系统工程闭环。
   - **核心提示**：沿着容错能力阶梯，从“静态存储保住单比特”往后依次补齐逻辑制备/读出、低错率双逻辑比特纠缠门、非 Clifford 门（魔术态工厂）、多比特晶格手术路由与实时解码闭环。
   - **完整分步演算**：从“单逻辑比特低于阈值存储”走向“通用容错量子计算（FTQC）”，至少还缺六类关键实证证据：
     1. **高保真逻辑态制备与逻辑读出**：能容错初始化并读取不同基下的逻辑态；
     2. **长时间多轮稳定纠错循环与泄漏管理**：在成千上万轮症状提取中维持不漂移、不因 $|2\rangle$ 泄漏或突发关联错误撞上高错误底板；
     3. **通用容错逻辑 Clifford 门与多逻辑比特扩展**：演示跨多块逻辑比特的横向逻辑门或晶格手术（如逻辑 $\overline{\mathrm{CNOT}}$、$\bar{H}$、$\bar{S}$）并验证多逻辑比特扩展时串扰受控；
     4. **容错非 Clifford 资源供给**：集成魔法态蒸馏工厂或魔法态培育池（MSC）与逻辑 $T$ 门注入，突破 Eastin–Knill 限制；
     5. **实时在线解码闭环**：在硬件循环周期 $\tau_{\mathrm{cyc}}$ 与反应时间 $\tau_{\mathrm{react}}$ 约束内实时输出解码决策并执行自适应前馈（而非事后离线批处理解码）；
     6. **端到端完整算法资源与成功率核算**：在真实容错逻辑线路上运行完整应用并核算总物理比特数、墙钟时间与最终答案精度。
   - **结论与边界回验**：低于阈值逻辑存储证明的是“容错内存”的可行性；要称为通用容错计算，还必须补齐逻辑制备/测量、多逻辑比特 Clifford 门与晶格手术、魔法态蒸馏/培育与非 Clifford 门注入、实时在线解码闭环、泄漏抑制以及端到端逻辑算法运行证据。
   - **易错坑提醒**：把“表面码存储实验突破阈值（$\Lambda > 1$）”解读为“通用容错量子计算机已经建成”。

5. **【基础】QV、XEB、CLOPS 与应用基准各自主要回答什么问题**

   - **题意与约定**：考察系统级与应用级四大主流基准尺子的设计目标、量程与固有盲区，明确为什么它们各自回答不同维度的问题、不能互相替代。
   - **核心提示**：按“有效方阵电路规模（QV）”“随机线路采样交叉熵保真度（XEB）”“电路编译到执行的端到端速度（CLOPS）”“特定领域任务指标（应用基准）”四条轴清晰界定各自量程与盲区。
   - **完整分步演算**：
     - **量子体积（QV）**：通过随机方形线路（宽度 $m$ 等于深度 $d$）的重输出概率是否统计显著超过 $2/3$，回答“这台机器能可靠跑通的最大方形随机线路规模 $2^m$ 有多大”，综合反映物理门质量、连通性与编译器优化能力，但因经典验证需精确模拟，难以扩展到 $m > 30$ 以上。
     - **线性交叉熵基准（XEB）**：把随机线路实测比特串在理想分布下的平均概率与均匀分布对比，回答“芯片执行深层随机采样电路时的整体分布保真度大致有多高”。但它不是严格分布距离，易受截断张量网络经典欺骗（spoofing），也不代表结构化算法表现。
     - **CLOPS（每秒电路层操作数）**：在固定体积内跑完一整套参数化更新的变分循环并计入编译与经典通信，回答“全栈系统（量子硬件 + 控制电子学 + 经典编排）的执行速度与吞吐有多快”。注意 IBM 已从 $\mathrm{CLOPS}_v$ 切换到 $\mathrm{CLOPS}_h$ 口径，不可把新旧版本画在同一条曲线上。
     - **应用导向基准（如 QED-C、SupermarQ）**：选取量子傅里叶变换、Grover、VQE、QAOA、哈密顿量模拟等典型工作负载，回答“面对具体结构化算法任务时，整套系统交出的答案质量、耗时与资源消耗究竟如何”。
   - **结论与边界回验**：QV 测综合可执行方形规模（质量×连通），XEB 测随机采样分布相关性，CLOPS 测全栈电路执行速度，应用基准测具体任务的端到端答案质量与资源；四者各司其职，不能用单一标量代替其余维度。
   - **易错坑提醒**：把某台机器的高 XEB 或高 QV 分数当成“它在所有商业或科学应用上都更快更准”的通用总分。

6. **【基础】实时解码器的吞吐、响应时延与准确率为何不能互相替代**

   - **题意与约定**：考察容错计算中实时经典解码器的三维刚性约束（对应第 11 章 §7.3）。分别给出三个物理量的定义，用离线批处理与积压发散两个反例说明缺一不可。
   - **核心提示**：严格区分平均处理速率（吞吐）、单次反馈等待上限（尾延迟）与纠错判决正确率（准确率），并思考“离线批处理吞吐够但时延爆表”与“单次很快但平均来不及导致队列雪崩”两种反例。
   - **完整分步演算**：
     - **准确率**：衡量解码器从含噪纠错症状中正确反推逻辑翻转的能力，直接决定有效逻辑错误率 $\varepsilon_L$ 与纠错阈值（准确率太低会直接吞噬硬件的物理保真度红利）。
     - **吞吐率**：衡量解码器单位时间内能持续消化的症状轮数（平均单轮解码耗时 $T_{\mathrm{dec}}$ 必须严格小于硬件纠错周期 $\tau_{\mathrm{cyc}}$）。按 Terhal 积压分析，只要 $T_{\mathrm{dec}} > \tau_{\mathrm{cyc}}$（积压比 $r_{\mathrm{back}} = T_{\mathrm{dec}}/\tau_{\mathrm{cyc}} > 1$），串行执行 $k$ 层自适应非 Clifford $T$ 门时未解码数据会按 $r_{\mathrm{back}}^k$ 指数级积压，最终把计算拖死。
     - **响应时延（含高分位尾延迟）**：衡量一轮症状到达后，解码器多快把纠正决策送回硬件控制器以执行下一层自适应 $T$ 门前馈。离线批处理解码器即使吞吐极高、准确率极佳，也可能因为攒批等待未来数据而拥有极长的尾延迟，导致在线逻辑比特原地空等退相干；反过来，单次响应极快但平均吞吐赶不上芯片产率，队列仍会不断积压崩溃。
   - **结论与边界回验**：准确率决定逻辑错误率高低，吞吐决定能否跟上症状产率避免指数积压，响应时延（尤其 99% 以上高分位尾延迟）决定逻辑门反应速度与墙钟时间；三者约束不同环节，缺一不可、不能互换（报告时须同步注明码距、并行度与尾延迟分位）。
   - **易错坑提醒**：看到某解码论文报出“离线批处理平均每轮仅 $0.4\,\mu\mathrm{s}$”就认为它已满足 $1\,\mu\mathrm{s}$ 超导周期实时要求，忽略批处理引入的长响应延迟以及偶发 $99.9\%$ 长尾延迟卡死整机同步的风险。

7. **【基础】比较量子与经典能耗时，至少须冻结哪些系统边界与成功条件**

   - **题意与约定**：考察量子—经典跨平台能耗对比的公平会计准则 $E_{\mathrm{solution}} = \frac{P_{\mathrm{tot}}\, t_{\mathrm{wall}}}{P_{\mathrm{success}}}$。先冻结“算什么、算多准”，再把两侧墙插电表边界画在完全对称的机房级口径上，并用正文简化算例演示核算。
   - **核心提示**：从整机墙钟功率边界（制冷机、测控机柜、解码与冷却外设）以及同任务、同解质量、同成功概率与端到端解题时间 $E_{\mathrm{solution}}=P_{\mathrm{tot}}t_{\mathrm{wall}}/p_{\mathrm{succ}}$ 列出冻结清单。
   - **完整分步演算**：公平比较两端的能源消耗，必须先冻结两组前提：
     1. **冻结任务与成功条件**：同一具体问题、同一输入规模、同一输出精度或置信度门槛、同一失败概率定义，并同时报告墙钟时间 $t_{\mathrm{wall}}$（防止慢几十倍换低功率的伪节能）。
     2. **冻结对称的整机系统边界**：功率分子 $P_{\mathrm{tot}} = P_{\mathrm{cryo}} + P_{\mathrm{laser}} + P_{\mathrm{control}} + P_{\mathrm{classical}} + P_{\mathrm{facility}}$ 必须明示是否完整包含稀释制冷机墙插电功率、激光与光学系统、室温/低温控制电子学、实时经典解码与前后处理服务器、机房配电与冷却（PUE）、校准停机期间的空闲基荷摊销，以及失败重试与后选择倍率 $1/P_{\mathrm{success}}$。

     例如按正文简化算例：整机边界内平均功率 $P_{\mathrm{tot}} = 20\,\mathrm{kW}$、单次运行墙钟时间 $t_{\mathrm{wall}} = 30\,\mathrm{s}$、独立成功概率 $P_{\mathrm{success}} = 0.25$，则平均产出一个合格解的能耗为：

     $$
     E_{\mathrm{solution}} = \frac{20\,\mathrm{kW} \times 30\,\mathrm{s}}{0.25} = 2{,}400\,\mathrm{kJ} = 2.4\,\mathrm{MJ} = \frac{2.4}{3.6}\,\mathrm{kWh} \approx 0.67\,\mathrm{kWh}.
     $$

   - **结论与边界回验**：至少须冻结同一任务、规模、精度/成功标准与墙钟时间，并在两端划定同等口径的墙插系统边界（含制冷、光控、经典解码、机房 PUE、空闲校准摊销及重试/后选择成本）；绝不能拿含全套制冷机房的量子整机，去对比只算单块 GPU 芯片热设计功耗的经典数字（或反之）。
   - **易错坑提醒**：只拿量子芯片冷头上那几纳瓦的微波耗散功率宣传“量子计算几乎不耗电”，忽略在 $10\text{--}20\,\mathrm{mK}$ 温区每排走 $1\,\mathrm{W}$ 冷端热量，室温稀释制冷机与压缩机需要消耗 $10^6\text{--}10^7\,\mathrm{W}$ 墙插电功率。

8. **【计算】甲、乙两系统有效可用记录速率对比与选择性偏差陷阱**

   - **题意与约定**：考察有效吞吐计算 $R_{\mathrm{eff}} = f_{\mathrm{rep}} \cdot p_{\mathrm{acc}}$ 与后选择统计无偏性的双重检验。先分别算出每秒可用记录数，再剖析接受偏差如何破坏结果有效性。
   - **核心提示**：套用 $R_{\mathrm{eff}}=f_{\mathrm{rep}}\cdot p_{\mathrm{acc}}$ 分别计算甲乙每秒可用记录数；第二问思考若后选择接受概率依赖于真实输出串，留存样本分布会如何偏离原目标分布。
   - **完整分步演算**：
     - **系统甲**：原始尝试率 $10^5\,\mathrm{s}^{-1}$，接受率 $1\% = 0.01$，每秒可用记录数为：

       $$
       R_{\mathrm{eff},\text{甲}} = 10^5 \times 0.01 = 1{,}000\ \text{条/秒}.
       $$

     - **系统乙**：原始尝试率 $2\times 10^4\,\mathrm{s}^{-1}$，接受率 $50\% = 0.50$，每秒可用记录数为：

       $$
       R_{\mathrm{eff},\text{乙}} = 2\times 10^4 \times 0.50 = 10{,}000\ \text{条/秒}.
       $$

     尽管甲的原始时钟快了 $5$ 倍，但按有效可用记录计，乙反而是甲的 **$10$ 倍**（$10{,}000 / 1{,}000 = 10$）。
   - **结论与边界回验**：甲每秒产出 $1{,}000$ 条可用记录，乙每秒产出 $10{,}000$ 条（乙为甲的 $10$ 倍）。但如果“接受事件”系统性偏向某些输出（例如某些比特串更容易丢光子或更易通过检错），保留下来的高吞吐数据就构成**有偏分布**，不能代表原任务的真实解；因此除了速率，还必须核查接受判据是否与输入或目标答案独立、单条记录的保真度与统计质量，以及达到同一无偏误差目标所需的总墙钟时间。
   - **易错坑提醒**：先入为主地盯住高原始重复率（$10^5\,\mathrm{Hz}$），或者算出乙有效吞吐高 $10$ 倍后就立刻判乙胜出，忘了检查后选择是否引入了系统性输出偏置。

9. **【计算】单比特去极化模型（$d = 2,\, \alpha = 0.998$）的 $F_{\mathrm{avg}}$、$r$、根保真度 $F$ 与 $1 - F$ 陷阱**

   - **题意与约定**：考察全书保真度符号契约（平方重叠 $F_{\mathrm{avg}} = F^2$ vs 根保真度 $F = \operatorname{Tr}\sqrt{\sqrt{\rho}\sigma\sqrt{\rho}}$）。套用第 11 章 §3.1 推导好的精确公式逐项代入，并定量揭示错用 $1 - F$ 导致的近半误差低估。
   - **核心提示**：代入单比特去极化平均门保真度公式 $F_{\mathrm{avg}}=\frac{d\alpha+1}{d+1}$ 与 $r=1-F_{\mathrm{avg}}$，再对纯态取平方根求本书约定的根保真度 $F=\sqrt{F_{\mathrm{avg}}}$ 并比较 $1-F$ 与 $r=1-F^2$ 的约两倍差距。
   - **完整分步演算**：单比特希尔伯特空间维数 $d = 2$，去极化信道 $\mathcal{D}_\alpha(\rho) = \alpha\rho + (1-\alpha)\frac{I}{d}$，代入 $\alpha = 0.998$：
     1. **平均门保真度 $F_{\mathrm{avg}}$**：对任意归一化纯态 $|\psi\rangle$，输出重叠概率相同且等于平均门保真度：

        $$
        F_{\mathrm{avg}} = \alpha + \frac{1 - \alpha}{d} = 0.998 + \frac{1 - 0.998}{2} = 0.998 + 0.001 = 0.999.
        $$

     2. **平均门不保真度（平均门错误率）$r$**：

        $$
        r = 1 - F_{\mathrm{avg}} = \frac{d - 1}{d}(1 - \alpha) = \frac{1}{2}(0.002) = 0.001 \quad (0.1\%).
        $$

        （顺带核验过程保真度 $F_p = \frac{(d+1)F_{\mathrm{avg}} - 1}{d} = \frac{3\times 0.999 - 1}{2} = 0.9985$。）
     3. **任意纯输入的根保真度 $F$**：当其中一个态为纯态 $|\psi\rangle$ 时，根保真度简化为 $F\bigl(|\psi\rangle\langle\psi|,\ \mathcal{D}_\alpha(|\psi\rangle\langle\psi|)\bigr) = \sqrt{\langle\psi|\mathcal{D}_\alpha(|\psi\rangle\langle\psi|)|\psi\rangle} = \sqrt{F_{\mathrm{avg}}}$：

        $$
        F = \sqrt{0.999} \approx 0.999499875 \approx 0.99950.
        $$

     4. **检验为何 $r$ 不能写成 $1 - F$**：若误把根保真度代入 $1 - F$，会算出：

        $$
        1 - F = 1 - \sqrt{0.999} \approx 0.000500125 \approx 0.00050,
        $$

        因为对小 $r$ 有 $1 - \sqrt{1 - r} \approx \frac{r}{2}$，这会把真实平均门错误率 $r = 0.001$ 凭空算小将近一半！
   - **结论与边界回验**：$F_{\mathrm{avg}} = 0.999$，平均门不保真度 $r = 0.001$，任意纯输入下的根保真度 $F = \sqrt{0.999} \approx 0.99950$；因为 $F_{\mathrm{avg}}$ 定义为平方重叠（$F^2$）的 Haar 平均，故 $r = 1 - F^2$，绝不能写成 $1 - F$。
   - **易错坑提醒**：在不同论文或软件文档之间复制保真度数字时，不核对对方报的是平方重叠 $F^2$ 还是根保真度 $F$，导致报告出的错误率平白差出一个因子 $2$。

## 第 12 章

> 对应章节：《12｜量子密码、后量子安全与量子网络》

1. **【基础】后量子密码（PQC）与量子密钥分发（QKD）的核心差异**

   - **题意与约定**：考察两类常因名称同含“量子”而被混为一谈的安全技术，从硬件部署、安全与信任假设、功能用途三个维度逐一对照。
   - **核心提示**：围绕硬件载体与物理链路、安全与信任假设（数学难题 vs 物理定律+经典预共享认证+可信节点）、功能用途（通用公钥/签名 vs 对称密钥协商）与距离限制全面区分 PQC 与 QKD。
   - **完整分步演算**：
     - **硬件与部署**：PQC 是纯经典数学算法（如 ML-KEM、ML-DSA），直接以软件或固件升级部署在现有服务器、终端与互联网协议（如 TLS 1.3）上；QKD 依赖专用量子光学硬件（单光子/弱相干光源、探测器、低损光纤或卫星链路），无法穿过常规经典路由器。
     - **信任假设**：PQC 的安全性建立在格、哈希或纠错码等数学难题的计算复杂度假设上，无需信任传输信道；QKD 的物理层安全基于量子不可克隆与测不准原理，但现实系统仍需对光源/探测器器件建模（诱骗态、MDI/DI-QKD），必须依赖**预先认证的经典信道**防中间人攻击，且无量子中继的长距链路往往依赖**可信中继节点**。
     - **功能用途**：PQC 同时覆盖密钥建立（KEM）与身份认证/完整性校验（数字签名）；QKD 仅能在两点间持续生成对称密钥，**不能提供数字签名或公钥身份认证**。
     - **密码工程与信任链纵深对照（第 12 章专章视角，区别于[第 0 章第 6 题](#第-0-章)的入门区分）**：① **信任边界**：QKD 并非“零前提无条件安全”，其经典公开后处理信道必须依赖预先共享的认证密钥（否则易遭中间人攻击），且在无量子中继器时跨城域组网往往被迫引入**可信中继节点**（必须信任每个中继站不被攻破）；② **标准化与混合迁移**：NIST 已于 2024 年正式发布首批 PQC 终版标准 **ML-KEM（FIPS 203）**、**ML-DSA（FIPS 204）** 与 **SLH-DSA（FIPS 205）**，工业界当前主流实践是“经典椭圆曲线 + ML-KEM”混合密钥封装，兼顾向后兼容与过渡期稳健性；③ **物理速率天花板**：点对点无中继 QKD 密钥率受光纤透射率 $\eta$ 的 PLOB 界 $C_{\mathrm{PLOB}}(\eta) = -\log_2(1-\eta)$ 刚性封顶，距离每增加 $50\ \mathrm{km}$（标准光纤损耗 $0.2\ \mathrm{dB/km}$）透射率即衰减 $10$ 倍。
   - **结论与边界回验**：PQC 是跑在经典硬件上、基于计算难题假设、兼顾密钥交换与签名的通用密码升级方案；QKD 是依赖量子光信道与器件/信任模型、仅用于协商对称密钥的物理层技术，两者定位与成本结构截然不同。
   - **易错坑提醒**：以为部署了 QKD 就不再需要 PQC，或误称 QKD 具有“绝对无条件物理安全”而忽略经典认证、探测器侧信道和可信中继节点暴露面。

2. **【基础】为何“HQC 已被 NIST 选中”不等于“HQC 已成为最终 FIPS”**

   - **题意与约定**：考察 NIST 后量子密码标准化的官方流程阶段（候选 $\to$ 选中 $\to$ 公开草案 $\to$ 最终 FIPS）与 2025–2026 年的真实标准演进史。
   - **核心提示**：区分 NIST 标准化的四个法定里程碑（入选候选 → 宣布选中 → 公开 FIPS 草案征求意见 → 正式批准发布终版 FIPS），对照 HQC 在当前周期所处的具体阶段。
   - **完整分步演算**：2025 年 3 月 11 日，NIST 在 NIST IR 8545 中选定拟循环纠错码方案 **HQC**（例如 HQC-128 公钥 $2{,}249\,\mathrm{B}$、密文 $4{,}497\,\mathrm{B}$）作为 ML-KEM 的非格类备份 KEM。但“选中”仅代表其**进入正式标准化起草流程**，后续仍须经历标准草案编写、参数与抗侧信道细节审校、全球公开征求意见及最终批准发布，截至 2026 年底尚未定稿为最终 FIPS（已发布的最终标准仅有 FIPS 203/204/205）。2026 年的真实反例进一步印证了区分阶段的必要性：额外数字签名候选 **HAWK** 于 2026 年 5 月（NIST IR 8610）晋级第 3 轮，但仅两个多月后即因循环格 Galois 自同构密钥恢复攻击于 **2026 年 7 月 29 日正式撤出第 3 轮**。
   - **结论与边界回验**：“被选中”只意味着算法晋级标准起草阶段，不等于最终 FIPS 已生效；合规与工程文档必须明确注明选中日期（2025-03-11）、当前文档状态与待定稿事实。
   - **易错坑提醒**：把仍在草案或选中阶段的方案（如 HQC、FN-DSA）和已正式发布的 FIPS 203/204/205 混写成“均已获 NIST 最终标准批准”，忽略在定稿前仍可能出现参数修订甚至撤回。

3. **【基础】纠缠交换为何既不违反不可克隆定理，也不允许超光速通信**

   - **题意与约定**：考察纠缠交换的四比特量子力学结构：它与隐形传态同构，消耗原资源态，且未收到经典结果前端点约化态与操作无关。
   - **核心提示**：把纠缠交换看作对纠缠态一半执行量子隐形传态：中间 Bell 测量消耗了原两对纠缠并破坏本地态，且在两位经典结果送达前，远端两节点联合态为最大混态 $I/4$，不携带任何可观测信号。
   - **完整分步演算**：
     - **不违反不可克隆**：中间站 Bob 对自己手里的 $B_1, B_2$ 做联合 Bell 测量，把原本独立的 $A\text{–}B_1$ 与 $B_2\text{–}C$ 两对纠缠**消耗掉**，从而在从未见面的 $A$ 与 $C$ 之间建立起一对新的纠缠。整个过程仅转移了纠缠关联，从未制造出任何未知量子态的第二份副本。
     - **不允许超光速通信**：在 Bob 尚未通过受光速限制的经典信道发来 $2$ 比特 Bell 测量结果之前，Alice 与 Charlie 手里的 $AC$ 联合态是四种等概率条件态的均匀混合：

       $$
       \rho_{AC} = \frac{1}{4}\bigl(|\Phi^+\rangle\langle\Phi^+| + |\Phi^-\rangle\langle\Phi^-| + |\Psi^+\rangle\langle\Psi^+| + |\Psi^-\rangle\langle\Psi^-|\bigr) = \frac{I_4}{4}.
       $$

       无论 Bob 是否执行测量、选择何种测量基，$AC$ 端在收到经典消息前看到的统计分布恒为完全随机的白噪声 $I_4/4$，根本无法读出任何可控信号。
   - **结论与边界回验**：纠缠交换消耗原有两对纠缠而不复制态，且端点必须等待光速传递的经典测量结果才能识别 Pauli 帧并恢复目标 Bell 态，因此同时严格遵守不可克隆定理与相对论因果律。
   - **易错坑提醒**：把“中间站测量瞬间端点 $AC$ 落入某个条件 Bell 态”误解为“远端立刻可测出物理变化，从而实现超光速传讯”。

4. **【基础】35 km 两节点实验与可扩展量子中继网络之间还缺哪些能力**

   - **题意与约定**：对照 Wehner 六阶段路线图与 2024 年波士顿 35 km 单段两节点城域实验，盘点迈向广域可扩展中继网络尚缺的核心技术积木。
   - **核心提示**：对照单段 35 km 城域演示与广域多跳中继网的差距，用光纤指数衰减 $10^{-\alpha L/10}$ 与多跳纠缠交换保真度衰减规律量化说明为何仍缺多跳交换、纯化/纠错、存储寿命与路由控制面。
   - **完整分步演算**：35 km 两节点实验验证了真实城市光纤上的单段先兆存储纠缠，但构建可扩展多跳中继网仍缺以下关键能力：① **多跳级联与高效纠缠交换**（跨越多座中继站连续接力而不跌破纠缠阈值）；② **高吞吐生成率与多路复用**（把毫赫兹级速率提升数个量级）；③ **纠缠纯化或量子纠错集成**（对抗多跳退化与存储退相干）；④ **远超等待尾分布的存取效率与存储寿命**；⑤ **低损双向量子频率转换（QFC）**；⑥ **可编程路由协议栈、实时控制面与长期高可用运维稳定性**。
     - **多跳损耗与保真度衰减量化算例**：标准电信光纤损耗约 $\alpha = 0.2\ \mathrm{dB/km}$，单段 $L = 35\ \mathrm{km}$ 透过率为 $\eta_1 = 10^{-0.2\times 35/10} = 10^{-0.7} \approx 0.1995$；若无中继直接拉长 $10$ 倍到 $350\ \mathrm{km}$，透过率暴跌至 $10^{-7}$。即便部署 $m$ 段中继做纠缠交换，若不做纠缠纯化或纠错，单跳 Werner 态保真度 $F_1 = 0.90$ 经 $m = 4$ 跳级联交换后仅剩：

       $$
       F_4 = \frac{1}{4} + \frac{3}{4}\left(\frac{4F_1 - 1}{3}\right)^4
       = 0.25 + 0.75\times\left(\frac{2.6}{3}\right)^4 \approx 0.6731,
       $$

       迅速滑向不可用的低保真区——因此“单段演示”到“多跳可扩展网络”之间必须跨过多跳交换、纯化/纠错与高并发存储三道量化门槛。
   - **结论与边界回验**：在两节点城域单段演示之外，可扩展量子中继网络还缺多跳交换级联、纯化/纠错集成、高并发纠缠产率、长寿命高效存储、实时路由控制与长期运维稳定性。
   - **易错坑提醒**：把单段两节点城域光纤纠缠误当作“广域量子互联网已经打通，只需按公里数拼接即可”。

5. **【计算】为何网络连接后的量子比特不能按芯片内全连接的成本计算**

   - **题意与约定**：对比同芯片局域耦合门与跨光学链路分布式远程门在成功概率、资源消耗和物理延迟上的数量级鸿沟。
   - **核心提示**：把芯片内数十纳秒确定性门与跨光纤远程门拆开比账：计入光纤单程传播时延 $\tau_{\mathrm{prop}}\approx 5\,\mu\mathrm{s/km}$、先兆纠缠低成功率带来的多次重试等待以及等待期间的存储退相干。
   - **完整分步演算**：同一芯片上直接耦合的双比特门可在几十纳秒至几十微秒内确定性完成；而跨越光纤网络的两个模块间执行一个远程逻辑门（如门隐形传态 `CZ`），每次都必须先**概率性**生成一对跨模块 Bell 态，经历光子损耗重试、量子存储等待与退相干、必要的多对纠缠纯化或纠错，最后再叠加经典光速往返通信（光纤单程约 $5\,\mu\mathrm{s/km}$）以完成条件 Pauli 校正。其单门时间成本和物理资源消耗比芯片内局域门高出数个数量级。
     - **跨模块远程门耗时数量级对比**：光在光纤中的单程传播时延为 $\tau_{\mathrm{prop}} = L/(c/n_{\mathrm{fiber}}) \approx 5\,\mu\mathrm{s/km}$。哪怕两台量子处理器仅相隔 $10\ \mathrm{km}$，单次门传送所需的经典往返光时就达 $100\,\mu\mathrm{s}$——相当于 **$2{,}000$ 个 $50\ \mathrm{ns}$ 超导局域双比特门**的时长！若先兆纠缠链路尝试率 $f_{\mathrm{rep}} = 1\ \mathrm{MHz}$、单次成功率 $p_{\mathrm{link}} = 10^{-3}$，仅等待一对跨模块 Bell 态就平均耗去 $1\ \mathrm{ms}$，期间工作比特还会承受 $e^{-t/T_{\mathrm{mem}}}$ 的存储退相干，因此分布式编译必须把跨模块门视为比局域门昂贵数个数量级的稀缺资源。
   - **结论与边界回验**：光学网络互联带来的是高昂的概率重试、存储退相干、纠缠消耗与经典通信延迟，“网络可达”绝不等价于“芯片内同成本全连接”，分布式编译必须极力压缩跨模块门次数。
   - **易错坑提醒**：把两台 50 比特处理器用光纤连起来就按“100 比特全连接单机”估算电路深度与运行时间。

6. **【基础】Bell 对为何不能当普通数据包处理，经典控制面至少需传递哪些元数据**

   - **题意与约定**：从量子纠缠资源的物理属性（双端共享、不可克隆、有限寿命、测量即消耗）出发，反推量子网络控制面协议栈必须追踪的最小元数据集合。
   - **核心提示**：从 Bell 对双端绑定、不可复制备份、限时退相干与测量即消耗四条物理属性出发，推导经典控制面在多跳网络中必须全程同步的 ID、槽位、超时截止与 $2m$ 比特 Pauli 帧元数据。
   - **完整分步演算**：经典数据包是局域比特串，可任意复制、缓存重传和逐跳存储转发；而一个 Bell 对是**由两个远端存储槽共同持有的非局域量子关联**——它不可克隆备份、在存储器中随时间持续退相干、且一经测量或用于门传送便立刻消耗改变。为协同管理这一易逝资源，经典控制面至少必须传递并同步：① 纠缠对全局编号（ID）；② 两端节点与具体物理存储槽地址；③ 生成时间戳与截止超时期限（cutoff）；④ 当前目标 Bell 态标签或累积 Pauli 帧；⑤ 质量/保真度估计及其标定口径；⑥ 先兆探测结果、Bell 测量两位经典结果以及失败/作废重试状态。
     - **多跳 Pauli 帧与截止期定量核算**：在 $m$ 跳串联纠缠交换路径中，每一跳中继站的 Bell 测量都随机吐出 $2$ 比特经典校正标签 $(a_j, b_j) \in \{0, 1\}^2$，整条路径共需汇集 $2m$ 比特经典控制信令并按模 $2$ 异或汇总成最终端点校正门 $X^{\bigoplus_j a_j} Z^{\bigoplus_j b_j}$；同时，若物理存储相干时间为 $T_{\mathrm{mem}}$，等待时长为 $t$ 的纠缠对保真度按 $F(t) \approx \frac{1}{4} + \frac{3}{4}(4F_0 - 1)e^{-t/T_{\mathrm{mem}}}/3$ 衰减，控制面必须据此设定严格截止期 $t_{\mathrm{cut}}$ 并自动回收超时槽位。
   - **结论与边界回验**：Bell 对是双端绑定、不可复制且限时衰变的量子资源，绝非普通数据包；经典控制面必须全程同步两端槽位、时间戳、截止期、Pauli 帧、保真度估计及先兆/交换测量结果。
   - **易错坑提醒**：误以为量子网络只需要传输光子，忽略伴随每一对纠缠的复杂经典控制面信令与精确时钟同步同样决定端到端吞吐。

7. **【计算】两条 $p = 0.1$ 并行链路（$\tau = 1\,\mathrm{ms}$）平均等待为何不是 $10\,\mathrm{ms}$**

   - **题意与约定**：考察独立同分布几何随机变量最大值 $\max(X, Y)$ 的期望计算。两条链路必须**都**成功才能做交换，因此完成轮数是 $\max(X, Y)$ 而非单链期望 $1/p$。
   - **核心提示**：记两条独立链路的成功轮数为几何随机变量 $X,Y\sim\mathrm{Geom}(p)$，用恒等式 $\max(X,Y)=X+Y-\min(X,Y)$ 并注意到 $\min(X,Y)$ 服从成功概率为 $1-(1-p)^2$ 的几何分布即可闭式求期望。
   - **完整分步演算**：设左右两段首次成功的轮数 $X, Y \in \{1, 2, \dots\}$ 独立服从成功概率 $p = 0.1$ 的几何分布，故单链期望 $\mathbb{E}[X] = \mathbb{E}[Y] = 1/p = 10$ 轮。每轮两段同时失败的概率为 $(1 - p)^2 = 0.9^2 = 0.81$，故“至少一段成功”的每轮概率为 $1 - (1 - p)^2 = 1 - 0.81 = 0.19$，从而较早成功轮数 $\min(X, Y)$ 的期望为：

     $$
     \mathbb{E}[\min(X, Y)] = \frac{1}{1 - (1 - p)^2} = \frac{1}{0.19} = \frac{100}{19} \approx 5.263\ \text{轮}.
     $$

     利用恒等式 $\max(X, Y) = X + Y - \min(X, Y)$ 取期望：

     $$
     \mathbb{E}[\max(X, Y)] = \frac{2}{p} - \frac{1}{1 - (1 - p)^2} = 20 - \frac{100}{19} = \frac{280}{19} \approx 14.737\ \text{轮}.
     $$

     乘以时隙 $\tau = 1\,\mathrm{ms}$，得平均等待时间为 **$14.74\,\mathrm{ms}$**（介于单链 $10\,\mathrm{ms}$ 与串行 $20\,\mathrm{ms}$ 之间）。
   - **结论与边界回验**：因需等待两段中较慢的那一段（$\max(X, Y)$），并行平均等待约 $14.74\,\mathrm{ms}$，而非单链平均的 $10\,\mathrm{ms}$。
   - **易错坑提醒**：想当然以为两条相同链路“并行跑”就和单条链路一样快；只要存在随机波动，两条链路总有一条滞后拖慢整体完工时刻（本模型尚未计入存储退相干、交换失败与经典往返时延）。

8. **【计算】BB84 截获再发送模型（1,000 信号）的保留数、错误数与 $25\%$ vs $12.5\%$ 分母辨析**

   - **题意与约定**：考察理想 BB84 筛选概率与截获—测量—再发送攻击的条件误差概率，重点区分“以筛选保留数为分母（QBER）”与“以总发送数为分母”两个不同统计口径。
   - **核心提示**：先按 Alice/Bob 选基一致的概率 $1/2$ 求平均保留比特数，再在一致基上按 Eve 选错基概率 $1/2$ 且重发后致错概率 $1/2$ 算出条件错误率；对比以“保留数”和以“总发送数”作分母的两个口径。
   - **完整分步演算**：Alice、Bob 与 Eve 各自独立等概率选 $Z$ 基或 $X$ 基：
     1. **平均筛选保留数**：Alice 与 Bob 选到同一基的概率为 $1/2$，故 $1{,}000$ 个信号平均保留 $1{,}000 \times \frac{1}{2} = 500$ 个比特。
     2. **平均错误数与 QBER**：在保留比特中，Eve 猜错基的概率为 $1/2$；一旦 Eve 用错基测量再重发（如把 $|0\rangle$ 测成 $|+\rangle$ 或 $|-\rangle$ 重发），Bob 用原基测量得到错误比特的概率为 $|\langle 1|\pm\rangle|^2 = 1/2$。因此保留序列的量子比特错误率（QBER）为：

        $$
        Q = \frac{1}{2} \times \frac{1}{2} = \frac{1}{4} = 25\%,
        $$

        平均出错个数为 $500 \times \frac{1}{4} = 125$ 个。
     3. **双分母对比**：$125 / 500 = 25\%$ 的分母是**筛选保留数**（标准 QBER 定义）；$125 / 1{,}000 = 12.5\%$ 的分母是**总发送信号数**，衡量的是“既被保留又出错”占总发送脉冲的比例。
   - **结论与边界回验**：$1{,}000$ 个信号平均保留 $500$ 个、其中平均错 $125$ 个；$25\%$ 与 $12.5\%$ 分别以“保留比特数”和“总发送信号数”为分母，不是同一个错误率定义。
   - **易错坑提醒**：混用两个分母把 $12.5\%$ 当成 QBER，或把理论期望 $500/125$ 当成单批 $1{,}000$ 次实验必定恰好出现的确定计数。

9. **【计算】公开抽查 $20$ 个保留比特零错误能否证明无窃听，及 $25\%$ 为何不是安全阈值**

   - **题意与约定**：考察独立抽样漏检概率 $(1 - Q)^k$ 的精确计算，以及单向后处理 BB84 安全门槛（$11\%$）与全量截获再发送误码率（$25\%$）之间的根本区别。
   - **核心提示**：在单比特错误率 $Q=1/4$ 下，连续 $k=20$ 次独立抽查全无错误的漏检概率为 $(1-Q)^k$；第二问对照单向 BB84 的 Shor–Preskill 阈值 $Q_{\max}\approx 11\%$ 与拦截重发特征值 $25\%$ 的含义区别。
   - **完整分步演算**：在全量截获再发送模型中，每个保留比特侥幸未出错的概率为 $1 - \frac{1}{4} = \frac{3}{4} = 0.75$。独立抽查 $20$ 个保留比特全部零错误的概率为：

     $$
     P(\text{20 比特全无错}) = \left(\frac{3}{4}\right)^{20} = 0.75^{20} \approx 0.003171 \quad (\text{约 } 0.317\%).
     $$

     该漏检概率虽小但严格大于零，因此 $20$ 比特零错误绝不能“证明”绝对没有窃听。同时，$25\%$ 只是 Eve 拦截全部光子的最粗糙攻击留下的印记：若 Eve 仅随机拦截比例 $f$ 的光子，QBER 立即降至 $Q = f/4$；而且按 Shor–Preskill 公式 $1 - 2h_2(Q)$，单向后处理理想 BB84 的安全密钥率在 $Q \approx 11.0\%$ 时就已经归零，远低于 $25\%$！
   - **结论与边界回验**：不能证明没有窃听，该模型下 $20$ 比特漏检概率约为 $0.00317$；$25\%$ 绝非安全门槛，完整安全结论还取决于光源/器件模型、有限长参数估计、经典认证与后处理（公开抽查过的 $20$ 比特须立刻作废，不可作密钥）。
   - **易错坑提醒**：误以为“只要测出的误码率低于 $25\%$ 就说明没有窃听、可以直接提取安全密钥”。

10. **【进阶】双链等待的总完成时间、额外存储时间与平均相干因子的 Jensen 差异**

    - **题意与约定**：区分随机变量 $\max(X, Y)$ 与 $D = |X - Y|$，用几何差分布闭式求和精确计算 $\mathbb{E}[e^{-D\tau/T_{\mathrm{mem}}}]$，并用凸函数 Jensen 不等式解释为何不能直接把 $\mathbb{E}[D]$ 代入指数。
    - **核心提示**：先明确总完成轮数为 $\max(X,Y)$、先成链的等待差为 $D=|X-Y|$，再用严格凸函数 $f(d)=e^{-d\tau/T_{\mathrm{mem}}}$ 的 Jensen 不等式 $\mathbb E[f(D)]>f(\mathbb E[D])$ 解释为何不能直接代入平均等待时间。
    - **完整分步演算**：记单轮成功概率 $p = 0.1,\ q = 1 - p = 0.9$，时隙 $\tau = 1\,\mathrm{ms}$，有效相干时间 $T_{\mathrm{mem}} = 20\,\mathrm{ms}$。
      1. **两个随机变量**：总完成轮数为 $\max(X, Y)$（期望 $\approx 14.74\,\mathrm{ms}$）；较早成功那一对的额外存储轮数为 $D = |X - Y| = X + Y - 2\min(X, Y)$，其期望存储时间为：

         $$
         \mathbb{E}[D]\tau = \left(\frac{2}{p} - \frac{2}{1 - q^2}\right)\tau = \left(20 - \frac{200}{19}\right)\mathrm{ms} = \frac{180}{19}\,\mathrm{ms} \approx 9.474\,\mathrm{ms}.
         $$

      2. **直接代入均值的错误结果**：$e^{-\mathbb{E}[D]\tau / T_{\mathrm{mem}}} = e^{-9.4737 / 20} \approx 0.6227 \approx 0.623$。
      3. **按 $D$ 精确分布求平均相干因子**：由 $\Pr(D = 0) = \frac{p}{2 - p}$ 与 $\Pr(D = d) = \frac{2pq^d}{2 - p}$（$d \ge 1$），令单时隙保留因子 $a = e^{-\tau/T_{\mathrm{mem}}} = e^{-1/20} \approx 0.95123$（得 $qa \approx 0.85611$）：

         $$
         \overline{C} = \mathbb{E}\bigl[e^{-D\tau/T_{\mathrm{mem}}}\bigr]
         = \frac{p}{2 - p}\left(1 + 2\sum_{d=1}^{\infty}(qa)^d\right)
         = \frac{p}{2 - p}\cdot\frac{1 + qa}{1 - qa}
         = \frac{0.1}{1.9}\times\frac{1.85611}{0.14389} \approx 0.6789 \approx 0.679.
         $$

         因为 $f(t) = e^{-t/T_{\mathrm{mem}}}$ 是严格凸函数，按 Jensen 不等式必有 $\mathbb{E}[f(D\tau)] > f(\mathbb{E}[D]\tau)$（$0.679 > 0.623$）。
    - **结论与边界回验**：总完成时间对应 $\max(X, Y)$，额外存储时间对应 $D = |X - Y|$（平均约 $9.47\,\mathrm{ms}$）；因指数衰减严格凸，精确平均相干因子为 $0.679$，不能用直接代入均值得到的 $0.623$ 代替（且纯退相位下对应 Bell 重叠为 $(1 + \overline{C})/2 \approx (1 + 0.6789)/2 \approx 0.839$，并非保真度掉到 $0.679$）。
    - **易错坑提醒**：不仅容易把 $\max(X, Y)$ 错当存储时长、把均值直接塞进非线性指数函数，还常把非对角相干因子 $\overline{C}$ 直接错当成态重叠或根保真度。

11. **【计算】纠缠交换测得 $|\Psi^-\rangle$ 时的条件态、概率、Pauli 修正与非选择平均态**

    - **题意与约定**：利用四比特初态在中间 Bell 基下的精确展开直接读出 $|\Psi^-\rangle$ 分支，严格按“从右向左作用”顺序验证校正门 $I \otimes ZX$，并求和得到忽略结果时的混合态。
    - **核心提示**：把两对初态 $|\Phi^+\rangle_{12}|\Phi^+\rangle_{34}$ 改写到中间两比特 $(2,3)$ 的四个 Bell 基展开式，读出 $|\Psi^-\rangle_{23}$ 分支对应的端点态 $(1,4)$ 与概率 $1/4$，再按从右向左作用验证还原门，并对四个分支求无条件平均。
    - **完整分步演算**：将 $|\Omega\rangle_{AB_1 B_2 C} = |\Phi^+\rangle_{AB_1}\otimes|\Phi^+\rangle_{B_2 C}$ 改写到 $B_1 B_2$ 的 Bell 基下：

      $$
      |\Omega\rangle_{AB_1 B_2 C} = \frac{1}{2}\Bigl(|\Phi^+\rangle_{B_1 B_2}|\Phi^+\rangle_{AC} + |\Phi^-\rangle_{B_1 B_2}|\Phi^-\rangle_{AC} + |\Psi^+\rangle_{B_1 B_2}|\Psi^+\rangle_{AC} + |\Psi^-\rangle_{B_1 B_2}|\Psi^-\rangle_{AC}\Bigr).
      $$

      - **条件态与概率**：测得 $|\Psi^-\rangle_{B_1 B_2}$ 的未归一化投影为 $\frac{1}{2}|\Psi^-\rangle_{AC}$，故出现概率为 $|1/2|^2 = 1/4$，归一化条件态为 $|\Psi^-\rangle_{AC} = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$。
      - **在 $C$ 端恢复 $+\,|\Phi^+\rangle$（先 $X$ 后 $Z$，即 $I \otimes ZX$）**：

        $$
        (I \otimes X)\frac{|01\rangle - |10\rangle}{\sqrt{2}} = \frac{|00\rangle - |11\rangle}{\sqrt{2}} = |\Phi^-\rangle, \qquad
        (I \otimes Z)\frac{|00\rangle - |11\rangle}{\sqrt{2}} = \frac{|00\rangle + |11\rangle}{\sqrt{2}} = +|\Phi^+\rangle.
        $$

        （若反序作用 $I \otimes XZ$，因 $XZ = -ZX$ 得 $-|\Phi^+\rangle$，物理态相同但多一个全局负号。）
      - **忽略结果且不修正的非选择态**：四正交 Bell 态各占 $1/4$ 权重混合，由完备性得 $\rho_{AC} = \frac{1}{4}\sum_{\beta}|\beta\rangle\langle\beta| = I_4/4$。
    - **结论与边界回验**：端点条件态为 $|\Psi^-\rangle_{AC}$，概率 $1/4$，在 $C$ 端施加 $ZX$（先 $X$ 后 $Z$）精确恢复为 $+|\Phi^+\rangle_{AC}$；忽略结果且不修正时，端点联合态退化为无纠缠最大混态 $I_4/4$。
    - **易错坑提醒**：把知道经典结果后的条件纠缠态与未获知结果的无条件平均态 $I_4/4$ 混为一谈，或在验证 $ZX$ 时弄反算符“从右向左”的作用顺序。

12. **【计算】$N = 15,\, a = 2$ 的模幂周期序列与平方差求因子原理**

    - **题意与约定**：逐项计算 $2^x \bmod 15$ 找出周期 $r$，再借助代数因式分解 $a^r - 1 = (a^{r/2} - 1)(a^{r/2} + 1)$ 说明为何分别对两括号求最大公因数可拆出非平凡因子。
    - **核心提示**：逐次计算 $2^1,2^2,\dots\bmod 15$ 得到周期 $r$；再利用 $a^r-1=(a^{r/2}-1)(a^{r/2}+1)$ 是 $N$ 的倍数且两因子均不为 $N$ 的倍数，说明各自与 $N$ 的最大公因数必抽出非平凡因子。
    - **完整分步演算**：从 $x = 0$ 起逐项取模 $15$：
      - $2^0 \bmod 15 = 1$，$2^1 \bmod 15 = 2$，$2^2 \bmod 15 = 4$，$2^3 \bmod 15 = 8$，$2^4 = 16 \equiv 1 \pmod{15}$。

      首次回到 $1$ 给出最小正周期 $r = 4$。因为 $r = 4$ 为偶数，将 $2^4 - 1 \equiv 0 \pmod{15}$ 做平方差分解：

      $$
      2^4 - 1 = (2^2 - 1)(2^2 + 1) = (4 - 1)(4 + 1) = 3 \times 5 \equiv 0 \pmod{15}.
      $$

      因 $r = 4$ 是最小周期，$15$ 不整除 $2^2 - 1 = 3$；又因 $2^2 = 4 \not\equiv -1 \pmod{15}$，$15$ 也不整除 $2^2 + 1 = 5$。因此 $15$ 的非平凡因子必然分别落入两个括号中，用欧几里得算法立得 $\gcd(3, 15) = 3$、$\gcd(5, 15) = 5$。
    - **结论与边界回验**：余数序列为 $1, 2, 4, 8, 1$，周期 $r = 4$；因 $15$ 整除 $(2^{r/2}-1)(2^{r/2}+1)$ 却不单独整除任一因子，分别计算 $\gcd(3, 15) = 3$ 与 $\gcd(5, 15) = 5$ 即拆出非平凡因子。
    - **易错坑提醒**：误以为 Shor 算法的量子加速发生在求 $\gcd$ 或列小表步骤上；实际量子加速仅针对大整数下经典难以穷举的“周期 $r$ 查找”环节，欧几里得求 $\gcd$ 本身就是多项式经典算法。

13. **【基础】ML-KEM 建立共享秘密的三箭头流程与公钥认证必要性**

    - **题意与约定**：梳理标准 KEM（FIPS 203 ML-KEM）三步抽象消息流，区分“封装密文 $c$”与“业务数据密文”，并说明公钥认证与隐式拒绝的工程衔接。
    - **核心提示**：按 KeyGen、Encaps、Decaps 三步画清接收方与发送方的消息流向（区分封装密文 $c$ 与对称加密业务密文），再从中间人替换公钥的攻击路径说明公钥认证的必要性。
    - **完整分步演算**：用三个箭头精确写出接收方（Bob）与发送方（Alice）建立共享秘密 $K$（恒为 $32\,\mathrm{B}$）的抽象流程：
      1. **密钥生成与公钥分发**：接收方运行 $\mathrm{KeyGen}() \to (\mathrm{pk}, \mathrm{sk})$，本地严密保管私钥 $\mathrm{sk}$，发送公钥：$\text{接收方} \xrightarrow{\ \mathrm{pk}\ } \text{发送方}$；
      2. **封装与发送密文**：发送方运行 $\mathrm{Encaps}(\mathrm{pk}) \to (c, K)$，本地保留共享秘密 $K$，发送封装密文：$\text{发送方} \xrightarrow{\ c\ } \text{接收方}$；
      3. **本地解封装恢复秘密**：接收方运行 $\mathrm{Decaps}(\mathrm{sk}, c) \longrightarrow K$，得到同一把共享秘密 $K$（再交给 AES 等对称密码加密业务数据）。

      **为何仍须认证公钥**：若攻击者在第一步把 $\mathrm{pk}$ 偷换为自己的公钥 $\mathrm{pk}_{\mathrm{Eve}}$，发送方就会毫无察觉地与攻击者协商出共享秘密（中间人攻击）；此外，FIPS 203 采用**隐式拒绝**机制——即使密文 $c$ 被篡改，解封装也不会报错，而是静默返回伪随机替代秘密，因此身份认证与密钥确认必须由上层协议（如证书链与 TLS 1.3 握手校验）共同完成。
    - **结论与边界回验**：三箭头依次为接收方生成并发送 $\mathrm{pk}$、发送方封装并回传密文 $c$、接收方用 $\mathrm{sk}$ 解封装还原 $K$；必须独立认证公钥（如通过数字签名证书）才能防止中间人替换公钥。
    - **易错坑提醒**：把封装密文 $c$ 误当成加密后的业务文件，或以为 ML-KEM 解封装接口“返回成功”就证明密文未被篡改且对方身份合法。

14. **【计算】BB84 对称误码 $e_b = e_p = 0.05$ 的 Shor–Preskill 密钥率与有限样本陷阱**

    - **题意与约定**：按二元香农熵 $h_2(x) = -x\log_2 x - (1-x)\log_2(1-x)$ 逐项精确计算渐近安全密钥率下界 $1 - 2h_2(0.05)$，再对照有限长公式说明为何不能直接乘 $10{,}000$ 报产量。
    - **核心提示**：把 $x=0.05$ 代入二元香农熵 $h_2(x)=-x\log_2 x-(1-x)\log_2(1-x)$ 算渐近密钥率 $1-2h_2(0.05)$；第二问列出有限块长下抽样统计误差、信息协调泄露与隐私放大平滑参数带来的扣减项。
    - **完整分步演算**：令 $Q = 0.05$（$1 - Q = 0.95$），逐项计算以 $2$ 为底的对数项（$\log_2(0.05) \approx -4.321928$，$\log_2(0.95) \approx -0.074001$）：

      $$
      -0.05\log_2(0.05) \approx 0.216096, \qquad
      -0.95\log_2(0.95) \approx 0.070301,
      $$

      $$
      h_2(0.05) \approx 0.216096 + 0.070301 = 0.286397,
      $$

      $$
      1 - 2h_2(0.05) \approx 1 - 2 \times 0.286397 = 1 - 0.572794 = 0.427206.
      $$

      直接乘以 $10{,}000$ 虽约为 $4{,}272$，但该式仅在渐近无穷长、理想单光子与理想纠错（$f_{\mathrm{EC}} = 1$）下成立。现实有限块长须满足 $\ell \le n_1^z[1 - h_2(\phi_1^u)] - \mathrm{leak}_{\mathrm{EC}} - \Delta(\varepsilon)$：须扣除抽样估计相位错误率上界 $\phi_1^u$ 的有限统计波动、实际信息协调冗余（$f_{\mathrm{EC}} > 1$）、经典认证密钥消耗、有限长安全修正项 $\Delta(\varepsilon)$ 及弱相干光源多光子修正，且 $10{,}000$ 个筛选比特对有限长参数估计往往过小，最终安全长度可能大幅缩水甚至归零。
    - **结论与边界回验**：$h_2(0.05) \approx 0.286397$，$1 - 2h_2(0.05) \approx 0.427206$；现实中仅有 $10{,}000$ 个筛选比特时，**不能**直接宣称产出 $4{,}272$ 个可证明安全的密钥比特。
    - **易错坑提醒**：错用自然对数 $\ln$ 算二元熵（会漏除 $\ln 2$），或者把渐近密钥率直接乘以有限块长（甚至把总发送光子数混成筛选比特数）来夸大安全密钥产量。

15. **【基础】2024 年波士顿 $35\,\mathrm{km}$ 城域实验与 2025 年 $2\,\mathrm{m}$ 跨模块门实验的口径边界**

    - **题意与约定**：考察真实量子网络顶刊报道中的两处高频口径偷换：跨子实验张冠李戴速率，以及把协议后半步的“确定性”外推成整条链路的“确定性”。
    - **核心提示**：分别核对两篇实验报道的精确分母与阶段边界：城域实验中不同子任务（光子探测率 vs 核自旋端到端纠缠率）不可混拼；跨模块门中的“确定性”发生在先兆 Bell 对已就绪之后的门传送步骤。
    - **完整分步演算**：
      1. **波士顿 35 km 实验（Knaut 等，*Nature* 629, 2024）**：论文里“最高约 $1\,\mathrm{Hz}$”指的是不同条件下的短距电子自旋纠缠，**不是** $35\,\mathrm{km}$ 城域光纤上 $^{29}\mathrm{Si}$ 核自旋存储器的纠缠生成率。据原论文数据，$35\,\mathrm{km}$ 城域核自旋纠缠的原始平均速率仅约 $0.23\,\mathrm{mHz} = 2.3\times 10^{-4}\,\mathrm{s}^{-1}$，平均每生成一对的等待间隔为：

         $$
         \bar{T} = \frac{1}{2.3\times 10^{-4}\,\mathrm{s}^{-1}} \approx 4{,}348\,\mathrm{s} \approx 72.5\,\mathrm{min},
         $$

         经过片上错误检测筛选后的速率更低至约 $0.10\,\mathrm{mHz}$。
      2. **牛津 2 m 跨模块逻辑门（Main 等，*Nature* 638, 2025）**：实验先通过光学链路**概率性**地生成跨模块远程 Bell 对；“确定性”严格**限定在已经拿到先兆确认的远程 Bell 对之后、执行门隐形传态 `CZ` 门的那一步**（不靠挑拣有利的门测量结果后选择），绝不代表光子纠缠尝试次次成功，也尚未推广到城域距离。
    - **结论与边界回验**：$1\,\mathrm{Hz}$ 不能张冠李戴为波士顿 $35\,\mathrm{km}$ 核自旋纠缠率（实测约 $0.23\,\mathrm{mHz}$、约 $72.5$ 分钟一对）；牛津实验的“确定性”仅限于拿到远程 Bell 对后的 `CZ` 门传送步骤。
    - **易错坑提醒**：只摘取论文摘要里最亮眼的单个数字或定语（“$1\,\mathrm{Hz}$”“确定性”），不核对正文与补充表格里该指标对应的具体子实验条件和分母。

16. **【计算】模 $q = 17$ 二维 LWE 加解密、噪声越界误判与 Shor 失效原因**

    - **题意与约定**：沿用第 12 章 §2.3 的模 $17$ 格密码参数（$m = 0 \mapsto 0,\, m = 1 \mapsto \lfloor 17/2\rfloor = 8$；因 $q = 17$ 为奇数、$0$ 与 $8$ 的中点恰落在整数 $4$，判决区 $m = 0$ 容忍 $w \in [-4, 4]$、$m = 1$ 容忍 $w \in [-3, 4]$，在 $w = -4$ 处会与 $(m = 0, w = +4)$ 等距碰撞，故对两比特均无歧义的对称充分容错界为 $|w| \le 3$），零跳步完成两组误差下的加密 $(u, v)$、残余噪声 $w = e^T r + e_2 - s^T e_1$ 与解密差值 $(v - s^T u)\bmod 17$ 验算，再从群周期与规约复杂度两层解释 Shor 为何无法攻破 LWE。
    - **核心提示**：严格按模 $17$ 矩阵向量乘法计算密文 $(u,v)=(A^T r+e_1,\; b^T r+e_2+8m)\bmod 17$，解密时算 $v-s^T u\bmod 17$ 并判断它离 $0$ 还是离 $8$ 更近；再结合带噪声项破坏周期结构说明 Shor 为何失效。
    - **完整分步演算**：由题给 $A = \begin{bmatrix}5 & 11\\ 9 & 4\end{bmatrix}$、$s = [1, -1]^T$、$e = [1, -1]^T$、$b = [12, 4]^T$，先写出转置 $A^T = \begin{bmatrix}5 & 9\\ 11 & 4\end{bmatrix}$，并计算公共项（$r = [0, 1]^T$）：

      $$
      A^T r = \begin{bmatrix}5(0) + 9(1)\\ 11(0) + 4(1)\end{bmatrix} = \begin{bmatrix}9\\ 4\end{bmatrix}, \qquad
      b^T r = 12(0) + 4(1) = 4, \qquad
      e^T r = 1(0) + (-1)(1) = -1.
      $$

      - **（a）$e_1 = [1, 0]^T,\ e_2 = 1,\ m = 1$**：
        1. 密文：$u = (A^T r + e_1)\bmod 17 = [9 + 1,\, 4 + 0]^T \bmod 17 = [10, 4]^T$；$v = (b^T r + e_2 + 8m)\bmod 17 = (4 + 1 + 8)\bmod 17 = 13$。
        2. 残余噪声：$s^T e_1 = 1(1) + (-1)(0) = 1$，故 $w = e^T r + e_2 - s^T e_1 = (-1) + 1 - 1 = -1$，满足对称无歧义充分界 $|w| = 1 \le 3$（落入 $m = 1$ 的容错区间 $[-3, 4]$）。
        3. 解密差值：$s^T u = 1(10) + (-1)(4) = 6 \pmod{17}$，得 $(v - s^T u)\bmod 17 = (13 - 6)\bmod 17 = 7$（独立回验 $(8m + w)\bmod 17 = 8 - 1 = 7$）。在模 $17$ 圆环上，$7$ 距 $8$ 仅 $1$ 步、距 $0$ 有 $7$ 步，**正确解码为 $m = 1$**。
      - **（b）$e_1 = [-2, 2]^T,\ e_2 = 2,\ m = 0$**：
        1. 密文：$u = ([9, 4]^T + [-2, 2]^T)\bmod 17 = [7, 6]^T$；$v = (4 + 2 + 0)\bmod 17 = 6$。
        2. 残余噪声：$s^T e_1 = 1(-2) + (-1)(2) = -4$，故 $w = (-1) + 2 - (-4) = +5$，**越界** $w = +5 \notin [-4, 4]$（更超出对称充分界 $|w| \le 3$）！
        3. 解密差值：$s^T u = 1(7) + (-1)(6) = 1 \pmod{17}$，得 $(v - s^T u)\bmod 17 = (6 - 1)\bmod 17 = 5$（回验 $8(0) + 5 = 5$）。在模 $17$ 圆环上，$5$ 距 $8$ 仅 $3$ 步，小于距 $0$ 的 $5$ 步，**被误判为 $m = 1$**（因过大噪声与私钥内积 $-s^T e_1 = +4$ 将 $w$ 推过 $0$ 与 $8$ 的整数中点 $4$）。
      - **Shor 为何无法攻破 LWE**：Shor 依赖阿贝尔群隐藏子群问题（Abelian HSP）的严格全局周期 $f(x + r) = f(x)$ 借 QFT 相长干涉；LWE 样本 $b = As + e$ 中的随机噪声 $e$ 彻底打碎了严格周期性，其格问题量子规约落入非阿贝尔二面体群 $D_N$-HSP，已知最优量子算法（Kuperberg 筛法）为亚指数级 $2^{O(\sqrt{n})}$ 而非多项式时间。
    - **结论与边界回验**：（a）$u = [10, 4]^T,\, v = 13,\, w = -1,\, (v - s^T u)\bmod 17 = 7$，正确解码为 $1$；（b）$u = [7, 6]^T,\, v = 6,\, w = +5,\, (v - s^T u)\bmod 17 = 5$，因 $w = +5$ 越过 $m = 0$ 容错区间 $[-4, 4]$（及对称界 $|w| \le 3$）误判为 $1$；噪声破坏严格阿贝尔周期使 Shor 失效。
    - **易错坑提醒**：计算 $w = e^T r + e_2 - s^T e_1$ 时漏掉 $-s^T e_1$ 的负号（会误把（b）的 $w$ 算成 $-3$），或忘在模 $17$ 圆环上取最短圆周距离 $\min(d, 17 - d)$。

17. **【计算】$1{,}000\,\mathrm{km}$ 光纤三代量子中继时延对比与 3G 纯光纤最大站距推导**

    - **题意与约定**：考察三代量子中继器（1G/2G/3G）在经典往返时延（RTT）上的量级跃迁，并由不可克隆定理导出的单向量子擦除信道容量零界 $Q(\mathcal{E}_p) = \max(0, 1 - 2p) > 0$ 严格推导 3G 中继最大单跳间距。
    - **核心提示**：用单程光时 $L/c_f$ 核算 1G（端到端经典往返）、2G（相邻站单跳经典往返）与 3G（单向编码无等待）的时延量级；再用量子擦除容量零界 $1-2p_{\mathrm{loss}}>0\iff \eta>1/2$ 解出 $10^{-\alpha d/10}>1/2$ 的最大站距 $d$。
    - **完整分步演算**：已知总长 $L = 1{,}000\,\mathrm{km}$、光纤光速 $c_f = 2\times 10^5\,\mathrm{km/s}$、衰减 $a = 0.2\,\mathrm{dB/km}$：
      1. **第一代中继（1G，端到端双向纯化回执）**：

         $$
         T_{\mathrm{RTT}}^{\mathrm{1G}} = \frac{2L}{c_f} = \frac{2 \times 1{,}000\,\mathrm{km}}{2\times 10^5\,\mathrm{km/s}} = 0.01\,\mathrm{s} = 10\,\mathrm{ms},
         $$

         单通道最高速率被光速锁死在 $1/(10\,\mathrm{ms}) = 100\,\mathrm{Hz}$ 以下。
      2. **第二代中继（2G，邻站 $L_0 = 20\,\mathrm{km}$ 双向先兆 + 端到端单向纠错）**：

         $$
         T_{\mathrm{RTT}}^{\mathrm{2G}} = \frac{2L_0}{c_f} = \frac{2 \times 20\,\mathrm{km}}{2\times 10^5\,\mathrm{km/s}} = 2\times 10^{-4}\,\mathrm{s} = 0.2\,\mathrm{ms} = 200\,\mu\mathrm{s},
         $$

         周期比 1G 缩短 **$50$ 倍**（单通道速率上限提至 $5\,\mathrm{kHz}$ 级）。
      3. **第三代中继（3G，纯单向抗擦除编码转发）**：彻底取消往返等待，周期仅受本地逻辑门时长 $t_{\mathrm{local}} \approx 1\,\mu\mathrm{s}$ 限制，比 2G 再快 **$200$ 倍**、比 1G 快整整 **$10^4$ 倍**（可达 $\mathrm{MHz}$ 级）。
      4. **3G 最大单跳站距理论上限**：由量子擦除容量 $Q(\mathcal{E}_p) = \max(0, 1 - 2p)$，无双向反馈的单向量子纠错能容忍的总光子丢失率必须严格满足 $p < 50\%$，即单跳总透过率 $\eta = 1 - p > 0.5$。换算为分贝损耗上限（以 $10$ 为底对数）：

         $$
         \text{最大允许损耗} = -10\log_{10}(0.5) = 10\log_{10} 2 \approx 3.0103\,\mathrm{dB}.
         $$

         在理想零器件损耗的纯光纤（$a = 0.2\,\mathrm{dB/km}$）中，最大理论站距为：

         $$
         L_0^{\max} = \frac{3.0103\,\mathrm{dB}}{0.2\,\mathrm{dB/km}} \approx 15.05\,\mathrm{km}.
         $$

    - **结论与边界回验**：三代周期时延依次为 $10\,\mathrm{ms}$（1G）、$0.2\,\mathrm{ms}$（2G，快 $50\times$）与约 $1\,\mu\mathrm{s}$（3G，快 $10^4\times$）；受 $50\%$ 擦除容量硬阈值限制，3G 在 $0.2\,\mathrm{dB/km}$ 理想纯光纤下的最大单跳站距上限仅为 $15.05\,\mathrm{km}$。
    - **易错坑提醒**：计算往返时延（RTT）时忘乘 $2$（错算成单程 $5\,\mathrm{ms}$ 与 $0.1\,\mathrm{ms}$），或误把 $15.05\,\mathrm{km}$ 当成现实可建的 3G 站距——计入发射、耦合、频率转换与探测损耗后，真实 3G 中继站必须密布到每隔 $1\text{--}5\,\mathrm{km}$ 一座。

## 第 13 章

> 对应章节：《13｜量子信息量度：熵、距离与可提取信息》（共 6 题）

1. **【基础】计算对角密度矩阵 $\rho = \operatorname{diag}(0.8, 0.2)$ 的 von Neumann 熵**

   - **题意与约定**：给定二维希尔伯特空间 $\mathbb{C}^2$ 上的单量子比特密度矩阵 $\rho = \begin{bmatrix} 0.8 & 0 \\ 0 & 0.2 \end{bmatrix}$，求其 von Neumann 熵 $S(\rho) = -\operatorname{Tr}(\rho\log_2\rho)$（单位：$\mathrm{bit}$）。对任意密度矩阵求熵，必须先求其本征值谱 $\{\lambda_j\}$，再把各非零本征值代入香农熵公式 $-\sum_j \lambda_j \log_2 \lambda_j$（约定 $0\log_2 0 = 0$）。本题矩阵已处于对角形式，对角元就是全部本征值。
   - **核心提示**：对角密度矩阵的本征值直接就是主对角元，代入 von Neumann 熵定义 $S(\rho)=-\sum_j\lambda_j\log_2\lambda_j$（注意以 $2$ 为底、单位 $\mathrm{bit}$）逐项计算即可。
   - **完整分步演算**：先核验合法性——两个对角元 $\lambda_1 = 0.8 > 0$、$\lambda_2 = 0.2 > 0$ 均非负，且迹 $\operatorname{Tr}(\rho) = 0.8 + 0.2 = 1$，故 $\rho$ 是合法密度矩阵。按对数底数约定统一采用 $\log_2$，代入二元香农熵 $h_2(p) = -p\log_2 p - (1-p)\log_2(1-p)$ 逐步展开：

     $$
     \begin{aligned}
     S(\rho)
     &= -\operatorname{Tr}(\rho\log_2\rho)
      = -\lambda_1\log_2\lambda_1 - \lambda_2\log_2\lambda_2 \\
     &= -0.8\log_2(0.8) - 0.2\log_2(0.2).
     \end{aligned}
     $$

     利用换底公式 $\log_2 x = \frac{\ln x}{\ln 2}$（其中 $\ln 2 \approx 0.69314718$）逐项算出两个对数：

     $$
     \log_2(0.8) = \log_2\!\left(\frac{4}{5}\right) = 2 - \log_2 5 \approx 2 - 2.32192809 = -0.32192809,
     $$

     $$
     \log_2(0.2) = \log_2\!\left(\frac{1}{5}\right) = -\log_2 5 \approx -2.32192809.
     $$

     两项分别乘以概率权重再求和：

     $$
     \begin{aligned}
     S(\rho)
     &\approx -0.8 \times (-0.32192809) - 0.2 \times (-2.32192809) \\
     &\approx 0.25754248 + 0.46438562
      = 0.72192809\ \mathrm{bit} \approx 0.722\ \mathrm{bit}.
     \end{aligned}
     $$

     边界回验：纯态熵为 $0$，单量子比特最大混态 $I/2$ 的熵为 $\log_2 2 = 1\ \mathrm{bit}$；本例处于两者之间，$0 < 0.7219 < 1$，完全自洽。结合正文第 1.3 节 Schumacher 量子压缩定理，该值正是该信源的渐近无损压缩率下界（例如正文对非正交信源 $\{|0\rangle,|+\rangle\}$ 取 $n=3$ 份压入 $2$ 比特的 8 维手算中，单份熵 $S(\rho)\approx 0.6009 < 2/3$，典型子空间权重 $p_{\mathrm{typ}}\approx 0.9419$，需严格区分平均码字根保真度 $\bar F = \sqrt{p_{\mathrm{typ}}^2 + \lambda_+^3(1-p_{\mathrm{typ}})} \approx 0.9609$ 与纠缠根保真度 $F_e = p_{\mathrm{typ}} \approx 0.9419$）。
   - **结论与边界回验**：$\rho = \operatorname{diag}(0.8, 0.2)$ 的 von Neumann 熵为 $S(\rho) = h_2(0.2) \approx 0.7219\ \mathrm{bit}$（约 $0.722\ \mathrm{bit}$）。
   - **易错坑提醒**：切忌把普通自然对数 $\ln$（算得约 $0.5004\ \mathrm{nat}$）直接标成 $\mathrm{bit}$；对一般非对角密度矩阵，更不可对每个矩阵元分别取 $\log_2$，必须先对角化求本征值。

2. **【计算】对比 Bell 态与经典相关混态的联合熵 $S(AB)$、条件熵 $S(A\mid B)$ 与互信息 $I(A:B)$**

   - **题意与约定**：在两量子比特四维空间 $\mathbb{C}^2_A \otimes \mathbb{C}^2_B$（大端基序 $|00\rangle, |01\rangle, |10\rangle, |11\rangle$）中，分别考察最大纠缠 Bell 纯态 $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$（密度矩阵 $\rho_{\Phi^+} = |\Phi^+\rangle\langle\Phi^+|$）和经典相关混态 $\rho_{\mathrm{cl}} = \frac{1}{2}|00\rangle\langle 00| + \frac{1}{2}|11\rangle\langle 11|$。先逐项写出整体态与偏迹约化态的本征值谱，再套用量子条件熵 $S(A\mid B) = S(AB) - S(B)$ 与量子互信息 $I(A:B) = S(A) + S(B) - S(AB)$。
   - **核心提示**：先分别求出两态的联合密度矩阵本征值与单比特约化态本征值，算出 $S(AB),S(A),S(B)$，再代入量子条件熵 $S(A\mid B)=S(AB)-S(B)$ 与互信息 $I(A:B)=S(A)+S(B)-S(AB)$，留意 Bell 态条件熵的符号。
   - **完整分步演算**：
     - **情形一：Bell 态 $|\Phi^+\rangle$**。写出 $4\times 4$ 密度矩阵并验证偏迹：

       $$
       \rho_{\Phi^+} = \frac{1}{2}\begin{bmatrix}
       1 & 0 & 0 & 1 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       1 & 0 & 0 & 1
       \end{bmatrix}.
       $$

       因 $\rho_{\Phi^+}$ 是秩 $1$ 纯态投影，其本征值为 $\{1, 0, 0, 0\}$，故整体熵 $S(AB) = -1\log_2 1 = 0\ \mathrm{bit}$。对子系统 $B$ 做偏迹：

       $$
       \rho_A = \operatorname{Tr}_B(\rho_{\Phi^+})
       = \frac{1}{2}\Big(\langle 0|0\rangle|0\rangle\langle 0| + \langle 1|0\rangle|0\rangle\langle 1| + \langle 0|1\rangle|1\rangle\langle 0| + \langle 1|1\rangle|1\rangle\langle 1|\Big)
       = \frac{1}{2}\bigl(|0\rangle\langle 0| + |1\rangle\langle 1|\bigr) = \frac{I}{2}.
       $$

       同理 $\rho_B = I/2$。二者的本征值均为 $\{1/2, 1/2\}$，因此

       $$
       S(A) = S(B) = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2} = 1\ \mathrm{bit}.
       $$

       代入条件熵与互信息定义：

       $$
       S(A\mid B) = S(AB) - S(B) = 0 - 1 = -1\ \mathrm{bit},
       \qquad
       I(A:B) = S(A) + S(B) - S(AB) = 1 + 1 - 0 = 2\ \mathrm{bit}.
       $$

       依据正文第 2.3 节的量子状态合并定理，$S(A\mid B) = -1\ \mathrm{bit}$ 的操作意义是：将子系统 $A$ 合并至持有 $B$ 的接收方不仅无需额外消耗纠缠，合并后双方还会净赚 $|S(A\mid B)| = 1\ \mathrm{ebit}$（即 $1$ 个高纯度 Bell 对）。
     - **情形二：经典相关混态 $\rho_{\mathrm{cl}}$**。矩阵已对角化为 $\rho_{\mathrm{cl}} = \operatorname{diag}(1/2, 0, 0, 1/2)$，非零本征值为 $\{1/2, 1/2\}$，故整体熵

       $$
       S(AB) = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2} = 1\ \mathrm{bit}.
       $$

       对 $B$ 与 $A$ 分别取偏迹，同样得到 $\rho_A = \rho_B = I/2$，故 $S(A) = S(B) = 1\ \mathrm{bit}$。依次代入定义：

       $$
       S(A\mid B) = S(AB) - S(B) = 1 - 1 = 0\ \mathrm{bit},
       \qquad
       I(A:B) = S(A) + S(B) - S(AB) = 1 + 1 - 1 = 1\ \mathrm{bit}.
       $$

     数值回验：两者均满足 Araki–Lieb 下界 $|S(A)-S(B)| \le S(AB) \le S(A)+S(B)$（即 $0 \le 0 \le 2$ 与 $0 \le 1 \le 2$），且单比特体系互信息严格满足 $0 \le I(A:B) \le 2\min\{S(A),S(B)\} = 2\ \mathrm{bit}$。
   - **结论与边界回验**：Bell 态给出 $S(AB)=0\ \mathrm{bit}$、$S(A\mid B)=-1\ \mathrm{bit}$、$I(A:B)=2\ \mathrm{bit}$；经典相关混态给出 $S(AB)=1\ \mathrm{bit}$、$S(A\mid B)=0\ \mathrm{bit}$、$I(A:B)=1\ \mathrm{bit}$。
   - **易错坑提醒**：经典信息论里条件熵恒非负、单比特系统互信息上限是 $1\ \mathrm{bit}$，但量子纠缠打破了这两条直觉——负条件熵是量子关联超越经典关联的标志；同时，两个态的局部边缘熵完全相同（均为 $1\ \mathrm{bit}$），说明绝不能只看 $S(A)$ 区分纠缠与经典相关。

3. **【计算】等概率区分 $|0\rangle$ 与 $|\phi\rangle = (\sqrt{3}\,|0\rangle + |1\rangle)/2$ 的 Helstrom 最优成功概率**

   - **题意与约定**：单量子比特以等先验 $p_0 = p_1 = 1/2$ 制备在纯态 $|0\rangle$ 或 $|\phi\rangle = \frac{\sqrt{3}}{2}|0\rangle + \frac{1}{2}|1\rangle$ 中，求所有合法量子测量（POVM）能达到的最大猜对概率 $p_{\mathrm{guess}}$。依据等先验 Helstrom 定理，$p_{\mathrm{guess}} = \frac{1 + T(\rho_0,\rho_1)}{2}$，其中迹距离 $T(\rho_0,\rho_1) = \frac{1}{2}\|\rho_0 - \rho_1\|_1$；对两个纯态还可直接利用快捷公式 $T = \sqrt{1 - |\langle 0|\phi\rangle|^2}$ 并行交叉验算。
   - **核心提示**：对等先验纯态 $|\psi_0\rangle,|\psi_1\rangle$，先算内积模长 $|\langle 0|\phi\rangle|$，再代入 Helstrom 精确公式 $P_{\mathrm{opt}}=\frac{1}{2}\bigl(1+\sqrt{1-|\langle\psi_0|\psi_1\rangle|^2}\bigr)$（或直接求 $\frac{1}{2}(\rho_0-\rho_1)$ 的本征值核验）。
   - **完整分步演算**：先检查 $|\phi\rangle$ 的归一化：$\left(\frac{\sqrt{3}}{2}\right)^2 + \left(\frac{1}{2}\right)^2 = \frac{3}{4} + \frac{1}{4} = 1$。
     - **路径一（纯态内积公式）**：按左共轭内积约定算得

       $$
       \langle 0|\phi\rangle
       = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} \sqrt{3}/2 \\ 1/2 \end{bmatrix}
       = \frac{\sqrt{3}}{2},
       \qquad
       |\langle 0|\phi\rangle|^2 = \frac{3}{4}.
       $$

       代入纯态迹距离公式：

       $$
       T\bigl(|0\rangle, |\phi\rangle\bigr) = \sqrt{1 - |\langle 0|\phi\rangle|^2} = \sqrt{1 - \frac{3}{4}} = \sqrt{\frac{1}{4}} = \frac{1}{2}.
       $$

     - **路径二（差矩阵本征值直接验算）**：写出两个密度矩阵并相减：

       $$
       \rho_0 = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix},
       \qquad
       \rho_1 = |\phi\rangle\langle\phi| = \begin{bmatrix} 3/4 & \sqrt{3}/4 \\ \sqrt{3}/4 & 1/4 \end{bmatrix},
       \qquad
       \Delta \equiv \rho_0 - \rho_1 = \begin{bmatrix} 1/4 & -\sqrt{3}/4 \\ -\sqrt{3}/4 & -1/4 \end{bmatrix}.
       $$

       算迹与行列式：$\operatorname{Tr}(\Delta) = \frac{1}{4} - \frac{1}{4} = 0$，$\det(\Delta) = -\frac{1}{16} - \frac{3}{16} = -\frac{1}{4}$。特征方程 $\lambda^2 - \frac{1}{4} = 0$ 给出精确本征值 $\lambda_\pm = \pm\frac{1}{2}$。于是迹范数 $\|\Delta\|_1 = |1/2| + |-1/2| = 1$，迹距离 $T = \frac{1}{2}\|\Delta\|_1 = \frac{1}{2}$，与路径一完全吻合！
     - **代入 Helstrom 定理并回验最优测量**：

       $$
       p_{\mathrm{guess}} = \frac{1 + T}{2} = \frac{1 + 1/2}{2} = \frac{3}{4} = 0.75.
       $$

       进一步解出 $\Delta$ 对应正本征值 $+1/2$ 的归一化本征态：方程 $(\Delta - \frac{1}{2}I)\mathbf{v} = \begin{bmatrix}-1/4 & -\sqrt{3}/4 \\ -\sqrt{3}/4 & -3/4\end{bmatrix}\begin{bmatrix}v_0\\ v_1\end{bmatrix} = 0$ 给出 $v_0 + \sqrt{3}v_1 = 0$，故正本征态为 $|e_+\rangle = \frac{\sqrt{3}}{2}|0\rangle - \frac{1}{2}|1\rangle$，与之正交的负本征态（对应 $-1/2$）为 $|e_-\rangle = \frac{1}{2}|0\rangle + \frac{\sqrt{3}}{2}|1\rangle$。用投影测量 $\{|e_+\rangle\langle e_+|,\, |e_-\rangle\langle e_-|\}$ 分别判别 $|0\rangle$ 与 $|\phi\rangle$：

       $$
       |\langle e_+|0\rangle|^2 = \left(\frac{\sqrt{3}}{2}\right)^2 = \frac{3}{4},
       \qquad
       |\langle e_-|\phi\rangle|^2 = \left(\frac{1}{2}\cdot\frac{\sqrt{3}}{2} + \frac{\sqrt{3}}{2}\cdot\frac{1}{2}\right)^2 = \left(\frac{\sqrt{3}}{2}\right)^2 = \frac{3}{4}.
       $$

       平均成功率 $\frac{1}{2}\cdot\frac{3}{4} + \frac{1}{2}\cdot\frac{3}{4} = \frac{3}{4}$，精确达到 Helstrom 上界！顺作对照：若要求绝不猜错、允许输出“不确定”（无歧义态判别 IDP），最优成功率仅 $1 - |\langle 0|\phi\rangle| = 1 - \frac{\sqrt{3}}{2} \approx 0.1340$，远低于最小错误判别的 $0.75$。
   - **结论与边界回验**：等先验 Helstrom 最优区分成功概率为 $p_{\mathrm{guess}} = \frac{3}{4} = 75\%$，由旋转基投影测量 $\{|e_+\rangle\langle e_+|,\, |e_-\rangle\langle e_-|\}$ 达到（其中 $|e_+\rangle = \frac{\sqrt{3}}{2}|0\rangle - \frac{1}{2}|1\rangle$）。
   - **易错坑提醒**：直接沿计算基 $\{|0\rangle,|1\rangle\}$ 测量时，猜对概率只有 $\frac{1}{2}(1) + \frac{1}{2}(1/4) = \frac{5}{8} = 62.5\%$，达不到 $75\%$；Helstrom 界给出的是全部合法 POVM 上的最优值，必须把测量基对称旋转到两态夹角平分线的垂直方向才能实现。

4. **【计算】按本书约定计算 $|+\rangle$ 与最大混态 $I/2$ 的根保真度与迹距离**

   - **题意与约定**：全书统一采用根保真度 $F(\rho,\sigma) = \operatorname{Tr}\sqrt{\sqrt{\rho}\sigma\sqrt{\rho}}$ 与迹距离 $T(\rho,\sigma) = \frac{1}{2}\|\rho-\sigma\|_1$。其中一方为纯态 $|\psi\rangle\langle\psi|$ 时，根保真度简化为 $F(|\psi\rangle,\sigma) = \sqrt{\langle\psi|\sigma|\psi\rangle}$。最后用 Fuchs–van de Graaf 双向不等式 $1 - F \le T \le \sqrt{1 - F^2}$ 做独立回验。
   - **核心提示**：利用一侧为纯态 $|+\rangle$ 的简化公式 $F(|+\rangle\langle +|,\sigma)=\sqrt{\langle +|\sigma|+\rangle}$ 求根保真度，再把 $\rho-\sigma$ 变换到 $X$ 基（或直接算 $2\times 2$ 特征值）求迹距离 $T=\frac{1}{2}\|\rho-\sigma\|_1$，最后用 Fuchs–van de Graaf 界回验。
   - **完整分步演算**：
     - **计算根保真度 $F(|+\rangle, I/2)$**：先求纯态与混态的测量重叠概率（平方保真度）$F^2 = \langle +|(I/2)|+\rangle$：

       $$
       \langle +|\frac{I}{2}|+\rangle
       = \frac{1}{2}\langle +|+\rangle
       = \frac{1}{2} \cdot \left(\left|\frac{1}{\sqrt{2}}\right|^2 + \left|\frac{1}{\sqrt{2}}\right|^2\right)
       = \frac{1}{2}.
       $$

       取正平方根得到根保真度：

       $$
       F\!\left(|+\rangle,\, \frac{I}{2}\right) = \sqrt{\frac{1}{2}} = \frac{1}{\sqrt{2}} \approx 0.7071.
       $$

     - **计算迹距离 $T(|+\rangle, I/2)$**：写出两个 $2\times 2$ 密度矩阵并求差：

       $$
       |+\rangle\langle +| = \begin{bmatrix} 1/2 & 1/2 \\ 1/2 & 1/2 \end{bmatrix},
       \qquad
       \frac{I}{2} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix},
       \qquad
       \frac{I}{2} - |+\rangle\langle +| = \begin{bmatrix} 0 & -1/2 \\ -1/2 & 0 \end{bmatrix} = -\frac{1}{2}X.
       $$

       因 Pauli 矩阵 $X$ 的本征值为 $\pm 1$，故差矩阵的本征值为 $\lambda_\pm = \pm\frac{1}{2}$。迹范数为本征值绝对值之和 $\|\frac{I}{2} - |+\rangle\langle +|\|_1 = \left|\frac{1}{2}\right| + \left|-\frac{1}{2}\right| = 1$，除以 $2$ 得迹距离：

       $$
       T\!\left(|+\rangle,\, \frac{I}{2}\right) = \frac{1}{2} \times 1 = \frac{1}{2} = 0.5.
       $$

     - **Fuchs–van de Graaf 双边不等式回验**：代入 $F = \frac{1}{\sqrt{2}} \approx 0.7071$ 与 $F^2 = \frac{1}{2}$：

       $$
       1 - F = 1 - \frac{1}{\sqrt{2}} \approx 0.2929
       \;\le\;
       T = 0.5000
       \;\le\;
       \sqrt{1 - F^2} = \sqrt{1 - \frac{1}{2}} = \frac{1}{\sqrt{2}} \approx 0.7071.
       $$

       几何直觉同步验证：在 Bloch 球上，$|+\rangle$ 位于赤道 $(1,0,0)$，$I/2$ 位于球心 $(0,0,0)$，欧氏距离 $|\vec r_1 - \vec r_2| = 1$，单量子比特迹距离恰等于 Bloch 球欧氏距离的一半 $1/2 = 0.5$。
   - **结论与边界回验**：根保真度为 $F(|+\rangle, I/2) = \frac{1}{\sqrt{2}} \approx 0.7071$（平方保真度 $F^2 = \frac{1}{2}$），迹距离为 $T(|+\rangle, I/2) = \frac{1}{2} = 0.5$。
   - **易错坑提醒**：一是忘记取平方根，误把平方保真度 $1/2$ 报成根保真度；二是把 $F$ 与 $T$ 误当成相加等于 $1$ 的互补概率（这里 $F + T \approx 1.2071 \ne 1$），两者只有通过 Fuchs–van de Graaf 不等式建立双向约束。

5. **【基础】等概率正交编码 $\{|0\rangle, |1\rangle\}$ 的 Holevo 量 $\chi$ 与可达测量**

   - **题意与约定**：发送方以等概率 $p_0 = p_1 = 1/2$ 编码经典比特 $X\in\{0,1\}$ 到正交纯态 $\rho_0 = |0\rangle\langle 0|$ 与 $\rho_1 = |1\rangle\langle 1|$。按 Holevo 量定义 $\chi(\mathscr{E}) = S(\bar\rho) - \sum_x p_x S(\rho_x)$ 计算上界，再构造具体测量求出经典互信息 $I(X:Y)$，检验其是否饱和 Holevo 界 $I(X:Y) \le \chi$。
   - **核心提示**：先写出平均系综态 $\bar\rho=\frac{1}{2}\rho_0+\frac{1}{2}\rho_1$，代入 Holevo 量定义 $\chi=S(\bar\rho)-\sum_x p_x S(\rho_x)$；因两态彼此正交且纯，思考哪组投影测量能无损区分它们从而使经典互信息饱和 $\chi$。
   - **完整分步演算**：
     - **第一步：计算系综平均态 $\bar\rho$ 与其熵**：

       $$
       \bar\rho = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1|
       = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
       = \frac{I}{2}.
       $$

       平均态 $\bar\rho = I/2$ 的本征值为 $\{1/2, 1/2\}$，故 $S(\bar\rho) = h_2(1/2) = 1\ \mathrm{bit}$。
     - **第二步：计算条件熵均项并求 $\chi$**：两个条件态 $\rho_0 = |0\rangle\langle 0|$ 与 $\rho_1 = |1\rangle\langle 1|$ 均为纯态（本征值均为 $\{1, 0\}$），因此 $S(\rho_0) = S(\rho_1) = 0\ \mathrm{bit}$。代入定义：

       $$
       \chi(\mathscr{E}) = S(\bar\rho) - \frac{1}{2}S(\rho_0) - \frac{1}{2}S(\rho_1) = 1 - 0 - 0 = 1\ \mathrm{bit}.
       $$

     - **第三步：用计算基测量验证等号达成**：接收方执行计算基投影测量 $\{M_0 = |0\rangle\langle 0|,\, M_1 = |1\rangle\langle 1|\}$，输出记为 $Y\in\{0,1\}$。条件概率表为 $P(Y=0\mid X=0) = 1$、$P(Y=1\mid X=1) = 1$，完全无错，故条件香农熵 $H(X\mid Y) = 0$，经典互信息达到

       $$
       I(X:Y) = H(X) - H(X\mid Y) = h_2(1/2) - 0 = 1\ \mathrm{bit} = \chi(\mathscr{E}).
       $$

     补充对照：Holevo 界等号仅在全部信号态彼此对易（对纯态即彼此正交）时才可由单副本测量饱和；若换成等概率非正交系综 $\{|0\rangle, |+\rangle\}$，有 $\chi = S(\bar\rho) \approx 0.6009\ \mathrm{bit}$，但任何单份测量的最大可访问信息 $I_{\mathrm{acc}}$ 仅约 $0.3991\ \mathrm{bit} < \chi$，需要多份联合纠缠测量才能渐近逼近 $\chi$。
   - **结论与边界回验**：Holevo 量为 $\chi = 1\ \mathrm{bit}$，在计算基 $\{|0\rangle\langle 0|,\, |1\rangle\langle 1|\}$ 下执行投影测量即可达到 $I(X:Y) = 1\ \mathrm{bit} = \chi$。
   - **易错坑提醒**：不要把“本例单份测量能达到 $\chi$”推广成一般定律；此外，虽然单量子比特可制备无穷多种叠加态，但 Holevo 定理严格保证 $I(X:Y) \le \chi \le S(\bar\rho) \le \log_2 2 = 1\ \mathrm{bit}$，单次传输不含预共享纠缠的 $1$ 个量子比特最多只能传递 $1\ \mathrm{bit}$ 经典信息。

6. **【进阶】为什么对混态 $\rho_{AB}$，边缘熵 $S(\rho_A)$ 一般不能直接称为纠缠量**

   - **题意与约定**：考察两体系统 $\mathcal{H}_A \otimes \mathcal{H}_B$ 的一般密度矩阵 $\rho_{AB}$。要否定“$S(\rho_A) > 0$ 等价于有纠缠”或“$S(\rho_A)$ 等于纠缠度”，只需构造一个明确可分离（零纠缠）却具有最大边缘熵 $S(\rho_A) = 1\ \mathrm{bit}$ 的最小反例，再阐明纯态与混态的适用边界。
   - **核心提示**：要证伪“$S(\rho_A)$ 度量混态纠缠”，先构造零纠缠却具最大边缘熵的可分混态反例，再进一步考察 Werner 态族 $\rho_W(p)$ 检验边缘熵与部分转置负性 $\mathcal N$ 在阈值 $p=1/3$ 两侧的截然表现。
   - **完整分步演算**：构造两量子比特经典相关混态：

     $$
     \rho_{AB} = \frac{1}{2}|0\rangle\langle 0|_A \otimes |0\rangle\langle 0|_B + \frac{1}{2}|1\rangle\langle 1|_A \otimes |1\rangle\langle 1|_B.
     $$

     - **证明其纠缠严格为零**：上式已经显式写成乘积态 $\rho_k^A \otimes \rho_k^B$ 的凸组合（$\sum_k p_k = \frac{1}{2} + \frac{1}{2} = 1$，$p_k \ge 0$），按两体可分态定义属于严格可分离态，无需任何量子纠缠、仅靠共享经典随机抛硬币即可局域制备，因此所有合法纠缠度量均给出 $0$。
     - **计算边缘熵 $S(\rho_A)$**：对子系统 $B$ 求偏迹，利用 $\operatorname{Tr}(|0\rangle\langle 0|_B) = \operatorname{Tr}(|1\rangle\langle 1|_B) = 1$：

       $$
       \rho_A = \operatorname{Tr}_B(\rho_{AB})
       = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1|
       = \frac{I}{2}
       \quad\Longrightarrow\quad
       S(\rho_A) = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2} = 1\ \mathrm{bit}.
       $$

     - **物理来源剖析**：此处 $S(\rho_A) = 1\ \mathrm{bit}$ 甚至与最大纠缠 Bell 态 $|\Phi^+\rangle$ 的边缘熵完全相等，但成因截然不同——它完全来自经典制备标签（究竟发了 $|00\rangle$ 还是 $|11\rangle$）的未知性，而非跨子系统量子纠缠。一般地，当整体态 $\rho_{AB}$ 本身混合（$S(AB) > 0$）时，$S(\rho_A)$ 混杂了整体经典随机性与真实量子纠缠两股不确定性；只有当整体态是**纯态**（$S(AB) = 0$，由 Schmidt 分解得 $\rho_A$ 与 $\rho_B$ 共享同一组非零本征值 $\{\lambda_k\}$）时，$S(\rho_A) = S(\rho_B)$ 才唯一且严格地度量两体纠缠（称为纠缠熵）。
     - **信息论拓展验算（Werner 态连续族对 $S(\rho_A)$ 的“失明”反例）**：考虑两比特各向同性 Werner 态族 $\rho_W(p) = p|\Phi^+\rangle\langle\Phi^+| + (1-p)\frac{I_4}{4}$（$p \in [0, 1]$）。对任意 $p$ 求偏迹均有 $\rho_A = p\frac{I}{2} + (1-p)\frac{I}{2} = \frac{I}{2}$，故边缘熵恒为 $S(\rho_A) = 1\ \mathrm{bit}$——**完全看不出 $p$ 的变化**！然而求部分转置 $\rho_W(p)^{T_B}$ 可得唯一可能为负的本征值：

       $$
       \lambda_{\min}\bigl(\rho_W(p)^{T_B}\bigr) = \frac{1 - 3p}{4}.
       $$

       代入两个代表点对比：① 取 $p = 1/4$（低于阈值 $1/3$）：$\lambda_{\min} = \frac{1 - 3/4}{4} = +\frac{1}{16} > 0$，满足 PPT 判据且两比特下充要可分，负性 $\mathcal{N} = 0$（零纠缠）；② 取 $p = 1/2$（高于阈值 $1/3$）：$\lambda_{\min} = \frac{1 - 3/2}{4} = -\frac{1}{8} < 0$，负性 $\mathcal{N} = \frac{1}{8} > 0$（真纠缠）。两态具有完全相同的边缘熵 $S(\rho_A) = 1\ \mathrm{bit}$，纠缠性质却一在可分区、一在纠缠区，从而彻底坐实边缘熵不能充当混态纠缠度量（与[第 3 章第 11 题](#第-3-章)的纯态几何对比及[第 18 章第 13 题](#第-18-章)的相干信息视角分层互补）。
   - **结论与边界回验**：对混态 $\rho_{AB}$，非零边缘熵 $S(\rho_A)$ 既可能来自纠缠，也可能纯粹来自经典概率混合（如 $\rho_{\mathrm{cl}}$ 零纠缠却有 $S(\rho_A)=1\ \mathrm{bit}$），故不能直接当作纠缠量；量化混态纠缠必须改用负性 $\mathcal{N}$、形成纠缠 $E_F$、蒸馏纠缠 $E_D$ 或压扁纠缠等专有指标（详见第 18 章第 6 节）。
   - **易错坑提醒**：实验里对双比特态做局部单比特层析，看到子系统接近 $I/2$（纯度接近 $1/2$、局部熵接近 $1\ \mathrm{bit}$），绝不能直接宣称造出了 Bell 态——它同样可能是被彻底退相干冲毁的经典混态，必须结合联合测量或纠缠见证核验整体纯度与非局域关联。

### 练 13-C：【计算】数据处理不等式（DPI）：退极化信道下量子相对熵单调下降手算

- **题意与约定**：对应[第 13 章第 4 节](../13-quantum-information.md)。给定两单比特对角密度矩阵 $\rho = |0\rangle\langle 0| = \operatorname{diag}(1, 0)$ 与 $\sigma = \operatorname{diag}(0.75, 0.25)$，施加单比特退极化信道 $\mathcal{E}_p(\tau) = (1 - p)\tau + p\frac{I}{2}$（取 $p = 0.4$）。零跳步计算信道作用前后的量子相对熵 $D(\rho\|\sigma)$ 与 $D\bigl(\mathcal{E}_p(\rho)\,\|\,\mathcal{E}_p(\sigma)\bigr)$（底数为 $2$，单位 $\mathrm{bit}$），验证数据处理不等式（DPI）并检查 $p \to 1$ 极限。
- **核心提示**：先检查支集条件 $\operatorname{supp}(\rho) \subseteq \operatorname{supp}(\sigma)$ 确保相对熵有限，对对角矩阵直接用 $D(\rho\|\sigma) = \sum_i \lambda_i \log_2(\lambda_i/\mu_i)$，再分别算出经 $\mathcal{E}_{0.4}$ 演化后的两组对角本征值代入对比。
- **完整分步演算**：
  - **第一步：计算信道作用前的相对熵 $D(\rho\|\sigma)$**：因 $\sigma$ 满秩（$0.75 > 0,\; 0.25 > 0$），支集包含条件自动满足。约定 $0\log_2 0 = 0$，代入定义得：

    $$
    D(\rho\|\sigma) = 1 \cdot \log_2\frac{1}{0.75} + 0 = \log_2\frac{4}{3} = 2 - \log_2 3 \approx 0.415037\ \mathrm{bit}.
    $$

  - **第二步：计算退极化信道 $\mathcal{E}_{0.4}$ 的输出态**：将 $p = 0.4$ 代入 $\mathcal{E}_p(\tau) = 0.6\,\tau + 0.4\,\operatorname{diag}(0.5, 0.5) = 0.6\,\tau + \operatorname{diag}(0.2, 0.2)$：

    $$
    \mathcal{E}_{0.4}(\rho) = \operatorname{diag}(0.6 \times 1 + 0.2,\; 0.6 \times 0 + 0.2) = \operatorname{diag}(0.80,\; 0.20),
    $$

    $$
    \mathcal{E}_{0.4}(\sigma) = \operatorname{diag}(0.6 \times 0.75 + 0.2,\; 0.6 \times 0.25 + 0.2) = \operatorname{diag}(0.65,\; 0.35).
    $$

    回验两输出迹均为 $0.80 + 0.20 = 1$ 与 $0.65 + 0.35 = 1$。
  - **第三步：计算信道作用后的相对熵并验证 DPI**：

    $$
    \begin{aligned}
    D\bigl(\mathcal{E}_{0.4}(\rho)\,\|\,\mathcal{E}_{0.4}(\sigma)\bigr)
    &= 0.80 \log_2\frac{0.80}{0.65} + 0.20 \log_2\frac{0.20}{0.35} \\
    &= 0.80 \log_2\frac{16}{13} + 0.20 \log_2\frac{4}{7} \\
    &\approx 0.80 \times 0.299560 + 0.20 \times (-0.807355) \\
    &\approx 0.239648 - 0.161471 = 0.078177\ \mathrm{bit}.
    \end{aligned}
    $$

    直接比较得 $0.078177\ \mathrm{bit} < 0.415037\ \mathrm{bit}$（缩减至原值的 $18.84\%$），严格验证数据处理不等式 $D(\mathcal{E}(\rho)\|\mathcal{E}(\sigma)) \le D(\rho\|\sigma)$。
- **结论与边界回验**：噪声信道只能磨平两态的可区分度而绝不会凭空放大；极限核验：$p = 0$ 时 $\mathcal{E}_0 = \mathcal{I}$ 保持相对熵不变（等号成立），$p \to 1$ 时两输出同时塌缩到最大混态 $I/2$，相对熵严格降为 $0$。
- **易错坑提醒**：量子相对熵不满足对称性（$D(\rho\|\sigma) \ne D(\sigma\|\rho)$）——若交换两态位置算 $D(\sigma\|\rho)$，因 $\rho$ 第二个本征值为 $0$ 而 $\sigma$ 对应项非零，结果将发散为 $+\infty$！

### 练 13-D：【进阶】非正交态无歧义判别（USD）的最优成功率（IDP 界）与弃权率核算

- **题意与约定**：对应[第 13 章第 3 节](../13-quantum-information.md)。通信接收方以等先验 $p_0 = p_+ = 1/2$ 收到两个非正交单比特纯态之一：$|0\rangle$ 或 $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$。构造达到 Ivanovic–Dieks–Peres（IDP）最优成功概率的三元无歧义判别 POVM $\{E_0, E_+, E_?\}$，检验零误判条件与完备性、正半定性，并对比 Helstrom 最小错误判别。
- **核心提示**：要保证把 $|+\rangle$ 零概率错判为 $|0\rangle$，令 $E_0 \propto |-\rangle\langle -|$（与 $|+\rangle$ 正交）；同理令 $E_+ \propto |1\rangle\langle 1|$（与 $|0\rangle$ 正交）。确定最大标量系数 $c$ 使余项 $E_? = I - E_0 - E_+ \succeq 0$，即得 IDP 界 $P_{\mathrm{USD}} = 1 - |\langle 0|+\rangle|$。
- **完整分步演算**：
  - **第一步：构造零误判 POVM 元素**：重叠模长为 $s = |\langle 0|+\rangle| = 1/\sqrt{2}$。设 $E_0 = c\,|-\rangle\langle -|$、$E_+ = c\,|1\rangle\langle 1|$（$c > 0$），立刻满足零误判：

    $$
    \langle +|E_0|+\rangle = c|\langle +|-\rangle|^2 = 0, \qquad
    \langle 0|E_+|0\rangle = c|\langle 0|1\rangle|^2 = 0.
    $$

  - **第二步：由 $E_? = I - E_0 - E_+ \succeq 0$ 确定最大系数 $c$**：在计算基下写出 $E_0 + E_+$ 的 $2\times 2$ 矩阵：

    $$
    E_0 + E_+ = c\begin{bmatrix} 1/2 & -1/2 \\ -1/2 & 1/2 \end{bmatrix} + c\begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}
    = c\begin{bmatrix} 1/2 & -1/2 \\ -1/2 & 3/2 \end{bmatrix}.
    $$

    求括号内矩阵的特征多项式：$(\frac{1}{2}-\lambda)(\frac{3}{2}-\lambda) - \frac{1}{4} = \lambda^2 - 2\lambda + \frac{1}{2} = 0$，两个本征值为 $\lambda_\pm = 1 \pm \frac{1}{\sqrt{2}}$。要使 $E_? = I - (E_0 + E_+) \succeq 0$，必须满足 $c\,\lambda_+ \le 1$，取等号得最优系数：

    $$
    c_{\max} = \frac{1}{1 + 1/\sqrt{2}} = 2 - \sqrt{2} \approx 0.585786.
    $$

    此时 $E_?$ 的两个本征值为 $1 - c_{\max}\lambda_+ = 0$ 与 $1 - c_{\max}\lambda_- = 1 - \frac{1-1/\sqrt{2}}{1+1/\sqrt{2}} = 2\sqrt{2} - 2 \approx 0.828427 > 0$，严格正半定且 $E_0 + E_+ + E_? = I$。
  - **第三步：计算 USD 最优成功概率、弃权率并对比 Helstrom 界**：

    $$
    P(\text{成功}\mid 0) = \langle 0|E_0|0\rangle = \frac{c_{\max}}{2} = 1 - \frac{1}{\sqrt{2}} \approx 0.292893,
    $$

    $$
    P(\text{成功}\mid +) = \langle +|E_+|+\rangle = \frac{c_{\max}}{2} = 1 - \frac{1}{\sqrt{2}} \approx 0.292893.
    $$

    故平均无歧义成功概率为 $P_{\mathrm{USD}} = 1 - |\langle 0|+\rangle| = 1 - \frac{1}{\sqrt{2}} \approx 29.29\%$，零错判率 $P_{\mathrm{err}} = 0$，但必须付出高达 $P_? = 1 - P_{\mathrm{USD}} = \frac{1}{\sqrt{2}} \approx 70.71\%$ 的“不确定弃权率”。对照同组态的 Helstrom 最小错误判别：

    $$
    P_{\mathrm{Helstrom}} = \frac{1}{2}\Bigl(1 + \sqrt{1 - |\langle 0|+\rangle|^2}\Bigr) = \frac{1}{2}\left(1 + \frac{1}{\sqrt{2}}\right) \approx 85.36\%,
    \qquad
    P_{\mathrm{err}}^{\mathrm{Helstrom}} \approx 14.64\%.
    $$

- **结论与边界回验**：USD 与 Helstrom 体现了量子判别中的两类最优权衡——Helstrom 永不弃权但容忍 $14.64\%$ 错判，USD 把错判严格压零但以 $70.71\%$ 的弃权率为代价。边界回验：当两态正交（$s = 0$）时两者同时达到 $100\%$ 成功；当两态重合（$s = 1$）时 USD 成功率降为 $0$（全弃权）、Helstrom 降为 $50\%$（盲猜）。
- **易错坑提醒**：无歧义判别本质上依赖**非投影三元 POVM**（3 个结果挤在 2 维空间里），仅靠标准二元投影测量（PVM）绝无法同时对两个非正交态实现零误判！

### 练 13-E：【进阶】条件平滑最小熵与量子剩余哈希引理（Leftover Hashing Lemma）有限长密钥核算

- **题意与约定**：对应[第 13 章第 7.3 节](../13-quantum-information.md#73-平滑熵剩余哈希引理与第-12-章有限长-qkd-闭环)。在有限长 QKD 后处理中，通信双方持有筛选密钥串 $X$，经熵不确定关系定界得知窃听者持有量子存储 $E$ 下的条件平滑最小熵 $H_{\min}^{\varepsilon'}(X\mid E) = 6{,}000\ \mathrm{bit}$（取平滑半径 $\varepsilon' = 10^{-10}$），纠错信息协调泄露 $\mathrm{leak}_{\mathrm{EC}} = 500\ \mathrm{bit}$。现采用二通用哈希族做隐私放大提取长度 $\ell$ 的最终密钥，要求总可组合保密误差满足 $\varepsilon = 2\varepsilon' + \varepsilon_{\mathrm{PA}} \le 10^{-9}$。利用量子剩余哈希引理核算可安全提取的最大密钥长度 $\ell$，并对比渐近极限公式的缺口。
- **核心提示**：套用第 13 章 §7.3 的量子剩余哈希引理 $\ell \le H_{\min}^{\varepsilon'}(X\mid E) - \mathrm{leak}_{\mathrm{EC}} - 2\log_2\!\bigl(\frac{1}{2\varepsilon_{\mathrm{PA}}}\bigr)$，先从总预算 $\varepsilon = 10^{-9}$ 中扣除 $2\varepsilon'$ 算出允许的哈希残余项 $\varepsilon_{\mathrm{PA}}$，再计算有限长隐私放大扣减位数。
- **完整分步演算**：
  - **第一步：分配可组合安全误差预算**：由 $\varepsilon = 2\varepsilon' + \varepsilon_{\mathrm{PA}} \le 10^{-9}$ 及 $\varepsilon' = 10^{-10}$，允许的最大哈希残余项为：

    $$
    \varepsilon_{\mathrm{PA}} = \varepsilon - 2\varepsilon' = 10^{-9} - 2 \times 10^{-10} = 8 \times 10^{-10}.
    $$

  - **第二步：计算隐私放大有限长安全缓冲位数**：

    $$
    2\log_2\frac{1}{2\varepsilon_{\mathrm{PA}}}
    = 2\log_2\frac{1}{1.6 \times 10^{-9}}
    = 2\log_2\bigl(6.25 \times 10^8\bigr)
    = 2 \times \frac{\ln(6.25 \times 10^8)}{\ln 2}
    \approx 2 \times 29.2193 = 58.4386\ \mathrm{bit}.
    $$

  - **第三步：求出最大整数安全密钥长度 $\ell$ 并反向回验**：

    $$
    \ell \le 6{,}000 - 500 - 58.4386 = 5{,}441.5614\ \mathrm{bit}
    \quad\Longrightarrow\quad
    \ell_{\max} = 5{,}441\ \mathrm{bit}.
    $$

    将 $\ell = 5{,}441$ 代回原迹距离上界公式检验：

    $$
    \Delta_{\mathrm{sec}} \le 2\varepsilon' + \frac{1}{2}\cdot 2^{-\frac{1}{2}(6000 - 500 - 5441)}
    = 2\times 10^{-10} + \frac{1}{2}\cdot 2^{-29.5}
    \approx 2\times 10^{-10} + 6.585\times 10^{-10}
    = 8.585\times 10^{-10} \le 10^{-9},
    $$

    严格达标！
- **结论与边界回验**：在平滑半径 $10^{-10}$、总保密参数 $10^{-9}$ 下，除纠错泄露 $500\ \mathrm{bit}$ 外，还必须额外牺牲 $59\ \mathrm{bit}$ 用于有限长隐私放大缓冲，最终最多提取 $\ell_{\max} = 5{,}441\ \mathrm{bit}$。若不经平滑熵与剩余哈希、盲目套用渐近 von Neumann 熵率 $S(X\mid E) - \mathrm{leak}_{\mathrm{EC}}$，不仅漏掉 $59\ \mathrm{bit}$ 隐私放大扣减，更会忽略平滑熵相对渐近熵的 $O(\sqrt{n})$ 有限块长统计惩罚，严重高估短块 QKD 的安全密钥量。
- **易错坑提醒**：注意总安全参数公式中平滑半径前的系数是 **$2\varepsilon'$** 而非 $\varepsilon'$，且哈希缓冲项前有系数 $2$（因平方根来自 $2^{-(\cdots)/2}$），漏掉任一因子都会导致安全证明失效。

## 第 14 章

> 对应章节：《14｜从算法电路到物理执行：编译、调度与控制》（共 8 题）

1. **【基础】三节点线形连接上实现端点 $\mathrm{CNOT}$ 为何可能需要额外双比特门**

   - **题意与约定**：芯片物理拓扑为 3 节点直线 $0 - 1 - 2$，耦合图边集仅含 $E_G = \{(0,1), (1,2)\}$，初始映射 $\pi(q_0, q_1, q_2) = (0, 1, 2)$（高位在左大端序 $|q_0 q_1 q_2\rangle$）。目标逻辑门为端点 $\mathrm{CNOT}(q_0, q_2)$。分析物理连边缺失迫使编译器插入路由交换（`SWAP`）、改换初始布局或动用硬件搬运/远程机制的底层原因与代价。
   - **核心提示**：在耦合图边集 $E_G=\{(0,1),(1,2)\}$ 上，由于 $(0,2)$ 没有直连边，比较“保持固定初始映射需插入 SWAP”与“编译期重选初始布局把枢纽逻辑比特放中间节点”两种路径的门数差异。
   - **完整分步演算**：物理节点 $0$ 与 $2$ 之间最短距离 $D[0][2] = 2 > 1$，硬件上不存在直接耦合 $(0,2)$ 的原生双比特脉冲。编译器通常有三条出路：
     - **方案 A（原地路由：借道并归位）**：依次施加 $\mathrm{SWAP}(0,1) \to \mathrm{CNOT}(1,2) \to \mathrm{SWAP}(0,1)$。每次 $\mathrm{SWAP}$ 拆成 $3$ 个 $\mathrm{CNOT}$，故总计需要 $3 + 1 + 3 = 7$ 个物理 $\mathrm{CNOT}$；
     - **方案 B（省去恢复 `SWAP` + 重排末态映射）**：若后续只需测量或可沿新位置继续编译，仅做 $\mathrm{SWAP}(0,1) \to \mathrm{CNOT}(1,2)$（共 $4$ 个物理 $\mathrm{CNOT}$）。以初态 $|100\rangle$ 验算：

       $$
       |100\rangle \xrightarrow{\mathrm{SWAP}(0,1)} |010\rangle \xrightarrow{\mathrm{CNOT}(1,2)} |011\rangle.
       $$

       此时逻辑比特 $(q_0, q_1, q_2)$ 位于物理槽 $(1, 0, 2)$，按新映射读出物理位串 `011` 还原得逻辑结果 `101`，与理想 $\mathrm{CNOT}(q_0,q_2)|100\rangle = |101\rangle$ 精确一致；
     - **方案 C（优化初始布局或前瞻路由）**：若事先把 $(q_0, q_2)$ 映射到相邻物理位 $(0,1)$，单门只需 $1$ 个 $\mathrm{CNOT}$；在多门复杂线路中，工业路由器 SABRE / LightSABRE 通过带前瞻扩展集 $E_{\mathrm{ext}}$ 的代价函数（如正文 4 比特线形算例中 $W=0.5$ 时 $\mathrm{SWAP}(1,2)$ 得分 $2.00 < \mathrm{SWAP}(0,1)$ 的 $2.25$）避免短视拆散后续相邻门。
     - **编译器初始布局优化视角（第 14 章路由层专属区分）**：与[第 9 章第 10 题](#第-9-章)固定映射下的物理故障核算不同，编译器的第一步是**初始布局（Layout Pass）**——只需在逻辑电路开始前把虚拟比特 $q_0$ 映射到居中的物理节点 $1$，令 $\pi'(q_0, q_1, q_2) = (1, 0, 2)$，则原本跨端点的逻辑门 $\mathrm{CNOT}(q_0, q_2)$ 立刻变成相邻物理边 $(1, 2)$ 上的 **1 个原生 $\mathrm{CNOT}$**，额外路由门数为 $0$！只有当多条双比特门冲突使全局无法把全部互动对都映射成近邻边时，才必须动用动态 `SWAP` 路由。
   - **结论与边界回验**：由于端点 $(0,2)$ 缺乏原生物理直连，在固定布局下必须插入物理 `SWAP`（增 $3$ 至 $6$ 个 $\mathrm{CNOT}$）、改换初始布局，或付出粒子搬运/测量前馈等平台特定开销。
   - **易错坑提醒**：省掉回程 `SWAP` 确实能把双比特门从 $7$ 个压到 $4$ 个，但若忘记在末尾按最终物理—逻辑映射重排比特序，在零噪声理想芯片上也会把 `011` 错当成逻辑态 `011` 而制造 $100\%$ 必错的软件缺陷。

2. **【计算】一个 $\mathrm{SWAP}$ 分解为三个 $\mathrm{CNOT}$：来回两次 $\mathrm{SWAP}$ 的额外门数与验证**

   - **题意与约定**：先在 4 维两比特计算基 $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ 上零跳步验证恒等式 $\mathrm{SWAP} = \mathrm{CNOT}_{01}\mathrm{CNOT}_{10}\mathrm{CNOT}_{01}$（算符从右向左作用），再核算来回两次 `SWAP` 的精确门数增量、关键路径耗时与简化无故障概率。
   - **核心提示**：先在四维计算基上逐一验证三枚交错 CNOT 的合成确为 $\mathrm{SWAP}$，再累加去程与回程两次 SWAP 的门数；并比较省略回程 SWAP、改在读出阶段重排逻辑映射所节省的双比特门比例。
   - **完整分步演算**：记控制位在前、目标位在后，$\mathrm{CNOT}_{01}|a,b\rangle = |a,\, a\oplus b\rangle$，$\mathrm{CNOT}_{10}|a,b\rangle = |a\oplus b,\, b\rangle$。对任意计算基态 $|a,b\rangle$（$a,b\in\{0,1\}$）连续作用三门：

     $$
     |a,b\rangle
     \xrightarrow{\mathrm{CNOT}_{01}} |a,\, a\oplus b\rangle
     \xrightarrow{\mathrm{CNOT}_{10}} |a\oplus(a\oplus b),\, a\oplus b\rangle = |b,\, a\oplus b\rangle
     \xrightarrow{\mathrm{CNOT}_{01}} |b,\, b\oplus(a\oplus b)\rangle = |b, a\rangle.
     $$

     逐一核对全部 4 个计算基态：$|00\rangle\to|00\rangle$、$|01\rangle\to|10\rangle$、$|10\rangle\to|01\rangle$、$|11\rangle\to|11\rangle$，确与 $\mathrm{SWAP}$ 矩阵完全相等（按 KAK/Weyl 室几何，$\mathrm{SWAP}$ 的 Cartan 坐标为 $(\frac{\pi}{4}, \frac{\pi}{4}, \frac{\pi}{4})$，因 $k_z \ne 0$，数学上至少需要 $3$ 个 $\mathrm{CNOT}$ 不可再压）。因此来回执行两次 `SWAP` 共增加

     $$
     \Delta N_{\mathrm{CNOT}} = 2 \times 3 = 6\text{ 个额外 }\mathrm{CNOT},
     \qquad
     N_{\mathrm{tot}} = 1 + 6 = 7\text{ 个 }\mathrm{CNOT}.
     $$

     代入正文 4.1 节参数（前置 $H(q_0)$ 耗时 $20\ \mathrm{ns}$、每个 $\mathrm{CNOT}$ 耗时 $200\ \mathrm{ns}$、并行测量 $800\ \mathrm{ns}$）：关键路径由直连时的 $20 + 200 + 800 = 1020\ \mathrm{ns}$ 暴涨至 $20 + 7\times 200 + 800 = 2220\ \mathrm{ns}$；在每门独立无错概率 $0.99$ 的简化模型下，全门无错路径概率从 $0.99$ 跌至 $0.99^7 \approx 0.9321$。
     - **编译优化量化收益：延迟恢复（Deferred Unrouting）**：在实际编译流水线中，如果该端点 $\mathrm{CNOT}$ 之后即进入读出（或后续门改按新映射继续调度），编译器只需更新逻辑—物理映射表 $\pi_{\mathrm{out}}$ 并在经典测量后重排比特下标，直接砍掉回程 `SWAP`：总双比特门数从 $7$ 降至 $4$（减少 $42.9\%$），在单门独立 $1\%$ 故障模型下无故障概率从 $0.99^7 \approx 93.21\%$ 提升至 $0.99^4 \approx 96.06\%$。
   - **结论与边界回验**：来回做两次 `SWAP` 会额外增加 $6$ 个 $\mathrm{CNOT}$（连同目标端点门共 $7$ 个 $\mathrm{CNOT}$）；若末尾允许更新输出映射省去回程 `SWAP`，则只增 $3$ 个（总计 $4$ 个）。
   - **易错坑提醒**：容易误把“来回两次 `SWAP`”当成只需 $2$ 个双比特门，或在估算门数时忘记每次 `SWAP` 的 $3$ 倍展开系数；同时也别把 $0.99^7 \approx 0.932$ 这类简化无错率直接等同于包含等待退相干、串扰与读出误差的真实态保真度。

3. **【计算】为什么四操作调度算例中把门时长直接相加会高估理想执行时间**

   - **题意与约定**：回看正文 4.3 节三比特四操作线路：$H(q_0)$（$20\ \mathrm{ns}$）、$\mathrm{CNOT}(q_0,q_1)$（$200\ \mathrm{ns}$，依赖 $H(q_0)$）、$X(q_2)$（$20\ \mathrm{ns}$，与前两者独立）、三比特并行测量（$800\ \mathrm{ns}$，等待全部门完成）。按有向无环图（DAG）关键路径公式 $a_j = \max(\max_{i\prec j} f_i,\; \max_{r\in R_j} u_r)$ 计算理想完工时间，并与机械累加对比。
   - **核心提示**：画出四操作之间的比特数据依赖图（DAG），识别互不共享比特、可同时并行执行的门对，用关键路径最长链时长对比四门时长直接串行相加之和。
   - **完整分步演算**：先列出机械全串行累加值（把三比特各自 $800\ \mathrm{ns}$ 测量也逐一串行相加）：

     $$
     T_{\mathrm{sum}} = 20 + 200 + 20 + 3 \times 800 = 2640\ \mathrm{ns}
     \qquad (\text{即便测量合并计一次也达 } 20 + 200 + 20 + 800 = 1040\ \mathrm{ns}).
     $$

     再按无共享总线冲突的尽早调度（ASAP）逐项排程：
     - $t \in [0, 20)\ \mathrm{ns}$：$H(q_0)$ 与互不相交的 $X(q_2)$ **同时并行**执行，均在 $20\ \mathrm{ns}$ 完工；
     - $t \in [20, 220)\ \mathrm{ns}$：前驱 $H(q_0)$ 完成后立刻启动 $\mathrm{CNOT}(q_0, q_1)$，完工时刻 $220\ \mathrm{ns}$（期间 $q_2$ 空闲等待，工程上可在空闲窗插动态解耦脉冲以抑制低频失谐噪声 $\delta(t)$）；
     - $t \in [220, 1020)\ \mathrm{ns}$：三颗量子比特同时并行执行读出测量，整体在 $1020\ \mathrm{ns}$ 完工。

     因此整条线路耗时由最长依赖链（关键路径 $H(q_0) \to \mathrm{CNOT}(q_0,q_1) \to \text{并行测量}$）决定：

     $$
     T_{\mathrm{crit}} = 20 + 200 + 800 = 1020\ \mathrm{ns} \ll 2640\ \mathrm{ns}.
     $$

     同时注意反面边界：正文 4.3 节四比特共享总线算例表明，若两门虽不共用量子比特却共用控制通道 $r$（如 $R_A=\{q_0,q_1,r\}$ 与 $R_B=\{q_2,q_3,r\}$），则 $A, B$ 仍须串行，总耗时由 $1100\ \mathrm{ns}$ 增至 $1300\ \mathrm{ns}$；且强行并行高串扰门对也会增大错误率。
   - **结论与边界回验**：由于不冲突的门（如 $X(q_2)$ 与 $H(q_0)$）以及多比特测量均可并行执行，理想完工时间等于关键路径长度 $1020\ \mathrm{ns}$，远小于所有操作时长机械相加的 $2640\ \mathrm{ns}$。
   - **易错坑提醒**：两个极端都错——既不能无视并行性把全部门时长机械累加，也不能只看量子比特集合不相交就假设一定能并行（必须把共享控制总线、读出复用与残余 $ZZ$ 串扰约束一起写进资源集合）。

4. **【计算】状态层析测得 Bloch 向量长度 $1.03$，为何不能把线性反演矩阵当作物理态**

   - **题意与约定**：任意单量子比特厄米、单位迹矩阵均可按 Pauli 基展开为 $\rho = \frac{1}{2}(I + \vec{r}\cdot\vec{\sigma})$，其中 $\vec{r} = (r_x, r_y, r_z) \in \mathbb{R}^3$。计算该矩阵的两个本征值关于长度 $|\vec{r}|$ 的精确公式，代入 $|\vec{r}| = 1.03$ 验证它破坏了密度矩阵的正半定性（产生负测量概率），并指出规范的物理重构流程。
   - **核心提示**：把单比特厄米单位迹矩阵 $\rho=\frac{1}{2}(I+\vec r\cdot\vec\sigma)$ 的两个本征值写成 $\lambda_\pm=(1\pm|\vec r|)/2$，代入 $|\vec r|=1.03$ 检验正半定性是否被破坏，再思考编译校准中应如何用带约束重构替代粗暴径向截断。
   - **完整分步演算**：取旋转坐标系使 $\vec{r}$ 指向新 $z'$ 轴，因酉相似保持本征值不变，$\rho$ 与对角矩阵 $\frac{1}{2}(I + |\vec{r}|Z) = \operatorname{diag}\!\left(\frac{1 + |\vec{r}|}{2},\; \frac{1 - |\vec{r}|}{2}\right)$ 具有完全相同的两个本征值：

     $$
     \lambda_+ = \frac{1 + |\vec{r}|}{2}, \qquad \lambda_- = \frac{1 - |\vec{r}|}{2}.
     $$

     合法物理密度矩阵必须正半定（$\rho \succeq 0$），等价于 $\lambda_- \ge 0 \iff |\vec{r}| \le 1$。代入线性反演得到的经验长度 $|\hat{\vec{r}}| = 1.03$：

     $$
     \lambda_+ = \frac{1 + 1.03}{2} = 1.015 > 1,
     \qquad
     \lambda_- = \frac{1 - 1.03}{2} = -0.015 < 0.
     $$

     若沿 $-\hat{\vec{r}}$ 方向做投影测量（对应本征态 $|e_-\rangle$），Born 规则会荒谬地预测出负概率 $P(e_-) = \langle e_-|\hat{\rho}_{\mathrm{lin}}|e_-\rangle = -0.015 < 0$（而沿 $+\hat{\vec{r}}$ 方向概率为 $1.015 > 1$），且无法代入 von Neumann 熵或根保真度公式。其成因是高纯度态本就贴近 Bloch 球面（$|\vec{r}| \approx 1$），有限次采样随机涨落或未校准的 SPAM 偏差很容易把经验向量推到球外；而在存在三能级泄漏的实际门校准中（如正文 DRAG 整形的 AC Stark 频移 $\frac{\delta E_1(t)}{\hbar} = \frac{(\lambda I(t)/2)^2}{-\alpha}$ 与三能级 GRAPE 验收），还须借助非后选择计算子空间平均重叠 $\bar{f}_{\mathrm{comp}}$ 区分泄漏与球内退相干。
     - **编译校准层两类工程陷阱（第 14 章专属侧重，区别于[第 15 章第 4 题](#第-15-章)的纯采样方差分析）**：① **切勿用径向硬截断 $\vec{r} \mapsto \vec{r}/|\vec{r}|$ 替代约束优化**——简单把球外估计拉回单位球面会把本带噪声的态强行锁死在纯态边界 $|\vec{r}| = 1$ 上，系统性高估门保真度与纯度；② **从态层析外推到过程层析（QPT）与门集层析（GST）时**，不仅须施加 Choi 矩阵半正定（CP）与保迹（TP）约束，还须处理门集规范自由度（gauge freedom），否则 SPAM 漂移会被错归为非物理的负 Choi 本征值。
   - **结论与边界回验**：Bloch 向量长度 $1.03 > 1$ 使线性反演矩阵出现负本征值 $\lambda_- = -0.015 < 0$，违背正半定性、给出负概率，绝非合法物理态；工程上应改用带正半定与单位迹约束的最大似然估计（MLE）并附上采样不确定度区间。
   - **易错坑提醒**：不要通过简单把负特征值截成 $0$ 再除迹就当作“无偏真实态”，投影回物理边界会引入轻微估计偏差，且若 $|\hat{\vec{r}}|$ 显著大于 $1$ 超过采样误差范围，更应先排查读出混淆矩阵漂移或测量轴未正交等系统误差。

5. **【进阶】读出混淆矩阵求逆为何会放大采样噪声**

   - **题意与约定**：按全书统一的列随机混淆矩阵定义 $\mathbf{q} = M\mathbf{p}$（列为真实态、行为报告结果），推导单比特 $M^{-1}$ 显式公式与线性缓解估计 $\hat{p}_{0,\mathrm{mit}}$ 的精确方差表达式，代入正文超导参数（$e_0=0.03, e_1=0.08$）与强噪声对照（$e_0=e_1=0.25$）算清方差放大倍数，并补充多比特协方差、漂移偏差与可扩展方法。
   - **核心提示**：写出列随机 $2\times 2$ 混淆矩阵 $M=\begin{bmatrix}1-a&1-b\\a&b\end{bmatrix}$ 及其行列式 $\det M=b-a$，显式求出 $M^{-1}$ 并代入方差传递公式 $\mathrm{Var}(\hat p)=\mathrm{Var}(\hat q)/(b-a)^2$，观察读出对比度变差时方差如何放大。
   - **完整分步演算**：设 $e_0 = \Pr(\text{报 }1\mid 0)$、$e_1 = \Pr(\text{报 }0\mid 1)$ 且 $e_0 + e_1 < 1$，混淆矩阵及其行列式为

     $$
     M = \begin{bmatrix} 1 - e_0 & e_1 \\ e_0 & 1 - e_1 \end{bmatrix},
     \qquad
     \det M = (1 - e_0)(1 - e_1) - e_0 e_1 = 1 - e_0 - e_1 > 0.
     $$

     由 $2\times 2$ 求逆公式得

     $$
     M^{-1} = \frac{1}{1 - e_0 - e_1}\begin{bmatrix} 1 - e_1 & -e_1 \\ -e_0 & 1 - e_0 \end{bmatrix}.
     $$

     对 $N$ 次独立采样测得的经验频率 $\hat{\mathbf{q}} = (\hat{q}_0, 1 - \hat{q}_0)^T$ 执行线性反演 $\hat{\mathbf{p}}_{\mathrm{mit}} = M^{-1}\hat{\mathbf{q}}$，展开第一分量：

     $$
     \hat{p}_{0,\mathrm{mit}}
     = \frac{(1 - e_1)\hat{q}_0 - e_1(1 - \hat{q}_0)}{1 - e_0 - e_1}
     = \frac{\hat{q}_0 - e_1}{1 - e_0 - e_1}.
     $$

     由于分母 $1 - e_0 - e_1 < 1$ 且 $M^{-1}$ 含大于 $1$ 的正元素与负元素，对常数缩放取方差得精确放大律：

     $$
     \operatorname{Var}(\hat{p}_{0,\mathrm{mit}})
     = \frac{\operatorname{Var}(\hat{q}_0)}{(1 - e_0 - e_1)^2}
     = \frac{q_0(1 - q_0)}{N(1 - e_0 - e_1)^2}.
     $$

     代入两组数值验算：
     - **典型超导读出（$e_0 = 0.03,\; e_1 = 0.08$）**：$\det M = 0.89$，$M^{-1} \approx \begin{bmatrix}1.0337 & -0.0899\\ -0.0337 & 1.0899\end{bmatrix}$，方差放大倍数为 $1/0.89^2 = 1/0.7921 \approx 1.2625$；
     - **强读出噪声（$e_0 = e_1 = 0.25$）**：$\det M = 0.50$，方差直接放大 $1/0.50^2 = 4$ 倍（需 $4$ 倍采样数才能恢复同等统计误差），且一旦 $\hat{q}_0 < 0.25$ 还会吐出负概率。

     在多比特情形下，频率分量间存在非零协方差，方差放大取决于 $M^{-1}\Sigma_{\hat{\mathbf{q}}}(M^{-1})^T$ 而不只是单一条件数；且若标定矩阵 $M$ 已漂移，求逆会直接注入系统偏差。大规模芯片上需改用 M3（稀疏子空间无矩阵迭代）或 TREX（测量前 Pauli 随机化对角化衰减系数）。
   - **结论与边界回验**：混淆矩阵 $M^{-1}$ 含绝对值大于 $1$ 及负号元素，线性反演会把单比特采样方差精确放大 $(1 - e_0 - e_1)^{-2}$ 倍（如 $e_0=0.03, e_1=0.08$ 时为 $1.2625\times$，$e_0=e_1=0.25$ 时为 $4\times$），强噪声下还可能出现负概率，若标定漂移更会引入系统偏差。
   - **易错坑提醒**：一是混淆行随机与列随机矩阵导致把 $M$ 转置用反；二是把读出缓解误解为“免费消除测量错误”，忽略了额外采样开销、校准矩阵自身有限样本误差以及它完全不能修复中途测量引起的泄漏与非 QND 破坏。

6. **【计算】动态电路实时反馈延迟预算的六项组成与等待退相干核算**

   - **题意与约定**：按正文 10.1 节把一次中途测量到条件门执行完毕的全过程拆为六个依次串联的物理时间环节，写出总反馈时延公式，代入超导教学参数核算总延迟与数据比特空闲等待弛豫损失，并严格区分“延迟组成项”与“等待导致的物理退相干后果”。
   - **核心提示**：按信号物理流向依次列出读出脉冲、信号积分判决、数据上行、经典计算/解码、下行指令派发与条件门执行六段时延并求和，再代入 $e^{-t/T_1}$ 估算数据比特等待期间的弛豫损耗。
   - **完整分步演算**：实时反馈闭环总时延由六项依次相加构成：

     $$
     t_{\mathrm{fb}} = t_{\mathrm{meas}} + t_{\mathrm{classify}} + t_{\mathrm{transport}} + t_{\mathrm{classical}} + t_{\mathrm{dispatch}} + t_{\mathrm{pulse}},
     $$

     各项物理含义依次为：① 读出模拟信号积分时间 $t_{\mathrm{meas}}$；② 状态判别与分类时间 $t_{\mathrm{classify}}$；③ 控制系统内部总线传输时间 $t_{\mathrm{transport}}$；④ 经典条件逻辑计算时间 $t_{\mathrm{classical}}$；⑤ 指令解码与波形下发时间 $t_{\mathrm{dispatch}}$；⑥ 条件物理脉冲自身时长 $t_{\mathrm{pulse}}$。代入正文超导数值算例（单位 $\mathrm{ns}$）：

     $$
     t_{\mathrm{fb}} = 800 + 150 + 300 + 200 + 150 + 50 = 1650\ \mathrm{ns} = 1.65\ \mu\mathrm{s}.
     $$

     在条件脉冲真正到来之前，旁侧保持量子态的数据比特已空闲等待 $t_{\mathrm{wait}} = t_{\mathrm{fb}} - t_{\mathrm{pulse}} = 1.60\ \mu\mathrm{s}$。若该数据比特处于激发态 $|1\rangle$ 且 $T_1 = 100\ \mu\mathrm{s}$，仅计振幅阻尼能量弛豫，等待期间衰变回 $|0\rangle$ 的概率就达

     $$
     p_{\mathrm{relax}} = 1 - e^{-t_{\mathrm{wait}}/T_1} = 1 - e^{-1.60/100} = 1 - e^{-0.016} \approx 0.01587 \approx 1.59\%.
     $$

     若在等待期间对数据比特插入动态解耦（如 XY4），仅能抑制低频 $Z$ 轴失谐噪声 $\delta(t)$ 引起的纯退相位，无法阻止 $T_1$ 自发弛豫。
   - **结论与边界回验**：六项预算依次为测量积分 $t_{\mathrm{meas}}$、状态判别 $t_{\mathrm{classify}}$、控制系统内传输 $t_{\mathrm{transport}}$、经典条件计算 $t_{\mathrm{classical}}$、指令下发 $t_{\mathrm{dispatch}}$ 与条件脉冲 $t_{\mathrm{pulse}}$；退相干是等待造成的误差后果，不是第七项时延分量。
   - **易错坑提醒**：一是把退相干错列进六项时间相加公式里；二是误以为只要把经典逻辑 $t_{\mathrm{classical}}$ 优化成零就能解决反馈瓶颈（上例中读出积分与传输合计就占 $1.10\ \mu\mathrm{s}$）；三是把云端 API 毫秒级网络往返与近端 FPGA 微秒级闭环实时路径混为一谈。

7. **【基础】为什么解码吞吐足够快，仍可能无法及时执行逻辑分支**

   - **题意与约定**：区分实时容错系统对流式解码器（处理纠错症状提取出的探测事件）的两条独立硬约束——**稳态平均吞吐**（$\bar{t}_{\mathrm{dec}} \le \tau_{\mathrm{cyc}}$）与**端到端反应时间及高分位尾延迟**（$\tau_{\mathrm{react}} \le \tau_{\mathrm{budget}}$），并结合批处理/滑窗延迟、突发排队积压及 Litinski 容错编译中不可对易多体旋转的串行依赖拆解原因。
   - **核心提示**：严格区分稳态平均吞吐（单位时间能处理的平均轮数）与单次最坏/高分位尾延迟（影响逻辑分支实时截止窗口），思考批处理或偶发长尾难题为何会令吞吐达标却仍错过反馈截止线。
   - **完整分步演算**：
     - **吞吐率 $\ne$ 单轮反应时延**：吞吐率衡量长期平均每秒处理多少轮纠错症状（例如平均 $\bar{t}_{\mathrm{dec}} = 0.96\ \mu\mathrm{s} < \tau_{\mathrm{cyc}} = 1.0\ \mu\mathrm{s}$ 即可避免 Terhal 指数积压 $r_{\mathrm{back}}^k$ 发散）。但高吞吐可以通过攒大批量（batching）、采用较深滑窗偷看未来多轮纠错症状、或引入并行流水线来换取——这些手段都会显著拉长单轮纠错症状从产生到产出分支判决的端到端等待时间；
     - **长尾突发引爆排队连锁违约**：即使没有批处理，一旦某一轮遭遇复杂关联错误簇（例如单个解码耗时突增至 $4.0\ \mu\mathrm{s}$，如第 19 章 20 任务 FIFO 队列算例），单服务台不仅该轮超时，还会把后续一连串普通轮次全部堵在队列里，使高分位响应时延（p99 / 最大值）远超单轮允许的反馈截止时间；
     - **对逻辑时钟的硬限制**：在 Litinski 容错编译框架下，虽然 Clifford 门可推入末态 Pauli 乘积测量（PPM），但彼此不对易的多体 $\pi/8$ 非 Clifford 旋转必须等待前一步的解码结果决定下一个条件 Clifford 修正或旋转分支，因此逻辑门时钟频率直接受限于端到端反应时间 $\tau_{\mathrm{react}}$ 与尾延迟，而非仅看平均吞吐。
   - **结论与边界回验**：平均吞吐足够快只保证系统长期不发生指数积压，不能保证每一轮都在硬反馈截止时间前完成；批处理/滑窗等待、传输下界以及偶发长尾解码造成的排队尾延迟，都会导致控制器错过实时条件分支窗口。因此实时解码器必须同时汇报稳态吞吐与端到端响应时延的高分位数。
   - **易错坑提醒**：只看离线桌面脚本跑完一万轮后的平均单轮耗时（或中位数），就签字担保在线硬件满足实时反馈截止时间，忽略了离线批处理与在线流式尾延迟、通信链路之间的根本鸿沟。

8. **【基础】保存编译随机种子为何不能保证下周真机结果完全相同**

   - **题意与约定**：按正文 13.3 节区分随机种子的三层可复现边界——编译器软件层确定性、量子硬件物理状态平稳性、以及端到端云栈版本一致性，明确种子到底冻结了什么、冻结不了什么，并列出真正可审计复现的必存工件清单。
   - **核心提示**：按三层可复现边界拆解：编译随机种子仅锁定软件端的启发式搜索与布局选择，既锁不住芯片参数的随时间慢漂移和两能级缺陷（TLS）跳变，也锁不住云端固件/校准快照的版本更新。
   - **完整分步演算**：
     - **随机种子仅冻结编译器的伪随机分支**：在 SABRE / LightSABRE 路由初始布局、多随机种子择优或随机编译（Pauli twirling）电路生成中，固定种子能确保**在完全相同的软件版本、目标机耦合图与校准参数输入下**产出字节一致的编译后 ISA 线路；
     - **无法冻结物理芯片与全栈运行环境**：一周之后，真实芯片必然经历四类变化——① 物理漂移与随机跳变（频率漂移、两能级系统 TLS 切换、$T_1/T_2$ 波动、读出混淆矩阵漂移）；② 校准与拓扑变更（每日自动校准刷新脉冲幅度/DRAG 参数，坏比特被屏蔽导致耦合子图变动）；③ 软硬件栈更新（固件、目标 ISA、原生门/分数门约束、后端运行时队列与调度策略调整）；④ 量子测量本身的固有随机抽样涨落（即使物理态完全不变，有限 shots 计数仍按多项分布随机起伏）。
     - **完整可复现归档清单**：除编译随机种子外，还必须冻结并存档带时间戳的硬件校准快照、精确的软件与固件版本及依赖锁、编译前逻辑线路与编译后物理 ISA 线路工件、物理比特布局与末态映射、后端名称与作业编号、全部原始计数（含时间戳分批记录）以及后处理配置。
   - **结论与边界回验**：编译随机种子只固定软件侧的伪随机选择，无法冻结真实硬件的物理漂移、校准更新、坏比特变化、固件升级与量子测量固有随机性，因此不能保证下周真机给出完全相同的结果。
   - **易错坑提醒**：把经典软件工程里“固定随机种子 = 比特级复现”的经验直接照搬到真机量子实验，既漏存校准快照与编译后物理线路，又误把跨周结果差异归咎于代码 bug 而忽略硬件漂移。

### 练 14-C：【进阶】Weyl 室坐标最小 CNOT 判据与 ZX 演算蜘蛛融合消门手算

- **题意与约定**：对应[第 14 章第 2.2–2.3 节](../14-compilation-control.md#22-进阶选读两比特最优门综合kakcartan分解与-weyl-室几何)。(a) 已知两比特 KAK 分解中 $\mathrm{CNOT}$、$\mathrm{iSWAP}$、$\mathrm{SWAP}$ 的 Weyl 室非局域坐标分别为 $(\frac{\pi}{4}, 0, 0)$、$(\frac{\pi}{4}, \frac{\pi}{4}, 0)$ 与 $(\frac{\pi}{4}, \frac{\pi}{4}, \frac{\pi}{4})$，利用 Makhlin 不变量 $g_1 = (\cos 2k_x\cos 2k_y\cos 2k_z + i\sin 2k_x\sin 2k_y\sin 2k_z)^2$ 与底面判据 $k_z = 0$，判定三者各自最少需要多少个 $\mathrm{CNOT}$；(b) 用 ZX 演算的 Hadamard 换色律与同色蜘蛛融合律化简单比特线路 $U = R_z(\frac{\pi}{4})\,H\,R_x(\frac{\pi}{2})\,H\,R_z(\frac{3\pi}{4})$，并用 $2\times 2$ 矩阵乘法独立回验。
- **核心提示**：第一问记住“$1$ 个 $\mathrm{CNOT}$ 仅达单点 $(\pi/4, 0, 0)$，$2$ 个 $\mathrm{CNOT}$ 扫满底面 $k_z = 0$（强迫 $g_1 \in \mathbb{R}_{\ge 0}$），凡 $k_z \ne 0$ 必用 $3$ 个 $\mathrm{CNOT}$”；第二问先把夹在两个 $H$ 中间的红色 $X$ 蜘蛛翻转成绿色 $Z$ 蜘蛛，再把三个相邻 $Z$ 蜘蛛的相位直接相加。
- **完整分步演算**：
  - **第一问：Weyl 室最小 CNOT 判定**：
    - 对 $\mathrm{CNOT}$：$(k_x, k_y, k_z) = (\frac{\pi}{4}, 0, 0)$，恰好就是单 $\mathrm{CNOT}$ 规范点 $A_1$，代入得 $g_1 = (0 + 0)^2 = 0 \in \mathbb{R}_{\ge 0}$，最少 **1 个 $\mathrm{CNOT}$**；
    - 对 $\mathrm{iSWAP}$：$(k_x, k_y, k_z) = (\frac{\pi}{4}, \frac{\pi}{4}, 0)$，位于底面 $k_z = 0$ 但异于单点 $A_1$，代入得 $g_1 = (0\cdot 0\cdot 1 + i\cdot 1\cdot 1\cdot 0)^2 = 0 \in \mathbb{R}_{\ge 0}$，故 $1$ 个不够、**2 个 $\mathrm{CNOT}$** 恰可精确合成；
    - 对 $\mathrm{SWAP}$：$(k_x, k_y, k_z) = (\frac{\pi}{4}, \frac{\pi}{4}, \frac{\pi}{4})$，$k_z = \frac{\pi}{4} \ne 0$，代入得

      $$
      g_1(\mathrm{SWAP}) = \bigl(0 + i\cdot 1\cdot 1\cdot 1\bigr)^2 = i^2 = -1 \notin \mathbb{R}_{\ge 0},
      $$

      违背 $2$-CNOT 可达集合的必要条件 $g_1 \in \mathbb{R}_{\ge 0}$，故最少必须 **3 个 $\mathrm{CNOT}$**（同时也达到 $\mathrm{SU}(4)$ 的全局上界 3）。
  - **第二步：ZX 演算化简与矩阵独立回验**：
    - **ZX 图重写**：利用 Hadamard 换色律 $H\,R_x(\alpha)\,H = R_z(\alpha)$（把夹在两枚黄盒 $H$ 间的红蜘蛛 $X(\pi/2)$ 换成绿蜘蛛 $Z(\pi/2)$ 并消去两枚 $H$），再用同色蜘蛛融合律 $Z(\alpha)Z(\beta) = Z(\alpha+\beta)$：

      $$
      U = R_z\!\left(\frac{\pi}{4}\right)\underbrace{H\,R_x\!\left(\frac{\pi}{2}\right)H}_{=\,R_z(\pi/2)}\,R_z\!\left(\frac{3\pi}{4}\right)
      = R_z\!\left(\frac{\pi}{4} + \frac{\pi}{2} + \frac{3\pi}{4}\right)
      = R_z\!\left(\frac{3\pi}{2}\right).
      $$

    - **$2\times 2$ 矩阵独立回验**：由 $H X H = Z$ 立即推得 $H e^{-i\frac{\pi}{4}X} H = e^{-i\frac{\pi}{4}HXH} = e^{-i\frac{\pi}{4}Z} = R_z(\frac{\pi}{2})$（连全局相位也严格为 $1$！），三枚对角阵相乘得：

      $$
      U = \operatorname{diag}\!\bigl(e^{-i\frac{3\pi}{4}},\; e^{+i\frac{3\pi}{4}}\bigr)
      = e^{-i\frac{3\pi}{4}}\begin{bmatrix} 1 & 0 \\ 0 & e^{i\frac{3\pi}{2}} \end{bmatrix}
      = e^{-i\frac{3\pi}{4}}\begin{bmatrix} 1 & 0 \\ 0 & -i \end{bmatrix}
      = e^{-i\frac{3\pi}{4}} S^\dagger.
      $$

      原本含 2 个 $H$、1 个 $R_x$ 和 2 个非 Clifford $T$-族旋转门（共 5 门）的线路，经两步 ZX 规则直接化简为 **1 个 Clifford 门 $S^\dagger$**（甚至连全部非 Clifford $T$ 门都抵消了，且在硬件上可用零时长 Virtual-Z 免费实现！）。
- **结论与边界回验**：最小 CNOT 数依次为 $\mathrm{CNOT}: 1$、$\mathrm{iSWAP}: 2$、$\mathrm{SWAP}: 3$；ZX 化简线路严格等于 $R_z(3\pi/2) = e^{-i3\pi/4}S^\dagger$。
- **易错坑提醒**：不要凭直觉以为“$\sqrt{\mathrm{SWAP}}$ 只是半个 $\mathrm{SWAP}$ 所以只要 $1.5 \to 2$ 个 $\mathrm{CNOT}$”——$\sqrt{\mathrm{SWAP}}$ 的坐标 $(\pi/8, \pi/8, -\pi/8)$ 同样有 $k_z \ne 0$（$g_1 = -i/4 \notin \mathbb{R}_{\ge 0}$；其伴随 $\sqrt{\mathrm{SWAP}}^\dagger$ 坐标为 $(\pi/8, \pi/8, +\pi/8)$，对应 $g_1 = +i/4$），依然必须 3 个 $\mathrm{CNOT}$！

### 练 14-D：【计算】DRAG 正交导数脉冲系数 $\beta/\alpha$ 与 M3 子空间读出缓解复杂度对比

- **题意与约定**：对应[第 14 章第 6.1 节](../14-compilation-control.md#61-drag-波形推导为什么正交通道要加主包络的时间导数)与[第 9.2 节](../14-compilation-control.md#92-突破-2n-指数墙m3-与-trex)。(a) 某超导 Transmon 非谐性为 $\alpha/(2\pi) = -250\ \mathrm{MHz}$，同相高斯主脉冲 $I(t) = \Omega_0 \exp\!\left[-\frac{(t-t_0)^2}{2\sigma^2}\right]$（脉宽参数 $\sigma = 5\ \mathrm{ns}$）。按 DRAG 波形公式 $Q(t) = -\frac{\beta}{\alpha}\dot{I}(t)$（取标准一阶泄漏抑制系数 $\beta = 1/2$），求 $Q(t)$ 达到极值的时刻、无量纲峰值幅度比 $|Q|_{\max}/\Omega_0$，并检验单位自洽性；(b) 对一条 $n = 20$ 比特线路执行 $4{,}000$ 次采样，实测仅出现 $k = 120$ 个不同比特串，对比全空间读出混淆矩阵求逆与 M3 子空间约化矩阵的双精度浮点数（`float64`，每元素 $8\ \mathrm{byte}$）内存占用。
- **核心提示**：第一问对 $I(t)$ 求时间导数得 $\dot{I}(t) = -\frac{t-t_0}{\sigma^2}I(t)$，再用一阶导数为零找出 $u e^{-u^2/2}$ 的极值点 $u = \pm 1$（切记把非谐性转成角频率 $\alpha = 2\pi\times(-250\ \mathrm{MHz})$！）；第二问分别按 $(2^n)^2 \times 8\ \mathrm{B}$ 与 $k^2 \times 8\ \mathrm{B}$ 核算。
- **完整分步演算**：
  - **第一问：DRAG 正交脉冲极值与单位检验**：令无量纲时间变量 $u = \frac{t - t_0}{\sigma}$，代入 $\dot{I}(t) = -\frac{u}{\sigma}\Omega_0 e^{-u^2/2}$ 得：

    $$
    Q(t) = -\frac{\beta}{\alpha}\dot{I}(t) = \frac{\beta}{\alpha\,\sigma}\,\Omega_0\,u\,e^{-u^2/2}.
    $$

    - **单位检验**：$\alpha$ 单位为 $\mathrm{rad/s}$，$\sigma$ 单位为 $\mathrm{s}$，故乘积 $\alpha\sigma$ 无量纲；$\beta$ 与 $u e^{-u^2/2}$ 均无量纲，因此 $Q(t)$ 与 $\Omega_0$ 共享完全相同的角频率单位 $\mathrm{rad/s}$。
    - **求极值点**：令 $\frac{d}{du}(u e^{-u^2/2}) = (1 - u^2)e^{-u^2/2} = 0$，得极值点 $u = \pm 1$，即脉冲中心前后各一个标准差时刻 **$t = t_0 \pm \sigma = t_0 \pm 5\ \mathrm{ns}$**，极值大小为 $e^{-1/2} = 1/\sqrt{e}$。
    - **代入角频率数值**：$|\alpha| = 2\pi \times 250 \times 10^6\ \mathrm{rad/s} = 5\pi \times 10^8\ \mathrm{rad/s}$，故 $|\alpha|\sigma = 5\pi \times 10^8 \times 5 \times 10^{-9} = 2.5\pi \approx 7.853982$。代入 $\beta = 1/2$：

      $$
      \frac{|Q|_{\max}}{\Omega_0}
      = \frac{\beta}{|\alpha|\sigma\sqrt{e}}
      = \frac{0.5}{7.853982 \times 1.648721}
      \approx 0.038613 \quad (\text{约 } 3.86\%).
      $$

  - **第二问：全空间混淆矩阵 vs M3 子空间矩阵内存对比**：
    - 全空间矩阵维度为 $2^{20} \times 2^{20} = 2^{40}$ 个元素，双精度存储需：

      $$
      M_{\mathrm{full}} = 8 \times 2^{40}\ \mathrm{B} = 8\ \mathrm{TiB}
      $$

      （且稠密求逆耗时 $O(8^n) = O(2^{60})$，彻底不可行）；
    - M3 仅在实测观测到的 $k = 120$ 个比特串支撑子空间内构造 $120 \times 120$ 约化混淆矩阵（辅以稀疏矩阵-向量迭代求解），双精度存储仅需：

      $$
      M_{\mathrm{M3}} = 120 \times 120 \times 8\ \mathrm{B} = 115{,}200\ \mathrm{B} = 112.50\ \mathrm{KiB},
      $$

      空间直接压缩超过 $7.6 \times 10^7$ 倍！
- **结论与边界回验**：DRAG 正交脉冲呈反对称双峰，在 $t_0 \pm 5\ \mathrm{ns}$ 达峰值，幅度仅为主脉冲的 $3.86\%$（满足弱扰动条件 $|\alpha|\sigma \gg 1$）；M3 将 $20$ 比特读出缓解从 $8\ \mathrm{TiB}$ 指数墙压降至 $112.50\ \mathrm{KiB}$。
- **易错坑提醒**：计算 DRAG 幅度比时最常见失误是直接拿普通频率 $250\ \mathrm{MHz}$ 乘以 $5\ \mathrm{ns}$ 漏掉 $2\pi$，结果会把正交脉冲幅值算大 $6.28$ 倍，反而人为引入严重相位与泄漏误差！

### 练 14-E：【进阶】Litinski 容错编译：把 Clifford 门推过 $T$ 门化为 Pauli 乘积旋转

- **题意与约定**：对应[第 14 章第 12.2 节](../14-compilation-control.md#122-litinski-clifford-消除与-pauli-乘积测量ppm)。在表面码晶格手术容错架构中，Litinski 编译通过把所有 Clifford 门推过非 Clifford $T$ 门（$T = e^{i\pi/8} e^{-i\frac{\pi}{8}Z}$）并吸收到末端的 Pauli 乘积测量（PPM）中，从而把电路彻底化简为“一串 $\pi/8$ Pauli 旋转 + 最终 PPM”。对 2 比特电路片段 $U = C\,(T_0 \otimes I_1)$，其中 Clifford 块 $C = \mathrm{CNOT}_{0\to 1}\,(H_0 \otimes I_1)$（大端序），零跳步推导把 $C$ 推到 $T_0$ 右侧后的等价 Pauli 乘积旋转，并用 $4\times 4$ 算符关系独立核验。
- **核心提示**：把 $T_0$ 写成 Pauli 旋转指数 $e^{-i\frac{\pi}{8}Z_0 I_1}$（除去无关全局相位 $e^{i\pi/8}$），应用酉共轭恒等式 $C\,e^{-i\theta P}\,C^\dagger = e^{-i\theta(C P C^\dagger)} \implies C\,e^{-i\theta P} = e^{-i\theta(C P C^\dagger)}\,C$，分两步把 $Z_0 I_1$ 经 $H_0$ 与 $\mathrm{CNOT}_{0\to 1}$ 共轭变换即可。
- **完整分步演算**：
  - **第一步：写出共轭推门恒等式**：因为任意酉算符 $C$ 满足 $C P^k C^\dagger = (C P C^\dagger)^k$，对幂级数逐项求和立得：

    $$
    C\,e^{-i\frac{\pi}{8} Z_0 I_1} = \Bigl(C\,e^{-i\frac{\pi}{8} Z_0 I_1}\,C^\dagger\Bigr) C = e^{-i\frac{\pi}{8}\bigl(C(Z_0 I_1)C^\dagger\bigr)}\,C.
    $$

  - **第二步：分两拍计算 Clifford 共轭 $C(Z_0 I_1)C^\dagger$**：将 $C = \mathrm{CNOT}_{0\to 1}(H_0 \otimes I_1)$ 代入（注意 $C^\dagger = (H_0 \otimes I_1)\mathrm{CNOT}_{0\to 1}$）：
    - 内层 $H_0$ 共轭：$(H_0 \otimes I_1)(Z_0 I_1)(H_0 \otimes I_1) = (H Z H)_0 \otimes I_1 = X_0 I_1$；
    - 外层 $\mathrm{CNOT}_{0\to 1}$ 共轭：利用控制位 $X$ 向目标位传播的规则 $\mathrm{CNOT}_{0\to 1}(X_0 I_1)\mathrm{CNOT}_{0\to 1} = X_0 X_1$（可逐基态验证：对 $|ab\rangle$，先 CNOT 再 $X_0$ 再 CNOT 把 $|a,b\rangle \to |a, a\oplus b\rangle \to |\bar{a}, a\oplus b\rangle \to |\bar{a}, \bar{a}\oplus a\oplus b\rangle = |\bar{a}, \bar{b}\rangle = (X_0 X_1)|ab\rangle$）。
  - **第三步：写出推门后的等价容错形式并检验**：

    $$
    C\,(T_0 \otimes I_1) = e^{i\frac{\pi}{8}}\,e^{-i\frac{\pi}{8} X_0 X_1}\,C = e^{i\frac{\pi}{8}}\,R_{XX}\!\left(\frac{\pi}{4}\right) C.
    $$

    按 $R_{XX}(\pi/4) = \cos(\frac{\pi}{8})I_4 - i\sin(\frac{\pi}{8})X_0 X_1$ 展开并与左侧直接作用在基态 $|00\rangle$ 上核验：
    - 左侧：$C T_0 |00\rangle = C|00\rangle = \mathrm{CNOT}_{0\to 1}|+0\rangle = |\Phi^+\rangle$；
    - 右侧：$e^{i\pi/8}\bigl(\cos\frac{\pi}{8}I - i\sin\frac{\pi}{8}X_0 X_1\bigr)|\Phi^+\rangle = e^{i\pi/8}\bigl(\cos\frac{\pi}{8} - i\sin\frac{\pi}{8}\bigr)|\Phi^+\rangle = e^{i\pi/8}e^{-i\pi/8}|\Phi^+\rangle = |\Phi^+\rangle$（因 $X_0 X_1|\Phi^+\rangle = +|\Phi^+\rangle$！），精确一致！
- **结论与边界回验**：Clifford 块 $C$ 被完整推到右侧且不增加任何 $T$ 门数量，原本的局域 $T_0$ 变为两比特非 Clifford Pauli 旋转 $e^{-i\frac{\pi}{8}X_0 X_1}$（在表面码上通过一次多比特晶格手术 + 1 份 $|T\rangle$ 魔术态注入完成）；若后续紧接单比特 $Z$ 测量，把 $C$ 继续推过测量即化为对 $C^\dagger Z_k C$ 的 Pauli 乘积测量（PPM），原电路中的所有 Clifford 门彻底从物理执行时间轴上消失。
- **易错坑提醒**：Clifford 消除虽然把 $T$-count 保持不变并消除了显式 Clifford 门时长，却可能把单比特 $Z$ 旋转变成高权重多比特 Pauli 旋转（如 $X_0 X_1$ 乃至几十比特串），从而在晶格手术中增加路由空道（routing space）占用——时空权衡绝不能只看“消掉多少门”而忽略布线面积。

## 第 15 章

> 对应章节：《15｜实践路线：从手算、模拟到真机实验与论文复核》（共 8 题）

1. **【基础】为什么应先做态矢量模拟，再做有限采样模拟**

   - **题意与约定**：依据正文第 1 节的四级验证阶梯，把“确定性代数正确性验证”与“有限样本统计涨落分析”拆成两道独立工序，说明为何两类误差混在一起会彻底丧失排错能力。
   - **核心提示**：把“电路逻辑与符号约定是否正确（确定性代数误差）”与“有限次测量的二项/多项随机涨落（统计噪声）”拆开，思考若第一步跳过态矢量模拟直接跑 shots，两类误差混在一起会怎样妨碍排错。
   - **完整分步演算**：
     - **第一步（态矢量/精确密度矩阵模拟）只查确定性逻辑**：精确态矢量模拟直接保存全部 $2^n$ 个复振幅，不含任何随机抽样噪声。在此阶段可以以机器精度（$10^{-14}$ 量级）一次抓出五类致命程序错误——门作用顺序写反（电路从左向右 vs 矩阵从右向左）、相对相位符号错、比特大端序/小端序颠倒（如 Qiskit 小端序 `'01'` vs Cirq/PennyLane 大端序）、归一化破坏，以及跨框架噪声参数口径差（例如模拟总 Pauli 翻转率 $q = 0.03$ 时，PennyLane/Cirq/Stim 传 `0.03`，而 Qiskit Aer 的 `depolarizing_error(λ, 1)` 满足 $q = \frac{3}{4}\lambda$，必须传 $\lambda = \frac{4}{3}q = 0.04$，否则无噪声比对中就会静默把 Bell 关联从 $0.96$ 错算成 $0.97$）；
     - **第二步（有限采样模拟）单独引入统计不确定度**：确认理论分布精确无误后，再加入有限采样次数 $N$，核验频率涨落（标准误量级 $\sim 1/\sqrt{N}$）、区间构造（使用 95% Wilson 得分区间或 Clopper–Pearson 精确界而非低概率端会坍塌的 Wald 区间）以及分批漂移检测。若第一步未做就直接跑 $N = 1000$ 次采样，见到 $0.463$ 偏离 $0.500$（正文种子 `20260922` 的 95% Wilson 区间为 $[0.4323, 0.4940]$）时，根本无法判断这是正常的 $5\%$ 统计波动，还是线路里漏写了一个门或写反了端序。
   - **结论与边界回验**：先用态矢量模拟在零抽样噪声下锁死门序、相位、端序、归一化与噪声模型口径，再引入有限采样检验统计涨落与区间覆盖，才能把程序逻辑错误与随机统计波动彻底隔离。
   - **易错坑提醒**：新手常一上来就用默认 $N = 1024$ 次采样跑电路，看到结果和预期差了几个百分点便盲目以为“只是随机误差”，从而放跑了端序写反或噪声系数差 $4/3$ 倍的严重程序错误。

2. **【进阶】只观察 Bell 电路的 `00/11` 相关，为何不能证明纠缠**

   - **题意与约定**：比较纯 Bell 纠缠态 $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ 与零纠缠的经典相关混态 $\rho_{\mathrm{cl}} = \frac{1}{2}|00\rangle\langle 00| + \frac{1}{2}|11\rangle\langle 11|$。先写出两者的 $4\times 4$ 密度矩阵，严格证明它们在计算基（$ZZ$ 基）下给出完全无法区分的 `00/11` 计数分布，再通过换基（$XX, YY$）把两者劈开。
   - **核心提示**：构造与 Bell 态在计算基有完全相同 `00/11` 频率的经典相关混态 $\rho_{\mathrm{cl}}$，再写出三基 Bell 保真度见证公式 $F^2=\frac{1}{4}(1+\langle XX\rangle-\langle YY\rangle+\langle ZZ\rangle)$，说明为何必须补测共轭基突破可分界 $1/2$。
   - **完整分步演算**：在大端计算基 $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ 下并排写出两者的密度矩阵：

     $$
     \rho_{\Phi^+} = |\Phi^+\rangle\langle\Phi^+|
     = \frac{1}{2}\begin{bmatrix}
     1 & 0 & 0 & 1 \\
     0 & 0 & 0 & 0 \\
     0 & 0 & 0 & 0 \\
     1 & 0 & 0 & 1
     \end{bmatrix},
     \qquad
     \rho_{\mathrm{cl}}
     = \frac{1}{2}\begin{bmatrix}
     1 & 0 & 0 & 0 \\
     0 & 0 & 0 & 0 \\
     0 & 0 & 0 & 0 \\
     0 & 0 & 0 & 1
     \end{bmatrix}.
     $$

     - **在 $ZZ$（计算基）下完全同分布**：计算基测量概率只读取密度矩阵的对角元。两个矩阵的对角元完全一致，均为 $(1/2, 0, 0, 1/2)$，因此都会输出 $50\%$ 的 `00`、$50\%$ 的 `11`，且 $\langle ZZ\rangle_{\Phi^+} = \langle ZZ\rangle_{\mathrm{cl}} = +1$。但 $\rho_{\mathrm{cl}}$ 已显式写成乘积态的经典概率混合（毫无纠缠），它缺少维持量子相干性的非对角项 $\frac{1}{2}|00\rangle\langle 11| + \frac{1}{2}|11\rangle\langle 00|$；
     - **换基测量彻底暴露差异**：利用 $X\otimes X$ 的反对角矩阵形式（仅 $(00,11),(01,10),(10,01),(11,00)$ 元为 $1$），分别求迹：

       $$
       \langle XX\rangle_{\Phi^+} = \operatorname{Tr}\bigl((X\otimes X)\rho_{\Phi^+}\bigr) = \frac{1}{2} + \frac{1}{2} = +1,
       \qquad
       \langle XX\rangle_{\mathrm{cl}} = \operatorname{Tr}\bigl((X\otimes X)\rho_{\mathrm{cl}}\bigr) = 0.
       $$

       同理 $\langle YY\rangle_{\Phi^+} = -1$ 而 $\langle YY\rangle_{\mathrm{cl}} = 0$。代入 Bell 重叠见证公式 $f_{\Phi^+} = \frac{1 + \langle XX\rangle - \langle YY\rangle + \langle ZZ\rangle}{4}$，经典混态只得 $f_{\Phi^+}(\rho_{\mathrm{cl}}) = \frac{1 + 0 - 0 + 1}{4} = \frac{1}{2}$，严格落在可分离态上界 $1/2$ 以内。
     - **实验复核最小见证数值证伪（第 15 章专属深化，区别于[第 3 章第 3 题](#第-3-章)的矩阵结构入门）**：在真实两比特硬件验收中，判定是否超越可分态界（$F^2_{\mathrm{sep}} \le 1/2$）最轻量的协议是测三组 Pauli 关联并代入 Bell 态平方重叠公式：

       $$
       F^2\bigl(|\Phi^+\rangle, \rho\bigr) = \frac{1}{4}\bigl(1 + \langle XX\rangle - \langle YY\rangle + \langle ZZ\rangle\bigr).
       $$

       即使计算基测得极强的关联 $\langle ZZ\rangle = 0.92$（对应 `00/11` 占比 $96\%$），只要强烈退相位把非对角相干冲毁为 $\langle XX\rangle = \langle YY\rangle = 0$，代入上式立刻得到 $F^2 = \frac{1 + 0.92}{4} = 0.48 < 0.50$，完全落入可分态区间——仅凭 `00/11` 直方图绝无权宣称实验制备出了纠缠态。
   - **结论与边界回验**：计算基的 `00/11` 强相关仅反映密度矩阵对角元，经典可分离混态 $\rho_{\mathrm{cl}}$ 能产生一模一样的直方图；要证实纠缠必须补测共轭基（$XX$、$YY$）以检验非对角相干项，构造超过可分阈值 $1/2$ 的纠缠见证（或执行带物理约束的态层析），同时写明可信测量（SPAM）前提。
   - **易错坑提醒**：把经典配对相关误当成量子纠缠，甚至看到真机 $ZZ$ 直方图里 `00+11` 占 $95\%$ 就宣称“纠缠保真度 $95\%$”，却从未测过 $XX$ 与 $YY$ 关联。

3. **【计算】计算 $|\Phi^+\rangle$ 的三个 Pauli 关联、理想 Bell 重叠 $f_{\Phi^+}$ 与本书约定的根保真度**

   - **题意与约定**：给定两比特最大纠缠纯态 $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$，逐项作用 $X\otimes X$、$Y\otimes Y$、$Z\otimes Z$ 计算期望值，再代入 Bell 重叠公式 $f_{\Phi^+} = \langle\Phi^+|\rho|\Phi^+\rangle = \frac{1 + \langle XX\rangle - \langle YY\rangle + \langle ZZ\rangle}{4}$，最后严格按全书根保真度口径 $F = \sqrt{f_{\Phi^+}}$ 换算。
   - **核心提示**：先将 $X\otimes X$、$Y\otimes Y$、$Z\otimes Z$ 逐项作用在 $|\Phi^+\rangle$ 上求三个期望值，代入 $f_{\Phi^+}=\frac{1}{4}(1+\langle XX\rangle-\langle YY\rangle+\langle ZZ\rangle)$，再开平方根得到本书约定的根保真度 $F$。
   - **完整分步演算**：使用单比特作用规则 $X|0\rangle = |1\rangle, X|1\rangle = |0\rangle$；$Y|0\rangle = i|1\rangle, Y|1\rangle = -i|0\rangle$；$Z|0\rangle = |0\rangle, Z|1\rangle = -|1\rangle$，逐项展开三个张量积算符对 $|\Phi^+\rangle$ 的作用：

     $$
     (X\otimes X)|\Phi^+\rangle = \frac{X|0\rangle\otimes X|0\rangle + X|1\rangle\otimes X|1\rangle}{\sqrt{2}} = \frac{|11\rangle + |00\rangle}{\sqrt{2}} = +|\Phi^+\rangle,
     $$

     $$
     (Y\otimes Y)|\Phi^+\rangle = \frac{(i|1\rangle)\otimes(i|1\rangle) + (-i|0\rangle)\otimes(-i|0\rangle)}{\sqrt{2}} = \frac{i^2|11\rangle + (-i)^2|00\rangle}{\sqrt{2}} = -\frac{|00\rangle + |11\rangle}{\sqrt{2}} = -|\Phi^+\rangle,
     $$

     $$
     (Z\otimes Z)|\Phi^+\rangle = \frac{|0\rangle\otimes|0\rangle + (-|1\rangle)\otimes(-|1\rangle)}{\sqrt{2}} = \frac{|00\rangle + |11\rangle}{\sqrt{2}} = +|\Phi^+\rangle.
     $$

     因为 $|\Phi^+\rangle$ 已归一化（$\langle\Phi^+|\Phi^+\rangle = \frac{1}{2} + \frac{1}{2} = 1$），直接取内积得三个精确期望值：

     $$
     \langle XX\rangle = +1, \qquad \langle YY\rangle = -1, \qquad \langle ZZ\rangle = +1.
     $$

     代入 Bell 投影展开式（注意 $YY$ 项前的负号）：

     $$
     f_{\Phi^+} = \frac{1 + \langle XX\rangle - \langle YY\rangle + \langle ZZ\rangle}{4}
     = \frac{1 + 1 - (-1) + 1}{4} = \frac{4}{4} = 1.
     $$

     换算为本书统一的根保真度口径：

     $$
     F\bigl(|\Phi^+\rangle, |\Phi^+\rangle\bigr) = \sqrt{f_{\Phi^+}} = \sqrt{1} = 1.
     $$

     特别提醒非理想态下的数值差异：例如正文实验二测得 $\hat{f}_{\Phi^+} = 0.6625$ 时，根保真度为 $\hat{F} = \sqrt{0.6625} \approx 0.8139$，两者相差 $0.15$ 以上。
   - **结论与边界回验**：理想 $|\Phi^+\rangle$ 的三个关联依次为 $\langle XX\rangle = +1$、$\langle YY\rangle = -1$、$\langle ZZ\rangle = +1$，Bell 重叠 $f_{\Phi^+} = 1$，本书约定的根保真度 $F = \sqrt{f_{\Phi^+}} = 1$。
   - **易错坑提醒**：一是把 $\langle YY\rangle$ 的符号记成 $+1$（忘记 $i\cdot i = -1$）；二是在非理想实验中省掉平方根或混写平方重叠 $f_{\Phi^+}$ 与根保真度 $F$，导致跨论文对比保真度时出现系统性虚高。

4. **【计算】为什么线性反演层析可能给出负特征值**

   - **题意与约定**：写出单比特线性反演层析公式 $\hat{\rho}_{\mathrm{lin}} = \frac{1}{2}(I + \hat{r}_x X + \hat{r}_y Y + \hat{r}_z Z)$，说明物理正半定条件要求 $|\hat{\vec{r}}| \le 1$，而无约束的线性反演把三组有限样本统计误差（或相关系统偏差）直接叠加进三个坐标分量，容易把贴近 Bloch 球面的高纯度态推出单位球外。用具体数字手算一个典型负特征值实例。
   - **核心提示**：对贴近 Bloch 球面的纯态 $|+\rangle$，用三轴有限采样估计值算出经验模长 $|\hat{\vec r}|=\sqrt{\hat r_x^2+\hat r_y^2+\hat r_z^2}$ 与本征值 $\lambda_-=(1-|\hat{\vec r}|)/2$，并从 $\mathbb E[\hat r_y^2+\hat r_z^2]=2/N$ 看为何高纯态大概率被推出球外。
   - **完整分步演算**：设真实制备的纯态是 $|+\rangle$（真实 Bloch 向量 $\vec{r} = (1, 0, 0)$，恰好位于球面边界 $|\vec{r}| = 1$）。对 $X, Y, Z$ 三组基分别执行有限次采样估计，设由于有限采样涨落测得经验期望 $\hat{r}_x = 0.98$、$\hat{r}_y = 0.20$、$\hat{r}_z = 0.25$。线性反演矩阵虽然自动满足厄米且迹为 $1$，但其 Bloch 向量长度变为

     $$
     |\hat{\vec{r}}| = \sqrt{0.98^2 + 0.20^2 + 0.25^2}
     = \sqrt{0.9604 + 0.0400 + 0.0625}
     = \sqrt{1.0629} \approx 1.0310 > 1.
     $$

     代入特征值公式 $\lambda_\pm = \frac{1 \pm |\hat{\vec{r}}|}{2}$ 得：

     $$
     \lambda_+ \approx \frac{1 + 1.0310}{2} = 1.0155,
     \qquad
     \lambda_- \approx \frac{1 - 1.0310}{2} = -0.0155 < 0.
     $$

     该负特征值破坏了密度矩阵的正半定性。更需注意：产生负特征值**并不要求三组测量误差彼此独立**——即使各基共享同一读出校准偏差或受时间慢漂移影响而高度相关，只要合向量模长超过 $1$，线性反演照样给出负特征值。在多比特系统里，球体边界曲率更高维、参数达 $4^n - 1$ 个，线性反演撞出负特征值几乎是常态，因此标准工程实践采用带正半定约束的最大似然估计（MLE）或贝叶斯重构并报告统计区间。
     - **有限采样统计机理定量证明（第 15 章统计侧重，区别于[第 14 章第 4 题](#第-14-章)的校准/CP 投影视角）**：对真实纯态 $|+\rangle$（$\vec{r} = (1, 0, 0)$），若 $X, Y, Z$ 三轴各独立采样 $N$ 次，则 $\hat{r}_y, \hat{r}_z$ 均值为 $0$、方差为 $1/N$。即便 $\hat{r}_x = 1$ 完全无误差，经验 Bloch 向量模长平方的统计期望也严格超过 $1$：

       $$
       \mathbb{E}\bigl[|\hat{\vec{r}}|^2\bigr] = \mathbb{E}[\hat{r}_x^2] + \mathbb{E}[\hat{r}_y^2] + \mathbb{E}[\hat{r}_z^2] = 1 + \frac{1}{N} + \frac{1}{N} = 1 + \frac{2}{N} > 1.
       $$

       取 $N = 100$ 即得 $\mathbb{E}[|\hat{\vec{r}}|^2] = 1.02$（均方根长度 $\approx 1.01 > 1$），说明对高纯度态做无约束线性反演时，有限采样统计涨落本身就会大概率把重构点推出 Bloch 球外。
   - **结论与边界回验**：线性反演不对重构矩阵施加正半定约束，有限采样统计波动或校准漂移（无论各轴误差是否独立）把高纯度态的经验 Bloch 向量推至单位球外（$|\hat{\vec{r}}| > 1$），便必然产生负特征值 $\lambda_- = (1 - |\hat{\vec{r}}|)/2 < 0$。
   - **易错坑提醒**：把负特征值一律误解为“实验代码写错了”或“量子力学失效”，实际上对接近纯态的有限采样这是线性反演的结构性现象；反过来，若负特征值幅值远超采样误差，才应排查 SPAM 标定失准。

5. **【基础】比较编译方案时，至少应同时报告哪四项资源**

   - **题意与约定**：编译优化是一个典型的多目标权衡问题——压缩门数、压缩深度、挑低错物理边与降低动态反馈开销往往不能同时最优。依据正文第 4.4 节与第 14 章编译流水线，归纳横向比较不同编译方案时必须同台公开的四项核心资源账单。
   - **核心提示**：围绕双比特门计数（及按错误率加权成本）、双比特关键路径深度、布局所需物理比特数与连接约束、以及中途测量/动态反馈与编译耗时四类核心资源梳理横向比较账本。
   - **完整分步演算**：对同一抽象逻辑电路比较两种编译方案（例如不同优化级别、不同路由器或不同原生门集）时，至少须同步列明以下四类定量指标：
     - **1. 编译后的门规模与路由开销**：明确分列原生**双比特纠缠门数**（如 `CNOT`/`CZ`/`ECR`/`iSWAP`）、原生单比特脉冲门数（与零耗时虚拟 Z 分开）、总门数，以及路由阶段额外插入的 `SWAP` 数（或离子/原子搬运次数）；
     - **2. 电路深度与硬件调度时长**：同时报告抽象门层深度与考虑共享控制总线、读出并行度及串扰禁配约束后的**实际物理调度完工时长**（单位 $\mathrm{ns}$ 或 $\mu\mathrm{s}$）；
     - **3. 物理比特布局、末态映射与对应校准质量**：写明电路映射到了芯片上哪几颗物理比特及哪些耦合边，并附上对应时间戳的实时校准快照（单/双比特门错误率、读出错误率、$T_1/T_2$ 与已知高串扰门对），以及多组编译随机种子下的分布范围；
     - **4. 动态控制与后处理开销（若适用）**：若方案涉及动态电路中途测量、实时纠错解码或线路切割/误差缓解，还必须同步报告反馈闭环延迟、解码吞吐/尾延迟或采样放大倍数 $\Gamma^2$；跨软件框架比对带噪性能时，须先核对端序与退极化参数换算（如 Qiskit Aer 的 $q = \frac{3}{4}\lambda$）。
   - **结论与边界回验**：比较编译方案至少要同时报告：① 编译后双比特门数、总门数与 `SWAP`/搬运开销；② 电路深度或实际调度时长；③ 所选物理比特布局与对应实时校准质量；④ 涉及动态反馈、解码或误差缓解时的延迟与采样放大成本。
   - **易错坑提醒**：只报“双比特门少了 15%”或“深度浅了 2 层”，却隐瞒新方案把门挤进了高串扰并发时间槽、或把电路挪到了错误率高一倍的边缘坏比特上，导致实际运行保真度不升反降。

6. **【基础】一篇论文只报告后选择后的保真度，还缺哪些关键信息**

   - **题意与约定**：后选择（post-selection）通过丢弃检测到错误或未满足特定标记条件的样本来换取留存样本的高条件保真度。如果不公开被丢弃的样本比例与总试验分母，任何低质量系统都能靠极端筛除拼出“99% 保真度”。结合正文第 4.5 节数值反例列齐必补信息。
   - **核心提示**：从后选择分母缺失可能掩盖的产率坍塌与选择偏倚出发，列出除条件保真度之外必报的原始总尝试数、筛选判据、接受率、基于留存样本的置信区间及未筛选原始结果。
   - **完整分步演算**：设原始总试验数为 $N_{\mathrm{raw}}$，满足后选择条件的接受数为 $N_{\mathrm{acc}}$，则**接受率**（retention / acceptance rate）为 $p_{\mathrm{acc}} = N_{\mathrm{acc}} / N_{\mathrm{raw}}$，接受样本中的条件正确率为 $p_{\mathrm{cond}}$，而**每原始尝试的有效交付率**为两者的乘积：

     $$
     p_{\mathrm{eff}} = p_{\mathrm{acc}} \cdot p_{\mathrm{cond}}.
     $$

     套用正文第 4.5 节的对比反例做零跳步验算：
     - **方法 A**：接受率 $p_{\mathrm{acc},A} = 80\%$，后选择条件正确率 $p_{\mathrm{cond},A} = 90\%$，每原始尝试交付正确率为 $0.80 \times 0.90 = 72\%$；
     - **方法 B**：接受率 $p_{\mathrm{acc},B} = 25\%$，后选择条件正确率 $p_{\mathrm{cond},B} = 96\%$，每原始尝试交付正确率反而暴跌至 $0.25 \times 0.96 = 24\%$（仅为方法 A 的三分之一！）。

     因此，凡使用后选择的论文都必须同时补齐七项关键字段：① **原始总试验数** $N_{\mathrm{raw}}$ 与**未后选择前的原始保真度/成功率**；② 精确且事前锁定的**后选择筛选规则**（排除事后挑样本）；③ **接受率** $p_{\mathrm{acc}}$ 及其随系统规模 $n$ 的衰减标度（是否指数下降）；④ **每原始尝试有效交付率** $p_{\mathrm{eff}}$；⑤ **单位墙钟时间的有效成功事件率**；⑥ 基于**有效留存样本数 $N_{\mathrm{acc}}$**（而非原始总数 $N_{\mathrm{raw}}$！）计算的统计不确定度与置信区间；⑦ 被丢弃分支的物理归因（泄漏、丢失还是误判）。
     **跨章侧重对照（第 15 章论文复核视角）**：本题提供审稿与复现时可直接勾选的完整披露核查清单，并与[第 9 章第 3 题](#第-9-章)（光子物理损耗 $\eta^m$）及[第 11 章第 3 题](#第-11-章)（吞吐缩水与 Wilson 置信区间放大 $13.5$ 倍）形成三层分工。
   - **结论与边界回验**：只报后选择保真度严重残缺，至少必须补报原始总试验数、后选择规则、接受率、每尝试有效交付率、单位时间有效事件数、基于留存样本量的置信区间，以及未后选择的原始结果。
   - **易错坑提醒**：一是在计算误差条时误把筛除前的 $N_{\mathrm{raw}}$ 代入分母（人为缩窄置信区间）；二是忽略接受率随比特数 $n$ 指数衰减的事实，把小规模高后选择保真度误判成可扩展优势。

7. **【基础】分别给出“观察”“解释”“外推”各一句示例，并剖析证据强度的逐级差异**

   - **题意与约定**：科研写作的核心纪律是把“直接测量到的事实”、“依赖物理/统计模型的推断”和“跨出当前实验范围的趋势预测”严格分层，绝不把外推包装成观察。构建同一 Bell 实验上的三句递进示例并逐层分析其假设依赖。
   - **核心提示**：围绕同一组 Bell 线路采样计数设计递进三句：第一句仅报原始计数与统计区间（观察），第二句引入噪声模型做相容归因（解释），第三句跨越实测比特规模做趋势预测（外推），再逐层对比假设依赖。
   - **完整分步演算**：围绕一次 2 比特 Bell 线路采样实验，写出层级分明的三句话：
     - **观察（Observation，证据最强）**：“在 2026-11-25 的校准快照上，对 2 比特 Bell 线路独立运行 $4000$ 次采样，计算基测得 `00` 或 `11` 共 $3680$ 次（频率 $\hat{p} = 0.9200$，双侧 $95\%$ Wilson 置信区间为 $[0.9112,\, 0.9280]$）。”——仅陈述可核验的原始计数、实验条件与确定性统计区间，不引入未检验的物理归因；
     - **解释（Interpretation，证据中等）**：“上述计数分布与‘芯片制备出的状态存在强 $ZZ$ 关联，且主要偏差来源于双比特门及读出噪声模型’这一物理假设在统计误差范围内相容。”——已依赖噪声模型、时间平稳性假设以及对 SPAM 与漂移的建模，且同一组 $ZZ$ 观察结果仍可能由经典混态解释（须补充 $XX, YY$ 证据才能进一步解释为量子纠缠）；
     - **外推（Extrapolation，证据最弱）**：“将该线路与同类编译策略扩展到 $50$ 比特处理器后，多体关联保真度仍能保持与当前规模相近的衰减斜率。”——远远跨出了实测的 $2$ 比特参数域，暗含串扰不激增、长程路由深度不恶化、控制带宽与冷却负载不触发新瓶颈等一系列未经验证的强假设。

     用 Wilson 区间公式验算上面“观察”句中的数值（$N=4000, k=3680, \hat{p}=0.92, z=1.959964$）：分母 $1 + z^2/N \approx 1.000960$，中心 $(0.92 + 0.000480)/1.000960 \approx 0.919597$，半宽 $1.959964\sqrt{0.92\times 0.08/4000 + 3.8415/(4\times 1.6\times 10^7)}/1.000960 \approx 0.008413$，区间精确为 $[0.9112,\, 0.9280]$。
   - **结论与边界回验**：“观察”是直接可复算的实验计数与统计事实，“解释”是在特定物理/噪声模型下的相容推断，“外推”是跨越未测规模或机制区的风险预测，三者的证据强度逐级递减，撰写报告与审读论文时必须用语区分。
   - **易错坑提醒**：在摘要或结论段把“外推”写成“观察”语气（例如用 2 比特或小码距数据直接断言“证明了百万比特实用潜力”），或者在“观察”中省略总样本量与置信区间。

8. **【计算】Bell 见证三基 Hoeffding 保守下界计算（$N = 100$ vs. $N = 400$）**

   - **题意与约定**：已知两次独立实验测得的 Pauli 关联点估计完全相同：$\widehat{XX} = 0.50$、$\widehat{YY} = -0.50$、$\widehat{ZZ} = 0.60$。第一次每组采样 $N = 100$ 次，第二次每组采样 $N = 400$ 次，要求在状态稳定、测量可信及组内独立前提下，用正文 4.2 节的三组并合 Hoeffding 界构造整体 $95\%$ 覆盖的保守下界，判断哪一次能越过可分阈值 $1/2$ 见证纠缠。
   - **核心提示**：先由三组 Pauli 点估计算出 Bell 保真度点估计 $\hat f$，再用 Hoeffding 界配联合界（三组各分配显著性 $\alpha/3$，注意有界范围 $[-1,1]$ 宽为 $2$）分别求 $N=100$ 与 $N=400$ 的误差半宽，最后判断下界是否跨过可分阈值 $1/2$。
   - **完整分步演算**：
     - **第一步：计算两次实验共同的点估计**：代入 Bell 重叠公式（留意 $YY$ 项前的负号）：

       $$
       \hat{f}_{\Phi^+}
       = \frac{1 + \widehat{XX} - \widehat{YY} + \widehat{ZZ}}{4}
       = \frac{1 + 0.50 - (-0.50) + 0.60}{4}
       = \frac{2.60}{4} = 0.65.
       $$

       （对应的根保真度点估计为 $\hat{F} = \sqrt{0.65} \approx 0.8062$。）
     - **第二步：写出三组并合 Hoeffding 误差半径公式**：每组单次乘积读数取值于 $\{-1, +1\}$（范围跨度 $b - a = 2$）。由 Hoeffding 不等式，单组样本均值偏差超过 $\varepsilon$ 的概率满足 $\Pr(|\hat{c} - c| \ge \varepsilon) \le 2\exp\!\left(-\frac{2N\varepsilon^2}{(b-a)^2}\right) = 2e^{-N\varepsilon^2/2}$。利用概率并合界（不要求三组之间独立），三组中至少有一组越界的概率不超过 $3 \times 2e^{-N\varepsilon^2/2} = 6e^{-N\varepsilon^2/2}$。令该总失误概率等于 $\alpha = 0.05$，解出单组误差半径：

       $$
       6e^{-N\varepsilon_N^2 / 2} = 0.05
       \implies
       e^{N\varepsilon_N^2 / 2} = \frac{6}{0.05} = 120
       \implies
       \varepsilon_N = \sqrt{\frac{2\ln 120}{N}}.
       $$

       其中 $\ln 120 \approx 4.78749174$，故 $2\ln 120 \approx 9.57498349$。因为三项在 $f_{\Phi^+}$ 中各自乘以权重 $\pm\frac{1}{4}$，总误差绝对值至多为 $\frac{3}{4}\varepsilon_N$，保守下界为 $L_N = \hat{f}_{\Phi^+} - \frac{3}{4}\varepsilon_N$。
     - **第三步：分别代入 $N = 100$ 与 $N = 400$ 精确计算**：
       - **第一次实验（每组 $N = 100$）**：

         $$
         \varepsilon_{100} = \sqrt{\frac{9.57498349}{100}} = \sqrt{0.09574983} \approx 0.309435,
         $$

         $$
         \frac{3}{4}\varepsilon_{100} \approx 0.232076,
         \qquad
         L_{100} = 0.65 - 0.232076 = 0.417924 \approx 0.4179 < \frac{1}{2}.
         $$

         由于下界 $0.4179$ 落在可分阈值 $0.5$ 左侧，**不能**以整体 $95\%$ 覆盖保证见证纠缠！
       - **第二次实验（每组 $N = 400$）**：样本量增大 $4$ 倍，误差半径恰好缩小 $\sqrt{4} = 2$ 倍：

         $$
         \varepsilon_{400} = \frac{\varepsilon_{100}}{2} = \sqrt{\frac{9.57498349}{400}} \approx 0.154717,
         $$

         $$
         \frac{3}{4}\varepsilon_{400} \approx 0.116038,
         \qquad
         L_{400} = 0.65 - 0.116038 = 0.533962 \approx 0.5340 > \frac{1}{2}.
         $$

         （换算为本书约定的根保真度保守下界为 $\sqrt{0.533962} \approx 0.7307$。）下界稳稳越过 $0.5$，在题设独立稳定与可信测量前提下**可以见证纠缠**。
   - **结论与边界回验**：两次点估计同为 $\hat{f}_{\Phi^+} = 0.65$；每组 $N = 100$ 时保守下界为 $0.4179 < 0.5$（不能见证纠缠），每组 $N = 400$ 时保守下界为 $0.5340 > 0.5$（可以见证纠缠）。
   - **易错坑提醒**：一是点估计 $0.65 > 0.5$ 就急于宣布“证明了纠缠”，忽略有限样本误差棒仍跨过 $0.5$；二是把三组并合系数 $6$ 漏写成单组系数 $2$（漏掉多重比较校正）；三是忘记该 Hoeffding 下界只包住独立随机抽样误差，并未计入时间漂移与读出混淆系统偏差。

## 第 16 章

> 对应章节：《16｜高级算法与验证：从查询下界、统一框架到可信输出》（共 12 题）

1. **【进阶】为什么 $T$ 次预言机查询的量子算法，其接受概率多项式次数至多为 $2T$ 而不是 $T$**

   - **题意与约定**：给定输入比特串 $z = (z_0, z_1, \dots, z_{N-1}) \in \{0,1\}^N$，考查多项式法（Beals 等，2001）的核心引理。用数学归纳法先证经过 $T$ 次相位预言机调用后，量子态中每个计算基振幅 $\alpha_x(z)$ 都是关于 $z_0,\dots,z_{N-1}$ 的多元实/复多项式且次数至多为 $T$，再由 Born 规则 $P_{\mathrm{acc}}(z) = \sum_{x\in A} |\alpha_x(z)|^2$ 推出概率次数至多翻倍为 $2T$。
   - **核心提示**：用数学归纳法追踪每次预言机调用如何给各计算基振幅乘上关于输入比特的 $1$ 次多线性因子（$T$ 次查询后振幅次数至多为 $T$），再注意接受概率是若干振幅模平方之和，乘积把多项式次数翻倍。
   - **完整分步演算**：
     - **第一步：写出相位预言机的线性多项式表示**。对布尔变量 $z_j \in \{0,1\}$，相位翻转因子精确等价于一次线性式：

       $$
       (-1)^{z_j} = 1 - 2z_j \qquad (z_j = 0 \mapsto +1,\quad z_j = 1 \mapsto -1).
       $$

       若采用比特翻转预言机 $|j, b, w\rangle \mapsto |j, b\oplus z_j, w\rangle$，它可写成 $(1-z_j)|j,b,w\rangle + z_j|j,b\oplus 1,w\rangle$，矩阵元同样是关于 $z_j$ 的至多一次多项式。
     - **第二步：对查询次数 $t = 0, 1, \dots, T$ 做归纳**。
       - 初始时刻 $t = 0$，寄存器处于与输入无关的固定基态 $|0\cdots 0\rangle$，全部振幅是常数（次数 $\le 0$）；
       - 两次查询之间的任意与输入无关酉门 $U_t$ 只是把已有振幅按常复系数做线性组合，绝不会提高多项式次数；
       - 每执行第 $t$ 次预言机查询 $O_z$，每个基态分量至多乘上一个关于 $z_j$ 的一次多项式 $1 - 2z_j$（或由 $1-z_j$ 与 $z_j$ 线性混合），因此所有振幅的多项式次数至多增加 $1$。

       归纳得出：完成 $T$ 次查询并施加末段酉门 $U_T$ 后，末态 $|\psi_T(z)\rangle = \sum_x \alpha_x(z)|x\rangle$ 中，每个复振幅 $\alpha_x(z)$ 的实部与虚部均为关于 $z_0,\dots,z_{N-1}$ 且总次数 $\le T$ 的多元多项式。
     - **第三步：经 Born 规则平方导致次数至多加倍**。设接受结果集合为 $A$，则接受概率为

       $$
       P_{\mathrm{acc}}(z)
       = \sum_{x \in A} |\alpha_x(z)|^2
       = \sum_{x \in A} \alpha_x^*(z)\,\alpha_x(z)
       = \sum_{x \in A} \Bigl(\bigl[\operatorname{Re}\alpha_x(z)\bigr]^2 + \bigl[\operatorname{Im}\alpha_x(z)\bigr]^2\Bigr).
       $$

       两个次数至多为 $T$ 的多项式相乘，其乘积次数至多为 $T + T = 2T$；有限多项求和不增加最高次数，故 $\deg(P_{\mathrm{acc}}) \le 2T$。
   - **结论与边界回验**：$T$ 次预言机查询使每个复振幅成为次数至多为 $T$ 的多元多项式，而测量接受概率是振幅模平方之和（两个至多 $T$ 次多项式相乘），因而次数上界翻倍至 $2T$。
   - **易错坑提醒**：这是一条**必要次数上界**（$T \ge \frac{1}{2}\deg(P_{\mathrm{acc}})$），绝不意味着任意 $2T$ 次多元多项式都能用 $T$ 次量子查询实现（例如单次查询无法精确计算多项式次数也为 $2$ 的 2 比特 $\mathrm{AND}(z_0, z_1) = z_0 z_1$，因为还须同时满足酉性与全输入有界约束）。

2. **【基础】写出 Deutsch 问题 $\mathrm{XOR}(z_0, z_1)$ 的实多项式并在全部四组输入上验证**

   - **题意与约定**：二元异或函数 $\mathrm{XOR}(z_0, z_1) = z_0 \oplus z_1 \in \{0, 1\}$ 对应判定单比特函数 $f:\{0,1\}\to\{0,1\}$ 是常数（$z_0=z_1$，输出 $0$）还是平衡（$z_0\ne z_1$，输出 $1$）。先用布尔插值构造唯一的多线性实多项式，再通过 Deutsch 算法 $1$ 次查询后的精确振幅回验其次数恰好饱和 $2T = 2$。
   - **核心提示**：对布尔变量 $z_0,z_1\in\{0,1\}$ 构造满足模 $2$ 加法的多线性实多项式 $P(z_0,z_1)=z_0+z_1-2z_0 z_1$（或 $(z_0-z_1)^2$），再把全部四组输入逐一代入验证。
   - **完整分步演算**：对布尔变量 $z_0, z_1 \in \{0,1\}$（满足 $z_0^2 = z_0,\; z_1^2 = z_1$），仅当 $(z_0,z_1) = (1,0)$ 或 $(0,1)$ 时函数取 $1$，按多线性拉格朗日插值展开：

     $$
     p(z_0, z_1) = z_0(1 - z_1) + (1 - z_0)z_1 = z_0 + z_1 - 2z_0 z_1.
     $$

     该多项式最高项为 $-2z_0 z_1$，总次数为 $2$。从 Deutsch 算法的单次相位查询独立回验：初始制备 $|+\rangle|-\rangle$ 经 $1$ 次查询与首比特 $H$ 门后，首比特测得 $|1\rangle$ 的复振幅为 $\alpha_1(z_0,z_1) = \frac{(-1)^{z_0} - (-1)^{z_1}}{2} = \frac{(1-2z_0)-(1-2z_1)}{2} = z_1 - z_0$（次数恰为 $T=1$），其模平方为

     $$
     P(1) = |\alpha_1(z_0, z_1)|^2 = (z_1 - z_0)^2 = z_1^2 + z_0^2 - 2z_0 z_1 = z_0 + z_1 - 2z_0 z_1 = p(z_0, z_1).
     $$

     在全部四组布尔输入上逐项代入验算：
     - $(z_0, z_1) = (0, 0)$：$p(0,0) = 0 + 0 - 2\cdot 0\cdot 0 = 0 = 0\oplus 0$；
     - $(z_0, z_1) = (0, 1)$：$p(0,1) = 0 + 1 - 2\cdot 0\cdot 1 = 1 = 0\oplus 1$；
     - $(z_0, z_1) = (1, 0)$：$p(1,0) = 1 + 0 - 2\cdot 1\cdot 0 = 1 = 1\oplus 0$；
     - $(z_0, z_1) = (1, 1)$：$p(1,1) = 1 + 1 - 2\cdot 1\cdot 1 = 0 = 1\oplus 1$。
   - **结论与边界回验**：$\mathrm{XOR}(z_0, z_1)$ 的唯一多线性实多项式为 $p(z_0, z_1) = z_0 + z_1 - 2z_0 z_1$，在 $(0,0),(0,1),(1,0),(1,1)$ 上依次输出 $0, 1, 1, 0$，精确验证了 $T = 1$ 次量子查询刚好能够实现次数为 $2T = 2$ 的异或判定。
   - **易错坑提醒**：经典确定算法判定 $z_0\oplus z_1$ 需要 $2$ 次查询，而量子算法利用 $1$ 次查询的线性振幅差 $z_1 - z_0$ 经平方跨到 $2$ 次多项式；另外不要忘记多线性化时用到布尔恒等式 $z_j^2 = z_j$，若把 $z_j$ 放宽到一般实数，$z_0 + z_1 - 2z_0 z_1$ 与 $(z_1 - z_0)^2$ 并不相等。

3. **【计算】在 3 比特 Simon 问题中，求 $s = 101$ 的正交补 $H^\perp$ 的全部四个元素**

   - **题意与约定**：在群 $G = \mathbb{F}_2^3 = \{0,1\}^3$ 中，隐藏子群为 $H = \{000, s\} = \{000, 101\}$。正交补定义为 $H^\perp = \{z = z_1 z_2 z_3 \in \mathbb{F}_2^3 \mid z\cdot s = 0 \pmod 2\}$，其中模 2 内积 $z\cdot s = z_1 s_1 \oplus z_2 s_2 \oplus z_3 s_3$。逐一检验全部 $2^3 = 8$ 个比特串并做子空间维度与封闭性回验。
   - **核心提示**：先按正交补定义 $z\cdot s\equiv 0\pmod 2$ 求出全部四个元素，再结合 Abelian 隐藏子群的陪集分解与特征标求和 $\sum_{h\in H}(-1)^{z\cdot h}$ 解释傅里叶采样为何精准落在 $H^\perp$ 上。
   - **完整分步演算**：将 $s = (s_1, s_2, s_3) = (1, 0, 1)$ 代入正交条件：

     $$
     z \cdot s = (z_1 \cdot 1) \oplus (z_2 \cdot 0) \oplus (z_3 \cdot 1) = z_1 \oplus z_3 = 0 \pmod 2
     \iff z_1 = z_3.
     $$

     这意味着第 $2$ 位 $z_2 \in \{0, 1\}$ 自由取值，而首尾两位必须相等（$z_1 = z_3 \in \{0, 1\}$）。对全部 $8$ 个元素逐一核对：
     - `000`：$0 \oplus 0 = 0$（**属于 $H^\perp$**）；
     - `001`：$0 \oplus 1 = 1$（不属于）；
     - `010`：$0 \oplus 0 = 0$（**属于 $H^\perp$**）；
     - `011`：$0 \oplus 1 = 1$（不属于）；
     - `100`：$1 \oplus 0 = 1$（不属于）；
     - `101`：$1 \oplus 1 = 0$（**属于 $H^\perp$**）；
     - `110`：$1 \oplus 0 = 1$（不属于）；
     - `111`：$1 \oplus 1 = 0$（**属于 $H^\perp$**）。

     回验子空间结构：$|H^\perp| = |G|/|H| = 8/2 = 4 = 2^{3-1}$；且任取两元素按位异或仍留在集合内（例如 $010 \oplus 101 = 111$），同时注意在 $\mathbb{F}_2^3$ 上 $s = 101$ 自身满足 $101 \cdot 101 = 1 \oplus 0 \oplus 1 = 0$，故 $s$ 自己就在 $H^\perp$ 中！
     - **隐藏子群（HSP）陪集分解与 $4$ 比特拓展对照（第 16 章群论深化）**：在阿贝尔群 $G = \mathbb{F}_2^3$ 中，$H = \{000, 101\}$ 把 $G$ 精确划分为 $|G|/|H| = 4$ 个两两不相交的陪集：$\{000, 101\},\; \{001, 100\},\; \{010, 111\},\; \{011, 110\}$。对任意陪集态 $|x \oplus H\rangle = \frac{1}{\sqrt{2}}(|x\rangle + |x\oplus s\rangle)$ 施加傅里叶变换 $H_{\mathrm{gate}}^{\otimes 3}$，特征标 $\chi_z(x) = (-1)^{z\cdot x}$ 在子群 $H$ 上求和给出：

       $$
       \sum_{h\in H} (-1)^{z\cdot(x\oplus h)} = (-1)^{z\cdot x}\bigl(1 + (-1)^{z\cdot s}\bigr)
       = \begin{cases} 2(-1)^{z\cdot x}, & z\cdot s = 0\ (z \in H^\perp), \\ 0, & z\cdot s = 1\ (z \notin H^\perp). \end{cases}
       $$

       因此相消干涉直接筛出正交对偶子群 $H^\perp$。**拓展对照（4 比特奇数权重 $s' = 1011$）**：若升到 $\mathbb{F}_2^4$ 并取隐藏串 $s' = 1011$（含 $3$ 个 `1`，奇权重），则 $|H'^{\perp}| = 2^{4-1} = 8$，约束为 $z_1 \oplus z_3 \oplus z_4 = 0$（$z_2$ 自由），全部 $8$ 个元素为 $\{0000, 0100, 0011, 0111, 1001, 1101, 1010, 1110\}$；此时 $s'\cdot s' = 1\oplus 0\oplus 1\oplus 1 = 1 \ne 0$，故 $s' \notin H'^{\perp}$，与 3 比特偶权重 $s = 101 \in H^\perp$ 形成鲜明对照（区别于[第 7 章第 1 题](#第-7-章)的穷举入门视角）。
   - **结论与边界回验**：正交补的全部四个元素为 $H^\perp = \{000,\, 010,\, 101,\, 111\}$，Simon 算法每次傅里叶采样将以各 $1/4$ 概率均匀输出这四个串之一。
   - **易错坑提醒**：受实欧氏空间“非零向量不能与自己正交”的直觉误导，初学者常把 $s = 101$ 漏出 $H^\perp$——在 $\mathbb{F}_2^n$ 中，任何含偶数个 `1` 的串都与自身模 2 正交！

4. **【进阶】四元素隐藏子群算例：写出陪集态 $|C_0\rangle, |C_1\rangle$、输入混态 $\rho_H$ 并证明 $H_{\mathrm{gate}}^{\otimes 2}$ 后仅测到 `00` 或 `11`**

   - **题意与约定**：群 $G = \mathbb{F}_2^2 = \{00, 01, 10, 11\}$，隐藏子群 $H = \{00, 11\}$，隐藏函数 $f$ 在同一陪集上取常数、不同陪集取不同值。写出两个不相交陪集及对应归一化量子态，对纠缠输出寄存器做偏迹求出输入寄存器的真实密度矩阵 $\rho_H$，再将 $H_{\mathrm{gate}}^{\otimes 2}$ 逐项作用在两个陪集态上，验证 `01` 与 `10` 的振幅精确相消。
   - **核心提示**：先按 $H=\{00,11\}$ 写出两个等权归一化陪集态 $|C_0\rangle,|C_1\rangle$ 及输入混态 $\rho_H=\frac{1}{2}|C_0\rangle\langle C_0|+\frac{1}{2}|C_1\rangle\langle C_1|$，再分别施加 $H_{\mathrm{gate}}^{\otimes 2}$ 验证相消干涉使 `01` 与 `10` 振幅清零。
   - **完整分步演算**：
     - **第一步：划分陪集并写归一化陪集态**。$G$ 按 $H = \{00, 11\}$ 分解为两个陪集 $C_0 = 00 \oplus H = \{00, 11\}$ 与 $C_1 = 01 \oplus H = \{01, 10\}$，各含 $2$ 个元素，对应的归一化陪集纯态为

       $$
       |C_0\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}},
       \qquad
       |C_1\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}.
       $$

     - **第二步：对输出寄存器求偏迹得到 $\rho_H$**。执行预言机后联合纯态为 $|\Psi\rangle = \frac{1}{\sqrt{2}}|C_0\rangle|f(00)\rangle + \frac{1}{\sqrt{2}}|C_1\rangle|f(01)\rangle$。因不同陪集函数值正交（$\langle f(00)|f(01)\rangle = 0$），丢弃输出寄存器（对其偏迹）后，交叉项归零，输入寄存器处于等权**混态**：

       $$
       \rho_H = \operatorname{Tr}_{\mathrm{out}}(|\Psi\rangle\langle\Psi|)
       = \frac{1}{2}|C_0\rangle\langle C_0| + \frac{1}{2}|C_1\rangle\langle C_1|.
       $$

     - **第三步：施加 $H_{\mathrm{gate}}^{\otimes 2}$ 并展开干涉**。利用公式 $H_{\mathrm{gate}}^{\otimes 2}|x\rangle = \frac{1}{2}\sum_{z\in\{0,1\}^2} (-1)^{x\cdot z}|z\rangle$，逐项计算两个陪集态的像：

       $$
       \begin{aligned}
       H_{\mathrm{gate}}^{\otimes 2}|C_0\rangle
       &= \frac{1}{2\sqrt{2}}\Bigl[(|00\rangle+|01\rangle+|10\rangle+|11\rangle)
         + (|00\rangle-|01\rangle-|10\rangle+|11\rangle)\Bigr]
        = \frac{|00\rangle + |11\rangle}{\sqrt{2}}, \\
       H_{\mathrm{gate}}^{\otimes 2}|C_1\rangle
       &= \frac{1}{2\sqrt{2}}\Bigl[(|00\rangle-|01\rangle+|10\rangle-|11\rangle)
         + (|00\rangle+|01\rangle-|10\rangle-|11\rangle)\Bigr]
        = \frac{|00\rangle - |11\rangle}{\sqrt{2}}.
       \end{aligned}
       $$

       两支条件纯态里，$|01\rangle$ 与 $|10\rangle$ 的振幅全部精确相消为 $0$，而 $|00\rangle$ 与 $|11\rangle$ 的概率各为 $|1/\sqrt{2}|^2 = 1/2$ 与 $|\pm 1/\sqrt{2}|^2 = 1/2$。于是对混态 $\rho_H$ 施加 $H_{\mathrm{gate}}^{\otimes 2}$ 后，输出分布与陪集标签无关：

       $$
       P(00) = \frac{1}{2}\cdot\frac{1}{2} + \frac{1}{2}\cdot\frac{1}{2} = \frac{1}{2},
       \qquad
       P(11) = \frac{1}{2}\cdot\frac{1}{2} + \frac{1}{2}\cdot\frac{1}{2} = \frac{1}{2},
       \qquad
       P(01) = P(10) = 0.
       $$

       回验正交补条件：$00\cdot 11 = 0$、$11\cdot 11 = 1\oplus 1 = 0$，两串恰好构成 $H^\perp = \{00, 11\}$，且概率和 $\frac{1}{2} + \frac{1}{2} = 1$。
   - **结论与边界回验**：$|C_0\rangle = \frac{|00\rangle+|11\rangle}{\sqrt{2}}$、$|C_1\rangle = \frac{|01\rangle+|10\rangle}{\sqrt{2}}$、$\rho_H = \frac{1}{2}|C_0\rangle\langle C_0| + \frac{1}{2}|C_1\rangle\langle C_1|$；经 $H_{\mathrm{gate}}^{\otimes 2}$ 后两个陪集分支均只在 $H^\perp = \{00, 11\}$ 上有非零振幅（各占 $1/2$），因此最终只能测得 `00` 或 `11`。
   - **易错坑提醒**：不要把丢弃输出后的 $\rho_H$ 误写成纯态叠加 $\frac{1}{\sqrt{2}}(|C_0\rangle+|C_1\rangle)$（后者是均匀态，经 $H^{\otimes 2}$ 只出 `00`）；输出寄存器与输入纠缠后丢弃，必然得到统计混合态，只是 $H_{\mathrm{gate}}^{\otimes 2}$ 把陪集平移变成了不影响测量概率的相对相位（$\pm 1$）。

5. **【计算】四环带硬币量子行走走两步后，哪一项的负号会影响后续步骤的干涉**

   - **题意与约定**：四顶点环 $V = \{0,1,2,3\}$ 配二维硬币空间 $\{|R\rangle, |L\rangle\}$，每步演化为 $W_{\mathrm{step}} = S(I_V\otimes C)$，其中 Hadamard 硬币满足 $C|R\rangle = \frac{|R\rangle+|L\rangle}{\sqrt{2}}$、$C|L\rangle = \frac{|R\rangle-|L\rangle}{\sqrt{2}}$，条件移位 $S|v,R\rangle = |v+1\bmod 4, R\rangle$、$S|v,L\rangle = |v-1\bmod 4, L\rangle$。从 $|\psi_0\rangle = |0, R\rangle$ 零跳步算至第 $3$ 步，亲眼见证该负号如何触发第 $3$ 步的完全相消干涉。
   - **核心提示**：固定每步演化 $W_{\mathrm{step}}=S(I_V\otimes H_{\mathrm{coin}})$，从 $|0,R\rangle$ 出发严格展开第 $1$ 步与第 $2$ 步的各顶点—硬币分支（牢记 $H|L\rangle=(|R\rangle-|L\rangle)/\sqrt{2}$ 带负号），定位带负号的分支项。
   - **完整分步演算**：
     - **第 1 步**：先硬币旋转再移位（注意 $0 - 1 \equiv 3 \pmod 4$）：

       $$
       |\psi_0\rangle = |0, R\rangle
       \xrightarrow{C} \frac{|0, R\rangle + |0, L\rangle}{\sqrt{2}}
       \xrightarrow{S} |\psi_1\rangle = \frac{|1, R\rangle + |3, L\rangle}{\sqrt{2}}.
       $$

     - **第 2 步**：分别演化两条分支（特别注意 $C|L\rangle$ 带来的负号）：

       $$
       |1, R\rangle \xrightarrow{C} \frac{|1, R\rangle + |1, L\rangle}{\sqrt{2}} \xrightarrow{S} \frac{|2, R\rangle + |0, L\rangle}{\sqrt{2}},
       $$

       $$
       |3, L\rangle \xrightarrow{C} \frac{|3, R\rangle - |3, L\rangle}{\sqrt{2}} \xrightarrow{S} \frac{|0, R\rangle - |2, L\rangle}{\sqrt{2}}.
       $$

       合并两支（各乘权重 $1/\sqrt{2}$），得精确两步态：

       $$
       |\psi_2\rangle = \frac{1}{2}\Bigl(|0, R\rangle + |0, L\rangle + |2, R\rangle - |2, L\rangle\Bigr).
       $$

       归一化回验：$4\times (1/2)^2 = 1$。关键负号就在 **$-|2, L\rangle$** 一项前！虽然此刻测位置仍得 $P(0) = P(2) = 1/2$，但推进到**第 3 步**时差异立现：
     - **第 3 步（干涉验证）**：对 $|\psi_2\rangle$ 再次施加 $C$，在顶点 $0$ 处 $|R\rangle+|L\rangle \xrightarrow{C} \sqrt{2}|R\rangle$（朝左相消）；在顶点 $2$ 处正因为有负号，$|R\rangle - |L\rangle \xrightarrow{C} \sqrt{2}|L\rangle$（朝右相消！）。随后条件移位 $S$ 把 $|0, R\rangle \mapsto |1, R\rangle$、$|2, L\rangle \mapsto |1, L\rangle$：

       $$
       |\psi_3\rangle = \frac{1}{2}\bigl(\sqrt{2}|1, R\rangle + \sqrt{2}|1, L\rangle\bigr) = \frac{|1, R\rangle + |1, L\rangle}{\sqrt{2}}.
       $$

       于是顶点 $3$ 概率精确相消为 $0$，全部 $100\%$ 概率汇聚到顶点 $1$（若抹掉该负号，两顶点朝右分支相加将均匀散落至顶点 $1$ 和 $3$）。
   - **结论与边界回验**：走两步后的态为 $|\psi_2\rangle = \frac{1}{2}(|0,R\rangle + |0,L\rangle + |2,R\rangle - |2,L\rangle)$，其中 **$-|2, L\rangle$** 项前的负号（源于 $C|L\rangle = (|R\rangle - |L\rangle)/\sqrt{2}$）决定了第 3 步在顶点 $2$ 处朝右分支完全相消、使全部概率汇集到顶点 $1$。
   - **易错坑提醒**：只看第 $2$ 步的位置概率分布 $P(0)=P(2)=1/2$ 就以为负号无关紧要，忘记硬币态与位置态纠缠携带的相对相位会在后续硬币算符混合路径时引发强烈相长/相消干涉。

6. **【进阶】为何元素互异性的 $O(N^{2/3})$ 不是“对数对做 Grover”？求 $N=4, r=2$ 时的标记占比 $\varepsilon$**

   - **题意与约定**：对比两种算法结构：① 对全部 $\binom{N}{2}$ 个数对直接套用 Grover 搜索的查询复杂度；② Ambainis / MNRS 量子行走在 Johnson 图 $J(N, r)$ 上复用已查询元素表的三段成本优化公式 $O(S + \frac{1}{\sqrt{\varepsilon}}(C + \frac{1}{\sqrt{\delta}}U))$。再对 $N=4, r=2$ 逐一列举全部子集验证标记占比 $\varepsilon$。
   - **核心提示**：先算出对全部 $\binom{N}{2}=\Theta(N^2)$ 个数对直接套 Grover 所需的查询量级（与 $O(N^{2/3})$ 对照），再用 Johnson 图 $J(N,r)$ 顶点总数 $\binom{N}{r}$ 与含唯一碰撞对的标记顶点数 $\binom{N-2}{r-2}$ 之比求 $\varepsilon$。
   - **完整分步演算**：
     - **第一部分：为何不是对数对直接做 Grover**。$N$ 个元素共有 $M = \binom{N}{2} = \frac{N(N-1)}{2} = \Theta(N^2)$ 个无序数对。若直接把每个数对当作 Grover 搜索项、每次检验需查询一对下标的值，则查询复杂度为 $O(\sqrt{M}) = O(\sqrt{N^2}) = O(N)$，相对经典 $O(N)$ 根本没有多项式查询加速！
     - **Ambainis 量子行走的 $O(N^{2/3})$ 加速机理**：算法在 Johnson 图 $J(N, r)$ 上行走——每个顶点维护一个大小为 $r$ 的已查询下标子集及其对应函数值。
       - 初始建表成本：$S = r$ 次查询；
       - 检查当前子集内是否含相等元素：无需新查询，$C = 0$；
       - 相邻顶点只替换 $1$ 个元素，单步更新成本：$U = O(1)$ 次查询；
       - Johnson 图的谱隙为 $\delta = \Theta(1/r)$，唯一碰撞对同时落入随机 $r$-子集的标记占比为

         $$
         \varepsilon = \frac{\binom{N-2}{r-2}}{\binom{N}{r}} = \frac{r(r-1)}{N(N-1)} = \Theta\!\left(\frac{r^2}{N^2}\right).
         $$

       代入 MNRS 总查询公式并令建表成本与行走成本平衡：

       $$
       Q = O\!\left(r + \frac{1}{\sqrt{r^2/N^2}}\cdot\frac{1}{\sqrt{1/r}}\right)
       = O\!\left(r + \frac{N}{\sqrt{r}}\right)
       \xrightarrow{\;r = N/\sqrt{r}\;\Rightarrow\; r = N^{2/3}\;}
       Q = O(N^{2/3}).
       $$

       可见加速来自相邻子集间的**信息复用（增量更新）**，而非对全部数对做无结构 Grover。
     - **第二部分：$N = 4, r = 2$ 的精确穷举验证**。令四个下标为 $\{1,2,3,4\}$，不妨设唯一相等的一对在 $\{1, 2\}$。大小为 $r=2$ 的全部子集共 $\binom{4}{2} = 6$ 个：$\{1,2\}, \{1,3\}, \{1,4\}, \{2,3\}, \{2,4\}, \{3,4\}$。其中同时包含 $1$ 和 $2$ 的标记子集恰有 $1$ 个（即 $\{1,2\}$），故标记占比为

       $$
       \varepsilon = \frac{1}{6}
       \qquad\text{（公式复验：}\frac{r(r-1)}{N(N-1)} = \frac{2\times 1}{4\times 3} = \frac{2}{12} = \frac{1}{6}\text{）}.
       $$

   - **结论与边界回验**：直接对 $\binom{N}{2}$ 数对做 Grover 仅得 $O(N)$ 查询，元素互异性的 $O(N^{2/3})$ 加速源于在 Johnson 图 $J(N, r)$ 上复用已查询表并平衡 $r$ 与 $N/\sqrt{r}$；当 $N = 4, r = 2$ 且恰有一对相等值时，标记子集占比 $\varepsilon = \frac{1}{6}$。
   - **易错坑提醒**：误以为 Grover 搜一切都能直接开平方根成 $O(N^{2/3})$，或者误把 $r$ 当成自由调到很小的常数（若 $r = O(1)$ 则 $\varepsilon = O(1/N^2)$，查询退回 $O(N)$）；同时注意 $O(N^{2/3})$ 是查询复杂度，不自动等于未计入量子存储器访问成本的门复杂度。

7. **【计算】构造 $H = 0.6X + 0.8Z$ 的 LCU 块编码 $\operatorname{PREPARE}$ / $\operatorname{SELECT}$ 并计算辅助位成功概率与条件态**

   - **题意与约定**：对 $H = \alpha_0 X + \alpha_1 Z$（$\alpha_0 = 0.6,\; \alpha_1 = 0.8 > 0$），引入 1 个辅助比特与 1 个系统比特（4 维空间，大端序 $|q_{\mathrm{anc}} q_{\mathrm{sys}}\rangle$）。先算 $L_1$ 归一化因子 $\lambda = \alpha_0 + \alpha_1$，构造满足 $\operatorname{PREPARE}|0\rangle = \sum_j \sqrt{\alpha_j/\lambda}|j\rangle$ 的 $2\times 2$ 酉矩阵与受控酉算符 $\operatorname{SELECT}$，验证 $W_{\mathrm{LCU}} = (\operatorname{PREPARE}^\dagger \otimes I)\operatorname{SELECT}(\operatorname{PREPARE}\otimes I)$ 的左上 $2\times 2$ 块恰为 $H/\lambda$，再代入初态 $|0\rangle_{\mathrm{anc}}|0\rangle_{\mathrm{sys}}$ 求辅助位测得 $0$ 的概率及归一化条件态。
   - **核心提示**：先求 1-范数 $\alpha=\alpha_0+\alpha_1$ 并按 $\operatorname{PREPARE}|0\rangle=\sqrt{\alpha_0/\alpha}|0\rangle+\sqrt{\alpha_1/\alpha}|1\rangle$ 与 $\operatorname{SELECT}=|0\rangle\langle 0|\otimes X+|1\rangle\langle 1|\otimes Z$ 组装 $4\times 4$ 酉阵，验证左上块等于 $H/\alpha$ 后计算辅助位测得 $|0\rangle$ 的概率。
   - **完整分步演算**：
     - **第一步：计算 $\lambda$ 并构造 $\operatorname{PREPARE}$ 与 $\operatorname{SELECT}$**。权重之和为 $\lambda = 0.6 + 0.8 = 1.4$，归一权重 $\frac{0.6}{1.4} = \frac{3}{7}$、$\frac{0.8}{1.4} = \frac{4}{7}$。取实正交酉补全：

       $$
       \operatorname{PREPARE} = \begin{pmatrix} \sqrt{3/7} & -\sqrt{4/7} \\ \sqrt{4/7} & \sqrt{3/7} \end{pmatrix},
       \qquad
       \operatorname{PREPARE}|0\rangle = \sqrt{\frac{3}{7}}|0\rangle + \sqrt{\frac{4}{7}}|1\rangle,
       $$

       $$
       \operatorname{SELECT} = |0\rangle\langle 0| \otimes X + |1\rangle\langle 1| \otimes Z
       = \begin{pmatrix} X & 0 \\ 0 & Z \end{pmatrix}.
       $$

     - **第二步：验证左上 $2\times 2$ 块精确等于 $H/\lambda$**。提取 $W_{\mathrm{LCU}}$ 在辅助位 $|0\rangle$ 上的左上块 $(\langle 0|\otimes I) W_{\mathrm{LCU}} (|0\rangle\otimes I)$：

       $$
       \begin{aligned}
       (\langle 0|\otimes I) W_{\mathrm{LCU}} (|0\rangle\otimes I)
       &= \Bigl(\sqrt{\tfrac{3}{7}}\langle 0| + \sqrt{\tfrac{4}{7}}\langle 1|\Bigr)
          \bigl(|0\rangle\langle 0|\otimes X + |1\rangle\langle 1|\otimes Z\bigr)
          \Bigl(\sqrt{\tfrac{3}{7}}|0\rangle + \sqrt{\tfrac{4}{7}}|1\rangle\Bigr) \\
       &= \frac{3}{7}X + \frac{4}{7}Z
        = \frac{0.6X + 0.8Z}{1.4}
        = \frac{H}{\lambda}.
       \end{aligned}
       $$

     - **第三步：作用在初态 $|0\rangle$ 上求成功概率与条件后态**。系统初态为 $|0\rangle$，辅助位测得 $0$ 对应的未归一化系统分支为

       $$
       |\tilde{\psi}_0\rangle
       = \frac{H}{\lambda}|0\rangle
       = \left(\frac{3}{7}X + \frac{4}{7}Z\right)|0\rangle
       = \frac{3}{7}|1\rangle + \frac{4}{7}|0\rangle
       = \frac{4}{7}|0\rangle + \frac{3}{7}|1\rangle.
       $$

       因此辅助位测得 $0$ 的成功概率为其平方范数：

       $$
       p_0 = \|\tilde{\psi}_0\|^2 = \left(\frac{4}{7}\right)^2 + \left(\frac{3}{7}\right)^2 = \frac{16 + 9}{49} = \frac{25}{49} \approx 0.5102.
       $$

       将 $|\tilde{\psi}_0\rangle$ 除以 $\sqrt{p_0} = 5/7$ 得到归一化条件系统态：

       $$
       |\psi_{\mathrm{cond}}\rangle = \frac{|\tilde{\psi}_0\rangle}{5/7} = \frac{4}{5}|0\rangle + \frac{3}{5}|1\rangle.
       $$

       回验归一化：$(4/5)^2 + (3/5)^2 = 16/25 + 9/25 = 1$（且因 $H^2 = (0.6^2+0.8^2)I = I$ 恰好是酉矩阵，故 $\|H|0\rangle\| = 1$，成功概率恰好等于 $1/\lambda^2 = 1/1.4^2 = 25/49$！）。
   - **结论与边界回验**：$\lambda = 1.4$，$\operatorname{PREPARE}|0\rangle = \sqrt{3/7}|0\rangle + \sqrt{4/7}|1\rangle$，$\operatorname{SELECT} = |0\rangle\langle 0|\otimes X + |1\rangle\langle 1|\otimes Z$，左上块恰为 $H/1.4$；系统初态为 $|0\rangle$ 时，辅助位测得 $0$ 的概率为 $p_0 = \frac{25}{49} \approx 51.02\%$，归一化条件系统态为 $\frac{4}{5}|0\rangle + \frac{3}{5}|1\rangle$。
   - **易错坑提醒**：切忌把 $\operatorname{PREPARE}$ 的权重 $3/7$ 与 $4/7$ 误当成系统输出态测量得 $|1\rangle$ 与 $|0\rangle$ 的最终概率（它们是未归一化叠加振幅系数，真正概率需先做线性叠加再按模平方除以 $p_0$ 得 $9/25$ 与 $16/25$）。

8. **【基础】对 $A = \operatorname{diag}(1, 0)$ 计算 $T_2(A) = 2A^2 - I$，并说明矩阵多项式为何不是逐元素代入**

   - **题意与约定**：按照线性代数中矩阵多项式的严格定义，对于多项式 $P(x) = \sum_{k=0}^d c_k x^k$，矩阵多项式是 $P(A) = \sum_{k=0}^d c_k A^k$（其中 $A^0 = I$，常数项乘单位矩阵而非全 1 矩阵）。先逐格算出 $T_2(A)$，再与错误的逐元素代入以及一般非对角矩阵对比，并顺带点明 QSVT 实部提取中的同源误区。
   - **核心提示**：按矩阵多项式定义先算矩阵平方 $A^2$ 再算 $2A^2-I$；对比逐元素代入 $2a_{ij}^2-1$ 会破坏单位阵非对角零元，再从特征谱视角说明矩阵多项式本质上是作用在特征值上。
   - **完整分步演算**：给定 $A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$，先算矩阵平方 $A^2 = A\cdot A$：

     $$
     A^2 = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}
     = \begin{pmatrix} 1\cdot 1 + 0\cdot 0 & 1\cdot 0 + 0\cdot 0 \\ 0\cdot 1 + 0\cdot 0 & 0\cdot 0 + 0\cdot 0 \end{pmatrix}
     = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} = A.
     $$

     再代入 $T_2(A) = 2A^2 - I$（注意常数项 $-1$ 对应 $-1\cdot I = \begin{pmatrix}-1 & 0\\ 0 & -1\end{pmatrix}$）：

     $$
     T_2(A) = 2\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} - \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
     = \begin{pmatrix} 2 - 1 & 0 - 0 \\ 0 - 0 & 0 - 1 \end{pmatrix}
     = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} = \operatorname{diag}(1, -1).
     $$

     **对比两种常见误算**：
     - 若错误地把 $A$ 的四个矩阵元逐个代入 $T_2(x) = 2x^2 - 1$，会把两个非对角元 $0$ 也代成 $T_2(0) = -1$，错算成 $\begin{pmatrix}1 & -1 \\ -1 & -1\end{pmatrix}$；
     - 若矩阵不是对角阵（例如 $A = X$），其本征值为 $\pm 1$，按矩阵乘法 $T_2(X) = 2X^2 - I = 2I - I = I$，而逐元素代入会得出彻底错误的矩阵！只有当 $A = U\Lambda U^\dagger$ 谱分解后，才有 $P(A) = U\,P(\Lambda)\,U^\dagger$，即多项式作用在**本征值**（对非厄米矩阵则为奇异值）上，而非原基下的每个矩阵元上。

     类似的矩阵结构陷阱也出现在 QSVT 提取目标实多项式 $P_{\mathrm{Re}}(A)$ 时：QSVT 线路左上块为 $P_{\mathrm{Re}}(A) + i P_{\mathrm{Im}}(A)$，若 $A$ 为一般复厄米矩阵，直接对 $U_\Phi$ 逐元素取实部 $\operatorname{Re} U_\Phi$ 会连同 $P_{\mathrm{Re}}(A)$ 自身的复非对角元一并破坏，正确做法是通过翻转相位序列 $\Phi \mapsto -\Phi$ 构造 $\frac{1}{2}(U_\Phi + U_{-\Phi})$ 来精确消去左上块伴随虚部 $i P_{\mathrm{Im}}(A)$。
   - **结论与边界回验**：$T_2(A) = \operatorname{diag}(1, -1)$；矩阵多项式由矩阵幂次线性组合定义（等价于在谱分解下作用于本征值，且常数项乘单位阵 $I$），绝不是把标量多项式逐元素套用到矩阵的每个位置。
   - **易错坑提醒**：一是误把常数项 $-1$ 作用到矩阵所有元素上（连非对角 $0$ 也减 $1$）；二是忘记检查 $A$ 是否厄米——若 $A$ 非厄米，奇异值变换作用在奇异值而非特征值上（例如正文 $A^2 = 0$ 而 $A^\dagger A \ne 0$ 反例）。

9. **【计算】计算 $x = 1/2$ 时 $W(x)^2$ 的左上角振幅及信号比特初态 $|0\rangle$ 测得 $0$ 的概率**

   - **题意与约定**：按正文 5.5 节 QSP 信号算符约定 $W(x) = \begin{pmatrix} x & i\sqrt{1 - x^2} \\ i\sqrt{1 - x^2} & x \end{pmatrix}$（$x \in [-1, 1]$），先对一般 $x$ 零跳步做矩阵乘法 $W(x)^2$，识别出左上角恰为二阶切比雪夫多项式 $T_2(x) = 2x^2 - 1$，再代入 $x = 1/2$ 分别求出振幅与测量概率并核验归一化。
   - **核心提示**：先做 $2\times 2$ 矩阵乘法算出 $W(x)^2$ 的一般代数表达式（观察其左上角恰为第二类/第一类 Chebyshev 多项式 $T_2(x)=2x^2-1$），再代入 $x=1/2$ 并对振幅取模平方求概率。
   - **完整分步演算**：记 $s = \sqrt{1 - x^2}$（实数，满足 $s^2 = 1 - x^2$），按矩阵乘法逐元展开 $W(x)^2$：

     $$
     \begin{aligned}
     W(x)^2
     &= \begin{pmatrix} x & is \\ is & x \end{pmatrix}
        \begin{pmatrix} x & is \\ is & x \end{pmatrix}
      = \begin{pmatrix} x\cdot x + (is)(is) & x(is) + (is)x \\ (is)x + x(is) & (is)(is) + x\cdot x \end{pmatrix} \\
     &= \begin{pmatrix} x^2 - s^2 & 2ixs \\ 2ixs & x^2 - s^2 \end{pmatrix}
      = \begin{pmatrix} 2x^2 - 1 & 2ix\sqrt{1 - x^2} \\ 2ix\sqrt{1 - x^2} & 2x^2 - 1 \end{pmatrix}.
     \end{aligned}
     $$

     可见左上角矩阵元精确等于 $T_2(x) = 2x^2 - 1$。代入 $x = \frac{1}{2}$，此时 $s = \sqrt{1 - \frac{1}{4}} = \frac{\sqrt{3}}{2}$：

     $$
     W\!\left(\frac{1}{2}\right)^2
     = \begin{pmatrix} 2\left(\frac{1}{2}\right)^2 - 1 & 2i\left(\frac{1}{2}\right)\left(\frac{\sqrt{3}}{2}\right) \\ 2i\left(\frac{1}{2}\right)\left(\frac{\sqrt{3}}{2}\right) & 2\left(\frac{1}{2}\right)^2 - 1 \end{pmatrix}
     = \begin{pmatrix} -\frac{1}{2} & i\frac{\sqrt{3}}{2} \\ i\frac{\sqrt{3}}{2} & -\frac{1}{2} \end{pmatrix}.
     $$

     信号比特从初态 $|0\rangle = \begin{pmatrix}1\\ 0\end{pmatrix}$ 出发，演化后的末态为

     $$
     W\!\left(\frac{1}{2}\right)^2|0\rangle = -\frac{1}{2}|0\rangle + i\frac{\sqrt{3}}{2}|1\rangle.
     $$

     按 Born 规则计算两个计算基结果的概率并回验总和：

     $$
     P(0) = \left|-\frac{1}{2}\right|^2 = \frac{1}{4} = 0.25,
     \qquad
     P(1) = \left|i\frac{\sqrt{3}}{2}\right|^2 = \frac{3}{4} = 0.75,
     \qquad
     P(0) + P(1) = \frac{1}{4} + \frac{3}{4} = 1.
     $$

   - **结论与边界回验**：$W(1/2)^2$ 的左上角复振幅为 $T_2(1/2) = -\frac{1}{2}$；从 $|0\rangle$ 出发最终测得 $0$ 的概率为 $\left|-\frac{1}{2}\right|^2 = \frac{1}{4}$（测得 $1$ 的概率为 $\frac{3}{4}$）。
   - **易错坑提醒**：一是看到左上角 $-1/2$ 带负号便误以为算出了“负概率”，忘记它是量子振幅、概率须取模平方；二是把 QSP 矩阵左下角的补多项式 $i Q(x)\sqrt{1-x^2}$ 与一般含相位 QSVT 左上块自身伴随虚部 $i P_{\mathrm{Im}}(A)$ 混为一谈。

10. **【基础】算法总误差预算 $10^{-3}$ 下的剩余误差份额核算**

    - **题意与约定**：依据正文第 6.1 节的算符范数/迹距离三角不等式 $\varepsilon_{\mathrm{tot}} \le \sum_{k=1}^6 \varepsilon_k$，全书将端到端量子算法拆成六类叠加误差源。扣除已占用的两项预算后，求出其余四类误差源能够**共同分享**的剩余总上限，并点明后选择条件下的放大效应。
    - **核心提示**：利用总误差三角不等式 $\varepsilon_{\mathrm{tot}}\le\sum_{k=1}^6\varepsilon_k$，从总预算中扣除已分配的截断与初态准备两项，得出其余四类误差源之和的硬上限。
    - **完整分步演算**：端到端任务通常包含六类主要误差源：① 物理/数学模型截断误差 $\varepsilon_{\mathrm{model}}$；② 初态制备误差 $\varepsilon_{\mathrm{prep}}$；③ 算法近似误差（如 Trotter、LCU 或 QSVT 多项式截断）$\varepsilon_{\mathrm{alg}}$；④ 离散门综合误差（如 Clifford+$T$ 近似）$\varepsilon_{\mathrm{synth}}$；⑤ 有限采样统计误差 $\varepsilon_{\mathrm{stat}}$；⑥ 硬件与容错逻辑残余误差 $\varepsilon_{\mathrm{hw}}$。由三角不等式保底约束：

      $$
      \varepsilon_{\mathrm{model}} + \varepsilon_{\mathrm{prep}} + \varepsilon_{\mathrm{alg}} + \varepsilon_{\mathrm{synth}} + \varepsilon_{\mathrm{stat}} + \varepsilon_{\mathrm{hw}} \le \varepsilon_{\mathrm{tot}} = 10^{-3}.
      $$

      代入已分配的 $\varepsilon_{\mathrm{model}} = 4\times 10^{-4}$ 与 $\varepsilon_{\mathrm{prep}} = 2\times 10^{-4}$：

      $$
      \varepsilon_{\mathrm{alg}} + \varepsilon_{\mathrm{synth}} + \varepsilon_{\mathrm{stat}} + \varepsilon_{\mathrm{hw}}
      \le 10^{-3} - 4\times 10^{-4} - 2\times 10^{-4}
      = (10 - 4 - 2)\times 10^{-4}
      = 4\times 10^{-4}.
      $$

      若将这 $4\times 10^{-4}$ 在四类误差间平均分配，每类仅能分到 $1\times 10^{-4}$（总预算的 $1/10$）。此外，如果算法末尾存在成功概率为 $p$ 的后选择步骤（见正文 5.8 节），进入后选择前的块编码或门误差 $\epsilon$ 还会被放大至最坏 $2\epsilon/\sqrt{p}$ 量级，此时在预算分配上必须提前按 $\sqrt{p}/2$ 反向收紧上游误差上限。
    - **结论与边界回验**：其余四类误差源（算法近似、门综合、有限采样、硬件/逻辑噪声）**合计**最多可分享 $4\times 10^{-4}$ 的误差预算（若均分每类仅 $1\times 10^{-4}$），绝不是每一项各自都能用满 $4\times 10^{-4}$。
    - **易错坑提醒**：只盯着自己设计的单模块（例如把门综合误差或 Trotter 误差单独卡在目标 $10^{-3}$），忘记所有六类误差会沿电路串联累加，导致整机端到端总误差严重超标。

11. **【进阶】单比特随机泡利经典阴影估计 $|0\rangle$ 的 $\langle Z\rangle$：均值、方差与 $200$ 次平均标准差**

    - **题意与约定**：先由单比特随机泡利测量信道 $\mathcal{M}_1(\rho) = \frac{1}{3}\rho + \frac{1}{3}I$ 反解出逆信道 $\mathcal{M}_1^{-1}(\sigma) = 3\sigma - I$，逐一写出测中 $Z, X, Y$ 基时的单次快照 $\hat{\rho}$ 与估计量 $\hat{Z} = \operatorname{Tr}(Z\hat{\rho})$ 的离散分布，再算均值、方差与 $200$ 次独立平均的标准差，最后对照全局 $n$ 比特 Clifford 逆信道及其无迹方差界。
    - **核心提示**：由单比特随机泡利测量逆信道 $\mathcal M_1^{-1}(X)=3X-I$ 写出单次快照估计量 $\hat Z=\operatorname{Tr}(Z\hat\rho)$ 在 $X,Y,Z$ 三种基下的取值与概率分布，求均值、方差并除以 $M=200$ 开根号得均值标准差。
    - **完整分步演算**：待测真态为 $\rho = |0\rangle\langle 0|$，真值 $\langle Z\rangle = \operatorname{Tr}(Z|0\rangle\langle 0|) = 1$。单次阴影实验以各 $1/3$ 概率均匀随机选取测量基 $b \in \{X, Y, Z\}$，得到坍缩本征态 $|\phi\rangle$ 后构造单张经典阴影快照 $\hat{\rho} = \mathcal{M}_1^{-1}(|\phi\rangle\langle\phi|) = 3|\phi\rangle\langle\phi| - I$：
      - **选中 $Z$ 基（概率 $1/3$）**：因初态就是 $|0\rangle$，必测得 $|0\rangle$。此时快照为 $\hat{\rho} = 3|0\rangle\langle 0| - I = \operatorname{diag}(2, -1)$（迹为 $2 + (-1) = 1$），对应估计量：

        $$
        \hat{Z} = \operatorname{Tr}\bigl(Z\,\operatorname{diag}(2, -1)\bigr) = (+1)(2) + (-1)(-1) = 3.
        $$

      - **选中 $X$ 或 $Y$ 基（合并概率 $2/3$）**：无论测到 $|+\rangle,|-\rangle$ 还是 $|+i\rangle,|-i\rangle$，均有 $\langle\phi|Z|\phi\rangle = 0$ 且 $\operatorname{Tr}(Z) = 0$，因此：

        $$
        \hat{Z} = \operatorname{Tr}\bigl(Z(3|\phi\rangle\langle\phi| - I)\bigr) = 3\langle\phi|Z|\phi\rangle - \operatorname{Tr}(Z) = 0.
        $$

      由离散分布 $\Pr(\hat{Z}=3) = 1/3,\; \Pr(\hat{Z}=0) = 2/3$ 逐步求一阶矩、二阶矩与方差：

      $$
      \mathbb{E}[\hat{Z}] = \frac{1}{3}\times 3 + \frac{2}{3}\times 0 = 1,
      \qquad
      \mathbb{E}[\hat{Z}^2] = \frac{1}{3}\times 3^2 + \frac{2}{3}\times 0^2 = \frac{9}{3} = 3,
      $$

      $$
      \operatorname{Var}(\hat{Z}) = \mathbb{E}[\hat{Z}^2] - \bigl(\mathbb{E}[\hat{Z}]\bigr)^2 = 3 - 1^2 = 2.
      $$

      对 $n = 200$ 次独立重复测量的样本均值 $\overline{Z}_{200} = \frac{1}{200}\sum_{t=1}^{200} \hat{Z}_t$：

      $$
      \operatorname{Var}(\overline{Z}_{200}) = \frac{\operatorname{Var}(\hat{Z})}{200} = \frac{2}{200} = 0.01,
      \qquad
      \operatorname{SD}(\overline{Z}_{200}) = \sqrt{0.01} = 0.1.
      $$

      **跨系综结构回验**：对照正文 7.3 节全局 $n$ 比特 Clifford 2-design 逆信道 $\mathcal{M}_{\mathrm{Cl}}^{-1}(X) = (2^n + 1)X - \operatorname{Tr}(X)I$，当 $n = 1$ 时恰退化为 $(2^1+1)X - \operatorname{Tr}(X)I = 3X - \operatorname{Tr}(X)I$，完全一致；并且全局 Clifford 阴影方差上界为 $3\operatorname{Tr}(O_0^2)$，其中 $O_0 = O - \frac{\operatorname{Tr}(O)}{2^n}I$ 为**无迹算符**（若 $O=Z$ 本身无迹，得 $3\operatorname{Tr}(Z^2)=6 \ge \operatorname{Var}(\hat{Z})=2$；若 $O=I$ 则 $O_0=0$，精确给出零方差，绝不可漏去迹项）。
    - **结论与边界回验**：单次估计量满足 $\mathbb{E}[\hat{Z}] = 1$、$\operatorname{Var}(\hat{Z}) = 2$；独立重复 $200$ 次取平均后的标准差为 $0.1$。
    - **易错坑提醒**：一是看到单次快照 $\hat{\rho}=\operatorname{diag}(2,-1)$ 含负特征值、单次估计 $\hat{Z}=3>1$ 就怀疑算错——单张快照不是物理态，只用来保证线性期望无偏；二是把标准差 $0.1$ 误当成“95% 置信误差界”或包含读出系统偏差的总误差。

12. **【计算】能量—能隙证书：求基态占据下界 $f_0$、根保真度下界 $F_0$ 与全部依赖前提**

    - **题意与约定**：设有限维厄米哈密顿量 $H$ 的非简并基态为 $|\psi_0\rangle$（本征能 $E_0$），第一激发态本征能为 $E_1 = E_0 + \Delta$（能隙 $\Delta > 0$）。先从谱分解零跳步证明不等式 $f_0 \ge 1 - \frac{E - E_0}{\Delta}$，再代入 $E - E_0 \le 0.03,\; \Delta = 0.20$ 算清基态占据概率（平方保真度）与本书根保真度下界，最后逐条列出证书生效的硬前提。
    - **核心提示**：把态在哈密顿量本征基下展开，对所有激发态应用 $E_k\ge E_0+\Delta$ 导出 Markov 型不等式 $1-f_0\le(E-E_0)/\Delta$，反解基态占据下界 $f_0$ 并开平方根得本书根保真度下界 $F_0$。
    - **完整分步演算**：将 $H$ 谱分解为 $H = \sum_{k \ge 0} E_k |\psi_k\rangle\langle\psi_k|$，其中 $E_0 < E_1 \le E_2 \le \cdots$ 且 $\Delta = E_1 - E_0 > 0$。对任意待检验量子态 $\rho$，记各本征态占据概率为 $p_k = \langle\psi_k|\rho|\psi_k\rangle \ge 0$（满足 $\sum_{k\ge 0} p_k = 1$，其中 $f_0 \equiv p_0 = \langle\psi_0|\rho|\psi_0\rangle$）。展开期望能量差 $E - E_0 = \operatorname{Tr}(H\rho) - E_0$：

      $$
      E - E_0 = \sum_{k \ge 0} (E_k - E_0)\, p_k = \sum_{k \ge 1} (E_k - E_0)\, p_k \ge \Delta \sum_{k \ge 1} p_k = \Delta(1 - f_0).
      $$

      因 $\Delta > 0$，两边同除 $\Delta$ 并移项立得基态占据（平方重叠）下界：

      $$
      f_0 \ge 1 - \frac{E - E_0}{\Delta}.
      $$

      代入本题数值 $E - E_0 \le 0.03$ 与 $\Delta = 0.20$：

      $$
      f_0 \ge 1 - \frac{0.03}{0.20} = 1 - 0.15 = 0.85.
      $$

      因基态唯一（非简并），按本书统一的根保真度口径 $F_0 = F(\rho, |\psi_0\rangle\langle\psi_0|) = \sqrt{\langle\psi_0|\rho|\psi_0\rangle} = \sqrt{f_0}$，开平方得：

      $$
      F_0 \ge \sqrt{0.85} \approx 0.921954 \approx 0.922.
      $$

      **该证书依赖的四条硬前提**：① 基态必须**非简并**（若基态简并，只能约束落入整个基态子空间的总权重 $\operatorname{Tr}(P_0\rho) \ge 0.85$，不能称为与某一个特定基态的根保真度）；② 已知的基态能量 $E_0$（或其可靠下界）与能隙下界 $\Delta$ 必须经严格理论/数值认证（不能靠猜测）；③ 实测能量 $E$ 必须取**含有限样本置信上界及全部系统误差上界**的保守值，不能把带负偏差的点估计当上界；④ 误差缓解（如 ZNE）可能输出低于 $E_0$ 的非物理能量估计，绝不可把违背变分下界的缓解值直接塞进证书公式。
    - **结论与边界回验**：基态占据概率（平方重叠）下界为 $f_0 \ge 0.85$，本书约定的根保真度下界为 $F_0 \ge \sqrt{0.85} \approx 0.922$；成立前提包括基态非简并、$E_0$ 与 $\Delta$ 下界可靠，以及能量上界完整包含统计与系统误差且无未计入负偏差。
    - **易错坑提醒**：一是把 $0.85$ 与 $\sqrt{0.85}\approx 0.922$ 两个保真度口径混写；二是把误差条尚未加上的能量点估计直接代入，或者在基态近似简并（$\Delta \ll 0.03$）时忽略证书彻底失效的事实（当 $E-E_0 \ge \Delta$ 时下界退化为 $0$，什么都证明不了）。

## 第 17 章

> 对应章节：《17｜量子计算模型：门、测量、绝热、退火、拓扑与模拟》（共 10 题）

1. **【基础】七大计算模型（含拓扑量子计算 TQC）分别把“程序”写在哪里**

   - **题意与约定**：对照第 17 章全景地图（门、测量/融合、绝热、退火、**拓扑**、模拟量子模拟与数字—模拟混合七大计算模型），逐一厘清每种模型中“可编程指令”的物理载体；并对**拓扑量子计算**（TQC）补全 Ising 任意子与 Fibonacci 任意子的 $2\times 2$ 编织矩阵对比验算，直观展示“程序写在编织词里”究竟如何决定计算通用性。
   - **核心提示**：把七大计算模型逐一映射到“硬件静态底层资源”与“决定具体算法的可编程参数”（例如门序列、测量角度序列、末态哈密顿量、任意子编织世界线、光晶格/里德堡可调耦合等）。
   - **完整分步演算**：七大计算模型各自把程序写入截然不同的物理与数学对象中：
     - **1. 门线路模型**：写在离散单/双比特酉门序列、比特连接拓扑与末尾（或中途）测量安排中；
     - **2. 基于测量的计算（MBQC）与光子融合计算（FBQC）**：写在纠缠资源态（簇态或常数尺寸光子资源态）、各节点的单比特测量基或 Type-II 融合测量网络，以及依据先前测量结果动态改写后续测量角的经典前馈规则中；
     - **3. 闭系统绝热量子计算（AQC）**：写在从易制备初态哈密顿量 $H_0$ 到目标问题哈密顿量 $H_1$ 的连续插值路径 $H(s)$、调度函数 $s(t)$ 与总演化时长 $T$ 中；
     - **4. 量子退火（QA）**：写在横向场驱动项、QUBO/Ising 问题系数（注意 `dimod` 自旋 $s_i = -z_i$ 与物理符号差异）、退火时间日程、稀疏硬件次图嵌入与链强度，以及读出和链修复规则中；
     - **5. 拓扑量子计算（TQC）**：写在二维拓扑相中**非阿贝尔任意子的拓扑简并融合子空间**、绝热交换粒子世界线的**编织词序列**（生成元 $\sigma_1 = R,\; \sigma_2 = F R F^{-1}$）以及末态融合荷测量中。以三任意子融合到固定总荷的二维逻辑比特空间为例，零跳步对比两种核心任意子模型：
       - **Ising 任意子（对应 Majorana 零模，融合规则 $\sigma\times\sigma = 1 + \psi$）**：在基 $\{|1\rangle, |\psi\rangle\}$ 下，

         $$
         F_{\mathrm{Ising}} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix} = H,
         \qquad
         R_{\mathrm{Ising}} = \begin{pmatrix} e^{-i\pi/8} & 0 \\ 0 & e^{i 3\pi/8} \end{pmatrix} = e^{-i\pi/8} S.
         $$

         于是 $\sigma_1 = R_{\mathrm{Ising}} \propto S$、$\sigma_2 = H R_{\mathrm{Ising}} H \propto R_x(\pi/2)$，两者均为 Clifford 门，且 $\operatorname{Tr}(\sigma_1\sigma_2^{-1}) = 1$（旋转角为有理角 $2\pi/3$），仅生成 $24$ 阶有限单比特 Clifford 群；仅靠 Ising 编织**不通用**，必须外补非拓扑保护的魔法态注入与蒸馏！
       - **Fibonacci 任意子（融合规则 $\tau\times\tau = 1 + \tau$，量子维数 $d_\tau = \phi = \frac{1+\sqrt{5}}{2}$）**：在基 $\{|1\rangle, |\tau\rangle\}$ 下，

         $$
         F_{\mathrm{Fib}} = \begin{pmatrix} \phi^{-1} & \phi^{-1/2} \\ \phi^{-1/2} & -\phi^{-1} \end{pmatrix},
         \qquad
         R_{\mathrm{Fib}} = \begin{pmatrix} e^{-i 4\pi/5} & 0 \\ 0 & e^{i 3\pi/5} \end{pmatrix}.
         $$

         可逐项验证 $F_{\mathrm{Fib}}^2 = I$ 且 Yang–Baxter 恒等式 $\sigma_1\sigma_2\sigma_1 = \sigma_2\sigma_1\sigma_2$ 严格成立；算得 $\det(\sigma_1\sigma_2^{-1}) = 1$，而 $\operatorname{Tr}(\sigma_1\sigma_2^{-1}) = \phi^{-2} = \frac{3 - \sqrt{5}}{2} \approx 0.381966$。其最小多项式 $t^2 - 3t + 1 = 0$ 的另一伽罗瓦共轭根为 $\phi^2 = \frac{3 + \sqrt{5}}{2} \approx 2.618034 > 2$，违背有理角余弦倍值所有共轭必落于 $[-2, 2]$ 的必要条件，故旋转角与 $\pi$ 无理，配合不对易轴 $\sigma_1$ 在 $\mathrm{SU}(2)$ 中稠密，**仅靠拓扑编织即可通用**！
     - **6. 模拟量子模拟器（AQS）**：写在硬件原生实现的多体相互作用（如里德堡原子阵列范德瓦尔斯阻塞或超冷光晶格 Fermi–Hubbard 跳跃/排斥）、初态制备、连续控制波形与待测多体可观测量中；
     - **7. 数字—模拟混合计算（DAQC）**：写在离散可编程单比特数字门脉冲与硬件原生多体模拟纠缠块的交替调度序列中。
   - **结论与边界回验**：七大模型的程序载体依次对应门序列、资源态与自适应测量/融合规则、连续绝热路径、退火系数与嵌入日程、非阿贝尔任意子编织词与融合测量、原生多体相互作用波形，以及模拟块与数字单比特门的交替调度；其中 TQC 的通用性取决于编织群是否在 $\mathrm{SU}(2)$ 稠密（Fibonacci 通用而 Ising 仅限 Clifford）。
   - **易错坑提醒**：以为“理想条件下多项式等价”就代表不同模型的门成本、噪声结构和实验难度一样；尤其不要把“拓扑量子计算”一概误解为“天生零开销通用”——Ising/Majorana 路线依然离不开昂贵的非拓扑魔法态工厂。

2. **【计算】MBQC 最小簇态手算：证明测 $X$ 基后输出为 $X^m H|\psi\rangle$ 并求两结果概率**

   - **题意与约定**：给定任意归一化未知单比特输入态 $|\psi\rangle = a|0\rangle + b|1\rangle$（$|a|^2 + |b|^2 = 1$）与辅助态 $|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}$，在两比特大端序空间 $\mathbb{C}^2\otimes\mathbb{C}^2$ 上先施加受控相位门 $\mathrm{CZ} = |0\rangle\langle 0|\otimes I + |1\rangle\langle 1|\otimes Z$ 生成最小簇态 $|\Phi\rangle$，再对第一比特执行 $X$ 基测量 $\{|+\rangle\langle +|,\, |-\rangle\langle -|\}$，分别投影算清未归一化分支、测量概率与归一化输出态。
   - **核心提示**：把 $\mathrm{CZ}(|\psi\rangle|+\rangle)$ 展开后，将第一比特改写到 $X$ 基 $\{|+\rangle,|-\rangle\}$，直接读出测得 $m\in\{0,1\}$ 时第二比特的归一化后态与对应概率，并与 $X^m H|\psi\rangle$ 逐项对照。
   - **完整分步演算**：
     - **第一步：施加 $\mathrm{CZ}$ 纠缠门**。展开初态 $|\psi\rangle|+\rangle = a|0\rangle|+\rangle + b|1\rangle|+\rangle$，利用 $Z|+\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$，得纠缠态：

       $$
       |\Phi\rangle = \mathrm{CZ}\bigl(|\psi\rangle|+\rangle\bigr) = a|0\rangle|+\rangle + b|1\rangle|-\rangle.
       $$

     - **第二步：对第一比特做 $X$ 基投影（计算左共轭内积）**。先算辅助内积 $\langle +|0\rangle = \frac{1}{\sqrt{2}}$、$\langle +|1\rangle = \frac{1}{\sqrt{2}}$、$\langle -|0\rangle = \frac{1}{\sqrt{2}}$、$\langle -|1\rangle = -\frac{1}{\sqrt{2}}$。
       - 若测量结果为 $|+\rangle$（记经典读数 $m = 0$），第二比特未归一化条件态为：

         $$
         |\tilde{\phi}_0\rangle
         = (\langle +|\otimes I)|\Phi\rangle
         = a\langle +|0\rangle|+\rangle + b\langle +|1\rangle|-\rangle
         = \frac{1}{\sqrt{2}}\bigl(a|+\rangle + b|-\rangle\bigr).
         $$

         因为 $H|0\rangle = |+\rangle,\; H|1\rangle = |-\rangle$，由线性性有 $a|+\rangle + b|-\rangle = H(a|0\rangle + b|1\rangle) = H|\psi\rangle$，故 $|\tilde{\phi}_0\rangle = \frac{1}{\sqrt{2}} H|\psi\rangle$。
       - 若测量结果为 $|-\rangle$（记经典读数 $m = 1$），第二比特未归一化条件态为：

         $$
         |\tilde{\phi}_1\rangle
         = (\langle -|\otimes I)|\Phi\rangle
         = a\langle -|0\rangle|+\rangle + b\langle -|1\rangle|-\rangle
         = \frac{1}{\sqrt{2}}\bigl(a|+\rangle - b|-\rangle\bigr).
         $$

         利用 $X|+\rangle = +|+\rangle$ 与 $X|-\rangle = -|-\rangle$ 验算：$X(a|+\rangle + b|-\rangle) = a|+\rangle - b|-\rangle$，故 $|\tilde{\phi}_1\rangle = \frac{1}{\sqrt{2}} X H|\psi\rangle$。
     - **第三步：求两种测量结果的概率并回验归一化**。由于 $H$ 与 $X$ 均为酉算符保持范数不变（$\|H|\psi\rangle\| = \|XH|\psi\rangle\| = \||\psi\rangle\| = 1$），两支的测量概率为未归一化分支的平方范数：

       $$
       P(m = 0) = \|\tilde{\phi}_0\|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 \|H|\psi\rangle\|^2 = \frac{1}{2},
       \qquad
       P(m = 1) = \|\tilde{\phi}_1\|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 \|XH|\psi\rangle\|^2 = \frac{1}{2}.
       $$

       概率和 $\frac{1}{2} + \frac{1}{2} = 1$，且与未知振幅 $a, b$ 完全无关（测量丝毫不泄露 $|\psi\rangle$ 的信息！）。除以 $\sqrt{1/2}$ 归一化，两支统一写作 $X^m H|\psi\rangle$（$m \in \{0, 1\}$）。
   - **结论与边界回验**：第一比特测得 $|+\rangle$（$m=0$）与 $|-\rangle$（$m=1$）的概率均为 $\frac{1}{2}$，对应的归一化输出态统一为 $X^m H|\psi\rangle$。
   - **易错坑提醒**：一是混淆算符顺序，把 $X^m H|\psi\rangle$ 误写成 $H X^m|\psi\rangle$（因 $HX = ZH \ne XH$，后者对应 $Z^m H|\psi\rangle$ 是错的！）；二是误以为随机测量概率依赖于未知输入态 $(a,b)$——若概率依赖输入态，测量就会破坏相干性并泄露量子信息，无法实现酉门隐形传态。

3. **【进阶】为什么 MBQC 的随机测量结果不是未知错误？何时必须启用自适应前馈**

   - **题意与约定**：区分“已知位置的确定性副产物算符”与“未知类型/未知位置的物理噪声”，再用赤道测角旋转算符 $J(\alpha) = H R_z(-\alpha)$ 的共轭关系 $J(-\alpha)X = Z J(\alpha)$ 精确说明 Clifford 步骤与非 Clifford 旋转在前馈需求上的分水岭，同时联系 gflow 与 FBQC 擦除机制。
   - **核心提示**：区分“测量结果已知、可确定性追踪的 Pauli 副产物”与“位置/类型未知的噪声”；再利用 $X$ 副产物穿过非 Clifford 赤道测角门 $J(\alpha)=H R_z(-\alpha)$ 时如何把旋转角反号，判断何时必须前馈改测角。
   - **完整分步演算**：
     - **为何不是未知错误**：上题中虽然 $m \in \{0,1\}$ 以各 $50\%$ 概率随机出现，但测量结果 $m$ 被经典探测器**精确记录**了下来，因此多出的 Pauli 算符 $X^m$（一般多步中为 $X^{s_X} Z^{s_Z}$）类型、作用比特与时机全部已知，称为**已知 Pauli 副产物算符**（byproduct operator）。这与环境造成、发生位置和类型未知的退相干错误有本质区别。
     - **何时可延迟、何时必须实时自适应前馈**：
       - **纯 Clifford 测量（测角 $\alpha \in \{0, \pm\pi/2, \pi\}$）**：因 Clifford 门把 Pauli 算符共轭映射为另一个 Pauli 算符，所有已知 Pauli 副产物都可以顺着线路推到最后，用纯经典软件 **Pauli 帧**（Pauli frame）追踪并在末态解释读数即可，无需中途改测角；
       - **一般非 Clifford 旋转（如 $\alpha = \pi/4$ 等任意赤道测角）**：记单步演化算符为 $J(\alpha) = H R_z(-\alpha)$。把前一步传来的副产物 $X^{m_0}$ 推过下一步 $J(\beta)$ 时，利用 $X R_z(-\beta) X = R_z(+\beta)$ 与 $H X = Z H$ 得精确恒等式：

         $$
         J(\beta)\, X = H R_z(-\beta)\, X = H X R_z(+\beta) = Z H R_z(+\beta) = Z\, J(-\beta).
         $$

         为了让物理上等价于执行目标 $J(+\beta)$（而不是错反向的 $J(-\beta)$！），当上一步测得 $m_0 = 1$ 时，控制器**必须实时翻转下一步的物理测量角**，取 $\beta_{\mathrm{phys}} = (-1)^{m_0}\beta$！此时才满足 $J((-1)^{m_0}\beta) X^{m_0} = Z^{m_0} J(\beta)$，把副产物继续安全维持在 Pauli 帧里。要保证任意测量结果分支都能确定性地找到一致的校正顺序，资源图必须具备因果流（causal flow）、广义流（gflow，注意 $XY$ 与 $XZ/YZ$ 平面条件不同）或 Pauli flow 结构。
   - **结论与边界回验**：随机结果 $m$ 已知且精确决定 Pauli 副产物算符，并非未知噪声；纯 Clifford 步可仅靠经典 Pauli 帧延后处理，而一旦引入非 Clifford 旋转角实现通用计算，就必须依据先前测量结果实时自适应调整后续测量基（自适应前馈），并要求图态具备确定性流结构。
   - **易错坑提醒**：以为“前馈只是为了纠错”或“可以在所有测量全部做完后再用经典电脑补救非 Clifford 测角符号”——一旦选错了非 Clifford 测量基的角度符号，错误已经变成非 Pauli 旋转，事后经典后处理无法挽回。

4. **【计算】绝热二能级避免交叉手算：求 $H(s) = -(1-s)X - sZ$ 的本征值、最小谱隙与端点基态**

   - **题意与约定**：给定无量纲闭系统绝热插值哈密顿量 $H(s) = -(1-s)X - sZ$（$s \in [0, 1]$，采用算法约定 $\hbar = 1$）。写出 $2\times 2$ 矩阵，列出完整特征方程 $\lambda^2 - (\operatorname{Tr} H)\lambda + \det H = 0$ 零跳步求本征值与谱隙 $\Delta(s) = E_+(s) - E_-(s)$，通过配方求严格最小谱隙 $\Delta_{\min}$，再分别解 $s=0$ 与 $s=1$ 的基态特征向量。
   - **核心提示**：写出 $H(s)=-(1-s)X-sZ$ 的 $2\times 2$ 矩阵，利用无迹 Pauli 组合的本征值公式 $\pm\sqrt{(1-s)^2+s^2}$ 求谱隙 $\Delta(s)$ 关于 $s$ 的最小值，再把 $s=0$ 与 $s=1$ 代入求两端基态。
   - **完整分步演算**：
     - **第一步：写出矩阵与特征方程**。代入 $X = \begin{pmatrix}0&1\\ 1&0\end{pmatrix}$ 与 $Z = \begin{pmatrix}1&0\\ 0&-1\end{pmatrix}$：

       $$
       H(s) = \begin{pmatrix} -s & -(1-s) \\ -(1-s) & s \end{pmatrix}.
       $$

       算迹与行列式：$\operatorname{Tr} H(s) = -s + s = 0$，$\det H(s) = (-s)(s) - [-(1-s)]^2 = -\bigl[s^2 + (1-s)^2\bigr]$。列出特征方程 $\det(H(s) - \lambda I) = 0$：

       $$
       \lambda^2 - \bigl(\operatorname{Tr} H(s)\bigr)\lambda + \det H(s) = 0
       \implies
       \lambda^2 - \bigl[s^2 + (1-s)^2\bigr] = 0.
       $$

       直接开方得两个瞬时本征值与瞬时谱隙：

       $$
       E_\pm(s) = \pm\sqrt{s^2 + (1-s)^2},
       \qquad
       \Delta(s) = E_+(s) - E_-(s) = 2\sqrt{s^2 + (1-s)^2}.
       $$

     - **第二步：配方求最小谱隙**。把根号内二次函数按 $s$ 配方：

       $$
       s^2 + (1-s)^2 = 2s^2 - 2s + 1 = 2\!\left(s - \frac{1}{2}\right)^2 + \frac{1}{2}.
       $$

       该式在 $s = \frac{1}{2}$ 处取得严格最小值 $\frac{1}{2}$，故最小谱隙为

       $$
       \Delta_{\min} = \Delta\!\left(\frac{1}{2}\right) = 2\sqrt{\frac{1}{2}} = \sqrt{2} \approx 1.4142 > 0.
       $$

       （衔接正文 4.2 节：经正交基旋转后，线性调度 $s=t/T$ 对应 Landau–Zener 参数 $\Delta = \sqrt{2}$、$v = 2\sqrt{2}/T$，无限扫频隧穿估计 $P_{\mathrm{LZ}} = \exp\!\bigl(-\frac{\pi\Delta^2}{2v}\bigr) = \exp\!\bigl(-\frac{\pi T}{2\sqrt{2}}\bigr)$，与最小谱隙直接挂钩。）
     - **第三步：求两端点基态（对应较小本征值 $E_- = -1$）**。
       - **$s = 0$**：$H(0) = -X = \begin{pmatrix}0&-1\\ -1&0\end{pmatrix}$，基态能量 $E_-(0) = -1$。解 $(-X - (-1)I)\mathbf{v} = \begin{pmatrix}1&-1\\ -1&1\end{pmatrix}\begin{pmatrix}v_0\\ v_1\end{pmatrix} = 0$ 得 $v_0 = v_1$，归一化基态为 $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$（回验：$-X|+\rangle = -|+\rangle$）；
       - **$s = 1$**：$H(1) = -Z = \begin{pmatrix}-1&0\\ 0&1\end{pmatrix}$，基态能量 $E_-(1) = -1$。直接读出对应 $-1$ 的归一化基态为 $|0\rangle = \begin{pmatrix}1\\ 0\end{pmatrix}$（回验：$-Z|0\rangle = -|0\rangle$）。
   - **结论与边界回验**：本征值为 $E_\pm(s) = \pm\sqrt{s^2 + (1-s)^2}$；谱隙 $\Delta(s) = 2\sqrt{s^2+(1-s)^2}$ 在 $s = 1/2$ 处取最小值 $\Delta_{\min} = \sqrt{2}$；端点基态在 $s = 0$ 为 $|+\rangle$、在 $s = 1$ 为 $|0\rangle$。
   - **易错坑提醒**：一是算谱隙时忘记乘 $2$（把单个能级绝对值 $\sqrt{1/2} = 1/\sqrt{2}$ 误报成谱隙 $\Delta_{\min}$）；二是看错 $H(1) = -Z$ 前的负号，误把 $s=1$ 的基态写成 $|1\rangle$（$+Z$ 的基态才是 $|1\rangle$，$-Z$ 的基态是 $|0\rangle$）。

5. **【基础】为何“绝热计算与门模型多项式等价”不能直接证明商用退火器具有优化量子优势**

   - **题意与约定**：沿着理论前提 $\to$ 物理硬件落差 $\to$ 计算复杂性边界 $\to$ 端到端实测基准四道关口，彻底拆穿“AQC $\equiv$ BQP $\implies$ 退火机优于经典优化”的逻辑跳步，并精准交代随机（stoquastic）哈密顿量的最新复杂性理论定位。
   - **核心提示**：沿四道关口逐一排查：理论等价要求非随机（non-stoquastic）任意局域哈密顿量与零温闭系统极慢演化，而商用退火器受限于随机型 Ising 耦合、有限温热噪声与启发式短退火时间。
   - **完整分步演算**：
     - **第一关（理论等价的苛刻前提）**：Aharonov 等人（2007）证明的 $\mathrm{AQC} = \mathrm{BQP}$ 多项式等价定理，要求**无噪闭系统零温绝热演化**、精确受控的插值路径，且关键地依赖允许正实数乃至复数非对角元的**非随机（non-stoquastic）** 2-局域哈密顿量；同时“多项式等价”允许巨大的多项式资源开销，丝毫不承诺在具体有限规模实例上更快。
     - **第二关（商用退火机的随机哈密顿量与开放环境现实）**：商用横向场 Ising 量子退火机（如 D-Wave）实现的通常是**随机（stoquastic）哈密顿量**（即存在某局域基底——此处为计算基——使所有非对角矩阵元实且 $\le 0$）。在复杂性理论上需保持精确表述：一方面，随机性依赖基底选择，无符号问题也不自动保证经典路径积分蒙特卡洛（PIMC）在所有拓扑能垒下都能多项式快速混合，且 Hastings（2021）已证明无符号问题绝热计算相对经典算法仍存在超多项式神谕分离；但另一方面，这仍**不**给予商用随机退火机对一般 $\mathrm{BQP}$ 线路的通用等价保证，更未证明其对商业组合优化具有普遍优势。
     - **第三关（谱隙关闭与物理工程瓶颈）**：实际硬件工作在有限温度、开放热库、有限耦合精度和稀疏图拓扑下，必须付出高昂的次图嵌入、链强度折中与链断裂代价；对于具体 NP-hard 组合优化实例，绝热路径上的最小谱隙 $\Delta_{\min}$ 常随规模指数关闭，导致绝热或退火时间指数暴涨。
     - **第四关（优势认证的唯一口径）**：要声称实际优化优势，必须在相同的目标解质量、成功阈值与端到端全账时间（TTS，含嵌入、编程、退火、读出与修复）下，正面超越当代强经典求解器（如并行回火、模拟退火、分支定界或二维/三维置信传播张量网络 BP-TN）。
   - **结论与边界回验**：模型等价定理仅刻画理想无噪非随机闭系统的渐近计算能力上限，而商用退火机属于受热噪声、稀疏嵌入与有限控制精度约束的开放随机系统，既无一般 BQP 等价保障，也不保证具体实例的最小谱隙与端到端 TTS 胜过强经典算法。
   - **易错坑提醒**：一是把“两种计算模型多项式等价”误读成“真实物理设备具有速度优势”；二是走向另一个极端，误以为“随机（stoquastic）哈密顿量 = 任何情形下都完全可被经典 PIMC 轻松模拟”（忽略了拓扑能垒慢混合与 Hastings 2021 的神谕分离）。

6. **【计算】量子退火求解时间（TTS）手算：$p_s = 0.2,\; t_a = 20\ \mu\mathrm{s}$ 与 $99\%$ 目标成功率**

   - **题意与约定**：已知单次独立退火尝试命中目标解的概率为 $p_s = 0.2$，单次退火脉冲时长 $t_a = 20\ \mu\mathrm{s}$。要求以至少 $99\%$ 的总体概率命中目标至少一次（即全部 $R$ 次独立尝试均失败的概率不超过 $\delta = 1 - 0.99 = 0.01$），先解出最小整数重复次数 $R$ 并做逐次代入回验，再求纯退火段 TTS，并对照正文端到端全账口径。
   - **核心提示**：先由至少成功一次的概率公式 $1-(1-p_s)^R\ge 0.99$ 取对数反解所需重复次数 $R=\lceil\ln(0.01)/\ln(1-p_s)\rceil$（注意向上取整），再乘以单次退火时长 $t_a$ 算纯退火段 TTS，并注明忽略的编程/读出开销。
   - **完整分步演算**：
     - **第一步：建立全失败概率不等式**。单次失败概率为 $1 - p_s = 1 - 0.2 = 0.8$。连续 $R$ 次独立退火全部失败的概率为 $(1 - p_s)^R = 0.8^R$，要求：

       $$
       0.8^R \le 0.01.
       $$

     - **第二步：取自然对数解出最小整数 $R$**。对两边取自然对数 $\ln$（注意 $\ln 0.8 \approx -0.22314355 < 0$，同除负数时**不等号必须反向**！）：

       $$
       R\ln 0.8 \le \ln 0.01
       \implies
       R \ge \frac{\ln 0.01}{\ln 0.8}
       \approx \frac{-4.60517019}{-0.22314355}
       \approx 20.637702.
       $$

       因重复次数必须为正整数，向上取整得：

       $$
       R = \left\lceil \frac{\ln 0.01}{\ln 0.8} \right\rceil = 21.
       $$

     - **第三步：临界整数逐一独立回验**。
       - $R = 20$ 时：至少成功一次的概率为 $1 - 0.8^{20} \approx 1 - 0.011529 = 0.988471 < 0.99$（未达标）；
       - $R = 21$ 时：至少成功一次的概率为 $1 - 0.8^{21} \approx 1 - 0.009223 = 0.990777 \ge 0.99$（刚好达标！）。
     - **第四步：计算纯退火段 TTS 与端到端全账提醒**。仅计每次 $t_a = 20\ \mu\mathrm{s}$ 的纯退火段：

       $$
       \mathrm{TTS}_{\mathrm{anneal}} = R \cdot t_a = 21 \times 20\ \mu\mathrm{s} = 420\ \mu\mathrm{s} = 0.42\ \mathrm{ms}.
       $$

       对照正文 5.1 节算例 C（$R=228$ 次、编程 $1\ \mathrm{s}$、每次退火 $20\ \mu\mathrm{s}$ 加读出与延迟 $120\ \mu\mathrm{s}$），纯退火段仅 $4.56\ \mathrm{ms}$ 而端到端全账高达 $1.0319\ \mathrm{s}$（相差 $226$ 倍以上）；因此与经典求解器横向对比时，必须补全次图嵌入、芯片编程、热化冷却、读出延迟、链修复与调参等全部墙钟开销。
   - **结论与边界回验**：至少需要重复 $R = 21$ 次；仅计纯退火段的求解时间为 $\mathrm{TTS}_{\mathrm{anneal}} = 420\ \mu\mathrm{s}$（端到端比较还须计入编程、嵌入、读出、复位、链修复与调参耗时）。
   - **易错坑提醒**：一是忘记 $\ln 0.8 < 0$ 造成不等号方向错误，或四舍五入/向下取整误算成 $R = 20$；二是直接拿 $420\ \mu\mathrm{s}$ 纯退火脉冲时间去和包含读盘、预处理和收敛校验的经典求解器墙钟时间做不公平对比。

7. **【计算】数字—模拟混合（DAQC）自旋回波（echo）序列推导：保留 $Z_2 Z_3$、抵消 $Z_1 Z_2$**

   - **题意与约定**：三比特系统的原生多体漂移哈密顿量为 $H_0 = J(Z_1 Z_2 + Z_2 Z_3)$（$J$ 为耦合角频率，$\hbar = 1$）。总演化时长 $t$ 均分为两段各 $t/2$，在中点与末尾各对第 $1$ 比特施加一发理想瞬时 $X_1$ 脉冲，总酉算符（从右向左作用）为 $U = X_1 e^{-i H_0 t/2} X_1 e^{-i H_0 t/2}$。利用矩阵指数级数共轭公式 $X_1 e^A X_1 = e^{X_1 A X_1}$ 及 Pauli 反对易关系逐步化简，并核查全部物理前提。
   - **核心提示**：把两段演化写成 $U=X_1 e^{-i H_0 t/2} X_1 e^{-i H_0 t/2}$，利用共轭规则 $X_1(Z_1 Z_2)X_1=-Z_1 Z_2$ 而 $X_1(Z_2 Z_3)X_1=+Z_2 Z_3$，因所有 $Z$ 项两两对易可直接合并指数相消。
   - **完整分步演算**：
     - **第一步：证明矩阵指数共轭关系**。因为 $X_1 = X_1^\dagger$ 且 $X_1^2 = I$，对任意方阵 $A$ 与正整数 $k$ 均有 $X_1 A^k X_1 = (X_1 A X_1)^k$。按矩阵指数泰勒级数逐项共轭：

       $$
       X_1 e^A X_1
       = X_1 \left(\sum_{k=0}^{\infty} \frac{A^k}{k!}\right) X_1
       = \sum_{k=0}^{\infty} \frac{(X_1 A X_1)^k}{k!}
       = e^{X_1 A X_1}.
       $$

     - **第二步：计算 $X_1 H_0 X_1$**。利用单比特反对易关系 $X_1 Z_1 X_1 = -Z_1$，且 $X_1$ 与作用在比特 $2, 3$ 上的 $Z_2, Z_3$ 对易：

       $$
       X_1 H_0 X_1
       = J\bigl[(X_1 Z_1 X_1) Z_2 + X_1^2 Z_2 Z_3\bigr]
       = J\bigl(-Z_1 Z_2 + Z_2 Z_3\bigr).
       $$

     - **第三步：合并两段演化并验证对易条件**。将第一步与第二步代回 $U$：

       $$
       U = \bigl(X_1 e^{-i H_0 t/2} X_1\bigr)\, e^{-i H_0 t/2}
         = e^{-i J(-Z_1 Z_2 + Z_2 Z_3) t/2}\, e^{-i J(Z_1 Z_2 + Z_2 Z_3) t/2}.
       $$

       检查两项生成元是否对易：因为 $Z_1 Z_2$ 与 $Z_2 Z_3$ 全由 $Z$ 算符组成（在计算基下同时对角），严格满足 $[Z_1 Z_2,\; Z_2 Z_3] = 0$，故可直接相加指数（无 Baker–Campbell–Hausdorff 高阶对易子余项！）：

       $$
       \begin{aligned}
       U &= \exp\!\left[-i J\bigl(-Z_1 Z_2 + Z_2 Z_3 + Z_1 Z_2 + Z_2 Z_3\bigr)\frac{t}{2}\right] \\
         &= \exp\!\left[-i J(2 Z_2 Z_3)\frac{t}{2}\right]
          = e^{-i J t\, Z_2 Z_3}.
       \end{aligned}
       $$

       前一半与后一半中的 $Z_1 Z_2$ 相位正好相反（$-\frac{Jt}{2} + \frac{Jt}{2} = 0$）精确抵消，而 $Z_2 Z_3$ 同号相加（$\frac{Jt}{2} + \frac{Jt}{2} = Jt$）完整保留。
     - **第四步：物理成立边界**。该精确抵消依赖三个强理想假设：① $X_1$ 脉冲瞬时完成且无幅度/轴向误差；② 两段自由演化时长严格相等（若失配为 $t_1 \ne t_2$，按 $e^{-i(\cdots)}$ 约定会残留相位因子 $e^{-i(t_1 - t_2)J Z_1 Z_2}$，即残余生成元 $(t_1 - t_2)J Z_1 Z_2$，正文指出该残余相移在计算基下隐身却会在 $X$ 基测量中暴露）；③ 硬件哈密顿量不含与 $Z_1 Z_2$ 不对易的横向串扰项。
   - **结论与边界回验**：$U = X_1 e^{-i H_0 t/2} X_1 e^{-i H_0 t/2} = e^{-i J t Z_2 Z_3}$，两半段中 $Z_1 Z_2$ 反号相消、$Z_2 Z_3$ 同号累加。
   - **易错坑提醒**：一是忘记在指数合并前显式验证 $[Z_1 Z_2, Z_2 Z_3] = 0$（若存在横向场 $h_x X_2$ 等非对易项，不能直接把两个指数相加，会产生 Trotter 误差）；二是漏掉末尾第二发 $X_1$ 脉冲（只打中点一发脉冲会多留一个未抵消的局域翻转 $X_1$）。

8. **【基础】模拟量子模拟器（AQS）从经典可算区外推时，至少应给出哪四类互补证据**

   - **题意与约定**：模拟量子模拟器面向专用多体物理问题（如里德堡原子阵列的 $\mathbb{Z}_2/\mathbb{Z}_3$ 相变或超冷费米光晶格的二维 Fermi–Hubbard 模型），缺乏门模型的通用容错纠错，一旦进入经典精确对角化算不动的大规模参数区，单靠“机器吐出一条好看的曲线”无法建立科学可信度。按正文验证框架系统给出四类彼此互补的证据链并界定边界。
   - **核心提示**：围绕“小规模/可解区与精确经典方法逐点校准”“硬件哈密顿量独立标定与噪声预算”“守恒量/对称性/交叉模型自洽检验”和“前沿近似经典方法（MPS/QMC/Pauli 传播）对照”四类证据组织作答。
   - **完整分步演算**：要让超出经典精确模拟区的实验结论站得住脚，必须构筑四根缺一不可的互补支柱：
     - **1. 解析结构与守恒律检验**：核查系统在已知极限与对称性下是否严格遵守理论约束——例如 Fermi–Hubbard 模拟中的总粒子数与自旋守恒、里德堡阻塞极限 $R_b/a$ 下的禁戒双激发约束、以及零耦合/弱耦合/可积点上的精确解析极限；
     - **2. 经典可算区定量对照**：在较小系统尺寸、较短演化时间、低纠缠或强/弱耦合可算区内，把硬件实测曲线与精确对角化（ED）、矩阵乘积态（MPS）、量子蒙特卡洛（QMC）或置信传播张量网络（BP-TN）做带误差棒的逐点定量比对，标定真实哈密顿量参数与噪声地板；
     - **3. 独立交叉验证**：在重叠参数区，用另一套物理平台（例如里德堡阵列对比超导/离子阱模拟）、另一种独立数值近似方法，或另一组互补测量方案（如从局域磁化扩展到高阶关联函数或随机测量阴影）独立复现核心特征；
     - **4. 规模、步长与校准稳定性检验**：系统改变格点尺寸、演化步长、初态温度/熵、校准工作点与读出后处理，验证目标物理结论（如相变临界点或标度指数）及其误差条呈现平滑可解释的趋势，而非由单点校准漂移或有限尺寸伪影制造。

     **严格范围限定**：上述四类证据只能为**受检的特定可观测量族、给定参数区间与声明的误差尺度**背书——局域密度或两点关联通过检验，绝不等于整个多体量子态的全局保真度已经通过验证。
   - **结论与边界回验**：至少需同时提供：① 解析结构与守恒律/极限核验；② 经典可算区的定量对照；③ 跨平台/跨算法/跨测量方案的独立交叉验证；④ 尺寸、步长与校准变化下的稳定性检验，并明确限定覆盖的可观测量与误差边界。
   - **易错坑提醒**：拿小尺寸（例如 $10$ 格点）与精确对角化吻合，就直接断言 $200$ 格点时的复杂非平衡多体关联一定同样准确，忽略了随规模增长的陷阱非均匀性、热熵累积、退相干与串扰漂移。

9. **【计算】8 位唯一目标搜索：为何渐近式给 $12.6$、最佳整数是 $12$，且 $12$ 次查询不等于 $12$ 次普通加密**

   - **题意与约定**：搜索空间规模 $N = 2^8 = 256$、唯一标记目标 $M = 1$。先用精确 Grover 旋转角 $\theta = \arcsin(\sqrt{M/N}) = \arcsin(1/16)$ 算出首峰连续最优点 $r_* = \frac{\pi}{4\theta} - \frac{1}{2}$ 并逐一验算 $r = 11, 12, 13$ 的精确成功概率 $p_r = \sin^2[(2r+1)\theta]$，再站在计算模型计费口径拆解“一次抽象预言机查询”与“一次经典加密”之间巨大的物理鸿沟。
   - **核心提示**：先用精确角 $\theta=\arcsin(1/16)$ 对比渐近估计 $\frac{\pi}{4}\sqrt{N}$ 与精确最佳整数 $k$ 对应的成功率 $\sin^2((2k+1)\theta)$；第二问把一次可逆加密预言机内部所需的数千逻辑门与普通经典加密区分开。
   - **完整分步演算**：
     - **第一步：对比渐近近似与精确角度公式**。常见渐近估算给出

       $$
       r_{\mathrm{asymp}} = \frac{\pi}{4}\sqrt{N} = \frac{\pi}{4}\sqrt{256} = 4\pi \approx 12.5664 \approx 12.6.
       $$

       它省去了初始态已自带的 $1$ 个 $\theta$（即公式中的 $-\frac{1}{2}$ 项）以及小角近似 $\sin\theta \approx \theta$。使用精确公式 $\theta = \arcsin\!\left(\frac{1}{\sqrt{256}}\right) = \arcsin\!\left(\frac{1}{16}\right) \approx 0.06254076\ \mathrm{rad}$，经过 $r$ 次 Grover 迭代后成功概率精确为

       $$
       p_r = \sin^2\!\bigl[(2r + 1)\theta\bigr].
       $$

       令角度恰好到达首个峰值 $\frac{\pi}{2}$：$(2r_* + 1)\theta = \frac{\pi}{2}$，解出精确连续最优点：

       $$
       r_* = \frac{\pi}{4\theta} - \frac{1}{2}
       \approx \frac{3.14159265}{4 \times 0.06254076} - 0.5
       \approx 12.558180 - 0.5
       = 12.058180.
       $$

     - **第二步：逐个整数回验首峰附近成功率**。
       - $r = 11$：$(23)\theta \approx 1.438437\ \mathrm{rad}$，$\sin^2(1.438437) \approx 0.982583$；
       - **$r = 12$**：$(25)\theta \approx 1.563519\ \mathrm{rad}$（距 $\pi/2 \approx 1.570796$ 仅差 $0.007277\ \mathrm{rad}$！），$p_{12} = \sin^2(1.563519) \approx \mathbf{0.999947}$；
       - $r = 13$：$(27)\theta \approx 1.688601\ \mathrm{rad}$（已越过 $\pi/2$ 发生过度旋转），$p_{13} = \sin^2(1.688601) \approx 0.986186 < p_{12}$。

       因此首个成功峰附近最佳整数是 **$r = 12$**（而非把 $12.6$ 向上取整得到的 $13$！）。同时保持数学严谨：$r = 12$ 是首峰最佳整数，而非全体非负整数上的绝对最大——例如迭代到更后面 $r = 213$ 时 $p_{213} \approx 0.999998$，但查询开销暴增近 $18$ 倍，工程上毫无必要。
     - **第三步：为何 $12$ 次查询远不等于 $12$ 次普通加密**。在门线路模型下，抽象的“$1$ 次预言机查询”必须展开成庞大的物理开销：将整套分组密码（如 AES S 盒与轮函数）编译成可逆量子算术线路、消耗大量辅助比特存放中间状态、与目标密文比对并执行相位回踢标记、再完整**反计算**清除全部中间垃圾位（避免纠缠破坏干涉）；每轮还要加上全寄存器扩散反射门。落到容错芯片上，每个非 Clifford 门（$T$/Toffoli）都要消耗魔法态工厂与表面码时空体积，串行深度与墙钟时间比一次经典 CPU 指令慢出许多个数量级。
   - **结论与边界回验**：渐近式 $\frac{\pi}{4}\sqrt{256}\approx 12.57$ 略去了 $-\frac{1}{2}$ 偏移项，精确连续最优点 $r_* \approx 12.058$ 决定首峰最佳整数为 $r = 12$（$p_{12} \approx 0.999947 > p_{13} \approx 0.986186$）；而每次量子查询需完整实现可逆加密、比对、相位标记、反计算、扩散与容错纠错，绝不能按普通经典加密次数直比墙钟成本。
   - **易错坑提醒**：一是习惯性地对 $\frac{\pi}{4}\sqrt{N}$ 向上取整，反而因过旋转拉低成功率还多花一次查询；二是把查询复杂度抽象步数当成物理时钟周期，严重高估 Grover 对对称密码的现实破译速度。

10. **【基础】为什么“数字—模拟方案比纯数字线路更浅”还不等于更快或更准？至少应补问哪些成本与误差**

    - **题意与约定**：电路“浅”（模拟纠缠块数或层数更少）只是一条抽象计数指标。要从“更浅”跨越到“实际运行更快、结果更准”，必须先钉死对比基线（对比哪套纯数字分解、编译器、目标误差与连接图），再沿四个维度逐项追问端到端真实代价。
    - **核心提示**：对比“抽象块数/层数更少”与“真实端到端速度与精度”，从单模拟块校准/串扰误差、物理绝对时长与编译转换开销、经典基线对齐三类容易被“更浅”掩盖的账目逐一追问。
    - **完整分步演算**：评估任何数字—模拟混合（DAQC）方案时，至少须补问以下四类核心成本与误差问题：
      - **1. 物理时间成本（块数少 $\ne$ 墙钟时间短）**：单次原生多体模拟纠缠块的实际脉冲持续时长有多长？各块之间能否真正并行？穿插其中的单比特数字重聚焦脉冲、波形切换缓冲与控制器同步等待是否全部计入总时长？一个持续微秒级的复杂模拟块可能比数层纳秒级数字门更慢；
      - **2. 物理误差与模型失配成本**：模拟纠缠块并非理想抽象哈密顿量——芯片原生耦合常伴随长程残余相互作用、有限脉宽畸变、串扰、漂移和校准不准（如第 7 题回波中两半段时长微小失配即留下 $X$ 基可见的残余耦合相位），其累积模型偏差往往缺乏离散门模型那样的标准表征与容错纠错手段；
      - **3. 验证方式与算法通用性**：如何独立验证大尺寸模拟块输出的准确度（缺乏标准 RB/GST 或全态验证）？这套固定多体相互作用加单比特门在物理噪声下是否真能高效覆盖目标任务，还是仅对个别定制模型有效？
      - **4. 同一口径下的端到端资源账单**：DAQC 与纯数字对照双方是否锁定了**完全相同的目标精度 $\varepsilon$、成功概率门槛、初态制备、读出缓解、重复采样次数与重试预算**？若纯数字基线用的是未经优化的朴素 Trotter 分解，所谓“更浅”只是稻草人对比。
    - **结论与边界回验**：块数变浅只是中间抽象指标；只有锁定强数字基线，并逐项核验①物理总时间、②模型偏差/有限脉宽/串扰等误差成本、③可验证性与通用性边界、④相同精度与采样预算下的端到端总账，确认时间与任务误差双双改善，才能得出“更快”或“更准”的结论。
    - **易错坑提醒**：把“模拟块数从 $20$ 层降到 $3$ 块”直接等价于“电路运行快了近 $7$ 倍、噪声小了近 $7$ 倍”，忽略了单个模拟块更长的演化时间、更难抑制的系统耦合偏差以及无法直接接入容错纠错架构的局限。

## 第 18 章

> 对应章节：《18｜量子信道、通信容量、复杂度与连续变量》（共 14 题）

1. **【计算】构造 $\rho = 0.8|0\rangle\langle 0| + 0.2|1\rangle\langle 1|$ 的两比特纯化并逐项偏迹验证**

   - **题意与约定**：给定单量子比特系统 $A$ 的混态 $\rho = 0.8|0\rangle\langle 0| + 0.2|1\rangle\langle 1|$，引入辅助参考系统 $R$（同样为二维空间 $\mathbb{C}^2$），依据谱分解构造纯化 $|\psi\rangle_{AR} = \sum_i \sqrt{\lambda_i}|e_i\rangle_A |r_i\rangle_R$，再把完整纯态密度矩阵 $|\psi\rangle\langle\psi|$ 全部四项逐一写出并对 $R$ 做偏迹验证还原。
   - **核心提示**：对对角态 $\rho=\sum_i\lambda_i|i\rangle\langle i|$，直接以 $\sqrt{\lambda_i}$ 为系数构造两比特纯化 $|\Psi\rangle_{AR}=\sum_i\sqrt{\lambda_i}|i\rangle_A|i\rangle_R$，再写出 $|\Psi\rangle\langle\Psi|$ 对 $R$ 求偏迹验证还原 $\rho$。
   - **完整分步演算**：$\rho$ 的本征值为 $\lambda_0 = 0.8,\; \lambda_1 = 0.2$，对应正交本征基为 $|0\rangle, |1\rangle$。取参考系统正交基 $\{|0\rangle_R, |1\rangle_R\}$，构造规范纯化态：

     $$
     |\psi\rangle_{AR} = \sqrt{0.8}\,|0\rangle_A|0\rangle_R + \sqrt{0.2}\,|1\rangle_A|1\rangle_R
     = \sqrt{0.8}\,|00\rangle + \sqrt{0.2}\,|11\rangle.
     $$

     先验证纯化态归一化：$(\sqrt{0.8})^2 + (\sqrt{0.2})^2 = 0.8 + 0.2 = 1$。展开两体纯态外积 $|\psi\rangle\langle\psi|$（注意 $\sqrt{0.8}\sqrt{0.2} = \sqrt{0.16} = 0.4$）：

     $$
     \begin{aligned}
     |\psi\rangle\langle\psi|_{AR}
     &= \bigl(\sqrt{0.8}\,|00\rangle + \sqrt{0.2}\,|11\rangle\bigr)
        \bigl(\sqrt{0.8}\,\langle 00| + \sqrt{0.2}\,\langle 11|\bigr) \\
     &= 0.8\,|00\rangle\langle 00| + 0.4\,|00\rangle\langle 11| + 0.4\,|11\rangle\langle 00| + 0.2\,|11\rangle\langle 11|.
     \end{aligned}
     $$

     使用偏迹基本线性规则 $\operatorname{Tr}_R\bigl(|a\rangle_A|i\rangle_R\langle b|_A\langle j|_R\bigr) = |a\rangle\langle b|_A \cdot \langle j|i\rangle_R$ 逐项计算：
     - 第 1 项：$0.8\,|0\rangle\langle 0|\cdot\langle 0|0\rangle = 0.8\,|0\rangle\langle 0|$；
     - 第 2 项：$0.4\,|0\rangle\langle 1|\cdot\langle 1|0\rangle = 0.4\,|0\rangle\langle 1|\cdot 0 = 0$；
     - 第 3 项：$0.4\,|1\rangle\langle 0|\cdot\langle 0|1\rangle = 0.4\,|1\rangle\langle 0|\cdot 0 = 0$；
     - 第 4 项：$0.2\,|1\rangle\langle 1|\cdot\langle 1|1\rangle = 0.2\,|1\rangle\langle 1|$。

     四项相加，交叉相干项全部归零，精确还原原混态：

     $$
     \operatorname{Tr}_R\bigl(|\psi\rangle\langle\psi|_{AR}\bigr) = 0.8\,|0\rangle\langle 0| + 0.2\,|1\rangle\langle 1| = \rho.
     $$

     由纯化唯一性定理，对参考系统 $R$ 单独施加任意酉算符 $U_R$ 得到 $(I_A \otimes U_R)|\psi\rangle_{AR}$，仍是同一个 $\rho$ 的合法纯化（例如 $\sqrt{0.8}|0+\rangle + \sqrt{0.2}|1-\rangle$）。
   - **结论与边界回验**：可取纯化 $|\psi\rangle_{AR} = \sqrt{0.8}\,|00\rangle + \sqrt{0.2}\,|11\rangle$，对其密度矩阵逐项求参考系统偏迹 $\operatorname{Tr}_R$ 精确还原 $\rho = 0.8|0\rangle\langle 0| + 0.2|1\rangle\langle 1|$。
   - **易错坑提醒**：一是把纯化系数写成概率 $0.8, 0.2$ 而忘记开平方根（那样范数平方仅为 $0.68 \ne 1$）；二是误以为一个混态只有唯一一个纯化，忽略了参考系统上任意酉变换 $I_A\otimes U_R$ 给出的无穷多等价纯化。

2. **【计算】求单比特复位信道 $\mathcal{R}(X) = \operatorname{Tr}(X)|0\rangle\langle 0|$ 的未归一化 Choi 矩阵并检验 CP 与 TP**

   - **题意与约定**：在本章未归一化最大纠缠向量 $|\Omega\rangle = |00\rangle + |11\rangle$（Watrous 约定）下，信道 $\mathcal{E}$ 的 Choi 矩阵定义为 $J_{\mathcal{E}} = (\mathcal{I}_{A'}\otimes\mathcal{E})(|\Omega\rangle\langle\Omega|) = \sum_{i,j=0}^1 |i\rangle\langle j| \otimes \mathcal{E}(|i\rangle\langle j|)$。逐个输入基矩阵 $|i\rangle\langle j|$ 代入 $\mathcal{R}$，写出完整 $4\times 4$ 矩阵，并分别检验完全正（$J_{\mathcal{R}} \succeq 0$）与保迹（$\operatorname{Tr}_B J_{\mathcal{R}} = I_{A'}$）。
   - **核心提示**：按未归一化 Choi 定义 $J_{\mathcal R}=\sum_{i,j=0}^1 |i\rangle\langle j|\otimes\mathcal R(|i\rangle\langle j|)$ 逐块计算四个 $2\times 2$ 子块（注意 $\operatorname{Tr}(|i\rangle\langle j|)=\delta_{ij}$），再检本征值非负（CP）与输出侧偏迹等于 $I$（TP）。
   - **完整分步演算**：
     - **第一步：逐项计算 $\mathcal{R}(|i\rangle\langle j|)$**。因为 $\operatorname{Tr}(|i\rangle\langle j|) = \langle j|i\rangle = \delta_{ij}$，故：

       $$
       \mathcal{R}(|0\rangle\langle 0|) = 1\cdot|0\rangle\langle 0|,
       \quad
       \mathcal{R}(|0\rangle\langle 1|) = 0,
       \quad
       \mathcal{R}(|1\rangle\langle 0|) = 0,
       \quad
       \mathcal{R}(|1\rangle\langle 1|) = 1\cdot|0\rangle\langle 0|.
       $$

     - **第二步：组装 Choi 矩阵 $J_{\mathcal{R}}$**。按定义把四个分块填入：

       $$
       J_{\mathcal{R}}
       = |0\rangle\langle 0|\otimes|0\rangle\langle 0| + |1\rangle\langle 1|\otimes|0\rangle\langle 0|
       = \bigl(|0\rangle\langle 0| + |1\rangle\langle 1|\bigr) \otimes |0\rangle\langle 0|
       = I \otimes |0\rangle\langle 0|.
       $$

       在大端基序 $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ 下写出显式 $4\times 4$ 矩阵：

       $$
       J_{\mathcal{R}} = \begin{pmatrix}
       1 & 0 & 0 & 0 \\
       0 & 0 & 0 & 0 \\
       0 & 0 & 1 & 0 \\
       0 & 0 & 0 & 0
       \end{pmatrix} = \operatorname{diag}(1, 0, 1, 0).
       $$

     - **第三步：分别检验完全正（CP）与保迹（TP）**。
       - **完全正（CP）**：$J_{\mathcal{R}}$ 是实对角矩阵，四个本征值为 $\{1, 0, 1, 0\}$，全部非负，故 $J_{\mathcal{R}} \succeq 0$，由 Choi 定理严格满足完全正（且由其两个特征向量 $|00\rangle, |10\rangle$ 直接读出 Kraus 算符 $K_0 = |0\rangle\langle 0|,\; K_1 = |0\rangle\langle 1|$，验算 $K_0^\dagger K_0 + K_1^\dagger K_1 = I$）；
       - **保迹（TP）**：对输出系统 $B$ 求偏迹：

         $$
         \operatorname{Tr}_B(J_{\mathcal{R}})
         = \operatorname{Tr}_B\bigl(I_{A'}\otimes |0\rangle\langle 0|_B\bigr)
         = I_{A'}\cdot \operatorname{Tr}(|0\rangle\langle 0|)
         = I_{A'}.
         $$

         顺带验证总迹 $\operatorname{Tr}(J_{\mathcal{R}}) = 1 + 0 + 1 + 0 = 2 = d$，完全符合未归一化约定。
   - **结论与边界回验**：在 $|\Omega\rangle = |00\rangle + |11\rangle$ 约定下，$J_{\mathcal{R}} = I\otimes|0\rangle\langle 0| = \operatorname{diag}(1,0,1,0)$；因其本征值 $\{1,0,1,0\}$ 均非负（$J_{\mathcal{R}} \succeq 0$）满足 CP，且 $\operatorname{Tr}_B J_{\mathcal{R}} = I$ 满足 TP，故 $\mathcal{R}$ 是合法的 CPTP 量子信道。
   - **易错坑提醒**：切忌只查 $J_{\mathcal{E}} \succeq 0$ 就宣布它是量子信道——半正定只保证完全正（CP），漏查 $\operatorname{Tr}_B J_{\mathcal{E}} = I_{A'}$ 会放过不保迹的缩放或截断映射。

3. **【基础】改用归一化最大纠缠态 $|\Phi_d\rangle = |\Omega\rangle/\sqrt{d}$ 定义 Choi 态时，总迹与保迹条件如何变化**

   - **题意与约定**：对照两大权威教材体系——Watrous（2018，本书主约定）用未归一化 $|\Omega\rangle = \sum_{i=0}^{d-1}|ii\rangle$ 定义 Choi 矩阵 $J_{\mathcal{E}}$，而 Wilde（2017）等文献用归一化最大纠缠态 $|\Phi_d\rangle = \frac{1}{\sqrt{d}}|\Omega\rangle$ 定义 Choi 态 $\Phi^{\mathcal{E}}$。把缩放系数 $1/d$ 逐项代入总迹与输出侧偏迹条件即可一眼看清换算关系。
   - **核心提示**：注意归一化 Choi 态 $\Phi_{\mathcal E}=\frac{1}{d}J_{\mathcal E}$ 只是对未归一化 Choi 矩阵整体除以维数 $d$，据此同步缩放总迹 $\operatorname{Tr}(\Phi_{\mathcal E})$ 与输出侧偏迹条件 $\operatorname{Tr}_B(\Phi_{\mathcal E})$。
   - **完整分步演算**：因 $|\Phi_d\rangle\langle\Phi_d| = \frac{1}{d}|\Omega\rangle\langle\Omega|$，由线性映射性质立得两者精确相差输入空间维数 $d$：

     $$
     \Phi^{\mathcal{E}}
     = (\mathcal{I}_{A'}\otimes\mathcal{E})(|\Phi_d\rangle\langle\Phi_d|)
     = \frac{1}{d}(\mathcal{I}_{A'}\otimes\mathcal{E})(|\Omega\rangle\langle\Omega|)
     = \frac{J_{\mathcal{E}}}{d}.
     $$

     - **保迹（TP）偏迹条件变化**：未归一化约定下保迹等价于 $\operatorname{Tr}_B J_{\mathcal{E}} = I_{A'}$；两边同除 $d$，归一化约定的保迹条件变为：

       $$
       \operatorname{Tr}_B\bigl(\Phi^{\mathcal{E}}\bigr) = \frac{1}{d}\operatorname{Tr}_B(J_{\mathcal{E}}) = \frac{I_{A'}}{d}.
       $$

     - **总迹变化**：对两边再取 $A'$ 上的迹（$\operatorname{Tr}(I_{A'}) = d$）：

       $$
       \operatorname{Tr}\bigl(\Phi^{\mathcal{E}}\bigr)
       = \operatorname{Tr}\!\left(\frac{I_{A'}}{d}\right) = \frac{d}{d} = 1,
       \qquad\text{（对照未归一化约定：}\operatorname{Tr}(J_{\mathcal{E}}) = d\text{）}.
       $$

     - **完全正（CP）条件不变**：因 $d > 0$，$\Phi^{\mathcal{E}} \succeq 0 \iff J_{\mathcal{E}} \succeq 0$。拿第 2 题 $d = 2$ 的单比特复位信道随手复验：$\Phi^{\mathcal{R}} = \frac{1}{2}J_{\mathcal{R}} = \operatorname{diag}(\frac{1}{2}, 0, \frac{1}{2}, 0)$，确实是迹为 $1$ 的合法两比特密度矩阵，且 $\operatorname{Tr}_B \Phi^{\mathcal{R}} = \frac{I}{2}$。
   - **结论与边界回验**：改用归一化最大纠缠态后，Choi 态满足 $\Phi^{\mathcal{E}} = J_{\mathcal{E}}/d$，其总迹从 $d$ 变为 $1$（本身成为合法二分密度矩阵），保迹偏迹条件从 $\operatorname{Tr}_B J_{\mathcal{E}} = I_{A'}$ 变为 $\operatorname{Tr}_B \Phi^{\mathcal{E}} = I_{A'}/d$。
   - **易错坑提醒**：跨教材查表或调包时忘记核对 Choi 矩阵是否除以了 $d$，把未归一化总迹 $d$ 误判成“信道不保迹”，或在从 Choi 态反解信道输出 $\mathcal{E}(\rho)$ 时漏乘因子 $d$。

4. **【计算】复算 $\rho = \operatorname{diag}(0.8, 0.2)$ 与 $\sigma = I/2$ 的量子相对熵，并解释为何不能与 Helstrom 单副本猜对率直接比较**

   - **题意与约定**：两矩阵同在计算基对角（彼此对易），直接套用量子相对熵定义 $D(\rho\|\sigma) = \operatorname{Tr}\bigl[\rho(\log_2\rho - \log_2\sigma)\bigr]$ 逐项计算（单位：$\mathrm{bit}$）；同时独立算出单副本等先验 Helstrom 最优猜对概率 $p_{\mathrm{guess}}$，从问题设定（多副本非对称 vs 单副本对称）、数学含义与物理单位三个层面说明二者不可混比。
   - **核心提示**：两矩阵同为对角阵，直接套用 $D(\rho\|\sigma)=\sum_i p_i\log_2(p_i/q_i)$ 逐项手算；第二问区分量子相对熵（对应多副本渐近指数衰减率，Stein 引理）与 Helstrom 界（对应单副本对称最小错误率）的操作意义。
   - **完整分步演算**：
     - **第一步：计算量子相对熵 $D(\rho\|\sigma)$**。因 $\rho = \operatorname{diag}(0.8, 0.2)$ 与 $\sigma = \operatorname{diag}(0.5, 0.5)$ 同时对角且支撑满足 $\operatorname{supp}(\rho) \subseteq \operatorname{supp}(\sigma)$，量子相对熵化为经典 KL 散度：

       $$
       \begin{aligned}
       D(\rho\|\sigma)
       &= 0.8\log_2\!\left(\frac{0.8}{0.5}\right) + 0.2\log_2\!\left(\frac{0.2}{0.5}\right) \\
       &= 0.8\log_2(1.6) + 0.2\log_2(0.4).
       \end{aligned}
       $$

       分别算两个对数（$\log_2(1.6) = \log_2(8/5) = 3 - \log_2 5 \approx 0.678071905$，$\log_2(0.4) = \log_2(2/5) = 1 - \log_2 5 \approx -1.321928095$）：

       $$
       \begin{aligned}
       D(\rho\|\sigma)
       &\approx 0.8 \times 0.678071905 + 0.2 \times (-1.321928095) \\
       &\approx 0.542457524 - 0.264385619
        = 0.278071905\ \mathrm{bit} \approx 0.2781\ \mathrm{bit}.
       \end{aligned}
       $$

       独立交叉验算：$D(\rho\|I/2) = \log_2 2 - S(\rho) = 1 - 0.721928095 = 0.278071905\ \mathrm{bit}$，与第 13 章第 1 题严丝合缝！
     - **第二步：计算单副本 Helstrom 成功率作对照**。差矩阵 $\rho - \sigma = \operatorname{diag}(0.3, -0.3)$，迹距离 $T(\rho,\sigma) = \frac{1}{2}(|0.3| + |-0.3|) = 0.3$，等先验单副本最优猜对率为

       $$
       p_{\mathrm{guess}} = \frac{1 + T(\rho,\sigma)}{2} = \frac{1 + 0.3}{2} = 0.65.
       $$

     - **第三步：阐明二者不可直接比大小的原因**。由量子 Stein 引理，$D(\rho\|\sigma) \approx 0.2781\ \mathrm{bit}$ 是**多副本（$n\to\infty$）非对称假设检验**（锁定第一类错误 $\alpha_n \le \epsilon$、最小化第二类错误 $\beta_n^*(\epsilon)$）下的渐近指数衰减率：$\lim_{n\to\infty} -\frac{1}{n}\log_2 \beta_n^*(\epsilon) = D(\rho\|\sigma)$，其值甚至可以大于 $1$ 乃至发散到 $+\infty$（当 $\operatorname{supp}(\rho)\not\subseteq\operatorname{supp}(\sigma)$ 时），单位是 $\mathrm{bit}$；而 $p_{\mathrm{guess}} = 0.65$ 是**单副本等先验对称判别**的无量纲概率（取值必在 $[0.5, 1]$）。
   - **结论与边界回验**：$D(\rho\|\sigma) \approx 0.2781\ \mathrm{bit}$（单副本 Helstrom 成功率为 $0.65$）；前者是渐近多副本非对称检验的指数衰减率（单位 $\mathrm{bit}$），后者是单副本对称判别的无量纲成功概率，任务、尺度与单位截然不同，不可直接比较大小。
   - **易错坑提醒**：一是把相对熵当成对称距离（实际上一般 $D(\rho\|\sigma) \ne D(\sigma\|\rho)$，本例中 $D(I/2\|\rho) = 0.5\log_2(0.5/0.8) + 0.5\log_2(0.5/0.2) \approx 0.3219 \ne 0.2781$）；二是把 $0.2781$ 误看成概率拿去和 $0.65$ 比较。

5. **【计算】单比特量子擦除信道 $\varepsilon = 1/4$ 时的四类容量 $C, Q, P, C_E$ 与报告规范**

   - **题意与约定**：单比特量子擦除信道以概率 $1-\varepsilon$ 完好透传输入态、以概率 $\varepsilon$ 输出与输入空间正交的可识别擦除旗标 $|e\rangle\langle e|$：$\mathcal{E}_\varepsilon(\rho) = (1-\varepsilon)\rho + \varepsilon\operatorname{Tr}(\rho)|e\rangle\langle e|$。由于其对称降解结构，四类渐近容量全部具有单字母精确闭式，直接代入 $\varepsilon = 1/4$ 计算并核对大小序关系。
   - **核心提示**：代入单比特量子擦除信道的四条精确闭式容量公式：$C=1-\varepsilon$、$Q=P=\max(0,1-2\varepsilon)$、$C_E=2(1-\varepsilon)$，并结合结果说明为何不交代任务与免费辅助资源就没法读懂“容量”。
   - **完整分步演算**：写出单比特擦除信道四类容量的精确闭式（全部按每次信道使用计，即 per use）：

     $$
     C = 1 - \varepsilon,
     \qquad
     Q = \max\{0,\, 1 - 2\varepsilon\},
     \qquad
     P = \max\{0,\, 1 - 2\varepsilon\},
     \qquad
     C_E = 2(1 - \varepsilon).
     $$

     将擦除概率 $\varepsilon = \frac{1}{4} = 0.25$ 逐项代入：
     - **经典容量（传普通经典消息，无辅助纠缠）**：

       $$
       C = 1 - \frac{1}{4} = \frac{3}{4} = 0.75\ \mathrm{bit/use}.
       $$

     - **量子容量（传未知量子态 / 生成纠缠）**：

       $$
       Q = \max\!\left\{0,\, 1 - 2\times\frac{1}{4}\right\} = 1 - \frac{1}{2} = 0.50\ \mathrm{qubit/use}.
       $$

     - **私密容量（传对窃听环境保密的经典消息）**：

       $$
       P = \max\!\left\{0,\, 1 - 2\times\frac{1}{4}\right\} = 1 - \frac{1}{2} = 0.50\ \mathrm{secret\ bit/use}.
       $$

     - **纠缠辅助经典容量（收发双方可免费使用无限预共享纠缠传经典消息）**：

       $$
       C_E = 2\left(1 - \frac{1}{4}\right) = 2\times\frac{3}{4} = 1.50\ \mathrm{bit/use}.
       $$

     边界与结构回验：数值满足普适排序 $Q \le P \le C \le C_E$（即 $0.50 \le 0.50 \le 0.75 \le 1.50$）；而当 $\varepsilon = 1/2$ 时，接收方与环境各拿到对称的一半擦除份额，由不可克隆定理必有 $Q = P = 0$（直接呼应第 12 章 $50\%$ 损耗边界），但此时仍能可靠传递 $C = 0.5\ \mathrm{bit/use}$ 普通经典信息！同时需强调 $P = Q$ 是擦除信道（及更一般降解信道）的特殊性质，并非普遍成立（某些零量子容量的束缚纠缠信道仍有严格正的私密容量 $P > Q = 0$）。
   - **结论与边界回验**：当 $\varepsilon = 1/4$ 时，$C = 0.75\ \mathrm{bit/use}$、$Q = 0.50\ \mathrm{qubit/use}$、$P = 0.50\ \mathrm{secret\ bit/use}$、$C_E = 1.50\ \mathrm{bit/use}$；同一物理信道对应四个不同数值，因此报告信道容量必须明确写清传输任务（经典/量子/私密）、允许的免费辅助资源（如预共享纠缠或双向经典通信）与每使用单位（per use）。
   - **易错坑提醒**：一是把信道容量误解为单一物理常数，甚至错标成通信工程速率单位 $\mathrm{bit/s}$；二是混淆四类任务，拿 $C_E = 1.50$ 去论证无辅助纠缠链路能突破单比特 $1\ \mathrm{bit}$ 限制（$C_E$ 本质上是超密编码 $2\ \mathrm{bit/use}$ 乘上存活率 $1-\varepsilon$）。

6. **【计算】加白噪声 Bell 态（Werner 态）取 $p = 0.6$：部分转置唯一负本征值、负性及对照指标**

   - **题意与约定**：考察两比特各向同性/加白噪声 Bell 态 $\rho_p = p|\Phi^+\rangle\langle\Phi^+| + (1-p)\frac{I_4}{4}$（$p \in [0, 1]$）。在大端序 $\{|00\rangle,|01\rangle,|10\rangle,|11\rangle\}$ 下显式写出 $\rho_p$ 的 $4\times 4$ 矩阵，对其第二个子系统 $B$ 的每个 $2\times 2$ 子块逐块转置得部分转置 $\rho_p^{T_B}$，求出全部四个精确本征值，再代入 $p = 0.6$ 计算负性 $\mathcal{N}$、对数负性 $E_N$、Wootters 共生度 $C_{\mathrm{conc}}$ 与形成纠缠 $E_F$。
   - **核心提示**：写出各向同性态 $\rho_p$ 的 $4\times 4$ 矩阵，对第二比特做部分转置 $\rho_p^{T_B}$ 后化为两个对角元与一个 $2\times 2$ 中心块，求全部四个本征值，代入负性 $\mathcal N=\sum_{\lambda_i<0}|\lambda_i|$ 与 $p=0.6$。
   - **完整分步演算**：
     - **第一步：写出 $\rho_p$ 与部分转置 $\rho_p^{T_B}$**。把 $4\times 4$ 矩阵按系统 $A$ 分成四个 $2\times 2$ 子块，对每个 $2\times 2$ 子块单独转置（仅左下角与右上角子块的 $(01)$ 和 $(10)$ 互换）：

       $$
       \rho_p = \frac{1}{4}\begin{pmatrix}
       1+p & 0 & 0 & 2p \\
       0 & 1-p & 0 & 0 \\
       0 & 0 & 1-p & 0 \\
       2p & 0 & 0 & 1+p
       \end{pmatrix}
       \;\xrightarrow{\;T_B\;}\;
       \rho_p^{T_B} = \frac{1}{4}\begin{pmatrix}
       1+p & 0 & 0 & 0 \\
       0 & 1-p & 2p & 0 \\
       0 & 2p & 1-p & 0 \\
       0 & 0 & 0 & 1+p
       \end{pmatrix}.
       $$

     - **第二步：分块求全部四个本征值**。
       - 外层两个 $1\times 1$ 对角元直接给出两个本征值：$\lambda_1 = \lambda_2 = \frac{1 + p}{4}$；
       - 中间 $2\times 2$ 对称块 $\frac{1}{4}\begin{pmatrix}1-p & 2p \\ 2p & 1-p\end{pmatrix}$ 的本征值为 $\frac{(1-p) \pm 2p}{4}$，即 $\lambda_3 = \frac{1 + p}{4}$ 与 $\lambda_4 = \frac{1 - 3p}{4}$。

       核验总迹：$3\cdot\frac{1+p}{4} + \frac{1-3p}{4} = \frac{3 + 3p + 1 - 3p}{4} = 1$！且由 PPT 判据，$\lambda_4 < 0 \iff p > \frac{1}{3}$。
     - **第三步：代入 $p = 0.6$ 计算负性及对照指标**。
       - 三个正本征值均为 $\frac{1 + 0.6}{4} = 0.4$，唯一负本征值为：

         $$
         \lambda_4 = \frac{1 - 3\times 0.6}{4} = \frac{1 - 1.8}{4} = -0.2.
         $$

       - 迹范数 $\|\rho_{0.6}^{T_B}\|_1 = 0.4 + 0.4 + 0.4 + |-0.2| = 1.4$，代入负性定义（亦等于全部负本征值绝对值之和）：

         $$
         \mathcal{N}(\rho_{0.6}) = \frac{\|\rho_{0.6}^{T_B}\|_1 - 1}{2} = \frac{1.4 - 1}{2} = 0.2
         \qquad\left(\text{核对公式 }\frac{3p-1}{4} = \frac{0.8}{4} = 0.2\right).
         $$

       - 同态三大常见混态纠缠指标对照：
         - **对数负性**：$E_N(\rho_{0.6}) = \log_2\bigl(1 + 2\mathcal{N}(\rho_{0.6})\bigr) = \log_2(1.4) \approx 0.4854\ \mathrm{ebit}$；
         - **Wootters 共生度**：$C_{\mathrm{conc}}(\rho_{0.6}) = \max\!\left\{0,\; \frac{3p-1}{2}\right\} = \frac{0.8}{2} = 0.4$；
         - **形成纠缠**：$E_F(\rho_{0.6}) = h_2\!\left(\frac{1 + \sqrt{1 - C_{\mathrm{conc}}^2}}{2}\right) = h_2\!\left(\frac{1 + \sqrt{0.84}}{2}\right) = h_2(0.958258) \approx 0.2502\ \mathrm{ebit}$。
   - **结论与边界回验**：$p = 0.6$ 时，部分转置 $\rho_{0.6}^{T_B}$ 的唯一负本征值为 $-0.2$，负性 $\mathcal{N}(\rho_{0.6}) = 0.2$（作为对照，同一态的对数负性 $E_N \approx 0.4854\ \mathrm{ebit}$、共生度 $C_{\mathrm{conc}} = 0.4$、形成纠缠 $E_F \approx 0.2502\ \mathrm{ebit}$）。
   - **易错坑提醒**：一是做部分转置时把整张 $4\times 4$ 矩阵全转置（全转置不改变本征值，抓不出纠缠！）；二是把 $0.2$、$0.4$、$0.2502$、$0.4854$ 这些不同定义下的混态纠缠数值混为一谈，报告混态纠缠必须明示具体度量名称。

7. **【基础】用量词写出 $\mathrm{QCMA}$ 与 $\mathrm{QMA}$ 的完备性与可靠性条件，并对比验证者与见证类型**

   - **题意与约定**：在计算复杂性理论中，$\mathrm{QMA}$ 与 $\mathrm{QCMA}$ 都是 $\mathrm{NP}$ / $\mathrm{MA}$ 的量子推广，处理带承诺（promise）的判定问题 $L = (L_{\mathrm{yes}}, L_{\mathrm{no}})$。用全称量词 $\forall$ 与存在量词 $\exists$ 严格写清两种实例上的接受概率约束、完备—可靠间隙 $c - s \ge 1/\operatorname{poly}(|x|)$，并一针见血地指出字母 `C` 修饰的对象。
   - **核心提示**：用“存在性量词 $\exists$（yes 情形存在好见证）”与“全称量词 $\forall$（no 情形任意见证均被低概率接受）”规范写清两类定义，重点对比量子多项式时间验证者是否相同，以及见证是经典比特串还是量子态。
   - **完整分步演算**：设 $x \in \{0,1\}^n$ 为输入实例（长度 $|x| = n$），$V_x$ 是由一致多项式时间经典算法生成的**多项式规模量子验证电路**，其末态输出 $1$ 比特判决结果 $V_x(w) \in \{0, 1\}$；设定阈值函数满足 $0 \le s(|x|) < c(|x|) \le 1$ 且承诺间隙 $c(|x|) - s(|x|) \ge \frac{1}{\operatorname{poly}(|x|)}$（经标准放大常取 $c = 2/3,\; s = 1/3$）。则两类复杂性类共享完全相同的量词结构：

     $$
     \begin{aligned}
     \text{完备性（yes 实例 } x \in L_{\mathrm{yes}}\text{）：}\quad & \exists\, w \in \mathcal{W}_n,\quad \Pr\bigl[V_x(w) = 1\bigr] \ge c(|x|), \\
     \text{可靠性（no 实例 } x \in L_{\mathrm{no}}\text{）：}\quad & \forall\, w \in \mathcal{W}_n,\quad \Pr\bigl[V_x(w) = 1\bigr] \le s(|x|).
     \end{aligned}
     $$

     两类唯一的本质区别在于见证空间 $\mathcal{W}_n$ 的物理类型：
     - **$\mathrm{QCMA}$（Quantum Classical Merlin–Arthur）**：验证者 $V_x$ 是**量子多项式时间电路**，但证明者（Merlin）提供的见证 $w$ 必须是多项式长度的**经典比特串** $w \in \{0,1\}^{p(n)}$（即“量子验证者 + 经典见证”）；
     - **$\mathrm{QMA}$（Quantum Merlin–Arthur）**：验证者 $V_x$ 同样是**量子多项式时间电路**，而见证 $w$ 可以是多项式数量量子比特上的任意**量子态** $\rho_w \in \mathcal{D}\bigl((\mathbb{C}^2)^{\otimes p(n)}\bigr)$（即“量子验证者 + 量子见证”，如局域哈密顿量问题的基态）。

     由此立得包含关系 $\mathrm{NP} \subseteq \mathrm{MA} \subseteq \mathrm{QCMA} \subseteq \mathrm{QMA}$（经典串可作为计算基态送入量子验证器，而一般纠缠量子态能否压缩成经典见证仍是公开核心难题）。
   - **结论与边界回验**：$\mathrm{QCMA}$ 与 $\mathrm{QMA}$ 共享“yes 实例 $\exists w$ 以 $\ge c$ 接受、no 实例 $\forall w$ 以 $\le s$ 接受”（$c - s \ge 1/\operatorname{poly}(|x|)$）的量词定义；两者的验证者**相同**（均为多项式时间量子验证者），仅**见证类型不同**（$\mathrm{QCMA}$ 为多项式长度经典串，$\mathrm{QMA}$ 为多项式量子比特量子态）。
   - **易错坑提醒**：看到 $\mathrm{QCMA}$ 中的字母 `C` 就望文生义成“经典验证者（Classical verifier）”，完全搞反了角色——`Q` 修饰验证者（Arthur，量子），`C` 修饰证明者发来的见证（Merlin，经典）。

8. **【基础】为什么 $\mathrm{QIP} = \mathrm{PSPACE}$ 不能解读成“普通量子计算机拥有求解全部 $\mathrm{PSPACE}$ 问题的高效算法”**

   - **题意与约定**：区分“带全能外部证明者的交互证明协议（$\mathrm{QIP}$）”与“单台独立运行的多项式时间量子计算机（$\mathrm{BQP}$）”两套计算模型，并对照 $\mathrm{IP} = \mathrm{PSPACE}$、$\mathrm{MIP}^* = \mathrm{RE}$ 与量子采样复杂度（BosonSampling / RCS 反证链），彻底防堵复杂性类定理的常见误读。
   - **核心提示**：区分“允许与无限算力外部证明者多轮交互的验证协议 $\mathrm{QIP}$”与“无外部帮助的独立量子计算类 $\mathrm{BQP}$”；前者即使在经典世界里 $\mathrm{IP}=\mathrm{PSPACE}$ 也早已成立，绝不意味着普通机器能高效自算 $\mathrm{PSPACE}$。
   - **完整分步演算**：
     - **交互证明模型的双角色结构**：$\mathrm{QIP}$（Quantum Interactive Proofs）协议由两方构成——一方是算力受限于量子多项式时间的**验证者**（Verifier），另一方是**计算能力完全不受限制（甚至可以运行指数时间乃至不可计算过程）但可能作弊的证明者**（Prover）。双方通过多项式轮量子消息往来交互，要求：对 yes 实例存在某个诚实证明策略以 $\ge 2/3$ 概率说服验证者；对 no 实例任何作弊策略都只能以 $\le 1/3$ 概率骗过验证者。
     - **与单机 $\mathrm{BQP}$ 的根本鸿沟**：Jain–Ji–Upadhyay–Watrous（2011）证明的 $\mathrm{QIP} = \mathrm{PSPACE}$ 刻画的是“在拥有全能证明者协助、且只需验证而不必自行搜索解的前提下，量子交互协议能验证的承诺问题总集合”（事实上经典交互证明早已有 Shamir 定理 $\mathrm{IP} = \mathrm{PSPACE}$，并不意味着经典电脑能多项式时间解 $\mathrm{PSPACE}$！）。而现实中的单台量子计算机对应的是**没有外部全能证明者**的 $\mathrm{BQP}$ 模型；目前公认 $\mathrm{BQP} \subseteq \mathrm{PP} \subseteq \mathrm{PSPACE}$，普遍猜想 $\mathrm{BQP}$ 严格小于 $\mathrm{PSPACE}$ 甚至不包含 $\mathrm{NP}$。
     - **同类复杂性防误读对照**：同理，$\mathrm{MIP}^* = \mathrm{RE}$（两个共享无限纠缠的全能证明者交互协议可验证停机问题）绝不说明现实量子计算机能解停机问题；而在第 7.4 节的**量子采样复杂度**理论（玻色采样、IQP、随机线路采样）中，通过 Stockmeyer 近似计数 + 反集中 + 平均情形猜想把“经典高效近似采样”导向“多项式层级 $\mathrm{PH}$ 坍塌至第 3 层”，证明的也是特定理想无噪采样分布的经典难模拟性，而非单机攻破 $\mathrm{PSPACE}$。
   - **结论与边界回验**：$\mathrm{QIP} = \mathrm{PSPACE}$ 依赖算力不受限的外部证明者协助验证，不是单台无协助量子计算机（$\mathrm{BQP}$）的独立求解算法，因此不能解读为量子计算机能高效求解全部 $\mathrm{PSPACE}$ 问题。
   - **易错坑提醒**：把所有带字母 `Q` 的复杂性类（$\mathrm{BQP}, \mathrm{QMA}, \mathrm{QIP}, \mathrm{MIP}^*$）统统当成“现实量子计算机自己能跑完的高效算法”，忽略了“独立求解”与“在无限算力证明者配合下做交互验证”的本质差别。

9. **【计算】双侧平衡码量子指纹的单次与 $10$ 次独立重复 SWAP 测试误报概率上界**

   - **题意与约定**：两方各持长经典串 $x, y$，经双侧平衡纠错码编码为长度 $m$ 的二进制码字 $E(x), E(y)$，使任意 $x \ne y$ 的相对 Hamming 距离 $\Delta_{xy} \in [1/4, 3/4]$，再制备对应相位指纹态 $|\phi_x\rangle = \frac{1}{\sqrt{m}}\sum_{j=1}^m (-1)^{E(x)_j}|j\rangle$。先由相对距离精确推算内积 $|\langle\phi_x|\phi_y\rangle|$ 的上界，再代入 SWAP 测试接受概率公式 $p_{\mathrm{same}} = \frac{1 + |\langle\phi_x|\phi_y\rangle|^2}{2}$ 算出单次与 $10$ 次独立副本全通过的精确分数与小数上界。
   - **核心提示**：先由双侧平衡码的相对 Hamming 距离范围 $[1/4,3/4]$ 算出两量子指纹态内积 $|\langle h(x)|h(y)\rangle|\le 1/2$，代入单次 SWAP 测试接受概率 $\frac{1+|\langle\psi|\phi\rangle|^2}{2}$ 得单次误报上界，再取 $10$ 次幂。
   - **完整分步演算**：
     - **第一步：计算不同输入指纹的内积上界**。在全部 $m$ 个坐标中，有 $(1 - \Delta_{xy})m$ 位满足 $E(x)_j = E(y)_j$（贡献 $+1$），有 $\Delta_{xy} m$ 位满足 $E(x)_j \ne E(y)_j$（贡献 $-1$），故内积精确为

       $$
       \langle\phi_x|\phi_y\rangle
       = \frac{1}{m}\Bigl[(1 - \Delta_{xy})m - \Delta_{xy} m\Bigr]
       = 1 - 2\Delta_{xy}.
       $$

       代入双侧条件 $\frac{1}{4} \le \Delta_{xy} \le \frac{3}{4}$，逐边乘 $-2$ 加 $1$ 得：

       $$
       1 - 2\left(\frac{3}{4}\right) \le 1 - 2\Delta_{xy} \le 1 - 2\left(\frac{1}{4}\right)
       \implies
       -\frac{1}{2} \le \langle\phi_x|\phi_y\rangle \le +\frac{1}{2}
       \implies
       |\langle\phi_x|\phi_y\rangle| \le \frac{1}{2}.
       $$

       （注意为何必须“双侧”限制：若 $\Delta_{xy}$ 接近 $1$，内积接近 $-1$，模平方仍接近 $1$，SWAP 测试照样高概率误报“相同”！）
     - **第二步：单次 SWAP 测试误报上界**。当 $x = y$ 时 $|\langle\phi_x|\phi_y\rangle| = 1$，SWAP 测试必以概率 $1$ 输出 $0$（判“相同”）；当 $x \ne y$ 时，误报“相同”的概率上界为：

       $$
       p_{\mathrm{same}}
       = \frac{1 + |\langle\phi_x|\phi_y\rangle|^2}{2}
       \le \frac{1 + (1/2)^2}{2}
       = \frac{1 + 1/4}{2}
       = \frac{5}{8} = 0.625.
       $$

     - **第三步：$10$ 次独立重复全部通过的误报上界**。独立制备 $10$ 对全新量子指纹并分别执行 SWAP 测试，仅当 $10$ 次全部输出 $0$ 才判“相同”，其联合误报概率上界为：

       $$
       p_{\mathrm{err},10}
       \le \left(\frac{5}{8}\right)^{10}
       = \frac{5^{10}}{8^{10}}
       = \frac{9{,}765{,}625}{1{,}073{,}741{,}824}
       \approx 0.00909495 \approx 0.909\%.
       $$

       （此时 $x=y$ 的正确接受概率仍保持 $1^{10} = 1$，实现单边零漏报与指数压低误报。）
   - **结论与边界回验**：输入不同时，单次 SWAP 测试误报“相同”的概率上界为 $\frac{5}{8} = 0.625$；独立重复 $10$ 次且全通过才判“相同”的误报上界为 $(5/8)^{10} = \frac{9{,}765{,}625}{1{,}073{,}741{,}824} \approx 0.009095$（约 $0.91\%$）。
   - **易错坑提醒**：一是忘记“$10$ 次独立重复”必须由发送方送出 $10$ 份全新制备的量子指纹，绝不能拿第一轮已经坍缩变形的测后态反复再跑 SWAP 测试；二是以为纠错码只要满足最小相对距离 $\Delta_{xy} \ge 1/4$ 就够了，忽略了距离过大（$\Delta_{xy} \to 1$）会导致相位内积趋近 $-1$ 而令 SWAP 测试失效。

10. **【计算】计算 $r = (\ln 2)/2$ 的单模压缩真空态方差 $\operatorname{Var}(\hat{q}), \operatorname{Var}(\hat{p})$、乘积与不确定性关系**

    - **题意与约定**：在本章连续变量无量纲正交分量约定 $[\hat{q}, \hat{p}] = i$（等价于 $\hbar = 1$，真空态协方差 $V = \frac{1}{2}I_2$）下，单模压缩真空态 $|r\rangle$ 具有零均值 $\langle\hat{q}\rangle = \langle\hat{p}\rangle = 0$ 与主轴方差 $\operatorname{Var}(\hat{q}) = \frac{1}{2}e^{-2r}$、$\operatorname{Var}(\hat{p}) = \frac{1}{2}e^{2r}$。代入 $r = (\ln 2)/2$ 精确求值，并与 Heisenberg–Robertson 不确定性下界 $\frac{1}{4}|\langle[\hat{q},\hat{p}]\rangle|^2 = \frac{1}{4}$ 核对。
    - **核心提示**：在 $[\hat q,\hat p]=i$（真空方差 $1/2$）约定下，单模压缩真空态的正交方差为 $\operatorname{Var}(\hat q)=\frac{1}{2}e^{-2r}$ 与 $\operatorname{Var}(\hat p)=\frac{1}{2}e^{2r}$，代入 $r=(\ln 2)/2$ 并检验乘积是否饱和下界 $1/4$。
    - **完整分步演算**：
      - **第一步：计算指数缩放因子 $e^{\pm 2r}$**。由 $r = \frac{\ln 2}{2}$ 得 $2r = \ln 2$，于是：

        $$
        e^{-2r} = e^{-\ln 2} = \frac{1}{2},
        \qquad
        e^{2r} = e^{\ln 2} = 2.
        $$

      - **第二步：代入两正交分量方差公式**：

        $$
        \operatorname{Var}(\hat{q}) = \frac{1}{2} e^{-2r} = \frac{1}{2}\cdot\frac{1}{2} = \frac{1}{4} = 0.25,
        \qquad
        \operatorname{Var}(\hat{p}) = \frac{1}{2} e^{2r} = \frac{1}{2}\cdot 2 = 1.
        $$

      - **第三步：计算方差乘积并对照不确定性原理**。两方差相乘：

        $$
        \operatorname{Var}(\hat{q})\,\operatorname{Var}(\hat{p}) = \frac{1}{4} \times 1 = \frac{1}{4}.
        $$

        在 $[\hat{q}, \hat{p}] = i$ 约定下，一般物理态的 Robertson 不确定性关系要求

        $$
        \operatorname{Var}(\hat{q})\,\operatorname{Var}(\hat{p})
        \ge \frac{1}{4}\bigl|\langle[\hat{q}, \hat{p}]\rangle\bigr|^2
        = \frac{1}{4}|i|^2
        = \frac{1}{4}.
        $$

        可见该压缩真空态的相空间 Wigner 椭圆面积（对应乘积 $\frac{1}{4}$）与真空圆盘完全相同，**恰好饱和不确定性下界**：$\hat{q}$ 方向的噪声方差相对真空 $1/2$ 压缩了一半（压至 $1/4$），但共轭分量 $\hat{p}$ 的方差严格按倒数倍数放大了一倍（涨至 $1$），丝毫没有突破量子不确定性原理。
    - **结论与边界回验**：$\operatorname{Var}(\hat{q}) = \frac{1}{4}$，$\operatorname{Var}(\hat{p}) = 1$，两者乘积为 $\frac{1}{4}$，恰好饱和 $[\hat{q}, \hat{p}] = i$ 下的不确定性下界 $\frac{1}{4}$；它靠牺牲共轭分量 $\hat{p}$ 的精度换取 $\hat{q}$ 的压噪，未违反不确定性关系。
    - **易错坑提醒**：跨文献查阅高斯光学公式时最易踩 $\hbar$ 约定坑——例如 Weedbrook（*RMP* 2012）取 $\hbar = 2$（此时真空方差为 $1$、不确定性下界为 $1$），而 Serafini（2023）取 $\hbar = 1$ 但协方差矩阵不带 $1/2$ 因子；代入数字前必须先核对 $[\hat{q},\hat{p}]$ 的常数因子。

11. **【进阶】恒等信道 $\mathcal{I}$ 的 Choi 矩阵谱与偏迹，以及转置映射 $\mathcal{T}(X) = X^T$ 为何不完全正**

    - **题意与约定**：延续本章未归一化约定 $|\Omega\rangle = |00\rangle + |11\rangle$，先写出单比特恒等信道 Choi 矩阵 $J_{\mathcal{I}} = |\Omega\rangle\langle\Omega|$，求其全部本征值与 $\operatorname{Tr}_B J_{\mathcal{I}}$；再写出转置映射 $\mathcal{T}(X) = X^T$ 的 Choi 矩阵 $J_{\mathcal{T}}$，显式构造负本征值对应的反对称态 $|\Psi^-\rangle$，证明它违背完全正性，并衔接钻石范数对纠缠探针的必要性。
    - **核心提示**：写出 $J_{\mathcal I}=|\Omega\rangle\langle\Omega|$ 求其秩 $1$ 本征值与输出侧偏迹；对转置映射 $\mathcal T$ 写出 $J_{\mathcal T}=\sum_{ij}|i\rangle\langle j|\otimes|j\rangle\langle i|$（恰为 $\mathrm{SWAP}$ 算符！），直接由 $\mathrm{SWAP}$ 的 $-1$ 本征值证伪 CP。
    - **完整分步演算**：
      - **第一部分：恒等信道 $\mathcal{I}$**。在大端基序 $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ 下，由 $\mathcal{I}(|i\rangle\langle j|) = |i\rangle\langle j|$ 得

        $$
        J_{\mathcal{I}}
        = \sum_{i,j=0}^1 |i\rangle\langle j| \otimes |i\rangle\langle j|
        = |\Omega\rangle\langle\Omega|
        = \begin{pmatrix}
        1 & 0 & 0 & 1 \\
        0 & 0 & 0 & 0 \\
        0 & 0 & 0 & 0 \\
        1 & 0 & 0 & 1
        \end{pmatrix}.
        $$

        - **本征值**：$J_{\mathcal{I}}$ 是秩 $1$ 厄米矩阵，因 $\langle\Omega|\Omega\rangle = 1^2 + 1^2 = 2$，故 $J_{\mathcal{I}}|\Omega\rangle = |\Omega\rangle\langle\Omega|\Omega\rangle = 2|\Omega\rangle$，唯一非零本征值为 $2$，与 $|\Omega\rangle$ 正交的三个方向本征值均为 $0$。全部四个本征值为 $\{2, 0, 0, 0\} \ge 0$，满足 CP。
        - **输出侧偏迹**：把 $J_{\mathcal{I}} = |00\rangle\langle 00| + |00\rangle\langle 11| + |11\rangle\langle 00| + |11\rangle\langle 11|$ 对 $B$ 取偏迹，两个交叉项带 $\langle 1|0\rangle = 0$ 与 $\langle 0|1\rangle = 0$ 全部消去，剩下：

          $$
          \operatorname{Tr}_B(J_{\mathcal{I}}) = |0\rangle\langle 0| + |1\rangle\langle 1| = I,
          $$

          满足 TP。
      - **第二部分：转置映射 $\mathcal{T}(X) = X^T$**。因 $\mathcal{T}(|i\rangle\langle j|) = |j\rangle\langle i|$，其 Choi 矩阵为两比特交换算符（SWAP 矩阵 $\mathsf{S}$）：

        $$
        J_{\mathcal{T}}
        = \sum_{i,j=0}^1 |i\rangle\langle j| \otimes |j\rangle\langle i|
        = \begin{pmatrix}
        1 & 0 & 0 & 0 \\
        0 & 0 & 1 & 0 \\
        0 & 1 & 0 & 0 \\
        0 & 0 & 0 & 1
        \end{pmatrix}.
        $$

        取单重态 $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}} = \frac{1}{\sqrt{2}}[0, 1, -1, 0]^T$ 逐行相乘验证：

        $$
        J_{\mathcal{T}}|\Psi^-\rangle
        = \frac{1}{\sqrt{2}}\begin{pmatrix} 1&0&0&0 \\ 0&0&1&0 \\ 0&1&0&0 \\ 0&0&0&1 \end{pmatrix}\begin{pmatrix} 0 \\ 1 \\ -1 \\ 0 \end{pmatrix}
        = \frac{1}{\sqrt{2}}\begin{pmatrix} 0 \\ -1 \\ 1 \\ 0 \end{pmatrix}
        = -|\Psi^-\rangle.
        $$

        可见 $J_{\mathcal{T}}$ 的四个本征值为 $\{+1, +1, +1, -1\}$，含有严格负本征值 $-1$，故 $J_{\mathcal{T}} \not\succeq 0$！虽然转置对任意**单个**量子比特的正半定矩阵保持正性且保迹，可一旦仅作用在纠缠对的一半上（如 $(\mathcal{I}\otimes\mathcal{T})(|\Phi^+\rangle\langle\Phi^+|) = \frac{1}{2}J_{\mathcal{T}}$），立刻吐出 $-1/2$ 的负概率，因此它不是完全正映射（这也正是为何评价量子信道距离必须引入参考纠缠系统的**钻石范数** $\|\mathcal{E}_1 - \mathcal{E}_2\|_\diamond = \sup_\rho \|(\mathcal{I}\otimes(\mathcal{E}_1 - \mathcal{E}_2))(\rho)\|_1$）。
    - **结论与边界回验**：$J_{\mathcal{I}} = |\Omega\rangle\langle\Omega|$ 的四个本征值为 $\{2, 0, 0, 0\}$，偏迹 $\operatorname{Tr}_B J_{\mathcal{I}} = I$（CPTP）；转置映射的 Choi 矩阵 $J_{\mathcal{T}} = \mathsf{S}$ 在反对称态 $|\Psi^-\rangle$ 上取本征值 $-1 < 0$，不满足半正定性，故无法通过完全正判据。
    - **易错坑提醒**：误以为“对一切单比特合法密度矩阵都输出合法密度矩阵的保迹线性映射就是合法量子信道”——转置映射是最经典反例，正性（P）严格弱于完全正性（CP）。

12. **【进阶】单副本非对称假设检验：约束 $\alpha \le 0.1$ 下求最小 $t$、第二类错误 $\beta$ 与 $D_H^{0.1}(\rho\|\sigma)$**

    - **题意与约定**：对对角态 $\rho = \operatorname{diag}(0.8, 0.2)$（原假设）与 $\sigma = I/2 = \operatorname{diag}(0.5, 0.5)$（备择假设）做单副本随机化检验：接受 $\rho$ 的 POVM 算符取为 $M = |0\rangle\langle 0| + t|1\rangle\langle 1| = \operatorname{diag}(1, t)$（$0 \le t \le 1$）。先由第一类错误 $\alpha = \operatorname{Tr}[(I - M)\rho] \le 0.1$ 解出最小允许 $t$，再算第二类错误 $\beta = \operatorname{Tr}(M\sigma)$ 与单副本假设检验相对熵 $D_H^{0.1}(\rho\|\sigma) = -\log_2 \beta$，最后用 Neyman–Pearson 似然比证明其全局最优性。
    - **核心提示**：因两态对角，取对角检验算符 $T=\operatorname{diag}(t_0,t_1)$（$0\le t_0,t_1\le 1$），按 Neyman–Pearson 引理优先给似然比 $p_i/q_i$ 更大的分量分配权重，在 $\alpha=1-(0.8t_0+0.2t_1)\le 0.1$ 下最小化 $\beta=0.5(t_0+t_1)$，最后算 $D_H^{0.1}=-\log_2\beta$。
    - **完整分步演算**：
      - **第一步：写出两类错误概率并求最小 $t$**。在 $\rho = \operatorname{diag}(0.8, 0.2)$ 下接受 $\rho$ 的概率为 $\operatorname{Tr}(M\rho) = 1\cdot 0.8 + t\cdot 0.2 = 0.8 + 0.2t$，故误拒 $\rho$ 的第一类错误概率为：

        $$
        \alpha = 1 - \operatorname{Tr}(M\rho) = 1 - (0.8 + 0.2t) = 0.2 - 0.2t.
        $$

        代入约束 $\alpha \le 0.1$：

        $$
        0.2 - 0.2t \le 0.1 \iff 0.2t \ge 0.1 \iff t \ge \frac{1}{2} = 0.5.
        $$

      - **第二步：最小化第二类错误 $\beta$ 并求 $D_H^{0.1}(\rho\|\sigma)$**。在 $\sigma = \operatorname{diag}(0.5, 0.5)$ 下误把 $\sigma$ 当作 $\rho$ 接受的第二类错误概率为：

        $$
        \beta = \operatorname{Tr}(M\sigma) = 1\cdot 0.5 + t\cdot 0.5 = 0.5 + 0.5t.
        $$

        因为 $\beta$ 关于 $t$ 严格单调递增，在可行域 $t \in [1/2, 1]$ 上取最小值 $t^* = \frac{1}{2}$，对应最小第二类错误为：

        $$
        \beta^* = 0.5 + 0.5\times\frac{1}{2} = 0.75 = \frac{3}{4}.
        $$

        代入假设检验相对熵定义（以 $2$ 为底）：

        $$
        D_H^{0.1}(\rho\|\sigma)
        = -\log_2 \beta^*
        = -\log_2\!\left(\frac{3}{4}\right)
        = \log_2\!\left(\frac{4}{3}\right)
        = 2 - \log_2 3
        \approx 2 - 1.5849625
        = 0.4150375\ \mathrm{bit} \approx 0.4150\ \mathrm{bit}.
        $$

      - **第三步：证明该策略在全部量子 POVM 中全局最优**。对任意一般 POVM 元素 $0 \preceq M \preceq I$，设其对角元为 $m_0, m_1 \in [0, 1]$。因 $\rho, \sigma$ 均为对角阵，非对角元完全不进入 $\operatorname{Tr}(M\rho) = 0.8m_0 + 0.2m_1$ 与 $\operatorname{Tr}(M\sigma) = 0.5m_0 + 0.5m_1$；比较两个结果的似然比：结果 $0$ 的似然比 $0.8/0.5 = 1.6$ 严格大于结果 $1$ 的 $0.2/0.5 = 0.4$，故为了在达到 $\operatorname{Tr}(M\rho) \ge 0.9$ 的同时把 $\operatorname{Tr}(M\sigma)$ 压到最低，必先将高似然比项 $m_0$ 拉满至 $1$，再把多余预算补给 $m_1 = t = 1/2$。
    - **结论与边界回验**：允许的最小参数为 $t = \frac{1}{2}$，对应的最优第二类错误为 $\beta = \frac{3}{4} = 0.75$，单副本假设检验相对熵为 $D_H^{0.1}(\rho\|\sigma) = -\log_2(0.75) \approx 0.4150\ \mathrm{bit}$。
    - **易错坑提醒**：只考虑确定性投影测量（$t \in \{0, 1\}$），会以为 $t=0$ 不满足 $\alpha = 0.2 \le 0.1$ 只能退而取 $t=1$（给出 $\beta=1,\; D_H^{0.1}=0$），错过了随机化 POVM（在测得 `1` 时抛硬币以 $1/2$ 概率接受）带来的非零分辨力。

13. **【计算】计算经典相关混态 $\rho_{AB}^{\mathrm{sep}} = \frac{1}{2}|00\rangle\langle 00| + \frac{1}{2}|11\rangle\langle 11|$ 的约化态与局部熵，并说明为何不代表 $1\ \mathrm{ebit}$ 纠缠**

    - **题意与约定**：先逐项做偏迹算出约化密度矩阵 $\rho_A$ 及其 von Neumann 熵 $S(A)$，再用两条独立判据——可分离显式凸分解与部分转置 PPT 检验（负性 $\mathcal{N} = 0$）——严格确认该态纠缠为零，澄清局部熵仅在整体为纯态时才代表纠缠。
    - **核心提示**：先对经典相关混态求偏迹 $\rho_A$ 与局部熵 $S(A)$，再用显式可分分解、部分转置 PPT 检验以及第 18 章量子相干信息 $I_c(A\rangle B)=S(B)-S(AB)$ 三重交叉验证其纠缠与可蒸馏资源均为零。
    - **完整分步演算**：
      - **第一步：偏迹求 $\rho_A$ 与 $S(A)$**。对子系统 $B$ 求偏迹，利用 $\operatorname{Tr}_B(|00\rangle\langle 00|) = |0\rangle\langle 0|\cdot\langle 0|0\rangle = |0\rangle\langle 0|$ 与 $\operatorname{Tr}_B(|11\rangle\langle 11|) = |1\rangle\langle 1|\cdot\langle 1|1\rangle = |1\rangle\langle 1|$：

        $$
        \rho_A = \operatorname{Tr}_B\bigl(\rho_{AB}^{\mathrm{sep}}\bigr)
        = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1|
        = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix}
        = \frac{I}{2}.
        $$

        两个本征值均为 $1/2$，故局部熵为：

        $$
        S(A) = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2} = 1\ \mathrm{bit}.
        $$

      - **第二步：双路径证伪“$1\ \mathrm{ebit}$ 纠缠”**。
        - **可分定义**：$\rho_{AB}^{\mathrm{sep}} = \frac{1}{2}(|0\rangle\langle 0|\otimes|0\rangle\langle 0|) + \frac{1}{2}(|1\rangle\langle 1|\otimes|1\rangle\langle 1|)$ 已是乘积态的经典概率混合，仅靠 LOCC（局域操作加经典抛硬币通信）即可无纠缠制备；
        - **部分转置回验**：因为 $\rho_{AB}^{\mathrm{sep}} = \operatorname{diag}(1/2, 0, 0, 1/2)$ 是实对角阵，其部分转置完全不变：$(\rho_{AB}^{\mathrm{sep}})^{T_B} = \rho_{AB}^{\mathrm{sep}} \succeq 0$，无任何负本征值，故负性 $\mathcal{N} = 0$、对数负性 $E_N = 0$、形成纠缠 $E_F = 0$。

        之所以 $S(A) = 1\ \mathrm{bit}$，是因为整体态本身是混合态（$S(AB) = 1\ \mathrm{bit} > 0$），单看一端的不确定性完全来源于经典的“不知发了 $00$ 还是 $11$”，而非跨系统的量子纠缠；只有在整体是纯态（$S(AB) = 0$）的前提下，$S(A) = 1\ \mathrm{bit}$ 才代表 $1\ \mathrm{ebit}$ 纠缠。
      - **信道容量与相干信息深化（第 18 章专属视角）**：进一步从量子通信资源的角度计算量子相干信息 $I_c(A\rangle B) = S(B) - S(AB)$（哈希界给出的可蒸馏纠缠下界）：对最大纠缠纯态 $|\Phi^+\rangle$，有 $S(B) = 1\ \mathrm{bit},\; S(AB) = 0 \implies I_c(A\rangle B) = +1\ \mathrm{bit}$（可提取 $1\ \mathrm{ebit}$）；而对本题的经典相关混态 $\rho_{AB}^{\mathrm{sep}}$，因 $S(B) = 1\ \mathrm{bit},\; S(AB) = 1\ \mathrm{bit}$，故：

        $$
        I_c(A\rangle B) = S(B) - S(AB) = 1 - 1 = 0\ \mathrm{bit},
        \qquad
        E_D\bigl(\rho_{AB}^{\mathrm{sep}}\bigr) = 0.
        $$

        由此把[第 3 章第 11 题](#第-3-章)的可分性直观与[第 13 章第 6 题](#第-13-章)的 Werner 态负性检验，统一收束到第 18 章的纠缠蒸馏与量子容量框架中。
    - **结论与边界回验**：约化态 $\rho_A = I/2$，局部熵 $S(A) = 1\ \mathrm{bit}$；但它属于零纠缠的经典可分离混态（$\mathcal{N} = 0,\; S(AB) = 1\ \mathrm{bit}$），绝不代表 $1\ \mathrm{ebit}$ 量子纠缠。
    - **易错坑提醒**：把纯态下的纠缠熵公式 $E(|\psi\rangle_{AB}) = S(\rho_A)$ 不加前提地照搬到混态上，误把最大混合噪声或经典共享随机性当成最大纠缠。

14. **【计算】计算 $r = (\ln 2)/2$ 压缩真空态的平均光子数 $\bar{n}$，并说明连续变量为何必须施加能量约束**

    - **题意与约定**：先通过两条独立路径——由第 10 题的方差 $(\operatorname{Var}(\hat{q}), \operatorname{Var}(\hat{p})) = (1/4, 1)$ 代入光子数算符 $\hat{a}^\dagger\hat{a} = \frac{\hat{q}^2 + \hat{p}^2 - 1}{2}$，以及直接套用压缩真空闭式 $\bar{n} = \sinh^2 r$——精确算得平均光子数 $\bar{n} = 1/8$；再从无限维相空间无界算符、能量约束钻石范数、Fock 空间截断尾界及 GKP 网格态的物理可制备性四个方面，讲透能量约束的不可替代性。
    - **核心提示**：分别用恒等式 $\bar n=\sinh^2 r$ 与相空间能量公式 $\bar n=\frac{1}{2}(\operatorname{Var}(\hat q)+\operatorname{Var}(\hat p)-1)$ 双路径互算平均光子数；再结合无穷维空间无界能量可造出任意陡峭误差说明能量约束的必要性。
    - **完整分步演算**：
      - **路径一（从正交分量方差推导）**：在本章约定 $[\hat{q}, \hat{p}] = i$ 下，湮灭与产生算符定义为 $\hat{a} = \frac{\hat{q} + i\hat{p}}{\sqrt{2}}$、$\hat{a}^\dagger = \frac{\hat{q} - i\hat{p}}{\sqrt{2}}$。展开光子数算符 $\hat{n} = \hat{a}^\dagger\hat{a}$：

        $$
        \hat{a}^\dagger\hat{a}
        = \frac{(\hat{q} - i\hat{p})(\hat{q} + i\hat{p})}{2}
        = \frac{\hat{q}^2 + \hat{p}^2 + i(\hat{q}\hat{p} - \hat{p}\hat{q})}{2}
        = \frac{\hat{q}^2 + \hat{p}^2 + i[\hat{q}, \hat{p}]}{2}
        = \frac{\hat{q}^2 + \hat{p}^2 - 1}{2}.
        $$

        因为压缩真空态具有零均值（$\langle\hat{q}\rangle = \langle\hat{p}\rangle = 0$），二阶矩精确等于方差：$\langle\hat{q}^2\rangle = \operatorname{Var}(\hat{q}) = \frac{1}{4}$、$\langle\hat{p}^2\rangle = \operatorname{Var}(\hat{p}) = 1$。代入得：

        $$
        \bar{n} = \langle\hat{a}^\dagger\hat{a}\rangle = \frac{\frac{1}{4} + 1 - 1}{2} = \frac{1}{8} = 0.125.
        $$

      - **路径二（由双曲函数闭式独立验算）**：利用 $e^r = 2^{1/2} = \sqrt{2}$ 与 $e^{-r} = \frac{1}{\sqrt{2}}$，算得：

        $$
        \sinh r = \frac{e^r - e^{-r}}{2} = \frac{\sqrt{2} - 1/\sqrt{2}}{2} = \frac{1}{2\sqrt{2}},
        \qquad
        \bar{n} = \sinh^2 r = \left(\frac{1}{2\sqrt{2}}\right)^2 = \frac{1}{8} = 0.125.
        $$

        两条路径精确吻合！
      - **为何连续变量近似精度与信道距离必须施加能量约束**：
        1. **压缩与能量刚性绑定**：要继续压低 $\operatorname{Var}(\hat{q}) = \frac{1}{2}e^{-2r}$，共轭方差 $\frac{1}{2}e^{2r}$ 与平均光子数 $\bar{n} = \sinh^2 r \sim \frac{1}{4}e^{2r}$ 同步指数暴涨；
        2. **无约束钻石范数病态跳跃**：在无限维空间里，只要允许输入任意高能量态，哪怕极微小的相移偏差 $\theta \to 0$ 也能把两个相差极小的信道拉开到最大距离 $\|\mathcal{U}_\theta - \mathcal{I}\|_\diamond = 2$（失去连续性），因此必须采用**能量约束钻石范数** $\|\mathcal{E}_1 - \mathcal{E}_2\|_{\diamond, E}$（限定 $\operatorname{Tr}(\hat{n}\rho) \le E$）；
        3. **数值模拟 Fock 截断尾界**：有限维截断至 $d$ 层时，由 Markov 不等式知截断遗漏概率满足 $\tau_d(\rho) \le \bar{n}/d$，必须凭平均能量控制截断误差与迹距离；
        4. **非高斯玻色编码（如 GKP 网格态）的物理边界**：正文第 9.5 节指出，方形 GKP 码由步长 $2\sqrt{\pi}$ 的位移稳定子围出面积 $4\pi = 2\times 2\pi$ 的相空间晶胞以容纳 $d=2$ 维逻辑比特（$[i2\sqrt{\pi}\hat{q}, -i2\sqrt{\pi}\hat{p}] = 4\pi i \Rightarrow e^{4\pi i}=1$），其理想狄拉克梳态需要无限压缩与无穷大能量，实际硬件必须施加有限能量阻尼包络 $\hat{E}_\Delta = e^{-\Delta^2\hat{a}^\dagger\hat{a}}$ 才能物理制备。
    - **结论与边界回验**：$r = (\ln 2)/2$ 的单模压缩真空态平均光子数为 $\bar{n} = \frac{1}{8} = 0.125$；在无限维希尔伯特空间中，信道距离连续性、Fock 截断误差界与 GKP 等非高斯编码的可实现性全部依赖有限平均能量约束，脱离能量预算谈“近似精度”或“信道距离”在数学和物理上都不良定。
    - **易错坑提醒**：一是忘记减去零点能对应项 $-1/2$（把 $\frac{1/4+1}{2} = 5/8$ 误算成平均光子数，其实真空态已有 $\frac{1/2+1/2}{2} = 1/2$，减完才是 $\bar{n}=0$！）；二是在无限维 Fock 截断仿真中把截断后的态向量偷偷重新归一化就宣称“截断无误差”。

## 第 19 章

> 对应章节：《19｜可维护量子系统工程》（共 12 题）

1. **【基础】为什么读出判决保真度很高，仍不能说明中途测量适合量子纠错**

   - **题意与约定**：区分“终止读出（只关心经典 `0/1` 报告对不对）”与“纠错中途测量（量子仪器，同时决定经典结果、测后量子态以及对邻近数据比特的扰动）”。用正文第 3.2 节的精确 Kraus 反例（理想投影 QND 仪器 A vs 破坏性读出加主动复位仪器 B）与第 3.1 节的旁观串扰算例，从数学与物理双视角拆透判决保真度的盲区。
   - **核心提示**：区分“仅关心经典 `0/1` 报告对错的终止判决保真度”与“纠错中途测量作为量子仪器必须同时保住测后量子态、不引发高能泄漏且不扰动邻近数据比特”的严格要求。
   - **完整分步演算**：
     - **反例一（相同 POVM 与 $100\%$ 判决保真度，截然不同的测后状态）**：在二维空间 $\mathbb{C}^2$ 上对比两台测量仪器：
       - **仪器 A（理想投影 QND）**：$K_0 = |0\rangle\langle 0|,\; K_1 = |1\rangle\langle 1|$；
       - **仪器 B（破坏性读出并主动复位至 $|0\rangle$）**：$L_0 = |0\rangle\langle 0|,\; L_1 = |0\rangle\langle 1|$。

       逐项计算两者的 POVM 元素：

       $$
       K_0^\dagger K_0 = L_0^\dagger L_0 = |0\rangle\langle 0|,
       \qquad
       K_1^\dagger K_1 = |1\rangle\langle 1| = (|1\rangle\langle 0|)(|0\rangle\langle 1|) = L_1^\dagger L_1.
       $$

       因此对任何输入态 $\rho$，两台仪器的首轮报告概率 $P(m) = \langle m|\rho|m\rangle$ 完全一致，常规读出判决保真度（assignment fidelity）同为 **$100\%$**！但连续测量两次时的同值概率 $P(m_1 = m_2) = \sum_{m=0}^1 \|O_m^2|\psi\rangle\|^2$ 彻底分道扬镳（因 $L_1^2 = 0$）：
       - 输入 $|0\rangle$：仪器 A 为 $1$，仪器 B 也为 $1$（单测 $|0\rangle$ 甚至抓不出差异！）；
       - 输入 $|1\rangle$：仪器 A 为 $1$，仪器 B 骤降为 **$0$**；
       - 输入 $|+\rangle$：仪器 A 为 $1$，仪器 B 仅为 **$1/2$**。
     - **反例二（旁观串扰掩盖在单比特判决指标之外）**：设单比特读出错误仅 $0.5\%$（判决保真度 $99.5\%$），但中途读出脉冲会让周围 $8$ 颗未测量的旁观数据比特各受 $0.15\%$ 额外错误。在独立错误近似下，至少一颗旁观比特出错的概率高达：

       $$
       P_{\mathrm{spectator}} = 1 - (1 - 0.0015)^8 \approx 1 - 0.98806 = 0.01194 \approx 1.19\%,
       $$

       已是被测比特自身 $0.5\%$ 判决错误的两倍多！此外，强读出脉冲还会诱导高能级泄漏（离开 $\{|0\rangle,|1\rangle\}$ 计算子空间）并引入谐振腔清空死时间与闭环反馈时延，这些在电路末尾的终止读出测试里全部被掩盖了。
   - **结论与边界回验**：读出判决保真度只刻画经典标签正确率，看不见测后态是否保持本征态（QND 性）、是否发生测量诱导泄漏、对旁观数据比特的串扰以及反馈时延与死时间；中途测量验收必须覆盖正交基与叠加态输入，全面标定上述六类量子仪器指标。
   - **易错坑提醒**：拿芯片手册里标注的“终止读出保真度 $99.5\%$”甚至只拿 $|0\rangle$ 复测两次得出的“重复性 $99\%$”，就推定该读出链可以直接胜任表面码中途纠错症状提取。

2. **【基础】被动等待、条件反馈和耗散工程复位分别把成本转移到了哪里**

   - **题意与约定**：复位（将比特从未知状态高保真拉回 $|0\rangle$）在物理上对应把熵排到外部环境，不存在“零耗时、零硬件、零串扰”的免费方案。逐一拆解三种主流复位机制的时间、误差、控制链路与热预算去向，明确跨方案比较必须采用的统一多维指标。
   - **核心提示**：围绕“把系统熵排往环境必须付出的代价”，分别从等待时间与相干损耗（被动等待）、中途测量+低时延控制链路（条件反馈）和辅助谐振腔/微波泵浦串扰（耗散工程复位）三处定位成本。
   - **完整分步演算**：
     - **1. 被动等待（热弛豫复位）**：
       - **省下了什么**：不需要额外读出脉冲、经典判决逻辑与条件门；
       - **成本落在哪里**：① **时间吞吐成本**——必须静等数倍能量弛豫时间 $T_1$（例如等 $5T_1$ 才把初始 $|1\rangle$ 衰减至 $e^{-5} \approx 0.67\%$，对 $T_1 = 100\text{–}300\ \mu\mathrm{s}$ 的超导比特或秒级离子阱而言，极大拉低循环速率）；② **热稳态残余激发底限**——在有限有效温度 $T_{\mathrm{eff}}$ 下，热平衡激发概率 $p_1 = (1 + e^{\hbar\omega_{01}/(k_B T_{\mathrm{eff}})})^{-1}$ 构成不可通过“等更久”消除的底限。
     - **2. 条件反馈（中途测量 + 实时条件 $X$ 脉冲）**：
       - **省下了什么**：把复位时长从数个 $T_1$ 压缩至微秒级，可打破热稳态底限；
       - **成本落在哪里**：① **六项实时闭环链路开销**（测量积分、分类、传输、经典判定、指令下发、条件脉冲）；② **读出与门复合误差**（判决判错就会把本该是 $|0\rangle$ 的翻成 $|1\rangle$，或漏翻 $|1\rangle$）；③ **旁观串扰与能级泄漏**（高能级 $|2\rangle$ 若无法被二分类识别，普通条件 $X_{01}$ 脉冲根本无法将其拉回 $|0\rangle$）。
     - **3. 耗散工程复位（辅助模抽运 / 参数耦合排熵）**：
       - **省下了什么**：无需经典实时反馈闭环即可自主快速排熵，且可扩展清理 $|2\rangle$ 泄漏；
       - **成本落在哪里**：① **硬件与封装复杂度**（额外辅助谐振腔/耦合器、微波泵浦线或光学通道）；② **低温热预算**（连续或脉冲泵浦功率经低温衰减器产生额外焦耳热）；③ **频谱与相干副作用**（泵浦诱导 AC Stark 频移、邻近比特串扰以及关断不彻底时的残余 Purcell 衰减）。
   - **结论与边界回验**：被动等待把成本付在漫长的 $T_1$ 等待时间与热稳态残余激发上；条件反馈把成本付在实时读出/分类/传输/条件脉冲链路误差与旁观串扰上；耗散工程把成本付在辅助谐振模、泵浦硬件、热预算与频谱串扰上。比较三种方案必须并排报告复位残差（含对 $|1\rangle, |2\rangle$ 的最坏输入）、总耗时、并行度与旁观影响。
   - **易错坑提醒**：只比单一的“平均复位保真度”，忽略了平均态往往掩盖“初态处于 $|1\rangle$ 或泄漏态 $|2\rangle$ 时复位变差”以及对邻近数据比特的附带损伤。

3. **【计算】把控制电子学从室温移到 $4\ \mathrm{K}$ 或 $100\ \mathrm{mK}$ 会同时改善和恶化什么**

   - **题意与约定**：先列明把控制电子学下沉低温级带来的信号/互连红利与热学/工程代价，再锚定稀释制冷机五温区跨越 $6$ 个数量级的冷量瀑布，用热预算方程 $P_s = P_{\mathrm{static}} + P_{\mathrm{switched}} + P_{\mathrm{analog}} + P_{\mathrm{IO}} + P_{\mathrm{wire}} < P_{\mathrm{cool}}(T_s)$ 零跳步复算正文 4.1 节 $100\ \mathrm{mK}$ 固定基荷挤压算例，并点明硅自旋“热比特”温区红利。
   - **核心提示**：先对照电子学下沉低温级带来的走线减短/热漏减少红利与冷量瀑布制约，再把五温区冷量预算代入热平衡方程 $P_s=P_{\mathrm{static}}+P_{\mathrm{dyn}}$，核算在 $100\,\mathrm{mK}$ 与 $4\,\mathrm{K}$ 级分别能容纳多少控制功耗。
   - **完整分步演算**：
     - **同时改善的工程项**：大幅缩减穿越多级法兰的室温同轴线缆数量（打破空间与热传导墙）、缩短控制与反馈信号传播时延、提升近端 I/O 引脚密度与复用能力、降低高频长同轴线插损与串扰；
     - **同时恶化的工程项**：冷级可用制冷功率暴跌引发的严格功耗天花板、近端芯片局部发热抬升样品真实电子温度（冷台温度计读数不等同于电子温度）、低温晶体管器件特性漂移与开关数字噪声耦合、以及封入冷机后极高的封装调试与返修难度。
     - **冷量瀑布与 $100\ \mathrm{mK}$ 热预算零跳步算例**：商用稀释制冷机的局部制冷量从 $50\ \mathrm{K}$ 板的 $\sim 30\ \mathrm{W}$、$4\ \mathrm{K}$ 板的 $\sim 1.5\ \mathrm{W}$（单脉管，多脉管数瓦），断崖式跌落到蒸馏室的数十毫瓦、$100\ \mathrm{mK}$ 冷板的数百微瓦至毫瓦级，直至 $20\ \mathrm{mK}$ 混合室仅剩约 **$19\ \mu\mathrm{W}$**（跨 $6$ 个数量级！且各级 $20\ \mathrm{dB}$ 微波衰减器把 $99\%$ 输入射频功率转化为当地焦耳热）。在 $100\ \mathrm{mK}$ 分配总热预算 $P_{\mathrm{budget}} = 600\ \mu\mathrm{W}$、线缆与 I/O 固定占 $120\ \mu\mathrm{W}$ 的算例中：
       - **原方案**（静态基荷 $P_{\mathrm{static}} = 80\ \mu\mathrm{W}$，每活跃通道 $p_{\mathrm{ch}} = 0.4\ \mu\mathrm{W}$）：

         $$
         N_{\mathrm{active}} \le \frac{600 - 80 - 120}{0.4} = \frac{400}{0.4} = 1{,}000\text{ 条（严格不等式最多 }999\text{ 条）}.
         $$

       - **改版方案**（单通道砍半至 $0.2\ \mu\mathrm{W}$，但静态基荷翻倍至 $160\ \mu\mathrm{W}$）：

         $$
         N'_{\mathrm{active}} \le \frac{600 - 160 - 120}{0.2} = \frac{320}{0.2} = 1{,}600\text{ 条}.
         $$

       单通道功耗降一半，总通道上限仅涨了 $60\%$ 而非 $100\%$——这就是**固定静态基荷的非线性挤压效应**！与此同时，半导体硅/锗自旋比特可在 $100\text{–}150\ \mathrm{mK}$（如 HRL 2026 芯片）乃至 $>1\ \mathrm{K}$ 运行，将可用冷量较 $20\ \mathrm{mK}$ 抬升 $1\text{–}3$ 个数量级，是评估 $4\ \mathrm{K}$ / mK Cryo-CMOS 集成的重要支点。
   - **结论与边界回验**：下沉至 $4\ \mathrm{K}$ 或 $100\ \mathrm{mK}$ 改善了布线密度、线缆热导与反馈时延，但恶化了冷级热预算约束、局部发热、数字开关噪声与可维修性；最佳温区分区必须依据实测制冷曲线并按五项总热负载公式逐级核算，没有放之四海而皆准的单一放置层。
   - **易错坑提醒**：一是把芯片单通道活动功耗（如 $\mathrm{nW/MHz}$）乘以通道数当整片总功耗，漏算了高昂的固定静态基荷 $P_{\mathrm{static}}$ 与线缆/衰减器焦耳热；二是把整机室温墙插功耗（数十千瓦）与混合室局部冷量（约 $19\ \mu\mathrm{W}$）混为一谈。

4. **【计算】为什么四个选定器件都达到高保真度，不能推出整片晶圆的功能良率**

   - **题意与约定**：从“抽样选择偏差（非随机样本）”、“五层良率分母定义混淆”以及“小样本精确统计下界”三层递进剖析，并零跳步手算双侧 $95\%$ Clopper–Pearson 精确下限 $p_{\mathrm{low}} = (0.025)^{1/4} \approx 39.8\%$ 与反推 $99\%$ 良率认证所需零失败样本量 $n = 368$（对照第 15 章单侧三倍法则 $n = 299$）。
   - **核心提示**：先指出人工挑出 4 个好器件的选择偏倚与“物理制备—频率命中—封装—低温存活—门达标”五层良率分母，再用 Clopper–Pearson 下限公式 $p_{\mathrm{low}}=(\alpha/2)^{1/n}$ 手算 $n=4$ 全通过时的 $95\%$ 置信下界。
   - **完整分步演算**：
     - **第一层（非随机抽样偏差）**：送入稀释制冷机做精细门标定的 $4$ 颗器件，往往已在室温探针台上经电阻、漏电、连通性或低温谐振预筛挑出。一旦样本经过预筛选，就不满足独立随机抽样前提，统计学上根本不能反推整片晶圆良率。
     - **第二层（偷换五层良率分母）**：制造良率须按工艺良率、电学良率、可调谐良率、全门集良率与服务良率逐级记账。“被测 $4$ 颗器件单/双比特门保真度 $>99\%$”衡量的是**已通过前序筛选器件的门质量**，其分母漏掉了晶圆上未成点、漏电、频率碰撞、受 TLS 缺陷瘫痪以及热循环后脱焊失效的全部裸片。
     - **第三层（小样本统计鸿沟零跳步手算）**：即便退一步假定这 $4$ 颗确系整片晶圆上独立随机抽取且 $4/4$ 零失败通过，在**双侧 $95\%$ Clopper–Pearson 精确置信区间**下（单尾概率 $\alpha/2 = 0.025$），真实良率下限 $p_{\mathrm{low}}$ 满足方程 $p_{\mathrm{low}}^4 = 0.025$，解得：

       $$
       p_{\mathrm{low}} = (0.025)^{1/4} = \exp\!\left(\frac{\ln 0.025}{4}\right) \approx \exp\!\left(\frac{-3.688879}{4}\right) \approx 0.397635 \approx 39.8\%.
       $$

       也就是说，$4/4$ 全通过与“真实良率只有约 $40\%$”在统计上完全相容！反过来算，若想在零失败的理想情况下把双侧 $95\%$ 下限推上 $99\%$（即 $(0.025)^{1/n} \ge 0.99$），两边取自然对数（注意 $\ln 0.99 \approx -0.0100503 < 0$，同除负数不等号反向）：

       $$
       n \ge \frac{\ln 0.025}{\ln 0.99} \approx \frac{-3.688879}{-0.0100503} \approx 367.04
       \implies
       n = 368\text{ 颗独立随机器件全部零失败}.
       $$

       （口径对照：若采用第 15 章第 3.2 节的**单侧 $95\%$** 三倍法则口径，单尾 $\alpha = 0.05$，则需 $n \ge \lceil\ln 0.05/\ln 0.99\rceil = \lceil 298.07\rceil = 299$ 颗，依然远超 $4$ 颗；且真实晶圆上相邻裸片存在空间工艺关联，实际认证样本量只会更大。）
   - **结论与边界回验**：四个选定器件存在预筛选择偏差且分母仅反映通过器件的门质量；即使按独立随机样本算，$4/4$ 全通过对应的双侧 $95\%$ Clopper–Pearson 下限也仅约 $39.8\%$（认证 $99\%$ 下限至少需 $368$ 颗零失败，单侧 $95\%$ 亦需 $299$ 颗），远远不足以推出整片晶圆功能良率。
   - **易错坑提醒**：把“冠军器件的门保真度 $99\%$”和“晶圆功能良率 $99\%$”混为一谈，或看到 $4/4 = 100\%$ 的点估计就忘记对小分母计算精确置信下界。

5. **【基础】自动找到一次好参数，为何不等于已经实现无人值守校准**

   - **题意与约定**：区分“一次性自动寻优”、“长期自动维持工作点”与“自动故障诊断及安全变更治理”三级工程成熟度；结合正文 6.2 节的 5 节点校准依赖图（DAG）演练参数变更的拓扑传播、整批回归拦截与乐观锁原子晋级机制。
   - **核心提示**：按“单次自动寻优 → 漂移监测与依赖图（DAG）增量重校准 → 回归门禁与自动回滚治理”三级工程成熟度，说明为何找到一次好参数只是起点。
   - **完整分步演算**：
     - **一次性寻优的局限**：真实处理器存在慢温漂、磁场漂移、两能级系统（TLS）随机频跳、部件老化以及并行串扰变化；且底层的物理校准参数彼此强耦合（上游频率动一点，下游读出阈值、单门幅度与双比特门相位全部失效）。跑通一次贝叶斯优化或自动扫描，只证明在那一刻找到了一个候选工作点，丝毫不具备长时稳定运维能力。
     - **无人值守校准的完整工程闭环（正文 5 节点 DAG 演练）**：设生产活动参数快照为版本 $7$，依赖图满足 $f_0 \to (a_0, m_0) \to g_{01} \to v_{01}$（$f_0$ 为比特 $0$ 频率，$a_0$ 为单门幅度，$m_0$ 为读出分类器，$g_{01}$ 为双比特门，$v_{01}$ 为并行门层回归；比特 $2$ 的 $a_2, m_2$ 在图中独立）。一旦监测到 $f_0$ 漂移并重标，无人值守系统必须严格执行四步治理：
       1. **按依赖闭包拓扑重验**：沿 $f_0 \to (a_0, m_0) \to g_{01} \to v_{01}$ 依次重标与验证受影响的全部下游节点（若真实硬件与比特 $2$ 有串扰，还必须把隐性边补进 DAG）；
       2. **部分通过必须整批拦截**：哪怕前四项全部达标、仅最后并行门层回归 $v_{01}$ 失败，也必须完整留存失败证据并维持原版本 $7$，严禁将前四项“半新半旧”拼上生产环境；
       3. **乐观锁原子晋级**：只有全闭包回归通过且提交瞬间核实线上仍为版本 $7$，才一次性原子切换至完整快照版本 $8$（若期间其他校准任务已升至版本 $8$，则拒绝本次基于旧基线的过期提交）；
       4. **异常降级而非盲目回滚**：配置回滚只能撤销软件参数，无法逆转芯片物理漂移——若旧快照 $7$ 在当前物理状态下也已失效，系统必须自动切入降级或维护队列，绝不继续伪称合格。
   - **结论与边界回验**：自动找到一次好参数只是起点；无人值守校准必须具备持续监测、漂移/故障分类、沿依赖图（DAG）做最小闭包重标、整批回归测试、乐观锁原子晋级或回滚以及全流程数据与版本追溯能力。
   - **易错坑提醒**：把“写了一个自动调参脚本”等同于“建好了生产级自动校准系统”，忽略了参数耦合回退、并发覆盖竞争以及“软件回滚无法消除物理漂移”三条运维底线。

6. **【基础】经典线路切割与先兆式量子链路的资源记账有何根本差异**

   - **题意与约定**：从物理过程（是否真正跨模块传输量子态与建立相干纠缠）切入，对比经典线路切割（circuit cutting，含 LO 与 LOCC）与先兆式光学量子链路（heralded photonic link）的数学标度、核心硬件开销及 2024–2025 实测里程碑，明晰两套完全不可混算的资源账本。
   - **核心提示**：从是否建立真实物理跨模块纠缠切入：对比线路切割（纯经典抽样重构，代价为随切割数指数增长的 $\gamma^{2k}$ 采样倍率）与先兆量子链路（真实物理纠缠分发，代价为光损重试、存储相干与光速经典延迟）。
   - **完整分步演算**：
     - **经典线路切割（LO / LOCC 准概率分解 QPD）**：
       - **物理本质**：芯片间**不传输任何量子态**，也未建立可存储的跨芯片物理纠缠对。编译器把跨分区导线或双比特门展开为局域测量与重制备信道的带符号线性组合 $\mathcal{U} = \sum_i c_i \mathcal{F}_i$（$\gamma = \sum_i |c_i| \ge 1$），各芯片独立执行局域子线路后在经典计算机上按带符号权重保序重构联合期望值；
       - **资源记账核心**：核心代价是随切口数 $K$ **指数增长的采样开销 $O(\gamma^{2K})$**（例如单 $\mathrm{CNOT}$ 切割 $\gamma = 3$，独立切 $K$ 门采样方差放大 $9^K$ 倍；即便引入跨芯片实时经典通信 LOCC——如 IBM 2024 年 142 比特等效演示——把 $K$ 条并行门底数压至 $(2^{K+1}-1)^2 = O(4^K)$，依然是指数标度），外加准概率保序经典后处理与实时经典延迟。它本质上是**用指数级经典采样时间换取单芯片宽度**。
     - **先兆式量子链路（物理 Bell 对 + 门隐形传态）**：
       - **物理本质**：通过光学干涉与光子探测（先兆信号）在两块物理芯片间概率性地**真实生成跨模块物理 Bell 纠缠对**，确认先兆成功后，再用局域门、经典通信与门隐形传态执行真正的相干远程双比特门（如牛津大学 2025 年在两套独立离子阱间实现约 $86\%$ 平均保真度的远程 CZ 门隐形传态）；
       - **资源记账核心**：核心代价是**纠缠生成速率（Hz/kHz 级）**、纠缠等待期间量子存储器的退相干、跨模块接口链路保真度、纠缠纯化（蒸馏）消耗、先兆失败重试以及前馈延迟。它提供的是**真正可扩展的相干联合量子寄存器**，但远程门开销远高于片内本地门。
   - **结论与边界回验**：线路切割不建立物理跨芯片纠缠，其账本核心是随切口数按 $O(\gamma^{2K})$ 指数暴涨的采样方差与经典重构开销；先兆式量子链路真实建立跨模块物理纠缠对并实现相干远程门，其账本核心是纠缠生成率、存储退相干、链路保真度、纯化与重试开销。前者不可伪装成联合相干寄存器，后者也不可把远程门按本地门成本混计。
   - **易错坑提醒**：看到线路切割重构出 $142$ 比特期望值就以为两块芯片之间已经建成了相干量子互联，或者把先兆式链路中低速、高误差的跨模块远程门和片内高速本地门不加区分地合并统计。

7. **【进阶】20 任务实时解码 FIFO 队列：为何平均服务 $<1\ \mu\mathrm{s}$ 仍有一半任务错过 $2\ \mu\mathrm{s}$ 截止线？写出递推式并分析增配第二台解码器的边界**

   - **题意与约定**：考察正文 8.3 节的单服务台先到先服务（FIFO）实时解码队列模型：$20$ 个连续纠错任务（编号 $n = 0, 1, \dots, 19$）以恒定间隔每 $1\ \mu\mathrm{s}$ 到达一次（到达时刻 $a_n = n\ \mu\mathrm{s}$），反馈硬截止时间为响应时延 $\ell_n \le 2.0\ \mu\mathrm{s}$。其中 $19$ 个普通任务的服务时长仅 $s_n = 0.8\ \mu\mathrm{s}$，唯独编号 $n = 2$ 遭遇复杂关联错误簇导致 $s_2 = 4.0\ \mu\mathrm{s}$。先核算平均服务时长 $\bar{s}$，再写出单服务台 FIFO 递推公式并逐项算出所有受波及任务，最后定量分析增加第二台同速并行解码器的作用与物理上限。
   - **核心提示**：写出单服务台 FIFO 队列的 Lindley 递推式 $W_n=\max(0,W_{n-1}+S_{n-1}-a)$ 与响应时间 $R_n=W_n+S_n$，代入前几项突发长服务任务看积压如何向后连锁传播；再讨论增配第二台解码器能否消除串行逻辑依赖。
   - **完整分步演算**：
     - **第一步：计算平均服务时长 $\bar{s}$**：

       $$
       \bar{s} = \frac{19 \times 0.8 + 1 \times 4.0}{20} = \frac{15.2 + 4.0}{20} = \frac{19.2}{20} = 0.96\ \mu\mathrm{s} < 1.0\ \mu\mathrm{s}.
       $$

       从长期平均吞吐看，平均服务速度确实快于每 $1.0\ \mu\mathrm{s}$ 一个任务的到达速率（负载比 $0.96 < 1$）。
     - **第二步：写出单服务台 FIFO 排队递推公式**。令第 $n$ 个任务的开始服务时刻为 $b_n$、完成时刻为 $f_n$（初始约定 $f_{-1} = 0$）、排队等待时长为 $w_n$、端到端响应时延为 $\ell_n$，则：

       $$
       b_n = \max(a_n,\, f_{n-1}),
       \qquad
       f_n = b_n + s_n,
       \qquad
       w_n = b_n - a_n,
       \qquad
       \ell_n = f_n - a_n = w_n + s_n.
       $$

     - **第三步：逐项递推计算关键任务响应时延（精确有理数核验）**：
       - $n = 0$：$a_0 = 0.0,\; b_0 = 0.0,\; f_0 = 0.8,\; w_0 = 0.0,\; \ell_0 = 0.8\ \mu\mathrm{s}$（满足）；
       - $n = 1$：$a_1 = 1.0,\; b_1 = \max(1.0, 0.8) = 1.0,\; f_1 = 1.8,\; w_1 = 0.0,\; \ell_1 = 0.8\ \mu\mathrm{s}$（满足）；
       - **$n = 2$（突发长尾任务）**：$a_2 = 2.0,\; b_2 = \max(2.0, 1.8) = 2.0,\; f_2 = 2.0 + 4.0 = 6.0,\; w_2 = 0.0,\; \ell_2 = \mathbf{4.0\ \mu\mathrm{s}}$（**错过**）；
       - **$n = 3$**：$a_3 = 3.0,\; b_3 = \max(3.0, 6.0) = 6.0,\; f_3 = 6.8,\; w_3 = 3.0,\; \ell_3 = 6.8 - 3.0 = \mathbf{3.8\ \mu\mathrm{s}}$（**错过**）；
       - **积压缓慢消化规律（$n = 3, 4, \dots, 12$）**：此后每个普通任务在 $1.0\ \mu\mathrm{s}$ 的到达间隔内仅消耗 $0.8\ \mu\mathrm{s}$ 服务时间，因此每推进一个任务，排队等待与响应时延只能消化 $1.0 - 0.8 = 0.2\ \mu\mathrm{s}$！由线性递推得 $\ell_n = 3.8 - 0.2(n - 3) = 4.4 - 0.2n\ \mu\mathrm{s}$：
         - $n = 4\text{–}10$：响应时延依次为 $3.6,\ 3.4,\ 3.2,\ 3.0,\ 2.8,\ 2.6,\ 2.4\ \mu\mathrm{s}$（全部**错过**）；
         - **$n = 11$**：$b_{11} = 12.4,\; f_{11} = 13.2,\; w_{11} = 1.4,\; \ell_{11} = \mathbf{2.2\ \mu\mathrm{s}}$（**错过**）；
         - **$n = 12$**：$b_{12} = 13.2,\; f_{12} = 14.0,\; w_{12} = 1.2,\; \ell_{12} = \mathbf{2.0\ \mu\mathrm{s}}$（**恰好恢复满足**）；
         - $n = 13\text{–}18$：响应依次降至 $1.8,\ 1.6,\ 1.4,\ 1.2,\ 1.0,\ 0.8\ \mu\mathrm{s}$（到 $n = 18$ 排队彻底清空，$w_{18} = 0$）；$n = 19$ 为 $0.8\ \mu\mathrm{s}$。

       统计全部 $20$ 个任务：**编号 $n = 2, 3, \dots, 11$ 共 $10$ 项（整整 $50\%$）错过 $2.0\ \mu\mathrm{s}$ 截止时间**，最大响应达到 $4.0\ \mu\mathrm{s}$！
     - **第四步：增配第二台同速并行解码器能解决什么、不能解决什么**。
       - **能解决的（排队连坐积压）**：当 $n = 2$ 在第 $1$ 台服务台运行至 $t = 6.0\ \mu\mathrm{s}$ 时，$n = 3$ 于 $t = 3.0\ \mu\mathrm{s}$ 到达并立刻进入空闲的第 $2$ 台解码器，在 $[3.0, 3.8]$ 完成（$\ell_3 = 0.8\ \mu\mathrm{s}$）；随后 $n = 4\text{–}19$ 全部实现零排队、响应均为 $0.8\ \mu\mathrm{s}$，原本被牵连超时的 **$9$ 个任务（$n = 3\text{–}11$）全部获救**，总超时数从 $10$ 降至 $1$；
       - **不能解决的（单任务自身服务时长下界）**：第 $2$ 号任务本身需要 $s_2 = 4.0\ \mu\mathrm{s}$ 的串行解码计算，加再多同速并行服务台也无法把它拆成两半压进 $2.0\ \mu\mathrm{s}$ 内，它仍会以 $\ell_2 = 4.0\ \mu\mathrm{s}$ 违约。要压低单任务自身最坏耗时，必须靠算法加速、专用硬件（如 ASIC/FPGA）、投机预计算，或修改容错协议放宽单次等待窗。
   - **结论与边界回验**：尽管 $\bar{s} = 0.96\ \mu\mathrm{s} < 1\ \mu\mathrm{s}$，但 $n = 2$ 的 $4.0\ \mu\mathrm{s}$ 长尾突发制造了 $3.0\ \mu\mathrm{s}$ 排队积压，每个后续普通任务只能消化 $0.2\ \mu\mathrm{s}$，导致 $n = 2\text{–}11$ 共 $10$ 项（$50\%$）错过 $2.0\ \mu\mathrm{s}$ 截止线；递推式为 $b_n = \max(a_n, f_{n-1}),\; f_n = b_n + s_n,\; w_n = b_n - a_n,\; \ell_n = f_n - a_n$；增配第二台并行解码器能彻底消除后续 $9$ 项排队连坐超时，但无法缩减 $n = 2$ 自身的 $4.0\ \mu\mathrm{s}$ 单任务最坏时延。
   - **易错坑提醒**：一是误用长期平均服务时间 $<1\ \mu\mathrm{s}$ 担保逐轮硬实时截止时间；二是以为“加机器并行”就能把单个长尾任务的端到端反应时间也成比例砍半（并行提高吞吐、消除排队，不直接降低单个不可拆任务的延迟下界）。

8. **【基础】GKP 码的“一个振荡器编码一个逻辑量子比特”为何不表示零辅助资源**

   - **题意与约定**：区分“编码逻辑比特所占据的希尔伯特空间模式数（单个谐振子）”与“物理制备、纠错症状提取、主动稳定及容错逻辑门所需的整机硬件资源”。衔接第 18 章 GKP 相空间 $4\pi$ 晶胞与有限能量包络，以及第 19 章 2023–2025 超导腔与离子阱 GKP 实验口径，全面列出背后的隐藏辅助开销。
   - **核心提示**：把“逻辑编码占据几个谐振子模式”与“整机物理硬件账单”分开算：清点制备 GKP 栅格态、周期性纠错症状提取与稳定化所需的辅助跨导/非线性比特、微波控制通道与读出链路。
   - **完整分步演算**：
     - **理想态与有限能量近似的物理鸿沟**：如第 18 章第 9.5 节所示，方形 GKP 码用步长 $2\sqrt{\pi}$ 的位移稳定子 $S_q = e^{i2\sqrt{\pi}\hat{q}}, S_p = e^{-i2\sqrt{\pi}\hat{p}}$ 围出面积 $4\pi$ 的相空间晶胞以编码 $d = 2$ 逻辑量子比特，但理想狄拉克梳码字 $|0_L\rangle, |1_L\rangle$ 需要无限压缩与无穷大平均光子数。真实实验室只能制备施加了阻尼包络 $\hat{E}_\Delta = e^{-\Delta^2\hat{a}^\dagger\hat{a}}$ 的有限能量近似态，且必须持续施加有限能量稳态反馈或耗散修整，防止峰宽在损耗下扩散越过 Voronoi 边界 $\pm\sqrt{\pi}/2$；
     - **完整运行链依赖五大辅助资源**：① **非线性辅助二能级系统**（超导腔需耦合高质量 transmon 辅助比特，离子阱声子模需耦合内部电子自旋态，以提供产生 Wigner 负性、纠错症状提取与读出所需的非高斯非线性）；② **高速实时经典反馈电子学**（例如 Yale 2023/2025 超导 GKP 实验依赖强化学习优化的实时 FPGA 反馈闭环才实现存储超越盈亏平衡，qutrit $G_3 = 1.82\pm 0.03$、ququart $G_4 = 1.87\pm 0.03$）；③ **精密微波/激光泵浦与复杂多音脉冲控制**；④ **低保真度双模逻辑门与外层级联码开销**（例如悉尼大学 2025 离子阱 GKP 虽演示通用逻辑门集，但双比特逻辑纠缠门过程保真度仅约 $0.68$，要迈向大规模实用容错仍需在外层级联表面码或 qLDPC 码）。
   - **结论与边界回验**：“一个振荡器编码一个逻辑比特”仅描述逻辑码字栖身的希尔伯特空间模式数，并不等于零辅助硬件；有限能量制备、纠错症状提取、实时反馈稳态、非高斯辅助比特、泵浦控制以及外层级联容错全部需要可观的物理与经典资源。
   - **易错坑提醒**：把玻色编码“硬件高效”误解成“只要放一个微波腔就能免去全部辅助比特、实时反馈和外层纠错码”，忽略了辅助 transmon 自身退相干往往正是当前 GKP 纠错周期的瓶颈之一。

9. **【计算】即时擦除与延迟擦除对在线解码的价值为何不同**

   - **题意与约定**：先用纠错码距 $d$ 的数学公式定量对比“未知位置 Pauli 错误”与“已知位置擦除错误”的纠错能力倍增效应（以 $d = 5$ 为例），再区分擦除标记暴露的时间点（纠错轮次进行中 vs 线路末尾终态测量）如何决定实时解码器与控制器能否采取在线补救措施，并强调擦除探测器自身的性能口径。
   - **核心提示**：先由 $2t+e<d$ 量化码距 $d=5$ 下擦除纠错能力是未知错误的两倍，再区分“当轮即时获知擦除位置（直接进最小权匹配降权）”与“事后延迟发现（错过在线反馈窗口或引发多轮传播）”的解码价值差。
   - **完整分步演算**：
     - **位置信息的数学倍增红利**：对码距为 $d$ 的量子纠错码，若错误位置未知，解码器必须同时定位并纠正错误，至多保证纠正 $\left\lfloor\frac{d-1}{2}\right\rfloor$ 个错误；一旦硬件在纠错轮次中直接标出出错位置（即转化为**擦除错误**），解码器只需在该已知位置上恢复状态，保证纠正上限直接翻倍至 $d - 1$ 个。以 $d = 5$ 为例：

       $$
       t_{\mathrm{unknown}} = \left\lfloor\frac{5 - 1}{2}\right\rfloor = 2,
       \qquad
       t_{\mathrm{erasure}} = 5 - 1 = 4.
       $$

     - **即时擦除（heralded / mid-circuit erasure）的在线价值**：在错误发生的当轮纠错周期内实时上报受损物理比特的精确位置与时间戳。实时解码器与控制器可立即采取四项在线动作：① 在解码校验图中将该位置的边权重设为高先验错误率（最大化利用 $d-1$ 纠错界）；② 对丢失或泄漏比特周围的稳定子校验相乘构造**合并校验**（supercheck）维持校验完整性；③ 动态调整物理路由绕开受损比特；④ 触发粒子重装、主动复位或泄漏消除单元（LRU）及时止损，防止泄漏跨轮扩散污染邻居。
     - **延迟擦除（delayed erasure）的局限**：仅在整段电路结束后的终态读出中才发现某颗比特处于泄漏态或原子已经丢失。这些事后信息虽然可用于**离线重解码**提升存储基准的统计后验精度，但早已错过中间各轮条件反馈、动态路由与非 Clifford 逻辑门实时分支的窗口，对在线容错计算无能为力。
     - **工程报告底线**：擦除探测器自身存在误报与漏报（如真阳性 $98\%$ 仍有 $2\%$ 漏检溜进更贵的未知错误预算，假阳性 $0.2\%$ 会白占码距额度），因此无论即时还是延迟擦除，都必须同时报告真阳性率、假阳性率与时间分辨率。
   - **结论与边界回验**：即时擦除在纠错当轮提供精确时空位置，允许在线解码器动态改写校验图、构造合并校验、路由绕行或即时重置，充分兑现 $d-1$ 翻倍纠错红利；延迟擦除只在末尾暴露，只能辅助离线重解码与事后分析，无法服务在线实时控制与逻辑反馈。
   - **易错坑提醒**：只要论文提到硬件具备“擦除检测能力”，就默认全过程享受 $d-1$ 翻倍阈值，却未核查它是轮中即时擦除还是末尾延迟擦除，也未核查探测真阳性率与探测动作本身引入的旁观串扰。

10. **【基础】qLDPC 的高编码率为何不自动等于更低的整机开销**

    - **题意与约定**：先澄清 qLDPC（量子低密度奇偶校验码）中“低密度”的真实含义（校验权重为常数，而非物理连线局域），再从芯片连接拓扑、并行校验电路与串扰、实时解码功耗与尾延迟、逻辑门编址与魔法态供给四个系统工程层面拆解“低物理/逻辑比特比 $\ne$ 低整机成本”。
    - **核心提示**：先澄清 qLDPC 的“低密度”指校验权重有界而非二维平面局域，再从长程非局域连线/跨层布线、并行校验串扰、复杂解码器延迟与逻辑寻址/魔术态接口四个整机维度评估总开销。
    - **完整分步演算**：
      - **高编码率只省了“静态存储比特数”这一项**：旋转表面码每 $2d^2 - 1$ 颗物理比特仅编码 $1$ 个逻辑比特（渐近编码率 $k/n \to 0$），而 qLDPC 码（如双变量自行车 Gross 码 $[[144, 12, 12]]$ 或常数码率族）把物理/逻辑比特比压缩了数倍乃至一个数量级。但这仅仅衡量了量子存储块本身的比特数量；
      - **四笔容易抵消比特红利的整机工程账**：
        1. **非局域连接与三维封装代价**：qLDPC 的“低密度”仅指每个校验作用于常数个比特，但拓扑定理（Bravyi–Poulin–Terhal 界）决定了高码率高码距 qLDPC 在纯二维平面上**必然需要长程非局域连线**。为此超导平台需更复杂的多层跨线、三维硅通孔或微波谐振腔耦合，中性原子/离子阱则需付出频繁的大范围粒子搬运时间与加热误差；
        2. **校验电路深度、并行度与物理阈值折损**：高权重校验（如权重 $6\text{–}12$ 对表面码权重 $4$）往往拉长每轮纠错症状提取电路深度，增大钩形错误（hook error）与空闲退相干风险；
        3. **复杂实时解码硬件开销**：与二维表面码高度规则的平面网格相比，qLDPC 的超图校验结构不能直接用最简平面 MWPM，常需信念传播加有序统计解码（BP+OSD）或专用迭代 FPGA/ASIC（如 IBM Relay-BP，单次迭代 $24\ \mathrm{ns}$），其尾延迟、面积与功耗必须满足每轮硬截止要求；
        4. **逻辑门编译与可寻址操作成本**：qLDPC 把多个逻辑比特共同压缩在同一个码块里，没有表面码那样独立排布的补丁边界；要在不破坏码距前提下单独对其中一两个逻辑比特做定向 Pauli 乘积测量（PPM）与非 Clifford 逻辑门，常需额外开辟辅助“缓冲/手术”区与昂贵的路由桥接。
    - **结论与边界回验**：qLDPC 的高编码率仅减少静态逻辑存储所需的物理比特比例，并不自动降低整机开销；长程互连封装、校验提取深度、复杂实时解码硬件以及块内逻辑门寻址与魔法态工厂开销都可能抵消比特节省，必须基于相同物理噪声、连接约束与端到端逻辑算法负载做整机对比。
    - **易错坑提醒**：直接拿“qLDPC 比表面码省 $10\times$ 物理比特”的静态存储比值，等同于“造一台通用容错计算机总造价、总功耗与运行时间也便宜 $10\times$”。

11. **【基础】ISO/IEC 4879:2024 已发布，为何仍不能说量子计算性能已有统一国际认证**

    - **题意与约定**：依据正文第 10.1 节的五级标准文档成熟度模型，精确核对 ISO/IEC 4879:2024 的正式适用范围（词汇表），并与正在起草的工作项目（如 IEEE P7130 / P7131）、信息性 RFC、行业开源规范以及第三方产品合格评定体系清晰切割。
    - **核心提示**：对照标准文档成熟度阶梯，明确 ISO/IEC 4879:2024 是一份“通用词汇表标准”（统一术语定义），并非跨平台硬件性能基准测试或第三方认证规范。
    - **完整分步演算**：
      - **核查 ISO/IEC 4879:2024 的法定文本范围**：该标准全称为 *Information technology — Quantum computing — Vocabulary*（2024 年 5 月发布，现归口 ISO/IEC JTC 3），其唯一正式职责是**统一量子计算基础术语与词汇定义**，减少学术界、工业界与采购合同中的沟通歧义；它**不包含**任何量子处理器性能基准测试规程、跨云互操作接口协议、容错安全认证门槛或产品合格评定条款；
      - **区分标准生态的五个不同成熟度层级**：
        - 已发布国际标准（如 ISO/IEC 4879:2024）：只证明该特定范围的正式标准文本已出版，绝不代表涵盖性能与互操作认证；
        - 立项工作项目/草案（如 IEEE P7130 术语、IEEE P7131 性能基准框架，以及 ISO/IEC JTC 3 下的多项在研工作组）：尚处起草、投票与修订阶段，条款未定稿且无法律或认证约束力；
        - 行业联盟规范（如 OpenQASM 3、QIR）、信息性 RFC 文档与厂商专有 API：分别代表开源社区约定、参考架构或单一厂商接口，均不等同于经独立认可实验室执行的统一国际性能认证。
    - **结论与边界回验**：ISO/IEC 4879:2024 仅是统一基础概念的国际**词汇标准**，并未规定统一性能基准、云端互操作规范或产品合格认证；看到正式标准编号发布或新委员会成立，绝不能外推成量子计算性能已有统一国际认证体系。
    - **易错坑提醒**：在采购标书或行业宣传里看到“符合 ISO/IEC 4879 国际标准”就误以为设备通过了权威性能与精度认证，实际上那只说明文档采用了标准术语。

12. **【计算】峰值 $10^5\ \mathrm{shots/s}$ 的设备为何可能只有远低于该值的长期有效吞吐**

    - **题意与约定**：区分“瞬时峰值采样率”与“墙钟长期合格有效吞吐”，先用正文 11.1 节算例 1（长期独立平稳 MTBF/MTTR + 计划校准乘积模型）与算例 2（24 小时真实日志重叠停机并集积分 + 降级窗口剥离）完成两组零跳步定量核算，再列出队列空闲、失败作业、重试与误差缓解等进一步拉低有效吞吐的因素。
    - **核心提示**：先按瞬时峰值乘以可用率（MTBF/(MTBF+MTTR)、计划校准占比、后选择合格率与编译/通信开销占比）估算长期有效吞吐，再对比停机时段重叠时为何应取并集而非简单连乘。
    - **完整分步演算**：峰值 $10^5\ \mathrm{shots/s}$ 仅在芯片完全在线、校准达标、且无空闲队列与通信停顿的理想窗口内测得。摊到真实 24 小时墙钟时间上，至少会被两类截然不同的可用率模型大幅折损：
      - **算例 1（长期近似独立平稳模型）**：设非计划故障统计满足 $\mathrm{MTBF} = 18\ \mathrm{h}$、$\mathrm{MTTR} = 2\ \mathrm{h}$，则非计划故障固有可用率为：

        $$
        A_u = \frac{\mathrm{MTBF}}{\mathrm{MTBF} + \mathrm{MTTR}} = \frac{18}{18 + 2} = 0.90.
        $$

        机房每天另有 $3\ \mathrm{h}$ 计划校准，可调度时间占比为 $\frac{21}{24} = 0.875$。若非计划故障与计划校准近似独立，综合可调度在线比例与折算吞吐为：

        $$
        A_{\mathrm{sched}} = 0.90 \times 0.875 = 0.7875,
        \qquad
        R_{\mathrm{sched}} = 10^5 \times 0.7875 = 7.875 \times 10^4\ \mathrm{shots/s}.
        $$

      - **算例 2（24 小时真实日志：重叠停机并集积分与降级剔除）**：若某日实测日志记录计划校准停机 $[2, 5)$（$3\ \mathrm{h}$）、突发故障停机 $[4, 6)$（$2\ \mathrm{h}$）、降级运行 $[10, 12)$（$2\ \mathrm{h}$，虽在线且以 $4\times 10^4\ \mathrm{s}^{-1}$ 出数，但门保真度跌破质量门槛）：
        - **停机并集**：$[2,5)\cup[4,6) = [2,6)$，因存在 $1\ \mathrm{h}$ 重叠 $[4,5)$，总停机时长为 $3 + 2 - 1 = 4\ \mathrm{h}$，全天**在线时长**为 $24 - 4 = 20\ \mathrm{h}$（$20/24 \approx 83.33\%$，切不可误用独立相乘 $(21/24)(22/24) \approx 80.21\%$ 或重复扣减成 $19\ \mathrm{h}$）；
        - **合格时长与墙钟合格吞吐**：扣除 $2\ \mathrm{h}$ 不达标降级段后，全天**合格时长**仅 $20 - 2 = 18\ \mathrm{h}$（占比 $75\%$），全天合格总样本数与长期墙钟合格吞吐分别为：

          $$
          N_{\mathrm{qualified}} = 18 \times 3{,}600 \times 10^5 = 6.48 \times 10^9,
          \qquad
          R_{\mathrm{wall}} = \frac{6.48 \times 10^9}{24 \times 3{,}600} = 75{,}000\ \mathrm{shots/s}.
          $$

      - **进一步折损项**：在 $7.5\times 10^4\ \mathrm{s}^{-1}$ 之上，真实生产作业还要扣除云端排队等待、编译与参数下发间隙、运行中途失败与重试作业、后选择丢弃率以及误差缓解（ZNE/PEC/切割）带来的额外采样倍率，使真正交付给用户的有效答案吞吐率远低于标称峰值 $10^5\ \mathrm{shots/s}$。
    - **结论与边界回验**：峰值 $10^5\ \mathrm{shots/s}$ 仅代表理想瞬时速率；扣除非计划故障、计划校准、质量降级窗口（日志按并集积分核算，如上例降至 $75{,}000\ \mathrm{s}^{-1}$；独立乘积例降至 $78{,}750\ \mathrm{s}^{-1}$）以及排队、失败重试与后选择接受率后，长期墙钟有效吞吐往往远低于峰值。
    - **易错坑提醒**：一是把峰值采样速率乘以 $86{,}400$ 秒当成单日真实产能；二是面对有明确起止时刻的运维日志时，盲目把各段可用比例直接相乘（或把重叠停机重复扣减），并且把降级窗口产出的不达标样本混进“合格有效样本”分子中。

## 第 20 章

1. **【计算】单电子自旋理想直流与交流灵敏度及跨平台可比性**

   - **题意与约定**：给定单电子自旋探针（探针数 $N = 1$），旋磁比普通频率口径为 $\frac{\gamma_e}{2\pi} = 28.025\ \mathrm{GHz/T}$，在无死时间（$t_d = 0$）、无读出损耗（$C = 1$）且不含衰减因子 $e$ 的理想条件下，求单轮探询时长 $\tau = 1\ \mu\mathrm{s}$ 与 $\tau = 1\ \mathrm{ms}$ 的磁场灵敏度 $\eta$（单位 $\mathrm{nT/\sqrt{Hz}}$），并分析为何不能仅凭 $\eta$ 将单个金刚石 NV 色心与 SERF 原子磁力计直接比大小。
   - **核心提示**：把 $\gamma_e=2\pi\times 28.025\,\mathrm{GHz/T}$ 代入理想直流灵敏度 $\eta_{\mathrm{dc}}=\frac{1}{\gamma_e\sqrt{T_2^*}}$ 与理想交流灵敏度 $\eta_{\mathrm{ac}}=\frac{\pi}{2\gamma_e\sqrt{T_2}}$（注意角频率 $2\pi$ 因子与单位 $\mathrm{T/\sqrt{Hz}}$），再列出跨平台对比须固定的口径。
   - **完整分步演算**：先把普通频率口径换算为角频率旋磁比 $\gamma_e$（单位 $\mathrm{rad/(s\cdot T)}$）：

     $$
     \gamma_e = 2\pi \times 28.025 \times 10^9\ \mathrm{rad/(s\cdot T)} \approx 1.76086 \times 10^{11}\ \mathrm{rad/(s\cdot T)}.
     $$

     $N$ 个独立无噪自旋单轮相位下限为 $\delta\phi_1 = 1/\sqrt{N}$，由 $\phi = \gamma_e B \tau$ 得单轮磁场不确定度 $\delta B_1 = \frac{1}{\gamma_e \tau \sqrt{N}}$。总墙钟时长 $T$ 内可重复 $\nu = T/\tau$ 轮，统计平均缩小 $\sqrt{\nu}$ 倍，因此

     $$
     \delta B(T) = \frac{1}{\gamma_e \tau \sqrt{N}}\cdot\sqrt{\frac{\tau}{T}} = \frac{1}{\gamma_e\sqrt{N\tau}}\cdot\frac{1}{\sqrt{T}}
     \quad\Longrightarrow\quad
     \eta \equiv \delta B(T)\sqrt{T} = \frac{1}{\gamma_e\sqrt{N\tau}}.
     $$

     将 $N = 1$ 与两档探询时长分别代入（利用 $1\ \mathrm{s}^{1/2} = 1\ \mathrm{Hz}^{-1/2}$）：

     $$
     \tau_{\mathrm{DC}} = 1\ \mu\mathrm{s} = 10^{-6}\ \mathrm{s} \implies \sqrt{\tau_{\mathrm{DC}}} = 10^{-3}\ \mathrm{s}^{1/2}, \qquad
     \eta_{\mathrm{DC}}^{\mathrm{ideal}} = \frac{1}{1.76086 \times 10^{11} \times 10^{-3}} \approx 5.679 \times 10^{-9}\ \mathrm{T/\sqrt{Hz}} = 5.68\ \mathrm{nT/\sqrt{Hz}};
     $$

     $$
     \tau_{\mathrm{AC}} = 1\ \mathrm{ms} = 10^{-3}\ \mathrm{s} \implies \sqrt{\tau_{\mathrm{AC}}} = \sqrt{1000}\times 10^{-3}\ \mathrm{s}^{1/2}, \qquad
     \eta_{\mathrm{AC}}^{\mathrm{ideal}} = \frac{5.679\ \mathrm{nT/\sqrt{Hz}}}{\sqrt{1000}} \approx 0.1796\ \mathrm{nT/\sqrt{Hz}} \approx 180\ \mathrm{pT/\sqrt{Hz}}.
     $$

   - **结论与边界回验**：两档数值与配套脚本 `sensing_lab.py`（`5.679` 与 `0.1796 nT/sqrt(Hz)`）完全一致，比例恰为 $\sqrt{1000} \approx 31.62$。虽然 SERF 光学泵浦原子磁力计（OPM）的体灵敏度可达 $\sim 1\ \mathrm{fT/\sqrt{Hz}}$，比室温单 NV 低约 $6$ 个数量级，但 SERF OPM 依赖毫米至厘米级加热气室（$150\text{–}200\,^\circ\mathrm{C}$、含 $\sim 10^{13}$ 颗原子）和多层磁屏蔽近零场，无法贴近纳米尺度样品；而磁偶极场按距离 $1/r^3$ 衰减，探头工作距离从 $1\ \mathrm{cm}$ 缩至 $10\ \mathrm{nm}$（缩小 $10^6$ 倍）时，同一核自旋的局域场强暴涨 $10^{18}$ 倍。因此离开探测体积、工作距离、温度环境与带宽单比 $\mathrm{T/\sqrt{Hz}}$ 属于伪比较。
   - **易错坑提醒**：别漏乘 $2\pi$ 把 $\gamma_e/(2\pi)$ 直接当成 $\gamma_e$（会高估 $\eta$ 达 $6.28$ 倍），也别把单位 $\mathrm{nT/\sqrt{Hz}}$ 误当成单次最小可测磁场 $\mathrm{nT}$。

2. **【计算】有限可见度 $V = 0.8$ 的单比特 Ramsey 经典 Fisher 信息与 $90^\circ$ 脉冲偏置**

   - **题意与约定**：给定带有限条纹可见度 $V = 0.8$ 的二元 Ramsey 输出分布 $P(+\mid\phi) = \frac{1 + V\cos\phi}{2}$ 与 $P(-\mid\phi) = \frac{1 - V\cos\phi}{2}$（$\phi \in \mathbb{R}$，单位 $\mathrm{rad}$），求经典 Fisher 信息 $F_C(\phi; 0.8)$ 的解析式，比较 $\phi = \pi/2$ 与 $\phi = 0$，并说明第二发 $\pi/2$ 脉冲旋转 $90^\circ$ 的物理原因。
   - **核心提示**：对二元分布 $P(\pm\mid\phi)=\frac{1\pm V\cos\phi}{2}$，先求导数 $\partial_\phi P$，代入经典 Fisher 信息定义 $F_C(\phi)=\frac{(\partial_\phi P_+)^2}{P_+(1-P_+)}$ 化简关于 $\phi$ 的表达式，再找最大值点并说明如何用 $90^\circ$ 脉冲偏置工作点。
   - **完整分步演算**：先核验概率归一化 $P(+\mid\phi) + P(-\mid\phi) = \frac{1+V\cos\phi}{2} + \frac{1-V\cos\phi}{2} = 1$，并对 $\phi$ 逐项求偏导：

     $$
     \frac{\partial P(+\mid\phi)}{\partial\phi} = -\frac{V}{2}\sin\phi, \qquad
     \frac{\partial P(-\mid\phi)}{\partial\phi} = +\frac{V}{2}\sin\phi.
     $$

     代入经典 Fisher 信息定义 $F_C(\phi; V) = \sum_{x\in\{+,-\}} \frac{[\partial_\phi P(x\mid\phi)]^2}{P(x\mid\phi)}$ 逐步通分化简：

     $$
     \begin{aligned}
     F_C(\phi; V)
     &= \frac{\bigl(-\frac{V}{2}\sin\phi\bigr)^2}{\frac{1 + V\cos\phi}{2}}
      + \frac{\bigl(+\frac{V}{2}\sin\phi\bigr)^2}{\frac{1 - V\cos\phi}{2}} \\
     &= \frac{V^2\sin^2\phi}{2}\left(\frac{1}{1 + V\cos\phi} + \frac{1}{1 - V\cos\phi}\right) \\
     &= \frac{V^2\sin^2\phi}{2}\cdot\frac{(1 - V\cos\phi) + (1 + V\cos\phi)}{1 - V^2\cos^2\phi}
      = \frac{V^2\sin^2\phi}{1 - V^2\cos^2\phi}.
     \end{aligned}
     $$

     将 $V = 0.8$（$V^2 = 0.64$）代入得 $F_C(\phi; 0.8) = \frac{0.64\sin^2\phi}{1 - 0.64\cos^2\phi}$。分别计算两个工作点：

     $$
     F_C\!\left(\frac{\pi}{2};\, 0.8\right) = \frac{0.64 \times 1^2}{1 - 0.64 \times 0^2} = 0.64, \qquad
     F_C(0;\, 0.8) = \frac{0.64 \times 0^2}{1 - 0.64 \times 1^2} = \frac{0}{0.36} = 0.
     $$

   - **结论与边界回验**：$\phi = \pi/2$ 处的 $0.64 = V^2$ 精确达到退相位单比特的量子 Fisher 信息上限 $F_Q = V^2$（`sensing_lab.py` 数值验证一致）；而在 $\phi = 0$ 处，分子斜率平方归零、分母因有限噪声保持 $1 - V^2 = 0.36 > 0$，导致 $F_C = 0$ 且 Cramér–Rao 下界发散（$\Delta\phi \to \infty$），同时偶函数 $\cos(+\epsilon) = \cos(-\epsilon)$ 也无法分辨微小信号的符号。实验中把第二发 $\pi/2$ 脉冲的相位旋转 $90^\circ$（等效在 $Y$ 基读出），将条纹平移为 $P(+_y\mid\phi) = \frac{1 + V\sin\phi}{2}$，正好把最陡的线性斜坡和峰值 $F_C = V^2$ 对准待测的微小信号 $\phi \approx 0$。
   - **易错坑提醒**：理想无噪（$V=1$）时分子分母的 $\sin^2\phi$ 精确约去给人“$\phi = 0$ 同样灵敏”的假象，一旦有哪怕 $1\%$ 噪声或读出错报，波峰处立即坍塌为灵敏度盲点。

3. **【进阶】纯态幺正编码的本征态零信息与根保真度 / 平方保真度的二阶展开**

   - **题意与约定**：考察纯态幺正编码 $|\psi_\theta\rangle = e^{-i\theta H}|\psi_0\rangle$（$H = H^\dagger$ 为不含 $\theta$ 的厄米生成元，$\theta \in \mathbb{R}$），分析本征态初态的 $F_Q$，并按全书统一的根保真度口径 $F(\rho,\sigma) = \operatorname{Tr}\sqrt{\sqrt\rho\sigma\sqrt\rho}$ 推导 $\delta \to 0$ 的二阶展开，再对比平方保真度 $F^2$。
   - **核心提示**：第一问把本征态方差 $\Delta H=0$ 代入纯态 QFI 公式 $F_Q=4(\Delta H)^2$；第二问对 $|\langle\psi_0|e^{-i\delta\theta H}|\psi_0\rangle|$ 做泰勒展开到 $(\delta\theta)^2$ 阶，分别写出平方保真度 $F^2$ 与根保真度 $F$ 的二阶系数（留心 $1/8$ 与 $1/4$ 的两倍差！）。
   - **完整分步演算**：纯态幺正编码满足 $F_Q(|\psi_\theta\rangle) = 4(\Delta H)^2 = 4\bigl(\langle H^2\rangle - \langle H\rangle^2\bigr)$。若初态取为 $H$ 的归一化本征态 $|\psi_0\rangle = |\lambda\rangle$（$H|\lambda\rangle = \lambda|\lambda\rangle$），则

     $$
     \langle H\rangle = \langle\lambda|H|\lambda\rangle = \lambda, \qquad
     \langle H^2\rangle = \langle\lambda|H^2|\lambda\rangle = \lambda^2
     \quad\Longrightarrow\quad
     F_Q = 4(\lambda^2 - \lambda^2) = 0.
     $$

     物理上，此时演化态 $|\psi_\theta\rangle = e^{-i\theta\lambda}|\lambda\rangle$ 只多出一个与测量统计无关的全局相位，当然无法携带任何关于 $\theta$ 的信息。接着将相邻纯态的复重叠按 $\delta \to 0$ 做二阶泰勒展开：

     $$
     \langle\psi_\theta|\psi_{\theta+\delta}\rangle
     = \langle\psi_\theta|e^{-i\delta H}|\psi_\theta\rangle
     = 1 - i\delta\langle H\rangle - \frac{\delta^2}{2}\langle H^2\rangle + O(\delta^3).
     $$

     取复数模平方（实部平方加虚部平方）得到**平方保真度** $F^2$：

     $$
     \begin{aligned}
     F^2(\rho_\theta, \rho_{\theta+\delta})
     &= \left(1 - \frac{\delta^2}{2}\langle H^2\rangle\right)^2 + \delta^2\langle H\rangle^2 + O(\delta^3) \\
     &= 1 - \bigl(\langle H^2\rangle - \langle H\rangle^2\bigr)\delta^2 + O(\delta^3)
      = 1 - (\Delta H)^2\delta^2 + O(\delta^3)
      = 1 - \frac{1}{4}F_Q(\rho_\theta)\,\delta^2 + O(\delta^3).
     \end{aligned}
     $$

     对上式开平方并利用 $\sqrt{1 - u} = 1 - \frac{u}{2} + O(u^2)$，立刻得到全书统一的**根保真度**二阶展开（Braunstein–Caves 定理保证该式对一般满秩混态同样成立）：

     $$
     F(\rho_\theta, \rho_{\theta+\delta}) = 1 - \frac{1}{8}F_Q(\rho_\theta)\,\delta^2 + O(\delta^3)
     \quad\Longleftrightarrow\quad
     F_Q(\rho_\theta) = 8\lim_{\delta\to 0}\frac{1 - F(\rho_\theta, \rho_{\theta+\delta})}{\delta^2}.
     $$

   - **结论与边界回验**：用 $\delta = 0$ 检验两端均得 $1$；比较两式可见，改用平方保真度 $F^2$ 时，二阶项系数从 $-\frac{1}{8}F_Q$ 变为 $-\frac{1}{4}F_Q$，相应的极限系数从 $8$ 变为 $4$（恰好相差 $2$ 倍）。
   - **易错坑提醒**：查阅不同量子传感论文时，若看到 $F_Q = 4\lim_{\delta\to 0}(1-\mathcal{F})/\delta^2$ 而非系数 $8$，不要误判算错，先确认该文献把 $\mathcal{F}$ 定义为平方保真度 $F^2$ 还是根保真度 $F$。

4. **【计算】$N = 3$ 比特 GHZ 态宇称测量手算、$F_C = F_Q = 9$ 与动态范围收缩**

   - **题意与约定**：在 $8$ 维大端序计算基 $\{|000\rangle, |001\rangle, \dots, |111\rangle\}$ 中，考察相位编码后的 $3$ 比特 GHZ 态 $|\psi_3(\phi)\rangle = \frac{|000\rangle + e^{i 3\phi}|111\rangle}{\sqrt{2}}$，手算局部 $H^{\otimes 3}$ 变换后的偶/奇宇称概率 $P_{\mathrm{even}}(\phi), P_{\mathrm{odd}}(\phi)$ 与经典 Fisher 信息 $F_C(\phi)$，验证 $F_C = F_Q = 9$，并给出无歧义相位区间。
   - **核心提示**：把 $X^{\otimes 3}$ 逐项作用在 3 比特 GHZ 相位态上算宇称期望 $\langle\Pi_X\rangle=\cos(3\phi)$ 与概率 $P(\pm\mid\phi)=\frac{1\pm\cos(3\phi)}{2}$，代入 $F_C(\phi)$ 验证它处处达到 $N^2=9$，再看周期从 $2\pi$ 缩窄到 $2\pi/3$ 对无歧义动态范围的影响。
   - **完整分步演算**：利用 $H|0\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}$、$H|1\rangle = \frac{|0\rangle-|1\rangle}{\sqrt{2}}$，对任意 $3$ 位比特串 $x \in \{0,1\}^3$（记 Hamming 权重、即串中 $1$ 的个数为 $|x|$），按张量积逐位展开得

     $$
     \langle x|H^{\otimes 3}|000\rangle = \frac{1}{2\sqrt{2}}, \qquad
     \langle x|H^{\otimes 3}|111\rangle = \frac{(-1)^{|x|}}{2\sqrt{2}}
     \quad\Longrightarrow\quad
     \langle x|H^{\otimes 3}|\psi_3(\phi)\rangle = \frac{1 + (-1)^{|x|}e^{i 3\phi}}{4}.
     $$

     将 $8$ 个比特串按宇称分为两组（每组恰好 $4$ 串），利用 $|1 \pm e^{i 3\phi}|^2 = (1\pm e^{-i 3\phi})(1\pm e^{i 3\phi}) = 2 \pm 2\cos(3\phi)$ 逐项求和：
     - **偶宇称组** $\{000, 011, 101, 110\}$（$|x|\in\{0,2\}$）：每串概率 $\frac{2+2\cos(3\phi)}{16} = \frac{1+\cos(3\phi)}{8}$，合计 $P_{\mathrm{even}}(\phi) = 4\cdot\frac{1+\cos(3\phi)}{8} = \frac{1+\cos(3\phi)}{2}$；
     - **奇宇称组** $\{001, 010, 100, 111\}$（$|x|\in\{1,3\}$）：每串概率 $\frac{1-\cos(3\phi)}{8}$，合计 $P_{\mathrm{odd}}(\phi) = 4\cdot\frac{1-\cos(3\phi)}{8} = \frac{1-\cos(3\phi)}{2}$。

     对 $\phi$ 求导得 $\partial_\phi P_{\mathrm{even}} = -\frac{3}{2}\sin(3\phi)$、$\partial_\phi P_{\mathrm{odd}} = +\frac{3}{2}\sin(3\phi)$，代入经典 Fisher 信息公式：

     $$
     F_C(\phi)
     = \frac{\bigl(-\frac{3}{2}\sin 3\phi\bigr)^2}{\frac{1+\cos 3\phi}{2}}
     + \frac{\bigl(+\frac{3}{2}\sin 3\phi\bigr)^2}{\frac{1-\cos 3\phi}{2}}
     = \frac{9}{2}\sin^2(3\phi)\cdot\frac{2}{1 - \cos^2(3\phi)}
     = 9 \qquad \bigl(3\phi \notin \pi\mathbb{Z}\bigr).
     $$

     再由生成元 $J_z = \frac{1}{2}(Z_0 + Z_1 + Z_2)$ 独立核验 QFI：$|000\rangle$ 与 $|111\rangle$ 的特征值分别为 $+\frac{3}{2}$ 与 $-\frac{3}{2}$，故 $\langle J_z\rangle = 0$、$\langle J_z^2\rangle = \frac{1}{2}(\frac{9}{4}) + \frac{1}{2}(\frac{9}{4}) = \frac{9}{4}$，得 $F_Q = 4(\Delta J_z)^2 = 4 \times \frac{9}{4} = 9 = F_C$。
   - **结论与边界回验**：$P_{\mathrm{even}} + P_{\mathrm{odd}} = 1$ 且宇称期望 $\langle X^{\otimes 3}\rangle = P_{\mathrm{even}} - P_{\mathrm{odd}} = \cos(3\phi)$（与 `sensing_lab.py` 数值断言吻合）。因为条纹周期从单比特的 $2\pi$ 缩成 $\frac{2\pi}{3}$，单调无歧义的相位动态范围缩窄到了 $\bigl[0, \frac{\pi}{3}\bigr]$（一般 $N$ 比特为 $\bigl[0, \frac{\pi}{N}\bigr]$）。
   - **易错坑提醒**：宇称灵敏度放大 $N$ 倍与动态范围缩小 $N$ 倍相伴相生；实际测大范围未知相位需借助逐级倍增的探询序列或自适应锁相解开相位卷绕。

5. **【进阶】可分态 $F_Q \le N$ 上界与 GHZ 态丢失 1 个比特后 $F_Q = 0$**

   - **题意与约定**：在全局局域相位编码 $U_N(\phi) = e^{-i\phi J_z}$（$J_z = \frac{1}{2}\sum_{j=1}^N Z_j$）下，先用 QFI 的凸性与可加性证出任意 $N$ 比特可分态的上限 $F_Q \le N$，再对 $N$ 比特 GHZ 态求偏迹说明丢失任意 $1$ 个比特的后果。
   - **核心提示**：第一问对乘积态用可加性 $F_Q(\bigotimes_j\rho_j)=\sum_j F_Q(\rho_j)\le N$，再用 QFI 的凸性推广到任意可分混态；第二问对 $N$ 比特 GHZ 相位态求任意单比特偏迹，观察相位 $e^{iN\phi}$ 是否在约化密度矩阵中彻底消失。
   - **完整分步演算**：任意 $N$ 比特可分态可写为直积态的凸组合 $\rho_{\mathrm{sep}} = \sum_m p_m\,\rho_m^{(1)}\otimes\cdots\otimes\rho_m^{(N)}$（$p_m \ge 0,\;\sum_m p_m = 1$）。依次运用三条性质：（1）QFI 的**凸性** $F_Q(\sum_m p_m\sigma_m) \le \sum_m p_m F_Q(\sigma_m)$；（2）在局域加性生成元下的**张量积可加性** $F_Q(\bigotimes_{j=1}^N \rho_m^{(j)}) = \sum_{j=1}^N F_Q(\rho_m^{(j)})$；（3）单比特生成元 $Z_j/2$ 特征值为 $\pm\frac{1}{2}$，故单比特 QFI 上界为 $F_Q(\rho_m^{(j)}) \le \bigl(\frac{1}{2} - (-\frac{1}{2})\bigr)^2 = 1$：

     $$
     F_Q(\rho_{\mathrm{sep}})
     \le \sum_m p_m\, F_Q\!\left(\bigotimes_{j=1}^N \rho_m^{(j)}\right)
     = \sum_m p_m \sum_{j=1}^N F_Q\!\bigl(\rho_m^{(j)}\bigr)
     \le \sum_m p_m \sum_{j=1}^N 1
     = N.
     $$

     再看编码后的 $N$ 比特 GHZ 态 $|\psi_N(\phi)\rangle = \frac{|0\rangle^{\otimes N} + e^{i N\phi}|1\rangle^{\otimes N}}{\sqrt{2}}$。由置换对称性，不妨设丢失最右侧第 $N$ 个比特，将密度矩阵 $|\psi_N(\phi)\rangle\langle\psi_N(\phi)|$ 展开四项并对第 $N$ 个比特求偏迹（利用正交性 $\operatorname{Tr}(|0\rangle\langle 1|) = \langle 1|0\rangle = 0$ 与 $\operatorname{Tr}(|1\rangle\langle 0|) = \langle 0|1\rangle = 0$）：

     $$
     \begin{aligned}
     \rho_{1\cdots N-1}(\phi)
     &= \operatorname{Tr}_N\bigl(|\psi_N(\phi)\rangle\langle\psi_N(\phi)|\bigr) \\
     &= \frac{1}{2}|0\rangle^{\otimes(N-1)}\langle 0|^{\otimes(N-1)}\operatorname{Tr}(|0\rangle\langle 0|)
      + \frac{e^{-i N\phi}}{2}|0\rangle^{\otimes(N-1)}\langle 1|^{\otimes(N-1)}\underbrace{\operatorname{Tr}(|0\rangle\langle 1|)}_{0} \\
     &\quad + \frac{e^{+i N\phi}}{2}|1\rangle^{\otimes(N-1)}\langle 0|^{\otimes(N-1)}\underbrace{\operatorname{Tr}(|1\rangle\langle 0|)}_{0}
      + \frac{1}{2}|1\rangle^{\otimes(N-1)}\langle 1|^{\otimes(N-1)}\operatorname{Tr}(|1\rangle\langle 1|) \\
     &= \frac{1}{2}|0\rangle^{\otimes(N-1)}\langle 0|^{\otimes(N-1)} + \frac{1}{2}|1\rangle^{\otimes(N-1)}\langle 1|^{\otimes(N-1)}.
     \end{aligned}
     $$

     所有含 $e^{\pm i N\phi}$ 的相干非对角项彻底归零，$\rho_{1\cdots N-1}$ 与 $\phi$ 完全无关，于是 $\partial_\phi\rho_{1\cdots N-1} \equiv 0$，SLD 算符 $L_\phi = 0$，立刻得到 $F_Q(\rho_{1\cdots N-1}) = \operatorname{Tr}(\rho_{1\cdots N-1} L_\phi^2) = 0$。
   - **结论与边界回验**：约化态满足 $\operatorname{Tr}\rho_{1\cdots N-1} = \frac{1}{2} + \frac{1}{2} = 1$ 且半正定（`sensing_lab.py` 针对 $N=4$ 核验相位差残差 $< 10^{-16}$）。反观 $N$ 个独立比特，丢失 $1$ 个仅使 $F_Q$ 从 $N$ 温和降至 $N-1$。
   - **易错坑提醒**：经典关联的混合可分态依然受限于 $F_Q \le N$，突破 SQL 必须依赖真量子纠缠；而 GHZ 态虽把 $F_Q$ 拉到极致 $N^2$，却毫无抗粒子丢失容错能力。

6. **【计算】独立马尔可夫纯退相位下的 Huelga（1997）坍塌与常数因子 $e$**

   - **题意与约定**：在独立马尔可夫纯退相位率 $\gamma > 0$（单比特非对角元衰减为 $e^{-\gamma t}$）、固定总墙钟时间 $T$ 且零死时间 $t_d = 0$（重复轮数 $\nu = T/t$）条件下，分别最大化 $N$ 独立比特与 $N$ 比特 GHZ 态关于频率偏移 $\omega$ 的总 Fisher 信息，并与含噪终极下界 $\sqrt{2\gamma/(NT)}$ 比较。
   - **核心提示**：记单轮相干时长为 $t$、总轮数 $\nu=T/t$，分别写出独立比特总信息 $I_{\mathrm{ind}}(t)=\frac{T}{t}N t^2 e^{-2\gamma t}$ 与 GHZ 总信息 $I_{\mathrm{GHZ}}(t)=\frac{T}{t}N^2 t^2 e^{-2N\gamma t}$，对 $t$ 求导找各自最优探测时长并比较最大值。
   - **完整分步演算**：对于单比特频率编码 $\phi = \omega t$，单轮 QFI 为 $F_Q^{(1)}(\omega; t) = t^2 e^{-2\gamma t}$。
     - **独立比特**：$N$ 比特单轮总信息为 $N t^2 e^{-2\gamma t}$，乘以轮数 $\nu = T/t$ 得总信息 $F_{\mathrm{unc}}(\omega; t) = N T\, t\, e^{-2\gamma t}$。令其对 $t > 0$ 的导数为零：

       $$
       \frac{d}{dt}\bigl(t\,e^{-2\gamma t}\bigr) = (1 - 2\gamma t)\,e^{-2\gamma t} = 0
       \quad\Longrightarrow\quad
       t_{\mathrm{opt}}^{\mathrm{unc}} = \frac{1}{2\gamma}.
       $$

       二阶导数在驻点处为 $-2\gamma e^{-1} < 0$，确为全局极大值。代回得

       $$
       F_{\mathrm{unc}}^{\max} = N T \cdot \frac{1}{2\gamma}\cdot e^{-1} = \frac{N T}{2 e \gamma}, \qquad
       (\Delta\omega)_{\mathrm{unc}}^{\min} = \frac{1}{\sqrt{F_{\mathrm{unc}}^{\max}}} = \sqrt{\frac{2 e \gamma}{N T}}.
       $$

     - **$N$ 比特 GHZ 态**：局域信道 $\mathcal{E}_t^{\otimes N}$ 作用在交叉项 $(|0\rangle\langle 1|)^{\otimes N}$ 上把 $N$ 个衰减因子连乘，相干度按 $e^{-N\gamma t}$ 衰减，单轮 QFI 为 $F_{\mathrm{GHZ}}^{(1)}(\omega; t) = N^2 t^2 e^{-2N\gamma t}$。总信息 $F_{\mathrm{GHZ}}(\omega; t) = \frac{T}{t}\cdot N^2 t^2 e^{-2N\gamma t} = N^2 T\, t\, e^{-2N\gamma t}$。同样求极值：

       $$
       \frac{d}{dt}\bigl(t\,e^{-2 N \gamma t}\bigr) = (1 - 2 N \gamma t)\,e^{-2 N \gamma t} = 0
       \quad\Longrightarrow\quad
       t_{\mathrm{opt}}^{\mathrm{GHZ}} = \frac{1}{2 N \gamma}.
       $$

       将最优时长代回，分子的 $N^2$ 与分母的 $N$ 精确抵消：

       $$
       F_{\mathrm{GHZ}}^{\max} = N^2 T \cdot \frac{1}{2 N \gamma}\cdot e^{-1} = \frac{N T}{2 e \gamma} = F_{\mathrm{unc}}^{\max}, \qquad
       (\Delta\omega)_{\mathrm{GHZ}}^{\min} = \sqrt{\frac{2 e \gamma}{N T}} = (\Delta\omega)_{\mathrm{unc}}^{\min}.
       $$

     - **常数因子 $e$ 的精确落点**：在含噪普适下界 $(\Delta\omega)_{\mathrm{ult}} = \sqrt{\frac{2\gamma}{NT}}$ 下（对应 $F_{\mathrm{tot}}^{\mathrm{any}} < \frac{NT\,t}{e^{2\gamma t}-1} < \frac{NT}{2\gamma}$），计算方差与标准差之比：

       $$
       \frac{\bigl[(\Delta\omega)_{\mathrm{unc}}^{\min}\bigr]^2}{\bigl[(\Delta\omega)_{\mathrm{ult}}\bigr]^2}
       = \frac{\bigl[(\Delta\omega)_{\mathrm{GHZ}}^{\min}\bigr]^2}{\bigl[(\Delta\omega)_{\mathrm{ult}}\bigr]^2}
       = \frac{2 e \gamma / (NT)}{2\gamma / (NT)} = e \approx 2.7183, \qquad
       \frac{(\Delta\omega)_{\mathrm{GHZ}}^{\min}}{(\Delta\omega)_{\mathrm{ult}}} = \sqrt{e} \approx 1.6487.
       $$

   - **结论与边界回验**：量纲检查 $[\sqrt{\gamma/(NT)}] = \mathrm{s}^{-1/2}/\mathrm{s}^{1/2} = \mathrm{s}^{-1} = \mathrm{rad/s}$ 自洽。结论是：零死时间下 GHZ 退回 SQL 并与独立比特精确打平；而常数因子 $e$（标准差 $\sqrt{e}$）并非“GHZ 赢了独立比特 $e$ 倍”，而是**一切最优纠缠态（如最优压缩态）相对于独立比特/GHZ 在马尔可夫退相位下所能获得的极限常数倍提升上限**。
   - **易错坑提醒**：Huelga 原文定义衰减率使 $\rho_{01} \propto e^{-\gamma_{\mathrm{H}} t/2}$（即 $\gamma = \gamma_{\mathrm{H}}/2$），换算时注意因子 $2$，别把 $e$ 的位置记反。

7. **【计算】有限死时间 $t_d = 0.1\ \mathrm{s}$ 下含噪 GHZ 严格输给独立比特**

   - **题意与约定**：取 $N = 16$、$\gamma = 1\ \mathrm{s}^{-1}$、$T = 100\ \mathrm{s}$ 与每轮制备读出死时间 $t_d = 0.1\ \mathrm{s}$（重复轮数 $\nu = \frac{T}{t + t_d}$），分别在 $t = 0.5\ \mathrm{s}$（独立比特）与 $t = 0.05\ \mathrm{s}$（GHZ 态）处核算总 Fisher 信息与频率不确定度。
   - **核心提示**：把总轮数替换为 $\nu=T/(t+t_d)$，分别计算独立比特与 $N=16$ GHZ 态在固定 $t_d=0.1\,\mathrm{s}$ 下的目标函数 $\frac{T}{t+t_d}N^k t^2 e^{-2k\gamma t}$（$k=1$ vs $k=16$），定位各自最优点并比较总信息量。
   - **完整分步演算**：逐项代入总信息公式 $F_{\mathrm{tot}}(t) = \frac{T}{t + t_d} F^{(1)}(t)$：
     - **独立比特（$t = 0.5\ \mathrm{s}$）**：占空比 $\frac{t}{t+t_d} = \frac{0.5}{0.6} \approx 83.33\%$，总轮数 $\nu_{\mathrm{unc}} = \frac{100}{0.6} = \frac{500}{3} \approx 166.67$；单轮信息 $F_{\mathrm{unc}}^{(1)} = 16 \times 0.5^2 \times e^{-2\times 1\times 0.5} = 4 e^{-1} \approx 1.4715\ \mathrm{s}^2$，于是

       $$
       F_{\mathrm{unc}}^{\mathrm{tot}}(0.5) = \frac{500}{3}\times 4 e^{-1} = \frac{2000}{3}e^{-1} \approx 245.25\ \mathrm{s}^2, \qquad
       \Delta\omega_{\mathrm{unc}} = \frac{1}{\sqrt{245.25}} \approx 0.06386\ \mathrm{rad/s}.
       $$

     - **含噪 GHZ 态（$t = 0.05\ \mathrm{s}$）**：占空比骤降至 $\frac{0.05}{0.15} \approx 33.33\%$，总轮数 $\nu_{\mathrm{GHZ}} = \frac{100}{0.15} = \frac{2000}{3} \approx 666.67$；因衰减指数为 $2 N \gamma t = 2\times 16\times 1\times 0.05 = 1.6$，单轮信息 $F_{\mathrm{GHZ}}^{(1)} = 16^2 \times 0.05^2 \times e^{-1.6} = 0.64\,e^{-1.6} \approx 0.12921\ \mathrm{s}^2$，于是

       $$
       F_{\mathrm{GHZ}}^{\mathrm{tot}}(0.05) = \frac{2000}{3}\times 0.64\,e^{-1.6} = \frac{1280}{3}e^{-1.6} \approx 86.14\ \mathrm{s}^2, \qquad
       \Delta\omega_{\mathrm{GHZ}} = \frac{1}{\sqrt{86.14}} \approx 0.10774\ \mathrm{rad/s}.
       $$

   - **结论与边界回验**：比值 $F_{\mathrm{unc}}^{\mathrm{tot}} / F_{\mathrm{GHZ}}^{\mathrm{tot}} \approx 2.847$，$\Delta\omega_{\mathrm{GHZ}} / \Delta\omega_{\mathrm{unc}} \approx 1.687$（`sensing_lab.py` 对两策略分别做全局寻优得 $t_{\mathrm{opt}}^{\mathrm{unc}} \approx 0.574\ \mathrm{s},\; \Delta\omega \approx 0.0635\ \mathrm{rad/s}$ 与 $t_{\mathrm{opt}}^{\mathrm{GHZ}} \approx 0.0518\ \mathrm{s},\; \Delta\omega \approx 0.1077\ \mathrm{rad/s}$，GHZ 仍劣于独立比特 $1.70$ 倍）。根本原因在于：GHZ 的 $N$ 倍退相位强迫单轮探询时长缩到 $t \sim 1/(2N\gamma) \ll t_d$，致使逾三分之二的墙钟时间白白消耗在反复重置与纠缠制备上，彻底打破了零死时间下的平局。
   - **易错坑提醒**：评判纠缠传感器是否实用，必须用含死时间 $t_d$ 的真实墙钟总时间 $T$ 核算，单比单轮相干时长内的瞬时斜率会严重高估脆弱纠缠态。

8. **【进阶】$N = 2$ 单轴扭转 Wineland 压缩参数、光学损耗天花板与 LIGO O4 滤波腔**

   - **题意与约定**：在 $N = 2$ 对称三重态子空间 $\{|+1\rangle = |00\rangle,\; |0\rangle_S = \frac{|01\rangle+|10\rangle}{\sqrt{2}},\; |-1\rangle = |11\rangle\}$ 中验证单轴扭转（OAT）态 $|\psi(\theta)\rangle = e^{-i\theta J_z^2}|+\rangle^{\otimes 2}$ 在 $\theta = \pi/6$ 处的 Wineland 参数 $\xi_R^2 = 2/3$；再算 $20\%$ 光学损耗下注入 $10\ \mathrm{dB}$ 压缩光的实测降噪，并解释 LIGO O4 增设 $300\ \mathrm{m}$ 滤波腔的动机。
   - **核心提示**：在 $N=2$ 对称三重态基下把单轴扭转态展开，计算平均自旋长度 $|\langle\vec J\rangle|$ 与垂直平面最小方差 $\Delta J_\perp^2$ 代入 Wineland 参数 $\xi_R^2=\frac{N(\Delta J_\perp)^2}{|\langle\vec J\rangle|^2}$；再由光损下压缩方差混合模型 $V_{\mathrm{out}}=\eta V_{\mathrm{in}}+(1-\eta)$ 导出损耗天花板。
   - **完整分步演算**：在三重态基下 $J_z = \operatorname{diag}(1, 0, -1)$，$J_z^2 = \operatorname{diag}(1, 0, 1)$，初态 $|+\rangle^{\otimes 2} = (\frac{1}{2}, \frac{1}{\sqrt{2}}, \frac{1}{2})^T$ 演化为 $|\psi(\theta)\rangle = (\frac{1}{2}e^{-i\theta}, \frac{1}{\sqrt{2}}, \frac{1}{2}e^{-i\theta})^T$（范数平方 $\frac{1}{4}+\frac{1}{2}+\frac{1}{4}=1$）。逐行计算集体自旋作用：

     $$
     J_x|\psi(\theta)\rangle = \begin{pmatrix}\frac{1}{2}\\ \frac{1}{\sqrt{2}}e^{-i\theta}\\ \frac{1}{2}\end{pmatrix}
     \implies \langle J_x\rangle = \frac{e^{i\theta}}{4} + \frac{e^{-i\theta}}{2} + \frac{e^{i\theta}}{4} = \cos\theta, \qquad
     \langle J_y\rangle = \langle J_z\rangle = 0.
     $$

     再算 $y\text{–}z$ 平面协方差矩阵（由 $J_y|\psi\rangle = (-\frac{i}{2}, 0, \frac{i}{2})^T$、$J_z|\psi\rangle = (\frac{1}{2}e^{-i\theta}, 0, -\frac{1}{2}e^{-i\theta})^T$）：

     $$
     (\Delta J_y)^2 = (\Delta J_z)^2 = \frac{1}{2}, \qquad
     \operatorname{Cov}(J_y, J_z) = \operatorname{Re}\langle\psi|J_y J_z|\psi\rangle = \operatorname{Re}\!\left(\frac{i e^{-i\theta}}{2}\right) = \frac{1}{2}\sin\theta
     \implies C_{yz} = \frac{1}{2}\begin{pmatrix}1 & \sin\theta\\ \sin\theta & 1\end{pmatrix}.
     $$

     $C_{yz}$ 的最小特征值为 $(\Delta J_\perp)^2_{\min} = \frac{1 - \sin\theta}{2}$（沿 $45^\circ$ 短轴 $J_\perp = \frac{J_y - J_z}{\sqrt{2}}$），代入 Wineland 公式并在 $\theta = \pi/6$（$\sin\theta = 1/2$）求值：

     $$
     \xi_R^2(\theta) = \frac{2\cdot\frac{1 - \sin\theta}{2}}{\cos^2\theta} = \frac{1 - \sin\theta}{1 - \sin^2\theta} = \frac{1}{1 + \sin\theta}
     \quad\Longrightarrow\quad
     \xi_R^2\!\left(\frac{\pi}{6}\right) = \frac{1}{1 + 1/2} = \frac{2}{3} \approx 0.6667,
     $$

     对应压缩深度 $-10\log_{10}(2/3) \approx 1.76\ \mathrm{dB}$。再算光学压缩损耗：注入 $10\ \mathrm{dB}$ 对应 $e^{-2r} = 10^{-10/10} = 0.10$，经透射率 $\eta_{\mathrm{opt}} = 0.80$（损耗 $1 - \eta_{\mathrm{opt}} = 0.20$）分束器混入真空涨落后，相对真空方差比为

     $$
     \frac{\operatorname{Var}_{\mathrm{loss}}(\hat q)}{\operatorname{Var}_{\mathrm{vac}}(\hat q)}
     = \eta_{\mathrm{opt}} e^{-2r} + (1 - \eta_{\mathrm{opt}})
     = 0.80 \times 0.10 + 0.20 = 0.28
     \quad\Longrightarrow\quad
     -10\log_{10}(0.28) \approx 5.53\ \mathrm{dB}.
     $$

   - **结论与边界回验**：即使注入无穷大压缩（$r\to\infty$），$20\%$ 损耗也把降噪硬锁死在 $-10\log_{10}(0.20) \approx 6.99\ \mathrm{dB}$ 天花板下（与 `sensing_lab.py` 完全一致）。LIGO O3 注入频率无关压缩光时，虽然压低了高频散粒噪声（相位分量），却因不确定性面积守恒同步放大了振幅涨落 $e^{+2r}$，导致低频段打在 $40\ \mathrm{kg}$ 镜面上的量子辐射压噪声恶化；O4 增设的 $300\ \mathrm{m}$ 光学滤波腔借助色散反射让压缩椭圆角度随音频频率自动旋转——高频压缩相位、低频压缩振幅，实现全频段宽带量子降噪（Hanford $4.0\ \mathrm{dB}$、Livingston $5.8\ \mathrm{dB}$）。
   - **易错坑提醒**：光学分贝是功率/方差比 $-10\log_{10}(\mathrm{Var}_{\mathrm{ratio}})$，换算到振幅噪声缩小倍数时须除以 $20$（$10^{\mathrm{dB}/20}$），不可把两者混为一谈。

9. **【计算】对称 CPMG-$n$ 交流整流相位与频域滤波函数主峰推导**

   - **题意与约定**：对称 CPMG-$n$（$n$ 为偶数）序列总时长 $T = n\tau$，在 $t_k = \frac{2k-1}{2n}T$（$k=1,\dots,n$）处施加理想 $\pi$ 脉冲，对应方波开关函数 $s(t) \in \{+1, -1\}$。求它对共振交流磁场 $B(t) = B_{\mathrm{ac}}\cos(\pi t/\tau)$ 累积的净相位 $\phi_{\mathrm{ac}}$，并由闭式滤波函数导出共振点 $\omega_0 = \pi n/T$ 处峰值 $|Y(\omega_0)|^2 = 4/\pi^2$。
   - **核心提示**：写出对称 CPMG-$n$ 的方波调制函数 $y(t)\in\{+1,-1\}$ 与共振余弦场乘积的逐段积分求整流相位 $\Phi=\gamma\int_0^T y(t)B(t)\,dt$，再对 $y(t)$ 做傅里叶变换确定滤波函数 $F(\omega T)$ 的主峰角频率。
   - **完整分步演算**：在 $[0, \tau/2)$ 上 $s(t) = +1$ 且 $\cos(\pi t/\tau) > 0$；在 $(\tau/2, 3\tau/2)$ 上 $s(t) = -1$ 且 $\cos(\pi t/\tau) < 0$；此后每逢余弦波过零变号，$s(t)$ 同步翻号，故乘积恒非负 $s(t)\cos(\pi t/\tau) = |\cos(\pi t/\tau)|$。先算单个 $\tau/2$ 段的积分：

     $$
     \int_0^{\tau/2} \cos\!\left(\frac{\pi t}{\tau}\right)dt
     = \left[\frac{\tau}{\pi}\sin\!\left(\frac{\pi t}{\tau}\right)\right]_0^{\tau/2}
     = \frac{\tau}{\pi}(1 - 0) = \frac{\tau}{\pi}.
     $$

     每个长度为 $\tau$ 的区段贡献 $\frac{2\tau}{\pi}$，全长 $T = n\tau$ 共 $n$ 段，于是净累积相位为

     $$
     \phi_{\mathrm{ac}} = \gamma_e B_{\mathrm{ac}} \int_0^T s(t)\cos\!\left(\frac{\pi t}{\tau}\right)dt
     = \gamma_e B_{\mathrm{ac}}\cdot n\cdot\frac{2\tau}{\pi}
     = \frac{2}{\pi}\gamma_e B_{\mathrm{ac}} T \approx 0.6366\,\gamma_e B_{\mathrm{ac}} T.
     $$

     再记无量纲频率 $z = \omega T$，对偶数 $n$ 的闭式滤波函数 $|Y_{\mathrm{CPMG},n}(\omega)|^2 = \frac{16\sin^4(z/(4n))\sin^2(z/2)}{z^2\cos^2(z/(2n))}$，令 $z = n\pi + \epsilon$（$\epsilon \to 0$）逐因子展开：
     - $\sin\!\left(\frac{n\pi + \epsilon}{4n}\right) \to \sin\frac{\pi}{4} = \frac{1}{\sqrt{2}} \implies 16\sin^4\frac{\pi}{4} = 16 \times \frac{1}{4} = 4$；
     - 因 $n$ 为偶数，$\frac{n\pi}{2}$ 为 $\pi$ 的整数倍，故 $\sin\!\left(\frac{n\pi+\epsilon}{2}\right) = (-1)^{n/2}\sin\frac{\epsilon}{2} = (-1)^{n/2}\frac{\epsilon}{2} + O(\epsilon^3)$；
     - $\cos\!\left(\frac{n\pi+\epsilon}{2n}\right) = \cos\!\left(\frac{\pi}{2} + \frac{\epsilon}{2n}\right) = -\sin\frac{\epsilon}{2n} = -\frac{\epsilon}{2n} + O(\epsilon^3)$。

     两项平方相除消去 $\epsilon^2$ 并代入分母 $z^2 \to (n\pi)^2$：

     $$
     \left|Y_{\mathrm{CPMG},n}(\omega_0)\right|^2
     = \lim_{\epsilon\to 0}\frac{4}{(n\pi)^2}\cdot\frac{(\epsilon/2)^2}{(\epsilon/(2n))^2}
     = \frac{4 n^2}{n^2 \pi^2}
     = \frac{4}{\pi^2} \approx 0.4053.
     $$

   - **结论与边界回验**：峰值 $\frac{4}{\pi^2} = \left(\frac{2}{\pi}\right)^2$ 与上一步整流系数平方严丝合缝，且与脉冲数 $n$ 无关（`sensing_lab.py` 对 $n=2, 4, 8$ 数值积分均精确给出 `0.405285`）；增大 $n$ 和 $T$ 的收益在于把通带宽度 $\Delta\omega \approx 2\pi/T$ 压窄并把相干时间延展至 $T_2^{\mathrm{DD}}$。
   - **易错坑提醒**：方波开关函数在奇数倍频 $k\omega_0$（$k=3,5,\dots$）处仍有高度为 $\frac{4}{(k\pi)^2}$ 的高次谐波通带，做量子噪声谱重建时切勿忽略谐波泄漏。

10. **【进阶】HNLS 条件逐案判定与 2 比特纠错传感码构造**

    - **题意与约定**：单比特信号哈密顿量为 $H = \frac{1}{2}Z_1$，根据 HNLS 充要条件 $H \notin \mathcal{S} \equiv \operatorname{span}\{I, L, L^\dagger, L^\dagger L\}$，逐一判定三种马尔可夫噪声下量子纠错能否恢复海森堡标度，并对唯一可行情形构造 $2$ 比特纠错传感码（大端序：左位比特 $1$ 为受噪探针，右位比特 $2$ 为无噪辅助比特）。
    - **核心提示**：逐案写出 Lindblad 算符空间 $\mathcal S=\operatorname{span}\{I,L_k,L_k^\dagger,L_j^\dagger L_k\}$，检验信号 $H=\frac{1}{2}Z_1$ 是否落入 $\mathcal S$（判断退相位 vs 比特翻转）；对满足 HNLS 的横场比特翻转噪声，构造把信号与噪声分入正交子空间的 2 比特码。
    - **完整分步演算**：逐案显式写出 $\mathcal{S}$ 的全部生成元并检验 $H \in \mathcal{S}$ 是否成立：
      - **(a) 纯退相位 $L = \sqrt{\gamma}\,Z_1$**：因 $L^\dagger = \sqrt{\gamma}\,Z_1$、$L^\dagger L = \gamma Z_1^2 = \gamma I$，故 $\mathcal{S} = \operatorname{span}\{I, Z_1\}$。由于基元 $Z_1$ 已在 $\mathcal{S}$ 中，故 $H = \frac{1}{2}Z_1 \in \mathcal{S}$，**HNLS 不成立**——任何纠错码都无法把平行于信号的退相位与待测磁场分开，不能恢复海森堡标度。
      - **(b) 比特翻转 $L = \sqrt{\gamma}\,X_1$**：因 $L^\dagger = \sqrt{\gamma}\,X_1$、$L^\dagger L = \gamma X_1^2 = \gamma I$，故 $\mathcal{S} = \operatorname{span}\{I, X_1\}$。按 Hilbert–Schmidt 内积验证正交性：

        $$
        \operatorname{Tr}(Z_1 I) = 0, \qquad \operatorname{Tr}(Z_1 X_1) = \operatorname{Tr}(i Y_1) = 0
        \quad\Longrightarrow\quad
        H = \frac{1}{2}Z_1 \perp \mathcal{S},\;\; H \notin \mathcal{S}.
        $$

        **HNLS 成立**，可借助量子纠错压制噪声并保住信号，恢复海森堡标度。
      - **(c) 振幅阻尼 $L = \sqrt{\gamma}\,|0\rangle\langle 1|$**：四个生成元依次为 $I$、$L/\sqrt{\gamma} = |0\rangle\langle 1|$、$L^\dagger/\sqrt{\gamma} = |1\rangle\langle 0|$ 以及极易遗漏的二次项

        $$
        \frac{L^\dagger L}{\gamma} = |1\rangle\langle 0|\cdot|0\rangle\langle 1| = |1\rangle\langle 1| = \frac{I - Z_1}{2}.
        $$

        线性组合立得 $Z_1 = I - \frac{2}{\gamma}L^\dagger L \in \mathcal{S}$，即 $H = \frac{1}{2}Z_1 \in \mathcal{S}$，**HNLS 不成立**，同样无法恢复海森堡标度。
      - **针对 (b) 构造 2 比特纠错传感码**：取二维编码子空间 $|\bar 0\rangle = |00\rangle$、$|\bar 1\rangle = |11\rangle$，投影算符 $P = |00\rangle\langle 00| + |11\rangle\langle 11|$，**稳定子**为 $S = Z_1 Z_2$（编码空间本征值 $+1$）。逐项核验两条核心条件：

        $$
        X_1|\bar 0\rangle = |10\rangle,\quad X_1|\bar 1\rangle = |01\rangle \implies P X_1 P = 0 \quad (\text{全部落入 } S=-1 \text{ 的正交错误空间，测 } Z_1 Z_2 \text{ 即可纠正});
        $$

        $$
        Z_1|\bar 0\rangle = +|\bar 0\rangle,\quad Z_1|\bar 1\rangle = -|\bar 1\rangle \implies P Z_1 P = |\bar 0\rangle\langle\bar 0| - |\bar 1\rangle\langle\bar 1| = \bar Z \quad (\text{待测信号无损保留}).
        $$

    - **结论与边界回验**：`sensing_lab.py` 对三种噪声算出的 $H$ 到 $\mathcal{S}$ 的垂直距离依次为 `0.0`、`0.707107`（即 $\|Z/2\|_F = 1/\sqrt{2}$）和 `0.0`，矩阵断言全部通过。现实工程中还要求纠错症状提取远快于噪声率且辅助比特足够长寿。
    - **易错坑提醒**：检验 HNLS 时最常犯的错误是漏掉二次项 $L^\dagger L$，从而误以为非对角跃迁 $|0\rangle\langle 1|$ 与对角信号 $Z_1$ 正交；实际上无跃迁演化项 $-\frac{1}{2}L^\dagger L\,dt$ 沿着 $Z_1$ 轴产生不可区分的衰减漂移。

## 第 21 章

1. **【基础】3 比特 Pauli 串二元辛编码、辛内积判定与算符乘法独立回验**

   - **题意与约定**：按大端序 $(q_0, q_1, q_2)$ 与单比特编码 $(0,0)\leftrightarrow I,\;(1,0)\leftrightarrow X,\;(0,1)\leftrightarrow Z,\;(1,1)\leftrightarrow Y = iXZ$，将 $P_1 = X_0 Y_1 Z_2$ 与 $P_2 = Y_0 X_1 Z_2$ 编码为 $6$ 比特二元辛行向量 $(x_0, x_1, x_2 \mid z_0, z_1, z_2)$，计算二元辛内积判定对易性，并用直接 Pauli 乘法独立回验。
   - **核心提示**：按编码规则 $(0,0)\leftrightarrow I,(1,0)\leftrightarrow X,(0,1)\leftrightarrow Z,(1,1)\leftrightarrow Y$ 写出两个 6 比特辛行向量 $(x\mid z)$，计算模 $2$ 辛内积 $x_1\cdot z_2\oplus z_1\cdot x_2$ 判定对易性，再逐位用单比特 Pauli 乘法律独立回验。
   - **完整分步演算**：逐位读取每比特的 $(x_j, z_j)$：
     - $P_1 = X_0 Y_1 Z_2$：$q_0$ 为 $X\leftrightarrow(1,0)$、$q_1$ 为 $Y\leftrightarrow(1,1)$、$q_2$ 为 $Z\leftrightarrow(0,1)$，拼成 $v_1 = (1, 1, 0 \mid 0, 1, 1)$；
     - $P_2 = Y_0 X_1 Z_2$：$q_0$ 为 $Y\leftrightarrow(1,1)$、$q_1$ 为 $X\leftrightarrow(1,0)$、$q_2$ 为 $Z\leftrightarrow(0,1)$，拼成 $v_2 = (1, 1, 0 \mid 1, 0, 1)$。

     代入二元辛内积定义 $\langle v_1, v_2\rangle_{\mathrm{sp}} = \bigoplus_{j=0}^{2}(x_{1,j} z_{2,j} \oplus z_{1,j} x_{2,j})$ 逐位计算：

     $$
     \begin{aligned}
     \langle v_1, v_2\rangle_{\mathrm{sp}}
     &= (x_{1,0}z_{2,0} \oplus z_{1,0}x_{2,0}) \oplus (x_{1,1}z_{2,1} \oplus z_{1,1}x_{2,1}) \oplus (x_{1,2}z_{2,2} \oplus z_{1,2}x_{2,2}) \\
     &= (1\cdot 1 \oplus 0\cdot 1) \oplus (1\cdot 0 \oplus 1\cdot 1) \oplus (0\cdot 1 \oplus 1\cdot 0) \\
     &= 1 \oplus 1 \oplus 0 = 0.
     \end{aligned}
     $$

     辛内积为 $0$，故 $P_1$ 与 $P_2$ **对易**（$P_1 P_2 = +P_2 P_1$）。
   - **结论与边界回验**：利用 $XY = +iZ$、$YX = -iZ$ 与 $Z^2 = I$ 逐位展开两种乘序：

     $$
     P_1 P_2 = (X_0 Y_0)\otimes(Y_1 X_1)\otimes(Z_2 Z_2) = (i Z_0)\otimes(-i Z_1)\otimes I_2 = +Z_0 Z_1 I_2,
     $$

     $$
     P_2 P_1 = (Y_0 X_0)\otimes(X_1 Y_1)\otimes(Z_2 Z_2) = (-i Z_0)\otimes(i Z_1)\otimes I_2 = +Z_0 Z_1 I_2.
     $$

     两式完全相等！原因在于第 $0$ 位和第 $1$ 位各产生一个负号，偶数个反对易位置使两个负号互相抵消。
   - **易错坑提醒**：多比特 Pauli 串的对易性看的是“单比特反对易位置的总数奇偶性”（模 $2$ 和），不能看到第 $0$ 位 $X_0 Y_0 = -Y_0 X_0$ 就草率断定整条串反对易。

2. **【计算】$\mathrm{CNOT}_{0\to 1}$ 共轭推导与相位修正公式的顺序核验**

   - **题意与约定**：记 $C = \mathrm{CNOT}_{0\to 1}$（控制位 $0$、目标位 $1$），由基础共轭规则 $C(X_0 I_1)C^\dagger = X_0 X_1$、$C(I_0 X_1)C^\dagger = I_0 X_1$、$C(Z_0 I_1)C^\dagger = Z_0 I_1$、$C(I_0 Z_1)C^\dagger = Z_0 Z_1$，逐一推导 $+X_0 Z_1$、$+Y_0 Y_1$ 与 $+X_0 Y_1$ 的共轭结果，对照相位修正公式 $r' = r \oplus [x_0 z_1 (x_1 \oplus z_0 \oplus 1)]$，并说明更新代码为何必须先用旧比特算完 $r'$。
   - **核心提示**：利用同态性 $C(P\cdot Q)C^\dagger=(C P C^\dagger)(C Q C^\dagger)$ 与 $Y=iXZ$，由四条基础 $\mathrm{CNOT}_{0\to 1}$ 生成元共轭规则推出复合 Pauli 串的像，并特别留心相乘顺序带来的正负号。
   - **完整分步演算**：利用 $Y = iXZ$、$XZ = -iY$ 及 $X^2 = Z^2 = I$ 逐项展开：

     $$
     \begin{aligned}
     C(+X_0 Z_1)C^\dagger &= (X_0 X_1)(Z_0 Z_1) = (X_0 Z_0)\otimes(X_1 Z_1) = (-iY_0)\otimes(-iY_1) = -Y_0 Y_1, \\
     C(+Y_0 Y_1)C^\dagger &= C\bigl((iX_0 Z_0)(iX_1 Z_1)\bigr)C^\dagger = -(X_0 X_1)(Z_0 I_1)(I_0 X_1)(Z_0 Z_1) = -(X_0 Z_0^2)\otimes(X_1^2 Z_1) = -X_0 Z_1, \\
     C(+X_0 Y_1)C^\dagger &= (X_0 X_1)\,i(I_0 X_1)(Z_0 Z_1) = (iX_0 Z_0)\otimes(X_1^2 Z_1) = +Y_0 Z_1.
     \end{aligned}
     $$

     再将三组旧比特 $(x_0, z_0, x_1, z_1)$（初值 $r = 0$）逐一代入相位公式与 $x_1' = x_1 \oplus x_0,\; z_0' = z_0 \oplus z_1$：
     - **$+X_0 Z_1$** $(1, 0, 0, 1)$：$x_0 z_1(x_1 \oplus z_0 \oplus 1) = 1\cdot 1\cdot(0 \oplus 0 \oplus 1) = 1 \implies r' = 1$（**变号**），新比特 $(x_0, z_0', x_1', z_1) = (1, 1, 1, 1) \leftrightarrow -Y_0 Y_1$；
     - **$+Y_0 Y_1$** $(1, 1, 1, 1)$：$x_0 z_1(x_1 \oplus z_0 \oplus 1) = 1\cdot 1\cdot(1 \oplus 1 \oplus 1) = 1 \implies r' = 1$（**变号**），新比特 $(1, 0, 0, 1) \leftrightarrow -X_0 Z_1$；
     - **$+X_0 Y_1$** $(1, 0, 1, 1)$：$x_0 z_1(x_1 \oplus z_0 \oplus 1) = 1\cdot 1\cdot(1 \oplus 0 \oplus 1) = 0 \implies r' = 0$（**不变号**），新比特 $(1, 1, 0, 1) \leftrightarrow +Y_0 Z_1$。

   - **结论与边界回验**：三种算符中只有 $+X_0 Z_1$ 与 $+Y_0 Y_1$ 变号，公式与直接展开 100% 吻合（`simulation_engines_lab.py` 全 $16$ 种双比特算符均已断言通过）。相位修正项里的 $x_1$ 与 $z_0$ 都是**更新前的旧比特**：如果在逐行赋值的代码里先把 `x1 ^= x0` 改写再立刻算 `r'`（此时 $z_0$ 尚未改写），那么在 $+X_0 Z_1$ 上 $x_1$ 从 $0$ 变 $1$、$x_1' \oplus z_0 \oplus 1 = 1\oplus 0\oplus 1 = 0$，会直接漏掉负号；同理先改 `z0` 再算 `r'` 也会让全部 $4$ 组 $x_0 = z_1 = 1$ 的情况符号全反。先统一读取旧值算出 $r'$、再就地更新 $x_1$ 和 $z_0$（与 $H/S$ 门保持一致的先相位后比特规范），才能彻底杜绝顺序覆写错误。
   - **易错坑提醒**：$S$ 门同样须先算 `r ^= x & z` 再改 `z ^= x`，否则 $+X \mapsto +Y$ 会错翻成 $-Y$。

3. **【进阶】去稳定子 $O(n^3) \to O(n^2)$ 降阶机制与 Stim 百万次采样加速原理**

   - **题意与约定**：对比仅存 $n$ 条稳定子、Aaronson–Gottesman 的 $2n$ 行去稳定子表以及 Stim（Gidney 2021）在确定性 $Z_a$ 测量与百万次含噪纠错采样中的算法复杂度和数据结构。
   - **核心提示**：思考没有去稳定子时为何确定性 $Z_a$ 测量需做 $O(n^3)$ 高斯消元求解线性组合系数，而维护共轭对偶的去稳定子表只需扫描与 $Z_a$ 反对易的去稳定子行即可在 $O(n^2)$ 内读出系数；再对比 Stim 一次参考态 + 批量泡利帧异或传播的机制。
   - **完整分步演算**：
     - **为何去稳定子把 $O(n^3)$ 压到 $O(n^2)$**：在确定性分支中，所有稳定子 $S_0,\dots,S_{n-1}$ 均与 $Z_a$ 对易（即第 $a$ 列稳定子区 $x_{\cdot, a}$ 全为 $0$），说明 $(-1)^m Z_a$ 必为稳定子生成元的唯一乘积：

       $$
       (-1)^m Z_a = \prod_{k=0}^{n-1} S_k^{c_k}, \qquad c_k \in \{0, 1\}.
       $$

       若只有 $n$ 条稳定子，要找二进制系数 $c_0,\dots,c_{n-1}$ 必须在 $\mathbb{F}_2$ 上对 $n\times n$ 矩阵做高斯消元，单次测量耗时 $O(n^3)$。引入配套的 $n$ 条去稳定子 $D_0,\dots,D_{n-1}$ 并维持三组辛不变量 $[D_i,D_j] = [S_i,S_j] = 0$、$D_i S_j = (-1)^{\delta_{ij}} S_j D_i$ 后，把上式两边同与 $D_j$ 做二元辛内积，因为 $D_j$ 仅与 $S_j$ 反对易，右边直接滤出单个未知数 $c_j$，左边恰好是 $\langle D_j, Z_a\rangle_{\mathrm{sp}} = x_{j,a}$：

       $$
       c_j = \langle D_j, Z_a\rangle_{\mathrm{sp}} = x_{j,a} \qquad (j = 0, 1, \dots, n-1).
       $$

       无需任何消元！只需扫一遍去稳定子区的第 $a$ 列，对所有 $x_{j,a} = 1$ 的行在暂存行上调用至多 $n$ 次 `rowsum`（每次 $O(n)$），最后读出相位位 $r_{\mathrm{scratch}} = m$，总复杂度精确降至 $O(n^2)$。
     - **Stim 在百万次含噪纠错采样中为何快数个量级**：Stim 结合了三项核心优化：（1）追踪**逆稳定子表（inverse tableau）**，进一步将单次确定性测量渐近压至 $O(n)$；（2）采用 **256 位宽 SIMD** 缓存友好内存布局，一条 CPU 指令并行异或 $256$ 位；（3）最关键的是**参考样本 + 批量 Pauli 帧传播（reference sample & Pauli frame simulation）**——对同一含随机 Pauli 噪声的纠错电路，昂贵的稳定子表**仅完整运行 $1$ 次**以生成无错参考测量串；后续数百万次含噪抽样不再操作 $O(n^2)$ 表格，而是仅把每次随机注入的轻量 2 比特/量子比特 Pauli 错误帧沿 Clifford 门按位异或推向测量端口，凡与测量算符反对易的错误帧就把对应参考比特取反，从而实现千赫兹级吞吐。
   - **结论与边界回验**：纯 Clifford 稳定子表在 `simulation_engines_lab.py` 的 4 比特随机中段测量压测中与态矢量误差 $< 10^{-14}$。其适用边界是噪声须为随机 Pauli/Clifford 信道，无法直接处理非 Clifford 相干旋转误差。
   - **易错坑提醒**：引入去稳定子使表格行数加倍（空间仍为 $O(n^2)$），单门更新仍是 $O(n)$；去稳定子行并非稳定原态的算符，绝不可混进稳定子群生成元。

4. **【进阶】$T|0\rangle$ 与 $|T\rangle$ 的精确稳定子秩、$|T\rangle$ 的稳定子展度与 $|T\rangle^{\otimes 2}$ 的 2 项分解**

   - **题意与约定**：针对相位门 $T = \operatorname{diag}(1, e^{i\pi/4})$，分别确定 $T|0\rangle$ 与魔法态 $|T\rangle = T|+\rangle = \frac{|0\rangle + e^{i\pi/4}|1\rangle}{\sqrt{2}}$ 的精确稳定子秩 $\chi_{\mathrm{stab}}$，推导 $|T\rangle$ 在非正交稳定子态 $\{|+\rangle, |+i\rangle\}$ 下的稳定子展度 $\xi(|T\rangle)$，并显式验证 $|T\rangle^{\otimes 2}$ 的 2 项纠缠稳定子分解。
   - **核心提示**：先检验 $T|0\rangle$ 与 $|0\rangle$ 是否仅差全局相位以定其稳定子秩；对 $|T\rangle$ 证其非稳定子态并显式写成两个稳定子态之和得 $\chi_{\mathrm{stab}}=2$，再算 $l_1$ 范数平方求展度 $\xi$，并用 Clifford 态分解写出 $|T\rangle^{\otimes 2}$ 的两项最优展开。
   - **完整分步演算**：
     - **单份稳定子秩**：$T|0\rangle = |0\rangle$ 由 $+Z$ 稳定，本身就是稳定子态，故 $\chi_{\mathrm{stab}}(T|0\rangle) = 1$。对于 $|T\rangle = \frac{|0\rangle + e^{i\pi/4}|1\rangle}{\sqrt{2}}$，其 Bloch 坐标为 $\bigl(\cos\frac{\pi}{4}, \sin\frac{\pi}{4}, 0\bigr) = \bigl(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0\bigr)$，不在 $6$ 个稳定子极点 $(\pm 1,0,0), (0,\pm 1,0), (0,0,\pm 1)$ 上，故 $\chi_{\mathrm{stab}}(|T\rangle) \ge 2$；又它可直接拆为 $|T\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{e^{i\pi/4}}{\sqrt{2}}|1\rangle$（两项均为稳定子态），因此精确稳定子秩 $\chi_{\mathrm{stab}}(|T\rangle) = 2$。
     - **赤道非正交分解与稳定子展度**：取 $|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}$、$|+i\rangle = \frac{|0\rangle+i|1\rangle}{\sqrt{2}}$ 及系数 $c_1 = \frac{e^{i\pi/8}}{2\cos(\pi/8)}$、$c_2 = \frac{e^{-i\pi/8}}{2\cos(\pi/8)}$，逐分量核验 $c_1|+\rangle + c_2|+i\rangle$（注意 $i e^{-i\pi/8} = e^{i(\pi/2-\pi/8)} = e^{i 3\pi/8}$）：

       $$
       \begin{aligned}
       |0\rangle\text{ 分量：} &\quad \frac{e^{i\pi/8} + e^{-i\pi/8}}{2\sqrt{2}\cos(\pi/8)} = \frac{2\cos(\pi/8)}{2\sqrt{2}\cos(\pi/8)} = \frac{1}{\sqrt{2}}, \\
       |1\rangle\text{ 分量：} &\quad \frac{e^{i\pi/8} + e^{i 3\pi/8}}{2\sqrt{2}\cos(\pi/8)} = \frac{e^{i\pi/4}(e^{-i\pi/8} + e^{i\pi/8})}{2\sqrt{2}\cos(\pi/8)} = \frac{e^{i\pi/4}}{\sqrt{2}}.
       \end{aligned}
       $$

       两分量与 $|T\rangle$ 精确相等！因 $|c_1| = |c_2| = \frac{1}{2\cos(\pi/8)}$，得最小 $\ell_1$ 范数平方——稳定子展度：

       $$
       \xi(|T\rangle) = \bigl(|c_1| + |c_2|\bigr)^2 = \frac{1}{\cos^2(\pi/8)} = \frac{2}{1 + \cos(\pi/4)} = \frac{4}{2 + \sqrt{2}} = 4 - 2\sqrt{2} \approx 1.171573.
       $$

       以 $2$ 为底换算为 $\log_2\xi(|T\rangle) \approx 0.228447$，远小于正交计算基分解的 $(\frac{1}{\sqrt{2}}+\frac{1}{\sqrt{2}})^2 = 2$。
     - **两份魔法态的 2 项分解**：将 $|T\rangle^{\otimes 2}$ 在大端序下展开（利用 $(e^{i\pi/4})^2 = e^{i\pi/2} = i$）并按奇偶宇称重组：

       $$
       \begin{aligned}
       |T\rangle^{\otimes 2}
       &= \frac{1}{2}\bigl(|00\rangle + e^{i\pi/4}|01\rangle + e^{i\pi/4}|10\rangle + i|11\rangle\bigr) \\
       &= \frac{1}{\sqrt{2}}\underbrace{\left(\frac{|00\rangle + i|11\rangle}{\sqrt{2}}\right)}_{|\psi_i\rangle}
        + \frac{e^{i\pi/4}}{\sqrt{2}}\underbrace{\left(\frac{|01\rangle + |10\rangle}{\sqrt{2}}\right)}_{|\Psi^+\rangle}.
       \end{aligned}
       $$

       核验两个基底都是 2 比特稳定子态：$X_0 Y_1 |\psi_i\rangle = \frac{i|11\rangle + i(-i)|00\rangle}{\sqrt{2}} = +|\psi_i\rangle$ 且 $Z_0 Z_1|\psi_i\rangle = +|\psi_i\rangle$，故 $|\psi_i\rangle$ 由 $\langle +X_0 Y_1, +Z_0 Z_1\rangle$ 稳定；$|\Psi^+\rangle$ 由 $\langle +X_0 X_1, -Z_0 Z_1\rangle$ 稳定。于是 $\chi_{\mathrm{stab}}(|T\rangle^{\otimes 2}) = 2 < 2^2 = 4$！
   - **结论与边界回验**：仅靠 2 份打包就立刻把 $t$ 份魔法态的精确稳定子秩上界从朴素 $2^t$ 压半至 $2^{t/2} = 2^{0.5 t}$；把更多份打包进纠缠稳定子态后，Bravyi–Gosset（2016）给出 6 份 7 项（$7^{t/6} \approx 2^{0.468 t}$）及按 $\xi(|T\rangle)^t \approx 2^{0.228 t}$ 标度的近似弱采样，Qassim–Pashayan–Gosset（2021）进一步将精确秩指数压至 $O(2^{0.396 t})$（数值均与 `simulation_engines_lab.py` 吻合）。
   - **易错坑提醒**：别以为电路里每出现 1 个 $T$ 门模拟代价就必然翻倍——作用在 $Z$ 本征态上的 $T$ 门不产生任何魔术度，而多份魔法态还可借纠缠稳定子态压缩秩与展度。

5. **【基础】$\mathrm{SWAP}$ 门破坏匹配门条件与两大经典可解孤岛的破壁资源**

   - **题意与约定**：按大端序计算基 $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ 写出 2 比特 $\mathrm{SWAP}$ 门矩阵，对照匹配门定义 $G(A, B)$（$A, B \in \mathrm{U}(2)$ 分别作用在偶宇称子空间 $\{|00\rangle, |11\rangle\}$ 与奇宇称子空间 $\{|01\rangle, |10\rangle\}$，且 $\det A = \det B$）检验行列式，并归纳打破匹配门孤岛与连续变量高斯孤岛的破壁资源。
   - **核心提示**：在大端序下写出 $\mathrm{SWAP}$ 矩阵，提取偶宇称块 $A$（对应 $|00\rangle,|11\rangle$）与奇宇称块 $B$（对应 $|01\rangle,|10\rangle$）分别计算行列式对比 $\det A$ 与 $\det B$；再指明打破匹配门与高斯孤岛所需的破壁资源。
   - **完整分步演算**：写出 $\mathrm{SWAP}$ 矩阵并提取偶、奇宇称两个 $2\times 2$ 子块：

     $$
     \mathrm{SWAP} = \begin{bmatrix}
     1 & 0 & 0 & 0 \\
     0 & 0 & 1 & 0 \\
     0 & 1 & 0 & 0 \\
     0 & 0 & 0 & 1
     \end{bmatrix}
     \quad\Longrightarrow\quad
     A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix},\;\;
     B = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}.
     $$

     分别计算行列式：

     $$
     \det A = 1\cdot 1 - 0\cdot 0 = +1, \qquad
     \det B = 0\cdot 0 - 1\cdot 1 = -1.
     $$

     因为 $\det A = +1 \ne -1 = \det B$，$\mathrm{SWAP}$ 门**不是**匹配门。
   - **结论与边界回验**：总结两类经典可模拟孤岛的表示规模与破壁资源：
     - **最近邻匹配门 / 自由费米子孤岛**：经 Jordan–Wigner 变换等价于仅含 Majorana 算符二次项的自由费米子演化，海森堡绘景下只需维护一张 $2n \times 2n$ 实正交矩阵 $R \in \mathrm{SO}(2n)$，经典 $O(n^3)$ 精确可解。**破壁资源**是打破一维最近邻拓扑限制——例如加入 $\mathrm{SWAP}$ 门（允许非最近邻作用）或引入四次费米子相互作用项——一旦跨出最近邻，立刻跃升为通用量子计算（Jozsa–Miyake 2008）。
     - **连续变量高斯 / 正 Wigner 孤岛**：$m$ 模高斯初态、高斯门与零差/外差测量只需以 $O(m^3)$ 追踪 $2m$ 维均值向量 $\mathbf{d}$ 与 $2m\times 2m$ 实协方差矩阵 $V$（受辛变换 $S \in \mathrm{Sp}(2m, \mathbb{R})$ 演化），更广义地 Wigner 函数处处非负的线路均可经典蒙特卡洛采样（Bartlett 等 2002；Mari–Eisert 2012）。**破壁资源**是**非高斯性与 Wigner 负性**，如单光子 Fock 态、立方相位门或 GKP 码态。
   - **易错坑提醒**：匹配门和高斯态都可以制造大量纠缠甚至任意连续角非 Clifford 旋转，但只要没有跨出各自代数封闭孤岛，纠缠本身并不能保证经典难算。

6. **【计算】3 比特态键 1 的矩阵乘积态（MPS）奇异值、键维与 $\chi' = 1$ 截断核算**

   - **题意与约定**：对 3 比特态 $|\psi\rangle = \frac{1}{\sqrt{2}}|000\rangle + \frac{1}{2}|011\rangle + \frac{1}{2}|111\rangle$（大端序 $|q_0 q_1 q_2\rangle$），写出键 1 切分 $(q_0 \mid q_1 q_2)$ 的 $2\times 4$ 矩阵 $\Psi^{[0\mid 12]}$，通过 Gram 矩阵 $G = \Psi^{[0\mid 12]}(\Psi^{[0\mid 12]})^\dagger$ 的本征值求非零奇异值 $\sigma_1, \sigma_2$、键维 $\chi_1$，以及截断至 $\chi' = 1$ 的平方误差 $\epsilon_{\mathrm{trunc}}$ 与重归一化根保真度 $F$。
   - **核心提示**：按键 $1$（左 $q_0$、右 $q_1 q_2$）把 3 比特态系数重排成 $2\times 4$ 矩阵 $M$，计算 $M M^\dagger$ 的本征值并开根号得全部奇异值 $\{s_k\}$ 与精确键维 $\chi$，再仅保留最大奇异值 $s_1$ 算 $\chi'=1$ 截断保真度平方 $s_1^2$。
   - **完整分步演算**：先核验态归一化：$(\frac{1}{\sqrt{2}})^2 + (\frac{1}{2})^2 + (\frac{1}{2})^2 = \frac{1}{2} + \frac{1}{4} + \frac{1}{4} = 1$。按行指标 $s_0 \in \{0, 1\}$、列指标 $s_1 s_2 \in \{00, 01, 10, 11\}$ 重排为 $2\times 4$ 矩阵：

     $$
     \Psi^{[0\mid 12]} = \begin{bmatrix}
     \frac{1}{\sqrt{2}} & 0 & 0 & \frac{1}{2} \\
     0 & 0 & 0 & \frac{1}{2}
     \end{bmatrix}.
     $$

     逐格计算 $2\times 2$ 实对称半正定矩阵 $G = \Psi^{[0\mid 12]}(\Psi^{[0\mid 12]})^\dagger$（即约化密度矩阵 $\rho_0$）：

     $$
     G = \begin{bmatrix}
     \frac{1}{\sqrt{2}} & 0 & 0 & \frac{1}{2} \\
     0 & 0 & 0 & \frac{1}{2}
     \end{bmatrix}
     \begin{bmatrix}
     \frac{1}{\sqrt{2}} & 0 \\
     0 & 0 \\
     0 & 0 \\
     \frac{1}{2} & \frac{1}{2}
     \end{bmatrix}
     = \begin{bmatrix}
     \frac{1}{2} + \frac{1}{4} & \frac{1}{4} \\
     \frac{1}{4} & \frac{1}{4}
     \end{bmatrix}
     = \begin{bmatrix}
     \frac{3}{4} & \frac{1}{4} \\
     \frac{1}{4} & \frac{1}{4}
     \end{bmatrix}.
     $$

     计算迹 $\operatorname{Tr}(G) = \frac{3}{4} + \frac{1}{4} = 1$、行列式 $\det(G) = \frac{3}{4}\cdot\frac{1}{4} - \frac{1}{4}\cdot\frac{1}{4} = \frac{2}{16} = \frac{1}{8}$，写出特征方程并求根：

     $$
     \lambda^2 - \lambda + \frac{1}{8} = 0
     \quad\Longrightarrow\quad
     \lambda_{1,2} = \frac{1 \pm \sqrt{1 - 4\cdot\frac{1}{8}}}{2} = \frac{1 \pm \frac{1}{\sqrt{2}}}{2} = \frac{2 \pm \sqrt{2}}{4}.
     $$

     数值为 $\lambda_1 \approx 0.853553$、$\lambda_2 \approx 0.146447$，两个本征值均严格大于 $0$，故**键维 $\chi_1 = 2$**，两个非零奇异值为（注意利用半角恒等式 $\cos^2\frac{\pi}{8} = \frac{2+\sqrt{2}}{4}$）：

     $$
     \sigma_1 = \sqrt{\lambda_1} = \sqrt{\frac{2 + \sqrt{2}}{4}} = \cos\frac{\pi}{8} \approx 0.923880, \qquad
     \sigma_2 = \sqrt{\lambda_2} = \sqrt{\frac{2 - \sqrt{2}}{4}} = \sin\frac{\pi}{8} \approx 0.382683.
     $$

     在键 1 强行截断至 $\chi' = 1$（舍弃较小奇异值 $\sigma_2$），由 Eckart–Young–Mirsky 定理与重归一化公式：

     $$
     \epsilon_{\mathrm{trunc}} = \sigma_2^2 = \frac{2 - \sqrt{2}}{4} \approx 0.146447, \qquad
     F = \sqrt{1 - \epsilon_{\mathrm{trunc}}} = \sigma_1 = \sqrt{\frac{2 + \sqrt{2}}{4}} \approx 0.923880.
     $$

   - **结论与边界回验**：$\sigma_1^2 + \sigma_2^2 = \frac{2+\sqrt{2}}{4} + \frac{2-\sqrt{2}}{4} = 1$；平方重叠 $F^2 = 1 - \epsilon_{\mathrm{trunc}} \approx 0.853553$。调用 `simulation_engines_lab.py` 的 `MPS3.from_statevector` 与 `truncate_bond1` 独立复算，结果精确吻合至小数点后 $15$ 位。
   - **易错坑提醒**：$G = \Psi\Psi^\dagger$ 的本征值是奇异值的**平方** $\sigma_i^2$ 而非 $\sigma_i$ 本身；截断平方误差 $\epsilon_{\mathrm{trunc}}$ 等于被舍弃的 $\sigma_i^2$ 之和，而全书统一的根保真度 $F$ 是 $\sqrt{1 - \epsilon_{\mathrm{trunc}}}$（还要再开一次根号）。

7. **【基础】非稳定子态 $|W_3\rangle$ 为何仅需 $\chi = 2$，以及 468 个 $T$ 门一维砖墙电路为何被张量网络击穿**

   - **题意与约定**：解释非稳定子态 $|W_3\rangle = \frac{1}{\sqrt{3}}(|100\rangle + |010\rangle + |001\rangle)$ 的 MPS 键维为何仅为 $\chi = 2$，并结合 2026 年 Manabe–Gu–Pan（`arXiv:2608.13110`，预印本）的 37.3 分钟复算战例剖析单比特 $T$ 门数量与张量网络复杂度的正交性。
   - **核心提示**：对 $|W_3\rangle$ 沿任意一维切割把态写成两项 Schmidt 展开证明 $\chi=2$（即便非稳定子）；再据此说明为何高 $T$-count 并不保证一维短程纠缠电路难模拟——张量网络只看切割纠缠熵而非 $T$ 门数量。
   - **完整分步演算**：
     - **$|W_3\rangle$（及任意 $|W_n\rangle$）键维恒为 $\chi = 2$ 的根源**：将比特链在任意一条键 $(q_0\cdots q_{k-1} \mid q_k\cdots q_{n-1})$ 处一刀剪断，$|W_n\rangle$ 中恰有一个 `1` 的约束使所有非零比特串自动落入两个正交扇区：左半侧已出现 `1`（右侧必全为 `0`），或左半侧全为 `0`（右侧处于归一化态 $|W_{n-k}\rangle$）：

       $$
       |W_n\rangle = \sqrt{\frac{k}{n}}\,|W_k\rangle_{\text{左}}\otimes|0\cdots 0\rangle_{\text{右}} + \sqrt{\frac{n-k}{n}}\,|0\cdots 0\rangle_{\text{左}}\otimes|W_{n-k}\rangle_{\text{右}}.
       $$

       虚拟键只需 2 个内部状态来传递“左侧是否已经出现过 `1`”这 1 比特计数信息，因此对任意 $n$（包括 $n=3$，其键 1 奇异值为 $\sqrt{2/3},\sqrt{1/3}$）Schmidt 秩严格等于 $\chi = 2$，尽管 $|W_3\rangle$ 带非零魔术度、不属于稳定子态。
     - **为何 468 个 $T$ 门挡不住时空张量网络**：IBM 与芝加哥大学的掺杂 Clifford 采样实验在 $70$ 个逻辑比特、深度 $70$ 上掺入了 $468$ 个非 Clifford $T$ 门，扩展稳定子引擎确实彻底失效（$2^{0.396 \times 468} \approx 6.2 \times 10^{55}$）。但该线路的纠缠门排布在**一维开放边界砖墙拓扑**上，所有双比特门的算符 Schmidt 秩均为 $2$。改用确定性**时空边界张量网络收缩**时，**任意单比特门（包括全部 $468$ 个 $T$ 门）都可以直接乘进相邻的格点或键张量中无损吸收，完全不增加虚拟键维或张量网收缩树宽**！Manabe–Gu–Pan 团队仅用 $256$ 张 H100 GPU 耗时 $37.3$ 分钟就算出了全部 $2{,}051$ 个公开比特串的精确振幅。
   - **结论与边界回验**：非 Clifford 魔术度（对付稳定子引擎）与高维体积律纠缠拓扑（对付张量网络引擎）是两把相互正交的尺子，单把某一维堆得再高，只要另一维留有结构缺口，就会被对应经典引擎从侧翼击穿。
   - **易错坑提醒**：在 MPS 或张量网络模拟中，单比特门（哪怕是任意非 Clifford 旋转或 $T$ 门）永远只做局部指标收缩、不增加键维；真正推高键维的是跨切面的深层双比特纠缠门。

8. **【计算】退极化信道海森堡伴随 $\mathcal{D}_p^\dagger$ 推导、$(1 - p)^w$ 标度与随机 Pauli 参数 $q$ 换算**

   - **题意与约定**：按全书主定义，单比特退极化信道为 $\mathcal{D}_p(\rho) = (1 - p)\rho + p\frac{I}{2}$（$0 \le p \le 1$），由迹内积恒等式 $\operatorname{Tr}[O\,\mathcal{D}_p(\rho)] = \operatorname{Tr}[\mathcal{D}_p^\dagger(O)\,\rho]$ 导出 $\mathcal{D}_p^\dagger$ 对 $\{I, X, Y, Z\}$ 及 $n$ 比特 Pauli 串的作用，并换算为随机 Pauli 形式 $\widetilde{\mathcal{D}}_q(\rho) = (1 - q)\rho + \frac{q}{3}(X\rho X + Y\rho Y + Z\rho Z)$。
   - **核心提示**：利用迹内积恒等式 $\operatorname{Tr}(O\,\mathcal D_p(\rho))=\operatorname{Tr}(\mathcal D_p^\dagger(O)\,\rho)$ 求出退极化伴随映射作用在 $I$ 与非单位 Pauli 上的缩放因子，推广到 $n$ 比特权重为 $w$ 的 Pauli 串，再代入 $q=3p/4$ 核对换算。
   - **完整分步演算**：对任意单比特算符 $O$ 与密度矩阵 $\rho$（$\operatorname{Tr}\rho = 1$）展开左边迹：

     $$
     \operatorname{Tr}\bigl[O\,\mathcal{D}_p(\rho)\bigr]
     = (1 - p)\operatorname{Tr}(O\rho) + \frac{p}{2}\operatorname{Tr}(O)\operatorname{Tr}(\rho)
     = \operatorname{Tr}\!\left[\left((1 - p)O + \frac{p}{2}\operatorname{Tr}(O)\,I\right)\rho\right].
     $$

     因对一切 $\rho$ 成立，直接读出伴随映射 $\mathcal{D}_p^\dagger(O) = (1 - p)O + \frac{p}{2}\operatorname{Tr}(O)\,I$。逐一代入四个 Pauli 矩阵（利用 $\operatorname{Tr}(I) = 2$，且 $\operatorname{Tr}(X) = \operatorname{Tr}(Y) = \operatorname{Tr}(Z) = 0$）：

     $$
     \mathcal{D}_p^\dagger(I) = (1 - p)I + \frac{p}{2}\cdot 2I = I, \qquad
     \mathcal{D}_p^\dagger(\sigma) = (1 - p)\sigma \quad (\sigma \in \{X, Y, Z\}).
     $$

     对 $n$ 比特并行退极化层 $\mathcal{D}_p^{\otimes n}$ 和任意 Pauli 串 $P = \bigotimes_{j=0}^{n-1} P_j$（记非恒等算符 $P_j \ne I$ 的个数为权重 $w = w(P)$），按张量积逐位作用：

     $$
     \bigl(\mathcal{D}_p^{\otimes n}\bigr)^\dagger(P)
     = \bigotimes_{j=0}^{n-1} \mathcal{D}_p^\dagger(P_j)
     = \left(\prod_{j:\, P_j \ne I}(1 - p)\right) \bigotimes_{j=0}^{n-1} P_j
     = (1 - p)^w\, P.
     $$

     最后建立与随机 Pauli 参数 $q$ 的精确换算：利用单比特恒等式 $\frac{I}{2} = \frac{1}{4}(\rho + X\rho X + Y\rho Y + Z\rho Z)$（对任意 $\operatorname{Tr}\rho = 1$ 的 $2\times 2$ 矩阵恒成立），把 $\mathcal{D}_p(\rho)$ 改写为

     $$
     \mathcal{D}_p(\rho) = \left(1 - \frac{3p}{4}\right)\rho + \frac{p}{4}\bigl(X\rho X + Y\rho Y + Z\rho Z\bigr).
     $$

     与 $\widetilde{\mathcal{D}}_q(\rho) = (1 - q)\rho + \frac{q}{3}(X\rho X + Y\rho Y + Z\rho Z)$ 逐项对照得 $q = \frac{3}{4}p \iff p = \frac{4}{3}q$，故对应的权重 $w$ 衰减因子为

     $$
     \bigl(\widetilde{\mathcal{D}}_q^{\otimes n}\bigr)^\dagger(P) = \left(1 - \frac{4}{3}q\right)^w P.
     $$

   - **结论与边界回验**：检验完全退极化点 $p = 1 \iff q = 3/4$：此时 $1 - \frac{4}{3}q = 0$，所有 $w \ge 1$ 的非平凡 Pauli 串均归零，仅留 $\mathcal{D}_1^\dagger(I) = I$，保单位性成立；另外 $\mathcal{D}_p^\dagger(O) = \mathcal{D}_p(O)$（退极化信道自伴），与 `simulation_engines_lab.py` 代码完全一致。
   - **易错坑提醒**：海森堡伴随 $\mathcal{D}_p^\dagger$ 绝不是退极化信道的逆映射 $\mathcal{D}_p^{-1}$——它把高权重串乘上缩小因子 $(1-p)^w$ 而非放大因子 $(1-p)^{-w}$，因此物理噪声越大，高权重分支死得越快，经典稀疏 Pauli 传播越容易截断。

9. **【计算】2 比特 2 层含噪 Pauli 传播反向树（$\theta = \pi/3,\; p = 0.1$）零跳步核算**

   - **题意与约定**：初态 $|\psi_0\rangle = |0+\rangle$，重复 $2$ 层含噪电路 $\mathcal{L} = \mathcal{D}_p^{\otimes 2} \circ \mathcal{U}_{R_x(\theta)_0 \otimes R_x(\theta)_1} \circ \mathcal{U}_{\mathrm{CNOT}_{0\to 1}}$，末态观测 $O^{(2)} = Z_0 I_1$。取 $\theta = \pi/3$（$60^\circ$）与 $p = 0.1$，零跳步计算精确期望值、在第 1 层噪声后执行 $w \le 1$ 截断的近似值、真实误差及算符范数上界。
   - **核心提示**：从末端观测量 $O=Z_0 I_1$ 出发在海森堡绘景**倒序**穿过每层噪声（乘 $(1-p)^w$）、双比特门与单比特旋转（按 $R^\dagger P R=\cos\theta\,P\pm\sin\theta\,Q$ 分裂分支），逐层保留权重并最终对初态 $|0+\rangle$ 求期望。
   - **完整分步演算**：先记 $\eta = 1 - p = 0.9$、$c = \cos\frac{\pi}{3} = \frac{1}{2}$、$s = \sin\frac{\pi}{3} = \frac{\sqrt{3}}{2}$（故 $c^2 = \frac{1}{4} = 0.25,\; s^2 = \frac{3}{4} = 0.75$）。从 $O^{(2)} = Z_0 I_1$ 严格按逆门序倒推两层：
     - **倒推第 2 层**：
       1) 过噪声伴随 $(\mathcal{D}_p^{\otimes 2})^\dagger$（权重 $w = 1$）：$Z_0 I_1 \mapsto \eta\, Z_0 I_1$；
       2) 过 $R_x(\theta)^{\otimes 2\,\dagger}$（$Z_0 \mapsto c Z_0 + s Y_0,\; I_1 \mapsto I_1$）：得 $\eta c\, Z_0 I_1 + \eta s\, Y_0 I_1$；
       3) 过 $\mathrm{CNOT}_{0\to 1}^\dagger$（$Z_0 I_1 \mapsto Z_0 I_1,\; Y_0 I_1 \mapsto Y_0 X_1$）：得 $O^{(1)} = \eta c\, Z_0 I_1 + \eta s\, Y_0 X_1$。
     - **倒推第 1 层**：
       1) 过第 1 层噪声伴随（$Z_0 I_1$ 权重 $w=1$ 乘 $\eta$，$Y_0 X_1$ 权重 $w=2$ 乘 $\eta^2$）：

          $$
          O^{(1)} \xrightarrow{(\mathcal{D}_p^{\otimes 2})^\dagger} \eta^2 c\, Z_0 I_1 + \eta^3 s\, Y_0 X_1.
          $$

       2) **精确分支继续倒推**：过 $R_x^\dagger$ 得 $\eta^2 c^2 Z_0 I_1 + \eta^2 cs Y_0 I_1 + \eta^3 cs Y_0 X_1 - \eta^3 s^2 Z_0 X_1$；再过 $\mathrm{CNOT}^\dagger$ 得初态前算符

          $$
          O^{(0)} = \eta^2 c^2 Z_0 I_1 + \eta^2 cs Y_0 X_1 + \eta^3 cs Y_0 I_1 - \eta^3 s^2 Z_0 X_1.
          $$

       3) **在初态 $|0+\rangle$ 上求期望**（$\langle ZI\rangle = \langle ZX\rangle = +1,\; \langle YX\rangle = \langle YI\rangle = 0$）：

          $$
          \langle Z_0 I_1\rangle_{\mathrm{exact}}
          = \eta^2 c^2 - \eta^3 s^2
          = 0.9^2 \times 0.25 - 0.9^3 \times 0.75
          = 0.81 \times 0.25 - 0.729 \times 0.75
          = 0.2025 - 0.54675 = -0.34425.
          $$

     - **第 1 层噪声后执行 $w \le 1$ 权重截断**：裁掉权重 $w = 2$ 的分支 $\eta^3 s\, Y_0 X_1$，仅保留 $\eta^2 c\, Z_0 I_1$，继续过第 1 层 $R_x^\dagger$ 与 $\mathrm{CNOT}^\dagger$ 得 $O_{\mathrm{trunc}}^{(0)} = \eta^2 c^2 Z_0 I_1 + \eta^2 cs Y_0 X_1$，在 $|0+\rangle$ 上求期望与误差核算：

       $$
       \langle Z_0 I_1\rangle_{\mathrm{trunc}} = \eta^2 c^2 = 0.2025, \qquad
       \bigl|\langle Z_0 I_1\rangle_{\mathrm{exact}} - \langle Z_0 I_1\rangle_{\mathrm{trunc}}\bigr| = |-0.34425 - 0.2025| = 0.54675,
       $$

       $$
       \text{算符范数误差上界：}\; \bigl|\eta^3 s\bigr| = (1 - p)^3\sin\frac{\pi}{3} = 0.729 \times \frac{\sqrt{3}}{2} \approx 0.631333.
       $$

   - **结论与边界回验**：独立运行 `simulation_engines_lab.py` 的 $4\times 4$ 密度矩阵正向演化得 `-0.34425000`（残差 $1.11\times 10^{-16}$），且不等式 $0.54675 \le 0.631333$ 严格成立。同时注意这组大角度（$60^\circ$）+ 较弱噪声（$p=0.1$）参数：激进的 $w \le 1$ 截断不仅误差巨大，甚至把期望值的**正负号都算反了**（$+0.2025$ 对 $-0.34425$），说明低噪声、大角度线路必须保留更高权重。
   - **易错坑提醒**：$R_x(\theta)^\dagger Y R_x(\theta) = c Y - s Z$ 带有**负号**，正是它导致第二项成为 $-\eta^3 s^2 Z_0 X_1$；手算海森堡方向 $U^\dagger P U$ 时务必核对正负号，切勿和薛定谔方向 $U P U^\dagger$ 混淆。

10. **【进阶】80 比特一维链含噪线路诊断与“四维量子优势边界”**

    - **题意与约定**：审评一条 $n = 80$ 比特、深度 $d = 40$、含 $t = 600$ 个 $T$ 门、开放一维链拓扑、平均双比特门退极化率 $p \approx 0.02$ 且仅输出单比特期望值 $\langle Z_j\rangle$ 的线路，对照“四维量子优势边界”定位全部暴露的经典模拟引擎，并阐明容错量子纠错（FTQC）的不可替代性。
    - **核心提示**：对照“四维量子优势边界”（大比特数/高非稳定子资源/高二维纠缠结构/极低物理噪声），逐一诊断该宣称中“开放一维链（MPS 友好）”与“$p\approx 0.02$ 深度 $40$（Pauli 传播指数衰减）”两处致命缺口。
    - **完整分步演算**：按“四维边界”逐关排查：
      - **维度一（比特规模 $n = 80 > 45$）**：通过。稠密态矢量需要 $16 \times 2^{80}\,\mathrm{B}$ 内存，无法直接存储。
      - **维度二（魔术度 $t = 600$ 个 $T$ 门）**：通过。纯稳定子表与扩展稳定子（$2^{0.396 \times 600} \gg 10^{70}$）均无法硬算。
      - **维度三（拓扑与纠缠结构）——彻底失守！** 芯片比特连成**开放一维链**，深度仅 $40$，直接落入 **1D MPS 与确定性时空边界张量网络**的射程！正如第 5.5 节 2026 年 Manabe–Gu–Pan 复算 $70$ 比特深度 $70$ 含 $468$ 个 $T$ 门的一维砖墙线路所证实，所有 $600$ 个单比特 $T$ 门都会被无损吸收进局域张量，沿空间或时间边界收缩即可精确算穿。
      - **维度四（物理噪声 $p \approx 0.02$ 与局域观测量）——同时失守！** 线路仅报告单比特局域期望值 $\langle Z_j\rangle$，且每层伴随高达 $p \approx 0.02$ 的退极化噪声，直接落入 **海森堡 Pauli 传播 / 稀疏 Pauli 动力学（SPD）** 的射程！权重为 $w$ 的高阶 Pauli 串每过一层即乘以 $(1-p)^w \approx 0.98^w$（如 $w = 15$ 经 $20$ 层后衰减至 $0.98^{300} \approx 2.3 \times 10^{-3}$），绝大部分长程高权重关联早已被噪声绞杀，稀疏截断即可在经典多项式时间内高精度复现 $\langle Z_j\rangle$。
    - **结论与边界回验**：跨过全部四道边界离不开容错量子纠错——裸物理（NISQ）芯片被锁死在深度与噪声的“剪刀差”里，做浅则纠缠光锥打不开，被张量网络击穿；做深则每层 $(1-p)^w$ 累积衰减把高权重干涉清零，被 SPD 击穿（而误差缓解 QEM 的采样开销随总噪声量指数爆炸，撑不起大深度）。只有把物理错误率压过纠错阈值后，靠量子纠错随码距 $d$ 指数压低逻辑错误率至 $p_L \ll 1/G$（守住维度四），同时在二维/高维拓扑上借晶格手术与魔法态蒸馏/培育运行海量逻辑 $T$ 门并维持深度体积律纠缠（同时守住维度一、二、三），才能真正进入容错级量子优势候选区。
    - **易错坑提醒**：即使同时跨过上述四维经典模拟边界，也只是量子优势的**必要条件而非充分条件**——实用优势还必须打赢该应用领域专属的经典启发式算法，并经受端到端验证与真实墙钟时间检验。

## 量子力学 Q1

1. **【基础】复态矢归一化与路径测量概率**

   - **题意与约定**：给定二维路径基 $\{|0\rangle, |1\rangle\}$ 下的未归一化向量 $|v\rangle = (1 + i)|0\rangle + \sqrt{2}\,|1\rangle$，先按左共轭内积 $\langle v|v\rangle = \sum_j |v_j|^2$ 求范数并归一化，再由 Born 规则算两路概率。
   - **核心提示**：先逐项求两复分量的模平方 $|1+i|^2$ 与 $|\sqrt{2}|^2$ 并相加开根号得范数，再用范数除原向量完成归一化，最后按 Born 规则求两路径概率并核对总和为 $1$。
   - **完整分步演算**：逐项计算各分量模平方（实部平方加虚部平方）：

     $$
     \langle v|v\rangle = |1 + i|^2 + |\sqrt{2}|^2 = (1^2 + 1^2) + 2 = 4
     \quad\Longrightarrow\quad
     \|v\| = \sqrt{4} = 2.
     $$

     除以范数 $2$ 得归一化态矢与两路概率：

     $$
     |\psi\rangle = \frac{1 + i}{2}|0\rangle + \frac{\sqrt{2}}{2}|1\rangle = \frac{1 + i}{2}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle,
     $$

     $$
     p(0) = \left|\frac{1 + i}{2}\right|^2 = \frac{1^2 + 1^2}{4} = \frac{1}{2}, \qquad
     p(1) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}.
     $$

   - **结论与边界回验**：概率均为非负实数且 $p(0) + p(1) = \frac{1}{2} + \frac{1}{2} = 1$。
   - **易错坑提醒**：概率由复振幅的模平方 $|a|^2 = a^* a$ 给出，绝不可用普通复数平方 $(1+i)^2/4 = i/2$ 替代。

2. **【计算】Mach–Zehnder 干涉仪矩阵推导、$|1\pm e^{i\phi}|^2$ 展开与 $\phi = \pi/3$ 核验**

   - **题意与约定**：采用本章平衡分束器 $B = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}$ 与下路径相位片 $U_\phi = \begin{bmatrix}1 & 0\\ 0 & e^{i\phi}\end{bmatrix}$（$\phi \in \mathbb{R}$），从端口 $0$ 初态 $|0\rangle = [1, 0]^T$ 出发，按从右向左顺序计算 $B U_\phi B|0\rangle$ 并核验 $\phi = \pi/3$。
   - **核心提示**：严格按矩阵从右向左次序依次计算 $B|0\rangle$、$U_\phi(B|0\rangle)$ 与 $B(U_\phi B|0\rangle)$，再用复数模平方展开公式 $|1\pm e^{i\phi}|^2=2\pm 2\cos\phi$ 化简两输出概率并代入 $\phi=\pi/3$ 核验。
   - **完整分步演算**：逐级按行展开矩阵乘法：

     $$
     B|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}\begin{bmatrix}1\\ 0\end{bmatrix} = \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix},
     \qquad
     U_\phi B|0\rangle = \begin{bmatrix}1 & 0\\ 0 & e^{i\phi}\end{bmatrix}\frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix} = \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ e^{i\phi}\end{bmatrix},
     $$

     $$
     B U_\phi B|0\rangle
     = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}\frac{1}{\sqrt{2}}\begin{bmatrix}1\\ e^{i\phi}\end{bmatrix}
     = \frac{1}{2}\begin{bmatrix}1 + e^{i\phi}\\ 1 - e^{i\phi}\end{bmatrix}.
     $$

     由此读出两个输出振幅 $A_0 = \frac{1 + e^{i\phi}}{2}$ 与 $A_1 = \frac{1 - e^{i\phi}}{2}$。一步不跳展开模平方 $|1 \pm e^{i\phi}|^2$（利用 $e^{-i\phi}e^{i\phi} = 1$ 与 $e^{i\phi} + e^{-i\phi} = 2\cos\phi$）：

     $$
     \begin{aligned}
     P_0 = |A_0|^2 &= \frac{|1 + e^{i\phi}|^2}{4} = \frac{(1 + e^{-i\phi})(1 + e^{i\phi})}{4} = \frac{1 + e^{i\phi} + e^{-i\phi} + 1}{4} = \frac{1 + \cos\phi}{2}, \\
     P_1 = |A_1|^2 &= \frac{|1 - e^{i\phi}|^2}{4} = \frac{(1 - e^{-i\phi})(1 - e^{i\phi})}{4} = \frac{1 - e^{i\phi} - e^{-i\phi} + 1}{4} = \frac{1 - \cos\phi}{2}.
     \end{aligned}
     $$

     代入 $\phi = \frac{\pi}{3}$（$\cos\frac{\pi}{3} = \frac{1}{2}$）：

     $$
     P_0 = \frac{1 + 1/2}{2} = \frac{3}{4}, \qquad
     P_1 = \frac{1 - 1/2}{2} = \frac{1}{4}, \qquad
     P_0 + P_1 = \frac{3}{4} + \frac{1}{4} = 1.
     $$

   - **结论与边界回验**：也可直接算复振幅 $A_0 = \frac{3 + i\sqrt{3}}{4}$、$A_1 = \frac{1 - i\sqrt{3}}{4}$，得 $|A_0|^2 = \frac{9+3}{16} = \frac{3}{4}$、$|A_1|^2 = \frac{1+3}{16} = \frac{1}{4}$，完全一致。
   - **易错坑提醒**：$U_\phi$ 夹在两块分束器中间，矩阵乘积须严格按“晚左早右”写成 $B U_\phi B$，切勿调换次序。

3. **【计算】路径记录、正交丢弃与部分重叠 $\gamma = 0.6$ 的输出概率**

   - **题意与约定**：粒子与路径记录装置经 $U_\phi$ 后处于联合态 $|\Psi\rangle = \frac{|0\rangle|d_0\rangle + e^{i\phi}|1\rangle|d_1\rangle}{\sqrt{2}}$，定义记录态重叠 $\gamma = \langle d_1|d_0\rangle$（$|\gamma| \le 1$），比较“无记录”“正交记录不读”与“实重叠 $\gamma = 0.6,\; \phi = 0$”三种实验。
   - **核心提示**：在粒子与路径探测器的联合态上对第二分束器作 $B\otimes I_d$，把末态按粒子路径 $|0\rangle,|1\rangle$ 整理后求模平方，观察干涉交叉项恰好乘上了探测器内积 $\operatorname{Re}(\gamma e^{i\phi})$，分别代入正交 $\gamma=0$ 与 $\gamma=0.6$。
   - **完整分步演算**：对记录自由度求偏迹（利用 $\operatorname{Tr}(|d_0\rangle\langle d_1|) = \langle d_1|d_0\rangle = \gamma$），得粒子在第二个分束器前的约化密度矩阵

     $$
     \rho_{\mathrm{path}}(\phi) = \frac{1}{2}\begin{bmatrix}1 & \gamma e^{-i\phi}\\ \gamma^* e^{i\phi} & 1\end{bmatrix}.
     $$

     送入 $B$ 后，由 $B^\dagger|0\rangle = |+\rangle$、$B^\dagger|1\rangle = |-\rangle$ 逐项展开输出概率：

     $$
     P_0(\phi) = \langle +|\rho_{\mathrm{path}}(\phi)|+\rangle = \frac{1 + \operatorname{Re}(\gamma e^{-i\phi})}{2}, \qquad
     P_1(\phi) = \langle -|\rho_{\mathrm{path}}(\phi)|-\rangle = \frac{1 - \operatorname{Re}(\gamma e^{-i\phi})}{2}.
     $$

     - **从未产生路径记录**：两路对应同一记录态，即 $\gamma = 1$，粒子保持纯态 $\frac{|0\rangle + e^{i\phi}|1\rangle}{\sqrt{2}}$，输出保留满幅干涉条纹 $P_0 = \frac{1+\cos\phi}{2}$、$P_1 = \frac{1-\cos\phi}{2}$。
     - **留下完全可区分的正交记录但不读**：$|d_0\rangle \perp |d_1\rangle \implies \gamma = 0$，非对角相干项清零，加上双臂等权 $1/2$ 给出最大混合态 $\rho_{\mathrm{path}} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{I}{2}$；经 $B$ 变换 $B(I/2)B^\dagger = I/2$，两端口对所有 $\phi$ 恒为 $P_0 = P_1 = \frac{1}{2}$，干涉彻底消失。
     - **实重叠 $\gamma = 0.6$ 且 $\phi = 0$**：$\operatorname{Re}(\gamma e^{0}) = 0.6$，代入得

       $$
       P_0 = \frac{1 + 0.6}{2} = 0.8, \qquad
       P_1 = \frac{1 - 0.6}{2} = 0.2.
       $$

   - **结论与边界回验**：$0.8 + 0.2 = 1$，条纹可见度 $\mathcal{V} = (0.8 - 0.2)/(0.8 + 0.2) = 0.6 = |\gamma|$。
   - **易错坑提醒**：决定干涉是否消失的是物理上是否留下了可区分的路径痕迹（即 $|\gamma|$ 大小），而非实验者主观上有没有去看读数。

4. **【计算】级联 Stern–Gerlach 实验计数与条件概率拆解**

   - **题意与约定**：$8000$ 个未偏振自旋-$1/2$ 原子依次通过“$SG_z$ 保留 $z+$”“$SG_x$ 保留 $x+$”“末级 $SG_z$ 测量 $z\pm$”三步，计算每步理想期望计数并指出条件概率。
   - **核心提示**：沿三级装置逐级乘以单级通过概率：未偏振束过第一级 $SG_z$ 取半，$|z+\rangle$ 过 $SG_x$ 保留 $|x+\rangle$ 再取半，最后 $|x+\rangle$ 过末级 $SG_z$ 等分；并区分无条件总占比与级联条件概率。
   - **完整分步演算**：
     - 第一步（未偏振束入 $SG_z$）：未偏振系综给出 $P(z+) = \frac{1}{2}$，留下 $8000 \times \frac{1}{2} = 4000$ 个处于 $|z+\rangle$ 的原子；
     - 第二步（$|z+\rangle$ 入 $SG_x$）：由 $|z+\rangle = \frac{|x+\rangle + |x-\rangle}{\sqrt{2}}$，条件概率 $P(x+ \mid z+) = |\langle x+|z+\rangle|^2 = \frac{1}{2}$，留下 $4000 \times \frac{1}{2} = 2000$ 个处于 $|x+\rangle$ 的原子；
     - 第三步（$|x+\rangle$ 入末级 $SG_z$）：由 $|x+\rangle = \frac{|z+\rangle + |z-\rangle}{\sqrt{2}}$，条件概率 $P(z\pm \mid x+) = |\langle z\pm|x+\rangle|^2 = \frac{1}{2}$，两出口各得

       $$
       N_{\mathrm{final}}(z+) = N_{\mathrm{final}}(z-) = 2000 \times \frac{1}{2} = 1000.
       $$

   - **结论与边界回验**：相对原始 $8000$ 束，每个最终出口的联合通过率为 $P(z+)P(x+\mid z+)P(z\pm\mid x+) = \frac{1}{2}\cdot\frac{1}{2}\cdot\frac{1}{2} = \frac{1}{8}$，而 $8000 \times \frac{1}{8} = 1000$。三个 $1/2$ 依次是以原始束、已筛出 $z+$ 与已筛出 $x+$ 为条件的条件概率。
   - **易错坑提醒**：切勿把第二步筛选后的 $z-$ 重新出现解释成“仪器把部分原子碰坏了”；$|x+\rangle$ 本身就是 $|z+\rangle$ 与 $|z-\rangle$ 的等权叠加，测 $X$ 抹去了原先确定的 $Z$ 信息。

5. **【计算】相干叠加 $|x+\rangle$ 与等权经典混合的 $X$ 基区分及密度矩阵**

   - **题意与约定**：在 $Z$ 基 $\{|z+\rangle, |z-\rangle\}$（即 $\{|0\rangle, |1\rangle\}$）中，对比纯叠加态 $|x+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ 与等权混合态（各 $1/2$ 概率处于 $|0\rangle$ 或 $|1\rangle$）。
   - **核心提示**：先在 $X$ 轴 Stern–Gerlach 装置下对比纯叠加态 $|x+\rangle$（确定单臂出射）与经典等权混合（双臂等分），再写出两者的 $2\times 2$ 密度矩阵，观察非对角相干元与纯度 $\operatorname{Tr}(\rho^2)$ 的区别。
   - **完整分步演算**：按密度矩阵定义 $\rho_{\mathrm{sup}} = |x+\rangle\langle x+|$ 与 $\rho_{\mathrm{mix}} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1|$ 写出 $2\times 2$ 矩阵：

     $$
     \rho_{\mathrm{sup}} = \frac{1}{2}\begin{bmatrix}1\\ 1\end{bmatrix}\begin{bmatrix}1 & 1\end{bmatrix} = \frac{1}{2}\begin{bmatrix}1 & 1\\ 1 & 1\end{bmatrix},
     \qquad
     \rho_{\mathrm{mix}} = \frac{1}{2}\begin{bmatrix}1 & 0\\ 0 & 0\end{bmatrix} + \frac{1}{2}\begin{bmatrix}0 & 0\\ 0 & 1\end{bmatrix} = \frac{1}{2}\begin{bmatrix}1 & 0\\ 0 & 1\end{bmatrix}.
     $$

     在 $Z$ 基下两者对角元均为 $(1/2, 1/2)$，统计完全相同；改在 $X$ 基 $\{|x+\rangle, |x-\rangle\}$ 测量：
     - 相干叠加：$p_{\mathrm{sup}}(x+) = \langle x+|\rho_{\mathrm{sup}}|x+\rangle = 1$，$p_{\mathrm{sup}}(x-) = 0$；
     - 经典混合：每个 $Z$ 本征态在 $X$ 基都给各半，故 $p_{\mathrm{mix}}(x+) = \langle x+|\frac{I}{2}|x+\rangle = \frac{1}{2}$，$p_{\mathrm{mix}}(x-) = \frac{1}{2}$。

     - **物理实验装置辨析（物理篇 Q1 实验视角，与[第 2 章第 5 题](#第-2-章)互补）**：把两束制备好的原子束直接送入沿水平 $x$ 轴定向的 Stern–Gerlach 磁铁——相干纯态 $|x+\rangle$ 的全部原子都从上出口 $x+$ 射出（下出口 $x-$ 计数为零），而 $z+/z-$ 经典等权混合束则在 $x+$ 与 $x-$ 两出口精确平分计数，实验上只需一次基底旋转即可区分相干叠加（纯度 $\operatorname{Tr}\rho^2 = 1$）与经典混合（纯度 $\operatorname{Tr}\rho^2 = 1/2$）。
   - **结论与边界回验**：两者均满足 $\operatorname{Tr}\rho = 1$ 且半正定，但纯度不同：$\operatorname{Tr}(\rho_{\mathrm{sup}}^2) = 1$（纯态），$\operatorname{Tr}(\rho_{\mathrm{mix}}^2) = \frac{1}{2} < 1$（混态）。
   - **易错坑提醒**：只在一组固定基下测出 $50\% / 50\%$ 绝不能证明制备出了叠加态，必须换基验证非对角相干项。

6. **【基础】全局相位 $e^{i\theta_{\mathrm{g}}}$ 不可观测性与相对相位 $e^{i\phi}$ 的干涉效应**

   - **题意与约定**：设归一化态 $|\psi\rangle$ 与任意归一化测量基态 $|m\rangle$，先证明整体乘上 $e^{i\theta_{\mathrm{g}}}$（$\theta_{\mathrm{g}} \in \mathbb{R}$）不改变任何投影概率，再解释为何单臂相对相位 $e^{i\phi}$ 能改变 Mach–Zehnder 输出。
   - **核心提示**：对任意投影基态 $|m\rangle$，利用内积右线性把整体因子 $e^{i\theta_{\mathrm{g}}}$ 提出模平方外并代入 $|e^{i\theta_{\mathrm{g}}}|^2=1$；再说明单臂相对相位留在干涉两臂求和内部，无法整体提出。
   - **完整分步演算**：利用内积的右线性以及单位复数模平方 $|e^{i\theta_{\mathrm{g}}}|^2 = \cos^2\theta_{\mathrm{g}} + \sin^2\theta_{\mathrm{g}} = 1$：

     $$
     \bigl|\langle m|e^{i\theta_{\mathrm{g}}}\psi\rangle\bigr|^2
     = \bigl|e^{i\theta_{\mathrm{g}}}\langle m|\psi\rangle\bigr|^2
     = \bigl|e^{i\theta_{\mathrm{g}}}\bigr|^2 \bigl|\langle m|\psi\rangle\bigr|^2
     = |\langle m|\psi\rangle|^2.
     $$

     相反，只给 $|1\rangle$ 分量乘 $e^{i\phi}$ 时，中间态变为 $(|0\rangle + e^{i\phi}|1\rangle)/\sqrt{2}$，$e^{i\phi}$ 无法提到整个态矢量外面；经第二个分束器 $B$ 线性叠加后，两出口振幅为 $\frac{1 \pm e^{i\phi}}{2}$，取模平方时交叉项 $e^{i\phi} + e^{-i\phi} = 2\cos\phi$ 显式保留了 $\phi$，使概率 $(1\pm\cos\phi)/2$ 在 $0$ 与 $1$ 之间连续摆动。
   - **结论与边界回验**：密度矩阵视角下 $(e^{i\theta_{\mathrm{g}}}|\psi\rangle)(\langle\psi|e^{-i\theta_{\mathrm{g}}}) = |\psi\rangle\langle\psi|$，全局相位在构成外积时即已精确抵消，而相对相位留在非对角元 $e^{\mp i\phi}$ 中。
   - **易错坑提醒**：若一个态成为更大纠缠态的某条条件分支（如控制门中的受控相位），局部的“全局相位”就会升级为整体态的相对相位，从而变成可观测量。

7. **【基础】Born 规则的物理公设地位与反例回验**

   - **题意与约定**：辨析数学公设、物理公设与实验检验三者关系，并用最小反例检验说明为何 Born 规则不是可以随意更改的猜测。
   - **核心提示**：区分数学公理（希尔伯特空间几何结构）、物理公设（Born 概率律）与实验证伪三层概念，并用“把概率改成振幅一次方或四次方破坏正定性/归一化/叠加干涉”的最小反例说明其刚性。
   - **完整分步演算**：线性代数只规定向量、内积和酉变换怎样运算，本身并不指明实验频率必须等于振幅的哪一个函数；把投影概率规定为 $p(k) = |\langle k|\psi\rangle|^2$ 是将形式数学映射到经验世界的**物理公设**。它绝非任意猜测，既受理论自洽性（酉变换下总概率守恒与非上下文性，如 Gleason 定理）严密约束，也接受了无数高精度实验检验。试构造两条反例规则在 Mach–Zehnder 态 $|\psi(\phi)\rangle = \frac{1+e^{i\phi}}{2}|0\rangle + \frac{1-e^{i\phi}}{2}|1\rangle$ 上回验：
     - **反例一（把模平方改为模的四次方 $|a_k|^4$）**：对平衡态 $|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}$，直接算和为 $|1/\sqrt{2}|^4 + |1/\sqrt{2}|^4 = \frac{1}{4} + \frac{1}{4} = \frac{1}{2} \ne 1$，立刻破坏酉演化下的总概率守恒。
     - **反例二（强行重归一化为 $p^{(4)}_k = |a_k|^4 / \sum_j |a_j|^4$）**：代入第 2 题 $\phi = \frac{\pi}{3}$ 处 $|A_0|^2 = \frac{3}{4},\; |A_1|^2 = \frac{1}{4}$，该规则预言

       $$
       p^{(4)}_0 = \frac{(3/4)^2}{(3/4)^2 + (1/4)^2} = \frac{9/16}{10/16} = 0.90 \ne 0.75,
       $$

       与单光子干涉和 Stern–Gerlach 实验精确测得的 $P_0(\pi/3) = 0.75$ 剧烈冲突，当场被实验证伪。
   - **结论与边界回验**：数学公设定义抽象形式系统，物理公设承担可证伪的经验预测；若未来高精度实验系统性违背 Born 规则，须修改物理理论而非用线性代数掩盖矛盾。
   - **易错坑提醒**：归一化条件 $\sum_k |a_k|^2 = 1$ 是“配合 Born 规则使总概率为 $1$”的配套约束，并不能反过来从纯代数证明自然界必须服从模平方律。

## 量子力学 Q2

1. **【计算】谱分解期望值、标准差与单次读数的区别**

   - **题意与约定**：给定厄米算符 $A = 2|0\rangle\langle 0| - |1\rangle\langle 1|$ 与归一化态 $|\psi\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$，求测量可能结果、对应概率、$\langle A\rangle$ 与 $\Delta A$。
   - **核心提示**：先由谱分解读出算符 $A$ 的两个本征值与对应测量概率，再用 $\langle A\rangle=\sum_k a_k p_k$ 与 $\Delta A=\sqrt{\langle A^2\rangle-\langle A\rangle^2}$ 计算期望与标准差，并对比单次测量允许出现的离散读数集合。
   - **完整分步演算**：由谱分解直接读出两个本征值 $a_0 = 2$（本征态 $|0\rangle$）与 $a_1 = -1$（本征态 $|1\rangle$）。按 Born 规则计算概率：

     $$
     p(2) = |\langle 0|\psi\rangle|^2 = \frac{1}{2}, \qquad
     p(-1) = |\langle 1|\psi\rangle|^2 = \frac{1}{2}.
     $$

     逐项计算一阶矩、二阶矩与标准差（因 $A^2 = 2^2|0\rangle\langle 0| + (-1)^2|1\rangle\langle 1| = 4|0\rangle\langle 0| + |1\rangle\langle 1|$）：

     $$
     \langle A\rangle = 2\cdot\frac{1}{2} + (-1)\cdot\frac{1}{2} = \frac{1}{2}, \qquad
     \langle A^2\rangle = 4\cdot\frac{1}{2} + 1\cdot\frac{1}{2} = \frac{5}{2},
     $$

     $$
     (\Delta A)^2 = \langle A^2\rangle - \langle A\rangle^2 = \frac{5}{2} - \left(\frac{1}{2}\right)^2 = \frac{9}{4}
     \quad\Longrightarrow\quad
     \Delta A = \frac{3}{2}.
     $$

   - **结论与边界回验**：也可直接算中心化方差 $\frac{1}{2}(2 - \frac{1}{2})^2 + \frac{1}{2}(-1 - \frac{1}{2})^2 = \frac{1}{2}\cdot\frac{9}{4} + \frac{1}{2}\cdot\frac{9}{4} = \frac{9}{4}$，一致。单次投影测量的仪器读数必落在算符谱 $\{2, -1\}$ 中，因此永远不会在单次实验里读出 $1/2$；$1/2$ 是对同制备系综重复大量测量后样本均值趋近的理论期望。
   - **易错坑提醒**：别把 $\langle A^2\rangle$ 误算成 $\langle A\rangle^2$，也别忘记标准差 $\Delta A$ 需要对方差开非负平方根。

2. **【进阶】Robertson 与 Schrödinger 不确定关系的完整推导**

   - **题意与约定**：对任意厄米算符 $A, B$ 与归一化态 $|\psi\rangle$，从中心化算符与 Cauchy–Schwarz 不等式出发推导 Robertson 关系，并指出保留复内积实部时多出的项。
   - **核心提示**：定义中心化算符 $\tilde A=A-\langle A\rangle I$、$\tilde B=B-\langle B\rangle I$，将 $|u\rangle=\tilde A|\psi\rangle$ 与 $|v\rangle=\tilde B|\psi\rangle$ 代入 Cauchy–Schwarz 不等式 $|\langle u|v\rangle|^2\le\langle u|u\rangle\langle v|v\rangle$，再把复内积拆成实部（反对易协方差）与虚部（对易子）两项平方和。
   - **完整分步演算**：定义中心化算符 $\widetilde{A} = A - \langle A\rangle I$、$\widetilde{B} = B - \langle B\rangle I$（二者仍厄米）及辅助向量 $|a\rangle = \widetilde{A}|\psi\rangle$、$|b\rangle = \widetilde{B}|\psi\rangle$。由厄米性得 $\langle a|a\rangle = \langle\psi|\widetilde{A}^2|\psi\rangle = (\Delta A)^2$、$\langle b|b\rangle = (\Delta B)^2$，且 $\langle a|b\rangle = \langle\psi|\widetilde{A}\widetilde{B}|\psi\rangle \equiv z$。施用 Cauchy–Schwarz 不等式 $\langle a|a\rangle\langle b|b\rangle \ge |\langle a|b\rangle|^2$（等价于 $2\times 2$ 格拉姆矩阵 $\begin{bmatrix}\langle a|a\rangle & \langle a|b\rangle\\ \langle b|a\rangle & \langle b|b\rangle\end{bmatrix} \succeq 0$ 的行列式非负）：

     $$
     (\Delta A)^2(\Delta B)^2 \ge |z|^2 = (\operatorname{Re} z)^2 + (\operatorname{Im} z)^2.
     $$

     因 $z^* = \langle\psi|(\widetilde{A}\widetilde{B})^\dagger|\psi\rangle = \langle\widetilde{B}\widetilde{A}\rangle$，将 $z$ 的虚部与实部分别改写为对易子与反对易子（注意常量项 $\langle A\rangle I, \langle B\rangle I$ 与任意算符对易，故 $[\widetilde{A}, \widetilde{B}] = [A, B]$）：

     $$
     \operatorname{Im} z = \frac{z - z^*}{2i} = \frac{1}{2i}\langle[\widetilde{A}, \widetilde{B}]\rangle = \frac{1}{2i}\langle[A, B]\rangle,
     \qquad
     \operatorname{Re} z = \frac{z + z^*}{2} = \frac{1}{2}\langle\{\widetilde{A}, \widetilde{B}\}\rangle = \frac{1}{2}\langle\{A, B\}\rangle - \langle A\rangle\langle B\rangle \equiv \operatorname{Cov}_\psi(A, B).
     $$

     丢弃非负项 $(\operatorname{Re} z)^2 \ge 0$ 后得 $(\Delta A)^2(\Delta B)^2 \ge \frac{1}{4}|\langle[A, B]\rangle|^2$，两边开非负平方根即证 Robertson 不确定关系：

     $$
     \Delta A\,\Delta B \ge \frac{1}{2}\bigl|\langle[A, B]\rangle\bigr|.
     $$

     若保留实部平方项 $\operatorname{Cov}_\psi(A, B)^2$，则得到更紧的 **Schrödinger 不确定关系**：

     $$
     (\Delta A)^2(\Delta B)^2 \ge \operatorname{Cov}_\psi(A, B)^2 + \frac{1}{4}\bigl|\langle[A, B]\rangle\bigr|^2.
     $$

   - **结论与边界回验**：取 $A = B$ 时，$[A, A] = 0$ 而 $\operatorname{Cov}_\psi(A, A) = (\Delta A)^2$，Schrödinger 关系化为 $(\Delta A)^4 \ge (\Delta A)^4$ 恒取等号。
   - **易错坑提醒**：推导中的 $(\Delta A)^2$ 刻画的是对同制备态独立分批测 $A$ 与测 $B$ 的内禀统计展宽，并非单次测量仪器读数精度与扰动的关系。

3. **【计算】$|{+i}\rangle$ 上验证 Robertson 不确定关系精确饱和**

   - **题意与约定**：对归一化态 $|{+i}\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}}$ 计算 $X, Z$ 的标准差乘积 $\Delta X\,\Delta Z$ 及 Robertson 下界 $\frac{1}{2}|\langle[X, Z]\rangle|$。
   - **核心提示**：在态 $|{+i}\rangle$ 上分别计算 $\langle X\rangle,\langle Y\rangle,\langle Z\rangle$，利用 $X^2=Z^2=I$ 直接求 $\Delta X$ 与 $\Delta Z$，再用 $[X,Z]=-2iY$ 算出 Robertson 右端 $\frac{1}{2}|\langle[X,Z]\rangle|$ 并比较左右两边。
   - **完整分步演算**：先验算 $Y|{+i}\rangle = \begin{bmatrix}0 & -i\\ i & 0\end{bmatrix}\frac{1}{\sqrt{2}}\begin{bmatrix}1\\ i\end{bmatrix} = \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ i\end{bmatrix} = +|{+i}\rangle$，故 $\langle Y\rangle = 1$。再直接算 $\langle X\rangle$ 与 $\langle Z\rangle$：

     $$
     \langle X\rangle = \frac{1}{2}\begin{bmatrix}1 & -i\end{bmatrix}\begin{bmatrix}i\\ 1\end{bmatrix} = \frac{i - i}{2} = 0, \qquad
     \langle Z\rangle = \frac{1}{2}\begin{bmatrix}1 & -i\end{bmatrix}\begin{bmatrix}1\\ -i\end{bmatrix} = \frac{1 - 1}{2} = 0.
     $$

     由 $X^2 = Z^2 = I$ 得 $\langle X^2\rangle = \langle Z^2\rangle = 1$，从而 $\Delta X = \sqrt{1 - 0} = 1$、$\Delta Z = \sqrt{1 - 0} = 1$，左端 $\Delta X\,\Delta Z = 1$。再由 $[X, Z] = XZ - ZX = -2iY$ 算右端：

     $$
     \frac{1}{2}\bigl|\langle[X, Z]\rangle\bigr| = \frac{1}{2}\bigl|-2i\langle Y\rangle\bigr| = |-i\cdot 1| = 1.
     $$

   - **结论与边界回验**：左端 $1$ 精确等于右端 $1$，且 $\operatorname{Cov}(X, Z) = 0$，因此 $|{+i}\rangle$ 使 Robertson（及 Schrödinger）不等式同时饱和。
   - **易错坑提醒**：$[X, Z] = -2iY$ 而不是 $+2iY$（循环次序 $X\to Y\to Z$ 为正），虽然取绝对值后不影响下界大小，但在动力学与对易演算中绝不可弄反符号。

4. **【进阶】Robertson 零下界不意味着方差为零与 Schrödinger 饱和验证**

   - **题意与约定**：对实系数态 $|\phi\rangle = \cos\frac{\pi}{8}|0\rangle + \sin\frac{\pi}{8}|1\rangle$ 计算 $\Delta X\,\Delta Z$、Robertson 下界与对称协方差 $\operatorname{Cov}_\phi(X, Z)$。
   - **核心提示**：对实系数态 $|\phi\rangle$ 分别计算 $\langle X\rangle,\langle Y\rangle,\langle Z\rangle$：由于 $\langle Y\rangle=0$ 使 Robertson 右端为零，但 $\Delta X,\Delta Z$ 均非零；接着补算反对易协方差项 $\frac{1}{2}\langle\{X,Z\}\rangle-\langle X\rangle\langle Z\rangle$ 验证 Schrödinger 界。
   - **完整分步演算**：逐项计算三个 Pauli 期望值（利用二倍角公式 $\cos\frac{\pi}{4} = \sin\frac{\pi}{4} = \frac{1}{\sqrt{2}}$）：

     $$
     \begin{aligned}
     \langle X\rangle &= 2\cos\frac{\pi}{8}\sin\frac{\pi}{8} = \sin\frac{\pi}{4} = \frac{1}{\sqrt{2}}, \\
     \langle Z\rangle &= \cos^2\frac{\pi}{8} - \sin^2\frac{\pi}{8} = \cos\frac{\pi}{4} = \frac{1}{\sqrt{2}}, \\
     \langle Y\rangle &= -i\cos\frac{\pi}{8}\sin\frac{\pi}{8} + i\sin\frac{\pi}{8}\cos\frac{\pi}{8} = 0.
     \end{aligned}
     $$

     于是 Robertson 右端为 $\frac{1}{2}|\langle[X, Z]\rangle| = |\langle Y\rangle| = 0$。但由 $X^2 = Z^2 = I$ 计算真实标准差：

     $$
     \Delta X = \sqrt{1 - \frac{1}{2}} = \frac{1}{\sqrt{2}}, \qquad
     \Delta Z = \sqrt{1 - \frac{1}{2}} = \frac{1}{\sqrt{2}}, \qquad
     \Delta X\,\Delta Z = \frac{1}{2} > 0.
     $$

     因此 $X$ 与 $Z$ 都不是确定的！延伸检验 Schrödinger 关系：因 $\{X, Z\} = 0$，对称协方差为

     $$
     \operatorname{Cov}_\phi(X, Z) = \frac{1}{2}\langle\{X, Z\}\rangle - \langle X\rangle\langle Z\rangle = 0 - \frac{1}{\sqrt{2}}\cdot\frac{1}{\sqrt{2}} = -\frac{1}{2}.
     $$

     代入 Schrödinger 右端得 $(-\frac{1}{2})^2 + 0^2 = \frac{1}{4}$，恰好等于左端 $(\Delta X)^2(\Delta Z)^2 = (\frac{1}{2})^2 = \frac{1}{4}$，**精确饱和**！
   - **结论与边界回验**：Bloch 向量 $(\frac{1}{\sqrt{2}}, 0, \frac{1}{\sqrt{2}})$ 模长为 $\sqrt{\frac{1}{2} + 0 + \frac{1}{2}} = 1$（纯态无误）。
   - **易错坑提醒**：Robertson 右端是**态依赖的下界**，下界退化为 $0$ 仅说明该不等式变松了，绝不表示两算符对易或方差为零。

5. **【计算】对角哈密顿量演化与 $|+\rangle$ 态的 $X$ 基振荡概率**

   - **题意与约定**：给定不含时对角哈密顿量 $\mathcal{H} = E_0|0\rangle\langle 0| + E_1|1\rangle\langle 1|$ 与初态 $|\psi(0)\rangle = |+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$，求 $U(t) = e^{-i\mathcal{H}t/\hbar}$ 与时刻 $t$ 测得 $X = +1$ 的概率。
   - **核心提示**：对角哈密顿量的演化算符直接把指数作用在各对角元上 $U(t)=\operatorname{diag}(e^{-iE_0 t/\hbar},e^{-iE_1 t/\hbar})$，作用在 $|+\rangle$ 上后提出全局相位，再与 $\langle +|$ 做内积取模平方得振荡概率。
   - **完整分步演算**：因为 $\mathcal{H}$ 在计算基对角，矩阵指数直接作用在各本征值上：

     $$
     U(t) = e^{-i E_0 t/\hbar}|0\rangle\langle 0| + e^{-i E_1 t/\hbar}|1\rangle\langle 1|, \qquad
     |\psi(t)\rangle = U(t)|+\rangle = \frac{e^{-i E_0 t/\hbar}|0\rangle + e^{-i E_1 t/\hbar}|1\rangle}{\sqrt{2}}.
     $$

     按左共轭内积计算 $X = +1$（本征态 $|+\rangle$）的振幅并提取全局相位 $e^{-i E_0 t/\hbar}$：

     $$
     \langle +|\psi(t)\rangle = \frac{1}{2}\bigl(e^{-i E_0 t/\hbar} + e^{-i E_1 t/\hbar}\bigr) = \frac{e^{-i E_0 t/\hbar}}{2}\bigl(1 + e^{-i(E_1 - E_0)t/\hbar}\bigr).
     $$

     取模平方（利用 $|e^{-i E_0 t/\hbar}|^2 = 1$ 与半角恒等式 $\frac{1+\cos\alpha}{2} = \cos^2\frac{\alpha}{2}$）：

     $$
     p_X(+; t)
     = \frac{1}{4}\bigl|1 + e^{-i(E_1 - E_0)t/\hbar}\bigr|^2
     = \frac{1 + \cos\!\bigl[(E_1 - E_0)t/\hbar\bigr]}{2}
     = \cos^2\!\left(\frac{(E_1 - E_0)t}{2\hbar}\right).
     $$

   - **结论与边界回验**：$t = 0$ 时 $p_X(+; 0) = \cos^2 0 = 1$（初态确为 $|+\rangle$）；将 $E_0, E_1$ 同时平移同一常数 $C$ 时能级差 $E_1 - E_0$ 不变，概率保持不变。
   - **易错坑提醒**：振荡角频率是 $(E_1 - E_0)/\hbar$，而 $\cos^2$ 括号内是半角 $(E_1 - E_0)t/(2\hbar)$，切勿遗漏分母的 $2$。

6. **【计算】$\mathcal{H}_X = \frac{\hbar\Omega}{2}X$ 演化概率与 $\Omega/(2\pi) = 25\ \mathrm{MHz}$ 的 $\pi$ 脉冲时长**

   - **题意与约定**：对不含时哈密顿量 $\mathcal{H}_X = \frac{\hbar\Omega}{2}X$（$\Omega$ 为角频率，单位 $\mathrm{rad/s}$），从 $|0\rangle$ 出发求 $p(1, t)$，并由普通频率 $\frac{\Omega}{2\pi} = 25\ \mathrm{MHz}$ 算 $\pi$ 脉冲时长 $t_\pi$。
   - **核心提示**：展开矩阵指数 $U(t)=e^{-i\frac{\Omega t}{2}X}=\cos(\frac{\Omega t}{2})I-i\sin(\frac{\Omega t}{2})X$ 作用于 $|0\rangle$ 求 $p(1,t)$；解 $\pi$ 脉冲时长时务必区分普通频率 $f=\Omega/(2\pi)$ 与角频率 $\Omega$，避免差掉 $2\pi$ 因子。
   - **完整分步演算**：因 $X^2 = I$，按矩阵指数展开得 $U(t) = e^{-i\Omega t X/2} = \cos\frac{\Omega t}{2}I - i\sin\frac{\Omega t}{2}X$。作用在 $|0\rangle$ 上（$I|0\rangle = |0\rangle,\; X|0\rangle = |1\rangle$）：

     $$
     |\psi(t)\rangle = U(t)|0\rangle = \cos\frac{\Omega t}{2}|0\rangle - i\sin\frac{\Omega t}{2}|1\rangle
     \quad\Longrightarrow\quad
     p(1, t) = \left|-i\sin\frac{\Omega t}{2}\right|^2 = \sin^2\frac{\Omega t}{2}.
     $$

     $\pi$ 脉冲首次把 $|0\rangle$ 完全翻至 $|1\rangle$，满足 $\frac{\Omega t_\pi}{2} = \frac{\pi}{2} \iff \Omega t_\pi = \pi$。由 $\frac{\Omega}{2\pi} = 25\ \mathrm{MHz} = 25 \times 10^6\ \mathrm{s}^{-1}$ 得 $\Omega = 2\pi \times 25 \times 10^6\ \mathrm{rad/s}$，故

     $$
     t_\pi = \frac{\pi}{\Omega} = \frac{1}{2(\Omega/2\pi)} = \frac{1}{2 \times 25 \times 10^6\ \mathrm{s}^{-1}} = 2.0 \times 10^{-8}\ \mathrm{s} = 20\ \mathrm{ns}.
     $$

   - **结论与边界回验**：$p(0, t) + p(1, t) = \cos^2\frac{\Omega t}{2} + \sin^2\frac{\Omega t}{2} = 1$；代入 $t = 20\ \mathrm{ns}$ 得 $\Omega t/2 = \pi/2$，$p(1, 20\ \mathrm{ns}) = 1$。
   - **易错坑提醒**：最常见错误是把 $25\ \mathrm{MHz}$ 直接当成角频率 $\Omega$ 代入 $\pi/\Omega$，会凭空多算一个 $2\pi$ 因子（错算成 $\approx 125.7\ \mathrm{ns}$）。

7. **【基础】能量本征态为何称为“定态”以及态矢是否字面不变**

   - **题意与约定**：设 $\mathcal{H}|E_n\rangle = E_n|E_n\rangle$，由定常薛定谔演化判断任意不显含时间可观测量的统计及态矢本身的变化。
   - **核心提示**：把能量本征态 $|E_n\rangle$ 代入定常薛定谔演化 $U(t)|E_n\rangle=e^{-iE_n t/\hbar}|E_n\rangle$，区分“态矢量自身带有随时间旋转的全局相位”与“任意不含时观测量的概率与期望均不随时间变化”。
   - **完整分步演算**：由 $U(t) = e^{-i\mathcal{H}t/\hbar}$ 得演化态为 $|E_n; t\rangle = e^{-i E_n t/\hbar}|E_n\rangle$。对任意不显含时间的投影态 $|m\rangle$，测量概率为

     $$
     \bigl|\langle m|E_n; t\rangle\bigr|^2 = \bigl|e^{-i E_n t/\hbar}\bigr|^2 \bigl|\langle m|E_n\rangle\bigr|^2 = \bigl|\langle m|E_n\rangle\bigr|^2,
     $$

     且对应的密度矩阵 $|E_n; t\rangle\langle E_n; t| = |E_n\rangle\langle E_n|$ 严格不含时。这就是“定态”的确切含义：**所有不显含时间的测量概率分布与期望值都恒定不变**。但这绝不表示态矢（右矢）字面上完全不变——它的每个复坐标都在以角频率 $E_n/\hbar$ 匀速旋转复相位 $e^{-i E_n t/\hbar}$。
   - **结论与边界回验**：一旦把两个不同能量的本征态叠在一起（如第 5 题的 $|+\rangle$），两项相位转速不同，就会产生随时间演化的相对相位 $e^{-i(E_1-E_0)t/\hbar}$ 并驱动可测振荡。
   - **易错坑提醒**：别把“定态”理解成经典粒子静止不动；定态的动能期望或非对易观测量方差依然可以非零。

8. **【进阶】两段不对易 $X/Z$ 脉冲的完整 $2\times 2$ 矩阵乘积、两条换序轨迹与单指数反例**

   - **题意与约定**：两段脉冲各持续 $\tau$，满足 $\omega\tau = \frac{\pi}{2}$，对应 $\mathcal{H}_X = \frac{\hbar\omega}{2}X$ 与 $\mathcal{H}_Z = \frac{\hbar\omega}{2}Z$，从初态 $|0\rangle = [1, 0]^T$ 出发，完整展开两种施序的 $2\times 2$ 矩阵乘法、中间态轨迹与末态 $X$ 基概率，并对照错误单指数。
   - **核心提示**：分别写出 $R_x(\pi/2)$ 与 $R_z(\pi/2)$ 的 $2\times 2$ 矩阵，按两种先后顺序乘出总演化矩阵并作用于初态，再对比两末态在 $X$ 基下的测量概率，并检验简单把时间积分放进单个指数是否漏掉了 $[X,Z]$ 对易项。
   - **完整分步演算**：先写出两段脉冲各自的 $2\times 2$ 演化矩阵（利用 $e^{\mp i\pi/4} = \frac{1 \mp i}{\sqrt{2}}$）：

     $$
     R_x\!\left(\frac{\pi}{2}\right) = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & -i\\ -i & 1\end{bmatrix}, \qquad
     R_z\!\left(\frac{\pi}{2}\right) = \begin{bmatrix}e^{-i\pi/4} & 0\\ 0 & e^{+i\pi/4}\end{bmatrix} = \frac{1}{\sqrt{2}}\begin{bmatrix}1 - i & 0\\ 0 & 1 + i\end{bmatrix}.
     $$

     - **轨迹一（先 $X$ 后 $Z$，晚左早右 $U_{X\to Z} = R_z(\frac{\pi}{2})R_x(\frac{\pi}{2})$）**：逐格做 $2\times 2$ 矩阵乘法：

       $$
       U_{X\to Z}
       = \frac{1}{2}\begin{bmatrix}1 - i & 0\\ 0 & 1 + i\end{bmatrix}\begin{bmatrix}1 & -i\\ -i & 1\end{bmatrix}
       = \frac{1}{2}\begin{bmatrix}(1-i)\cdot 1 + 0 & (1-i)(-i) + 0\\ 0 + (1+i)(-i) & 0 + (1+i)\cdot 1\end{bmatrix}
       = \frac{1}{2}\begin{bmatrix}1 - i & -1 - i\\ 1 - i & 1 + i\end{bmatrix}.
       $$

       逐步追踪态演化与 Bloch 向量：$|0\rangle \xrightarrow{R_x(\pi/2)} \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ -i\end{bmatrix} = |{-i}\rangle \xrightarrow{R_z(\pi/2)} \frac{1}{2}\begin{bmatrix}1 - i\\ 1 - i\end{bmatrix} = e^{-i\pi/4}|+\rangle$（Bloch 路径：$(0,0,1)\to(0,-1,0)\to(1,0,0)$）。最终测 $X$，得 $p_X(+) = |\langle +|e^{-i\pi/4}|+\rangle|^2 = 1$。
     - **轨迹二（先 $Z$ 后 $X$，$U_{Z\to X} = R_x(\frac{\pi}{2})R_z(\frac{\pi}{2})$）**：逐格做 $2\times 2$ 矩阵乘法：

       $$
       U_{Z\to X}
       = \frac{1}{2}\begin{bmatrix}1 & -i\\ -i & 1\end{bmatrix}\begin{bmatrix}1 - i & 0\\ 0 & 1 + i\end{bmatrix}
       = \frac{1}{2}\begin{bmatrix}1 - i & -i(1 + i)\\ -i(1 - i) & 1 + i\end{bmatrix}
       = \frac{1}{2}\begin{bmatrix}1 - i & 1 - i\\ -1 - i & 1 + i\end{bmatrix}.
       $$

       逐步追踪态演化与 Bloch 向量：$|0\rangle \xrightarrow{R_z(\pi/2)} e^{-i\pi/4}|0\rangle$（绕 $z$ 轴转北极不动！）$\xrightarrow{R_x(\pi/2)} \frac{1}{2}\begin{bmatrix}1 - i\\ -1 - i\end{bmatrix} = e^{-i\pi/4}|{-i}\rangle$（注意 $-1 - i = -i(1 - i)$；Bloch 路径：$(0,0,1)\to(0,0,1)\to(0,-1,0)$）。最终测 $X$，振幅 $\langle +|e^{-i\pi/4}|{-i}\rangle = e^{-i\pi/4}\frac{1 - i}{2}$，概率为

       $$
       p_X(+) = \left|\frac{1 - i}{2}\right|^2 = \frac{1^2 + (-1)^2}{4} = \frac{1}{2}, \qquad
       p_X(-) = \frac{1}{2}.
       $$

   - **结论与边界回验**：两种安排的普通时间积分完全相同，均为 $A = \frac{1}{\hbar}\int_0^{2\tau}\mathcal{H}(t)\,dt = \frac{\pi}{4}(X + Z)$；若错误忽略时间排序而直接算 $U_{\mathrm{naive}} = e^{-iA}$，会得出 $p_X(+) = \frac{1 + \sin^2(\pi\sqrt{2}/4)}{2} \approx 0.9014$，与轨迹一（$1$）和轨迹二（$1/2$）全不相符。根源在于 $[X, Z] = -2iY \ne 0$，时变不对易哈密顿量必须按时间顺序分段连乘（或使用保幺正的 Magnus 展开）。
   - **易错坑提醒**：矩阵乘积 $R_z R_x$ 表示**先施 $R_x$ 后施 $R_z$**，初学者最容易把电路从左向右的时间顺序和算符从右向左的作用顺序写反。

### 练 Q2-C：【进阶】两段不对易脉冲的二阶 Magnus 展开与 Dyson 截断破坏幺正性反例

- **题意与约定**：对应[量子力学 Q2 第 8.1 节](../quantum-mechanics/02-observables-dynamics.md#81-两段不对易-xz-脉冲换序dyson-破幺正反例与二阶-magnus-手算)。单比特在 $[0, \tau/2]$ 内受定常哈密顿量 $\mathcal{H}_1 = \frac{\hbar\Omega}{2}X$ 驱动，在 $[\tau/2, \tau]$ 内切换为 $\mathcal{H}_2 = \frac{\hbar\Omega}{2}Z$ 驱动，记单段无量纲脉冲面积 $\theta = \Omega\tau/2$，取 $\theta = \pi/4$。分别写出：(a) 精确时间排序演化 $U_{\mathrm{exact}}$；(b) 一阶与二阶 Magnus 展开 $U_{\mathrm{M1}} = e^{\Omega_1}$、$U_{\mathrm{M2}} = e^{\Omega_1 + \Omega_2}$，检验其严格幺正性；(c) 一阶截断 Dyson 级数 $U_{\mathrm{D1}} = I + \Omega_1$，证明其直接破坏幺正性与概率守恒，并比较三者与精确解的 Frobenius 范数误差。
- **核心提示**：由时间排序规则，后施加的 $\mathcal{H}_2$ 写在左边；Magnus 展开把演化写成单一指数 $e^{\Omega_1 + \Omega_2 + \cdots}$，其中 $\Omega_1 = -\frac{i}{\hbar}\int_0^\tau \mathcal{H}(t)\,dt$，$\Omega_2 = -\frac{1}{2\hbar^2}\int_0^\tau dt_1\int_0^{t_1}dt_2\,[\mathcal{H}(t_1), \mathcal{H}(t_2)]$，对两段常值脉冲该二重积分直接化简为 $\frac{1}{2}[A_2, A_1]$！
- **完整分步演算**：
  - **第一步：精确解与分段生成元**：记 $A_1 = -\frac{i}{\hbar}\mathcal{H}_1\frac{\tau}{2} = -i\frac{\theta}{2}X$、$A_2 = -\frac{i}{\hbar}\mathcal{H}_2\frac{\tau}{2} = -i\frac{\theta}{2}Z$，精确时间排序演化为：

    $$
    U_{\mathrm{exact}} = e^{A_2} e^{A_1} = e^{-i\frac{\theta}{2}Z} e^{-i\frac{\theta}{2}X}.
    $$

  - **第二步：一阶与二阶 Magnus 展开及幺正性证明**：
    - 一阶项为两段积分之和：$\Omega_1 = A_1 + A_2 = -i\frac{\theta}{2}(X + Z)$；
    - 二阶项仅在 $t_1 \in [\tau/2, \tau],\; t_2 \in [0, \tau/2]$ 上有非零对易子，积分面积恰为 $(\tau/2)^2$，再乘前因子 $\frac{1}{2}$ 并利用 $[Z, X] = 2iY$：

      $$
      \Omega_2 = \frac{1}{2}[A_2, A_1]
      = \frac{1}{2}\left[-i\frac{\theta}{2}Z,\; -i\frac{\theta}{2}X\right]
      = -\frac{\theta^2}{8}[Z, X]
      = -\frac{\theta^2}{8}(2iY)
      = -i\frac{\theta^2}{4}Y.
      $$

    - **严格幺正性检验**：因 $X, Y, Z$ 均为厄米矩阵且 $\theta \in \mathbb{R}$，立刻有 $\Omega_1^\dagger = -\Omega_1$ 与 $\Omega_2^\dagger = -\Omega_2$（均为反厄米矩阵），从而无论截断到一阶还是二阶，矩阵指数 $U_{\mathrm{M1}} = e^{\Omega_1}$ 与 $U_{\mathrm{M2}} = e^{\Omega_1 + \Omega_2}$ 均严格满足 $U^\dagger U = e^{-\Omega}e^{\Omega} = I$，100% 保持态矢量归一化！
  - **第三步：一阶截断 Dyson 级数破幺正反例与误差对比**：一阶 Dyson 展开 $U_{\mathrm{D1}} = I + \Omega_1 = I - i\frac{\theta}{2}(X + Z)$。计算 $U_{\mathrm{D1}}^\dagger U_{\mathrm{D1}}$（利用 $X^2 = Z^2 = I$ 且 $XZ + ZX = 0$）：

    $$
    U_{\mathrm{D1}}^\dagger U_{\mathrm{D1}}
    = \left(I + i\frac{\theta}{2}(X + Z)\right)\left(I - i\frac{\theta}{2}(X + Z)\right)
    = I + \frac{\theta^2}{4}(X^2 + Z^2 + XZ + ZX)
    = \left(1 + \frac{\theta^2}{2}\right) I.
    $$

    代入 $\theta = \pi/4$，得 $U_{\mathrm{D1}}^\dagger U_{\mathrm{D1}} = \left(1 + \frac{\pi^2}{32}\right)I \approx 1.3084\,I \ne I$——任意归一化初态经 $U_{\mathrm{D1}}$ 作用后概率总和直接暴涨到 $130.84\%$！
    计算三者在 $\theta = \pi/4$ 时相对精确演化 $U_{\mathrm{exact}}$ 的 Frobenius 范数误差 $\|U - U_{\mathrm{exact}}\|_F$：
    - $\|U_{\mathrm{D1}} - U_{\mathrm{exact}}\|_F \approx 0.3032$（误差最大且严重破幺正）；
    - $\|U_{\mathrm{M1}} - U_{\mathrm{exact}}\|_F \approx 0.2107$（严格幺正，漏掉 $[Z,X]$ 二阶修正）；
    - $\|U_{\mathrm{M2}} - U_{\mathrm{exact}}\|_F \approx 0.0415$（严格幺正，补入 $-i\frac{\theta^2}{4}Y$ 后误差骤降逾 $5$ 倍！）。
- **结论与边界回验**：Magnus 展开把时间排序近似留在李代数（反厄米生成元）内部，任意阶截断都天然保持严格幺正；而直接截断 Dyson 泰勒级数在有限脉冲面积下必然破坏概率守恒（$1 + \theta^2/2 > 1$）。
- **易错坑提醒**：二阶 Magnus 项 $\Omega_2 = \frac{1}{2}[A_2, A_1]$ 中“后施加的 $A_2$ 在左、先施加的 $A_1$ 在右”，若写反次序就会把 $Y$ 轴修正的符号彻底算错！

### 练 Q2-D：【计算】完备对易可观测量集（CSCO）破除两比特能谱简并与非对易反例

- **题意与约定**：对应[量子力学 Q2 第 3.2 节](../quantum-mechanics/02-observables-dynamics.md#32-简并怎么办完备对易可观测量集合csco)。在两比特大端序计算基 $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ 下，考察总纵向自旋算符 $A = Z_0 + Z_1 = Z\otimes I + I\otimes Z$。(a) 写出 $A$ 的 $4\times 4$ 对角矩阵，找出全部本征值及其简并度，说明为何单靠 $A$ 的测量结果无法唯一确定量子态；(b) 检验 $B = Z_0 - Z_1$ 是否与 $A$ 对易并破除全部简并，构成一个完备对易可观测量集（CSCO）；(c) 计算 $[A, X_0]$ 说明为何不能用 $X_0$ 与 $A$ 组成 CSCO。
- **核心提示**：先把 $Z_0 = \operatorname{diag}(1, 1, -1, -1)$ 与 $Z_1 = \operatorname{diag}(1, -1, 1, -1)$ 逐位相加和相减读出全部本征值对 $(a, b)$；检验第二问与第三问时直接算矩阵对易子 $[A, B]$ 与 $[A, X_0]$。
- **完整分步演算**：
  - **第一问：求 $A = Z_0 + Z_1$ 的谱与简并子空间**：

    $$
    Z_0 = \operatorname{diag}(1, 1, -1, -1), \qquad
    Z_1 = \operatorname{diag}(1, -1, 1, -1)
    \quad\Longrightarrow\quad
    A = Z_0 + Z_1 = \operatorname{diag}(2,\; 0,\; 0,\; -2).
    $$

    本征值与简并度为：
    - $a = +2$（非简并，唯一本征态 $|00\rangle$）；
    - $a = -2$（非简并，唯一本征态 $|11\rangle$）；
    - $a = 0$（**二重简并**，对应二维本征子空间 $\mathcal{V}_0 = \operatorname{span}\{|01\rangle, |10\rangle\}$）。因此仅知“测得 $A = 0$”无法区分 $|01\rangle$、$|10\rangle$ 乃至任意叠加态 $\alpha|01\rangle + \beta|10\rangle$。
  - **第二问：用 $B = Z_0 - Z_1$ 构造 CSCO**：先算 $B$ 的矩阵及与 $A$ 的对易子：

    $$
    B = Z_0 - Z_1 = \operatorname{diag}(0,\; 2,\; -2,\; 0).
    $$

    因 $A$ 与 $B$ 均为同基对角阵，显见 $[A, B] = AB - BA = 0$（相容可观测量，可同时测量）。逐基态列出联合本征值二元组 $(a, b)$：
    - $|00\rangle \mapsto (+2, 0)$；
    - $|01\rangle \mapsto (0, +2)$；
    - $|10\rangle \mapsto (0, -2)$；
    - $|11\rangle \mapsto (-2, 0)$。

    四个二元组互不相同，原本二重简并的 $\mathcal{V}_0$ 被 $B$ 的本征值 $+2$ 与 $-2$ 彻底劈开，故 $\{A, B\}$ 构成一个合法的 CSCO（同样，交换算符 $S_{XY} = X_0 X_1 + Y_0 Y_1$ 也与 $A$ 对易，会把 $\mathcal{V}_0$ 劈成单态 $|\Psi^-\rangle$ 与三重态 $|\Psi^+\rangle$，构成另一组等价但基底不同的 CSCO！）。
  - **第三问：检验非对易算符 $X_0$ 为何失败**：因 $[Z_0, X_0] = 2i Y_0$ 且 $[Z_1, X_0] = 0$，立即得：

    $$
    [A, X_0] = [Z_0 + Z_1, X_0] = [Z_0, X_0] + 0 = 2i\,Y_0 \ne 0.
    $$

    由于 $A$ 与 $X_0$ 不对易，两者不存在共同本征基（测量 $X_0$ 会把 $A = 0$ 子空间打散回 $A = \pm 2$），绝不能组成 CSCO。
- **结论与边界回验**：$A$ 存在二重简并的 $a = 0$ 子空间；补入对易算符 $B = Z_0 - Z_1$ 后四组联合本征值两两相异，唯一锁定全部 4 个正交基态；$X_0$ 因 $[A, X_0] = 2iY_0 \ne 0$ 不相容而失败。
- **易错坑提醒**：CSCO 并不唯一——同一简并子空间可以选用不同对易算符（例如 $Z_0 - Z_1$ 选出乘积基 $|01\rangle, |10\rangle$，而 $X_0 X_1 + Y_0 Y_1$ 选出纠缠基 $|\Psi^\pm\rangle$），选用哪组取决于物理问题自身的对称性。

## 量子力学 Q3

1. **【计算】$6\ \mathrm{GHz}$ 能隙的能量与等效温度换算**

   - **题意与约定**：按 2019 SI 精确定义常数 $h = 6.62607015 \times 10^{-34}\ \mathrm{J\cdot s}$ 与 $k_{\mathrm{B}} = 1.380649 \times 10^{-23}\ \mathrm{J/K}$，计算普通频率 $f = 6\ \mathrm{GHz} = 6 \times 10^9\ \mathrm{Hz}$ 对应的能隙 $\Delta E$（单位 $\mathrm{J}$）与等效温度 $\Delta E/k_{\mathrm{B}}$（单位 $\mathrm{K}$）。
   - **核心提示**：代入 2019 SI 精确常数 $h=6.62607015\times 10^{-34}\,\mathrm{J\cdot s}$ 与 $k_{\mathrm B}=1.380649\times 10^{-23}\,\mathrm{J/K}$，依次计算 $\Delta E=hf$（焦耳）及等效温度尺度 $T_{\mathrm{eq}}=\Delta E/k_{\mathrm B}$（开尔文）。
   - **完整分步演算**：利用 $\Delta E = hf$ 直接相乘并除以 $k_{\mathrm{B}}$：

     $$
     \Delta E = hf = (6.62607015 \times 10^{-34}\ \mathrm{J\cdot s})(6 \times 10^9\ \mathrm{s}^{-1}) \approx 3.9756 \times 10^{-24}\ \mathrm{J} \approx 3.976 \times 10^{-24}\ \mathrm{J},
     $$

     $$
     \frac{\Delta E}{k_{\mathrm{B}}} = \frac{3.97564 \times 10^{-24}\ \mathrm{J}}{1.380649 \times 10^{-23}\ \mathrm{J/K}} \approx 0.288\ \mathrm{K} = 288\ \mathrm{mK}.
     $$

   - **结论与边界回验**：经验换算系数 $h/k_{\mathrm{B}} \approx 4.7992 \times 10^{-11}\ \mathrm{K/Hz} \approx 48\ \mathrm{mK/GHz}$，乘以 $6\ \mathrm{GHz}$ 得 $288\ \mathrm{mK} = 0.288\ \mathrm{K}$，量纲与数值双吻合。
   - **易错坑提醒**：$\Delta E = hf = \hbar\omega$，代入普通频率 $f$ 时用 $h$，代入角频率 $\omega = 2\pi f$ 时用 $\hbar$，切勿混配。

2. **【计算】$4\ \mathrm{GHz}$、$50\ \mathrm{mK}$ 下的二能级热平衡占据**

   - **题意与约定**：在热平衡非简并二能级模型中，取 $f = 4 \times 10^9\ \mathrm{Hz}$ 与温度 $T = 50\ \mathrm{mK} = 0.050\ \mathrm{K}$，由玻尔兹曼分布求 $p_1/p_0$ 与 $p_1$。
   - **核心提示**：先算玻尔兹曼无量纲指数 $x=hf/(k_{\mathrm B}T)$（注意将 $50\,\mathrm{mK}$ 换算为 $0.050\,\mathrm{K}$），由 $p_1/p_0=e^{-x}$ 求比值，再利用归一化 $p_0+p_1=1$ 算出激发态热占据 $p_1=\frac{e^{-x}}{1+e^{-x}}$。
   - **完整分步演算**：先算无量纲能隙与热能之比 $x = \frac{hf}{k_{\mathrm{B}} T}$：

     $$
     x = \frac{(6.62607015 \times 10^{-34})(4 \times 10^9)}{(1.380649 \times 10^{-23})(0.050)}
     = \frac{2.65043 \times 10^{-24}}{6.90325 \times 10^{-25}}
     \approx 3.8394.
     $$

     代入玻尔兹曼比值与归一化条件 $p_0 + p_1 = 1$：

     $$
     \frac{p_1}{p_0} = e^{-x} \approx e^{-3.8394} \approx 0.02151, \qquad
     p_1 = \frac{e^{-x}}{1 + e^{-x}} = \frac{1}{1 + e^x} \approx \frac{0.02151}{1.02151} \approx 0.0211.
     $$

   - **结论与边界回验**：$p_0 = 1 - p_1 \approx 0.9789$，满足 $p_1/p_0 \approx 0.0215$。约 $2.11\%$ 仅适用于理想热平衡非简并二能级模型；真实超导芯片常受杂散红外辐射与非平衡准粒子影响，有效温度往往高于冷台名义温度。
   - **易错坑提醒**：温度 $50\ \mathrm{mK}$ 必须先换算为 $0.050\ \mathrm{K}$ 再代入，漏掉 $10^{-3}$ 会把热占据误算小几十个数量级。

3. **【基础】“只保留两个能级”的四项联合检查与超导、离子阱实例**

   - **题意与约定**：说明将多能级物理器件截断为二维量子比特时，为何制备、控制、读出与环境四环节缺一不可，并给出超导与离子阱具体实例。
   - **核心提示**：从初态制备、脉冲频谱选择控制、读出分辨与子空间外泄漏监测、以及环境弛豫通道四个环节逐一论证截断充分性，并为超导 Transmon 与囚禁离子分别匹配具体的物理能级与参数例子。
   - **完整分步演算**：在纸面上挑出 $|0\rangle, |1\rangle$ 并不自动把真实动力学关进二维子空间，必须同时核验四项条件：（1）**制备**须把绝大部分布居锁定在 $\{|0\rangle, |1\rangle\}$ 内；（2）**控制**脉冲频谱与强度不能显著激发子空间外的跃迁；（3）**读出**须准确区分 $|0\rangle, |1\rangle$ 并能识别或界定子空间外泄漏；（4）**环境**耦合不能在门或等待期间造成快速弛豫、退相位或跳出子空间。
     - **两类主力硬件四环节定量对照（物理篇 Q3 器件视角，区别于[量子力学 Q4 第 8 题](#量子力学-q4)的连续波函数截断视角）**：
       - **超导 Transmon**：① *制备*：典型 $\omega_{01}/(2\pi) \approx 5\ \mathrm{GHz}$ 须在 $15\text{–}20\ \mathrm{mK}$ 稀释制冷机下结合主动复位压制 $|1\rangle$ 热占据；② *控制*：弱非谐性 $\alpha/(2\pi) \approx -250\ \mathrm{MHz}$，门脉宽若短至数纳秒须加 DRAG 导数波形抑制 $|1\rangle \to |2\rangle$ 泄漏；③ *读出*：cQED 色散读出驱动光子数必须远低于临界光子数 $n_{\mathrm{crit}} = \Delta_{qr}^2/(4g^2)$，防止测量诱导态跃迁到更高能级；④ *环境*：须压制红外杂散光子、二能级系统（TLS）与准粒子引起的 $T_1/T_2$ 退相干。
       - **囚禁离子（如 $^{171}\mathrm{Yb}^+$ 超精细钟态）**：① *制备*：靠圆偏振光泵浦把布居精准导入 $F=0, m_F=0$ 基态，避免残留到 $m_F = \pm 1$ 塞曼子能级；② *控制*：拉曼双光子或微波驱动频率与偏振必须避开邻近塞曼跃迁并抑制自发拉曼散射；③ *读出*：利用循环荧光跃迁区分亮态与暗态，同时防范向长寿命亚稳态的光学暗态泄漏；④ *环境*：须屏蔽磁场低频起伏（借 $m_F=0\leftrightarrow 0$ 一阶磁场不敏感“钟态”）并压低电极表面噪声导致的反常声子加热。
   - **结论与边界回验**：结合主流硬件实例对照说明：
     - **超导 Transmon**：取非谐电路最低两能级 $|0\rangle, |1\rangle$，但过短或过强的微波脉冲频谱展宽会覆盖 $|1\rangle \leftrightarrow |2\rangle$ 跃迁并触发泄漏（需依靠非谐性与 DRAG 整形抑制）。
     - **离子阱**：以两个内部超精细或光学态存逻辑信息，双比特纠缠门却必须暂时耦合到离子链的集体振动模；若门结束时运动模与内部态未能完全解纠缠，逻辑操作就会退化为非酉的噪声通道而非理想两比特酉门。
   - **易错坑提醒**：多能级系统里的辅助态（如振动模、Rydberg 态）本身不是错误，门末未干净归位才产生泄漏与残留纠缠。

4. **【计算】$4\ \mathrm{ns}$ 脉冲频宽与 $250\ \mathrm{MHz}$ 非谐性的泄漏风险评估**

   - **题意与约定**：给定 $f_{01} = 5.00\ \mathrm{GHz}$、$f_{12} = 4.75\ \mathrm{GHz}$ 与脉冲时长 $\tau = 4\ \mathrm{ns} = 4 \times 10^{-9}\ \mathrm{s}$，估算频宽并界定该估算的适用范围。
   - **核心提示**：先用时间—带宽估算 $\Delta f\sim 1/\tau$ 算出 $4\,\mathrm{ns}$ 脉冲的频谱宽度，再与非谐性 $|\alpha|/(2\pi)=|f_{12}-f_{01}|$ 直接比较量级，评估驱动 $|0\rangle\leftrightarrow|1\rangle$ 时旁瓣误触 $|1\rangle\leftrightarrow|2\rangle$ 的风险。
   - **完整分步演算**：先求相邻跃迁绝对非谐性，再按傅里叶时间—频率关系估算脉冲频宽量级：

     $$
     |\alpha|/(2\pi) = |f_{12} - f_{01}| = |4.75 - 5.00|\ \mathrm{GHz} = 0.25\ \mathrm{GHz} = 250\ \mathrm{MHz},
     $$

     $$
     \Delta f_{\mathrm{pulse}} \sim \frac{1}{\tau} = \frac{1}{4 \times 10^{-9}\ \mathrm{s}} = 2.5 \times 10^8\ \mathrm{Hz} = 250\ \mathrm{MHz}.
     $$

   - **结论与边界回验**：脉冲频宽 $250\ \mathrm{MHz}$ 与非谐性 $250\ \mathrm{MHz}$ 处于同一量级，说明脉冲频谱在 $f_{12}$ 处存在显著能量分量，强烈提示 $|1\rangle \to |2\rangle$ 泄漏风险。但 $1/\tau$ 仅是量级警报，不能单独算出精确泄漏概率：真实泄漏还取决于包络形状与旁瓣、DRAG 整形、驱动幅度、三能级跃迁矩阵元 $\sqrt{2}$ 因子、初态在 $|1\rangle$ 上的占据、失谐及硬件线路传递函数。
   - **易错坑提醒**：压短门时长可减少退相干误差，却会拉宽频谱诱发泄漏——两者之间的权衡决定超导单比特门的典型时长（约 $10\text{–}30\ \mathrm{ns}$）。

5. **【基础】旋磁比 $\gamma$ 符号与磁场中自旋高低能态约定**

   - **题意与约定**：对磁场 $B > 0$ 中的自旋哈密顿量 $H = -\frac{1}{2}\gamma\hbar B\sigma_z$（其中 $\sigma_z|+z\rangle = +|+z\rangle,\; \sigma_z|-z\rangle = -|-z\rangle$），按 $\gamma > 0$ 与 $\gamma < 0$ 分情形求能量高低。
   - **核心提示**：把 $\sigma_z|\pm z\rangle=\pm|\pm z\rangle$ 代入 $H=-\frac{1}{2}\gamma\hbar B\sigma_z$，写出两本征态的能量 $E_{\pm}=\mp\frac{1}{2}\gamma\hbar B$，按 $\gamma>0$ 与 $\gamma<0$ 分情况判断谁能量更低、再决定逻辑 $|0\rangle$ 贴在哪个态上。
   - **完整分步演算**：将 $\sigma_z$ 两个本征值 $+1, -1$ 直接代入 $H$：

     $$
     E_{+z} = -\frac{\gamma\hbar B}{2}, \qquad
     E_{-z} = +\frac{\gamma\hbar B}{2}, \qquad
     E_{-z} - E_{+z} = \gamma\hbar B.
     $$

     - 若 **$\gamma > 0$**（如质子）：$E_{+z} < E_{-z}$，故 $|+z\rangle$ 为低能基态、$|-z\rangle$ 为高能激发态；
     - 若 **$\gamma < 0$**（如自由电子因带负电荷磁矩与自旋反向）：不等号翻转，$E_{-z} < E_{+z}$，故 $|-z\rangle$ 才是低能基态。
   - **结论与边界回验**：无论 $\gamma$ 正负，能隙大小均为 $|\gamma|\hbar B > 0$。由于“自旋朝上（$|+z\rangle$）”并非在所有粒子中都是基态，不能先入为主地把“自旋朝上”固定称为逻辑 $|0\rangle$；正确做法是先由完整哈密顿量判定高低能态，再显式声明逻辑 $|0\rangle, |1\rangle$ 的映射约定。
   - **易错坑提醒**：核对实验与理论论文时，务必先查清逻辑 $|0\rangle$ 对齐的是物理基态还是 $\sigma_z = +1$，防止能级与失谐正负号整体写反。

6. **【计算】失谐 Rabi 振荡的广义频率、最大激发概率与首次峰值时间**

   - **题意与约定**：按本章旋转波近似驱动约定，给定普通频率口径 $\frac{\Omega}{2\pi} = 4\ \mathrm{MHz}$、失谐 $\frac{\Delta}{2\pi} = 3\ \mathrm{MHz}$，从初态 $|0\rangle$ 出发求广义 Rabi 频率、峰值高度与首峰时刻。
   - **核心提示**：先用广义 Rabi 频率 $\Omega_{\mathrm{eff}}=\sqrt{\Omega^2+\Delta^2}$（可在普通频率口径下直接用勾股数算 $\Omega_{\mathrm{eff}}/(2\pi)$），再代入失谐 Rabi 激发公式 $P_1(t)=\frac{\Omega^2}{\Omega_{\mathrm{eff}}^2}\sin^2(\frac{\Omega_{\mathrm{eff}}t}{2})$ 求峰值与首次达峰时间。
   - **完整分步演算**：由 $P_1(t) = \frac{\Omega^2}{\Omega_{\mathrm{eff}}^2}\sin^2\!\left(\frac{\Omega_{\mathrm{eff}}t}{2}\right)$ 及 $\Omega_{\mathrm{eff}} = \sqrt{\Omega^2 + \Delta^2}$ 逐项计算：

     $$
     \frac{\Omega_{\mathrm{eff}}}{2\pi} = \sqrt{\left(\frac{\Omega}{2\pi}\right)^2 + \left(\frac{\Delta}{2\pi}\right)^2} = \sqrt{4^2 + 3^2}\ \mathrm{MHz} = 5\ \mathrm{MHz},
     $$

     $$
     P_1^{\max} = \frac{\Omega^2}{\Omega^2 + \Delta^2} = \frac{4^2}{4^2 + 3^2} = \frac{16}{25} = 0.64.
     $$

     首次达到最大值时 $\sin^2(\Omega_{\mathrm{eff}}t_{\mathrm{peak}}/2) = 1$，即 $\frac{\Omega_{\mathrm{eff}} t_{\mathrm{peak}}}{2} = \frac{\pi}{2}$：

     $$
     t_{\mathrm{peak}} = \frac{\pi}{\Omega_{\mathrm{eff}}} = \frac{1}{2\bigl(\Omega_{\mathrm{eff}}/(2\pi)\bigr)} = \frac{1}{2 \times 5 \times 10^6\ \mathrm{s}^{-1}} = 1.0 \times 10^{-7}\ \mathrm{s} = 100\ \mathrm{ns}.
     $$

   - **结论与边界回验**：在共振（$\Delta = 0$）时 $\Omega/(2\pi) = 4\ \mathrm{MHz}$ 给出 $t_\pi = \frac{1}{2\times 4\ \mathrm{MHz}} = 125\ \mathrm{ns}$、$P_1^{\max} = 1$；加入 $3\ \mathrm{MHz}$ 失谐后，首峰从 $125\ \mathrm{ns}$ **提前**到 $100\ \mathrm{ns}$，但最大翻转概率被压低到 $0.64$。
   - **易错坑提醒**：失谐并不会让 Rabi 振荡变慢，而是让它振得更快、摆幅更矮；算比值时 $2\pi$ 约去，但算时间 $t_{\mathrm{peak}} = \pi/\Omega_{\mathrm{eff}}$ 时务必区分角频率与普通频率。

7. **【计算】第 10 节系统—环境纠缠态偏迹与非对角相干衰减**

   - **题意与约定**：对应本章**第 10 节**系统—环境纠缠态 $|\Psi(t)\rangle = \alpha|0\rangle|E_0(t)\rangle + \beta|1\rangle|E_1(t)\rangle$（$|\alpha|^2 + |\beta|^2 = 1$），当环境重叠 $\langle E_1|E_0\rangle = 0.3 e^{i\theta}$ 时，求系统约化密度矩阵的对角占据与非对角相干项变化。
   - **核心提示**：先写出系统—环境联合纯态外积 $|\Psi\rangle\langle\Psi|$，对环境求偏迹时利用 $\operatorname{Tr}_E(|E_i\rangle\langle E_j|)=\langle E_j|E_i\rangle$，核对主对角元是否依赖环境重叠、非对角相干元如何按 $\langle E_1|E_0\rangle$ 衰减。
   - **完整分步演算**：按第 10 节偏迹公式 $\rho_S(t) = \operatorname{Tr}_E(|\Psi(t)\rangle\langle\Psi(t)|)$（利用 $\langle E_0|E_0\rangle = \langle E_1|E_1\rangle = 1$ 与 $\operatorname{Tr}(|E_0\rangle\langle E_1|) = \langle E_1|E_0\rangle$）：

     $$
     \rho_S(t) = \begin{pmatrix}
     |\alpha|^2 & \alpha\beta^*\langle E_1|E_0\rangle \\
     \alpha^*\beta\langle E_0|E_1\rangle & |\beta|^2
     \end{pmatrix}
     = \begin{pmatrix}
     |\alpha|^2 & 0.3 e^{i\theta}\alpha\beta^* \\
     0.3 e^{-i\theta}\alpha^*\beta & |\beta|^2
     \end{pmatrix}.
     $$

     直接读出：两个对角占据概率仍分别为 $|\alpha|^2$ 与 $|\beta|^2$，**完全不变**（纯退相位过程不交换能量）；非对角相干项 $\rho_{01}(t) = 0.3 e^{i\theta}\alpha\beta^*$，其模 $|\rho_{01}(t)| = 0.3|\alpha\beta^*|$ 衰减为初始值的 **$0.3$ 倍**，并附加相位 $\theta$。
   - **结论与边界回验**：$\operatorname{Tr}\rho_S = |\alpha|^2 + |\beta|^2 = 1$，行列式 $|\alpha|^2|\beta|^2(1 - 0.3^2) = 0.91|\alpha\beta|^2 \ge 0$（合法半正定密度矩阵）。当 $|\langle E_1|E_0\rangle| = 1$ 时相干无损；当重叠降为 $0$ 时相干项彻底消失。
   - **易错坑提醒**：相干项里乘的是 $\langle E_1|E_0\rangle$ 而非 $\langle E_0|E_1\rangle$，写反共轭会把附加相位 $\theta$ 变号。

8. **【基础】双轨光子编码逻辑基态与真空丢失态 $|00\rangle_{ab}$ 的区别**

   - **题意与约定**：设两正交光学模式（如两条波导或两种偏振）为 $a, b$，光子数基写作 $|n_a n_b\rangle_{ab}$，写出双轨光子量子比特的两个逻辑基态，并说明 $|00\rangle_{ab}$ 的物理含义。
   - **核心提示**：按双轨单光子编码写出总光子数恒为 $1$ 的两个逻辑基态 $|10\rangle_{ab},|01\rangle_{ab}$，再按光子数守恒判断 $|00\rangle_{ab}$ 属于逻辑子空间内的状态还是物理光子丢失（擦除）态。
   - **完整分步演算**：双轨编码把**单个光子**占据哪一条轨道编码为逻辑比特：

     $$
     |0_L\rangle = |10\rangle_{ab}, \qquad
     |1_L\rangle = |01\rangle_{ab}.
     $$

     计算总光子数算符 $\hat{N}_{\mathrm{tot}} = \hat{n}_a + \hat{n}_b$ 在两逻辑态上的本征值，均为 $1 + 0 = 0 + 1 = 1$（同属单光子扇区）；而全空态 $|00\rangle_{ab}$ 满足 $\hat{N}_{\mathrm{tot}}|00\rangle_{ab} = 0$，它落在计算子空间之外，代表光子在波导、光纤或探测器中发生**丢失（擦除错误）**，绝不是逻辑 $0$。
   - **结论与边界回验**：双轨编码的优势正是光子丢失会跳出单光子子空间并被末端的无点击探测识别为可定位的擦除错误；将无光子态 $|0\rangle$ 与单光子态 $|1\rangle$ 当作逻辑基属于另一种单轨编码，两者不可混用。
   - **易错坑提醒**：读光子电路论文时看清 $|0_L\rangle = |10\rangle$ 与 $|00\rangle$ 的光子数差异，别把真空态误当成逻辑 $0$ 算进门保真度。

### 练 Q3-C：【计算】计算基失谐 $\Delta$ 与能量基失谐 $\delta_E$ 符号等价验证及 cQED 色散读出频移

- **题意与约定**：对应[量子力学 Q3 第 6.2 节](../quantum-mechanics/03-levels-control.md#62-计算基与能量基的失谐符号等价对照表)与[第 9.3 节](../quantum-mechanics/03-levels-control.md#93-transmon-三能级修正为何-alpha-to-0-时色散位移归零)。(a) 验证本书主口径（计算基 $Z = |0\rangle\langle 0| - |1\rangle\langle 1|$，失谐 $\Delta = \omega_d - \omega_0$，旋转系哈密顿量 $\mathcal{H}_{\mathrm{rot}} = \frac{\hbar\Delta}{2}Z + \frac{\hbar\Omega}{2}X$）与传统量子光学能量基口径（$Z_E = |e\rangle\langle e| - |g\rangle\langle g| = -Z$，失谐 $\delta_E = \omega_0 - \omega_d = -\Delta$，旋转系 $\mathcal{H}_{\mathrm{rot}} = \frac{\hbar\delta_E}{2}Z_E + \frac{\hbar\Omega}{2}X$）给出完全相同的矩阵元，并在红失谐 $\omega_d < \omega_0$ 下核对两者符号；(b) 对超导 Transmon-谐振腔色散耦合系统，取耦合 $g/(2\pi) = 80\ \mathrm{MHz}$、比特—腔失谐 $\Delta_{qr}/(2\pi) = -1.2\ \mathrm{GHz}$、非谐性 $\alpha/(2\pi) = -240\ \mathrm{MHz}$，计算理想二能级色散位移 $\chi_{\mathrm{2LS}}$、Transmon 三能级修正色散位移 $\chi_{\mathrm{transmon}}$、两者比值以及临界光子数 $n_{\mathrm{crit}}$。
- **核心提示**：第一问只需把 $Z_E = -Z$ 与 $\delta_E = -\Delta$ 同时代入观察两个负号精确抵消；第二问代入第 9.3 节精确公式 $\chi_{\mathrm{2LS}} = \frac{g^2}{\Delta_{qr}}$、$\chi_{\mathrm{transmon}} = \frac{g^2}{\Delta_{qr}}\cdot\frac{\alpha}{\Delta_{qr}+\alpha}$ 与 $n_{\mathrm{crit}} = \frac{\Delta_{qr}^2}{4g^2}$（普通频率口径下 $2\pi$ 因子在分子分母同步约去）。
- **完整分步演算**：
  - **第一问：双口径失谐符号等价验证**：将 $|g\rangle \leftrightarrow |0\rangle$、$|e\rangle \leftrightarrow |1\rangle$ 对应，有 $Z_E = |1\rangle\langle 1| - |0\rangle\langle 0| = -Z$ 且 $\delta_E = \omega_0 - \omega_d = -(\omega_d - \omega_0) = -\Delta$。直接代入得：

    $$
    \frac{\hbar\delta_E}{2}Z_E = \frac{\hbar(-\Delta)}{2}(-Z) = +\frac{\hbar\Delta}{2}Z
    = \begin{bmatrix} +\hbar\Delta/2 & 0 \\ 0 & -\hbar\Delta/2 \end{bmatrix}.
    $$

    核对红失谐情形（$\omega_d < \omega_0$）：本书口径下 $\Delta < 0$，故 $|0\rangle$ 对角元为负（$-\frac{\hbar|\Delta|}{2}$）、$|1\rangle$ 对角元为正（$+\frac{\hbar|\Delta|}{2}$）；能量基口径下 $\delta_E = |\Delta| > 0$，因 $Z_E = \operatorname{diag}(-1, +1)$，$|g\rangle$ 对角元同样为 $-\frac{\hbar|\Delta|}{2}$、$|e\rangle$ 对角元同样为 $+\frac{\hbar|\Delta|}{2}$，矩阵逐格完全一致！
  - **第二问：cQED 色散位移与临界光子数核算**：统一采用普通频率 $\mathrm{MHz}$ 单位（$g/(2\pi) = 80\ \mathrm{MHz},\; \Delta_{qr}/(2\pi) = -1200\ \mathrm{MHz},\; \alpha/(2\pi) = -240\ \mathrm{MHz}$），先确认色散条件小参数 $g/|\Delta_{qr}| = 80/1200 = 1/15 \approx 0.067 \ll 1$ 成立：
    - 理想二能级色散位移：

      $$
      \frac{\chi_{\mathrm{2LS}}}{2\pi} = \frac{g^2/(2\pi)^2}{\Delta_{qr}/(2\pi)}
      = \frac{80^2}{-1200}\ \mathrm{MHz}
      = -\frac{6400}{1200}\ \mathrm{MHz}
      = -\frac{16}{3}\ \mathrm{MHz} \approx -5.3333\ \mathrm{MHz}.
      $$

    - Transmon 三能级修正色散位移（计入 $|1\rangle \leftrightarrow |2\rangle$ 虚跃迁推挤，分母 $\Delta_{qr} + \alpha = -1200 - 240 = -1440\ \mathrm{MHz}$）：

      $$
      \frac{\chi_{\mathrm{transmon}}}{2\pi}
      = \frac{\chi_{\mathrm{2LS}}}{2\pi}\cdot\frac{\alpha}{\Delta_{qr} + \alpha}
      = \left(-\frac{16}{3}\right)\cdot\frac{-240}{-1440}\ \mathrm{MHz}
      = \left(-\frac{16}{3}\right)\cdot\frac{1}{6}\ \mathrm{MHz}
      = -\frac{8}{9}\ \mathrm{MHz} \approx -0.8889\ \mathrm{MHz}.
      $$

      可见理想二能级模型把真实 Transmon 的读出腔频劈裂精确高估了 **$\mathbf{6}$ 倍**！
    - 临界光子数：

      $$
      n_{\mathrm{crit}} = \frac{\Delta_{qr}^2}{4g^2} = \frac{1200^2}{4 \times 80^2} = \frac{1{,}440{,}000}{25{,}600} = 56.25.
      $$

- **结论与边界回验**：计算基 $(\Delta, Z)$ 与能量基 $(\delta_E, Z_E)$ 物理矩阵逐元严格一致；该器件上 $\chi_{\mathrm{2LS}}/(2\pi) \approx -5.3333\ \mathrm{MHz}$、$\chi_{\mathrm{transmon}}/(2\pi) \approx -0.8889\ \mathrm{MHz}$（缩减 $6$ 倍），$n_{\mathrm{crit}} = 56.25$。检验极限 $\alpha \to 0$ 时 $\chi_{\mathrm{transmon}} \to 0$，印证无非线性即无色散读出。
- **易错坑提醒**：混用一套文献的 $\delta_E = \omega_0 - \omega_d$ 却配另一套文献的计算基 $Z = |0\rangle\langle 0| - |1\rangle\langle 1|$，会导致整个旋转系失谐符号颠倒，画出的 Ramsey 相位演进方向全反！

### 练 Q3-D：【计算】Ramsey 自由进动与 Hahn 自旋回波消除静态失谐的矩阵手算对比

- **题意与约定**：对应[量子力学 Q3 第 7.1–7.2 节](../quantum-mechanics/03-levels-control.md#71-ramsey-干涉仪用自由进动把失谐变成相位)。设单比特在总自由演化时长 $T$ 内承受未知但恒定的静态频率漂移失谐 $\Delta \ne 0$，时长 $\tau$ 的自由演化算符为 $U_{\mathrm{free}}(\tau) = e^{-i\frac{\Delta\tau}{2}Z} = R_z(\Delta\tau)$，理想共振 $X$ 脉冲为 $R_x(\theta) = \cos(\theta/2)I - i\sin(\theta/2)X$。从初态 $|0\rangle$ 出发，零跳步对比：(a) Ramsey 序列 $R_x(\pi/2)\to U_{\mathrm{free}}(T)\to R_x(\pi/2)$ 的末态与测得 $|1\rangle$ 的概率 $P_{\mathrm{Ramsey}}(1)$；(b) Hahn 自旋回波序列 $R_x(\pi/2)\to U_{\mathrm{free}}(T/2)\to R_x(\pi)\to U_{\mathrm{free}}(T/2)\to R_x(\pi/2)$ 的末态与测得 $|1\rangle$ 的概率 $P_{\mathrm{Hahn}}(1)$，解释为何回波能把静态失谐彻底清零从而测出 $T_2$ 而非 $T_2^*$。
- **核心提示**：第一问依次乘三个 $2\times 2$ 矩阵（或用 $R_x(\pi/2) = \frac{1}{\sqrt{2}}(I - iX)$）算出 $|1\rangle$ 振幅；第二问在合并中间三项时直接利用 Pauli 反对易恒等式 $X\,e^{-i\phi Z}\,X = e^{+i\phi Z}$，观察两半段静态相位精确抵消！
- **完整分步演算**：
  - **第一问：Ramsey 序列逐拍矩阵手算**：记总进动角 $\phi = \Delta T$，有 $R_x(\pi/2) = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -i \\ -i & 1 \end{bmatrix}$ 与 $U_{\mathrm{free}}(T) = \begin{bmatrix} e^{-i\phi/2} & 0 \\ 0 & e^{+i\phi/2} \end{bmatrix}$。从右向左依次作用在 $|0\rangle$ 上：
    - 第 1 步（首枚 $\pi/2$ 脉冲）：$|\psi_1\rangle = R_x(\pi/2)|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 \\ -i \end{bmatrix}$；
    - 第 2 步（自由进动 $T$）：$|\psi_2\rangle = U_{\mathrm{free}}(T)|\psi_1\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} e^{-i\phi/2} \\ -i\,e^{+i\phi/2} \end{bmatrix}$；
    - 第 3 步（末枚 $\pi/2$ 脉冲）：

      $$
      |\psi_{\mathrm{Ramsey}}\rangle
      = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & -i \\ -i & 1 \end{bmatrix}
        \frac{1}{\sqrt{2}}\begin{bmatrix} e^{-i\phi/2} \\ -i\,e^{+i\phi/2} \end{bmatrix}
      = \frac{1}{2}\begin{bmatrix} e^{-i\phi/2} - e^{+i\phi/2} \\ -i\bigl(e^{-i\phi/2} + e^{+i\phi/2}\bigr) \end{bmatrix}
      = \begin{bmatrix} -i\sin(\phi/2) \\ -i\cos(\phi/2) \end{bmatrix}.
      $$

    读出测量概率：$P_{\mathrm{Ramsey}}(0) = \sin^2(\Delta T/2)$、$P_{\mathrm{Ramsey}}(1) = \cos^2(\Delta T/2)$（和恒为 $1$）。可见当静态失谐 $\Delta$ 在不同实验轮次间缓慢随机漂移时，余弦条纹平均后迅速衰减，给出较短的自由感应衰减时间 $T_2^*$。
  - **第二问：Hahn 自旋回波消除静态失谐**：中点 $\pi$ 脉冲为 $R_x(\pi) = -iX$。先化简中间三项 $U_{\mathrm{free}}(T/2)\,R_x(\pi)\,U_{\mathrm{free}}(T/2)$：利用 $X Z X = -Z \implies X e^{-i\frac{\phi}{4}Z} X = e^{+i\frac{\phi}{4}Z}$（因 $X^2 = I$，改写为 $e^{-i\frac{\phi}{4}Z} X = X e^{+i\frac{\phi}{4}Z}$）：

    $$
    U_{\mathrm{free}}(T/2)\,R_x(\pi)\,U_{\mathrm{free}}(T/2)
    = (-i)\,e^{-i\frac{\phi}{4}Z}\,X\,e^{-i\frac{\phi}{4}Z}
    = (-i)\,X\,e^{+i\frac{\phi}{4}Z}\,e^{-i\frac{\phi}{4}Z}
    = -iX = R_x(\pi)!
    $$

    两半段自由演化积累的静态相位 $+\Delta T/4$ 与 $-\Delta T/4$ 精确抵消！于是整条 Hahn 回波序列的净演化算符与静态失谐 $\Delta$ 完全无关：

    $$
    U_{\mathrm{Hahn}} = R_x(\pi/2)\,R_x(\pi)\,R_x(\pi/2) = R_x(2\pi) = -I,
    \qquad
    |\psi_{\mathrm{Hahn}}\rangle = -|0\rangle,
    $$

    因此对任意恒定失谐 $\Delta$ 均有 $P_{\mathrm{Hahn}}(0) = 1$、$P_{\mathrm{Hahn}}(1) = 0$（完美回波重组）！
- **结论与边界回验**：Ramsey 输出 $P_{\mathrm{Ramsey}}(1) = \cos^2(\Delta T/2)$ 对静态失谐高度敏感（适合精确标定失谐频率与测 $T_2^*$）；Hahn 回波在中点翻转布居使前后两半段静态相位精确对消，输出恒为 $|0\rangle$（除去 $-1$ 全局相位），屏蔽准静态低频漂移、暴露真正不可逆的动力学退相位时间 $T_2$。检验 $\Delta = 0$ 极限：Ramsey 变为 $R_x(\pi)|0\rangle = -i|1\rangle$（$P(1)=1$），Hahn 为 $R_x(2\pi)|0\rangle = -|0\rangle$（$P(1)=0$），完全吻合。
- **易错坑提醒**：Hahn 回波只能消除在单个回波窗口 $T$ 内基本不变的**低频/静态**失谐；对快于 $1/T$ 的高频白噪声（马尔可夫退相位），前后两半段的随机相位互不相关，无法靠中点 $\pi$ 脉冲相消。

## 量子力学 Q4

1. **【基础】长度 $L$ 区间常数波函数的归一化、子区间概率与量纲分析**

   - **题意与约定**：一维粒子限制在区间 $[0, L]$ 内，波函数取常数 $\psi(x) = A$（$x \in [0, L]$），区间外为 $0$。求归一化常数 $A$、落在任意三分之一长度子区间内的概率，并明确 $|\psi(x)|^2$ 与 $\psi(x)$ 的国际单位。
   - **核心提示**：对区间 $[0,L]$ 上的常数波函数 $\psi(x)=A$ 施加归一化积分 $\int_0^L |A|^2\,dx=1$ 反解 $A$，再积分三分之一区间求概率，并根据 $|\psi(x)|^2\,dx$ 无量纲反推概率密度与波函数的物理单位。
   - **完整分步演算**：按连续空间归一化条件 $\int_{-\infty}^{+\infty}|\psi(x)|^2\,dx = 1$ 直接积分：

     $$
     1 = \int_0^L |A|^2\,dx = |A|^2 \int_0^L 1\,dx = |A|^2 L
     \quad\Longrightarrow\quad
     |A| = \frac{1}{\sqrt{L}}.
     $$

     取全局相位使 $A > 0$，得归一化波函数 $\psi(x) = \frac{1}{\sqrt{L}}$（$0 \le x \le L$）。对任意长度为 $L/3$ 的子区间 $[a, a + L/3] \subset [0, L]$，概率为密度积分：

     $$
     P = \int_a^{a + L/3} |\psi(x)|^2\,dx = \int_a^{a + L/3} \frac{1}{L}\,dx = \frac{1}{L}\cdot\frac{L}{3} = \frac{1}{3}.
     $$

     量纲分析：积分 $P = \int |\psi(x)|^2\,dx$ 必须无量纲，而 $[dx] = \mathrm{m}$，因此概率密度单位为 $\bigl[|\psi(x)|^2\bigr] = \mathrm{m}^{-1}$（每米），波函数振幅单位为 $\bigl[\psi(x)\bigr] = \mathrm{m}^{-1/2}$（米的负二分之一次方）。
   - **结论与边界回验**：取整个区间 $[0, L]$ 积分得 $\int_0^L (1/L)\,dx = 1$，量纲 $\mathrm{m}^{-1}\cdot\mathrm{m} = 1$ 无误。
   - **易错坑提醒**：$|\psi(x)|^2$ 是**概率密度**而非“粒子恰好落在单点 $x$ 的概率”（在连续分布里单点概率恒为 $0$），它甚至可以在局部大于 $1$（例如当 $L = 0.25\ \mathrm{m}$ 时 $|\psi|^2 = 4\ \mathrm{m}^{-1}$），只要总积分为 $1$ 即可。

2. **【基础】无限深势阱排除 $n = 0$ 的原因与井宽加倍时的基态能量标度**

   - **题意与约定**：一维无限深方势阱（$0 \le x \le L$）满足硬壁边界条件 $\phi(0) = \phi(L) = 0$，定态解为 $\phi_n(x) = \sqrt{\frac{2}{L}}\sin\!\left(\frac{n\pi x}{L}\right)$，能量 $E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}$。解释为何不能取 $n = 0$，并算井宽 $L \to 2L$ 时基态能量的变化。
   - **核心提示**：把 $n=0$ 代入定态波函数 $\phi_n(x)=\sqrt{2/L}\sin(n\pi x/L)$ 看它是否处处为零（无法归一化）；再由能级公式 $E_n=\frac{n^2\pi^2\hbar^2}{2mL^2}$ 看井宽 $L\to 2L$ 时基态能量如何按 $1/L^2$ 缩放。
   - **完整分步演算**：若强行代入 $n = 0$，则波数 $k_0 = 0$，波函数在全空间恒为零：

     $$
     \phi_0(x) = \sqrt{\frac{2}{L}}\sin(0) \equiv 0 \quad\Longrightarrow\quad \int_0^L |\phi_0(x)|^2\,dx = 0 \ne 1.
     $$

     零向量无法归一化，不代表任何存在粒子的物理状态，故最小允许量子数必为 $n = 1$。井宽为 $L$ 与 $2L$ 时的基态能量分别为

     $$
     E_1(L) = \frac{\pi^2\hbar^2}{2mL^2}, \qquad
     E_1(2L) = \frac{\pi^2\hbar^2}{2m(2L)^2} = \frac{\pi^2\hbar^2}{8mL^2} = \frac{1}{4}E_1(L).
     $$

     即井宽加倍后基态能量降为原来的 $\frac{1}{4}$。
   - **结论与边界回验**：由 $E_1 \propto 1/L^2$，受限空间放宽 $2$ 倍，德布罗意基模波长加倍、动量标度减半（$p \sim \hbar\pi/L$），动能 $p^2/(2m)$ 随之降为 $1/4$。这一变化来自硬壁几何边界的放宽，与普朗克常数 $\hbar$ 无关。
   - **易错坑提醒**：$n = -1$ 仅给 $\phi_1(x)$ 乘上全局负号 $-1$，表示同一物理态而非独立新能级，因此势阱本征态只取正整数 $n = 1, 2, 3, \dots$。

3. **【计算】无限深势阱基态落在中间一半区域 $[L/4, 3L/4]$ 的完整积分推导**

   - **题意与约定**：取基态波函数 $\phi_1(x) = \sqrt{\frac{2}{L}}\sin\!\left(\frac{\pi x}{L}\right)$，零跳步积分求粒子落在 $[L/4, 3L/4]$ 的概率 $P_{\mathrm{mid}}$，并解释为何大于区间比例 $1/2$。
   - **核心提示**：对概率密度 $|\phi_1(x)|^2=\frac{2}{L}\sin^2(\frac{\pi x}{L})$ 先用降幂恒等式 $\sin^2\theta=\frac{1-\cos(2\theta)}{2}$，再逐项在区间 $[L/4,3L/4]$ 上定积分，并从波形中心高、两端低的分布形状解释为何大于 $1/2$。
   - **完整分步演算**：写出积分式并做无量纲换元 $u = x/L$（$dx = L\,du$，上下限由 $x = L/4, 3L/4$ 变为 $u = 1/4, 3/4$），再显式使用倍角降幂公式 $\sin^2(\pi u) = \frac{1 - \cos(2\pi u)}{2}$：

     $$
     \begin{aligned}
     P_{\mathrm{mid}}
     &= \int_{L/4}^{3L/4} |\phi_1(x)|^2\,dx
      = \frac{2}{L}\int_{L/4}^{3L/4}\sin^2\!\left(\frac{\pi x}{L}\right)dx
      = \int_{1/4}^{3/4} 2\sin^2(\pi u)\,du \\
     &= \int_{1/4}^{3/4} \bigl[1 - \cos(2\pi u)\bigr]\,du
      = \left[u - \frac{\sin(2\pi u)}{2\pi}\right]_{1/4}^{3/4} \\
     &= \left(\frac{3}{4} - \frac{\sin(3\pi/2)}{2\pi}\right) - \left(\frac{1}{4} - \frac{\sin(\pi/2)}{2\pi}\right).
     \end{aligned}
     $$

     代入精确三角函数值 $\sin(3\pi/2) = -1$ 与 $\sin(\pi/2) = +1$：

     $$
     P_{\mathrm{mid}} = \left(\frac{3}{4} + \frac{1}{2\pi}\right) - \left(\frac{1}{4} - \frac{1}{2\pi}\right) = \frac{1}{2} + \frac{1}{\pi} \approx 0.5 + 0.318310 \approx 0.8183.
     $$

   - **结论与边界回验**：剩余概率 $1 - 0.8183 = 0.1817$ 对称分布在靠墙的两段 $[0, L/4]$ 与 $[3L/4, L]$ 中（各约 $9.08\%$）。因为基态密度 $\frac{2}{L}\sin^2(\pi x/L)$ 在井中央 $x = L/2$ 处取峰值、在两壁处被硬壁压回零，所以中间一半宽度聚集了超过 $81.8\%$ 的概率，远非均匀分布的 $1/2$。
   - **易错坑提醒**：计算原函数时别漏掉 $\cos(2\pi u)$ 积分出来的分母 $2\pi$，也别把 $\sin(3\pi/2) = -1$ 的负号丢掉（丢负号会错算成 $1/2$）。

4. **【计算】两能级等权叠加态的左半井概率振荡与能量分布守恒**

   - **题意与约定**：对第 3 节叠加态 $\psi(x, t) = \frac{1}{\sqrt{2}}\bigl[\phi_1(x)e^{-iE_1 t/\hbar} + \phi_2(x)e^{-iE_2 t/\hbar}\bigr]$（其中 $E_2 = 4E_1 \implies E_2 - E_1 = 3E_1$），推导左半井 $[0, L/2]$ 概率 $P_{\mathrm{left}}(t)$，求 $t = 0$ 与 $t = \pi\hbar/(3E_1)$ 处数值，并核验能量分布。
   - **核心提示**：展开 $|\psi(x,t)|^2$ 时保留 $\phi_1(x)\phi_2(x)$ 的干涉交叉项 $2\cos[(E_2-E_1)t/\hbar]$，在左半井 $[0,L/2]$ 上积分看为何随时间振荡；同时按各定态展开系数模平方检验能量测量分布是否含时。
   - **完整分步演算**：展开实函数 $\phi_1, \phi_2$ 的概率密度：

     $$
     |\psi(x, t)|^2 = \frac{\phi_1(x)^2 + \phi_2(x)^2}{2} + \phi_1(x)\phi_2(x)\cos\!\left(\frac{3E_1 t}{\hbar}\right).
     $$

     对 $[0, L/2]$ 积分：由对称性 $\int_0^{L/2}\phi_1^2\,dx = \int_0^{L/2}\phi_2^2\,dx = \frac{1}{2}$，第一项贡献 $\frac{1}{2}$；交叉项换元 $u = x/L$ 并用积化和差 $2\sin(\pi u)\sin(2\pi u) = \cos(\pi u) - \cos(3\pi u)$：

     $$
     I_{\mathrm{left}} = \int_0^{1/2}\bigl[\cos(\pi u) - \cos(3\pi u)\bigr]\,du
     = \left[\frac{\sin(\pi u)}{\pi} - \frac{\sin(3\pi u)}{3\pi}\right]_0^{1/2}
     = \frac{1}{\pi} - \frac{-1}{3\pi} = \frac{4}{3\pi} \approx 0.424413.
     $$

     合得 $P_{\mathrm{left}}(t) = \frac{1}{2} + \frac{4}{3\pi}\cos\!\left(\frac{3E_1 t}{\hbar}\right)$。分别代入两个时刻：

     $$
     P_{\mathrm{left}}(0) = \frac{1}{2} + \frac{4}{3\pi}\cos 0 \approx 0.9244, \qquad
     P_{\mathrm{left}}\!\left(\frac{\pi\hbar}{3E_1}\right) = \frac{1}{2} + \frac{4}{3\pi}\cos\pi \approx 0.0756.
     $$

   - **结论与边界回验**：两时刻之和 $0.9244 + 0.0756 = 1$（由对称性，后者恰为 $t=0$ 时的右半井概率）。任何时刻测量能量，得到 $E_1$ 与 $E_2$ 的概率恒为 $|\frac{1}{\sqrt{2}}e^{-iE_1 t/\hbar}|^2 = \frac{1}{2}$ 与 $\frac{1}{2}$，平均能量恒为 $\frac{E_1 + E_2}{2} = \frac{5}{2}E_1$，**能量分布完全不变**；位置概率左右涌动源于两分量之间的相对相位干涉（换成各半经典混合态时交叉项消失，$P_{\mathrm{left}} \equiv 1/2$）。
   - **易错坑提醒**：左半井概率变化绝不意味着粒子在与外界交换能量，孤立势阱的哈密顿量不含时，能量分布严格守恒。

5. **【计算】谐振子降阶算符 $\hat a$ 作用在 $|3\rangle$ 上的结果、范数与能级差**

   - **题意与约定**：一维量子谐振子哈密顿量 $\hat H = \hbar\omega(\hat a^\dagger\hat a + \frac{1}{2}I)$，Fock 态满足 $\hat N|n\rangle = \hat a^\dagger\hat a|n\rangle = n|n\rangle$ 及能量 $E_n = \bigl(n + \frac{1}{2}\bigr)\hbar\omega$。求 $\hat a|3\rangle$、其范数、原能量与降阶归一化态能量。
   - **核心提示**：套用降阶算符作用律 $\hat a|n\rangle=\sqrt{n}|n-1\rangle$ 代入 $n=3$ 求出结果向量与范数（注意 $\hat a$ 不是保范酉算符！），再把 $n=3$ 与 $n=2$ 代入含零点能的谱公式 $E_n=(n+\frac{1}{2})\hbar\omega$。
   - **完整分步演算**：先由降阶关系验证系数——因 $\hat N(\hat a|n\rangle) = (\hat a\hat N - \hat a)|n\rangle = (n - 1)\hat a|n\rangle$，故 $\hat a|n\rangle$ 正比于 $|n - 1\rangle$，而其范数平方为

     $$
     \bigl\|\hat a|n\rangle\bigr\|^2 = \langle n|\hat a^\dagger\hat a|n\rangle = \langle n|\hat N|n\rangle = n
     \quad\Longrightarrow\quad
     \hat a|n\rangle = \sqrt{n}\,|n - 1\rangle \quad (n \ge 1).
     $$

     代入 $n = 3$ 得

     $$
     \hat a|3\rangle = \sqrt{3}\,|2\rangle, \qquad
     \bigl\|\hat a|3\rangle\bigr\| = \sqrt{3}, \qquad
     \bigl\|\hat a|3\rangle\bigr\|^2 = 3.
     $$

     再把 $n = 3$ 与降阶后重归一化的态 $|2\rangle$ 分别代入能谱公式 $E_n = \bigl(n + \frac{1}{2}\bigr)\hbar\omega$：

     $$
     E_3 = \left(3 + \frac{1}{2}\right)\hbar\omega = \frac{7}{2}\hbar\omega, \qquad
     E_2 = \left(2 + \frac{1}{2}\right)\hbar\omega = \frac{5}{2}\hbar\omega, \qquad
     E_3 - E_2 = \hbar\omega.
     $$

   - **结论与边界回验**：降阶恰使能量精确下降一个量子 $\hbar\omega$。因 $\hat a^\dagger\hat a = \hat N \ne I$，$\hat a$ 不是保范数的酉量子门，而是会放大高 Fock 态长度的无界算符，故范数平方 $3 > 1$ 绝不可误当作一次物理测量的成功概率。
   - **易错坑提醒**：谐振子第 $n$ 激发态能量是 $(n + \frac{1}{2})\hbar\omega$ 而非 $n\hbar\omega$，切勿漏掉零点能 $\frac{1}{2}\hbar\omega$。

6. **【进阶】谐振子基态的零点动能、势能与最小不确定度 $\Delta\hat x\,\Delta\hat p = \frac{\hbar}{2}$**

   - **题意与约定**：用谐振子升降算符反解 $\hat x$ 与 $\hat p$，零跳步证明基态 $|0\rangle$ 满足 $\langle\hat x\rangle = \langle\hat p\rangle = 0$ 但动能、势能均非零，并求不确定度乘积。
   - **核心提示**：先由 $\hat a,\hat a^\dagger$ 定义反解 $\hat x,\hat p$ 并利用 $\hat a|0\rangle=0$ 验证一阶矩为零；算二阶矩 $\langle\hat x^2\rangle,\langle\hat p^2\rangle$ 时务必展开四项并利用 $[\hat a,\hat a^\dagger]=I$ 保留唯一的 $\hat a\hat a^\dagger$ 存活项，进而求零点动能、势能与 $\Delta\hat x\,\Delta\hat p$。
   - **完整分步演算**：由定义 $\hat a = \sqrt{\frac{m\omega}{2\hbar}}\hat x + \frac{i}{\sqrt{2m\hbar\omega}}\hat p$ 及其共轭 $\hat a^\dagger = \sqrt{\frac{m\omega}{2\hbar}}\hat x - \frac{i}{\sqrt{2m\hbar\omega}}\hat p$，两式相加与相减直接反解出位置和动量算符：

     $$
     \hat x = \sqrt{\frac{\hbar}{2m\omega}}\bigl(\hat a + \hat a^\dagger\bigr), \qquad
     \hat p = i\sqrt{\frac{m\hbar\omega}{2}}\bigl(\hat a^\dagger - \hat a\bigr).
     $$

     利用 $\hat a|0\rangle = 0$、$\hat a^\dagger|0\rangle = |1\rangle$ 与正交性 $\langle 0|1\rangle = 0$，立即验证一阶矩均为零：

     $$
     \langle 0|\hat x|0\rangle = \sqrt{\frac{\hbar}{2m\omega}}\langle 0|1\rangle = 0, \qquad
     \langle 0|\hat p|0\rangle = i\sqrt{\frac{m\hbar\omega}{2}}\langle 0|1\rangle = 0.
     $$

     再把 $\hat x^2$ 与 $\hat p^2$ 完整展开（注意不可交换 $\hat a\hat a^\dagger$ 与 $\hat a^\dagger\hat a$），并利用 $\hat a|0\rangle = 0$、$\langle 0|\hat a^\dagger = 0$、$\hat a\hat a^\dagger|0\rangle = (\hat a^\dagger\hat a + I)|0\rangle = |0\rangle$（仅 $\hat a\hat a^\dagger$ 一项存活！）：

     $$
     \langle 0|\hat x^2|0\rangle = \frac{\hbar}{2m\omega}\langle 0|\bigl(\hat a^2 + (\hat a^\dagger)^2 + \hat a\hat a^\dagger + \hat a^\dagger\hat a\bigr)|0\rangle = \frac{\hbar}{2m\omega}\langle 0|0\rangle = \frac{\hbar}{2m\omega},
     $$

     $$
     \langle 0|\hat p^2|0\rangle = -\frac{m\hbar\omega}{2}\langle 0|\bigl((\hat a^\dagger)^2 + \hat a^2 - \hat a\hat a^\dagger - \hat a^\dagger\hat a\bigr)|0\rangle = +\frac{m\hbar\omega}{2}\langle 0|0\rangle = \frac{m\hbar\omega}{2}.
     $$

     因为位置和动量存在非零起伏（均值为零不代表平方的均值为零），动能与势能的期望均严格为正：

     $$
     \langle\hat T\rangle_0 = \frac{\langle\hat p^2\rangle_0}{2m} = \frac{1}{4}\hbar\omega, \qquad
     \langle\hat V\rangle_0 = \frac{1}{2}m\omega^2\langle\hat x^2\rangle_0 = \frac{1}{4}\hbar\omega, \qquad
     \langle\hat T\rangle_0 + \langle\hat V\rangle_0 = \frac{1}{2}\hbar\omega = E_0.
     $$

     最后计算位置与动量标准差及其乘积：

     $$
     \Delta\hat x = \sqrt{\langle\hat x^2\rangle_0} = \sqrt{\frac{\hbar}{2m\omega}}, \qquad
     \Delta\hat p = \sqrt{\langle\hat p^2\rangle_0} = \sqrt{\frac{m\hbar\omega}{2}}
     \quad\Longrightarrow\quad
     \Delta\hat x\,\Delta\hat p = \frac{\hbar}{2}.
     $$

   - **结论与边界回验**：不确定度乘积精确饱和 Heisenberg–Robertson 下界 $\frac{\hbar}{2}$，且动能与势能精确平分零点能 $E_0 = \frac{1}{2}\hbar\omega$。
   - **易错坑提醒**：饱和下界仅说明基态是最小不确定度高斯波包，绝不能据此赋予基态一条同时具有确定位置和确定动量的经典轨道。

7. **【计算】方势垒 $E = V_0/2$、$\kappa L = 1$ 的精确隧穿透射率与 $e^{-2\kappa L}$ 近似陷阱**

   - **题意与约定**：对一维矩形势垒（高度 $V_0$、宽度 $L$，能量 $0 < E < V_0$），波数 $k = \sqrt{2mE}/\hbar$、衰减系数 $\kappa = \sqrt{2m(V_0 - E)}/\hbar$，在 $E = V_0/2$ 与 $\kappa L = 1$ 下算精确透射率 $T$ 并对比朴素指数 $e^{-2\kappa L}$。
   - **核心提示**：把 $E=V_0/2$ 代入方势垒精确隧穿公式 $T(E)=\bigl[1+\frac{V_0^2\sinh^2(\kappa L)}{4E(V_0-E)}\bigr]^{-1}$，用 $1+\sinh^2 u=\cosh^2 u$ 化简并代入 $\kappa L=1$，再与朴素 $e^{-2\kappa L}$ 及含前因子渐近式 $4e^{-2\kappa L}$ 对比。
   - **完整分步演算**：代入本章边界匹配得到的精确隧穿公式 $T(E) = \left[1 + \frac{V_0^2\sinh^2(\kappa L)}{4E(V_0 - E)}\right]^{-1}$。当 $E = V_0/2$ 时 $V_0 - E = V_0/2$（即 $k = \kappa$），系数 $\frac{V_0^2}{4(V_0/2)(V_0/2)} = 1$，再由恒等式 $1 + \sinh^2 u = \cosh^2 u$ 化简并代入 $\kappa L = 1$（$\cosh(1) = \frac{e + e^{-1}}{2} \approx 1.543081$）：

     $$
     T_{\mathrm{exact}} = \frac{1}{1 + \sinh^2(\kappa L)} = \frac{1}{\cosh^2(\kappa L)}
     \quad\Longrightarrow\quad
     T_{\mathrm{exact}}(\kappa L = 1) = \frac{1}{\cosh^2(1)} \approx \frac{1}{2.381098} \approx 0.419974.
     $$

     对照两类近似公式在 $\kappa L = 1$ 处的数值：
     - **朴素衰减指数**：$T_{\mathrm{naive}} = e^{-2\kappa L} = e^{-2} \approx 0.135335$（仅为精确值的 $32.2\%$，低估逾三倍！）；
     - **含边界匹配前因子的厚势垒渐近式**：$T_{\mathrm{thick}} = \frac{16E(V_0 - E)}{V_0^2}e^{-2\kappa L} = 4e^{-2} \approx 0.541341$（仍高估 $28.9\%$，因为 $\kappa L = 1$ 尚不够厚）。
   - **结论与边界回验**：$\kappa L = 1$ 处的透射率满足 $0 < T < 1$（反射率 $R = 1 - T \approx 0.580026$）。朴素 $e^{-2\kappa L}$ 丢掉了左右边界波函数与导数连续匹配产生的前因子 $4$，即使势垒极厚（$\kappa L \to \infty$）在 $E = V_0/2$ 处仍恒差 $4$ 倍；而在 $\kappa L < \ln 2 \approx 0.693$ 时连 $4e^{-2\kappa L}$ 都会超过 $1$ 而失效。
   - **易错坑提醒**：指数因子 $e^{-2\kappa L}$ 刻画的是透射率随势垒宽度的敏感标度，定量求解绝不可省去边界连续条件匹配。

8. **【基础】为何“选两个能级起名 0 和 1”不足以证明二能级近似有效**

   - **题意与约定**：结合真实多能级量子器件的连续波函数、高阶能级与外部耦合自由度，列出验证二能级截断有效的完整物理与动力学判据。
   - **核心提示**：从真实器件处于连续或无穷维希尔伯特空间的事实出发，按初态制备、驱动频谱泄漏、子空间外读出监测、环境耗散通道与多比特门辅助自由度解纠缠五个维度检查截断充分性。
   - **完整分步演算**：任何真实物理载体（超导电路、囚禁离子、中性原子、半导体量子点或光子模式）都镶嵌在更高维甚至连续无穷维的希尔伯特空间里，单靠给其中两个本征态贴上 $|0\rangle, |1\rangle$ 的标签，并不能保证演化过程不逃逸出该二维子空间。充分论证必须逐项量化核验以下五个维度：
     - **初态制备保真度**：制备与复位协议能否在目标精度内把布居压进 $\{|0\rangle, |1\rangle\}$，不把热激发或高能态混入初态；
     - **频谱选择性与驱动泄漏**：非谐性 $|\omega_{12} - \omega_{01}|$、脉冲频宽 $\sim 1/\tau$、波形整形（如 DRAG）及跃迁矩阵元是否把门操作期间向 $|2\rangle$ 等邻近能级的泄漏压到目标错率以下；
     - **读出分辨与泄漏监测**：测量方案能否可靠区分 $|0\rangle, |1\rangle$，并识别或统计子空间外态（如 $|2\rangle$ 或双轨光子真空丢失态 $|00\rangle_{ab}$），避免把泄漏静默折叠成普通比特翻转；
     - **环境弛豫与退相干通道**：耗散、杂散电磁模、电荷或磁场噪声是否在电路深度内保持低失真，且不开启逃逸出子空间的跃迁；
     - **多比特门辅助自由度解纠缠**：凡借用振动模、谐振腔光子或 Rydberg 态实现双比特门的方案，必须证明门结束时辅助自由度完整归位、与逻辑比特彻底脱钩。
     **跨章侧重对照（物理篇 Q4 连续空间与无穷维截断视角）**：本题紧扣连续波函数与无穷维 Fock/能级梯上的子空间泄漏检验（$M^\dagger M + \boldsymbol{\lambda}^\dagger\boldsymbol{\lambda} = I_2$ 与截断收敛性）；超导 Transmon 与囚禁离子在制备/控制/读出/环境四环节的定量器件参数实例见[量子力学 Q3 第 3 题](#量子力学-q3)。
   - **结论与边界回验**：只有当上述五项误差的总预算低于目标门错率或纠错阈值时，用 $2\times 2$ Pauli 矩阵与单比特门描述器件才是受控的物理近似，而非一厢情愿的数学命名。
   - **易错坑提醒**：在仿真或实验报告中看到二维投影后的“归一化态”并不代表没有泄漏——必须单独监测子空间外占据 $1 - (P_0 + P_1)$ 或完整的三能级/多模截断收敛性。

## 配套实验册与进阶练习索引

除上述 **271 道章末自检题**（均已配齐难度分级、防剧透核心提示与四步零跳步全解）外，全书还配套了三类独立标签扩展练习与实跑资源，均不改动既有 271 题编号体系：

- **章内就地进阶练习（53 道）**：全书 26 篇正文均已在章末或核心小节就地配备独立标签练习（其中 25 章各 2 道 `练 XX-A/B`，第 12 章 3 道 `练 12-A/B/C`，合计 53 道），紧贴正文例题即时巩固；
- **本附录薄弱章盲区精练（14 道）**：针对高密度或低题密章节，在本附录对应章末增补 14 道独立标签四步零跳步练习——[第 0 章](#第-0-章)（`练 00-C/D`，三大支柱与 40 比特内存墙）、[第 5 章](#第-5-章)（`练 05-C/D`，GAD/PTM 与 $T_1/T_2/T_\phi$ 边界）、[第 13 章](#第-13-章)（`练 13-C/D/E`，DPI、无歧义判别与剩余哈希引理）、[第 14 章](#第-14-章)（`练 14-C/D/E`，Weyl 室/ZX 演算、DRAG/M3 与 Litinski 推门）、[量子力学 Q2](#量子力学-q2)（`练 Q2-C/D`，二阶 Magnus/Dyson 反例与 CSCO）以及[量子力学 Q3](#量子力学-q3)（`练 Q3-C/D`，双口径失谐/cQED 色散与 Ramsey/Hahn 回波）；
- **分主题实验册与代码实跑**：可从[实验、练习与可复现代码总览](../labs/README.md)总索引进入[基础实验册](../labs/foundations.md)、[算法实验册](../labs/algorithms.md)、[系统实验册](../labs/systems.md)、[第 15 章统计实验](../labs/practice.md)，以及[开源代码对照](software-practice.md)与[完整 SDK 实验册](../labs/sdk-validation.md)。
