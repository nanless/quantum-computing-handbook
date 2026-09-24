# 第 67 轮｜第 05、18 章定点终审（只读）

范围：只读核查第 05 章 §5.4 的两种单比特退极化参数、第 18 章 §4.5 的无预共享纠缠经典擦除信道容量上界，以及第 05、18 章自检答案和第 13 章 Holevo 维数约定。不改算法组正文或共享答案。以下行号以本轮核查时文件为准。

## P0–P2 结论

- **P0：无。** 限定范围内没有符号颠倒、错误等号或容量结论错误。
- **P1：无。** 第 18 章第 511–534 行的上界确实涵盖任意跨 $n$ 次输入的联合量子编码，并不依赖“输入是 $n$ 个独立 qubit”这一额外假设。
- **P2：无待修。** 第 05 章第 286–323 行、第 18 章第 509–534 行，以及共享答案第 232、851–883 行，在本轮指定问题上自洽。唯一可选的编辑微调是第 18 章 Fano 公式处明写 $K\ge2$；正常正速率码本自动满足，故不列为缺陷。

## 第 05 章：退极化参数和边界

正文第 290–321 行取 $\mathcal D_p(\rho)=(1-p)\rho+pI/2$，$0\le p\le1$，另一约定为 $\widetilde{\mathcal D}_q(\rho)=(1-q)\rho+(q/3)\sum_{P=X,Y,Z}P\rho P$，$0\le q\le1$。令 $\rho=(I+\vec r\cdot\vec\sigma)/2$，逐一 Pauli 共轭后，$\sum_P P\rho P=(3I-\vec r\cdot\vec\sigma)/2=2I-\rho$。故第二式的 Bloch 因子是 $1-4q/3$；与第一式的 $1-p$ 比较，得到 $p=4q/3$、$q=3p/4$，正文第 305–321 行正确。

端点独立检查：$q=3/4$ 时 Bloch 因子为零，即完全混合；$q=1$ 时因子为 $-1/3$，对输入 $|0\rangle$ 输出 $\operatorname{diag}(1/3,2/3)$，不是“以合法概率 $p\le1$ 替换成 $I/2$”。因此第 323 行关于 $q>3/4$ 的区分正确；从数学上的完全正信道看，形式参数 $p=4q/3$ 可延至 $4/3$，但超出本书 $p$ 的概率解释。第 05 章自检第 6 题（第 429 行）及答案第 232 行：$p=0.20\Rightarrow q=0.15$，每个非恒等 Pauli 概率 $q/3=0.05$，正确。可核对 [Preskill 量子计算讲义第 3 章](http://theory.caltech.edu/~preskill/ph219/chap3_15.pdf)、[PennyLane 退极化信道官方文档](https://docs.pennylane.ai/en/stable/code/api/pennylane.DepolarizingChannel.html)；后者明确列 $q=3/4$ 完全退极化、$q=1$ 均匀非恒等 Pauli。[IBM Qiskit Aer 官方文档](https://eu-de.quantum.cloud.ibm.com/docs/api/qiskit/0.38/qiskit_aer.noise.depolarizing_error)也允许单 qubit 的替换式系数延至 $4/3$，与“合法信道范围可宽于概率混合解释”一致。

## 第 18 章：任意联合编码的擦除上界

正文第 490–516 行：信道每个位置独立地以概率 $\varepsilon$ 擦除，令 $S$ 为保留位置集，旗标让 Bob 知道 $S$。擦除选择与消息 $X$ 独立，所以 $I(X:S)=0$。固定任何 $S=s$ 后，不论 Alice 的 $n$-qubit 码字在输入端有多少纠缠，Bob 的非旗标部分只在 $\bigotimes_{i\in s}\mathbb C^2$ 上，维数 $2^{|s|}$；其余旗标是已知的纯态。于是条件态系综的 Holevo 量满足 $I(X:B\mid S=s)\le\log_2(2^{|s|})=|s|$。平均后

$$I(X:BS)=I(X:B\mid S)\le\sum_s\Pr(s)|s|=n(1-\varepsilon).$$

这正是正文第 514–516 行。它只要求无预共享纠缠；若双方另持共享纠缠，Bob 的条件系统不再只由接收的 $|s|$ 个 qubit 构成，不能套用此界。第 13 章第 403–433 行也明确把 $\chi\le\log_2d$ 限定在无预共享纠缠的通信模型中，跨章约定一致。[Bennett–DiVincenzo–Smolin 原论文](https://doi.org/10.1103/PhysRevLett.78.3217)给擦除信道经典容量结论；[Wilde《Quantum Information Theory》§20.4.3](https://fenix.tecnico.ulisboa.pt/downloadFile/1407993358931417/Quantum%20Information%20Theory%20%5BMark%20M.%20Wilde%5D%20%282017%29.pdf)写 $d$ 维结果 $(1-\varepsilon)\log_2d$，与此 qubit 推导吻合。

正文第 519–534 行的 Fano 桥接也正确。对 $K\ge2$ 个等概率消息，$H(X)=\log_2K$；译码测量是对 $B,S$ 的处理，故 $I(X:\widehat X)\le I(X:BS)$。Fano 给 $H(X\mid\widehat X)\le h_2(p_e)+p_e\log_2(K-1)$，所以

$$\log_2K\le n(1-\varepsilon)+h_2(p_e)+p_e\log_2(K-1)
\le n(1-\varepsilon)+h_2(p_e)+p_e\log_2K.$$

确实可移项、除 $n$ 得正文第 529–531 行 $(1-p_e)\log_2K/n\le1-\varepsilon+h_2(p_e)/n$。可靠码序列 $p_e\to0$ 且 $h_2(p_e)\le1$，便有速率上界 $1-\varepsilon$；正文第 534 行的结论成立。[Trevisan《Lecture Notes on Quantum Information Theory》§7，PDF 第 58 页](https://people.dm.unipi.it/trevisan/teaching/PhD/2022-qinfo/2022-Qinfo-notes.pdf)用同一 Fano–互信息链条证明信道容量弱逆定理。

下界第 509 行用正交态把 qubit 擦除信道化为二元经典擦除信道，经典块码可达任意小于 $1-\varepsilon$ 的速率；与上界合并得 $C=1-\varepsilon$。第 18 章自检第 5 题（第 1047 行）及答案第 851–883 行，在 $\varepsilon=1/4$ 时的 $C=0.75$ bit/use、$Q=P=0.50$、$C_E=1.50$ 数值与各自资源条件均正确；本轮对后三种容量只做跨章口径核对，未重证其容量定理。

## 未覆盖边界

主代理在本轮另补第 12 章第 162 行的 QKD 损耗换算，顺手只读复核：$100\,\mathrm{km}\times0.235\,\mathrm{dB/km}=23.5\,\mathrm{dB}$，$10^{-23.5/10}=0.0044668359\approx4.47\times10^{-3}$；论文另报的整链路 $31.5\,\mathrm{dB}$ 对应 $10^{-31.5/10}=0.0007079458\approx7.08\times10^{-4}$。两个数值、舍入和“光纤本体／整链路”的边界均正确，亦未将其误作安全密钥率。原始实验论文：[Tang 等，npj Quantum Information (2022)](https://www.nature.com/articles/s41534-022-00630-3)。

这不是第 05、18 章逐句全审，也没有重新证明 HSW 定理、所有纠缠辅助容量定理或第 18 章其他复杂度章节。本报告的“零待修”只限于指定的两段推导、自检答案、第 13 章维数约定及上述第 12 章追加换算。
