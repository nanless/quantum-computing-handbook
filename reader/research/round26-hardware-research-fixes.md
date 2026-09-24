# 第 26 轮硬件、编译控制与网络算例审校

审校日期：2026-09-22

## 范围与结论

- 独占修改：`handbook/09-hardware.md`、`handbook/14-compilation-control.md`。
- 只读核查：`handbook/12-security-network-frontiers.md` 及 `handbook/assets/entanglement-swapping.svg`，包括新增 BB84、两段链路等待时间、纠缠交换算例和明暗主题渲染。
- 未修改共享附录、README、图、工具或 `sources/`，未增加自检题。
- 找到并修复 2 组实质性问题：一处门基通用性条件写得过宽；一处表面码实验的“101 个物理比特”没有解释其与常见 $2d^2-1$ 计数的差异。另完成一组中文物理术语和标题去套话修订。
- 第 12 章的时效事实、公式和新图未发现需要修改的问题。

## 1. 第 09 章的修订

### 1.1 距离 7 表面码为何是 101 个物理比特

原文只写“101 个物理量子比特、距离 7”，初学者若刚学过旋转表面码的近似计数 $2d^2-1$，会算出 $2\times7^2-1=97$，容易误以为正文或公式有一处错了。

现改为：该实验运行在 105 比特处理器上，距离 7 存储实验实际使用 101 个物理比特，其中 49 个数据比特、48 个测量比特和 4 个额外泄漏清除比特。前两项相加正是裸旋转补丁的 97，额外 4 个来自边界泄漏清除。逻辑错误率与抑制因子没有改动。

一手证据：

