"""Known-answer and mutation checks; run python3 verify_lab14.py."""
import copy
import portfolio as p
import mandate as m

expected = {
    'Benchmark': ('6.80%', '10.46%', '0.0%', '0.0 / 0.0 / 40.0 / 60.0', True),
    'Equal weight': ('5.20%', '5.21%', '50.0%', '25.0 / 25.0 / 25.0 / 25.0', False),
    'Inverse volatility': ('3.77%', '1.05%', '90.3%', '84.3 / 6.0 / 7.0 / 2.6', False),
}
cov = p.covariance_matrix(p.VOLATILITIES, p.CORRELATIONS)
for name, weights in p.baseline_portfolios().items():
    result = (f'{p.portfolio_return(weights, p.EXPECTED_RETURNS):.2%}',
              f'{p.portfolio_volatility(weights, cov):.2%}',
              f'{p.reserve_weight(weights, p.RESERVE_ELIGIBLE):.1%}',
              ' / '.join(f'{w * 100:.1f}' for w in weights),
              p.meets_objective(p.portfolio_return(weights, p.EXPECTED_RETURNS), p.OBJECTIVE))
    assert result == expected[name], (name, result)
    print(f'PASS: {name}, all published values')
probe = copy.deepcopy(p.CORRELATIONS)
probe[2][3] = probe[3][2] = .50
risk = p.portfolio_volatility([0, 0, .4, .6], p.covariance_matrix(p.VOLATILITIES, probe))
assert f'{risk:.2%}' == '11.00%'
print(f'PASS: correlation 0.50 in both cells -> benchmark {risk:.2%}')
for label, value, symmetric in [('out of range', 1.3, True), ('asymmetric', .5, False)]:
    probe = copy.deepcopy(p.CORRELATIONS)
    probe[2][3] = value
    if symmetric:
        probe[3][2] = value
    try:
        p.covariance_matrix(p.VOLATILITIES, probe)
    except ValueError as error:
        print(f'PASS: {label} refused: {error}')
    else:
        raise AssertionError(f'{label} was accepted')
checks = m.check(m.CANDIDATES['E'])
assert [i for i, row in enumerate(checks) if not row[2]] == [2]
assert checks[2][1] == 0
print('PASS: benchmark E fails the 3% reserve rule at 0.0%; other checkable rules pass')
assert p.CORRELATIONS[2][3] == p.CORRELATIONS[3][2] == .25
print('PASS: original correlations remain 0.25')
