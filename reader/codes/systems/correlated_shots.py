"""Chapter 11: exact variance of a synthetic two-level batch model.

Run: python3 codes/systems/correlated_shots.py
No random sampling: enumerate the binomial mixture, standard library only.
Independent batches; within each batch probability is 0.4 or 0.6 equiprobably.
"""
import json
from math import comb, sqrt, isclose


def moments(size=100, batches=100, low=.4, high=.6):
    if size < 1 or batches < 1 or not (0 <= low <= high <= 1):
        raise ValueError("Invalid batch parameters")
    mean = (low + high) / 2
    if mean in (0, 1):
        raise ValueError("Correlation coefficient undefined at zero variance")
    weights = [sum(.5 * comb(size, k) * p**k * (1-p)**(size-k)
                   for p in (low, high)) for k in range(size+1)]
    assert isclose(sum(weights), 1, abs_tol=1e-12)
    exact = sum(w * (k/size - mean)**2 for k, w in enumerate(weights)) / batches
    corr = ((high-low)/2)**2 / (mean*(1-mean))
    inflation = 1 + (size-1)*corr
    naive = mean * (1-mean) / (size*batches)
    assert isclose(exact, naive * inflation, rel_tol=1e-12)
    return {"raw_shots": size*batches, "intrabatch_correlation": corr,
            "variance_inflation": inflation, "effective_shots": size*batches/inflation,
            "iid_standard_error": sqrt(naive), "actual_standard_error": sqrt(exact)}


if __name__ == "__main__":
    result = moments()
    assert isclose(result["variance_inflation"], 4.96)
    assert isclose(moments(low=.5, high=.5)["variance_inflation"], 1)
    assert isclose(moments(size=1)["variance_inflation"], 1)
    print(json.dumps(result, indent=2))
