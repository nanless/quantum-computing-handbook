# 集成组：九个完整发行包的可核验任务

访问和运行日期2026-10-13。直接版本见 [requirements.txt](requirements.txt)，完整依赖见 [requirements-lock.txt](requirements-lock.txt)，官方发行元数据见 [package-metadata.json](package-metadata.json)。安装记录和 `pip check` 保存在同目录。

```sh
python codes/sdk/workflows/validate_workflows.py --case all
```

在按依赖锁定文件建立的独立 Python 3.11 环境中执行。`--case` 可以选 `qiskit,algorithms,sqd,mpf,obp,cutting,mitiq,pygsti,pauli-prop`。不用 `-O`，因为断言是验收的一部分。脚本不会安装包或请求云服务；输出 [results-all.json](results-all.json) / 分项文件，异常保留堆栈并返回非零状态。

- Qiskit：非邻接CX编译到线型拓扑，带最终布局比较完整酉，再独立验证含复相位末态；门的表示变换不能改变输出。
- Algorithms：两位Grover、含真正放大幂的迭代振幅估计、Ry单参数VQE；保留IAE各轮原始计数、幂/区间及VQE目标历史，分别与0.2和`-sqrt(0.53)`比较。
- SQD：实际采样4096次、去重、Pauli投影、ARPACK求解，与完整矩阵谱及残差比较；限制子空间检查Ritz上界。本例不是分子活性空间计算。
- MPF：SDK线性约束解与cvxpy/CLARABEL解对照；真正分解Suzuki线路后计算。直接求高层PauliEvolutionGate的精确矩阵会绕过待测近似，所以不采用它。
- OBP：两片非交换旋转的完整回传与`U†ZU`比較；预算只许一项时复现0.3.0零接受段返回错误，按metadata回退原始问题。保持错误可见，不悄悄扩大预算。
- 切割：Bell电路分成A/B，生成全部六个准概率项、各12个本地实验，模拟精确本地结果并重构XX/ZZ/IZ。未使用有限shots，不能由此宣称方差小。
- Mitiq：真正折叠1/3/5倍电路、逐门加同一退极化、密度矩阵执行、Richardson外推；独立核对`-(1-4p/3)^k`。模拟结果没有实验漂移。
- pyGSTi：同POVM的投影工具与复位工具重复读数；另做92设置的16384次/设置LGST拟合，逐条保存[计数](gst-counts.json)，用长度1–12的密集矩阵概率检查预测。部分短线路与训练集重合，长度更长的检查才是额外预测；非CP的线性拟合不能伪称受约束最大似然估计。
- Pauli-prop：真正调用已安装wheel中的Rust扩展，核对完整回传、单项截断及达到的L1误差界。不是完整shading/PNA流程。

[首次失败记录](initial-failures.json)区分真实库缺陷、接口显示约定和本书记录器错误；最终日志为 [run.log](run.log)。复数用`[实部,虚部]`记录，不用其模平方代替矩阵系数。固定种子的一次置信区间覆盖不证明频率覆盖定理。
