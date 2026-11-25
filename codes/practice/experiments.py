#!/usr/bin/env python3
"""Chapter 15: reproducible statistical checks; Python 3.9+, standard library."""
import json, math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from validation_reports import write_result

def bell_lower(counts, alpha=0.05):
    correlations=[]; radii=[]
    for plus, minus in counts:
        n=plus+minus
        assert n>0 and plus>=0 and minus>=0
        correlations.append((plus-minus)/n)
        radii.append(math.sqrt(2*math.log(6/alpha)/n))
    f=(1+correlations[0]-correlations[1]+correlations[2])/4
    return {'point':f,'lower':f-sum(radii)/4,'radii':radii}

def main():
    counts=[(775,225),(250,750),(800,200)]
    bell=bell_lower(counts)
    assert abs(bell['point']-0.6625)<1e-12
    assert 0.5891<bell['lower']<0.5892
    # N differs by basis. Applying N=1000 to all three is invalid here.
    unequal=bell_lower([(775,225),(25,75),(800,200)])
    assert unequal['lower']<bell['lower']
    # Linear extrapolation at noise factors 1,3: weights 3/2,-1/2.
    raw=[0.90,0.50]; w=[1.5,-0.5]
    estimate=sum(a*b for a,b in zip(w,raw))
    assert math.isclose(estimate,1.10)
    total=4000
    equal_worst=sum(a*a/(total/2) for a in w)
    optimal_n=[3000,1000]
    optimal_worst=sum(a*a/n for a,n in zip(w,optimal_n))
    assert math.isclose(equal_worst,5/total)
    assert math.isclose(optimal_worst,4/total)
    # Checking 20 independent tests at alpha=.05: familywise error is not .05.
    familywise=1-0.95**20
    assert 0.64<familywise<0.65
    result={'model':'synthetic fixed counts, independent bounded outcomes assumed',
      'bell_equal':bell,'bell_unequal':unequal,
      'zne':{'estimate':estimate,'equal_allocation_variance_upper':equal_worst,
             'optimal_allocation_variance_upper':optimal_worst,'optimal_shots':optimal_n},
      'twenty_independent_tests_false_positive_probability':familywise}
    target=pathlib.Path(__file__).resolve().with_name('results.json')
    write_result(target, json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
