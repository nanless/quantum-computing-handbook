"""Chapter 12: finite-memory two-link renewal process, standard library only.

Run: python3 codes/systems/network_cutoff.py
Synthetic p=0.1 per link per 1 ms slot; ideal herald/swap; both links reset on
timeout. K allows exactly K further attempts after the first pair is stored.
Compares closed form against explicit transient-state probability propagation.
"""
import json
from math import exp, isclose


def closed_form(p, cutoff, tau_ms=1, memory_ms=20):
    if not 0 < p <= 1 or not isinstance(cutoff, int) or cutoff < 0:
        raise ValueError("p in (0,1], cutoff a nonnegative integer")
    if tau_ms <= 0 or memory_ms <= 0:
        raise ValueError("Positive times required")
    q = 1-p
    den = p*p + 2*p*q*(1-q**cutoff)
    wait = (1 + 2*q*(1-q**cutoff)) / den
    coherence = (p*p + 2*p*q*sum(p*q**(d-1)*exp(-d*tau_ms/memory_ms)
                                for d in range(1, cutoff+1))) / den
    return wait, coherence


def state_expectation(p, cutoff):
    # State 0: both empty. State k>0: one ready, k attempts remain.
    q = 1-p
    mass = [1.] + [0.] * cutoff
    expected = 0.
    for _ in range(100000):
        expected += sum(mass)  # E[T] = sum_{t>=0} P(T>t).
        nxt = [0.] * (cutoff+1)
        nxt[0] += q*q*mass[0]
        nxt[cutoff] += 2*p*q*mass[0]
        for k in range(1, cutoff+1):
            nxt[k-1] += q*mass[k]
        mass = nxt
        if sum(mass) < 1e-15:
            break
    else:
        raise RuntimeError("Increase horizon for this p")
    return expected


if __name__ == "__main__":
    output = []
    for k in (0, 1, 5, 20):
        wait, coherence = closed_form(.1, k)
        numerical = state_expectation(.1, k)
        assert isclose(wait, numerical, rel_tol=1e-11)
        output.append({"cutoff_slots": k, "expected_slots": wait,
                       "conditional_coherence": coherence})
    assert isclose(output[0]["expected_slots"], 100)
    assert isclose(output[1]["expected_slots"], 295/7)
    assert closed_form(1, 5) == (1, 1)
    print(json.dumps(output, indent=2))
