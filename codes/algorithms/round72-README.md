# 第72轮算法组练习

八篇正文新增10组详细练习，完整SDK说明及原始样本见[SDK说明](sdk/README.md)。

```sh
python3 codes/algorithms/round72_checks.py all
```

该标准库入口独立核算第13章阴影纯度插件偏差和无偏U统计，以及Q4相干态截止尾部与无限剩余项上界；单项参数为 `13`、`q4`。它不替代SDK HHL、QSP、随机阴影等真实运行，完整记录在 [sdk/round72-results.json](sdk/round72-results.json)。

[绘图程序](round72_figures.py)在算法SDK环境读取真实结果，生成算法三联SVG；绘图依赖已在该环境锁定。
