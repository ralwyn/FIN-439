"""Lab 13 Meridian mandate checker. Course training case; USD millions / percent.
Run: python3 mandate.py   or python3 mandate.py --verify
AI-assisted implementation, 2026-10-19. No personal AI-off work is claimed.
"""
import argparse
import copy
import math

HOLDINGS = {
    'Cash': ('none', 0, True),
    'Treasury bills': ('U.S. Treasury', 1, True),
    'Treasury 10-year note': ('U.S. Treasury', 1, True),
    'Global equity index fund': ('diversified fund', 2, False),
    'Investment-grade bond fund': ('diversified fund', 3, False),
    'Private real estate fund': ('diversified fund', 90, False),
    'Acme Corp bonds': ('Acme Corp', 4, False),
    'Acme Corp stock': ('Acme Corp', 1, False),
}
NAMES = list(HOLDINGS)
CANDIDATES = {
    'A': [2, 2, 10, 60, 26, 0, 0, 0],
    'B': [1, 0, 0, 55, 20, 15, 5, 4],
    'C': [1, 1, 0, 70, 20, 0, 0, 8],
    # AI attack candidate: checkable constraints alone do not prove suitability.
    'D': [100, 0, 0, 0, 0, 0, 0, 0],
    # Lab 14: the benchmark itself must also face the mandate.
    'E': [0, 0, 0, 60, 40, 0, 0, 0],
}
RESERVE_SIZE = 100.0
QUARTERLY_DISTRIBUTION = .75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT = {'none', 'U.S. Treasury', 'diversified fund'}


def check(weights):
    if len(weights) != len(HOLDINGS) or not all(math.isfinite(w) for w in weights):
        raise ValueError('One finite numeric weight is required for every holding.')
    if RESERVE_SIZE <= 0:
        raise ValueError('Reserve size must be positive.')
    reserve_min = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    reserve = liquid = 0.0
    issuers = {}
    for name, weight in zip(NAMES, weights):
        issuer, days, eligible = HOLDINGS[name]
        if eligible:
            reserve += weight
        if days <= LIQUIDITY_WINDOW:
            liquid += weight
        if issuer not in EXEMPT:
            issuers[issuer] = issuers.get(issuer, 0) + weight
    company = max(issuers.values(), default=0)
    return [
        ('Weights sum to 100', sum(weights), math.isclose(sum(weights), 100, abs_tol=1e-8)),
        ('Long-only: lowest weight', min(weights), min(weights) >= 0),
        (f'Reserve >= {reserve_min:.1f}%', reserve, reserve >= reserve_min - 1e-8),
        (f'Liquid within {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.1f}%', liquid, liquid >= MINIMUM_LIQUID_SHARE - 1e-8),
        (f'Largest single company <= {ISSUER_LIMIT:.1f}%', company, company <= ISSUER_LIMIT + 1e-8),
    ]


def show(name, weights):
    print(f'\nCandidate {name}')
    results = check(weights)
    for label, value, passed in results:
        print(f'{label}: {value:.1f} — {"pass" if passed else "FAIL"}')
    print('Calendar-year loss: requires CIO clarification')
    print('Turnover: not evaluated; current holdings/trades and approval status not supplied.')
    failures = sum(not r[2] for r in results)
    print('passes every checkable rule' if not failures else f'fails {failures} rule(s)')
    return results


def verify():
    # Independent course-authored known answers, rather than snapshots of this code.
    expected = {'A': [100, 0, 14, 100, 0], 'B': [100, 0, 1, 85, 9], 'C': [100, 0, 2, 100, 8]}
    for name, values in expected.items():
        results = check(CANDIDATES[name])
        assert all(math.isclose(r[1], v) for r, v in zip(results, values))
    assert [sum(not r[2] for r in check(CANDIDATES[n])) for n in 'ABC'] == [0, 3, 1]
    probe = copy.deepcopy(CANDIDATES['A'])
    probe[0], probe[3] = -2, 64
    results = show('A long-only probe (temporary)', probe)
    assert [i for i, r in enumerate(results) if not r[2]] == [1]
    assert results[2][1] == 10
    assert all(r[2] for r in check(CANDIDATES['D']))
    assert [i for i, r in enumerate(check(CANDIDATES['E'])) if not r[2]] == [2]
    assert CANDIDATES['A'][0] == 2  # original inputs were not mutated
    print('\nPASS: all published known answers, negative-weight probe, D and benchmark E; base restored.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    print(f'Reserve minimum: {QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100:.1f}%')
    for name, weights in CANDIDATES.items():
        show(name, weights)
    if args.verify:
        verify()
