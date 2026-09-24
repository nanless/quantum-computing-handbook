# 第 48 轮：基础组新增推导的只读交叉审

日期：2026-09-23。检查范围限于 handbook/quantum-mechanics/01-experiments-states.md 的部分路径记录、handbook/03-multiple-qubits.md 的单配性、handbook/04-circuits-protocols.md 的不可删除，以及 handbook/05-noise-channels.md 的 $T_1/T_2$ 衔接。不修改这些文件、阅读版或 sources/。

## 复算结果

| 位置 | 独立核查 | 结论 |
|---|---|---|
| 量子力学 Q1 §2.2 | $\gamma=\langle d_1|d_0\rangle$ 给路径态非对角元 $\gamma e^{-i\phi}/2$；平衡第二分束器得到 $P_0=[1+\operatorname{Re}(\gamma e^{-i\phi})]/2$。写 $\gamma=|\gamma|e^{i\delta}$ 后极值是 $(1\pm|\gamma|)/2$，所以等权无损模型的可见度为 $|\gamma|$；$\gamma=0.6$ 的 $0.2/0.8$ 正确。正文已限定不能推广到不平衡或有损装置。 | 无 P0–P2 |
| 主篇 03 §8 | 当 $\rho_{AB}$ 是 Bell 纯态时，任意扩张必为 $\rho_{AB}\otimes\rho_C$，可由纯边缘态的秩一支持空间或 Schmidt 分解证明。GHZ 态偏迹 $C$ 后为 $00/11$ 的各半经典混合，非 Bell 纯态。正文未把这一特殊情形误说成“任意少量纠缠都排除第三方”。 | 无 P0–P2 |
| 主篇 04 §5 | 两种输入 $|\phi\phi A\rangle,|\psi\psi A\rangle$ 的内积为 $c^2$；输出的内积为 $c\langle A_\phi|A_\psi\rangle$。对 $0<|c|<1$，辅助态内积必须为 $c$，不能固定为同一态。$|0\rangle,|+\rangle$ 给 $c=1/\sqrt2$；SWAP 把状态搬入环境而非无痕删除，与结论一致。 | 无 P0–P2 |
| 主篇 05 §6 | 振幅阻尼 $\gamma(t)=1-e^{-t/T_1}$ 给 $\rho_{11}=(1-a)e^{-t/T_1}$、$\rho_{01}=ce^{-t/(2T_1)}$。独立随机 $Z$ 退相位再乘 $e^{-t/T_\phi}$，因此 $1/T_2=1/(2T_1)+1/T_\phi$；$60\,\mu s$ 与 $60\,\mu s$ 合成 $40\,\mu s$，两矩阵元 $0.2567$、$0.1839$，与正文舍入一致。零温、Markov、指数衰减前提已写出。 | 无 P0–P2 |

## 一处非阻断性 P3 建议

第 05 章 §6 的原有 Ramsey 拟合式 $P_1(t)=\tfrac12[1+C e^{-(t/T_2^*)^\alpha}\cos(\Delta t+\phi)]$ 尚未逐一解释 $C,\Delta,\phi$。建议补一句：$C$ 是对比度，$\Delta$ 是相对于参考驱动的**角频率**失谐（单位 rad/s；若用 Hz 须写 $2\pi\Delta f\,t$），$\phi$ 是初始相位。这能避免初学者把 Hz 直接代进余弦。此项属于原有符号可读性，不影响新增 $T_1/T_2$ 推导。

## 一手依据

- [Englert, Fringe Visibility and Which-Way Information](https://doi.org/10.1103/PhysRevLett.77.2154), *PRL* 77 (1996)：路径信息与可见度的原始定量讨论；本教材的简式另外依赖文中注明的等权、无损模型。
- [Coffman、Kundu、Wootters, Distributed Entanglement](https://arxiv.org/abs/quant-ph/9907047)：三比特单配性的原始定量工作；教材只用其中较易验证的纯态特殊情形。
- [Pati、Braunstein, Impossibility of deleting an unknown quantum state](https://arxiv.org/abs/quant-ph/9911090)：不可删除的原始工作。
- [Preskill, Qubit Channels, Lecture 5](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-5-Qubit-Channels.pdf)：振幅阻尼、纯退相位与无额外退相位时 $T_2=2T_1$ 的极限。

这是限定范围的交叉审结论，不是对全书所有量子力学内容的完备性声明。
