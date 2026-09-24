# 第 16 轮：计算模型与高级算法实施记录

> 日期：2026-09-22  
> 任务范围：新建第 17 章，并修改第 7、8、16 章；不修改 README、练习附录、共享附录或审校日志。

## 一、完成情况

已落实第 15 轮算法审计的 4 项 P1 与 8 项 P2 中适合当前主线的全部内容。没有改动 `handbook/00–06`、`09–15`、任何 `handbook/appendices/*`、根 README 或 `handbook/README.md`。

新增文件：

- `handbook/17-computation-models.md`
- `work/research/round16-ch17-answer-draft.md`
- `work/research/round16-models-algorithms-implementation.md`

修改文件：

- `handbook/07-algorithms.md`
- `handbook/08-applications.md`
- `handbook/16-advanced-algorithms-verification.md`

## 二、第 17 章新增内容

### 1. 计算模型地图

用 Mermaid 关系图和总表比较：

- 门线路模型；
- 测量型量子计算；
- 闭系统绝热计算；
- 量子退火；
- 模拟量子模拟器；
- 数字—模拟混合模型。

统一按“程序写在哪里、核心资源、典型输出、首要成本”比较，并明确理论可互相模拟不代表硬件成本、噪声和实用性能相同。

### 2. MBQC 最小可复算例

从

$$
CZ(|\psi\rangle|+\rangle)
=a|0\rangle|+\rangle+b|1\rangle|-\rangle
$$

逐支投影，得到输出 $X^mH|\psi\rangle$，两结果概率各为 $1/2$。补充 Pauli 伴随算符、Pauli 帧、适应性前馈和资源态边界。

### 3. 绝热模型与退火

- 对 $H(s)=-(1-s)X-sZ$ 完整求谱，得到 $\Delta_{\min}=\sqrt2$；
- 说明绝热条件还依赖路径导数、光滑性、误差定义和所用定理；
- 区分绝热—门模型多项式等价与实际退火设备；
- 给出 TTS 公式并手算 $p_s=0.2,t_a=20\ \mu\mathrm{s},99\%$ 成功置信度时需 21 次、退火段 TTS 为 $420\ \mu\mathrm{s}$；加入读出复位后例为 $2.52\ \mathrm{ms}$。

### 4. 模拟与数字—模拟混合

- 区分数字模拟算法、模拟量子模拟器和数字—模拟混合控制；
- 用 echo 序列从 $J(Z_1Z_2+Z_2Z_3)$ 中抵消 $Z_1Z_2$、保留 $Z_2Z_3$；
- 列出瞬时脉冲、时长相等、无残余不可对易项等假设；
- 给出模拟器从可算区外推的四类证据及 Mermaid 验证图。

### 5. 密码算法成本案例

新增因数分解/离散对数、密钥穷举、哈希原像、碰撞和 PQC 的任务分表；用 8 位密钥例说明约 13 次 Grover 查询仍需可逆加密、比较、相位标记、反计算和扩散，不等于 13 次普通加密。

### 6. 教学结构

- 共 3 个 Mermaid 图；
- 多张模型、模拟路线、密码任务和声明审查表；
- 8 条常见误区；
- 10 道自检；
- 独立答案草稿已写入 `work/research/round16-ch17-answer-draft.md`，未触碰共享练习附录。

## 三、第 7 章修改

### 现代 Hamiltonian 模拟方法

新增乘积公式、qDRIFT、Taylor/LCU、qubitization/QSP 与截断 Dyson 的选择表，字段统一为一步操作、主导量、适用直觉和边界。

新增 qDRIFT 手算：

$$
H=0.6X+0.8Z,
\quad \lambda=1.4,
\quad p_X=3/7,
\quad p_Z=4/7.
$$

一阶平均生成项复算为 $-itH/N$，并明确严谨分析对象是平均量子信道，不能把平均矩阵直觉写成每条随机线路的精确等式。

### 量子线性系统

新增

$$
A=\operatorname{diag}(1,2),
\quad |b\rangle=|+\rangle
$$

的二维例，得到

