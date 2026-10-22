# FIN 439 — Lab 15 prework

Prepared October 22, 2026. Fictional client and mandate proposed at the student's request; no actual institution or investment account is represented.

## My Project 2 idea: university scholarship fund

The fictional Campus Opportunity Scholarship Fund invests $1 million for at least ten years. It plans to distribute $40,000 each year for scholarships. Its 6.5% nominal annual return objective over rolling five-year periods reflects a 4% annual spending rate plus an assumed 2.5% inflation rate. This is a planning target, not a guaranteed return. Annual rebalancing is assumed. The lab uses arithmetic annualized historical mean returns as estimates; those are not the same as realized compound annual growth over five years.

**One hard constraint:** at least 10% of portfolio value must be allocated to BIL, the designated reserve sleeve. At inception that is $100,000, or 2.5 years of planned $40,000 payments. Only BIL counts toward this reserve; IEF does not because its longer-duration bond prices can fluctuate materially. Review reserve adequacy when spending or portfolio value changes.

The model permits only long-only, fully invested mixes of the four selected ETFs. No leverage or short selling. The optimization criterion is the lowest estimated annualized volatility among mixes meeting the 6.5% expected-return objective and 10% BIL minimum, using the lab's 5-percentage-point search grid. Volatility is a risk measure, not a guaranteed maximum loss. No additional loss cap is invented.

## My fund universe

| Ticker | Fund name | Role | Counts toward reserve? |
|---|---|---|---|
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Near-term scholarship reserve; Treasury-bill exposure | Yes |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government-bond exposure | No |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade corporate fixed income | No |
| VT | Vanguard Total World Stock ETF | Broad global equity growth exposure | No |

These four course-example tickers match the four economic roles and keep the project manageable. This is an educational design, not a claim that these are the best funds. Bond and equity funds can lose value; the reserve sleeve is a traded ETF, not a guaranteed bank deposit.

Issuer references for names and exposure:

- BIL: https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil
- IEF: https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf
- LQD: https://www.ishares.com/us/products/239566/lqd-ishares-iboxx-investment-grade-corporate-bond-etf
- VT: https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf

## Price file and provenance

`prices.csv`: Date first, then BIL, IEF, LQD, VT; oldest month first. Downloaded October 22, 2026 from Yahoo Finance through yfinance. Requested monthly data from October 1, 2021 inclusive to October 1, 2026 exclusive, so the incomplete October 2026 month is excluded. Extracted the explicit **Adj Close** field with `auto_adjust=False` to include Yahoo's distribution/split adjustments.

| Ticker | Source | Download date |
|---|---|---|
| BIL | https://finance.yahoo.com/quote/BIL/history/ | 2026-10-22 |
| IEF | https://finance.yahoo.com/quote/IEF/history/ | 2026-10-22 |
| LQD | https://finance.yahoo.com/quote/LQD/history/ | 2026-10-22 |
| VT | https://finance.yahoo.com/quote/VT/history/ | 2026-10-22 |

Validated: 60 monthly price rows, four tickers, unique dates/months in ascending order, no missing or nonpositive prices. First monthly label 2021-10-01, last 2026-09-01. Monthly labels represent the vendor's month buckets, not necessarily month-end trading dates. 60 price levels give 59 monthly returns. The original Yahoo monthly data is retained in `yahoo-monthly-raw.csv`, and the download script is supplied for reproducibility. No missing prices were forward-filled. Historical adjusted values can be revised by the vendor.

## Streamlit installation and reading

An isolated Python 3.12 environment is available at `Desktop/FIN439/.venv` (the initial setup environment was under work/lab15-venv). Installed Streamlit 1.66.1 and yfinance 1.7.0 plus their dependencies. The system's default Python 3.9 was left alone. Streamlit's Hello demo was launched on http://127.0.0.1:8501.

When a user moves a normal Streamlit control, the script reruns from top to bottom using the new widget values. That is why changing the return estimate can recalculate the allocation automatically. State and caching can preserve selected information across reruns.

Reading: https://docs.streamlit.io/get-started/installation/command-line and https://docs.streamlit.io/get-started/fundamentals/main-concepts through **Data flow**.

## Say this to my partner

“My fictional client is a university scholarship fund with a ten-year horizon. Its target is 6.5% nominal annual return, and its hard constraint is at least 10% in BIL for scholarship reserves. My four funds are BIL, IEF, LQD and VT. The returns we estimate from five years of prices are history, not forecasts.”

## Next in Lab 15

Start the app on Meridian first: objective 6.5%, reserve minimum 3%, with bills and the 10-year note reserve-eligible. Validate the published Meridian answers before uploading this project's CSV. For my universe set the objective to 6.5%, minimum reserve to 10%, and mark only BIL as eligible. Compare all available returns with the last 36 monthly returns. If no mix meets the objective, report that result without lowering the target.

This prework record preserves the preparation details; the completed search/app, stress results and AI-partner attack are in lab15.md.
