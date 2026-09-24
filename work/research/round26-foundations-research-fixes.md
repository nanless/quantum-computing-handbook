# 第 26 轮基础数学与量子信息调研修订

日期：2026-09-22  
范围：`handbook/00-overview.md`、`handbook/01-math.md`、`handbook/13-quantum-information.md`。  
边界：未修改 `sources/`、共享附录、README、图片或工具；未新增自检题。

## 1. 本轮方法

本轮没有沿用第 25 轮的结论，而是重新逐段检查三章，按以下顺序审阅：

1. 初学者在本段第一次见到什么对象；
2. 文字是否把“目前未知”写成“不可能”，或把一个实验里程碑写成概念定义；
3. 数学定义是否给全条件，能否用二维例子核查；
4. 数值例子是否解释了操作含义，而不仅是算出一个数；
5. 结论是否与权威教材、公开课程或原始论文一致。

## 2. 权威来源与支持范围

以下页面均于 2026-09-22 访问。

| 来源 | 发布信息 | 本轮用于核对的内容 |
|---|---|---|
| John Preskill, [Quantum Computing in the NISQ era and beyond](https://quantum-journal.org/papers/q-2018-08-06-79/) | *Quantum* 2, 79；2018-08-06 | NISQ 指受噪声限制的中等规模设备，不等同于容错计算，也不是一套严格技术成熟度分级。 |
| Google Quantum AI, [Suppressing quantum errors by scaling a surface code logical qubit](https://www.nature.com/articles/s41586-022-05434-1) | *Nature* 614, 676–681；2023-02-22 | 增大码距后逻辑错误下降是可扩展纠错的重要证据，但论文也明确区分 crossover、below-threshold 与特定逻辑错误指标。 |
| John Watrous, [The Theory of Quantum Information, Chapter 1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.1.pdf) | Cambridge University Press 书稿；2018 | 正半定算符的等价条件：二次型非负、厄米且全部本征值非负；同时核对酉算符与谱分解。 |
| John Preskill, [Quantum Computation lecture notes](https://www.preskill.caltech.edu/ph229/) | Caltech 公开课程讲义；第 2、3 章 2015 年修订 | 纯态、全局相位、测量与演化的标准教学表述。 |
| C. H. Bennett et al., [Concentrating Partial Entanglement by Local Operations](https://arxiv.org/abs/quant-ph/9511030) | *Physical Review A* 53, 2046–2052 (1996)；预印本 1995-11-21 | 多份二分纯态通过局域操作与经典通信浓缩为 Bell 对，渐近产率趋于纠缠熵。 |
| M. Mohseni, A. M. Steinberg, J. A. Bergou, [Optical Realization of Optimal Unambiguous Discrimination for Pure and Mixed Quantum States](https://doi.org/10.1103/PhysRevLett.93.200403) | *Physical Review Letters* 93, 200403；2004-11-09 | 非正交态不能做零错误、每次必答的确定性判别；允许“不确定”结果后可以无歧义判别。 |
| M. Ban, K. Yamazaki, O. Hirota, [Accessible information in combined and sequential quantum measurements on a binary-state signal](https://doi.org/10.1103/PhysRevA.55.22) | *Physical Review A* 55, 22–26；1997-01-01 | 二元纯态信号的可访问信息；用于核对等先验 $|0\rangle,|+\rangle$ 的实际最优互信息。 |
| C. A. Fuchs, [Distinguishability and Accessible Information in Quantum Theory](https://arxiv.org/abs/quant-ph/9601020) | 博士论文预印本；1996-01-23 | 区分最小错误判别、可访问信息与 Holevo 上界，并核对二元纯态的对称例。 |

## 3. 发现与修订

### 3.1 第 00 章：全景与证据边界

#### 发现 1：文字说“四层”，流程图实际有五个节点

- 原问题：经典问题与数据、编码、量子演化、测量采样、经典后处理共五个环节，却写成“四层”。初学者会不知道是图错还是文字错。
- 修订：改为“把一次端到端计算拆开，可看到五个相连环节”，与 Mermaid 图逐项一致。
- 位置：`00-overview.md` 第 7–15 行附近。

#### 发现 2：把“目前没有已知优势”写成了无条件的“没有优势”

- 原问题：“对大量日常任务没有优势”是超过现有证据的否定命题。
- 修订：改成“目前没有已知的量子优势”，并明确这是知识现状，不是不可能性定理；第 5 节相应把“没有理由期待”改成“目前没有已知证据表明会普遍替代”。
- 位置：第 5 行及第 94 行附近。

#### 发现 3：四阶段容易被误读为正式、互斥的成熟度标准

- 原问题：不同平台可能同时做物理比特、纠错与逻辑线路；只按单一阶段归类会掩盖任务与指标差异。
- 修订：标题改为“四个常见里程碑”，正文声明它只是粗略路线，不是公认且互斥的正式分级。
- 位置：第 97–106 行附近。标题文字发生变化，但该标题在当前范围内没有被本地链接引用；未改其他导航文件。

#### 发现 4：把一种较强尺度证据写成“错误校正演示”的定义

- 原问题：“逻辑量子比特随码距或资源增加而比物理量子比特更可靠”混合了三件事：做过纠错操作、观察到随尺度抑错、跨过相对某个物理基线的 break-even。
- 修订：先用编码、综合征提取、检测/校正说明纠错演示的对象，再区分“随码距增加而下降”的尺度证据和需要明确寿命、门或每周期错误率口径的 break-even。
- 位置：第 103 行附近。

### 3.2 第 01 章：数学对象与可手算判据

#### 发现 5：归一化之后直接进入基展开，缺少全局相位等价

- 原问题：后文频繁“忽略全局相位”，但第 01 章没有先证明为什么能忽略。初学者容易把全局相位与相对相位一并删掉。
- 修订：新增短节，对任意实数 $\gamma$ 逐步计算

  $$
  (e^{-i\gamma}\langle\psi|)P(e^{i\gamma}|\psi\rangle)
  =\langle\psi|P|\psi\rangle,
  $$

  并用 $|+\rangle$ 与 $i|+\rangle$、$|+\rangle$ 与 $|-\rangle$ 对照全局和相对相位。
- 位置：第 60–72 行附近。

#### 发现 6：正半定表项对初学者过度压缩

- 原问题：只写 $\langle v|A|v\rangle\ge0$，没有解释不等号比较实数，也没有给出厄米性和本征值判据；初学者还可能误以为“对角元非负”就够了。
- 修订：定义中显式加入 $A=A^\dagger$；补充有限维等价判据及两个 $2\times2$ 例子：

  $$
  \begin{bmatrix}1&i\\-i&1\end{bmatrix}
  \quad\text{的本征值为 }0,2,
  $$

  而 $\bigl[\begin{smallmatrix}1&2\\2&1\end{smallmatrix}\bigr]$ 虽对角元为正，本征值却为 $3,-1$。
- 位置：第 99–112 行附近。

### 3.3 第 13 章：从信息量数值到操作任务

#### 发现 7：“0.469 ebit”可能被当成单份可切分对象

- 原问题：只给单位和数值，没有告诉读者分数 ebit 的资源含义。
- 修订：明确它是多副本 LOCC 下的渐近率；$n$ 份该纯态约可浓缩为 $0.469n$ 个 Bell 对，而不是单份确定地产生“0.469 个 Bell 对”。
- 位置：第 150–152 行附近。

#### 发现 8：“非正交态不能无误区分”缺少判别规则的条件

- 原问题：若不说明“每轮必须二选一”，读者会误以为无歧义判别也被排除。
- 修订：区分确定性二选一与允许“不确定”结果的无歧义判别；对等先验 $|0\rangle,|+\rangle$ 给出

  $$
  p_{\rm USD}=1-|\langle0|+\rangle|
  =1-\frac1{\sqrt2}\approx0.2929.
  $$
- 位置：第 219 行附近。

#### 发现 9：Holevo 例只算上界，没有展示它可能不可达

- 原问题：读者可能把 $\chi\approx0.601$ bit 当成一定能由某次测量提取的信息。
- 修订：对等先验 $|0\rangle,|+\rangle$ 继续计算。该对称二元纯态例中，最小错误测量也最大化互信息，错误率

  $$
  p_e=\frac12\left(1-\frac1{\sqrt2}\right)
  \approx0.1464466094,
  $$

  因此

  $$
  h_2(p_e)\approx0.6008760367,
  \qquad
  I_{\rm acc}=1-h_2(p_e)\approx0.3991239633\text{ bit}.
  $$

  这严格小于 $\chi\approx0.601$ bit。正文同时提醒：最小错误率和最大互信息一般是不同优化目标，本例测量相同来自其对称二元纯态结构。
- 位置：第 332–344 行附近。

#### 文字清理

- `00-overview.md` 的“完整闭环”改为“一次完整过程”。
- `13-quantum-information.md` 的“通信资源账本”改为“通信所需资源”。

## 4. 独立计算与结构核验

### 数值复算

- $h_2(0.1)=0.4689955936$，与 $0.469$ ebit 一致。
- $1-1/\sqrt2=0.2928932188$，与无歧义判别成功率一致。
- $p_e=(1-1/\sqrt2)/2=0.1464466094$。
- $h_2(p_e)=0.6008760367$，故 $1-h_2(p_e)=0.3991239633$ bit。
- 正半定例的特征多项式为 $(1-\lambda)^2-1=\lambda(\lambda-2)$，本征值 $0,2$；反例的本征值为 $3,-1$。

### 静态核验

- 三章显示公式分隔符均为偶数：第 00 章 8 个，第 01 章 46 个，第 13 章 72 个。
- 未新增自检题，因此现有题答条数与锚点不受影响。
- 没有修改已有公式编号、图片路径或附录链接。
- 搜索确认旧措辞“完整计算包含四层”“对大量日常任务没有优势”“通信资源账本”已不再出现。

## 5. 未完成项与边界

- 本轮没有改共享练习答案；新增内容没有改变现有六道第 01 章或六道第 13 章自检题的答案。
- 本轮没有扩展连续变量、信道容量或混态纠缠量；这些主题已有第 18 章承接，不为追求篇幅在基础章重复。
- Mermaid 图本身未修改，只修正了与其节点数不一致的正文。
- 未发现需要留给后续轮次的 P0/P1 问题；新增段落仍应由另一审稿人做只读交叉复算。

