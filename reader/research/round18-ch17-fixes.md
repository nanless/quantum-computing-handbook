# 第 18 轮修订记录：计算模型与新增算法

日期：2026-09-22

## 1. 结论

`work/research/round17-cross-ch17-math-audit.md` 的 7 项 P2 已全部落实。修改范围为：

- `handbook/07-algorithms.md`；
- `handbook/08-applications.md`；
- `handbook/17-computation-models.md`；
- `handbook/appendices/exercises.md` 的第 17 章答案。

复核后无需修改 `handbook/16-advanced-algorithms-verification.md`：第 16 章的 QSP、委托验证和跨尺度验证本身没有数学或事实问题。也无需修改 `handbook/README.md`：本轮将第 17 章自检第 10 题替换为本章已讲授的数字—模拟比较题，因而不再要求读者把第 16 章作为必修先修；README 现有“04、07、09、14”路线仍与主体内容一致。

未修改第 18、19 章、审校日志或 `sources/`。

## 2. 七项修订

### 2.1 qDRIFT 条件、符号与误差口径

在 `handbook/07-algorithms.md`：

- 把“随机抽取 Pauli/酉项”改为“随机抽取可高效演化的归一化 Hermitian 项；Pauli 串为特例”；
- 增加一般形式

  $$
  H=\sum_jh_jH_j,
  \quad H_j=H_j^\dagger,
  \quad \|H_j\|=1,
  $$

  $$
  p_j=\frac{|h_j|}{\lambda},
  \quad \lambda=\sum_j|h_j|,
  $$

  以及抽样后施加

  $$
  e^{-i(\lambda t/N)\operatorname{sgn}(h_j)H_j};
  $$

- 明确负系数的符号不能被绝对值抽样概率吃掉；
- 明确 $N=O(\lambda^2t^2/\epsilon)$ 对应的是以金刚石范数约束的平均信道误差，并用白话解释金刚石范数会连同参考系统考察最坏情形。

正系数例 $0.6X+0.8Z$ 的原推导保持不变。

### 2.2 TTS 定义域、边界值与来源

在 `handbook/17-computation-models.md`：

- 给重复公式增加 $0<p_s<1$、$0<\delta<1$；
- 单列 $p_s=0$ 时有限重复无效、$p_s=1$ 时 $R=1$；
- 提醒有限样本估出的 $p_s$ 需要传播不确定性，不能只代入点估计；
- 增列 Rønnow 等人的一手 TTS 基准论文。

内部算例仍有

$$
\left\lceil\frac{\log0.01}{\log0.8}\right\rceil=21,
\qquad
21\times20\,\mu\mathrm{s}=420\,\mu\mathrm{s}.
$$

### 2.3 收紧绝热—门模型等价的适用条件

将原来的“明确路径构造”改为“高效可描述的局域 Hamiltonian 路径”，并显式把目标精度、Hamiltonian 范数与导数、演化时间列入资源计数。保留原有四条工程边界，不把模型级多项式等价改写成退火器性能保证。

### 2.4 Grover 迭代改为精确最佳整数 12

正文、自检和答案同步改写。对 $N=256$、唯一目标，使用

$$
\theta=\arcsin(1/16),
\qquad
p_r=\sin^2[(2r+1)\theta].
$$

连续最优点为

$$
\frac{\pi}{4\theta}-\frac12
=12.0581803105\ldots,
$$

故最佳整数为 $r=12$。独立复算：

$$
p_{12}=0.9999470421\ldots,
\qquad
p_{13}=0.9861862401\ldots.
$$

正文仍保留 $\pi\sqrt N/4\approx12.6$，但明确它只是渐近尺度，不能机械向上取整。教学重点改成“12 次 oracle 查询也不等于 12 次普通加密”。

### 2.5 消除第 17 章自检第 10 题的先修错位

采用第 17 轮报告的方案 2：不把第 16 章强制加入先修，而把原来要求复述 Mahadev/LWE、多证明者和有限量子客户端的题，替换成正文已经完整讲授的题：

