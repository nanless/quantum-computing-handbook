# 第 72 轮：八个完整发布包的本地算法验证

核查和实际运行日期：2026-10-13。环境为 macOS arm64、Python 3.11.15。这里的“完整运行 SDK”指正常安装正式发布包和所需依赖，实际调用算法/数学对象完成以下小任务；没有运行全部上游测试套件，没有调用账户、云硬件或付费服务。完整安装日志、依赖锁、CPU/墙钟时间、原始计数与数值断言随本目录保存。正式包与 `codes/vendor/` 的固定源码摘录可能来自不同版本，不把两者等同。

## 安装与运行

从仓库根目录，先建立新环境，再按锁定版本安装。安装步骤需要网络，实验步骤不需要网络。本轮隔离环境是 `/tmp/quantum-round72-algorithms-sdk`；它是可重建的本机运行环境，不是仓库交付物。

```sh
python3.11 -m venv /tmp/quantum-round72-algorithms-sdk
/tmp/quantum-round72-algorithms-sdk/bin/python -m pip install -r codes/algorithms/sdk/requirements-lock.txt
/tmp/quantum-round72-algorithms-sdk/bin/python -m pip check
/tmp/quantum-round72-algorithms-sdk/bin/python codes/algorithms/sdk/round72_sdk.py all
```

也可将 `all` 换成下表的包名，单独运行。不要使用 `-O` 关闭断言。环境锁含完整传递依赖；在别的操作系统、CPU 架构或 Python 版本上，某些轮子可能不可用，需保留实际安装结果，不能把失败静默称为已经验证。脚本没有读取账户凭据，没有隐式上传样本。`install.log` 是初次安装输出，`run.log` 是增强重跑输出；完整运行 JSON 内的时间从每项函数开始计，含首次进入该项时的 import，受缓存、其它进程与平台影响，只作复现记录，不是 SDK 性能排名。

| 任务名 | 正式版本 | 实際执行链 | 独立核对 | 限定范围 |
|---|---|---|---|---|
| `cirq` | 1.7.0 | 四位非对角 HHL：受控 U/U²、QFT、倒数旋转、反计算、后选择；Z/X 两批各 20000 shots；DJ/BV；六位 Simon | HHL 解析解、成功率5/8、残差与相位寄存器；Simon完整边缘概率及GF(2)约束 | 已知两维A的矩阵门，非一般稀疏模拟器；理想本地CPU模拟 |
| `pennylane` | 0.45.1 | Bell QNode → 30000随机Pauli快照 → ClassicalShadow；参数偏移VQE → 100步梯度下降 | 自行按匹配基加权全部记录；Bell解析值/方差；VQE精确本征值 | 只估计XX/YY/ZZ/ZI，不重构完整态；VQE为精确期望 |
| `openfermion` | 1.8.1 | FermionOperator → Jordan–Wigner → sparse operator → 固定一粒子块对角化 | 手写四维矩阵、解析二次特征方程及反对易关系 | 两轨道跳跃模型，未产生真实分子积分 |
| `qualtran` | 0.7.0 | ModExp及其分解在指数0…7上执行；Toffoli完整张量收缩；子bloq计数 | Python整数模幂、独立8×8Toffoli置换 | 模幂的可逆经典语义和分解，非大型Shor/物理RSA攻击 |
| `pyqsp` | 0.2.0 | Chebyshev系数 → sym_qsp真实相位求解 → SDK响应 | 自编2×2信号酉及相位连乘，1001点目标与酉性 | 目标为Im U00；网格验证不等于连续误差认证、完整矩阵QSVT或容错综合 |
| `quimb` | 1.15.0 | 任意实加权小图 → Evolution.solve → 时间态和概率 | 三路径解析完美转移；五节点独立谱展开、范数/能量 | 连续时间稠密小图；非coin/MNRS搜索算法 |
| `thewalrus` | 0.22.0 | covariance物理性/纯度 → probabilities 20层Fock概率；两模排序 | 压缩真空组合数公式、平均光子数1/8、hbar默认反例 | Gaussian模型下的非Gaussian光子数统计，有限截止；未采样大规模GBS |
| `dimod` | 0.12.22 | BQM → ExactSolver → 全4串 → to_ising | 原QUBO逐项值、可行性与常数/自旋符号 | 经典穷举基线，未调用量子退火器或测TTS |

## 保存的样本与证据

- [round72-results.json](round72-results.json)：实际全部八任务结果、版本、CPU及墙钟秒数；seed 72013。该种子只固定本地模拟伪随机数，不保证别的平台最后一位或随机序列不变。
- [shadow-samples.npz](shadow-samples.npz)：全部30000×2的 `bits` 和 `recipes`，及 `seed`。用 `numpy.load(..., allow_pickle=False)` 读取；基标签0/1/2对应X/Y/Z，结果位0/1对应+1/−1。原始匹配计数与JSON相符；不是硬件数据。
- [hhl-circuit.txt](hhl-circuit.txt)：实际Cirq四位电路，时间向右。基序 `[p0,p1,b,a]`，高位在左；辅助成功值为1。
- [pyqsp-solver.log](pyqsp-solver.log)：真正相位求解过程，不是给定零相位序列的响应。
- [requirements-lock.txt](requirements-lock.txt)、[install.log](install.log)、[run.log](run.log)：依赖和实际安装/执行输出。`pip check` 返回 `No broken requirements found`。

HHL 两批测量独立重新制备：Z批成功12461次，条件计数0/1为11252/1209；X批成功12488次，条件计数+/−为10022/2466。成功率及条件频率需分别报告，不能将条件计数的分母换成全部尝试。程序的采样容忍阈值仅用于固定种子的回归，不是替代一般置信区间。

PennyLane的XX/YY/ZZ匹配数为3376/3386/3304，估计1.0128/−1.0158/0.9912；单次匹配权重9、全样本均值的解析方差8/30000。VQE末能量−0.7280109889280264，参照−√0.53。pyqsp重建最大网格误差约1.8e−16。Walrus前20层质量0.9999999999467017、未重归一化平均光子数0.1249999989213747。

## 与工业工作流的连接

这里复现的是工业研究可以使用的**接口环节**，例如费米子映射与粒子数、参数化能量优化、可重用随机测量、模算术分解、QSP相位、张量/图演化、Gaussian概率与QUBO基线。发布包可安装、接口返回正确小例，与已生产部署、商业收益或端到端量子优势是不同证据；本目录不从小模型推断后者。

主要官方接口核查于2026-10-13：[Cirq](https://quantumai.google/cirq)、[PennyLane阴影](https://docs.pennylane.ai/en/stable/code/api/pennylane.ClassicalShadow.html)、[OpenFermion](https://quantumai.google/openfermion/tutorials/intro_to_openfermion)、[Qualtran模幂](https://qualtran.readthedocs.io/en/latest/bloqs/cryptography/rsa/factoring-via-modexp.html)、[pyqsp](https://github.com/ichuang/pyqsp/blob/master/README.md)、[quimb](https://quimb.readthedocs.io/en/latest/autoapi/quimb/evo/index.html)、[The Walrus](https://the-walrus.readthedocs.io/en/stable/quick_guide.html)、[dimod](https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/)。脚本为本书自编教学调用，没有拷贝上述包内部源码；正常安装的上游许可随包保留，不将依赖包许可证替换为本书许可证。
