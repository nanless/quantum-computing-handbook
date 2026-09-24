# 第 33 轮｜Q1 定点修订记录

日期：2026-09-23  
依据：`work/research/round32-qm14-crossreview.md`  
正文：`handbook/quantum-mechanics/01-experiments-states.md`

本轮只处理交叉审查确认的 Q1 问题，并同步 Q1 自检答案。没有修改其他量子力学章节。

## 问题与修复

| 原等级 | 问题 | 修复结果 |
|---|---|---|
| P1 | 把“存在可区分路径记录”直接等同于 $\rho=I/2$，漏掉记录态正交和两路径等权条件 | 已改为一般记录态重叠 $\gamma=\langle d_1|d_0\rangle$；明确只有 $\gamma=0$ 且两路等权时才有 $I/2$ |
| P2 | $\rho$、$U\rho U^\dagger$ 和测量概率在首次使用前没有定义 | 已在 2.2 节开头补纯态、概率混合、酉变换和投影测量概率四条最小规则 |
| P2 | Stanford 个人页面上的 8.051 学生笔记被用作课程讲义来源 | 已换成 Barton Zwiebach 的 MIT OCW 8.05 官方 Chapter 2 讲义 |

### 1. 路径记录不再被写成二元开关

修订后的正文从联合态出发：

$$
|\Psi\rangle
=\frac{|0\rangle|d_0\rangle+e^{i\phi}|1\rangle|d_1\rangle}{\sqrt2},
\qquad
\gamma=\langle d_1|d_0\rangle.
$$

展开 $|\Psi\rangle\langle\Psi|$ 后，$|0\rangle\langle1|$ 项的记录部分在忽略记录时给出 $\langle d_1|d_0\rangle$，所以

$$
\rho_{\rm path}(\phi)
=\frac12
\begin{bmatrix}
1&\gamma e^{-i\phi}\\
\gamma^*e^{i\phi}&1
\end{bmatrix}.
$$

由本章的平衡分束器 $B=H$ 直接相乘，输出对角元为

$$
P_0=\frac{1+\operatorname{Re}(\gamma e^{-i\phi})}{2},
\qquad
P_1=\frac{1-\operatorname{Re}(\gamma e^{-i\phi})}{2}.
$$

独立核对三个边界：

- $\gamma=1$：两条路径留下相同记录，恢复 $(1\pm\cos\phi)/2$；
- $\gamma=0$：记录态正交、完全可区分，且本例两路等权，得到 $\rho=I/2$ 与 $P_0=P_1=1/2$；
- $\gamma=0.6$ 为实数、$\phi=0$：$P_0=0.8$、$P_1=0.2$，展示部分记录只削弱干涉而不必完全消除。

上述限定已同步到三情形表、常见误解、自检第 3 题、共享附录 Q1 答案第 3 题与 `round31-qm1-answers.md`。表格内的模使用 `\lvert\gamma\rvert`，避免裸竖线的 Markdown 兼容性风险。第 33 轮当时把全局相位符号改为 $\chi$，以避免与本节记录态重叠 $\gamma$ 混用；第 34 轮随后发现全书符号表已把 $\chi$ 固定用于 Holevo 量，因此第 35 轮又把全局相位统一改为 $\theta_{\rm g}$。这条补记保留实际修订历史，不把第 33 轮初稿状态改写成从未出现过。

### 2. 密度矩阵首次出现已有最小入口

首次使用前现在明确给出：

$$
\rho_{\rm pure}=|\psi\rangle\langle\psi|,
\qquad
\rho_{\rm mix}=\sum_jp_j|\psi_j\rangle\langle\psi_j|,
$$

$$
\rho\longmapsto U\rho U^\dagger,
\qquad
p(m)=\langle m|\rho|m\rangle.
$$

正文还用一条交叉项解释记录态内积怎样进入约化态，并回链主篇第 03 章真实存在的偏迹锚点 `#4-局部操作不能单独揭示整个纠缠态`。这使初学者能够复算 $B\rho B^\dagger$，又不在 Q1 提前展开完整密度算符理论。

### 3. 来源身份修正

删除正文和参考资料对 Stanford 个人页面学生笔记的依赖，替换为：

- Barton Zwiebach, MIT OpenCourseWare 8.05, *Spin One-Half, Bras, Kets, and Operators*（2013；访问 2026-09-23）：<https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/a56c316e4ec548d8bd0a554fac9a74e8_MIT8_05F13_Chap_02.pdf>

该官方讲义第 1 节明确覆盖银原子、非均匀磁场、同轴连续筛选以及 $z$、$x$、$z$ 顺序 Stern–Gerlach 实验，直接支持正文相关陈述。

`round31-qm1-research.md` 保留原始研究过程，但已在开头增加“初稿快照说明”，如实指出第 33 轮修正了正交条件和来源身份，避免旧报告进入离线包后造成误读。

## 文件清单

- 修改 `handbook/quantum-mechanics/01-experiments-states.md`
- 修改 `handbook/appendices/exercises.md` 中且仅中“量子力学 Q1”答案段
- 修改 `work/research/round31-qm1-answers.md`
- 在 `work/research/round31-qm1-research.md` 开头补历史快照说明
- 新增本报告

## 结论

第 32 轮针对 Q1 的 1 项 P1、2 项 P2 均已落实。一般记录态公式、边界条件、数值反例、题答和来源身份现已一致；本轮未留下已知未完成项。
