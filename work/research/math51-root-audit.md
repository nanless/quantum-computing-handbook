# 数学工具章第 51 轮主审：学习路径与可手算性

范围：`handbook/01-math.md`、先修自测与第 1 章题答。读者设定为只记得中学代数、数年未系统学数学的人。以下是教学缺口，不代表现有式子均有错误；三路独立只读审稿另有报告。

## 关键缺口

| 级别 | 位置 | 具体问题与拟补台阶 |
|---|---|---|
| P2 | §1 | `a+bi` 之后立即到 `re^{iθ}`，复数乘法、共轭、模的几何意义、角度与弧度、`1+i=√2e^{iπ/4}` 均未手算。补四则、坐标图和相位乘法例；让读者先会数，再看 Euler 形式。 |
| P2 | §2 | ket、bra 和内积在向量加法/数乘、行列形状、转置/共轭转置之前出现。补二维逐项运算、`T` 与 `†` 的区别、行乘列的完整算式和范数归一化为什么除以长度。Cauchy–Schwarz 证明标为进阶可回读，避免打断第一遍主线。 |
| P2 | §3–6 | 基、Kronecker `δ`、本征值、外积、迹均基本只有定义；从 `X(a,b)^T` 的两行方程解 `λ=±1`，从 `|+〉〈+|` 逐格做外积、取迹，并在基变换中算出坐标和概率。不要用尚未定义的行列式。 |
| P2 | §7 | 张量积给出四分量定义，却没有把矩阵张量积写成四块、比较 `H⊗I` 与 `I⊗H` 的 4×4 矩阵；补逐项和位序核对。 |
| P2 | §8 | 条件概率与 Bayes 只有抽象式，没有样本空间、交集与分母的具体计数表；`Var(\hat p)=p(1-p)/N` 缺从指示变量和独立性来的推导。补 1000 人筛查的完整计数表、±1 期望例和样本频率方差。 |
| P2 | §9 | `O/Ω/Θ/o`、`n` 和 `N=2^n` 过于密集。先用 `3n²+7n+2` 比较增长，再精确定义“从某规模起有常数界”；给 `n=20,N=2^20` 的查询与门成本对照，并把进阶术语与基础读法分层。 |

## 来源与边界

[Watrous《The Theory of Quantum Information》数学预备章](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf)把复向量、内积、范数和基作为量子信息计算的底层，并明确它本身是给已有线性代数基础读者的复习，而非零基础教程；本章应比其给出更多中间步骤。[IBM Quantum Learning 的内积与投影课程](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/inner-products-and-projections)逐项展示列向量到 bra、内积求和及长度；[多系统的经典信息课程](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/classical-information)给张量积的具体分量定义。[MIT 18.03 的复数极坐标讲义](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/6ae2bc2f86967cd3cf686b0b2e782544_MIT18_03SCF11_s6_5text.pdf)核对极坐标与 Euler 形式。这些权威资料提供正确性对照，章节先后与手算细度是本书面向读者的编辑判断。

## 实施约束

保持第 01 章与第 02 章、Q1 的统一基序和符号约定；勿把数学章变成纯粹公理教材或跳过量子应用。新图用轴名、弧度、色彩加线型双重标注；长表在手机容器内横滑，不产生整页横溢。所有新增自检题需与答案一一对应。
