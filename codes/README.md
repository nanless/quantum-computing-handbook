# 可复现实验与第三方源码

在仓库根目录运行 `python3 codes/run_all.py`（或 `make test`）。该入口执行本书的标准库教学程序并核对第三方源码清单，全程离线。请保留 Python 断言。

解压独立代码包后，在含 `codes/` 和 `CODE-VALIDATION.json` 的目录运行同一命令。发布清单将包内缺省的第三方快照核验标为不适用，其余项目照常运行。完整 Git 仓库仍要求核对快照。

| 目录 | 内容 | 入口 |
|---|---|---|
| foundations | 00–05、13、Q1–Q4 共11组原实验及11组新增诊断 | `python3 codes/foundations/foundations_lab.py --case all` |
| algorithms | 06–08、16–18 共6组原实验、6组新增检查、第 21 章三大经典模拟迷你引擎及 V4 算法核验 | `python3 codes/algorithms/experiments.py all`、`simulation_engines_lab.py`、`v4_algorithms_lab.py` |
| systems | 09–12、14、19 共12个系统程序，以及第 20 章量子传感与精密测量验算 | 见 [systems/README.md](systems/README.md) 与 `sensing_lab.py` |
| practice | 15章7组统计实验、V4 统计与实践核验、科学图与纯标准库 SVG 生成器 | `python3 codes/practice/experiments.py`、`v4_practice_lab.py`、`generate_v4_figures.py` |
| review | 交换复核的两组独立计算路径 | `python3 codes/review/cross_foundations.py` 与 `cross_systems.py` |
| vendor | 31个上游项目的固定源码摘录与许可 | `python3 codes/snapshot_sources.py --verify` |

教学实验结果来自精确小模型、合成计数或固定种子模拟。程序中的断言和各目录的 `expected-results.json`、`results.json` 提供复算依据。默认将当前批次结果写到 `work/research/code-validation.json`，子程序新结果写入同目录下的 `local-check-results/`。加 `--output-dir 路径` 可另选目录。某一检查超时后，入口保存超时和已捕获的输出，继续其余检查，最终以非零状态汇报失败。

## 科学插图生成器

- **纯标准库亮暗双主题科学 SVG 绘图器（V2 / V3 / V4）**：默认生成模式**零第三方依赖（纯 Python 3 标准库）**，直接输出带真实 `<text>` 节点与 `@media (prefers-color-scheme: dark)` 适配的矢量图；其中 `generate_v2_figures_part2b.py`、`generate_v3_figures_part1.py`、`upgrade_legacy_svgs_part2.py` 等脚本内置可选 `--check-bbox` 视觉几何审计参数，仅在显式启用该参数时延迟导入 `playwright.sync_api`：
  - `codes/practice/generate_bloch_sphere.py`：生成单比特基础 Bloch 球 `bloch-sphere.svg`；
  - `codes/practice/generate_v2_figures_part1a.py`、`generate_v2_figures_part1b.py`、`generate_v2_figures_part2a.py`、`generate_v2_figures_part2b.py`：生成 19 幅 `v2-*.svg` 科学插图（覆盖第 01–08、10、12–14、16–18、Q1、Q3、Q4 章）；
  - `codes/practice/generate_v3_figures_part1.py`、`generate_v3_figures_part2.py`、`generate_v3_figures_part3.py`：生成 21 幅 `v3-*.svg` 科学插图（覆盖第 00、01、Q1、Q2、05、08、09、11、12、14、15、17、18、19、Q4、20、21 章）；
  - `codes/practice/generate_v4_figures.py`：生成 V4 新增与升级的亮暗双主题 `v4-*.svg` 科学插图；
  - `codes/practice/generate_cover_banner.py`：生成动态/静态双轨封面横幅 `cover-banner.svg` 与 `cover-banner-static.svg`；
  - `codes/practice/upgrade_legacy_svgs_part1.py`、`upgrade_legacy_svgs_part2.py`：将 14 幅历史专题与实验统计 SVG 原地升级为亮暗双主题与纯 `<text>` 中文标注；
  - `codes/practice/upgrade_round72_trajectories_svg.py`：直接基于 `codes/foundations/sdk/all-results.json` 归档的官方 QuTiP 轨迹数据重建 `round72-foundations-trajectories.svg`；
  - `codes/systems/plot_round71_spectrum.py`：纯标准库生成矩形脉冲失谐频谱图 `round71-systems-spectrum.svg`。
- **早期/专项 Matplotlib 绘图脚本**（依赖 `practice/requirements-figures.txt` 或对应 `sdk`/`sdk73` 锁定环境，具体命令与依赖见各组 README）：`codes/practice/plot_figures.py`、`codes/practice/research_figures.py`、`codes/practice/workflow_figures.py`、`codes/algorithms/generate_figure.py`、`codes/algorithms/round70_figures.py`、`codes/algorithms/round71_figures.py`、`codes/algorithms/round72_figures.py`、`codes/algorithms/round73_figures.py`、`codes/foundations/generate_diagnostic_figure.py`、`codes/foundations/generate_round71_eraser.py`、`codes/foundations/generate_round72_figure.py`、`codes/foundations/generate_round73_figure.py`、`codes/systems/plot_round70_cutoff.py` 与 `codes/sdk/round73/figures.py`。

上述绘图程序均不属于默认标准库统一验算入口，按需单独运行即可。

## 许可与离线副本边界

本仓库未对原创教材和教学代码声明开放许可证；公开可读不自动赋予转载或再许可权。第三方材料遵循各自原许可证，不因放在同一仓库而改变。详见 [vendor/README.md](vendor/README.md)。

离线阅读版也附带代码副本，方便阅读或另存；主要开发和运行入口是仓库根目录的本目录。Markdown 教材中的代码链接会自动转到离线副本。

