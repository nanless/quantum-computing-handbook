# 第 44 轮：量子指纹随机码存在性补证

本轮只修 `handbook/18-channels-capacities-complexity.md` 第 7.1 节的随机码存在性段，未编辑其他正文或 `sources/`。

上一版给出“固定一对坏码字的概率至多 `2e^(−m/8)`”及“输入对少于 `2^(2n−1)`”，但没有把二者明确相乘，也没有解释这些坏事件不必独立。本轮补出并合界：

$$
\Pr(\exists\text{ 距离越界的输入对})
<2^{2n-1}\cdot2e^{-m/8}
=2^{2n}e^{-m/8}.
$$

当 `m>16n ln2` 时，指数写成 `2n ln2−m/8<0`，故上界小于 1，至少有一组选出的码字没有任何坏对。该条件只需 `m` 随 `n` 线性增长。并合界逐项相加，不需要不同输入对的事件独立；只有构造固定一对的二项距离分布时使用不同码字各位独立均匀的采样设定。文字仍区分随机存在性和实际高效编码。

独立检查：若 `n=10`，充分条件是 `m>16×10×ln2≈110.90`，取整数 `m=111` 即使右侧严格小于 1。这个数是保守存在性常数，不是最优码长或实现建议。

一手来源：[Buhrman、Cleve、Watrous、de Wolf，《Quantum Fingerprinting》](https://arxiv.org/abs/quant-ph/0102001)；[作者论文 PDF](https://jhwatrous.github.io/BuhrmanCleveWatrousdeWolf2001.pdf)中的双侧距离随机码论证。本轮只补完整概率算术，没有改变指纹态、swap test 或通信模型定义。
