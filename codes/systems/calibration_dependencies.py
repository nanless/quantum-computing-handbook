"""Chapter 19: local calibration dependency closure and atomic promotion demo.

Run: python3 codes/systems/calibration_dependencies.py
Synthetic graph and snapshots; no instruments or services. Standard library only.
Graph edges represent declared validation dependencies, not measured causality.
"""
import json
from copy import deepcopy
from graphlib import TopologicalSorter


DEPENDENCIES = {
    "freq0": set(), "amp0": {"freq0"}, "readout0": {"freq0"},
    "cx01": {"amp0", "readout0"}, "layer01": {"cx01"},
    "amp2": set(), "readout2": set(),
}


def affected(graph, changed):
    if not changed <= graph.keys():
        raise ValueError("Unknown changed parameter")
    if any(not parents <= graph.keys() for parents in graph.values()):
        raise ValueError("Unknown dependency")
    order = list(TopologicalSorter(graph).static_order())  # Reject cycles.
    stale = set(changed)
    for node in order:
        if graph[node] & stale:
            stale.add(node)
    return [node for node in order if node in stale]


def promote(active, candidate, required, evidence, expected_version):
    # Caller supplies the dependency closure, not merely the directly changed keys.
    known, required_keys = set(active["parameters"]), set(required)
    if not set(candidate) <= required_keys <= known:
        raise ValueError("Candidate and validation keys must be known and validated")
    if active["version"] != expected_version:
        raise ValueError("Active snapshot changed while candidate was tested")
    if not all(evidence.get(node, False) for node in required):
        return deepcopy(active), False
    updated = deepcopy(active)
    updated["parameters"].update(candidate)
    updated["version"] += 1
    return updated, True


if __name__ == "__main__":
    required = affected(DEPENDENCIES, {"freq0"})
    assert set(required) == {"freq0", "amp0", "readout0", "cx01", "layer01"}
    assert "amp2" not in required
    active = {"version": 7, "parameters": {key: 1.0 for key in DEPENDENCIES}}
    candidate = {key: 1.1 for key in required}
    evidence = {key: True for key in required}
    evidence["layer01"] = False
    rejected, ok = promote(active, candidate, required, evidence, 7)
    assert not ok and rejected == active
    evidence["layer01"] = True
    accepted, ok = promote(active, candidate, required, evidence, 7)
    assert ok and accepted["version"] == 8 and active["version"] == 7
    assert accepted["parameters"]["amp2"] == 1.0
    try:
        promote(accepted, candidate, required, evidence, 7)
    except ValueError:
        pass
    else:
        raise AssertionError("Stale transaction accepted")
    for extra_key in ("amp2", "unknown_parameter"):
        try:
            promote(active, {"freq0": 2, extra_key: 999}, ["freq0"], {"freq0": True}, 7)
        except ValueError:
            pass
        else:
            raise AssertionError("Unvalidated candidate key accepted")
    print(json.dumps({"revalidation_order": required, "failed_regression_version": rejected["version"],
                      "passed_regression_version": accepted["version"], "unrelated_amp2": 1.0}, indent=2))
