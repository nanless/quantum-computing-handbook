# 第 52 轮｜数学工具章两张原生教学图

本轮只新增 `handbook/assets/math-complex-plane.svg`（1120 × 650）和 `handbook/assets/math-object-shapes.svg`（1220 × 750）；没有编辑 `01-math.md`、`reader/` 或 `sources/`。

## 图 1：复平面上的 $z=1+i$

图中等比例坐标从原点到 $(1,1)$；实线指向 $z=1+i$，虚线指向共轭 $z^*=1-i$。分别以文字标出实部、虚部、$|z|=\sqrt{1^2+1^2}=\sqrt2$、相位 $\pi/4$、关于实轴的镜像，并写明这不是 Bloch 球。没有把复数的极坐标图误说成物理量子态的三维图。推荐嵌入 `01-math.md` 第 1 节中 `e^{i\theta}=\cos\theta+i\sin\theta` 之后、现有“从振幅到概率”算例之前，旁边正文可用一句话连接 $z=\sqrt2 e^{i\pi/4}$ 和 $z^*z=2$。

## 图 2：ket、bra、内积和外积的形状

选用同一归一化向量 $|v\rangle=(1,i)^T/\sqrt2$，图示共轭转置为 $\langle v|=(1,-i)/\sqrt2$。左下实线框展示 $(1\times2)(2\times1)$ 的内积结果为标量 $1$；右下虚线框展示 $(2\times1)(1\times2)$ 的外积结果为 $\frac12\begin{bmatrix}1&-i\\i&1\end{bmatrix}$。分格显示矩阵元素，避免把行向量的两个元素误看成一个 $1-i$。推荐嵌入 `01-math.md` 第 2 节 ket/bra 定义与内积公式之后、抽象正交例子之前；第 6 节外积处可回链此图，不必重复大图。

两图均有具体 `<title>` 和 `<desc>`，采用色彩加实线/虚线或实线/虚线框双重编码。均有浅/深色样式。`xmllint --noout` 通过；实际用 Chromium 分别渲染浅深主题并人工查看，无标签碰撞，等式和矩阵元素正确。渲染检查文件暂存在 `/private/tmp/math-complex-plane-{light,dark}.png` 和 `/private/tmp/math-object-shapes-final-{light,dark}.png`。放入阅读版时应沿用现有 `.scientific-svg` 容器的局部横向滚动，不把 1120/1220 宽图整张缩至 390px；最终仍需检查正文嵌入后的手机左右边缘和图下说明。

数学记号对照：[IBM 基础量子信息课程的单系统态向量](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information)；本图的具体元素另经手算核对。图不是来自该课程，也不暗示其认可此版式。
