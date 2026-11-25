"""Exact finite checks for the Chapter 10 stabilizer and distillation examples.

Run python3 codes/systems/stabilizer_distillation_checks.py from the repository.
Only the Python standard library is required.
"""
from collections import deque
from itertools import combinations, product
import json
import math


def parity(mask):
    return bin(mask).count('1') % 2


def xor_span(rows):
    space = {0}
    for row in rows:
        space |= {codeword ^ row for codeword in space}
    return space


def triangular_code(cut):
    # Integer coordinates (2x, 2 sqrt(3) y) for the same honeycomb as the figure.
    corners = [(1, 1), (0, 2), (-1, 1), (-1, -1), (0, -2), (1, -1)]
    faces = []
    edges = {}
    for u, v in product(range(-4, 7), repeat=2):
        polygon = [(2*u+v+x, 3*v+y) for x, y in corners]
        inside = [point for point in polygon
                  if max(2*(point[0]-1), point[1]-point[0], 2-point[0]-point[1]) <= cut]
        if len(inside) >= 4:
            faces.append(inside)
        for left, right in zip(polygon, polygon[1:] + polygon[:1]):
            if left in inside and right in inside:
                edges.setdefault(left, set()).add(right)
                edges.setdefault(right, set()).add(left)
    sites = sorted(edges)
    labels = {sites[0]: 1}
    queue = deque(labels)
    while queue:
        point = queue.popleft()
        for neighbor in edges[point]:
            if neighbor not in labels:
                labels[neighbor] = -labels[point]
                queue.append(neighbor)
            assert labels[neighbor] == -labels[point]
    assert len(labels) == len(sites)
    polarity = sum(labels.values())
    assert abs(polarity) == 1
    signs = [polarity * labels[site] for site in sites]
    rows = [sum(1 << sites.index(point) for point in face) for face in faces]
    return signs, rows


def check_code(cut, n, d):
    signs, rows = triangular_code(cut)
    assert len(signs) == n
    assert all(not parity(a & b) for a, b in product(rows, repeat=2))
    span = xor_span(rows)
    assert len(span) == 2 ** ((n - 1) // 2)
    phase_classes_stabilizer = len(span) ** 2
    phase_classes_centralizer = 2 ** (2*n - (n-1))
    minimum = next(weight for weight in range(1, d+1)
                   if any(mask not in span and all(not parity(mask & row) for row in rows)
                          for chosen in combinations(range(n), weight)
                          for mask in [sum(1 << i for i in chosen)]))
    assert minimum == d
    for row in rows:
        assert sum(sign for i, sign in enumerate(signs) if (row >> i) & 1) == 0
    # Verify the signed S and H_XY actions on both CSS logical basis supports.
    # Signed S's phase is exp(i pi*w/2); signed H_XY's is exp(i pi*(1-2w)/4).
    for codeword in span:
        signed_weight = sum(sign for i, sign in enumerate(signs) if (codeword >> i) & 1)
        assert signed_weight % 4 == 0
        assert (sum(signs) - signed_weight) % 4 == 1
    assert sum(signs) == 1
    uniform_flips = sum(bin(row).count('1') % 4 == 2 for row in rows)
    assert uniform_flips == (0 if d == 3 else 3)
    return dict(n=n, distance=d, stabilizer_generators=len(rows)*2,
                phase_classes_stabilizer=phase_classes_stabilizer,
                phase_classes_centralizer=phase_classes_centralizer,
                sublattices=[signs.count(1), signs.count(-1)],
                x_check_sign_flips_under_uniform_phase_gate=uniform_flips)


def accepted_distillation(p):
    accept, error = [], []
    triples = 0
    for weight in range(16):
        probability = p**weight * (1-p)**(15-weight)
        for locations in combinations(range(1,16),weight):
            syndrome = 0
            for column in locations:
                syndrome ^= column
            if syndrome == 0:
                accept.append(probability)
                if weight % 2:
                    error.append(probability)
                triples += weight == 3
    assert triples == 35
    accept_probability = math.fsum(accept)
    return accept_probability, math.fsum(error)/accept_probability


def main():
    steane = check_code(2, 7, 3)
    color5 = check_code(4, 19, 5)
    assert steane["phase_classes_stabilizer"] == 64
    assert steane["phase_classes_centralizer"] == 256
    p = 0.01
    accept, error = accepted_distillation(p)
    second_accept, second_error = accepted_distillation(error)
    assert math.isclose(accept, .86009033, abs_tol=5e-9)
    assert math.isclose(error, 3.60877e-5, abs_tol=5e-11)
    syndrome_all = 0
    for column in range(1,16):
        syndrome_all ^= column
    assert syndrome_all == 0 and 15 % 2 == 1
    print(json.dumps({
        "trivial_single_qubit_code_distance": min(bin(mask).count('1') for mask in (1,)),
        "steane": steane, "color_distance_five": color5,
        "distillation": {"p": p, "accept": accept, "conditional_error": error,
                         "second_conditional_error": second_error,
                         "raw_states_per_two_stage_output": 225 / (accept * second_accept),
                         "fully_correlated_accept": 1, "fully_correlated_error": p},
    }, indent=2))


if __name__ == "__main__":
    main()
