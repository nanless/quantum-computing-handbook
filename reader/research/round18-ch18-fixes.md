# 第 18 轮修订：第 18 章修复记录

## 1. 完成情况

本轮根据 `work/research/round17-cross-ch18-pedagogy-audit.md` 修复了全部 1 项 P1 与 7 项 P2。修改范围严格限制为：

- `handbook/18-channels-capacities-complexity.md`；
- `handbook/05-noise-channels.md`；
- `handbook/13-quantum-information.md`；
- `handbook/appendices/exercises.md` 的第 18 章答案；
- `handbook/appendices/notation.md`；
- `handbook/appendices/glossary.md`；
- `handbook/appendices/references.md`。

没有修改第 17、19 章或 `audit-log.md`。

## 2. P1 修复

### 量子指纹双侧码距条件

正文不再从“最小相对距离至少为 $\delta$”错误推出重叠绝对值上界，而是定义

$$
\Delta_{xy}=\frac1m d_H(E(x),E(y)),
\qquad
\delta\le\Delta_{xy}\le1-\delta.
$$

随后逐步推出

$$
\langle\phi_x|\phi_y\rangle=1-2\Delta_{xy},
$$

以及

$$
|\langle\phi_x|\phi_y\rangle|
=|1-2\Delta_{xy}|le1-2\delta.
$$

自检第 9 题同步改为任意两个不同码字的相对 Hamming 距离都在 $[1/4,3/4]$；答案也先从 $\Delta_{xy}$ 推出绝对值上界，再计算 swap test。这样保留原有的

$$
p_{\rm same}\le\frac58,
\qquad
\left(\frac58\right)^{10}\approx0.00909495,
$$

同时使结论真正由题设推出。

## 3. 七项 P2 修复

1. **Uhlmann 共同辅助空间**：增加

   $$
   \dim R\ge\max\{\operatorname{rank}(\rho),\operatorname{rank}(\sigma)\},
   $$

   并说明先把固定的 $\rho$ 纯化嵌入共同参考空间，再优化 $\sigma$ 的纯化。

2. **Stein 精确指数式**：显式定义 $\beta_n^*(\epsilon)$，把模糊的 $\beta_n\approx2^{-nD}$ 改为

   $$
   \lim_{n\to\infty}-\frac1n\log_2\beta_n^*(\epsilon)
   =D(\rho\|\sigma),
   $$

   并给出等价的 $2^{-nD+o(n)}$ 写法。答案 4 同步注明这是以 2 为底的每副本错误指数。

3. **擦除信道最优性桥梁**：经典容量段分别给出正交编码的可达率和未擦除分支的维数上界；纠缠辅助容量对任意输入推导

   $$
   I(R:B)=2(1-\varepsilon)S(\rho)
   \le2(1-\varepsilon),
   $$

   再说明最大混合输入取等。量子容量段明确指出可降解性给出 $\varepsilon\le1/2$ 的单字母最优性，反降解性给出另一半区间的零容量。

4. **私密容量资源口径**：容量表改为“无额外辅助信道”；正文区分无辅助私密经典通信、允许前向公共通信但不增益的密钥生成模型，以及反向/双向辅助容量。

5. **连续变量边界**：统一 $\hat q,\hat p,\hat R$ 帽号；注明压缩轴与 $r>0$；把 Gaussian 高效模拟的条件展开为有效描述、多项式模式数与步骤数、多项式数值精度，并排除无限能量或指数精度形式输入。

6. **初学者术语与符号入口**：首次出现时写出态系综、独立同分布、状态制备与测量误差、有限次采样；正文补互补、可降解和反降解信道的一句话定义。符号表新增 $|\Omega\rangle,J_{\mathcal E},D,D_H^\epsilon,I_c,C/Q/P/C_E,\mathcal N(\rho),\hat q,\hat p,V$。术语表新增纯化、Choi、相干信息、互补信道、负性、信道容量、QCMA/QMA、QIP、通信复杂度和 Gaussian 态。

7. **引用与元数据**：第 18 章加入 Peres、Horodecki 三人组、Vidal–Werner 的原始来源；补全 Bennett–Shor–Smolin–Thapliyal 的期刊卷页、年份和 DOI；QIP = PSPACE 改用已核对的 JACM DOI。精选参考页增加擦除信道、纠缠辅助容量、量子指纹、QIP、负性和 Gaussian 信息入口，并把 Watrous 教材范围扩展到第 8 章。

## 4. 第 05、13 章回链

- 第 05 章回链补充说明第 18 章采用未归一化最大纠缠向量定义 Choi 矩阵，防止与归一化 Choi 态混用。
- 第 13 章三处回链分别补充：两 qubit PPT 与高维局限、Stein 的严格渐近指数、擦除容量的免费资源和“可达率 + 上界”证明结构。

## 5. 十题复算

| 题号 | 检查结果 |
|---:|---|
| 1 | 纯化展开后，两个交叉项偏迹为零，约化态为 $\operatorname{diag}(0.8,0.2)$ |
| 2 | $J_{\mathcal R}=I\otimes|0\rangle\langle0|=\operatorname{diag}(1,0,1,0)$；谱非负且 $\operatorname{Tr}_B J=I$ |
| 3 | $\tau_{\mathcal E}=J_{\mathcal E}/d$；总迹为 1，输出偏迹为 $I/d$ |
| 4 | $D=0.27807190511263774$ bit；迹距离 $0.3$；Helstrom 成功率 $0.65$ |
| 5 | $\varepsilon=1/4$ 时 $(C,Q,P,C_E)=(0.75,0.50,0.50,1.50)$ |
| 6 | 部分转置谱 $(-0.2,0.4,0.4,0.4)$，负性 $0.2$ |
| 7 | QCMA/QMA 的量词相同，见证分别为经典串与量子态，验证者均为量子多项式时间 |
| 8 | QIP 多出计算不受限的证明者，故 $\mathrm{QIP}=\mathrm{PSPACE}$ 不推出 $\mathrm{BQP}=\mathrm{PSPACE}$ |
| 9 | 双侧码距给 $|\langle\phi_x|\phi_y\rangle|\le1/2$；单次误报 $5/8$；十次全通过为 $0.009094947017729282$ |
| 10 | $r=(\ln2)/2$ 时方差为 $1/4,1$，乘积 $1/4$，饱和不确定性下界 |

第 18 章自检编号为 1–10，答案编号也为 1–10，逐题对应。

## 6. 静态检查

- 本轮涉及的七个 handbook 文件，`$$` 数量均为偶数；
- Markdown 代码围栏均闭合；
- 本地 Markdown 链接目标均存在；
- 第 18 章答案锚点有效；
- 未发现新的公式、编号或链接问题。
