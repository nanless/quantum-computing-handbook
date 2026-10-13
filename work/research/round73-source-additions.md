# 第73轮新增源码归档

2026-10-13实际联网解析五个官方HEAD为40位固定提交，只对新项目调用refresh_project。先copytree旧vendor到临时staging，再下载/核对所有新文件，整树verify后通过replace_snapshot一次目录事务出版，最后再verify。没有运行全量--refresh。

| 新项目 | 固定提交 | 新文件数 |
|---|---|---:|
| qiskit-addon-slc | d5ccf669fef81908cb4b8d87f74c59042fd91fd9 | 6 |
| qiskit-addon-pna | 9fc9b7fb9c6342fa1e10a7f02b8f8f83d5209fe2 | 3 |
| qiskit-mitigation | 2908a901b2a679def49b5c3fda3879940514235f | 5 |
| samplomatic | 56dac5e883519ae085ac2e78f25b1572536912bd | 6 |
| random123 | 9545ff6413f258be2f04c1d319d99aaef7521150 | 5 |

新增25份，总31项目122份。旧26项目97份文件的commit、原manifest项目条目与实际字节逐字保留；旧retrieved_at_utc未刷新，新增另记round73_added_at_utc。

每个项目包括原README、全部实际存在的根许可证/NOTICE及代表性核心模块。五完整克隆的根文件名单分别核对；这五项目本轮根声明均只有LICENSE或LICENSE.txt，没有漏掉实际根NOTICE。前四为Apache-2.0，Random123保留D. E. Shaw Research三条款原文；各版权头原样。源快照kind仍为unmodified-source-excerpts-not-installable-package，不把excerpt当安装包。完整SDK运行另见codes/sdk/round73，归档不等于所有功能或生产环境验收。

SLC保存forward/backward/local_scales/commutator_bounds；PNA保存核心pna；mitigation保存pec/noise/mitigation_task；samplomatic保存boxing/build/inject_noise/samplex；Random123保存philox/uniform/u01fixedpt。文件SHA-256、字节数、固定raw URL均在manifest。

round73-source-additions.json记录事务及全部新记录，round73-source-additions.log保存真实下载/逐树核验输出。python3 codes/snapshot_sources.py --verify退出0。原六项离线事务回归实际退出0，见round73-snapshot-tests.log；未编写镜像实现的新测试。模块登记仅增加五行，旧项目路径与函数没有修改。
