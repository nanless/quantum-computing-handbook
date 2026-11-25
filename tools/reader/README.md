# 离线阅读版与多格式出版工具链

正文源文件位于 `handbook/`，离线网页阅读版输出位于 `reader/`，合订本 PDF 与 EPUB 3 出版产物输出位于 `dist/`。整个 `reader/` 文件夹完整自包含（含本地 KaTeX 字体、预渲染公式、矢量图表、配套代码与离线交互实验台），复制整目录后直接打开 `reader/index.html` 即可零依赖离线阅读，无需服务器或联网；不要只复制单个 HTML 文件。

## 快速构建与全套验收命令

在项目根目录运行：

```sh
# 1. 安装锁定依赖与 Chromium（首次或依赖变更时）
npm ci --prefix tools/reader --ignore-scripts --no-audit --no-fund
npm exec --prefix tools/reader -- playwright install chromium

# 2. 构建离线阅读版（含 6 篇 26 章路线、展厅首页、可折叠本章解答与离线实验台）
node tools/reader/build.mjs

# 3. 浏览器三宽全量验收（1440px / 390px / 320px、暗色模式、交互实验台与 SVG 边界）
node tools/reader/verify.mjs

# 4. 全书质量与完整性门禁（公式定界符、术语统一、SVG 文本节点、26 章 271 题对齐）
node tools/reader/check-v3-quality.mjs

# 5. 专项算例与题答复核（或直接在仓库根目录运行 make check-all / make lint）
node tools/reader/check-network-examples.mjs
node tools/reader/check-qm-examples.mjs
node tools/reader/check-qm-review.mjs
```

仓库根目录已提供统一 `Makefile`（支持 `make test`、`make lint`、`make build`、`make verify`、`make pdf`、`make epub`、`make release`、`make check-all`），`tools/reader/package.json` 亦提供对应的 `npm run --prefix tools/reader <script>` 入口。PDF 后处理依赖锁定于 [`tools/reader/requirements-pdf.txt`](requirements-pdf.txt)（`PyMuPDF`、`pypdf`，可用 `make install-pdf` 安装）。

如需指定本机已安装的共享 Playwright 依赖或 Chromium 可执行文件，可传入环境变量 `HANDBOOK_NODE_MODULES` 与 `HANDBOOK_CHROMIUM`（切勿将本机绝对路径写入教材或仓库配置）。Mermaid 流程图在构建阶段通过仅绑定 `127.0.0.1` 的临时服务预渲染并缓存于 `work/render-cache/`，成品不依赖任何在线服务。

## 阅读版核心特性与六篇 26 章路线

- [**六篇 26 章阅读顺序**](../../handbook/README.md)保留 `00–21` 与 `Q1–Q4` 章号。`reading-order.mjs` 为首页、侧栏、上一章和下一章、PDF 分篇和目录、EPUB 阅读序和分篇题答提供同一顺序。`reading-order.test.mjs` 核对 Markdown 主目录、自检题速查表与解答正文的顺序，并检验 EPUB 分篇后的题答位置。
- **纸感制图桌双主题阅读体验（`reader.css` & `reader.js`）**：支持亮/暗模式手动切换（`#theme-toggle` + `localStorage` 持久化）与系统偏好自适应、顶部 2px 阅读进度条、右侧目录 ScrollSpy、四色语义 Callout 提示框、算例/练习标题微标、科学矢量图可见图注与原生 `<dialog>` 放大灯箱、代码块与行间公式（原始 TeX）一键复制、以及行内公式与后随标点防拆行胶水。
- **课程首页与交互实验台**。`reader/index.html` 集成量子干涉交互演示、六篇阅读顺序和科研复核概览。构建同步发布离线交互实验台 `reader/lab/quantum-lab.html`。
- **可折叠本章参考解答**：构建期从 `handbook/appendices/exercises.md` 自动解析对应章节的零跳步推导，以默认折叠的 `<details>` 卡片注入每章末尾（打印时自动全部展开），不改变正文 `<article>` 的公式计数与哈希校验。

## 多格式电子书出版（A4 PDF 与 EPUB 3）

在完成原稿更新后，可在项目根目录生成离线合订本 PDF 与原生 MathML EPUB 3：

```sh
# 构建带封面、页眉页码与 3 级 Unicode 书签的 A4 合订本 PDF -> dist/quantum-computing-handbook.pdf
node tools/reader/build-pdf.mjs

# 如需独立运行 PDF 后处理与 10 项出版质量门禁（元数据、3 级书签、内链、字形与体积检查）
python3 tools/reader/postprocess-pdf.py

# 构建原生 MathML 3 电子书 -> dist/quantum-computing-handbook.epub
node tools/reader/build-epub.mjs
```

