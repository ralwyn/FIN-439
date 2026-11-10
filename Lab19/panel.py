"""Lab 19: shared SEC facts, deterministic checks, separate investor judgments."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import base_facts as base

HERE = Path(__file__).resolve().parent
base.FIELDS.update({'liabilities': ('Liabilities',), 'research_and_development': (
    'ResearchAndDevelopmentExpense', 'ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost')})
base.FLOWS.add('research_and_development')
INVESTORS = ('Buffett', 'Cathie Wood', 'Burry')


def outcome(value, predicate):
    return 'not known' if value is None else ('pass' if predicate(value) else 'fail')


def all_years(values):
    if len(values) != 5 or any(x is None for x in values):
        return 'not known'
    return 'pass' if all(values) else 'fail'


def add_checks(report, threshold=15.0):
    if not 0 <= threshold <= 100:
        raise ValueError('Growth threshold must be between 0 and 100 percent.')
    rows = report['rows']
    for r in rows:
        values = {k: x['value'] for k, x in r['facts'].items()}
        equity, liabilities = values['equity'], values['liabilities']
        rd, revenue = values['research_and_development'], values['revenue']
        r['liabilities_to_equity'] = None if equity is None or equity <= 0 or liabilities is None else liabilities/equity
        r['rd_percent'] = None if rd is None or revenue is None or revenue <= 0 else rd/revenue*100
    first, last = rows[0]['facts']['revenue']['value'], rows[-1]['facts']['revenue']['value']
    growth = None if len(rows) != 5 or first is None or first <= 0 or last is None or last <= 0 else ((last/first)**.25-1)*100
    cash_checks = []
    for r in rows:
        cf, ni = r['facts']['operating_cash_flow']['value'], r['facts']['net_income']['value']
        cash_checks.append(None if cf is None or ni is None else cf >= ni)
    report['growth_percent'] = growth
    report['growth_threshold_percent'] = threshold
    report['panel'] = {
        'Buffett': base.checks(rows),
        'Cathie Wood': {
            f'Revenue CAGR at least {threshold:g}%': outcome(growth, lambda x: x >= threshold),
            'Latest R&D / revenue at least 5%': outcome(rows[-1]['rd_percent'], lambda x: x >= 5)},
        'Burry': {
            'Operating cash flow at least net income every year': all_years(cash_checks),
            'Latest liabilities / equity no more than 2': outcome(rows[-1]['liabilities_to_equity'], lambda x: x <= 2)}}
    return report


def build(ticker='COST', threshold=15, live=False):
    ticker = base.validate_ticker(ticker)
    if live:
        data, source = base.fetch_company(ticker, HERE/'cache')
    else:
        raw = gzip.decompress((HERE/'evidence'/f'{ticker}-companyfacts.json.gz').read_bytes())
        source = json.loads((HERE/'evidence'/f'{ticker}-source.json').read_text())
        digest = hashlib.sha256(raw).hexdigest()
        if digest != source.get('saved_uncompressed_sha256', source['sha256']):
            raise ValueError('Saved SEC source does not match its SHA-256 record.')
        data = json.loads(raw)
    return add_checks(base.build_report(data, ticker, source), threshold)


def printed(report):
    lines = [base.report_text(report), '\n## Panel additions\n',
             '| Fiscal year end | Liabilities USD millions | R&D USD millions | Liabilities / equity | R&D / revenue |',
             '|---|---:|---:|---:|---:|']
    for r in report['rows']:
        ratio = 'not known' if r['liabilities_to_equity'] is None else f"{r['liabilities_to_equity']:.2f}"
        rd = 'not found' if r['rd_percent'] is None else f"{r['rd_percent']:.2f}%"
        lines.append(f"| {r['fiscal_year_end']} | {base.money(r['facts']['liabilities']['value'])} | {base.money(r['facts']['research_and_development']['value'])} | {ratio} | {rd} |")
    for r in report['rows']:
        if r['roe_percent'] is not None:
            lines.append(f"ROE {r['fiscal_year_end']}: {r['roe_percent']:.1f}%")
    g = report['growth_percent']
    lines.append('\nRevenue CAGR: '+('not known' if g is None else f'{g:.2f}%'))
    lines.append(f"Growth threshold: {report['growth_threshold_percent']:g}%")
    lines += ['\n| Investor | Check | Result |', '|---|---|---|']
    for investor, checks in report['panel'].items():
        for check, result in checks.items():
            lines.append(f'| {investor} | {check} | {result} |')
    return '\n'.join(lines)+'\n'


def fingerprint(report):
    return hashlib.sha256(json.dumps({'rows': report['rows'], 'panel': report['panel']}, sort_keys=True).encode()).hexdigest()


def flags(memo, report):
    return base.unprinted_numbers(memo, printed(report))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker', nargs='?', default='COST')
    parser.add_argument('--threshold', type=float, default=15)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--investor', choices=INVESTORS)
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()
    r = build(args.ticker, args.threshold, args.live)
    text = printed(r)
    if args.investor:
        text += '\nSelected perspective: '+args.investor+'\n'+json.dumps(r['panel'][args.investor], indent=2)
    if args.save:
        stem = args.ticker.upper() + (f'-threshold-{args.threshold:g}' if args.threshold != 15 else '')
        (HERE/'evidence'/f'{stem}-panel.json').write_text(json.dumps(r, indent=2)+'\n')
        (HERE/'evidence'/f'{stem}-printed.md').write_text(text)
    print(text)


if __name__ == '__main__':
    main()
