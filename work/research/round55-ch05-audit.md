# 第 55 轮：第 05 章混态与信道初学者审查

范围：`handbook/05-noise-channels.md`。用 IBM Quantum Learning 的[密度矩阵基础](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics)及[信道的 Kraus 表示](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels)、Watrous《Theory of Quantum Information》核对定义与适用条件。

P1：原章第一屏直接给一般密度矩阵、厄米/正半定/迹三性质，§3 又先给 POVM、测量工具的抽象公式。对刚读完单/双比特的初学者，这相当于把结论当定义；需先用“每轮抛硬币制备 $|0\rangle$ 或 $|1\rangle$”的两乘两矩阵展示为什么不能只给一个态矢量。测量工具、完全正反例和 Choi 关系可明确标为进阶回看。

P2：§2 的叠加/混合虽然列了矩阵，没有逐格算 $\operatorname{Tr}(\rho^2)$，所以“纯度”看起来是背公式。加入 $|+\rangle$ 与 $I/2$ 的两个结果 1、1/2。

P2：§5 的四个噪声模型大量并排公式，缺“同一个输入 $|+\rangle$ 如何分别变化”的比较；至少先把一个 $p=1/4$ 的比特翻转例子算出，并说明它在该输入上看似无效，并非信道等于恒等。这一点能避免读者混淆“单个测试态统计不变”和“噪声不存在”。

现有振幅阻尼 $\gamma=0.36$ 输出 $[[0.68,0.40],[0.40,0.32]]$ 可由 Kraus 直接复算。原章对参数约定、部分转置反例和 Markov 假设边界已有保留，不应为求简化删去。
