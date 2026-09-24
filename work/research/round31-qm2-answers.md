# 量子力学 Q2 自检题完整答案草稿

供总编并入共享练习附录；对应 `handbook/quantum-mechanics/02-observables-dynamics.md`。建议锚点标题为 `## 量子力学 Q2`。

1. 算符

   $$
   A=2|0\rangle\langle0|-|1\rangle\langle1|
   $$

   的两个本征值为 $2,-1$，对应投影为 $|0\rangle\langle0|,|1\rangle\langle1|$。对

   $$
   |\psi\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},
   $$

   两个结果的概率都是 $1/2$。因此

   $$
   \langle A\rangle
   =2\times\frac12+(-1)\times\frac12
   =\frac12.
   $$

   又有

   $$
   \langle A^2\rangle
   =2^2\times\frac12+(-1)^2\times\frac12
   =\frac52,
   $$

   所以

   $$
   (\Delta A)^2
   =\frac52-\left(\frac12\right)^2
   =\frac94,
   \qquad
   \Delta A=\frac32.
   $$

   单次读数只能是谱中的 $2$ 或 $-1$，不会是 $1/2$。$1/2$ 是对同一种制备重复许多次后样本平均趋近的理论期望。

2. 定义

   $$
   \widetilde A=A-\langle A\rangle I,
   \qquad
   \widetilde B=B-\langle B\rangle I,
   $$

   以及

   $$
   |a\rangle=\widetilde A|\psi\rangle,
   \qquad
   |b\rangle=\widetilde B|\psi\rangle.
   $$

   因为中心化后的算符仍是厄米算符，

   $$
   \langle a|a\rangle=(\Delta A)^2,
   \qquad
   \langle b|b\rangle=(\Delta B)^2.
   $$

   Cauchy–Schwarz 不等式给出

   $$
   (\Delta A)^2(\Delta B)^2
   \ge|\langle a|b\rangle|^2
   =|\langle\widetilde A\widetilde B\rangle|^2.
   $$

   令 $z=\langle\widetilde A\widetilde B\rangle$。由于

   $$
   z^*=\langle\widetilde B\widetilde A\rangle,
   $$

   所以

   $$
   \operatorname{Im}z
   =\frac{z-z^*}{2i}
   =\frac1{2i}\langle[\widetilde A,\widetilde B]\rangle
   =\frac1{2i}\langle[A,B]\rangle.
   $$

   又因为 $|z|^2\ge(\operatorname{Im}z)^2$，

   $$
   (\Delta A)^2(\Delta B)^2
   \ge\frac14|\langle[A,B]\rangle|^2.
   $$

   两边取非负平方根即得

   $$
   \Delta A\,\Delta B
   \ge\frac12|\langle[A,B]\rangle|.
   $$

3. 对

   $$
   |{+i}\rangle=\frac{|0\rangle+i|1\rangle}{\sqrt2},
   $$

   有 $Y|{+i}\rangle=|{+i}\rangle$，故 $\langle Y\rangle=1$。这个态在 $X$ 基和 $Z$ 基都给 $\pm1$ 各半，所以

   $$
   \langle X\rangle=\langle Z\rangle=0.
   $$

   利用 $X^2=Z^2=I$，

   $$
   \Delta X=\sqrt{1-0^2}=1,
   \qquad
   \Delta Z=1.
   $$

   左端为 $1$。又因 $[X,Z]=-2iY$，右端为

   $$
   \frac12|\langle[X,Z]\rangle|
   =\frac12|-2i\langle Y\rangle|=1.
   $$

   两端相等，这个态使 Robertson 关系饱和。

4. 对

   $$
   |\phi\rangle
   =\cos\frac\pi8|0\rangle+\sin\frac\pi8|1\rangle,
   $$

   系数为实数，所以 $\langle Y\rangle=0$。因此

   $$
   \frac12|\langle[X,Z]\rangle|
   =\frac12|-2i\langle Y\rangle|=0.
   $$

   但这个态的 Bloch 向量为 $(1/\sqrt2,0,1/\sqrt2)$，故

   $$
   \langle X\rangle=\langle Z\rangle=\frac1{\sqrt2}.
   $$

   再用 $X^2=Z^2=I$：

   $$
   \Delta X=\Delta Z
   =\sqrt{1-\frac12}
   =\frac1{\sqrt2}.
   $$

   所以 $\Delta X\Delta Z=1/2$，两个量都不是确定的。Robertson 右端为零只表示这个特定的状态依赖下界没有提供信息，不表示 $X,Z$ 对易，也不表示方差为零。

