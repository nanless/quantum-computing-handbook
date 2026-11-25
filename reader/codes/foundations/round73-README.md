# F73：读出、完整约束层析与时变动力学

日期2026-10-13。八篇就地练习保留原题编号，各用F73标签。新代码处理上一轮仍未运行的读出/SPAM假设、完整CP+TP拟合及真实计数MLE、时变开放演化和轨迹误差。全部为本地CPU合成实验；真实器件、联合SPAM辨识、非Markov环境和生产部署尚未复现。

## 1. 八组独立数学练习

从仓库根目录运行，仅需Python 3.9以上标准库：

    python3 codes/foundations/round73_checks.py --case all

单组把all换成00、01、02、03、04、05、q1或q2。[实际八组结果](round73-all-results.json)和[实际日志](round73-run.log)保存本轮输出；这组程序直接复算数学，不读取SDK结果来宣称SDK再次运行。

| 编号 | 算什么 | 独立检查 |
|---|---|---|
| 00 | 两设置校准、QST、QPT训练/留出账本 | 65024次；不混入轨迹和反馈shots |
| 01 | 行报告/列真值的2×2逆校准矩阵 | 逆、扰动放大、带符号估计 |
| 02 | 不对称错判的仿射均值及一阶方差 | 目标shots和校准shots分别计入；见下文数学勘误与历史对照 |
| 03 | Bell四格错报分布与见证 | 四格枚举对照相关公式及偏置扣除 |
| 04 | 消息错报触发的传态Pauli信道 | 四Kraus权重、TP、Z/Y缩放 |
| 05 | 旋转加阻尼的Choi矩阵 | Kraus外积、完整偏迹、Born公式、虚部TP反例 |
| q1 | 错报导致的干涉浅条纹 | 最高/最低/可见度；与漏检分开 |
| q2 | Gaussian驱动开放Bloch方程 | 独立标准库RK4、150–2400步比较 |

## 1.1 数学勘误：不对称读出反演的一阶偏导与历史 SDK 归档对照

在不对称读出反演 $r(m,\alpha,\beta)=\frac{m+\alpha-\beta}{1-\alpha-\beta}$（$d=1-\alpha-\beta$）中，正确的一阶偏导数为

$$\frac{\partial r}{\partial\alpha}=\frac{1+r}{d},\qquad \frac{\partial r}{\partial\beta}=\frac{r-1}{d}.$$

这满足物理边界：当真实态为 $|0\rangle$（$r=+1$）时真 `1` 不出现，必有 $\partial r/\partial\beta=0$；当真实态为 $|1\rangle$（$r=-1$）时真 `0` 不出现，必有 $\partial r/\partial\alpha=0$。对标杆态 $Z$ 轴参数（$r=0.5,\alpha=0.12,\beta=0.23,N=8192,N_c=16384$），正确的一阶方差分解为：

- 目标测量方差项：`0.0002342522`；
- 标定 $\hat\alpha$ 贡献项：`0.0000343241`；
- 标定 $\hat\beta$ 贡献项：`0.0000063961`；
- 标定方差合计 `0.0000407202`（占总方差 `14.8%`），**正确总方差为 `0.0002749724`，总标准误为 `0.01658229`**；对应完整三轴协方差矩阵对角元为 `[0.0003262672, 0.0002116728, 0.0002749724]`。

