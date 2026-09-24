# 第 16 轮实施记录：信道、信息与复杂度桥梁

日期：2026-09-22

## 1. 实施结论

本轮新建 `handbook/18-channels-capacities-complexity.md`，并只在第 05、13 章加入简短先导与回链。第 15 轮列出的 3 项 P1 与 5 项 P2 已全部进入新章主线；一次性信息论、Petz 恢复、高级复杂度体系、容量超激活与完整 Gaussian 信息论仍保持为延伸边界，没有挤入初学者主线。

新章包括 4 幅 Mermaid 图、3 张比较表、8 个以上逐步推导或数值算例，以及 10 道自检题。完整答案草稿位于 `work/research/round16-ch18-answer-draft.md`。

## 2. 文件改动

### `handbook/18-channels-capacities-complexity.md`（新建）

按“表示工具 → 操作任务 → 复杂度模型 → 连续变量入口”的顺序组织：

1. **纯化与 Uhlmann 定理**
   - 从谱分解构造标准纯化；
   - 逐项偏迹 $\sqrt{0.8}|00\rangle+\sqrt{0.2}|11\rangle$；
   - 说明辅助系统最小维数、纯化非唯一性和等距变换；
   - 明确本书采用根保真度，Uhlmann 公式右侧不平方。
2. **Choi–Jamiołkowski 对应**
   - 先固定未归一化 $|\Omega\rangle$；
   - 给出重构公式、CP 判据和 TP 偏迹条件；
   - 用 qubit 复位信道算出 $\operatorname{diag}(1,0,1,0)$；
   - 对照归一化 Choi 态，防止差一个输入维数；
   - 用表格区分 Kraus、Stinespring、Choi 与 Pauli transfer matrix。
3. **Stein 非对称假设检验**
   - 分开定义第一类错误 $\alpha$ 与第二类错误 $\beta$；
   - 写出 $D_H^\epsilon$ 和 i.i.d. Stein 极限；
   - 算出对角态相对熵 $0.278071905$ bit，并与单副本 Helstrom 任务分离。
4. **四种信道容量**
   - 区分 $C,Q,P,C_E$ 的对象、免费资源和单位；
   - 解释渐近块长、联合编码与正则化；
   - 给出 Holevo 量、相干信息、私密信息差和纠缠辅助互信息公式；
   - 完整计算 qubit 擦除信道：

     $$
     C=1-\varepsilon,
     \quad Q=P=\max\{0,1-2\varepsilon\},
     \quad C_E=2(1-\varepsilon).
     $$

     对 $\varepsilon=1/4$，结果为 $0.75,0.50,0.50,1.50$，并明确 $P=Q$ 只是擦除信道的特殊性质。
   - 加入固定资源账本下的信道级数据处理说明。
5. **混态纠缠与资源理论**
   - 先声明免费态、LOCC 与资源单调性；
   - 区分形成成本、可蒸馏纠缠和负性；
   - 对加白噪声 Bell 态逐步求部分转置谱：

     $$
     \mathcal N(\rho_p)=\max\{0,(3p-1)/4\}.
     $$

   - 明确两 qubit 的 PPT 充要性不能无条件推广到高维。
6. **QCMA、QMA 与 QIP**
   - 写出 yes 实例“存在见证”和 no 实例“对所有见证”的量词；
   - 固定 $c-s\ge1/\operatorname{poly}(|x|)$；
   - 解释 QCMA/QMA 的验证者相同、见证类型不同；
   - 用接受算子 $M=|+\rangle\langle+|$ 给出 $1$ 与 $1/2$ 的小算例；
   - 以时序图解释 QIP，并把 $\mathrm{QIP}=\mathrm{PSPACE}$ 与 BQP 算法能力分开。
7. **通信复杂度与量子指纹**
   - 先固定单向/交互/同时消息、随机性、纠缠和错误模型；
   - 从经典纠错码推导指纹内积与 swap test 概率；
   - 对 $\delta=1/4$ 得一次误报上界 $5/8$，10 次独立重复得约 $0.00909495$；
   - 将指数优势限定在无共享随机性的同时消息模型。
8. **连续变量最小入口**
   - 固定 $[q,p]=i$ 与真空方差 $1/2$；
   - 定义一阶矩、协方差矩阵、Gaussian 操作和同相/外差探测；
   - 对 $r=(\ln2)/2$ 算出方差 $1/4$ 与 $1$；
   - 明确 Gaussian 可模拟结论的条件、非 Gaussian 资源、能量约束及有限压缩 GKP 边界。

### `handbook/05-noise-channels.md`

在由系统—环境演化推出 Kraus 表示后加入一段短回链，说明第 18 章将补纯化、Choi 和多种信道容量；不重复展开定义。

