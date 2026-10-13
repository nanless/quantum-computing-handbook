# 第73轮：上层工作流实际运行

核验日期2026-10-13。完整发行包安装于独立Python3.11环境；本目录保存直接依赖、完整锁、安装/依赖检查日志、原始计数、独立参考和失败。`vendor`是另一套固定源码摘录，没有拼接或执行摘录。锁定环境实际解析为pauli-prop0.1.0；`package-metadata.json`中其最新0.2.1仅是查询记录，不能当本实验版本。

```sh
python3.11 -m venv .venv-round73-workflows
.venv-round73-workflows/bin/python -m pip install -r codes/sdk/round73/requirements-lock.txt
.venv-round73-workflows/bin/python -m pip check
.venv-round73-workflows/bin/python codes/sdk/round73/dynamic_mpf.py
.venv-round73-workflows/bin/python codes/sdk/round73/long_gst.py
.venv-round73-workflows/bin/python codes/sdk/round73/pna_workflow.py
.venv-round73-workflows/bin/python codes/sdk/round73/slc_workflow.py
python3 codes/sdk/round73/check_saved.py
```

本机实际使用uv创建环境/安装，`uv pip freeze/check --python`保存真实锁和检查；uv环境不附pip，不能把失败的`python -m pip`说成通过。重画科学SVG运行`figures.py`，需完整锁中matplotlib；图由保存的实际结果生成。

| 流程 | 实际完成与独立核对 | 边界/失败 |
|---|---|---|
| 动态MPF | MPF0.3.0、quimb1.15.0完整TEBD MPO，3时间×2参考步长；16维dense指数及谱分解交换复核；CLARABEL约束解 | 原quimb四阶系数不能消三阶误差；保留首次失败，脚本显式子类窄修正，不修改安装包。Gram病态导致系数不稳，不称得到唯一可靠最优权重 |
| 长序列GST | pyGSTi0.10.2、CPTPLND、logl、448设置×4096计数，12条未训练电路总体概率；独立PTM/Choi/TP检查 | ideal遇正计数零概率，其真实NLL无限；旧有限数字明确为1e-12截断评分。无留出有限shots、无漂移/非Markov设备拟合 |
| PNA | PNA0.2.0实际生成逆噪声可观测量、Aer密度矩阵估计，独立矩阵；20000有限shots分配与原计数；25%标定偏移 | 一个噪声层的精确教学模型，不宣称所有多层非对易噪声都能此法精确移到末端 |
| SLC→PEC | SLC0.1.0完整前向/后向/合并/选择，Samplomatic0.21.0模板及逆噪声采样，Aer三批1024×64（全/部分/全零防护），mitigation0.1.1真实后处理 | 合成已知噪声，非硬件学习/云Executor。noise局部编号依全局canonical排序；box body可能反序，首次错映射失败保留。零mask缺陷原样记录。非broadcast stds实际为variance且展平忽略随机化聚类；使用独立cluster SE，broadcast twirl_stds核对 |
| SQD-HPC/Philox | 完整固定SQD-HPC与Random123，单机OpenMP1/2/4/8线程和serial，相同4000输入位级一致；51测试36669断言 | C++17官方Random123适配，不是C++26标准引擎；非MPI/多节点或吞吐优势 |

HPC使用完整源码，而非归档的少数头文件。`hpc/CMakeLists.txt`接受`SQD_SOURCE`、`RANDOM123_SOURCE`两个完整checkout路径。SQD提交`69f003f8304c8094ff06ba2600d38a0c683422ff`；Random123提交`9545ff6413f258be2f04c1d319d99aaef7521150`。用其原构建说明初始化SQD子模块。普通CMake/OpenMP工具链可运行：

```sh
cmake -S codes/sdk/round73/hpc -B /tmp/handbook-hpc73 -DSQD_SOURCE=/path/to/full/sqd -DRANDOM123_SOURCE=/path/to/full/random123 -DSQD_ENABLE_OPENMP=ON
cmake --build /tmp/handbook-hpc73 --target parallel_recovery sqd_tests
OMP_NUM_THREADS=4 /tmp/handbook-hpc73/parallel_recovery
OMP_NUM_THREADS=4 /tmp/handbook-hpc73/upstream/sqd_tests
```

AppleClang需要外部libomp。真实配置、首次目标作用域错误、修正配置及编译日志均保留在`hpc/`；先确认库可用和配置成功再编译。`hpc/results.json`及五份完整输出给实际结果，不把CPU并行性扩写为量子优势。

数学、练习与工业复现边界见[SDK实验册](../../../handbook/labs/sdk-validation.md)。默认标准库入口另独立核对原计数、符号、方差和保存的矩阵，不重新联网安装。
