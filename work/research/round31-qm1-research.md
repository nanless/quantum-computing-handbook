# 第 31 轮：Q1“从实验认识量子态”调研与撰写记录

> **初稿快照说明（第 33 轮补记）**：本报告保留第 31 轮的原始研究过程，其中把“留下路径记录后丢弃记录”直接写成 $\rho=I/2$，漏写了记录态完全可区分（正交）且两路径等权的条件；所引 Stanford-hosted 8.051 文件也实际是学生笔记。正文、题目与答案已在第 33 轮补上一般重叠度 $\gamma=\langle d_1|d_0\rangle$ 的处理，并把该来源替换为 MIT OCW 8.05 官方讲义。详见 [`round33-qm1-fixes.md`](round33-qm1-fixes.md)。

日期：2026-09-22  
新增正文：`handbook/quantum-mechanics/01-experiments-states.md`  
答案草稿：`work/research/round31-qm1-answers.md`

## 目标与边界

本章定位在现有第 01 章数学之后、第 02 章单量子比特之前。它不扩写量子物理史，也不预讲完整测量工具、开放系统或量子诠释；目标是让初学者从两组可复算实验理解状态、振幅、Born 规则、相位、互补基以及叠加与混合的区别。

本轮完整阅读了 `handbook/STYLE.md`，并遵守以下约束：先给操作对象再给术语；概率先算振幅再取模平方；显式区分条件态和丢弃结果后的非选择态；表格中的 ket 使用 `\lvert` 或避免裸竖线；没有修改共享 README、附录、图片或构建文件；`sources/` 保持只读。

## 资料核查与支持范围

1. [MIT Quantum Physics I, Lecture Note 1](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/7f930e013cef9cd7dec5aa88baa83f0a_MIT8_04S16_LecNotes1.pdf)（2016；访问 2026-09-22）。
   - 支持范围：讲义第 7–8 页明确介绍平衡分束器、Mach–Zehnder 两路重合、两个探测器以及单光子逐个输入仍呈现的干涉；第 9 页继续给出叠加系数与模平方概率。
   - 本章没有照搬其相位约定，而是先声明 $B=H$ 的有效端口约定，再独立推导 $P_0=(1+\cos\phi)/2$、$P_1=(1-\cos\phi)/2$。
2. [MIT 22.51 Course Notes, Chapter 7: Mixed States](https://ocw.mit.edu/courses/22-51-quantum-theory-of-radiation-interactions-fall-2012/00e219fe9b8a81b64613f1428e87cb00_MIT22_51F12_Ch7.pdf)（2012；访问 2026-09-22）。
   - 支持范围：状态与重复制备系综的关系、纯态投影、混态的概率凸组合、迹为 1 与正性。
3. [Born, “Zur Quantenmechanik der Stoßvorgänge”](https://doi.org/10.1007/BF01397477), *Zeitschrift für Physik* 37, 863–867 (1926)。
   - 支持范围：波函数概率解释的原始历史来源。正文谨慎区分历史来源与现代一般 Born 公设，不声称一般有限维测量公式已由该短文完整给出。
4. [MIT 5.61, The Postulates of Quantum Mechanics](https://www.ocw.mit.edu/courses/5-61-physical-chemistry-fall-2007/e69210652de904428188a04bd0345440_lecture10.pdf)（2007；访问 2026-09-22）。
   - 支持范围：现代课程将测量结果、概率密度和测量规则列为量子力学公设。用于支撑“Born 规则不是线性代数定理”。
5. [Gerlach and Stern 1922 原始论文英译](https://arxiv.org/abs/2301.11343)（译文 2023，明确给出原文 *Zeitschrift für Physik* 9, 349–352）。
   - 支持范围：银原子束、非均匀磁场及空间量子化的原始实验事实。正文明确原实验的当时解释与现代自旋解释不完全相同。
6. [Stanford-hosted 8.051 Quantum Physics II notes](https://web.stanford.edu/~lindrew/8.051.pdf)（访问 2026-09-22）。
   - 支持范围：银原子基态有效二态、磁场梯度、重复同轴 Stern–Gerlach 筛选以及不同轴基展开。

## 关键设计与独立复算

### 1. 干涉仪相位约定

采用

$$
B=\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix},
\qquad
U_\phi=\operatorname{diag}(1,e^{i\phi}).
$$

独立相乘得

$$
B U_\phi B|0\rangle
=\frac12\begin{bmatrix}1+e^{i\phi}\\1-e^{i\phi}\end{bmatrix}.
$$

两概率之和为

$$
\frac{1+\cos\phi}{2}+\frac{1-\cos\phi}{2}=1.
$$

正文说明物理分束器常把反射相位写为 $i$；固定相位与端口标签可以吸收入基和相位零点。本章结论依赖全程一致的约定，不宣称只有该矩阵“真实”。

### 2. 无测量、丢弃结果、条件测量

- 无路径记录：保留 $|0\rangle\langle1|$ 相干项，输出随 $\phi$ 变化。
- 有路径记录但丢弃结果：$\rho=I/2$，经 $B$ 后仍为 $I/2$，输出恒为各半。
- 知道路径结果：条件态分别为 $|0\rangle,|1\rangle$；各自经 $B$ 后也给各半，但这是两个分组后的条件统计。

三者在正文单列，并另提醒“阻挡一路”还涉及吸收和对存活样本重新归一化。

### 3. Stern–Gerlach 计数

未偏振 $N$ 个原子依次保留 $z+$、保留 $x+$，再测 $z$：平均数量依次为 $N/2$、$N/4$、最终两支各 $N/8$。正文同时报告每一步的条件通过率和相对原始束流的数量，避免把“第二次同轴测量概率为 1”误读为总通过率 1。

### 4. 叠加与混合

独立展开

$$
|x+\rangle\langle x+|
=\frac12\begin{bmatrix}1&1\\1&1\end{bmatrix},
\qquad
\frac12|z+\rangle\langle z+|
+\frac12|z-\rangle\langle z-|
=\frac I2.
$$

两者 $Z$ 基概率相同，$X$ 基概率分别为 $(1,0)$ 与 $(1/2,1/2)$。该例直接连接“无知混合”与可观测相干项，不靠哲学措辞区分。

## 完成项

- 新增一章正文，含制备—变换—测量框架、归一化算例、Mach–Zehnder 完整振幅推导、三种路径处理、全局/相对相位、Stern–Gerlach 顺序筛选、互补基、叠加与混合、状态与制备记录的边界。
- 按主审约定引用 `../assets/qm-interference.svg`；正文图题明确只表示“无路径记录”的情形。
- 设置 7 道自检题，覆盖数值归一化、干涉推导、测量分支、顺序筛选、密度矩阵、相位和公设含义。
- 另写 7 份逐步答案草稿，未修改共享练习附录。

## 留给交叉审校的事项

- SVG 由主审另行制作，本轮只按约定公式和相对路径引用，未做成图后的明暗主题、窄屏或文字遮挡验收。
- 主审整合答案时需创建 `#量子力学-q1` 锚点，并复核章内链接。
- 导航、README、术语表和构建入口不在本轮写权限内，需要主审统一接入。