- Google Quantum AI 等，[Quantum error correction below the surface code threshold](https://www.nature.com/articles/s41586-024-08449-y)，*Nature* 638, 920–926 (2025)。正文明确列出 49 data、48 measure、4 additional leakage removal qubits，并给出 $\epsilon_7=(1.43\pm0.03)\times10^{-3}$、$\Lambda=2.14\pm0.02$。
- [Author Correction](https://www.nature.com/articles/s41586-026-10559-8)，用于保留原文已经写明的 2026 年更正边界。

限定：101 是该距离 7 存储实验占用的物理比特数，不是处理器总量，也不是逻辑算法的通用物理开销。论文使用离线高精度译码；不能据此推断任意逻辑门已经实时容错。

### 1.2 术语

- 把“激发态人口衰减”改为“激发态占据概率的衰减”。
- 把“校准如何形成依赖闭环”改为“校准参数如何相互依赖并在漂移后重新验证”，直接说明动作和触发条件。

## 2. 第 14 章的修订

### 2.1 修正固定角度旋转的通用性条件

原文说“$R_z$ 和某个固定角度的 $X$ 轴旋转”即可继续分解。这个说法过宽：例如只有固定的 $R_x(\pi)$ 与任意 $R_z$ 并不能精确生成任意单比特酉矩阵。

现改为一个明确可用的常见组合：任意角度 $R_z$ 加固定 $R_x(\pi/2)$，后者常记为 $\sqrt{X}$ 或 SX；同时明确“并非任取一个固定角度都自动足够”，后端必须公布完整通用门基和分解规则。

官方技术文档：

- IBM Quantum，[Represent quantum computers for the transpiler](https://quantum.cloud.ibm.com/docs/en/guides/represent-quantum-computers)：目标机门基必须通用，示例基包含 `rz`、`sx`、`x`、`ecr`。
- IBM Quantum，[Fractional gates](https://quantum.cloud.ibm.com/docs/en/guides/fractional-gates)：说明任意 $R_x(\theta)$ 如何在常见超导门基中分解为虚拟 $R_z$ 与有限时长的 $\sqrt{X}$ 门。

限定：这里说明的是单比特精确综合；完整多比特通用性还需要纠缠门。具体后端可能提供其他原生旋转或参数化门，不能把 IBM 示例当成所有硬件的唯一门基。

### 2.2 物理中文与标题

- “控制相位账本”改为“控制器的相位记录”。
- Rabi 实验的“人口振荡”改为“激发态占据概率随驱动时长或幅度振荡”。
- “能实时闭环”改为“能及时完成实时反馈”。
- 标题“Bell 电路落地”改为“Bell 电路的物理执行”，并把“端到端检查”改成“从编译到测量依次检查”。

标题改动前已搜索全书和研究报告，没有正文链接指向旧标题锚点，故没有产生站内失效链接。新标题锚点为 `#12-一个完整例子bell-电路的物理执行`；当前也没有章节依赖它。

### 2.3 实时译码数字核验

正文的 2026 年例子无需改数值。原论文明确报告：8 比特 stability-8 实验、9 个 measurement rounds、完整响应 9.6 μs，其中译码 6.5 μs，通信与控制 3.1 μs。论文还说明该实验只测量四个 $Z\otimes Z$ 稳定子，省略中央 $X^{\otimes4}$ 稳定子，且一次综合征提取约 1.7 μs。因此正文保留“小规模集成实例，不能外推到任意码距”的限定是必要的。

一手证据：L. Caune 等，[Demonstrating real-time and low-latency quantum error correction with superconducting qubits](https://www.nature.com/articles/s41467-026-73331-6)，*Nature Communications* 17, 7383 (2026)。

## 3. 第 12 章只读核查

### 3.1 NIST 与网络实验的时效事实

以下表述截至 2026-09-22 仍与一手页面一致：

- NIST 的 [PQC 项目主页](https://csrc.nist.gov/projects/post-quantum-cryptography)仍把 HQC 写为正在标准化的额外 KEM；[Selected Algorithms](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/selected-algorithms)标为 “FIPS coming soon”。因此“已选择”不等于“最终 FIPS 已发布”的正文限定正确。
- Knaut 等的 [Nature 原论文](https://www.nature.com/articles/s41586-024-07252-z)明确区分 40 km 盘纤与 35 km 波士顿地区部署光纤回路；部署链路是 35 km、17 dB 损耗的回路，并非两个相距 35 km 的独立城市节点。正文已经保留“光纤盘/部署回路”边界。
- Kucera 等的 [npj Quantum Information 原论文](https://www.nature.com/articles/s41534-024-00886-x)报告 14.4 km 萨尔布吕肯城市暗纤、光子—光子和离子—光子纠缠，以及离子态到远端电信光子的传送。正文没有把它误写成多跳中继或远程存储器—存储器纠缠。

### 3.2 BB84 复算

在正文明确给定的理想截获—重发模型中：

- 保留比特中，Eve 选错基的概率为 $1/2$；选错后 Bob 出错的条件概率为 $1/2$，所以 QBER 为 $1/4$。
- 1000 个发送信号的期望筛选量为 500，期望错误数为 125；$125/500=25\%$ 与 $125/1000=12.5\%$ 的分母区分正确。
- 20 个独立抽查位均未发现错误的概率为 $(3/4)^{20}=0.0031712$。
- $h_2(0.01)=0.0807931$，故 $1-2h_2(0.01)=0.8384137$；$h_2(0.05)=0.2863970$，故相应下界为 $0.4272061$。数值与正文一致。

安全公式的一手来源：P. W. Shor 与 J. Preskill，[Simple Proof of Security of the BB84 Quantum Key Distribution Protocol](https://doi.org/10.1103/PhysRevLett.85.441)，*Physical Review Letters* 85, 441–444 (2000)。正文正确把 $1-h_2(e_b)-h_2(e_p)$ 限定在理想单光子、渐近、已认证经典信道和相应安全模型内，没有把约 11% 写成通用器件阈值。

### 3.3 两段几何等待时间复算

取 $p=0.1,q=0.9,\tau=1\,\mathrm{ms}$：

$$
\mathbb E[\max(X,Y)]
=\frac2p-\frac1{1-q^2}
=20-\frac1{0.19}
=14.736842.
$$

先成功链路的额外等待时隙 $D=|X-Y|$ 满足

$$
\mathbb E[D]
=\frac2p-\frac2{1-q^2}
=9.473684.
$$

正文给出的分布

$$
\Pr(D=0)=\frac p{2-p},\qquad
\Pr(D=d)=\frac{2pq^d}{2-p},\quad d\ge1
$$

归一化为 1。取 $T_{\rm mem}=20\,\mathrm{ms}$、$a=e^{-\tau/T_{\rm mem}}$，

$$
\mathbb E[a^D]
=\frac p{2-p}\frac{1+qa}{1-qa}
=0.678904,
$$

而 $e^{-\mathbb E[D]\tau/T_{\rm mem}}=0.622704$。正文的 0.679 与 0.623 均正确，也正确说明了“平均后再取指数”与“指数后再平均”不同。

相关一手研究：E. Shchukin、F. Schmidt、P. van Loock，[Waiting time in quantum repeaters with probabilistic entanglement swapping](https://doi.org/10.1103/PhysRevA.100.032322)，*Physical Review A* 100, 032322 (2019)。当前算例是两条独立同参链路、无限重试、成功后可存储的教学特例，不含交换失败、超时截断或经典往返。

### 3.4 纠缠交换复算与图片检查

按 $A,B_1,B_2,C$ 排序，两个 $|\Phi^+\rangle$ 的展开式正确。投影到 $B_1B_2$ 的 $|\Phi^+\rangle$ 后得到

$$
{}_{B_1B_2}\langle\Phi^+|\Omega\rangle
=\frac{|00\rangle_{AC}+|11\rangle_{AC}}{2\sqrt2}
=\frac12|\Phi^+\rangle_{AC},
$$

其范数平方为 $1/4$。四个结果的 $I,Z,X,XZ$ 条件修正与本书从右向左作用的约定一致；忽略测量记录时，四个正交 Bell 态的等权混合为 $I_4/4$。

`entanglement-swapping.svg` 通过 XML 解析。实际检查了 1100×590 的明、暗主题渲染：上方两条实线只连接 $A$–$B_1$、$B_2$–$C$；虚线箭头从中间测量向两端传播；下方按记录修正后只连接 $A$–$C$。标题、图注和正文都明确实线是纠缠配对关系而非信号传播路径，未发现方向、标签、遮挡或暗色对比问题。

原始协议：M. Żukowski 等，[“Event-ready-detectors” Bell experiment via entanglement swapping](https://doi.org/10.1103/PhysRevLett.71.4287)，*Physical Review Letters* 71, 4287–4290 (1993)。

## 4. 其他复算与静态检查

- 第 14 章 Rabi 算例：$\Omega/2\pi=10\,\mathrm{MHz}$ 时，$T_\pi=\pi/\Omega=50\,\mathrm{ns}$，$T_{\pi/2}=25\,\mathrm{ns}$；$\Delta/2\pi=1\,\mathrm{MHz}$ 时 $\Delta/\Omega=0.1$。通过。
- 反馈等待算例：六项相加为 1.6 μs；$1-e^{-1.6/100}=0.015873$，即 1.59%。通过。
- 第 14 章旧标题“Bell 电路落地”没有被任何 Markdown 链接引用；已检查现有第 09、11、14 章锚点引用，均仍可解析。
- 没有改动第 12 章、新 SVG、练习答案或自检题数量。

## 5. 保留的边界

- HQC、硬件里程碑和 2026 实时译码结果属于时效事实，后续版本必须继续保留截止日期并复查官方页面或论文更正。
- $R_z+\sqrt X$ 是常见单比特通用基示例，不代表所有后端的原生门，也不代表脉冲误差、泄漏和串扰已由代数分解解决。
- 两段等待与纠缠交换是理想教学模型；真实网络还要加入不等链路概率、经典往返、有限缓存、交换成功率、存储退相干和探测误报。

