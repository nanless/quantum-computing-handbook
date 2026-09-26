# 第三方源码固定快照

核验于 2026-09-26；只保存代表性源码与许可，不是完整可安装软件包。原始版权头保留，不自动执行这些文件。许可证以各目录实际原件为准，未对全书或独立教学程序重新授权。

[机器可读清单](manifest.json)包含完整 commit、原始 URL、字节数及 SHA-256。离线校验：`python3 codes/snapshot_sources.py --verify`。按固定快照重新下载：`python3 codes/snapshot_sources.py --fetch`；只有显式 `--refresh` 才改为新的 HEAD。

## 固定版本与内容

| 项目 | 提交 | 许可 | 本地文件 |
|---|---|---|---|
| [qiskit-algorithms](https://github.com/qiskit-community/qiskit-algorithms) | [bcb7ded3594d](https://github.com/qiskit-community/qiskit-algorithms/tree/bcb7ded3594dac02e14acce7f59f05976916d39d) | Apache-2.0 | [LICENSE.txt](qiskit-algorithms/LICENSE.txt) · [qiskit_algorithms/amplitude_amplifiers/grover.py](qiskit-algorithms/qiskit_algorithms/amplitude_amplifiers/grover.py) · [qiskit_algorithms/amplitude_estimators/iae.py](qiskit-algorithms/qiskit_algorithms/amplitude_estimators/iae.py) · [qiskit_algorithms/minimum_eigensolvers/vqe.py](qiskit-algorithms/qiskit_algorithms/minimum_eigensolvers/vqe.py) · [qiskit_algorithms/phase_estimators/phase_estimation.py](qiskit-algorithms/qiskit_algorithms/phase_estimators/phase_estimation.py) |
| [cirq](https://github.com/quantumlib/Cirq) | [e1fa91b61d46](https://github.com/quantumlib/Cirq/tree/e1fa91b61d46437c63953b259c18a0c9d3b8ddad) | Apache-2.0 | [AUTHORS](cirq/AUTHORS) · [LICENSE](cirq/LICENSE) · [examples/grover.py](cirq/examples/grover.py) · [examples/phase_estimator.py](cirq/examples/phase_estimator.py) · [examples/shor.py](cirq/examples/shor.py) |
| [pennylane](https://github.com/PennyLaneAI/pennylane) | [45f1df84938b](https://github.com/PennyLaneAI/pennylane/tree/45f1df84938b3bcbab9e20b284e90010d5f839aa) | Apache-2.0 | [LICENSE](pennylane/LICENSE) · [pennylane/qaoa/cost.py](pennylane/pennylane/qaoa/cost.py) · [pennylane/templates/subroutines/qsvt.py](pennylane/pennylane/templates/subroutines/qsvt.py) |
| [openfermion](https://github.com/quantumlib/OpenFermion) | [60a6e1ab3362](https://github.com/quantumlib/OpenFermion/tree/60a6e1ab3362b6e580a3a96ebf24e42680c78799) | Apache-2.0 | [AUTHORS](openfermion/AUTHORS) · [LICENSE](openfermion/LICENSE) · [NOTICE](openfermion/NOTICE) · [src/openfermion/transforms/opconversions/jordan_wigner.py](openfermion/src/openfermion/transforms/opconversions/jordan_wigner.py) |
| [qualtran](https://github.com/quantumlib/Qualtran) | [8db02b8b3fb3](https://github.com/quantumlib/Qualtran/tree/8db02b8b3fb39d69d2900dcc7b52d9d6a36834c3) | Apache-2.0 | [LICENSE](qualtran/LICENSE) · [qualtran/bloqs/arithmetic/addition.py](qualtran/qualtran/bloqs/arithmetic/addition.py) · [qualtran/bloqs/qft/qft_text_book.py](qualtran/qualtran/bloqs/qft/qft_text_book.py) |
| [qiskit-addon-sqd](https://github.com/Qiskit/qiskit-addon-sqd) | [99ef7544aac3](https://github.com/Qiskit/qiskit-addon-sqd/tree/99ef7544aac30280bcee76737b1faedce06d197f) | Apache-2.0 | [LICENSE.txt](qiskit-addon-sqd/LICENSE.txt) · [qiskit_addon_sqd/configuration_recovery.py](qiskit-addon-sqd/qiskit_addon_sqd/configuration_recovery.py) · [qiskit_addon_sqd/fermion.py](qiskit-addon-sqd/qiskit_addon_sqd/fermion.py) |
| [qutip](https://github.com/qutip/qutip) | [310b91e7d8bb](https://github.com/qutip/qutip/tree/310b91e7d8bbfcffa523c380cc4e733906d0a330) | BSD-3-Clause | [LICENSE.txt](qutip/LICENSE.txt) · [qutip/solver/mesolve.py](qutip/qutip/solver/mesolve.py) |
| [quimb](https://github.com/jcmgray/quimb) | [ebe5a45718aa](https://github.com/jcmgray/quimb/tree/ebe5a45718aa423a6b75d75e257e737044c077dd) | Apache-2.0 | [LICENSE.txt](quimb/LICENSE.txt) · [quimb/tensor/circuit_gen.py](quimb/quimb/tensor/circuit_gen.py) · [quimb/tensor/contraction.py](quimb/quimb/tensor/contraction.py) |
| [stim](https://github.com/quantumlib/Stim) | [131793efb342](https://github.com/quantumlib/Stim/tree/131793efb34238481fadb1b4959f2395ec3f722a) | Apache-2.0 | [LICENSE](stim/LICENSE) · [src/stim/gen/gen_rep_code.cc](stim/src/stim/gen/gen_rep_code.cc) · [src/stim/gen/gen_surface_code.cc](stim/src/stim/gen/gen_surface_code.cc) |
| [pymatching](https://github.com/oscarhiggott/PyMatching) | [6f63b2b9474b](https://github.com/oscarhiggott/PyMatching/tree/6f63b2b9474ba0fa7e511fe52bffdce858a06984) | Apache-2.0 | [LICENSE](pymatching/LICENSE) · [src/pymatching/matching.py](pymatching/src/pymatching/matching.py) |
| [mitiq](https://github.com/unitaryfoundation/mitiq) | [1a892a9783dd](https://github.com/unitaryfoundation/mitiq/tree/1a892a9783ddfe8c39d3d035613d6f3d168df9af) | GPL-3.0，保留原文 | [LICENSE](mitiq/LICENSE) · [mitiq/zne/inference.py](mitiq/mitiq/zne/inference.py) · [mitiq/zne/scaling/folding.py](mitiq/mitiq/zne/scaling/folding.py) |
| [dimod](https://github.com/dwavesystems/dimod) | [7eadc49df61f](https://github.com/dwavesystems/dimod/tree/7eadc49df61fdf01848d882636b719548d30b142) | Apache-2.0 | [LICENSE](dimod/LICENSE) · [dimod/reference/samplers/exact_solver.py](dimod/dimod/reference/samplers/exact_solver.py) |
| [qiskit](https://github.com/Qiskit/qiskit) | [e9c25a42586a](https://github.com/Qiskit/qiskit/tree/e9c25a42586aba7f513de65b020fc6360fac7c67) | Apache-2.0 | [LICENSE.txt](qiskit/LICENSE.txt) · [qiskit/quantum_info/states/utils.py](qiskit/qiskit/quantum_info/states/utils.py) · [qiskit/transpiler/passes/routing/sabre_swap.py](qiskit/qiskit/transpiler/passes/routing/sabre_swap.py) |
| [sequence](https://github.com/sequence-toolbox/SeQUeNCe) | [3133c66d80a8](https://github.com/sequence-toolbox/SeQUeNCe/tree/3133c66d80a898c6c3cc9af9eec3fa94fdbe2233) | BSD 三条款形式，保留原文 | [LICENSE](sequence/LICENSE) · [sequence/entanglement_management/teleportation.py](sequence/sequence/entanglement_management/teleportation.py) · [sequence/entanglement_management/entanglement_protocol.py](sequence/sequence/entanglement_management/entanglement_protocol.py) |
| [liboqs](https://github.com/open-quantum-safe/liboqs) | [b196b57aa615](https://github.com/open-quantum-safe/liboqs/tree/b196b57aa615c84d62cbf6a59a8bfc294e6747dd) | 本摘录 MIT；其他模块另查 | [LICENSE.txt](liboqs/LICENSE.txt) · [tests/example_kem.c](liboqs/tests/example_kem.c) |

## 阅读而非直接安装

先打开相关源码，跟踪输入、输出、边界检查和依赖。需要运行完整包时，在独立环境克隆官方仓库并 checkout 对应 40 位提交，再遵循该提交的安装说明。不要把本目录加入 PYTHONPATH 来冒充完整包。

Mitiq 当前固定快照的 LICENSE 是 GPL 第 3 版；不能凭旧资料写成宽松许可。QuTiP 与 SeQUeNCe 保留原有三条款许可文本。liboqs 的仓库包含不同许可组件，本轮仅保存标注 MIT 的 KEM 示例和根声明。

下载工具不读取云令牌、不访问付费服务、不执行上游程序。第三方源码仅做下载完整性核验；本书自编实验的执行记录与之分开。
