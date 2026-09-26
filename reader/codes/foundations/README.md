# 基础章的可复现实验

本目录覆盖主篇 00、01、02、03、04、05、13，以及量子力学 Q1–Q4，共 11 个章级实验。完整题目、分步解答、适用条件见 [基础实验册](../../labs/foundations.html)。这些是本书独立编写的教学实现，未复制第三方软件源码。

只依赖 Python 3 标准库，不联网、不访问量子设备、不安装依赖。在仓库根目录运行：

```sh
python3 codes/foundations/foundations_lab.py --case all
python3 codes/foundations/foundations_lab.py --case 04
python3 codes/foundations/foundations_lab.py --case q4
python3 codes/foundations/foundations_lab.py --case all --output /tmp/foundations-results.json
```

`--case` 可选 `00 01 02 03 04 05 13 q1 q2 q3 q4 all`。默认种子为 `20260926`，只影响 `00` 的合成采样；其余计算是确定性的。不要用 `python3 -O`，因为它会删除本教学脚本中的 `assert` 检查。

[expected-results.json](expected-results.json) 是本轮实际运行结果，不是硬件测量。浮点输出末位可以随环境略变；教学矩阵检查默认容差为 `1e-10`，势阱差分残差另用 `1e-8`。程序检查矩阵归一化、厄米性、二维正性、Kraus 完备关系、传态四个分支与网格收敛；没有以“一批随机数必须命中置信区间”作为测试条件。

| 实验 | 检查对象 | 可改变的量 |
|---|---|---|
| 00 | 1000 次采样、恰好对半概率、Hoeffding 半径 | 命令行随机种子 |
| 01 | 复内积、外积、Hadamard 换基 | 输入两分量 |
| 02 | 测量 Y 时的 S†/H 顺序 | 输入相位 |
| 03 | 非最大纠缠态的偏迹与远端酉操作 | B 的旋转角 |
| 04 | 8 分量传态线路全部四个结果 | 输入态的复振幅 |
| 05 | 阻尼 + 退相位、T1/T2 的区别 | 时间及衰减常数 |
| 13 | 不等先验的最优判别 | 先验概率 |
| Q1 | 复环境重叠与干涉条纹位置 | 重叠的模和相位 |
| Q2 | 时序和子系统能量零点 | 两段门序与分支相位 |
| Q3 | 热占据、角频率单位、失谐 Rabi 峰值 | 温度、驱动、失谐 |
| Q4 | 硬壁差分算符、归一化、二阶收敛 | 内点数 |

## 开源实现与工程迁移

核查日期：2026-09-26。下列软件是拓展入口，不是本脚本的隐藏依赖；软件当前页面可能随更新变化，做复现时还应记录所安装的具体版本与源码提交。

- [Qiskit quantum_info 官方 API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/quantum_info)：`Statevector` / `DensityMatrix` 表示态，`Kraus` 表示信道，`partial_trace` 取约化态，`state_fidelity` 返回平方保真度。本书 F 是根保真度，比较时需开方。该库的 `qargs` 是被迹掉的子系统编号，不能当作保留编号。源码仓库：[Qiskit/qiskit](https://github.com/Qiskit/qiskit)。
- [QuTiP 主方程求解器文档](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)：`mesolve` 接收 Hamiltonian、初态、时间列表、塌缩算符与观测量，用于 Lindblad 模型；对弛豫塌缩算符应使用 `sqrt(rate) * |0><1|`，不能把速率本身当振幅。源码仓库：[qutip/qutip](https://github.com/qutip/qutip)。有限能级截断必须提高维数、缩小步长复查，且 Markov 模型适用性由物理假设决定。

Qiskit 的电路模拟适合检查门序、端序和协议；QuTiP 的开放系统模型适合检查连续驱动、耗散与多能级泄漏。它们都不把输入的教学参数自动转成真实设备的校准数据。移到工程场景前需要明确读出错判、泄漏标签、驱动幅度单位、采样批次和漂移记录，才能比较输出。
