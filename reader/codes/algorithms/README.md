# 算法、模拟引擎与容量：可执行教学实验

本目录是本书自行编写的本地参考计算与自动化数学断言脚本，主验证程序均只依赖 Python 3 标准库（可选绘图另需 `matplotlib` / `numpy`）。默认不请求云服务，不自动执行 `codes/vendor/` 中的第三方源码。完整推导、题目与证据边界见[算法实验册](../../labs/algorithms.html)。

所有脚本必须使用普通 `python3` 运行，**不得加关闭断言的 `-O` 参数**；默认基序为大端序（高位在左），内积为左反线性共轭，数值容差除特别标注外均为 `1e-10`–`1e-12`。

## 一、主干基础实验（`experiments.py`）

在仓库根目录运行：

```sh
python3 codes/algorithms/experiments.py all
```

可把 `all` 换成 `06`、`07`、`08`、`16`、`17`、`18` 单独核验某一章。固定确定性输入，无随机采样，不冒充真机 shots：

- `experiments.py`：第 06–08、16–18 章六组核心算例与独立解析断言；
- `expected-results.json`：确定性参考输出；
- `generate_figure.py`：从同一组计算重建 `handbook/assets/algorithm-lab-checks.svg`（可选依赖 `matplotlib` / `numpy`）。

逆 QFT 接线与加法器字宽另用 `python3 codes/algorithms/qpe_modular_checks.py` 验证。逆变换中缺少入口反序时，以相位 $1/4$ 复现概率 $(0,1/4,1/2,1/4)$。模 21 的 $20+20$ 在六位工作寄存器得到 19 且清除比较位，并用五位输入暴露错误。脚本遍历四个小模数、控制开关和闲置地址。

## 二、第二篇全覆盖与 QSVT 共享验证（`v4_algorithms_lab.py`）

覆盖第 06、07、08 章与第 16 章共用 QSVT 全部新增与扩展算例，纯 Python 3 标准库、零第三方依赖：

```sh
python3 codes/algorithms/v4_algorithms_lab.py all
```

可把 `all` 换成 `06`、`07`、`08`、`16` 分章运行：

| 模块 | 覆盖章节 | 核验对象与关键断言 |
|---|---|---|
| `06` | [第 06 章](../../06-algorithmic-primitives.html) | 显式 6 门 `PREPARE/SELECT` 块编码（$H = 0.6X + 0.8Z$）、Babbush (*PRX* 2018) 4 项 QROM 一元迭代全 16 表查表（无控与受控两版）、固定点振幅放大 $L=3, 7$ 闭式与二维矩阵双路核对、量子计数 $N=16, M=4$ |
| `07` | [第 07 章](../../07-algorithms.html) | LCHS 1D 耗散方程柯西核与 2024 改进核求积、Carleman 线性化 $2\times 2$ 截断（$R<1$ 收敛 vs $R>1$ 崩溃）、Shor $N=35$ 连分数与 Dirichlet 峰、$E(\mathbb{F}_7)$ ECDLP 群表、泊松方程条件数 $\kappa$ |
| `08` | [第 08 章](../../08-applications.html) | $\mathrm{H}_2$ 2-qubit UCCSD、4 轨道 SQD+S-CORE 变分阶梯、$K_3$ QAOA $p=1$ 最优角、WS-QAOA 倾斜混合器与 $XY$-mixer、3 物品背包 QUBO $P>2$、2 比特离散看涨期权小角度编码与 VaR/CVaR、QNG Bloch 度规、数据再上传 $L=2$、DLA 2 比特反例 |
| `16` | [第 16 章](../../16-advanced-algorithms-verification.html) | 显式 $4\times 4$ 负谱矩阵 QSVT（`pyqsp` $W$ 约定与 PennyLane $R$ 约定 4 相位角误差均 $<10^{-8}$），含 $8\times 8$ 相干实部提取器成功概率 $0.00444112$ |

## 三、经典模拟三大引擎（`simulation_engines_lab.py`）

配套[第 21 章](../../21-stabilizer-classical-simulation.html)，纯 Python 3 标准库实现并与精确态矢量/密度矩阵逐格互验（容差 `< 1e-12`）：

```sh
python3 codes/algorithms/simulation_engines_lab.py
```