> 为什么数字—模拟方案“更浅”仍不自动等于更快或更准？

答案从四个方面给出可核查口径：比较基线、时间成本、误差成本、验证/通用性与共同资源口径。这样第 17 章仍可按 README 的现有路线独立学习；第 16 章的详细信任模型继续作为延伸链接。

### 2.6 中文术语统一

在第 17 章正文及第 17 章答案中统一：

- `schedule` → “调度函数”，首次结合 $s(t)$ 解释；
- `observable` → “可观察量”；
- `password primitive` → “密码原语”，并解释为组成协议的基础运算。

`time to solution` 与 `refocusing` 原文已有中文解释，保留中英对照。

### 2.7 三顶点 QAOA 直接来源

在 `handbook/08-applications.md` 参考起点增列 Wang、Hadfield、Jiang、Rieffel 的一般图 $p=1$ MaxCut 解析论文。正文公式与数值未改，因为复算正确：

$$
1+\frac{3\sqrt3}{8}
=1.6495190528\ldots.
$$

## 3. 题答同步

第 17 章仍为 10 道自检，正文题号与 `appendices/exercises.md` 第 17 章答案一一对应：

| 题号 | 主题 | 同步状态 |
|---:|---|---|
| 1 | 各模型的程序载体 | 已统一“调度函数/可观察量” |
| 2 | MBQC 投影 | 原答案正确，保留 |
| 3 | 已知 Pauli 伴随与前馈 | 原答案正确，保留 |
| 4 | 二能级绝热谱 | 原答案正确，保留 |
| 5 | 模型等价与退火优势 | 原答案正确，保留 |
| 6 | TTS 数值 | 原答案正确，正文补定义域 |
| 7 | echo | 原答案正确，保留 |
| 8 | 模拟器外推证据 | 已统一“可观察量” |
| 9 | Grover 精确整数与 oracle 成本 | 正文、题目、答案全部改为 12 |
| 10 | 数字—模拟“更浅”的资源边界 | 新题与新答案一致 |

## 4. 复算与检查

独立复算结果：

- MBQC 两支概率均为 $1/2$，输出为 $X^mH|\psi\rangle$；
- 二能级绝热最小谱隙为 $\sqrt2$；
- TTS 重复数为 21；
- echo 得 $e^{-iJtZ_2Z_3}$；
- 三顶点路径 QAOA 为 $1.6495190528\ldots$；
- qDRIFT 例的抽样概率为 $3/7,4/7$，平均一阶生成项为 $H$；
- QLSA 例的 $|x\rangle=(2|0\rangle+|1\rangle)/\sqrt5$、$\langle Z\rangle=3/5$；
- QSP 的 $W(x)^2$ 左上元为 $2x^2-1$；
- Grover 的 $r=12$ 比 $r=13$ 更接近第一次概率峰值。

静态回归包括：修改文件的显示公式定界符成对、代码围栏成对、本地 Markdown 链接可解析、第 17 章题目和答案均为 10 项、无合并冲突标记。工作目录不是 Git 仓库，因此无法使用 Git 差异检查。

## 5. 一手来源

- E. Campbell, [A random compiler for fast Hamiltonian simulation](https://arxiv.org/abs/1811.08017)（qDRIFT）。
- D. Aharonov et al., [Adiabatic Quantum Computation is Equivalent to Standard Quantum Computation](https://arxiv.org/abs/quant-ph/0405098)（绝热—门模型等价）。
- T. F. Rønnow et al., [Defining and detecting quantum speedup](https://arxiv.org/abs/1401.2910)（TTS）。
- M. Boyer et al., [Tight bounds on quantum searching](https://arxiv.org/abs/quant-ph/9605034)（Grover 精确成功概率）。
- Z. Wang et al., [Quantum Approximate Optimization Algorithm for MaxCut: A Fermionic View](https://arxiv.org/abs/1706.02998)（一般图 $p=1$ QAOA）。
