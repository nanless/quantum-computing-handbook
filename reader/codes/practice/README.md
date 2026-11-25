# 实验方法、统计验证与绘图脚本说明

本目录配套[第 15 章：实践路线](../../15-practice-research.html)与[实践实验册](../../labs/practice.html)，包含离线统计检验脚本、工作流核验程序与全书科学图生成代码。统计与验证脚本全部仅依赖 **Python 3 标准库**，不联网、不调用云服务；绘图脚本另需 `matplotlib` 与 `numpy`（依赖见 [requirements-figures.txt](requirements-figures.txt)）。

所有验证脚本必须使用普通 `python3` 运行，**不得加关闭断言的 `-O` 参数**。

## 一、纯标准库统计与验证脚本

在仓库根目录运行：

```sh
python3 codes/practice/experiments.py
python3 codes/practice/research_checks.py
python3 codes/practice/v4_practice_lab.py
python3 codes/practice/source_reading_checks.py
python3 codes/practice/workflow_checks.py
```

各脚本覆盖范围与独立核验内容：

| 脚本文件 | 配套位置 | 核验内容与随机种子约定 |
|---|---|---|
| `experiments.py` | [实验册 P15-A–C](../../labs/practice.html) | Bell 三基等样本/不等样本 Hoeffding 下界、ZNE $c=(1,3)$ 固定总预算 4,000 shots 均分 $5\times$ vs 最优 $3:1$ 分配 $4\times$、20 次独立检验假阳性率 $64.15\%$（确定性公式，无随机种子，输出写入 `results.json`） |
| `research_checks.py` | [实验册 P15-D–G](../../labs/practice.html) | 后选择接受率与每尝试交付率、零失败精确 Clopper–Pearson 上界（$N=2995$）与 $n=20$ 全覆盖网格枚举、按墙钟耗时分配预算 $N_i \propto |a_i|/\sqrt{c_i}$、准概率分解（QPD）与 CNOT 切割方差 $9^k$（确定性枚举，输出写入 `research-results.json`） |
| `v4_practice_lab.py` | [第 15 章 §2–4](../../15-practice-research.html) 与 [第 08 章 §7](../../08-applications.html) | ① ZNE 固定总 shots 精确倍率（$c=(1,2)$ 均分 $10\times$/最优 $9\times$、$c=(1,3)$ $5\times$/$4\times$、三点 Richardson $57\times$/$49\times$）及 PEC 因子；② Wald vs Wilson 精确二项覆盖率、$k=0$ 零失败 Bootstrap 崩溃反例、Bell 非线性根保真度百分位/BCa Bootstrap 区间、10 批漂移 $\chi^2$/聚类 SE/Cluster Bootstrap；③ 少聚类 $t_{B-1}$ 分位数（$B=4, 10$）10,000 次蒙特卡洛覆盖率与 Holm/BH-FDR 五项表；④ 纯标准库 $O(2^n)$ 张量切片引擎与线路等价性验证（QCEC 第一层 16 条随机乘积态证伪）。随机模拟全部锁定固定种子 `20261125` |
| `source_reading_checks.py` | [软件实践附录](../../appendices/software-practice.html) | 第三方源码摘录接口与本地固定结果一致性核对（输出写入 `source-reading-results.json`） |
| `workflow_checks.py` | 实验工作流归档 | 端到端数据契约、批处理记录与核查字段完整性测试（输出写入 `workflow-results.json`） |

## 二、科学图生成脚本

- `plot_figures.py`、`research_figures.py`、`workflow_figures.py`、`generate_bloch_sphere.py`、`generate_cover_banner.py`、`generate_v2_figures_part*.py`、`generate_v3_figures_part*.py`、`generate_v4_figures.py`：全书由公式或可复算数据驱动的科学 SVG 生成脚本。

## 三、适用边界说明

本目录的统计与模拟程序用于教学演示、区间性质核验与小规模线路原型自检：
- 合成计数与蒙特卡洛试验不代表真实量子硬件的物理测量结果；
- 纯标准库 $O(2^n)$ 张量切片引擎与随机乘积态 QCEC 原型仅用于验证方法与小规模线路（$n \le 12$），大规模编译形式化等价性验证应使用 MQT QCEC 等专业决策图/ZX 引擎。
