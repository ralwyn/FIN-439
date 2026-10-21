"""FIN 439 Lab 14. AI-assisted; course training inputs, not market estimates.
Run: python3 portfolio.py. Returns and volatilities use decimals.
"""
import math

SLEEVES = ['Treasury bills', 'Treasury 10-year note',
           'Investment-grade bond fund', 'Global equity index fund']
EXPECTED_RETURNS = [0.035, 0.043, 0.050, 0.080]
VOLATILITIES = [0.005, 0.070, 0.060, 0.160]
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE = 0.065  # CPI estimate 2.5% + 4 percentage points
RESERVE_ELIGIBLE = [True, True, False, False]


def validate_correlations(correlations, n):
    if len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError('Correlation table must be square with one row per sleeve.')
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f'Correlation [{i}][{j}] must be finite and between -1 and 1.')
            if not math.isclose(value, correlations[j][i], abs_tol=1e-12):
                raise ValueError('Correlation table must be symmetric.')
        if not math.isclose(correlations[i][i], 1.0, abs_tol=1e-12):
            raise ValueError('Correlation diagonal must equal 1.')


def covariance_matrix(volatilities, correlations):
    validate_correlations(correlations, len(volatilities))
    if any(not math.isfinite(v) or v <= 0 for v in volatilities):
        raise ValueError('Volatilities must be finite and positive.')
    return [[correlations[i][j] * volatilities[i] * volatilities[j]
             for j in range(len(volatilities))] for i in range(len(volatilities))]


def validate_weights(weights, n):
    if len(weights) != n or any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError('One finite nonnegative weight is required per sleeve.')
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-10):
        raise ValueError('Weights must sum to 1.')


def portfolio_return(weights, returns):
    validate_weights(weights, len(returns))
    if any(not math.isfinite(r) for r in returns):
        raise ValueError('Expected returns must be finite.')
    return sum(w * r for w, r in zip(weights, returns))


def portfolio_variance(weights, covariance):
    validate_weights(weights, len(covariance))
    # Both (i,j) and (j,i) appear: the cross-asset covariance is counted twice.
    return sum(weights[i] * weights[j] * covariance[i][j]
               for i in range(len(weights)) for j in range(len(weights)))


def portfolio_volatility(weights, covariance):
    variance = portfolio_variance(weights, covariance)
    if variance < -1e-12:
        raise ValueError('Negative portfolio variance; check covariance inputs.')
    return math.sqrt(max(variance, 0.0))


def reserve_weight(weights, eligible):
    validate_weights(weights, len(eligible))
    return sum(w for w, counts in zip(weights, eligible) if counts)


def meets_objective(expected_return, objective):
    return expected_return >= objective - 1e-12


def equal_weights(n):
    return [1 / n] * n


def inverse_volatility_weights(volatilities):
    if any(not math.isfinite(v) or v <= 0 for v in volatilities):
        raise ValueError('Inverse volatility requires finite positive volatilities.')
    inverse = [1 / v for v in volatilities]
    return [v / sum(inverse) for v in inverse]


def baseline_portfolios():
    return {'Benchmark': [0.0, 0.0, 0.4, 0.6],
            'Equal weight': equal_weights(len(SLEEVES)),
            'Inverse volatility': inverse_volatility_weights(VOLATILITIES)}


def main():
    covariance = covariance_matrix(VOLATILITIES, CORRELATIONS)
    print('Course-authored training inputs; CPI 2.5% is a labelled estimate.')
    print('Weight order: ' + ' / '.join(SLEEVES))
    for name, weights in baseline_portfolios().items():
        expected = portfolio_return(weights, EXPECTED_RETURNS)
        print(f'\n{name}')
        print('Weights (%): ' + ' / '.join(f'{w * 100:.1f}' for w in weights))
        print(f'Expected return: {expected:.2%}')
        print(f'Volatility: {portfolio_volatility(weights, covariance):.2%}')
        print(f'Reserve-eligible weight: {reserve_weight(weights, RESERVE_ELIGIBLE):.1%}')
        print(f'Meets objective {OBJECTIVE:.1%}: {"yes" if meets_objective(expected, OBJECTIVE) else "no"}')


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        raise SystemExit(f'Input error: {error}')
