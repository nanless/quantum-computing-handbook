# 第 02 章独立审查（修订前）

范围：`handbook/02-single-qubit.md`、`handbook/assets/bloch-sphere.svg` 与 `handbook/appendices/exercises.md` 的第 2 章题答。按多年未碰数学的入门读者逐段检查定义、代数、实验含义及图文关系；查阅下列官方课程和教材原稿，不把网页的简化表述直接当严格证明。

## 核对来源

- [IBM Quantum Learning：量子位、门与电路](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits)：二维态、Bloch 球、门作用及基测量。
- [IBM Quantum Learning：Bloch sphere](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere)：去全局相位后的参数化、球内与球面。
- [IBM Quantum Learning：测量的数学形式](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements)：投影、POVM、测量后状态的区别。
- [John Watrous, *The Theory of Quantum Information*, 第 2 章](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf)：量子测量工具及条件后态的一般定义。
- [IBM Quantum 文档：Measure qubits](https://quantum.cloud.ibm.com/docs/en/guides/measure-qubits)：计算基读出惯例；硬件叙述只保留限于具体平台的条件性表述。

## 发现

1. **P1，入口过陡。** 开头立即用复振幅与“理想预测”，尚未逐项写出 $|0\rangle,|1\rangle$ 的列向量、归一化、计算基概率及分支后态。初学者无法独立重做第一个例子。应从一组归一化的二维数字开始。
2. **P1，叠加与混合只有断言。** 第 1 节说换基可区分，却没用 $|+\rangle\langle+|$ 与 $I/2$ 的计数/矩阵算出差异；全局和相对相位也缺逐行 $H$ 变换。应建立贯穿全章的同一组态。
3. **P1，Bloch 参数化跳步。** 需要解释两个复振幅的四个实数如何经归一化与全局相位剩两个角；特别说明极点处 $\varphi$ 不唯一，以及纵坐标是 Pauli 期望、不是“粒子空间位置”。
4. **P1，门操作只列结论。** $X,Y,Z,H$ 需要至少一个“矩阵乘列向量”的完整行运算，门次序由右向左；$Y=iXZ$ 虽正确，但若直接并列会让读者误以为 $X$、$Z$ 可交换。
5. **P2，旋转门的指数级数与 SU(2) 太早。** 严格推导可保留为“进阶回看”，先用 $R_y$ 的具体矩阵和 $|0\rangle$ 的概率解说半角；同时区分全局的 $R(2\pi)=-I$ 与受控分支相位。
6. **P1，测量节抽象公式先于手算。** 应先完成 $Z$ 与 $X$ 基的振幅、概率、条件后态和“丢弃记录”计算，再引进 $P_k$；明确测量规则是物理公设，不由矩阵恒等式推出。
7. **P2，POVM/工具节在主线过深。** 内容基本正确，适合放进“进阶回看”并增补一次二维逐项算例；应先解释 POVM 只给统计量、工具才决定后态，再列通式。
8. **P2，采样数字缺读者可复算过程。** $p=1/2$ 时 $N=1000,10000$ 的标准差应逐项代入，说明“标准差”不是确定误差上界；设备偏差不会凭增大 shots 自动消失。
9. **P2，自检只四题，覆盖很窄。** 需补相位、矩阵作用、非选择态、Bloch 参数、POVM 和频率计算，题答写出中间步骤。
10. **图表审查。** 现有 Bloch 球 SVG 六轴点及纯混态标签在几何、符号上可用；正文需先解释三轴再放图，图题应直接告知“球面是纯态、球内是混态”，避免图被当物理三维空间。

## 修订验收重点

- 每个新符号第一次出现说明类型、维度或范围。
- 每个概率先算振幅、再算模平方，条件态与未记录结果的状态分开。
- 章节主线留给单比特实验与算术；一般工具与 SU(2) 的严格推导可读但不作为入门门槛。
- 所有新增题与本章自检一一对应；读者能用第 01 章的四则、矩阵与概率复算。