## 回归测试、分章核验与独立复算入口

- `tests/test_snapshot_sources.py` 提供六种完全离线的隔离回归，包括下载失败、校验失败、成功发布和目录替换回滚；统一运行入口也执行这些测试。
- 第 15 章后选择、零失败上界、时间预算与准概率四组固定样本：`python3 codes/practice/research_checks.py`，输出 `practice/research-results.json`；配套图由 `python3 codes/practice/research_figures.py` 生成。
- 源码阅读练习的独立数学核对：`python3 codes/practice/source_reading_checks.py`。该程序不导入 `vendor` 文件；基础、算法与系统三组教学与核验脚本均已接入统一入口，最新统一运行结果写入 `work/research/code-validation.json`（早期归档报告原样保留以备追溯）。
- 逐章细算与工业工作流核验：基础组 `python3 codes/foundations/round71_checks.py --case all`、算法组 `python3 codes/algorithms/round71_checks.py all`、系统组 `python3 codes/systems/round71_checks.py --case all`（为保持历史哈希与引用可追溯而沿用原文件名）；工业工作流独立模型为 `python3 codes/practice/workflow_checks.py`（结果见 `practice/workflow-results.json`）。以上脚本均接入统一入口，不导入或执行 `vendor` 摘录。
- 跨库对照的纯标准库独立复算：基础组 `python3 codes/foundations/round72_stdlib.py --case all`、算法组 `python3 codes/algorithms/round72_checks.py all`、系统组 `python3 codes/systems/round72_checks.py --case all`，均已收录于统一入口。26 个核心开源项目的完整 SDK 实跑任务、依赖锁、原始样本与 C/C++ 构建说明单列于[SDK 隔离实跑总说明](sdk/README.md)，需在各自隔离环境中运行，不由默认入口联网安装。
- 进阶核验与已存档实跑结果复算：统一入口同时收录基础/算法/系统三组 `round73_checks.py`（`codes/foundations/round73_checks.py`、`codes/algorithms/round73_checks.py`、`codes/systems/round73_checks.py`）以及 `codes/sdk/round73/check_saved.py`，后者仅用标准库独立复算原始计数、聚类方差、Liouville 乘积与 MPF 目标值。面向其余扩展项目与完整工作流的隔离 SDK 与编译说明另见[进阶集成工作流归档](sdk/round73/README.md)（含可选批量调度入口 `codes/sdk/round73/run_workflows.py`，不由默认入口联网安装）；各组 `sdk73/` 目录保留真实运行环境、原始失败记录与样本，与 [codes/vendor/](vendor/README.md) 中 31 个项目 122 份固定提交源码摘录一一对应。
- `python3 codes/algorithms/round73_checks.py all` 对照固定档案中的四档非格点 HHL、两步数的行走概率和 QSVT 多项式及后选概率。只验数学时加 `--math-only`，报告会注明跳过 SDK 档案对照。SLC 归档校验逐批匹配种子身份，按实际读取的原始计数汇总随机化数和样本量，同时复算每批聚类标准误。
- **隔离环境交叉复核脚本**（需在对应隔离环境中安装 `numpy`/`scipy`/`stim` 等科学计算依赖，不接入默认纯标准库入口 `run_all.py`）：
  - `codes/foundations/round72_cross_algorithms.py`、`codes/foundations/round73_cross_gst.py`
  - `codes/algorithms/round73_cross_root.py`、`codes/algorithms/round73_cross_systems.py`
  - `codes/systems/crossreview72.py`、`codes/systems/sdk73/crossreview_algorithms.py`

## V3 / V4 新增离线标准库专题实验

- `codes/systems/sensing_lab.py`（对应[第 20 章](../handbook/20-quantum-sensing-metrology.md)，运行 `python3 codes/systems/sensing_lab.py`）：零外网纯标准库实现，覆盖 NV 单自旋灵敏度、Ramsey CFI/QFI/SLD 与根保真度 Bures 极限、GHZ（$N=2,3,4$）宇称测量与单比特丢失退相干归零、Huelga 1997 马尔可夫退相位标度与死时间惩罚、单轴扭转自旋压缩（Wineland $\xi_R^2$）与光学损耗压缩、CPMG 锁相滤波器及 HNLS 纠错传感 2 比特码等断言模块（详细说明见 [systems/README.md](systems/README.md)）。
- `codes/algorithms/simulation_engines_lab.py`（对应[第 21 章](../handbook/21-stabilizer-classical-simulation.md)，运行 `python3 codes/algorithms/simulation_engines_lab.py`）：零外网纯标准库实现，覆盖 Aaronson–Gottesman 稳定子表（Tableau）、3 比特矩阵乘积态（MPS）逐键 SVD 左正则构造与截断误差核算、海森堡绘景含噪 Pauli 传播（SPD）与 $\ell_1$ 截断上界三大迷你引擎，并与独立态矢量/密度矩阵精确参考解逐格断言比对（断言容差 `< 1e-12`，三引擎实测最大误差均不超过 `2.22e-15`）。
- `codes/algorithms/v4_algorithms_lab.py`（对应 V4 算法篇专项深化，运行 `python3 codes/algorithms/v4_algorithms_lab.py`）：零外网纯标准库数值验算脚本，对 V4 算法篇新增推导、复杂度边界与小规模精确对照执行确定性断言检验。
- `codes/practice/v4_practice_lab.py`（对应 V4 统计实践与工程边界深化，运行 `python3 codes/practice/v4_practice_lab.py`）：零外网纯标准库统计与实践数值验算脚本，对 V4 实践篇新增区间估计、误差预算与反例边界执行确定性断言检验。
