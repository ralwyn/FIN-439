"""Executed course fixtures, CSV estimates and portfolio constraints.
Run: python3 verify_lab15.py. No prices are downloaded by this script.
"""
import copy
import io
import json
import math
from pathlib import Path
import portfolio as p

ROOT = Path(__file__).resolve().parent

def solve(returns, corr=None):
    return p.search_portfolio(returns, p.VOLATILITIES,
        p.CORRELATIONS if corr is None else corr, .065, p.RESERVE_ELIGIBLE, .03)

def verify_fixture(result, weights, expected_return, risk):
    assert result is not None
    assert result['weights'] == weights, result
    assert f"{result['return'] * 100:.2f}" == expected_return
    assert f"{result['volatility'] * 100:.2f}" == risk

def valid_result(result, returns, objective, eligible, minimum):
    if result is None:
        return
    assert math.isclose(sum(result['weights']), 1)
    assert all(w >= 0 and math.isclose(w * 20, round(w * 20)) for w in result['weights'])
    assert p.portfolio_return(result['weights'], returns) >= objective - 1e-12
    assert p.reserve_weight(result['weights'], eligible) >= minimum - 1e-12

def main():
    base = solve(p.EXPECTED_RETURNS)
    verify_fixture(base, [0, .2, .25, .55], '6.51', '9.44')
    changed = p.EXPECTED_RETURNS.copy()
    changed[3] = .07
    stress = solve(changed)
    verify_fixture(stress, [0, .1, .1, .8], '6.53', '12.94')
    assert math.isclose(p.largest_weight_change(base, stress), 25)
    corr = copy.deepcopy(p.CORRELATIONS)
    corr[2][3] = corr[3][2] = .5
    correlation_probe = solve(p.EXPECTED_RETURNS, corr)
    verify_fixture(correlation_probe, [0, .4, 0, .6], '6.52', '9.73')
    bad = copy.deepcopy(corr)
    bad[2][3] = bad[3][2] = 1.3
    try:
        solve(p.EXPECTED_RETURNS, bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid correlation was not refused.')
    grid = list(p.weight_grid(4))
    assert len(grid) == len({tuple(w) for w in grid}) == 1771
    assert solve([0,0,0,0]) is None
    result = {'meridian_as_loaded': base, 'meridian_equity_7': stress,
              'meridian_change_pp': p.largest_weight_change(base, stress),
              'meridian_correlation_050': correlation_probe}
    full = p.estimate_from_csv(ROOT / 'prices.csv')
    recent = p.estimate_from_csv(ROOT / 'prices.csv', True)
    assert full['months'] == 59 and recent['months'] == 36
    eligible = [name == 'BIL' for name in full['names']]
    for key, data in [('scholarship_all', full), ('scholarship_36', recent)]:
        allocation = p.search_portfolio(data['returns'],data['volatilities'],data['correlations'],.065,eligible,.1)
        valid_result(allocation, data['returns'], .065, eligible, .1)
        result[key] = {'estimates': data, 'allocation': allocation}
    lower = full['returns'].copy()
    lower[full['names'].index('VT')] -= .01
    own_stress = p.search_portfolio(lower,full['volatilities'],full['correlations'],.065,eligible,.1)
    valid_result(own_stress, lower, .065, eligible, .1)
    result['scholarship_VT_minus_1pp'] = own_stress
    result['scholarship_window_change_pp'] = p.largest_weight_change(result['scholarship_all']['allocation'], result['scholarship_36']['allocation'])
    result['scholarship_VT_stress_change_pp'] = p.largest_weight_change(result['scholarship_all']['allocation'], own_stress)
    # Independent numpy cross-check for estimation arithmetic, not a snapshot of engine code.
    import numpy as np
    import pandas as pd
    levels = pd.read_csv(ROOT / 'prices.csv').iloc[:,1:].to_numpy()
    monthly = levels[1:] / levels[:-1] - 1
    for data, values in [(full,monthly),(recent,monthly[-36:])]:
        assert np.allclose(data['returns'],np.mean(values,axis=0)*12)
        assert np.allclose(data['volatilities'],np.std(values,axis=0,ddof=1)*np.sqrt(12))
        assert np.allclose(data['correlations'],np.corrcoef(values,rowvar=False))
    for csv_text in ['Date,A,B,C\n2020-02-01,1,2,3\n2020-01-01,2,3,4\n2020-03-01,3,4,5',
                     'Date,A,B,C\n2020-01-01,1,2,3\n2020-02-01,0,3,4\n2020-03-01,3,4,5']:
        try:
            p.estimate_from_csv(io.StringIO(csv_text))
        except ValueError:
            pass
        else:
            raise AssertionError('Bad monthly data was accepted.')
    (ROOT/'executed-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: three published Meridian fixtures; 25-point shift; bad correlation rejection.')
    print('PASS: 1771 distinct mixes; infeasible target; malformed monthly data rejection.')
    print('PASS: 59/36 monthly-return windows cross-checked independently with numpy.')
    print('PASS: scholarship allocations meet long-only, sum-to-one, 5-point grid, 6.5% target and 10% reserve constraints.')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
