# 第 9 轮修订：基础、量子信息与实验可验证性

> 依据：`work/research/round8-cross-foundations-information-audit.md`  
> 修改范围：`handbook/00-overview.md`、`01-math.md`、`03-multiple-qubits.md`、`04-circuits-protocols.md`、`13-quantum-information.md`、`15-practice-research.md`。  
> 未修改：`02-single-qubit.md`、`05-noise-channels.md`、`appendices/exercises.md`、`appendices/audit-log.md` 及其他共享附录。

## 1. 完成情况

第 8 轮列出的、位于本轮允许修改六章中的 **3 项 P1 与 6 项 P2 已全部落实**。另有 1 项 P2 只位于 `appendices/exercises.md` 第 5 章答案；本轮明确禁止修改该附录，因此保留给附录维护者。对应的 `05-noise-channels.md:91–106` 正文已经准确区分“转置 $T$ 是正映射”和“$T\otimes I$ 不是正映射”，不需要重复修改正文。

| 严重度 | 已修 | 本轮允许范围内遗留 |
|---|---:|---:|
| P0 | 0 | 0 |
| P1 | 3 | 0 |
| P2 | 6 | 0 |

## 2. 逐项修改

### 00｜HHL 加速对象与资源边界

- 将含混的“指数型依赖改善”改成可核查表述：在稀疏或可高效访问、条件数和精度受控、输出限于解态或其可观测量时，对矩阵维数 $N$ 的依赖可降为 $\operatorname{polylog}(N)$。
- 明确 HHL 通常不输出完整经典解向量。
- 增加 HHL 原始 PRL 论文 DOI。

### 01｜渐近增长率

- 把逐点严格不等式改为

  $$
  1\prec\log n\prec n\prec n\log n\prec n^2\prec2^n\prec n!,
  $$

  并定义 $f\prec g$ 表示 $f=o(g)$。
- 明说这是 $n\to\infty$ 时的增长率比较，不要求每个有限 $n$ 都满足严格大小关系。

### 03｜CHSH 假设与原始文献

- 用测量设置独立与 Bell 局域性替代“局域性 + 预先确定结果”的含混说法。
- 增加因子分解公式

  $$
  p(A,B\mid a,b,\lambda)
  =p(A\mid a,\lambda)p(B\mid b,\lambda),
  $$

  并用平实文字解释公式。
- 明确随机局域模型也受 CHSH 约束；确定性响应可视为扩充隐藏变量后的等价表示。
- 增加 Clauser–Horne–Shimony–Holt 1969 原始论文 DOI；保留 Bell 1964 引用。

### 04｜不可克隆证明的全局相位

- 不再先断言复内积 $c=c^2$ 只有 $c=0,1$，而是直接比较内积模：

  $$
  |\langle\phi|\psi\rangle|
  =|\langle\phi|\psi\rangle|^2.
  $$

- 明确 $|c|=0$ 是正交态，$|c|=1$ 是只差全局相位的同一物理射线；被禁止的是 $0<|c|<1$ 的不同非正交态。

### 13｜相对熵与 Holevo 界

- 将数据处理的直觉限定为“按相对熵衡量的信息不增加”，并指出相对熵对应多副本、非对称假设检验；单样本等先验成功率由迹距离刻画。
- Holevo 段新增

  $$
  I_{\rm acc}\le\chi\le\log_2d.
  $$

- 由 $d=2^n$ 推出：无预共享纠缠、只发送 $n$ 个量子比特时，可访问经典信息不超过 $n$ bit。
- 超密编码说明显式计入预共享 Bell 对，避免看似违反无辅助模型的维数上界。

### 15｜实验统计、见证与过程层析