包含三大可独立阅读的教学迷你引擎：① Aaronson–Gottesman 稳定子表引擎（含去稳定子、$O(n)$ Clifford 门更新与 $O(n^2)$ 确定性测量）；② 3 比特矩阵乘积态（MPS）用直接旋转列向量的薄 SVD 检查数值秩与截断误差；③ 海森堡绘景 Pauli 传播与含噪稀疏 Pauli 动力学（SPD）及算符范数截断误差界检验。

## 四、专题核验与反例归档脚本

以下标准库专题核验脚本保留原文件名与确定性输出档案以维护全书引用与哈希追溯（均已接入 `codes/run_all.py`）：

### 4.1 接口边界与符号反例核验（`round70_checks.py`）

```sh
python3 codes/algorithms/round70_checks.py all
```

可选 `06`、`07`、`08`、`16`、`17`、`18`，分别对应正文各章的就地反例与算例（无随机采样，容差 `1e-10`；可选配图脚本 `round70_figures.py` 生成 `handbook/assets/round70-amplitude-aliasing.svg` 与 `round70-chain-strength.svg`）：

| 章节 | 固定输入与核验对象 | 独立核对路径 |
|---|---|---|
| 06（§8.1） | Hadamard 测试，$U = \operatorname{diag}(1, \pm i)$ | 四维联合振幅与复期望值实/虚部，$S$ vs $S^\dagger$ 符号反转 |
| 07（§4.2） | MLAE 计数 25/100 与 100/100 | 三倍角多项式 $p_1(a)=a(3-4a)^2$ 混叠与联合对数似然 |
| 08（§2.5） | 两道共享参数 $R_y(\theta)$ 门（$\theta=\pi/8$） | 旋转矩阵解析导数 $-\sqrt{2}$ 与链式法则 |
| 16（§5.8） | 小成功率后选择分支（$p=0.0001$） | 归一化状态距离、根保真度与 $O(\epsilon/\sqrt{p})$ 放大上界 |
| 17（§5.3） | 两自旋嵌入链（$J=1,2,3,8$） | 穷举四配置能谱与临界阈值简并 |
| 18（§3.2） | 重复码与三位奇偶校验码 | 全部消息及八种擦除掩码与二项式公式 |

### 4.2 偏迹、有限预算与多章独立复核（`round71_checks.py` / `round72_checks.py` / `round73_checks.py`）

```sh
python3 codes/algorithms/round71_checks.py all
python3 codes/algorithms/round72_checks.py all
python3 codes/algorithms/round73_checks.py all
```

- **`round71_checks.py`**（覆盖 `06, 07, 08, 13, 16, 17, 18, q4`）：核验垃圾位偏迹纯度与局域复位反例（Ch06 §1.4）、Simon $d=2$ 全部 $k\le 5$ 序列满秩穷举（Ch07 §1.4）、Bell 态共测协方差与边缘计数反例（Ch08 §2.4）、量子互信息与条件熵（Ch13）、标量块编码与二维量子化（Ch16）、两段回波酉连乘（Ch17）、单模高斯协方差缩放（Ch18）及方势垒透射共振（Q4，配图脚本 `round71_figures.py`）。
- **`round72_checks.py`**（覆盖 `13, q4`）：核验经典阴影非线性纯度估计偏差与两副本 $U$-统计量，以及相干态 Fock 截断余项界（配图脚本 `round72_figures.py`）。
- **`round73_checks.py`**（覆盖 `06, 07, 08, 13, 16, 17, 18, q4`）：核验有符号 QPE 补码解码与 $\pm\Lambda$ Nyquist 端点混叠（Ch06 §6.5）、负谱非网格 HHL 垃圾概率方差恒等式与 $t=3\to 4$ 非单调反弹（Ch07 §6.4）、两轨道粒子数罚项临界阈值（Ch08 §3.3）、混态根保真度（Ch13）、$4\times 4$ 负谱 QSVT 与 4 维超立方体 SKW 行走（Ch16）、3 比特 MBQC 四分支前馈（Ch17）、非高斯高能尾马尔可夫界（Ch18）及有限截断生成元指数偏差（Q4）。

## 五、边界与第三方材料说明

本目录所有教学实现均为小规模精确数值或解析对照，不替代生产级容错编译器、大规模张量网络求解器或云端真机实验。跨 SDK 固定版本离线复现日志见 `codes/algorithms/sdk/` 与 `codes/algorithms/sdk73/`；第三方只读源码摘录及许可信息以 [vendor 清单](../vendor/manifest.json)为准。
