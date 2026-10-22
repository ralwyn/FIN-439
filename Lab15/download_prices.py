"""Download five years of completed monthly Yahoo adjusted-close observations.
Run with the Lab 15 environment: python download_prices.py BIL IEF LQD VT
These are practice tickers unless adopted against your own mandate.
"""
import argparse
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime
import yfinance as yf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tickers', nargs='+')
    args = parser.parse_args()
    tickers = list(dict.fromkeys(t.upper() for t in args.tickers))
    if not 3 <= len(tickers) <= 6:
        parser.error('Choose three to six distinct fund tickers.')
    here = Path(__file__).resolve().parent
    yf.set_tz_cache_location(str(here / '.yfinance-cache'))
    today = datetime.now(ZoneInfo('America/Indiana/Indianapolis')).date()
    end = today.replace(day=1)  # exclude the unfinished current month
    start = end.replace(year=end.year - 5)
    raw = yf.download(tickers, start=start.isoformat(), end=end.isoformat(),
                      interval='1mo', auto_adjust=False, progress=False, threads=False)
    if raw is None or raw.empty or 'Adj Close' not in raw.columns.get_level_values(0):
        raise SystemExit('Download failed or no Adj Close field; no prices.csv created.')
    prices = raw['Adj Close'].reindex(columns=tickers).sort_index()
    if len(prices) != 60 or prices.isna().any().any() or (prices <= 0).any().any():
        raise SystemExit(f'Expected 60 complete positive monthly prices; received {len(prices)} rows. Inspect source; no prices.csv created.')
    if not prices.index.is_unique or len(set(prices.index.to_period('M'))) != 60:
        raise SystemExit('Duplicate monthly observations; no prices.csv created.')
    raw.to_csv(here / 'yahoo-monthly-raw.csv')
    prices.index.name = 'Date'
    prices.to_csv(here / 'prices.csv', date_format='%Y-%m-%d', float_format='%.8f')
    rows = ['# Price source record', '', f'Download date: {today}.',
            f'Requested period: {start} inclusive to {end} exclusive; current partial month excluded.',
            'Yahoo Finance monthly Adj Close, downloaded using yfinance with auto_adjust=False.',
            'Dates are Yahoo monthly labels, not necessarily month-end trading dates.',
            '60 monthly price levels yield 59 monthly returns. No missing values were filled.',
            'Historical returns are estimates, not forecasts.', '', '| Ticker | Source |', '|---|---|']
    rows += [f'| {t} | https://finance.yahoo.com/quote/{t}/history/ |' for t in tickers]
    rows += ['', f'Validation: {len(prices)} rows; oldest first; unique months; no missing or nonpositive values.',
             f'First label: {prices.index[0].date()}; last label: {prices.index[-1].date()}.']
    (here / 'price-sources.md').write_text('\n'.join(rows) + '\n')
    print('\n'.join(rows))


if __name__ == '__main__':
    main()
