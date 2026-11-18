# Price source record

Download date: 2026-10-22.
Requested period: 2021-10-01 inclusive to 2026-10-01 exclusive; current partial month excluded.
Yahoo Finance monthly Adj Close, downloaded using yfinance with auto_adjust=False.
Dates are Yahoo monthly labels, not necessarily month-end trading dates.
60 monthly price levels yield 59 monthly returns. No missing values were filled.
Historical returns are estimates, not forecasts.

| Ticker | Source |
|---|---|
| BIL | https://finance.yahoo.com/quote/BIL/history/ |
| IEF | https://finance.yahoo.com/quote/IEF/history/ |
| LQD | https://finance.yahoo.com/quote/LQD/history/ |
| VT | https://finance.yahoo.com/quote/VT/history/ |

Validation: 60 rows; oldest first; unique months; no missing or nonpositive values.
First label: 2021-10-01; last label: 2026-09-01.

## Transformation and reproducibility

Saved `prices.csv` SHA-256: `401be7c5bb93e4e4009107f16fd71073987b19600c72948ff25c2cfb42270abf`. Recompute from this repository with `python verify_project.py` and `python engine.py`. The file contains the vendor's adjusted monthly price levels, not raw individual distributions or a point-in-time vintage. For each asset the code calculates each monthly return as current adjusted price divided by prior adjusted price minus one, annualizes the arithmetic mean by multiplying by 12, annualizes sample standard deviation by √12, and derives sample correlations using those same consecutive monthly returns. Portfolio covariance is correlation × the two volatilities. The default sample has 60 price rows / 59 return observations; the alternative uses the last 36 returns / 37 prices. The 59/36 windows are estimates, not independent out-of-sample backtests.

The original yfinance version, complete API response and original retrieval timestamp were not retained; the saved CSV, retrieval date and public history pages are available. Adjustments can change retrospectively, and vendor terms and redistribution rights should be checked before reuse outside this educational project. The estimates inherit vendor errors, selection of four ETFs, the chosen window and survivorship/adjustment limitations. Zero missing prices were filled, and nonconsecutive months or nonpositive prices cause rejection. Transaction costs, reference holdings, the 6.5% target and the 10% floor are explicit scenario/mandate assumptions, not measured quotes or sourced forecasts.
