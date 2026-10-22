"""Free Yahoo Finance history via the unofficial yfinance client; no API key."""
import io
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import yfinance as yf
import portfolio as p


def fetch_monthly_prices(ticker_text):
    tickers = list(dict.fromkeys(re.split(r'[\s,;]+', ticker_text.strip().upper())))
    if not 3 <= len(tickers) <= 6 or any(not re.fullmatch(r'[A-Z0-9][A-Z0-9.\-^=]{0,14}', t) for t in tickers):
        raise ValueError('Enter three to six distinct valid tickers, separated by commas.')
    now = datetime.now(ZoneInfo('America/Indiana/Indianapolis'))
    end = now.date().replace(day=1)
    start = end.replace(year=end.year - 5)
    cache = Path(__file__).resolve().parent / '.market-cache'
    cache.mkdir(exist_ok=True)
    yf.set_tz_cache_location(str(cache))
    raw = yf.download(tickers, start=start.isoformat(), end=end.isoformat(),
        interval='1mo', auto_adjust=False, progress=False, threads=False, timeout=20)
    if raw is None or raw.empty or 'Adj Close' not in raw.columns.get_level_values(0):
        raise ValueError('Yahoo returned no adjusted-close history. Check tickers or retry later.')
    prices = raw['Adj Close'].reindex(columns=tickers).sort_index()
    if len(prices) != 60 or prices.isna().any().any() or (prices <= 0).any().any():
        raise ValueError('Each ticker must have 60 complete positive monthly prices. '
                         'No prices were filled or substituted. Check for a newer fund or a failed download.')
    prices.index.name = 'Date'
    csv_text = prices.to_csv(date_format='%Y-%m-%d', float_format='%.8f')
    p.estimate_from_csv(io.StringIO(csv_text))  # shared engine validates months and prices
    record = {'tickers': tickers, 'source': 'Yahoo Finance via yfinance (unofficial client)',
              'downloaded': now.isoformat(timespec='seconds'),
              'start': start.isoformat(), 'end_exclusive': end.isoformat(),
              'field': 'Adj Close', 'auto_adjust': False, 'interval': '1mo',
              'price_rows': len(prices), 'monthly_returns': len(prices) - 1,
              'history_links': {t: f'https://finance.yahoo.com/quote/{t}/history/' for t in tickers}}
    return csv_text, record
