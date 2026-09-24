# 量子计算：从直觉到研究入口

一套面向初学者和入门研究生的中文量子计算教材。内容从数学与量子力学先修知识开始，逐步进入量子线路、算法、硬件、纠错、网络与研究实践；公式推导、手算例题和参考资料与正文相互链接。

下载或克隆本仓库后，打开 [离线阅读版](reader/index.html)（`reader/index.html`）即可阅读。请保留整个 `reader/` 文件夹；仅下载单个 HTML 页面会缺少样式、图片和其他章节。GitHub 网页上的 HTML 文件不等于已经部署的网站。

## 从哪里开始

- [全书目录与推荐阅读路线](handbook/README.md)
- [先修知识自测](handbook/appendices/prerequisites.md)
- [量子力学基础篇](handbook/quantum-mechanics/README.md)
- [符号表](handbook/appendices/notation.md)与[术语表](handbook/appendices/glossary.md)
- [参考资料](handbook/appendices/references.md)与[审校记录](handbook/appendices/audit-log.md)

`handbook/` 是 Markdown 原稿；`reader/` 是已生成的离线阅读版；`tools/reader/` 包含构建和检查程序；`work/research/` 保存与正文相互引用的审校、算例和验证记录。

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
