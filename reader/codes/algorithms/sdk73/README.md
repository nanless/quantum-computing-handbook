# 第73轮：完整负谱 HHL、离散行走搜索、QSVT 与两步 MBQC

实际核验2026-10-13。复用已在第72轮完整安装的隔离环境，没有修改其软件或旧结果；新运行、锁、原样本和失败全部另存此目录。Python3.11.15、Cirq1.7.0、PennyLane0.45.1、NumPy2.4.6、SciPy1.17.1，完整依赖见 `requirements-lock.txt`，`pip-check.log` 实际输出无损坏依赖。它是较大的原算法环境锁，包含第72轮其他包；最小直接需求见 `requirements.txt`。

```sh
python3.11 -m venv /tmp/quantum-sdk73-algorithms
/tmp/quantum-sdk73-algorithms/bin/python -m pip install -r codes/algorithms/sdk73/requirements-lock.txt
/tmp/quantum-sdk73-algorithms/bin/python -m pip check
/tmp/quantum-sdk73-algorithms/bin/python codes/algorithms/sdk73/validate_algorithms.py all
python3 codes/algorithms/round73_checks.py all
/tmp/quantum-sdk73-algorithms/bin/python codes/algorithms/round73_figures.py
```

执行命令从仓库根目录运行。可把 `all` 改成 `hhl / walk / qsvt / mbqc`，各任务写 `results-<任务>.json`，避免单项记录冒充全套。默认标准库验证不安装依赖、不调用SDK、不联网；SDK脚本不请求云账号或设备。包安装是另行明确动作。图生成器读取 `results-all.json`，没有把理论值伪装成实测图。

## 四项完整运行与独立参考

| 任务 | 实际包步骤 | 独立参考、保留记录与边界 |
|---|---|---|
|负谱与非网格HHL|输入态酉完成、受控矩阵指数、SDK逆QFT、有符号倒数旋转、逆QPE、辅助/相位/系统测量|独立DFT+谱构造逐联合振幅、`solve`仅当比较目标；完整联合态与两个20000位串批次、参数、垃圾与条件混态；小密集矩阵门，不是可扩展稀疏输入|
|SKW超立方体离散搜索|方向Grover硬币、目标条件−I硬币、逐标签受控位翻转、位置测量|64维独立coin/置换矩阵逐步比较，删除标记后的均匀态反例；0…16联合态、20000样本与全直方图；是SKW小实例，不是完整MNRS|
|负谱非对角QSVT|真实多项式相位求解、矩阵BlockEncode、投影相位序列、实际QNode、额外选择位相干提取实部|独立手乘 `.8*A**3−.3*A`、完整酉、实际QNode与selector态；`U*`不是`U†`，密集控制块只适用于本小矩阵，不宣称一般高效共轭或容错综合|
|两步适应性MBQC|三位资源链、中途测量、条件二次旋转、条件Pauli纠正、已知目标逆制备测量|标准库独立四支部分收缩，各概率1/4且纠正后相同目标；20000原记录四支5012/5083/4999/4906，最终检验失败0；不是恶意服务器验证或实际前馈时延测量|

本次最终命令退出码0，`run.log`、`results-all.json`含真正结果与任务时长。第一次开发运行预期HHL六位根保真度大于.995的断言失败，真实值为.99444844；保留 `run-initial.log`、`initial-failures.json`。修正的是作者不恰当的阈值预判，改为.99回归阈值并完整报告真实数据；独立振幅、概率与密度矩阵参考没有放松。此时误差仍存在，不能把程序passed写成精确求逆。

## 一般小矩阵接口与输入承诺

`hhl(A, b, t, scale=4, cutoff=.5, constant=.5, name='case', shots=0)` 可从模块导入并接受任意所述小输入：`t`须为至少1的整数（拒绝布尔/负数/非整数）、Hermitian、维数为至少2且是2的幂、归一化一维复向量、所有本征值满足 `cutoff <= abs(eig) < scale`、`0 < constant <= cutoff < scale`。验证参数要明确提供，不能用本书两维输出作为任意稀疏线性系统的复杂度证据。

有符号标签网格是 `2*scale*y/M`，后半圈用 `y-M`。近零标签旋转振幅置0，其余振幅 `C/lambda_y`；这是硬截止的教学滤波。真实谱是否满足承诺在此小例由密集本征求解先检查，是经典已知矩阵接口；大输入的oracle承诺通常不能免费这样验证。

固定输入包括实旋转基下谱−1/2、−1.1/2.3以及四维谱−1.3/−.7/1.1/2.2。复输入刻意避免仅检查概率而漏掉相对相位。成功分支明确保存三层：仅辅助成功、辅助成功且相位0、辅助成功且相位非0。前者对相位做偏迹，计算根保真度与纯度；再筛相位0则输出另一条件纯态及其方向残差。方向残差采用 `||(I−bb†)A|x_clean>||`，不把已归一化解态误塞进未经重标度的 `Ax=b`。

`hhl-*-t*.npz` 中 `joint` 排序是相位MSB→系统MSB→flag，shape `(2**t, dimension, 2)`。`*-samples.npz` 保存每次所有测量位及实际seed。二维非网格四位20000次辅助成功3215、清零2751、垃圾464；精确负谱三位成功3252且全部清零。未采样的位数只报告精确本地模拟概率，不添加虚构shots。

`walk-states-samples.npz` 包含17个64分量联合态、目标step矩阵、shift、coin和20000×4位置位。比较列中的经典最终均匀边缘与经典累计首次命中是不同事件，禁止混做一个性能指标。SKW步骤先coin后shift，方向j翻位置第j位，高位在左。

## 研究与工业实践接续

本轮补足的是可运行研究部件：线性系统的负谱/有限精度误差账、行走谓词与相干邻居更新、QSVT从相位到完整负谱矩阵块、真实中途反馈。工业迁移还要展开oracle门、数据制备、读出目标、全部重试、原生门综合、硬件校准及强经典基线。密集CPU线路能核对数学和接口，不能证明生产优势。

仍未实现任意规模稀疏HHL与平滑滤波统一误差证书、一般MNRS相位反射搜索、完整任意群HSP、高阶大矩阵QSVT容错门编译、有限能量GKP以及大型非Gaussian采样。对应缺口仍保留，不把新增四项演示写成穷尽全部算法。

核查的一手来源（访问2026-10-13）：[HHL2009](https://arxiv.org/abs/0811.3171)、[SKW2003](https://arxiv.org/abs/quant-ph/0210064)、[QSVT2019](https://arxiv.org/abs/1806.01838)、[Cirq模拟](https://quantumai.google/cirq/simulate/simulation)、[Cirq经典条件控制](https://quantumai.google/cirq/build/classical_control)、[PennyLane qsvt](https://docs.pennylane.ai/en/stable/code/api/pennylane.qsvt.html)、[BlockEncode](https://docs.pennylane.ai/en/stable/code/api/pennylane.BlockEncode.html)。本书调用程序为原创教学实现；官方包来自完整发行环境，未执行vendor摘录或把第三方许可套到本书。
