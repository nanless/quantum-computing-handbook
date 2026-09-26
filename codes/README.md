# 可复现实验与第三方源码

在仓库根目录运行 `python3 codes/run_all.py`。该入口只执行本书的标准库教学程序，并核对源码和音频清单；不联网、不运行第三方摘录、不请求云设备。不要使用 `python3 -O` 关闭断言。

| 目录 | 内容 | 入口 |
|---|---|---|
| foundations | 00–05、13、Q1–Q4 共11组基础实验 | `python3 codes/foundations/foundations_lab.py --case all` |
| algorithms | 06–08、16–18 共6组算法模型实验 | `python3 codes/algorithms/experiments.py all` |
| systems | 09–12、14、19 共6个系统程序 | 见该目录 README |
| practice | 15章统计实验、5个合成音频、科学图 | `python3 codes/practice/experiments.py` |
| vendor | 15个上游项目的固定源码摘录与许可 | `python3 codes/snapshot_sources.py --verify` |

教学实验结果是精确小模型、合成计数或固定种子模拟；不是新采集的真机数据。程序中的断言和各目录的 `expected-results.json` / `results.json` 提供复算依据。统一运行报告保存在 `work/research/round69-code-validation.json`。

音频生成：`python3 codes/practice/generate_audio.py`。绘图需要 `practice/requirements-figures.txt` 中锁定的包，生成命令是 `python3 codes/practice/plot_figures.py` 与 `python3 codes/algorithms/generate_figure.py`。这两个绘图程序不属于标准库统一运行入口。

本仓库未对原创教材和教学代码声明开放许可证；公开可读不自动赋予转载或再许可权。第三方材料遵循各自原许可证，不因放在同一仓库而改变。详见 [vendor/README.md](vendor/README.md)。

离线阅读版也附带代码副本，方便阅读或另存；主要开发和运行入口是仓库根目录的本目录。Markdown 教材中的代码链接会自动转到离线副本。

`tests/test_snapshot_sources.py` 提供六种完全离线的隔离回归，包括下载失败、校验失败、成功发布和目录替换回滚；统一运行入口也执行这些测试。
