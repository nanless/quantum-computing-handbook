# 量子力学 Q3 自检题答案草稿

对应正文：`handbook/quantum-mechanics/03-levels-control.md`。

1. **6 GHz 的能隙。**

   $$
   \Delta E=hf
   =(6.62607015\times10^{-34})(6\times10^9)
   \approx3.976\times10^{-24}\ \mathrm J.
   $$

   用 $k_{\rm B}=1.380649\times10^{-23}\ \mathrm{J/K}$：

   $$
   \frac{\Delta E}{k_{\rm B}}
   \approx\frac{3.976\times10^{-24}}{1.380649\times10^{-23}}
   \approx0.288\ \mathrm K.
   $$

2. **4 GHz、50 mK 的热占据。** 先算无量纲指数：

   $$
   x=\frac{hf}{k_{\rm B}T}
   =\frac{(6.62607015\times10^{-34})(4\times10^9)}
   {(1.380649\times10^{-23})(0.050)}
   \approx3.839.
   $$

   所以

   $$
   \frac{p_1}{p_0}=e^{-x}\approx0.0215,
   $$

   $$
   p_1=\frac{e^{-x}}{1+e^{-x}}
   =\frac1{1+e^x}
   \approx0.0211.
   $$

   约 $2.11\%$ 的结果只属于平衡、非简并二能级模型，不是对真实器件的直接预报。

3. **两能级截断的检查项。** 只写出两个态并不能保证实验一直留在这个子空间：制备必须把大部分概率放入两个选定态；控制场不能显著驱动其他跃迁；读出必须能区分逻辑态，并识别或界定泄漏；环境在门和等待期间不能快速造成弛豫、退相位或离开子空间。

   超导例子：transmon 用最低两级编码，但过快或过强的微波脉冲会把 $|1\rangle$ 驱到 $|2\rangle$。离子例子：两个内部态存储逻辑信息，纠缠门却会暂时耦合振动模；门结束时若运动与内部态没有解纠缠，逻辑操作就不再是理想的两比特酉门。

4. **4 ns 脉冲与非谐性。** 相邻跃迁差为

   $$
   |f_{12}-f_{01}|=0.25\ \mathrm{GHz}=250\ \mathrm{MHz}.
   $$

   $4\ \mathrm{ns}$ 脉冲的频谱宽度量级为

   $$
   \Delta f_{\rm pulse}\sim\frac1\tau
   =\frac1{4\ \mathrm{ns}}
   =250\ \mathrm{MHz}.
   $$

   两者同量级，所以脉冲在频域中可能显著覆盖 $1\leftrightarrow2$ 跃迁，提示泄漏风险。但 $1/\tau$ 只是量级估计；实际泄漏还取决于包络形状和旁瓣、驱动幅度、跃迁矩阵元、初态在 $|1\rangle$ 上的占据、失谐、线路传递函数与脉冲整形，不能由这一个比值直接算出概率。

5. **旋磁比符号与高低能态。** 设 $\sigma_z|+z\rangle=+|+z\rangle$、$\sigma_z|-z\rangle=-|-z\rangle$。能量分别为

   $$
   E_{+z}=-\frac{\gamma\hbar B}{2},
   \qquad
   E_{-z}=+\frac{\gamma\hbar B}{2}.
   $$

   若 $\gamma>0$，$E_{+z}<E_{-z}$，所以 $|+z\rangle$ 较低；若 $\gamma<0$，不等号反转，$|-z\rangle$ 较低。因此“spin up”是否是低能态取决于磁矩定义、粒子种类和用词约定。应先从 Hamiltonian 判定能量，再规定逻辑 $|0\rangle,|1\rangle$。

6. **有失谐的 Rabi 振荡。**

   $$
   \frac{\Omega_R}{2\pi}
   =\sqrt{4^2+3^2}\ \mathrm{MHz}
   =5\ \mathrm{MHz}.
   $$

   最大激发概率为

   $$
   P_1^{\max}
   =\frac{\Omega^2}{\Omega^2+\Delta^2}
   =\frac{16}{25}=0.64.
   $$

   第一次最大值满足 $\Omega_Rt/2=\pi/2$：

   $$
   t_{\rm peak}=\frac\pi{\Omega_R}
   =\frac1{2(5\ \mathrm{MHz})}
   =100\ \mathrm{ns}.
   $$

   这里频率比值中 $2\pi$ 会相消；算时间时使用的 $\Omega_R$ 仍是角频率。

7. **环境重叠与相干项。** 偏迹后的对角元仍是 $|\alpha|^2$ 与 $|\beta|^2$，所以这个纯退相位模型不改变两个占据概率。非对角元变为

   $$
   \rho_{01}(t)
   =\alpha\beta^*\langle E_1|E_0\rangle
   =0.3e^{i\theta}\alpha\beta^*.
   $$

   相干项的模变成初始值的 $0.3$ 倍，并多出相位 $\theta$。若重叠降到 0，相干项完全消失；若重叠模为 1，则环境没有获得可区分两个分支的信息。

8. **双轨光子编码。** 两个模式记为 $a,b$，双轨计算基为

   $$
   |0_L\rangle=|10\rangle_{ab},
   \qquad
   |1_L\rangle=|01\rangle_{ab}.
   $$

   两个逻辑态都含一个光子，只是光子位于不同模式。$|00\rangle_{ab}$ 没有光子，离开了“一份激发分布在两条轨道”的计算子空间，通常表示光子丢失或擦除。把真空当作逻辑 0 属于另一种单轨编码，不能与双轨定义混用。
