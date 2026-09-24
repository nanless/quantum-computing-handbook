# 第 50 轮：QAOA、Ramsey 与 Bell 图只读终审

限定范围：第 08 章三顶点路径的 $p=1$ QAOA 全参数域证明、第 05 章 Ramsey 拟合式的单位与参数定义、更新后的 `bell-witness-sampling.svg` 明暗两版。未编辑正文、SVG 或阅读器。参照 [Farhi、Goldstone、Gutmann 的原始 QAOA 论文](https://arxiv.org/abs/1411.4028)、[Wang 等的一般图 $p=1$ 解析研究](https://arxiv.org/abs/1706.02998)与 [Qblox 原厂 Ramsey 实验文档](https://docs.qblox.com/en/main/applications/superconducting/fixed_frequency_transmon/090_ramsey.html)进行独立复核。

## 第 08 章 QAOA

- 第 08 章以 $C_{uv}=(1-Z_uZ_v)/2$、$B=\sum_jX_j$、$e^{-i\beta B}e^{-i\gamma C}$ 定义符号。逐项 Pauli 共轭给出路径每边 $\langle C_{uv}\rangle=1/2+\sin(4\beta)\sin\gamma(1+\cos\gamma)/4$；两边相加的表达式一致。
- $g(\gamma)=\sin\gamma(1+\cos\gamma)$ 的导数写成 $2\cos^2\gamma+\cos\gamma-1=(2\cos\gamma-1)(\cos\gamma+1)$，正确。在 $0\le\gamma\le\pi$，端点 $g=0$、内点 $\gamma=\pi/3$ 取得最大 $3\sqrt3/4$，且 $\sin4\beta\le1$ 在 $\beta=\pi/8$ 达到 1。
- 成本 Hamiltonian 的本征值是整数 $0,1,2$，因此期望式的 $\gamma$ 周期为 $2\pi$。对后半周期取 $\gamma'=2\pi-\gamma$ 与 $\beta'=\beta+\pi/4$，$\cos\gamma'=\cos\gamma$、$\sin\gamma'=-\sin\gamma$、$\sin4\beta'=-\sin4\beta$，乘积不变，覆盖所有实数 $\beta,\gamma$。所以全参数最大期望割值 $1+3\sqrt3/8=1.6495190528$ 的结论成立；它不是“单次必得最优割”，正文也明确区分。
- 另以独立八维态矢量逐基态施加代价相位和三次 $X$ 旋转核算，$\beta=\pi/8,\gamma=\pi/3$ 得 $1.6495190528$；随机参数 $(\gamma,\beta)=(1,0.2),(4.1,0.8),(5.5,-0.3)$ 的直接模拟与解析式逐例吻合到浮点精度。未发现边界角或符号遗漏。

## 第 05 章 Ramsey

- $\Delta=\omega_0-\omega_{\rm ref}$ 为角频率差，单位 rad/s，$\Delta t$ 为无量纲相位；若频率以 Hz 报告，换成 $\Delta=2\pi\Delta f$ 再写 $\cos(\Delta t+\phi)$，正确。Qblox 原厂 Ramsey 调度代码也以 $2\pi\times\text{detuning(Hz)}\times\tau$ 构造恢复脉冲相位；不同脉冲顺序可能翻转余弦内失谐的符号，但可由定义与 $\phi$ 吸收，正文已经说明相位约定。
- $C$ 作为振荡对比度、$\phi$ 作为初始相位、$\alpha$ 作为包络指数，与相邻的 $T_2^*$ 解释匹配。公式以 $1/2$ 为理想概率基线，并明说真实读出可有偏置，不会把拟合参数伪装成无条件物理常数。

## Bell 图

将更新后的 SVG 分别以明、暗主题直接渲染并查看：阈值虚线、两端帽、菱形点估计和其上方标签互不遮挡；明暗对比都足够；横轴明确标明仅展示 0.4—0.8。标签仍是下界 0.5891、估计 0.6625、上界 0.7359，三者坐标与第 48 轮独立计算一致。图上文字与正文的三组各 1000 次、95% 保守区间及未计校准/漂移限定相符。

结论：这三个指定对象未发现剩余 P0—P2 问题。结论限定于所审的公式、物理单位、算例与图示，不是对全书或全部量子计算研究的无条件完备性声明。
