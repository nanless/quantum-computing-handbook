# 基础章的可复现实验

本目录覆盖主篇 00、01、02、03、04、05、13，以及量子力学 Q1–Q4，共 11 个章级实验。完整题目、分步解答、适用条件见 [基础实验册](../../labs/foundations.html)。这些是本书独立编写的教学实现，未复制第三方软件源码。

2026-10-13 另补三组专题扩展实验（均保留原章自检编号，按需独立运行）：

- **[F71 展开练习](round71-README.md)**（纯 Python 3 标准库，运行 `python3 codes/foundations/round71_checks.py --case all`）：涵盖稠密内存字节表、被动换基与主动施门对照、非投影弱测量仪器、复数 Schmidt 构造、关联保持传态、信道顺序、条件擦除条纹与加强不确定关系。
- **[F72 矩阵指数与基础 SDK 归档复算](round72-README.md)**：其中纯 Python 3 标准库入口 `python3 codes/foundations/round72_stdlib.py --case all` 独立复算八篇已归档的矩阵指数验算（第 01 章 $e^{-i\frac{\pi}{4}X}$ 与逐格指数反例）、8192 次采样 QST 径向 PSD 投影、局部阻尼、动态反馈、Choi 偏迹、漏检分母与解析开放演化（**不会**重新安装或调用第三方 SDK）；完整固定版本官方 SDK（Qiskit / Aer / Experiments / QuTiP）隔离实跑说明与依赖锁见 [round72-README.md](round72-README.md) 及 [完整 SDK 实验册](../../labs/sdk-validation.html)。
- **[F73 不对称读出求逆、约束层析与时变开放演化](round73-README.md)**：纯 Python 3 标准库入口 `python3 codes/foundations/round73_checks.py --case all` 独立验算列随机不对称读出矩阵求逆与条件数扰动放大（第 01 章）、不对称读出仿射还原与一阶方差传播勘误对照（第 02 章）、Bell 四格错报、传态错报信道、旋转加阻尼 Choi 矩阵、错报浅条纹与 Gaussian 驱动开放 Bloch 方程；完整 SDK 隔离实跑及历史归档说明见 [round73-README.md](round73-README.md)。

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

## 新增诊断实验

每章增加一个“看起来合理但还不足以成立”的反例。题目、条件、分步解答就地放在对应章的“新增诊断练习”，不改变原自检编号。[diagnostic_lab.py](diagnostic_lab.py) 复用同目录中本书自编的 `foundations_lab.py` 矩阵助手；没有第三方运行依赖。Python 3.9 及以上可运行；固定输入、无随机采样，故不设置随机种子。

```sh
python3 codes/foundations/diagnostic_lab.py --case all
python3 codes/foundations/diagnostic_lab.py --case 05
python3 codes/foundations/diagnostic_lab.py --case all --output /tmp/diagnostic-results.json
```

[diagnostic-results.json](diagnostic-results.json) 保存实际运行的全部固定输入与结果；全部是合成计数或理想模型，未连接硬件。矩阵和数值断言容差沿用 `1e-10`，不要用 `python3 -O` 关闭断言。

| 编号 | 对应章节诊断 | 关键检查结果 |
|---|---|---|
| 00 | 重复记录的相关性 | 10 块各复制 100 次：真实频率标准差 0.158114，误当独立则 0.015811 |
| 01 | 基态检查不等于酉性 | 两列均归一化，但 $A^\dagger A\ne I$；叠加输出长度平方 2 或 0 |
| 02 | 有限数据层析的物理性 | 原本征值约 -0.065685、1.065685；径向投影不是通用最大似然法 |
| 03 | 复相位纠缠的测量方向 | ZZ=1，XX=0，XY=1；旋转见证后可检测 |
| 04 | 受控门的相位 | C(I) 与 C(-I) 的控制 H 读出分别为 0、1 |
| 05 | 非零平衡占据的阻尼 | γ=0.36，r=0.1；三个激发输出 0.036、0.676、0.356 |
| 13 | 后选与收缩定理 | 条件距离 0.936329；保留全部标记距离 0.706476 ≤ 输入 0.8 |
| Q1 | 不等路径权重与退相干 | 同为可见度 0.6，纯度却分别为 1 和 0.68 |
| Q2 | 简并测量与精细测量 | 相同读数统计，返回叠加态的概率为 1 或 1/2 |
| Q3 | 失谐符号的不可辨识性 | 两条 Rabi 曲线相同；有相位参考的 Y 测量可读符号 |
| Q4 | Fock 截断的边界误差 | 四维对易子对角为 1、1、1、-3；最高层占据 3% 时期望为 0.88 |

工程延伸入口：Qiskit Experiments 的[态层析拟合](https://qiskit-community.github.io/qiskit-experiments/manuals/verification/state_tomography)、Qiskit Aer 的[广义振幅阻尼](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.amplitude_damping_error.html)、QuTiP 的[有限维 Fock 算符](https://qutip.readthedocs.io/en/stable/guide/guide-states.html)。这些是经过网页核查的官方接口入口，未在本诊断脚本中安装或执行；具体源码快照及许可由 [vendor 清单](../vendor/README.md)单独管理。GAD 参数文字与矩阵的上游矛盾见第 05 章，不凭名称猜热占据指哪一个能级。
