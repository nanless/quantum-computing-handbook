# 第 55 轮：量子力学 Q1 初学者路线审查

范围：`handbook/quantum-mechanics/01-experiments-states.md`。本文已有正规化、Mach–Zehnder、路径记录、Stern–Gerlach 与叠加/混合的多组准确算例，来源也列出 MIT 课程、Born、Gerlach–Stern、Englert。此次重点不是推倒重写，而是检查已忘记数学的读者能否从 Q1 首次进入实验语言。

## 待修点

1. P1：开头仅写“先修第 01 章”，却在 §2.2 提前用密度矩阵、环境记录态、偏迹和复数重叠因子。读者尚未读第 03/05 章，容易误以为这些是理解无路径记录与完整路径记录差异的必要条件。应把 §2.2 明确分为先读的概率层、后读的矩阵层，章首给跳读路径。
2. P2：§2.2 先列四条密度矩阵规则再给 A/B/C 情形，正好反过来。先用一组具体 100 次理想计数说明“无记录可以全走一端、有完全可区分记录各半”；再给环境重叠参数解释部分可区分情况，可把抽象符号与经验问题连接。
3. P2：部分可区分情形给 `γ=0.6` 后直接报 0.8/0.2，最好列一个乘入公式的中间等式，并写明这不是“不看记录”本身造成的退相干。
4. P2：Stern–Gerlach 的数量表在 $N$ 符号下正确，但每一道筛选后的分母变化可用 8000 个原子复算一次，与自检第 4 题衔接。
5. P2：第 5 节两张表讲叠加与混合，但 `p(x+)=1/2` 的混合分支只口述。宜写出全概率加权式 `1/2×1/2+1/2×1/2=1/2`，并与纯态 `p=1` 并排。

公式核对：$P_0=(1+\operatorname{Re}(\gamma e^{-i\phi}))/2$、$\mathcal V=|\gamma|$ 仅在文中等权无损模型下成立，原稿已写明限制；未发现确定数值错误。参考 [MIT 8.04](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/7f930e013cef9cd7dec5aa88baa83f0a_MIT8_04S16_LecNotes1.pdf)、[MIT 22.51 混态课程](https://ocw.mit.edu/courses/22-51-quantum-theory-of-radiation-interactions-fall-2012/00e219fe9b8a81b64613f1428e87cb00_MIT22_51F12_Ch7.pdf)、[Englert 原始论文](https://doi.org/10.1103/PhysRevLett.77.2154)。未改 `sources/`。