5. Hamiltonian 已经在 $|0\rangle,|1\rangle$ 基中对角化，因此

   $$
   U(t)=e^{-iE_0t/\hbar}|0\rangle\langle0|
   +e^{-iE_1t/\hbar}|1\rangle\langle1|.
   $$

   对初态 $|+\rangle$，

   $$
   |\psi(t)\rangle
   =\frac{e^{-iE_0t/\hbar}|0\rangle
   +e^{-iE_1t/\hbar}|1\rangle}{\sqrt2}.
   $$

   $X=+1$ 的振幅为

   $$
   \langle+|\psi(t)\rangle
   =\frac12\left(e^{-iE_0t/\hbar}+e^{-iE_1t/\hbar}\right).
   $$

   取模平方：

   $$
   \begin{aligned}
   p_X(+;t)
   &=\frac14\left|1+e^{-i(E_1-E_0)t/\hbar}\right|^2\\
   &=\frac{1+\cos[(E_1-E_0)t/\hbar]}2\\
   &=\cos^2\frac{(E_1-E_0)t}{2\hbar}.
   \end{aligned}
   $$

   第一行已去掉共同全局相位；概率只依赖能级差。

6. 因为

   $$
   U(t)=e^{-i\Omega tX/2}
   =\cos\frac{\Omega t}{2}I-i\sin\frac{\Omega t}{2}X,
   $$

   所以

   $$
   U(t)|0\rangle
   =\cos\frac{\Omega t}{2}|0\rangle
   -i\sin\frac{\Omega t}{2}|1\rangle,
   $$

   $$
   p(1,t)=\sin^2\frac{\Omega t}{2}.
   $$

   $\pi$ 脉冲满足 $\Omega t_\pi=\pi$。题目给

   $$
   \frac{\Omega}{2\pi}=25\ \mathrm{MHz},
   $$

   因此

   $$
   t_\pi=\frac\pi\Omega
   =\frac1{2(25\times10^6\ \mathrm{s}^{-1})}
   =2.0\times10^{-8}\ \mathrm{s}
   =20\ \mathrm{ns}.
   $$

7. 若 $\mathcal H|E_n\rangle=E_n|E_n\rangle$，则

   $$
   |E_n;t\rangle=e^{-iE_nt/\hbar}|E_n\rangle.
   $$

   时间演化只给整个态乘共同全局相位，因此任意不显含时间的测量概率都不变；这就是“定态”的含义。ket 的坐标仍乘了随时间变化的复相位，所以不能把“定态”解释成 ket 字面上完全不变。不同能量的叠加态会积累相对相位，通常产生可测的时间变化。

8. 取每段旋转角为 $\pi/2$。先 $X$ 后 $Z$ 时，较晚的 $Z$ 操作写在左边：

   $$
   U_{X\to Z}=R_z(\pi/2)R_x(\pi/2),
   $$

   且

   $$
   U_{X\to Z}|0\rangle=e^{-i\pi/4}|+\rangle.
   $$

   所以最后测 $X$，得到 $+1$ 的概率是 1。

   交换顺序：

   $$
   U_{Z\to X}=R_x(\pi/2)R_z(\pi/2),
   $$

   $$
   U_{Z\to X}|0\rangle
   =e^{-i\pi/4}|{-i}\rangle.
   $$

   $|{-i}\rangle$ 在 $X$ 基给 $\pm1$ 各半，所以 $p_X(+)=1/2$。两种安排的普通时间积分都是 $\pi(X+Z)/4$，却得到不同结果；原因是 $[X,Z]\ne0$，真实演化必须按时间顺序相乘，不能只对 Hamiltonian 积分后做一次普通指数。
