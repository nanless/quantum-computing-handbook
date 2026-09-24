# Q1｜从实验认识量子态：自检答案草稿

供主审整合进 `handbook/appendices/exercises.md#量子力学-q1`。题号与 `handbook/quantum-mechanics/01-experiments-states.md` 一一对应。

1. 先算范数平方：

   $$
   \langle v|v\rangle=|1+i|^2+|\sqrt2|^2=2+2=4.
   $$

   因此

   $$
   |\psi\rangle=\frac{1+i}{2}|0\rangle+\frac1{\sqrt2}|1\rangle.
   $$

   路径概率为 $p(0)=|1+i|^2/4=1/2$、$p(1)=1/2$，和为 1。不能用 $(1+i)^2/4=i/2$ 当作概率。

2. 由

   $$
   B|0\rangle=\frac1{\sqrt2}
   \begin{bmatrix}1\\1\end{bmatrix},
   \qquad
   U_\phi B|0\rangle=\frac1{\sqrt2}
   \begin{bmatrix}1\\e^{i\phi}\end{bmatrix},
   $$

   再乘一次 $B$ 得

   $$
   B U_\phi B|0\rangle
   =\frac12
   \begin{bmatrix}1+e^{i\phi}\\1-e^{i\phi}\end{bmatrix}.
   $$

   所以 $A_0=(1+e^{i\phi})/2$、$A_1=(1-e^{i\phi})/2$。当 $\phi=\pi/3$ 时，$\cos\phi=1/2$，故 $P_0=3/4$、$P_1=1/4$，总和为 1。

3. 没有路径记录时，可以取两条路径对应同一个记录态，即 $\gamma=\langle d_1|d_0\rangle=1$。第二个分束器前是相干纯态

   $$
   (|0\rangle+e^{i\phi}|1\rangle)/\sqrt2,
   $$

   因而输出为 $(1+\cos\phi)/2$ 与 $(1-\cos\phi)/2$。若平衡分束器后的两条路径留下**完全可区分的正交记录**，则 $\gamma=0$；丢弃记录后，单看粒子的非选择态才是

   $$
   \rho=\tfrac12|0\rangle\langle0|+\tfrac12|1\rangle\langle1|=I/2.
   $$

   这里的 $I/2$ 还用到了两条路径权重各为 $1/2$。经过 $B$ 后仍是 $I/2$，两端恒为各半。一般地，部分可区分记录给出

   $$
   P_0=\frac{1+\operatorname{Re}(\gamma e^{-i\phi})}{2},
   \qquad
   P_1=\frac{1-\operatorname{Re}(\gamma e^{-i\phi})}{2}.
   $$

   所以当 $\gamma=0.6$ 为实数且 $\phi=0$ 时，$P_0=0.8$、$P_1=0.2$。关键不在实验者是否“看过”，而在两条路径关联的记录态是否正交，或更一般地说，它们的重叠有多大。

4. 8000 个未偏振原子经第一道 $z+$ 筛选平均留下 $8000\times1/2=4000$ 个；再保留 $x+$ 平均留下 $4000\times1/2=2000$ 个；最后测 $z$，两个输出各得 $2000\times1/2=1000$ 个。三个 $1/2$ 分别是：以原始未偏振束为条件得到 $z+$，以已得到 $z+$ 为条件得到 $x+$，以及以已得到 $x+$ 为条件得到最终 $z+$ 或 $z-$。相对原始输入，两个最终分支的联合通过率各为 $1/8$。

5. 对相干叠加 $|x+\rangle$，$X$ 基测量给 $p(x+)=1,p(x-)=0$；对 $z+$/$z-$ 等概率混合，每个 $z$ 本征态在 $X$ 基都给各半，因此混合后仍为 $p(x+)=p(x-)=1/2$。矩阵分别是

   $$
   \rho_{\rm sup}=\frac12
   \begin{bmatrix}1&1\\1&1\end{bmatrix},
   \qquad
   \rho_{\rm mix}=\frac12
   \begin{bmatrix}1&0\\0&1\end{bmatrix}.
   $$

   它们的 $Z$ 基对角元相同，非对角相干项不同。

6. 对任意归一化 $|m\rangle$，

   $$
   |\langle m|e^{i\theta_{\rm g}}\psi\rangle|^2
   =|e^{i\theta_{\rm g}}|^2|\langle m|\psi\rangle|^2
   =|\langle m|\psi\rangle|^2.
   $$

   所以整体共同相位不改变任何投影测量统计。只给 $|1\rangle$ 分量乘 $e^{i\phi}$ 时，得到的是相对相位；第二个分束器把两路振幅组合为 $(1\pm e^{i\phi})/2$，其模平方随 $\phi$ 改变。

7. 线性代数规定向量、内积和模平方怎样计算，却不自动规定实验频率必须等于哪一个数学量。Born 规则是量子理论连接状态与测量概率的物理公设；公设不是随意猜测，因为它必须与其他公设相容，并接受大量可重复实验检验。数学公设定义形式系统，物理公设还承担经验预测；若实验系统性违背 Born 规则，就需要修改物理理论，而不是靠线性代数把矛盾消去。
