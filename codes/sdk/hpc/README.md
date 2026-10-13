# 完整 SQD-HPC C++ 构建

完整上游固定为`69f003f8304c8094ff06ba2600d38a0c683422ff`，不是直接编译vendor内的几个头文件。

```sh
git clone https://github.com/Qiskit/qiskit-addon-sqd-hpc.git sqd-hpc
git -C sqd-hpc checkout 69f003f8304c8094ff06ba2600d38a0c683422ff
git -C sqd-hpc submodule update --init --recursive
cmake -S sqd-hpc -B sqd-upstream-build -DCMAKE_BUILD_TYPE=Release
cmake --build sqd-upstream-build --target sqd_tests sqd_rng_reproducibility_dump
./sqd-upstream-build/sqd_tests
cmake -S codes/sdk/hpc -B sqd-handbook-build -DSQD_SOURCE="$PWD/sqd-hpc"
cmake --build sqd-handbook-build --target handbook_sqd
./sqd-handbook-build/handbook_sqd
```

实际使用Apple Clang 21、C++17、单进程串行模式。完整上游49测试/36652断言通过，见[日志](upstream-tests.log)。本书[独立驱动](validate_hpc.cpp)从16个四位配置开始，后选择到4个满足两侧各一电子的配置，再执行8批无放回三样本子采样和组态恢复。后选择权重独立核对为6、7、10、11除以34，结果归一化、粒子数、重复种子一致性均检查，见[结果](results.json)。

上游随机输出同构建重复两次一致，见[rng-first.txt](rng-first.txt)和[rng-second.txt](rng-second.txt)。这没有检查跨编译器、线程或MPI的位级复现；C++17构建也没有测试C++26 Philox。没有执行大规模分布式电子结构计算。编译选项依据[上游官方说明](https://qiskit.github.io/qiskit-addon-sqd-hpc/compilation-flags.html)。
