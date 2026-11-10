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


# Lab 15 additions: the Lab 14 functions and printed output above are preserved.
def weight_grid(n, units=20):
    """Generate every fully invested long-only allocation in 1/units steps."""
    if n < 1 or units < 1:
        raise ValueError('Positive asset count and grid size required.')

    def allocations(remaining, slots, prefix):
        if slots == 1:
            yield prefix + [remaining / units]
        else:
            for amount in range(remaining + 1):
                yield from allocations(remaining - amount, slots - 1,
                                       prefix + [amount / units])

    yield from allocations(units, n, [])


def search_portfolio(returns, volatilities, correlations, objective,
                     eligible, reserve_minimum):
    """Lowest volatility on the 5-point grid, or None if infeasible.

    Ties retain the first allocation encountered. This is a discrete grid
    search, not a continuous global optimizer or a guarantee about future risk.
    """
    n = len(returns)
    if not 3 <= n <= 6 or len(volatilities) != n or len(eligible) != n:
        raise ValueError('Use three to six assets with matching input lengths.')
    if not all(math.isfinite(r) for r in returns) or not math.isfinite(objective):
        raise ValueError('Return estimates and objective must be finite.')
    if not math.isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError('Reserve minimum must be between 0% and 100%.')
    covariance = covariance_matrix(volatilities, correlations)
    best = None
    best_variance = math.inf
    for weights in weight_grid(n):
        expected = portfolio_return(weights, returns)
        reserve = reserve_weight(weights, eligible)
        if not meets_objective(expected, objective) or reserve < reserve_minimum - 1e-12:
            continue
        variance = portfolio_variance(weights, covariance)
        if variance < best_variance - 1e-15:
            best_variance = variance
            best = {'weights': weights, 'return': expected,
                    'volatility': portfolio_volatility(weights, covariance),
                    'reserve': reserve}
    return best


def estimate_from_csv(source, last_36=False):
    """Estimate moments from monthly adjusted prices; standard library only.

    source: path, text stream, or binary Streamlit upload. Compute returns first,
    then select the last 36 returns (requires 37 price rows). Use sample moments.
    """
    import csv
    import io
    import statistics
    from datetime import date
    from pathlib import Path

    if isinstance(source, (str, Path)):
        text = Path(source).read_text(encoding='utf-8-sig')
    else:
        text = source.getvalue() if hasattr(source, 'getvalue') else source.read()
        if isinstance(text, bytes):
            text = text.decode('utf-8-sig')
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or not 4 <= len(rows[0]) <= 7:
        raise ValueError('CSV needs Date first and three to six ticker columns.')
    names = [name.strip() for name in rows[0][1:]]
    if any(not name for name in names) or len(set(names)) != len(names):
        raise ValueError('Ticker headers must be nonempty and unique.')
    dates, prices = [], []
    for line_number, row in enumerate(rows[1:], 2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(names) + 1:
            raise ValueError(f'CSV row {line_number}: wrong number of columns.')
        try:
            day = date.fromisoformat(row[0].strip())
            values = [float(cell) for cell in row[1:]]
        except ValueError:
            raise ValueError(f'CSV row {line_number}: use YYYY-MM-DD and numeric prices.') from None
        if any(not math.isfinite(v) or v <= 0 for v in values):
            raise ValueError(f'CSV row {line_number}: prices must be finite and positive.')
        month = day.year * 12 + day.month
        if dates:
            previous = dates[-1].year * 12 + dates[-1].month
            if month != previous + 1:
                raise ValueError('CSV must be oldest first with one row per consecutive month.')
        dates.append(day)
        prices.append(values)
    if len(prices) < 3:
        raise ValueError('At least three monthly price rows are needed.')
    monthly = [[prices[t][i] / prices[t - 1][i] - 1 for i in range(len(names))]
               for t in range(1, len(prices))]
    return_dates = dates[1:]
    if last_36:
        if len(monthly) < 36:
            raise ValueError('Last 36 months requires at least 37 monthly price rows.')
        monthly, return_dates = monthly[-36:], return_dates[-36:]
    series = list(zip(*monthly))
    means = [statistics.mean(values) for values in series]
    deviations = [statistics.stdev(values) for values in series]
    if any(sd <= 0 for sd in deviations):
        raise ValueError('Every asset needs nonzero monthly return volatility.')
    correlation = [[1.0 if i == j else max(-1.0, min(1.0,
        sum((a - means[i]) * (b - means[j]) for a, b in zip(series[i], series[j]))
        / ((len(monthly) - 1) * deviations[i] * deviations[j])))
        for j in range(len(names))] for i in range(len(names))]
    return {'names': names, 'returns': [mean * 12 for mean in means],
            'volatilities': [sd * math.sqrt(12) for sd in deviations],
            'correlations': correlation, 'months': len(monthly),
            'first_return_date': return_dates[0].isoformat(),
            'last_return_date': return_dates[-1].isoformat()}


def largest_weight_change(first, second):
    """Largest absolute weight movement in percentage points; None if no mix."""
    if first is None or second is None:
        return None
    return max(abs(a - b) for a, b in zip(first['weights'], second['weights'])) * 100


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        raise SystemExit(f'Input error: {error}')
