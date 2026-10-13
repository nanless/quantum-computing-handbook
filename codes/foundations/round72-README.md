# F72｜完整官方 SDK 的基础实验

本轮实际安装并执行完整官方发布包：Qiskit 2.5.2、Aer 0.17.2、Qiskit Experiments 0.14.2、QuTiP 5.3.1。版本查证与所有本地执行日期为 2026-10-13。依赖来自官方 PyPI 发布，未执行 `codes/vendor/` 摘录；默认全部本地 CPU，无云任务、账号或付费调用。这是完整 SDK 上的小模型验证，不是生产应用、硬件复现或“所有算法已穷尽”。

## 可复现命令

从仓库根目录运行。Python 3.11 的本次隔离环境为 `/tmp/quantum-round72-foundations-sdk`；它是本机临时环境，不随离线书分发。环境重建命令为：

```sh
python3.11 -m venv /tmp/quantum-round72-foundations-sdk
/tmp/quantum-round72-foundations-sdk/bin/python -m pip install -r codes/foundations/sdk/requirements-lock.txt
/tmp/quantum-round72-foundations-sdk/bin/python -m pip check
/tmp/quantum-round72-foundations-sdk/bin/python codes/foundations/sdk/validate_sdks.py --case all
/tmp/quantum-round72-foundations-sdk/bin/python codes/foundations/round72_checks.py --case all
/tmp/quantum-round72-foundations-sdk/bin/python codes/foundations/generate_round72_figure.py
```

须不带 `-O`，以保留数学断言。完整验证器可单独选 `aer/tomography/qutip`；逐章连接脚本可选 `00/01/02/03/04/05/q1/q2`。逐章脚本的 00、02、05、q2 显式复用完整验证器输出，并保存输入 JSON 的 SHA-256；它不是声称这四组重复调用了一次上游拟合或求解。`--case all` 的保存结果覆盖全八篇，单独案例会只保存本次所选案例。应按完整验证器→逐章脚本的顺序运行。

## 证据与输入

- [固定直接依赖](sdk/requirements.txt)、[完整依赖锁](sdk/requirements-lock.txt)、[PyPI 发布元数据](sdk/pypi-release-metadata.json)、[安装日志](sdk/install.log)和[pip check](sdk/pip-check.log)保存环境证据；安装本身不算算法通过。
- [完整 SDK 结果](sdk/all-results.json)记录 Python、平台、版本、脚本哈希、每组通过状态、计数、复矩阵（每个复数为 `[实部,虚部]`）、容差、种子、模型及误差定义；[实际运行日志](sdk/run.log)包含三类通过消息。
- [逐章程序](round72_checks.py)、[八篇实际结果](round72-results.json)与[逐章执行日志](sdk/chapter-run.log)核对正文 F72 参数。
- 首次 QST 对照把事后正性修正与未修正线性逆矩阵直接用 `.003` 容差比较，实际失败。已保存[首次失败日志](sdk/initial-failure-run.log)与[首次结果](sdk/initial-failure-results.json)。修复使用单比特径向 PSD 公式独立重算后比较，不靠放宽容差接受结果。

## 逐章覆盖与边界