$$
|x\rangle=\frac{2|0\rangle+|1\rangle}{\sqrt5},
\quad \kappa=2,
\quad \langle Z\rangle=\frac35.
$$

例题直接展示“估计 observable”与“打印全部带符号分量”的差别，并补解态验证受 $\kappa$ 影响的边界。

### Local Hamiltonian 与 QMA

正式定义 $k$-local Hamiltonian 判定问题、YES/NO 阈值与逆多项式承诺间隙；区分承诺间隙 $b-a$ 和物理谱隙 $E_1-E_0$。二比特 1-local 例的能量为 $0,1,1,2$，在 $a=1/4,b=3/4$ 时为 YES；承诺间隙 $1/2$，物理谱隙 1。

## 四、第 8 章修改

### 非平凡 QAOA 小例

在单边 MaxCut 后追加三顶点路径。对 $\beta=\pi/8,\gamma=\pi/3$，复算得

$$
\langle C_{12}+C_{23}\rangle
=1+\frac{3\sqrt3}{8}
\approx1.64952<2.
$$

由此展示度数和局部邻域已经进入 $p=1$ 期望式，避免把单边满分角度外推到一般图。

### QML 数据访问摊销

新增

$$
R>\frac{T_{\rm build}}{T_C-T_Q}
$$

的摊销条件。对 $T_{\rm build}=10^6,T_Q=10^3,T_C=10^5$，需至少 11 次复用；若每 5 次重建则不回本。明确数字是成本口径练习，不代表具体硬件。

## 五、第 16 章修改

### QSP 信号序列

在现有矩阵多项式例后新增

$$
W(x)=
\begin{pmatrix}
x&i\sqrt{1-x^2}\\
i\sqrt{1-x^2}&x
\end{pmatrix},
$$

直接平方得到左上元 $2x^2-1=T_2(x)$。说明查询次数、次数、奇偶性、有界性和相位约定的关系。

### 委托验证信任模型

把此前一行“陷阱/交互/密码学验证”展开为五类：直接复核、有限量子客户端陷阱式 MBQC、多证明者 rigidity、基于 LWE 的单证明者经典验证、统计基准。加入隐藏陷阱位置的 $1/(m+1)$ 检测概率直觉，并明确这不是完整安全证明。

### 跨尺度验证

新增小尺寸/短时间经典对照、守恒量与极限、跨平台/算法交叉、规模与校准稳定性四支柱图。对理论值 1 与三组估计计算出 $1.25\sigma,3.5\sigma,6\sigma$ 偏差，说明既不能忽略系统趋势，也不能仅凭三点断言偏差来源。

## 六、复算与静态检查

已完成以下独立复算：

1. MBQC 两个投影分支范数均为 $1/2$，输出统一为 $X^mH|\psi\rangle$。
2. 绝热二能级本征值为 $\pm\sqrt{s^2+(1-s)^2}$，最小谱隙为 $\sqrt2$。
3. TTS 中 $\lceil\log0.01/\log0.8\rceil=21$。
4. echo 中两项对易，$Z_1Z_2$ 抵消，$Z_2Z_3$ 总相位为 $Jt$。
5. qDRIFT 概率和为 1，平均一阶生成元为 $H$。
6. QLSA 解态平方范数为 1，$\langle Z\rangle=3/5$。
7. 三顶点 QAOA 逐振幅数值复算为 $1.6495190528$，与解析式一致。
8. QSP 的 $W(x)$ 为酉矩阵，$W(x)^2$ 左上元为 $T_2(x)$。
9. 四个修改正文的 `$$` 数量均为偶数；所有代码围栏数量均为偶数。
10. 修改文件中的本地 Markdown 链接目标存在。

## 七、取舍与残余工作

- 没有把 Feynman–Kitaev history state、stoquastic Hamiltonian、量子 PCP 或高次 QSP 相位综合塞入主线。这些属于第 15 轮“扩展”，会明显增加前置知识。
- 没有改第 12 章密码段和第 14 章控制段；所需密码任务表与 echo 已集中放入第 17 章，以遵守本轮文件边界。
- 没有修改 README、练习附录或审校日志。后续整合者需把第 17 章加入目录，将答案草稿并入共享练习，并补相应审校记录。