- **A4 合订本 PDF 流水线（`build-pdf.mjs` + `postprocess-pdf.py`）**：零外网本地 KaTeX 预渲染与按块并行 Chrome 排版（`tagged: false`），经两遍构建探测精确正文页码并生成带右对齐页码的两栏目录，再由 PyMuPDF 原生合订、写入 `/PageLabels`（封面 `Cover` / 目录罗马页码 `i` 起 / 正文 `1` 起零偏移连续编号）与页眉页脚，生成 **3 级 Unicode 书签**与 **2,000+ 条精确内部跳转链接**，并执行 `/ToUnicode` CMap **康熙部首归一化**、字体子集化与流/SMask 去重无损压缩（成品稳定控制在 **`< 50 MiB`**，0 xref 损坏）。后处理主动清空不完整的 `/StructTreeRoot` 与 `/MarkInfo`（避免误导屏幕阅读器，并在 `work/research/pdf-build-report.json` 通过 `noMisleadingPartialTagTree` 如实记录 `structTreeRoot: false`、`structParentsPages: 0`）；PDF 用于印刷版式；可重排 EPUB 与 Web 提供原生公式语义，阅读器和辅助技术支持需分别核验。
- **EPUB 3 电子书流水线（`build-epub.mjs`）**：输出原生 MathML 3 公式与矢量 SVG（完整收录 26 章正文、7 篇附录含附录 G 审校记录及 6 篇实验册），包含可访问性发现元数据及 EPUB 2 NCX 兼容导航，由 Python 标准库打包为首条目无压缩 `mimetype` 的标准归档，并对全包 XML/XHTML/OPF/SVG 良构性及全部内部链接/锚点执行零报错门禁（报告写入 `work/research/epub-build-report.json`）。

> 浏览器“打印本章”仅作为单章便捷打印功能；正式合订本交付以 `build-pdf.mjs` + `postprocess-pdf.py` 及 `build-epub.mjs` 验收通过的 `dist/` 产物为准。

## GitHub Actions CI、Pages 与 Release 工作流

- `.github/workflows/ci.yml`：在 `push` 与 `pull_request` 时运行全套离线验收门禁（`python3 codes/run_all.py`、质量与隐私门禁、算例/题答复核、`build.mjs` 与 `verify.mjs`），显式安装 `fonts-noto-cjk` 与 `fonts-wqy-zenhei` 并缓存 Playwright 浏览器。
- `.github/workflows/pages.yml`：在主分支更新或手动触发时执行完整离线门禁与构建验证，收紧 `build` job 至只读权限，将 `reader/` 与带 GitHub Releases 入口的 `_pages/dist/index.html` 发布至 GitHub Pages。
- `.github/workflows/release-ebooks.yml` 通过手动操作触发。留空发行标签时只生成本次工作流制品。填写已存在的发行标签时，工作流在构建和发布前分别核对标签指向构建提交。全套文件包括 PDF、EPUB、Web ZIP、代码 ZIP、`BUILDINFO.json` 和 `SHA256SUMS.txt`。新发行先上传到草稿，下载复核所有制品再公开。失败后保留草稿，同一套制品可重试，已公开的版本只允许比对。

本地打包使用 `make release VERSION=v1.2.3 EPUBCHECK_JAR=/path/to/epubcheck.jar`。如果本机已有 `epubcheck` 命令，可省略 JAR 参数。正式工作流使用固定版本的官方 EPUBCheck 并拒绝错误与警告。打包前核对 Web、PDF、EPUB 构建时的源文件摘要及各成品摘要。打包器实际离线打开解压后的 Web ZIP，并运行代码 ZIP 适用的公开检查。完整仓库的 vendor 快照仍由 `make test` 校验。

## 验收报告、代码与历史检查说明

- **构建与浏览器验证报告**：仅写入 `work/research/reader-build-report.json` 与 `work/research/reader-verification.json`；V4 已停止向 `reader/research/` 复制内部日志与审校归档（`build.mjs` 构建前自动清理旧目录，`verify.mjs` 与 `build-release.mjs` 强制门禁校验 `reader/` 零 `research/` 与零 `STYLE.html`）。桌面及两种手机宽度、暗色模式、交互实验台与科学图截图保存于 `work/rendered/`。
- **验证覆盖范围**：包括全书所有生成页的 1440px / 390px / 320px 布局与溢出检查、源/输出与 `inputHashes`（含 `reader.js` 与 `quantum-lab.html`）SHA-256 核验、公式计数与 `mathSourceDigest`、标题序列与锚点、目录搜索与翻页顺序、`reader/lab/quantum-lab.html` 离线交互零报错，以及全部 `handbook/assets/*.svg` 的 `getBBox()` 边界与亮/暗双色渲染检查。
- **质量与隐私门禁（`check-v3-quality.mjs`）**：校验全书面向读者的 Markdown（含 `audit-log.md`，不再豁免）零 `\(...\)` / `\[...\]`、零禁用旧术语（`参数偏移` / `玩具模型` / `左线性`）、统一采用“解码”（仅放行 `亦称译码`、`旧称译码`、`vendor` 原文）、全部科学 SVG 含真实 `<text>` 节点、26 章自检题数与 `exercises.md` 精确对齐（总计 271 题），以及 `handbook/`、`codes/`（排除 `vendor/`）与 `tools/reader/` 零本机绝对隐私路径泄露。
- **离线教学代码**：运行 `python3 codes/run_all.py` 按清单执行标准库数值脚本与第三方快照哈希核对，结果写入 `work/research/code-validation.json`。构建会复制 `codes/` 并仅改写本书自编说明中的教材相对链接，第三方 `vendor/` 字节原样保留。
- **浏览器收尾保护**：`browser-cleanup.mjs` 在保存报告后为浏览器退出设置 10 秒上限，防止部分 Chrome 版本的残留传输句柄阻塞进程，且不会改变检查失败状态。
- **历史轮次脚本退役说明**：早期已失效且会覆写历史归档 JSON 的 `check-round71/72/73.mjs` 与 `verify-round71/72/73-visuals.mjs` 已于 V4 清理下线；原始历史运行证据文件仍完整保留于 `work/research/round7*-*.json` 供追溯。自动截图不代替人工目视验收，实际人工抽查范围另行记录于审校报告。
