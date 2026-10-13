# 完整 SDK 实际运行

第72轮在四个独立 Python 3.11 环境和两个完整 C/C++ 项目中执行了本地任务。每个 Python 目录保存完整依赖锁定；安装整个发行包，未通过修改 `vendor/` 的 import 拼接摘录。SDK 测试与 `python3 codes/run_all.py` 分开，后者仍只运行标准库实验。

| 环境 | 完整包与实际任务 | 代码及记录 |
|---|---|---|
| 基础 | Aer 的模拟、噪声与动态传态；Experiments 的状态/过程拟合；QuTiP 主方程/轨迹 | [基础说明](../foundations/round72-README.md)、[SDK脚本](../foundations/sdk/validate_sdks.py) |
| 算法 | Cirq HHL/oracle；PennyLane优化/阴影；OpenFermion映射；Qualtran模幂/分解；pyqsp相位合成；quimb图行走；Walrus光子概率；dimod穷举 | [算法说明](../algorithms/round72-README.md)、[SDK脚本](../algorithms/sdk/round72_sdk.py) |
| 系统 | Stim采样/PyMatching译码；qutip-qtrl受约束GRAPE；SeQUeNCe双向时序 | [系统说明](../systems/round72-README.md)、[系统SDK](../systems/sdk/README.md) |
| 集成 | Qiskit编译；Algorithms Grover/VQE/IAE；SQD；MPF；OBP；切割；Mitiq；pyGSTi仪器/LGST；Pauli Rust引擎 | [集成说明](workflows/README.md)、[脚本](workflows/validate_workflows.py)、[结果](workflows/results-all.json) |
| C++ | SQD-HPC完整49项上游测试及本书后选择→子采样→组态恢复 | [编译与核对](hpc/README.md) |
| C | liboqs完整ML-KEM-512/768/1024构建、封装/解封装、篡改密文 | [构建程序](../systems/sdk/run_liboqs.py)、[记录](../systems/sdk/liboqs-build-run.json) |

分别创建环境，不能假定所有库都能在同一个环境解决依赖。以集成组为例，在仓库根目录执行：

```sh
python3.11 -m venv .venv-workflows
.venv-workflows/bin/python -m pip install -r codes/sdk/workflows/requirements-lock.txt
.venv-workflows/bin/python -m pip check
.venv-workflows/bin/python codes/sdk/workflows/validate_workflows.py --case all
```

其余组换成各自的锁定文件和入口。环境目录不要提交。锁定记录来自 macOS ARM64；其他平台可能需要编译器或不同平台轮子，完整环境验证应在目标平台重新执行。运行记录中保存了平台、版本、种子、输入、误差和限定范围；日志中的本机安装路径只用于原始证据。

这些是实际完成的 CPU 小任务，并非每个项目所有功能或所有上游测试。只有 SQD-HPC 明确执行了所列完整上游测试；没有新采集 QPU、客户生产或付费云数据。OBP 0.3.0 的零接受段缺陷明确保留复现和防护验算，不把防护程序通过写成库缺陷已经修复。

教材逐项解释见[完整SDK实验册](../../labs/sdk-validation.html)。历史 `vendor/` 的固定提交与这次 PyPI 发行版本是两套来源，不改写旧清单伪装相同版本。
