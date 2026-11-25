# 可复现实验与第三方源码

在仓库根目录运行 `python3 codes/run_all.py`。该入口只执行本书的标准库教学程序，并核对源码和音频清单；不联网、不运行第三方摘录、不请求云设备。不要使用 `python3 -O` 关闭断言。

| 目录 | 内容 | 入口 |
|---|---|---|
| foundations | 00–05、13、Q1–Q4 共11组原实验及11组新增诊断 | `python3 codes/foundations/foundations_lab.py --case all` |
| algorithms | 06–08、16–18 共6组原实验、6组新增检查，以及第 21 章三大经典模拟迷你引擎 | `python3 codes/algorithms/experiments.py all` 与 `simulation_engines_lab.py` |
| systems | 09–12、14、19 共12个系统程序，以及第 20 章量子传感与精密测量验算 | 见该目录 README 与 `sensing_lab.py` |
| practice | 15章7组统计实验、5个合成音频、科学图与 V3 纯标准库 SVG 生成器 | `python3 codes/practice/experiments.py` |
| review | 交换复核的两组独立计算路径 | `python3 codes/review/cross_foundations.py` 与 `cross_systems.py` |
| vendor | 31个上游项目的固定源码摘录与许可 | `python3 codes/snapshot_sources.py --verify` |

教学实验结果是精确小模型、合成计数或固定种子模拟；不是新采集的真机数据。程序中的断言和各目录的 `expected-results.json` / `results.json` 提供复算依据。统一运行报告保存在 `work/research/code-validation.json`。

音频生成：`python3 codes/practice/generate_audio.py`。早期 Matplotlib 绘图需要 `practice/requirements-figures.txt` 中锁定的包，生成命令是 `python3 codes/practice/plot_figures.py` 与 `python3 codes/algorithms/generate_figure.py`；同类绘图脚本还包括 `practice/research_figures.py`、`foundations/generate_diagnostic_figure.py`、`algorithms/round70_figures.py`、`systems/plot_round70_cutoff.py`，具体命令、图名和依赖见各组 README。V3 版新建与升级的亮暗双主题科学 SVG 绘图器均改用**纯 Python 3 标准库**零外网离线生成（直接输出带真实 `<text>` 节点与 `@media (prefers-color-scheme: dark)` 适配的矢量图），包括：

- `codes/practice/generate_v3_figures_part1.py`、`generate_v3_figures_part2.py`、`generate_v3_figures_part3.py`：生成 21 幅 V3 新增科学 SVG（覆盖第 00、01、Q1、Q2、05、08、09、11、12、14、15、17、18、19、Q4、20、21 章）；
- `codes/practice/generate_cover_banner.py`：生成动态/静态双轨封面横幅 `cover-banner.svg` 与 `cover-banner-static.svg`；
- `codes/practice/upgrade_legacy_svgs_part1.py`、`upgrade_legacy_svgs_part2.py`：将 14 幅历史 round70–73 与实验统计 SVG 原地升级为亮暗双主题与纯 `<text>` 中文标注；
- `codes/practice/upgrade_round72_trajectories_svg.py`：直接基于 `codes/foundations/sdk/all-results.json` 归档的官方 QuTiP 轨迹数据重建 `round72-foundations-trajectories.svg`。

上述绘图程序均不属于默认标准库统一验算入口，按需单独运行即可。

本仓库未对原创教材和教学代码声明开放许可证；公开可读不自动赋予转载或再许可权。第三方材料遵循各自原许可证，不因放在同一仓库而改变。详见 [vendor/README.md](vendor/README.md)。

离线阅读版也附带代码副本，方便阅读或另存；主要开发和运行入口是仓库根目录的本目录。Markdown 教材中的代码链接会自动转到离线副本。

`tests/test_snapshot_sources.py` 提供六种完全离线的隔离回归，包括下载失败、校验失败、成功发布和目录替换回滚；统一运行入口也执行这些测试。

第15章新增后选择、零失败上界、时间预算与准概率四组固定样本：`python3 codes/practice/research_checks.py`，输出 `practice/research-results.json`。图由 `python3 codes/practice/research_figures.py` 生成，依赖仍见 `practice/requirements-figures.txt`。

