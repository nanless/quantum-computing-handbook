# 第 62 轮交换审：导论、多比特与量子力学基础

日期：2026-09-24。只读审查 `work/research/round61-foundations-review.md` 所列修订，并抽查其余已报无改章节。没有修改受审正文、共享练习答案或 `reader/`。

## 发现：第 03 章纠缠见证的“未检出”解释需要补一个符号反例（P2）

位置：`handbook/03-multiple-qubits.md` 第 378–406 行，尤其第 406 行。新增证明本身正确：对任意乘积态，$C_X+C_Z=x_Ax_B+z_Az_B\le1$；可分混态按凸组合也满足这个上界。$q=0.8$ 的 Bell 白噪声混态给 $C_X=C_Z=0.8$、和为 1.6、两组各 $450,450,50,50$ 的**期望**计数，也均正确。

问题在界后的解释：“有些纠缠态的相关方向不在此处选的 $X,Z$ 两轴上”，会令读者以为本见证漏检都因为要换测量轴。一个更近、更可手算的反例是同章已经介绍的 $|\Phi^-\rangle=(|00\rangle-|11\rangle)/\sqrt2$。它仍沿同一 $X,Z$ 两轴有完美相关，但 $C_Z=+1,C_X=-1$，故 $C_X+C_Z=0$，未触发本章专为 $|\Phi^+\rangle$ 取向写的“正号”见证。原始论文 [Audenaert–Plenio, Eq. (26)](https://arxiv.org/pdf/quant-ph/0608067) 甚至给出在只知道两组相关值时的更一般条件 $|C_X|+|C_Z|>1$。建议：保留易教的正号证明，紧接着加 $\Phi^-$ 的两行反例；或先说明可在固定局域重标号后按观测符号采用绝对值版本。不要把“正号和不超界”与“不在两个轴上”当作唯一解释。

## 较低优先级措辞建议：transmon 比值需同样约束电荷色散的比较口径（P3）

位置：`handbook/quantum-mechanics/03-levels-control.md` 第 164–174 行。新增绝对非谐性 $\alpha\approx-E_C/\hbar$、相对非谐性 $|\alpha|/\omega_{01}\approx\sqrt{E_C/(8E_J)}$ 及“固定 $E_C$ / 固定 $\omega_{01}$”的区分准确，且比旧句严谨。第 164 行仍说“增大这个比值会指数地压低电荷色散”。[Koch 等原文 Eq. (2.5)](https://schusterlab.stanford.edu/static/pdfs/Koch2007.pdf) 的绝对电荷色散还含 $E_C$ 及比值的代数前因子；指数抑制严格说是随 $E_J/E_C$ 增长的**主导依赖**，尤其是固定 $E_C$ 或以 $E_C$ 归一时。若一边任意改变 $E_C$ 的绝对尺度，只给比值不能唯一推出 MHz 单位的绝对色散。建议将该句改成“在固定 $E_C$ 或比较归一化色散时，随 $E_J/E_C$ 增大受到指数主导的抑制”。这与本段对绝对/相对非谐性的谨慎口径一致，不影响主要结论。

## 核查通过的重点

- `handbook/00-overview.md` 第 135–146 行：$H|0\rangle$ 测得均匀结果是理想模型的单轮概率；`010101…` 说明边际频率对半不等于不可预测。[NIST SP 800-90B](https://csrc.nist.gov/pubs/sp/800/90/b/final) 确实覆盖熵源、最小熵、健康测试与调理；官方摘要也说明它须与 SP 800-90A/C 的其他部件组合，正文没有误称一次频数检验为整机安全认证。
- `handbook/03-multiple-qubits.md` 第 457–475 行：$P_\pm^2=P_\pm$，读数算符 $A=P_+-P_-$ 满足 $A^2=I$；$\mathcal B^2=4I-[A_0,A_1]\otimes[B_0,B_1]$ 的符号与范数上界检查正确。$|\Phi^+\rangle$ 的四项 CHSH 相关值也和 $2\sqrt2$ 一致。
- `handbook/quantum-mechanics/03-levels-control.md` 第 158–196 行：在 $E_J/E_C\gg1$ 条件下，$\hbar\omega_{01}\approx\sqrt{8E_JE_C}-E_C$、$\hbar\alpha\approx-E_C$，以及固定 $E_C$ 时绝对间隔在该阶近似中不变，均与 Koch 原始推导相符。教学脉冲的 $20\,\mathrm{ns}\to50\,\mathrm{MHz}$、$5\,\mathrm{ns}\to200\,\mathrm{MHz}$ 量级换算也正确。
- 抽查无改章节：`01-math.md` 的复数内积与 Cauchy–Schwarz 展开、二项频率方差都明确写出独立同分布前提；`02-single-qubit.md` 的相同 POVM/不同测后态算例正确；`04-circuits-protocols.md` 的传态四分支及 Bob 无消息时 $I/2$ 正确；Q1 的记录重叠 $\gamma=\langle d_1|d_0\rangle$ 对应非对角元和可见度 $|\gamma|$；Q2 的 Robertson 交换子符号正确；Q4 的有限势垒边界匹配、$E=V_0/2$ 时 $1/\cosh^2(\kappa L)$ 以及厚势垒近似一致。抽查未发现需立即修改的高优先级错误。

## 边界

本次报告是独立抽查与定点核验，不是对各篇每句话的形式化证明。主要需改的是第 03 章未检出原因的教学解释；第 Q3 条是提高参数口径一致性的建议。受审组可自行修正文句并同步其审稿报告；本组没有越界代改。
