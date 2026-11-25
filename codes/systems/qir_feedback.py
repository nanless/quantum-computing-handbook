"""Run the Chapter 14 QIR 2.0 feedback example on QIR Runner 0.9.7.

Pass --clang clang to assemble LLVM bitcode before running. The default
runs the same textual module. Uses four real simulator batches covering
both branch values and both supported result-read ABI spellings.
"""

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

MODULE = r"""
@condition = internal constant [10 x i8] c"condition\00"
@target = internal constant [7 x i8] c"target\00"

define i64 @feedback() #0 {
entry:
  call void @__quantum__rt__initialize(ptr null)
  call void @__quantum__qis__x__body(ptr null)
  call void @__quantum__qis__mz__body(ptr null, ptr null)
  %feed = call i1 @__quantum__rt__read_result(ptr readonly null)
  br i1 %feed, label %apply, label %finish

apply:
  call void @__quantum__qis__x__body(ptr inttoptr (i64 1 to ptr))
  br label %finish

finish:
  call void @__quantum__qis__mz__body(ptr inttoptr (i64 1 to ptr), ptr inttoptr (i64 1 to ptr))
  call void @__quantum__rt__result_record_output(ptr null, ptr @condition)
  call void @__quantum__rt__result_record_output(ptr inttoptr (i64 1 to ptr), ptr @target)
  ret i64 0
}

declare void @__quantum__rt__initialize(ptr)
declare void @__quantum__qis__x__body(ptr)
declare void @__quantum__qis__mz__body(ptr, ptr writeonly) #1
declare i1 @__quantum__rt__read_result(ptr readonly)
declare void @__quantum__rt__result_record_output(ptr, ptr)

attributes #0 = { "entry_point" "qir_profiles"="adaptive_profile" "output_labeling_schema"="labeled" "required_num_qubits"="2" "required_num_results"="2" }
attributes #1 = { "irreversible" }

!llvm.module.flags = !{!0, !1, !2, !3}
!0 = !{i32 1, !"qir_major_version", i32 2}
!1 = !{i32 7, !"qir_minor_version", i32 0}
!2 = !{i32 1, !"dynamic_qubit_management", i1 false}
!3 = !{i32 1, !"dynamic_result_management", i1 false}
"""


def assert_output(output, expected, shots):
    rows = list(filter(None, output.splitlines()))
    results = [line.split("\t")[2:] for line in rows if line.startswith("OUTPUT\tRESULT\t")]
    assert results == [[str(expected), label] for _ in range(shots) for label in ("condition", "target")], output
    assert rows.count("END\t0") == shots, output
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clang", help="optional clang executable used to emit a .bc module")
    args = parser.parse_args()
    import qirrunner

    installed_version = version("qirrunner")
    if installed_version != "0.9.7":
        parser.error(f"install qirrunner==0.9.7 (found {installed_version})")
    results = {}
    with TemporaryDirectory() as temp:
        for abi in ("__quantum__rt__read_result", "__quantum__qis__read_result__body"):
            for bit in (0, 1):
                source = MODULE.replace("__quantum__rt__read_result", abi)
                if bit == 0:
                    source = source.replace("  call void @__quantum__qis__x__body(ptr null)\n", "")
                path = Path(temp) / "feedback.ll"
                path.write_text(source, encoding="utf-8")
                if args.clang:
                    bitcode = path.with_suffix(".bc")
                    subprocess.run([args.clang, "-c", "-emit-llvm", "-Wno-override-module",
                                    "-x", "ir", str(path), "-o", str(bitcode)], check=True)
                    path = bitcode
                output = qirrunner.OutputHandler()
                qirrunner.run(str(path), entry_point="feedback", shots=3, rng_seed=20261126,
                              output_fn=output.handle)
                results[f"{abi}/{bit}"] = assert_output(output.get_output(), bit, 3)
    print(json.dumps({"qirrunner": installed_version, "assembled_bitcode": bool(args.clang),
                      "labelled_outputs": results}, indent=2))


if __name__ == "__main__":
    main()