源码阅读练习的独立数学核对：`python3 codes/practice/source_reading_checks.py`。该程序不导入 `vendor` 文件；基础、算法与系统三组教学与核验脚本均已接入统一入口，最新统一运行结果写入 `work/research/code-validation.json`（早期归档报告原样保留以备追溯）。

逐章细算与工业工作流核验：基础组 `python3 codes/foundations/round71_checks.py --case all`、算法组 `python3 codes/algorithms/round71_checks.py all`、系统组 `python3 codes/systems/round71_checks.py --case all`（各组对应说明与结果文件提供固定输入、单位、参数边界与详细答案，为保持历史哈希与引用可追溯而沿用原文件名）；工业工作流独立模型为 `python3 codes/practice/workflow_checks.py`（结果见 `practice/workflow-results.json`，图生成命令 `python3 codes/practice/workflow_figures.py` 使用前述固定绘图依赖）。以上脚本均接入统一入口，不导入或执行 `vendor` 摘录。

跨库对照的纯标准库独立复算：基础组 `python3 codes/foundations/round72_stdlib.py --case all`、算法组 `python3 codes/algorithms/round72_checks.py all`、系统组 `python3 codes/systems/round72_checks.py --case all`，均已收录于统一入口。26 个核心开源项目的完整 SDK 实跑任务、依赖锁、原始样本与 C/C++ 构建说明单列于[SDK 隔离实跑总说明](sdk/README.md)，需在各自隔离环境中运行，不由默认入口联网安装。

进阶核验与已存档实跑结果复算：统一入口同时收录基础/算法/系统三组 `round73_checks.py`（`codes/foundations/round73_checks.py`、`codes/algorithms/round73_checks.py`、`codes/systems/round73_checks.py`）以及 `codes/sdk/round73/check_saved.py`，后者仅用标准库独立复算原始计数、聚类方差、Liouville 乘积与 MPF 目标值。面向其余扩展项目与完整工作流的隔离 SDK 与编译说明另见[进阶集成工作流归档](sdk/round73/README.md)（不由默认入口联网安装）；各组 `sdk73/` 目录保留真实运行环境、原始失败记录与样本，与 [codes/vendor/](vendor/README.md) 中 31 个项目 122 份固定提交源码摘录一一对应。

V3 终稿在默认统一入口 `python3 codes/run_all.py` 中新增两项零外网纯 Python 3 标准库实验脚本，使离线统一检查增至 **36 项离线脚本检查**（另附 5 个 WAV 音频格式与 SHA-256 校验）：

- `codes/systems/sensing_lab.py`（对应[第 20 章](../20-quantum-sensing-metrology.html)，运行 `python3 codes/systems/sensing_lab.py`）：零外网纯标准库实现，覆盖 NV 单自旋灵敏度、Ramsey CFI/QFI/SLD 与根保真度 Bures 极限、GHZ（$N=2,3,4$）宇称测量与单比特丢失退相干归零、Huelga 1997 马尔可夫退相位标度与死时间惩罚、单轴扭转自旋压缩（Wineland $\xi_R^2$）与光学损耗压缩、CPMG 锁相滤波器及 HNLS 纠错传感 2 比特码等 **7 项断言模块**。
- `codes/algorithms/simulation_engines_lab.py`（对应[第 21 章](../21-stabilizer-classical-simulation.html)，运行 `python3 codes/algorithms/simulation_engines_lab.py`）：零外网纯标准库实现，覆盖 Aaronson–Gottesman 稳定子表（Tableau）、3 比特矩阵乘积态（MPS）逐键 SVD 左正则构造与截断误差核算、海森堡绘景含噪 Pauli 传播（SPD）与 $\ell_1$ 截断上界三大迷你引擎，并与独立态矢量/密度矩阵精确参考解逐格断言比对（断言容差 `< 1e-12`，三引擎实测最大误差均不超过 `2.22e-15`，依次为 `2.22e-15`、`2.48e-16` 与 `1.11e-15`）。
