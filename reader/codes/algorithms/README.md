# 算法、模型与容量：可执行教学实验

本目录是本书自行编写的小规模参考计算。六组实验只依赖 Python 3 标准库；可选绘图另需 matplotlib。不请求云服务，不运行下载的第三方源码。完整问题、推导、答案和证据边界见 [实验说明](../../labs/algorithms.html)。

在仓库根目录运行：

```sh
python3 codes/algorithms/experiments.py all
```

若已安装 matplotlib，可运行 `python3 codes/algorithms/generate_figure.py` 重建图；本轮使用 matplotlib 3.9.4、NumPy 2.0.2，并查看生成 PNG 检查标签与图例。

可把 `all` 换成 `06`、`07`、`08`、`16`、`17`、`18` 单独检查一组。脚本使用普通 Python 运行，不能加关闭断言的 `-O`。固定输入，无随机采样，因而无需随机种子；输出为确定性概率/误差预算，不冒充硬件 shots 或实验计数。第 17 组的 20/100 是题目给定的假设校准记录，不是本次运行收集的数据。

- `experiments.py`：六组参考计算与独立解析断言；基序按整数对应的显示二进制串，最高位在左。
- `expected-results.json`：本轮实际运行输出。浮点最后几位允许平台级微差，验收用 `1e-10` 容差。
- `generate_figure.py`：从同一组计算生成 `handbook/assets/algorithm-lab-checks.svg`，概率曲线是计算结果；两点之间的线仅便于辨认离散点。

算法边界：直接 DFT 求和是经典小规模相位估计模拟；振幅数组的内存随比特数指数增长；QAOA 只实现三顶点路径；QSP 实验没有实现一般相位合成；信道代码计算单次相干信息并使用正文容量定理，不证明正则化容量。没有隐藏调用生产量子求解器。

原始算法及官方工业研究入口列在实验页。统一第三方代码存档和提交版本以 [vendor 清单](../vendor/manifest.json) 为准；不要将本目录教学实现和该清单里的上游源码混为一谈。
