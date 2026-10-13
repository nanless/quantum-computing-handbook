# 可复现实验与第三方源码

在仓库根目录运行 `python3 codes/run_all.py`。该入口只执行本书的标准库教学程序，并核对源码和音频清单；不联网、不运行第三方摘录、不请求云设备。不要使用 `python3 -O` 关闭断言。

| 目录 | 内容 | 入口 |
|---|---|---|
| foundations | 00–05、13、Q1–Q4 共11组原实验及11组新增诊断 | `python3 codes/foundations/foundations_lab.py --case all` |
| algorithms | 06–08、16–18 共6组原实验及6组新增检查 | `python3 codes/algorithms/experiments.py all` |
| systems | 09–12、14、19 共12个系统程序 | 见该目录 README |
| practice | 15章7组统计实验、5个合成音频、科学图 | `python3 codes/practice/experiments.py` |
| review | 交换复核的两组独立计算路径 | `python3 codes/review/cross_foundations.py` 与 `cross_systems.py` |
| vendor | 31个上游项目的固定源码摘录与许可 | `python3 codes/snapshot_sources.py --verify` |

教学实验结果是精确小模型、合成计数或固定种子模拟；不是新采集的真机数据。程序中的断言和各目录的 `expected-results.json` / `results.json` 提供复算依据。统一运行报告保存在 `work/research/code-validation.json`。

音频生成：`python3 codes/practice/generate_audio.py`。绘图需要 `practice/requirements-figures.txt` 中锁定的包，生成命令是 `python3 codes/practice/plot_figures.py` 与 `python3 codes/algorithms/generate_figure.py`。绘图程序不属于标准库统一运行入口；新增生成器还包括 `practice/research_figures.py`、`foundations/generate_diagnostic_figure.py`、`algorithms/round70_figures.py`、`systems/plot_round70_cutoff.py`，具体命令、图名和依赖见各组README。

本仓库未对原创教材和教学代码声明开放许可证；公开可读不自动赋予转载或再许可权。第三方材料遵循各自原许可证，不因放在同一仓库而改变。详见 [vendor/README.md](vendor/README.md)。

离线阅读版也附带代码副本，方便阅读或另存；主要开发和运行入口是仓库根目录的本目录。Markdown 教材中的代码链接会自动转到离线副本。

`tests/test_snapshot_sources.py` 提供六种完全离线的隔离回归，包括下载失败、校验失败、成功发布和目录替换回滚；统一运行入口也执行这些测试。

第15章新增后选择、零失败上界、时间预算与准概率四组固定样本：`python3 codes/practice/research_checks.py`，输出 `practice/research-results.json`。图由 `python3 codes/practice/research_figures.py` 生成，依赖仍见 `practice/requirements-figures.txt`。

源码阅读练习的独立数学核对：`python3 codes/practice/source_reading_checks.py`。该程序不导入vendor文件；新版基础、算法和系统实验均已接入统一入口。历史round69报告保留，最新统一结果写入 `work/research/code-validation.json`。

第71轮逐章细算：基础 `python3 codes/foundations/round71_checks.py --case all`，算法 `python3 codes/algorithms/round71_checks.py all`，系统 `python3 codes/systems/round71_checks.py --case all`。各组的round71说明与结果提供固定输入、单位、参数边界及详细答案；均接入统一入口。工业工作流独立模型为 `python3 codes/practice/workflow_checks.py`，结果见 `practice/workflow-results.json`；图生成命令 `python3 codes/practice/workflow_figures.py` 使用上述固定绘图依赖。它们不导入或执行vendor摘录。

第72轮逐章核算新增三组入口：基础归档独立复算 `python3 codes/foundations/round72_stdlib.py --case all`、算法 `python3 codes/algorithms/round72_checks.py all`、系统 `python3 codes/systems/round72_checks.py --case all`。统一入口收录它们。完整26项目的实际SDK任务、依赖锁、原始样本和C/C++构建单列于[SDK说明](sdk/README.md)，需各自隔离环境，不由默认入口联网安装。

第73轮默认入口新增基础/算法/系统三个`round73_checks.py`及`codes/sdk/round73/check_saved.py`，总34入口。后者用标准库独立复算原计数、聚类方差、Liouville乘积与MPF目标。完整SDK和编译入口另见[第73轮](sdk/round73/README.md)，不由默认入口安装或联网。各组三套sdk73记录保留实际环境、原失败和样本；源归档31项目122文件中旧26/97未改变。
