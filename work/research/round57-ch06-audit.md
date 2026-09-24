# 第 6 章修订前审查（2026-09-24）

范围：`handbook/06-algorithmic-primitives.md` 及练习附录第 6 章。重点是入门可算性、承诺条件和资源口径，不把本轮审查外推为全书审查。

## 一手核对资料

- [Watrous，IBM Quantum Learning：查询模型](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/query-model-of-computation)：oracle 的定义与“查询数忽略构建成本”的界限。
- [Watrous，IBM Quantum Learning：相位估计流程](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure)：QFT、控制幂与有限精度。
- [Watrous，IBM Quantum Learning：Grover 算法](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/grover-algorithm-description)：相位查询、反射与搜索条件。
- [Brassard 等，*Quantum Amplitude Amplification and Estimation*](https://arxiv.org/abs/quant-ph/0005055)：一般初态下的振幅放大及 $A,A^{-1}$ 成本。
- [Cleve 等，*Quantum Algorithms Revisited*](https://arxiv.org/abs/quant-ph/9708016)：相位估计与控制幂。
- [IBM Quantum Documentation：乘积公式模拟](https://quantum.cloud.ibm.com/docs/en/tutorials/multi-product-formula)：$e^{-iHt}$、分片误差和线路深度的区别。
- [Beals 等，*Quantum Lower Bounds by Polynomials*](https://arxiv.org/abs/quant-ph/9802049)：查询下界的多项式方法。

## 问题与改法

| 优先级 | 位置 | 发现 | 改法 |
|---|---|---|---|
| 高 | 引言 | 宣称“六个结构”，正文却含多个额外结构，且没有先给“输入—承诺—可问 oracle—输出—错误—成本”的读题框架。 | 给统一算法卡片，明确 oracle 不是免费物理门。 |
| 高 | §1–3 | 可逆 oracle 到回踢、Deutsch–Jozsa 和 BV 的代数已正确，但对久未看数学者跳过了 $x\cdot y$、从两分支消去一分支的手算。 | 逐位解释二进制内积，添加 $n=1$ 的最小干涉算例，并明确承诺只允许特定输入。 |
| 高 | §4 | 通用振幅放大把 $A|0\rangle$ 抽象给出，却没有说“好/坏子空间”的投影定义、$A$ 和 $A^\dagger$ 怎么进入反射；$\Theta(\sqrt{N/M})$ 只属于均匀搜索。 | 从 4 项实例倒回二维旋转，给通用成本 $O(1/\sqrt a)$ 次 $A,A^\dagger$ 和标记检查，并区分零好项与未知 $a$。 |
| 中 | §5 | QFT 虽有 $N=4$ 的一列，但没解释叠加输入为何干涉、单位矩阵为何幺正及“电路可实现”依赖门集精度。 | 添加周期相位态经逆 QFT 聚焦的 $N=4$ 例与正交和式，说明精确抽象门模型。 |
| 中 | §6 | 相位估计分布讲得很细，但主线先引入较难的正弦核和统一界；相位与能量关系、控制幂成本的物理含义欠直观。 | 把易算 $U=Z$、$\phi=1/4$ 提前，再将正弦推导标为进阶；加能量解释及资源表。 |
| 高 | 全章 | 作为“算法共同骨架”的入门章，正文没有哈密顿量模拟的基本例子和资源口径，读者进入应用章前缺少台阶。 | 添加一节：输入 $H,t,|\psi_0\rangle$，目标 $e^{-iHt}$，对易与不对易小例子，乘积公式误差与读出成本。 |
| 中 | §7–9 | 反计算只用三步口号，成功概率的验证条件未量化；下界方法偏研究综述。 | 加两比特可逆计算的垃圾位/反计算实际振幅例子；下界仍保留进阶入口但标清不作为入门门槛。 |
| 中 | 自检 | 8 题多集中于原理复述，缺少 oracle 表、QFT 干涉、P​​E 误差与模拟步数口径的练习。 | 扩充对应手算题，附录答案写完整中间步骤。 |

现有核心公式抽样核对未见直接错误；主要缺陷是前提散落、例子与公式间断层，以及模拟缺席。
