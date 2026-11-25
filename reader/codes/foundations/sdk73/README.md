# 基础SDK第73轮

完整安装、四条实际运行任务、原始样本、CP+TP上游缺陷/正确接口、模型条件和复现命令见[基础第73轮说明](../round73-README.md)。实际完整运行`validate_sdks.py --case all`，锁定依赖与日志位于本目录，最终四case见[all-results.json](all-results.json)。默认标准库独立核算为父目录`round73_checks.py --case all`；不联网、不执行vendor摘录。

> **数学勘误提示（保留历史落盘原貌）：** 本目录历史归档脚本 `validate_sdks.py`（第 66 行）与结果文件 `all-results.json` 的 `delta_method_total_covariance` 字段在计算不对称读出反演 $r=(m+\alpha-\beta)/(1-\alpha-\beta)$ 的一阶方差传播时，曾将偏导 $\partial r/\partial\alpha=(1+r)/d$ 与 $\partial r/\partial\beta=(r-1)/d$ 写反，致使历史记录中的 $Z$ 轴总方差为 `0.0002956305`（SE `0.01719391`）。为维护历史运行日志与 `script_sha256` 证据链完整，本目录历史文件保持原字节不改动；现[第 02 章正文](../../../02-single-qubit.html#83-不对称读出校准方差传播与-spam-边界)及标准库脚本 `../round73_checks.py --case 02` 已纠正为正确公式（正确 $Z$ 轴总方差 `0.0002749724`，SE `0.01658229`，详见[第 73 轮说明勘误节](../round73-README.md#11-数学勘误不对称读出反演的一阶偏导与历史-sdk-归档对照)）。
