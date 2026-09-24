# 第七轮实施记录：理论、算法与验证

日期：2026-09-22

## 1. 完成范围

本轮直接修改：

- `handbook/06-algorithmic-primitives.md`
- `handbook/07-algorithms.md`
- `handbook/08-applications.md`
- `handbook/10-error-correction.md`
- 新建 `handbook/16-advanced-algorithms-verification.md`

按协调要求，没有直接修改 `handbook/appendices/exercises.md`。新增题目的可合并答案另写入：

- `work/research/round7-exercise-answers-6-8-10-16.md`

未修改第 00–05、09、11–15 章和 `sources/`。

## 2. 各章改动

### 第 06 章

- 新增“查询下界”主线：多项式方法、hybrid/adversary 直觉、promise/total function 边界。
- 用 Deutsch XOR 的二次多项式做可手算例，解释 $T$ 次查询的接受概率次数至多 $2T$。
- 给出 Grover $\Omega(\sqrt N)$ 下界的几何直觉，并明确它只约束所声明 oracle 模型。
- 新增两道自检与 Beals、Bennett 等原始来源。

### 第 07 章

- 在 Simon 与 Shor 之间补出 hidden subgroup 的概念桥梁。
- 给出连分数恢复 $|y/Q-k/r|<1/(2r^2)$ 的充分条件，并强调只能恢复既约分数。
- 把 $H=X+Z$ 的 Trotter 例扩成交换子范数误差界和 $t=0.2,r=4$ 数值预算。
- 增加 Hamiltonian 的局域、稀疏 oracle、LCU、block encoding 四种输入模型及 no-fast-forwarding 边界。
- 将幅度估计扩成完整二维推导：Grover 本征相位、BHMT 误差界、$a=1/2$ 两位 QPE 手算、方法对照表。
- 扩充复杂度关系，加入 $\mathrm{PostBQP}=\mathrm{PP}$、$\mathrm{QIP}=\mathrm{PSPACE}$ 的模型限定和 BQP/QMA complete problem 例子。
- 新增四道自检与 AE、模拟、复杂度来源。

### 第 08 章

- 为 QML 增加四类数据访问模型表。
- 加入 Tang 反量子化所说明的“公平访问”边界。
- 明确区分难模拟、难估计和难学习。
- 加入量子核集中与 $O(1/\delta^2)$ shots 的数值例。
- 新增两道自检和四项 QML 原始/同行评审来源。

### 第 10 章

- 在 T 门与魔法态部分补入任意 $R_z$ 旋转综合。
- 给出 Ross–Selinger 模型下典型主项 $3\log_2(1/\epsilon)$ 及 $\epsilon=10^{-10}$ 的百 T 门量级手算。
- 强调模型依赖、T depth、工厂吞吐和精度分配。
- 新增一道自检与原始来源。

### 第 16 章

新章以五条相互衔接的主线组织，而不是罗列术语：

1. 六问算法审计卡；
2. 查询下界：oracle、多项式方法、hybrid/adversary、promise；
3. HSP：陪集态、Abelian Fourier sampling、Simon/Shor、非 Abelian 查询/时间分离；
4. 量子行走：四环 coined walk 手算、MNRS 型成本、element distinctness；
5. 现代模拟栈：LCU 的 PREPARE/SELECT 推导、block encoding 定义与归一化、qubitization 相位映射、QSP/QSVT 关系图和矩阵多项式例；
6. 算法级精度与失败概率预算、从 oracle 展开到容错资源；
7. 输出类型导向的验证、tomography、classical shadows、直接保真度估计、能隙—保真度界与验证梯子。

新章包含 10 道自检题和对应答案草稿。

## 3. 关键复算

- Deutsch XOR：$z_0+z_1-2z_0z_1$ 在四个 Boolean 输入上为 `0,1,1,0`。
- Trotter：$[X,Z]=-2iY$，故 $\|[X,Z]\|=2$；$t=0.2,r=4$ 的一阶界为 $0.01$；界不超过 $0.002$ 需 $r\ge20$。
- AE：$a=1/2\Rightarrow\theta=\pi/4$，两支归一化相位为 $1/4,3/4$，均映回 $1/2$。
- LCU：$0.6X+0.8Z$ 的权重为 $3/7,4/7$，左上块确为 $H/1.4$。
- QSP 小例：$A=\operatorname{diag}(1,0)$，$T_2(A)=2A^2-I=\operatorname{diag}(1,-1)$。
- 四环 walk：二步态归一化，四个带 coin 标签的振幅绝对值均为 $1/2$。
- classical shadow：随机 Pauli 测量下 $\hat Z$ 以概率 $1/3$ 为 3、其余为 0，均值 1、方差 2。
- 能隙界：由 $E\ge E_0+(1-F_0)\Delta$ 得 $F_0\ge1-(E-E_0)/\Delta$。
- 旋转综合：从 $10^{-6}$ 收紧到 $10^{-12}$，T count 主项增加 $3\log_2(10^6)\approx59.8$。

## 4. 取舍

- 没有把完整 adversary SDP、QSP 相位求解算法、非 Abelian 群表示论或 tomography 最优常数放进正文；这些会压垮入门研究生衔接章。正文保留可复算骨架、适用条件和原始来源。
- 第 06–08、10 章只放读懂本章结论所需的桥梁；LCU/QSVT、量子行走和验证的重内容集中到第 16 章，避免重复。
- 没有扩写第六轮 C 级历史资源估算案例；第 11 章已有资源估算框架，本轮优先完成 A/B 级理论链。
- classical shadows 明确保留 shadow norm，避免“样本只依赖 $\log M$”的误导；tomography 只给一般满秩态的尺度与假设，不写脱离误差度量的单一公式。
- QSP/QSVT 的表述限定在 Hermitian/奇异值变换语境，并注明奇偶性、有界性、谱区间与编码成本，没有使用“任意矩阵函数”一类过强表述。

## 5. 残余整合工作

- 需要由不与他人冲突的整合者把 `round7-exercise-answers-6-8-10-16.md` 合并进附录练习答案。
- 全书目录/阅读路线若要展示第 16 章，需要在统一整合轮更新 README；本轮未动 README，以遵守限定范围并避免冲突。
- 新增术语如 block encoding、qubitization、shadow norm 可在最终统一术语审查时加入 glossary/notation；本轮未改附录。
