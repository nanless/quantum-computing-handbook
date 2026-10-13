# 离线阅读版

正文源文件位于 `handbook/`，输出位于 `reader/`。复制整个 `reader` 文件夹后，打开其中的 `index.html` 即可阅读，无需服务器或联网。不要只复制单个 HTML 文件。

在项目根目录运行：

```sh
npm ci --prefix tools/reader --ignore-scripts --no-audit --no-fund
npm exec --prefix tools/reader -- playwright install chromium
node tools/reader/build.mjs
node tools/reader/verify.mjs
node tools/reader/check-network-examples.mjs
node tools/reader/check-qm-examples.mjs
node tools/reader/check-qm-review.mjs
```

构建依赖锁定在 `package-lock.json`。需要 Node.js、Playwright 和 Chromium；按上面命令安装即可，不依赖作者电脑的路径。如已有共享的 Playwright 运行环境，可用 `HANDBOOK_NODE_MODULES` 指向含 Playwright 的依赖目录，用 `HANDBOOK_CHROMIUM` 指向 Chromium 可执行文件。Mermaid 通过仅绑定本机的临时服务渲染，构建完成后关闭；成品不依赖该服务。

构建报告与验证报告位于 `work/research/reader-build-report.json`、`work/research/reader-verification.json`，页面与科学插图截图位于 `work/rendered/`。验证包括当前 40 页的宽屏与窄屏检查、原稿与输出哈希、公式内容和顺序、小节标题、资源与链接、目录交互及 SVG 文字边界。量子力学基础篇单独分组，保留原主篇编号；两组的翻页顺序分别检查。第 15 章的代码注释保留在代码块内；标题须从 Markdown 结构提取，不能按行首井号直接扫描。

网络算例检查独立计算四个 Bell 投影与修正、丢弃记录后的密度矩阵、等待分布的有限双重和与闭式，结果写入 `work/research/network-example-checks.json`。它只验证这些小模型的代数和数值，不替代 QKD 安全证明、真实硬件模型或全部正文定理的审校。当前并未把浏览器打印结果作为经过逐页验收的 PDF 交付。

量子力学算例检查复算干涉、Pauli 不确定度、势阱和 Gaussian 积分、矩形势垒边界匹配及通量守恒、热占据和 Rabi 脉冲，写入 `work/research/qm-example-checks.json`。这些检查验证明确模型的公式与数字，不代替物理公设、近似条件和教学表达的独立审阅。

题答复核检查全书编号、新基础篇答案与审稿草稿的一致性、相位符号同步及全局相位的概率不变性，写入 `work/research/qm-question-inventory.json`。

## 章级实验、源码和音频

`python3 codes/run_all.py` 执行本书标准库实验并核对第三方快照哈希与5段WAV格式；最新统一结果写入 `work/research/code-validation.json`，不会覆盖历史轮次报告。科学图重建需要 `codes/practice/requirements-figures.txt` 中的可选依赖。第三方摘录不参与执行。

构建程序会复制 `codes/`，并仅改写本书自编代码说明中指向教材的链接；vendor 文件逐字节保留。`reader/codes/run_all.py` 也能在复制后的阅读版布局下运行；生成的本地检查报告在 `reader/work/research/`。浏览器检查涵盖40页两种宽度、代码副本哈希以及音频元数据加载。音频不自动播放。

如果没有 Playwright 对应浏览器，可用 `HANDBOOK_CHROMIUM` 指向已安装的 Chrome/Chromium；不要把本机绝对路径写进教材。浏览器执行权限与依赖存在性是环境条件，失败时应保留错误而非报告检查通过。

第71轮的额外检查：`node tools/reader/check-round71.mjs` 核对24章独立练习标签、代码入口和26项目97文件的目录一致性；`node tools/reader/verify-round71-visuals.mjs` 生成24章×两宽度的新增内容截图、四张科学图的完整图像与上下文。后者只生成截图并检查基础溢出，人工目视范围须另写报告，不能将截图数量当成已逐屏读审。先完成构建，再运行浏览器检查；可沿用上文HANDBOOK_CHROMIUM环境参数。
