# 系统实验：从噪声标签到长期吞吐

六个脚本均为本手册原创教学程序，只用 Python 标准库，在 Python 3.9.6 实际运行通过。脚本不会连接量子设备，也不需要账户或密钥。数据全部为模型参数、合成日志或伪随机模拟，不是真机测量。

在项目根目录分别运行：

```sh
python3 codes/systems/hardware_flags.py
python3 codes/systems/weighted_decoder.py
python3 codes/systems/factory_schedule.py
python3 codes/systems/network_wait.py
python3 codes/systems/routing_mapping.py
python3 codes/systems/service_timeline.py
```

| 程序 | 对应章节 | 核心断言 | 参考输出 |
|---|---|---|---|
| `hardware_flags.py` | 09 硬件 | 四类计数守恒，条件概率分母为零时返回 `None` | 精确率 0.3290799194；漏检 20 |
| `weighted_decoder.py` | 10 纠错 | 八错误概率归一化，残余仅为恒等或逻辑 X | 加权失败 0.01；最少翻转失败 0.0432 |
| `factory_schedule.py` | 11 资源 | 每次消费前供应足够，上一层已结束 | 一厂 16 周期；两厂 10 周期 |
| `network_wait.py` | 12 网络 | 解析值与固定种子样本均值在六标准误内 | 解析等待 11.428571；模拟 11.44125 |
| `routing_mapping.py` | 14 编译 | 八基向量和一个复态等价；不解释映射有反例 | 最大振幅误差 0；4 门或恢复后的 7 门 |
| `service_timeline.py` | 19 运维 | 重叠/嵌套/相接区间只算一次 | 在线 20 h；合格 18 h；75000 合格 shots/s |

完整实际运行输出保存在 [expected-results.json](expected-results.json)，其中同时记录 Python 版本。有随机性的程序明确设置 `69012` 或 `69014`；其余程序是完全确定性的精确枚举或算术，不需要随机种子。`assert` 是教学不变量检查，请不要用 Python 的 `-O` 选项关闭它们。浮点输出最后几位可能随环境变化，应按文档精度或误差容限比较。

手算过程、后续练习与开源研究路线见[系统实验册](../../handbook/labs/systems.md)。第三方源码位于上级 `vendor`，有各自许可证；这里的六个标准库脚本不依赖第三方源码快照。
