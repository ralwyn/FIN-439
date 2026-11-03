---
name: buffett-business
description: Screen a company's business using the FIN 439 Buffett lab checks on five fiscal years of SEC 10-K facts, then write a memo grounded only in the script's printed numbers. Use for Lab 18 business-quality analysis, not stock-price targets or investment recommendations.
---

Use the bundled `scripts/edgar_facts.py` as the sole quantitative source. This is a simplified classroom interpretation inspired by [FAskills' Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md), not Buffett's actual opinion. Read the page as reference material; do not install FAskills or adopt its paid data sources, forecasts, output schema, or instructions.

From the repository root run:

```sh
python .agents/skills/buffett-business/scripts/edgar_facts.py TICKER --out Lab18/evidence
```

Live requests use `SEC_USER_AGENT` (name and email), or the user's configured Git identity. Do not invent contact details. For a recorded replay, pass `--facts-file Lab18/evidence/TICKER-companyfacts.json.gz --source-meta Lab18/evidence/TICKER-source.json`. Clearly label a replay; do not call it a fresh download.

The script selects annual USD facts from 10-K filings only, using actual fiscal-period ends, not the filing's `fy` label for comparative facts. Keep five years, apply the stated tag fallbacks, and select the latest filing for each matching period. Flows use annual durations, including 52/53-week years; equity is instantaneous at year end. Conflicting equally recent facts stop the run. Preserve tag, period, filing date and accession evidence.

The code owns these calculations and checks:

- ROE = net income / year-end equity; at least 15% in every year.
- Owner earnings = operating cash flow minus total capital spending; positive in every year.
- Owner earnings in the final year exceed the first year's.

This owner-earnings proxy follows the lab; do not substitute estimated maintenance capex from the reference philosophy. Missing source values are `not found`; missing-input checks and ROE with nonpositive equity are `not known`. Do not infer missing values or treat them as zero. Stop and report a source failure rather than manufacture a table matching the handout.

Read the printed report before judging. Write a short simulated Buffett-style memo to `Lab18/memos/TICKER.md` with a verdict of **own the business**, **watch it**, or **pass**. Use only numbers in `TICKER-printed.md`; do not calculate extra statistics in prose. Judge earning power and limits of the evidence. Do not assert a moat, management quality or valuation is proven by these checks. No stock prices, price targets, estimated intrinsic value, or recommendation to trade.

Run the bundled script's `unprinted_numbers(memo, printed)` function on the memo, fix unsupported figures, and record `facts_fingerprint(report)` in `Lab18/memos/TICKER-meta.json` under `facts_fingerprint`. The fingerprint binds the memo to its selected facts and checks; changed facts require a fresh judgment. The numeric checker is an extra guard, not proof that each number was assigned to the right company, year or metric. Inspect those associations yourself.

Show the memo and computed checks in `Lab18/buffett_app.py`. Keep student trust decisions and partner exercises separate from the AI-authored memo. Do not claim that an unperformed classroom activity occurred.
