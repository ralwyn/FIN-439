# FIN 439 — Lab 15: Portfolio Stability

A scholarship-fund portfolio research app built on the same engine as Lab 14. Start with Meridian's training case; then use the sourced BIL/IEF/LQD/VT project history or enter your own ETF tickers through free Yahoo Finance access.

## Start here

- [Lab report and Mermaid engine diagram](lab15.md)
- [Requirement checklist](CHECKLIST.md)
- [Executed validation](validation.txt) and [machine-readable results](executed-results.json)
- [Mandate, fund roles and sources](prework.md), [price provenance](price-sources.md), [monthly adjusted prices](prices.csv)

## Run

Python 3.12 recommended. From this Lab15 directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python portfolio.py
python verify_lab15.py
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
```

Existing Desktop/FIN439 setup: double-click Start-Lab15.command; it uses the shared ../.venv. Open http://127.0.0.1:8502. Use an already-running tab instead of starting a duplicate server on that port.

Meridian opens at 6.5% objective, 3% reserve floor. For the scholarship demo or uploaded prices.csv use 6.5%, 10%, only BIL eligible. The full-history project mix is 60% BIL / 40% VT; the 36-month mix is 85% BIL / 15% VT. These are estimates, not forecasts. All calculations use the unchanged objective; infeasible cases are reported honestly.

## Features and limits

5-point grid search; expected-return edits; reserve eligibility; one-point return stress; all-history/36-month comparison; historical ETF charts; correlation table; source metadata; scenario and prices export. Ticker downloads use the unofficial yfinance client, can be rate-limited and are cached for one hour. Completed calendar months only; missing histories are rejected. Historical ETF growth charts are not backtests of the selected mix. Portfolio statistics do not certify full mandate compliance or future losses.

The local files live in Desktop/FIN439/Lab15. The shared environment, bytecode and market caches are excluded from publication. See FILE-MANIFEST.json for the published package contents and hashes.
