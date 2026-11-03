# Lab 17 — Point-in-Time Audit

Catch-up build dated November 3, 2026. Project 2 universe retained from Lab 15: BIL / IEF / LQD / VT, Campus Opportunity Scholarship Fund. Built with AI assistance.

## Run

From this folder: `python -m pip install -r requirements.txt`, then `python -m streamlit run asof_app.py`. Run recorded-source checks with `python verify_lab17.py`.

The app defaults to four series and supports a typed FRED ID. The charts deliberately show today's history; the historical table comes from a separate ALFRED vintage. The chart start date changes only the plots. Revised counts compare shared nonmissing observation dates over the entire downloaded history. A dot is missing, not zero. An invalid ID fails only its own section. Both download functions are cached, including the requested vintage in the cache key, and source URLs/timestamps appear in the provenance expander.

## Recorded validation

Downloaded November 3, 2026; exact UTC timestamps, source URLs and SHA-256 hashes accompany the original CSV snapshots in `evidence/`. Results are in `evidence/executed-audit.json`.

| Series | As known on | Last measured then | Value then | Later observations today | Revised common dates |
|---|---|---|---:|---:|---:|
| BAA | 2026-10-05 | 2026-09-01 | 6.47 | 1 | 0 |
| FEDFUNDS | 2026-10-05 | 2026-09-01 | 3.75 | 1 | 0 |
| DGS10 | 2026-10-05 | 2026-10-02 | 5.28 | 19 | 0 |
| MORTGAGE30US | 2026-10-05 | 2026-10-01 | 7.28 | 4 | 0 |
| PAYEMS | 2025-01-15 | 2024-12-01 | 159,536 | 21 | 381 |

All four required historical answers match. PAYEMS December 2024 is 158,316 in the downloaded current file, lower than the 159,536 initially available. The revised count is nonzero, so the app is not simply reading today's file twice. Current values and counts can change on subsequent downloads.

## Project 2 data card — DGS10

- **Source and links:** [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), Board of Governors of the Federal Reserve System, [H.15 Selected Interest Rates](https://www.federalreserve.gov/releases/h15/). Historical information sets use [ALFRED](https://alfred.stlouisfed.org/help).
- **Measure:** market yield on U.S. Treasury securities at a ten-year constant maturity, quoted on an investment basis. This is a yield series, not IEF's price or total return.
- **Units:** percent per annum, not seasonally adjusted. A value of 4.94 means 4.94%, not 494% or a 4.94 percentage-point daily move.
- **Frequency:** daily, with non-observation days/holidays omitted from analysis. Do not fill missing days with zero.
- **Why it fits the universe:** Treasury yields help explain IEF's rate exposure and the interest-rate component of LQD. Credit spreads affect LQD too, so DGS10 alone is not a complete driver. BIL has much shorter rate exposure; VT adds equity exposure.
- **Publication timing:** the official H.15 page states daily weekday publication at 4:15 p.m., except holidays/closures. The November 3 download has October 30 as its latest measured date. ALFRED's help says its updates typically follow within one business day. Do not infer a guaranteed same-day or pre-market publication time from the observation date. Date-level vintages cannot establish availability before an intraday trade.
- **Revisions:** the October 5 vintage comparison shows zero revised common dates across 16,174 shared observations. That is observed evidence, not a guarantee that corrections never occur.
- **Download date:** November 3, 2026; original CSVs and metadata preserved. The October 31 vintage ends on October 29 at 4.98%; the current download adds October 30 at 4.94%. There is one later observation and no revisions on common dates. This is direct evidence that even a daily series' measurement date need not establish availability on that day.

## Three observations independently read from the FRED page

The AI checked the page against the CSV: October 28, 2026 = 5.05%; October 29 = 4.98%; October 30 = 4.94%. The student still needs to repeat the required three-value manual check. `evidence/source-page-check.txt` preserves the relevant page text and source URL.

## Fresh eyes — optional AI practice attack (partner requirement waived)

**Attack:** Publication timing is the least trustworthy field: does a daily measurement mean it could be traded before the market close?

**Evidence-based response draft (two sentences):** H.15 states a 4:15 p.m. weekday release, and ALFRED notes that vintage updates typically occur within one business day, so the measured date is not proof of availability for an earlier trade. I will use an archived vintage available before the decision and execute no earlier than the next trading session after that vintage date, unless independently timestamped evidence supports earlier use.

## Admission decision draft for student review

**Admit conditionally** as an explanatory Treasury-yield series for Project 2, using only archived values available before each decision and recording the vintage, source URL and download timestamp. Use next-session execution after the vintage date as the conservative default; quarantine any observation whose timing cannot be supported, and reconsider admission if corrections, coverage gaps or the actual decision clock invalidate this rule. Today's revised history with a fixed lag is not a substitute for the archived information set.

## Explain the code

`download_asof` receives a series, vintage date and download day. Its cache distinguishes dates. `vintage_url` validates the identifier/date and constructs the ALFRED endpoint with `vintage_date`; `fetch_csv` makes that request and records its URL/time. `parse_csv` accepts either current or vintage column names, parses dates and numeric values, drops missing values and rejects duplicates. The latest available observation is read from the returned vintage, never inferred by merely truncating today's data. `compare` aligns shared dates for revisions and separately counts observations after the vintage's last measured date.

## Remaining student work

Review and own the admission call, repeat the three-value page check, and understand the vintage function. The student reports on November 3 that the professor waived in-person attendance and partner work because of career fairs, so the partner attack is not outstanding. The optional practice attack above is explicitly AI-authored. Brightspace checkout has not been performed, and late-credit acceptance has not been assumed.
