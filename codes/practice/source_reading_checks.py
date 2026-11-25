#!/usr/bin/env python3
"""Independent stdlib checks for source-reading exercises S04/S05/S06/S08.

Does not import or execute vendor files. S07 is an engineering discussion,
not a claim that a numerical unit test certifies a control system.
"""
import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation_reports import write_result


def main():
    if not __debug__:
        raise RuntimeError('Run without -O')
    samples = []
    for x in [0, .5, 1]:
        t0, t2 = 1, 2*x*x-1
        correct, wrong = .5*t0+.5*t2, t2
        assert math.isclose(correct, x*x, abs_tol=1e-12)
        samples.append(dict(x=x, correct=correct, wrong=wrong))
    a = [[-.4, .3], [.3, .4]]
    square = [[sum(a[i][k]*a[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    for i in range(2):
        for j in range(2):
            assert math.isclose(square[i][j], .25 if i == j else 0, abs_tol=1e-12)
    snapshot = [[.5, 1.5], [1.5, .5]]
    for v, eigenvalue in [([1, 1], 2), ([1, -1], -1)]:
        out = [sum(snapshot[i][j]*v[j] for j in range(2)) for i in range(2)]
        assert all(math.isclose(x, eigenvalue*y) for x, y in zip(out, v))
    correct_order = 1.5*.4-.5*(-.2)
    swapped_order = 1.5*(-.2)-.5*.4
    assert math.isclose(correct_order, .7) and math.isclose(swapped_order, -.5)
    result = {'scope': 'independent authored math; no upstream runtime tests',
              'S04_Chebyshev': samples,
              'S05_LCU': {'matrix': a, 'square': square, 'norm': .5, 'alpha': .7},
              'S06_shadow': {'matrix': snapshot, 'eigenvalues': [2, -1], 'trace': 1},
              'S08_order': {'correct': correct_order, 'swapped': swapped_order}}
    text = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    write_result(Path(__file__).resolve().with_name('source-reading-results.json'), text)
    print(text, end='')


if __name__ == '__main__':
    main()
