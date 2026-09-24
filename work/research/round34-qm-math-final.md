# 第 34 轮｜Q2/Q3 数学与共享符号有限终审

日期：2026-09-23  
性质：只读复核；本轮未修改正文、答案或共享附录。  
范围：Q2、Q3 第 32 轮所列三项 P2 修复，以及 `appendices/notation.md` 中与基础篇直接相关的共享符号。

## 结论

| 范围 | P0 | P1 | P2 |
|---|---:|---:|---:|
| Q2/Q3 三项既有修复 | 0 | 0 | 0 |
| 共享符号交叉核对 | 0 | 0 | 1 |
| 合计 | **0** | **0** | **1** |

Q3 的表格、偏迹先修和术语解释三项均已正确闭环。有限终审另发现一项与 Q1 第 33 轮新增符号有关的共享约定冲突，需由主审定点改名；没有发现影响公式结论的 P0/P1。

## 唯一未闭环项

### P2｜Q1 把共享符号 $\chi$ 又用作全局相位角

位置：

- `handbook/quantum-mechanics/01-experiments-states.md` 当前约第 303–314、478 行；
- `handbook/appendices/exercises.md` 的 Q1 答案第 6 题，当前约第 963–964 行；
- `work/research/round31-qm1-answers.md` 第 6 题。

共享符号表 `handbook/appendices/notation.md` 明确约定

$$
\chi=\text{Holevo 量}.
$$

但 Q1 第 33 轮为避免记录态重叠 $\gamma$ 与全局相位重名，把全局相位改成了 $e^{i\chi}$。局部公式本身没有数学错误，不过这会让同一个全书符号同时表示 Holevo 量和相位角，不符合共享符号约定。

精确修法：把 Q1 正文、自检第 6 题、共享答案和答案草稿中的全局相位统一改为不承担全书固定含义的 $\theta_{\rm g}$，即

$$
|\psi'\rangle=e^{i\theta_{\rm g}}|\psi\rangle.
$$

同时把 `round33-qm1-fixes.md` 中“改为 $\chi$”的记录同步改成 $\theta_{\rm g}$。不需要改符号表，也不应改变本节记录态重叠 $\gamma=\langle d_1|d_0\rangle$。

## 已通过的三项修复

### 1. Q3 平台表的竖线

第 451–458 行逐行统计均恰有 4 个 Markdown 列分隔符。表内 ket 已写成 `\lvert`：transmon、偏振、双轨及真空/多光子态均不再含裸 ket 竖线。源文件符合 `STYLE.md`，也消除了通用 Markdown 渲染器的兼容性风险。

### 2. Q3 偏迹首次出现处

第 424–433 行现在先给白话功能，再给定义

$$
\rho_S=\operatorname{Tr}_E(|\Psi\rangle\langle\Psi|)
=\sum_j{}_E\!\langle e_j|\Psi\rangle\langle\Psi|e_j\rangle_E.
$$

代入

$$
|\Psi\rangle=\alpha|0\rangle|E_0\rangle+\beta|1\rangle|E_1\rangle
$$

后，非对角元分别为 $\alpha\beta^*\langle E_1|E_0\rangle$ 与其复共轭，次序正确。回链锚点 `../03-multiple-qubits.md#4-局部操作不能单独揭示整个纠缠态` 已在目标文件中确认存在。

### 3. Q3 首次术语与文字清理

- Bloch–Siegert 位移已解释为 RWA 丢弃的反向旋转快项造成的小共振频移；
- Rydberg 态首次出现即解释为主量子数高、相互作用强的原子高激发态；
- Zeeman 态在平台表中解释为由磁场分裂并按磁量子数区分的能级；
- “Gibbs 分布”已回指第 3 节的热平衡 Boltzmann（Gibbs）分布；
- “处处处于”的重复字已不存在。

这些补充都没有改变原有公式或引入新的先修负担。

## Q2/Q3 共享符号抽查

- Q2 用 $\mathcal H$ 表示 Hamiltonian，与 Hadamard 门 $H$ 分开；Q3 在首次换用普通 $H$ 时明确声明局部约定。
- $f$ 为 Hz、$\omega$ 与 $\Omega$ 为 rad/s，$\omega=2\pi f$、$\hbar\omega=hf$，与共享符号表一致。
- Q3 的 $\Delta=\omega_0-\omega_d$、$\Omega_R=\sqrt{\Omega^2+\Delta^2}$ 与符号表一致。
- Q3 明确 $Z_E=-Z$、$Y_E=-Y$；共享符号表也记录了同一约定。
- Q2 的 $\langle A\rangle$、$\Delta A$、$[A,B]$ 与共享符号表一致。

除 $\chi$ 重用外，本轮限定范围内未发现新的 P0/P1/P2。
