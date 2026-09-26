"""Chapter 14: deterministic list scheduling, including shared control resources.

Run: python3 codes/systems/resource_schedule.py
Times in ns. Standard library only. This feasible greedy schedule is NOT a
general optimizer; no hardware timing/alignment or noise simulation is claimed.
"""
import json


def schedule(operations):
    completed, available, result = {}, {}, []
    for name, duration, predecessors, resources in operations:
        if name in completed or duration <= 0 or not resources:
            raise ValueError("Unique names, positive durations and resources required")
        if any(dep not in completed for dep in predecessors):
            raise ValueError("Operations must be topologically ordered")
        start = max([0] + [completed[dep] for dep in predecessors]
                    + [available.get(res, 0) for res in resources])
        end = start + duration
        result.append({"name": name, "start_ns": start, "end_ns": end,
                       "resources": list(resources)})
        completed[name] = end
        for resource in resources:
            available[resource] = end
    # Independently check resource overlap and dependency completion.
    for row, (_, _, deps, _) in zip(result, operations):
        assert all(completed[dep] <= row["start_ns"] for dep in deps)
    for i, left in enumerate(result):
        for right in result[i+1:]:
            if set(left["resources"]) & set(right["resources"]):
                assert left["end_ns"] <= right["start_ns"] or right["end_ns"] <= left["start_ns"]
    return result


def example(shared):
    a = ("q0", "q1") + (("drive_bus",) if shared else ())
    b = ("q2", "q3") + (("drive_bus",) if shared else ())
    return schedule([("A", 200, (), a), ("B", 200, (), b),
                     ("C", 100, ("A", "B"), ("q1", "q2")),
                     ("measure", 800, ("C",), ("q0", "q1", "q2", "q3", "readout_bus"))])


if __name__ == "__main__":
    parallel, shared = example(False), example(True)
    assert parallel[-1]["end_ns"] == 1100
    assert shared[-1]["end_ns"] == 1300
    try:
        schedule([("bad", 10, ("missing",), ("q0",))])
    except ValueError:
        pass
    else:
        raise AssertionError("Missing predecessor accepted")
    print(json.dumps({"qubits_only": parallel, "shared_bus": shared}, indent=2))