| 篇章 | 实际上游操作 | 独立对照与结果 | 适用限制 |
|---|---|---|---|
| 00 | Aer statevector、stabilizer，2048 shots | 两方法 `00/11=1027/1021`、`1008/1040`，无异号 | 同种子不保证跨算法计数相同；仅 Clifford Bell 电路 |
| 01 | SciPy expm、QuTiP Qobj.expm、Qiskit RXGate | 与 `(I-iX)/sqrt(2)` 最大差 <1e-12；逐格指数列长平方2 | 有限二维、无时序合并假设 |
| 02 | Experiments QST 三基，各8192 shots，完整拟合 | 原始Bloch长1.01609，独立PSD与SDK差6.11e-16 | 可信理想测量基，无硬件SPAM |
| 03 | Aer广义阻尼作用Bell的B，Qiskit偏迹 | A=I/2，B=diag(.644,.356)，部分转置最小谱-.31642835 | PPT负值足够证明纠缠，未泛化高维必要性 |
| 04 | Aer动态测量、if_test，六输入完整校正；另遗漏Z | 完整校正各输入误差<1e-11，遗漏Z样本相干残差.00105716 | 理想反馈，无器件延迟/门噪声 |
| 05 | Experiments完整12设置QPT，16384与32 shots两档 | 高shot Choi距离.0279380；32-shot修正后CP真、TP假，偏迹误差.04658984 | linear_inversion+PSD/trace重缩放不保证TP；不冒充约束MLE |
| Q1 | Aer辅助标记效率模型8192 shots | 被检出4077/1013、漏检3102，条件.800982、吞吐.621338 | 合成无暗计数，不闭合实际Bell探测漏洞 |
| Q2 | QuTiP mesolve 41点、mcsolve 4096轨迹 | 精确误差6.34e-11；MC误差.00305354，965跳跃 | Markov零温、独立普通轨迹；时间点相关 |

完整 Aer 信道网格另检验六个输入（含复相位）×γ三值×r三值，共54例，直接检查 Choi谱、输出偏迹、Kraus CP/TP和解析阻尼输出；最大逐格差1.34e-15。动态传态实际检验全部四种 Alice 结果出现，打印端序 c1c0=A,Q 明示。

QuTiP 的本例选择 `|0>` 为基态、`|1>` 为激发态，L显式用外积，避免猜 `sigmam` 的能级方向；时间us、H/hbar的角频率rad/us、率1/us、L的单位1/sqrt(us)。`std_expect` 为轨迹期望的总体标准差，经验标准误从原始 `runs_expect` 以 `ddof=1` 再除sqrt(N)计算。六倍经验标准误的回归容差只抓实现错误，不是同时覆盖所有时刻的置信证明。

## 官方文档与固定源码核对

下列入口在 2026-10-13 真实浏览；旧轮访问日期保留原样。

1. [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)，在线页面标0.17.1，而本次实际包0.17.2；行为另由固定包验证。
2. [amplitude_damping_error](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.amplitude_damping_error.html)，参数r的文字/矩阵冲突沿用历史说明，本轮用54例、固定点和源码核验。
3. [State tomography](https://qiskit-community.github.io/qiskit-experiments/manuals/verification/state_tomography.html)、[ProcessTomography](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.ProcessTomography.html)、[TomographyAnalysis](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.tomography.TomographyAnalysis.html)，0.14.2。
4. [QuTiP master equation](https://qutip.readthedocs.io/en/v5.3.1/guide/dynamics/dynamics-master.html)、[MC guide](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html)、[MultiTrajResult源码](https://qutip.readthedocs.io/en/stable/_modules/qutip/solver/multitrajresult.html)。stable页面把“errors”写1/n而未定义；独立均值方差定义与5.3.1安装源码表明标准误通常1/sqrt(n)。`_create_e_data`计算std_expect，`_target_tolerance_end`另处理jackknife停止标准。没有沿用文档里特定机器的7倍性能数字。
5. [Peres 1996](https://arxiv.org/abs/quant-ph/9604005)，原始部分转置判据；负谱演算本轮独立完成。

[源码身份及SHA-256](sdk/source-checks.json)记录本次安装包中的相关文件。只是检查安装包来源与函数内容，没有再分发整套上游源码。图由[生成器](generate_round72_figure.py)直接读取真实保存JSON；原尺寸SVG和PNG均在书中资产目录，误差线为单时刻一倍标准误。

## 无额外依赖的归档复算

`python3 codes/foundations/round72_stdlib.py --case all` 只用标准库，独立复算八篇保存的SDK结果：矩阵指数、QST计数与二维PSD、局部阻尼、缺少反馈的分支加权、Choi偏迹、漏检分母和解析开放演化。它已接默认统一入口，**不会重新安装或运行SDK**。前面的 `round72_checks.py` 则需要基础SDK环境，两者不能混用。
