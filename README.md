# 量子计算：从直觉到研究入口

一套面向初学者和入门研究生的中文量子计算教材。内容从数学与量子力学先修知识开始，逐步进入量子线路、算法、硬件、纠错、网络与研究实践；公式推导、手算例题和参考资料与正文相互链接。

下载或克隆本仓库后，打开 [离线阅读版](reader/index.html)（`reader/index.html`）即可阅读。请保留整个 `reader/` 文件夹；仅下载单个 HTML 页面会缺少样式、图片和其他章节。GitHub 网页上的 HTML 文件不等于已经部署的网站。

## 从哪里开始

- [全书目录与推荐阅读路线](handbook/README.md)
- [先修知识自测](handbook/appendices/prerequisites.md)
- [量子力学基础篇](handbook/quantum-mechanics/README.md)
- [符号表](handbook/appendices/notation.md)与[术语表](handbook/appendices/glossary.md)
- [实验、代码与音频](handbook/labs/README.md)及[算法与工业开源对照](handbook/appendices/software-practice.md)
- [参考资料](handbook/appendices/references.md)与[审校记录](handbook/appendices/audit-log.md)

`codes/` 包含可运行教学实验与带许可的第三方固定源码摘录；`handbook/` 是 Markdown 原稿；`reader/` 是已生成的离线阅读版；`tools/reader/` 包含构建和检查程序；`work/research/` 保存与正文相互引用的审校、算例和验证记录。

第72轮对24篇正文逐篇复核，补充章节练习、完整HHL/QSP/阴影等实现，以及26个完整SDK或C/C++项目的实际本地任务。代码、依赖锁、原始样本和明确边界见[完整SDK实验册](handbook/labs/sdk-validation.md)；当前第三方固定摘录仍为26项目97文件。数学01位于实验Q1之前，离线侧栏与翻页统一采用该顺序。逐章修改和验收见[第72轮整合记录](work/research/round72-final-integration.md)。

## 重新生成阅读版

需要 Node.js 和 Chromium。在仓库根目录运行：

```sh
npm ci --prefix tools/reader --ignore-scripts --no-audit --no-fund
npm exec --prefix tools/reader -- playwright install chromium
node tools/reader/build.mjs
node tools/reader/verify.mjs
```

更多算例核对命令及报告说明见 [构建说明](tools/reader/README.md)。阅读已经提交的 `reader/` 不需要安装这些工具。

文中产业、产品和工程进展可能随时间变化，请留意正文标注的核验日期，并通过所列原始资料复核。本仓库目前未附开放许可；公开可读不代表可以转载、改编或再授权。

第73轮再次逐篇审查24篇正文，补齐SDK实验册中的负谱HHL、SKW、QSVT选择位、两步MBQC、动态MPF、完整SLC/PEC、PNA、长序列GST及Philox并行等可验证缺口。新增逐步练习、原始样本与科学图；第三方固定摘录现为31项目122文件，旧26/97原字节保留。[本轮整合与验收](work/research/round73-final-integration.md)区分实际SDK运行、标准库复算、上游缺陷防护及尚未复现的硬件/生产范围。数学01仍在全部依赖它的物理与线路内容之前，侧栏和翻页一致。
