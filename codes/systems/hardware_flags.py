"""Chapter 09: erasure flags, exact confusion counts, synthetic not hardware data."""
import json


def counts(total, loss_rate, sensitivity, false_positive):
    assert total > 0 and all(0 <= x <= 1 for x in (loss_rate, sensitivity, false_positive))
    lost = total * loss_rate
    present = total - lost
    tp, fp = lost * sensitivity, present * false_positive
    fn, tn = lost - tp, present - fp
    return dict(tp=tp, fp=fp, fn=fn, tn=tn,
                precision=tp / (tp + fp) if tp + fp else None,
                missed_loss_unflagged=fn / (fn + tn) if fn + tn else None)


def main():
    result = counts(1_000_000, .001, .98, .002)
    assert abs(sum(result[k] for k in ('tp', 'fp', 'fn', 'tn')) - 1_000_000) < 1e-8
    assert result['tp'] == 980 and result['fp'] == 1998 and result['fn'] == 20
    assert abs(result['precision'] - 980 / 2978) < 1e-12
    assert counts(100, 0, 1, 0)['precision'] is None
    assert counts(100, 1, 1, 0)['missed_loss_unflagged'] is None
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