**历史归档说明（保留原貌不篡改）：** 此前在隔离 SDK 环境落盘的 [`sdk73/validate_sdks.py`](sdk73/validate_sdks.py)（第 66 行）与归档结果 [`sdk73/all-results.json`](sdk73/all-results.json)（以及 `sdk73/initial-failures.json`）曾将两项偏导写反为 `da=(true_r-1)/.65`、`db=(true_r+1)/.65`，从而在历史 JSON 的 `delta_method_total_covariance` 中得到偏大的 $Z$ 轴总方差 `0.0002956305`（标定项 `0.0000613783`，SE `0.01719391`）与 $Y$ 轴方差 `0.0002474536`（$X$ 轴因 $r_x=0$ 不受影响）。为忠实保存当时隔离 SDK 环境的真实落盘记录及其 `script_sha256` 证据链，本书**不伪造修改** `sdk73/all-results.json` 或历史驱动脚本；现[第 02 章正文](../../02-single-qubit.html#83-不对称读出校准方差传播与-spam-边界)与标准库校验脚本 [`round73_checks.py`](round73_checks.py)（`--case 02`）均已纠正为正确偏导，并辅以独立中心差分、物理边界检验以及与历史写反值的显式对照。

## 2. 安装完整固定SDK并运行

新隔离环境不改旧round72环境。官方直接版本见[sdk73/requirements.txt](sdk73/requirements.txt)；完整解析依赖见[锁定文件](sdk73/requirements-lock.txt)，CVXPY1.9.3是在旧固定依赖基础上增加的完整官方包，依赖SCS3.3.1、CLARABEL0.11.1。Python实际为3.11.15；各准确版本以[结果包字段](sdk73/all-results.json)为准。

以下是可复现命令，安装阶段需要联网；验证脚本不发云任务或下载内容，不执行vendor摘录。环境名可以自行改变。

    python3.11 -m venv /tmp/quantum-round73-foundations-sdk
    /tmp/quantum-round73-foundations-sdk/bin/python -m pip install -r codes/foundations/sdk73/requirements-lock.txt
    /tmp/quantum-round73-foundations-sdk/bin/python codes/foundations/sdk73/validate_sdks.py --case all

本机实际用uv建立无pip环境，等价固定包安装/检查的真实日志在[install.log](sdk73/install.log)及[pip-check.log](sdk73/pip-check.log)；建立和安装命令是：

    uv venv --python python3.11 /tmp/quantum-round73-foundations-sdk
    uv pip install --python /tmp/quantum-round73-foundations-sdk/bin/python -r codes/foundations/sdk73/base-round72-lock.txt cvxpy==1.9.3
    uv pip check --python /tmp/quantum-round73-foundations-sdk/bin/python

不使用Python的-O选项，它会移除断言。[官方发布元数据](sdk73/official-release-metadata.json)包含固定发布文件哈希与上传时间；[关键已安装源码哈希](sdk73/installed-source-hashes.json)支持核对完整包里的真实接口。环境本身、轮子和二进制扩展未复制进仓库；固定依赖、原始输入/样本、自己的驱动与来源齐备。

## 3. 四条真正执行的流程

| 程序case | 完整SDK操作 | 独立验收和边界 |
|---|---|---|
| readout | Aer非对称ReadoutError→Experiments两列LocalReadoutError→三基QST→带噪测量基拟合 | 从原计数重构A及仿射Bloch，逐格差<5e-16；只假设制备/换基可信，没有识别任意SPAM |
| feedback | Aer中途测量→报告错判→if_test条件X/Z→Bob平均密度矩阵 | 16384次，四个Pauli分支解析信道；修改报告频率不会撤销已经误触发的物理门 |
| qpt | 先Ry(π/5)再广义阻尼→十二训练及十二留出设置→SDK Gaussian拟合→独立全约束及真正计数MLE | CP+完整复偏迹TP分别验收，独立概率与权重比较；训练与留出似然分开 |
| dynamics | QuTiP时变mesolve→三容差收敛→2048 mcsolve轨迹→封闭sesolve及中点连乘 | 独立实Bloch方程、标准库RK4、原轨迹SE/时间协方差；不是脉冲设备实验 |

最终完整运行退出0，[run.log](sdk73/run.log)与[all-results.json](sdk73/all-results.json)对应全部四case。单case输出会另保存为对应name-results.json，不覆盖旧72。单独feedback已跑的[结果](sdk73/feedback-results.json)也保留；以最终all作为当前整合验收。

readout校准/目标种子730/731，QPT训练/留出732/733，QuTiP根种子734，反馈735。每任务使用不同生成流；2048条轨迹各有独立SeedSequence派生子种子，根种子及完整spawn keys、跃迁时刻写入JSON。不复制旧记录或重新复位同一生成流来冒充新增独立样本。账本中65024次加反馈16384次，共81408次电路重新制备；2048条经典求解器轨迹另计。

## 4. 新发现：TP选项不能代替完整偏迹验收

0.14.2的默认trace_preserving=True路径在Hermitian分支只限制偏迹实部。本轮的复杂有限计数使输出偏迹非对角虚部达到约0.00091311；metadata仍声称TP。这由[固定官方源码](https://github.com/qiskit-community/qiskit-experiments/blob/0.14.2/qiskit_experiments/library/tomography/fitters/cvxpy_utils.py)及独立矩阵核验定位（访问2026-10-13），不是读取图标或推测。

[TP反例JSON](sdk73/sdk-tp-counterexample.json)保存实际错误J和偏迹。第05章另给干净手算反例J=I4/2+0.1(Y⊗I)，谱合法但偏迹为I+0.2Y，说明Hermitian偏迹仍可有虚非对角。

本书调用同SDK的partial_trace=np.array([I])路径，外层长度1表示一个条件分量；它同时施加实虚条件。独立CVXPY以Hermitian变量直接加四个复数块迹条件，再比较完整J，误差约1.02e-9。没有改或声称修复上游包。

初次0.00062差异、CLARABEL的optimal_inaccurate与首次排查记录均原样保留在[初次失败](sdk73/initial-failures.json)与[TP反例JSON](sdk73/sdk-tp-counterexample.json)（重复的中间调试日志已于 V4 仓库卫生清理中移除）。排查证明设计矩阵、频率与权重相符，差异来自默认TP约束少了虚部；之后修正完整约束才达成严格验收，未用放宽容差掩盖它。最终独立构造和SDK都使用SCS，独立性来自不同概率设计与完整约束实现，不声称做了两种独立优化引擎的最终认证。

Gaussian最小二乘是Gaussian近似模型的优化，真正计数MLE使用-k log p；两者分别报告。第05章给训练和留出数字，并指出MLE并未在所有矩阵距离上更好。本次有数值概率下界1e-10、理想可信SPAM、单比特过程，尚未完成置信区域、联合门集MLE、漂移稳健拟合或高维扩展。

## 5. 动力学原始样本与科学图

[trajectory-observables.npz](sdk73/trajectory-observables.npz)包含runs_xyz形状(3,2048,61)、时间网格及每条跃迁数；读取不需要pickle。它不是由平均曲线逆推的样本。JSON保留跳跃时刻、轨迹均值/标准误、配对时间协方差、独立Bloch参考、三容差与四片数比较。

    /tmp/quantum-round73-foundations-sdk/bin/python codes/foundations/generate_round73_figure.py

原图生成输入哈希保留在[生成输入哈希](round73-figure-provenance.json)；正文 Q2 已全面升级采用亮暗双主题矢量图 [v3-q2-lindblad-trajectories.svg](../../handbook/assets/v3-q2-lindblad-trajectories.svg)，早期 Matplotlib 导出的旧版 `round73-foundations-dynamics.{svg,png}` 已于 V4 清理中退役移除。公式、图、样本均采用μs、rad/μs、1/μs；宽度0.35μs明确是Gaussian指数参数。

逐点一倍SE不能当整曲线同时置信带。同一轨迹在不同时间点相关；有21条发生两次跃迁，驱动下不能使用“至多跃迁一次”的旧Bernoulli模型。工业上进一步还须校准设备波形、泄漏、非Markov模型和反馈延迟，本轮未实现这些项。
