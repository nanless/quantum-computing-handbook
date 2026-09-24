# 第 37 轮：先导知识路线与自测的资料核查

日期：2026-09-23。范围：新《入门先修》附录及其入口；不覆盖另外三个分组对正文的研究与修订。

## 查到的缺口

原版数学章已经有复数、向量、矩阵、谱分解、张量积的定义和算例，Q1–Q4 也解释物理。然而总目录没有让读者在入门前发现自己缺少分数/条件概率、模运算、实验采样或微积分中的哪一块。尤其“数学 01 的先修：高中代数”容易让读者误以为所有路线都具有相同的数学门槛。没有单独的自测入口，读者只有读到中途才知道该补什么。

## 原始课程资料与支持范围

- [IBM Quantum Learning, Basics of quantum information: Overview](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)：课程面向不同背景读者，建议先熟悉基本线性代数、复数以及集合、函数；内容从单系统、多系统进到线路和纠缠协议。用于限定量子信息入门的基础准备，不替代本书具体的课程安排。
- [IBM Quantum Learning, Classical information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/classical-information)：正式把经典概率向量放在量子态前讲，说明概率语言是有价值的先修。用于支持诊断题先查条件分母和概率向量，不声称量子测量概率能只从经典计数推出。
- [MIT OpenCourseWare, 8.04 Quantum Physics I Syllabus](https://www.ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/pages/syllabus/)：完整本科波动力学课程把振动/波和微分方程列为正式先修，课程包含势阱、谐振子、势垒透射。用于解释本书 Q4 的微积分门槛与算法线路入门门槛不同。

## 实施与独立复算

新增 `handbook/appendices/prerequisites.md`：按量子线路、算法、器件、波函数、实验判断分五条路径；给七题连着详细核对，分别查条件分母、复数归一化、矩阵乘法顺序、两比特基序、模周期、二项抽样和势阱积分。页面把不熟悉的动作直接回链到相应正文。全书导读增加入口，离线阅读器的附录导航把该页置前。

主审独立复算：$200/800=1/4$，$200/2000=1/10$；向量 $(1,1+i)$ 的范数平方为 3、概率 $1/3,2/3$；$HZH|0\rangle=|1\rangle$；$|1\rangle\otimes|+\rangle=(0,0,1,1)^T/\sqrt2$；$2^k\bmod15$ 首个重复周期为 4；400 次独立伯努利事件在 $p=1/2$ 下的频率标准差为 0.025；$\int_0^L\sin^2(\pi x/L)dx=L/2$。这些是明确模型的教学例子，不用于估计真实硬件性能。

## 待后续检查

新增附录与所有内部链接须经阅读器构建和两种宽度验证；表格在手机宽度下应仍可横向阅读。正式交叉审稿在第 38 轮读取修订后的完整版本，不能把本轮初稿当成没有问题的最终版。