- 在 plug-in 标准误后增加适用边界：极端比例或小样本时使用 Wilson、Jeffreys 或精确二项区间；有漂移或相关 shots 时使用时间分块或保留相关性的重采样。
- Bell 见证区分真实 $f$ 与估计量 $\hat f$：实验声称纠缠时，应让单侧置信下界超过 $1/2$，并计入 SPAM 系统误差；点估计刚越阈值不够。
- 将“噪声通道层析的最小版本”改名为“弛豫与退相位的三轴诊断”。
- 明确三条同轴衰减曲线不是信息完备过程层析，不能识别一般信道的轴间混合和平移。
- 给出单比特过程层析的教学方案：以 $|0\rangle,|1\rangle,|+\rangle,|+i\rangle$ 为四个线性独立输入，对每个输出测 $X,Y,Z$，重构 Choi 矩阵或 Pauli transfer matrix，并报告物理性、统计与 SPAM 限制。
- 增加 Qiskit Experiments 过程层析官方文档与 NIST 二项比例置信区间来源。

## 3. 复算与一致性检查

### 3.1 渐近关系

逐对检查：

- $1/\log n\to0$；
- $\log n/n\to0$；
- $n/(n\log n)=1/\log n\to0$；
- $n\log n/n^2=\log n/n\to0$；
- $n^2/2^n\to0$；
- $2^n/n!\to0$。

因此新链条在 $o(\cdot)$ 意义下成立，也不再与 $n=1,2$ 的有限值冲突。

### 3.2 不可克隆内积

输入态对的内积模为 $|c|$。理想克隆后，两个输出副本使内积变为 $c^2$，其模为 $|c|^2$。酉性要求 $|c|=|c|^2$，所以只有 0 或 1。取 $|\phi\rangle=i|\psi\rangle$ 时 $|c|=1$，正确归入同一物理态。

### 3.3 Holevo 维数界

对 $d$ 维平均态，$S(\bar\rho)\le\log_2d$，且每个 $S(\rho_x)\ge0$，所以

$$
\chi=S(\bar\rho)-\sum_xp_xS(\rho_x)\le\log_2d.
$$

与 $I_{\rm acc}\le\chi$ 合并即得新增公式。原有两例仍正确：正交单比特编码达到 1 bit；等概率 $|0\rangle,|+\rangle$ 的 $\chi\approx0.601$ bit。

### 3.4 Bell 见证

任意两比特可分纯态与最大纠缠态的重叠不超过 $1/2$，凸组合也不超过该上界。因此真实 $f_{\Phi^+}>1/2$ 的判据不变。新增内容只要求有限样本判定使用下置信界，没有改变见证公式或根保真度换算 $F=\sqrt f$。

### 3.5 过程层析信息完备性

一般单比特保迹信道可写为 Bloch 仿射映射 $\vec r\mapsto A\vec r+\vec t$，其中 $A$ 有 9 个实参数，$\vec t$ 有 3 个。原三条曲线只观察三个特定输入—输出同轴分量，不能确定全部 12 个参数。四个线性独立输入配合每个输出的 $X,Y,Z$ 层析提供重构一般单比特信道所需的信息；是否满足 CP/TP 仍需在拟合中检查。

## 4. 引用核对

- HHL：A. W. Harrow, A. Hassidim, S. Lloyd, *Physical Review Letters* 103, 150502 (2009)，[DOI](https://doi.org/10.1103/PhysRevLett.103.150502)。
- CHSH：J. F. Clauser, M. A. Horne, A. Shimony, R. A. Holt, *Physical Review Letters* 23, 880–884 (1969)，[DOI](https://doi.org/10.1103/PhysRevLett.23.880)。
- Holevo：正文原有 A. S. Holevo 1973 原始论文与 Watrous 教材支持 $I_{\rm acc}\le\chi\le\log d$。
- 过程层析：[Qiskit Experiments `ProcessTomography`](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.ProcessTomography.html) 明确说明多个输入态、多个测量基和信道重构。
- 二项区间：[NIST/SEMATECH e-Handbook](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) 明确指出小样本或少失败数时，简单对称正态区间可能不准确。

## 5. 残余事项

- 本轮没有发现新增 P0/P1/P2。
- 唯一未落地项是共享练习附录第 5 章答案的自洽措辞，因为本轮明确禁止修改 `appendices/exercises.md`。它不含数值错误，第 05 章正文也已经准确；建议附录维护者在自己的轮次补成“$T$ 正但 $T\otimes I$ 非正，所以 $T$ 不完全正”。