### `handbook/13-quantum-information.md`

加入三处短回链：

- 纯态纠缠熵之后，指向混态资源理论和负性；
- 相对熵之后，指向 Stein 假设检验；
- Holevo 算例之后，指向四种容量与擦除信道。

### `work/research/round16-ch18-answer-draft.md`（新建）

给出 10 道题的完整答案，包括每步偏迹、Choi CP/TP 检查、归一化转换、Helstrom 对照、四种擦除容量、负性、复杂度量词、QIP 模型、量子指纹重复误差与压缩态方差。

## 3. 第 15 轮缺口映射

| 第 15 轮项目 | 本轮落点 | 状态 |
|---|---|---|
| P1-1 纯化/Uhlmann | 第 18 章 §1 | 已落实 |
| P1-2 Choi–Jamiołkowski | 第 18 章 §2 | 已落实 |
| P1-3 信道容量 | 第 18 章 §4 | 已落实，并补齐私密容量 |
| P2-1 Stein 假设检验 | 第 18 章 §3 | 已落实 |
| P2-2 混态纠缠资源 | 第 18 章 §5 | 已落实 |
| P2-3 QCMA/QMA | 第 18 章 §6.1–6.2 | 已落实 |
| P2-4 通信复杂度 | 第 18 章 §7 | 已落实 |
| P2-5 QIP/验证与 CV 入口 | 第 18 章 §6.3、§8 | 已落实 |

## 4. 复算与静态检查

### 数值复算

- $0.8\log_2(1.6)+0.2\log_2(0.4)=0.27807190511263774$；
- $(5/8)^{10}=0.009094947017729282$；
- $p=0.6$ 时部分转置负本征值 $(1-3p)/4=-0.2$，负性为 $0.2$；
- $\varepsilon=1/4$ 时 $C=0.75,Q=0.50,P=0.50,C_E=1.50$；
- $r=(\ln2)/2$ 时 $e^{-2r}=1/2,e^{2r}=2$，方差乘积为 $1/4$。

### 结构检查

- 第 18 章有 4 个 Mermaid 代码块、3 张 Markdown 表、10 道自检题；
- 第 18 章与答案稿的 `$$` 定界符数量均为偶数；全部代码围栏成对；
- 第 05、13 章新增的 `18-channels-capacities-complexity.md` 相对链接均可解析；
- 未修改 `sources/`、README、练习附录、符号表、术语表、参考文献总表或审校日志。

工作目录不是 Git 仓库，因此不能运行 `git diff --check`；改以逐文件定界符、围栏与本地链接检查完成静态验收。

## 5. 权威核对来源

以下资料均于 2026-09-22 访问：

- John Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/)（作者公开教材，2018）。
- A. Uhlmann, [The “transition probability” in the state space of a $*$-algebra](https://doi.org/10.1016/0034-4877(76)90060-4)（1976）。
- A. Jamiołkowski, [Linear transformations which preserve trace and positive semidefiniteness of operators](https://doi.org/10.1016/0034-4877(72)90011-0)（1972）。
- M.-D. Choi, [Completely positive linear maps on complex matrices](https://doi.org/10.1016/0024-3795(75)90075-0)（1975）。
- I. Devetak, [The private classical capacity and quantum capacity of a quantum channel](https://doi.org/10.1109/TIT.2004.839515)（2005）。
- C. H. Bennett, D. P. DiVincenzo, J. A. Smolin, [Capacities of Quantum Erasure Channels](https://doi.org/10.1103/PhysRevLett.78.3217)（1997）。
- T. Ogawa, H. Nagaoka, [Strong converse and Stein's lemma in quantum hypothesis testing](https://doi.org/10.1109/18.887855)（2000）。
- E. Chitambar, G. Gour, [Quantum resource theories](https://doi.org/10.1103/RevModPhys.91.025001)（2019）。
- R. Jain et al., [QIP = PSPACE](https://arxiv.org/abs/0907.4737)（预印本 2009；JACM 2011）。
- H. Buhrman et al., [Quantum Fingerprinting](https://doi.org/10.1103/PhysRevLett.87.167902)（2001）。
- C. Weedbrook et al., [Gaussian Quantum Information](https://arxiv.org/abs/1110.3234)（预印本 2011；RMP 2012）。

## 6. 未纳入主线的内容

按第 15 轮建议，以下内容仍作为后续延伸，不在本轮证明：光滑熵与二阶渐近、Petz 恢复、容量超加性与超激活、混态纠缠量完整谱系、QMA(2)/MIP* 等高级验证类，以及 Williamson 分解和 bosonic Gaussian 信道容量。这些主题需要更多前置知识，加入本章会打断当前由可手算例驱动的教学路径。
